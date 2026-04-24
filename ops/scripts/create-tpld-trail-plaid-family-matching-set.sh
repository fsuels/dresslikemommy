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

HANDLE="trail-plaid-family-matching-set"
TITLE="Trail Plaid Family Matching Set — Hooded Sun Shirt & Cargo Shorts"
SEO_TITLE="Trail Plaid Family Matching Set | Dress Like Mommy"
SEO_DESCRIPTION="Lightweight family matching set with a hooded plaid sun shirt and gray-green cargo shorts for moms, dads, girls & boys. Sizes 1-2Y–3XL."
PRINT_NAME="Trail Plaid"
SHORTCODE="TPLD"
COLOR_TOKEN="OLIVE"
COLOR_NAME="Trail Plaid"
LISTING_MODE="Family Matching"
CATEGORY="FamilySet"
CATEGORY_WORD="Set"
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
VENDOR_URL="https://detail.1688.com/offer/1034690588459.html"
VENDOR="dresslikemommy.com"
FORCE_SPEC_PRICES="true"
CHILD_PRICE="28.99"
MOTHER_PRICE="31.99"
PRICE_NEIGHBOR_HANDLE="blue-striped-family-matching-set"
SIZE_NEIGHBOR_HANDLE="blue-striped-family-matching-set"

SCRIPT_PATH="${ROOT}/ops/scripts/create-tpld-trail-plaid-family-matching-set.sh"
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
  {"audience":"child","role":"Girl Shirt","garment":"Shirt","vendor_label":"80","picker_label":"Girl 1-2 Years","sku_suffix":"KID12Y","age":"1-2","weight":"9-11.5 kg","height":"75-85 cm","chest_cm":70,"hip_cm":74,"waist_cm":70,"length_cm":36,"sleeve_cm":25,"pant_cm":0},
  {"audience":"child","role":"Girl Shirt","garment":"Shirt","vendor_label":"90","picker_label":"Girl 2 Years","sku_suffix":"KID2Y","age":"2","weight":"12-14.5 kg","height":"86-95 cm","chest_cm":76,"hip_cm":80,"waist_cm":76,"length_cm":39,"sleeve_cm":28,"pant_cm":0},
  {"audience":"child","role":"Girl Shirt","garment":"Shirt","vendor_label":"100","picker_label":"Girl 3 Years","sku_suffix":"KID3Y","age":"3","weight":"15-17.5 kg","height":"96-105 cm","chest_cm":82,"hip_cm":86,"waist_cm":82,"length_cm":42,"sleeve_cm":31,"pant_cm":0},
  {"audience":"child","role":"Girl Shirt","garment":"Shirt","vendor_label":"110","picker_label":"Girl 4 Years","sku_suffix":"KID4Y","age":"4","weight":"18-20 kg","height":"106-115 cm","chest_cm":86,"hip_cm":90,"waist_cm":86,"length_cm":45,"sleeve_cm":34,"pant_cm":0},
  {"audience":"child","role":"Girl Shirt","garment":"Shirt","vendor_label":"120","picker_label":"Girl 5 Years","sku_suffix":"KID5Y","age":"5","weight":"20.5-22.5 kg","height":"116-125 cm","chest_cm":88,"hip_cm":92,"waist_cm":88,"length_cm":48,"sleeve_cm":36,"pant_cm":0},
  {"audience":"child","role":"Girl Shirt","garment":"Shirt","vendor_label":"130","picker_label":"Girl 6-7 Years","sku_suffix":"KID67Y","age":"6-7","weight":"23-25 kg","height":"126-135 cm","chest_cm":90,"hip_cm":94,"waist_cm":90,"length_cm":50,"sleeve_cm":39,"pant_cm":0},
  {"audience":"child","role":"Girl Shirt","garment":"Shirt","vendor_label":"140","picker_label":"Girl 8 Years","sku_suffix":"KID8Y","age":"8","weight":"25.5-30 kg","height":"136-145 cm","chest_cm":92,"hip_cm":96,"waist_cm":92,"length_cm":52,"sleeve_cm":42,"pant_cm":0},
  {"audience":"child","role":"Girl Shirt","garment":"Shirt","vendor_label":"150","picker_label":"Girl 9-10 Years","sku_suffix":"KID910Y","age":"9-10","weight":"30.5-40 kg","height":"145-155 cm","chest_cm":96,"hip_cm":100,"waist_cm":96,"length_cm":55,"sleeve_cm":45,"pant_cm":0},
  {"audience":"child","role":"Boy Shirt","garment":"Shirt","vendor_label":"80","picker_label":"Boy 1-2 Years","sku_suffix":"KID12Y","age":"1-2","weight":"9-11.5 kg","height":"75-85 cm","chest_cm":70,"hip_cm":74,"waist_cm":70,"length_cm":36,"sleeve_cm":25,"pant_cm":0},
  {"audience":"child","role":"Boy Shirt","garment":"Shirt","vendor_label":"90","picker_label":"Boy 2 Years","sku_suffix":"KID2Y","age":"2","weight":"12-14.5 kg","height":"86-95 cm","chest_cm":76,"hip_cm":80,"waist_cm":76,"length_cm":39,"sleeve_cm":28,"pant_cm":0},
  {"audience":"child","role":"Boy Shirt","garment":"Shirt","vendor_label":"100","picker_label":"Boy 3 Years","sku_suffix":"KID3Y","age":"3","weight":"15-17.5 kg","height":"96-105 cm","chest_cm":82,"hip_cm":86,"waist_cm":82,"length_cm":42,"sleeve_cm":31,"pant_cm":0},
  {"audience":"child","role":"Boy Shirt","garment":"Shirt","vendor_label":"110","picker_label":"Boy 4 Years","sku_suffix":"KID4Y","age":"4","weight":"18-20 kg","height":"106-115 cm","chest_cm":86,"hip_cm":90,"waist_cm":86,"length_cm":45,"sleeve_cm":34,"pant_cm":0},
  {"audience":"child","role":"Boy Shirt","garment":"Shirt","vendor_label":"120","picker_label":"Boy 5 Years","sku_suffix":"KID5Y","age":"5","weight":"20.5-22.5 kg","height":"116-125 cm","chest_cm":88,"hip_cm":92,"waist_cm":88,"length_cm":48,"sleeve_cm":36,"pant_cm":0},
  {"audience":"child","role":"Boy Shirt","garment":"Shirt","vendor_label":"130","picker_label":"Boy 6-7 Years","sku_suffix":"KID67Y","age":"6-7","weight":"23-25 kg","height":"126-135 cm","chest_cm":90,"hip_cm":94,"waist_cm":90,"length_cm":50,"sleeve_cm":39,"pant_cm":0},
  {"audience":"child","role":"Boy Shirt","garment":"Shirt","vendor_label":"140","picker_label":"Boy 8 Years","sku_suffix":"KID8Y","age":"8","weight":"25.5-30 kg","height":"136-145 cm","chest_cm":92,"hip_cm":96,"waist_cm":92,"length_cm":52,"sleeve_cm":42,"pant_cm":0},
  {"audience":"child","role":"Boy Shirt","garment":"Shirt","vendor_label":"150","picker_label":"Boy 9-10 Years","sku_suffix":"KID910Y","age":"9-10","weight":"30.5-40 kg","height":"145-155 cm","chest_cm":96,"hip_cm":100,"waist_cm":96,"length_cm":55,"sleeve_cm":45,"pant_cm":0},
  {"audience":"mother","role":"Mother Shirt","garment":"Shirt","vendor_label":"S","picker_label":"Mother S","sku_suffix":"S","age":"—","weight":"47.5-57.5 kg","height":"—","chest_cm":104,"hip_cm":104,"waist_cm":92,"length_cm":65,"sleeve_cm":50,"pant_cm":0},
  {"audience":"mother","role":"Mother Shirt","garment":"Shirt","vendor_label":"M","picker_label":"Mother M","sku_suffix":"M","age":"—","weight":"58-62.5 kg","height":"—","chest_cm":106,"hip_cm":106,"waist_cm":94,"length_cm":66,"sleeve_cm":52,"pant_cm":0},
  {"audience":"mother","role":"Mother Shirt","garment":"Shirt","vendor_label":"L","picker_label":"Mother L","sku_suffix":"L","age":"—","weight":"63-69.5 kg","height":"—","chest_cm":110,"hip_cm":110,"waist_cm":98,"length_cm":67,"sleeve_cm":53,"pant_cm":0},
  {"audience":"mother","role":"Mother Shirt","garment":"Shirt","vendor_label":"XL","picker_label":"Mother XL","sku_suffix":"XL","age":"—","weight":"70-77.5 kg","height":"—","chest_cm":114,"hip_cm":114,"waist_cm":102,"length_cm":69,"sleeve_cm":54,"pant_cm":0},
  {"audience":"mother","role":"Mother Shirt","garment":"Shirt","vendor_label":"XXL","picker_label":"Mother 2XL","sku_suffix":"2XL","age":"—","weight":"78-85 kg","height":"—","chest_cm":118,"hip_cm":118,"waist_cm":106,"length_cm":71,"sleeve_cm":55,"pant_cm":0},
  {"audience":"mother","role":"Mother Shirt","garment":"Shirt","vendor_label":"3XL","picker_label":"Mother 3XL","sku_suffix":"3XL","age":"—","weight":"85.5-95 kg","height":"—","chest_cm":122,"hip_cm":122,"waist_cm":110,"length_cm":74,"sleeve_cm":56,"pant_cm":0},
  {"audience":"father","role":"Father Shirt","garment":"Shirt","vendor_label":"S","picker_label":"Father S","sku_suffix":"S","age":"—","weight":"47.5-57.5 kg","height":"—","chest_cm":104,"hip_cm":104,"waist_cm":92,"length_cm":65,"sleeve_cm":50,"pant_cm":0},
  {"audience":"father","role":"Father Shirt","garment":"Shirt","vendor_label":"M","picker_label":"Father M","sku_suffix":"M","age":"—","weight":"58-62.5 kg","height":"—","chest_cm":106,"hip_cm":106,"waist_cm":94,"length_cm":66,"sleeve_cm":52,"pant_cm":0},
  {"audience":"father","role":"Father Shirt","garment":"Shirt","vendor_label":"L","picker_label":"Father L","sku_suffix":"L","age":"—","weight":"63-69.5 kg","height":"—","chest_cm":110,"hip_cm":110,"waist_cm":98,"length_cm":67,"sleeve_cm":53,"pant_cm":0},
  {"audience":"father","role":"Father Shirt","garment":"Shirt","vendor_label":"XL","picker_label":"Father XL","sku_suffix":"XL","age":"—","weight":"70-77.5 kg","height":"—","chest_cm":114,"hip_cm":114,"waist_cm":102,"length_cm":69,"sleeve_cm":54,"pant_cm":0},
  {"audience":"father","role":"Father Shirt","garment":"Shirt","vendor_label":"XXL","picker_label":"Father 2XL","sku_suffix":"2XL","age":"—","weight":"78-85 kg","height":"—","chest_cm":118,"hip_cm":118,"waist_cm":106,"length_cm":71,"sleeve_cm":55,"pant_cm":0},
  {"audience":"father","role":"Father Shirt","garment":"Shirt","vendor_label":"3XL","picker_label":"Father 3XL","sku_suffix":"3XL","age":"—","weight":"85.5-95 kg","height":"—","chest_cm":122,"hip_cm":122,"waist_cm":110,"length_cm":74,"sleeve_cm":56,"pant_cm":0},
  {"audience":"child","role":"Girl Shorts","garment":"Shorts","vendor_label":"80","picker_label":"Girl 1-2 Years","sku_suffix":"KID12Y","age":"1-2","weight":"9-11.5 kg","height":"75-85 cm","chest_cm":0,"hip_cm":76,"waist_cm":44,"length_cm":29,"sleeve_cm":0,"pant_cm":29},
  {"audience":"child","role":"Girl Shorts","garment":"Shorts","vendor_label":"90","picker_label":"Girl 2 Years","sku_suffix":"KID2Y","age":"2","weight":"12-14.5 kg","height":"86-95 cm","chest_cm":0,"hip_cm":80,"waist_cm":46,"length_cm":32,"sleeve_cm":0,"pant_cm":32},
  {"audience":"child","role":"Girl Shorts","garment":"Shorts","vendor_label":"100","picker_label":"Girl 3 Years","sku_suffix":"KID3Y","age":"3","weight":"15-17.5 kg","height":"96-105 cm","chest_cm":0,"hip_cm":84,"waist_cm":49,"length_cm":35,"sleeve_cm":0,"pant_cm":35},
  {"audience":"child","role":"Girl Shorts","garment":"Shorts","vendor_label":"110","picker_label":"Girl 4 Years","sku_suffix":"KID4Y","age":"4","weight":"18-20 kg","height":"106-115 cm","chest_cm":0,"hip_cm":88,"waist_cm":52,"length_cm":38,"sleeve_cm":0,"pant_cm":38},
  {"audience":"child","role":"Girl Shorts","garment":"Shorts","vendor_label":"120","picker_label":"Girl 5 Years","sku_suffix":"KID5Y","age":"5","weight":"20.5-22.5 kg","height":"116-125 cm","chest_cm":0,"hip_cm":92,"waist_cm":55,"length_cm":41,"sleeve_cm":0,"pant_cm":41},
  {"audience":"child","role":"Girl Shorts","garment":"Shorts","vendor_label":"130","picker_label":"Girl 6-7 Years","sku_suffix":"KID67Y","age":"6-7","weight":"23-25 kg","height":"126-135 cm","chest_cm":0,"hip_cm":96,"waist_cm":58,"length_cm":44,"sleeve_cm":0,"pant_cm":44},
  {"audience":"child","role":"Girl Shorts","garment":"Shorts","vendor_label":"140","picker_label":"Girl 8 Years","sku_suffix":"KID8Y","age":"8","weight":"25.5-30 kg","height":"136-145 cm","chest_cm":0,"hip_cm":100,"waist_cm":61,"length_cm":47,"sleeve_cm":0,"pant_cm":47},
  {"audience":"child","role":"Girl Shorts","garment":"Shorts","vendor_label":"150","picker_label":"Girl 9-10 Years","sku_suffix":"KID910Y","age":"9-10","weight":"30.5-40 kg","height":"145-155 cm","chest_cm":0,"hip_cm":104,"waist_cm":64,"length_cm":50,"sleeve_cm":0,"pant_cm":50},
  {"audience":"child","role":"Boy Shorts","garment":"Shorts","vendor_label":"80","picker_label":"Boy 1-2 Years","sku_suffix":"KID12Y","age":"1-2","weight":"9-11.5 kg","height":"75-85 cm","chest_cm":0,"hip_cm":76,"waist_cm":44,"length_cm":29,"sleeve_cm":0,"pant_cm":29},
  {"audience":"child","role":"Boy Shorts","garment":"Shorts","vendor_label":"90","picker_label":"Boy 2 Years","sku_suffix":"KID2Y","age":"2","weight":"12-14.5 kg","height":"86-95 cm","chest_cm":0,"hip_cm":80,"waist_cm":46,"length_cm":32,"sleeve_cm":0,"pant_cm":32},
  {"audience":"child","role":"Boy Shorts","garment":"Shorts","vendor_label":"100","picker_label":"Boy 3 Years","sku_suffix":"KID3Y","age":"3","weight":"15-17.5 kg","height":"96-105 cm","chest_cm":0,"hip_cm":84,"waist_cm":49,"length_cm":35,"sleeve_cm":0,"pant_cm":35},
  {"audience":"child","role":"Boy Shorts","garment":"Shorts","vendor_label":"110","picker_label":"Boy 4 Years","sku_suffix":"KID4Y","age":"4","weight":"18-20 kg","height":"106-115 cm","chest_cm":0,"hip_cm":88,"waist_cm":52,"length_cm":38,"sleeve_cm":0,"pant_cm":38},
  {"audience":"child","role":"Boy Shorts","garment":"Shorts","vendor_label":"120","picker_label":"Boy 5 Years","sku_suffix":"KID5Y","age":"5","weight":"20.5-22.5 kg","height":"116-125 cm","chest_cm":0,"hip_cm":92,"waist_cm":55,"length_cm":41,"sleeve_cm":0,"pant_cm":41},
  {"audience":"child","role":"Boy Shorts","garment":"Shorts","vendor_label":"130","picker_label":"Boy 6-7 Years","sku_suffix":"KID67Y","age":"6-7","weight":"23-25 kg","height":"126-135 cm","chest_cm":0,"hip_cm":96,"waist_cm":58,"length_cm":44,"sleeve_cm":0,"pant_cm":44},
  {"audience":"child","role":"Boy Shorts","garment":"Shorts","vendor_label":"140","picker_label":"Boy 8 Years","sku_suffix":"KID8Y","age":"8","weight":"25.5-30 kg","height":"136-145 cm","chest_cm":0,"hip_cm":100,"waist_cm":61,"length_cm":47,"sleeve_cm":0,"pant_cm":47},
  {"audience":"child","role":"Boy Shorts","garment":"Shorts","vendor_label":"150","picker_label":"Boy 9-10 Years","sku_suffix":"KID910Y","age":"9-10","weight":"30.5-40 kg","height":"145-155 cm","chest_cm":0,"hip_cm":104,"waist_cm":64,"length_cm":50,"sleeve_cm":0,"pant_cm":50},
  {"audience":"mother","role":"Mother Shorts","garment":"Shorts","vendor_label":"S","picker_label":"Mother S","sku_suffix":"S","age":"—","weight":"47.5-57.5 kg","height":"—","chest_cm":0,"hip_cm":108,"waist_cm":68,"length_cm":56,"sleeve_cm":0,"pant_cm":56},
  {"audience":"mother","role":"Mother Shorts","garment":"Shorts","vendor_label":"M","picker_label":"Mother M","sku_suffix":"M","age":"—","weight":"58-62.5 kg","height":"—","chest_cm":0,"hip_cm":112,"waist_cm":72,"length_cm":57,"sleeve_cm":0,"pant_cm":57},
  {"audience":"mother","role":"Mother Shorts","garment":"Shorts","vendor_label":"L","picker_label":"Mother L","sku_suffix":"L","age":"—","weight":"63-69.5 kg","height":"—","chest_cm":0,"hip_cm":116,"waist_cm":76,"length_cm":58,"sleeve_cm":0,"pant_cm":58},
  {"audience":"mother","role":"Mother Shorts","garment":"Shorts","vendor_label":"XL","picker_label":"Mother XL","sku_suffix":"XL","age":"—","weight":"70-77.5 kg","height":"—","chest_cm":0,"hip_cm":120,"waist_cm":80,"length_cm":59,"sleeve_cm":0,"pant_cm":59},
  {"audience":"mother","role":"Mother Shorts","garment":"Shorts","vendor_label":"XXL","picker_label":"Mother 2XL","sku_suffix":"2XL","age":"—","weight":"78-85 kg","height":"—","chest_cm":0,"hip_cm":124,"waist_cm":84,"length_cm":60,"sleeve_cm":0,"pant_cm":60},
  {"audience":"mother","role":"Mother Shorts","garment":"Shorts","vendor_label":"3XL","picker_label":"Mother 3XL","sku_suffix":"3XL","age":"—","weight":"85.5-95 kg","height":"—","chest_cm":0,"hip_cm":128,"waist_cm":88,"length_cm":61,"sleeve_cm":0,"pant_cm":61},
  {"audience":"father","role":"Father Shorts","garment":"Shorts","vendor_label":"S","picker_label":"Father S","sku_suffix":"S","age":"—","weight":"47.5-57.5 kg","height":"—","chest_cm":0,"hip_cm":108,"waist_cm":68,"length_cm":56,"sleeve_cm":0,"pant_cm":56},
  {"audience":"father","role":"Father Shorts","garment":"Shorts","vendor_label":"M","picker_label":"Father M","sku_suffix":"M","age":"—","weight":"58-62.5 kg","height":"—","chest_cm":0,"hip_cm":112,"waist_cm":72,"length_cm":57,"sleeve_cm":0,"pant_cm":57},
  {"audience":"father","role":"Father Shorts","garment":"Shorts","vendor_label":"L","picker_label":"Father L","sku_suffix":"L","age":"—","weight":"63-69.5 kg","height":"—","chest_cm":0,"hip_cm":116,"waist_cm":76,"length_cm":58,"sleeve_cm":0,"pant_cm":58},
  {"audience":"father","role":"Father Shorts","garment":"Shorts","vendor_label":"XL","picker_label":"Father XL","sku_suffix":"XL","age":"—","weight":"70-77.5 kg","height":"—","chest_cm":0,"hip_cm":120,"waist_cm":80,"length_cm":59,"sleeve_cm":0,"pant_cm":59},
  {"audience":"father","role":"Father Shorts","garment":"Shorts","vendor_label":"XXL","picker_label":"Father 2XL","sku_suffix":"2XL","age":"—","weight":"78-85 kg","height":"—","chest_cm":0,"hip_cm":124,"waist_cm":84,"length_cm":60,"sleeve_cm":0,"pant_cm":60},
  {"audience":"father","role":"Father Shorts","garment":"Shorts","vendor_label":"3XL","picker_label":"Father 3XL","sku_suffix":"3XL","age":"—","weight":"85.5-95 kg","height":"—","chest_cm":0,"hip_cm":128,"waist_cm":88,"length_cm":61,"sleeve_cm":0,"pant_cm":61}
]
JSON

cat > "${WORK}/size_metaobject_map.json" <<'JSON'
[
  {"picker_label":"Girl 1-2 Years","gid":"gid://shopify/Metaobject/129972797537","catalog_label":"12-18 months","source_handle":"live-shopify-size-metaobject"},
  {"picker_label":"Girl 2 Years","gid":"gid://shopify/Metaobject/129972863073","catalog_label":"2-3 years","source_handle":"live-shopify-size-metaobject"},
  {"picker_label":"Girl 3 Years","gid":"gid://shopify/Metaobject/129972895841","catalog_label":"3-4 years","source_handle":"live-shopify-size-metaobject"},
  {"picker_label":"Girl 4 Years","gid":"gid://shopify/Metaobject/129972928609","catalog_label":"4-5 years","source_handle":"live-shopify-size-metaobject"},
  {"picker_label":"Girl 5 Years","gid":"gid://shopify/Metaobject/129972961377","catalog_label":"5-6 years","source_handle":"live-shopify-size-metaobject"},
  {"picker_label":"Girl 6-7 Years","gid":"gid://shopify/Metaobject/139840323681","catalog_label":"6-7 years","source_handle":"live-shopify-size-metaobject"},
  {"picker_label":"Girl 8 Years","gid":"gid://shopify/Metaobject/139840356449","catalog_label":"7-8 years","source_handle":"live-shopify-size-metaobject"},
  {"picker_label":"Girl 9-10 Years","gid":"gid://shopify/Metaobject/139840389217","catalog_label":"8-9 years (closest live catalog match)","source_handle":"live-shopify-size-metaobject"},
  {"picker_label":"Boy 1-2 Years","gid":"gid://shopify/Metaobject/129972797537","catalog_label":"12-18 months","source_handle":"live-shopify-size-metaobject"},
  {"picker_label":"Boy 2 Years","gid":"gid://shopify/Metaobject/129972863073","catalog_label":"2-3 years","source_handle":"live-shopify-size-metaobject"},
  {"picker_label":"Boy 3 Years","gid":"gid://shopify/Metaobject/129972895841","catalog_label":"3-4 years","source_handle":"live-shopify-size-metaobject"},
  {"picker_label":"Boy 4 Years","gid":"gid://shopify/Metaobject/129972928609","catalog_label":"4-5 years","source_handle":"live-shopify-size-metaobject"},
  {"picker_label":"Boy 5 Years","gid":"gid://shopify/Metaobject/129972961377","catalog_label":"5-6 years","source_handle":"live-shopify-size-metaobject"},
  {"picker_label":"Boy 6-7 Years","gid":"gid://shopify/Metaobject/139840323681","catalog_label":"6-7 years","source_handle":"live-shopify-size-metaobject"},
  {"picker_label":"Boy 8 Years","gid":"gid://shopify/Metaobject/139840356449","catalog_label":"7-8 years","source_handle":"live-shopify-size-metaobject"},
  {"picker_label":"Boy 9-10 Years","gid":"gid://shopify/Metaobject/139840389217","catalog_label":"8-9 years (closest live catalog match)","source_handle":"live-shopify-size-metaobject"},
  {"picker_label":"Mother S","gid":"gid://shopify/Metaobject/129975255137","catalog_label":"S","source_handle":"live-shopify-size-metaobject"},
  {"picker_label":"Mother M","gid":"gid://shopify/Metaobject/129975222369","catalog_label":"M","source_handle":"live-shopify-size-metaobject"},
  {"picker_label":"Mother L","gid":"gid://shopify/Metaobject/129975189601","catalog_label":"L","source_handle":"live-shopify-size-metaobject"},
  {"picker_label":"Mother XL","gid":"gid://shopify/Metaobject/129975287905","catalog_label":"XL","source_handle":"live-shopify-size-metaobject"},
  {"picker_label":"Mother 2XL","gid":"gid://shopify/Metaobject/129975156833","catalog_label":"2XL","source_handle":"live-shopify-size-metaobject"},
  {"picker_label":"Mother 3XL","gid":"gid://shopify/Metaobject/139840421985","catalog_label":"3XL","source_handle":"live-shopify-size-metaobject"},
  {"picker_label":"Father S","gid":"gid://shopify/Metaobject/129975255137","catalog_label":"S","source_handle":"live-shopify-size-metaobject"},
  {"picker_label":"Father M","gid":"gid://shopify/Metaobject/129975222369","catalog_label":"M","source_handle":"live-shopify-size-metaobject"},
  {"picker_label":"Father L","gid":"gid://shopify/Metaobject/129975189601","catalog_label":"L","source_handle":"live-shopify-size-metaobject"},
  {"picker_label":"Father XL","gid":"gid://shopify/Metaobject/129975287905","catalog_label":"XL","source_handle":"live-shopify-size-metaobject"},
  {"picker_label":"Father 2XL","gid":"gid://shopify/Metaobject/129975156833","catalog_label":"2XL","source_handle":"live-shopify-size-metaobject"},
  {"picker_label":"Father 3XL","gid":"gid://shopify/Metaobject/139840421985","catalog_label":"3XL","source_handle":"live-shopify-size-metaobject"}
]
JSON

cp "${WORK}/size_chart.json" "$SIZE_CHART_OUT"

python3 - "${WORK}/size_chart.json" "${WORK}/size_metaobject_map.json" "${WORK}/derived.json" "${WORK}/body.html" \
  "$TITLE" "$SEO_TITLE" "$SEO_DESCRIPTION" "$SHORTCODE" "$COLOR_TOKEN" "$COLOR_NAME" "$PRINT_NAME" \
  "$CHILD_PRICE" "$CHILD_COMPARE" "$MOTHER_PRICE" "$MOTHER_COMPARE" "$VENDOR_URL" "$SEASON" <<'PY'
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
    "Girl Shirt": "GRL",
    "Boy Shirt": "BOY",
    "Mother Shirt": "MOM",
    "Father Shirt": "DAD",
    "Girl Shorts": "GSO",
    "Boy Shorts": "BSO",
    "Mother Shorts": "MSO",
    "Father Shorts": "FSO",
}
size_tokens = {
    "Girl 1-2 Years": "KID12Y",
    "Girl 2 Years": "KID2Y",
    "Girl 3 Years": "KID3Y",
    "Girl 4 Years": "KID4Y",
    "Girl 5 Years": "KID5Y",
    "Girl 6-7 Years": "KID67Y",
    "Girl 8 Years": "KID8Y",
    "Girl 9-10 Years": "KID910Y",
    "Boy 1-2 Years": "KID12Y",
    "Boy 2 Years": "KID2Y",
    "Boy 3 Years": "KID3Y",
    "Boy 4 Years": "KID4Y",
    "Boy 5 Years": "KID5Y",
    "Boy 6-7 Years": "KID67Y",
    "Boy 8 Years": "KID8Y",
    "Boy 9-10 Years": "KID910Y",
    "Mother S": "S",
    "Mother M": "M",
    "Mother L": "L",
    "Mother XL": "XL",
    "Mother 2XL": "2XL",
    "Mother 3XL": "3XL",
    "Father S": "S",
    "Father M": "M",
    "Father L": "L",
    "Father XL": "XL",
    "Father 2XL": "2XL",
    "Father 3XL": "3XL",
}

def format_num(value):
    numeric = float(value)
    if numeric.is_integer():
        return str(int(numeric))
    return f"{numeric:.1f}".rstrip("0").rstrip(".")

def cm_in(value):
    if not value:
        return "—"
    numeric = float(value)
    return f"{format_num(numeric)} cm / {format_num(numeric / 2.54)} in"

def metric_text_to_dual_unit(value, metric_unit, imperial_unit, multiplier):
    text = str(value or "").strip()
    if not text or text in {"—", "-", "--"}:
        return "—"
    lowered = text.lower()
    if "/" in text and metric_unit.lower() in lowered and imperial_unit.lower() in lowered:
        return text

    range_match = re.fullmatch(r"(-?\d+(?:\.\d+)?)\s*[-–]\s*(-?\d+(?:\.\d+)?)\s*" + re.escape(metric_unit), text, re.IGNORECASE)
    if range_match:
        low = float(range_match.group(1))
        high = float(range_match.group(2))
        return (
            f"{format_num(low)}-{format_num(high)} {metric_unit} / "
            f"{format_num(low * multiplier)}-{format_num(high * multiplier)} {imperial_unit}"
        )

    single_match = re.fullmatch(r"(-?\d+(?:\.\d+)?)\s*" + re.escape(metric_unit), text, re.IGNORECASE)
    if single_match:
        numeric = float(single_match.group(1))
        return f"{format_num(numeric)} {metric_unit} / {format_num(numeric * multiplier)} {imperial_unit}"

    return text

def kg_lbs(value):
    return metric_text_to_dual_unit(value, "kg", "lbs", 2.20462)

def cm_range_in(value):
    return metric_text_to_dual_unit(value, "cm", "in", 1 / 2.54)

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

garments = []
seen_garments = set()
for row in chart:
    if row["garment"] not in seen_garments:
        garments.append(row["garment"])
        seen_garments.add(row["garment"])

raw_size_labels = [row["picker_label"] for row in chart]
has_duplicate_size_labels = len(set(raw_size_labels)) != len(raw_size_labels)
use_type_option = len(garments) > 1 or has_duplicate_size_labels

type_values = []
if use_type_option:
    for garment in garments:
        type_values.append({"name": garment})

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
        [row["garment"], row["picker_label"]]
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

girl_labels = [row["picker_label"] for row in chart if row["role"] == "Girl Shirt"]
boy_labels = [row["picker_label"] for row in chart if row["role"] == "Boy Shirt"]
mother_labels = [row["picker_label"] for row in chart if row["role"] == "Mother Shirt"]
father_labels = [row["picker_label"] for row in chart if row["role"] == "Father Shirt"]

def size_phrase():
    child_ladder = [
        "Girl 1-2 Years",
        "Girl 2 Years",
        "Girl 3 Years",
        "Girl 4 Years",
        "Girl 5 Years",
        "Girl 6-7 Years",
        "Girl 8 Years",
        "Girl 9-10 Years",
    ]
    child = "1-2Y–9-10Y" if girl_labels == child_ladder and len(boy_labels) == len(child_ladder) else "see chart"
    moms = "Mother S–3XL" if mother_labels == ["Mother S", "Mother M", "Mother L", "Mother XL", "Mother 2XL", "Mother 3XL"] else "Mother " + ", ".join(label.replace("Mother ", "") for label in mother_labels)
    dads = "Father S–3XL" if father_labels == ["Father S", "Father M", "Father L", "Father XL", "Father 2XL", "Father 3XL"] else "Father " + ", ".join(label.replace("Father ", "") for label in father_labels)
    return f"Girls & Boys {child}; {moms}; {dads} for both the shirt and the shorts"

def li(label, text):
    return f"<li><strong>{label}:</strong> {html.escape(text)}</li>"

def shirt_table_row(row):
    return (
        "<tr>"
        f"<td>{html.escape(row['picker_label'])}</td>"
        f"<td>{html.escape(row['age'])}</td>"
        f"<td>{html.escape(kg_lbs(row['weight']))}</td>"
        f"<td>{html.escape(cm_range_in(row['height']))}</td>"
        f"<td>{cm_in(row['chest_cm'])}</td>"
        f"<td>{cm_in(row['sleeve_cm'])}</td>"
        f"<td>{cm_in(row['pant_cm'])}</td>"
        f"<td>{cm_in(row['hip_cm'])}</td>"
        f"<td>{cm_in(row['waist_cm'])}</td>"
        f"<td>{cm_in(row['length_cm'])}</td>"
        "</tr>"
    )

def shorts_table_row(row):
    return (
        "<tr>"
        f"<td>{html.escape(row['picker_label'])}</td>"
        f"<td>{html.escape(row['age'])}</td>"
        f"<td>{html.escape(kg_lbs(row['weight']))}</td>"
        f"<td>{html.escape(cm_range_in(row['height']))}</td>"
        f"<td>{cm_in(row['chest_cm'])}</td>"
        f"<td>{cm_in(row['sleeve_cm'])}</td>"
        f"<td>{cm_in(row['pant_cm'])}</td>"
        f"<td>{cm_in(row['hip_cm'])}</td>"
        f"<td>{cm_in(row['waist_cm'])}</td>"
        f"<td>{cm_in(row['length_cm'])}</td>"
        "</tr>"
    )

shirt_rows = [shirt_table_row(row) for row in chart if row["garment"] == "Shirt"]
short_rows = [shorts_table_row(row) for row in chart if row["garment"] == "Shorts"]

body_html = "\n".join([
    "<ul>",
    li("Fabric", "Lightweight woven fabric with an easy drape and a relaxed summer hand-feel for both the hooded shirt and the cargo shorts."),
    li("Family story", "A coordinated four-role matching look for moms, dads, girls, and boys, designed for park days, family photos, travel, and easy weekend plans."),
    li("Print", f"\"{print_name}\" pairs a beige-and-olive plaid hooded sun shirt with muted gray-green cargo shorts for an outdoorsy family palette."),
    li("Design details", "Customers can choose the hooded button-front sun shirt or the pull-on elastic-waist cargo shorts with roomy patch pockets. The blue-letter inner tee shown in the lifestyle photo is not included."),
    li("Care", "Machine wash cold on gentle, line dry, do not bleach, and use a cool iron inside-out if needed."),
    li("Size range", size_phrase() + "."),
    "</ul>",
    "",
    "<h3>Size Chart — Hooded Sun Shirt</h3>",
    "<table id=\"size-chart\">",
    "  <thead>",
    "    <tr>",
    "      <th>Size</th>",
    "      <th>Age</th>",
    "      <th>Weight (kg/lbs)</th>",
    "      <th>Height (cm/in)</th>",
    "      <th>Chest/Bust (cm/in)</th>",
    "      <th>Sleeve (cm/in)</th>",
    "      <th>Pant/Short or — (cm/in)</th>",
    "      <th>Hip (cm/in)</th>",
    "      <th>Waist (cm/in)</th>",
    "      <th>Garment Length (cm/in)</th>",
    "    </tr>",
    "  </thead>",
    "  <tbody>",
    *shirt_rows,
    "  </tbody>",
    "</table>",
    "",
    "<h3>Size Chart — Cargo Shorts</h3>",
    "<table id=\"size-chart-shorts\">",
    "  <thead>",
    "    <tr>",
    "      <th>Size</th>",
    "      <th>Age</th>",
    "      <th>Weight (kg/lbs)</th>",
    "      <th>Height (cm/in)</th>",
    "      <th>Chest/Bust or — (cm/in)</th>",
    "      <th>Sleeve or — (cm/in)</th>",
    "      <th>Pant/Short Length (cm/in)</th>",
    "      <th>Hip (cm/in)</th>",
    "      <th>Waist (cm/in)</th>",
    "      <th>Garment Length (cm/in)</th>",
    "    </tr>",
    "  </thead>",
    "  <tbody>",
    *short_rows,
    "  </tbody>",
    "</table>",
    "",
    "<p>Trail Plaid gives family matching a more laid-back, utility-inspired feel. The beige plaid hooded shirt softens the look, while the gray-green cargo shorts keep the palette grounded and casual. Together they read easy, outdoorsy, and photo-ready without looking fussy.</p>",
    "",
    "<p>This listing now lets shoppers choose the piece they need: the lightweight hooded shirt for easy sun coverage or the roomy cargo shorts for practical warm-weather wear. It works well for sightseeing, travel days, beach-town walks, playground runs, and all the family moments where coordinated style should still feel comfortable.</p>",
    "",
    "<h3>Key Features:</h3>",
    "<ul>",
    li("Choose your piece", "Use the Type selector to shop the hooded sun shirt or the cargo shorts separately within the same family matching listing."),
    li("Easy plaid layer", "The hooded button-front shirt adds lightweight coverage for sun and breezy afternoons."),
    li("Relaxed cargo shorts", "Patch-pocket shorts keep the look practical and comfortable for active days."),
    li("Four-role matching", "One listing covers girl, boy, mother, and father size runs for both garments."),
    li("Styled tee not included", "The blue-letter inner tee visible in the lifestyle image is intentionally excluded from this listing."),
    "</ul>",
    "",
    "<p>Choose the shirt or shorts sizes you need and build a family matching look that feels casual, coordinated, and ready for the next sunny plan.</p>",
])

tags = [
    "Family Matching",
    "Mommy and Me",
    "Daddy and Me",
    "Sets",
    "Summer Family Matching Set",
    "Matching Family Outfits",
    "Matching Family Set",
    "Matching Family Shirt",
    "Matching Family Shorts",
    "Summer",
    "Resort",
    "Vacation",
    "Trail Plaid",
    "Plaid",
    "Checkered",
    "Beige",
    "Gray",
    "Green",
    "Olive",
    "Khaki",
    "Hooded Shirt",
    "Sun Shirt",
    "Cargo Shorts",
    "Girl Shirt",
    "Boy Shirt",
    "Mother Shirt",
    "Father Shirt",
    "Girl Shorts",
    "Boy Shorts",
    "Mother Shorts",
    "Father Shorts",
    "Four-Role Matching",
    "Child 1-2yr",
    "Child 2-3yr",
    "Child 4-5yr",
    "Child 6-8yr",
    "Child 9-10yr",
    "Mother S",
    "Mother M",
    "Mother L",
    "Mother XL",
    "Mother 2XL",
    "Mother 3XL",
    "Father S",
    "Father M",
    "Father L",
    "Father XL",
    "Father 2XL",
    "Father 3XL",
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
    "seed_skus_sorted": sorted(item["sku"] for item in recap if item["garment"] == "Shirt"),
    "shopify_size_refs": list(dict.fromkeys(size_map[row["picker_label"]]["gid"] for row in chart)),
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
COLOR_PATTERN_GIDS_JSON='["gid://shopify/Metaobject/69641928801","gid://shopify/Metaobject/69944672353","gid://shopify/Metaobject/70220546145","gid://shopify/Metaobject/130283143265"]'
TARGET_GENDER_GIDS_JSON='["gid://shopify/Metaobject/129971617889","gid://shopify/Metaobject/130231107681"]'
CARE_INSTRUCTIONS_GIDS_JSON='["gid://shopify/Metaobject/130283503713"]'

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
    TYPE_OPTION_ID="$(echo "$EXISTING_RESPONSE" | jq -r '.data.productByHandle.options[]? | select(.name=="Type") | .id' | head -n 1)"
    COLOR_OPTION_ID="$(echo "$EXISTING_RESPONSE" | jq -r '.data.productByHandle.options[]? | select(.name=="Color") | .id' | head -n 1)"

    if [[ -z "$TYPE_OPTION_ID" ]]; then
      PRODUCT_OPTIONS_CREATE_MUTATION='mutation ProductOptionsCreate($productId: ID!, $options: [OptionCreateInput!]!, $variantStrategy: ProductOptionCreateVariantStrategy) {
        productOptionsCreate(productId: $productId, options: $options, variantStrategy: $variantStrategy) {
          product {
            id
            options { id name position values optionValues { id name hasVariants } }
          }
          userErrors { field message }
        }
      }'

      PRODUCT_OPTIONS_CREATE_RESPONSE="$(gql "$PRODUCT_OPTIONS_CREATE_MUTATION" "$(jq -nc --arg product_id "$PRODUCT_ID" --argjson type_values "$(jq -c '.type_values' "${WORK}/derived.json")" '{productId: $product_id, options: [{name: "Type", values: $type_values}], variantStrategy: "LEAVE_AS_IS"}')")"
      check_graphql_errors "$PRODUCT_OPTIONS_CREATE_RESPONSE" "productOptionsCreate"
      check_user_errors "$PRODUCT_OPTIONS_CREATE_RESPONSE" '.data.productOptionsCreate.userErrors' "productOptionsCreate"
      refresh_existing_product
      COLOR_OPTION_ID="$(echo "$EXISTING_RESPONSE" | jq -r '.data.productByHandle.options[]? | select(.name=="Color") | .id' | head -n 1)"
    fi

    if [[ -n "$COLOR_OPTION_ID" ]]; then
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

      PRODUCT_OPTIONS_DELETE_RESPONSE="$(gql "$PRODUCT_OPTIONS_DELETE_MUTATION" "$(jq -nc --arg product_id "$PRODUCT_ID" --arg color_option_id "$COLOR_OPTION_ID" '{productId: $product_id, options: [$color_option_id], strategy: "NON_DESTRUCTIVE"}')")"
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
VARIANTS_TO_CREATE_JSON="$VARIANTS_JSON"
if [[ "$CREATE_NEW_PRODUCT" == "1" ]]; then
  SHOULD_CREATE_VARIANTS="1"
else
  EXISTING_VARIANT_COUNT="$(echo "$EXISTING_RESPONSE" | jq '.data.productByHandle.variants.nodes | length')"
  EXISTING_SKUS_SORTED="$(echo "$EXISTING_RESPONSE" | jq -r '.data.productByHandle.variants.nodes[].sku // empty' | sed '/^$/d' | sort)"
  if [[ "$EXISTING_VARIANT_COUNT" -eq 0 ]]; then
    SHOULD_CREATE_VARIANTS="1"
  elif [[ "$EXISTING_VARIANT_COUNT" -eq 1 && -z "$EXISTING_SKUS_SORTED" ]]; then
    SHOULD_CREATE_VARIANTS="1"
  else
    RECONCILE_JSON="$(python3 - "${WORK}/derived.json" "${WORK}/existing.json" <<'PY'
import json
import sys

derived = json.load(open(sys.argv[1]))
existing_nodes = json.load(open(sys.argv[2]))["data"]["productByHandle"]["variants"]["nodes"]
derived_by_sku = {row["inventoryItem"]["sku"]: row for row in derived["variants"]}
existing_skus = [node["sku"] for node in existing_nodes if node.get("sku")]
existing_set = set(existing_skus)
extra_skus = sorted(existing_set - set(derived_by_sku))
missing_variants = [row for row in derived["variants"] if row["inventoryItem"]["sku"] not in existing_set]
print(json.dumps({
    "extra_skus": extra_skus,
    "missing_variants": missing_variants,
}))
PY
)"

    EXTRA_SKU_COUNT="$(echo "$RECONCILE_JSON" | jq '.extra_skus | length')"
    if [[ "$EXTRA_SKU_COUNT" -ne 0 ]]; then
      echo "ERROR: existing product handle ${HANDLE} has unexpected live variants; refusing to create duplicates." >&2
      echo "Existing SKUs:" >&2
      echo "$EXISTING_SKUS_SORTED" >&2
      echo "Derived SKUs:" >&2
      echo "$DERIVED_SKUS_SORTED" >&2
      echo "Unexpected extra SKUs:" >&2
      echo "$RECONCILE_JSON" | jq -r '.extra_skus[]' >&2
      exit 1
    fi

    SHOULD_UPDATE_VARIANTS="1"
    VARIANTS_TO_CREATE_JSON="$(echo "$RECONCILE_JSON" | jq -c '.missing_variants')"
    if [[ "$(echo "$VARIANTS_TO_CREATE_JSON" | jq 'length')" -gt 0 ]]; then
      SHOULD_CREATE_VARIANTS="1"
    fi
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
    --argjson variants "$VARIANTS_TO_CREATE_JSON" '
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
        "optionValues": spec["optionValues"],
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
  --arg target_gender_value "$(echo "$TARGET_GENDER_GIDS_JSON" | jq -c .)" \
  --arg size_value "$(echo "$SHOPIFY_SIZE_REFS_JSON" | jq -c .)" \
  --arg merch_subcategory "$MERCH_SUBCATEGORY" \
  --arg merch_subcategory2 "$MERCH_SUBCATEGORY2" \
  --arg merch_style "$MERCH_STYLE" \
  --arg merch_type "$MERCH_TYPE" \
  --arg seo_title "$SEO_TITLE" \
  --arg seo_description "$SEO_DESCRIPTION" '
  [
      {ownerId: $pid, namespace: "custom", key: "category1", type: "single_line_text_field", value: "Family Matching"},
      {ownerId: $pid, namespace: "custom", key: "subcategory", type: "single_line_text_field", value: $merch_subcategory},
      {ownerId: $pid, namespace: "custom", key: "subcategory2", type: "single_line_text_field", value: $merch_subcategory2},
      {ownerId: $pid, namespace: "custom", key: "pattern", type: "single_line_text_field", value: "Trail Plaid Cargo"},
      {ownerId: $pid, namespace: "custom", key: "style", type: "single_line_text_field", value: $merch_style},
      {ownerId: $pid, namespace: "custom", key: "type", type: "single_line_text_field", value: $merch_type},
      {ownerId: $pid, namespace: "mm-google-shopping", key: "custom_product", type: "boolean", value: "false"},
      {ownerId: $pid, namespace: "mm-google-shopping", key: "gender", type: "single_line_text_field", value: "unisex"},
      {ownerId: $pid, namespace: "mm-google-shopping", key: "age_group", type: "single_line_text_field", value: "adult"},
      {ownerId: $pid, namespace: "mm-google-shopping", key: "condition", type: "single_line_text_field", value: "new"},
      {ownerId: $pid, namespace: "mm-google-shopping", key: "custom_label_0", type: "single_line_text_field", value: "Family Matching"},
      {ownerId: $pid, namespace: "mm-google-shopping", key: "custom_label_1", type: "single_line_text_field", value: "Trail Plaid"},
      {ownerId: $pid, namespace: "mm-google-shopping", key: "custom_label_2", type: "single_line_text_field", value: "Summer"},
      {ownerId: $pid, namespace: "mm-google-shopping", key: "custom_label_3", type: "single_line_text_field", value: "Hooded Shirt & Cargo Shorts"},
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

STALE_SHOPIFY_METAFIELDS_TO_DELETE_JSON="$(python3 - "${WORK}/existing.json" "$PRODUCT_ID" <<'PY'
import json
import sys

existing = json.load(open(sys.argv[1]))
product_id = sys.argv[2]
keys_to_delete = {"dress-occasion", "dress-style", "skirt-dress-length-type", "top-length-type"}
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

if ((${#MEDIA_FILES[@]})); then
for image_path in "${MEDIA_FILES[@]}"; do
  image_name="$(basename "$image_path")"
  case "$image_name" in
    01-*)
      alt_text="Plaid hooded sun shirt from the Trail Plaid family matching set."
      ;;
    02-*)
      alt_text="Gray-green cargo shorts from the Trail Plaid family matching set."
      ;;
    *)
      alt_text="Family wearing the Trail Plaid matching set with a hooded plaid shirt and cargo shorts."
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
fi

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
  if echo "$VERIFY_RESPONSE" | jq -e '.data.product.collections.nodes | map(.handle) | index("family-sets") != null' > /dev/null; then
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
    ("Live option values match derived values", all(next((option["values"] for option in product_options if option["name"] == axis["name"]), None) == axis["values"] for axis in option_axes), json.dumps({option["name"]: option["values"] for option in product_options}, ensure_ascii=False)),
    (f"Every {' x '.join(option_names)} combination exists", live_option_pairs == expected_option_pairs, str(sorted(live_option_pairs))),
    ("Size table first column matches picker labels", first_cells == expected_first_cells, " | ".join(first_cells)),
    ("Size tables expose metric + imperial units", "kg/lbs" in html_body and "cm/in" in html_body and bool(re.search(r"\b(?:lbs|in)\b", html_body)), "kg/lbs + cm/in"),
    ("Each size table has 10 headers", table_header_counts and all(count == 10 for count in table_header_counts), str(table_header_counts)),
    ("Table row count matches SIZE_CHART", len(tbody_rows) == len(chart), str(len(tbody_rows))),
    ("Waist populated for every row", all(str(row["waist_cm"]).strip() not in {"", "—"} for row in chart), "all rows populated"),
    ("publishedAt is populated", bool(product["publishedAt"]), product["publishedAt"] or ""),
    ("onlineStoreUrl is populated", bool(product["onlineStoreUrl"]), product["onlineStoreUrl"] or ""),
    ("Taxonomy category is set", product["category"]["id"] == "gid://shopify/TaxonomyCategory/aa-1-11", product["category"]["id"]),
    ("Taxonomy category full name matches expected leaf", product["category"]["fullName"] == expected_taxonomy_full_name, product["category"]["fullName"]),
    ("Family-set merchandising tag is present", merch_collection_tag in product["tags"], ", ".join(product["tags"])),
    ("Family-set smart collection is attached", "family-sets" in collection_handles, str(sorted(collection_handles))),
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
    ("shopify", "size"),
    ("shopify", "target-gender"),
    ("global", "title_tag"),
    ("global", "description_tag"),
}
checks.append(("Applicable metafields are written", required_written.issubset(metafield_keys), str(sorted(required_written - metafield_keys))))

skipped_metafields = {
    "shopify.clothing-features": "The current store catalog only exposes heavyweight or technical feature values in this namespace, which would be inaccurate for this lightweight summer family set.",
    "shopify.fabric": "The direct vendor page was captcha-blocked and the supplied chart plus photos do not confirm one honest fiber metaobject, so this field was left unset rather than guessing cotton vs. synthetic.",
    "shopify.dress-occasion": "Not written because the honest Shopify taxonomy for this product is `Outfit Sets`, not `Dresses`.",
    "shopify.dress-style": "Not written because this is a mixed shirt-and-shorts listing rather than a dress-only taxonomy leaf.",
    "shopify.fit": "The Outfit Sets taxonomy exposes fit, but no reliable writable standard Shopify metafield definition is currently available in this store for that attribute.",
    "shopify.neckline": "The hooded shirt plus separate cargo-shorts presentation does not map cleanly to one honest product-level neckline value in this store.",
    "shopify.pants-length-type": "Not written because the product-level record mixes tops and shorts, and this store does not expose a reliable writable standard Shopify metafield definition for shorts length on this mixed outfit-set owner subtype.",
    "shopify.skirt-dress-length-type": "Not written because the listing is not a dress product and no skirt-length claim would be honest here.",
    "shopify.sleeve-length-type": "Not written because the product-level record mixes shirts and shorts, and this store does not expose a reliable writable definition for that mixed-garment context.",
    "shopify.top-length-type": "Removed if present because the listing mixes shirt and shorts rows, and no single top-length value honestly covers the whole product.",
    "shopify.waist-rise": "The shorts waist was derived for the size table, but no reliable writable standard Shopify metafield definition is currently available in this store for this mixed shirt-and-shorts listing.",
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
    put("Google Shopping / Gender", "unisex")
    put("Google Shopping / Age Group", "adult")
    put("Google Shopping / Condition", "new")
    put("Google Shopping / Custom Product", "FALSE")
    put("Google Shopping / Custom Label 0", "Family Matching")
    put("Google Shopping / Custom Label 1", "Trail Plaid")
    put("Google Shopping / Custom Label 2", "Summer")
    put("Google Shopping / Custom Label 3", "Hooded Shirt & Cargo Shorts")
    put("Google Shopping / Custom Label 4", "Four-Role Matching")
    put("Category1 (product.metafields.custom.category1)", "Family Matching")
    put("Pattern (product.metafields.custom.pattern)", "Trail Plaid Cargo")
    put("Style (product.metafields.custom.style)", merch_style)
    put("SubCategory (product.metafields.custom.subcategory)", merch_subcategory)
    put("SubCategory2 (product.metafields.custom.subcategory2)", merch_subcategory2)
    put("Type (product.metafields.custom.type)", merch_type)
    put("Google: Custom Product (product.metafields.mm-google-shopping.custom_product)", "false")
    put("Age group (product.metafields.shopify.age-group)", "kids, adults")
    put("Color (product.metafields.shopify.color-pattern)", "Beige, Gray, Green, Checkered")
    put("Size (product.metafields.shopify.size)", ", ".join(x["name"] for x in derived["size_values"]))
    put("Target Gender (product.metafields.shopify.target-gender)", "Female, Male")
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
lines.append("| LISTING_MODE | Family Matching |")
lines.append("| PRIMARY_CATEGORY | Set → FamilySet (Shopify taxonomy kept as Outfit Sets) |")
lines.append("| DESIGNS_TO_LIST | Gray green cargo shorts, Sun protection shirt |")
lines.append("| EXCLUDE_ITEMS | Blue-letter inner tee excluded; listing now sells the shirt and shorts as separate Type choices |")
lines.append("| SHORTCODE | auto → `TPLD` |")
lines.append("| COLOR_TOKEN | auto → `OLIVE` |")
lines.append("| FORCE_SPEC_PRICES | true |")
lines.append("")
lines.append("## Vendor fetch status")
lines.append("The direct 1688 page was captcha-blocked during this run, so the attached size-chart image and supplied product photos were used as the authoritative source of truth. The top shirt table and lower cargo-short table were each kept as separate garment tracks, while the middle blue-letter tee table was excluded because the request only covered the hooded sun shirt plus gray-green cargo shorts. Per the operator correction, this listing now uses `Type / Size` so shoppers choose `Shirt` or `Shorts` rather than a color value. Neighbor pricing was anchored to `blue-striped-family-matching-set`, size metaobject GIDs came from live `shopify--size` lookups, and the Shopify taxonomy stays `Outfit Sets` for honest standard-category attributes.")
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
lines.append("- The shirt chest column is labeled `胸围*2`, so each published number was doubled before writing `chest_cm`.")
lines.append("- Shirt `hip_cm` / `waist_cm` were derived from the store's canonical shirt rules because the vendor shirt table only publishes chest, length, shoulder, and sleeve.")
lines.append("- The shorts `臀围` values were treated as flat vendor widths and doubled to full `hip_cm`; the adult raw values `54-64` cannot be honest full-circumference hips.")
lines.append("- The vendor omits shorts waist, so `waist_cm` was derived from the store's live elastic-short grading curve: child waists `44-64 cm` and adult waists `68-88 cm`.")
lines.append("- The shared child ladders were duplicated into both girl and boy rows so the storefront can still merchandise both kid roles while the shopper selects the garment through `Type`.")
lines.append("- The shared adult ladders were duplicated into both mother and father rows so the storefront can still merchandise both parent roles while the shopper selects the garment through `Type`.")
lines.append("- Adult height guidance is left as `—` because the vendor chart does not provide it and the supplied evidence does not justify role-specific height guesses.")
lines.append("")
lines.append("### Vendor → picker mapping log")
lines.append("- Shirt 80 / 90 / 100 / 110 / 120 / 130 / 140 / 150 → Girl 1-2 Years through Girl 9-10 Years, plus Boy 1-2 Years through Boy 9-10 Years")
lines.append("- Shorts 80 / 90 / 100 / 110 / 120 / 130 / 140 / 150 → Girl 1-2 Years through Girl 9-10 Years, plus Boy 1-2 Years through Boy 9-10 Years")
lines.append("- Shirt S / M / L / XL / XXL / 3XL → Mother S / M / L / XL / 2XL / 3XL and Father S / M / L / XL / 2XL / 3XL")
lines.append("- Shorts S / M / L / XL / XXL / 3XL → Mother S / M / L / XL / 2XL / 3XL and Father S / M / L / XL / 2XL / 3XL")
lines.append("")
lines.append("### EXCLUDE_ITEMS decisions")
lines.append("- The middle vendor table `26B020-蓝字母短袖` was excluded because the request only covered the gray-green cargo shorts and the hooded sun-protection shirt.")
lines.append("- The lifestyle photo's inner blue-letter tee is not included in the product and is called out in the body copy to prevent confusion.")
lines.append("")
lines.append("## Body HTML")
lines.append("- 1 `<ul>` with 6 bullets (fabric, family story, print, design details, care, size range).")
lines.append("- 2 garment-specific `<h3>` + `<table>` blocks (`Hooded Sun Shirt` and `Cargo Shorts`), each with 10 `<th>` headers.")
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
lines.append("- If merchandising wants a stronger PDP disclaimer about the excluded inner tee, add the same note to image captions or FAQ copy.")
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
lines.append("- Size metaobject map: live `shopify--size` metaobject lookups")

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
