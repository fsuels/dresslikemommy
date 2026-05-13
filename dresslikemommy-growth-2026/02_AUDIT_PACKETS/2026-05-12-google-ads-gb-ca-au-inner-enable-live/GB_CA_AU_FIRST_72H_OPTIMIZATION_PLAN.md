# GB/CA/AU First 72h Optimization Plan

Date: 2026-05-12

Decision: `LOCAL_OPERATOR_PLAN_READY_NO_ACCOUNT_WRITES`

## Current Live Test

GB, CA, and AU are live as a tight English-first exact Search micro-cohort:

| Market | Campaign ID | Ad group ID | Enabled scope | Daily budget | Status |
|---|---:|---:|---|---:|---|
| GB | `23838895360` | `194138528537` | 3 exact keywords + 1 RSA | `$2/day` | Enabled / Eligible |
| CA | `23834423669` | `196679079575` | 3 exact keywords + 1 RSA | `$2/day` | Enabled / Eligible |
| AU | `23834424182` | `198852670520` | 3 exact keywords + 1 RSA | `$2/day` | Enabled / Eligible |

Enabled exact keywords in each market:

- `[mommy and me dresses]`
- `[mother daughter dresses]`
- `[mom and daughter matching outfits]`

## ROAS Math

Target ROAS: `650%` / `6.5x`.

Using the existing planning AOV assumption of `$70`, target CPA is:

- `$70 / 6.5 = $10.77` maximum ad cost per purchase.

This first test is deliberately small:

- Per market max spend at current budget: `$2/day`.
- Three-market combined max spend: `$6/day`.
- At 72 hours, expected max exposure is roughly `$6` per market / `$18` combined if Google spends fully.

## First 72h Readback Cadence

| Time | Required readback | Pass/act rule |
|---|---|---|
| T+6h | Status, policy, impressions, clicks, cost | If any campaign leaves `Eligible` or shows policy/URL failure, investigate immediately. |
| T+24h | Impressions, CTR, CPC, cost, search terms, country/location, device, conversions/value | Add negative candidates only from actual irrelevant terms or unmistakable low-buying intent; no budget scale yet. |
| T+48h | Same, plus landing/currency spot-check if clicks occurred | If clicks arrive from wrong country or wrong currency route, pause affected unit under exact approval and repair. |
| T+72h | Same, plus zero-purchase threshold review | If any single market spends `>= $16` with 0 purchases, prepare exact pause approval for that ad group; at `$2/day`, this threshold likely will not trigger by 72h. |
| T+7d | CPA, ROAS, conversion value, search-term quality, market split | Scale only winners with purchase/value evidence; do not scale on clicks alone. |

Current baseline log:

- `gb_ca_au_optimization_baseline_log.csv`
- Baseline timestamp: `2026-05-12T07:38:01-04:00`
- Baseline: GB/CA/AU enabled/eligible, `$2/day`, `1` enabled target ad group and `9` paused ad groups per market, displayed cost `$0.00`, conversions `0.00`, conversion value `$0.00`.

## Kill / Hold / Scale Rules

Hard kill or pause candidate:

- Any campaign/ad group loses eligible status because of policy, URL, or destination mismatch.
- Any clicks appear from outside the intended country.
- Any final URL readback loses market currency: GB must carry GBP, CA CAD, AU AUD.
- Any single market spends `>= $16` with `0` purchases.
- Any market spends enough to prove poor query quality and all search terms are weak retail-comparison, free/DIY, costume, supplier, used, or tutorial intent.

Hold:

- Low impressions and low spend with no clear bad search terms.
- Good CTR but too little spend for conversion judgment.
- One or two clicks with no purchase while search terms are high-intent and landing/currency are clean.

Scale candidate:

- At least one purchase with correct conversion value/currency evidence.
- Search terms remain high-intent and no location/currency drift.
- CPA is on track toward `$10.77` or the campaign has high-quality assisted conversion evidence that justifies controlled continuation.
- Any budget/bid increase still requires exact owner approval naming the campaign and new value.

## Immediate Next Operator Tasks

1. Run read-only Google Ads performance/search-term readbacks for GB/CA/AU once enough time has passed for data to populate.
2. Compare actual search terms against `gb_ca_au_negative_watchlist.csv`.
3. Draft exact negative-keyword approval only for terms supported by evidence or clearly harmful country-tail terms.
4. Keep Pinterest and next-market expansion moving in parallel, but do not scale GB/CA/AU budgets until purchase/value signals justify it.
