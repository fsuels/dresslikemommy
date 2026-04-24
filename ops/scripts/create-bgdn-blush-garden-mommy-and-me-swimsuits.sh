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

HANDLE="blush-garden-mommy-and-me-swimsuits"
TITLE="Blush Garden Mommy and Me Swimsuits - Ruffle Swim Dress"
SEO_TITLE="Blush Garden Mommy & Me Swim Dress | Dress Like Mommy"
SEO_DESCRIPTION="Stretch floral mommy-and-me swim dresses for mom + daughter. Sizes 3Y, 4Y, 5Y, 6-7Y, 9-10Y and Mom M-4XL."
PRINT_NAME="Blush Garden"
SHORTCODE="BGDN"
COLOR_TOKEN="BLUSH"
COLOR_NAME="Blush Floral"
LISTING_MODE="Mommy and Me"
CATEGORY="Swimsuits"
PRODUCT_TYPE="Matching Family Swimwear"
CUSTOM_TYPE="Swimsuit"
TAXONOMY_GID="gid://shopify/TaxonomyCategory/aa-1-20-17"
EXPECTED_TAXONOMY_FULL_NAME="Apparel & Accessories > Clothing > Swimwear > Swim Dresses"
SEASON="Summer"
VENDOR_URL="https://detail.1688.com/offer/1039451116404.html"
VENDOR="dresslikemommy.com"
FORCE_SPEC_PRICES="true"
CHILD_PRICE="14.99"
MOTHER_PRICE="16.99"
PRICE_NEIGHBOR_HANDLE="elegant-mother-daughter-matching-one-piece-swimsuit-with-patterned-mesh-skirt-family-beachwear-set"
SIZE_NEIGHBOR_HANDLE="live-shopify-size-metaobject"

SCRIPT_PATH="${ROOT}/ops/scripts/create-bgdn-blush-garden-mommy-and-me-swimsuits.sh"
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

validate_taxonomy_category() {
  local query response typename node_id full_name is_leaf
  query='query TaxonomyCategory($id: ID!) {
    node(id: $id) {
      __typename
      ... on TaxonomyCategory {
        id
        fullName
        isLeaf
      }
    }
  }'
  response="$(gql "$query" "$(jq -nc --arg id "$TAXONOMY_GID" '{id:$id}')")"
  check_graphql_errors "$response" "taxonomy category lookup"
  typename="$(echo "$response" | jq -r '.data.node.__typename // empty')"
  node_id="$(echo "$response" | jq -r '.data.node.id // empty')"
  full_name="$(echo "$response" | jq -r '.data.node.fullName // empty')"
  is_leaf="$(echo "$response" | jq -r '.data.node.isLeaf // empty')"
  if [[ "$typename" != "TaxonomyCategory" || "$node_id" != "$TAXONOMY_GID" || "$full_name" != "$EXPECTED_TAXONOMY_FULL_NAME" || "$is_leaf" != "true" ]]; then
    echo "ERROR: taxonomy guard failed for ${CATEGORY}. Expected ${TAXONOMY_GID} -> ${EXPECTED_TAXONOMY_FULL_NAME}, got ${node_id} -> ${full_name} (type=${typename}, leaf=${is_leaf})." >&2
    exit 1
  fi
}

compare_at_price() {
  python3 - "$1" <<'PY'
import math
import sys

price = float(sys.argv[1])
value = price * 1.15
dollars = math.floor(value)
candidate = dollars + 0.99
if candidate < value:
    candidate = dollars + 1.99
print(f"{candidate:.2f}")
PY
}

CHILD_COMPARE="$(compare_at_price "$CHILD_PRICE")"
MOTHER_COMPARE="$(compare_at_price "$MOTHER_PRICE")"
validate_taxonomy_category

cat > "${WORK}/size_chart.json" <<'JSON'
[
  {"audience":"child","role":"Girl Swimsuit","garment":"Swimsuit","vendor_label":"M","picker_label":"Child 3 Years","sku_suffix":"KID3Y","age":"3","weight":"12.5-15 kg / 27.6-33.1 lbs","height":"100-105 cm / 39.4-41.3 in","chest_display":"-","skirt_display":"-","pant_display":"-","hip_display":"-","waist_display":"-","length_display":"-"},
  {"audience":"child","role":"Girl Swimsuit","garment":"Swimsuit","vendor_label":"L","picker_label":"Child 4 Years","sku_suffix":"KID4Y","age":"4","weight":"15-22.5 kg / 33.1-49.6 lbs","height":"105-115 cm / 41.3-45.3 in","chest_display":"-","skirt_display":"-","pant_display":"-","hip_display":"-","waist_display":"-","length_display":"-"},
  {"audience":"child","role":"Girl Swimsuit","garment":"Swimsuit","vendor_label":"XL","picker_label":"Child 5 Years","sku_suffix":"KID5Y","age":"5","weight":"23-27.5 kg / 50.7-60.6 lbs","height":"116-125 cm / 45.7-49.2 in","chest_display":"-","skirt_display":"-","pant_display":"-","hip_display":"-","waist_display":"-","length_display":"-"},
  {"audience":"child","role":"Girl Swimsuit","garment":"Swimsuit","vendor_label":"2XL(部分款)","picker_label":"Child 6-7 Years","sku_suffix":"KID67Y","age":"6-7","weight":"27.5-32.5 kg / 60.6-71.7 lbs","height":"126-140 cm / 49.6-55.1 in","chest_display":"-","skirt_display":"-","pant_display":"-","hip_display":"-","waist_display":"-","length_display":"-"},
  {"audience":"child","role":"Girl Swimsuit","garment":"Swimsuit","vendor_label":"3XL(部分款)","picker_label":"Child 9-10 Years","sku_suffix":"KID910Y","age":"9-10","weight":"32.5-42.5 kg / 71.7-93.7 lbs","height":"140-155 cm / 55.1-61.0 in","chest_display":"-","skirt_display":"-","pant_display":"-","hip_display":"-","waist_display":"-","length_display":"-"},
  {"audience":"mother","role":"Mother Swimsuit","garment":"Swimsuit","vendor_label":"M","picker_label":"Mother M","sku_suffix":"M","age":"-","weight":"45-49.5 kg / 99.2-109.1 lbs","height":"152-160 cm / 59.8-63.0 in","chest_display":"70ABC-75AB","skirt_display":"-","pant_display":"-","hip_display":"-","waist_display":"Under 66.7 cm / Under 26.2 in","length_display":"-"},
  {"audience":"mother","role":"Mother Swimsuit","garment":"Swimsuit","vendor_label":"L","picker_label":"Mother L","sku_suffix":"L","age":"-","weight":"50-57.5 kg / 110.2-126.8 lbs","height":"160-165 cm / 63.0-65.0 in","chest_display":"75ABC-80AB","skirt_display":"-","pant_display":"-","hip_display":"-","waist_display":"70.0-73.3 cm / 27.6-28.9 in","length_display":"-"},
  {"audience":"mother","role":"Mother Swimsuit","garment":"Swimsuit","vendor_label":"XL","picker_label":"Mother XL","sku_suffix":"XL","age":"-","weight":"58-62.5 kg / 127.9-137.8 lbs","height":"165-170 cm / 65.0-66.9 in","chest_display":"75ABC-80BC","skirt_display":"-","pant_display":"-","hip_display":"-","waist_display":"76.7-80.0 cm / 30.2-31.5 in","length_display":"-"},
  {"audience":"mother","role":"Mother Swimsuit","garment":"Swimsuit","vendor_label":"2XL(部分款)","picker_label":"Mother 2XL","sku_suffix":"2XL","age":"-","weight":"63-72.5 kg / 138.9-159.8 lbs","height":"165-170 cm / 65.0-66.9 in","chest_display":"80ABC-85AB","skirt_display":"-","pant_display":"-","hip_display":"-","waist_display":"83.3-86.7 cm / 32.8-34.1 in","length_display":"-"},
  {"audience":"mother","role":"Mother Swimsuit","garment":"Swimsuit","vendor_label":"3XL(部分款)","picker_label":"Mother 3XL","sku_suffix":"3XL","age":"-","weight":"73-82.5 kg / 160.9-181.9 lbs","height":"165-175 cm / 65.0-68.9 in","chest_display":"85BC-90BC","skirt_display":"-","pant_display":"-","hip_display":"-","waist_display":"90.0-93.3 cm / 35.4-36.7 in","length_display":"-"},
  {"audience":"mother","role":"Mother Swimsuit","garment":"Swimsuit","vendor_label":"4XL(部分款)","picker_label":"Mother 4XL","sku_suffix":"4XL","age":"-","weight":"83-97.5 kg / 183.0-214.9 lbs","height":"165-175 cm / 65.0-68.9 in","chest_display":"85BCD-95ABC","skirt_display":"-","pant_display":"-","hip_display":"-","waist_display":"96.7-103.3 cm / 38.1-40.7 in","length_display":"-"}
]
JSON

cat > "${WORK}/size_metaobject_map.json" <<'JSON'
[
  {"picker_label":"Child 3 Years","gid":"gid://shopify/Metaobject/129972895841","catalog_label":"3-4 years","source_handle":"shopify--size metaobjects"},
  {"picker_label":"Child 4 Years","gid":"gid://shopify/Metaobject/129972928609","catalog_label":"4-5 years","source_handle":"shopify--size metaobjects"},
  {"picker_label":"Child 5 Years","gid":"gid://shopify/Metaobject/129972961377","catalog_label":"5-6 years","source_handle":"shopify--size metaobjects"},
  {"picker_label":"Child 6-7 Years","gid":"gid://shopify/Metaobject/139840323681","catalog_label":"6-7 years","source_handle":"shopify--size metaobjects"},
  {"picker_label":"Child 9-10 Years","gid":"gid://shopify/Metaobject/129971552353","catalog_label":"10","source_handle":"shopify--size metaobjects"},
  {"picker_label":"Mother M","gid":"gid://shopify/Metaobject/129975222369","catalog_label":"M","source_handle":"shopify--size metaobjects"},
  {"picker_label":"Mother L","gid":"gid://shopify/Metaobject/129975189601","catalog_label":"L","source_handle":"shopify--size metaobjects"},
  {"picker_label":"Mother XL","gid":"gid://shopify/Metaobject/129975287905","catalog_label":"XL","source_handle":"shopify--size metaobjects"},
  {"picker_label":"Mother 2XL","gid":"gid://shopify/Metaobject/129975156833","catalog_label":"2XL","source_handle":"shopify--size metaobjects"},
  {"picker_label":"Mother 3XL","gid":"gid://shopify/Metaobject/139840421985","catalog_label":"3XL","source_handle":"shopify--size metaobjects"},
  {"picker_label":"Mother 4XL","gid":"gid://shopify/Metaobject/139840716897","catalog_label":"4XL","source_handle":"shopify--size metaobjects"}
]
JSON

cp "${WORK}/size_chart.json" "$SIZE_CHART_OUT"

python3 - "${WORK}/size_chart.json" "${WORK}/size_metaobject_map.json" "${WORK}/derived.json" "${WORK}/body.html" \
  "$TITLE" "$SEO_TITLE" "$SEO_DESCRIPTION" "$SHORTCODE" "$COLOR_TOKEN" "$COLOR_NAME" "$PRINT_NAME" \
  "$CHILD_PRICE" "$CHILD_COMPARE" "$MOTHER_PRICE" "$MOTHER_COMPARE" "$VENDOR_URL" <<'PY'
import html
import json
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
mother_price = sys.argv[14]
mother_compare = sys.argv[15]
vendor_url = sys.argv[16]

chart = json.loads(chart_path.read_text())
size_map = {row["picker_label"]: row for row in json.loads(size_map_path.read_text())}

required = [
    "audience",
    "role",
    "garment",
    "vendor_label",
    "picker_label",
    "sku_suffix",
    "age",
    "weight",
    "height",
    "chest_display",
    "skirt_display",
    "pant_display",
    "hip_display",
    "waist_display",
    "length_display",
]

role_tokens = {
    "Girl Swimsuit": "GRL",
    "Mother Swimsuit": "MOM",
}
size_tokens = {
    "Child 3 Years": "KID3Y",
    "Child 4 Years": "KID4Y",
    "Child 5 Years": "KID5Y",
    "Child 6-7 Years": "KID67Y",
    "Child 9-10 Years": "KID910Y",
    "Mother M": "M",
    "Mother L": "L",
    "Mother XL": "XL",
    "Mother 2XL": "2XL",
    "Mother 3XL": "3XL",
    "Mother 4XL": "4XL",
}

errors = []
seen_pairs = set()
for row in chart:
    missing = [field for field in required if row.get(field) in (None, "")]
    if missing:
        errors.append(f"row {row.get('vendor_label')} missing {', '.join(missing)}")
    pair = (row.get("role"), row.get("picker_label"))
    if pair in seen_pairs:
        errors.append(f"duplicate (role, picker_label): {pair}")
    seen_pairs.add(pair)
    if row.get("role") not in role_tokens:
        errors.append(f"unknown role {row.get('role')}")
    if row.get("picker_label") not in size_tokens:
        errors.append(f"unknown size token mapping {row.get('picker_label')}")
    if row.get("picker_label") not in size_map:
        errors.append(f"missing size metaobject mapping {row.get('picker_label')}")

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

color_values = [{"name": color_name}]
option_axes = [
    {"name": "Size", "values": [value["name"] for value in size_values]},
    {"name": "Color", "values": [color_name]},
]
product_options = [
    {"name": axis["name"], "values": [{"name": value} for value in axis["values"]]}
    for axis in option_axes
]

def sku_for(row):
    return f"DLM-{shortcode}-{role_tokens[row['role']]}-{size_tokens[row['picker_label']]}-{color_token}"

variants = []
recap = []
expected_variant_option_pairs = []
for row in chart:
    price = child_price if row["audience"] == "child" else mother_price
    compare = child_compare if row["audience"] == "child" else mother_compare
    sku = sku_for(row)
    option_values = [row["picker_label"], color_name]
    variants.append(
        {
            "price": price,
            "compareAtPrice": compare,
            "inventoryPolicy": "DENY",
            "inventoryItem": {
                "sku": sku,
                "tracked": True,
                "requiresShipping": True,
            },
            "optionValues": [
                {"optionName": "Size", "name": row["picker_label"]},
                {"optionName": "Color", "name": color_name},
            ],
        }
    )
    expected_variant_option_pairs.append(option_values)
    recap.append(
        {
            **row,
            "sku": sku,
            "price": price,
            "compare_at_price": compare,
            "shopify_size_gid": size_map[row["picker_label"]]["gid"],
            "catalog_label": size_map[row["picker_label"]]["catalog_label"],
            "option1_value": option_values[0],
            "option2_value": option_values[1],
        }
    )

child_labels = [row["picker_label"] for row in chart if row["audience"] == "child"]
mother_labels = [row["picker_label"] for row in chart if row["audience"] == "mother"]

if child_labels == [
    "Child 3 Years",
    "Child 4 Years",
    "Child 5 Years",
    "Child 6-7 Years",
    "Child 9-10 Years",
] and mother_labels == [
    "Mother M",
    "Mother L",
    "Mother XL",
    "Mother 2XL",
    "Mother 3XL",
    "Mother 4XL",
]:
    size_phrase = "3Y, 4Y, 5Y, 6-7Y, 9-10Y and Mom M-4XL"
else:
    size_phrase = ", ".join(child_labels + mother_labels)

rows_html = []
for row in chart:
    age_display = row["age"] if row["audience"] == "child" else ""
    rows_html.append(
        "<tr>"
        f"<td>{html.escape(row['picker_label'])}</td>"
        f"<td>{html.escape(age_display)}</td>"
        f"<td>{html.escape(row['weight'])}</td>"
        f"<td>{html.escape(row['height'])}</td>"
        f"<td>{html.escape(row['chest_display'])}</td>"
        f"<td>{html.escape(row['skirt_display'])}</td>"
        f"<td>{html.escape(row['pant_display'])}</td>"
        f"<td>{html.escape(row['hip_display'])}</td>"
        f"<td>{html.escape(row['waist_display'])}</td>"
        f"<td>{html.escape(row['length_display'])}</td>"
        "</tr>"
    )

body_html = "\n".join(
    [
        "<ul>",
        "<li><strong>Fabric:</strong> Smooth stretch swim fabric with a softly lined feel that moves easily from splash time to family photos.</li>",
        "<li><strong>Family story:</strong> A coordinated mom-and-daughter swim dress moment made for beach mornings, pool parties, resort afternoons, and vacation photos.</li>",
        f"<li><strong>Print:</strong> \"{html.escape(print_name)}\" layers tiny coral blooms over a soft white base with rose-pink ruffle trim for a sweet summer look.</li>",
        "<li><strong>Design details:</strong> Square ruffle neckline, attached swim bottoms, skirted one-piece silhouette, and a small rosette accent at the hip.</li>",
        "<li><strong>Care:</strong> Rinse after swimming, hand wash cold, line dry in the shade, and avoid bleach or rough poolside surfaces.</li>",
        "<li><strong>Size range:</strong> Girls Child 3 Years to Child 9-10 Years; Mother M to Mother 4XL.</li>",
        "</ul>",
        "",
        "<h3>Size Chart - Swim Dress</h3>",
        "<table id=\"size-chart\">",
        "  <thead>",
        "    <tr>",
        "      <th>Size</th>",
        "      <th>Age</th>",
        "      <th>Weight (kg/lbs)</th>",
        "      <th>Height (cm/in)</th>",
        "      <th>Chest/Bust (bra size)</th>",
        "      <th>Skirt Length (cm/in)</th>",
        "      <th>Pant/Short or - (cm/in)</th>",
        "      <th>Hip (cm/in)</th>",
        "      <th>Waist (cm/in)</th>",
        "      <th>Garment Length (cm/in)</th>",
        "    </tr>",
        "  </thead>",
        "  <tbody>",
        *rows_html,
        "  </tbody>",
        "</table>",
        "",
        "<p>The Blush Garden Mommy and Me Swimsuits bring a soft vacation palette to a pool-ready silhouette. Tiny coral florals, rose-pink ruffle trim, and the skirted one-piece cut make the set feel sweet and photo-ready without losing the practical ease you want for swim days.</p>",
        "",
        "<p>Each suit keeps the coverage-friendly look of a little swim dress while the attached bottoms stay ready for splashing, swimming, and chasing little ones around the pool. It is an easy mom-and-mini match for beach trips, resort mornings, backyard water play, and family travel photos.</p>",
        "",
        "<h3>Key Features:</h3>",
        "<ul>",
        "<li><strong>Skirted swim-dress shape:</strong> One-piece construction keeps the look polished while the flared hem feels playful and easy.</li>",
        "<li><strong>Ruffle neckline detail:</strong> The rose-trimmed ruffle frames the shoulders for a sweet statement in both sizes.</li>",
        "<li><strong>Attached bottoms:</strong> The close-fitting inner brief keeps coverage secure for swimming, wading, and water play.</li>",
        "<li><strong>Soft floral palette:</strong> White ground plus blush-and-coral blooms style beautifully with straw bags, sandals, and beach coverups.</li>",
        "<li><strong>Inclusive mom sizing:</strong> Mother sizes run from M through 4XL alongside the matching girls size set.</li>",
        "</ul>",
        "",
        "<p>Choose the sizes you need and pack a matching swim look that feels ready for beach days, poolside photos, and every sunny family memory.</p>",
    ]
)

tags = list(
    dict.fromkeys(
        [
            "Mommy and Me",
            "Swimsuits",
            "Matching Family Swimwear",
            "Matching Swimwear",
            "Girl Swimsuit",
            "Mother Swimsuit",
            "Swim Dress",
            "Swim Dresses",
            "One-Piece Swimsuit",
            "Ruffle Swim Dress",
            "Summer",
            "Beach",
            "Pool",
            "Vacation",
            "Resort",
            "White",
            "Pink",
            "Blush",
            "Floral",
            "Ruffle",
            "Attached Bottoms",
            "Rose Trim",
            "Mom Size L",
            "Mom Size M",
            "Mom Size XL",
            "Mom Size 2XL",
            "Mom Size 3XL",
            "Mom Size 4XL",
            "Child 2-3yr",
            "Child 4-5yr",
            "Child 6-8yr",
            "Child 9-10yr",
            vendor_url,
        ]
    )
)

derived = {
    "size_values": size_values,
    "color_values": color_values,
    "product_options": product_options,
    "option_axes": option_axes,
    "option_names": [axis["name"] for axis in option_axes],
    "expected_variant_option_pairs": expected_variant_option_pairs,
    "variants": variants,
    "row_count": len(chart),
    "derived_skus_sorted": sorted(v["inventoryItem"]["sku"] for v in variants),
    "shopify_size_refs": [size_map[row["picker_label"]]["gid"] for row in chart],
    "size_phrase": size_phrase,
    "tags": tags,
    "recap": recap,
}

derived_path.write_text(json.dumps(derived, indent=2))
body_path.write_text(body_html)
PY

BODY_HTML="$(cat "${WORK}/body.html")"
cp "${WORK}/body.html" "$BODY_HTML_OUT"

ROW_COUNT="$(jq -r '.row_count' "${WORK}/derived.json")"
PRODUCT_OPTIONS_JSON="$(jq -c '.product_options' "${WORK}/derived.json")"
OPTION_NAMES_JSON="$(jq -c '.option_names' "${WORK}/derived.json")"
OPTION_REORDER_JSON="$(jq -c '[.option_axes[] | {name: .name, values: (.values | map({name: .}))}]' "${WORK}/derived.json")"
VARIANTS_JSON="$(jq -c '.variants' "${WORK}/derived.json")"
DERIVED_SKUS_SORTED="$(jq -r '.derived_skus_sorted[]' "${WORK}/derived.json")"
TAGS_JSON="$(jq -c '.tags' "${WORK}/derived.json")"
SHOPIFY_SIZE_REFS_JSON="$(jq -c '.shopify_size_refs' "${WORK}/derived.json")"

AGE_GROUP_GIDS_JSON='["gid://shopify/Metaobject/129972764769","gid://shopify/Metaobject/128116523105","gid://shopify/Metaobject/128116490337"]'
COLOR_PATTERN_GIDS_JSON='["gid://shopify/Metaobject/69639733345","gid://shopify/Metaobject/69963645025","gid://shopify/Metaobject/129971519585"]'
TARGET_GENDER_GIDS_JSON='["gid://shopify/Metaobject/129971617889"]'

EXISTING_QUERY='query ExistingProduct($handle: String!) {
  productByHandle(handle: $handle) {
    id
    handle
    options {
      id
      name
      position
      values
      optionValues { id name hasVariants }
    }
    variants(first: 100) {
      nodes {
        id
        sku
        price
        compareAtPrice
        inventoryPolicy
        selectedOptions { name value }
        inventoryItem { tracked requiresShipping }
      }
    }
    media(first: 50) {
      nodes {
        ... on MediaImage {
          id
          alt
          image { url }
        }
      }
    }
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

if [[ -z "$PRODUCT_ID" ]]; then
  CREATE_NEW_PRODUCT="1"
  PRODUCT_CREATE_MUTATION='mutation ProductCreate($input: ProductInput!) {
    productCreate(input: $input) {
      product { id handle title }
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
    {
      input: {
        handle: $handle,
        title: $title,
        descriptionHtml: $body,
        vendor: $vendor,
        productType: $product_type,
        tags: $tags,
        status: "ACTIVE",
        category: $category,
        seo: {title: $seo_title, description: $seo_description},
        productOptions: $product_options
      }
    }')"

  PRODUCT_CREATE_RESPONSE="$(gql "$PRODUCT_CREATE_MUTATION" "$PRODUCT_CREATE_VARS")"
  check_graphql_errors "$PRODUCT_CREATE_RESPONSE" "productCreate"
  check_user_errors "$PRODUCT_CREATE_RESPONSE" '.data.productCreate.userErrors' "productCreate"
  PRODUCT_ID="$(echo "$PRODUCT_CREATE_RESPONSE" | jq -r '.data.productCreate.product.id // empty')"
fi

if [[ -z "$PRODUCT_ID" ]]; then
  echo "ERROR: product id missing after create/update flow." >&2
  exit 1
fi

PRODUCT_UPDATE_MUTATION='mutation ProductUpdate($product: ProductUpdateInput!) {
  productUpdate(product: $product) {
    product { id handle title }
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
  {
    product: {
      id: $id,
      handle: $handle,
      title: $title,
      descriptionHtml: $body,
      vendor: $vendor,
      productType: $product_type,
      tags: $tags,
      status: "ACTIVE",
      category: $category,
      seo: {title: $seo_title, description: $seo_description}
    }
  }')"

PRODUCT_UPDATE_RESPONSE="$(gql "$PRODUCT_UPDATE_MUTATION" "$PRODUCT_UPDATE_VARS")"
check_graphql_errors "$PRODUCT_UPDATE_RESPONSE" "productUpdate"
check_user_errors "$PRODUCT_UPDATE_RESPONSE" '.data.productUpdate.userErrors' "productUpdate"

if [[ "$CREATE_NEW_PRODUCT" == "0" ]]; then
  TYPE_OPTION_ID="$(echo "$EXISTING_RESPONSE" | jq -r '.data.productByHandle.options[]? | select(.name=="Type") | .id' | head -n 1)"
  COLOR_OPTION_ID="$(echo "$EXISTING_RESPONSE" | jq -r '.data.productByHandle.options[]? | select(.name=="Color") | .id' | head -n 1)"

  if [[ -z "$COLOR_OPTION_ID" ]]; then
    PRODUCT_OPTIONS_CREATE_MUTATION='mutation ProductOptionsCreate($productId: ID!, $options: [OptionCreateInput!]!, $variantStrategy: ProductOptionCreateVariantStrategy) {
      productOptionsCreate(productId: $productId, options: $options, variantStrategy: $variantStrategy) {
        product {
          id
          options { id name position values optionValues { id name hasVariants } }
        }
        userErrors { field message }
      }
    }'

    PRODUCT_OPTIONS_CREATE_RESPONSE="$(gql "$PRODUCT_OPTIONS_CREATE_MUTATION" "$(jq -nc --arg product_id "$PRODUCT_ID" --arg color_name "$COLOR_NAME" '{productId: $product_id, options: [{name: "Color", values: [{name: $color_name}]}], variantStrategy: "LEAVE_AS_IS"}')")"
    check_graphql_errors "$PRODUCT_OPTIONS_CREATE_RESPONSE" "productOptionsCreate"
    check_user_errors "$PRODUCT_OPTIONS_CREATE_RESPONSE" '.data.productOptionsCreate.userErrors' "productOptionsCreate"
    refresh_existing_product
    TYPE_OPTION_ID="$(echo "$EXISTING_RESPONSE" | jq -r '.data.productByHandle.options[]? | select(.name=="Type") | .id' | head -n 1)"
  fi

  if [[ -n "$TYPE_OPTION_ID" ]]; then
    PRODUCT_OPTIONS_DELETE_MUTATION='mutation ProductOptionsDelete($productId: ID!, $options: [ID!]!, $strategy: ProductOptionDeleteStrategy) {
      productOptionsDelete(productId: $productId, options: $options, strategy: $strategy) {
        deletedOptionsIds
        product {
          id
          options { id name position values optionValues { id name hasVariants } }
        }
        userErrors { field message }
      }
    }'

    PRODUCT_OPTIONS_DELETE_RESPONSE="$(gql "$PRODUCT_OPTIONS_DELETE_MUTATION" "$(jq -nc --arg product_id "$PRODUCT_ID" --arg type_option_id "$TYPE_OPTION_ID" '{productId: $product_id, options: [$type_option_id], strategy: "NON_DESTRUCTIVE"}')")"
    check_graphql_errors "$PRODUCT_OPTIONS_DELETE_RESPONSE" "productOptionsDelete"
    check_user_errors "$PRODUCT_OPTIONS_DELETE_RESPONSE" '.data.productOptionsDelete.userErrors' "productOptionsDelete"
    refresh_existing_product
  fi

  NEED_REORDER="$(echo "$EXISTING_RESPONSE" | jq -r --argjson expected "$OPTION_NAMES_JSON" '([.data.productByHandle.options[]?.name] != $expected) | tostring')"
  if [[ "$NEED_REORDER" == "true" ]]; then
    PRODUCT_OPTIONS_REORDER_MUTATION='mutation ProductOptionsReorder($productId: ID!, $options: [OptionReorderInput!]!) {
      productOptionsReorder(productId: $productId, options: $options) {
        product {
          id
          options { id name position values optionValues { id name hasVariants } }
        }
        userErrors { field message }
      }
    }'

    PRODUCT_OPTIONS_REORDER_RESPONSE="$(gql "$PRODUCT_OPTIONS_REORDER_MUTATION" "$(jq -nc --arg product_id "$PRODUCT_ID" --argjson options "$OPTION_REORDER_JSON" '{productId: $product_id, options: $options}')")"
    check_graphql_errors "$PRODUCT_OPTIONS_REORDER_RESPONSE" "productOptionsReorder"
    check_user_errors "$PRODUCT_OPTIONS_REORDER_RESPONSE" '.data.productOptionsReorder.userErrors' "productOptionsReorder"
    refresh_existing_product
  fi
fi

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
    echo "ERROR: existing product handle ${HANDLE} has unexpected live variants; refusing to create duplicates." >&2
    echo "Existing SKUs:" >&2
    echo "$EXISTING_SKUS_SORTED" >&2
    echo "Derived SKUs:" >&2
    echo "$DERIVED_SKUS_SORTED" >&2
    exit 1
  fi
fi

if [[ "$SHOULD_CREATE_VARIANTS" == "1" ]]; then
  BULK_CREATE_MUTATION='mutation ProductVariantsBulkCreate($productId: ID!, $variants: [ProductVariantsBulkInput!]!, $strategy: ProductVariantsBulkCreateStrategy) {
    productVariantsBulkCreate(productId: $productId, variants: $variants, strategy: $strategy) {
      productVariants { id sku title price compareAtPrice inventoryPolicy }
      userErrors { field message }
    }
  }'

  BULK_CREATE_VARS="$(jq -nc \
    --arg product_id "$PRODUCT_ID" \
    --argjson variants "$VARIANTS_JSON" '
    {productId: $product_id, variants: $variants, strategy: "REMOVE_STANDALONE_VARIANT"}')"

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
    sku = node["sku"]
    spec = spec_by_sku[sku]
    updates.append(
        {
            "id": node["id"],
            "price": spec["price"],
            "compareAtPrice": spec["compareAtPrice"],
            "inventoryPolicy": "DENY",
        }
    )
print(json.dumps(updates))
PY
)"

  BULK_UPDATE_MUTATION='mutation ProductVariantsBulkUpdate($productId: ID!, $variants: [ProductVariantsBulkInput!]!) {
    productVariantsBulkUpdate(productId: $productId, variants: $variants) {
      productVariants { id sku title price compareAtPrice inventoryPolicy }
      userErrors { field message }
    }
  }'

  BULK_UPDATE_VARS="$(jq -nc \
    --arg product_id "$PRODUCT_ID" \
    --argjson variants "$VARIANTS_UPDATE_JSON" '
    {productId: $product_id, variants: $variants}')"

  BULK_UPDATE_RESPONSE="$(gql "$BULK_UPDATE_MUTATION" "$BULK_UPDATE_VARS")"
  check_graphql_errors "$BULK_UPDATE_RESPONSE" "productVariantsBulkUpdate"
  check_user_errors "$BULK_UPDATE_RESPONSE" '.data.productVariantsBulkUpdate.userErrors' "productVariantsBulkUpdate"
fi

FABRIC_GIDS_JSON='["gid://shopify/Metaobject/69622366305"]'

METAFIELDS_SET_MUTATION='mutation MetafieldsSet($metafields: [MetafieldsSetInput!]!) {
  metafieldsSet(metafields: $metafields) {
    metafields { namespace key type value }
    userErrors { field message }
  }
}'

METAFIELDS_JSON="$(jq -nc \
  --arg pid "$PRODUCT_ID" \
  --arg age_group_value "$(echo "$AGE_GROUP_GIDS_JSON" | jq -c .)" \
  --arg color_value "$(echo "$COLOR_PATTERN_GIDS_JSON" | jq -c .)" \
  --arg fabric_value "$(echo "$FABRIC_GIDS_JSON" | jq -c .)" \
  --arg target_gender_value "$(echo "$TARGET_GENDER_GIDS_JSON" | jq -c .)" \
  --arg size_value "$(echo "$SHOPIFY_SIZE_REFS_JSON" | jq -c .)" \
  --arg seo_title "$SEO_TITLE" \
  --arg seo_description "$SEO_DESCRIPTION" '
  [
      {ownerId: $pid, namespace: "custom", key: "category1", type: "single_line_text_field", value: "Mommy and Me"},
      {ownerId: $pid, namespace: "custom", key: "subcategory", type: "single_line_text_field", value: "Swimsuits"},
      {ownerId: $pid, namespace: "custom", key: "subcategory2", type: "single_line_text_field", value: "Swim Dresses"},
      {ownerId: $pid, namespace: "custom", key: "pattern", type: "single_line_text_field", value: "Blush Floral"},
      {ownerId: $pid, namespace: "custom", key: "style", type: "single_line_text_field", value: "Ruffle Swim Dress"},
      {ownerId: $pid, namespace: "custom", key: "type", type: "single_line_text_field", value: "Swimsuit"},
      {ownerId: $pid, namespace: "mm-google-shopping", key: "custom_product", type: "boolean", value: "false"},
      {ownerId: $pid, namespace: "mm-google-shopping", key: "gender", type: "single_line_text_field", value: "female"},
      {ownerId: $pid, namespace: "mm-google-shopping", key: "age_group", type: "single_line_text_field", value: "adult"},
      {ownerId: $pid, namespace: "mm-google-shopping", key: "condition", type: "single_line_text_field", value: "new"},
      {ownerId: $pid, namespace: "mm-google-shopping", key: "custom_label_0", type: "single_line_text_field", value: "Mommy and Me"},
      {ownerId: $pid, namespace: "mm-google-shopping", key: "custom_label_1", type: "single_line_text_field", value: "Blush Garden"},
      {ownerId: $pid, namespace: "mm-google-shopping", key: "custom_label_2", type: "single_line_text_field", value: "Summer"},
      {ownerId: $pid, namespace: "mm-google-shopping", key: "custom_label_3", type: "single_line_text_field", value: "Ruffle Swim Dress"},
      {ownerId: $pid, namespace: "mm-google-shopping", key: "custom_label_4", type: "single_line_text_field", value: "Two-Role Matching"},
      {ownerId: $pid, namespace: "shopify", key: "age-group", type: "list.metaobject_reference", value: $age_group_value},
      {ownerId: $pid, namespace: "shopify", key: "color-pattern", type: "list.metaobject_reference", value: $color_value},
      {ownerId: $pid, namespace: "shopify", key: "fabric", type: "list.metaobject_reference", value: $fabric_value},
      {ownerId: $pid, namespace: "shopify", key: "size", type: "list.metaobject_reference", value: $size_value},
      {ownerId: $pid, namespace: "shopify", key: "target-gender", type: "list.metaobject_reference", value: $target_gender_value},
      {ownerId: $pid, namespace: "global", key: "title_tag", type: "single_line_text_field", value: $seo_title},
      {ownerId: $pid, namespace: "global", key: "description_tag", type: "single_line_text_field", value: $seo_description}
  ]')"

for batch in \
  "$(echo "$METAFIELDS_JSON" | jq -c '.[0:25]')" \
  "$(echo "$METAFIELDS_JSON" | jq -c '.[25:]')"
do
  if [[ "$(echo "$batch" | jq 'length')" -eq 0 ]]; then
    continue
  fi
  METAFIELDS_SET_RESPONSE="$(gql "$METAFIELDS_SET_MUTATION" "$(jq -nc --argjson metafields "$batch" '{metafields:$metafields}')")"
  check_graphql_errors "$METAFIELDS_SET_RESPONSE" "metafieldsSet"
  check_user_errors "$METAFIELDS_SET_RESPONSE" '.data.metafieldsSet.userErrors' "metafieldsSet"
done

PUBLICATIONS_JSON='[
  {"publicationId":"gid://shopify/Publication/55169925"},
  {"publicationId":"gid://shopify/Publication/21969633377"},
  {"publicationId":"gid://shopify/Publication/29172400225"},
  {"publicationId":"gid://shopify/Publication/76582879329"},
  {"publicationId":"gid://shopify/Publication/76604768353"}
]'

PUBLISH_MUTATION='mutation PublishablePublish($id: ID!, $input: [PublicationInput!]!) {
  publishablePublish(id: $id, input: $input) {
    publishable { availablePublicationsCount { count } }
    userErrors { field message }
  }
}'

PUBLISH_RESPONSE="$(gql "$PUBLISH_MUTATION" "$(jq -nc --arg id "$PRODUCT_ID" --argjson input "$PUBLICATIONS_JSON" '{id:$id, input:$input}')")"
check_graphql_errors "$PUBLISH_RESPONSE" "publishablePublish"
check_user_errors "$PUBLISH_RESPONSE" '.data.publishablePublish.userErrors' "publishablePublish"

MEDIA_QUERY='query ProductMedia($id: ID!) {
  product(id: $id) {
    media(first: 50) {
      nodes {
        ... on MediaImage {
          id
          alt
          image { url }
        }
      }
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

for image_path in "${MEDIA_FILES[@]}"; do
  image_name="$(basename "$image_path")"
  case "$image_name" in
    01-*)
      alt_text="Mother and daughter in matching blush floral ruffle swim dresses outdoors by a pool."
      ;;
    02-*)
      alt_text="Girl wearing the blush floral ruffle swim dress with attached bottoms and a rose applique detail."
      ;;
    *)
      alt_text="Blush Garden mommy-and-me floral ruffle swim dress for mother and daughter."
      ;;
  esac

  if grep -Fxq "$alt_text" <<< "$EXISTING_MEDIA_ALTS"; then
    continue
  fi

  mime_type="$(python3 - "$image_path" <<'PY'
import mimetypes
import sys
print(mimetypes.guess_type(sys.argv[1])[0] or "application/octet-stream")
PY
)"

  STAGED_UPLOAD_MUTATION='mutation StagedUploadsCreate($input: [StagedUploadInput!]!) {
    stagedUploadsCreate(input: $input) {
      stagedTargets {
        url
        resourceUrl
        parameters { name value }
      }
      userErrors { field message }
    }
  }'

  STAGED_UPLOAD_VARS="$(jq -nc \
    --arg filename "$image_name" \
    --arg mime_type "$mime_type" '
    {input: [{filename: $filename, mimeType: $mime_type, resource: "IMAGE", httpMethod: "POST"}]}')"

  STAGED_UPLOAD_RESPONSE="$(gql "$STAGED_UPLOAD_MUTATION" "$STAGED_UPLOAD_VARS")"
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

  PRODUCT_CREATE_MEDIA_MUTATION='mutation ProductCreateMedia($productId: ID!, $media: [CreateMediaInput!]!) {
    productCreateMedia(productId: $productId, media: $media) {
      media {
        ... on MediaImage { id alt }
      }
      userErrors { field message }
    }
  }'

  PRODUCT_CREATE_MEDIA_VARS="$(jq -nc \
    --arg product_id "$PRODUCT_ID" \
    --arg original_source "$resource_url" \
    --arg alt_text "$alt_text" '
    {productId: $product_id, media: [{originalSource: $original_source, mediaContentType: "IMAGE", alt: $alt_text}]}')"

  PRODUCT_CREATE_MEDIA_RESPONSE="$(gql "$PRODUCT_CREATE_MEDIA_MUTATION" "$PRODUCT_CREATE_MEDIA_VARS")"
  check_graphql_errors "$PRODUCT_CREATE_MEDIA_RESPONSE" "productCreateMedia"
  check_user_errors "$PRODUCT_CREATE_MEDIA_RESPONSE" '.data.productCreateMedia.userErrors' "productCreateMedia"
done

sleep 2

VERIFY_QUERY='query VerifyProduct($id: ID!) {
  product(id: $id) {
    id
    title
    handle
    status
    publishedAt
    onlineStoreUrl
    descriptionHtml
    tags
    seo { title description }
    category { id fullName }
    variants(first: 100) {
      nodes {
        id
        sku
        title
        price
        compareAtPrice
        inventoryPolicy
        selectedOptions { name value }
        inventoryItem { tracked requiresShipping }
      }
    }
    options {
      name
      position
      values
      optionValues { id name hasVariants }
    }
    media(first: 50) {
      nodes {
        ... on MediaImage {
          alt
          image { url }
        }
      }
    }
    collections(first: 50) {
      nodes {
        title
        handle
      }
    }
    metafields(first: 80) {
      nodes {
        namespace
        key
        type
        value
      }
    }
    resourcePublicationsV2(first: 20) {
      nodes {
        isPublished
        publishDate
        publication { id name }
      }
    }
  }
}'

VERIFY_RESPONSE="$(gql "$VERIFY_QUERY" "$(jq -nc --arg id "$PRODUCT_ID" '{id:$id}')")"
check_graphql_errors "$VERIFY_RESPONSE" "verify query"
echo "$VERIFY_RESPONSE" > "$VERIFY_JSON_OUT"

python3 - "$VERIFY_JSON_OUT" "${WORK}/derived.json" "${WORK}/size_chart.json" "${WORK}/size_metaobject_map.json" \
  "$LISTING_MD" "$CSV_OUT" "$CSV_HEADER_SOURCE" "$HANDLE" "$TITLE" "$SEO_TITLE" "$SEO_DESCRIPTION" \
  "$PRICE_NEIGHBOR_HANDLE" "$SIZE_NEIGHBOR_HANDLE" "$CHILD_PRICE" "$CHILD_COMPARE" "$MOTHER_PRICE" "$MOTHER_COMPARE" \
  "$VENDOR_URL" "$SCRIPT_PATH" "$SIZE_CHART_OUT" "$BODY_HTML_OUT" "$UPLOAD_DIR" "$PRODUCT_ID" <<'PY'
import csv
import json
import re
import sys
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
mother_price = sys.argv[16]
mother_compare = sys.argv[17]
vendor_url = sys.argv[18]
script_path = sys.argv[19]
size_chart_out = sys.argv[20]
body_html_out = sys.argv[21]
upload_dir = sys.argv[22]
product_gid = sys.argv[23]

verify = json.loads(verify_path.read_text())
derived = json.loads(derived_path.read_text())
chart = json.loads(chart_path.read_text())
size_map = {row["picker_label"]: row for row in json.loads(size_map_path.read_text())}
product = verify["data"]["product"]
variants = product["variants"]["nodes"]
product_options = product["options"]
metafields = product["metafields"]["nodes"]
collections = product["collections"]["nodes"]
publications = product["resourcePublicationsV2"]["nodes"]

spec_by_sku = {row["sku"]: row for row in derived["recap"]}
live_skus_sorted = sorted(v["sku"] for v in variants)
derived_skus_sorted = derived["derived_skus_sorted"]
option_names = derived["option_names"]
expected_option_pairs = {tuple(pair) for pair in derived["expected_variant_option_pairs"]}
live_option_names = [option["name"] for option in product_options]

html_body = product["descriptionHtml"]
th_count = len(re.findall(r"<th>", html_body))
table_match = re.search(r"<table id=\"size-chart\">(.*?)</table>", html_body, re.S)
table_html = table_match.group(1) if table_match else ""
tbody_match = re.search(r"<tbody>(.*?)</tbody>", html_body, re.S)
tbody_rows = re.findall(r"<tr>(.*?)</tr>", tbody_match.group(1), re.S) if tbody_match else []
first_cells = []
age_cells = []
for row_html in tbody_rows:
    cells = re.findall(r"<td>(.*?)</td>", row_html, re.S)
    first_cells.append(re.sub(r"<.*?>", "", cells[0]).strip() if len(cells) > 0 else "")
    age_cells.append(re.sub(r"<.*?>", "", cells[1]).strip() if len(cells) > 1 else "")

expected_first_cells = [row["picker_label"] for row in chart]
expected_age_cells = [row["age"] if row["audience"] == "child" else "" for row in chart]
live_option_pairs = set()
for variant in variants:
    option_map = {opt["name"]: opt["value"] for opt in variant["selectedOptions"]}
    live_option_pairs.add(tuple(option_map.get(name) for name in option_names))

expected_publications = {
    "gid://shopify/Publication/55169925",
    "gid://shopify/Publication/21969633377",
    "gid://shopify/Publication/29172400225",
    "gid://shopify/Publication/76582879329",
    "gid://shopify/Publication/76604768353",
}
published_ids = {node["publication"]["id"] for node in publications if node["isPublished"]}
metafield_keys = {(node["namespace"], node["key"]) for node in metafields}

checks = [
    ("Title <= 70 chars", len(product["title"]) <= 70, str(len(product["title"]))),
    ("SEO title <= 60 chars", len(product["seo"]["title"]) <= 60, str(len(product["seo"]["title"]))),
    ("SEO description <= 155 chars", len(product["seo"]["description"]) <= 155, str(len(product["seo"]["description"]))),
    ("Live variant count matches SIZE_CHART", len(variants) == len(chart), f"{len(variants)} vs {len(chart)}"),
    ("Live SKUs match derived SKUs", live_skus_sorted == derived_skus_sorted, ", ".join(live_skus_sorted)),
    ("Live option axes match derived axes", live_option_names == option_names, " / ".join(live_option_names)),
    (f"Every {' x '.join(option_names)} combination exists", live_option_pairs == expected_option_pairs, str(sorted(live_option_pairs))),
    ("Size table first column matches picker labels", first_cells == expected_first_cells, " | ".join(first_cells)),
    ("Age cells are blank for mother rows", age_cells == expected_age_cells, " | ".join(age_cells)),
    ("Each size table has 10 headers", th_count == 10, str(th_count)),
    ("Table row count matches SIZE_CHART", len(tbody_rows) == len(chart), str(len(tbody_rows))),
    ("Size table exposes vendor recommendation units", all(token in table_html for token in ["Weight (kg/lbs)", "Height (cm/in)", "Chest/Bust (bra size)", "Waist (cm/in)"]), "kg/lbs + cm/in + bra size"),
    ("Mother waist guidance is populated", all(row["waist_display"] not in (None, "", "-") for row in chart if row["audience"] == "mother"), "all mother rows populated"),
    ("publishedAt is populated", bool(product["publishedAt"]), product["publishedAt"] or ""),
    ("onlineStoreUrl is populated", bool(product["onlineStoreUrl"]), product["onlineStoreUrl"] or ""),
    (
        "Taxonomy category is set",
        product["category"]["id"] == "gid://shopify/TaxonomyCategory/aa-1-20-17"
        and product["category"]["fullName"] == "Apparel & Accessories > Clothing > Swimwear > Swim Dresses",
        f'{product["category"]["id"]} | {product["category"]["fullName"]}',
    ),
    ("Required publications are live", expected_publications.issubset(published_ids), str(sorted(published_ids))),
    ("Vendor URL tag present", vendor_url in product["tags"], vendor_url),
    ("Swimsuits collection tags are present", "Swimsuits" in product["tags"] and "Mommy and Me" in product["tags"], ", ".join(sorted(set(product["tags"]) & {"Swimsuits", "Mommy and Me"}))),
]

price_rows = []
for variant in variants:
    spec = spec_by_sku[variant["sku"]]
    price_ok = variant["price"] == spec["price"]
    cmp_ok = variant["compareAtPrice"] == spec["compare_at_price"]
    tracked_ok = variant["inventoryItem"]["tracked"] and variant["inventoryItem"]["requiresShipping"]
    deny_ok = variant["inventoryPolicy"] == "DENY"
    price_rows.append(
        {
            "sku": variant["sku"],
            "live_price": variant["price"],
            "live_compare": variant["compareAtPrice"],
            "spec_price": spec["price"],
            "spec_compare": spec["compare_at_price"],
            "match": "Y" if (price_ok and cmp_ok and tracked_ok and deny_ok) else "N",
        }
    )

required_written = {
    ("custom", "category1"),
    ("custom", "subcategory"),
    ("custom", "subcategory2"),
    ("custom", "pattern"),
    ("custom", "style"),
    ("custom", "type"),
    ("mm-google-shopping", "custom_product"),
    ("mm-google-shopping", "gender"),
    ("mm-google-shopping", "age_group"),
    ("mm-google-shopping", "condition"),
    ("mm-google-shopping", "custom_label_0"),
    ("mm-google-shopping", "custom_label_1"),
    ("mm-google-shopping", "custom_label_2"),
    ("mm-google-shopping", "custom_label_3"),
    ("mm-google-shopping", "custom_label_4"),
    ("shopify", "age-group"),
    ("shopify", "color-pattern"),
    ("shopify", "fabric"),
    ("shopify", "size"),
    ("shopify", "target-gender"),
    ("global", "title_tag"),
    ("global", "description_tag"),
}
checks.append(("Applicable metafields are written", required_written.issubset(metafield_keys), str(sorted(required_written - metafield_keys))))

skipped_metafields = {
    "shopify.care-instructions": "The store's only live standard care option is `Machine washable`, which is less honest than the swim-specific rinse and hand-wash guidance used in the body copy.",
    "shopify.clothing-features": "The store's only live clothing-features option is `Insulated`, which is inaccurate for this lightweight swimsuit.",
    "shopify.dress-occasion": "Skipped because this swim-dress run only writes the universal metafields required by the listing prompt plus the honest swimwear basics.",
    "shopify.dress-style": "Skipped because the live swimwear neighbors do not rely on this standard metafield and the run already carries the style in custom metafields.",
    "shopify.neckline": "The ruffle neckline is visible in the imagery, but this run keeps swimwear writes to the lean verified set used by the live swimwear catalog.",
    "shopify.skirt-dress-length-type": "Skipped because the chart is a fit-recommendation table with no garment-length measurements to support a dress-length taxonomy write.",
    "shopify.sleeve-length-type": "Skipped per the listing prompt note used in recent swimwear and pajama runs: omit sleeve-length-type for swimsuits.",
}

written_metafields = []
for node in metafields:
    if node["namespace"] in {"custom", "mm-google-shopping", "shopify", "global"}:
        written_metafields.append(node)

links = {
    "admin": f"https://admin.shopify.com/store/dresslikemommy/products/{product_gid.split('/')[-1]}",
    "live": product["onlineStoreUrl"],
}

with csv_header_source.open(newline="") as fh:
    header = next(csv.reader(fh))

csv_rows = []
for recap in derived["recap"]:
    row = {header_name: "" for header_name in header}

    def put(field, value):
        if field in row:
            row[field] = value

    put("Handle", handle)
    put("Title", title)
    put("Body (HTML)", product["descriptionHtml"])
    put("Vendor", "dresslikemommy.com")
    put("Product Category", "Apparel & Accessories > Clothing > Swimwear > Swim Dresses")
    put("Type", "Matching Family Swimwear")
    put("Tags", ", ".join(product["tags"]))
    put("Published", "TRUE")
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
    put("SEO Title", seo_title)
    put("SEO Description", seo_description)
    put("Google Shopping / Gender", "female")
    put("Google Shopping / Age Group", "adult")
    put("Google Shopping / Condition", "new")
    put("Google Shopping / Custom Product", "FALSE")
    put("Google Shopping / Custom Label 0", "Mommy and Me")
    put("Google Shopping / Custom Label 1", "Blush Garden")
    put("Google Shopping / Custom Label 2", "Summer")
    put("Google Shopping / Custom Label 3", "Ruffle Swim Dress")
    put("Google Shopping / Custom Label 4", "Two-Role Matching")
    put("Category1 (product.metafields.custom.category1)", "Mommy and Me")
    put("Pattern (product.metafields.custom.pattern)", "Blush Floral")
    put("Style (product.metafields.custom.style)", "Ruffle Swim Dress")
    put("SubCategory (product.metafields.custom.subcategory)", "Swimsuits")
    put("SubCategory2 (product.metafields.custom.subcategory2)", "Swim Dresses")
    put("Type (product.metafields.custom.type)", "Swimsuit")
    put("Google: Custom Product (product.metafields.mm-google-shopping.custom_product)", "false")
    put("Age group (product.metafields.shopify.age-group)", "Toddlers, Kids, Adults")
    put("Color (product.metafields.shopify.color-pattern)", "White, Pink, Floral")
    put("Fabric (product.metafields.shopify.fabric)", "Polyester")
    put("Size (product.metafields.shopify.size)", ", ".join(x["picker_label"] for x in derived["recap"]))
    put("Target Gender (product.metafields.shopify.target-gender)", "Female")
    put("Status", "active")
    csv_rows.append(row)

with csv_out_path.open("w", newline="") as fh:
    writer = csv.DictWriter(fh, fieldnames=header)
    writer.writeheader()
    for row in csv_rows:
        writer.writerow(row)

lines = []
lines.append(f"# {title}")
lines.append("")
lines.append("## Links")
lines.append(f"- **Admin:** {links['admin']}")
lines.append(f"- **Live:** {links['live']}")
lines.append(f"- **Vendor:** {vendor_url}")
lines.append(f"- **Product GID:** `{product_gid}`")
lines.append(f"- **Handle:** `{handle}`")
lines.append("")
lines.append("## Inputs (resolved)")
lines.append("| Field | Value |")
lines.append("|---|---|")
lines.append(f"| VENDOR_URL | {vendor_url} |")
lines.append("| SIZE_CHART_SOURCE | attached image |")
lines.append("| LISTING_MODE | Mommy and Me |")
lines.append("| PRIMARY_CATEGORY | Swimsuit -> Swimsuits (Shopify taxonomy resolved to Swim Dresses) |")
lines.append("| DESIGNS_TO_LIST | Options color and size only -> Blush Floral only, no Type axis |")
lines.append("| EXCLUDE_ITEMS | none |")
lines.append("| SHORTCODE | auto -> `BGDN` |")
lines.append("| COLOR_TOKEN | auto -> `BLUSH` |")
lines.append("| FORCE_SPEC_PRICES | true |")
lines.append("")
lines.append("## Vendor fetch status")
lines.append("The direct 1688 page was captcha-blocked during this run on 2026-04-23, so the attached size-chart image and supplied product photos were used as the authoritative source of truth. The imagery shows a white-and-blush floral mother-daughter swim dress with a square ruffle neckline, attached bottoms, and a small rosette accent at the hip. Pricing was anchored to the live swim-dress neighbor `elegant-mother-daughter-matching-one-piece-swimsuit-with-patterned-mesh-skirt-family-beachwear-set`, size references were anchored to direct live `shopify--size` metaobject lookups, and the stale swimsuit taxonomy map in the prompt was corrected via live `node(id:)` validation before publish.")
lines.append("")
lines.append("## Title & SEO")
lines.append("| | Value | Chars |")
lines.append("|---|---|---|")
lines.append(f"| Product Title | `{product['title']}` | {len(product['title'])} |")
lines.append(f"| SEO Title | `{product['seo']['title']}` | {len(product['seo']['title'])} |")
lines.append(f"| SEO Description | `{product['seo']['description']}` | {len(product['seo']['description'])} |")
lines.append("")
lines.append("## SIZE_CHART recap")
lines.append("| Role | Vendor | Picker | SKU | Price | Cmp | shopify.size GID |")
lines.append("|---|---|---|---|---|---|---|")
for recap in derived["recap"]:
    lines.append(
        f"| {recap['role']} | {recap['vendor_label']} | {recap['picker_label']} | `{recap['sku']}` | {recap['price']} | {recap['compare_at_price']} | `{recap['shopify_size_gid']}` ({recap['catalog_label']}) |"
    )
lines.append("")
lines.append("### Derivations (flagged per spec)")
lines.append("- The swimsuit taxonomy GID in the canonical prompt (`gid://shopify/TaxonomyCategory/aa-1-13-15`) does not resolve in the live 2025-01 Admin API, so this run halted and corrected the taxonomy to the live leaf `gid://shopify/TaxonomyCategory/aa-1-20-17` (`Swim Dresses`) before publishing.")
lines.append("- The chart is a fit-recommendation table, not a garment-measurement table. Unsupported columns such as skirt length, pant length, hip, and garment length were kept as `-` instead of being fabricated.")
lines.append("- Child rows were mapped to the nearest canonical DLM size labels by height midpoint: 100-105 cm -> Child 3 Years, 105-115 cm -> Child 4 Years, 116-125 cm -> Child 5 Years, 126-140 cm -> Child 6-7 Years, and 140-155 cm -> Child 9-10 Years.")
lines.append("- Adult waist guidance was converted from Chinese chi ranges to cm/in for the shopper-facing table while the bust guidance stayed in the vendor's published bra-size notation.")
lines.append("- Adult 2XL, 3XL, and 4XL rows are marked `部分款` in the vendor chart. They were retained because the operator attached this exact chart for the selected floral print and did not exclude those rows.")
lines.append("- `Mother 4XL` extends the printed size scheme in the prompt, but the attached chart explicitly includes a 4XL row and the live store exposes a truthful `shopify--size` 4XL metaobject, so the run preserved it instead of collapsing the size range.")
lines.append("")
lines.append("### Vendor -> picker mapping log")
lines.append("- Child M -> Child 3 Years")
lines.append("- Child L -> Child 4 Years")
lines.append("- Child XL -> Child 5 Years")
lines.append("- Child 2XL(部分款) -> Child 6-7 Years")
lines.append("- Child 3XL(部分款) -> Child 9-10 Years")
lines.append("- Mother M -> Mother M")
lines.append("- Mother L -> Mother L")
lines.append("- Mother XL -> Mother XL")
lines.append("- Mother 2XL(部分款) -> Mother 2XL")
lines.append("- Mother 3XL(部分款) -> Mother 3XL")
lines.append("- Mother 4XL(部分款) -> Mother 4XL")
lines.append("")
lines.append("### EXCLUDE_ITEMS decisions")
lines.append("- No exclusions were requested, so every vendor-supported row from the chart was kept.")
lines.append("")
lines.append("## Body HTML")
lines.append("- 1 `<ul>` with 6 bullets (fabric, family story, print, design details, care, size range).")
lines.append("- 1 `<h3>` plus 1 size table with 10 `<th>` headers and 11 body rows.")
lines.append("- The size table keeps vendor recommendation data honest: height and weight use metric + imperial, bust stays in vendor bra-size notation, and unsupported measurement columns stay `-`.")
lines.append("- 2 narrative paragraphs, 1 key-features block, and 1 closing CTA paragraph.")
lines.append("")
lines.append("## Option axes & variants")
lines.append("- Option 1: `Size` -> `Child 3 Years`, `Child 4 Years`, `Child 5 Years`, `Child 6-7 Years`, `Child 9-10 Years`, `Mother M`, `Mother L`, `Mother XL`, `Mother 2XL`, `Mother 3XL`, `Mother 4XL`")
lines.append(f"- Option 2: `Color` -> `{derived['color_values'][0]['name']}`")
lines.append(f"- Variants live: **{len(variants)}**")
lines.append("")
lines.append("## Verify pass table")
lines.append("| Check | Result | Detail |")
lines.append("|---|---|---|")
for label, ok, detail in checks:
    lines.append(f"| {label} | {'Y' if ok else 'N'} | {detail} |")
lines.append("")
lines.append("## Price parity (FORCE_SPEC_PRICES=true)")
lines.append("| SKU | Live Price | Live Cmp | Spec Price | Spec Cmp | Match |")
lines.append("|---|---|---|---|---|---|")
for row in price_rows:
    lines.append(f"| {row['sku']} | {row['live_price']} | {row['live_compare']} | {row['spec_price']} | {row['spec_compare']} | {row['match']} |")
lines.append("")
lines.append("## Metafields - written")
lines.append("| Namespace.Key | Type | Value |")
lines.append("|---|---|---|")
for node in sorted(written_metafields, key=lambda x: (x["namespace"], x["key"])):
    value = node["value"]
    if len(value) > 90:
        value = value[:87] + "..."
    lines.append(f"| {node['namespace']}.{node['key']} | {node['type']} | `{value}` |")
lines.append("")
lines.append("## Metafields - skipped")
lines.append("| Namespace.Key | Reason |")
lines.append("|---|---|")
for key, reason in skipped_metafields.items():
    lines.append(f"| {key} | {reason} |")
lines.append("")
lines.append(f"## Tags written ({len(product['tags'])})")
lines.append("`" + ", ".join(product["tags"]) + "`")
lines.append("")
lines.append("## Publication")
lines.append("- Online Store")
lines.append("- Google & YouTube")
lines.append("- Facebook & Instagram")
lines.append("- Pinterest")
lines.append("- TikTok")
lines.append("")
lines.append("## Smart collections")
if collections:
    for collection in collections:
        lines.append(f"- {collection['title']} (`/{collection['handle']}`)")
else:
    lines.append("- No smart collections were returned immediately after publish. Shopify may still be reindexing.")
lines.append("")
lines.append("## Manual follow-ups")
lines.append("- Confirm the exact fiber composition if the vendor page becomes accessible without captcha; `shopify.fabric` is set to `Polyester` because that is the only honest live standard fabric metaobject available in this store for this run.")
lines.append("- Re-check whether the selected floral print truly carries the vendor's `部分款` 4XL row once the source page is accessible without captcha.")
lines.append("- Inventory quantities and per-variant grams still need operator stock values.")
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
lines.append(f"- Price neighbor: `{price_neighbor_handle}`")
lines.append(f"- Size reference source: `{size_neighbor_handle}`")
lines.append("- Collection rules verified live: `/swimsuits` requires the tags `Swimsuits` + `Mommy and Me`.")

listing_md_path.write_text("\n".join(lines) + "\n")
PY

echo "Runner complete: ${SCRIPT_PATH}"
echo "Listing log: ${LISTING_MD}"
echo "Verify JSON: ${VERIFY_JSON_OUT}"
echo "CSV: ${CSV_OUT}"
