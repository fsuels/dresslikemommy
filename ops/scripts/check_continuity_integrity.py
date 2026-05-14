#!/usr/bin/env python3
"""Strict continuity guard for the paid-growth command layer.

This complements ``audit_marketing_command_integration.py``. The marketing
audit catches side documents inside ``ops/marketing``; this script checks the
broader continuity spine that future agents rely on before they act.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OPS = ROOT / "ops"
MARKETING = OPS / "marketing"

CANONICAL_WORKLOG = OPS / "AGENT_WORKLOG.md"
CANONICAL_PROMPT = OPS / "prompts" / "paid-growth-ai-army-continuation-prompt.md"
ALT_WORKLOG_GLOB = "AGENT_WORKLOG*.md"
INTEGRATION_AUDIT = OPS / "scripts" / "audit_marketing_command_integration.py"

COCKPIT_HTML = MARKETING / "operator_cockpit.html"
COCKPIT_SOURCES = [
    MARKETING / "operator_cockpit.md",
    MARKETING / "current_marketing_state.md",
    MARKETING / "action_queue.md",
    MARKETING / "daily_scorecard.md",
    MARKETING / "blocker_board.md",
    MARKETING / "spend_authorization.md",
    MARKETING / "campaign_explorer.json",
    MARKETING / "memory_digest.md",
]

SPEND_CORE_FILES = [
    MARKETING / "current_marketing_state.md",
    MARKETING / "action_queue.md",
    MARKETING / "blocker_board.md",
    MARKETING / "operator_cockpit.md",
    COCKPIT_HTML,
]


@dataclass
class CheckResult:
    name: str
    ok: bool
    detail: str

    @property
    def status(self) -> str:
        return "PASS" if self.ok else "FAIL"


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(errors="replace")


def latest_anchor(text: str) -> str | None:
    matches = re.findall(r"AGENT_CONTINUITY_ANCHOR:\s*([A-Za-z0-9_.:-]+)", text)
    return matches[-1] if matches else None


def session_titles(text: str) -> set[str]:
    return set(re.findall(r"^Session:\s*(.+)$", text, re.MULTILINE))


def check_canonical_worklog() -> tuple[CheckResult, str | None]:
    if not CANONICAL_WORKLOG.exists():
        return CheckResult("canonical_worklog", False, f"missing {rel(CANONICAL_WORKLOG)}"), None

    text = read_text(CANONICAL_WORKLOG)
    line_count = len(text.splitlines())
    anchor = latest_anchor(text)
    if line_count < 100:
        return CheckResult("canonical_worklog", False, f"{rel(CANONICAL_WORKLOG)} has only {line_count} lines"), anchor
    if not anchor:
        return CheckResult("canonical_worklog", False, f"{rel(CANONICAL_WORKLOG)} has no AGENT_CONTINUITY_ANCHOR"), None
    return CheckResult("canonical_worklog", True, f"{rel(CANONICAL_WORKLOG)} has {line_count} lines; latest anchor {anchor}"), anchor


def check_alternate_worklogs() -> CheckResult:
    canonical_text = read_text(CANONICAL_WORKLOG) if CANONICAL_WORKLOG.exists() else ""
    canonical_sessions = session_titles(canonical_text)
    failures: list[str] = []
    details: list[str] = []

    for path in sorted(OPS.glob(ALT_WORKLOG_GLOB)):
        if path == CANONICAL_WORKLOG:
            continue
        text = read_text(path)
        head = "\n".join(text.splitlines()[:20])
        missing_markers = [
            marker
            for marker in (
                "HISTORICAL_DO_NOT_USE",
                "Canonical source: `ops/AGENT_WORKLOG.md`",
                "Migration status: `COMPARED_UNIQUE_SUMMARIZED_IN_CANONICAL`",
            )
            if marker not in head
        ]
        alt_sessions = session_titles(text)
        unique_sessions = sorted(alt_sessions - canonical_sessions)
        if missing_markers:
            failures.append(f"{rel(path)} missing quarantine marker(s): {', '.join(missing_markers)}")
        if unique_sessions and "AGENT_WORKLOG_utf8.md` unique historical session titles summarized" not in canonical_text:
            failures.append(f"{rel(path)} has {len(unique_sessions)} unique session titles not summarized in canonical worklog")
        details.append(f"{rel(path)} quarantined; {len(unique_sessions)} unique historical session titles compared")

    if failures:
        return CheckResult("alternate_worklogs", False, "; ".join(failures))
    if not details:
        return CheckResult("alternate_worklogs", True, "no alternate AGENT_WORKLOG*.md files present")
    return CheckResult("alternate_worklogs", True, "; ".join(details))


def check_prompt_anchor_policy(latest: str | None) -> CheckResult:
    if not CANONICAL_PROMPT.exists():
        return CheckResult("prompt_anchor_policy", False, f"missing {rel(CANONICAL_PROMPT)}")
    text = read_text(CANONICAL_PROMPT)
    first_actions = text
    start = text.find("## First actions")
    end = text.find("## North Star")
    if start != -1 and end != -1 and end > start:
        first_actions = text[start:end]

    stale_phrase = "As of this prompt refresh, the latest paid-growth anchor is"
    required = "Resolve the latest `AGENT_CONTINUITY_ANCHOR` from `ops/AGENT_WORKLOG.md`"
    if stale_phrase in first_actions:
        return CheckResult("prompt_anchor_policy", False, "canonical prompt still hard-codes a latest-anchor phrase in First actions")
    if re.search(r"AGENT_CONTINUITY_ANCHOR:\s*[A-Za-z0-9_.:-]+", first_actions):
        return CheckResult("prompt_anchor_policy", False, "canonical prompt First actions contains a literal anchor instead of resolving from worklog")
    if required not in first_actions:
        return CheckResult("prompt_anchor_policy", False, "canonical prompt does not require resolving latest anchor from worklog")
    return CheckResult("prompt_anchor_policy", True, f"prompt resolves latest anchor from worklog; current worklog latest is {latest or 'unknown'}")


def parse_spend_status() -> str | None:
    path = MARKETING / "spend_authorization.md"
    if not path.exists():
        return None
    match = re.search(r"^Status:\s*`([^`]+)`", read_text(path), re.MULTILINE)
    return match.group(1) if match else None


def check_spend_authority_agreement() -> CheckResult:
    status = parse_spend_status()
    if not status:
        return CheckResult("spend_authority_agreement", False, "could not parse Status from ops/marketing/spend_authorization.md")
    if status not in {"APPROVED_ACTIVE", "PENDING_OWNER_APPROVAL"}:
        return CheckResult("spend_authority_agreement", False, f"unexpected spend status {status}")

    failures: list[str] = []
    for path in SPEND_CORE_FILES:
        if not path.exists():
            failures.append(f"missing {rel(path)}")
            continue
        text = read_text(path)
        if status not in text:
            failures.append(f"{rel(path)} does not mention active spend status {status}")

    blocker = MARKETING / "blocker_board.md"
    if blocker.exists():
        line = next((line for line in read_text(blocker).splitlines() if "Standing bounded spend authority" in line), "")
        if status not in line:
            failures.append("blocker_board standing authority row does not match spend_authorization.md")

    if failures:
        return CheckResult("spend_authority_agreement", False, "; ".join(failures))
    return CheckResult("spend_authority_agreement", True, f"core command-layer files agree on {status}")


def check_cockpit_freshness() -> CheckResult:
    if not COCKPIT_HTML.exists():
        return CheckResult("cockpit_freshness", False, f"missing {rel(COCKPIT_HTML)}")
    missing_sources = [rel(path) for path in COCKPIT_SOURCES if not path.exists()]
    if missing_sources:
        return CheckResult("cockpit_freshness", False, f"missing cockpit source(s): {', '.join(missing_sources)}")

    latest_source = max(path.stat().st_mtime for path in COCKPIT_SOURCES)
    stale_sources = [rel(path) for path in COCKPIT_SOURCES if path.stat().st_mtime > COCKPIT_HTML.stat().st_mtime]
    if COCKPIT_HTML.stat().st_mtime < latest_source:
        return CheckResult("cockpit_freshness", False, f"{rel(COCKPIT_HTML)} is older than: {', '.join(stale_sources)}")

    status = parse_spend_status()
    html = read_text(COCKPIT_HTML)
    if status and status not in html:
        return CheckResult("cockpit_freshness", False, f"{rel(COCKPIT_HTML)} does not contain current spend status {status}")
    return CheckResult("cockpit_freshness", True, f"{rel(COCKPIT_HTML)} is newer than cockpit sources")


def check_marketing_integration_audit() -> CheckResult:
    if not INTEGRATION_AUDIT.exists():
        return CheckResult("marketing_integration_audit", False, f"missing {rel(INTEGRATION_AUDIT)}")
    proc = subprocess.run(
        ["python3.13", str(INTEGRATION_AUDIT), "--fail-on-risk"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=60,
        check=False,
    )
    if proc.returncode != 0:
        tail = "\n".join((proc.stdout + proc.stderr).splitlines()[-8:])
        return CheckResult("marketing_integration_audit", False, f"audit returned {proc.returncode}: {tail}")
    match = re.search(r"Side-document risks:\s*`?(\d+)`?", proc.stdout)
    if not match:
        return CheckResult("marketing_integration_audit", False, "audit output did not include side-document risk count")
    if match.group(1) != "0":
        return CheckResult("marketing_integration_audit", False, f"audit reports {match.group(1)} side-document risks")
    return CheckResult("marketing_integration_audit", True, "marketing integration audit reports 0 side-document risks")


def check_agent_bootstrap_parity() -> CheckResult:
    agents = ROOT / "AGENTS.md"
    claude = ROOT / "CLAUDE.md"
    if not agents.exists() or not claude.exists():
        return CheckResult("agent_bootstrap_parity", False, "AGENTS.md or CLAUDE.md is missing")
    if agents.read_bytes() != claude.read_bytes():
        return CheckResult("agent_bootstrap_parity", False, "AGENTS.md and CLAUDE.md are not byte-for-byte identical")
    return CheckResult("agent_bootstrap_parity", True, "AGENTS.md and CLAUDE.md are byte-for-byte identical")


def run_checks() -> list[CheckResult]:
    worklog_result, anchor = check_canonical_worklog()
    return [
        worklog_result,
        check_alternate_worklogs(),
        check_prompt_anchor_policy(anchor),
        check_spend_authority_agreement(),
        check_cockpit_freshness(),
        check_marketing_integration_audit(),
        check_agent_bootstrap_parity(),
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true", help="fail with a nonzero exit code on any integrity failure")
    args = parser.parse_args()

    results = run_checks()
    failed = [result for result in results if not result.ok]

    print("# Continuity Integrity Check")
    print("")
    for result in results:
        print(f"- {result.status} {result.name}: {result.detail}")
    print("")
    if failed:
        print("CONTINUITY_FAILED")
        return 1 if args.strict else 0
    print("CONTINUITY_OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
