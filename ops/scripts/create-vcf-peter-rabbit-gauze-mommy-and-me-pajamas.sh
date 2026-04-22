#!/usr/bin/env bash
# Create + fully-configure Shopify product for:
#   Peter Rabbit Gauze Mommy and Me Pajamas — Long-Sleeve Set
# Handle:   peter-rabbit-gauze-mommy-and-me-pajamas
# Vendor:   dresslikemommy.com  (source: 1688 offer 828526529351)
# Category: Pajamas (Matching Family Pajamas)
# API ver:  2025-01
#
# Single-source-of-truth SIZE_CHART JSON declared once at top.
# productOptions, variants, tags, body-HTML size table, shopify.size
# metafield, and SEO description are all derived from it.
#
# Usage:  bash create-vcf-peter-rabbit-gauze-mommy-and-me-pajamas.sh
# Requires env file: /Users/fsuels/.config/dresslikemommy/shopify-admin.env
set -euo pipefail

ENV_FILE="${SHOPIFY_ENV_FILE:-${HOME}/.config/dresslikemommy/shopify-admin.env}"
if [[ -f "$ENV_FILE" ]]; then
  # shellcheck disable=SC1090
  source "$ENV_FILE"
fi
: "${SHOPIFY_STORE_DOMAIN:?SHOPIFY_STORE_DOMAIN not set}"
: "${SHOPIFY_ADMIN_ACCESS_TOKEN:?SHOPIFY_ADMIN_ACCESS_TOKEN not set}"

API="https://${SHOPIFY_STORE_DOMAIN}/admin/api/2025-01/graphql.json"
H_TOKEN="X-Shopify-Access-Token: ${SHOPIFY_ADMIN_ACCESS_TOKEN}"
H_JSON="Content-Type: application/json"

gql() {
  # $1 = JSON body file path
  curl -sS -X POST -H "$H_TOKEN" -H "$H_JSON" --data @"$1" "$API"
}

TMPDIR_LOCAL="$(mktemp -d)"
trap 'rm -rf "$TMPDIR_LOCAL"' EXIT

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# -------------------------------------------------------------------
# SIZE_CHART — the ONLY place variants are defined
# 11 rows: 7 kid (90/100/110/120/130/140/150) + 4 mother (S/M/L/XL)
# Chest/Hip/Waist already doubled from vendor's 1/2 columns.
# -------------------------------------------------------------------
cat > "$TMPDIR_LOCAL/SIZE_CHART.json" <<'JSON'
[
  {"audience":"child","vendor_label":"90","picker_label":"Child 2 Years","sku_suffix":"KID2Y","age":"2","weight":"12–14 kg / 26–31 lbs","height":"85–95 cm / 33–37 in","chest_cm":68,"hip_cm":69,"waist_cm":43,"length_cm":41,"shoulder_cm":27,"sleeve_cm":33,"pant_cm":53,"size_metaobject_gid":"gid://shopify/Metaobject/129972863073","price":"35.99","compare_at":"41.49","weight_grams":320},
  {"audience":"child","vendor_label":"100","picker_label":"Child 3 Years","sku_suffix":"KID3Y","age":"3","weight":"14–16 kg / 31–35 lbs","height":"95–105 cm / 37–41 in","chest_cm":72,"hip_cm":73,"waist_cm":45,"length_cm":44,"shoulder_cm":28.5,"sleeve_cm":36,"pant_cm":58,"size_metaobject_gid":"gid://shopify/Metaobject/129972895841","price":"35.99","compare_at":"41.49","weight_grams":360},
  {"audience":"child","vendor_label":"110","picker_label":"Child 4 Years","sku_suffix":"KID4Y","age":"4","weight":"16–19 kg / 35–42 lbs","height":"105–115 cm / 41–45 in","chest_cm":76,"hip_cm":77,"waist_cm":47,"length_cm":47,"shoulder_cm":30,"sleeve_cm":39,"pant_cm":63,"size_metaobject_gid":"gid://shopify/Metaobject/129972928609","price":"35.99","compare_at":"41.49","weight_grams":400},
  {"audience":"child","vendor_label":"120","picker_label":"Child 5 Years","sku_suffix":"KID5Y","age":"5","weight":"19–22 kg / 42–49 lbs","height":"115–125 cm / 45–49 in","chest_cm":80,"hip_cm":81,"waist_cm":49,"length_cm":50,"shoulder_cm":31.5,"sleeve_cm":42,"pant_cm":68,"size_metaobject_gid":"gid://shopify/Metaobject/129972961377","price":"35.99","compare_at":"41.49","weight_grams":440},
  {"audience":"child","vendor_label":"130","picker_label":"Child 6-7 Years","sku_suffix":"KID67Y","age":"6–7","weight":"22–26 kg / 49–57 lbs","height":"125–135 cm / 49–53 in","chest_cm":84,"hip_cm":85,"waist_cm":52,"length_cm":53,"shoulder_cm":33,"sleeve_cm":45,"pant_cm":73,"size_metaobject_gid":"gid://shopify/Metaobject/139840323681","price":"35.99","compare_at":"41.49","weight_grams":480},
  {"audience":"child","vendor_label":"140","picker_label":"Child 8 Years","sku_suffix":"KID8Y","age":"8","weight":"26–30 kg / 57–66 lbs","height":"135–145 cm / 53–57 in","chest_cm":88,"hip_cm":89,"waist_cm":55,"length_cm":56,"shoulder_cm":34.5,"sleeve_cm":48,"pant_cm":78,"size_metaobject_gid":"gid://shopify/Metaobject/139840356449","price":"35.99","compare_at":"41.49","weight_grams":520},
  {"audience":"child","vendor_label":"150","picker_label":"Child 9-10 Years","sku_suffix":"KID910Y","age":"9–10","weight":"30–36 kg / 66–79 lbs","height":"145–155 cm / 57–61 in","chest_cm":92,"hip_cm":93,"waist_cm":57,"length_cm":59,"shoulder_cm":36,"sleeve_cm":51,"pant_cm":83,"size_metaobject_gid":"gid://shopify/Metaobject/139840389217","price":"35.99","compare_at":"41.49","weight_grams":560},
  {"audience":"mother","vendor_label":"S","picker_label":"Mother S","sku_suffix":"MOMS","age":"—","weight":"48–55 kg / 106–121 lbs","height":"155–163 cm / 61–64 in","chest_cm":106,"hip_cm":111,"waist_cm":73,"length_cm":66,"shoulder_cm":40.5,"sleeve_cm":54,"pant_cm":97,"size_metaobject_gid":"gid://shopify/Metaobject/129975255137","price":"39.99","compare_at":"45.99","weight_grams":700},
  {"audience":"mother","vendor_label":"M","picker_label":"Mother M","sku_suffix":"MOMM","age":"—","weight":"55–62 kg / 121–137 lbs","height":"160–168 cm / 63–66 in","chest_cm":110,"hip_cm":115,"waist_cm":75,"length_cm":69,"shoulder_cm":42,"sleeve_cm":54,"pant_cm":99,"size_metaobject_gid":"gid://shopify/Metaobject/129975222369","price":"39.99","compare_at":"45.99","weight_grams":740},
  {"audience":"mother","vendor_label":"L","picker_label":"Mother L","sku_suffix":"MOML","age":"—","weight":"62–70 kg / 137–154 lbs","height":"163–170 cm / 64–67 in","chest_cm":114,"hip_cm":119,"waist_cm":77,"length_cm":71,"shoulder_cm":43.5,"sleeve_cm":54,"pant_cm":102,"size_metaobject_gid":"gid://shopify/Metaobject/129975189601","price":"39.99","compare_at":"45.99","weight_grams":780},
  {"audience":"mother","vendor_label":"XL","picker_label":"Mother XL","sku_suffix":"MOMXL","age":"—","weight":"70–78 kg / 154–172 lbs","height":"168–175 cm / 66–69 in","chest_cm":116,"hip_cm":123,"waist_cm":80,"length_cm":73,"shoulder_cm":45,"sleeve_cm":54,"pant_cm":103,"size_metaobject_gid":"gid://shopify/Metaobject/129975287905","price":"39.99","compare_at":"45.99","weight_grams":820}
]
JSON

# -------------------------------------------------------------------
# Static listing fields (Title, SEO, color token, etc.)
# -------------------------------------------------------------------
PRODUCT_TITLE='Peter Rabbit Gauze Mommy and Me Pajamas — Long-Sleeve Set'
PRODUCT_HANDLE='peter-rabbit-gauze-mommy-and-me-pajamas'
SEO_TITLE='Peter Rabbit Mommy & Me Pajamas — Gauze | Dress Like Mommy'
SEO_DESC='Shop our Peter Rabbit matching mommy-and-me pajamas — cotton gauze long-sleeve sets for mom + daughter. Sizes 2Y–10Y & Mom S–XL.'
COLOR_NAME='Peter Rabbit Meadow'
COLOR_TOKEN='CREAM'
SHORTCODE='VCF'
VENDOR_URL='https://detail.1688.com/offer/828526529351.html'
DESC_HTML_FILE="$SCRIPT_DIR/peter-rabbit-gauze-description.html"

# -------------------------------------------------------------------
# PREFLIGHT GUARDS — halt before any API call on any inconsistency
# -------------------------------------------------------------------
jq -e 'all(.[]; .audience and .vendor_label and .picker_label and .sku_suffix and .age and .weight and .height and .chest_cm and .hip_cm and .waist_cm and .length_cm)' \
   "$TMPDIR_LOCAL/SIZE_CHART.json" > /dev/null \
   || { echo "PREFLIGHT FAILED: a SIZE_CHART row is missing a required field"; exit 1; }

python3 - "$TMPDIR_LOCAL/SIZE_CHART.json" "$PRODUCT_TITLE" "$SEO_TITLE" "$SEO_DESC" "$DESC_HTML_FILE" "$SHORTCODE" "$COLOR_TOKEN" <<'PY'
import json, sys, os, re
chart_path, title, seo_t, seo_d, desc_path, shortcode, color_token = sys.argv[1:8]
chart = json.load(open(chart_path))

errors = []
required = ["audience","vendor_label","picker_label","sku_suffix","age","weight","height","chest_cm","hip_cm","waist_cm","length_cm","price","compare_at"]
for i, row in enumerate(chart):
    for k in required:
        if k not in row or row[k] in (None, ""):
            errors.append(f"row {i} missing {k}")
labels = [r["picker_label"] for r in chart]
if len(labels) != len(set(labels)):
    errors.append(f"duplicate picker_label in chart: {labels}")
if len(title) > 70: errors.append(f"TITLE>70 ({len(title)}): {title}")
if len(seo_t) > 60: errors.append(f"SEO_TITLE>60 ({len(seo_t)}): {seo_t}")
if len(seo_d) > 155: errors.append(f"SEO_DESC>155 ({len(seo_d)}): {seo_d}")
if not os.path.isfile(desc_path): errors.append(f"missing desc file: {desc_path}")
if os.path.isfile(desc_path):
    html = open(desc_path).read()
    m = re.search(r'<table id="size-chart">.*?<tbody>(.*?)</tbody>', html, re.S)
    if m:
        tbody_rows = len(re.findall(r'<tr>', m.group(1)))
        if tbody_rows != len(chart):
            errors.append(f"body size-table rows ({tbody_rows}) != SIZE_CHART length ({len(chart)})")
    else:
        errors.append("could not find <table id=\"size-chart\"> tbody in description.html")
    th_count = len(re.findall(r'<th>', html))
    if th_count != 10:
        errors.append(f"body size-table <th> count {th_count} != 10")

if errors:
    print("PREFLIGHT FAILED:")
    for e in errors: print("  -", e)
    sys.exit(1)

# Derived lists
def child_bucket(label):
    return ("Child 2-3yr"  if label in ("Child 2 Years","Child 3 Years") else
            "Child 4-5yr"  if label in ("Child 4 Years","Child 5 Years") else
            "Child 6-8yr"  if label in ("Child 6-7 Years","Child 8 Years") else
            "Child 9-10yr" if label == "Child 9-10 Years" else None)

derived = {
    "size_option_values": [r["picker_label"] for r in chart],
    "skus": [f"DLM-{shortcode}-{r['sku_suffix']}-{color_token}" for r in chart],
    "shopify_size_gids": [r["size_metaobject_gid"] for r in chart if r["size_metaobject_gid"]],
    "mother_tags": [r["picker_label"] for r in chart if r["audience"] == "mother"],
    "child_buckets": sorted({b for r in chart if r["audience"]=="child" for b in [child_bucket(r["picker_label"])] if b}),
}
json.dump(derived, open(os.path.join(os.path.dirname(chart_path),"derived.json"),"w"), indent=2)
print("PREFLIGHT OK — SIZE_CHART rows:", len(chart))
print("  picker labels:", derived["size_option_values"])
print("  SKUs:", derived["skus"])
print("  mother picker labels:", derived["mother_tags"])
print("  child age-bucket tags:", derived["child_buckets"])
print("  shopify.size GIDs:", derived["shopify_size_gids"])
PY

DERIVED_JSON="$TMPDIR_LOCAL/derived.json"

# -------------------------------------------------------------------
# 5a. productCreate
# -------------------------------------------------------------------
python3 - "$TMPDIR_LOCAL/productCreate.json" \
         "$TMPDIR_LOCAL/SIZE_CHART.json" \
         "$DERIVED_JSON" \
         "$DESC_HTML_FILE" \
         "$PRODUCT_TITLE" "$PRODUCT_HANDLE" "$SEO_TITLE" "$SEO_DESC" \
         "$COLOR_NAME" "$VENDOR_URL" <<'PY'
import json, sys
out, chart_p, derived_p, desc_p, title, handle, seo_t, seo_d, color_name, vendor_url = sys.argv[1:11]
chart   = json.load(open(chart_p))
derived = json.load(open(derived_p))
desc    = open(desc_p).read()

tags = [
    "Mommy and Me",
    "Pajamas",
    "Matching Family Pajamas",
    "Long Sleeve Pajamas",
    "Summer",
    "Spring",
    "Fall",
    "Cream",
    "Ivory",
    "Peter Rabbit",
    "Bunny",
    "Rabbit",
    "Eucalyptus",
    "Watercolor",
    "Floral",
    "Storybook",
    "Cotton",
    "Cotton Gauze",
    "Four Layer Gauze",
    "Loungewear",
    "Button Up Pajamas",
    "Easter",
]
tags += derived["child_buckets"]
tags += derived["mother_tags"]
tags.append(vendor_url)

product = {
    "title": title,
    "handle": handle,
    "vendor": "dresslikemommy.com",
    "productType": "Matching Family Pajamas",
    "status": "ACTIVE",
    "category": "gid://shopify/TaxonomyCategory/aa-1-17-4",
    "descriptionHtml": desc,
    "seo": { "title": seo_t, "description": seo_d },
    "tags": tags,
    "productOptions": [
        {"name": "Size", "values": [{"name": v} for v in derived["size_option_values"]]},
        {"name": "Color","values": [{"name": color_name}]}
    ]
}
body = {
    "query": "mutation productCreate($product: ProductCreateInput!) { productCreate(product: $product) { product { id handle title } userErrors { field message } } }",
    "variables": {"product": product}
}
json.dump(body, open(out,"w"))
PY

echo "==> productCreate"
CREATE_RESP="$(gql "$TMPDIR_LOCAL/productCreate.json")"
echo "$CREATE_RESP" | python3 -c "import json,sys; d=json.load(sys.stdin); print(json.dumps(d, indent=2)[:2000])"
PRODUCT_ID="$(echo "$CREATE_RESP" | python3 -c "import json,sys; print(json.load(sys.stdin)['data']['productCreate']['product']['id'])")"
echo "PRODUCT_ID=$PRODUCT_ID"
echo "$PRODUCT_ID" > "$SCRIPT_DIR/.peter-rabbit-gauze-last-product-id"

# -------------------------------------------------------------------
# 5b. productVariantsBulkCreate (strategy REMOVE_STANDALONE_VARIANT)
# -------------------------------------------------------------------
python3 - "$PRODUCT_ID" \
         "$TMPDIR_LOCAL/SIZE_CHART.json" \
         "$TMPDIR_LOCAL/variantsCreate.json" \
         "$COLOR_NAME" "$SHORTCODE" "$COLOR_TOKEN" <<'PY'
import json, sys
pid, chart_p, out, color_name, shortcode, color_token = sys.argv[1:7]
chart = json.load(open(chart_p))

variants = []
for r in chart:
    variants.append({
        "price": r["price"],
        "compareAtPrice": r["compare_at"],
        "inventoryPolicy": "DENY",
        "optionValues": [
            {"optionName": "Size",  "name": r["picker_label"]},
            {"optionName": "Color", "name": color_name}
        ],
        "inventoryItem": {
            "sku": f"DLM-{shortcode}-{r['sku_suffix']}-{color_token}",
            "tracked": True,
            "requiresShipping": True,
            "measurement": {"weight": {"value": r["weight_grams"], "unit": "GRAMS"}}
        }
    })
body = {
    "query": "mutation bulkCreate($productId: ID!, $variants: [ProductVariantsBulkInput!]!, $strategy: ProductVariantsBulkCreateStrategy) { productVariantsBulkCreate(productId: $productId, variants: $variants, strategy: $strategy) { productVariants { id title sku price compareAtPrice inventoryPolicy } userErrors { field message } } }",
    "variables": {
        "productId": pid,
        "strategy": "REMOVE_STANDALONE_VARIANT",
        "variants": variants
    }
}
json.dump(body, open(out,"w"))
PY

echo "==> productVariantsBulkCreate"
VRESP="$(gql "$TMPDIR_LOCAL/variantsCreate.json")"
echo "$VRESP" | python3 -c "import json,sys; d=json.load(sys.stdin); print(json.dumps(d, indent=2)[:3000])"

# -------------------------------------------------------------------
# 5c. metafieldsSet
# -------------------------------------------------------------------
python3 - "$PRODUCT_ID" \
         "$TMPDIR_LOCAL/SIZE_CHART.json" \
         "$DERIVED_JSON" \
         "$TMPDIR_LOCAL/metafieldsSet.json" \
         "$SEO_TITLE" "$SEO_DESC" <<'PY'
import json, sys
pid, chart_p, derived_p, out, seo_t, seo_d = sys.argv[1:7]
chart   = json.load(open(chart_p))
derived = json.load(open(derived_p))

color_pattern_gids = [
    "gid://shopify/Metaobject/69641928801",   # Beige
    "gid://shopify/Metaobject/129971519585",  # Floral
    "gid://shopify/Metaobject/130231140449",  # Multicolor
]
fabric_gids = ["gid://shopify/Metaobject/69622399073"]  # Cotton
target_gender_gids = ["gid://shopify/Metaobject/129971617889"]  # Female
age_group_gids = [
    "gid://shopify/Metaobject/129972764769",  # Toddlers
    "gid://shopify/Metaobject/128116523105",  # Kids
    "gid://shopify/Metaobject/128116490337",  # Adults
]
size_gids = derived["shopify_size_gids"]

mfs = [
    ["custom","category1",         "single_line_text_field","Mommy and Me"],
    ["custom","subcategory",       "single_line_text_field","Pajamas"],
    ["custom","subcategory2",      "single_line_text_field","Summer Pajamas"],
    ["custom","pattern",           "single_line_text_field","Watercolor Peter Rabbit bunnies + eucalyptus meadow print"],
    ["custom","style",             "single_line_text_field","Matching Family Set"],
    ["custom","type",              "single_line_text_field","Two-Piece Pajama Set"],
    ["mm-google-shopping","custom_product","boolean","false"],
    ["mm-google-shopping","gender",        "single_line_text_field","female"],
    ["mm-google-shopping","age_group",     "single_line_text_field","adult"],
    ["mm-google-shopping","condition",     "single_line_text_field","new"],
    ["mm-google-shopping","custom_label_0","single_line_text_field","Mommy and Me"],
    ["mm-google-shopping","custom_label_1","single_line_text_field","Peter Rabbit Bunny"],
    ["mm-google-shopping","custom_label_2","single_line_text_field","Summer"],
    ["mm-google-shopping","custom_label_3","single_line_text_field","Long Sleeve"],
    ["mm-google-shopping","custom_label_4","single_line_text_field","Family Matching"],
    ["shopify","age-group",     "list.metaobject_reference", json.dumps(age_group_gids)],
    ["shopify","color-pattern", "list.metaobject_reference", json.dumps(color_pattern_gids)],
    ["shopify","fabric",        "list.metaobject_reference", json.dumps(fabric_gids)],
    ["shopify","size",          "list.metaobject_reference", json.dumps(size_gids)],
    ["shopify","target-gender", "list.metaobject_reference", json.dumps(target_gender_gids)],
    ["global","title_tag",      "single_line_text_field", seo_t],
    ["global","description_tag","single_line_text_field", seo_d],
]

metas = [{"ownerId": pid, "namespace": ns, "key": k, "type": t, "value": v} for ns,k,t,v in mfs]
body = {
    "query": "mutation metafieldsSet($metafields: [MetafieldsSetInput!]!) { metafieldsSet(metafields: $metafields) { metafields { id namespace key type value } userErrors { field message } } }",
    "variables": { "metafields": metas }
}
json.dump(body, open(out,"w"))
PY

echo "==> metafieldsSet"
MFRESP="$(gql "$TMPDIR_LOCAL/metafieldsSet.json")"
echo "$MFRESP" | python3 -c "
import json,sys
d=json.load(sys.stdin)
res=d.get('data',{}).get('metafieldsSet',{})
ue=res.get('userErrors',[])
mfs=res.get('metafields',[]) or []
print('wrote',len(mfs),'metafields')
for m in mfs:
    v=str(m['value'])
    print(' -',m['namespace']+'.'+m['key'],'(',m['type'],') =',v[:120])
if ue: print('userErrors:',json.dumps(ue,indent=2))
"

# -------------------------------------------------------------------
# 5d. publishablePublish — 5 channels
# -------------------------------------------------------------------
for PUB in \
  "gid://shopify/Publication/55169925"      \
  "gid://shopify/Publication/21969633377"   \
  "gid://shopify/Publication/29172400225"   \
  "gid://shopify/Publication/76582879329"   \
  "gid://shopify/Publication/76604768353"
do
  cat > "$TMPDIR_LOCAL/publish.json" <<JSON
{"query":"mutation pub(\$id:ID!,\$input:[PublicationInput!]!){ publishablePublish(id:\$id, input:\$input){ userErrors{ field message } } }","variables":{"id":"$PRODUCT_ID","input":[{"publicationId":"$PUB"}]}}
JSON
  echo "==> publish to $PUB"
  gql "$TMPDIR_LOCAL/publish.json" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d)"
done

# -------------------------------------------------------------------
# 5e. Media (idempotent — only if images present)
# -------------------------------------------------------------------
IMAGE_DIR="/Users/fsuels/Projects/dresslikemommy/uploads/peter-rabbit-gauze-mommy-and-me-pajamas"
if [[ -d "$IMAGE_DIR" ]] && compgen -G "$IMAGE_DIR/*" > /dev/null; then
  echo "==> media present at $IMAGE_DIR — upload step would run here"
  echo "    (TODO: stagedUploadsCreate + productCreateMedia)"
else
  echo "==> media: no images at $IMAGE_DIR (skip; re-run once images drop)"
fi

# -------------------------------------------------------------------
# POST-CREATE VERIFY — diff live SKUs vs derived SKUs, halt on mismatch
# -------------------------------------------------------------------
cat > "$TMPDIR_LOCAL/verify.json" <<JSON
{"query":"query(\$id:ID!){ product(id:\$id){ id handle title status publishedAt onlineStoreUrl options{ name values } variants(first:50){ edges{ node{ sku title price compareAtPrice inventoryPolicy inventoryItem{ tracked requiresShipping } } } } tags seo{ title description } descriptionHtml metafields(first:40){ edges{ node{ namespace key type value } } } } }","variables":{"id":"$PRODUCT_ID"}}
JSON
echo "==> post-create verify"
VER="$(gql "$TMPDIR_LOCAL/verify.json")"
echo "$VER" > "$SCRIPT_DIR/.peter-rabbit-gauze-verify.json"
python3 - "$VER" "$DERIVED_JSON" <<'PY'
import json, sys, re
ver = json.loads(sys.argv[1])
derived = json.load(open(sys.argv[2]))
p = ver["data"]["product"]
live_skus = sorted([e["node"]["sku"] for e in p["variants"]["edges"]])
want_skus = sorted(derived["skus"])
print("LIVE SKUs:", live_skus)
print("WANT SKUs:", want_skus)
assert live_skus == want_skus, "SKU MISMATCH"
print("SKU MATCH OK — count:", len(live_skus))
print("published at:", p.get("publishedAt"))
print("onlineStoreUrl:", p.get("onlineStoreUrl"))
print("status:", p.get("status"))
html = p.get("descriptionHtml","")
m = re.search(r'<table id="size-chart">.*?<tbody>(.*?)</tbody>', html, re.S)
if m:
    rows = len(re.findall(r'<tr>', m.group(1)))
    print("live size-chart tbody rows:", rows)
    assert rows == len(derived["skus"]), "live size-chart row count mismatch"
else:
    raise SystemExit("live descriptionHtml has no #size-chart table")
th_count = len(re.findall(r'<th>', html))
print("live size-chart <th> count:", th_count)
assert th_count == 10, "live <th> count != 10"
PY

echo ""
echo "ALL DONE — product id: $PRODUCT_ID"
