# Paid Growth Single Continuation Prompt Canonicalization

Date: 2026-05-08

Anchor: `AGENT_CONTINUITY_ANCHOR: 2026-05-08-paid-growth-single-continuation-prompt-canonicalized`

## Why

The owner asked why prior sessions produced multiple different continuation prompts and stated that one stable prompt must always work in any new session.

Root cause: the paid-growth canonical prompt and memory protocol told agents to produce session-specific continuation prompts, while evidence packets also contained `NEXT_CONTINUATION_PROMPT.md` files. That made packet prompts, final-message prompts, and the canonical prompt look like separate choices.

## Change

The canonical prompt now has a single-prompt rule:

- The owner-standard prompt is embedded at the top of `ops/prompts/paid-growth-ai-army-continuation-prompt.md`.
- Future sessions should use that prompt as the reusable entry point.
- The latest state must be recovered from durable repo memory: `AGENTS.md`, the bottom of `ops/AGENT_WORKLOG.md`, `ops/PROBLEM_TRACKER.md`, and `ops/AGENT_COORDINATION.md`.
- Packet `NEXT_CONTINUATION_PROMPT.md` files, if created, should be pointers back to the canonical prompt plus the latest anchor/gates, not alternate operating prompts.
- Final responses should not give the owner multiple competing prompts.

## Files Updated

- `ops/prompts/paid-growth-ai-army-continuation-prompt.md`
- `AGENTS.md`
- `ops/MEMORY_CONTINUITY_PROTOCOL.md`
- `ops/PROBLEM_TRACKER.md`
- `ops/AGENT_WORKLOG.md`

## Guardrails

Prompt/memory/process update only.

No external account writes, no live spend, no campaign enablement, no budget/bid/status changes, no PMax enable, no Standard Shopping changes, no product-scope/feed-label/product-group changes, no conversion-goal changes, no Merchant uploads, no Shopify live product-data changes, no Pinterest writes, no checkout payment/order, and no theme publish.

## Result

`PROB-2026-05-08-CONTINUATION-PROMPT-SPLIT` is solved by making `ops/prompts/paid-growth-ai-army-continuation-prompt.md` the only canonical operating prompt and clarifying that all future prompts/readbacks must point back to it.
