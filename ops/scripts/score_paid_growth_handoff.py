#!/usr/bin/env python3.13
"""Local scorecard for Dress Like Mommy paid-growth handoffs.

This script checks handoff text before it becomes the next agent's operating
state. It is intentionally local-only: it reads text files, writes an optional
report, and never calls Shopify, Google Ads, Pinterest, Merchant Center, or
other external systems.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

try:
    from compile_task_context import (
        DEFAULT_COORDINATION,
        DEFAULT_CURRENT_STATE,
        DEFAULT_PROBLEM_TRACKER,
        DEFAULT_WORKLOG,
        VALID_EVIDENCE_LABELS,
        VALID_TASK_KINDS,
        VALID_TASK_STAGES,
        compile_task_context,
    )
except ModuleNotFoundError:  # Support package-style imports from the repo root.
    from ops.scripts.compile_task_context import (
        DEFAULT_COORDINATION,
        DEFAULT_CURRENT_STATE,
        DEFAULT_PROBLEM_TRACKER,
        DEFAULT_WORKLOG,
        VALID_EVIDENCE_LABELS,
        VALID_TASK_KINDS,
        VALID_TASK_STAGES,
        compile_task_context,
    )


ROOT = Path(__file__).resolve().parents[2]
CANONICAL_PROMPT = "ops/prompts/paid-growth-ai-army-continuation-prompt.md"

NEXT_ACTION_RE = re.compile(
    r"(?im)^\s*(?:[-*]\s*)?(?:recommended next action|next best action)\s*:"
)
ANCHOR_RE = re.compile(r"AGENT_CONTINUITY_ANCHOR:\s*[A-Za-z0-9_.:-]+")
ANCHOR_ID_RE = re.compile(r"AGENT_CONTINUITY_ANCHOR:\s*([A-Za-z0-9_.:-]+)")
URL_RE = re.compile(r"https?://|www\.", re.IGNORECASE)
FIELD_RE = re.compile(
    r"(?im)^\s*(?:[-*]\s*)?`?(?P<key>[a-z][a-z0-9_]*)`?\s*(?::|=)\s*"
    r"`?(?P<value>[^`\n]+?)`?\s*$"
)
DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")

ACTION_TERMS = (
    "fix now",
    "execute approved bounded action",
    "prepare exact approval packet",
    "approval packet",
    "reroute",
    "hold with evidence",
    "paused-ready",
    "readback passed",
    "repair",
    "fixed",
)

APPROVAL_TERMS = (
    "fresh explicit action-time approval",
    "fresh approval",
    "exact approval",
    "approval phrase",
    "owner approval",
)

BLOCKED_SURFACE_TERMS = (
    "no live spend",
    "no campaign enablement",
    "no budget/bid/status",
    "no product-scope",
    "no feed-label",
    "no conversion-goal",
    "no merchant upload",
    "no shopify live product-data",
    "do not publish",
    "do not change status",
    "do not enable",
)

PHYSICAL_INVENTORY_CLAIMS = (
    "physical store",
    "retail location",
    "local pickup",
    "our warehouse",
    "warehouse stock",
    "on-hand stock",
    "stocked inventory",
)

PLACEHOLDER_VALUES = {
    "",
    "N/A",
    "NA",
    "PLACEHOLDER",
    "TBD",
    "TODO",
    "UNKNOWN",
}
NOT_APPLICABLE_VALUES = {"NOT_APPLICABLE", "NOT APPLICABLE"}
FALSE_OR_NOT_APPLICABLE_VALUES = {
    "FALSE",
    "NO",
    *NOT_APPLICABLE_VALUES,
}
TRUE_VALUES = {"TRUE", "YES"}
MATERIAL_VALUES = {"MATERIAL", *TRUE_VALUES}
NOT_MATERIAL_VALUES = {"NOT_MATERIAL", "NOT MATERIAL", "FALSE", "NO"}
INDEPENDENT_VERIFIER_VALUE = "DID_NOT_BUILD_OR_EXECUTE"
AUTHORITY_FIELDS = (
    "source_live_evidence_as_of",
    "live_state_mode",
    "effective_approval_policy",
    "approved_external_scope",
)
SEMANTIC_AUTHORITY_FIELDS = (
    "control_as_of",
    "source_live_evidence_as_of",
    "live_state_mode",
    "live_readback_fresh_until",
    "autonomous_action_ready",
    "effective_approval_policy",
    "approved_external_scope",
    "supersedes_execution_readiness_below",
)
UNCERTAINTY_BRANCH_FIELDS = (
    "decision_changing_evidence",
    "if_evidence_supports_recommendation",
    "if_evidence_opposes_recommendation",
)


@dataclass(frozen=True)
class CriterionResult:
    name: str
    passed: bool
    detail: str


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(errors="replace")


def has_term(text: str, terms: tuple[str, ...]) -> bool:
    lower = text.lower()
    return any(term in lower for term in terms)


def normalize_field_value(value: str | None) -> str:
    if value is None:
        return ""
    return " ".join(value.strip().strip("`").split()).upper()


def parse_fields(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for match in FIELD_RE.finditer(text):
        fields[match.group("key").lower()] = match.group("value").strip()
    return fields


def parse_field_occurrences(text: str) -> dict[str, list[str]]:
    fields: dict[str, list[str]] = {}
    for match in FIELD_RE.finditer(text):
        fields.setdefault(match.group("key").lower(), []).append(
            match.group("value").strip()
        )
    return fields


def has_substantive_value(fields: dict[str, str], key: str) -> bool:
    return normalize_field_value(fields.get(key)) not in PLACEHOLDER_VALUES


def score_authoritative_execution_context(fields: dict[str, str]) -> CriterionResult:
    authority_context = normalize_field_value(fields.get("authority_context"))
    if authority_context in NOT_APPLICABLE_VALUES:
        return CriterionResult(
            "authoritative_execution_context",
            True,
            "authority context is explicitly NOT_APPLICABLE",
        )

    missing = [key for key in AUTHORITY_FIELDS if not has_substantive_value(fields, key)]
    evidence_date = normalize_field_value(fields.get("source_live_evidence_as_of"))
    valid_date = bool(DATE_RE.fullmatch(evidence_date))
    passed = not missing and valid_date
    if passed:
        detail = "names evidence date, execution mode, effective authority, and approved external scope"
    else:
        problems = []
        if missing:
            problems.append("missing or placeholder: " + ", ".join(missing))
        if not valid_date:
            problems.append("source_live_evidence_as_of must be YYYY-MM-DD")
        detail = "; ".join(problems)
    return CriterionResult("authoritative_execution_context", passed, detail)


def score_uncertainty_outcome_branches(fields: dict[str, str]) -> CriterionResult:
    depends_on_uncertainty = normalize_field_value(
        fields.get("decision_depends_on_uncertain_state")
    )
    if depends_on_uncertainty in FALSE_OR_NOT_APPLICABLE_VALUES:
        return CriterionResult(
            "uncertainty_outcome_branches",
            True,
            "decision explicitly does not depend on uncertain state",
        )
    if depends_on_uncertainty not in TRUE_VALUES:
        return CriterionResult(
            "uncertainty_outcome_branches",
            False,
            "decision_depends_on_uncertain_state must be true, false, or NOT_APPLICABLE",
        )

    missing = [key for key in UNCERTAINTY_BRANCH_FIELDS if not has_substantive_value(fields, key)]
    supports = normalize_field_value(fields.get("if_evidence_supports_recommendation"))
    opposes = normalize_field_value(fields.get("if_evidence_opposes_recommendation"))
    branches_differ = bool(supports and opposes and supports != opposes)
    passed = not missing and branches_differ
    if passed:
        detail = "names decision-changing evidence and distinct actions for both outcomes"
    else:
        problems = []
        if missing:
            problems.append("missing or placeholder: " + ", ".join(missing))
        if not branches_differ:
            problems.append("supporting and opposing evidence branches must name distinct actions")
        detail = "; ".join(problems)
    return CriterionResult("uncertainty_outcome_branches", passed, detail)


def score_independent_material_decision_verifier(
    fields: dict[str, str],
) -> CriterionResult:
    material_decision = normalize_field_value(fields.get("material_decision"))
    if material_decision in NOT_MATERIAL_VALUES:
        return CriterionResult(
            "independent_material_decision_verifier",
            True,
            "decision is explicitly NOT_MATERIAL",
        )
    if material_decision not in MATERIAL_VALUES:
        return CriterionResult(
            "independent_material_decision_verifier",
            False,
            "material_decision must be MATERIAL or NOT_MATERIAL",
        )

    verifier = normalize_field_value(fields.get("independent_verifier"))
    independence = normalize_field_value(fields.get("verifier_independence"))
    named_verifier = verifier not in PLACEHOLDER_VALUES | {"NONE", "SELF"}
    passed = named_verifier and independence == INDEPENDENT_VERIFIER_VALUE
    detail = (
        "names a verifier who did not build or execute the material action"
        if passed
        else "material decision needs a named independent_verifier and verifier_independence=DID_NOT_BUILD_OR_EXECUTE"
    )
    return CriterionResult("independent_material_decision_verifier", passed, detail)


def has_unapproved_url(text: str) -> bool:
    for match in URL_RE.finditer(text):
        start = max(0, match.start() - 80)
        end = min(len(text), match.end() + 160)
        context = text[start:end].lower()
        if "dresslikemommy.com" in context or "admin.shopify.com" in context:
            continue
        return True
    return False


def has_positive_inventory_claim(text: str) -> bool:
    lower = text.lower()
    for term in PHYSICAL_INVENTORY_CLAIMS:
        start = 0
        while True:
            idx = lower.find(term, start)
            if idx == -1:
                break
            prefix = lower[max(0, idx - 32) : idx]
            if not any(marker in prefix for marker in ("no ", "not ", "never ", "do not ", "without ")):
                return True
            start = idx + len(term)
    return False


def score_text(text: str) -> list[CriterionResult]:
    lower = text.lower()
    fields = parse_fields(text)
    next_actions = NEXT_ACTION_RE.findall(text)
    has_monitor = "monitor" in lower or "monitoring" in lower
    has_action = has_term(text, ACTION_TERMS)

    return [
        CriterionResult(
            "latest_anchor_named",
            bool(ANCHOR_RE.search(text)),
            "names an AGENT_CONTINUITY_ANCHOR" if ANCHOR_RE.search(text) else "missing AGENT_CONTINUITY_ANCHOR",
        ),
        CriterionResult(
            "one_next_action",
            len(next_actions) == 1,
            f"found {len(next_actions)} next-action label(s)",
        ),
        CriterionResult(
            "canonical_prompt_reused",
            CANONICAL_PROMPT in text,
            f"mentions {CANONICAL_PROMPT}" if CANONICAL_PROMPT in text else "missing canonical prompt path",
        ),
        CriterionResult(
            "approval_boundary_preserved",
            has_term(text, APPROVAL_TERMS) and has_term(text, BLOCKED_SURFACE_TERMS),
            "approval language and blocked live surfaces are present"
            if has_term(text, APPROVAL_TERMS) and has_term(text, BLOCKED_SURFACE_TERMS)
            else "missing approval language or blocked live-surface reminder",
        ),
        CriterionResult(
            "sales_moving_outcome",
            has_action,
            "handoff names an action, approval packet, repair, reroute, or evidence-backed hold"
            if has_action
            else "handoff reads like monitoring or summary without an action",
        ),
        CriterionResult(
            "blocker_or_gate_named",
            ("blocker" in lower or "gate" in lower or "approval" in lower) and "next" in lower,
            "names a blocker/gate/approval and a next step"
            if ("blocker" in lower or "gate" in lower or "approval" in lower) and "next" in lower
            else "missing concrete blocker/gate plus next step",
        ),
        CriterionResult(
            "not_monitor_only",
            not (has_monitor and not has_action),
            "monitoring is tied to action" if not (has_monitor and not has_action) else "monitoring appears as the deliverable",
        ),
        CriterionResult(
            "no_source_or_supplier_url",
            not has_unapproved_url(text),
            "no non-Dress-Like-Mommy URL-like source found"
            if not has_unapproved_url(text)
            else "contains a non-Dress-Like-Mommy URL-like string",
        ),
        CriterionResult(
            "no_physical_inventory_claim",
            not has_positive_inventory_claim(text),
            "no positive physical-store, warehouse, local-pickup, or on-hand-stock claim"
            if not has_positive_inventory_claim(text)
            else "contains a positive physical-store, warehouse, local-pickup, or on-hand-stock claim",
        ),
        score_authoritative_execution_context(fields),
        score_uncertainty_outcome_branches(fields),
        score_independent_material_decision_verifier(fields),
    ]


def semantic_score_text(
    text: str, task_context: dict[str, object]
) -> list[CriterionResult]:
    """Score semantic consistency against a compiled canonical task context."""

    diagnostics = task_context.get("diagnostics", {})
    context_ready = (
        isinstance(diagnostics, dict) and diagnostics.get("status") == "OK"
    )
    occurrences = parse_field_occurrences(text)
    task_kind = str(task_context.get("task_kind", "paid-growth"))

    selected = task_context.get("selected_anchor")
    selected_anchor_id = (
        selected.get("anchor_id") if isinstance(selected, dict) else None
    )
    named_anchors = ANCHOR_ID_RE.findall(text)
    anchor_passed = (
        context_ready
        and isinstance(selected_anchor_id, str)
        and len(named_anchors) == 1
        and named_anchors[0].casefold() == selected_anchor_id.casefold()
    )
    anchor_detail = (
        f"names the unique retrieved anchor {selected_anchor_id}"
        if anchor_passed
        else "handoff must name exactly the unique task-relevant compiled anchor"
    )

    authority = task_context.get("authority", {})
    authority_fields = authority.get("fields", {}) if isinstance(authority, dict) else {}
    authority_problems: list[str] = []
    if not context_ready or not isinstance(authority_fields, dict):
        authority_problems.append("compiled context is fail-closed")
    elif task_kind == "local":
        values = occurrences.get("authority_context", [])
        if len(values) != 1 or normalize_field_value(values[0]) not in NOT_APPLICABLE_VALUES:
            authority_problems.append(
                "local semantic context requires authority_context=NOT_APPLICABLE exactly once"
            )
    else:
        for key in SEMANTIC_AUTHORITY_FIELDS:
            values = occurrences.get(key, [])
            expected = authority_fields.get(key)
            if len(values) != 1:
                authority_problems.append(f"{key} occurs {len(values)} time(s)")
            elif normalize_field_value(values[0]) != normalize_field_value(
                str(expected) if expected is not None else None
            ):
                authority_problems.append(f"{key} differs from current control")
    authority_passed = not authority_problems

    next_action = task_context.get("next_action", {})
    expected_next_action = (
        next_action.get("id") if isinstance(next_action, dict) else None
    )
    next_action_values = occurrences.get("next_best_action", [])
    if task_kind == "local" and expected_next_action is None:
        next_action_passed = context_ready and not next_action_values
    else:
        next_action_passed = (
            context_ready
            and isinstance(expected_next_action, str)
            and len(next_action_values) == 1
            and normalize_field_value(next_action_values[0])
            == normalize_field_value(expected_next_action)
        )

    expected_evidence_grade = (
        authority.get("evidence_grade") if isinstance(authority, dict) else None
    )
    evidence_values = occurrences.get("evidence_grade", [])
    normalized_evidence = (
        normalize_field_value(evidence_values[0]) if len(evidence_values) == 1 else ""
    )
    evidence_passed = (
        context_ready
        and len(evidence_values) == 1
        and normalized_evidence in VALID_EVIDENCE_LABELS
        and normalized_evidence == normalize_field_value(
            str(expected_evidence_grade) if expected_evidence_grade is not None else None
        )
    )

    expected_task_stage = normalize_field_value(str(task_context.get("task_stage", "")))
    task_stage_values = occurrences.get("task_stage", [])
    normalized_task_stage = (
        normalize_field_value(task_stage_values[0])
        if len(task_stage_values) == 1
        else ""
    )
    task_stage_passed = (
        context_ready
        and len(task_stage_values) == 1
        and normalized_task_stage in VALID_TASK_STAGES
        and normalized_task_stage != "UNKNOWN"
        and expected_task_stage != "UNKNOWN"
        and normalized_task_stage == expected_task_stage
    )

    return [
        CriterionResult(
            "semantically_relevant_anchor",
            anchor_passed,
            anchor_detail,
        ),
        CriterionResult(
            "authority_matches_current_control",
            authority_passed,
            "all current authority fields occur once and match exactly"
            if authority_passed
            else "; ".join(authority_problems),
        ),
        CriterionResult(
            "next_action_matches_current_control",
            next_action_passed,
            f"next_best_action matches {expected_next_action}"
            if next_action_passed
            else "next_best_action must occur once and match current control",
        ),
        CriterionResult(
            "evidence_grade_matches_current_control",
            evidence_passed,
            f"evidence_grade matches {expected_evidence_grade}"
            if evidence_passed
            else "evidence_grade must be a canonical label matching current control",
        ),
        CriterionResult(
            "task_stage_matches_retrieved_anchor",
            task_stage_passed,
            f"task_stage matches {expected_task_stage}"
            if task_stage_passed
            else "task_stage must occur once, be non-UNKNOWN, and match the retrieved anchor",
        ),
    ]


def score_file(
    path: Path, task_context: dict[str, object] | None = None
) -> dict[str, object]:
    text = read_text(path)
    criteria = score_text(text)
    if task_context is not None:
        criteria.extend(semantic_score_text(text, task_context))
    passed_count = sum(1 for item in criteria if item.passed)
    failed = [item for item in criteria if not item.passed]
    return {
        "path": path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else path.as_posix(),
        "passed": not failed,
        "score": passed_count,
        "max_score": len(criteria),
        "criteria": [item.__dict__ for item in criteria],
        "failed": [item.name for item in failed],
    }


def build_report(results: list[dict[str, object]]) -> str:
    total_files = len(results)
    passed_files = sum(1 for result in results if result["passed"])
    lines = [
        "# Paid-Growth Handoff Scorecard",
        "",
        "Integration status: `GENERATED`",
        "",
        "Purpose: local-only scorecard for paid-growth continuation handoffs. It does not perform external writes.",
        "",
        "## Summary",
        "",
        f"- Files checked: `{total_files}`",
        f"- Files passing: `{passed_files}`",
        f"- Files failing: `{total_files - passed_files}`",
        "",
        "## Results",
        "",
    ]

    for result in results:
        lines.extend(
            [
                f"### `{result['path']}`",
                "",
                f"- Score: `{result['score']}/{result['max_score']}`",
                f"- Passed: `{str(result['passed']).lower()}`",
                "",
                "| Criterion | Pass | Detail |",
                "|---|---:|---|",
            ]
        )
        for criterion in result["criteria"]:  # type: ignore[index]
            lines.append(
                f"| `{criterion['name']}` | `{str(criterion['passed']).lower()}` | {criterion['detail']} |"
            )
        lines.append("")

    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", help="Markdown/text handoff files to score")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of a Markdown report")
    parser.add_argument("--write-report", type=Path, help="Write a Markdown report to this path")
    parser.add_argument("--fail-on-issues", action="store_true", help="Exit 1 if any file fails")
    parser.add_argument(
        "--task-query",
        help="Enable semantic checks using a retrieval-first compiled task context",
    )
    parser.add_argument(
        "--task-kind",
        choices=sorted(VALID_TASK_KINDS),
        default="paid-growth",
        help="Semantic context authority type",
    )
    parser.add_argument(
        "--task-entity",
        action="append",
        default=[],
        help="Exact task entity for semantic anchor retrieval; repeatable",
    )
    parser.add_argument("--task-worklog", type=Path, default=DEFAULT_WORKLOG)
    parser.add_argument("--task-current-state", type=Path, default=DEFAULT_CURRENT_STATE)
    parser.add_argument("--task-problem-tracker", type=Path, default=DEFAULT_PROBLEM_TRACKER)
    parser.add_argument("--task-coordination", type=Path, default=DEFAULT_COORDINATION)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    paths = [Path(path).expanduser() for path in args.paths]
    missing = [path.as_posix() for path in paths if not path.exists()]
    if missing:
        sys.stderr.write("Missing handoff file(s): " + ", ".join(missing) + "\n")
        return 2

    task_context = None
    if args.task_query:
        context_paths = (
            (args.task_worklog, args.task_current_state)
            if args.task_kind == "paid-growth"
            else (args.task_worklog,)
        )
        missing_context = [path.as_posix() for path in context_paths if not path.exists()]
        if missing_context:
            sys.stderr.write(
                "Missing task-context file(s): " + ", ".join(missing_context) + "\n"
            )
            return 2
        task_context = compile_task_context(
            args.task_query,
            explicit_entities=args.task_entity,
            worklog_path=args.task_worklog,
            current_state_path=args.task_current_state,
            problem_tracker_path=args.task_problem_tracker,
            coordination_path=args.task_coordination,
            task_kind=args.task_kind,
        )

    results = [score_file(path.resolve(), task_context) for path in paths]
    payload = {
        "files_checked": len(results),
        "files_passing": sum(1 for result in results if result["passed"]),
        "files_failing": sum(1 for result in results if not result["passed"]),
        "results": results,
    }
    if task_context is not None:
        payload["task_context"] = task_context

    if args.write_report:
        args.write_report.parent.mkdir(parents=True, exist_ok=True)
        args.write_report.write_text(build_report(results), encoding="utf-8")

    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(build_report(results))

    if args.fail_on_issues and payload["files_failing"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
