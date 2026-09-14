"""Validate the prepared source-bound packet. Never calls external systems."""
from pathlib import Path
from datetime import datetime, timezone
import csv, hashlib, html, json, re
from urllib.parse import urlparse, parse_qs
from pypdf import PdfReader

D = Path(__file__).resolve().parent
ROOT = D.parents[2]
checks = {}
def check(name, value):
    checks[name] = bool(value)
def read(name):
    return json.loads((D/name).read_text())
def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

b = read('article-before.json')
new = read('article-update-variables.json')
rollback = read('article-rollback-variables.json')
module = (D/'article-insertion.html').read_text().rstrip('\n')
candidate = (D/'article-body-proposed.html').read_text()
marker = '<h2>The Golden Rule: Coordinate, Don’t Clone</h2>'
old_timing = '<strong>Plan outfits 2 weeks ahead</strong> — don’t scramble the day before'
new_timing = '<strong>Plan around your delivery estimate</strong> — check the estimate for your destination and allow time to try on outfits before the photo session'
expected = b['body'].replace(marker,module+'\n\n'+marker).replace(old_timing,new_timing)
check('article_exact_id', b['id'] == new['id'] == rollback['id'] == 'gid://shopify/Article/559471919201')
check('one_body_field_only', set(new) == {'id','article'} and set(new['article']) == {'body'})
check('before_is_published', b['isPublished'] is True)
check('unique_insertion_anchor', b['body'].count(marker) == 1)
check('unique_timing_correction', b['body'].count(old_timing) == 1)
check('only_two_reviewed_body_changes', new['article']['body'] == candidate == expected)
check('review_artifact_byte_identical_to_payload', (D/'article-body-proposed.html').read_bytes() == new['article']['body'].encode('utf-8'))
check('rollback_exact', rollback == {'id':b['id'],'article':{'body':b['body']}})
check('internal_links_untagged', 'utm_' not in candidate)
check('no_insertion_script_or_placeholder', not re.search(r'<script|localhost|127\.0\.0|\[[A-Z_ ]+\]|1688|alibaba',module,re.I))
check('sold_separately_disclosure', 'each mother or daughter dress is sold separately' in module)
tr = read('article-translations-before.json')
check('translation_impact_count', tr['total_rows'] == 36 and tr['body_translations'] == 17)
check('translation_initial_flags_recorded', all(r['outdated'] is False for r in tr['rows']))
pin = read('pins.json')['pins']
check('six_distinct_pin_drafts', len(pin) == 6 and len({p['id'] for p in pin}) == 6)
check('six_distinct_tracking_links', len({p['tracking_url'] for p in pin}) == 6)
check('pin_title_and_description_lengths', all(len(p['title']) <= 100 and len(p['description']) <= 500 for p in pin))
check('pin_status_is_unpublished', all(p['status'] == 'COPY_READY_NOT_PUBLISHED' for p in pin))
for p in pin:
    u = urlparse(p['tracking_url']); q = parse_qs(u.query)
    check(p['id']+'_correct_domain_and_tracking', u.scheme == 'https' and u.netloc == 'www.dresslikemommy.com' and q == {'utm_source':['pinterest'],'utm_medium':['social'],'utm_campaign':['organic_202609'],'utm_content':[p['id'].lower()]})
check('no_held_skyfade_promotion', all('skyfade' not in p['destination'].lower() for p in pin) and 'skyfade' not in module.lower())
baseline=read('shopify_baseline.json')['reports']
f=list(map(float,baseline['funnel']['rows'][0]))
check('conversion_decimal_reconciles', abs(f[4] - f[3]/f[0]) < 1e-12)
check('funnel_nests', f[0]>=f[1]>=f[2]>=f[3])
check('device_sessions_reconcile',sum(int(r[1]) for r in baseline['devices']['rows'])==4896)
check('device_completions_reconcile',sum(int(r[3]) for r in baseline['devices']['rows'])==10)
check('session_source_top15_tail_known',4896-sum(int(r[2]) for r in baseline['session_referrers_top15']['rows'])==7)
check('country_top12_tail_known',4896-sum(int(r[1]) for r in baseline['session_countries_top12']['rows'])==750)
check('sales_referral_money_reconciles',round(sum(float(r[3]) for r in baseline['order_referrers']['rows']),2)==847.42)
check('sales_components_reconcile',round(sum(float(x) for x in baseline['sales']['rows'][0][1:4]),2)==821.44 and round(821.44+25.98,2)==847.42)
cal=list(csv.DictReader((D/'calendar.csv').open()))
check('calendar_no_additional_distribution_spend',all(r['extra_distribution_budget_usd']=='0' for r in cal))
check('calendar_all_pins_once', all(sum(r['asset']==p['id'] for r in cal)==1 for p in pin))
check('calendar_new_pins_wait_for_sunshine', all('Sunshine completed' in r['dependency'] for r in cal if r['asset'] in {p['id'] for p in pin}))
check('calendar_three_pin_weekly_cap_includes_sunshine', sum(r['channel']=='Pinterest' and (r['day']=='1-3' or (r['day'].isdigit() and int(r['day'])<=7)) for r in cal)<=3 and sum(r['channel']=='Pinterest' and r['day'].isdigit() and 8<=int(r['day'])<=14 for r in cal)<=3)
pdf=ROOT/'output/pdf/family-photo-outfit-planner.pdf'
r=PdfReader(pdf); text='\n'.join(p.extract_text() or '' for p in r.pages)
links=[str(a.get_object().get('/A',{}).get('/URI','')) for p in r.pages for a in p.get('/Annots',[])]
check('pdf_one_readable_page',len(r.pages)==1 and 'Family photo outfit planner' in text)
check('pdf_two_correct_destination_links',len(links)==2 and all(urlparse(u).netloc=='www.dresslikemommy.com' and parse_qs(urlparse(u).query).get('utm_medium')==['referral'] for u in links))

# Display-only preview, independent of the mutation payload and live theme.
preview_body=candidate.replace('href="/','href="https://www.dresslikemommy.com/')
css='body{margin:0;background:#faf7f4;color:#292529;font:17px/1.65 system-ui,sans-serif}main{max-width:820px;margin:auto;padding:32px 22px}aside{padding:16px;background:#f1e4e7;border-left:4px solid #895363;font-size:14px}h1{font-size:32px;line-height:1.2}h2{font-size:24px;line-height:1.3;margin-top:36px}h3{font-size:19px}a{color:#7b3f55;overflow-wrap:anywhere}li{margin:10px 0}ol,ul{padding-left:24px}*{box-sizing:border-box}'
preview='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Local review - family-photo guide</title><style>'+css+'</style><main><aside>LOCAL REVIEW - NOT PUBLISHED<br>Existing article 559471919201. One buying section plus a delivery-planning correction. This preview does not simulate the live theme.</aside><h1>'+html.escape(b['title'])+'</h1>'+preview_body+'</main></html>'
(D/'article-review.html').write_text(preview)
hashes={p.name:digest(p) for p in sorted(D.iterdir()) if p.is_file() and p.name not in {'verification.json','review.md'}}
hashes[str(pdf.relative_to(ROOT))]=digest(pdf)
result={'checked_at_utc':datetime.now(timezone.utc).isoformat(),'checks':checks,'passed':sum(checks.values()),'failed':[k for k,v in checks.items() if not v],'sha256':hashes,'external_mutations':0,'publication_status':'NOT_RUN_AWAITING_EXACT_APPROVAL','graphql_schema_validation':'Connector passed source query, translations query and proposed mutation in this task','pdf_visual_review':'Root inspected final Poppler render at /private/tmp/dlm-family-planner-preview.png; no clipping or missing glyphs','render_note':'Initial Poppler lacked writable fontconfig cache; stopped. PyMuPDF unavailable. Poppler rerun passed with temporary fontconfig pointing to system fonts and /private/tmp cache.'}
(D/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'passed':result['passed'],'failed':result['failed'],'pdf_pages':len(r.pages),'pin_drafts':len(pin),'article_extra_words':len(re.sub('<[^>]+>',' ',module).split())}))
raise SystemExit(0 if all(checks.values()) else 1)
