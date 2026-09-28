# Paid-acquisition lane: scaling model to $1M a year (2026-09-27)

> **CLOSED 2026-09-28 by the owner: no paid marketing.** Everything below is history. Do not execute any of it; see `ops/marketing/spend_authorization.md` (`REVOKED_BY_OWNER`).

Lane: paid acquisition, planning only. Parent packet: `2026-09-27-million-plan`.
Task class: `BUILD` (local plan). No ad-platform, Merchant, Shopify, GA4 or browser action happened, and no credential was read.

## Evidence labels used here

| Label | Meaning |
|---|---|
| `REPO_KNOWN` | Read from a repo file in this session. The file's own date is given. |
| `REPO_KNOWN (LIVE_VERIFIED <date>)` | The source packet recorded a live readback on that date. It is not current live truth. |
| `LIVE_READBACK_REQUIRED` | Must be read fresh on the exact surface before any action depends on it. |
| `STALE_OR_SUPERSEDED` | Older state that a newer control or record overrides. |
| `MODEL` | Arithmetic from the inputs above. It is only as good as those inputs. |
| `ASSUMPTION` | A planning input that is not proven in repo evidence. It is labeled so it can be replaced. |
| `OWNER_DECISION` | Needs the owner's choice. The agent cannot decide it. |

## 0. Current authority (read before any live step)

- Authoritative control in `ops/marketing/current_marketing_state.md` says: `live_state_mode=STALE_READBACK_REQUIRED`, `approved_external_scope=NONE`, `autonomous_action_ready=false`, `next_best_action=READ_ONLY_MARKETING_RECONCILIATION`. `REPO_KNOWN` (control as of 2026-09-05).
- `spend_authorization.md` still says `APPROVED_ACTIVE` ($80/day total, $5/day per test). That is necessary but not sufficient. With control at `NONE`, **standing spend authority is NONE**. `STALE_OR_SUPERSEDED` for present action.
- There is one narrow exact owner scope: the US Google Search replacement at $20/day average and a $0.20 max CPC. It is `PARTIAL_BLOCKED_GOOGLE_IDENTITY_VERIFICATION`. Draft `10215473139` exists, and nothing was saved or activated. `REPO_KNOWN` (2026-09-23).
- Nothing in this plan grants authority. Each ramp step below still needs the command-layer gates plus the fresh approvals listed in §7.

## 1. Inputs

| Input | Value | Label |
|---|---|---|
| Revenue now | 2026 YTD: 143 orders, $9.1k. 2025: $6.5k. 2020 peak: 2,264 orders, $117.1k | `REPO_KNOWN (LIVE_VERIFIED 2026-09-27)`, profit study §4 |
| AOV | about $66. It has been stable at $55–68 over the years | same |
| Landed cost | 48% of revenue: product/domestic/fees 27% + freight 21% | same, §1 |
| Refunds; payment fees | about 3.7%; about 3.9% (ESTIMATE) | same |
| Contribution before ads | about 44% | same |
| Landed cost by basket | 1 item 65%, 2 items 52% (48% of orders), 3 items 48%, 4 items 45%, 5+ items 43% | same |
| Christmas 2026 pajamas | $35.99 adult / $32.99 child. About 31–40% landed. Family orders run 4–7 items | same, and the Christmas packet §6 |
| Recent price raise | 55 products, floor-based (for example $15.99 → $19.99). Median +18% per the parent | Plan: `REPO_KNOWN` (`reprice_plan.json`). Applied state: `LIVE_READBACK_REQUIRED` |
| Market price lists | Eurozone +15%, UK +15%, Australia +20% | `REPO_KNOWN (LIVE_VERIFIED 2026-09-27)`, worklog anchor `2026-09-27-market-price-adjust-eu-uk-au` |
| Store conversion | Qualified shoppers (mobile OR Google search): 2,342 sessions, 9 purchases, **0.38%**. All sessions: 5,552 sessions, **0.16%** (2026-08-25 → 09-23) | `STALE_OR_SUPERSEDED`: this includes spike day 09-16 and is directional only, n=9 (`DEC-20260926-SPIKE-DAY-EXCLUSIONS`) |
| Google-search funnel | 69 carts → 11 checkouts (30 days to 2026-09-24) | `REPO_KNOWN`, delivery-dates packet |
| Channel history (2019–2021) | Google search $117k, direct $82k, Bing $10.6k (Bing + Yahoo + DDG $20.0k per the study), social about $6k | Parent brief and `REPO_KNOWN`, profit study §4 |
| Q4 share | October–December was 31.2% of 2025 sales | `REPO_KNOWN`, profit study §5 |

## 2. Required orders, sessions and conversion rate (`MODEL`)

### 2a. Orders needed for $1M

| AOV | Orders per year | vs 2020 peak (2,264) |
|---:|---:|---:|
| $66 (today) | 15,152 | 6.7× |
| $80 | 12,500 | 5.5× |
| $90 | 11,111 | 4.9× |
| $100 | 10,000 | 4.4× |
| $150 (Christmas family basket) | 6,667 | 2.9× |

### 2b. Sessions needed (orders ÷ CVR)

| Orders | CVR 0.38% | CVR 1.0% | CVR 1.5% | CVR 2.0% |
|---:|---:|---:|---:|---:|
| 15,152 (AOV $66) | 3.99M | 1.52M | 1.01M | 758k |
| 12,500 (AOV $80) | 3.29M | 1.25M | 833k | 625k |
| 10,000 (AOV $100) | 2.63M | 1.00M | 667k | 500k |

Today the store gets about 5.5k sessions in 30 days (about 67k a year), and more than half of them are low-intent or bots. Qualified traffic is about 2.3k in 30 days (about 28k a year). **At today's 0.38% CVR, $1M is not reachable by buying traffic.** Traffic would have to grow more than 100×, and the economics below show that each click would lose money. CVR and AOV have to move first.

### 2c. Staged run-rate gates (no calendar)

A stage is reached when trailing revenue sustains the run-rate. Use trailing-90-day revenue × 4, adjusted for seasonality with the 2025 month mix, and exclude spike days. Paid share and CVR are the targets that unlock each stage. They are `ASSUMPTION`s to replace with measured values.

| Stage | Run-rate | AOV | Blended CVR | Orders/yr | Sessions/yr | Paid share of revenue | Paid revenue | Ad spend at 6.5× |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| S0 now | about $12k | $66 | 0.38% | about 180 | about 67k | about 0 | — | — |
| S1 | $100k | $75 | 0.8% | 1,333 | 167k | 40% | $40k | $6.2k |
| S2 | $250k | $80 | 1.0% | 3,125 | 313k | 50% | $125k | $19.2k |
| S3 | $500k | $85 | 1.2% | 5,882 | 490k | 55% | $275k | $42.3k |
| S4 | $1M | $90 | 1.4% | 11,111 | 794k | 58% | $580k | $89.2k |

Non-paid share at S4 is about $420k from email/SMS repeat, direct/brand, organic Google/free listings and organic social. That is consistent with history: direct/repeat alone was $82k when the store did $280k over 2019–2021.

**Suggested paid mix at S4** (`ASSUMPTION`; the gates in §5 reallocate it by measured marginal ROAS):
- Google Shopping/PMax/Search: $250k.
- Meta Advantage+ catalog: $150k.
- Pinterest: $70k.
- Microsoft: $60k.
- TikTok: $50k.

### 2d. The click-economics gate (the decisive constraint)

- ROAS = CVR × AOV ÷ CPC. Revenue per click (RPC) = CVR × AOV.
- To hit 650% ROAS, **RPC must be at least 6.5 × CPC.** At the owner's $0.20 cap, that is RPC ≥ $1.30.

| AOV \ CVR | 0.4% | 1.0% | 2.0% | 3.0% |
|---|---|---|---|---|
| $66, CPC $0.20 | 1.3× | 3.3× | **6.6×** | 9.9× |
| $66, CPC $0.15 | 1.8× | 4.4× | 8.8× | 13.2× |
| $100, CPC $0.20 | 2.0× | 5.0× | 10× | 15× |
| $150, CPC $0.20 | 3.0× | **7.5×** | 15× | 22.5× |

- At $66 AOV, paid clicks must convert at **≥ 1.97%** (about 5× the current qualified rate) to reach 650% at a $0.20 CPC.
- A Christmas family basket around $150 needs only **≥ 0.87%**. This is why the Christmas line is the right first paid lane.
- At the current 0.38% and $66 AOV, a $0.20 click returns about 1.25×. That is below break-even (2.25×).
- Conclusion: CRO, AOV (bundles, the free-shipping threshold) and the Christmas basket are paid-growth prerequisites, not side projects.

## 3. Break-even and target ROAS

### 3a. By landed-cost profile (`MODEL`)

- Contribution before ads = 1 − landed − 3.7% refunds − 3.9% fees = 92.4% − landed.
- Break-even ROAS = 1 ÷ contribution.
- ROAS for a 35% net = 1 ÷ (contribution − 35%).

| Landed % | Typical case | Contribution | Break-even ROAS | Net at 650% | ROAS for 35% net |
|---:|---|---:|---:|---:|---:|
| 31% | Best Christmas 2026 pajama baskets | 61.4% | 1.63× | 46.0% | 3.8× |
| 36% | Christmas 2026 midpoint | 56.4% | 1.77× | 41.0% | 4.7× |
| 40% | Worst Christmas 2026 basket | 52.4% | 1.91× | 37.0% | 5.8× |
| 42% | Owner target landed | 50.4% | 1.98× | **35.0%** | 6.5× |
| 45% | 4-item basket | 47.4% | 2.11× | 32.0% | 8.1× |
| 48% | Store average today | 44.4% | 2.25× | 29.0% | 10.6× |
| 52% | 2-item basket (the most common) | 40.4% | 2.48× | 25.0% | 18.5× |
| 65% | 1-item basket | 27.4% | 3.65× | 12.0% | impossible |

Payment fees are a higher share on small orders, so the 1–2-item rows are slightly optimistic. LTV credit is set to 0 until repeat purchase is measured again, because there is currently no post-purchase or win-back flow.

### 3b. Per-channel ROAS rules

All ROAS gates use **Shopify-reconciled revenue** (net merchandise, excluding tax) divided by platform spend. Platform-reported ROAS is diagnostic until §6 is met.

| Channel | Expected basket profile (`ASSUMPTION`) | Kill line | Hold band | Scale gate |
|---|---|---|---|---|
| Google Shopping / free listings (evergreen catalog) | 2–3 items, landed about 48–52% | < 2.5× | 2.5–6.5× | ≥ 6.5× |
| Google Shopping / Search, Christmas 2026 set | 4–7 items, landed about 31–40% | < 2.0× | 2.0–4.7× | ≥ 4.7× (35% net); ≥ 6.5× preferred |
| Google Search, evergreen | 2 items | < 2.5× | 2.5–6.5× | ≥ 6.5× |
| Microsoft Search/Shopping | Same as Google | Same | Same | Same |
| Meta Advantage+ catalog | Unknown; retargeting likely larger baskets | < 2.5× | 2.5–6.5× | ≥ 6.5× (Christmas product set ≥ 4.7×) |
| Pinterest catalog | Unknown | < 2.5× | 2.5–6.5× | ≥ 6.5× |
| TikTok | Unknown, and likely single-item impulse buys | < 3.0× | 3.0–6.5× | ≥ 6.5× |

- Kill lines sit at or just above break-even for the expected basket.
- The **hold band** allows optimization (queries, negatives, products, creative) but no budget increase.
- The owner's 650% North Star is unchanged as the default. The Christmas 4.7× line only says where that product set still clears a 35% net. It is an `OWNER_DECISION` to use it as a scale threshold.

### 3c. Product scope for paid (applies to every channel)

- Exclude from paid any product whose 2-piece landed cost is above 55% until it is repriced or re-sourced. Per the study that includes:
  - the $14.99–16.99 swimsuits (76–77%);
  - the Mommy & Me pajama line (63–70%);
  - Vintage Cottage (53%), which is borderline.
- Several of these were in the 55-product reprice, so recompute the landed cost at the new prices first (`LIVE_READBACK_REQUIRED`).
- Feed change needed: add `custom_label_0 = season` (`christmas_2026` and similar) and `custom_label_1 = margin tier` (A ≤ 42%, B 42–50%, C > 50% landed) in the feed builder, so Shopping, Pinterest and Meta can bid or exclude by margin.
  - This is a local code change plus Merchant/Pinterest/Meta product-set changes.
  - The Merchant/product-group part needs fresh approval.

## 4. Channel sequencing (ordered by priority, then gates)

Priority follows the owner's order where the gates allow. Microsoft is added because it is already live and spending, and because Bing was historically about 7% of revenue.

### P0: stop leaks and establish truth (blocks all scaling)

1. **Measurement validation** (§6). Nothing scales past L1 until it passes.
2. **Microsoft spend drift.** In the latest readbacks, six campaigns were Enabled at $20/day each. Their $0.20 caps exceed the retained $0.15 ceiling. Reported conversions are 0. Audience network took $20.24 of $28.04 (Sep 17–22). An exact six-campaign pause question and an Audience opt-out packet are pending. `REPO_KNOWN` (2026-09-21/26). Current state: `LIVE_READBACK_REQUIRED`.
3. **Merchant US feed.** It has returned 503 since 2026-09-23, and the Merchant fetch fails, so free listings and Shopping degrade. The rebuild is blocked on the missing `read_markets` scope. `REPO_KNOWN` (`PROB-2026-09-24-MERCHANT-US-FEED-STALE`).

### P1: Google free listings, then Standard Shopping; PMax is deferred

- **Free listings: $0 spend and the fastest recovery of the lost Google channel.**
  - Gates: fresh US feed (200, under 24 h); apparel attributes filled; Christmas products published to the Google & YouTube channel.
  - 1,023 of 4,741 US rows (21.6%, 111 products) have blank color, gender or age_group. `REPO_KNOWN` (2026-09-25 packet).
  - Merchant readback of the actual disapproval reasons: `LIVE_READBACK_REQUIRED`.
- **Standard Shopping (US first).** Manual CPC with a ceiling of ≤ $0.20 fits the owner's CPC control. Product groups come from custom labels, starting with the Christmas set and margin tier A.
  - Existing Standard Shopping `23802638621` and the V2 campaigns: `STALE_OR_SUPERSEDED` (May, old Merchant `124884876`). The live account and Merchant are `6509972886` / `513542500`.
  - Build a new paused campaign rather than revive the old one.
- **PMax** (`24247604341`, Paused, $5/day; `REPO_KNOWN` 2026-09-21) stays paused.
  - PMax has no per-click cap (`ASSUMPTION` about the current product, to verify), which conflicts with the owner's CPC control.
  - `VISION.md` already bars PMax before measurement, feed, assets and scope are ready.
  - Unlock: ≥ 30 validated Shopping purchases with Shopify-reconciled ROAS ≥ 6.5×, plus an explicit owner waiver of per-click control in exchange for a target-ROAS floor (`OWNER_DECISION`).

### P2: Google Search (US) and Microsoft Search/Shopping

- **Google Search.**
  - The replacement campaign draft (6 groups, 48 keywords, $20/day, $0.20 cap) resumes only after the owner's identity check.
  - Existing ads rate Poor for keyword relevance; the RSA-strength diagnostic is still gated.
  - Add a Christmas long-tail group (§8).
  - Keep exact/phrase match and ≤ $0.20, and follow the playbook's 24-hour zero-impression rule.
  - Bidding moves to Purchase-only Maximize Conversions, then to target ROAS, only after §6 passes and the lane has ≥ 15–30 purchases (`ASSUMPTION` from Google guidance; re-verify). A CPC cap is kept where the strategy allows one.
- **Microsoft.**
  - Make the account clean first (P0). Then use Microsoft as a cheap-CPC clone of validated Google Search groups and a Microsoft Shopping campaign from the same feed.
  - The Microsoft Merchant/store state is `LIVE_READBACK_REQUIRED`.
  - UET has one purchase receipt verified with limits. Value and transaction identity are unverified (`PROB-2026-09-06-MICROSOFT-PURCHASE-TRUTH`).
  - Localized EU/PL/IT builds stay paused until the US lane passes L1. Italian needs the pending country answer.

### P3: Meta Advantage+ catalog (the S3–S4 scale engine)

- Current state:
  - Page `942388912516328` and dataset/pixel `547553035448852` are qualified.
  - The Shopify F&I channel shows 257 approved.
  - The ad account, Commerce catalog binding and current event delivery are **unknown**.
  - Meta shows "Returns not accepted", while store policy is a conditional 30 days (`PROB-2026-09-06-META-ACCOUNT-QUALIFICATION`, `REPO_KNOWN` 2026-09-12).
- Gates:
  - Owner-confirmed ad account and business, with billing done by the owner.
  - Pixel + CAPI purchase acceptance (§6).
  - Catalog linked to the ad account.
  - Return policy corrected.
  - Buyer-QA cart pass.
- Structure:
  - Start with catalog retargeting (viewed/added, not purchased) at the L0 cap.
  - Then Advantage+ shopping prospecting with a minimum-ROAS bid control if the account offers it (`ASSUMPTION`, to verify). This is how the owner's cost control carries over, because a $0.20 CPC cap is not realistic on Meta.
- Creative: the ChatGPT lifestyle images that exist now, then short UGC-style video.

### P4: Pinterest catalog

- Current state:
  - Advertiser `549756244483`, campaign `626758581530` Paused.
  - The Phase 1 paused replacement is approval-ready (`PROB-2026-05-28-PINTEREST-PARENT-ZERO-ROAS`).
  - Tag and CAPI rate "Fair". CAPI product ID and click ID are 0%, and the catalog match rate is low (`PROB-2026-09-09-PINTEREST-MEASUREMENT-ACCEPTANCE`).
  - The organic baseline has 0 outbound clicks.
- Gates: event-quality repair (Phase 2) and a genuine purchase match before any spend.
- For Q4, Pinterest can be ready before Meta because its infrastructure is further along. In that case the gates decide, not this order.

### P5: TikTok

- There is no ad account, pixel or catalog evidence. Products are published to the Shopify TikTok channel (`REPO_KNOWN`, June).
- Gates:
  - Meta has passed L2, which proves creative and catalog economics.
  - The owner creates the account.
  - The pixel and Events API are installed through the Shopify TikTok channel.
  - Video creative is supplied.
- Expected to fit small baskets; keep the stricter kill line.

## 5. Budget ramp rules (gated on measured ROAS, not the calendar)

Windows are counted in purchases, not days. Every step also needs current authority (§0), fresh before/after readback and reviewer PASS.

| Level | Budget rule | Enter when | Leave up when | Leave down when |
|---|---|---|---|---|
| L0 Learn | ≤ $5/day per new campaign (existing rule); total within the owner-approved cap | Channel gates in §4 and §6 pass | ≥ 3 Shopify-reconciled purchases and ROAS ≥ kill line | No add-to-cart or checkout signal after spend ≈ 0.5 × target CPA → narrow or hold. No purchase after spend ≈ 1× target CPA → pause/narrow/reroute (existing thresholds, with target CPA = AOV ÷ 6.5, e.g. $10.15 at $66 and $23 at $150) |
| L1 Prove | Hold the budget; optimize queries, negatives, products and creative | L0 exit | Trailing window of ≥ 10 purchases at ≥ the scale gate (§3b) | Trailing ≥ 10-purchase ROAS < kill line → back to L0 or pause |
| L2 Scale | Raise +20–30% per step. After a step, no further raise until ≥ 10 new purchases accrue after it | L1 exit | Each step re-tested on its own post-step window | Post-step ROAS < scale gate → revert the step. < kill line → cut 50%. Two failed steps → hold at the last good level |
| L3 Automate | Target-ROAS / value bidding; PMax or Advantage+ prospecting | ≥ 30 validated purchases in the lane, values reconciled to Shopify within ±10%, owner waiver where CPC control is dropped | Same step rule | Same |

**Cross-channel rules**
- The next dollar goes to the lane with the highest marginal Shopify-reconciled ROAS above its scale gate.
- Blended MER (total revenue ÷ total ad spend) must stay ≥ 6.5×. If blended net falls below 35% for a trailing window of ≥ 30 orders, freeze all raises.
- Total spend never exceeds the owner-approved daily cap. The cap needed for S4 is about $245/day on average, with Q4 peaks higher. The current file cap is $80/day, and raising it is an owner approval.
- Zero impressions 24 hours after enabling → same-day serving diagnosis (playbook rule).
- Any measurement break (conversion tag down, value mismatch > 10%, feed 503) → freeze raises in affected lanes until it is fixed.

## 6. Measurement prerequisites still missing

| # | Prerequisite | State | Label |
|---|---|---|---|
| M1 | Google Ads Purchase `7760272273`: genuine purchase received with correct value, currency and transaction ID, no duplicates; Purchase is the only primary goal | "Awaiting conversions"; last ping Sep 22; Enhanced Conversions not configured | `REPO_KNOWN` (2026-09-23), `LIVE_READBACK_REQUIRED` |
| M2 | GA4 `330266838` ↔ Shopify purchase parity (±5–10%) | 1 order matched ($111.96, Sep 13). Parity is ACTIVE_SOLVING, and client-ID truncation is open | `REPO_KNOWN` |
| M3 | Non-USD purchase values (EUR/GBP/AUD/CAD), now more important after the Markets price lists | `PROB-2026-05-10-NON-US-PURCHASE-CURRENCY-MEASUREMENT` open | `REPO_KNOWN` |
| M4 | Consent: preferences control live, and consent mode behavior verified for EEA/UK | Fix was built in a theme preview; live state since then is unknown | `LIVE_READBACK_REQUIRED` |
| M5 | Microsoft UET purchase value, transaction ID and goal acceptance | 1 receipt verified with limits | `REPO_KNOWN` |
| M6 | Pinterest tag + CAPI purchase match (product ID, click ID, deduplication) | Fair; CAPI product ID and click ID 0% | `REPO_KNOWN` |
| M7 | Meta pixel/CAPI purchase delivery and deduplication | Unknown | `LIVE_READBACK_REQUIRED` |
| M8 | TikTok pixel/Events API | None | `REPO_KNOWN` (absent) |
| M9 | Shopify-reconciled channel ROAS: daily join of spend with UTM/click ID and Shopify orders. Some orders have no first/last visit | Not built | `REPO_KNOWN` |
| M10 | Decision-grade CVR with spike-day and bot exclusion. `qualified_shopper_conversion.py` does not enforce date exclusions | Open | `REPO_KNOWN` |
| M11 | Per-order landed cost fed back to reporting (contribution-ROAS by basket/product), plus a new-vs-returning flag | Not built; the BuckyDrop study is a one-off | `REPO_KNOWN` |
| M12 | Christmas products emit color/gender/age_group in the feed. Their options are Role/Size and they carry several taxonomy color values, and the generator uses a taxonomy color only when exactly one is set | Likely blank color | `ASSUMPTION` from `generator.js` logic and the specs; verify in the candidate feed |

- **A single validation event covers M1/M2/M5/M6/M7:** one real desktop order, placed and refunded by the owner (existing next action `OWNER_DESKTOP_PAID_TEST_ORDER_2026_09`), then read on every receiver.
- Gate to leave L0: M1, M2, M9 and M10 pass for Google; the channel's own row passes for the others.

## 7. Exact owner actions that unblock each channel

Ordered by how much each unblocks.

| # | Owner action | Unblocks | Why it comes here |
|---|---|---|---|
| O1 | Add the `read_markets` scope to the Shopify Dev Dashboard app, reinstall it, run `refresh_shopify_admin_token.py`, then say "go" for the US feed prepare → build → review → promote run | Free listings, Shopping, Microsoft Shopping, Pinterest/Meta feed freshness | Google was 42% of peak revenue. Free listings cost $0, and the feed has been 503 since Sep 23 |
| O2 | Choose durable feed automation: Cloudflare cron with the Shopify secret, or a Mac LaunchAgent | Stops the 48-hour guard from silently lapsing again | Same |
| O3 | Complete Google's "Confirm it's you" check in the preserved Chrome DLM activation tab (Ads `6509972886`) | Google Search replacement and any Google Ads save | Every Google Ads write currently fails to save |
| O4 | Place one real desktop order, then refund it | M1/M2/M5/M6/M7 in one event | It is the only way to validate purchase value and deduplication |
| O5 | Approve Shopify writes setting Google color/gender/age_group on the 111 affected products and on the 11 Christmas products | About 21.6% of US rows become eligible | Disapproved rows cannot serve on free listings or Shopping |
| O6 | Activate the 11 Christmas 2026 drafts (4 images each, inventory set, published to Online Store + Google & YouTube + Facebook & Instagram + Pinterest + Microsoft channels) | The whole Q4 plan (§8) | Highest-margin, largest baskets, and time-boxed |
| O7 | Confirm the US Christmas order-by date: does the 12–16-day window include the supplier's "ships in 7 days"? | Ad copy cutoff and pause date | See §8c |
| O8 | Sign in to Microsoft Advertising, answer the pending six-campaign pause question, approve or amend the Audience opt-out packet, and set a numeric Microsoft budget/loss cap | Stops unmeasured spend; Microsoft L0 | This is money leaving now with 0 measured sales |
| O9 | Set a new policy: total daily cap and the ROAS gates in §3b and §5 (update `spend_authorization.md`) | Any ramp beyond L0 | The current $80/day cap and NONE control cannot fund S2+ |
| O10 | Pinterest: approve the Phase 1 paused replacement (existing packet) | Pinterest L0 after M6 | The packet already exists |
| O11 | Meta: confirm the ad account and business, add billing (owner only), connect the F&I catalog to the ad account, fix the "Returns not accepted" setting, answer the pending two-item cart QA question | Meta L0 | This is the scale engine for S3–S4 |
| O12 | Decide whether the CPC cap stays absolute or becomes a ROAS floor plus daily cap for automated lanes | PMax, Advantage+, target ROAS (L3) | Automated lanes cannot honor a per-click cap |
| O13 | TikTok: create the ad account/Business Center (account creation is owner-only) and install the pixel through the Shopify TikTok channel | TikTok L0 | Last, after Meta L2 |
| O14 | AOV and margin decisions already pending: free shipping over $69 with a fee below it, or the price floor; reprice or re-source the Mommy & Me pajama line | Raises RPC for every channel (§2d) | These unlock more paid growth than any bid change |

## 8. Q4 Christmas 2026 plan

### 8a. The 11 designs

- Reconciliation: 24 drafts were created. 13 were archived as non-2026 releases (`tools/run_logs/archived_non2026.json`), which leaves 11. `REPO_KNOWN`.
- The 11 designs:
  - classic-red-plaid
  - evergreen-fair-isle
  - jolly-crew
  - joyful-merry-blessed
  - let-it-snow
  - lights-out-reindeer
  - plaid-reindeer
  - plaid-tree-trio
  - snowy-village-stripes
  - we-are-family-evergreen
  - we-are-family-red
  - All use the handle suffix `-family-matching-pajamas`.
- AI-image status (snapshot from 2026-09-27 00:23 local):
  - 4 had 4 images attached (classic-red-plaid, evergreen-fair-isle, jolly-crew, joyful-merry-blessed).
  - 3 were generating (let-it-snow, plaid-tree-trio, we-are-family-red).
  - 4 had not started.
  - `REPO_KNOWN`. Current Shopify status is `LIVE_READBACK_REQUIRED`.
- Economics: $35.99 / $32.99 per piece. Landed about 31–40%. Family orders of 4–7 pieces put AOV around $140–240 (`MODEL`). Break-even ROAS is about 1.6–1.9×.

### 8b. Campaigns to prepare now

Everything below is built locally or saved paused. Each live save needs its listed gate and approval.

| # | Build | Gate before enabling |
|---|---|---|
| X1 | **Feed readiness for the 11:** item_group_id, color/gender/age_group per variant role, `custom_label_0=christmas_2026`, margin tier A. Verify in the candidate TSV before promotion | O1, O5, O6 |
| X2 | **Free listings:** automatic once X1 is promoted and Merchant approves | Merchant readback shows "showing on Google" for the 11 |
| X3 | **Google Standard Shopping `DLM \| GADS \| US \| EN \| Shopping \| XMAS26`** (paused): product group = `christmas_2026`, manual CPC starting at $0.12–0.15 with a $0.20 ceiling, L0 $5/day, Shopping priority High over any evergreen Shopping campaign | O3, O4 (M1 passes), X2, current authority |
| X4 | **Google Search Christmas ad group** in the US Search campaign: exact/phrase long-tail. Candidates to check against the Keyword Planner at a $0.20 ceiling: matching family christmas pajamas, family christmas pajamas set, christmas pajamas for the whole family, plaid family christmas pajamas, fair isle family pajamas, reindeer family pajamas, matching christmas pajamas for family of 4. Head terms above $0.20 are rejected, not bid up. Landing is the PDP or `christmas-pajamas` once it has live products. Anti-cannibalization: Search owns named queries, Shopping owns product discovery | O3, O6, M1, keyword `GREEN` rows |
| X5 | **Microsoft clone** of X3/X4 | O8, M5, X3/X4 at L1 |
| X6 | **Pinterest:** Christmas product group in the catalog. Organic Christmas Pins once products are live, within the 3-Pins-per-168-hours rule. Paid catalog only after O10 and M6 | M6 and O10 |
| X7 | **Meta Advantage+ catalog, Christmas product set.** Retargeting first | O11, M7. If Meta gates are not met while there is still time to ship for Christmas, skip paid Meta this season and use organic |
| X8 | **Brand-safety exceptions:** Grinch, Disney, Stitch and "Rudolph" as exact negatives across Christmas lanes. The catalog deliberately excludes that intellectual property; this is a reviewer-checked routing rule, not a guessed waste list. All other negatives come from search-term evidence | Reviewer PASS |
| X9 | **Copy rules:** no stock, warehouse or "ships today" claims (dropshipping). Delivery stated as the 12–16-day window or the dated range on the PDP. The "Order by <date> for Christmas" line only after O7 | O7 |

### 8c. Last safe US order date

Sources disagree:

| Source | Date | Basis |
|---|---|---|
| Christmas packet / storefront | Dec 8 | The 12–16-day window only. It may exclude dispatch |
| Profit study (parent's figure) | **about Dec 5** | About 4 days dispatch + 12–16 days Registered Air Mail |
| Conservative | Dec 1 | The supplier (smr) states "ships in 7 days", + 16 days transit. Actual carrier transit was 9.3–12.6 days (n=3) |

- Plan: use **Dec 5** as the working US cutoff, per the parent.
  - Christmas-delivery claims and the Christmas-only campaigns (X3/X4/X5/X7) are paused or re-messaged at the confirmed cutoff.
  - Until O7 is answered, copy avoids a specific order-by date.
- International cutoffs are earlier. EU and AU ship by air cargo, whose transit times are not in evidence (`LIVE_READBACK_REQUIRED`).
- Do not rescue late orders with UPS, Air Express or EMS: December 2024 rush shipments ran 67–87% landed.
- After the cutoff, the gift card (archived; republishing is an owner decision) is the only honest Christmas-gift offer.
- Ramp in season: the §5 rules apply unchanged. Windows are counted in purchases, and the short season is the reason to have X1–X4 saved paused before activation, so L0 can start the moment the gates pass.

## 9. Risks and contradictions (fail closed until reconciled)

- `spend_authorization.md` `APPROVED_ACTIVE` vs control `NONE` → NONE governs.
- Microsoft campaigns may be spending with $0.20 caps above the retained $0.15 ceiling and no validated purchases.
- The owner's $0.20 CPC control is not compatible with automated bidding (PMax, Advantage+, target ROAS). O12 decides this.
- The 650% target at today's 48% landed gives 29% net, below the 35% floor. Scaling at 650% is only 35%-net-safe for tier-A margin products (≤ 42% landed) or larger baskets.
- The price raises may lower CVR. Measure CVR and AOV again after the raise, with spike days excluded, before using the §2 targets.
- The 12–16-day delivery window caps CVR at scale. A US 3PL is a later step (profit study, Stage 3), and it becomes an honest customer claim only once real stock exists there.

## 10. Next

- **One owner action first: O1**, adding `read_markets` and approving the US feed run.
  - It restores Google free listings at $0 spend. Google is the channel that produced 42% of peak revenue.
  - It is a prerequisite for Shopping, Microsoft Shopping and the Christmas catalog lanes.
  - It does not depend on the identity check or any spend approval.
- Internal queue, in disjoint lanes:
  1. Add season and margin custom labels to the feed builder locally, with tests, and confirm the 11 Christmas products emit color/gender/age_group (M12).
  2. Build X3/X4 as a local payload with Keyword Planner feasibility rows ready for the paused save after O3.
  3. Recompute decision-grade qualified CVR and RPC with the spike-day exclusion (M10), so the §2d gate starts from a true baseline.
