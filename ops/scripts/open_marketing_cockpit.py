#!/usr/bin/env python3
"""Open the live local growth dashboard, with an explicit saved-view fallback."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import webbrowser
from pathlib import Path

from install_marketing_dashboard import port_receipt
from marketing_dashboard_server import DEFAULT_PORT


ROOT = Path(__file__).resolve().parents[2]
COCKPIT = ROOT / "ops" / "marketing" / "operator_cockpit.html"
RENDERER = ROOT / "ops" / "scripts" / "render_marketing_cockpit.py"
LIVE_URL = f"http://127.0.0.1:{DEFAULT_PORT}/ops/marketing/operator_cockpit.html"
CHROME_DASHBOARD_APP = "com.google.Chrome.app.ohmcggcffpoppmkkkfmcojkkdblblkkd"


def render() -> None:
    subprocess.run([sys.executable, str(RENDERER)], cwd=ROOT, check=True)


def healthy_live_service(receipt: dict) -> bool:
    status = receipt.get("status") or {}
    revision = status.get("revision")
    return bool(
        receipt.get("ours") is True
        and status.get("online") is True
        and status.get("content_error") is None
        and isinstance(revision, str)
        and re.fullmatch(r"[a-f0-9]{64}", revision)
        and status.get("rendered_at")
    )


def open_cockpit(url: str | None = None, *, prefer_dashboard_app: bool = False) -> None:
    url = url or COCKPIT.resolve().as_uri()
    if prefer_dashboard_app:
        try:
            subprocess.run(["open", "-b", CHROME_DASHBOARD_APP, url], cwd=ROOT, check=True, capture_output=True)
            return
        except (OSError, subprocess.CalledProcessError):
            pass  # The exact installed app is optional; keep the live URL.
    try:
        subprocess.run(["open", url], cwd=ROOT, check=True)
    except (OSError, subprocess.CalledProcessError):
        if not webbrowser.open(url):
            raise SystemExit(f"Could not open cockpit automatically. Open manually: {url}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--no-open",
        action="store_true",
        help="Report the live URL without opening or re-rendering it; render a saved view only if the service is unavailable.",
    )
    args = parser.parse_args()
    receipt = port_receipt(DEFAULT_PORT, ROOT)
    if healthy_live_service(receipt):
        if not args.no_open:
            open_cockpit(LIVE_URL, prefer_dashboard_app=True)
        print(f"Marketing cockpit live: {LIVE_URL}")
        return

    if receipt.get("ours"):
        # The running service owns this generated output. Never overwrite its
        # last-good copy while its current source records are invalid.
        if not COCKPIT.is_file():
            raise SystemExit("The live service has no healthy current render or saved dashboard. Correct its source records before opening it.")
        explanation = "Live records are not healthy; last saved snapshot only"
    else:
        render()
        explanation = "Live service unavailable for this checkout; saved snapshot only"
    if not args.no_open:
        open_cockpit()
    print(f"{explanation}: {COCKPIT.resolve().as_uri()}")


if __name__ == "__main__":
    main()
