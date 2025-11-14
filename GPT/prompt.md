## Prompt 1 – Update homepage hero copy in `templates/index.json`

You are an AI coding assistant working in the repo at `C:\dev\dresslikemommy`. The theme is Shopify Dawn‑based and `templates/index.json` is a minified JSON object. I need you to safely update the homepage hero copy without breaking the JSON.

**Goal**
- Update the `hero_family_fit_FvXq4J` section in `templates/index.json` to use new hero text that leans into “picture‑perfect family moments” while keeping the rest of the section and file untouched.

**File:** `templates/index.json`  
**Key:** `hero_family_fit_FvXq4J`

### What’s there now

In `templates/index.json` you will find a fragment like this (all on one line in the actual file):

```json
"hero_family_fit_FvXq4J":{"type":"hero-family-fit","settings":{"eyebrow":"Match every moment","heading":"<p>Family outfits without the couture markup</p>","body":"<p>Curated looks for every family outing. Inclusive sizing, photo-ready sets, and fuss-free exchanges so dressing alike stays fun.</p>","primary_label":"Shop Mommy & Me","primary_link":"/collections/dresses","secondary_label":"Shop family sets","secondary_link":"/collections/family-sets","shipping_message":"","heading_size":"h1","layout":"media_right","color_scheme":"scheme-2","desktop_image":null,"mobile_image":null,"padding_top":36,"padding_bottom":32,"desktop_video_url":"https://cdn.shopify.com/videos/c/o/v/8b1cab37e2814ca09929ebecbf545029.mp4","mobile_video_url":"https://cdn.shopify.com/videos/c/o/v/89a6bbc425fc4558b367a0a0654a2d44.mp4","video_poster_image":null,"video_overlay_opacity":20,"video_poster_custom":"https://cdn.shopify.com/s/files/1/1557/1635/files/hero-family-fit-desktop-still_png.png?v=1763039806"},"blocks":{"badge_free_shipping":{"type":"badge","settings":{"text":"Free shipping + easy exchanges"}},"badge_sizes":{"type":"badge","settings":{"text":"Inclusive sizing XS-4X"}},"badge_social_proof":{"type":"badge","settings":{"text":"Loved by 30k families"}}},"block_order":["badge_free_shipping","badge_sizes","badge_social_proof"]}
```

### What to change it to

Replace that entire `"hero_family_fit_FvXq4J":{...}` fragment with this new version (still minified JSON):

```json
"hero_family_fit_FvXq4J":{"type":"hero-family-fit","settings":{"eyebrow":"Make every moment match","heading":"<p>Picture-perfect outfits for your whole crew</p>","body":"<p>From mommy-and-me twirls to holiday card photos, we make matching feel easy. Soft fabrics, inclusive sizing, and shipping you can trust&mdash;so you can focus on the memories, not the outfits.</p>","primary_label":"Shop Mommy &amp; Me dresses","primary_link":"/collections/dresses","secondary_label":"See family photo outfits","secondary_link":"/collections/family-sets","shipping_message":"","heading_size":"h1","layout":"media_right","color_scheme":"scheme-2","desktop_image":null,"mobile_image":null,"padding_top":36,"padding_bottom":32,"desktop_video_url":"https://cdn.shopify.com/videos/c/o/v/8b1cab37e2814ca09929ebecbf545029.mp4","mobile_video_url":"https://cdn.shopify.com/videos/c/o/v/89a6bbc425fc4558b367a0a0654a2d44.mp4","video_poster_image":null,"video_overlay_opacity":20,"video_poster_custom":"https://cdn.shopify.com/s/files/1/1557/1635/files/hero-family-fit-desktop-still_png.png?v=1763039806"},"blocks":{"badge_free_shipping":{"type":"badge","settings":{"text":"Free shipping + easy exchanges"}},"badge_sizes":{"type":"badge","settings":{"text":"Inclusive sizing XS-4X"}},"badge_social_proof":{"type":"badge","settings":{"text":"Loved by 30k families"}}},"block_order":["badge_free_shipping","badge_sizes","badge_social_proof"]}
```

### Requirements

- Do **not** modify any other section entries or the `"order"` array.
- Keep the JSON minified (one line is fine); just swap this substring exactly.
- After the change, validate that `templates/index.json` parses as JSON.

Stop once this replacement is complete.

---

## Prompt 2 – Update Mommy & Me Dresses intro in `templates/collection.json`

You are an AI coding assistant working in `C:\dev\dresslikemommy`. The file `templates/collection.json` is a minified JSON object defining collection sections and intros. I need you to update the intro text for the Mommy & Me Dresses collection while keeping everything else intact.

**File:** `templates/collection.json`  
**Block:** `"intro-mommy-dresses"` inside the `"intro-links-primary"` section.

### What’s there now

Search for this substring in `templates/collection.json` (it will appear as part of a long line):

```json
"intro-mommy-dresses":{"type":"intro-config","settings":{"handle":"mommy-and-me-dresses","eyebrow":"Mommy & me style guide","intro_richtext":"<p>Matching Mommy & Me dresses should feel effortless. Layer floaty maxi dresses for mom with twirl-ready minis and you have a one-and-done look for photoshoots or brunch. Need alternates? Our <a href=\"/collections/matching-family-pajamas\">matching family pajamas</a> keep cozy nights coordinated, and <a href=\"/collections/mommy-and-me-swimsuits\">family swimsuits</a> bring the same vibe to beach days.</p>","links_heading":"Plan the rest of the look","color_scheme":"scheme-1","padding_top":32,"padding_bottom":24}}
```

### What to change it to

Replace that entire `intro-mommy-dresses` block with this updated version (only the `intro_richtext` has changed, everything else is the same):

```json
"intro-mommy-dresses":{"type":"intro-config","settings":{"handle":"mommy-and-me-dresses","eyebrow":"Mommy & me style guide","intro_richtext":"<p>Matching Mommy &amp; Me dresses should feel effortless. Start by choosing mom’s silhouette (maxi, midi, or skater), then pick matching minis in the same print. Everything here is photo‑ready and comfy enough for brunch, birthdays, or family photos—just choose your sizes and go.</p>","links_heading":"Plan the rest of the look","color_scheme":"scheme-1","padding_top":32,"padding_bottom":24}}
```

### Requirements

- Do **not** change any other `"intro-config"` or `"link"` blocks.
- Keep the JSON structure and surrounding commas/braces exactly as they were so `templates/collection.json` remains valid.
- Validate that the JSON still parses after your edit.

Stop once this replacement is complete.

---

## Prompt 3 – Update Daddy & Me intro in `templates/collection.json`

You are working in `C:\dev\dresslikemommy`. The file `templates/collection.json` contains an `intro-daddy` block for the `daddy-and-me` handle. I need you to update its `intro_richtext` to a more gift‑oriented version.

**File:** `templates/collection.json`  
**Block:** `"intro-daddy"` inside `"intro-links-secondary"`.

### What’s there now

Find the `"intro-daddy"` block, which currently looks like this (all on one line):

```json
"intro-daddy":{"type":"intro-config","settings":{"handle":"daddy-and-me","eyebrow":"Daddy & Me playbook","intro_richtext":"<p>Match dad's laid-back polos, tees, and hoodies with kid-sized versions for instant photo moments. Layer with denim or joggers so playground plans stay comfortable.</p>","links_heading":"Complete the duo","color_scheme":"scheme-1","padding_top":32,"padding_bottom":24}}
```

### What to change it to

Replace the entire block with this version (only `intro_richtext` is different):

```json
"intro-daddy":{"type":"intro-config","settings":{"handle":"daddy-and-me","eyebrow":"Daddy & Me playbook","intro_richtext":"<p>Looking for the easiest Father’s Day or new‑dad gift? These tees and sets are sized for dads and littles together, so you can choose one design and match both in minutes. Pick his usual t‑shirt size and your mini’s age—we’ll handle the rest.</p>","links_heading":"Complete the duo","color_scheme":"scheme-1","padding_top":32,"padding_bottom":24}}
```

### Requirements

- Do not alter any other blocks (e.g., `link-daddy-tops`, `link-daddy-dresses`, etc.).
- Keep JSON valid and minified.

Stop when this replacement is done.

---

## Prompt 4 – Update Family Sets intro in `templates/collection.json`

You are editing `C:\dev\dresslikemommy\templates\collection.json`. There is already an `intro-family-sets` block inside `"intro-links-secondary"`. I need you to replace its `intro_richtext` with a clearer, bundle‑focused message.

**File:** `templates/collection.json`  
**Block:** `"intro-family-sets"` inside `"intro-links-secondary"`.

### What’s there now

Search for `"intro-family-sets":{"type":"intro-config"`; you will see a block like this (content may differ slightly, but the structure matches):

```json
"intro-family-sets":{"type":"intro-config","settings":{"handle":"family-sets","eyebrow":"Family Matching Sets","intro_richtext":"...existing text...","links_heading":"...","color_scheme":"scheme-1","padding_top":32,"padding_bottom":24}}
```

### What to change it to

Replace the entire `intro-family-sets` block with:

```json
"intro-family-sets":{"type":"intro-config","settings":{"handle":"family-sets","eyebrow":"Family sets, solved in one place","intro_richtext":"<p>Family matching sets are the fastest way to outfit everyone from one place. Pick a design you love, then add each family member’s size from the same set—no guessing or mixing across collections. Most sets include options for mom, dad, and kids so you can build your bundle in just a few clicks.</p>","links_heading":"Finish the matching story","color_scheme":"scheme-1","padding_top":32,"padding_bottom":24}}
```

### Requirements

- Keep the `"block_order"` array as it is; ensure `intro-family-sets` still appears there.
- Don’t touch other intros or links.

Stop when this replacement is complete.

---

## Prompt 5 – Insert homepage email signup banner section in `templates/index.json`

You are editing `C:\dev\dresslikemommy\templates\index.json`. I want you to add a new `email-signup-banner` section to the homepage and insert it into the section `order` array.

**File:** `templates/index.json`

### 5.1 Add a new section definition

Inside the top‑level `"sections"` object, add a new entry with a unique key, for example `"email_signup_home_CRO"`. It should look like this (minified, commas placed appropriately):

```json
"email_signup_home_CRO":{"type":"email-signup-banner","blocks":{"heading":{"type":"heading","settings":{"heading":"Get the family photo outfit cheat sheet","heading_size":"h2"}},"paragraph":{"type":"paragraph","settings":{"text":"<p>Drop your email to get our quick guide to choosing colors, fits, and poses for family photos—plus early access to new matching sets and occasional VIP offers.</p>","text_style":"body"}},"email_form":{"type":"email_form","settings":{}}},"block_order":["heading","paragraph","email_form"],"settings":{"image":null,"image_overlay_opacity":0,"show_background_image":false,"image_height":"small","desktop_content_position":"middle-center","show_text_box":true,"desktop_content_alignment":"center","mobile_content_alignment":"center","color_scheme":"scheme-1"}}
```

Important:
- Insert this as another key/value in the `"sections"` object, alongside existing keys like `"hero_family_fit_FvXq4J"`, `"home_best_sellers_Lp9k"`, etc.
- Ensure you add a comma before/after as needed so the JSON remains valid.

### 5.2 Add the section to the order array

At the bottom of `templates/index.json` there is an `"order":[ ... ]` array, currently something like:

```json
"order":["hero_family_fit_FvXq4J","home_best_sellers_Lp9k","home_reassurance_row_7rF","home_outfit_stories_Xq0n","home_editorial_copy","collection_list_PX36Hk","featured_collection","collection_list_QW3Byc"]
```

Modify this array to insert `"email_signup_home_CRO"` after `"home_outfit_stories_Xq0n"` and before `"home_editorial_copy"`, like this:

```json
"order":["hero_family_fit_FvXq4J","home_best_sellers_Lp9k","home_reassurance_row_7rF","home_outfit_stories_Xq0n","email_signup_home_CRO","home_editorial_copy","collection_list_PX36Hk","featured_collection","collection_list_QW3Byc"]
```

### Requirements

- Keep the rest of the file unchanged.
- Ensure `templates/index.json` is still valid JSON after you add the new section and update the order array.

Stop when the new `email_signup_home_CRO` section is defined and referenced in the order array.
