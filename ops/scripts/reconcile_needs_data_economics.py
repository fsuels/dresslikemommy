#!/usr/bin/env python3
"""Reconcile remaining economics data gaps without mutating live systems."""

from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from typing import Any, Iterable

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops.scripts.build_shopify_margin_cac_export_pack import (  # noqa: E402
    amount_value,
    q2,
    q4,
    rows_from_dicts,
    safe_div,
    sources_rows,
    write_csv,
    write_xlsx,
)
from ops.scripts.refresh_paid_label_export import API_VERSION, ShopifyClient  # noqa: E402
from ops.scripts.shopify_admin_config import load_access_token, resolve_store_domain  # noqa: E402


PAYOUTS_QUERY = """
query Payouts($first: Int!, $after: String) {
  shopifyPaymentsAccount {
    id
    activated
    country
    defaultCurrency
    payouts(first: $first, after: $after, sortKey: ISSUED_AT, reverse: true) {
      nodes {
        id
        legacyResourceId
        issuedAt
        status
        transactionType
        net { amount currencyCode }
        summary {
          chargesGross { amount currencyCode }
          chargesFee { amount currencyCode }
          refundsFeeGross { amount currencyCode }
          refundsFee { amount currencyCode }
          adjustmentsGross { amount currencyCode }
          adjustmentsFee { amount currencyCode }
          reservedFundsGross { amount currencyCode }
          reservedFundsFee { amount currencyCode }
          retriedPayoutsGross { amount currencyCode }
          retriedPayoutsFee { amount currencyCode }
          advanceGross { amount currencyCode }
          advanceFees { amount currencyCode }
          usdcRebateCreditAmount { amount currencyCode }
        }
      }
      pageInfo { hasNextPage endCursor }
    }
  }
}
"""


BALANCE_TRANSACTIONS_QUERY = """
query BalanceTransactions($first: Int!, $after: String) {
  shopifyPaymentsAccount {
    balanceTransactions(
      first: $first,
      after: $after,
      sortKey: PROCESSED_AT,
      reverse: true
    ) {
      nodes {
        id
        transactionDate
        type
        sourceType
        sourceId
        sourceOrderTransactionId
        test
        amount { amount currencyCode }
        fee { amount currencyCode }
        net { amount currencyCode }
        adjustmentReason
        associatedOrder { id name }
        associatedPayout { id status }
      }
      pageInfo { hasNextPage endCursor }
    }
  }
}
"""


DISPUTES_QUERY = """
query Disputes($first: Int!, $after: String, $query: String!) {
  shopifyPaymentsAccount {
    disputes(first: $first, after: $after, reverse: true, query: $query) {
      nodes {
        id
        legacyResourceId
        initiatedAt
        status
        type
        amount { amount currencyCode }
        evidenceDueBy
        finalizedOn
        order { id legacyResourceId }
        reasonDetails { reason networkReasonCode }
      }
      pageInfo { hasNextPage endCursor }
    }
  }
}
"""


def parse_dt(value: str) -> datetime:
    text = value.replace("Z", "+00:00")
    return datetime.fromisoformat(text)


def as_utc(value: str) -> datetime:
    dt = parse_dt(value)
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def in_window(value: str, start_utc: datetime, end_utc: datetime) -> bool:
    if not value:
        return False
    dt = as_utc(value)
    return start_utc <= dt < end_utc


def money_amount(node: Any) -> Decimal:
    return amount_value(node or {})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def page_shopify_connection(
    client: ShopifyClient,
    query: str,
    variables: dict[str, Any] | None,
    extractor: list[str],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    after: str | None = None
    while True:
        call_vars = dict(variables or {})
        call_vars.update({"first": 100, "after": after})
        data = client.graphql(query, call_vars)
        connection: Any = data
        for part in extractor:
            connection = connection[part]
        rows.extend(connection.get("nodes") or [])
        page = connection.get("pageInfo") or {}
        if not page.get("hasNextPage"):
            break
        after = page.get("endCursor")
    return rows


def fetch_payouts(client: ShopifyClient, start_utc: datetime, end_utc: datetime) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    account: dict[str, Any] = {}
    after: str | None = None
    while True:
        data = client.graphql(PAYOUTS_QUERY, {"first": 100, "after": after})
        account = data.get("shopifyPaymentsAccount") or {}
        connection = account.get("payouts") or {}
        nodes = connection.get("nodes") or []
        for node in nodes:
            issued_at = node.get("issuedAt") or ""
            if in_window(issued_at, start_utc, end_utc):
                rows.append(node)
        if nodes:
            oldest = as_utc(nodes[-1].get("issuedAt") or "1970-01-01T00:00:00Z")
            if oldest < start_utc:
                break
        page = connection.get("pageInfo") or {}
        if not page.get("hasNextPage"):
            break
        after = page.get("endCursor")
    return account, rows


def fetch_balance_transactions(
    client: ShopifyClient, start_utc: datetime, end_utc: datetime
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    after: str | None = None
    while True:
        data = client.graphql(BALANCE_TRANSACTIONS_QUERY, {"first": 100, "after": after})
        connection = (data.get("shopifyPaymentsAccount") or {}).get("balanceTransactions") or {}
        nodes = connection.get("nodes") or []
        for node in nodes:
            tx_at = node.get("transactionDate") or ""
            if in_window(tx_at, start_utc, end_utc):
                rows.append(node)
        if nodes:
            oldest = as_utc(nodes[-1].get("transactionDate") or "1970-01-01T00:00:00Z")
            if oldest < start_utc:
                break
        page = connection.get("pageInfo") or {}
        if not page.get("hasNextPage"):
            break
        after = page.get("endCursor")
    return rows


def fetch_disputes(client: ShopifyClient, start_utc: datetime, end_utc: datetime) -> list[dict[str, Any]]:
    query = f"initiated_at:>={start_utc.date().isoformat()} initiated_at:<{end_utc.date().isoformat()}"
    try:
        rows = page_shopify_connection(
            client,
            DISPUTES_QUERY,
            {"query": query},
            ["shopifyPaymentsAccount", "disputes"],
        )
    except RuntimeError:
        return []
    return [row for row in rows if in_window(row.get("initiatedAt") or "", start_utc, end_utc)]


def flatten_payout(node: dict[str, Any]) -> dict[str, str]:
    summary = node.get("summary") or {}
    return {
        "payout_id": node.get("legacyResourceId") or node.get("id") or "",
        "issued_at": node.get("issuedAt") or "",
        "status": node.get("status") or "",
        "transaction_type": node.get("transactionType") or "",
        "net": q2(money_amount(node.get("net"))),
        "charges_gross": q2(money_amount(summary.get("chargesGross"))),
        "charges_fee": q2(money_amount(summary.get("chargesFee"))),
        "refunds_gross": q2(money_amount(summary.get("refundsFeeGross"))),
        "refunds_fee": q2(money_amount(summary.get("refundsFee"))),
        "adjustments_gross": q2(money_amount(summary.get("adjustmentsGross"))),
        "adjustments_fee": q2(money_amount(summary.get("adjustmentsFee"))),
        "reserved_funds_gross": q2(money_amount(summary.get("reservedFundsGross"))),
        "reserved_funds_fee": q2(money_amount(summary.get("reservedFundsFee"))),
        "retried_payouts_gross": q2(money_amount(summary.get("retriedPayoutsGross"))),
        "retried_payouts_fee": q2(money_amount(summary.get("retriedPayoutsFee"))),
        "advance_gross": q2(money_amount(summary.get("advanceGross"))),
        "advance_fees": q2(money_amount(summary.get("advanceFees"))),
        "usdc_rebate_credit_amount": q2(money_amount(summary.get("usdcRebateCreditAmount"))),
    }


def flatten_balance_transaction(node: dict[str, Any]) -> dict[str, str]:
    order = node.get("associatedOrder") or {}
    payout = node.get("associatedPayout") or {}
    return {
        "balance_transaction_id": node.get("id") or "",
        "transaction_date": node.get("transactionDate") or "",
        "type": node.get("type") or "",
        "source_type": node.get("sourceType") or "",
        "source_id": node.get("sourceId") or "",
        "source_order_transaction_id": node.get("sourceOrderTransactionId") or "",
        "test": "TRUE" if node.get("test") else "FALSE",
        "amount": q2(money_amount(node.get("amount"))),
        "fee": q2(money_amount(node.get("fee"))),
        "net": q2(money_amount(node.get("net"))),
        "adjustment_reason": node.get("adjustmentReason") or "",
        "associated_order_gid": order.get("id") or "",
        "associated_order_name": order.get("name") or "",
        "associated_payout_gid": payout.get("id") or "",
        "associated_payout_status": payout.get("status") or "",
    }


def flatten_dispute(node: dict[str, Any]) -> dict[str, str]:
    reason = node.get("reasonDetails") or {}
    order = node.get("order") or {}
    return {
        "dispute_id": node.get("legacyResourceId") or node.get("id") or "",
        "initiated_at": node.get("initiatedAt") or "",
        "status": node.get("status") or "",
        "type": node.get("type") or "",
        "amount": q2(money_amount(node.get("amount"))),
        "evidence_due_by": node.get("evidenceDueBy") or "",
        "finalized_on": node.get("finalizedOn") or "",
        "order_id": order.get("legacyResourceId") or "",
        "reason": reason.get("reason") or "",
        "network_reason_code": reason.get("networkReasonCode") or "",
    }


def build_shipping_rows(order_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in order_rows:
        if row.get("included_in_model") != "TRUE":
            continue
        rows.append(
            {
                "order_id": row.get("order_id", ""),
                "processed_at": row.get("processed_at", ""),
                "fulfillment_status": row.get("fulfillment_status", ""),
                "source_name": row.get("source_name", ""),
                "shipping_charged": row.get("shipping_charged", "0.00"),
                "refund_shipping": row.get("refund_shipping", "0.00"),
                "actual_label_or_carrier_cost": "",
                "actual_cost_status": "NEEDS_SHIPPING_LABEL_REPORT_OR_CARRIER_INVOICE",
                "notes": "Shopify Admin GraphQL exposes shipping charged/refunded here, not actual label/carrier cost.",
            }
        )
    return rows


def copy_if_exists(src: Path, dest_dir: Path) -> str:
    if not src.exists():
        return ""
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / src.name
    shutil.copy2(src, dest)
    return str(dest)


def parse_money_text(text: str, label: str) -> Decimal | None:
    match = re.search(rf"{re.escape(label)}[^\\n$]*\\$([0-9,]+(?:\\.\\d+)?)", text, re.I)
    if not match:
        return None
    return Decimal(match.group(1).replace(",", ""))


def build_ad_spend_rows(raw_root: Path, packet_dir: Path) -> list[dict[str, str]]:
    evidence_dir = packet_dir / "imported_ad_analytics_evidence"
    rows: list[dict[str, str]] = []

    pinterest_365 = raw_root / "PINTEREST/2026-04-28_authenticated_browser_capture/ads_reporting_campaigns_365d.txt"
    pinterest_ads_365 = raw_root / "PINTEREST/2026-04-28_authenticated_browser_capture/ads_reporting_ads_365d.txt"
    pinterest_text = pinterest_365.read_text(encoding="utf-8") if pinterest_365.exists() else ""
    pinterest_spend = Decimal("0") if "$0.00" in pinterest_text and "0 campaigns" in pinterest_text else None
    rows.append(
        {
            "platform": "Pinterest Ads",
            "range": "2025-04-28 to 2026-04-27",
            "status": "COLLECTED_ZERO_SPEND_365D" if pinterest_spend == Decimal("0") else "NEEDS_EXPORT",
            "spend": q2(pinterest_spend or Decimal("0")),
            "clicks": "0" if pinterest_spend == Decimal("0") else "",
            "conversions": "0" if pinterest_spend == Decimal("0") else "",
            "evidence": str(pinterest_365 if pinterest_365.exists() else ""),
            "notes": "Authenticated Pinterest browser capture showed 0 campaigns/0 ads and $0.00 spend over 365d."
            if pinterest_spend == Decimal("0")
            else "Pinterest 365d reporting evidence not found.",
        }
    )
    if pinterest_ads_365.exists():
        copy_if_exists(pinterest_ads_365, evidence_dir)
    if pinterest_365.exists():
        copy_if_exists(pinterest_365, evidence_dir)

    downloads = Path.home() / "Downloads"
    google_packet = downloads / "2026-04-28_GOOGLE_ADS_PACKET_v1.md"
    google_desc = downloads / "2026-04-28_GOOGLE_ADS_EXPORT_DESCRIPTION.md"
    google_text = google_packet.read_text(encoding="utf-8") if google_packet.exists() else ""
    google_visible_zero = "Mar 1–28, 2026" in google_text and "$0.00" in google_text
    rows.append(
        {
            "platform": "Google Ads",
            "range": "Visible page only: 2026-03-01 to 2026-03-28",
            "status": "PARTIAL_VISIBLE_ZERO_SPEND" if google_visible_zero else "NEEDS_EXPORT",
            "spend": "0.00" if google_visible_zero else "",
            "clicks": "0" if google_visible_zero else "",
            "conversions": "0 visible / tracking not recording" if google_visible_zero else "",
            "evidence": str(google_packet if google_packet.exists() else ""),
            "notes": "Imported Downloads packet. It does not satisfy full 30/90/365 export; conversion tracking shows 0 recording conversions."
            if google_visible_zero
            else "No usable local Google Ads packet found.",
        }
    )
    copy_if_exists(google_packet, evidence_dir)
    copy_if_exists(google_desc, evidence_dir)
    copy_if_exists(downloads / "2026-04-28_GOOGLE_ADS_SCREENSHOTS.zip", evidence_dir)

    ga4_packet = downloads / "2026-04-28_GA4_PACKET_v1.md"
    ga4_desc = downloads / "2026-04-28_GA4_EXPORT_DESCRIPTION.md"
    ga4_text = ga4_packet.read_text(encoding="utf-8") if ga4_packet.exists() else ""
    rows.append(
        {
            "platform": "GA4",
            "range": "Visible Home cards: 2026-04-20 to 2026-04-26; partial 90d page views",
            "status": "PARTIAL_ANALYTICS_IMPORTED" if ga4_text else "NEEDS_EXPORT",
            "spend": "",
            "clicks": "",
            "conversions": "4 purchases visible in GA4 Home" if "Purchases | 4" in ga4_text else "",
            "evidence": str(ga4_packet if ga4_packet.exists() else ""),
            "notes": "GA4 packet helps source/device gap only partially; it is not an ad-spend source and lacks ecommerce source/device exports.",
        }
    )
    copy_if_exists(ga4_packet, evidence_dir)
    copy_if_exists(ga4_desc, evidence_dir)
    copy_if_exists(downloads / "2026-04-28_GA4_SCREENSHOTS.zip", evidence_dir)

    rows.append(
        {
            "platform": "Meta Ads",
            "range": "365d requested",
            "status": "NEEDS_EXPORT",
            "spend": "",
            "clicks": "",
            "conversions": "",
            "evidence": "",
            "notes": "No Meta Ads export, local packet, or credential source found in this workspace during this pass.",
        }
    )
    return rows


def summarize_payouts(rows: list[dict[str, str]]) -> dict[str, Any]:
    totals: dict[str, Decimal] = defaultdict(Decimal)
    status_counts = Counter()
    type_counts = Counter()
    for row in rows:
        status_counts[row["status"]] += 1
        type_counts[row["transaction_type"]] += 1
        for field in [
            "net",
            "charges_gross",
            "charges_fee",
            "refunds_gross",
            "refunds_fee",
            "adjustments_gross",
            "adjustments_fee",
            "reserved_funds_gross",
            "reserved_funds_fee",
            "retried_payouts_gross",
            "retried_payouts_fee",
            "advance_gross",
            "advance_fees",
            "usdc_rebate_credit_amount",
        ]:
            totals[field] += Decimal(row[field] or "0")
    return {
        "rows": len(rows),
        "status_counts": dict(status_counts),
        "transaction_type_counts": dict(type_counts),
        "totals": {key: q2(value) for key, value in sorted(totals.items())},
    }


def summarize_balance(rows: list[dict[str, str]]) -> dict[str, Any]:
    totals: dict[str, Decimal] = defaultdict(Decimal)
    type_counts = Counter()
    for row in rows:
        type_counts[row["type"]] += 1
        for field in ["amount", "fee", "net"]:
            totals[field] += Decimal(row[field] or "0")
    return {
        "rows": len(rows),
        "type_counts": dict(type_counts),
        "totals": {key: q2(value) for key, value in sorted(totals.items())},
    }


def build_gap_rows(
    shipping_rows: list[dict[str, str]],
    payout_summary: dict[str, Any],
    balance_summary: dict[str, Any],
    dispute_rows: list[dict[str, str]],
    ad_rows: list[dict[str, str]],
    order_rows: list[dict[str, str]],
    order_line_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    shipping_charged = sum(Decimal(row["shipping_charged"] or "0") for row in shipping_rows)
    refund_shipping = sum(Decimal(row["refund_shipping"] or "0") for row in shipping_rows)
    order_model_fees = sum(
        Decimal(row.get("observed_payment_fee_allocated") or "0")
        for row in order_line_rows
        if row.get("included_in_model") == "TRUE"
    )
    pinterest = next((row for row in ad_rows if row["platform"] == "Pinterest Ads"), {})
    google = next((row for row in ad_rows if row["platform"] == "Google Ads"), {})
    ga4 = next((row for row in ad_rows if row["platform"] == "GA4"), {})
    meta = next((row for row in ad_rows if row["platform"] == "Meta Ads"), {})
    balance_fee_total = Decimal((balance_summary.get("totals") or {}).get("fee") or "0")
    balance_type_counts = balance_summary.get("type_counts") or {}
    shipping_label_tx_count = sum(
        count for tx_type, count in balance_type_counts.items() if "SHIPPING" in tx_type
    )
    gateway_counts = Counter(
        row.get("payment_gateways", "")
        for row in order_rows
        if row.get("included_in_model") == "TRUE"
    )
    return [
        {
            "gap": "Finance reports",
            "new_status": "RECONCILED_PARTIAL",
            "evidence": "Admin order totals + Shopify Payments balance/payout API",
            "value": f"Order-model payment fees {q2(order_model_fees)}; balance transaction fees {q2(balance_fee_total)}",
            "remaining_blocker": "Official Shopify Finance report export still needed for exact report parity.",
        },
        {
            "gap": "Shipping label/carrier cost",
            "new_status": "NEEDS_CARRIER_EXPORT",
            "evidence": "Order shipping charged/refunded collected from Admin export",
            "value": f"Shipping charged {q2(shipping_charged)}; shipping refunded {q2(refund_shipping)}; ShopifyPayments shipping-label balance tx count {shipping_label_tx_count}",
            "remaining_blocker": "Actual label/carrier cost is not in Admin GraphQL order export; no ShopifyPayments shipping-label transactions were observed, so use carrier/dropship invoices if shipping is external.",
        },
        {
            "gap": "Payout/payment fees/adjustments",
            "new_status": "COLLECTED_SHOPIFY_PAYMENTS_API",
            "evidence": "ShopifyPayments payouts, balance transactions, disputes",
            "value": f"Payout rows {payout_summary['rows']}; balance rows {balance_summary['rows']}; dispute rows {len(dispute_rows)}",
            "remaining_blocker": ""
            if set(gateway_counts) == {"shopify_payments"}
            else "External gateway/provider exports still required for non-Shopify payment gateways.",
        },
        {
            "gap": "Pinterest ad spend",
            "new_status": pinterest.get("status", "NEEDS_EXPORT"),
            "evidence": pinterest.get("evidence", ""),
            "value": f"Spend {pinterest.get('spend', '')}",
            "remaining_blocker": "" if pinterest.get("status") == "COLLECTED_ZERO_SPEND_365D" else "Export Pinterest Ads report.",
        },
        {
            "gap": "Google Ads ad spend",
            "new_status": google.get("status", "NEEDS_EXPORT"),
            "evidence": google.get("evidence", ""),
            "value": f"Spend {google.get('spend', '')}",
            "remaining_blocker": "Full 30/90/365 campaign/search-term/location/device exports still required.",
        },
        {
            "gap": "Meta Ads ad spend",
            "new_status": meta.get("status", "NEEDS_EXPORT"),
            "evidence": meta.get("evidence", ""),
            "value": "",
            "remaining_blocker": "No local Meta Ads export or credential source found.",
        },
        {
            "gap": "Analytics source/device",
            "new_status": ga4.get("status", "NEEDS_EXPORT"),
            "evidence": ga4.get("evidence", ""),
            "value": ga4.get("conversions", ""),
            "remaining_blocker": "GA4 detailed ecommerce by source/campaign/country/device/landing page/item still required.",
        },
    ]


def command_center_rows(summary: dict[str, Any]) -> list[list[str]]:
    return [
        ["Dress Like Mommy NEEDS_DATA Reconciliation", ""],
        ["Generated", summary["generated_at_local"]],
        ["Base packet", summary["base_packet"]],
        ["Read/write status", summary["write_status"]],
        ["Payout rows", str(summary["payout_summary"]["rows"])],
        ["Balance transaction rows", str(summary["balance_transaction_summary"]["rows"])],
        ["Dispute rows", str(summary["dispute_rows"])],
        ["Shipping charged collected", summary["shipping_charged_total"]],
        ["Actual shipping cost status", "NEEDS_SHIPPING_LABEL_REPORT_OR_CARRIER_INVOICE"],
        ["Pinterest spend status", summary["ad_spend_status"].get("Pinterest Ads", "")],
        ["Google Ads spend status", summary["ad_spend_status"].get("Google Ads", "")],
        ["GA4 analytics status", summary["ad_spend_status"].get("GA4", "")],
        ["Meta Ads status", summary["ad_spend_status"].get("Meta Ads", "")],
        ["Decision", "Do not change ads, discounts, bundles, or scale until remaining blockers are resolved."],
    ]


def build_reconciliation(
    base_packet: Path,
    output_root: Path,
    stamp: str,
    store_domain: str,
    access_token: str,
) -> Path:
    base_summary = json.loads((base_packet / "summary.json").read_text(encoding="utf-8"))
    start_utc = as_utc(base_summary["date_range"]["start_inclusive"])
    end_utc = as_utc(base_summary["date_range"]["end_exclusive"])
    generated = datetime.now().astimezone()
    packet_dir = output_root / "02_AUDIT_PACKETS" / stamp
    raw_root = output_root / "01_EXPORTS_RAW"
    packet_dir.mkdir(parents=True, exist_ok=True)

    client = ShopifyClient(store_domain, access_token, API_VERSION)
    account, raw_payouts = fetch_payouts(client, start_utc, end_utc)
    raw_balance = fetch_balance_transactions(client, start_utc, end_utc)
    raw_disputes = fetch_disputes(client, start_utc, end_utc)

    payouts = [flatten_payout(row) for row in raw_payouts]
    balance_rows = [flatten_balance_transaction(row) for row in raw_balance]
    dispute_rows = [flatten_dispute(row) for row in raw_disputes]
    order_rows = read_csv(base_packet / "orders_readonly_sanitized.csv")
    order_line_rows = read_csv(base_packet / "order_line_items_margin_model.csv")
    shipping_rows = build_shipping_rows(order_rows)
    ad_rows = build_ad_spend_rows(raw_root, packet_dir)
    payout_summary = summarize_payouts(payouts)
    balance_summary = summarize_balance(balance_rows)
    gap_rows = build_gap_rows(
        shipping_rows,
        payout_summary,
        balance_summary,
        dispute_rows,
        ad_rows,
        order_rows,
        order_line_rows,
    )

    shipping_charged = sum(Decimal(row["shipping_charged"] or "0") for row in shipping_rows)
    summary = {
        "generated_at_local": generated.isoformat(timespec="seconds"),
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "store_domain": store_domain,
        "api_version": API_VERSION,
        "base_packet": str(base_packet),
        "date_range": base_summary["date_range"],
        "write_status": "READ_ONLY_NO_SHOPIFY_FEED_AD_PRODUCT_DISCOUNT_CHANGES",
        "shopify_payments_account": {
            "id": account.get("id", ""),
            "activated": account.get("activated"),
            "country": account.get("country", ""),
            "default_currency": account.get("defaultCurrency", ""),
        },
        "payout_summary": payout_summary,
        "balance_transaction_summary": balance_summary,
        "dispute_rows": len(dispute_rows),
        "shipping_rows": len(shipping_rows),
        "shipping_charged_total": q2(shipping_charged),
        "ad_spend_status": {row["platform"]: row["status"] for row in ad_rows},
        "remaining_hard_blockers": [
            "Actual shipping label/carrier costs",
            "Full Google Ads 30/90/365 exports",
            "Detailed GA4 ecommerce source/device exports",
            "Meta Ads export if Meta is used",
            "Official Shopify Finance report parity export",
        ],
    }

    raw_api = {
        "summary": summary,
        "raw_payouts": raw_payouts,
        "raw_balance_transactions": raw_balance,
        "raw_disputes": raw_disputes,
    }
    (packet_dir / "shopify_payments_api_raw.json").write_text(
        json.dumps(raw_api, indent=2) + "\n", encoding="utf-8"
    )
    write_csv(packet_dir / "shopify_payments_payouts.csv", payouts)
    write_csv(packet_dir / "shopify_payments_balance_transactions.csv", balance_rows)
    write_csv(packet_dir / "shopify_payments_disputes.csv", dispute_rows)
    write_csv(packet_dir / "shipping_cost_reconciliation.csv", shipping_rows)
    write_csv(packet_dir / "ad_spend_analytics_reconciliation.csv", ad_rows)
    write_csv(packet_dir / "needs_data_gap_reconciliation.csv", gap_rows)
    (packet_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    readme = [
        "# NEEDS_DATA Economics Reconciliation",
        "",
        "Read-only reconciliation pass. No Shopify, feed, product, discount, ad, billing, or campaign changes were made.",
        "",
        "## What improved",
        "",
        "- Shopify Payments payouts, balance transactions, and disputes were collected through Admin GraphQL.",
        "- Order shipping charged/refunded was reconciled into a shipping-cost worklist.",
        "- Existing Pinterest, Google Ads, and GA4 local packets were imported into one ad/analytics evidence table.",
        "",
        "## What remains blocked",
        "",
        "- Actual shipping label/carrier costs still require Shopify Shipping reports or carrier invoices.",
        "- Google Ads still needs full 30/90/365 campaign, search term, location, and device exports.",
        "- GA4 still needs detailed ecommerce source/campaign/country/device/landing page/item exports.",
        "- Meta Ads still needs export if it is in use.",
        "- Official Shopify Finance reports should still be exported for report parity.",
        "",
    ]
    (packet_dir / "README.md").write_text("\n".join(readme), encoding="utf-8")

    write_xlsx(
        packet_dir / "dress_like_mommy_needs_data_reconciliation.xlsx",
        [
            ("Command_Center", command_center_rows(summary)),
            ("Gap_Reconciliation", rows_from_dicts(gap_rows)),
            ("Payments_Payouts", rows_from_dicts(payouts)),
            ("Balance_Txns", rows_from_dicts(balance_rows)),
            ("Shipping_Costs", rows_from_dicts(shipping_rows)),
            ("Ad_Analytics", rows_from_dicts(ad_rows)),
            ("Disputes", rows_from_dicts(dispute_rows)),
            ("Sources", sources_rows()),
        ],
    )
    return packet_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Read-only reconciliation of remaining economics gaps.")
    parser.add_argument(
        "--base-packet",
        type=Path,
        default=Path(
            "dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-29-shopify-margin-cac-export-pack"
        ),
    )
    parser.add_argument("--output-root", type=Path, default=Path("dresslikemommy-growth-2026"))
    parser.add_argument("--stamp", default="2026-04-29-needs-data-economics-reconciliation")
    parser.add_argument("--store-domain", default="")
    parser.add_argument("--access-token", default="")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    store_domain = resolve_store_domain(
        args.store_domain,
        fallback_domain="dresslikemommy-com.myshopify.com",
    )
    access_token = load_access_token(args.access_token)
    packet_dir = build_reconciliation(
        base_packet=args.base_packet,
        output_root=args.output_root,
        stamp=args.stamp,
        store_domain=store_domain,
        access_token=access_token,
    )
    print(f"packet_dir={packet_dir}")
    print(f"summary={packet_dir / 'summary.json'}")
    print(f"workbook={packet_dir / 'dress_like_mommy_needs_data_reconciliation.xlsx'}")


if __name__ == "__main__":
    main()
