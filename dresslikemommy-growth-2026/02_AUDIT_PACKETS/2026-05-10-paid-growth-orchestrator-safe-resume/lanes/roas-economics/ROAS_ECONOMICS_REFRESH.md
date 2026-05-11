# ROAS Economics Refresh

**Lane:** D / Roas-Economics
**AGENT_CONTINUITY_ANCHOR:** 2026-05-10-paid-growth-orchestrator-safe-resume
**Date (Pacific):** 2026-05-10
**Author:** Roas-Economics subagent (local-only, no live spend writes)

---

## 1. Inputs (canonical assumptions)

| Input | Value | Source / Notes |
|---|---|---|
| AOV | $70.00 | Working assumption for paid-growth math |
| Gross margin | 50% | Pre-ad-cost contribution margin |
| Target ROAS | 650% (6.5x) | Operator target for enable/scale decisions |
| Max CPC (active local cap) | $0.15 | Current cap on paused non-US Search builds |
| Per-country daily budget | $2/day | Smallest-future-spend-unit |
| Hard-pause spend rule | $16 cumulative w/ 0 purchases | From 2026-05-08 economics packet |

---

## 2. Canonical economics (formulas + worked values)

**Target CPA (max allowable cost per acquisition):**
`CPA_target = AOV / Target ROAS = $70 / 6.5 = $10.77`

**Gross profit per order, before ad cost:**
`GP_pre_ad = AOV * gross_margin = $70 * 0.50 = $35.00`

**Contribution per order, after target CPA, before returns:**
`Contribution = GP_pre_ad - CPA_target = $35.00 - $10.77 = $24.23`

**Breakeven conversion rate at a given max CPC:**
`CVR_breakeven = max_CPC / CPA_target`

| Max CPC | Breakeven CVR | Formula |
|---|---|---|
| $0.15 | **1.39%** | $0.15 / $10.77 |
| $0.20 | **1.86%** | $0.20 / $10.77 |
| $0.25 | **2.32%** | $0.25 / $10.77 |

Interpretation: at the current $0.15 CPC cap, an ad group needs roughly 1 conversion per 72 clicks to hit the 650% target. Anything materially below that drains contribution.

---

## 3. Pause / kill threshold table (zero-purchase guardrails)

At $0.15 max CPC and $2/day per non-US country build, $16 cumulative spend equates to roughly **106 clicks** ($16 / $0.15) and approximately **8 elapsed days** at the daily cap. That is more than sufficient sample to reject "no signal yet" if zero conversions have landed.

| Cumulative spend, 0 purchases | ~Clicks at $0.15 CPC | Action |
|---|---|---|
| $8 | ~53 | **Warning.** Recheck targeting (geo, device, search-term hygiene, audience overlap). No bid/budget change. |
| $16 | ~106 | **Hard pause.** Pause ad group, log review note, escalate to operator. No restart without fresh approval. |
| $24 (single ad group, cumulative) | ~160 | **Kill ad group.** Do not resurrect under same configuration; require restructure before any re-enable. |

These thresholds apply per ad group. Account- or campaign-level totals are tracked separately and do not trigger ad-group kill on their own.

---

## 4. Standard Shopping post-May-6 readback (starvation, not failure)

Post-2026-05-06 through 2026-05-09 Pacific:

- 1 click, 58 impressions, $0.02 cost, avg CPC $0.02, 0.00 conversions, $0.00 conversion value.
- All-time on Standard Shopping: 82 clicks, 3,962 impressions, $18.60 cost, $0.23 avg CPC, 0 conversions.

**Interpretation:** 1 click in 4 days at $0.02 avg CPC is **starvation**, not a performance signal. The campaign is delivering essentially zero auction presence; a 0% CVR on n=1 click is statistically meaningless. The all-time $0.23 avg CPC vs. current $0.02 indicates the campaign is being out-bid out of the auction entirely, likely a combination of bid cap, bid strategy, or feed/quality issue rather than demand or creative.

**Recommendation:** Do **not** change budget, bid, max-CPC cap, targeting scope, or campaign structure on Standard Shopping. The $16 zero-purchase rule has not yet tripped (current cumulative post-May-6 spend = $0.02). Let impressions stabilize and accumulate before drawing any conclusion. **Reaffirmed guardrail: no Standard Shopping change without fresh explicit operator approval.**

---

## 5. Smallest-future-spend-unit recommendation (first approved live enable)

For the first live enable per the existing market activation scorecard, **GB / Mommy & Me Dresses - Exact only**:

| Parameter | Value |
|---|---|
| Geo | GB only |
| Match type | Exact only |
| Daily budget | $2/day |
| Max CPC | $0.15 |
| Hard-pause trigger | $16 cumulative spend w/ 0 purchases |
| Warning trigger | $8 cumulative spend w/ 0 purchases |
| Kill trigger (ad group) | $24 cumulative spend w/ 0 purchases |
| Target CPA | $10.77 |
| Breakeven CVR at $0.15 CPC | 1.39% |
| Review checkpoints | 24h, 72h, 7d (Pacific) |

**Checkpoint expectations:**
- **24h:** confirm impressions are flowing (>0), avg CPC within cap, no policy/disapproval flags. No optimization actions.
- **72h:** confirm spend trajectory is on pace (~$6 cumulative); if spend < $1 cumulative, treat as starvation, do not raise bid without approval.
- **7d:** evaluate against conv data only if cumulative spend >= $8. If spend < $8 by day 7, extend window; do not draw CVR conclusions on undersampled data.

---

## 6. Guardrails preserved

- No live spend, campaign, ads, budget, bid, conversion, status, product, feed, theme, payment, or order writes performed by this lane.
- No browser or account access used.
- `ops/PROBLEM_TRACKER.md` not modified; parent integrates.
- Standard Shopping untouched; no recommendation taken without fresh operator approval.
- All numbers above are math refreshes against existing assumptions; they do not constitute approval to enable any campaign.

---

## 7. Files touched

- Created: `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-safe-resume/lanes/roas-economics/ROAS_ECONOMICS_REFRESH.md`

No other files modified.
