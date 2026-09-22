"""Independent AU full-source and candidate review; offline, evidence-only writes."""
import collections
import csv
import datetime as dt
import decimal
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import urllib.parse

sys.dont_write_bytecode = True
OUT = Path(__file__).resolve().parent
RUN = OUT.parent
AUDIT = RUN.parents[1]
ROOT = AUDIT.parents[2]
BASE = AUDIT / 'recovery_20260911/direct-feed-deployment'
LIFE = BASE / 'local_lifecycle_interim'
RELEASE = BASE / 'automation_release_v1'
PRIOR = AUDIT / 'recovery_20260914/au_color47_refresh_20260915'
REVIEWER = '/root/merchant_us_maintenance_review'
NODE = '/Users/fsuels/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node'
checks, failures = [], []


def load(path):
    return json.loads(path.read_bytes())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(name, passed):
    checks.append({'check': name, 'passed': bool(passed)})
    if not passed:
        failures.append(name)


def save(name, value):
    with (OUT / name).open('x') as handle:
        json.dump(value, handle, indent=2)
        handle.write('\n')


def time(value):
    return dt.datetime.fromisoformat(value.replace('Z', '+00:00'))


def tsv(relative):
    return list(csv.DictReader(io.StringIO((RUN / relative).read_text()), delimiter='\t'))


prepare = load(RUN / 'prepare.json')
intent = load(RUN / 'build.intent.json')
build = load(RUN / 'build.json')
pins = load(RUN / 'build_dependency_pins.json')
native = load(RUN / 'native_before.json')
guard = load(RUN / 'filter_guard_note.json')
packet = load(RUN / 'containment_and_delta.json')
config = load(BASE / 'international_candidate_config.json')
market = next(m for m in config['markets'] if m['key'] == 'au-en')
holds = load(RUN / 'eligibility_holds.json')
snapshot = load(RUN / 'source/au-en.snapshot.json')
raw_manifest = load(RUN / 'source/au-en.manifest.json')
raw_diagnostic = load(RUN / 'source/au-en.diagnostics.json')
manifest = load(RUN / 'candidate/au-en.manifest.json')
diagnostic = load(RUN / 'candidate/au-en.diagnostics.json')
before_manifest = load(RUN / 'before.au-en.manifest.json')
rows, raw_rows, before_rows = tsv('candidate/au-en.tsv'), tsv('source/au-en.tsv'), tsv('before.au-en.tsv')
by_id, raw_by_id, before_by_id = ({r['id']: r for r in group} for group in (rows, raw_rows, before_rows))
check('dependency_pins_exact_prior', pins == load(PRIOR / 'build_dependency_pins.json'))
for relative, expected in pins.items():
    check('pinned_dependency:' + relative, digest(ROOT / relative) == expected and not (ROOT / relative).is_symlink())
check('config_known_au_hash', digest(BASE / 'international_candidate_config.json') == '6be63f2712324d9a3d0bddf750b1f46616e5e910e9cecb15073c3b17754163ed')
check('unchanged_age_guards', config['maxSnapshotAgeHours'] == 24 and config['maxFeedAgeHours'] == 48)
check('no_return_label_emission', config['returnPolicy']['emitLabels'] is False and 'return_policy_label' not in rows[0])
check('empty_raw_native_hold_policy', 'eligibilityHolds' not in config and raw_diagnostic['eligibilityHolds']['configuredParentIds'] == [] and raw_diagnostic['eligibilityHolds']['removedAvailableRows'] == 0 and not any(e['code'] == 'reviewed_parent_eligibility_hold' for e in raw_diagnostic['exclusions']))
check('precondition_stop_no_candidate_or_dependency_write', guard['initial_attempt_candidate_writes'] == 0 and guard['source_or_dependency_changes'] == 0)
for entry in prepare['baseline']:
    check('baseline_binding:' + Path(entry['path']).name, digest(Path(entry['path'])) == digest(Path(entry['source'])) == entry['sha256'])
check('before_feed_manifest_hash', digest(RUN / 'before.au-en.tsv') == before_manifest['sha256'] == packet['before_feed_sha256'])
check('prepare_exact_current_scope', prepare['action'] == 'TA07-US-AU-SOURCE-MAINTENANCE-20260921' and prepare['source_id'] == '10727245667' and prepare['merchant_id'] == '513542500' and prepare['existing_manual_source'] is True and prepare['no_new_market_or_source'] is True)
check('native_exact_identity', native['merchant_account_id'] == '513542500' and native['source_id'] == '10727245667' and native['source_name'] == 'DLM AU English Free Listings')
check('native_existing_au_free_manual', native['source_type'] == 'File (manual)' and native['country'] == 'Australia' and native['language'] == 'English' and native['feed_label'] == 'AU' and native['marketing_methods'] == ['Free listings'] and native['source_count'] == 4741)
check('native_before_no_writes', native['native_uploads'] == 0 and native['source_setting_changes'] == 0)
claim_lines = [(n, line) for n, line in enumerate((ROOT / 'ops/AGENT_COORDINATION.md').read_text().splitlines(), 1) if '| Current owner Merchant Center international free-listing audit and repair |' in line]
check('sole_writer_claim', len(claim_lines) == 1 and 'root01a08706-c63a-7e01-ba48-7777bcb1788a sole Merchant/channel writer' in claim_lines[0][1] and 'direct nonspend active-product/lifecycle/feed/website/setup corrections' in claim_lines[0][1])
check('build_current_live_success', build['returncode'] == 0 and build['live'] is True and build['stderr'] == '' and intent['live'] is True)
check('build_command_exact', intent['command'] == [NODE, str(RELEASE / 'bin/build.mjs'), '--config', str(BASE / 'international_candidate_config.json'), '--market', 'au-en', '--live', '--previous-manifest', str(RUN / 'before.au-en.manifest.json'), '--out', str(RUN / 'source')])
check('genuine_source_clock', time(build['started_at_utc']) == time(intent['started_at_utc']) <= time(snapshot['startedAt']) <= time(snapshot['completedAt']) <= time(build['finished_at_utc']))
check('fresh_advanced_source_clock', time(snapshot['completedAt']) > time(before_manifest['sourceCompletedAt']) and -60 <= (dt.datetime.now(dt.timezone.utc) - time(snapshot['completedAt'])).total_seconds() <= 7200)
check('clock_propagated_without_restamp', snapshot['completedAt'] == raw_manifest['sourceCompletedAt'] == manifest['sourceCompletedAt'] == raw_diagnostic['sourceCompletedAt'] == diagnostic['sourceCompletedAt'] == packet['source_completed_at'] and raw_manifest['generatedAt'] == manifest['generatedAt'] == raw_diagnostic['generatedAt'] == diagnostic['generatedAt'])
check('generation_within_build', time(snapshot['completedAt']) <= time(manifest['generatedAt']) <= time(build['finished_at_utc']))
check('shop_identity', snapshot['shop']['id'] == config['shopId'] == 'gid://shopify/Shop/15571635' and snapshot['sourceLocale'] == 'en' and snapshot['onlinePublicationId'] == config['onlinePublicationId'])
check('au_market_identity', snapshot['market'] == raw_manifest['market'] == manifest['market'] == {'key': 'au-en', 'country': 'AU', 'locale': 'en', 'currency': 'AUD', 'marketId': 'gid://shopify/Market/544866401'})
check('country_effective_catalog_stable', snapshot['marketContext'] == snapshot['finalMarketContext'] and snapshot['marketContext']['currency'] == 'AUD' and snapshot['marketContext']['catalogs'] == market['expectedCatalogs'] == [{'id': 'gid://shopify/MarketCatalog/910622817', 'publicationId': 'gid://shopify/Publication/77105823841'}] and market['marketId'] in snapshot['marketContext']['activeMarketIds'])
products = snapshot['products']
check('exact_complete_parent_counts', snapshot['paginationComplete'] is True and snapshot['activeCount'] == snapshot['finalActiveCount'] == {'count': len(products), 'precision': 'EXACT'} and manifest['sourceParents'] == len(products) == 238)
check('unique_parents', len({p['id'] for p in products}) == len(products))
manifest_keys = ['id', 'status', 'updatedAt', 'variantsCount', 'onlinePublished', 'countryPublished', 'catalogPublished']
check('stable_final_manifest', sorted([{k: p[k] for k in manifest_keys} for p in products], key=lambda p: p['id']) == snapshot['finalManifest'])
trace = collections.defaultdict(list)
for event in snapshot['trace']:
    trace[event['connection']].append(event)
for label in ['products', 'final_manifest']:
    pages = trace[label]
    check('complete_pages:' + label, sum(p['rows'] for p in pages) == len(products) and pages[-1]['hasNextPage'] is False and all(p['hasNextPage'] is True and p['rows'] > 0 for p in pages[:-1]))
check('initial_final_catalog_pagination', len(trace['market_catalogs']) == 2 and all(e['rows'] == 1 and e['hasNextPage'] is False for e in trace['market_catalogs']))
held = {h['product_id'] for h in holds['holds']}
check('six_holds_exact', held == {'gid://shopify/Product/' + n for n in ['7516369715297', '7516479848545', '7536337125473', '7536992976993', '7536988520545', '7536086089825']} and len(holds['holds']) == 6)
check('canonical_hold_bytes_exact', digest(RUN / 'eligibility_holds.json') == digest(LIFE / 'eligibility_holds_20260911.json') == packet['holds_sha256'] == '8ef6615558d3ff08e9b2bcef424041c36e25710be17101bd8145cc46c7b33733')
source_variants, raw_expected, eligible, exclusions = set(), set(), set(), {}
held_counts = collections.Counter()
source_prices = []
for p in products:
    pid = p['id'].rsplit('/', 1)[-1]
    check('active_complete_parent:' + pid, p['status'] == 'ACTIVE' and p['variantsCount'] == {'count': len(p['variants']), 'precision': 'EXACT'})
    pages = trace['variants:' + p['id']]
    check('complete_variant_pages:' + pid, bool(pages) and sum(e['rows'] for e in pages) == len(p['variants']) and pages[-1]['hasNextPage'] is False and all(e['hasNextPage'] is True and e['rows'] > 0 for e in pages[:-1]))
    for v in p['variants']:
        vid = v['id'].rsplit('/', 1)[-1]
        offer = f'shopify_AU_{pid}_{vid}'
        check('unique_variant:' + vid, v['id'] not in source_variants)
        source_variants.add(v['id'])
        check('boolean_availability:' + vid, type(v['availableForSale']) is bool)
        money = v['contextualPricing']['price']
        amount = decimal.Decimal(money['amount'])
        source_prices.append(amount)
        check('all_source_aud_prices:' + vid, money['currencyCode'] == 'AUD' and amount > 0 and amount == amount.quantize(decimal.Decimal('0.01')))
        reason = ('not_on_online_store' if not p['onlinePublished'] else 'not_published_in_country' if not p['countryPublished'] else 'not_in_market_catalog' if not p['catalogPublished'] else 'variant_not_available_for_sale' if not v['availableForSale'] else None)
        if reason:
            exclusions[offer] = reason
            continue
        raw_expected.add(offer)
        raw_row = raw_by_id.get(offer)
        check('available_raw_offer_and_price:' + vid, raw_row is not None and raw_row['price'] == f'{amount:.2f} AUD')
        if p['id'] in held:
            exclusions[offer] = 'reviewed_parent_eligibility_hold'
            held_counts[p['id']] += 1
            continue
        eligible.add(offer)
        row = by_id.get(offer)
        check('eligible_offer_present:' + vid, row is not None)
        if row is None:
            continue
        check('candidate_source_price:' + vid, row['price'] == f'{amount:.2f} AUD')
        check('candidate_identity_availability_destination:' + vid, row['item_group_id'] == f'shopify_AU_{pid}' and row['availability'] == 'in_stock' and row['excluded_destination'] == 'Shopping_ads')
        url = urllib.parse.urlsplit(row['link'])
        check('exact_au_context_variant_link:' + vid, url.scheme == 'https' and url.netloc == 'www.dresslikemommy.com' and url.path == '/products/' + p['handle'] and urllib.parse.parse_qs(url.query) == {'country': ['AU'], 'currency': ['AUD'], 'variant': [vid]} and not url.fragment)
        images = [m['image']['url'] for m in v['media']['nodes'] if m.get('image', {}).get('url')]
        check('source_image_binding:' + vid, row['image_link'] == (images[0] if images else p['featuredMedia']['image']['url']))
        check('raw_row_preserved_exact:' + vid, row == raw_row)
check('raw_full_eligible_partition', raw_expected == set(raw_by_id) and len(raw_rows) == len(raw_by_id) == 4903)
check('candidate_full_partition', eligible == set(by_id) and not set(exclusions) & eligible and len(eligible) + len(exclusions) == len(source_variants) == 4925 and len(rows) == len(by_id) == 4741)
check('source_variant_count', manifest['sourceVariants'] == len(source_variants))
check('candidate_exclusion_diagnostics', {e['id']: e['code'] for e in diagnostic['exclusions']} == exclusions and len(diagnostic['exclusions']) == len(exclusions))
check('raw_only_unavailable_exclusions', {e['id']: e['code'] for e in raw_diagnostic['exclusions']} == {k: v for k, v in exclusions.items() if v != 'reviewed_parent_eligibility_hold'})
check('hold_counts_exact', diagnostic['eligibilityHolds']['removed_rows_by_parent'] == dict(held_counts) and sum(held_counts.values()) == packet['held_available_rows'] == 162)
check('all_diagnostics_no_errors', raw_diagnostic['errors'] == diagnostic['errors'] == [] and raw_diagnostic['outOfStock'] == diagnostic['outOfStock'] == 0 and diagnostic['returnPolicyLabelsEmitted'] is False)
check('source_snapshot_bytes_preserved', (RUN / 'source/au-en.snapshot.json').read_bytes() == (RUN / 'candidate/au-en.snapshot.json').read_bytes())
changed = {key: [field for field in rows[0] if by_id[key][field] != before_by_id[key][field]] for key in sorted(set(by_id) & set(before_by_id)) if by_id[key] != before_by_id[key]}
check('zero_added_removed', set(by_id) == set(before_by_id) and packet['added_ids'] == packet['removed_ids'] == [])
check('exact186_price_only_changes', len(changed) == 186 and all(fields == ['price'] for fields in changed.values()) and changed == packet['changed'] and packet['changed_field_counts'] == {'price': 186})
check('every_nonprice_field_preserved', all({k: v for k, v in row.items() if k != 'price'} == {k: v for k, v in before_by_id[oid].items() if k != 'price'} for oid, row in by_id.items()))
check('six_protected_preserved', len(packet['protected_ids']) == 6 and all(oid in by_id for oid in packet['protected_ids']) and packet['protected_omissions'] == [])
check('no_extreme_aud_price', max(source_prices) == decimal.Decimal('58.00') and min(source_prices) == decimal.Decimal('22.00'))
price_groups = collections.defaultdict(list)
for oid in sorted(changed):
    price_groups[(before_by_id[oid]['price'], by_id[oid]['price'])].append(oid)
check('three_expected_price_groups', {pair: len(ids) for pair, ids in price_groups.items()} == {('37.00 AUD', '38.00 AUD'): 93, ('47.00 AUD', '48.00 AUD'): 50, ('57.00 AUD', '58.00 AUD'): 43})
replay = subprocess.run([NODE, str(OUT / 'raw_replay.mjs'), str(RUN)], capture_output=True, text=True, timeout=90)
check('offline_generator_replay_exit', replay.returncode == 0 and replay.stderr == '')
replay_result = json.loads(replay.stdout)
save('raw_replay.json', replay_result)
check('offline_generator_raw_exact', replay_result['passed'] is True and replay_result['raw_rows'] == 4903 and replay_result['source_completed_at'] == snapshot['completedAt'])
sys.path.insert(0, str(LIFE))
from cohort_filter import apply_holds
output, replay_manifest, replay_diagnostic = apply_holds((RUN / 'source/au-en.tsv').read_bytes(), raw_manifest, raw_diagnostic, (RUN / 'eligibility_holds.json').read_bytes(), before_manifest['rowIds'], protected_ids=packet['protected_ids'], source_parent_ids=[p['id'] for p in products])
check('single_filter_replay_exact_all_three_outputs', output == (RUN / 'candidate/au-en.tsv').read_bytes() and replay_manifest == manifest and replay_diagnostic == diagnostic)
check('candidate_byte_hash_and_size', digest(RUN / 'candidate/au-en.tsv') == manifest['sha256'] == packet['candidate_feed_sha256'] == 'b4249404c374bbfd0467633c2959a0ddc13f85ce86fbf5c71177260455a45d5d' and len(output) == manifest['bytes'] == packet['candidate_feed_bytes'] == 16621192)
check('candidate_md5', hashlib.md5(output).hexdigest() == manifest['expectedMd5'] == manifest['objectEtag'] == packet['candidate_feed_md5'])
check('manifest_row_ids_exact', [row['id'] for row in rows] == manifest['rowIds'] and manifest['rows'] == len(rows))
check('pins_still_exact_after_review', all(digest(ROOT / relative) == expected for relative, expected in pins.items()))
sample_ids = [ids[0] for pair, ids in sorted(price_groups.items())] + packet['protected_ids']
samples = [{'id': oid, 'purpose': 'changed_price_group' if oid in changed else 'protected_offer', 'title': by_id[oid]['title'], 'expected_price': by_id[oid]['price'], 'expected_availability': 'In stock', 'expected_country': 'Australia', 'expected_marketing_method': 'Free listings', 'expected_status': 'Approved'} for oid in dict.fromkeys(sample_ids)]
save('native_after_sample_plan.json', {'source_id': '10727245667', 'merchant_id': '513542500', 'samples': samples, 'sample_count': len(samples), 'scope_limit': 'Representative native offer readbacks; does not individually verify all186 changed prices or establish storefront buyer acceptance.'})
expiry = time(snapshot['completedAt']) + dt.timedelta(hours=2)
summary = {'reviewer': REVIEWER, 'reviewed_at_utc': dt.datetime.now(dt.timezone.utc).isoformat(), 'decision': 'HOLD' if failures else 'APPROVE_EXACT_AU_NATIVE_UPLOAD', 'check_count': len(checks), 'passed_count': sum(c['passed'] for c in checks), 'failures': failures,
    'source_completed_at': snapshot['completedAt'], 'upload_deadline_utc': expiry.isoformat(), 'parents': len(products), 'variants_all_aud_prices_checked': len(source_variants), 'raw_rows': len(raw_rows), 'candidate_rows': len(rows), 'candidate_parents': len({r['item_group_id'] for r in rows}), 'exclusion_counts': dict(collections.Counter(exclusions.values())),
    'price_groups': [{'before': pair[0], 'after': pair[1], 'rows': len(ids), 'sample_id': ids[0]} for pair, ids in sorted(price_groups.items())], 'changed_rows': len(changed), 'unchanged_whole_rows': len(rows) - len(changed), 'source_requests': len(snapshot['trace']) + 2, 'source_aud_price_range': [str(min(source_prices)), str(max(source_prices))],
    'warnings_all_raw_rows': dict(collections.Counter(w['code'] for w in raw_diagnostic['warnings'])), 'emitted_missing_color_rows': sum(not row['color'] for row in rows), 'offline_generator_replay_exact': replay_result['passed'], 'single_filter_outputs_exact': output == (RUN / 'candidate/au-en.tsv').read_bytes() and replay_manifest == manifest and replay_diagnostic == diagnostic,
    'claim': {'path': str(ROOT / 'ops/AGENT_COORDINATION.md'), 'line': claim_lines[0][0], 'row_sha256': hashlib.sha256(claim_lines[0][1].encode()).hexdigest()}, 'external_calls': 0, 'external_writes': 0,
    'limits': ['Read-only independent local review of root-captured source/native evidence; not a new direct Google or Shopify read.', 'Existing numeric-variant arrival limitations remain separate; no new buyer acceptance or checkout/traffic/sales claim.', 'Legacy diagnostics include held/nonemitted offers; raw warning totals are not emitted-row counts.', 'The old native receipt display has no verified timezone and is not fresh acceptance.']}
save('checks.json', {'checks': checks, 'failures': failures})
save('summary.json', summary)
artifacts = [RUN / name for name in ['prepare.json', 'build.intent.json', 'build.json', 'build_dependency_pins.json', 'dependency_verification.json', 'native_before.json', 'filter_guard_note.json', 'containment_and_delta.json', 'before.au-en.tsv', 'before.au-en.manifest.json', 'eligibility_holds.json']]
artifacts += [RUN / directory / ('au-en.' + suffix) for directory in ['source', 'candidate'] for suffix in ['tsv', 'snapshot.json', 'manifest.json', 'diagnostics.json']]
artifacts += [OUT / name for name in ['summary.json', 'checks.json', 'raw_replay.json', 'native_after_sample_plan.json', 'reconcile.py', 'raw_replay.mjs']]
bindings = {str(p.relative_to(ROOT)): digest(p) for p in artifacts}
bindings.update(pins)
if not failures:
    review = {'review_version': 1, 'independent': True, 'reviewer': REVIEWER, 'reviewed_at_utc': summary['reviewed_at_utc'], 'decision': 'APPROVE_EXACT_AU_NATIVE_UPLOAD', 'verdict': 'PASS_WITH_LIMITS', 'action': prepare['action'], 'scope': 'Exact existing AU manual free-listing source replacement only; root retains execution and parent acceptance authority.',
        'destination': {'account_id': '513542500', 'source_id': '10727245667', 'source_name': 'DLM AU English Free Listings', 'country': 'AU', 'language': 'en', 'currency': 'AUD', 'feed_label': 'AU', 'marketing_method': 'Free listings', 'source_type': 'File (manual)'},
        'candidate': {'path': str(RUN / 'candidate/au-en.tsv'), 'sha256': digest(RUN / 'candidate/au-en.tsv'), 'md5': hashlib.md5(output).hexdigest(), 'bytes': len(output), 'rows': len(rows)}, 'source_completed_at_utc': snapshot['completedAt'], 'generated_at_utc': manifest['generatedAt'], 'upload_deadline_utc': expiry.isoformat(), 'binding_path_base': str(ROOT), 'bindings': bindings, 'claim': summary['claim'],
        'source_eligibility_and_all_prices_verified': True, 'source_eligibility_holds_verified': True, 'single_writer_claim_verified': True, 'protected_omissions_verified': [], 'buyer_qualified_added_ids': [], 'independent_check_count': len(checks),
        'action_time_requirements': ['Root rechecks all bound bytes, current sole-writer claim and exact native account/source/settings; any material drift requires new review.', 'Upload this exact candidate once before the source+120minute deadline. Never restamp source time or repeat an uncertain upload.', 'Preserve six holds, AU/en/AUD Free listings, Shopping_ads exclusions and existing source configuration. No scheduler, Worker, theme, schema, hold or new-market action.'],
        'after_requirements': ['Observe native processing completion: expected4741updated,0new,All recognized,No issues found; interim processing/zero counters are not final.', 'Read all9 planned native offers: one per changed AUD price group plus the6protected offers. Verify exact offer identity,price,In stock,Approved,Australia,and Free listings.', 'Capture receipt timestamps and obtain independent after-review. No blanket buyer-path claim or automatic stale-data rollback.'], 'limits': summary['limits'], 'external_calls': 0, 'external_writes': 0}
    save('review.json', review)
print(json.dumps({k: summary[k] for k in ['decision', 'check_count', 'passed_count', 'failures', 'source_completed_at', 'upload_deadline_utc', 'parents', 'variants_all_aud_prices_checked', 'candidate_rows', 'candidate_parents', 'exclusion_counts', 'price_groups', 'unchanged_whole_rows', 'source_requests']} | {'review_sha256': digest(OUT / 'review.json') if (OUT / 'review.json').exists() else None, 'summary_sha256': digest(OUT / 'summary.json')}))
