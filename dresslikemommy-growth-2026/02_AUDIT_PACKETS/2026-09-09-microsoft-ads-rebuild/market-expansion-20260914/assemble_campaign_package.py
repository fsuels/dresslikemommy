"""Build review tables only. No network, upload, native budget or account mutations."""
from pathlib import Path
import csv
import hashlib
import json
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent
BASE = HERE.parent

def read_json(name):
    return json.loads((HERE / name).read_text())

def read_csv(name):
    return list(csv.DictReader((BASE / name).open()))

def save_json(name, data):
    (HERE / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')

def save_csv(name, rows):
    with (HERE / name).open('w', newline='') as output:
        writer = csv.DictWriter(output, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

inventory = read_json('market-language-inventory.json')
native = read_json('native-creation-readback.json')
english = read_json('english-master-assets.json')
additional = read_json('localized-assets-missing.json')
legacy_negatives = read_json('legacy-negative-profiles.json')
sessions = read_json('market-session-evidence.json')
campaigns = read_csv('campaigns.csv')
groups = {r['ad_group_key']: r for r in read_csv('ad_groups.csv')}
ads = read_csv('responsive_search_ads.csv')
keywords = read_csv('keywords.csv')
campaign_index = {r['campaign_key']: r for r in campaigns}
language_index = {r['locale']: r for r in inventory['languages']}
extra_index = {r['locale']: r for r in additional['locales']}
negative_rows = legacy_negatives['profiles']
negative_index = {r['locale']: r for r in negative_rows}
library = []

for locale, info in language_index.items():
    if locale == 'ko':
        continue
    source_group = None
    if locale == 'en':
        h = [r['text'] for r in english['headlines']]
        d = [r['text'] for r in english['descriptions']]
        k = [r['text'] for r in english['exact_keywords']]
        n = [{key: r[key] for key in ['text', 'match_type', 'scope', 'rationale']} for r in english['negative_profile']]
        source = 'english-master-assets.json'
    elif locale in extra_index:
        row = extra_index[locale]
        h, d, k = row['headlines'], row['descriptions'], row['keywords']
        n = [{'text': text, 'match_type': 'Phrase', 'scope': 'Campaign', 'rationale': 'Localized non-shopping-intent candidate; query and semantic review still apply.'} for text in row['negatives']]
        source = 'localized-assets-missing.json'
    else:
        row = next(r for r in ads if campaign_index[r['campaign_key']]['shopify_locale'] == locale and groups[r['ad_group_key']]['intent'] == 'dresses')
        source_group = row['ad_group_key']
        h = [row[f'headline_{i}'] for i in range(1, 9)]
        d = [row[f'description_{i}'] for i in range(1, 4)]
        k = [r['keyword'] for r in keywords if r['ad_group_key'] == source_group and r['match_type'] == 'Exact']
        n = negative_index[locale]['negatives']
        source = '../responsive_search_ads.csv + ../keywords.csv + legacy-negative-profiles.json'
    library.append({
        'asset_set_id': 'dresses_' + locale.lower().replace('-', '_'),
        'locale': locale, 'language': info['name'],
        'microsoft_language': info['microsoft_language_name'],
        'microsoft_language_code': info['microsoft_language_code'],
        'native_language_option_observed': True,
        'native_language_saved': False,
        'headlines': h, 'descriptions': d,
        'exact_keywords': k, 'negatives': n,
        'final_url': info['dress_landing_url'],
        'destination_evidence': info['landing_status'],
        'rendered_checkout_verified': False,
        'source': source, 'legacy_source_group': source_group,
        'copy_review': 'AI_REVIEW_NOT_HUMAN_NATIVE_SPEAKER_CERTIFICATION',
        'variant_gate': 'PORTUGAL_REVIEW_REQUIRED_FOR_BRAZILIAN_COPY_AND_STOREFRONT' if locale == 'pt-BR' else None,
        'observed_language_search_volume': None, 'observed_microsoft_cpc': None,
        'observed_microsoft_cpa': None, 'intended_status': 'Paused',
        'native_implementation': 'NOT_APPLIED_FROM_THIS_PACKAGE',
    })

assets = {r['locale']: r for r in library}
countries = {r['country_code']: r for r in inventory['countries']}
session_rows = {r[0]: r for r in sessions['countries']['rows']}
aliases = {'Bahamas': 'Bahamas', 'Czechia': 'Czechia'}
blueprints = []
pairs = [(c['country_code'], c['shopify_locale']) for c in campaigns]
pairs += [('GB','en'),('CA','en'),('CA','fr'),('AT','de'),('BE','nl'),('BE','fr'),
          ('GR','el'),('FI','fi'),('NO','no'),('PL','pl'),('PT','pt-BR'),('SE','sv'),
          ('US','ar'),('US','he'),('US','hi'),('US','ja'),('US','ru'),
          ('NZ','en'),('IE','en'),('CH','de'),('CH','fr'),('CH','it'),('MX','es'),('SV','es')]
assert len(pairs) == len(set(pairs))
old_pairs = {(c['country_code'], c['shopify_locale']): c for c in campaigns}
native_existing = {('US','en'): {'campaign_id':'506254907','ad_group_id':'1272136755587035','ad_id':'79508657389070'},
                   ('DE','de'): {'campaign_id':'506254908','ad_group_id':'1262241151661314','ad_id':'78890182372245'}}

for country, locale in pairs:
    old = old_pairs.get((country, locale))
    key = old['campaign_key'] if old else f'ms_{country.lower()}_{locale.lower().replace("-", "_")}_202609'
    a, c = assets[locale], countries[country]
    s = session_rows.get(aliases.get(c['country_name'], c['country_name']))
    stage = 'RESERVE_REQUIRE_DEMAND_AND_ECONOMICS'
    if (country, locale) in native_existing:
        stage = 'PRESERVE_EXISTING_PAUSED_BASELINE'
    elif (country, locale) in [('DK','da'),('CZ','cs'),('GB','en'),('CA','en'),('AT','de')]:
        stage = 'NEXT_CANDIDATE_AFTER_MEASUREMENT_AND_BUDGET'
    elif country == 'US':
        stage = 'LANGUAGE_AUDIENCE_HYPOTHESIS_NOT_MEASURED'
    gates = ['NUMERIC_BUDGET_AND_TEST_LOSS', 'SUPPORTED_CONSENT_REPAIR', 'EXACT_PURCHASE_RECEIVER_AND_DEDUP', 'ACTUAL_CONTRIBUTION_ECONOMICS', 'COUNTRY_LANGUAGE_LANDING_CHECKOUT', 'NATIVE_TARGET_AND_EDITORIAL_READBACK', 'NATIVE_URL_TEST_AND_EFFECTIVE_AUTOTAG_VALUE_MAPPING']
    if locale == 'pt-BR':
        gates.append('PORTUGAL_LANGUAGE_VARIANT_REVIEW')
    if country in ['MX']:
        gates.append('USE_COUNTRY_REGION_MATCH_NOT_VERACRUZ_NEIGHBORHOOD')
    blueprint = {
        'campaign_key': key,
        'campaign_name': old['campaign_name'] if old else f'DLM | MS | {country} | {a["microsoft_language_code"]} | Search | 202609',
        'country_code': country, 'country_name': c['country_name'],
        'shopify_market_memberships': [r['market_name'] for r in c['active_market_memberships']],
        'locale': locale, 'language': a['microsoft_language'],
        'asset_set_id': a['asset_set_id'], 'final_url': a['final_url'],
        'phase': stage, 'intended_status': 'Paused',
        'existing_native': native_existing.get((country, locale)),
        'existing_native_policy': 'PRESERVE_IDS_AND_FULL_ASSET_ARRAYS_RECONCILE_BEFORE_ADDING',
        'daily_budget': None, 'test_loss_limit': None,
        'cpc_ceiling_usd': 0.15, 'cap_is_available_for_new_campaign': 'VERIFY_AT_SAVE',
        'bid_strategy_candidate': 'MaxClicks_only_if_current_native_hard_cap_supported_and_authorized',
        'location_intent': 'People in your targeted locations',
        'campaign_language_only': True, 'ad_groups_inherit_language': True,
        'initial_match_type': 'Exact', 'broad_match': False, 'ai_max': False,
        'url_expansion': False, 'auto_apply_changes': False,
        'distribution': 'VERIFY_NARROWEST_AVAILABLE_NO_BING_ONLY_CLAIM',
        'negative_application_scope': 'Campaign',
        'session_diagnostic': None if s is None else {'sessions': int(s[1]), 'completed_checkout_sessions': int(s[4]), 'scope': 'ALL_CHANNEL_NOT_LANGUAGE_OR_MICROSOFT_ATTRIBUTION'},
        'native_created_or_updated_by_this_package': False,
        'launch_gates': gates,
    }
    blueprints.append(blueprint)

coverage = []
for code, country in countries.items():
    s = session_rows.get(country['country_name'])
    linked = [b for b in blueprints if b['country_code'] == code]
    geo_gate = 'EXACT_NATIVE_COUNTRY_TARGET_NOT_SAVED_FROM_THIS_PACKAGE'
    if code in ['US', 'DE']:
        geo_gate = 'EXISTING_BASELINE_TARGET_PREVIOUSLY_SAVED_REVERIFY_BEFORE_PACKAGE_ACTION'
    if code in ['AX','BL','PM','TC','TF','WF','XK']:
        geo_gate = 'BULK_NAME_NOT_FOUND_REQUIRE_PRECISE_NATIVE_RESOLUTION'
    elif code in ['MF','RE']:
        geo_gate = 'BULK_NAME_WRONG_PLACE_DO_NOT_APPLY'
    elif code in ['LU','SM']:
        geo_gate = 'BULK_MATCH_TARGET_LEVEL_AMBIGUOUS'
    elif code == 'MX':
        geo_gate = 'EXACT_COUNTRY_OPTION_OBSERVED_NEIGHBORHOOD_BULK_MATCH_REJECTED'
    if code == 'RU':
        geo_gate = 'CURRENT_MICROSOFT_AD_DELIVERY_UNVERIFIED_NO_RUSSIA_LAUNCH'
    coverage.append({
        'country_code': code, 'country_name': country['country_name'],
        'shopify_markets': '; '.join(r['market_name'] for r in country['active_market_memberships']),
        'configured': True, 'campaign_blueprints': '; '.join(b['campaign_key'] for b in linked),
        'prepared_language_candidates': '; '.join(b['locale'] for b in linked),
        'status': 'LOCAL_CAMPAIGN_CANDIDATES_GATED' if linked else 'COVERAGE_RECORDED_TARGET_LANGUAGE_AND_DEMAND_NOT_YET_QUALIFIED',
        'native_geo_gate': geo_gate, 'shipping_and_checkout_verified': False,
        'session_count': None if s is None else int(s[1]),
        'completed_checkout_sessions': None if s is None else int(s[4]),
        'session_scope': 'ALL_CHANNEL_2026_06_16_TO_2026_09_13_NOT_PAID_ORDERS',
        'launch_authorized': False,
    })

source_names = ['market-language-inventory.json','native-creation-readback.json','localized-assets-missing.json','english-master-assets.json','legacy-negative-profiles.json','market-session-evidence.json','strategy-controls.json']
package = {
    'schema': 'microsoft-all-market-review-package.v1',
    'prepared_at_utc': datetime.now(timezone.utc).isoformat(),
    'status': 'LOCAL_BUILD_NATIVE_CREATION_BLOCKED_PENDING_NUMERIC_BUDGET',
    'account_id': '477439', 'customer_id': '770182',
    'user_intent': 'Create expert U.S. and international campaigns for supported languages with negative keywords and low acquisition cost.',
    'authorization': {'local_preparation': True, 'current_campaign_creation_intent': True, 'numeric_campaign_budget': None, 'numeric_test_loss': None, 'new_campaign_save': False, 'spend_or_enablement': False},
    'assets': library, 'campaign_blueprints': blueprints, 'country_coverage': coverage,
    'unsupported_language': {'locale':'ko','language':'Korean','reason':'Absent from freshly observed native Search language selector; no Korean native campaign prepared.'},
    'market_coverage': 'All six active Shopify markets inventoried; all 65 configured countries accounted for. Campaign candidates are deliberately not a launch-everywhere recommendation.',
    'source_hashes': {name:hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in source_names},
    'operating_rules': [
        'Concentrate a funded test on a small number of qualified country-language cohorts; do not start all 35 at once.',
        'Preserve existing US and DE native IDs; reconcile before adding assets or keywords to avoid duplication.',
        'Manual UTM suffixes are proposed values. Existing native automatic tagging can replace them; run native URL Test and record effective campaign/adgroup mappings before attribution analysis.',
        'Treat exact keywords as intent candidates with close-variant overlap, not measured separate demand pools.',
        'Review negatives against positive phrases and plausible product queries; avoid broad garment, age, price or gifting exclusions.',
        'Review actual search terms and distribution after meaningful volume, respecting attribution lag; cheap clicks are diagnostic only.',
        'Do not promote MaxConversions or target ROAS until genuine purchase value, consent, duplication and data sufficiency are demonstrated.',
        'Daily budget is not a hard lifetime spend cap; any future cash and loss stop needs explicit authority and monitoring.',
        'Calculate allowable CPA from actual retained order contribution less required profit and approved acquisition allowance; unknown inputs remain unknown.',
        'Do not infer Brazil, India, Israel, Japan or Korea shipping from language availability.',
        'Pause/scale decisions require exact current paid authority, before/after evidence and purchase/economics checks.',
    ],
    'business_outcome': {'verified_new_native_campaigns':0,'verified_new_paid_sales':None,'verified_profit_increase':None},
}
save_json('campaign-package.json', package)
save_csv('country-coverage.csv', coverage)
campaign_export, ad_export, keyword_export, negative_export = [], [], [], []
for b in blueprints:
    a = assets[b['locale']]
    campaign_export.append({k:b[k] for k in ['campaign_key','campaign_name','country_code','locale','phase','intended_status','daily_budget','test_loss_limit','cpc_ceiling_usd','location_intent','initial_match_type','final_url']})
    ad = {'campaign_key':b['campaign_key'],'asset_set_id':a['asset_set_id'],'ad_group':'Mother Daughter | Matching Dresses','intended_status':'Paused','native_ad_id':(b['existing_native'] or {}).get('ad_id',''),'final_url':a['final_url'],'final_url_suffix':f'utm_source=bing&utm_medium=cpc&utm_campaign={b["campaign_key"]}&utm_content={b["campaign_key"]}_dresses_rsa_1','suffix_evidence':'PROPOSED_MANUAL_VALUES_NATIVE_AUTOTAGGING_CAN_REPLACE_REQUIRE_URL_TEST','table_type':'LOCAL_REVIEW_NOT_MICROSOFT_BULK'}
    ad.update({f'headline_{i+1}': a['headlines'][i] if i < len(a['headlines']) else '' for i in range(15)})
    ad.update({f'description_{i+1}': a['descriptions'][i] if i < len(a['descriptions']) else '' for i in range(4)})
    ad_export.append(ad)
    keyword_export += [{'campaign_key':b['campaign_key'],'locale':b['locale'],'keyword':text,'match_type':'Exact','intended_status':'Paused','final_url':a['final_url'],'native_action':'RECONCILE_EXISTING_IDS_FIRST'} for text in a['exact_keywords']]
    negative_export += [{'campaign_key':b['campaign_key'],'locale':b['locale'],'negative_keyword':n['text'],'match_type':n['match_type'],'scope':n['scope'],'action':'LOCAL_REVIEW_ONLY_RECONCILE_EXISTING','rationale':n['rationale']} for n in a['negatives']]
save_csv('campaigns-review.csv',campaign_export)
save_csv('ads-review.csv',ad_export)
save_csv('keywords-review.csv',keyword_export)
save_csv('negatives-review.csv',negative_export)
print(json.dumps({'language_asset_sets':len(library),'campaign_blueprints':len(blueprints),'countries_accounted_for':len(coverage),'countries_with_blueprints':len(set(b['country_code'] for b in blueprints)),'rsa_rows':len(ad_export),'keyword_rows':len(keyword_export),'negative_rows':len(negative_export),'unique_headlines':sum(len(a['headlines']) for a in library),'unique_descriptions':sum(len(a['descriptions']) for a in library),'unique_keyword_candidates':sum(len(a['exact_keywords']) for a in library),'unique_negative_candidates':sum(len(a['negatives']) for a in library),'native_mutations':0},indent=2))
