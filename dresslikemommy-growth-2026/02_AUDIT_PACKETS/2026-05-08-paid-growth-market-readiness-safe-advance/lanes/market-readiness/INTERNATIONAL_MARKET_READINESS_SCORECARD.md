# International Market Readiness Scorecard

Generated: 2026-05-08T23:59:35.904411-04:00

Decision: `NO_NON_US_MARKET_LIVE_SPEND_READY`. GB, CA, AU, ES, IT, RO, and PT have enough checkout or rate evidence to support paused infrastructure only, but remain approval-gated. CH, DK, DE, NL, SE, FR, BE, PL, CZ, and GR remain checkout-pending.

## Fresh Low-Volume Checks

- Requested cap: at most two fresh public/no-payment country checks, preferring CH and DK.
- Attempted: `1` country check(s).
- Stopped due to 429/CAPTCHA guardrail: `True`.
- CH result: product landing returned HTTP 200, retained `country=CH`, found expected CHF and `html lang=en`, but the body matched the verification/CAPTCHA detector before cart add. No cart, shipping-rate, checkout, payment, or order action was performed.
- DK result: not attempted because the CH guardrail stopped fresh probing.
- Note: prior landing-only evidence warned broad CAPTCHA strings can appear in ordinary Shopify script text. This lane still treated the fresh detector hit conservatively and stopped.

## Market Tier Table

| Market | Currency | Landing status | Checkout status | Blockers | Next safe QA | Paid status |
|---|---|---|---|---|---|---|
| GB - United Kingdom | GBP | 200 / en / GBP / country=GB retained | PASS checkout UI: en-GB, Standard FREE, Express GBP 10.00 | Known tested beach URL SEO/social title hold; Merchant/Pinterest/tracking/economics and exact owner approval still required. | Rerun just-in-time checkout UI and use a repaired/swapped final URL before enablement. | `approval-gated` |
| CA - Canada | CAD | 200 / en / CAD / country=CA retained | PASS checkout UI: en-CA, Standard FREE, Express CAD 19.00 | French Canada posture unresolved; tested beach URL SEO/social title hold; Merchant/Pinterest/tracking/economics and exact owner approval still required. | Rerun just-in-time checkout UI, decide French Canada handling, and use a repaired/swapped final URL before enablement. | `approval-gated` |
| AU - Australia | AUD | 200 / en / AUD / country=AU retained | PASS isolated checkout/UI: en-AU, Standard FREE, Express AUD approx 18.24 API / AUD display in UI | Prior 429 solved by isolated browser, but retest action-time; tested beach URL SEO/social title hold; parent gates and approval remain. | Rerun just-in-time isolated checkout, then parent tracking/catalog/economics gates. | `approval-gated` |
| ES - Spain | EUR | 200 / es / EUR / country=ES retained | PASS prior checkout to shipping after localization: Standard free, Express EUR 11.95 | Checkout mostly English in prior run; localized final URL works only when country-qualified; Merchant/Pinterest/tracking/economics and approval remain. | Rerun country-qualified localized UI and tracking/catalog readbacks before spend. | `approval-gated` |
| IT - Italy | EUR | 200 / it / EUR / country=IT retained | PASS prior checkout to shipping after localization: Standard free, Express EUR 11.95 | Checkout mostly English in prior run; Merchant/Pinterest/tracking/economics and approval remain. | Rerun country-qualified localized UI and tracking/catalog readbacks before spend. | `approval-gated` |
| RO - Romania | RON | 200 / ro / RON / country=RO retained | PASS prior checkout to shipping after localization: Standard free, Express RON 60.00 | RON economics required; checkout mostly English in prior run; Merchant/Pinterest/tracking/economics and approval remain. | Rerun country-qualified localized UI; model in RON with FX-normalized reporting. | `approval-gated` |
| PT - Portugal | EUR | 200 / pt-BR / EUR / country=PT retained | PASS checkout to shipping after cooldown: Standard free, Express EUR 11.95, total EUR 24.95 on test item | Uses pt-BR storefront copy for Portugal; Merchant/Pinterest/tracking/economics and approval remain. | Decide pt-BR acceptability; rerun just-in-time checkout and parent gates before spend. | `approval-gated` |
| CH - Switzerland | CHF | Prior: 200 / en / CHF / country=CH retained. Fresh: HTTP 200 and CHF found, then stopped before cart due verification/CAPTCHA text detector. | NO checkout/rate evidence. Fresh run did not add to cart. | Fresh broad detector saw verification/CAPTCHA text on product HTML, so guardrail stopped. Possible ordinary Shopify script false positive, but no cart/rate conclusion. Duties/language split also unresolved. | Cooldown, then one isolated browser no-payment checkout-to-shipping run for CH only; stop on visible 429/CAPTCHA. | `checkout-pending` |
| DK - Denmark | DKK | Prior: 200 / en / DKK / country=DK retained. Fresh DK not attempted because CH guardrail stopped probing. | NO checkout/rate evidence. | No fresh cart/rate proof; Danish language quality and DKK reporting unresolved. | After cooldown, one low-volume DK browser or endpoint checkout/shipping run; stop on 429/CAPTCHA. | `checkout-pending` |
| DE - Germany | EUR | Prior: 200 / en / EUR / country=DE retained | NO checkout/rate evidence. | German language/policy quality, checkout, catalog, tracking, economics unresolved. | Run one no-payment checkout/shipping QA and German landing/policy review. | `checkout-pending` |
| NL - Netherlands | EUR | Prior: 200 / en / EUR / country=NL retained | Earlier no-payment rate evidence mentioned in prior packets, not refreshed here. | Dutch language quality and fresh checkout proof unresolved; parent gates remain. | Refresh country-qualified checkout/rate proof and Dutch landing quality. | `checkout-pending` |
| SE - Sweden | SEK | Prior: 200 / en / SEK / country=SE retained | NO checkout/rate evidence. | Swedish language quality, SEK reporting, checkout, catalog, tracking, economics unresolved. | Run one no-payment checkout/shipping QA and Swedish landing/policy review. | `checkout-pending` |
| FR - France | EUR | Prior: 200 / en / EUR / country=FR retained | NO checkout/rate evidence. | French language/policy quality, checkout, catalog, tracking, economics unresolved. | Run one no-payment checkout/shipping QA and French landing/policy review. | `checkout-pending` |
| BE - Belgium | EUR | Prior: 200 / en / EUR / country=BE retained | NO checkout/rate evidence. | French/Dutch split, checkout, catalog, tracking, economics unresolved. | Run one no-payment checkout/shipping QA and decide FR/NL language split. | `checkout-pending` |
| PL - Poland | PLN | Prior: 200 / en / PLN / country=PL retained | NO checkout/rate evidence. | Polish language quality, PLN reporting, checkout, catalog, tracking, economics unresolved. | Run one no-payment checkout/shipping QA and Polish landing/policy review. | `checkout-pending` |
| CZ - Czechia | CZK | Prior: 200 / en / CZK / country=CZ retained | NO checkout/rate evidence. | Czech language quality, CZK reporting, checkout, catalog, tracking, economics unresolved. | Run one no-payment checkout/shipping QA and Czech landing/policy review. | `checkout-pending` |
| GR - Greece | EUR | Prior: 200 / en / EUR / country=GR retained | NO checkout/rate evidence. | Greek language quality, checkout, catalog, tracking, economics unresolved. | Run one no-payment checkout/shipping QA and Greek landing/policy review. | `checkout-pending` |

## Practical Tiers

- `approval-gated`: GB, CA, AU, ES, IT, RO, PT. These have checkout/rate evidence, but no live spend is cleared. Parent Merchant/Pinterest/tracking/economics gates, the beach URL hold, and exact owner approval still apply.
- `checkout-pending`: CH, DK, DE, NL, SE, FR, BE, PL, CZ, GR. These can remain paused-shell/local infrastructure candidates from landing evidence, but need one-country-at-a-time no-payment checkout/shipping QA before any spend discussion.
- `paused-shell-ready`: all 17 non-US markets can be represented in paused local Search infrastructure only. That does not mean live-spend-ready.

## Guardrails Preserved

- public/read-only storefront checks only
- no checkout payment
- no order
- no Shopify Admin changes
- no Ads, Merchant, or Pinterest writes
- fresh probing stopped after CH verification/CAPTCHA text detector fired
- writes limited to market-readiness lane

## Evidence Used

- 2026-05-08 paid-growth AI-army localization checkout readiness report and JSON
- 2026-05-08 GB/CA visual checkout UI readback
- 2026-05-08 AU isolated checkout-to-shipping readback
- 2026-05-08 PT checkout-to-shipping readback
- 2026-05-07 ES/IT/RO currency presentment browser readback
- fresh CH low-volume public product check in this lane

Raw fresh-check file: `raw/fresh_ch_dk_public_rate_checks.json`.
