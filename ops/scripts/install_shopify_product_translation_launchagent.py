#!/usr/bin/env python3
"""Install or manage the local macOS launchd job for automatic Shopify product translations."""

from __future__ import annotations

import argparse
import json
import plistlib
import subprocess
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops.scripts.shopify_admin_config import DEFAULT_CONFIG_DIR  # noqa: E402


LABEL = "com.dresslikemommy.shopify-product-translations"
PLIST_PATH = Path.home() / "Library" / "LaunchAgents" / f"{LABEL}.plist"
LOG_DIR = Path.home() / "Library" / "Logs" / "dresslikemommy"
STATE_PATH = DEFAULT_CONFIG_DIR / "shopify-product-translation-state.json"
WORKER_PATH = REPO_ROOT / "ops" / "scripts" / "poll_shopify_product_translations.py"
PYTHON_BIN = Path("/usr/bin/python3")


def run_command(args: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, text=True, capture_output=True, check=check)


def launchctl_target() -> str:
    uid = run_command(["id", "-u"]).stdout.strip()
    return f"gui/{uid}"


def build_program_arguments(parsed: argparse.Namespace) -> list[str]:
    args = [
        str(PYTHON_BIN),
        str(WORKER_PATH),
        "--state-path",
        str(Path(parsed.state_path).expanduser()),
        "--jsonl-log",
        str((LOG_DIR / "shopify-product-translation.jsonl").expanduser()),
        "--cache-path",
        str(Path(parsed.cache_path).expanduser()),
        "--min-age-seconds",
        str(max(parsed.min_age_seconds, 0)),
        "--page-size",
        str(max(parsed.page_size, 1)),
        "--max-pages",
        str(max(parsed.max_pages, 1)),
        "--max-products-per-run",
        str(max(parsed.max_products_per_run, 1)),
        "--max-nested-resources",
        str(max(parsed.max_nested_resources, 1)),
        "--pause-ms",
        str(max(parsed.pause_ms, 0)),
        "--initialize-now",
    ]
    if parsed.execute:
        args.append("--execute")
    if parsed.locales:
        args.extend(["--locales", parsed.locales])
    return args


def plist_payload(parsed: argparse.Namespace) -> dict[str, Any]:
    stdout_path = LOG_DIR / "shopify-product-translation.stdout.log"
    stderr_path = LOG_DIR / "shopify-product-translation.stderr.log"
    return {
        "Label": LABEL,
        "ProgramArguments": build_program_arguments(parsed),
        "WorkingDirectory": str(REPO_ROOT),
        "RunAtLoad": True,
        "StartInterval": max(parsed.interval_seconds, 60),
        "StandardOutPath": str(stdout_path),
        "StandardErrorPath": str(stderr_path),
        "ProcessType": "Background",
    }


def write_plist(parsed: argparse.Namespace) -> None:
    PLIST_PATH.parent.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    Path(parsed.state_path).expanduser().parent.mkdir(parents=True, exist_ok=True)
    Path(parsed.cache_path).expanduser().parent.mkdir(parents=True, exist_ok=True)
    with PLIST_PATH.open("wb") as handle:
        plistlib.dump(plist_payload(parsed), handle)


def bootout_if_loaded() -> None:
    target = launchctl_target()
    run_command(["/bin/launchctl", "bootout", target, str(PLIST_PATH)], check=False)


def bootstrap() -> None:
    target = launchctl_target()
    run_command(["/bin/launchctl", "bootstrap", target, str(PLIST_PATH)])
    run_command(["/bin/launchctl", "enable", f"{target}/{LABEL}"], check=False)
    run_command(["/bin/launchctl", "kickstart", "-k", f"{target}/{LABEL}"], check=False)


def uninstall() -> None:
    bootout_if_loaded()
    if PLIST_PATH.exists():
        PLIST_PATH.unlink()


def status(parsed: argparse.Namespace) -> None:
    target = launchctl_target()
    launchctl_result = run_command(["/bin/launchctl", "print", f"{target}/{LABEL}"], check=False)
    state_path = Path(parsed.state_path).expanduser()
    state = {}
    if state_path.exists():
        state = json.loads(state_path.read_text(encoding="utf-8"))
    print(
        json.dumps(
            {
                "label": LABEL,
                "plist_path": str(PLIST_PATH),
                "plist_exists": PLIST_PATH.exists(),
                "loaded": launchctl_result.returncode == 0,
                "state_path": str(state_path),
                "state": state,
            },
            indent=2,
        )
    )


def install(parsed: argparse.Namespace) -> None:
    write_plist(parsed)
    bootout_if_loaded()
    bootstrap()
    status(parsed)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["install", "uninstall", "status"], help="LaunchAgent action.")
    parser.add_argument("--interval-seconds", type=int, default=300, help="How often the worker runs.")
    parser.add_argument("--state-path", default=str(STATE_PATH), help="Persistent worker state path.")
    parser.add_argument(
        "--cache-path",
        default=str(REPO_ROOT / "ops" / "content" / "shopify-product-translation-live-cache.json"),
        help="Shared translation cache path.",
    )
    parser.add_argument("--locales", default="", help="Optional comma-separated locale list override.")
    parser.add_argument("--min-age-seconds", type=int, default=300, help="Wait this long after product creation before translating.")
    parser.add_argument("--page-size", type=int, default=25, help="Recent products page size.")
    parser.add_argument("--max-pages", type=int, default=4, help="Maximum pages scanned per run.")
    parser.add_argument("--max-products-per-run", type=int, default=3, help="Maximum products handled per run.")
    parser.add_argument("--max-nested-resources", type=int, default=100, help="Nested translatable resources fetched per product or option.")
    parser.add_argument("--pause-ms", type=int, default=250, help="Pause between live translation writes.")
    parser.add_argument("--execute", action="store_true", help="Apply translations live instead of dry-run.")
    args = parser.parse_args()

    if args.action == "install":
        install(args)
        return
    if args.action == "uninstall":
        uninstall()
        status(args)
        return
    status(args)


if __name__ == "__main__":
    main()
