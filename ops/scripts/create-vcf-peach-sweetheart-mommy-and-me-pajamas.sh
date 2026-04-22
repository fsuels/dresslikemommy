#!/usr/bin/env bash
# Create + fully-configure Shopify product for:
#   Peach Sweetheart Mommy and Me Pajamas — Short-Sleeve Set
# Handle:   peach-sweetheart-mommy-and-me-pajamas
# Vendor:   dresslikemommy.com  (source: 1688 offer 920493992812)
# Category: Pajamas (Matching Family Pajamas)
# API ver:  2025-01
#
# Designs listed: Peach sweetheart-children's style, Peach sweetheart-adult style
# Vendor size chart: 1688 captcha-blocked direct fetch; user supplied 尺码参数
# screenshot — used as authoritative source for all 11 vendor rows.
#
# All 1/2 dimension columns from vendor are doubled to full circumference.
#
# Usage:  bash create-vcf-peach-sweetheart-mommy-and-me-pajamas.sh
set -euo pipefail

ENV_FILE="${SHOPIFY_ENV_FILE:-${HOME}/.config/dresslikemommy/shopify-admin.env}"
[[ -f "$ENV_FILE" ]] && source "$ENV_FILE"
: "${SHOPIFY_STORE_DOMAIN:?SHOPIFY_STORE_DOMAIN not set}"
: "${SHOPIFY_ADMIN_ACCESS_TOKEN:?SHOPIFY_ADMIN_ACCESS_TOKEN not set}"

API="https://${SHOPIFY_STORE_DOMAIN}/admin/api/2025-01/graphql.json"
H_TOKEN="X-Shopify-Access-Token: ${SHOPIFY_ADMIN_ACCESS_TOKEN}"
H_JSON="Content-Type: application/json"

gql() { curl -sS -X POST -H "$H_TOKEN" -H "$H_JSON" --data @"$1" "$API"; }

TMPDIR_LOCAL="$(mktemp -d)"
trap 'rm -rf "$TMPDIR_LOCAL"' EXIT

HANDLE="peach-sweetheart-mommy-and-me-pajamas"
TITLE="Peach Sweetheart Mommy and Me Pajamas — Short-Sleeve Set"
SEO_TITLE="Peach Mommy & Me Pajamas — Matching Set | Dress Like Mommy"
SEO_DESC="Shop our Peach Sweetheart matching mommy-and-me pajamas — soft cotton short-sleeve set for mom + daughter. Sizes 2Y–10Y, Mom S–XL."
VENDOR_URL="https://detail.1688.com/offer/920493992812.html"
SHORTCODE="VCF"
COLOR_TOKEN="CREAM"
COLOR_LABEL="Peach Sweetheart"
CHILD_PRICE="26.99"
MOTHER_PRICE="32.99"
CHILD_COMPARE="31.04"   # round_up(26.99*1.15,.99) = 31.04
MOTHER_COMPARE="37.99"  # round_up(32.99*1.15,.99) = 37.99

# ─────────────────────────────────────────────────────────────────────────────
# SIZE_CHART — single source of truth. ALL downstream payloads derive from this.
# Vendor 1/2胸围, 1/2臀围, 1/2腰围 are HALVES → already doubled here.
# ─────────────────────────────────────────────────────────────────────────────
cat > "$TMPDIR_LOCAL/size_chart.json" <<'JSON'
[
  {"audience":"child","vendor_label":"90", "picker_label":"Child 2 Years",   "sku_suffix":"KID2Y",  "age":"2",   "weight":"12–14 kg / 26–31 lbs",   "height":"85–95 cm / 33–37 in",   "chest_cm":60, "hip_cm":58, "waist_cm":42, "length_cm":33, "sleeve_cm":16.5, "pant_cm":27},
  {"audience":"child","vendor_label":"100","picker_label":"Child 3 Years",   "sku_suffix":"KID3Y",  "age":"3",   "weight":"14–16 kg / 31–35 lbs",   "height":"95–105 cm / 37–41 in",  "chest_cm":64, "hip_cm":62, "waist_cm":44, "length_cm":36, "sleeve_cm":17.5, "pant_cm":29.5},
  {"audience":"child","vendor_label":"110","picker_label":"Child 4 Years",   "sku_suffix":"KID4Y",  "age":"4",   "weight":"16–19 kg / 35–42 lbs",   "height":"105–115 cm / 41–45 in", "chest_cm":68, "hip_cm":66, "waist_cm":46, "length_cm":39, "sleeve_cm":19.5, "pant_cm":32},
  {"audience":"child","vendor_label":"120","picker_label":"Child 5 Years",   "sku_suffix":"KID5Y",  "age":"5",   "weight":"19–22 kg / 42–49 lbs",   "height":"115–125 cm / 45–49 in", "chest_cm":72, "hip_cm":70, "waist_cm":48, "length_cm":42, "sleeve_cm":21,   "pant_cm":34.5},
  {"audience":"child","vendor_label":"130","picker_label":"Child 6-7 Years", "sku_suffix":"KID67Y", "age":"6–7", "weight":"22–27 kg / 49–60 lbs",   "height":"125–135 cm / 49–53 in", "chest_cm":76, "hip_cm":74, "waist_cm":50, "length_cm":45, "sleeve_cm":22.5, "pant_cm":37},
  {"audience":"child","vendor_label":"140","picker_label":"Child 8 Years",   "sku_suffix":"KID8Y",  "age":"8",   "weight":"27–32 kg / 60–71 lbs",   "height":"135–145 cm / 53–57 in", "chest_cm":80, "hip_cm":78, "waist_cm":52, "length_cm":48, "sleeve_cm":24,   "pant_cm":39.5},
  {"audience":"child","vendor_label":"150","picker_label":"Child 9-10 Years","sku_suffix":"KID910Y","age":"9–10","weight":"32–38 kg / 71–84 lbs",  "height":"145–155 cm / 57–61 in", "chest_cm":84, "hip_cm":82, "waist_cm":54, "length_cm":51, "sleeve_cm":25.5, "pant_cm":42},
  {"audience":"mother","vendor_label":"S", "picker_label":"Mother S",       "sku_suffix":"MOMS",  "age":"—", "weight":"45–55 kg / 99–121 lbs",  "height":"155–162 cm / 61–64 in", "chest_cm":94, "hip_cm":104,"waist_cm":70, "length_cm":59, "sleeve_cm":21,   "pant_cm":45},
  {"audience":"mother","vendor_label":"M", "picker_label":"Mother M",       "sku_suffix":"MOMM",  "age":"—", "weight":"55–62 kg / 121–137 lbs", "height":"160–167 cm / 63–66 in", "chest_cm":98, "hip_cm":108,"waist_cm":72, "length_cm":60, "sleeve_cm":22,   "pant_cm":46},
  {"audience":"mother","vendor_label":"L", "picker_label":"Mother L",       "sku_suffix":"MOML",  "age":"—", "weight":"62–70 kg / 137–154 lbs", "height":"165–172 cm / 65–68 in", "chest_cm":102,"hip_cm":112,"waist_cm":74, "length_cm":61, "sleeve_cm":23,   "pant_cm":47},
  {"audience":"mother","vendor_label":"XL","picker_label":"Mother XL",      "sku_suffix":"MOMXL", "age":"—", "weight":"70–78 kg / 154–172 lbs", "height":"170–177 cm / 67–70 in", "chest_cm":106,"hip_cm":116,"waist_cm":76, "length_cm":62, "sleeve_cm":24,   "pant_cm":48}
]
JSON

# ─────────────────────────────────────────────────────────────────────────────
# Preflight guards (halt before any API call)
# ─────────────────────────────────────────────────────────────────────────────
echo "==> Preflight: validate SIZE_CHART"
ROW_COUNT=$(jq 'length' "$TMPDIR_LOCAL/size_chart.json")
echo "  rows: $ROW_COUNT"
if [[ "$ROW_COUNT" -ne 11 ]]; then echo "FATAL: expected 11 rows"; exit 1; fi

# Required-field validation
jq -e 'all(.[]; .audience and .vendor_label and .picker_label and .sku_suffix and .age and .weight and .height and (.chest_cm|type=="number") and (.hip_cm|type=="number") and (.waist_cm|type=="number") and (.length_cm|type=="number"))' \
  "$TMPDIR_LOCAL/size_chart.json" > /dev/null || { echo "FATAL: missing required fields"; exit 1; }
echo "  ✓ all rows have required fields (incl waist_cm)"

# Duplicate picker_label check
DUPES=$(jq -r '[.[].picker_label] | group_by(.) | map(select(length>1)) | length' "$TMPDIR_LOCAL/size_chart.json")
if [[ "$DUPES" -ne 0 ]]; then echo "FATAL: duplicate picker_label"; exit 1; fi
echo "  ✓ picker_labels unique"

# Title/SEO length checks
[[ ${#TITLE}    -le 70 ]]  || { echo "FATAL: title $((${#TITLE})) > 70";    exit 1; }
[[ ${#SEO_TITLE} -le 60 ]] || { echo "FATAL: seo_title $((${#SEO_TITLE})) > 60"; exit 1; }
[[ ${#SEO_DESC}  -le 155 ]] || { echo "FATAL: seo_desc $((${#SEO_DESC})) > 155"; exit 1; }
echo "  ✓ title=${#TITLE}, seo_title=${#SEO_TITLE}, seo_desc=${#SEO_DESC}"

# ─────────────────────────────────────────────────────────────────────────────
# Derive: productOptions.Size.values
# ─────────────────────────────────────────────────────────────────────────────
SIZE_VALUES=$(jq -c '[.[] | {name: .picker_label}]' "$TMPDIR_LOCAL/size_chart.json")
echo "  size values: $SIZE_VALUES"

# ─────────────────────────────────────────────────────────────────────────────
# Derive: body HTML size table (10 columns) — first cell = picker_label
# Columns: Size | Age | Weight | Height | Chest/Bust | Sleeve | — | Hip | Waist | Garment Length
# ─────────────────────────────────────────────────────────────────────────────
fmt_dual_cm() {
  local v="$1"; awk -v c="$v" 'BEGIN{printf "%g cm / %.1f in", c, c/2.54}'
}
build_size_table_rows() {
  local out=""
  local last_audience=""
  local i=0
  local n
  n=$(jq 'length' "$TMPDIR_LOCAL/size_chart.json")
  while [[ $i -lt $n ]]; do
    local row aud picker age weight height chest hip waist length sleeve
    row=$(jq -c ".[$i]" "$TMPDIR_LOCAL/size_chart.json")
    aud=$(echo "$row" | jq -r '.audience')
    picker=$(echo "$row" | jq -r '.picker_label')
    age=$(echo "$row" | jq -r '.age')
    weight=$(echo "$row" | jq -r '.weight')
    height=$(echo "$row" | jq -r '.height')
    chest=$(echo "$row" | jq -r '.chest_cm')
    hip=$(echo "$row" | jq -r '.hip_cm')
    waist=$(echo "$row" | jq -r '.waist_cm')
    length=$(echo "$row" | jq -r '.length_cm')
    sleeve=$(echo "$row" | jq -r '.sleeve_cm')

    if [[ "$aud" != "$last_audience" ]]; then
      if [[ "$aud" == "child" ]]; then
        out+="    <!-- Children Sizes -->"$'\n'
      else
        out+="    <!-- Adult Sizes -->"$'\n'
      fi
      last_audience="$aud"
    fi
    out+="    <tr><td>${picker}</td><td>${age}</td><td>${weight}</td><td>${height}</td><td>$(fmt_dual_cm $chest)</td><td>$(fmt_dual_cm $sleeve)</td><td>—</td><td>$(fmt_dual_cm $hip)</td><td>$(fmt_dual_cm $waist)</td><td>$(fmt_dual_cm $length)</td></tr>"$'\n'
    i=$((i+1))
  done
  printf '%s' "$out"
}
SIZE_TABLE_ROWS=$(build_size_table_rows)

# ─────────────────────────────────────────────────────────────────────────────
# Derive: tags (mother-size tags only for vendor's actual mother labels)
# ─────────────────────────────────────────────────────────────────────────────
MOTHER_SIZE_TAGS=()
while IFS= read -r ml; do
  case "$ml" in
    "Mother S")  MOTHER_SIZE_TAGS+=("Mother S");;
    "Mother M")  MOTHER_SIZE_TAGS+=("Mother M");;
    "Mother L")  MOTHER_SIZE_TAGS+=("Mother L");;
    "Mother XL") MOTHER_SIZE_TAGS+=("Mother XL");;
  esac
done < <(jq -r '.[] | select(.audience=="mother") | .picker_label' "$TMPDIR_LOCAL/size_chart.json")

# Child age buckets (only those covered by SIZE_CHART kid rows)
CHILD_BUCKETS=()
HAS_23=$(jq '[.[] | select(.audience=="child" and (.picker_label=="Child 2 Years" or .picker_label=="Child 3 Years"))] | length' "$TMPDIR_LOCAL/size_chart.json")
HAS_45=$(jq '[.[] | select(.audience=="child" and (.picker_label=="Child 4 Years" or .picker_label=="Child 5 Years"))] | length' "$TMPDIR_LOCAL/size_chart.json")
HAS_68=$(jq '[.[] | select(.audience=="child" and (.picker_label=="Child 6-7 Years" or .picker_label=="Child 8 Years"))] | length' "$TMPDIR_LOCAL/size_chart.json")
HAS_910=$(jq '[.[] | select(.audience=="child" and .picker_label=="Child 9-10 Years")] | length' "$TMPDIR_LOCAL/size_chart.json")
[[ $HAS_23  -gt 0 ]] && CHILD_BUCKETS+=("Child 2-3yr")
[[ $HAS_45  -gt 0 ]] && CHILD_BUCKETS+=("Child 4-5yr")
[[ $HAS_68  -gt 0 ]] && CHILD_BUCKETS+=("Child 6-8yr")
[[ $HAS_910 -gt 0 ]] && CHILD_BUCKETS+=("Child 9-10yr")

# ─────────────────────────────────────────────────────────────────────────────
# Derive: shopify.size GIDs — canonical map
# ─────────────────────────────────────────────────────────────────────────────
declare -A SIZE_GID_MAP=(
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
SIZE_GIDS_JSON=$(
  jq -r '.[].picker_label' "$TMPDIR_LOCAL/size_chart.json" \
  | while read -r pl; do echo "${SIZE_GID_MAP[$pl]:-}"; done \
  | grep -v '^$' | jq -R . | jq -sc .
)

# ─────────────────────────────────────────────────────────────────────────────
# Build description HTML
# ─────────────────────────────────────────────────────────────────────────────
SIZE_RANGE_BULLET="Sizes Child 2 Years through 9–10 Years and Mother S–XL — see chart"

cat > "$TMPDIR_LOCAL/description.html" <<HTMLEOF
<ul>
  <li><strong>Fabric:</strong> Soft cotton blend — breathable, gentle on skin, light enough for warm nights.</li>
  <li><strong>Family Story:</strong> A picture-perfect mommy-and-me sleep set built for snuggles, story-time, and Sunday-morning pancakes.</li>
  <li><strong>Print:</strong> Sweet hand-painted peaches and leafy sprigs scattered on a creamy ivory ground, framed with soft blush sleeves.</li>
  <li><strong>Design Details:</strong> Round neck, short raglan sleeves, relaxed pull-on shorts with a covered elastic waist — coordinating mom and daughter cuts.</li>
  <li><strong>Care:</strong> Machine wash cold with like colors, tumble dry low, do not bleach, warm iron if needed.</li>
  <li><strong>Size Range:</strong> ${SIZE_RANGE_BULLET}.</li>
</ul>

<h3>Size Chart</h3>
<table id="size-chart">
  <thead>
    <tr><th>Size</th><th>Age</th><th>Weight</th><th>Height</th><th>Chest/Bust</th><th>Sleeve</th><th>—</th><th>Hip</th><th>Waist</th><th>Garment Length</th></tr>
  </thead>
  <tbody>
${SIZE_TABLE_ROWS}  </tbody>
</table>

<p>Meet our Peach Sweetheart pajama set — a warm-weather mommy-and-me favorite in the softest cotton blend. The relaxed short-sleeve top and easy pull-on shorts move with busy mornings and lazy afternoons, while the matching mom and daughter cuts make every moment match. From cozy bedtime routines to brunch in pajamas, this set is built to be loved in.</p>

<p>The print is all heart: tumbling watercolor peaches, leafy little sprigs, and that fresh-from-the-orchard sweetness on a creamy ivory ground. Soft blush sleeves and shorts pick up the peach blossom blush, finished with covered elastic waists and gently rolled hems. Pair it for picture-perfect family photos, holiday cards, summer birthdays — or just because matching is more fun.</p>

<h3>Key Features:</h3>
<ul>
  <li><strong>Soft Cotton Blend:</strong> Breathable, lightweight, easy on little skin.</li>
  <li><strong>Matching Mom + Daughter Cuts:</strong> Coordinated proportions, picture-ready in every size.</li>
  <li><strong>Easy Pull-On Shorts:</strong> Covered elastic waist for all-night comfort.</li>
  <li><strong>Hand-Painted Peach Print:</strong> Sweet seasonal motifs on a creamy ivory base.</li>
  <li><strong>Family Sizing:</strong> Sized from Child 2 Years through Mother XL.</li>
</ul>

<p>Make every moment match — slip into the Peach Sweetheart set and let the cuddles begin.</p>
HTMLEOF

# ─────────────────────────────────────────────────────────────────────────────
# 5a. productCreate
# ─────────────────────────────────────────────────────────────────────────────
TAGS_JSON=$(python3 -c "
import json
tags=['Mommy and Me','Pajamas','Matching Family Pajamas','Short Sleeve Pajamas','Summer',
      'Cream','Ivory','Pink','Peach','Peach Sweetheart','Fruit','Floral','Watercolor',
      'Cotton','Cotton Blend','Loungewear']
tags += ['$(IFS=,; echo \"${CHILD_BUCKETS[*]}\")'.split(',')] if False else []
tags += '${CHILD_BUCKETS[*]}'.split() if False else []
" 2>/dev/null || true)

# Build tags via python for safety
python3 - "$TMPDIR_LOCAL/size_chart.json" "$VENDOR_URL" > "$TMPDIR_LOCAL/tags.json" <<PY
import json, sys
sc=json.load(open(sys.argv[1])); vurl=sys.argv[2]
mother_pickers=[r['picker_label'] for r in sc if r['audience']=='mother']
child_pickers =[r['picker_label'] for r in sc if r['audience']=='child']
buckets=[]
if any(p in ('Child 2 Years','Child 3 Years') for p in child_pickers): buckets.append('Child 2-3yr')
if any(p in ('Child 4 Years','Child 5 Years') for p in child_pickers): buckets.append('Child 4-5yr')
if any(p in ('Child 6-7 Years','Child 8 Years') for p in child_pickers): buckets.append('Child 6-8yr')
if any(p == 'Child 9-10 Years' for p in child_pickers): buckets.append('Child 9-10yr')
tags=['Mommy and Me','Pajamas','Matching Family Pajamas','Short Sleeve Pajamas','Summer',
      'Cream','Ivory','Pink','Peach','Peach Sweetheart','Fruit','Watercolor',
      'Cotton','Cotton Blend','Loungewear']
tags += buckets
tags += [m for m in ('Mother S','Mother M','Mother L','Mother XL') if m in mother_pickers]
tags.append(vurl)
json.dump(tags, sys.stdout)
PY

python3 - "$TMPDIR_LOCAL/description.html" "$TMPDIR_LOCAL/tags.json" "$TITLE" "$HANDLE" "$SEO_TITLE" "$SEO_DESC" "$SIZE_VALUES" "$COLOR_LABEL" > "$TMPDIR_LOCAL/productCreate.json" <<'PY'
import json, sys
desc=open(sys.argv[1]).read()
tags=json.load(open(sys.argv[2]))
title, handle, seo_title, seo_desc, size_values_json, color_label = sys.argv[3:]
size_values=json.loads(size_values_json)
body = {
  "query": "mutation productCreate($product: ProductCreateInput!) { productCreate(product: $product) { product { id handle title } userErrors { field message } } }",
  "variables": { "product": {
    "title": title, "handle": handle, "vendor": "dresslikemommy.com",
    "productType": "Matching Family Pajamas", "status": "ACTIVE",
    "category": "gid://shopify/TaxonomyCategory/aa-1-17-4",
    "descriptionHtml": desc,
    "seo": { "title": seo_title, "description": seo_desc },
    "tags": tags,
    "productOptions": [
      { "name": "Size", "values": size_values },
      { "name": "Color", "values": [ { "name": color_label } ] }
    ]
  }}
}
json.dump(body, sys.stdout)
PY

echo "==> productCreate"
PRESP="$(gql "$TMPDIR_LOCAL/productCreate.json")"
echo "$PRESP" | python3 -c "import json,sys;d=json.load(sys.stdin);print(json.dumps(d.get('data',{}).get('productCreate',{}),indent=2)[:1200])"
PRODUCT_ID=$(echo "$PRESP" | python3 -c "import json,sys;d=json.load(sys.stdin);print(d['data']['productCreate']['product']['id'])")
echo "PRODUCT_ID=$PRODUCT_ID"
[[ -z "$PRODUCT_ID" || "$PRODUCT_ID" == "None" ]] && { echo "FATAL: productCreate failed"; exit 1; }

# ─────────────────────────────────────────────────────────────────────────────
# 5b. productVariantsBulkCreate
# ─────────────────────────────────────────────────────────────────────────────
python3 - "$PRODUCT_ID" "$TMPDIR_LOCAL/size_chart.json" "$SHORTCODE" "$COLOR_TOKEN" "$COLOR_LABEL" "$CHILD_PRICE" "$MOTHER_PRICE" "$CHILD_COMPARE" "$MOTHER_COMPARE" > "$TMPDIR_LOCAL/variantsCreate.json" <<'PY'
import json, sys
pid, scfile, shortcode, color_token, color_label, cp, mp, cc, mc = sys.argv[1:]
sc=json.load(open(scfile))
variants=[]
for r in sc:
  is_mom = r['audience']=='mother'
  price = mp if is_mom else cp
  cmp_at = mc if is_mom else cc
  sku = f"DLM-{shortcode}-{r['sku_suffix']}-{color_token}"
  variants.append({
    "price": price,
    "compareAtPrice": cmp_at,
    "inventoryItem": {"sku": sku, "tracked": True, "requiresShipping": True},
    "inventoryPolicy": "DENY",
    "optionValues": [
      {"optionName":"Size","name":r['picker_label']},
      {"optionName":"Color","name":color_label}
    ]
  })
body={
  "query":"mutation v($pid:ID!,$variants:[ProductVariantsBulkInput!]!,$strategy:ProductVariantsBulkCreateStrategy){ productVariantsBulkCreate(productId:$pid,variants:$variants,strategy:$strategy){ productVariants{ id sku price compareAtPrice inventoryPolicy } userErrors{ field message } } }",
  "variables":{"pid":pid,"variants":variants,"strategy":"REMOVE_STANDALONE_VARIANT"}
}
json.dump(body,sys.stdout)
PY

echo "==> productVariantsBulkCreate"
VRESP="$(gql "$TMPDIR_LOCAL/variantsCreate.json")"
echo "$VRESP" | python3 -c "import json,sys;d=json.load(sys.stdin);print(json.dumps(d.get('data',{}).get('productVariantsBulkCreate',{}),indent=2)[:2000])"

# ─────────────────────────────────────────────────────────────────────────────
# 5c. metafieldsSet
# ─────────────────────────────────────────────────────────────────────────────
python3 - "$PRODUCT_ID" "$TMPDIR_LOCAL/size_chart.json" "$SEO_TITLE" "$SEO_DESC" > "$TMPDIR_LOCAL/metafieldsSet.json" <<'PY'
import json, sys
pid, scfile, seo_title, seo_desc = sys.argv[1:]
sc=json.load(open(scfile))

# canonical maps
SIZE_GID = {
  "Child 2 Years":"gid://shopify/Metaobject/129972863073",
  "Child 3 Years":"gid://shopify/Metaobject/129972895841",
  "Child 4 Years":"gid://shopify/Metaobject/129972928609",
  "Child 5 Years":"gid://shopify/Metaobject/129972961377",
  "Child 6-7 Years":"gid://shopify/Metaobject/139840323681",
  "Child 8 Years":"gid://shopify/Metaobject/139840356449",
  "Child 9-10 Years":"gid://shopify/Metaobject/139840389217",
  "Mother S":"gid://shopify/Metaobject/129975255137",
  "Mother M":"gid://shopify/Metaobject/129975222369",
  "Mother L":"gid://shopify/Metaobject/129975189601",
  "Mother XL":"gid://shopify/Metaobject/129975287905",
}
COLOR_GID = {
  "Beige":"gid://shopify/Metaobject/69641928801",
  "Pink":"gid://shopify/Metaobject/69963645025",
  "Floral":"gid://shopify/Metaobject/129971519585",
}
FABRIC_COTTON = "gid://shopify/Metaobject/69622399073"
TG_FEMALE     = "gid://shopify/Metaobject/129971617889"
AG_KIDS       = "gid://shopify/Metaobject/128116523105"
AG_ADULTS     = "gid://shopify/Metaobject/128116490337"

size_gids   = [SIZE_GID[r['picker_label']] for r in sc if r['picker_label'] in SIZE_GID]
ag_gids     = []
if any(r['audience']=='child'  for r in sc): ag_gids.append(AG_KIDS)
if any(r['audience']=='mother' for r in sc): ag_gids.append(AG_ADULTS)

mfs = [
  ["custom","category1","single_line_text_field","Mommy and Me"],
  ["custom","subcategory","single_line_text_field","Pajamas"],
  ["custom","subcategory2","single_line_text_field","Summer Pajamas"],
  ["custom","pattern","single_line_text_field","Peach Sweetheart watercolor peach print"],
  ["custom","style","single_line_text_field","Matching Family Set"],
  ["custom","type","single_line_text_field","Two-Piece Pajama Set"],
  ["mm-google-shopping","custom_product","boolean","false"],
  ["mm-google-shopping","gender","single_line_text_field","female"],
  ["mm-google-shopping","age_group","single_line_text_field","adult"],
  ["mm-google-shopping","condition","single_line_text_field","new"],
  ["mm-google-shopping","custom_label_0","single_line_text_field","Mommy and Me"],
  ["mm-google-shopping","custom_label_1","single_line_text_field","Peach Fruit Print"],
  ["mm-google-shopping","custom_label_2","single_line_text_field","Summer"],
  ["mm-google-shopping","custom_label_3","single_line_text_field","Short Sleeve"],
  ["mm-google-shopping","custom_label_4","single_line_text_field","Family Matching"],
  ["shopify","age-group","list.metaobject_reference", json.dumps(ag_gids)],
  ["shopify","color-pattern","list.metaobject_reference", json.dumps([COLOR_GID["Beige"], COLOR_GID["Pink"], COLOR_GID["Floral"]])],
  ["shopify","fabric","list.metaobject_reference", json.dumps([FABRIC_COTTON])],
  ["shopify","size","list.metaobject_reference", json.dumps(size_gids)],
  ["shopify","target-gender","list.metaobject_reference", json.dumps([TG_FEMALE])],
  ["global","title_tag","single_line_text_field", seo_title],
  ["global","description_tag","single_line_text_field", seo_desc],
]
# Note: shopify.sleeve-length-type is OMITTED for Pajamas per category-skip rule.
# shopify.clothing-features OMITTED — catalog only has "Insulated", which doesn't
# honestly fit a summer cotton pajama set.

metas=[{"ownerId":pid,"namespace":ns,"key":k,"type":t,"value":v} for ns,k,t,v in mfs]
body={
  "query":"mutation metafieldsSet($metafields: [MetafieldsSetInput!]!) { metafieldsSet(metafields: $metafields) { metafields { id namespace key type value } userErrors { field message } } }",
  "variables":{"metafields":metas}
}
json.dump(body,sys.stdout)
PY

echo "==> metafieldsSet"
MFRESP="$(gql "$TMPDIR_LOCAL/metafieldsSet.json")"
echo "$MFRESP" | python3 -c "import json,sys;d=json.load(sys.stdin);ue=d.get('data',{}).get('metafieldsSet',{}).get('userErrors',[]);mfs=d.get('data',{}).get('metafieldsSet',{}).get('metafields',[]);print('wrote',len(mfs),'metafields');[print(' -',m['namespace']+'.'+m['key'],'=',str(m['value'])[:80]) for m in mfs];print('userErrors:',ue)"

# ─────────────────────────────────────────────────────────────────────────────
# 5d. publishablePublish (5 channels)
# ─────────────────────────────────────────────────────────────────────────────
echo "==> publishablePublish"
for PUB in \
  "gid://shopify/Publication/55169925" \
  "gid://shopify/Publication/21969633377" \
  "gid://shopify/Publication/29172400225" \
  "gid://shopify/Publication/76582879329" \
  "gid://shopify/Publication/76604768353"; do
  cat > "$TMPDIR_LOCAL/pub.json" <<EOF
{"query":"mutation pub(\$id:ID!,\$input:[PublicationInput!]!){ publishablePublish(id:\$id, input:\$input){ userErrors{ field message } } }","variables":{"id":"$PRODUCT_ID","input":[{"publicationId":"$PUB"}]}}
EOF
  RES="$(gql "$TMPDIR_LOCAL/pub.json")"
  echo "  $PUB -> $(echo "$RES" | python3 -c "import json,sys;d=json.load(sys.stdin);print(d.get('data',{}).get('publishablePublish',{}).get('userErrors',[]) or 'ok')")"
done

# ─────────────────────────────────────────────────────────────────────────────
# 5e. Media — only if uploads exist
# ─────────────────────────────────────────────────────────────────────────────
UPLOAD_DIR="${HOME}/Projects/dresslikemommy/uploads/peach-sweetheart-mommy-and-me-pajamas"
if [[ -d "$UPLOAD_DIR" ]] && compgen -G "$UPLOAD_DIR/*" > /dev/null; then
  echo "==> media upload (TODO if needed)"
else
  echo "==> media: no images at $UPLOAD_DIR — skipping (manual follow-up)"
fi

# ─────────────────────────────────────────────────────────────────────────────
# Post-create verification
# ─────────────────────────────────────────────────────────────────────────────
echo "==> verify"
cat > "$TMPDIR_LOCAL/verify.json" <<EOF
{"query":"query(\$id:ID!){ product(id:\$id){ id title handle onlineStoreUrl publishedAt status descriptionHtml variants(first:50){ nodes{ sku price compareAtPrice inventoryPolicy inventoryItem{ tracked requiresShipping } selectedOptions{ name value } } } } }","variables":{"id":"$PRODUCT_ID"}}
EOF
VRESP="$(gql "$TMPDIR_LOCAL/verify.json")"
echo "$VRESP" > "$TMPDIR_LOCAL/verify.out.json"

python3 - "$TMPDIR_LOCAL/verify.out.json" "$TMPDIR_LOCAL/size_chart.json" "$SHORTCODE" "$COLOR_TOKEN" <<'PY'
import json, sys, re
v=json.load(open(sys.argv[1]))['data']['product']
sc=json.load(open(sys.argv[2]))
shortcode, color_token = sys.argv[3:]
print(f"  title={v['title']}")
print(f"  handle={v['handle']}")
print(f"  status={v['status']}  publishedAt={v['publishedAt']}")
print(f"  onlineStoreUrl={v['onlineStoreUrl']}")
live_skus = sorted(n['sku'] for n in v['variants']['nodes'])
derived = sorted(f"DLM-{shortcode}-{r['sku_suffix']}-{color_token}" for r in sc)
print(f"  live variant count: {len(live_skus)}  expected: {len(sc)}")
assert len(live_skus)==len(sc), "FATAL: variant count mismatch"
assert live_skus==derived, f"FATAL: SKU mismatch\nlive={live_skus}\nderived={derived}"
print("  ✓ SKUs match")
desc=v['descriptionHtml']
tr_count=len(re.findall(r'<tr>', desc))
# tr_count includes header; data rows = tr_count - 1
data_rows = tr_count - 1
th_count = len(re.findall(r'<th>', desc))
print(f"  body size table: data_rows={data_rows} (expected {len(sc)})  th_count={th_count} (expected 10)")
assert data_rows==len(sc), "FATAL: size table row count mismatch"
assert th_count==10, "FATAL: size table column count mismatch"
print("  ✓ size table 10 cols, correct row count")
for n in v['variants']['nodes']:
  ip=n.get('inventoryPolicy'); inv=n.get('inventoryItem',{})
  assert ip=='DENY' and inv.get('tracked') and inv.get('requiresShipping'), f"FATAL: variant policy: {n}"
print("  ✓ all variants DENY/tracked/requiresShipping")
print(f"\nADMIN_URL=https://admin.shopify.com/store/dresslikemommy/products/{v['id'].split('/')[-1]}")
print(f"LIVE_URL=https://www.dresslikemommy.com/products/{v['handle']}")
PY

echo "==> DONE"
