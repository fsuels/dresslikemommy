#!/usr/bin/env bash
# Retry metafields for Good Night Song of the Sea product with correct types.
set -euo pipefail

ENV_FILE="${SHOPIFY_ENV_FILE:-${HOME}/.config/dresslikemommy/shopify-admin.env}"
if [ ! -f "$ENV_FILE" ]; then
  for C in "/sessions/kind-laughing-cerf/mnt/.config--dresslikemommy/shopify-admin.env" "/Users/fsuels/.config/dresslikemommy/shopify-admin.env"; do
    [ -f "$C" ] && ENV_FILE="$C" && break
  done
fi
source "$ENV_FILE"

API="https://${SHOPIFY_STORE_DOMAIN}/admin/api/2025-01/graphql.json"
AUTH=(-H "X-Shopify-Access-Token: ${SHOPIFY_ADMIN_ACCESS_TOKEN}" -H "Content-Type: application/json")
PID="gid://shopify/Product/7533351272545"

gql() {
  jq -n --arg q "$1" --argjson v "${2:-{\}}" '{query:$q, variables:$v}' \
    | curl -sS "${AUTH[@]}" -X POST -d @- "$API"
}

# BATCH 1: custom.* + mm-google-shopping.* + global.* (all text)
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
 {ownerId:$id,namespace:"mm-google-shopping",key:"google_product_category",type:"single_line_text_field",value:"Apparel & Accessories > Clothing > Sleepwear & Loungewear > Pajamas"}
]')
echo "==> batch 1 custom/google"
RESP=$(gql 'mutation($metafields:[MetafieldsSetInput!]!){metafieldsSet(metafields:$metafields){metafields{id namespace key} userErrors{field message}}}' "$(jq -n --argjson m "$MF" '{metafields:$m}')")
echo "$RESP" | jq '.data.metafieldsSet.userErrors, (.data.metafieldsSet.metafields|length)'

# BATCH 2: shopify.* (list.metaobject_reference)
# GIDs from store introspection
AGE_KIDS="gid://shopify/Metaobject/128116523105"
AGE_ADULT="gid://shopify/Metaobject/128116490337"
TGENDER_FEMALE="gid://shopify/Metaobject/129971617889"
COLOR_BEIGE="gid://shopify/Metaobject/69641928801"
COLOR_BLUE="gid://shopify/Metaobject/69639766113"
COLOR_MULTI="gid://shopify/Metaobject/130231140449"
COLOR_FLORAL="gid://shopify/Metaobject/129971519585"
SLEEVE_SHORT="gid://shopify/Metaobject/129971486817"
FABRIC_COTTON="gid://shopify/Metaobject/69622399073"
# sizes — exact same ordered GIDs bird-chirping uses
S_K2="gid://shopify/Metaobject/129972863073"
S_K3="gid://shopify/Metaobject/129972895841"
S_K4="gid://shopify/Metaobject/129972928609"
S_K5="gid://shopify/Metaobject/129972961377"
S_K67="gid://shopify/Metaobject/139840323681"
S_K8="gid://shopify/Metaobject/139840356449"
S_K910="gid://shopify/Metaobject/139840389217"
S_MS="gid://shopify/Metaobject/129975255137"
S_MM="gid://shopify/Metaobject/129975222369"
S_ML="gid://shopify/Metaobject/129975189601"
S_MXL="gid://shopify/Metaobject/129975287905"

MF2=$(jq -n --arg id "$PID" \
  --arg age "[\"$AGE_KIDS\",\"$AGE_ADULT\"]" \
  --arg tg "[\"$TGENDER_FEMALE\"]" \
  --arg col "[\"$COLOR_BEIGE\",\"$COLOR_BLUE\",\"$COLOR_MULTI\",\"$COLOR_FLORAL\"]" \
  --arg sl "[\"$SLEEVE_SHORT\"]" \
  --arg fa "[\"$FABRIC_COTTON\"]" \
  --arg sz "[\"$S_K2\",\"$S_K3\",\"$S_K4\",\"$S_K5\",\"$S_K67\",\"$S_K8\",\"$S_K910\",\"$S_MS\",\"$S_MM\",\"$S_ML\",\"$S_MXL\"]" '
[
 {ownerId:$id,namespace:"shopify",key:"age-group",type:"list.metaobject_reference",value:$age},
 {ownerId:$id,namespace:"shopify",key:"target-gender",type:"list.metaobject_reference",value:$tg},
 {ownerId:$id,namespace:"shopify",key:"color-pattern",type:"list.metaobject_reference",value:$col},
 {ownerId:$id,namespace:"shopify",key:"sleeve-length-type",type:"list.metaobject_reference",value:$sl},
 {ownerId:$id,namespace:"shopify",key:"fabric",type:"list.metaobject_reference",value:$fa},
 {ownerId:$id,namespace:"shopify",key:"size",type:"list.metaobject_reference",value:$sz}
]')
echo "==> batch 2 shopify.*"
RESP=$(gql 'mutation($metafields:[MetafieldsSetInput!]!){metafieldsSet(metafields:$metafields){metafields{id namespace key} userErrors{field message}}}' "$(jq -n --argjson m "$MF2" '{metafields:$m}')")
echo "$RESP" | jq '.data.metafieldsSet.userErrors, (.data.metafieldsSet.metafields|length)'
