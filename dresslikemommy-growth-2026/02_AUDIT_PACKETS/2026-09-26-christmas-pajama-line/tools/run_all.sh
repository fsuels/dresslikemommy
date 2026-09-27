#!/usr/bin/env bash
# Run the canonical per-design listing runners one at a time (the shared
# translation cache has no cross-process lock). Logs to tools/run_logs/.
set -uo pipefail
ROOT="/Users/fsuels/Projects/dresslikemommy"
T="$ROOT/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-26-christmas-pajama-line/tools"
mkdir -p "$T/run_logs"
wait_idle() {
  while pgrep -f "ops/scripts/(poll_shopify_product_translations|finalize_shopify_listing_localization|repair_localized_product_size_charts)\.py" >/dev/null; do sleep 60; done
}
for spec in "$@"; do
  [[ "${LISTING_DEFER_CLOSEOUT:-0}" == "1" ]] || wait_idle
  handle=$(basename "$spec" .json)
  code=$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['shortcode'].lower())" "$spec")
  runner="$ROOT/ops/scripts/create-$code-$handle.sh"
  start=$(date +%s)
  bash "$runner" > "$T/run_logs/$handle.log" 2>&1
  rc=$?
  status=$(python3 -c "import json,sys;print(json.load(open(sys.argv[1])).get('status'))" "$ROOT/ops/listings/$handle-localization-closeout.json" 2>/dev/null)
  echo "$(date +%H:%M:%S) $handle rc=$rc closeout=$status secs=$(( $(date +%s) - start ))"
done
echo DONE
