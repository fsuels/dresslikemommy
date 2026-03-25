#!/usr/bin/env python3
import argparse
import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OPS_DIR = ROOT / "ops"
CONTENT_DIR = OPS_DIR / "content"
LOG_DIR = OPS_DIR / "logs" / "translation"
REGISTRY_PATH = CONTENT_DIR / "translation-batches.json"
SYNC_SCRIPT = ROOT / "ops" / "scripts" / "sync_shopify_translations.py"

sys.path.append(str(SYNC_SCRIPT.parent))
from sync_shopify_translations import DEFAULT_EXPORT_DIR, load_candidates  # noqa: E402


BATCHES = {
    "west": ["es", "fr", "de", "it", "pt-BR"],
    "northern": ["nl", "pl", "ru", "sv", "tr"],
    "asia": ["ar", "hi", "id", "th", "vi"],
    "cjk": ["ja", "ko", "zh-CN", "zh-TW"],
}


def batch_paths(name):
    return {
        "cache": CONTENT_DIR / f"shopify-translation-cache-{name}.json",
        "report": CONTENT_DIR / f"shopify-translation-sync-report-{name}.json",
        "jsonl": CONTENT_DIR / f"shopify-translation-bulk-{name}.jsonl",
        "log": LOG_DIR / f"{name}.log",
    }


def load_registry():
    if not REGISTRY_PATH.exists():
        return {}
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def save_registry(data):
    CONTENT_DIR.mkdir(parents=True, exist_ok=True)
    REGISTRY_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def pid_alive(pid):
    if not pid:
        return False
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True


def command_for(name):
    paths = batch_paths(name)
    return [
        sys.executable,
        str(SYNC_SCRIPT),
        "--locales",
        ",".join(BATCHES[name]),
        "--cache",
        str(paths["cache"]),
        "--report",
        str(paths["report"]),
        "--jsonl-path",
        str(paths["jsonl"]),
    ]


def start_batches(force_restart=False):
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    registry = load_registry()
    if force_restart:
        stop_batches()
        registry = {}

    updates = {}
    for name in BATCHES:
        existing = registry.get(name, {})
        if pid_alive(existing.get("pid")):
            updates[name] = existing
            continue

        paths = batch_paths(name)
        with paths["log"].open("a", encoding="utf-8") as handle:
            handle.write(
                f"\n=== START {time.strftime('%Y-%m-%d %H:%M:%S')} batch={name} "
                f"locales={','.join(BATCHES[name])} ===\n"
            )
            handle.flush()
            process = subprocess.Popen(
                command_for(name),
                cwd=str(ROOT),
                stdout=handle,
                stderr=subprocess.STDOUT,
                start_new_session=True,
            )

        updates[name] = {
            "pid": process.pid,
            "started_at": int(time.time()),
            "locales": BATCHES[name],
            "log_path": str(paths["log"]),
            "cache_path": str(paths["cache"]),
            "report_path": str(paths["report"]),
            "jsonl_path": str(paths["jsonl"]),
            "command": command_for(name),
        }

    save_registry(updates)
    return updates


def stop_batches():
    registry = load_registry()
    pids = set()
    for item in registry.values():
        pid = item.get("pid")
        if pid_alive(pid):
            pids.add(pid)
    result = subprocess.run(
        ["pgrep", "-f", "sync_shopify_translations.py --locales"],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
    )
    for line in result.stdout.splitlines():
        line = line.strip()
        if line.isdigit():
            pids.add(int(line))

    for pid in sorted(pids):
        if pid_alive(pid):
            os.kill(pid, signal.SIGTERM)
    time.sleep(1)
    for pid in sorted(pids):
        if pid_alive(pid):
            os.kill(pid, signal.SIGKILL)
    save_registry({})


def target_counts(locales):
    _, unique_texts, _ = load_candidates(DEFAULT_EXPORT_DIR, locales)
    return {locale: len(texts) for locale, texts in unique_texts.items()}


def cache_counts(path):
    cache_path = Path(path)
    if not cache_path.exists():
        return {}
    data = json.loads(cache_path.read_text(encoding="utf-8"))
    return {locale: len(values) for locale, values in data.items()}


def tail_log(path, lines=3):
    log_path = Path(path)
    if not log_path.exists():
        return []
    content = log_path.read_text(encoding="utf-8", errors="replace").splitlines()
    return content[-lines:]


def print_status():
    registry = load_registry()
    now = time.time()
    for name, locales in BATCHES.items():
        entry = registry.get(name, {})
        paths = batch_paths(name)
        alive = pid_alive(entry.get("pid"))
        targets = target_counts(locales)
        counts = cache_counts(paths["cache"])
        mtime_age = None
        if paths["cache"].exists():
            mtime_age = now - paths["cache"].stat().st_mtime

        print(f"{name}: pid={entry.get('pid')} alive={alive} log={paths['log']}")
        for locale in locales:
            current = counts.get(locale, 0)
            target = targets.get(locale, 0)
            shown = min(current, target)
            pct = (shown / target * 100) if target else 0.0
            extra = " (cache exceeds target)" if current > target else ""
            print(f"  {locale}: {shown}/{target} ({pct:.1f}%) raw_cache={current}{extra}")
        if mtime_age is None:
            print("  cache_age: missing")
        else:
            print(f"  cache_age_seconds: {mtime_age:.1f}")
        print(f"  report_exists: {paths['report'].exists()} jsonl_exists: {paths['jsonl'].exists()}")
        for line in tail_log(paths["log"]):
            print(f"  log: {line}")


def main():
    parser = argparse.ArgumentParser(description="Start, stop, and inspect Shopify translation batch workers.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    start_parser = subparsers.add_parser("start")
    start_parser.add_argument("--force-restart", action="store_true")

    subparsers.add_parser("stop")
    subparsers.add_parser("status")

    args = parser.parse_args()

    if args.command == "start":
        start_batches(force_restart=args.force_restart)
        print_status()
        return
    if args.command == "stop":
        stop_batches()
        print("stopped translation batches")
        return
    if args.command == "status":
        print_status()
        return


if __name__ == "__main__":
    main()
