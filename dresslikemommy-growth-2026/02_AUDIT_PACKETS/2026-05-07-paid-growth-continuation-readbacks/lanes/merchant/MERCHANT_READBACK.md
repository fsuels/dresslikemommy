# Merchant / Google & YouTube Source Refresh Readback

Generated: 2026-05-07 14:36 EDT

Scope: read-only Merchant Center, Google & YouTube, and Shopify paid-cohort checks for account `124884876` and sample offer `shopify_US_7227254276193_41871113158753`.

No live writes were made. I did not repeat the Google & YouTube unpublish/republish toggle. I did not upload Merchant data, edit Shopify products, change feeds, labels, product groups, campaigns, conversion goals, budgets, bids, or statuses.

## Lane Board

- Moving: none; readbacks completed.
- Blocked: full Merchant API product-issues export is blocked by local Google OAuth scopes.
- Waiting on approval: any repeat Google & YouTube source action, Merchant upload, feed edit, product edit, or campaign/feed-scope change.
- Done: browser sample source timestamp readback, browser diagnostics page text capture, Shopify paid-cohort age_group dry-run, API diagnostics attempt with blocker artifact.
- Next safe parallel action: wait for Merchant processing, then re-run the same read-only sample timestamp plus diagnostics/product-issues readback; do not toggle again unless the parent has fresh explicit approval.

## Results

### Merchant browser source/timestamp readback

Command:

```bash
python3 ops/scripts/check_merchant_center_clean_labels_live.py --account 124884876 --cdp-port 9222 --sample-offer-id shopify_US_7227254276193_41871113158753 --expected-labels-csv dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-29-merchant-clean-label-upload/upload_matched_full_clean_labels_with_age_group.csv --output-dir dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-paid-growth-continuation-readbacks/lanes/merchant/browser-source-readback
```

Artifact:

- `browser-source-readback/merchant_exact_label_readback_refresh_check.json`

Output summary:

- `gate_status`: `PASS_CAMPAIGN_FILTER_LABELS_VISIBLE`
- `full_label_gate_status`: `PASS_ALL_EXPECTED_LABELS_VISIBLE`
- US/en sample source timestamp: `2026-05-07T14:14:02+00:00`
- Source: `10627623003` / `Shopify App API`
- Labels still visible: `custom_label_0=paid_eligible`, `custom_label_4=us_test_ready`
- Full expected sample labels visible: `paid_eligible`, `margin_medium`, `swimsuits`, `aov_medium`, `us_test_ready`
- Observed mismatches: none

Interpretation:

- The paid-campaign labels are still present.
- The US/en source row has not advanced beyond the old `2026-05-07T14:14:02Z` timestamp, so the prior approved single-product publication toggle has not yet produced a newer US/en source row for this sample.
- The sample also has newer non-US/localized rows in Merchant, but those rows do not carry the paid US labels and do not resolve the US/en age_group propagation question.

### Merchant diagnostics page readback

Command:

```bash
python3 - <<'PY'
import json, re, time, urllib.parse, urllib.request
from datetime import datetime
from pathlib import Path
import websocket

OUT = Path('dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-paid-growth-continuation-readbacks/lanes/merchant/diagnostics-browser-readback')
OUT.mkdir(parents=True, exist_ok=True)
url = 'https://merchants.google.com/mc/products/diagnostics?a=124884876&marketingMethod=16&priorityFixes=true'
endpoint = 'http://127.0.0.1:9222/json/new?' + urllib.parse.quote(url, safe=':/?=&')
req = urllib.request.Request(endpoint, method='PUT')
with urllib.request.urlopen(req, timeout=10) as response:
    target = json.loads(response.read().decode('utf-8'))
ws = websocket.create_connection(target['webSocketDebuggerUrl'], timeout=30, suppress_origin=True)
msg_id = 1
def call(method, params=None, timeout=15):
    global msg_id
    mid = msg_id
    msg_id += 1
    ws.send(json.dumps({'id': mid, 'method': method, 'params': params or {}}))
    start = time.time()
    while time.time() - start < timeout:
        event = json.loads(ws.recv())
        if event.get('id') == mid:
            return event
    raise TimeoutError(method)
try:
    call('Page.enable')
    call('Runtime.enable')
    time.sleep(8)
    call('Page.reload', {'ignoreCache': True})
    time.sleep(15)
    result = call('Runtime.evaluate', {'expression': "document.body ? document.body.innerText : ''", 'returnByValue': True}, timeout=30)
    text = result.get('result', {}).get('result', {}).get('value', '') or ''
finally:
    ws.close()
lines = [re.sub(r'\s+', ' ', line).strip() for line in text.splitlines()]
lines = [line for line in lines if line]
(OUT / 'diagnostics_page_text.txt').write_text('\n'.join(lines) + ('\n' if lines else ''), encoding='utf-8')
summary = {
    'generated_at': datetime.now().isoformat(timespec='seconds'),
    'mode': 'READ_ONLY_MERCHANT_DIAGNOSTICS_PAGE_TEXT_CAPTURE',
    'url': url,
    'target_id': target.get('id'),
    'line_count': len(lines),
    'interesting_lines': [line for line in lines if any(p in line.lower() for p in ['missing age group', 'age group', 'limited performance', 'needs attention', 'not approved', 'pending', 'approved'])][:120],
    'missing_age_group_lines': [line for line in lines if 'missing age group' in line.lower()][:40],
    'notes': ['Captured document.body.innerText from a separate Merchant Diagnostics tab via CDP; no Merchant edits/uploads were made.'],
}
(OUT / 'diagnostics_page_summary.json').write_text(json.dumps(summary, indent=2, sort_keys=True) + '\n', encoding='utf-8')
print(json.dumps({k: summary[k] for k in ['generated_at', 'line_count', 'missing_age_group_lines', 'interesting_lines']}, indent=2))
PY
```

Artifacts:

- `diagnostics-browser-readback/diagnostics_page_summary.json`
- `diagnostics-browser-readback/diagnostics_page_text.txt`

Output summary:

- Diagnostics page capture generated at `2026-05-07T14:35:21`
- Visible page text included `Last updated at 2:33 PM May 7, 2026`
- Visible issue examples still included `Missing age group`
- Visible page text also included Merchant's platform diagnostic label `Missing local inventory data`

Interpretation:

- Merchant diagnostics has refreshed more recently than the previous 2:01 PM readback, but the visible diagnostics UI still shows `Missing age group`.
- This browser text capture is not a full product-issues export and does not prove the exact paid-cohort count; it is a current UI clue that the issue has not cleared.
- Owner correction: Dress Like Mommy is a dropshipping business with no physical store and no owned physical inventory. The `Missing local inventory data` line is a Merchant Center diagnostic label only; it should not be interpreted as a requirement to claim or create physical/local inventory, and no Shopify inventory quantity or warehouse/store promise should be fabricated from this readback.

### Shopify paid-cohort age_group dry-run

Command:

```bash
python3 ops/scripts/repair_paid_cohort_variant_age_group.py --output-dir dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-paid-growth-continuation-readbacks/lanes/merchant/shopify-age-group-dry-run
```

Artifacts:

- `shopify-age-group-dry-run/summary.json`
- `shopify-age-group-dry-run/planned_variant_age_group_updates.csv`

Output summary:

- `execute`: `false`
- Target paid variant rows: `780`
- Planned updates: `0`
- Skipped rows: `780`
- Reason counts: `already_correct: 780`

Interpretation:

- Shopify-side ProductVariant `mm-google-shopping.age_group` remains correct for all current paid-cohort variants.
- No Shopify product-data write is needed from this lane.

### Merchant API product-issues export attempt

Command:

```bash
python3 ops/scripts/export_merchant_center_api_diagnostics.py --merchant-id 124884876 --input-eligibility dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-06-live-visual-qa-merchant-age-group-gate/paid_cohort_age_group_after_patch_rows.csv --output-dir dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-paid-growth-continuation-readbacks/lanes/merchant/api-product-issues
```

Artifacts:

- `api-product-issues/merchant_center_api_diagnostics_summary.json`
- `api-product-issues/merchant_center_api_diagnostics_evidence.csv`
- `api-product-issues/merchant_center_api_diagnostics_raw.jsonl`

Output summary:

- Token source: `gcloud auth print-access-token`
- Merchant API `products.list`: `403 PERMISSION_DENIED`, insufficient authentication scopes
- Content API `productstatuses.list`: `403 PERMISSION_DENIED`, insufficient authentication scopes
- Current variant rows scanned from input: `780`
- Merchant evidence rows: `0`

Interpretation:

- Full API product-issues export remains blocked by local Google OAuth scopes.
- The script wrote header-only/empty blocker artifacts instead of fabricating status.

## Blockers

- Full Merchant product-issues evidence needs either a Google token with Merchant/Content API scopes or a browser-export path that exposes item-level diagnostics/counts.
- The sample US/en source timestamp remains old, so there is no evidence yet that the Shopify age_group fix has propagated into the Merchant US/en source row.

## Next Safe Action

Wait for additional Merchant processing time, then repeat the read-only sample timestamp check and diagnostics/product-issues readback. Do not repeat the Google & YouTube toggle, edit product data, upload feeds, or change campaign/feed scope unless the parent has fresh explicit approval.
