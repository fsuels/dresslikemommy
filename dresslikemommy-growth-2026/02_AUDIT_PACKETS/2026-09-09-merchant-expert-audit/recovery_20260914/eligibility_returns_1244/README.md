# Merchant eligibility and returns — September 14, 2026

Status: **PARTIAL operational setup; bounded current read completed.**

- Google’s account setup/policy page now says “No issues for you to fix.” Four protected US/Australia representatives are Approved, In stock and marked as showing through Free listings, with the expected prices.
- US and Australia each retain 4,761 source offers. The latest US scheduled fetch failed with “Connection failed.” Australia’s September 11 manual submission remains clean.
- The product dashboard reports 9,522 total and 54 not showing, with its data timestamp at September 13 midnight. The remaining displayed issue is image processing. This is not a measured traffic or sales result.
- The only configured return policy is Verified for Austria. US/Australia coverage and product exceptions are absent from that policy list.
- The current saved refund policy, linked Shopify page and public US/English page agree on conditional 30-day returns. Current Terms separately exclude all sale/personalized items, so the policy conflict remains.
- US Store Quality still has no score. Neither a specific cause nor a badge timeline is established.

No sources, offers, policies, prices, shipping, theme, paid settings or account controls were changed during this follow-up. No upload, Update, appeal, blocked download or Worker access retry occurred. Native policy inspection was cancelled with the single existing policy intact.

## Evidence

- [Eligibility and source health](native_eligibility_and_source_health.json)
- [Current return source and field qualification](return_policy_source_qualification.json)
- [Decision, unmet dependencies and handoff](decision_and_handoff.json)
- [Executor consistency checks: 28/28 passed](local_receipt_checks.json)

Independent review is requested from the parent; these consistency checks are not an independent verification.

Next channel action: diagnose and correct the failed existing US scheduled fetch. This comes first because the offers can now show, while failed fetching threatens catalog freshness. Return expansion remains gated by policy consistency and complete current exception assignments.

Continue through the existing [paid-growth continuation prompt](/Users/fsuels/Projects/dresslikemommy/ops/prompts/paid-growth-ai-army-continuation-prompt.md), preserving the Merchant owner, existing sources and all six product holds.
