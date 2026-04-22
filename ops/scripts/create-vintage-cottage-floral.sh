#!/usr/bin/env bash
# Create the Vintage Cottage Floral Mommy-and-Me pajama draft via Shopify Admin GraphQL.
# Idempotent-ish: if the handle already exists it will error; change the handle or delete first.

set -euo pipefail

source "$HOME/.config/dresslikemommy/shopify-admin.env"

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

HANDLE="vintage-cottage-floral-mommy-and-me-pajama-set"
TITLE="Vintage Cottage Floral Mommy and Me Matching Pajama Set — Short-Sleeve Button-Down Top + Shorts (Mother & Daughter)"
VENDOR="dresslikemommy.com"
TYPE="Matching Family Pajamas"
SEO_TITLE="Mommy and Me Pajamas — Vintage Cottage Floral Set"
SEO_DESC="Match your mini in our Vintage Cottage Floral mommy-and-me pajama set — breathable cotton, button-down top, sizes 2Y–10Y + Mom S–XL. Shop the set."

TAGS_JSON='["Mommy and Me","Pajamas","Matching Family Pajamas","Short Sleeve Pajamas","Summer","Cream","Floral","Vintage Cottage Floral","Storybook","Whimsical","Child 2-3yr","Child 4-5yr","Child 6-8yr","Child 9-10yr","Mother S","Mother M","Mother L","Mother XL","https://detail.1688.com/offer/900601808231.html"]'

BODY_HTML=$(cat <<'HTML'
<ul><li><strong>Soft breathable cotton:</strong> Lightweight woven cotton with a smooth hand-feel that stays cool on warm nights and gentle against little cheeks.</li><li><strong>Make every moment match:</strong> Coordinating mother and daughter sets designed for brunch, birthdays, holiday cards, and cozy family bonding — effortless matching, photo-ready in seconds.</li><li><strong>Vintage cottage floral print:</strong> A storybook-inspired bouquet of hydrangeas, tulips, and wildflowers scattered over a warm cream ground — picture-perfect and quietly whimsical.</li><li><strong>Classic design details:</strong> Notched collar, full button-down front, contrast sage-green piping along the placket, cuffs, and hem, and pull-on elastic-waist shorts for easy movement.</li><li><strong>Easy care & breathable:</strong> Machine-wash cold, tumble dry low. Breathable cotton weave keeps airflow high and wrinkles low.</li><li><strong>Full family size range:</strong> Girls 2–10 years and Mothers S–XL so the whole family can twin.</li></ul><p>&nbsp;</p><table id="size-chart"><thead><tr><th>Size</th><th>Recommended Weight (kg/lbs)</th><th>Recommended Height (cm/in)</th><th>Chest/Bust (cm/in)</th><th>Sleeve Length (cm/in)</th><th>Pant/Short Length (cm/in)</th><th>Hip (cm/in)</th><th>Garment Length (cm/in)</th></tr></thead><tbody><!-- Children Sizes --><tr><td>Child 2 Years (90)</td><td>11–13 kg / 24–29 lbs</td><td>85–95 cm / 33–37 in</td><td>68 cm / 26.8 in</td><td>16 cm / 6.3 in</td><td>26 cm / 10.2 in</td><td>70 cm / 27.6 in</td><td>38 cm / 15.0 in</td></tr><tr><td>Child 3 Years (100)</td><td>13–16 kg / 29–35 lbs</td><td>95–105 cm / 37–41 in</td><td>72 cm / 28.3 in</td><td>17 cm / 6.7 in</td><td>28 cm / 11.0 in</td><td>74 cm / 29.1 in</td><td>41 cm / 16.1 in</td></tr><tr><td>Child 4 Years (110)</td><td>16–19 kg / 35–42 lbs</td><td>105–115 cm / 41–45 in</td><td>76 cm / 29.9 in</td><td>18 cm / 7.1 in</td><td>30 cm / 11.8 in</td><td>78 cm / 30.7 in</td><td>44 cm / 17.3 in</td></tr><tr><td>Child 5 Years (120)</td><td>19–22 kg / 42–49 lbs</td><td>115–125 cm / 45–49 in</td><td>80 cm / 31.5 in</td><td>19 cm / 7.5 in</td><td>33 cm / 13.0 in</td><td>83 cm / 32.7 in</td><td>47 cm / 18.5 in</td></tr><tr><td>Child 6-7 Years (130)</td><td>22–27 kg / 49–60 lbs</td><td>125–135 cm / 49–53 in</td><td>84 cm / 33.1 in</td><td>20 cm / 7.9 in</td><td>35.5 cm / 14.0 in</td><td>87 cm / 34.3 in</td><td>50 cm / 19.7 in</td></tr><tr><td>Child 8 Years (140)</td><td>27–33 kg / 60–73 lbs</td><td>135–145 cm / 53–57 in</td><td>88 cm / 34.6 in</td><td>21 cm / 8.3 in</td><td>38 cm / 15.0 in</td><td>91 cm / 35.8 in</td><td>53 cm / 20.9 in</td></tr><tr><td>Child 9-10 Years (150)</td><td>33–40 kg / 73–88 lbs</td><td>145–155 cm / 57–61 in</td><td>92 cm / 36.2 in</td><td>22 cm / 8.7 in</td><td>40.5 cm / 15.9 in</td><td>95 cm / 37.4 in</td><td>56 cm / 22.0 in</td></tr><!-- Adult Sizes --><tr><td>Mother S</td><td>45–52 kg / 99–115 lbs</td><td>155–160 cm / 61–63 in</td><td>102 cm / 40.2 in</td><td>22 cm / 8.7 in</td><td>40 cm / 15.7 in</td><td>106 cm / 41.7 in</td><td>58 cm / 22.8 in</td></tr><tr><td>Mother M</td><td>52–60 kg / 115–132 lbs</td><td>160–165 cm / 63–65 in</td><td>106 cm / 41.7 in</td><td>23 cm / 9.1 in</td><td>41 cm / 16.1 in</td><td>110 cm / 43.3 in</td><td>60 cm / 23.6 in</td></tr><tr><td>Mother L</td><td>60–68 kg / 132–150 lbs</td><td>165–170 cm / 65–67 in</td><td>110 cm / 43.3 in</td><td>24 cm / 9.4 in</td><td>42.5 cm / 16.7 in</td><td>114 cm / 44.9 in</td><td>63 cm / 24.8 in</td></tr><tr><td>Mother XL</td><td>68–75 kg / 150–165 lbs</td><td>170–175 cm / 67–69 in</td><td>114 cm / 44.9 in</td><td>25 cm / 9.8 in</td><td>44 cm / 17.3 in</td><td>118 cm / 46.5 in</td><td>65 cm / 25.6 in</td></tr></tbody></table><p>Our Vintage Cottage Floral mommy-and-me pajama set turns bedtime into a storybook moment. The cream cotton is painted with watercolor hydrangeas, blush tulips, and trailing garden wildflowers, finished with soft sage piping that frames the notched collar and cuffs. It is the kind of print that belongs in a sun-drenched reading nook — gentle, nostalgic, and quietly whimsical.</p><p>Wear it for slow Sunday brunches, summer sleepovers, birthday mornings, and those holiday-card mornings when everyone needs to look picture-perfect without trying. The button-down top and elastic-waist shorts move easily from pillow fights to pancake-making, and the full mother-and-daughter size run means nobody gets left out of the twinning moment.</p><h3>Key Features:</h3><ul><li><strong>Coordinated mother &amp; daughter fit:</strong> Identical print in adult and child cuts so every family photo matches effortlessly.</li><li><strong>Breathable cotton weave:</strong> Lightweight and airy for warm-weather sleep and summer travel.</li><li><strong>Button-down top:</strong> Classic notched collar, contrast sage piping, and real buttons down the front.</li><li><strong>Pull-on shorts:</strong> Soft elastic waistband for easy on-and-off and all-night comfort.</li><li><strong>Inclusive sizing:</strong> Girls 2–10 Years and Mothers S–XL — add both to cart to complete the set.</li></ul><p>Add the mother size and the matching children's size to your cart to make every moment match — bedtime, brunch, and every snapshot in between.</p>
HTML
)

# ============= STEP 1: productCreate =============
METAFIELDS_JSON=$(cat <<'JSON'
[
  {"namespace":"custom","key":"category1","type":"single_line_text_field","value":"Mommy and Me"},
  {"namespace":"custom","key":"subcategory","type":"single_line_text_field","value":"Pajamas"},
  {"namespace":"custom","key":"subcategory2","type":"single_line_text_field","value":"Summer Pajamas"},
  {"namespace":"custom","key":"pattern","type":"single_line_text_field","value":"Vintage Cottage Floral Print"},
  {"namespace":"custom","key":"style","type":"single_line_text_field","value":"Matching Family Set"},
  {"namespace":"custom","key":"type","type":"single_line_text_field","value":"Two-Piece Pajama Set"}
]
JSON
)

SEO_JSON=$(jq -nc --arg t "$SEO_TITLE" --arg d "$SEO_DESC" '{title:$t, description:$d}')

CREATE_QUERY='mutation ProductCreate($input: ProductInput!) {
  productCreate(input: $input) {
    product { id handle title status onlineStoreUrl }
    userErrors { field message }
  }
}'

CREATE_VARS=$(jq -nc \
  --arg handle "$HANDLE" \
  --arg title "$TITLE" \
  --arg vendor "$VENDOR" \
  --arg ptype "$TYPE" \
  --arg body "$BODY_HTML" \
  --argjson tags "$TAGS_JSON" \
  --argjson mfs "$METAFIELDS_JSON" \
  --argjson seo "$SEO_JSON" '
  {
    input: {
      handle: $handle,
      title: $title,
      vendor: $vendor,
      productType: $ptype,
      descriptionHtml: $body,
      tags: $tags,
      status: "DRAFT",
      seo: $seo,
      metafields: $mfs,
      productOptions: [
        { name: "Size",  values: [
            {name:"Child 2 Years"},{name:"Child 3 Years"},{name:"Child 4 Years"},
            {name:"Child 5 Years"},{name:"Child 6-7 Years"},{name:"Child 8 Years"},
            {name:"Child 9-10 Years"},
            {name:"Mother S"},{name:"Mother M"},{name:"Mother L"},{name:"Mother XL"}
        ]},
        { name: "Color", values: [ {name:"Vintage Cottage Floral"} ] }
      ]
    }
  }')

echo ">>> productCreate" >&2
CREATE_RESP=$(gql "$CREATE_QUERY" "$CREATE_VARS")
echo "$CREATE_RESP" | jq . >&2

PRODUCT_ID=$(echo "$CREATE_RESP" | jq -r '.data.productCreate.product.id // empty')
if [[ -z "$PRODUCT_ID" ]]; then
  echo "ERROR: productCreate failed" >&2
  exit 1
fi
echo "PRODUCT_ID=$PRODUCT_ID" >&2

# ============= STEP 2: productVariantsBulkCreate =============
VARIANTS_JSON=$(cat <<'JSON'
[
  {"price":"34.99","compareAtPrice":"40.24","sku":"DLM-VCF-KID2Y-CREAM",   "optionValues":[{"optionName":"Size","name":"Child 2 Years"},    {"optionName":"Color","name":"Vintage Cottage Floral"}]},
  {"price":"34.99","compareAtPrice":"40.24","sku":"DLM-VCF-KID3Y-CREAM",   "optionValues":[{"optionName":"Size","name":"Child 3 Years"},    {"optionName":"Color","name":"Vintage Cottage Floral"}]},
  {"price":"34.99","compareAtPrice":"40.24","sku":"DLM-VCF-KID4Y-CREAM",   "optionValues":[{"optionName":"Size","name":"Child 4 Years"},    {"optionName":"Color","name":"Vintage Cottage Floral"}]},
  {"price":"34.99","compareAtPrice":"40.24","sku":"DLM-VCF-KID5Y-CREAM",   "optionValues":[{"optionName":"Size","name":"Child 5 Years"},    {"optionName":"Color","name":"Vintage Cottage Floral"}]},
  {"price":"34.99","compareAtPrice":"40.24","sku":"DLM-VCF-KID67Y-CREAM",  "optionValues":[{"optionName":"Size","name":"Child 6-7 Years"},  {"optionName":"Color","name":"Vintage Cottage Floral"}]},
  {"price":"34.99","compareAtPrice":"40.24","sku":"DLM-VCF-KID8Y-CREAM",   "optionValues":[{"optionName":"Size","name":"Child 8 Years"},    {"optionName":"Color","name":"Vintage Cottage Floral"}]},
  {"price":"34.99","compareAtPrice":"40.24","sku":"DLM-VCF-KID910Y-CREAM", "optionValues":[{"optionName":"Size","name":"Child 9-10 Years"}, {"optionName":"Color","name":"Vintage Cottage Floral"}]},
  {"price":"39.99","compareAtPrice":"45.99","sku":"DLM-VCF-MOMS-CREAM",    "optionValues":[{"optionName":"Size","name":"Mother S"},         {"optionName":"Color","name":"Vintage Cottage Floral"}]},
  {"price":"39.99","compareAtPrice":"45.99","sku":"DLM-VCF-MOMM-CREAM",    "optionValues":[{"optionName":"Size","name":"Mother M"},         {"optionName":"Color","name":"Vintage Cottage Floral"}]},
  {"price":"39.99","compareAtPrice":"45.99","sku":"DLM-VCF-MOML-CREAM",    "optionValues":[{"optionName":"Size","name":"Mother L"},         {"optionName":"Color","name":"Vintage Cottage Floral"}]},
  {"price":"39.99","compareAtPrice":"45.99","sku":"DLM-VCF-MOMXL-CREAM",   "optionValues":[{"optionName":"Size","name":"Mother XL"},        {"optionName":"Color","name":"Vintage Cottage Floral"}]}
]
JSON
)

BULK_QUERY='mutation ProductVariantsBulkCreate($productId: ID!, $variants: [ProductVariantsBulkInput!]!, $strategy: ProductVariantsBulkCreateStrategy) {
  productVariantsBulkCreate(productId: $productId, variants: $variants, strategy: $strategy) {
    product { id variants(first: 50) { nodes { id sku title price compareAtPrice selectedOptions { name value } } } }
    userErrors { field message }
  }
}'

BULK_VARS=$(jq -nc --arg pid "$PRODUCT_ID" --argjson v "$VARIANTS_JSON" '
  { productId: $pid, variants: $v, strategy: "REMOVE_STANDALONE_VARIANT" }')

echo ">>> productVariantsBulkCreate" >&2
BULK_RESP=$(gql "$BULK_QUERY" "$BULK_VARS")
echo "$BULK_RESP" | jq . >&2

# Final summary
echo
echo "=== SUMMARY ==="
echo "Product ID:  $PRODUCT_ID"
echo "Handle:      $HANDLE"
ADMIN_NUM_ID=$(echo "$PRODUCT_ID" | sed 's|gid://shopify/Product/||')
echo "Admin URL:   https://admin.shopify.com/store/dresslikemommy/products/$ADMIN_NUM_ID"
echo "Variants:"
echo "$BULK_RESP" | jq -r '.data.productVariantsBulkCreate.product.variants.nodes[] | "  - \(.sku)  \(.title)  $\(.price)  (compare $\(.compareAtPrice))"'
