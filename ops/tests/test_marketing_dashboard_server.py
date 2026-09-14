#!/usr/bin/env python3
"""Real loopback HTTP regressions; fixtures never install a job or touch accounts."""

from __future__ import annotations

import http.client
import json
import os
import plistlib
import re
import sys
import tempfile
import threading
import unittest
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import marketing_dashboard_server as dashboard
import install_marketing_dashboard as installer


RENDERER_FIXTURE = '''from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
def build_html():
    task = (ROOT / "ops/marketing/action_queue.md").read_text()
    return '<!doctype html><html><head><title>Growth</title></head><body>VERSION_A ' + task + '<a href="action_queue.md">Task</a><a href="../../dresslikemommy-growth-2026/02_AUDIT_PACKETS/proof/result.md">Evidence</a><a href="../../.env">Never serve</a><a href="../../ops/scripts/render_marketing_cockpit.py">Never serve code</a><a href="../../ops/AGENT_WORKLOG.md">Never serve chronology body</a></body></html>'
'''


class LiveDashboardTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="dlm-dashboard-test-")
        self.root = Path(self.temporary.name)
        for name in dashboard.SOURCE_FILES:
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("Canonical fixture\n")
        (self.root / "ops/marketing/campaign_explorer.json").write_text('{"saved": true}')
        (self.root / dashboard.RENDERER).write_text(RENDERER_FIXTURE)
        (self.root / "ops/marketing/action_queue.md").write_text("TA-01 awaiting access")
        (self.root / dashboard.WORKLOG).write_text("""## 2026-09-08 — First recorded change
AGENT_CONTINUITY_ANCHOR: 2026-09-08-first-change
- `task_entities`: TA-01, TA-16
Sensitive worklog body that must never be returned: TOKEN=PRIVATE_TEST_VALUE.
## 2026-09-09 — Updated task handoff
AGENT_CONTINUITY_ANCHOR: 2026-09-09-updated-task-handoff
- `task_entities`: TA-06, TA-11
Another private body.
""")
        self.evidence = self.root / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/proof/result.md"
        self.evidence.parent.mkdir(parents=True)
        self.evidence.write_text("Verified fixture evidence.")
        (self.root / ".env").write_text("PRIVATE_TEST_VALUE")
        (self.root / "ops/marketing/unlinked.md").write_text("PRIVATE_UNLINKED_RECORD")
        self.state = dashboard.DashboardState(self.root, poll_interval=0)
        self.server = dashboard.DashboardServer(self.state, port=0)
        self.thread = threading.Thread(target=lambda: self.server.serve_forever(poll_interval=0.01), daemon=True)
        self.thread.start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(2)
        self.temporary.cleanup()

    def request(self, path, method="GET", headers=None, body=None):
        connection = http.client.HTTPConnection("127.0.0.1", self.server.server_port, timeout=3)
        try:
            connection.request(method, path, body=body, headers=headers or {})
            response = connection.getresponse()
            return response.status, dict(response.getheaders()), response.read()
        finally:
            connection.close()

    def status(self):
        code, headers, body = self.request("/api/status")
        self.assertEqual(code, 200)
        return json.loads(body)

    def test_root_redirect_and_served_page_revision_match(self):
        code, headers, _ = self.request("/")
        self.assertEqual(code, 302)
        self.assertEqual(headers["Location"], "/" + dashboard.DASHBOARD)
        status = self.status()
        code, headers, body = self.request("/" + dashboard.DASHBOARD)
        self.assertEqual(code, 200)
        self.assertIn(b"TA-01 awaiting access", body)
        revision = re.search(rb'name="dlm-dashboard-revision" content="([a-f0-9]+)"', body).group(1).decode()
        self.assertEqual(revision, status["revision"])
        self.assertNotIn("dlm-dashboard-revision", (self.root / dashboard.DASHBOARD).read_text())
        self.assertEqual(headers["Cache-Control"], "no-store")

    def test_source_change_refreshes_without_restarting_and_touch_does_not_rebuild(self):
        first = self.status()
        cache = self.root / dashboard.DASHBOARD
        before_mtime = cache.stat().st_mtime_ns
        os.utime(self.root / "ops/marketing/action_queue.md", None)
        same = self.status()
        self.assertEqual(first["revision"], same["revision"])
        self.assertEqual(before_mtime, cache.stat().st_mtime_ns)
        (self.root / "ops/marketing/action_queue.md").write_text("TA-01 access verified; next review")
        changed = self.status()
        self.assertNotEqual(first["revision"], changed["revision"])
        self.assertIn(b"access verified; next review", self.request("/" + dashboard.DASHBOARD)[2])
        self.assertEqual(first["started_at"], changed["started_at"])

    def test_renderer_source_reloads_even_with_same_timestamp_and_length(self):
        file = self.root / dashboard.RENDERER
        initial_stat = file.stat()
        before = self.status()["revision"]
        file.write_text(RENDERER_FIXTURE.replace("VERSION_A", "VERSION_B"))
        os.utime(file, ns=(initial_stat.st_atime_ns, initial_stat.st_mtime_ns))
        after = self.status()["revision"]
        self.assertNotEqual(before, after)
        self.assertIn(b"VERSION_B", self.request("/" + dashboard.DASHBOARD)[2])

    def test_malformed_source_retains_last_good_page_and_recovers(self):
        before = self.status()
        page = self.request("/" + dashboard.DASHBOARD)[2]
        file = self.root / "ops/marketing/campaign_explorer.json"
        file.write_text('{"secret": "PRIVATE_TEST_VALUE", broken')
        failed = self.status()
        self.assertTrue(failed["online"])
        self.assertEqual(failed["content_error"], dashboard.CONTENT_ERROR)
        self.assertEqual(before["revision"], failed["revision"])
        self.assertEqual(page, self.request("/" + dashboard.DASHBOARD)[2])
        self.assertNotIn("PRIVATE_TEST_VALUE", json.dumps(failed))
        file.write_text('{"saved": "corrected"}')
        recovered = self.status()
        self.assertIsNone(recovered["content_error"])
        self.assertNotEqual(before["revision"], recovered["revision"])

    def test_final_snapshot_race_never_pairs_old_page_with_new_revision(self):
        before = self.status()
        page = self.request("/" + dashboard.DASHBOARD)[2]
        action = self.root / "ops/marketing/action_queue.md"
        action.write_text("TA-01 intermediate edit")
        snapshot = self.state._snapshot
        calls = 0

        def change_during_final_snapshot(extra):
            nonlocal calls
            calls += 1
            if calls == 3:
                action.write_text("TA-01 completed edit")
            return snapshot(extra)

        with mock.patch.object(self.state, "_snapshot", side_effect=change_during_final_snapshot):
            failed = self.status()
        self.assertEqual(failed["revision"], before["revision"])
        self.assertEqual(failed["content_error"], dashboard.CONTENT_ERROR)
        self.assertIn("awaiting access", self.state.html)
        recovered = self.status()
        self.assertIsNone(recovered["content_error"])
        self.assertNotEqual(before["revision"], recovered["revision"])
        self.assertIn(b"completed edit", self.request("/" + dashboard.DASHBOARD)[2])

    def test_cleanly_truncated_task_section_keeps_last_good_until_boundary_returns(self):
        renderer = self.root / dashboard.RENDERER
        renderer.write_text(RENDERER_FIXTURE + '\ndef current_task_rows(markdown):\n    return ["fixture task"]\n')
        action = self.root / "ops/marketing/action_queue.md"
        complete = "## Current turnaround tasks — September 9\n\n| Action | Owner agent |\n|---|---|\n| TA-01 awaiting access | root |\n\n## Next steps\nRetain the queue.\n"
        action.write_text(complete)
        before = self.status()
        self.assertIsNone(before["content_error"])
        old_html = self.state.html
        action.write_text(complete.split("\n## Next steps")[0])
        failed = self.status()
        self.assertEqual(failed["revision"], before["revision"])
        self.assertEqual(failed["content_error"], dashboard.CONTENT_ERROR)
        self.assertEqual(old_html, self.state.html)
        action.write_text(complete.replace("awaiting access", "access verified"))
        recovered = self.status()
        self.assertIsNone(recovered["content_error"])
        self.assertNotEqual(before["revision"], recovered["revision"])
        self.assertIn(b"access verified", self.request("/" + dashboard.DASHBOARD)[2])

    def test_missing_source_and_renderer_exception_expose_only_generic_error(self):
        (self.root / dashboard.RENDERER).write_text(RENDERER_FIXTURE + '\ndef build_html():\n    raise ValueError("PRIVATE_TEST_VALUE /Users/private/details")\n')
        status = self.status()
        self.assertEqual(status["content_error"], dashboard.CONTENT_ERROR)
        self.assertNotIn("PRIVATE_TEST_VALUE", json.dumps(status))
        (self.root / "ops/marketing/action_queue.md").unlink()
        self.assertEqual(self.status()["content_error"], dashboard.CONTENT_ERROR)

    def test_startup_with_invalid_source_uses_cache_but_claims_no_current_revision(self):
        (self.root / "ops/marketing/campaign_explorer.json").write_text("invalid")
        restarted = dashboard.DashboardState(self.root, poll_interval=0)
        self.assertIsNone(restarted.status()["revision"])
        self.assertEqual(restarted.status()["content_error"], dashboard.CONTENT_ERROR)
        self.assertIn(b"awaiting access", restarted.page())
        self.assertFalse(restarted.allowed_files)

    def test_only_explicitly_linked_safe_records_are_served_as_inert_documents(self):
        for route in ("/ops/marketing/action_queue.md", "/dresslikemommy-growth-2026/02_AUDIT_PACKETS/proof/result.md"):
            with self.subTest(route=route):
                code, headers, _ = self.request(route)
                self.assertEqual(code, 200)
                self.assertEqual(headers["Content-Type"], "text/plain; charset=utf-8")
                self.assertEqual(headers["X-Content-Type-Options"], "nosniff")
        for route in ("/.env", "/.git/config", "/ops/marketing/unlinked.md", "/ops/marketing/", "/ops/scripts/render_marketing_cockpit.py", "/ops/AGENT_WORKLOG.md"):
            with self.subTest(route=route):
                self.assertEqual(self.request(route)[0], 404)

    def test_traversal_encoding_and_symlink_escape_are_rejected(self):
        for route in ("/../.env", "/%2e%2e/.env", "/%252e%252e/.env", "/ops/marketing/../.env", "/ops%5c..%5c.env", "/file%00.md", "/file%ZZ.md"):
            with self.subTest(route=route):
                self.assertEqual(self.request(route)[0], 400)
        self.evidence.unlink()
        self.evidence.symlink_to(self.root / ".env")
        self.assertEqual(self.request("/dresslikemommy-growth-2026/02_AUDIT_PACKETS/proof/result.md")[0], 404)
        self.evidence.unlink()
        self.evidence.symlink_to(Path(self.temporary.name).parent / "private-outside.md")
        self.assertEqual(self.request("/dresslikemommy-growth-2026/02_AUDIT_PACKETS/proof/result.md")[0], 404)

    def test_host_cross_origin_and_cors_reads_are_rejected(self):
        for headers in ({"Host": "attacker.example"}, {"Host": "192.168.1.2:8767"}, {"Origin": "https://attacker.example"}, {"Origin": "null"}, {"Referer": "https://attacker.example/"}, {"Sec-Fetch-Site": "cross-site"}, {"Sec-Fetch-Site": "same-site"}):
            with self.subTest(headers=headers):
                code, response_headers, _ = self.request("/api/status", headers=headers)
                self.assertEqual(code, 403)
                self.assertNotIn("Access-Control-Allow-Origin", response_headers)
        origin = f"http://127.0.0.1:{self.server.server_port}"
        self.assertEqual(self.request("/api/status", headers={"Origin": origin, "Referer": origin + "/", "Sec-Fetch-Site": "same-origin"})[0], 200)

    def test_status_is_sanitized_and_never_infers_live_workers(self):
        raw = self.request("/api/status")[2].decode()
        status = json.loads(raw)
        self.assertEqual(status["service"], dashboard.SERVICE)
        self.assertEqual(status["live_agent_status"], "not_connected")
        self.assertEqual(status["recent_handoffs"][0], {"date": "2026-09-09", "title": "Updated task handoff", "anchor": "2026-09-09-updated-task-handoff", "task_ids": ["TA-06", "TA-11"]})
        self.assertNotIn(self.temporary.name, raw)
        self.assertNotIn("PRIVATE_TEST_VALUE", raw)
        self.assertNotIn("private body", raw)
        self.assertTrue(all(set(entry) == {"name", "modified_at"} and "/" not in entry["name"] for entry in status["source_files"]))
        self.assertTrue(status["checked_at"] and status["rendered_at"] and status["last_source_change_at"])

    def test_http_methods_cannot_mutate_records(self):
        before = (self.root / "ops/marketing/action_queue.md").read_bytes()
        for method in ("POST", "PUT", "PATCH", "DELETE", "OPTIONS", "TRACE", "CONNECT"):
            with self.subTest(method=method):
                code, headers, _ = self.request("/ops/marketing/action_queue.md", method=method, body="replace all records")
                self.assertEqual(code, 405)
                self.assertEqual(headers["Allow"], "GET, HEAD")
        self.assertEqual(before, (self.root / "ops/marketing/action_queue.md").read_bytes())
        code, _, body = self.request("/api/status", method="HEAD")
        self.assertEqual((code, body), (200, b""))

    def test_installer_detects_same_service_and_different_checkout_on_real_port(self):
        self.assertTrue(installer.port_receipt(self.server.server_port, self.root)["ours"])
        conflict = installer.port_receipt(self.server.server_port, self.root / "different-checkout")
        self.assertTrue(conflict["occupied"])
        self.assertFalse(conflict["ours"])
        self.assertIsNone(conflict["status"])


class InstallerConfigurationTests(unittest.TestCase):
    def test_plist_is_absolute_private_persistent_and_roundtrips(self):
        root = Path("/tmp/dlm-checkout")
        home = Path("/tmp/dlm-owner")
        payload = installer.build_plist(root, Path(sys.executable), home)
        self.assertEqual(plistlib.loads(plistlib.dumps(payload)), payload)
        self.assertEqual(payload["Label"], installer.LABEL)
        self.assertEqual(payload["WorkingDirectory"], str(root.resolve()))
        self.assertTrue(payload["RunAtLoad"] and payload["KeepAlive"])
        self.assertEqual(payload["Umask"], 0o077)
        self.assertEqual(payload["ProgramArguments"][0], str(Path(sys.executable).resolve()))
        self.assertEqual(payload["ProgramArguments"][-2:], ["--port", "8767"])
        self.assertNotIn("Chrome", json.dumps(payload))
        installer.validate_existing(payload, root, 8767)
        with self.assertRaises(installer.InstallationError):
            installer.validate_existing(payload, root, 8768)
        with self.assertRaises(installer.InstallationError):
            installer.validate_existing(payload, Path("/tmp/other-checkout"), 8767)
        different_command = dict(payload, ProgramArguments=["/bin/sh", "-c"] + payload["ProgramArguments"])
        with self.assertRaises(installer.InstallationError):
            installer.validate_existing(different_command, root, 8767)

    def test_existing_plist_backup_is_exact_and_reinstallation_is_idempotent(self):
        with tempfile.TemporaryDirectory(prefix="dlm-plist-test-") as directory:
            base = Path(directory)
            target = base / "LaunchAgents" / (installer.LABEL + ".plist")
            payload = installer.build_plist(base / "repo", Path(sys.executable), base / "owner")
            with mock.patch.object(installer, "run") as run:
                self.assertIsNone(installer.atomic_plist(target, payload))
                before = target.read_bytes()
                before_time = target.stat().st_mtime_ns
                self.assertIsNone(installer.atomic_plist(target, payload))
                self.assertEqual(before_time, target.stat().st_mtime_ns)
                changed = dict(payload, ThrottleInterval=20)
                backup = installer.atomic_plist(target, changed)
                self.assertEqual(backup.read_bytes(), before)
                self.assertEqual(plistlib.loads(target.read_bytes()), changed)
                self.assertEqual(target.stat().st_mode & 0o777, 0o600)
                self.assertEqual(run.call_count, 2)
                self.assertTrue(all(call.args[0][:2] == ["/usr/bin/plutil", "-lint"] for call in run.call_args_list))

    def test_install_refuses_port_conflict_before_any_files_or_job_mutation(self):
        with tempfile.TemporaryDirectory(prefix="dlm-conflict-test-") as directory:
            root = Path(directory) / "repo"
            home = Path(directory) / "owner"
            server = root / "ops/scripts/marketing_dashboard_server.py"
            server.parent.mkdir(parents=True)
            server.write_text("fixture")
            with mock.patch.object(installer, "validate_interpreter"), mock.patch.object(installer, "loaded", return_value=False), mock.patch.object(installer, "port_receipt", return_value={"occupied": True, "ours": False, "status": None}), mock.patch.object(installer, "run") as run:
                with self.assertRaises(installer.InstallationError):
                    installer.install(root, Path(sys.executable), home, 8767)
                run.assert_not_called()
                self.assertFalse(home.exists())


if __name__ == "__main__":
    unittest.main()
