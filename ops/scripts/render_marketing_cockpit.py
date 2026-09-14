#!/usr/bin/env python3
"""Render the marketing command layer into a self-contained human cockpit."""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MARKETING = ROOT / "ops" / "marketing"
MARKETING_CONTROL_START = "<!-- MARKETING_AUTHORITATIVE_CONTROL:START -->"
MARKETING_CONTROL_END = "<!-- MARKETING_AUTHORITATIVE_CONTROL:END -->"


@dataclass(frozen=True)
class Table:
    headers: list[str]
    rows: list[list[str]]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def strip_inline_markdown(value: str) -> str:
    value = value.strip()
    value = re.sub(r"`([^`]+)`", r"\1", value)
    value = re.sub(r"\*\*([^*]+)\*\*", r"\1", value)
    value = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", value)
    return value.strip()


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


def split_sections(markdown: str) -> dict[str, str]:
    sections: dict[str, list[str]] = {}
    current = ""
    for line in markdown.splitlines():
        if line.startswith("## "):
            current = line[3:].strip()
            sections[current] = []
            continue
        if current:
            sections[current].append(line)
    return {key: "\n".join(lines).strip() for key, lines in sections.items()}


def extract_bullets(markdown: str, limit: int | None = None) -> list[str]:
    bullets: list[str] = []
    for line in markdown.splitlines():
        match = re.match(r"^\s*(?:[-*]|\d+\.)\s+(.*)$", line)
        if match:
            bullets.append(strip_inline_markdown(match.group(1)))
    return bullets[:limit] if limit else bullets


def extract_first_paragraph(markdown: str) -> str:
    for block in re.split(r"\n\s*\n", markdown.strip()):
        block = block.strip()
        if block and not block.startswith("- ") and not block.startswith("|"):
            return strip_inline_markdown(" ".join(block.splitlines()))
    return ""


def parse_tables(markdown: str) -> list[Table]:
    tables: list[Table] = []
    lines = markdown.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line.startswith("|") or i + 1 >= len(lines):
            i += 1
            continue
        separator = lines[i + 1].strip()
        if not re.match(r"^\|[\s:\-|]+\|$", separator):
            i += 1
            continue
        headers = [strip_inline_markdown(cell) for cell in line.strip("|").split("|")]
        rows: list[list[str]] = []
        i += 2
        while i < len(lines) and lines[i].strip().startswith("|"):
            cells = [strip_inline_markdown(cell) for cell in lines[i].strip().strip("|").split("|")]
            if len(cells) < len(headers):
                cells.extend([""] * (len(headers) - len(cells)))
            rows.append(cells[: len(headers)])
            i += 1
        tables.append(Table(headers=headers, rows=rows))
    return tables


def status_class(text: str) -> str:
    normalized = text.upper()
    if "RED" in normalized or "BLOCK" in normalized or "REQUIRED" in normalized:
        return "danger"
    if "YELLOW" in normalized or "PENDING" in normalized or "GATE" in normalized or "ACTION_DUE" in normalized:
        return "warn"
    if "DONE" in normalized or "PASS" in normalized or "APPROVED" in normalized:
        return "good"
    if "HOLD" in normalized or "READONLY" in normalized or "READ-ONLY" in normalized:
        return "neutral"
    return "plain"


def h(value: str) -> str:
    return html.escape(value, quote=True)


def render_list(items: list[str], *, numbered: bool = False) -> str:
    tag = "ol" if numbered else "ul"
    if not items:
        return '<p class="empty">No items captured.</p>'
    return f"<{tag}>" + "".join(f"<li>{h(item)}</li>" for item in items) + f"</{tag}>"


def render_score_rows(table: Table | None) -> str:
    if not table:
        return '<p class="empty">Scorecard table not found.</p>'
    index = {name: pos for pos, name in enumerate(table.headers)}
    cards = []
    for row in table.rows:
        surface = row[index.get("Surface", 0)]
        spend = row[index.get("Spend", 1)]
        clicks = row[index.get("Clicks", 2)]
        impressions = row[index.get("Impr.", 3)]
        purchases = row[index.get("Purchases", 4)]
        roas = row[index.get("ROAS", 6)]
        decision = row[index.get("Decision", 7)]
        cards.append(
            f"""
            <article class="metric-card {status_class(decision)}" data-status="{h(decision)}">
              <div class="metric-head">
                <h3>{h(surface)}</h3>
                <span>{h(decision)}</span>
              </div>
              <dl class="metric-grid">
                <div><dt>Spend</dt><dd>{h(spend)}</dd></div>
                <div><dt>Clicks</dt><dd>{h(clicks)}</dd></div>
                <div><dt>Impr.</dt><dd>{h(impressions)}</dd></div>
                <div><dt>Purchases</dt><dd>{h(purchases)}</dd></div>
                <div><dt>ROAS</dt><dd>{h(roas)}</dd></div>
              </dl>
            </article>
            """
        )
    return "\n".join(cards)


def render_action_rows(table: Table | None) -> str:
    if not table:
        return '<p class="empty">Action queue table not found.</p>'
    idx = {name: pos for pos, name in enumerate(table.headers)}
    rows = []
    for row in table.rows:
        priority = row[idx.get("Priority", 0)]
        status = row[idx.get("Status", 1)]
        action = row[idx.get("Action", 2)]
        owner = row[idx.get("Owner agent", 3)]
        gate = row[idx.get("Gate", 4)]
        rows.append(
            f"""
            <article class="queue-row {status_class(status)}" data-status="{h(status)}">
              <div class="row-top">
                <span class="priority">{h(priority)}</span>
                <span class="pill">{h(status)}</span>
                <span class="owner">{h(owner)}</span>
              </div>
              <h3>{h(action)}</h3>
              <p>{h(gate)}</p>
            </article>
            """
        )
    return "\n".join(rows)


def render_blocker_rows(table: Table | None) -> str:
    if not table:
        return '<p class="empty">Blocker table not found.</p>'
    idx = {name: pos for pos, name in enumerate(table.headers)}
    rows = []
    for row in table.rows:
        priority = row[idx.get("Priority", 0)]
        blocker = row[idx.get("Blocker", 1)]
        status = row[idx.get("Current compact status", 2)]
        next_action = row[idx.get("Next unblock action", 3)]
        rows.append(
            f"""
            <article class="blocker-card {status_class(priority + ' ' + status)}">
              <div class="row-top">
                <span class="priority">{h(priority)}</span>
                <span class="pill">{h(status.split(':', 1)[0])}</span>
              </div>
              <h3>{h(blocker)}</h3>
              <p>{h(next_action)}</p>
            </article>
            """
        )
    return "\n".join(rows)


def render_detail_list(items: list[str]) -> str:
    if not items:
        return '<p class="empty">Not captured yet.</p>'
    return "<ul>" + "".join(f"<li>{h(item)}</li>" for item in items) + "</ul>"


def render_campaign_explorer(data: dict, *, historical: bool = False) -> str:
    channels = data.get("channels", [])
    campaigns = data.get("campaigns", [])
    tabs = []
    for index, channel in enumerate(channels):
        tabs.append(
            f'<button class="channel-tab{" active" if index == 0 else ""}" type="button" '
            f'data-channel="{h(channel.get("id", ""))}">{h(channel.get("label", ""))}</button>'
        )

    cards = []
    panels = []
    for index, campaign in enumerate(campaigns):
        channel = campaign.get("channel", "")
        campaign_id = campaign.get("id", "")
        status = campaign.get("status_label", "")
        if historical:
            status = f"Historical: {status}"
        first_active = index == 0
        cards.append(
            f"""
            <button class="campaign-card {status_class(status)}{' active' if first_active else ''}" type="button"
              data-channel="{h(channel)}" data-campaign="{h(campaign_id)}">
              <span class="pill">{h(status)}</span>
              <strong>{h(campaign.get("name", ""))}</strong>
              <small>{h(campaign.get("campaign_name", ""))}</small>
            </button>
            """
        )
        panels.append(
            f"""
            <article class="campaign-detail{' active' if first_active else ''}" data-campaign-panel="{h(campaign_id)}">
              <div class="detail-head">
                <div>
                  <span class="eyebrow">{h(status)}</span>
                  <h3>{h(campaign.get("name", ""))}</h3>
                  <p>{h(campaign.get("running_state", ""))}</p>
                  <div class="decision-summary">
                    <div><span>Health</span><strong>{h(campaign.get("health_status", ""))}</strong></div>
                    <div><span>Activated</span><strong>{h(campaign.get("activated_at", ""))}</strong></div>
                    <div><span>Latest</span><strong>{h(campaign.get("latest_readback", ""))}</strong></div>
                    <div><span>Next decision</span><strong>{h(campaign.get("next_decision", ""))}</strong></div>
                  </div>
                </div>
                <dl class="detail-kpis">
                  <div><dt>Campaign ID</dt><dd>{h(campaign.get("campaign_id", ""))}</dd></div>
                  <div><dt>Budget</dt><dd>{h(campaign.get("budget", ""))}</dd></div>
                  <div><dt>Ad strength</dt><dd>{h(campaign.get("ad_strength", ""))}</dd></div>
                  <div><dt>Opt. score</dt><dd>{h(campaign.get("optimization_score", ""))}</dd></div>
                </dl>
              </div>
              <div class="detail-grid">
                <section class="detail-box wide priority-box">
                  <h4>Test Clock / Decision Deadline</h4>
                  <p><strong>Activated:</strong> {h(campaign.get("activated_at", ""))}</p>
                  <p><strong>Next decision:</strong> {h(campaign.get("next_decision", ""))}</p>
                  {render_detail_list(campaign.get("test_clock", []))}
                </section>
                <section class="detail-box">
                  <h4>{'Snapshot Metrics (Historical)' if historical else 'Today / Yesterday Metrics'}</h4>
                  {render_detail_list(campaign.get("metrics_snapshot", []))}
                </section>
                <section class="detail-box">
                  <h4>Success Measurement</h4>
                  {render_detail_list(campaign.get("success_measurement", []))}
                </section>
                <section class="detail-box">
                  <h4>Bid Strategy / Why</h4>
                  <p><strong>{h(campaign.get("bid_strategy_type", campaign.get("bid_strategy", "")))}</strong></p>
                  {render_detail_list(campaign.get("bid_strategy_reasoning", []))}
                </section>
                <section class="detail-box">
                  <h4>Bid Change Rules</h4>
                  {render_detail_list(campaign.get("bid_change_triggers", []))}
                </section>
                <section class="detail-box">
                  <h4>Improve / Change Triggers</h4>
                  {render_detail_list(campaign.get("improvement_triggers", []))}
                </section>
                <section class="detail-box">
                  <h4>Proactive Monitoring</h4>
                  {render_detail_list(campaign.get("proactive_monitoring", []))}
                </section>
                <section class="detail-box">
                  <h4>Assumptions To Test</h4>
                  {render_detail_list(campaign.get("assumptions", []))}
                </section>
                <section class="detail-box wide">
                  <h4>What We Are Aiming For</h4>
                  <p>{h(campaign.get("objective", ""))}</p>
                </section>
                <section class="detail-box">
                  <h4>Strategy / Agent Reasoning</h4>
                  {render_detail_list(campaign.get("strategy_reasoning", []))}
                </section>
                <section class="detail-box">
                  <h4>Active Objects</h4>
                  {render_detail_list(campaign.get("active_objects", []))}
                </section>
                <section class="detail-box">
                  <h4>Keywords / Targeting</h4>
                  {render_detail_list(campaign.get("keywords", []))}
                </section>
                <section class="detail-box">
                  <h4>Keyword Selection Criteria</h4>
                  {render_detail_list(campaign.get("keyword_selection_criteria", []))}
                </section>
                <section class="detail-box">
                  <h4>Keyword Economics / Low-Waste Test</h4>
                  {render_detail_list(campaign.get("keyword_economics", []))}
                </section>
                <section class="detail-box">
                  <h4>Anti-Cannibalization Rules</h4>
                  {render_detail_list(campaign.get("anti_cannibalization_rules", []))}
                </section>
                <section class="detail-box">
                  <h4>Negative Keyword Criteria</h4>
                  {render_detail_list(campaign.get("negative_keyword_strategy", []))}
                </section>
                <section class="detail-box wide">
                  <h4>2026 Expert Source Standard</h4>
                  {render_detail_list(campaign.get("expert_strategy_standard", []))}
                </section>
                <section class="detail-box">
                  <h4>Daily Owner / Optimization Loop</h4>
                  {render_detail_list(campaign.get("daily_optimization_owner", []))}
                </section>
                <section class="detail-box">
                  <h4>Continuous Improvement Rules</h4>
                  {render_detail_list(campaign.get("continuous_improvement_loop", []))}
                </section>
                <section class="detail-box">
                  <h4>Ads / Creative</h4>
                  {render_detail_list(campaign.get("ads", []))}
                </section>
                <section class="detail-box">
                  <h4>Quality Checks</h4>
                  {render_detail_list(campaign.get("quality_notes", []))}
                </section>
                <section class="detail-box wide">
                  <h4>Full Attention Checklist</h4>
                  {render_detail_list(campaign.get("full_quality_checklist", []))}
                </section>
                <section class="detail-box">
                  <h4>Human Verify</h4>
                  {render_detail_list(campaign.get("human_verify", []))}
                </section>
                <section class="detail-box wide">
                  <h4>Deadline / Next Check</h4>
                  <p>{h(campaign.get("deadline_or_next_check", ""))}</p>
                  <p class="risk-line">{h(campaign.get("blocked_or_risk", ""))}</p>
                </section>
                <section class="detail-box wide evidence-box">
                  <h4>Evidence</h4>
                  {render_detail_list(campaign.get("evidence", []))}
                </section>
              </div>
            </article>
            """
        )
    explorer = f"""
    <section class="panel span-12 campaign-explorer" data-filter-scope>
      <div class="section-head">
        <div>
          <h2>{'Historical Campaign Snapshots' if historical else 'Campaign Explorer'}</h2>
          <p>Pick Google Ads or Pinterest, then click a campaign to inspect the test clock, metrics, improvement triggers, active objects, targeting, anti-cannibalization, expert strategy, quality, evidence, and next checks.</p>
        </div>
        <div class="channel-tabs" role="tablist" aria-label="Marketing channels">
          {''.join(tabs)}
        </div>
      </div>
      <div class="campaign-layout">
        <nav class="campaign-list" aria-label="Campaign list">
          {''.join(cards)}
        </nav>
        <div class="campaign-panels">
          {''.join(panels)}
        </div>
      </div>
    </section>
    """
    if historical:
        return f"""
        <details class="panel span-12 historical-campaigns">
          <summary>Historical campaign snapshots — expand for reference only</summary>
          <p class="risk-line">Current campaign reconciliation is incomplete. These saved
          snapshots do not establish what is enabled, serving, spending, or approved now.
          Their status labels, budgets, metrics, and deadlines are historical. Use the
          dated current scorecard and authoritative control for present decisions.</p>
          {explorer}
        </details>
        """
    return explorer


def find_table(path: Path, header: str) -> Table | None:
    for table in parse_tables(read_text(path)):
        if header in table.headers:
            return table
    return None


def current_task_rows(markdown: str) -> list[dict[str, str]]:
    """Read the current task section, including table rows after blank lines.

    Historical tables and readiness colors must not become current task state.
    Missing presentation fields remain visibly unknown, never inferred as done.
    """
    if len(re.findall(r"^## Current turnaround tasks[^\n]*$", markdown, re.MULTILINE)) != 1:
        raise ValueError("Expected exactly one current turnaround task section")
    sections = split_sections(markdown)
    matches = [body for title, body in sections.items() if title.startswith("Current turnaround tasks")]
    if len(matches) != 1:
        raise ValueError("Expected exactly one current turnaround task section")
    headers: list[str] = []
    tasks: dict[str, dict[str, str]] = {}
    for line in matches[0].splitlines():
        if not line.startswith("|"):
            continue
        cells = [strip_inline_markdown(c) for c in line.strip().strip("|").split("|")]
        if "Action" in cells and "Owner agent" in cells:
            headers = cells
            continue
        if not headers or not re.search(r"\bTA-\d+\b", line):
            continue
        if len(cells) != len(headers):
            raise ValueError("Current task row has a mismatched column count")
        row = dict(zip(headers, cells))
        match = re.match(r"(TA-\d+)\b", row.get("Action", ""))
        if not match:
            raise ValueError("Current task action must start with a task ID")
        task_id = match.group(1)
        if task_id in tasks:
            raise ValueError(f"Duplicate current task: {task_id}")
        row["id"] = task_id
        tasks[task_id] = row
    if not tasks:
        raise ValueError("Current task section has no readable tasks")
    return sorted(tasks.values(), key=lambda r: (r.get("Priority", "P9"), int(r["id"].split("-")[1])))


def source_links(value: str) -> str:
    """Link only existing task evidence files; never synthesize external URLs."""
    packet = ROOT / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-05-ceo-turnaround"
    links = []
    for name in dict.fromkeys(re.findall(r"[A-Za-z0-9_-]+\.(?:md|json|csv)", value)):
        candidates = [MARKETING / name, packet / name]
        found = next((p for p in candidates if p.is_file()), None)
        if found is not None:
            rel = "../../" + found.relative_to(ROOT).as_posix()
            links.append(f'<a href="{h(rel)}">{h(name)}</a>')
    links.append('<a href="action_queue.md">Canonical task record</a>')
    return " ".join(links)


OWNER_STYLE = """
    .owner-desk { --accent: #205e51; color: #203d36; }
    .live-panel { display: flex; flex-wrap: wrap; align-items: center; gap: 10px 18px; border: 1px solid #cbd8d1; border-radius: 12px; background: #fff; padding: 12px 16px; margin: 0 0 22px; }
    .live-status { font-size: 12px; font-weight: 800; color: #766d53; }
    .live-status[data-state="online"] { color: #216b47; }
    .live-status[data-state="offline"], .live-status[data-state="error"] { color: #a43526; }
    .live-status::before { content: ''; display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: currentColor; margin-right: 7px; }
    .live-detail { flex: 1 1 240px; font-size: 12px; color: #61746b; }
    .live-controls { display: flex; gap: 12px; flex-wrap: wrap; align-items: center; }
    .live-controls label { font-size: 12px; display: flex; gap: 6px; align-items: center; min-height: 44px; }
    .live-handoffs { margin-top: 20px; border-top: 1px solid #d5ded6; padding-top: 10px; }
    .live-handoffs summary { cursor: pointer; min-height: 44px; padding: 12px 0; font-weight: 750; }
    .live-handoffs ol { list-style: none; padding: 0; margin: 0; display: grid; gap: 8px; }
    .live-handoffs li { border-left: 2px solid #c1d5c5; padding: 8px 12px; margin: 0; }
    .live-handoffs li strong { display: block; font-size: 13px; }
    .live-handoffs li span { display: block; font-size: 11px; color: #6b7c70; margin-top: 4px; overflow-wrap: anywhere; }
    #taskBoardStart { scroll-margin-top: 115px; }
    .owner-desk h2 { text-transform: none; letter-spacing: -.025em; font-size: 23px; color: #203d36; }
    .desk-eyebrow { font-size: 12px; text-transform: uppercase; letter-spacing: .1em; font-weight: 800; color: #63746d; }
    .desk-intro { display: flex; justify-content: space-between; gap: 24px; align-items: flex-end; margin: 6px 0 22px; }
    .desk-intro h2 { font-size: clamp(27px, 3vw, 40px); margin: 9px 0 8px; }
    .desk-intro p { color: #61746b; margin: 6px 0; max-width: 720px; }
    .desk-link, .desk-button { border: 1px solid #cbd8d1; border-radius: 9px; background: #fff; padding: 10px 14px; color: #244d40; font: inherit; font-size: 13px; font-weight: 700; cursor: pointer; text-decoration: none; min-height: 44px; }
    .desk-button.primary { background: #205e51; color: #fff; border-color: #205e51; }
    .desk-button:hover, .desk-link:hover { background: #edf3ef; }
    .desk-button.primary:hover { background: #194c41; }
    .owner-desk :focus-visible, #resumeDialog :focus-visible { outline: 3px solid #bc6319; outline-offset: 3px; }
    .desk-results { display: grid; grid-template-columns: repeat(5,minmax(0,1fr)); gap: 12px; }
    .desk-result { border: 1px solid #d9e1da; background: #fff; border-radius: 13px; padding: 18px; min-width: 0; }
    .desk-result:first-child { background: #eaf2e9; border-color: #c8d9c6; }
    .desk-result h3 { font-size: 12px; color: #67796f; margin: 0 0 10px; }
    .desk-result strong { display: block; font-size: 23px; letter-spacing: -.035em; line-height: 1.12; overflow-wrap: anywhere; }
    .desk-result p { font-size: 12px; color: #536b5f; line-height: 1.5; margin: 10px 0; }
    .desk-result small, .desk-meta { font-size: 11px; color: #6c7a74; overflow-wrap: anywhere; }
    .desk-note { color: #69776e; font-size: 12px; margin: 12px 0 22px; }
    .desk-next { background: #fff8e9; border: 1px solid #ebd8b5; border-radius: 13px; padding: 18px 20px; margin: 20px 0; display: grid; grid-template-columns: 150px 1fr auto; gap: 18px; align-items: center; }
    .desk-next h3 { margin: 4px 0; font-size: 15px; }
    .desk-next p { margin: 0; font-size: 14px; line-height: 1.55; }
    .desk-toolbar { display: flex; gap: 8px; flex-wrap: wrap; align-items: center; margin: 24px 0 14px; }
    .desk-tabs { display: flex; flex-wrap: wrap; gap: 5px; flex: 1 1 500px; }
    .desk-tabs button { background: transparent; border: 1px solid transparent; }
    .desk-tabs button[aria-pressed="true"] { background: #205e51; color: white; }
    .desk-inputs { display: flex; flex-wrap: wrap; gap: 10px; }
    .desk-inputs label { display: grid; gap: 4px; font-size: 11px; font-weight: 700; color: #61736b; }
    .desk-inputs input, .desk-inputs select { min-height: 44px; border: 1px solid #ced8d1; background: white; border-radius: 9px; padding: 10px 12px; font: inherit; font-size: 13px; max-width: 100%; }
    .desk-board { display: grid; grid-template-columns: repeat(3,minmax(0,1fr)); gap: 14px; align-items: start; }
    .desk-task { background: #fff; border: 1px solid #d9e1da; border-radius: 13px; padding: 19px; min-width: 0; scroll-margin-top: 20px; }
    .desk-task[data-owner="Manual action"] { border-top: 3px solid #b87823; }
    .desk-task[data-stage="Verification remaining"] { border-top: 3px solid #589681; }
    .desk-task h3 { font-size: 16px; line-height: 1.4; letter-spacing: -.015em; margin: 12px 0; color: #233e33; overflow-wrap: anywhere; }
    .desk-task p { font-size: 13px; line-height: 1.6; margin: 8px 0; overflow-wrap: anywhere; }
    .desk-task-top { display: flex; justify-content: space-between; gap: 8px; align-items: center; }
    .desk-id { font-size: 11px; font-weight: 800; color: #597267; }
    .desk-badge { display: inline-flex; font-size: 10px; font-weight: 750; border-radius: 5px; padding: 4px 7px; background: #edf2ee; color: #476350; }
    .desk-badge.attention { background: #fff0d8; color: #865b1e; }
    .desk-progress { border-left: 2px solid #b8d1bf; padding-left: 12px; margin: 15px 0; }
    .desk-progress strong, .desk-nextstep strong { font-size: 10px; color: #657b6d; letter-spacing: .04em; text-transform: uppercase; }
    .desk-progress p { color: #496653; }
    .desk-board[data-view="milestones"] .desk-nextstep { display: none; }
    .desk-board[data-view="milestones"] .desk-progress { background: #f0f5ef; border-radius: 6px; padding: 12px; }
    .desk-nextstep { background: #f6f7f2; padding: 12px; border-radius: 8px; }
    .desk-task summary { cursor: pointer; min-height: 44px; padding: 13px 0; color: #476c59; font-size: 12px; font-weight: 700; }
    .desk-task details { font-size: 12px; }
    .desk-task details p { font-size: 12px; }
    .desk-sources { display: grid; gap: 6px; padding: 9px 0; }
    .desk-sources a { font-size: 11px; color: #205e51; overflow-wrap: anywhere; }
    .desk-footer-row { display: flex; align-items: center; justify-content: space-between; gap: 10px; margin-top: 15px; }
    .desk-empty { border: 1px dashed #bdcabc; padding: 30px; border-radius: 12px; color: #576d5d; }
    .desk-team { display: grid; grid-template-columns: repeat(4,minmax(0,1fr)); gap: 12px; margin: 15px 0; }
    .desk-team article { border: 1px solid #d9e1da; background: #fff; border-radius: 12px; padding: 17px; }
    .desk-team h3 { margin: 0 0 8px; font-size: 15px; }
    .desk-team p { font-size: 13px; line-height: 1.6; }
    .desk-method { margin-top: 28px; padding: 0; }
    .desk-method summary { cursor: pointer; min-height: 44px; font-size: 15px; font-weight: 700; padding: 14px 0; }
    .desk-method ol { max-width: 1000px; font-size: 14px; line-height: 1.7; }
    .legacy { margin-top: 25px; border-top: 1px solid #cbd6cb; padding-top: 18px; }
    .legacy > summary { cursor: pointer; min-height: 44px; font-weight: 700; color: #536b5c; }
    .legacy-controls { padding: 12px 0 22px; }
    #resumeDialog { width: min(720px,calc(100vw - 32px)); max-height: calc(100vh - 40px); border: 1px solid #b6cbbc; border-radius: 16px; padding: 24px; color: #244436; }
    #resumeDialog::backdrop { background: #152f2670; }
    #resumeDialog textarea { display: block; width: 100%; min-height: 270px; max-height: 50vh; margin: 14px 0; border: 1px solid #bbcfc1; border-radius: 8px; padding: 12px; font-size: 13px; line-height: 1.5; }
    #resumeDialog .dialog-actions { display: flex; flex-wrap: wrap; gap: 10px; }
    .owner-desk [hidden] { display: none !important; }
    @media(max-width: 1120px) { .desk-results { grid-template-columns: repeat(3,minmax(0,1fr)); } .desk-board { grid-template-columns: repeat(2,minmax(0,1fr)); } .desk-team { grid-template-columns: repeat(2,minmax(0,1fr)); } }
    @media(max-width: 720px) { .desk-intro { display: block; } .desk-intro .desk-link { display: inline-block; margin-top: 10px; } .desk-results { grid-template-columns: repeat(2,minmax(0,1fr)); } .desk-result:first-child { grid-column: 1 / -1; } .desk-board,.desk-team { grid-template-columns: 1fr; } .desk-next { grid-template-columns: 1fr; gap: 10px; } .desk-next .desk-button { justify-self: start; } .desk-inputs { width: 100%; } .desk-inputs label { flex: 1 1 130px; min-width: 0; } .desk-inputs input { width: 100%; } .desk-result { padding: 14px; } .desk-tabs { gap: 2px; } .desk-tabs .desk-button { font-size: 12px; padding: 10px; } }
"""


LIVE_SCRIPT = """
(() => {
  const badge = document.getElementById('liveStatus');
  const detail = document.getElementById('liveDetail');
  const auto = document.getElementById('liveAuto');
  const check = document.getElementById('liveCheck');
  const updates = document.getElementById('liveHandoffs');
  const localService = location.protocol === 'http:' && location.hostname === '127.0.0.1';
  let pageRevision = document.querySelector('meta[name="dlm-dashboard-revision"]')?.content || '';
  let busy = false, timer, lastGoodCheck = null;
  const when = value => { const date = new Date(value); return Number.isFinite(date.getTime()) ? date.toLocaleString() : 'not recorded'; };
  try {
    auto.checked = localStorage.getItem('dlm-live-auto') !== 'false';
    const saved = JSON.parse(sessionStorage.getItem('dlm-live-position') || 'null');
    sessionStorage.removeItem('dlm-live-position');
    if (saved) {
      for (const id of saved.openTasks || []) document.querySelector(`#${CSS.escape(id)} details`)?.setAttribute('open', '');
      if (saved.handoffsOpen) document.getElementById('teamHandoffs').open = true;
      requestAnimationFrame(() => window.scrollTo(0, Number(saved.y) || 0));
    }
  } catch {}
  if (!localService) {
    badge.textContent = 'Saved file';
    detail.textContent = 'Open the live dashboard for automatic updates.';
    auto.disabled = true;
    check.textContent = 'Open live dashboard';
    check.addEventListener('click', () => location.assign('http://127.0.0.1:8767/'));
    return;
  }
  function keepPositionAndReload() {
    try { sessionStorage.setItem('dlm-live-position', JSON.stringify({y:scrollY, openTasks:[...document.querySelectorAll('.desk-task details[open]')].map(d=>d.closest('.desk-task').id),handoffsOpen:document.getElementById('teamHandoffs').open})); } catch {}
    location.reload();
  }
  function showHandoffs(items) {
    const nodes = (Array.isArray(items) ? items : []).slice(0, 6).map(item => {
      const row = document.createElement('li');
      const title = document.createElement('strong');
      title.textContent = String(item.title || 'Recorded handoff');
      const evidence = document.createElement('span');
      evidence.textContent = [item.date, ...(Array.isArray(item.task_ids) ? item.task_ids : []), item.anchor].filter(Boolean).join(' · ');
      row.append(title, evidence); return row;
    });
    if (!nodes.length) { const row = document.createElement('li'); row.textContent = 'No recent handoffs recorded.'; nodes.push(row); }
    updates.replaceChildren(...nodes);
  }
  async function poll(forceRefresh = false) {
    if (busy) return;
    busy = true; clearTimeout(timer);
    try {
      const response = await fetch('/api/status', {cache:'no-store',signal:AbortSignal.timeout(4000)});
      if (!response.ok) throw new Error('Status unavailable');
      const status = await response.json();
      if (status.service !== 'dlm-growth-dashboard' || !status.online) throw new Error('Unexpected service');
      lastGoodCheck = new Date();
      if (status.content_error) {
        badge.dataset.state = 'error'; badge.textContent = 'Source needs attention';
        detail.textContent = 'The last good view is retained. A source record could not be rendered; current updates are not confirmed.';
        return;
      }
      if (typeof status.revision !== 'string' || !status.revision) throw new Error('Invalid source revision');
      badge.dataset.state = 'online'; badge.textContent = 'Live view connected';
      detail.textContent = `Checked ${lastGoodCheck.toLocaleTimeString()} · Latest record change ${when(status.last_source_change_at)}. Business evidence keeps its own dates.`;
      showHandoffs(status.recent_handoffs);
      if (!pageRevision || status.revision !== pageRevision) {
        const interaction = document.getElementById('resumeDialog').open || ['INPUT','SELECT','TEXTAREA'].includes(document.activeElement.tagName);
        if ((auto.checked || forceRefresh) && !interaction) { keepPositionAndReload(); return; }
        badge.textContent = 'Updates ready';
        detail.textContent = 'New source changes are ready. Finish the open control or click Check for updates to refresh the view.';
      }
    } catch {
      badge.dataset.state = 'offline'; badge.textContent = 'Connection interrupted';
      detail.textContent = `Showing the saved view. ${lastGoodCheck ? 'Last connected '+lastGoodCheck.toLocaleTimeString()+'. ' : ''}Retrying automatically; this does not indicate whether agents or campaigns stopped.`;
    } finally {
      busy = false;
      timer = setTimeout(() => poll(), document.hidden ? 15000 : 5000);
    }
  }
  auto.addEventListener('change', () => { try { localStorage.setItem('dlm-live-auto',String(auto.checked)); } catch {} poll(); });
  check.addEventListener('click', () => poll(true));
  document.addEventListener('visibilitychange', () => { if (!document.hidden) poll(); });
  window.addEventListener('focus', () => poll());
  poll();
})();
"""


OWNER_SCRIPT = """
(() => {
  const cards = [...document.querySelectorAll('.desk-task')];
  const buttons = [...document.querySelectorAll('[data-desk-view]')];
  const query = document.getElementById('taskSearch');
  const lane = document.getElementById('taskLane');
  const count = document.getElementById('taskCount');
  let view = 'all';
  const matchesView = (card, target) => {
    if (target === 'owner') return ['Access','Manual action','Information','Revision'].includes(card.dataset.owner);
    if (target === 'blocked') return ['Needs access','Needs evidence','Waiting on dependency','Needs owner information'].includes(card.dataset.stage);
    if (target === 'verify') return card.dataset.stage === 'Verification remaining';
    if (target === 'milestones') return card.dataset.milestone === 'yes';
    return true;
  };
  function filter() {
    let visible = 0;
    cards.forEach(card => {
      const show = matchesView(card, view) && (!query.value || card.textContent.toLowerCase().includes(query.value.toLowerCase())) && (!lane.value || card.dataset.lane.includes(lane.value));
      card.hidden = !show;
      if (show) visible++;
    });
    buttons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.deskView === view)));
    count.textContent = `${visible} of ${cards.length} tasks · ${view === 'milestones' ? 'Recorded milestones; parent tasks still have remaining work.' : 'Saved checkpoints; assigned roles do not indicate running agents.'}`;
    document.querySelector('.desk-board').dataset.view = view;
    document.getElementById('ownerInputHelp').hidden = view !== 'owner';
    document.getElementById('taskEmpty').hidden = visible > 0;
    try { localStorage.setItem('dlm-owner-view', JSON.stringify({ view, query: query.value, lane: lane.value })); } catch {}
  }
  buttons.forEach(button => button.addEventListener('click', () => { view = button.dataset.deskView; filter(); }));
  query.addEventListener('input', filter);
  lane.addEventListener('change', filter);
  document.getElementById('taskReset').addEventListener('click', () => { query.value = ''; lane.value = ''; view = 'all'; filter(); });
  document.querySelectorAll('[data-owner-jump]').forEach(button => button.addEventListener('click', () => { view = 'owner'; query.value = ''; lane.value = ''; filter(); document.getElementById('taskBoardStart').scrollIntoView({behavior:'smooth'}); }));
  try {
    const saved = JSON.parse(localStorage.getItem('dlm-owner-view') || '{}');
    if (buttons.some(b => b.dataset.deskView === saved.view)) view = saved.view;
    query.value = typeof saved.query === 'string' ? saved.query : '';
    lane.value = [...lane.options].some(o => o.value === saved.lane) ? saved.lane : '';
  } catch {}
  filter();
  const payload = JSON.parse(document.getElementById('deskHandoffData').textContent);
  const dialog = document.getElementById('resumeDialog');
  const textarea = document.getElementById('resumeText');
  let trigger;
  document.querySelectorAll('[data-resume-task]').forEach(button => button.addEventListener('click', () => {
    trigger = button;
    const id = button.dataset.resumeTask;
    document.getElementById('resumeTitle').textContent = `Continue ${id}`;
    textarea.value = payload.prompt + '\\n\\nTask context: ' + id + '. Use its current row in ops/marketing/action_queue.md and current evidence. Preserve completed milestones. The dashboard is a saved checkpoint, not authority or a fresh account readback.';
    document.getElementById('copyResult').textContent = 'Paste into the existing Dress Like Mommy growth task. This does not start an agent or approve an action.';
    dialog.showModal();
    textarea.focus();
    textarea.setSelectionRange(0, 0);
    textarea.scrollTop = 0;
  }));
  document.getElementById('closeResume').addEventListener('click', () => dialog.close());
  dialog.addEventListener('close', () => trigger?.focus());
  document.getElementById('copyResume').addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(textarea.value);
      document.getElementById('copyResult').textContent = 'Copied. Paste into your existing growth task to continue.';
    } catch {
      textarea.focus(); textarea.select();
      document.getElementById('copyResult').textContent = 'Text selected. Use your usual Copy shortcut; clipboard access is unavailable here.';
    }
  });
})();
"""


def render_owner_view(tasks: list[dict[str, str]], sections: dict[str, str], updated: str) -> str:
    cards = []
    counts = {
        "all": len(tasks),
        "owner": sum(t.get("Owner input") in {"Access", "Manual action", "Information", "Revision"} for t in tasks),
        "blocked": sum(t.get("Checkpoint") in {"Needs access", "Needs evidence", "Waiting on dependency", "Needs owner information"} for t in tasks),
        "verify": sum(t.get("Checkpoint") == "Verification remaining" for t in tasks),
        "milestones": sum(bool(t.get("Completed milestone")) for t in tasks),
    }
    for task in tasks:
        get = lambda key: task.get(key) or "Not recorded — inspect canonical task"
        needs = get("Owner input")
        title = task.get("Task title") or re.sub(r"^TA-\d+\s*", "", get("Action"))
        business_result = task.get("Business result") or "No measured task-level traffic, sales or retained-profit effect is recorded in this row."
        cards.append(f'''<article class="desk-task" id="{h(task['id'])}" data-stage="{h(get('Checkpoint'))}" data-owner="{h(needs)}" data-lane="{h(get('Lane').lower())}" data-milestone="{'yes' if task.get('Completed milestone') else 'no'}">
          <div class="desk-task-top"><span class="desk-id">{h(task['id'])} · {h(get('Priority'))}</span><span class="desk-badge">{h(get('Checkpoint'))}</span></div>
          <h3>{h(title)}</h3><span class="desk-meta">{h(get('Lane'))}</span>
          <div class="desk-progress"><strong>Recorded milestone</strong><p>{h(get('Completed milestone'))}</p></div>
          <div class="desk-nextstep"><strong>Next / still missing</strong><p>{h(get('Next step'))}</p></div>
          <p><span class="desk-badge {'attention' if needs != 'None' else ''}">Owner input: {h(needs)}</span></p>
          <details><summary>Owner, evidence &amp; finish conditions</summary>
            <p><b>Responsible:</b> {h(get('Owner agent'))}</p>
            <p><b>Remaining conditions:</b> {h(get('Gate'))}</p>
            <p><b>Execution gate:</b> {h(get('Status'))}. Task progress does not grant live authority.</p>
            <p><b>Business impact:</b> {h(business_result)}</p>
            <div class="desk-sources">{source_links(get('Evidence/source'))}</div>
          </details>
          <div class="desk-footer-row"><span class="desk-meta">Recorded {h(get('Checkpoint date'))}</span><button class="desk-button" data-resume-task="{h(task['id'])}">Continue {h(task['id'])}</button></div>
        </article>''')
    results = []
    result_table = find_table(MARKETING / "daily_scorecard.md", "Metric")
    if result_table:
        for cells in result_table.rows:
            row = dict(zip(result_table.headers, cells))
            results.append(f'''<article class="desk-result"><h3>{h(row.get('Metric','Unknown'))}</h3><strong>{h(row.get('Value','UNKNOWN'))}</strong><p>{h(row.get('Meaning',''))}</p><small>{h(row.get('Evidence as of','Date unavailable'))}</small></article>''')
    else:
        results.append('<p class="desk-empty">Current results are not recorded. Inspect the dated scorecard; no zero or profit estimate is inferred.</p>')
    prompt_source = read_text(ROOT / "ops/prompts/paid-growth-ai-army-continuation-prompt.md")
    prompt_match = re.search(r"```text\n(.*?)\n```", prompt_source, re.DOTALL)
    if not prompt_match:
        raise ValueError("Canonical continuation prompt is missing")
    payload = json.dumps({"prompt": prompt_match.group(1)}).replace("<", "\\u003c")
    tabs = "".join(f'<button class="desk-button" data-desk-view="{key}" aria-pressed="{str(key == "all").lower()}">{label} <span>{counts[key]}</span></button>' for key, label in [('all','All tasks'),('owner','Needs you'),('blocked','Blocked / dependencies'),('verify','Verify next'),('milestones','Milestones')])
    owner_action = extract_first_paragraph(sections.get("One Owner Action", ""))
    owner_counts = {kind: sum(t.get("Owner input") == kind for t in tasks) for kind in ['Access', 'Manual action', 'Information', 'Revision', 'Future approval']}
    owner_help = ' · '.join(f'{kind}: {amount}' for kind, amount in owner_counts.items()) + '. Shared access can unblock several tasks. Future approvals still depend on preparation; inspect the exact record before requesting a decision.'
    return f'''<div class="owner-desk">
      <div class="live-panel" aria-label="Live dashboard connection"><span id="liveStatus" class="live-status" data-state="waiting" aria-live="polite">Connecting to local view</span><span id="liveDetail" class="live-detail">Checking service and source freshness…</span><div class="live-controls"><label><input id="liveAuto" type="checkbox" checked> Auto-update view</label><button id="liveCheck" class="desk-button">Check for updates</button></div></div>
      <div class="desk-intro"><div><span class="desk-eyebrow">Dress Like Mommy / Owner workspace</span><h2>See the work. Grow the profit.</h2><p>Free traffic, paid traffic and the steps that turn visits into profitable orders.</p></div><a class="desk-link" href="daily_scorecard.md">Read the result evidence</a></div>
      <div class="desk-results">{''.join(results)}</div>
      <p class="desk-note">Task changes update automatically in the live view. Business metrics use the dated evidence shown above. Page built {h(updated)}. Task milestones do not establish traffic or profit lift. Target: 30% retained profit, with paid ROAS as a supporting measure.</p>
      <div class="desk-next"><div><span class="desk-eyebrow">First unblock</span><h3>Next owner action</h3></div><p>{h(owner_action or 'No owner action recorded; inspect current task evidence.')} <span class="desk-meta">Saved owner request; this dashboard does not recheck its live status.</span></p><button id="showOwner" data-owner-jump class="desk-button primary">See what needs me</button></div>
      <div id="taskBoardStart"><h2>Your growth work</h2><p class="desk-note">A completed step stays visible even when publication, verification or measurement is still missing. No completion percentages are guessed.</p></div>
      <div class="desk-toolbar"><div class="desk-tabs" aria-label="Task views">{tabs}</div><div class="desk-inputs"><label>Find a task<input id="taskSearch" type="search" placeholder="Task, channel or blocker"></label><label>Growth lane<select id="taskLane"><option value="">All lanes</option><option value="free">Free traffic</option><option value="paid">Paid traffic</option><option value="store">Store conversion</option><option value="measurement">Measurement &amp; profit</option><option value="coordination">Coordination</option></select></label></div></div>
      <p id="taskCount" class="desk-note" aria-live="polite"></p><p id="ownerInputHelp" class="desk-note" hidden>{h(owner_help)}</p><div id="taskEmpty" class="desk-empty" hidden>No tasks match this view. <button id="taskReset" class="desk-button">Clear filters</button></div>
      <div class="desk-board">{''.join(cards)}</div>
      <details id="teamHandoffs" class="live-handoffs"><summary>Team handoffs and recent progress</summary><p class="desk-note">Updates come from the shared worklog and task records. Internal agent messages stay with the agents; decisions and results are preserved here. Running-agent status is not connected to this view.</p><ol id="liveHandoffs"><li>Connect to the live service to see recent recorded handoffs.</li></ol></details>
      <details class="desk-method"><summary>How we work toward sales and profit</summary>
        <p>Recommended trial: one accountable growth lead, specialists on demand, and at most two active execution items. Start with a free-traffic deliverable and a paid/measurement prerequisite. These are assigned roles, not always-running agents.</p>
        <div class="desk-team"><article><h3>Free acquisition</h3><p>SEO, free product listings and organic posts. Finish at a verified customer entry point, then measure qualified visits and orders.</p></article><article><h3>Paid acquisition</h3><p>Google, Microsoft and Pinterest operators. Qualify an offer and its measurement before an exact bounded test.</p></article><article><h3>Store conversion</h3><p>Product clarity, localization and cart journeys. Fix a demonstrated buying obstacle and verify the shopper path.</p></article><article><h3>Measurement &amp; profit</h3><p>Same-window orders, expenses and channel performance. Reconcile actual retained profit and decide hold, stop or scale.</p></article></div>
        <ol><li>Pick a small deliverable with a finish line, owner and dated baseline.</li><li>Finish preparation, execute within existing authority, and verify the actual result. Preserve missing steps in the same task.</li><li>Request a concrete decision only when needed. Manual publication, access and missing facts stay distinct from approval.</li><li>Measure purchases and retained profit in a declared window. Published work is an operational milestone; profit remains a separate result.</li><li>At handoff update the existing task row and worklog. The local service refreshes this view. Continue from the task ID and its evidence.</li></ol>
        <p><a href="operator_cockpit.md">Full working proposal and Zenith assessment</a> · <a href="team_registry.md">Existing specialist roles</a> · <a href="../prompts/paid-growth-ai-army-continuation-prompt.md">Canonical continuation prompt</a></p>
      </details>
      <dialog id="resumeDialog" aria-labelledby="resumeTitle"><h2 id="resumeTitle">Continue task</h2><p id="copyResult" aria-live="polite"></p><label for="resumeText">Canonical continuation prompt with task context</label><textarea id="resumeText" readonly></textarea><div class="dialog-actions"><button id="copyResume" class="desk-button primary">Copy continuation</button><button id="closeResume" class="desk-button">Close</button></div></dialog>
      <script type="application/json" id="deskHandoffData">{payload}</script>
    </div>'''


def build_html() -> str:
    cockpit_md = read_text(MARKETING / "operator_cockpit.md")
    sections = split_sections(cockpit_md)
    score_table = find_table(MARKETING / "daily_scorecard.md", "Surface")
    action_table = find_table(MARKETING / "action_queue.md", "Action")
    blocker_table = find_table(MARKETING / "blocker_board.md", "Blocker")
    spend_text = read_text(MARKETING / "spend_authorization.md")
    state_text = read_text(MARKETING / "current_marketing_state.md")
    authoritative_control = parse_authoritative_control(state_text)
    campaign_data = json.loads(read_text(MARKETING / "campaign_explorer.json"))
    updated = dt.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M %Z")
    owner_tasks = current_task_rows(read_text(MARKETING / "action_queue.md"))
    owner_view = render_owner_view(owner_tasks, sections, updated)
    if action_table:
        action_table = Table(action_table.headers, [[task.get(key, "") for key in action_table.headers] for task in owner_tasks])

    current_goal = extract_first_paragraph(sections.get("Current Goal", ""))
    owner_action = extract_first_paragraph(sections.get("One Owner Action", ""))
    success_measure = extract_first_paragraph(sections.get("Success Measure", ""))
    expert_standard = extract_first_paragraph(sections.get("Expert Strategy Standard", ""))
    done_today = extract_bullets(sections.get("Done Today", ""))
    local_changes = extract_bullets(sections.get("Local Changes", ""))
    live_changes = extract_bullets(sections.get("Live Changes", ""))
    next_tasks = extract_bullets(sections.get("Next 3 Tasks", ""), limit=3)
    assumptions = extract_bullets(sections.get("Assumptions", ""))
    risks = extract_bullets(sections.get("Risks / Approval Needed", ""))
    if "APPROVED_ACTIVE" in spend_text:
        spend_status = "APPROVED_ACTIVE"
    elif "PENDING_OWNER_APPROVAL" in spend_text:
        spend_status = "PENDING_OWNER_APPROVAL"
    else:
        spend_status = "CHECK FILE"
    # A historical verdict in the append-only log is not a current-scope review.
    reviewer_verdict = "SEE LATEST DATED REVIEW"
    live_state_mode = authoritative_control.get("live_state_mode", "MISSING_CONTROL")
    effective_approval_policy = authoritative_control.get(
        "effective_approval_policy",
        "CHECK_CURRENT_MARKETING_STATE",
    )
    authoritative_next = authoritative_control.get(
        "next_best_action",
        next_tasks[0] if next_tasks else "CHECK_CURRENT_MARKETING_STATE",
    )
    fail_closed = live_state_mode != "LIVE_CURRENT"
    control_class = "danger" if fail_closed else "good"
    approval_class = (
        "danger"
        if effective_approval_policy == "FRESH_ACTION_TIME_APPROVAL_REQUIRED"
        else status_class(effective_approval_policy)
    )
    spend_class = "neutral" if fail_closed else status_class(spend_status)
    authoritative_risk = (
        "Historical readiness is not current action authority; complete read-only reconciliation first."
        if fail_closed
        else (risks[0] if risks else "No risk captured")
    )

    output = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#205e51">
  <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='16' fill='%23205e51'/%3E%3Ctext x='32' y='41' text-anchor='middle' font-family='Arial' font-weight='bold' font-size='24' fill='white'%3EDLM%3C/text%3E%3C/svg%3E">
  <title>Dress Like Mommy · Growth Dashboard</title>
  <style>
    :root {{
      color-scheme: light;
      --ink: #19202a;
      --muted: #667084;
      --line: #dbe2eb;
      --paper: #f7f9fc;
      --panel: #ffffff;
      --blue: #265cff;
      --teal: #087f8c;
      --green: #147a3d;
      --amber: #9a5b00;
      --red: #b42318;
      --lav: #6658d3;
      --shadow: 0 18px 50px rgba(35, 48, 73, 0.12);
    }}
    * {{ box-sizing: border-box; }}
    html {{ overflow-x: hidden; }}
    body {{
      margin: 0;
      background: var(--paper);
      color: var(--ink);
      font: 15px/1.45 Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      overflow-x: hidden;
      max-width: 100vw;
    }}
    h1, h2, h3, p, li, span, strong, dd {{ overflow-wrap: anywhere; }}
    h1, h2, h3, p, li, span, strong, dd {{ word-break: normal; }}
    a {{ color: inherit; }}
    .shell {{ min-height: 100vh; }}
    header {{
      background: #ffffff;
      border-bottom: 1px solid var(--line);
      position: sticky;
      top: 0;
      z-index: 10;
    }}
    .topbar {{
      display: grid;
      grid-template-columns: minmax(260px, 1fr) auto;
      gap: 20px;
      align-items: center;
      max-width: 1480px;
      margin: 0 auto;
      padding: 18px 24px;
      min-width: 0;
    }}
    .brand h1 {{
      margin: 0;
      font-size: 23px;
      letter-spacing: 0;
    }}
    .brand p {{ margin: 3px 0 0; color: var(--muted); }}
    .controls {{
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
      justify-content: flex-end;
      min-width: 0;
    }}
    .search {{
      width: min(360px, 42vw);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 10px 12px;
      font: inherit;
      background: #fff;
      max-width: 100%;
    }}
    .toggle {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 9px 12px;
      background: #fff;
      color: var(--muted);
      white-space: nowrap;
    }}
    main {{
      max-width: 1480px;
      margin: 0 auto;
      padding: 24px;
      min-width: 0;
    }}
    .hero {{
      display: grid;
      grid-template-columns: minmax(0, 1.5fr) minmax(300px, 0.8fr);
      gap: 18px;
      margin-bottom: 18px;
    }}
    .panel {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      box-shadow: var(--shadow);
      min-width: 0;
    }}
    .goal {{
      padding: 24px;
      display: grid;
      align-content: space-between;
      min-height: 220px;
      min-width: 0;
    }}
    .goal h2, section h2 {{
      margin: 0;
      font-size: 17px;
      letter-spacing: 0;
    }}
    .goal p.big {{
      margin: 14px 0;
      max-width: 820px;
      font-size: 26px;
      line-height: 1.16;
      font-weight: 750;
    }}
    .chips {{ display: flex; flex-wrap: wrap; gap: 8px; }}
    .chip, .pill, .priority {{
      display: inline-flex;
      align-items: center;
      min-height: 28px;
      border-radius: 8px;
      padding: 5px 9px;
      font-size: 12px;
      font-weight: 750;
      border: 1px solid var(--line);
      background: #fff;
      max-width: 100%;
      white-space: normal;
    }}
    .chip.danger, .danger .pill {{ color: var(--red); background: #fff4f2; border-color: #ffd4ce; }}
    .chip.warn, .warn .pill {{ color: var(--amber); background: #fff8e6; border-color: #ffe1a6; }}
    .chip.good, .good .pill {{ color: var(--green); background: #eefbf2; border-color: #bfe8cb; }}
    .chip.neutral, .neutral .pill {{ color: var(--teal); background: #effbfc; border-color: #bce8ed; }}
    .status-board {{
      padding: 18px;
      display: grid;
      gap: 12px;
    }}
    .status-tile {{
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 14px;
      background: #fbfcfe;
    }}
    .status-tile span {{
      display: block;
      color: var(--muted);
      font-size: 12px;
      text-transform: uppercase;
      font-weight: 800;
    }}
    .status-tile strong {{
      display: block;
      margin-top: 5px;
      font-size: 18px;
    }}
    .grid {{
      display: grid;
      gap: 18px;
      grid-template-columns: repeat(12, 1fr);
      align-items: start;
      min-width: 0;
    }}
    section {{
      padding: 18px;
    }}
    .span-12 {{ grid-column: span 12; }}
    .span-7 {{ grid-column: span 7; }}
    .span-5 {{ grid-column: span 5; }}
    .span-4 {{ grid-column: span 4; }}
    .section-head {{
      display: flex;
      justify-content: space-between;
      gap: 12px;
      align-items: baseline;
      margin-bottom: 14px;
    }}
    .section-head > div {{ min-width: 0; }}
    .section-head p {{ margin: 0; color: var(--muted); }}
    .campaign-explorer .section-head {{
      align-items: center;
    }}
    .channel-tabs {{
      display: inline-flex;
      gap: 6px;
      padding: 4px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #f8fafc;
      flex-wrap: wrap;
    }}
    .channel-tab {{
      border: 0;
      border-radius: 7px;
      padding: 8px 12px;
      background: transparent;
      color: var(--muted);
      font: inherit;
      font-weight: 800;
      cursor: pointer;
    }}
    .channel-tab.active {{
      background: #fff;
      color: var(--blue);
      box-shadow: 0 4px 14px rgba(31, 45, 74, 0.11);
    }}
    .campaign-layout {{
      display: grid;
      grid-template-columns: minmax(260px, 0.34fr) minmax(0, 1fr);
      gap: 14px;
      align-items: start;
    }}
    .campaign-list {{
      display: grid;
      gap: 10px;
      max-height: 760px;
      overflow: auto;
      padding-right: 4px;
    }}
    .campaign-card {{
      width: 100%;
      border: 1px solid var(--line);
      border-left: 5px solid var(--blue);
      border-radius: 8px;
      background: #fff;
      padding: 13px;
      text-align: left;
      cursor: pointer;
      font: inherit;
      display: grid;
      gap: 8px;
    }}
    .campaign-card.danger {{ border-left-color: var(--red); }}
    .campaign-card.warn {{ border-left-color: var(--amber); }}
    .campaign-card.good {{ border-left-color: var(--green); }}
    .campaign-card.neutral {{ border-left-color: var(--teal); }}
    .campaign-card.active {{
      outline: 2px solid rgba(38, 92, 255, 0.32);
      box-shadow: 0 12px 28px rgba(38, 92, 255, 0.12);
    }}
    .campaign-card strong {{
      font-size: 15px;
      line-height: 1.2;
    }}
    .campaign-card small {{
      color: var(--muted);
      font-size: 12px;
      line-height: 1.25;
    }}
    .campaign-detail {{
      display: none;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #fff;
      padding: 18px;
    }}
    .campaign-detail.active {{ display: block; }}
    .detail-head {{
      display: grid;
      grid-template-columns: minmax(0, 1fr) minmax(280px, 0.62fr);
      gap: 18px;
      align-items: start;
      padding-bottom: 16px;
      border-bottom: 1px solid var(--line);
    }}
    .eyebrow {{
      display: inline-block;
      color: var(--teal);
      font-size: 12px;
      font-weight: 850;
      text-transform: uppercase;
      margin-bottom: 6px;
    }}
    .detail-head h3 {{
      margin: 0;
      font-size: 24px;
      line-height: 1.12;
    }}
    .detail-head p {{
      margin: 8px 0 0;
      color: var(--muted);
      font-weight: 650;
    }}
    .decision-summary {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 8px;
      margin-top: 12px;
    }}
    .decision-summary div {{
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 9px 10px;
      background: #fffaf0;
      min-width: 0;
    }}
    .decision-summary span {{
      display: block;
      color: var(--amber);
      font-size: 11px;
      text-transform: uppercase;
      font-weight: 850;
    }}
    .decision-summary strong {{
      display: block;
      margin-top: 3px;
      font-size: 13px;
      line-height: 1.25;
    }}
    .detail-kpis {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 10px;
      margin: 0;
    }}
    .detail-kpis div {{
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 11px;
      background: #fbfcfe;
      min-width: 0;
    }}
    .detail-kpis dd {{
      font-size: 15px;
      overflow-wrap: anywhere;
    }}
    .detail-grid {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 12px;
      padding-top: 16px;
    }}
    .detail-box {{
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #fbfcfe;
      padding: 14px;
      min-width: 0;
    }}
    .detail-box.wide {{ grid-column: span 2; }}
    .detail-box h4 {{
      margin: 0 0 9px;
      font-size: 13px;
      text-transform: uppercase;
      color: var(--muted);
      letter-spacing: 0;
    }}
    .detail-box p {{
      margin: 0 0 8px;
    }}
    .detail-box li {{
      margin: 6px 0;
    }}
    .priority-box {{
      border-left: 5px solid var(--amber);
      background: #fffaf0;
    }}
    .risk-line {{
      margin-top: 10px !important;
      color: var(--red);
      font-weight: 750;
    }}
    .evidence-box li {{
      font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
      font-size: 12px;
    }}
    .score-grid {{
      display: grid;
      grid-template-columns: repeat(4, minmax(220px, 1fr));
      gap: 12px;
    }}
    .metric-card, .queue-row, .blocker-card {{
      border: 1px solid var(--line);
      border-left: 5px solid var(--blue);
      border-radius: 8px;
      background: #fff;
      padding: 14px;
      min-width: 0;
    }}
    .metric-card.warn, .queue-row.warn, .blocker-card.warn {{ border-left-color: var(--amber); }}
    .metric-card.danger, .queue-row.danger, .blocker-card.danger {{ border-left-color: var(--red); }}
    .metric-card.good, .queue-row.good, .blocker-card.good {{ border-left-color: var(--green); }}
    .metric-card.neutral, .queue-row.neutral, .blocker-card.neutral {{ border-left-color: var(--teal); }}
    .metric-head, .row-top {{
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 8px;
      flex-wrap: wrap;
    }}
    .metric-head h3, .queue-row h3, .blocker-card h3 {{
      margin: 0;
      font-size: 15px;
      line-height: 1.25;
    }}
    .metric-head span {{
      color: var(--muted);
      font-size: 11px;
      font-weight: 800;
      max-width: 170px;
      text-align: right;
    }}
    .metric-grid {{
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 8px;
      margin: 14px 0 0;
    }}
    .metric-grid div {{
      min-width: 0;
      border-top: 1px solid var(--line);
      padding-top: 8px;
    }}
    dt {{
      color: var(--muted);
      font-size: 11px;
      font-weight: 800;
      text-transform: uppercase;
    }}
    dd {{ margin: 2px 0 0; font-weight: 800; }}
    .queue-stack, .blocker-stack {{
      display: grid;
      gap: 10px;
      max-height: 680px;
      overflow: auto;
      padding-right: 4px;
    }}
    .queue-row h3, .blocker-card h3 {{ margin-top: 10px; }}
    .queue-row p, .blocker-card p {{ margin: 8px 0 0; color: var(--muted); }}
    .owner {{ color: var(--muted); font-size: 12px; font-weight: 700; }}
    ul, ol {{
      margin: 0;
      padding-left: 20px;
    }}
    li {{ margin: 8px 0; }}
    .compact-list li::marker {{ color: var(--lav); font-weight: 800; }}
    .split {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 14px;
    }}
    .note-box {{
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 14px;
      background: #fbfcfe;
    }}
    .note-box h3 {{
      margin: 0 0 10px;
      font-size: 14px;
    }}
    footer {{
      max-width: 1480px;
      margin: 0 auto;
      padding: 0 24px 24px;
      color: var(--muted);
    }}
    .hidden {{ display: none !important; }}
    @media (max-width: 1120px) {{
      .hero, .split {{ grid-template-columns: 1fr; }}
      .campaign-layout, .detail-head {{ grid-template-columns: 1fr; }}
      .score-grid {{ grid-template-columns: repeat(2, minmax(220px, 1fr)); }}
      .span-7, .span-5, .span-4 {{ grid-column: span 12; }}
    }}
    @media (max-width: 720px) {{
      .shell {{ width: 100vw; overflow-x: hidden; }}
      .topbar {{ grid-template-columns: 1fr; }}
      .topbar {{ padding: 18px 14px; }}
      .topbar, main, footer {{ max-width: 100vw; }}
      .controls {{ display: grid; grid-template-columns: 1fr; justify-content: stretch; }}
      .search {{ width: 100%; }}
      .toggle {{ width: fit-content; max-width: 100%; }}
      main {{ padding: 14px; }}
      .hero, .grid {{ width: 100%; max-width: 100%; overflow-x: hidden; }}
      .panel {{ max-width: calc(100vw - 28px); overflow-x: hidden; }}
      .brand h1 {{ font-size: 20px; line-height: 1.16; }}
      .brand p {{ font-size: 14px; }}
      .goal {{ padding: 18px; }}
      .goal p.big {{ font-size: 19px; line-height: 1.2; }}
      .status-tile strong {{ font-size: 16px; }}
      .goal p.big, .status-tile strong, .metric-head span, .queue-row h3, .blocker-card h3 {{
        word-break: break-word;
        overflow-wrap: anywhere;
      }}
      .campaign-explorer .section-head {{ display: grid; }}
      .channel-tabs {{ width: 100%; }}
      .channel-tab {{ flex: 1 1 auto; }}
      .detail-grid, .detail-kpis {{ grid-template-columns: 1fr; }}
      .decision-summary {{ grid-template-columns: 1fr; }}
      .detail-box.wide {{ grid-column: span 1; }}
      .detail-head h3 {{ font-size: 20px; }}
      section {{ padding: 14px; }}
      .score-grid, .metric-grid {{ grid-template-columns: 1fr; }}
    }}
    {OWNER_STYLE}
  </style>
</head>
<body>
  <div class="shell">
    <header>
      <div class="topbar">
        <div class="brand">
          <h1>Growth dashboard</h1>
          <p>Dress Like Mommy · One task queue across sessions</p>
        </div>
        <div class="controls">
          <a class="desk-link" href="#taskBoardStart">View tasks</a>
          <button class="desk-button primary" data-owner-jump>Needs your input</button>
        </div>
      </div>
    </header>
    <main>
      {owner_view}
      <details class="legacy"><summary>Account history and detailed operator records</summary>
      <p class="desk-note">The sections below preserve dated records across sessions. They do not establish current serving, spending, account access or new sales.</p>
      <div class="controls legacy-controls"><input class="search" id="search" type="search" aria-label="Search operator history" placeholder="Search operator history"><label class="toggle"><input id="needsAction" type="checkbox"> Flagged records only</label></div>
      <div class="hero">
        <section class="goal panel">
          <div>
            <h2>Current Goal</h2>
            <p class="big">{h(current_goal)}</p>
          </div>
          <div class="chips">
            <span class="chip {control_class}">State: {h(live_state_mode)}</span>
            <span class="chip {approval_class}">Effective authority: {h(effective_approval_policy)}</span>
            <span class="chip {spend_class}">Standing spend record: {h(spend_status)}</span>
            <span class="chip warn">Review log: {h(reviewer_verdict)}</span>
            <span class="chip neutral">Full-paid controls; exact nonspend permissions are separate</span>
          </div>
        </section>
        <aside class="status-board panel">
          <div class="status-tile">
            <span>Success Measure</span>
            <strong>{h(success_measure or "Maximize profitable sales at about 650% ROAS.")}</strong>
          </div>
          <div class="status-tile">
            <span>Expert Standard</span>
            <strong>{h(expert_standard or "Use source-backed high-intent, low-waste strategy with anti-cannibalization controls.")}</strong>
          </div>
          <div class="status-tile">
            <span>Next Best Move</span>
            <strong>{h(authoritative_next)}</strong>
          </div>
          <div class="status-tile">
            <span>One Owner Action</span>
            <strong>{h(owner_action or authoritative_next)}</strong>
          </div>
          <div class="status-tile">
            <span>Main Risk</span>
            <strong>{h(authoritative_risk)}</strong>
          </div>
          <div class="status-tile">
            <span>Human Check</span>
            <strong>Open this file, scan red/yellow cards, approve only exact scoped actions.</strong>
          </div>
        </aside>
      </div>

      <div class="grid">
        {render_campaign_explorer(campaign_data, historical=fail_closed)}

        <section class="panel span-12" data-filter-scope>
          <div class="section-head">
            <h2>Historical Channel Scorecard</h2>
            <p>Saved channel evidence; not a current performance window</p>
          </div>
          <div class="score-grid">
            {render_score_rows(score_table)}
          </div>
        </section>

        <section class="panel span-7" data-filter-scope>
          <div class="section-head">
            <h2>Operator Readiness Detail</h2>
            <p>Original readiness fields; all current tasks appear in the owner board above. Colors are not action authority.</p>
          </div>
          <div class="queue-stack">
            {render_action_rows(action_table)}
          </div>
        </section>

        <section class="panel span-5" data-filter-scope>
          <div class="section-head">
            <h2>Blockers</h2>
            <p>What stops the next sales-moving step</p>
          </div>
          <div class="blocker-stack">
            {render_blocker_rows(blocker_table)}
          </div>
        </section>

        <section class="panel span-4">
          <div class="section-head">
            <h2>Next 3 Tasks</h2>
          </div>
          <div class="compact-list">{render_list(next_tasks, numbered=True)}</div>
        </section>

        <section class="panel span-4">
          <div class="section-head">
            <h2>What Changed</h2>
          </div>
          <div class="split">
            <div class="note-box">
              <h3>Local</h3>
              {render_list(local_changes)}
            </div>
            <div class="note-box">
              <h3>Live</h3>
              {render_list(live_changes)}
            </div>
          </div>
        </section>

        <section class="panel span-4">
          <div class="section-head">
            <h2>Safety Notes</h2>
          </div>
          <div class="compact-list">{render_list(risks)}</div>
        </section>

        <section class="panel span-7">
          <div class="section-head">
            <h2>Recorded Work Across Sessions</h2>
          </div>
          <div class="compact-list">{render_list(done_today)}</div>
        </section>

        <section class="panel span-5">
          <div class="section-head">
            <h2>Assumptions</h2>
          </div>
          <div class="compact-list">{render_list(assumptions)}</div>
        </section>
      </div>
      </details>
    </main>
    <footer>
      Source records: <a href="operator_cockpit.md">Operating proposal</a> · <a href="action_queue.md">Task queue</a> · <a href="daily_scorecard.md">Scorecard</a> · <a href="current_marketing_state.md">Current authority and evidence</a> · <a href="review_log.md">Review log</a>.
    </footer>
  </div>
  <script>
    {OWNER_SCRIPT}
    {LIVE_SCRIPT}
    const search = document.getElementById('search');
    const needsAction = document.getElementById('needsAction');
    const cards = Array.from(document.querySelectorAll('.metric-card, .queue-row, .blocker-card, .campaign-card'));
    const channelTabs = Array.from(document.querySelectorAll('.channel-tab'));
    const campaignCards = Array.from(document.querySelectorAll('.campaign-card'));
    const campaignPanels = Array.from(document.querySelectorAll('.campaign-detail'));
    let activeChannel = channelTabs[0]?.dataset.channel || '';

    function isNeedsAction(card) {{
      return card.classList.contains('danger') || card.classList.contains('warn');
    }}

    function selectCampaign(id) {{
      campaignCards.forEach((card) => card.classList.toggle('active', card.dataset.campaign === id));
      campaignPanels.forEach((panel) => panel.classList.toggle('active', panel.dataset.campaignPanel === id));
    }}

    function selectChannel(channel) {{
      activeChannel = channel;
      channelTabs.forEach((tab) => tab.classList.toggle('active', tab.dataset.channel === channel));
      const firstVisible = campaignCards.find((card) => card.dataset.channel === channel);
      campaignCards.forEach((card) => {{
        const inChannel = card.dataset.channel === channel;
        card.classList.toggle('channel-hidden', !inChannel);
      }});
      if (firstVisible) selectCampaign(firstVisible.dataset.campaign);
      applyFilters();
    }}

    function applyFilters() {{
      const query = search.value.trim().toLowerCase();
      const actionOnly = needsAction.checked;
      cards.forEach((card) => {{
        const text = card.textContent.toLowerCase();
        const matchesSearch = !query || text.includes(query);
        const matchesAction = !actionOnly || isNeedsAction(card);
        const matchesChannel = !card.classList.contains('campaign-card') || card.dataset.channel === activeChannel;
        card.classList.toggle('hidden', !(matchesSearch && matchesAction && matchesChannel));
      }});
    }}

    channelTabs.forEach((tab) => tab.addEventListener('click', () => selectChannel(tab.dataset.channel)));
    campaignCards.forEach((card) => card.addEventListener('click', () => selectCampaign(card.dataset.campaign)));
    search.addEventListener('input', applyFilters);
    needsAction.addEventListener('change', applyFilters);
    if (activeChannel) selectChannel(activeChannel);
  </script>
</body>
</html>
"""

    return "\n".join(line.rstrip() for line in output.splitlines()) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=MARKETING / "operator_cockpit.html",
        help="HTML file to write.",
    )
    args = parser.parse_args()
    html_output = build_html()
    args.output.write_text(html_output, encoding="utf-8")
    print(f"Rendered {args.output.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
