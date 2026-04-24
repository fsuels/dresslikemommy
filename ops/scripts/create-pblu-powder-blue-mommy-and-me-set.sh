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

HANDLE="powder-blue-mommy-and-me-set"
TITLE="Powder Blue Mommy and Me Set — Flutter Top & Eyelet Pants"
SEO_TITLE="Powder Blue Mommy & Me Set | Dress Like Mommy"
SEO_DESCRIPTION="Lightweight woven mommy-and-me set with a flutter top and eyelet pants for mom + daughter. Sizes 3Y–10Y and Mom S–M."
PRINT_NAME="Powder Blue"
SHORTCODE="PBLU"
COLOR_TOKEN="BLUE"
COLOR_NAME="Blue"
LISTING_MODE="Mommy and Me"
CATEGORY="Sets"
CATEGORY_WORD="Set"
PRODUCT_TYPE="Matching Family Sets"
CUSTOM_TYPE="Two-Piece Set"
TAXONOMY_GID="gid://shopify/TaxonomyCategory/aa-1-11"
EXPECTED_TAXONOMY_FULL_NAME="Apparel & Accessories > Clothing > Outfit Sets"
MERCH_SUBCATEGORY="Dresses"
MERCH_SUBCATEGORY2="Summer Dresses"
MERCH_STYLE="Resort Sundress"
MERCH_TYPE="Dress"
MERCH_COLLECTION_TAG="Sundresses"
SEASON="Summer"
VENDOR_URL="https://detail.1688.com/offer/1034212252780.html"
VENDOR="dresslikemommy.com"
FORCE_SPEC_PRICES="true"
CHILD_PRICE="28.99"
MOTHER_PRICE="31.99"
PRICE_NEIGHBOR_HANDLE="blue-striped-family-matching-set"
SIZE_NEIGHBOR_HANDLE="white-lace-mommy-and-me-dresses"

SCRIPT_PATH="${ROOT}/ops/scripts/create-pblu-powder-blue-mommy-and-me-set.sh"
UPLOAD_DIR="${ROOT}/uploads/${HANDLE}"
LISTING_MD="${ROOT}/ops/listings/${HANDLE}-listing.md"
CSV_OUT="${ROOT}/ops/listings/${HANDLE}-shopify-import.csv"
VERIFY_JSON_OUT="${ROOT}/ops/listings/verify-${HANDLE}.json"
SIZE_CHART_OUT="${ROOT}/ops/listings/size-chart-${HANDLE}.json"
BODY_HTML_OUT="${ROOT}/ops/listings/body-${HANDLE}.html"
CSV_HEADER_SOURCE="${ROOT}/bird-chirping-mommy-and-me-pajamas-shopify-import.csv"

PUB_ONLINE="gid://shopify/Publication/55169925"
PUB_GOOGLE="gid://shopify/Publication/21969633377"
PUB_META="gid://shopify/Publication/29172400225"
PUB_PINT="gid://shopify/Publication/76582879329"
PUB_TIKTOK="gid://shopify/Publication/76604768353"

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

cat > "${WORK}/size_chart.json" <<'JSON'
[
  {"audience":"child","role":"Girl Set","garment":"Set","vendor_label":"100","picker_label":"Child 3 Years","sku_suffix":"KID3Y","age":"3","weight":"14–16 kg / 31–35 lbs","height":"95–105 cm / 37–41 in","chest_cm":72,"hip_cm":76,"waist_cm":44,"length_cm":44,"skirt_cm":44,"pant_cm":56},
  {"audience":"child","role":"Girl Set","garment":"Set","vendor_label":"110","picker_label":"Child 4 Years","sku_suffix":"KID4Y","age":"4","weight":"16–19 kg / 35–42 lbs","height":"105–115 cm / 41–45 in","chest_cm":76,"hip_cm":80,"waist_cm":46,"length_cm":48,"skirt_cm":48,"pant_cm":61},
  {"audience":"child","role":"Girl Set","garment":"Set","vendor_label":"120","picker_label":"Child 5 Years","sku_suffix":"KID5Y","age":"5","weight":"19–22 kg / 42–49 lbs","height":"115–125 cm / 45–49 in","chest_cm":80,"hip_cm":84,"waist_cm":49,"length_cm":51,"skirt_cm":51,"pant_cm":66},
  {"audience":"child","role":"Girl Set","garment":"Set","vendor_label":"130","picker_label":"Child 6-7 Years","sku_suffix":"KID67Y","age":"6–7","weight":"22–27 kg / 49–60 lbs","height":"125–135 cm / 49–53 in","chest_cm":84,"hip_cm":88,"waist_cm":52,"length_cm":54,"skirt_cm":54,"pant_cm":72},
  {"audience":"child","role":"Girl Set","garment":"Set","vendor_label":"140","picker_label":"Child 8 Years","sku_suffix":"KID8Y","age":"8","weight":"27–32 kg / 60–71 lbs","height":"135–145 cm / 53–57 in","chest_cm":88,"hip_cm":92,"waist_cm":55,"length_cm":59,"skirt_cm":59,"pant_cm":78},
  {"audience":"child","role":"Girl Set","garment":"Set","vendor_label":"150","picker_label":"Child 9-10 Years","sku_suffix":"KID910Y","age":"9–10","weight":"32–38 kg / 71–84 lbs","height":"145–155 cm / 57–61 in","chest_cm":92,"hip_cm":96,"waist_cm":58,"length_cm":64,"skirt_cm":64,"pant_cm":84},
  {"audience":"mother","role":"Mother Set","garment":"Set","vendor_label":"S","picker_label":"Mother S","sku_suffix":"S","age":"—","weight":"50–57 kg / 110–125 lbs","height":"155–163 cm / 61–64 in","chest_cm":96,"hip_cm":100,"waist_cm":65,"length_cm":72,"skirt_cm":72,"pant_cm":91},
  {"audience":"mother","role":"Mother Set","garment":"Set","vendor_label":"M","picker_label":"Mother M","sku_suffix":"M","age":"—","weight":"57–64 kg / 125–141 lbs","height":"160–168 cm / 63–66 in","chest_cm":100,"hip_cm":104,"waist_cm":69,"length_cm":74,"skirt_cm":74,"pant_cm":93}
]
JSON

cat > "${WORK}/size_metaobject_map.json" <<'JSON'
[
  {"picker_label":"Child 3 Years","gid":"gid://shopify/Metaobject/129972895841","catalog_label":"3-4 years","source_handle":"white-lace-mommy-and-me-dresses"},
  {"picker_label":"Child 4 Years","gid":"gid://shopify/Metaobject/129972928609","catalog_label":"4-5 years","source_handle":"white-lace-mommy-and-me-dresses"},
  {"picker_label":"Child 5 Years","gid":"gid://shopify/Metaobject/129972961377","catalog_label":"5-6 years","source_handle":"white-lace-mommy-and-me-dresses"},
  {"picker_label":"Child 6-7 Years","gid":"gid://shopify/Metaobject/139840323681","catalog_label":"6-7 years","source_handle":"white-lace-mommy-and-me-dresses"},
  {"picker_label":"Child 8 Years","gid":"gid://shopify/Metaobject/139840356449","catalog_label":"7-8 years","source_handle":"white-lace-mommy-and-me-dresses"},
  {"picker_label":"Child 9-10 Years","gid":"gid://shopify/Metaobject/139840389217","catalog_label":"8-9 years (closest live catalog match)","source_handle":"white-lace-mommy-and-me-dresses"},
  {"picker_label":"Mother S","gid":"gid://shopify/Metaobject/129975255137","catalog_label":"Mother S","source_handle":"white-lace-mommy-and-me-dresses"},
  {"picker_label":"Mother M","gid":"gid://shopify/Metaobject/129975222369","catalog_label":"Mother M","source_handle":"white-lace-mommy-and-me-dresses"}
]
JSON

cp "${WORK}/size_chart.json" "$SIZE_CHART_OUT"

python3 - "${WORK}/size_chart.json" "${WORK}/size_metaobject_map.json" "${WORK}/derived.json" "${WORK}/body.html" \
  "$TITLE" "$SEO_TITLE" "$SEO_DESCRIPTION" "$SHORTCODE" "$COLOR_TOKEN" "$COLOR_NAME" "$PRINT_NAME" \
  "$CHILD_PRICE" "$CHILD_COMPARE" "$MOTHER_PRICE" "$MOTHER_COMPARE" "$VENDOR_URL" "$SEASON" <<'PY'
import html
import json
import math
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
season = sys.argv[17]

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
    "chest_cm",
    "hip_cm",
    "waist_cm",
    "length_cm",
    "pant_cm",
]

role_tokens = {
    "Girl Set": "GRL",
    "Mother Set": "MOM",
}
size_tokens = {
    "Child 3 Years": "KID3Y",
    "Child 4 Years": "KID4Y",
    "Child 5 Years": "KID5Y",
    "Child 6-7 Years": "KID67Y",
    "Child 8 Years": "KID8Y",
    "Child 9-10 Years": "KID910Y",
    "Mother S": "S",
    "Mother M": "M",
}

def cm_in(value):
    return f"{value} cm / {value / 2.54:.1f} in"

errors = []
seen_pairs = set()
for row in chart:
    missing = [field for field in required if row.get(field) in (None, "")]
    if missing:
      errors.append(f"row {row.get('vendor_label')} missing {', '.join(missing)}")
    if row.get("skirt_cm") in (None, "") and row.get("sleeve_cm") in (None, ""):
        errors.append(f"row {row.get('vendor_label')} missing skirt_cm/sleeve_cm")
    pair = (row.get("role"), row.get("picker_label"))
    if pair in seen_pairs:
        errors.append(f"duplicate (role, picker_label) pair: {pair}")
    seen_pairs.add(pair)
    if row.get("role") not in role_tokens:
        errors.append(f"unknown role token mapping for {row.get('role')}")
    if row.get("picker_label") not in size_tokens:
        errors.append(f"unknown size token mapping for {row.get('picker_label')}")
    if row.get("picker_label") not in size_map:
        errors.append(f"missing size metaobject mapping for {row.get('picker_label')}")

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

garments = sorted({row["garment"] for row in chart})
raw_size_labels = [row["picker_label"] for row in chart]
has_duplicate_size_labels = len(set(raw_size_labels)) != len(raw_size_labels)
use_type_option = len(garments) > 1 or has_duplicate_size_labels

type_values = []
seen_types = set()
if use_type_option:
    for row in chart:
        if row["role"] not in seen_types:
            type_values.append({"name": row["role"]})
            seen_types.add(row["role"])

color_values = [{"name": color_name}]
option_axes = (
    [
        {"name": "Type", "values": [value["name"] for value in type_values]},
        {"name": "Size", "values": [value["name"] for value in size_values]},
    ]
    if use_type_option
    else [
        {"name": "Size", "values": [value["name"] for value in size_values]},
        {"name": "Color", "values": [color_name]},
    ]
)
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
    option_names = [axis["name"] for axis in option_axes]
    option_values = (
        [row["role"], row["picker_label"]]
        if use_type_option
        else [row["picker_label"], color_name]
    )
    variants.append({
        "price": price,
        "compareAtPrice": compare,
        "inventoryPolicy": "DENY",
        "inventoryItem": {
            "sku": sku,
            "tracked": True,
            "requiresShipping": True,
        },
        "optionValues": [
            {"optionName": option_name, "name": option_value}
            for option_name, option_value in zip(option_names, option_values)
        ],
    })
    expected_variant_option_pairs.append(option_values)
    recap.append({
        **row,
        "sku": sku,
        "price": price,
        "compare_at_price": compare,
        "shopify_size_gid": size_map[row["picker_label"]]["gid"],
        "catalog_label": size_map[row["picker_label"]]["catalog_label"],
        "option1_value": option_values[0],
        "option2_value": option_values[1],
    })

child_labels = [row["picker_label"] for row in chart if row["audience"] == "child"]
mother_labels = [row["picker_label"] for row in chart if row["audience"] == "mother"]

def size_phrase():
    kid = "3Y–10Y" if child_labels == [
        "Child 3 Years",
        "Child 4 Years",
        "Child 5 Years",
        "Child 6-7 Years",
        "Child 8 Years",
        "Child 9-10 Years",
    ] else ", ".join(label.replace("Child ", "").replace(" Years", "Y") for label in child_labels)
    moms = "Mom S–M" if mother_labels == ["Mother S", "Mother M"] else "Mom " + ", ".join(label.replace("Mother ", "") for label in mother_labels)
    return f"{kid} and {moms}"

def li(label, text):
    return f"<li><strong>{label}:</strong> {html.escape(text)}</li>"

rows_html = []
for row in chart:
    rows_html.append(
        "<tr>"
        f"<td>{html.escape(row['picker_label'])}</td>"
        f"<td>{html.escape(row['age'])}</td>"
        f"<td>{html.escape(row['weight'])}</td>"
        f"<td>{html.escape(row['height'])}</td>"
        f"<td>{cm_in(row['chest_cm'])}</td>"
        f"<td>{cm_in(row['skirt_cm'])}</td>"
        f"<td>{cm_in(row['pant_cm'])}</td>"
        f"<td>{cm_in(row['hip_cm'])}</td>"
        f"<td>{cm_in(row['waist_cm'])}</td>"
        f"<td>{cm_in(row['length_cm'])}</td>"
        "</tr>"
    )

body_html = "\n".join([
    "<ul>",
    li("Fabric", "Lightweight woven set with an airy flutter top and embroidered eyelet pants for breezy summer wear."),
    li("Family story", "A coastal-ready matching set for mom and daughter, made for beach walks, vacations, and photo days."),
    li("Print", f"\"{print_name}\" pairs a soft sky-blue top with crisp white eyelet wide-leg pants."),
    li("Design details", "Adjustable spaghetti straps, a floaty ruffle hem, scalloped eyelet pants, and an easy pull-on waistband."),
    li("Care", "Machine wash cold on gentle, line dry, do not bleach, and use a cool iron on the reverse if needed."),
    li("Size range", f"Girls Child 3 Years to Child 9-10 Years; Mother S to Mother M."),
    "</ul>",
    "",
    "<h3>Size Chart — Top & Pants Set</h3>",
    "<table id=\"size-chart\">",
    "  <thead>",
    "    <tr>",
    "      <th>Size</th>",
    "      <th>Age</th>",
    "      <th>Weight (kg/lbs)</th>",
    "      <th>Height (cm/in)</th>",
    "      <th>Chest/Bust (cm/in)</th>",
    "      <th>Sleeve or Skirt (cm/in)</th>",
    "      <th>Pant/Short or — (cm/in)</th>",
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
    "<p>Bring a little seaside calm to your matching-moment wardrobe with the Powder Blue Mommy and Me Set. The floaty top skims softly away from the body for an airy feel, while the bright white eyelet pants add texture, movement, and a vacation-ready finish. From beach houses to boardwalk photos, it delivers that dressed-up-without-trying look in one easy pairing.</p>",
    "",
    "<p>The styling is playful but polished: adjustable straps, a soft flutter hem, scalloped eyelet pants, and a relaxed fit that moves comfortably through warm-weather plans. Wear it for resort dinners, family photos, brunch by the water, or any day you want your mom-and-mini look to feel fresh, light, and picture-perfect.</p>",
    "",
    "<h3>Key Features:</h3>",
    "<ul>",
    li("Airy summer feel", "Lightweight woven textures keep the set comfortable on sunny days."),
    li("Photo-ready contrast", "Powder blue and crisp white create a fresh coastal palette."),
    li("Two-piece versatility", "Style the flutter top and eyelet pants together or mix them with closet basics."),
    li("Adjustable comfort", "Straps and an easy waistband help each size wear comfortably."),
    li("Mom + mini matching", "Both roles share the same soft resort-ready silhouette for easy twinning."),
    "</ul>",
    "",
    "<p>Add your sizes and make the next beach day, vacation dinner, or family photo feel instantly coordinated.</p>",
])

tags = [
    "Mommy and Me",
    "Dresses",
    "Summer Dresses",
    "Sundresses",
    "Matching Family Dresses",
    "Matching Family Dress",
    "Matching Family Outfits",
    "Summer",
    "Summer Matching Outfit",
    "Beach",
    "Resort",
    "Vacation",
    "Powder Blue",
    "Blue",
    "White",
    "Eyelet",
    "Scalloped",
    "Ruffle",
    "Flutter Top",
    "Sleeveless Dress",
    "Wide-Leg Pants",
    "Girl Dress",
    "Mother Dress",
    "Mother S",
    "Mother M",
    "Mom Size S",
    "Mom Size M",
    "Child 2-3yr",
    "Child 4-5yr",
    "Child 6-8yr",
    "Child 9-10yr",
    vendor_url,
]
tags = sorted(dict.fromkeys(tags))

derived = {
    "use_type_option": use_type_option,
    "has_duplicate_size_labels": has_duplicate_size_labels,
    "product_options": product_options,
    "option_axes": option_axes,
    "option_names": [axis["name"] for axis in option_axes],
    "type_values": type_values,
    "color_values": color_values,
    "size_values": size_values,
    "expected_variant_option_pairs": expected_variant_option_pairs,
    "variants": variants,
    "row_count": len(chart),
    "derived_skus_sorted": sorted(v["inventoryItem"]["sku"] for v in variants),
    "shopify_size_refs": [size_map[row["picker_label"]]["gid"] for row in chart],
    "size_phrase": size_phrase(),
    "tags": tags,
    "recap": recap,
}

derived_path.write_text(json.dumps(derived, indent=2))
body_path.write_text(body_html)
PY

BODY_HTML="$(cat "${WORK}/body.html")"
cp "${WORK}/body.html" "$BODY_HTML_OUT"

ROW_COUNT="$(jq -r '.row_count' "${WORK}/derived.json")"
USE_TYPE_OPTION="$(jq -r '.use_type_option' "${WORK}/derived.json")"
PRODUCT_OPTIONS_JSON="$(jq -c '.product_options' "${WORK}/derived.json")"
OPTION_NAMES_JSON="$(jq -c '.option_names' "${WORK}/derived.json")"
OPTION_REORDER_JSON="$(jq -c '[.option_axes[] | {name: .name, values: (.values | map({name: .}))}]' "${WORK}/derived.json")"
VARIANTS_JSON="$(jq -c '.variants' "${WORK}/derived.json")"
DERIVED_SKUS_SORTED="$(jq -r '.derived_skus_sorted[]' "${WORK}/derived.json")"
TAGS_JSON="$(jq -c '.tags' "${WORK}/derived.json")"
SHOPIFY_SIZE_REFS_JSON="$(jq -c '.shopify_size_refs' "${WORK}/derived.json")"

AGE_GROUP_GIDS_JSON='["gid://shopify/Metaobject/128116523105","gid://shopify/Metaobject/128116490337"]'
COLOR_PATTERN_GIDS_JSON='["gid://shopify/Metaobject/69639766113","gid://shopify/Metaobject/69639733345"]'
TARGET_GENDER_GIDS_JSON='["gid://shopify/Metaobject/129971617889"]'
CARE_INSTRUCTIONS_GIDS_JSON='["gid://shopify/Metaobject/130283503713"]'
FABRIC_GIDS_JSON='["gid://shopify/Metaobject/69622399073"]'
TOP_LENGTH_GIDS_JSON='["gid://shopify/Metaobject/130282553441"]'

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
    metafields(first: 120, namespace: "shopify") {
      nodes {
        namespace
        key
        type
        value
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
    product {
      id
      handle
      title
    }
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
  if [[ "$USE_TYPE_OPTION" == "true" ]]; then
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
  else
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
    updates.append({
        "id": node["id"],
        "price": spec["price"],
        "compareAtPrice": spec["compareAtPrice"],
        "inventoryPolicy": "DENY",
    })
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
  --arg fabric_value "$(echo "$FABRIC_GIDS_JSON" | jq -c .)" \
  --arg target_gender_value "$(echo "$TARGET_GENDER_GIDS_JSON" | jq -c .)" \
  --arg size_value "$(echo "$SHOPIFY_SIZE_REFS_JSON" | jq -c .)" \
  --arg top_length_value "$(echo "$TOP_LENGTH_GIDS_JSON" | jq -c .)" \
  --arg merch_subcategory "$MERCH_SUBCATEGORY" \
  --arg merch_subcategory2 "$MERCH_SUBCATEGORY2" \
  --arg merch_style "$MERCH_STYLE" \
  --arg merch_type "$MERCH_TYPE" \
  --arg seo_title "$SEO_TITLE" \
  --arg seo_description "$SEO_DESCRIPTION" '
  [
      {ownerId: $pid, namespace: "custom", key: "category1", type: "single_line_text_field", value: "Mommy and Me"},
      {ownerId: $pid, namespace: "custom", key: "subcategory", type: "single_line_text_field", value: $merch_subcategory},
      {ownerId: $pid, namespace: "custom", key: "subcategory2", type: "single_line_text_field", value: $merch_subcategory2},
      {ownerId: $pid, namespace: "custom", key: "pattern", type: "single_line_text_field", value: "Powder Blue Eyelet"},
      {ownerId: $pid, namespace: "custom", key: "style", type: "single_line_text_field", value: $merch_style},
      {ownerId: $pid, namespace: "custom", key: "type", type: "single_line_text_field", value: $merch_type},
      {ownerId: $pid, namespace: "mm-google-shopping", key: "custom_product", type: "boolean", value: "false"},
      {ownerId: $pid, namespace: "mm-google-shopping", key: "gender", type: "single_line_text_field", value: "female"},
      {ownerId: $pid, namespace: "mm-google-shopping", key: "age_group", type: "single_line_text_field", value: "adult"},
      {ownerId: $pid, namespace: "mm-google-shopping", key: "condition", type: "single_line_text_field", value: "new"},
      {ownerId: $pid, namespace: "mm-google-shopping", key: "custom_label_0", type: "single_line_text_field", value: "Mommy and Me"},
      {ownerId: $pid, namespace: "mm-google-shopping", key: "custom_label_1", type: "single_line_text_field", value: "Powder Blue"},
      {ownerId: $pid, namespace: "mm-google-shopping", key: "custom_label_2", type: "single_line_text_field", value: "Summer"},
      {ownerId: $pid, namespace: "mm-google-shopping", key: "custom_label_3", type: "single_line_text_field", value: "Flutter Top & Eyelet Pants"},
      {ownerId: $pid, namespace: "mm-google-shopping", key: "custom_label_4", type: "single_line_text_field", value: "Two-Role Matching"},
      {ownerId: $pid, namespace: "shopify", key: "age-group", type: "list.metaobject_reference", value: $age_group_value},
      {ownerId: $pid, namespace: "shopify", key: "care-instructions", type: "list.metaobject_reference", value: $care_instructions_value},
      {ownerId: $pid, namespace: "shopify", key: "color-pattern", type: "list.metaobject_reference", value: $color_value},
      {ownerId: $pid, namespace: "shopify", key: "fabric", type: "list.metaobject_reference", value: $fabric_value},
      {ownerId: $pid, namespace: "shopify", key: "size", type: "list.metaobject_reference", value: $size_value},
      {ownerId: $pid, namespace: "shopify", key: "target-gender", type: "list.metaobject_reference", value: $target_gender_value},
      {ownerId: $pid, namespace: "shopify", key: "top-length-type", type: "list.metaobject_reference", value: $top_length_value},
      {ownerId: $pid, namespace: "global", key: "title_tag", type: "single_line_text_field", value: $seo_title},
      {ownerId: $pid, namespace: "global", key: "description_tag", type: "single_line_text_field", value: $seo_description}
  ]')"

while IFS= read -r metafields_batch; do
  METAFIELDS_SET_RESPONSE="$(gql "$METAFIELDS_SET_MUTATION" "$(jq -nc --argjson metafields "$metafields_batch" '{metafields: $metafields}')")"
  check_graphql_errors "$METAFIELDS_SET_RESPONSE" "metafieldsSet"
  check_user_errors "$METAFIELDS_SET_RESPONSE" '.data.metafieldsSet.userErrors' "metafieldsSet"
done < <(echo "$METAFIELDS_JSON" | jq -c '. as $all | [range(0; length; 25) as $i | $all[$i:($i + 25)]][]')

STALE_SHOPIFY_METAFIELDS_TO_DELETE_JSON="$(python3 - "${WORK}/existing.json" "$PRODUCT_ID" <<'PY'
import json
import sys

existing = json.load(open(sys.argv[1]))
product_id = sys.argv[2]
keys_to_delete = {"dress-occasion", "dress-style", "skirt-dress-length-type"}
delete_list = []
product = existing.get("data", {}).get("productByHandle") or {}
for node in product.get("metafields", {}).get("nodes", []):
    if node["key"] in keys_to_delete:
        delete_list.append({
            "ownerId": product_id,
            "namespace": "shopify",
            "key": node["key"],
        })
print(json.dumps(delete_list))
PY
)"

if [[ "$STALE_SHOPIFY_METAFIELDS_TO_DELETE_JSON" != "[]" ]]; then
  METAFIELDS_DELETE_MUTATION='mutation MetafieldsDelete($metafields: [MetafieldIdentifierInput!]!) {
    metafieldsDelete(metafields: $metafields) {
      deletedMetafields { key namespace ownerId }
      userErrors { field message }
    }
  }'

  METAFIELDS_DELETE_RESPONSE="$(gql "$METAFIELDS_DELETE_MUTATION" "$(jq -nc --argjson metafields "$STALE_SHOPIFY_METAFIELDS_TO_DELETE_JSON" '{metafields: $metafields}')")"
  check_graphql_errors "$METAFIELDS_DELETE_RESPONSE" "metafieldsDelete"
  check_user_errors "$METAFIELDS_DELETE_RESPONSE" '.data.metafieldsDelete.userErrors' "metafieldsDelete"
fi

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
      alt_text="Mother and daughter in a powder blue matching flutter top and white eyelet pants set by the water."
      ;;
    02-*)
      alt_text="Mommy-and-me powder blue summer set with airy ruffle top and white eyelet wide-leg pants in bright seaside light."
      ;;
    03-*)
      alt_text="Back view of the girls' powder blue flutter top and white eyelet pants matching set on a boardwalk."
      ;;
    04-*)
      alt_text="Rear view of the powder blue sleeveless top and white scalloped eyelet pants from the mommy-and-me set."
      ;;
    *)
      alt_text="Powder blue mommy-and-me flutter top with white eyelet pants set for mother and daughter."
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
        title
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

for _attempt in {1..12}; do
  if echo "$VERIFY_RESPONSE" | jq -e '.data.product.collections.nodes | map(.handle) | index("dresses") != null' > /dev/null; then
    break
  fi
  sleep 3
  VERIFY_RESPONSE="$(gql "$VERIFY_QUERY" "$(jq -nc --arg id "$PRODUCT_ID" '{id:$id}')")"
  check_graphql_errors "$VERIFY_RESPONSE" "verify query"
done

echo "$VERIFY_RESPONSE" > "$VERIFY_JSON_OUT"

python3 - "$VERIFY_JSON_OUT" "${WORK}/derived.json" "${WORK}/size_chart.json" "${WORK}/size_metaobject_map.json" \
  "$LISTING_MD" "$CSV_OUT" "$CSV_HEADER_SOURCE" "$HANDLE" "$TITLE" "$SEO_TITLE" "$SEO_DESCRIPTION" \
  "$PRICE_NEIGHBOR_HANDLE" "$SIZE_NEIGHBOR_HANDLE" "$CHILD_PRICE" "$CHILD_COMPARE" "$MOTHER_PRICE" "$MOTHER_COMPARE" \
  "$VENDOR_URL" "$SCRIPT_PATH" "$SIZE_CHART_OUT" "$BODY_HTML_OUT" "$UPLOAD_DIR" "$PRODUCT_ID" \
  "$EXPECTED_TAXONOMY_FULL_NAME" "$MERCH_SUBCATEGORY" "$MERCH_SUBCATEGORY2" "$MERCH_STYLE" "$MERCH_TYPE" "$MERCH_COLLECTION_TAG" <<'PY'
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
expected_taxonomy_full_name = sys.argv[24]
merch_subcategory = sys.argv[25]
merch_subcategory2 = sys.argv[26]
merch_style = sys.argv[27]
merch_type = sys.argv[28]
merch_collection_tag = sys.argv[29]

verify = json.loads(verify_path.read_text())
derived = json.loads(derived_path.read_text())
chart = json.loads(chart_path.read_text())
size_map = {row["picker_label"]: row for row in json.loads(size_map_path.read_text())}
product = verify["data"]["product"]
product_options = product["options"]
variants = product["variants"]["nodes"]
metafields = product["metafields"]["nodes"]
collections = product["collections"]["nodes"]
publications = product["resourcePublicationsV2"]["nodes"]
collection_handles = {collection["handle"] for collection in collections}

spec_by_sku = {row["sku"]: row for row in derived["recap"]}
live_skus_sorted = sorted(v["sku"] for v in variants)
derived_skus_sorted = derived["derived_skus_sorted"]
option_names = derived["option_names"]
option_axes = derived["option_axes"]
expected_option_pairs = {tuple(pair) for pair in derived["expected_variant_option_pairs"]}
live_option_names = [option["name"] for option in product_options]

html_body = product["descriptionHtml"]
th_count = len(re.findall(r"<th>", html_body))
tr_count = len(re.findall(r"<tr>", html_body))
tbody_match = re.search(r"<tbody>(.*?)</tbody>", html_body, re.S)
tbody_rows = re.findall(r"<tr>(.*?)</tr>", tbody_match.group(1), re.S) if tbody_match else []
first_cells = []
for row_html in tbody_rows:
    cell = re.search(r"<td>(.*?)</td>", row_html, re.S)
    first_cells.append(re.sub(r"<.*?>", "", cell.group(1)).strip() if cell else "")

expected_first_cells = [row["picker_label"] for row in chart]
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
    ("Each size table has 10 headers", th_count == 10, str(th_count)),
    ("Table row count matches SIZE_CHART", len(tbody_rows) == len(chart), str(len(tbody_rows))),
    ("publishedAt is populated", bool(product["publishedAt"]), product["publishedAt"] or ""),
    ("onlineStoreUrl is populated", bool(product["onlineStoreUrl"]), product["onlineStoreUrl"] or ""),
    ("Taxonomy category is set", product["category"]["id"] == "gid://shopify/TaxonomyCategory/aa-1-11", product["category"]["id"]),
    ("Taxonomy category full name matches expected leaf", product["category"]["fullName"] == expected_taxonomy_full_name, product["category"]["fullName"]),
    ("Dress merchandising tag is present", merch_collection_tag in product["tags"], ", ".join(product["tags"])),
    ("Dress smart collection is attached", "dresses" in collection_handles, str(sorted(collection_handles))),
    ("Required publications are live", expected_publications.issubset(published_ids), str(sorted(published_ids))),
]

price_rows = []
price_drift = False
for variant in variants:
    spec = spec_by_sku[variant["sku"]]
    price_ok = variant["price"] == spec["price"]
    cmp_ok = variant["compareAtPrice"] == spec["compare_at_price"]
    tracked_ok = variant["inventoryItem"]["tracked"] and variant["inventoryItem"]["requiresShipping"]
    deny_ok = variant["inventoryPolicy"] == "DENY"
    if not (price_ok and cmp_ok and tracked_ok and deny_ok):
        price_drift = True
    price_rows.append({
        "sku": variant["sku"],
        "live_price": variant["price"],
        "live_compare": variant["compareAtPrice"],
        "spec_price": spec["price"],
        "spec_compare": spec["compare_at_price"],
        "match": "✓" if (price_ok and cmp_ok and tracked_ok and deny_ok) else "✗",
    })

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
    ("shopify", "care-instructions"),
    ("shopify", "color-pattern"),
    ("shopify", "fabric"),
    ("shopify", "size"),
    ("shopify", "target-gender"),
    ("shopify", "top-length-type"),
    ("global", "title_tag"),
    ("global", "description_tag"),
}
checks.append(("Applicable metafields are written", required_written.issubset(metafield_keys), str(sorted(required_written - metafield_keys))))

skipped_metafields = {
    "shopify.clothing-features": "The current store catalog only exposes values like `Insulated` in this standard metafield namespace, which would be inaccurate for this lightweight summer outfit set.",
    "shopify.dress-occasion": "Removed if present because the honest Shopify taxonomy for this product remains `Outfit Sets` even though the storefront merchandising override places it under dresses.",
    "shopify.dress-style": "Not applicable because the honest Shopify taxonomy for this product remains `Outfit Sets`, not `Dresses`.",
    "shopify.fit": "The Outfit Sets taxonomy exposes fit, but no writable standard Shopify metafield definition is currently available in this store for that attribute.",
    "shopify.neckline": "The images support a square neckline, but Shopify currently rejects this standard metafield for the `Outfit Sets` owner subtype through the Admin API in this store.",
    "shopify.pants-length-type": "The pants are visibly full length, but no writable standard Shopify metafield definition is currently available in this store for that attribute.",
    "shopify.skirt-dress-length-type": "Not applicable because the honest Shopify taxonomy for this product remains `Outfit Sets`, not `Dresses`.",
    "shopify.sleeve-length-type": "The images support a sleeveless / spaghetti-strap top, but Shopify currently rejects this standard metafield for the `Outfit Sets` owner subtype through the Admin API in this store.",
    "shopify.waist-rise": "The waistband sits around the natural waist visually, but no writable standard Shopify metafield definition is currently available in this store for that attribute.",
}

written_metafields = []
for node in metafields:
    if node["namespace"] in {"custom", "mm-google-shopping", "shopify", "global"}:
        written_metafields.append(node)

links = {
    "admin": f"https://admin.shopify.com/store/dresslikemommy/products/{product_gid.split('/')[-1]}",
    "live": product["onlineStoreUrl"],
}

csv_rows = []
for recap in derived["recap"]:
    row = {header: "" for header in next(csv.reader([csv_header_source.read_text().splitlines()[0]]))}
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
    put("Google Shopping / Custom Label 1", "Powder Blue")
    put("Google Shopping / Custom Label 2", "Summer")
    put("Google Shopping / Custom Label 3", "Flutter Top & Eyelet Pants")
    put("Google Shopping / Custom Label 4", "Two-Role Matching")
    put("Category1 (product.metafields.custom.category1)", "Mommy and Me")
    put("Pattern (product.metafields.custom.pattern)", "Powder Blue Eyelet")
    put("Style (product.metafields.custom.style)", merch_style)
    put("SubCategory (product.metafields.custom.subcategory)", merch_subcategory)
    put("SubCategory2 (product.metafields.custom.subcategory2)", merch_subcategory2)
    put("Type (product.metafields.custom.type)", merch_type)
    put("Google: Custom Product (product.metafields.mm-google-shopping.custom_product)", "false")
    put("Age group (product.metafields.shopify.age-group)", "kids, adults")
    put("Color (product.metafields.shopify.color-pattern)", "Blue, White")
    put("Size (product.metafields.shopify.size)", ", ".join(x["picker_label"] for x in derived["recap"]))
    put("Target Gender (product.metafields.shopify.target-gender)", "Female")
    put("Status", "active")
    csv_rows.append(row)

with csv_header_source.open(newline="") as fh:
    header = next(csv.reader(fh))

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
lines.append("| PRIMARY_CATEGORY | auto → Dresses (storefront merchandising override; Shopify taxonomy kept as Outfit Sets) |")
lines.append("| DESIGNS_TO_LIST | auto → Powder Blue only |")
lines.append("| EXCLUDE_ITEMS | none |")
lines.append("| SHORTCODE | auto → `PBLU` |")
lines.append("| COLOR_TOKEN | auto → `BLUE` |")
lines.append("| FORCE_SPEC_PRICES | true |")
lines.append("")
lines.append("## Vendor fetch status")
lines.append("The direct 1688 page was captcha-blocked during this run, so the attached size-chart image was used as the authoritative source of truth for variants. The supplied lifestyle images show a powder-blue flutter top paired with white eyelet wide-leg pants for mother and daughter. Neighbor pricing was anchored to `blue-striped-family-matching-set`, size metaobject GIDs were anchored to `white-lace-mommy-and-me-dresses`, the Shopify taxonomy stays `Outfit Sets` for honest standard-category attributes, and the storefront merchandising fields were intentionally overridden to `Dresses` plus the `Sundresses` tag so this listing can surface under dresses and use the dress pill.")
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
lines.append("- `chest_cm` and `hip_cm` were derived from standard loose summer set grading because the vendor chart only publishes top-drop, pant length, and waist.")
lines.append("- `weight` and `height` use the store's standard child and mother size guidance for the mapped picker labels.")
lines.append("- The vendor column labeled `吊带（肩带可调节）` was interpreted as the garment drop/visible top length because the 44–74 cm range aligns with the supplied photos; that published value is reused for both `skirt_cm` and `length_cm` to preserve the vendor evidence without inventing a second unsupported top-length field.")
lines.append("")
lines.append("### Vendor → picker mapping log")
lines.append("- 100 → Child 3 Years")
lines.append("- 110 → Child 4 Years")
lines.append("- 120 → Child 5 Years")
lines.append("- 130 → Child 6-7 Years")
lines.append("- 140 → Child 8 Years")
lines.append("- 150 → Child 9-10 Years")
lines.append("- S → Mother S")
lines.append("- M → Mother M")
lines.append("")
lines.append("### EXCLUDE_ITEMS decisions")
lines.append("- No exclusions were requested, so every vendor-supported row in the attached chart was kept.")
lines.append("")
lines.append("## Body HTML")
lines.append("- 1 `<ul>` with 6 bullets (fabric, family story, print, design details, care, size range).")
lines.append("- 1 `<h3>` + 1 size table with 10 `<th>` headers and 8 body rows.")
lines.append("- 2 narrative paragraphs, 1 key-features block, and 1 closing CTA paragraph.")
lines.append("")
lines.append("## Option axes & variants")
for index, axis in enumerate(option_axes, start=1):
    values = ", ".join(f"`{value}`" for value in axis["values"])
    lines.append(f"- Option {index}: `{axis['name']}` → {values}")
lines.append(f"- Variants live: **{len(variants)}**")
lines.append("")
lines.append("## Verify pass table")
lines.append("| Check | Result | Detail |")
lines.append("|---|---|---|")
for label, ok, detail in checks:
    lines.append(f"| {label} | {'✅' if ok else '❌'} | {detail} |")
lines.append("")
lines.append("## Price parity (FORCE_SPEC_PRICES=true)")
lines.append("| SKU | Live Price | Live Cmp | Spec Price | Spec Cmp | Match |")
lines.append("|---|---|---|---|---|---|")
for row in price_rows:
    lines.append(f"| {row['sku']} | {row['live_price']} | {row['live_compare']} | {row['spec_price']} | {row['spec_compare']} | {row['match']} |")
lines.append("")
lines.append("## Metafields — written")
lines.append("| Namespace.Key | Type | Value |")
lines.append("|---|---|---|")
for node in sorted(written_metafields, key=lambda x: (x["namespace"], x["key"])):
    value = node["value"]
    if len(value) > 90:
        value = value[:87] + "..."
    lines.append(f"| {node['namespace']}.{node['key']} | {node['type']} | `{value}` |")
lines.append("")
lines.append("## Metafields — skipped")
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
    lines.append("- No smart collections were attached in the immediate verification query; Shopify reindex may still be pending.")
lines.append("")
lines.append("## Manual follow-ups")
lines.append("- Inventory quantities and per-variant grams still need operator stock values.")
lines.append("- If Shopify exposes writable standard metafields for `fit`, `pants-length-type`, or `waist-rise` in this store later, extend the runner to write the already-inferred outfit-set attributes too.")
if not collections:
    lines.append("- Re-check smart collection attachment after Shopify reindex if merchandising placement matters immediately.")
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
lines.append(f"- Neighbor pricing: `{price_neighbor_handle}`")
lines.append(f"- Size metaobject map: `{size_neighbor_handle}`")

listing_md_path.write_text("\n".join(lines) + "\n")

failed = [label for label, ok, _detail in checks if not ok]
if price_drift:
    failed.append("Price parity")
if failed:
    raise SystemExit("VERIFY FAILED: " + ", ".join(failed))
PY

echo "Admin URL: https://admin.shopify.com/store/dresslikemommy/products/${PRODUCT_ID##*/}"
echo "Live URL: https://www.dresslikemommy.com/products/${HANDLE}"
echo "Listing log: ${LISTING_MD}"
echo "CSV backup: ${CSV_OUT}"
