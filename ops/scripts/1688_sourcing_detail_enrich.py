#!/usr/bin/env python3
"""Enrich shortlisted 1688 candidates from product detail pages.

This is browser-assisted automation. It attaches to the local logged-in Chrome
debugging port, opens normal 1688 detail pages, reads visible DOM evidence, and
writes detail-stage sourcing artifacts. It does not bypass login or CAPTCHA.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import itertools
import json
import mimetypes
import re
import subprocess
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCING_ROOT = REPO_ROOT / "ops" / "sourcing"
DETAIL_ROOT = SOURCING_ROOT / "detail-enrichment"
VENDOR_IMAGES_ROOT = SOURCING_ROOT / "vendor-images"
DECISIONS_PATH = SOURCING_ROOT / "state" / "decisions.json"
VENDORS_PATH = SOURCING_ROOT / "state" / "vendors.json"
SCORER_PATH = REPO_ROOT / "ops" / "scripts" / "1688_sourcing_score.py"


DETAIL_JS = r"""
(() => {
  const absolutize = (url) => {
    if (!url) return "";
    if (url.startsWith("//")) url = `https:${url}`;
    try { return new URL(url, location.href).href; } catch { return ""; }
  };
  const text = (node) => (node?.innerText || node?.textContent || "").replace(/\s+/g, " ").trim();
  const attr = (node, name) => node?.getAttribute?.(name) || "";
  const uniq = (items) => [...new Set(items.map((item) => String(item || "").trim()).filter(Boolean))];
  const meta = (selector) => document.querySelector(selector)?.content || "";
  const body = text(document.body);
  const lowerBody = body.toLowerCase();
  const detectTerms = (terms) => terms.filter((term) => lowerBody.includes(term.toLowerCase()));
  const firstSrcset = (value) => (value || "").split(",")[0]?.trim().split(/\s+/)[0] || "";
  const imageUrls = uniq(Array.from(document.images).map((image) => {
    return absolutize(
      image.currentSrc ||
      attr(image, "src") ||
      attr(image, "data-src") ||
      attr(image, "data-original") ||
      attr(image, "data-lazy-src") ||
      firstSrcset(attr(image, "srcset"))
    );
  })).filter((url) => {
    const lower = url.toLowerCase();
    return /^https?:/.test(url) &&
      /(alicdn|cbu01|cbu02|cbu03|1688)/.test(lower) &&
      !/(avatar|logo|icon|sprite|gif)/.test(lower);
  }).slice(0, 24);
  const cleanPageTitle = (value) => (value || "")
    .replace(/\s*[-_—|]\s*(?:阿里巴巴|1688).*$/i, "")
    .trim();
  const companyLike = (value) => /(?:有限责任公司|有限公司|贸易公司|服饰公司|商行|工厂)$/.test(value || "");
  const titleCandidates = [
    text(document.querySelector("h1")),
    cleanPageTitle(document.title),
    cleanPageTitle(meta('meta[property="og:title"]')),
    body.slice(0, 120)
  ].map((value) => (value || "").trim()).filter(Boolean);
  const title = titleCandidates.find((value) => !companyLike(value)) || titleCandidates[0] || "";
  const anchorCandidates = Array.from(document.querySelectorAll("a[href]"));
  const vendorAnchor = anchorCandidates.find((anchor) => /shop\.1688\.com|\.1688\.com\/page\/index/.test(anchor.href));
  const vendorNode = document.querySelector('[class*="shop-name"], [class*="company"], [class*="supplier"], [class*="seller"]');
  const vendorMatch = body.match(/(?:供应商|公司名称|店铺|卖家|厂名)[:： ]{0,6}([\u4e00-\u9fffA-Za-z0-9（）()·\-. ]{2,50})/);
  const vendorName = uniq([
    text(vendorAnchor),
    text(vendorNode),
    vendorMatch?.[1] || ""
  ]).find((value) => value.length >= 2 && value.length <= 80) || "";
  const vendorUrl = absolutize(vendorAnchor?.href || "");
  const price = body.match(/[¥￥]\s*([0-9]+(?:\.[0-9]+)?)/)?.[1] || "";
  // 1688 commonly renders "1件起批 60天老客价". Matching only digits after
  // 起批 would incorrectly turn the 60-day loyalty-price label into MOQ 60.
  const moq = (
    body.match(/(\d+(?:\.\d+)?)\s*(?:件|个|套|pcs?|pieces?)\s*(?:起批|起订)/i)?.[1] ||
    body.match(/(?:起批量?|起订量?|MOQ|moq)\s*[:：]?\s*(\d+(?:\.\d+)?)\s*(?:件|个|套|pcs?|pieces?)?/i)?.[1] ||
    ""
  );
  const repeat = body.match(/(?:回头率|Repurchase Rate)[^0-9]{0,10}([0-9]+(?:\.[0-9]+)?)\s*%/i)?.[1] || "";
  const tenurePatterns = [
    /(\d+(?:\.\d+)?)\s*年\s*(?:诚信通|经营|店龄|开店|入驻|会员|老店)/i,
    /(?:诚信通|经营年限|店龄|开店|入驻|会员年限)[^\d]{0,12}(\d+(?:\.\d+)?)\s*年/i,
    /(?:supplier|company|store|member|in business)[^0-9]{0,24}(\d+(?:\.\d+)?)\s*years?/i,
    /(\d+(?:\.\d+)?)\s*years?[^A-Za-z0-9]{0,16}(?:supplier|company|store|member|in business)/i
  ];
  const tenureMatch = tenurePatterns.map((pattern) => body.match(pattern)).find(Boolean);
  const years = tenureMatch?.[1] || "";
  const rating = body.match(/(?:综合|服务|描述|物流|评分|rating)[^\d]{0,12}([4-5](?:\.\d{1,2})?)/i)?.[1] || "";
  const salesMatch = body.match(/(?:近30天|30天|月销|月售|成交|付款|销量|已售|售出|sold|orders)[^\d]{0,14}(\d+(?:\.\d+)?)(万|K|k)?\+?/i);
  const normalizeCount = (value, unit) => {
    let parsed = Number(value);
    if (unit === "万") parsed *= 10000;
    if (/K/i.test(unit || "")) parsed *= 1000;
    return parsed ? String(Math.round(parsed)) : "";
  };
  const badgeTerms = [
    "实力商家", "超级工厂", "深度验厂", "深度认证", "真实工厂", "买家保障", "品质保障",
    "官方物流", "源头工厂", "工厂", "15天包换", "包换"
  ];
  const serviceTerms = [
    "24小时发货", "48小时发货", "72小时发货", "当日发货", "急速发货", "现货",
    "一件代发", "代发", "官方物流", "退货包运费", "七天无理由", "15天包换"
  ];
  const riskTerms = [
    "Disney", "Mickey", "Minnie", "Nike", "Adidas", "Barbie", "Hello Kitty", "Snoopy",
    "Pokemon", "Marvel", "迪士尼", "米奇", "米妮", "耐克", "阿迪", "芭比", "凯蒂猫",
    "史努比", "宝可梦", "漫威", "卡通", "联名", "logo"
  ];
  const availabilityTerms = ["现货", "有货", "库存", "已下架", "商品不存在", "售罄", "库存不足"];
  const dispatchTerms = detectTerms(["24小时发货", "48小时发货", "72小时发货", "当日发货", "急速发货", "现货"]);
  const hasDropship = /一件代发|[^不]代发|dropship|drop ship|one piece/i.test(body);
  const hasSizeChart = /尺码表|尺寸表|尺码信息|尺码建议|size chart|size guide/i.test(body);
  return JSON.stringify({
    collected_at: new Date().toISOString(),
    page_url: location.href,
    page_title: document.title,
    title,
    vendor_name: vendorName,
    vendor_url: vendorUrl,
    price_cny: price,
    moq,
    monthly_sales: salesMatch ? normalizeCount(salesMatch[1], salesMatch[2]) : "",
    sales_context: salesMatch ? `${salesMatch[0]} (detail page visible sales label; confirm exact window if needed.)` : "",
    repurchase_rate_pct: repeat ? `${repeat}%` : "",
    rating,
    years_on_1688: years,
    years_on_1688_scope: years ? "supplier_context_phrase" : "",
    years_on_1688_label: tenureMatch?.[0] || "",
    badges: uniq(detectTerms(badgeTerms)).join(" | "),
    service_flags: uniq([...detectTerms(serviceTerms), ...dispatchTerms]).join(" | "),
    dropship_supported: hasDropship ? "yes" : "",
    size_chart: hasSizeChart ? "yes" : "",
    availability: uniq(detectTerms(availabilityTerms)).join(" | "),
    ip_risk_flags: uniq(detectTerms(riskTerms)).join(" | "),
    image_urls: imageUrls,
    raw_detail_text: body.slice(0, 18000)
  });
})()
"""


class CdpClient:
    def __init__(self, port: int) -> None:
        try:
            import websocket  # type: ignore
        except ImportError as exc:
            raise SystemExit("Missing Python package websocket-client. Install it or use the browser console collector.") from exc
        pages = json.load(urllib.request.urlopen(f"http://127.0.0.1:{port}/json/list", timeout=8))
        page = next((item for item in pages if item.get("type") == "page" and "1688" in str(item.get("url", ""))), None)
        page = page or next((item for item in pages if item.get("type") == "page"), None)
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
            timeout=30,
        )
        value = response.get("result", {}).get("result", {}).get("value", "{}")
        return json.loads(value)

    def close(self) -> None:
        self.ws.close()


def clean(value: Any) -> str:
    if value is None:
        return ""
    return re.sub(r"\s+", " ", str(value)).strip()


SUPPLIER_TENURE_SCOPE = "supplier_context_phrase"
SUPPLIER_TENURE_PATTERNS = (
    re.compile(r"(\d+(?:\.\d+)?)\s*年\s*(?:诚信通|经营|店龄|开店|入驻|会员|老店)", re.IGNORECASE),
    re.compile(r"(?:诚信通|经营年限|店龄|开店|入驻|会员年限)[^\d]{0,12}(\d+(?:\.\d+)?)\s*年", re.IGNORECASE),
    re.compile(r"(?:supplier|company|store|member|in business)[^0-9]{0,24}(\d+(?:\.\d+)?)\s*years?", re.IGNORECASE),
    re.compile(r"(\d+(?:\.\d+)?)\s*years?[^A-Za-z0-9]{0,16}(?:supplier|company|store|member|in business)", re.IGNORECASE),
)


def validated_supplier_tenure(detail: dict[str, Any]) -> tuple[str, str, str]:
    """Fail closed unless the captured label itself proves supplier-tenure context."""
    if clean(detail.get("years_on_1688_scope")) != SUPPLIER_TENURE_SCOPE:
        return "", "", ""
    raw_years = clean(detail.get("years_on_1688"))
    raw_label = clean(detail.get("years_on_1688_label"))
    if not raw_years or not raw_label:
        return "", "", ""
    for pattern in SUPPLIER_TENURE_PATTERNS:
        match = pattern.search(raw_label)
        if match and clean(match.group(1)) == raw_years:
            return raw_years, raw_label, SUPPLIER_TENURE_SCOPE
    return "", "", ""


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def offer_key(product_url: str) -> str:
    match = re.search(r"/offer/(\d+)\.html", clean(product_url))
    if match:
        return match.group(1)
    return clean(product_url)


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def relative(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def split_list(value: str) -> list[str]:
    return [clean(part) for part in re.split(r"[|,;，、]+", value or "") if clean(part)]


def merge_unique(*values: str) -> str:
    seen: set[str] = set()
    merged: list[str] = []
    for value in values:
        for part in split_list(value):
            key = part.lower()
            if key not in seen:
                seen.add(key)
                merged.append(part)
    return " | ".join(merged)


DETAIL_PAGE_TITLE_SUFFIX = re.compile(r"\s*[-_—|]\s*(?:阿里巴巴|1688).*$", re.IGNORECASE)
SUPPLIER_NAME_SUFFIX = re.compile(r"(?:有限责任公司|有限公司|贸易公司|服饰公司|商行|工厂)$")
DETAIL_ONLY_GENERIC_IP_TERMS = {"品牌"}
DISPATCH_EVIDENCE_TERMS = (
    "24小时发货",
    "48小时发货",
    "72小时发货",
    "当日发货",
    "急速发货",
    "ships within",
    "hour shipping",
    "same-day shipping",
    "ready stock",
    "现货",
)


def detail_product_title(base: dict[str, Any], detail: dict[str, Any]) -> str:
    """Prefer a product title and never replace it with the supplier name."""
    base_title = clean(base.get("title"))
    vendor_name = clean(detail.get("vendor_name"))
    candidates = [
        DETAIL_PAGE_TITLE_SUFFIX.sub("", clean(detail.get("page_title"))),
        DETAIL_PAGE_TITLE_SUFFIX.sub("", clean(detail.get("title"))),
        base_title,
    ]
    for candidate in candidates:
        if not candidate:
            continue
        if vendor_name and candidate == vendor_name:
            continue
        if base_title and len(candidate) <= 80 and SUPPLIER_NAME_SUFFIX.search(candidate):
            continue
        return candidate
    return base_title


def detail_moq(detail: dict[str, Any]) -> str:
    """Extract the quantity tied to the minimum-order label, not a nearby day count."""
    raw = clean(detail.get("raw_detail_text"))
    patterns = (
        re.compile(r"(\d+(?:\.\d+)?)\s*(?:件|个|套|pcs?|pieces?)\s*(?:起批|起订)", re.IGNORECASE),
        re.compile(
            r"(?:起批量?|起订量?|MOQ)\s*[:：]?\s*(\d+(?:\.\d+)?)\s*(?:件|个|套|pcs?|pieces?)?",
            re.IGNORECASE,
        ),
    )
    for pattern in patterns:
        match = pattern.search(raw)
        if match:
            return clean(match.group(1))
    return clean(detail.get("moq"))


def detail_ip_risk_flags(detail: dict[str, Any]) -> str:
    """Drop generic legal-copy matches while retaining named or product-specific risks."""
    return " | ".join(
        part for part in split_list(clean(detail.get("ip_risk_flags"))) if part.lower() not in DETAIL_ONLY_GENERIC_IP_TERMS
    )


def dispatch_evidence_label(value: Any) -> str:
    """Return service text only when it actually proves dispatch speed or ready stock."""
    text = clean(value)
    lowered = text.lower()
    return text if any(term.lower() in lowered for term in DISPATCH_EVIDENCE_TERMS) else ""


def normalize_image_url(url: str) -> str:
    text = clean(url)
    if text.startswith("//"):
        return f"https:{text}"
    return text


def download_images(urls: list[str], offer_id: str, referer: str) -> Path:
    image_dir = VENDOR_IMAGES_ROOT / offer_id
    image_dir.mkdir(parents=True, exist_ok=True)
    saved: list[dict[str, Any]] = []
    for index, url in enumerate([normalize_image_url(item) for item in urls if clean(item)][:12], start=1):
        suffix = Path(urllib.parse.urlparse(url).path).suffix.lower()
        if suffix not in {".jpg", ".jpeg", ".png", ".webp"}:
            suffix = ".jpg"
        target = image_dir / f"{offer_id}-{index:02d}{suffix}"
        request = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124 Safari/537.36",
                "Referer": referer or "https://detail.1688.com/",
                "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                data = response.read()
                content_type = response.headers.get("Content-Type") or mimetypes.guess_type(target.name)[0] or "image/jpeg"
            if len(data) < 1500:
                continue
            target.write_bytes(data)
            saved.append({"url": url, "path": relative(target), "content_type": content_type, "bytes": len(data)})
        except Exception as exc:
            saved.append({"url": url, "error": str(exc)})
    write_json(image_dir / "manifest.json", {"offer_id": offer_id, "saved_at": now_iso(), "images": saved})
    return image_dir


def iter_scored_candidates() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for scored_path in sorted(SOURCING_ROOT.glob("**/scored-candidates.json")):
        if scored_path.parent.name == "demo-shortlist":
            continue
        payload = read_json(scored_path, {})
        if not isinstance(payload, dict):
            continue
        run_metadata = read_json(scored_path.parent / "run.json", {})
        category_id = clean(run_metadata.get("category_id"))
        for item in payload.get("candidates", []):
            if not isinstance(item, dict):
                continue
            row = dict(item)
            row["key"] = offer_key(row.get("product_url", ""))
            row["run_id"] = run_metadata.get("run_id") or scored_path.parent.name
            row["run_dir"] = relative(scored_path.parent)
            row["category_id"] = category_id or clean(row.get("category_id"))
            rows.append(row)
    return rows


def dedupe_for_enrichment(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    stage_rank = {"detail": 2, "search": 1}
    verdict_rank = {"Gold": 3, "Test": 2, "Reject": 1}
    deduped: dict[str, dict[str, Any]] = {}
    for row in rows:
        key = clean(row.get("key")) or offer_key(row.get("product_url", ""))
        if not key:
            continue
        current = deduped.get(key)
        rank = (
            stage_rank.get(clean(row.get("review_stage")), 0),
            verdict_rank.get(clean(row.get("verdict")), 0),
            int(row.get("score") or 0),
            clean(row.get("run_id")),
        )
        current_rank = (
            stage_rank.get(clean(current.get("review_stage")), 0) if current else 0,
            verdict_rank.get(clean(current.get("verdict")), 0) if current else 0,
            int(current.get("score") or 0) if current else 0,
            clean(current.get("run_id")) if current else "",
        )
        if current is None or rank >= current_rank:
            deduped[key] = row
    return list(deduped.values())


def selected_candidates(key: str, category: str, limit: int) -> list[dict[str, Any]]:
    rows = dedupe_for_enrichment(iter_scored_candidates())
    if key:
        return [row for row in rows if clean(row.get("key")) == key or offer_key(row.get("product_url", "")) == key]
    selected = [
        row
        for row in rows
        if row.get("verdict") in {"Gold", "Test"}
        and (not category or category == "all" or row.get("category_id") == category)
    ]
    selected.sort(key=lambda row: (clean(row.get("review_stage")) == "detail", -int(row.get("score") or 0)))
    return selected[:limit]


def is_blocked_page(payload: dict[str, Any]) -> bool:
    text = f"{payload.get('page_url', '')} {payload.get('page_title', '')}".lower()
    return "_____tmd_____" in text or "punish" in text or "captcha" in text or "login.1688.com" in text or "login.taobao.com" in text


def collect_detail(client: CdpClient, url: str) -> dict[str, Any]:
    client.navigate(url)
    time.sleep(5)
    for y in (1200, 2600, 5200, 9000, 14000):
        client.call("Runtime.evaluate", {"expression": f"window.scrollTo(0, Math.min(document.body.scrollHeight, {y}))"})
        time.sleep(1.1)
    payload = client.evaluate_json(DETAIL_JS)
    if is_blocked_page(payload):
        raise SystemExit(
            "1688 detail page is blocked by login/CAPTCHA/interception. "
            "Open the helper browser, clear the check, then run detail verification again."
        )
    return payload


def enriched_row(base: dict[str, Any], detail: dict[str, Any], image_dir: Path, evidence_path: Path) -> dict[str, Any]:
    image_urls = [normalize_image_url(url) for url in detail.get("image_urls", []) if clean(url)]
    tenure_years, tenure_label, tenure_scope = validated_supplier_tenure(detail)
    row = dict(base)
    row.update(
        {
            "title": detail_product_title(base, detail),
            "vendor_name": clean(detail.get("vendor_name")) or clean(base.get("vendor_name")),
            "vendor_url": clean(detail.get("vendor_url")) or clean(base.get("vendor_url")),
            "price_cny": clean(detail.get("price_cny")) or clean(base.get("price_cny")),
            "moq": detail_moq(detail) or clean(base.get("moq")),
            "monthly_sales": clean(detail.get("monthly_sales")) or clean(base.get("monthly_sales")),
            "sales_context": clean(detail.get("sales_context")) or clean(base.get("sales_context")),
            "repurchase_rate_pct": clean(detail.get("repurchase_rate_pct")) or clean(base.get("repurchase_rate_pct")),
            "rating": clean(detail.get("rating")) or clean(base.get("rating")),
            # Search-card values and unscoped whole-page matches are never trusted as company tenure.
            "years_on_1688": tenure_years,
            "years_on_1688_scope": tenure_scope,
            "years_on_1688_label": tenure_label,
            "badges": merge_unique(clean(base.get("badges")), clean(detail.get("badges"))),
            "service_flags": merge_unique(clean(base.get("service_flags")), clean(detail.get("service_flags"))),
            "dropship_supported": clean(detail.get("dropship_supported")) or clean(base.get("dropship_supported")),
            "size_chart": clean(detail.get("size_chart")) or clean(base.get("size_chart")),
            "availability": clean(detail.get("availability")) or clean(base.get("availability")),
            "ip_risk_flags": merge_unique(clean(base.get("ip_risk_flags")), detail_ip_risk_flags(detail)),
            "image_url": image_urls[0] if image_urls else clean(base.get("image_url")),
            "vendor_image_urls": " | ".join(image_urls),
            "vendor_images_path": relative(image_dir),
            "detail_evidence_path": relative(evidence_path),
            # Keep search-card evidence product-scoped. The full detail text is
            # retained in detail-evidence.json, but it also contains platform
            # disclaimers that must not become product/IP/category signals.
            "raw_card_text": clean(base.get("raw_card_text")) or detail_product_title(base, detail),
            "notes": merge_unique(
                clean(base.get("notes")),
                f"Detail enriched from logged-in 1688 page: {detail.get('page_url', '')}",
            ),
            "image_quality": "5" if len(image_urls) >= 4 else ("4" if image_urls else clean(base.get("image_quality"))),
        }
    )
    return row


def run_scorer(candidate_path: Path, output_dir: Path) -> dict[str, Any]:
    subprocess.run(
        [
            "python3",
            str(SCORER_PATH),
            "--input",
            str(candidate_path),
            "--output-dir",
            str(output_dir),
            "--stage",
            "detail",
            "--decision-state",
            str(DECISIONS_PATH),
        ],
        cwd=str(REPO_ROOT),
        check=True,
    )
    scored = read_json(output_dir / "scored-candidates.json", {})
    candidates = scored.get("candidates", []) if isinstance(scored, dict) else []
    return candidates[0] if candidates else {}


def update_decision_evidence(key: str, base: dict[str, Any], scored: dict[str, Any], output_dir: Path, image_dir: Path) -> None:
    decisions = read_json(DECISIONS_PATH, {"version": 1, "updated_at": "", "items": {}})
    decisions.setdefault("version", 1)
    decisions.setdefault("items", {})
    items = decisions["items"]
    existing = items.get(key, {})
    if not isinstance(existing, dict):
        existing = {}
    evidence = existing.get("evidence", {})
    if not isinstance(evidence, dict):
        evidence = {}
    service = clean(scored.get("service_flags"))
    vendor_summary = " | ".join(
        value
        for value in [
            clean(scored.get("vendor_name")),
            clean(scored.get("badges")),
            f"{clean(scored.get('years_on_1688'))} years" if clean(scored.get("years_on_1688")) else "",
            f"rating {clean(scored.get('rating'))}" if clean(scored.get("rating")) else "",
        ]
        if value
    )
    if clean(scored.get("size_chart")):
        evidence["size_chart_source"] = f"1688 detail page detected size chart text: {scored.get('product_url', '')}"
    if clean(scored.get("vendor_images_path")):
        evidence["vendor_images_path"] = relative(image_dir)
    if clean(scored.get("dropship_supported")):
        evidence["dropship_confirmed"] = clean(scored.get("dropship_supported"))
    dispatch_evidence = dispatch_evidence_label(service)
    if dispatch_evidence:
        evidence["dispatch_confirmed"] = dispatch_evidence
    else:
        evidence.pop("dispatch_confirmed", None)
    if vendor_summary:
        evidence["supplier_confirmed"] = vendor_summary
    evidence["detail_evidence_path"] = relative(output_dir / "detail-evidence.json")
    evidence["detail_verdict"] = clean(scored.get("verdict"))
    evidence["detail_score"] = str(scored.get("score", ""))
    note = (
        f"Detail enrichment {now_iso()}: verdict {scored.get('verdict')} score {scored.get('score')}. "
        f"Run: {relative(output_dir)}"
    )
    evidence["notes"] = merge_unique(clean(evidence.get("notes")), note)
    existing.update(
        {
            "action": existing.get("action", ""),
            "product_url": clean(scored.get("product_url")) or clean(base.get("product_url")),
            "title": clean(scored.get("title")) or clean(base.get("title")),
            "category_id": clean(scored.get("category_id")) or clean(base.get("category_id")),
            "run_id": clean(scored.get("run_id")) or clean(base.get("run_id")),
            "verdict": clean(scored.get("verdict")),
            "score": scored.get("score", ""),
            "evidence": evidence,
            "updated_at": now_iso(),
        }
    )
    items[key] = existing
    decisions["updated_at"] = now_iso()
    write_json(DECISIONS_PATH, decisions)


def vendor_key(scored: dict[str, Any]) -> str:
    vendor_url = clean(scored.get("vendor_url"))
    if vendor_url:
        parsed = urllib.parse.urlparse(vendor_url)
        compact = f"{parsed.netloc}{parsed.path}".strip("/")
        if compact:
            return hashlib.sha1(compact.encode("utf-8")).hexdigest()[:16]
    vendor_name = clean(scored.get("vendor_name"))
    if vendor_name:
        return hashlib.sha1(vendor_name.encode("utf-8")).hexdigest()[:16]
    return ""


def update_vendor_database(key: str, base: dict[str, Any], scored: dict[str, Any]) -> None:
    supplier_key = vendor_key(scored)
    if not supplier_key:
        return
    payload = read_json(VENDORS_PATH, {"version": 1, "updated_at": "", "vendors": {}})
    payload.setdefault("version", 1)
    payload.setdefault("vendors", {})
    vendors = payload["vendors"]
    record = vendors.get(supplier_key, {})
    if not isinstance(record, dict):
        record = {}
    offer_keys = set(record.get("offer_keys", []))
    categories = set(record.get("categories", []))
    offer_keys.add(key)
    if clean(scored.get("category_id")) or clean(base.get("category_id")):
        categories.add(clean(scored.get("category_id")) or clean(base.get("category_id")))
    verdict_counts = record.get("verdict_counts", {})
    if not isinstance(verdict_counts, dict):
        verdict_counts = {}
    verdict = clean(scored.get("verdict")) or "Unknown"
    verdict_counts[verdict] = int(verdict_counts.get(verdict, 0)) + 1
    record.update(
        {
            "vendor_name": clean(scored.get("vendor_name")) or record.get("vendor_name", ""),
            "vendor_url": clean(scored.get("vendor_url")) or record.get("vendor_url", ""),
            "badges": merge_unique(clean(record.get("badges")), clean(scored.get("badges"))),
            "service_flags": merge_unique(clean(record.get("service_flags")), clean(scored.get("service_flags"))),
            "years_on_1688": clean(scored.get("years_on_1688")) or record.get("years_on_1688", ""),
            "years_on_1688_scope": clean(scored.get("years_on_1688_scope")) or record.get("years_on_1688_scope", ""),
            "years_on_1688_label": clean(scored.get("years_on_1688_label")) or record.get("years_on_1688_label", ""),
            "rating": clean(scored.get("rating")) or record.get("rating", ""),
            "offer_keys": sorted(offer_keys),
            "categories": sorted(category for category in categories if category),
            "verdict_counts": verdict_counts,
            "last_seen_at": now_iso(),
        }
    )
    vendors[supplier_key] = record
    payload["updated_at"] = now_iso()
    write_json(VENDORS_PATH, payload)


def enrich_one(client: CdpClient, base: dict[str, Any]) -> dict[str, Any]:
    product_url = clean(base.get("product_url"))
    key = clean(base.get("key")) or offer_key(product_url)
    if not product_url or not key:
        raise SystemExit("Selected candidate is missing a 1688 product URL.")
    output_dir = DETAIL_ROOT / key
    output_dir.mkdir(parents=True, exist_ok=True)
    detail = collect_detail(client, product_url)
    image_dir = download_images(detail.get("image_urls", []), key, product_url)
    evidence_path = output_dir / "detail-evidence.json"
    write_json(evidence_path, {"base_candidate": base, "detail": detail, "image_dir": relative(image_dir)})
    row = enriched_row(base, detail, image_dir, evidence_path)
    candidate_path = output_dir / "candidates.json"
    write_json(
        candidate_path,
        {
            "collected_at": now_iso(),
            "source": "1688 logged-in CDP detail page",
            "category_id": clean(row.get("category_id")),
            "candidates": [row],
        },
    )
    write_json(
        output_dir / "run.json",
        {
            "run_id": output_dir.name,
            "category_id": clean(row.get("category_id")),
            "source": "1688 logged-in CDP detail page",
            "stage": "detail",
            "product_url": product_url,
            "notes": "Collected by ops/scripts/1688_sourcing_detail_enrich.py from a logged-in browser session.",
        },
    )
    scored = run_scorer(candidate_path, output_dir)
    update_decision_evidence(key, base, scored, output_dir, image_dir)
    update_vendor_database(key, base, scored)
    return {"key": key, "output_dir": relative(output_dir), "verdict": scored.get("verdict"), "score": scored.get("score")}


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify 1688 detail-page proof for shortlisted candidates.")
    parser.add_argument("--key", default="", help="Specific 1688 offer ID to verify.")
    parser.add_argument("--category", default="", help="Category id to batch verify, or all.")
    parser.add_argument("--limit", type=int, default=3, help="Maximum candidates to verify in batch mode.")
    parser.add_argument("--port", type=int, default=9333, help="Local Chrome DevTools Protocol port.")
    args = parser.parse_args()

    candidates = selected_candidates(clean(args.key), clean(args.category), max(1, min(args.limit, 12)))
    if not candidates:
        raise SystemExit("No matching shortlisted candidates found for detail enrichment.")

    client = CdpClient(args.port)
    results: list[dict[str, Any]] = []
    try:
        for candidate in candidates:
            results.append(enrich_one(client, candidate))
    finally:
        client.close()

    for result in results:
        print(f"{result['output_dir']} detail_verdict={result.get('verdict')} score={result.get('score')}")
    print(f"enriched={len(results)}")


if __name__ == "__main__":
    main()
