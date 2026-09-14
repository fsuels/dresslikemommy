# Independent Google Ads signup tag review

Reviewed: 2026-09-11, 18:15:52 UTC; initial review 17:56 UTC. Reviewer: `tag_repair_review`; root owns live execution and canonical integration.

Current verdict: `PASS_WITH_LIMITS`; the final resolution below closes the material wording and evidence-time findings. Confidence: medium because this reviewer has assessed root-supplied native evidence and has not independently accessed authenticated UI or verified runtime behavior. Genuine purchase and consent acceptance remain open. The review uses public primary documentation, the current user request, repository control, and root-supplied readbacks.

## Supported method and rejected alternative

Google documents manually adding a Google tag through the existing Google & YouTube app without connecting its account. Custom event destinations use the exact `AW-CONVERSION_ID/CONVERSION_LABEL` from the conversion snippet. Linking Ads can create conversion actions and account defaults, so a direct link is a materially broader alternative here. [Google's Shopify tagging guide](https://support.google.com/google-ads/answer/16030792?hl=en).

Combining tags shares configuration and users across connected destinations. It can change on-page behavior and cannot be directly undone; reassigning IDs is a separate reconstruction operation. The signup merge warning therefore represents substantive changes, rather than an installation acknowledgement. Keep the separate-tag path. [Google tag management](https://support.google.com/tagmanager/answer/12329709).

Both sources checked 2026-09-11. No publication or update date was visible in the retrieved text.

## Evidence and uncertainty

- `ROOT_REPORTED_LIVE`: exact Ads customer `650-997-2886`, URL `ocid8520129103`, DLM tag container `263891119`, `AW-18433316477`. Existing GA4 `G-N4EQNK0MMB` / `GT-PJ5D7RB` lists one GA4 destination. The guided merge was not confirmed; current Ads tag installation test failed.
- `ROOT_REPORTED_LIVE`: Shopify store `dresslikemommy-com`; the app lists Merchant `GT-T5R7JFVL` and manually added `G-N4EQNK0MMB`, with no current AW tag. Merchant and Business Profile are connected; Ads is unlinked. Conversion measurement is On, but all seven editable event destinations show a dash. No save was made.
- `HISTORICAL_ONLY`: September 9 migration evidence records disconnected duplicate GA4 pixel `111181921`, preserved Ads pixel `111214689`, and unresolved genuine-purchase receiver acceptance. The legacy Ads pixel needs a fresh destination match.
- `REPO_KNOWN`: exact signup claim is read-only diagnosis; global paid authority remains `NONE` / `STALE_READBACK_REQUIRED`. This review neither changes those controls nor supplies live execution authority.

## Preflight required before Save

1. Match the legacy Ads pixel's current `config` and `send_to` AW IDs/labels and event triggers. App tag absence alone does not exclude a duplicate external sender.
2. Reconfirm the current account's tag ID and review inherited app/tag consent, enhanced conversions, and user-provided-data settings. A retained switch can apply to a newly added destination. Do not assume manual addition avoids new identifier sharing.
3. Snapshot the tag list, seven event mappings, relevant data-sharing settings, and exact change. Root must reconcile its own claim to the current user's narrow tracking-repair authority before execution.
4. For purchase mapping, independently read the existing action's AW/label, Purchase category, event trigger, value/currency configuration, and present primary/default role. Missing or ambiguous label: base-tag repair only, with purchase mapping blocked. Do not guess a label, create a surrogate purchase, or repurpose a page-view action.
5. Verify that installation acknowledgement will not activate a pending campaign. Launch, spend, billing, tag merge/user grants, account linking, new enhanced conversions/customer-data transfer, and changed conversion goals require their own exact current authorization.

The user's instruction to fix the specified tag setup reasonably authorizes the smallest supported installation and exact existing purchase mapping, once these prerequisites pass. This is a scope interpretation, not a waiver of the pasted brief's restriction on consequential live changes or customer-data transfer. Unexpected additional effects require a concrete approval decision before that action.

## Acceptance and rollback

- Reload app settings: exact new AW appears once; pre-existing tags, destinations, consent settings and pixel states match the snapshot. Rollback removes only the newly added tag/mapping and restores exact prior values; never reconnect the disconnected GA4 sender as a generic rollback.
- Retest the exact Ads tag and inspect consent-aware browser dispatch. A found tag proves installation only; one page view does not prove purchase delivery or receiver ingestion.
- For the next genuine purchase, reconcile transaction ID, value, currency and items to the intended Ads action/receiver and GA4; check duplicate dispatch and counting separately. Do not generate artificial production purchases or click live ads to manufacture proof.
- Any completed installation remains `IMPLEMENTED` / narrowly `VERIFIED` only for its actual checks. Purchase acceptance, campaign delivery, and profitability retain separate statuses.

Parent-owned next action: freshly identify legacy pixel `111214689` and the current Purchase action before saving, because those identities determine both duplicate risk and the smallest safe repair.

## Live campaign discovery and exact pause proposal

Root reports a fresh read at approximately 17:54 UTC (corrected from its initially supplied approximate time), in the same account `650-997-2886`: exactly one table row, `Campaign #1`, campaign `24247604341`, Performance Max, Enabled, Eligible (Learning), budget `$5.00/day`. The visible September 6–11 Eastern reporting window showed zero impressions, clicks, conversions and spend. Its conversion action was unverified. Root made no status or budget change. These are parent-supplied observations, not independent runtime verification or a guarantee that no costs can subsequently appear.

Pause review verdict: `PASS_TO_REQUEST_EXACT_PAUSE`; execution is `PENDING_EXPLICIT_USER_APPROVAL`. The proposed change is only Enabled → Paused for campaign `24247604341`. It preserves budget, bids, assets, goals and all other campaigns/settings. Pausing is proportionate because an enabled campaign can begin serving while its purchase measurement is unresolved; the current general request does not establish exact campaign-status authority.

Immediately before an approved Save, root must freshly confirm the account, campaign ID, current status and `$5.00/day` budget against the before-state. Reload after Save and record Paused with unchanged budget and other settings. An unexpected conflicting edit or activation/budget dialog stops the action. Do not delete, archive, pause account-wide, or automatically re-enable as rollback; resuming spend needs exact authority.

This discovery supersedes the next-action ordering above: first obtain the owner's decision on this single reversible pause, while independently completing the legacy sender and Purchase-label reads. No installation result should be presented as launch or spending approval.

## 17:58 UTC resolution: exact two-write repair

New root-supplied current evidence resolves the identified legacy-sender and Purchase-action gaps:

- Shopify custom pixel `111214689` remains connected (its editor offers Disconnect). Current constants are `AW_CONVERSION_ID="AW-853411529"` and `AW_CONVERSION_LABEL="kZ_RCN-T3K0cEMmN-JYD"`. It is a different destination from the requested new tag and must remain unchanged. This resolves the identified same-destination collision risk; it does not prove all runtime purchase dispatches are deduplicated.
- At 17:56–17:57 UTC, Ads action `7760272273`, created September 11, was Purchases / Primary / Website, counted Every conversion, using dynamic values with a `$1` fallback. Account-default Purchase has exactly one primary action and is used by one of one campaigns. Enhanced Conversions is Not configured. The existing manual event snippet exposes `AW-18433316477/DTaoCJG3sfQcEP2s2NVE`.
- Root has not changed click triggers, installed code, changed goals, linked an account, or changed campaign status/budget. The existing app still lists only GA4 and Merchant tags, with seven blank Ads event destinations.

Cleared scope under the user's current request to fix this exact setup, subject to each fresh form matching only the stated change:

| Write | Exact change | Required immediate readback |
|---|---|---|
| 1 | Add `AW-18433316477` to the existing Google & YouTube app's manually added Google tags | Reload confirms that AW once, with `G-N4EQNK0MMB` and `GT-T5R7JFVL` preserved |
| 2 | Map only Shopify Checkout completed to existing `AW-18433316477/DTaoCJG3sfQcEP2s2NVE` | Reload confirms that exact mapping and the other six event destinations still blank |

Use the supported app's dynamic order payload; do not insert a fixed `$1` purchase value or invent a new conversion action. Preserve all existing account/action settings and connected pixels. The target action's EC status is Not configured; confirm no form introduces enhanced-conversion consent, new user grants, identifier-sharing selection, tag merge, direct Ads link, account-default changes, or campaign activation. An unexpected additional effect is outside this clearance and stops that Save.

No further user confirmation is needed for these two bounded measurement repairs when these conditions hold. Root must record the exact scope in its own claim; full paid authority remains unchanged. The campaign pause remains `PENDING_EXPLICIT_USER_APPROVAL`, independent of the authorized repair; do not imply that the unanswered pause request grants or blocks tag-installation authority.

After both app readbacks, run the existing exact Ads installation detector and consent-aware storefront check. Report the literal results separately. Genuine purchase event payload, receiver acceptance, duplicate counting, campaign performance and profit remain unverified until their own evidence exists. Root may continue these two app changes while the pause question remains pending.

## 18:12 UTC after-execution review and strategy challenge

`PASS_WITH_LIMITS_FOR_IMPLEMENTED_CONFIGURATION`: reviewed `execution_receipt.json` and the updated `READBACK.md`. Both explicitly derive from root-observed native Chrome UI and a manual redacted transcription. The executor performed full reloads; this reviewer did not build, execute, or replay the native flow. Sixteen independent contract/receipt consistency checks passed for identity, exact tag addition/multiplicity, purchase destination/action, preservation assertions, pending pause, and absence of campaign/payment/ad-click actions. These are consistency checks on the receipt, not independent runtime tests.

The recorded app after-state contains `GT-T5R7JFVL`, `G-N4EQNK0MMB`, and `AW-18433316477` once each; only Checkout completed maps to `AW-18433316477/DTaoCJG3sfQcEP2s2NVE`, with six other mappings blank and measurement On. The approximately 18:06 UTC Google detector reported successful tag detection. Root then cleared an unsaved, preselected enhanced-conversions option before continuing to Overview; the receipt does not show an EC activation. A fresh final Purchase settings read should retain the exact post-completion EC status if claiming that specific setting is unchanged.

The receipt's final campaign read remains Enabled / `$5.00/day`, with serving status now Pending — All asset groups under review. Zero report metrics retain their September 6–11 window; the earlier Eligible (Learning) wording is historical. The exact pause question remains unanswered. No pause or spending permission is inferred from the repair or onboarding completion.

Purchase receiver verification, dynamic value/currency/items, transaction deduplication, new-destination consent transitions and paid attribution remain `NOT_VERIFIED_HERE`. No purchase or payment was performed. An organic purchase can establish collection/dispatch evidence; counted paid attribution needs its own genuine qualifying interaction. Do not claim that no customer-data transmission occurred from the absence of EC activation alone: Google's app reference includes conditional user-data fields. [Shopify event parameters](https://developers.google.com/tag-platform/gtagjs/reference/shopify-event-parameters), checked September 11; page updated July 28, 2026.

Bounded launch/economics challenge:

- **PASS for hypothetical arithmetic:** ten independent calculations reproduce revenue `$64`, variable cost `$37`, contribution `$27`, margin `42.19%`, target CAC `$17`, business ROAS `2.37x`/`3.76x`, platform ROAS `2.67x`/`4.24x`, and `$1,000` contribution for the hypothetical 100-customer cohort. These establish no actual store costs or profitability.
- **PASS for value-basis distinction:** the primary app reference confirms discounted purchase value excluding shipping/taxes and the stated April 24, 2025 change. [Google app reference](https://developers.google.com/tag-platform/gtagjs/reference/shopify-event-parameters). The strategy correctly avoids treating a 650% ambition as a justified current bid target.
- **PASS for spending-limit caution:** current primary documentation supports the stated general 2x daily/30.4x monthly mechanics, subject to budget changes and mid-month starts. A configured budget is not current user authority, and a daily average is not a strict same-day cap. [Google spending limits](https://support.google.com/google-ads/answer/10486637?hl=en-IE), checked September 11; no visible update date.
- **Material wording correction:** strategy step 5 combines consent and enhanced conversions under Requirement. State clearly that EC is optional, remains unconfigured unless separately authorized, and is not a mandatory enablement step. The direct EC introduction-page fetch returned HTTP 429; no retry or claim of source verification from that failed request was made.
- **Material scope correction:** strategy step 4 should make any competing-GA4-action downgrade conditional on fresh duplicate evidence and exact authorization. This account currently has one primary Purchase; the executed repair did not authorize conversion-goal edits.
- **Continuity corrections:** replace the strategy's stale incomplete-repair statement and competing continuation prompt. In `READBACK.md`, distinguish root reloads from an independent native replay. At the review's 18:10:55 UTC read, the reported evidence interval ended at 18:13 UTC, which was still in the future; use the last actual observed time.

No material numerical error or case for an immediate additional campaign was found in this bounded review. Actual retained contribution, supplier/return costs, market/cohort choice, campaign exposure authority, and genuine purchase acceptance remain decision gates. The novel-feature source register was not independently re-audited in full by this reviewer.

Final reviewer outcome at this checkpoint: the exact measurement configuration is supported by coherent root live receipts; launch/scale remains unapproved. Parent should resolve the wording/time corrections above, preserve the open runtime gates, and obtain the pending single-campaign pause decision. The reviewer modified only this independent review artifact.

## Final resolution — 18:15:52 UTC

Final verdict: `PASS_WITH_LIMITS`. Re-read the corrected packet and root's supplied after-state delta. The earlier material corrections are `RESOLVED`: optional EC is explicit; duplicate-goal changes require fresh evidence and exact authorization; completed installation replaces the stale in-progress statement; the continuation points to the canonical prompt; root after-state readbacks are accurately named; and the evidence interval ends at the actual 18:11 UTC checkpoint. The updated execution receipt records a fresh post-completion Purchase-action reload retaining Primary, Every, dynamic values with USD1 fallback, and Enhanced Conversions Not configured.

The restored strategy constraints match the current cockpit's 30% all-in profit target, USD0.15 CPC ceiling, and stricter ROAS/contribution objectives. Independently recomputed `min(R/6.5, CM − H − 0.30R)` for the explicitly hypothetical R=64, CM=27, H=0: allowed ads are `$7.80`; business ROAS is `8.21x` and platform ROAS `9.23x` using its separate `$72` value basis. Positive overhead reduces the allowance, zero/negative allowances are unqualified, and unknown cost inputs remain blocking. The generic `$17` illustration is explicitly identified as failing the project's 30% target.

Conditional Manual CPC Search preparation and qualified Shopping as an alternative are defensible under those constraints. The file does not treat the current PMax as having a verified hard CPC cap or authorize its continued exposure. Manual CPC controls still need exact account inspection: Google's documentation identifies features and bid adjustments that can raise a maximum bid, supporting the strategy's modifier check. [Manual CPC bidding](https://support.google.com/google-ads/answer/2390250?hl=en), independently checked September 11; no visible update date. No auction feasibility or profitable acquisition result has been established.

Final delta validation: eleven corrected-packet checks and eight constraint arithmetic/edge-case checks passed. Earlier sixteen receipt/contract comparisons and ten generic hypothetical calculations retain their separate scope. No shared generator, canonical file, native session, or live account was changed by this reviewer.

No material unresolved issue was found in the reviewed deltas. Limits remain: operator-transcribed native evidence rather than independent runtime replay; genuine purchase payload/receiver/deduplication and consent transitions unverified; actual economics and paid attribution unknown; campaign pause awaiting the owner. The one owner action remains the pending exact temporary-pause decision for campaign `24247604341`. This final review does not authorize pause, launch, spend, goal changes, or scale.
