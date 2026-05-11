# Next Continuation Prompt

Latest anchor: `AGENT_CONTINUITY_ANCHOR: 2026-05-10-paid-growth-multilingual-platform-matrix`

Use the single owner-standard prompt in `ops/prompts/paid-growth-ai-army-continuation-prompt.md`. Do not create a competing prompt.

Paste this:

```text
Continue the Dress Like Mommy paid-growth sprint in `/Users/fsuels/Projects/dresslikemommy`.

Use `ops/prompts/paid-growth-ai-army-continuation-prompt.md` as the canonical operating prompt. Read it first and follow it, not just summarize it.

Act as the parent/orchestrator. Use parallel subagents wherever supported, with disjoint workstreams and separate browser/account tabs when needed.

Follow the problem-solving protocol and update `ops/PROBLEM_TRACKER.md` for every active problem, failed readback, blocker, attempt, result, approval gate, and solved status. Do not document known problems passively. Work the solution until fixed, disproven, superseded by a safer path, or gated with the exact next unblock action.

Guardrails: no live spend, no campaign enablement, no budget/bid/status changes, no PMax enable, no Standard Shopping changes, no product-scope/feed-label/product-group changes, no conversion-goal changes, no Merchant uploads, and no Shopify live product-data changes unless I give fresh explicit action-time approval.

Start now. Inspect, plan, split the work, execute safe read-only/local/paused-build work, verify, update evidence packets, update `ops/PROBLEM_TRACKER.md`, update `ops/AGENT_WORKLOG.md` with a new `AGENT_CONTINUITY_ANCHOR`, and finish with the next continuation prompt.
```

State to preserve from this packet:

- Google Ads current state remains `12 built / 3 absent / 2 parked`.
- Built/read back paused: `GB`, `CA`, `AU`, `CH`, `DK`, `DE`, `NL`, `SE`, `ES`, `IT`, `PL`, `CZ`.
- Absent: `RO`, `PT`, `GR`.
- Parked: `FR`, `BE`.
- All 17 Google Ads split CSVs are locally present and passed the session's structural guardrail parse.
- Pinterest is only US `en-US` local-template-ready: clean `342` rows, `4` exclusions, Event Quality `Fair`; no non-US Pinterest setup exists.
- Stricter current guardrail means no new paused account object should be created if it requires setting initial budget/bid/status unless the owner gives explicit action-time approval that reconciles that conflict.

Next best workstreams:

- Measurement agent: prove non-US purchase event currency/value or prepare controlled test purchase approval.
- Google Ads agent: wait for exact branch approval to retry `RO` or skip/park `RO` and continue `PT` then `GR`; do not re-upload completed countries.
- Pinterest agent: request exact paused US draft approval or read-only Event Quality verification approval; do not write account objects without it.
- QA/localization agent: drive native-speaker review and landing-language QA for the 14 locale variants.
- Parent/docs agent: keep `ops/PROBLEM_TRACKER.md`, `ops/AGENT_WORKLOG.md`, and packet evidence current.
