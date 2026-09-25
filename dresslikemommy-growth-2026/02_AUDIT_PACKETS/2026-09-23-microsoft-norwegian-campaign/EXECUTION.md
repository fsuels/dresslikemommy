# Norwegian Microsoft Search preparation

Status: PARTIAL_LOCAL_PREPARATION; native build NOT RUN pending country clarification.

Owner: task `01a0d0ef-bf6e-7760-87dc-b3f4a023f3ea`. Account `477439`, customer `770182`. Root controls only its assigned Codex IAB browser 2, original tab 1. No Microsoft Ads Save, Copy, Paste, Enable, Delete, budget, bid, tracking or peer-campaign mutation has been submitted in this task.

## Exact scope and unresolved decision

The user requests a Norwegian Bokmål copy of `DLM | MS | US | EN | Search | 202609`, preserving images and source structure while localizing ads, keywords, campaign and group negatives, destinations and text assets. The user wrote `NB | NB`, whereas the pasted brief explicitly specifies United States and `US | NB`. Country is unresolved; question sent for Norway (`NO | NB`) versus United States (`US | NB`). Do not infer an answer. Keep the new campaign paused as the supplied build instructions specify; activation is separate.

An initial question also asked whether the existing paused English `#2` copy was intended. This branch is now superseded by authoritative owner coordination: **campaign `506256099` belongs exclusively to the active Polish build**, task `01a0cf40-b64f-7421-94b3-6c53b9032625`. Its owner confirms it is now named `DLM | MS | PL | PL | Search | 202609`, Paused, Polish/Poland presence, USD10/day, MaxClicks0.20. Do not repurpose it. Create a separate Norwegian copy only after country is resolved and a fresh inventory excludes a duplicate.

## Native source readback — September 23 EDT / September 24 UTC

Assigned tab authenticated to Microsoft Advertising. Initial campaign inventory contained 12 campaigns; source `506254907` Enabled, USD10/day, Auto: Max Clicks; no Norwegian-named target. Seven enabled source groups: Family Matching Shirts `1260042129652944`; Father & Son Shirts `1262241153333250`; Mommy & Me Swimsuits `1269937734374761`; Mommy & Me Pajamas `1271037246253962`; Mommy & Me Dresses `1272136755587035`; Family Matching Sweaters `1274335781733965`; Family Matching Outfits `1275435291895118`. Brief explicitly adds the eighth mother/daughter outfits group.

Source settings freshly read: English; Maximize Clicks; checked maximum CPC USD0.20; individual budget USD10.00/day; United States; People in your targeted locations selected. Campaign tracking template, final URL suffix and custom parameter fields blank. Account/group/ad tracking inheritance was NOT RUN. Account-default purchase goal displayed No recent conversions; this is not purchase ingestion/attribution verification.

Only sections were expanded, without editing fields. Clicking Cancel unexpectedly produced an unsaved-changes warning. Root clicked No; screenshot confirmed the dialog closed and source editor remained. No Save or discard was accepted. Preserve original tab at source settings; for subsequent work use a clean task-owned Microsoft tab after explaining this limitation, rather than save/discard that editor. This matches a previously recorded Microsoft UI symptom but its cause remains UNKNOWN.

## Norwegian destinations

At 2026-09-24 01:09:12–01:09:21 UTC all eight supplied `/no/collections/` routes rendered localized H1s and product headings: family-tops, dresses, new-women-outfits, pajamas, daddy-me-shirts, mommy-and-me, swimsuits, family-sweaters. The session retained Germany/EUR and Norsk; no country/currency/cart/privacy setting was changed. This proves route availability only, not Norwegian-market inventory, shipping or checkout. The temporary storefront tab was closed.

Remaining visible issues include `seksjoner.annonser.standard_promo`, `Innen Family Matching`, `Most relevant`, and English product image alt text. These are storefront findings, outside the current Ads localization write scope. Full checkout, responsive purchase journey and simultaneous parent/child availability were NOT RUN.

## Build and verification plan

Payload source is the user attachment; see `payload/campaign_payload.json` and `payload/validation.json`. Preserve all conditional Exact group negatives and supplied supplemental English campaign negatives for mixed-language searches. Advertised 160 image-caption pairs are absent from the pasted attachment; translate actual copied image text only after native image/caption readback, preserving images/crops and shared source assets. Do not fabricate the missing attachment.

Decision options: create a separate paused source copy after country answer; hold; or repurpose an existing copy. The third is rejected because the observed copy is Polish-owned. Intended outcome is eight Norwegian groups/RSAs with supplied exact tuples, source images and matching monetary/settings baseline. Success requires saved native settings and all fields plus complete positive/campaign-negative/group-negative exports, zero missing or unintended tuples. Kill conditions: unresolved country, wrong campaign, peer claim, interactive policy/authentication gate, or irreversible cleanup without action-time confirmation. Smallest rollback is retain new target paused and correct its scoped values; no source/peer deletion. No additional spend or activation is authorized.

Next action: obtain Norway versus United States answer, then fresh inventory and the authorized paused build. Canonical continuation is `ops/prompts/paid-growth-ai-army-continuation-prompt.md` with this packet and the actual answer; do not repeat resolved authorization.

## Local validation result

Eight groups, 144 positives (62 Exact/82 Phrase), 120 headlines, 32 descriptions, 233 campaign negatives (222 Phrase/11 Exact) and all 54 group negatives (30 Exact/24 Phrase). Group negative counts in brief order are 8/8/9/0/10/13/0/6. Eight sitelinks, 32 associations, six callouts and eight snippets prepared. Builder reports 222 successful text-length checks, no duplicate tuples or literal positive/negative conflicts. Independent reviewer separately compared the complete attachment and all paste files with the payload and confirmed these counts and exact content. Review is local only; Microsoft semantic matching, editorial approval and saved native target are not verified. See `review/PREFLIGHT.md` for the independently authored limits.

The coordination message to the Polish task was sent under the `coordinate-multi-agent-work` skill to establish disjoint campaign ownership. Its response excludes `506256099` from this task. Canonical append interval has been requested from that active peer before touching shared files; no concurrent writer or claim takeover is intended.

## Closeout checks

Independent preflight PASS_WITH_GATES. Cockpit render and integration audit passed (25/25, zero risks); strict continuity returned CONTINUITY_OK. Initial scoped diff check found one added blank line at worklog EOF; that formatting issue was corrected before final recheck. The Polish-confirmed shared interval is released after final checks. No native Norwegian campaign has been created; country answer remains required. Canonical records updated: own coordination claim, problem entry, worklog anchor and cockpit section; generated cockpit/integration report refreshed. No global authority changes.

## Resumption — corrected Norwegian/Norsk instruction

User first replied Poland/Polish, then explicitly corrected: “in that case you need to do Norwegian with language norsk with the instructions I gave you!” Root applies original language/country correspondence as Norway/Norwegian Bokmål, exact name DLM | MS | NO | NB | Search | 202609, and announced that interpretation before execution. Separate new paused source copy with unchanged USD10/day MaxClicks0.20 baseline; Polish506256099 excluded. Earlier country-pending status is superseded for this bounded build. Original source editor remains untouched; clean same-task IAB tab3 now owns new copy operations. Native targetID pending first save.
