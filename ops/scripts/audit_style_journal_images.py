#!/usr/bin/env python3
"""Fail fast when Style Journal article images are duplicated or drift."""

from __future__ import annotations

import argparse
import csv
import hashlib
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
HANDLE_IMAGE_RE = re.compile(
    r"when\s+'(?P<handle>[^']+)'\s*\n\s*assign\s+image_asset\s*=\s*'(?P<asset>[^']+)'",
    re.MULTILINE,
)
REQUIRED_MANIFEST_COLUMNS = ("index", "handle", "asset", "source", "title")


@dataclass(frozen=True)
class ManifestRow:
    line_no: int
    index: str
    handle: str
    asset: str
    source: str
    title: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Audit the Style Journal image manifest, Liquid fallback mapping, "
            "and local asset files for duplicate blog images."
        )
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=REPO_ROOT / "ops/style-journal-image-manifest.tsv",
        help="TSV manifest with index, handle, asset, source, and title columns.",
    )
    parser.add_argument(
        "--snippet",
        type=Path,
        default=REPO_ROOT / "snippets/article-featured-image-fallback.liquid",
        help="Liquid snippet that maps article handles to fallback image assets.",
    )
    parser.add_argument(
        "--assets-dir",
        type=Path,
        default=REPO_ROOT / "assets",
        help="Theme assets directory containing the style-journal image files.",
    )
    parser.add_argument(
        "--required-prefix",
        default="style-journal-",
        help="Required filename prefix for manifest assets. Use an empty value to disable.",
    )
    return parser.parse_args()


def display_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def read_manifest(path: Path, errors: list[str]) -> list[ManifestRow]:
    if not path.exists():
        errors.append(f"manifest is missing: {display_path(path)}")
        return []

    rows: list[ManifestRow] = []
    with path.open(newline="", encoding="utf-8") as manifest_file:
        reader = csv.DictReader(manifest_file, delimiter="\t")
        missing_columns = [
            column for column in REQUIRED_MANIFEST_COLUMNS if column not in (reader.fieldnames or [])
        ]
        if missing_columns:
            errors.append(
                f"manifest is missing required columns: {', '.join(missing_columns)}"
            )
            return []

        for line_no, raw_row in enumerate(reader, start=2):
            row = ManifestRow(
                line_no=line_no,
                index=(raw_row.get("index") or "").strip(),
                handle=(raw_row.get("handle") or "").strip(),
                asset=(raw_row.get("asset") or "").strip(),
                source=(raw_row.get("source") or "").strip(),
                title=(raw_row.get("title") or "").strip(),
            )
            if not row.handle:
                errors.append(f"manifest line {line_no} has a blank handle")
            if not row.asset:
                errors.append(f"manifest line {line_no} has a blank asset")
            rows.append(row)

    if not rows:
        errors.append("manifest has no article rows")

    return rows


def read_liquid_mapping(path: Path, errors: list[str]) -> dict[str, tuple[str, int]]:
    if not path.exists():
        errors.append(f"Liquid snippet is missing: {display_path(path)}")
        return {}

    text = path.read_text(encoding="utf-8")
    hits: dict[str, list[tuple[str, int]]] = defaultdict(list)
    for match in HANDLE_IMAGE_RE.finditer(text):
        line_no = text.count("\n", 0, match.start()) + 1
        hits[match.group("handle")].append((match.group("asset"), line_no))

    mapping: dict[str, tuple[str, int]] = {}
    for handle, assignments in sorted(hits.items()):
        unique_assets = sorted({asset for asset, _line_no in assignments})
        lines = ", ".join(str(line_no) for _asset, line_no in assignments)
        if len(assignments) > 1:
            errors.append(
                f"Liquid handle '{handle}' is mapped {len(assignments)} times on lines {lines}"
            )
        if len(unique_assets) > 1:
            errors.append(
                f"Liquid handle '{handle}' maps to multiple assets: {', '.join(unique_assets)}"
            )
        mapping[handle] = assignments[0]

    if not mapping:
        errors.append(f"no quoted article-handle image mappings found in {display_path(path)}")

    return mapping


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as image_file:
        for chunk in iter(lambda: image_file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def add_duplicate_value_errors(
    label: str,
    rows: list[ManifestRow],
    value_getter,
    errors: list[str],
) -> None:
    values = [value_getter(row) for row in rows if value_getter(row)]
    for value, count in sorted(Counter(values).items()):
        if count < 2:
            continue
        handles = [row.handle for row in rows if value_getter(row) == value]
        errors.append(
            f"duplicate {label} '{value}' is used by {count} manifest rows: {', '.join(handles)}"
        )


def audit() -> int:
    args = parse_args()
    errors: list[str] = []

    manifest_rows = read_manifest(args.manifest, errors)
    liquid_mapping = read_liquid_mapping(args.snippet, errors)

    add_duplicate_value_errors("handle", manifest_rows, lambda row: row.handle, errors)
    add_duplicate_value_errors("asset", manifest_rows, lambda row: row.asset, errors)
    add_duplicate_value_errors("source", manifest_rows, lambda row: row.source, errors)

    manifest_handles = {row.handle for row in manifest_rows}
    manifest_assets = {row.asset for row in manifest_rows}

    extra_liquid_handles = sorted(set(liquid_mapping) - manifest_handles)
    if extra_liquid_handles:
        errors.append(
            "Liquid has article image mappings missing from the manifest: "
            + ", ".join(extra_liquid_handles)
        )

    missing_liquid_handles = sorted(manifest_handles - set(liquid_mapping))
    if missing_liquid_handles:
        errors.append(
            "manifest handles missing from Liquid image mapping: "
            + ", ".join(missing_liquid_handles)
        )

    if args.required_prefix:
        for row in manifest_rows:
            if row.asset and not row.asset.startswith(args.required_prefix):
                errors.append(
                    f"manifest line {row.line_no} asset '{row.asset}' does not start with "
                    f"'{args.required_prefix}'"
                )

    file_hashes: dict[str, list[str]] = defaultdict(list)
    existing_assets = 0
    for row in manifest_rows:
        if not row.asset:
            continue
        asset_path = args.assets_dir / row.asset
        if not asset_path.exists():
            errors.append(
                f"asset for handle '{row.handle}' is missing: {display_path(asset_path)}"
            )
            continue
        if not asset_path.is_file():
            errors.append(
                f"asset for handle '{row.handle}' is not a file: {display_path(asset_path)}"
            )
            continue
        existing_assets += 1
        file_hashes[sha256_file(asset_path)].append(row.asset)

    for digest, assets in sorted(file_hashes.items()):
        unique_assets = sorted(set(assets))
        if len(unique_assets) > 1:
            errors.append(
                "byte-identical image files share sha256 "
                f"{digest[:12]}: {', '.join(unique_assets)}"
            )

    for row in manifest_rows:
        assigned = liquid_mapping.get(row.handle)
        if assigned is None:
            continue
        assigned_asset, line_no = assigned
        if assigned_asset != row.asset:
            errors.append(
                f"Liquid line {line_no} maps '{row.handle}' to '{assigned_asset}', "
                f"but manifest expects '{row.asset}'"
            )
        if assigned_asset and assigned_asset not in manifest_assets:
            errors.append(
                f"Liquid line {line_no} uses asset '{assigned_asset}' for '{row.handle}', "
                "but that asset is not in the manifest"
            )

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(
            f"Style Journal image audit failed with {len(errors)} issue(s).",
            file=sys.stderr,
        )
        return 1

    print(
        f"OK: audited {len(manifest_rows)} Style Journal mappings with "
        f"{len(manifest_assets)} unique filenames, {existing_assets} local files, "
        f"and {len(file_hashes)} unique image hashes."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(audit())
