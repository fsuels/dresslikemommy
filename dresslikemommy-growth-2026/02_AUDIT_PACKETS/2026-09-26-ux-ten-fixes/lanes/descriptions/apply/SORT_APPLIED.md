# Pajama collections seasonal MANUAL order — applied 2026-09-26 (~20:25 UTC)

Owner approval: "yes, continue implementing everything" / "I want you to do the work" (chat, 2026-09-26).
Channel: Shopify connector (Admin GraphQL). The stored Admin tokens returned 401 at the time.

- Before: `family-pajamas` (Collection/140957614177) and `pajamas` (Collection/240129605) both `CREATED_DESC`. Position 1 was `snowflake-reindeer-family-matching-onesie-pajamas`. The rule was unchanged (TYPE = Matching Family Pajamas AND TAG = Pajamas); the peer rule edit landed 2026-09-24.
- Writes: `collectionUpdate sortOrder: MANUAL` on both, then `collectionReorderProducts` with positions 0-7 per §3 of SORT_ORDER_PACKET.md. Jobs: daf6f4d7-… (family-pajamas) and 28e77457-… (pajamas). userErrors: none.
- Readback (LIVE_VERIFIED, public products.json): both collections start beanie-ghost, pumpkin-ghost, boo-stripe, trick-or-treat, spooky-skeleton, monster-bloom, snowflake-reindeer, autumn-woodland-bunny.
- Rollback: `collectionUpdate(input:{id, sortOrder: CREATED_DESC})` on each.
- REQUIRED follow-ups: ~2026-10-15 move Christmas pajamas to the top and drop Halloween below the long-sleeve sets; after 2026-11-01 put Halloween last. New pajama products land at the END of a MANUAL collection.
