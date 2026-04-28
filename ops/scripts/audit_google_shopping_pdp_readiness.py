#!/usr/bin/env python3
"""Run read-only storefront PDP readiness QA for Shopping candidate products.

The script selects locally viable candidate variants, audits each unique product
page, performs a disposable Shopify AJAX add-to-cart check for one available
candidate variant per product, clears that anonymous cart session, and writes
variant-level PDP evidence for the clean-subset generator.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import time
import urllib.request
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable
from urllib import parse

import requests
import websocket
from bs4 import BeautifulSoup


DEFAULT_MASTER = Path(
    "dresslikemommy-growth-2026/02_AUDIT_PACKETS/"
    "2026-04-28-google-shopping-us-clean-subset_REVIEW_ONLY/google_shopping_us_clean_subset_master.csv"
)
DEFAULT_OUTPUT_DIR = Path(
    "dresslikemommy-growth-2026/02_AUDIT_PACKETS/"
    "2026-04-28-google-shopping-us-clean-subset_REVIEW_ONLY"
)
DEFAULT_STOREFRONT = "https://www.dresslikemommy.com"
DESKTOP_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
)
LOCAL_BLOCKER_PREFIXES = (
    "exclude_unknown_price",
    "exclude_unknown_margin",
    "exclude_missing_sku",
    "exclude_missing_gtin",
    "exclude_inventory_needs_data",
    "exclude_out_of_stock",
    "exclude_low_aov_no_multi_item_order",
    "exclude_weak_initial_collection_",
)
FETCH_BLOCKER_STATUS = {0, 408, 425, 429, 500, 502, 503, 504}

EVIDENCE_FIELDNAMES = [
    "merchant_center_item_id",
    "shopify_product_id",
    "shopify_variant_id",
    "handle",
    "product_url",
    "pdp_status",
    "pdp_issue_count",
    "pdp_issues",
    "page_load_status",
    "product_json_status",
    "image_status",
    "price_status",
    "variant_selection_status",
    "add_to_cart_status",
    "subscription_deferred_status",
    "delivery_estimate_status",
    "trust_claim_status",
    "shipping_returns_status",
    "size_guide_status",
    "review_state_status",
    "us_experience_status",
    "sample_variant_id",
    "sample_variant_available",
    "http_status",
    "final_url",
    "product_json_variant_count",
    "product_json_available_variant_count",
    "notes",
]

PRODUCT_FIELDNAMES = [
    "shopify_product_id",
    "handle",
    "title",
    "product_family",
    "product_url",
    "pdp_status",
    "pdp_issue_count",
    "pdp_issues",
    "sample_variant_id",
    "sample_variant_title",
    "sample_variant_price",
    "variant_rows_covered",
    "http_status",
    "final_url",
    "add_to_cart_status",
    "notes",
]


@dataclass
class HttpResult:
    status_code: int
    final_url: str
    text: str
    error: str


class CdpFetcher:
    def __init__(self, cdp_base_url: str, start_url: str):
        self.cdp_base_url = cdp_base_url.rstrip("/")
        create_url = f"{self.cdp_base_url}/json/new?{parse.quote(start_url, safe=':/?=&')}"
        req = urllib.request.Request(create_url, method="PUT")
        self.target = json.loads(urllib.request.urlopen(req, timeout=10).read().decode("utf-8"))
        self.ws = websocket.create_connection(
            self.target["webSocketDebuggerUrl"],
            timeout=60,
            suppress_origin=True,
        )
        self.next_id = 1
        self.command("Page.enable")
        self.command("Runtime.enable")
        self.command("Page.navigate", {"url": start_url})
        time.sleep(1.0)

    def command(self, method: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        command_id = self.next_id
        self.next_id += 1
        self.ws.send(json.dumps({"id": command_id, "method": method, "params": params or {}}))
        while True:
            message = json.loads(self.ws.recv())
            if message.get("id") == command_id:
                return message

    def evaluate(self, expression: str) -> Any:
        response = self.command(
            "Runtime.evaluate",
            {"expression": expression, "awaitPromise": True, "returnByValue": True},
        )
        result = response.get("result", {}).get("result", {})
        if "exceptionDetails" in response.get("result", {}):
            raise RuntimeError(clean(response["result"]["exceptionDetails"]))
        return result.get("value")

    def fetch_text(self, url: str, *, accept: str = "*/*") -> HttpResult:
        expression = f"""
        (async () => {{
          try {{
            const response = await fetch({json.dumps(url)}, {{
              credentials: 'include',
              headers: {{'Accept': {json.dumps(accept)}}}
            }});
            const text = await response.text();
            return {{status: response.status, url: response.url, text}};
          }} catch (error) {{
            return {{status: 0, url: {json.dumps(url)}, text: '', error: String(error)}};
          }}
        }})()
        """
        value = self.evaluate(expression) or {}
        return HttpResult(
            int(value.get("status") or 0),
            clean(value.get("url") or url),
            value.get("text") or "",
            clean(value.get("error")),
        )

    def rendered_text(self, url: str) -> str:
        self.command("Page.navigate", {"url": url})
        time.sleep(4.0)
        value = self.evaluate("document.body ? document.body.innerText : ''")
        return clean(value)

    def add_to_cart(self, variant_id: str) -> tuple[str, str]:
        expression = f"""
        (async () => {{
          try {{
            const body = new URLSearchParams({{id: {json.dumps(variant_id)}, quantity: '1'}});
            const response = await fetch('/cart/add.js', {{
              method: 'POST',
              credentials: 'include',
              headers: {{'Accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}},
              body
            }});
            const text = await response.text();
            await fetch('/cart/clear.js', {{method: 'POST', credentials: 'include'}}).catch(() => null);
            return {{status: response.status, text}};
          }} catch (error) {{
            return {{status: 0, text: String(error)}};
          }}
        }})()
        """
        value = self.evaluate(expression) or {}
        status = int(value.get("status") or 0)
        return ("PASS" if status == 200 else "FAIL", "" if status == 200 else f"HTTP {status}: {clean(value.get('text'))[:240]}")

    def close(self) -> None:
        try:
            self.ws.close()
        finally:
            target_id = self.target.get("id")
            if target_id:
                try:
                    urllib.request.urlopen(f"{self.cdp_base_url}/json/close/{target_id}", timeout=5).read()
                except Exception:  # noqa: BLE001
                    pass


def clean(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip())


def normalize(value: object) -> str:
    return re.sub(r"[^a-z0-9]+", "_", clean(value).lower()).strip("_")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: Iterable[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def product_handle(product_url: str) -> str:
    path = parse.urlparse(product_url).path.strip("/")
    if path.startswith("products/"):
        return path.split("/", 1)[1]
    return path.rsplit("/", 1)[-1]


def local_viable(row: dict[str, str]) -> bool:
    reasons = [reason for reason in row.get("exclusion_reason", "").split(";") if reason]
    return not any(reason.startswith(LOCAL_BLOCKER_PREFIXES) for reason in reasons)


def select_candidates(master_rows: list[dict[str, str]], limit_products: int) -> list[dict[str, str]]:
    candidates = [row for row in master_rows if local_viable(row)]
    family_priority = {
        "mommy_me": 0,
        "family_matching": 1,
        "pajamas": 2,
        "swimsuits": 3,
        "daddy_me": 4,
        "dresses": 5,
        "other": 6,
    }
    products: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in candidates:
        products[row["shopify_product_id"]].append(row)

    ranked_products = sorted(
        products.values(),
        key=lambda rows: (
            family_priority.get(rows[0].get("product_family"), 99),
            -max(float(row.get("price") or 0) for row in rows),
            rows[0].get("title", ""),
        ),
    )
    if limit_products > 0:
        ranked_products = ranked_products[:limit_products]
    selected: list[dict[str, str]] = []
    for rows in ranked_products:
        selected.extend(rows)
    return selected


def get_url(session: requests.Session, url: str) -> HttpResult:
    last = HttpResult(0, url, "", "")
    for attempt in range(3):
        try:
            response = session.get(url, timeout=30, allow_redirects=True)
            last = HttpResult(response.status_code, response.url, response.text, "")
            if response.status_code not in {429, 503}:
                return last
            retry_after = response.headers.get("Retry-After")
            delay = int(retry_after) if retry_after and retry_after.isdigit() else 5 * (attempt + 1)
        except Exception as exc:  # noqa: BLE001
            last = HttpResult(0, url, "", clean(str(exc)))
            delay = 5 * (attempt + 1)
        time.sleep(delay)
    return last


def visible_text(html: str) -> str:
    soup = BeautifulSoup(html or "", "html.parser")
    for tag in soup(["script", "style", "noscript", "svg", "template"]):
        tag.decompose()
    for tag in soup.select(
        "[hidden], [aria-hidden='true'], #shopify-buyer-consent, "
        ".shopify-buyer-consent, [data-consent-type='subscription']"
    ):
        tag.decompose()
    for tag in list(soup.find_all(style=True)):
        if tag.attrs is None:
            continue
        style = re.sub(r"\s+", "", tag.get("style", "").lower())
        if "display:none" in style or "visibility:hidden" in style:
            tag.decompose()
    return clean(soup.get_text(" "))


def parse_html_checks(html: str) -> dict[str, bool]:
    soup = BeautifulSoup(html or "", "html.parser")
    return {
        "has_product_form": bool(soup.select('form[action*="/cart/add"], product-form')),
        "has_variant_input": bool(soup.select('input[name="id"], select[name="id"], variant-selects, variant-radios')),
        "has_add_button": bool(soup.select('button[name="add"], .product-form__submit')),
        "has_size_guide": bool(re.search(r"size (guide|chart)|compare family sizes", visible_text(html), re.I)),
        "has_us_currency": bool(re.search(r"United States\\s*\\|\\s*USD|USD|\\$\\d", visible_text(html), re.I)),
    }


def load_product_json(session: requests.Session, product_url: str) -> tuple[dict[str, Any], str]:
    url = product_url.rstrip("/") + ".js"
    last_error = ""
    for attempt in range(3):
        try:
            response = session.get(url, timeout=30, headers={"Accept": "application/json"})
            if response.status_code in {429, 503}:
                retry_after = response.headers.get("Retry-After")
                delay = int(retry_after) if retry_after and retry_after.isdigit() else 5 * (attempt + 1)
                last_error = f"HTTP {response.status_code}"
                time.sleep(delay)
                continue
            response.raise_for_status()
            return response.json(), ""
        except Exception as exc:  # noqa: BLE001
            last_error = clean(str(exc))
            time.sleep(5 * (attempt + 1))
    return {}, last_error


def load_product_json_cdp(cdp: CdpFetcher, product_url: str) -> tuple[dict[str, Any], str]:
    result = cdp.fetch_text(product_url.rstrip("/") + ".js", accept="application/json")
    if result.status_code != 200:
        return {}, f"HTTP {result.status_code}: {result.text[:240]}"
    try:
        return json.loads(result.text), ""
    except json.JSONDecodeError as exc:
        return {}, clean(str(exc))


def format_price(cents: int | float | str) -> str:
    try:
        value = int(cents)
    except (TypeError, ValueError):
        return ""
    return f"${value / 100:,.2f}"


def first_available_candidate_variant(
    product_json: dict[str, Any],
    candidate_rows: list[dict[str, str]],
) -> dict[str, Any]:
    candidate_ids = {clean(row.get("shopify_variant_id")) for row in candidate_rows}
    for variant in product_json.get("variants") or []:
        if clean(variant.get("id")) in candidate_ids and variant.get("available"):
            return variant
    for variant in product_json.get("variants") or []:
        if clean(variant.get("id")) in candidate_ids:
            return variant
    return {}


def add_to_cart_check(session: requests.Session, variant_id: str) -> tuple[str, str]:
    if not variant_id:
        return "FAIL", "No candidate variant ID available for add-to-cart test."
    last_note = ""
    for attempt in range(3):
        try:
            response = session.post(
                "https://www.dresslikemommy.com/cart/add.js",
                data={"id": variant_id, "quantity": "1"},
                timeout=30,
                headers={"Accept": "application/json"},
            )
            if response.status_code == 200:
                try:
                    session.post("https://www.dresslikemommy.com/cart/clear.js", timeout=15)
                except Exception:  # noqa: BLE001
                    pass
                return "PASS", ""
            last_note = f"HTTP {response.status_code}: {clean(response.text)[:240]}"
            if response.status_code not in {429, 503}:
                break
            retry_after = response.headers.get("Retry-After")
            delay = int(retry_after) if retry_after and retry_after.isdigit() else 5 * (attempt + 1)
            time.sleep(delay)
        except Exception as exc:  # noqa: BLE001
            last_note = clean(str(exc))
            time.sleep(5 * (attempt + 1))
        finally:
            try:
                session.post("https://www.dresslikemommy.com/cart/clear.js", timeout=15)
            except Exception:  # noqa: BLE001
                pass
    return "FAIL", last_note


def text_has_any(text: str, patterns: list[str]) -> bool:
    return any(re.search(pattern, text, flags=re.I) for pattern in patterns)


def has_delivery_estimate(text: str) -> bool:
    if not text_has_any(text, [r"\b(delivery|shipping|arrives?|business days?)\b"]):
        return False
    return text_has_any(
        text,
        [
            r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2}",
            r"\b\d+\s*[-–]\s*\d+\s+business days\b",
            r"\b\d+\s+business days\b",
        ],
    )


def audit_product(
    product_rows: list[dict[str, str]],
    pause_ms: int,
    *,
    cdp: CdpFetcher | None = None,
) -> tuple[dict[str, str], list[dict[str, str]]]:
    first = product_rows[0]
    product_url = first["product_url"]
    session = requests.Session()
    session.headers.update({"User-Agent": DESKTOP_UA})
    if cdp:
        page = cdp.fetch_text(product_url, accept="text/html,application/xhtml+xml")
        product_json, product_json_error = load_product_json_cdp(cdp, product_url)
        rendered_page_text = cdp.rendered_text(product_url)
    else:
        page = get_url(session, product_url)
        product_json, product_json_error = load_product_json(session, product_url)
        rendered_page_text = ""
    text = rendered_page_text or visible_text(page.text)
    html_checks = parse_html_checks(page.text)
    if rendered_page_text:
        html_checks["has_size_guide"] = bool(
            re.search(r"size (guide|chart)|compare family sizes|your size details", rendered_page_text, re.I)
        )
    sample_variant = first_available_candidate_variant(product_json, product_rows)
    sample_variant_id = clean(sample_variant.get("id"))
    add_status, add_note = cdp.add_to_cart(sample_variant_id) if cdp else add_to_cart_check(session, sample_variant_id)

    variants = product_json.get("variants") or []
    available_variants = [variant for variant in variants if variant.get("available")]
    images = product_json.get("images") or []
    media = product_json.get("media") or []
    price_text = format_price(product_json.get("price_min") or product_json.get("price"))

    issues: list[str] = []
    status_fields: dict[str, str] = {}
    notes: list[str] = []
    verification_blocked = page.status_code in FETCH_BLOCKER_STATUS
    if verification_blocked:
        issues.append(f"pdp_fetch_blocked_http_{page.status_code}")
        if page.error:
            notes.append(page.error)

    same_domain = parse.urlparse(page.final_url).netloc.endswith("dresslikemommy.com")
    status_fields["page_load_status"] = (
        "NEEDS_DATA" if verification_blocked else "PASS" if page.status_code == 200 and same_domain else "FAIL"
    )
    if status_fields["page_load_status"] == "FAIL":
        issues.append(f"page_load_http_{page.status_code}")
        if page.error:
            notes.append(page.error)

    product_json_blocked = product_json_error.startswith("HTTP 429") or product_json_error.startswith("HTTP 503")
    verification_blocked = verification_blocked or product_json_blocked
    status_fields["product_json_status"] = (
        "NEEDS_DATA" if product_json_blocked else "PASS" if product_json and variants else "FAIL"
    )
    if product_json_blocked:
        issues.append("product_json_fetch_blocked")
    if status_fields["product_json_status"] == "FAIL":
        issues.append("product_json_missing_or_empty")
        if product_json_error:
            notes.append(product_json_error)

    status_fields["image_status"] = "NEEDS_DATA" if verification_blocked else "PASS" if images or media else "FAIL"
    if status_fields["image_status"] == "FAIL":
        issues.append("product_image_missing")

    status_fields["price_status"] = "NEEDS_DATA" if verification_blocked else "PASS" if price_text and price_text in text else "FAIL"
    if status_fields["price_status"] == "FAIL":
        issues.append("price_not_clear_on_pdp")

    variant_ui_ok = html_checks["has_product_form"] and html_checks["has_variant_input"] and html_checks["has_add_button"]
    status_fields["variant_selection_status"] = "NEEDS_DATA" if verification_blocked else "PASS" if variant_ui_ok else "FAIL"
    if status_fields["variant_selection_status"] == "FAIL":
        issues.append("variant_selection_or_add_button_unclear")

    status_fields["add_to_cart_status"] = "NEEDS_DATA" if verification_blocked and add_status == "FAIL" else add_status
    if add_status != "PASS":
        issues.append("add_to_cart_needs_data" if verification_blocked else "add_to_cart_failed")
        if add_note:
            notes.append(add_note)

    subscription_confusion = text_has_any(
        text,
        [
            r"deferred, subscription, or recurring purchase",
            r"recurring purchase",
            r"subscription",
            r"authorize you to charge my payment method",
        ],
    )
    status_fields["subscription_deferred_status"] = (
        "NEEDS_DATA" if verification_blocked else "FAIL" if subscription_confusion else "PASS"
    )
    if subscription_confusion:
        issues.append("recurring_subscription_deferred_text_present")

    checkout_only_delivery = re.search(r"Delivery details at checkout", text, flags=re.I)
    delivery_estimate_visible = has_delivery_estimate(text)
    status_fields["delivery_estimate_status"] = (
        "NEEDS_DATA" if verification_blocked else "PASS" if delivery_estimate_visible and not checkout_only_delivery else "FAIL"
    )
    if status_fields["delivery_estimate_status"] == "FAIL":
        issues.append("delivery_estimate_checkout_only_or_blank")

    unsupported_trust = text_has_any(
        text,
        [
            r"Delivery guaranteed",
            r"Secure Logistics",
            r"Full refund for your damaged or lost package",
            r"guaranteed: Accurate and precise order tracking",
        ],
    )
    status_fields["trust_claim_status"] = "NEEDS_DATA" if verification_blocked else "FAIL" if unsupported_trust else "PASS"
    if unsupported_trust:
        issues.append("unsupported_trust_or_guarantee_claim")

    conflicting_shipping_returns = text_has_any(
        text,
        [
            r"customs\\s+(fees|taxes|charges).*?(customer|buyer|responsibility)",
            r"duties\\s+(fees|taxes|charges).*?(customer|buyer|responsibility)",
            r"no returns.*30 days",
        ],
    )
    has_shipping_returns = text_has_any(text, [r"Shipping", r"Return Policy", r"Easy Returns"])
    status_fields["shipping_returns_status"] = (
        "NEEDS_DATA" if verification_blocked else "FAIL" if conflicting_shipping_returns or not has_shipping_returns else "PASS"
    )
    if conflicting_shipping_returns:
        issues.append("conflicting_shipping_customs_or_returns_language")
    elif not has_shipping_returns:
        issues.append("shipping_returns_copy_missing")

    status_fields["size_guide_status"] = "NEEDS_DATA" if verification_blocked else "PASS" if html_checks["has_size_guide"] else "FAIL"
    if status_fields["size_guide_status"] == "FAIL":
        issues.append("size_guide_missing_or_unclear")

    misleading_review_state = text_has_any(text, [r"\\d+\\s+reviews"]) and text_has_any(text, [r"No reviews"])
    status_fields["review_state_status"] = (
        "NEEDS_DATA" if verification_blocked else "FAIL" if misleading_review_state else "PASS"
    )
    if misleading_review_state:
        issues.append("review_state_misleading")

    status_fields["us_experience_status"] = "NEEDS_DATA" if verification_blocked else "PASS" if html_checks["has_us_currency"] else "FAIL"
    if status_fields["us_experience_status"] == "FAIL":
        issues.append("us_currency_market_not_clear")

    if sample_variant and not sample_variant.get("available"):
        issues.append("sample_candidate_variant_unavailable")

    issues = sorted(dict.fromkeys(issues))
    pdp_status = "NEEDS_DATA" if verification_blocked else "PASS" if not issues else "FAIL"
    if pause_ms > 0:
        time.sleep(pause_ms / 1000)

    product_summary = {
        "shopify_product_id": first["shopify_product_id"],
        "handle": product_handle(product_url),
        "title": first["title"],
        "product_family": first["product_family"],
        "product_url": product_url,
        "pdp_status": pdp_status,
        "pdp_issue_count": str(len(issues)),
        "pdp_issues": "|".join(issues),
        "sample_variant_id": sample_variant_id,
        "sample_variant_title": clean(sample_variant.get("title")),
        "sample_variant_price": format_price(sample_variant.get("price")),
        "variant_rows_covered": str(len(product_rows)),
        "http_status": str(page.status_code),
        "final_url": page.final_url,
        "add_to_cart_status": add_status,
        "notes": "|".join(dict.fromkeys(note for note in notes if note)),
    }
    evidence_rows: list[dict[str, str]] = []
    for row in product_rows:
        evidence_rows.append(
            {
                "merchant_center_item_id": row["merchant_center_item_id"],
                "shopify_product_id": row["shopify_product_id"],
                "shopify_variant_id": row["shopify_variant_id"],
                "handle": product_summary["handle"],
                "product_url": product_url,
                "pdp_status": pdp_status,
                "pdp_issue_count": str(len(issues)),
                "pdp_issues": "|".join(issues),
                **status_fields,
                "sample_variant_id": sample_variant_id,
                "sample_variant_available": str(bool(sample_variant.get("available"))).upper(),
                "http_status": str(page.status_code),
                "final_url": page.final_url,
                "product_json_variant_count": str(len(variants)),
                "product_json_available_variant_count": str(len(available_variants)),
                "notes": product_summary["notes"],
            }
        )
    return product_summary, evidence_rows


def build_outputs(
    master_csv: Path,
    output_dir: Path,
    limit_products: int,
    pause_ms: int,
    *,
    cdp_url: str = "",
) -> dict[str, object]:
    master_rows = read_csv(master_csv)
    candidate_rows = select_candidates(master_rows, limit_products)
    by_product: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in candidate_rows:
        by_product[row["shopify_product_id"]].append(row)

    product_rows: list[dict[str, str]] = []
    evidence_rows: list[dict[str, str]] = []
    cdp = CdpFetcher(cdp_url, DEFAULT_STOREFRONT) if cdp_url else None
    try:
        for rows in by_product.values():
            product_summary, variant_evidence = audit_product(rows, pause_ms, cdp=cdp)
            product_rows.append(product_summary)
            evidence_rows.extend(variant_evidence)
    finally:
        if cdp:
            cdp.close()

    output_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "pdp_evidence": output_dir / "pdp_shopping_qa_evidence.csv",
        "product_summary": output_dir / "pdp_shopping_qa_product_summary.csv",
        "summary": output_dir / "pdp_shopping_qa_summary.json",
    }
    write_csv(paths["pdp_evidence"], EVIDENCE_FIELDNAMES, evidence_rows)
    write_csv(paths["product_summary"], PRODUCT_FIELDNAMES, product_rows)

    issue_counts = Counter(
        issue
        for row in product_rows
        for issue in row["pdp_issues"].split("|")
        if issue
    )
    summary = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "mode": "READ_ONLY_PDP_SHOPPING_QA",
        "fetch_mode": "chrome_devtools_browser_context" if cdp_url else "python_requests",
        "master_csv": str(master_csv),
        "candidate_variant_rows": len(candidate_rows),
        "candidate_products": len(by_product),
        "pdp_evidence_rows": len(evidence_rows),
        "pdp_pass_products": sum(1 for row in product_rows if row["pdp_status"] == "PASS"),
        "pdp_fail_products": sum(1 for row in product_rows if row["pdp_status"] == "FAIL"),
        "pdp_pass_variant_rows": sum(1 for row in evidence_rows if row["pdp_status"] == "PASS"),
        "pdp_fail_variant_rows": sum(1 for row in evidence_rows if row["pdp_status"] == "FAIL"),
        "top_pdp_issues": dict(issue_counts.most_common(20)),
        "outputs": {key: str(path) for key, path in paths.items()},
    }
    paths["summary"].write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--master-csv", type=Path, default=DEFAULT_MASTER)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--limit-products", type=int, default=0)
    parser.add_argument("--pause-ms", type=int, default=150)
    parser.add_argument("--cdp-url", default="", help="Optional Chrome DevTools HTTP base URL, for example http://127.0.0.1:9222.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary = build_outputs(args.master_csv, args.output_dir, args.limit_products, args.pause_ms, cdp_url=args.cdp_url)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
