import copy
import hashlib
import json
import unittest

from cohort_filter import apply_holds


class CohortTests(unittest.TestCase):
    def setUp(self):
        self.ids = ['shopify_US_1_11', 'shopify_US_2_21', 'shopify_US_2_22', 'shopify_US_3_31']
        self.lines = [b'id\ttitle\tprice\n'] + [(i + '\tCafé family "set", size S\t22.99 USD\n').encode() for i in self.ids]
        self.body = b''.join(self.lines)
        sha = hashlib.sha256(self.body).hexdigest(); md5 = hashlib.md5(self.body).hexdigest()
        self.manifest = {'schemaVersion': 1, 'market': {'key': 'us-en', 'country': 'US', 'locale': 'en', 'currency': 'USD'},
                         'sha256': sha, 'bytes': len(self.body), 'objectEtag': md5, 'expectedMd5': md5,
                         'objectKey': 'merchant/us-en/' + sha + '.tsv', 'rowIds': self.ids, 'rows': 4,
                         'sourceParents': 3, 'sourceVariants': 4, 'sourceCompletedAt': '2026-09-11T10:00:00Z'}
        self.diagnostics = {'rows': 4, 'errors': [], 'sourceCounts': {'parents': 3, 'variants': 4},
                            'exceptionRows': 2, 'exclusions': [], 'returnCohorts': [
                                {'productId': 'gid://shopify/Product/2', 'classification': 'verified_policy_exception'}]}
        self.spec = {'schemaVersion': 1, 'markets': ['us-en', 'au-en'], 'holds': [
            {'product_id': 'gid://shopify/Product/2', 'reason': 'Fixture hold', 'evidence': ['fixture'], 'release_condition': 'Fixture accepted'}]}
        self.parents = ['gid://shopify/Product/' + str(i) for i in (1, 2, 3)]

    def run_filter(self, spec=None, protected=()):
        return apply_holds(self.body, self.manifest, self.diagnostics, json.dumps(spec or self.spec).encode(), self.ids, protected, self.parents)

    def test_unknown_parent_hold_is_rejected(self):
        spec = copy.deepcopy(self.spec)
        spec['holds'][0]['product_id'] = 'gid://shopify/Product/999'
        with self.assertRaisesRegex(ValueError, 'unknown_held_parent'):
            self.run_filter(spec)

    def test_known_unavailable_parent_is_explicitly_distinguished(self):
        self.parents.append('gid://shopify/Product/4'); self.manifest['sourceParents'] = 4
        spec = copy.deepcopy(self.spec)
        spec['holds'][0]['product_id'] = 'gid://shopify/Product/4'
        body, manifest, diagnostics = self.run_filter(spec)
        self.assertEqual(body, self.body)
        self.assertEqual(diagnostics['eligibilityHolds']['known_held_parents_without_available_rows'], ['gid://shopify/Product/4'])

    def test_complete_source_identity_is_required(self):
        self.parents.pop()
        with self.assertRaisesRegex(ValueError, 'complete_source_parent_ids_required'):
            self.run_filter()

    def test_exact_parent_removal_preserves_every_retained_byte(self):
        body, manifest, diagnostics = self.run_filter()
        self.assertEqual(body, self.lines[0] + self.lines[1] + self.lines[4])
        self.assertEqual(manifest['rowIds'], [self.ids[0], self.ids[3]])
        self.assertEqual(diagnostics['lifecycle']['removed'], self.ids[1:3])
        self.assertEqual(diagnostics['lifecycle']['added'], [])
        self.assertEqual(diagnostics['eligibilityHolds']['removed_rows_by_parent'], {'gid://shopify/Product/2': 2})
        self.assertEqual(diagnostics['eligibilityHolds']['kept_parents'], 2)

    def test_complete_source_counts_and_timestamps_unchanged(self):
        _, manifest, diagnostics = self.run_filter()
        for field in ('market', 'sourceParents', 'sourceVariants', 'sourceCompletedAt'):
            self.assertEqual(manifest[field], self.manifest[field])
        self.assertEqual(diagnostics['sourceCounts'], self.diagnostics['sourceCounts'])
        self.assertEqual(self.manifest['rows'], 4)

    def test_exception_diagnostics_follow_retained_cohort(self):
        _, _, diagnostics = self.run_filter()
        self.assertEqual(diagnostics['exceptionRows'], 0)
        self.assertEqual(diagnostics['returnCohorts'], [])

    def test_protected_existing_pilot_cannot_be_lost(self):
        self.run_filter(protected=[self.ids[0]])
        with self.assertRaisesRegex(ValueError, 'protected_offer_lost'):
            self.run_filter(protected=[self.ids[1]])

    def test_duplicate_or_unsubstantiated_hold_rejected(self):
        spec = copy.deepcopy(self.spec); spec['holds'].append(spec['holds'][0])
        with self.assertRaisesRegex(ValueError, 'duplicate_held_parent'):
            self.run_filter(spec)
        spec = copy.deepcopy(self.spec); spec['holds'][0]['evidence'] = []
        with self.assertRaisesRegex(ValueError, 'hold_evidence_missing'):
            self.run_filter(spec)

    def test_wrong_market_or_input_hash_rejected(self):
        spec = copy.deepcopy(self.spec); spec['markets'] = ['au-en']
        with self.assertRaisesRegex(ValueError, 'hold_scope_mismatch'):
            self.run_filter(spec)
        self.manifest['sha256'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'input_hash_mismatch'):
            self.run_filter()

    def test_no_guessed_stock_or_status_change(self):
        _, _, diagnostics = self.run_filter()
        self.assertEqual({x['code'] for x in diagnostics['exclusions']}, {'reviewed_parent_eligibility_hold'})
        self.assertNotIn('outOfStock', diagnostics)


if __name__ == '__main__':
    unittest.main()
