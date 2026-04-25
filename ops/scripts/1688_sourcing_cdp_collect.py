#!/usr/bin/env python3
"""Collect first-pass 1688 candidates from a logged-in Chrome CDP session.

This is browser-assisted automation. It attaches to an already logged-in local
Chrome debugging port, loads normal 1688 search pages, reads visible DOM cards,
and then runs the local scorecard. It does not bypass login or CAPTCHA.
"""

from __future__ import annotations

import argparse
import datetime as dt
import itertools
import json
import subprocess
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCING_ROOT = REPO_ROOT / "ops" / "sourcing"
CATEGORIES_PATH = SOURCING_ROOT / "sourcing-categories.json"
DECISIONS_PATH = SOURCING_ROOT / "state" / "decisions.json"
SCORER_PATH = REPO_ROOT / "ops" / "scripts" / "1688_sourcing_score.py"


COLLECT_JS = r"""
(() => {
  const absolutize = (url) => {
    try { return new URL(url, location.href).href; } catch { return ""; }
  };
  const text = (node) => (node?.innerText || node?.textContent || "").replace(/\s+/g, " ").trim();
  const attr = (node, name) => node?.getAttribute?.(name) || "";
  const uniq = (items) => [...new Set(items.filter(Boolean))];
  const usefulParent = (anchor) => {
    let node = anchor;
    for (let i = 0; i < 7 && node?.parentElement; i += 1) {
      const body = text(node);
      const hasImage = Boolean(node.querySelector("img"));
      const hasPrice = /[¥￥]\s*\d|MOQ|起批|成交|回头率|发货|实力商家|官方物流/.test(body);
      if (hasImage && body.length > 20 && (hasPrice || body.length > 80)) return node;
      node = node.parentElement;
    }
    return anchor.closest("div,li,article") || anchor;
  };
  const parsePrice = (body) => body.match(/[¥￥]\s*([0-9]+(?:\.[0-9]+)?)/)?.[1] || "";
  const parseMoq = (body) => body.match(/(?:起批|起订|MOQ|moq)[^\d]{0,8}(\d+)/i)?.[1] || "";
  const parsePercent = (body, label) => {
    const escaped = label.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    const match = body.match(new RegExp(`${escaped}[^0-9]{0,10}([0-9]+(?:\\.[0-9]+)?)\\s*%`, "i"));
    return match ? `${match[1]}%` : "";
  };
  const parseYears = (body) => body.match(/(\d+(?:\.\d+)?)\s*年(?:店|诚信通|经营|会员)?/)?.[1] || "";
  const normalizeCount = (value, unit) => {
    let parsed = Number(value);
    if (unit === "万") parsed *= 10000;
    if (/K/i.test(unit || "")) parsed *= 1000;
    return String(Math.round(parsed));
  };
  const parseSalesInfo = (body) => {
    const patterns = [
      /(?:近30天|30天|月销|月售|成交|付款|销量|已售|售出|sold|orders)[^\d]{0,12}(\d+(?:\.\d+)?)(万|K|k)?\+?/i,
      /(\d+(?:\.\d+)?)(万|K|k)?\+?\s*(?:sold|orders|成交|付款|人付款|已售|售出)/i
    ];
    for (const pattern of patterns) {
      const match = body.match(pattern);
      if (!match) continue;
      const raw = match[0].replace(/\s+/g, " ").trim();
      let window = "Visible 1688 search-card sales label; exact time window not shown.";
      if (/近30天|30天|月销|月售|monthly|past 30/i.test(raw)) {
        window = "Likely recent 30-day/monthly sales because the visible label says 30 days/monthly.";
      }
      if (/累计|total/i.test(raw)) {
        window = "Likely cumulative sales because the visible label says total/cumulative.";
      }
      return { value: normalizeCount(match[1], match[2]), context: `${raw} (${window})` };
    }
    return { value: "", context: "" };
  };
  const detectTerms = (body, terms) => terms.filter((term) => body.toLowerCase().includes(term.toLowerCase()));
  const badgeTerms = [
    "实力商家", "超级工厂", "深度验厂", "深度认证", "真实工厂", "买家保障", "品质保障",
    "官方物流", "48小时发货", "24小时发货", "现货", "一件代发", "15天包换", "包换", "in stock"
  ];
  const riskTerms = [
    "Disney", "Mickey", "Minnie", "Nike", "Adidas", "Barbie", "Hello Kitty", "Snoopy",
    "Pokemon", "Marvel", "迪士尼", "米奇", "米妮", "耐克", "阿迪", "芭比", "凯蒂猫",
    "史努比", "宝可梦", "漫威", "卡通", "联名", "品牌", "logo"
  ];
  const anchors = Array.from(document.querySelectorAll('a[href*="/offer/"], a[href*="detail.1688.com/offer/"]'));
  const seen = new Set();
  const candidates = [];
  for (const anchor of anchors) {
    const productUrl = absolutize(anchor.href);
    const offerId = productUrl.match(/offer\/(\d+)\.html/)?.[1] || productUrl;
    if (!productUrl || seen.has(offerId)) continue;
    seen.add(offerId);
    const card = usefulParent(anchor);
    const body = text(card);
    const image = card.querySelector("img") || anchor.querySelector("img");
    const imageUrl = absolutize(
      attr(image, "src") || attr(image, "data-src") || attr(image, "data-original") || attr(image, "data-lazy-src")
    );
    const title = attr(anchor, "title") || attr(image, "alt") || text(anchor) || body.split(/[¥￥]/)[0].slice(0, 120);
    const salesInfo = parseSalesInfo(body);
    candidates.push({
      product_url: productUrl,
      image_url: imageUrl,
      title,
      vendor_name: "",
      vendor_url: "",
      vendor_location: "",
      price_cny: parsePrice(body),
      moq: parseMoq(body),
      monthly_sales: salesInfo.value,
      sales_context: salesInfo.context,
      repurchase_rate_pct: parsePercent(body, "回头率") || parsePercent(body, "Repurchase Rate"),
      rating: "",
      years_on_1688: parseYears(body),
      badges: uniq(detectTerms(body, badgeTerms)).join(" | "),
      service_flags: uniq(detectTerms(body, ["官方物流", "48小时发货", "24小时发货", "现货", "一件代发", "15天包换", "包换", "in stock"])).join(" | "),
      dropship_supported: body.includes("一件代发") || body.toLowerCase().includes("one piece") ? "yes" : "",
      size_chart: "",
      category_match: "5",
      style_fit: imageUrl ? "4" : "3",
      image_quality: imageUrl ? "3" : "",
      ip_risk_flags: uniq(detectTerms(`${title} ${body}`, riskTerms)).join(" | "),
      raw_card_text: body.slice(0, 1200),
      search_url: location.href,
      notes: `Collected from logged-in 1688 search: ${location.href}`
    });
  }
  return JSON.stringify({
    collected_at: new Date().toISOString(),
    page_url: location.href,
    page_title: document.title,
    candidates
  });
})()
"""


class CdpClient:
    def __init__(self, port: int) -> None:
        try:
            import websocket  # type: ignore
        except ImportError as exc:
            raise SystemExit("Missing Python package websocket-client. Install it or use the browser console collector.") from exc
        self.websocket = websocket
        pages = json.load(urllib.request.urlopen(f"http://127.0.0.1:{port}/json/list", timeout=8))
        page = next((item for item in pages if item.get("type") == "page"), None)
        if not page:
            raise SystemExit(f"No Chrome page found on CDP port {port}.")
        self.ws = websocket.create_connection(page["webSocketDebuggerUrl"], timeout=20, suppress_origin=True)
        self.ids = itertools.count(1)

    def call(self, method: str, params: dict[str, Any] | None = None, timeout: int = 20) -> dict[str, Any]:
        message_id = next(self.ids)
        self.ws.send(json.dumps({"id": message_id, "method": method, "params": params or {}}))
        deadline = time.time() + timeout
        while time.time() < deadline:
            message = json.loads(self.ws.recv())
            if message.get("id") == message_id:
                return message
        raise TimeoutError(method)

    def navigate(self, url: str) -> None:
        self.call("Page.navigate", {"url": url}, timeout=10)

    def evaluate_json(self, expression: str) -> dict[str, Any]:
        response = self.call(
            "Runtime.evaluate",
            {"expression": expression, "awaitPromise": True, "returnByValue": True},
            timeout=20,
        )
        value = response.get("result", {}).get("result", {}).get("value", "{}")
        return json.loads(value)

    def close(self) -> None:
        self.ws.close()


def gbk_quote(query: str) -> str:
    return urllib.parse.quote_from_bytes(query.encode("gbk", errors="ignore"))


def search_url(query: str) -> str:
    return f"https://s.1688.com/selloffer/offer_search.htm?keywords={gbk_quote(query)}"


def load_categories() -> dict[str, dict[str, Any]]:
    payload = json.loads(CATEGORIES_PATH.read_text(encoding="utf-8"))
    return {item["id"]: item for item in payload.get("categories", [])}


def dedupe_candidates(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    result: list[dict[str, Any]] = []
    for row in rows:
        url = str(row.get("product_url", ""))
        match = re_search_offer(url)
        key = match or url
        if not key or key in seen:
            continue
        seen.add(key)
        result.append(row)
    return result


def category_match_score(row: dict[str, Any], category_id: str) -> str:
    haystack = " ".join(
        str(row.get(field, "")).lower()
        for field in ("title", "raw_card_text", "badges", "service_flags")
    )
    terms = {
        "mommy-and-me": ("mother", "daughter", "mom", "mommy", "母女", "亲子", "parent-child"),
        "daddy-and-me": ("father", "son", "dad", "daddy", "父子", "父女", "亲子", "parent-child"),
        "family-matching": ("family", "mother", "father", "daughter", "son", "家庭", "全家", "亲子", "parent-child"),
        "couples": ("couple", "men", "women", "情侣", "男", "女"),
        "maternity": ("maternity", "pregnant", "pregnancy", "孕妇", "孕妈", "哺乳"),
    }
    strong_terms = terms.get(category_id, ())
    if any(term in haystack for term in strong_terms):
        return "5"
    if category_id == "family-matching" and ("dress" in haystack and "shirt" in haystack):
        return "4"
    return "2"


def re_search_offer(url: str) -> str:
    import re

    match = re.search(r"/offer/(\d+)\.html", url)
    return match.group(1) if match else ""


def run_scorer(candidate_path: Path, output_dir: Path) -> None:
    subprocess.run(
        [
            "python3",
            str(SCORER_PATH),
            "--input",
            str(candidate_path),
            "--output-dir",
            str(output_dir),
            "--stage",
            "search",
            "--decision-state",
            str(DECISIONS_PATH),
        ],
        cwd=str(REPO_ROOT),
        check=True,
    )


def reviewable_count(output_dir: Path) -> int:
    scored_path = output_dir / "scored-candidates.json"
    if not scored_path.exists():
        return 0
    payload = json.loads(scored_path.read_text(encoding="utf-8"))
    return sum(1 for item in payload.get("candidates", []) if item.get("verdict") in {"Gold", "Test"})


def is_blocked_page(payload: dict[str, Any]) -> bool:
    page_url = str(payload.get("page_url") or "").lower()
    page_title = str(payload.get("page_title") or "").lower()
    return "_____tmd_____" in page_url or "punish" in page_url or "captcha" in page_title


def collect_from_page(client: CdpClient, url: str) -> dict[str, Any]:
    client.navigate(url)
    time.sleep(5)
    for y in (1200, 2600, 5200, 9000, 13000):
        client.call("Runtime.evaluate", {"expression": f"window.scrollTo(0, Math.min(document.body.scrollHeight, {y}))"})
        time.sleep(1.1)
    return client.evaluate_json(COLLECT_JS)


def write_run_files(
    *,
    output_dir: Path,
    candidate_path: Path,
    rows: list[dict[str, Any]],
    category_id: str,
    selected_queries: list[str],
    collected_pages: list[dict[str, Any]],
    target_reviewable: int,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    candidate_payload = {
        "collected_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "page_url": collected_pages[-1]["page_url"] if collected_pages else "",
        "page_title": collected_pages[-1]["page_title"] if collected_pages else "",
        "category_id": category_id,
        "query": selected_queries[0],
        "queries": selected_queries,
        "collected_pages": collected_pages,
        "target_reviewable": target_reviewable,
        "candidates": rows,
    }
    candidate_path.write_text(json.dumps(candidate_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    run_metadata = {
        "run_id": output_dir.name,
        "category_id": category_id,
        "source": "1688 logged-in CDP search",
        "query": selected_queries[0],
        "queries": selected_queries,
        "search_url": search_url(selected_queries[0]),
        "target_reviewable": target_reviewable,
        "stage": "search",
        "notes": "Collected by ops/scripts/1688_sourcing_cdp_collect.py from a logged-in browser session.",
    }
    (output_dir / "run.json").write_text(json.dumps(run_metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    run_scorer(candidate_path, output_dir)


def collect_category(category_id: str, limit: int, port: int, query_index: int, target_reviewable: int = 0) -> Path:
    categories = load_categories()
    if category_id not in categories:
        raise SystemExit(f"Unknown category: {category_id}")
    category = categories[category_id]
    queries = category.get("queries", [])
    if not queries:
        raise SystemExit(f"No queries configured for category: {category_id}")
    selected_queries = queries if query_index < 0 or target_reviewable > 0 else [queries[min(query_index, len(queries) - 1)]]
    stamp = dt.datetime.now().strftime("%Y-%m-%d-%H%M")
    output_dir = SOURCING_ROOT / f"{stamp}-{category_id}-1688-auto"
    candidate_path = output_dir / "candidates.json"

    client = CdpClient(port)
    all_rows: list[dict[str, Any]] = []
    collected_pages: list[dict[str, Any]] = []
    attempted_queries: list[str] = []
    try:
        for query in selected_queries:
            attempted_queries.append(query)
            url = search_url(query)
            payload = collect_from_page(client, url)
            if is_blocked_page(payload):
                page_title = payload.get("page_title") or "Captcha/verification page"
                page_url = payload.get("page_url") or url
                if not all_rows:
                    raise SystemExit(
                        "1688 CAPTCHA/interception page is open. Use Open 1688 Login/Search, "
                        f"complete the browser check, then run again. Page title: {page_title}. URL: {page_url}"
                    )
                break
            page_rows = payload.get("candidates", [])
            for row in page_rows:
                row["search_query"] = query
                row["search_url"] = payload.get("page_url") or url
            all_rows.extend(page_rows)
            collected_pages.append(
                {
                    "query": query,
                    "search_url": url,
                    "page_url": payload.get("page_url"),
                    "page_title": payload.get("page_title"),
                    "count": len(page_rows),
                }
            )
            rows = dedupe_candidates(all_rows)[:limit]
            for row in rows:
                row["category_match"] = category_match_score(row, category_id)
            write_run_files(
                output_dir=output_dir,
                candidate_path=candidate_path,
                rows=rows,
                category_id=category_id,
                selected_queries=attempted_queries.copy(),
                collected_pages=collected_pages,
                target_reviewable=target_reviewable,
            )
            if target_reviewable and reviewable_count(output_dir) >= target_reviewable:
                break
    finally:
        client.close()

    rows = dedupe_candidates(all_rows)[:limit]
    for row in rows:
        row["category_match"] = category_match_score(row, category_id)
    if not rows:
        raise SystemExit("No 1688 product cards were collected. The browser may need login/CAPTCHA recovery.")
    write_run_files(
        output_dir=output_dir,
        candidate_path=candidate_path,
        rows=rows,
        category_id=category_id,
        selected_queries=attempted_queries or selected_queries,
        collected_pages=collected_pages,
        target_reviewable=target_reviewable,
    )
    print(f"reviewable={reviewable_count(output_dir)} total={len(rows)} queries={len(attempted_queries or selected_queries)}")
    return output_dir


def main() -> None:
    parser = argparse.ArgumentParser(description="Collect 1688 candidates through an already logged-in Chrome CDP session.")
    parser.add_argument("--category", default="family-matching", help="Category id from ops/sourcing/sourcing-categories.json, or 'all'.")
    parser.add_argument("--limit", type=int, default=24, help="Maximum candidates to save per category.")
    parser.add_argument("--port", type=int, default=9333, help="Local Chrome DevTools Protocol port.")
    parser.add_argument("--query-index", type=int, default=0, help="Which configured query to use for the category. Use -1 to try all configured queries.")
    parser.add_argument("--target-reviewable", type=int, default=0, help="Try all configured queries and aim for this many Gold/Test candidates.")
    args = parser.parse_args()

    categories = load_categories()
    category_ids = list(categories) if args.category == "all" else [args.category]
    for category_id in category_ids:
        output_dir = collect_category(category_id, args.limit, args.port, args.query_index, args.target_reviewable)
        print(output_dir.relative_to(REPO_ROOT))


if __name__ == "__main__":
    main()
