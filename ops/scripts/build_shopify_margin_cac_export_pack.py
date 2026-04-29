#!/usr/bin/env python3
"""Build a read-only Shopify margin, CAC, and ROAS export packet."""

from __future__ import annotations

import argparse
import csv
import json
import sys
import zipfile
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path
from typing import Any, Iterable
from xml.sax.saxutils import escape

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops.scripts.refresh_paid_label_export import (  # noqa: E402
    API_VERSION,
    ShopifyClient,
    fetch_active_variants,
    parse_money,
)
from ops.scripts.shopify_admin_config import (  # noqa: E402
    load_access_token,
    resolve_store_domain,
)


DEFAULT_AOV_BENCHMARK = Decimal("63.25")
DEFAULT_MARKETING_CAP_RATE = Decimal("0.15")
DEFAULT_ALL_IN_NON_MARKETING_COST_RATE = Decimal("0.50")
DEFAULT_DAYS = 365
PAGE_SIZE = 50


ORDERS_QUERY = """
query OrdersForMarginPacket($first: Int!, $after: String, $query: String!) {
  orders(first: $first, after: $after, query: $query, sortKey: PROCESSED_AT) {
    nodes {
      id
      legacyResourceId
      processedAt
      createdAt
      cancelledAt
      test
      displayFinancialStatus
      displayFulfillmentStatus
      sourceName
      currencyCode
      paymentGatewayNames
      currentTotalPriceSet { shopMoney { amount currencyCode } }
      subtotalPriceSet { shopMoney { amount currencyCode } }
      totalDiscountsSet { shopMoney { amount currencyCode } }
      totalShippingPriceSet { shopMoney { amount currencyCode } }
      totalTaxSet { shopMoney { amount currencyCode } }
      totalRefundedSet { shopMoney { amount currencyCode } }
      netPaymentSet { shopMoney { amount currencyCode } }
      customerJourneySummary {
        firstVisit {
          source
          sourceType
          utmParameters { source medium campaign content term }
        }
        lastVisit {
          source
          sourceType
          utmParameters { source medium campaign content term }
        }
      }
      transactions(first: 50) {
        id
        kind
        status
        gateway
        amountSet { shopMoney { amount currencyCode } }
        fees {
          amount { amount currencyCode }
          taxAmount { amount currencyCode }
          type
          rate
          rateName
          flatFee { amount currencyCode }
          flatFeeName
        }
      }
      lineItems(first: 100) {
        nodes {
          id
          title
          name
          quantity
          currentQuantity
          sku
          variantTitle
          vendor
          discountedTotalSet { shopMoney { amount currencyCode } }
          originalTotalSet { shopMoney { amount currencyCode } }
          totalDiscountSet { shopMoney { amount currencyCode } }
          product {
            id
            legacyResourceId
            title
            handle
            productType
            vendor
            status
            tags
          }
          variant {
            id
            legacyResourceId
            sku
            price
            product {
              id
              legacyResourceId
              title
              handle
              productType
              vendor
              status
              tags
            }
            inventoryItem {
              id
              legacyResourceId
              unitCost { amount currencyCode }
            }
          }
        }
        pageInfo { hasNextPage endCursor }
      }
      refunds(first: 50) {
        id
        legacyResourceId
        createdAt
        processedAt
        totalRefundedSet { shopMoney { amount currencyCode } }
        refundLineItems(first: 100) {
          nodes {
            id
            quantity
            subtotalSet { shopMoney { amount currencyCode } }
            totalTaxSet { shopMoney { amount currencyCode } }
            lineItem {
              id
              sku
              title
              variant {
                id
                legacyResourceId
                product { legacyResourceId handle title }
              }
            }
          }
          pageInfo { hasNextPage endCursor }
        }
        refundShippingLines(first: 20) {
          nodes {
            subtotalAmountSet { shopMoney { amount currencyCode } }
            taxAmountSet { shopMoney { amount currencyCode } }
          }
          pageInfo { hasNextPage endCursor }
        }
        transactions(first: 20) {
          nodes {
            kind
            status
            gateway
            amountSet { shopMoney { amount currencyCode } }
            fees {
              amount { amount currencyCode }
              taxAmount { amount currencyCode }
              type
            }
          }
          pageInfo { hasNextPage endCursor }
        }
      }
    }
    pageInfo { hasNextPage endCursor }
  }
}
"""


def money(node: Any) -> Decimal:
    amount = (((node or {}).get("shopMoney") or {}).get("amount"))
    if amount in (None, ""):
        return Decimal("0")
    try:
        return Decimal(str(amount))
    except (InvalidOperation, ValueError):
        return Decimal("0")


def amount_value(node: Any) -> Decimal:
    amount = (node or {}).get("amount")
    if amount in (None, ""):
        return Decimal("0")
    try:
        return Decimal(str(amount))
    except (InvalidOperation, ValueError):
        return Decimal("0")


def q2(value: Decimal) -> str:
    return str(value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def q4(value: Decimal) -> str:
    return str(value.quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP))


def safe_div(numerator: Decimal, denominator: Decimal) -> Decimal:
    if denominator == 0:
        return Decimal("0")
    return numerator / denominator


def list_join(values: Iterable[str]) -> str:
    return "|".join(sorted({value for value in values if value}))


def first_nonempty(*values: Any) -> str:
    for value in values:
        if value not in (None, ""):
            return str(value)
    return ""


def utm_value(visit: dict[str, Any] | None, key: str) -> str:
    return str(((visit or {}).get("utmParameters") or {}).get(key) or "")


def visit_value(summary: dict[str, Any] | None, which: str, key: str) -> str:
    return str(((summary or {}).get(which) or {}).get(key) or "")


def local_now() -> datetime:
    return datetime.now().astimezone()


def default_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d-shopify-margin-cac-export-pack")


def orders_query_for_range(start: datetime, end: datetime) -> str:
    return f"processed_at:>={start.isoformat()} processed_at:<{end.isoformat()}"


def fetch_orders(client: ShopifyClient, query: str) -> list[dict[str, Any]]:
    orders: list[dict[str, Any]] = []
    after: str | None = None
    while True:
        data = client.graphql(ORDERS_QUERY, {"first": PAGE_SIZE, "after": after, "query": query})
        page = data["orders"]
        orders.extend(page["nodes"])
        if not page["pageInfo"]["hasNextPage"]:
            break
        after = page["pageInfo"]["endCursor"]
    return orders


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = list(rows[0].keys()) if rows else []
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
            extrasaction="ignore",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


@dataclass
class PacketPaths:
    packet_dir: Path
    raw_orders_json: Path
    raw_variants_json: Path
    orders_csv: Path
    line_items_csv: Path
    active_variants_csv: Path
    product_model_csv: Path
    field_map_csv: Path
    export_checklist_csv: Path
    operating_rules_csv: Path
    workbook_xlsx: Path
    summary_json: Path
    readme_md: Path


def variant_unit_cost(variant: dict[str, Any]) -> Decimal | None:
    unit_cost = (((variant.get("inventoryItem") or {}).get("unitCost")) or {}).get("amount")
    return parse_money(unit_cost)


def variant_product(variant: dict[str, Any]) -> dict[str, Any]:
    return variant.get("product") or {}


def collect_active_variant_rows(variants: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    product_catalog: dict[str, dict[str, Any]] = {}
    for variant in variants:
        product = variant_product(variant)
        product_id = str(product.get("legacyResourceId") or "")
        variant_id = str(variant.get("legacyResourceId") or "")
        price = parse_money(variant.get("price")) or Decimal("0")
        unit_cost = variant_unit_cost(variant)
        inventory_quantity = int(variant.get("inventoryQuantity") or 0)
        inventory_policy = str(variant.get("inventoryPolicy") or "")
        active_sellable = inventory_quantity > 0 or inventory_policy == "CONTINUE"
        rows.append(
            {
                "product_id": product_id,
                "product_gid": product.get("id") or "",
                "handle": product.get("handle") or "",
                "product_title": product.get("title") or "",
                "product_status": product.get("status") or "",
                "product_type": product.get("productType") or "",
                "vendor": product.get("vendor") or "",
                "variant_id": variant_id,
                "variant_gid": variant.get("id") or "",
                "variant_title": variant.get("title") or "",
                "sku": variant.get("sku") or "",
                "price": q2(price),
                "unit_cost": q2(unit_cost) if unit_cost is not None else "",
                "unit_cost_present": "TRUE" if unit_cost is not None else "FALSE",
                "inventory_quantity": str(inventory_quantity),
                "inventory_policy": inventory_policy,
                "active_sellable": "TRUE" if active_sellable else "FALSE",
            }
        )

        if not product_id:
            continue
        entry = product_catalog.setdefault(
            product_id,
            {
                "product_id": product_id,
                "product_gid": product.get("id") or "",
                "handle": product.get("handle") or "",
                "product_title": product.get("title") or "",
                "product_status": product.get("status") or "",
                "product_type": product.get("productType") or "",
                "vendor": product.get("vendor") or "",
                "tags": list(product.get("tags") or []),
                "active_variant_count": 0,
                "sellable_variant_count": 0,
                "missing_unit_cost_variants": 0,
                "price_min": None,
                "price_max": None,
            },
        )
        entry["active_variant_count"] += 1
        if active_sellable:
            entry["sellable_variant_count"] += 1
        if unit_cost is None:
            entry["missing_unit_cost_variants"] += 1
        entry["price_min"] = price if entry["price_min"] is None else min(entry["price_min"], price)
        entry["price_max"] = price if entry["price_max"] is None else max(entry["price_max"], price)
    return rows, product_catalog


def transaction_fee_total(order: dict[str, Any]) -> Decimal:
    total = Decimal("0")
    for transaction in order.get("transactions") or []:
        if transaction.get("status") != "SUCCESS":
            continue
        for fee in transaction.get("fees") or []:
            total += amount_value(fee.get("amount"))
            total += amount_value(fee.get("taxAmount"))
    return total


def refund_maps(order: dict[str, Any]) -> tuple[dict[str, dict[str, Decimal]], Decimal, int]:
    by_line_item: dict[str, dict[str, Decimal]] = defaultdict(
        lambda: {"refund_qty": Decimal("0"), "refund_subtotal": Decimal("0"), "refund_tax": Decimal("0")}
    )
    refund_shipping = Decimal("0")
    clipped_connections = 0
    for refund in order.get("refunds") or []:
        refund_items = (refund.get("refundLineItems") or {})
        if (refund_items.get("pageInfo") or {}).get("hasNextPage"):
            clipped_connections += 1
        for node in refund_items.get("nodes") or []:
            line_item_id = ((node.get("lineItem") or {}).get("id")) or ""
            if not line_item_id:
                continue
            by_line_item[line_item_id]["refund_qty"] += Decimal(str(node.get("quantity") or 0))
            by_line_item[line_item_id]["refund_subtotal"] += money(node.get("subtotalSet"))
            by_line_item[line_item_id]["refund_tax"] += money(node.get("totalTaxSet"))
        shipping_lines = (refund.get("refundShippingLines") or {})
        if (shipping_lines.get("pageInfo") or {}).get("hasNextPage"):
            clipped_connections += 1
        for node in shipping_lines.get("nodes") or []:
            refund_shipping += money(node.get("subtotalAmountSet")) + money(node.get("taxAmountSet"))
    return by_line_item, refund_shipping, clipped_connections


def product_from_line_item(line_item: dict[str, Any]) -> dict[str, Any]:
    variant = line_item.get("variant") or {}
    product = variant.get("product") or line_item.get("product") or {}
    return product or {}


def variant_from_line_item(line_item: dict[str, Any]) -> dict[str, Any]:
    return line_item.get("variant") or {}


def order_visit_fields(order: dict[str, Any]) -> dict[str, str]:
    journey = order.get("customerJourneySummary") or {}
    first_visit = journey.get("firstVisit") or {}
    last_visit = journey.get("lastVisit") or {}
    return {
        "first_visit_source": str(first_visit.get("source") or ""),
        "first_visit_source_type": str(first_visit.get("sourceType") or ""),
        "first_utm_source": utm_value(first_visit, "source"),
        "first_utm_medium": utm_value(first_visit, "medium"),
        "first_utm_campaign": utm_value(first_visit, "campaign"),
        "last_visit_source": str(last_visit.get("source") or ""),
        "last_visit_source_type": str(last_visit.get("sourceType") or ""),
        "last_utm_source": utm_value(last_visit, "source"),
        "last_utm_medium": utm_value(last_visit, "medium"),
        "last_utm_campaign": utm_value(last_visit, "campaign"),
    }


def build_order_and_line_rows(
    orders: list[dict[str, Any]],
    all_in_cost_rate: Decimal,
    marketing_cap_rate: Decimal,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, dict[str, Any]], dict[str, Any]]:
    order_rows: list[dict[str, Any]] = []
    line_rows: list[dict[str, Any]] = []
    product_metrics: dict[str, dict[str, Any]] = {}
    order_product_seen: set[tuple[str, str]] = set()
    warnings = {
        "orders_with_line_items_clipped": 0,
        "refund_connections_clipped": 0,
        "orders_with_missing_variant_reference": 0,
    }

    for order in orders:
        order_id = str(order.get("legacyResourceId") or "")
        is_cancelled = bool(order.get("cancelledAt"))
        is_test = bool(order.get("test"))
        include_financials = not is_cancelled and not is_test
        current_total = money(order.get("currentTotalPriceSet"))
        subtotal = money(order.get("subtotalPriceSet"))
        discounts = money(order.get("totalDiscountsSet"))
        shipping = money(order.get("totalShippingPriceSet"))
        taxes = money(order.get("totalTaxSet"))
        refunds_total = money(order.get("totalRefundedSet"))
        net_payment = money(order.get("netPaymentSet"))
        fee_total = transaction_fee_total(order)
        refund_by_line, refund_shipping, clipped_refunds = refund_maps(order)
        warnings["refund_connections_clipped"] += clipped_refunds
        line_items = (order.get("lineItems") or {})
        line_nodes = line_items.get("nodes") or []
        if (line_items.get("pageInfo") or {}).get("hasNextPage"):
            warnings["orders_with_line_items_clipped"] += 1

        line_net_total = Decimal("0")
        for line in line_nodes:
            line_net_total += money(line.get("discountedTotalSet")) - refund_by_line[line.get("id")]["refund_subtotal"]

        visit_fields = order_visit_fields(order)
        order_rows.append(
            {
                "order_id": order_id,
                "processed_at": order.get("processedAt") or "",
                "created_at": order.get("createdAt") or "",
                "cancelled_at": order.get("cancelledAt") or "",
                "included_in_model": "TRUE" if include_financials else "FALSE",
                "test_order": "TRUE" if is_test else "FALSE",
                "financial_status": order.get("displayFinancialStatus") or "",
                "fulfillment_status": order.get("displayFulfillmentStatus") or "",
                "source_name": order.get("sourceName") or "",
                "payment_gateways": list_join(order.get("paymentGatewayNames") or []),
                "currency": order.get("currencyCode") or "",
                "current_total": q2(current_total),
                "subtotal": q2(subtotal),
                "discounts": q2(discounts),
                "shipping_charged": q2(shipping),
                "tax": q2(taxes),
                "refunds_total": q2(refunds_total),
                "refund_shipping": q2(refund_shipping),
                "net_payment": q2(net_payment),
                "observed_transaction_fees": q2(fee_total),
                **visit_fields,
            }
        )

        product_ids_in_order: set[str] = set()
        for line in line_nodes:
            product = product_from_line_item(line)
            variant = variant_from_line_item(line)
            product_id = str(product.get("legacyResourceId") or "")
            variant_id = str(variant.get("legacyResourceId") or "")
            if not variant:
                warnings["orders_with_missing_variant_reference"] += 1
            refund = refund_by_line[line.get("id")]
            gross_sales = money(line.get("originalTotalSet"))
            discount_amount = money(line.get("totalDiscountSet"))
            item_sales_before_refunds = money(line.get("discountedTotalSet"))
            refund_subtotal = refund["refund_subtotal"]
            refund_qty = refund["refund_qty"]
            net_item_sales = item_sales_before_refunds - refund_subtotal
            quantity = Decimal(str(line.get("quantity") or 0))
            current_quantity = Decimal(str(line.get("currentQuantity") or 0))
            net_quantity = quantity - refund_qty
            unit_cost = variant_unit_cost(variant) if variant else None
            unit_cost_cogs = (unit_cost or Decimal("0")) * net_quantity
            all_in_non_marketing_cost = net_item_sales * all_in_cost_rate
            fee_allocated = fee_total * safe_div(net_item_sales, line_net_total)
            shipping_allocated = shipping * safe_div(net_item_sales, line_net_total)
            max_marketing_spend = net_item_sales * marketing_cap_rate
            contribution_before_ads = net_item_sales - all_in_non_marketing_cost
            contribution_after_max_marketing = contribution_before_ads - max_marketing_spend
            target_roas_floor = safe_div(Decimal("1"), marketing_cap_rate)

            line_row = {
                "order_id": order_id,
                "processed_at": order.get("processedAt") or "",
                "included_in_model": "TRUE" if include_financials else "FALSE",
                "financial_status": order.get("displayFinancialStatus") or "",
                "fulfillment_status": order.get("displayFulfillmentStatus") or "",
                "source_name": order.get("sourceName") or "",
                "last_visit_source": visit_fields["last_visit_source"],
                "last_visit_source_type": visit_fields["last_visit_source_type"],
                "last_utm_source": visit_fields["last_utm_source"],
                "last_utm_medium": visit_fields["last_utm_medium"],
                "last_utm_campaign": visit_fields["last_utm_campaign"],
                "product_id": product_id,
                "product_gid": product.get("id") or "",
                "handle": product.get("handle") or "",
                "product_title": product.get("title") or line.get("title") or "",
                "product_type": product.get("productType") or "",
                "vendor": product.get("vendor") or line.get("vendor") or "",
                "variant_id": variant_id,
                "variant_gid": variant.get("id") or "",
                "variant_title": first_nonempty(line.get("variantTitle"), variant.get("title")),
                "sku": first_nonempty(line.get("sku"), variant.get("sku")),
                "quantity": q2(quantity),
                "current_quantity": q2(current_quantity),
                "refund_quantity": q2(refund_qty),
                "net_quantity": q2(net_quantity),
                "gross_sales": q2(gross_sales),
                "discounts": q2(discount_amount),
                "item_sales_before_refunds": q2(item_sales_before_refunds),
                "refund_subtotal": q2(refund_subtotal),
                "net_item_sales": q2(net_item_sales),
                "unit_cost_current_shopify": q2(unit_cost) if unit_cost is not None else "",
                "unit_cost_basis_cogs": q2(unit_cost_cogs),
                "operator_all_in_non_marketing_cost_50pct": q2(all_in_non_marketing_cost),
                "observed_payment_fee_allocated": q2(fee_allocated),
                "shipping_charged_allocated": q2(shipping_allocated),
                "contribution_before_ads": q2(contribution_before_ads),
                "max_marketing_spend_15pct": q2(max_marketing_spend),
                "contribution_after_max_marketing": q2(contribution_after_max_marketing),
                "target_roas_floor": q4(target_roas_floor),
            }
            line_rows.append(line_row)

            if not include_financials or not product_id:
                continue
            product_ids_in_order.add(product_id)
            metric = product_metrics.setdefault(
                product_id,
                {
                    "product_id": product_id,
                    "product_gid": product.get("id") or "",
                    "handle": product.get("handle") or "",
                    "product_title": product.get("title") or line.get("title") or "",
                    "product_status": product.get("status") or "",
                    "product_type": product.get("productType") or "",
                    "vendor": product.get("vendor") or line.get("vendor") or "",
                    "order_ids": set(),
                    "order_revenue_seen": Decimal("0"),
                    "quantity": Decimal("0"),
                    "refund_quantity": Decimal("0"),
                    "gross_sales": Decimal("0"),
                    "discounts": Decimal("0"),
                    "item_sales_before_refunds": Decimal("0"),
                    "refund_subtotal": Decimal("0"),
                    "net_item_sales": Decimal("0"),
                    "unit_cost_basis_cogs": Decimal("0"),
                    "operator_all_in_non_marketing_cost": Decimal("0"),
                    "observed_payment_fee_allocated": Decimal("0"),
                    "shipping_charged_allocated": Decimal("0"),
                    "contribution_before_ads": Decimal("0"),
                    "max_marketing_spend": Decimal("0"),
                    "contribution_after_max_marketing": Decimal("0"),
                    "source_counts": Counter(),
                    "utm_source_counts": Counter(),
                },
            )
            metric["quantity"] += quantity
            metric["refund_quantity"] += refund_qty
            metric["gross_sales"] += gross_sales
            metric["discounts"] += discount_amount
            metric["item_sales_before_refunds"] += item_sales_before_refunds
            metric["refund_subtotal"] += refund_subtotal
            metric["net_item_sales"] += net_item_sales
            metric["unit_cost_basis_cogs"] += unit_cost_cogs
            metric["operator_all_in_non_marketing_cost"] += all_in_non_marketing_cost
            metric["observed_payment_fee_allocated"] += fee_allocated
            metric["shipping_charged_allocated"] += shipping_allocated
            metric["contribution_before_ads"] += contribution_before_ads
            metric["max_marketing_spend"] += max_marketing_spend
            metric["contribution_after_max_marketing"] += contribution_after_max_marketing
            if visit_fields["last_visit_source"]:
                metric["source_counts"][visit_fields["last_visit_source"]] += 1
            if visit_fields["last_utm_source"]:
                metric["utm_source_counts"][visit_fields["last_utm_source"]] += 1

        if include_financials:
            for product_id in product_ids_in_order:
                key = (order_id, product_id)
                if key in order_product_seen:
                    continue
                order_product_seen.add(key)
                product_metrics[product_id]["order_ids"].add(order_id)
                product_metrics[product_id]["order_revenue_seen"] += current_total

    return order_rows, line_rows, product_metrics, warnings


def tier_for_product(
    *,
    sales_orders: int,
    observed_aov: Decimal,
    refund_rate: Decimal,
    contribution_after_max_marketing: Decimal,
    missing_unit_cost_variants: int,
    sellable_variant_count: int,
    aov_benchmark: Decimal,
) -> tuple[str, str]:
    if missing_unit_cost_variants:
        return "D", "NEEDS_COST_DATA"
    if sellable_variant_count == 0:
        return "D", "NO_SELLABLE_ACTIVE_VARIANTS"
    if sales_orders == 0:
        return "D", "NEEDS_ORDER_DATA"
    if contribution_after_max_marketing <= 0:
        return "D", "NEGATIVE_AFTER_MAX_MARKETING"
    if refund_rate > Decimal("0.10"):
        return "C", "REFUND_RATE_REVIEW"
    if observed_aov < Decimal("50.00"):
        return "C", "LOW_OBSERVED_AOV_BUNDLE_OR_REPRICE"
    if sales_orders < 2:
        return "B", "LOW_SAMPLE_SIZE_REVIEW_ONLY"
    if observed_aov >= aov_benchmark:
        return "A", "CANDIDATE_FOR_PAUSED_BUILDOUT_REVIEW"
    return "B", "KNOWN_COST_POSITIVE_BUT_AOV_BELOW_BENCHMARK"


def build_product_model_rows(
    product_catalog: dict[str, dict[str, Any]],
    product_metrics: dict[str, dict[str, Any]],
    aov_benchmark: Decimal,
    all_in_cost_rate: Decimal,
    marketing_cap_rate: Decimal,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    all_product_ids = sorted(set(product_catalog) | set(product_metrics))
    target_roas_floor = safe_div(Decimal("1"), marketing_cap_rate)
    for product_id in all_product_ids:
        catalog = product_catalog.get(product_id, {})
        metric = product_metrics.get(product_id, {})
        order_ids = metric.get("order_ids", set())
        sales_orders = len(order_ids)
        order_revenue_seen = metric.get("order_revenue_seen", Decimal("0"))
        observed_aov = safe_div(order_revenue_seen, Decimal(sales_orders))
        net_item_sales = metric.get("net_item_sales", Decimal("0"))
        gross_sales = metric.get("gross_sales", Decimal("0"))
        refund_subtotal = metric.get("refund_subtotal", Decimal("0"))
        refund_rate = safe_div(refund_subtotal, gross_sales)
        contribution_after = metric.get("contribution_after_max_marketing", Decimal("0"))
        missing_unit_cost_variants = int(catalog.get("missing_unit_cost_variants") or 0)
        sellable_variant_count = int(catalog.get("sellable_variant_count") or 0)
        tier, reason = tier_for_product(
            sales_orders=sales_orders,
            observed_aov=observed_aov,
            refund_rate=refund_rate,
            contribution_after_max_marketing=contribution_after,
            missing_unit_cost_variants=missing_unit_cost_variants,
            sellable_variant_count=sellable_variant_count,
            aov_benchmark=aov_benchmark,
        )
        if tier == "A":
            action = "Review for paused buildout only; do not enable spend until channel/measurement checks pass."
        elif tier == "B":
            action = "Keep in review; collect more orders or improve basket/AOV before scaling."
        elif tier == "C":
            action = "Do not advertise until AOV/refund/product economics are fixed."
        else:
            action = "Do not advertise; missing sales, cost, or sellable inventory evidence."

        rows.append(
            {
                "product_id": product_id,
                "handle": first_nonempty(catalog.get("handle"), metric.get("handle")),
                "product_title": first_nonempty(
                    catalog.get("product_title"), metric.get("product_title")
                ),
                "product_status": first_nonempty(
                    catalog.get("product_status"), metric.get("product_status")
                ),
                "product_type": first_nonempty(
                    catalog.get("product_type"), metric.get("product_type")
                ),
                "vendor": first_nonempty(catalog.get("vendor"), metric.get("vendor")),
                "active_variant_count": str(catalog.get("active_variant_count", 0)),
                "sellable_variant_count": str(sellable_variant_count),
                "missing_unit_cost_variants": str(missing_unit_cost_variants),
                "price_min": q2(catalog.get("price_min") or Decimal("0")),
                "price_max": q2(catalog.get("price_max") or Decimal("0")),
                "orders_with_product": str(sales_orders),
                "observed_order_revenue_for_product_orders": q2(order_revenue_seen),
                "observed_aov_for_orders_with_product": q2(observed_aov),
                "quantity_sold": q2(metric.get("quantity", Decimal("0"))),
                "refund_quantity": q2(metric.get("refund_quantity", Decimal("0"))),
                "gross_sales": q2(gross_sales),
                "discounts": q2(metric.get("discounts", Decimal("0"))),
                "item_sales_before_refunds": q2(metric.get("item_sales_before_refunds", Decimal("0"))),
                "refund_subtotal": q2(refund_subtotal),
                "refund_rate": q4(refund_rate),
                "net_item_sales": q2(net_item_sales),
                "unit_cost_basis_cogs_current_shopify": q2(metric.get("unit_cost_basis_cogs", Decimal("0"))),
                "operator_all_in_non_marketing_cost_50pct": q2(
                    metric.get("operator_all_in_non_marketing_cost", Decimal("0"))
                ),
                "observed_payment_fee_allocated": q2(
                    metric.get("observed_payment_fee_allocated", Decimal("0"))
                ),
                "shipping_charged_allocated": q2(
                    metric.get("shipping_charged_allocated", Decimal("0"))
                ),
                "contribution_before_ads": q2(metric.get("contribution_before_ads", Decimal("0"))),
                "max_cac_per_order_at_15pct_observed_aov": q2(observed_aov * marketing_cap_rate),
                "max_marketing_spend_15pct_product_revenue": q2(
                    metric.get("max_marketing_spend", Decimal("0"))
                ),
                "target_roas_floor": q4(target_roas_floor),
                "contribution_after_max_marketing": q2(contribution_after),
                "tier": tier,
                "tier_reason": reason,
                "recommended_action": action,
                "top_last_visit_sources": ",".join(
                    f"{name}:{count}" for name, count in (metric.get("source_counts") or Counter()).most_common(5)
                ),
                "top_last_utm_sources": ",".join(
                    f"{name}:{count}" for name, count in (metric.get("utm_source_counts") or Counter()).most_common(5)
                ),
                "cost_formula_used": f"net_item_sales * {all_in_cost_rate}",
                "cac_formula_used": f"observed_aov_for_orders_with_product * {marketing_cap_rate}",
            }
        )
    return rows


def field_map_rows() -> list[dict[str, str]]:
    return [
        {
            "metric": "Orders and order line items",
            "status": "COLLECTED",
            "source": "Shopify Admin GraphQL orders query",
            "notes": "Sanitized; no customer names, emails, addresses, phone numbers, cookies, or tokens exported.",
        },
        {
            "metric": "Product catalog, active variants, Cost per item",
            "status": "COLLECTED",
            "source": "Shopify Admin GraphQL productVariants and InventoryItem.unitCost",
            "notes": "Uses current Cost per item. Current operating rule is unit_cost = variant price x 50%.",
        },
        {
            "metric": "Refund financial impact by line item",
            "status": "COLLECTED",
            "source": "Shopify Admin GraphQL refunds/refundLineItems",
            "notes": "Financial refunds are included; operational return status is separate.",
        },
        {
            "metric": "Payment processing fees",
            "status": "COLLECTED_PARTIAL",
            "source": "Shopify Admin GraphQL OrderTransaction.fees",
            "notes": "Captured where Shopify exposes transaction fees; third-party or payout-level adjustments still need payout reports.",
        },
        {
            "metric": "Finance reports",
            "status": "PARTIAL_NEEDS_EXPORT",
            "source": "Derived from order totals in Admin GraphQL",
            "notes": "Export official Finance reports to reconcile gross sales, discounts, returns, taxes, shipping, and payments.",
        },
        {
            "metric": "Shipping label cost by order",
            "status": "NEEDS_DATA",
            "source": "Shopify Shipping labels by order report or carrier invoices",
            "notes": "Order shipping charged is collected, but label/carrier cost is not available in this API packet.",
        },
        {
            "metric": "Payout adjustments and chargebacks",
            "status": "NEEDS_DATA",
            "source": "Shopify Payments payout export / payment provider exports",
            "notes": "Needed before final ad scale decisions.",
        },
        {
            "metric": "Channel/source/UTM",
            "status": "COLLECTED_PARTIAL",
            "source": "CustomerJourneySummary first/last visit fields",
            "notes": "Good for directional source review; Shopify Analytics/GA4 export still needed for full source/device analysis.",
        },
        {
            "metric": "Device type",
            "status": "NEEDS_DATA",
            "source": "Shopify Analytics or GA4",
            "notes": "Not exposed in the read-only Admin order export used here.",
        },
        {
            "metric": "Ad spend, campaign CAC, campaign ROAS",
            "status": "NEEDS_DATA",
            "source": "Google Ads, Pinterest Ads, Meta Ads exports",
            "notes": "No ad changes should be made from this packet alone.",
        },
    ]


def export_checklist_rows() -> list[dict[str, str]]:
    return [
        {"pack": "Orders", "status": "COLLECTED", "how": "Admin GraphQL read-only export in this packet"},
        {"pack": "Products / Cost per item", "status": "COLLECTED", "how": "Admin GraphQL active variant export in this packet"},
        {"pack": "Finance reports", "status": "NEEDS_EXPORT", "how": "Shopify Admin > Analytics > Reports > Finances"},
        {"pack": "Shipping labels", "status": "NEEDS_EXPORT", "how": "Shopify Admin > Analytics > Reports > Shipping labels by order, plus carrier invoices if labels are external"},
        {"pack": "Payout/payment fees", "status": "PARTIAL_NEEDS_EXPORT", "how": "Transaction fees captured in API; export Shopify Payments payouts for reconciliation"},
        {"pack": "Analytics source/device", "status": "PARTIAL_NEEDS_EXPORT", "how": "CustomerJourney source/UTM captured in API; export Shopify Analytics/GA4 for source/device"},
        {"pack": "Ad spend by product/campaign", "status": "NEEDS_EXPORT", "how": "Google Ads, Pinterest Ads, Meta Ads exports before CAC decisions"},
    ]


def operating_rules_rows() -> list[dict[str, str]]:
    return [
        {
            "rule": "No ad scale from Shopify Home",
            "decision": "Do not increase spend, enable campaigns, or scale products until product-level economics and channel data pass.",
        },
        {
            "rule": "Cost basis",
            "decision": "Use current operator rule: all-in non-marketing cost = 50% of net item sales unless better audited cost is available.",
        },
        {
            "rule": "Marketing cap",
            "decision": "Max CAC is 15% of observed AOV; default target ROAS floor is 6.67.",
        },
        {
            "rule": "Tier A",
            "decision": "Review for paused campaign buildout only; still verify channel feed, tracking, shipping, returns, and policy evidence first.",
        },
        {
            "rule": "Tier B",
            "decision": "Known-cost positive products needing more orders or better AOV before scale.",
        },
        {
            "rule": "Tier C",
            "decision": "Do not advertise until AOV/refund/product issue is fixed.",
        },
        {
            "rule": "Tier D",
            "decision": "Do not advertise; missing sales, cost, or sellable inventory evidence.",
        },
        {
            "rule": "Discounts",
            "decision": "Do not create or deepen discounts from this packet. Discounts reduce max CAC and should be modeled first.",
        },
        {
            "rule": "Bundles",
            "decision": "Use low-AOV products as bundle/reprice candidates, not standalone scale candidates.",
        },
    ]


def command_center_rows(summary: dict[str, Any]) -> list[list[Any]]:
    return [
        ["Dress Like Mommy Margin/CAC Command Center", ""],
        ["Generated", summary["generated_at_local"]],
        ["Date range", summary["date_range_display"]],
        ["Read/write status", "READ_ONLY_NO_SHOPIFY_FEED_AD_CHANGES"],
        ["Orders collected", summary["orders_collected"]],
        ["Orders included in model", summary["orders_included_in_model"]],
        ["Open/unfulfilled included orders", summary["unfulfilled_included_orders"]],
        ["Active variant rows", summary["active_variant_rows"]],
        ["Product rows in CAC model", summary["product_model_rows"]],
        ["Observed AOV", summary["observed_aov"]],
        ["Max CAC at observed AOV", summary["max_cac_observed_aov"]],
        ["Target ROAS floor", summary["target_roas_floor"]],
        ["Tier A products", summary["tier_counts"].get("A", 0)],
        ["Tier B products", summary["tier_counts"].get("B", 0)],
        ["Tier C products", summary["tier_counts"].get("C", 0)],
        ["Tier D products", summary["tier_counts"].get("D", 0)],
        ["Next action", "Export remaining NEEDS_DATA packs before changing ads, discounts, bundles, or scaling."],
    ]


def assumptions_rows(
    aov_benchmark: Decimal,
    all_in_cost_rate: Decimal,
    marketing_cap_rate: Decimal,
) -> list[list[Any]]:
    return [
        ["Assumption", "Value", "Notes"],
        ["AOV benchmark", q2(aov_benchmark), "Existing operator benchmark from growth workspace."],
        ["All-in non-marketing cost rate", q4(all_in_cost_rate), "Includes product cost, shipping, and fees per current rule."],
        ["Marketing cap rate", q4(marketing_cap_rate), "Max CAC = AOV x marketing cap."],
        ["Target ROAS floor", q4(safe_div(Decimal("1"), marketing_cap_rate)), "Revenue / max CAC."],
        ["Product contribution before ads", "net_item_sales - (net_item_sales x all-in cost rate)", "Computed per line and product."],
        ["Contribution after max marketing", "net_item_sales - 50% cost - 15% marketing", "Returns are netted through refund line items where available."],
        ["Payment fee treatment", "Evidence only in main model", "Do not double-subtract fees because current 50% all-in cost assumption already includes fees."],
    ]


def sources_rows() -> list[list[str]]:
    return [
        ["Source", "URL or local evidence"],
        ["Shopify order export docs", "https://help.shopify.com/en/manual/fulfillment/managing-orders/exporting-orders"],
        ["Shopify product export docs", "https://help.shopify.com/en/manual/products/import-export/export-products"],
        ["Shopify finance reports docs", "https://help.shopify.com/en/manual/reports-and-analytics/shopify-reports/report-types/default-reports/finances-report"],
        ["Shopify shipping label report docs", "https://help.shopify.com/en/manual/reports-and-analytics/shopify-reports/report-types/default-reports/order-reports"],
        ["Local paid economics rule", "dresslikemommy-growth-2026/04_IMPLEMENTATION_PLANS/2026-04-28-paid-spend-product-economics.md"],
        ["Local cost sync evidence", "dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-28-variant-cost-50pct-active-live_SHOPIFY_COST_SYNC_50PCT/summary.json"],
    ]


def rows_from_dicts(rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> list[list[Any]]:
    if fieldnames is None:
        fieldnames = list(rows[0].keys()) if rows else []
    return [fieldnames, *[[row.get(field, "") for field in fieldnames] for row in rows]]


def col_name(index: int) -> str:
    name = ""
    while index:
        index, remainder = divmod(index - 1, 26)
        name = chr(65 + remainder) + name
    return name


def xlsx_cell(ref: str, value: Any) -> str:
    if value is None:
        return f'<c r="{ref}"/>'
    if isinstance(value, Decimal):
        return f'<c r="{ref}"><v>{value}</v></c>'
    if isinstance(value, bool):
        return f'<c r="{ref}" t="b"><v>{1 if value else 0}</v></c>'
    if isinstance(value, (int, float)):
        return f'<c r="{ref}"><v>{value}</v></c>'
    text = str(value)
    preserve = ' xml:space="preserve"' if text != text.strip() else ""
    return f'<c r="{ref}" t="inlineStr"><is><t{preserve}>{escape(text)}</t></is></c>'


def xlsx_sheet_xml(rows: list[list[Any]]) -> str:
    body: list[str] = []
    for r_index, row in enumerate(rows, start=1):
        cells = [xlsx_cell(f"{col_name(c_index)}{r_index}", value) for c_index, value in enumerate(row, start=1)]
        body.append(f'<row r="{r_index}">{"".join(cells)}</row>')
    max_cols = max((len(row) for row in rows), default=1)
    max_rows = max(len(rows), 1)
    dimension = f"A1:{col_name(max_cols)}{max_rows}"
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        f'<dimension ref="{dimension}"/>'
        '<sheetViews><sheetView workbookViewId="0"/></sheetViews>'
        '<sheetFormatPr defaultRowHeight="15"/>'
        f'<sheetData>{"".join(body)}</sheetData>'
        '</worksheet>'
    )


def write_xlsx(path: Path, sheets: list[tuple[str, list[list[Any]]]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    content_types = [
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">',
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>',
        '<Default Extension="xml" ContentType="application/xml"/>',
        '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>',
        '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>',
        '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>',
        '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>',
    ]
    for index in range(1, len(sheets) + 1):
        content_types.append(
            f'<Override PartName="/xl/worksheets/sheet{index}.xml" '
            'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        )
    content_types.append("</Types>")

    workbook_sheets = "".join(
        f'<sheet name="{escape(name)}" sheetId="{index}" r:id="rId{index}"/>'
        for index, (name, _) in enumerate(sheets, start=1)
    )
    workbook_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        f"<sheets>{workbook_sheets}</sheets></workbook>"
    )
    rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
        '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
        '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>'
        '</Relationships>'
    )
    workbook_rels_items = []
    for index in range(1, len(sheets) + 1):
        workbook_rels_items.append(
            f'<Relationship Id="rId{index}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{index}.xml"/>'
        )
    workbook_rels_items.append(
        f'<Relationship Id="rId{len(sheets) + 1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
    )
    workbook_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        f'{"".join(workbook_rels_items)}</Relationships>'
    )
    styles_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        '<fonts count="1"><font><sz val="11"/><name val="Calibri"/></font></fonts>'
        '<fills count="1"><fill><patternFill patternType="none"/></fill></fills>'
        '<borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>'
        '<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>'
        '<cellXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/></cellXfs>'
        '<cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>'
        '</styleSheet>'
    )
    now = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    core_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
        'xmlns:dc="http://purl.org/dc/elements/1.1/" '
        'xmlns:dcterms="http://purl.org/dc/terms/" '
        'xmlns:dcmitype="http://purl.org/dc/dcmitype/" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
        '<dc:title>Dress Like Mommy Margin CAC Packet</dc:title>'
        '<dc:creator>Codex</dc:creator>'
        f'<dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created>'
        f'<dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified>'
        '</cp:coreProperties>'
    )
    app_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
        'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
        '<Application>Codex</Application></Properties>'
    )

    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", "".join(content_types))
        zf.writestr("_rels/.rels", rels)
        zf.writestr("xl/workbook.xml", workbook_xml)
        zf.writestr("xl/_rels/workbook.xml.rels", workbook_rels)
        zf.writestr("xl/styles.xml", styles_xml)
        zf.writestr("docProps/core.xml", core_xml)
        zf.writestr("docProps/app.xml", app_xml)
        for index, (_, rows) in enumerate(sheets, start=1):
            zf.writestr(f"xl/worksheets/sheet{index}.xml", xlsx_sheet_xml(rows))


def write_readme(path: Path, summary: dict[str, Any]) -> None:
    path.write_text(
        "\n".join(
            [
                "# Shopify Margin CAC Export Pack",
                "",
                "Read-only packet. No Shopify, feed, discount, ad, product, billing, or settings writes were performed.",
                "",
                "## What this contains",
                "",
                "- Sanitized Shopify Admin order export and order line-item model.",
                "- Active product/variant cost-basis export.",
                "- Product-level contribution margin, max CAC, target ROAS, and A/B/C/D tiering.",
                "- Field map and export checklist for remaining data gaps.",
                "",
                "## Current decision",
                "",
                "Do not change ads, discounts, bundles, or product scaling from Shopify Home alone. Use this packet as the first economics layer, then reconcile the remaining NEEDS_DATA exports.",
                "",
                "## Key results",
                "",
                f"- Date range: {summary['date_range_display']}",
                f"- Orders collected: {summary['orders_collected']}",
                f"- Orders included in model: {summary['orders_included_in_model']}",
                f"- Active variants: {summary['active_variant_rows']}",
                f"- Product model rows: {summary['product_model_rows']}",
                f"- Observed AOV: ${summary['observed_aov']}",
                f"- Max CAC at observed AOV: ${summary['max_cac_observed_aov']}",
                f"- Target ROAS floor: {summary['target_roas_floor']}",
                f"- Tier counts: {json.dumps(summary['tier_counts'], sort_keys=True)}",
                "",
                "## Remaining gaps",
                "",
                "- Official Shopify Finance reports still need export/reconciliation.",
                "- Shipping label costs or carrier invoices are still needed for true fulfillment-cost proof.",
                "- Shopify Payments payout adjustments, chargebacks, and external gateway fees still need export.",
                "- Analytics source/device and ad-platform spend exports are still needed before CAC decisions become executable.",
                "",
            ]
        ),
        encoding="utf-8",
    )


def build_packet(
    output_root: Path,
    stamp: str,
    store_domain: str,
    access_token: str,
    days: int,
    aov_benchmark: Decimal,
    all_in_cost_rate: Decimal,
    marketing_cap_rate: Decimal,
) -> PacketPaths:
    generated_local = local_now()
    end = generated_local
    start = end - timedelta(days=days)
    query = orders_query_for_range(start, end)
    packet_dir = output_root / "02_AUDIT_PACKETS" / stamp
    raw_dir = output_root / "01_EXPORTS_RAW" / "SHOPIFY"
    analysis_dir = output_root / "03_LOCAL_ANALYSIS"
    packet_dir.mkdir(parents=True, exist_ok=True)
    raw_dir.mkdir(parents=True, exist_ok=True)
    analysis_dir.mkdir(parents=True, exist_ok=True)

    paths = PacketPaths(
        packet_dir=packet_dir,
        raw_orders_json=raw_dir / f"{stamp}_orders_readonly_sanitized.json",
        raw_variants_json=raw_dir / f"{stamp}_active_variants_readonly_sanitized.json",
        orders_csv=packet_dir / "orders_readonly_sanitized.csv",
        line_items_csv=packet_dir / "order_line_items_margin_model.csv",
        active_variants_csv=packet_dir / "active_variants_cost_basis.csv",
        product_model_csv=packet_dir / "product_cac_model.csv",
        field_map_csv=packet_dir / "field_map.csv",
        export_checklist_csv=packet_dir / "export_checklist.csv",
        operating_rules_csv=packet_dir / "operating_rules.csv",
        workbook_xlsx=packet_dir / "dress_like_mommy_product_margin_cac_model.xlsx",
        summary_json=packet_dir / "summary.json",
        readme_md=packet_dir / "README.md",
    )

    client = ShopifyClient(store_domain, access_token, API_VERSION)
    variants = fetch_active_variants(client)
    orders = fetch_orders(client, query)

    active_variant_rows, product_catalog = collect_active_variant_rows(variants)
    order_rows, line_rows, product_metrics, warnings = build_order_and_line_rows(
        orders=orders,
        all_in_cost_rate=all_in_cost_rate,
        marketing_cap_rate=marketing_cap_rate,
    )
    product_model_rows = build_product_model_rows(
        product_catalog=product_catalog,
        product_metrics=product_metrics,
        aov_benchmark=aov_benchmark,
        all_in_cost_rate=all_in_cost_rate,
        marketing_cap_rate=marketing_cap_rate,
    )
    field_rows = field_map_rows()
    checklist_rows = export_checklist_rows()
    rules_rows = operating_rules_rows()

    included_orders = [row for row in order_rows if row["included_in_model"] == "TRUE"]
    included_total = sum(Decimal(row["current_total"]) for row in included_orders)
    observed_aov = safe_div(included_total, Decimal(len(included_orders)))
    max_cac = observed_aov * marketing_cap_rate
    target_roas = safe_div(Decimal("1"), marketing_cap_rate)
    tier_counts = Counter(row["tier"] for row in product_model_rows)
    summary = {
        "generated_at_local": generated_local.isoformat(timespec="seconds"),
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "store_domain": store_domain,
        "api_version": API_VERSION,
        "date_range": {
            "start_inclusive": start.isoformat(timespec="seconds"),
            "end_exclusive": end.isoformat(timespec="seconds"),
            "days_requested": days,
        },
        "date_range_display": f"{start.isoformat(timespec='seconds')} through {end.isoformat(timespec='seconds')}",
        "shopify_order_query": query,
        "privacy": "Sanitized order/product economics only; no customer names, emails, addresses, phone numbers, tokens, cookies, or billing credentials exported.",
        "write_status": "READ_ONLY_NO_SHOPIFY_FEED_AD_PRODUCT_DISCOUNT_CHANGES",
        "orders_collected": len(orders),
        "orders_included_in_model": len(included_orders),
        "cancelled_or_test_orders_excluded": len(order_rows) - len(included_orders),
        "unfulfilled_included_orders": sum(
            1 for row in included_orders if row["fulfillment_status"] != "FULFILLED"
        ),
        "active_variant_rows": len(active_variant_rows),
        "active_product_rows": len(product_catalog),
        "product_model_rows": len(product_model_rows),
        "observed_total_revenue": q2(included_total),
        "observed_aov": q2(observed_aov),
        "max_cac_observed_aov": q2(max_cac),
        "target_roas_floor": q4(target_roas),
        "all_in_non_marketing_cost_rate": q4(all_in_cost_rate),
        "marketing_cap_rate": q4(marketing_cap_rate),
        "aov_benchmark": q2(aov_benchmark),
        "tier_counts": dict(sorted(tier_counts.items())),
        "warnings": warnings,
        "files": {
            "raw_orders_json": str(paths.raw_orders_json),
            "raw_active_variants_json": str(paths.raw_variants_json),
            "orders_csv": str(paths.orders_csv),
            "line_items_csv": str(paths.line_items_csv),
            "active_variants_csv": str(paths.active_variants_csv),
            "product_model_csv": str(paths.product_model_csv),
            "field_map_csv": str(paths.field_map_csv),
            "export_checklist_csv": str(paths.export_checklist_csv),
            "operating_rules_csv": str(paths.operating_rules_csv),
            "workbook_xlsx": str(paths.workbook_xlsx),
            "readme_md": str(paths.readme_md),
        },
    }

    paths.raw_orders_json.write_text(
        json.dumps(
            {
                "summary": summary,
                "orders": orders,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    paths.raw_variants_json.write_text(
        json.dumps(
            {
                "summary": {
                    "generated_at_local": summary["generated_at_local"],
                    "store_domain": store_domain,
                    "api_version": API_VERSION,
                    "active_variant_rows": len(variants),
                    "privacy": "Product/variant fields only; no customer or credential data.",
                },
                "variants": variants,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    write_csv(paths.orders_csv, order_rows)
    write_csv(paths.line_items_csv, line_rows)
    write_csv(paths.active_variants_csv, active_variant_rows)
    write_csv(paths.product_model_csv, product_model_rows)
    write_csv(paths.field_map_csv, field_rows)
    write_csv(paths.export_checklist_csv, checklist_rows)
    write_csv(paths.operating_rules_csv, rules_rows)
    paths.summary_json.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    write_readme(paths.readme_md, summary)

    # Keep the workbook compact enough to open quickly while the CSV remains the full source of truth.
    product_model_preview = product_model_rows[:1000]
    line_item_preview = line_rows[:1000]
    write_xlsx(
        paths.workbook_xlsx,
        [
            ("Command_Center", command_center_rows(summary)),
            ("Assumptions", assumptions_rows(aov_benchmark, all_in_cost_rate, marketing_cap_rate)),
            ("Export_Checklist", rows_from_dicts(checklist_rows)),
            ("Product_CAC_Model", rows_from_dicts(product_model_preview)),
            ("Order_Line_Model", rows_from_dicts(line_item_preview)),
            ("Field_Map", rows_from_dicts(field_rows)),
            ("Operating_Rules", rows_from_dicts(rules_rows)),
            ("Sources", sources_rows()),
        ],
    )
    return paths


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a read-only Shopify product margin/CAC/ROAS export packet."
    )
    parser.add_argument("--output-root", type=Path, default=Path("dresslikemommy-growth-2026"))
    parser.add_argument("--stamp", default=default_stamp())
    parser.add_argument("--store-domain", default="")
    parser.add_argument("--access-token", default="")
    parser.add_argument("--days", type=int, default=DEFAULT_DAYS)
    parser.add_argument("--aov-benchmark", default=str(DEFAULT_AOV_BENCHMARK))
    parser.add_argument("--all-in-cost-rate", default=str(DEFAULT_ALL_IN_NON_MARKETING_COST_RATE))
    parser.add_argument("--marketing-cap-rate", default=str(DEFAULT_MARKETING_CAP_RATE))
    return parser.parse_args()


def decimal_arg(value: str) -> Decimal:
    parsed = parse_money(value)
    if parsed is None:
        raise argparse.ArgumentTypeError(f"Invalid decimal value: {value}")
    return parsed


def main() -> None:
    args = parse_args()
    store_domain = resolve_store_domain(
        args.store_domain,
        fallback_domain="dresslikemommy-com.myshopify.com",
    )
    access_token = load_access_token(args.access_token)
    paths = build_packet(
        output_root=args.output_root,
        stamp=args.stamp,
        store_domain=store_domain,
        access_token=access_token,
        days=args.days,
        aov_benchmark=decimal_arg(args.aov_benchmark),
        all_in_cost_rate=decimal_arg(args.all_in_cost_rate),
        marketing_cap_rate=decimal_arg(args.marketing_cap_rate),
    )
    print(f"packet_dir={paths.packet_dir}")
    print(f"summary={paths.summary_json}")
    print(f"workbook={paths.workbook_xlsx}")


if __name__ == "__main__":
    main()
