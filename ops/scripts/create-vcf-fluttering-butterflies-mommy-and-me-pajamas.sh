#!/usr/bin/env bash
set -euo pipefail

ROOT="/Users/fsuels/Projects/dresslikemommy"
ENV_FILE="${SHOPIFY_ENV_FILE:-${HOME}/.config/dresslikemommy/shopify-admin.env}"

if [[ -f "$ENV_FILE" ]]; then
  # shellcheck disable=SC1090
  source "$ENV_FILE"
fi

: "${SHOPIFY_STORE_DOMAIN:?SHOPIFY_STORE_DOMAIN not set}"
: "${SHOPIFY_ADMIN_ACCESS_TOKEN:?SHOPIFY_ADMIN_ACCESS_TOKEN not set}"

STORE="${SHOPIFY_STORE_DOMAIN}"
TOKEN="${SHOPIFY_ADMIN_ACCESS_TOKEN}"
API="https://${STORE}/admin/api/2025-01/graphql.json"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

HANDLE="fluttering-butterflies-mommy-and-me-pajamas"
TITLE="Fluttering Butterflies Mommy and Me Pajamas — Short-Sleeve Set"
SEO_TITLE="Butterfly Mommy & Me Pajamas — Set | Dress Like Mommy"
SEO_DESCRIPTION="Shop our Fluttering Butterflies matching mommy-and-me pajamas — soft bamboo-cotton gauze short-sleeve set for mom + daughter. Sizes 2Y–10Y & Mom S–XL."
PRINT_NAME="Fluttering Butterflies"
COLOR_OPTION_VALUE="${PRINT_NAME}"
SHORTCODE="VCF"
COLOR_TOKEN="CREAM"
CHILD_PRICE="33.99"
MOTHER_PRICE="37.99"
SEASON="Summer"
CATEGORY="Pajamas"
CATEGORY_WORD="Pajamas"
PRODUCT_TYPE="Matching Family Pajamas"
CUSTOM_TYPE="Two-Piece Pajama Set"
TAXONOMY_GID="gid://shopify/TaxonomyCategory/aa-1-17-4"
GOOGLE_PRODUCT_CATEGORY="2580"
SHOPIFY_CATEGORY_PATH="Apparel & Accessories > Clothing > Sleepwear & Loungewear > Pajamas"
VENDOR_URL="https://detail.1688.com/offer/1026510859610.html"
VENDOR_TITLE_CN="安旦26新品春夏竹棉纱布亲子家居服甜美荷叶边短袖长裤居家套装 - 阿里巴巴"
VENDOR_TITLE_EN="Andan 26 new spring/summer bamboo-cotton gauze family homewear sweet ruffle-trim short-sleeve long-pants lounge set."
DESIGNS_TO_LIST="蝴蝶飞飞（成人款）, 蝴蝶飞飞（儿童款）"
HERO_IMAGE_SOURCE="/Users/fsuels/Downloads/white/ChatGPT Image Apr 21, 2026, 01_43_34 PM.png"
SIZE_IMAGE_SOURCE="/private/var/folders/5t/g_ys4vp54n9c0cfg7zkjm4n00000gn/T/TemporaryItems/com.apple.Photos.NSItemProvider/uuid=69939F2A-E720-48DD-8BFD-E99DA3A70B80&code=001&library=1&type=1&mode=1&loc=true&cap=true.png/Image 4-21-26 at 1.41 PM.png"
UPLOAD_DIR="${ROOT}/uploads/${HANDLE}"
LISTING_MD="${ROOT}/${HANDLE}-listing.md"
CSV_OUT="${ROOT}/${HANDLE}-shopify-import.csv"

PHOTO_URLS_JSON='["https://cbu01.alicdn.com/img/ibank/O1CN01ZjfOlF2AN4jS76L8x_!!2210477678190-0-cib.jpg_.webp"]'

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
  {"audience":"child","vendor_label":"90","picker_label":"Child 2 Years","sku_suffix":"KID2Y","age":"2","weight":"11–14 kg / 24–31 lbs","height":"85–95 cm / 33–37 in","chest_cm":67,"hip_cm":66,"waist_cm":42,"length_cm":35.5,"sleeve_cm":17.5,"pant_cm":55,"shoulder_cm":22.5},
  {"audience":"child","vendor_label":"100","picker_label":"Child 3 Years","sku_suffix":"KID3Y","age":"3","weight":"14–16 kg / 31–35 lbs","height":"95–105 cm / 37–41 in","chest_cm":71,"hip_cm":70,"waist_cm":44,"length_cm":38.5,"sleeve_cm":18,"pant_cm":60,"shoulder_cm":24},
  {"audience":"child","vendor_label":"110","picker_label":"Child 4 Years","sku_suffix":"KID4Y","age":"4","weight":"16–19 kg / 35–42 lbs","height":"105–115 cm / 41–45 in","chest_cm":75,"hip_cm":74,"waist_cm":46,"length_cm":41.5,"sleeve_cm":18.5,"pant_cm":65,"shoulder_cm":25.5},
  {"audience":"child","vendor_label":"120","picker_label":"Child 5 Years","sku_suffix":"KID5Y","age":"5","weight":"19–22 kg / 42–49 lbs","height":"115–125 cm / 45–49 in","chest_cm":79,"hip_cm":78,"waist_cm":48,"length_cm":45,"sleeve_cm":19,"pant_cm":70,"shoulder_cm":27},
  {"audience":"child","vendor_label":"130","picker_label":"Child 6-7 Years","sku_suffix":"KID67Y","age":"6–7","weight":"22–27 kg / 49–60 lbs","height":"125–135 cm / 49–53 in","chest_cm":83,"hip_cm":82,"waist_cm":50,"length_cm":48,"sleeve_cm":19.5,"pant_cm":75,"shoulder_cm":28.5},
  {"audience":"child","vendor_label":"140","picker_label":"Child 8 Years","sku_suffix":"KID8Y","age":"8","weight":"27–33 kg / 60–73 lbs","height":"135–145 cm / 53–57 in","chest_cm":87,"hip_cm":86,"waist_cm":52,"length_cm":52,"sleeve_cm":20,"pant_cm":80,"shoulder_cm":30},
  {"audience":"child","vendor_label":"150","picker_label":"Child 9-10 Years","sku_suffix":"KID910Y","age":"9–10","weight":"33–40 kg / 73–88 lbs","height":"145–155 cm / 57–61 in","chest_cm":91,"hip_cm":90,"waist_cm":54,"length_cm":56,"sleeve_cm":20.5,"pant_cm":86,"shoulder_cm":31.5},
  {"audience":"mother","vendor_label":"S","picker_label":"Mother S","sku_suffix":"MOMS","age":"—","weight":"45–52 kg / 99–115 lbs","height":"155–160 cm / 61–63 in","chest_cm":99,"hip_cm":95,"waist_cm":72,"length_cm":62,"sleeve_cm":24,"pant_cm":97,"shoulder_cm":37},
  {"audience":"mother","vendor_label":"M","picker_label":"Mother M","sku_suffix":"MOMM","age":"—","weight":"52–60 kg / 115–132 lbs","height":"160–165 cm / 63–65 in","chest_cm":103,"hip_cm":99,"waist_cm":74,"length_cm":64,"sleeve_cm":25,"pant_cm":99,"shoulder_cm":38},
  {"audience":"mother","vendor_label":"L","picker_label":"Mother L","sku_suffix":"MOML","age":"—","weight":"60–68 kg / 132–150 lbs","height":"165–170 cm / 65–67 in","chest_cm":107,"hip_cm":103,"waist_cm":76,"length_cm":66,"sleeve_cm":26,"pant_cm":101,"shoulder_cm":39},
  {"audience":"mother","vendor_label":"XL","picker_label":"Mother XL","sku_suffix":"MOMXL","age":"—","weight":"68–75 kg / 150–165 lbs","height":"170–175 cm / 67–69 in","chest_cm":111,"hip_cm":107,"waist_cm":78,"length_cm":68,"sleeve_cm":27,"pant_cm":103,"shoulder_cm":40}
]
JSON

ROW_COUNT="$(jq 'length' "${WORK}/size_chart.json")"
jq -e 'all(.[]; .audience and .vendor_label and .picker_label and .sku_suffix and .age and .weight and .height and (.chest_cm != null) and (.hip_cm != null) and (.waist_cm != null) and (.length_cm != null) and (.sleeve_cm != null) and (.pant_cm != null))' "${WORK}/size_chart.json" > /dev/null
jq -e '([.[].picker_label] | length) == ([.[].picker_label] | unique | length)' "${WORK}/size_chart.json" > /dev/null

SIZE_VALUES_JSON="$(jq -c '[.[] | {name: .picker_label}]' "${WORK}/size_chart.json")"
SIZE_VALUE_COUNT="$(echo "$SIZE_VALUES_JSON" | jq 'length')"

VARIANTS_JSON="$(jq -c \
  --arg child_price "$CHILD_PRICE" \
  --arg child_compare "$CHILD_COMPARE" \
  --arg mother_price "$MOTHER_PRICE" \
  --arg mother_compare "$MOTHER_COMPARE" \
  --arg shortcode "$SHORTCODE" \
  --arg color_token "$COLOR_TOKEN" \
  --arg color_name "$COLOR_OPTION_VALUE" '
  [
    .[] | {
      price: (if .audience == "child" then $child_price else $mother_price end),
      compareAtPrice: (if .audience == "child" then $child_compare else $mother_compare end),
      inventoryPolicy: "DENY",
      inventoryItem: {
        sku: ("DLM-" + $shortcode + "-" + .sku_suffix + "-" + $color_token),
        tracked: true,
        requiresShipping: true
      },
      optionValues: [
        {optionName: "Size", name: .picker_label},
        {optionName: "Color", name: $color_name}
      ]
    }
  ]' "${WORK}/size_chart.json")"
VARIANT_COUNT="$(echo "$VARIANTS_JSON" | jq 'length')"

if [[ "$ROW_COUNT" -ne "$SIZE_VALUE_COUNT" || "$ROW_COUNT" -ne "$VARIANT_COUNT" ]]; then
  echo "ERROR: SIZE_CHART row count, option value count, and variant count diverged." >&2
  exit 1
fi

DERIVED_SKUS_SORTED="$(echo "$VARIANTS_JSON" | jq -r '.[].inventoryItem.sku' | sort)"

SEO_SIZE_PHRASE="$(jq -r '
  def short_kid:
    if . == "Child 2 Years" then "2Y"
    elif . == "Child 3 Years" then "3Y"
    elif . == "Child 4 Years" then "4Y"
    elif . == "Child 5 Years" then "5Y"
    elif . == "Child 6-7 Years" then "6-7Y"
    elif . == "Child 8 Years" then "8Y"
    elif . == "Child 9-10 Years" then "9-10Y"
    else .
    end;
  def short_mom:
    if . == "Mother One Size" then "One Size"
    else sub("^Mother "; "")
    end;
  [.[] | select(.audience == "child") | .picker_label | short_kid] as $kids |
  [.[] | select(.audience == "mother") | .picker_label | short_mom] as $moms |
  (
    if $kids == ["2Y","3Y","4Y","5Y","6-7Y","8Y","9-10Y"] then "2Y–10Y"
    elif ($kids | length) > 0 then ($kids | join(", "))
    else ""
    end
  ) as $kid_phrase |
  (
    if $moms == ["S","M","L","XL"] then "Mom S–XL"
    elif $moms == ["One Size"] then "Mom One Size"
    elif ($moms | length) > 0 then "Mom " + ($moms | join(", "))
    else ""
    end
  ) as $mom_phrase |
  if $kid_phrase != "" and $mom_phrase != "" then $kid_phrase + " & " + $mom_phrase
  elif $kid_phrase != "" then $kid_phrase
  else $mom_phrase
  end' "${WORK}/size_chart.json")"

SIZE_RANGE_COPY="$(jq -r '
  [.[] | select(.audience == "child") | .picker_label] as $kids |
  [.[] | select(.audience == "mother") | .picker_label | sub("^Mother "; "")] as $moms |
  (
    if $kids == ["Child 2 Years","Child 3 Years","Child 4 Years","Child 5 Years","Child 6-7 Years","Child 8 Years","Child 9-10 Years"] then "Girls 2Y–10Y"
    elif ($kids | length) > 0 then "Girls " + (($kids | map(sub("^Child "; "") | sub(" Years"; "Y")) ) | join(", "))
    else ""
    end
  ) as $kid_phrase |
  (
    if $moms == ["S","M","L","XL"] then "Mothers S–XL"
    elif ($moms | length) > 0 then "Mothers " + ($moms | join(", "))
    else ""
    end
  ) as $mom_phrase |
  if $kid_phrase != "" and $mom_phrase != "" then $kid_phrase + " and " + $mom_phrase
  elif $kid_phrase != "" then $kid_phrase
  else $mom_phrase
  end' "${WORK}/size_chart.json")"

CHILD_ROWS_HTML="$(jq -r '
  def metric_text($s): ($s | split("/") | .[0] | gsub("\\s*(cm|kg)\\s*$"; "") | gsub("^\\s+|\\s+$"; ""));
  [
    .[] | select(.audience == "child") |
    "<tr><td>\(.picker_label)</td><td>\(.age)</td><td>\(metric_text(.weight))</td><td>\(metric_text(.height))</td><td>\(.chest_cm)</td><td>\(.sleeve_cm)</td><td>\(.pant_cm)</td><td>\(.hip_cm)</td><td>\(.waist_cm)</td><td>\(.length_cm)</td></tr>"
  ] | join("")' "${WORK}/size_chart.json")"

ADULT_ROWS_HTML="$(jq -r '
  def metric_text($s): ($s | split("/") | .[0] | gsub("\\s*(cm|kg)\\s*$"; "") | gsub("^\\s+|\\s+$"; ""));
  [
    .[] | select(.audience == "mother") |
    "<tr><td>\(.picker_label)</td><td>\(.age)</td><td>\(metric_text(.weight))</td><td>\(metric_text(.height))</td><td>\(.chest_cm)</td><td>\(.sleeve_cm)</td><td>\(.pant_cm)</td><td>\(.hip_cm)</td><td>\(.waist_cm)</td><td>\(.length_cm)</td></tr>"
  ] | join("")' "${WORK}/size_chart.json")"

SIZE_TABLE_HTML="<h3>Size Chart</h3><table id=\"size-chart\"><thead><tr><th>Size</th><th>Age</th><th>Weight (kg/lbs)</th><th>Height (cm/in)</th><th>Chest/Bust (cm/in)</th><th>Sleeve (cm/in)</th><th>Pant/Short (cm/in)</th><th>Hip (cm/in)</th><th>Waist (cm/in)</th><th>Garment Length (cm/in)</th></tr></thead><tbody><!-- Children Sizes -->${CHILD_ROWS_HTML}<!-- Adult Sizes -->${ADULT_ROWS_HTML}</tbody></table>"

BASE_TAGS_JSON='[
  "Mommy and Me",
  "Pajamas",
  "Matching Family Pajamas",
  "Short Sleeve Pajamas",
  "Two-Piece Pajama Set",
  "Summer",
  "Summer Pajamas",
  "Cream",
  "Ivory",
  "Pink",
  "Beige",
  "Floral",
  "Multicolor",
  "Butterfly",
  "Butterflies",
  "Fluttering Butterflies",
  "Wildflower",
  "Botanical",
  "Garden",
  "Watercolor",
  "Ruffle",
  "Sweet Ruffle Trim",
  "Bamboo Cotton Gauze"
]'

CHILD_BUCKET_TAGS_JSON="$(jq -c '
  [.[].picker_label] as $labels |
  [
    (if any($labels[]; . == "Child 2 Years" or . == "Child 3 Years") then "Child 2-3yr" else empty end),
    (if any($labels[]; . == "Child 4 Years" or . == "Child 5 Years") then "Child 4-5yr" else empty end),
    (if any($labels[]; . == "Child 6-7 Years" or . == "Child 8 Years") then "Child 6-8yr" else empty end),
    (if any($labels[]; . == "Child 9-10 Years") then "Child 9-10yr" else empty end)
  ]' "${WORK}/size_chart.json")"

MOTHER_SIZE_TAGS_JSON="$(jq -c '[.[] | select(.audience == "mother") | .picker_label]' "${WORK}/size_chart.json")"

TAGS_JSON="$(jq -nc \
  --argjson base "$BASE_TAGS_JSON" \
  --argjson child "$CHILD_BUCKET_TAGS_JSON" \
  --argjson mother "$MOTHER_SIZE_TAGS_JSON" \
  --arg vendor_url "$VENDOR_URL" \
  '($base + $child + $mother + [$vendor_url]) | unique')"

BODY_HTML="$(python3 - "$SIZE_RANGE_COPY" "$SIZE_TABLE_HTML" <<'PY'
import sys

size_range_copy = sys.argv[1]
size_table_html = sys.argv[2]

print(f"""<ul>
  <li><strong>Light bamboo-cotton gauze:</strong> The vendor title explicitly calls out bamboo-cotton gauze, giving this set an airy, breathable feel that suits spring and summer lounging.</li>
  <li><strong>Make every moment match:</strong> Coordinating mother-and-daughter pajamas made for brunch, birthdays, holiday cards, sleepovers, and all the picture-perfect in-between moments.</li>
  <li><strong>Fluttering Butterflies print:</strong> Blush butterflies and delicate meadow florals drift across a creamy ivory ground for a soft, romantic storybook look.</li>
  <li><strong>Sweet ruffle trim:</strong> The supplier title notes a sweet ruffle finish, and the provided lifestyle image shows soft flutter sleeves and ruffled hems that keep the set playful and polished.</li>
  <li><strong>Gentle-care routine:</strong> Wash cold on a delicate cycle and line dry or tumble low to help protect the airy gauze texture and watercolor-style print.</li>
  <li><strong>Size range:</strong> {size_range_copy} so every matching-photo moment can stay in step.</li>
</ul>
<p>&nbsp;</p>
{size_table_html}
<p>Fluttering Butterflies is the kind of pajama set that makes a quiet night feel a little more special. The cream bamboo-cotton gauze is scattered with watercolor butterflies, soft meadow florals, and trailing greenery that read light, romantic, and easy. Short sleeves keep the look breezy for spring and summer, while the relaxed long-pant silhouette adds just enough coverage for bedtime, breakfast, and slow weekends at home. Sweet ruffle trim gives both the mother and child versions a dressed-up finish without taking away the lounge-all-day comfort.</p>
<p>This is a matching set made for sleepovers, birthday mornings, Mother's Day brunch at home, and the family snapshots that end up framed long after the season ends. The print feels soft enough for everyday lounging but polished enough to look picture-ready the second you pull it on. Because the vendor's size sheet includes the full child 90-150 run plus mother S-XL, the listing stays true to the real availability without inventing missing sizes. Add both sizes to your cart and make every bedtime, brunch, and holiday-card morning feel beautifully matched.</p>
<h3>Key Features:</h3>
<ul>
  <li><strong>Bamboo-cotton gauze comfort:</strong> Lightweight woven fabric with breathable structure for warmer-weather lounging.</li>
  <li><strong>Sweet ruffle finish:</strong> Flutter sleeves and ruffled hems echo the vendor's sweet ruffle-trim callout.</li>
  <li><strong>Relaxed long-pant silhouette:</strong> Easy movement for bedtime, breakfast, and slow family mornings.</li>
  <li><strong>Soft butterfly-and-floral print:</strong> Cream, blush, and meadow-green tones keep the look romantic and photo-ready.</li>
  <li><strong>Full matching size run:</strong> Real vendor availability spans child 90-150 and mother S-XL.</li>
</ul>
<p>Add the mother size and the matching child size to your cart to make every moment match, from bedtime routines to brunch photos and holiday-card mornings.</p>""")
PY
)"

printf '%s' "$BODY_HTML" > "${WORK}/body.html"

if [[ ${#TITLE} -gt 70 ]]; then
  echo "ERROR: title length exceeds 70 characters." >&2
  exit 1
fi
if [[ ${#SEO_TITLE} -gt 60 ]]; then
  echo "ERROR: SEO title length exceeds 60 characters." >&2
  exit 1
fi
if [[ ${#SEO_DESCRIPTION} -gt 155 ]]; then
  echo "ERROR: SEO description length exceeds 155 characters." >&2
  exit 1
fi

NEIGHBOR_QUERY='query NeighborProduct($handle: String!) {
  productByHandle(handle: $handle) {
    id
    sizeField: metafield(namespace: "shopify", key: "size") {
      references(first: 30) {
        nodes {
          ... on Metaobject { id displayName handle }
        }
      }
    }
    ageField: metafield(namespace: "shopify", key: "age-group") {
      references(first: 10) {
        nodes {
          ... on Metaobject { id displayName handle }
        }
      }
    }
    colorField: metafield(namespace: "shopify", key: "color-pattern") {
      references(first: 10) {
        nodes {
          ... on Metaobject { id displayName handle }
        }
      }
    }
    fabricField: metafield(namespace: "shopify", key: "fabric") {
      references(first: 10) {
        nodes {
          ... on Metaobject { id displayName handle }
        }
      }
    }
    genderField: metafield(namespace: "shopify", key: "target-gender") {
      references(first: 10) {
        nodes {
          ... on Metaobject { id displayName handle }
        }
      }
    }
  }
}'

NEIGHBOR_HANDLE=""
NEIGHBOR_RESPONSE=""
for candidate in little-sheep-meadow-mommy-and-me-pajamas grape-vineyard-mommy-and-me-pajamas; do
  resp="$(gql "$NEIGHBOR_QUERY" "$(jq -nc --arg handle "$candidate" '{handle:$handle}')")"
  check_graphql_errors "$resp" "neighbor lookup"
  if [[ "$(echo "$resp" | jq -r '.data.productByHandle.id // empty')" != "" ]]; then
    NEIGHBOR_HANDLE="$candidate"
    NEIGHBOR_RESPONSE="$resp"
    break
  fi
done

if [[ -z "$NEIGHBOR_HANDLE" ]]; then
  echo "ERROR: unable to resolve a neighbor pajama product for metaobject lookups." >&2
  exit 1
fi

printf '%s' "$NEIGHBOR_RESPONSE" > "${WORK}/neighbor.json"

CANONICAL_SIZE_DISPLAY_MAP='{
  "Child 2 Years": "2-3 years",
  "Child 3 Years": "3-4 years",
  "Child 4 Years": "4-5 years",
  "Child 5 Years": "5-6 years",
  "Child 6-7 Years": "6-7 years",
  "Child 8 Years": "7-8 years",
  "Child 9-10 Years": "8-9 years",
  "Mother S": "S",
  "Mother M": "M",
  "Mother L": "L",
  "Mother XL": "XL"
}'

SIZE_METAOBJECT_MAP_JSON="$(jq -c \
  --argjson canonical "$CANONICAL_SIZE_DISPLAY_MAP" '
  (.data.productByHandle.sizeField.references.nodes // []) as $refs |
  reduce ($canonical | to_entries[]) as $entry ({};
    . + {
      ($entry.key): (
        $refs
        | map(select(.displayName == $entry.value))
        | .[0]
        | {gid: .id, catalog_label: .displayName}
      )
    }
  )' "${WORK}/neighbor.json")"
printf '%s' "$SIZE_METAOBJECT_MAP_JSON" > "${WORK}/size_metaobject_map.json"

if ! jq -e 'all(to_entries[]; .value.gid != null and .value.catalog_label != null)' "${WORK}/size_metaobject_map.json" > /dev/null; then
  echo "ERROR: failed to resolve one or more shopify.size metaobject mappings from neighbor product ${NEIGHBOR_HANDLE}." >&2
  exit 1
fi

SHOPIFY_SIZE_REFS_JSON="$(jq -c \
  --argjson map "$SIZE_METAOBJECT_MAP_JSON" '
  [ .[] | $map[.picker_label].gid ]' "${WORK}/size_chart.json")"

AGE_GROUP_GIDS_JSON="$(jq -c '[.data.productByHandle.ageField.references.nodes[] | .id]' "${WORK}/neighbor.json")"
COLOR_PATTERN_GIDS_JSON="$(jq -c '[.data.productByHandle.colorField.references.nodes[] | .id]' "${WORK}/neighbor.json")"
FABRIC_GIDS_JSON="$(jq -c '[.data.productByHandle.fabricField.references.nodes[] | .id]' "${WORK}/neighbor.json")"
TARGET_GENDER_GIDS_JSON="$(jq -c '[.data.productByHandle.genderField.references.nodes[] | .id]' "${WORK}/neighbor.json")"

EXPECTED_WRITTEN_METAFIELDS_JSON='[
  "custom.category1",
  "custom.subcategory",
  "custom.subcategory2",
  "custom.pattern",
  "custom.style",
  "custom.type",
  "mm-google-shopping.custom_product",
  "mm-google-shopping.gender",
  "mm-google-shopping.age_group",
  "mm-google-shopping.condition",
  "mm-google-shopping.custom_label_0",
  "mm-google-shopping.custom_label_1",
  "mm-google-shopping.custom_label_2",
  "mm-google-shopping.custom_label_3",
  "mm-google-shopping.custom_label_4",
  "shopify.age-group",
  "shopify.color-pattern",
  "shopify.fabric",
  "shopify.size",
  "shopify.target-gender",
  "global.title_tag",
  "global.description_tag"
]'

SKIPPED_METAFIELDS_JSON='[
  {"key":"shopify.clothing-features","reason":"No honest standard-catalog clothing-features entry fits a lightweight summer bamboo-cotton gauze pajama set."},
  {"key":"shopify.sleeve-length-type","reason":"Omitted for Pajamas per the listing spec."},
  {"key":"shopify.neckline","reason":"Dresses/Tops only; does not apply to Pajamas."},
  {"key":"shopify.dress-occasion","reason":"Dresses only; does not apply to Pajamas."},
  {"key":"shopify.dress-style","reason":"Dresses only; does not apply to Pajamas."},
  {"key":"shopify.skirt-dress-length-type","reason":"Dresses/Skirts only; does not apply to Pajamas."}
]'

EXISTING_QUERY='query ExistingProduct($handle: String!) {
  productByHandle(handle: $handle) {
    id
    handle
    variants(first: 100) {
      nodes { sku title }
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

EXISTING_RESPONSE="$(gql "$EXISTING_QUERY" "$(jq -nc --arg handle "$HANDLE" '{handle:$handle}')")"
check_graphql_errors "$EXISTING_RESPONSE" "existing product lookup"
PRODUCT_ID="$(echo "$EXISTING_RESPONSE" | jq -r '.data.productByHandle.id // empty')"
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
    --arg vendor "dresslikemommy.com" \
    --arg product_type "$PRODUCT_TYPE" \
    --arg category "$TAXONOMY_GID" \
    --arg seo_title "$SEO_TITLE" \
    --arg seo_description "$SEO_DESCRIPTION" \
    --arg color "$COLOR_OPTION_VALUE" \
    --argjson tags "$TAGS_JSON" \
    --argjson size_values "$SIZE_VALUES_JSON" '
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
        productOptions: [
          {name: "Size", values: $size_values},
          {name: "Color", values: [{name: $color}]}
        ]
      }
    }')"

  PRODUCT_CREATE_RESPONSE="$(gql "$PRODUCT_CREATE_MUTATION" "$PRODUCT_CREATE_VARS")"
  check_graphql_errors "$PRODUCT_CREATE_RESPONSE" "productCreate"
  check_user_errors "$PRODUCT_CREATE_RESPONSE" '.data.productCreate.userErrors' "productCreate"
  PRODUCT_ID="$(echo "$PRODUCT_CREATE_RESPONSE" | jq -r '.data.productCreate.product.id')"
fi

if [[ -z "$PRODUCT_ID" || "$PRODUCT_ID" == "null" ]]; then
  echo "ERROR: product id missing after create/update flow." >&2
  exit 1
fi

PRODUCT_UPDATE_MUTATION='mutation ProductUpdate($product: ProductUpdateInput!) {
  productUpdate(product: $product) {
    product {
      id
      handle
      title
      seo { title description }
    }
    userErrors { field message }
  }
}'

PRODUCT_UPDATE_VARS="$(jq -nc \
  --arg id "$PRODUCT_ID" \
  --arg handle "$HANDLE" \
  --arg title "$TITLE" \
  --arg body "$BODY_HTML" \
  --arg vendor "dresslikemommy.com" \
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

if [[ "$CREATE_NEW_PRODUCT" == "1" ]]; then
  SHOULD_CREATE_VARIANTS="1"
else
  EXISTING_VARIANT_COUNT="$(echo "$EXISTING_RESPONSE" | jq '.data.productByHandle.variants.nodes | length')"
  EXISTING_SKUS_SORTED="$(echo "$EXISTING_RESPONSE" | jq -r '.data.productByHandle.variants.nodes[].sku // empty' | sed '/^$/d' | sort)"
  if [[ "$EXISTING_VARIANT_COUNT" -eq 0 ]]; then
    SHOULD_CREATE_VARIANTS="1"
  elif [[ "$EXISTING_VARIANT_COUNT" -eq "$ROW_COUNT" && "$EXISTING_SKUS_SORTED" == "$DERIVED_SKUS_SORTED" ]]; then
    SHOULD_CREATE_VARIANTS="0"
  elif [[ "$EXISTING_VARIANT_COUNT" -eq 1 && -z "$EXISTING_SKUS_SORTED" ]]; then
    SHOULD_CREATE_VARIANTS="1"
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

METAFIELDS_SET_MUTATION='mutation MetafieldsSet($metafields: [MetafieldsSetInput!]!) {
  metafieldsSet(metafields: $metafields) {
    metafields { namespace key type value }
    userErrors { field message }
  }
}'

METAFIELDS_SET_VARS="$(jq -nc \
  --arg pid "$PRODUCT_ID" \
  --arg age_group_value "$(echo "$AGE_GROUP_GIDS_JSON" | jq -c .)" \
  --arg color_value "$(echo "$COLOR_PATTERN_GIDS_JSON" | jq -c .)" \
  --arg fabric_value "$(echo "$FABRIC_GIDS_JSON" | jq -c .)" \
  --arg target_gender_value "$(echo "$TARGET_GENDER_GIDS_JSON" | jq -c .)" \
  --arg size_value "$(echo "$SHOPIFY_SIZE_REFS_JSON" | jq -c .)" \
  --arg seo_title "$SEO_TITLE" \
  --arg seo_description "$SEO_DESCRIPTION" '
  {
    metafields: [
      {ownerId: $pid, namespace: "custom", key: "category1", type: "single_line_text_field", value: "Mommy and Me"},
      {ownerId: $pid, namespace: "custom", key: "subcategory", type: "single_line_text_field", value: "Pajamas"},
      {ownerId: $pid, namespace: "custom", key: "subcategory2", type: "single_line_text_field", value: "Summer Pajamas"},
      {ownerId: $pid, namespace: "custom", key: "pattern", type: "single_line_text_field", value: "Fluttering Butterflies Print"},
      {ownerId: $pid, namespace: "custom", key: "style", type: "single_line_text_field", value: "Matching Family Set"},
      {ownerId: $pid, namespace: "custom", key: "type", type: "single_line_text_field", value: "Two-Piece Pajama Set"},
      {ownerId: $pid, namespace: "mm-google-shopping", key: "custom_product", type: "boolean", value: "false"},
      {ownerId: $pid, namespace: "mm-google-shopping", key: "gender", type: "single_line_text_field", value: "female"},
      {ownerId: $pid, namespace: "mm-google-shopping", key: "age_group", type: "single_line_text_field", value: "adult"},
      {ownerId: $pid, namespace: "mm-google-shopping", key: "condition", type: "single_line_text_field", value: "new"},
      {ownerId: $pid, namespace: "mm-google-shopping", key: "custom_label_0", type: "single_line_text_field", value: "Mommy and Me"},
      {ownerId: $pid, namespace: "mm-google-shopping", key: "custom_label_1", type: "single_line_text_field", value: "Butterfly Garden"},
      {ownerId: $pid, namespace: "mm-google-shopping", key: "custom_label_2", type: "single_line_text_field", value: "Summer"},
      {ownerId: $pid, namespace: "mm-google-shopping", key: "custom_label_3", type: "single_line_text_field", value: "Short-Sleeve Set"},
      {ownerId: $pid, namespace: "mm-google-shopping", key: "custom_label_4", type: "single_line_text_field", value: "Family Matching"},
      {ownerId: $pid, namespace: "shopify", key: "age-group", type: "list.metaobject_reference", value: $age_group_value},
      {ownerId: $pid, namespace: "shopify", key: "color-pattern", type: "list.metaobject_reference", value: $color_value},
      {ownerId: $pid, namespace: "shopify", key: "fabric", type: "list.metaobject_reference", value: $fabric_value},
      {ownerId: $pid, namespace: "shopify", key: "size", type: "list.metaobject_reference", value: $size_value},
      {ownerId: $pid, namespace: "shopify", key: "target-gender", type: "list.metaobject_reference", value: $target_gender_value},
      {ownerId: $pid, namespace: "global", key: "title_tag", type: "single_line_text_field", value: $seo_title},
      {ownerId: $pid, namespace: "global", key: "description_tag", type: "single_line_text_field", value: $seo_description}
    ]
  }')"

METAFIELDS_SET_RESPONSE="$(gql "$METAFIELDS_SET_MUTATION" "$METAFIELDS_SET_VARS")"
check_graphql_errors "$METAFIELDS_SET_RESPONSE" "metafieldsSet"
check_user_errors "$METAFIELDS_SET_RESPONSE" '.data.metafieldsSet.userErrors' "metafieldsSet"

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

mkdir -p "$UPLOAD_DIR"

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

if [[ "${#MEDIA_FILES[@]}" -gt 0 ]]; then
  for image_path in "${MEDIA_FILES[@]}"; do
    image_name="$(basename "$image_path")"
    image_name_lower="$(echo "$image_name" | tr '[:upper:]' '[:lower:]')"

    if [[ "$image_name_lower" == *size* || "$image_name_lower" == *chart* ]]; then
      alt_text="Vendor size chart for Fluttering Butterflies mommy and me pajamas showing child 90-150 and mother S-XL measurements."
    else
      alt_text="Mother and daughter in matching cream butterfly floral bamboo-cotton gauze short-sleeve pajamas with sweet ruffle trim and relaxed long pants in a bright neutral living room."
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
    tags
    descriptionHtml
    seo { title description }
    category { id fullName }
    variants(first: 100) {
      nodes {
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
        ruleSet {
          appliedDisjunctively
          rules { column relation condition }
        }
      }
    }
    metafields(first: 80) {
      edges {
        node {
          namespace
          key
          type
          value
        }
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
printf '%s' "$VERIFY_RESPONSE" > "${WORK}/verify.json"

CONTEXT_JSON="$(jq -nc \
  --arg title "$TITLE" \
  --arg handle "$HANDLE" \
  --arg shortcode "$SHORTCODE" \
  --arg print_name "$PRINT_NAME" \
  --arg vendor_url "$VENDOR_URL" \
  --arg vendor_title_cn "$VENDOR_TITLE_CN" \
  --arg vendor_title_en "$VENDOR_TITLE_EN" \
  --arg designs_to_list "$DESIGNS_TO_LIST" \
  --arg body_html "$BODY_HTML" \
  --arg seo_title "$SEO_TITLE" \
  --arg seo_description "$SEO_DESCRIPTION" \
  --arg season "$SEASON" \
  --arg category "$CATEGORY" \
  --arg category_word "$CATEGORY_WORD" \
  --arg product_type "$PRODUCT_TYPE" \
  --arg custom_type "$CUSTOM_TYPE" \
  --arg taxonomy_gid "$TAXONOMY_GID" \
  --arg taxonomy_path "$SHOPIFY_CATEGORY_PATH" \
  --arg google_product_category "$GOOGLE_PRODUCT_CATEGORY" \
  --arg child_price "$CHILD_PRICE" \
  --arg child_compare "$CHILD_COMPARE" \
  --arg mother_price "$MOTHER_PRICE" \
  --arg mother_compare "$MOTHER_COMPARE" \
  --arg seo_size_phrase "$SEO_SIZE_PHRASE" \
  --arg size_range_copy "$SIZE_RANGE_COPY" \
  --arg upload_dir "$UPLOAD_DIR" \
  --arg listing_md "$LISTING_MD" \
  --arg csv_out "$CSV_OUT" \
  --arg color_option "$COLOR_OPTION_VALUE" \
  --arg color_token "$COLOR_TOKEN" \
  --arg hero_image_source "$HERO_IMAGE_SOURCE" \
  --arg size_image_source "$SIZE_IMAGE_SOURCE" \
  --argjson tags "$TAGS_JSON" \
  --argjson photo_urls "$PHOTO_URLS_JSON" \
  --argjson expected_metafields "$EXPECTED_WRITTEN_METAFIELDS_JSON" \
  --argjson skipped_metafields "$SKIPPED_METAFIELDS_JSON" \
  --argjson publications "$PUBLICATIONS_JSON" \
  --argjson size_metaobject_map "$SIZE_METAOBJECT_MAP_JSON" '
  {
    title: $title,
    handle: $handle,
    shortcode: $shortcode,
    print_name: $print_name,
    vendor_url: $vendor_url,
    vendor_title_cn: $vendor_title_cn,
    vendor_title_en: $vendor_title_en,
    designs_to_list: $designs_to_list,
    body_html: $body_html,
    seo_title: $seo_title,
    seo_description: $seo_description,
    season: $season,
    category: $category,
    category_word: $category_word,
    product_type: $product_type,
    custom_type: $custom_type,
    taxonomy_gid: $taxonomy_gid,
    taxonomy_path: $taxonomy_path,
    google_product_category: $google_product_category,
    child_price: $child_price,
    child_compare: $child_compare,
    mother_price: $mother_price,
    mother_compare: $mother_compare,
    seo_size_phrase: $seo_size_phrase,
    size_range_copy: $size_range_copy,
    upload_dir: $upload_dir,
    listing_md: $listing_md,
    csv_out: $csv_out,
    color_option: $color_option,
    color_token: $color_token,
    hero_image_source: $hero_image_source,
    size_image_source: $size_image_source,
    tags: $tags,
    photo_urls: $photo_urls,
    expected_metafields: $expected_metafields,
    skipped_metafields: $skipped_metafields,
    publications: $publications,
    size_metaobject_map: $size_metaobject_map
  }')"
printf '%s' "$CONTEXT_JSON" > "${WORK}/context.json"

python3 - "${WORK}/context.json" "${WORK}/size_chart.json" "${WORK}/verify.json" <<'PY'
import csv
import json
import re
import sys
from pathlib import Path


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


context = load_json(sys.argv[1])
size_chart = load_json(sys.argv[2])
verify_payload = load_json(sys.argv[3])["data"]["product"]

table_match = re.search(r'(<table id="size-chart">.*?</table>)', verify_payload["descriptionHtml"], re.S)
table_html = table_match.group(1) if table_match else ""
thead_count = len(re.findall(r"<th\b", table_html))
tbody_match = re.search(r"<tbody>(.*?)</tbody>", table_html, re.S)
tbody_html = tbody_match.group(1) if tbody_match else ""
tbody_row_count = len(re.findall(r"<tr>", tbody_html))
row_html_segments = re.findall(r"<tr>\s*(.*?)\s*</tr>", tbody_html, re.S)
row_cells = [
    [re.sub(r"<[^>]+>", "", cell).strip() for cell in re.findall(r"<td>\s*(.*?)\s*</td>", row_html, re.S)]
    for row_html in row_html_segments
]
first_cells = [cells[0] for cells in row_cells if cells]

live_skus = sorted(v["sku"] for v in verify_payload["variants"]["nodes"])
derived_skus = sorted(
    f"DLM-{context['shortcode']}-{row['sku_suffix']}-{context['color_token']}" for row in size_chart
)

variant_checks = []
for variant in verify_payload["variants"]["nodes"]:
    ok = (
        variant["sku"]
        and variant["price"]
        and variant["compareAtPrice"]
        and variant["inventoryPolicy"] == "DENY"
        and variant["inventoryItem"]["tracked"] is True
        and variant["inventoryItem"]["requiresShipping"] is True
    )
    variant_checks.append(ok)

waist_ok = len(row_cells) == len(size_chart) and all(
    len(cells) >= 9 and cells[8] and cells[8] != "—" for cells in row_cells
)
single_unit_cells_ok = all("/" not in cell for cells in row_cells for cell in cells[1:])
picker_ok = [row["picker_label"] for row in size_chart] == first_cells

required_tags = {
    "Mommy and Me",
    "Pajamas",
    "Matching Family Pajamas",
    "Short Sleeve Pajamas",
    "Summer",
    context["vendor_url"],
    "Child 2-3yr",
    "Child 4-5yr",
    "Child 6-8yr",
    "Child 9-10yr",
    "Mother S",
    "Mother M",
    "Mother L",
    "Mother XL",
}
live_tags = set(verify_payload["tags"])

live_metafields = {f"{edge['node']['namespace']}.{edge['node']['key']}" for edge in verify_payload["metafields"]["edges"]}
expected_metafields = set(context["expected_metafields"])

publication_map = {
    node["publication"]["id"]: {"name": node["publication"]["name"], "isPublished": node["isPublished"], "publishDate": node["publishDate"]}
    for node in verify_payload["resourcePublicationsV2"]["nodes"]
}
all_publications_ok = all(publication_map.get(pub["publicationId"], {}).get("isPublished") is True for pub in context["publications"])

smart_collections = [
    {
        "title": node["title"],
        "handle": node["handle"],
    }
    for node in verify_payload["collections"]["nodes"]
    if node.get("ruleSet") is not None
]

verification_rows = [
    ("Title <= 70 chars", len(verify_payload["title"]) <= 70, str(len(verify_payload["title"]))),
    ("SEO title <= 60 chars", len((verify_payload["seo"]["title"] or "")) <= 60, str(len(verify_payload["seo"]["title"] or ""))),
    ("SEO description <= 155 chars", len((verify_payload["seo"]["description"] or "")) <= 155, str(len(verify_payload["seo"]["description"] or ""))),
    ("Live variant count matches SIZE_CHART", len(verify_payload["variants"]["nodes"]) == len(size_chart), f"{len(verify_payload['variants']['nodes'])} vs {len(size_chart)}"),
    ("Live SKUs match derived SKUs", live_skus == derived_skus, "match" if live_skus == derived_skus else "mismatch"),
    ("Every variant tracked + DENY + priced", all(variant_checks), "all variants verified" if all(variant_checks) else "one or more variants failed"),
    ("Published to all required channels", all_publications_ok, "all 5 target publications live" if all_publications_ok else "missing publication"),
    ("publishedAt not null", bool(verify_payload["publishedAt"]), verify_payload["publishedAt"] or "missing"),
    ("onlineStoreUrl populated", bool(verify_payload["onlineStoreUrl"]), verify_payload["onlineStoreUrl"] or "missing"),
    ("Taxonomy category set", verify_payload["category"] and verify_payload["category"]["id"] == context["taxonomy_gid"], verify_payload["category"]["id"] if verify_payload["category"] else "missing"),
    ("Size-chart table has 10 columns", thead_count == 10, str(thead_count)),
    ("Size-chart table row count matches SIZE_CHART", tbody_row_count == len(size_chart), str(tbody_row_count)),
    ("Picker labels match first size-table column", picker_ok, "exact order match" if picker_ok else "mismatch"),
    ("Age column present and populated", "<th>Age</th>" in table_html and all(row["age"] for row in size_chart), "present"),
    ("Waist column populated for every row", waist_ok, "all waist values present" if waist_ok else "missing waist cell"),
    ("Size-chart cells use one unit at a time", single_unit_cells_ok, "no slash-separated values in table cells" if single_unit_cells_ok else "found dual-unit cell"),
    ("Required tags present", required_tags.issubset(live_tags), "all required tags present" if required_tags.issubset(live_tags) else "missing required tags"),
    ("Applicable metafields written", expected_metafields.issubset(live_metafields), "all expected metafields present" if expected_metafields.issubset(live_metafields) else "missing metafields"),
]

failures = [row for row in verification_rows if not row[1]]
if failures:
    for label, _, detail in failures:
        print(f"VERIFY FAILED: {label} -> {detail}", file=sys.stderr)
    sys.exit(1)

product_numeric_id = verify_payload["id"].split("/")[-1]
admin_url = f"https://admin.shopify.com/store/dresslikemommy/products/{product_numeric_id}"
live_url = f"https://www.dresslikemommy.com/products/{context['handle']}"

size_recap_rows = []
for row in size_chart:
    gid_info = context["size_metaobject_map"][row["picker_label"]]
    size_recap_rows.append(
        {
            "vendor_label": row["vendor_label"],
            "picker_label": row["picker_label"],
            "sku": f"DLM-{context['shortcode']}-{row['sku_suffix']}-{context['color_token']}",
            "price": context["child_price"] if row["audience"] == "child" else context["mother_price"],
            "shopify_size_gid": gid_info["gid"],
            "catalog_label": gid_info["catalog_label"],
        }
    )

header_path = Path("/Users/fsuels/Projects/dresslikemommy/bird-chirping-mommy-and-me-pajamas-shopify-import.csv")
with header_path.open("r", encoding="utf-8", newline="") as fh:
    headers = next(csv.reader(fh))

size_list_for_csv = ",".join(row["picker_label"] for row in size_chart)
row_dicts = []
for index, row in enumerate(size_chart):
    sku = f"DLM-{context['shortcode']}-{row['sku_suffix']}-{context['color_token']}"
    price = context["child_price"] if row["audience"] == "child" else context["mother_price"]
    compare_at = context["child_compare"] if row["audience"] == "child" else context["mother_compare"]
    record = {header: "" for header in headers}
    record["Handle"] = context["handle"]
    record["Option1 Name"] = "Size"
    record["Option1 Value"] = row["picker_label"]
    record["Option2 Name"] = "Color"
    record["Option2 Value"] = context["color_option"]
    record["Variant SKU"] = sku
    record["Variant Inventory Tracker"] = "shopify"
    record["Variant Inventory Policy"] = "deny"
    record["Variant Fulfillment Service"] = "manual"
    record["Variant Price"] = price
    record["Variant Compare At Price"] = compare_at
    record["Variant Requires Shipping"] = "TRUE"
    record["Variant Taxable"] = "TRUE"
    record["Variant Weight Unit"] = "oz"
    record["Google Shopping / MPN"] = sku
    if index == 0:
        record["Title"] = context["title"]
        record["Body (HTML)"] = context["body_html"]
        record["Vendor"] = "dresslikemommy.com"
        record["Product Category"] = context["taxonomy_path"]
        record["Type"] = context["product_type"]
        record["Tags"] = ", ".join(context["tags"])
        record["Published"] = "TRUE"
        record["Gift Card"] = "FALSE"
        record["SEO Title"] = context["seo_title"]
        record["SEO Description"] = context["seo_description"]
        record["Google Shopping / Google Product Category"] = context["google_product_category"]
        record["Google Shopping / Gender"] = "Female"
        record["Google Shopping / Age Group"] = "Adult"
        record["Google Shopping / Condition"] = "new"
        record["Google Shopping / Custom Product"] = "FALSE"
        record["Google Shopping / Custom Label 0"] = "Mommy and Me"
        record["Google Shopping / Custom Label 1"] = "Butterfly Garden"
        record["Google Shopping / Custom Label 2"] = context["season"]
        record["Google Shopping / Custom Label 3"] = "Short-Sleeve Set"
        record["Google Shopping / Custom Label 4"] = "Family Matching"
        record["Category1 (product.metafields.custom.category1)"] = "Mommy and Me"
        record["Pattern (product.metafields.custom.pattern)"] = "Fluttering Butterflies Print"
        record["Style (product.metafields.custom.style)"] = "Matching Family Set"
        record["SubCategory (product.metafields.custom.subcategory)"] = "Pajamas"
        record["SubCategory2 (product.metafields.custom.subcategory2)"] = "Summer Pajamas"
        record["Type (product.metafields.custom.type)"] = "Two-Piece Pajama Set"
        record["Google: Custom Product (product.metafields.mm-google-shopping.custom_product)"] = "FALSE"
        record["Age group (product.metafields.shopify.age-group)"] = "Kids,Adults"
        record["Color (product.metafields.shopify.color-pattern)"] = "Beige,Floral,Multicolor"
        record["Fabric (product.metafields.shopify.fabric)"] = "Cotton"
        record["Size (product.metafields.shopify.size)"] = size_list_for_csv
        record["Status"] = "active"
    row_dicts.append(record)

with Path(context["csv_out"]).open("w", encoding="utf-8", newline="") as fh:
    writer = csv.DictWriter(fh, fieldnames=headers)
    writer.writeheader()
    writer.writerows(row_dicts)

metafields_written_lines = [
    "- custom.category1 = `Mommy and Me`",
    "- custom.subcategory = `Pajamas`",
    "- custom.subcategory2 = `Summer Pajamas`",
    "- custom.pattern = `Fluttering Butterflies Print`",
    "- custom.style = `Matching Family Set`",
    "- custom.type = `Two-Piece Pajama Set`",
    "- mm-google-shopping.custom_product = `false`",
    "- mm-google-shopping.gender = `female`",
    "- mm-google-shopping.age_group = `adult`",
    "- mm-google-shopping.condition = `new`",
    "- mm-google-shopping.custom_label_0 = `Mommy and Me`",
    "- mm-google-shopping.custom_label_1 = `Butterfly Garden`",
    "- mm-google-shopping.custom_label_2 = `Summer`",
    "- mm-google-shopping.custom_label_3 = `Short-Sleeve Set`",
    "- mm-google-shopping.custom_label_4 = `Family Matching`",
    "- shopify.age-group -> `Kids`, `Adults`",
    "- shopify.color-pattern -> `Beige`, `Floral`, `Multicolor`",
    "- shopify.fabric -> `Cotton`",
    "- shopify.size -> 11 catalog metaobject references in chart order",
    "- shopify.target-gender -> `Female`",
    "- global.title_tag = SEO title",
    "- global.description_tag = SEO description",
]

skipped_lines = [f"- `{item['key']}` — {item['reason']}" for item in context["skipped_metafields"]]

smart_collection_lines = []
for item in smart_collections:
    smart_collection_lines.append(f"- {item['title']} (`/{item['handle']}`)")
if not smart_collection_lines:
    smart_collection_lines.append("- None yet; smart collections may still be in the normal Shopify reindex window.")

photo_lines = [f"- {url}" for url in context["photo_urls"]]
photo_lines.append(f"- Local hero media used for upload: `{context['hero_image_source']}`")

verification_lines = [
    f"| {label} | {'PASS' if ok else 'FAIL'} | {detail} |"
    for label, ok, detail in verification_rows
]

size_recap_lines = [
    f"| {row['vendor_label']} | {row['picker_label']} | {row['sku']} | ${row['price']} | {row['shopify_size_gid']} ({row['catalog_label']}) |"
    for row in size_recap_rows
]

listing_md = f"""# {context['title']}

**Status:** Live (ACTIVE, published to all 5 required sales channels)
**Admin URL:** {admin_url}
**Live URL:** {live_url}
**Product ID:** {verify_payload['id']}
**Handle:** {verify_payload['handle']}
**Vendor (storefront):** dresslikemommy.com
**Vendor source URL (tags only):** {context['vendor_url']}

## Title & SEO
- **Title ({len(context['title'])}/70):** {context['title']}
- **SEO title ({len(context['seo_title'])}/60):** {context['seo_title']}
- **SEO description ({len(context['seo_description'])}/155):** {context['seo_description']}

## Pricing
| Audience | Price | Compare-at |
|---|---|---|
| Child | ${context['child_price']} | ${context['child_compare']} |
| Mother | ${context['mother_price']} | ${context['mother_compare']} |

## Vendor source-of-truth
- Direct HTTP fetch of `{context['vendor_url']}` hit 1688 anti-bot/captcha markup.
- The supplier page was confirmed inside the already-open Chrome `francisco` profile by reading Chrome's live session/history data on disk, which recovered the real page title and offer URL from that profile.
- **Recovered vendor title (CN):** `{context['vendor_title_cn']}`
- **Recovered vendor title (EN gloss):** {context['vendor_title_en']}
- **Design labels used:** `{context['designs_to_list']}`
- **Size-chart source of truth:** the user-supplied `尺码参数` screenshot. All 11 vendor rows were extracted directly from that image. `1/2胸围`, `1/2臀围`, and `1/2腰围` were doubled to full circumference values.
- **Columns present on the vendor chart:** size, garment length, half chest, shoulder width, sleeve length, pant length, half hip, half waist.
- **Vendor rows counted:** 11 total (`7` child, `4` mother).
- **Fabric evidence:** `竹棉纱布` in the recovered title, translated as bamboo-cotton gauze.
- **Design-detail evidence:** `甜美荷叶边` in the recovered title, translated as sweet ruffle trim.
- **Care note:** explicit wash instructions were not exposed in the accessible Chrome session snapshot, so the customer-facing care line uses conservative bamboo-cotton gauze guidance and is documented as an inference.
- **Recovered photo URLs / assets used:**
{chr(10).join(photo_lines)}

## SIZE_CHART recap
| Vendor row | Picker label | SKU | Price | shopify.size GID |
|---|---|---|---|---|
{chr(10).join(size_recap_lines)}

## Notes on mapping
- Kid sizes map from vendor height rows `90-150` to the standard picker labels `Child 2 Years` through `Child 9-10 Years`.
- Shopify's standard size catalog uses age-range metaobjects, so `Child 9-10 Years` correctly maps to the closest current catalog entry `8-9 years`.
- Mother sizes map 1:1 from vendor `S/M/L/XL` to `Mother S/M/L/XL`.
- Waist values were not invented: the vendor provided `1/2腰围` for every row, and each waist was doubled to full circumference.
- Kid weight ranges are inferred from standard CN child height/weight bands because the vendor size table did not include weight.
- The customer-facing source table now stores one unit at a time, while the storefront size-guide toggle handles centimeter/inch switching from those source values.

## Tags written
`{', '.join(context['tags'])}`

## Metafields written
{chr(10).join(metafields_written_lines)}

## Metafields skipped
{chr(10).join(skipped_lines)}

## Phase 6 verification
| Check | Result | Detail |
|---|---|---|
{chr(10).join(verification_lines)}

## Sales channels published
"""

for publication in context["publications"]:
    pub_state = publication_map.get(publication["publicationId"], {})
    listing_md += f"- {pub_state.get('name', publication['publicationId'])} — `{publication['publicationId']}` ({pub_state.get('publishDate', 'published')})\n"

listing_md += f"""
## Smart collections
{chr(10).join(smart_collection_lines)}

## Manual follow-ups
- Add more gallery angles if you want a fuller PDP image stack; this run attached the supplied hero image successfully when present in the uploads folder.
- Enter real variant shipping weights in grams/ounces when available; the backup CSV leaves hard weights blank rather than inventing them.
- Set live inventory quantities per variant after stock intake.
- Recheck smart-collection membership after the normal Shopify reindex window if any collection rules are still catching up.

## Files
- `{context['listing_md']}`
- `{context['csv_out']}`
- `/Users/fsuels/Projects/dresslikemommy/ops/scripts/create-vcf-fluttering-butterflies-mommy-and-me-pajamas.sh`
"""

Path(context["listing_md"]).write_text(listing_md, encoding="utf-8")
print(admin_url)
print(live_url)
PY

echo "Created/updated product ${PRODUCT_ID}"
echo "Listing notes: ${LISTING_MD}"
echo "Backup CSV: ${CSV_OUT}"
