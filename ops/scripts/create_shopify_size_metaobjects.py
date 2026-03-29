#!/usr/bin/env python3
"""Create a narrow batch of Shopify size metaobjects for deterministic size fills."""

from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops.scripts.fill_shopify_apparel_attributes import (  # noqa: E402
    ShopifyClient,
    build_metaobject_index,
    clean,
    normalize_text,
    split_csv,
)
from ops.scripts.shopify_admin_config import load_access_token, resolve_store_domain  # noqa: E402


DEFAULT_OUTPUT_DIR = Path("ops/feed-engineering/2026-03-29-phase-3i-size-metaobject-batch-1")

SAFE_BATCH = {
    "6-7 years": {
        "handle": "6-7-years",
        "taxonomy_reference": "gid://shopify/TaxonomyValue/227",
        "taxonomy_name": "6-7 years",
    },
    "7-8 years": {
        "handle": "7-8-years",
        "taxonomy_reference": "gid://shopify/TaxonomyValue/228",
        "taxonomy_name": "7-8 years",
    },
    "8-9 years": {
        "handle": "8-9-years",
        "taxonomy_reference": "gid://shopify/TaxonomyValue/229",
        "taxonomy_name": "8-9 years",
    },
    "3XL": {
        "handle": "3xl",
        "taxonomy_reference": "gid://shopify/TaxonomyValue/2918",
        "taxonomy_name": "Triple extra large (XXXL)",
    },
    "4XL": {
        "handle": "4xl",
        "taxonomy_reference": "gid://shopify/TaxonomyValue/2919",
        "taxonomy_name": "Four extra large (4XL)",
    },
}

METAOBJECT_CREATE_MUTATION = """
mutation CreateMetaobject($metaobject: MetaobjectCreateInput!) {
  metaobjectCreate(metaobject: $metaobject) {
    metaobject {
      id
      handle
      displayName
      fields {
        key
        value
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


@dataclass
class PlannedMetaobject:
    label: str
    handle: str
    taxonomy_reference: str
    taxonomy_name: str
    status: str
    reason: str
    existing_id: str = ""
    existing_handle: str = ""
    existing_display_name: str = ""
    created_id: str = ""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--store-domain", default="", help="Shopify store domain.")
    parser.add_argument("--access-token", default="", help="Shopify Admin API access token.")
    parser.add_argument(
        "--labels",
        default=",".join(SAFE_BATCH.keys()),
        help="Comma-separated subset of supported batch-1 labels to plan/create.",
    )
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="Directory for dry-run and execution artifacts.")
    parser.add_argument("--execute", action="store_true", help="Create planned size metaobjects live.")
    parser.add_argument("--pause-ms", type=int, default=250, help="Pause between live creates.")
    return parser.parse_args()


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def create_metaobject(client: ShopifyClient, *, label: str, handle: str, taxonomy_reference: str) -> tuple[str, str]:
    payload = {
        "type": "shopify--size",
        "handle": handle,
        "fields": [
            {"key": "label", "value": label},
            {"key": "taxonomy_reference", "value": taxonomy_reference},
        ],
    }
    data = client.graphql(METAOBJECT_CREATE_MUTATION, {"metaobject": payload})["metaobjectCreate"]
    errors = []
    for item in data.get("userErrors") or []:
        field = " / ".join(item.get("field") or [])
        message = clean(item.get("message"))
        errors.append(f"{field}: {message}" if field else message)
    if errors:
        return "", " | ".join(errors)
    metaobject = data.get("metaobject") or {}
    return clean(metaobject.get("id")), ""


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    requested_labels = split_csv(args.labels)
    unsupported = [label for label in requested_labels if label not in SAFE_BATCH]
    if unsupported:
        raise RuntimeError(f"Unsupported size labels requested: {', '.join(unsupported)}")
    if not requested_labels:
        raise RuntimeError("At least one supported size label is required.")

    client = ShopifyClient(
        resolve_store_domain(args.store_domain, fallback_domain="dresslikemommy-com.myshopify.com"),
        load_access_token(args.access_token),
    )
    existing_refs = client.fetch_metaobjects("shopify--size")
    existing_index = build_metaobject_index(existing_refs)
    planned: list[PlannedMetaobject] = []

    for label in requested_labels:
        target = SAFE_BATCH[label]
        existing = existing_index.get(normalize_text(label)) or existing_index.get(target["handle"])
        if existing:
            planned.append(
                PlannedMetaobject(
                    label=label,
                    handle=target["handle"],
                    taxonomy_reference=target["taxonomy_reference"],
                    taxonomy_name=target["taxonomy_name"],
                    status="skip",
                    reason="already_exists",
                    existing_id=clean(existing.id),
                    existing_handle=clean(existing.handle),
                    existing_display_name=clean(existing.display_name),
                )
            )
            continue
        planned.append(
            PlannedMetaobject(
                label=label,
                handle=target["handle"],
                taxonomy_reference=target["taxonomy_reference"],
                taxonomy_name=target["taxonomy_name"],
                status="plan",
                reason="ready",
            )
        )

    execution = {
        "execute": bool(args.execute),
        "planned_metaobject_creates": sum(1 for item in planned if item.status == "plan"),
        "created_metaobjects": 0,
        "errors": [],
    }

    if args.execute:
        for item in planned:
            if item.status != "plan":
                continue
            created_id, error_message = create_metaobject(
                client,
                label=item.label,
                handle=item.handle,
                taxonomy_reference=item.taxonomy_reference,
            )
            if error_message:
                execution["errors"].append({"label": item.label, "handle": item.handle, "error": error_message})
                continue
            item.created_id = created_id
            execution["created_metaobjects"] += 1
            if args.pause_ms > 0:
                time.sleep(args.pause_ms / 1000.0)

    fieldnames = [
        "label",
        "handle",
        "taxonomy_reference",
        "taxonomy_name",
        "status",
        "reason",
        "existing_id",
        "existing_handle",
        "existing_display_name",
        "created_id",
    ]
    write_csv(
        output_dir / "planned_size_metaobjects.csv",
        [
            {
                "label": item.label,
                "handle": item.handle,
                "taxonomy_reference": item.taxonomy_reference,
                "taxonomy_name": item.taxonomy_name,
                "status": item.status,
                "reason": item.reason,
                "existing_id": item.existing_id,
                "existing_handle": item.existing_handle,
                "existing_display_name": item.existing_display_name,
                "created_id": item.created_id,
            }
            for item in planned
        ],
        fieldnames,
    )

    summary = {
        "output_dir": str(output_dir),
        "requested_labels": requested_labels,
        "planned_metaobject_creates": execution["planned_metaobject_creates"],
        "skipped_existing": sum(1 for item in planned if item.status != "plan"),
        "execution": execution,
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
