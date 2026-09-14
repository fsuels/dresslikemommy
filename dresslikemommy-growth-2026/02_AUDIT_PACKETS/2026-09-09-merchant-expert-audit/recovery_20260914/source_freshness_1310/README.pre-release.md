# US source freshness — September 14, 2026

Status: **PARTIAL — fresh candidate prepared; independent review and live release pending.**

The stored US pointer still carries the September 11 21:18:15.731 UTC source scan and was 63.89 hours old at the one initial supported pointer read. The existing host expires a feed after 48 hours. This is consistent with the native September 14 “Connection failed” receipt; the public host response was not retried or independently read here.

The unchanged existing builder completed a new exact Shopify US source scan at **13:16:10.466 UTC**: 238 active parents, 4,925 variants, 4,903 available. Applying the unchanged six-parent holds excludes 162 available variants. All 22 unavailable variants are omitted. The candidate contains **4,741 offers from 232 parents**.

The candidate removes 20 offers from two parents absent from the complete current ACTIVE source scan. There are no new offers or changed retained feed fields. All 4,741 retained rows match the prior release, every price matches the fresh Shopify source, the pilot remains $17.99, and the five corrected Adult 2XL prices remain $22.99. Absence from the active source does not establish whether a product was archived or deleted.

Executor checks: **28/28 PASS**, not independent approval. The candidate packet and release/rollback bindings were sent to the existing parent reviewer. The exact source freshness deadline for release is **15:16:10.466 UTC**. Before-pointer and feed bytes are preserved; the expired old pointer must not be restamped or described as a healthy rollback.

No Cloudflare write, Google Update, AU upload, policy change, Worker change, scheduler change or credential transfer occurred during preparation. Shared canonical files remain parent-owned. US Google receipt and source recovery are unverified until exact independent approval, existing guarded promotion, and native source readback complete. Other markets and Store Quality remain open in the preceding eligibility/returns packet.

Evidence:
- `pointer_first_read.json` and `prepare_guard_readback.json`
- `candidate_source_delta_checks.json`
- `release_and_rollback_bindings.json`
- Existing-format candidate under `local_lifecycle_interim/runs/20260914T131200Z-us-freshness/`
