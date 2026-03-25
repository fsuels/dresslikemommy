#!/usr/bin/env python3
"""Build a Shopify redirect import CSV from a GSC coverage export."""

from __future__ import annotations

import argparse
import csv
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlsplit


DEFAULT_INPUT = Path(
    "/Users/fsuels/Downloads/https___www.dresslikemommy.com_-Coverage-Drilldown-2026-03-24/Table.csv"
)
DEFAULT_OUTPUT_DIR = Path("ops/redirect_audit")

LOCALE_RE = re.compile(r"^/([a-z]{2}(?:-[a-z]{2})?)(?=/|$)")

SAFE_COLLECTIONS = {
    "accessories",
    "all",
    "bottoms",
    "daddy-and-me",
    "daddy-me-t-shirts",
    "dresses",
    "family-matching",
    "family-pajamas",
    "family-tops",
    "matching-outfits",
    "maternity",
    "popular-mommy-me-1",
    "sweaters",
    "swimsuits",
    "trunks",
}

COLLECTION_ALIASES = {
    "best-sellers": "/collections/all",
    "casual-dresses": "/collections/dresses",
    "christmas-matching-outfits": "/collections/family-matching",
    "daddy-me": "/collections/daddy-and-me",
    "daddy-me-shorts": "/collections/trunks",
    "daddy-me-t-shirts": "/collections/daddy-me-t-shirts",
    "family-matching-pajamas": "/collections/family-pajamas",
    "family-matching-sets": "/collections/family-matching",
    "family-matching-sweaters-jackets": "/collections/sweaters",
    "family-matching-swimsuits": "/collections/swimsuits",
    "family-matching-t-shirts": "/collections/family-tops",
    "formal-dresses": "/collections/dresses",
    "halloween-matching": "/collections/matching-outfits",
    "holiday-matching-outfits": "/collections/family-matching",
    "jumpers": "/collections/sweaters",
    "leggings": "/collections/bottoms",
    "matching-couples-t-shirts": "/collections/family-tops",
    "matching-dresses": "/collections/dresses",
    "matching-family-outfits": "/collections/family-matching",
    "matching-swimwear": "/collections/swimsuits",
    "maternity-dresses": "/collections/maternity",
    "maxi-dresses": "/collections/dresses",
    "midi-dresses": "/collections/dresses",
    "mini-dresses": "/collections/dresses",
    "mommy-and-me-dresses": "/collections/matching-outfits",
    "mommy-me": "/collections/matching-outfits",
    "mother-daughter-dresses": "/collections/matching-outfits",
    "mother-daughter-swimsuits": "/collections/swimsuits",
    "new-arrivals": "/collections/all",
    "new-matching-outfits": "/collections/matching-outfits",
    "new-women-outfits": "/collections/matching-outfits",
    "pants": "/collections/bottoms",
    "popular-family-matching": "/collections/family-matching",
    "popular-mommy-me": "/collections/popular-mommy-me-1",
    "popular-mommy-me-1": "/collections/popular-mommy-me-1",
    "rompers": "/collections/matching-outfits",
    "skirts": "/collections/bottoms",
    "sundresses": "/collections/dresses",
    "swimwear": "/collections/swimsuits",
    "tops": "/collections/family-tops",
}

SAFE_PAGES = {
    "/pages/about-us",
    "/pages/company-information",
    "/pages/faqs",
    "/pages/return-policy",
    "/pages/secure-payments",
    "/pages/shipping-and-delivery",
    "/pages/terms-and-conditions",
    "/pages/wholesale-drop-shipping",
}

HOLIDAY_TOKENS = {
    "christmas",
    "xmas",
    "holiday",
    "reindeer",
    "grinch",
    "santa",
    "snowflake",
    "snowman",
    "fair isle",
    "festive",
}
PAJAMA_TOKENS = {"pajama", "pajamas", "sleepwear", "loungewear", "onesie", "onesies", "pjs"}
SWIM_TOKENS = {
    "bathing",
    "beachwear",
    "bikini",
    "monokini",
    "one-piece",
    "one piece",
    "swim",
    "swimsuit",
    "swimwear",
    "tankini",
}
TRUNK_TOKENS = {"board short", "board shorts", "swim short", "swim shorts", "trunk", "trunks"}
SWEATER_TOKENS = {
    "cardigan",
    "coat",
    "coats",
    "fleece",
    "hoodie",
    "hoodies",
    "jacket",
    "jackets",
    "pullover",
    "pullovers",
    "sweater",
    "sweaters",
    "sweatshirt",
    "sweatshirts",
    "vest",
}
TOP_TOKENS = {
    "button-down",
    "button down",
    "button-up",
    "button up",
    "shirt",
    "shirts",
    "t-shirt",
    "t shirt",
    "t-shirts",
    "t shirts",
    "tee",
    "tees",
    "top",
    "tops",
}
DRESS_TOKENS = {
    "dress",
    "dresses",
    "gown",
    "gowns",
    "jumpsuit",
    "jumpsuits",
    "maxi",
    "midi",
    "mini",
    "romper",
    "rompers",
    "skirt",
    "skirts",
}
ACCESSORY_TOKENS = {"beanie", "bow", "hairband", "hat", "headband", "headbands", "scarf", "turban"}
MATERNITY_TOKENS = {"baby shower", "maternity", "pregnancy", "pregnant", "photoshoot"}
DADDY_TOKENS = {"dad", "daddy", "father", "son", "pilot", "monster", "big man", "little man"}
FAMILY_TOKENS = {"family", "matching", "mother", "daughter", "mommy", "mom", "child", "children"}


@dataclass
class Decision:
    source: str
    target: str
    reason: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT, help="GSC CSV export path")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR, help="Output directory")
    parser.add_argument(
        "--basename",
        default="gsc_coverage_2026_03_24",
        help="Output file prefix inside the output directory",
    )
    return parser.parse_args()


def normalize_source(url_or_path: str) -> str:
    path = urlsplit(url_or_path).path or "/"
    if path != "/":
        path = path.rstrip("/")
    return path or "/"


def strip_locale(path: str) -> tuple[str, str]:
    match = LOCALE_RE.match(path)
    if not match:
        return "", path
    locale = match.group(1)
    rest = path[match.end() :] or "/"
    return locale, rest


def unwrap_analysis_path(path: str) -> str:
    if path.startswith("/a/s/"):
        return path[4:]

    if path.startswith("/wpm@") and "/sandbox/" in path:
        return path.split("/sandbox", 1)[1] or "/"

    return path


def token_text(value: str) -> str:
    return value.replace("-", " ").replace("_", " ").lower()


def has_any(text: str, tokens: set[str]) -> bool:
    return any(token in text for token in tokens)


def product_target(handle: str) -> tuple[str, str]:
    text = token_text(handle)

    if has_any(text, HOLIDAY_TOKENS) and has_any(text, PAJAMA_TOKENS):
        return "/collections/christmas-pajamas", "holiday pajama product"
    if has_any(text, HOLIDAY_TOKENS) and has_any(text, SWEATER_TOKENS):
        return "/collections/christmas-sweaters", "holiday sweater product"
    if has_any(text, HOLIDAY_TOKENS) and has_any(text, TOP_TOKENS):
        return "/collections/family-tops", "holiday top product"
    if has_any(text, PAJAMA_TOKENS):
        return "/collections/family-pajamas", "pajama product"
    if has_any(text, TRUNK_TOKENS):
        return "/collections/trunks", "trunks product"
    if has_any(text, SWIM_TOKENS):
        return "/collections/swimsuits", "swim product"
    if has_any(text, MATERNITY_TOKENS):
        return "/collections/maternity", "maternity product"
    if has_any(text, ACCESSORY_TOKENS):
        return "/collections/accessories", "accessory product"
    if has_any(text, DADDY_TOKENS) and has_any(text, TOP_TOKENS):
        return "/collections/daddy-me-t-shirts", "daddy tee product"
    if has_any(text, DADDY_TOKENS):
        return "/collections/daddy-and-me", "daddy product"
    if has_any(text, SWEATER_TOKENS):
        return "/collections/sweaters", "sweater or outerwear product"
    if has_any(text, DRESS_TOKENS):
        return "/collections/dresses", "dress product"
    if has_any(text, TOP_TOKENS):
        return "/collections/family-tops", "top product"
    if "set" in text or "outfit" in text or has_any(text, FAMILY_TOKENS):
        return "/collections/family-matching", "family outfit product"
    return "", ""


def collection_target(handle: str) -> tuple[str, str]:
    if handle in COLLECTION_ALIASES:
        return COLLECTION_ALIASES[handle], f"collection alias {handle}"
    if handle in SAFE_COLLECTIONS:
        return f"/collections/{handle}", f"safe collection {handle}"

    text = token_text(handle)
    if has_any(text, HOLIDAY_TOKENS) and has_any(text, PAJAMA_TOKENS):
        return "/collections/christmas-pajamas", "holiday pajama collection"
    if has_any(text, HOLIDAY_TOKENS) and has_any(text, SWEATER_TOKENS):
        return "/collections/christmas-sweaters", "holiday sweater collection"
    if has_any(text, PAJAMA_TOKENS):
        return "/collections/family-pajamas", "pajama collection"
    if has_any(text, TRUNK_TOKENS):
        return "/collections/trunks", "trunks collection"
    if has_any(text, SWIM_TOKENS):
        return "/collections/swimsuits", "swim collection"
    if has_any(text, MATERNITY_TOKENS):
        return "/collections/maternity", "maternity collection"
    if has_any(text, ACCESSORY_TOKENS):
        return "/collections/accessories", "accessory collection"
    if has_any(text, DADDY_TOKENS) and has_any(text, TOP_TOKENS):
        return "/collections/daddy-me-t-shirts", "daddy tee collection"
    if has_any(text, DADDY_TOKENS):
        return "/collections/daddy-and-me", "daddy collection"
    if has_any(text, SWEATER_TOKENS):
        return "/collections/sweaters", "sweater collection"
    if has_any(text, DRESS_TOKENS):
        return "/collections/dresses", "dress collection"
    if has_any(text, TOP_TOKENS):
        return "/collections/family-tops", "top collection"
    if "outfit" in text or "matching" in text or "family" in text:
        return "/collections/family-matching", "family collection"
    return "", ""


def classify_path(source_path: str) -> tuple[str, str]:
    analysis_path = unwrap_analysis_path(source_path)
    locale, base_path = strip_locale(analysis_path)

    if locale and base_path == "/":
        return "/", f"locale root {locale}"

    if source_path in {"/${t}", "/b", "/comments", "/interfaces/interfaceStore.php", "/paginfo@dresslikemommy.com", "/s"}:
        return "/", "invalid utility path"
    if source_path == "/thank_you":
        return "/cart", "thank you path"
    if "*" in source_path and "cart" in source_path:
        return "/cart", "wildcard cart path"

    if base_path in {"/account", "/account/login", "/account/register", "/blogs/news", "/cart"}:
        return base_path, f"locale-stripped utility path {base_path}"

    if base_path.startswith("/pages/"):
        if base_path in SAFE_PAGES:
            return base_path, f"locale-stripped page {base_path}"
        return "/", f"unknown page {base_path}"

    if base_path.startswith("/collections/") and "/products/" in base_path:
        handle = base_path.split("/products/", 1)[1]
        target, reason = product_target(handle)
        if target:
            return target, reason
        return "", f"manual nested product {handle}"

    if base_path.startswith("/products/"):
        handle = base_path.split("/products/", 1)[1]
        if handle == "gift-card":
            return "/", "gift card path"
        target, reason = product_target(handle)
        if target:
            return target, reason
        return "", f"manual product {handle}"

    if base_path.startswith("/collections/"):
        handle = base_path.split("/collections/", 1)[1]
        target, reason = collection_target(handle)
        if target:
            return target, reason
        return "", f"manual collection {handle}"

    if base_path == "/":
        return "/", "root path"

    return "", f"manual path {base_path}"


def main() -> int:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    redirects: list[Decision] = []
    manual_rows: list[tuple[str, str]] = []
    seen_sources: set[str] = set()
    reasons = Counter()

    with args.input.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            source = normalize_source(row.get("URL") or "")
            if not source or source in seen_sources:
                continue
            seen_sources.add(source)

            target, reason = classify_path(source)
            if target and target != source:
                redirects.append(Decision(source=source, target=target, reason=reason))
                reasons[reason] += 1
            else:
                manual_rows.append((source, reason or "no rule"))

    redirect_csv = args.output_dir / f"{args.basename}_shopify_redirects.csv"
    detailed_csv = args.output_dir / f"{args.basename}_redirect_details.csv"
    manual_csv = args.output_dir / f"{args.basename}_manual_review.csv"
    summary_md = args.output_dir / f"{args.basename}_summary.md"

    with redirect_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["Redirect from", "Redirect to"])
        for row in redirects:
            writer.writerow([row.source, row.target])

    with detailed_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["Source path", "Redirect target", "Reason"])
        for row in redirects:
            writer.writerow([row.source, row.target, row.reason])

    with manual_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["Source path", "Reason"])
        for row in manual_rows:
            writer.writerow(row)

    lines = [
        f"# {args.basename}",
        "",
        f"- Input rows processed: {len(seen_sources)}",
        f"- Redirect rows generated: {len(redirects)}",
        f"- Manual review rows: {len(manual_rows)}",
        "",
        "## Top Reasons",
    ]
    for reason, count in reasons.most_common(20):
        lines.append(f"- {reason}: {count}")
    summary_md.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"redirect_csv={redirect_csv}")
    print(f"detailed_csv={detailed_csv}")
    print(f"manual_csv={manual_csv}")
    print(f"summary_md={summary_md}")
    print(f"redirect_rows={len(redirects)}")
    print(f"manual_rows={len(manual_rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
