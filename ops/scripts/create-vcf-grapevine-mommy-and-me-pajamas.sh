#!/usr/bin/env bash
# Create + fully-configure Shopify product for:
#   Grapevine Mommy and Me Pajamas — Short-Sleeve Set
# Handle:   grapevine-mommy-and-me-pajamas
# Vendor:   dresslikemommy.com  (source: 1688 offer 792917229223)
# Category: Pajamas (Matching Family Pajamas)
# API ver:  2025-01
#
# SIZE_CHART JSON declared once at top — productOptions, variants,
# tags, body-HTML size table, shopify.size metafield, and SEO desc
# are all derived from it.
#
# Usage:  bash create-vcf-grapevine-mommy-and-me-pajamas.sh
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
  curl -sS -X POST -H "$H_TOKEN" -H "$H_JSON" --data @"$1" "$API"
}

TMPDIR_LOCAL="$(mktemp -d)"
trap 'rm -rf "$TMPDIR_LOCAL"' EXIT

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# -------------------------------------------------------------------
# SIZE_CHART — the ONLY place variants are defined
# Vendor offers child S/M/L with explicit age recommendations:
#   S = 1-2yr (garment length 54 cm)
#   M = 3-4yr (garment length 64 cm)
#   L = 5-6yr (garment length 74 cm)
# Adult 均码 → Mother One Size (single variant).
# Vendor's explicit age labels override the garment-length heuristic.
# -------------------------------------------------------------------
cat > "$TMPDIR_LOCAL/SIZE_CHART.json" <<'JSON'
[
  {
    "audience": "child",
    "vendor_label": "儿童S码（推荐1-2岁，garment length 54cm）",
    "picker_label": "Child 1-2 Years",
    "sku_suffix": "KID12Y",
    "age": "1–2",
    "weight": "10–13 kg / 22–29 lbs",
    "height": "80–90 cm / 31–35 in",
    "chest_full_cm": 66,
    "hem_full_cm": 99,
    "sleeve_cm": 19,
    "cuff_cm": 12,
    "length_cm": 54,
    "size_metaobject_gid": "gid://shopify/Metaobject/129972863073",
    "price": "28.99",
    "compare_at": "33.49",
    "weight_grams": 260
  },
  {
    "audience": "child",
    "vendor_label": "儿童M码（推荐3-4岁，garment length 64cm）",
    "picker_label": "Child 3-4 Years",
    "sku_suffix": "KID34Y",
    "age": "3–4",
    "weight": "14–17 kg / 31–37 lbs",
    "height": "95–105 cm / 37–41 in",
    "chest_full_cm": 70,
    "hem_full_cm": 103,
    "sleeve_cm": 20,
    "cuff_cm": 12.5,
    "length_cm": 64,
    "size_metaobject_gid": "gid://shopify/Metaobject/129972895841",
    "price": "28.99",
    "compare_at": "33.49",
    "weight_grams": 300
  },
  {
    "audience": "child",
    "vendor_label": "儿童L码（推荐5-6岁，garment length 74cm）",
    "picker_label": "Child 5-6 Years",
    "sku_suffix": "KID56Y",
    "age": "5–6",
    "weight": "18–22 kg / 40–49 lbs",
    "height": "110–120 cm / 43–47 in",
    "chest_full_cm": 74,
    "hem_full_cm": 111,
    "sleeve_cm": 21.5,
    "cuff_cm": 13,
    "length_cm": 74,
    "size_metaobject_gid": "gid://shopify/Metaobject/129972961377",
    "price": "28.99",
    "compare_at": "33.49",
    "weight_grams": 340
  },
  {
    "audience": "mother",
    "vendor_label": "成人均码（推荐75kg内）",
    "picker_label": "Mother One Size",
    "sku_suffix": "MOMOS",
    "age": "—",
    "weight": "up to 75 kg / 165 lbs",
    "height": "155–175 cm / 61–69 in",
    "chest_full_cm": 114,
    "hem_full_cm": 144,
    "sleeve_cm": 30,
    "cuff_cm": 21.5,
    "length_cm": 102,
    "size_metaobject_gid": null,
    "price": "31.99",
    "compare_at": "36.99",
    "weight_grams": 400
  }
]
JSON

# -------------------------------------------------------------------
# Static listing fields
# -------------------------------------------------------------------
PRODUCT_TITLE='Grapevine Mommy and Me Pajamas — Short-Sleeve Set'
PRODUCT_HANDLE='grapevine-mommy-and-me-pajamas'
SEO_TITLE='Grapevine Mommy & Me Pajamas — Matching | Dress Like Mommy'
SEO_DESC='Shop our Grapevine matching mommy-and-me pajamas — soft bamboo-cotton gauze short-sleeve sets for mom + daughter. Sizes 1-2Y, 3-4Y, 5-6Y & Mom One Size.'
COLOR_NAME='Grapevine Cream'
COLOR_TOKEN='CREAM'
SHORTCODE='VCF'
VENDOR_URL='https://detail.1688.com/offer/792917229223.html'
DESC_HTML_FILE="$SCRIPT_DIR/grapevine-description.html"

# -------------------------------------------------------------------
# PREFLIGHT GUARDS
# -------------------------------------------------------------------
python3 - "$TMPDIR_LOCAL/SIZE_CHART.json" "$PRODUCT_TITLE" "$SEO_TITLE" "$SEO_DESC" "$DESC_HTML_FILE" "$SHORTCODE" "$COLOR_TOKEN" <<'PY'
import json, sys, os, re
chart_path, title, seo_t, seo_d, desc_path, shortcode, color_token = sys.argv[1:8]
chart = json.load(open(chart_path))

errors = []
required = ["audience","vendor_label","picker_label","sku_suffix","age","weight","height","price","compare_at"]
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

if errors:
    print("PREFLIGHT FAILED:")
    for e in errors: print("  -", e)
    sys.exit(1)

derived = {
    "size_option_values": [r["picker_label"] for r in chart],
    "skus": [f"DLM-{shortcode}-{r['sku_suffix']}-{color_token}" for r in chart],
    "shopify_size_gids": [r["size_metaobject_gid"] for r in chart if r["size_metaobject_gid"]],
    "mother_tags": [r["picker_label"] for r in chart if r["audience"] == "mother"],
    "child_buckets": sorted({ _bucket for r in chart if r["audience"]=="child"
                              for _bucket in [
                                  "Child 1-2yr"  if r["picker_label"] == "Child 1-2 Years" else
                                  "Child 2-3yr"  if r["picker_label"] in ("Child 2 Years","Child 3 Years") else
                                  "Child 3-4yr"  if r["picker_label"] == "Child 3-4 Years" else
                                  "Child 4-5yr"  if r["picker_label"] in ("Child 4 Years","Child 5 Years") else
                                  "Child 5-6yr"  if r["picker_label"] == "Child 5-6 Years" else
                                  "Child 6-8yr"  if r["picker_label"] in ("Child 6-7 Years","Child 8 Years") else
                                  "Child 9-10yr"
                              ]}),
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
    "Short Sleeve Pajamas",
    "Nightgown",
    "Sleep Dress",
    "Summer",
    "Cream",
    "Ivory",
    "Rose",
    "Pink",
    "Sage",
    "Grapevine",
    "Vineyard",
    "Grape",
    "Vine",
    "Botanical",
    "Floral",
    "Watercolor",
    "Cottagecore",
    "Bamboo",
    "Cotton",
    "Loungewear",
    "Raglan Sleeve",
]
tags += derived["child_buckets"]   # Child 1-2yr / 3-4yr / 5-6yr per vendor ages
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
echo "$PRODUCT_ID" > "$SCRIPT_DIR/.grapevine-last-product-id"

# -------------------------------------------------------------------
# 5b. productVariantsBulkCreate
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

# Store catalog GIDs from neighbor pajamas
color_pattern_gids = [
    "gid://shopify/Metaobject/69641928801",   # Beige/Cream
    "gid://shopify/Metaobject/129971519585",  # Floral/Multi
    "gid://shopify/Metaobject/130231140449",  # Multicolor
]
fabric_gids = ["gid://shopify/Metaobject/69622399073"]   # Cotton (bamboo-cotton blend best-fit)
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
    ["custom","pattern",           "single_line_text_field","Watercolor Grapevine print — grapes, leaves, trailing vines on cream"],
    ["custom","style",             "single_line_text_field","Matching Family Set"],
    ["custom","type",              "single_line_text_field","Two-Piece Pajama Set"],
    ["mm-google-shopping","custom_product","boolean","false"],
    ["mm-google-shopping","gender",        "single_line_text_field","female"],
    ["mm-google-shopping","age_group",     "single_line_text_field","adult"],
    ["mm-google-shopping","condition",     "single_line_text_field","new"],
    ["mm-google-shopping","custom_label_0","single_line_text_field","Mommy and Me"],
    ["mm-google-shopping","custom_label_1","single_line_text_field","Grapevine Botanical"],
    ["mm-google-shopping","custom_label_2","single_line_text_field","Summer"],
    ["mm-google-shopping","custom_label_3","single_line_text_field","Short Sleeve"],
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
# POST-CREATE VERIFY
# -------------------------------------------------------------------
cat > "$TMPDIR_LOCAL/verify.json" <<JSON
{"query":"query(\$id:ID!){ product(id:\$id){ id handle title status publishedAt onlineStoreUrl options{ name values } variants(first:50){ edges{ node{ sku title price compareAtPrice inventoryPolicy inventoryItem{ tracked requiresShipping } } } } tags seo{ title description } metafields(first:40){ edges{ node{ namespace key type value } } } } }","variables":{"id":"$PRODUCT_ID"}}
JSON
echo "==> post-create verify"
VER="$(gql "$TMPDIR_LOCAL/verify.json")"
echo "$VER" > "$SCRIPT_DIR/.grapevine-verify.json"
python3 - "$VER" "$DERIVED_JSON" <<'PY'
import json, sys
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
PY

echo ""
echo "ALL DONE — product id: $PRODUCT_ID"
