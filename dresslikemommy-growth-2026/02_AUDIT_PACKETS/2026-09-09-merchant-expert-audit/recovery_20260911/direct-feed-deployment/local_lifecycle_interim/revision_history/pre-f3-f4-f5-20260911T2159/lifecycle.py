"""Bounded local successor to the reviewed US feed uploader; no scheduler/deploy.

prepare -> build -> independent review -> promote -> readback.
Only this executable may publish merchant/us-en/current.json while the Merchant
single-writer claim is held. The lock excludes local concurrent executions;
remote compare-before-write is a drift check, not a claimed server-side CAS.
"""
from __future__ import annotations

import argparse
import base64
import contextlib
import csv
import datetime as dt
import decimal
import fcntl
import hashlib
import io
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request

from cohort_filter import apply_holds

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
RELEASE = BASE / 'automation_release_v1'
PRIVATE = Path('/Users/fsuels/.config/dresslikemommy')
NODE = Path('/Users/fsuels/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node')
ACCOUNT = '6b1df53f8a1ce4b5b5312f833a2cd966'
BUCKET = 'dlm-merchant-feeds'
POINTER = 'merchant/us-en/current.json'
PUBLIC_URL = 'https://dlm-merchant-feed-worker.dresslikemommy.workers.dev/feeds/us-en.tsv'
HOLD_SPEC = HERE / 'eligibility_holds_20260911.json'
COHORT_CODE = HERE / 'cohort_filter.py'
CONFIG_SHA = '83ab7abf281a88e4efb9cd21fbe6c4d8923aaa65d9ef400da2c8eb16f847b07b'
FREEZE_SHA = '1837f202c7c49d78ef4669c320e29e87682ff3811fabfd5ac39e5be863ccffed'
MARKET = {'key': 'us-en', 'country': 'US', 'locale': 'en', 'currency': 'USD',
          'marketId': 'gid://shopify/Market/544735329'}
HEADERS = ['id', 'item_group_id', 'title', 'description', 'link', 'image_link',
           'availability', 'price', 'condition', 'brand', 'gtin', 'mpn',
           'identifier_exists', 'age_group', 'gender', 'color', 'size', 'excluded_destination']


class Stop(RuntimeError):
    """Public, non-secret diagnostic code only."""


def require(ok, code):
    if not ok:
        raise Stop(code)


def now():
    return dt.datetime.now(dt.timezone.utc)


def stamp():
    return now().isoformat()


def time_value(value):
    return dt.datetime.fromisoformat(value.replace('Z', '+00:00'))


def sha(body):
    return hashlib.sha256(body).hexdigest()


def encode(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def read(path):
    return json.loads(path.read_bytes())


def save(path, value):
    # Exclusive evidence creation makes repeated/ambiguous commands visible.
    with path.open('x') as file:
        json.dump(value, file, indent=2)
        file.write('\n')


@contextlib.contextmanager
def writer_lock(lock_path=None):
    path = lock_path or PRIVATE / 'merchant-us-feed-writer.lock'
    fd = os.open(path, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
    try:
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise Stop('another_local_us_feed_writer_active') from None
        yield
    finally:
        os.close(fd)


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise Stop('redirect_refused')


class Cloudflare:
    def __init__(self):
        values = {}
        for line in (PRIVATE / 'cloudflare.env').read_text().splitlines():
            match = re.match(r'\s*(?:export\s+)?(CLOUDFLARE_API_TOKEN|CLOUDFLARE_ACCOUNT_ID)\s*=\s*(.*)$', line)
            if match:
                value = shlex.split(match[2], comments=True)
                require(len(value) == 1, 'private_cloudflare_config_invalid')
                values[match[1]] = value[0]
        require(values.get('CLOUDFLARE_ACCOUNT_ID') == ACCOUNT, 'cloudflare_account_mismatch')
        require(bool(values.get('CLOUDFLARE_API_TOKEN')), 'cloudflare_token_unavailable')
        self.token = values['CLOUDFLARE_API_TOKEN']
        self.opener = urllib.request.build_opener(NoRedirect())

    def request(self, suffix, method='GET', body=None, content_type=None):
        require(suffix.startswith(('/r2/buckets/' + BUCKET + '/objects/', '/workers/scripts')), 'endpoint_out_of_scope')
        url = 'https://api.cloudflare.com/client/v4/accounts/' + ACCOUNT + suffix
        headers = {'Authorization': 'Bearer ' + self.token}
        if body is not None:
            headers.update({'Content-Type': content_type,
                            'Content-MD5': base64.b64encode(hashlib.md5(body).digest()).decode(),
                            'cf-r2-data-catalog-check': 'true'})
        request = urllib.request.Request(url, data=body, headers=headers, method=method)
        with self.opener.open(request, timeout=55) as response:
            return response.read(), {k.lower(): v for k, v in response.headers.items()}

    def get(self, key):
        require(key == POINTER or re.fullmatch(r'merchant/us-en/[a-f0-9]{64}\.tsv', key), 'object_key_out_of_scope')
        return self.request('/r2/buckets/' + BUCKET + '/objects/' + urllib.parse.quote(key, safe='/'))

    def put(self, key, body, content_type):
        require(key == POINTER or key == 'merchant/us-en/' + sha(body) + '.tsv', 'write_key_out_of_scope')
        return self.request('/r2/buckets/' + BUCKET + '/objects/' + urllib.parse.quote(key, safe='/'), 'PUT', body, content_type)

    def workers(self):
        raw, _ = self.request('/workers/scripts')
        data = json.loads(raw)
        require(data.get('success') is True, 'worker_metadata_read_failed')
        result = {v['id']: {k: v.get(k) for k in ('id', 'etag', 'created_on', 'modified_on')}
                  for v in data['result'] if v['id'] in ('dlm-merchant-feed-worker', 'dlm-pinterest-feed-worker')}
        require(len(result) == 2, 'expected_worker_metadata_missing')
        return result

    def public(self):
        # Public source bytes only. The Cloudflare credential is not attached.
        request = urllib.request.Request(PUBLIC_URL, headers={'Cache-Control': 'no-cache'})
        with self.opener.open(request, timeout=55) as response:
            return response.read(), {k.lower(): v for k, v in response.headers.items()}


def verify_freeze():
    manifest_path = RELEASE / 'freeze_manifest.json'
    require(sha(manifest_path.read_bytes()) == FREEZE_SHA, 'builder_freeze_manifest_drift')
    for item in read(manifest_path)['files']:
        path = RELEASE / item['path']
        require(path.resolve().is_relative_to(RELEASE.resolve()), 'freeze_path_out_of_scope')
        require(sha(path.read_bytes()) == item['sha256'], 'frozen_builder_file_drift')
    require(sha((RELEASE / 'config.json').read_bytes()) == CONFIG_SHA, 'us_config_drift')


def validate_manifest(manifest, body):
    require(manifest.get('schemaVersion') == 1 and manifest.get('market') == MARKET, 'manifest_market_mismatch')
    require(manifest['sha256'] == sha(body) and manifest['bytes'] == len(body) <= 60_000_000, 'feed_hash_or_size_mismatch')
    md5 = hashlib.md5(body).hexdigest()
    require(manifest['objectEtag'] == manifest['expectedMd5'] == md5, 'feed_md5_mismatch')
    require(manifest['objectKey'] == 'merchant/us-en/' + sha(body) + '.tsv', 'manifest_object_key_mismatch')
    reader = csv.DictReader(io.StringIO(body.decode('utf-8')), delimiter='\t')
    require(reader.fieldnames == HEADERS, 'feed_header_mismatch')
    rows = list(reader)
    require(0 < len(rows) == manifest['rows'], 'zero_or_wrong_row_count')
    require([r['id'] for r in rows] == manifest['rowIds'] and len(set(manifest['rowIds'])) == len(rows), 'feed_ids_mismatch')
    for row in rows:
        require(None not in row and all(v is not None for v in row.values()), 'malformed_tsv_row')
        match = re.fullmatch(r'shopify_US_(\d+)_(\d+)', row['id'])
        require(bool(match) and row['item_group_id'] == 'shopify_US_' + match[1], 'offer_group_mismatch')
        require(row['availability'] == 'in_stock' and row['excluded_destination'] == 'Shopping_ads', 'availability_or_paid_scope_mismatch')
        require(bool(re.fullmatch(r'\d+\.\d{2} USD', row['price'])), 'price_currency_invalid')
        require(0 < decimal.Decimal(row['price'].split()[0]), 'nonpositive_price')
        url = urllib.parse.urlsplit(row['link'])
        query = urllib.parse.parse_qs(url.query)
        require(url.scheme == 'https' and url.netloc == 'www.dresslikemommy.com' and url.path.startswith('/products/')
                and query.get('variant') == [match[2]] and not (set(query) - {'variant'}), 'landing_context_mismatch')
    return {r['id']: r for r in rows}


def compare_rows(before, after):
    added, removed = sorted(after.keys() - before.keys()), sorted(before.keys() - after.keys())
    changed = {key: [field for field in HEADERS if before[key][field] != after[key][field]]
               for key in sorted(before.keys() & after.keys()) if before[key] != after[key]}
    return {'added_ids': added, 'removed_ids': removed, 'changed_fields': changed,
            'retained_count': len(before.keys() & after.keys()),
            'unchanged_retained_count': len(before.keys() & after.keys()) - len(changed)}


def prepare(api, run, hold_path=HOLD_SPEC):
    require(not run.exists(), 'run_directory_already_exists')
    run.mkdir(mode=0o700, parents=False)
    raw, headers = api.get(POINTER)
    manifest = json.loads(raw)
    body, _ = api.get(manifest['objectKey'])
    validate_manifest(manifest, body)
    (run / 'before.pointer.json').write_bytes(raw)
    (run / 'before.tsv').write_bytes(body)
    hold_bytes = hold_path.read_bytes()
    (run / 'eligibility_holds.json').write_bytes(hold_bytes)
    save(run / 'prepare.json', {'at_utc': stamp(), 'pointer_sha256': sha(raw),
         'pointer_etag': headers.get('etag'), 'before_feed_sha256': sha(body), 'workers': api.workers(),
         'account': ACCOUNT, 'bucket': BUCKET, 'pointer': POINTER, 'merchant_source': '10727274744',
         'config_sha256': CONFIG_SHA, 'builder_freeze_sha256': FREEZE_SHA,
         'planned_eligibility_holds_sha256': sha(hold_bytes)})


def build(run):
    require((run / 'prepare.json').exists() and not (run / 'build.json').exists(), 'prepare_missing_or_build_already_attempted')
    require(not (run / 'candidate').exists(), 'candidate_directory_already_exists')
    command = [str(NODE), str(RELEASE / 'bin/build.mjs'), '--config', str(RELEASE / 'config.json'),
               '--market', 'us-en', '--live', '--previous-manifest', str(run / 'before.pointer.json'),
               '--out', str(run / 'candidate')]
    started = stamp()
    save(run / 'build.intent.json', {'started_at_utc': started, 'command': command, 'live': True})
    env = dict(os.environ)
    for key in ('SHOPIFY_ADMIN_SHOP_DOMAIN', 'SHOPIFY_STORE_DOMAIN', 'SHOPIFY_ADMIN_API_TOKEN',
                'SHOPIFY_ADMIN_ACCESS_TOKEN', 'SHOPIFY_ADMIN_TOKEN'):
        env.pop(key, None)
    result = subprocess.run(command, capture_output=True, text=True, timeout=900, env=env)
    # The frozen builder only emits sanitized counters/error codes. No raw payloads.
    save(run / 'build.json', {'started_at_utc': started, 'finished_at_utc': stamp(), 'returncode': result.returncode,
                            'stdout': result.stdout, 'stderr': result.stderr, 'live': True})
    require(result.returncode == 0, 'fresh_source_build_failed')
    contain(run)
    summary = candidate(run)
    save(run / 'candidate_review_packet.json', summary)


def contain(run, hold_path=HOLD_SPEC, revise=False):
    """Contain the completed local scan, preserving its original four files."""
    previous_receipt = None
    if revise:
        verify_containment(run)
        previous_receipt = read(run / 'contain.receipt.json')
        original = run / 'unfiltered'
    else:
        require(not (run / 'contain.receipt.json').exists() and not (run / 'unfiltered').exists(), 'containment_already_attempted')
        original = run / 'candidate'
    require(read(run / 'build.json')['returncode'] == 0, 'successful_build_required_before_containment')
    hold_copy = run / 'eligibility_holds.json'
    if not hold_copy.exists():
        hold_copy.write_bytes(hold_path.read_bytes())
    hold_bytes = hold_path.read_bytes() if revise else hold_copy.read_bytes()
    if revise:
        require(sha(hold_bytes) != previous_receipt['hold_spec_sha256'], 'no_hold_revision_change')
    planned = read(run / 'prepare.json').get('planned_eligibility_holds_sha256')
    require(revise or planned is None or planned == sha(hold_bytes), 'planned_hold_spec_changed')
    raw_manifest = read(original / 'us-en.manifest.json')
    raw_body = (original / 'us-en.tsv').read_bytes()
    validate_manifest(raw_manifest, raw_body)
    output, manifest, diagnostics = apply_holds(raw_body, raw_manifest,
        read(original / 'us-en.diagnostics.json'), hold_bytes, read(run / 'before.pointer.json')['rowIds'])
    source_files = ('us-en.tsv', 'us-en.manifest.json', 'us-en.diagnostics.json', 'us-en.snapshot.json')
    hashes = {name: sha((original / name).read_bytes()) for name in source_files}
    if revise:
        history = run / 'containment_history' / previous_receipt['hold_spec_sha256']
        history.mkdir(parents=True, exist_ok=False)
        for name in source_files:
            shutil.copy2(run / 'candidate' / name, history / name)
        shutil.copy2(hold_copy, history / 'eligibility_holds.json')
        shutil.copy2(run / 'contain.receipt.json', history / 'contain.receipt.json')
        hold_copy.write_bytes(hold_bytes)
    else:
        unfiltered = run / 'unfiltered'; unfiltered.mkdir()
        for name in source_files:
            shutil.copy2(original / name, unfiltered / name)
    destination = run / 'candidate'
    # A partial local write cannot pass the deterministic proof below or publish.
    (destination / 'us-en.tsv').write_bytes(output)
    (destination / 'us-en.manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    (destination / 'us-en.diagnostics.json').write_text(json.dumps(diagnostics, indent=2) + '\n')
    receipt = {'at_utc': stamp(), 'original_files': hashes,
         'hold_spec_sha256': sha(hold_bytes), 'cohort_filter_sha256': sha(COHORT_CODE.read_bytes()),
         'result': diagnostics['eligibilityHolds'], 'source_scan_reused_without_restamping': True}
    if revise:
        receipt['previous_containment_evidence'] = str(history.relative_to(run))
        (run / 'contain.receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    else:
        save(run / 'contain.receipt.json', receipt)


def verify_containment(run):
    require((run / 'contain.receipt.json').exists(), 'known_eligibility_holds_not_applied')
    receipt = read(run / 'contain.receipt.json')
    hold_bytes = (run / 'eligibility_holds.json').read_bytes()
    require(sha(hold_bytes) == receipt['hold_spec_sha256'], 'hold_spec_changed')
    require(sha(COHORT_CODE.read_bytes()) == receipt['cohort_filter_sha256'], 'cohort_filter_code_changed')
    raw, filtered = run / 'unfiltered', run / 'candidate'
    require(all(sha((raw / name).read_bytes()) == value for name, value in receipt['original_files'].items()), 'unfiltered_source_changed')
    output, manifest, diagnostics = apply_holds((raw / 'us-en.tsv').read_bytes(), read(raw / 'us-en.manifest.json'),
        read(raw / 'us-en.diagnostics.json'), hold_bytes, read(run / 'before.pointer.json')['rowIds'])
    require(output == (filtered / 'us-en.tsv').read_bytes() and manifest == read(filtered / 'us-en.manifest.json')
            and diagnostics == read(filtered / 'us-en.diagnostics.json'), 'containment_not_exact')
    require((filtered / 'us-en.snapshot.json').read_bytes() == (raw / 'us-en.snapshot.json').read_bytes(), 'containment_changed_source_snapshot')
    return receipt


def candidate(run):
    prepared = read(run / 'prepare.json')
    before_raw, before_body = (run / 'before.pointer.json').read_bytes(), (run / 'before.tsv').read_bytes()
    require(sha(before_raw) == prepared['pointer_sha256'] and sha(before_body) == prepared['before_feed_sha256'], 'before_evidence_changed')
    before = validate_manifest(json.loads(before_raw), before_body)
    containment = verify_containment(run)
    directory = run / 'candidate'
    manifest = read(directory / 'us-en.manifest.json')
    body = (directory / 'us-en.tsv').read_bytes()
    after = validate_manifest(manifest, body)
    source_path = directory / 'us-en.snapshot.json'
    snapshot = read(source_path)
    diagnostics = read(directory / 'us-en.diagnostics.json')
    receipt = read(run / 'build.json')
    require(receipt['live'] is True and receipt['returncode'] == 0, 'successful_live_scan_required')
    require(snapshot['shop']['id'] == 'gid://shopify/Shop/15571635' and snapshot['market'] == MARKET, 'snapshot_identity_mismatch')
    require(snapshot['paginationComplete'] is True and not diagnostics['errors'], 'incomplete_or_invalid_source')
    require(time_value(receipt['started_at_utc']) <= time_value(snapshot['startedAt']) <= time_value(snapshot['completedAt']) <= time_value(receipt['finished_at_utc']), 'source_not_from_this_live_run')
    age = (now() - time_value(snapshot['completedAt'])).total_seconds()
    require(-60 <= age <= 7200, 'candidate_source_expired')
    require(manifest['sourceCompletedAt'] == snapshot['completedAt'] and manifest['rows'] == diagnostics['rows'], 'source_manifest_mismatch')
    require(snapshot['activeCount'] == snapshot['finalActiveCount'] == {'count': len(snapshot['products']), 'precision': 'EXACT'}, 'active_count_mismatch')
    require(len(snapshot['products']) == manifest['sourceParents'] and sum(len(p['variants']) for p in snapshot['products']) == manifest['sourceVariants'], 'source_variant_counts_mismatch')
    require(time_value(manifest['sourceCompletedAt']) > time_value(json.loads(before_raw)['sourceCompletedAt']), 'source_did_not_advance')
    require(diagnostics['returnPolicyLabelsEmitted'] is False, 'return_contract_changed')
    delta = compare_rows(before, after)
    require(sorted(diagnostics['lifecycle']['added']) == delta['added_ids'] and sorted(diagnostics['lifecycle']['removed']) == delta['removed_ids'], 'lifecycle_delta_mismatch')
    return {'status': 'CANDIDATE_REQUIRES_INDEPENDENT_REVIEW', 'market': MARKET,
            'eligibility_holds_sha256': containment['hold_spec_sha256'],
            'cohort_filter_sha256': containment['cohort_filter_sha256'],
            'containment_receipt_sha256': sha((run / 'contain.receipt.json').read_bytes()),
            'contained_available_rows': diagnostics['eligibilityHolds']['removed_available_rows'],
            'eligible_parent_count': diagnostics['eligibilityHolds']['kept_parents'],
            'prepare_receipt_sha256': sha((run / 'prepare.json').read_bytes()),
            'live_build_receipt_sha256': sha((run / 'build.json').read_bytes()),
            'live_build_intent_sha256': sha((run / 'build.intent.json').read_bytes()),
            'before_pointer_sha256': sha(before_raw), 'candidate_manifest_sha256': sha((directory / 'us-en.manifest.json').read_bytes()),
            'candidate_feed_sha256': sha(body), 'candidate_snapshot_sha256': sha(source_path.read_bytes()),
            'candidate_diagnostics_sha256': sha((directory / 'us-en.diagnostics.json').read_bytes()),
            'uploader_sha256': sha(Path(__file__).read_bytes()), 'config_sha256': CONFIG_SHA,
            'builder_freeze_sha256': FREEZE_SHA, 'source_completed_at': manifest['sourceCompletedAt'],
            'rows': len(after), 'before_rows': len(before), 'delta': delta,
            'prices_above_1000_usd': [key for key, row in after.items() if decimal.Decimal(row['price'].split()[0]) > 1000],
            'mass_removal_review_required': len(delta['removed_ids']) > max(25, len(before) * 0.1),
            'bytes_unchanged': sha(body) == sha(before_body), 'source_renewal_requires_this_fresh_scan': True}


def validate_review(run, review_path, expected_hash):
    raw = review_path.read_bytes()
    require(sha(raw) == expected_hash, 'independent_review_hash_mismatch')
    review, packet = json.loads(raw), candidate(run)
    require(review.get('decision') == 'APPROVE_EXACT_US_FEED_POINTER' and review.get('independent') is True, 'independent_approval_missing')
    require(bool(review.get('reviewer')) and review.get('reviewer') != '01a08706-c63a-7e01-ba48-7777bcb1788a', 'independent_reviewer_missing')
    fields = ('eligibility_holds_sha256', 'cohort_filter_sha256', 'containment_receipt_sha256',
              'prepare_receipt_sha256', 'live_build_receipt_sha256', 'live_build_intent_sha256',
              'before_pointer_sha256', 'candidate_manifest_sha256', 'candidate_feed_sha256', 'candidate_snapshot_sha256',
              'candidate_diagnostics_sha256', 'uploader_sha256', 'config_sha256', 'builder_freeze_sha256', 'source_completed_at')
    require(all(review.get(key) == packet[key] for key in fields), 'independent_review_binding_mismatch')
    require(review.get('source_eligibility_and_all_prices_verified') is True, 'source_reconciliation_missing')
    require(review.get('source_eligibility_holds_verified') is True, 'source_hold_review_missing')
    require(review.get('single_writer_claim_verified') is True, 'single_writer_claim_missing')
    require(not packet['prices_above_1000_usd'], 'extreme_price_requires_separate_exact_repair')
    require(not packet['mass_removal_review_required'] or review.get('mass_removal_explicitly_verified') is True, 'mass_removal_unexplained')
    require(not packet['delta']['added_ids'] or sorted(review.get('buyer_qualified_added_ids', [])) == packet['delta']['added_ids'], 'added_buyer_routes_unqualified')
    return packet


def verify_object_transport(manifest, body, headers):
    # The existing Admin REST endpoint has returned this exact weak gzip ETag
    # for decoded bytes. It is a transport validator, not the raw R2 binding ETag.
    # Preserve full SHA256/MD5 proof; accept no other transport transformation.
    expected = manifest['objectEtag']
    require(sha(body) == manifest['sha256'] and hashlib.md5(body).hexdigest() == expected,
            'remote_object_hash_mismatch')
    allowed = {'"' + expected + '"', 'W/"' + expected + '-gzip"'}
    require(headers.get('etag') in allowed, 'remote_object_transport_etag_mismatch')


def verify_remote(api, manifest, expected_workers, public=False):
    pointer, _ = api.get(POINTER)
    require(json.loads(pointer) == manifest, 'after_pointer_mismatch')
    body, headers = api.get(manifest['objectKey'])
    validate_manifest(manifest, body)
    verify_object_transport(manifest, body, headers)
    require(api.workers() == expected_workers, 'worker_metadata_changed')
    result = {'pointer_verified': True, 'immutable_verified': True, 'workers_unchanged': True, 'sha256': sha(body), 'rows': manifest['rows']}
    if public:
        published, public_headers = api.public()
        require(published == body and public_headers.get('x-dlm-feed-source-updated') == manifest['sourceCompletedAt'], 'public_host_not_current')
        require(public_headers.get('x-dlm-feed-country') == 'US' and public_headers.get('x-dlm-feed-language') == 'en'
                and public_headers.get('x-dlm-feed-currency') == 'USD', 'public_host_context_mismatch')
        result['public_verified'] = True
    return result


def promote(api, run, review_path, review_hash):
    packet = validate_review(run, review_path, review_hash)
    prepared = read(run / 'prepare.json')
    manifest = read(run / 'candidate/us-en.manifest.json')
    body = (run / 'candidate/us-en.tsv').read_bytes()
    current, _ = api.get(POINTER)
    require(api.workers() == prepared['workers'], 'worker_metadata_drift')
    if json.loads(current) == manifest:
        return {'status': 'ALREADY_COMMITTED_VERIFIED', **verify_remote(api, manifest, prepared['workers'])}
    require(sha(current) == prepared['pointer_sha256'], 'remote_pointer_drift')
    require(not (run / 'promote.intent.json').exists(), 'prior_uncertain_attempt_requires_readback')
    save(run / 'promote.intent.json', {'at_utc': stamp(), 'independent_review_sha256': review_hash,
         'before_pointer_sha256': packet['before_pointer_sha256'], 'intended_manifest_sha256': sha(encode(manifest)),
         'feed_sha256': sha(body), 'scope': 'Existing US free-listing pointer only; no scheduler/Worker/credential change'})
    object_reused = False
    try:
        existing, _ = api.get(manifest['objectKey'])
        require(existing == body, 'immutable_object_conflict')
        object_reused = True
    except urllib.error.HTTPError as error:
        if error.code != 404:
            raise
        api.put(manifest['objectKey'], body, 'text/tab-separated-values; charset=utf-8')
    received, headers = api.get(manifest['objectKey'])
    require(received == body, 'immutable_readback_failed')
    verify_object_transport(manifest, received, headers)
    require(api.workers() == prepared['workers'], 'worker_changed_before_commit')
    current, _ = api.get(POINTER)
    require(sha(current) == prepared['pointer_sha256'], 'pointer_changed_during_upload')
    # Upload latency must not consume the source/review validity window.
    # Re-read and re-bind every reviewed local artifact immediately before PUT.
    final_packet = validate_review(run, review_path, review_hash)
    require(final_packet == packet, 'candidate_changed_during_upload')
    final_age = (now() - time_value(final_packet['source_completed_at'])).total_seconds()
    require(-60 <= final_age <= 7200, 'candidate_source_expired_before_commit')
    # Local lock + explicit sole-writer claim spans this before-read and commit.
    # No remote CAS support is asserted for this documented REST endpoint.
    try:
        api.put(POINTER, encode(manifest), 'application/json')
    except urllib.error.HTTPError:
        # An explicit auth/permission or provider error is a stop, not a retry.
        raise
    except (urllib.error.URLError, TimeoutError, ConnectionError, OSError):
        # Resolve an ambiguous commit with reads only. Never repeat PUT.
        resolved = verify_remote(api, manifest, prepared['workers'])
        return {'status': 'COMMITTED_AFTER_UNCERTAIN_RESPONSE_VERIFIED', 'object_reused': object_reused, **resolved}
    return {'status': 'COMMITTED_VERIFIED', 'object_reused': object_reused,
            **verify_remote(api, manifest, prepared['workers'])}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('phase', choices=('prepare', 'build', 'contain', 'revise-containment', 'inspect', 'promote', 'readback'))
    parser.add_argument('--run', required=True)
    parser.add_argument('--review')
    parser.add_argument('--review-sha256')
    args = parser.parse_args()
    run = Path(args.run).resolve()
    require(run.parent == (HERE / 'runs').resolve() and re.fullmatch(r'\d{8}T\d{6}Z-[a-z0-9-]+', run.name), 'run_path_out_of_scope')
    require(not Path(args.run).is_symlink(), 'run_symlink_refused')
    verify_freeze()
    with writer_lock():
        if args.phase == 'prepare':
            prepare(Cloudflare(), run)
            result = {'status': 'REMOTE_BEFORE_STATE_PREPARED'}
        elif args.phase == 'build':
            build(run)
            result = {'status': 'FRESH_LIVE_CANDIDATE_BUILT_REVIEW_REQUIRED'}
        elif args.phase == 'contain':
            contain(run)
            result = {'status': 'LOCAL_EXACT_ELIGIBILITY_HOLDS_APPLIED_REVIEW_REQUIRED'}
        elif args.phase == 'revise-containment':
            contain(run, revise=True)
            result = {'status': 'LOCAL_HOLD_REVISION_PREPARED_PREVIOUS_EVIDENCE_PRESERVED'}
        elif args.phase == 'inspect':
            result = candidate(run)
        elif args.phase == 'promote':
            require(bool(args.review and args.review_sha256), 'review_arguments_required')
            result = promote(Cloudflare(), run, Path(args.review).resolve(), args.review_sha256)
        else:
            result = {'status': 'AFTER_STATE_AND_PUBLIC_HOST_VERIFIED', **verify_remote(Cloudflare(),
                      read(run / 'candidate/us-en.manifest.json'), read(run / 'prepare.json')['workers'], public=True)}
        result.update(at_utc=stamp(), phase=args.phase, google_receipt='NOT_INFERRED_FROM_HOSTED_READBACK',
                      shopify_credential_transferred=False, worker_or_scheduler_changed=False)
        if args.phase != 'inspect':
            save(run / (args.phase + '.result-' + now().strftime('%Y%m%dT%H%M%S%fZ') + '.json'), result)
        print(json.dumps(result))


if __name__ == '__main__':
    try:
        main()
    except urllib.error.HTTPError as error:
        print(json.dumps({'status': 'STOPPED', 'code': 'http_' + str(error.code)})); sys.exit(1)
    except Stop as error:
        print(json.dumps({'status': 'STOPPED', 'code': str(error)})); sys.exit(1)
    except Exception as error:
        # Avoid URL/token or provider body leakage from exception text.
        print(json.dumps({'status': 'STOPPED', 'code': type(error).__name__})); sys.exit(1)
