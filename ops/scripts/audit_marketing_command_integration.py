#!/usr/bin/env python3
"""Audit whether ops/marketing artifacts are wired into the command loop.

The goal is to catch "side documents": files that exist but are not registered,
referenced by execution surfaces, or marked as intentional archive/generated
artifacts.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MARKETING_DIR = ROOT / "ops" / "marketing"
REPORT = MARKETING_DIR / "command_layer_integration_audit.md"

TRACKED_SUFFIXES = {".md", ".csv", ".json", ".html"}

CORE_FILES = {
    "AGENTS.md",
    "action_queue.md",
    "assumption_log.md",
    "blocker_board.md",
    "campaign_explorer.json",
    "current_marketing_state.md",
    "daily_scorecard.md",
    "decision_log.md",
    "memory_digest.md",
    "operator_cockpit.md",
    "prompt_log.md",
    "review_log.md",
    "reviewer_checklist.md",
    "spend_authorization.md",
    "team_registry.md",
}

GENERATED_OR_CONTROLLED = {
    "operator_cockpit.html": "generated cockpit",
    "command_layer_integration_audit.md": "generated integration audit",
}

ACTION_SURFACES = {
    "ops/marketing/action_queue.md",
    "ops/marketing/current_marketing_state.md",
    "ops/marketing/daily_scorecard.md",
    "ops/marketing/blocker_board.md",
    "ops/marketing/operator_cockpit.md",
    "ops/PROBLEM_TRACKER.md",
}

REFERENCE_SURFACES = [
    "AGENTS.md",
    "CLAUDE.md",
    "ops/marketing/AGENTS.md",
    "ops/marketing/action_queue.md",
    "ops/marketing/current_marketing_state.md",
    "ops/marketing/daily_scorecard.md",
    "ops/marketing/blocker_board.md",
    "ops/marketing/operator_cockpit.md",
    "ops/marketing/memory_digest.md",
    "ops/marketing/decision_log.md",
    "ops/marketing/review_log.md",
    "ops/marketing/assumption_log.md",
    "ops/marketing/prompt_log.md",
    "ops/marketing/campaign_explorer.json",
    "ops/PROBLEM_TRACKER.md",
    "ops/AGENT_COORDINATION.md",
    "ops/AGENT_WORKLOG.md",
]


@dataclass
class AuditRow:
    file: str
    status: str
    registered: bool
    ref_count: int
    action_ref: bool
    refs: list[str]
    fix: str


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(errors="replace")


def is_registered(name: str, rel: str, registry_text: str) -> bool:
    if name == "AGENTS.md":
        return True
    return name in registry_text or rel in registry_text


def is_archive_reference(path: Path) -> bool:
    if path.suffix != ".md":
        return False
    text = read_text(path)
    markers = (
        "Integration status: `ARCHIVE_REFERENCE`",
        "Integration status: ARCHIVE_REFERENCE",
        "Integration status: `GENERATED`",
        "Integration status: GENERATED",
    )
    return any(marker in text for marker in markers)


def find_refs(name: str, rel: str, surfaces: dict[str, str]) -> list[str]:
    refs: list[str] = []
    for surface, text in surfaces.items():
        if surface == rel:
            continue
        if surface == "ops/marketing/command_layer_integration_audit.md":
            continue
        if name in text or rel in text:
            refs.append(surface)
    return refs


def classify(path: Path, registry_text: str, surfaces: dict[str, str]) -> AuditRow:
    rel = path.relative_to(ROOT).as_posix()
    name = path.name
    registered = is_registered(name, rel, registry_text)
    refs = find_refs(name, rel, surfaces)
    action_ref = any(ref in ACTION_SURFACES for ref in refs)
    archive = is_archive_reference(path)

    if name in GENERATED_OR_CONTROLLED:
        return AuditRow(rel, "PASS_GENERATED", registered, len(refs), action_ref, refs, GENERATED_OR_CONTROLLED[name])

    if name in CORE_FILES:
        if registered:
            return AuditRow(rel, "PASS_CORE", registered, len(refs), action_ref, refs, "none")
        return AuditRow(rel, "RISK_CORE_UNREGISTERED", registered, len(refs), action_ref, refs, "add to ops/marketing/AGENTS.md Source Of Truth")

    if archive:
        if registered:
            return AuditRow(rel, "PASS_ARCHIVE_REFERENCE", registered, len(refs), action_ref, refs, "none")
        return AuditRow(rel, "RISK_ARCHIVE_UNREGISTERED", registered, len(refs), action_ref, refs, "register archive status in ops/marketing/AGENTS.md")

    if not registered and not refs:
        return AuditRow(rel, "RISK_ORPHAN", registered, 0, False, refs, "register it or delete/archive it")

    if not registered:
        return AuditRow(rel, "RISK_UNREGISTERED", registered, len(refs), action_ref, refs, "add to Source Of Truth or mark ARCHIVE_REFERENCE")

    if len(refs) < 2:
        return AuditRow(rel, "RISK_WEAKLY_LINKED", registered, len(refs), action_ref, refs, "link from action_queue/current_state/cockpit plus worklog or tracker")

    if not action_ref:
        return AuditRow(rel, "RISK_NO_ACTION_SURFACE", registered, len(refs), action_ref, refs, "link from action_queue/current_state/daily_scorecard/blocker_board/cockpit/tracker")

    return AuditRow(rel, "PASS_INTEGRATED", registered, len(refs), action_ref, refs, "none")


def build_report(rows: list[AuditRow]) -> str:
    risk_rows = [row for row in rows if row.status.startswith("RISK")]
    pass_rows = [row for row in rows if not row.status.startswith("RISK")]
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    out = [
        "# Marketing Command Layer Integration Audit",
        "",
        "Integration status: `GENERATED`",
        "",
        f"Last generated: {now}",
        "",
        "Purpose: identify command-layer files that risk becoming side documents nobody uses.",
        "",
        "## Summary",
        "",
        f"- Tracked files: `{len(rows)}`",
        f"- Integrated/generated/archive files: `{len(pass_rows)}`",
        f"- Side-document risks: `{len(risk_rows)}`",
        "",
        "A side-document risk means a file is missing from the source registry, has too few command-loop references, or is not connected to an action surface.",
        "",
        "## Required Rule",
        "",
        "No new `ops/marketing/` artifact counts as done unless it is either:",
        "",
        "- registered in `ops/marketing/AGENTS.md`,",
        "- linked from an action surface such as `action_queue.md`, `current_marketing_state.md`, `daily_scorecard.md`, `blocker_board.md`, `operator_cockpit.md`, or `ops/PROBLEM_TRACKER.md`,",
        "- logged in continuity files such as `ops/AGENT_WORKLOG.md`, `ops/AGENT_COORDINATION.md`, `decision_log.md`, `review_log.md`, `assumption_log.md`, or `memory_digest.md`,",
        "- or explicitly marked as `Integration status: ARCHIVE_REFERENCE` or `Integration status: GENERATED`.",
        "",
        "## File Results",
        "",
        "| File | Status | Registered | Ref count | Action surface | Fix |",
        "|---|---|---:|---:|---:|---|",
    ]

    for row in rows:
        out.append(
            f"| `{row.file}` | `{row.status}` | `{str(row.registered).lower()}` | `{row.ref_count}` | `{str(row.action_ref).lower()}` | {row.fix} |"
        )

    if risk_rows:
        out.extend(["", "## Risks To Fix", ""])
        for row in risk_rows:
            refs = ", ".join(f"`{ref}`" for ref in row.refs) if row.refs else "none"
            out.append(f"- `{row.file}`: `{row.status}`; refs: {refs}; fix: {row.fix}.")
    else:
        out.extend(["", "## Risks To Fix", "", "- None."])

    out.extend(
        [
            "",
            "## Command",
            "",
            "```bash",
            "python3.13 ops/scripts/audit_marketing_command_integration.py --write-report --fail-on-risk",
            "```",
            "",
        ]
    )
    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--fail-on-risk", action="store_true")
    args = parser.parse_args()

    registry_text = read_text(MARKETING_DIR / "AGENTS.md")
    surfaces: dict[str, str] = {}
    for rel in REFERENCE_SURFACES:
        path = ROOT / rel
        if path.exists():
            surfaces[rel] = read_text(path)

    files = [
        path
        for path in sorted(MARKETING_DIR.iterdir())
        if path.is_file() and path.suffix in TRACKED_SUFFIXES
    ]
    rows = [classify(path, registry_text, surfaces) for path in files]
    report = build_report(rows)

    print(report)
    if args.write_report:
        REPORT.write_text(report, encoding="utf-8")

    risk_count = sum(1 for row in rows if row.status.startswith("RISK"))
    if args.fail_on_risk and risk_count:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
