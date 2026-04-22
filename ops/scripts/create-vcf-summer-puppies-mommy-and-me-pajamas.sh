#!/usr/bin/env bash
# Create + fully-configure Shopify product for:
#   Summer Puppies Mommy and Me Pajamas — Short-Sleeve Set
# Handle:   summer-puppies-mommy-and-me-pajamas
# Vendor:   dresslikemommy.com  (source: 1688 offer 900601808231)
# Category: Pajamas (Matching Family Pajamas)
# API ver:  2025-01
#
# Usage:  bash create-vcf-summer-puppies-mommy-and-me-pajamas.sh
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

# ---------- 5a. productCreate ----------
cat > "$TMPDIR_LOCAL/productCreate.json" <<'JSON'
{
  "query": "mutation productCreate($product: ProductCreateInput!) { productCreate(product: $product) { product { id handle title onlineStorePreviewUrl } userErrors { field message } } }",
  "variables": {
    "product": {
      "title": "Summer Puppies Mommy and Me Pajamas — Short-Sleeve Set",
      "handle": "summer-puppies-mommy-and-me-pajamas",
      "vendor": "dresslikemommy.com",
      "productType": "Matching Family Pajamas",
      "status": "ACTIVE",
      "category": "gid://shopify/TaxonomyCategory/aa-1-17-4",
      "descriptionHtml": "__DESC_HTML__",
      "seo": {
        "title": "Summer Puppies Mommy and Me Pajamas | Short-Sleeve Set",
        "description": "Soft bamboo-cotton gauze puppy-print pajamas for mom and little one — piped collars, easy shorts, picture-perfect. Shop the set."
      },
      "tags": [
        "Mommy and Me",
        "Pajamas",
        "Matching Family Pajamas",
        "Short Sleeve Pajamas",
        "Summer",
        "Cream",
        "Ivory",
        "Puppy",
        "Dog",
        "Golden Retriever",
        "Summer Puppies",
        "Cartoon",
        "Animal Print",
        "Bamboo Cotton",
        "Gauze",
        "Loungewear",
        "Child 2-3yr",
        "Child 4-5yr",
        "Child 6-8yr",
        "Child 9-10yr",
        "Mother S",
        "Mother M",
        "Mother L",
        "Mother XL",
        "https://detail.1688.com/offer/900601808231.html"
      ],
      "productOptions": [
        { "name": "Size", "values": [
          { "name": "Child 2 Years" },
          { "name": "Child 3 Years" },
          { "name": "Child 4 Years" },
          { "name": "Child 5 Years" },
          { "name": "Child 6-7 Years" },
          { "name": "Child 8 Years" },
          { "name": "Child 9-10 Years" },
          { "name": "Mother S" },
          { "name": "Mother M" },
          { "name": "Mother L" },
          { "name": "Mother XL" }
        ]},
        { "name": "Color", "values": [ { "name": "Summer Puppies" } ] }
      ]
    }
  }
}
JSON

echo "==> productCreate"
# Description HTML is large — inject via jq to avoid JSON-escaping headaches
DESC_HTML_FILE="$(dirname "$0")/description.html"
if [[ ! -f "$DESC_HTML_FILE" ]]; then
  echo "ERROR: missing $DESC_HTML_FILE" >&2; exit 1
fi
python3 - "$TMPDIR_LOCAL/productCreate.json" "$DESC_HTML_FILE" <<'PY'
import json, sys
pc, dh = sys.argv[1], sys.argv[2]
with open(dh) as f: html = f.read()
with open(pc) as f: body = json.load(f)
body["variables"]["product"]["descriptionHtml"] = html
with open(pc, "w") as f: json.dump(body, f)
PY

RESP="$(gql "$TMPDIR_LOCAL/productCreate.json")"
echo "$RESP" | python3 -c "import json,sys; d=json.load(sys.stdin); print(json.dumps(d, indent=2)[:1500])"
PRODUCT_ID="$(echo "$RESP" | python3 -c "import json,sys; print(json.load(sys.stdin)['data']['productCreate']['product']['id'])")"
echo "PRODUCT_ID=$PRODUCT_ID"
echo "$PRODUCT_ID" > "$(dirname "$0")/.last-product-id"

# ---------- Fetch option IDs (needed for variants optionValues) ----------
cat > "$TMPDIR_LOCAL/getOptions.json" <<JSON
{"query":"query(\$id:ID!){ product(id:\$id){ options{ id name values } } }","variables":{"id":"$PRODUCT_ID"}}
JSON
OPT_RESP="$(gql "$TMPDIR_LOCAL/getOptions.json")"
echo "$OPT_RESP" | python3 -c "import json,sys; print(json.dumps(json.load(sys.stdin), indent=2))"

# ---------- 5b. productVariantsBulkCreate ----------
python3 - "$PRODUCT_ID" "$TMPDIR_LOCAL/variantsCreate.json" <<'PY'
import json, sys
pid = sys.argv[1]
out = sys.argv[2]
# Sizes: picker name -> SKU token
sizes = [
  ("Child 2 Years",   "KID2Y",  "31.99", "36.99", 300),
  ("Child 3 Years",   "KID3Y",  "31.99", "36.99", 300),
  ("Child 4 Years",   "KID4Y",  "31.99", "36.99", 300),
  ("Child 5 Years",   "KID5Y",  "31.99", "36.99", 300),
  ("Child 6-7 Years", "KID67Y", "31.99", "36.99", 300),
  ("Child 8 Years",   "KID8Y",  "31.99", "36.99", 300),
  ("Child 9-10 Years","KID910Y","31.99", "36.99", 300),
  ("Mother S",        "MOMS",   "34.99", "40.99", 350),
  ("Mother M",        "MOMM",   "34.99", "40.99", 350),
  ("Mother L",        "MOML",   "34.99", "40.99", 350),
  ("Mother XL",       "MOMXL",  "34.99", "40.99", 350),
]
variants = []
for size, tok, price, cap, grams in sizes:
    variants.append({
      "price": price,
      "compareAtPrice": cap,
      "inventoryPolicy": "DENY",
      "optionValues": [
        {"optionName": "Size", "name": size},
        {"optionName": "Color", "name": "Summer Puppies"}
      ],
      "inventoryItem": {
        "sku": f"DLM-VCF-{tok}-CREAM",
        "tracked": True,
        "requiresShipping": True,
        "measurement": {"weight": {"value": grams, "unit": "GRAMS"}}
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
with open(out, "w") as f: json.dump(body, f)
PY

echo "==> productVariantsBulkCreate"
VRESP="$(gql "$TMPDIR_LOCAL/variantsCreate.json")"
echo "$VRESP" | python3 -c "import json,sys; d=json.load(sys.stdin); print(json.dumps(d, indent=2)[:3000])"

# ---------- 5c. metafieldsSet ----------
python3 - "$PRODUCT_ID" "$TMPDIR_LOCAL/metafieldsSet.json" <<'PY'
import json, sys
pid = sys.argv[1]
out = sys.argv[2]

# [namespace, key, type, value]
mfs = [
  ["custom","category1","single_line_text_field","Mommy and Me"],
  ["custom","subcategory","single_line_text_field","Pajamas"],
  ["custom","subcategory2","single_line_text_field","Summer Pajamas"],
  ["custom","pattern","single_line_text_field","Summer Puppies watercolor golden retriever print"],
  ["custom","style","single_line_text_field","Matching Family Set"],
  ["custom","type","single_line_text_field","Two-Piece Pajama Set"],
  ["mm-google-shopping","custom_product","boolean","false"],
  ["mm-google-shopping","gender","single_line_text_field","female"],
  ["mm-google-shopping","age_group","single_line_text_field","adult"],
  ["mm-google-shopping","condition","single_line_text_field","new"],
  ["mm-google-shopping","custom_label_0","single_line_text_field","Mommy and Me"],
  ["mm-google-shopping","custom_label_1","single_line_text_field","Puppy Animal Print"],
  ["mm-google-shopping","custom_label_2","single_line_text_field","Summer"],
  ["mm-google-shopping","custom_label_3","single_line_text_field","Short Sleeve"],
  ["mm-google-shopping","custom_label_4","single_line_text_field","Family Matching"],
  ["shopify","age-group","list.single_line_text_field", json.dumps(["kids","adults"]) ],
  ["shopify","clothing-features","list.single_line_text_field", json.dumps(["Breathable","Soft","Lightweight"]) ],
  ["shopify","color-pattern","list.single_line_text_field", json.dumps(["Cream","Ivory","Animal Print"]) ],
  ["shopify","fabric","single_line_text_field","Bamboo Cotton Gauze"],
  ["shopify","size","list.single_line_text_field", json.dumps([
    "Child 2 Years","Child 3 Years","Child 4 Years","Child 5 Years",
    "Child 6-7 Years","Child 8 Years","Child 9-10 Years",
    "Mother S","Mother M","Mother L","Mother XL"
  ]) ],
  ["shopify","sleeve-length-type","single_line_text_field","Short Sleeve"],
  ["shopify","neckline","single_line_text_field","Notched Collar"],
  ["global","title_tag","single_line_text_field","Summer Puppies Mommy and Me Pajamas | Short-Sleeve Set"],
  ["global","description_tag","single_line_text_field","Soft bamboo-cotton gauze puppy-print pajamas for mom and little one — piped collars, easy shorts, picture-perfect. Shop the set."],
]

metas = []
for ns, key, typ, val in mfs:
    metas.append({
      "ownerId": pid,
      "namespace": ns,
      "key": key,
      "type": typ,
      "value": val
    })

body = {
  "query": "mutation metafieldsSet($metafields: [MetafieldsSetInput!]!) { metafieldsSet(metafields: $metafields) { metafields { id namespace key type value } userErrors { field message } } }",
  "variables": { "metafields": metas }
}
with open(out, "w") as f: json.dump(body, f)
PY

echo "==> metafieldsSet"
MFRESP="$(gql "$TMPDIR_LOCAL/metafieldsSet.json")"
echo "$MFRESP" | python3 -c "import json,sys; d=json.load(sys.stdin); ue=d.get('data',{}).get('metafieldsSet',{}).get('userErrors',[]); mfs=d.get('data',{}).get('metafieldsSet',{}).get('metafields',[]); print('wrote',len(mfs),'metafields'); [print(' -',m['namespace']+'.'+m['key'],'=',str(m['value'])[:80]) for m in mfs]; print('userErrors:',ue)"

# ---------- 5d. publishablePublish (5 channels) ----------
for PUB in \
  "gid://shopify/Publication/55169925" \
  "gid://shopify/Publication/21969633377" \
  "gid://shopify/Publication/29172400225" \
  "gid://shopify/Publication/76582879329" \
  "gid://shopify/Publication/76604768353"
do
  cat > "$TMPDIR_LOCAL/publish.json" <<JSON
{"query":"mutation pub(\$id:ID!,\$input:[PublicationInput!]!){ publishablePublish(id:\$id, input:\$input){ userErrors{ field message } } }","variables":{"id":"$PRODUCT_ID","input":[{"publicationId":"$PUB"}]}}
JSON
  echo "==> publish to $PUB"
  gql "$TMPDIR_LOCAL/publish.json" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d)"
done

echo ""
echo "ALL DONE — product id: $PRODUCT_ID"
