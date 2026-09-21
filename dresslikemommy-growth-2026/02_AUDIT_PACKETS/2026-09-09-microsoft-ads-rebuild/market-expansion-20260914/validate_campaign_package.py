"""Validate review-table joins and deployment boundaries, not live ad delivery."""
from pathlib import Path
import csv
import hashlib
import json
import re
import unicodedata
from urllib.parse import urlsplit, parse_qs

HERE = Path(__file__).resolve().parent
package = json.loads((HERE/'campaign-package.json').read_text())
checks = []

def check(name, condition):
    checks.append({'check':name,'passed':bool(condition)})

def units(text):
    return sum(2 if unicodedata.east_asian_width(c) in ('F','W') else 1 for c in text)

def normalized(text):
    return ' '.join(re.findall(r'\w+', unicodedata.normalize('NFKC', text).casefold()))

def blocked(query, negative):
    query, text = normalized(query), normalized(negative['text'])
    if negative['match_type'] == 'Exact':
        return query == text
    return f' {text} ' in f' {query} '

assets = package['assets']
blueprints = package['campaign_blueprints']
countries = package['country_coverage']
asset_index = {a['asset_set_id']:a for a in assets}
check('twenty_unique_language_sets',len(assets)==20 and len({a['locale'] for a in assets})==20)
check('korean_explicitly_held',all(a['locale']!='ko' for a in assets) and package['unsupported_language']['locale']=='ko')
check('thirty_five_unique_campaign_pairs',len(blueprints)==35 and len({(b['country_code'],b['locale']) for b in blueprints})==35)
check('sixty_five_countries_accounted_for',len(countries)==65 and len({c['country_code'] for c in countries})==65)
check('six_shopify_markets_covered',len({m for b in blueprints for m in b['shopify_market_memberships']})==6)
check('all_languages_have_blueprints',{a['locale'] for a in assets}=={b['locale'] for b in blueprints})
check('rsa_asset_count_limits',all(3<=len(a['headlines'])<=15 and 2<=len(a['descriptions'])<=4 for a in assets))
check('rsa_text_width_limits',all(all(units(t)<=30 for t in a['headlines']) and all(units(t)<=90 for t in a['descriptions']) for a in assets))
check('exact_keyword_limits',all(all(len(t)<=100 and len(t.split())<=10 for t in a['exact_keywords']) for a in assets))
check('negative_limits_and_types',all(all(n['match_type'] in ['Phrase','Exact'] and n['scope']=='Campaign' and len(n['text'])<=100 and len(n['text'].split())<=10 for n in a['negatives']) for a in assets))
conflicts=[{'locale':a['locale'],'positive':q,'negative':n['text']} for a in assets for q in a['exact_keywords'] for n in a['negatives'] if blocked(q,n)]
check('no_positive_negative_lexical_conflicts',not conflicts)
check('no_duplicate_positive_strings',all(len(a['exact_keywords'])==len({normalized(t) for t in a['exact_keywords']}) for a in assets))
check('every_campaign_binds_its_locale',all(asset_index[b['asset_set_id']]['locale']==b['locale'] for b in blueprints))
check('every_campaign_binds_dress_destination',all(b['final_url']==asset_index[b['asset_set_id']]['final_url'] and urlsplit(b['final_url']).hostname=='www.dresslikemommy.com' and urlsplit(b['final_url']).path.endswith('/collections/dresses') for b in blueprints))
check('no_numeric_budgets_or_loss_limits',all(b['daily_budget'] is None and b['test_loss_limit'] is None for b in blueprints))
check('all_intended_paused',all(b['intended_status']=='Paused' for b in blueprints))
check('no_expansion_or_broad_defaults',all(not b['broad_match'] and not b['ai_max'] and not b['url_expansion'] and not b['auto_apply_changes'] for b in blueprints))
check('presence_only_and_inherited_language',all(b['location_intent']=='People in your targeted locations' and b['campaign_language_only'] and b['ad_groups_inherit_language'] for b in blueprints))
check('existing_native_ids_preserved',{b['existing_native']['campaign_id'] for b in blueprints if b['existing_native']}=={'506254907','506254908'})
check('unconfigured_home_countries_not_targeted',not ({b['country_code'] for b in blueprints}&{'BR','IN','IL','JP','KR'}))
check('portugal_variant_gate_present',all('PORTUGAL_LANGUAGE_VARIANT_REVIEW' in b['launch_gates'] for b in blueprints if b['locale']=='pt-BR'))
check('country_coverage_does_not_authorize_launch',all(not c['launch_authorized'] and not c['shipping_and_checkout_verified'] for c in countries))
check('no_false_native_implementation_claim',all(not b['native_created_or_updated_by_this_package'] for b in blueprints))
check('all_source_hashes_match',all(hashlib.sha256((HERE/n).read_bytes()).hexdigest()==digest for n,digest in package['source_hashes'].items()))
export = list(csv.DictReader((HERE/'ads-review.csv').open()))
check('ad_review_export_has_35_rows',len(export)==35)
check('each_utm_bound_to_its_campaign',all(parse_qs(r['final_url_suffix']).get('utm_campaign')==[r['campaign_key']] for r in export))
check('export_clearly_non_bulk',all(r['table_type']=='LOCAL_REVIEW_NOT_MICROSOFT_BULK' for r in export))
report={'schema':'microsoft-campaign-package-validation.v1','status':'PASS_WITH_LIVE_GATES' if all(c['passed'] for c in checks) else 'FAIL','checks':checks,'passed':sum(c['passed'] for c in checks),'total':len(checks),'lexical_conflicts':conflicts,'limits':'Static checks do not prove semantic native matching, demand, eligibility, editorial acceptance, checkout, purchase attribution or profit.'}
(HERE/'package-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['status','passed','total','lexical_conflicts']},ensure_ascii=False))
raise SystemExit(0 if all(c['passed'] for c in checks) else 1)
