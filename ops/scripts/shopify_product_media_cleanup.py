#!/usr/bin/env python3
"""Audit, prepare, and replace oversized Shopify product images.

The workflow is intentionally split into safe stages:

1. `audit`
   Fetch active product media, aggregate shared files, and write JSON/CSV reports
   ranking the largest originals.
2. `prepare`
   Refresh the selected media URLs, download the originals locally, compress them
   with Pillow, and build a replacement manifest. This does not modify Shopify.
3. `replace`
   Dry-run by default. With `--execute`, stage the prepared files and update the
   existing `MediaImage` records in place via `fileUpdate`, which preserves file
   references instead of deleting and re-adding media.

Credentials:
  - `--store-domain`, or `SHOPIFY_STORE_DOMAIN`
  - `--access-token`, or `SHOPIFY_ADMIN_ACCESS_TOKEN`
  - fallback token file: ~/.config/dresslikemommy/translation-helper-token.json

Typical usage:
  python3 ops/scripts/shopify_product_media_cleanup.py audit
  python3 ops/scripts/shopify_product_media_cleanup.py prepare --preset balanced --limit 50
  python3 ops/scripts/shopify_product_media_cleanup.py replace
  python3 ops/scripts/shopify_product_media_cleanup.py replace --execute --batch-size 10
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import mimetypes
import os
import random
import re
import sys
import time
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple
from urllib.parse import urlparse

import requests
from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT_DIR = ROOT / "tmp" / "shopify-media-cleanup"
DEFAULT_TOKEN_PATH = Path.home() / ".config" / "dresslikemommy" / "translation-helper-token.json"
DEFAULT_STORE_DOMAIN = os.environ.get("SHOPIFY_STORE_DOMAIN", "dresslikemommy-com.myshopify.com")
DEFAULT_API_VERSION = os.environ.get(
    "SHOPIFY_ADMIN_API_VERSION",
    os.environ.get("SHOPIFY_API_VERSION", "2026-01"),
)
DEFAULT_PRODUCT_QUERY = "status:active"
DEFAULT_AUDIT_JSON = DEFAULT_OUTPUT_DIR / "shopify-product-media-audit.json"
DEFAULT_AUDIT_CSV = DEFAULT_OUTPUT_DIR / "shopify-product-media-audit.csv"
DEFAULT_FLAGGED_CSV = DEFAULT_OUTPUT_DIR / "shopify-product-media-flagged.csv"
DEFAULT_MANIFEST = DEFAULT_OUTPUT_DIR / "shopify-product-media-replacement-manifest.json"
DEFAULT_REPLACE_RESULTS = DEFAULT_OUTPUT_DIR / "shopify-product-media-replace-results.json"

DEFAULT_FLAG_FILE_SIZE_MB = 2.5
DEFAULT_FLAG_MAX_DIMENSION = 3000
DEFAULT_FLAG_MEGAPIXELS = 8.0

MIN_JPEG_QUALITY = 40
MAX_JPEG_QUALITY = 95
READY_FILE_STATUSES = {"READY"}
PROCESSING_FILE_STATUSES = {"UPLOADED", "PROCESSING"}
FAILURE_FILE_STATUSES = {"FAILED"}
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}

PRESET_CONFIGS: Dict[str, Dict[str, Any]] = {
    "conservative": {
        "target_max_dimension": 2600,
        "jpeg_quality": 88,
        "webp_quality": 86,
        "png_quantize_colors": None,
        "min_savings_percent": 0.05,
        "min_savings_bytes": 50 * 1024,
    },
    "balanced": {
        "target_max_dimension": 2200,
        "jpeg_quality": 82,
        "webp_quality": 80,
        "png_quantize_colors": None,
        "min_savings_percent": 0.08,
        "min_savings_bytes": 80 * 1024,
    },
    "aggressive": {
        "target_max_dimension": 1800,
        "jpeg_quality": 74,
        "webp_quality": 72,
        "png_quantize_colors": 256,
        "min_savings_percent": 0.12,
        "min_savings_bytes": 120 * 1024,
    },
}

PRODUCT_MEDIA_QUERY = """
query ProductMediaAudit($first: Int!, $after: String, $query: String) {
  products(first: $first, after: $after, query: $query, sortKey: UPDATED_AT) {
    pageInfo {
      hasNextPage
      endCursor
    }
    nodes {
      id
      handle
      title
      status
      media(first: 250) {
        nodes {
          __typename
          id
          alt
          mediaContentType
          status
          ... on MediaImage {
            fileStatus
            fileErrors {
              code
              message
              details
            }
            image {
              url
              width
              height
            }
            originalSource {
              fileSize
              url
            }
          }
        }
      }
    }
  }
}
"""

MEDIA_BY_IDS_QUERY = """
query MediaByIds($ids: [ID!]!) {
  nodes(ids: $ids) {
    __typename
    ... on MediaImage {
      id
      alt
      fileStatus
      fileErrors {
        code
        message
        details
      }
      image {
        url
        width
        height
      }
      originalSource {
        fileSize
        url
      }
    }
  }
}
"""

STAGED_UPLOADS_CREATE_MUTATION = """
mutation StagedUploadsCreate($input: [StagedUploadInput!]!) {
  stagedUploadsCreate(input: $input) {
    stagedTargets {
      url
      resourceUrl
      parameters {
        name
        value
      }
    }
    userErrors {
      field
      message
    }
  }
}
"""

FILE_UPDATE_MUTATION = """
mutation FileUpdate($files: [FileUpdateInput!]!) {
  fileUpdate(files: $files) {
    files {
      id
      alt
      fileStatus
      ... on MediaImage {
        image {
          width
          height
        }
        fileErrors {
          code
          message
          details
        }
      }
    }
    userErrors {
      field
      message
      code
    }
  }
}
"""


@dataclass(frozen=True)
class Thresholds:
    file_size_bytes: int
    max_dimension: int
    megapixels: float


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def clean(value: object) -> str:
    return str(value or "").strip()


def normalize_store_domain(raw_domain: str) -> str:
    value = clean(raw_domain)
    value = value.replace("https://", "").replace("http://", "")
    return value.rstrip("/")


def require_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def bytes_to_mb(num_bytes: Optional[int]) -> float:
    if not num_bytes:
        return 0.0
    return num_bytes / (1024 * 1024)


def percent_saved(before: int, after: int) -> float:
    if before <= 0:
        return 0.0
    return ((before - after) / before) * 100.0


def clamp_quality(value: int) -> int:
    return max(MIN_JPEG_QUALITY, min(MAX_JPEG_QUALITY, value))


def path_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def safe_slug(value: str, fallback: str) -> str:
    slug = re.sub(r"[^a-z0-9._-]+", "-", clean(value).lower()).strip("-._")
    return slug or fallback


def url_extension(url: str) -> str:
    suffix = Path(urlparse(clean(url)).path).suffix.lower()
    return suffix


def guess_mime_type(filename: str, fallback_extension: str = "") -> str:
    guessed, _ = mimetypes.guess_type(filename)
    if guessed:
        return guessed
    if fallback_extension in {".jpg", ".jpeg"}:
        return "image/jpeg"
    if fallback_extension == ".png":
        return "image/png"
    if fallback_extension == ".webp":
        return "image/webp"
    if fallback_extension == ".gif":
        return "image/gif"
    return "application/octet-stream"


def load_token(token_path: Path = DEFAULT_TOKEN_PATH) -> Optional[str]:
    if not token_path.exists():
        return None
    payload = json.loads(token_path.read_text(encoding="utf-8"))
    token = clean(payload.get("access_token"))
    return token or None


def resolve_access_token(explicit_token: str) -> str:
    token = clean(explicit_token) or clean(os.environ.get("SHOPIFY_ADMIN_ACCESS_TOKEN", ""))
    if token:
        return token
    fallback = load_token()
    if fallback:
        return fallback
    raise RuntimeError(
        "Missing Shopify Admin access token. Pass --access-token, set "
        "SHOPIFY_ADMIN_ACCESS_TOKEN, or provide the local token file."
    )


def chunked(items: Sequence[Any], chunk_size: int) -> Iterable[Sequence[Any]]:
    for index in range(0, len(items), chunk_size):
        yield items[index:index + chunk_size]


class ShopifyClient:
    def __init__(self, store_domain: str, access_token: str, api_version: str):
        self.store_domain = normalize_store_domain(store_domain)
        self.endpoint = f"https://{self.store_domain}/admin/api/{api_version}/graphql.json"
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "X-Shopify-Access-Token": access_token,
            }
        )

    def graphql(self, query: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        payload = {"query": query, "variables": variables or {}}
        for attempt in range(1, 7):
            response = self.session.post(self.endpoint, json=payload, timeout=90)
            if response.status_code == 429 and attempt < 6:
                time.sleep(min(12.0, (1.5 ** attempt) + random.uniform(0.1, 0.7)))
                continue
            response.raise_for_status()
            data = response.json()
            errors = data.get("errors") or []
            if not errors:
                return data.get("data", {})
            codes = {item.get("extensions", {}).get("code") for item in errors}
            if "THROTTLED" in codes and attempt < 6:
                time.sleep(min(12.0, (1.5 ** attempt) + random.uniform(0.1, 0.7)))
                continue
            raise RuntimeError(f"Shopify GraphQL errors: {json.dumps(errors, ensure_ascii=False)}")
        raise RuntimeError("Shopify GraphQL request failed after retries.")

    def iter_product_media(
        self,
        *,
        product_query: str,
        page_size: int,
        max_products: int,
    ) -> Iterable[Dict[str, Any]]:
        cursor: Optional[str] = None
        seen = 0
        while True:
            data = self.graphql(
                PRODUCT_MEDIA_QUERY,
                {"first": page_size, "after": cursor, "query": product_query or None},
            )
            root = data["products"]
            nodes = root.get("nodes", [])
            for node in nodes:
                yield node
                seen += 1
                if max_products and seen >= max_products:
                    return
            if not root["pageInfo"]["hasNextPage"]:
                return
            cursor = root["pageInfo"]["endCursor"]

    def media_by_ids(self, media_ids: Sequence[str]) -> Dict[str, Dict[str, Any]]:
        result: Dict[str, Dict[str, Any]] = {}
        for batch in chunked(list(media_ids), 100):
            data = self.graphql(MEDIA_BY_IDS_QUERY, {"ids": list(batch)})
            for node in data.get("nodes", []) or []:
                if not node or node.get("__typename") != "MediaImage":
                    continue
                result[clean(node.get("id"))] = node
        return result

    def staged_uploads_create(self, files: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
        data = self.graphql(STAGED_UPLOADS_CREATE_MUTATION, {"input": list(files)})
        payload = data["stagedUploadsCreate"]
        user_errors = payload.get("userErrors", [])
        if user_errors:
            raise RuntimeError(
                "stagedUploadsCreate failed: "
                + json.dumps(user_errors, ensure_ascii=False)
            )
        return payload.get("stagedTargets", [])

    def file_update(self, files: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
        data = self.graphql(FILE_UPDATE_MUTATION, {"files": list(files)})
        return data["fileUpdate"]


def build_thresholds(args: argparse.Namespace) -> Thresholds:
    return Thresholds(
        file_size_bytes=int(float(args.flag_file_size_mb) * 1024 * 1024),
        max_dimension=int(args.flag_max_dimension),
        megapixels=float(args.flag_megapixels),
    )


def media_record_from_node(node: Dict[str, Any]) -> Dict[str, Any]:
    original_source = node.get("originalSource") or {}
    image = node.get("image") or {}
    original_url = clean(original_source.get("url"))
    processed_url = clean(image.get("url"))
    extension = url_extension(original_url) or url_extension(processed_url)
    width = int(image.get("width") or 0)
    height = int(image.get("height") or 0)
    file_size = int(original_source.get("fileSize") or 0)
    max_dimension = max(width, height)
    megapixels = round((width * height) / 1_000_000, 2) if width and height else 0.0

    return {
        "media_id": clean(node.get("id")),
        "alt": clean(node.get("alt")),
        "media_content_type": clean(node.get("mediaContentType")),
        "status": clean(node.get("status")),
        "file_status": clean(node.get("fileStatus")),
        "file_errors": node.get("fileErrors") or [],
        "original": {
            "url": original_url,
            "bytes": file_size,
            "extension": extension.lower(),
            "mime_type": guess_mime_type(f"image{extension}", extension.lower()),
        },
        "image": {
            "url": processed_url,
            "width": width,
            "height": height,
            "max_dimension": max_dimension,
            "megapixels": megapixels,
        },
        "references": [],
        "reference_count": 0,
        "flagged": False,
        "flag_reasons": [],
    }


def merge_media_records(base: Dict[str, Any], fresh: Dict[str, Any]) -> None:
    if not base["alt"] and fresh["alt"]:
        base["alt"] = fresh["alt"]
    if not base["original"]["url"] and fresh["original"]["url"]:
        base["original"]["url"] = fresh["original"]["url"]
    if fresh["original"]["bytes"] and fresh["original"]["bytes"] > base["original"]["bytes"]:
        base["original"]["bytes"] = fresh["original"]["bytes"]
    if fresh["original"]["extension"] and not base["original"]["extension"]:
        base["original"]["extension"] = fresh["original"]["extension"]
    if fresh["original"]["mime_type"] and base["original"]["mime_type"] == "application/octet-stream":
        base["original"]["mime_type"] = fresh["original"]["mime_type"]
    if fresh["image"]["width"] and fresh["image"]["height"]:
        base["image"] = fresh["image"]
    if fresh["file_status"]:
        base["file_status"] = fresh["file_status"]
    if fresh["status"]:
        base["status"] = fresh["status"]
    if fresh["file_errors"]:
        base["file_errors"] = fresh["file_errors"]


def apply_flags(record: Dict[str, Any], thresholds: Thresholds) -> None:
    reasons: List[str] = []
    original_bytes = int(record["original"]["bytes"] or 0)
    max_dimension = int(record["image"]["max_dimension"] or 0)
    megapixels = float(record["image"]["megapixels"] or 0.0)

    if original_bytes and original_bytes > thresholds.file_size_bytes:
        reasons.append("file_size")
    if max_dimension and max_dimension > thresholds.max_dimension:
        reasons.append("max_dimension")
    if megapixels and megapixels > thresholds.megapixels:
        reasons.append("megapixels")

    record["flagged"] = bool(reasons)
    record["flag_reasons"] = reasons


def sort_media_records(records: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return sorted(
        records,
        key=lambda item: (
            int(item["original"]["bytes"] or 0),
            int(item["image"]["max_dimension"] or 0),
            float(item["image"]["megapixels"] or 0.0),
            item["media_id"],
        ),
        reverse=True,
    )


def build_audit_summary(records: Sequence[Dict[str, Any]], product_count: int) -> Dict[str, Any]:
    total_original_bytes = sum(int(item["original"]["bytes"] or 0) for item in records)
    flagged_records = [item for item in records if item["flagged"]]
    flagged_original_bytes = sum(int(item["original"]["bytes"] or 0) for item in flagged_records)
    shared_records = [item for item in records if int(item["reference_count"]) > 1]

    return {
        "products_scanned": product_count,
        "unique_media_images": len(records),
        "flagged_media_images": len(flagged_records),
        "shared_media_images": len(shared_records),
        "product_media_references": sum(int(item["reference_count"]) for item in records),
        "total_original_bytes": total_original_bytes,
        "total_original_mb": round(bytes_to_mb(total_original_bytes), 2),
        "flagged_original_bytes": flagged_original_bytes,
        "flagged_original_mb": round(bytes_to_mb(flagged_original_bytes), 2),
        "largest_media_id": records[0]["media_id"] if records else "",
        "largest_file_mb": round(bytes_to_mb(records[0]["original"]["bytes"]), 2) if records else 0.0,
    }


def write_json(path: Path, payload: Dict[str, Any]) -> None:
    require_parent(path)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_audit_csv(path: Path, records: Sequence[Dict[str, Any]], flagged_only: bool) -> None:
    require_parent(path)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "media_id",
                "reference_count",
                "product_handles",
                "file_status",
                "file_size_bytes",
                "file_size_mb",
                "width",
                "height",
                "max_dimension",
                "megapixels",
                "extension",
                "mime_type",
                "flagged",
                "flag_reasons",
                "alt",
                "original_url",
                "processed_url",
            ],
        )
        writer.writeheader()
        for item in records:
            if flagged_only and not item["flagged"]:
                continue
            handles = [
                f"{ref['product_handle']}#{ref['position']}"
                for ref in item["references"]
            ]
            writer.writerow(
                {
                    "media_id": item["media_id"],
                    "reference_count": item["reference_count"],
                    "product_handles": ";".join(handles),
                    "file_status": item["file_status"],
                    "file_size_bytes": item["original"]["bytes"],
                    "file_size_mb": f"{bytes_to_mb(item['original']['bytes']):.2f}",
                    "width": item["image"]["width"],
                    "height": item["image"]["height"],
                    "max_dimension": item["image"]["max_dimension"],
                    "megapixels": item["image"]["megapixels"],
                    "extension": item["original"]["extension"],
                    "mime_type": item["original"]["mime_type"],
                    "flagged": str(item["flagged"]).lower(),
                    "flag_reasons": ",".join(item["flag_reasons"]),
                    "alt": item["alt"],
                    "original_url": item["original"]["url"],
                    "processed_url": item["image"]["url"],
                }
            )


def fetch_audit_data(client: ShopifyClient, args: argparse.Namespace) -> Tuple[List[Dict[str, Any]], int]:
    media_map: Dict[str, Dict[str, Any]] = {}
    product_count = 0
    thresholds = build_thresholds(args)

    for product in client.iter_product_media(
        product_query=args.product_query,
        page_size=args.page_size,
        max_products=args.max_products,
    ):
        product_count += 1
        media_nodes = ((product.get("media") or {}).get("nodes") or [])
        for position, node in enumerate(media_nodes, start=1):
            if node.get("__typename") != "MediaImage":
                continue
            media_id = clean(node.get("id"))
            if not media_id:
                continue
            record = media_map.get(media_id)
            fresh_record = media_record_from_node(node)
            if record is None:
                record = fresh_record
                media_map[media_id] = record
            else:
                merge_media_records(record, fresh_record)

            record["references"].append(
                {
                    "product_id": clean(product.get("id")),
                    "product_handle": clean(product.get("handle")),
                    "product_title": clean(product.get("title")),
                    "product_status": clean(product.get("status")),
                    "position": position,
                }
            )
            record["reference_count"] = len(record["references"])

    records = sort_media_records(list(media_map.values()))
    for record in records:
        apply_flags(record, thresholds)
    return records, product_count


def print_audit_summary(summary: Dict[str, Any], records: Sequence[Dict[str, Any]], limit: int) -> None:
    print(f"Products scanned: {summary['products_scanned']}")
    print(f"Unique media images: {summary['unique_media_images']}")
    print(f"Flagged media images: {summary['flagged_media_images']}")
    print(f"Shared media images: {summary['shared_media_images']}")
    print(f"Total original MB: {summary['total_original_mb']:.2f}")
    print(f"Flagged original MB: {summary['flagged_original_mb']:.2f}")

    flagged = [item for item in records if item["flagged"]]
    if not flagged:
        return

    sample = flagged[:limit]
    print("")
    print(f"Top flagged media (showing {len(sample)} of {len(flagged)}):")
    for item in sample:
        refs = ", ".join(ref["product_handle"] for ref in item["references"][:3])
        print(
            "- "
            f"{item['media_id']} "
            f"{bytes_to_mb(item['original']['bytes']):.2f} MB "
            f"{item['image']['width']}x{item['image']['height']} "
            f"[{', '.join(item['flag_reasons'])}] "
            f"{refs}"
        )


def fresh_media_snapshot(node: Dict[str, Any]) -> Dict[str, Any]:
    original_source = node.get("originalSource") or {}
    image = node.get("image") or {}
    original_url = clean(original_source.get("url"))
    extension = url_extension(original_url) or url_extension(clean(image.get("url")))
    return {
        "media_id": clean(node.get("id")),
        "alt": clean(node.get("alt")),
        "file_status": clean(node.get("fileStatus")),
        "file_errors": node.get("fileErrors") or [],
        "original": {
            "url": original_url,
            "bytes": int(original_source.get("fileSize") or 0),
            "extension": extension.lower(),
            "mime_type": guess_mime_type(f"image{extension}", extension.lower()),
        },
        "image": {
            "url": clean(image.get("url")),
            "width": int(image.get("width") or 0),
            "height": int(image.get("height") or 0),
        },
    }


def source_drifted(audit_record: Dict[str, Any], live_record: Dict[str, Any]) -> bool:
    expected = audit_record["original"]
    expected_image = audit_record["image"]
    live_original = live_record["original"]
    live_image = live_record["image"]
    return any(
        [
            int(expected.get("bytes") or 0) != int(live_original.get("bytes") or 0),
            int(expected_image.get("width") or 0) != int(live_image.get("width") or 0),
            int(expected_image.get("height") or 0) != int(live_image.get("height") or 0),
        ]
    )


def download_media(url: str, target_path: Path) -> Tuple[Path, int, str]:
    require_parent(target_path)
    response = requests.get(url, stream=True, timeout=120)
    response.raise_for_status()
    content_type = clean(response.headers.get("Content-Type")).split(";", 1)[0]
    with target_path.open("wb") as handle:
        for chunk in response.iter_content(chunk_size=1024 * 1024):
            if chunk:
                handle.write(chunk)
    return target_path, target_path.stat().st_size, content_type


def resize_dimensions(width: int, height: int, target_max_dimension: int) -> Tuple[int, int]:
    if width <= 0 or height <= 0:
        return width, height
    largest = max(width, height)
    if largest <= target_max_dimension:
        return width, height
    scale = target_max_dimension / float(largest)
    return max(1, int(round(width * scale))), max(1, int(round(height * scale)))


def optimize_png_image(image: Image.Image, colors: Optional[int]) -> Image.Image:
    working = image
    if colors:
        if "A" in working.getbands():
            working = working.convert("RGBA").quantize(colors=colors)
        else:
            working = working.convert("RGB").quantize(colors=colors)
    return working


def compress_image(
    source_path: Path,
    destination_path: Path,
    *,
    extension: str,
    config: Dict[str, Any],
) -> Dict[str, Any]:
    require_parent(destination_path)
    extension = extension.lower()

    with Image.open(source_path) as opened:
        if getattr(opened, "is_animated", False):
            raise RuntimeError("Animated images are skipped to avoid frame loss.")

        image = ImageOps.exif_transpose(opened)
        original_width, original_height = image.size
        target_width, target_height = resize_dimensions(
            original_width,
            original_height,
            int(config["target_max_dimension"]),
        )
        resized = image
        if (target_width, target_height) != image.size:
            resized = image.resize((target_width, target_height), Image.Resampling.LANCZOS)

        save_kwargs: Dict[str, Any] = {}
        if extension in {".jpg", ".jpeg"}:
            final = resized.convert("RGB")
            save_kwargs = {
                "format": "JPEG",
                "quality": clamp_quality(int(config["jpeg_quality"])),
                "optimize": True,
                "progressive": True,
            }
        elif extension == ".png":
            final = optimize_png_image(resized, config.get("png_quantize_colors"))
            save_kwargs = {
                "format": "PNG",
                "optimize": True,
                "compress_level": 9,
            }
        elif extension == ".webp":
            final = resized
            save_kwargs = {
                "format": "WEBP",
                "quality": clamp_quality(int(config["webp_quality"])),
                "method": 6,
            }
        elif extension == ".gif":
            final = resized
            save_kwargs = {
                "format": "GIF",
                "optimize": True,
            }
        else:
            raise RuntimeError(f"Unsupported file type for compression: {extension or 'unknown'}")

        final.save(destination_path, **save_kwargs)
        output_size = destination_path.stat().st_size
        return {
            "path": str(destination_path),
            "bytes": output_size,
            "sha256": path_sha256(destination_path),
            "mime_type": guess_mime_type(destination_path.name, extension),
            "width": target_width,
            "height": target_height,
        }


def manifest_entry_from_record(
    audit_record: Dict[str, Any],
    live_record: Dict[str, Any],
    original_path: Path,
    original_size: int,
    replacement: Optional[Dict[str, Any]],
    skip_reason: str,
) -> Dict[str, Any]:
    original_file_path = str(original_path) if original_path and original_path.is_file() else ""
    original_file_sha = path_sha256(original_path) if original_path and original_path.is_file() else ""
    entry = {
        "media_id": audit_record["media_id"],
        "alt": audit_record["alt"],
        "references": audit_record["references"],
        "reference_count": audit_record["reference_count"],
        "flag_reasons": audit_record["flag_reasons"],
        "source_snapshot": {
            "bytes": live_record["original"]["bytes"],
            "width": live_record["image"]["width"],
            "height": live_record["image"]["height"],
            "extension": live_record["original"]["extension"],
            "mime_type": live_record["original"]["mime_type"],
            "file_status": live_record["file_status"],
        },
        "downloaded_original": {
            "path": original_file_path,
            "bytes": int(original_size or 0),
            "sha256": original_file_sha,
        },
        "replacement": replacement or {},
        "ready_for_upload": bool(replacement),
        "skip_reason": clean(skip_reason),
    }
    if replacement:
        before = int(live_record["original"]["bytes"] or 0)
        after = int(replacement["bytes"] or 0)
        entry["savings"] = {
            "bytes": before - after,
            "percent": round(percent_saved(before, after), 2),
        }
    else:
        entry["savings"] = {"bytes": 0, "percent": 0.0}
    return entry


def parse_error_index(field: Any) -> Optional[int]:
    if not isinstance(field, list):
        return None
    for item in field:
        if isinstance(item, int):
            return item
        if isinstance(item, str) and item.isdigit():
            return int(item)
    return None


def stage_upload_file(target: Dict[str, Any], local_path: Path, mime_type: str) -> None:
    parameters = {item["name"]: item["value"] for item in target.get("parameters", [])}
    with local_path.open("rb") as handle:
        response = requests.post(
            target["url"],
            data=parameters,
            files={"file": (local_path.name, handle, mime_type)},
            timeout=300,
        )
    response.raise_for_status()


def wait_for_file_statuses(
    client: ShopifyClient,
    media_ids: Sequence[str],
    *,
    timeout_seconds: int,
    poll_interval_seconds: float,
) -> Dict[str, Dict[str, Any]]:
    deadline = time.time() + timeout_seconds
    last_snapshot: Dict[str, Dict[str, Any]] = {}

    while True:
        last_snapshot = {
            media_id: fresh_media_snapshot(node)
            for media_id, node in client.media_by_ids(media_ids).items()
        }
        pending = [
            media_id
            for media_id, snapshot in last_snapshot.items()
            if snapshot["file_status"] in PROCESSING_FILE_STATUSES
        ]
        if not pending:
            return last_snapshot
        if time.time() >= deadline:
            return last_snapshot
        time.sleep(poll_interval_seconds)


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--store-domain",
        default=DEFAULT_STORE_DOMAIN,
        help=f"Shopify store domain. Defaults to {DEFAULT_STORE_DOMAIN}.",
    )
    parser.add_argument(
        "--access-token",
        default=os.environ.get("SHOPIFY_ADMIN_ACCESS_TOKEN", ""),
        help="Shopify Admin API access token. Falls back to env or local token file.",
    )
    parser.add_argument(
        "--api-version",
        default=DEFAULT_API_VERSION,
        help=f"Shopify Admin API version (default: {DEFAULT_API_VERSION}).",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Directory for reports and manifests (default: {DEFAULT_OUTPUT_DIR}).",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    audit = subparsers.add_parser("audit", help="Fetch product media sizes and write audit reports.")
    audit.add_argument("--product-query", default=DEFAULT_PRODUCT_QUERY, help="Shopify product search query.")
    audit.add_argument("--page-size", type=int, default=50, help="Products to fetch per request.")
    audit.add_argument("--max-products", type=int, default=0, help="Optional product cap for testing.")
    audit.add_argument(
        "--flag-file-size-mb",
        type=float,
        default=DEFAULT_FLAG_FILE_SIZE_MB,
        help=f"Flag originals larger than this many MB (default: {DEFAULT_FLAG_FILE_SIZE_MB}).",
    )
    audit.add_argument(
        "--flag-max-dimension",
        type=int,
        default=DEFAULT_FLAG_MAX_DIMENSION,
        help=f"Flag images larger than this max dimension (default: {DEFAULT_FLAG_MAX_DIMENSION}).",
    )
    audit.add_argument(
        "--flag-megapixels",
        type=float,
        default=DEFAULT_FLAG_MEGAPIXELS,
        help=f"Flag images larger than this many megapixels (default: {DEFAULT_FLAG_MEGAPIXELS}).",
    )
    audit.add_argument("--audit-json", type=Path, default=DEFAULT_AUDIT_JSON)
    audit.add_argument("--audit-csv", type=Path, default=DEFAULT_AUDIT_CSV)
    audit.add_argument("--flagged-csv", type=Path, default=DEFAULT_FLAGGED_CSV)
    audit.add_argument("--sample-limit", type=int, default=15, help="Top flagged rows to print.")

    prepare = subparsers.add_parser(
        "prepare",
        help="Download selected originals locally, compress them, and write a replacement manifest.",
    )
    prepare.add_argument("--audit-json", type=Path, default=DEFAULT_AUDIT_JSON)
    prepare.add_argument(
        "--preset",
        choices=sorted(PRESET_CONFIGS.keys()),
        default="balanced",
        help="Compression preset.",
    )
    prepare.add_argument("--limit", type=int, default=0, help="Optional limit on selected media files.")
    prepare.add_argument(
        "--include-unflagged",
        action="store_true",
        help="Prepare from all audited media instead of flagged rows only.",
    )
    prepare.add_argument(
        "--allow-source-drift",
        action="store_true",
        help="Allow prepare to continue if the live file size or dimensions changed since the audit.",
    )
    prepare.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)

    replace = subparsers.add_parser(
        "replace",
        help="Dry-run or execute Shopify fileUpdate replacements from a prepared manifest.",
    )
    replace.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    replace.add_argument("--execute", action="store_true", help="Apply updates to Shopify.")
    replace.add_argument("--limit", type=int, default=0, help="Optional cap on manifest entries.")
    replace.add_argument("--batch-size", type=int, default=10, help="Files to update per batch.")
    replace.add_argument(
        "--force",
        action="store_true",
        help="Allow replacement when the live file drifted from the manifest source snapshot.",
    )
    replace.add_argument(
        "--poll-timeout-seconds",
        type=int,
        default=600,
        help="How long to wait for Shopify file processing before returning.",
    )
    replace.add_argument(
        "--poll-interval-seconds",
        type=float,
        default=3.0,
        help="How often to poll Shopify for file status.",
    )
    replace.add_argument("--results-json", type=Path, default=DEFAULT_REPLACE_RESULTS)

    return parser.parse_args(argv)


def run_audit(args: argparse.Namespace) -> int:
    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    client = ShopifyClient(
        store_domain=args.store_domain,
        access_token=resolve_access_token(args.access_token),
        api_version=args.api_version,
    )

    records, product_count = fetch_audit_data(client, args)
    thresholds = build_thresholds(args)
    summary = build_audit_summary(records, product_count)
    payload = {
        "generated_at": utc_now(),
        "store_domain": normalize_store_domain(args.store_domain),
        "api_version": args.api_version,
        "product_query": args.product_query,
        "thresholds": {
            "flag_file_size_mb": round(bytes_to_mb(thresholds.file_size_bytes), 2),
            "flag_file_size_bytes": thresholds.file_size_bytes,
            "flag_max_dimension": thresholds.max_dimension,
            "flag_megapixels": thresholds.megapixels,
        },
        "summary": summary,
        "records": records,
    }

    write_json(args.audit_json, payload)
    write_audit_csv(args.audit_csv, records, flagged_only=False)
    write_audit_csv(args.flagged_csv, records, flagged_only=True)
    print_audit_summary(summary, [item for item in records if item["flagged"]], args.sample_limit)
    print("")
    print(f"Audit JSON: {args.audit_json}")
    print(f"Audit CSV: {args.audit_csv}")
    print(f"Flagged CSV: {args.flagged_csv}")
    return 0


def select_audit_records(audit_payload: Dict[str, Any], include_unflagged: bool, limit: int) -> List[Dict[str, Any]]:
    records = audit_payload.get("records", []) or []
    if not include_unflagged:
        records = [item for item in records if item.get("flagged")]
    if limit > 0:
        records = records[:limit]
    return records


def run_prepare(args: argparse.Namespace) -> int:
    if not args.audit_json.exists():
        raise FileNotFoundError(f"Audit JSON not found: {args.audit_json}")

    audit_payload = json.loads(args.audit_json.read_text(encoding="utf-8"))
    selected_records = select_audit_records(audit_payload, args.include_unflagged, args.limit)
    if not selected_records:
        print("No audit records selected for preparation.")
        return 0

    client = ShopifyClient(
        store_domain=args.store_domain,
        access_token=resolve_access_token(args.access_token),
        api_version=args.api_version,
    )
    preset = deepcopy(PRESET_CONFIGS[args.preset])
    media_ids = [item["media_id"] for item in selected_records]
    live_map = {
        media_id: fresh_media_snapshot(node)
        for media_id, node in client.media_by_ids(media_ids).items()
    }

    output_dir = args.output_dir
    originals_dir = output_dir / "originals"
    prepared_dir = output_dir / "prepared" / args.preset
    output_dir.mkdir(parents=True, exist_ok=True)

    entries: List[Dict[str, Any]] = []
    prepared_count = 0
    total_before = 0
    total_after = 0

    for audit_record in selected_records:
        media_id = audit_record["media_id"]
        live_record = live_map.get(media_id)
        if not live_record:
            entries.append(
                manifest_entry_from_record(
                    audit_record,
                    {
                        "original": {"bytes": 0, "extension": "", "mime_type": "", "url": ""},
                        "image": {"width": 0, "height": 0, "url": ""},
                        "file_status": "",
                    },
                    Path(),
                    0,
                    None,
                    "media_not_found",
                )
            )
            continue

        if live_record["file_status"] not in READY_FILE_STATUSES:
            entries.append(
                manifest_entry_from_record(
                    audit_record,
                    live_record,
                    Path(),
                    0,
                    None,
                    f"live_file_status_{live_record['file_status'].lower() or 'unknown'}",
                )
            )
            continue

        if source_drifted(audit_record, live_record) and not args.allow_source_drift:
            entries.append(
                manifest_entry_from_record(
                    audit_record,
                    live_record,
                    Path(),
                    0,
                    None,
                    "source_drifted_since_audit",
                )
            )
            continue

        extension = clean(live_record["original"]["extension"]).lower()
        if extension not in SUPPORTED_EXTENSIONS:
            entries.append(
                manifest_entry_from_record(
                    audit_record,
                    live_record,
                    Path(),
                    0,
                    None,
                    f"unsupported_extension_{extension or 'unknown'}",
                )
            )
            continue

        product_stub = safe_slug(
            audit_record["references"][0]["product_handle"] if audit_record["references"] else media_id,
            media_id.replace("/", "-"),
        )
        base_name = safe_slug(f"{product_stub}-{media_id.split('/')[-1]}", media_id.split("/")[-1])
        original_path = originals_dir / f"{base_name}{extension}"
        prepared_path = prepared_dir / f"{base_name}{extension}"

        try:
            _, original_size, downloaded_content_type = download_media(live_record["original"]["url"], original_path)
        except Exception as exc:  # pragma: no cover - operator failure path
            entries.append(
                manifest_entry_from_record(
                    audit_record,
                    live_record,
                    original_path,
                    0,
                    None,
                    f"download_failed:{exc}",
                )
            )
            continue

        live_record["original"]["mime_type"] = downloaded_content_type or live_record["original"]["mime_type"]

        try:
            replacement = compress_image(
                original_path,
                prepared_path,
                extension=extension,
                config=preset,
            )
        except Exception as exc:
            entries.append(
                manifest_entry_from_record(
                    audit_record,
                    live_record,
                    original_path,
                    original_size,
                    None,
                    f"compress_failed:{exc}",
                )
            )
            continue

        saved_bytes = original_size - int(replacement["bytes"])
        saved_percent = percent_saved(original_size, int(replacement["bytes"]))
        if saved_bytes <= 0:
            prepared_path.unlink(missing_ok=True)
            entries.append(
                manifest_entry_from_record(
                    audit_record,
                    live_record,
                    original_path,
                    original_size,
                    None,
                    "no_savings",
                )
            )
            continue

        if saved_bytes < int(preset["min_savings_bytes"]) or saved_percent < float(preset["min_savings_percent"]) * 100.0:
            prepared_path.unlink(missing_ok=True)
            entries.append(
                manifest_entry_from_record(
                    audit_record,
                    live_record,
                    original_path,
                    original_size,
                    None,
                    "below_minimum_savings_threshold",
                )
            )
            continue

        prepared_count += 1
        total_before += original_size
        total_after += int(replacement["bytes"])
        entries.append(
            manifest_entry_from_record(
                audit_record,
                live_record,
                original_path,
                original_size,
                replacement,
                "",
            )
        )

    summary = {
        "selected_records": len(selected_records),
        "prepared_records": prepared_count,
        "skipped_records": len(entries) - prepared_count,
        "total_original_bytes": total_before,
        "total_original_mb": round(bytes_to_mb(total_before), 2),
        "total_replacement_bytes": total_after,
        "total_replacement_mb": round(bytes_to_mb(total_after), 2),
        "total_saved_bytes": total_before - total_after,
        "total_saved_mb": round(bytes_to_mb(total_before - total_after), 2),
        "total_saved_percent": round(percent_saved(total_before, total_after), 2) if total_before else 0.0,
    }
    manifest = {
        "generated_at": utc_now(),
        "store_domain": normalize_store_domain(args.store_domain),
        "api_version": args.api_version,
        "audit_json": str(args.audit_json),
        "preset": args.preset,
        "preset_config": preset,
        "summary": summary,
        "entries": entries,
    }
    write_json(args.manifest, manifest)

    print(f"Prepared records: {summary['prepared_records']} / {summary['selected_records']}")
    print(f"Total original MB: {summary['total_original_mb']:.2f}")
    print(f"Total replacement MB: {summary['total_replacement_mb']:.2f}")
    print(f"Total saved MB: {summary['total_saved_mb']:.2f}")
    print(f"Total saved %: {summary['total_saved_percent']:.2f}")
    print(f"Manifest: {args.manifest}")
    return 0


def replace_candidates(manifest: Dict[str, Any], limit: int) -> List[Dict[str, Any]]:
    entries = [item for item in (manifest.get("entries") or []) if item.get("ready_for_upload")]
    if limit > 0:
        entries = entries[:limit]
    return entries


def run_replace(args: argparse.Namespace) -> int:
    if not args.manifest.exists():
        raise FileNotFoundError(f"Manifest not found: {args.manifest}")

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    candidates = replace_candidates(manifest, args.limit)
    if not candidates:
        print("No prepared manifest entries are ready for replacement.")
        return 0

    client = ShopifyClient(
        store_domain=args.store_domain,
        access_token=resolve_access_token(args.access_token),
        api_version=args.api_version,
    )
    media_ids = [item["media_id"] for item in candidates]
    live_map = {
        media_id: fresh_media_snapshot(node)
        for media_id, node in client.media_by_ids(media_ids).items()
    }

    preflight: List[Dict[str, Any]] = []
    ready_entries: List[Dict[str, Any]] = []
    for entry in candidates:
        local_path = Path(entry["replacement"]["path"])
        if not local_path.exists():
            preflight.append({"media_id": entry["media_id"], "action": "skipped", "reason": "replacement_missing"})
            continue

        live_record = live_map.get(entry["media_id"])
        if not live_record:
            preflight.append({"media_id": entry["media_id"], "action": "skipped", "reason": "media_not_found"})
            continue

        source_snapshot = entry.get("source_snapshot", {})
        drifted = any(
            [
                int(source_snapshot.get("bytes") or 0) != int(live_record["original"]["bytes"] or 0),
                int(source_snapshot.get("width") or 0) != int(live_record["image"]["width"] or 0),
                int(source_snapshot.get("height") or 0) != int(live_record["image"]["height"] or 0),
            ]
        )
        if drifted and not args.force:
            preflight.append({"media_id": entry["media_id"], "action": "skipped", "reason": "source_drifted"})
            continue

        preflight.append({"media_id": entry["media_id"], "action": "ready", "reason": "ready"})
        ready_entries.append(entry)

    if not args.execute:
        summary = {
            "generated_at": utc_now(),
            "store_domain": normalize_store_domain(args.store_domain),
            "mode": "dry_run",
            "ready_count": len(ready_entries),
            "skipped_count": len([item for item in preflight if item["action"] == "skipped"]),
            "results": preflight,
        }
        write_json(args.results_json, summary)
        print(f"Dry run ready count: {summary['ready_count']}")
        print(f"Dry run skipped count: {summary['skipped_count']}")
        print(f"Dry run results: {args.results_json}")
        return 0

    results: List[Dict[str, Any]] = []
    for batch in chunked(ready_entries, max(1, args.batch_size)):
        staged_inputs = []
        for entry in batch:
            local_path = Path(entry["replacement"]["path"])
            mime_type = clean(entry["replacement"]["mime_type"]) or guess_mime_type(local_path.name, local_path.suffix.lower())
            staged_inputs.append(
                {
                    "resource": "IMAGE",
                    "filename": local_path.name,
                    "mimeType": mime_type,
                    "httpMethod": "POST",
                    "fileSize": str(local_path.stat().st_size),
                }
            )

        staged_targets = client.staged_uploads_create(staged_inputs)
        if len(staged_targets) != len(batch):
            raise RuntimeError("stagedUploadsCreate returned an unexpected target count.")

        update_inputs: List[Dict[str, Any]] = []
        staged_index_to_entry: Dict[int, Dict[str, Any]] = {}
        for index, entry in enumerate(batch):
            local_path = Path(entry["replacement"]["path"])
            mime_type = clean(entry["replacement"]["mime_type"]) or guess_mime_type(local_path.name, local_path.suffix.lower())
            stage_upload_file(staged_targets[index], local_path, mime_type)
            update_inputs.append(
                {
                    "id": entry["media_id"],
                    "originalSource": staged_targets[index]["resourceUrl"],
                }
            )
            staged_index_to_entry[index] = entry

        payload = client.file_update(update_inputs)
        user_errors = payload.get("userErrors", [])
        error_indices = set()
        for error in user_errors:
            index = parse_error_index(error.get("field"))
            if index is None:
                results.append(
                    {
                        "media_id": "",
                        "action": "error",
                        "reason": clean(error.get("message")) or "file_update_error",
                    }
                )
                continue
            error_indices.add(index)
            entry = staged_index_to_entry.get(index)
            results.append(
                {
                    "media_id": entry["media_id"] if entry else "",
                    "action": "error",
                    "reason": clean(error.get("message")) or "file_update_error",
                }
            )

        polled = wait_for_file_statuses(
            client,
            [entry["media_id"] for entry in batch],
            timeout_seconds=args.poll_timeout_seconds,
            poll_interval_seconds=args.poll_interval_seconds,
        )

        for index, entry in enumerate(batch):
            if index in error_indices:
                continue
            snapshot = polled.get(entry["media_id"], {})
            status = clean(snapshot.get("file_status"))
            file_errors = snapshot.get("file_errors", [])
            if status in READY_FILE_STATUSES:
                results.append(
                    {
                        "media_id": entry["media_id"],
                        "action": "updated",
                        "reason": "updated",
                        "file_status": status,
                        "width": snapshot.get("image", {}).get("width", 0),
                        "height": snapshot.get("image", {}).get("height", 0),
                    }
                )
            elif status in FAILURE_FILE_STATUSES:
                details = "; ".join(
                    clean(error.get("details")) or clean(error.get("message"))
                    for error in file_errors
                )
                results.append(
                    {
                        "media_id": entry["media_id"],
                        "action": "error",
                        "reason": details or f"file_status_{status.lower()}",
                        "file_status": status,
                    }
                )
            else:
                results.append(
                    {
                        "media_id": entry["media_id"],
                        "action": "pending",
                        "reason": f"file_status_{status.lower() or 'unknown'}",
                        "file_status": status,
                    }
                )

    counts: Dict[str, int] = {}
    for item in results:
        counts[item["action"]] = counts.get(item["action"], 0) + 1
    output = {
        "generated_at": utc_now(),
        "store_domain": normalize_store_domain(args.store_domain),
        "mode": "execute",
        "summary": counts,
        "results": results,
    }
    write_json(args.results_json, output)
    print("Execution summary:")
    for action, count in sorted(counts.items()):
        print(f"  {action}: {count}")
    print(f"Results: {args.results_json}")
    return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    try:
        if args.command == "audit":
            return run_audit(args)
        if args.command == "prepare":
            return run_prepare(args)
        if args.command == "replace":
            return run_replace(args)
    except requests.HTTPError as exc:
        body = exc.response.text if exc.response is not None else ""
        print(f"HTTP error: {exc} {body}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1
    raise RuntimeError(f"Unknown command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
