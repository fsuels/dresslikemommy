#!/usr/bin/env python3
"""Read a private fixed-window export; emit aggregate evidence without order IDs.

No API calls or mutations. Monetary arithmetic uses Decimal. This September
reconciliation intentionally stops on ambiguous IDs, partial refunds, changed
line quantities, currency mismatches or incomplete pagination instead of
inventing an allocation. A future cohort with those conditions needs a new
explicit reconciliation method.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter, defaultdict
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from zoneinfo import ZoneInfo
from datetime import datetime

D = Decimal
CENT = D('0.01')


def money(record, field):
    value = record[field]['shopMoney']
    assert value['currencyCode'] == 'USD', 'Unexpected shop currency'
    return D(value['amount'])


def usd(value):
    return str(value.quantize(CENT, rounding=ROUND_HALF_UP))


def line_value(line):
    return money(line, 'originalTotalSet') - sum(
        (money(x, 'allocatedAmountSet') for x in line['discountAllocations']), D(0))


def valid(order):
    return not order['test'] and not order['cancelledAt'] and order['displayFinancialStatus'] == 'PAID'


def normalize_id(value):
    return str(value).strip().removeprefix('#')


def shop_date(value, timezone):
    return datetime.fromisoformat(value.replace('Z', '+00:00')).astimezone(ZoneInfo(timezone)).strftime('%Y-%m-%d')


def build(data):
    orders = data['orders']
    assert len({o['id'] for o in orders}) == len(orders), 'Duplicate Shopify ID'
    assert all(data['windows']['start90'] <= o['createdAt'] < data['windows']['endExclusive'] for o in orders)
    assert all(o['displayFinancialStatus'] in ('PAID', 'REFUNDED') for o in orders), 'Unsupported payment/refund state'
    details = {o['id']: o for o in data['details']}
    assert set(details) == {o['id'] for o in orders}, 'Order details missing'
    assert all(not d['lineItems']['pageInfo']['hasNextPage'] and not d['shippingLines']['pageInfo']['hasNextPage'] for d in details.values())
    variants = {v['id']: v for v in data['variants'] if v}
    index = defaultdict(set)
    order_map = {o['id']: o for o in orders}
    for o in orders:
        for key in (o['id'], o['id'].rsplit('/', 1)[-1], o['name']):
            index[normalize_id(key)].add(o['id'])
    ga4 = data['ga4']
    assert len({g['transaction_id'] for g in ga4}) == len(ga4), 'Duplicate GA4 ID'
    matched = []
    for g in ga4:
        keys = index[normalize_id(g['transaction_id'])]
        assert len(keys) == 1, 'Unmatched or ambiguous GA4 ID'
        o = order_map[next(iter(keys))]
        assert g['reporting_currency'] == 'USD' and D(g['ecommerce_purchases']) == 1
        date = shop_date(o['createdAt'], data['shop']['timeZone']).replace('-', '')
        assert date == g['date'].replace('-', ''), 'Purchase date mismatch'
        matched.append((g, o))
    matched_ids = {o['id'] for _, o in matched}
    windows = {}
    for name, start in [('90d', data['windows']['start90']), ('28d', data['windows']['start28'])]:
        rows = [o for o in orders if o['createdAt'] >= start]
        paid = [o for o in rows if valid(o)]
        pairs = [(g, o) for g, o in matched if o['createdAt'] >= start]
        missing = [o for o in paid if o['id'] not in matched_ids]
        ga = sum((D(g['purchase_revenue']) for g, _ in pairs), D(0))
        matched_original = sum((money(o, 'subtotalPriceSet') for _, o in pairs), D(0))
        windows[name] = {
            'shopify_all_orders': len(rows), 'paid_noncancelled_orders': len(paid),
            'cancelled_refunded_orders': sum(bool(o['cancelledAt']) for o in rows),
            'test_orders': sum(o['test'] for o in rows),
            'shopify_original_merchandise_usd': usd(sum((money(o, 'subtotalPriceSet') for o in rows), D(0))),
            'shopify_retained_merchandise_usd': usd(sum((money(o, 'currentSubtotalPriceSet') for o in rows), D(0))),
            'shopify_current_total_including_shipping_usd': usd(sum((money(o, 'currentTotalPriceSet') for o in rows), D(0))),
            'ga4_purchases': len(pairs), 'ga4_purchase_revenue_usd_full_precision': str(ga),
            'matched_retained_paid_orders': sum(valid(o) for _, o in pairs),
            'ga4_includes_cancelled_refunded_orders': sum(bool(o['cancelledAt']) for _, o in pairs),
            'missing_retained_paid_orders': len(missing),
            'missing_retained_merchandise_usd': usd(sum((money(o, 'currentSubtotalPriceSet') for o in missing), D(0))),
            'missing_country_counts': dict(Counter(o['shippingAddress']['countryCodeV2'] for o in missing)),
            'matched_shopify_original_merchandise_usd': usd(matched_original),
            'matched_ga4_minus_shopify_merchandise_usd': str(ga - matched_original),
        }
    products = {}
    for o in orders:
        if not valid(o):
            continue
        lines = details[o['id']]['lineItems']['nodes']
        assert all(l['quantity'] == l['currentQuantity'] for l in lines), 'Explicit removed/refunded line allocation required'
        assert sum((line_value(l) for l in lines), D(0)) == money(o, 'currentSubtotalPriceSet'), 'Line-to-order mismatch'
        for l in lines:
            p = l['product']
            pid = p['id'].rsplit('/', 1)[-1] if p else 'UNRESOLVED'
            row = products.setdefault(pid, {'product_id': pid, 'title': p['title'] if p else 'Unresolved product identity', 'orders': set(), 'recent_orders': set(), 'units': 0, 'revenue': D(0), 'recent_revenue': D(0), 'countries': defaultdict(Decimal), 'current_modeled_cost': D(0), 'missing_current_cost_lines': 0, 'first_sale': shop_date(o['createdAt'], data['shop']['timeZone']), 'last_sale': shop_date(o['createdAt'], data['shop']['timeZone'])})
            amount = line_value(l)
            row['orders'].add(o['id']); row['units'] += l['currentQuantity']; row['revenue'] += amount
            row['last_sale'] = shop_date(o['createdAt'], data['shop']['timeZone'])
            row['countries'][o['shippingAddress']['countryCodeV2']] += amount
            if o['createdAt'] >= data['windows']['start28']:
                row['recent_orders'].add(o['id']); row['recent_revenue'] += amount
            v = variants.get((l['variant'] or {}).get('id'))
            cost = (v or {}).get('inventoryItem', {}).get('unitCost')
            if cost:
                assert cost['currencyCode'] == 'USD'
                row['current_modeled_cost'] += D(cost['amount']) * l['currentQuantity']
            else:
                row['missing_current_cost_lines'] += 1
    assert sum((r['revenue'] for r in products.values()), D(0)) == D(windows['90d']['shopify_retained_merchandise_usd'])
    product_rows = [{'product_id': r['product_id'], 'title': r['title'], 'orders_90d': len(r['orders']), 'orders_28d': len(r['recent_orders']), 'units_90d': r['units'], 'merchandise_usd_90d': usd(r['revenue']), 'merchandise_usd_28d': usd(r['recent_revenue']), 'country_merchandise_usd': {k: usd(v) for k, v in r['countries'].items()}, 'current_modeled_unit_cost_total_usd': usd(r['current_modeled_cost']) if not r['missing_current_cost_lines'] else None, 'missing_current_cost_lines': r['missing_current_cost_lines'], 'first_sale_date': r['first_sale'], 'last_sale_date': r['last_sale']} for r in products.values()]
    product_rows.sort(key=lambda r: D(r['merchandise_usd_90d']), reverse=True)
    candidate_rows = []
    for c in data['campaign_candidates']:
        row = products.get(c['product_id'])
        exact = [(o, l) for o in orders if valid(o) for l in details[o['id']]['lineItems']['nodes'] if (l['variant'] or {}).get('id', '').rsplit('/', 1)[-1] in c['variant_ids']]
        vs = [variants.get('gid://shopify/ProductVariant/' + x) for x in c['variant_ids']]
        assert all(vs), 'Candidate variant missing'
        candidate_rows.append({'rank_in_old_packet': int(c['rank']), 'product_id': c['product_id'], 'title': c['title'], 'orders_90d': len(row['orders']) if row else 0, 'orders_28d': len(row['recent_orders']) if row else 0, 'retained_merchandise_usd_90d': usd(row['revenue']) if row else '0.00', 'retained_merchandise_usd_28d': usd(row['recent_revenue']) if row else '0.00', 'countries_90d': sorted(row['countries']) if row else [], 'exact_old_variant_count': len(c['variant_ids']), 'current_available_variants': sum(v['availableForSale'] for v in vs), 'current_product_statuses': sorted({v['product']['status'] for v in vs}), 'exact_variant_units_sold_90d': sum(l['currentQuantity'] for _, l in exact), 'exact_variant_merchandise_usd_90d': usd(sum((line_value(l) for _, l in exact), D(0))), 'exact_variant_us_units_90d': sum(l['currentQuantity'] for o, l in exact if o['shippingAddress']['countryCodeV2'] == 'US')})
    fees = defaultdict(Decimal)
    for o in orders:
        if not valid(o): continue
        for t in details[o['id']]['transactions']:
            if t['status'] != 'SUCCESS' or t['kind'] not in ('SALE', 'CAPTURE'): continue
            for f in t['fees']:
                fees[f['amount']['currencyCode']] += D(f['amount']['amount'])
                fees[f['taxAmount']['currencyCode']] += D(f['taxAmount']['amount'])
    shipping = defaultdict(lambda: {'orders': 0, 'charge': D(0)})
    for o in orders:
        if o['createdAt'] < data['windows']['start28']: continue
        for s in details[o['id']]['shippingLines']['nodes']:
            shipping[s['title']]['orders'] += 1
            shipping[s['title']]['charge'] += money(s, 'discountedPriceSet')
    half_cost = sum(v['inventoryItem']['unitCost'] is not None and D(v['inventoryItem']['unitCost']['amount']) == (D(v['price']) / 2).quantize(CENT, rounding=ROUND_HALF_UP) for v in variants.values())
    paid_pairs = [(g, o) for g, o in matched if g['session_source_medium'] == 'google / cpc']
    campaign_groups = {}
    for g, o in paid_pairs:
        key = (g['session_campaign_id'], g['session_source_medium'])
        group = campaign_groups.setdefault(key, {'orders': 0, 'ga4_revenue': D(0), 'shopify_merchandise': D(0), 'shopify_first_visit_types': Counter(), 'shopify_last_visit_types': Counter()})
        group['orders'] += 1
        group['ga4_revenue'] += D(g['purchase_revenue'])
        group['shopify_merchandise'] += money(o, 'subtotalPriceSet')
        group['shopify_first_visit_types'][(o['customerJourneySummary']['firstVisit'] or {}).get('sourceType') or 'UNKNOWN'] += 1
        group['shopify_last_visit_types'][(o['customerJourneySummary']['lastVisit'] or {}).get('sourceType') or 'UNKNOWN'] += 1
    paid_evidence = [{'ga4_session_campaign_id': key[0], 'ga4_session_source_medium': key[1], 'matched_orders': group['orders'], 'ga4_revenue_usd': str(group['ga4_revenue']), 'shopify_merchandise_usd': usd(group['shopify_merchandise']), 'shopify_first_visit_type_counts': dict(group['shopify_first_visit_types']), 'shopify_last_visit_type_counts': dict(group['shopify_last_visit_types'])} for key, group in campaign_groups.items()]
    mismatched_values = [(g, o) for g, o in matched if abs(D(g['purchase_revenue']) - money(o, 'subtotalPriceSet')) > CENT]
    return {'source_read_at_utc': data['createdAtUtc'], 'shop': data['shop'], 'windows': windows, 'join': {'unique_ga4_matches': len(matched), 'unmatched_ga4_ids': 0, 'ambiguous_matches': 0, 'date_mismatches': 0, 'value_differences_over_one_cent': len(mismatched_values), 'those_with_non_usd_presentment': sum(o['presentmentCurrencyCode'] != 'USD' for _, o in mismatched_values)}, 'cost_basis': {'current_variants_checked': len(variants), 'exact_half_price_rounded_half_up': half_cost, 'classification': 'MODELED_NOT_INVOICE_VERIFIED', 'fees_native_currency_totals': {k: usd(v) for k, v in sorted(fees.items())}, 'settled_payment_fee_access': 'PERMISSION_REQUIRED: connector lacks read_shopify_payments or read_shopify_payments_accounts', 'actual_fulfillment_costs': 'UNKNOWN_OWNER_LOCATION_REQUESTED', 'actual_net_margin': None}, 'shipping_28d': {k: {'orders': v['orders'], 'charged_usd': usd(v['charge'])} for k, v in shipping.items()}, 'google_cpc_evidence': paid_evidence, 'candidate_campaign_id': '23867953136', 'candidates': candidate_rows, 'products': product_rows, 'no_campaign_or_account_changes': True}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True, type=Path)
    parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    data = json.loads(args.input.read_text())
    result = build(data)
    result['private_input_sha256'] = hashlib.sha256(args.input.read_bytes()).hexdigest()
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / 'sales_candidate_reconciliation_summary.json').write_text(json.dumps(result, indent=2) + '\n')
    for key, filename in [('candidates', 'current_sold_campaign_candidates.csv'), ('products', 'current_product_sales_and_modeled_costs.csv')]:
        rows = [{k: json.dumps(v, sort_keys=True) if isinstance(v, (dict, list)) else v for k, v in r.items()} for r in result[key]]
        with (args.out / filename).open('w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)
    print(json.dumps({'status': 'PASS', 'ga4_matches': result['join']['unique_ga4_matches'], 'current_variants_checked': result['cost_basis']['current_variants_checked'], 'half_price_costs': result['cost_basis']['exact_half_price_rounded_half_up'], 'candidate_products': len(result['candidates']), 'product_aggregate_rows': len(result['products'])}))


if __name__ == '__main__':
    main()
