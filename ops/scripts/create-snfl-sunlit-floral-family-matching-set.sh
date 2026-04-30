#!/usr/bin/env bash
set -euo pipefail

ROOT="/Users/fsuels/Projects/dresslikemommy"
ENV_FILE="${SHOPIFY_ENV_FILE:-${HOME}/.config/dresslikemommy/shopify-admin.env}"

if [[ -f "$ENV_FILE" ]]; then
  # shellcheck disable=SC1090
  source "$ENV_FILE"
fi

: "${SHOPIFY_STORE_DOMAIN:=dresslikemommy-com.myshopify.com}"
: "${SHOPIFY_ADMIN_ACCESS_TOKEN:?SHOPIFY_ADMIN_ACCESS_TOKEN not set}"

API="https://${SHOPIFY_STORE_DOMAIN}/admin/api/2025-01/graphql.json"
TOKEN="${SHOPIFY_ADMIN_ACCESS_TOKEN}"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

HANDLE="sunlit-floral-family-matching-set"
TITLE="Sunlit Floral Family Matching Set - Dress & Shirt"
SEO_TITLE="Sunlit Floral Family Set | Dress Like Mommy"
SEO_DESCRIPTION="Lightweight woven family matching set with floral dresses and collared shirts for mom, dad, girls and boys. Sizes 2Y-10Y, Mother S-2XL, Father S-4XL."
PRINT_NAME="Sunlit Floral"
SHORTCODE="SNFL"
COLOR_TOKEN="SUNNY"
COLOR_NAME="Sunlit Floral"
LISTING_MODE="Family Matching"
CATEGORY="FamilySet"
PRODUCT_TYPE="Matching Family Sets"
CUSTOM_TYPE="Two-Piece Set"
TAXONOMY_GID="gid://shopify/TaxonomyCategory/aa-1-11"
EXPECTED_TAXONOMY_FULL_NAME="Apparel & Accessories > Clothing > Outfit Sets"
MERCH_SUBCATEGORY="Set"
MERCH_SUBCATEGORY2="Summer Family Matching Set"
MERCH_STYLE="Matching Family Set"
MERCH_TYPE="Two-Piece Set"
MERCH_COLLECTION_TAG="Matching Family Set"
SEASON="Summer"
VENDOR_URL="https://detail.1688.com/offer/1035829442886.html"
VENDOR="dresslikemommy.com"
CHILD_PRICE="28.99"
ADULT_PRICE="31.99"
PRICE_NEIGHBOR_HANDLE="citrus-bloom-family-matching-set"
SIZE_NEIGHBOR_HANDLE="citrus-bloom-family-matching-set"

SCRIPT_PATH="${ROOT}/ops/scripts/create-snfl-sunlit-floral-family-matching-set.sh"
UPLOAD_DIR="${ROOT}/uploads/${HANDLE}"
LISTING_MD="${ROOT}/ops/listings/${HANDLE}-listing.md"
CSV_OUT="${ROOT}/ops/listings/${HANDLE}-shopify-import.csv"
VERIFY_JSON_OUT="${ROOT}/ops/listings/verify-${HANDLE}.json"
SIZE_CHART_OUT="${ROOT}/ops/listings/size-chart-${HANDLE}.json"
BODY_HTML_OUT="${ROOT}/ops/listings/body-${HANDLE}.html"
CSV_HEADER_SOURCE="${ROOT}/bird-chirping-mommy-and-me-pajamas-shopify-import.csv"

mkdir -p "${ROOT}/ops/listings" "$UPLOAD_DIR"

gql() {
  local query="$1"
  local variables="${2-}"
  if [[ -z "$variables" ]]; then
    variables='{}'
  fi
  curl -sS -X POST "$API" \
    -H "X-Shopify-Access-Token: $TOKEN" \
    -H "Content-Type: application/json" \
    -d "$(jq -nc --arg q "$query" --argjson v "$variables" '{query:$q, variables:$v}')"
}

check_graphql_errors() {
  local response="$1"
  local label="$2"
  local errors
  errors="$(echo "$response" | jq -c '.errors // []')"
  if [[ "$errors" != "[]" && "$errors" != "null" ]]; then
    echo "ERROR: ${label} GraphQL errors: ${errors}" >&2
    exit 1
  fi
}

check_user_errors() {
  local response="$1"
  local path="$2"
  local label="$3"
  local errors
  errors="$(echo "$response" | jq -c "${path} // []")"
  if [[ "$errors" != "[]" && "$errors" != "null" ]]; then
    echo "ERROR: ${label} userErrors: ${errors}" >&2
    exit 1
  fi
}

compare_at_price() {
  python3 - "$1" <<'PY'
from decimal import Decimal, ROUND_FLOOR
import sys

price = Decimal(sys.argv[1])
value = price * Decimal("1.15")
dollars = value.to_integral_value(rounding=ROUND_FLOOR)
candidate = dollars + Decimal("0.99")
if candidate < value:
    candidate = dollars + Decimal("1.99")
print(f"{candidate:.2f}")
PY
}

CHILD_COMPARE="$(compare_at_price "$CHILD_PRICE")"
ADULT_COMPARE="$(compare_at_price "$ADULT_PRICE")"

cat > "${WORK}/size_chart.json" <<'JSON'
[
  {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"90/2码","picker_label":"Child 2 Years","sku_suffix":"KID2Y","age":"2","weight":"7.5-11 kg","height":"80-90 cm","chest_cm":58,"hip_cm":62,"waist_cm":58,"length_cm":50,"skirt_cm":50,"pant_cm":0},
  {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"100/4码","picker_label":"Child 3 Years","sku_suffix":"KID3Y","age":"3","weight":"11-15 kg","height":"90-100 cm","chest_cm":62,"hip_cm":66,"waist_cm":62,"length_cm":54,"skirt_cm":54,"pant_cm":0},
  {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"110/6码","picker_label":"Child 4 Years","sku_suffix":"KID4Y","age":"4","weight":"15-19 kg","height":"100-110 cm","chest_cm":66,"hip_cm":70,"waist_cm":66,"length_cm":58,"skirt_cm":58,"pant_cm":0},
  {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"120/8码","picker_label":"Child 5 Years","sku_suffix":"KID5Y","age":"5","weight":"19-22.5 kg","height":"110-120 cm","chest_cm":70,"hip_cm":74,"waist_cm":70,"length_cm":62,"skirt_cm":62,"pant_cm":0},
  {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"130/10码","picker_label":"Child 6-7 Years","sku_suffix":"KID67Y","age":"6-7","weight":"22.5-27.5 kg","height":"120-130 cm","chest_cm":74,"hip_cm":78,"waist_cm":74,"length_cm":66,"skirt_cm":66,"pant_cm":0},
  {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"140/12码","picker_label":"Child 8 Years","sku_suffix":"KID8Y","age":"8","weight":"27.5-32.5 kg","height":"130-140 cm","chest_cm":78,"hip_cm":82,"waist_cm":78,"length_cm":70,"skirt_cm":70,"pant_cm":0},
  {"audience":"child","role":"Girl Dress","garment":"Dress","vendor_label":"150/14码","picker_label":"Child 9-10 Years","sku_suffix":"KID910Y","age":"9-10","weight":"32.5-40 kg","height":"140-150 cm","chest_cm":82,"hip_cm":86,"waist_cm":82,"length_cm":74,"skirt_cm":74,"pant_cm":0},
  {"audience":"mother","role":"Mother Dress","garment":"Dress","vendor_label":"S/160","picker_label":"Mother S","sku_suffix":"S","age":"—","weight":"42.5-50 kg","height":"155-160 cm","chest_cm":82,"hip_cm":88,"waist_cm":80,"length_cm":76,"skirt_cm":76,"pant_cm":0},
  {"audience":"mother","role":"Mother Dress","garment":"Dress","vendor_label":"M/165","picker_label":"Mother M","sku_suffix":"M","age":"—","weight":"50-55 kg","height":"155-160 cm","chest_cm":86,"hip_cm":92,"waist_cm":84,"length_cm":77,"skirt_cm":77,"pant_cm":0},
  {"audience":"mother","role":"Mother Dress","garment":"Dress","vendor_label":"L/170","picker_label":"Mother L","sku_suffix":"L","age":"—","weight":"55-60 kg","height":"155-165 cm","chest_cm":90,"hip_cm":96,"waist_cm":88,"length_cm":78,"skirt_cm":78,"pant_cm":0},
  {"audience":"mother","role":"Mother Dress","garment":"Dress","vendor_label":"XL/175","picker_label":"Mother XL","sku_suffix":"XL","age":"—","weight":"60-65 kg","height":"165-170 cm","chest_cm":94,"hip_cm":100,"waist_cm":92,"length_cm":79,"skirt_cm":79,"pant_cm":0},
  {"audience":"mother","role":"Mother Dress","garment":"Dress","vendor_label":"2XL/180","picker_label":"Mother 2XL","sku_suffix":"2XL","age":"—","weight":"65-70 kg","height":"170-175 cm","chest_cm":98,"hip_cm":104,"waist_cm":96,"length_cm":80,"skirt_cm":80,"pant_cm":0},
  {"audience":"child","role":"Boy Shirt","garment":"Shirt","vendor_label":"90/2码","picker_label":"Child 2 Years","sku_suffix":"KID2Y","age":"2","weight":"7.5-11 kg","height":"80-90 cm","chest_cm":62,"hip_cm":66,"waist_cm":62,"length_cm":38,"shoulder_cm":0,"pant_cm":0},
  {"audience":"child","role":"Boy Shirt","garment":"Shirt","vendor_label":"100/4码","picker_label":"Child 3 Years","sku_suffix":"KID3Y","age":"3","weight":"11-15 kg","height":"90-100 cm","chest_cm":66,"hip_cm":70,"waist_cm":66,"length_cm":41,"shoulder_cm":0,"pant_cm":0},
  {"audience":"child","role":"Boy Shirt","garment":"Shirt","vendor_label":"110/6码","picker_label":"Child 4 Years","sku_suffix":"KID4Y","age":"4","weight":"15-19 kg","height":"100-110 cm","chest_cm":70,"hip_cm":74,"waist_cm":70,"length_cm":44,"shoulder_cm":0,"pant_cm":0},
  {"audience":"child","role":"Boy Shirt","garment":"Shirt","vendor_label":"120/8码","picker_label":"Child 5 Years","sku_suffix":"KID5Y","age":"5","weight":"19-22.5 kg","height":"110-120 cm","chest_cm":74,"hip_cm":78,"waist_cm":74,"length_cm":47,"shoulder_cm":0,"pant_cm":0},
  {"audience":"child","role":"Boy Shirt","garment":"Shirt","vendor_label":"130/10码","picker_label":"Child 6-7 Years","sku_suffix":"KID67Y","age":"6-7","weight":"22.5-27.5 kg","height":"120-130 cm","chest_cm":78,"hip_cm":82,"waist_cm":78,"length_cm":50,"shoulder_cm":0,"pant_cm":0},
  {"audience":"child","role":"Boy Shirt","garment":"Shirt","vendor_label":"140/12码","picker_label":"Child 8 Years","sku_suffix":"KID8Y","age":"8","weight":"27.5-32.5 kg","height":"130-140 cm","chest_cm":82,"hip_cm":86,"waist_cm":82,"length_cm":53,"shoulder_cm":0,"pant_cm":0},
  {"audience":"child","role":"Boy Shirt","garment":"Shirt","vendor_label":"150/14码","picker_label":"Child 9-10 Years","sku_suffix":"KID910Y","age":"9-10","weight":"32.5-40 kg","height":"140-150 cm","chest_cm":86,"hip_cm":90,"waist_cm":86,"length_cm":56,"shoulder_cm":0,"pant_cm":0},
  {"audience":"father","role":"Father Shirt","garment":"Shirt","vendor_label":"S/165","picker_label":"Father S","sku_suffix":"S","age":"—","weight":"40-47.5 kg","height":"155-165 cm","chest_cm":98,"hip_cm":98,"waist_cm":86,"length_cm":66,"shoulder_cm":0,"pant_cm":0},
  {"audience":"father","role":"Father Shirt","garment":"Shirt","vendor_label":"M/165","picker_label":"Father M","sku_suffix":"M","age":"—","weight":"47.5-55 kg","height":"155-165 cm","chest_cm":102,"hip_cm":102,"waist_cm":90,"length_cm":68,"shoulder_cm":0,"pant_cm":0},
  {"audience":"father","role":"Father Shirt","garment":"Shirt","vendor_label":"L/170","picker_label":"Father L","sku_suffix":"L","age":"—","weight":"55-65 kg","height":"165-170 cm","chest_cm":106,"hip_cm":106,"waist_cm":94,"length_cm":70,"shoulder_cm":0,"pant_cm":0},
  {"audience":"father","role":"Father Shirt","garment":"Shirt","vendor_label":"XL/175","picker_label":"Father XL","sku_suffix":"XL","age":"—","weight":"65-75 kg","height":"165-170 cm","chest_cm":110,"hip_cm":110,"waist_cm":98,"length_cm":72,"shoulder_cm":0,"pant_cm":0},
  {"audience":"father","role":"Father Shirt","garment":"Shirt","vendor_label":"2XL/180","picker_label":"Father 2XL","sku_suffix":"2XL","age":"—","weight":"75-85 kg","height":"175-180 cm","chest_cm":114,"hip_cm":114,"waist_cm":102,"length_cm":74,"shoulder_cm":0,"pant_cm":0},
  {"audience":"father","role":"Father Shirt","garment":"Shirt","vendor_label":"3XL/185","picker_label":"Father 3XL","sku_suffix":"3XL","age":"—","weight":"85-95 kg","height":"175-180 cm","chest_cm":118,"hip_cm":118,"waist_cm":106,"length_cm":76,"shoulder_cm":0,"pant_cm":0},
  {"audience":"father","role":"Father Shirt","garment":"Shirt","vendor_label":"4XL/185","picker_label":"Father 4XL","sku_suffix":"4XL","age":"—","weight":"95-105 kg","height":"175-180 cm","chest_cm":122,"hip_cm":122,"waist_cm":110,"length_cm":78,"shoulder_cm":0,"pant_cm":0}
]
JSON

cat > "${WORK}/size_metaobject_map.json" <<'JSON'
[
  {"picker_label":"Child 2 Years","gid":"gid://shopify/Metaobject/129972863073","catalog_label":"2-3 years","source_handle":"citrus-bloom-family-matching-set"},
  {"picker_label":"Child 3 Years","gid":"gid://shopify/Metaobject/129972895841","catalog_label":"3-4 years","source_handle":"citrus-bloom-family-matching-set"},
  {"picker_label":"Child 4 Years","gid":"gid://shopify/Metaobject/129972928609","catalog_label":"4-5 years","source_handle":"citrus-bloom-family-matching-set"},
  {"picker_label":"Child 5 Years","gid":"gid://shopify/Metaobject/129972961377","catalog_label":"5-6 years","source_handle":"citrus-bloom-family-matching-set"},
  {"picker_label":"Child 6-7 Years","gid":"gid://shopify/Metaobject/139840323681","catalog_label":"6-7 years","source_handle":"citrus-bloom-family-matching-set"},
  {"picker_label":"Child 8 Years","gid":"gid://shopify/Metaobject/129973026913","catalog_label":"8","source_handle":"citrus-bloom-family-matching-set"},
  {"picker_label":"Child 9-10 Years","gid":"gid://shopify/Metaobject/129971552353","catalog_label":"10","source_handle":"citrus-bloom-family-matching-set"},
  {"picker_label":"Mother S","gid":"gid://shopify/Metaobject/129975255137","catalog_label":"S","source_handle":"citrus-bloom-family-matching-set"},
  {"picker_label":"Mother M","gid":"gid://shopify/Metaobject/129975222369","catalog_label":"M","source_handle":"citrus-bloom-family-matching-set"},
  {"picker_label":"Mother L","gid":"gid://shopify/Metaobject/129975189601","catalog_label":"L","source_handle":"citrus-bloom-family-matching-set"},
  {"picker_label":"Mother XL","gid":"gid://shopify/Metaobject/129975287905","catalog_label":"XL","source_handle":"citrus-bloom-family-matching-set"},
  {"picker_label":"Mother 2XL","gid":"gid://shopify/Metaobject/129975156833","catalog_label":"2XL","source_handle":"citrus-bloom-family-matching-set"},
  {"picker_label":"Father S","gid":"gid://shopify/Metaobject/129975255137","catalog_label":"S","source_handle":"citrus-bloom-family-matching-set"},
  {"picker_label":"Father M","gid":"gid://shopify/Metaobject/129975222369","catalog_label":"M","source_handle":"citrus-bloom-family-matching-set"},
  {"picker_label":"Father L","gid":"gid://shopify/Metaobject/129975189601","catalog_label":"L","source_handle":"citrus-bloom-family-matching-set"},
  {"picker_label":"Father XL","gid":"gid://shopify/Metaobject/129975287905","catalog_label":"XL","source_handle":"citrus-bloom-family-matching-set"},
  {"picker_label":"Father 2XL","gid":"gid://shopify/Metaobject/129975156833","catalog_label":"2XL","source_handle":"citrus-bloom-family-matching-set"},
  {"picker_label":"Father 3XL","gid":"gid://shopify/Metaobject/139840421985","catalog_label":"3XL","source_handle":"citrus-bloom-family-matching-set"},
  {"picker_label":"Father 4XL","gid":"gid://shopify/Metaobject/139840716897","catalog_label":"4XL","source_handle":"citrus-bloom-family-matching-set"}
]
JSON

cat > "${WORK}/vendor-evidence.json" <<JSON
{
  "title": "Family matching floral strap dress and collared short-sleeve shirt",
  "notes": "Attached image shows girls and mothers in a floral dress, boys and fathers in a matching floral collared shirt. White shorts are styling only and are not in the size chart.",
  "raw_detail_text": "男童尺码 男装尺码 女童裙子 妈妈裙子 shirt dress"
}
JSON

cp "${WORK}/size_chart.json" "$SIZE_CHART_OUT"

python3 - "${WORK}/size_chart.json" "${WORK}/size_metaobject_map.json" "${WORK}/derived.json" "${WORK}/body.html" \
  "$TITLE" "$SEO_TITLE" "$SEO_DESCRIPTION" "$SHORTCODE" "$COLOR_TOKEN" "$COLOR_NAME" "$PRINT_NAME" \
  "$CHILD_PRICE" "$CHILD_COMPARE" "$ADULT_PRICE" "$ADULT_COMPARE" "$VENDOR_URL" "$SEASON" <<'PY'
from decimal import Decimal, ROUND_HALF_UP
import html
import json
import re
import sys
from pathlib import Path

chart_path = Path(sys.argv[1])
size_map_path = Path(sys.argv[2])
derived_path = Path(sys.argv[3])
body_path = Path(sys.argv[4])
title = sys.argv[5]
seo_title = sys.argv[6]
seo_description = sys.argv[7]
shortcode = sys.argv[8]
color_token = sys.argv[9]
color_name = sys.argv[10]
print_name = sys.argv[11]
child_price = sys.argv[12]
child_compare = sys.argv[13]
adult_price = sys.argv[14]
adult_compare = sys.argv[15]
vendor_url = sys.argv[16]
season = sys.argv[17]

chart = json.loads(chart_path.read_text(encoding="utf-8"))
size_map = {row["picker_label"]: row for row in json.loads(size_map_path.read_text(encoding="utf-8"))}

required = [
    "audience", "role", "garment", "vendor_label", "picker_label", "sku_suffix",
    "age", "weight", "height", "chest_cm", "hip_cm", "waist_cm", "length_cm", "pant_cm",
]
role_tokens = {
    "Girl Dress": "GRL",
    "Mother Dress": "MOM",
    "Boy Shirt": "BOY",
    "Father Shirt": "DAD",
}
size_tokens = {
    "Child 2 Years": "KID2Y",
    "Child 3 Years": "KID3Y",
    "Child 4 Years": "KID4Y",
    "Child 5 Years": "KID5Y",
    "Child 6-7 Years": "KID67Y",
    "Child 8 Years": "KID8Y",
    "Child 9-10 Years": "KID910Y",
    "Mother S": "S",
    "Mother M": "M",
    "Mother L": "L",
    "Mother XL": "XL",
    "Mother 2XL": "2XL",
    "Father S": "S",
    "Father M": "M",
    "Father L": "L",
    "Father XL": "XL",
    "Father 2XL": "2XL",
    "Father 3XL": "3XL",
    "Father 4XL": "4XL",
}

def money_half(value: str) -> str:
    return str((Decimal(value) * Decimal("0.50")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))

def format_num(value):
    numeric = Decimal(str(value))
    if numeric == numeric.to_integral_value():
        return str(int(numeric))
    return f"{numeric.normalize():f}"

def cm_in(value):
    numeric = Decimal(str(value or 0))
    if numeric == 0:
        return "&mdash;"
    inches = (numeric / Decimal("2.54")).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
    return f"{format_num(numeric)} cm / {format_num(inches)} in"

def metric_text_to_dual_unit(value, metric_unit, imperial_unit, multiplier):
    text = str(value or "").strip()
    if not text or text in {"—", "-", "--"}:
        return "&mdash;"
    range_match = re.fullmatch(r"(-?\d+(?:\.\d+)?)\s*[-–]\s*(-?\d+(?:\.\d+)?)\s*" + re.escape(metric_unit), text, re.I)
    if range_match:
        low = Decimal(range_match.group(1))
        high = Decimal(range_match.group(2))
        m = Decimal(str(multiplier))
        low_imp = (low * m).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
        high_imp = (high * m).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
        return f"{format_num(low)}-{format_num(high)} {metric_unit} / {format_num(low_imp)}-{format_num(high_imp)} {imperial_unit}"
    single_match = re.fullmatch(r"(-?\d+(?:\.\d+)?)\s*" + re.escape(metric_unit), text, re.I)
    if single_match:
        numeric = Decimal(single_match.group(1))
        imp = (numeric * Decimal(str(multiplier))).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
        return f"{format_num(numeric)} {metric_unit} / {format_num(imp)} {imperial_unit}"
    return html.escape(text)

def kg_lbs(value):
    return metric_text_to_dual_unit(value, "kg", "lbs", Decimal("2.20462"))

def cm_range_in(value):
    return metric_text_to_dual_unit(value, "cm", "in", Decimal("0.3937007874"))

errors = []
seen_pairs = set()
for row in chart:
    missing = [field for field in required if row.get(field) in (None, "")]
    if missing:
        errors.append(f"row {row.get('vendor_label')} missing {', '.join(missing)}")
    if row.get("skirt_cm") in (None, "") and row.get("shoulder_cm") in (None, "") and row.get("sleeve_cm") in (None, ""):
        errors.append(f"row {row.get('vendor_label')} missing skirt_cm/shoulder_cm/sleeve_cm")
    pair = (row["role"], row["picker_label"])
    if pair in seen_pairs:
        errors.append(f"duplicate (role, picker_label) pair: {pair}")
    seen_pairs.add(pair)
    if row["role"] not in role_tokens:
        errors.append(f"unknown role token mapping for {row['role']}")
    if row["picker_label"] not in size_tokens:
        errors.append(f"unknown size token mapping for {row['picker_label']}")
    if row["picker_label"] not in size_map:
        errors.append(f"missing size metaobject mapping for {row['picker_label']}")

if len(title) > 70:
    errors.append(f"title too long: {len(title)}")
if len(seo_title) > 60:
    errors.append(f"seo title too long: {len(seo_title)}")
if len(seo_description) > 155:
    errors.append(f"seo description too long: {len(seo_description)}")
if errors:
    raise SystemExit("PREFLIGHT FAILED:\n- " + "\n- ".join(errors))

size_values = []
seen_sizes = set()
for row in chart:
    if row["picker_label"] not in seen_sizes:
        size_values.append({"name": row["picker_label"]})
        seen_sizes.add(row["picker_label"])

garments = []
for row in chart:
    if row["garment"] not in garments:
        garments.append(row["garment"])
raw_size_labels = [row["picker_label"] for row in chart]
use_type_option = len(garments) > 1 or len(set(raw_size_labels)) != len(raw_size_labels)
option_axes = [
    {"name": "Type", "values": garments},
    {"name": "Size", "values": [value["name"] for value in size_values]},
] if use_type_option else [
    {"name": "Size", "values": [value["name"] for value in size_values]},
    {"name": "Color", "values": [color_name]},
]
product_options = [{"name": axis["name"], "values": [{"name": value} for value in axis["values"]]} for axis in option_axes]

def sku_for(row):
    return f"DLM-{shortcode}-{role_tokens[row['role']]}-{size_tokens[row['picker_label']]}-{color_token}"

variants = []
recap = []
expected_variant_option_pairs = []
for row in chart:
    price = child_price if row["audience"] == "child" else adult_price
    compare = child_compare if row["audience"] == "child" else adult_compare
    sku = sku_for(row)
    option_values = [row["garment"], row["picker_label"]] if use_type_option else [row["picker_label"], color_name]
    variants.append({
        "price": price,
        "compareAtPrice": compare,
        "taxable": True,
        "inventoryPolicy": "DENY",
        "inventoryItem": {
            "sku": sku,
            "cost": money_half(price),
            "tracked": True,
            "requiresShipping": True,
        },
        "optionValues": [
            {"optionName": option_name, "name": option_value}
            for option_name, option_value in zip([axis["name"] for axis in option_axes], option_values)
        ],
    })
    expected_variant_option_pairs.append(option_values)
    recap.append({
        **row,
        "sku": sku,
        "price": price,
        "compare_at_price": compare,
        "cost": money_half(price),
        "shopify_size_gid": size_map[row["picker_label"]]["gid"],
        "catalog_label": size_map[row["picker_label"]]["catalog_label"],
        "option1_value": option_values[0],
        "option2_value": option_values[1],
    })

def size_phrase():
    return "Girls and boys 2Y through 10Y; Mother S-2XL; Father S-4XL"

def li(label, text):
    return f"<li><strong>{label}:</strong> {html.escape(text)}</li>"

def table_row(row):
    second_measure = cm_in(row.get("skirt_cm") or row.get("shoulder_cm") or 0)
    return (
        "<tr>"
        f"<td>{html.escape(row['picker_label'])}</td>"
        f"<td>{html.escape(row['age'])}</td>"
        f"<td>{kg_lbs(row['weight'])}</td>"
        f"<td>{cm_range_in(row['height'])}</td>"
        f"<td>{cm_in(row['chest_cm'])}</td>"
        f"<td>{second_measure}</td>"
        f"<td>{cm_in(row['pant_cm'])}</td>"
        f"<td>{cm_in(row['hip_cm'])}</td>"
        f"<td>{cm_in(row['waist_cm'])}</td>"
        f"<td>{cm_in(row['length_cm'])}</td>"
        "</tr>"
    )

dress_rows = [table_row(row) for row in chart if row["garment"] == "Dress"]
shirt_rows = [table_row(row) for row in chart if row["garment"] == "Shirt"]

body_html = "\n".join([
    "<ul>",
    li("Fabric", "Lightweight woven fabric with an airy warm-weather feel; exact fiber content should be reconfirmed when the vendor page is readable."),
    li("Family story", "A coordinated four-role look for moms, dads, girls, and boys, made for beach photos, vacations, birthdays, and sunny family plans."),
    li("Print", f"{print_name} mixes red, yellow, blue, and green florals over a light ground for a bright resort-ready palette."),
    li("Design details", "Girls and moms wear the floral shoulder-strap dress, while boys and dads wear the matching short-sleeve collared button-front shirt. White shorts are styling only and are not included."),
    li("Care", "Machine wash cold on gentle, line dry, do not bleach, and cool iron inside-out if needed."),
    li("Size range", size_phrase() + "."),
    "</ul>",
    "",
    "<h3>Size Chart - Dress</h3>",
    "<table id=\"size-chart\">",
    "  <thead><tr><th>Size</th><th>Age</th><th>Weight (kg/lbs)</th><th>Height (cm/in)</th><th>Chest/Bust (cm/in)</th><th>Skirt Length (cm/in)</th><th>Pant/Short or &mdash; (cm/in)</th><th>Hip (cm/in)</th><th>Waist (cm/in)</th><th>Garment Length (cm/in)</th></tr></thead>",
    "  <tbody>",
    *dress_rows,
    "  </tbody>",
    "</table>",
    "",
    "<h3>Size Chart - Shirt</h3>",
    "<table id=\"size-chart-shirt\">",
    "  <thead><tr><th>Size</th><th>Age</th><th>Weight (kg/lbs)</th><th>Height (cm/in)</th><th>Chest/Bust (cm/in)</th><th>Shoulder or &mdash; (cm/in)</th><th>Pant/Short or &mdash; (cm/in)</th><th>Hip (cm/in)</th><th>Waist (cm/in)</th><th>Garment Length (cm/in)</th></tr></thead>",
    "  <tbody>",
    *shirt_rows,
    "  </tbody>",
    "</table>",
    "",
    "<p>Sunlit Floral brings a cheerful vacation mood to family matching. Moms and girls get the coordinated floral dress with a breezy, photo-ready shape, while dads and boys wear the same garden print as a collared short-sleeve shirt.</p>",
    "",
    "<p>The mix keeps every role coordinated without forcing everyone into the same silhouette. Pair the shirts with neutral shorts or linen pants, and let the dresses carry the same bright floral story for warm-weather portraits, resort dinners, and easy weekend outings.</p>",
    "",
    "<h3>Key Features:</h3>",
    "<ul>",
    li("Four-role coordination", "One draft covers girl dress, mother dress, boy shirt, and father shirt sizes."),
    li("Sunny floral palette", "Red, yellow, blue, and green florals photograph beautifully against beach, garden, and resort backdrops."),
    li("Dress and shirt model", "The Type option separates the actual purchasable garments so shoppers can choose honest pieces."),
    li("Size-chart backed", "Every variant is backed by a row from the attached vendor chart."),
    li("Styling note", "White shorts shown in the supplied image are styling only and not part of this listing."),
    "</ul>",
    "",
    "<p>Choose the dress and shirt sizes your family needs, then build a coordinated floral look that feels polished, easy, and ready for the next sunny memory.</p>",
])

tags = sorted(dict.fromkeys([
    "Family Matching", "Mommy and Me", "Daddy and Me", "Sets",
    "Summer Family Matching Set", "Matching Family Outfits", "Matching Family Set",
    "Matching Family Dress", "Matching Family Shirt", "Dress & Shirt", "Summer",
    "Beach", "Resort", "Vacation", "Sunlit Floral", "Garden Floral", "Floral",
    "Multicolor", "Red Floral", "Yellow Floral", "Blue Floral", "Green",
    "Shoulder Strap Dress", "Sleeveless Dress", "Short Sleeve Shirt",
    "Button Front Shirt", "Collared Shirt", "Girl Dress", "Mother Dress",
    "Boy Shirt", "Father Shirt", "Four-Role Matching",
    "Child 2 Years", "Child 3 Years", "Child 4 Years", "Child 5 Years",
    "Child 6-7 Years", "Child 8 Years", "Child 9-10 Years",
    "Mother S", "Mother M", "Mother L", "Mother XL", "Mother 2XL",
    "Father S", "Father M", "Father L", "Father XL", "Father 2XL",
    "Father 3XL", "Father 4XL", vendor_url,
]))

derived = {
    "use_type_option": use_type_option,
    "product_options": product_options,
    "option_axes": option_axes,
    "option_names": [axis["name"] for axis in option_axes],
    "size_values": size_values,
    "expected_variant_option_pairs": expected_variant_option_pairs,
    "variants": variants,
    "row_count": len(chart),
    "derived_skus_sorted": sorted(v["inventoryItem"]["sku"] for v in variants),
    "shopify_size_refs": list(dict.fromkeys(size_map[row["picker_label"]]["gid"] for row in chart)),
    "size_phrase": size_phrase(),
    "tags": tags,
    "recap": recap,
}

derived_path.write_text(json.dumps(derived, indent=2), encoding="utf-8")
body_path.write_text(body_html, encoding="utf-8")
PY

BODY_HTML="$(cat "${WORK}/body.html")"
cp "${WORK}/body.html" "$BODY_HTML_OUT"

ROW_COUNT="$(jq -r '.row_count' "${WORK}/derived.json")"
PRODUCT_OPTIONS_JSON="$(jq -c '.product_options' "${WORK}/derived.json")"
OPTION_NAMES_JSON="$(jq -c '.option_names' "${WORK}/derived.json")"
VARIANTS_JSON="$(jq -c '.variants' "${WORK}/derived.json")"
DERIVED_SKUS_SORTED="$(jq -r '.derived_skus_sorted[]' "${WORK}/derived.json")"
TAGS_JSON="$(jq -c '.tags' "${WORK}/derived.json")"
SHOPIFY_SIZE_REFS_JSON="$(jq -c '.shopify_size_refs' "${WORK}/derived.json")"

python3 ops/scripts/validate_listing_variant_model.py \
  --size-chart "${WORK}/size_chart.json" \
  --derived "${WORK}/derived.json" \
  --vendor-evidence "${WORK}/vendor-evidence.json" \
  --primary-category "$CATEGORY" \
  --tags "$(jq -r '.tags | join(",")' "${WORK}/derived.json")"

TAXONOMY_RESPONSE="$(gql 'query TaxonomyNode($id: ID!) { node(id: $id) { ... on TaxonomyCategory { id fullName } } }' "$(jq -nc --arg id "$TAXONOMY_GID" '{id:$id}')")"
check_graphql_errors "$TAXONOMY_RESPONSE" "taxonomy lookup"
TAXONOMY_FULL_NAME="$(echo "$TAXONOMY_RESPONSE" | jq -r '.data.node.fullName // empty')"
if [[ "$TAXONOMY_FULL_NAME" != "$EXPECTED_TAXONOMY_FULL_NAME" ]]; then
  echo "ERROR: taxonomy ${TAXONOMY_GID} resolved to '${TAXONOMY_FULL_NAME}', expected '${EXPECTED_TAXONOMY_FULL_NAME}'." >&2
  exit 1
fi

AGE_GROUP_GIDS_JSON='["gid://shopify/Metaobject/128116523105","gid://shopify/Metaobject/128116490337"]'
COLOR_PATTERN_GIDS_JSON='["gid://shopify/Metaobject/69622104161","gid://shopify/Metaobject/69639766113","gid://shopify/Metaobject/69963645025","gid://shopify/Metaobject/130231140449","gid://shopify/Metaobject/129971519585"]'
TARGET_GENDER_GIDS_JSON='["gid://shopify/Metaobject/129971617889","gid://shopify/Metaobject/130231107681"]'
CARE_INSTRUCTIONS_GIDS_JSON='["gid://shopify/Metaobject/130283503713"]'

EXISTING_QUERY='query ExistingProduct($handle: String!) {
  productByHandle(handle: $handle) {
    id
    handle
    status
    publishedAt
    options { id name position values optionValues { id name hasVariants } }
    variants(first: 100) {
      nodes {
        id
        sku
        price
        compareAtPrice
        inventoryPolicy
        selectedOptions { name value }
        inventoryItem { tracked requiresShipping unitCost { amount currencyCode } }
      }
    }
    metafields(first: 120, namespace: "shopify") { nodes { namespace key type value } }
  }
}'

refresh_existing_product() {
  EXISTING_RESPONSE="$(gql "$EXISTING_QUERY" "$(jq -nc --arg handle "$HANDLE" '{handle:$handle}')")"
  check_graphql_errors "$EXISTING_RESPONSE" "existing product lookup"
  echo "$EXISTING_RESPONSE" > "${WORK}/existing.json"
  PRODUCT_ID="$(echo "$EXISTING_RESPONSE" | jq -r '.data.productByHandle.id // empty')"
}

refresh_existing_product
CREATE_NEW_PRODUCT="0"

if [[ -n "$PRODUCT_ID" ]]; then
  EXISTING_STATUS="$(echo "$EXISTING_RESPONSE" | jq -r '.data.productByHandle.status // empty')"
  EXISTING_PUBLISHED_AT="$(echo "$EXISTING_RESPONSE" | jq -r '.data.productByHandle.publishedAt // empty')"
  if [[ "$EXISTING_STATUS" != "DRAFT" || -n "$EXISTING_PUBLISHED_AT" ]]; then
    echo "ERROR: existing handle ${HANDLE} is not an unpublished draft; refusing to alter publish state." >&2
    exit 1
  fi
else
  CREATE_NEW_PRODUCT="1"
  PRODUCT_CREATE_MUTATION='mutation ProductCreate($input: ProductInput!) {
    productCreate(input: $input) {
      product { id handle title status }
      userErrors { field message }
    }
  }'

  PRODUCT_CREATE_VARS="$(jq -nc \
    --arg handle "$HANDLE" \
    --arg title "$TITLE" \
    --arg body "$BODY_HTML" \
    --arg vendor "$VENDOR" \
    --arg product_type "$PRODUCT_TYPE" \
    --arg category "$TAXONOMY_GID" \
    --arg seo_title "$SEO_TITLE" \
    --arg seo_description "$SEO_DESCRIPTION" \
    --argjson tags "$TAGS_JSON" \
    --argjson product_options "$PRODUCT_OPTIONS_JSON" '
    {input: {
      handle: $handle,
      title: $title,
      descriptionHtml: $body,
      vendor: $vendor,
      productType: $product_type,
      tags: $tags,
      status: "DRAFT",
      category: $category,
      seo: {title: $seo_title, description: $seo_description},
      productOptions: $product_options
    }}')"

  PRODUCT_CREATE_RESPONSE="$(gql "$PRODUCT_CREATE_MUTATION" "$PRODUCT_CREATE_VARS")"
  check_graphql_errors "$PRODUCT_CREATE_RESPONSE" "productCreate"
  check_user_errors "$PRODUCT_CREATE_RESPONSE" '.data.productCreate.userErrors' "productCreate"
  PRODUCT_ID="$(echo "$PRODUCT_CREATE_RESPONSE" | jq -r '.data.productCreate.product.id // empty')"
fi

if [[ -z "$PRODUCT_ID" ]]; then
  echo "ERROR: product id missing after create flow." >&2
  exit 1
fi

PRODUCT_UPDATE_MUTATION='mutation ProductUpdate($product: ProductUpdateInput!) {
  productUpdate(product: $product) {
    product { id handle title status }
    userErrors { field message }
  }
}'

PRODUCT_UPDATE_VARS="$(jq -nc \
  --arg id "$PRODUCT_ID" \
  --arg handle "$HANDLE" \
  --arg title "$TITLE" \
  --arg body "$BODY_HTML" \
  --arg vendor "$VENDOR" \
  --arg product_type "$PRODUCT_TYPE" \
  --arg category "$TAXONOMY_GID" \
  --arg seo_title "$SEO_TITLE" \
  --arg seo_description "$SEO_DESCRIPTION" \
  --argjson tags "$TAGS_JSON" '
  {product: {
    id: $id,
    handle: $handle,
    title: $title,
    descriptionHtml: $body,
    vendor: $vendor,
    productType: $product_type,
    tags: $tags,
    status: "DRAFT",
    category: $category,
    seo: {title: $seo_title, description: $seo_description}
  }}')"

PRODUCT_UPDATE_RESPONSE="$(gql "$PRODUCT_UPDATE_MUTATION" "$PRODUCT_UPDATE_VARS")"
check_graphql_errors "$PRODUCT_UPDATE_RESPONSE" "productUpdate"
check_user_errors "$PRODUCT_UPDATE_RESPONSE" '.data.productUpdate.userErrors' "productUpdate"

SHOULD_CREATE_VARIANTS="0"
SHOULD_UPDATE_VARIANTS="0"
if [[ "$CREATE_NEW_PRODUCT" == "1" ]]; then
  SHOULD_CREATE_VARIANTS="1"
else
  EXISTING_VARIANT_COUNT="$(echo "$EXISTING_RESPONSE" | jq '.data.productByHandle.variants.nodes | length')"
  EXISTING_SKUS_SORTED="$(echo "$EXISTING_RESPONSE" | jq -r '.data.productByHandle.variants.nodes[].sku // empty' | sed '/^$/d' | sort)"
  if [[ "$EXISTING_VARIANT_COUNT" -eq 0 ]]; then
    SHOULD_CREATE_VARIANTS="1"
  elif [[ "$EXISTING_VARIANT_COUNT" -eq 1 && -z "$EXISTING_SKUS_SORTED" ]]; then
    SHOULD_CREATE_VARIANTS="1"
  elif [[ "$EXISTING_VARIANT_COUNT" -eq "$ROW_COUNT" && "$EXISTING_SKUS_SORTED" == "$DERIVED_SKUS_SORTED" ]]; then
    SHOULD_UPDATE_VARIANTS="1"
  else
    echo "ERROR: existing draft handle ${HANDLE} has unexpected variants; refusing to create duplicates." >&2
    exit 1
  fi
fi

if [[ "$SHOULD_CREATE_VARIANTS" == "1" ]]; then
  BULK_CREATE_MUTATION='mutation ProductVariantsBulkCreate($productId: ID!, $variants: [ProductVariantsBulkInput!]!, $strategy: ProductVariantsBulkCreateStrategy) {
    productVariantsBulkCreate(productId: $productId, variants: $variants, strategy: $strategy) {
      productVariants { id sku title price compareAtPrice inventoryPolicy inventoryItem { tracked requiresShipping unitCost { amount currencyCode } } }
      userErrors { field message }
    }
  }'
  BULK_CREATE_VARS="$(jq -nc --arg product_id "$PRODUCT_ID" --argjson variants "$VARIANTS_JSON" '{productId: $product_id, variants: $variants, strategy: "REMOVE_STANDALONE_VARIANT"}')"
  BULK_CREATE_RESPONSE="$(gql "$BULK_CREATE_MUTATION" "$BULK_CREATE_VARS")"
  check_graphql_errors "$BULK_CREATE_RESPONSE" "productVariantsBulkCreate"
  check_user_errors "$BULK_CREATE_RESPONSE" '.data.productVariantsBulkCreate.userErrors' "productVariantsBulkCreate"
fi

if [[ "$SHOULD_UPDATE_VARIANTS" == "1" ]]; then
  VARIANTS_UPDATE_JSON="$(python3 - "${WORK}/derived.json" "${WORK}/existing.json" <<'PY'
import json
import sys

derived = json.load(open(sys.argv[1]))
existing = json.load(open(sys.argv[2]))["data"]["productByHandle"]["variants"]["nodes"]
spec_by_sku = {row["inventoryItem"]["sku"]: row for row in derived["variants"]}
updates = []
for node in existing:
    spec = spec_by_sku[node["sku"]]
    updates.append({
        "id": node["id"],
        "price": spec["price"],
        "compareAtPrice": spec["compareAtPrice"],
        "taxable": True,
        "inventoryPolicy": "DENY",
        "inventoryItem": spec["inventoryItem"],
        "optionValues": spec["optionValues"],
    })
print(json.dumps(updates))
PY
)"
  BULK_UPDATE_MUTATION='mutation ProductVariantsBulkUpdate($productId: ID!, $variants: [ProductVariantsBulkInput!]!) {
    productVariantsBulkUpdate(productId: $productId, variants: $variants) {
      productVariants { id sku title price compareAtPrice inventoryPolicy inventoryItem { tracked requiresShipping unitCost { amount currencyCode } } }
      userErrors { field message }
    }
  }'
  BULK_UPDATE_VARS="$(jq -nc --arg product_id "$PRODUCT_ID" --argjson variants "$VARIANTS_UPDATE_JSON" '{productId: $product_id, variants: $variants}')"
  BULK_UPDATE_RESPONSE="$(gql "$BULK_UPDATE_MUTATION" "$BULK_UPDATE_VARS")"
  check_graphql_errors "$BULK_UPDATE_RESPONSE" "productVariantsBulkUpdate"
  check_user_errors "$BULK_UPDATE_RESPONSE" '.data.productVariantsBulkUpdate.userErrors' "productVariantsBulkUpdate"
fi

METAFIELDS_SET_MUTATION='mutation MetafieldsSet($metafields: [MetafieldsSetInput!]!) {
  metafieldsSet(metafields: $metafields) {
    metafields { namespace key type value }
    userErrors { field message }
  }
}'

METAFIELDS_JSON="$(jq -nc \
  --arg pid "$PRODUCT_ID" \
  --arg age_group_value "$(echo "$AGE_GROUP_GIDS_JSON" | jq -c .)" \
  --arg care_instructions_value "$(echo "$CARE_INSTRUCTIONS_GIDS_JSON" | jq -c .)" \
  --arg color_value "$(echo "$COLOR_PATTERN_GIDS_JSON" | jq -c .)" \
  --arg target_gender_value "$(echo "$TARGET_GENDER_GIDS_JSON" | jq -c .)" \
  --arg size_value "$(echo "$SHOPIFY_SIZE_REFS_JSON" | jq -c .)" \
  --arg seo_title "$SEO_TITLE" \
  --arg seo_description "$SEO_DESCRIPTION" \
  --arg merch_subcategory "$MERCH_SUBCATEGORY" \
  --arg merch_subcategory2 "$MERCH_SUBCATEGORY2" \
  --arg merch_style "$MERCH_STYLE" \
  --arg merch_type "$MERCH_TYPE" '
  [
    {ownerId: $pid, namespace: "custom", key: "category1", type: "single_line_text_field", value: "Family Matching"},
    {ownerId: $pid, namespace: "custom", key: "subcategory", type: "single_line_text_field", value: $merch_subcategory},
    {ownerId: $pid, namespace: "custom", key: "subcategory2", type: "single_line_text_field", value: $merch_subcategory2},
    {ownerId: $pid, namespace: "custom", key: "pattern", type: "single_line_text_field", value: "Sunlit Floral"},
    {ownerId: $pid, namespace: "custom", key: "style", type: "single_line_text_field", value: $merch_style},
    {ownerId: $pid, namespace: "custom", key: "type", type: "single_line_text_field", value: $merch_type},
    {ownerId: $pid, namespace: "mm-google-shopping", key: "custom_product", type: "boolean", value: "false"},
    {ownerId: $pid, namespace: "mm-google-shopping", key: "gender", type: "single_line_text_field", value: "unisex"},
    {ownerId: $pid, namespace: "mm-google-shopping", key: "age_group", type: "single_line_text_field", value: "adult"},
    {ownerId: $pid, namespace: "mm-google-shopping", key: "condition", type: "single_line_text_field", value: "new"},
    {ownerId: $pid, namespace: "mm-google-shopping", key: "custom_label_0", type: "single_line_text_field", value: "Family Matching"},
    {ownerId: $pid, namespace: "mm-google-shopping", key: "custom_label_1", type: "single_line_text_field", value: "Sunlit Floral"},
    {ownerId: $pid, namespace: "mm-google-shopping", key: "custom_label_2", type: "single_line_text_field", value: "Summer"},
    {ownerId: $pid, namespace: "mm-google-shopping", key: "custom_label_3", type: "single_line_text_field", value: "Dress & Shirt"},
    {ownerId: $pid, namespace: "mm-google-shopping", key: "custom_label_4", type: "single_line_text_field", value: "Four-Role Matching"},
    {ownerId: $pid, namespace: "shopify", key: "age-group", type: "list.metaobject_reference", value: $age_group_value},
    {ownerId: $pid, namespace: "shopify", key: "care-instructions", type: "list.metaobject_reference", value: $care_instructions_value},
    {ownerId: $pid, namespace: "shopify", key: "color-pattern", type: "list.metaobject_reference", value: $color_value},
    {ownerId: $pid, namespace: "shopify", key: "size", type: "list.metaobject_reference", value: $size_value},
    {ownerId: $pid, namespace: "shopify", key: "target-gender", type: "list.metaobject_reference", value: $target_gender_value},
    {ownerId: $pid, namespace: "global", key: "title_tag", type: "single_line_text_field", value: $seo_title},
    {ownerId: $pid, namespace: "global", key: "description_tag", type: "single_line_text_field", value: $seo_description}
  ]')"

while IFS= read -r metafields_batch; do
  METAFIELDS_SET_RESPONSE="$(gql "$METAFIELDS_SET_MUTATION" "$(jq -nc --argjson metafields "$metafields_batch" '{metafields: $metafields}')")"
  check_graphql_errors "$METAFIELDS_SET_RESPONSE" "metafieldsSet"
  check_user_errors "$METAFIELDS_SET_RESPONSE" '.data.metafieldsSet.userErrors' "metafieldsSet"
done < <(echo "$METAFIELDS_JSON" | jq -c '. as $all | [range(0; length; 25) as $i | $all[$i:($i + 25)]][]')

MEDIA_QUERY='query ProductMedia($id: ID!) {
  product(id: $id) {
    media(first: 50) {
      nodes { ... on MediaImage { id alt image { url } } }
    }
  }
}'
MEDIA_RESPONSE="$(gql "$MEDIA_QUERY" "$(jq -nc --arg id "$PRODUCT_ID" '{id:$id}')")"
check_graphql_errors "$MEDIA_RESPONSE" "product media lookup"
EXISTING_MEDIA_ALTS="$(echo "$MEDIA_RESPONSE" | jq -r '.data.product.media.nodes[].alt // empty')"

MEDIA_FILES=()
while IFS= read -r -d '' media_file; do
  MEDIA_FILES+=("$media_file")
done < <(find "$UPLOAD_DIR" -maxdepth 1 -type f \( -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.png' -o -iname '*.webp' \) -print0 | sort -z)

if ((${#MEDIA_FILES[@]})); then
  for image_path in "${MEDIA_FILES[@]}"; do
    image_name="$(basename "$image_path")"
    if [[ "$image_name" == 01-* ]]; then
      alt_text="Sunlit Floral family matching dress and shirt set for moms, dads, girls, and boys."
    else
      alt_text="Sunlit Floral family matching outfit detail."
    fi
    if grep -Fxq "$alt_text" <<< "$EXISTING_MEDIA_ALTS"; then
      continue
    fi
    mime_type="$(python3 - "$image_path" <<'PY'
import mimetypes
import sys
print(mimetypes.guess_type(sys.argv[1])[0] or "application/octet-stream")
PY
)"
    STAGED_UPLOAD_RESPONSE="$(gql 'mutation StagedUploadsCreate($input: [StagedUploadInput!]!) { stagedUploadsCreate(input: $input) { stagedTargets { url resourceUrl parameters { name value } } userErrors { field message } } }' "$(jq -nc --arg filename "$image_name" --arg mime_type "$mime_type" '{input: [{filename: $filename, mimeType: $mime_type, resource: "IMAGE", httpMethod: "POST"}]}')")"
    check_graphql_errors "$STAGED_UPLOAD_RESPONSE" "stagedUploadsCreate"
    check_user_errors "$STAGED_UPLOAD_RESPONSE" '.data.stagedUploadsCreate.userErrors' "stagedUploadsCreate"
    upload_url="$(echo "$STAGED_UPLOAD_RESPONSE" | jq -r '.data.stagedUploadsCreate.stagedTargets[0].url')"
    resource_url="$(echo "$STAGED_UPLOAD_RESPONSE" | jq -r '.data.stagedUploadsCreate.stagedTargets[0].resourceUrl')"
    form_args=()
    while IFS= read -r param; do
      form_args+=(-F "$param")
    done < <(echo "$STAGED_UPLOAD_RESPONSE" | jq -r '.data.stagedUploadsCreate.stagedTargets[0].parameters[] | "\(.name)=\(.value)"')
    form_args+=(-F "file=@${image_path}")
    curl -sS -X POST "$upload_url" "${form_args[@]}" > /dev/null
    PRODUCT_CREATE_MEDIA_RESPONSE="$(gql 'mutation ProductCreateMedia($productId: ID!, $media: [CreateMediaInput!]!) { productCreateMedia(productId: $productId, media: $media) { media { ... on MediaImage { id alt } } userErrors { field message } } }' "$(jq -nc --arg product_id "$PRODUCT_ID" --arg original_source "$resource_url" --arg alt_text "$alt_text" '{productId: $product_id, media: [{originalSource: $original_source, mediaContentType: "IMAGE", alt: $alt_text}]}')")"
    check_graphql_errors "$PRODUCT_CREATE_MEDIA_RESPONSE" "productCreateMedia"
    check_user_errors "$PRODUCT_CREATE_MEDIA_RESPONSE" '.data.productCreateMedia.userErrors' "productCreateMedia"
  done
fi

sleep 2

VERIFY_QUERY='query VerifyProduct($id: ID!) {
  product(id: $id) {
    id title handle status publishedAt onlineStoreUrl descriptionHtml tags
    seo { title description }
    category { id fullName }
    options { id name position values optionValues { id name hasVariants } }
    variants(first: 100) {
      nodes {
        id sku title price compareAtPrice inventoryPolicy taxable
        selectedOptions { name value }
        inventoryItem { tracked requiresShipping unitCost { amount currencyCode } }
      }
    }
    media(first: 50) { nodes { ... on MediaImage { alt image { url } } } }
    collections(first: 50) { nodes { title handle } }
    metafields(first: 80) { nodes { namespace key type value } }
    resourcePublicationsV2(first: 20) { nodes { isPublished publishDate publication { id name } } }
  }
}'
VERIFY_RESPONSE="$(gql "$VERIFY_QUERY" "$(jq -nc --arg id "$PRODUCT_ID" '{id:$id}')")"
check_graphql_errors "$VERIFY_RESPONSE" "verify query"
echo "$VERIFY_RESPONSE" > "$VERIFY_JSON_OUT"

python3 - "$VERIFY_JSON_OUT" "${WORK}/derived.json" "${WORK}/size_chart.json" "${WORK}/size_metaobject_map.json" \
  "$LISTING_MD" "$CSV_OUT" "$CSV_HEADER_SOURCE" "$HANDLE" "$TITLE" "$SEO_TITLE" "$SEO_DESCRIPTION" \
  "$PRICE_NEIGHBOR_HANDLE" "$SIZE_NEIGHBOR_HANDLE" "$CHILD_PRICE" "$CHILD_COMPARE" "$ADULT_PRICE" "$ADULT_COMPARE" \
  "$VENDOR_URL" "$SCRIPT_PATH" "$SIZE_CHART_OUT" "$BODY_HTML_OUT" "$UPLOAD_DIR" "$PRODUCT_ID" \
  "$EXPECTED_TAXONOMY_FULL_NAME" "$MERCH_SUBCATEGORY" "$MERCH_SUBCATEGORY2" "$MERCH_STYLE" "$MERCH_TYPE" "$MERCH_COLLECTION_TAG" <<'PY'
import csv
import json
import re
import sys
from decimal import Decimal
from pathlib import Path

verify_path = Path(sys.argv[1])
derived_path = Path(sys.argv[2])
chart_path = Path(sys.argv[3])
size_map_path = Path(sys.argv[4])
listing_md_path = Path(sys.argv[5])
csv_out_path = Path(sys.argv[6])
csv_header_source = Path(sys.argv[7])
handle = sys.argv[8]
title = sys.argv[9]
seo_title = sys.argv[10]
seo_description = sys.argv[11]
price_neighbor_handle = sys.argv[12]
size_neighbor_handle = sys.argv[13]
child_price = sys.argv[14]
child_compare = sys.argv[15]
adult_price = sys.argv[16]
adult_compare = sys.argv[17]
vendor_url = sys.argv[18]
script_path = sys.argv[19]
size_chart_out = sys.argv[20]
body_html_out = sys.argv[21]
upload_dir = sys.argv[22]
product_gid = sys.argv[23]
expected_taxonomy_full_name = sys.argv[24]
merch_subcategory = sys.argv[25]
merch_subcategory2 = sys.argv[26]
merch_style = sys.argv[27]
merch_type = sys.argv[28]
merch_collection_tag = sys.argv[29]

verify = json.loads(verify_path.read_text(encoding="utf-8"))
derived = json.loads(derived_path.read_text(encoding="utf-8"))
chart = json.loads(chart_path.read_text(encoding="utf-8"))
size_map = {row["picker_label"]: row for row in json.loads(size_map_path.read_text(encoding="utf-8"))}
product = verify["data"]["product"]
variants = product["variants"]["nodes"]
metafields = product["metafields"]["nodes"]
collections = product["collections"]["nodes"]
publications = product["resourcePublicationsV2"]["nodes"]

spec_by_sku = {row["sku"]: row for row in derived["recap"]}
live_skus_sorted = sorted(v["sku"] for v in variants)
derived_skus_sorted = derived["derived_skus_sorted"]
option_names = derived["option_names"]
option_axes = derived["option_axes"]
product_options = product["options"]
live_option_names = [option["name"] for option in product_options]
expected_option_pairs = {tuple(pair) for pair in derived["expected_variant_option_pairs"]}
live_option_pairs = set()
for variant in variants:
    option_map = {opt["name"]: opt["value"] for opt in variant["selectedOptions"]}
    live_option_pairs.add(tuple(option_map.get(name) for name in option_names))

html_body = product["descriptionHtml"]
table_blocks = re.findall(r"<table[^>]*>(.*?)</table>", html_body, re.S)
table_header_counts = [len(re.findall(r"<th>", block)) for block in table_blocks]
tbody_rows = []
for tbody_html in re.findall(r"<tbody>(.*?)</tbody>", html_body, re.S):
    tbody_rows.extend(re.findall(r"<tr>(.*?)</tr>", tbody_html, re.S))
first_cells = []
for row_html in tbody_rows:
    cell = re.search(r"<td>(.*?)</td>", row_html, re.S)
    first_cells.append(re.sub(r"<.*?>", "", cell.group(1)).strip() if cell else "")
expected_first_cells = [row["picker_label"] for row in chart]
published_ids = [node["publication"]["id"] for node in publications if node["isPublished"]]
metafield_keys = {(node["namespace"], node["key"]) for node in metafields}

checks = [
    ("Title <= 70 chars", len(product["title"]) <= 70, str(len(product["title"]))),
    ("SEO title <= 60 chars", len(product["seo"]["title"]) <= 60, str(len(product["seo"]["title"]))),
    ("SEO description <= 155 chars", len(product["seo"]["description"]) <= 155, str(len(product["seo"]["description"]))),
    ("Live variant count matches SIZE_CHART", len(variants) == len(chart), f"{len(variants)} vs {len(chart)}"),
    ("Live SKUs match derived SKUs", live_skus_sorted == derived_skus_sorted, ", ".join(live_skus_sorted)),
    ("Live option axes match derived axes", live_option_names == option_names, " / ".join(live_option_names)),
    ("Live option values match derived values", all(next((option["values"] for option in product_options if option["name"] == axis["name"]), None) == axis["values"] for axis in option_axes), json.dumps({option["name"]: option["values"] for option in product_options}, ensure_ascii=False)),
    (f"Every {' x '.join(option_names)} combination exists", live_option_pairs == expected_option_pairs, str(sorted(live_option_pairs))),
    ("Size table first column matches picker labels", first_cells == expected_first_cells, " | ".join(first_cells)),
    ("Each size table has 10 headers", table_header_counts and all(count == 10 for count in table_header_counts), str(table_header_counts)),
    ("Table row count matches SIZE_CHART", len(tbody_rows) == len(chart), str(len(tbody_rows))),
    ("Waist populated for every row", all(row.get("waist_cm") not in (None, "", 0) for row in chart), "yes"),
    ("Product status is DRAFT", product["status"] == "DRAFT", product["status"]),
    ("publishedAt is null", product["publishedAt"] is None, str(product["publishedAt"])),
    ("No sales-channel publication is live", not published_ids, str(sorted(published_ids))),
    ("Taxonomy category is set", product["category"]["id"] == "gid://shopify/TaxonomyCategory/aa-1-11", product["category"]["id"]),
    ("Taxonomy category full name matches expected leaf", product["category"]["fullName"] == expected_taxonomy_full_name, product["category"]["fullName"]),
    ("Family-set merchandising tag is present", merch_collection_tag in product["tags"], ", ".join(product["tags"])),
]
required_written = {
    ("custom", "category1"), ("custom", "subcategory"), ("custom", "subcategory2"),
    ("custom", "pattern"), ("custom", "style"), ("custom", "type"),
    ("mm-google-shopping", "custom_product"), ("mm-google-shopping", "gender"),
    ("mm-google-shopping", "age_group"), ("mm-google-shopping", "condition"),
    ("mm-google-shopping", "custom_label_0"), ("mm-google-shopping", "custom_label_1"),
    ("mm-google-shopping", "custom_label_2"), ("mm-google-shopping", "custom_label_3"),
    ("mm-google-shopping", "custom_label_4"), ("shopify", "age-group"),
    ("shopify", "care-instructions"), ("shopify", "color-pattern"),
    ("shopify", "size"), ("shopify", "target-gender"),
    ("global", "title_tag"), ("global", "description_tag"),
}
checks.append(("Applicable metafields are written", required_written.issubset(metafield_keys), str(sorted(required_written - metafield_keys))))

price_rows = []
price_drift = False
for variant in variants:
    spec = spec_by_sku[variant["sku"]]
    unit_cost = ((variant.get("inventoryItem") or {}).get("unitCost") or {}).get("amount")
    price_ok = variant["price"] == spec["price"]
    cmp_ok = variant["compareAtPrice"] == spec["compare_at_price"]
    cost_ok = unit_cost is not None and Decimal(unit_cost) == Decimal(spec["cost"])
    tracked_ok = variant["inventoryItem"]["tracked"] and variant["inventoryItem"]["requiresShipping"]
    deny_ok = variant["inventoryPolicy"] == "DENY"
    taxable_ok = variant["taxable"] is True
    ok = price_ok and cmp_ok and cost_ok and tracked_ok and deny_ok and taxable_ok
    price_drift = price_drift or not ok
    price_rows.append({
        "sku": variant["sku"],
        "live_price": variant["price"],
        "live_compare": variant["compareAtPrice"],
        "live_cost": f"{Decimal(unit_cost):.2f}" if unit_cost is not None else "",
        "spec_price": spec["price"],
        "spec_compare": spec["compare_at_price"],
        "spec_cost": spec["cost"],
        "match": "yes" if ok else "no",
    })

skipped_metafields = {
    "shopify.clothing-features": "No current store catalog value honestly describes this lightweight summer family set.",
    "shopify.fabric": "The direct 1688 page was CAPTCHA-blocked and the attached chart/image do not confirm one exact fiber.",
    "shopify.dress-occasion": "The honest Shopify taxonomy is Outfit Sets, not Dresses.",
    "shopify.dress-style": "The product mixes dresses and shirts under Outfit Sets.",
    "shopify.fit": "No reliable writable standard Shopify metafield definition is available for this mixed outfit-set product.",
    "shopify.neckline": "The product-level neckline would be misleading across both dresses and collared shirts.",
    "shopify.pants-length-type": "Shorts are styling only and not included.",
    "shopify.skirt-dress-length-type": "The listing mixes dresses and shirts, so a dress-only length field would overstate scope.",
    "shopify.sleeve-length-type": "The listing mixes sleeveless dresses and short-sleeve shirts.",
    "shopify.top-length-type": "No single product-level top length is honest across dresses and shirts.",
    "shopify.waist-rise": "No pants/shorts garment is sold in this listing.",
}
written_metafields = [node for node in metafields if node["namespace"] in {"custom", "mm-google-shopping", "shopify", "global"}]

with csv_header_source.open(newline="", encoding="utf-8") as fh:
    header = next(csv.reader(fh))

csv_rows = []
for recap in derived["recap"]:
    row = {field: "" for field in header}
    def put(field, value):
        if field in row:
            row[field] = value
    put("Handle", handle)
    put("Title", title)
    put("Body (HTML)", product["descriptionHtml"])
    put("Vendor", "dresslikemommy.com")
    put("Product Category", "Apparel & Accessories > Clothing > Outfit Sets")
    put("Type", "Matching Family Sets")
    put("Tags", ", ".join(product["tags"]))
    put("Published", "FALSE")
    put("Option1 Name", option_names[0])
    put("Option1 Value", recap["option1_value"])
    put("Option2 Name", option_names[1])
    put("Option2 Value", recap["option2_value"])
    put("Variant SKU", recap["sku"])
    put("Variant Grams", "0")
    put("Variant Inventory Tracker", "shopify")
    put("Variant Inventory Policy", "deny")
    put("Variant Fulfillment Service", "manual")
    put("Variant Price", recap["price"])
    put("Variant Compare At Price", recap["compare_at_price"])
    put("Variant Requires Shipping", "TRUE")
    put("Variant Taxable", "TRUE")
    put("Cost per item", recap["cost"])
    put("SEO Title", seo_title)
    put("SEO Description", seo_description)
    put("Google Shopping / Gender", "unisex")
    put("Google Shopping / Age Group", "adult")
    put("Google Shopping / Condition", "new")
    put("Google Shopping / Custom Product", "FALSE")
    put("Google Shopping / Custom Label 0", "Family Matching")
    put("Google Shopping / Custom Label 1", "Sunlit Floral")
    put("Google Shopping / Custom Label 2", "Summer")
    put("Google Shopping / Custom Label 3", "Dress & Shirt")
    put("Google Shopping / Custom Label 4", "Four-Role Matching")
    put("Category1 (product.metafields.custom.category1)", "Family Matching")
    put("Pattern (product.metafields.custom.pattern)", "Sunlit Floral")
    put("Style (product.metafields.custom.style)", merch_style)
    put("SubCategory (product.metafields.custom.subcategory)", merch_subcategory)
    put("SubCategory2 (product.metafields.custom.subcategory2)", merch_subcategory2)
    put("Type (product.metafields.custom.type)", merch_type)
    put("Google: Custom Product (product.metafields.mm-google-shopping.custom_product)", "false")
    put("Age group (product.metafields.shopify.age-group)", "kids, adults")
    put("Color (product.metafields.shopify.color-pattern)", "Blue, Yellow, Pink, Green, Floral")
    put("Size (product.metafields.shopify.size)", ", ".join(x["name"] for x in derived["size_values"]))
    put("Target Gender (product.metafields.shopify.target-gender)", "Female, Male")
    put("Status", "draft")
    csv_rows.append(row)

with csv_out_path.open("w", newline="", encoding="utf-8") as fh:
    writer = csv.DictWriter(fh, fieldnames=header)
    writer.writeheader()
    writer.writerows(csv_rows)

admin_url = f"https://admin.shopify.com/store/dresslikemommy/products/{product_gid.split('/')[-1]}"
live_url = "not published"
lines = []
lines.append(f"# {title}")
lines.append("")
lines.append("## Links")
lines.append(f"- **Admin:** {admin_url}")
lines.append(f"- **Live:** {live_url}")
lines.append(f"- **Vendor:** {vendor_url}")
lines.append(f"- **Product GID:** `{product_gid}`")
lines.append(f"- **Handle:** `{handle}`")
lines.append("")
lines.append("## Inputs (resolved)")
lines.append("| Field | Value |")
lines.append("|---|---|")
lines.append(f"| VENDOR_URL | {vendor_url} |")
lines.append("| SIZE_CHART_SOURCE | attached image |")
lines.append("| LISTING_MODE | Family Matching |")
lines.append("| PRIMARY_CATEGORY | auto -> FamilySet (Shopify taxonomy: Outfit Sets) |")
lines.append("| DESIGNS_TO_LIST | Dress, Shirt |")
lines.append("| EXCLUDE_ITEMS | none; white shorts in the product image are styling only and excluded because no shorts rows exist in the size chart |")
lines.append("| SHORTCODE | auto -> `SNFL` |")
lines.append("| COLOR_TOKEN | auto -> `SUNNY` |")
lines.append("| FORCE_SPEC_PRICES | true |")
lines.append("")
lines.append("## Vendor fetch status")
lines.append("The direct 1688 page returned Alibaba CAPTCHA/punish markup during this run, so the attached size-chart image and supplied product image were used as the authoritative source. The attached chart publishes shirt length/chest rows for boys and fathers and skirt/dress length/chest rows for girls and mothers; hip and waist were derived only where the chart omits them, following the canonical rules.")
lines.append("")
lines.append("## Title & SEO")
lines.append("| | Value | Chars |")
lines.append("|---|---|---|")
lines.append(f"| Product Title | `{product['title']}` | {len(product['title'])} |")
lines.append(f"| SEO Title | `{product['seo']['title']}` | {len(product['seo']['title'])} |")
lines.append(f"| SEO Description | `{product['seo']['description']}` | {len(product['seo']['description'])} |")
lines.append("")
lines.append("## SIZE_CHART recap")
lines.append("| Role | Vendor | Picker | Type | SKU | Price | Cost | shopify.size GID |")
lines.append("|---|---|---|---|---|---|---|---|")
for recap in derived["recap"]:
    lines.append(f"| {recap['role']} | {recap['vendor_label']} | {recap['picker_label']} | {recap['option1_value']} | `{recap['sku']}` | {recap['price']} | {recap['cost']} | `{recap['shopify_size_gid']}` ({recap['catalog_label']}) |")
lines.append("")
lines.append("### Derivations")
lines.append("- Vendor weight guidance was converted from jin to kg, then rendered as kg/lbs in the storefront table.")
lines.append("- Girl dress hip = chest + 4; girl dress waist = chest.")
lines.append("- Mother dress hip = bust + 6; mother dress waist = hip - 8.")
lines.append("- Boy shirt hip = chest + 4; boy shirt waist = chest.")
lines.append("- Father shirt hip = chest; father shirt waist = chest - 12.")
lines.append("- Shirt shoulder and pant/short values are blank because the chart does not publish them and shorts are not included.")
lines.append("")
lines.append("### Vendor -> picker mapping")
lines.extend([
    "- 90 -> Child 2 Years", "- 100 -> Child 3 Years", "- 110 -> Child 4 Years",
    "- 120 -> Child 5 Years", "- 130 -> Child 6-7 Years", "- 140 -> Child 8 Years",
    "- 150 -> Child 9-10 Years", "- Mother S/M/L/XL/2XL mapped directly",
    "- Father S/M/L/XL/2XL/3XL/4XL mapped directly using existing store size metaobjects",
])
lines.append("")
lines.append("## Option axes & variants")
for index, axis in enumerate(option_axes, start=1):
    values = ", ".join(f"`{value}`" for value in axis["values"])
    lines.append(f"- Option {index}: `{axis['name']}` -> {values}")
lines.append(f"- Variants live: **{len(variants)}**")
lines.append("")
lines.append("## Verify pass table")
lines.append("| Check | Result | Detail |")
lines.append("|---|---|---|")
for label, ok, detail in checks:
    lines.append(f"| {label} | {'PASS' if ok else 'FAIL'} | {detail} |")
lines.append("")
lines.append("## Price and cost parity")
lines.append("| SKU | Live Price | Live Cmp | Live Cost | Spec Price | Spec Cmp | Spec Cost | Match |")
lines.append("|---|---|---|---|---|---|---|---|")
for row in price_rows:
    lines.append(f"| {row['sku']} | {row['live_price']} | {row['live_compare']} | {row['live_cost']} | {row['spec_price']} | {row['spec_compare']} | {row['spec_cost']} | {row['match']} |")
lines.append("")
lines.append("## Metafields written")
lines.append("| Namespace.Key | Type | Value |")
lines.append("|---|---|---|")
for node in sorted(written_metafields, key=lambda x: (x["namespace"], x["key"])):
    value = node["value"]
    if len(value) > 90:
        value = value[:87] + "..."
    lines.append(f"| {node['namespace']}.{node['key']} | {node['type']} | `{value}` |")
lines.append("")
lines.append("## Metafields skipped")
lines.append("| Namespace.Key | Reason |")
lines.append("|---|---|")
for key, reason in skipped_metafields.items():
    lines.append(f"| {key} | {reason} |")
lines.append("")
lines.append(f"## Tags written ({len(product['tags'])})")
lines.append("`" + ", ".join(product["tags"]) + "`")
lines.append("")
lines.append("## Publication")
lines.append("- Product remains DRAFT.")
lines.append("- Live URL: not published.")
lines.append("- Sales-channel publication check: no live publication IDs returned.")
lines.append("")
lines.append("## Smart collections")
if collections:
    for collection in collections:
        lines.append(f"- {collection['title']} (`/{collection['handle']}`)")
else:
    lines.append("- No smart collection attachment is expected while the product remains an unpublished draft; Shopify indexing may attach collections later.")
lines.append("")
lines.append("## Manual follow-ups")
lines.append("- Replace or retouch the supplied watermarked product image before publication.")
lines.append("- Confirm exact fabric composition if the vendor page becomes readable later; `shopify.fabric` was intentionally skipped.")
lines.append("- Inventory quantities and grams still need operator stock values.")
lines.append("")
lines.append("## Files saved")
lines.append(f"- `{script_path}`")
lines.append(f"- `{listing_md_path}`")
lines.append(f"- `{csv_out_path}`")
lines.append(f"- `{verify_path}`")
lines.append(f"- `{size_chart_out}`")
lines.append(f"- `{body_html_out}`")
lines.append(f"- `{upload_dir}`")
lines.append("")
lines.append("## Sources")
lines.append(f"- Attached size chart image from operator request.")
lines.append(f"- Attached product image from operator request.")
lines.append(f"- Neighbor pricing: `{price_neighbor_handle}`.")
lines.append(f"- Size metaobject map: `{size_neighbor_handle}` and existing live size metaobjects.")

listing_md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

failed = [label for label, ok, _detail in checks if not ok]
if price_drift:
    failed.append("Price/cost parity")
if failed:
    raise SystemExit("VERIFY FAILED: " + ", ".join(failed))
PY

echo "Admin URL: https://admin.shopify.com/store/dresslikemommy/products/${PRODUCT_ID##*/}"
echo "Live URL: not published"
echo "Listing log: ${LISTING_MD}"
echo "CSV backup: ${CSV_OUT}"
