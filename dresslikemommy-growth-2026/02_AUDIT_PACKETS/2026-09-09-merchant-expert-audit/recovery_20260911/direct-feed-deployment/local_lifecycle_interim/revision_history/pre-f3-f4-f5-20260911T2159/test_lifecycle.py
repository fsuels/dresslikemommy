"""Offline conflict, scope, and ambiguous-outcome tests for the local publisher."""
import copy
import csv
import datetime as dt
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import urllib.error

import lifecycle as app


def feed(price='22.99 USD'):
    row = {name: '' for name in app.HEADERS}
    row.update(id='shopify_US_1_2', item_group_id='shopify_US_1', title='Fixture', description='Fixture',
               link='https://www.dresslikemommy.com/products/fixture?variant=2',
               image_link='https://cdn.shopify.com/fixture.png', price=price,
               availability='in_stock', excluded_destination='Shopping_ads')
    file = io.StringIO()
    writer = csv.DictWriter(file, fieldnames=app.HEADERS, delimiter='\t', lineterminator='\n')
    writer.writeheader(); writer.writerow(row)
    return file.getvalue().encode()


def manifest(body, timestamp):
    digest = hashlib.md5(body).hexdigest()
    return {'schemaVersion': 1, 'market': app.MARKET, 'sha256': app.sha(body), 'objectEtag': digest,
            'expectedMd5': digest, 'objectKey': 'merchant/us-en/' + app.sha(body) + '.tsv',
            'bytes': len(body), 'rows': 1, 'rowIds': ['shopify_US_1_2'], 'sourceCompletedAt': timestamp}


class FakeApi:
    def __init__(self, before, body):
        self.objects = {app.POINTER: app.encode(before), before['objectKey']: body}
        self.writes = []
        self.worker_data = {'fixture': 'unchanged'}
        self.drift_on_object_put = False
        self.corrupt_object_readback = False
        self.pointer_timeout = None
        self.object_timeout = False
        self.on_object_put = None
        self.weak_gzip_transport_etag = False

    def get(self, key):
        if key not in self.objects:
            raise urllib.error.HTTPError('https://api.cloudflare.com/', 404, 'not found', {}, None)
        body = self.objects[key]
        if self.corrupt_object_readback and key != app.POINTER and self.writes:
            body += b'bad'
        etag = '"' + hashlib.md5(body).hexdigest() + '"'
        if self.weak_gzip_transport_etag:
            etag = 'W/"' + hashlib.md5(body).hexdigest() + '-gzip"'
        return body, {'etag': etag}

    def put(self, key, body, content_type):
        self.writes.append(key)
        if key == app.POINTER:
            if self.pointer_timeout == 'before':
                raise TimeoutError()
            if self.pointer_timeout == 'auth':
                raise urllib.error.HTTPError('https://api.cloudflare.com/', 403, 'forbidden', {}, None)
        self.objects[key] = body
        if key != app.POINTER and self.drift_on_object_put:
            changed = json.loads(self.objects[app.POINTER]); changed['fixture_external_change'] = True
            self.objects[app.POINTER] = app.encode(changed)
        if key != app.POINTER and self.object_timeout:
            raise TimeoutError()
        if key != app.POINTER and self.on_object_put:
            self.on_object_put()
        if key == app.POINTER and self.pointer_timeout == 'after':
            raise TimeoutError()
        return b'{}', {}

    def workers(self):
        return copy.deepcopy(self.worker_data)


class PublisherTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.run = Path(self.temp.name)
        self.before_body = feed(); self.body = feed('23.99 USD')
        self.before = manifest(self.before_body, '2026-09-11T10:00:00Z')
        self.after = manifest(self.body, '2026-09-11T11:00:00Z')
        self.api = FakeApi(self.before, self.before_body)
        (self.run / 'candidate').mkdir()
        self.write_candidate()
        app.save(self.run / 'prepare.json', {'pointer_sha256': app.sha(app.encode(self.before)), 'workers': self.api.workers()})
        self.review_packet = {'before_pointer_sha256': app.sha(app.encode(self.before)), 'source_completed_at': app.stamp()}

    def tearDown(self):
        self.temp.cleanup()

    def write_candidate(self):
        (self.run / 'candidate/us-en.manifest.json').write_bytes(app.encode(self.after))
        (self.run / 'candidate/us-en.tsv').write_bytes(self.body)

    def promote(self):
        # Candidate/source reconciliation is separately tested with a real frozen
        # manifest and independently reviewed for the actual live run.
        with patch.object(app, 'validate_review', return_value=self.review_packet):
            return app.promote(self.api, self.run, self.run / 'independent.json', 'fixture')

    def test_changed_object_uploaded_then_pointer(self):
        result = self.promote()
        self.assertEqual(result['status'], 'COMMITTED_VERIFIED')
        self.assertEqual(self.api.writes, [self.after['objectKey'], app.POINTER])

    def test_unchanged_bytes_reuse_object_and_renew_only_fresh_manifest(self):
        self.body = self.before_body; self.after = manifest(self.body, '2026-09-11T11:00:00Z'); self.write_candidate()
        self.assertTrue(self.promote()['object_reused'])
        self.assertEqual(self.api.writes, [app.POINTER])

    def test_pointer_drift_before_any_write_stops(self):
        self.api.objects[app.POINTER] += b' '
        with self.assertRaisesRegex(app.Stop, 'remote_pointer_drift'):
            self.promote()
        self.assertEqual(self.api.writes, [])

    def test_pointer_drift_during_object_upload_preserved(self):
        self.api.drift_on_object_put = True
        with self.assertRaisesRegex(app.Stop, 'pointer_changed_during_upload'):
            self.promote()
        self.assertNotIn(app.POINTER, self.api.writes)
        self.assertTrue(json.loads(self.api.objects[app.POINTER])['fixture_external_change'])

    def test_partial_or_corrupted_object_never_promoted(self):
        self.api.corrupt_object_readback = True
        with self.assertRaisesRegex(app.Stop, 'immutable_readback_failed'):
            self.promote()
        self.assertNotIn(app.POINTER, self.api.writes)

    def test_uncertain_object_upload_does_not_retry_or_promote(self):
        self.api.object_timeout = True
        with self.assertRaises(TimeoutError):
            self.promote()
        with self.assertRaisesRegex(app.Stop, 'prior_uncertain_attempt'):
            self.promote()
        self.assertEqual(self.api.writes, [self.after['objectKey']])

    def test_uncertain_committed_pointer_is_resolved_by_reads(self):
        self.api.pointer_timeout = 'after'
        self.assertEqual(self.promote()['status'], 'COMMITTED_AFTER_UNCERTAIN_RESPONSE_VERIFIED')
        self.assertEqual(self.promote()['status'], 'ALREADY_COMMITTED_VERIFIED')
        self.assertEqual(self.api.writes.count(app.POINTER), 1)

    def test_uncertain_uncommitted_pointer_is_not_blindly_retried(self):
        self.api.pointer_timeout = 'before'
        with self.assertRaisesRegex(app.Stop, 'after_pointer_mismatch'):
            self.promote()
        with self.assertRaisesRegex(app.Stop, 'prior_uncertain_attempt'):
            self.promote()
        self.assertEqual(self.api.objects[app.POINTER], app.encode(self.before))
        self.assertEqual(self.api.writes.count(app.POINTER), 1)

    def test_explicit_403_is_a_stop(self):
        self.api.pointer_timeout = 'auth'
        with self.assertRaises(urllib.error.HTTPError) as error:
            self.promote()
        self.assertEqual(error.exception.code, 403)

    def test_worker_change_stops_before_write(self):
        self.api.worker_data['fixture'] = 'changed'
        with self.assertRaisesRegex(app.Stop, 'worker_metadata_drift'):
            self.promote()
        self.assertEqual(self.api.writes, [])

    def test_wrong_market_rejected(self):
        wrong = copy.deepcopy(self.after); wrong['market']['country'] = 'CA'
        with self.assertRaisesRegex(app.Stop, 'manifest_market_mismatch'):
            app.validate_manifest(wrong, self.body)

    def test_empty_or_wrong_count_rejected(self):
        wrong = dict(self.after, rows=0)
        with self.assertRaisesRegex(app.Stop, 'zero_or_wrong_row_count'):
            app.validate_manifest(wrong, self.body)

    def test_redirect_refused_before_following(self):
        with self.assertRaisesRegex(app.Stop, 'redirect_refused'):
            app.NoRedirect().redirect_request(None, None, 302, '', {}, 'https://elsewhere.example/')

    def test_exclusive_process_lock(self):
        path = self.run / 'fixture.lock'
        with app.writer_lock(path):
            with self.assertRaisesRegex(app.Stop, 'another_local_us_feed_writer_active'):
                with app.writer_lock(path):
                    self.fail('concurrent writer acquired lock')

    def test_independent_review_hash_required(self):
        path = self.run / 'review.json'; path.write_text('{}')
        with self.assertRaisesRegex(app.Stop, 'independent_review_hash_mismatch'):
            app.validate_review(self.run, path, 'not-the-real-hash')

    def test_review_binds_candidate_and_lifecycle_authority(self):
        packet = {key: 'fixture' for key in ('eligibility_holds_sha256', 'cohort_filter_sha256',
            'containment_receipt_sha256', 'prepare_receipt_sha256', 'live_build_receipt_sha256',
            'live_build_intent_sha256', 'before_pointer_sha256', 'candidate_manifest_sha256',
            'candidate_feed_sha256', 'candidate_snapshot_sha256', 'candidate_diagnostics_sha256',
            'uploader_sha256', 'config_sha256', 'builder_freeze_sha256', 'source_completed_at')}
        packet.update(prices_above_1000_usd=[], mass_removal_review_required=False, delta={'added_ids': []})
        review = {**packet, 'decision': 'APPROVE_EXACT_US_FEED_POINTER', 'independent': True,
                  'reviewer': 'independent-reviewer', 'source_eligibility_and_all_prices_verified': True,
                  'single_writer_claim_verified': True, 'source_eligibility_holds_verified': True}
        path = self.run / 'review.json'; path.write_bytes(app.encode(review))
        with patch.object(app, 'candidate', return_value=packet):
            self.assertEqual(app.validate_review(self.run, path, app.sha(path.read_bytes())), packet)
            review['candidate_feed_sha256'] = 'different'; path.write_bytes(app.encode(review))
            with self.assertRaisesRegex(app.Stop, 'independent_review_binding_mismatch'):
                app.validate_review(self.run, path, app.sha(path.read_bytes()))

    def source_fixture(self):
        before = app.encode(self.before)
        (self.run / 'before.pointer.json').write_bytes(before)
        (self.run / 'before.tsv').write_bytes(self.before_body)
        prepared = app.read(self.run / 'prepare.json'); prepared['before_feed_sha256'] = app.sha(self.before_body)
        (self.run / 'prepare.json').write_bytes(app.encode(prepared))
        snapshot = {'shop': {'id': 'gid://shopify/Shop/15571635'}, 'market': app.MARKET,
                    'paginationComplete': True, 'startedAt': '2026-09-11T10:31:00Z',
                    'completedAt': self.after['sourceCompletedAt'],
                    'activeCount': {'count': 1, 'precision': 'EXACT'},
                    'finalActiveCount': {'count': 1, 'precision': 'EXACT'},
                    'products': [{'id': 'gid://shopify/Product/1', 'variants': [{'id': 'gid://shopify/ProductVariant/2'}]}]}
        self.after.update(sourceParents=1, sourceVariants=1); self.write_candidate()
        app.save(self.run / 'candidate/us-en.snapshot.json', snapshot)
        app.save(self.run / 'candidate/us-en.diagnostics.json', {'errors': [], 'rows': 1,
                 'returnPolicyLabelsEmitted': False, 'lifecycle': {'added': [], 'removed': []}})
        app.save(self.run / 'build.intent.json', {'live': True})
        app.save(self.run / 'build.json', {'live': True, 'returncode': 0,
                 'started_at_utc': '2026-09-11T10:30:00Z', 'finished_at_utc': '2026-09-11T11:01:00Z'})

    def test_fresh_source_packet_and_true_price_delta(self):
        self.source_fixture()
        app.contain(self.run)
        with patch.object(app, 'now', return_value=dt.datetime(2026, 9, 11, 11, 2, tzinfo=dt.timezone.utc)):
            packet = app.candidate(self.run)
        self.assertEqual(packet['delta']['changed_fields'], {'shopify_US_1_2': ['price']})
        self.assertFalse(packet['bytes_unchanged'])

    def test_old_snapshot_cannot_be_restamped_as_new_scan(self):
        self.source_fixture()
        path = self.run / 'candidate/us-en.snapshot.json'; snapshot = app.read(path)
        snapshot['startedAt'] = '2026-09-11T09:00:00Z'; path.write_bytes(app.encode(snapshot))
        app.contain(self.run)
        with self.assertRaisesRegex(app.Stop, 'source_not_from_this_live_run'):
            app.candidate(self.run)

    def test_candidate_source_expires_before_publication(self):
        self.source_fixture()
        app.contain(self.run)
        with patch.object(app, 'now', return_value=dt.datetime(2026, 9, 11, 13, 1, tzinfo=dt.timezone.utc)):
            with self.assertRaisesRegex(app.Stop, 'candidate_source_expired'):
                app.candidate(self.run)

    def test_incomplete_catalog_cannot_renew_existing_feed(self):
        self.source_fixture()
        path = self.run / 'candidate/us-en.snapshot.json'; snapshot = app.read(path)
        snapshot['paginationComplete'] = False; path.write_bytes(app.encode(snapshot))
        app.contain(self.run)
        with self.assertRaisesRegex(app.Stop, 'incomplete_or_invalid_source'):
            app.candidate(self.run)

    def test_source_expiring_during_upload_never_commits_pointer(self):
        self.source_fixture()
        app.contain(self.run)
        clock = [dt.datetime(2026, 9, 11, 12, 59, 59, tzinfo=dt.timezone.utc)]
        def advance():
            clock[0] = dt.datetime(2026, 9, 11, 13, 0, 1, tzinfo=dt.timezone.utc)
        self.api.on_object_put = advance
        with patch.object(app, 'now', side_effect=lambda: clock[0]):
            packet = app.candidate(self.run)
            review = {**packet, 'decision': 'APPROVE_EXACT_US_FEED_POINTER', 'independent': True,
                      'reviewer': 'independent-reviewer', 'source_eligibility_and_all_prices_verified': True,
                      'single_writer_claim_verified': True, 'source_eligibility_holds_verified': True}
            path = self.run / 'independent-review.json'; path.write_bytes(app.encode(review))
            with self.assertRaisesRegex(app.Stop, 'candidate_source_expired'):
                app.promote(self.api, self.run, path, app.sha(path.read_bytes()))
        self.assertEqual(self.api.writes, [self.after['objectKey']])
        self.assertEqual(self.api.objects[app.POINTER], app.encode(self.before))

    def test_review_changed_during_upload_never_commits_pointer(self):
        def changed(*args):
            if self.api.writes:
                raise app.Stop('independent_review_hash_mismatch')
            return self.review_packet
        with patch.object(app, 'validate_review', side_effect=changed):
            with self.assertRaisesRegex(app.Stop, 'independent_review_hash_mismatch'):
                app.promote(self.api, self.run, self.run / 'review.json', 'fixture')
        self.assertNotIn(app.POINTER, self.api.writes)

    def test_recorded_weak_gzip_etag_with_exact_bytes_is_accepted(self):
        self.api.weak_gzip_transport_etag = True
        self.assertEqual(self.promote()['status'], 'COMMITTED_VERIFIED')
        self.assertEqual(self.api.writes, [self.after['objectKey'], app.POINTER])

    def test_weak_gzip_etag_wrong_hash_is_rejected(self):
        with self.assertRaisesRegex(app.Stop, 'remote_object_transport_etag_mismatch'):
            app.verify_object_transport(self.after, self.body, {'etag': 'W/"' + '0' * 32 + '-gzip"'})

    def test_transport_etag_never_substitutes_for_full_body_hash(self):
        etag = 'W/"' + self.after['objectEtag'] + '-gzip"'
        with self.assertRaisesRegex(app.Stop, 'remote_object_hash_mismatch'):
            app.verify_object_transport(self.after, self.body + b'bad', {'etag': etag})

    def test_unrecorded_or_malformed_transport_etag_rejected(self):
        for etag in (None, self.after['objectEtag'], 'W/"' + self.after['objectEtag'] + '-br"',
                     'W/"' + self.after['objectEtag'] + '"', '"malformed"'):
            with self.subTest(etag=etag):
                with self.assertRaisesRegex(app.Stop, 'remote_object_transport_etag_mismatch'):
                    app.verify_object_transport(self.after, self.body, {'etag': etag})

    def test_known_hold_layer_required_before_review(self):
        self.source_fixture()
        with self.assertRaisesRegex(app.Stop, 'known_eligibility_holds_not_applied'):
            app.candidate(self.run)

    def test_changed_hold_file_invalidates_containment(self):
        self.source_fixture(); app.contain(self.run)
        path = self.run / 'eligibility_holds.json'; changed = app.read(path)
        changed['holds'] = []; path.write_bytes(app.encode(changed))
        with self.assertRaisesRegex(app.Stop, 'hold_spec_changed'):
            app.verify_containment(self.run)

    def test_unfiltered_evidence_and_filtered_rows_are_bound(self):
        self.source_fixture(); app.contain(self.run)
        path = self.run / 'candidate/us-en.tsv'; path.write_bytes(path.read_bytes().replace(b'23.99', b'24.99'))
        with self.assertRaisesRegex(app.Stop, 'containment_not_exact'):
            app.verify_containment(self.run)

    def test_reviewed_local_hold_revision_preserves_prior_evidence(self):
        self.source_fixture(); app.contain(self.run)
        before = (self.run / 'candidate/us-en.tsv').read_bytes()
        old_holds = (self.run / 'eligibility_holds.json').read_bytes()
        revised = json.loads(old_holds)
        revised['holds'].append({'product_id': 'gid://shopify/Product/999', 'reason': 'New reviewed fixture hold',
                                'evidence': ['fixture'], 'release_condition': 'Fixture repaired'})
        path = self.run / 'new-holds.json'; path.write_bytes(app.encode(revised))
        app.contain(self.run, path, revise=True)
        history = self.run / 'containment_history' / app.sha(old_holds)
        self.assertEqual((history / 'us-en.tsv').read_bytes(), before)
        self.assertEqual((history / 'eligibility_holds.json').read_bytes(), old_holds)
        self.assertEqual((self.run / 'unfiltered/us-en.tsv').read_bytes(), self.body)
        app.verify_containment(self.run)
        with self.assertRaisesRegex(app.Stop, 'no_hold_revision_change'):
            app.contain(self.run, path, revise=True)


if __name__ == '__main__':
    unittest.main()
