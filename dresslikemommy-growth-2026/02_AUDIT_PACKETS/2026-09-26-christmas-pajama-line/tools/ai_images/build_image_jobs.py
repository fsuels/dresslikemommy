#!/usr/bin/env python3
"""Build one image-generation job per 2026 Christmas pajama draft.

Each job = uploads/<handle>/ai/ with prompt.txt and ref1..ref3.jpg (vendor
references). The prompt is the owner's DRESS LIKE MOMMY photoshoot prompt,
adapted for a non-interactive Codex run that produces IMAGE 1, 3, 5 and 6
(owner's 4-image selection) in one session so the same family is used.
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path

from PIL import Image

ROOT = Path("/Users/fsuels/Projects/dresslikemommy")
TOOLS = ROOT / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-26-christmas-pajama-line/tools"

# Exact garment lettering to copy letter for letter (None = no lettering).
LETTERING = {
    "eternal-bliss-hearts": 'the small pink script "Eternal bliss" inside the two outlined hearts, exactly as printed',
    "good-luck-smile": 'the words "GOOD LUCK" under the big smiley face, exactly as printed',
    "starry-sky": 'the tiny script "a sky full of stars" under the star cluster, exactly as printed',
    "beary-cozy": 'the red script "beary cozy" on the adult and child tops',
    "candy-tree-christmas": '"MERRY" / "Christmas" lettering with a Santa hat on the red tops',
    "classic-red-plaid": None,
    "cookie-baking-crew": '"Cookie BAKING crew" beside a gingerbread cookie in a Santa hat',
    "cozy-reindeer": None,
    "evergreen-fair-isle": None,
    "green-merry-christmas": 'white script "Merry Christmas" beside a smiling Santa',
    "here-for-the-cookies": '"I\'M JUST HERE for the COOKIES"',
    "jolly-crew": 'white script "Jolly Crew"',
    "jolly-santa": 'white script "Merry Christmas" above a waving Santa',
    "joyful-merry-blessed": 'white script "Joyful Merry Blessed" with holly leaves',
    "let-it-snow": '"LET IT SNOW"',
    "lights-out-reindeer": '"Lights Out!" under a reindeer tangled in colorful lights',
    "merry-xmas-lights": '"MERRY" (red) above "XMAS!" (white) framed by colorful string-light bulbs',
    "plaid-reindeer": None,
    "plaid-tree-trio": "the small gold script under the three trees, copied exactly as in the reference photos",
    "reindeer-forest": 'white script "Merry Christmas" with green trees and reindeer',
    "santas-crew": '"SANTA\'S crew" in colorful letters with a Santa hat and antlers',
    "snowy-reindeer": None,
    "snowy-village-stripes": 'the small "Merry Christmas" lettering on the adult tops',
    "team-santa": '"TEAM SANTA" on the adult tops; the child top keeps its own lettering exactly as in the reference photos',
    "vintage-tree-truck": "the white holiday script under the car, copied exactly as in the reference photos",
    "we-are-family-evergreen": '"We are Family" in red and black',
    "we-are-family-red": '"We are Family" in black and white',
    "merry-snowman": 'red script "Merry Christmas" above the snowman',
    "black-santa-christmas": 'white script "Merry Christmas" above the cartoon Santa',
    "red-nordic-reindeer": None,
    "merry-reindeer-plaid": 'red block letters "MERRY CHRISTMAS" under the reindeer',
    "white-tree-nordic": None,
    "candy-cane-santa": '"MERRY CHRISTMAS!" beside Santa and the reindeer',
    "christmas-crew-plaid": '"CHRISTMAS CREW" lettering under the plaid Santa hat, copied exactly as in the reference photos',
    "merry-tartan-reindeer": '"MERRY CHRISTMAS" lettering under the reindeer antlers and Santa hat',
    "santa-gingerbread-raglan": "the festive Merry Christmas lettering around Santa and the tree, copied exactly as in the reference photos",
    "ho-ho-santa-hat": 'red script "Merry Christmas" under the Santa hat on the tops, and white "HO HO" lettering on the red pants',
    "dino-christmas": None,
    "navy-santa-holly": 'white script "Merry Christmas" above Santa',
    "blue-plaid-reindeer": None,
    "green-plaid-merry-tree": "\"a very Merry Christmas\" in white script on and under the decorated tree, copied exactly as in the reference photos",
    "buffalo-plaid-tree": '"MERRY Christmas" in red and black buffalo plaid letters under the tree, copied exactly as in the reference photos',
    "sky-stripe": 'the small cream label on the chest with tiny "HMP" letters and a bunny, copied exactly as in the reference photos',
}
ROLE_NOTES = {
    "candy-cane-santa": "The red and white candy cane stripe runs over ONE shoulder and down ONE sleeve only; the other sleeve is plain green. Keep that asymmetry.",
    "merry-tartan-reindeer": "The top body is navy and BOTH sleeves are red tartan; the pants are the same red tartan.",
    "dino-christmas": "Keep the dinosaurs friendly and cartoon-style exactly like the print; no realistic dinosaurs.",
    "team-santa": "The adult tops and the child top carry different lettering; keep each version on the right person.",
    "snowy-village-stripes": "The adult tops show a snowy village scene; the child top shows its own festive character graphic. Keep each version on the right person.",
    "plaid-reindeer": "The reindeer graphic varies slightly by family member (different hat or scarf); keep the versions shown in the references.",
    "snowy-reindeer": "The tops are SHORT-SLEEVE. Do not make them long-sleeve.",
}

PROMPT = """DRESS LIKE MOMMY — RELIABLE PHOTOSHOOT SYSTEM (automated run)

The attached vendor product images are the exact clothing reference for ONE Shopify listing: Family Matching Christmas pajamas, "{print_name}".

Generate FOUR separate images in this order, one at a time, and save each generated image file into the current working directory with exactly these names:
- image1.png — IMAGE 1, MAIN HERO IMAGE
- image3.png — IMAGE 3, BEST OCCASION IMAGE
- image5.png — IMAGE 5, PRODUCT-ONLY IMAGE
- image6.png — IMAGE 6, ALTERNATE LIFESTYLE IMAGE
Do not ask me anything and do not wait for NEXT; continue until all four files are saved. Keep the same model family across images 1, 3 and 6, as if photographed in one professional photoshoot.

IMPORTANT: Do NOT create a collage, grid or contact sheet. Do NOT put multiple photos inside one image.
Each output must be one single image, vertical 9:16 portrait, full-frame photo, no borders, no split screen, no text labels, no watermarks. If the generator returns a slightly different ratio, crop minimally to exact 9:16; do not downscale further.

SOURCE OF TRUTH: the uploaded vendor images are the exact clothing reference. The clothing must stay exactly the same as the vendor images.
You may change: models, pose, background, lighting, lifestyle setting, camera angle, scene.
You must NOT change: clothing color, clothing print, clothing pattern, graphic text, text spelling, fabric look, neckline, sleeve length, collar, buttons, pockets, waistband, drawstring, hemline, adult version, child version, matching family design.

PRODUCT LOCK for this listing:
- {print_sentence}
- {design_details}
- Garment lettering to reproduce exactly, letter for letter: {lettering}.
- {role_note}Only these garments exist: the matching two-piece pajama set (top + pants) for mom, dad and children. Do NOT add a baby romper, baby bodysuit, socks, slippers with prints, a dog, a pet outfit, a bandana or any other extra printed item.

BRAND CONTEXT: Dress Like Mommy sells matching family clothing. Images should feel warm, clean, bright, realistic, wholesome, family-friendly, commercial, European lifestyle catalog style, suitable for Shopify listings.

MODEL STYLE: all models must be European. Use a natural-looking European family (mom, dad, a girl and a boy): fair to light-medium skin tones, blonde, light brown or soft brunette hair, soft natural makeup, clean family-friendly styling, warm smiles, approachable real-family look; not runway models, not luxury fashion models, not overly glamorous, not heavily edited. The models MUST be different people from the vendor photos.

SCENES (holiday pajamas): Christmas morning, cozy bright bedroom with soft white bedding, family living room with a decorated tree, bedtime story, clean festive home.

IMAGE 1 — MAIN HERO IMAGE: the strongest Shopify main image. Show the product clearly in a clean, bright, professional Christmas lifestyle setting. Full outfits visible on the whole family.
IMAGE 3 — BEST OCCASION IMAGE: the most commercially useful scene for Christmas pajamas, e.g. Christmas morning by the tree opening gifts or a cozy festive bedroom. Same family as IMAGE 1. Clothing clearly visible.
IMAGE 5 — PRODUCT-ONLY IMAGE: no people. One adult set and one child set shown as a clean flat lay or on hangers on a simple light background, matching the vendor product exactly, so customers can verify what they are buying.
IMAGE 6 — ALTERNATE LIFESTYLE IMAGE: another strong gallery image with a different pose, angle or setting (e.g. sitting together on the bed or sofa, reading a story, laughing), same family, not repetitive.

STRICT QUALITY CHECK before saving each image: compare it to the vendor images. Reject and regenerate if the clothing design, color, print, pattern or graphic text changed, if the lettering is misspelled or unreadable, if the product is hidden, if anyone wears an invented item, if the wrong person wears the wrong garment, if the adult and child versions no longer match, if it is a collage or multi-image layout, if it is not vertical 9:16, or if it looks fake, distorted or unusable for Shopify.

When all four files are saved, reply with one line per file: name, width x height.
"""


PROMPT_MM = """DRESS LIKE MOMMY — RELIABLE PHOTOSHOOT SYSTEM (automated run)

The attached vendor images are the exact clothing reference for ONE Shopify listing: Mommy and Me matching pajamas, "{print_name}".
ref1.jpg is the vendor photo of the set (it may show only the child's version); ref2.jpg and ref3.jpg are close-up crops of the same garment (top details, pants).
The women's set is the identical design in a women's cut: same fabric, print, collar, piping, buttons or zipper, and pockets.

Generate FOUR separate images in this order, one at a time, and save each generated image file into the current working directory with exactly these names:
- image1.png — IMAGE 1, MAIN HERO IMAGE
- image3.png — IMAGE 3, BEST OCCASION IMAGE
- image5.png — IMAGE 5, PRODUCT-ONLY IMAGE
- image6.png — IMAGE 6, ALTERNATE LIFESTYLE IMAGE
Do not ask me anything and do not wait for NEXT; continue until all four files are saved. Keep the same mother and daughter across images 1, 3 and 6, as if photographed in one professional photoshoot.

IMPORTANT: Do NOT create a collage, grid or contact sheet. Do NOT put multiple photos inside one image.
Each output must be one single image, vertical 9:16 portrait, full-frame photo, no borders, no split screen, no text labels, no watermarks. If the generator returns a slightly different ratio, crop minimally to exact 9:16; do not downscale further.

SOURCE OF TRUTH: the vendor images are the exact clothing reference. The clothing must stay exactly the same as the vendor images.
You may change: models, pose, background, lighting, lifestyle setting, camera angle, scene.
You must NOT change: clothing color, print, pattern, collar shape, piping color, buttons or zipper, pockets, embroidery, fabric look (flat knit vs plush fleece), sleeve length, pant length, waistband, cuffs, hem.

PRODUCT LOCK for this listing:
- {print_sentence}
- {design_details}
- Garment lettering to reproduce exactly, letter for letter: {lettering}.
- {role_note}Only these garments exist: the matching two-piece pajama set (top + pants) for mom and daughter. Do NOT add a dad, a boy, a baby, socks, slippers with prints, a pet, a robe, a headband with prints or any other extra printed item. Do NOT add drawstrings, extra pockets, bows or trims that the vendor garment does not have.

BRAND CONTEXT: Dress Like Mommy sells matching mommy-and-me clothing. Images should feel warm, clean, bright, realistic, wholesome, family-friendly, commercial, European lifestyle catalog style, suitable for Shopify listings.

MODEL STYLE: all models must be European: one mom (about 30–38) and one daughter (about 6–9): fair to light-medium skin tones, blonde, light brown or soft brunette hair, soft natural makeup, warm smiles, approachable real-family look; not runway models, not overly glamorous, not heavily edited. The models MUST be different people from any vendor photo.

SCENES (winter pajamas, not Christmas-specific): cozy bright bedroom with soft white bedding, reading a bedtime story, hot cocoa on a winter morning by a window, a calm cream-and-wood living room. No Christmas trees, no Santa, no holiday decorations.

IMAGE 1 — MAIN HERO IMAGE: mom and daughter standing or sitting close together, full outfits clearly visible, clean bright cozy setting.
IMAGE 3 — BEST OCCASION IMAGE: the most commercially useful scene, e.g. a bedtime story in bed or a slow winter morning with cocoa. Same mom and daughter. Clothing clearly visible.
IMAGE 5 — PRODUCT-ONLY IMAGE: no people. One women's set and one child set as a clean flat lay on a simple light background, matching the vendor garment exactly, so customers can verify what they are buying.
IMAGE 6 — ALTERNATE LIFESTYLE IMAGE: another strong gallery image with a different pose, angle or setting (e.g. laughing on the sofa, brushing hair together), same mom and daughter, not repetitive.

STRICT QUALITY CHECK before saving each image: compare it to the vendor images. Reject and regenerate if the print, colors, collar, piping, buttons or pocket changed, if anyone wears an invented item, if the mother's and daughter's sets no longer match, if it is a collage or multi-image layout, if it is not vertical 9:16, or if it looks fake, distorted or unusable for Shopify.

When all four files are saved, reply with one line per file: name, width x height.
"""


PROMPT_SW = """DRESS LIKE MOMMY — RELIABLE PHOTOSHOOT SYSTEM (automated run)

The attached vendor images are the exact clothing reference for ONE Shopify listing: Family Matching Christmas crewneck sweatshirts, "{print_name}".
The same sweatshirt comes in RED and in GREEN; the family can mix both colors exactly like the vendor photos.

Generate FOUR separate images in this order, one at a time, and save each generated image file into the current working directory with exactly these names:
- image1.png — IMAGE 1, MAIN HERO IMAGE
- image3.png — IMAGE 3, BEST OCCASION IMAGE
- image5.png — IMAGE 5, PRODUCT-ONLY IMAGE
- image6.png — IMAGE 6, ALTERNATE LIFESTYLE IMAGE
Do not ask me anything and do not wait for NEXT; continue until all four files are saved. Keep the same model family across images 1, 3 and 6, as if photographed in one professional photoshoot.

IMPORTANT: Do NOT create a collage, grid or contact sheet. Each output must be one single image, vertical 9:16 portrait, full-frame photo, no borders, no text labels, no watermarks. If the generator returns a slightly different ratio, crop minimally to exact 9:16.

SOURCE OF TRUTH: the vendor images are the exact clothing reference for the SWEATSHIRTS. The sweatshirt must stay exactly the same: color (red or green), the row of small printed characters across the chest (gift box, Santa, snowman in a Santa hat, reindeer, Christmas tree, gift box, tiny gold stars), print size and position, crew neckline, ribbed cuffs and hem.
Only the sweatshirts are sold. Bottoms must be plain, unbranded jeans or plain neutral trousers. Do NOT show any cap, hat with logo, brand logo, text lettering, sunglasses or accessory with branding. No baby romper, no pet outfit.

PRODUCT LOCK:
- {print_sentence}
- {design_details}
- Garment lettering: none (do not add any text to the sweatshirts).
- {role_note}Mom and dad wear adult sweatshirts; a girl and a boy wear child sweatshirts. Mix red and green across the family.

BRAND CONTEXT: warm, clean, bright, realistic, wholesome, family-friendly, commercial, European lifestyle catalog style, suitable for Shopify listings.

MODEL STYLE: all models European: a natural-looking family (mom, dad, a girl and a boy), fair to light-medium skin, blonde, light brown or soft brunette hair, warm smiles; not runway models. The models MUST be different people from the vendor photos.

SCENES (Christmas): family living room with a decorated tree, decorating the tree, a cozy Christmas morning, a snowy-window holiday home.

IMAGE 1 — MAIN HERO IMAGE: the whole family standing together by a decorated tree, all four sweatshirts clearly visible, chest prints readable.
IMAGE 3 — BEST OCCASION IMAGE: decorating the Christmas tree or opening gifts together; same family; sweatshirts clearly visible.
IMAGE 5 — PRODUCT-ONLY IMAGE: no people. One adult sweatshirt and one child sweatshirt (one red, one green) as a clean flat lay on a simple light background, matching the vendor garment exactly.
IMAGE 6 — ALTERNATE LIFESTYLE IMAGE: a different pose or setting (sitting together on the sofa with cocoa, laughing), same family.

STRICT QUALITY CHECK before saving each image: reject and regenerate if the print changed, characters are missing or distorted, colors are wrong, any logo or text appears, anyone wears an invented printed item, it is a collage, it is not vertical 9:16, or it looks fake or unusable for Shopify.

When all four files are saved, reply with one line per file: name, width x height.
"""


PROMPT_SWF = """DRESS LIKE MOMMY — RELIABLE PHOTOSHOOT SYSTEM (automated run)

The attached vendor images are the exact clothing reference for ONE Shopify listing: Family Matching crewneck sweatshirts, "{print_name}".
The same sweatshirt is sold in these colors: {colors_line}. The family can mix colors, exactly like the vendor photos.

Generate FOUR separate images in this order, one at a time, and save each generated image file into the current working directory with exactly these names:
- image1.png — IMAGE 1, MAIN HERO IMAGE
- image3.png — IMAGE 3, BEST OCCASION IMAGE
- image5.png — IMAGE 5, PRODUCT-ONLY IMAGE
- image6.png — IMAGE 6, ALTERNATE LIFESTYLE IMAGE
Do not ask me anything and do not wait for NEXT; continue until all four files are saved. Keep the same model family across images 1, 3 and 6, as if photographed in one professional photoshoot.

IMPORTANT: Do NOT create a collage, grid or contact sheet. Each output must be one single image, vertical 9:16 portrait, full-frame photo, no borders, no text labels, no watermarks. If the generator returns a slightly different ratio, crop minimally to exact 9:16.

SOURCE OF TRUTH: the vendor images are the exact clothing reference for the SWEATSHIRTS. Each sweatshirt must stay exactly the same: its color (only colors from the list above; raglan colors keep their contrast sleeves and cream body), the chest print (design, colors, size and position), crew neckline, ribbed cuffs and hem, relaxed drop-shoulder fit.
Only the sweatshirts are sold. Bottoms must be plain, unbranded jeans, plain trousers or a plain skirt. Do NOT show any cap, hat with logo, brand logo, sunglasses, extra text, or accessory with branding. No baby romper, no pet outfit.

PRODUCT LOCK:
- {print_sentence}
- {design_details}
- Garment lettering: {lettering}.
- {role_note}Mom and dad wear adult sweatshirts; a girl and a boy wear child sweatshirts. Show at least two of the listed colors across the family, like the vendor photos.

BRAND CONTEXT: warm, clean, bright, realistic, wholesome, family-friendly, commercial, European lifestyle catalog style, suitable for Shopify listings.

MODEL STYLE: all models European: a natural-looking family (mom, dad, a girl and a boy), fair to light-medium skin, blonde, light brown or soft brunette hair, warm smiles; not runway models. The models MUST be different people from the vendor photos.

SCENES (fall, everyday): a sunny autumn park path with fallen leaves, a cozy bright living room, a weekend trip by the sea on a cool day, a pumpkin patch or farm stand. No Christmas decorations.

IMAGE 1 — MAIN HERO IMAGE: the whole family standing together outdoors on a fall day, all four sweatshirts clearly visible, chest prints readable.
IMAGE 3 — BEST OCCASION IMAGE: a family outing (autumn park walk or seaside weekend); same family; sweatshirts clearly visible.
IMAGE 5 — PRODUCT-ONLY IMAGE: no people. One adult sweatshirt and one child sweatshirt (two different listed colors) as a clean flat lay on a simple light background, matching the vendor garments exactly.
IMAGE 6 — ALTERNATE LIFESTYLE IMAGE: a different pose or setting (sitting together on the sofa at home, laughing), same family.

STRICT QUALITY CHECK before saving each image: reject and regenerate if the print changed, is missing or distorted, a color is not in the list, any logo or extra text appears, anyone wears an invented printed item, it is a collage, it is not vertical 9:16, or it looks fake or unusable for Shopify.

When all four files are saved, reply with one line per file: name, width x height.
"""


PROMPT_PET = """DRESS LIKE MOMMY — RELIABLE PHOTOSHOOT SYSTEM (automated run)

This Shopify listing sells ONE product: a matching DOG VEST, "{print_name}" — {print_sentence}
ref1.jpg is the vendor photo: the small sleeveless plaid dog vest is the item at the top of the flat lay (the human pajamas in that photo are a different listing).
ref2.jpg shows the matching family pajama set (sold separately) exactly as it must look when the family appears.
ref3.jpg is a close-up of the dog vest plaid.

Generate FOUR separate images in this order and save each into the current working directory with exactly these names:
- image1.png — IMAGE 1, MAIN HERO: a friendly medium-size dog wearing the blue and black plaid vest, sitting in front of a decorated Christmas tree, the vest clearly visible.
- image3.png — IMAGE 3, BEST OCCASION: the same dog wearing the vest with a European family (mom, dad, girl, boy) in the matching Blue Plaid Reindeer pajamas from ref2 on Christmas morning, the dog in front and the vest clearly visible.
- image5.png — IMAGE 5, PRODUCT-ONLY: the dog vest alone as a clean flat lay on a simple light background, matching the vendor vest exactly (sleeveless, black binding at the neck, leg openings and curved hem, a row of small snaps down the center, same plaid).
- image6.png — IMAGE 6, ALTERNATE LIFESTYLE: the same dog in the vest cuddled on a sofa with the girl in the matching pajamas, cozy holiday living room.
Do not ask me anything; continue until all four files are saved. Keep the same dog and family across images 1, 3 and 6.

Each output: one single vertical 9:16 photo, no collage, no borders, no text, no watermark. Crop minimally to 9:16 if needed.
PRODUCT LOCK: the dog vest plaid, colors (blue and black with white lines) and cut must match the vendor vest exactly; black binding at the neck, leg openings and curved hem; a row of small snaps down the center; no sleeves, no hood, no bow, no text on the vest. The family pajamas must match ref2 exactly (black tops with sky-blue trim and the ornament reindeer print, blue plaid pants with black cuffs). No other printed items, no logos, no dog collars with text.
STYLE: warm, bright, realistic European lifestyle catalog photos for Shopify; the dog looks happy and well cared for.
STRICT QUALITY CHECK before saving: reject and regenerate if the vest cut or plaid changed, the dog wears anything else printed, the family pajamas differ from ref2, it is a collage, or not 9:16.
When all four files are saved, reply with one line per file: name, width x height.
"""


import sys as _sys
_sys.path.insert(0, str(TOOLS))
import build_specs_zoya as zb  # noqa: E402
ZREFS = {k: zb.ahash(p) for k, p in zb.CHART_REFS.items()}


def white_fraction(path: Path) -> float:
    im = Image.open(path).convert("RGB")
    im.thumbnail((160, 160))
    px = list(im.getdata())
    return sum(1 for r, g, b in px if r > 232 and g > 232 and b > 232) / len(px)


def main() -> None:
    import importlib.util, sys  # noqa: E401
    sys.path.insert(0, str(TOOLS))
    from engine_loader import load
    jobs = []
    only = set(sys.argv[1:])  # optional: build jobs for these handles only
    for spec_path in sorted((TOOLS / "specs").glob("*.json")):
        spec = json.loads(spec_path.read_text(encoding="utf-8"))
        if only and spec["handle"] not in only:
            continue
        handle = spec["handle"]
        key = (handle.replace("-family-matching-pajamas", "").replace("-mommy-and-me-pajamas", "")
               .replace("-family-matching-sweatshirts", "").replace("-matching-dog-vest", "-dog-vest"))
        ns = load(spec_path)
        job = ROOT / "uploads" / handle / "ai"
        job.mkdir(parents=True, exist_ok=True)
        # ref1 = the draft's vendor image (on-model); ref2/ref3 = clean product shots from the offer gallery.
        shutil.copyfile(ROOT / "uploads" / handle / spec["image_filename"], job / "ref1.jpg")
        desc = ROOT / "ops/sourcing/vendor-images" / spec["offer_id"] / "desc"
        candidates = []
        # Explicit gallery picks (spec "ai_refs") win; supplier charts never become references.
        picks = [desc / n for n in spec.get("ai_refs", [])]
        # A spec that names ai_refs (even an empty list) never falls back to scanning the
        # offer gallery: multi-design offers mix other designs into the description.
        explicit = "ai_refs" in spec and spec.get("mode") in ("mommy_me", "family_sweatshirt", "family_pet")
        for p in ([] if (picks or explicit) else sorted(desc.glob("*.jpg"))):
            if p.name in spec.get("skip_ref_images", []):
                continue
            try:
                w, h = Image.open(p).size
            except Exception:
                continue
            if min(w, h) < 600 or p.name in ("00.jpg", "01.jpg"):  # 00/01 are the size charts on these offers
                continue
            if spec.get("chart_table", "").startswith("zoya") and zb.chart_kind(p, ZREFS):
                continue
            candidates.append((white_fraction(p), p))
        candidates.sort(key=lambda t: -t[0])
        import hashlib
        main_hash = hashlib.md5((ROOT / "uploads" / handle / spec["image_filename"]).read_bytes()).hexdigest()
        seen = {main_hash}
        refs = []
        ordered = [(0, p) for p in picks] or sorted(candidates, key=lambda t: (t[0] <= 0.35, -t[0]))
        for frac, p in ordered:
            digest = hashlib.md5(p.read_bytes()).hexdigest()
            if digest in seen:
                continue
            seen.add(digest)
            refs.append(p)
            if len(refs) == 2:
                break
        for i, p in enumerate(refs, start=2):
            shutil.copyfile(p, job / f"ref{i}.jpg")
        # Only the design's own flat lay exists: add two detail crops of it (top, pants)
        # so the generator sees collar, piping, buttons and print up close.
        if len(refs) < 2:
            base = Image.open(job / "ref1.jpg").convert("RGB")
            w, h = base.size
            crops = [(0, 0, int(w * 0.62), int(h * 0.62)), (int(w * 0.45), int(h * 0.1), w, int(h * 0.95))]
            for i, box in enumerate(crops[len(refs):], start=2 + len(refs)):
                c = base.crop(box)
                c = c.resize((c.width * 2, c.height * 2))
                c.save(job / f"ref{i}.jpg", quality=92)
            refs = refs + [None] * (2 - len(refs))
        lettering = LETTERING.get(key) or "none (no lettering on these garments; do not add any text)"
        role_note = (ROLE_NOTES.get(key, "") + " ") if ROLE_NOTES.get(key) else ""
        base_prompt = PROMPT_SWF if spec.get("title_variant") == "everyday" else {"mommy_me": PROMPT_MM, "family_sweatshirt": PROMPT_SW, "family_pet": PROMPT_PET}.get(spec.get("mode"), PROMPT)
        if spec.get("garment") == "sweater":  # knit family sweaters reuse the everyday prompt
            base_prompt = (PROMPT_SWF.replace("crewneck sweatshirts", "knit crewneck sweaters").replace("SWEATSHIRTS", "KNIT SWEATERS")
                           .replace("sweatshirts", "knit sweaters").replace("sweatshirt", "knit sweater")
                           .replace("its color (only colors from the list above; raglan colors keep their contrast sleeves and cream body), the chest print",
                                    "its color (only colors from the list above), the knit pattern and texture, the chest motif"))
        if len(spec.get("colors", [])) == 1:  # single-color listing: everyone wears the one color
            base_prompt = (base_prompt.replace(" The family can mix colors, exactly like the vendor photos.", " Everyone wears this one color, exactly like the vendor photos.")
                           .replace(" Show at least two of the listed colors across the family, like the vendor photos.", "")
                           .replace("(two different listed colors)", "(same color)"))
        prompt = base_prompt.format(
            colors_line=", ".join(c["name"] for c in spec.get("colors", [])),
            print_name=spec["print_name"],
            print_sentence=spec["print_sentence"],
            design_details=ns["DESIGN_TEXT"][spec["design_key"]],
            lettering=lettering,
            role_note=role_note,
        )
        (job / "prompt.txt").write_text(prompt, encoding="utf-8")
        jobs.append({"handle": handle, "refs": 1 + len(refs), "dir": str(job)})
    (TOOLS / "ai_images" / "jobs.json").write_text(json.dumps(jobs, indent=1), encoding="utf-8")
    for j in jobs:
        print(j["handle"], "refs", j["refs"])


if __name__ == "__main__":
    main()
