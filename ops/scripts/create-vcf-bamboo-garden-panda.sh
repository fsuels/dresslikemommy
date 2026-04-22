#!/usr/bin/env bash
# ============================================================================
#  VCF — Bamboo Garden Panda Mommy-and-Me Pajama Listing (Shopify Admin 2025-01)
#
#  Vendor source: https://detail.1688.com/offer/792917229223.html
#
#  DESIGN PRINCIPLE — single source of truth: the VENDOR_SIZE_CHART JSON block
#  below drives EVERYTHING downstream (option values, variants, SKUs, body
#  HTML size table, tags, shopify.size metafield, SEO description, summary).
#  This prevents the "size chart says 4 rows, script lists 7 variants" class
#  of bug: change the chart, rerun, and every artifact stays in lockstep.
#
#  To adapt this script to a new vendor offer:
#    1. Update the CONFIG block (handle, title, pricing, tokens, URLs, etc.).
#    2. Replace VENDOR_SIZE_CHART with the rows the vendor actually sells.
#    3. Map shopify.size metaobject GIDs in SIZE_METAOBJECT_MAP for any new
#       size label (or omit — unmapped sizes are skipped, not faked).
#    4. Run. Preflight validation will abort with a clear message if anything
#       is inconsistent before a single Admin API call is made.
#
#  Flow: preflight -> productCreate -> productVariantsBulkCreate ->
#        metafieldsSet -> publishablePublish -> media attach -> verify.
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
  # $1 = query, $2 = variables json
  curl -sS -X POST "$API" \
    -H "X-Shopify-Access-Token: $TOKEN" \
    -H "Content-Type: application/json" \
    -d "$(jq -nc --arg q "$1" --argjson v "$2" '{query:$q, variables:$v}')"
}

# Abort with a user-facing message on any jq userError we see
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
#  CONFIG — product-level constants
# ============================================================================
HANDLE="bamboo-garden-panda-mommy-and-me-pajamas"
TITLE="Bamboo Garden Panda Mommy and Me Pajamas — Short-Sleeve Set"
VENDOR="dresslikemommy.com"
PTYPE="Matching Family Pajamas"
# SEO — expert optimized (≤60 / ≤155). High-intent head terms first, brand suffix for CTR.
SEO_TITLE="Panda Mommy & Me Pajamas — Matching Set | Dress Like Mommy"
CATEGORY_GID="gid://shopify/TaxonomyCategory/aa-1-17-4"
VENDOR_URL="https://detail.1688.com/offer/792917229223.html"

SHORTCODE="VCF"
COLOR_TOKEN="CREAM"
COLOR_NAME="Bamboo Garden Panda Cream"

CHILD_PRICE="28.99"
CHILD_COMPARE="34.99"
MOTHER_PRICE="31.99"
MOTHER_COMPARE="37.49"

# ============================================================================
#  VENDOR_SIZE_CHART — single source of truth
#
#  Each row represents ONE variant the vendor actually produces. Adding or
#  removing a row is all you need to change the listing's variant count.
#
#  Fields:
#    audience     : "child" or "mother"           (drives price + SKU prefix)
#    label        : Shopify size picker value     (must match theme resolver)
#    sku_suffix   : goes into DLM-{SHORTCODE}-{sku_suffix}-{COLOR_TOKEN}
#    age          : body-chart "Age" cell, e.g. "2–3" or "—"
#    weight       : body-chart "Recommended Weight (kg/lbs)" cell
#    height       : body-chart "Recommended Height (cm/in)" cell
#    chest_cm     : half-chest doubled -> full bust in cm (int)
#    sleeve_cm    : sleeve length cm (number)
#    hem_cm       : hem circumference cm (number)
#    length_cm    : garment length cm (number)
# ============================================================================
VENDOR_SIZE_CHART=$(cat <<'JSON'
[
  {"audience":"child","label":"Child 3 Years","sku_suffix":"KID3Y","age":"2–3","weight":"13–16 kg / 29–35 lbs","height":"90–100 cm / 35–39 in","chest_cm":66,"sleeve_cm":19,"hem_cm":99,"length_cm":54},
  {"audience":"child","label":"Child 5 Years","sku_suffix":"KID5Y","age":"4–5","weight":"17–22 kg / 37–49 lbs","height":"105–115 cm / 41–45 in","chest_cm":70,"sleeve_cm":20,"hem_cm":103,"length_cm":64},
  {"audience":"child","label":"Child 8 Years","sku_suffix":"KID8Y","age":"6–8","weight":"22–28 kg / 49–62 lbs","height":"125–140 cm / 49–55 in","chest_cm":74,"sleeve_cm":21.5,"hem_cm":111,"length_cm":74},
  {"audience":"mother","label":"Mother One Size","sku_suffix":"MOMOS","age":"—","weight":"50–72 kg / 110–159 lbs","height":"155–172 cm / 61–68 in","chest_cm":114,"sleeve_cm":30,"hem_cm":144,"length_cm":102}
]
JSON
)

# ============================================================================
#  SIZE_METAOBJECT_MAP — shopify.size standard catalog GIDs.
#  Unmapped labels are SKIPPED (not faked) — the script logs which sizes
#  could not be referenced in shopify.size. This is how "Mother One Size"
#  correctly falls out of the metafield: there is no catalog entry for it.
# ============================================================================
SIZE_METAOBJECT_MAP=$(cat <<'JSON'
{
  "Child 3 Years":  "gid://shopify/Metaobject/129972895841",
  "Child 5 Years":  "gid://shopify/Metaobject/129972961377",
  "Child 8 Years":  "gid://shopify/Metaobject/139840356449"
}
JSON
)

# ============================================================================
#  DESCRIPTIVE COPY — static marketing blocks (not derived from chart)
# ============================================================================
read -r -d '' BULLETS_HTML <<'HTML' || true
<ul><li><strong>Soft breathable cotton blend:</strong> Lightweight knit with a smooth watercolor-painted hand-feel that stays cool on warm nights and gentle against little cheeks.</li><li><strong>Make every moment match:</strong> Coordinating mother-and-daughter sleep sets made for slumber parties, lazy Sundays, holiday mornings, and cozy family bonding — photo-ready in seconds.</li><li><strong>Bamboo Garden Panda print:</strong> A watercolor garden of tumbling baby pandas nestled among trailing bamboo stalks and wild botanicals on a soft cream ground — picture-perfect and quietly whimsical.</li><li><strong>Relaxed raglan-sleeve cut:</strong> Heather-gray raglan short sleeves, a crew neckline, breezy swing body, and a clean contrast-bound hem for a modern sleep-dress silhouette.</li><li><strong>Easy care &amp; breathable:</strong> Machine-wash cold, tumble dry low. Airy cotton-blend knit keeps airflow high and wrinkles low.</li>__SIZE_RANGE_BULLET__</ul>
HTML

read -r -d '' NARRATIVE_HTML <<'HTML' || true
<p>Our Bamboo Garden Panda mommy-and-me sleep set turns bedtime into a watercolor storybook. The soft cream body is painted edge-to-edge with tumbling pandas cuddling among trailing bamboo, wild sage, and tiny botanical sprigs, while heather-gray raglan sleeves frame the look with a modern sporty-sweet contrast. It is the kind of print that belongs in a sun-drenched reading nook — gentle, nostalgic, and quietly whimsical.</p><p>Wear it for slow Sunday mornings, zoo-trip sleepover eves, birthday pajama parties, and those holiday-card mornings when everyone needs to look picture-perfect without trying. The breezy midi silhouette with short raglan sleeves moves easily from pillow fights to pancake-making. The mother style is cut to a generous one-size fit (comfortably sized S through XL with a relaxed, flowing drape).</p><h3>Key Features:</h3><ul><li><strong>Coordinated mother &amp; daughter fit:</strong> Identical watercolor panda print in adult and child cuts so every family photo matches effortlessly.</li><li><strong>Breathable cotton-blend knit:</strong> Lightweight and airy for warm-weather sleep and summer travel.</li><li><strong>Heather-gray raglan sleeves:</strong> Contrast short sleeves and crew neckline give a modern sport-pajama finish.</li><li><strong>Relaxed sleep-dress silhouette:</strong> Swing body with a clean bound hem — easy on-and-off and all-night comfort.</li><li><strong>Mother One Size fit:</strong> Generously cut — 114 cm bust / 144 cm hem — comfortably fits adult S through XL.</li></ul><p>Add the mother one size and the matching child size to your cart to make every moment match — bedtime, brunch, and every snapshot in between.</p>
HTML

BASE_TAGS_JSON='["Mommy and Me","Pajamas","Matching Family Pajamas","Short Sleeve Pajamas","Nightgown","Sleep Dress","Summer","Cream","Gray","Charcoal","Panda","Panda Print","Bamboo","Bamboo Garden","Watercolor","Botanical","Animal Print","Raglan Sleeve","Kung Fu Panda","Zoo","Child 2-3yr","Child 4-5yr","Child 6-8yr"]'

# ============================================================================
#  DERIVED FIELDS — everything below is computed from VENDOR_SIZE_CHART.
#  Do not hand-edit these blocks; edit the chart instead.
# ============================================================================

# -- Preflight: validate chart shape (fail fast, no API calls yet) ----------
ROW_COUNT=$(echo "$VENDOR_SIZE_CHART" | jq 'length')
if [[ "$ROW_COUNT" -lt 1 ]]; then
  echo "ERROR: VENDOR_SIZE_CHART is empty." >&2; exit 1
fi
if ! echo "$VENDOR_SIZE_CHART" | jq -e 'all(.[]; .audience and .label and .sku_suffix and .age and .weight and .height and .chest_cm and .sleeve_cm and .hem_cm and .length_cm)' > /dev/null; then
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

# -- Option values list (Size picker) ---------------------------------------
SIZE_VALUES_JSON=$(echo "$VENDOR_SIZE_CHART" | jq -c '[.[] | {name: .label}]')

# -- Variants payload for productVariantsBulkCreate -------------------------
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

# Sanity: variant count must equal chart row count
VARIANT_COUNT=$(echo "$VARIANTS_JSON" | jq 'length')
if [[ "$VARIANT_COUNT" -ne "$ROW_COUNT" ]]; then
  echo "ERROR: derived variant count ($VARIANT_COUNT) != chart rows ($ROW_COUNT)" >&2; exit 1
fi

# -- Body HTML size table derived from chart --------------------------------
SIZE_TABLE_ROWS=$(echo "$VENDOR_SIZE_CHART" | jq -r '
  .[] | "<tr><td>\(.label)</td><td>\(.age)</td><td>\(.weight)</td><td>\(.height)</td><td>\(.chest_cm) cm / \((.chest_cm/2.54*10|round)/10) in</td><td>\(.sleeve_cm) cm / \((.sleeve_cm/2.54*10|round)/10) in</td><td>—</td><td>\(.hem_cm) cm / \((.hem_cm/2.54*10|round)/10) in</td><td>\(.length_cm) cm / \((.length_cm/2.54*10|round)/10) in</td></tr>"
' | tr -d '\n')

SIZE_TABLE_HTML="<h3>Size Chart</h3><table id=\"size-chart\"><thead><tr><th>Size</th><th>Age</th><th>Recommended Weight (kg/lbs)</th><th>Recommended Height (cm/in)</th><th>Chest/Bust (cm/in)</th><th>Sleeve Length (cm/in)</th><th>Pant/Short Length (cm/in)</th><th>Hip (cm/in)</th><th>Garment Length (cm/in)</th></tr></thead><tbody>${SIZE_TABLE_ROWS}</tbody></table>"

# -- Human-readable size summary for bullet + SEO desc + tags ---------------
CHILD_SHORT=$(echo "$VENDOR_SIZE_CHART" | jq -r '[.[] | select(.audience=="child") | .label | capture("(?<n>[0-9]+) Years").n] | join(", ")')
# Turn "3, 5, 8" -> "3Y, 5Y, 8Y"
CHILD_SHORT_Y=$(echo "$CHILD_SHORT" | sed 's/\([0-9]\+\)/\1Y/g')
MOTHER_LABELS=$(echo "$VENDOR_SIZE_CHART" | jq -r '[.[] | select(.audience=="mother") | .label] | join(", ")')

if [[ -n "$MOTHER_LABELS" ]]; then
  SIZE_RANGE_BULLET="<li><strong>Family size range:</strong> Girls ${CHILD_SHORT_Y} and ${MOTHER_LABELS} so the whole family can twin.</li>"
  SIZE_RANGE_SHORT="Sizes ${CHILD_SHORT_Y} & ${MOTHER_LABELS}"
else
  SIZE_RANGE_BULLET="<li><strong>Kids size range:</strong> Girls ${CHILD_SHORT_Y}.</li>"
  SIZE_RANGE_SHORT="Sizes ${CHILD_SHORT_Y}"
fi

BODY_HTML="${BULLETS_HTML/__SIZE_RANGE_BULLET__/$SIZE_RANGE_BULLET}<p>&nbsp;</p>${SIZE_TABLE_HTML}${NARRATIVE_HTML}"

# -- SEO description (≤155 chars) + length guard ----------------------------
# Expert pattern: action opener ("Shop our") + print + head term ("matching
# mommy-and-me pajamas") + fabric + audience + sizes. Scannable on SERP.
# "Mom One Size" instead of "Mother One Size" saves 3 chars for the size phrase.
SIZE_RANGE_SEO=$(echo "$SIZE_RANGE_SHORT" | sed 's/Mother One Size/Mom One Size/g')
SEO_DESC="Shop our Bamboo Garden Panda matching mommy-and-me pajamas — soft cotton short-sleeve sets for mom + daughter. ${SIZE_RANGE_SEO}."
SEO_DESC_LEN=${#SEO_DESC}
if (( SEO_DESC_LEN > 155 )); then
  # fallback trim #1: drop the audience phrase
  SEO_DESC="Shop our Bamboo Garden Panda matching mommy-and-me pajamas in soft cotton. ${SIZE_RANGE_SEO}. Shop the set."
  SEO_DESC_LEN=${#SEO_DESC}
fi
if (( SEO_DESC_LEN > 155 )); then
  # fallback trim #2: minimal
  SEO_DESC="Bamboo Garden Panda matching mommy-and-me pajamas. ${SIZE_RANGE_SEO}. Shop the set."
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

# -- Tags derived: base + audience labels + vendor URL ----------------------
TAGS_JSON=$(jq -nc \
  --argjson base "$BASE_TAGS_JSON" \
  --argjson chart "$VENDOR_SIZE_CHART" \
  --arg vurl "$VENDOR_URL" '
  ($base + [$chart[] | select(.audience=="mother") | .label] + [$vurl]) | unique_by(.) ')

# -- shopify.size list.metaobject_reference derived from map + chart --------
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
      {ownerId:$pid, namespace:"mm-google-shopping", key:"custom_label_3",  type:"single_line_text_field", value:"Short Sleeve Set"},
      {ownerId:$pid, namespace:"mm-google-shopping", key:"custom_label_4",  type:"single_line_text_field", value:"Family Matching"},
      {ownerId:$pid, namespace:"shopify", key:"age-group",     type:"list.metaobject_reference", value:"[\"gid://shopify/Metaobject/128116523105\",\"gid://shopify/Metaobject/128116490337\"]"},
      {ownerId:$pid, namespace:"shopify", key:"color-pattern", type:"list.metaobject_reference", value:"[\"gid://shopify/Metaobject/69641928801\",\"gid://shopify/Metaobject/69944672353\",\"gid://shopify/Metaobject/130231140449\"]"},
      {ownerId:$pid, namespace:"shopify", key:"fabric",        type:"list.metaobject_reference", value:"[\"gid://shopify/Metaobject/69622399073\"]"},
      {ownerId:$pid, namespace:"shopify", key:"size",          type:"list.metaobject_reference", value:($size_refs | tostring)},
      {ownerId:$pid, namespace:"shopify", key:"target-gender", type:"list.metaobject_reference", value:"[\"gid://shopify/Metaobject/129971617889\"]"},
      {ownerId:$pid, namespace:"global",  key:"title_tag",         type:"single_line_text_field", value:$seo_title},
      {ownerId:$pid, namespace:"global",  key:"description_tag",   type:"single_line_text_field", value:$seo_desc}
    ]
  }')
# Category-restricted metafields intentionally omitted: shopify.sleeve-length-type,
# shopify.neckline (Dresses/Tops only), shopify.clothing-features (catalog lacks
# a fit for summer pajamas). Unmapped sizes like "Mother One Size" are skipped
# above rather than faked.

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
MEDIA_DIR="/Users/fsuels/Projects/dresslikemommy/uploads/bamboo-garden-panda-mommy-and-me-pajamas"
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
      "$(jq -nc --arg pid "$PRODUCT_ID" --arg url "$RESOURCE_URL" --arg alt "Mom and daughter in matching Bamboo Garden Panda cream watercolor short-sleeve sleep dresses, sitting together on a cream sofa in a bright sunlit living room." \
        '{productId:$pid, media:[{originalSource:$url, mediaContentType:"IMAGE", alt:$alt}]}')" | jq . >&2
  done
else
  echo "NOTE: no local media at $MEDIA_DIR — skipping media attach. Drop hero image there and rerun this block." >&2
fi

# ============================================================================
#  STEP 6 — verify (live vs derived)
# ============================================================================
VERIFY_RESP=$(gql 'query($id:ID!){ product(id:$id){ id title status variants(first:100){ edges{ node{ sku title price compareAtPrice inventoryPolicy inventoryItem{ tracked } } } } availablePublicationsCount{ count } seo{ title description } metafields(first:50){ edges{ node{ namespace key } } } } }' \
  "$(jq -nc --arg id "$PRODUCT_ID" '{id:$id}')")

LIVE_SKUS=$(echo "$VERIFY_RESP" | jq -r '.data.product.variants.edges[].node.sku' | sort)
DERIVED_SKUS=$(echo "$VARIANTS_JSON" | jq -r '.[].inventoryItem.sku' | sort)
if [[ "$LIVE_SKUS" != "$DERIVED_SKUS" ]]; then
  echo "ERROR: live SKUs diverge from derived SKUs." >&2
  diff <(echo "$LIVE_SKUS") <(echo "$DERIVED_SKUS") >&2 || true
  exit 1
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
