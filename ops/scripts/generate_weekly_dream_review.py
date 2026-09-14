#!/usr/bin/env python3.13
"""Generate a local weekly dream review for Dress Like Mommy.

The report consolidates recent repo memory into a short review packet. It is
local-only: it reads files in this repository, writes an optional Markdown
report, and never calls Shopify, Google Ads, Pinterest, Merchant Center, GA4,
GTM, or any external account.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
INDEPENDENT_EVENT_THRESHOLD = 2
FAIL_CLOSED_NEXT_ACTION = (
    "AUTHORITATIVE_NEXT_ACTION_UNAVAILABLE__READ_ONLY_RECONCILIATION_REQUIRED"
)


@dataclass(frozen=True)
class SourceSpec:
    path: str
    role: str
    precedence: int
    signal_eligible: bool


DEFAULT_SOURCE_SPECS = (
    SourceSpec("ops/marketing/current_marketing_state.md", "AUTHORITY", 100, False),
    SourceSpec("ops/marketing/action_queue.md", "CURRENT_STATUS", 90, False),
    SourceSpec("ops/PROBLEM_TRACKER.md", "CURRENT_STATUS", 80, False),
    SourceSpec("ops/marketing/decision_log.md", "OUTCOME_LOG", 70, False),
    SourceSpec("ops/AGENT_WORKLOG.md", "EVENT_LOG", 60, True),
    SourceSpec("ops/AGENT_COORDINATION.md", "OWNERSHIP", 50, False),
    SourceSpec("ops/marketing/memory_digest.md", "CONTEXT", 40, False),
    SourceSpec("ops/marketing/dream_consolidation_prompt.md", "CONTEXT", 30, False),
    SourceSpec("ops/prompts/paid-growth-ai-army-continuation-prompt.md", "CONTEXT", 20, False),
    SourceSpec("docs/agent-loops/self-improvement-pilot-loop.md", "CONTEXT", 10, False),
    SourceSpec("docs/agent-loops/localized-pdp-quality-loop.md", "CONTEXT", 10, False),
)
DEFAULT_SOURCES = tuple(spec.path for spec in DEFAULT_SOURCE_SPECS)

ANCHOR_RE = re.compile(r"AGENT_CONTINUITY_ANCHOR:\s*([A-Za-z0-9_.:-]+)")
ANCHOR_LINE_RE = re.compile(
    r"^\s*AGENT_CONTINUITY_ANCHOR:\s*([A-Za-z0-9_.:-]+)\s*$"
)
TOP_LEVEL_HEADING_RE = re.compile(r"^##\s+(.+?)\s*$")
CONTROL_BLOCK_RE = re.compile(
    r"<!-- MARKETING_AUTHORITATIVE_CONTROL:START -->(.*?)"
    r"<!-- MARKETING_AUTHORITATIVE_CONTROL:END -->",
    flags=re.DOTALL,
)
CONTROL_FIELD_RE = re.compile(r"^\s*-\s*`([a-z0-9_]+)`:\s*`([^`]*)`\s*$")
CANONICAL_ACTION_RE = re.compile(r"[A-Z][A-Z0-9_:-]*")
REQUIRED_CONTROL_FIELDS = {
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

OBSERVED_SECTION_NAMES = {
    "summary",
    "outcome",
    "outcomes",
    "result",
    "results",
    "readback",
    "readbacks",
    "verification",
    "failures",
    "root cause",
    "problem tracking",
    "residual risks",
}


@dataclass(frozen=True)
class SourceReadback:
    path: str
    exists: bool
    total_lines: int
    included_lines: int
    anchor_count: int
    text: str
    role: str = "CONTEXT"
    precedence: int = 0
    signal_eligible: bool = False
    start_line: int = 1


@dataclass(frozen=True)
class ReviewEvent:
    event_id: str
    title: str
    source_path: str
    anchor_line: int
    outcome_lines: tuple[tuple[int, str], ...]


@dataclass(frozen=True)
class SignalDefinition:
    key: str
    label: str
    patterns: tuple[str, ...]
    meaning: str
    proposed_rule: str


@dataclass(frozen=True)
class SignalResult:
    key: str
    label: str
    count: int
    meaning: str
    proposed_rule: str
    event_count: int
    mention_count: int
    qualifies: bool
    exemplars: tuple[str, ...]


SIGNALS = (
    SignalDefinition(
        "monitor_only_drift",
        "Monitoring can become the deliverable",
        (
            r"circular monitor",
            r"monitor loops?",
            r"monitoring is not progress",
            r"monitoring as the deliverable",
            r"monitor/readback cycles as the deliverable",
        ),
        "Agents keep needing reminders that watching numbers is not progress unless it creates a decision, fix, approval packet, reroute, or evidence-backed hold.",
        "Keep handoffs tied to one action outcome: fix now, bounded approved action, exact approval packet, reroute, or hold with evidence.",
    ),
    SignalDefinition(
        "one_next_action",
        "Next action discipline matters",
        (
            r"one best next action",
            r"single recommended next action",
            r"several possible next steps",
            r"competing prompts?",
            r"vague next",
        ),
        "The repo repeatedly values one owner-ready next action over option lists.",
        "Every dream review and paid-growth handoff should name exactly one recommended next action.",
    ),
    SignalDefinition(
        "approval_boundaries",
        "Live-risk approvals stay explicit",
        (
            r"fresh explicit",
            r"exact approval",
            r"approval phrase",
            r"approval-gated",
            r"no live spend",
            r"no .*budget/bid/status",
        ),
        "The useful memory is only safe if it preserves the line between local prep and live writes.",
        "Treat all dream-review output as local advisory evidence unless the owner gives fresh action-time approval.",
    ),
    SignalDefinition(
        "source_inventory_safety",
        "Source and inventory claims need guards",
        (
            r"source leak",
            r"supplier/source",
            r"vendor/source",
            r"physical store",
            r"owned physical inventory",
            r"local inventory",
            r"warehouse",
            r"on-hand stock",
        ),
        "Listing, feed, and ad work can hurt trust if source details or false inventory claims leak.",
        "Before paid traffic or publication, keep source-leak and dropshipping-honesty checks in the owning loop.",
    ),
    SignalDefinition(
        "localization_quality",
        "Localized PDP quality is a repeatable gate",
        (
            r"localized PDP",
            r"translation",
            r"English leakage",
            r"review-widget",
            r"language-smoke",
            r"raw translation",
        ),
        "International growth depends on pages that look native enough for shoppers, not just translated enough for an API check.",
        "Run the localized PDP quality loop before treating translated products as ready for paid traffic.",
    ),
    SignalDefinition(
        "feed_grouping",
        "Feed grouping cannot regress",
        (
            r"item_group_id",
            r"feed grouping",
            r"Pinterest feed",
            r"parent featured image",
            r"same-parent variants",
        ),
        "Pinterest and catalog work has a hard parent/variant grouping rule.",
        "Keep the grouping guard wired into continuity and do not approve per-variant feeds without parent grouping.",
    ),
    SignalDefinition(
        "self_improvement_ready",
        "A local scorecard already exists",
        (
            r"self-improvement pilot",
            r"score_paid_growth_handoff",
            r"scorecard",
            r"prompt improvement",
            r"handoff quality",
        ),
        "The project already has a small local scorecard; the next step is regular use, not a new command layer.",
        "Use the handoff scorecard before changing the canonical paid-growth prompt or closing risky handoffs.",
    ),
)


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def resolve_path(path: str | Path) -> Path:
    candidate = Path(path).expanduser()
    if candidate.is_absolute():
        return candidate
    return ROOT / candidate


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(errors="replace")


def source_spec_for_path(path: str | Path) -> SourceSpec:
    resolved = resolve_path(path)
    relative = rel(resolved)
    for spec in DEFAULT_SOURCE_SPECS:
        if relative == spec.path:
            return spec
    return SourceSpec(relative, "CONTEXT", 0, False)


def read_source(
    path: Path,
    tail_lines: int,
    spec: SourceSpec | None = None,
) -> SourceReadback:
    selected_spec = spec or source_spec_for_path(path)
    if not path.exists():
        return SourceReadback(
            rel(path),
            False,
            0,
            0,
            0,
            "",
            selected_spec.role,
            selected_spec.precedence,
            selected_spec.signal_eligible,
            1,
        )

    text = read_text(path)
    lines = text.splitlines()
    included = lines
    start_line = 1
    if path.name == "AGENT_WORKLOG.md" and tail_lines > 0 and len(lines) > tail_lines:
        start_index = len(lines) - tail_lines
        while start_index > 0 and not TOP_LEVEL_HEADING_RE.fullmatch(
            lines[start_index].strip()
        ):
            start_index -= 1
        included = lines[start_index:]
        start_line = start_index + 1
    included_text = "\n".join(included)
    return SourceReadback(
        path=rel(path),
        exists=True,
        total_lines=len(lines),
        included_lines=len(included),
        anchor_count=len(ANCHOR_RE.findall(text)),
        text=included_text,
        role=selected_spec.role,
        precedence=selected_spec.precedence,
        signal_eligible=selected_spec.signal_eligible,
        start_line=start_line,
    )


def latest_anchors(worklog_text: str, limit: int) -> list[str]:
    anchors = ANCHOR_RE.findall(worklog_text)
    if limit <= 0:
        return anchors

    seen: set[str] = set()
    recent_unique: list[str] = []
    for anchor in reversed(anchors):
        if anchor in seen:
            continue
        seen.add(anchor)
        recent_unique.append(anchor)
        if len(recent_unique) == limit:
            break
    return list(reversed(recent_unique))


def _section_name(line: str) -> str | None:
    stripped = line.strip()
    if not stripped:
        return None
    heading = re.fullmatch(r"#{2,6}\s+(.+?)\s*", stripped)
    if heading:
        name = heading.group(1).rstrip(":").strip().lower()
    elif stripped.endswith(":") and not stripped.startswith(("-", "*")):
        name = stripped[:-1].strip().lower()
    else:
        return None
    if len(name) > 60:
        return None
    return name


def extract_review_events(source: SourceReadback) -> list[ReviewEvent]:
    """Extract newest independent continuity events and observed-result lines.

    Exact anchor IDs are deduplicated first. A second content fingerprint keeps
    a copied observed-result block from becoming a second event merely because
    its anchor was renamed.
    """

    if not source.exists or not source.signal_eligible or source.role != "EVENT_LOG":
        return []

    lines = source.text.splitlines()
    anchor_positions: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = ANCHOR_LINE_RE.fullmatch(line)
        if match:
            anchor_positions.append((index, match.group(1)))

    candidates: list[ReviewEvent] = []
    for position, (anchor_index, event_id) in enumerate(anchor_positions):
        end_index = (
            anchor_positions[position + 1][0]
            if position + 1 < len(anchor_positions)
            else len(lines)
        )
        title = event_id
        for prior_index in range(anchor_index - 1, -1, -1):
            heading = TOP_LEVEL_HEADING_RE.fullmatch(lines[prior_index].strip())
            if heading:
                title = heading.group(1).strip()
                break

        active_observed_section = False
        outcome_lines: list[tuple[int, str]] = []
        for line_index in range(anchor_index + 1, end_index):
            line = lines[line_index]
            section_name = _section_name(line)
            if section_name is not None:
                active_observed_section = section_name in OBSERVED_SECTION_NAMES
                continue
            if active_observed_section and line.strip() and line.strip() != "---":
                outcome_lines.append((source.start_line + line_index, line.strip()))

        candidates.append(
            ReviewEvent(
                event_id=event_id,
                title=title,
                source_path=source.path,
                anchor_line=source.start_line + anchor_index,
                outcome_lines=tuple(outcome_lines),
            )
        )

    newest_by_id: dict[str, ReviewEvent] = {}
    for event in reversed(candidates):
        newest_by_id.setdefault(event.event_id, event)
    id_deduplicated = [
        event for event in candidates if newest_by_id.get(event.event_id) is event
    ]

    def outcome_fingerprint(event: ReviewEvent) -> str:
        return "\n".join(
            " ".join(line.casefold().split()) for _, line in event.outcome_lines
        )

    newest_by_outcome: dict[str, ReviewEvent] = {}
    for event in reversed(id_deduplicated):
        fingerprint = outcome_fingerprint(event)
        if fingerprint:
            newest_by_outcome.setdefault(fingerprint, event)
    return [
        event
        for event in id_deduplicated
        if not outcome_fingerprint(event)
        or newest_by_outcome.get(outcome_fingerprint(event)) is event
    ]


def count_pattern(text: str, pattern: str) -> int:
    return len(re.findall(pattern, text, flags=re.IGNORECASE))


def score_events(events: list[ReviewEvent]) -> list[SignalResult]:
    results: list[SignalResult] = []
    for signal in SIGNALS:
        event_count = 0
        mention_count = 0
        exemplars: list[str] = []
        for event in events:
            event_mentions = 0
            first_match: tuple[int, str] | None = None
            for line_number, line in event.outcome_lines:
                line_mentions = sum(
                    count_pattern(line, pattern) for pattern in signal.patterns
                )
                if line_mentions and first_match is None:
                    first_match = (line_number, line)
                event_mentions += line_mentions
            if event_mentions:
                event_count += 1
                mention_count += event_mentions
                if first_match and len(exemplars) < 2:
                    safe_line = re.sub(
                        r"https?://\S+", "[URL_REDACTED]", first_match[1]
                    )
                    safe_line = safe_line.replace("|", "\\|").replace("`", "'")
                    if len(safe_line) > 240:
                        safe_line = safe_line[:237].rstrip() + "..."
                    exemplars.append(
                        f"{event.source_path}:{first_match[0]} "
                        f"[{event.event_id}] {safe_line}"
                    )
        results.append(
            SignalResult(
                key=signal.key,
                label=signal.label,
                count=event_count,
                meaning=signal.meaning,
                proposed_rule=signal.proposed_rule,
                event_count=event_count,
                mention_count=mention_count,
                qualifies=event_count >= INDEPENDENT_EVENT_THRESHOLD,
                exemplars=tuple(exemplars),
            )
        )
    return results


def score_signals(text: str) -> list[SignalResult]:
    """Compatibility wrapper that treats the supplied text as an event log."""

    lines = text.splitlines()
    source = SourceReadback(
        path="<memory>",
        exists=True,
        total_lines=len(lines),
        included_lines=len(lines),
        anchor_count=len(ANCHOR_RE.findall(text)),
        text=text,
        role="EVENT_LOG",
        precedence=0,
        signal_eligible=True,
    )
    events = extract_review_events(source)
    if not events and text.strip():
        events = [
            ReviewEvent(
                event_id="legacy-input",
                title="Legacy input",
                source_path=source.path,
                anchor_line=1,
                outcome_lines=tuple(
                    (line_number, line.strip())
                    for line_number, line in enumerate(lines, start=1)
                    if line.strip()
                ),
            )
        ]
    return score_events(events)


def parse_authoritative_control(
    text: str,
    source_path: str = "ops/marketing/current_marketing_state.md",
) -> dict[str, object]:
    blocks = CONTROL_BLOCK_RE.findall(text)
    diagnostics: list[str] = []
    if len(blocks) != 1:
        diagnostics.append(f"expected_one_control_block_found_{len(blocks)}")
        return {
            "valid": False,
            "source": source_path,
            "next_best_action": FAIL_CLOSED_NEXT_ACTION,
            "fields": {},
            "diagnostics": diagnostics,
        }

    fields: dict[str, str] = {}
    duplicate_fields: set[str] = set()
    for line in blocks[0].splitlines():
        match = CONTROL_FIELD_RE.fullmatch(line)
        if not match:
            continue
        key, value = match.groups()
        if key in fields:
            duplicate_fields.add(key)
        fields[key] = value.strip()

    if duplicate_fields:
        diagnostics.append(
            "duplicate_fields:" + ",".join(sorted(duplicate_fields))
        )
    missing_fields = sorted(REQUIRED_CONTROL_FIELDS - fields.keys())
    if missing_fields:
        diagnostics.append("missing_fields:" + ",".join(missing_fields))
    next_best_action = fields.get("next_best_action", "")
    if not CANONICAL_ACTION_RE.fullmatch(next_best_action):
        diagnostics.append("missing_or_invalid_next_best_action")
    if fields.get("autonomous_action_ready") not in {"true", "false"}:
        diagnostics.append("invalid_autonomous_action_ready")
    if fields.get("supersedes_execution_readiness_below") not in {"true", "false"}:
        diagnostics.append("invalid_supersedes_execution_readiness_below")

    valid = not diagnostics
    return {
        "valid": valid,
        "source": source_path,
        "next_best_action": next_best_action if valid else FAIL_CLOSED_NEXT_ACTION,
        "fields": fields,
        "diagnostics": diagnostics,
    }


def choose_next_action(
    text: str,
    signals: list[SignalResult],
    authoritative_control: dict[str, object] | None = None,
) -> str:
    if authoritative_control is not None:
        action = str(
            authoritative_control.get("next_best_action", FAIL_CLOSED_NEXT_ACTION)
        )
        if authoritative_control.get("valid") is True:
            return f"Execute the authoritative repo-local next action: `{action}`."
        return f"Fail closed: `{FAIL_CLOSED_NEXT_ACTION}`."

    # Compatibility fallback for direct callers. The CLI always supplies the
    # authoritative control and therefore never lets historical keyword volume
    # override current command-layer authority.
    lower = text.lower()
    if "review-widget" in lower or "localized pdp" in lower:
        return (
            "Resolve the localized PDP review-widget policy first: either repair "
            "the app-controlled server strings with fresh approval or classify raw "
            "widget markup separately while keeping browser-visible text as the "
            "shopper gate."
        )
    if any(
        signal.key == "self_improvement_ready" and signal.qualifies
        for signal in signals
    ):
        return (
            "Run the paid-growth handoff scorecard before the next risky handoff or "
            "canonical prompt change, then keep only one small improvement if the "
            "same examples improve."
        )
    return (
        "Generate this weekly review before the next paid-growth closeout, then "
        "follow the current command layer's single best next action."
    )


def default_report_path(as_of: str) -> Path:
    return (
        ROOT
        / "dresslikemommy-growth-2026"
        / "02_AUDIT_PACKETS"
        / f"{as_of}-weekly-dream-review"
        / "WEEKLY_DREAM_REVIEW.md"
    )


def build_payload(
    *,
    as_of: str,
    sources: list[SourceReadback],
    anchors: list[str],
    signals: list[SignalResult],
    next_action: str,
    events: list[ReviewEvent] | None = None,
    authority: dict[str, object] | None = None,
) -> dict[str, object]:
    return {
        "as_of": as_of,
        "sources": [
            {
                "path": source.path,
                "exists": source.exists,
                "total_lines": source.total_lines,
                "included_lines": source.included_lines,
                "anchor_count": source.anchor_count,
                "role": source.role,
                "precedence": source.precedence,
                "signal_eligible": source.signal_eligible,
            }
            for source in sources
        ],
        "latest_anchors": anchors,
        "signals": [asdict(signal) for signal in signals],
        "recommended_next_action": next_action,
        "local_only": True,
        "external_writes": False,
        "review_events": [asdict(event) for event in (events or [])],
        "signal_provenance": {
            "independent_event_threshold": INDEPENDENT_EVENT_THRESHOLD,
            "event_deduplication": [
                "newest_exact_anchor_id",
                "newest_normalized_observed_result_fingerprint",
            ],
            "eligible_source_roles": ["EVENT_LOG"],
            "observed_sections": sorted(OBSERVED_SECTION_NAMES),
        },
        "authoritative_control": authority or {},
    }


def build_report(payload: dict[str, object]) -> str:
    sources = payload["sources"]  # type: ignore[assignment]
    anchors = payload["latest_anchors"]  # type: ignore[assignment]
    signals = payload["signals"]  # type: ignore[assignment]
    review_events = payload.get("review_events", [])  # type: ignore[assignment]
    authority = payload.get("authoritative_control", {})  # type: ignore[assignment]
    active_signals = [signal for signal in signals if signal["qualifies"]]  # type: ignore[index]

    lines = [
        "# Weekly Dream Review",
        "",
        "Integration status: `GENERATED`",
        "",
        f"As of: `{payload['as_of']}`",
        "",
        "Purpose: local-only consolidation of observed cross-session outcomes. This report does not authorize live writes.",
        "",
        "## Safety Boundary",
        "",
        "- Read local files only.",
        "- No Shopify Admin, Google Ads, Pinterest, Merchant Center, GA4/GTM, feed, campaign, product, theme, billing, credential, payment, order, or publication writes.",
        "- Suggested prompt or checklist changes require human review before promotion.",
        "",
        "## Sources Read",
        "",
        "| Source | Role | Precedence | Signal eligible | Exists | Lines read | Anchors in file |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for source in sources:  # type: ignore[assignment]
        lines.append(
            f"| `{source['path']}` | `{source['role']}` | `{source['precedence']}` | "
            f"`{str(source['signal_eligible']).lower()}` | `{str(source['exists']).lower()}` | "
            f"`{source['included_lines']}/{source['total_lines']}` | `{source['anchor_count']}` |"
        )

    lines.extend(["", "## Authoritative Action", ""])
    if authority.get("valid") is True:  # type: ignore[union-attr]
        lines.append(
            f"- Current `next_best_action`: `{authority['next_best_action']}` from `{authority['source']}`."  # type: ignore[index]
        )
    else:
        lines.append(f"- Fail closed: `{FAIL_CLOSED_NEXT_ACTION}`.")

    lines.extend(["", "## Latest Worklog Anchors", ""])
    if anchors:
        for anchor in anchors:  # type: ignore[assignment]
            lines.append(f"- `AGENT_CONTINUITY_ANCHOR: {anchor}`")
    else:
        lines.append("- No anchors found in the selected worklog source.")

    lines.extend(["", "## Recent Events Reviewed", ""])
    if review_events:
        lines.extend(
            [
                "| Event | Source anchor | Observed-result lines |",
                "|---|---|---:|",
            ]
        )
        for event in review_events:  # type: ignore[assignment]
            title = str(event["title"]).replace("|", "\\|")
            lines.append(
                f"| {title} | `{event['source_path']}:{event['anchor_line']}` "
                f"(`{event['event_id']}`) | `{len(event['outcome_lines'])}` |"
            )
    else:
        lines.append("- No eligible deduplicated worklog events were found in the review window.")

    lines.extend(
        [
            "",
            "## Cross-Session Signals",
            "",
            f"A signal qualifies only after `{INDEPENDENT_EVENT_THRESHOLD}` distinct continuity events contain observed outcome evidence.",
            "",
            "| Signal | Events | Mentions | Qualifies | Exemplars | Meaning | Proposed Rule |",
            "|---|---:|---:|---:|---|---|---|",
        ]
    )
    for signal in signals:  # type: ignore[assignment]
        exemplars = "<br>".join(
            str(item).replace("|", "\\|") for item in signal["exemplars"]
        )
        lines.append(
            f"| {signal['label']} | `{signal['event_count']}` | `{signal['mention_count']}` | "
            f"`{str(signal['qualifies']).lower()}` | {exemplars or '-'} | "
            f"{signal['meaning']} | {signal['proposed_rule']} |"
        )

    lines.extend(["", "## Proposed Local Improvements", ""])
    if active_signals:
        promoted = sorted(
            active_signals,
            key=lambda signal: (-int(signal["event_count"]), str(signal["key"])),
        )[0]
        lines.append(f"- Promotion candidate: {promoted['proposed_rule']}")
        if len(active_signals) > 1:
            lines.append(
                f"- `{len(active_signals) - 1}` other qualifying signal(s) remain context only; promote at most one durable rule in this review."
            )
    else:
        lines.append(
            "- No signal appeared in two independent observed-result events. Keep the current prompts and loops unchanged."
        )

    lines.extend(
        [
            "",
            "## Recommended Next Action",
            "",
            f"- {payload['recommended_next_action']}",
            "",
            "## Review Decision",
            "",
            "- `KEEP_LOCAL_ONLY`: this report may guide the next session, but it does not change canonical prompts or live business systems by itself.",
            "- If a future prompt/checklist change is proposed, test it against a small example set and rerun continuity checks before promotion.",
            "",
            "## Command",
            "",
            "```bash",
            "python3.13 ops/scripts/generate_weekly_dream_review.py --as-of YYYY-MM-DD --write-report dresslikemommy-growth-2026/02_AUDIT_PACKETS/YYYY-MM-DD-weekly-dream-review/WEEKLY_DREAM_REVIEW.md",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--as-of", default=date.today().isoformat(), help="Review date, normally YYYY-MM-DD")
    parser.add_argument("--source", action="append", default=[], help="Override default source list; repeatable")
    parser.add_argument("--worklog-tail-lines", type=int, default=900, help="Lines to read from the end of ops/AGENT_WORKLOG.md")
    parser.add_argument("--anchor-limit", type=int, default=5, help="Latest anchors to include")
    parser.add_argument("--write-report", type=Path, help="Write Markdown report to this path")
    parser.add_argument("--write-default-report", action="store_true", help="Write to the default audit packet path")
    parser.add_argument("--json", action="store_true", help="Print JSON payload instead of Markdown")
    return parser.parse_args()


def run(args: argparse.Namespace) -> tuple[dict[str, object], str, Path | None]:
    specs = (
        tuple(source_spec_for_path(path) for path in args.source)
        if args.source
        else DEFAULT_SOURCE_SPECS
    )
    sources = [
        read_source(resolve_path(spec.path), args.worklog_tail_lines, spec)
        for spec in specs
    ]

    events: list[ReviewEvent] = []
    for source in sources:
        events.extend(extract_review_events(source))

    worklog_path = resolve_path("ops/AGENT_WORKLOG.md")
    worklog_text = read_text(worklog_path) if worklog_path.exists() else ""
    anchors = latest_anchors(worklog_text, args.anchor_limit)
    signals = score_events(events)

    authority_source = next(
        (source for source in sources if source.role == "AUTHORITY"), None
    )
    if authority_source is None:
        authority_path = resolve_path("ops/marketing/current_marketing_state.md")
        authority_text = read_text(authority_path) if authority_path.exists() else ""
        authority_source_path = rel(authority_path)
    else:
        authority_text = authority_source.text
        authority_source_path = authority_source.path
    authority = parse_authoritative_control(authority_text, authority_source_path)
    combined_text = "\n\n".join(source.text for source in sources if source.exists)
    next_action = choose_next_action(combined_text, signals, authority)
    payload = build_payload(
        as_of=args.as_of,
        sources=sources,
        anchors=anchors,
        signals=signals,
        next_action=next_action,
        events=events,
        authority=authority,
    )
    report = build_report(payload)

    output_path: Path | None = None
    if args.write_default_report:
        output_path = default_report_path(args.as_of)
    if args.write_report:
        output_path = args.write_report
        if not output_path.is_absolute():
            output_path = ROOT / output_path
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(report, encoding="utf-8")

    return payload, report, output_path


def main() -> int:
    args = parse_args()
    payload, report, output_path = run(args)
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(report)
    if output_path:
        sys.stderr.write(f"Wrote report: {rel(output_path)}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
