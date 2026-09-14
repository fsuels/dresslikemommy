"""Prepare exact Microsoft-owned continuity changes without applying them."""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
ANCHOR = "2026-09-11-microsoft-purchase-goals-and-ad-controls"
EVIDENCE = "2026-09-09-microsoft-ads-rebuild/receiver-20260911-1930"
edits = []

def add(path, before, after):
    text = (ROOT / path).read_text()
    assert before != after
    assert text.count(before) == 1, (path, text.count(before), before[:90])
    edits.append(dict(file=path, operation="replace", before=before, after=after))

def row(path, prefix, after):
    lines = (ROOT / path).read_text().splitlines()
    found = [x for x in lines if x.startswith(prefix)]
    assert len(found) == 1, (path, prefix)
    add(path, found[0], after)

def section(path, title, after):
    text = (ROOT / path).read_text()
    match = re.search(r"^#{2,3} " + re.escape(title) + r"\n", text, re.M)
    assert match, (path, title)
    following = re.search(r"^#{2,3} ", text[match.end():], re.M)
    end = match.end() + following.start() if following else len(text)
    add(path, text[match.start():end], after.rstrip() + "\n\n")

def append(path, after):
    text = (ROOT / path).read_text()
    edits.append(dict(file=path, operation="append", before="", after="\n\n"+after.rstrip()+"\n"))

checkpoint = f"""## September11 Microsoft purchase goals and ad controls

TA-15; anchor {ANCHOR}. Account477439/customer770182 is LIVE_VERIFIED in this task's authenticated background Microsoft browser. The earlier sign-in request is superseded. Five normal native Saves changed six reviewed fields: ShopifyCheckoutCompleteEventTracking is now the sole primary checkout goal, counts All and uses variable revenue with USD0 fallback; legacy ShopifyCheckoutCompleteTracking and Purchases stay Active but are excluded from bidding/standard Conversions. Smart and AddToCart remain secondary. Both automatic ad-creation opt-ins are Off: responsive search ad recommendations and multimedia creation in dynamic ad groups. All11 campaigns remain Paused with their configured budgets unchanged; MSCLKIDOn and other recorded account settings are preserved. Goal pre/post review21/24checks, ad-control pre/post8/8checks PASS. Configuration is verified, not purchase accuracy or profit.

UET36005151 is Active. Purchase dashboard shows94events in the six-month-limited view; last event four days ago; event parameters list GoalValue/Currency/PageType/ProductId, but sample values/order identities were not exported. Regional seven-day consent tooltips: pageview27%, view_item0%; purchase Healthy means no EEA/UK/Switzerland sample, not proven regional consent. Independent correction review12checks PASS. Counting All is not order deduplication. Legacy goal history remains; standard conversion/revenue/ROAS reporting can change after exclusion. Real purchase/value/currency/order-repeat/paid-attribution and actual contribution remain unverified.

Shopify native app/home returned a technical loading error after the normal retry and safe store-home fallback; no authentication cause or app-side repair is claimed. The publisher cookie-source defect remains a supported-app repair dependency; no duplicate sender, unconditional consent or local-vendor-copy pretend fix. Native Search creation was inspected and cancelled before Save. Microsoft says Search Save & exit can start ads, so no paused/draft persistence is inferred. Existing local USEN/DEDE preparation remains2groups/6exact keywords/2RSAs/14negatives, with ten local destination fields corrected to the directly inspected US/en and DE/de dresses collections. German market renders Deutsch/EUR; collection readback is not fulfillment/checkout/native-language acceptance. Four local collection-ID/provenance fields are corrected too. Existing pausedAU402056810 exposes a MaximizeClicks optional0.15USDfield with no inline error; inspection was cancelled and originalEnhancedCPC/Paused/5USDreopened. Newcampaign/serveracceptance/inheritance/actualCPC remainunverified; legacyTextcustomization staysOn. See cpc_control_readback.json. Scheduled-import table at477439 returned no results with only Excludingdeletedfilter; no import changes.

Existing microsoft-ads-profitable-growth-operator heartbeat remains ACTIVE every4h on this task; first scheduled execution remains unobserved. Earlier103-negative decisions and fixed August12–September10 order baseline10paid orders/821.44USDsubtotal are preserved. Next internal action: resolve the supported app consent/purchase receiver path and qualify explicit Paused creation with a current enforceable CPC control; actual costs and numeric launch cash/loss remain required before the single proposed paid experiment. No paid activation or profit increase is claimed. Parent V7 owner publication action, all peer ownership and full-paid NONE are unchanged. Evidence:{EVIDENCE}/READBACK.md.
"""

row("ops/AGENT_COORDINATION.md", "| Current owner Microsoft Ads tracking and campaign rebuild |",
    f"| Current owner Microsoft Ads tracking and campaign rebuild | Microsoft477439/customer770182; UET36005151/APP931561569; current receiver and initial USEN/DEDE preparation | "+chr(96)+"LIVE_GOAL_AND_AD_CONTROLS_VERIFIED__PURCHASE_CONSENT_AND_STAGE_GATED"+chr(96)+f" | root01a08703 sole Microsoft writer; international_campaign_build independent exact reviews; UX owns theme | Current owner ongoing Microsoft follow-through and bounded nonspend repair/qualified paused preparation; existing every4h heartbeat | No new numeric paid launch, billing/security/account switch, fabricated purchase, blind source/consent patch or theme publication; preserve peers and existing sources | {EVIDENCE}/READBACK.md; exact_goal_postflight_review.json; auto_creation_postflight_review.json; anchor{ANCHOR} | Authentication verified; obsolete sign-in gate superseded. Five Saves/six fields: sole primary purchase Event All/USD0 fallback, legacy checkout goals secondary, two ad-creation opt-insOff. All11Paused/budgets/MSCLKID preserved. Regional consent page27%/view_item0%; purchase no regional sample. App technical-load error; native Search Save&exit may serve, no new campaign. Profit/cost/purchase acceptance open; parent V7/paidNONE preserved. Canonical interval released to X after checks |")

row("ops/marketing/action_queue.md", "| P0 | YELLOW | "+chr(96)+"TA-15"+chr(96),
    f"| P0 | YELLOW | "+chr(96)+"TA-15"+chr(96)+f" Finish Microsoft477439/770182 purchase acceptance and qualified paused preparation | root01a08703 sole Microsoft writer; independent exact reviews; UX owns theme | Live purchase-goal and two ad-control corrections verified; regional consent, source repair, explicit paused creation/CPC and actual economics open | current_marketing_state.md; {EVIDENCE}/READBACK.md; anchor{ANCHOR} | Paid traffic | In progress | Technical dependency | Five Saves/six fields verified; one primary event purchase; all11Paused; MSCLKIDOn; every4h follow-up ACTIVE | Complete supported app consent and real purchase receiver acceptance, then qualify explicit paused USEN/DEDE creation and current CPC control. No repeat sign-in/goal repair; numeric launch gated | 2026-09-11 | Finish purchase/consent acceptance and paused cost-control qualification |")

section("ops/marketing/current_marketing_state.md", "September11 Microsoft recurring operator and campaign cleanup", checkpoint)
section("ops/marketing/operator_cockpit.md", "September11 Microsoft recurring operator", checkpoint)
section("ops/PROBLEM_TRACKER.md", "Microsoft September11 recurring operator checkpoint",
f"""### Microsoft September11 purchase receiver and paused preparation checkpoint

Current status: ACTIVE_OPERATOR / CONFIGURATION_REPAIR_VERIFIED / FUNCTIONAL_ACCEPTANCE_OPEN. Account477439/customer770182 authenticated in own background IAB; old sign-in dependency superseded. Exact event purchase goal is sole primary, All count/variable USD0 fallback; two URL checkout goals remain Active/secondary; Smart/AddToCart preserved. Two automatic-ad-creation opt-outs savedOff. All11Paused/budgets/MSCLKID and recorded unlisted options preserved. Five native Saves/sixfields, independently reviewed. No source reinstall, repeat prior repair or native campaign creation.

Regional consent signals are incomplete: pageview27% and view_item0% of eligible regional events in seven days; purchase Healthy explicitly has no EEA/UK/CH sample. No exported values/order IDs, true order dedup or paid revenue acceptance. Shopify app/home technical loading error prevents current supported UI source correction; no inferred login or source-specific cause. Microsoft Search Save&exit may serve, so explicit Paused persistence and current CPC cap remain open. Local10URLfields now select observed matching-dress destinations; purchase/checkout/fulfillment/native-language and actual economics/cash/loss gates remain. Existing every4h follow-up and103-negative/fixed10-order baselines preserved. Evidence:{EVIDENCE}/READBACK.md; anchor{ANCHOR}. Historical attempts below remain dated evidence; parent V7 and full-paidNONE unchanged.
""")

path="ops/marketing/blocker_board.md"
line=next(x for x in (ROOT/path).read_text().splitlines() if x.startswith("TA-15: account477439/customer770182"))
add(path,line,f"TA-15: Microsoft477439/customer770182 authenticated; old sign-in request superseded. Five reviewed native Saves/sixfields completed: sole primary event purchase All/USD0fallback, legacy checkout secondary, two ad-creation opt-outsOff. All11Paused/budgets/MSCLKID preserved. Remaining receiver gaps: actual values/order repeats/paid attribution and regional consent pageview27%/view_item0%; purchase Healthy means no regional sample. Shopify app/home technical load error; supported publisher-cookie repair remains open. Native Search Save&exit may serve, so paused persistence/current CPC need qualification. Local USEN/DEDE dress destinations corrected; actual costs and exact numeric cash/loss remain unknown. Every4h follow-up ACTIVE; parent V7/fullpaidNONE/peers preserved. Evidence:{EVIDENCE}/READBACK.md; anchor{ANCHOR}.")

append("ops/marketing/daily_scorecard.md",f"""## September11 Microsoft configuration repair and receiver limits

{ANCHOR}: five native Saves/six fields IMPLEMENTED and configuration readback VERIFIED. Sole primary purchaseEvent All/variable USD0fallback; both legacy checkout goals Active/secondary; autoRSA and multimedia-in-dynamic-groups opt-insOff. All11 campaigns Paused, configured budgets total120USD/day unchanged; that total is not spend authority or actual spend. MSCLKIDOn. UET36005151 Active; six-month-limited dashboard94purchase events, last event four days ago, and parameter names only. Seven-day EEA/UK/CH signal coverage page27%, product0%; purchase Healthy has no regional sample. No new order/value/currency/dedup/paid-attribution or profit acceptance. Fixed August12–September10 ten-order/821.44USD subtotal baseline remains separate. Independent goal21/24, controls8/8, regional interpretation12 checks PASS. Evidence:{EVIDENCE}/READBACK.md. No change to other cohorts or full-paid authority.
""")

append("ops/marketing/decision_log.md",f"""## DLM-DEC-2026-09-11-MICROSOFT-SINGLE-PURCHASE-GOAL

Registered from the prewrite frozen purchase_goal_repair_contract.json SHAa5b8b398e04fb3755e85304c711f81c32bed21e8495df00f82c508c1997cb1b7 and decision_challenge_amendment.json; no retrospective invented prediction. Existing event purchase with variable value is the selected primary; two overlapping URL checkout definitions become secondary. CountAll captures repeat conversions; zero fallback avoids fabricated fixed purchase value when missing. Alternative retains three primary checkout definitions and inconsistent fixed defaults. No deletion, source replacement, consent or spend change; exact inverse four fields retained. Independent21-check preflight and24-check postflight pass; reviewer DID_NOT_BUILD_OR_EXECUTE.

DLM-OUT-2026-09-11-MICROSOFT-SINGLE-PURCHASE-GOAL: three native Saves/fourfields completed; full goal editors reopened, all5Active, one primaryEvent All/USD0fallback, accountMSCLKID and11Paused campaigns/budgets preserved. Configuration prediction met. Actual transaction values, regional consent, order-repeat handling and paid attribution remain UNKNOWN. CountAll is not dedup; retained legacy history does not mean unchanged standard-report totals. No profit claim.

## DLM-DEC-2026-09-11-MICROSOFT-MANUAL-AD-CONTROL

Registered from prewrite frozen auto_creation_contract.json SHAb4a00ad74ade466f34af5f62abff159b6658049b460ac37a0387ad54c09cf90d. Selected two exactOn-to-Off opt-outs: auto-apply Add responsive search ads and Automatically create multimedia ads in my dynamic ad groups. Alternative leaves unreviewed new creative creation enabled; deleting existing objects is unnecessary. Zero new advertising exposure; preserve unlisted settings, all paused campaigns and prior goal repair. Exact inverse two checkbox values retained.

DLM-OUT-2026-09-11-MICROSOFT-MANUAL-AD-CONTROL: two native Saves/twofields completed; both pages reopenedOff, other four auto-apply optionsOff and recorded account options/MSCLKID preserved, all11Paused and goal grid preserved. Independent pre/post8/8PASS, DID_NOT_BUILD_OR_EXECUTE. Existing multimedia placeholders remain and cannot be edited while opted out; no all-automation/placement exclusion claim. Regional consent correction independently12checksPASS: purchase Healthy was no sample; pageview27%/view_item0% are signal coverage. No purchase/profit causality. Evidence for both decisions/outcomes:{EVIDENCE}/READBACK.md; anchor{ANCHOR}.
""")

append("ops/marketing/review_log.md",f"""## September11 Microsoft exact native repair verification

/root/international_campaign_build DID_NOT_BUILD_OR_EXECUTE: goal preflight21/postflight24checksPASS; exact two ad-creation opt-outs preflight8/postflight8PASS; corrected regional-consent interpretation12PASS. Contracts bind exact477439/770182 fields and rollback; after comparisons bind root's independently reopened native readbacks. Reviewer did not replay the browser. Both goal/existing11Paused/account-preservation observations reconcile. Unrecorded campaign ads/bids were not individually audited and current grid does not reverify every detailed goal field. Historical IDs in editors remain REPO_KNOWN where not exposed. Configuration is complete; real order/value/currency/dedup/EEA-UK-CH consent, supported source repair and profit remain unverified. Source purchase Healthy has no regional sample; previous generic>75% application is withdrawn, not applied as measured coverage. Evidence:{EVIDENCE}/exact_goal_postflight_review.json, auto_creation_postflight_review.json, consent_diagnostic_independent_review.json; anchor{ANCHOR}.
""")

append("ops/AGENT_WORKLOG.md",f"""## 2026-09-11 Microsoft purchase goals and ad controls

AGENT_CONTINUITY_ANCHOR: {ANCHOR}

VERIFY / LIVE_VERIFIED exact Microsoft477439/customer770182. Owner continued professional repairs; task-owned IAB authentication succeeded, superseding obsolete sign-in gate. Root sole external writer. Three goal Saves/fourfields and two automatic-ad-control Saves/twofields completed with frozen exact plans, before/staged/readback/inverse and independent reviews. Sole primary ShopifyCheckoutCompleteEventTracking nowAll/variableUSD0fallback; URL checkout goals remainActive/secondary, Smart/AddToCart preserved. Both ad-creation opt-insOff; all11Paused/budgets/MSCLKID/account settings preserved. Actual receiver purchase/value/order dedup/consent/profit remainsopen. PurchaseHealthytooltip=no regional sample; pageview27%/view_item0% eligible regional seven-day signal coverage,12independent checksPASS. Shopifyapp/home technicalloadingerror; no auth inference or source pretendfix. Search wizard inspected/cancelled beforeSave, since official Save&exit mayserve. Local initial USEN/DEDE10destination fields select actualmatching-dresscollections; no new native campaign or exposure. Existing103negative dispositions/10-orderbaseline/4hheartbeat preserved.

Current paid authority machine fields: source_live_evidence_as_of=2026-06-01; live_state_mode=STALE_READBACK_REQUIRED; effective_approval_policy=FRESH_ACTION_TIME_APPROVAL_REQUIRED; approved_external_scope=NONE. These marked full-paid values are preserved, not promoted by the separate current owner nonspend repair authority. Exact-surface evidence is2026-09-11 in this packet. decision_depends_on_uncertain_state=true; decision_changing_evidence=realpurchase/value/currency/orderrepeat/regionalconsent plus explicitpausedpersistence/currentCPC/actualcost/cash; if_evidence_supports_recommendation=finish qualified paused stage then request only exact missing paidlaunch authority; if_evidence_opposes_recommendation=hold affected market and complete supported source/landing correction; material_decision=true; independent_verifier=/root/international_campaign_build; verifier_independence=DID_NOT_BUILD_OR_EXECUTE.

Evidence:{EVIDENCE}/READBACK.md; purchase_goal_repair_contract.json/execution_receipt.json, auto_creation_contract.json/auto_creation_execution_receipt.json and exact independent reviews. Frozen decisionsDLM-DEC-2026-09-11-MICROSOFT-SINGLE-PURCHASE-GOAL andDLM-DEC-2026-09-11-MICROSOFT-MANUAL-AD-CONTROL have linked configuration outcomes, not business acceptance. No completed source/Coral/Smartrepair reapplied; no private Chrome use, account switch, billing change, paid activation or theme write. Canonical closeout only after explicit GoogleAds01a09194release; exact inverse verifies unrelatedbytes. Preserve parentV7ownerpublication/fullpaidblock/peers. Release interval to X01a0915d and root after renderer/integration/strict checks; continued Microsoft UI/ownpacket work does not hold sharedlease.

Next operator action: supported Shopify app consent and purchase receiver acceptance, plus explicit paused/CPC qualification. Owner OneAction remains existing reviewed V7 publication through ShopifyAdmin because it addresses live buyer defects and AUrelease. Continue via ops/prompts/paid-growth-ai-army-continuation-prompt.md at this anchor, TA-15, preserving fivecompletedSaves and exactuncertainties.
""")

before_dir=Path(json.loads((OUT/"canonical_snapshot_location.json").read_text())["directory"])
before_dir.mkdir(exist_ok=True)
hashes={}
for path in sorted({e["file"] for e in edits}):
    data=(ROOT/path).read_bytes()
    (before_dir/path.replace("/","__")).write_bytes(data)
    hashes[path]=hashlib.sha256(data).hexdigest()
control=re.search(r"<!-- MARKETING_AUTHORITATIVE_CONTROL:START -->.*?<!-- MARKETING_AUTHORITATIVE_CONTROL:END -->",(ROOT/"ops/marketing/current_marketing_state.md").read_text(),re.S).group()
parent=next(x for x in (ROOT/"ops/marketing/current_marketing_state.md").read_text().splitlines() if x.startswith("One Owner Action:"))
plan=dict(status="FROZEN_AWAITING_INDEPENDENT_REVIEW",anchor=ANCHOR,writer_release="Explicit Ads01a09194 release to Microsoft received in current session; next X then Pinterest",edits=edits,before_hashes=hashes,guarded_sections={"full_paid_control_sha256":hashlib.sha256(control.encode()).hexdigest(),"parent_one_owner_action_sha256":hashlib.sha256(parent.encode()).hexdigest()},rules=["No peer edits","Each exact before once","Only ten root continuity targets","Separate local landing correction must pass before applying text claiming correction","Render, integration, strict, scoped diff and exact inverse preservation before release"])
(OUT/"canonical_update_plan.json").write_text(json.dumps(plan,indent=2)+"\n")
print(json.dumps(dict(status=plan["status"],files=len(hashes),edits=len(edits),anchor=ANCHOR,guards=plan["guarded_sections"])))
