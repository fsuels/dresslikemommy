"""Reproduce a frozen, local-only 30-day Data pilot; no network or account access.

Run with --check to validate calculations and compare existing output without writes.
The source hash binds this analysis to its original snapshot. A changed source needs
a new dated analysis, not an overwrite of this one. Currency is inherited from the
saved store report context; settlement currency and FX are not established here.
"""
import argparse
import csv
import hashlib
import io
import json
from datetime import date
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
SOURCE = 'dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-09-organic-growth/shopify_baseline.json'
SOURCE_HASH = 'ae3f01ea0689060292cf576fde8dbd48859407d8712c8790a42728064f25b4b1'
D = Decimal


def build():
    checks = []

    def check(name, ok):
        checks.append({'check': name, 'passed': bool(ok)})
        if not ok:
            raise ValueError(name)

    raw = (ROOT / SOURCE).read_bytes()
    check('Frozen source SHA256 matches', hashlib.sha256(raw).hexdigest() == SOURCE_HASH)
    source = json.loads(raw)
    window = source['date_window']
    check('Thirty complete historical dates', window == {'since': '2026-08-10', 'until': '2026-09-08', 'inclusive_days': 30}
          and (date.fromisoformat(window['until']) - date.fromisoformat(window['since'])).days + 1 == 30)
    check('Reporting timezone is America/New_York', source['reporting_timezone'] == 'America/New_York')
    tables = {}
    for name, report in source['reports'].items():
        columns = [c['name'] for c in report['columns']]
        check(name + ': unique column names', len(columns) == len(set(columns)))
        check(name + ': rows match declared rowCount', len(report['rows']) == report['rowCount'])
        check(name + ': row widths match schema', all(len(row) == len(columns) for row in report['rows']))
        tables[name] = [dict(zip(columns, row)) for row in report['rows']]
        if name != 'products_90d_top12':
            check(name + ': exact 30-day query bounds', 'SINCE 2026-08-10 UNTIL 2026-09-08' in report['query'])
    check('90-day product report excluded from 30-day analysis',
          'SINCE 2026-06-11 UNTIL 2026-09-08' in source['reports']['products_90d_top12']['query'])
    funnel = tables['funnel'][0]
    sales = tables['sales'][0]
    total = lambda rows, key: sum((D(r[key]) for r in rows), D(0))
    check('Sales arithmetic', D(sales['net_sales']) + D(sales['shipping_charges']) + D(sales['taxes']) == D(sales['total_sales']))
    check('Gross/net equality explained by zero discounts and reversals',
          D(sales['discounts']) == D(sales['sales_reversals']) == 0 and D(sales['gross_sales']) == D(sales['net_sales']))
    for key in ('orders', 'total_sales'):
        check('Order referrers reconcile ' + key, total(tables['order_referrers'], key) == D(sales[key]))
    for key in ('sessions', 'sessions_with_cart_additions', 'sessions_that_completed_checkout'):
        check('Devices reconcile ' + key, total(tables['devices'], key) == D(funnel[key]))
    stages = [D(funnel[k]) for k in ('sessions', 'sessions_with_cart_additions', 'sessions_that_reached_checkout', 'sessions_that_completed_checkout')]
    check('Funnel denominators positive and nested', stages[0] > 0 and all(a >= b >= 0 for a, b in zip(stages, stages[1:])))
    check('Raw conversion field is fraction, not already percent', abs(D(funnel['conversion_rate']) - stages[-1] / stages[0]) < D('1e-15'))
    referrers = tables['session_referrers_top15']
    countries = tables['session_countries_top12']
    residuals = {}
    for name, rows in [('session_referrers_top15', referrers), ('session_countries_top12', countries)]:
        residuals[name] = {}
        for key in ('sessions', 'sessions_that_completed_checkout'):
            remainder = D(funnel[key]) - total(rows, key)
            check(name + ': nonnegative residual for ' + key, remainder >= 0)
            residuals[name][key] = int(remainder)
    percent = lambda numerator, denominator: str((D(numerator) / D(denominator) * 100).quantize(D('0.000001'))) if D(denominator) else None
    result = {
        'schema': 'dlm.data_pilot.v1', 'evidence_label': 'REPO_KNOWN',
        'source': SOURCE, 'source_sha256': SOURCE_HASH,
        'captured_at_utc': source['captured_at_utc'], 'window': window,
        'reporting_timezone': source['reporting_timezone'],
        'currency_basis': 'USD shop-report context; not verified settlement currency',
        'reported_sales': sales, 'reported_funnel': funnel,
        'rates_percent': {
            'session_to_cart': percent(stages[1], stages[0]),
            'session_to_completed_checkout': percent(stages[3], stages[0]),
            'cart_to_reached_checkout': percent(stages[2], stages[1]),
            'reached_checkout_to_completed_checkout': percent(stages[3], stages[2]),
        },
        'devices': tables['devices'], 'session_referrers_top15': referrers,
        'session_countries_top12': countries, 'order_referrers': tables['order_referrers'],
        'top_n_residuals': residuals,
        'profit_qualification': {
            'status': 'INSUFFICIENT_MATCHED_EVIDENCE', 'actual_contribution_after_ads': None,
            'matched_ad_spend': None, 'roas': None, 'cpa': None, 'profitable_product_ranking': None,
            'reason': 'No complete order-level cost, settled-currency and acquisition join for the selected 30-day window.'},
        'excluded_from_joins': ['products_90d_top12', '28-day paid-order baseline', 'rolling two-order checkpoints', 'conditional historical cost scenarios'],
        'not_inferred': ['completed checkout is a retained paid order', 'search means organic', 'country sessions identify buyer shipping market', 'zero observed completions proves a broken device', 'publication caused sales', 'missing cost is zero'],
        'execution': {'engine': 'Codex plus standard-library Python and data skills', 'openai_data_plugin_test': 'NOT_RUN', 'live_reads': 0, 'external_writes': 0},
    }
    check('Profit, spend, ROAS and CPA remain unknown', all(result['profit_qualification'][k] is None for k in ('actual_contribution_after_ads', 'matched_ad_spend', 'roas', 'cpa', 'profitable_product_ranking')))
    validation = {'status': 'PASS', 'source_sha256': SOURCE_HASH, 'checks_passed': len(checks), 'checks_failed': 0, 'checks': checks}
    metrics = io.StringIO()
    writer = csv.writer(metrics)
    writer.writerow(['metric', 'value', 'unit', 'basis', 'since', 'until', 'evidence'])
    for k in ('orders', 'net_sales', 'shipping_charges', 'total_sales'):
        writer.writerow([k, sales[k], 'count' if k == 'orders' else 'USD', 'Shopify sales report; retained-order audit not established', window['since'], window['until'], 'REPO_KNOWN'])
    for k in ('sessions', 'sessions_with_cart_additions', 'sessions_that_reached_checkout', 'sessions_that_completed_checkout'):
        writer.writerow([k, funnel[k], 'sessions', 'Shopify session report; QA/bot exclusions unverified', window['since'], window['until'], 'REPO_KNOWN'])
    writer.writerow(['session_to_completed_checkout', result['rates_percent']['session_to_completed_checkout'], 'percent', 'completed checkout sessions / sessions * 100', window['since'], window['until'], 'REPO_KNOWN'])
    for k in ('actual_contribution_after_ads', 'matched_ad_spend', 'roas', 'cpa'):
        writer.writerow([k, '', 'UNKNOWN', result['profit_qualification']['reason'], window['since'], window['until'], 'LIVE_READBACK_REQUIRED'])
    return {'analysis.json': json.dumps(result, indent=2, ensure_ascii=False) + '\n', 'validation.json': json.dumps(validation, indent=2) + '\n', 'metrics.csv': metrics.getvalue()}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    outputs = build()
    for name, content in outputs.items():
        path = OUT / name
        if args.check:
            if not path.exists() or path.read_text() != content.replace('\r\n', '\n'):
                raise SystemExit('Saved output differs: ' + name)
        else:
            path.write_text(content)
    print(json.dumps({'status': 'PASS', 'checks': json.loads(outputs['validation.json'])['checks_passed'], 'saved_outputs': len(outputs), 'mode': 'check-only' if args.check else 'write-local-packet', 'external_calls': 0}))
