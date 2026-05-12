# Paid Growth Measurement Safe Lanes Report

Generated: 2026-05-12

Anchor: `AGENT_CONTINUITY_ANCHOR: 2026-05-12-paid-growth-measurement-safe-lanes`

## Scope

The parent/orchestrator continued the canonical paid-growth prompt with no live-write approvals in this session. Work was limited to read-only account/UI probes, local artifact verification, local theme copy repair, evidence integration, and tracker/worklog updates.

No live spend, campaign enablement, upload/apply, budget/bid/status change, PMax, Standard Shopping change, product-scope/feed-label/product-group change, conversion-goal change, Merchant upload/source edit/sync, Pinterest account write, Shopify product-data write, payment/order/refund/cancel, credential/account/billing edit, CAPTCHA bypass, or destructive filesystem action occurred.

## Measurement

The non-US purchase-event currency/value gate remains open.

New safe recovery paths tried:

1. GA4 Data API metadata retry for property `330266838`.
   - Result: `403 ACCESS_TOKEN_SCOPE_INSUFFICIENT`.
   - Evidence: terminal readback; same blocker as prior packet.

2. GA4 UI direct report URL probe through existing logged-in Chrome CDP.
   - `events_purchase_with_event_dims`: stayed on `Analytics | Events: Event name`; purchase/currency/transaction not visible.
   - `monetization_purchases_purchase_event`: fell back to GA4 Home; purchases card visible, but no transaction/currency fields.
   - `transaction_id_report_direct`: reached `Analytics | Transactions: Transaction ID`; transaction report route is visible, but currency is not visible and no sanitized non-USD candidate amount matched.
   - Evidence: `ga4_readonly_probe/ga4_event_level_dimension_probe_summary.json` and screenshots.

3. GA4 UI sanitized network probe.
   - Result: found internal report/config references including `transaction-id-report`, but not usable order-level non-US currency/value/transaction evidence.
   - Stored only sanitized snippets, not raw response bodies.
   - Evidence: `ga4_readonly_probe/ga4_network_sanitized_probe_summary.json`.

Conclusion: aggregate GA4 purchase visibility is stronger, and the transaction report route exists, but the required non-US `purchase` event currency/value/order-level match is still not proven. The next non-destructive unblock is refreshed GA4 Data/Admin API scopes. If that cannot be provided and the owner wants closure, the next gate is exact approval for the controlled non-US test-purchase/refund/cancel procedure.

## Sidecar Integration

Google Ads paused Search:

- Verified current state remains `12 built / 3 absent / 2 parked`.
- Built/read back clean and paused: `GB`, `CA`, `AU`, `CH`, `DK`, `DE`, `NL`, `SE`, `ES`, `IT`, `PL`, `CZ`.
- Absent: `RO`, `PT`, `GR`.
- Parked: `FR`, `BE`.
- No Ads browser or account write occurred.

Native/localization:

- 2026-05-11 native rewrite packet is internally consistent: `450` keyword rows, `45` RSA rows, `133` negative-review rows, `15` locale-status rows, all `REVIEW_ONLY_NOT_UPLOAD`.
- Review-ready local-only slices remain `es-ES`, `it-IT`, `ro-RO`, `de-DE`, `nl-NL`, `fr-FR`, `sv-SE`, `pl-PL`, and `cs-CZ`.
- Gated slices remain `pt-PT`, `da-DK`, `fr-BE`, `nl-BE`, `el-GR`, and `CH-SPLIT`.
- Landing QA prevents live use: RO/DE/SE/CZ supplier-token blockers; DE/SE language issues; NL/FR/PL/CZ native landing review; DE/NL/FR/SE/PL/CZ final URL route rebuild.

Pinterest/Merchant/Beach:

- Pinterest clean US scope remains `342` rows with `4` exclusions; Event Quality still approval-gated.
- Merchant US/es issue remains isolated to source `10627981690`; live repair is approval-gated.
- Beach SEO/social live metadata remains approval-gated, while Ads risk is locally mitigated by held CSVs with `0` bad-handle hits.

## Local Theme QA Repair

Applied a narrow local-only PDP purchase-confidence copy repair:

- `snippets/pdp-purchase-confidence.liquid`
- `locales/en.default.json`
- `locales/ro.json`
- `locales/ro-RO.json`

What changed:

- Removed fallback/customer-facing wording that said standard shipping is "free."
- Romanian purchase-confidence labels now say `Livrare standard inclusă` and related Romanian shipping labels.
- Removed the stale unused `pc_fallback_copy` assignment, clearing the last Theme Check warning.

Readback:

- EN local Golden Daisy PDP: `0` hits for `Free standard shipping`, `Standard shipping is free`, or false 10% discount strings.
- RO local Golden Daisy PDP: `0` hits for `Free standard shipping`, `Standard shipping is free`, `Livrare standard gratuit`, or false 10% discount strings.

Remaining local/theme risks:

- Interactive matching-set JS still contains hard-coded English dynamic labels.
- Zero-review `Customer photos` still needs locale coverage.
- Supplier/source-token exposure in public localized product HTML remains a separate product/card data blocker; no Shopify product-data write was made.

## Verification

Passed:

- `ruby -rjson -e 'ARGV.each { |f| JSON.parse(File.read(f)); puts "OK #{f}" }' locales/en.default.json locales/ro.json locales/ro-RO.json`
- `rg -n "Free standard shipping|Standard shipping is free|Livrare standard gratuit" locales/ro.json locales/ro-RO.json locales/en.default.json snippets/pdp-purchase-confidence.liquid` returned no matches.
- `node --check assets/product-desktop-ux.js`
- `git diff --check`
- `shopify theme check --path . --fail-level error --output text` returned no offenses.
- Local readback for `/products/golden-daisy-mommy-and-me-set`.
- Local readback for `/ro/products/golden-daisy-mommy-and-me-set?country=RO`.

## Closest Safe Stopping Point

All safe local/read-only lanes are now either advanced or explicitly gated:

- Measurement is gated by GA4 API scopes or controlled test purchase approval.
- Remaining Google Ads paused builds are gated by upload-throttle/no-in-progress readback and exact branch decision for `RO` versus skip/park.
- Native/localized copy is review-only and landing-gated.
- Pinterest/Merchant/Beach blockers are approval-gated.
- Theme QA has one local copy fix applied and verified; remaining localization risks are tracked.
