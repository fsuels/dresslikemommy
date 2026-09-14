"""Derived channel inventories for the task compiler; never a business-state store."""

from __future__ import annotations

import re
from datetime import date
from pathlib import Path
from typing import Callable

from render_marketing_cockpit import current_task_rows


CHANNEL_ALIASES = {
    "google-ads": ("google ads", "adwords"),
    "google-merchant": ("google merchant center", "google merchant", "merchant center"),
    "google-analytics": ("google analytics", "ga4"),
    "microsoft-ads": ("microsoft advertising", "microsoft ads", "bing ads"),
    "pinterest": ("pinterest",),
    "x": ("x", "twitter"),
    "shopify": ("shopify",),
}
CHANNEL_PATTERNS = {
    "google-ads": r"\bgoogle[\s_-]*(?:ads|operator)\b|\bads(?=\d)|\badwords\b",
    "google-merchant": r"\bmerchant(?=\b|\d)",
    "google-analytics": r"\b(?:ga4|gtm)(?=\b|\d)|\bgoogle[\s_-]*analytics\b",
    "microsoft-ads": r"\bmicrosoft(?:[\s_-]+(?:ads|advertising)\b|(?=\d{6,}\b))|\bbing[\s_-]*ads\b|\buet\b",
    "pinterest": r"\bpinterest\b|\bpins?\b",
    "x": r"\b(?:x|twitter)(?:[\s_-]+(?:public[\s_-]+)?(?:profile|pilot|account|operation|relaunch|organic[\s_-]+(?:pilot|operation|relaunch|growth|content|posts?|publishing|traffic|marketing|campaign))\b|\.com/)",
    "shopify": r"\bshopify(?=\b|\d)|\bstorefront\b|\btheme(?=\b|\d)",
}
QUERY_FILLERS = frozenset(
    "continue resume start work working on with the project task please in for my our help me to".split()
)
DATE_RE = re.compile(r"(?<!\d)\d{4}-\d{2}-\d{2}(?!\d)")
TASK_ID_RE = re.compile(r"\bTA-\d+\b")
OWNER_ID_RE = re.compile(r"\b([0-9a-f]{8})(?![0-9a-f])", re.IGNORECASE)
RESOURCE_REFERENCE_RE = re.compile(
    r"(?<![A-Za-z0-9_.-])(?:(?:[A-Za-z0-9_.-]+/)+[A-Za-z0-9_.-]+|"
    r"[A-Za-z0-9_.-]+\.[A-Za-z][A-Za-z0-9]*)(?![A-Za-z0-9_.-])"
)
COMPOUND_IDENTIFIER_RE = re.compile(
    r"(?<![A-Za-z0-9_.-])[A-Za-z][A-Za-z0-9_]*(?:[.-][A-Za-z0-9_]+)+(?![A-Za-z0-9_.-])"
)


def contains_relationship_entity(text: str, entity: str, contains_entity: Callable) -> bool:
    """Dates inside receipts/actions are not account links; full identifiers survive."""
    if entity.isdigit() and len(entity) == 8:
        try:
            date(int(entity[:4]), int(entity[4:6]), int(entity[6:]))
        except ValueError:
            pass
        else:
            occurrence = re.compile(rf"(?<![A-Za-z0-9_]){re.escape(entity)}(?![A-Za-z0-9_])")

            def mask_resource_date(match):
                # Keep numeric account directories and typed IDs. Only an
                # untyped date embedded in a resource name loses ID status.
                return "/".join(part if part == entity else occurrence.sub(" ", part)
                                for part in match.group().split("/"))

            text = RESOURCE_REFERENCE_RE.sub(mask_resource_date, text)
            # Named actions can carry the same dates without a file extension.
            # Mask only their untyped date component, not another bare/typed ID.
            text = COMPOUND_IDENTIFIER_RE.sub(
                lambda match: occurrence.sub(" ", match.group()), text
            )
    return contains_entity(text, entity)


def owner_ids(text: str) -> set[str]:
    normalized = re.sub(
        r"\b(?:root|parent|task|merchant|ux|analytics|pinterest|google|microsoft|ads|ga4)(?=[0-9a-f]{8})",
        " ", text.casefold(),
    )
    return set(OWNER_ID_RE.findall(normalized))


def channel_for_query(query: str) -> str | None:
    """Only broad, single-channel requests bypass single-anchor selection."""
    normalized = " ".join(re.findall(r"[a-z0-9]+", query.casefold()))
    matches = []
    for channel, aliases in CHANNEL_ALIASES.items():
        for alias in aliases:
            match = re.search(rf"\b{re.escape(alias)}\b", normalized)
            if match:
                remainder = normalized[:match.start()] + " " + normalized[match.end():]
                if set(remainder.split()) <= QUERY_FILLERS:
                    matches.append(channel)
                    break
    return matches[0] if len(matches) == 1 else None


def channel_matches(channel: str, text: str, *, task: bool = False) -> bool:
    if re.search(CHANNEL_PATTERNS[channel], text, re.IGNORECASE):
        return True
    if not task:
        return False
    if channel == "google-ads":
        # Generic paid-pilot tasks belong in the Ads inventory, but an explicitly
        # named Microsoft/Pinterest task is not silently reassigned to Google.
        return bool(re.search(r"\bpaid traffic\b", text, re.IGNORECASE)) and not any(
            re.search(CHANNEL_PATTERNS[other], text, re.IGNORECASE)
            for other in ("microsoft-ads", "pinterest")
        )
    if channel == "shopify":
        explicit_other = any(re.search(CHANNEL_PATTERNS[other], text, re.IGNORECASE) for other in ("microsoft-ads", "pinterest"))
        return not explicit_other and bool(re.search(r"\bstore\b|\b(?:sizing|headings)\b|\bproduct (?:prices|copy|titles|source|repair|selection)\b", text, re.IGNORECASE))
    return False


def source_block(path: Path, text: str, start: int, end: int, format_path: Callable) -> dict:
    return {
        "source_path": format_path(path), "start_line": start, "end_line": end,
        "text": "\n".join(text.splitlines()[start - 1:end]), "evidence_grade": "REPO_KNOWN",
    }


def record_dates(text: str) -> list[str]:
    dates = DATE_RE.findall(text)
    # Receipt names may use YYYYMMDD. These are evidence dates, not account
    # identities; keep bare/typed IDs and numeric account directories out.
    for resource in RESOURCE_REFERENCE_RE.finditer(text):
        for part in resource.group().split("/"):
            for value in re.findall(r"(?<![A-Za-z0-9_])\d{8}(?![A-Za-z0-9_])", part):
                if part == value:
                    continue
                try:
                    dates.append(date(int(value[:4]), int(value[4:6]), int(value[6:])).isoformat())
                except ValueError:
                    pass
    return dates


def coordination_rows(path: Path, text: str, format_path: Callable) -> list[dict]:
    """Read complete registry rows; blocked-action mentions are not their subject."""
    rows = []
    headers = []
    for number, line in enumerate(text.splitlines(), 1):
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in re.split(r"(?<!\\)\|", line.strip().strip("|"))]
        if "Workstream" in cells and "Owner / Agent" in cells:
            headers = cells
            continue
        if not headers or len(cells) != len(headers) or all(re.fullmatch(r"[-: ]+", cell) for cell in cells):
            continue
        row = source_block(path, text, number, number, format_path)
        row["fields"] = dict(zip(headers, cells))
        row["record_date"] = max(record_dates(line), default=None)
        rows.append(row)
    return rows


def business_goal(path: Path, format_path: Callable) -> dict | None:
    if not path.is_file():
        return None
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    starts = [i for i, line in enumerate(lines) if line == "## Owner's Goal In Plain English"]
    if len(starts) != 1:
        return None
    start = starts[0]
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    while end > start and not lines[end - 1].strip():
        end -= 1
    return source_block(path, text, start + 1, end, format_path)


def build_session_brief(
    channel: str, *, action_queue_path: Path, goal_path: Path,
    coordination_path: Path, anchors: list[dict], format_path: Callable,
    extract_entities: Callable, contains_entity: Callable,
) -> tuple[dict, list[str], list[str]]:
    errors, warnings = [], []
    current_tasks = []
    if action_queue_path.is_file():
        queue_text = action_queue_path.read_text(encoding="utf-8")
        try:
            tasks = current_task_rows(queue_text)
        except ValueError as exc:
            tasks = []
            errors.append(f"INVALID_CURRENT_TASK_QUEUE: {exc}")
        # The shared renderer owns parsing/validation; this pass only attaches
        # the original source line and does not implement a second task parser.
        in_current = False
        task_lines = {}
        for number, line in enumerate(queue_text.splitlines(), 1):
            if line.startswith("## "):
                in_current = line.startswith("## Current turnaround tasks")
            if in_current and line.startswith("|"):
                task_id = TASK_ID_RE.search(line)
                if task_id:
                    task_lines[task_id.group()] = number
        for task in tasks:
            subject = " ".join(task.get(key, "") for key in ("Action", "Task title", "Lane"))
            owner_routing = (
                channel == "google-ads" and "paid" in task.get("Lane", "").casefold()
                and channel_matches(channel, task.get("Owner agent", ""))
            )
            next_step_routing = channel == "google-merchant" and channel_matches(channel, task.get("Next step", ""))
            if not (channel_matches(channel, subject, task=True) or owner_routing or next_step_routing):
                continue
            number = task_lines[task["id"]]
            row = source_block(action_queue_path, queue_text, number, number, format_path)
            row.update({"id": task["id"], "fields": task})
            current_tasks.append(row)
    else:
        errors.append(f"CURRENT_TASK_QUEUE_MISSING: {format_path(action_queue_path)}")
    if not current_tasks:
        errors.append("NO_CURRENT_CHANNEL_TASKS")

    goal = business_goal(goal_path, format_path)
    if goal is None:
        warnings.append(f"sourced business goal unavailable: {format_path(goal_path)}")
    task_ids = {row["id"] for row in current_tasks}
    def relationship_entities(text):
        return [entity for entity in extract_entities(text)
                if contains_relationship_entity(text, entity, contains_entity)]

    entities_by_task = {row["id"]: relationship_entities(row["text"]) for row in current_tasks}
    for row in current_tasks:
        # A queue card may name a problem rather than its product. Recover that
        # identity from the latest explicitly linked metadata, with provenance;
        # do not expand through arbitrary prose or recursively follow accounts.
        problem_ids = [entity for entity in entities_by_task[row["id"]] if entity.startswith("PROB-")]
        for anchor in reversed(anchors):
            metadata_text = ",".join(anchor["metadata"].get("task_entities", []))
            metadata_tasks = set(TASK_ID_RE.findall(metadata_text))
            # A multi-task or peer handoff remains related evidence below,
            # but its unpartitioned identities cannot be assigned to this task.
            if metadata_tasks - {row["id"]}:
                continue
            if row["id"] not in metadata_tasks and not any(
                contains_entity(metadata_text, entity) for entity in problem_ids
            ):
                continue
            derived = relationship_entities(metadata_text)
            entities_by_task[row["id"]] = sorted(set(entities_by_task[row["id"]]) | set(derived))
            row["identity_evidence"] = {
                "entities": derived, "anchor_id": anchor["anchor_id"],
                **{key: anchor[key] for key in ("source_path", "start_line", "end_line")},
            }
            break
    task_entities = sorted({entity for entities in entities_by_task.values() for entity in entities})
    task_dates = [date for row in current_tasks for date in DATE_RE.findall(row["fields"].get("Checkpoint date", ""))]
    cutoff = min(task_dates, default="")
    claims = []
    older_claims = []
    excluded_historical = 0
    if coordination_path.is_file():
        for row in coordination_rows(coordination_path, coordination_path.read_text(encoding="utf-8"), format_path):
            fields = row["fields"]
            subject = fields.get("Workstream", "") + " " + fields.get("Surface", "")
            explicit_task_links = task_ids & set(TASK_ID_RE.findall(row["text"]))
            identity_subject = subject + " " + fields.get("Last Evidence / Handoff", "")
            entity_links = {
                task_id: [entity for entity in entities
                          if contains_relationship_entity(identity_subject, entity, contains_entity)]
                for task_id, entities in entities_by_task.items()
            }
            entity_links = {task_id: hits for task_id, hits in entity_links.items() if hits}
            linked = sorted(explicit_task_links | set(entity_links))
            entity_match = any(contains_relationship_entity(subject, entity, contains_entity)
                               for entity in task_entities)
            if not (linked or entity_match or channel_matches(channel, subject)):
                continue
            row["linked_task_ids"] = linked
            row["task_link_basis"] = {
                task_id: {"explicit_task_id": task_id in explicit_task_links, "exact_entities": entity_links.get(task_id, [])}
                for task_id in linked
            }
            record_date = row["record_date"] or ""
            if cutoff and record_date and record_date < cutoff:
                excluded_historical += 1
                # An old unresolved lock is not cleared or silently revived as
                # present permission. Keep its identity/status and exact source
                # available for reconciliation outside the current brief.
                older_claims.append({
                    key: row[key] for key in ("source_path", "start_line", "end_line", "record_date", "linked_task_ids", "task_link_basis")
                } | {
                    "workstream": fields.get("Workstream"), "owner": fields.get("Owner / Agent"),
                    "status": fields.get("Status"), "evidence_grade": "STALE_OR_SUPERSEDED",
                    "handling": "HISTORICAL_SCOPE_REQUIRES_RECONCILIATION; this retrieval neither clears a lock nor grants its old scope",
                })
                continue
            row["dated_before_current_tasks"] = bool(cutoff and record_date and record_date < cutoff)
            claims.append(row)
        claims.sort(key=lambda row: (-(int((row["record_date"] or "0000-00-00").replace("-", ""))), row["start_line"]))
    else:
        warnings.append(f"coordination registry unavailable: {format_path(coordination_path)}")

    direct_anchors, related_anchors = [], []
    primary_account_ids = {
        number for row in current_tasks
        for number in re.findall(r"\b(?:Ads|manager)(\d{7,})", row["fields"].get("Action", ""), re.IGNORECASE)
    } if channel == "google-ads" else set()
    for anchor in reversed(anchors):
        metadata = anchor["metadata"]
        subject = anchor["anchor_id"] + " " + " ".join(metadata.get("task_entities", []))
        linked = task_ids & set(TASK_ID_RE.findall(anchor["text"]))
        if channel_matches(channel, subject) or any(
            contains_relationship_entity(subject, entity, contains_entity) for entity in primary_account_ids
        ):
            direct_anchors.append(anchor)
        elif linked or any(contains_relationship_entity(subject, entity, contains_entity) for entity in task_entities):
            related_anchors.append(anchor)
    anchor_count = len(direct_anchors) + len(related_anchors)
    # Keep the channel's own recent outcomes visible even when a shared account
    # or theme generates newer cross-channel handoffs.
    recent = (direct_anchors[:3] + related_anchors[:3])[:6]
    if len(recent) < 6:
        used = {anchor["anchor_id"] for anchor in recent}
        recent.extend(anchor for anchor in direct_anchors + related_anchors if anchor["anchor_id"] not in used)
        recent = recent[:6]

    conflicts, comparisons = [], []
    for row in current_tasks:
        task_roots = owner_ids(row["fields"].get("Owner agent", ""))
        for claim in claims:
            if row["id"] not in claim["linked_task_ids"]:
                continue
            comparison = {
                "task_id": row["id"],
                "queue_source": {key: row[key] for key in ("source_path", "start_line", "end_line")},
                "claim_source": {key: claim[key] for key in ("source_path", "start_line", "end_line")},
                "queue_owner": row["fields"].get("Owner agent"),
                "claim_owner": claim["fields"].get("Owner / Agent"),
                "match_basis": claim["task_link_basis"][row["id"]],
                "conflict_assessment": "UNRESOLVED_SOURCE_COMPARISON; differently worded gates are not automatically reconciled",
                "queue_status": row["fields"].get("Status"),
                "queue_gate": row["fields"].get("Gate"),
                "queue_next_step": row["fields"].get("Next step"),
                "claim_status": claim["fields"].get("Status"),
                "claim_notes": claim["fields"].get("Notes"),
            }
            comparisons.append(comparison)
            claim_roots = owner_ids(str(comparison["claim_owner"]))
            if comparison["match_basis"]["explicit_task_id"] and task_roots and claim_roots and task_roots.isdisjoint(claim_roots):
                conflicts.append({"kind": "OWNER_MISMATCH_REQUIRES_RECONCILIATION", **comparison})
    if conflicts:
        warnings.append("current queue and coordination owner identities disagree; preserve both and reconcile before action")

    return {
        "channel": channel,
        "mode": "CHANNEL_INVENTORY",
        "external_write_authorized": False,
        "authority_note": "Retrieved context is not external-write approval or a transferred claim. Current user scope, exact authority, claim ownership and fresh readbacks still govern.",
        "evidence_note": "Current tasks are repo-known records. Dated worklog evidence is historical context; receipt, local tests and completed source repairs do not establish serving, purchase acceptance or profit. Textual gate differences require source review; no semantic reconciliation is inferred.",
        "business_goal": goal,
        "current_tasks": current_tasks,
        "coordination_claims": claims,
        "excluded_historical_coordination_count": excluded_historical,
        "older_coordination_claims": older_claims,
        "recent_anchors": recent,
        "relevant_anchor_count": anchor_count,
        "source_comparisons": comparisons,
        "conflicts": conflicts,
        "next_step": "Review the sourced tasks and existing owner claims; resume the applicable unfinished step without replaying completed work. Broad Shopify inventory does not select a product or release.",
    }, errors, warnings


def render_context_brief(payload: dict) -> str:
    """Startup view without repeated raw rows; complete JSON remains available."""
    def source(record: dict) -> str:
        start = record.get("start_line", record.get("line"))
        end = record.get("end_line")
        suffix = f"-{end}" if end and end != start else ""
        return f"{record.get('source_path')}:{start}{suffix}"

    lines = [f"# Session context: {payload['query']}", "", f"Retrieval: {payload['diagnostics']['status']}",
             "Context is not external-write approval, transferred ownership, or a current live readback."]
    for kind in ("errors", "warnings"):
        lines.extend(f"{kind.upper()}: {item}" for item in payload["diagnostics"][kind])
    authority = payload["authority"]
    lines += ["", f"Authority — {source(authority)}"]
    lines.extend(f"- {key}: {value}" for key, value in authority["fields"].items())
    brief = payload.get("session_brief")
    if brief:
        goal = brief.get("business_goal")
        if goal:
            lines += ["", f"Business goal — {source(goal)}", goal["text"]]
        lines += ["", f"Current {brief['channel']} tasks ({len(brief['current_tasks'])}); repo-known, not live proof"]
        for row in brief["current_tasks"]:
            fields = row["fields"]
            lines += ["", f"{row['id']} — {fields.get('Task title', fields.get('Action'))} — {source(row)}"]
            for key in ("Priority", "Status", "Action", "Owner agent", "Lane", "Checkpoint", "Checkpoint date", "Owner input", "Gate", "Completed milestone", "Next step", "Evidence/source"):
                lines.append(f"- {key}: {fields.get(key, 'UNKNOWN')}")
            if row.get("identity_evidence"):
                identity = row["identity_evidence"]
                lines.append(f"- Identity metadata: {identity['anchor_id']} — {source(identity)}")
        lines += ["", f"Current coordination claims ({len(brief['coordination_claims'])})",
                  "Read the complete allowed/blocked actions and notes at these source rows before acting; these summaries confer no scope."]
        for claim in brief["coordination_claims"]:
            fields = claim["fields"]
            linked = ", ".join(claim["linked_task_ids"]) or "channel scope"
            lines.append(f"- {fields.get('Workstream')} [{linked}]: {fields.get('Status')}; owner {fields.get('Owner / Agent')} — {source(claim)}")
        older_count = len(brief["older_coordination_claims"])
        lines.append(f"Older coordination records: {older_count} separated from current scope. Complete JSON retains every older identity/status/source; no old lock is cleared or scope revived.")
        if brief["source_comparisons"]:
            lines += ["", "Queue/claim gate comparisons remain unresolved; inspect the paired sources before taking over work:"]
            for item in brief["source_comparisons"]:
                lines.append(f"- {item['task_id']}: queue {source(item['queue_source'])}; claim {source(item['claim_source'])}; claim status {item['claim_status']}")
        for conflict in brief["conflicts"]:
            lines.append(f"CONFLICT {conflict['kind']}: {conflict['task_id']}; queue owner {conflict['queue_owner']}; claim owner {conflict['claim_owner']}; {source(conflict['claim_source'])}")
        lines += ["", f"Recent channel/related anchors ({len(brief['recent_anchors'])} of {brief['relevant_anchor_count']} relevant records; source text available in JSON):"]
        lines.extend(f"- {row['anchor_id']} — {source(row)} [{row['evidence_grade']}]" for row in brief["recent_anchors"])
        lines += ["", brief["next_step"]]
    else:
        selected = payload.get("selected_anchor")
        if selected:
            lines += ["", f"Selected relevance anchor: {selected['anchor_id']} — {source(selected)}",
                      f"Currentness: {selected.get('currentness', 'REPO_KNOWN; verify live state before acting')}"]
    newer = payload.get("newer_same_entity_records", [])
    if newer:
        lines += ["", "Newer same-entity records must be reviewed before treating the selected evidence as current:"]
        lines.extend(f"- {row['anchor_id']} — {source(row)}" for row in newer)
    lines += ["", "Default --format json retains complete task/claim/anchor records. This brief selects fields explicitly; it does not replace source review."]
    return "\n".join(lines) + "\n"
