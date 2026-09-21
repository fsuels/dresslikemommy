# Local main sync scope inventory

Confidence: H for observed Git metadata and path counts; M for dated completion/owner applicability. Advisory only. Snapshot: 2026-09-15T07:15:34.473350+00:00 through 2026-09-15T07:15:34.685737+00:00.

Branch `main`; HEAD `949dab7a0f6c7b853eca034fbf645e68055c552b`. Staged index: 0 paths. Observed 3,160 dirty/untracked paths: 30 tracked modifications and 3,130 untracked paths. No Git mutation was performed.

## Path groups

| Group | Paths |
| --- | ---: |
| production_theme | 2 |
| theme_deployment_controls | 0 |
| ops_canonical | 12 |
| ops_other | 14 |
| evidence_packet | 3,132 |
| other_project | 0 |

The JSON records every observed path under its exact directory, Git status and filesystem metadata, with owner scope, advisory disposition and prior-review membership. Only path metadata was collected from dirty files.

| Evidence packet | Paths |
| --- | ---: |
| 2026-09-05-ceo-turnaround | 1,917 |
| 2026-09-09-merchant-expert-audit | 526 |
| 2026-09-09-microsoft-ads-rebuild | 26 |
| 2026-09-09-organic-growth | 181 |
| 2026-09-10-storefront-ux-pagespeed | 464 |
| 2026-09-11-google-ads-signup-tag | 16 |
| 2026-09-15-project-main-sync | 2 |

## Conservative completed scope

16 paths have an observed completion basis: 14 peer-source paths checked by the existing UX sync review and the two root-accepted seven-file disposition reports. They are candidates only after the owner cutoff and fresh byte binding; no current source hash was recomputed here.

Existing review: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-15-project-main-sync/LOCAL_SYNC_REVIEW.json` (SHA256 `39b6bb705a5224d3d4cd95f660ba4983792ec4460ac0df5717948503e6c3c3dd`), completed 2026-09-15T07:06:21.338782+00:00; status `PLAN_READY__EXACT_CANONICAL_AND_ACTIVE_SOURCE_CUTOFF_PENDING`. It already contains the detailed source bindings, privacy exclusions and projection rules. This inventory does not replace or repeat that review.

Reviewed completed source paths:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-09-merchant-expert-audit/recovery_20260911/direct-feed-deployment/automation_release_v1/src/checkpoint.js`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-09-merchant-expert-audit/recovery_20260911/direct-feed-deployment/automation_release_v1/src/shopify-auth.js`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-09-merchant-expert-audit/recovery_20260911/direct-feed-deployment/automation_release_v1/src/worker.js`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-09-merchant-expert-audit/recovery_20260911/direct-feed-deployment/automation_release_v1/wrangler.toml`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-09-merchant-expert-audit/recovery_20260911/direct-feed-deployment/local_lifecycle_interim/README.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-09-merchant-expert-audit/recovery_20260911/direct-feed-deployment/local_lifecycle_interim/lifecycle.py`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-09-merchant-expert-audit/recovery_20260911/direct-feed-deployment/automation_release_v1/src/admin-reader.js`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-09-merchant-expert-audit/recovery_20260911/direct-feed-deployment/automation_release_v1/test/auth-integration.test.mjs`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-09-merchant-expert-audit/recovery_20260911/direct-feed-deployment/automation_release_v1/test/shopify-auth.test.mjs`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-09-merchant-expert-audit/recovery_20260911/direct-feed-deployment/local_lifecycle_interim/native_profile_fixture.mjs`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-09-merchant-expert-audit/recovery_20260911/direct-feed-deployment/local_lifecycle_interim/native_release_profile.py`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-09-merchant-expert-audit/recovery_20260911/direct-feed-deployment/local_lifecycle_interim/release_contract_20260914.json`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-09-merchant-expert-audit/recovery_20260911/direct-feed-deployment/local_lifecycle_interim/test_native_release_profile.py`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-09-merchant-expert-audit/recovery_20260911/direct-feed-deployment/local_lifecycle_interim/verify_native_candidate.mjs`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-05-ceo-turnaround/theme_seven_local_differences_disposition_20260915.json`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-05-ceo-turnaround/theme_seven_local_differences_disposition_20260915.md`

## Active and private holds

Root supplied an active11-file canonical scope; 12 canonical/generated dirty paths were observed. All are held, together with the current CEO checkpoint/evidence, until root resolves the exact final cutoff. No path was guessed eligible from that count difference.

- `ops/AGENT_COORDINATION.md`
- `ops/AGENT_WORKLOG.md`
- `ops/PROBLEM_TRACKER.md`
- `ops/marketing/action_queue.md`
- `ops/marketing/blocker_board.md`
- `ops/marketing/command_layer_integration_audit.md`
- `ops/marketing/current_marketing_state.md`
- `ops/marketing/daily_scorecard.md`
- `ops/marketing/decision_log.md`
- `ops/marketing/memory_digest.md`
- `ops/marketing/operator_cockpit.html`
- `ops/marketing/operator_cockpit.md`

UX retains the critical CSS task and its evidence. Both `assets/theme-inline-head-static-03.css` and `assets/theme-inline-body-static-07.css` remain held even if clean in this snapshot. Merchant, Microsoft, Ads and organic packet owners retain their cutoffs. The remaining packet files are evidence with unknown per-file completion, not a blanket completed-source allowance.

Preserve all 22 existing private exclusions (22 present here), listed exactly in the JSON, and all existing ignored runtime/private caches. The excluded originals were not opened. `ops/AGENT_WORKLOG.md` and `ops/prompts/shopify-listing-from-1688.md` require the existing approved public index projections; the previous listing-prompt projection equaled HEAD. Do not overwrite local originals.

## Safe cutoff and handoff

1. Root finishes the critical head/body CSS acceptance and due sales/canonical integration, runs its final required checks, and names the exact canonical/evidence cutoff to the existing UX Git integrator. Hold all12 observed dirty canonical/generated paths until root resolves its stated11-file scope.
2. UX verifies current branch, HEAD and staged index against the handoff. Preserve any new staged or peer work; this advisory snapshot is not staging authority or a content freeze.
3. Use the existing LOCAL_SYNC_REVIEW path sets and root final exact allowlist. Rebind the14 reviewed completed peer-source paths and the two accepted disposition reports; add other evidence only as an explicitly accepted cutoff snapshot, without claiming those workstreams complete.
4. At the cutoff, obtain a brief no-write handoff for each included owner scope; hash the exact allowed bytes before and after capture. If a path moves, exclude it from that batch or obtain a fresh owner binding. Do not freeze unrelated owners or use blanket git add.
5. Preserve all22 known private exclusions and ignored runtime/private caches. Use the existing approved public index projection for the final worklog, preserving its local original. Revalidate the listing-prompt projection; the prior review found it identical to HEAD, so do not manufacture a change.
6. Stage only the agreed exact paths/blobs, review the index against that allowlist and known exclusions, and run the narrow required cutoff/continuity checks. Commit completed eligible work and honestly labeled evidence under the already requested local-main scope; record the resulting local commit and residual paths.
7. Leave later peer edits for a later cutoff. No Git push, remote synchronization, connected MAIN write or publication belongs to this local commit handoff.

## Limits

- The snapshot is advisory and can become stale immediately while root and peers continue writing.
- No dirty production-theme path does not imply all local theme work is published or no active theme task remains.
- Prior reviewed completed-source hashes were reused as dated evidence and were not freshly rehashed.
- All other evidence paths retain unknown per-file completion; a packet name or review filename does not prove readiness.
- Known private exclusions are preserved from existing review; this is not a fresh sensitive-content clearance.
- No remote freshness, MAIN publication or push was checked or authorized.
- The two inventory output files are created after the snapshot and therefore are not included in its dirty/untracked counts.

HEAD stable during this capture: true. Added paths during capture: 0; removed: 0; status changes: 0. Content stability was not tested.

Only this JSON and Markdown inventory were written. No staging, commits, remote/network calls, source edits, canonical edits, browser/API use or sensitive-content scan occurred.
