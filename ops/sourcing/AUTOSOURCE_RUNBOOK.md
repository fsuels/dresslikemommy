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

**Nonstop mode (owner 2026-09-29: "you need to work nonstop without me having to prompt you"):** one run works through as many categories as fit. After each category (steps 1–7), run `autosource.py elapsed`; while it says CONTINUE, go back to step 1 (`next`) for the next category. When it says STOP, or on a CAPTCHA, do steps 8–10 once, covering every category of this run. Build every product that passes; there is no per-run cap. Quality rules never relax to hit a count.


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
- **Engine path** (`spec` → `build` → `translate` → `images` → `review` → `finish`): family sweatshirts and sweaters, and Mommy & Me / Daddy & Me knit pairs (`knit_role`).
- **Standalone path** for what the engine can't model — **siblings (kids-only), couples (adults-only), maternity (women-only)**: write `/tmp/autosource/recipe_<handle>.json` in the standalone schema below, then `standalone <recipe>` → `images <handle>` → `review <handle>` (QA) → `standalone-finish <handle>`.

## Standalone recipe schema (siblings / couples / maternity)

```json
{
 "kind": "standalone", "audience": "kids|adults|women", "offer_id": "1060255226703", "handle": "teddy-bear-siblings-christmas-sweaters", "code": "SBTB",
 "print_name": "Teddy Bear Fair Isle",
 "title": "≤70 chars", "seo_title": "≤60 chars … | Dress Like Mommy", "seo_desc": "≤155 chars",
 "product_type": "Siblings Matching Sweaters | Couples Matching Sweatshirts | Maternity Sweaters",
 "category1": "Siblings | Couples | Maternity", "subcategory": "Sweaters", "subcategory2": "Christmas Sweaters", "style": "Crewneck Sweater", "type": "Knit Sweater",
 "google_gender": "unisex|female|male", "taxonomy_gid": "gid://shopify/TaxonomyCategory/aa-1-13-12",
 "color_pattern_ids": ["69641928801"], "fabric_ids": ["69622399073", "69622366305"],
 "colors": [{"name": "Cream", "token": "CRM", "vendor_value": "<exact SKU colour value>"}],
 "sizes": [{"label": "2T", "vendor_size": "<exact SKU size value>", "suffix": "2T", "age": "2", "height": 90, "weight": "-", "chest": 62, "sleeve": 34, "length": 39, "size_gid": "129972863073"}],
 "grams": 250, "lead": "one honest paragraph", "bullets": [["Matching look:", "…"], ["Fabric:", "…"], ["Sizes:", "…"], ["Care:", "Follow the care label sewn into each garment."]],
 "chart_garment": "Sweater", "closing": "Pair them with …",
 "tags": ["Siblings", "Brother and Sister", "Sweaters", "Christmas"],
 "ai_refs": ["04.jpg", "13.jpg", "10.jpg"],
 "image_prompt": "full Codex photoshoot prompt",
 "alts": ["alt for image1", "alt for image3", "alt for image5", "alt for image6"],
 "translation_note": "- '<print name>' is the print name; 'Siblings' means brother and sister matching outfits."
}
```

Standalone recipe notes:

- **product_type** must contain Sweaters, Sweatshirts, Tops, Dresses or Sets, so the product joins new-arrivals.
- **taxonomy_gid:** aa-1-13-12 for sweaters, aa-1-13-14 for sweatshirts.
- **image_prompt:** copy the structure of `uploads/teddy-bear-siblings-christmas-sweaters/ai/prompt.txt`: exact garment description, IMAGE 1/3/5/6 scenes, 9:16, no text or logos, PRODUCT LOCK, and who wears it.
- **Colours are optional.** If the offer has only one colour, omit `colors` and set `"vendor_color": "<value>"`.
- **Size-metaobject ids** are optional; give them for all sizes or none:
  - Kids: 2-3y 129972863073, 3-4y 129972895841, 4-5y 129972928609, 5-6y 129972961377, 6 129972994145, 8 129973026913, 10 129971552353, 12 129971650657.
  - Adults: S 129975255137, M 129975222369, L 129975189601, XL 129975287905, 2XL 129975156833, 3XL 139840421985, 4XL 139840716897.
- **Fabric ids:** Cotton 69622399073, Polyester 69622366305, Viscose/Modal 139931877473.

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
