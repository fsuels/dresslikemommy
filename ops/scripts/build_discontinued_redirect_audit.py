#!/usr/bin/env python3
"""Build redirect and gone-candidate CSVs for discontinued products.

This script compares historical product handles from a Shopify product export
against the live storefront and classifies dead product URLs into:

- import-ready Shopify URL redirects,
- gone candidates that should stay removed,
- manual-review items that need operator judgment,
- already live or already redirected URLs.

It is intentionally conservative. When a dead URL does not match a strong rule,
it is sent to manual review instead of forcing a weak redirect.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import ssl
import time
import urllib.error
import urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path


DEFAULT_EXPORT = Path("GPT/products_export_1_backfill.csv")
DEFAULT_OUTPUT_DIR = Path("ops/redirect_audit")
DEFAULT_CACHE = DEFAULT_OUTPUT_DIR / "status_cache.json"
DEFAULT_BASE_URL = "https://www.dresslikemommy.com"

REDIRECT_TARGETS = {
    "swimsuits": "/collections/swimsuits",
    "tops": "/collections/family-tops",
    "daddy_tees": "/collections/daddy-me-t-shirts",
    "daddy_general": "/collections/daddy-and-me",
    "trunks": "/collections/trunks",
    "sweaters": "/collections/sweaters",
    "pajamas": "/collections/family-pajamas",
}

FESTIVE_TOKENS = {
    "christmas",
    "xmas",
    "reindeer",
    "santa",
    "grinch",
    "elf",
    "fair isle",
    "snowflake",
}
DRAGON_TOKENS = {"dragon"}
DADDY_TOKENS = {
    "daddy and me",
    "daddy-me",
    "dad and",
    "father and",
    "father-son",
    "father son",
    "dad and son",
    "dads and",
}
SWIM_TOKENS = {
    "swim",
    "swimsuit",
    "swimwear",
    "bikini",
    "one-piece",
    "one piece",
    "bathing",
    "beachwear",
}
TRUNK_TOKENS = {
    "trunk",
    "trunks",
    "swim short",
    "swim shorts",
    "board short",
    "board shorts",
}
TEE_TOKENS = {
    "t-shirt",
    "t shirt",
    "t-shirts",
    "t shirts",
    "tee",
    "tees",
    "graphic tee",
}
SHIRT_TOKENS = {
    "shirt",
    "shirts",
    "button-down",
    "button down",
    "button-up",
    "button up",
}
SWEATER_TOKENS = {
    "sweater",
    "sweaters",
    "jacket",
    "jackets",
    "coat",
    "coats",
    "hoodie",
    "hoodies",
    "cardigan",
    "cardigans",
    "pullover",
    "pullovers",
    "fleece",
}
PAJAMA_TOKENS = {
    "pajama",
    "pajamas",
    "sleepwear",
    "sleep set",
    "loungewear",
}
TOP_TOKENS = TEE_TOKENS | SHIRT_TOKENS | {"top", "tops"}


@dataclass
class ProductRecord:
    handle: str
    title: str
    published: str
    status: str
    category1: str
    subcategory: str
    subcategory2: str
    product_type: str
    style: str
    pattern: str
    tags: str

    @property
    def path(self) -> str:
        return f"/products/{self.handle}"

    @property
    def text_blob(self) -> str:
        parts = [
            self.handle,
            self.title,
            self.category1,
            self.subcategory,
            self.subcategory2,
            self.product_type,
            self.style,
            self.pattern,
            self.tags,
        ]
        return " | ".join(part.strip().lower() for part in parts if part and part.strip())


@dataclass
class StatusResult:
    status: str
    location: str
    checked_at: int


@dataclass
class Decision:
    bucket: str
    reason: str
    confidence: str
    target: str = ""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--export", type=Path, default=DEFAULT_EXPORT, help="Historical Shopify export CSV")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR, help="Directory for generated files")
    parser.add_argument("--cache", type=Path, default=DEFAULT_CACHE, help="JSON cache for live status checks")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help="Storefront origin")
    parser.add_argument("--timeout", type=int, default=12, help="Per-request timeout in seconds")
    parser.add_argument("--workers", type=int, default=6, help="Concurrent live status checks")
    parser.add_argument("--retries", type=int, default=3, help="Retries for rate-limited/network checks")
    parser.add_argument(
        "--include-regex",
        default="",
        help="Only audit products whose combined metadata matches this case-insensitive regex",
    )
    parser.add_argument(
        "--exclude-regex",
        default="",
        help="Skip products whose combined metadata matches this case-insensitive regex",
    )
    parser.add_argument(
        "--refresh-cache",
        action="store_true",
        help="Ignore the existing status cache and recheck all handles",
    )
    return parser.parse_args()


def load_products(export_path: Path) -> list[ProductRecord]:
    products: list[ProductRecord] = []
    seen_handles: set[str] = set()

    with export_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            product_handle = (row.get("Handle") or "").strip()
            if not product_handle or product_handle in seen_handles:
                continue
            seen_handles.add(product_handle)
            products.append(
                ProductRecord(
                    handle=product_handle,
                    title=(row.get("Title") or "").strip(),
                    published=(row.get("Published") or "").strip().lower(),
                    status=(row.get("Status") or "").strip().lower(),
                    category1=(row.get("Category1 (product.metafields.custom.category1)") or "").strip(),
                    subcategory=(row.get("SubCategory (product.metafields.custom.subcategory)") or "").strip(),
                    subcategory2=(row.get("SubCategory2 (product.metafields.custom.subcategory2)") or "").strip(),
                    product_type=(row.get("Type (product.metafields.custom.type)") or row.get("Type") or "").strip(),
                    style=(row.get("Style (product.metafields.custom.style)") or "").strip(),
                    pattern=(row.get("Pattern (product.metafields.custom.pattern)") or "").strip(),
                    tags=(row.get("Tags") or "").strip(),
                )
            )

    return products


def load_cache(cache_path: Path) -> dict[str, StatusResult]:
    if not cache_path.exists():
        return {}

    raw = json.loads(cache_path.read_text(encoding="utf-8"))
    cache: dict[str, StatusResult] = {}
    for path, payload in raw.items():
        cache[path] = StatusResult(
            status=str(payload.get("status", "")),
            location=str(payload.get("location", "")),
            checked_at=int(payload.get("checked_at", 0)),
        )
    return cache


def save_cache(cache_path: Path, cache: dict[str, StatusResult]) -> None:
    serializable = {
        path: {
            "status": value.status,
            "location": value.location,
            "checked_at": value.checked_at,
        }
        for path, value in sorted(cache.items())
    }
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(json.dumps(serializable, indent=2, sort_keys=True), encoding="utf-8")


def build_opener() -> urllib.request.OpenerDirector:
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None

    context = ssl.create_default_context()
    return urllib.request.build_opener(urllib.request.HTTPSHandler(context=context), NoRedirect)


def fetch_status(base_url: str, path: str, timeout: int, retries: int) -> StatusResult:
    last_result: StatusResult | None = None

    for attempt in range(retries):
        opener = build_opener()
        request = urllib.request.Request(
            f"{base_url}{path}",
            method="HEAD",
            headers={"User-Agent": "Mozilla/5.0"},
        )

        try:
            with opener.open(request, timeout=timeout) as response:
                result = StatusResult(
                    status=str(response.status),
                    location=response.headers.get("Location", ""),
                    checked_at=int(time.time()),
                )
        except urllib.error.HTTPError as error:
            result = StatusResult(
                status=str(error.code),
                location=error.headers.get("Location", ""),
                checked_at=int(time.time()),
            )
        except Exception as error:  # pragma: no cover - network-dependent
            result = StatusResult(
                status=f"ERR:{type(error).__name__}",
                location=str(error),
                checked_at=int(time.time()),
            )

        last_result = result

        if result.status not in {"429", "ERR:TimeoutError", "ERR:URLError"}:
            return result

        if attempt < retries - 1:
            time.sleep(1.5 * (attempt + 1))

    assert last_result is not None
    return last_result


def has_any_token(text: str, tokens: set[str]) -> bool:
    return any(token in text for token in tokens)


def classify_dead_product(record: ProductRecord) -> Decision:
    text = record.text_blob
    is_daddy = has_any_token(text, DADDY_TOKENS) or "daddy and me" in record.category1.lower()
    is_festive = has_any_token(text, FESTIVE_TOKENS)
    is_dragon = has_any_token(text, DRAGON_TOKENS)
    is_trunks = has_any_token(text, TRUNK_TOKENS)
    is_swim = has_any_token(text, SWIM_TOKENS)
    has_tee_terms = has_any_token(text, TEE_TOKENS)
    has_shirt_terms = has_any_token(text, SHIRT_TOKENS)
    is_sweater = has_any_token(text, SWEATER_TOKENS)
    is_pajama = has_any_token(text, PAJAMA_TOKENS)
    is_top = has_any_token(text, TOP_TOKENS)

    if is_festive:
        return Decision(bucket="gone", reason="seasonal_festive_product", confidence="high")

    if is_dragon:
        return Decision(bucket="gone", reason="dragon_novelty_product", confidence="high")

    if is_daddy and is_trunks:
        return Decision(
            bucket="redirect",
            reason="daddy_and_me_swim_trunks",
            confidence="high",
            target=REDIRECT_TARGETS["trunks"],
        )

    if is_swim:
        return Decision(
            bucket="redirect",
            reason="swimwear_category_match",
            confidence="high",
            target=REDIRECT_TARGETS["swimsuits"],
        )

    if is_daddy and has_tee_terms:
        return Decision(
            bucket="redirect",
            reason="daddy_and_me_tshirt_match",
            confidence="high",
            target=REDIRECT_TARGETS["daddy_tees"],
        )

    if is_daddy and has_shirt_terms and not has_tee_terms:
        return Decision(
            bucket="redirect",
            reason="daddy_and_me_general_match",
            confidence="medium",
            target=REDIRECT_TARGETS["daddy_general"],
        )

    if is_sweater:
        return Decision(
            bucket="redirect",
            reason="sweater_or_outerwear_match",
            confidence="high",
            target=REDIRECT_TARGETS["sweaters"],
        )

    if is_pajama:
        return Decision(
            bucket="redirect",
            reason="pajama_category_match",
            confidence="medium",
            target=REDIRECT_TARGETS["pajamas"],
        )

    if is_top:
        return Decision(
            bucket="redirect",
            reason="tops_category_match",
            confidence="medium",
            target=REDIRECT_TARGETS["tops"],
        )

    return Decision(bucket="review", reason="no_safe_rule_match", confidence="low")


def classify_record(record: ProductRecord, status_result: StatusResult) -> Decision:
    if status_result.status == "200":
        return Decision(bucket="live", reason="still_live", confidence="high")

    if status_result.status in {"301", "302", "307", "308"}:
        return Decision(
            bucket="already_redirected",
            reason="storefront_redirect_exists",
            confidence="high",
            target=status_result.location,
        )

    if status_result.status == "404":
        return classify_dead_product(record)

    return Decision(bucket="review", reason=f"unexpected_status_{status_result.status}", confidence="low")


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_summary(
    path: Path,
    products: list[ProductRecord],
    decisions: dict[str, Decision],
    statuses: dict[str, StatusResult],
) -> None:
    status_counts = Counter(status.status for status in statuses.values())
    bucket_counts = Counter(decision.bucket for decision in decisions.values())
    redirect_target_counts = Counter(
        decision.target for decision in decisions.values() if decision.bucket == "redirect"
    )

    lines = [
        "# Discontinued Redirect Audit",
        "",
        f"- Generated at: {time.strftime('%Y-%m-%d %H:%M:%S %Z')}",
        f"- Source export: `{DEFAULT_EXPORT}`",
        f"- Unique product handles audited: `{len(products)}`",
        "",
        "## Live Status Counts",
        "",
    ]

    for status, count in sorted(status_counts.items()):
        lines.append(f"- `{status}`: `{count}`")

    lines.extend(["", "## Decision Buckets", ""])
    for bucket, count in sorted(bucket_counts.items()):
        lines.append(f"- `{bucket}`: `{count}`")

    if redirect_target_counts:
        lines.extend(["", "## Redirect Targets", ""])
        for target, count in sorted(redirect_target_counts.items()):
            lines.append(f"- `{target}`: `{count}`")

    lines.extend(
        [
            "",
            "## Generated Files",
            "",
            "- `shopify_url_redirects.csv`: import-ready redirect rows for Shopify admin.",
            "- `redirect_candidates_detailed.csv`: redirect rows with reasons and product metadata.",
            "- `gone_candidates.csv`: dead URLs that should stay removed rather than be redirected.",
            "- `manual_review.csv`: dead URLs without a safe automatic rule.",
            "- `already_resolved.csv`: live or already redirected URLs.",
            "",
            "## Notes",
            "",
            "- Holiday and dragon-pattern products are conservatively treated as `gone` candidates.",
            "- Only high- or medium-confidence matches become automatic redirect rows.",
            "- Anything ambiguous is routed to manual review rather than forcing a weak redirect.",
        ]
    )

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    products = load_products(args.export)
    include_pattern = re.compile(args.include_regex, re.IGNORECASE) if args.include_regex else None
    exclude_pattern = re.compile(args.exclude_regex, re.IGNORECASE) if args.exclude_regex else None
    if include_pattern or exclude_pattern:
        filtered_products: list[ProductRecord] = []
        for product in products:
            text = product.text_blob
            if include_pattern and not include_pattern.search(text):
                continue
            if exclude_pattern and exclude_pattern.search(text):
                continue
            filtered_products.append(product)
        products = filtered_products

    output_dir: Path = args.output_dir
    cache_path: Path = args.cache
    output_dir.mkdir(parents=True, exist_ok=True)

    cache = {} if args.refresh_cache else load_cache(cache_path)

    uncached = [
        product
        for product in products
        if product.path not in cache
        or cache[product.path].status == "429"
        or cache[product.path].status.startswith("ERR:")
    ]
    if uncached:
        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            future_map = {
                executor.submit(
                    fetch_status,
                    args.base_url,
                    product.path,
                    args.timeout,
                    args.retries,
                ): product.path
                for product in uncached
            }
            for future in as_completed(future_map):
                path = future_map[future]
                cache[path] = future.result()

        save_cache(cache_path, cache)

    decisions: dict[str, Decision] = {}
    redirect_rows: list[dict[str, str]] = []
    redirect_details: list[dict[str, str]] = []
    gone_rows: list[dict[str, str]] = []
    review_rows: list[dict[str, str]] = []
    resolved_rows: list[dict[str, str]] = []

    for product in products:
        status_result = cache[product.path]
        decision = classify_record(product, status_result)
        decisions[product.path] = decision

        common = {
            "Path": product.path,
            "Handle": product.handle,
            "Title": product.title,
            "Published": product.published,
            "Status": product.status,
            "Category1": product.category1,
            "SubCategory": product.subcategory,
            "SubCategory2": product.subcategory2,
            "Type": product.product_type,
            "Style": product.style,
            "Pattern": product.pattern,
            "Tags": product.tags,
            "Live status": status_result.status,
            "Live location": status_result.location,
            "Decision": decision.bucket,
            "Reason": decision.reason,
            "Confidence": decision.confidence,
            "Target": decision.target,
        }

        if decision.bucket == "redirect":
            redirect_rows.append(
                {
                    "Redirect from": product.path,
                    "Redirect to": decision.target,
                }
            )
            redirect_details.append(common)
        elif decision.bucket == "gone":
            gone_rows.append(common)
        elif decision.bucket == "review":
            review_rows.append(common)
        else:
            resolved_rows.append(common)

    write_csv(
        output_dir / "shopify_url_redirects.csv",
        redirect_rows,
        ["Redirect from", "Redirect to"],
    )
    detailed_fields = [
        "Path",
        "Handle",
        "Title",
        "Published",
        "Status",
        "Category1",
        "SubCategory",
        "SubCategory2",
        "Type",
        "Style",
        "Pattern",
        "Tags",
        "Live status",
        "Live location",
        "Decision",
        "Reason",
        "Confidence",
        "Target",
    ]
    write_csv(output_dir / "redirect_candidates_detailed.csv", redirect_details, detailed_fields)
    write_csv(output_dir / "gone_candidates.csv", gone_rows, detailed_fields)
    write_csv(output_dir / "manual_review.csv", review_rows, detailed_fields)
    write_csv(output_dir / "already_resolved.csv", resolved_rows, detailed_fields)
    write_summary(output_dir / "summary.md", products, decisions, cache)

    print(f"Audited {len(products)} unique product handles")
    print(f"Generated {len(redirect_rows)} redirect rows")
    print(f"Generated {len(gone_rows)} gone candidates")
    print(f"Generated {len(review_rows)} manual review rows")
    print(f"Recorded {len(resolved_rows)} live/already-resolved rows")
    print(f"Output directory: {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
