"""Opener routing tests: all browser/open operations are mocked."""

from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import open_marketing_cockpit as opener


def live_receipt(**overrides):
    status = {"online": True, "revision": "a" * 64, "rendered_at": "2026-09-09T12:00:00Z", "content_error": None}
    status.update(overrides)
    return {"occupied": True, "ours": True, "status": status}


class OpenerTests(unittest.TestCase):
    def run_main(self, receipt, *arguments):
        output = StringIO()
        with mock.patch.object(opener, "port_receipt", return_value=receipt) as probe, mock.patch.object(sys, "argv", ["open_marketing_cockpit.py", *arguments]), redirect_stdout(output):
            opener.main()
        probe.assert_called_once_with(opener.DEFAULT_PORT, opener.ROOT)
        return output.getvalue()

    def test_no_open_reuses_matching_live_service_without_rendering_or_launching(self):
        with mock.patch.object(opener, "render") as render, mock.patch.object(opener, "open_cockpit") as launch:
            output = self.run_main(live_receipt(), "--no-open")
        render.assert_not_called()
        launch.assert_not_called()
        self.assertIn("Marketing cockpit live: " + opener.LIVE_URL, output)

    def test_normal_live_invocation_prefers_exact_dashboard_app(self):
        with mock.patch.object(opener, "render") as render, mock.patch.object(opener.subprocess, "run") as run:
            self.run_main(live_receipt())
        render.assert_not_called()
        run.assert_called_once_with(["open", "-b", opener.CHROME_DASHBOARD_APP, opener.LIVE_URL], cwd=opener.ROOT, check=True, capture_output=True)

    def test_missing_dashboard_app_falls_back_to_browser_with_same_live_url(self):
        missing = subprocess.CalledProcessError(1, "open")
        with mock.patch.object(opener.subprocess, "run", side_effect=[missing, mock.Mock()]) as run, mock.patch.object(opener.webbrowser, "open") as browser:
            opener.open_cockpit(opener.LIVE_URL, prefer_dashboard_app=True)
        self.assertEqual(run.call_args_list[1], mock.call(["open", opener.LIVE_URL], cwd=opener.ROOT, check=True))
        browser.assert_not_called()

    def test_browser_library_is_last_fallback_and_failure_reports_exact_url(self):
        with mock.patch.object(opener.subprocess, "run", side_effect=OSError), mock.patch.object(opener.webbrowser, "open", return_value=True) as browser:
            opener.open_cockpit(opener.LIVE_URL, prefer_dashboard_app=True)
        browser.assert_called_once_with(opener.LIVE_URL)
        with mock.patch.object(opener.subprocess, "run", side_effect=OSError), mock.patch.object(opener.webbrowser, "open", return_value=False):
            with self.assertRaisesRegex(SystemExit, "127.0.0.1:8767"):
                opener.open_cockpit(opener.LIVE_URL)

    def test_unavailable_service_renders_saved_view_and_reports_fallback(self):
        with mock.patch.object(opener, "render") as render, mock.patch.object(opener, "open_cockpit") as launch:
            output = self.run_main({"occupied": False, "ours": False, "status": None}, "--no-open")
        render.assert_called_once_with()
        launch.assert_not_called()
        self.assertIn("saved snapshot only", output)
        self.assertNotIn("cockpit live", output)

    def test_other_checkout_is_never_treated_as_this_live_dashboard(self):
        wrong = live_receipt()
        wrong["ours"] = False
        with mock.patch.object(opener, "render") as render, mock.patch.object(opener, "open_cockpit") as launch:
            output = self.run_main(wrong)
        render.assert_called_once_with()
        launch.assert_called_once_with()
        self.assertIn("unavailable for this checkout", output)

    def test_unhealthy_matching_service_keeps_saved_bytes_without_rendering(self):
        with tempfile.TemporaryDirectory(prefix="dlm-opener-test-") as directory:
            cache = Path(directory) / "operator_cockpit.html"
            cache.write_text("last good snapshot")
            for changes in ({"content_error": "invalid source"}, {"revision": None}, {"online": False}, {"rendered_at": None}):
                with self.subTest(changes=changes), mock.patch.object(opener, "COCKPIT", cache), mock.patch.object(opener, "render") as render, mock.patch.object(opener, "open_cockpit") as launch:
                    output = self.run_main(live_receipt(**changes), "--no-open")
                render.assert_not_called()
                launch.assert_not_called()
                self.assertEqual(cache.read_text(), "last good snapshot")
                self.assertIn("last saved snapshot only", output)

    def test_unhealthy_service_without_cache_does_not_compete_with_server_writer(self):
        with tempfile.TemporaryDirectory(prefix="dlm-opener-test-") as directory:
            with mock.patch.object(opener, "COCKPIT", Path(directory) / "absent.html"), mock.patch.object(opener, "render") as render:
                with self.assertRaisesRegex(SystemExit, "no healthy current render"):
                    self.run_main(live_receipt(content_error="invalid source"), "--no-open")
                render.assert_not_called()


if __name__ == "__main__":
    unittest.main()
