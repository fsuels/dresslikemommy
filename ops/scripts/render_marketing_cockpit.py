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


def render_campaign_explorer(data: dict) -> str:
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
                  <span class="eyebrow">{h(campaign.get("status_label", ""))}</span>
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
                  <h4>Today / Yesterday Metrics</h4>
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
    return f"""
    <section class="panel span-12 campaign-explorer" data-filter-scope>
      <div class="section-head">
        <div>
          <h2>Campaign Explorer</h2>
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


def find_table(path: Path, header: str) -> Table | None:
    for table in parse_tables(read_text(path)):
        if header in table.headers:
            return table
    return None


def build_html() -> str:
    cockpit_md = read_text(MARKETING / "operator_cockpit.md")
    sections = split_sections(cockpit_md)
    score_table = find_table(MARKETING / "daily_scorecard.md", "Surface")
    action_table = find_table(MARKETING / "action_queue.md", "Action")
    blocker_table = find_table(MARKETING / "blocker_board.md", "Blocker")
    spend_text = read_text(MARKETING / "spend_authorization.md")
    review_text = read_text(MARKETING / "review_log.md")
    campaign_data = json.loads(read_text(MARKETING / "campaign_explorer.json"))
    updated = dt.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M %Z")

    current_goal = extract_first_paragraph(sections.get("Current Goal", ""))
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
    reviewer_verdict = "PASS_WITH_GATES" if "PASS_WITH_GATES" in review_text else "CHECK REVIEW LOG"

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Dress Like Mommy Marketing Cockpit</title>
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
  </style>
</head>
<body>
  <div class="shell">
    <header>
      <div class="topbar">
        <div class="brand">
          <h1>Dress Like Mommy Marketing Cockpit</h1>
          <p>One-screen operator view generated from the paid-growth command layer. Rendered {h(updated)}.</p>
        </div>
        <div class="controls">
          <input class="search" id="search" type="search" placeholder="Search campaigns, blockers, tasks...">
          <label class="toggle"><input id="needsAction" type="checkbox"> Needs action only</label>
        </div>
      </div>
    </header>
    <main>
      <div class="hero">
        <section class="goal panel">
          <div>
            <h2>Current Goal</h2>
            <p class="big">{h(current_goal)}</p>
          </div>
          <div class="chips">
            <span class="chip {status_class(spend_status)}">Spend: {h(spend_status)}</span>
            <span class="chip warn">Reviewer: {h(reviewer_verdict)}</span>
            <span class="chip neutral">Live writes: none in this pass</span>
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
            <strong>{h(next_tasks[0] if next_tasks else "Check action queue")}</strong>
          </div>
          <div class="status-tile">
            <span>Main Risk</span>
            <strong>{h(risks[0] if risks else "No risk captured")}</strong>
          </div>
          <div class="status-tile">
            <span>Human Check</span>
            <strong>Open this file, scan red/yellow cards, approve only exact scoped actions.</strong>
          </div>
        </aside>
      </div>

      <div class="grid">
        {render_campaign_explorer(campaign_data)}

        <section class="panel span-12" data-filter-scope>
          <div class="section-head">
            <h2>Live Scorecard</h2>
            <p>Current readback decisions by surface</p>
          </div>
          <div class="score-grid">
            {render_score_rows(score_table)}
          </div>
        </section>

        <section class="panel span-7" data-filter-scope>
          <div class="section-head">
            <h2>Action Queue</h2>
            <p>Green is safe, yellow is prepare/read back, red needs a gate.</p>
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
            <h2>Done Today</h2>
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
    </main>
    <footer>
      Source files: ops/marketing/operator_cockpit.md, daily_scorecard.md, action_queue.md, blocker_board.md, spend_authorization.md, review_log.md.
    </footer>
  </div>
  <script>
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


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=MARKETING / "operator_cockpit.html",
        help="HTML file to write.",
    )
    args = parser.parse_args()
    html_output = "\n".join(line.rstrip() for line in build_html().splitlines()) + "\n"
    args.output.write_text(html_output, encoding="utf-8")
    print(f"Rendered {args.output.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
