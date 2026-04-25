#!/bin/zsh
set -e

cd /Users/fsuels/Projects/dresslikemommy

PORT="${DLM_SOURCING_PORT:-8766}"
LOG="${DLM_SOURCING_LOG:-/tmp/dresslikemommy-sourcing-dashboard.log}"

if /usr/sbin/lsof -nP -iTCP:${PORT} -sTCP:LISTEN >/dev/null 2>&1; then
  exit 0
fi

exec /usr/bin/python3 ops/scripts/1688_sourcing_dashboard.py --host 127.0.0.1 --port "${PORT}" >> "${LOG}" 2>&1
