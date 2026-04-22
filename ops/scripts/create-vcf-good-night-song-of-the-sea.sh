#!/usr/bin/env bash
# Create "Good Night Song of the Sea Mommy and Me Pajamas" on dresslikemommy.com via Admin API
# Run: bash ops/scripts/create-vcf-good-night-song-of-the-sea.sh
set -euo pipefail

ENV_FILE="${SHOPIFY_ENV_FILE:-${HOME}/.config/dresslikemommy/shopify-admin.env}"
if [ ! -f "$ENV_FILE" ]; then
  # Sandbox fallback: cowork mount
  for CANDIDATE in \
    "/sessions/kind-laughing-cerf/mnt/.config--dresslikemommy/shopify-admin.env" \
    "/Users/fsuels/.config/dresslikemommy/shopify-admin.env"; do
    [ -f "$CANDIDATE" ] && ENV_FILE="$CANDIDATE" && break
  done
fi
# shellcheck disable=SC1090
source "$ENV_FILE"

: "${SHOPIFY_STORE_DOMAIN:?}"; : "${SHOPIFY_ADMIN_ACCESS_TOKEN:?}"
API="https://${SHOPIFY_STORE_DOMAIN}/admin/api/2025-01/graphql.json"
AUTH=( -H "X-Shopify-Access-Token: ${SHOPIFY_ADMIN_ACCESS_TOKEN}" -H "Content-Type: application/json" )

gql() {
  local query="$1" vars="${2:-{\}}"
  jq -n --arg q "$query" --argjson v "$vars" '{query:$q, variables:$v}' \
    | curl -sS "${AUTH[@]}" -X POST -d @- "$API"
}

TITLE="Good Night Song of the Sea Mommy and Me Pajamas — Short-Sleeve Set"
HANDLE="good-night-song-of-the-sea-mommy-and-me-pajamas"
SEO_TITLE="Good Night Song of the Sea Mommy and Me Pajamas | Set"
SEO_DESC="Match your mini in our Good Night Song of the Sea mommy-and-me cotton-gauze pajamas — short-sleeve top + shorts, sizes 2Y–10Y & S–XL. Shop the set."

BODY_HTML=$(cat <<'EOF'
<ul>
  <li><strong>Breathable cotton-gauze weave:</strong> Light, airy double-gauze with a soft hand-feel that stays cool on warm summer nights and is gentle against little cheeks.</li>
  <li><strong>Make every moment match:</strong> Coordinating mother and daughter sets made for brunch, birthdays, holiday cards, and cozy family bonding — effortless matching, photo-ready in seconds.</li>
  <li><strong>Good Night Song of the Sea print:</strong> A dreamy watercolor ocean of whales, sea turtles, jellyfish, mermaids, stingrays, and coral on a soft cream ground — picture-perfect and quietly whimsical.</li>
  <li><strong>Classic design details:</strong> Notched collar, full button-down front, contrast dusty-blue piping along the placket, cuffs, and hem, and pull-on elastic-waist shorts for easy movement.</li>
  <li><strong>Easy care &amp; breathable:</strong> Machine-wash cold, tumble dry low. The open gauze weave keeps airflow high and wrinkles low.</li>
  <li><strong>Full family size range:</strong> Girls 2–10 Years and Mothers S–XL so the whole family can twin.</li>
</ul>
<p>&nbsp;</p>
<h3>Size Chart</h3>
<table id="size-chart">
  <thead>
    <tr>
      <th>Size</th>
      <th>Age</th>
      <th>Recommended Weight (kg/lbs)</th>
      <th>Recommended Height (cm/in)</th>
      <th>Chest/Bust (cm/in)</th>
      <th>Sleeve Length (cm/in)</th>
      <th>Pant/Short Length (cm/in)</th>
      <th>Hip (cm/in)</th>
      <th>Garment Length (cm/in)</th>
    </tr>
  </thead>
  <tbody>
    <!-- Children Sizes -->
    <tr><td>Child 2 Years</td><td>2</td><td>11–13 kg / 24–29 lbs</td><td>85–95 cm / 33–37 in</td><td>68 cm / 26.8 in</td><td>16 cm / 6.3 in</td><td>26 cm / 10.2 in</td><td>70 cm / 27.6 in</td><td>38 cm / 15.0 in</td></tr>
    <tr><td>Child 3 Years</td><td>3</td><td>13–16 kg / 29–35 lbs</td><td>95–105 cm / 37–41 in</td><td>72 cm / 28.3 in</td><td>17 cm / 6.7 in</td><td>28 cm / 11.0 in</td><td>74 cm / 29.1 in</td><td>41 cm / 16.1 in</td></tr>
    <tr><td>Child 4 Years</td><td>4</td><td>16–19 kg / 35–42 lbs</td><td>105–115 cm / 41–45 in</td><td>76 cm / 29.9 in</td><td>18 cm / 7.1 in</td><td>30 cm / 11.8 in</td><td>78 cm / 30.7 in</td><td>44 cm / 17.3 in</td></tr>
    <tr><td>Child 5 Years</td><td>5</td><td>19–22 kg / 42–49 lbs</td><td>115–125 cm / 45–49 in</td><td>80 cm / 31.5 in</td><td>19 cm / 7.5 in</td><td>33 cm / 13.0 in</td><td>83 cm / 32.7 in</td><td>47 cm / 18.5 in</td></tr>
    <tr><td>Child 6-7 Years</td><td>6–7</td><td>22–27 kg / 49–60 lbs</td><td>125–135 cm / 49–53 in</td><td>84 cm / 33.1 in</td><td>20 cm / 7.9 in</td><td>35.5 cm / 14.0 in</td><td>87 cm / 34.3 in</td><td>50 cm / 19.7 in</td></tr>
    <tr><td>Child 8 Years</td><td>8</td><td>27–33 kg / 60–73 lbs</td><td>135–145 cm / 53–57 in</td><td>88 cm / 34.6 in</td><td>21 cm / 8.3 in</td><td>38 cm / 15.0 in</td><td>91 cm / 35.8 in</td><td>53 cm / 20.9 in</td></tr>
    <tr><td>Child 9-10 Years</td><td>9–10</td><td>33–40 kg / 73–88 lbs</td><td>145–155 cm / 57–61 in</td><td>92 cm / 36.2 in</td><td>22 cm / 8.7 in</td><td>40.5 cm / 15.9 in</td><td>95 cm / 37.4 in</td><td>56 cm / 22.0 in</td></tr>
    <!-- Adult Sizes -->
    <tr><td>Mother S</td><td>—</td><td>45–52 kg / 99–115 lbs</td><td>155–160 cm / 61–63 in</td><td>102 cm / 40.2 in</td><td>22 cm / 8.7 in</td><td>40 cm / 15.7 in</td><td>106 cm / 41.7 in</td><td>58 cm / 22.8 in</td></tr>
    <tr><td>Mother M</td><td>—</td><td>52–60 kg / 115–132 lbs</td><td>160–165 cm / 63–65 in</td><td>106 cm / 41.7 in</td><td>23 cm / 9.1 in</td><td>41 cm / 16.1 in</td><td>110 cm / 43.3 in</td><td>60 cm / 23.6 in</td></tr>
    <tr><td>Mother L</td><td>—</td><td>60–68 kg / 132–150 lbs</td><td>165–170 cm / 65–67 in</td><td>110 cm / 43.3 in</td><td>24 cm / 9.4 in</td><td>42.5 cm / 16.7 in</td><td>114 cm / 44.9 in</td><td>63 cm / 24.8 in</td></tr>
    <tr><td>Mother XL</td><td>—</td><td>68–75 kg / 150–165 lbs</td><td>170–175 cm / 67–69 in</td><td>114 cm / 44.9 in</td><td>25 cm / 9.8 in</td><td>44 cm / 17.3 in</td><td>118 cm / 46.5 in</td><td>65 cm / 25.6 in</td></tr>
  </tbody>
</table>
<p>Our Good Night Song of the Sea mommy-and-me pajama set turns bedtime into a drifting ocean lullaby. The cream cotton-gauze is painted with watercolor whales, sea turtles, jellyfish, mermaids, stingrays, and swaying coral, finished with soft dusty-blue piping that frames the notched collar, cuffs, and hem. It is the kind of print that belongs in a seaside cottage reading nook — gentle, nostalgic, and quietly whimsical.</p>
<p>Wear it for slow Sunday brunches, summer sleepovers, beach-house mornings, birthday pancakes, and those holiday-card mornings when the whole family needs to look picture-perfect without trying. The button-down top and elastic-waist shorts move easily from pillow fights to pancake-making, and the full mother-and-daughter size run means nobody gets left out of the twinning moment.</p>
<h3>Key Features:</h3>
<ul>
  <li><strong>Coordinated mother &amp; daughter fit:</strong> Identical under-the-sea print in adult and child cuts so every family photo matches effortlessly.</li>
  <li><strong>Breathable cotton-gauze weave:</strong> Lightweight and airy for warm-weather sleep and summer travel.</li>
  <li><strong>Button-down top:</strong> Classic notched collar, contrast dusty-blue piping, and real buttons down the front.</li>
  <li><strong>Pull-on shorts:</strong> Soft elastic waistband for easy on-and-off and all-night comfort.</li>
  <li><strong>Inclusive sizing:</strong> Girls 2–10 Years and Mothers S–XL — add both to cart to complete the set.</li>
</ul>
<p>Add the mother size and the matching children's size to your cart to make every moment match — bedtime, brunch, and every snapshot in between.</p>
EOF
)

TAGS='Mommy and Me, Pajamas, Matching Family Pajamas, Short Sleeve Pajamas, Summer, Cream, Ivory, Blue, Navy, Sea Print, Ocean Print, Whale Print, Jellyfish Print, Mermaid Print, Under the Sea, Nautical, Storybook, Whimsical, Good Night Song of the Sea, Child 2-3yr, Child 4-5yr, Child 6-8yr, Child 9-10yr, Mother S, Mother M, Mother L, Mother XL, https://detail.1688.com/offer/900601808231.html'

########################################
# 5a: productCreate
########################################
echo "==> 5a productCreate"
VARS=$(jq -n --arg t "$TITLE" --arg h "$HANDLE" --arg b "$BODY_HTML" \
  --arg st "$SEO_TITLE" --arg sd "$SEO_DESC" --arg tg "$TAGS" '
  {product:{
     title:$t, handle:$h, descriptionHtml:$b, vendor:"dresslikemommy.com",
     productType:"Matching Family Pajamas",
     tags:($tg|split(", ")),
     productOptions:[
       {name:"Size", values:[
         {name:"Child 2 Years"},{name:"Child 3 Years"},{name:"Child 4 Years"},
         {name:"Child 5 Years"},{name:"Child 6-7 Years"},{name:"Child 8 Years"},
         {name:"Child 9-10 Years"},{name:"Mother S"},{name:"Mother M"},
         {name:"Mother L"},{name:"Mother XL"}
       ]},
       {name:"Color", values:[{name:"Good Night Song of the Sea"}]}
     ],
     seo:{title:$st, description:$sd},
     status:"ACTIVE",
     category:"gid://shopify/TaxonomyCategory/aa-1-17-4"
  }}')
RESP=$(gql 'mutation($product: ProductCreateInput!){productCreate(product:$product){product{id handle onlineStoreUrl} userErrors{field message}}}' "$VARS")
echo "$RESP" | jq .
PID=$(echo "$RESP" | jq -r '.data.productCreate.product.id')
[ -z "$PID" ] || [ "$PID" = "null" ] && { echo "productCreate failed"; exit 1; }
echo "PID=$PID"

########################################
# 5b: productVariantsBulkCreate
########################################
echo "==> 5b productVariantsBulkCreate"
VARIANTS=$(jq -n '[
 {size:"Child 2 Years",    sku:"DLM-VCF-KID2Y-CREAM",   price:"31.99",cap:"40.24"},
 {size:"Child 3 Years",    sku:"DLM-VCF-KID3Y-CREAM",   price:"31.99",cap:"40.24"},
 {size:"Child 4 Years",    sku:"DLM-VCF-KID4Y-CREAM",   price:"31.99",cap:"40.24"},
 {size:"Child 5 Years",    sku:"DLM-VCF-KID5Y-CREAM",   price:"31.99",cap:"40.24"},
 {size:"Child 6-7 Years",  sku:"DLM-VCF-KID67Y-CREAM",  price:"31.99",cap:"40.24"},
 {size:"Child 8 Years",    sku:"DLM-VCF-KID8Y-CREAM",   price:"31.99",cap:"40.24"},
 {size:"Child 9-10 Years", sku:"DLM-VCF-KID910Y-CREAM", price:"31.99",cap:"40.24"},
 {size:"Mother S",         sku:"DLM-VCF-MOMS-CREAM",    price:"34.99",cap:"45.99"},
 {size:"Mother M",         sku:"DLM-VCF-MOMM-CREAM",    price:"34.99",cap:"45.99"},
 {size:"Mother L",         sku:"DLM-VCF-MOML-CREAM",    price:"34.99",cap:"45.99"},
 {size:"Mother XL",        sku:"DLM-VCF-MOMXL-CREAM",   price:"34.99",cap:"45.99"}
] | map({
  price:.price, compareAtPrice:.cap, inventoryPolicy:"DENY",
  inventoryItem:{sku:.sku, tracked:true, requiresShipping:true},
  optionValues:[{optionName:"Size",name:.size},{optionName:"Color",name:"Good Night Song of the Sea"}]
})')
VARS=$(jq -n --arg id "$PID" --argjson v "$VARIANTS" \
  '{productId:$id, strategy:"REMOVE_STANDALONE_VARIANT", variants:$v}')
RESP=$(gql 'mutation($productId:ID!,$strategy:ProductVariantsBulkCreateStrategy,$variants:[ProductVariantsBulkInput!]!){productVariantsBulkCreate(productId:$productId,strategy:$strategy,variants:$variants){productVariants{id sku title price compareAtPrice} userErrors{field message}}}' "$VARS")
echo "$RESP" | jq '.data.productVariantsBulkCreate.userErrors, (.data.productVariantsBulkCreate.productVariants|length)'

########################################
# 5c: metafieldsSet (batch)
########################################
echo "==> 5c metafieldsSet"
MF=$(jq -n --arg id "$PID" '
[
 {ownerId:$id,namespace:"custom",key:"category1",type:"single_line_text_field",value:"Mommy and Me"},
 {ownerId:$id,namespace:"custom",key:"subcategory",type:"single_line_text_field",value:"Pajamas"},
 {ownerId:$id,namespace:"custom",key:"subcategory2",type:"single_line_text_field",value:"Summer Pajamas"},
 {ownerId:$id,namespace:"custom",key:"pattern",type:"single_line_text_field",value:"Good Night Song of the Sea watercolor ocean print with whales, turtles, jellyfish, mermaids"},
 {ownerId:$id,namespace:"custom",key:"style",type:"single_line_text_field",value:"Matching Family Set"},
 {ownerId:$id,namespace:"custom",key:"type",type:"single_line_text_field",value:"Two-Piece Pajama Set"},
 {ownerId:$id,namespace:"mm-google-shopping",key:"custom_product",type:"boolean",value:"false"},
 {ownerId:$id,namespace:"mm-google-shopping",key:"gender",type:"single_line_text_field",value:"female"},
 {ownerId:$id,namespace:"mm-google-shopping",key:"age_group",type:"single_line_text_field",value:"adult"},
 {ownerId:$id,namespace:"mm-google-shopping",key:"condition",type:"single_line_text_field",value:"new"},
 {ownerId:$id,namespace:"mm-google-shopping",key:"custom_label_0",type:"single_line_text_field",value:"Mommy and Me"},
 {ownerId:$id,namespace:"mm-google-shopping",key:"custom_label_1",type:"single_line_text_field",value:"Under the Sea"},
 {ownerId:$id,namespace:"mm-google-shopping",key:"custom_label_2",type:"single_line_text_field",value:"Summer"},
 {ownerId:$id,namespace:"mm-google-shopping",key:"custom_label_3",type:"single_line_text_field",value:"Short Sleeve"},
 {ownerId:$id,namespace:"mm-google-shopping",key:"custom_label_4",type:"single_line_text_field",value:"Family Matching"},
 {ownerId:$id,namespace:"shopify",key:"age-group",type:"list.single_line_text_field",value:"[\"kids\",\"adults\"]"},
 {ownerId:$id,namespace:"shopify",key:"clothing-features",type:"list.single_line_text_field",value:"[\"Breathable\",\"Lightweight\",\"Button-front\"]"},
 {ownerId:$id,namespace:"shopify",key:"color-pattern",type:"list.single_line_text_field",value:"[\"Cream\",\"Ivory\",\"Blue\",\"Navy\",\"Multicolor\"]"},
 {ownerId:$id,namespace:"shopify",key:"fabric",type:"single_line_text_field",value:"Cotton Blend"},
 {ownerId:$id,namespace:"shopify",key:"size",type:"list.single_line_text_field",value:"[\"Child 2 Years\",\"Child 3 Years\",\"Child 4 Years\",\"Child 5 Years\",\"Child 6-7 Years\",\"Child 8 Years\",\"Child 9-10 Years\",\"Mother S\",\"Mother M\",\"Mother L\",\"Mother XL\"]"},
 {ownerId:$id,namespace:"shopify",key:"sleeve-length-type",type:"single_line_text_field",value:"Short Sleeve"},
 {ownerId:$id,namespace:"shopify",key:"neckline",type:"single_line_text_field",value:"Notched Collar"},
 {ownerId:$id,namespace:"global",key:"title_tag",type:"single_line_text_field",value:"Good Night Song of the Sea Mommy and Me Pajamas | Set"},
 {ownerId:$id,namespace:"global",key:"description_tag",type:"single_line_text_field",value:"Match your mini in our Good Night Song of the Sea mommy-and-me cotton-gauze pajamas — short-sleeve top + shorts, sizes 2Y–10Y & S–XL. Shop the set."}
]')
VARS=$(jq -n --argjson m "$MF" '{metafields:$m}')
RESP=$(gql 'mutation($metafields:[MetafieldsSetInput!]!){metafieldsSet(metafields:$metafields){metafields{id namespace key} userErrors{field message}}}' "$VARS")
echo "$RESP" | jq '.data.metafieldsSet.userErrors, (.data.metafieldsSet.metafields|length)'

########################################
# 5d: publishablePublish
########################################
echo "==> 5d publishablePublish"
for PUB in \
  "gid://shopify/Publication/55169925" \
  "gid://shopify/Publication/21969633377" \
  "gid://shopify/Publication/29172400225" \
  "gid://shopify/Publication/76582879329" \
  "gid://shopify/Publication/76604768353"
do
  VARS=$(jq -n --arg id "$PID" --arg pub "$PUB" \
    '{id:$id, input:[{publicationId:$pub}]}')
  RESP=$(gql 'mutation($id:ID!,$input:[PublicationInput!]!){publishablePublish(id:$id,input:$input){userErrors{field message}}}' "$VARS")
  echo "  -> $PUB"; echo "$RESP" | jq '.data.publishablePublish.userErrors'
done

########################################
# 6: verify
########################################
echo "==> 6 verify"
VARS=$(jq -n --arg id "$PID" '{id:$id}')
gql 'query($id:ID!){product(id:$id){id title handle onlineStoreUrl status publishedAt seo{title description} category{id name} options{name values} variants(first:25){nodes{sku title price compareAtPrice inventoryPolicy inventoryItem{tracked requiresShipping}}} metafields(first:50){nodes{namespace key type value}} collections(first:20){nodes{title handle}}}}' "$VARS" \
  | tee /tmp/verify.json | jq '.data.product | {title, handle, status, publishedAt, onlineStoreUrl, cat:.category.name, variants:.variants.nodes|length, metafields:.metafields.nodes|length, collections:[.collections.nodes[].handle]}'

echo "DONE. admin URL: https://admin.shopify.com/store/dresslikemommy/products/$(echo $PID | sed 's|gid://shopify/Product/||')"
