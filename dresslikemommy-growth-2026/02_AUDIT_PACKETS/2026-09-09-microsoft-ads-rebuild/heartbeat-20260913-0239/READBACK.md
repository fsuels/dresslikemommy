# Microsoft keyword qualification — September 13, 2026

Confidence: M. Native inputs, identities and downloads are verified; traffic and profitability are estimates or unknown.

TA-15; account477439/customer770182; sole Microsoft operator root01a08703. This continuation tested the six existing paused keywords and eight reserve terms from the existing local library. It did not repeat completed campaign imports, consent tests, ad-asset checks, delivery tooltips or order reads.

**Result: the retained USD0.15 ceiling is not yet supported as a useful traffic plan.** The isolated US saved-keyword scenario displays zero weekly clicks and one impression. Germany displays zeros. The four US reserve terms have a small fractional forecast signal: the native Clicks chart shows0.10 weekly clicks at a0.15 bid, while the table and CSV round clicks to0. The German reserves provide no positive finite click count in the export. None of these results establishes conversion rate, CPA, ROAS or profit, and unavailable data is not proof of zero demand.

| Isolated forecast | Terms | Daily modelling input | Displayed weekly clicks | Displayed weekly impressions | Displayed weekly spend |
| --- | ---: | ---: | --- | --- | --- |
| Existing US terms | 3 Exact | USD5 | 0 | 1 | USD0.00 |
| Existing German terms | 3 Exact | USD3 | 0 | 0 | USD0.00 |
| US reserve terms | 4 Exact variants | USD5 | 0; chart0.10 | 1; summary range1–2 | USD0.01; summary range0.01–0.02 |
| German reserve terms | 4 Exact variants | USD3 | 0 | 0 | USD0.00 |

All four runs used USD0.15, the respective single country, Microsoft sites and select traffic, and the seven corresponding saved negatives supplied in quoted syntax. The native planner showed **All languages**; it did not expose a language editor or a presence-only setting in these forms. These are qualified country/keyword planning scenarios, not an exact recreation of the campaigns' English/German, presence-only, Maximize Clicks configuration. The network label also does not certify Audience exclusion.

The native exports explicitly confirm Exact for every row in the four final forecasts. Plain input initially defaulted to Broad. A subsequent bracketed query appended Exact rows rather than replacing the Broad rows. Those two diagnostic exports are preserved, excluded from the final comparison, and the temporary Broad rows were removed from the planner before the isolated US run. The saved six live-account keywords were already Exact and were not changed.

The exports preserve Microsoft's literal dash and NaN/NaN% values. Most click/spend fields export as dashes even where the grid displays0. No missing value was converted to measured zero; no average CPC was calculated from rounded totals. The US reserve's fractional chart point is recorded separately in [native_scenarios.json](native_scenarios.json). The ten source downloads and their byte counts, timestamps, row counts and SHA256 hashes are listed in [download_manifest.json](download_manifest.json).

Historical research returned the twelve months September2025–August2026 under Last12months. Monthly ranges are historical keyword demand, not Exact-match forecasts. The main useful comparisons are:

| Country and term | Average monthly range | Competition shown in UI | Suggested bid |
| --- | --- | --- | --- |
| US: mother daughter matching dresses | 100–1K | High | unavailable |
| US: mother daughter dresses that match | 10–100 | unavailable | unavailable |
| US: mommy and me matching dresses | 10–100 | High | unavailable |
| US reserve: mommy and me dresses | 100–1K | High | USD0.50 |
| US reserve: mom and daughter matching dresses | 10–100 | Medium | unavailable |
| DE: mama tochter kleider | 10–100 | unavailable | unavailable |
| DE reserve: kleider für mutter und tochter | 10–100 | Medium | unavailable |

The other seven of fourteen researched terms have unavailable average monthly volume. The four history CSVs retain all fourteen terms and each month's returned range. The0.50 suggested bid is an estimate derived from advertising data, not an actual CPC, a guaranteed auction-entry price or an approved bid increase. [Microsoft's statistics documentation](https://github.com/MicrosoftDocs/Advertising/blob/main/advertising/msa-help/hlp_BA_CONC_KeywordPlanner_StatisticsTrafficEstimates.md) distinguishes historical demand, weekly forecasts and maximum versus average CPC. The [CampaignEstimator reference](https://learn.microsoft.com/en-us/advertising/ad-insight-service/campaignestimator?view=bingads-13) also states that forecasts are not specific to an existing campaign.

The eight reserve strings came from [the existing keyword library](../keywords.csv): US lines5–8 and DE lines61–64. Four source rows were Phrase; all eight were modelled as Exact variants for this comparison. Their original library rows still use broader mommy-and-me collection URLs. They must not be blindly imported; the intended reviewed destinations are the English/German dresses collections. The source library itself was not edited.

**Decision: HOLD_WITH_EVIDENCE_NO_CAMPAIGN_CHANGE.** Adding the eight terms or raising a bid simply to produce activity is not justified by these results. US mommy and me dresses / mom and daughter matching dresses and DE kleider für mutter und tochter remain demand-supported hypotheses for later qualification, not approved campaign additions. Continue the supported consent repair on the already-pending contact answer or a supported publisher change, then genuine purchase acceptance. Actual contribution and exact numeric paid authority are still required for a paid experiment. No new owner question was raised; the parent's existing theme-publication owner action is unchanged.

Execution boundary: eleven **planner-only** Save clicks changed research filters or temporary keyword groups; four planner Delete clicks cleared completed/probe rows; ten native CSV exports were downloaded. There were zero Save to my account clicks, campaign/account/conversion Saves, imports, enablements, support messages, generated tracking events, staged purchases, or order queries. These research CSVs retain Draft Campaign labels and are **not import files**. The task-owned tab7 remains on the four-term German reserve estimate, no dialog open, marked for handoff.

Interaction limits: one unsupported waitForEvent method returned before Export ran; normal native Export clicks then produced the downloaded files. One stale checkbox reference failed after two checkboxes had succeeded; a fresh readback identified those selections, and only the third intended Broad checkbox was then selected. One named-table DOM extraction returned an empty list, so native AX and downloaded CSV evidence were used. Neither issue changed a saved campaign or account setting. In-flight and retained cross-view results were excluded until fresh keyword identities and completed loading were observed.

source_live_evidence_as_of: 2026-09-13
live_state_mode: STALE_READBACK_REQUIRED
effective_approval_policy: FRESH_ACTION_TIME_APPROVAL_REQUIRED
approved_external_scope: NONE
current_exact_nonspend_scope: Existing Microsoft tracking repair and qualified paused USEN/DEDE preparation; planner-only research in this wake.
decision_depends_on_uncertain_state: true
decision_changing_evidence: Supported consent repair/contact answer; genuine purchase acceptance; actual contribution and exact paid authority; materially different qualified forecast or measured serving evidence.
if_evidence_supports_recommendation: Retain the hold and prepare only the next qualified bounded action.
if_evidence_opposes_recommendation: Re-evaluate the specific premise from new evidence, without an automatic bid raise or import.
material_decision: No new paid or production action proposed; significant qualification finding submitted for independent review.
independent_verifier: PASS_WITH_LIMITS; [paused_import_verifier review](review/qualification_review.json) passed35 checks of frozen sources and interpretation; no independent live replay claimed. Root packet validation passed30 checks. Only this completion field changed after the frozen review.

Continue through the [canonical paid-growth prompt](../../../../ops/prompts/paid-growth-ai-army-continuation-prompt.md), current TA-15 and the existing consent-support packet. This evidence does not create a competing queue or change authority.
