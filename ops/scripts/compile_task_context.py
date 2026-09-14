#!/usr/bin/env python3.13
"""Compile a deterministic, retrieval-first task context from canonical files.

The compiler is local-only. It selects a task-relevant continuity anchor instead
of falling back to the globally newest anchor, reads the exact authoritative
marketing control block, and labels retrieved evidence conservatively. It never
calls or writes to an external system.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from session_context import build_session_brief, channel_for_query, coordination_rows, render_context_brief


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_WORKLOG = ROOT / "ops/AGENT_WORKLOG.md"
DEFAULT_CURRENT_STATE = ROOT / "ops/marketing/current_marketing_state.md"
DEFAULT_PROBLEM_TRACKER = ROOT / "ops/PROBLEM_TRACKER.md"
DEFAULT_COORDINATION = ROOT / "ops/AGENT_COORDINATION.md"

SCHEMA_VERSION = "1.0"
AUTHORITY_START = "<!-- MARKETING_AUTHORITATIVE_CONTROL:START -->"
AUTHORITY_END = "<!-- MARKETING_AUTHORITATIVE_CONTROL:END -->"
AUTHORITY_FIELDS = (
    "control_as_of",
    "source_live_evidence_as_of",
    "live_state_mode",
    "live_readback_fresh_until",
    "autonomous_action_ready",
    "effective_approval_policy",
    "approved_external_scope",
    "next_best_action",
    "supersedes_execution_readiness_below",
)
VALID_EVIDENCE_LABELS = frozenset(
    {
        "REPO_KNOWN",
        "LIVE_READBACK_REQUIRED",
        "LIVE_VERIFIED",
        "STALE_OR_SUPERSEDED",
    }
)
VALID_TASK_STAGES = frozenset(
    {
        "DIAGNOSE",
        "BUILD",
        "VERIFY",
        "HANDOFF",
        "BLOCKED",
        "UNKNOWN",
    }
)
VALID_TASK_KINDS = frozenset({"paid-growth", "local"})

ANCHOR_LINE_RE = re.compile(
    r"(?m)^\s*AGENT_CONTINUITY_ANCHOR:\s*(?P<anchor>[A-Za-z0-9_.:-]+)\s*$"
)
FIELD_LINE_RE = re.compile(
    r"(?m)^[ \t]*(?:[-*][ \t]+)?`?(?P<key>[a-z][a-z0-9_]*)`?[ \t]*:[ \t]*"
    r"(?P<value>[^\n]+?)[ \t]*$"
)
EXACT_AUTHORITY_FIELD_RE = re.compile(
    r"^\s*-\s*`(?P<key>[a-z][a-z0-9_]*)`\s*:\s*`(?P<value>[^`]*)`\s*$"
)
ANCHOR_ENTITY_RE = re.compile(
    r"(?i)AGENT_CONTINUITY_ANCHOR:\s*([A-Za-z0-9_.:-]+)"
)
PATH_ENTITY_RE = re.compile(
    r"(?<![A-Za-z0-9_.-])(?:[A-Za-z0-9_.-]+/)+[A-Za-z0-9_.-]+"
)
PREFIXED_ID_RE = re.compile(
    r"(?i)\b(?:PROB|ERR|DLM|TASK|FAM)-[A-Z0-9_.:-]+(?:-[A-Z0-9_.:-]+)*\b"
)
ACTION_ID_RE = re.compile(r"\b[A-Z][A-Z0-9]+(?:_[A-Z0-9]+)+\b")
LONG_NUMERIC_ID_RE = re.compile(r"\b\d{7,}\b")
COMPACT_ID_RE = re.compile(
    # Prefix-specific minimums retain one numeric capture for findall callers.
    r"(?i)(?<![A-Za-z0-9_])(?:(?:Merchant|GA4|property|Ads|manager|Shopify|Product|"
    r"campaign|source|theme|advertiser|tag|pixel|variant|Purchase|UET)(?=\d{7})|"
    r"Microsoft(?=\d{6}))(\d+)(?![A-Za-z0-9_])"
)
WORD_RE = re.compile(r"[A-Za-z0-9]+")

STOPWORDS = frozenset(
    {
        "a",
        "an",
        "and",
        "are",
        "as",
        "at",
        "be",
        "by",
        "continue",
        "current",
        "do",
        "for",
        "from",
        "in",
        "is",
        "it",
        "of",
        "on",
        "or",
        "project",
        "task",
        "the",
        "this",
        "to",
        "with",
    }
)


@dataclass(frozen=True)
class AnchorRecord:
    anchor_id: str
    start_line: int
    end_line: int
    order: int
    text: str


@dataclass(frozen=True)
class RankedAnchor:
    record: AnchorRecord
    entity_hits: tuple[str, ...]
    token_hits: tuple[str, ...]

    @property
    def relevance_score(self) -> int:
        return 100 * len(self.entity_hits) + len(self.token_hits)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(errors="replace")


def display_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return resolved.relative_to(ROOT).as_posix()
    except ValueError:
        return resolved.as_posix()


def stable_unique(values: Iterable[str]) -> list[str]:
    by_normalized: dict[str, str] = {}
    for raw in values:
        value = raw.strip().strip("`")
        if value:
            by_normalized.setdefault(value.casefold(), value)
    return [by_normalized[key] for key in sorted(by_normalized)]


def extract_entities(text: str, explicit_entities: Iterable[str] = ()) -> list[str]:
    """Extract stable IDs and paths; ordinary prose is not promoted to an entity."""

    values: list[str] = list(explicit_entities)
    values.extend(ANCHOR_ENTITY_RE.findall(text))
    values.extend(PATH_ENTITY_RE.findall(text))
    values.extend(PREFIXED_ID_RE.findall(text))
    values.extend(ACTION_ID_RE.findall(text))
    values.extend(LONG_NUMERIC_ID_RE.findall(text))
    values.extend(COMPACT_ID_RE.findall(text))
    return stable_unique(values)


def significant_tokens(text: str) -> tuple[str, ...]:
    tokens = {
        token.casefold()
        for token in WORD_RE.findall(text)
        if len(token) >= 3
        and token.casefold() not in STOPWORDS
        and not token.isdigit()
    }
    return tuple(sorted(tokens))


def contains_exact_entity(text: str, entity: str) -> bool:
    pattern = re.compile(
        rf"(?<![A-Za-z0-9_]){re.escape(entity)}(?![A-Za-z0-9_])",
        re.IGNORECASE,
    )
    if pattern.search(text):
        return True
    # Repository records sometimes join a typed account label to its number.
    # Match the complete typed number, never a numeric substring or arbitrary
    # word suffix; explicit multi-entity intersection remains unchanged.
    return entity.isdigit() and entity in COMPACT_ID_RE.findall(text)


def parse_anchor_records(text: str) -> tuple[list[AnchorRecord], list[str]]:
    """Return newest copy of each exact whole-line anchor declaration."""

    lines = text.splitlines()
    matches = list(ANCHOR_LINE_RE.finditer(text))
    records: list[AnchorRecord] = []
    for order, match in enumerate(matches):
        start_line = text.count("\n", 0, match.start()) + 1
        if order + 1 < len(matches):
            end_line = text.count("\n", 0, matches[order + 1].start())
        else:
            end_line = len(lines)
        for candidate_line in range(start_line + 1, end_line + 1):
            if lines[candidate_line - 1].strip() == "---":
                end_line = candidate_line - 1
                break
        record_text = "\n".join(lines[start_line - 1 : end_line])
        records.append(
            AnchorRecord(
                anchor_id=match.group("anchor"),
                start_line=start_line,
                end_line=end_line,
                order=order,
                text=record_text,
            )
        )

    newest_by_id: dict[str, AnchorRecord] = {}
    counts: dict[str, int] = {}
    for record in records:
        key = record.anchor_id.casefold()
        counts[key] = counts.get(key, 0) + 1
        newest_by_id[key] = record
    duplicate_ids = sorted(
        newest_by_id[key].anchor_id for key, count in counts.items() if count > 1
    )
    deduplicated = sorted(newest_by_id.values(), key=lambda record: record.order)
    return deduplicated, duplicate_ids


def rank_anchors(
    records: Iterable[AnchorRecord], query: str, entities: Iterable[str]
) -> list[RankedAnchor]:
    query_tokens = significant_tokens(query)
    ranked: list[RankedAnchor] = []
    for record in records:
        searchable = f"{record.anchor_id}\n{record.text}"
        entity_hits = tuple(
            entity for entity in entities if contains_exact_entity(searchable, entity)
        )
        record_tokens = set(significant_tokens(searchable))
        token_hits = tuple(token for token in query_tokens if token in record_tokens)
        ranked.append(RankedAnchor(record, entity_hits, token_hits))
    return sorted(
        ranked,
        key=lambda item: (
            -item.relevance_score,
            -len(item.entity_hits),
            -len(item.token_hits),
            -item.record.order,
            item.record.anchor_id.casefold(),
        ),
    )


def select_anchor(
    ranked: list[RankedAnchor],
    has_entities: bool,
    required_entities: Iterable[str] = (),
) -> tuple[RankedAnchor | None, str | None]:
    if not ranked:
        return None, "NO_RELEVANT_ANCHOR"

    required = stable_unique(required_entities)
    if required:
        required_keys = {entity.casefold() for entity in required}
        relevant = [
            item
            for item in ranked
            if required_keys
            <= {entity.casefold() for entity in item.entity_hits}
        ]
        if not relevant:
            return None, "REQUIRED_ENTITIES_NOT_COLOCATED"
    elif has_entities:
        relevant = [item for item in ranked if item.entity_hits]
    else:
        relevant = [item for item in ranked if len(item.token_hits) >= 2]
    if not relevant:
        return None, "NO_RELEVANT_ANCHOR"

    best = relevant[0]
    tied = [
        item
        for item in relevant
        if item.relevance_score == best.relevance_score
        and len(item.entity_hits) == len(best.entity_hits)
        and len(item.token_hits) == len(best.token_hits)
    ]
    if len(tied) > 1:
        if not has_entities:
            return None, "AMBIGUOUS_RELEVANT_ANCHOR"
        distinct_hit_sets = {
            tuple(entity.casefold() for entity in item.entity_hits) for item in tied
        }
        if len(distinct_hit_sets) > 1:
            return None, "AMBIGUOUS_RELEVANT_ANCHOR"
    if required:
        # For the same explicitly required scope, later state supersedes older
        # prose matches. Keep different entity sets and ambiguity checks intact.
        best_hits = frozenset(entity.casefold() for entity in best.entity_hits)
        best = max(
            (
                item for item in relevant
                if frozenset(entity.casefold() for entity in item.entity_hits) == best_hits
            ),
            key=lambda item: item.record.order,
        )
    return best, None


def parse_exact_authority_block(
    text: str, source_path: Path
) -> tuple[dict[str, object], list[str]]:
    errors: list[str] = []
    start_count = text.count(AUTHORITY_START)
    end_count = text.count(AUTHORITY_END)
    if start_count != 1 or end_count != 1:
        errors.append(
            "authoritative control markers must each occur exactly once"
        )
        return {
            "evidence_grade": "LIVE_READBACK_REQUIRED",
            "end_line": None,
            "fields": {},
            "source_path": display_path(source_path),
            "start_line": None,
        }, errors

    start_index = text.index(AUTHORITY_START)
    end_index = text.index(AUTHORITY_END)
    if end_index <= start_index:
        errors.append("authoritative control end marker precedes start marker")
        return {
            "evidence_grade": "LIVE_READBACK_REQUIRED",
            "end_line": None,
            "fields": {},
            "source_path": display_path(source_path),
            "start_line": None,
        }, errors

    start_line = text.count("\n", 0, start_index) + 1
    end_line = text.count("\n", 0, end_index) + 1
    block_lines = text[start_index + len(AUTHORITY_START) : end_index].splitlines()
    occurrences: dict[str, list[str]] = {}
    malformed_nonblank: list[str] = []
    for line in block_lines:
        if not line.strip():
            continue
        match = EXACT_AUTHORITY_FIELD_RE.fullmatch(line)
        if not match:
            malformed_nonblank.append(line.strip())
            continue
        occurrences.setdefault(match.group("key"), []).append(
            match.group("value").strip()
        )

    if malformed_nonblank:
        errors.append("malformed authoritative control field line(s)")
    duplicate_fields = sorted(
        key for key, values in occurrences.items() if len(values) != 1
    )
    if duplicate_fields:
        errors.append("duplicate authoritative field(s): " + ", ".join(duplicate_fields))
    missing_fields = [key for key in AUTHORITY_FIELDS if key not in occurrences]
    if missing_fields:
        errors.append("missing authoritative field(s): " + ", ".join(missing_fields))
    unexpected_fields = sorted(set(occurrences) - set(AUTHORITY_FIELDS))
    if unexpected_fields:
        errors.append("unexpected authoritative field(s): " + ", ".join(unexpected_fields))

    fields = {
        key: values[0]
        for key, values in sorted(occurrences.items())
        if len(values) == 1
    }
    evidence_grade = authority_evidence_grade(fields)
    return {
        "evidence_grade": evidence_grade,
        "end_line": end_line,
        "fields": fields,
        "source_path": display_path(source_path),
        "start_line": start_line,
    }, errors


def authority_evidence_grade(fields: dict[str, str]) -> str:
    live_state_mode = fields.get("live_state_mode", "").upper()
    fresh_until = fields.get("live_readback_fresh_until", "").upper()
    if live_state_mode == "LIVE_CURRENT" and fresh_until != "EXPIRED":
        return "LIVE_VERIFIED"
    if "STALE" in live_state_mode or "REQUIRED" in live_state_mode or fresh_until == "EXPIRED":
        return "LIVE_READBACK_REQUIRED"
    return "REPO_KNOWN"


def parse_anchor_metadata(record: AnchorRecord) -> dict[str, object]:
    def clean_value(value: str) -> str:
        value = value.strip().rstrip(".;").strip()
        if value.startswith("`") and value.endswith("`"):
            value = value[1:-1]
        return value.strip().rstrip(".;").strip()

    occurrences: dict[str, list[str]] = {}
    for match in FIELD_LINE_RE.finditer(record.text):
        key = match.group("key").casefold()
        if key in {"task_entities", "task_stage", "next_action_id"}:
            occurrences.setdefault(key, []).append(clean_value(match.group("value")))

    metadata: dict[str, object] = {}
    duplicate_fields = sorted(key for key, values in occurrences.items() if len(values) > 1)
    if duplicate_fields:
        metadata["duplicate_fields"] = duplicate_fields
    task_entities: list[str] = []
    if len(occurrences.get("task_entities", [])) == 1:
        task_entities = stable_unique(
            clean_value(part)
            for part in occurrences["task_entities"][0].split(",")
        )
    task_stage = "UNKNOWN"
    if len(occurrences.get("task_stage", [])) == 1:
        candidate = occurrences["task_stage"][0].upper()
        if candidate in VALID_TASK_STAGES:
            task_stage = candidate
        else:
            metadata["invalid_task_stage"] = candidate
    next_action_id = None
    if len(occurrences.get("next_action_id", [])) == 1:
        next_action_id = occurrences["next_action_id"][0]
    metadata.update(
        {
            "next_action_id": next_action_id,
            "task_entities": task_entities,
            "task_stage": task_stage,
        }
    )
    return metadata


def historical_evidence_grade(text: str, authority_grade: str) -> str:
    lower = text.casefold()
    looks_like_live_claim = any(
        marker in lower
        for marker in (
            "live_verified",
            "live readback",
            "approved_active",
            "`green`",
        )
    )
    if authority_grade == "LIVE_READBACK_REQUIRED" and looks_like_live_claim:
        return "STALE_OR_SUPERSEDED"
    return "REPO_KNOWN"


def matching_source_lines(
    path: Path,
    text: str,
    entities: list[str],
    query_tokens: tuple[str, ...],
    authority_grade: str,
    limit: int = 4,
) -> list[dict[str, object]]:
    matches: list[dict[str, object]] = []
    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        line = " ".join(raw_line.strip().split())
        if not line:
            continue
        entity_hits = [entity for entity in entities if contains_exact_entity(line, entity)]
        token_hits = sorted(set(query_tokens) & set(significant_tokens(line)))
        qualifies = bool(entity_hits) if entities else len(token_hits) >= 2
        if not qualifies:
            continue
        matches.append(
            {
                "evidence_grade": historical_evidence_grade(line, authority_grade),
                "line": line_number,
                "matched_entities": sorted(entity_hits, key=str.casefold),
                "matched_tokens": token_hits,
                "source_path": display_path(path),
                "text": line[:500],
            }
        )
        if len(matches) >= limit:
            break
    return matches


def matching_coordination_rows(
    path: Path, text: str, entities: list[str], query_tokens: tuple[str, ...],
    authority_grade: str, limit: int = 4,
) -> list[dict[str, object]]:
    matches = []
    for row in coordination_rows(path, text, display_path):
        fields = row["fields"]
        subject = " ".join(str(fields.get(key, "")) for key in ("Workstream", "Surface", "Last Evidence / Handoff"))
        entity_hits = [entity for entity in entities if contains_exact_entity(subject, entity)]
        token_hits = sorted(set(query_tokens) & set(significant_tokens(subject)))
        if not (bool(entity_hits) if entities else len(token_hits) >= 2):
            continue
        matches.append({
            **row, "line": row["start_line"], "matched_entities": entity_hits,
            "matched_tokens": token_hits,
            "evidence_grade": historical_evidence_grade(row["text"], authority_grade),
        })
    matches.sort(key=lambda row: (-int((row["record_date"] or "0000-00-00").replace("-", "")), row["start_line"]))
    return matches[:limit]


def compile_task_context(
    query: str,
    *,
    explicit_entities: Iterable[str] = (),
    worklog_path: Path = DEFAULT_WORKLOG,
    current_state_path: Path = DEFAULT_CURRENT_STATE,
    problem_tracker_path: Path = DEFAULT_PROBLEM_TRACKER,
    coordination_path: Path = DEFAULT_COORDINATION,
    task_kind: str = "paid-growth",
    action_queue_path: Path | None = None,
    goal_path: Path | None = None,
) -> dict[str, object]:
    """Build context without mutating files or silently choosing a global anchor."""

    if task_kind not in VALID_TASK_KINDS:
        raise ValueError(f"invalid task_kind: {task_kind}")
    worklog_text = read_text(worklog_path)
    records, duplicate_anchor_ids = parse_anchor_records(worklog_text)
    required_entities = stable_unique(explicit_entities)
    entities = extract_entities(query, required_entities)
    ranked = rank_anchors(records, query, entities)
    selected, anchor_error = select_anchor(
        ranked,
        bool(entities),
        required_entities=required_entities,
    )
    session_channel = (
        channel_for_query(query)
        if task_kind == "paid-growth" and not entities
        else None
    )
    if session_channel:
        # A broad channel request asks for its task inventory, not one inferred
        # product/campaign anchor. Detailed and explicit-entity requests retain
        # the original ambiguity and intersection contract.
        selected, anchor_error = None, None
    if task_kind == "paid-growth":
        authority, authority_errors = parse_exact_authority_block(
            read_text(current_state_path), current_state_path
        )
    else:
        authority = {
            "context": "NOT_APPLICABLE",
            "evidence_grade": "REPO_KNOWN",
            "end_line": None,
            "fields": {},
            "source_path": None,
            "start_line": None,
        }
        authority_errors = []

    errors = list(authority_errors)
    if anchor_error:
        errors.append(anchor_error)

    warnings: list[str] = []
    selected_anchor: dict[str, object] | None = None
    task_stage = "UNKNOWN"
    selected_metadata: dict[str, object] = {}
    newer_same_entity_records: list[dict[str, object]] = []
    if selected:
        selected_metadata = parse_anchor_metadata(selected.record)
        task_stage = str(selected_metadata["task_stage"])
        if task_stage == "UNKNOWN":
            warnings.append("selected anchor has no valid task_stage metadata")
        if selected_metadata.get("duplicate_fields"):
            errors.append("selected anchor has duplicate task metadata field(s)")
        if selected_metadata.get("invalid_task_stage"):
            errors.append("selected anchor has invalid task_stage metadata")
        selected_anchor = {
            "anchor_id": selected.record.anchor_id,
            "end_line": selected.record.end_line,
            "entity_hits": list(selected.entity_hits),
            "metadata": selected_metadata,
            "relevance_score": selected.relevance_score,
            "source_path": display_path(worklog_path),
            "start_line": selected.record.start_line,
            "token_hits": list(selected.token_hits),
        }
        if selected.entity_hits:
            matching_newer = [
                item for item in ranked
                if item.record.order > selected.record.order
                and set(selected.entity_hits) <= set(item.entity_hits)
            ]
            for item in sorted(matching_newer, key=lambda item: -item.record.order)[:4]:
                newer_same_entity_records.append({
                    "anchor_id": item.record.anchor_id,
                    "source_path": display_path(worklog_path),
                    "start_line": item.record.start_line, "end_line": item.record.end_line,
                    "metadata": parse_anchor_metadata(item.record),
                    "text": item.record.text,
                    "evidence_grade": "REPO_KNOWN",
                })
            if newer_same_entity_records:
                selected_anchor["currentness"] = "UNRESOLVED_NEWER_SAME_ENTITY_RECORDS_EXIST"
                warnings.append(
                    "selected anchor is historical relevance context; newer same-entity records exist. "
                    "Read newer_same_entity_records before treating any business state or next step as current"
                )

    authority_fields = authority.get("fields", {})
    if not isinstance(authority_fields, dict):
        authority_fields = {}
    next_action_id = (
        authority_fields.get("next_best_action")
        if task_kind == "paid-growth"
        else selected_metadata.get("next_action_id")
    )
    if selected_metadata.get("next_action_id") and next_action_id:
        if str(selected_metadata["next_action_id"]).upper() != str(next_action_id).upper():
            errors.append("selected anchor next_action_id contradicts authoritative control")

    evidence: list[dict[str, object]] = []
    authority_grade = str(authority["evidence_grade"])
    session_brief = None
    if session_channel:
        anchor_sources = [{
            "anchor_id": record.anchor_id, "source_path": display_path(worklog_path),
            "start_line": record.start_line, "end_line": record.end_line,
            "text": record.text, "metadata": parse_anchor_metadata(record),
            "evidence_grade": historical_evidence_grade(record.text, authority_grade),
        } for record in records]
        session_brief, brief_errors, brief_warnings = build_session_brief(
            session_channel,
            action_queue_path=action_queue_path or current_state_path.parent / "action_queue.md",
            goal_path=goal_path or worklog_path.parent / "GROWTH_NORTH_STAR.md",
            coordination_path=coordination_path,
            anchors=anchor_sources, format_path=display_path,
            extract_entities=extract_entities, contains_entity=contains_exact_entity,
        )
        errors.extend(brief_errors)
        warnings.extend(brief_warnings)
    if task_kind == "paid-growth":
        evidence.append(
            {
                "evidence_grade": authority_grade,
                "line": authority.get("start_line"),
                "source_path": display_path(current_state_path),
                "text": "Authoritative Execution Control",
            }
        )
    if selected:
        evidence.append(
            {
                "evidence_grade": historical_evidence_grade(
                    selected.record.text, authority_grade
                ),
                "line": selected.record.start_line,
                "source_path": display_path(worklog_path),
                "text": f"AGENT_CONTINUITY_ANCHOR: {selected.record.anchor_id}",
            }
        )

    query_tokens = significant_tokens(query)
    for optional_path in (problem_tracker_path, coordination_path):
        if session_brief is not None and optional_path == coordination_path:
            evidence.extend({
                "source_path": row["source_path"], "line": row["start_line"],
                "evidence_grade": row["evidence_grade"],
                "text": row["fields"].get("Workstream", "Coordination claim"),
                "complete_record": "session_brief.coordination_claims",
            } for row in session_brief["coordination_claims"])
            continue
        if optional_path.exists():
            matcher = matching_coordination_rows if optional_path == coordination_path else matching_source_lines
            evidence.extend(
                matcher(
                    optional_path,
                    read_text(optional_path),
                    entities,
                    query_tokens,
                    authority_grade,
                )
            )
        else:
            warnings.append(f"optional source missing: {display_path(optional_path)}")

    ranked_preview = [
        {
            "anchor_id": item.record.anchor_id,
            "entity_hits": list(item.entity_hits),
            "relevance_score": item.relevance_score,
            "start_line": item.record.start_line,
            "token_hits": list(item.token_hits),
        }
        for item in ranked[:5]
        if item.relevance_score > 0
    ]
    status = "OK" if not errors else "FAILED_CLOSED"
    return {
        "authority": authority,
        "diagnostics": {
            "duplicate_anchor_ids": duplicate_anchor_ids,
            "errors": sorted(errors),
            "ranked_anchor_candidates": ranked_preview,
            "status": status,
            "warnings": sorted(warnings),
        },
        "entities": entities,
        "evidence": evidence,
        "next_action": {
            "id": next_action_id,
            "source_path": (
                display_path(current_state_path)
                if task_kind == "paid-growth"
                else display_path(worklog_path)
            ),
        },
        "newer_same_entity_records": newer_same_entity_records,
        "query": " ".join(query.split()),
        "schema_version": SCHEMA_VERSION,
        "session_brief": session_brief,
        "selected_anchor": selected_anchor,
        "task_stage": task_stage,
        "task_kind": task_kind,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", required=True, help="Task or continuation query")
    parser.add_argument(
        "--task-kind",
        choices=sorted(VALID_TASK_KINDS),
        default="paid-growth",
        help="Use paid-growth authority or compile repo-local continuity only",
    )
    parser.add_argument(
        "--entity",
        action="append",
        default=[],
        help="Exact stable ID/path to require during anchor retrieval; repeatable",
    )
    parser.add_argument("--worklog", type=Path, default=DEFAULT_WORKLOG)
    parser.add_argument("--current-state", type=Path, default=DEFAULT_CURRENT_STATE)
    parser.add_argument("--problem-tracker", type=Path, default=DEFAULT_PROBLEM_TRACKER)
    parser.add_argument("--coordination", type=Path, default=DEFAULT_COORDINATION)
    parser.add_argument("--action-queue", type=Path, help="Canonical action queue; defaults beside current state")
    parser.add_argument("--goal", type=Path, help="Growth North Star; defaults beside worklog")
    parser.add_argument("--format", choices=("json", "brief"), default="json", help="Complete JSON or compact sourced startup view")
    parser.add_argument("--output", type=Path, help="Optional JSON output path")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    required = (
        (args.worklog, args.current_state)
        if args.task_kind == "paid-growth"
        else (args.worklog,)
    )
    missing = [display_path(path) for path in required if not path.exists()]
    if missing:
        sys.stderr.write("Missing required context file(s): " + ", ".join(missing) + "\n")
        return 2

    payload = compile_task_context(
        args.query,
        explicit_entities=args.entity,
        worklog_path=args.worklog,
        current_state_path=args.current_state,
        problem_tracker_path=args.problem_tracker,
        coordination_path=args.coordination,
        task_kind=args.task_kind,
        action_queue_path=args.action_queue,
        goal_path=args.goal,
    )
    rendered = (
        render_context_brief(payload)
        if args.format == "brief"
        else json.dumps(payload, indent=2, sort_keys=True) + "\n"
    )
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if payload["diagnostics"]["status"] == "OK" else 1  # type: ignore[index]


if __name__ == "__main__":
    raise SystemExit(main())
