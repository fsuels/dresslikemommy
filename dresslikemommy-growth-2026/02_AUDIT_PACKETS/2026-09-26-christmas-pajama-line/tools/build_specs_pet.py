#!/usr/bin/env python3
"""Spec for the 衣林 matching dog vest sold with Blue Plaid Reindeer (offer 1029357235756,
mode "family_pet", chart "yilin_dog").

Same offer and gate as the live family set (created 2026-03-12, release Autumn 2026, 衣林,
our top pajama supplier). The offer sells the vest as Dog S–XXL at ¥14 in the same blue
plaid as the family pants. Pricing: the vendor lists a 450 g placeholder weight for every
SKU; a dog vest ships at roughly 200 g, so landed ≈ (14 + 5 + 45.4 + 8.2×2)/7.11 + fees
≈ $12.4, and the 50% single-item rule needs ≥ $24.80 → $24.99, compare-at +$10.
"""
import json
from pathlib import Path

ROOT = Path("/Users/fsuels/Projects/dresslikemommy")
TOOLS = ROOT / "dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-26-christmas-pajama-line/tools"
OFFER = "1029357235756"
handle = "blue-plaid-reindeer-matching-dog-vest"
fname = "01-blue-plaid-reindeer-dog-vest.jpg"
up = ROOT / "uploads" / handle
up.mkdir(parents=True, exist_ok=True)
man = json.loads((ROOT / f"ops/sourcing/vendor-images/{OFFER}/desc/manifest.json").read_text(encoding="utf-8"))
(up / fname).write_bytes((ROOT / f"ops/sourcing/vendor-images/{OFFER}/desc/16.jpg").read_bytes())
spec = {
    "mode": "family_pet", "offer_id": OFFER, "offer_created": "2026-03-12", "handle": handle, "shortcode": "BPRV",
    "print_name": "Blue Plaid Reindeer",
    "colors": [{"name": "Blue", "token": "BLU"}],
    "color_pattern_gids": ["gid://shopify/Metaobject/69639766113", "gid://shopify/Metaobject/69943132257",
                           "gid://shopify/Metaobject/130283143265"],
    "color_pattern_labels": ["Blue", "Black", "Checkered"],
    "fabric_key": "cotton65", "design_key": "dog_vest", "sleeve_style": "Sleeveless",
    "print_sentence": "A blue and black plaid dog vest cut from the same plaid as the Blue Plaid Reindeer family pajama pants.",
    "feature_label": "Blue plaid:", "feature_text": "The same blue and black plaid as the family pajama pants.",
    "extra_tags": ["Plaid", "Blue", "Blue Plaid Reindeer Family Matching Pajamas"],
    "media_alt": "Dog in a matching blue and black plaid vest beside a family in Blue Plaid Reindeer Christmas pajamas.",
    "image_url": next(d["url"] for d in man["desc_images"] if d.get("path", "").endswith("/16.jpg")),
    "image_filename": fname, "ai_refs": ["16.jpg", "10.jpg"], "skip_ref_images": ["00.jpg", "01.jpg", "02.jpg", "03.jpg"],
    "chart_source": "yilin_cn", "chart_table": "yilin_dog",
    "chart_note": "the offer's own description publishes the 狗狗尺寸表 (collar, back length, bust) inside description image 03, saved as SOURCE_SIZE_CHART.",
    "child_price": "24.99", "adult_price": "24.99",
    "vendor_title": "欧美棉圣诞亲子家居服套装 (衣林) — dog vest option",
    "vendor_color_values": ["As Shown in Picture"], "vendor_codes": [],
    "vendor_size_labels": ["Dog S", "Dog M", "Dog L", "Dog XL", "Dog 2XL"],
    "vendor_prices_note": "Dog ¥14 (all sizes).",
    "designs_note": "The dog vest option of the Blue Plaid Reindeer family offer, one Shopify product linked to the family set.",
    "exclusions_note": "Only the Dog S–XXL SKUs are listed here; the family sizes are the separate Blue Plaid Reindeer family listing.",
    "evidence_lines": [
        "Supplier: 衣林 (Guangzhou Yilin garment), our top pajama supplier by BuckyDrop history.",
        "New-design gate: offer created 2026-03-12; 'Year and season of release' Autumn 2026 (same offer as the live family set).",
        "Fabric evidence: fabric name cotton, main fabric content 65% (offer attribute).",
        "Pricing: ¥14 unit, ~200 g shipped estimate (vendor weight field is a 450 g placeholder), landed ≈ $12.4 → $24.99 passes the 50% single-item test.",
    ],
}
(TOOLS / "specs" / f"{handle}.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(handle)
