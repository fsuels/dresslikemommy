#!/usr/bin/env bash
# Generate IMAGE 1/3/5/6 per draft with the ChatGPT app's bundled Codex (owner's Pro login, no API billing).
# One listing at a time, in an isolated scratch dir (keeps the repo AGENTS.md out of Codex's context).
set -uo pipefail
ROOT=/Users/fsuels/Projects/dresslikemommy
A=$ROOT/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-26-christmas-pajama-line/tools/ai_images
WORK=/private/tmp/claude-501/-Users-fsuels-Projects-dresslikemommy/a76726b8-00be-4d83-af09-8ad9c025381c/scratchpad/ai_jobs
CODEX=/Applications/ChatGPT.app/Contents/Resources/codex
mkdir -p "$WORK" "$A/logs"
for handle in "$@"; do
  out=$ROOT/uploads/$handle/ai
  if [[ -f $out/image1.png && -f $out/image3.png && -f $out/image5.png && -f $out/image6.png ]]; then
    echo "$(date +%T) $handle skip (already has 4 images)"; continue
  fi
  attempt=0
  while (( attempt < 4 )); do
    attempt=$((attempt+1))
    w=$WORK/$handle; rm -rf "$w"; mkdir -p "$w"
    cp "$out"/ref*.jpg "$out/prompt.txt" "$w/"
    start=$(date +%s)
    ( cd "$w" && perl -e "alarm shift; exec @ARGV" 3000 "$CODEX" exec --skip-git-repo-check -C "$w" -s workspace-write \
        -i "$w/ref1.jpg" -i "$w/ref2.jpg" -i "$w/ref3.jpg" - < "$w/prompt.txt" ) > "$A/logs/$handle.try$attempt.log" 2>&1
    rc=$?
    n=$(ls "$w"/image{1,3,5,6}.png 2>/dev/null | wc -l | tr -d ' ')
    echo "$(date +%T) $handle try$attempt rc=$rc images=$n secs=$(( $(date +%s) - start ))"
    if [[ $n == 4 ]]; then cp "$w"/image{1,3,5,6}.png "$out/"; break; fi
    if grep -q -i -E "rate limit|usage limit|quota|too many requests|try again later" "$A/logs/$handle.try$attempt.log"; then
      echo "$(date +%T) $handle limit hit; pausing 30 min"; sleep 1800
    fi
  done
done
echo "$(date +%T) DONE"
