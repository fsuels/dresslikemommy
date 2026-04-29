# Pinterest Arabic/Portuguese Next-Feed Recheck - 2026-04-29

Read-only recheck through the authenticated Chrome/CDP Pinterest session on Apr 29, 2026 around 12:19 AM EDT.

## Evidence

- Raw captures: `dresslikemommy-growth-2026/01_EXPORTS_RAW/PINTEREST/2026-04-29_next_ar_pt_catalog_recheck/`
- Prior completed-feed packet: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-29_PINTEREST_POST_INGESTION_RECHECK.md`

## Result

No new completed Arabic or Portuguese feed was available yet.

| Feed | Data source ID | Current latest completed ingestion | Warning total | Warning 188 | Warning 1039 | Warning 126 | Interpretation |
|---|---:|---:|---:|---:|---:|---:|---|
| ar | 3041760849210539103 | Apr 28 at 10:18 PM EDT | 2,071 | 2,010 | 114 | 4 | Same completed run already captured; not a new post-fix ingestion. |
| pt-BR | 3041760900274511922 | Apr 28 at 9:19 AM EDT | 2,071 | 2,010 | 114 | 4 | Still pre-fix relative to the Apr 28 evening Shopify fixes. |

The data-source overview also showed other feeds moving, including `ko` and `ja` in `Processing` and `he` completed at Apr 28 at 11:26 PM EDT, but those were not the requested Arabic/Portuguese feeds.

## Decision

Do not export Pinterest issue details yet, and do not start global archived legacy cleanup yet. The escalation condition was "same counts persist after one more post-fix ingestion"; this recheck did not find a newer Arabic or Portuguese completed ingestion to evaluate.

If Arabic or Portuguese completes another post-fix ingestion and still shows the same counts, treat it first as a Pinterest/Shopify feed-profile cache/support issue because current Shopify Admin readbacks were already clean for active Online Store + Pinterest scope. Only consider global archived legacy cleanup if the exported Pinterest issue details prove Pinterest is still counting archived/unpublished legacy rows and channel/support cannot clear or ignore them.

## Next Check Window

Based on the visible feed cadence:

- pt-BR next expected completion window: Apr 29, 2026 after about 9:19 AM EDT.
- ar next expected completion window: Apr 29, 2026 after about 10:18 PM EDT.
