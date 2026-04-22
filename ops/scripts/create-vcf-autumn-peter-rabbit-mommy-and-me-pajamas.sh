#!/usr/bin/env bash
# Dress Like Mommy — Autumn Peter Rabbit Mommy and Me Pajamas
# Runner: derive EVERYTHING from SIZE_CHART, preflight guard, create,
# variants, metafields, publish, verify.
set -euo pipefail

# ─────────────────────────────────────────────────────────────────────────────
# 0. Creds
# ─────────────────────────────────────────────────────────────────────────────
if [[ -f "/Users/fsuels/.config/dresslikemommy/shopify-admin.env" ]]; then
  # shellcheck disable=SC1091
  source "/Users/fsuels/.config/dresslikemommy/shopify-admin.env"
fi

: "${SHOPIFY_STORE_DOMAIN:=dresslikemommy-com.myshopify.com}"

if [[ -z "${SHOPIFY_ADMIN_ACCESS_TOKEN:-}" ]]; then
  echo "SHOPIFY_ADMIN_ACCESS_TOKEN is not set. Load ~/.config/dresslikemommy/shopify-admin.env before running this script." >&2
  exit 1
fi
API="https://${SHOPIFY_STORE_DOMAIN}/admin/api/2025-01/graphql.json"
HDR_TOKEN="X-Shopify-Access-Token: ${SHOPIFY_ADMIN_ACCESS_TOKEN}"
HDR_CT="Content-Type: application/json"

gql() {
  curl -sS -X POST "$API" -H "$HDR_TOKEN" -H "$HDR_CT" -d "$1"
}

# ─────────────────────────────────────────────────────────────────────────────
# 1. Constants
# ─────────────────────────────────────────────────────────────────────────────
SHORTCODE="VCF"
COLOR_TOKEN="CREAM"
COLOR_NAME="Autumn Peter Rabbit"
HANDLE="autumn-peter-rabbit-mommy-and-me-pajamas"
TITLE="Autumn Peter Rabbit Mommy and Me Pajamas — Short-Sleeve Set"
SEO_TITLE="Peter Rabbit Mommy & Me Pajamas | Dress Like Mommy"
SEO_DESC="Shop our Autumn Peter Rabbit matching mommy-and-me pajamas — soft cotton Short-Sleeve Set for mom + daughter. Kids 2Y–10Y, Mom S–XL."
VENDOR="dresslikemommy.com"
PRODUCT_TYPE="Matching Family Pajamas"
TAXONOMY_GID="gid://shopify/TaxonomyCategory/aa-1-17-4"
CHILD_PRICE="35.99"
MOTHER_PRICE="39.99"
CHILD_CMP="40.24"   # 35.99 × 1.15 → 41.39 → round_up .99 → 41.99? per rule table 35.99 → 40.24 per supplied table
MOTHER_CMP="45.99"  # 39.99 × 1.15 → 45.99 per supplied table
VENDOR_URL="https://detail.1688.com/offer/828526529351.html"
SEASON="Fall"

# Publication GIDs
PUB_ONLINE="gid://shopify/Publication/55169925"
PUB_GOOGLE="gid://shopify/Publication/21969633377"
PUB_META="gid://shopify/Publication/29172400225"
PUB_PINT="gid://shopify/Publication/76582879329"
PUB_TT="gid://shopify/Publication/76604768353"

# Metaobject GIDs (verified against store)
GID_AGE_KIDS="gid://shopify/Metaobject/128116523105"
GID_AGE_ADULTS="gid://shopify/Metaobject/128116490337"
GID_FABRIC_COTTON="gid://shopify/Metaobject/69622399073"
GID_GENDER_FEMALE="gid://shopify/Metaobject/129971617889"
GID_COLOR_BEIGE="gid://shopify/Metaobject/69641928801"
GID_COLOR_WHITE="gid://shopify/Metaobject/69639733345"
GID_COLOR_BROWN="" # no brown seen; fallback multicolor
GID_COLOR_MULTI="gid://shopify/Metaobject/130231140449"
GID_COLOR_FLORAL="gid://shopify/Metaobject/129971519585"

# Size catalog GIDs
declare -A SIZE_GID=(
  ["Child 2 Years"]="gid://shopify/Metaobject/129972863073"
  ["Child 3 Years"]="gid://shopify/Metaobject/129972895841"
  ["Child 4 Years"]="gid://shopify/Metaobject/129972928609"
  ["Child 5 Years"]="gid://shopify/Metaobject/129972961377"
  ["Child 6-7 Years"]="gid://shopify/Metaobject/139840323681"
  ["Child 8 Years"]="gid://shopify/Metaobject/139840356449"
  ["Child 9-10 Years"]="gid://shopify/Metaobject/139840389217"
  ["Mother S"]="gid://shopify/Metaobject/129975255137"
  ["Mother M"]="gid://shopify/Metaobject/129975222369"
  ["Mother L"]="gid://shopify/Metaobject/129975189601"
  ["Mother XL"]="gid://shopify/Metaobject/129975287905"
)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CHART="$SCRIPT_DIR/size_chart.json"

# ─────────────────────────────────────────────────────────────────────────────
# 2. Preflight
# ─────────────────────────────────────────────────────────────────────────────
echo "── Preflight ──"
jq -e 'all(.[]; .audience and .vendor_label and .picker_label and .sku_suffix and .age and .weight and .height and .chest_cm and .hip_cm and .waist_cm and .length_cm)' "$CHART" >/dev/null || { echo "FAIL: missing required SIZE_CHART fields"; exit 1; }

ROW_COUNT=$(jq 'length' "$CHART")
UNIQ=$(jq '[.[].picker_label] | unique | length' "$CHART")
[[ "$ROW_COUNT" == "$UNIQ" ]] || { echo "FAIL: duplicate picker_label"; exit 1; }
[[ ${#TITLE} -le 70 ]] || { echo "FAIL: title > 70"; exit 1; }
[[ ${#SEO_TITLE} -le 60 ]] || { echo "FAIL: seo title > 60"; exit 1; }
[[ ${#SEO_DESC} -le 155 ]] || { echo "FAIL: seo desc > 155"; exit 1; }
echo "✓ Preflight OK — rows=$ROW_COUNT, title=${#TITLE}, seo_t=${#SEO_TITLE}, seo_d=${#SEO_DESC}"

# ─────────────────────────────────────────────────────────────────────────────
# 3. Derive Size picker values (chart order)
# ─────────────────────────────────────────────────────────────────────────────
SIZE_VALUES_JSON=$(jq '[.[].picker_label | {name:.}]' "$CHART")
echo "Size option values: $(jq -c . <<<"$SIZE_VALUES_JSON")"

# ─────────────────────────────────────────────────────────────────────────────
# 4. Build Body HTML (including 10-col size table)
# ─────────────────────────────────────────────────────────────────────────────
cm_to_in() { awk -v c="$1" 'BEGIN{printf "%.1f", c/2.54}'; }

# Build size-chart table rows using jq
ROWS_HTML=$(
  jq -r '
    def fmt_cm($x): ($x|tostring) + " cm / " + (($x/2.54)|.*10|round|./10|tostring) + " in";
    .[]
    | @html "<tr><td>\(.picker_label)</td><td>\(.age)</td><td>\(.weight)</td><td>\(.height)</td><td>\(fmt_cm(.chest_cm))</td><td>\(fmt_cm(.sleeve_cm))</td><td>\(fmt_cm(.pant_cm))</td><td>\(fmt_cm(.hip_cm))</td><td>\(fmt_cm(.waist_cm))</td><td>\(fmt_cm(.length_cm))</td></tr>"
  ' "$CHART"
)
# Inject audience section comments
FIRST_MOTHER_IDX=$(jq '[.[] | .audience] | index("mother")' "$CHART")
KID_ROWS=$(jq -r --argjson idx "$FIRST_MOTHER_IDX" '
  def fmt_cm($x): ($x|tostring) + " cm / " + (($x/2.54)|.*10|round|./10|tostring) + " in";
  .[0:$idx][]
  | "<tr><td>\(.picker_label)</td><td>\(.age)</td><td>\(.weight)</td><td>\(.height)</td><td>\(fmt_cm(.chest_cm))</td><td>\(fmt_cm(.sleeve_cm))</td><td>\(fmt_cm(.pant_cm))</td><td>\(fmt_cm(.hip_cm))</td><td>\(fmt_cm(.waist_cm))</td><td>\(fmt_cm(.length_cm))</td></tr>"
' "$CHART")
MOM_ROWS=$(jq -r --argjson idx "$FIRST_MOTHER_IDX" '
  def fmt_cm($x): ($x|tostring) + " cm / " + (($x/2.54)|.*10|round|./10|tostring) + " in";
  .[$idx:][]
  | "<tr><td>\(.picker_label)</td><td>\(.age)</td><td>\(.weight)</td><td>\(.height)</td><td>\(fmt_cm(.chest_cm))</td><td>\(fmt_cm(.sleeve_cm))</td><td>\(fmt_cm(.pant_cm))</td><td>\(fmt_cm(.hip_cm))</td><td>\(fmt_cm(.waist_cm))</td><td>\(fmt_cm(.length_cm))</td></tr>"
' "$CHART")

read -r -d '' BODY_HTML <<HTML || true
<ul>
  <li><strong>Fabric:</strong> Soft 4-layer cotton gauze (muslin) — breathable, naturally crinkled, and gets cozier with every wash.</li>
  <li><strong>Family story:</strong> Picture-perfect matching pajamas for mom and daughter — built for brunch, birthdays, and holiday cards.</li>
  <li><strong>Print:</strong> "Autumn Peter Rabbit" — watercolor bunnies, acorns, mushrooms, and autumn leaves on a warm cream base.</li>
  <li><strong>Design details:</strong> Notch collar, button-front top with contrast piping, chest pocket, elastic-waist pants.</li>
  <li><strong>Care:</strong> Machine wash cold on gentle, tumble dry low, no bleach, warm iron if needed.</li>
  <li><strong>Size range:</strong> Kids Child 2 Years to Child 9-10 Years; Mother S to Mother XL.</li>
</ul>

<h3>Size Chart</h3>
<table id="size-chart">
  <thead>
    <tr>
      <th>Size</th>
      <th>Age</th>
      <th>Weight</th>
      <th>Height</th>
      <th>Chest/Bust</th>
      <th>Sleeve</th>
      <th>Pant</th>
      <th>Hip</th>
      <th>Waist</th>
      <th>Garment Length</th>
    </tr>
  </thead>
  <tbody>
    <!-- Children Sizes -->
    ${KID_ROWS}
    <!-- Adult Sizes -->
    ${MOM_ROWS}
  </tbody>
</table>

<p>Welcome bunny season with our Autumn Peter Rabbit Mommy and Me Pajamas — a cozy two-piece set that turns bedtime and lazy mornings into a matching moment. Cut from lightweight, breathable 4-layer cotton gauze, the fabric softens with every wash so both mom and little one can curl up in something that feels as good as it looks. Warm autumn tones — cream, caramel, muted sage — let the watercolor bunnies, acorns, and mushrooms do all the talking.</p>

<p>Inspired by a woodland walk at golden hour, the print gathers up Peter Rabbit, his leafy friends, and little harvest vignettes into a story you and your daughter can wear together. Pair them for a photo-ready brunch, a weekend at the pumpkin patch, the annual family portrait, or a cozy night of storybooks and hot cocoa. These pajamas make every moment match — effortlessly.</p>

<h3>Key Features:</h3>
<ul>
  <li><strong>Breathable cotton gauze:</strong> 4-layer muslin weave keeps air moving and skin happy.</li>
  <li><strong>Elevated details:</strong> Notch collar, contrast piping, buttoned placket, and a chest pocket on every top.</li>
  <li><strong>Mom + mini matching:</strong> Identical print on both sizes for head-to-toe family twinning.</li>
  <li><strong>Everyday ease:</strong> Elastic-waist pants, relaxed fit, and a printed top that layers effortlessly.</li>
  <li><strong>Photo-ready neutrals:</strong> Cream palette styles with any home backdrop — Thanksgiving, birthdays, holiday cards.</li>
</ul>

<p>Slip into the softest matching moment of the season — grab your set and make this autumn one you'll want to frame.</p>
HTML

# ─────────────────────────────────────────────────────────────────────────────
# 5. Tags (include VENDOR_URL, mother-size tags only for rows in SIZE_CHART)
# ─────────────────────────────────────────────────────────────────────────────
TAGS_JSON=$(jq -cn --argjson chart "$(cat "$CHART")" --arg vendor_url "$VENDOR_URL" '
  def mom_size_tag(p): if p=="Mother S" then "Mom Size S"
    elif p=="Mother M" then "Mom Size M"
    elif p=="Mother L" then "Mom Size L"
    elif p=="Mother XL" then "Mom Size XL"
    elif p=="Mother One Size" then "Mom One Size"
    else null end;
  def kid_bucket(p): if p=="Child 2 Years" or p=="Child 3 Years" then "Child 2-3yr"
    elif p=="Child 4 Years" or p=="Child 5 Years" then "Child 4-5yr"
    elif p=="Child 6-7 Years" or p=="Child 8 Years" then "Child 6-8yr"
    elif p=="Child 9-10 Years" then "Child 9-10yr"
    else null end;
  ([
    "Mommy and Me", "Pajamas", "Matching Family Pajamas", "Short Sleeve Pajamas",
    "Fall", "Autumn", "Peter Rabbit", "Rabbit", "Bunny", "Woodland",
    "Cream", "Beige", "Floral",
    "Cotton Gauze", "Muslin",
    $vendor_url
  ] + [$chart[] | select(.audience=="child") | kid_bucket(.picker_label)]
    + [$chart[] | select(.audience=="mother") | mom_size_tag(.picker_label)])
  | map(select(. != null))
  | unique
')
echo "Tags: $TAGS_JSON"

# ─────────────────────────────────────────────────────────────────────────────
# 6. Create product
# ─────────────────────────────────────────────────────────────────────────────
echo "── productCreate ──"
CREATE_PAYLOAD=$(jq -nc \
  --arg title "$TITLE" \
  --arg handle "$HANDLE" \
  --arg body "$BODY_HTML" \
  --arg ptype "$PRODUCT_TYPE" \
  --arg vendor "$VENDOR" \
  --arg seoT "$SEO_TITLE" \
  --arg seoD "$SEO_DESC" \
  --arg color "$COLOR_NAME" \
  --arg tax "$TAXONOMY_GID" \
  --argjson sizeValues "$SIZE_VALUES_JSON" \
  --argjson tags "$TAGS_JSON" \
  '{
    query:"mutation productCreate($input: ProductInput!){ productCreate(input:$input){ product{ id handle title } userErrors{ field message }}}",
    variables:{input:{
      title:$title, handle:$handle, descriptionHtml:$body,
      productType:$ptype, vendor:$vendor, status:"ACTIVE",
      tags:$tags, category:$tax,
      seo:{title:$seoT, description:$seoD},
      productOptions:[
        {name:"Size", values:$sizeValues},
        {name:"Color", values:[{name:$color}]}
      ]
    }}
  }')

CREATE_RESP=$(gql "$CREATE_PAYLOAD")
echo "$CREATE_RESP" | jq '.data.productCreate.userErrors'
PRODUCT_ID=$(echo "$CREATE_RESP" | jq -r '.data.productCreate.product.id // empty')
[[ -n "$PRODUCT_ID" ]] || { echo "FAIL: productCreate"; echo "$CREATE_RESP" | jq .; exit 1; }
echo "✓ Created $PRODUCT_ID"

# ─────────────────────────────────────────────────────────────────────────────
# 7. Bulk-create variants
# ─────────────────────────────────────────────────────────────────────────────
echo "── productVariantsBulkCreate ──"
VARIANTS_JSON=$(jq -nc \
  --arg shortcode "$SHORTCODE" \
  --arg color_token "$COLOR_TOKEN" \
  --arg color_name "$COLOR_NAME" \
  --arg child_price "$CHILD_PRICE" \
  --arg mother_price "$MOTHER_PRICE" \
  --arg child_cmp "$CHILD_CMP" \
  --arg mother_cmp "$MOTHER_CMP" \
  --argjson chart "$(cat "$CHART")" '
  [$chart[] | {
    price: (if .audience=="child" then $child_price else $mother_price end),
    compareAtPrice: (if .audience=="child" then $child_cmp else $mother_cmp end),
    inventoryPolicy: "DENY",
    inventoryItem: { sku: ("DLM-" + $shortcode + "-" + .sku_suffix + "-" + $color_token), tracked: true, requiresShipping: true },
    optionValues: [
      { optionName: "Size", name: .picker_label },
      { optionName: "Color", name: $color_name }
    ]
  }]')

VCREATE_PAYLOAD=$(jq -nc --arg pid "$PRODUCT_ID" --argjson variants "$VARIANTS_JSON" '
  {
    query:"mutation varCreate($productId:ID!, $strategy:ProductVariantsBulkCreateStrategy, $variants:[ProductVariantsBulkInput!]!){ productVariantsBulkCreate(productId:$productId, strategy:$strategy, variants:$variants){ productVariants{ id sku title inventoryPolicy } userErrors{ field message }}}",
    variables:{ productId:$pid, strategy:"REMOVE_STANDALONE_VARIANT", variants:$variants }
  }')

VCREATE_RESP=$(gql "$VCREATE_PAYLOAD")
echo "$VCREATE_RESP" | jq '.data.productVariantsBulkCreate.userErrors'
VCOUNT=$(echo "$VCREATE_RESP" | jq '.data.productVariantsBulkCreate.productVariants | length')
echo "✓ Variants created: $VCOUNT"

# ─────────────────────────────────────────────────────────────────────────────
# 8. Metafields (single batch)
# ─────────────────────────────────────────────────────────────────────────────
echo "── metafieldsSet ──"

# Build shopify.size GID list from SIZE_CHART picker labels
SIZE_GIDS_JSON=$(jq -nc --argjson chart "$(cat "$CHART")" '
  def m(p): if p=="Child 2 Years" then "gid://shopify/Metaobject/129972863073"
    elif p=="Child 3 Years" then "gid://shopify/Metaobject/129972895841"
    elif p=="Child 4 Years" then "gid://shopify/Metaobject/129972928609"
    elif p=="Child 5 Years" then "gid://shopify/Metaobject/129972961377"
    elif p=="Child 6-7 Years" then "gid://shopify/Metaobject/139840323681"
    elif p=="Child 8 Years" then "gid://shopify/Metaobject/139840356449"
    elif p=="Child 9-10 Years" then "gid://shopify/Metaobject/139840389217"
    elif p=="Mother S" then "gid://shopify/Metaobject/129975255137"
    elif p=="Mother M" then "gid://shopify/Metaobject/129975222369"
    elif p=="Mother L" then "gid://shopify/Metaobject/129975189601"
    elif p=="Mother XL" then "gid://shopify/Metaobject/129975287905"
    else null end;
  [$chart[] | m(.picker_label)] | map(select(.!=null))')

COLOR_GIDS_JSON='["gid://shopify/Metaobject/69641928801","gid://shopify/Metaobject/129971519585","gid://shopify/Metaobject/130231140449"]'  # Beige, Floral, Multicolor
AGE_GIDS_JSON='["gid://shopify/Metaobject/128116523105","gid://shopify/Metaobject/128116490337"]'  # Kids, Adults
GENDER_GIDS_JSON='["gid://shopify/Metaobject/129971617889"]'  # Female
FABRIC_GIDS_JSON='["gid://shopify/Metaobject/69622399073"]'    # Cotton

MF_PAYLOAD=$(jq -nc \
  --arg pid "$PRODUCT_ID" \
  --arg season "$SEASON" \
  --arg seoT "$SEO_TITLE" \
  --arg seoD "$SEO_DESC" \
  --argjson size_gids "$SIZE_GIDS_JSON" \
  --argjson color_gids "$COLOR_GIDS_JSON" \
  --argjson age_gids "$AGE_GIDS_JSON" \
  --argjson gender_gids "$GENDER_GIDS_JSON" \
  --argjson fabric_gids "$FABRIC_GIDS_JSON" '
  def mf(ns;k;t;v): {ownerId:$pid, namespace:ns, key:k, type:t, value:v};
  {
    query:"mutation mfSet($mf:[MetafieldsSetInput!]!){ metafieldsSet(metafields:$mf){ userErrors{ field message } metafields{ id namespace key }}}",
    variables:{ mf:[
      mf("custom";"category1";"single_line_text_field";"Mommy and Me"),
      mf("custom";"subcategory";"single_line_text_field";"Pajamas"),
      mf("custom";"subcategory2";"single_line_text_field";($season + " Pajamas")),
      mf("custom";"pattern";"single_line_text_field";"Autumn Peter Rabbit"),
      mf("custom";"style";"single_line_text_field";"Matching Family Set"),
      mf("custom";"type";"single_line_text_field";"Two-Piece Pajama Set"),
      mf("mm-google-shopping";"custom_product";"boolean";"false"),
      mf("mm-google-shopping";"gender";"single_line_text_field";"female"),
      mf("mm-google-shopping";"age_group";"single_line_text_field";"adult"),
      mf("mm-google-shopping";"condition";"single_line_text_field";"new"),
      mf("mm-google-shopping";"custom_label_0";"single_line_text_field";"Mommy and Me"),
      mf("mm-google-shopping";"custom_label_1";"single_line_text_field";"Peter Rabbit"),
      mf("mm-google-shopping";"custom_label_2";"single_line_text_field";$season),
      mf("mm-google-shopping";"custom_label_3";"single_line_text_field";"Short-Sleeve Set"),
      mf("mm-google-shopping";"custom_label_4";"single_line_text_field";"Family Matching"),
      mf("shopify";"age-group";"list.metaobject_reference";($age_gids|tostring)),
      mf("shopify";"color-pattern";"list.metaobject_reference";($color_gids|tostring)),
      mf("shopify";"fabric";"list.metaobject_reference";($fabric_gids|tostring)),
      mf("shopify";"size";"list.metaobject_reference";($size_gids|tostring)),
      mf("shopify";"target-gender";"list.metaobject_reference";($gender_gids|tostring)),
      mf("global";"title_tag";"single_line_text_field";$seoT),
      mf("global";"description_tag";"single_line_text_field";$seoD)
    ]}
  }')

MF_RESP=$(gql "$MF_PAYLOAD")
echo "$MF_RESP" | jq '.data.metafieldsSet.userErrors'
MF_COUNT=$(echo "$MF_RESP" | jq '.data.metafieldsSet.metafields | length')
echo "✓ Metafields written: $MF_COUNT"

# ─────────────────────────────────────────────────────────────────────────────
# 9. Publish to channels
# ─────────────────────────────────────────────────────────────────────────────
echo "── publishablePublish ──"
PUB_PAYLOAD=$(jq -nc --arg pid "$PRODUCT_ID" \
  --arg p1 "$PUB_ONLINE" --arg p2 "$PUB_GOOGLE" --arg p3 "$PUB_META" --arg p4 "$PUB_PINT" --arg p5 "$PUB_TT" '
  {
    query:"mutation pub($id:ID!, $input:[PublicationInput!]!){ publishablePublish(id:$id, input:$input){ publishable{ availablePublicationsCount{ count } } userErrors{ field message }}}",
    variables:{ id:$pid, input:[
      {publicationId:$p1},{publicationId:$p2},{publicationId:$p3},{publicationId:$p4},{publicationId:$p5}
    ]}
  }')
PUB_RESP=$(gql "$PUB_PAYLOAD")
echo "$PUB_RESP" | jq '.data.publishablePublish.userErrors'

# ─────────────────────────────────────────────────────────────────────────────
# 10. Media (idempotent — only if uploads dir exists)
# ─────────────────────────────────────────────────────────────────────────────
UPLOAD_DIR="/Users/fsuels/Projects/dresslikemommy/uploads/${HANDLE}"
if [[ -d "$UPLOAD_DIR" ]] && compgen -G "$UPLOAD_DIR/*" >/dev/null; then
  echo "── media upload ── (found $UPLOAD_DIR)"
  echo "  (implemented as follow-up; uploads present)"
else
  echo "── media upload skipped — $UPLOAD_DIR missing; manual follow-up required"
fi

# ─────────────────────────────────────────────────────────────────────────────
# 11. Post-create verify
# ─────────────────────────────────────────────────────────────────────────────
echo "── verify ──"
VERIFY_PAYLOAD=$(jq -nc --arg pid "$PRODUCT_ID" '{
  query:"query($id:ID!){ product(id:$id){ id title handle publishedAt onlineStoreUrl descriptionHtml seo{ title description } tags variants(first:50){ edges { node { sku title price compareAtPrice inventoryPolicy inventoryItem { tracked requiresShipping }}}} metafields(first:50){ edges { node { namespace key type value }}}}}",
  variables:{id:$pid}
}')
VERIFY=$(gql "$VERIFY_PAYLOAD")

LIVE_SKUS=$(echo "$VERIFY" | jq -r '[.data.product.variants.edges[].node.sku] | sort | .[]')
DERIVED_SKUS=$(jq -r --arg s "$SHORTCODE" --arg c "$COLOR_TOKEN" '.[] | "DLM-" + $s + "-" + .sku_suffix + "-" + $c' "$CHART" | sort)
echo "Live SKUs:"
echo "$LIVE_SKUS"
echo "Derived SKUs:"
echo "$DERIVED_SKUS"
diff <(echo "$LIVE_SKUS") <(echo "$DERIVED_SKUS") && echo "✓ SKU match" || echo "✗ SKU mismatch"

LIVE_VCOUNT=$(echo "$VERIFY" | jq '.data.product.variants.edges | length')
[[ "$LIVE_VCOUNT" == "$ROW_COUNT" ]] && echo "✓ Variant count OK ($LIVE_VCOUNT)" || echo "✗ Variant count $LIVE_VCOUNT != $ROW_COUNT"

# Body HTML table check
DHTML=$(echo "$VERIFY" | jq -r '.data.product.descriptionHtml')
TR_COUNT=$(echo "$DHTML" | grep -o '<tr>' | wc -l)
TH_COUNT=$(echo "$DHTML" | grep -o '<th>' | wc -l)
echo "Body table: <tr>=$TR_COUNT (expect $((ROW_COUNT+1))), <th>=$TH_COUNT (expect 10)"

PUBAT=$(echo "$VERIFY" | jq -r '.data.product.publishedAt // empty')
URL=$(echo "$VERIFY" | jq -r '.data.product.onlineStoreUrl // empty')
echo "publishedAt: $PUBAT"
echo "onlineStoreUrl: $URL"

PID_NUM="${PRODUCT_ID##*/}"
echo ""
echo "Admin: https://admin.shopify.com/store/dresslikemommy/products/${PID_NUM}"
echo "Live : https://www.dresslikemommy.com/products/${HANDLE}"

# Save verify dump for recap
echo "$VERIFY" > "$SCRIPT_DIR/../listings/verify-${HANDLE}.json"
echo "Saved verify dump to ops/listings/verify-${HANDLE}.json"
