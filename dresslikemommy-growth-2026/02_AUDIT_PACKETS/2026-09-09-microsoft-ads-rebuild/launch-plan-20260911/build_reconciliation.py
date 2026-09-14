"""Build a local, non-executable launch contract from frozen read-only receipts."""
from pathlib import Path
from decimal import Decimal, ROUND_DOWN
import csv
import datetime
import hashlib
import json

HERE = Path(__file__).resolve().parent
PACKET = HERE.parent
REPO = PACKET.parents[2]
ATTACHMENT = Path('/Users/fsuels/.codex/attachments/fcad2a44-3b3a-4a26-a400-6fc7e03183a9/pasted-text.txt')
D = Decimal
CENT = D('0.01')

def read(name):
    return json.loads((HERE / name).read_text())

def object_row(table, row):
    return dict(zip([c['name'] for c in table['columns']], row))

def money(value):
    return str(value.quantize(CENT, rounding=ROUND_DOWN))

analytics = read('analytics_readback.json')
catalog = read('shopify_candidate_readback.json')['data']
aug = object_row(analytics['august_sales'], analytics['august_sales']['rows'][0])
sessions = object_row(analytics['preceding_90_complete_day_sessions'], analytics['preceding_90_complete_day_sessions']['rows'][0])
countries = [object_row(analytics['country_sessions'], r) for r in analytics['country_sessions']['rows']]
assert sum(int(r['sessions']) for r in countries) == int(sessions['sessions'])
assert sum(int(r['sessions_that_completed_checkout']) for r in countries) == int(sessions['sessions_that_completed_checkout'])
assert D(aug['gross_sales']) + D(aug['discounts']) + D(aug['sales_reversals']) == D(aug['net_sales'])
assert D(aug['net_sales']) + D(aug['shipping_charges']) + D(aug['taxes']) == D(aug['total_sales'])
assert catalog['shop']['myshopifyDomain'] == 'dresslikemommy-com.myshopify.com'
assert catalog['shop']['currencyCode'] == 'USD'
assert not catalog['markets']['pageInfo']['hasNextPage']
for key in ('coral', 'sunshine'):
    assert not catalog[key]['variants']['pageInfo']['hasNextPage']

def variant(key, title):
    found = [v for v in catalog[key]['variants']['nodes'] if v['title'] == title]
    assert len(found) == 1
    return found[0]

child_dress = variant('coral', 'Child 4 Years / Coral Blossom')
mother_dress = variant('coral', 'Mother S / Coral Blossom')
child_tee = variant('sunshine', 'Child 2 Years / Sunshine Stripe')
adult_tee = variant('sunshine', 'Adult S / Sunshine Stripe')
cases = [
    ('Coral child dress, one piece', [child_dress]),
    ('Coral mother dress, one piece', [mother_dress]),
    ('Coral mother + child, two separate pieces', [mother_dress, child_dress]),
    ('Sunshine child tee, one piece', [child_tee]),
    ('Sunshine adult tee, one piece', [adult_tee]),
    ('Sunshine adult + child, two separate pieces', [adult_tee, child_tee]),
]
scenarios = []
for label, variants in cases:
    revenue = sum((D(v['price']) for v in variants), D(0))
    ratio_cap = min(revenue * D('0.15'), revenue / D('6.67'))
    rounded_cap = D(money(ratio_cap))
    scenarios.append({
        'basket': label,
        'currency': 'USD',
        'pieces': len(variants),
        'merchandise_revenue_before_any_discount_or_refund': money(revenue),
        'ratio_only_cac_ceiling': money(ratio_cap),
        'required_cvr_at_0_15_cpc_percent': str((D('0.15') / rounded_cap * 100).quantize(D('0.0001'))),
        'actual_contribution': None,
        'approved_allowable_cac': None,
        'supplier_stock_verified': False,
        'microsoft_offer_ids': None,
        'shopify_variant_ids': [v['id'] for v in variants],
        'interpretation': 'Arithmetic scenario only; not expected AOV, actual margin, campaign forecast or approved cohort',
    })

formula = {
    'R': 'Merchandise after discounts/refunds, excluding tax and shipping charges',
    'S': 'Shipping charges actually retained',
    'K': 'Disjoint actual net product cost, payment fees, fulfillment/outbound freight, return handling and other variable costs',
    'C': 'R + S - K',
    'allowable_cac': 'min(0.15 * R, R / 6.67, C - 0.30 * R); reject nonpositive; unknown C means unknown actual allowable CAC',
    'refund_rule': 'Subtract merchandise refunds once; reconcile reserves with actual outcomes; apply supplier credits only when evidenced',
    'allocation_rule': 'Remaining Microsoft allocation needs an explicit period, owner cash/loss limits and all other marketing commitments; unknown inputs remain null',
    'rounding_rule': 'Money ceilings rounded DOWN to whole cents; displayed CVR uses that rounded ceiling',
}
us = next(r for r in countries if r['session_country'] == 'United States')
economics = {
    'as_of_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'revenue_definition': formula,
    'rule_provenance': {
        'historical_file': '2026-04-29-shopify-margin-cac-export-pack/operating_rules.csv',
        'historical_model': 'summary.json marketing_cap_rate0.1500 / target_roas_floor6.6667; cost assumption0.50',
        'current_user_research': '15% total marketing and6.67 ROAS retained as conservative planning constraints; not activation authority',
        'canonical': 'about6.5 ROAS and30% retained-profit objective; stricter6.67 used in this local plan only',
        'cost_conflict': 'Older rule labels50% all-in nonmarketing; field_map calls unitCost50%. Neither is invoice-backed landed-cost truth. Do not add overlapping modeled and actual costs.',
    },
    'august_all_marketing_illustration': {
        'sales_window': '2026-08-01 through2026-08-31, America/New_York',
        'net_merchandise': aug['net_sales'],
        'rate': '0.15',
        'exact_envelope': str(D(aug['net_sales']) * D('0.15')),
        'cents_floor': money(D(aug['net_sales']) * D('0.15')),
        'other_marketing_commitments': None,
        'approved_test_cash': None,
        'approved_test_loss': None,
        'remaining_microsoft_budget': None,
        'limitation': 'Past-August sensitivity illustration, not September allowance or owner-approved budget',
    },
    'session_reconciliation': {
        'window': '2026-06-12 through2026-09-09 inclusive,90complete dates',
        'country_rows': len(countries),
        'country_totals_reconcile': True,
        'overall_cvr_percent': str((D(sessions['sessions_that_completed_checkout']) / D(sessions['sessions']) * 100).quantize(D('0.0001'))),
        'us_cvr_percent': str((D(us['sessions_that_completed_checkout']) / D(us['sessions']) * 100).quantize(D('0.0001'))),
        'limitation': 'Session outcomes are not paid-order/customer counts. These mixed-source rates are not Microsoft forecasts. Tiny country numerators do not rank profitable markets.',
    },
    'basket_scenarios': scenarios,
}
(HERE / 'economics.json').write_text(json.dumps(economics, indent=2) + '\n')
with (HERE / 'basket_economics.csv').open('w', newline='') as f:
    columns = ['basket','currency','pieces','merchandise_revenue_before_any_discount_or_refund','ratio_only_cac_ceiling','required_cvr_at_0_15_cpc_percent','actual_contribution','approved_allowable_cac']
    writer = csv.DictWriter(f, fieldnames=columns, extrasaction='ignore')
    writer.writeheader()
    writer.writerows(scenarios)

contract = {
    'schema': 'dlm.microsoft.local_launch_contract.v1',
    'decision_id': 'DLM-DEC-2026-09-11-MICROSOFT-LAUNCH-RECONCILIATION',
    'status': 'NO_GO_FOR_ACTIVATION__LOCAL_REVIEW_ONLY',
    'not_a_microsoft_import_file': True,
    'user_research': {'path':str(ATTACHMENT),'sha256':hashlib.sha256(ATTACHMENT.read_bytes()).hexdigest(),'research_date':'2026-09-10'},
    'existing_account': {'account_id':'477439','customer_id':'770182','uet_id':'36005151','app_pixel_id':'931561569','current_native_readback':False,'microsoft_merchant_store_id':None,'catalog_id':None,'primary_purchase_goal_id':None},
    'history': 'Dated September6/9 account evidence and Smart163000100 exclusion preserved; account is not assumed new or history-free',
    'selected_first_market': {'country':'US','language':'en','currency':'USD','status':'PRIMARY_PREPARATION_CANDIDATE_NOT_APPROVED_ACTIVATION'},
    'selection': {
        'first_paid_campaign_type': None,
        'maximum_simultaneous_initial_paid_experiments':1,
        'shopping_branch': {'name':'US_EN_Shopping_Core_Prospecting','type':'STANDARD_SHOPPING','subtype':'SEARCH','save_status':'Paused','approved_offer_ids':[],'everything_else':'EXCLUDED','bid_strategy':None,'bid_strategy_candidate':'Maximize Clicks only if current native Shopping supports and preserves effective0.15USD Max CPC; Enhanced CPC base bid is not a hard cap','daily_budget':None,'conditional_gates':['Current correct Microsoft Merchant store and approved exact variant offer IDs','Actual item/size/purchase-unit/price/image and fulfillment qualification','Account-supported bid control satisfying owner0.15CPC constraint or explicit changed constraint','Effective geography/network/consent/purchase checks','Exact campaign review and owner cash/loss/activation approval']},
        'search_branch': {'source':'../campaign_plan.md and existing local USEN dress rows','save_status':'Paused','scope':'One USEN dress ad group; three existing exact keywords and one existing RSA after requalification','bid_strategy_candidate':'Maximize Clicks ONLY if native0.15USD Max CPC exists and persists; it optimizes clicks, not buyers','daily_budget':None,'ai_max_and_expansion':{'ai_max':'OFF; record current saved state','search_term_matching':'OFF; inspect dependent control','text_customization':'OFF; inspect dependent control','final_url_expansion':'OFF; inspect dependent control','scheduled_imports_and_auto_apply':'Inspect whether they can restore expansion; do not infer disablement from campaign status'},'conditional_gates':['Matched available landing and genuine purchase signal','Current query/native country/language/network/bid-control readback','Exact review and owner cash/loss/activation approval']},
        'decision_rule':'Narrow US Search is the first preparation candidate; choose Standard Shopping instead only when approved exact offers and equivalent economics, measurement, landing and cost-control gates support it. No US winner or cheaper Shopping CPC inferred. Never enable both simply because both are prepared.',
    },
    'international': {
        'published_locales': [r['locale'] for r in catalog['shopLocales']],
        'active_markets': catalog['markets']['nodes'],
        'countries': '65distinct countries is September9 evidence, not refreshed by current market-names query',
        'search_reserves': 'Existing9-language/11design library preserved; Germany provisional next country, Denmark alternate; others local reserves. Choose only after current demand/fulfillment/CPC evidence.',
        'shopify_channel_feed_language': 'Official native integration documents English; this does not make all Shopify markets English or limit the integration to US',
        'localized_shopping': 'Separate supported Microsoft catalog/feed language and country/label mapping requires account verification; no automatic propagation from21Shopify locales inferred',
    },
    'measurement': {
        'installed_source': 'Last exact bundle verified2026-09-10T00:37:28Z; no new tag or code edit in this plan',
        'event_source': 'Current audited app uses checkout_completed; rawshop-wpa sends merchandise subtotal/currency; distinct legacy storefront source preserved pending receiver evidence',
        'purchase_goal': 'Choose one verified primary purchase goal after current receiver mapping; preserve secondary reporting and completed Smart exclusion',
        'identity': 'Stable logical order identity needed for reconciliation; bind any platform order/event identifier only to documented supported fields. Do not guess product offer ID shape.',
        'pre_activation_gate': 'Authorized functional purchase/value/currency/consent/repeat-delivery proof can be obtained without a prior ad click; use actual confirmed order evidence and permitted tests',
        'post_activation_gate': 'Legitimate paid-click attribution and spend/qualified-traffic monitoring after bounded activation; required before scale, never fabricate production events',
        'refunds': 'Business ledger adjusts actual refunds independently. Automatic Shopify-to-Microsoft refund sync is unverified.',
        'publisher_cookie_defect': 'Previously reproduced malformedmsclkid cookie with90daylocalStorage fallback; source remains publisher-managed, real loss unknown, no installed repair claimed',
    },
    'authority': {'new_spend':False,'numeric_launch_budget':None,'owner_test_loss':None,'manual_review_required_for_proposed_bids_budgets_targeting_goals_creative':True,'current_nonspend_repair_request_preserved':True,'full_paid_scope':'NONE'},
    'access': {'status':'WAITING_EXACT_MICROSOFT_SELECTED_TAB_READINESS','today_native_calls':0,'owner_activity_preserved':True,'prior_specific_auto_review_gate_preserved':True},
    'rollback': 'No external mutation in this packet. Preserve old campaigns and sources. Before any later saved configuration bind exact before-state and inverse settings; new campaigns explicitly Paused.',
}
(HERE / 'launch_contract.json').write_text(json.dumps(contract, indent=2) + '\n')
frozen_names = ['campaigns.csv','ad_groups.csv','keywords.csv','negative_keywords.csv','responsive_search_ads.csv','market_readiness.json','microsoft_deployed_app_pixel.js','microsoft_deployed_storefront_script.js']
manifest = {'captured_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'preserved_existing_files':{name:hashlib.sha256((PACKET/name).read_bytes()).hexdigest() for name in frozen_names},'generated_files':['economics.json','basket_economics.csv','launch_contract.json'],'source_receipts':['analytics_readback.json','shopify_candidate_readback.json']}
(HERE / 'build_receipt.json').write_text(json.dumps(manifest, indent=2)+'\n')
print(json.dumps({'local_outputs':manifest['generated_files'],'basket_scenarios':len(scenarios),'live_product_variants':sum(len(catalog[k]['variants']['nodes']) for k in ('coral','sunshine')),'published_locales':len(catalog['shopLocales']),'active_markets':len(catalog['markets']['nodes']),'approved_offer_count':0,'first_campaign_type':None,'remaining_microsoft_budget':None},indent=2))
