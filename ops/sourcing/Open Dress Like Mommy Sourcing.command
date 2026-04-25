#!/bin/zsh
set -e

cd /Users/fsuels/Projects/dresslikemommy

PORT=8766
URL="http://127.0.0.1:${PORT}/"
LOG="/tmp/dresslikemommy-sourcing-dashboard.log"

if ! /usr/sbin/lsof -nP -iTCP:${PORT} -sTCP:LISTEN >/dev/null 2>&1; then
  /usr/bin/nohup /Users/fsuels/Projects/dresslikemommy/ops/sourcing/start-sourcing-dashboard.sh > "${LOG}" 2>&1 &
  sleep 1
fi

/usr/bin/open "${URL}"
