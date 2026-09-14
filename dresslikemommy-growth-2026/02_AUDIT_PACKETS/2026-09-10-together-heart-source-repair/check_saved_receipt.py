"""Read-only checks of this packet's real Shopify receipts; never connects or writes Shopify."""
import copy
import hashlib
import json
import sys
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT/'ops'/'scripts'))
from ops.scripts.poll_shopify_product_translations import ExistingTranslation, ResourceSnapshot
from ops.scripts.repair_localized_product_size_charts import audit_product as coverage_audit
from ops.scripts.audit_localized_size_chart_variant_mapping import variant_matches_table, size_and_type_options
from ops.scripts.audit_shopify_product_translation_completeness import audit_product_snapshots
from ops.scripts.repair_localized_product_size_charts import product_snapshot

PACKET = Path(__file__).resolve().parent
before = json.loads((PACKET/'before.json').read_text())
after = json.loads((PACKET/'after.json').read_text())
plan = json.loads((PACKET/'plan.json').read_text())
checks = {}
checks['shop_identity'] = after['source']['shop'] == before['source']['shop']
checks['locales_preserved'] = after['source']['shopLocales'] == before['source']['shopLocales']
old_product = before['source']['product']
product = after['source']['product']
untouched = lambda p: {k:v for k,v in p.items() if k not in ('descriptionHtml','updatedAt')}
checks['all_returned_nonbody_product_fields_preserved'] = untouched(product) == untouched(old_product)
checks['variants98_preserved_complete'] = len(product['variants']['nodes']) == 98 and not product['variants']['pageInfo']['hasNextPage'] and product['variants'] == old_product['variants']
checks['publications_preserved_complete'] = not product['resourcePublications']['pageInfo']['hasNextPage'] and product['resourcePublications'] == old_product['resourcePublications']
old_source = before['source']['translatableResource']['translatableContent']
source = after['source']['translatableResource']['translatableContent']
checks['other_source_values_and_digests_preserved'] = [x for x in source if x['key']!='body_html'] == [x for x in old_source if x['key']!='body_html']
expected = {r['locale']:r for r in plan['rows']}
bodies = {'en':product['descriptionHtml']}
nonbody_count = 0
translations = {}
for alias,locale in before['locale_alias_map'].items():
    old = before['translations']['translatableResource'][alias]
    new = after['translations']['translatableResource'][alias]
    old_other = [x for x in old if x['key']!='body_html']
    new_other = [x for x in new if x['key']!='body_html']
    checks['nonbody_translation_preserved_'+locale] = old_other == new_other
    nonbody_count += len(new_other)
    body = [x for x in new if x['key']=='body_html']
    checks['body_row_current_'+locale] = len(body)==1 and body[0]['outdated'] is False
    bodies[locale] = body[0]['value']
    for row in new:
        translations[(locale,row['key'])] = ExistingTranslation(**row)
checks['nonbody_translation_count80'] = nonbody_count == 80
checks['full_parent_translation_count100'] = len(translations) == 100
for locale,body in bodies.items():
    checks['exact_body_'+locale] = body == expected[locale]['after_body']
    old_rows = BeautifulSoup(expected[locale]['before_body'],'html.parser').select('table tbody tr')
    rows = BeautifulSoup(body,'html.parser').select('table tbody tr')
    checks['table14rows_'+locale] = len(rows)==len(old_rows)==14
    values = [[c.get_text() for c in r.select('td')] for r in rows]
    old_values = [[c.get_text() for c in r.select('td')] for r in old_rows]
    checks['hip_waist28unavailable_'+locale] = all(len(v)==10 and v[7]==v[8]=='—' for v in values)
    checks['other112table_cells_preserved_'+locale] = all(all(a[i]==b[i] for i in range(10) if i not in (7,8)) for a,b in zip(values,old_values))

snapshot = ResourceSnapshot(resource_id=product['id'],resource_type='PRODUCT',translatable_content=source,existing_translations=translations)
class SavedReceiptReader:
    def fetch_resource(self,resource_id,locales,max_nested):
        assert resource_id==product['id']
        return snapshot
    def register_translations(self,*args,**kwargs):
        raise AssertionError('Read-only receipt review forbids registration')

locales=list(before['locale_alias_map'].values())
coverage=coverage_audit(SavedReceiptReader(),product,locales,execute=False,pause_ms=0,force_rebuild_size_chart_tables=False)
checks['canonical_coverage_zero_missing_planned_errors'] = coverage['missing_locales']==[] and coverage['planned_translation_count']==0 and coverage['errors']==[]
checks['canonical_coverage20'] = len(coverage['already_ok_locales'])==20
size_name,type_name=size_and_type_options(product)
unmatched=[]
for locale in locales:
    for variant in product['variants']['nodes']:
        ok,reason=variant_matches_table(variant,size_name,type_name,bodies[locale])
        if not ok: unmatched.append({'locale':locale,'variant_id':variant['id'],'reason':reason})
checks['variant_locale1960_no_unmatched'] = len(locales)*len(product['variants']['nodes'])==1960 and not unmatched
issues,counters=audit_product_snapshots(product_snapshot(product),[snapshot],locales,max_snippets_per_body=20)
checks['parent_translation_completeness_no_issues'] = not issues
report={'source':'Separate real Shopify query receipts saved in after.json; no live request or production mutation from this verifier.','after_sha256':hashlib.sha256((PACKET/'after.json').read_bytes()).hexdigest(),'checks':checks,'checks_passed':sum(checks.values()),'checks_total':len(checks),'coverage':coverage,'variant_locale_checks':1960,'unmatched':unmatched,'parent_translation_counters':counters,'parent_translation_issues':issues,'scope_limit':'Parent resource fields and all98variant row mappings only. No forced full-product refresh or claimed re-audit of840nested translation slots. Force-rebuild helper is not used because it moves tables/adds comments; explicit exact cell equality supplements its standard coverage check.'}
(PACKET/'after_checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'passed':report['checks_passed'],'total':report['checks_total'],'failures':[k for k,v in checks.items() if not v],'coverage':[len(coverage['missing_locales']),coverage['planned_translation_count'],len(coverage['errors'])],'variant_locale_checks':1960,'unmatched':len(unmatched),'translation_issues':len(issues)}))
assert all(checks.values()), 'Saved receipt verification failed; do not claim completion.'
