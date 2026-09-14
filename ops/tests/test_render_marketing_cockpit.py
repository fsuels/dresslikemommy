"""Freshness tests: historical reports must not look like current authority."""
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/render_marketing_cockpit.py"
spec = importlib.util.spec_from_file_location("render_marketing_cockpit", SCRIPT)
module = importlib.util.module_from_spec(spec)
# dataclasses resolves the module while the renderer is imported.
import sys
sys.modules[spec.name] = module
spec.loader.exec_module(module)


class FreshnessTests(unittest.TestCase):
    maxDiff = 1200
    def setUp(self):
        self.snapshot = {
            "channels": [{"id": "google", "label": "Google Ads"}],
            "campaigns": [{"id": "sample", "channel": "google", "name": "Saved test",
                           "status_label": "ACTIVE", "running_state": "Enabled in May"}],
        }

    def test_stale_snapshots_are_collapsed_and_marked(self):
        html = module.render_campaign_explorer(self.snapshot, historical=True)
        self.assertIn('<details class="panel span-12 historical-campaigns">', html)
        self.assertNotIn(" open", html)
        self.assertIn("Historical: ACTIVE", html)
        self.assertIn("Snapshot Metrics (Historical)", html)
        self.assertNotIn("Today / Yesterday Metrics", html)
        self.assertIn("do not establish what is enabled", html)
        self.assertEqual(self.snapshot["campaigns"][0]["status_label"], "ACTIVE")

    def test_current_explorer_remains_interactive(self):
        html = module.render_campaign_explorer(self.snapshot)
        self.assertNotIn("<details", html)
        self.assertIn('data-campaign="sample"', html)
        self.assertIn('data-channel="google"', html)
        self.assertIn("Today / Yesterday Metrics", html)
        self.assertNotIn("Historical: ACTIVE", html)

    def test_build_uses_control_and_never_old_review_pass(self):
        with patch.object(module, "parse_authoritative_control", return_value={
            "live_state_mode": "STALE_READBACK_REQUIRED",
            "effective_approval_policy": "FRESH_ACTION_TIME_APPROVAL_REQUIRED",
        }):
            html = module.build_html()
        self.assertIn("historical-campaigns", html)
        self.assertIn("Review log: SEE LATEST DATED REVIEW", html)
        self.assertIn("<span>One Owner Action</span>", html)
        self.assertIn("<h2>Historical Channel Scorecard</h2>", html)
        self.assertNotIn("<h2>Live Scorecard</h2>", html)
        self.assertIn("STALE_READBACK_REQUIRED", html)


class OwnerTaskTests(unittest.TestCase):
    maxDiff = 1200

    def test_blank_lines_do_not_drop_tasks_and_history_is_excluded(self):
        markdown = '''## Current turnaround tasks — sample
| Priority | Status | Action | Owner agent | Gate | Evidence/source |
|---|---|---|---|---|---|
| P1 | YELLOW | `TA-01` First | root | Review | first.md |

| P0 | RED | `TA-15` Second | root | Hold | second.md |

| P1 | YELLOW | `TA-18` Third | root | Read | third.md |

## Historical queue
| Priority | Status | Action | Owner agent | Gate | Evidence/source |
|---|---|---|---|---|---|
| P0 | GREEN | `TA-99` Historical | root | Old approval | old.md |
'''
        rows = module.current_task_rows(markdown)
        self.assertEqual([row['id'] for row in rows], ['TA-15','TA-01','TA-18'])
        self.assertEqual(rows[0]['Status'], 'RED')
        self.assertNotIn('Checkpoint', rows[0])

    def test_duplicate_and_malformed_rows_fail_visibly(self):
        header = '## Current turnaround tasks\n| Priority | Status | Action | Owner agent | Gate | Evidence/source |\n|---|---|---|---|---|---|\n'
        row = '| P1 | YELLOW | TA-01 Work | root | pending | file.md |\n'
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            module.current_task_rows(header + row + row)
        with self.assertRaisesRegex(ValueError, 'column count'):
            module.current_task_rows(header + '| P1 | TA-01 Work |\n')

    def test_missing_or_ambiguous_current_section_fails_visibly(self):
        with self.assertRaises(ValueError):
            module.current_task_rows('## Historical queue\n')
        with self.assertRaises(ValueError):
            module.current_task_rows('## Current turnaround tasks A\n## Current turnaround tasks B\n')
        with self.assertRaises(ValueError):
            module.current_task_rows('## Current turnaround tasks A\n## Current turnaround tasks A\n')
        with self.assertRaisesRegex(ValueError, 'no readable tasks'):
            module.current_task_rows('## Current turnaround tasks\nNo rows yet.')

    def test_actual_tasks_preserve_manual_release_and_paid_hold(self):
        rows = {r['id']: r for r in module.current_task_rows((module.MARKETING/'action_queue.md').read_text())}
        self.assertTrue({'TA-15','TA-18','TA-17','TA-19'}.issubset(rows))
        self.assertEqual(rows['TA-06']['Owner input'], 'Manual action')
        self.assertIn('137782591585', rows['TA-06']['Next step'])
        self.assertIn('already authorized', rows['TA-06']['Completed milestone'])
        self.assertEqual(rows['TA-09']['Status'], 'RED')
        self.assertEqual(rows['TA-09']['Owner input'], 'Future approval')
        self.assertEqual(rows['TA-17']['Checkpoint'], 'Verification remaining')
        self.assertEqual(rows['TA-19']['Checkpoint'], 'Verification remaining')
        control = module.parse_authoritative_control((module.MARKETING/'current_marketing_state.md').read_text())
        self.assertEqual(control['approved_external_scope'], 'NONE')

    def test_unknown_progress_is_never_invented_and_input_is_escaped(self):
        task = {'id':'TA-88','Action':'TA-88 <script>alert(1)</script>','Status':'YELLOW'}
        output = module.render_owner_view([task], {}, 'test date')
        self.assertIn('Not recorded', output)
        self.assertIn('data-milestone="no"', output)
        self.assertNotIn('<script>alert(1)</script>', output)
        self.assertIn('&lt;script&gt;', output)
        self.assertIn('Task context', module.OWNER_SCRIPT)

    def test_result_snapshot_keeps_unknown_profit_and_separate_cohort(self):
        table = module.find_table(module.MARKETING/'daily_scorecard.md', 'Metric')
        rows = {r[0]: dict(zip(table.headers,r)) for r in table.rows}
        self.assertEqual(rows['Retained profit']['Value'], 'UNKNOWN')
        self.assertEqual(rows['Observed orders']['Value'], '2')
        self.assertIn('not new orders today', rows['Observed orders']['Meaning'])
        self.assertIn('earlier eight-order baseline', rows['Observed orders']['Meaning'])
        self.assertEqual(rows['Free traffic']['Value'], 'NOT REFRESHED')

    def test_continuation_reuses_the_canonical_prompt(self):
        import json, re
        output = module.render_owner_view([], {}, 'test date')
        payload = json.loads(re.search(r'id="deskHandoffData">(.*?)</script>', output).group(1))
        source = (module.ROOT/'ops/prompts/paid-growth-ai-army-continuation-prompt.md').read_text()
        expected = re.search(r'```text\n(.*?)\n```',source,re.DOTALL).group(1)
        self.assertEqual(payload['prompt'], expected)


if __name__ == "__main__":
    unittest.main()
