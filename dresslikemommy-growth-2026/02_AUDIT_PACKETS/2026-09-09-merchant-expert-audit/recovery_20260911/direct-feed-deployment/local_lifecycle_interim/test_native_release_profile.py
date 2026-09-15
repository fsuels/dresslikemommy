"""Offline tests of the named current profile through real generator artifacts."""
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


class NativeProfileTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.run = Path(self.temp.name)
        app.select_release_profile('native-holds-20260914')
        self.addCleanup(lambda: app.select_release_profile('legacy'))
        self.addCleanup(self.temp.cleanup)
        self.clock = patch.object(app, 'now', return_value=dt.datetime(2026, 9, 14, 20, 30, tzinfo=dt.timezone.utc))
        self.clock.start(); self.addCleanup(self.clock.stop)

    def fixture(self, scenario='base'):
        result = subprocess.run([str(app.NODE), str(app.HERE / 'native_profile_fixture.mjs'), str(self.run), scenario],
                                capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
        shutil.copy2(app.HOLD_SPEC, self.run / 'eligibility_holds.json')
        before = (self.run / 'before.pointer.json').read_bytes()
        app.save(self.run / 'prepare.json', {'pointer_sha256': app.sha(before),
            'before_feed_sha256': app.sha((self.run / 'before.tsv').read_bytes()),
            'workers': {'fixture': 'unchanged'}, 'release_profile': app.RELEASE_PROFILE,
            'config_sha256': app.CONFIG_SHA, 'builder_freeze_sha256': app.FREEZE_SHA,
            'planned_eligibility_holds_sha256': app.sha(app.HOLD_SPEC.read_bytes())})
        app.save(self.run / 'build.intent.json', {'live': True, 'synthetic': True})
        app.save(self.run / 'build.json', {'returncode': 0, 'live': True, 'synthetic': True,
            'started_at_utc': '2026-09-14T19:59:00Z', 'finished_at_utc': '2026-09-14T20:01:00Z'})

    def review(self, packet, omissions=True):
        result = {**packet, 'decision': 'APPROVE_EXACT_US_FEED_POINTER', 'independent': True,
                  'reviewer': 'synthetic-independent-reviewer', 'source_eligibility_and_all_prices_verified': True,
                  'source_eligibility_holds_verified': True, 'single_writer_claim_verified': True,
                  'protected_omissions_verified': packet['protected_omissions'] if omissions else []}
        path = self.run / 'independent-review.json'
        path.write_bytes(app.encode(result))
        return path, app.sha(path.read_bytes())

    def test_current_contract_verifies_without_modifying_historical_freeze(self):
        old = app.RELEASE / 'freeze_manifest.json'
        before = app.sha(old.read_bytes())
        app.verify_freeze()
        self.assertEqual(before, app.LEGACY_FREEZE_SHA)
        self.assertEqual(app.sha(old.read_bytes()), before)

    def test_dependency_change_rejected_without_changing_real_files(self):
        original = app.sha
        with patch.object(app, 'sha', side_effect=lambda b: '0' * 64 if b == (app.RELEASE / 'bin/build.mjs').read_bytes() else original(b)):
            with self.assertRaisesRegex(app.Stop, 'dependency_drift'):
                app.verify_freeze()

    def test_manifest_digest_change_rejected(self):
        with patch.object(app, 'FREEZE_SHA', '0' * 64):
            with self.assertRaisesRegex(app.Stop, 'manifest_drift'):
                app.verify_freeze()

    def test_unknown_profile_rejected(self):
        with self.assertRaisesRegex(app.Stop, 'unknown_release_profile'):
            app.select_release_profile('/tmp/unreviewed.json')

    def test_native_hold_counts_are_not_applied_twice(self):
        self.fixture()
        before = {name: (self.run / 'candidate' / name).read_bytes() for name in
                  ('us-en.tsv', 'us-en.manifest.json', 'us-en.diagnostics.json', 'us-en.snapshot.json')}
        app.contain(self.run)
        packet = app.candidate(self.run)
        self.assertEqual(packet['contained_available_rows'], 1)
        self.assertEqual(packet['rows'], 7)
        for name, body in before.items(): self.assertEqual((self.run / 'candidate' / name).read_bytes(), body)
        self.assertFalse(app.read(self.run / 'contain.receipt.json')['second_filter_applied'])

    def test_absent_held_parent_does_not_stop_complete_source(self):
        self.fixture('held-absent'); app.contain(self.run)
        receipt = app.verify_containment(self.run)
        self.assertEqual(receipt['native_replay']['removedAvailableRows'], 0)
        self.assertIn('gid://shopify/Product/7516369715297', receipt['native_replay']['sourceAbsentHeldParentIds'])
        self.assertEqual(app.candidate(self.run)['rows'], 7)

    def test_legacy_run_cannot_be_reused_with_current_profile(self):
        self.fixture()
        path = self.run / 'prepare.json'; value = app.read(path); value.pop('release_profile')
        path.write_bytes(app.encode(value))
        with self.assertRaisesRegex(app.Stop, 'run_release_profile_mismatch'):
            app.contain(self.run)

    def test_current_run_cannot_be_reused_with_legacy_profile(self):
        self.fixture(); app.select_release_profile('legacy')
        with self.assertRaisesRegex(app.Stop, 'run_release_profile_mismatch'):
            app.contain(self.run)

    def test_upstream_diagnostics_cannot_be_replaced_with_zero_hold_counts(self):
        self.fixture()
        path = self.run / 'candidate/us-en.diagnostics.json'; value = app.read(path)
        value['eligibilityHolds']['removedAvailableRows'] = 0; path.write_bytes(app.encode(value))
        with self.assertRaisesRegex(app.Stop, 'native_candidate_replay_failed'):
            app.contain(self.run)

    def test_eligible_protected_row_cannot_be_omitted(self):
        self.fixture()
        path = self.run / 'candidate/us-en.tsv'; lines = path.read_bytes().splitlines(keepends=True)
        path.write_bytes(b''.join([lines[0], *lines[2:]]))
        with self.assertRaisesRegex(app.Stop, 'native_candidate_replay_failed'):
            app.contain(self.run)

    def test_source_proven_protected_omission_requires_exact_independent_reason(self):
        self.fixture('protected-parent-absent'); app.contain(self.run)
        packet = app.candidate(self.run)
        self.assertEqual(packet['protected_omissions'], [{'id': app.PROTECTED_US_IDS[0],
            'reason': 'parent_absent_from_complete_active_catalog'}])
        review, digest = self.review(packet, omissions=False)
        with self.assertRaisesRegex(app.Stop, 'protected_omissions_not_independently_verified'):
            app.validate_review(self.run, review, digest)
        review, digest = self.review(packet)
        self.assertEqual(app.validate_review(self.run, review, digest), packet)

    def test_unavailable_protected_omission_is_accurately_classified(self):
        self.fixture('protected-unavailable'); app.contain(self.run)
        self.assertEqual(app.candidate(self.run)['protected_omissions'][0]['reason'], 'variant_not_available_for_sale')

    def test_unpublished_protected_omission_is_accurately_classified(self):
        self.fixture('protected-unpublished'); app.contain(self.run)
        self.assertEqual(app.candidate(self.run)['protected_omissions'][0]['reason'], 'not_on_online_store')

    def test_stale_snapshot_cannot_be_promoted(self):
        self.fixture(); app.contain(self.run)
        with patch.object(app, 'now', return_value=dt.datetime(2026, 9, 14, 22, 1, tzinfo=dt.timezone.utc)):
            with self.assertRaisesRegex(app.Stop, 'candidate_source_expired'):
                app.candidate(self.run)

    def test_incomplete_snapshot_rejected_by_offline_replay(self):
        self.fixture()
        path = self.run / 'candidate/us-en.snapshot.json'; value = app.read(path)
        value['paginationComplete'] = False; path.write_bytes(app.encode(value))
        with self.assertRaisesRegex(app.Stop, 'native_candidate_replay_failed'):
            app.contain(self.run)

    def test_candidate_drift_after_review_prevents_pointer_write(self):
        self.fixture(); app.contain(self.run)
        packet = app.candidate(self.run); review, digest = self.review(packet)
        api = FakeApi(app.read(self.run / 'before.pointer.json'), (self.run / 'before.tsv').read_bytes())
        api.objects[app.POINTER] = (self.run / 'before.pointer.json').read_bytes()
        # Force an immutable object write so the midway candidate drift hook runs.
        after = app.read(self.run / 'candidate/us-en.manifest.json')
        api.objects.pop(after['objectKey'], None)
        def change():
            path = self.run / 'candidate/us-en.diagnostics.json'
            value = app.read(path); value['rows'] = 999; path.write_bytes(app.encode(value))
        api.on_object_put = change
        with self.assertRaisesRegex(app.Stop, 'native_artifact_changed'):
            app.promote(api, self.run, review, digest)
        self.assertNotIn(app.POINTER, api.writes)

    def test_native_profile_does_not_allow_unreviewed_hold_revision(self):
        self.fixture(); app.contain(self.run)
        with self.assertRaisesRegex(app.Stop, 'new_release_profile'):
            app.contain(self.run, revise=True)


if __name__ == '__main__':
    unittest.main()
