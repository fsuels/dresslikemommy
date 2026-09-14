"""One-use, narrow own-entry integration. Never reapply after the anchor exists."""
from pathlib import Path
from datetime import datetime, timezone
import json, re, hashlib, sys, difflib

ROOT = Path('/Users/fsuels/Projects/dresslikemommy')
PACKET = '2026-09-09-pinterest-expert-audit'
BASE = ROOT / 'dresslikemommy-growth-2026/02_AUDIT_PACKETS' / PACKET
ANCHOR = '2026-09-11-pinterest-content-batch-and-background-access'
APPLY = '--apply' in sys.argv
assert ANCHOR not in (ROOT / 'ops/AGENT_WORKLOG.md').read_text(), 'Already applied; do not replay'
queue = (ROOT / 'ops/marketing/action_queue.md').read_text()
used = {int(x) for x in re.findall(r'TA-(\d+)', queue)}
TASK = f'TA-{max(used) + 1:02d}'
NOW = datetime.now(timezone.utc).isoformat()
changes = {}

def sha(value):
    return hashlib.sha256(value.encode() if isinstance(value, str) else value).hexdigest()

def edit(path, transform):
    old = (ROOT / path).read_text()
    new = transform(old)
    assert old != new, path
    changes[path] = (old, new)

def insert_before(text, marker, addition):
    assert text.count(marker) == 1, marker
    return text.replace(marker, addition + '\n\n' + marker, 1)

def replace_line(text, prefix, replacement):
    lines = text.splitlines(True)
    ids = [i for i, line in enumerate(lines) if line.startswith(prefix)]
    assert len(ids) == 1, prefix
    lines[ids[0]] = replacement + '\n'
    return ''.join(lines)

def row(fields):
    assert all('|' not in x and '\n' not in x for x in fields)
    return '| ' + ' | '.join(fields) + ' |'

evidence = f'{PACKET}/CONTENT_BATCH_20260911.json; BACKGROUND_ACCESS_20260911.json; PROFILE_COPY_REPAIR_20260911.json'
summary = f'''## September11 Pinterest continuing content and current background access

The owner renewed ongoing Pinterest repair and organic-content work. Five new2:3 graphics P2-P6 are complete, making six prepared P1-P6 assets with original titles/descriptions/fourUTMs preserved. P4 independent28checks, P2/P5 combined54 and P3/P6 combined58 pass; original P1review remains. The current store-source Rainbow/Pastel images were recovered and inspected. The inconsistent Pastel child flat-lay is excluded; physical garment/media consistency is not certified. The six-image ZIP passes integrity. No new Pin, schedule, campaign, consent change or spend occurred. Existing12slots and at-most3totalPins per rolling7days remain; dates are candidates, not a schedule. TA-11 and TA-20 clocks stay separate and unchanged.

Fresh task-owned background IAB confirms the public Dress Like Mommy profile, existing merchant-guidelines badge and current unsupported largest/quality biography. A249-character factual replacement plus same-domain HTTP-to-HTTPS correction is independently reviewed and prepared, not saved. The editable session is currently another profile; advertiser549756244483 returns403. Shopify Customer Events stops at account selection; exact connector shop15571635 matches but pixel22577249 query is denied for missing read_pixels. No account switch, scope expansion, credential access or personal/native Chrome fallback. Existing account question remains pending.

A complete bounded222-request main-tab navigation kept marketing/analytics/preferences denied before and after, with zero Pinterest requests in that capture. This does not cover separate workers, granted consent, CAPI/receiver acceptance, catalog matching or a genuine purchase. The older native callback/consent conflict and cleanup uncertainty remain dated and unresolved. Full-paid control remains NONE/STALE_READBACK_REQUIRED. Current public P4 URL retains all four UTMs; product/guide main headings and Pastel Product metadata were read back.

{TASK} now owns continuing content/profile work independently of TA-12 measurement. Existing parent30-minute heartbeat may resume only a concrete eligible step; no duplicate scheduler was created. Next source work is N1: one640x667Together Heart overview exists, but actual neckline/cuff closeups are still needed; do not fabricate them. Evidence: {evidence}; N1_SOURCE_PREFLIGHT_20260911.json; anchor{ANCHOR}.'''
edit('ops/marketing/current_marketing_state.md', lambda s: insert_before(s, '## September11 owner Pinterest plan and next guide creative', summary))

score = f'''## September11 Pinterest six-asset production and bounded public QA

Five new images complete the existing six-Pin batch; all six1024x1536assets have exact original copy/UTMs and independent local review. New livePins0, schedules0, tracking-setting changes0, campaign activations0 and spend0. This is prepared content, not acquired traffic. Current public profile displays845followers/3kmonthlyviews and a merchant-guidelines badge; no growth trend or attributable sales is inferred. Fresh denied-consent main-tab capture222requests/zeroPinterest is limited evidence, not receiver or purchase proof. Profile two-field correction is prepared, not saved. ZIP integrity passes; separate Sunshine/article cohorts unchanged. Evidence: {evidence}; anchor{ANCHOR}.'''
edit('ops/marketing/daily_scorecard.md', lambda s: insert_before(s, '## September11 Pinterest local production outcome', score))

block = f'''## September11 Pinterest background identity and receiving evidence

Current access supersedes older shared-native directions: task-owned Pinterest IAB is a different editable profile and target advertiser returns403; Shopify Customer Events presents account selection; connector exact pixel read is denied for read_pixels. Owner connects existing background sessions; no duplicate question, account switch, permission change or native fallback. Six reviewed local Pins and truthful249-character bio/HTTPS correction are ready for fresh target/crop/duplicate/link checks. {TASK} continues independent source/creative work while TA-12 receiver/consent/purchase/catalog gates remain. Main-tab denied-consent222/zeroPinterest does not resolve older native conflict. Existing full-paidNONE, currentUXrelease owner and clocks preserved. Evidence: {evidence}; anchor{ANCHOR}.'''
edit('ops/marketing/blocker_board.md', lambda s: insert_before(s, '## September11 Pinterest plan is ready locally; execution gates preserved', block))

cockpit = f'Pinterest checkpoint September11: Six P1-P6 original-copy/UTM assets now prepared and independently reviewed; five created in this continuation, all unpublished/unscheduled. Current profile bio/HTTPS correction prepared. Task-owned Pinterest wrong-profile403 and Shopify account-selection/read_pixels gates remain. Bounded main-tab222requests with marketing/analytics/preferences denied and zeroPinterest is not receiver/worker/purchase proof. Older native consent/cleanup uncertainty persists. {TASK} owns continuing organic production separately from TA-12 measurement; existing parent30-minute heartbeat only, no new schedule. Full-paidNONE and all released Pin/cohort/UX ownership preserved. [Content and current access](../../dresslikemommy-growth-2026/02_AUDIT_PACKETS/{PACKET}/CONTENT_BATCH_20260911.json). Anchor{ANCHOR}.'
edit('ops/marketing/operator_cockpit.md', lambda s: replace_line(s, 'Pinterest checkpoint September11:', cockpit))

measurement_row = row(['P1','YELLOW','`TA-12` Finish Pinterest managed-integration and consent acceptance','root Pinterest task01a08704; UX release integrator; independent consent/release reviewers','Background account access and receiving proof required; complete denied main-tab capture is limited; older callback/consent conflict persists; UX137888792673 unpublished',f'{PACKET}/DENIED_CONSENT_NAVIGATION_20260911.json; BACKGROUND_ACCESS_20260911.json; SHOPIFY_PIXEL_CONFIG_READBACK_20260911.md; PROB-2026-09-09-PINTEREST-MEASUREMENT-ACCEPTANCE','Free + paid','Needs access','Access','Shop identity verified; denied flags before/after and222main-tab requests with zeroPinterest. Exact pixel query denied read_pixels; no missing-pixel inference or new consent/production change','Use owner-connected task-owned sessions for controlled consent/restoration and exact Tag14d/CAPI/catalog/real-purchase receipt checks; preserve old native uncertainty and exact existing consent-test gate', '2026-09-11','Finish Pinterest measurement acceptance'])
content_row = row(['P1','YELLOW',f'`{TASK}` Continue Pinterest content and profile repairs','root Pinterest task01a08704 sole publisher; independent source/creative reviewers','Six original-copy/UTM2:3assets reviewed; native account/duplicate/crop/link checks required. Existing12slots and3Pins per rolling7days; no paid authority',evidence,'Free traffic','Needs evidence','Access','Five newP2-P6assets plus existingP1 ready;140combined new creative checksPASS; six-image ZIP integrityPASS. Exact249-character bio/HTTPS correction reviewed, unpublished. N1overview source qualified; closeups missing','Continue N1source qualification independently. After correct account readback, save only reviewed bio/HTTPS fields and publish or schedule eligible Pins once with per-Pin after-readback and actual7/14/30-day cohorts. Do not wait on paid tracking to prepare truthful organic content','2026-09-11','Continue Pinterest content and profile repairs'])
assert len(measurement_row.split('|')) == 15 and len(content_row.split('|')) == 15
edit('ops/marketing/action_queue.md', lambda s: replace_line(s, '| P1 | YELLOW | `TA-12`', measurement_row + '\n' + content_row))

claim = row(['Current owner Pinterest expert audit and growth setup','Advertiser549756244483; tag2620007050621; pixel22577249; existingP1-P6; profiledresslikemommy','`CONTENT_BATCH_VERIFIED__BACKGROUND_ACCOUNT_GATED`','root01a08704 sole Pinterest owner; consent_diagnosis/consent_fix/release_verifier independent; UX01a088c3 owns137888792673','Owner renewed ongoing nonspend Pinterest repair/content. Six assets and exact two-field profile repair prepared; public/source reads and next N1qualification may continue. Fresh correct account/target/readback required for publishing','No wrong-account edit/switch, personal-native fallback, consent-review bypass, duplicate tag/reinstall, repeat released Pin/board/source repair, paid launch, MAIN publication, credential change or peer overwrite',f'{evidence}; anchor{ANCHOR}',f'New {TASK} content lane is separate from TA-12measurement and TA-20outcomes. No new native write this turn; old native cleanup uncertainty retained. Existing parent30-minute heartbeat only. Own-entry canonical interval releases directly to root after required checks.'])
edit('ops/AGENT_COORDINATION.md', lambda s: replace_line(s, '| Current owner Pinterest expert audit and growth setup |', claim))

problems = f'''## PROB-2026-09-11-PINTEREST-PROFILE-COPY

- Priority P2; status EXACT_REPAIR_READY__BACKGROUND_ACCOUNT_GATED; owner root01a08704; {TASK}.
- Fresh public profile still contains unsupported largest-collection/most-stylish/high-quality claims and an HTTP storefront link. Exact249-character factual bio and same-domain HTTPS correction independently PASS. Name/username/avatar/badge/Instagram/boards/Pins/ads remain outside this two-field change.
- Current viewer is another account; advertiser403. No Save attempted. After owner connects the existing session, refresh editor identity and before-state, apply only these two reviewed fields under the ongoing repair request, then reload and verify exact fields/preserved state.
- Evidence: {PACKET}/PROFILE_COPY_REPAIR_20260911.json; PROFILE_COPY_REPAIR_REVIEW_20260911.md; anchor{ANCHOR}.

## PROB-2026-09-11-PASTEL-IMAGE-PROPORTION

- Priority P2; status PIN_SOURCE_EXCLUSION_VERIFIED__PRODUCT_MEDIA_RECONCILIATION_OPEN. Pinterest root01a08704 owns creative exclusion; any product-source change remains with its qualified product owner.
- Exact current product7536086089825 lifestyle and child flat-lay depict materially different skirt-to-bodice proportions. Pictured sizes are unknown, so size variation versus generated-image inconsistency is unresolved. No physical fit defect or buyer injury is inferred.
- P3/P6 use only the reviewed lifestyle source; the child flat-lay is excluded. Do not recreate hidden garments or silently remove/change Shopify media. Resolve using exact source-backed garment/pictured-size evidence before promoting physical consistency to verified.
- Evidence: {PACKET}/PASTEL_SOURCE_RECOVERY_20260911.json; PASTEL_VISUAL_SOURCE_REVIEW_20260911.md; P3_P6_INDEPENDENT_REVIEW_20260911.md; anchor{ANCHOR}.'''
measurement_update = f'''- Current background checkpoint supersedes older shared-native directions: target Pinterest403 under another editable profile; Shopify account selection; exact shop verified but pixel read denied read_pixels. No switch/scope expansion/native fallback. Fresh denied main-tab222requests/zeroPinterest with denied marketing/analytics/preferences before and after is not worker/receiver/granted-consent/purchase acceptance. Older native conflict and cleanup uncertainty remain. {TASK} continues separate source/content work. Evidence: {PACKET}/BACKGROUND_ACCESS_20260911.json; DENIED_CONSENT_NAVIGATION_20260911.json; SHOPIFY_PIXEL_CONFIG_READBACK_20260911.md; anchor{ANCHOR}.\n\n'''
def update_problems(s):
    marker='## PROB-2026-09-09-PINTEREST-MEASUREMENT-ACCEPTANCE'
    s=insert_before(s,marker,problems)
    s=s.replace(marker+'\n\n',marker+'\n\n'+measurement_update,1)
    old='- Next: after normal shared Chrome handback, Shopify Customer events → Pinterest Test/permissions/privacy and exact Tag/CAPI comparison. Redacted provider packet prepared NOT_SENT; no payment/fake event. Paid USD15 proposal remains NOT_LAUNCH_READY and full-paid NONE unchanged.'
    new='- Next: owner-connected task-owned background Shopify Customer Events and exact Pinterest Tag/CAPI readback, with restoration and existing test-consent gates before any grant. Redacted provider packet remains NOT_SENT; no payment/fake event. Manual Sales/Pins/Checkout is the current local proposal; old USD15 traffic proposal is archived. Full-paid NONE unchanged.'
    assert old in s
    return s.replace(old,new,1)
edit('ops/PROBLEM_TRACKER.md',update_problems)

log=f'''\n\n## September11 — Pinterest continuing content batch and current account boundaries

AGENT_CONTINUITY_ANCHOR: {ANCHOR}

{summary.split(chr(10)+chr(10),1)[1]}

Current user asked to continue fixing Pinterest and creating traffic content. Root completed the independent work instead of stopping at the account gate: five additional source/illustration-based graphics, exact copy/UTM preservation, four recovered product assets, live P4/public product checks, truthful profile repair and next N1source preflight. All six Pin artifacts remain local. Product-source consistency is qualified, not physical product certification. Public-profile metadata and views are not attributable outcomes. Fresh API denied/null is not missing-pixel evidence.

Canonical interval: explicit Microsoft-to-Pinterest release received September11 after Microsoft closeout; Pinterest returns directly to root after checks. Existing parent30-minute scheduler already ACTIVE; no new automation or changed prompt. New {TASK} is the sole continuing content task in action_queue.md; the content register and ZIP are assets, not second queues. Preserved paid control, parent Google Ads pause OneOwnerAction, TA-11/20, peers, earlier cohorts, source/Pin/board repair receipts and all prior worklog bytes.

- task_entities: {TASK}, TA-12, TA-11, TA-20, advertiser549756244483, tag2620007050621, pixel22577249, P1-P6, product7536086089825, product7229023846497, product7672336646241
- task_stage: HANDOFF
- source_live_evidence_as_of: 2026-09-11 current task-owned public/profile/Shopify identity and bounded denied-consent reads; receiver remains earlier dated evidence
- live_state_mode: STALE_READBACK_REQUIRED for full paid; named bounded public observations LIVE_VERIFIED
- effective_approval_policy: current ongoing nonspend repair/content request; account identity and exact action readback required; no new paid or consent-grant authority
- approved_external_scope: NONE in unchanged full-paid control; zero external writes this continuation
- authority_context: CURRENT_USER_ONGOING_PINTEREST_NONSPEND_WORK
- decision_depends_on_uncertain_state: true
- decision_changing_evidence: correct editable account, exact destination/crop/duplicates, source-backed garment details and actual receiver/consent/purchase matching
- if_evidence_supports_recommendation: apply only reviewed profile fields and eligible unique organic Pins within capacity; record actual IDs and separate completed-date cohorts
- if_evidence_opposes_recommendation: preserve conflicting state, exclude unqualified source images, continue an independent source/creative step and hold dependent publication or paid action
- material_decision: CONTINUING_CONTENT_AND_EXACT_PROFILE_REPAIR_PREPARATION
- independent_verifier: release_verifier P4/P2-P5/P3-P6; consent_fix product sources; consent_diagnosis bounded tracking and profile copy
- verifier_independence: DID_NOT_BUILD_OR_EXECUTE
- next_action_id: READ_ONLY_MARKETING_RECONCILIATION

Single owner-facing next action: connect Dress Like Mommy in the existing task-owned background Pinterest/Shopify sessions, because wrong-profile403 and account selection block publishing and receiver inspection. While pending, continue N1real-source qualification without fabricated closeups. Continue through ops/prompts/paid-growth-ai-army-continuation-prompt.md and this anchor; do not repeat completed graphics, prior Pin/board/source writes or genuine unchanged access blockers. Validation is recorded in CONTENT_INTEGRATION_VERIFICATION_20260911.json after commands actually run.\n'''
edit('ops/AGENT_WORKLOG.md',lambda s:s+log)

control_pattern=r'<!-- MARKETING_AUTHORITATIVE_CONTROL:START -->.*?<!-- MARKETING_AUTHORITATIVE_CONTROL:END -->'
old_state,new_state=changes['ops/marketing/current_marketing_state.md']
control=re.search(control_pattern,old_state,re.S).group()
assert control==re.search(control_pattern,new_state,re.S).group()
assert sha(control)=='1e09f7d618b678bf1d534b3c9421fe1b84162c8047b37033d1270420bb098c57'
oldq,newq=changes['ops/marketing/action_queue.md']
def peer_rows(s):
    return '\n'.join(l for l in s.splitlines() if l.startswith('|') and '`TA-12`' not in l and f'`{TASK}`' not in l)
assert peer_rows(oldq)==peer_rows(newq)
oldc,newc=changes['ops/AGENT_COORDINATION.md']
def without_prefix(s,prefix):
    return ''.join(l for l in s.splitlines(True) if not l.startswith(prefix))
assert without_prefix(oldc,'| Current owner Pinterest expert audit and growth setup |')==without_prefix(newc,'| Current owner Pinterest expert audit and growth setup |')
oldo,newo=changes['ops/marketing/operator_cockpit.md']
assert without_prefix(oldo,'Pinterest checkpoint September11:')==without_prefix(newo,'Pinterest checkpoint September11:')
assert changes['ops/AGENT_WORKLOG.md'][1].startswith(changes['ops/AGENT_WORKLOG.md'][0])
result={'status':'APPLIED' if APPLY else 'DRY_RUN','recorded_at_utc':NOW,'task_id':TASK,'anchor':ANCHOR,'canonical_grant':'Explicit Microsoft release to Pinterest, September11; return to root','full_paid_control_sha256':sha(control),'protected_peer_rows_sha256':sha(peer_rows(oldq)),'protected_coordination_sha256':sha(without_prefix(oldc,'| Current owner Pinterest expert audit and growth setup |')),'protected_cockpit_and_parent_action_sha256':sha(without_prefix(oldo,'Pinterest checkpoint September11:')),'old_worklog_sha256':sha(changes['ops/AGENT_WORKLOG.md'][0]),'old_worklog_bytes':len(changes['ops/AGENT_WORKLOG.md'][0].encode()),'files':[]}
diff=[]
for rel,(old,new) in changes.items():
    assert (ROOT/rel).read_text()==old,'Concurrent modification: '+rel
    result['files'].append({'path':rel,'before_sha256':sha(old),'after_sha256':sha(new)})
    diff.extend(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile=rel,tofile=rel))
if APPLY:
    for rel,(old,new) in changes.items():
        assert (ROOT/rel).read_text()==old,'Concurrent modification: '+rel
        (ROOT/rel).write_text(new)
    for rel,(old,new) in changes.items():
        assert (ROOT/rel).read_text()==new,'After-state mismatch: '+rel
    (BASE/'CONTENT_CANONICAL_APPLY_20260911.json').write_text(json.dumps(result,indent=2)+'\n')
else:
    (BASE/'CONTENT_CANONICAL_DRY_RUN_20260911.json').write_text(json.dumps(result,indent=2)+'\n')
(BASE/'CONTENT_CANONICAL_DIFF_20260911.patch').write_text(''.join(diff))
print(json.dumps({'status':result['status'],'task_id':TASK,'files':len(changes),'protected_checks':'PASS','full_paid_control_sha256':sha(control)},indent=2))
