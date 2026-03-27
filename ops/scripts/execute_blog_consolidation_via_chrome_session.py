#!/usr/bin/env python3
"""Execute blog seasonal consolidation via an authenticated Chrome Shopify Admin tab.

This script reads the generated consolidation CSV, determines a canonical winner
for each cluster, archives duplicate year-based articles, and creates or updates
Shopify URL redirects to the canonical year-free handle.

The stored Admin token currently returns 401 for this store, so this helper uses
the active logged-in Google Chrome Shopify Admin tab via AppleScript + in-page
GraphQL requests instead of repo-stored credentials.

Dry-run is default. Re-run with --execute to mutate live Shopify data.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import re
import subprocess
import sys
import textwrap
import time
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


DEFAULT_PLAN_CSV = Path("ops/content/seo/blog-seasonal-consolidation-plan-2026-03-26.csv")
DEFAULT_REPORT_JSON = Path("tmp/blog_consolidation_live_report.json")
DEFAULT_STORE = "dresslikemommy-com"
DEFAULT_BLOG_ID = "gid://shopify/Blog/41450437"
DEFAULT_ADMIN_URL = f"https://admin.shopify.com/store/{DEFAULT_STORE}/content/articles/559651291233"
DEFAULT_ARCHIVE_PREFIX = dt.datetime.now().strftime("arch-%Y%m%d")
BLOG_PREFIX = "/blogs/news/"
ARCHIVE_TITLE_PREFIX = "[Archived duplicate] "

APPLE_SCRIPT_RUNNER = textwrap.dedent(
    """
    on run argv
      tell application "Google Chrome"
        return execute active tab of front window javascript (item 1 of argv)
      end tell
    end run
    """
)

BLOG_ARTICLES_QUERY = """
query BlogArticles($id: ID!, $cursor: String) {
  blog(id: $id) {
    articles(first: 100, after: $cursor) {
      nodes {
        id
        handle
        title
        publishedAt
        isPublished
      }
      pageInfo {
        hasNextPage
        endCursor
      }
    }
  }
}
"""

URL_REDIRECTS_QUERY = """
query UrlRedirects($query: String!) {
  urlRedirects(first: 10, query: $query) {
    nodes {
      id
      path
      target
    }
  }
}
"""

ARTICLE_UPDATE_MUTATION = """
mutation ArticleUpdate($id: ID!, $article: ArticleUpdateInput!) {
  articleUpdate(id: $id, article: $article) {
    article {
      id
      handle
      title
      publishedAt
      isPublished
    }
    userErrors {
      field
      message
    }
  }
}
"""

URL_REDIRECT_CREATE_MUTATION = """
mutation UrlRedirectCreate($urlRedirect: UrlRedirectInput!) {
  urlRedirectCreate(urlRedirect: $urlRedirect) {
    urlRedirect {
      id
      path
      target
    }
    userErrors {
      field
      message
    }
  }
}
"""

URL_REDIRECT_DELETE_MUTATION = """
mutation UrlRedirectDelete($id: ID!) {
  urlRedirectDelete(id: $id) {
    deletedUrlRedirectId
    userErrors {
      field
      message
    }
  }
}
"""


@dataclass(frozen=True)
class ArticleRecord:
    id: str
    handle: str
    title: str
    published_at: Optional[str]
    is_published: bool


@dataclass(frozen=True)
class ClusterPlan:
    canonical_slug: str
    canonical_title: str
    sources: List[str]


@dataclass(frozen=True)
class ClusterDecision:
    canonical_slug: str
    canonical_title: str
    winner: ArticleRecord
    winner_requires_rename: bool
    source_articles: List[ArticleRecord]
    missing_source_handles: List[str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan-csv", type=Path, default=DEFAULT_PLAN_CSV)
    parser.add_argument("--report-json", type=Path, default=DEFAULT_REPORT_JSON)
    parser.add_argument("--store", default=DEFAULT_STORE)
    parser.add_argument("--blog-id", default=DEFAULT_BLOG_ID)
    parser.add_argument("--admin-url", default=DEFAULT_ADMIN_URL)
    parser.add_argument("--archive-prefix", default=DEFAULT_ARCHIVE_PREFIX)
    parser.add_argument("--execute", action="store_true", help="Apply live Shopify updates")
    parser.add_argument(
        "--canonical-slugs",
        default="",
        help="Optional comma-separated canonical slugs to limit execution scope",
    )
    return parser.parse_args()


def clean(value: object) -> str:
    return str(value or "").strip()


def normalize_slug(value: str) -> str:
    return clean(value).strip("/")


def parse_rows(plan_csv: Path, canonical_scope: Iterable[str]) -> List[ClusterPlan]:
    requested = {normalize_slug(slug) for slug in canonical_scope if normalize_slug(slug)}
    clusters: Dict[str, Dict[str, Any]] = defaultdict(lambda: {"canonical_title": "", "sources": []})
    with plan_csv.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            decision = clean(row.get("keep_or_redirect", "")).upper()
            if decision != "REDIRECT":
                continue
            canonical_slug = normalize_slug(row.get("canonical_slug", ""))
            if requested and canonical_slug not in requested:
                continue
            source_slug = normalize_slug(row.get("redirect_from_slug", ""))
            if not canonical_slug or not source_slug:
                continue
            clusters[canonical_slug]["canonical_title"] = clean(row.get("canonical_title", "")) or canonical_slug
            clusters[canonical_slug]["sources"].append(source_slug)

    plans: List[ClusterPlan] = []
    for canonical_slug in sorted(clusters):
        plans.append(
            ClusterPlan(
                canonical_slug=canonical_slug,
                canonical_title=clusters[canonical_slug]["canonical_title"],
                sources=sorted(dict.fromkeys(clusters[canonical_slug]["sources"])),
            )
        )
    return plans


def run_subprocess(args: List[str], *, input_text: Optional[str] = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, input=input_text, text=True, capture_output=True, check=False)


def ensure_admin_tab(admin_url: str) -> None:
    script = textwrap.dedent(
        f"""
        tell application "Google Chrome"
          if (count of windows) = 0 then make new window
          set URL of active tab of front window to "{admin_url}"
          activate
        end tell
        """
    )
    result = run_subprocess(["osascript"], input_text=script)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "Failed to open Google Chrome admin tab.")
    time.sleep(5)


def execute_chrome_javascript(js_code: str) -> str:
    result = run_subprocess(["osascript", "-", js_code], input_text=APPLE_SCRIPT_RUNNER)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "Chrome JavaScript execution failed.")
    return result.stdout


def graphql_via_chrome(store: str, query: str, variables: Dict[str, Any]) -> Dict[str, Any]:
    js_code = """
(() => {
  const scriptEl = document.querySelector('script[data-serialized-id="server-data"]');
  if (!scriptEl) {
    return JSON.stringify({ error: "missing server-data", location: location.href });
  }
  const csrf = JSON.parse(scriptEl.textContent).csrfToken;
  const xhr = new XMLHttpRequest();
  xhr.open("POST", "/api/shopify/%s", false);
  xhr.setRequestHeader("accept", "application/json");
  xhr.setRequestHeader("content-type", "application/json");
  xhr.setRequestHeader("x-csrf-token", csrf);
  xhr.send(JSON.stringify({ query: %s, variables: %s }));
  return xhr.responseText;
})()
""" % (
        store,
        json.dumps(query),
        json.dumps(variables, ensure_ascii=True),
    )
    raw = execute_chrome_javascript(js_code)
    payload = json.loads(raw)
    if payload.get("error"):
        raise RuntimeError(f"Browser session error: {payload}")
    if payload.get("errors"):
        raise RuntimeError(f"Shopify GraphQL errors: {json.dumps(payload['errors'], ensure_ascii=False)}")
    return payload["data"]


def fetch_all_articles(store: str, blog_id: str) -> List[ArticleRecord]:
    articles: List[ArticleRecord] = []
    cursor = None
    while True:
        data = graphql_via_chrome(store, BLOG_ARTICLES_QUERY, {"id": blog_id, "cursor": cursor})
        connection = data["blog"]["articles"]
        for node in connection["nodes"]:
            articles.append(
                ArticleRecord(
                    id=node["id"],
                    handle=node["handle"],
                    title=node["title"],
                    published_at=node.get("publishedAt"),
                    is_published=bool(node.get("isPublished")),
                )
            )
        if not connection["pageInfo"]["hasNextPage"]:
            break
        cursor = connection["pageInfo"]["endCursor"]
    return articles


def parse_timestamp(value: Optional[str]) -> dt.datetime:
    if not value:
        return dt.datetime.min.replace(tzinfo=dt.timezone.utc)
    normalized = value.replace("Z", "+00:00")
    return dt.datetime.fromisoformat(normalized)


YEAR_RE = re.compile(r"(19|20)\d{2}(?!.*(19|20)\d{2})")


def year_from_handle(handle: str) -> int:
    match = YEAR_RE.search(handle)
    return int(match.group(0)) if match else 0


def choose_winner(canonical_slug: str, live_by_handle: Dict[str, ArticleRecord], source_articles: List[ArticleRecord]) -> Tuple[ArticleRecord, bool]:
    canonical_article = live_by_handle.get(canonical_slug)
    if canonical_article:
        return canonical_article, False
    ranked = sorted(source_articles, key=lambda article: (parse_timestamp(article.published_at), year_from_handle(article.handle)))
    return ranked[-1], True


def build_decisions(plans: List[ClusterPlan], live_articles: List[ArticleRecord]) -> List[ClusterDecision]:
    live_by_handle = {article.handle: article for article in live_articles}
    decisions: List[ClusterDecision] = []
    for plan in plans:
        source_articles = [live_by_handle[source] for source in plan.sources if source in live_by_handle]
        missing_source_handles = [source for source in plan.sources if source not in live_by_handle]
        if not source_articles and plan.canonical_slug not in live_by_handle:
            continue
        winner, winner_requires_rename = choose_winner(plan.canonical_slug, live_by_handle, source_articles)
        decisions.append(
            ClusterDecision(
                canonical_slug=plan.canonical_slug,
                canonical_title=plan.canonical_title,
                winner=winner,
                winner_requires_rename=winner_requires_rename,
                source_articles=source_articles,
                missing_source_handles=missing_source_handles,
            )
        )
    return decisions


def make_archive_handle(source_handle: str, archive_prefix: str, reserved_handles: set[str]) -> str:
    base = f"{archive_prefix}-{source_handle}"
    if len(base) > 240:
        base = base[:240].rstrip("-")
    candidate = base
    counter = 2
    while candidate in reserved_handles:
        suffix = f"-{counter}"
        candidate = f"{base[: max(1, 240 - len(suffix))]}{suffix}"
        counter += 1
    reserved_handles.add(candidate)
    return candidate


def query_redirect_nodes(store: str, path: str) -> List[Dict[str, str]]:
    data = graphql_via_chrome(store, URL_REDIRECTS_QUERY, {"query": f"path:{path}"})
    return list(data["urlRedirects"]["nodes"])


def ensure_redirect(store: str, path: str, target: str) -> Dict[str, Any]:
    existing_nodes = query_redirect_nodes(store, path)
    if existing_nodes and all(node["target"] == target for node in existing_nodes):
        return {"status": "unchanged", "path": path, "target": target, "existing_ids": [node["id"] for node in existing_nodes]}

    deleted_ids: List[str] = []
    for node in existing_nodes:
        data = graphql_via_chrome(store, URL_REDIRECT_DELETE_MUTATION, {"id": node["id"]})
        payload = data["urlRedirectDelete"]
        if payload.get("userErrors"):
            raise RuntimeError(f"Redirect delete failed for {path}: {payload['userErrors']}")
        deleted_ids.append(payload["deletedUrlRedirectId"])

    data = graphql_via_chrome(store, URL_REDIRECT_CREATE_MUTATION, {"urlRedirect": {"path": path, "target": target}})
    payload = data["urlRedirectCreate"]
    if payload.get("userErrors"):
        raise RuntimeError(f"Redirect create failed for {path}: {payload['userErrors']}")
    created = payload["urlRedirect"]
    return {"status": "created" if not existing_nodes else "replaced", "path": path, "target": target, "deleted_ids": deleted_ids, "created_id": created["id"]}


def update_article(store: str, article_id: str, article_input: Dict[str, Any]) -> Dict[str, Any]:
    data = graphql_via_chrome(store, ARTICLE_UPDATE_MUTATION, {"id": article_id, "article": article_input})
    payload = data["articleUpdate"]
    if payload.get("userErrors"):
        raise RuntimeError(f"Article update failed for {article_id}: {payload['userErrors']}")
    return payload["article"]


def collect_stray_suffix_duplicates(live_articles: List[ArticleRecord], decisions: List[ClusterDecision]) -> List[Tuple[ArticleRecord, str, str]]:
    canonical_titles = {decision.canonical_slug: decision.canonical_title for decision in decisions}
    live_by_handle = {article.handle: article for article in live_articles}
    planned_source_handles = {
        article.handle
        for decision in decisions
        for article in decision.source_articles
    }
    extras: List[Tuple[ArticleRecord, str, str]] = []
    for article in live_articles:
        if not article.handle.endswith("-1"):
            continue
        if article.handle in planned_source_handles:
            continue
        base_handle = article.handle[:-2]
        if base_handle not in live_by_handle:
            continue
        canonical_title = canonical_titles.get(base_handle)
        if canonical_title and article.title == canonical_title:
            extras.append((article, base_handle, canonical_title))
    return extras


def summarize(decisions: List[ClusterDecision], live_articles: List[ArticleRecord]) -> Dict[str, Any]:
    canonical_existing = sum(1 for decision in decisions if not decision.winner_requires_rename)
    canonical_missing = sum(1 for decision in decisions if decision.winner_requires_rename)
    source_count = sum(len(decision.source_articles) for decision in decisions)
    archive_count = sum(
        len([article for article in decision.source_articles if article.id != decision.winner.id])
        for decision in decisions
    )
    redirect_count = sum(len(decision.source_articles) + len(decision.missing_source_handles) for decision in decisions)
    stray_suffix_count = len(collect_stray_suffix_duplicates(live_articles, decisions))
    return {
        "clusters": len(decisions),
        "canonical_existing": canonical_existing,
        "canonical_missing": canonical_missing,
        "source_articles_live": source_count,
        "archive_operations": archive_count,
        "redirect_operations": redirect_count,
        "stray_suffix_duplicates": stray_suffix_count,
    }


def main() -> int:
    args = parse_args()
    canonical_scope = [part.strip() for part in args.canonical_slugs.split(",") if part.strip()]
    plans = parse_rows(args.plan_csv, canonical_scope)
    if not plans:
        print("No consolidation rows matched the requested scope.", file=sys.stderr)
        return 1

    ensure_admin_tab(args.admin_url)
    live_articles = fetch_all_articles(args.store, args.blog_id)
    decisions = build_decisions(plans, live_articles)
    reserved_handles = {article.handle for article in live_articles}
    summary = summarize(decisions, live_articles)

    report: Dict[str, Any] = {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "store": args.store,
        "blog_id": args.blog_id,
        "plan_csv": str(args.plan_csv),
        "execute": args.execute,
        "summary": summary,
        "clusters": [],
        "stray_suffix_duplicates": [],
        "operations": {"article_updates": [], "redirects": []},
    }

    for decision in decisions:
        report["clusters"].append(
            {
                "canonical_slug": decision.canonical_slug,
                "canonical_title": decision.canonical_title,
                "winner_handle": decision.winner.handle,
                "winner_id": decision.winner.id,
                "winner_requires_rename": decision.winner_requires_rename,
                "source_handles": [article.handle for article in decision.source_articles],
                "missing_source_handles": decision.missing_source_handles,
            }
        )

    extras = collect_stray_suffix_duplicates(live_articles, decisions)
    report["stray_suffix_duplicates"] = [
        {"handle": article.handle, "id": article.id, "target_handle": target_handle}
        for article, target_handle, _ in extras
    ]

    if not args.execute:
        args.report_json.parent.mkdir(parents=True, exist_ok=True)
        args.report_json.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        print(f"report_json={args.report_json}")
        return 0

    # Canonical winner title normalization and winner renames.
    for decision in decisions:
        if decision.winner_requires_rename:
            updated = update_article(
                args.store,
                decision.winner.id,
                {"handle": decision.canonical_slug, "title": decision.canonical_title},
            )
            report["operations"]["article_updates"].append(
                {
                    "action": "rename_to_canonical",
                    "article_id": decision.winner.id,
                    "before_handle": decision.winner.handle,
                    "after_handle": updated["handle"],
                    "title": updated["title"],
                }
            )
        elif decision.winner.title != decision.canonical_title:
            updated = update_article(
                args.store,
                decision.winner.id,
                {"title": decision.canonical_title},
            )
            report["operations"]["article_updates"].append(
                {
                    "action": "normalize_canonical_title",
                    "article_id": decision.winner.id,
                    "before_handle": decision.winner.handle,
                    "after_handle": updated["handle"],
                    "title": updated["title"],
                }
            )

    # Archive duplicate source articles.
    for decision in decisions:
        for article in decision.source_articles:
            if article.id == decision.winner.id:
                continue
            archive_handle = make_archive_handle(article.handle, args.archive_prefix, reserved_handles)
            updated = update_article(
                args.store,
                article.id,
                {
                    "handle": archive_handle,
                    "title": f"{ARCHIVE_TITLE_PREFIX}{article.title}",
                    "isPublished": False,
                },
            )
            report["operations"]["article_updates"].append(
                {
                    "action": "archive_duplicate",
                    "article_id": article.id,
                    "before_handle": article.handle,
                    "after_handle": updated["handle"],
                    "title": updated["title"],
                    "canonical_target": decision.canonical_slug,
                }
            )

    # Cleanup stray "-1" duplicates after canonical renames.
    for article, target_handle, canonical_title in extras:
        archive_handle = make_archive_handle(article.handle, args.archive_prefix, reserved_handles)
        updated = update_article(
            args.store,
            article.id,
            {
                "handle": archive_handle,
                "title": f"{ARCHIVE_TITLE_PREFIX}{article.title}",
                "isPublished": False,
            },
        )
        report["operations"]["article_updates"].append(
            {
                "action": "archive_stray_suffix_duplicate",
                "article_id": article.id,
                "before_handle": article.handle,
                "after_handle": updated["handle"],
                "title": updated["title"],
                "canonical_target": target_handle,
            }
        )
        redirect_result = ensure_redirect(args.store, f"{BLOG_PREFIX}{article.handle}", f"{BLOG_PREFIX}{target_handle}")
        report["operations"]["redirects"].append(redirect_result)

    # Create or update redirects for planned source handles.
    for decision in decisions:
        target_path = f"{BLOG_PREFIX}{decision.canonical_slug}"
        for source_slug in list(dict.fromkeys([article.handle for article in decision.source_articles] + decision.missing_source_handles)):
            if source_slug == decision.canonical_slug:
                continue
            redirect_result = ensure_redirect(args.store, f"{BLOG_PREFIX}{source_slug}", target_path)
            report["operations"]["redirects"].append(redirect_result)

    args.report_json.parent.mkdir(parents=True, exist_ok=True)
    args.report_json.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"article_updates={len(report['operations']['article_updates'])}")
    print(f"redirects={len(report['operations']['redirects'])}")
    print(f"report_json={args.report_json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
