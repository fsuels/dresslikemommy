#!/usr/bin/env python3
"""Repair high-risk Shopify page-content blockers.

Defaults to dry-run. Use --execute to write Admin page updates.
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

import requests


API_VERSION = "2026-01"
PAGE_IDS = {
    "faq": 161933381,
    "shipping": 161928901,
    "return": 161929989,
    "about": 161498117,
}
BAD_PATTERNS = [
    "assassinshoodies",
    "FREE delivery worldwide",
    "all countries around the world",
    "15-30 days",
    "don’t need to pay customs fee",
    "low value gifts",
    "30 days of purchase",
    "4-6 weeks",
    "Thousands of Happy Families",
    "thousands of families",
    "Trusted since 2016",
    "Founded in 2016",
    "30-day hassle-free",
]


def load_admin_config() -> tuple[str, str]:
    config_dir = Path.home() / ".config" / "dresslikemommy"
    env_path = config_dir / "shopify-admin.env"
    token_path = config_dir / "admin-api-token.json"
    values: dict[str, str] = {}

    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            match = re.match(r"\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)=(.*)", line)
            if not match:
                continue
            key, value = match.groups()
            values[key] = value.strip().strip('"').strip("'")

    if token_path.exists():
        token_data = json.loads(token_path.read_text(encoding="utf-8"))
        values.setdefault("SHOPIFY_STORE_DOMAIN", token_data.get("store_domain", ""))
        values.setdefault("SHOPIFY_ADMIN_ACCESS_TOKEN", token_data.get("access_token", ""))

    store = values.get("SHOPIFY_STORE_DOMAIN")
    token = values.get("SHOPIFY_ADMIN_ACCESS_TOKEN")
    if not store or not token:
        raise SystemExit("Shopify Admin credentials not loaded in this shell and no local credential file could be used.")
    return store, token


def admin_session(token: str) -> requests.Session:
    session = requests.Session()
    session.headers.update(
        {
            "X-Shopify-Access-Token": token,
            "Content-Type": "application/json",
        }
    )
    return session


def request_json(session: requests.Session, method: str, url: str, **kwargs) -> dict:
    response = session.request(method, url, timeout=30, **kwargs)
    if response.status_code == 401:
        raise SystemExit("Stored Shopify Admin token requires regeneration/reinstall: 401 Invalid API key or access token.")
    response.raise_for_status()
    return response.json()


def count_hits(body: str) -> dict[str, int]:
    lowered = body.lower()
    return {pattern: lowered.count(pattern.lower()) for pattern in BAD_PATTERNS if pattern.lower() in lowered}


def fix_faq(body: str) -> str:
    replacements = {
        'href="http://www.assassinshoodies.com/pages/sizing-information"': 'href="https://www.dresslikemommy.com/pages/size-guide"',
        'href="https://www.assassinshoodies.com/pages/sizing-information"': 'href="https://www.dresslikemommy.com/pages/size-guide"',
        'hef="www.assassinshoodies.com/pages/track-your-order"': 'href="https://www.dresslikemommy.com/pages/track-your-order"',
        'href="www.assassinshoodies.com/pages/track-your-order"': 'href="https://www.dresslikemommy.com/pages/track-your-order"',
        "mail%20to:": "mailto:",
        (
            "<p>It sure is. We use PayPal to process payments. So not even our staff get to see your payment details. "
            "PayPal is the World's biggest secure payment provider. Our website is built on the Shopify secure platform. "
            "All of your personal information is locked down tight.</p>"
        ): (
            "<p>Yes. Checkout is hosted securely by Shopify and supports the payment methods shown at checkout. "
            "We do not store your full card details on our site.</p>"
        ),
        "<p>We offer absolutely FREE delivery worldwide.</p>": (
            "<p>We offer free standard shipping on all orders to the destinations listed in our shipping policy.</p>"
        ),
        "<p>Yes, we do. We deliver to all countries around the world.</p>": (
            "<p>We currently ship to the countries listed in our shipping policy. "
            "If your country is not listed at checkout, contact us before placing an order.</p>"
        ),
        (
            '<p>The delivery usually takes about 15-30 days. However, you can check the exact delivery estimates here: '
            '<a href="https://www.dresslikemommy.com/pages/shipping-and-delivery" alt="Shipping Page">Shipping Page</a></p>'
        ): (
            '<p>Processing and transit times vary by destination and carrier. Review the '
            '<a href="https://www.dresslikemommy.com/policies/shipping-policy" alt="Shipping Policy">shipping policy</a> '
            "for the current shipping details before checkout.</p>"
        ),
        "<p>No, you don’t need to pay customs fee. We mark all our orders as low value gifts. Moreover, we send bigger orders in separate packages.</p>": (
            "<p>Customs duties, import taxes, or local fees may be charged by your destination country and are the customer's responsibility. "
            "We cannot mark orders as gifts or lower-value shipments.</p>"
        ),
        (
            '<p>Please contact us at <a href="mailto:support@dresslikemommy.com">support@dresslikemommy.com</a> and provide us with your order number. '
            "You can send us your item back and we will send you a new item with the updated size. *Postage costs will be at your expense.</p>"
        ): (
            '<p>Please contact us at <a href="mailto:support@dresslikemommy.com">support@dresslikemommy.com</a> and provide your order number. '
            "Approved exchanges follow the current refund policy, including item-condition requirements and return-shipping responsibility.</p>"
        ),
        (
            '<p>Please contact us at <a href="mailto:support@dresslikemommy.com">support@dresslikemommy.com</a> and provide us with your order number. '
            "You can send us your item back and we will issue a refund. *Postage costs will be at your expense.</p>"
        ): (
            '<p>Please contact us at <a href="mailto:support@dresslikemommy.com">support@dresslikemommy.com</a> and provide your order number. '
            "Review the refund policy for eligibility, return shipping, and refund timing before sending anything back.</p>"
        ),
    }

    updated = body
    for old, new in replacements.items():
        updated = updated.replace(old, new)
    return updated


def fix_about(body: str) -> str:
    replacements = {
        (
            "<p>Founded in 2016 by Francisco, a father of two girls in Naples, Florida, Dress Like Mommy started when he noticed how his daughters "
            "lit up every time they matched outfits with their mom. That spark of joy — the giggles, the photos, the \"we're twinning!\" moments — "
            "became the heart of a business dedicated to bringing families closer through fashion.</p>"
        ): (
            "<p>Dress Like Mommy grew from Francisco's family idea in Naples, Florida: the joy his daughters felt when they matched outfits with their mom. "
            'That spark — the giggles, the photos, and the "we\'re twinning!" moments — became the heart of a business dedicated to bringing families closer through fashion.</p>'
        ),
        (
            "<p>Since 2016, we've served thousands of families across the United States, Canada, United Kingdom, and Australia. Whether it's Christmas morning "
            "matching jammies, a family photo shoot, or just a fun day out twinning with your mini-me, our customers keep coming back for the smiles these outfits create.</p>"
        ): (
            "<p>We serve families across the United States, Canada, United Kingdom, and Australia. Whether it's Christmas morning matching pajamas, a family photo shoot, "
            "or a fun day out twinning with your mini-me, our customers come to us for coordinated outfits that make getting dressed together simpler.</p>"
        ),
        "<li>\n<strong>Thousands of Happy Families</strong> since 2016</li>": (
            "<li>\n<strong>Family Matching Made Easy</strong> — Coordinated outfits for photos, holidays, trips, and everyday moments</li>"
        ),
        "<li>\n<strong>Easy Returns</strong> — 30-day hassle-free return policy</li>": (
            "<li>\n<strong>Easy Returns</strong> — Clear return and exchange guidance in our refund policy</li>"
        ),
        "<p><em>Dress Like Mommy — Making family moments even more special since 2016.</em></p>": (
            "<p><em>Dress Like Mommy — Making family moments even more special.</em></p>"
        ),
    }

    updated = body
    for old, new in replacements.items():
        updated = updated.replace(old, new)
    return updated


def policy_body(policies: list[dict], handle: str) -> str:
    for policy in policies:
        if policy.get("handle") == handle:
            body = policy.get("body") or ""
            if body:
                return body
    raise SystemExit(f"Could not find Shopify policy body for {handle}.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true", help="Write changes to Shopify Admin pages.")
    parser.add_argument(
        "--artifact-dir",
        default="dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-28_STOREFRONT_BLOCKER_FIXES",
    )
    args = parser.parse_args()

    store, token = load_admin_config()
    session = admin_session(token)
    base_url = f"https://{store}/admin/api/{API_VERSION}"
    artifact_dir = Path(args.artifact_dir)
    artifact_dir.mkdir(parents=True, exist_ok=True)

    policies = request_json(session, "GET", f"{base_url}/policies.json").get("policies", [])
    shipping_policy = policy_body(policies, "shipping-policy")
    refund_policy = policy_body(policies, "refund-policy")

    transforms = {
        "faq": fix_faq,
        "shipping": lambda _body: shipping_policy,
        "return": lambda _body: refund_policy,
        "about": fix_about,
    }

    summary = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "mode": "execute" if args.execute else "dry-run",
        "pages": {},
    }

    for key, page_id in PAGE_IDS.items():
        page = request_json(session, "GET", f"{base_url}/pages/{page_id}.json")["page"]
        before_body = page.get("body_html") or ""
        after_body = transforms[key](before_body)
        before_hits = count_hits(before_body)
        after_hits = count_hits(after_body)

        (artifact_dir / f"{key}-before.json").write_text(json.dumps(page, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        after_page = {**page, "body_html": after_body}
        (artifact_dir / f"{key}-after.json").write_text(json.dumps(after_page, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

        changed = before_body != after_body
        if args.execute and changed:
            request_json(
                session,
                "PUT",
                f"{base_url}/pages/{page_id}.json",
                json={"page": {"id": page_id, "body_html": after_body}},
            )

        summary["pages"][key] = {
            "id": page_id,
            "handle": page.get("handle"),
            "changed": changed,
            "before_hits": before_hits,
            "after_hits": after_hits,
        }

    if args.execute:
        for key, page_id in PAGE_IDS.items():
            live_page = request_json(session, "GET", f"{base_url}/pages/{page_id}.json")["page"]
            live_body = live_page.get("body_html") or ""
            summary["pages"][key]["live_hits"] = count_hits(live_body)
            (artifact_dir / f"{key}-live.json").write_text(json.dumps(live_page, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    (artifact_dir / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
