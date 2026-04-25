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
  const parseSales = (body) => {
    const match = body.match(/(?:成交|付款|销量|已售|售出|sold|orders)[^\d]{0,8}(\d+(?:\.\d+)?)(万|K|\+)?/i);
    if (!match) return "";
    let value = Number(match[1]);
    if (match[2] === "万") value *= 10000;
    if (/K/i.test(match[2] || "")) value *= 1000;
    return String(Math.round(value));
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
    candidates.push({
      product_url: productUrl,
      image_url: imageUrl,
      title,
      vendor_name: "",
      vendor_url: "",
      vendor_location: "",
      price_cny: parsePrice(body),
      moq: parseMoq(body),
      monthly_sales: parseSales(body),
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


def collect_category(category_id: str, limit: int, port: int, query_index: int) -> Path:
    categories = load_categories()
    if category_id not in categories:
        raise SystemExit(f"Unknown category: {category_id}")
    category = categories[category_id]
    queries = category.get("queries", [])
    if not queries:
        raise SystemExit(f"No queries configured for category: {category_id}")
    query = queries[min(query_index, len(queries) - 1)]
    url = search_url(query)
    stamp = dt.datetime.now().strftime("%Y-%m-%d-%H%M")
    output_dir = SOURCING_ROOT / f"{stamp}-{category_id}-1688-auto"
    output_dir.mkdir(parents=True, exist_ok=True)

    client = CdpClient(port)
    try:
        client.navigate(url)
        time.sleep(5)
        client.call("Runtime.evaluate", {"expression": "window.scrollTo(0, Math.min(document.body.scrollHeight, 2600))"})
        time.sleep(2)
        payload = client.evaluate_json(COLLECT_JS)
    finally:
        client.close()

    rows = dedupe_candidates(payload.get("candidates", []))[:limit]
    for row in rows:
        row["category_match"] = category_match_score(row, category_id)
    candidate_path = output_dir / "candidates.json"
    candidate_payload = {
        "collected_at": payload.get("collected_at"),
        "page_url": payload.get("page_url"),
        "page_title": payload.get("page_title"),
        "category_id": category_id,
        "query": query,
        "candidates": rows,
    }
    candidate_path.write_text(json.dumps(candidate_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    run_metadata = {
        "run_id": output_dir.name,
        "category_id": category_id,
        "source": "1688 logged-in CDP search",
        "query": query,
        "search_url": url,
        "stage": "search",
        "notes": "Collected by ops/scripts/1688_sourcing_cdp_collect.py from a logged-in browser session.",
    }
    (output_dir / "run.json").write_text(json.dumps(run_metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    run_scorer(candidate_path, output_dir)
    return output_dir


def main() -> None:
    parser = argparse.ArgumentParser(description="Collect 1688 candidates through an already logged-in Chrome CDP session.")
    parser.add_argument("--category", default="family-matching", help="Category id from ops/sourcing/sourcing-categories.json, or 'all'.")
    parser.add_argument("--limit", type=int, default=24, help="Maximum candidates to save per category.")
    parser.add_argument("--port", type=int, default=9333, help="Local Chrome DevTools Protocol port.")
    parser.add_argument("--query-index", type=int, default=0, help="Which configured query to use for the category.")
    args = parser.parse_args()

    categories = load_categories()
    category_ids = list(categories) if args.category == "all" else [args.category]
    for category_id in category_ids:
        output_dir = collect_category(category_id, args.limit, args.port, args.query_index)
        print(output_dir.relative_to(REPO_ROOT))


if __name__ == "__main__":
    main()
