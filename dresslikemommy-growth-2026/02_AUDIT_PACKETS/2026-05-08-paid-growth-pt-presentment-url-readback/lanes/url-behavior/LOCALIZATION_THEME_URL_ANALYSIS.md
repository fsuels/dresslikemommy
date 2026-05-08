# Local Market-Localized Ad URL Behavior Analysis

Generated: 2026-05-08 EDT

Assigned lane: local-only analysis for market-localized paid URL behavior. No browser tests, Shopify Admin writes, theme edits, Markets/currency/shipping changes, Ads/Merchant/Pinterest writes, payment, or order were performed by this sidecar.

## Decision

`THEME_ANALYSIS_ONLY__BARE_LANGUAGE_ROUTES_NOT_PROVEN_SAFE_FOR_PAID_TRAFFIC`

The local theme shows two different mechanisms:

- Language route links are built from `language.root_url` and the current path.
- Country/currency presentment is set through Shopify's localization form with `country_code`.

That matches the prior browser evidence: direct `/es`, `/it`, `/ro`, and `/pt` routes can land as English / United States / USD, while storefront localization can correct product/cart/checkout presentment after it is set.

## How The Current Selector Works

### Selector loading

- `layout/theme.liquid` loads `component-localization-form.css` and `localization-form.js` when the shop has multiple countries or languages.
- Header settings enable both country and language selectors in `sections/header-group.json`.
- Announcement-bar selectors are disabled in `sections/header-group.json`.
- Footer currently enables the language selector only, not country.

### Header and mobile selector surfaces

- Desktop header renders separate Shopify localization forms:
  - `HeaderCountryForm` wraps the country selector.
  - `HeaderLanguageForm` wraps the language selector.
- Mobile drawer renders separate forms too:
  - `HeaderCountryMobileForm`
  - `HeaderLanguageMobileForm`

### Country selector

- `snippets/country-localization.liquid` displays the active `localization.country.name`, currency ISO code, and currency symbol.
- Country options are anchors with `href="#"` and `data-value="{{ country.iso_code }}"`.
- The form contains a hidden input named `country_code`.
- This means the local country selector is not a GET URL mechanism. It depends on form submission to Shopify's localization endpoint.

### Language selector

- `snippets/language-localization.liquid` computes `locale_relative_path` from `request.path`.
- It builds a fallback `href` from each `language.root_url` plus the current relative path.
- The form contains a hidden input named `locale_code`.
- On normal storefront hosts, the JS intercepts the language anchor click and submits the localization form. On localhost only, it follows the fallback route URL because the Shopify preview proxy can return `401` for `/localization` POST.

### JavaScript submit behavior

- `assets/localization-form.js` looks for one hidden input named either `locale_code` or `country_code`.
- On item click, it takes the clicked anchor's `data-value`, writes it into that hidden input, and calls `form.submit()`.
- If no form/hidden input path is available, it can fall back to the anchor `href`; for country links that fallback is only `#`.

## What This Means For Paid URLs

The theme currently does not include local code that reads URL parameters such as `country`, `currency`, `locale`, `country_code`, or a custom ad parameter and then sets Shopify market presentment.

The local language-route logic can build URLs like `/pt/products/...`, but local theme code alone does not make that route set Portugal/EUR. Country selection is a separate form submit with `country_code=PT`.

Therefore, unless parent browser tests prove a native Shopify URL/query pattern reliably sets country and currency for a fresh visitor, bare language-path ad final URLs should stay blocked for ES/IT/RO/PT paid traffic.

## Prior Evidence Used

Prior parent browser evidence in `2026-05-07-paid-growth-currency-presentment-readback` found:

| Market | Fresh direct route | After storefront localization |
|---|---|---|
| ES | Direct `/es` first landed English / US / USD | Spain / Spanish / EUR; checkout shipping step reached |
| IT | Direct `/it` first landed English / US / USD | Italy / Italian / EUR; checkout shipping step reached |
| RO | Direct `/ro` first landed English / US / USD | Romania / Romanian / RON; checkout shipping step reached |
| PT | Direct `/pt` first landed English / US / USD | Portugal / pt-BR / EUR on product page; checkout blocked by `429` |

Endpoint-only cart-rate checks also returned USD when storefront market localization was not set. That is consistent with the local theme: the cart/SEO/analytics currency signals derive from `cart.currency.iso_code` or `localization.country.currency.iso_code`, so a US-localized session reports USD.

## Related Theme Observations

SEO and structured data are downstream of market state:

- `snippets/meta-tags.liquid` sets product price currency from `cart.currency.iso_code`, then `localization.country.currency.iso_code`, then shop currency.
- `snippets/jsonld-seo.liquid` uses the same currency fallback and uses `localization.country.iso_code` for shipping destination/return policy structured data.
- Hreflang alternates are generated from language roots and current relative path. They are SEO hints, not a country/currency setter.

Parameterized product URLs:

- `layout/theme.liquid` strips query parameters from product canonicals.
- Any product page with a query string sets `parameterized_product_noindex`.
- This is not automatically bad for paid traffic, but if a future paid URL helper uses query params, it should redirect/clean the URL after setting localization and preserve attribution parameters intentionally.

Cart/add locale nuance:

- `assets/cart.js` has a helper that prefixes cart endpoints with `window.Shopify.routes.root` for locale-aware cart operations.
- `assets/product-form.js` and `assets/product-desktop-ux.js` still fetch `routes.cart_add_url` directly.
- This does not force country/currency, but if parent keeps seeing localized PT product pages post to non-localized `/cart/add` routes, a future theme-local patch could normalize add-to-cart endpoints with the same locale-aware route helper. That would require theme edit/publish approval and checkout QA.

## Local-Only Options If Browser Tests Fail

These are analysis-only options. None were implemented.

1. Use only browser-proven native URL templates if they work.
   - If parent proves a Shopify-native GET pattern reliably lands fresh PT visitors in Portugal / EUR and preserves checkout, use that exact tested final URL template.
   - Do not infer this from language paths alone.

2. Add a theme-level ad-localization handoff for explicit ad parameters.
   - Example ad final URL shape: `/pt/products/<handle>?dlm_country=PT&dlm_locale=pt-BR&utm_source=google...`
   - Theme JS would run only when explicit `dlm_country` / `dlm_locale` params exist.
   - It would compare the requested country/locale to Liquid-rendered current country/locale, submit a Shopify localization POST with `country_code`, `locale_code`, and a safe `return_to`, then stop.
   - It must preserve `utm_*`, `gclid`, `gbraid`, `wbraid`, `gad_source`, and other attribution parameters or intentionally hand them back after redirect.
   - It must prevent loops with sessionStorage and a current-state check.
   - This needs approval, implementation, preview QA, and live publish approval.

3. Add a dedicated localization handoff landing route.
   - A small page/template can receive target country/locale/return path, set Shopify localization, then forward to the product/collection.
   - This keeps forcing logic away from every product page and can be kept out of SEO indexing.
   - It adds one redirect/reload to ad traffic, so it needs speed and conversion QA.

4. If needed, patch locale-aware add-to-cart consistency.
   - This would not solve initial market selection.
   - It may reduce route/currency friction after localization if product add-to-cart still posts to the wrong locale root.

5. Shopify Markets/Admin configuration review.
   - If native market domains/subfolders or country redirects are the right durable answer, that is outside this sidecar's local-only scope and requires explicit Admin/Markets approval.

## Not Recommended

- Do not treat hreflang/canonical changes as a market presentment fix.
- Do not rely on the visible selector alone for paid traffic.
- Do not create physical-store, warehouse, local-inventory, stocked-inventory, pickup, or guaranteed on-hand-stock claims.
- Do not change Shopify Markets, shipping rates, product data, Merchant feeds, or Ads URLs live without parent approval.

## File References

- `assets/localization-form.js`: hidden `locale_code`/`country_code` selection and form submit behavior.
- `snippets/country-localization.liquid`: country options and hidden `country_code`.
- `snippets/language-localization.liquid`: language root URL construction and hidden `locale_code`.
- `sections/header.liquid`: desktop header country/language forms.
- `snippets/header-drawer.liquid`: mobile drawer country/language forms.
- `sections/footer.liquid`: footer localization forms.
- `sections/header-group.json`: header selectors enabled, announcement selectors disabled.
- `sections/footer-group.json`: footer language enabled, footer country disabled.
- `layout/theme.liquid`: localization asset loading, product query canonical/noindex behavior, global cart route variables.
- `snippets/meta-tags.liquid`: product price currency and hreflang generation.
- `snippets/jsonld-seo.liquid`: structured data currency and country usage.
- `assets/cart.js`, `assets/product-form.js`, `assets/product-desktop-ux.js`: locale-aware cart route behavior is inconsistent across cart vs product add-to-cart code paths.

## Guardrails Preserved

- No theme edits.
- No Shopify Admin, Markets, currency, shipping-rate, or product-data writes.
- No Google Ads, Merchant, Pinterest, feed, catalog, campaign, budget, bid, status, conversion-goal, product-scope, feed-label, product-group, or pixel writes.
- No payment and no order.
