#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

from bs4 import BeautifulSoup


DEFAULT_ENV_FILE = Path.home() / ".config" / "dresslikemommy" / "shopify-admin.env"
EMPTY_VALUES = {"", "-", "--", "—", "–", "n/a"}
MEASUREMENT_TOKENS = (
    "height",
    "chest",
    "bust",
    "hip",
    "waist",
    "length",
    "sleeve",
    "shoulder",
    "pant",
    "short",
    "skirt",
    "garment",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Normalize Shopify size-chart tables to expose cm/in and kg/lbs.")
    parser.add_argument("handles", nargs="+", help="Shopify product handles to repair")
    parser.add_argument(
        "--env-file",
        default=os.environ.get("SHOPIFY_ENV_FILE", str(DEFAULT_ENV_FILE)),
        help="Path to the Shopify admin env file",
    )
    return parser.parse_args()


def load_env_file(path: Path) -> None:
    if not path.exists():
        return

    for raw_line in path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[7:].strip()
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key.strip(), value)


def shopify_request(query: str, variables: dict[str, object]) -> dict[str, object]:
    domain = os.environ.get("SHOPIFY_STORE_DOMAIN", "dresslikemommy-com.myshopify.com")
    token = os.environ.get("SHOPIFY_ADMIN_ACCESS_TOKEN")
    if not token:
        raise SystemExit("SHOPIFY_ADMIN_ACCESS_TOKEN not set")

    payload = json.dumps({"query": query, "variables": variables}).encode("utf-8")
    request = urllib.request.Request(
        f"https://{domain}/admin/api/2025-01/graphql.json",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": token,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise SystemExit(f"Shopify API request failed: {exc.read().decode('utf-8', 'ignore')}") from exc

    if data.get("errors"):
        raise SystemExit(f"Shopify GraphQL errors: {json.dumps(data['errors'])}")
    return data


def normalize_unit_token(value: str) -> str:
    token = str(value or "").strip().lower()
    mapping = {
        "cm": "cm",
        "cms": "cm",
        "centimeter": "cm",
        "centimeters": "cm",
        "centimetre": "cm",
        "centimetres": "cm",
        "in": "in",
        "inch": "in",
        "inches": "in",
        "kg": "kg",
        "kgs": "kg",
        "kilogram": "kg",
        "kilograms": "kg",
        "lb": "lbs",
        "lbs": "lbs",
        "pounds": "lbs",
    }
    return mapping.get(token, "")


def parse_header_text(text: str) -> tuple[str, list[str]]:
    raw = " ".join(str(text or "").split())
    match = re.match(r"^(.*?)(?:\s*\(([^)]*)\))?$", raw)
    if not match:
        return raw, []
    label = (match.group(1) or raw).strip()
    units = []
    if match.group(2):
        units = [normalize_unit_token(unit) for unit in match.group(2).split("/") if normalize_unit_token(unit)]
    return label, units


def convertible_pair(unit: str) -> tuple[str, str] | None:
    normalized = normalize_unit_token(unit)
    if normalized in {"cm", "in"}:
        return ("cm", "in")
    if normalized in {"kg", "lbs"}:
        return ("kg", "lbs")
    return None


def infer_pair_from_values(values: list[str]) -> tuple[str, str] | None:
    seen = set()
    for value in values:
        lowered = value.lower()
        if "cm" in lowered or re.search(r"\b(?:in|inch|inches)\b", lowered):
            seen.add("cm")
        if re.search(r"\b(?:in|inch|inches)\b", lowered):
            seen.add("in")
        if re.search(r"\bkg\b", lowered):
            seen.add("kg")
        if re.search(r"\blbs?\b", lowered):
            seen.add("lbs")

    if "cm" in seen or "in" in seen:
        return ("cm", "in")
    if "kg" in seen or "lbs" in seen:
        return ("kg", "lbs")
    return None


def infer_pair_from_label(label: str) -> tuple[str, str] | None:
    lowered = label.lower()
    if lowered in {"size", "age", "—"}:
        return None
    if "weight" in lowered:
        return ("kg", "lbs")
    if any(token in lowered for token in MEASUREMENT_TOKENS):
        return ("cm", "in")
    return None


def infer_header_pair(label: str, units: list[str], values: list[str]) -> tuple[str, str] | None:
    for unit in units:
        pair = convertible_pair(unit)
        if pair:
            return pair

    pair = infer_pair_from_values(values)
    if pair:
        return pair

    return infer_pair_from_label(label)


def format_num(value: float) -> str:
    if float(value).is_integer():
        return str(int(value))
    return f"{value:.1f}".rstrip("0").rstrip(".")


def to_dual_unit(value: str, metric_unit: str, imperial_unit: str, multiplier: float) -> str:
    text = " ".join(str(value or "").split())
    if text.lower() in EMPTY_VALUES:
        return "—"

    lowered = text.lower()
    if "/" in text and metric_unit in lowered and imperial_unit in lowered:
        return text

    range_match = re.fullmatch(
        rf"(-?\d+(?:\.\d+)?)\s*[-–—]\s*(-?\d+(?:\.\d+)?)\s*(?:{re.escape(metric_unit)})?",
        text,
        re.IGNORECASE,
    )
    if range_match:
        low = float(range_match.group(1))
        high = float(range_match.group(2))
        return (
            f"{format_num(low)}-{format_num(high)} {metric_unit} / "
            f"{format_num(low * multiplier)}-{format_num(high * multiplier)} {imperial_unit}"
        )

    single_match = re.fullmatch(rf"(-?\d+(?:\.\d+)?)\s*(?:{re.escape(metric_unit)})?", text, re.IGNORECASE)
    if single_match:
        numeric = float(single_match.group(1))
        return f"{format_num(numeric)} {metric_unit} / {format_num(numeric * multiplier)} {imperial_unit}"

    return text


def normalize_table(table) -> tuple[bool, int]:
    rows = table.find_all("tr")
    if len(rows) < 2:
        return False, 0

    header_cells = rows[0].find_all(["th", "td"])
    body_rows = [row.find_all("td") for row in rows[1:]]
    body_rows = [cells for cells in body_rows if len(cells) == len(header_cells)]
    if not body_rows:
        return False, 0

    changed = False
    normalized_columns = 0

    for index, header_cell in enumerate(header_cells):
        header_text = header_cell.get_text(" ", strip=True)
        label, units = parse_header_text(header_text)
        column_values = [cells[index].get_text(" ", strip=True) for cells in body_rows if cells[index].get_text(" ", strip=True)]
        pair = infer_header_pair(label, units, column_values)
        if not pair:
            continue

        metric_unit, imperial_unit = pair
        multiplier = 2.20462 if metric_unit == "kg" else 1 / 2.54
        normalized_columns += 1

        normalized_header = f"{label} ({metric_unit}/{imperial_unit})"
        if header_text != normalized_header:
            header_cell.string = normalized_header
            changed = True

        for cells in body_rows:
            cell = cells[index]
            existing = cell.get_text(" ", strip=True)
            normalized = to_dual_unit(existing, metric_unit, imperial_unit, multiplier)
            if existing != normalized:
                cell.string = normalized
                changed = True

    return changed, normalized_columns


def normalize_description_html(description_html: str) -> tuple[str, bool, int]:
    soup = BeautifulSoup(description_html, "html.parser")
    changed = False
    normalized_tables = 0

    for table in soup.find_all("table"):
        table_id = (table.get("id") or "").lower()
        if "size-chart" not in table_id:
            continue

        table_changed, normalized_columns = normalize_table(table)
        if table_changed:
            changed = True
        if normalized_columns:
            normalized_tables += 1

    return soup.decode(formatter="html"), changed, normalized_tables


def fetch_product(handle: str) -> dict[str, object] | None:
    query = """
    query ProductByHandle($handle: String!) {
      productByHandle(handle: $handle) {
        id
        handle
        title
        descriptionHtml
        onlineStoreUrl
      }
    }
    """
    data = shopify_request(query, {"handle": handle})
    return data.get("data", {}).get("productByHandle")


def update_product_description(product_id: str, description_html: str) -> dict[str, object]:
    mutation = """
    mutation ProductUpdate($input: ProductInput!) {
      productUpdate(input: $input) {
        product {
          id
          handle
          updatedAt
        }
        userErrors {
          field
          message
        }
      }
    }
    """
    data = shopify_request(mutation, {"input": {"id": product_id, "descriptionHtml": description_html}})
    payload = data.get("data", {}).get("productUpdate", {})
    if payload.get("userErrors"):
        raise SystemExit(f"productUpdate userErrors: {json.dumps(payload['userErrors'])}")
    return payload.get("product", {})


def main() -> int:
    args = parse_args()
    load_env_file(Path(args.env_file).expanduser())

    changed_handles = []
    unchanged_handles = []

    for handle in args.handles:
        product = fetch_product(handle)
        if not product:
            print(f"{handle}: not found", file=sys.stderr)
            return 1

        normalized_html, changed, normalized_tables = normalize_description_html(product["descriptionHtml"] or "")
        if not changed:
            unchanged_handles.append({"handle": handle, "tables": normalized_tables, "url": product.get("onlineStoreUrl")})
            continue

        updated = update_product_description(product["id"], normalized_html)
        changed_handles.append(
            {
                "handle": handle,
                "tables": normalized_tables,
                "updated_at": updated.get("updatedAt"),
                "url": product.get("onlineStoreUrl"),
            }
        )

    print(json.dumps({"changed": changed_handles, "unchanged": unchanged_handles}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
