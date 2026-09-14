# Weekly Dream Review

Integration status: `GENERATED`

As of: `2026-07-09`

Purpose: local-only consolidation of recent repo memory. This report does not authorize live writes.

## Safety Boundary

- Read local files only.
- No Shopify Admin, Google Ads, Pinterest, Merchant Center, GA4/GTM, feed, campaign, product, theme, billing, credential, payment, order, or publication writes.
- Suggested prompt or checklist changes require human review before promotion.

## Sources Read

| Source | Exists | Lines read | Anchors in file |
|---|---:|---:|---:|
| `ops/AGENT_WORKLOG.md` | `true` | `900/46000` | `1276` |
| `ops/PROBLEM_TRACKER.md` | `true` | `3838/3838` | `2` |
| `ops/AGENT_COORDINATION.md` | `true` | `267/267` | `193` |
| `ops/marketing/memory_digest.md` | `true` | `99/99` | `0` |
| `ops/marketing/dream_consolidation_prompt.md` | `true` | `47/47` | `0` |
| `ops/prompts/paid-growth-ai-army-continuation-prompt.md` | `true` | `230/230` | `4` |
| `docs/agent-loops/self-improvement-pilot-loop.md` | `true` | `93/93` | `0` |
| `docs/agent-loops/localized-pdp-quality-loop.md` | `true` | `107/107` | `0` |

## Latest Worklog Anchors

- `AGENT_CONTINUITY_ANCHOR: 2026-06-29-red-tropical-leaf-active-size-correction-complete`
- `AGENT_CONTINUITY_ANCHOR: 2026-07-02-localized-pdp-quality-loop-designed`
- `AGENT_CONTINUITY_ANCHOR: 2026-07-02-sunshine-daisy-es-visible-localization-pass-review-widget-raw-gate`
- `AGENT_CONTINUITY_ANCHOR: 2026-07-09-paid-growth-handoff-self-improvement-pilot`
- `AGENT_CONTINUITY_ANCHOR: 2026-07-09-weekly-dream-review-local-loop`

## Cross-Session Signals

| Signal | Count | Meaning | Proposed Rule |
|---|---:|---|---|
| Monitoring can become the deliverable | `6` | Agents keep needing reminders that watching numbers is not progress unless it creates a decision, fix, approval packet, reroute, or evidence-backed hold. | Keep handoffs tied to one action outcome: fix now, bounded approved action, exact approval packet, reroute, or hold with evidence. |
| Next action discipline matters | `7` | The repo repeatedly values one owner-ready next action over option lists. | Every dream review and paid-growth handoff should name exactly one recommended next action. |
| Live-risk approvals stay explicit | `370` | The useful memory is only safe if it preserves the line between local prep and live writes. | Treat all dream-review output as local advisory evidence unless the owner gives fresh action-time approval. |
| Source and inventory claims need guards | `147` | Listing, feed, and ad work can hurt trust if source details or false inventory claims leak. | Before paid traffic or publication, keep source-leak and dropshipping-honesty checks in the owning loop. |
| Localized PDP quality is a repeatable gate | `282` | International growth depends on pages that look native enough for shoppers, not just translated enough for an API check. | Run the localized PDP quality loop before treating translated products as ready for paid traffic. |
| Feed grouping cannot regress | `40` | Pinterest and catalog work has a hard parent/variant grouping rule. | Keep the grouping guard wired into continuity and do not approve per-variant feeds without parent grouping. |
| A local scorecard already exists | `53` | The project already has a small local scorecard; the next step is regular use, not a new command layer. | Use the handoff scorecard before changing the canonical paid-growth prompt or closing risky handoffs. |

## Proposed Local Improvements

- Keep handoffs tied to one action outcome: fix now, bounded approved action, exact approval packet, reroute, or hold with evidence.
- Every dream review and paid-growth handoff should name exactly one recommended next action.
- Treat all dream-review output as local advisory evidence unless the owner gives fresh action-time approval.
- Before paid traffic or publication, keep source-leak and dropshipping-honesty checks in the owning loop.
- Run the localized PDP quality loop before treating translated products as ready for paid traffic.
- Keep the grouping guard wired into continuity and do not approve per-variant feeds without parent grouping.
- Use the handoff scorecard before changing the canonical paid-growth prompt or closing risky handoffs.

## Recommended Next Action

- Use the existing Pinterest Phase 1 paused replacement setup gate as the first paid-growth action if the owner chooses Pinterest next: keep the campaign paused, require the exact approval phrase, read back before and after, and do not relaunch spend.

## Review Decision

- `KEEP_LOCAL_ONLY`: this report may guide the next session, but it does not change canonical prompts or live business systems by itself.
- If a future prompt/checklist change is proposed, test it against a small example set and rerun continuity checks before promotion.

## Command

```bash
python3.13 ops/scripts/generate_weekly_dream_review.py --as-of YYYY-MM-DD --write-report dresslikemommy-growth-2026/02_AUDIT_PACKETS/YYYY-MM-DD-weekly-dream-review/WEEKLY_DREAM_REVIEW.md
```
