"""Independent synthetic failure cases; all writes stay in this review packet."""
import datetime as dt
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import lifecycle as app
from test_lifecycle import FakeApi

OUT = Path(__file__).resolve().parent


class IndependentNativeCases(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=OUT / 'tmp')
        self.run = Path(self.temp.name)
        self.addCleanup(self.temp.cleanup)
        app.select_release_profile('native-holds-20260914')
        self.addCleanup(lambda: app.select_release_profile('legacy'))
        self.time = dt.datetime(2026, 9, 14, 20, 30, tzinfo=dt.timezone.utc)
        clock = patch.object(app, 'now', side_effect=lambda: self.time)
        clock.start(); self.addCleanup(clock.stop)

    def fixture(self, scenario='protected-unavailable', directory=None):
        run = directory or self.run
        result = subprocess.run([str(app.NODE), str(app.HERE / 'native_profile_fixture.mjs'), str(run), scenario],
                                capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
        shutil.copy2(app.HOLD_SPEC, run / 'eligibility_holds.json')
        app.save(run / 'prepare.json', {
            'pointer_sha256': app.sha((run / 'before.pointer.json').read_bytes()),
            'before_feed_sha256': app.sha((run / 'before.tsv').read_bytes()),
            'workers': {'fixture': 'unchanged'}, 'release_profile': app.RELEASE_PROFILE,
            'config_sha256': app.CONFIG_SHA, 'builder_freeze_sha256': app.FREEZE_SHA,
            'planned_eligibility_holds_sha256': app.sha(app.HOLD_SPEC.read_bytes())})
        app.save(run / 'build.intent.json', {'live': True, 'synthetic': True})
        app.save(run / 'build.json', {'live': True, 'synthetic': True, 'returncode': 0,
            'started_at_utc': '2026-09-14T19:59:00Z', 'finished_at_utc': '2026-09-14T20:01:00Z'})
        app.contain(run)
        return app.candidate(run)

    def approved(self):
        packet = self.fixture()
        review = {**packet, 'decision': 'APPROVE_EXACT_US_FEED_POINTER',
                  'independent': True, 'reviewer': 'synthetic-independent-native-failure-review',
                  'source_eligibility_and_all_prices_verified': True,
                  'source_eligibility_holds_verified': True, 'single_writer_claim_verified': True,
                  'protected_omissions_verified': packet['protected_omissions']}
        review_path = self.run / 'synthetic-exact-review.json'
        review_path.write_bytes(app.encode(review))
        before_bytes = (self.run / 'before.pointer.json').read_bytes()
        api = FakeApi(json.loads(before_bytes), (self.run / 'before.tsv').read_bytes())
        # The real before-read binds transport bytes, not just JSON semantics.
        api.objects[app.POINTER] = before_bytes
        return api, review_path, app.sha(review_path.read_bytes())

    def test_dependency_drift_before_upload_blocks_every_put(self):
        api, review, digest = self.approved()
        original = app.sha
        target = (app.RELEASE / 'bin/build.mjs').read_bytes()
        with patch.object(app, 'sha', side_effect=lambda raw: '0' * 64 if raw == target else original(raw)):
            with self.assertRaisesRegex(app.Stop, 'release_profile_dependency_drift'):
                app.promote(api, self.run, review, digest)
        self.assertEqual(api.writes, [])

    def test_dependency_drift_after_immutable_upload_blocks_pointer(self):
        api, review, digest = self.approved()
        original = app.sha
        target = (app.RELEASE / 'src/generator.js').read_bytes()
        changed = False
        def drift():
            nonlocal changed
            changed = True
        api.on_object_put = drift
        with patch.object(app, 'sha', side_effect=lambda raw: '0' * 64 if changed and raw == target else original(raw)):
            with self.assertRaisesRegex(app.Stop, 'release_profile_dependency_drift'):
                app.promote(api, self.run, review, digest)
        self.assertTrue(changed)
        self.assertEqual(len(api.writes), 1)
        self.assertNotIn(app.POINTER, api.writes)

    def test_uncertain_committed_pointer_resolves_without_second_put(self):
        api, review, digest = self.approved()
        api.pointer_timeout = 'after'
        result = app.promote(api, self.run, review, digest)
        self.assertEqual(result['status'], 'COMMITTED_AFTER_UNCERTAIN_RESPONSE_VERIFIED')
        self.assertEqual(app.promote(api, self.run, review, digest)['status'], 'ALREADY_COMMITTED_VERIFIED')
        self.assertEqual(api.writes.count(app.POINTER), 1)

    def test_uncertain_uncommitted_pointer_cannot_be_blindly_retried(self):
        api, review, digest = self.approved()
        original = api.objects[app.POINTER]
        api.pointer_timeout = 'before'
        with self.assertRaisesRegex(app.Stop, 'after_pointer_mismatch'):
            app.promote(api, self.run, review, digest)
        with self.assertRaisesRegex(app.Stop, 'prior_uncertain_attempt'):
            app.promote(api, self.run, review, digest)
        self.assertEqual(api.writes.count(app.POINTER), 1)
        self.assertEqual(api.objects[app.POINTER], original)

    def test_source_expiry_during_upload_cannot_advance_pointer(self):
        api, review, digest = self.approved()
        def expire():
            self.time = dt.datetime(2026, 9, 14, 22, 0, 0, 1000, tzinfo=dt.timezone.utc)
        api.on_object_put = expire
        with self.assertRaisesRegex(app.Stop, 'candidate_source_expired'):
            app.promote(api, self.run, review, digest)
        self.assertEqual(len(api.writes), 1)
        self.assertNotIn(app.POINTER, api.writes)

    def test_replay_cannot_override_the_actual_scan_window(self):
        self.fixture()
        receipt_path = self.run / 'build.json'
        receipt = app.read(receipt_path)
        receipt['started_at_utc'] = '2026-09-14T20:00:01Z'
        receipt_path.write_bytes(app.encode(receipt))
        with self.assertRaisesRegex(app.Stop, 'source_not_from_this_live_run'):
            app.candidate(self.run)

    def test_absent_parent_reactivation_keeps_the_hold(self):
        absent = self.fixture('held-absent')
        absent_summary = app.read(self.run / 'contain.receipt.json')['native_replay']
        returned_dir = self.run / 'reactivated'
        returned = self.fixture('base', returned_dir)
        returned_summary = app.read(returned_dir / 'contain.receipt.json')['native_replay']
        held = 'gid://shopify/Product/7516369715297'
        self.assertIn(held, absent_summary['sourceAbsentHeldParentIds'])
        self.assertNotIn(held, returned_summary['sourceAbsentHeldParentIds'])
        self.assertEqual(absent['contained_available_rows'], 0)
        self.assertEqual(returned['contained_available_rows'], 1)
        self.assertEqual(absent_summary['configuredHeldParentIds'], returned_summary['configuredHeldParentIds'])
        self.assertEqual(len(returned_summary['configuredHeldParentIds']), 6)
        self.assertEqual(absent['candidate_feed_sha256'], returned['candidate_feed_sha256'])

    def test_valid_old_fields_do_not_substitute_for_native_review_binding(self):
        api, review, digest = self.approved()
        value = app.read(review)
        value['native_verifier_sha256'] = '0' * 64
        review.write_bytes(app.encode(value))
        with self.assertRaisesRegex(app.Stop, 'independent_review_profile_mismatch'):
            app.promote(api, self.run, review, app.sha(review.read_bytes()))
        self.assertEqual(api.writes, [])
