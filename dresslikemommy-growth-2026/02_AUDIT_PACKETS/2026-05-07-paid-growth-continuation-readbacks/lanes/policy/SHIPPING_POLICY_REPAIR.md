# Shipping/Policy Copy Repair Lane

Generated: 2026-05-07

Scope: read-only policy/copy repair planning for the paid-growth continuation sprint. No Shopify Admin writes, no theme edits, no theme publish, no shipping-rate changes, no market changes, no ad/feed/campaign changes, and no checkout payment steps were performed.

## Decision

The blocker copy is Shopify Admin-managed content, not a local theme source.

Owner correction: Dress Like Mommy is a dropshipping business. It does not have a physical store and does not hold owned physical inventory. All replacement copy below must be read as policy/checkout availability copy only; do not add language that implies a retail location, a warehouse, stocked local inventory, or guaranteed on-hand stock. For customer-facing copy, use neutral wording such as "online store", "shipping partners", and "shown at checkout" unless the owner explicitly requests public use of the word "dropshipping".

Do not patch theme files for this issue. The Dawn theme only renders or links the Admin-managed content:

- `sections/main-page.liquid:22` renders `{{ page.content }}` for Shopify pages.
- `templates/page.json` uses `main-page`.
- `sections/home-conversion-hero.liquid:5` and `sections/hero-banner.liquid:710` link to `shop.shipping_policy.url`, but do not contain the country-list blocker text.

Target Admin-managed surfaces:

| Public surface | Source evidence | Source type | Repair needed |
|---|---|---|---|
| `/policies/shipping-policy` | `parent-country-admin-checkout/policies_admin_readback.json`, `SHOP_POLICY::29845782625` in `ops/content/shopify-live-digest-map.json`, public readback | Shopify policy | Replace country-list and delivery/rates sections |
| `/pages/shipping-info` | `PAGE::86424617057` in `ops/content/shopify-live-digest-map.json`, public readback | Shopify page | Replace body copy sections that say worldwide but list only four countries |
| `/policies/terms-of-service` | `parent-country-admin-checkout/policies_admin_readback.json`, `SHOP_POLICY::14695813` in `ops/content/shopify-live-digest-map.json`, public readback | Shopify policy | Replace section 3 price sentence and section 5 shipping list |
| Legacy `/pages/shipping-and-delivery` page | Existing lane dry-run shows page `161928901`, handle `shipping-and-delivery` | Shopify page, legacy/redirect surface | Recheck after approval; update or redirect only if still public/crawlable |

An existing dry-run summary is present at `admin-page-policy-readonly-dry-run/summary.json`. I read it and did not overwrite it. It confirms the legacy page `161928901` currently carries the same Shipping Policy country-list blocker. Full before/after body JSONs were pruned from this packet so outdated physical-location/warehouse wording is not preserved as reusable evidence.

## Exact Blocker Text/Locations

### Shipping Policy

Source: `/policies/shipping-policy`, Admin policy handle `shipping-policy`.

Blocker:

> Where We Ship We currently ship to: United States (all 50 states + territories) Canada United Kingdom Australia Can’t find your country? Contact us at info@dresslikemommy.com — we may be able to arrange shipping to additional destinations.

Related mismatch:

> Delivery Times Estimated delivery times after your order has been processed and shipped: United States: 7–15 business days (standard) | 5–7 business days (express, where available) Canada: 10–20 business days United Kingdom: 10–20 business days Australia: 12–25 business days

Why it blocks paid growth: Admin shipping and checkout evidence show broader country availability, but this public policy implies only four standard destinations.

### Shipping Info Page

Source: `/pages/shipping-info`, Shopify page `PAGE::86424617057`, handle `shipping-info`.

Blockers:

> At Dress Like Mommy, we ship matching family outfits to families worldwide.

Then, on the same page:

> Where We Ship United States — all 50 states + territories Canada United Kingdom Australia Don’t see your country? Email us at info@dresslikemommy.com — we may be able to arrange shipping.

Related mismatch:

> Delivery Times Estimated delivery times after your order ships: United States: 7–12 business days Canada: 10–15 business days United Kingdom: 10–15 business days Australia: 12–20 business days

Why it blocks paid growth: the page both overclaims "worldwide" and underclaims standard shipping availability by listing only `US`, `CA`, `GB`, and `AU`.

### Terms Of Service

Source: `/policies/terms-of-service`, Admin policy handle `terms-of-service`.

Blockers:

> All prices are in USD unless otherwise noted

> 5. Shipping and Delivery We ship to the United States, Canada, United Kingdom, and Australia

Why it blocks paid growth: broader markets/currencies appear in country selectors, but Terms still name only the four current visible destinations and imply USD as the default across all markets.

## Ready-To-Apply Replacement Copy

These are section-level replacements, not full legal rewrites. They preserve the current business posture while removing the four-country-only blocker and avoiding a blind "worldwide" promise.

### Shipping Policy: Replace "Where We Ship"

```html
<h2>Where We Ship</h2>
<p>Shipping is available to the countries and regions shown at checkout. Availability depends on the destination, product, and shipping methods shown during checkout. Use the country/region selector or the checkout shipping step to confirm whether we can ship to your address before placing an order.</p>
<p>If your destination does not appear at checkout, or if no shipping method is shown for your address, contact us at <a href="mailto:info@dresslikemommy.com">info@dresslikemommy.com</a> before ordering.</p>
```

### Shipping Policy: Replace "Shipping Rates"

```html
<h2>Shipping Rates</h2>
<p>Available shipping methods and rates are shown at checkout before payment. Standard shipping is free when a free standard method is shown for your destination. Express or paid options may be available for some addresses and will display before you place the order.</p>
```

### Shipping Policy: Replace "Delivery Times"

```html
<h2>Delivery Times</h2>
<p>Orders are processed within 1-3 business days after payment confirmation. Delivery estimates vary by destination, carrier, customs processing, and the shipping method shown at checkout.</p>
<ul>
  <li><strong>Standard Delivery:</strong> the current checkout estimate displays before payment.</li>
  <li><strong>Express Delivery:</strong> available for some destinations where shown at checkout.</li>
</ul>
<p>These are estimates. Actual delivery times may vary because of customs processing, carrier delays, weather, holidays, or local conditions.</p>
```

### Shipping Policy: Keep/Refresh Customs And Duties

```html
<h2>Customs, Duties, And Import Taxes</h2>
<p>For orders shipped outside the United States, your destination country or carrier may collect import duties, taxes, brokerage fees, or customs charges. These charges are the customer's responsibility unless checkout explicitly says they are included.</p>
<p>We cannot predict these charges, mark orders as gifts, or lower the declared value of an order. Contact your local customs office for destination-specific guidance before ordering.</p>
```

### Shipping Info Page: Replace Opening And Country Sections

```html
<h2>Shipping Information</h2>
<p>At <strong>Dress Like Mommy</strong>, we are an online store that ships matching family outfits to destinations available at checkout through our shipping and fulfillment partners. Here is how to confirm shipping, delivery timing, and tracking before you place an order.</p>

<h3>Free And Paid Shipping Options</h3>
<p>Available shipping methods and rates are shown at checkout before payment. Standard shipping is free when a free standard method is shown for your destination. Express or paid options may be available for some addresses.</p>

<h3>Where We Ship</h3>
<p>Shipping availability is based on the country/region and address entered at checkout. If checkout shows a shipping method for your address, we can ship there under the displayed method and rate.</p>
<p>If your destination does not appear at checkout, or if no shipping method is shown, email us at <a href="mailto:info@dresslikemommy.com">info@dresslikemommy.com</a> before ordering.</p>
```

### Shipping Info Page: Replace Delivery Times

```html
<h3>Processing And Delivery Times</h3>
<p>Orders are processed within 1-3 business days after payment confirmation. During holidays, promotions, or high-volume periods, processing may take an additional 1-2 business days.</p>
<p>Delivery estimates vary by destination, carrier, customs processing, and the shipping method shown at checkout. Review the shipping method and estimate shown during checkout before placing your order.</p>
<p>Tracking may take 24-48 hours to update after the tracking number is issued.</p>
```

### Shipping Info Page: Keep/Refresh Customs And Duties

```html
<h3>Customs, Duties, And Import Taxes</h3>
<p>For orders outside the United States, your destination country or carrier may collect import duties, taxes, brokerage fees, or customs charges. These are the customer's responsibility unless checkout explicitly says they are included.</p>
<p>We cannot predict these charges, mark orders as gifts, or lower the declared value of an order. Contact your local customs office for destination-specific guidance before ordering.</p>
```

### Terms Of Service: Replace Pricing Sentence In Section 3

```html
<li>Prices display in the currency selected or shown at checkout unless otherwise noted.</li>
```

### Terms Of Service: Replace Section 5 "Shipping And Delivery"

```html
<h2>5. Shipping and Delivery</h2>
<ul>
  <li>Dress Like Mommy is an online store. Shipping is available to countries and regions where checkout shows an available shipping method for the address entered.</li>
  <li>Processing time is typically 1-3 business days after payment confirmation.</li>
  <li>Available shipping methods, rates, delivery estimates, taxes, and duties information are shown at checkout before payment where available.</li>
  <li>Standard shipping is free when a free standard method is shown for your destination.</li>
  <li>Express shipping may be available for some destinations where shown at checkout.</li>
  <li>Tracking information is provided by email once the order ships.</li>
  <li>We are not responsible for delays caused by customs, weather, holidays, carrier issues, or local delivery conditions.</li>
</ul>
<p>For full shipping details, see our <a href="https://www.dresslikemommy.com/pages/shipping-info">Shipping Information</a> page.</p>
```

## Approval-Gated Next Action

Required owner approval phrase before any Shopify Admin write:

```text
APPROVE SHIPPING POLICY COPY REPAIR: UPDATE SHOPIFY ADMIN SHIPPING POLICY, SHIPPING INFO PAGE, AND TERMS SHIPPING SECTION USING THE 2026-05-07 POLICY LANE DRAFT; DO NOT CHANGE THEME, PRODUCTS, SHIPPING RATES, MARKETS, ADS, FEEDS, BUDGETS, CAMPAIGN STATUSES, OR CONVERSION GOALS; READ BACK PUBLIC PAGES AFTER SAVE.
```

After approval:

1. Open Shopify Admin only in the parent-approved browser/account session.
2. Update Settings > Policies > Shipping policy using the section replacements above.
3. Update Online Store > Pages > Shipping Info (`PAGE::86424617057`, handle `shipping-info`) using the section replacements above.
4. Update Settings > Policies > Terms of service section 3 pricing sentence and section 5 shipping block.
5. Recheck whether legacy page `PAGE::161928901`, handle `shipping-and-delivery`, is still public, redirected, linked, or indexed. If it is public/crawlable, apply the same neutral shipping copy or redirect it to `/pages/shipping-info` only with separate approval.
6. Read back public text for:
   - `https://www.dresslikemommy.com/policies/shipping-policy`
   - `https://www.dresslikemommy.com/pages/shipping-info`
   - `https://www.dresslikemommy.com/policies/terms-of-service`
7. Verify these phrases are absent from public pages:
   - `We currently ship to: United States`
   - `We ship to the United States, Canada, United Kingdom, and Australia`
   - `Don’t see your country?`
   - `we ship matching family outfits to families worldwide`
8. Only after public copy passes, run slow no-payment checkout QA for `NL`, `ES`, `IT`, `RO`, and `PT`. Copy repair alone is not approval for live international spend.

## Commands/Evidence Used

- `rg` scans of `templates`, `sections`, `snippets`, `config`, `locales`, `assets` for exact shipping blocker strings.
- `sed` reads of `sections/main-page.liquid`, `templates/page.json`, `sections/home-conversion-hero.liquid`, and `sections/hero-banner.liquid`.
- Prior packet: `2026-05-07-paid-growth-parallel-infra-sprint/localization-shipping-qa/LOCALIZATION_SHIPPING_QA_REPORT.md`.
- Prior packet: `2026-05-07-paid-growth-parallel-infra-sprint/parent-country-admin-checkout/policies_admin_readback.json`.
- Prior packet: `2026-05-07-paid-growth-parallel-infra-sprint/parent-country-admin-checkout/shipping_admin_readback.json`.
- Existing lane artifact: `admin-page-policy-readonly-dry-run/summary.json`. Full before/after page-body JSONs were intentionally pruned from this packet.
- Local Admin digest: `ops/content/shopify-live-digest-map.json`.
- Public read-only text extraction from `/policies/shipping-policy`, `/pages/shipping-info`, and `/policies/terms-of-service`.

## Residual Risks

- The replacement copy should receive owner/legal review because it touches public policy and Terms language.
- Checkout proof is still incomplete for `NL`, `ES`, `IT`, `RO`, and `PT`.
- Portuguese route QA remains blocked by prior `404`/`500` route findings.
- Translated versions of Admin-managed policy/page copy may need separate native/localization review after the English source is repaired.
