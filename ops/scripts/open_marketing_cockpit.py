#!/usr/bin/env python3
"""Render and open the human paid-growth cockpit in the local browser."""

from __future__ import annotations

import argparse
import subprocess
import sys
import webbrowser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
COCKPIT = ROOT / "ops" / "marketing" / "operator_cockpit.html"
RENDERER = ROOT / "ops" / "scripts" / "render_marketing_cockpit.py"


def render() -> None:
    subprocess.run([sys.executable, str(RENDERER)], cwd=ROOT, check=True)


def open_cockpit() -> None:
    url = COCKPIT.resolve().as_uri()
    try:
        subprocess.run(["open", str(COCKPIT)], cwd=ROOT, check=True)
    except (OSError, subprocess.CalledProcessError):
        if not webbrowser.open(url):
            raise SystemExit(f"Could not open cockpit automatically. Open manually: {url}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--no-open",
        action="store_true",
        help="Render the dashboard without opening a browser.",
    )
    args = parser.parse_args()
    render()
    if not args.no_open:
        open_cockpit()
    print(f"Marketing cockpit ready: {COCKPIT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
