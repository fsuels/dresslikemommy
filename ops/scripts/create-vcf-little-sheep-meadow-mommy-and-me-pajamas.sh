#!/usr/bin/env bash
# ============================================================================
#  VCF — Little Sheep Meadow Mommy-and-Me Pajama Listing (Shopify Admin 2025-01)
#
#  Vendor source: https://detail.1688.com/offer/1028115745039.html
#
#  DESIGN PRINCIPLE — single source of truth: the VENDOR_SIZE_CHART JSON block
#  below drives EVERYTHING downstream (option values, variants, SKUs, body
#  HTML size table, tags, shopify.size metafield, SEO description, summary).
#  Change the chart and every artifact stays in lockstep.
# ============================================================================
set -euo pipefail

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

gql() {
  curl -sS -X POST "$API" \
    -H "X-Shopify-Access-Token: $TOKEN" \
    -H "Content-Type: application/json" \
    -d "$(jq -nc --arg q "$1" --argjson v "$2" '{query:$q, variables:$v}')"
}

check_user_errors() {
  local resp="$1" path="$2" label="$3"
  local errs
  errs=$(echo "$resp" | jq -c "$path // []")
  if [[ "$errs" != "[]" && "$errs" != "null" ]]; then
    echo "ERROR: $label userErrors: $errs" >&2
    exit 1
  fi
}

# ============================================================================
#  CONFIG
# ============================================================================
HANDLE="little-sheep-meadow-mommy-and-me-pajamas"
TITLE="Little Sheep Meadow Mommy and Me Pajamas — Short-Sleeve Set"
VENDOR="dresslikemommy.com"
PTYPE="Matching Family Pajamas"
SEO_TITLE="Lamb Mommy & Me Pajamas — Matching Set | Dress Like Mommy"
CATEGORY_GID="gid://shopify/TaxonomyCategory/aa-1-17-4"
VENDOR_URL="https://detail.1688.com/offer/1028115745039.html"

SHORTCODE="VCF"
COLOR_TOKEN="CREAM"
COLOR_NAME="Little Sheep Meadow Cream"

CHILD_PRICE="32.99"
CHILD_COMPARE="37.99"
MOTHER_PRICE="35.99"
MOTHER_COMPARE="41.49"

# ============================================================================
#  VENDOR_SIZE_CHART — single source of truth (from 尺码参数 table)
#  Child rows 90/100/110/120/130/140/150 + Mother S/M/L/XL.
#  chest_cm = 1/2胸围 doubled. hip_cm = 1/2臀围 doubled. waist_cm = 腰围*2.
#  height/weight inferred from CN kid pajama bands + adult fit bands.
# ============================================================================
VENDOR_SIZE_CHART=$(cat <<'JSON'
[
  {"audience":"child","label":"Child 2 Years",    "sku_suffix":"KID2Y", "age":"2",   "weight":"12–14 kg / 26–31 lbs","height":"85–95 cm / 33–37 in",  "chest_cm":67,"sleeve_cm":16,  "pant_cm":52,"hip_cm":65,"waist_cm":42,"length_cm":35.5},
  {"audience":"child","label":"Child 3 Years",    "sku_suffix":"KID3Y", "age":"3",   "weight":"14–16 kg / 31–35 lbs","height":"95–105 cm / 37–41 in", "chest_cm":71,"sleeve_cm":16.5,"pant_cm":57,"hip_cm":69,"waist_cm":44,"length_cm":39.5},
  {"audience":"child","label":"Child 4 Years",    "sku_suffix":"KID4Y", "age":"4",   "weight":"16–19 kg / 35–42 lbs","height":"105–115 cm / 41–45 in","chest_cm":75,"sleeve_cm":17,  "pant_cm":62,"hip_cm":73,"waist_cm":46,"length_cm":42},
  {"audience":"child","label":"Child 5 Years",    "sku_suffix":"KID5Y", "age":"5",   "weight":"19–22 kg / 42–49 lbs","height":"115–125 cm / 45–49 in","chest_cm":79,"sleeve_cm":17.5,"pant_cm":67,"hip_cm":77,"waist_cm":48,"length_cm":45},
  {"audience":"child","label":"Child 6-7 Years", "sku_suffix":"KID67Y","age":"6–7", "weight":"22–26 kg / 49–57 lbs","height":"125–135 cm / 49–53 in","chest_cm":83,"sleeve_cm":18,  "pant_cm":72,"hip_cm":81,"waist_cm":50,"length_cm":48},
  {"audience":"child","label":"Child 8 Years",    "sku_suffix":"KID8Y", "age":"8",   "weight":"26–30 kg / 57–66 lbs","height":"135–145 cm / 53–57 in","chest_cm":87,"sleeve_cm":18.5,"pant_cm":77,"hip_cm":84,"waist_cm":52,"length_cm":52},
  {"audience":"child","label":"Child 9-10 Years","sku_suffix":"KID910Y","age":"9–10","weight":"30–35 kg / 66–77 lbs","height":"145–155 cm / 57–61 in","chest_cm":91,"sleeve_cm":19,  "pant_cm":83,"hip_cm":88,"waist_cm":54,"length_cm":56},
  {"audience":"mother","label":"Mother S", "sku_suffix":"MOMS", "age":"—","weight":"45–52 kg / 99–115 lbs", "height":"155–160 cm / 61–63 in","chest_cm":99, "sleeve_cm":22.5,"pant_cm":97, "hip_cm":95, "waist_cm":72,"length_cm":62},
  {"audience":"mother","label":"Mother M", "sku_suffix":"MOMM", "age":"—","weight":"52–58 kg / 115–128 lbs","height":"160–165 cm / 63–65 in","chest_cm":103,"sleeve_cm":23,  "pant_cm":99, "hip_cm":99, "waist_cm":74,"length_cm":64},
  {"audience":"mother","label":"Mother L", "sku_suffix":"MOML", "age":"—","weight":"58–65 kg / 128–143 lbs","height":"163–170 cm / 64–67 in","chest_cm":107,"sleeve_cm":24,  "pant_cm":101,"hip_cm":103,"waist_cm":76,"length_cm":66},
  {"audience":"mother","label":"Mother XL","sku_suffix":"MOMXL","age":"—","weight":"65–72 kg / 143–159 lbs","height":"165–172 cm / 65–68 in","chest_cm":111,"sleeve_cm":25.5,"pant_cm":103,"hip_cm":107,"waist_cm":78,"length_cm":68}
]
JSON
)

# ============================================================================
#  SIZE_METAOBJECT_MAP — shopify.size standard catalog GIDs.
#  Our store catalog uses age-range labels for kids; we map picker labels
#  to the closest standard catalog entry. Unmapped labels are SKIPPED.
# ============================================================================
SIZE_METAOBJECT_MAP=$(cat <<'JSON'
{
  "Child 2 Years":    "gid://shopify/Metaobject/129972863073",
  "Child 3 Years":    "gid://shopify/Metaobject/129972895841",
  "Child 4 Years":    "gid://shopify/Metaobject/129972928609",
  "Child 5 Years":    "gid://shopify/Metaobject/129972961377",
  "Child 6-7 Years":  "gid://shopify/Metaobject/139840323681",
  "Child 8 Years":    "gid://shopify/Metaobject/139840356449",
  "Child 9-10 Years": "gid://shopify/Metaobject/139840389217",
  "Mother S":         "gid://shopify/Metaobject/129975255137",
  "Mother M":         "gid://shopify/Metaobject/129975222369",
  "Mother L":         "gid://shopify/Metaobject/129975189601",
  "Mother XL":        "gid://shopify/Metaobject/129975287905"
}
JSON
)

# ============================================================================
#  DESCRIPTIVE COPY
# ============================================================================
read -r -d '' BULLETS_HTML <<'HTML' || true
<ul><li><strong>Soft breathable cotton:</strong> Lightweight double-gauze-style cotton with a gentle hand-feel — airy for summer sleep and kind to little cheeks.</li><li><strong>Make every moment match:</strong> Coordinating mother-and-daughter short-sleeve pajama sets built for slumber parties, lazy Sundays, holiday mornings, and photo-ready family bonding.</li><li><strong>Little Sheep Meadow watercolor print:</strong> A pastoral storybook scene of lambs, bunnies, baby chicks and sprouting carrots in soft pastels on a cream background — picture-perfect and quietly whimsical.</li><li><strong>Mom's notched V-neck + Girl's Peter Pan collar:</strong> Mother style wears a soft notched V-neckline; daughter style wears a sweet scalloped Peter Pan collar with buttery yellow trim — coordinated, not clone-identical.</li><li><strong>Easy care:</strong> Machine-wash cold, tumble dry low. Cotton knit keeps airflow high and wrinkles low.</li>__SIZE_RANGE_BULLET__</ul>
HTML

read -r -d '' NARRATIVE_HTML <<'HTML' || true
<p>Our Little Sheep Meadow mommy-and-me pajama set turns bedtime into a watercolor storybook. The soft cream ground is painted edge-to-edge with curly lambs napping in tall grass, bunnies peeking past sprouting carrots, and a single baby chick nestled in wildflowers — the kind of pastoral print that belongs in a sunlit nursery window. Mom's top wears a soft notched V-neckline with a short-sleeve relaxed cut, and daughter's style adds a scalloped Peter Pan collar trimmed in buttery yellow for an extra-sweet finish.</p><p>Wear it for slow Sunday mornings, grandma sleepovers, birthday pajama parties, and those holiday-card mornings when everyone needs to look picture-perfect without trying. The breezy short-sleeve top and pull-on pant moves easily from pillow fights to pancake-making. Pair the matching mother and daughter sizes to make every snapshot twin — brunch, birthdays, and the quiet moments in between.</p><h3>Key Features:</h3><ul><li><strong>Coordinated mother &amp; daughter fit:</strong> Same Little Sheep Meadow watercolor print in adult and child cuts so every family photo matches effortlessly.</li><li><strong>Breathable cotton knit:</strong> Lightweight and airy for warm-weather sleep and summer travel.</li><li><strong>Two-piece short-sleeve pajama set:</strong> Notched V-neck top for mom, scalloped Peter Pan collar top for girls, and matching pull-on pants with elastic waistband.</li><li><strong>Soft pastel palette:</strong> Cream ground with watercolor-painted lambs, bunnies, chicks, and carrots — gentle and nursery-ready.</li><li><strong>Pastel yellow contrast trim:</strong> Buttery yellow cuff and collar accents tie the mother and daughter versions together.</li></ul>
<p>Add the matching mother and daughter sizes to your cart to make every moment match — bedtime, brunch, and every snapshot in between.</p>
HTML

BASE_TAGS_JSON='["Mommy and Me","Pajamas","Matching Family Pajamas","Short Sleeve Pajamas","Two-Piece Pajama Set","Summer","Cream","Yellow","Pastel","Floral","Multicolor","Lamb","Little Sheep","Sheep","Bunny","Rabbit","Chick","Carrot","Watercolor","Farm","Pastoral","Meadow","Cottagecore","Nursery","Peter Pan Collar","V-Neck","Cotton","Child 2-3yr","Child 4-5yr","Child 6-8yr","Child 9-10yr"]'

# ============================================================================
#  DERIVED FIELDS
# ============================================================================
ROW_COUNT=$(echo "$VENDOR_SIZE_CHART" | jq 'length')
if [[ "$ROW_COUNT" -lt 1 ]]; then
  echo "ERROR: VENDOR_SIZE_CHART is empty." >&2; exit 1
fi
if ! echo "$VENDOR_SIZE_CHART" | jq -e 'all(.[]; .audience and .label and .sku_suffix and .age and .weight and .height and .chest_cm and .sleeve_cm and .pant_cm and .hip_cm and .waist_cm and .length_cm)' > /dev/null; then
  echo "ERROR: VENDOR_SIZE_CHART row is missing a required field." >&2; exit 1
fi
DUPES=$(echo "$VENDOR_SIZE_CHART" | jq -r '[.[].label] | group_by(.)[] | select(length>1) | .[0]')
if [[ -n "$DUPES" ]]; then
  echo "ERROR: duplicate size labels in VENDOR_SIZE_CHART: $DUPES" >&2; exit 1
fi
BAD_AUDIENCE=$(echo "$VENDOR_SIZE_CHART" | jq -r '.[].audience' | grep -vE '^(child|mother)$' || true)
if [[ -n "$BAD_AUDIENCE" ]]; then
  echo "ERROR: audience must be 'child' or 'mother'. Got: $BAD_AUDIENCE" >&2; exit 1
fi
echo "[preflight] $ROW_COUNT variant rows validated from vendor size chart." >&2

SIZE_VALUES_JSON=$(echo "$VENDOR_SIZE_CHART" | jq -c '[.[] | {name: .label}]')

VARIANTS_JSON=$(echo "$VENDOR_SIZE_CHART" | jq -c \
  --arg cp "$CHILD_PRICE" --arg cc "$CHILD_COMPARE" \
  --arg mp "$MOTHER_PRICE" --arg mc "$MOTHER_COMPARE" \
  --arg sc "$SHORTCODE" --arg ct "$COLOR_TOKEN" --arg cn "$COLOR_NAME" '
  [ .[] | {
      price: (if .audience=="child" then $cp else $mp end),
      compareAtPrice: (if .audience=="child" then $cc else $mc end),
      inventoryPolicy: "DENY",
      inventoryItem: { sku: ("DLM-" + $sc + "-" + .sku_suffix + "-" + $ct), tracked: true, requiresShipping: true },
      optionValues: [
        { optionName: "Size",  name: .label },
        { optionName: "Color", name: $cn    }
      ]
    }
  ]')

VARIANT_COUNT=$(echo "$VARIANTS_JSON" | jq 'length')
if [[ "$VARIANT_COUNT" -ne "$ROW_COUNT" ]]; then
  echo "ERROR: derived variant count ($VARIANT_COUNT) != chart rows ($ROW_COUNT)" >&2; exit 1
fi

# Body size table — child rows first, then adult rows, with comment markers
CHILD_ROWS=$(echo "$VENDOR_SIZE_CHART" | jq -r '
  .[] | select(.audience=="child") | "<tr><td>\(.label)</td><td>\(.age)</td><td>\(.weight)</td><td>\(.height)</td><td>\(.chest_cm) cm / \((.chest_cm/2.54*10|round)/10) in</td><td>\(.sleeve_cm) cm / \((.sleeve_cm/2.54*10|round)/10) in</td><td>\(.pant_cm) cm / \((.pant_cm/2.54*10|round)/10) in</td><td>\(.hip_cm) cm / \((.hip_cm/2.54*10|round)/10) in</td><td>\(.waist_cm) cm / \((.waist_cm/2.54*10|round)/10) in</td><td>\(.length_cm) cm / \((.length_cm/2.54*10|round)/10) in</td></tr>"
' | tr -d '\n')
ADULT_ROWS=$(echo "$VENDOR_SIZE_CHART" | jq -r '
  .[] | select(.audience=="mother") | "<tr><td>\(.label)</td><td>\(.age)</td><td>\(.weight)</td><td>\(.height)</td><td>\(.chest_cm) cm / \((.chest_cm/2.54*10|round)/10) in</td><td>\(.sleeve_cm) cm / \((.sleeve_cm/2.54*10|round)/10) in</td><td>\(.pant_cm) cm / \((.pant_cm/2.54*10|round)/10) in</td><td>\(.hip_cm) cm / \((.hip_cm/2.54*10|round)/10) in</td><td>\(.waist_cm) cm / \((.waist_cm/2.54*10|round)/10) in</td><td>\(.length_cm) cm / \((.length_cm/2.54*10|round)/10) in</td></tr>"
' | tr -d '\n')

SIZE_TABLE_HTML="<h3>Size Chart</h3><table id=\"size-chart\"><thead><tr><th>Size</th><th>Age</th><th>Recommended Weight (kg/lbs)</th><th>Recommended Height (cm/in)</th><th>Chest/Bust (cm/in)</th><th>Sleeve Length (cm/in)</th><th>Pant/Short Length (cm/in)</th><th>Hip (cm/in)</th><th>Waist (cm/in)</th><th>Garment Length (cm/in)</th></tr></thead><tbody><!-- Children Sizes -->${CHILD_ROWS}<!-- Adult Sizes -->${ADULT_ROWS}</tbody></table>"

CHILD_SHORT=$(echo "$VENDOR_SIZE_CHART" | jq -r '[.[] | select(.audience=="child") | .label] | join(", ")')
MOTHER_LABELS=$(echo "$VENDOR_SIZE_CHART" | jq -r '[.[] | select(.audience=="mother") | .label] | join(" / ")')

if [[ -n "$MOTHER_LABELS" ]]; then
  SIZE_RANGE_BULLET="<li><strong>Family size range:</strong> Girls 2Y through 9–10Y and ${MOTHER_LABELS} so the whole family can twin.</li>"
else
  SIZE_RANGE_BULLET="<li><strong>Kids size range:</strong> Girls 2Y through 9–10Y.</li>"
fi

# Build body
BODY_HTML="${BULLETS_HTML/__SIZE_RANGE_BULLET__/$SIZE_RANGE_BULLET}<p>&nbsp;</p>${SIZE_TABLE_HTML}${NARRATIVE_HTML}"

# SEO desc — "Sizes 2Y–10Y & Mom S–XL" format
SEO_DESC="Shop our Little Sheep Meadow matching mommy-and-me pajamas — soft cotton short-sleeve sets for mom + daughter. Sizes 2Y–10Y & Mom S–XL."
SEO_DESC_LEN=${#SEO_DESC}
if (( SEO_DESC_LEN > 155 )); then
  SEO_DESC="Shop our Little Sheep Meadow mommy-and-me pajamas in soft cotton for mom + daughter. Sizes 2Y–10Y & Mom S–XL."
  SEO_DESC_LEN=${#SEO_DESC}
fi
if (( SEO_DESC_LEN > 155 )); then
  SEO_DESC="Little Sheep Meadow mommy-and-me pajamas. Sizes 2Y–10Y & Mom S–XL. Shop the set."
  SEO_DESC_LEN=${#SEO_DESC}
fi
if (( SEO_DESC_LEN > 155 )); then
  echo "ERROR: SEO_DESC still too long ($SEO_DESC_LEN chars)" >&2; exit 1
fi
SEO_TITLE_LEN=${#SEO_TITLE}
if (( SEO_TITLE_LEN > 60 )); then
  echo "ERROR: SEO_TITLE too long ($SEO_TITLE_LEN chars)" >&2; exit 1
fi
TITLE_LEN=${#TITLE}
if (( TITLE_LEN > 70 )); then
  echo "ERROR: TITLE too long ($TITLE_LEN chars)" >&2; exit 1
fi
echo "[preflight] TITLE $TITLE_LEN / SEO_TITLE $SEO_TITLE_LEN / SEO_DESC $SEO_DESC_LEN chars." >&2

# Tags: base + mother size labels that exist + vendor URL
TAGS_JSON=$(jq -nc \
  --argjson base "$BASE_TAGS_JSON" \
  --argjson chart "$VENDOR_SIZE_CHART" \
  --arg vurl "$VENDOR_URL" '
  ($base + [$chart[] | select(.audience=="mother") | .label] + [$vurl]) | unique_by(.) ')

# shopify.size metafield — only labels that have a catalog entry
SIZE_METAFIELD_VALUE=$(jq -nc --argjson chart "$VENDOR_SIZE_CHART" --argjson map "$SIZE_METAOBJECT_MAP" '
  [ $chart[].label | select(. as $l | $map[$l] != null) | $map[.] ]')
UNMAPPED_SIZES=$(jq -r --argjson chart "$VENDOR_SIZE_CHART" --argjson map "$SIZE_METAOBJECT_MAP" '
  [ $chart[].label | select(. as $l | $map[$l] == null) ] | join(", ")' <<<'{}')
if [[ -n "$UNMAPPED_SIZES" ]]; then
  echo "[preflight] shopify.size: unmapped sizes skipped -> $UNMAPPED_SIZES" >&2
fi

# ============================================================================
#  STEP 1 — productCreate
# ============================================================================
SEO_JSON=$(jq -nc --arg t "$SEO_TITLE" --arg d "$SEO_DESC" '{title:$t, description:$d}')

CREATE_QUERY='mutation ProductCreate($input: ProductInput!) {
  productCreate(input: $input) {
    product { id handle title status }
    userErrors { field message }
  }
}'

CREATE_VARS=$(jq -nc \
  --arg handle "$HANDLE" \
  --arg title "$TITLE" \
  --arg vendor "$VENDOR" \
  --arg ptype "$PTYPE" \
  --arg body "$BODY_HTML" \
  --arg cat "$CATEGORY_GID" \
  --argjson tags "$TAGS_JSON" \
  --argjson seo "$SEO_JSON" \
  --argjson sizes "$SIZE_VALUES_JSON" \
  --arg color "$COLOR_NAME" '
  {
    input: {
      handle: $handle,
      title: $title,
      vendor: $vendor,
      productType: $ptype,
      descriptionHtml: $body,
      tags: $tags,
      status: "ACTIVE",
      seo: $seo,
      category: $cat,
      productOptions: [
        { name: "Size",  values: $sizes },
        { name: "Color", values: [ {name: $color} ] }
      ]
    }
  }')

echo ">>> productCreate" >&2
CREATE_RESP=$(gql "$CREATE_QUERY" "$CREATE_VARS")
echo "$CREATE_RESP" | jq . >&2
check_user_errors "$CREATE_RESP" '.data.productCreate.userErrors' "productCreate"

PRODUCT_ID=$(echo "$CREATE_RESP" | jq -r '.data.productCreate.product.id // empty')
if [[ -z "$PRODUCT_ID" ]]; then
  echo "ERROR: productCreate did not return a product id" >&2; exit 1
fi
ADMIN_NUM_ID=$(echo "$PRODUCT_ID" | sed 's|gid://shopify/Product/||')
echo "PRODUCT_ID=$PRODUCT_ID" >&2

# ============================================================================
#  STEP 2 — productVariantsBulkCreate
# ============================================================================
BULK_QUERY='mutation ProductVariantsBulkCreate($productId: ID!, $variants: [ProductVariantsBulkInput!]!, $strategy: ProductVariantsBulkCreateStrategy) {
  productVariantsBulkCreate(productId: $productId, variants: $variants, strategy: $strategy) {
    product { id variants(first: 100) { nodes { id sku title price compareAtPrice inventoryPolicy selectedOptions { name value } } } }
    userErrors { field message }
  }
}'

BULK_VARS=$(jq -nc --arg pid "$PRODUCT_ID" --argjson v "$VARIANTS_JSON" '
  { productId: $pid, variants: $v, strategy: "REMOVE_STANDALONE_VARIANT" }')

echo ">>> productVariantsBulkCreate ($VARIANT_COUNT variants)" >&2
BULK_RESP=$(gql "$BULK_QUERY" "$BULK_VARS")
echo "$BULK_RESP" | jq . >&2
check_user_errors "$BULK_RESP" '.data.productVariantsBulkCreate.userErrors' "productVariantsBulkCreate"

LIVE_VARIANT_COUNT=$(echo "$BULK_RESP" | jq '.data.productVariantsBulkCreate.product.variants.nodes | length')
if [[ "$LIVE_VARIANT_COUNT" -ne "$VARIANT_COUNT" ]]; then
  echo "ERROR: live variant count ($LIVE_VARIANT_COUNT) != chart rows ($VARIANT_COUNT)" >&2; exit 1
fi

# ============================================================================
#  STEP 3 — metafieldsSet
# ============================================================================
MF_QUERY='mutation MetafieldsSet($metafields: [MetafieldsSetInput!]!) {
  metafieldsSet(metafields: $metafields) {
    metafields { id namespace key type value }
    userErrors { field message }
  }
}'

MF_VARS=$(jq -nc \
  --arg pid "$PRODUCT_ID" \
  --arg seo_title "$SEO_TITLE" \
  --arg seo_desc "$SEO_DESC" \
  --argjson size_refs "$SIZE_METAFIELD_VALUE" '
  {
    metafields: [
      {ownerId:$pid, namespace:"custom", key:"category1",   type:"single_line_text_field", value:"Mommy and Me"},
      {ownerId:$pid, namespace:"custom", key:"subcategory", type:"single_line_text_field", value:"Pajamas"},
      {ownerId:$pid, namespace:"custom", key:"subcategory2",type:"single_line_text_field", value:"Summer Pajamas"},
      {ownerId:$pid, namespace:"custom", key:"pattern",     type:"single_line_text_field", value:"Little Sheep Meadow Print"},
      {ownerId:$pid, namespace:"custom", key:"style",       type:"single_line_text_field", value:"Matching Family Set"},
      {ownerId:$pid, namespace:"custom", key:"type",        type:"single_line_text_field", value:"Two-Piece Pajama Set"},
      {ownerId:$pid, namespace:"mm-google-shopping", key:"custom_product",  type:"boolean",                value:"false"},
      {ownerId:$pid, namespace:"mm-google-shopping", key:"gender",          type:"single_line_text_field", value:"female"},
      {ownerId:$pid, namespace:"mm-google-shopping", key:"age_group",       type:"single_line_text_field", value:"adult"},
      {ownerId:$pid, namespace:"mm-google-shopping", key:"condition",       type:"single_line_text_field", value:"new"},
      {ownerId:$pid, namespace:"mm-google-shopping", key:"custom_label_0",  type:"single_line_text_field", value:"Mommy and Me"},
      {ownerId:$pid, namespace:"mm-google-shopping", key:"custom_label_1",  type:"single_line_text_field", value:"Lamb Sheep Meadow"},
      {ownerId:$pid, namespace:"mm-google-shopping", key:"custom_label_2",  type:"single_line_text_field", value:"Summer"},
      {ownerId:$pid, namespace:"mm-google-shopping", key:"custom_label_3",  type:"single_line_text_field", value:"Short Sleeve Set"},
      {ownerId:$pid, namespace:"mm-google-shopping", key:"custom_label_4",  type:"single_line_text_field", value:"Family Matching"},
      {ownerId:$pid, namespace:"shopify", key:"age-group",     type:"list.metaobject_reference", value:"[\"gid://shopify/Metaobject/128116523105\",\"gid://shopify/Metaobject/128116490337\"]"},
      {ownerId:$pid, namespace:"shopify", key:"color-pattern", type:"list.metaobject_reference", value:"[\"gid://shopify/Metaobject/69641928801\",\"gid://shopify/Metaobject/129971519585\",\"gid://shopify/Metaobject/130231140449\"]"},
      {ownerId:$pid, namespace:"shopify", key:"fabric",        type:"list.metaobject_reference", value:"[\"gid://shopify/Metaobject/69622399073\"]"},
      {ownerId:$pid, namespace:"shopify", key:"size",          type:"list.metaobject_reference", value:($size_refs | tostring)},
      {ownerId:$pid, namespace:"shopify", key:"target-gender", type:"list.metaobject_reference", value:"[\"gid://shopify/Metaobject/129971617889\"]"},
      {ownerId:$pid, namespace:"global",  key:"title_tag",         type:"single_line_text_field", value:$seo_title},
      {ownerId:$pid, namespace:"global",  key:"description_tag",   type:"single_line_text_field", value:$seo_desc}
    ]
  }')
# Skipped (with reason):
#   - shopify.sleeve-length-type, shopify.neckline: store enforces subtype —
#     category is Matching Family Pajamas, which rejects these. (The spec
#     says to omit sleeve-length-type for Pajamas anyway.)
#   - shopify.dress-occasion, dress-style, skirt-dress-length-type: Dresses only.
#   - shopify.clothing-features: no catalog entry fits summer cotton pajamas
#     (only "Insulated" exists, which is wrong for this product).

echo ">>> metafieldsSet" >&2
MF_RESP=$(gql "$MF_QUERY" "$MF_VARS")
echo "$MF_RESP" | jq . >&2
check_user_errors "$MF_RESP" '.data.metafieldsSet.userErrors' "metafieldsSet"

# ============================================================================
#  STEP 4 — publishablePublish (all sales channels)
# ============================================================================
PUB_QUERY='mutation PublishablePublish($id: ID!, $input: [PublicationInput!]!) {
  publishablePublish(id: $id, input: $input) {
    userErrors { field message }
    publishable { availablePublicationsCount { count } }
  }
}'

PUB_VARS=$(jq -nc --arg pid "$PRODUCT_ID" '
  {
    id: $pid,
    input: [
      {publicationId: "gid://shopify/Publication/55169925"},
      {publicationId: "gid://shopify/Publication/21969633377"},
      {publicationId: "gid://shopify/Publication/29172400225"},
      {publicationId: "gid://shopify/Publication/76582879329"},
      {publicationId: "gid://shopify/Publication/76604768353"}
    ]
  }')

echo ">>> publishablePublish" >&2
PUB_RESP=$(gql "$PUB_QUERY" "$PUB_VARS")
echo "$PUB_RESP" | jq . >&2
check_user_errors "$PUB_RESP" '.data.publishablePublish.userErrors' "publishablePublish"

# ============================================================================
#  STEP 5 — media attach (if local images exist)
# ============================================================================
MEDIA_DIR="/Users/fsuels/Projects/dresslikemommy/uploads/little-sheep-meadow-mommy-and-me-pajamas"
if [[ -d "$MEDIA_DIR" ]] && compgen -G "$MEDIA_DIR/*.jpg" > /dev/null; then
  echo ">>> attaching media from $MEDIA_DIR" >&2
  for IMG in "$MEDIA_DIR"/*.jpg; do
    FNAME=$(basename "$IMG")
    STAGE_RESP=$(gql 'mutation($input:[StagedUploadInput!]!){stagedUploadsCreate(input:$input){stagedTargets{url resourceUrl parameters{name value}} userErrors{field message}}}' \
      "$(jq -nc --arg f "$FNAME" '{input:[{filename:$f, mimeType:"image/jpeg", resource:"IMAGE", httpMethod:"POST"}]}')")
    URL=$(echo "$STAGE_RESP" | jq -r '.data.stagedUploadsCreate.stagedTargets[0].url')
    RESOURCE_URL=$(echo "$STAGE_RESP" | jq -r '.data.stagedUploadsCreate.stagedTargets[0].resourceUrl')
    FORM_ARGS=()
    while IFS= read -r line; do
      FORM_ARGS+=(-F "$line")
    done < <(echo "$STAGE_RESP" | jq -r '.data.stagedUploadsCreate.stagedTargets[0].parameters[] | "\(.name)=\(.value)"')
    FORM_ARGS+=(-F "file=@$IMG")
    curl -sS -X POST "$URL" "${FORM_ARGS[@]}" > /dev/null
    gql 'mutation($productId:ID!,$media:[CreateMediaInput!]!){productCreateMedia(productId:$productId,media:$media){media{...on MediaImage{id alt}} userErrors{field message}}}' \
      "$(jq -nc --arg pid "$PRODUCT_ID" --arg url "$RESOURCE_URL" --arg alt "Mom and daughter in matching Little Sheep Meadow cream watercolor pajamas with lambs, bunnies, and carrots print, seated together on a cream sofa in a bright living room." \
        '{productId:$pid, media:[{originalSource:$url, mediaContentType:"IMAGE", alt:$alt}]}')" | jq . >&2
  done
else
  echo "NOTE: no local media at $MEDIA_DIR — skipping media attach. Drop hero image there and rerun this block." >&2
fi

# ============================================================================
#  STEP 6 — verify (live vs derived)
# ============================================================================
VERIFY_RESP=$(gql 'query($id:ID!){ product(id:$id){ id title status onlineStoreUrl publishedAt variants(first:100){ edges{ node{ sku title price compareAtPrice inventoryPolicy inventoryItem{ tracked } } } } availablePublicationsCount{ count } seo{ title description } } }' \
  "$(jq -nc --arg id "$PRODUCT_ID" '{id:$id}')")

LIVE_SKUS=$(echo "$VERIFY_RESP" | jq -r '.data.product.variants.edges[].node.sku' | sort)
DERIVED_SKUS=$(echo "$VARIANTS_JSON" | jq -r '.[].inventoryItem.sku' | sort)
if [[ "$LIVE_SKUS" != "$DERIVED_SKUS" ]]; then
  echo "ERROR: live SKUs diverge from derived SKUs." >&2
  diff <(echo "$LIVE_SKUS") <(echo "$DERIVED_SKUS") >&2 || true
  exit 1
fi
LIVE_COUNT=$(echo "$VERIFY_RESP" | jq '.data.product.variants.edges | length')
if [[ "$LIVE_COUNT" -ne "$ROW_COUNT" ]]; then
  echo "ERROR: post-create variant count ($LIVE_COUNT) != chart rows ($ROW_COUNT)" >&2; exit 1
fi
echo "[verify] SKUs match vendor chart ($VARIANT_COUNT rows)." >&2

# ============================================================================
#  Final summary
# ============================================================================
echo
echo "=== SUMMARY ==="
echo "Product ID:  $PRODUCT_ID"
echo "Handle:      $HANDLE"
echo "Admin URL:   https://admin.shopify.com/store/dresslikemommy/products/$ADMIN_NUM_ID"
echo "Storefront:  https://www.dresslikemommy.com/products/$HANDLE"
echo "SEO:         title=$SEO_TITLE_LEN chars / desc=$SEO_DESC_LEN chars"
echo "Vendor rows: $ROW_COUNT  |  Live variants: $LIVE_VARIANT_COUNT"
echo "Variants:"
echo "$BULK_RESP" | jq -r '.data.productVariantsBulkCreate.product.variants.nodes[] | "  - \(.sku)  \(.title)  $\(.price)  (compare $\(.compareAtPrice))  policy=\(.inventoryPolicy)"'
