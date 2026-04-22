#!/usr/bin/env bash
# ============================================================================
#  VCF — Polar Adventure Mommy-and-Me Pajama Listing (Shopify Admin 2025-01)
#
#  Vendor source: https://detail.1688.com/offer/828526529351.html
#  (1688 captcha-blocks direct fetch — size chart extracted from the user's
#  attached 尺码参数 screenshot which is the authoritative fallback per the
#  runbook contract. See listing.md for the vendor→picker mapping.)
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
HANDLE="polar-adventure-mommy-and-me-pajamas"
TITLE="Polar Adventure Mommy and Me Pajamas — Long-Sleeve Set"
VENDOR="dresslikemommy.com"
PTYPE="Matching Family Pajamas"
SEO_TITLE="Polar Mommy & Me Pajamas — Matching Set | Dress Like Mommy"
CATEGORY_GID="gid://shopify/TaxonomyCategory/aa-1-17-4"
VENDOR_URL="https://detail.1688.com/offer/828526529351.html"

SHORTCODE="VCF"
COLOR_TOKEN="CREAM"
COLOR_NAME="Polar Adventure Cream"

CHILD_PRICE="35.99"
CHILD_COMPARE="41.99"
MOTHER_PRICE="39.99"
MOTHER_COMPARE="45.99"

# ============================================================================
#  VENDOR_SIZE_CHART — single source of truth (from 尺码参数 table)
#
#  Vendor columns (extracted from attached screenshot):
#    尺码 | 1/2胸围 | 1/2腰围 | 衣长 | 肩宽 | 袖长 | 裤长 | 1/2臀围
#
#  Conversions:
#    - chest_cm  = 1/2胸围 × 2   (full circumference)
#    - waist_cm  = 1/2腰围 × 2   (full circumference)
#    - hip_cm    = 1/2臀围 × 2   (full circumference)
#    - sleeve_cm, pant_cm, length_cm = vendor verbatim
#
#  Size-scheme decisions:
#    - Kid rows 90/100/110/120/130/140/150 → Child 2/3/4/5/6-7/8/9-10 Years.
#    - Vendor adult table has XS,S,M,L,XL,XXL. The store size scheme
#      (child+mother) only defines Mother S/M/L/XL — so XS and XXL are
#      dropped with explicit skip reason in listing.md.
#
#  Height/weight inferred from standard CN kid pajama bands + vendor
#  男士试穿建议 (adult try-on advice) for the mom fit bands.
# ============================================================================
VENDOR_SIZE_CHART=$(cat <<'JSON'
[
  {"audience":"child","label":"Child 2 Years",    "sku_suffix":"KID2Y", "age":"2",   "weight":"12–14 kg / 26–31 lbs","height":"85–95 cm / 33–37 in",  "chest_cm":68, "sleeve_cm":33,"pant_cm":53,"hip_cm":69, "waist_cm":43,"length_cm":41},
  {"audience":"child","label":"Child 3 Years",    "sku_suffix":"KID3Y", "age":"3",   "weight":"14–16 kg / 31–35 lbs","height":"95–105 cm / 37–41 in", "chest_cm":72, "sleeve_cm":36,"pant_cm":58,"hip_cm":73, "waist_cm":45,"length_cm":44},
  {"audience":"child","label":"Child 4 Years",    "sku_suffix":"KID4Y", "age":"4",   "weight":"16–19 kg / 35–42 lbs","height":"105–115 cm / 41–45 in","chest_cm":76, "sleeve_cm":39,"pant_cm":63,"hip_cm":77, "waist_cm":47,"length_cm":47},
  {"audience":"child","label":"Child 5 Years",    "sku_suffix":"KID5Y", "age":"5",   "weight":"19–22 kg / 42–49 lbs","height":"115–125 cm / 45–49 in","chest_cm":80, "sleeve_cm":42,"pant_cm":68,"hip_cm":81, "waist_cm":49,"length_cm":50},
  {"audience":"child","label":"Child 6-7 Years", "sku_suffix":"KID67Y","age":"6–7", "weight":"22–26 kg / 49–57 lbs","height":"125–135 cm / 49–53 in","chest_cm":84, "sleeve_cm":45,"pant_cm":73,"hip_cm":85, "waist_cm":52,"length_cm":53},
  {"audience":"child","label":"Child 8 Years",    "sku_suffix":"KID8Y", "age":"8",   "weight":"26–30 kg / 57–66 lbs","height":"135–145 cm / 53–57 in","chest_cm":88, "sleeve_cm":48,"pant_cm":78,"hip_cm":89, "waist_cm":55,"length_cm":56},
  {"audience":"child","label":"Child 9-10 Years","sku_suffix":"KID910Y","age":"9–10","weight":"30–35 kg / 66–77 lbs","height":"145–155 cm / 57–61 in","chest_cm":92, "sleeve_cm":51,"pant_cm":83,"hip_cm":93, "waist_cm":57,"length_cm":59},
  {"audience":"mother","label":"Mother S", "sku_suffix":"MOMS", "age":"—","weight":"48–55 kg / 106–121 lbs","height":"155–163 cm / 61–64 in","chest_cm":106,"sleeve_cm":57,"pant_cm":97, "hip_cm":111,"waist_cm":73,"length_cm":66},
  {"audience":"mother","label":"Mother M", "sku_suffix":"MOMM", "age":"—","weight":"55–62 kg / 121–137 lbs","height":"160–168 cm / 63–66 in","chest_cm":110,"sleeve_cm":59,"pant_cm":99, "hip_cm":115,"waist_cm":75,"length_cm":69},
  {"audience":"mother","label":"Mother L", "sku_suffix":"MOML", "age":"—","weight":"62–70 kg / 137–154 lbs","height":"165–172 cm / 65–68 in","chest_cm":114,"sleeve_cm":59,"pant_cm":102,"hip_cm":119,"waist_cm":77,"length_cm":71},
  {"audience":"mother","label":"Mother XL","sku_suffix":"MOMXL","age":"—","weight":"70–78 kg / 154–172 lbs","height":"168–175 cm / 66–69 in","chest_cm":116,"sleeve_cm":60,"pant_cm":103,"hip_cm":123,"waist_cm":80,"length_cm":73}
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
<ul><li><strong>Four-layer breathable cotton gauze:</strong> Soft bamboo-cotton gauze knit with airy four-layer construction — snuggly enough for cool winter nights, breathable enough for year-round wear.</li><li><strong>Make every moment match:</strong> Coordinating mother-and-daughter long-sleeve pajama sets designed for bedtime stories, snow-day mornings, holiday cards, and brunch-worthy family photos.</li><li><strong>Polar Adventure storybook print:</strong> A wintry watercolor scene of polar bears, emperor penguins, harp seals, and arctic hares across a soft cream ground — picture-perfect and quietly whimsical.</li><li><strong>Classic notched collar + patch pockets:</strong> Mother style and daughter style both feature a soft notched collar and buttoned front — with sweet patch pockets on the kids' top for stashing bedtime treasures.</li><li><strong>Easy care:</strong> Machine-wash cold, tumble dry low. Cotton gauze keeps airflow high and wrinkles soft.</li>__SIZE_RANGE_BULLET__</ul>
HTML

read -r -d '' NARRATIVE_HTML <<'HTML' || true
<p>Our Polar Adventure mommy-and-me pajama set turns bedtime into a wintry storybook. The soft cream ground is painted edge-to-edge with watercolor polar bears cradling their cubs, emperor penguins waddling in a row, harp seal pups on snow banks, and scripted story lines that whisper "the silent night, the beauty of…" Mom's top wears a relaxed notched collar with a buttoned placket and long-sleeve fit, and daughter's style adds patch pockets at the hip — perfect for hiding a tiny stuffed penguin.</p><p>Wear it for slow holiday mornings, grandparent sleepovers, first-snow breakfasts, and those Christmas-card mornings when everyone needs to look picture-perfect without trying. The cotton-gauze top and pull-on pant moves easily from pillow fights to pancake-making. Pair the matching mother and daughter sizes to make every moment match — brunch, birthdays, and every snapshot in between.</p><h3>Key Features:</h3><ul><li><strong>Coordinated mother &amp; daughter fit:</strong> Same Polar Adventure watercolor print in adult and child cuts so every family photo matches effortlessly.</li><li><strong>Four-layer cotton gauze knit:</strong> Breathable yet snuggly — airy for three seasons and warm enough for chilly bedtimes.</li><li><strong>Two-piece long-sleeve pajama set:</strong> Notched collar button-front top and matching pull-on pants with elastic waistband.</li><li><strong>Soft cream palette with arctic watercolor motifs:</strong> Polar bears, penguins, seals, and hares in gentle earth tones.</li><li><strong>Kids' patch pockets:</strong> Sweet front patch pockets on the child's top add a storybook detail.</li></ul>
<p>Add the matching mother and daughter sizes to your cart to make every moment match — bedtime, brunch, and every snapshot in between.</p>
HTML

BASE_TAGS_JSON='["Mommy and Me","Pajamas","Matching Family Pajamas","Long Sleeve Pajamas","Two-Piece Pajama Set","Winter","Fall","Summer","Cream","Beige","White","Multicolor","Polar Bear","Penguin","Seal","Arctic","Polar Adventure","Polar","Watercolor","Animal","Storybook","Nursery","Notched Collar","Button Front","Cotton","Gauze","Four Layer","Child 2-3yr","Child 4-5yr","Child 6-8yr","Child 9-10yr"]'

# ============================================================================
#  DERIVED FIELDS
# ============================================================================
ROW_COUNT=$(echo "$VENDOR_SIZE_CHART" | jq 'length')
if [[ "$ROW_COUNT" -lt 1 ]]; then
  echo "ERROR: VENDOR_SIZE_CHART is empty." >&2; exit 1
fi

# Preflight: every row has ALL required fields populated (including waist)
if ! echo "$VENDOR_SIZE_CHART" | jq -e 'all(.[]; .audience and .vendor_label // .label and .label and .sku_suffix and .age and .weight and .height and .chest_cm and .hip_cm and .waist_cm and .length_cm)' > /dev/null; then
  echo "ERROR: VENDOR_SIZE_CHART row is missing a required field (chest/hip/waist/length)." >&2; exit 1
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

SIZE_TABLE_HTML="<h3>Size Chart</h3><table id=\"size-chart\"><thead><tr><th>Size</th><th>Age</th><th>Recommended Weight (kg/lbs)</th><th>Recommended Height (cm/in)</th><th>Chest/Bust (cm/in)</th><th>Sleeve Length (cm/in)</th><th>Pant Length (cm/in)</th><th>Hip (cm/in)</th><th>Waist (cm/in)</th><th>Garment Length (cm/in)</th></tr></thead><tbody><!-- Children Sizes -->${CHILD_ROWS}<!-- Adult Sizes -->${ADULT_ROWS}</tbody></table>"

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
SEO_DESC="Shop our Polar Adventure matching mommy-and-me pajamas — soft cotton long-sleeve sets for mom + daughter. Sizes 2Y–10Y & Mom S–XL."
SEO_DESC_LEN=$(python3 -c "import sys; print(len(sys.argv[1]))" "$SEO_DESC")
if (( SEO_DESC_LEN > 155 )); then
  SEO_DESC="Shop our Polar Adventure mommy-and-me pajamas in soft cotton for mom + daughter. Sizes 2Y–10Y & Mom S–XL."
  SEO_DESC_LEN=$(python3 -c "import sys; print(len(sys.argv[1]))" "$SEO_DESC")
fi
if (( SEO_DESC_LEN > 155 )); then
  SEO_DESC="Polar Adventure mommy-and-me pajamas. Sizes 2Y–10Y & Mom S–XL. Shop the set."
  SEO_DESC_LEN=$(python3 -c "import sys; print(len(sys.argv[1]))" "$SEO_DESC")
fi
if (( SEO_DESC_LEN > 155 )); then
  echo "ERROR: SEO_DESC still too long ($SEO_DESC_LEN chars)" >&2; exit 1
fi

SEO_TITLE_LEN=$(python3 -c "import sys; print(len(sys.argv[1]))" "$SEO_TITLE")
if (( SEO_TITLE_LEN > 60 )); then
  echo "ERROR: SEO_TITLE too long ($SEO_TITLE_LEN chars)" >&2; exit 1
fi
TITLE_LEN=$(python3 -c "import sys; print(len(sys.argv[1]))" "$TITLE")
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
UNMAPPED_SIZES=$(jq -nr --argjson chart "$VENDOR_SIZE_CHART" --argjson map "$SIZE_METAOBJECT_MAP" '
  [ $chart[].label | select(. as $l | $map[$l] == null) ] | join(", ")')
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
      {ownerId:$pid, namespace:"custom", key:"pattern",     type:"single_line_text_field", value:"Polar Adventure Watercolor Print"},
      {ownerId:$pid, namespace:"custom", key:"style",       type:"single_line_text_field", value:"Matching Family Set"},
      {ownerId:$pid, namespace:"custom", key:"type",        type:"single_line_text_field", value:"Two-Piece Pajama Set"},
      {ownerId:$pid, namespace:"mm-google-shopping", key:"custom_product",  type:"boolean",                value:"false"},
      {ownerId:$pid, namespace:"mm-google-shopping", key:"gender",          type:"single_line_text_field", value:"female"},
      {ownerId:$pid, namespace:"mm-google-shopping", key:"age_group",       type:"single_line_text_field", value:"adult"},
      {ownerId:$pid, namespace:"mm-google-shopping", key:"condition",       type:"single_line_text_field", value:"new"},
      {ownerId:$pid, namespace:"mm-google-shopping", key:"custom_label_0",  type:"single_line_text_field", value:"Mommy and Me"},
      {ownerId:$pid, namespace:"mm-google-shopping", key:"custom_label_1",  type:"single_line_text_field", value:"Polar Adventure"},
      {ownerId:$pid, namespace:"mm-google-shopping", key:"custom_label_2",  type:"single_line_text_field", value:"Summer"},
      {ownerId:$pid, namespace:"mm-google-shopping", key:"custom_label_3",  type:"single_line_text_field", value:"Long-Sleeve Set"},
      {ownerId:$pid, namespace:"mm-google-shopping", key:"custom_label_4",  type:"single_line_text_field", value:"Family Matching"},
      {ownerId:$pid, namespace:"shopify", key:"age-group",     type:"list.metaobject_reference", value:"[\"gid://shopify/Metaobject/128116523105\",\"gid://shopify/Metaobject/128116490337\"]"},
      {ownerId:$pid, namespace:"shopify", key:"color-pattern", type:"list.metaobject_reference", value:"[\"gid://shopify/Metaobject/69641928801\",\"gid://shopify/Metaobject/69639733345\",\"gid://shopify/Metaobject/130231140449\"]"},
      {ownerId:$pid, namespace:"shopify", key:"fabric",        type:"list.metaobject_reference", value:"[\"gid://shopify/Metaobject/69622399073\"]"},
      {ownerId:$pid, namespace:"shopify", key:"size",          type:"list.metaobject_reference", value:($size_refs | tostring)},
      {ownerId:$pid, namespace:"shopify", key:"target-gender", type:"list.metaobject_reference", value:"[\"gid://shopify/Metaobject/129971617889\"]"},
      {ownerId:$pid, namespace:"global",  key:"title_tag",         type:"single_line_text_field", value:$seo_title},
      {ownerId:$pid, namespace:"global",  key:"description_tag",   type:"single_line_text_field", value:$seo_desc}
    ]
  }')
# Skipped (with reason):
#   - shopify.sleeve-length-type: spec says omit for Pajamas category.
#   - shopify.neckline, shopify.dress-occasion, shopify.dress-style,
#     shopify.skirt-dress-length-type: Dresses/Tops only; Pajamas rejected.
#   - shopify.clothing-features: catalog only has "Insulated" which doesn't
#     honestly fit a cotton-gauze pajama set; omitted per skip rule.

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
MEDIA_DIR="/Users/fsuels/Projects/dresslikemommy/uploads/polar-adventure-mommy-and-me-pajamas"
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
      "$(jq -nc --arg pid "$PRODUCT_ID" --arg url "$RESOURCE_URL" --arg alt "Mom and daughter in matching Polar Adventure cream cotton pajamas with watercolor polar bears, penguins, and seals, seated on cream stairs in warm light." \
        '{productId:$pid, media:[{originalSource:$url, mediaContentType:"IMAGE", alt:$alt}]}')" | jq . >&2
  done
else
  echo "NOTE: no local media at $MEDIA_DIR — skipping media attach. Drop hero images there and rerun this block." >&2
fi

# ============================================================================
#  STEP 6 — verify (live vs derived)
# ============================================================================
VERIFY_RESP=$(gql 'query($id:ID!){ product(id:$id){ id title status onlineStoreUrl publishedAt descriptionHtml variants(first:100){ edges{ node{ sku title price compareAtPrice inventoryPolicy inventoryItem{ tracked } } } } availablePublicationsCount{ count } seo{ title description } } }' \
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

# Body size-table structural check: row count + column count
LIVE_BODY=$(echo "$VERIFY_RESP" | jq -r '.data.product.descriptionHtml')
TR_COUNT=$(echo "$LIVE_BODY" | grep -oE '<tr>' | wc -l | tr -d ' ')
# TR count = 1 thead row + ROW_COUNT tbody rows
EXPECTED_TR=$((ROW_COUNT + 1))
if [[ "$TR_COUNT" -ne "$EXPECTED_TR" ]]; then
  echo "ERROR: body size-table <tr> count $TR_COUNT != expected $EXPECTED_TR (1 header + $ROW_COUNT data)." >&2
  exit 1
fi
TH_COUNT=$(echo "$LIVE_BODY" | grep -oE '<th>' | wc -l | tr -d ' ')
if [[ "$TH_COUNT" -ne 10 ]]; then
  echo "ERROR: body size-table <th> count $TH_COUNT != expected 10 columns." >&2
  exit 1
fi
echo "[verify] SKUs match vendor chart ($VARIANT_COUNT rows); body size-table has 10 columns and $ROW_COUNT data rows." >&2

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
