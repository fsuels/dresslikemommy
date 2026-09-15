# Merchant refresh repair — September 14

The catalog refresh fallback is implemented and independently verified. It can now use the current generator without applying product exclusions twice or stopping simply because a previously protected listing was archived.

- **69 checks passed:** 61 focused tests plus eight independent failure cases.
- **4,741 US rows matched exactly** when replaying the saved complete catalog. The six product holds remained intact.
- **The existing daily task was updated** to use this reviewed process for the next due source refresh.

This run changed local refresh code and the existing task instructions. It did not upload another feed or activate cloud credentials. The saved source timestamp remains September 14 at 13:16 UTC; the next proactive US refresh target is September 15 at 13:16 UTC.

The most recent live evidence from earlier today showed 4,741 approved products each for the US and Australia. The other 29 configured countries still lacked products, and Store Quality still showed no score. Those facts were not re-audited during this repair.

The next owner action remains publication of the reviewed **DLM UX Performance QA 2026-09-10** theme, ID **137888792673**, through Shopify Admin. Its variant-entry correction must be live and verified before the next localized/Canada/UK feeds. The connector explicitly prohibits agent theme publication and MAIN writes. Existing questions about Canada/UK delivery, return-policy conflicts, and the dedicated cloud app remain pending; no duplicate question was sent.

Use [execution_handoff.json](execution_handoff.json) for exact evidence, limits and the next internal actions. The single continuation entry remains `ops/prompts/paid-growth-ai-army-continuation-prompt.md`.
