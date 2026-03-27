#!/usr/bin/env python3

import argparse
import csv
import re
import subprocess
import sys
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


SITEMAP_URL = "https://www.dresslikemommy.com/sitemap_blogs_1.xml"
SITEMAP_NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}


@dataclass(frozen=True)
class Rule:
    canonical_slug: str
    canonical_title: str
    topic_cluster: str
    audience: str
    season: str
    patterns: tuple[str, ...]


MANUAL_RULES = (
    Rule(
        canonical_slug="mommy-and-me-valentines-day-outfits",
        canonical_title="Mommy and Me Valentine's Day Outfits",
        topic_cluster="Mommy & Me Valentine's Day",
        audience="Mommy & Me",
        season="Valentine's Day",
        patterns=(
            r"^mommy-and-me-valentines-day-outfits$",
            r"^valentines-day-mommy-and-me-outfits-for-\d{4}$",
            r"^mommy-and-me-valentines-day-dress-guide-\d{4}$",
        ),
    ),
    Rule(
        canonical_slug="adorable-matching-valentines-day-looks-for-the-whole-family",
        canonical_title="Adorable Matching Valentine's Day Looks for the Whole Family",
        topic_cluster="Family Valentine's Day",
        audience="Family",
        season="Valentine's Day",
        patterns=(
            r"^adorable-matching-valentines-day-looks-for-the-whole-family$",
            r"^red-and-pink-family-matching-outfits-for-valentines-day$",
            r"^heart-themed-matching-outfits-for-families-\d{4}$",
        ),
    ),
    Rule(
        canonical_slug="red-white-and-blue-patriotic-family-matching-looks",
        canonical_title="Red, White, and Blue Patriotic Family Matching Looks",
        topic_cluster="Patriotic Family Matching",
        audience="Family",
        season="4th of July",
        patterns=(
            r"^red-white-and-blue-patriotic-family-matching-looks$",
            r"^4th-of-july-family-matching-outfits-\d{4}$",
            r"^memorial-day-weekend-family-matching-looks-\d{4}$",
        ),
    ),
    Rule(
        canonical_slug="back-to-school-daddy-and-me-photo-outfits",
        canonical_title="Back-to-School Daddy and Me Photo Outfits",
        topic_cluster="Daddy & Me Back to School",
        audience="Daddy & Me",
        season="Back to School",
        patterns=(
            r"^back-to-school-daddy-and-me-photo-outfits$",
            r"^back-to-school-daddy-and-me-photo-outfits-\d{4}-edition$",
        ),
    ),
    Rule(
        canonical_slug="back-to-school-matching-outfits-for-first-day-photos",
        canonical_title="Back-to-School Matching Outfits for First-Day Photos",
        topic_cluster="Family Back to School",
        audience="Family",
        season="Back to School",
        patterns=(
            r"^back-to-school-matching-outfits-for-first-day-photos$",
            r"^back-to-school-matching-outfits-for-first-day-photos-\d{4}$",
        ),
    ),
    Rule(
        canonical_slug="best-family-matching-outfits-for-harvest-season",
        canonical_title="Best Family Matching Outfits for Harvest Season",
        topic_cluster="Fall Harvest Family Matching",
        audience="Family",
        season="Fall",
        patterns=(
            r"^best-family-matching-outfits-for-harvest-season$",
            r"^best-family-matching-outfits-for-harvest-season-\d{4}-edition$",
        ),
    ),
    Rule(
        canonical_slug="matching-family-outfits-for-august-vacations",
        canonical_title="Matching Family Outfits for August Vacations",
        topic_cluster="Late Summer Family Vacation",
        audience="Family",
        season="Summer",
        patterns=(
            r"^matching-family-outfits-for-august-vacations$",
            r"^matching-family-outfits-for-august-vacations-\d{4}-edition$",
        ),
    ),
    Rule(
        canonical_slug="october-family-style-cozy-matching-looks-for-autumn",
        canonical_title="October Family Style: Cozy Matching Looks for Autumn",
        topic_cluster="October Family Matching",
        audience="Family",
        season="Fall",
        patterns=(
            r"^october-family-style-cozy-matching-looks-for-autumn$",
            r"^october-family-style-cozy-matching-looks-for-autumn-\d{4}-edition$",
        ),
    ),
    Rule(
        canonical_slug="winter-family-photo-outfits-matching-looks-for-cold-weather",
        canonical_title="Winter Family Photo Outfits: Matching Looks for Cold Weather",
        topic_cluster="Winter Family Photos",
        audience="Family",
        season="Winter",
        patterns=(
            r"^winter-family-photo-outfits-matching-looks-for-cold-weather$",
            r"^winter-family-photo-outfits-matching-looks-for-cold-weather-\d{4}$",
        ),
    ),
    Rule(
        canonical_slug="summer-vacation-matching-family-outfits-guide",
        canonical_title="Summer Vacation Matching Family Outfits Guide",
        topic_cluster="Summer Family Vacation",
        audience="Family",
        season="Summer",
        patterns=(
            r"^summer-vacation-matching-family-outfits-guide$",
            r"^summer-vacation-matching-family-outfits-guide-1$",
        ),
    ),
    Rule(
        canonical_slug="apple-picking-matching-outfits-for-the-whole-family",
        canonical_title="Apple Picking Matching Outfits for the Whole Family",
        topic_cluster="Apple Picking Family Matching",
        audience="Family",
        season="Fall",
        patterns=(
            r"^apple-picking-matching-outfits-for-the-whole-family$",
            r"^apple-picking-family-matching-outfits-\d{4}$",
        ),
    ),
    Rule(
        canonical_slug="new-year-new-matching-looks-family-fashion",
        canonical_title="New Year, New Matching Looks: Family Fashion",
        topic_cluster="New Year Family Matching",
        audience="Family",
        season="New Year's",
        patterns=(
            r"^new-year-new-matching-looks-family-fashion-for-\d{4}$",
            r"^new-years-eve-family-matching-outfits-\d{4}$",
        ),
    ),
    Rule(
        canonical_slug="easter-sunday-family-matching-outfits",
        canonical_title="Easter Sunday Family Matching Outfits",
        topic_cluster="Family Easter",
        audience="Family",
        season="Easter",
        patterns=(
            r"^easter-sunday-family-matching-outfits-\d{4}$",
            r"^matching-family-outfits-for-easter-brunch-\d{4}$",
        ),
    ),
    Rule(
        canonical_slug="mommy-and-me-easter-outfit-ideas",
        canonical_title="Mommy and Me Easter Outfit Ideas",
        topic_cluster="Mommy & Me Easter",
        audience="Mommy & Me",
        season="Easter",
        patterns=(
            r"^mommy-and-me-easter-outfit-ideas-for-\d{4}$",
            r"^mommy-and-me-easter-dresses-\d{4}$",
        ),
    ),
    Rule(
        canonical_slug="mothers-day-matching-outfits-mommy-and-me-guide",
        canonical_title="Mother's Day Matching Outfits: Mommy and Me Guide",
        topic_cluster="Mommy & Me Mother's Day",
        audience="Mommy & Me",
        season="Mother's Day",
        patterns=(
            r"^mothers-day-matching-outfits-mommy-and-me-guide-\d{4}$",
            r"^best-mommy-and-me-dresses-for-mothers-day-\d{4}$",
        ),
    ),
    Rule(
        canonical_slug="summer-matching-family-outfits",
        canonical_title="Summer Matching Family Outfits",
        topic_cluster="Summer Family Matching",
        audience="Family",
        season="Summer",
        patterns=(r"^summer-matching-family-outfits-for-\d{4}$",),
    ),
    Rule(
        canonical_slug="christmas-matching-family-pajamas",
        canonical_title="Christmas Matching Family Pajamas",
        topic_cluster="Christmas Family Pajamas",
        audience="Family",
        season="Christmas",
        patterns=(r"^christmas-matching-family-pajamas-for-\d{4}$",),
    ),
    Rule(
        canonical_slug="holiday-family-matching-outfits-complete-guide",
        canonical_title="Holiday Family Matching Outfits Complete Guide",
        topic_cluster="Holiday Family Matching",
        audience="Family",
        season="Holiday",
        patterns=(r"^holiday-family-matching-outfits-complete-\d{4}-guide$",),
    ),
    Rule(
        canonical_slug="daddy-and-me-spring-outfits",
        canonical_title="Daddy and Me Spring Outfits",
        topic_cluster="Daddy & Me Spring",
        audience="Daddy & Me",
        season="Spring",
        patterns=(r"^daddy-and-me-spring-outfits-for-\d{4}$",),
    ),
    Rule(
        canonical_slug="daddy-and-me-fall-outfit-ideas",
        canonical_title="Daddy and Me Fall Outfit Ideas",
        topic_cluster="Daddy & Me Fall",
        audience="Daddy & Me",
        season="Fall",
        patterns=(r"^daddy-and-me-fall-outfit-ideas-for-\d{4}$",),
    ),
    Rule(
        canonical_slug="mommy-and-me-back-to-school-style-guide",
        canonical_title="Mommy and Me Back-to-School Style Guide",
        topic_cluster="Mommy & Me Back to School",
        audience="Mommy & Me",
        season="Back to School",
        patterns=(r"^mommy-and-me-back-to-school-style-guide-\d{4}$",),
    ),
    Rule(
        canonical_slug="mommy-and-me-summer-dress-guide",
        canonical_title="Mommy and Me Summer Dress Guide",
        topic_cluster="Mommy & Me Summer Dresses",
        audience="Mommy & Me",
        season="Summer",
        patterns=(r"^mommy-and-me-summer-dress-guide-\d{4}$",),
    ),
    Rule(
        canonical_slug="mommy-and-me-thanksgiving-style-guide",
        canonical_title="Mommy and Me Thanksgiving Style Guide",
        topic_cluster="Mommy & Me Thanksgiving",
        audience="Mommy & Me",
        season="Thanksgiving",
        patterns=(r"^mommy-and-me-thanksgiving-style-guide-\d{4}$",),
    ),
)


TITLE_REPLACEMENTS = (
    ("mommy and me", "Mommy and Me"),
    ("daddy and me", "Daddy and Me"),
    ("mother daughter", "Mother-Daughter"),
    ("family", "Family"),
    ("valentines day", "Valentine's Day"),
    ("mothers day", "Mother's Day"),
    ("fathers day", "Father's Day"),
    ("new years eve", "New Year's Eve"),
    ("new year", "New Year"),
    ("4th of july", "4th of July"),
    ("back to school", "Back-to-School"),
    ("black friday", "Black Friday"),
    ("apple picking", "Apple Picking"),
    ("pumpkin patch", "Pumpkin Patch"),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-xml", help="Use a local sitemap XML instead of fetching live.")
    parser.add_argument("--sitemap-url", default=SITEMAP_URL)
    parser.add_argument("--slug-audit-csv", required=True)
    parser.add_argument("--plan-csv", required=True)
    return parser.parse_args()


def fetch_sitemap_xml(args: argparse.Namespace) -> bytes:
    if args.input_xml:
        return Path(args.input_xml).read_bytes()

    request = urllib.request.Request(
        args.sitemap_url,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/xml,text/xml;q=0.9,*/*;q=0.8",
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.read()
    except Exception:
        result = subprocess.run(
            ["curl", "-A", "Mozilla/5.0", "-fsSL", args.sitemap_url],
            check=True,
            capture_output=True,
        )
        return result.stdout


def extract_slugs(xml_bytes: bytes) -> list[str]:
    root = ET.fromstring(xml_bytes)
    slugs = []
    for url in root.findall("sm:url", SITEMAP_NS):
        loc = url.find("sm:loc", SITEMAP_NS)
        if loc is None or not loc.text:
            continue
        full_url = loc.text.strip()
        if full_url.rstrip("/") == "https://www.dresslikemommy.com/blogs/news":
            continue
        slugs.append(full_url.split("/blogs/news/")[-1].strip("/"))
    return slugs


def extract_year(slug: str) -> str:
    match = re.search(r"(20\d{2})", slug)
    return match.group(1) if match else ""


def normalize_slug(slug: str) -> str:
    normalized = re.sub(r"-20\d{2}(?=-|$)", "", slug)
    normalized = re.sub(r"-edition(?=-|$)", "", normalized)
    normalized = re.sub(r"-1$", "", normalized)
    normalized = re.sub(r"-+", "-", normalized).strip("-")
    if normalized.endswith("-for"):
        normalized = normalized[:-4]
    return normalized


def match_rule(slug: str) -> Optional[Rule]:
    for rule in MANUAL_RULES:
        for pattern in rule.patterns:
            if re.match(pattern, slug):
                return rule
    return None


def detect_audience(slug: str) -> str:
    if "mommy-and-me" in slug:
        return "Mommy & Me"
    if "daddy-and-me" in slug:
        return "Daddy & Me"
    if "mother-daughter" in slug:
        return "Mother-Daughter"
    if "couple" in slug or "couples" in slug:
        return "Couples"
    if "family" in slug:
        return "Family"
    return "General"


def detect_season(slug: str) -> str:
    checks = (
        ("valentines", "Valentine's Day"),
        ("easter", "Easter"),
        ("mothers-day", "Mother's Day"),
        ("fathers-day", "Father's Day"),
        ("new-year", "New Year's"),
        ("new-years", "New Year's"),
        ("christmas", "Christmas"),
        ("thanksgiving", "Thanksgiving"),
        ("halloween", "Halloween"),
        ("4th-of-july", "4th of July"),
        ("memorial-day", "4th of July"),
        ("back-to-school", "Back to School"),
        ("black-friday", "Holiday"),
        ("holiday", "Holiday"),
        ("winter", "Winter"),
        ("january", "Winter"),
        ("spring", "Spring"),
        ("summer", "Summer"),
        ("swimsuit", "Summer"),
        ("beach", "Summer"),
        ("august", "Summer"),
        ("hot-weather", "Summer"),
        ("fall", "Fall"),
        ("autumn", "Fall"),
        ("apple-picking", "Fall"),
        ("pumpkin", "Fall"),
        ("october", "Fall"),
        ("harvest", "Fall"),
        ("september", "Fall"),
    )
    for token, season in checks:
        if token in slug:
            return season
    return "Evergreen"


def build_title(slug: str) -> str:
    title = slug.replace("-", " ")
    title = re.sub(r"\s+", " ", title).strip().title()
    title = title.replace(" And ", " and ")
    title = title.replace(" Of ", " of ")
    title = title.replace(" For ", " for ")
    title = title.replace(" To ", " to ")
    title = title.replace(" The ", " the ")
    title = title.replace(" In ", " in ")
    title = title.replace(" With ", " with ")
    for source, target in TITLE_REPLACEMENTS:
        title = re.sub(rf"\b{re.escape(source.title())}\b", target, title)
        title = re.sub(rf"\b{re.escape(source)}\b", target, title, flags=re.IGNORECASE)
    return title


def build_topic_cluster(canonical_slug: str, audience: str, season: str) -> str:
    if "pajama" in canonical_slug:
        return f"{season} {audience} Pajamas".replace("General ", "")
    if "swimsuit" in canonical_slug or "swim" in canonical_slug:
        return f"{season} {audience} Swimsuits".replace("General ", "")
    if "photo" in canonical_slug:
        return f"{season} {audience} Photos".replace("General ", "")
    if "back-to-school" in canonical_slug:
        return f"{audience} Back to School".replace("General ", "")
    if "halloween" in canonical_slug:
        return f"{audience} Halloween".replace("General ", "")
    if "thanksgiving" in canonical_slug:
        return f"{audience} Thanksgiving".replace("General ", "")
    if "christmas" in canonical_slug:
        return f"{audience} Christmas".replace("General ", "")
    if "holiday" in canonical_slug:
        return f"{audience} Holiday".replace("General ", "")
    if "valentines" in canonical_slug:
        return f"{audience} Valentine's Day".replace("General ", "")
    if "easter" in canonical_slug:
        return f"{audience} Easter".replace("General ", "")
    if "mothers-day" in canonical_slug:
        return f"{audience} Mother's Day".replace("General ", "")
    if "fathers-day" in canonical_slug:
        return f"{audience} Father's Day".replace("General ", "")
    if "new-year" in canonical_slug or "new-years" in canonical_slug:
        return f"{audience} New Year's".replace("General ", "")
    if "fall" in canonical_slug or "autumn" in canonical_slug:
        return f"{season} {audience} Matching".replace("General ", "")
    if "winter" in canonical_slug:
        return f"{season} {audience} Matching".replace("General ", "")
    if "spring" in canonical_slug:
        return f"{season} {audience} Matching".replace("General ", "")
    if "summer" in canonical_slug or "beach" in canonical_slug or "vacation" in canonical_slug:
        return f"{season} {audience} Matching".replace("General ", "")
    return build_title(canonical_slug)


def metadata_for_slug(slug: str) -> tuple[str, str, str, str]:
    rule = match_rule(slug)
    if rule:
        return (
            rule.canonical_slug,
            rule.canonical_title,
            rule.topic_cluster,
            rule.audience,
            rule.season,
        )

    canonical_slug = normalize_slug(slug)
    audience = detect_audience(canonical_slug)
    season = detect_season(canonical_slug)
    canonical_title = build_title(canonical_slug)
    topic_cluster = build_topic_cluster(canonical_slug, audience, season)
    return canonical_slug, canonical_title, topic_cluster, audience, season


def write_slug_audit(slugs: list[str], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=("position", "slug", "url"))
        writer.writeheader()
        for index, slug in enumerate(slugs, start=1):
            writer.writerow(
                {
                    "position": index,
                    "slug": slug,
                    "url": f"https://www.dresslikemommy.com/blogs/news/{slug}",
                }
            )


def write_plan(slugs: list[str], output_path: Path) -> tuple[int, int]:
    canonical_map = {}
    redirect_rows = []
    for slug in slugs:
        canonical_slug, canonical_title, topic_cluster, audience, season = metadata_for_slug(slug)
        canonical_map.setdefault(
            canonical_slug,
            {
                "canonical_slug": canonical_slug,
                "canonical_title": canonical_title,
                "topic_cluster": topic_cluster,
                "audience": audience,
                "season": season,
            },
        )
        if slug != canonical_slug:
            redirect_rows.append(
                {
                    "canonical_slug": canonical_slug,
                    "canonical_title": canonical_title,
                    "topic_cluster": topic_cluster,
                    "audience": audience,
                    "season": season,
                    "redirect_from_slug": slug,
                    "redirect_from_year": extract_year(slug),
                    "keep_or_redirect": "REDIRECT",
                    "status": "not started",
                }
            )

    keep_rows = [
        {
            **row,
            "redirect_from_slug": "",
            "redirect_from_year": "",
            "keep_or_redirect": "KEEP",
            "status": "not started",
        }
        for row in canonical_map.values()
    ]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="") as handle:
        fieldnames = (
            "canonical_slug",
            "canonical_title",
            "topic_cluster",
            "audience",
            "season",
            "redirect_from_slug",
            "redirect_from_year",
            "keep_or_redirect",
            "status",
        )
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()

        for row in sorted(keep_rows, key=lambda item: item["canonical_slug"]):
            writer.writerow(row)

        for row in sorted(
            redirect_rows,
            key=lambda item: (
                item["canonical_slug"],
                item["redirect_from_year"] or "9999",
                item["redirect_from_slug"],
            ),
        ):
            writer.writerow(row)

    return len(keep_rows), len(redirect_rows)


def main() -> int:
    args = parse_args()
    xml_bytes = fetch_sitemap_xml(args)
    slugs = extract_slugs(xml_bytes)
    if len(slugs) != 254:
        print(f"Expected 254 article slugs, found {len(slugs)}", file=sys.stderr)

    write_slug_audit(slugs, Path(args.slug_audit_csv))
    keep_count, redirect_count = write_plan(slugs, Path(args.plan_csv))
    print(
        f"Generated slug audit for {len(slugs)} blog posts and consolidation plan with "
        f"{keep_count} canonical rows and {redirect_count} redirect rows."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
