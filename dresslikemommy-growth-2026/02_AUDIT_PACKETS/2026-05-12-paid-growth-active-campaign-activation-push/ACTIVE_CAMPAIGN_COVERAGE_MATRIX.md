# Active Campaign Coverage Matrix

Generated: 2026-05-12

Owner-stated goal:
- Working active Google Ads and Pinterest campaigns for every viable language/market.

Important correction:
- The goal is not complete. The prior safe-lane packet only advanced and documented blockers. It did not make all campaigns active.
- New campaign activation, spend, budget/bid/status edits, Pinterest account objects, Merchant uploads, conversion-goal changes, or Shopify production mutations still require fresh exact action-time approval.

## Google Ads

### Active / Live Now

| Market | Language posture | Campaign | ID | Current state | Notes |
|---|---|---|---|---|---|
| US | English Shopping | `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY` | `23802638621` | Enabled / Eligible | Shopping, `US$20/day`, tight paid cohort, child bids lowered to `$0.04`. Do not touch status/budget/product scope/feed labels/product groups/conversion goals without exact approval. |
| US | English Brand Search | `DLM_US_SEARCH_BRAND_PROTECT_PAUSED_20260429` | `23805046526` | Enabled Search | Latest sidecar says newer 2026-05-06 evidence supersedes older `$5/day` text: `$2/day`, Maximize clicks, `$0.15` max CPC bid limit. Fresh readback still prudent before operational decisions. |

### Built But Paused

| Market | Language posture | Campaign | ID | Budget | Status | Activation blocker |
|---|---|---|---|---:|---|---|
| US | English nonbrand | `DLM_US_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260506` | `23827590655` | `$2/day` | Paused | Needs activation approval and just-in-time readbacks. |
| GB | English | `DLM_GB_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | `23838895360` | `$2/day` | Paused | First non-US activation candidate after GA4 non-US purchase proof closes or exact controlled-test approval path resolves it. |
| CA | English | `DLM_CA_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | `23834423669` | `$2/day` | Paused | Needs measurement proof and activation approval. |
| AU | English | `DLM_AU_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | `23834424182` | `$2/day` | Paused | Needs measurement proof and activation approval. |
| CH | Split/gated | `DLM_CH_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | `23834425358` | `$1/day` | Paused | Needs language split / English-first decision before active spend. |
| DK | Danish gated | `DLM_DK_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | `23838969244` | `$1/day` | Paused | Danish native rewrite required before native platform use; English-first would need explicit owner decision. |
| DE | German | `DLM_DE_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | `23834427575` | `$1/day` | Paused | Supplier/source-token and mixed-language/base-route blockers must clear before native/localized spend. |
| NL | Dutch | `DLM_NL_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | `23829110118` | `$1/day` | Paused | Needs native title/copy QA and final URL map refresh. |
| SE | Swedish | `DLM_SE_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | `23838970036` | `$1/day` | Paused | Supplier/source-token and English fallback title/H1 blockers must clear. |
| ES | Spanish | `DLM_ES_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | `23829133584` | `$1/day` | Paused | Cleanest native-review candidate, but still needs native review/full URL QA and measurement proof. |
| IT | Italian | `DLM_IT_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | `23829232530` | `$1/day` | Paused | Cleanest native-review candidate, but still needs native review/full URL QA and measurement proof. |
| PL | Polish | `DLM_PL_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | `23829238698` | `$1/day` | Paused | Needs native title/copy QA and final URL map refresh. |
| CZ | Czech | `DLM_CZ_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | `23829253812` | `$1/day` | Paused | Supplier/source-token/native QA blockers must clear. |

Readback basis:
- The 12 non-US built campaigns above were read back as paused Search, presence-only, content network off, and YouTube off.
- `GB`, `IT`, `PL`, and `CZ` previously required presence-only repairs after `DONT_CARE` readbacks and then passed.

### Absent / Parked

| Market | Language posture | State | Exact blocker | Next safe action |
|---|---|---|---|---|
| RO | Romanian | Absent / uncreated | Prior preview became stale/not visible; retry hit Google Ads concurrent-upload/throttle before upload. Landing has supplier/source-token blocker. | After cooldown, confirm no active in-progress `RO`/`FR`/`BE` row and no `RO` campaign, then retry one-country RO preview only. |
| PT | Portuguese | Absent / unattempted | Blocked behind one-country-at-a-time RO guard; `pt-BR` vs `pt-PT` language/dialect decision still open. | Either solve/park RO with exact owner decision, then preview PT one-country-at-a-time after dialect decision. |
| GR | Greek | Absent / unattempted | Blocked behind RO/PT sequencing and Greek native-review/platform-use gate. | Preview only after upstream sequence or exact owner skip/park decision. |
| FR | French | Parked | Stale/in-progress preview/apply recovery produced completed-with-errors/no changes and no FR campaign. | Fresh non-stale `88/88 # OK` preview plus no-duplicate readback. |
| BE | French/Dutch split | Parked | Google Ads upload throttle and Belgium FR/NL split/route proof unresolved. | Last after upload-throttle cooldown and language-split decision. |

### Not Activation Ready

| Surface | State | Why not active-ready |
|---|---|---|
| PMax Shopping / PMax T-Shirts | Paused/blocked | Wrong/no-products and readiness risks; do not enable by inference. |
| Remarketing `23609373008` | Paused | Prior enable attempt hit `Most ads limited by policy`, then rollback. |
| Native-language Google Ads replacement rows | Local only | `REVIEW_ONLY_NOT_UPLOAD`; native review and landing QA required. |

## Pinterest

### Active / Live Now

| Market | Language posture | State | Notes |
|---|---|---|---|
| All | All | No active Pinterest campaigns documented | Known baseline remains `0` campaigns, `0` serving, `$0.00` spend. |

### Account-Ready Only After Approval

| Market | Language posture | Scope | State | Activation blocker |
|---|---|---|---|---|
| US | `en-US` | Clean `342` EN-US `IN_STOCK` rows; exclude variants `41878208249953`, `41878208479329`, `41878208577633`, `41878208610401` | Paused-draft operator templates exist, review-only | Exact approval required to create paused Pinterest drafts/account objects. Live spend separately gated. |

Pinterest US known IDs:
- Advertiser `549756244483`
- Catalog `Catalog_Retail` / `3041764155561548387`
- Allowed EN Shopify feed profile `3041760867124595727`
- Blocked failed sitemap source `3041760916127467912`

### Non-US Pinterest

| Market group | State | Gap |
|---|---|---|
| GB / CA / AU | Best next local packet candidates | No country-specific Pinterest catalog/source/feed profile, item-level readback, clean in-stock scope, product-group filter readback, exclusion set, localized promoted-pin approval, country targeting readback, or paused account objects. |
| ES / IT / DE / NL / SE / FR / PL / CZ / RO / PT / DK / BE / GR / CH | Local-only prep or gated | Needs Pinterest-specific scope/source proof plus native copy/landing-language QA and market split decisions. |

### Pinterest Event Quality / Tag Blockers

Known remaining blockers:
- Event Quality `Fair`
- `product_id__ADD_PAYMENT_INFO`
- `hashed_email__ADD_TO_CART`
- `click_id_epik__CHECKOUT`
- Enhanced Match `ERROR`

Important guardrail:
- Repo evidence finds no theme-side Pinterest event code. Pinterest tag/CAPI is via the official Shopify Pinterest app through `content_for_header`. Do not add a duplicate theme tag or custom CAPI by inference.

## Global Gating Before New Live Activation

Before any new non-US Google Ads active spend:
1. GA4 property `330266838` must prove order-level non-US purchase `transaction/currency/value`, or owner must explicitly approve a controlled non-US test purchase/refund/cancel.
2. Chosen campaign/ad group must pass just-in-time readbacks: paused status, intended budget, CPC cap, presence-only location, Search-only, content/YouTube off, account-default purchases, no conversion-goal override, clean change history.
3. Chosen final URL must pass action-time storefront readback: correct country/currency, add-to-cart, checkout entry without payment, no verification wall, no stale metadata issue.
4. Any native-language campaign use must have native review and landing-language QA.
5. Any approval must name the exact campaign/ad group/product scope/change.

Before any Pinterest active spend:
1. Create paused account objects first with exact approval and readbacks.
2. Reconfirm Event Quality/app binding if the owner wants a freshness check.
3. Do not create live Pinterest spend or budgets/bids/status activation without a separate exact live-spend approval.

## Parent Interpretation

The real goal is all viable language/market campaigns active and working across Google Ads and Pinterest.

Closest safe next actions:
1. Close or explicitly approve the measurement gate path.
2. Get exact approval for the first Google Ads non-US activation only after gate closure.
3. Get exact approval for paused Pinterest US draft creation.
4. Continue absent Google Ads country build only one-country-at-a-time after upload-throttle cooldown and no-duplicate readbacks.
5. Build Pinterest non-US local scope packets starting GB, CA, AU, then localized markets.
