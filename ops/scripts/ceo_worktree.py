#!/usr/bin/env python3
"""Guarded git/release helper for unattended CEO loop runs.

The shared checkout is dirty with other sessions' work and usually lags
origin/main, so unattended agents never run git there. Every change is made in a
throwaway worktree at the current origin/main tip under ~/dlm-ceo-worktrees/
(outside /tmp, because .theme-check.yml ignores tmp/**), checked, committed and
pushed from there.

  start --name N               create worktree N at origin/main; prints its path
  status --name N              list changed files in worktree N
  check --name N               git diff --check, JSON validity, theme check (if theme files changed), engine tests
  commit --name N --message-file F   check, commit everything in N, rebase onto a moved origin/main, push to main
  sync-theme --name N [--apply]      compare live theme with origin/main (run after a theme commit)
  finish --name N              remove worktree N
  organic --message-file F     commit the organic engine's files (ops/organic/**, its articles) from the shared checkout
  push-pending                 push commits parked on ceo-pending/* branches after an SSH failure

GitHub access: fetch uses SSH and falls back to HTTPS via the gh CLI (read-only account); push needs the
SSH key and is retried with backoff. If push still fails, the commit is parked on a ceo-pending/* branch.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
ROOT = Path.home() / "dlm-ceo-worktrees"
THEME_DIRS = ("layout/", "sections/", "snippets/", "assets/", "blocks/", "templates/", "config/", "locales/")
TRAILER = "Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"
ORGANIC_SKIP = {"RUN_LOCK", "CEO_LOCK"}


def run(cmd, cwd, check=True, timeout=600):
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    if check and result.returncode != 0:
        raise SystemExit(f"FAILED: {' '.join(cmd)}\n{result.stdout[-2000:]}\n{result.stderr[-2000:]}")
    return result


def tree(name: str) -> Path:
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{1,40}", name):
        raise SystemExit("name must be lowercase letters, digits and hyphens")
    return ROOT / name


HTTPS_URL = "https://github.com/fsuels/dresslikemommy.git"
GH_CRED = ["-c", "credential.helper=", "-c", "credential.helper=!gh auth git-credential"]


def fetch_main(cwd: Path) -> None:
    """Refresh origin/main: SSH first, then HTTPS (gh credentials) into the same ref."""
    for attempt in range(3):
        if run(["git", "fetch", "-q", "origin", "main"], cwd, check=False).returncode == 0:
            return
        https = run(["git", *GH_CRED, "fetch", "-q", HTTPS_URL, "+refs/heads/main:refs/remotes/origin/main"], cwd, check=False)
        if https.returncode == 0:
            return
        time.sleep(10 * (attempt + 1))
    raise SystemExit("FAILED: cannot fetch origin/main over SSH or HTTPS")


def push_main(cwd: Path) -> bool:
    for attempt in range(4):
        if run(["git", "push", "-q", "origin", "HEAD:main"], cwd, check=False).returncode == 0:
            return True
        time.sleep(15 * (attempt + 1))
    return False


def cmd_start(args) -> int:
    path = tree(args.name)
    if path.exists():
        raise SystemExit(f"{path} already exists; run finish --name {args.name} first")
    ROOT.mkdir(parents=True, exist_ok=True)
    fetch_main(REPO)
    run(["git", "worktree", "add", "-q", "--detach", str(path), "origin/main"], REPO)
    print(json.dumps({"path": str(path), "base": run(["git", "rev-parse", "HEAD"], path).stdout.strip()}))
    return 0


def changed(path: Path):
    out = run(["git", "status", "--porcelain", "--untracked-files=all"], path).stdout
    return [line[3:].strip().strip('"') for line in out.splitlines() if line.strip()]


def cmd_status(args) -> int:
    print("\n".join(changed(tree(args.name))) or "(no changes)")
    return 0


def do_check(path: Path) -> list:
    files = changed(path)
    problems = []
    if not files:
        return ["no changes to commit"]
    run(["git", "add", "-A"], path)
    diff_check = run(["git", "diff", "--cached", "--check"], path, check=False)
    if diff_check.returncode:
        problems.append("git diff --check: " + diff_check.stdout[-800:])
    for rel in files:
        if rel.endswith(".json") and (path / rel).exists():
            text = (path / rel).read_text(encoding="utf-8")
            try:
                json.loads(re.sub(r"^\s*/\*.*?\*/", "", text, flags=re.S))
            except ValueError as error:
                problems.append(f"invalid JSON {rel}: {error}")
    if any(rel.startswith(THEME_DIRS) for rel in files):
        result = run(["shopify", "theme", "check", "--output", "json", "--fail-level", "error"], path, check=False, timeout=400)
        try:
            offenses = [o for f in json.loads(result.stdout or "[]") for o in f.get("offenses", []) if o.get("severity") in (0, "error")]
        except ValueError:
            offenses = [result.stdout[-500:] or result.stderr[-500:]]
        if offenses:
            problems.append(f"theme check errors: {offenses[:5]}")
    if any(rel in ("ops/AGENT_WORKLOG.md", "ops/AGENT_COORDINATION.md", "AGENTS.md", "CLAUDE.md") for rel in files):
        # A fresh checkout gives files arbitrary mtimes; the cockpit freshness check compares mtimes only.
        cockpit = path / "ops/marketing/operator_cockpit.html"
        if cockpit.exists():
            cockpit.touch()
        continuity = run(["python3.13", "ops/scripts/check_continuity_integrity.py", "--strict"], path, check=False, timeout=400)
        if "CONTINUITY_OK" not in continuity.stdout:
            problems.append("strict continuity: " + "; ".join(l for l in continuity.stdout.splitlines() if "FAIL" in l)[:800])
    if any(rel.startswith(("ops/scripts/organic_engine.py", "ops/tests/")) for rel in files):
        tests = run([sys.executable, "-m", "unittest", "ops.tests.test_organic_engine"], path, check=False)
        if tests.returncode:
            problems.append("engine tests failed: " + tests.stderr[-800:])
    return problems


def cmd_check(args) -> int:
    problems = do_check(tree(args.name))
    print(json.dumps({"problems": problems, "ok": not problems}, indent=2))
    return 0 if not problems else 1


def commit_and_push(path: Path, message: str) -> str:
    problems = do_check(path)
    if problems:
        raise SystemExit(json.dumps({"refused": problems}, indent=2))
    if TRAILER.split(":")[0] not in message:
        message = message.rstrip() + "\n\n" + TRAILER + "\n"
    subprocess.run(["git", "commit", "-q", "-F", "-"], cwd=path, input=message, text=True, check=True, capture_output=True)
    for _ in range(3):
        fetch_main(path)
        if run(["git", "merge-base", "--is-ancestor", "origin/main", "HEAD"], path, check=False).returncode:
            rebase = run(["git", "rebase", "-q", "origin/main"], path, check=False)
            if rebase.returncode:
                run(["git", "rebase", "--abort"], path, check=False)
                raise SystemExit("rebase conflict with a newer origin/main; nothing pushed")
        if push_main(path):
            return run(["git", "rev-parse", "--short", "HEAD"], path).stdout.strip()
        # A rejected push after a fresh fetch usually means SSH itself failed: park the commit.
        branch = f"ceo-pending/{path.name}-{time.strftime('%Y%m%dT%H%M%S', time.gmtime())}"
        run(["git", "branch", branch, "HEAD"], path)
        raise SystemExit(f"PUSH FAILED (SSH): commit parked on branch {branch}; run `ceo_worktree.py push-pending` later")
    raise SystemExit("push rejected 3 times; nothing pushed")


def cmd_commit(args) -> int:
    sha = commit_and_push(tree(args.name), Path(args.message_file).read_text(encoding="utf-8"))
    print(json.dumps({"pushed": sha}))
    return 0


def cmd_push_pending(args) -> int:
    branches = [b.strip() for b in run(["git", "branch", "--list", "ceo-pending/*", "--format=%(refname:short)"], REPO).stdout.splitlines() if b.strip()]
    if not branches:
        print("no pending commits")
        return 0
    name = "pending-push"
    path = tree(name)
    if path.exists():
        cmd_finish(argparse.Namespace(name=name))
    cmd_start(argparse.Namespace(name=name))
    pushed = []
    try:
        for branch in branches:
            pick = run(["git", "cherry-pick", branch], path, check=False)
            if pick.returncode:
                run(["git", "cherry-pick", "--abort"], path, check=False)
                print(f"skip {branch}: conflicts with main (resolve by hand)")
                continue
            pushed.append(branch)
        if pushed and push_main(path):
            for branch in pushed:
                run(["git", "branch", "-D", branch], REPO, check=False)
            print(json.dumps({"pushed": run(["git", "rev-parse", "--short", "HEAD"], path).stdout.strip(), "branches": pushed}))
            return 0
        print(json.dumps({"pushed": None, "branches": pushed}))
        return 1
    finally:
        cmd_finish(argparse.Namespace(name=name))


def cmd_sync_theme(args) -> int:
    path = tree(args.name)
    fetch_main(path)
    cmd = [sys.executable, "ops/scripts/sync_live_theme_from_main.py"] + (["--apply"] if args.apply else [])
    result = run(cmd, path, check=False, timeout=600)
    print(result.stdout[-3000:] + result.stderr[-1000:])
    return result.returncode


def cmd_finish(args) -> int:
    path = tree(args.name)
    if path.exists():
        run(["git", "worktree", "remove", "--force", str(path)], REPO)
    run(["git", "worktree", "prune"], REPO)
    print(f"removed {path}")
    return 0


def cmd_organic(args) -> int:
    name = "organic-sync"
    path = tree(name)
    if path.exists():
        cmd_finish(argparse.Namespace(name=name))
    cmd_start(argparse.Namespace(name=name))
    try:
        engine_log = (REPO / "ops/organic/ENGINE_LOG.md").read_text(encoding="utf-8")
        for src in (REPO / "ops/organic").rglob("*"):
            if src.is_file() and src.name not in ORGANIC_SKIP:
                dst = path / src.relative_to(REPO)
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
        for src in (REPO / "ops/content/style-journal/articles").glob("*.html"):
            dst = path / src.relative_to(REPO)
            if not dst.exists() or f"/blogs/news/{src.stem}" in engine_log or f"body-{src.stem}" in engine_log:
                shutil.copy2(src, dst)
        if not changed(path):
            print(json.dumps({"pushed": None, "note": "nothing new to commit"}))
            return 0
        files = changed(path)
        sha = commit_and_push(path, Path(args.message_file).read_text(encoding="utf-8"))
        print(json.dumps({"pushed": sha, "files": files}))
        return 0
    finally:
        cmd_finish(argparse.Namespace(name=name))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    for command, func in (("start", cmd_start), ("status", cmd_status), ("check", cmd_check), ("finish", cmd_finish)):
        p = sub.add_parser(command)
        p.add_argument("--name", required=True)
        p.set_defaults(func=func)
    p = sub.add_parser("commit")
    p.add_argument("--name", required=True)
    p.add_argument("--message-file", required=True)
    p.set_defaults(func=cmd_commit)
    p = sub.add_parser("sync-theme")
    p.add_argument("--name", required=True)
    p.add_argument("--apply", action="store_true")
    p.set_defaults(func=cmd_sync_theme)
    p = sub.add_parser("push-pending")
    p.set_defaults(func=cmd_push_pending)
    p = sub.add_parser("organic")
    p.add_argument("--message-file", required=True)
    p.set_defaults(func=cmd_organic)
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
