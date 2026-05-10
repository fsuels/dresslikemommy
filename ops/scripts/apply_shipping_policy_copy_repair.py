#!/usr/bin/env python3
"""Apply the approved 2026-05-07 shipping/policy copy repair.

This script is intentionally narrow:
- Shopify policies: Shipping Policy and Terms of Service body copy only.
- Shopify page: Shipping Info page body copy only.
- No theme, product, market, shipping-rate, feed, campaign, budget, or checkout
  setting changes.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib import error, request

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops.scripts.shopify_admin_config import load_access_token, resolve_store_domain  # noqa: E402


API_VERSION = "2026-01"
TIMEOUT_SECONDS = 90
SHIPPING_INFO_PAGE_ID = 86424617057
LEGACY_SHIPPING_PAGE_ID = 161928901
DEFAULT_ARTIFACT_DIR = Path(
    "dresslikemommy-growth-2026/02_AUDIT_PACKETS/"
    "2026-05-07-shipping-policy-copy-repair-applied"
)

PUBLIC_URLS = {
    "shipping_policy": "https://www.dresslikemommy.com/policies/shipping-policy",
    "shipping_info": "https://www.dresslikemommy.com/pages/shipping-info",
    "terms_of_service": "https://www.dresslikemommy.com/policies/terms-of-service",
    "legacy_shipping_page": "https://www.dresslikemommy.com/pages/shipping-and-delivery",
}

BLOCKER_PHRASES = [
    "We currently ship to:",
    "We ship to the United States, Canada, United Kingdom, and Australia",
    "Don't see your country?",
    "Don\u2019t see your country?",
    "we ship matching family outfits to families worldwide",
    "All prices are in USD unless otherwise noted",
    "Standard shipping is free when a free standard method is shown",
    "Free And Paid Shipping Options",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def clean_text(value: str) -> str:
    text = re.sub(r"(?is)<(script|style).*?</\1>", " ", value or "")
    text = re.sub(r"(?s)<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def request_json(
    *,
    method: str,
    url: str,
    token: str,
    payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    headers = {
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": token,
    }
    req = request.Request(url, data=data, headers=headers, method=method)
    for attempt in range(5):
        try:
            with request.urlopen(req, timeout=TIMEOUT_SECONDS) as response:
                return json.loads(response.read().decode("utf-8"))
        except error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            if exc.code in {429, 500, 502, 503, 504} and attempt < 4:
                time.sleep(2**attempt)
                continue
            if exc.code == 401:
                raise RuntimeError("Stored Shopify Admin token requires regeneration/reinstall: 401") from exc
            raise RuntimeError(f"Shopify HTTP {exc.code}: {body[:1000]}") from exc
    raise RuntimeError(f"Shopify request failed after retries: {method} {url}")


def graphql(
    *,
    store_domain: str,
    token: str,
    query: str,
    variables: dict[str, Any] | None = None,
) -> dict[str, Any]:
    url = f"https://{store_domain}/admin/api/{API_VERSION}/graphql.json"
    payload = {"query": query, "variables": variables or {}}
    data = request_json(method="POST", url=url, token=token, payload=payload)
    if data.get("errors"):
        raise RuntimeError(f"Shopify GraphQL errors: {data['errors']}")
    return data["data"]


def public_get(url: str) -> dict[str, Any]:
    req = request.Request(
        url,
        headers={
            "Accept": "text/html,*/*",
            "User-Agent": "DressLikeMommyOps/1.0 (+policy readback)",
        },
    )
    try:
        with request.urlopen(req, timeout=TIMEOUT_SECONDS) as response:
            body = response.read().decode("utf-8", errors="replace")
            return {
                "url": url,
                "final_url": response.geturl(),
                "http_status": response.status,
                "body": body,
            }
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        return {
            "url": url,
            "final_url": exc.geturl(),
            "http_status": exc.code,
            "body": body,
        }


def shipping_policy_body() -> str:
    return """<h1>Shipping Policy</h1>
<p><strong>Last Updated:</strong> January 28, 2026</p>
<p>At <strong>Dress Like Mommy</strong>, we want your matching outfits to arrive as clearly and reliably as possible. Review the shipping method, rate, and delivery estimate shown at checkout before placing an order.</p>

<h2>Where We Ship</h2>
<p>Shipping is available to the countries and regions shown at checkout. Availability depends on the destination, product, and shipping methods shown during checkout. Use the country/region selector or the checkout shipping step to confirm whether we can ship to your address before placing an order.</p>
<p>If your destination does not appear at checkout, or if no shipping method is shown for your address, contact us at <a href="mailto:info@dresslikemommy.com">info@dresslikemommy.com</a> before ordering.</p>

<h2>Shipping Rates</h2>
<p>Standard shipping is included in product prices for countries and regions where a standard method is available. Checkout shows the exact method, delivery estimate, and any express upgrade before payment.</p>

<h2>Processing Time</h2>
<p>Orders are processed within 1-3 business days after payment confirmation. During holidays, promotions, or high-volume periods, processing may take an additional 1-2 business days.</p>
<p>You will receive an email with tracking information once your order ships.</p>

<h2>Delivery Times</h2>
<p>Orders are processed within 1-3 business days after payment confirmation. Delivery estimates vary by destination, carrier, customs processing, and the shipping method shown at checkout.</p>
<ul>
  <li><strong>Standard Delivery:</strong> the current checkout estimate displays before payment.</li>
  <li><strong>Express Delivery:</strong> available for some destinations where shown at checkout.</li>
</ul>
<p>These are estimates. Actual delivery times may vary because of customs processing, carrier delays, weather, holidays, or local conditions.</p>

<h2>How Our Shipping Works</h2>
<ol>
  <li><strong>Order Placed:</strong> you receive an order confirmation email.</li>
  <li><strong>Order Processing:</strong> your order is prepared after payment confirmation.</li>
  <li><strong>Shipped:</strong> tracking information is emailed when available.</li>
  <li><strong>In Transit:</strong> use the tracking link for carrier updates.</li>
  <li><strong>Delivered:</strong> your package is delivered to the address provided at checkout.</li>
</ol>

<h2>Order Tracking</h2>
<p>Every order includes a tracking number when the carrier provides one. Tracking may take 24-48 hours to update after the number is issued.</p>
<p>You can also check your order status anytime by visiting our <a href="https://dresslikemommy.com/account">Order Status</a> page.</p>

<h2>Customs, Duties, And Import Taxes</h2>
<p>For orders shipped outside the United States, your destination country or carrier may collect import duties, taxes, brokerage fees, or customs charges. These charges are the customer's responsibility unless checkout explicitly says they are included.</p>
<p>We cannot predict these charges, mark orders as gifts, or lower the declared value of an order. Contact your local customs office for destination-specific guidance before ordering.</p>

<h2>Shipping Problems</h2>
<p>If your package is delayed, missing, or marked as delivered but not received, contact us at <a href="mailto:info@dresslikemommy.com">info@dresslikemommy.com</a> with your order number and tracking information. We will help review the carrier information and next available steps.</p>

<h2>Contact Us</h2>
<p>For shipping questions, email <a href="mailto:info@dresslikemommy.com">info@dresslikemommy.com</a>.</p>
"""


def shipping_info_body() -> str:
    return """<h2>Shipping Information</h2>
<p>At <strong>Dress Like Mommy</strong>, we are an online store that ships matching family outfits to destinations available at checkout through our shipping and fulfillment partners. Here is how to confirm shipping, delivery timing, and tracking before you place an order.</p>

<h3>Standard And Express Shipping Options</h3>
<p>Standard shipping is included in product prices for countries and regions where a standard method is available. Checkout shows the exact method, delivery estimate, and any express upgrade before payment.</p>

<h3>Where We Ship</h3>
<p>Shipping availability is based on the country/region and address entered at checkout. If checkout shows a shipping method for your address, we can ship there under the displayed method and rate.</p>
<p>If your destination does not appear at checkout, or if no shipping method is shown, email us at <a href="mailto:info@dresslikemommy.com">info@dresslikemommy.com</a> before ordering.</p>

<h3>Processing And Delivery Times</h3>
<p>Orders are processed within 1-3 business days after payment confirmation. During holidays, promotions, or high-volume periods, processing may take an additional 1-2 business days.</p>
<p>Delivery estimates vary by destination, carrier, customs processing, and the shipping method shown at checkout. Review the shipping method and estimate shown during checkout before placing your order.</p>
<p>Tracking may take 24-48 hours to update after the tracking number is issued.</p>

<h3>Order Tracking</h3>
<p>Once your order ships, check your email for tracking information. You can also visit your account or use the tracking link in the shipping confirmation email when available.</p>

<h3>Customs, Duties, And Import Taxes</h3>
<p>For orders outside the United States, your destination country or carrier may collect import duties, taxes, brokerage fees, or customs charges. These are the customer's responsibility unless checkout explicitly says they are included.</p>
<p>We cannot predict these charges, mark orders as gifts, or lower the declared value of an order. Contact your local customs office for destination-specific guidance before ordering.</p>

<h3>Shipping FAQ</h3>
<p><strong>Can I change my shipping address after ordering?</strong><br>Contact us as soon as possible at <a href="mailto:info@dresslikemommy.com">info@dresslikemommy.com</a>. If your order has not moved into fulfillment yet, we can review whether an address change is still possible.</p>
<p><strong>Do you ship to P.O. Boxes?</strong><br>Shipping availability for P.O. Boxes depends on the destination and carrier options shown at checkout.</p>
<p><strong>My package has not arrived yet.</strong><br>Check your tracking link first. If the tracking has not updated for several business days or the delivery estimate has passed, email us with your order number.</p>
"""


def update_terms_body(current_body: str) -> str:
    updated = current_body
    updated = re.sub(
        r"<li>\s*All prices are in\s*<strong>USD</strong>\s*unless otherwise noted\s*</li>",
        "<li>Prices display in the currency selected or shown at checkout unless otherwise noted.</li>",
        updated,
        count=1,
        flags=re.I,
    )
    shipping_section = """<h2>5. Shipping and Delivery</h2>
<ul>
  <li>Dress Like Mommy is an online store. Shipping is available to countries and regions where checkout shows an available shipping method for the address entered.</li>
  <li>Processing time is typically 1-3 business days after payment confirmation.</li>
  <li>Available shipping methods, rates, delivery estimates, taxes, and duties information are shown at checkout before payment where available.</li>
  <li>Standard shipping is included in product prices for countries and regions where a standard method is available.</li>
  <li>Express shipping may be available for some destinations where shown at checkout.</li>
  <li>Tracking information is provided by email once the order ships.</li>
  <li>We are not responsible for delays caused by customs, weather, holidays, carrier issues, or local delivery conditions.</li>
</ul>
<p>For full shipping details, see our <a href="https://www.dresslikemommy.com/pages/shipping-info">Shipping Information</a> page.</p>
"""
    updated = re.sub(
        r"<h2>\s*5\.\s*Shipping and Delivery\s*</h2>.*?(?=<h2>\s*6\.\s*Returns and Refunds\s*</h2>)",
        shipping_section,
        updated,
        count=1,
        flags=re.I | re.S,
    )
    return updated


def blocker_hits(body: str) -> list[str]:
    text = clean_text(body).lower()
    hits = []
    for phrase in BLOCKER_PHRASES:
        if phrase.lower() in text:
            hits.append(phrase)
    return hits


def fetch_policies(store_domain: str, token: str) -> list[dict[str, Any]]:
    base_url = f"https://{store_domain}/admin/api/{API_VERSION}"
    return request_json(method="GET", url=f"{base_url}/policies.json", token=token).get("policies", [])


def fetch_page(store_domain: str, token: str, page_id: int) -> dict[str, Any]:
    base_url = f"https://{store_domain}/admin/api/{API_VERSION}"
    return request_json(method="GET", url=f"{base_url}/pages/{page_id}.json", token=token)["page"]


def update_page(store_domain: str, token: str, page_id: int, body_html: str) -> None:
    base_url = f"https://{store_domain}/admin/api/{API_VERSION}"
    request_json(
        method="PUT",
        url=f"{base_url}/pages/{page_id}.json",
        token=token,
        payload={"page": {"id": page_id, "body_html": body_html}},
    )


def policy_body(policies: list[dict[str, Any]], handle: str) -> str:
    for policy in policies:
        if policy.get("handle") == handle:
            return str(policy.get("body") or "")
    raise RuntimeError(f"Could not find policy handle {handle}")


def update_policy(store_domain: str, token: str, policy_type: str, body: str) -> dict[str, Any]:
    mutation = """
mutation UpdateShopPolicy($shopPolicy: ShopPolicyInput!) {
  shopPolicyUpdate(shopPolicy: $shopPolicy) {
    shopPolicy {
      id
      type
      body
      url
    }
    userErrors {
      field
      message
    }
  }
}
"""
    data = graphql(
        store_domain=store_domain,
        token=token,
        query=mutation,
        variables={"shopPolicy": {"type": policy_type, "body": body}},
    )["shopPolicyUpdate"]
    errors = data.get("userErrors") or []
    if errors:
        raise RuntimeError(f"shopPolicyUpdate {policy_type} userErrors: {errors}")
    return data.get("shopPolicy") or {}


def public_readback(artifact_dir: Path) -> dict[str, Any]:
    results: dict[str, Any] = {}
    for key, url in PUBLIC_URLS.items():
        response = public_get(url)
        body = response.get("body") or ""
        write_text(artifact_dir / "public-readback" / f"{key}.html", body)
        results[key] = {
            "url": url,
            "final_url": response.get("final_url"),
            "http_status": response.get("http_status"),
            "text_excerpt": clean_text(body)[:1200],
            "blocker_hits": blocker_hits(body),
        }
    return results


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--store-domain", default="")
    parser.add_argument("--access-token", default="")
    parser.add_argument("--artifact-dir", type=Path, default=DEFAULT_ARTIFACT_DIR)
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--approval-note", default="")
    args = parser.parse_args()

    artifact_dir = args.artifact_dir
    artifact_dir.mkdir(parents=True, exist_ok=True)

    store_domain = resolve_store_domain(args.store_domain, fallback_domain="dresslikemommy-com.myshopify.com")
    token = load_access_token(args.access_token)
    policies = fetch_policies(store_domain, token)
    shipping_page = fetch_page(store_domain, token, SHIPPING_INFO_PAGE_ID)
    legacy_page = fetch_page(store_domain, token, LEGACY_SHIPPING_PAGE_ID)

    before = {
        "shipping_policy": policy_body(policies, "shipping-policy"),
        "terms_of_service": policy_body(policies, "terms-of-service"),
        "shipping_info_page": str(shipping_page.get("body_html") or ""),
        "legacy_shipping_page": str(legacy_page.get("body_html") or ""),
    }
    after = {
        "shipping_policy": shipping_policy_body(),
        "terms_of_service": update_terms_body(before["terms_of_service"]),
        "shipping_info_page": shipping_info_body(),
        "legacy_shipping_page": before["legacy_shipping_page"],
    }

    for key, body in before.items():
        write_text(artifact_dir / "before" / f"{key}.html", body)
    for key, body in after.items():
        write_text(artifact_dir / "after" / f"{key}.html", body)

    plan = {
        "generated_at": utc_now(),
        "mode": "execute" if args.execute else "dry-run",
        "approval_note": args.approval_note,
        "store_domain": store_domain,
        "targets": {
            "shipping_policy": {
                "policy_type": "SHIPPING_POLICY",
                "changed": before["shipping_policy"] != after["shipping_policy"],
                "before_sha256": sha256_text(before["shipping_policy"]),
                "after_sha256": sha256_text(after["shipping_policy"]),
                "before_blocker_hits": blocker_hits(before["shipping_policy"]),
                "after_blocker_hits": blocker_hits(after["shipping_policy"]),
            },
            "terms_of_service": {
                "policy_type": "TERMS_OF_SERVICE",
                "changed": before["terms_of_service"] != after["terms_of_service"],
                "before_sha256": sha256_text(before["terms_of_service"]),
                "after_sha256": sha256_text(after["terms_of_service"]),
                "before_blocker_hits": blocker_hits(before["terms_of_service"]),
                "after_blocker_hits": blocker_hits(after["terms_of_service"]),
            },
            "shipping_info_page": {
                "page_id": SHIPPING_INFO_PAGE_ID,
                "handle": shipping_page.get("handle"),
                "published_at": shipping_page.get("published_at"),
                "changed": before["shipping_info_page"] != after["shipping_info_page"],
                "before_sha256": sha256_text(before["shipping_info_page"]),
                "after_sha256": sha256_text(after["shipping_info_page"]),
                "before_blocker_hits": blocker_hits(before["shipping_info_page"]),
                "after_blocker_hits": blocker_hits(after["shipping_info_page"]),
            },
            "legacy_shipping_page": {
                "page_id": LEGACY_SHIPPING_PAGE_ID,
                "handle": legacy_page.get("handle"),
                "published_at": legacy_page.get("published_at"),
                "changed": False,
                "reason_not_changed": "Legacy page is unpublished; approval covered recheck, not redirect/update.",
                "before_blocker_hits": blocker_hits(before["legacy_shipping_page"]),
            },
        },
    }

    execution = {
        "execute": bool(args.execute),
        "applied": [],
        "skipped": [],
    }
    if args.execute:
        if plan["targets"]["shipping_policy"]["changed"]:
            update_policy(store_domain, token, "SHIPPING_POLICY", after["shipping_policy"])
            execution["applied"].append("shipping_policy")
        else:
            execution["skipped"].append("shipping_policy_unchanged")

        if plan["targets"]["terms_of_service"]["changed"]:
            update_policy(store_domain, token, "TERMS_OF_SERVICE", after["terms_of_service"])
            execution["applied"].append("terms_of_service")
        else:
            execution["skipped"].append("terms_of_service_unchanged")

        if plan["targets"]["shipping_info_page"]["changed"]:
            update_page(store_domain, token, SHIPPING_INFO_PAGE_ID, after["shipping_info_page"])
            execution["applied"].append("shipping_info_page")
        else:
            execution["skipped"].append("shipping_info_page_unchanged")

    time.sleep(1.0 if args.execute else 0.0)
    readback = public_readback(artifact_dir)
    result = {
        "plan": plan,
        "execution": execution,
        "public_readback": readback,
    }
    write_text(artifact_dir / "summary.json", json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
