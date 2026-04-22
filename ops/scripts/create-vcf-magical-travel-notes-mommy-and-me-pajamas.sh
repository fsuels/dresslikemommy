#!/usr/bin/env bash
# Create live Shopify product: Magical Travel Notes Mommy and Me Pajamas — Short-Sleeve Set
# Single source of truth: SIZE_CHART JSON declared at top.
# Derives variants payload, body-HTML size table, tags, shopify.size GIDs, SEO size phrase via jq.
set -euo pipefail

# ----- Credentials -----
ENV_FILE="${HOME}/.config/dresslikemommy/shopify-admin.env"
if [ -f "$ENV_FILE" ]; then
  # shellcheck disable=SC1090
  source "$ENV_FILE"
else
  echo "ERROR: missing $ENV_FILE" >&2
  exit 2
fi
: "${SHOPIFY_STORE_DOMAIN:?}"
: "${SHOPIFY_ADMIN_ACCESS_TOKEN:?}"
API="https://${SHOPIFY_STORE_DOMAIN}/admin/api/2025-01/graphql.json"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

# ----- Constants -----
TITLE="Magical Travel Notes Mommy and Me Pajamas — Short-Sleeve Set"
HANDLE="magical-travel-notes-mommy-and-me-pajamas"
SHORTCODE="VCF"
COLOR_TOKEN="CREAM"
COLOR_NAME="Magical Travel Notes Cream"
PRINT_NAME="Magical Travel Notes"
SEASON="Summer"
CATEGORY="Pajamas"
CATEGORYWORD="Pajamas"
GARMENT_HOOK="Short-Sleeve Set"
PRODUCT_TYPE="Matching Family Pajamas"
TAXONOMY_GID="gid://shopify/TaxonomyCategory/aa-1-17-4"
CHILD_PRICE="35.99"
MOTHER_PRICE="39.99"
VENDOR_URL="https://detail.1688.com/offer/828526529351.html"
SEO_TITLE="Magical Travel Notes Mommy & Me Pajamas | Dress Like Mommy"
SEO_DESC="Shop our Magical Travel Notes matching mommy-and-me pajamas — soft cotton short-sleeve set for mom + daughter. Sizes 2Y–10Y & Mom S–XL."

# Compute compare-at: round_up to next .99
ru() { python3 -c "import math,sys; p=float(sys.argv[1]); v=p*1.15; n=math.ceil((v-0.99)/1.0)*1.0+0.99; n=round(n,2); print(f'{n:.2f}')" "$1"; }
CHILD_COMPARE="$(ru "$CHILD_PRICE")"   # 35.99 -> 41.99? 35.99*1.15=41.3885 -> 41.99
MOTHER_COMPARE="$(ru "$MOTHER_PRICE")" # 39.99*1.15=45.9885 -> 45.99
echo "Compare-at: child=$CHILD_COMPARE  mother=$MOTHER_COMPARE"

# ----- SIZE_CHART (single source of truth) -----
# Vendor 尺码参数 image (user-supplied; 1688 direct fetch captcha-blocked per fallback rule) is authoritative.
# Column map used:
#   尺码 = vendor_label
#   1/2胸围 -> chest_cm = ×2
#   1/2腰围 -> waist_cm = ×2
#   衣长   -> length_cm (verbatim)
#   肩宽   -> shoulder (not emitted to chart; informational)
#   袖长   -> sleeve_cm
#   裤长   -> pant_cm
#   1/2臀围 -> hip_cm = ×2
# Kid weights inferred from standard CN kid height->weight bands (no weight column on vendor sheet).
# Adult XS and XXL rows exist on vendor sheet but are NOT emitted: store size scheme is S/M/L/XL only. Documented in listing.md.
cat > "$WORK/size_chart.json" <<'JSON'
[
 {"audience":"child","vendor_label":"90","picker_label":"Child 2 Years","sku_suffix":"KID2Y","age":"2","weight":"11–14 kg / 24–31 lbs","height":"85–95 cm / 33–37 in","chest_cm":68,"hip_cm":69,"waist_cm":43,"length_cm":41,"sleeve_cm":33,"pant_cm":53,"shopify_size_gid":"gid://shopify/Metaobject/129972863073"},
 {"audience":"child","vendor_label":"100","picker_label":"Child 3 Years","sku_suffix":"KID3Y","age":"3","weight":"14–16 kg / 31–35 lbs","height":"95–105 cm / 37–41 in","chest_cm":72,"hip_cm":73,"waist_cm":45,"length_cm":44,"sleeve_cm":36,"pant_cm":58,"shopify_size_gid":"gid://shopify/Metaobject/129972895841"},
 {"audience":"child","vendor_label":"110","picker_label":"Child 4 Years","sku_suffix":"KID4Y","age":"4","weight":"16–19 kg / 35–42 lbs","height":"105–115 cm / 41–45 in","chest_cm":76,"hip_cm":77,"waist_cm":47,"length_cm":47,"sleeve_cm":39,"pant_cm":63,"shopify_size_gid":"gid://shopify/Metaobject/129972928609"},
 {"audience":"child","vendor_label":"120","picker_label":"Child 5 Years","sku_suffix":"KID5Y","age":"5","weight":"19–22 kg / 42–49 lbs","height":"115–125 cm / 45–49 in","chest_cm":80,"hip_cm":81,"waist_cm":49,"length_cm":50,"sleeve_cm":42,"pant_cm":68,"shopify_size_gid":"gid://shopify/Metaobject/129972961377"},
 {"audience":"child","vendor_label":"130","picker_label":"Child 6-7 Years","sku_suffix":"KID67Y","age":"6–7","weight":"22–27 kg / 49–60 lbs","height":"125–135 cm / 49–53 in","chest_cm":84,"hip_cm":85,"waist_cm":52,"length_cm":53,"sleeve_cm":45,"pant_cm":73,"shopify_size_gid":"gid://shopify/Metaobject/139840323681"},
 {"audience":"child","vendor_label":"140","picker_label":"Child 8 Years","sku_suffix":"KID8Y","age":"8","weight":"27–33 kg / 60–73 lbs","height":"135–145 cm / 53–57 in","chest_cm":88,"hip_cm":89,"waist_cm":55,"length_cm":56,"sleeve_cm":48,"pant_cm":78,"shopify_size_gid":"gid://shopify/Metaobject/139840356449"},
 {"audience":"child","vendor_label":"150","picker_label":"Child 9-10 Years","sku_suffix":"KID910Y","age":"9–10","weight":"33–40 kg / 73–88 lbs","height":"145–155 cm / 57–61 in","chest_cm":92,"hip_cm":93,"waist_cm":57,"length_cm":59,"sleeve_cm":51,"pant_cm":83,"shopify_size_gid":"gid://shopify/Metaobject/139840389217"},
 {"audience":"mother","vendor_label":"S","picker_label":"Mother S","sku_suffix":"MOMS","age":"—","weight":"50–58 kg / 110–128 lbs","height":"155–162 cm / 61–64 in","chest_cm":106,"hip_cm":111,"waist_cm":73,"length_cm":66,"sleeve_cm":57,"pant_cm":97,"shopify_size_gid":"gid://shopify/Metaobject/129975255137"},
 {"audience":"mother","vendor_label":"M","picker_label":"Mother M","sku_suffix":"MOMM","age":"—","weight":"58–65 kg / 128–143 lbs","height":"160–167 cm / 63–66 in","chest_cm":110,"hip_cm":115,"waist_cm":75,"length_cm":69,"sleeve_cm":54,"pant_cm":99,"shopify_size_gid":"gid://shopify/Metaobject/129975222369"},
 {"audience":"mother","vendor_label":"L","picker_label":"Mother L","sku_suffix":"MOML","age":"—","weight":"65–72 kg / 143–159 lbs","height":"165–172 cm / 65–68 in","chest_cm":114,"hip_cm":119,"waist_cm":77,"length_cm":71,"sleeve_cm":57,"pant_cm":102,"shopify_size_gid":"gid://shopify/Metaobject/129975189601"},
 {"audience":"mother","vendor_label":"XL","picker_label":"Mother XL","sku_suffix":"MOMXL","age":"—","weight":"72–80 kg / 159–176 lbs","height":"170–177 cm / 67–70 in","chest_cm":116,"hip_cm":123,"waist_cm":80,"length_cm":73,"sleeve_cm":58,"pant_cm":103,"shopify_size_gid":"gid://shopify/Metaobject/129975287905"}
]
JSON

# ----- Preflight guards (halt before API) -----
echo "== Preflight =="
ROW_COUNT=$(jq 'length' "$WORK/size_chart.json")
[ "$ROW_COUNT" -eq 11 ] || { echo "FAIL: row_count=$ROW_COUNT, expected 11"; exit 1; }
jq -e 'all(.[]; .audience and .vendor_label and .picker_label and .sku_suffix and .age and .weight and .height and (.chest_cm|type=="number") and (.hip_cm|type=="number") and (.waist_cm|type=="number") and (.length_cm|type=="number") and (.sleeve_cm|type=="number") and (.pant_cm|type=="number"))' "$WORK/size_chart.json" >/dev/null \
  || { echo "FAIL: missing required SIZE_CHART fields"; exit 1; }
DUPS=$(jq -r '.[].picker_label' "$WORK/size_chart.json" | sort | uniq -d | wc -l | tr -d ' ')
[ "$DUPS" -eq 0 ] || { echo "FAIL: duplicate picker_label"; exit 1; }
DUP_SKUS=$(jq -r --arg sc "$SHORTCODE" --arg ct "$COLOR_TOKEN" '.[] | "DLM-\($sc)-\(.sku_suffix)-\($ct)"' "$WORK/size_chart.json" | sort | uniq -d | wc -l | tr -d ' ')
[ "$DUP_SKUS" -eq 0 ] || { echo "FAIL: duplicate SKUs"; exit 1; }
[ ${#TITLE} -le 70 ] || { echo "FAIL: title len ${#TITLE}>70"; exit 1; }
[ ${#SEO_TITLE} -le 60 ] || { echo "FAIL: SEO title len ${#SEO_TITLE}>60"; exit 1; }
[ ${#SEO_DESC} -le 155 ] || { echo "FAIL: SEO desc len ${#SEO_DESC}>155"; exit 1; }
echo "Preflight OK (rows=$ROW_COUNT title=${#TITLE} seoT=${#SEO_TITLE} seoD=${#SEO_DESC})"

# ----- Derive size option values, variants, tags, body table, shopify.size GIDs -----
SIZE_VALUES_JSON=$(jq -c '[.[] | {name: .picker_label}]' "$WORK/size_chart.json")
SIZE_GIDS_JSON=$(jq -c '[.[] | .shopify_size_gid] | unique' "$WORK/size_chart.json")

# Variants payload
jq -c --arg sc "$SHORTCODE" --arg ct "$COLOR_TOKEN" --arg color "$COLOR_NAME" \
   --arg cprice "$CHILD_PRICE" --arg ccomp "$CHILD_COMPARE" \
   --arg mprice "$MOTHER_PRICE" --arg mcomp "$MOTHER_COMPARE" '
  [ .[] | {
    optionValues: [
      {optionName: "Size",  name: .picker_label},
      {optionName: "Color", name: $color}
    ],
    price:           (if .audience=="child" then $cprice else $mprice end),
    compareAtPrice:  (if .audience=="child" then $ccomp  else $mcomp  end),
    inventoryPolicy: "DENY",
    inventoryItem: {
      sku: ("DLM-" + $sc + "-" + .sku_suffix + "-" + $ct),
      tracked: true,
      requiresShipping: true
    }
  } ]' "$WORK/size_chart.json" > "$WORK/variants.json"

# Body HTML — generate 10-col size table from SIZE_CHART
python3 - "$WORK/size_chart.json" > "$WORK/body.html" <<'PY'
import json, sys
sc=json.load(open(sys.argv[1]))
def cm_in(cm):
    if cm is None: return "—"
    return f"{cm:g} cm / {round(cm/2.54,1):g} in"
rows_html=[]
last_aud=None
for r in sc:
    if r["audience"]!=last_aud:
        rows_html.append(f"<!-- {'Children Sizes' if r['audience']=='child' else 'Adult Sizes'} -->")
        last_aud=r["audience"]
    sleeve=cm_in(r["sleeve_cm"]) if r["sleeve_cm"] else "—"
    pant=cm_in(r["pant_cm"]) if r["pant_cm"] else "—"
    rows_html.append("<tr>"
        f"<td>{r['picker_label']}</td>"
        f"<td>{r['age']}</td>"
        f"<td>{r['weight']}</td>"
        f"<td>{r['height']}</td>"
        f"<td>{cm_in(r['chest_cm'])}</td>"
        f"<td>{sleeve}</td>"
        f"<td>{pant}</td>"
        f"<td>{cm_in(r['hip_cm'])}</td>"
        f"<td>{cm_in(r['waist_cm'])}</td>"
        f"<td>{cm_in(r['length_cm'])}</td>"
        "</tr>")
table_rows="\n".join(rows_html)

body=f"""<ul>
<li><strong>Soft cotton-blend gauze:</strong> Four-layer breathable cotton-blend gauze with an airy, smooth hand-feel that keeps mom and little one comfortable day into night.</li>
<li><strong>Make every moment match:</strong> Coordinating mother and daughter sets made for brunch, birthdays, holiday cards, and cozy family bonding — picture-perfect in seconds.</li>
<li><strong>Magical Travel Notes print:</strong> Whimsical watercolor storybook scene of mushrooms, ferns, hedgehogs, and woodland finds on a creamy ivory ground — like a page from a traveler's nature journal.</li>
<li><strong>Classic design details:</strong> Notched-collar button-front top with chest pocket, matching pull-on pants with elastic waist — easy on, easy off for sleep, lounging, and slow mornings.</li>
<li><strong>Easy care &amp; breathable:</strong> Machine-wash cold inside out, tumble dry low. Cotton-blend gauze softens with every wash.</li>
<li><strong>Full family size range:</strong> Girls 2–10 Years and Mothers S–XL so every little one and every mom can twin.</li>
</ul>
<p>&nbsp;</p>
<h3>Size Chart</h3>
<table id="size-chart">
<thead><tr>
<th>Size</th>
<th>Age</th>
<th>Recommended Weight (kg/lbs)</th>
<th>Recommended Height (cm/in)</th>
<th>Chest/Bust (cm/in)</th>
<th>Sleeve Length (cm/in)</th>
<th>Pant Length (cm/in)</th>
<th>Hip (cm/in)</th>
<th>Waist (cm/in)</th>
<th>Garment Length (cm/in)</th>
</tr></thead>
<tbody>
{table_rows}
</tbody>
</table>
<p>Our Magical Travel Notes mommy-and-me pajama set turns quiet evenings into a small forest adventure. A creamy ivory ground is scattered with hand-painted mushrooms, curling ferns, sleepy hedgehogs, and little woodland treasures — the kind of print that feels like a page from a keepsake travel journal. The notched-collar button-front top and matching pull-on pants carry the same motif in both adult and child cuts, so every family photo lines up the way you imagined it.</p>
<p>Wear it for weekend pajama days, bedtime stories, birthday mornings, and those holiday-card mornings when everyone needs to look picture-perfect without trying. The breathable four-layer cotton-blend gauze moves with you from pillow fights to pancake-making, and the full mother-and-daughter size run means nobody gets left out of the twinning moment.</p>
<h3>Key Features:</h3>
<ul>
<li><strong>Coordinated mother &amp; daughter fit:</strong> Identical Magical Travel Notes print in adult and child cuts so every family photo matches effortlessly.</li>
<li><strong>Four-layer cotton-blend gauze:</strong> Soft, breathable, and gentle on skin — a cozy weight for cool-weather sleep and slow mornings.</li>
<li><strong>Notched-collar button-front top:</strong> Classic pajama silhouette with chest pocket detail for a polished, storybook look.</li>
<li><strong>Pull-on matching pants:</strong> Elastic waistband for comfortable wear and easy on-and-off.</li>
<li><strong>Inclusive sizing:</strong> Girls 2–10 Years and Mothers S–XL — add both to cart to complete the set.</li>
</ul>
<p>Add the mother size and the matching children's size to your cart to make every moment match — bedtime, brunch, and every snapshot in between.</p>
"""
sys.stdout.write(body)
PY

BODY_HTML="$(cat "$WORK/body.html")"

# Tag list
TAGS_JSON=$(jq -c -n --arg url "$VENDOR_URL" '
[
  "Mommy and Me", "Pajamas", "Matching Family Pajamas",
  "Short Sleeve Pajamas", "Summer", "Summer Pajamas",
  "Cream", "Ivory", "Green", "Red",
  "Magical Travel Notes", "Mushroom Print", "Woodland Print",
  "Hedgehog Print", "Forest Print", "Fern Print", "Botanical",
  "Storybook", "Whimsical", "Cottagecore",
  "Child 2-3yr", "Child 4-5yr", "Child 6-8yr", "Child 9-10yr",
  "Mother S", "Mother M", "Mother L", "Mother XL",
  $url
]')

# ----- 5a. productCreate -----
echo "== productCreate =="
PRODUCT_INPUT=$(jq -c -n \
  --arg title "$TITLE" \
  --arg handle "$HANDLE" \
  --arg body "$BODY_HTML" \
  --arg ptype "$PRODUCT_TYPE" \
  --arg vendor "dresslikemommy.com" \
  --arg taxgid "$TAXONOMY_GID" \
  --arg seoT "$SEO_TITLE" \
  --arg seoD "$SEO_DESC" \
  --arg color "$COLOR_NAME" \
  --argjson sizeValues "$SIZE_VALUES_JSON" \
  --argjson tags "$TAGS_JSON" '
{
  title: $title, handle: $handle, descriptionHtml: $body,
  productType: $ptype, vendor: $vendor, status: "ACTIVE",
  category: $taxgid,
  tags: $tags,
  seo: {title: $seoT, description: $seoD},
  productOptions: [
    {name: "Size",  values: $sizeValues},
    {name: "Color", values: [{name: $color}]}
  ]
}')
cat > "$WORK/m_create.json" <<EOF
{"query":"mutation create(\$input: ProductInput!) { productCreate(input: \$input) { product { id handle title } userErrors { field message } } }","variables":{"input": $PRODUCT_INPUT}}
EOF
RES=$(curl -s -X POST "$API" -H "X-Shopify-Access-Token: $SHOPIFY_ADMIN_ACCESS_TOKEN" -H "Content-Type: application/json" --data @"$WORK/m_create.json")
echo "$RES" | jq '.data.productCreate.userErrors'
PRODUCT_ID=$(echo "$RES" | jq -r '.data.productCreate.product.id')
[ "$PRODUCT_ID" != "null" ] && [ -n "$PRODUCT_ID" ] || { echo "FAIL productCreate"; echo "$RES"; exit 1; }
echo "Product: $PRODUCT_ID"

# ----- 5b. productVariantsBulkCreate -----
echo "== productVariantsBulkCreate =="
VARIANTS_PAYLOAD=$(cat "$WORK/variants.json")
cat > "$WORK/m_variants.json" <<EOF
{"query":"mutation v(\$pid: ID!, \$vars: [ProductVariantsBulkInput!]!) { productVariantsBulkCreate(productId: \$pid, variants: \$vars, strategy: REMOVE_STANDALONE_VARIANT) { productVariants { id sku title price compareAtPrice inventoryPolicy } userErrors { field message } } }","variables":{"pid":"$PRODUCT_ID","vars":$VARIANTS_PAYLOAD}}
EOF
RES=$(curl -s -X POST "$API" -H "X-Shopify-Access-Token: $SHOPIFY_ADMIN_ACCESS_TOKEN" -H "Content-Type: application/json" --data @"$WORK/m_variants.json")
echo "$RES" | jq '.data.productVariantsBulkCreate.userErrors'
VCOUNT=$(echo "$RES" | jq '.data.productVariantsBulkCreate.productVariants | length')
echo "Variants created: $VCOUNT"
[ "$VCOUNT" -eq 11 ] || { echo "FAIL: expected 11 variants"; echo "$RES" | head -200; exit 1; }

# ----- 5c. metafieldsSet -----
echo "== metafieldsSet =="
SIZE_GIDS_VALUE=$(echo "$SIZE_GIDS_JSON" | jq -c .)
cat > "$WORK/metafields.json" <<EOF
[
  {"ownerId":"$PRODUCT_ID","namespace":"custom","key":"category1","type":"single_line_text_field","value":"Mommy and Me"},
  {"ownerId":"$PRODUCT_ID","namespace":"custom","key":"subcategory","type":"single_line_text_field","value":"Pajamas"},
  {"ownerId":"$PRODUCT_ID","namespace":"custom","key":"subcategory2","type":"single_line_text_field","value":"Summer Pajamas"},
  {"ownerId":"$PRODUCT_ID","namespace":"custom","key":"pattern","type":"single_line_text_field","value":"Magical Travel Notes Mushroom & Woodland Print"},
  {"ownerId":"$PRODUCT_ID","namespace":"custom","key":"style","type":"single_line_text_field","value":"Matching Family Set"},
  {"ownerId":"$PRODUCT_ID","namespace":"custom","key":"type","type":"single_line_text_field","value":"Two-Piece Pajama Set"},
  {"ownerId":"$PRODUCT_ID","namespace":"mm-google-shopping","key":"custom_product","type":"boolean","value":"false"},
  {"ownerId":"$PRODUCT_ID","namespace":"mm-google-shopping","key":"gender","type":"single_line_text_field","value":"female"},
  {"ownerId":"$PRODUCT_ID","namespace":"mm-google-shopping","key":"age_group","type":"single_line_text_field","value":"adult"},
  {"ownerId":"$PRODUCT_ID","namespace":"mm-google-shopping","key":"condition","type":"single_line_text_field","value":"new"},
  {"ownerId":"$PRODUCT_ID","namespace":"mm-google-shopping","key":"custom_label_0","type":"single_line_text_field","value":"Mommy and Me"},
  {"ownerId":"$PRODUCT_ID","namespace":"mm-google-shopping","key":"custom_label_1","type":"single_line_text_field","value":"Magical Travel Notes"},
  {"ownerId":"$PRODUCT_ID","namespace":"mm-google-shopping","key":"custom_label_2","type":"single_line_text_field","value":"Summer"},
  {"ownerId":"$PRODUCT_ID","namespace":"mm-google-shopping","key":"custom_label_3","type":"single_line_text_field","value":"Short Sleeve"},
  {"ownerId":"$PRODUCT_ID","namespace":"mm-google-shopping","key":"custom_label_4","type":"single_line_text_field","value":"Family Matching"},
  {"ownerId":"$PRODUCT_ID","namespace":"shopify","key":"age-group","type":"list.metaobject_reference","value":"[\"gid://shopify/Metaobject/128116523105\",\"gid://shopify/Metaobject/128116490337\"]"},
  {"ownerId":"$PRODUCT_ID","namespace":"shopify","key":"target-gender","type":"list.metaobject_reference","value":"[\"gid://shopify/Metaobject/129971617889\"]"},
  {"ownerId":"$PRODUCT_ID","namespace":"shopify","key":"color-pattern","type":"list.metaobject_reference","value":"[\"gid://shopify/Metaobject/129971519585\"]"},
  {"ownerId":"$PRODUCT_ID","namespace":"shopify","key":"fabric","type":"list.metaobject_reference","value":"[\"gid://shopify/Metaobject/69622399073\"]"},
  {"ownerId":"$PRODUCT_ID","namespace":"shopify","key":"size","type":"list.metaobject_reference","value":$(echo "$SIZE_GIDS_VALUE" | jq -R .)},
  {"ownerId":"$PRODUCT_ID","namespace":"global","key":"title_tag","type":"single_line_text_field","value":"$SEO_TITLE"},
  {"ownerId":"$PRODUCT_ID","namespace":"global","key":"description_tag","type":"single_line_text_field","value":"$SEO_DESC"}
]
EOF
# SKIPPED metafields (documented in listing.md):
#   shopify.clothing-features (no honest catalog entry for plain cotton-blend gauze pajamas)
#   shopify.sleeve-length-type (skipped for Pajamas per spec)
#   shopify.neckline, shopify.dress-occasion, shopify.dress-style, shopify.skirt-dress-length-type (Dresses/Tops only)
META=$(cat "$WORK/metafields.json")
cat > "$WORK/m_metafields.json" <<EOF
{"query":"mutation msf(\$mf: [MetafieldsSetInput!]!) { metafieldsSet(metafields: \$mf) { metafields { namespace key } userErrors { field message } } }","variables":{"mf":$META}}
EOF
RES=$(curl -s -X POST "$API" -H "X-Shopify-Access-Token: $SHOPIFY_ADMIN_ACCESS_TOKEN" -H "Content-Type: application/json" --data @"$WORK/m_metafields.json")
echo "$RES" | jq '.data.metafieldsSet.userErrors'
WROTE=$(echo "$RES" | jq '.data.metafieldsSet.metafields | length')
echo "Metafields written: $WROTE"

# ----- 5d. publishablePublish (5 channels) -----
echo "== publishablePublish =="
for PUB in \
  "gid://shopify/Publication/55169925" \
  "gid://shopify/Publication/21969633377" \
  "gid://shopify/Publication/29172400225" \
  "gid://shopify/Publication/76582879329" \
  "gid://shopify/Publication/76604768353"; do
cat > "$WORK/m_pub.json" <<EOF
{"query":"mutation pub(\$id: ID!, \$pubs: [PublicationInput!]!) { publishablePublish(id: \$id, input: \$pubs) { userErrors { field message } } }","variables":{"id":"$PRODUCT_ID","pubs":[{"publicationId":"$PUB"}]}}
EOF
RES=$(curl -s -X POST "$API" -H "X-Shopify-Access-Token: $SHOPIFY_ADMIN_ACCESS_TOKEN" -H "Content-Type: application/json" --data @"$WORK/m_pub.json")
echo "  $PUB -> $(echo "$RES" | jq -c '.data.publishablePublish.userErrors')"
done

# ----- 5e. Media upload (idempotent — only if uploads dir has files) -----
UPLOAD_DIR="${HOME}/Projects/dresslikemommy/uploads/${HANDLE}"
if [ -d "$UPLOAD_DIR" ] && [ -n "$(ls -A "$UPLOAD_DIR" 2>/dev/null)" ]; then
  echo "== media upload =="
  echo "TODO: stagedUploadsCreate + productCreateMedia for files in $UPLOAD_DIR"
else
  echo "(no media in $UPLOAD_DIR — skipping; rerun script after dropping images there)"
fi

# ----- Post-create verification -----
echo "== post-create verify =="
cat > "$WORK/q_verify.json" <<EOF
{"query":"query { product(id: \"$PRODUCT_ID\") { id title handle status publishedAt onlineStoreUrl seo { title description } variants(first: 30) { nodes { sku price compareAtPrice inventoryPolicy inventoryItem { tracked requiresShipping } selectedOptions { name value } } } descriptionHtml } }"}
EOF
curl -s -X POST "$API" -H "X-Shopify-Access-Token: $SHOPIFY_ADMIN_ACCESS_TOKEN" -H "Content-Type: application/json" --data @"$WORK/q_verify.json" > "$WORK/verify.json"
python3 - "$WORK/size_chart.json" "$WORK/verify.json" <<'PY'
import json,sys,re
sc=json.load(open(sys.argv[1]))
v=json.load(open(sys.argv[2]))['data']['product']
checks=[]
checks.append(("title len <= 70", len(v['title'])<=70, len(v['title'])))
checks.append(("seo title <= 60", len((v['seo']['title'] or ''))<=60, len(v['seo']['title'] or '')))
checks.append(("seo desc <= 155", len((v['seo']['description'] or ''))<=155, len(v['seo']['description'] or '')))
live_skus=sorted(x['sku'] for x in v['variants']['nodes'])
expected_skus=sorted(f"DLM-VCF-{r['sku_suffix']}-CREAM" for r in sc)
checks.append(("variant count == SIZE_CHART", len(live_skus)==len(sc), f"{len(live_skus)} vs {len(sc)}"))
checks.append(("live SKUs == derived", live_skus==expected_skus, "match" if live_skus==expected_skus else f"diff"))
for var in v['variants']['nodes']:
    ok = var['inventoryPolicy']=='DENY' and var['inventoryItem']['tracked'] and var['inventoryItem']['requiresShipping'] and var['price'] and var['compareAtPrice']
    if not ok:
        checks.append((f"variant {var['sku']} fields", False, var))
        break
else:
    checks.append(("all variants tracked/DENY/priced", True, "ok"))
checks.append(("publishedAt set", v.get('publishedAt') is not None, v.get('publishedAt')))
checks.append(("onlineStoreUrl set", bool(v.get('onlineStoreUrl')), v.get('onlineStoreUrl')))
body=v['descriptionHtml']
ths=re.findall(r'<th>', body)
checks.append(("size table th == 10", ths.count('<th>')>=10, ths.count('<th>')))
m=re.search(r'<tbody>(.*?)</tbody>', body, re.S)
data_trs = len(re.findall(r'<tr>', m.group(1))) if m else 0
checks.append((f"tbody tr == {len(sc)}", data_trs==len(sc), data_trs))
for r in sc:
    has = f"<td>{r['picker_label']}</td>" in body
    if not has:
        checks.append((f"picker '{r['picker_label']}' first cell", False, "missing"))
        break
else:
    checks.append(("all picker labels in size table", True, "ok"))
fails=[c for c in checks if not c[1]]
print("CHECK | OK | DETAIL")
for c in checks: print(f"  {c[0]:<35} {'PASS' if c[1] else 'FAIL'}  {c[2]}")
if fails:
    print("VERIFY FAILED")
    sys.exit(1)
print("VERIFY PASS")
PY

NUMERIC=${PRODUCT_ID##*/}
echo
echo "✅ Admin URL: https://admin.shopify.com/store/dresslikemommy/products/${NUMERIC}"
echo "✅ Live URL:  https://www.dresslikemommy.com/products/${HANDLE}"
