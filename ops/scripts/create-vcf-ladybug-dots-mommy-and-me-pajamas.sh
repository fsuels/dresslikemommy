#!/usr/bin/env bash
set -euo pipefail

ENV_FILE="${SHOPIFY_ENV_FILE:-${HOME}/.config/dresslikemommy/shopify-admin.env}"
if [[ -f "$ENV_FILE" ]]; then
  # shellcheck disable=SC1090
  source "$ENV_FILE"
fi
: "${SHOPIFY_STORE_DOMAIN:?SHOPIFY_STORE_DOMAIN not set}"
: "${SHOPIFY_ADMIN_ACCESS_TOKEN:?SHOPIFY_ADMIN_ACCESS_TOKEN not set}"

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
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

cm_to_in() {
  python3 - "$1" <<'PY'
from decimal import Decimal, ROUND_HALF_UP
import sys
value = Decimal(sys.argv[1])
inch = (value / Decimal("2.54")).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
print(format(inch, "f"))
PY
}

HANDLE="ladybug-dots-mommy-and-me-pajamas"
TITLE="Ladybug Dots Mommy and Me Pajamas — Short-Sleeve Set"
SEO_TITLE="Ladybug Mommy & Me Pajamas — Cotton Set | Dress Like Mommy"
SEO_DESC="Shop our Ladybug Dots matching mommy-and-me pajamas — bamboo-cotton gauze short-sleeve set for mom + daughter. Sizes 2Y–10Y, Mom S–XL."
PRODUCT_TYPE="Matching Family Pajamas"
CUSTOM_TYPE="Two-Piece Pajama Set"
TAXONOMY_GID="gid://shopify/TaxonomyCategory/aa-1-17-4"
GOOGLE_PRODUCT_CATEGORY="Apparel & Accessories > Clothing > Sleepwear & Loungewear > Pajamas"
VENDOR="dresslikemommy.com"
VENDOR_URL="https://detail.1688.com/offer/1026510859610.html"
VENDOR_HISTORY_TITLE="安旦26新品春夏竹棉纱布亲子家居服甜美荷叶边短袖长裤居家套装 - 阿里巴巴"
DESIGNS_TO_LIST="瓢虫点点（成人款-小V领）, 瓢虫点点（儿童款-前扣娃娃领）"
SEASON="Summer"
SHORTCODE="VCF"
COLOR_TOKEN="CREAM"
PRINT_NAME="Ladybug Dots"
COLOR_NAME="Ladybug Dots"
CHILD_PRICE="33.99"
CHILD_COMPARE="39.09"
MOTHER_PRICE="37.99"
MOTHER_COMPARE="43.69"
PHOTO_ALT="Mom and daughter in matching Ladybug Dots bamboo-cotton gauze pajamas with tiny ladybugs, wildflowers, and dragonflies, seated together on a cream sofa."

ADMIN_URL_BASE="https://admin.shopify.com/store/dresslikemommy/products"
LIVE_URL_BASE="https://www.dresslikemommy.com/products"
OUT_LISTING="${REPO_ROOT}/${HANDLE}-listing.md"
OUT_CSV="${REPO_ROOT}/${HANDLE}-shopify-import.csv"
VERIFY_JSON="${REPO_ROOT}/ops/scripts/.ladybug-dots-verify.json"
LAST_ID_FILE="${REPO_ROOT}/ops/scripts/.ladybug-dots-last-product-id"
MEDIA_DIR="${REPO_ROOT}/uploads/${HANDLE}"
RESUME_PRODUCT_ID="${RESUME_PRODUCT_ID:-}"

SIZE_CHART=$(cat <<'JSON'
[
  {"audience":"child","vendor_label":"90","picker_label":"Child 2 Years","sku_suffix":"KID2Y","age":"2","weight":"12–14 kg / 26–31 lbs","height":"85–95 cm / 33–37 in","chest_cm":67,"hip_cm":65,"waist_cm":42,"length_cm":35.5,"sleeve_cm":16,"pant_cm":52,"shopify_size_gid":"gid://shopify/Metaobject/129972863073"},
  {"audience":"child","vendor_label":"100","picker_label":"Child 3 Years","sku_suffix":"KID3Y","age":"3","weight":"14–16 kg / 31–35 lbs","height":"95–105 cm / 37–41 in","chest_cm":71,"hip_cm":69,"waist_cm":44,"length_cm":39.5,"sleeve_cm":16.5,"pant_cm":57,"shopify_size_gid":"gid://shopify/Metaobject/129972895841"},
  {"audience":"child","vendor_label":"110","picker_label":"Child 4 Years","sku_suffix":"KID4Y","age":"4","weight":"16–19 kg / 35–42 lbs","height":"105–115 cm / 41–45 in","chest_cm":75,"hip_cm":73,"waist_cm":46,"length_cm":42,"sleeve_cm":17,"pant_cm":62,"shopify_size_gid":"gid://shopify/Metaobject/129972928609"},
  {"audience":"child","vendor_label":"120","picker_label":"Child 5 Years","sku_suffix":"KID5Y","age":"5","weight":"19–22 kg / 42–49 lbs","height":"115–125 cm / 45–49 in","chest_cm":79,"hip_cm":77,"waist_cm":48,"length_cm":45,"sleeve_cm":17.5,"pant_cm":67,"shopify_size_gid":"gid://shopify/Metaobject/129972961377"},
  {"audience":"child","vendor_label":"130","picker_label":"Child 6-7 Years","sku_suffix":"KID67Y","age":"6–7","weight":"22–26 kg / 49–57 lbs","height":"125–135 cm / 49–53 in","chest_cm":83,"hip_cm":81,"waist_cm":50,"length_cm":48,"sleeve_cm":18,"pant_cm":72,"shopify_size_gid":"gid://shopify/Metaobject/139840323681"},
  {"audience":"child","vendor_label":"140","picker_label":"Child 8 Years","sku_suffix":"KID8Y","age":"8","weight":"26–30 kg / 57–66 lbs","height":"135–145 cm / 53–57 in","chest_cm":87,"hip_cm":84,"waist_cm":52,"length_cm":52,"sleeve_cm":18.5,"pant_cm":77,"shopify_size_gid":"gid://shopify/Metaobject/139840356449"},
  {"audience":"child","vendor_label":"150","picker_label":"Child 9-10 Years","sku_suffix":"KID910Y","age":"9–10","weight":"30–35 kg / 66–77 lbs","height":"145–155 cm / 57–61 in","chest_cm":91,"hip_cm":88,"waist_cm":54,"length_cm":56,"sleeve_cm":19,"pant_cm":83,"shopify_size_gid":"gid://shopify/Metaobject/139840389217"},
  {"audience":"mother","vendor_label":"S","picker_label":"Mother S","sku_suffix":"MOMS","age":"—","weight":"45–52 kg / 99–115 lbs","height":"155–160 cm / 61–63 in","chest_cm":99,"hip_cm":95,"waist_cm":72,"length_cm":62,"sleeve_cm":22.5,"pant_cm":97,"shopify_size_gid":"gid://shopify/Metaobject/129975255137"},
  {"audience":"mother","vendor_label":"M","picker_label":"Mother M","sku_suffix":"MOMM","age":"—","weight":"52–58 kg / 115–128 lbs","height":"160–165 cm / 63–65 in","chest_cm":103,"hip_cm":99,"waist_cm":74,"length_cm":64,"sleeve_cm":23.5,"pant_cm":99,"shopify_size_gid":"gid://shopify/Metaobject/129975222369"},
  {"audience":"mother","vendor_label":"L","picker_label":"Mother L","sku_suffix":"MOML","age":"—","weight":"58–65 kg / 128–143 lbs","height":"163–170 cm / 64–67 in","chest_cm":107,"hip_cm":103,"waist_cm":76,"length_cm":66,"sleeve_cm":24.5,"pant_cm":101,"shopify_size_gid":"gid://shopify/Metaobject/129975189601"},
  {"audience":"mother","vendor_label":"XL","picker_label":"Mother XL","sku_suffix":"MOMXL","age":"—","weight":"65–72 kg / 143–159 lbs","height":"165–172 cm / 65–68 in","chest_cm":111,"hip_cm":107,"waist_cm":78,"length_cm":68,"sleeve_cm":25.5,"pant_cm":103,"shopify_size_gid":"gid://shopify/Metaobject/129975287905"}
]
JSON
)

SIZE_ROW_COUNT=$(echo "$SIZE_CHART" | jq 'length')
SIZE_VALUES_JSON=$(echo "$SIZE_CHART" | jq -c '[.[] | {name: .picker_label}]')
SIZE_GIDS_JSON=$(echo "$SIZE_CHART" | jq -c '[.[] | .shopify_size_gid]')
TAGS_JSON=$(echo "$SIZE_CHART" | jq -c --arg url "$VENDOR_URL" '
  [
    "Mommy and Me",
    "Pajamas",
    "Matching Family Pajamas",
    "Short Sleeve Pajamas",
    "Summer",
    "Blue",
    "Sky Blue",
    "Yellow",
    "Green",
    "Floral",
    "Multicolor",
    "Ladybug",
    "Ladybug Dots",
    "Wildflower",
    "Dragonfly",
    "Botanical",
    "Bamboo Cotton Gauze",
    "Bamboo",
    "Cotton Gauze",
    "V-Neck",
    "Peter Pan Collar",
    "Front Button",
    "Child 2-3yr",
    "Child 4-5yr",
    "Child 6-8yr",
    "Child 9-10yr",
    $url
  ] + ([.[] | select(.audience=="mother") | .picker_label]) | unique')

VARIANTS_JSON=$(echo "$SIZE_CHART" | jq -c \
  --arg cp "$CHILD_PRICE" \
  --arg cc "$CHILD_COMPARE" \
  --arg mp "$MOTHER_PRICE" \
  --arg mc "$MOTHER_COMPARE" \
  --arg sc "$SHORTCODE" \
  --arg ct "$COLOR_TOKEN" \
  --arg color "$COLOR_NAME" '
  [ .[] | {
      price: (if .audience=="child" then $cp else $mp end),
      compareAtPrice: (if .audience=="child" then $cc else $mc end),
      inventoryPolicy: "DENY",
      inventoryItem: {
        sku: ("DLM-" + $sc + "-" + .sku_suffix + "-" + $ct),
        tracked: true,
        requiresShipping: true
      },
      optionValues: [
        {optionName:"Size", name:.picker_label},
        {optionName:"Color", name:$color}
      ]
    }
  ]')

SIZE_PHRASE="Sizes 2Y–10Y, Mom S–XL."
BODY_HTML=$(echo "$SIZE_CHART" | jq -r '
  def in1($cm): (($cm / 2.54) * 10 | round / 10 | tostring);
  def num($v): ($v | tostring);
  def cm_in($v): (num($v) + " cm / " + in1($v) + " in");
  def row:
    "<tr><td>" + .picker_label + "</td><td>" + .age + "</td><td>" + .weight + "</td><td>" + .height + "</td><td>" + cm_in(.chest_cm) + "</td><td>" + cm_in(.sleeve_cm) + "</td><td>" + cm_in(.pant_cm) + "</td><td>" + cm_in(.hip_cm) + "</td><td>" + cm_in(.waist_cm) + "</td><td>" + cm_in(.length_cm) + "</td></tr>";
  (map(select(.audience=="child") | row) | join("")) as $kids |
  (map(select(.audience=="mother") | row) | join("")) as $moms |
  "<ul>" +
  "<li><strong>Fabric:</strong> Soft bamboo-cotton gauze with a breathable, airy hand-feel that stays light for warm-weather lounging and bedtime.</li>" +
  "<li><strong>Family Story:</strong> Matching mom-and-mini pajama sets made for brunch, birthdays, holiday cards, and those picture-perfect slow mornings at home.</li>" +
  "<li><strong>Print:</strong> Ladybug Dots brings tiny ladybugs, scattered wildflowers, and airy dragonflies across a pale blue ground for a sweet garden-story finish.</li>" +
  "<li><strong>Design Details:</strong> Mom wears the soft small V-neck top while the child style keeps the front-button doll collar, both paired with easy long pants for coordinated comfort.</li>" +
  "<li><strong>Care:</strong> Gentle cold wash and low-heat drying keep the gauzy feel soft and the print fresh for repeat wear.</li>" +
  "<li><strong>Size Range:</strong> " + "Children 2Y–10Y plus Mother S–XL so the whole family can make every moment match." + "</li>" +
  "</ul>" +
  "<h3>Size Chart</h3>" +
  "<table id=\"size-chart\"><thead><tr><th>Size</th><th>Age</th><th>Weight</th><th>Height</th><th>Chest/Bust</th><th>Sleeve</th><th>Pant/Short</th><th>Hip</th><th>Waist</th><th>Garment Length</th></tr></thead><tbody><!-- Children Sizes -->" + $kids + "<!-- Adult Sizes -->" + $moms + "</tbody></table>" +
  "<p>Our Ladybug Dots mommy-and-me pajama set turns everyday wind-down time into a little garden story. The airy bamboo-cotton gauze is sprinkled with tiny ladybugs, drifting dragonflies, and delicate meadow florals across a soft pale blue ground that feels calm, sweet, and camera-ready. Mom’s relaxed V-neck top keeps the look clean and easy, while the child style adds a button-front Peter Pan collar that feels extra special without losing comfort. It is an effortless matching set for bedtime routines, weekend cartoons, and family photos that still feel natural.</p>" +
  "<p>Because the silhouettes coordinate rather than copy exactly, the set feels styled and photo-ready instead of costume-like. The long pants keep coverage soft and easy for cooler mornings, while the lightweight gauze construction stays breathable through spring and summer. Wear it for pancake brunches, birthday mornings, sleepovers at grandma’s, and the kind of holiday-card snapshots that become family favorites. When you want matching that still feels elevated, this is the kind of pajama set that makes every moment match.</p>" +
  "<h3>Key Features:</h3><ul>" +
  "<li><strong>Breathable gauze fabric:</strong> Bamboo-cotton construction feels airy, soft, and light for warm-weather lounging.</li>" +
  "<li><strong>Two coordinated necklines:</strong> Mom’s soft V-neck and the child’s front-button doll collar keep the pairing polished and charming.</li>" +
  "<li><strong>Long-pant comfort:</strong> Relaxed full-length bottoms make the set easy for bedtime, mornings, and travel.</li>" +
  "<li><strong>Photo-ready print story:</strong> Tiny ladybugs, meadow flowers, and dragonflies create a whimsical garden look.</li>" +
  "<li><strong>Matching family feel:</strong> Child sizes 2Y–10Y and Mother S–XL make the duo easy to style together.</li>" +
  "</ul><p>Choose mom’s size and your little one’s match to make bedtime, brunch, and every snapshot in between feel a little more picture-perfect.</p>"
')

if ! echo "$SIZE_CHART" | jq -e 'all(.[]; .audience and .vendor_label and .picker_label and .sku_suffix and .age and .weight and .height and .chest_cm and .hip_cm and .waist_cm and .length_cm)' >/dev/null; then
  echo "ERROR: SIZE_CHART row is missing a required field." >&2
  exit 1
fi

DUPES=$(echo "$SIZE_CHART" | jq -r '[.[].picker_label] | group_by(.)[] | select(length>1) | .[0]')
if [[ -n "$DUPES" ]]; then
  echo "ERROR: duplicate picker_label in SIZE_CHART: $DUPES" >&2
  exit 1
fi

if [[ "$(echo "$SIZE_VALUES_JSON" | jq 'length')" -ne "$SIZE_ROW_COUNT" ]]; then
  echo "ERROR: productOptions.Size.values count mismatch." >&2
  exit 1
fi
if [[ "$(echo "$VARIANTS_JSON" | jq 'length')" -ne "$SIZE_ROW_COUNT" ]]; then
  echo "ERROR: variants payload count mismatch." >&2
  exit 1
fi
if [[ ${#TITLE} -gt 70 ]]; then
  echo "ERROR: Title exceeds 70 chars." >&2
  exit 1
fi
if [[ ${#SEO_TITLE} -gt 60 ]]; then
  echo "ERROR: SEO title exceeds 60 chars." >&2
  exit 1
fi
if [[ ${#SEO_DESC} -gt 155 ]]; then
  echo "ERROR: SEO description exceeds 155 chars." >&2
  exit 1
fi

if [[ -n "$RESUME_PRODUCT_ID" ]]; then
  PRODUCT_ID="$RESUME_PRODUCT_ID"
  echo ">>> resume existing product: $PRODUCT_ID" >&2
  echo "$PRODUCT_ID" > "$LAST_ID_FILE"
  ADMIN_NUM_ID="${PRODUCT_ID##*/}"
else
  SEARCH_QUERY='query($q:String!){ products(first:1, query:$q){ edges{ node{ id handle title } } } }'
  SEARCH_VARS=$(jq -nc --arg q "handle:${HANDLE}" '{q:$q}')
  SEARCH_RESP=$(gql "$SEARCH_QUERY" "$SEARCH_VARS")
  EXISTING_ID=$(echo "$SEARCH_RESP" | jq -r '.data.products.edges[0].node.id // empty')
  if [[ -n "$EXISTING_ID" ]]; then
    echo "ERROR: product handle already exists: $EXISTING_ID" >&2
    exit 1
  fi

  CREATE_QUERY='mutation ProductCreate($input: ProductInput!) {
    productCreate(input: $input) {
      product { id handle title status }
      userErrors { field message }
    }
  }'
  CREATE_VARS=$(jq -nc \
    --arg title "$TITLE" \
    --arg handle "$HANDLE" \
    --arg body "$BODY_HTML" \
    --arg vendor "$VENDOR" \
    --arg product_type "$PRODUCT_TYPE" \
    --arg category "$TAXONOMY_GID" \
    --arg seo_title "$SEO_TITLE" \
    --arg seo_desc "$SEO_DESC" \
    --arg color "$COLOR_NAME" \
    --argjson tags "$TAGS_JSON" \
    --argjson sizes "$SIZE_VALUES_JSON" '
    {
      input: {
        title: $title,
        handle: $handle,
        descriptionHtml: $body,
        vendor: $vendor,
        productType: $product_type,
        tags: $tags,
        status: "ACTIVE",
        category: $category,
        seo: {title:$seo_title, description:$seo_desc},
        productOptions: [
          {name:"Size", values:$sizes},
          {name:"Color", values:[{name:$color}]}
        ]
      }
    }')

  echo ">>> productCreate" >&2
  CREATE_RESP=$(gql "$CREATE_QUERY" "$CREATE_VARS")
  check_user_errors "$CREATE_RESP" '.data.productCreate.userErrors' "productCreate"
  PRODUCT_ID=$(echo "$CREATE_RESP" | jq -r '.data.productCreate.product.id // empty')
  if [[ -z "$PRODUCT_ID" ]]; then
    echo "ERROR: productCreate returned no product id." >&2
    exit 1
  fi
  echo "$PRODUCT_ID" > "$LAST_ID_FILE"
  ADMIN_NUM_ID="${PRODUCT_ID##*/}"

  UPDATE_QUERY='mutation ProductUpdate($input: ProductInput!) {
    productUpdate(input: $input) {
      product { id seo { title description } }
      userErrors { field message }
    }
  }'
  UPDATE_VARS=$(jq -nc --arg id "$PRODUCT_ID" --arg title "$SEO_TITLE" --arg desc "$SEO_DESC" '
    {input:{id:$id, seo:{title:$title, description:$desc}}}')
  echo ">>> productUpdate (seo mirror)" >&2
  UPDATE_RESP=$(gql "$UPDATE_QUERY" "$UPDATE_VARS")
  check_user_errors "$UPDATE_RESP" '.data.productUpdate.userErrors' "productUpdate"

  BULK_QUERY='mutation ProductVariantsBulkCreate($productId: ID!, $variants: [ProductVariantsBulkInput!]!, $strategy: ProductVariantsBulkCreateStrategy) {
    productVariantsBulkCreate(productId: $productId, variants: $variants, strategy: $strategy) {
      product { id variants(first: 100) { nodes { id sku title price compareAtPrice inventoryPolicy selectedOptions { name value } inventoryItem { tracked requiresShipping } } } }
      userErrors { field message }
    }
  }'
  BULK_VARS=$(jq -nc --arg pid "$PRODUCT_ID" --argjson vars "$VARIANTS_JSON" '
    {productId:$pid, variants:$vars, strategy:"REMOVE_STANDALONE_VARIANT"}')
  echo ">>> productVariantsBulkCreate" >&2
  BULK_RESP=$(gql "$BULK_QUERY" "$BULK_VARS")
  check_user_errors "$BULK_RESP" '.data.productVariantsBulkCreate.userErrors' "productVariantsBulkCreate"
  LIVE_VARIANT_COUNT=$(echo "$BULK_RESP" | jq '.data.productVariantsBulkCreate.product.variants.nodes | length')
  if [[ "$LIVE_VARIANT_COUNT" -ne "$SIZE_ROW_COUNT" ]]; then
    echo "ERROR: live variant count mismatch immediately after bulk create." >&2
    exit 1
  fi
fi

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
  --arg size_refs "$SIZE_GIDS_JSON" '
  {
    metafields: [
      {ownerId:$pid, namespace:"custom", key:"category1", type:"single_line_text_field", value:"Mommy and Me"},
      {ownerId:$pid, namespace:"custom", key:"subcategory", type:"single_line_text_field", value:"Pajamas"},
      {ownerId:$pid, namespace:"custom", key:"subcategory2", type:"single_line_text_field", value:"Summer Pajamas"},
      {ownerId:$pid, namespace:"custom", key:"pattern", type:"single_line_text_field", value:"Ladybug Dots wildflower print on pale blue bamboo-cotton gauze"},
      {ownerId:$pid, namespace:"custom", key:"style", type:"single_line_text_field", value:"Matching Family Set"},
      {ownerId:$pid, namespace:"custom", key:"type", type:"single_line_text_field", value:"Two-Piece Pajama Set"},
      {ownerId:$pid, namespace:"mm-google-shopping", key:"custom_product", type:"boolean", value:"false"},
      {ownerId:$pid, namespace:"mm-google-shopping", key:"gender", type:"single_line_text_field", value:"female"},
      {ownerId:$pid, namespace:"mm-google-shopping", key:"age_group", type:"single_line_text_field", value:"adult"},
      {ownerId:$pid, namespace:"mm-google-shopping", key:"condition", type:"single_line_text_field", value:"new"},
      {ownerId:$pid, namespace:"mm-google-shopping", key:"custom_label_0", type:"single_line_text_field", value:"Mommy and Me"},
      {ownerId:$pid, namespace:"mm-google-shopping", key:"custom_label_1", type:"single_line_text_field", value:"Ladybug Dots"},
      {ownerId:$pid, namespace:"mm-google-shopping", key:"custom_label_2", type:"single_line_text_field", value:"Summer"},
      {ownerId:$pid, namespace:"mm-google-shopping", key:"custom_label_3", type:"single_line_text_field", value:"Short-Sleeve Set"},
      {ownerId:$pid, namespace:"mm-google-shopping", key:"custom_label_4", type:"single_line_text_field", value:"Family Matching"},
      {ownerId:$pid, namespace:"shopify", key:"age-group", type:"list.metaobject_reference", value:"[\"gid://shopify/Metaobject/128116523105\",\"gid://shopify/Metaobject/128116490337\"]"},
      {ownerId:$pid, namespace:"shopify", key:"color-pattern", type:"list.metaobject_reference", value:"[\"gid://shopify/Metaobject/69639766113\",\"gid://shopify/Metaobject/69622104161\",\"gid://shopify/Metaobject/70220546145\",\"gid://shopify/Metaobject/129971519585\",\"gid://shopify/Metaobject/130231140449\"]"},
      {ownerId:$pid, namespace:"shopify", key:"fabric", type:"list.metaobject_reference", value:"[\"gid://shopify/Metaobject/69622399073\"]"},
      {ownerId:$pid, namespace:"shopify", key:"size", type:"list.metaobject_reference", value:$size_refs},
      {ownerId:$pid, namespace:"shopify", key:"target-gender", type:"list.metaobject_reference", value:"[\"gid://shopify/Metaobject/129971617889\"]"},
      {ownerId:$pid, namespace:"global", key:"title_tag", type:"single_line_text_field", value:$seo_title},
      {ownerId:$pid, namespace:"global", key:"description_tag", type:"single_line_text_field", value:$seo_desc}
    ]
  }')
echo ">>> metafieldsSet" >&2
MF_RESP=$(gql "$MF_QUERY" "$MF_VARS")
check_user_errors "$MF_RESP" '.data.metafieldsSet.userErrors' "metafieldsSet"
MF_COUNT=$(echo "$MF_RESP" | jq '.data.metafieldsSet.metafields | length')

PUB_QUERY='mutation PublishablePublish($id: ID!, $input: [PublicationInput!]!) {
  publishablePublish(id: $id, input: $input) {
    publishable { availablePublicationsCount { count } }
    userErrors { field message }
  }
}'
PUB_VARS=$(jq -nc --arg pid "$PRODUCT_ID" '
  {id:$pid,input:[
    {publicationId:"gid://shopify/Publication/55169925"},
    {publicationId:"gid://shopify/Publication/21969633377"},
    {publicationId:"gid://shopify/Publication/29172400225"},
    {publicationId:"gid://shopify/Publication/76582879329"},
    {publicationId:"gid://shopify/Publication/76604768353"}
  ]}')
echo ">>> publishablePublish" >&2
PUB_RESP=$(gql "$PUB_QUERY" "$PUB_VARS")
check_user_errors "$PUB_RESP" '.data.publishablePublish.userErrors' "publishablePublish"

if [[ -d "$MEDIA_DIR" ]]; then
  shopt -s nullglob
  MEDIA_FILES=("$MEDIA_DIR"/*.jpg "$MEDIA_DIR"/*.jpeg "$MEDIA_DIR"/*.png "$MEDIA_DIR"/*.webp)
  shopt -u nullglob
else
  MEDIA_FILES=()
fi

if [[ ${#MEDIA_FILES[@]} -gt 0 ]]; then
  echo ">>> media attach (${#MEDIA_FILES[@]} files)" >&2
  EXISTING_MEDIA_RESP=$(gql 'query($id:ID!){ product(id:$id){ media(first:50){ nodes{ alt } } } }' "$(jq -nc --arg id "$PRODUCT_ID" '{id:$id}')")
  EXISTING_MEDIA_ALTS=$(echo "$EXISTING_MEDIA_RESP" | jq -c '[.data.product.media.nodes[].alt // empty]')
  for img in "${MEDIA_FILES[@]}"; do
    ext="${img##*.}"
    ext_lc="$(printf '%s' "$ext" | tr '[:upper:]' '[:lower:]')"
    mime="image/jpeg"
    case "$ext_lc" in
      png) mime="image/png" ;;
      webp) mime="image/webp" ;;
      jpg|jpeg) mime="image/jpeg" ;;
    esac
    fname="$(basename "$img")"
    alt="$PHOTO_ALT"
    case "$fname" in
      *size-chart*)
        alt="Size chart for the Ladybug Dots mommy-and-me bamboo-cotton gauze pajama set with child 90-150 and mother S-XL measurements."
        ;;
      hero*|lifestyle*)
        alt="$PHOTO_ALT"
        ;;
      *)
        alt="Lifestyle image of the Ladybug Dots mommy-and-me bamboo-cotton gauze pajama set."
        ;;
    esac
    if echo "$EXISTING_MEDIA_ALTS" | jq -e --arg alt "$alt" 'index($alt) != null' >/dev/null; then
      echo ">>> media skip (already attached): $fname" >&2
      continue
    fi
    STAGE_RESP=$(gql 'mutation($input:[StagedUploadInput!]!){ stagedUploadsCreate(input:$input){ stagedTargets{ url resourceUrl parameters{ name value } } userErrors{ field message } } }' \
      "$(jq -nc --arg fname "$fname" --arg mime "$mime" '{input:[{filename:$fname,mimeType:$mime,resource:"IMAGE",httpMethod:"POST"}]}')")
    check_user_errors "$STAGE_RESP" '.data.stagedUploadsCreate.userErrors' "stagedUploadsCreate"
    upload_url="$(echo "$STAGE_RESP" | jq -r '.data.stagedUploadsCreate.stagedTargets[0].url')"
    resource_url="$(echo "$STAGE_RESP" | jq -r '.data.stagedUploadsCreate.stagedTargets[0].resourceUrl')"
    FORM_ARGS=()
    while IFS= read -r line; do
      FORM_ARGS+=(-F "$line")
    done < <(echo "$STAGE_RESP" | jq -r '.data.stagedUploadsCreate.stagedTargets[0].parameters[] | "\(.name)=\(.value)"')
    FORM_ARGS+=(-F "file=@$img")
    curl -sS -X POST "$upload_url" "${FORM_ARGS[@]}" >/dev/null
    MEDIA_RESP=$(gql 'mutation($productId:ID!,$media:[CreateMediaInput!]!){ productCreateMedia(productId:$productId,media:$media){ media{ alt mediaContentType ... on MediaImage { id image { url } } } userErrors{ field message } } }' \
      "$(jq -nc --arg pid "$PRODUCT_ID" --arg src "$resource_url" --arg alt "$alt" '{productId:$pid,media:[{originalSource:$src,mediaContentType:"IMAGE",alt:$alt}]}')")
    check_user_errors "$MEDIA_RESP" '.data.productCreateMedia.userErrors' "productCreateMedia"
    EXISTING_MEDIA_ALTS=$(echo "$EXISTING_MEDIA_ALTS" | jq -c --arg alt "$alt" '. + [$alt]')
  done
else
  echo "NOTE: no media files found at $MEDIA_DIR" >&2
fi

VERIFY_QUERY='query($id: ID!) {
  product(id: $id) {
    id
    handle
    title
    status
    onlineStoreUrl
    publishedAt
    descriptionHtml
    tags
    seo { title description }
    category { id name }
    collections(first: 50) { nodes { title } }
    media(first: 20) {
      nodes {
        alt
        mediaContentType
        ... on MediaImage { image { url } }
      }
    }
    variants(first: 100) {
      nodes {
        sku
        title
        price
        compareAtPrice
        inventoryPolicy
        inventoryItem { tracked requiresShipping }
      }
    }
  }
}'
VERIFY_VARS=$(jq -nc --arg id "$PRODUCT_ID" '{id:$id}')

COLLECTIONS_JSON='[]'
for _ in 1 2 3 4 5 6; do
  VERIFY_RESP=$(gql "$VERIFY_QUERY" "$VERIFY_VARS")
  COLLECTIONS_JSON=$(echo "$VERIFY_RESP" | jq -c '.data.product.collections.nodes // []')
  if [[ "$COLLECTIONS_JSON" != "[]" ]]; then
    break
  fi
  sleep 10
done
echo "$VERIFY_RESP" | jq . > "$VERIFY_JSON"

python3 - "$VERIFY_JSON" "$SIZE_ROW_COUNT" "$TITLE" "$SEO_TITLE" "$SEO_DESC" "$VARIANTS_JSON" "$SIZE_CHART" "$VENDOR_URL" <<'PY'
import json
import re
import sys

verify_path, row_count, title, seo_title, seo_desc, variants_json, size_chart_json, vendor_url = sys.argv[1:]
row_count = int(row_count)
verify = json.load(open(verify_path))
product = verify["data"]["product"]
chart = json.loads(size_chart_json)
variants = json.loads(variants_json)

live_skus = sorted(v["sku"] for v in product["variants"]["nodes"])
derived_skus = sorted(v["inventoryItem"]["sku"] for v in variants)
if live_skus != derived_skus:
    raise SystemExit("ERROR: live SKUs sorted != derived SKUs sorted")
if len(product["variants"]["nodes"]) != row_count:
    raise SystemExit("ERROR: live variant count mismatch")
if len(title) > 70 or len(seo_title) > 60 or len(seo_desc) > 155:
    raise SystemExit("ERROR: title or SEO lengths out of bounds")
if product["publishedAt"] is None or not product["onlineStoreUrl"]:
    raise SystemExit("ERROR: product is not live on Online Store")
body = product["descriptionHtml"]
thead_match = re.search(r"<thead>\s*<tr>(.*?)</tr>\s*</thead>", body, re.S)
tbody_match = re.search(r"<tbody>(.*?)</tbody>", body, re.S)
if not thead_match or not tbody_match:
    raise SystemExit("ERROR: missing size-chart thead/tbody")
th_count = len(re.findall(r"<th>", thead_match.group(1)))
if th_count != 10:
    raise SystemExit(f"ERROR: size-chart column count {th_count} != 10")
rows = re.findall(r"<tr>(.*?)</tr>", tbody_match.group(1), re.S)
if len(rows) != row_count:
    raise SystemExit(f"ERROR: size-chart row count {len(rows)} != {row_count}")
first_cells = []
for row in rows:
    cells = re.findall(r"<td>(.*?)</td>", row, re.S)
    if len(cells) != 10:
        raise SystemExit("ERROR: one or more size-chart rows do not have 10 columns")
    first_cells.append(re.sub(r"<.*?>", "", cells[0]).strip())
    if not re.sub(r"<.*?>", "", cells[1]).strip():
        raise SystemExit("ERROR: blank age column cell found")
    waist = re.sub(r"<.*?>", "", cells[8]).strip()
    if "cm /" not in waist:
        raise SystemExit("ERROR: waist cell missing dual-unit formatting")
expected_labels = [row["picker_label"] for row in chart]
if first_cells != expected_labels:
    raise SystemExit("ERROR: size-chart first column labels do not match picker labels")
tags = set(product["tags"])
required_tags = {
    "Mommy and Me",
    "Pajamas",
    "Matching Family Pajamas",
    "Short Sleeve Pajamas",
    "Summer",
    vendor_url,
    "Child 2-3yr",
    "Child 4-5yr",
    "Child 6-8yr",
    "Child 9-10yr",
    "Mother S",
    "Mother M",
    "Mother L",
    "Mother XL",
}
missing = sorted(required_tags - tags)
if missing:
    raise SystemExit("ERROR: missing required tags: " + ", ".join(missing))
for live in product["variants"]["nodes"]:
    if live["inventoryPolicy"] != "DENY":
        raise SystemExit("ERROR: inventoryPolicy must be DENY")
    if not live["inventoryItem"]["tracked"] or not live["inventoryItem"]["requiresShipping"]:
        raise SystemExit("ERROR: tracked/requiresShipping mismatch")
    if not live["price"] or not live["compareAtPrice"]:
        raise SystemExit("ERROR: missing price/compareAtPrice")
PY

python3 - "$VERIFY_JSON" "$SIZE_CHART" "$OUT_LISTING" "$OUT_CSV" "$TITLE" "$SEO_TITLE" "$SEO_DESC" "$CHILD_PRICE" "$CHILD_COMPARE" "$MOTHER_PRICE" "$MOTHER_COMPARE" "$VENDOR_URL" "$DESIGNS_TO_LIST" "$VENDOR_HISTORY_TITLE" "$PRINT_NAME" "$HANDLE" <<'PY'
import csv
import json
import sys

verify_path, size_chart_json, out_listing, out_csv, title, seo_title, seo_desc, child_price, child_compare, mother_price, mother_compare, vendor_url, designs_to_list, vendor_history_title, print_name, handle = sys.argv[1:]
verify = json.load(open(verify_path))
product = verify["data"]["product"]
chart = json.loads(size_chart_json)
collections = [node["title"] for node in product["collections"]["nodes"]]
media_nodes = product["media"]["nodes"]
image_url = ""
if media_nodes:
    for node in media_nodes:
        if node.get("mediaContentType") == "IMAGE":
            image_url = (((node or {}).get("image") or {}).get("url")) or ""
            if image_url:
                break

size_lines = []
for row in chart:
    price = child_price if row["audience"] == "child" else mother_price
    size_lines.append(
        {
            "vendor": row["vendor_label"],
            "picker": row["picker_label"],
            "sku": f"DLM-VCF-{row['sku_suffix']}-CREAM",
            "price": price,
            "gid": row["shopify_size_gid"],
        }
    )

written_metafields = [
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
    "global.description_tag",
]
skipped_metafields = [
    ("shopify.clothing-features", "Skipped because the store's current standard-catalog options do not honestly fit a light summer gauze pajama set."),
    ("shopify.sleeve-length-type", "Skipped because store rules say to omit sleeve-length-type for Pajamas."),
    ("shopify.neckline", "Skipped because neckline metafield is reserved for Dresses/Tops, not Pajamas."),
    ("shopify.dress-occasion", "Skipped because this is a Pajamas listing, not a Dress."),
    ("shopify.dress-style", "Skipped because this is a Pajamas listing, not a Dress."),
    ("shopify.skirt-dress-length-type", "Skipped because this is a Pajamas listing, not a Dress."),
]

with open(out_listing, "w", encoding="utf-8") as f:
    f.write(f"# {title}\n\n")
    f.write(f"- **Admin URL:** https://admin.shopify.com/store/dresslikemommy/products/{product['id'].split('/')[-1]}\n")
    f.write(f"- **Live URL:** https://www.dresslikemommy.com/products/{product['handle']}\n")
    f.write(f"- **Vendor URL:** {vendor_url}\n")
    f.write(f"- **Vendor browser title source:** {vendor_history_title}\n")
    f.write(f"- **Designs listed:** {designs_to_list}\n")
    f.write("- **Phase 1 source notes:** vendor title recovered from the user's existing signed-in Chrome profile history; size rows taken from the attached 尺码参数 screenshot after the raw 1688 terminal fetch hit anti-bot protection; product media attached from the user-supplied lifestyle image.\n")
    f.write("- **Fabric note:** `竹棉纱布` translated as bamboo-cotton gauze from the supplier title recovered from Chrome history.\n")
    f.write("- **Care note:** customer-facing care copy follows the store's standard bamboo-cotton gauze guidance because the live vendor tab metadata available from Chrome history/session records did not expose a recoverable care block.\n")
    f.write("- **Photo URL note:** recoverable supplier tab/session metadata did not expose a complete vendor image gallery URL list; the live listing uses the user-supplied product image attached during media upload.\n\n")
    f.write("## SIZE_CHART JSON\n\n```json\n")
    json.dump(chart, f, ensure_ascii=False, indent=2)
    f.write("\n```\n\n")
    f.write("## SIZE_CHART recap\n\n")
    f.write("| Vendor row | Picker label | SKU | Price | shopify.size GID |\n")
    f.write("|---|---|---|---|---|\n")
    for row in size_lines:
        f.write(f"| {row['vendor']} | {row['picker']} | {row['sku']} | ${row['price']} | {row['gid']} |\n")
    f.write("\n## Metafields written\n\n")
    for key in written_metafields:
        f.write(f"- `{key}`\n")
    f.write("\n## Metafields skipped\n\n")
    for key, reason in skipped_metafields:
        f.write(f"- `{key}` — {reason}\n")
    f.write("\n## Verification summary\n\n")
    f.write(f"- Title length: {len(title)}\n")
    f.write(f"- SEO title length: {len(seo_title)}\n")
    f.write(f"- SEO description length: {len(seo_desc)}\n")
    f.write(f"- Live variant count: {len(product['variants']['nodes'])}\n")
    f.write(f"- Smart collections: {', '.join(collections) if collections else 'none yet (Shopify reindex window)'}\n")
    f.write(f"- Published at: {product['publishedAt']}\n")
    f.write(f"- Media attached: {'yes' if image_url else 'no'}\n")

headers = [
    'Handle', 'Title', 'Body (HTML)', 'Vendor', 'Product Category', 'Type', 'Tags', 'Published',
    'Option1 Name', 'Option1 Value', 'Option1 Linked To', 'Option2 Name', 'Option2 Value', 'Option2 Linked To',
    'Option3 Name', 'Option3 Value', 'Option3 Linked To', 'Variant SKU', 'Variant Grams',
    'Variant Inventory Tracker', 'Variant Inventory Qty', 'Variant Inventory Policy',
    'Variant Fulfillment Service', 'Variant Price', 'Variant Compare At Price', 'Variant Requires Shipping',
    'Variant Taxable', 'Variant Barcode', 'Image Src', 'Image Position', 'Image Alt Text', 'Gift Card',
    'SEO Title', 'SEO Description', 'Google Shopping / Google Product Category', 'Google Shopping / Gender',
    'Google Shopping / Age Group', 'Google Shopping / MPN', 'Google Shopping / Condition',
    'Google Shopping / Custom Product', 'Google Shopping / Custom Label 0', 'Google Shopping / Custom Label 1',
    'Google Shopping / Custom Label 2', 'Google Shopping / Custom Label 3', 'Google Shopping / Custom Label 4',
    'custom.category1 (single_line_text_field)', 'custom.subcategory (single_line_text_field)',
    'custom.subcategory2 (single_line_text_field)', 'custom.pattern (single_line_text_field)',
    'custom.style (single_line_text_field)', 'custom.type (single_line_text_field)', 'Variant Image',
    'Variant Weight Unit', 'Variant Tax Code', 'Cost per item', 'Included / United States',
    'Price / United States', 'Compare At Price / United States', 'Included / International',
    'Price / International', 'Compare At Price / International', 'Status', 'Smart Collection',
    'Manual Collection', 'Color (product.metafields.shopify.color-pattern)',
    'Age Group (product.metafields.shopify.age-group)', 'Fabric (product.metafields.shopify.fabric)',
    'Size (product.metafields.shopify.size)', 'Target Gender (product.metafields.shopify.target-gender)',
    'Region (excluded)', 'SKU', 'Status (variant)', 'Customs Information', 'Shipping', 'Image Position 2'
]

size_gid_value = "; ".join(row["shopify_size_gid"] for row in chart)
tags_csv = ", ".join(product["tags"])
pattern_value = "Ladybug Dots wildflower print on pale blue bamboo-cotton gauze"
rows = []
for idx, row in enumerate(chart, start=1):
    variant_sku = f"DLM-VCF-{row['sku_suffix']}-CREAM"
    price = child_price if row["audience"] == "child" else mother_price
    compare = child_compare if row["audience"] == "child" else mother_compare
    base = {h: "" for h in headers}
    base['Handle'] = handle
    base['Option1 Name'] = 'Size'
    base['Option1 Value'] = row['picker_label']
    base['Option2 Name'] = 'Color'
    base['Option2 Value'] = print_name
    base['Variant SKU'] = variant_sku
    base['Variant Grams'] = '0'
    base['Variant Inventory Tracker'] = 'shopify'
    base['Variant Inventory Qty'] = '0'
    base['Variant Inventory Policy'] = 'deny'
    base['Variant Fulfillment Service'] = 'manual'
    base['Variant Price'] = price
    base['Variant Compare At Price'] = compare
    base['Variant Requires Shipping'] = 'TRUE'
    base['Variant Taxable'] = 'TRUE'
    base['Gift Card'] = 'FALSE'
    base['Variant Weight Unit'] = 'oz'
    base['Status'] = 'active'
    base['SKU'] = variant_sku
    if idx == 1:
      base['Title'] = title
      base['Body (HTML)'] = product['descriptionHtml']
      base['Vendor'] = 'dresslikemommy.com'
      base['Product Category'] = 'Apparel & Accessories > Clothing > Sleepwear & Loungewear > Pajamas'
      base['Type'] = 'Matching Family Pajamas'
      base['Tags'] = tags_csv
      base['Published'] = 'TRUE'
      base['Image Src'] = image_url
      base['Image Position'] = '1' if image_url else ''
      base['Image Alt Text'] = media_nodes[0]['alt'] if media_nodes else ''
      base['SEO Title'] = seo_title
      base['SEO Description'] = seo_desc
      base['Google Shopping / Google Product Category'] = GOOGLE_PRODUCT_CATEGORY = 'Apparel & Accessories > Clothing > Sleepwear & Loungewear > Pajamas'
      base['Google Shopping / Gender'] = 'female'
      base['Google Shopping / Age Group'] = 'adult'
      base['Google Shopping / Condition'] = 'new'
      base['Google Shopping / Custom Product'] = 'FALSE'
      base['Google Shopping / Custom Label 0'] = 'Mommy and Me'
      base['Google Shopping / Custom Label 1'] = 'Ladybug Dots'
      base['Google Shopping / Custom Label 2'] = 'Summer'
      base['Google Shopping / Custom Label 3'] = 'Short-Sleeve Set'
      base['Google Shopping / Custom Label 4'] = 'Family Matching'
      base['custom.category1 (single_line_text_field)'] = 'Mommy and Me'
      base['custom.subcategory (single_line_text_field)'] = 'Pajamas'
      base['custom.subcategory2 (single_line_text_field)'] = 'Summer Pajamas'
      base['custom.pattern (single_line_text_field)'] = pattern_value
      base['custom.style (single_line_text_field)'] = 'Matching Family Set'
      base['custom.type (single_line_text_field)'] = 'Two-Piece Pajama Set'
      base['Variant Image'] = image_url
      base['Price / United States'] = price
      base['Compare At Price / United States'] = compare
      base['Price / International'] = price
      base['Compare At Price / International'] = compare
      base['Color (product.metafields.shopify.color-pattern)'] = "; ".join([
          "gid://shopify/Metaobject/69639766113",
          "gid://shopify/Metaobject/69622104161",
          "gid://shopify/Metaobject/70220546145",
          "gid://shopify/Metaobject/129971519585",
          "gid://shopify/Metaobject/130231140449",
      ])
      base['Age Group (product.metafields.shopify.age-group)'] = "; ".join([
          "gid://shopify/Metaobject/128116523105",
          "gid://shopify/Metaobject/128116490337",
      ])
      base['Fabric (product.metafields.shopify.fabric)'] = "gid://shopify/Metaobject/69622399073"
      base['Size (product.metafields.shopify.size)'] = size_gid_value
      base['Target Gender (product.metafields.shopify.target-gender)'] = "gid://shopify/Metaobject/129971617889"
    rows.append(base)

with open(out_csv, "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    writer.writerows(rows)
PY

echo
echo "=== SUMMARY ==="
echo "Admin URL:   ${ADMIN_URL_BASE}/${ADMIN_NUM_ID}"
echo "Live URL:    ${LIVE_URL_BASE}/${HANDLE}"
echo "Listing MD:  ${OUT_LISTING}"
echo "CSV:         ${OUT_CSV}"
echo "Verify JSON: ${VERIFY_JSON}"
