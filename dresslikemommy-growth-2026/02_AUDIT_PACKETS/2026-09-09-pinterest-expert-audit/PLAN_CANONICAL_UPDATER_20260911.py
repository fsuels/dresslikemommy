from pathlib import Path
from datetime import datetime,timezone
import json,re,hashlib,sys,difflib
root=Path('/Users/fsuels/Projects/dresslikemommy'); packet='2026-09-09-pinterest-expert-audit'; anchor='2026-09-11-pinterest-owner-plan-and-guide-creative'
base='dresslikemommy-growth-2026/02_AUDIT_PACKETS/'+packet
changes={}
def edit(rel,fn):
 p=root/rel;old=p.read_text();new=fn(old);assert old!=new,rel;changes[rel]=(old,new)
def insert(s,marker,new):
 assert s.count(marker)==1,marker
 assert anchor not in s,'already applied'
 return s.replace(marker,new+'\n\n'+marker,1)
def line(s,prefix,fn):
 a=s.splitlines(True);ids=[i for i,x in enumerate(a) if x.startswith(prefix)];assert len(ids)==1,prefix
 i=ids[0];a[i]=fn(a[i].rstrip('\n'))+'\n';return ''.join(a)
summary='''## September11 owner Pinterest plan and next guide creative

User-supplied September10 plan reconciled against current official sources and existing receipts. Local primary proposal now manual Sales/Pins/explicit completed Checkout, one provisionalUS/English adult-shopping group and two distinct creatives. The exact older ConsiderationUSD15/72h proposal is archived, not activated. USD5fixed-daily is a starting proposal only; total loss/cap/dates and approvedCPA remain unset. Full Performance+ All Products/automatic retargeting is excluded from this initial design. No saved native campaign or new spend authority.

Original P1 guide checklist artwork is finished at1024x1536; original P1title/description and social UTM retained, existing six-copy artifact unchanged.12capacity slots include the completed Sunshine Pin and two later real-video concepts, at most3totalPins per rolling7days. Dates are proposals, no upload/publication/scheduling occurred. Exact P1 publication scope and native identity/duplicate/crop/tagged-link checks remain for final action; prior Sunshine one-Pin authority is already fulfilled. Four dated merchandise-only6.5x CPA ceilings are3.38/3.84/7.22/11.07USD, not approved profitable CPAs; actual basket costs remain unknown.

Existing consent-test approval and owner-activity/native handback remain unresolved; this research plan is not a temporary consent grant. Current callback/consent conflict, open test-tab cleanup and receiver/purchase/catalog gates remain as recorded below. UX release ownership, completed Pin/board/source repairs, TA-11completion/TA-20measurement, other owners and full-paidNONE preserved. Evidence: '''+packet+'/PLAN_RECONCILIATION_20260911.md; P1_RELEASE_PACKET_20260911.json; PLAN_SOURCE_CHECK_20260911.md; anchor'+anchor+'.'
edit('ops/marketing/current_marketing_state.md',lambda s:insert(s,'## September 11 Pinterest pixel callbacks verified; consent acceptance conflicted',summary))
digest='''## September11 Pinterest owner-plan implementation

Current local primary spec is manual Sales/Pins/completed Checkout; old Consideration15USD/72h exact file archived. No native campaign or numeric approved loss/CPA/cap. P1original checklist artwork finished; six existing copy records and social UTMs preserved.12unscheduled capacity slots including completed Sunshine and2video concepts, at most3per rolling7days. Actual costs, P1final native/publication scope, consent-test approval, cleanup and receiving evidence remain gated. No new publication, consent, spend or theme action; no change to existing clocks/owners. Evidence: '''+packet+'/PLAN_RECONCILIATION_20260911.md; anchor'+anchor+'.'
edit('ops/marketing/memory_digest.md',lambda s:insert(s,'## September 11 Pinterest native diagnostic checkpoint',digest))
score='''## September11 Pinterest local production outcome

One original P1guide graphic now exists locally,1024x1536, with original copy/link and hash-bound release packet.12capacity slots reconcile existing Sunshine/P1-P6 and five later concepts; only Sunshine is published. New live Pins0, scheduledPins0, campaigns0 and media spend0 from this turn. Primary local proposal switched to Sales/Pins/completed Checkout without inferring eligibility or performance.19root local structure/UTM/cadence/asset/arithmetic checksPASS; independent review is recorded in the packet. Existing acquisition/receiver metrics and Sunshine full-date windows unchanged. Actual basket economics and consent/native gates remain open. Evidence: '''+packet+'/PLAN_ROOT_CHECKS_20260911.json; PLAN_IMPLEMENTATION_REVIEW_20260911.md; anchor'+anchor+'.'
edit('ops/marketing/daily_scorecard.md',lambda s:insert(s,'## September 11 Pinterest diagnostic receipt; no acquisition result',score))
block='''## September11 Pinterest plan is ready locally; execution gates preserved

The new manual Sales/Pins/completed Checkout proposal and finished P1guide asset do not clear consent, receiving-event, current-cost or exact launch authority gates. Existing temporary consent-test question remains pending, native owner-activity pause continues, and P1must pass final profile/duplicate/crop/link and exact publication-scope checks. Numeric approvedCPA/loss/totalcap/dates unset. No defaultPerformance+AllProducts, old15USDtraffic-test activation or extra calendar. Full-paidNONE and currentUXowner retained. Evidence: '''+packet+'/PLAN_RECONCILIATION_20260911.md; anchor'+anchor+'.'
edit('ops/marketing/blocker_board.md',lambda s:insert(s,'## September 11 Pinterest consent-test approval and stable native access',block))
add=' Owner-plan update: manual Sales/Pins/completed Checkout is now the conditional primary spec, with no approvedCPA/loss/cap/dates; old traffic spec archived. P1guide checklist artwork finished locally; original copy/UTMs preserved.12unscheduled slots include Sunshine and2video concepts. Exact P1native/publication scope remains for final action. [Plan and creative](../../'+base+'/PLAN_RECONCILIATION_20260911.md). Anchor'+anchor+'.'
edit('ops/marketing/operator_cockpit.md',lambda s:line(s,'Pinterest checkpoint September11:',lambda old:old+add))
edit('ops/marketing/action_queue.md',lambda s:line(s,'| P1 | YELLOW | `TA-12`',lambda old:old.replace('Connection/privacy and local page/product callbacks verified;','Local Sales/Pins/Checkout proposal reconciled, P1guide asset prepared; connection/privacy and local page/product callbacks verified;').replace('PIXEL_HELPER_INTERPRETATION_20260911.md;','PIXEL_HELPER_INTERPRETATION_20260911.md; PLAN_RECONCILIATION_20260911.md;')))
edit('ops/AGENT_COORDINATION.md',lambda s:line(s,'| Current owner Pinterest expert audit and growth setup |',lambda old:old.replace('Existing repairs preserved;','Existing repairs preserved; local Sales proposal/P1guide asset ready, native publication/launch gates retained;').replace('Shared interval ends after closeout checks','Owner-plan packet '+packet+'/PLAN_RECONCILIATION_20260911.md; anchor'+anchor+'. Shared interval ends after closeout checks')))
frame=json.loads((root/base/'PLAN_DECISION_FRAME_20260911.json').read_text())
dec='''\n\n## DLM-DEC-2026-09-11-PINTEREST-MANUAL-SALES-PLAN

Frozen before replacing the current local proposal in PLAN_DECISION_FRAME_20260911.json at'''+frame['frozen_at_utc']+'''. Current owner supplied a September10Pinterest growth plan. Chosen: primary manual Sales/Pins/explicit completed Checkout pilot, source-qualified2creatives and real basket economics; finish an original P1guide asset while preserving existing copy/UTMs and capacity. Alternative: retain cheap-traffic calibration as default or use unrestricted Performance+AllProducts; neither resolves current purchase/consent/economics evidence. Prior proposal archived byte-exact; no frozen prior decision rewritten.

Prediction/success: accurate current campaign semantics, no invented spend cap or CPA, one truthful readable2:3guide asset and zero drift to prior public Pins/6copy/UTMs/owners. Kill: unverified availability, costs, true receipt, explicit consent, publication or spending authority promoted to fact. Current max media exposure0USD. Window: local reconciliation this turn; business cohorts start only on actual future publication/activation, preserving Sunshine dates. Rollback is retained historical local spec and versioned asset; no external state to undo.

- decision_id: DLM-DEC-2026-09-11-PINTEREST-MANUAL-SALES-PLAN
- outcome_id: DLM-OUT-2026-09-11-PINTEREST-PLAN-AND-P1-ASSET
- outcome_status: LOCAL_PLAN_AND_CREATIVE_VERIFIED__NATIVE_PUBLICATION_AND_PAID_GATED
- evidence: '''+packet+'''/PLAN_RECONCILIATION_20260911.md; PLAN_DECISION_FRAME_20260911.json; PLAN_ROOT_CHECKS_20260911.json; PLAN_IMPLEMENTATION_REVIEW_20260911.md

Observed: current spec Sales/Pins/Checkout, actual spend/draft0; P1original1024x1536graphic with exact original copy/link, existing source artifact unchanged.12slots/2video concepts respect3per rolling7days; no live schedule. Four Decimal floor CPA scenarios remain unqualified without actual costs.19root checksPASS; independent source/implementation review recorded separately, no account or buyer acceptance implied. Consent-test approval and owner native handback still pending. Source/asset readiness does not create publication/spend permission. Anchor'''+anchor+'.\n'
edit('ops/marketing/decision_log.md',lambda s:s+dec)
review='''\n\n## September11 Pinterest supplied-plan and creative review

/root/consent_diagnosis DID_NOT_BUILD_OR_EXECUTE independently checked eight current primary-source findings: Salescreative/event distinctions, Performance+campaign versus bidding, product/retargeting limits, fixed/average/lifetime budget semantics and scheduling. Account-specific availability/authority unverified. /root/release_verifier reviewed the implementation and viewed original P1asset; exact verdict, checks and any corrections are in PLAN_IMPLEMENTATION_REVIEW_20260911.md. Root19local structure/UTM/cadence/hash/arithmetic checksPASS. No independent native publisher, receiving-event, current-cost or conversion-performance proof. Evidence: '''+packet+'/PLAN_SOURCE_CHECK_20260911.md; PLAN_ROOT_CHECKS_20260911.json; anchor'+anchor+'.\n'
edit('ops/marketing/review_log.md',lambda s:s+review)
log='''\n\n## September11 — Pinterest owner plan implemented locally and next guide creative finished

AGENT_CONTINUITY_ANCHOR: '''+anchor+'\n\n'+summary.split('\n\n',1)[1]+'''

Primary source verification supports Sales/Pins/Checkout and budget distinctions; Shopifycheckout-upgrade deadline and PinterestNov12futuremerchant-policy date verified separately. No native or private-account probe after owner-activity pause. Built-in image_gen created originalP1graphic, then exact PNG copied into packet; no input photo/model, prices, stock, shipping speed or downloadable-PDF claim.19root local checks passed; independent source and implementation/visual reviews recorded separately. Existing organic pins.json, published Pin/board/source receipts and main paid-control bytes preserved. No new production pixel/privacy/theme/account/publisher/spend action.

- task_entities: TA-11, TA-12, TA-20, advertiser549756244483, tag2620007050621, pixel22577249, Pin343118065387544334, P1, product7545279512673, DLM-DEC-2026-09-11-PINTEREST-MANUAL-SALES-PLAN
- task_stage: HANDOFF
- source_live_evidence_as_of: 2026-09-11 official documentation/public guide and local asset evidence; native account/consent checkpoint remains earlierSep11, receiverSep10observed/Sep9updated
- live_state_mode: STALE_READBACK_REQUIRED for paid; no new native readback
- effective_approval_policy: current owner supplied plan permits local preparation; existing consent and exact live publication/spend gates remain
- approved_external_scope: NONE in unchanged full-paid control
- authority_context: CURRENT_USER_PLAN_LOCAL_PREPARATION_ONLY
- decision_depends_on_uncertain_state: true
- decision_changing_evidence: current native objective/event/budget controls, actual basket costs and purchase/consent receipt; exact P1publisher/asset/route checks
- if_evidence_supports_recommendation: complete only the qualified reviewed P1 or bounded paid action under exact current authority and readback
- if_evidence_opposes_recommendation: hold paid scope, fix the proven blocker and use independent truthful organic work; do not buy cheap clicks to mask missing orders
- material_decision: MANUAL_SALES_PRIMARY_LOCAL_SPEC_AND_P1_CREATIVE
- independent_verifier: consent_diagnosis source review; release_verifier implementation and asset review
- verifier_independence: DID_NOT_BUILD_OR_EXECUTE
- decision_id: DLM-DEC-2026-09-11-PINTEREST-MANUAL-SALES-PLAN
- outcome_id: DLM-OUT-2026-09-11-PINTEREST-PLAN-AND-P1-ASSET
- next_action_id: READ_ONLY_MARKETING_RECONCILIATION

One next Pinterest action: resolve the existing temporary-consent test approval and normal native handback, enabling controlled cleanup and receipt diagnosis. Disjoint lanes: P1final native/authority check, actual basket costs, same-windowTag/CAPI/catalog proof. Continue through ops/prompts/paid-growth-ai-army-continuation-prompt.md and this anchor. Local plan/creative changes are complete; external publication, paid launch and sales improvement remain unproved.\n'''
edit('ops/AGENT_WORKLOG.md',lambda s:s+log)
pat=r'<!-- MARKETING_AUTHORITATIVE_CONTROL:START -->.*?<!-- MARKETING_AUTHORITATIVE_CONTROL:END -->'
a,b=changes['ops/marketing/current_marketing_state.md'];control=re.search(pat,a,re.S).group();assert control==re.search(pat,b,re.S).group();assert len(control.encode())==506
out={'status':'APPLIED' if '--apply' in sys.argv else 'DRY_RUN','anchor':anchor,'control_sha256':hashlib.sha256(control.encode()).hexdigest(),'as_of_utc':datetime.now(timezone.utc).isoformat(),'files':[]}
for rel,(old,new) in changes.items():
 out['files'].append({'path':rel,'before_sha256':hashlib.sha256(old.encode()).hexdigest(),'after_sha256':hashlib.sha256(new.encode()).hexdigest()})
 if '--apply' in sys.argv:
  assert (root/rel).read_text()==old,'concurrent change: '+rel
  (root/rel).write_text(new)
Path('/private/tmp/dlm-pinterest-plan-canonical-result-20260911.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'files':len(out['files']),'control_sha256':out['control_sha256'],'anchor':anchor},indent=2))
