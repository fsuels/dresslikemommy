"""Read-only validation of this evidence packet; no network or output writes.

Uses the JSON Schema keywords present in acceptance.schema.json and rejects an
unsupported keyword. This is a bounded local checker, not a general Draft 2020-12
implementation. Optional --report writes only this folder's validation.json.
"""
import copy
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
SCHEMA = json.loads((HERE / 'acceptance.schema.json').read_text())
DATA = json.loads((HERE / 'acceptance.current.json').read_text())
KEYWORDS = {'$schema', '$id', '$ref', '$defs', 'title', 'type', 'properties',
            'additionalProperties', 'required', 'const', 'enum', 'allOf', 'if',
            'then', 'items', 'contains', 'minItems', 'maxItems', 'uniqueItems',
            'minimum', 'pattern', 'format', 'minLength'}


def check_schema(s):
    assert not set(s) - KEYWORDS, 'Unsupported schema keyword'
    for group in ('properties', '$defs'):
        for child in s.get(group, {}).values():
            check_schema(child)
    for key in ('if', 'then', 'items', 'contains'):
        if key in s:
            check_schema(s[key])
    for child in s.get('allOf', []):
        check_schema(child)


def validate(value, s, path='$'):
    def require(ok, reason):
        if not ok:
            raise ValueError(path + ': ' + reason)
    if '$ref' in s:
        ref = SCHEMA
        for piece in s['$ref'][2:].split('/'):
            ref = ref[piece.replace('~1', '/').replace('~0', '~')]
        validate(value, ref, path)
    types = {'object': isinstance(value, dict), 'array': isinstance(value, list),
             'string': isinstance(value, str), 'boolean': type(value) is bool,
             'integer': type(value) is int, 'number': type(value) in (int, float),
             'null': value is None}
    if 'type' in s:
        wanted = s['type'] if isinstance(s['type'], list) else [s['type']]
        require(any(types[t] for t in wanted), 'type')
    if 'const' in s:
        require(value == s['const'] and (type(s['const']) is not bool or type(value) is bool), 'const')
    if 'enum' in s:
        require(value in s['enum'], 'enum')
    if isinstance(value, dict):
        require(set(s.get('required', [])) <= set(value), 'required fields')
        props = s.get('properties', {})
        if s.get('additionalProperties') is False:
            require(set(value) <= set(props), 'unexpected fields')
        for key, child in props.items():
            if key in value:
                validate(value[key], child, path + '.' + key)
    if isinstance(value, list):
        require(len(value) >= s.get('minItems', 0), 'minItems')
        require(len(value) <= s.get('maxItems', len(value)), 'maxItems')
        if s.get('uniqueItems'):
            require(len(value) == len({json.dumps(x, sort_keys=True) for x in value}), 'uniqueItems')
        if 'items' in s:
            for i, item in enumerate(value):
                validate(item, s['items'], f'{path}[{i}]')
        if 'contains' in s:
            matched = False
            for item in value:
                try:
                    validate(item, s['contains'], path)
                    matched = True
                except ValueError:
                    pass
            require(matched, 'contains')
    if isinstance(value, str):
        require(len(value) >= s.get('minLength', 0), 'minLength')
        if 'pattern' in s:
            require(re.search(s['pattern'], value) is not None, 'pattern')
        if s.get('format') == 'date-time':
            require(datetime.fromisoformat(value.replace('Z', '+00:00')).tzinfo is not None, 'date-time timezone')
    if type(value) in (int, float) and 'minimum' in s:
        require(value >= s['minimum'], 'minimum')
    for child in s.get('allOf', []):
        validate(value, child, path)
    if 'if' in s:
        try:
            validate(value, s['if'], path)
            applies = True
        except ValueError:
            applies = False
        if applies and 'then' in s:
            validate(value, s['then'], path)


check_schema(SCHEMA)
validate(DATA, SCHEMA)
checks = []


def check(name, condition):
    assert condition, name
    checks.append(name)


for src in DATA['source_evidence']:
    check('source_hash_' + src['id'], hashlib.sha256((REPO / src['path']).read_bytes()).hexdigest() == src['sha256'])
hist = [r for r in DATA['worked_existing_data'] if r['alias'].startswith('COST_')]
check('six_unique_historical_rows', len(hist) == len({r['alias'] for r in hist}) == 6)
for field, expected in [('provider_charge', '1551.13'), ('recorded_fee', '23.86'), ('recorded_payout_net', '571.68')]:
    check('historical_' + field, sum(Decimal(r[field]['amount']) for r in hist) == Decimal(expected))
recent = {r['alias']: r for r in DATA['worked_existing_data'] if r['alias'].startswith('RECENT_')}
check('recent_fee_currencies_separate', recent['RECENT_01']['recorded_fee']['currency'] == 'EUR' and recent['RECENT_02']['recorded_fee']['currency'] == 'USD')
check('recent_fee_amounts', recent['RECENT_01']['recorded_fee']['amount'] == '2.78' and recent['RECENT_02']['recorded_fee']['amount'] == '1.42')
check('all_actual_cost_profit_CAC_unknown', all(r[k]['amount'] is None for r in DATA['worked_existing_data'] for k in ['actual_provider_settlement_usd', 'actual_net_profit_usd', 'actual_max_cac_usd']))
check('all_markets_unqualified', all(not r['qualified_for_spend'] for r in DATA['market_economics']))
check('worker_limit_not_failure', DATA['measurement']['new_ads_dispatch']['status'] == 'CAPABILITY_LIMIT')
check('unknown_consent_retained', DATA['measurement']['last_passive_observation']['consent_choice'] == 'UNKNOWN')
check('complete_root_capture_not_worker_claim', DATA['measurement']['last_passive_observation']['selected_events'] == 576 and not DATA['measurement']['last_passive_observation']['truncated'])
check('no_current_readiness_promotion', not any(DATA['readiness'][k] for k in ['measurement_ready', 'financially_qualified', 'launch_authorized']))
check('30d_not_90d', DATA['baseline_reports'][0]['orders'] == 10 and DATA['baseline_reports'][1]['orders'] == 43)
check('partial_zero_report_not_receiver', DATA['baseline_reports'][2]['orders'] == 0 and DATA['measurement']['genuine_purchase']['status'] == 'NOT_RUN')

# Adversarial rejection cases protect the actual decision boundaries.
cases = [
    ('wrong_destination', lambda d: d['identities'].__setitem__('new_destination', 'AW-853411529/wrong')),
    ('unknown_cost_zero', lambda d: d['worked_existing_data'][0]['actual_provider_settlement_usd'].__setitem__('amount', '0')),
    ('unknown_profit_number', lambda d: d['worked_existing_data'][0]['actual_net_profit_usd'].__setitem__('amount', '100')),
    ('market_qualified_without_cost', lambda d: d['market_economics'][0].__setitem__('qualified_for_spend', True)),
    ('measurement_without_purchase', lambda d: d['readiness'].__setitem__('measurement_ready', True)),
    ('economics_without_market', lambda d: d['readiness'].__setitem__('financially_qualified', True)),
    ('launch_without_authority', lambda d: d['readiness'].__setitem__('launch_authorized', True)),
    ('authority_without_receipt', lambda d: d['authority'].__setitem__('new_spend_authorized', True)),
    ('pass_without_evidence', lambda d: d['measurement']['configuration'].__setitem__('evidence_refs', [])),
    ('raw_customer_data', lambda d: d['measurement']['transaction_match'].__setitem__('raw_customer_data_retained', True)),
]
for name, mutate in cases:
    candidate = copy.deepcopy(DATA)
    mutate(candidate)
    try:
        validate(candidate, SCHEMA)
    except ValueError:
        checks.append('rejected_' + name)
    else:
        raise AssertionError('Unexpected acceptance: ' + name)

result = {'status': 'PASS_WITH_LIMITS', 'checked_at_utc': datetime.now(timezone.utc).isoformat(),
          'checks_passed': len(checks), 'checks': checks,
          'schema_validation': 'All assertion keywords used by this schema covered by bounded local checker; not a general Draft2020-12 engine',
          'external_calls': 0, 'independent_native_replay': False,
          'full_schema_engine_limit': 'System Python lacks jsonschema; python3.13 unavailable; Node has missing simdjson dylib. No install or environment repair attempted.'}
if '--report' in sys.argv:
    (HERE / 'validation.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
