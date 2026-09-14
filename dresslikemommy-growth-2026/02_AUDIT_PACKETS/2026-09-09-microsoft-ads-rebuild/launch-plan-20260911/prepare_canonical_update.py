"""Prepare guarded Microsoft-only local continuity edits; does not apply them."""
from pathlib import Path
import hashlib, json, re
HERE = Path(__file__).resolve().parent
PACKET = HERE.parent
REPO = PACKET.parents[2]
ANCHOR = '2026-09-11-microsoft-launch-plan-reconciled'
PREFIX = 'dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-09-microsoft-ads-rebuild'
changes = []
def replace(path, old, new):
    current = (REPO/path).read_text()
    assert current.count(old) == 1, (path, current.count(old), old[:70])
    changes.append({'path':path,'old':old,'new':new})
def add_before(path, marker, content):
    replace(path, marker, content+'\n\n'+marker)
def append(path, content):
    current=(REPO/path).read_text()
    assert ANCHOR not in current
    changes.append({'path':path,'old':'','new':'\n\n'+content.rstrip()+'\n','append':True})
def replace_row(path, key, new):
    rows=[s for s in (REPO/path).read_text().splitlines() if s.startswith('|') and key in s]
    assert len(rows)==1, (path,len(rows))
    replace(path,rows[0],new)

checkpoint="""## September 11 Microsoft launch-plan reconciliation

TA-15; anchor `2026-09-11-microsoft-launch-plan-reconciled`. Owner supplied the September10 launch research. September11 read-only Shopify queries verify21published locales/sixACTIVE market groups, Coral9/Sunshine14 configured available variants, and reproduce the fixed August/June12–September9 reports. August net merchandise750.66USD gives112.599USD at15%, a historical all-marketing illustration only; current Microsoft allocation and actual contribution remainUNKNOWN. The older50% cost model is not audited margin. All129country rows reconcile22,294sessions/36completed-checkout sessions; US14,996/21. Session outcomes are not new-customer orders or Microsoft forecasts.

Current local decision prepares one US/en paid experiment, narrow Search as first candidate, Standard Shopping as alternative only after exact approved offers and equivalent economics/measurement/CPC gates. Existing11design/9language library and USEN/DEDE paused-preparation scope remain; the old5+3/day example is historical, not current activation. Local formula is min(0.15R,R/6.67,C-0.30R) with actual disjoint costs; unknown C means unknown allowable CAC. eCPC is not a hard0.15cap. Official Shopify channel English feed is distinct from supported separate localized MMC catalogs;21storefront locales do not imply21feeds. Functional purchase/value/currency/consent/repeat-delivery acceptance is prelaunch; legitimate paid-click attribution is postactivation and required before scale.

No native calls or Microsoft/Shopify external writes this September11 work. Existing selected-Microsoft readiness and checkout-page questions remain pending after earlier automatic review; no repeated question/probe/workaround. Previous Smart163000100 exclusion, Coral21body repair, installed source and campaign CSVs are preserved. Current UX137888792673 owns the successor theme; earlier137881223265 is historical, not a current release target. Receiver mapping, publisher cookie repair, actual costs, fulfillment, current CPC/approved feed and exact cash/loss/launch authority remain open. Evidence:2026-09-09-microsoft-ads-rebuild/launch-plan-20260911/RECONCILIATION.md, launch_contract.json, economics.json, platform_review.md and independent_reconciliation_review.json. Full-paid control and parent OneOwnerAction unchanged."""
add_before('ops/marketing/current_marketing_state.md','## September 9 Microsoft tracking and campaign rebuild',checkpoint)
row="| P0 | YELLOW | `TA-15` Finish Microsoft477439/770182 purchase acceptance and qualified paused preparation | root01a08703 sole Microsoft writer; international_campaign_build independent reconciliation review; UX owns theme | Sept11 Shopify reports/locales/prices reconciled; native receiver/CPC/feed access and actual economics remain open | 2026-09-09-microsoft-ads-rebuild/launch-plan-20260911/RECONCILIATION.md; launch_contract.json; anchor2026-09-11-microsoft-launch-plan-reconciled | Paid traffic | Local launch decision prepared; exact selected-tab access pending | Existing Microsoft477439 selected-tab/inspect-now confirmation; no duplicate request | Preserve Smart exclusion, Coral21body repair and11design/9language library. One US paid experiment proposed; Search first candidate, Shopping alternative. Current allocation/approved offers unknown | After serialized handback inspect UET/goals and current CPC/feed controls; reviewed nonspend repair and qualified USEN/DEDE paused preparation. Functional purchase before launch; genuine paid attribution after launch/before scale. Numeric launch remains gated | 2026-09-11 | Finish Microsoft receiver and cost-control qualification |"
replace_row('ops/marketing/action_queue.md','`TA-15`',row)
claim="| Current owner Microsoft Ads tracking and campaign rebuild | Microsoft477439/customer770182; UET36005151/APP931561569; completed Coral7607764287585 body repair; local campaign/launch reconciliation | `LOCAL_LAUNCH_RECONCILED__MICROSOFT_RECEIVER_AND_STAGE_GATED` | root01a08703 sole Microsoft writer; international_campaign_build independent platform/math review; UX owns successor theme | Saved owner Microsoft nonspend tracking repair and qualified native paused preparation; supplied September10 research authorizes reconciliation, not numeric activation | No paid enablement/billing/security/account creation/switch, fabricated purchase, blind source removal, vendor-code pretend repair or theme publication. Preserve peers and previous sources/campaigns | 2026-09-09-microsoft-ads-rebuild/launch-plan-20260911/RECONCILIATION.md; launch_contract.json; current Shopify read-only receipts | September11 zero native calls/external writes. Existing selected-Microsoft inspection/checkout questions pending after prior automatic review. Fresh21locales/sixmarkets/23variants;129country totals reconcile. One US paid experiment is proposed, Search first candidate/Shopping conditional; existing USEN/DEDE paused preparation and all local designs remain. Actual costs, approved offers, receiver/consent/CPC and cash/loss authority unknown. Anchor2026-09-11-microsoft-launch-plan-reconciled; full-paidNONE and parent owner action preserved |"
replace_row('ops/AGENT_COORDINATION.md','| Current owner Microsoft Ads tracking and campaign rebuild |',claim)
add_before('ops/marketing/operator_cockpit.md','## September 9 Microsoft implementation checkpoint',checkpoint.replace('## September 11 Microsoft launch-plan reconciliation','## September 11 Microsoft decision update'))
add_before('ops/PROBLEM_TRACKER.md','### `PROB-2026-09-06-MICROSOFT-PURCHASE-TRUTH`','''### Microsoft September 11 reconciliation checkpoint

Existing PROB-2026-09-06-MICROSOFT-PURCHASE-TRUTH remains open. Fresh Shopify data and independent official-document review correct the launch proposal: one US experiment; Search first candidate, Shopping conditional on approved offers and effective CPC. eCPC does not enforce0.15; native English feed is separate from localized MMC feeds; actual contribution/remaining budget unknown. Functional purchase acceptance before activation does not require a previous ad click. No new native attempt or external write; earlier exact selected-tab/checkout gates and publisher-managed cookie issue persist. Do not reapply the completed Smart/Coral repairs or treat this local contract as a native import. Anchor2026-09-11-microsoft-launch-plan-reconciled; evidence launch-plan-20260911/RECONCILIATION.md.''')
blocker_path='ops/marketing/blocker_board.md'
first=(REPO/blocker_path).read_text().splitlines()[0]
replace(blocker_path,first+'\n',first+'''\n\n## September 11 Microsoft exact remaining gates

TA-15: local launch plan reconciled against fresh Shopify receipts and current primary documentation; no native/external change. Existing exact selected-account readiness and serialized handback remain needed for account477439. Receiver purchase/value/currency/consent/overlap, supported publisher-cookie correction, actual contribution/fulfillment, current CPC/approved offers and numeric launch cash/loss remain unresolved. One US experiment proposed, Search first candidate and Shopping conditional; international designs and USEN/DEDE paused preparation preserved. Published21locales do not certify Microsoft feeds. The old blanket Mac-lock narrative is historical; no new unlock question/probe. Parent OneOwnerAction and peer gates remain unchanged. Evidence: launch-plan-20260911/RECONCILIATION.md; anchor2026-09-11-microsoft-launch-plan-reconciled.\n''')
append('ops/marketing/daily_scorecard.md',"""## September 11 Microsoft research reconciliation — fixed historical windows

Anchor2026-09-11-microsoft-launch-plan-reconciled. Read-only ShopifyQL at16:47:40UTC, explicitly not today's sales or paid performance: August1–31 orders10/gross887.37/reversals-136.71/net750.66/shipping39.53/total790.19USD. Fifteen percent of net112.599USD is an August all-marketing illustration, not available Microsoft cash. June12–September9 sessions22,294/completed-checkout sessions36/rate0.1614784%; US14,996/21/0.1400373%; all129country rows reconcile. These are session metrics, not deduplicated paid/new-customer orders. Current actual contribution, Microsoft CPA/ROAS/retained profit and remaining allocation UNKNOWN. Six price-based arithmetic scenarios preserve unknown cost cells; no new spend, native call or live write. Prior cohort rows unchanged. Evidence: launch-plan-20260911/analytics_readback.json, economics.json and basket_economics.csv.""")
append('ops/marketing/decision_log.md',"""## DLM-DEC-2026-09-11-MICROSOFT-LAUNCH-RECONCILIATION

Baseline: supplied September10 Shopping-first research plus existing paused-account history, preserved USEN/DEDE local library, September11 Shopify fixed-window reports and23variant configuration. Authority is saved bounded Microsoft nonspend repair/paused preparation; no numeric launch. Decision: prepare one US/en paid experiment; narrow Search first candidate, Standard Shopping alternative only if exact approved cohort and equal economics/measurement/CPC requirements justify it. Compare one small Search test against one exact-offer Shopping test; never activate both just because prepared. Preserve international reserves. Forecast: clearer causal diagnosis and lower avoidable waste than splitting unapproved cash across unqualified markets; no CPC/CPA or sales forecast.

Success: current477439 receiver accepts a permitted functional purchase/value/currency/consent/repeat-delivery check; one intended primary goal; documented effective0.15CPC control, actual positive contribution and exact cash/loss/activation authorization; paused after-state before approved activation. Paid-click attribution follows activation and must pass before scaling. Kill: wrong account/offer/purchase/consent, ineffective cap, unsupported product/fulfillment claims, unknown/nonpositive economics, missing authority or native review rejection. Decision window: next exact-account readback before any native save/activation; recheck October1 strategy rules if applicable. Local-only rollback: restore only recorded replacement segments if superseded; no external change to undo. Independent verifier international_campaign_build did not build root math/contract.

## DLM-OUT-2026-09-11-MICROSOFT-LAUNCH-RECONCILIATION

PREPARED_LOCAL / BUSINESS_OUTCOME_NOT_OBSERVED. Fresh read-only receipts and local calculations resolve the financial-definition/platform-proposal contradictions. Current acquisition/receiver/approved-feed/cost/activation outcome remains gated. No live experiment or measured lift. Evidence launch-plan-20260911/RECONCILIATION.md, launch_contract.json, platform_review.md and independent_reconciliation_review.json. Anchor2026-09-11-microsoft-launch-plan-reconciled. Revisit the prediction after the exact receiver/CPC/offer decision; do not label preparation as profitable sales.""")
append('ops/marketing/review_log.md',"""## September 11 Microsoft launch-plan independent review

Scope: current primary-document claims and root's newly built launch contract/economics, not current account behavior. international_campaign_build owns platform_review.md/json and independent_reconciliation_review.md/json; did not build/execute root analytics/math/contract. Root preserves all existing campaign/source files and full-paid/peer controls. Independent result PASS_LOCAL_RECONCILIATION / HOLD_ACTIVATION: rational-arithmetic replay verifies129country rows,90reporting dates,sixbasket scenarios,eightlocal links andeightpreserved inputs. Exact reviewed hashes live in the receipt. Native receipt, actual cost and activation remain outside this review. Anchor2026-09-11-microsoft-launch-plan-reconciled.""")
append('ops/AGENT_WORKLOG.md',"""## September 11 — Microsoft supplied launch plan reconciled with current Shopify evidence

AGENT_CONTINUITY_ANCHOR: 2026-09-11-microsoft-launch-plan-reconciled

- `task_entities`: TA-15, PROB-2026-09-06-MICROSOFT-PURCHASE-TRUTH, Microsoft477439, Customer770182, UET36005151, APP931561569, DLM-DEC-2026-09-11-MICROSOFT-LAUNCH-RECONCILIATION
- `task_stage`: HANDOFF
- `next_action_id`: READ_ONLY_MARKETING_RECONCILIATION

Owner supplied a September10 launch plan during the existing expert Microsoft repair/campaign task. Root reconciled it against exact read-only ShopifyQL16:47:40UTC and schema-validated Admin16:49:50UTC. Fixed August net750.66 and June12–September9 sessions22,294/36 reconcile, including129country rows. Twenty-one locales/sixACTIVE markets and23Coral/Sunshine variants verified as configuration. Model50% cost is not actual contribution; remaining Microsoft budget staysnull. Local Decimal builder produces six basket scenarios and a non-executable launch contract. No new campaign CSV, native draft, paid activation or source code change.

Independent international_campaign_build checked current platform documentation and root economics/contract. Corrections: eCPC cannot enforce0.15; Shopify native English feed differs from separate localized MMC catalogs; actual AI Max/expansion and futureOctober1 controls must be read back; CAPI transaction ID is not itself browser/server deduplication. Functional purchase proof can precede advertising; paid-click attribution follows approved activation and precedes scaling.

Decision selects narrow USSearch as first preparation candidate, StandardShopping conditional alternative after approved cohort/equal economics/measurement/CPC checks, maximum one initial paid experiment. Preserve11local designs/9languages, USEN/DEDE paused preparation, prior Smart exclusion/Coral repair/source receipts. Existing5+3/day example remains dated proposal, not current activation. No native calls, Microsoft/Shopify writes or spend this turn. Prior automatic-review selected-Microsoft/checkout prerequisites persist; no duplicate owner question or workaround.

Canonical lease followed Pinterest then Merchant release. Root updates only own Microsoft/TA-15 checkpoints, dated scorecard, decision/review and this append; exact paid control, parent OneOwnerAction and peer rows preserved. Before/after and exact local inverse segments recorded in launch-plan-20260911/canonical_update_plan.json. Renderer/integration/strict/diff results are saved after execution in closeout_checks.json.

- `source_live_evidence_as_of`: 2026-09-11T16:47:40Z to2026-09-11T16:49:50Z Shopify reads only; Microsoft native not refreshed
- `live_state_mode`: STALE_READBACK_REQUIRED for full-paid; stated Shopify configuration/report facts LIVE_VERIFIED_READ_ONLY
- `effective_approval_policy`: FRESH_ACTION_TIME_APPROVAL_REQUIRED for full-paid; saved bounded Microsoft nonspend repair retained
- `approved_external_scope`: NONE in authoritative full-paid control
- `authority_context`: CURRENT_OWNER_MICROSOFT_REPAIR_AND_LOCAL_PAUSED_PREPARATION; supplied research adds no numeric launch authority
- `decision_depends_on_uncertain_state`: true
- `decision_changing_evidence`: correct-account purchase/consent/overlap, approved exact Shopping offers, actual contribution, native CPC controls and owner cash/loss limits
- `if_evidence_supports_recommendation`: complete reviewed nonspend repair, read back qualified paused preparation and present the exact single-test activation packet
- `if_evidence_opposes_recommendation`: reject the failed candidate or choose the qualified alternative; preserve sources/history and do not weaken economics/CPC/authority
- `material_decision`: true for future paid-test selection; local preparation only this turn
- `independent_verifier`: international_campaign_build
- `verifier_independence`: DID_NOT_BUILD_OR_EXECUTE_ROOT_MATH_CONTRACT_OR_ANALYTICS_READS; primary-doc and frozen-receipt review

Single next Microsoft action: obtain the existing exact selected-account readiness and serialized handback, then inspect receiver/CPC/feed controls because these determine the concrete repair and which single test qualifies. Parent OneOwnerAction remains unchanged. Continue through ops/prompts/paid-growth-ai-army-continuation-prompt.md from this anchor; no separate operating prompt.""")
# Packet guidance, not campaign CSV mutations.
plan_path=PREFIX+'/campaign_plan.md'
title=(REPO/plan_path).read_text().splitlines()[0]
replace(plan_path,title+'\n',title+"""\n\n## September 11 current launch decision

The [reconciled launch plan](launch-plan-20260911/RECONCILIATION.md) and [local launch contract](launch-plan-20260911/launch_contract.json) now control the proposed first activation: one US/en experiment, narrow Search first candidate and Standard Shopping conditional alternative. Existing USEN/DEDE paused preparation and every campaign CSV remain unchanged. The older5+3/day and6.5ROAS examples below are dated scenarios, not approved/current launch budgets; the new local model uses15%/6.67 and actual contribution with30%reserve. Functional purchase acceptance is required before activation; legitimate paid-click attribution is verified after activation and before scale. No new native create/import/enable/spend.\n""")
replace(plan_path,"1. Root's correct-account UET purchase evidence: one completed paid purchase, revenue/currency, consent and deduplication.","1. Root's correct-account UET functional purchase evidence: one authorized genuine completed purchase, revenue/currency, consent and repeat-delivery behavior. A prior ad click is not required for that functional check; legitimate paid-click attribution is a post-activation gate before scaling.")
old=next(s for s in (REPO/plan_path).read_text().splitlines() if s.startswith('**Next action:**'))
replace(plan_path,old,"**Next action:** after the existing exact-account access handback, finish receiver and current CPC/feed qualification; preserve qualified U.S. English/Germany German paused preparation. Select only one first US paid experiment using [the September11 contract](launch-plan-20260911/launch_contract.json). Remaining offer, actual-cost and numeric launch gates stay open. Continue through [the canonical paid-growth prompt](../../../ops/prompts/paid-growth-ai-army-continuation-prompt.md); this packet creates no competing operating prompt.")
add_before(PREFIX+'/READBACK.md','## Latest resume — September10 02:13UTC',"""## Latest continuation — September 11 supplied plan reconciled

**LOCAL_PREPARATION_VERIFIED; native receiver/staging remains gated.** The [new reconciliation](launch-plan-20260911/RECONCILIATION.md) integrates the supplied research with September11 Shopify reports,21locales/sixmarkets/23variants and independent primary-document review. It prepares one US paid experiment with Search first candidate and Shopping conditional alternative; preserves the USEN/DEDE paused-preparation scope and11design/9language library. The existing campaign CSVs and audited app/storefront source bytes are unchanged. Native feed/receiver/CPC controls, actual contribution and approved cash/loss remain unknown; the historical August112.60 illustration is not a Microsoft budget.

New implementation is local only: fixed-window read-only receipts, six reproducible basket scenarios, explicit purchase prelaunch/postlaunch gates and a non-executable [launch contract](launch-plan-20260911/launch_contract.json). No native calls, Microsoft settings/native drafts/Shopify mutation or new spend this turn. The prior exact selected-tab/checkout questions remain pending; no duplicate question or access workaround. Current UX137888792673 successor owns theme release; earlier137881223265 references below are historical. Preserve prior Smart/Coral repairs.

Continue with the existing canonical prompt at anchor2026-09-11-microsoft-launch-plan-reconciled. [Independent platform review](launch-plan-20260911/platform_review.md); [independent reconciliation review](launch-plan-20260911/independent_reconciliation_review.json); [closeout checks](launch-plan-20260911/closeout_checks.json).""")
# Before-state protection captures exact scope outside all proposed replacements.
current={p:(REPO/p).read_text() for p in sorted({x['path'] for x in changes})}
updated=dict(current)
for c in changes:
    if c.get('append'): updated[c['path']]+=c['new']
    else:
        assert updated[c['path']].count(c['old'])==1, c['path']
        updated[c['path']]=updated[c['path']].replace(c['old'],c['new'],1)
def sha(s):return hashlib.sha256(s.encode()).hexdigest()
state=current['ops/marketing/current_marketing_state.md']
control=re.search(r'<!-- MARKETING_AUTHORITATIVE_CONTROL:START -->.*?<!-- MARKETING_AUTHORITATIVE_CONTROL:END -->',state,re.S).group()
owner=re.search(r'## One Owner Action\n.*?(?=\n## )',current['ops/marketing/operator_cockpit.md'],re.S).group()
assert control in updated['ops/marketing/current_marketing_state.md']
assert owner in updated['ops/marketing/operator_cockpit.md']
before_peer_rows=[s for s in current['ops/AGENT_COORDINATION.md'].splitlines() if s.startswith('|') and '| Current owner Microsoft Ads tracking and campaign rebuild |' not in s]
after_peer_rows=[s for s in updated['ops/AGENT_COORDINATION.md'].splitlines() if s.startswith('|') and '| Current owner Microsoft Ads tracking and campaign rebuild |' not in s]
assert before_peer_rows==after_peer_rows
before_queue=[s for s in current['ops/marketing/action_queue.md'].splitlines() if s.startswith('|') and '`TA-15`' not in s]
after_queue=[s for s in updated['ops/marketing/action_queue.md'].splitlines() if s.startswith('|') and '`TA-15`' not in s]
assert before_queue==after_queue
payload={'anchor':ANCHOR,'status':'PREPARED_NOT_APPLIED','changes':changes,'before_hashes':{p:sha(s) for p,s in current.items()},'expected_after_hashes':{p:sha(s) for p,s in updated.items()},'preserved_paid_control_sha256':sha(control),'preserved_owner_action_sha256':sha(owner),'peer_claim_rows_preserved':len(before_peer_rows),'peer_queue_rows_preserved':len(before_queue)}
(HERE/'canonical_update_plan.json').write_text(json.dumps(payload,indent=2)+'\n')
print(json.dumps({k:v for k,v in payload.items() if k not in ['changes','before_hashes','expected_after_hashes']},indent=2))
print('Prepared replacements:',len(changes),'files:',len(current))

