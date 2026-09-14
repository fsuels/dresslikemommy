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
from datetime import date, timedelta
from pathlib import Path


# Minimum supported Python. Lets the script run under whatever python3 the
# caller has (python3, python3.10, python3.13, etc.) instead of hard-coding a
# single binary name. We still require >= 3.10 for f-strings/dataclass syntax
# already used below.
MIN_PYTHON = (3, 10)
if sys.version_info < MIN_PYTHON:
    sys.stderr.write(
        f"check_continuity_integrity.py requires Python "
        f">= {MIN_PYTHON[0]}.{MIN_PYTHON[1]}; got {sys.version.split()[0]}\n"
    )
    sys.exit(2)

# Use the same interpreter that started this script for all subprocess Python
# calls — avoids hard-coding `python3.13` on systems that only ship `python3`
# (e.g. Linux sandboxes used by browser-based agents).
PYTHON_BIN = sys.executable or "python3"


ROOT = Path(__file__).resolve().parents[2]
OPS = ROOT / "ops"
MARKETING = OPS / "marketing"

CANONICAL_WORKLOG = OPS / "AGENT_WORKLOG.md"
CANONICAL_PROMPT = OPS / "prompts" / "paid-growth-ai-army-continuation-prompt.md"
ALT_WORKLOG_GLOB = "AGENT_WORKLOG*.md"
INTEGRATION_AUDIT = OPS / "scripts" / "audit_marketing_command_integration.py"
PINTEREST_FEED_GROUPING_CHECK = OPS / "scripts" / "check_pinterest_feed_grouping.py"
PINTEREST_FEED_GROUPING_FRESHNESS_MARKER = (
    ROOT
    / "dresslikemommy-growth-2026"
    / "02_AUDIT_PACKETS"
    / "2026-05-15-pinterest-feed-grouping-all-markets-fix"
    / "FIX_LANDED_FRESHNESS_MARKER.txt"
)

COCKPIT_HTML = MARKETING / "operator_cockpit.html"
COCKPIT_RENDERER = OPS / "scripts" / "render_marketing_cockpit.py"
COCKPIT_SOURCES = [
    COCKPIT_RENDERER,
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

MARKETING_FRESHNESS_FILES = {
    "current_marketing_state": MARKETING / "current_marketing_state.md",
    "action_queue": MARKETING / "action_queue.md",
    "daily_scorecard": MARKETING / "daily_scorecard.md",
}
MARKETING_CONTROL_START = "<!-- MARKETING_AUTHORITATIVE_CONTROL:START -->"
MARKETING_CONTROL_END = "<!-- MARKETING_AUTHORITATIVE_CONTROL:END -->"
MAX_LIVE_STATE_AGE_DAYS = 7
MAX_ROOT_BOOTSTRAP_BYTES = 10 * 1024
MAX_PAID_GROWTH_INSTRUCTION_BYTES = 16 * 1024

LISTING_LOCALIZATION_CLOSEOUT = OPS / "scripts" / "finalize_shopify_listing_localization.py"
LISTING_LOCALIZATION_WORKFLOW_FILES = [
    OPS / "prompts" / "START-HERE.md",
    OPS / "prompts" / "shopify-listing-master-prompt.md",
    OPS / "prompts" / "shopify-listing-from-1688.md",
    ROOT / "docs" / "agent-loops" / "product-listing-localization-loop.md",
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
    return CheckResult(
        "spend_authority_agreement",
        True,
        f"core files agree on standing record {status}; semantic control determines effective action authority",
    )


def parse_reconciled_date(text: str) -> date | None:
    match = re.search(r"^Last reconciled:\s*(\d{4}-\d{2}-\d{2})\b", text, re.MULTILINE)
    if not match:
        return None
    try:
        return date.fromisoformat(match.group(1))
    except ValueError:
        return None


def parse_authoritative_control(text: str) -> dict[str, str]:
    start = text.find(MARKETING_CONTROL_START)
    end = text.find(MARKETING_CONTROL_END)
    if start == -1 or end == -1 or end <= start:
        return {}
    block = text[start + len(MARKETING_CONTROL_START) : end]
    return {
        key: value
        for key, value in re.findall(
            r"^-\s+`([a-z_]+)`:\s+`([^`\n]+)`\s*$",
            block,
            re.MULTILINE,
        )
    }


def green_action_rows(action_queue_text: str) -> list[str]:
    return re.findall(
        r"^\|[^|\n]+\|\s*GREEN\s*\|[^\n]*$",
        action_queue_text,
        re.MULTILINE,
    )


def has_green_action(action_queue_text: str) -> bool:
    return bool(green_action_rows(action_queue_text))


def evaluate_marketing_semantic_freshness(
    state_text: str,
    action_queue_text: str,
    scorecard_text: str,
    *,
    today: date,
    spend_status: str | None = None,
) -> CheckResult:
    texts = {
        "current_marketing_state": state_text,
        "action_queue": action_queue_text,
        "daily_scorecard": scorecard_text,
    }
    reconciled_dates: dict[str, date] = {}
    for name, text in texts.items():
        reconciled = parse_reconciled_date(text)
        if reconciled is None:
            return CheckResult(
                "marketing_semantic_freshness",
                False,
                f"{name} is missing a valid Last reconciled YYYY-MM-DD date",
            )
        if reconciled > today:
            return CheckResult(
                "marketing_semantic_freshness",
                False,
                f"{name} has a future Last reconciled date {reconciled.isoformat()}",
            )
        reconciled_dates[name] = reconciled

    control = parse_authoritative_control(state_text)
    if not control:
        oldest_age = max((today - value).days for value in reconciled_dates.values())
        return CheckResult(
            "marketing_semantic_freshness",
            False,
            "missing authoritative marketing control block"
            + (f"; oldest command-layer readback is {oldest_age} days old" if oldest_age else ""),
        )

    required_fields = {
        "control_as_of",
        "source_live_evidence_as_of",
        "live_state_mode",
        "live_readback_fresh_until",
        "autonomous_action_ready",
        "effective_approval_policy",
        "approved_external_scope",
        "next_best_action",
        "supersedes_execution_readiness_below",
    }
    missing_fields = sorted(required_fields - control.keys())
    if missing_fields:
        return CheckResult(
            "marketing_semantic_freshness",
            False,
            f"authoritative control block is missing: {', '.join(missing_fields)}",
        )

    control_dates: dict[str, date] = {}
    for field in ("control_as_of", "source_live_evidence_as_of"):
        try:
            parsed = date.fromisoformat(control[field])
        except ValueError:
            return CheckResult(
                "marketing_semantic_freshness",
                False,
                f"{field} must be YYYY-MM-DD",
            )
        if parsed > today:
            return CheckResult(
                "marketing_semantic_freshness",
                False,
                f"{field} cannot be in the future",
            )
        control_dates[field] = parsed

    if control["supersedes_execution_readiness_below"] != "true":
        return CheckResult(
            "marketing_semantic_freshness",
            False,
            "authoritative control block must supersede older execution-readiness labels",
        )
    if control_dates["source_live_evidence_as_of"] > control_dates["control_as_of"]:
        return CheckResult(
            "marketing_semantic_freshness",
            False,
            "source_live_evidence_as_of cannot be later than control_as_of",
        )

    mode = control["live_state_mode"]
    green_action = has_green_action(action_queue_text)
    if mode == "STALE_READBACK_REQUIRED":
        expected = {
            "live_readback_fresh_until": "EXPIRED",
            "autonomous_action_ready": "false",
            "effective_approval_policy": "FRESH_ACTION_TIME_APPROVAL_REQUIRED",
            "approved_external_scope": "NONE",
            "next_best_action": "READ_ONLY_MARKETING_RECONCILIATION",
        }
        mismatches = [
            f"{key}={control[key]!r} (expected {value!r})"
            for key, value in expected.items()
            if control[key] != value
        ]
        if mismatches:
            return CheckResult(
                "marketing_semantic_freshness",
                False,
                "stale mode is not fail-closed: " + "; ".join(mismatches),
            )
        if green_action:
            return CheckResult(
                "marketing_semantic_freshness",
                False,
                "stale mode cannot coexist with a GREEN action-queue row",
            )
        oldest = min(reconciled_dates.values())
        return CheckResult(
            "marketing_semantic_freshness",
            True,
            "stale command layer is explicitly fail-closed; "
            f"oldest readback {oldest.isoformat()}, next action read-only reconciliation",
        )

    if mode != "LIVE_CURRENT":
        return CheckResult(
            "marketing_semantic_freshness",
            False,
            f"unknown live_state_mode {mode!r}",
        )

    stale_control_dates = [
        f"{name}={(today - value).days}d"
        for name, value in control_dates.items()
        if (today - value).days > MAX_LIVE_STATE_AGE_DAYS
    ]
    if stale_control_dates:
        return CheckResult(
            "marketing_semantic_freshness",
            False,
            "LIVE_CURRENT control evidence exceeds semantic freshness limit: "
            + ", ".join(stale_control_dates),
        )

    stale_files = [
        f"{name}={(today - reconciled).days}d"
        for name, reconciled in reconciled_dates.items()
        if (today - reconciled).days > MAX_LIVE_STATE_AGE_DAYS
    ]
    if stale_files:
        return CheckResult(
            "marketing_semantic_freshness",
            False,
            "LIVE_CURRENT exceeds semantic freshness limit: " + ", ".join(stale_files),
        )
    source_date = control_dates["source_live_evidence_as_of"]
    lagging_files = [
        name
        for name, reconciled in reconciled_dates.items()
        if reconciled < source_date
    ]
    if lagging_files:
        return CheckResult(
            "marketing_semantic_freshness",
            False,
            "LIVE_CURRENT command-layer date predates source evidence: "
            + ", ".join(lagging_files),
        )

    try:
        fresh_until = date.fromisoformat(control["live_readback_fresh_until"])
    except ValueError:
        return CheckResult(
            "marketing_semantic_freshness",
            False,
            "LIVE_CURRENT live_readback_fresh_until must be YYYY-MM-DD",
        )
    if fresh_until < today:
        return CheckResult(
            "marketing_semantic_freshness",
            False,
            f"LIVE_CURRENT readback expired on {fresh_until.isoformat()}",
        )
    maximum_fresh_until = (
        control_dates["source_live_evidence_as_of"]
        + timedelta(days=MAX_LIVE_STATE_AGE_DAYS)
    )
    if fresh_until > maximum_fresh_until:
        return CheckResult(
            "marketing_semantic_freshness",
            False,
            "LIVE_CURRENT fresh-until date exceeds the evidence-age limit: "
            f"{fresh_until.isoformat()} > {maximum_fresh_until.isoformat()}",
        )

    ready = control["autonomous_action_ready"]
    if ready not in {"true", "false"}:
        return CheckResult(
            "marketing_semantic_freshness",
            False,
            "autonomous_action_ready must be true or false",
        )
    if ready == "true":
        if spend_status != "APPROVED_ACTIVE":
            return CheckResult(
                "marketing_semantic_freshness",
                False,
                "autonomous action requires spend_authorization Status APPROVED_ACTIVE",
            )
        if control["effective_approval_policy"] != "APPROVED_ACTIVE_WITHIN_CAPS":
            return CheckResult(
                "marketing_semantic_freshness",
                False,
                "autonomous action requires APPROVED_ACTIVE_WITHIN_CAPS",
            )
        if control["approved_external_scope"] == "NONE":
            return CheckResult(
                "marketing_semantic_freshness",
                False,
                "autonomous action requires a non-empty approved_external_scope",
            )
        green_rows = green_action_rows(action_queue_text)
        if not green_rows:
            return CheckResult(
                "marketing_semantic_freshness",
                False,
                "autonomous action requires at least one GREEN action-queue row",
            )
        approved_scope = control["approved_external_scope"]
        exact_scope_marker = f"`{approved_scope}`"
        if not any(exact_scope_marker in row for row in green_rows):
            return CheckResult(
                "marketing_semantic_freshness",
                False,
                "approved_external_scope must be named exactly in backticks in a GREEN action-queue row",
            )
    else:
        if control["effective_approval_policy"] != "FRESH_ACTION_TIME_APPROVAL_REQUIRED":
            return CheckResult(
                "marketing_semantic_freshness",
                False,
                "non-autonomous LIVE_CURRENT mode requires FRESH_ACTION_TIME_APPROVAL_REQUIRED",
            )
        if control["approved_external_scope"] != "NONE":
            return CheckResult(
                "marketing_semantic_freshness",
                False,
                "non-autonomous LIVE_CURRENT mode requires approved_external_scope=NONE",
            )
        if green_action:
            return CheckResult(
                "marketing_semantic_freshness",
                False,
                "GREEN action-queue row requires autonomous_action_ready=true",
            )

    return CheckResult(
        "marketing_semantic_freshness",
        True,
        f"live command layer is current through {fresh_until.isoformat()}; autonomous_action_ready={ready}",
    )


def check_marketing_semantic_freshness() -> CheckResult:
    missing = [
        rel(path)
        for path in MARKETING_FRESHNESS_FILES.values()
        if not path.exists()
    ]
    if missing:
        return CheckResult(
            "marketing_semantic_freshness",
            False,
            f"missing command-layer file(s): {', '.join(missing)}",
        )
    return evaluate_marketing_semantic_freshness(
        read_text(MARKETING_FRESHNESS_FILES["current_marketing_state"]),
        read_text(MARKETING_FRESHNESS_FILES["action_queue"]),
        read_text(MARKETING_FRESHNESS_FILES["daily_scorecard"]),
        today=date.today(),
        spend_status=parse_spend_status(),
    )


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
        [PYTHON_BIN, str(INTEGRATION_AUDIT), "--fail-on-risk"],
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


def check_pinterest_feed_grouping() -> CheckResult:
    """Wire the Pinterest feed grouping guardrail into continuity.

    Behavior:
    - If the freshness marker file does NOT exist, the fix is still in
      progress: run the guardrail in report-only mode and PASS as long as
      it produces output without errors. This prevents false-alarming on
      the current per-variant feed snapshots while the channel toggle is
      being approved/applied.
    - If the freshness marker DOES exist, run the guardrail in strict
      mode: any per-variant regression FAILS continuity.

    To flip the gate to strict, an agent must create the marker file
    after capturing a clean after-state readback per market. The marker
    is a tiny text file with the marker date and the per-market readback
    summary; creating it is itself an attested action.
    """
    if not PINTEREST_FEED_GROUPING_CHECK.exists():
        return CheckResult(
            "pinterest_feed_grouping",
            False,
            f"missing {rel(PINTEREST_FEED_GROUPING_CHECK)}",
        )
    strict_mode = False
    if PINTEREST_FEED_GROUPING_FRESHNESS_MARKER.exists():
        try:
            marker_text = PINTEREST_FEED_GROUPING_FRESHNESS_MARKER.read_text(encoding="utf-8")
        except Exception:
            marker_text = ""
        # Only flip to strict mode if the marker contains the explicit attest
        # phrase as the FIRST non-blank non-comment line. A test-only or
        # accidental file does not flip the gate; this prevents accidental
        # strictification from leftover smoke-test artifacts or from
        # documentation inside the marker that merely mentions the phrase.
        ATTEST_PHRASE = "FIX_LANDED_ATTEST: per-market after-state readback complete"
        for raw in marker_text.splitlines():
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if line == ATTEST_PHRASE or line.startswith(ATTEST_PHRASE):
                strict_mode = True
            break
    cmd = [PYTHON_BIN, str(PINTEREST_FEED_GROUPING_CHECK)]
    if strict_mode:
        cmd.append("--strict")
    else:
        cmd.extend(["--report-only", "--strict"])
    proc = subprocess.run(
        cmd,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=120,
        check=False,
    )
    if proc.returncode == 2:
        return CheckResult(
            "pinterest_feed_grouping",
            False,
            f"guardrail script ERROR rc=2: {proc.stderr[-200:] or proc.stdout[-200:]}",
        )
    if strict_mode and proc.returncode != 0:
        tail = "\n".join((proc.stdout + proc.stderr).splitlines()[-8:])
        return CheckResult(
            "pinterest_feed_grouping",
            False,
            f"strict-mode regression detected after fix landed: {tail}",
        )
    # In fix-in-progress mode the guardrail returns 0 even with FAIL findings.
    fails = re.findall(r"^- FAIL", proc.stdout, re.MULTILINE)
    if strict_mode:
        return CheckResult(
            "pinterest_feed_grouping",
            True,
            "strict guardrail PASS after fix landed",
        )
    return CheckResult(
        "pinterest_feed_grouping",
        True,
        f"fix-in-progress mode (no freshness marker yet); guardrail reports {len(fails)} FAIL snapshot(s) to remediate",
    )


def check_agent_bootstrap_parity() -> CheckResult:
    agents = ROOT / "AGENTS.md"
    claude = ROOT / "CLAUDE.md"
    if not agents.exists() or not claude.exists():
        return CheckResult("agent_bootstrap_parity", False, "AGENTS.md or CLAUDE.md is missing")
    if agents.read_bytes() != claude.read_bytes():
        return CheckResult("agent_bootstrap_parity", False, "AGENTS.md and CLAUDE.md are not byte-for-byte identical")
    root_bytes = agents.stat().st_size
    marketing_guide = MARKETING / "AGENTS.md"
    marketing_bytes = marketing_guide.stat().st_size if marketing_guide.exists() else 0
    paid_growth_chain_bytes = root_bytes + marketing_bytes
    if root_bytes > MAX_ROOT_BOOTSTRAP_BYTES:
        return CheckResult(
            "agent_bootstrap_parity",
            False,
            f"root bootstrap is {root_bytes} bytes; compact below {MAX_ROOT_BOOTSTRAP_BYTES}",
        )
    if paid_growth_chain_bytes > MAX_PAID_GROWTH_INSTRUCTION_BYTES:
        return CheckResult(
            "agent_bootstrap_parity",
            False,
            f"root plus paid-growth bootstrap is {paid_growth_chain_bytes} bytes; compact below {MAX_PAID_GROWTH_INSTRUCTION_BYTES}",
        )
    return CheckResult(
        "agent_bootstrap_parity",
        True,
        "AGENTS.md and CLAUDE.md are byte-identical; instruction budgets pass "
        f"(root={root_bytes}, root+paid-growth={paid_growth_chain_bytes} bytes)",
    )


def check_listing_localization_workflow() -> CheckResult:
    if not LISTING_LOCALIZATION_CLOSEOUT.exists():
        return CheckResult(
            "listing_localization_workflow",
            False,
            f"missing {rel(LISTING_LOCALIZATION_CLOSEOUT)}",
        )

    closeout_text = read_text(LISTING_LOCALIZATION_CLOSEOUT)
    required_closeout_markers = [
        "poll_shopify_product_translations.py",
        "--min-age-seconds",
        "--force-refresh",
        "audit_shopify_product_translation_completeness.py",
        "repair_localized_product_size_charts.py",
        "audit_localized_size_chart_variant_mapping.py",
    ]
    missing_markers = [marker for marker in required_closeout_markers if marker not in closeout_text]

    missing_files: list[str] = []
    missing_references: list[str] = []
    for path in LISTING_LOCALIZATION_WORKFLOW_FILES:
        if not path.exists():
            missing_files.append(rel(path))
            continue
        if "finalize_shopify_listing_localization.py" not in read_text(path):
            missing_references.append(rel(path))

    if missing_markers or missing_files or missing_references:
        details = []
        if missing_markers:
            details.append(f"closeout missing marker(s): {', '.join(missing_markers)}")
        if missing_files:
            details.append(f"missing workflow file(s): {', '.join(missing_files)}")
        if missing_references:
            details.append(f"workflow file(s) do not require closeout: {', '.join(missing_references)}")
        return CheckResult("listing_localization_workflow", False, "; ".join(details))

    return CheckResult(
        "listing_localization_workflow",
        True,
        "synchronous closeout is wired into canonical listing workflow files with immediate translation and strict audits",
    )


def run_checks() -> list[CheckResult]:
    worklog_result, anchor = check_canonical_worklog()
    return [
        worklog_result,
        check_alternate_worklogs(),
        check_prompt_anchor_policy(anchor),
        check_spend_authority_agreement(),
        check_marketing_semantic_freshness(),
        check_cockpit_freshness(),
        check_marketing_integration_audit(),
        check_pinterest_feed_grouping(),
        check_listing_localization_workflow(),
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
