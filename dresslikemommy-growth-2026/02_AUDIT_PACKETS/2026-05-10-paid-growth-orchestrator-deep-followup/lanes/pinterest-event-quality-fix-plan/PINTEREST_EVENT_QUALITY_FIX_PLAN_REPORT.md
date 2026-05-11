# Pinterest Event Quality Fix Plan Report

Lane: C / Pinterest-Event-Quality-Fix-Plan
AGENT_CONTINUITY_ANCHOR: 2026-05-10-paid-growth-orchestrator-deep-followup
Subagent: Pinterest-Event-Quality-Fix-Plan
Generated: 2026-05-10
Active blocker referenced: `PROB-2026-05-08-PINTEREST-EVENT-QUALITY` (`OWNER_APPROVAL_REQUIRED`)

This report is purely local and read-only. No Pinterest, Shopify, theme, or browser writes were made. All claims about theme/repo state are grounded in `Grep`/`Read` evidence with absolute paths and line numbers. Pinterest dashboard URL patterns and gap details cite the prior 2026-05-08 readback packet.

---

## 1. Map the Fair to Good gap

The `Fair` overall WEB Event Quality reading on advertiser `549756244483` is driven by four named gaps. Each is mapped to its actual fix surface below. Source for the gap list: `event_quality_api_probe.json` (`topActionItems` and `qualityComponents`) and the `event_quality.txt` UI capture, both at `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-pinterest-catalog-event-unblock/lanes/pinterest/raw/`.

### 1.1 `product_id__ADD_PAYMENT_INFO` (rank 1 top action item)

Probe values (`event_quality_api_probe.json` lines 653 to 676):

- `product_id_catalog_match` value `0.0`, status `FAIL`.
- `product_id_coverage` value `0.0`, status `FAIL`.
- `actionItemId: product_id__ADD_PAYMENT_INFO`, `isTopActionItem: true`.

Where the fix lives:

- **Theme (none).** A repo-wide search of `snippets/`, `assets/`, `layout/`, `sections/`, `templates/`, and `config/` for `pintrk`, `pinterest_tag`, `tag_id`, and `epik` returned **no theme-side Pinterest tag firing code** (see Section 4 evidence). The Add Payment Info event is fired by Shopify Checkout and forwarded by the official Shopify Pinterest app; no theme snippet currently emits it.
- **Shopify Pinterest official app (primary surface).** Add Payment Info is an event Shopify Checkout reports; the official Pinterest app maps cart line `product_id` (variant or product) into the event payload. The fact that other events (`product_id__ADD_TO_CART` value `51.6%`, `product_id__INITIATE_CHECKOUT` value `73.6%`, `product_id__CHECKOUT` value `86.7%`, all `GOOD`) carry `product_id` correctly indicates the catalog/Shopify product side is fine. The gap is specifically the AddPaymentInfo step omitting the cart-line product_id in the payload the official app sends. This is **Shopify-app-managed CAPI behavior** and not directly editable from theme code.
- **CAPI server side (Shopify-managed).** The Conversions API delivery for AddPaymentInfo is performed by the Shopify Pinterest app; it cannot be edited as customer code without standing up a separate custom CAPI integration, which is explicitly ruled out by the prior packet (`ops/PROBLEM_TRACKER.md` line 815: "Adding duplicate theme-level Pinterest tag or custom CAPI is ruled out without exact approval").
- **Pinterest dashboard.** Dashboard cannot inject `product_id` into a missing event; it can only read what it received. Dashboard role here is verification, not repair.

Net: this gap is **Shopify Pinterest official app surface**. Fix path is to confirm the official app is on the latest version, that the catalog is connected to the same advertiser, and that "Share all events" remains enabled. If a follow-up app version still does not populate `product_id` on AddPaymentInfo, the only repair becomes a separately approved Shopify Customer Events / custom CAPI implementation.

### 1.2 `hashed_email__ADD_TO_CART` (rank 2 top action item)

Probe values (`event_quality_api_probe.json` lines 793 to 810):

- `hashed_email_match_rate` value `100.0`, status `PASS`.
- `hashed_email_coverage` value `4.225...`, status `FAIL`.
- `actionItemId: hashed_email__ADD_TO_CART`, `isTopActionItem: true`.

Where the fix lives:

- **Theme (none).** No theme-side AddToCart Pinterest event is emitted (Section 4). No place in `snippets/`, `assets/`, `layout/`, `sections/`, `templates/` adds an `em` (hashed email) parameter to a Pinterest call.
- **Shopify Pinterest official app.** AddToCart in this account is fired before login/email capture for most sessions, which mechanically caps coverage near the email-capture rate (Klaviyo / newsletter / customer-account capture). Match rate is already `100%`, meaning when an email is present it hashes correctly; the deficit is **coverage**, not match quality.
- **Storefront / customer behavior.** Coverage rises when more sessions have a known email by AddToCart time. Surfaces that influence this: account-aware login for repeat shoppers, newsletter prompt before AddToCart, and Klaviyo / Shopify customer-event identity stitching. Each of those is independent owner approval territory.
- **Pinterest dashboard.** Read-only verification.

Net: the gap is **Shopify Pinterest official app + identity-capture surface**, not theme code. Dashboard cannot inject hashed email. Theme cannot inject hashed email into a Pinterest event the theme is not currently emitting. The fix is upstream: more sessions with known email at AddToCart, or a separately approved Customer Events handler that reads `customer.email` (when present) and forwards to Pinterest CAPI.

### 1.3 `click_id_epik__CHECKOUT` (rank 3 top action item)

Probe values (`event_quality_api_probe.json` lines 495 to 513):

- `click_id_epik_match_rate` value `0.0`, status `FAIL`.
- `click_id_epik_coverage` value `0.0`, status `FAIL`.
- `actionItemId: click_id_epik__CHECKOUT`, `isTopActionItem: true`.
- Same `0.0` `FAIL` shape on every other event under `click_id_epik` (`PAGE_VISIT`, `ADD_TO_CART`, `ADD_PAYMENT_INFO`, `SEARCH`, `INITIATE_CHECKOUT`, `VIEW_CATEGORY`, `CHECKOUT`).

Where the fix lives:

- **Pinterest click ID `_epik`.** This is the Pinterest first-party cookie set on the storefront when a user lands from a Pinterest pin click that includes the `epik` parameter. `click_id_epik_coverage = 0.0` across **every event**, not just CHECKOUT, means the storefront is not currently receiving `epik`-tagged Pinterest clicks at all, which is consistent with the campaign baseline of `0 campaigns / 0 clicks / $0 spend` (`raw/campaign_spend_baseline.txt`).
- **Theme (no current dependency).** No theme code reads or persists `_epik`. The official Pinterest app is responsible for setting and reading the `_epik` cookie when present.
- **Shopify Pinterest official app.** Already on `Always on`. Nothing to flip.
- **Pinterest dashboard.** Read-only verification.

Net: this gap **resolves itself only after live Pinterest spend produces real `_epik`-tagged clicks**. It cannot be fixed pre-spend by any theme, app, or dashboard action. This is a **circular constraint**: lifting `click_id_epik` to `Good` requires live Pinterest traffic, but live Pinterest spend is gated on Event Quality being `Good`. The escape is to accept this specific item is volume-gated and not blocking, and to grade overall Event Quality on the other parameters once the Product ID and hashed Email coverage gaps are addressed.

### 1.4 `Enhanced Match` `ERROR` (deeper underlying issue)

Probe values (`event_quality_api_probe.json` lines 103 to 252):

- `Enhanced Match` group `status: ERROR`, `updatedDate: 2026-05-06`.
- Items: `checkout_has_em` `PASS`, `add_to_cart_has_em` `PASS`, `page_visit_has_em` `PASS`, `init_has_em` `PASS`. `signup_has_em` `MISSING` (level `ERROR`), `lead_has_em` `MISSING` (level `ERROR`), `watch_video_has_em` `MISSING` (level `ERROR`), `app_install_has_em` `MISSING` (level `ERROR`), `search_has_em` `FAIL`, `view_category_has_em` `FAIL`.

Where the fix lives:

- **Pinterest dashboard interpretation, not theme.** The `MISSING` items (signup, lead, watch_video, app_install) are events the store does not need to fire (not a video / lead / app install merchant), so `MISSING` is structurally permanent and not a theme bug.
- **Shopify Pinterest official app.** The `FAIL` items (`search_has_em`, `view_category_has_em`) mean Search and ViewCategory events are reaching Pinterest **without identity (em / external_id) attached** in enough sessions. Other events (`page_visit`, `add_to_cart`, `checkout`, `init`) are `PASS`. Same official-app constraint: Search and ViewCategory Pinterest events come from the official app's Customer Event subscription; the theme does not currently fire them.
- **Automatic Enhanced Match status `PASS`** (`event_quality_api_probe.json` lines 261 to 287): `aem_enabled = 100%`. The base AEM mechanism is on. The `ERROR` is an aggregation of the `MISSING` and `FAIL` per-event sub-checks above.

Net: same surface as 1.1 / 1.2. Dashboard can verify; app can be reconfirmed; theme cannot patch without an approved custom Customer Events implementation.

### 1.5 Summary table

| Gap | Theme fix? | Shopify Pinterest app fix? | Pinterest dashboard fix? | Custom CAPI fix? | Volume-gated? |
|---|---|---|---|---|---|
| `product_id__ADD_PAYMENT_INFO` | No (no theme tag) | Reconfirm app + catalog binding | Verify only | Possible if app remains broken (separate approval) | No |
| `hashed_email__ADD_TO_CART` | No (no theme tag) | Reconfirm app + identity capture | Verify only | Possible if app remains broken (separate approval) | Partial (rises with logged-in volume) |
| `click_id_epik__CHECKOUT` | No (no theme tag) | No app action helps | Verify only | No | Yes (requires live Pinterest clicks) |
| `Enhanced Match` `ERROR` | No (no theme tag) | Reconfirm app | Verify only | Possible if app remains broken (separate approval) | Partial |

---

## 2. Concrete action sequence

This is the ordered sequence a browser-enabled operator should run **after** owner approval of Phrase A in Section 5. Each step lists the dashboard URL pattern, the action, what NOT to click, and the readback that proves the step worked. URL patterns are sourced from prior packet captures cited inline.

### Step 0 (Pre-flight)

URL: `https://ads.pinterest.com/advertiser/549756244483/` (advertiser `549756244483` cited at `dresslikemommy-growth-2026/01_EXPORTS_RAW/PINTEREST/2026-04-28_authenticated_browser_capture/conversion_health_network.json:3`).

- Click: nothing yet. Confirm logged-in identity matches account `Dress Like Mommy | Matching Family Outfits` / domain `dresslikemommy.com` (per `raw/event_quality.txt` lines 2 to 4).
- Do NOT click any campaign/budget/bid/status control. Do NOT enter the Ads Manager create flow.
- Readback: top-level chrome shows the correct advertiser ID `549756244483`.

### Step 1 (Confirm Event Quality baseline before any change)

URL: `https://ads.pinterest.com/advertiser/549756244483/conversions/events-overview/`.
URL: `https://ads.pinterest.com/advertiser/549756244483/conversions/health/` (cited at `dresslikemommy-growth-2026/01_EXPORTS_RAW/PINTEREST/2026-04-28_authenticated_browser_capture/conversion_health_network.json:3`).

- Click: the Event quality tab.
- Do NOT click "Set up API", "Tag manager", or "Conversion upload" (those are documented in `raw/event_quality.txt` lines 8 to 18 and would risk a duplicate tag/CAPI).
- Readback: Event quality score reads `Fair`. Top 3 action items in this exact order: `Product ID in Add Payment Info`, `Email in Add to Cart`, `Click ID in Checkout` (matches `raw/event_quality.txt` lines 32 to 59). Date stamp matches `Updated 5/6/2026` or newer.

### Step 2 (Verify Pinterest tag + CAPI freshness)

API readback (read-only via dashboard XHR) of `https://api.pinterest.com/ads/v4/advertisers/549756244483/conversions/latest`.

- Click: nothing. The dashboard fetches this on the Event quality page.
- Do NOT use "Set up API" / "Conversion upload" / "Upload file" / "Upload history" tabs.
- Readback: `data.TAG` and `data.CONVERSIONS_API` timestamps both fresh (most recent visit + a few seconds). Baseline reference: TAG `1778219456502890000` and CAPI `1778219473760287700` (`event_quality_api_probe.json` lines 64 to 67).

### Step 3 (Confirm Verified Merchant Program and Automatic Enhanced Match still pass)

URL: `https://ads.pinterest.com/advertiser/549756244483/conversions/health?groupKey=Verified+Merchant+Program`.
URL: `https://ads.pinterest.com/advertiser/549756244483/conversions/health?groupKey=Automatic+Enhanced+Match`.

- Click: each group key link from the Event Quality page summary.
- Do NOT click any "Edit" / "Reset" / "Reconfigure" control.
- Readback: Verified Merchant Program `status: PASS` (probe lines 304 to 306). Automatic Enhanced Match `status: PASS`, `aem_enabled` value `100.0` (probe lines 267 to 285).

### Step 4 (Open Enhanced Match group to confirm which events are MISSING vs FAIL)

URL: `https://ads.pinterest.com/advertiser/549756244483/conversions/health?groupKey=Enhanced+Match`.

- Click: the group row.
- Do NOT click "Improve" / "Fix issues" buttons that would launch the Pinterest app reinstall or tag manager flow yet.
- Readback: per-event rows match probe data: `checkout_has_em`, `add_to_cart_has_em`, `page_visit_has_em`, `init_has_em` all `PASS`. `search_has_em` and `view_category_has_em` `FAIL`. `signup_has_em`, `lead_has_em`, `watch_video_has_em`, `app_install_has_em` all `MISSING` (`event_quality_api_probe.json` lines 112 to 248). The `MISSING` set being limited to event types this merchant does not actually fire (signup/lead/video/app) is the expected shape; that confirms no broken theme tag is firing them empty.

### Step 5 (Reconfirm the official Shopify Pinterest app config)

URL: `https://admin.shopify.com/store/dresslikemommy-com/apps` (admin pattern matches `dresslikemommy-growth-2026/04_IMPLEMENTATION_PLANS/2026-04-29-vetted-shopify-admin-fix-orchestration.md:193`).

- Click: open the Pinterest app entry. Inside the app, locate the data sharing toggle (referenced as `Always on` / share all events on 2026-05-06; tracker line 801).
- Do NOT click any "Disconnect", "Reinstall", "Reset feed", "Refresh source", or "Manage catalog" control.
- Do NOT change advertiser binding, country setting, or feed selection.
- Readback: the data sharing setting still reads `Always on` (or the platform's current equivalent of "Share all events"). The bound advertiser ID matches `549756244483`. The bound merchant remains the existing Verified Merchant.

### Step 6 (Reconfirm Customer Events does NOT have a competing Pinterest pixel)

URL: `https://admin.shopify.com/store/dresslikemommy-com/settings/customer_events` (cited at `dresslikemommy-growth-2026/04_IMPLEMENTATION_PLANS/2026-04-29-vetted-shopify-admin-fix-orchestration.md:193`).

- Click: only the "Web pixels" / list view.
- Do NOT click "Add custom pixel" or "Add app pixel".
- Do NOT edit any existing pixel.
- Readback: only the Pinterest official app pixel is listed in the Pinterest row. No second Pinterest entry. No custom pixel containing the strings `pintrk` or `pinterest`.

### Step 7 (Final Event Quality re-read after a 24 to 72 hour observation window)

URL: `https://ads.pinterest.com/advertiser/549756244483/conversions/events-overview/` Event quality tab again.

- Click: refresh.
- Do NOT enable any campaign or modify any budget/bid/status during the window.
- Readback: the three top action items either drop in count or change rank. The criterion for "good enough to enable" is in Section 6.

### Steps NOT to take in this lane

- Do NOT install a second Pinterest tag in the theme. (Tracker line 815 explicitly forbids it pre-approval.)
- Do NOT add or edit a Shopify Customer Event web pixel for Pinterest. (Phrase B in Section 5 is required first.)
- Do NOT modify catalog data sources, feed mappings, product groups, audiences, or any campaign object.
- Do NOT modify Shopify Admin product data (titles, descriptions, prices, age_group, sizes).
- Do NOT touch Markets, shipping, or checkout settings.

---

## 3. Risk: dupe events and dedupe mechanism

Tag and CAPI both fire within seconds (`event_quality_api_probe.json` lines 64 to 67: TAG `1778219456502890000`, CAPI `1778219473760287700`, ~17 ms apart in nanoseconds). Without dedupe, every event would be counted twice.

Dedupe mechanism the Pinterest official app uses: **`event_id` (a.k.a. `external_event_id`)**. Both the browser-side Pinterest Tag call and the server-side CAPI call attach the same `event_id` per logical event. Pinterest's pipeline then collapses duplicates by `(event_name, event_id)` within its merge window.

Evidence the mechanism is currently active and healthy:

- `event_quality.txt` lines 118 to 131 ("Duplicate events" section): "Event parameters in good health" lists `Event ID` for `Page Visit` and `View Category`.
- `event_quality_api_probe.json` lines 1490 to 1546 (`external_event_id` block):
  - `PAGE_VISIT`: `external_event_id_overlap` value `94.50971...`, `external_event_id_capi_coverage` `100.0`, `external_event_id_tag_coverage` `100.0`, status `GOOD`.
  - `VIEW_CATEGORY`: `external_event_id_overlap` value `97.0873...`, both coverages `100.0`, status `GOOD`.

Theme-side dedupe ID visibility:

- Theme repo grep for `pintrk`, `pinterest_tag`, `tag_id`, `epik`, `external_event_id`, `event_id` against Pinterest contexts in `snippets/`, `assets/`, `layout/`, `sections/`, `templates/`, `config/` returned **no matches** that fire a Pinterest event (Section 4). The dedupe ID is therefore not minted by the theme; it is generated and threaded by the official Shopify Pinterest app between its browser tag injection (via `content_for_header`) and its server-side CAPI emission.

Risk flag for any future paused-draft enable:

- Because the `event_id` lives entirely inside the Shopify-managed Pinterest app, the theme cannot independently observe or test it. If a future approved theme writer adds a second Pinterest tag (custom pixel or theme snippet) **without using the same `event_id`**, every event on covered surfaces would be emitted three times (theme tag + official tag + official CAPI) with only the official tag/CAPI pair deduping. That would visibly inflate AddToCart / Checkout counts in Pinterest.
- Mitigation: any approved theme-side Pinterest work must subscribe to (and reuse) the `event_id` already used by the official app, OR the official app's tag must be disabled at the same time the theme tag is enabled (an explicit Phrase B Section 5 scope). Adding a second tag without one of those moves is a known dupe hazard and is currently ruled out by tracker line 815.
- Today, only `PAGE_VISIT` and `VIEW_CATEGORY` show in the `external_event_id` health view. AddToCart, AddPaymentInfo, Checkout, InitiateCheckout, Search are not yet listed in the public dedupe health table (probe lines 1490 to 1546). That is **not** evidence those events are not deduped; it is just a reporting view limitation. But it does mean a future theme writer cannot use the dashboard alone to confirm dedupe on AddToCart / Checkout if they add a second tag; they would have to inspect the network trace.

---

## 4. Theme-code readback only

Catalog of current theme state for any future approved theme writer. No edits proposed.

### 4.1 Files containing the literal token `pinterest` / `pintrk` / `pinterest-tag`

Bash command (via `Grep` tool, regex `pinterest|pintrk|pinterest-tag`, case-insensitive, restricted to `snippets/`, `assets/`, `layout/`, `sections/`, `templates/`, `config/`):

| File | Line | Content category |
|---|---|---|
| `/Users/fsuels/Projects/dresslikemommy/sections/announcement-bar.liquid` | 6 | `settings.social_pinterest_link` social-link gate (NOT a tag) |
| `/Users/fsuels/Projects/dresslikemommy/config/settings_data.json` | 118 | `social_pinterest_link` setting value |
| `/Users/fsuels/Projects/dresslikemommy/config/settings_data.json` | 383 | `social_pinterest_link` setting value (preset) |
| `/Users/fsuels/Projects/dresslikemommy/config/settings_schema.json` | 1350 | `social_pinterest_link` schema id |
| `/Users/fsuels/Projects/dresslikemommy/config/settings_schema.json` | 1351 | `social_pinterest_link` label binding |
| `/Users/fsuels/Projects/dresslikemommy/config/settings_schema.json` | 1352 | `social_pinterest_link` placeholder binding |
| `/Users/fsuels/Projects/dresslikemommy/sections/footer.liquid` | 14 | `settings.social_pinterest_link` social-link gate |
| `/Users/fsuels/Projects/dresslikemommy/sections/header.liquid` | 247 | `settings.social_pinterest_link` social-link gate |
| `/Users/fsuels/Projects/dresslikemommy/sections/main-password-footer.liquid` | 21, 23, 24, 25 | Pinterest social-link rendering on password page (anchor tag, icon, a11y label) |
| `/Users/fsuels/Projects/dresslikemommy/snippets/social-icons.liquid` | 53, 55, 56, 57 | Pinterest social-link rendering (anchor, icon, a11y label) |
| `/Users/fsuels/Projects/dresslikemommy/snippets/header-drawer.liquid` | 285, 287, 288, 289 | Pinterest social-link rendering inside mobile drawer |
| `/Users/fsuels/Projects/dresslikemommy/snippets/product-schema-extra.liquid` | 61 | `https://www.pinterest.com/dresslikemommy` literal in JSON-LD `sameAs` array |
| `/Users/fsuels/Projects/dresslikemommy/snippets/icon-pinterest.liquid` | 1 | Inline SVG icon definition |
| `/Users/fsuels/Projects/dresslikemommy/snippets/jsonld-seo.liquid` | 13 | `social_pinterest_link` enumerated in social-handle list for JSON-LD |
| `/Users/fsuels/Projects/dresslikemommy/snippets/jsonld-seo.liquid` | 32 | `https://www.pinterest.com/dresslikemommy` literal in JSON-LD `sameAs` array |

Every match is a social-link, settings-binding, icon, or JSON-LD `sameAs` reference. **None fires a Pinterest event.**

### 4.2 Files containing `pintrk` / `pinterest_tag` / `tag_id` / `epik`

Bash command (via `Grep` tool, regex `pintrk|pinterest_tag|tag_id|epik`, case-insensitive, restricted to `snippets/`, `assets/`, `layout/`, `sections/`, `templates/`, `config/`):

- Result: `No matches found`.

There is **no theme-side Pinterest tag, no theme-side `pintrk` call, no theme-side tag ID, and no theme-side `_epik` cookie reader**.

### 4.3 Files containing `AddToCart` / `AddPaymentInfo` / `InitiateCheckout` / `trackCustomEvent` / `track(`

Bash command (via `Grep` tool, regex `AddToCart|AddPaymentInfo|InitiateCheckout|trackCustomEvent|track\(`, restricted to `snippets/`, `assets/`, `layout/`, `sections/`, `templates/`):

- Only matches: `/Users/fsuels/Projects/dresslikemommy/assets/analytics.js` lines 973, 987, 999, 1516. All four are GA4 dataLayer pushes (`pushAddToCartEvent`, `initProductAddToCartTracking`, `pushEcommerceEvent('add_to_cart', ...)`). No Pinterest event call.

### 4.4 Pinterest tag injection path (today)

The Pinterest base tag and CAPI are injected via the official Shopify Pinterest app, threaded through Shopify's Customer Events / web pixels stack. The theme exposes them only via the standard `{{ content_for_header }}` slot:

- `/Users/fsuels/Projects/dresslikemommy/layout/theme.liquid` line 425: `{{ content_for_header }}` (canonical location).
- `/Users/fsuels/Projects/dresslikemommy/layout/password.liquid` line 24: `{{ content_for_header }}` (storefront password mode).
- `/Users/fsuels/Projects/dresslikemommy/templates/gift_card.liquid` line 28: `{{ content_for_header }}` (gift card template).
- `/Users/fsuels/Projects/dresslikemommy/snippets/cjpod.liquid` line 2: `{% capture header_content %}{{content_for_header}}{% endcapture %}` (read-only capture for a `cjpodflag` feature gate; does not modify content).

Net theme state for Pinterest events: passthrough only. A future approved theme writer who needs to add a second Pinterest event would have a clean slate (no existing `pintrk` to collide with), but must coordinate with the Shopify Pinterest app's existing tag to avoid the dedupe hazard documented in Section 3.

---

## 5. Owner-approval phrasing

### Phrase A: Event Quality dashboard repair (no theme/CAPI writes)

```
APPROVE READ-ONLY PINTEREST EVENT QUALITY VERIFICATION AND OFFICIAL APP RECONFIRMATION FOR ADVERTISER 549756244483: OPEN PINTEREST ADS MANAGER EVENT QUALITY, CONVERSIONS HEALTH, ENHANCED MATCH, VERIFIED MERCHANT, AND AUTOMATIC ENHANCED MATCH VIEWS; OPEN THE OFFICIAL SHOPIFY PINTEREST APP AND THE SHOPIFY CUSTOMER EVENTS LIST PAGE; CONFIRM SHARE-ALL-EVENTS REMAINS ON, ADVERTISER BINDING REMAINS 549756244483, AND NO SECOND PINTEREST PIXEL EXISTS; NO CAMPAIGN, AD GROUP, AD, PRODUCT GROUP, AUDIENCE, BUDGET, BID, STATUS, TAG, CAPI, CATALOG, DATA SOURCE, FEED, MERCHANT, GOOGLE ADS, SHOPIFY PRODUCT, MARKETS, SHIPPING, OR THEME WRITE; READ BACK BEFORE AND AFTER.
```

### Phrase B: Event-firing theme repair (specific snippet/file scope, no Shopify Admin product data, no live spend)

```
APPROVE NARROW SHOPIFY CUSTOMER EVENTS WEB PIXEL ADDITION FOR PINTEREST EVENT QUALITY REPAIR ONLY (PRODUCT_ID ON ADD_PAYMENT_INFO AND HASHED_EMAIL ON ADD_TO_CART): IMPLEMENT INSIDE A SINGLE NEW SHOPIFY CUSTOMER EVENT SUBSCRIBER (NOT A LIQUID THEME EDIT), REUSE THE OFFICIAL SHOPIFY PINTEREST APP EVENT_ID FOR DEDUPE, FIRE ONLY ADD_PAYMENT_INFO AND ADD_TO_CART, NO PAGE_VISIT/VIEW_CATEGORY/CHECKOUT/INITIATE_CHECKOUT/SEARCH/SIGNUP/LEAD; NO SECOND BASE TAG, NO PINTRK INSTALL IN LAYOUT/THEME.LIQUID OR ANY SNIPPET; NO SHOPIFY ADMIN PRODUCT DATA, MERCHANT, FEED, CATALOG, MARKETS, SHIPPING, OR CHECKOUT WRITE; NO PINTEREST CAMPAIGN, AD GROUP, AD, PRODUCT GROUP, AUDIENCE, BUDGET, BID, OR STATUS WRITE; NO LIVE SPEND ENABLEMENT; READ BACK BEFORE AND AFTER WITH NETWORK CAPTURE PROVING NO DUPLICATE EMISSION.
```

Phrase A is the recommended first step. Phrase B is held in reserve in case Phrase A's reconfirmation does not lift `product_id__ADD_PAYMENT_INFO` and `hashed_email__ADD_TO_CART` after a 7 to 14 day observation window.

---

## 6. Definition of "Good enough to enable"

Live Pinterest spend should be unblocked only when **all** of the following readbacks are observed in a single Event Quality session:

### 6.1 Overall and per-source quality

- `https://api.pinterest.com/ads/v4/advertisers/549756244483/conversions/acq_overall_status?lookback_period`:
  - `data.sourcePlatforms.WEB.ingestionSources.TAG.status` = `GOOD`.
  - `data.sourcePlatforms.WEB.ingestionSources.CONVERSIONS_API.status` = `GOOD`.
- Event Quality summary card on the dashboard reads `Good` (matching `raw/event_quality.txt` line 33 wording, but with `Good` substituted for `Fair`).

### 6.2 Per-event status thresholds (from `acq_scores`)

For each of `PAGE_VISIT`, `ADD_TO_CART`, `INITIATE_CHECKOUT`, `ADD_PAYMENT_INFO`, `CHECKOUT`:

- `product_id` block: `status = GOOD`. `product_id_coverage` value >= `50.0` (today: AddToCart 100, IC 100, Checkout 100, AddPaymentInfo `0.0` `FAIL`). The blocking event today is AddPaymentInfo only.
- `hashed_email` block: `status = GOOD`. `hashed_email_coverage` value >= `25.0`. Today AddToCart is `4.225...` `FAIL`; Checkout `100.0` `PASS`; IC `43.39...` `PASS`; AddPaymentInfo `100.0` `PASS`. The blocking event today is AddToCart only.
- `advertiser_external_id` block: `status = GOOD` (already true today on all events).
- `ip_address`, `user_agent`, `source_url`, `order_value` blocks: `status = GOOD` (already true today across the board).

### 6.3 Enhanced Match group

- `https://api.pinterest.com/ads/v4/advertisers/549756244483/conversions/health?criteria_group_key=Enhanced+Match`:
  - `data.status` = `PASS` OR `data.status` = `WARN` with no `level: ERROR` items on `CHECKOUT`, `ADD_TO_CART`, `ADD_PAYMENT_INFO`, `INITIATE_CHECKOUT`, `PAGE_VISIT`.
  - `signup_has_em`, `lead_has_em`, `watch_video_has_em`, `app_install_has_em` may remain `MISSING` (the merchant does not fire those events; they are not blockers if the dashboard treats them as informational).
  - `search_has_em` and `view_category_has_em` should reach `PASS`.

### 6.4 Verified Merchant Program and Automatic Enhanced Match

- Verified Merchant Program `status: PASS` (already true today).
- Automatic Enhanced Match `status: PASS`, `aem_enabled` value `100.0` (already true today).

### 6.5 Dedupe

- `external_event_id` block on at least `PAGE_VISIT` and `VIEW_CATEGORY` remains `status: GOOD` with `external_event_id_overlap` value >= `90.0` (today PAGE_VISIT 94.5, VIEW_CATEGORY 97.0).

### 6.6 Click ID exception

- `click_id_epik__CHECKOUT` and the rest of the `click_id_epik` block may remain `NEEDS_IMPROVEMENT` at first live-enable time. Rationale: this metric requires real Pinterest click traffic (`_epik` cookie set on a paid landing) to populate, which is impossible while spend is `$0.00` (`raw/campaign_spend_baseline.txt` baseline). It must be re-evaluated 14 days after first live spend; if it still reads `0.0` at that point, that is the trigger for a deeper investigation.

### 6.7 Freshness

- `https://api.pinterest.com/ads/v4/advertisers/549756244483/conversions/latest`:
  - `data.TAG` and `data.CONVERSIONS_API` timestamps both within the last 1 hour (today both fresh: TAG `1778219456502890000`, CAPI `1778219473760287700`).

If 6.1, 6.2, 6.3, 6.4, 6.5, and 6.7 are met (with 6.6 acknowledged as volume-gated), Event Quality is "Good enough to enable" the previously approved 342-row paused US draft.

---

## 7. Guardrails preserved

- No Pinterest writes (campaign, ad group, ad, product group, audience, budget, bid, status, tag, CAPI, catalog source, data source, feed). No browser/account access.
- No Shopify Admin writes (product data, Markets, shipping, customer events, theme).
- No theme edits. No new files in `snippets/`, `assets/`, `layout/`, `sections/`, `templates/`, `config/`.
- No `ops/PROBLEM_TRACKER.md` modification; integration deferred to parent.
- No customer PII, cookies, request headers, payment data, or credentials stored.
- `ops/AGENT_WORKLOG.md` not modified; integration deferred to parent.

## 8. Files touched

Created (this lane only):
- `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-deep-followup/lanes/pinterest-event-quality-fix-plan/PINTEREST_EVENT_QUALITY_FIX_PLAN_REPORT.md`

Read-only references:
- `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-pinterest-catalog-event-unblock/PINTEREST_CATALOG_EVENT_UNBLOCK_REPORT.md`
- `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-pinterest-catalog-event-unblock/lanes/pinterest/raw/event_quality_api_probe.json`
- `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-pinterest-catalog-event-unblock/lanes/pinterest/raw/event_quality.txt`
- `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-pinterest-catalog-event-unblock/lanes/pinterest/raw/campaign_spend_baseline.txt`
- `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-safe-resume/lanes/pinterest-paused-draft/PINTEREST_PAUSED_DRAFT_GATE_REPORT.md`
- `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/01_EXPORTS_RAW/PINTEREST/2026-04-28_authenticated_browser_capture/conversion_health_network.json`
- `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/04_IMPLEMENTATION_PLANS/2026-04-29-vetted-shopify-admin-fix-orchestration.md`
- `/Users/fsuels/Projects/dresslikemommy/ops/PROBLEM_TRACKER.md`
- `/Users/fsuels/Projects/dresslikemommy/layout/theme.liquid`
- `/Users/fsuels/Projects/dresslikemommy/layout/password.liquid`
- `/Users/fsuels/Projects/dresslikemommy/snippets/cjpod.liquid`
- `/Users/fsuels/Projects/dresslikemommy/templates/gift_card.liquid`
- `/Users/fsuels/Projects/dresslikemommy/assets/analytics.js`
- `/Users/fsuels/Projects/dresslikemommy/snippets/social-icons.liquid`
- `/Users/fsuels/Projects/dresslikemommy/snippets/header-drawer.liquid`
- `/Users/fsuels/Projects/dresslikemommy/snippets/product-schema-extra.liquid`
- `/Users/fsuels/Projects/dresslikemommy/snippets/jsonld-seo.liquid`
- `/Users/fsuels/Projects/dresslikemommy/snippets/icon-pinterest.liquid`
- `/Users/fsuels/Projects/dresslikemommy/sections/announcement-bar.liquid`
- `/Users/fsuels/Projects/dresslikemommy/sections/footer.liquid`
- `/Users/fsuels/Projects/dresslikemommy/sections/header.liquid`
- `/Users/fsuels/Projects/dresslikemommy/sections/main-password-footer.liquid`
- `/Users/fsuels/Projects/dresslikemommy/config/settings_data.json`
- `/Users/fsuels/Projects/dresslikemommy/config/settings_schema.json`
