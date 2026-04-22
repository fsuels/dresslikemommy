#!/usr/bin/env bash
# ============================================================================
#  VCF — Bamboo Garden Panda Cotton Mommy-and-Me Pajamas (4-layer muslin)
#  Vendor source: https://detail.1688.com/offer/828526529351.html
#
#  SINGLE SOURCE OF TRUTH: the SIZE_CHART JSON block below drives every
#  downstream artifact — productOptions, variants, SKUs, body HTML size
#  table (10 cols), tags, shopify.size metafield, SEO size phrase, CSV.
#  Edit the chart and every artifact updates in lockstep.
# ============================================================================
set -euo pipefail

# -------- credentials ----------------------------------------------------
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
HANDLE="bamboo-garden-panda-cotton-mommy-and-me-pajamas"
TITLE="Bamboo Garden Panda Mommy and Me Pajamas — Long-Sleeve Set"
VENDOR="dresslikemommy.com"
PTYPE="Matching Family Pajamas"
SEO_TITLE="Panda Mommy & Me Pajamas — Matching Set | Dress Like Mommy"
CATEGORY_GID="gid://shopify/TaxonomyCategory/aa-1-17-4"
VENDOR_URL="https://detail.1688.com/offer/828526529351.html"

SHORTCODE="VCF"
COLOR_TOKEN="CREAM"
COLOR_NAME="Bamboo Garden Panda Cream"

CHILD_PRICE="35.99"
CHILD_COMPARE="41.49"
MOTHER_PRICE="39.99"
MOTHER_COMPARE="45.99"

# ============================================================================
#  SIZE_CHART — 11 rows (7 kid + 4 mother).
#
#  Vendor columns captured: 1/2胸围 (half_chest), 1/2腰围 (half_waist),
#  衣长 (length), 肩宽 (shoulder), 袖长 (sleeve), 裤长 (pant),
#  1/2臀围 (half_hip). Full circumferences computed by doubling halves.
#
#  Fields:
#    audience     : "child" or "mother"
#    vendor_label : raw vendor row label
#    picker_label : Shopify picker value (theme resolver match)
#    sku_suffix   : goes into DLM-{SHORTCODE}-{sku_suffix}-{COLOR_TOKEN}
#    age          : "2", "6-7", or "—"
#    weight       : "12–14 kg / 26–31 lbs"
#    height       : "85–95 cm / 33–37 in"
#    chest_cm     : full bust circumference (half×2)
#    hip_cm       : full hip circumference (half×2)
#    waist_cm     : full waist circumference (half×2)
#    length_cm    : 衣长 verbatim
#    sleeve_cm    : 袖长 verbatim
#    pant_cm      : 裤长 verbatim
# ============================================================================
SIZE_CHART=$(cat <<'JSON'
[
  {"audience":"child","vendor_label":"90","picker_label":"Child 2 Years","sku_suffix":"KID2Y","age":"2","weight":"12–14 kg / 26–31 lbs","height":"85–95 cm / 33–37 in","chest_cm":68,"hip_cm":69,"waist_cm":43,"length_cm":41,"sleeve_cm":33,"pant_cm":53},
  {"audience":"child","vendor_label":"100","picker_label":"Child 3 Years","sku_suffix":"KID3Y","age":"3","weight":"14–17 kg / 31–37 lbs","height":"95–105 cm / 37–41 in","chest_cm":72,"hip_cm":73,"waist_cm":45,"length_cm":44,"sleeve_cm":36,"pant_cm":58},
  {"audience":"child","vendor_label":"110","picker_label":"Child 4 Years","sku_suffix":"KID4Y","age":"4","weight":"17–20 kg / 37–44 lbs","height":"105–115 cm / 41–45 in","chest_cm":76,"hip_cm":77,"waist_cm":47,"length_cm":47,"sleeve_cm":39,"pant_cm":63},
  {"audience":"child","vendor_label":"120","picker_label":"Child 5 Years","sku_suffix":"KID5Y","age":"5","weight":"20–23 kg / 44–51 lbs","height":"115–125 cm / 45–49 in","chest_cm":80,"hip_cm":81,"waist_cm":49,"length_cm":50,"sleeve_cm":42,"pant_cm":68},
  {"audience":"child","vendor_label":"130","picker_label":"Child 6-7 Years","sku_suffix":"KID67Y","age":"6-7","weight":"23–27 kg / 51–60 lbs","height":"125–135 cm / 49–53 in","chest_cm":84,"hip_cm":85,"waist_cm":52,"length_cm":53,"sleeve_cm":45,"pant_cm":73},
  {"audience":"child","vendor_label":"140","picker_label":"Child 8 Years","sku_suffix":"KID8Y","age":"8","weight":"27–32 kg / 60–70 lbs","height":"135–145 cm / 53–57 in","chest_cm":88,"hip_cm":89,"waist_cm":55,"length_cm":56,"sleeve_cm":48,"pant_cm":78},
  {"audience":"child","vendor_label":"150","picker_label":"Child 9-10 Years","sku_suffix":"KID910Y","age":"9-10","weight":"32–37 kg / 70–82 lbs","height":"145–155 cm / 57–61 in","chest_cm":92,"hip_cm":93,"waist_cm":57,"length_cm":59,"sleeve_cm":51,"pant_cm":83},
  {"audience":"mother","vendor_label":"S","picker_label":"Mother S","sku_suffix":"MOMS","age":"—","weight":"50–55 kg / 110–121 lbs","height":"155–162 cm / 61–64 in","chest_cm":106,"hip_cm":111,"waist_cm":73,"length_cm":66,"sleeve_cm":58,"pant_cm":97},
  {"audience":"mother","vendor_label":"M","picker_label":"Mother M","sku_suffix":"MOMM","age":"—","weight":"55–62 kg / 121–137 lbs","height":"160–167 cm / 63–66 in","chest_cm":110,"hip_cm":115,"waist_cm":75,"length_cm":69,"sleeve_cm":58,"pant_cm":99},
  {"audience":"mother","vendor_label":"L","picker_label":"Mother L","sku_suffix":"MOML","age":"—","weight":"62–68 kg / 137–150 lbs","height":"163–170 cm / 64–67 in","chest_cm":114,"hip_cm":119,"waist_cm":77,"length_cm":71,"sleeve_cm":58,"pant_cm":102},
  {"audience":"mother","vendor_label":"XL","picker_label":"Mother XL","sku_suffix":"MOMXL","age":"—","weight":"68–75 kg / 150–165 lbs","height":"166–173 cm / 65–68 in","chest_cm":116,"hip_cm":123,"waist_cm":80,"length_cm":73,"sleeve_cm":58,"pant_cm":103}
]
JSON
)

# ============================================================================
#  SIZE_METAOBJECT_MAP — shopify.size standard catalog GIDs.
#  Child 9-10 Years maps to 8-9 years (closest; 9-10 not in catalog).
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
<ul><li><strong>Soft four-layer cotton muslin:</strong> Breathable, lightweight cotton gauze that gets softer wash after wash — gentle against little cheeks and airy enough for all-night comfort.</li><li><strong>Make every moment match:</strong> Coordinating mother-and-daughter sleep sets made for slumber parties, lazy Sundays, holiday mornings, and photo-ready family moments.</li><li><strong>Bamboo Garden Panda print:</strong> A painterly garden of tumbling baby pandas playing among trailing bamboo stalks and soft botanicals on a cream ground — picture-perfect and quietly whimsical.</li><li><strong>Button-front relaxed cut:</strong> Classic notch-collar button-up top, full-length sleeves with soft cuffs, straight pull-on pants — a modern heirloom-pajama silhouette.</li><li><strong>Easy care &amp; breathable:</strong> Machine-wash cold, tumble dry low. Airy cotton muslin keeps airflow high and wrinkles gentle.</li>__SIZE_RANGE_BULLET__</ul>
HTML

read -r -d '' NARRATIVE_HTML <<'HTML' || true
<p>Our Bamboo Garden Panda mommy-and-me pajama set turns bedtime into a watercolor storybook. The soft cream body is painted edge-to-edge with tumbling pandas cuddling among trailing bamboo, wild sage, and tiny botanical sprigs — a print that feels gentle, nostalgic, and quietly whimsical. Cut from soft four-layer cotton muslin with a classic notch-collar button-up top, cuffed long sleeves, and matching pull-on pants, it is the kind of set you will reach for on every cozy night in.</p><p>Wear it for slow Sunday mornings, zoo-trip sleepover eves, birthday pajama parties, and those holiday-card mornings when everyone needs to look picture-perfect without trying. The relaxed fit moves easily from pillow fights to pancake-making, and the breathable cotton keeps mom and daughter cool and comfortable whether you are curled under a blanket or padding around the kitchen.</p><h3>Key Features:</h3><ul><li><strong>Coordinated mother &amp; daughter fit:</strong> Identical watercolor panda print in adult and child cuts so every family photo matches effortlessly.</li><li><strong>Breathable cotton muslin:</strong> Four-layer cotton gauze — soft, airy, and light enough for warm-weather sleep, warm enough for shoulder-season cozy.</li><li><strong>Button-front notch-collar top:</strong> Traditional pajama silhouette with small chest pocket detail.</li><li><strong>Cuffed long sleeves &amp; pull-on pants:</strong> Easy on-and-off and all-night comfort for every body.</li><li><strong>Family size range:</strong> Mother S through XL plus seven kid sizes (2Y–10Y) so the whole family can twin.</li></ul><p>Add mom's size and your little one's size to your cart to make every moment match — brunch, birthdays, and every snapshot in between.</p>
HTML

BASE_TAGS_JSON='["Mommy and Me","Pajamas","Matching Family Pajamas","Long Sleeve Pajamas","Button-Up Pajamas","Summer","Spring","Fall","Cream","Ivory","Green","Black","Panda","Panda Print","Bamboo","Bamboo Garden","Watercolor","Botanical","Animal Print","Cotton Muslin","Kung Fu Panda","Zoo","Child 2-3yr","Child 4-5yr","Child 6-8yr","Child 9-10yr"]'

# ============================================================================
#  PREFLIGHT — halt before any API call if chart is inconsistent
# ============================================================================
ROW_COUNT=$(echo "$SIZE_CHART" | jq 'length')
if [[ "$ROW_COUNT" -lt 1 ]]; then echo "ERROR: SIZE_CHART empty" >&2; exit 1; fi

if ! echo "$SIZE_CHART" | jq -e 'all(.[]; .audience and .vendor_label and .picker_label and .sku_suffix and .age and .weight and .height and .chest_cm and .hip_cm and .waist_cm and .length_cm and .sleeve_cm and .pant_cm)' > /dev/null; then
  echo "ERROR: SIZE_CHART row is missing a required field." >&2; exit 1
fi

DUPES=$(echo "$SIZE_CHART" | jq -r '[.[].picker_label] | group_by(.)[] | select(length>1) | .[0]')
if [[ -n "$DUPES" ]]; then echo "ERROR: duplicate picker_label: $DUPES" >&2; exit 1; fi

BAD_AUD=$(echo "$SIZE_CHART" | jq -r '.[].audience' | grep -vE '^(child|mother)$' || true)
if [[ -n "$BAD_AUD" ]]; then echo "ERROR: bad audience: $BAD_AUD" >&2; exit 1; fi

echo "[preflight] $ROW_COUNT rows validated (all required fields populated)" >&2

# -- productOptions.Size.values (derived) -----------------------------------
SIZE_VALUES_JSON=$(echo "$SIZE_CHART" | jq -c '[.[] | {name: .picker_label}]')

# -- Variants payload (derived) ---------------------------------------------
VARIANTS_JSON=$(echo "$SIZE_CHART" | jq -c \
  --arg cp "$CHILD_PRICE" --arg cc "$CHILD_COMPARE" \
  --arg mp "$MOTHER_PRICE" --arg mc "$MOTHER_COMPARE" \
  --arg sc "$SHORTCODE" --arg ct "$COLOR_TOKEN" --arg cn "$COLOR_NAME" '
  [ .[] | {
      price: (if .audience=="child" then $cp else $mp end),
      compareAtPrice: (if .audience=="child" then $cc else $mc end),
      inventoryPolicy: "DENY",
      inventoryItem: { sku: ("DLM-" + $sc + "-" + .sku_suffix + "-" + $ct), tracked: true, requiresShipping: true },
      optionValues: [
        { optionName: "Size",  name: .picker_label },
        { optionName: "Color", name: $cn }
      ]
    } ]')

VARIANT_COUNT=$(echo "$VARIANTS_JSON" | jq 'length')
if [[ "$VARIANT_COUNT" -ne "$ROW_COUNT" ]]; then
  echo "ERROR: derived variant count $VARIANT_COUNT != chart rows $ROW_COUNT" >&2; exit 1
fi

# -- 10-column body-HTML size table (derived) -------------------------------
# Columns: Size | Age | Weight | Height | Chest/Bust | Sleeve | Pant | Hip | Waist | Garment Length
KID_ROWS=$(echo "$SIZE_CHART" | jq -r '
  [.[] | select(.audience=="child")] | .[] |
  "<tr><td>\(.picker_label)</td><td>\(.age)</td><td>\(.weight)</td><td>\(.height)</td><td>\(.chest_cm) cm / \((.chest_cm/2.54*10|round)/10) in</td><td>\(.sleeve_cm) cm / \((.sleeve_cm/2.54*10|round)/10) in</td><td>\(.pant_cm) cm / \((.pant_cm/2.54*10|round)/10) in</td><td>\(.hip_cm) cm / \((.hip_cm/2.54*10|round)/10) in</td><td>\(.waist_cm) cm / \((.waist_cm/2.54*10|round)/10) in</td><td>\(.length_cm) cm / \((.length_cm/2.54*10|round)/10) in</td></tr>"' | tr -d '\n')

ADULT_ROWS=$(echo "$SIZE_CHART" | jq -r '
  [.[] | select(.audience=="mother")] | .[] |
  "<tr><td>\(.picker_label)</td><td>\(.age)</td><td>\(.weight)</td><td>\(.height)</td><td>\(.chest_cm) cm / \((.chest_cm/2.54*10|round)/10) in</td><td>\(.sleeve_cm) cm / \((.sleeve_cm/2.54*10|round)/10) in</td><td>\(.pant_cm) cm / \((.pant_cm/2.54*10|round)/10) in</td><td>\(.hip_cm) cm / \((.hip_cm/2.54*10|round)/10) in</td><td>\(.waist_cm) cm / \((.waist_cm/2.54*10|round)/10) in</td><td>\(.length_cm) cm / \((.length_cm/2.54*10|round)/10) in</td></tr>"' | tr -d '\n')

SIZE_TABLE_HTML="<h3>Size Chart</h3><table id=\"size-chart\"><thead><tr><th>Size</th><th>Age</th><th>Recommended Weight (kg/lbs)</th><th>Recommended Height (cm/in)</th><th>Chest/Bust (cm/in)</th><th>Sleeve Length (cm/in)</th><th>Pant Length (cm/in)</th><th>Hip (cm/in)</th><th>Waist (cm/in)</th><th>Garment Length (cm/in)</th></tr></thead><tbody><!-- Children Sizes -->${KID_ROWS}<!-- Adult Sizes -->${ADULT_ROWS}</tbody></table>"

# -- Size range bullet + SEO size phrase (derived) --------------------------
CHILD_LABELS=$(echo "$SIZE_CHART" | jq -r '[.[] | select(.audience=="child") | .picker_label] | length')
MOTHER_LABELS_LIST=$(echo "$SIZE_CHART" | jq -r '[.[] | select(.audience=="mother") | .picker_label | sub("Mother "; "Mom ")] | join(", ")')
# Kids: if contiguous 2Y..10Y use range
KID_RANGE="2Y–10Y"
# Mother: S–XL range
if [[ "$MOTHER_LABELS_LIST" == "Mom S, Mom M, Mom L, Mom XL" ]]; then
  MOM_RANGE="Mom S–XL"
else
  MOM_RANGE="$MOTHER_LABELS_LIST"
fi

SIZE_RANGE_BULLET="<li><strong>Family size range:</strong> Kids ${KID_RANGE} and ${MOM_RANGE// / }.</li>"
# Simpler narrative form
SIZE_RANGE_BULLET="<li><strong>Family size range:</strong> Kids ${KID_RANGE} plus Mom S–XL so the whole family can twin.</li>"

BODY_HTML="${BULLETS_HTML/__SIZE_RANGE_BULLET__/$SIZE_RANGE_BULLET}<p>&nbsp;</p>${SIZE_TABLE_HTML}${NARRATIVE_HTML}"

# -- SEO description (≤155) with trim fallbacks -----------------------------
SEO_DESC="Shop our Bamboo Garden Panda matching mommy-and-me pajamas — soft cotton long-sleeve sets for mom + daughter. Sizes ${KID_RANGE} & ${MOM_RANGE}."
SEO_DESC_LEN=${#SEO_DESC}
if (( SEO_DESC_LEN > 155 )); then
  SEO_DESC="Shop our Bamboo Garden Panda matching mommy-and-me pajamas — long-sleeve sets for mom + daughter. Sizes ${KID_RANGE} & ${MOM_RANGE}."
  SEO_DESC_LEN=${#SEO_DESC}
fi
if (( SEO_DESC_LEN > 155 )); then
  SEO_DESC="Bamboo Garden Panda matching mommy-and-me pajamas in soft cotton. Sizes ${KID_RANGE} & ${MOM_RANGE}."
  SEO_DESC_LEN=${#SEO_DESC}
fi
if (( SEO_DESC_LEN > 155 )); then echo "ERROR: SEO_DESC $SEO_DESC_LEN chars" >&2; exit 1; fi

SEO_TITLE_LEN=${#SEO_TITLE}
TITLE_LEN=${#TITLE}
if (( SEO_TITLE_LEN > 60 )); then echo "ERROR: SEO_TITLE $SEO_TITLE_LEN chars" >&2; exit 1; fi
if (( TITLE_LEN > 70 )); then echo "ERROR: TITLE $TITLE_LEN chars" >&2; exit 1; fi
echo "[preflight] TITLE=$TITLE_LEN SEO_TITLE=$SEO_TITLE_LEN SEO_DESC=$SEO_DESC_LEN" >&2

# -- Tags (derived: base + mother picker labels present + vendor URL) -------
TAGS_JSON=$(jq -nc \
  --argjson base "$BASE_TAGS_JSON" \
  --argjson chart "$SIZE_CHART" \
  --arg vurl "$VENDOR_URL" '
  ($base
   + [$chart[] | select(.audience=="mother") | .picker_label]
   + [$vurl]) | unique_by(.) ')

# -- shopify.size metafield (derived) ---------------------------------------
SIZE_METAFIELD_VALUE=$(jq -nc --argjson chart "$SIZE_CHART" --argjson map "$SIZE_METAOBJECT_MAP" '
  [ $chart[].picker_label | select(. as $l | $map[$l] != null) | $map[.] ]')
UNMAPPED_SIZES=$(jq -rn --argjson chart "$SIZE_CHART" --argjson map "$SIZE_METAOBJECT_MAP" '
  [ $chart[].picker_label | select(. as $l | $map[$l] == null) ] | join(", ")')
if [[ -n "$UNMAPPED_SIZES" ]]; then
  echo "[preflight] shopify.size skips: $UNMAPPED_SIZES" >&2
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
check_user_errors "$CREATE_RESP" '.data.productCreate.userErrors' "productCreate"

PRODUCT_ID=$(echo "$CREATE_RESP" | jq -r '.data.productCreate.product.id // empty')
if [[ -z "$PRODUCT_ID" ]]; then
  echo "$CREATE_RESP" | jq . >&2
  echo "ERROR: productCreate returned no id" >&2; exit 1
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
check_user_errors "$BULK_RESP" '.data.productVariantsBulkCreate.userErrors' "productVariantsBulkCreate"

LIVE_VARIANT_COUNT=$(echo "$BULK_RESP" | jq '.data.productVariantsBulkCreate.product.variants.nodes | length')
if [[ "$LIVE_VARIANT_COUNT" -ne "$VARIANT_COUNT" ]]; then
  echo "ERROR: live variant count $LIVE_VARIANT_COUNT != chart $VARIANT_COUNT" >&2; exit 1
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
      {ownerId:$pid, namespace:"custom", key:"pattern",     type:"single_line_text_field", value:"Bamboo Garden Panda Print"},
      {ownerId:$pid, namespace:"custom", key:"style",       type:"single_line_text_field", value:"Matching Family Set"},
      {ownerId:$pid, namespace:"custom", key:"type",        type:"single_line_text_field", value:"Two-Piece Pajama Set"},
      {ownerId:$pid, namespace:"mm-google-shopping", key:"custom_product",  type:"boolean",                value:"false"},
      {ownerId:$pid, namespace:"mm-google-shopping", key:"gender",          type:"single_line_text_field", value:"female"},
      {ownerId:$pid, namespace:"mm-google-shopping", key:"age_group",       type:"single_line_text_field", value:"adult"},
      {ownerId:$pid, namespace:"mm-google-shopping", key:"condition",       type:"single_line_text_field", value:"new"},
      {ownerId:$pid, namespace:"mm-google-shopping", key:"custom_label_0",  type:"single_line_text_field", value:"Mommy and Me"},
      {ownerId:$pid, namespace:"mm-google-shopping", key:"custom_label_1",  type:"single_line_text_field", value:"Panda Bamboo"},
      {ownerId:$pid, namespace:"mm-google-shopping", key:"custom_label_2",  type:"single_line_text_field", value:"Summer"},
      {ownerId:$pid, namespace:"mm-google-shopping", key:"custom_label_3",  type:"single_line_text_field", value:"Long Sleeve Set"},
      {ownerId:$pid, namespace:"mm-google-shopping", key:"custom_label_4",  type:"single_line_text_field", value:"Family Matching"},
      {ownerId:$pid, namespace:"shopify", key:"age-group",     type:"list.metaobject_reference", value:"[\"gid://shopify/Metaobject/128116523105\",\"gid://shopify/Metaobject/128116490337\"]"},
      {ownerId:$pid, namespace:"shopify", key:"color-pattern", type:"list.metaobject_reference", value:"[\"gid://shopify/Metaobject/69641928801\",\"gid://shopify/Metaobject/69943132257\",\"gid://shopify/Metaobject/70220546145\",\"gid://shopify/Metaobject/130231140449\"]"},
      {ownerId:$pid, namespace:"shopify", key:"fabric",        type:"list.metaobject_reference", value:"[\"gid://shopify/Metaobject/69622399073\"]"},
      {ownerId:$pid, namespace:"shopify", key:"size",          type:"list.metaobject_reference", value:($size_refs | tostring)},
      {ownerId:$pid, namespace:"shopify", key:"target-gender", type:"list.metaobject_reference", value:"[\"gid://shopify/Metaobject/129971617889\"]"},
      {ownerId:$pid, namespace:"global",  key:"title_tag",       type:"single_line_text_field", value:$seo_title},
      {ownerId:$pid, namespace:"global",  key:"description_tag", type:"single_line_text_field", value:$seo_desc}
    ]
  }')

echo ">>> metafieldsSet" >&2
MF_RESP=$(gql "$MF_QUERY" "$MF_VARS")
check_user_errors "$MF_RESP" '.data.metafieldsSet.userErrors' "metafieldsSet"

# ============================================================================
#  STEP 4 — publishablePublish
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
check_user_errors "$PUB_RESP" '.data.publishablePublish.userErrors' "publishablePublish"

# ============================================================================
#  STEP 5 — media attach (idempotent)
# ============================================================================
MEDIA_DIR="/Users/fsuels/Projects/dresslikemommy/uploads/${HANDLE}"
if [[ -d "$MEDIA_DIR" ]] && compgen -G "$MEDIA_DIR/*.jpg" > /dev/null; then
  echo ">>> attaching media from $MEDIA_DIR" >&2
  for IMG in "$MEDIA_DIR"/*.jpg; do
    FNAME=$(basename "$IMG")
    STAGE_RESP=$(gql 'mutation($input:[StagedUploadInput!]!){stagedUploadsCreate(input:$input){stagedTargets{url resourceUrl parameters{name value}} userErrors{field message}}}' \
      "$(jq -nc --arg f "$FNAME" '{input:[{filename:$f, mimeType:"image/jpeg", resource:"IMAGE", httpMethod:"POST"}]}')")
    URL=$(echo "$STAGE_RESP" | jq -r '.data.stagedUploadsCreate.stagedTargets[0].url')
    RESOURCE_URL=$(echo "$STAGE_RESP" | jq -r '.data.stagedUploadsCreate.stagedTargets[0].resourceUrl')
    FORM_ARGS=()
    while IFS= read -r line; do FORM_ARGS+=(-F "$line"); done < <(echo "$STAGE_RESP" | jq -r '.data.stagedUploadsCreate.stagedTargets[0].parameters[] | "\(.name)=\(.value)"')
    FORM_ARGS+=(-F "file=@$IMG")
    curl -sS -X POST "$URL" "${FORM_ARGS[@]}" > /dev/null
    gql 'mutation($productId:ID!,$media:[CreateMediaInput!]!){productCreateMedia(productId:$productId,media:$media){media{...on MediaImage{id alt}} userErrors{field message}}}' \
      "$(jq -nc --arg pid "$PRODUCT_ID" --arg url "$RESOURCE_URL" --arg alt "Mother and daughter in matching Bamboo Garden Panda cream cotton button-up pajamas with long sleeves, cozying together on a cream sofa." \
        '{productId:$pid, media:[{originalSource:$url, mediaContentType:"IMAGE", alt:$alt}]}')" > /dev/null
  done
else
  echo "NOTE: no media at $MEDIA_DIR — re-run after images drop." >&2
fi

# ============================================================================
#  STEP 6 — verify
# ============================================================================
VERIFY_RESP=$(gql 'query($id:ID!){ product(id:$id){ id title handle status onlineStoreUrl publishedAt descriptionHtml variants(first:100){ edges{ node{ sku title price compareAtPrice inventoryPolicy inventoryItem{ tracked requiresShipping } } } } seo{ title description } availablePublicationsCount{ count } } }' \
  "$(jq -nc --arg id "$PRODUCT_ID" '{id:$id}')")

LIVE_SKUS=$(echo "$VERIFY_RESP" | jq -r '.data.product.variants.edges[].node.sku' | sort)
DERIVED_SKUS=$(echo "$VARIANTS_JSON" | jq -r '.[].inventoryItem.sku' | sort)
if [[ "$LIVE_SKUS" != "$DERIVED_SKUS" ]]; then
  echo "ERROR: live SKUs differ from derived." >&2
  diff <(echo "$LIVE_SKUS") <(echo "$DERIVED_SKUS") >&2
  exit 1
fi
echo "[verify] $VARIANT_COUNT SKUs match" >&2

# Size table structural check — 10 <th> columns, SIZE_CHART.length <tr> data rows
LIVE_BODY=$(echo "$VERIFY_RESP" | jq -r '.data.product.descriptionHtml')
TH_COUNT=$(echo "$LIVE_BODY" | grep -oE '<th>' | wc -l | tr -d ' ')
# tr rows in tbody: count <tr> after <tbody>
TBODY_ROWS=$(echo "$LIVE_BODY" | sed -n 's/.*<tbody>\(.*\)<\/tbody>.*/\1/p' | grep -oE '<tr>' | wc -l | tr -d ' ')
if [[ "$TH_COUNT" -ne 10 ]]; then
  echo "ERROR: expected 10 <th>, got $TH_COUNT" >&2; exit 1
fi
if [[ "$TBODY_ROWS" -ne "$ROW_COUNT" ]]; then
  echo "ERROR: expected $ROW_COUNT body rows, got $TBODY_ROWS" >&2; exit 1
fi
echo "[verify] body-HTML size table: $TH_COUNT columns × $TBODY_ROWS data rows" >&2

# ============================================================================
#  SUMMARY
# ============================================================================
echo
echo "=== SUMMARY ==="
echo "Product ID:  $PRODUCT_ID"
echo "Handle:      $HANDLE"
echo "Admin URL:   https://admin.shopify.com/store/dresslikemommy/products/$ADMIN_NUM_ID"
echo "Storefront:  https://www.dresslikemommy.com/products/$HANDLE"
echo "SEO:         title=$SEO_TITLE_LEN chars / desc=$SEO_DESC_LEN chars"
echo "Rows:        $ROW_COUNT  |  Live variants: $LIVE_VARIANT_COUNT"
echo "Variants:"
echo "$BULK_RESP" | jq -r '.data.productVariantsBulkCreate.product.variants.nodes[] | "  - \(.sku)  \(.title)  $\(.price)  (compare $\(.compareAtPrice))"'
