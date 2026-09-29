# Autosource runbook — unattended product sourcing (scheduled task `autosource`)

Owner, 2026-09-29: "I need you to constantly get me new products for all categories. Expand my offerings!" and "this needs to run continuously without me having to babysit … 24 hours a day". This scheduled job runs every hour. Each run does ONE sourcing round, builds every product that passes every rule, and records the results. This file is the run's memory: rules, steps, and formats. Canonical rules win over this file: the "Owner product rules" at the top of `ops/sourcing/CONTINUOUS-EXPANSION-WORKFLOW.md`.

## Command rules (unattended: anything else stalls or is refused)

- The ONLY shell command shape is `/usr/bin/python3 ops/sourcing/autosource.py <subcommand> …`, run from the repo root. Never use cd, &&, pipes, redirection, other scripts, ls/cat/grep, `python3 -c`, git, or curl.
- Read files and images with the Read tool, and search with Grep/Glob.
- Write only these files, with the Write tool:
  - `/tmp/autosource/recipe_<handle>.json`
  - `/tmp/autosource/worklog_append.md`
  - `/tmp/autosource/suppliers_append.md`
- Never edit repo files directly; `autosource.py commit` copies and appends them.
- Messaging: SendMessage to the "Website sales improvement" session (if listed) with new live handles. Nothing else.

## Hard rules (every product; fail any, skip it)

1. **Category:** Mommy & Me, family matching, Daddy & Me, siblings, couples, maternity, or matching family accessories.
   - No pets.
   - No kids' pajamas/sleepwear: the kids' sleepwear flammability hold (packet #14) is still open.
2. **Fresh and in season:** offer created in 2026, AND the release attribute says 2026 plus Autumn/Fall/Winter (秋/冬). "Spring 2026", a year only, or "Other" fails.
3. **Shipping (ALWAYS):** the offer promises 24h/48h dispatch (`deliveryLimit` 1 or 2 / "48-Hour Shipping" / 承诺48小时发货). 3-, 7- or 15-day promises fail.
4. **Supplier:** `gate` prints the verdict.
   - Standard: ≥5 years on 1688, 48h pickup ≥95%, fulfillment ≥97%, service ≥4.0, MOQ 1.
   - 3–4 years only with strict stats: pickup ≥97%, fulfillment ≥97%, quality returns ≤1%, disputes ≈0, service ≥4.0, 500+ orders in 30 days.
5. **No IP or logos:**
   - No licensed characters or look-alikes: Disney/Mickey, Sanrio, Snoopy, Pooh, Chiikawa, Grinch, Stitch, superheroes.
   - No Rudolph-style red-nosed reindeer.
   - No brand parodies (PRADA/"PADA", Polo pony, NY caps).
   - No "SMILE"/smiley-face prints (Smiley® mark).
   - No national/patriotic or Chinese-New-Year themes (off-market).
   - No garbled or odd lettering.
6. **No duplicates:** compare the vendor photos with our live and archived store products of the same type (Grep specs and `ops/sourcing/TRUSTED-SUPPLIERS.md`). A near-identical print on a different garment counts as a duplicate.
7. **Appeal:** skip tiny or generic chest logos on template photo sets, school/kindergarten activity uniforms, and summer-themed text on winter items.
8. **Real fabric:** state the real fabric % honestly.
9. **Price:** landed ≤50% of price (the engine formula does this); compare-at = price + $10.

## Steps of one run

0. **Lock:** `autosource.py lock acquire`. If it prints LOCKED, stop immediately. Always `lock release` at the end, even after errors.
1. **Pick the category:** `autosource.py next` prints this round's category and the exact command to run (search or catalog). Run it.
2. **Screen:** `autosource.py scan <IDS>`, using the IDS line from step 1; it paces itself.
3. **Supplier check:** `autosource.py gate <ids that printed PASS>`. Keep the gate PASS ones.
4. **Look before building:** for each survivor, run `autosource.py capture <id>` and open `/tmp/autosource/sheet_<id>.jpg` with Read.
   - Judge rules 5–7 and duplicates.
   - Find the size-chart image and read it at full size (Read the file in `ops/sourcing/vendor-images/<id>/desc/`).
   - If it passes, run `autosource.py skus <id>`.
5. **Build one product at a time.** Write `/tmp/autosource/recipe_<handle>.json` (schema below), then run:
   1. `spec <recipe>`
   2. `build <handle>`
   3. `translate <handle>`
   4. `images <handle>` (about 10 minutes)
   5. `review <handle>`
6. **QA the photos:** Read `/tmp/autosource/<handle>_review.jpg`.
   - Reject if the print, lettering or colours differ from the vendor garment, any logo or extra text appears, the image isn't 9:16, it looks fake, or the kids and adults wear the wrong prints.
   - If rejected, do not finish. Record it for the CEO session, leave the product DRAFT, and move on.
7. **Go live:** `autosource.py finish <handle>`. It must print a `[listing-localization] PASS` line and a `LIVE …` readback. If the closeout fails, leave the product DRAFT and record it.
8. **Record:** write `/tmp/autosource/worklog_append.md` using the anchor format below, then run `autosource.py commit "Autosource: <n> new listings (<category>)"`.
   - Optionally also write `/tmp/autosource/suppliers_append.md` (dated supplier readings), so they are appended to TRUSTED-SUPPLIERS.md.
9. **Notify:** SendMessage the website session with each new live handle, its category and price, so it can place them.
10. **Release:** `autosource.py lock release`.

## Stop conditions

- Exit code 3 / "BLOCKED" (CAPTCHA or login): stop 1688 work for this run. Record `BLOCKED_1688_CAPTCHA` in the worklog append and release the lock. Never bypass it.
- Stop on any money, billing, customer-messaging, login or permission prompt.
- Never move money. Never change settings or other products.
- If a step fails twice, skip that product. Record why.

## Recipe schema (`/tmp/autosource/recipe_<handle>.json`)

```json
{
 "offer_id": "1081053551587", "handle": "hooray-sun-family-matching-sweatshirts", "shortcode": "HRSN",
 "print_name": "Hooray Sun", "title_variant": "everyday",
 "garment": "sweater (only for knits; omit for sweatshirts)", "knit_role": "mommy|daddy (only for 2-person knit pairs; omit otherwise)",
 "chart_no_sleeve": false,
 "colors": [{"name": "Cream", "token": "CRM", "vendor_value": "<exact SKU colour value from skus output>"}],
 "color_pattern_ids": ["69641928801"], "color_pattern_labels": ["Beige"],
 "sizes": {
   "Child 100": {"vendor_size": "<exact SKU size value>", "chart_label": "100 (90-100 cm)", "picker": "Child 2-3 Years", "suffix": "KID23Y", "age": "2-3",
                 "length": 40, "chest": 70, "sleeve": 30, "height": "90-100", "weight": "12.5-15"},
   "Adult M": {"vendor_size": "M", "chart_label": "Adult M", "picker": "Adult M", "suffix": "M", "age": "—", "length": 63, "chest": 96, "sleeve": 53, "height": "155-165", "weight": "42.5-47.5"}
 },
 "chart_image": "04.jpg", "hero_image": "00.jpg", "ai_refs": ["00.jpg", "05.jpg"],
 "fabric_key": "cotton_sweat", "design_key": "crew_sweatshirt",
 "print_sentence": "…", "feature_label": "…:", "feature_text": "…", "extra_tags": ["…"], "media_alt": "…",
 "chart_note": "the offer's own size chart (description image 04) …", "vendor_title": "…",
 "evidence_lines": ["Supplier: …, N years on 1688, 48h pickup …%, …", "Owner 24-48h rule: …", "Fresh gate: release …", "Fabric evidence: …"],
 "child_grams": 250, "adult_grams": 450
}
```

Recipe notes:

- **Size keys:** use "Child <vendor cm>" and "Adult <size>" (the engine infers the audience from the prefix). Pick picker labels the engine knows:
  - Child 6-12 Months, 1-2, 2-3, 4, 5-6, 6-7, 7-8, 9-10, 11-12, 13-14 Years.
  - Adult S–4XL.
  - Skip sizes the store can't represent: 5XL, baby rompers.
  - Height→age examples: 80 cm → 6-12 Months, 90 → 1-2, 100 → 2-3, 110 → 4, 120 → 5-6, 130 → 6-7 or 7-8, 140 → 9-10, 150 → 11-12, 160 → 13-14.
- **Chest:** full chest (胸围) as published; 半胸围 ×2. Weights: 斤 ÷ 2 = kg.
- **Sleeve:** if the chart has no sleeve column (only 肩宽 shoulder), set `"chart_no_sleeve": true` and omit sleeve.
- **Colour-pattern metaobject ids:** Red 69600804961, Green 70220546145, White 69639733345, Beige 69641928801, Blue 69639766113, Pink 69963645025, Purple 130284126305, Yellow 69622104161, Black 69943132257, Gray 69944672353.
- **Codes and names:** the shortcode must be 4 unused capital letters. The handle and print name must not repeat an existing product name.
- **fabric_key:** cotton_sweat (cotton), cotton_blend_sweat (cotton/polyester), modal_knit (modal/viscose knit). design_key: crew_sweatshirt, crew_knit, collar_knit, cardigan_knit.
- **What can be automated:** family sweatshirts and sweaters, and Mommy & Me / Daddy & Me knit pairs (`knit_role`).
  - Siblings-only (kids-only), couples-only (adults-only) and maternity have no engine mode yet. Shortlist them in `suppliers_append.md` with offer id, supplier stats and why they pass. The CEO session builds them.

## Worklog append format (`/tmp/autosource/worklog_append.md`)

```
## AGENT_CONTINUITY_ANCHOR: <UTC date>-autosource-<category-slug>

- task_entities: <handles / offer ids>
- task_stage: LIVE_VERIFIED | NO_QUALIFIER | BLOCKED_1688_CAPTCHA
- next_action_id: NEXT_AUTOSOURCE_ROUND

- Category searched, number screened/passed, each new live handle with price and readback line, skipped candidates with the rule they failed, supplier near-misses.
```

## Final message of the run

Short summary: category, screened/passed counts, new LIVE handles, skipped reasons, and anything BLOCKED.
