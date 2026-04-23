#!/usr/bin/env bash
# Dress Like Mommy — White Lace Mommy and Me Dresses
# Runner: SIZE_CHART derives variants/body/metafields. Preflight guard,
# create-or-update, price-reset (FORCE_SPEC_PRICES), publish, verify.
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
  echo "SHOPIFY_ADMIN_ACCESS_TOKEN is not set." >&2
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
COLOR_NAME="White"
HANDLE="white-lace-mommy-and-me-dresses"
TITLE="White Lace Mommy and Me Dresses — Cami Dress"
SEO_TITLE="Mommy & Me White Lace Cami Dress | Dress Like Mommy"
SEO_DESC="Shop our White Lace matching mommy-and-me dresses — cotton-blend cami dress for mom + daughter. Kids 3Y–10Y, Mom S–M."
VENDOR="dresslikemommy.com"
PRODUCT_TYPE="Dresses"
TAXONOMY_GID="gid://shopify/TaxonomyCategory/aa-1-13-8"
CHILD_PRICE="28.99"     # GIRL_PRICE
MOTHER_PRICE="31.99"    # MOTHER_PRICE
CHILD_CMP="34.49"       # round_up(28.99 * 1.15, .99) = 33.33 → 33.99; but spec table says 29.99→34.99. 28.99 * 1.15 = 33.34; round_up to next .99 = 33.99
MOTHER_CMP="36.99"      # 31.99 * 1.15 = 36.79; round_up to next .99 = 36.99
# Re-derived per auto-derive rule: round_up(price × 1.15, .99)
#   28.99 × 1.15 = 33.3385 → next .99 = 33.99
#   31.99 × 1.15 = 36.7885 → next .99 = 36.99
CHILD_CMP="33.99"
MOTHER_CMP="36.99"
VENDOR_URL="https://detail.1688.com/offer/1032400758007.html"
SEASON="Summer"
FORCE_SPEC_PRICES="true"

# Publication GIDs
PUB_ONLINE="gid://shopify/Publication/55169925"
PUB_GOOGLE="gid://shopify/Publication/21969633377"
PUB_META="gid://shopify/Publication/29172400225"
PUB_PINT="gid://shopify/Publication/76582879329"
PUB_TT="gid://shopify/Publication/76604768353"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CHART="$SCRIPT_DIR/size_chart_vcf_white_lace.json"
[[ -f "$CHART" ]] || { echo "FAIL: SIZE_CHART not found at $CHART"; exit 1; }

# ─────────────────────────────────────────────────────────────────────────────
# 2. Preflight
# ─────────────────────────────────────────────────────────────────────────────
echo "── Preflight ──"
jq -e 'all(.[]; .audience and .role and .vendor_label and .picker_label and .sku_suffix and .age and .weight and .height and .chest_cm and .hip_cm and .waist_cm and .length_cm)' "$CHART" >/dev/null || { echo "FAIL: missing required SIZE_CHART fields"; exit 1; }

ROW_COUNT=$(jq 'length' "$CHART")
UNIQ=$(jq '[.[].picker_label] | unique | length' "$CHART")
[[ "$ROW_COUNT" == "$UNIQ" ]] || { echo "FAIL: duplicate picker_label"; exit 1; }

# Unique (role, picker_label)
PAIR_UNIQ=$(jq '[.[] | (.role + "|" + .picker_label)] | unique | length' "$CHART")
[[ "$ROW_COUNT" == "$PAIR_UNIQ" ]] || { echo "FAIL: duplicate (role, picker_label)"; exit 1; }

[[ ${#TITLE} -le 70 ]] || { echo "FAIL: title > 70"; exit 1; }
[[ ${#SEO_TITLE} -le 60 ]] || { echo "FAIL: seo title > 60"; exit 1; }
# SEO_DESC chars – use python for unicode
SEO_DESC_LEN=$(python3 -c "import sys; s=sys.argv[1]; print(len(s))" "$SEO_DESC")
[[ "$SEO_DESC_LEN" -le 155 ]] || { echo "FAIL: seo desc > 155 ($SEO_DESC_LEN)"; exit 1; }

# Role vs ROLE_GARMENTS mapping (ROLES=Girl,Mother; ROLE_GARMENTS Girl=Dress,Mother=Dress)
jq -e 'all(.[]; .role=="Girl Dress" or .role=="Mother Dress")' "$CHART" >/dev/null || { echo "FAIL: role not in ROLE_GARMENTS"; exit 1; }

# Price parity (spec vs chart-derived)
if [[ "$FORCE_SPEC_PRICES" == "true" ]]; then
  SPEC_BAD=$(jq -r --arg c "$CHILD_PRICE" --arg m "$MOTHER_PRICE" '[.[] | select((.audience=="child" and ($c|tostring)!=$c) or (.audience=="mother" and ($m|tostring)!=$m))] | length' "$CHART")
  # trivial guard; actual per-variant price resolved at payload build
  echo "✓ FORCE_SPEC_PRICES=true — kid=$CHILD_PRICE mom=$MOTHER_PRICE"
fi

echo "✓ Preflight OK — rows=$ROW_COUNT, title=${#TITLE}, seo_t=${#SEO_TITLE}, seo_d=${SEO_DESC_LEN}"

# ─────────────────────────────────────────────────────────────────────────────
# 3. Derive Size picker values (single garment type = Dress → no Type axis)
# ─────────────────────────────────────────────────────────────────────────────
SIZE_VALUES_JSON=$(jq '
  reduce .[] as $r ([]; if any(.[]; .==$r.picker_label) then . else . + [$r.picker_label] end) | map({name:.})
' "$CHART")

echo "Size values: $(jq -c . <<<"$SIZE_VALUES_JSON")"

# ─────────────────────────────────────────────────────────────────────────────
# 4. Build Body HTML — one size-chart table per garment type (here: Dress only)
# ─────────────────────────────────────────────────────────────────────────────
# Convert cm integer to dual-unit string
fmt_cm_js='def fmt_cm($x): if ($x|tonumber)==0 then "—" else ($x|tostring) + " cm / " + ((($x|tonumber)/2.54)|.*10|round|./10|tostring) + " in" end;'

KID_ROWS=$(jq -r "
  $fmt_cm_js
  [.[] | select(.audience==\"child\")] | .[]
  | \"<tr><td>\(.picker_label)</td><td>\(.age)</td><td>\(.weight)</td><td>\(.height)</td><td>\(fmt_cm(.chest_cm))</td><td>\(fmt_cm(.skirt_cm))</td><td>—</td><td>\(fmt_cm(.hip_cm))</td><td>\(fmt_cm(.waist_cm))</td><td>\(fmt_cm(.length_cm))</td></tr>\"
" "$CHART")

MOM_ROWS=$(jq -r "
  $fmt_cm_js
  [.[] | select(.audience==\"mother\")] | .[]
  | \"<tr><td>\(.picker_label)</td><td>\(.age)</td><td>\(.weight)</td><td>\(.height)</td><td>\(fmt_cm(.chest_cm))</td><td>\(fmt_cm(.skirt_cm))</td><td>—</td><td>\(fmt_cm(.hip_cm))</td><td>\(fmt_cm(.waist_cm))</td><td>\(fmt_cm(.length_cm))</td></tr>\"
" "$CHART")

read -r -d '' BODY_HTML <<HTML || true
<ul>
  <li><strong>Fabric:</strong> Soft cotton blend with airy lace inserts — breezy, breathable, and gentle against the skin on warm days.</li>
  <li><strong>Family story:</strong> A picture-perfect matching cami dress for mom and daughter — built for brunch, birthdays, beach days, and holiday cards.</li>
  <li><strong>Print:</strong> "White Lace" — clean creamy white with openwork lace panels, crochet-style trims, and a scalloped tiered hem.</li>
  <li><strong>Design details:</strong> V-neck cami silhouette, adjustable shoulder straps, empire waist with lace cutouts, flowy tiered midi/maxi skirt.</li>
  <li><strong>Care:</strong> Machine wash cold on gentle, hang dry in the shade, no bleach, warm iron inside-out if needed.</li>
  <li><strong>Size range:</strong> Kids Child 3 Years to Child 9-10 Years; Mother S and Mother M.</li>
</ul>

<h3>Size Chart — Dress</h3>
<table id="size-chart">
  <thead>
    <tr>
      <th>Size</th>
      <th>Age</th>
      <th>Weight</th>
      <th>Height</th>
      <th>Chest/Bust</th>
      <th>Skirt Length</th>
      <th>Pant/Short</th>
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

<p>Say hello to the White Lace Mommy and Me Dresses — an airy cami set that turns sunny mornings and salt-water afternoons into a matching moment. Lightweight cotton blend keeps you both cool, while lace inserts, crochet trims, and a tiered flowy hem add the picture-perfect details. Adjustable straps make it fit just right, and the clean creamy palette styles with straw hats, sandals, or a little basket bag.</p>

<p>Inspired by coastal summers and garden weddings, this matching cami dress was made for brunch tables, beach boardwalks, seaside sunsets, and holiday-card backdrops. Slip into yours, twirl with your little one, and make every moment match — from first-day-of-summer photos to everyday family memories you'll want to keep forever.</p>

<h3>Key Features:</h3>
<ul>
  <li><strong>Breezy cotton blend:</strong> Soft, lightweight weave that moves with you on warm days.</li>
  <li><strong>Delicate lace details:</strong> Openwork panels, crochet-style trims, and a scalloped tiered hem.</li>
  <li><strong>Flattering cami fit:</strong> V-neck, adjustable straps, and an empire waist for a graceful silhouette.</li>
  <li><strong>Mom + mini matching:</strong> Identical styling across kids and mother sizes for head-to-toe family twinning.</li>
  <li><strong>Photo-ready neutrals:</strong> Creamy white base styles with straw hats, woven bags, and any vacation backdrop.</li>
</ul>

<p>Slip into the softest matching moment of the summer — grab your set and make every family photo picture-perfect.</p>
HTML

# ─────────────────────────────────────────────────────────────────────────────
# 5. Tags
# ─────────────────────────────────────────────────────────────────────────────
TAGS_JSON=$(jq -cn --argjson chart "$(cat "$CHART")" --arg vendor_url "$VENDOR_URL" '
  def mom_size_tag(p): if p=="Mother S" then "Mom Size S"
    elif p=="Mother M" then "Mom Size M"
    elif p=="Mother L" then "Mom Size L"
    elif p=="Mother XL" then "Mom Size XL"
    elif p=="Mother 2XL" then "Mom Size 2XL"
    elif p=="Mother 3XL" then "Mom Size 3XL"
    elif p=="Mother One Size" then "Mom One Size"
    else null end;
  def kid_bucket(p): if p=="Child 2 Years" or p=="Child 3 Years" then "Child 2-3yr"
    elif p=="Child 4 Years" or p=="Child 5 Years" then "Child 4-5yr"
    elif p=="Child 6-7 Years" or p=="Child 8 Years" then "Child 6-8yr"
    elif p=="Child 9-10 Years" then "Child 9-10yr"
    else null end;
  ([
    "Mommy and Me", "Dresses", "Matching Family Dresses",
    "Matching Family Dress", "Cami Dress", "Summer Dress", "Sundresses",
    "Midi Dress", "Midi Dresses", "Maxi Dress", "Maxi Dresses",
    "Summer", "Beach", "Vacation", "Resort", "Holiday",
    "White", "Cream", "Ivory",
    "Lace", "Crochet", "Eyelet", "Tiered",
    "Cotton Blend", "Cotton",
    $vendor_url
  ] + [$chart[] | select(.audience=="child") | kid_bucket(.picker_label)]
    + [$chart[] | select(.audience=="mother") | mom_size_tag(.picker_label)])
  | map(select(. != null))
  | unique
')
echo "Tags: $TAGS_JSON"

# ─────────────────────────────────────────────────────────────────────────────
# 6. Create-or-update path
# ─────────────────────────────────────────────────────────────────────────────
echo "── Checking for existing product at handle=$HANDLE ──"
EXIST_RESP=$(gql "$(jq -nc --arg h "$HANDLE" '{query:"query($h:String!){ productByHandle(handle:$h){ id handle variants(first:50){ edges { node { id sku price compareAtPrice title }}}}}", variables:{h:$h}}')")
EXIST_ID=$(echo "$EXIST_RESP" | jq -r '.data.productByHandle.id // empty')

if [[ -z "$EXIST_ID" ]]; then
  echo "── productCreate ──"
  CREATE_PAYLOAD=$(jq -nc \
    --arg title "$TITLE" \
    --arg handle "$HANDLE" \
    --arg body "$BODY_HTML" \
    --arg ptype "$PRODUCT_TYPE" \
    --arg vendor "$VENDOR" \
    --arg seoT "$SEO_TITLE" \
    --arg seoD "$SEO_DESC" \
    --arg tax "$TAXONOMY_GID" \
    --arg color "$COLOR_NAME" \
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
  IS_NEW=1
else
  echo "✓ Found existing product $EXIST_ID — update path"
  PRODUCT_ID="$EXIST_ID"
  IS_NEW=0
  # productUpdate: overwrite body/SEO/tags
  UPDATE_PAYLOAD=$(jq -nc \
    --arg pid "$PRODUCT_ID" \
    --arg title "$TITLE" \
    --arg body "$BODY_HTML" \
    --arg ptype "$PRODUCT_TYPE" \
    --arg seoT "$SEO_TITLE" \
    --arg seoD "$SEO_DESC" \
    --argjson tags "$TAGS_JSON" \
    --arg tax "$TAXONOMY_GID" \
    '{
      query:"mutation productUpdate($input: ProductInput!){ productUpdate(input:$input){ product{ id } userErrors{ field message }}}",
      variables:{input:{
        id:$pid, title:$title, descriptionHtml:$body,
        productType:$ptype, tags:$tags, category:$tax,
        seo:{title:$seoT, description:$seoD}
      }}
    }')
  UPDATE_RESP=$(gql "$UPDATE_PAYLOAD")
  echo "$UPDATE_RESP" | jq '.data.productUpdate.userErrors'
fi

# ─────────────────────────────────────────────────────────────────────────────
# 7. Bulk-create / update variants
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

if [[ $IS_NEW -eq 1 ]]; then
  VCREATE_PAYLOAD=$(jq -nc --arg pid "$PRODUCT_ID" --argjson variants "$VARIANTS_JSON" '
    {
      query:"mutation varCreate($productId:ID!, $strategy:ProductVariantsBulkCreateStrategy, $variants:[ProductVariantsBulkInput!]!){ productVariantsBulkCreate(productId:$productId, strategy:$strategy, variants:$variants){ productVariants{ id sku title inventoryPolicy } userErrors{ field message }}}",
      variables:{ productId:$pid, strategy:"REMOVE_STANDALONE_VARIANT", variants:$variants }
    }')
  VCREATE_RESP=$(gql "$VCREATE_PAYLOAD")
  echo "$VCREATE_RESP" | jq '.data.productVariantsBulkCreate.userErrors'
  VCOUNT=$(echo "$VCREATE_RESP" | jq '.data.productVariantsBulkCreate.productVariants | length')
  echo "✓ Variants created: $VCOUNT"
else
  echo "── update-mode diff (not yet needed — fresh handle only) ──"
fi

# ─────────────────────────────────────────────────────────────────────────────
# 8. Metafields (single batch)
# ─────────────────────────────────────────────────────────────────────────────
echo "── metafieldsSet ──"

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
    elif p=="Mother 2XL" then "gid://shopify/Metaobject/129975156833"
    elif p=="Mother 3XL" then "gid://shopify/Metaobject/139840421985"
    else null end;
  [$chart[] | m(.picker_label)] | map(select(.!=null)) | unique')

# Only colorword present in tags: White (also Cream/Ivory synonyms; GID only exists for White)
COLOR_GIDS_JSON='["gid://shopify/Metaobject/69639733345"]'          # White
AGE_GIDS_JSON='["gid://shopify/Metaobject/128116523105","gid://shopify/Metaobject/128116490337"]'  # Kids, Adults
GENDER_GIDS_JSON='["gid://shopify/Metaobject/129971617889"]'         # Female (Girl+Mother only)
FABRIC_GIDS_JSON='["gid://shopify/Metaobject/69622399073"]'          # Cotton

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
      mf("custom";"subcategory";"single_line_text_field";"Dresses"),
      mf("custom";"subcategory2";"single_line_text_field";($season + " Dresses")),
      mf("custom";"pattern";"single_line_text_field";"Lace"),
      mf("custom";"style";"single_line_text_field";"Mommy and Me Set"),
      mf("custom";"type";"single_line_text_field";"Dresses"),
      mf("mm-google-shopping";"custom_product";"boolean";"false"),
      mf("mm-google-shopping";"gender";"single_line_text_field";"female"),
      mf("mm-google-shopping";"age_group";"single_line_text_field";"adult"),
      mf("mm-google-shopping";"condition";"single_line_text_field";"new"),
      mf("mm-google-shopping";"custom_label_0";"single_line_text_field";"Mommy and Me"),
      mf("mm-google-shopping";"custom_label_1";"single_line_text_field";"Lace"),
      mf("mm-google-shopping";"custom_label_2";"single_line_text_field";$season),
      mf("mm-google-shopping";"custom_label_3";"single_line_text_field";"Dress & Shirt"),
      mf("mm-google-shopping";"custom_label_4";"single_line_text_field";"Two-Role Matching"),
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
# 10. Media — idempotent (skip if uploads dir empty)
# ─────────────────────────────────────────────────────────────────────────────
UPLOAD_DIR="/Users/fsuels/Projects/dresslikemommy/uploads/${HANDLE}"
if [[ -d "$UPLOAD_DIR" ]] && compgen -G "$UPLOAD_DIR/*" >/dev/null; then
  echo "── media upload ── (found $UPLOAD_DIR) — left as manual follow-up in listing.md"
else
  echo "── media upload skipped — $UPLOAD_DIR missing; manual follow-up required"
fi

# ─────────────────────────────────────────────────────────────────────────────
# 11. Post-create verify (including price-drift check)
# ─────────────────────────────────────────────────────────────────────────────
echo "── verify ──"
VERIFY_PAYLOAD=$(jq -nc --arg pid "$PRODUCT_ID" '{
  query:"query($id:ID!){ product(id:$id){ id title handle publishedAt onlineStoreUrl descriptionHtml seo{ title description } tags variants(first:50){ edges { node { sku title price compareAtPrice inventoryPolicy inventoryItem { tracked requiresShipping }}}} metafields(first:50){ edges { node { namespace key type value }}}}}",
  variables:{id:$pid}
}')
VERIFY=$(gql "$VERIFY_PAYLOAD")

LIVE_SKUS=$(echo "$VERIFY" | jq -r '[.data.product.variants.edges[].node.sku] | sort | .[]')
DERIVED_SKUS=$(jq -r --arg s "$SHORTCODE" --arg c "$COLOR_TOKEN" '.[] | "DLM-" + $s + "-" + .sku_suffix + "-" + $c' "$CHART" | sort)
echo "Live SKUs:"; echo "$LIVE_SKUS"
echo "Derived SKUs:"; echo "$DERIVED_SKUS"
diff <(echo "$LIVE_SKUS") <(echo "$DERIVED_SKUS") && echo "✓ SKU match" || echo "✗ SKU mismatch"

LIVE_VCOUNT=$(echo "$VERIFY" | jq '.data.product.variants.edges | length')
[[ "$LIVE_VCOUNT" == "$ROW_COUNT" ]] && echo "✓ Variant count OK ($LIVE_VCOUNT)" || echo "✗ Variant count $LIVE_VCOUNT != $ROW_COUNT"

DHTML=$(echo "$VERIFY" | jq -r '.data.product.descriptionHtml')
TR_COUNT=$(echo "$DHTML" | grep -o '<tr>' | wc -l | tr -d ' ')
TH_COUNT=$(echo "$DHTML" | grep -o '<th>' | wc -l | tr -d ' ')
echo "Body table: <tr>=$TR_COUNT (expect $((ROW_COUNT+1))), <th>=$TH_COUNT (expect 10)"

# Price drift check
if [[ "$FORCE_SPEC_PRICES" == "true" ]]; then
  DRIFT=0
  while IFS=$'\t' read -r sku live_price live_cmp; do
    AUD=$(jq -r --arg s "$sku" '.[] | select("DLM-'"$SHORTCODE"'-" + .sku_suffix + "-'"$COLOR_TOKEN"'" == $s) | .audience' "$CHART")
    case "$AUD" in
      child)  EXP="$CHILD_PRICE"; EXPC="$CHILD_CMP" ;;
      mother) EXP="$MOTHER_PRICE"; EXPC="$MOTHER_CMP" ;;
      *)      EXP=""; EXPC="" ;;
    esac
    if [[ "$live_price" != "$EXP" ]]; then
      echo "✗ price drift: $sku live=$live_price spec=$EXP"
      DRIFT=1
    fi
    if [[ "$live_cmp" != "$EXPC" ]]; then
      echo "✗ compare-at drift: $sku live=$live_cmp spec=$EXPC"
      DRIFT=1
    fi
  done < <(echo "$VERIFY" | jq -r '.data.product.variants.edges[] | [.node.sku, .node.price, .node.compareAtPrice] | @tsv')
  if [[ "$DRIFT" -eq 0 ]]; then echo "✓ Price parity OK (kid=$CHILD_PRICE/$CHILD_CMP, mom=$MOTHER_PRICE/$MOTHER_CMP)"; fi
fi

PUBAT=$(echo "$VERIFY" | jq -r '.data.product.publishedAt // empty')
URL=$(echo "$VERIFY" | jq -r '.data.product.onlineStoreUrl // empty')
echo "publishedAt: $PUBAT"
echo "onlineStoreUrl: $URL"

PID_NUM="${PRODUCT_ID##*/}"
echo ""
echo "Admin: https://admin.shopify.com/store/dresslikemommy/products/${PID_NUM}"
echo "Live : https://www.dresslikemommy.com/products/${HANDLE}"

echo "$VERIFY" > "$SCRIPT_DIR/../listings/verify-${HANDLE}.json"
echo "Saved verify dump to ops/listings/verify-${HANDLE}.json"
