#!/usr/bin/env bash
# create-vcf-little-pear-pajamas.sh
# Ships "Little Pear Mommy and Me Pajamas — Short-Sleeve Set" to dresslikemommy.com.
# All variant-dependent fields are derived from SIZE_CHART (jq). Hand-maintained parallel lists are forbidden.
set -euo pipefail

# ---------- creds ----------
if [ -f "${HOME}/.config/dresslikemommy/shopify-admin.env" ]; then
  source "${HOME}/.config/dresslikemommy/shopify-admin.env"
fi
: "${SHOPIFY_STORE_DOMAIN:=dresslikemommy-com.myshopify.com}"
: "${SHOPIFY_ADMIN_ACCESS_TOKEN:?Set SHOPIFY_ADMIN_ACCESS_TOKEN}"
API="https://${SHOPIFY_STORE_DOMAIN}/admin/api/2025-01/graphql.json"
HDR_AUTH="X-Shopify-Access-Token: ${SHOPIFY_ADMIN_ACCESS_TOKEN}"
HDR_JSON="Content-Type: application/json"
gql() { curl -s -X POST "${API}" -H "${HDR_AUTH}" -H "${HDR_JSON}" --data "$1"; }

# ---------- product constants ----------
HANDLE="little-pear-mommy-and-me-pajamas"
TITLE="Little Pear Mommy and Me Pajamas — Short-Sleeve Set"
SEO_TITLE="Pear Mommy & Me Pajamas — Cotton Set | Dress Like Mommy"
SEO_DESC="Shop our Little Pear matching mommy-and-me pajama set — soft cotton short-sleeve set for mom + daughter. Kids 2Y–10Y, Mom S–XL."
PRODUCT_TYPE="Matching Family Pajamas"
VENDOR="dresslikemommy.com"
TAXONOMY_GID="gid://shopify/TaxonomyCategory/aa-1-17-4"
COLOR_LABEL="Little Pear Cream"
COLOR_TOKEN="CREAM"
SHORTCODE="VCF"
CHILD_PRICE="26.99"
MOTHER_PRICE="32.99"
CHILD_COMPARE="31.04"      # 26.99 × 1.15 → 31.04 (round_up .99 → 31.99)
MOTHER_COMPARE="38.24"     # 32.99 × 1.15 → 37.94 → 37.99
# Apply round_up(price × 1.15, .99):
CHILD_COMPARE="31.99"
MOTHER_COMPARE="37.99"
VENDOR_URL="https://detail.1688.com/offer/920493992812.html"

OUT_DIR="$(cd "$(dirname "$0")/../listings" && pwd)"
SIZE_CHART_FILE="${OUT_DIR}/size_chart.json"

# ---------- write SIZE_CHART (single source of truth) ----------
mkdir -p "${OUT_DIR}"
cat > "${SIZE_CHART_FILE}" <<'JSON'
[
  {"audience":"child","vendor_label":"90","picker_label":"Child 2 Years","sku_suffix":"KID2Y","age":"2","weight":"12–14 kg / 26–31 lbs","height":"85–95 cm / 33–37 in","chest_cm":"60 cm / 23.6 in","hip_cm":"58 cm / 22.8 in","waist_cm":"42 cm / 16.5 in","length_cm":"33 cm / 13.0 in","sleeve_cm":"16.5 cm / 6.5 in","pant_cm":"27 cm / 10.6 in","size_gid":"gid://shopify/Metaobject/129972863073"},
  {"audience":"child","vendor_label":"100","picker_label":"Child 3 Years","sku_suffix":"KID3Y","age":"3","weight":"14–17 kg / 31–37 lbs","height":"95–105 cm / 37–41 in","chest_cm":"64 cm / 25.2 in","hip_cm":"62 cm / 24.4 in","waist_cm":"44 cm / 17.3 in","length_cm":"36 cm / 14.2 in","sleeve_cm":"17.5 cm / 6.9 in","pant_cm":"29.5 cm / 11.6 in","size_gid":"gid://shopify/Metaobject/129972895841"},
  {"audience":"child","vendor_label":"110","picker_label":"Child 4 Years","sku_suffix":"KID4Y","age":"4","weight":"17–20 kg / 37–44 lbs","height":"105–115 cm / 41–45 in","chest_cm":"68 cm / 26.8 in","hip_cm":"66 cm / 26.0 in","waist_cm":"46 cm / 18.1 in","length_cm":"39 cm / 15.4 in","sleeve_cm":"19.5 cm / 7.7 in","pant_cm":"32 cm / 12.6 in","size_gid":"gid://shopify/Metaobject/129972928609"},
  {"audience":"child","vendor_label":"120","picker_label":"Child 5 Years","sku_suffix":"KID5Y","age":"5","weight":"20–24 kg / 44–53 lbs","height":"115–125 cm / 45–49 in","chest_cm":"72 cm / 28.3 in","hip_cm":"70 cm / 27.6 in","waist_cm":"48 cm / 18.9 in","length_cm":"42 cm / 16.5 in","sleeve_cm":"21 cm / 8.3 in","pant_cm":"34.5 cm / 13.6 in","size_gid":"gid://shopify/Metaobject/129972961377"},
  {"audience":"child","vendor_label":"130","picker_label":"Child 6-7 Years","sku_suffix":"KID67Y","age":"6–7","weight":"24–28 kg / 53–62 lbs","height":"125–135 cm / 49–53 in","chest_cm":"76 cm / 29.9 in","hip_cm":"74 cm / 29.1 in","waist_cm":"50 cm / 19.7 in","length_cm":"45 cm / 17.7 in","sleeve_cm":"22.5 cm / 8.9 in","pant_cm":"37 cm / 14.6 in","size_gid":"gid://shopify/Metaobject/139840323681"},
  {"audience":"child","vendor_label":"140","picker_label":"Child 8 Years","sku_suffix":"KID8Y","age":"8","weight":"28–33 kg / 62–73 lbs","height":"135–145 cm / 53–57 in","chest_cm":"80 cm / 31.5 in","hip_cm":"78 cm / 30.7 in","waist_cm":"52 cm / 20.5 in","length_cm":"48 cm / 18.9 in","sleeve_cm":"24 cm / 9.4 in","pant_cm":"39.5 cm / 15.6 in","size_gid":"gid://shopify/Metaobject/139840356449"},
  {"audience":"child","vendor_label":"150","picker_label":"Child 9-10 Years","sku_suffix":"KID910Y","age":"9–10","weight":"33–38 kg / 73–84 lbs","height":"145–155 cm / 57–61 in","chest_cm":"84 cm / 33.1 in","hip_cm":"82 cm / 32.3 in","waist_cm":"54 cm / 21.3 in","length_cm":"51 cm / 20.1 in","sleeve_cm":"25.5 cm / 10.0 in","pant_cm":"42 cm / 16.5 in","size_gid":"gid://shopify/Metaobject/139840389217"},
  {"audience":"mother","vendor_label":"S","picker_label":"Mother S","sku_suffix":"MOMS","age":"—","weight":"45–52 kg / 99–115 lbs","height":"155–162 cm / 61–64 in","chest_cm":"94 cm / 37.0 in","hip_cm":"104 cm / 40.9 in","waist_cm":"70 cm / 27.6 in","length_cm":"59 cm / 23.2 in","sleeve_cm":"21 cm / 8.3 in","pant_cm":"45 cm / 17.7 in","size_gid":"gid://shopify/Metaobject/129975255137"},
  {"audience":"mother","vendor_label":"M","picker_label":"Mother M","sku_suffix":"MOMM","age":"—","weight":"52–60 kg / 115–132 lbs","height":"160–167 cm / 63–66 in","chest_cm":"98 cm / 38.6 in","hip_cm":"108 cm / 42.5 in","waist_cm":"72 cm / 28.3 in","length_cm":"60 cm / 23.6 in","sleeve_cm":"22 cm / 8.7 in","pant_cm":"46 cm / 18.1 in","size_gid":"gid://shopify/Metaobject/129975222369"},
  {"audience":"mother","vendor_label":"L","picker_label":"Mother L","sku_suffix":"MOML","age":"—","weight":"60–68 kg / 132–150 lbs","height":"165–172 cm / 65–68 in","chest_cm":"102 cm / 40.2 in","hip_cm":"112 cm / 44.1 in","waist_cm":"74 cm / 29.1 in","length_cm":"61 cm / 24.0 in","sleeve_cm":"23 cm / 9.1 in","pant_cm":"47 cm / 18.5 in","size_gid":"gid://shopify/Metaobject/129975189601"},
  {"audience":"mother","vendor_label":"XL","picker_label":"Mother XL","sku_suffix":"MOMXL","age":"—","weight":"68–77 kg / 150–170 lbs","height":"168–175 cm / 66–69 in","chest_cm":"106 cm / 41.7 in","hip_cm":"116 cm / 45.7 in","waist_cm":"76 cm / 29.9 in","length_cm":"62 cm / 24.4 in","sleeve_cm":"24 cm / 9.4 in","pant_cm":"48 cm / 18.9 in","size_gid":"gid://shopify/Metaobject/129975287905"}
]
JSON

# ---------- preflight guards ----------
ROW_COUNT=$(jq 'length' "${SIZE_CHART_FILE}")
echo "Preflight: SIZE_CHART rows = ${ROW_COUNT}"
[ "${ROW_COUNT}" -eq 11 ] || { echo "FAIL: expected 11 rows"; exit 1; }

jq -e 'all(.[]; .audience and .vendor_label and .picker_label and .sku_suffix and .age and .weight and .height and .chest_cm and .hip_cm and .waist_cm and .length_cm and .sleeve_cm and .pant_cm)' \
  "${SIZE_CHART_FILE}" > /dev/null || { echo "FAIL: missing required fields"; exit 1; }

DUP=$(jq -r '[.[].picker_label] | group_by(.) | map(select(length>1)) | length' "${SIZE_CHART_FILE}")
[ "${DUP}" -eq 0 ] || { echo "FAIL: duplicate picker_labels"; exit 1; }

[ ${#TITLE} -le 70 ] || { echo "FAIL: TITLE > 70"; exit 1; }
[ ${#SEO_TITLE} -le 60 ] || { echo "FAIL: SEO_TITLE > 60"; exit 1; }
[ ${#SEO_DESC} -le 155 ] || { echo "FAIL: SEO_DESC > 155"; exit 1; }
echo "Preflight: PASS"

# ---------- derive option values, variants, body table ----------
SIZE_VALUES_JSON=$(jq -c '[.[].picker_label | {name:.}]' "${SIZE_CHART_FILE}")
COLOR_VALUES_JSON=$(jq -c -n --arg c "${COLOR_LABEL}" '[{name:$c}]')

VARIANTS_JSON=$(jq -c \
  --arg cprice "${CHILD_PRICE}" --arg ccmp "${CHILD_COMPARE}" \
  --arg mprice "${MOTHER_PRICE}" --arg mcmp "${MOTHER_COMPARE}" \
  --arg sc "${SHORTCODE}" --arg ct "${COLOR_TOKEN}" --arg color "${COLOR_LABEL}" '
  [ .[] | {
      price:    (if .audience=="child" then $cprice else $mprice end),
      compareAtPrice: (if .audience=="child" then $ccmp else $mcmp end),
      inventoryPolicy: "DENY",
      inventoryItem: { sku: ("DLM-"+$sc+"-"+.sku_suffix+"-"+$ct), tracked: true, requiresShipping: true, measurement: { weight: { value: (if .audience=="child" then 150 else 350 end), unit: "GRAMS" } } },
      optionValues: [ {optionName:"Size", name: .picker_label}, {optionName:"Color", name: $color} ]
    } ]
  ' "${SIZE_CHART_FILE}")

# Build body-html size table rows: 10 columns
KID_TR=$(jq -r '
  [.[] | select(.audience=="child")] |
  map( "<tr><td>" + .picker_label + "</td><td>" + .age + "</td><td>" + .weight + "</td><td>" + .height + "</td><td>" + .chest_cm + "</td><td>" + .sleeve_cm + "</td><td>" + .pant_cm + "</td><td>" + .hip_cm + "</td><td>" + .waist_cm + "</td><td>" + .length_cm + "</td></tr>" )
  | join("\n      ")
' "${SIZE_CHART_FILE}")

MOM_TR=$(jq -r '
  [.[] | select(.audience=="mother")] |
  map( "<tr><td>" + .picker_label + "</td><td>" + .age + "</td><td>" + .weight + "</td><td>" + .height + "</td><td>" + .chest_cm + "</td><td>" + .sleeve_cm + "</td><td>" + .pant_cm + "</td><td>" + .hip_cm + "</td><td>" + .waist_cm + "</td><td>" + .length_cm + "</td></tr>" )
  | join("\n      ")
' "${SIZE_CHART_FILE}")

# ---------- body html ----------
BODY_HTML=$(cat <<HTML
<ul>
  <li><strong>Fabric:</strong> Soft 100% cotton knit — lightweight, breathable, and gentle on skin for all-night comfort.</li>
  <li><strong>Family Story:</strong> Matching mom-and-mini sets so brunch, birthdays, and holiday cards always feel picture-perfect.</li>
  <li><strong>Print:</strong> Hand-drawn Little Pear print — sweet golden pears tossed across a creamy ivory ground with sage leaves.</li>
  <li><strong>Design Details:</strong> Short-sleeve crew tee + pull-on shorts in a soft pear-green trim, relaxed family fit.</li>
  <li><strong>Care:</strong> Machine wash cold with like colors, tumble dry low, no bleach.</li>
  <li><strong>Size Range:</strong> Child 2Y–10Y plus Mother S–XL — make every moment match.</li>
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
      <th>Pant/Short</th>
      <th>Hip</th>
      <th>Waist</th>
      <th>Garment Length</th>
    </tr>
  </thead>
  <tbody>
    <!-- Children Sizes -->
    ${KID_TR}
    <!-- Adult Sizes -->
    ${MOM_TR}
  </tbody>
</table>

<p>Our Little Pear pajama set is designed for those slow summer mornings when the whole family lingers a little longer over pancakes. Brushed-soft cotton skims the skin without clinging, and a relaxed silhouette gives both moms and minis room to stretch, snuggle, and play. The matching short-sleeve top + shorts pair makes a low-fuss, high-cute outfit for sleepovers, lazy Sundays, and pre-bedtime story time.</p>

<p>The print itself is a love letter to orchard summers — golden pears float across a soft ivory ground with little sage leaves and dainty blossoms tucked between. Sweet, fresh, and just a touch retro, it photographs beautifully against linen sheets, garden picnics, and white porch swings. Wear them for slow weekends, summer-camp pajama nights, photo-day matching, or as a gift for the new mom who loves a little whimsy.</p>

<h3>Key Features:</h3>
<ul>
  <li><strong>Mommy-and-Me Matching:</strong> Coordinating cuts and identical print scaled for both mom and child.</li>
  <li><strong>Soft Cotton Knit:</strong> Lightweight, breathable, and pre-washed for all-night comfort.</li>
  <li><strong>Easy On / Easy Off:</strong> Pull-over crew neck top and elastic-waist shorts — no buttons, no fuss.</li>
  <li><strong>Family Photo-Ready:</strong> Cream + sage palette plays nicely with linen, neutrals, and fresh florals.</li>
  <li><strong>Travel-Friendly:</strong> Packs flat and barely wrinkles — perfect for grandparent visits and weekend getaways.</li>
</ul>

<p>Slip into the set and make every morning feel a little more picture-perfect — because the best matching memories start in your favorite pajamas.</p>
HTML
)

# Stash body html for later metafield + verify
BODY_FILE="${OUT_DIR}/body.html"
printf "%s" "${BODY_HTML}" > "${BODY_FILE}"

# tags
TAGS_JSON=$(jq -c -n \
  --arg url "${VENDOR_URL}" \
  --argjson chart "$(cat ${SIZE_CHART_FILE})" '
  ($chart | map(.picker_label)) as $pl |
  ([
    "Mommy and Me", "Pajamas", "Matching Family Pajamas", "Short Sleeve Pajamas",
    "Summer", "Cream", "Yellow", "Green", "White",
    "Pear Print", "Little Pear", "Fruit Print", "Cottagecore",
    "Cotton", "Knit", "Two-Piece Pajama Set",
    $url
  ]
  + (if any($pl[]; . == "Child 2 Years" or . == "Child 3 Years") then ["Child 2-3yr"] else [] end)
  + (if any($pl[]; . == "Child 4 Years" or . == "Child 5 Years") then ["Child 4-5yr"] else [] end)
  + (if any($pl[]; . == "Child 6-7 Years" or . == "Child 8 Years") then ["Child 6-8yr"] else [] end)
  + (if any($pl[]; . == "Child 9-10 Years") then ["Child 9-10yr"] else [] end)
  + ([ $chart[] | select(.audience=="mother") | "Mother " + .vendor_label ])
  ) | unique
'
)

# size metafield (one GID per row that has one)
SIZE_GIDS=$(jq -c '[.[] | select(.size_gid != null) | .size_gid]' "${SIZE_CHART_FILE}")

# ---------- Phase 5a: productCreate ----------
echo "Phase 5a: productCreate ..."
PRODUCT_OPTIONS_JSON=$(jq -c -n --argjson sv "${SIZE_VALUES_JSON}" --argjson cv "${COLOR_VALUES_JSON}" '
  [ {name:"Size", values: $sv}, {name:"Color", values: $cv} ]
')

CREATE_PAYLOAD=$(jq -c -n \
  --arg title "${TITLE}" \
  --arg handle "${HANDLE}" \
  --arg body "${BODY_HTML}" \
  --arg ptype "${PRODUCT_TYPE}" \
  --arg vendor "${VENDOR}" \
  --arg seoT "${SEO_TITLE}" \
  --arg seoD "${SEO_DESC}" \
  --arg cat "${TAXONOMY_GID}" \
  --argjson opts "${PRODUCT_OPTIONS_JSON}" \
  --argjson tags "${TAGS_JSON}" '
  { query: "mutation pc($input: ProductInput!){ productCreate(input:$input){ product{ id handle title } userErrors{ field message } } }",
    variables: { input: {
      title: $title, handle: $handle, descriptionHtml: $body,
      productType: $ptype, vendor: $vendor,
      tags: $tags, productOptions: $opts,
      seo: { title: $seoT, description: $seoD },
      status: "ACTIVE", category: $cat
    } }
  }')

CREATE_RESP=$(gql "${CREATE_PAYLOAD}")
echo "${CREATE_RESP}" | jq .
PRODUCT_ID=$(echo "${CREATE_RESP}" | jq -r '.data.productCreate.product.id')
[ "${PRODUCT_ID}" != "null" ] && [ -n "${PRODUCT_ID}" ] || { echo "FAIL: productCreate"; exit 1; }
echo "PRODUCT_ID=${PRODUCT_ID}"

# ---------- Phase 5b: productVariantsBulkCreate ----------
echo "Phase 5b: productVariantsBulkCreate ..."
VAR_PAYLOAD=$(jq -c -n --arg pid "${PRODUCT_ID}" --argjson vars "${VARIANTS_JSON}" '
  { query: "mutation v($pid: ID!, $vars: [ProductVariantsBulkInput!]!, $strategy: ProductVariantsBulkCreateStrategy){ productVariantsBulkCreate(productId:$pid, variants:$vars, strategy:$strategy){ productVariants{ id sku title price compareAtPrice } userErrors{ field message } } }",
    variables: { pid: $pid, vars: $vars, strategy: "REMOVE_STANDALONE_VARIANT" }
  }')
VAR_RESP=$(gql "${VAR_PAYLOAD}")
echo "${VAR_RESP}" | jq '.data.productVariantsBulkCreate.userErrors, (.data.productVariantsBulkCreate.productVariants | length)'
ERR_COUNT=$(echo "${VAR_RESP}" | jq '.data.productVariantsBulkCreate.userErrors | length')
[ "${ERR_COUNT}" -eq 0 ] || { echo "${VAR_RESP}" | jq .; echo "FAIL: variant errors"; exit 1; }

# ---------- Phase 5c: metafieldsSet ----------
echo "Phase 5c: metafieldsSet ..."
META_PAYLOAD=$(jq -c -n --arg pid "${PRODUCT_ID}" --argjson sizes "${SIZE_GIDS}" '
  {query:"mutation m($metafields:[MetafieldsSetInput!]!){ metafieldsSet(metafields:$metafields){ metafields{ namespace key } userErrors{ field message } } }",
   variables:{ metafields: [
    {ownerId:$pid, namespace:"custom", key:"category1", type:"single_line_text_field", value:"Mommy and Me"},
    {ownerId:$pid, namespace:"custom", key:"subcategory", type:"single_line_text_field", value:"Pajamas"},
    {ownerId:$pid, namespace:"custom", key:"subcategory2", type:"single_line_text_field", value:"Summer Pajamas"},
    {ownerId:$pid, namespace:"custom", key:"pattern", type:"single_line_text_field", value:"Little Pear cartoon fruit print on cream with sage leaves"},
    {ownerId:$pid, namespace:"custom", key:"style", type:"single_line_text_field", value:"Matching Family Set"},
    {ownerId:$pid, namespace:"custom", key:"type", type:"single_line_text_field", value:"Two-Piece Pajama Set"},
    {ownerId:$pid, namespace:"mm-google-shopping", key:"custom_product", type:"boolean", value:"false"},
    {ownerId:$pid, namespace:"mm-google-shopping", key:"google_product_category", type:"single_line_text_field", value:"Apparel & Accessories > Clothing > Sleepwear & Loungewear > Pajamas"},
    {ownerId:$pid, namespace:"mm-google-shopping", key:"gender", type:"single_line_text_field", value:"female"},
    {ownerId:$pid, namespace:"mm-google-shopping", key:"age_group", type:"single_line_text_field", value:"adult"},
    {ownerId:$pid, namespace:"mm-google-shopping", key:"condition", type:"single_line_text_field", value:"new"},
    {ownerId:$pid, namespace:"mm-google-shopping", key:"custom_label_0", type:"single_line_text_field", value:"Mommy and Me"},
    {ownerId:$pid, namespace:"mm-google-shopping", key:"custom_label_1", type:"single_line_text_field", value:"Little Pear"},
    {ownerId:$pid, namespace:"mm-google-shopping", key:"custom_label_2", type:"single_line_text_field", value:"Summer"},
    {ownerId:$pid, namespace:"mm-google-shopping", key:"custom_label_3", type:"single_line_text_field", value:"Short Sleeve"},
    {ownerId:$pid, namespace:"mm-google-shopping", key:"custom_label_4", type:"single_line_text_field", value:"Family Matching"},
    {ownerId:$pid, namespace:"shopify", key:"age-group", type:"list.metaobject_reference", value:"[\"gid://shopify/Metaobject/128116523105\",\"gid://shopify/Metaobject/128116490337\"]"},
    {ownerId:$pid, namespace:"shopify", key:"color-pattern", type:"list.metaobject_reference", value:"[\"gid://shopify/Metaobject/69639733345\",\"gid://shopify/Metaobject/69622104161\",\"gid://shopify/Metaobject/70220546145\"]"},
    {ownerId:$pid, namespace:"shopify", key:"fabric", type:"list.metaobject_reference", value:"[\"gid://shopify/Metaobject/69622399073\"]"},
    {ownerId:$pid, namespace:"shopify", key:"size", type:"list.metaobject_reference", value:($sizes|tostring)},
    {ownerId:$pid, namespace:"shopify", key:"target-gender", type:"list.metaobject_reference", value:"[\"gid://shopify/Metaobject/129971617889\"]"},
    {ownerId:$pid, namespace:"global", key:"title_tag", type:"single_line_text_field", value:"'"${SEO_TITLE}"'"},
    {ownerId:$pid, namespace:"global", key:"description_tag", type:"single_line_text_field", value:"'"${SEO_DESC}"'"}
   ] } }')
META_RESP=$(gql "${META_PAYLOAD}")
echo "${META_RESP}" | jq '.data.metafieldsSet.userErrors, (.data.metafieldsSet.metafields | length)'

# ---------- Phase 5d: publishablePublish ----------
echo "Phase 5d: publish to sales channels ..."
for PUB_GID in \
  "gid://shopify/Publication/55169925" \
  "gid://shopify/Publication/21969633377" \
  "gid://shopify/Publication/29172400225" \
  "gid://shopify/Publication/76582879329" \
  "gid://shopify/Publication/76604768353"
do
  PUB_PAYLOAD=$(jq -c -n --arg pid "${PRODUCT_ID}" --arg pub "${PUB_GID}" '
    {query:"mutation pp($id:ID!,$input:[PublicationInput!]!){ publishablePublish(id:$id,input:$input){ userErrors{ field message } } }",
     variables:{id:$pid,input:[{publicationId:$pub}]}}')
  PUB_RESP=$(gql "${PUB_PAYLOAD}")
  echo "  ${PUB_GID} -> $(echo ${PUB_RESP} | jq -c '.data.publishablePublish.userErrors')"
done

# ---------- Phase 5e: media (skip if uploads dir empty) ----------
UPLOAD_DIR="/Users/fsuels/Projects/dresslikemommy/uploads/${HANDLE}"
if [ -d "${UPLOAD_DIR}" ] && [ "$(ls -A ${UPLOAD_DIR} 2>/dev/null)" ]; then
  echo "Phase 5e: media upload from ${UPLOAD_DIR} ..."
  echo "  (manual follow-up — runner is idempotent; rerun media block after files drop)"
else
  echo "Phase 5e: SKIP media — no files at ${UPLOAD_DIR} (manual follow-up)"
fi

# ---------- Phase 6: post-create verify ----------
echo "Phase 6: verify ..."
VERIFY_PAYLOAD=$(jq -c -n --arg pid "${PRODUCT_ID}" '
  {query:"query($id:ID!){ product(id:$id){ id handle title onlineStoreUrl publishedAt seo{title description} descriptionHtml tags variants(first:50){edges{node{ sku title price compareAtPrice inventoryPolicy inventoryItem{ tracked }}}} collections(first:20){edges{node{ id title }}} } }",
   variables:{id:$pid}}')
VERIFY_RESP=$(gql "${VERIFY_PAYLOAD}")
echo "${VERIFY_RESP}" > "${OUT_DIR}/verify.json"

echo
echo "=== Verify summary ==="
python3 - <<PYEOF
import json,re,sys
d = json.load(open("${OUT_DIR}/verify.json"))
p = d["data"]["product"]
chart = json.load(open("${SIZE_CHART_FILE}"))
expected_skus = sorted(["DLM-${SHORTCODE}-"+r["sku_suffix"]+"-${COLOR_TOKEN}" for r in chart])
live_skus = sorted([e["node"]["sku"] for e in p["variants"]["edges"]])
print("Title len:", len(p["title"]), "<=70?", len(p["title"])<=70)
print("SEO title len:", len(p["seo"]["title"]), "<=60?", len(p["seo"]["title"])<=60)
print("SEO desc len:", len(p["seo"]["description"]), "<=155?", len(p["seo"]["description"])<=155)
print("Live variant count:", len(live_skus), "expected:", len(chart))
print("SKUs match:", live_skus == expected_skus)
if live_skus != expected_skus:
    print("  expected:", expected_skus)
    print("  live:    ", live_skus)
print("publishedAt:", p["publishedAt"])
print("onlineStoreUrl:", p["onlineStoreUrl"])
body = p["descriptionHtml"]
th_count = body.count("<th>")
tr_data = re.findall(r"<tbody>(.*?)</tbody>", body, re.S)
tr_count = len(re.findall(r"<tr>", tr_data[0])) if tr_data else 0
print("size-table <th> cols:", th_count, "(want 10)")
print("size-table data <tr> rows:", tr_count, "(want 11)")
waist_in_body = all(r["waist_cm"] in body for r in chart)
print("waist values in body:", waist_in_body)
for v in p["variants"]["edges"]:
    n = v["node"]
    ok = (n["inventoryPolicy"]=="DENY" and n["inventoryItem"]["tracked"] and n["price"] and n["compareAtPrice"])
    if not ok:
        print("  variant flag:", n["sku"], n)
print("Collections:", [e["node"]["title"] for e in p["collections"]["edges"]])
PYEOF

echo
echo "=== Hand-off ==="
echo "Admin URL: https://admin.shopify.com/store/dresslikemommy/products/$(echo ${PRODUCT_ID} | sed 's|.*/||')"
echo "Live URL : https://www.dresslikemommy.com/products/${HANDLE}"
echo "Files    : ${SIZE_CHART_FILE}  ${OUT_DIR}/body.html  ${OUT_DIR}/verify.json"
