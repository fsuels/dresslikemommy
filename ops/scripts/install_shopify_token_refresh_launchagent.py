#!/usr/bin/env python3
"""Install or manage the local macOS launchd job that keeps the Shopify Admin token fresh.

The job runs `refresh_shopify_admin_token.py --if-needed` at login and every hour.
It only mints a new 24-hour token when the stored one has less than 2 hours left,
so the other local jobs (product translations, import autofill, cost sync) always
read a valid token from ~/.config/dresslikemommy/.

Usage:
    python3 ops/scripts/install_shopify_token_refresh_launchagent.py install
    python3 ops/scripts/install_shopify_token_refresh_launchagent.py status
    python3 ops/scripts/install_shopify_token_refresh_launchagent.py uninstall
"""
from __future__ import annotations

import argparse
import plistlib
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
LABEL = "com.dresslikemommy.shopify-token-refresh"
PLIST_PATH = Path.home() / "Library" / "LaunchAgents" / f"{LABEL}.plist"
LOG_DIR = Path.home() / "Library" / "Logs" / "dresslikemommy"
WORKER_PATH = REPO_ROOT / "ops" / "scripts" / "refresh_shopify_admin_token.py"
PYTHON_BIN = Path("/usr/bin/python3")
INTERVAL_SECONDS = 3600


def run(args: list[str], check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(args, text=True, capture_output=True, check=check)


def target() -> str:
    return f"gui/{run(['id', '-u']).stdout.strip()}"


def plist_payload() -> dict:
    return {
        "Label": LABEL,
        "ProgramArguments": [str(PYTHON_BIN), str(WORKER_PATH), "--if-needed"],
        "WorkingDirectory": str(REPO_ROOT),
        "RunAtLoad": True,
        "StartInterval": INTERVAL_SECONDS,
        "StandardOutPath": str(LOG_DIR / "shopify-token-refresh.stdout.log"),
        "StandardErrorPath": str(LOG_DIR / "shopify-token-refresh.stderr.log"),
    }


def install() -> int:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    PLIST_PATH.parent.mkdir(parents=True, exist_ok=True)
    run(["launchctl", "bootout", target(), str(PLIST_PATH)], check=False)
    PLIST_PATH.write_bytes(plistlib.dumps(plist_payload()))
    run(["launchctl", "bootstrap", target(), str(PLIST_PATH)])
    print(f"Installed {LABEL}: runs at login and every {INTERVAL_SECONDS // 60} minutes.")
    return status()


def uninstall() -> int:
    run(["launchctl", "bootout", target(), str(PLIST_PATH)], check=False)
    if PLIST_PATH.exists():
        PLIST_PATH.unlink()
    print(f"Removed {LABEL}.")
    return 0


def status() -> int:
    result = run(["launchctl", "print", f"{target()}/{LABEL}"], check=False)
    if result.returncode != 0:
        print(f"{LABEL} is not loaded.")
        return 1
    keep = ("state =", "runs =", "last exit code", "run interval")
    for line in result.stdout.splitlines():
        if any(k in line for k in keep):
            print(line.strip())
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("action", choices=["install", "status", "uninstall"])
    args = parser.parse_args(argv)
    return {"install": install, "status": status, "uninstall": uninstall}[args.action]()


if __name__ == "__main__":
    sys.exit(main())
