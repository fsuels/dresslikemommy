#!/usr/bin/env bash
set -uo pipefail
T="/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-26-christmas-pajama-line/tools"
cd /Users/fsuels/Projects/dresslikemommy
echo "$(date +%H:%M:%S) waiting for peer translation processes"
while pgrep -f "ops/scripts/(poll_shopify_product_translations|finalize_shopify_listing_localization|repair_localized_product_size_charts)\.py" >/dev/null; do sleep 60; done
echo "$(date +%H:%M:%S) idle; seeding cache"
python3 "$T/seed_cache.py" 2>&1 | grep -v -i -E "NotOpenSSL|warnings.warn"
"$T/run_all.sh" "$T"/specs/*.json
