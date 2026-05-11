# Measurement Readback Recipe (Lane D)

Generated: 2026-05-10
Lane: `measurement-readback-recipe`
Parent packet: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-decision-pack-and-preflight/`
Anchor it answers to: `2026-05-10-paid-growth-orchestrator-deep-followup`
Author: Lane D `Measurement-Readback-Recipe` subagent (local file write only; no live writes, no browser, no network, no theme/Shopify/Ads/Merchant/Pinterest writes, no curl, no script execution)

## Scope and constraints

- This is a paste-ready, non-destructive readback recipe for the next browser-enabled operator. It is a "what to look for and where" guide only.
- It does NOT enable, pause, save, apply, upload, or push anything.
- It is an instruction document; the operator runs it, this lane does not.
- Every measurement claim below traces back to the prior gap audit at `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-deep-followup/lanes/measurement-conversion-gap/MEASUREMENT_CONVERSION_GAP_REPORT.md`. Theme `file:line` cites are reproduced from that audit and not re-derived here.

---

## 1. Top 3 measurement risks (carried forward from the prior gap audit)

The prior gap audit does not use the verbatim header "Top 3 measurement risks"; it presents the risks across sections 1, 3, and 4 of `MEASUREMENT_CONVERSION_GAP_REPORT.md`. They are reproduced here as the three risks this readback recipe must close before the first non-US live enable.

### Risk 1 - Currency presentment risk for non-US revenue attribution

Source: `MEASUREMENT_CONVERSION_GAP_REPORT.md` section 4 (lines 154-183).

Verbatim from source:

> "The theme has no `purchase` event ... Therefore the currency stamped on the `purchase` request to `googleadservices.com/pagead/conversion/853411529/` and to `G-N4EQNK0MMB` is determined by the Google & YouTube app, not by the theme dataLayer. The 2026-04-30 paid-value gate ... only proved this for a US/USD order. Non-US currency behavior of the official app's purchase request is `unknown without browser access`."
> (`MEASUREMENT_CONVERSION_GAP_REPORT.md:170-171`)

Plausible behaviors enumerated in source `:172-176`: (1) `currency=<presentment>` (best), (2) `currency=USD` with FX-converted value (opaque), (3) `currency=<shop primary>` (worst, materially under-reports non-USD ROAS).

Theme-side evidence (carried forward, do not re-verify in browser):
- `assets/analytics.js:126-139` `getCurrency()` reads `meta[property="og:price:currency"]` first, then `Shopify.currency.active`, then defaults `'USD'`.
- `assets/analytics.js:392` and `:462` and `:820` stamp presentment currency on view_item / add_to_cart / view_cart / begin_checkout / select_item / view_item_list / cart-snapshot items.
- `grep -n "purchase\b" assets/analytics.js` returns zero hits; no theme-side purchase event exists.

### Risk 2 - Cross-market conversion goal risk (`Account-default: Purchases`)

Source: `MEASUREMENT_CONVERSION_GAP_REPORT.md` section 1 (lines 16-60).

Verbatim from source:

> "The 9 paused non-US Search campaigns (`GB`, `CA`, `AU`, `CH`, `DK`, `DE`, `NL`, `SE`, `ES`) were created under the canonical TEST BUILD approval which forbade conversion-goal changes; they therefore inherit `Account-default: Purchases`, which currently resolves to the same single Primary `Google Shopping App Purchase` action."
> (`MEASUREMENT_CONVERSION_GAP_REPORT.md:28`)

> "Cross-attribution risk ... grows the moment any non-US Search campaign is enabled."
> (`MEASUREMENT_CONVERSION_GAP_REPORT.md:42`)

Inheritance chain (per source `:20-30`): campaign -> `Account-default` conversion goal at account level -> single Primary purchase action `Google Shopping App Purchase` -> Shopify-side Google & YouTube app firing `purchase` from any market on `/checkout/thank_you`.

### Risk 3 - Pinterest Event Quality `Fair` handoff

Source: `MEASUREMENT_CONVERSION_GAP_REPORT.md` section 3 (lines 101-150).

Verbatim from source:

> "After that fix, the `2026-05-08-pinterest-catalog-event-unblock/PINTEREST_CATALOG_EVENT_UNBLOCK_REPORT.md:58-66` readback still showed Event Quality `Fair` overall ... The three remaining action items reported by Pinterest ... are: 1. `product_id__ADD_PAYMENT_INFO` missing 2. `hashed_email__ADD_TO_CART` missing 3. `click_id_epik__CHECKOUT` missing"
> (`MEASUREMENT_CONVERSION_GAP_REPORT.md:114-118`)

> "the `_epik` cookie is generated from real Pinterest ad clicks, and the account currently has zero campaigns serving. So the `click_id_epik__CHECKOUT` gap will only close once real paid Pinterest traffic is flowing. It cannot be repaired theme-side or via more app config. It is a chicken-and-egg gap."
> (`MEASUREMENT_CONVERSION_GAP_REPORT.md:141`)

---

## 2. Pre-enable readback checklist (one item per risk)

Order of execution: Risk 1 -> Risk 2 -> Risk 3. All three are READ-ONLY. None of them touches a Save / Apply / Enable / Pause / Upload / Push button.

### Risk 1 readback - currency presentment via Google Tag Assistant + GA4 DebugView

Goal: confirm the live `currency` field value the Google & YouTube Shopify app actually puts on outbound `purchase` and pre-purchase ecommerce events for an EUR / SEK / CHF visitor. This is the gap the prior audit explicitly tagged `unknown without browser access` (`MEASUREMENT_CONVERSION_GAP_REPORT.md:171`, `:182`).

Operator steps (read-only, no order submission):

1. Open `https://tagassistant.google.com/` in the existing logged-in Google Ads / GA4 browser profile. Click `Add domain` and enter `https://www.dresslikemommy.com/`. Confirm Tag Assistant launches a new preview tab.
2. In the preview tab, confirm Tag Assistant detects: one `Google Tag (gtag.js)` sourced from the Google & YouTube Shopify app (NOT a duplicate from theme). This is the Tag Assistant equivalent of step 7 in `MEASUREMENT_CONVERSION_GAP_REPORT.md:81`.
3. In a SECOND tab, open `https://analytics.google.com/` -> property `G-N4EQNK0MMB` -> Configure -> DebugView. Confirm DebugView is showing the Tag Assistant preview session (it will appear as a debug device).
4. In the Tag Assistant preview tab, navigate to `https://www.dresslikemommy.com/?country=GB`. Use the storefront country/currency switcher (or append `?country=` query) to land on a GB-presentment page. Confirm storefront price displays in `GBP`. Repeat the run for `?country=DE` (EUR), `?country=SE` (SEK), `?country=CH` (CHF). One run per market.
5. For each market run, walk the funnel in the preview tab in this exact order, with NO payment data entry: `view_item` (open a paid-eligible product) -> `add_to_cart` (click Add to cart) -> `view_cart` (open cart drawer / cart page) -> `begin_checkout` (click Checkout, land on `/checkouts/...` first step). DO NOT fill name, address, email, or payment fields. DO NOT click `Pay now`. DO NOT submit a real order.
6. After each event in the preview-tab event log, click the event row and read the `currency` parameter:
   - GB run: each event must show `currency: GBP`.
   - DE run: each event must show `currency: EUR`.
   - SE run: each event must show `currency: SEK`.
   - CH run: each event must show `currency: CHF`.
7. Cross-confirm in GA4 DebugView (the second tab) that the same events appear with the same `currency` parameter values.
8. For the placeholder `/checkout/thank_you` `purchase` event behavior: this readback is REPLAY-ONLY. Use Tag Assistant's `Record` mode on a HISTORICAL non-US thank-you page if and only if one exists in the existing recorded sessions, OR wait for a real organic non-US order to land in DebugView naturally. Do NOT submit a synthetic real order with payment data to manufacture a `purchase` event. If no replay or organic data exists, mark this sub-step `OBSERVATION_PENDING` and proceed; the section 3 pass/fail rules below treat that as a non-blocker for pre-purchase events but a blocker for the purchase-currency confirmation specifically.
9. Capture screenshots of the Tag Assistant event-detail panel and the GA4 DebugView event card for each market and each event. File them under `dresslikemommy-growth-2026/02_AUDIT_PACKETS/<YYYY-MM-DD>-measurement-readback-pre-first-enable/raw/risk1_currency/<MARKET>_<EVENT>.png`. No write to GA4, no write to Tag Assistant settings.

EXPLICIT NON-ACTION (reproduced for emphasis): **Do NOT submit a real order; use a Tag Assistant preview/replay only.** Do not enter payment information, do not enter shipping address, do not click `Pay now`. The Tag Assistant preview session is sufficient for `view_item`, `add_to_cart`, `view_cart`, and `begin_checkout` `currency` capture. The `/checkout/thank_you` `purchase` event currency must come from replay of an existing recorded thank-you session OR from a future real organic non-US order observed in DebugView, NOT from a fabricated test order.

### Risk 2 readback - Account-default Purchases bucket scope and country segmentation

Goal: confirm `Google Shopping App Purchase` is the only Primary action that resolves under `Account-default: Purchases`, that no campaign-level override has been added to any non-US Search campaign, that no non-US live enable has occurred yet, and where to read country-segmented conversion data once enable happens.

Operator steps (read-only, no Save):

1. Open Google Ads -> Tools and settings -> Conversions -> Conversion actions. Click `Google Shopping App Purchase` to open its Settings panel. Read (do not edit):
   - Source: app/web
   - Category: `Purchase`
   - Counting: confirm matches current spec
   - Value: `Use different values. If there's no value, use 0.`
   - Click-through window
   - Attribution model
   - Include in `Conversions`: `Yes`
   - Geo / locale filter: confirm `none` (or equivalent "no restriction")
   These items are enumerated in `MEASUREMENT_CONVERSION_GAP_REPORT.md:47`.
2. Same Conversion-action panel, Activity tab. Filter Activity by Country. Read whether non-US purchases have already arrived in this action historically (per `MEASUREMENT_CONVERSION_GAP_REPORT.md:48`). Capture screenshot. No edits.
3. For EACH of the 9 paused non-US Search campaigns (`GB 23838895360`, `CA 23834423669`, `AU 23834424182`, `CH`, `DK`, `DE`, `NL`, `SE`, `ES 23829133584`), open campaign Settings -> Goals. Confirm `Account-default` resolves to a list that contains EXACTLY one Primary purchase action: `Google Shopping App Purchase`. Confirm there is NO campaign-level conversion-goal override (per `MEASUREMENT_CONVERSION_GAP_REPORT.md:49`, `FIRST_ENABLE_RUNBOOK_REPORT.md:71`). Capture per-campaign screenshot.
4. Confirm no non-US live enable has occurred yet by reading the Status column for all 9 campaigns above: each must read `Paused`. Cross-confirm against `ops/AGENT_COORDINATION.md` (look for any active `IN_PROGRESS` claim touching `non-US Search` or any of the 9 campaign IDs) and `ops/AGENT_WORKLOG.md` tail (look for any worklog row newer than 2026-05-10 with anchor pattern `*-non-us-first-enable-*-live`). Both must show no live enable. Capture the campaign-status screenshot.
5. Country-segmented conversion data location (the exact path to read AFTER any future enable, recorded here so the operator knows where to come back to): Google Ads -> Reports -> Predefined reports -> Conversions -> segment by `Conversion action` AND `Country/Territory`, last 30 days. This is the canonical view for confirming whether non-US conversions and US conversions are landing in the same `Google Shopping App Purchase` bucket and whether US Standard Shopping is leaking attribution to non-US countries (per `MEASUREMENT_CONVERSION_GAP_REPORT.md:50-51`).
6. Pre-enable baseline: in the same Reports -> Conversions view, segment by Country last 30 days for the conversion action `Google Shopping App Purchase`. Confirm whether non-US country rows have any non-zero conversions BEFORE any non-US Search is enabled. Record the baseline so post-enable deltas are interpretable (per `MEASUREMENT_CONVERSION_GAP_REPORT.md:50`).

### Risk 3 readback - Pinterest Event Quality `Fair` current state

Goal: read current Pinterest Events Manager state and document that this metric is gated on real ad-click volume and cannot be theme-fixed.

Operator steps (read-only):

1. Open Pinterest Ads Manager -> Conversions -> Events Manager. Select pixel ID `22577249` (per `MEASUREMENT_CONVERSION_GAP_REPORT.md:113`).
2. Read the Event Quality dashboard top-line score. Record current value (expected `Fair` per `MEASUREMENT_CONVERSION_GAP_REPORT.md:114` and `PINTEREST_CATALOG_EVENT_UNBLOCK_REPORT.md:58-66`).
3. Read the per-event detail panel for `add_to_cart`, `checkout`, and `add_payment_info`. Record:
   - `Pinterest Tag latest` timestamp.
   - `Conversions API latest` timestamp.
   - `Verified Merchant Program` status (expected `PASS`).
   - `Automatic Enhanced Match` status (expected `PASS`).
   - `Enhanced Match` status (expected `ERROR`).
   - `Deduplicated` flag for the most-recent shared `event_name` pair (per `MEASUREMENT_CONVERSION_GAP_REPORT.md:196`).
4. Read the three remaining action items panel. Confirm the same three gaps from `MEASUREMENT_CONVERSION_GAP_REPORT.md:114-118` are still listed:
   1. `product_id__ADD_PAYMENT_INFO` missing
   2. `hashed_email__ADD_TO_CART` missing
   3. `click_id_epik__CHECKOUT` missing
5. Capture full-page screenshot of the Event Quality dashboard and each per-event detail panel. File under `raw/risk3_pinterest_eq/`.

What counts as "improvement" vs "no change":
- "Improvement": top-line score moves from `Fair` to `Good` OR any of the three missing items disappears from the action-items panel OR `Enhanced Match` flips from `ERROR` to `PASS`.
- "No change": top-line still `Fair`, all three action items still listed, `Enhanced Match` still `ERROR`. Per the prior audit, no change is the EXPECTED state because `click_id_epik__CHECKOUT` is click-volume gated and the account currently has zero campaigns serving (`MEASUREMENT_CONVERSION_GAP_REPORT.md:141`).

Confirmation that this is click-volume gated and cannot be theme-fixed: `MEASUREMENT_CONVERSION_GAP_REPORT.md:141` states explicitly "It cannot be repaired theme-side or via more app config. It is a chicken-and-egg gap: the metric improves only after the operator runs a small approved paused-draft -> enabled campaign and gets real ad clicks." Adding `pintrk` to the theme is forbidden by `ops/AGENT_COORDINATION.md:75` (per `MEASUREMENT_CONVERSION_GAP_REPORT.md:150`).

---

## 3. Pass / fail definitions for each readback

### Risk 1 pass / fail (currency presentment)

- **PASS** = `currency` parameter in the Tag Assistant event-detail payload AND the GA4 DebugView event card matches the storefront-displayed market currency for AT LEAST ONE EUR-region test (e.g., DE shows `currency: EUR` on `view_item`, `add_to_cart`, `view_cart`, AND `begin_checkout`) AND at least one additional non-EUR market (SEK or CHF) shows the matching currency code on the same four events.
- **PARTIAL PASS** = pre-purchase events (view_item, add_to_cart, view_cart, begin_checkout) PASS for the markets above, but the `/checkout/thank_you` `purchase` event currency could not be confirmed because no replay or organic non-US thank-you data was available in the readback window. Mark as `OBSERVATION_PENDING_PURCHASE_CURRENCY` and treat as a soft-block: do not proceed with the first non-US enable until the next genuine non-US organic purchase has been observed in DebugView with `currency=<presentment>`. This matches `MEASUREMENT_CONVERSION_GAP_REPORT.md:217` `M5` "real-purchase currency proof".
- **FAIL** = any market run shows `currency: USD` on a non-US storefront, OR any market run shows the presentment value as a USD-converted number (per the worst-case scenario `MEASUREMENT_CONVERSION_GAP_REPORT.md:175`), OR `currency` is `(not set)` / missing.

### Risk 2 pass / fail (Account-default Purchases bucket)

- **PASS** = `Google Shopping App Purchase` is the ONLY Primary purchase action under `Account-default` AND no campaign-level conversion-goal override exists on any of the 9 non-US Search campaigns AND all 9 campaigns currently read `Paused` AND the country-segmented Conversions report path (Reports -> Predefined -> Conversions, segmented by Conversion action and Country/Territory) loads and renders the last-30-day baseline.
- **FAIL** = any duplicate Primary purchase action exists at account level (per `MEASUREMENT_CONVERSION_GAP_REPORT.md:49`: "If any duplicate purchase action is Primary at account level, a non-US enable will inflate counts"), OR any of the 9 non-US Search campaigns shows a campaign-level conversion-goal override, OR any of the 9 campaigns is no longer `Paused`, OR `Google Shopping App Purchase` shows a hidden geo restriction (per `MEASUREMENT_CONVERSION_GAP_REPORT.md:43` "No-conversion-counted risk").

### Risk 3 pass / fail (Pinterest Event Quality `Fair`)

- **INFORMATIONAL ONLY - DOES NOT BLOCK PAUSED INFRASTRUCTURE.** The Pinterest Event Quality readback is a state observation, not a gate. Per `MEASUREMENT_CONVERSION_GAP_REPORT.md:141`, the `click_id_epik__CHECKOUT` action item cannot close until real paid Pinterest traffic flows, and Pinterest is not the first non-US enable target. Record current Event Quality and the three action items as a baseline. Do not gate the Google non-US first enable on this readback. Do gate any future Pinterest spend enable on `MEASUREMENT_CONVERSION_GAP_REPORT.md:220` `M8` (`Deduplicated=Yes` for most-recent `add_to_cart` and `checkout` event pair).

---

## 4. What to do if any readback fails

If Risk 1 FAILs OR Risk 2 FAILs (Risk 3 is informational only):

1. **Park the relevant approval.** Do NOT request the owner to paste the verbatim approval phrase from `FIRST_ENABLE_RUNBOOK_REPORT.md:81-83`. Do NOT proceed with the GB first non-US enable described in that runbook section 3.
2. **Do not proceed to the first non-US enable.** Specifically: do NOT enable campaign `23838895360`, do NOT enable ad group `Mommy & Me Dresses - Exact only`, do NOT toggle any of the 9 non-US Search campaigns from `Paused`.
3. **Log the result in the problem tracker.** Append a new row to `ops/PROBLEM_TRACKER.md` with id pattern `PROB-<YYYY-MM-DD>-MEASUREMENT-READBACK-<RISK1_CURRENCY|RISK2_CONV_GOAL>-FAIL`, severity `P1` if Risk 1 FAIL with `currency=USD` on non-US (materially under-reports ROAS), `P1` if Risk 2 FAIL with duplicate Primary action (inflates conversion counts on enable), `P2` for the partial-pass `OBSERVATION_PENDING_PURCHASE_CURRENCY` case. Cite this readback file path and the Risk-N section. Reference back to `MEASUREMENT_CONVERSION_GAP_REPORT.md:209-225` `MEASUREMENT_GATE_FOR_NON_US_SEARCH_ENABLE` items M1-M11 and which item failed.
4. **Escalate to owner.** Send the owner a chat message stating which Risk failed, which campaign IDs are now blocked from enable, the evidence file path under `raw/`, the problem-tracker row ID, and the question of which remediation path to authorize next (a remediation may itself require a separate owner approval phrase, per `MEASUREMENT_CONVERSION_GAP_REPORT.md:55-57`).
5. **Re-run this readback recipe** only after the underlying remediation is in place. Do not re-run as a way to "try again" without a remediation.

---

## 5. Explicit list of actions NOT to take during this readback

The operator MUST NOT do any of the following while executing this recipe. This list is exhaustive for the scope of this recipe.

1. **No Save.** Do not click any Save button in Google Ads, GA4, Tag Assistant, Pinterest Events Manager, Shopify Admin, or any other UI surface visited during this readback.
2. **No Apply.** Do not click any Apply, Apply changes, or Apply recommendation button.
3. **No Enable.** Do not toggle any campaign, ad group, ad, conversion action, audience, or extension from `Paused` to `Enabled`. Specifically do NOT enable campaign `23838895360`, do NOT enable ad group `Mommy & Me Dresses - Exact only`, and do NOT enable any of the 9 non-US Search campaigns (`GB`, `CA`, `AU`, `CH`, `DK`, `DE`, `NL`, `SE`, `ES`).
4. **No Pause.** Do not toggle any currently-Enabled unit (e.g., `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY` `23802638621`, `DLM_US_SEARCH_BRAND_PROTECT_PAUSED_20260429`) from `Enabled` to `Paused`. This recipe is observational; pausing live US infrastructure is out of scope.
5. **No Upload.** Do not upload any CSV, audience list, customer-match file, conversion-import file, feed file, or asset to Google Ads, Merchant Center, GA4, Pinterest, or Shopify. Specifically do NOT upload `00_intl_search_paused_draft_web_bulk_vacation_family_hold.csv` or any of the 9 country split CSVs.
6. **No theme push.** Do not edit `/Users/fsuels/Projects/dresslikemommy/assets/analytics.js`, `layout/theme.liquid`, any snippet, any section, any template, or any other theme file. Do not run `shopify theme push`. Do not add `pintrk`, `epik`, `event_id`, or any custom Pinterest tag/CAPI code to the theme (forbidden by `ops/AGENT_COORDINATION.md:75` per `MEASUREMENT_CONVERSION_GAP_REPORT.md:150`).
7. **No order submission.** Do not click `Pay now`, `Place order`, `Complete order`, `Continue to payment`, or any equivalent terminal-step button on `/checkouts/...`. Do not submit any synthetic real order with real or test payment credentials. The Risk 1 readback uses Tag Assistant preview mode and DebugView observation only; do not manufacture a `purchase` event by paying.
8. **No payment data entry.** Do not type a card number, do not paste a card number, do not select a saved card, do not enter PayPal/Apple Pay/Shop Pay credentials, do not enter a billing address. Even in test mode. Even on a staging domain. The Risk 1 readback never requires payment fields to be touched.
9. **No CAPTCHA bypass.** If the storefront, Google Ads, GA4, Pinterest, or Shopify presents a CAPTCHA / reCAPTCHA / hCaptcha / Cloudflare Turnstile challenge during this readback, do NOT attempt to bypass it programmatically, do NOT use any browser-automation tool to solve it, do NOT use any third-party CAPTCHA-solving service. Solve it manually with the operator's own input or abort the readback and route to parent.
10. **No conversion-action edit.** Do not click `Edit settings` on `Google Shopping App Purchase`. Do not change Category, Value, Counting, Click-through window, Attribution, Include in Conversions, or Geo. Settings panels are READ-ONLY in this recipe.
11. **No conversion-goal change.** Do not add, remove, or reorder any Primary or Secondary purchase action at account level. Do not add a campaign-level conversion-goal override on any campaign. Doing so requires the separate owner approval phrase quoted in `MEASUREMENT_CONVERSION_GAP_REPORT.md:57`.
12. **No GA4 property-setting change.** Do not edit `Reporting identity`, `Currency`, data-stream config, measurement ID, or any Admin-side setting. Reading the values is fine; writing them is not.
13. **No Tag Assistant publish.** Do not click `Publish` or `Submit` in Tag Assistant or Google Tag Manager. The session is preview-only.
14. **No Pinterest Events Manager edit.** Do not click `Edit pixel`, do not change Enhanced Match settings, do not toggle `Always on` / `share all events`. Read the dashboard only.
15. **No Shopify Admin write.** Do not edit Customer Events, Web Pixels Manager, the Google & YouTube app config, the Pinterest app config, theme settings, product data, or any other Shopify Admin surface.
16. **No Merchant Center write.** Do not approve, deny, or edit any product, feed, attribute, or policy notice in Merchant Center.
17. **No script execution.** Do not run any `curl`, `bash`, `node`, `python`, `gcloud`, `gam`, RPC helper, or other script that writes to Google Ads, GA4, Merchant Center, Pinterest, or Shopify. Read-only RPC reads (such as the campaign-readback helper used by prior non-US lanes per `FIRST_ENABLE_RUNBOOK_REPORT.md:123`) are out of scope for THIS recipe; this recipe is a UI/dashboard readback only. RPC reads belong to the just-in-time pre-enable RPC step in `FIRST_ENABLE_RUNBOOK_REPORT.md:60-71`, not here.
18. **No new file writes by this lane.** The only file written by this lane is this recipe itself. The operator's evidence captures (screenshots, JSON, problem-tracker rows) are written by the operator at execution time, not by this lane.

---

## 6. Guardrails honored by this recipe

- No Google Ads, Merchant Center, Pinterest, GA4, Shopify Admin, or theme writes are made or proposed.
- No conversion goal, conversion action, attribution, pixel, or audience change is made or proposed.
- No campaign enable, budget, bid, or status change is made or proposed.
- No order submission, no payment data entry, no CAPTCHA bypass.
- The only file written by this lane is this recipe.
- Every measurement claim cites `MEASUREMENT_CONVERSION_GAP_REPORT.md:<line>` so the operator can trace it back to evidence rather than inference.
- Items requiring browser access are explicitly framed as "operator steps", not as actions taken by this lane.

---

## 7. Files touched

WRITTEN by this subagent (lane report only):
- `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-decision-pack-and-preflight/lanes/measurement-readback-recipe/MEASUREMENT_READBACK_RECIPE.md`

READ by this subagent (no modifications):
- `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-deep-followup/lanes/measurement-conversion-gap/MEASUREMENT_CONVERSION_GAP_REPORT.md`
- `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-deep-followup/lanes/first-enable-runbook/FIRST_ENABLE_RUNBOOK_REPORT.md`
- `/Users/fsuels/Projects/dresslikemommy/assets/analytics.js` (lines 126-139 only, to confirm the `getCurrency()` cite reproduced from the gap audit)
