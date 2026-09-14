# Dress Like Mommy Vision

Purpose: this file is the product and business compass for AI-assisted work in this repository. It is not an operating manual. Use `AGENTS.md` and the loop docs for how to work; use this file for what the work should protect and improve.

## Evidence Basis

- Repo evidence: the Shopify theme, homepage, and templates describe a store for mommy-and-me, daddy-and-me, family matching, vacation, pajama, swimwear, and photo-day outfits.
- Repo evidence: `ops/GROWTH_NORTH_STAR.md` defines the current paid-growth goal as profitable Google Ads and Pinterest growth at about `650% ROAS`.
- Repo evidence: `AGENTS.md` and listing prompts define hard safety rules around dropshipping honesty, vendor/source URL hygiene, draft-first listings, localization, feed grouping, and approval-gated external writes.
- Memory/context: prior continuity emphasizes one best next action, approval-gated Pinterest phases, and sales-moving work instead of circular monitoring.
- Inference: the durable product direction is a trustworthy, conversion-ready international Shopify store for coordinated family outfits, supported by operator-side AI workflows and measured paid growth.

## Purpose

Dress Like Mommy helps families buy coordinated outfits for moments they want to remember: vacations, family photos, birthdays, holidays, beach days, pajamas, swimwear, and everyday matching looks. The store should make it easy to understand who each piece is for, what size to choose, when it can arrive, and why checkout is safe.

## Target Users

- Parents and gift buyers shopping for matching family looks.
- Mothers shopping for mommy-and-me outfits.
- Fathers or families shopping for daddy-and-me or father-inclusive matching looks.
- International shoppers when the language, currency, shipping, and checkout path are ready.
- The owner/operator using local AI workflows to create listings, improve paid growth, and protect catalog quality.

Open question: which persona should be treated as primary in future brand copy and homepage decisions: US moms, international families, occasion shoppers, vacation shoppers, or another segment?

## User Jobs To Be Done

- Find a matching look by relationship, occasion, garment, color, or season.
- Choose the right piece and size for each family member without confusion.
- Understand shipping, returns, pricing, and per-piece or set behavior before checkout.
- Trust product photos, descriptions, size charts, and translated content.
- Move from ad or search intent to a clean landing page and purchase path.

## Business And Operational Objective

The business objective is profitable ecommerce growth, not traffic for its own sake. Paid-growth work should move toward as many profitable conversions as possible at about `650% ROAS`, while protecting customer trust, catalog quality, measurement accuracy, and channel eligibility.

Operationally, the repo should support fast, evidence-based execution: local or draft work first, exact approval for live-risk changes, fresh readbacks after external writes, and continuity notes that prevent agents from repeating solved work.

## Product Principles

- Be honest about the model: Dress Like Mommy is a dropshipping business with no physical store and no owned physical inventory.
- Never imply guaranteed local stock, a retail location, a warehouse, or on-hand inventory unless verified by owner-approved evidence.
- Treat size charts as product truth. Do not create variants or measurement claims not supported by source evidence.
- Keep vendor/source URLs and supplier names out of customer-visible and feed-visible data.
- Prefer fewer, clearer choices over dense or confusing product surfaces.
- Make every paid-traffic landing page worthy of real shoppers before sending traffic.

## UX Principles

- Mobile PDPs, collection pages, cart, and localization flows are revenue-critical.
- Above-the-fold product pages should clarify the product, price, selected audience/piece/size, shipping confidence, and next action.
- Matching-set products must make it obvious whether the shopper is adding one piece or multiple coordinated pieces.
- Collection and homepage navigation should map to shopper intent: relationship, occasion, garment, season, and use case.
- International routes must not mix stale language, wrong currency, source leakage, or unsupported shipping claims.
- Accessibility basics are product quality: labels, focus states, alt text, contrast, keyboard behavior, and no hidden scroll traps.

## AI And Automation Principles

- AI tooling is operator-side by default. Do not add a live storefront AI surface unless the owner explicitly asks for that product direction.
- Agents should create drafts, local packets, validation reports, and approval-ready artifacts before live-risk writes.
- Agents should act on clear safe fixes, but must stop for approvals, credentials, billing, payment, destructive actions, and external write gates.
- Automation should reduce repeated manual risk: feed checks, variant validation, localization audits, source-leak scans, readbacks, and continuity updates.
- Stale repo evidence is not current live proof. Treat it as a lead until refreshed.

## Measurable Progress

Progress means one of:

- A verified customer-facing improvement to storefront, PDP, cart, localization, tracking, or catalog quality.
- A verified feed, listing, or translation repair with passing guards.
- A paid-growth decision based on fresh enough evidence.
- A paused or draft artifact that is approval-ready and bounded.
- A blocker narrowed to an exact approval, credential, platform, or readback step.

Monitoring alone is not progress unless it produces a fix, bounded action, approval packet, reroute, or evidence-backed hold.

## Success Metrics

- Paid-growth purchases, revenue, CPA, and ROAS.
- Conversion tracking parity against Shopify order truth where applicable.
- Product/feed eligibility for intended paid cohorts.
- Clean feed grouping for Pinterest and apparel attributes for Merchant Center.
- PDP/cart/mobile readbacks passing for affected flows.
- Localized size-chart coverage and variant-row mapping with zero unmatched variants.
- Source/vendor leak checks passing for new listings and paid surfaces.
- Fewer unresolved problem-tracker entries without exact next action.

## Non-Goals

- Do not optimize for cheap unqualified clicks.
- Do not enable PMax, broad remarketing, or broad automated spend before measurement, feed, asset, and product-scope readiness.
- Do not treat generated packets or audits as the end result when a safe next action exists.
- Do not publish Shopify products, feed changes, campaigns, conversion changes, discounts, or pixels without the required approval and readback plan.
- Do not create a second command layer that competes with `ops/marketing/`.
- Do not put vendor/source URLs into public store, sales-channel, feed-visible, prompt, or worklog data.

## Safety And Approval Boundaries

Current user instructions and task scope override standing repo authority. If a turn says audit-only or docs-only, no live external writes occur even if another file says bounded authority is active.

Fresh explicit approval is required for:

- Shopify product publication, status, price, discount, policy, page, translation, inventory, channel, or checkout changes.
- Paid-media spend, campaign status, budgets, bids, keywords, negatives, product groups, feed labels, conversion goals, or attribution settings.
- Merchant/Pinterest feed source, catalog, product-group, tag, CAPI, or sync changes.
- Billing, credentials, account permissions, payment, order, refund, or destructive filesystem/git/database actions.

Read-only checks, local artifacts, drafts, and paused/review-only packets are allowed when they follow the repo guides and do not leak secrets or source data.
