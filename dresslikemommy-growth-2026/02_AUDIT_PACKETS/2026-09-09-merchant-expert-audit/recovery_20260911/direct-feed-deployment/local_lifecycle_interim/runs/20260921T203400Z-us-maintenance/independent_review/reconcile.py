"""Independent local evidence review. No credential, network, or release calls."""
import collections
import csv
import datetime as dt
import decimal
import hashlib
import io
import json
from pathlib import Path
import re
import sys
import urllib.parse

sys.dont_write_bytecode = True
OUT = Path(__file__).resolve().parent
RUN = OUT.parent
LIFE = RUN.parents[1]
BASE = LIFE.parent
RELEASE = BASE / 'automation_release_v1'
ROOT = BASE.parents[4]
REVIEWER = '/root/merchant_us_maintenance_review'
checks, failures = [], []


def load(path):
    return json.loads(path.read_bytes())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(name, value):
    checks.append({'check': name, 'passed': bool(value)})
    if not value:
        failures.append(name)


def save(name, value):
    with (OUT / name).open('x') as handle:
        json.dump(value, handle, indent=2)
        handle.write('\n')


def time(value):
    return dt.datetime.fromisoformat(value.replace('Z', '+00:00'))


contract = load(LIFE / 'release_contract_20260914.json')
config = load(RELEASE / 'config.json')
prepare = load(RUN / 'prepare.json')
intent = load(RUN / 'build.intent.json')
build = load(RUN / 'build.json')
contain = load(RUN / 'contain.receipt.json')
packet = load(RUN / 'candidate_review_packet.json')
snapshot = load(RUN / 'candidate/us-en.snapshot.json')
manifest = load(RUN / 'candidate/us-en.manifest.json')
diagnostics = load(RUN / 'candidate/us-en.diagnostics.json')
before_manifest = load(RUN / 'before.pointer.json')
holds = load(RUN / 'eligibility_holds.json')
market = next(m for m in config['markets'] if m['key'] == 'us-en')
rows = list(csv.DictReader(io.StringIO((RUN / 'candidate/us-en.tsv').read_text()), delimiter='\t'))
before_rows = list(csv.DictReader(io.StringIO((RUN / 'before.tsv').read_text()), delimiter='\t'))
by_id, before_by_id = {r['id']: r for r in rows}, {r['id']: r for r in before_rows}
roots = {'builder': RELEASE, 'local': LIFE, 'audit': BASE.parent.parent}
for entry in contract['files']:
    target = roots[entry['root']] / entry['path']
    check('pinned_dependency:' + entry['path'], not target.is_symlink() and digest(target) == entry['sha256'])
check('release_profile_exact', contract['profile'] == prepare['release_profile'] == packet['release_profile'] == 'native-holds-20260914')
check('release_contract_hash', digest(LIFE / 'release_contract_20260914.json') == '82a3f587677d260cbe1af569a069ad26f318e91a33c97f9767b43dbab80b3e59')
check('lifecycle_hash', digest(LIFE / 'lifecycle.py') == '08580cd0f7d9bc61ade2b98e0d8b46d9c86f9a8ed6987936d6cecf85b7c6e14c')
check('historical_freeze_preserved', digest(RELEASE / 'freeze_manifest.json') == contract['historicalFreezeUnchanged']['sha256'])
check('current_config_bound', digest(RELEASE / 'config.json') == prepare['config_sha256'] == contract['configSha256'])
check('only_us_enabled', [m['key'] for m in config['markets'] if m['enabled']] == ['us-en'])
check('unchanged_age_guards', config['maxSnapshotAgeHours'] == 24 and config['maxFeedAgeHours'] == 48)
check('free_listing_columns', 'return_policy_label' not in rows[0] and config['returnPolicy']['emitLabels'] is False)
check('before_pointer_bound', digest(RUN / 'before.pointer.json') == prepare['pointer_sha256'] == packet['before_pointer_sha256'])
check('before_feed_bound', digest(RUN / 'before.tsv') == prepare['before_feed_sha256'] == before_manifest['sha256'])
prior_prepare = load(LIFE / 'runs/20260915T015530Z-us-color47-refresh/prepare.json')
check('worker_metadata_matches_accepted_run', prepare['workers'] == prior_prepare['workers'])
check('existing_us_target', prepare['merchant_source'] == '10727274744' and prepare['pointer'] == 'merchant/us-en/current.json' and prepare['bucket'] == 'dlm-merchant-feeds' and prepare['account'] == '6b1df53f8a1ce4b5b5312f833a2cd966')
coordination = (ROOT / 'ops/AGENT_COORDINATION.md').read_text()
claim = [line for line in coordination.splitlines() if '| Current owner Merchant Center international free-listing audit and repair |' in line]
check('sole_writer_claim', len(claim) == 1 and 'root01a08706-c63a-7e01-ba48-7777bcb1788a sole Merchant/channel writer' in claim[0] and 'US10727274744/AU10727245667' in claim[0] and 'direct nonspend active-product/lifecycle/feed/website/setup corrections' in claim[0])
claim_sha = hashlib.sha256(claim[0].encode()).hexdigest() if claim else None
check('live_successful_scan', build['live'] is True and build['returncode'] == 0 and not build['stderr'] and intent['live'] is True and '--live' in intent['command'] and '--snapshot' not in intent['command'])
check('exact_build_command', intent['command'][1:3] == [str(RELEASE / 'bin/build.mjs'), '--config'] and intent['command'][3:] == [str(RELEASE / 'config.json'), '--market', 'us-en', '--live', '--previous-manifest', str(RUN / 'before.pointer.json'), '--out', str(RUN / 'candidate')])
check('genuine_source_clock', time(build['started_at_utc']) == time(intent['started_at_utc']) <= time(snapshot['startedAt']) <= time(snapshot['completedAt']) <= time(build['finished_at_utc']))
check('source_clock_advanced', time(snapshot['completedAt']) > time(before_manifest['sourceCompletedAt']))
check('source_clock_propagated', snapshot['completedAt'] == manifest['sourceCompletedAt'] == diagnostics['sourceCompletedAt'] == packet['source_completed_at'])
check('fresh_within_120_minutes', -60 <= (dt.datetime.now(dt.timezone.utc) - time(snapshot['completedAt'])).total_seconds() <= 7200)
check('generation_clock_bound', manifest['generatedAt'] == diagnostics['generatedAt'] and time(snapshot['completedAt']) <= time(manifest['generatedAt']) <= time(build['finished_at_utc']))
check('shop_identity', snapshot['shop']['id'] == config['shopId'] == 'gid://shopify/Shop/15571635' and snapshot['sourceLocale'] == 'en' and snapshot['onlinePublicationId'] == config['onlinePublicationId'])
check('market_identity', snapshot['market'] == manifest['market'] == packet['market'] == {'key': 'us-en', 'country': 'US', 'locale': 'en', 'currency': 'USD', 'marketId': 'gid://shopify/Market/544735329'})
check('catalog_identity_stable', snapshot['marketContext'] == snapshot['finalMarketContext'] and snapshot['marketContext']['currency'] == 'USD' and snapshot['marketContext']['catalogs'] == market['expectedCatalogs'] and market['marketId'] in snapshot['marketContext']['activeMarketIds'])
products = snapshot['products']
check('exact_complete_parent_counts', snapshot['paginationComplete'] is True and snapshot['activeCount'] == snapshot['finalActiveCount'] == {'count': len(products), 'precision': 'EXACT'} and manifest['sourceParents'] == len(products))
check('unique_parent_ids', len({p['id'] for p in products}) == len(products))
fields = ['id', 'status', 'updatedAt', 'variantsCount', 'onlinePublished', 'countryPublished', 'catalogPublished']
observed_manifest = sorted([{key: p[key] for key in fields} for p in products], key=lambda p: p['id'])
check('final_manifest_exact', observed_manifest == snapshot['finalManifest'])
trace = collections.defaultdict(list)
for event in snapshot['trace']:
    trace[event['connection']].append(event)
for label, count in [('products', len(products)), ('final_manifest', len(products))]:
    pages = trace[label]
    check('complete_pages:' + label, sum(p['rows'] for p in pages) == count and pages[-1]['hasNextPage'] is False and all(p['hasNextPage'] is True and p['rows'] > 0 for p in pages[:-1]))
check('catalog_before_after_pages', len(trace['market_catalogs']) == 2 and all(p == {'connection': 'market_catalogs', 'rows': 1, 'hasNextPage': False} for p in trace['market_catalogs']))
held_ids = {h['product_id'] for h in holds['holds']}
check('six_exact_holds', held_ids == {'gid://shopify/Product/' + n for n in ['7516369715297', '7516479848545', '7536337125473', '7536992976993', '7536988520545', '7536086089825']} and len(holds['holds']) == 6)
check('holds_file_exact', digest(RUN / 'eligibility_holds.json') == digest(LIFE / 'eligibility_holds_20260911.json') == prepare['planned_eligibility_holds_sha256'] == config['eligibilityHolds']['source']['sha256'])
check('holds_config_exact', config['eligibilityHolds']['holds'] == holds['holds'])
eligible, excluded, source_variants, source_prices = {}, {}, set(), []
held_counts = collections.Counter()
for p in products:
    pid = p['id'].rsplit('/', 1)[-1]
    check('active_unique_complete_parent:' + pid, p['status'] == 'ACTIVE' and p['variantsCount'] == {'count': len(p['variants']), 'precision': 'EXACT'})
    pages = trace['variants:' + p['id']]
    check('complete_variant_pages:' + pid, bool(pages) and sum(t['rows'] for t in pages) == len(p['variants']) and pages[-1]['hasNextPage'] is False and all(t['hasNextPage'] is True and t['rows'] > 0 for t in pages[:-1]))
    for v in p['variants']:
        vid = v['id'].rsplit('/', 1)[-1]
        offer = f'shopify_US_{pid}_{vid}'
        check('unique_variant:' + vid, v['id'] not in source_variants)
        source_variants.add(v['id'])
        check('boolean_availability:' + vid, type(v['availableForSale']) is bool)
        money = v['contextualPricing']['price']
        amount = decimal.Decimal(money['amount'])
        check('source_price:' + vid, money['currencyCode'] == 'USD' and amount > 0 and amount == amount.quantize(decimal.Decimal('0.01')))
        source_prices.append(amount)
        reason = ('not_on_online_store' if not p['onlinePublished'] else 'not_published_in_country' if not p['countryPublished'] else 'not_in_market_catalog' if not p['catalogPublished'] else 'variant_not_available_for_sale' if not v['availableForSale'] else 'reviewed_parent_eligibility_hold' if p['id'] in held_ids else None)
        if reason:
            excluded[offer] = reason
            if reason == 'reviewed_parent_eligibility_hold':
                held_counts[p['id']] += 1
            continue
        eligible[offer] = (p, v)
        row = by_id.get(offer)
        check('eligible_offer_present:' + vid, row is not None)
        if row is None:
            continue
        check('row_identity_and_availability:' + vid, row['item_group_id'] == f'shopify_US_{pid}' and row['availability'] == 'in_stock' and row['excluded_destination'] == 'Shopping_ads')
        check('exact_contextual_price:' + vid, row['price'] == f'{amount:.2f} USD')
        url = urllib.parse.urlsplit(row['link'])
        check('exact_product_variant_link:' + vid, url.scheme == 'https' and url.netloc == 'www.dresslikemommy.com' and url.path == '/products/' + p['handle'] and urllib.parse.parse_qs(url.query) == {'variant': [vid]} and not url.fragment)
        images = [m['image']['url'] for m in v['media']['nodes'] if m.get('image', {}).get('url')]
        image = images[0] if images else p['featuredMedia']['image']['url']
        check('source_image_binding:' + vid, row['image_link'] == image)
check('variant_count_complete', len(source_variants) == manifest['sourceVariants'] == sum(len(p['variants']) for p in products))
check('entire_offer_partition_exact', set(eligible) == set(by_id) and not set(excluded) & set(by_id) and len(eligible) + len(excluded) == len(source_variants) and len(rows) == len(by_id))
reported_exclusions = {e['id']: e['code'] for e in diagnostics['exclusions'] if e.get('id')}
check('diagnostic_exclusions_exact', reported_exclusions == excluded and len(diagnostics['exclusions']) == len(excluded))
check('hold_counts_exact', diagnostics['eligibilityHolds']['removedRowsByParent'] == dict(held_counts) and sum(held_counts.values()) == packet['contained_available_rows'] == 162)
check('no_source_or_feed_errors', diagnostics['errors'] == [] and diagnostics['outOfStock'] == 0 and diagnostics['returnPolicyLabelsEmitted'] is False)
check('source_variant_count_4925', len(source_variants) == 4925)
check('output_4741_parents_232', len(rows) == 4741 and len({r['item_group_id'] for r in rows}) == packet['eligible_parent_count'] == 232)
delta = {'added_ids': sorted(set(by_id) - set(before_by_id)), 'removed_ids': sorted(set(before_by_id) - set(by_id)), 'changed_fields': {key: [field for field in rows[0] if by_id[key][field] != before_by_id[key][field]] for key in sorted(set(by_id) & set(before_by_id)) if by_id[key] != before_by_id[key]}, 'retained_count': len(set(by_id) & set(before_by_id)), 'unchanged_retained_count': sum(by_id[key] == before_by_id[key] for key in set(by_id) & set(before_by_id))}
check('independent_delta_exact', delta == packet['delta'])
check('all_output_bytes_unchanged', (RUN / 'candidate/us-en.tsv').read_bytes() == (RUN / 'before.tsv').read_bytes() and packet['bytes_unchanged'] is True)
check('no_added_buyer_routes_needed', delta['added_ids'] == [])
check('no_removed_or_changed_offers', delta['removed_ids'] == [] and delta['changed_fields'] == {})
check('no_mass_removal', packet['mass_removal_review_required'] is False)
check('no_extreme_feed_prices', all(decimal.Decimal(r['price'].split()[0]) <= 1000 for r in rows) and packet['prices_above_1000_usd'] == [])
for filename, expected in contain['original_files'].items():
    check('source_artifact_unmodified:' + filename, digest(RUN / 'candidate' / filename) == digest(RUN / 'unfiltered' / filename) == expected)
check('no_second_filter_or_restamp', contain['second_filter_applied'] is False and contain['source_scan_reused_without_restamping'] is True and contain['native_replay']['sourceClockChanged'] is False)
sys.path.insert(0, str(LIFE))
import lifecycle
lifecycle.select_release_profile('native-holds-20260914')
try:
    verified_packet = lifecycle.candidate(RUN)
    check('supported_offline_replay_and_all_packet_bindings', verified_packet == packet)
except Exception as error:
    check('supported_offline_replay_and_all_packet_bindings', False)
    failures.append(type(error).__name__ + ':' + str(error))
check('six_protected_ids_preserved', all(i in by_id for i in lifecycle.PROTECTED_US_IDS) and packet['protected_omissions'] == [])
source_deadline = time(snapshot['completedAt']) + dt.timedelta(hours=2)
summary = {
    'reviewer': REVIEWER, 'reviewed_at_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
    'decision': 'HOLD' if failures else 'APPROVE_EXACT_US_FEED_POINTER',
    'check_count': len(checks), 'passed_count': sum(c['passed'] for c in checks), 'failures': failures,
    'source_completed_at': snapshot['completedAt'], 'source_deadline_utc': source_deadline.isoformat(),
    'source_parents': len(products), 'source_variants_all_prices_checked': len(source_variants),
    'feed_rows_all_prices_bound': len(rows), 'eligible_parents': len({r['item_group_id'] for r in rows}),
    'source_price_range_usd': [str(min(source_prices)), str(max(source_prices))],
    'exclusion_counts': dict(collections.Counter(excluded.values())), 'held_available_by_parent': dict(held_counts),
    'delta': delta, 'warning_counts': dict(collections.Counter(w['code'] for w in diagnostics['warnings'])),
    'source_requests': len(snapshot['trace']) + 2, 'claim_sha256_at_review': claim_sha,
    'feed_sha256': digest(RUN / 'candidate/us-en.tsv'),
    'boundary': 'Offline independent review only. No credentials read, network/API calls, browser, source rebuild, external write, Git or canonical mutation.',
    'action_time_requirements': ['Root must use the pinned promote command, which independently rechecks current remote pointer and Worker equality under the writer lock.', 'Promotion must finish within the unchanged 120-minute source window. Never restamp the source clock.', 'Google source processing/offer approval and business outcomes need separate receiving evidence.'],
    'limits': ['Existing buyer-route limitations are not cured by this byte-identical source renewal.', '5,690 existing nonblocking diagnostics remain; no claim of perfect attributes or sales/profit.'],
}
save('checks.json', {'checks': checks, 'failures': failures})
save('summary.json', summary)
if not failures:
    fields = ('eligibility_holds_sha256', 'source_qualification_sha256', 'cohort_filter_sha256', 'containment_receipt_sha256', 'prepare_receipt_sha256', 'live_build_receipt_sha256', 'live_build_intent_sha256', 'before_pointer_sha256', 'candidate_manifest_sha256', 'candidate_feed_sha256', 'candidate_snapshot_sha256', 'candidate_diagnostics_sha256', 'uploader_sha256', 'config_sha256', 'builder_freeze_sha256', 'source_completed_at', 'release_profile', 'native_verifier_sha256')
    review = {key: packet[key] for key in fields}
    review.update(decision='APPROVE_EXACT_US_FEED_POINTER', independent=True, reviewer=REVIEWER,
        reviewed_at_utc=summary['reviewed_at_utc'], protected_omissions_verified=packet['protected_omissions'],
        source_eligibility_and_all_prices_verified=True, source_eligibility_holds_verified=True,
        single_writer_claim_verified=True, buyer_qualified_added_ids=[], mass_removal_explicitly_verified=False,
        approved_action='TA07-US-AU-SOURCE-MAINTENANCE-20260921: existing US/en/USD free-listing source pointer renewal only',
        approval_expires_at_utc=source_deadline.isoformat(), checks_sha256=digest(OUT / 'checks.json'),
        independent_summary_sha256=digest(OUT / 'summary.json'), action_time_requirements=summary['action_time_requirements'])
    save('review.json', review)
    lifecycle.validate_review(RUN, OUT / 'review.json', digest(OUT / 'review.json'))
    save('validator_receipt.json', {'passed': True, 'validator': 'pinned lifecycle.validate_review; offline candidate/native replay only', 'validated_at_utc': dt.datetime.now(dt.timezone.utc).isoformat(), 'review_sha256': digest(OUT / 'review.json'), 'check_count': len(checks), 'no_external_calls': True})
print(json.dumps({**{k: summary[k] for k in ['decision', 'check_count', 'passed_count', 'failures', 'source_completed_at', 'source_deadline_utc', 'source_parents', 'source_variants_all_prices_checked', 'feed_rows_all_prices_bound', 'eligible_parents', 'source_price_range_usd', 'exclusion_counts', 'source_requests', 'feed_sha256']}, 'review_sha256': digest(OUT / 'review.json') if (OUT / 'review.json').exists() else None, 'summary_sha256': digest(OUT / 'summary.json')}))
