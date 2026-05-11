# Native Rewrite Local-only + Measurement Continuation

Generated: 2026-05-11
Anchor: `AGENT_CONTINUITY_ANCHOR: 2026-05-11-paid-growth-native-rewrite-local-measurement-continuation`
Mode: `LOCAL_ONLY_REVIEW_PACKET_AND_READONLY_MEASUREMENT_CONTINUATION`

## Scope

This packet continues from `AGENT_CONTINUITY_ANCHOR: 2026-05-11-paid-growth-native-review-measurement-readonly-continuation`.

It does not redo the expert keyword packet. It creates a replacement review layer for the locales the May 11 triage marked `REWRITE_RECOMMENDED`:

- `es-ES`, `it-IT`, `ro-RO`
- `de-DE`, `nl-NL`, `fr-FR`, `sv-SE`
- `pl-PL`, `cs-CZ`

Source counts preserved from the expert packet:

- Source native keyword rows: `700`
- Source RSA rows: `70`
- Source negative-review rows: `205`

Replacement artifacts created:

- `google_ads_native_keyword_replacements_local_only.csv`: `450` rows
- `google_ads_native_rsa_replacements_local_only.csv`: `45` rows
- `google_ads_native_negative_replacements_local_only.csv`: `133` rows
- `native_rewrite_locale_status.csv`: `15` rows

Every Google Ads row remains `REVIEW_ONLY_NOT_UPLOAD`.

## Quality Changes

- Spanish rows replace non-native noun chains such as `looks familia coordinados` and `moda baño familiar`.
- Italian rows replace literal constructions such as `vestiti papà figlio`, `Idee per famiglia`, and broad `costume` negative intent.
- Romanian rows add missing prepositions/conjunctions such as `de baie pentru familie` and `tată și copil`.
- German rows normalize compounds/capitalization such as `Mama-Tochter-Kleider` and `Familienpyjamas`.
- Dutch rows replace English-influenced forms with `bijpassende` or compact Dutch compounds.
- French rows add connectors/hyphenation such as `robes mère-fille` and `looks de famille`.
- Swedish rows fix separated compounds such as `familjekläder`, `familjepyjamas`, and `badkläder för familjen`.
- Polish rows add case/connectors such as `sukienki mama-córka` and `rodzinne stroje kąpielowe`.
- Czech rows replace noun-chain phrases with `šaty pro mámu a dceru`, `rodinné plavky`, and related forms.

Negative keywords were narrowed where broad terms could block valid apparel intent. Marketplace/supplier terms remain exact-only review candidates.

## Still Gated

- `pt-PT`: no platform use until the Portugal `pt-PT` versus `pt-BR` storefront/dialect decision is made and read back.
- `da-DK`: remains blocked for true Danish-native rewrite.
- `fr-BE` and `nl-BE`: remain blocked until Belgium FR/NL split and route proof are resolved.
- `el-GR`: still requires Greek-native review and landing-language QA before platform use.
- `CH`: still has no native rows and needs a de-CH/fr-CH/it-CH/English split decision.

## Measurement Lane

The non-US purchase-event currency/value gate remains open. This packet does not claim it is solved.

Read-only evidence available from the prior packet:

- Shopify Admin sanitized non-USD order candidates: `7` rows across `DKK`, `GBP`, and `CHF`.
- GA4 UI access to property `330266838` was proven.
- GA4 Home showed `Purchases: 7` for May 4-10, but did not expose order-level currency/value.
- A fresh read-only GA4 Events pagination probe in this packet reached row `12` on the standard Events report for `Apr 13 - May 10, 2026`: `purchase`, `17` events, `16` users, `$1,103.34` total revenue. This confirms GA4 purchase events/revenue are visible in aggregate, but still not the required non-US order-level currency/value/transaction proof.
- Google Ads conversion action `Google Shopping App Purchase` remains healthy at aggregate/configuration level.
- GA4 Admin/Data API with the existing `gcloud` token is blocked by `403 ACCESS_TOKEN_SCOPE_INSUFFICIENT`.

The cleanest remaining read-only proof path is GA4 UI Explore/report export for property `330266838`, filtered to `eventName = purchase` for `2026-04-01` through `2026-05-10`, with transaction ID/currency/country/date/value dimensions if the UI exposes them. If the UI cannot expose the event-level fields, the exact next gate is read-only GA4 API scope refresh or controlled non-US test-purchase approval.

## Guardrails

No live spend, campaign enablement, account-object creation, upload/preview/apply, budget/bid/status change, PMax, Standard Shopping, product-scope/feed-label/product-group change, conversion-goal change, Merchant upload/source edit/sync, Shopify live product-data/theme write, Pinterest write, GA4/GTM write, checkout payment/order/refund/cancel, credential/account/billing edit, CAPTCHA bypass, destructive filesystem action, or unrelated dirty-worktree cleanup occurred.
