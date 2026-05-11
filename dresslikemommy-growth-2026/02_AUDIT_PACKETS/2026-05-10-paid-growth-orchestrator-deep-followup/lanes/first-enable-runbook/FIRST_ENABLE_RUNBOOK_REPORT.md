# First-Enable Runbook - GB / Mommy & Me Dresses - Exact

**Lane:** E / First-Enable-Runbook
**AGENT_CONTINUITY_ANCHOR:** 2026-05-10-paid-growth-orchestrator-deep-followup
**Date (Pacific):** 2026-05-10
**Author:** First-Enable-Runbook subagent (local file write only; no live writes, no browser, no network)
**Scope:** Operator-facing runbook for the very first non-US live spend action. This document **prepares for** the first-enable; it does **not** make or execute the enable decision.

---

## 0. Subject of this runbook

| Field | Value |
|---|---|
| Campaign name | (existing GB paused Search test) |
| Campaign ID | `23838895360` |
| Country / market | `GB` |
| Network | Google Search Network only |
| Channel | Search |
| Daily budget | `$2/day` (USD) - no change |
| Bid strategy | Manual CPC |
| Max CPC cap | `$0.15` - no change |
| Location | United States/UK presence-only (`LOCATION_OF_PRESENCE`); positive geo = `GB`, negative geo = excluded surfaces |
| Content / YouTube | Off |
| Ad group to enable | `Mommy & Me Dresses - Exact` |
| Match type policy | Exact only |
| Other ad groups in campaign | All remain Paused |
| Conversion goal posture | Account-default `Purchases` (no goal change) |
| Status before action | Paused (campaign + all ad groups) |
| Status after action | Campaign Enabled, only `Mommy & Me Dresses - Exact` ad group Enabled, all other ad groups remain Paused |

Source: `MARKET_ACTIVATION_SCORECARD.md` (lane E of 2026-05-10-paid-growth-orchestrator-safe-resume) and `ROAS_ECONOMICS_REFRESH.md` (lane D, same packet).

---

## 1. Pre-enable gate checklist

The operator must walk this checklist top-to-bottom and confirm each item before clicking Enable. Any FAIL aborts the enable. Items 1-7 are the canonical safety gates; items 8-12 are the operator-side just-in-time live readbacks captured the same minute as the action.

> **Forward-dependency note.** Two sibling lanes in this same packet have not been written yet at the time this runbook was authored:
> - Lane A `ads-apply-playbook` at `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-deep-followup/lanes/ads-apply-playbook/ADS_APPLY_PLAYBOOK_REPORT.md` - **NOT YET PRESENT.** When that report is written, items 9 and 10 below must be reconciled against any final UI-step refinements it contains.
> - Lane B `measurement-conversion-gap` at `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-deep-followup/lanes/measurement-conversion-gap/MEASUREMENT_CONVERSION_GAP_REPORT.md` - **NOT YET PRESENT.** When that report is written, item 4 below must be reconciled against any cross-market conversion-goal exposure it identifies. If lane B finds a conversion-goal isolation gap, this runbook does not authorize enable until the gap is closed.

### Canonical gates (1-7)

- [ ] **1. Owner approval phrase received verbatim.** The exact phrase in section 2 of this runbook has been pasted by the owner in chat with no edits, no abbreviations, and no rewording. If anything in the phrase is altered (campaign ID, ad-group name, budget, CPC, scope), abort and re-request.
- [ ] **2. Beach-SEO mitigation still intact.** Confirm the held CSV `00_intl_search_paused_draft_web_bulk_vacation_family_hold.csv` and the `GB_intl_search_paused_draft_web_bulk.csv` split still show `0` bad-handle hits and `0` `Vacation Family` rows tied to the bad handle. Source of truth: `lanes/beach-seo-gate/BEACH_SEO_GATE_REPORT.md` (2026-05-10-paid-growth-orchestrator-safe-resume), section 1 and 2. `PROB-2026-05-08-BEACH-OUTFIT-SEO-TITLE-MISMATCH` mitigation must read `PARTIALLY_MITIGATED_LOCAL_ADS_HOLD` or stronger.
- [ ] **3. GB landing/checkout QA still passing.** GB checkout-to-shipping QA recorded `PASS` 2026-05-08: `en-GB`, GBP, Standard `FREE`, Express `GBP 10.00`. No newer regression in `ops/PROBLEM_TRACKER.md`. Source: `MARKET_ACTIVATION_SCORECARD.md` row `GB`.
- [ ] **4. Conversion-goal cross-market risk audited.** GB campaign reuses the US-tied `Purchases` account-default conversion goal. Confirm:
  - Account purchase action (`Google Shopping App Purchase` / `Purchases`, primary, dynamic value, enhanced conversions on) is unchanged from the 2026-04-30 measurement gate pass evidence.
  - No campaign-level conversion-goal override has been added on `23838895360`.
  - GA4 measurement id remains `G-N4EQNK0MMB` and Google Ads conversion endpoint `www.googleadservices.com/pagead/conversion/853411529/` label `UbkpCN-fhogBEMmN-JYD` is still firing on the `/checkouts/.../thank_you` flow.
  - **Forward dependency:** if Lane B (`measurement-conversion-gap`) is published and identifies a cross-market exposure (for example, value/currency leak, transaction-id collision, dedupe miss, or non-US enhanced-conversion hash absence), DO NOT proceed; route back to parent.
- [ ] **5. Standard Shopping not in a regressed state.** `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY` (`23802638621`) status icon must read `Enabled`, budget `$20/day` (or whatever the current owner-approved level is), no supplier-domain leak, no product-group regression. Post-May-6 readback baseline: 1 click / 58 impressions / $0.02 cost / 0 conversions over 2026-05-06 to 2026-05-09. This is starvation, not failure (per Lane D section 4). The runbook does **not** treat starvation as a regression. A regression is only triggered if any of: status flips off Enabled, budget or max CPC moves without owner approval, supplier-domain text reappears, or `Everything else in "All products"` becomes enabled.
- [ ] **6. Brand Search not in a regressed state.** `DLM_US_SEARCH_BRAND_PROTECT_PAUSED_20260429` reads `Eligible`, `$5.00/day`, `Maximize clicks`, max CPC cap `$0.20`, primary purchase conversion goal at account default. No newer Brand Search edit in the worklog tail since the 2026-05-01 owner-set-`$5/day` readback.
- [ ] **7. No other writer claim active in `ops/AGENT_COORDINATION.md` for Google Ads.** Search the file for any active row touching: `Google Ads`, `non-US Search`, `paused build`, `enable`, `campaign 23838895360`, or `GB`. If any is `IN_PROGRESS` or claimed by a different agent/lane, do not proceed; resolve coordination first. Specifically the `2026-05-10 Google Ads non-US Search paused build IT recheck / remaining absent` lane must already read DONE/handed off, and the `localized-shipping-info-link-repair` lane must read `DONE_LIVE_THEME_PUSH_READBACK_PASSED`.

### Just-in-time GB campaign RPC readback (8-12), captured live within 5 minutes of the enable

- [ ] **8. RPC readback - paused state.** Read campaign `23838895360` from Google Ads RPC. Confirm `serving_status` reads paused/`PAUSED` and `status` reads `PAUSED` immediately before the click.
- [ ] **9. RPC readback - Search / presence-only / English / GB geo.** Confirm:
  - `advertising_channel_type = SEARCH`
  - `advertising_channel_sub_type` not Standard Shopping, not PMax
  - Network: Google Search Network only; content network OFF, YouTube OFF
  - Languages: English (en)
  - Locations: positive `GB`, negative excluded surfaces; positive geo target type `LOCATION_OF_PRESENCE`; negative geo target type `LOCATION_OF_PRESENCE`
  - Budget = `$2.00/day`
  - Bid strategy = `MANUAL_CPC`, max CPC cap = `$0.15`
- [ ] **10. RPC readback - ad group inventory.** Confirm the campaign contains the named ad group `Mommy & Me Dresses - Exact` and that it is currently `PAUSED`. Confirm all other ad groups in this campaign are also `PAUSED` (so that the post-action delta is exactly +1 ad group enabled, +1 campaign enabled).
- [ ] **11. No PMax / no Standard Shopping / no Merchant feed binding on this campaign.** Confirm no `merchant_id`, no `feed_label`, no PMax asset group, no Shopping product-group structure attached to `23838895360`. This is a pure non-Shopping Search campaign.
- [ ] **12. No conversion-goal override.** Confirm `selective_optimization` / campaign-level conversion-goal customization is unset on `23838895360` (campaign uses account-default Purchases).

If every box from 1-12 is checked, the operator is cleared to proceed to section 3. If any box is unchecked, abort and route back to parent for resolution.

---

## 2. Exact owner-approval phrase (verbatim, paste-ready)

The owner must paste this phrase in chat with no edits before any enable click. The format follows the `APPROVE PAUSED NON-US GOOGLE SEARCH TEST BUILD ONLY...` style established in `ops/prompts/paid-growth-ai-army-continuation-prompt.md` (lines 179-181).

```
APPROVE FIRST NON-US LIVE ENABLE - GB SEARCH ONLY: ENABLE CAMPAIGN 23838895360 (GB PAUSED NON-US SEARCH TEST BUILD) AND ENABLE ONLY THE AD GROUP "Mommy & Me Dresses - Exact"; LEAVE ALL OTHER AD GROUPS IN CAMPAIGN 23838895360 PAUSED; KEEP DAILY BUDGET AT $2.00/DAY WITH NO BUDGET CHANGE; KEEP MANUAL CPC WITH MAX CPC CAP $0.15 WITH NO BID CHANGE; KEEP PRESENCE-ONLY GB GEO TARGETING; KEEP CONTENT NETWORK AND YOUTUBE OFF; KEEP ACCOUNT-DEFAULT PURCHASES CONVERSION GOAL WITH NO CONVERSION-GOAL CHANGE AND NO CAMPAIGN-LEVEL OVERRIDE; NO US CAMPAIGN 23827590655 CHANGES; NO PMAX, STANDARD SHOPPING, MERCHANT, FEED, PRODUCT-SCOPE, FEED-LABEL, PRODUCT-GROUP, SHOPIFY PRODUCT-DATA, PINTEREST, GA4/GTM, OR THEME CHANGES; NO ENABLE OF CA, AU, CH, DK, DE, NL, SE, OR ES PAUSED CAMPAIGNS; READ BACK CAMPAIGN STATUS, AD GROUP STATUS, BUDGET, MAX CPC, NETWORK, GEO, AND CONVERSION-GOAL BEFORE AND AFTER; APPLY $8 ZERO-PURCHASE WARNING / $16 ZERO-PURCHASE HARD-PAUSE / $24 ZERO-PURCHASE AD-GROUP-KILL RULE.
```

Headline (first 80 chars): `APPROVE FIRST NON-US LIVE ENABLE - GB SEARCH ONLY: ENABLE CAMPAIGN 23838895360`

---

## 3. Apply-time runbook (Google Ads UI step-by-step)

The operator runs these steps in the existing logged-in Google Ads tab. Every step has an evidence capture obligation. Save all evidence under:

```
dresslikemommy-growth-2026/02_AUDIT_PACKETS/<YYYY-MM-DD>-google-ads-non-us-first-enable-gb/
  raw/
    pre-enable-readback/
      campaign_23838895360_rpc_pre.json
      campaign_23838895360_overview_pre.png
      adgroup_mommy_me_dresses_exact_only_pre.png
    enable-action/
      campaign_enable_click_pre.png
      adgroup_enable_click_pre.png
      campaign_enable_click_post.png
      adgroup_enable_click_post.png
      enable_action_timestamp.txt
    post-enable-readback/
      campaign_23838895360_rpc_post.json
      campaign_23838895360_overview_post.png
      adgroup_mommy_me_dresses_exact_only_post.png
      campaign_locations_panel_post.png
      campaign_networks_panel_post.png
      campaign_settings_panel_post.png
  FIRST_ENABLE_GB_EXECUTION_REPORT.md
```

Replace `<YYYY-MM-DD>` with the operator-time date.

### Steps

1. **Open the campaign overview tab.**
   Navigate to Google Ads -> All campaigns -> filter to campaign id `23838895360`. Capture full-page screenshot to `pre-enable-readback/campaign_23838895360_overview_pre.png`.

2. **Capture pre-enable RPC readback.** Run the existing CDP/RPC helper used by prior non-US lanes (the same helper that produced `working/final_campaign_readback_summary_2026-05-10*.json` for the paused build). Save to `pre-enable-readback/campaign_23838895360_rpc_pre.json`. Verify the JSON shows `status=PAUSED`, `advertising_channel_type=SEARCH`, budget `$2/day`, max CPC `$0.15`, `LOCATION_OF_PRESENCE`, content/YouTube off, and the `Mommy & Me Dresses - Exact` ad group present and `PAUSED`.

3. **Re-walk gate checklist items 1-12** in section 1 of this runbook. Stop if any FAIL.

4. **Drill into ad groups view** for campaign `23838895360`. Confirm visible row for `Mommy & Me Dresses - Exact` with status `Paused` and that all other ad-group rows in this campaign also read `Paused`. Capture screenshot to `pre-enable-readback/adgroup_mommy_me_dresses_exact_only_pre.png`.

5. **Enable the ad group first.** Toggle only the `Mommy & Me Dresses - Exact` ad group from `Paused` to `Enabled`. Do not multi-select. Capture screenshot of the click target before (`enable-action/adgroup_enable_click_pre.png`) and after (`enable-action/adgroup_enable_click_post.png`).

6. **Enable the campaign.** Return to the campaign row and toggle campaign `23838895360` from `Paused` to `Enabled`. Capture screenshot of the click target before (`enable-action/campaign_enable_click_pre.png`) and after (`enable-action/campaign_enable_click_post.png`). Write the local timestamp to `enable-action/enable_action_timestamp.txt` in ISO-8601 with timezone (for example `2026-05-10T19:09:00-07:00`).

7. **Capture post-enable RPC readback** within 60 seconds of the second click. Save to `post-enable-readback/campaign_23838895360_rpc_post.json`. The expected delta vs pre is exactly: campaign `status=ENABLED`, ad group `Mommy & Me Dresses - Exact` `status=ENABLED`. Everything else (budget, max CPC, networks, geo, conversion goal) must be byte-identical to pre.

8. **Capture post-enable UI readbacks.** Take three additional screenshots from the campaign settings: the Locations panel (`post-enable-readback/campaign_locations_panel_post.png`), the Networks panel (`post-enable-readback/campaign_networks_panel_post.png`), and the campaign Settings overview (`post-enable-readback/campaign_settings_panel_post.png`). Confirm visually: `LOCATION_OF_PRESENCE`, GB-only, Search-only, content/YouTube off.

9. **If the post-RPC delta is anything other than the exact +1 ad group / +1 campaign enable**, immediately execute section 5 rollback. Do not attempt to "fix" with another click.

10. **Write the execution report.** Fill `FIRST_ENABLE_GB_EXECUTION_REPORT.md` with the captured evidence paths, the verbatim approval phrase the owner pasted, the pre/post RPC delta diff, and a worklog anchor `AGENT_CONTINUITY_ANCHOR: <YYYY-MM-DD>-google-ads-non-us-first-enable-gb-live`.

11. **Append to `ops/AGENT_WORKLOG.md`** at the bottom with that anchor, the campaign id, the ad group name, the timestamp, and pointers to the evidence files.

12. **Update `ops/AGENT_COORDINATION.md`** to mark the first-enable lane `DONE_LIVE_ENABLE_GB_RPC_READBACK_PASSED` and release the writer claim.

---

## 4. Review schedule and thresholds

All times below are Pacific. Anchor T0 = the timestamp recorded in `enable-action/enable_action_timestamp.txt`. All economics math traces to `ROAS_ECONOMICS_REFRESH.md` (lane D, 2026-05-10-paid-growth-orchestrator-safe-resume).

### 4a. T+24h checkpoint

**Read these metrics, in this order, from Google Ads UI and RPC:**

1. Campaign-level: status (must remain `Enabled`), impressions, clicks, cost, avg CPC, conversions, conversion value.
2. Ad-group-level (`Mommy & Me Dresses - Exact`): same six metrics.
3. Search terms report: any irrelevant queries already serving.
4. Locations report: confirm 100% of clicks/impressions are in `GB`.
5. Devices report: device split.
6. Policy / disapproval flags on the campaign and on every keyword and every RSA in the active ad group.

**Expected at T+24h (from Lane D section 5):** impressions > 0, avg CPC at or below `$0.15`, no policy/disapproval flags, no non-GB clicks. Cumulative spend trajectory is ~$0-$2 (likely under $1 because Manual CPC at `$0.15` cap rarely hits full budget on day 1).

**Actions at T+24h:**

- **No optimization actions.** Do not raise bid, lower bid, change geo, change keywords, or change creative. The 24h check is observational only.
- If impressions = 0, log "starvation watch" and continue. Per Lane D, post-May-6 Standard Shopping behavior shows that low-CPC caps can starve out of the auction; this is not failure.
- If any policy/disapproval flag appears, route to parent.
- If non-GB clicks appear, this is a presence-only targeting regression: pause the ad group immediately (section 5 rollback), do not pause the whole account.

### 4b. T+72h checkpoint

**Read same six metrics + search terms + locations + devices.**

**Expected at T+72h (Lane D section 5):** cumulative spend on pace for ~$6 (~$2/day x 3 days). If cumulative spend < $1, treat as starvation, do not raise bid without owner approval.

**Kill thresholds engaged at T+72h** (per Lane D section 3):

| Cumulative ad-group spend | Cumulative purchases | Action |
|---|---|---|
| `>= $8` | `0` | **Warning.** Recheck targeting (geo, device, search-term hygiene, audience overlap). No bid/budget change. Document in worklog. |
| `>= $16` | `0` | **Hard pause.** Pause ad group, log review note, escalate to operator. No restart without fresh owner approval. (See section 5 rollback.) |
| `>= $24` | `0` | **Kill ad group.** Do not resurrect under same configuration. Restructure required before any re-enable. (See section 5 rollback.) |

If T+72h cumulative spend is `< $8`, none of the kill thresholds have engaged yet; continue to T+7d.

### 4c. T+7d checkpoint (full review)

**Read all metrics from above plus:**

7. CVR (conversions / clicks) - only meaningful if cumulative clicks `>= 50`.
8. CPA (cost / conversions) - only meaningful if conversions `>= 1`.
9. ROAS (conversion value / cost) - only meaningful if conversion value > 0.
10. Cumulative spend, cumulative purchases, cumulative purchase value.

**Win threshold (Lane D section 2):**
- **Breakeven CVR at $0.15 CPC = 1.39%** (formula: max CPC / target CPA = $0.15 / $10.77).
- **Win:** CVR `>= 1.39%` over the 7d window with cumulative clicks `>= 50` (sample-size floor for credible CVR). Equivalently, CPA `<= $10.77` with conversions `>= 1`.
- **Stronger win:** ROAS `>= 6.5x` (i.e. matches the 650% target).

**Hold-and-observe threshold:**
- Cumulative spend `< $8` and conversions `= 0`: extend the window. Do not draw CVR conclusions on undersampled data per Lane D section 5.
- Cumulative clicks `< 50`: extend the window even if spend has crossed `$8`.

**Kill thresholds at T+7d** (same as T+72h table above): if `>= $16` cumulative spend with 0 purchases at any point during the 7d window, hard pause has already engaged; if `>= $24` cumulative ad-group spend with 0 purchases, kill the ad group.

**Mid-band (between win and kill):**
- CVR `< 1.39%` but `> 0%` AND cumulative spend `< $16`: continue observing through day 14. Do not scale. Document the partial signal.

### 4d. Post-7d scaling vs expansion (only if win threshold met)

If T+7d shows CVR `>= 1.39%` AND ROAS trending toward `6.5x` AND cumulative clicks `>= 50` AND cumulative purchases `>= 1`:

- **Do not auto-scale.** Hold budget and bid for another 7 days to confirm the signal is not noise.
- After day 14, if the signal holds, propose to the owner one of:
  - **Vertical scale option A:** raise GB ad-group budget allocation (still within `$2/day` campaign budget, just remove starvation pressure on the active ad group). Requires fresh owner approval phrase.
  - **Vertical scale option B:** raise GB campaign daily budget from `$2` to `$4` (max). Requires fresh owner approval phrase.
  - **Horizontal expansion option C:** enable a second GB ad group from the same paused campaign (the next-tier exact-only group). Requires fresh owner approval phrase.
  - **Cross-market expansion option D:** enable `CA` paused campaign `23834423669` at `$2/day`, ad group `Mommy & Me Dresses - Exact`, identical guardrails. Requires fresh owner approval phrase.

The default first escalation is option C if GB looks healthy but starved (low impressions), or option D if GB is at full delivery and CVR is solid.

---

## 5. Rollback procedure

If any kill threshold trips, or any guardrail is breached, execute the following in order. **Pause, do not delete.** Deletion destroys learning history.

### 5a. Pause the offending unit

| Trigger | Action |
|---|---|
| `>= $16` cumulative spend, 0 purchases | Pause ad group `Mommy & Me Dresses - Exact` (toggle Enabled -> Paused). Leave campaign Enabled with no other ad group enabled. This effectively halts spend without destroying the campaign shell. |
| `>= $24` cumulative ad-group spend, 0 purchases | Same pause action, plus: do not reuse this ad group's exact configuration. Mark it for restructure. |
| Non-GB clicks appear | Pause ad group immediately. Do not pause campaign. |
| Policy/disapproval on creative | Pause the disapproved RSA; if it is the only RSA, pause the ad group. |
| Standard Shopping or Brand Search regresses | Pause the GB ad group anyway (defensive isolation), then route to parent for the unrelated regression. |
| Owner says stop | Pause the ad group; if the owner says fully stop, pause the campaign. |
| Presence-only targeting regression | Pause the ad group, capture the Locations panel screenshot, route to parent. |

### 5b. Capture rollback evidence

Save under:

```
dresslikemommy-growth-2026/02_AUDIT_PACKETS/<YYYY-MM-DD>-google-ads-non-us-first-enable-gb/rollback/
  trigger_summary.txt
  metrics_at_rollback.json
  campaign_overview_at_rollback.png
  adgroup_overview_at_rollback.png
  rpc_at_rollback.json
  pause_action_pre.png
  pause_action_post.png
```

`trigger_summary.txt` must state: which trigger fired, cumulative spend, cumulative purchases, cumulative clicks, and the exact timestamp of the pause click.

### 5c. Open a problem-tracker entry

Append a new row to `ops/PROBLEM_TRACKER.md` with id pattern `PROB-<YYYY-MM-DD>-GB-FIRST-ENABLE-<SHORT-REASON>`, severity `P1` if non-GB traffic or policy violation, otherwise `P2`. State:

- Trigger that fired.
- Cumulative spend / clicks / purchases at trigger.
- Pause action timestamp.
- Pointer to `rollback/` evidence directory.
- Whether GB ad group is restructure-eligible or kill-only.

### 5d. Worklog anchor

Append to bottom of `ops/AGENT_WORKLOG.md`:

```
<YYYY-MM-DD> - Google Ads non-US first-enable GB rollback
AGENT_CONTINUITY_ANCHOR: <YYYY-MM-DD>-google-ads-non-us-first-enable-gb-rollback

Why:
- <one-line trigger description>

What changed:
- Paused ad group "Mommy & Me Dresses - Exact" in campaign 23838895360 ...

Evidence:
- dresslikemommy-growth-2026/02_AUDIT_PACKETS/<YYYY-MM-DD>-google-ads-non-us-first-enable-gb/rollback/

Guardrails:
- No other campaign, budget, bid, conversion-goal, or product-scope changes.

Next:
- Owner decision: restructure / kill / re-enable after fix.
```

### 5e. Owner notification template

Send to owner in chat:

```
GB first-enable hard pause triggered.

Trigger: <warning / hard pause / kill> at $<X> cumulative spend with <N> purchases (CVR <Y>% over <C> clicks).
Action taken: paused ad group "Mommy & Me Dresses - Exact" in campaign 23838895360 at <ISO timestamp>.
Campaign status: Enabled (shell only, all ad groups paused).
Spend stopped: yes.
Standard Shopping: <unchanged / regressed - see PROB-...>
Brand Search: <unchanged / regressed - see PROB-...>
US campaign 23827590655: unchanged.

Evidence: dresslikemommy-growth-2026/02_AUDIT_PACKETS/<YYYY-MM-DD>-google-ads-non-us-first-enable-gb/rollback/
Problem tracker: PROB-<YYYY-MM-DD>-GB-FIRST-ENABLE-<SHORT-REASON>

Awaiting your decision: (a) restructure ad group and re-enable, (b) kill ad group permanently, (c) move on to CA, (d) full stop on non-US Search.
```

---

## 6. Forward path after first GB enable

If GB clears the 7-day review with **CVR >= 1.39%** and at least 1 purchase and cumulative clicks >= 50, the next escalation steps in priority order are:

### 6a. Confirm-the-signal hold (days 7-14)

Hold GB at `$2/day`, max CPC `$0.15`, single ad group enabled, for 7 more days. Watch for CVR collapse. If CVR holds at `>= 1.39%` and CPA holds at `<= $10.77` (Lane D section 2 target CPA = AOV / target ROAS = $70 / 6.5 = $10.77), the signal is real.

### 6b. Trigger to expand the GB ad-group set

If during the days 7-14 hold the GB campaign is **delivery-starved** (impression share lost to bid `> 50%` or fewer than 5 clicks/day), enable a second exact-only ad group from the same paused GB campaign. This adds query coverage without raising bid or budget, and tests whether the CVR generalizes to a second product theme. Requires fresh owner approval phrase modeled on section 2 with `Mommy & Me Dresses - Exact` swapped for the next ad group name.

### 6c. Trigger to expand budget on GB

If during the days 7-14 hold the GB campaign is **demand-starved** (impression share lost to budget `> 30%`, average daily spend `>= $1.80`, CVR `>= 1.39%`), raise GB daily budget from `$2` to `$4`. Hold max CPC at `$0.15`. Requires fresh owner approval phrase. Per Lane D, the breakeven CVR does not change with budget; budget only changes the rate of learning.

### 6d. Trigger to escalate to CA

CA is the next country in the staged enablement order (`MARKET_ACTIVATION_SCORECARD.md` section "Staged enablement order"). Trigger CA enable when **all** of:
- GB has held CVR `>= 1.39%` and CPA `<= $10.77` for at least 14 cumulative days post-enable.
- GB Standard Shopping and Brand Search remain in non-regressed state.
- GB has produced at least 3 GB purchases (sample-size floor for "the goal/landing/checkout chain works in a non-US market").
- Beach-SEO mitigation (`PROB-2026-05-08-BEACH-OUTFIT-SEO-TITLE-MISMATCH`) is still intact.

CA enable uses the same runbook structure with campaign id `23834423669`, same `Mommy & Me Dresses - Exact` ad group, `$2/day`, `$0.15` max CPC. New owner approval phrase required.

### 6e. Trigger to escalate to AU

AU is the third tier-1 English market. Trigger AU enable when **all** of:
- CA has cleared its own 7-day review with CVR `>= 1.39%`.
- GB is still healthy.
- AU presence-only targeting and `en-AU` checkout-to-shipping QA are still passing.

AU enable: campaign id `23834424182`, same ad group, `$2/day`, `$0.15` max CPC. New owner approval phrase required.

### 6f. Tier-2 (ES / IT / RO / PT) gate

**Do not** escalate to ES (`23829133584`), or to IT/RO/PT once their paused builds exist, until `PROB-2026-05-09-NON-US-SEARCH-NATIVE-LANGUAGE-COPY-GATE` clears with native-speaker review. Tier-2 markets cannot be enabled on tier-1 evidence alone.

### 6g. PMax and Standard Shopping interactions

PMax and any expansion of Standard Shopping remain out of scope for this runbook. Per `ops/GOOGLE_ADS_CONTINUITY.md`, PMax is blocked on multiple structural gates. Standard Shopping changes require a fresh, separate owner approval phrase. Do not let GB Search wins justify PMax enable.

---

## 7. Decision tree summary

```
Pre-enable gate checklist (section 1)
|
+-- ANY item 1-12 fails ----------> ABORT. Route to parent. Do not click Enable.
|
+-- ALL items 1-12 pass
        |
        v
   Owner pastes verbatim approval phrase (section 2)
        |
        +-- phrase altered or missing ---> ABORT. Re-request.
        |
        +-- phrase exact
                |
                v
           Apply-time runbook (section 3): pre-RPC -> enable ad group -> enable campaign -> post-RPC
                |
                +-- post-RPC delta != exactly +1 ad group / +1 campaign ---> ROLLBACK (section 5).
                |
                +-- delta clean
                        |
                        v
                   T+24h check
                        |
                        +-- non-GB clicks / policy flag / status flip ---> ROLLBACK (section 5).
                        +-- impressions = 0 ---> "starvation watch", continue.
                        +-- clean ---> continue to T+72h.
                                |
                                v
                           T+72h check
                                |
                                +-- spend >= $16, 0 purchases ---> HARD PAUSE (section 5a row 2).
                                +-- spend >= $8, 0 purchases ---> WARNING. No bid/budget change. Continue.
                                +-- on-pace, < $8 spend ---> continue to T+7d.
                                        |
                                        v
                                   T+7d check
                                        |
                                        +-- spend >= $24, 0 purchases ---> KILL AD GROUP (section 5a row 2 plus restructure flag).
                                        +-- spend >= $16, 0 purchases ---> HARD PAUSE (section 5a row 2).
                                        +-- clicks < 50 OR spend < $8 ---> HOLD-AND-OBSERVE. Extend window.
                                        +-- CVR < 1.39%, > 0%, spend < $16 ---> HOLD-AND-OBSERVE. Continue to day 14.
                                        +-- CVR >= 1.39% AND clicks >= 50 AND >= 1 purchase ---> WIN.
                                                |
                                                v
                                           Days 7-14 confirm-the-signal hold (section 6a)
                                                |
                                                +-- signal collapses ---> downgrade to HOLD-AND-OBSERVE or HARD PAUSE per spend.
                                                +-- signal holds ---> SCALE / EXPAND (section 6b/6c) or CROSS-MARKET (section 6d/6e).
                                                          (Each scale/expand step requires a fresh verbatim owner approval phrase.)
```

---

## 8. Guardrails preserved by this runbook

- This runbook is local file write only. No live writes, no browser actions, no network requests, no theme edits, no Shopify/Merchant/Pinterest/GA4/Google Ads writes were performed by this lane.
- This runbook does NOT make the live enable decision and does NOT execute it.
- All economics math (target CPA $10.77, breakeven CVR 1.39% at $0.15 CPC, $8 warning / $16 hard pause / $24 kill) traces to `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-safe-resume/lanes/roas-economics/ROAS_ECONOMICS_REFRESH.md` sections 2 and 3.
- All market-readiness facts (campaign id `23838895360`, GB checkout-to-shipping PASS, presence-only, `$2/day`, smallest-future-spend-unit recommendation `GB / Mommy & Me Dresses - Exact`) trace to `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-safe-resume/lanes/market-activation/MARKET_ACTIVATION_SCORECARD.md`.
- No US campaign `23827590655`, PMax, Standard Shopping, Brand Search, Merchant, Shopify product-data, Pinterest, theme, product-scope, feed-label, product-group, conversion-goal, budget/bid/status-enable, or product/feed/conversion change is contemplated by this runbook.
- Forward dependencies on Lane A (`ads-apply-playbook`) and Lane B (`measurement-conversion-gap`) are flagged in section 1 with explicit reconciliation requirements.

---

## 9. Files touched

WRITTEN by this subagent (lane report only):
- `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-deep-followup/lanes/first-enable-runbook/FIRST_ENABLE_RUNBOOK_REPORT.md`

READ by this subagent (no modifications):
- `ops/GROWTH_NORTH_STAR.md`
- `ops/GOOGLE_ADS_CONTINUITY.md`
- `ops/AGENT_WORKLOG.md` (anchor lookup only)
- `ops/AGENT_COORDINATION.md` (claim status only)
- `ops/prompts/paid-growth-ai-army-continuation-prompt.md` (canonical approval-phrase format)
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-safe-resume/lanes/roas-economics/ROAS_ECONOMICS_REFRESH.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-safe-resume/lanes/market-activation/MARKET_ACTIVATION_SCORECARD.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-safe-resume/lanes/ads-resume-order/ADS_RESUME_ORDER_REPORT.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-safe-resume/lanes/beach-seo-gate/BEACH_SEO_GATE_REPORT.md`
