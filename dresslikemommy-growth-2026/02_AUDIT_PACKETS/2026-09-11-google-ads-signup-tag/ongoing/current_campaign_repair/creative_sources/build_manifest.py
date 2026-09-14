"""Build a source-bound creative review packet. Local reads only; no image edits."""

import csv
import hashlib
import json
from pathlib import Path
from PIL import Image


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[5]
COLLECTION = HERE / "../../landing_qa/source_collection_en.json"
SOURCE_FILES = {
    "RGHM_landscape_v1": "uploads/red-gingham-mommy-and-me-set/02-front-garden.webp",
    "SBF_landscape_v1": "uploads/sky-blue-family-matching-set/01-sky-blue-family-matching-product.png",
    "TGHW_landscape_v1": "uploads/together-heart-family-matching-sweaters/01-together-heart-family-sweaters.png",
    "NSPR_landscape_v1": "uploads/navy-sprig-mommy-and-me-dresses/01-navy-sprig-mommy-and-me-product.png",
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def image_metadata(path):
    with Image.open(path) as im:
        width, height = im.size
        result = {"width": width, "height": height, "format": im.format,
                  "ratio": round(width / height, 6), "metadata_keys": list(im.info)}
    return {**result, "bytes": path.stat().st_size, "sha256": sha(path)}


def write(name, data):
    (HERE / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


collection = json.loads(COLLECTION.read_text())
assert collection["http_status"] == 200 and collection["main_unique_product_link_count"] == 36
cards = []
headings = {h["text"]: h["attrs"]["id"].rsplit("-", 1)[-1]
            for h in collection["headings"] if h.get("in_main")
            and "__product-grid-" in h.get("attrs", {}).get("id", "")}
for index, link in enumerate(collection["product_links"]):
    handle = link["url"].split("/products/")[-1].split("?")[0]
    if handle in {c["handle"] for c in cards}:
        continue
    cards.append({"handle": handle, "product_id": headings[link["text"]], "title": link["text"],
                  "url": link["url"], "product_links_index": index})
assert len(cards) == 36
by_handle = {c["handle"]: c for c in cards}
inventory = []
for card in cards:
    for path in sorted((ROOT / "uploads" / card["handle"]).glob("*")):
        if path.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"}:
            continue
        if any(term in path.name.lower() for term in ["size", "chart", "source", "selector"]):
            continue
        inventory.append({"handle": card["handle"], "product_id": card["product_id"],
                          "local_file": str(path.relative_to(ROOT)), **image_metadata(path)})
assert len(inventory) == 25
write("local_collection_image_inventory.json", {
    "method": "Matched exact handles from the preserved 36-card first page to local uploads/<handle> directories; nonrecursive image metadata scan.",
    "capture_source": str(COLLECTION.relative_to(HERE)), "capture_sha256": sha(COLLECTION),
    "capture_completed_at": collection["completed_at"], "first_page_cards": cards,
    "source_page_reported_collection_total": 118,
    "scope_limit": "36 observed first-page cards, not an exhaustive image or 118-product collection audit. Local filename/handle association alone does not prove current Shopify media attachment or rights.",
    "excluded_filenames_containing": ["size", "chart", "source", "selector"],
    "images": inventory,
})

provenance = {
    "RGHM_landscape_v1": {
        "source_class": "LOCAL_LISTING_PRODUCT_PHOTOGRAPH__CAMERA_ORIGINAL_STATUS_UNKNOWN",
        "record": "ops/listings/red-gingham-mommy-and-me-set-listing.md",
        "record_lines": [24, 73, 76, 161],
        "facts": ["Historical listing record binds the product ID/handle to the local uploads directory.",
                  "Supplier/listing evidence exists, but no exact image authorship, paid-ad license or model-release document was found in the scoped records.",
                  "Current fresh collection card calls these separates; top and pants are selected individually. No complete-outfit price claim is permitted by this image alone."],
        "current_shopify_media_id": "NOT_READ", "source_to_current_media_byte_identity": "NOT_VERIFIED",
    },
    "SBF_landscape_v1": {
        "source_class": "OWNER_SUPPLIED_LOCAL_LISTING_PRODUCT_IMAGE__CAMERA_ORIGINAL_STATUS_UNKNOWN",
        "record": "ops/listings/sky-blue-family-matching-set-listing.md", "record_lines": [24, 65, 154],
        "facts": ["Historical listing identifies the attached product image as source evidence.",
                  "Historical verify-sky-blue-family-matching-set.json includes matching product-media alt text; no current media bytes were fetched.",
                  "Shorts and accessories are styling only; the source listing excludes shorts variants."],
        "current_shopify_media_id": "NOT_READ", "source_to_current_media_byte_identity": "NOT_VERIFIED",
    },
    "TGHW_landscape_v1": {
        "source_class": "OWNER_SUPPLIED_LOCAL_LISTING_PRODUCT_IMAGE__CAMERA_ORIGINAL_STATUS_UNKNOWN",
        "record": "ops/listings/together-heart-family-matching-sweaters-listing.md", "record_lines": [24, 25, 26, 170],
        "facts": ["Historical listing identifies the supplied product image and describes four long-sleeve crewneck sweaters with Together heart back graphics.",
                  "The listing's phrase 'owned product image' is a record claim, not independent proof of copyright or advertising/model-release rights.",
                  "Pants, skirts, hats, glasses, shoes and accessories are styling only; image shows four colors, not evidence for all offered colors."],
        "current_shopify_media_id": "NOT_READ", "source_to_current_media_byte_identity": "NOT_VERIFIED",
    },
    "NSPR_landscape_v1": {
        "source_class": "OWNER_SUPPLIED_LOCAL_LISTING_PRODUCT_IMAGE__CAMERA_ORIGINAL_STATUS_UNKNOWN",
        "record": "ops/listings/navy-sprig-mommy-and-me-dresses-listing.md", "record_lines": [6, 22, 28, 96],
        "facts": ["Historical listing identifies the owner-attached product image as source evidence.",
                  "Both subjects, hats and shoes are complete in the 310x476 input; source resolution limits verification of tiny print/construction details.",
                  "Dress and cardigan are separate Type choices, not one bundled SKU."],
        "current_shopify_media_id": "NOT_READ", "source_to_current_media_byte_identity": "NOT_VERIFIED",
    },
}
reviews = {
    "RGHM_landscape_v1": {
        "decision": "VISUAL_REVIEW_CANDIDATE__SECOND_REVIEW_PENDING",
        "observed": ["Two original subject roles, standing/raised-leg pose, white gathered tops, red gingham pants, baskets and complete garment coverage remain visually recognizable.",
                     "The canvas adds wall/garden space and removes unused upper wall as requested; there is no added promotional text or third person."],
        "limits": ["Exact source-pixel preservation is not asserted. Pixel inequality alone is not evidence of a consumer-visible garment defect.",
                   "Review the lace construction, gingham size, seam placement, fit and faces for consumer-visible fidelity before promotion."],
        "background_only_invariant": "NOT_VERIFIED", "garment_identity": "BROAD_VISUAL_CONSISTENCY__EXACT_DETAILS_UNVERIFIED",
        "parent_visual_review": "Root reported designs, cuts and colors visually consistent; second independent review pending.",
    },
    "SBF_landscape_v1": {
        "decision": "REJECTED__OUTSIDE_BACKGROUND_ONLY_SCOPE",
        "observed": ["The output reconstructs the father's top-of-head and raised hand that were clipped by the source edges, despite the explicit no-reconstruction prompt.",
                     "The generated father/child facial detail is re-rendered. This cannot be treated as protected original foreground."],
        "limits": ["Dresses and shirts remain similar in broad color/style, but exact pleating, neckline and human-identity preservation is not verified."],
        "background_only_invariant": "FAILED", "garment_identity": "NOT_VERIFIED",
    },
    "TGHW_landscape_v1": {
        "decision": "VISUAL_REVIEW_CANDIDATE__SECOND_REVIEW_PENDING",
        "observed": ["Four back-facing subjects, blue/yellow/red/black sweaters, heart hand pose and complete visible outfits are retained in broad composition.",
                     "The existing Together wording remains visible on all four sweaters; stray top-edge sky text is removed and no new promotional text is added."],
        "limits": ["Exact source-pixel preservation is not asserted. Pixel inequality alone is not evidence of a consumer-visible garment defect.",
                   "Check heart artwork, typography, sweater construction and colors against the source; readable wording alone does not prove the whole graphic is faithful."],
        "background_only_invariant": "NOT_VERIFIED", "garment_identity": "BROAD_VISUAL_CONSISTENCY__EXACT_DETAILS_UNVERIFIED",
        "parent_visual_review": "Root reported designs, cuts and colors visually consistent; second independent review pending.",
    },
    "NSPR_landscape_v1": {
        "decision": "VISUAL_REVIEW_CANDIDATE__INDEPENDENT_REVIEW_PENDING",
        "observed": ["Two complete subjects, original standing relationship, hats and footwear remain in frame.",
                     "Navy small-sprig dresses, gray open cardigans and respective garment lengths remain broadly consistent. No promotional text or extra person was added."],
        "limits": ["The input is only310x476. Fine sprig shape/density and center-front neckline/tie/button details are not fully resolvable; inspect these before promotion.",
                   "Generated dimensions do not supply new factual evidence about fine garment detail, fibers, included accessories or rights."],
        "background_only_invariant": "NOT_VERIFIED", "garment_identity": "BROAD_VISUAL_CONSISTENCY__FINE_DETAILS_SOURCE_LIMITED",
        "parent_visual_review": "PENDING",
    },
}
receipts = json.loads((HERE / "generation_receipts.json").read_text())
prompts = json.loads((HERE / "generation_prompts.json").read_text())
receipts["receipts"].append(json.loads((HERE / "replacement_generation_receipt.json").read_text()))
prompts["items"].append(json.loads((HERE / "replacement_generation_prompt.json").read_text())["item"])
rows = []
for item in prompts["items"]:
    key = item["asset_id"]
    source = ROOT / SOURCE_FILES[key]
    generated = HERE / "generated" / (key + ".png")
    receipt = next(r for r in receipts["receipts"] if r["asset_id"] == key)
    original_output = Path(receipt["result"]["generated_path"])
    assert generated.read_bytes() == original_output.read_bytes()
    source_meta, result_meta = image_metadata(source), image_metadata(generated)
    assert result_meta["width"] >= 1200 and result_meta["height"] >= 628
    assert abs(result_meta["ratio"] - 1.91) < 0.01
    card = by_handle[item["handle"]]
    assert card["product_id"] == item["product_id"]
    rows.append({"asset_id": key, "product_id": item["product_id"], "handle": item["handle"],
                 "name": card["title"], "source_file": SOURCE_FILES[key], "source_metadata": source_meta,
                 "source_visually_inspected": True, "generated_file": "generated/" + key + ".png",
                 "generated_metadata": result_meta, "generated_visually_inspected": True,
                 "source_original_bytes_preserved": True, "tool_original_output_bytes_preserved": True,
                 "collection_membership": {"status": "OBSERVED_IN_SAME_SESSION_PUBLIC_COLLECTION_FIRST_PAGE",
                                           "source": str(COLLECTION.relative_to(HERE)),
                                           "captured_at": collection["completed_at"],
                                           "product_links_index": card["product_links_index"],
                                           "collection_url": collection["final_url"]},
                 "provenance": provenance[key], "visual_review": reviews[key],
                 "upload_authorization": "PARENT_REVIEW_REQUIRED__NO_UPLOAD_PERFORMED"})
manifest = {
    "artifact_type": "CREATIVE_REVIEW_PACKET_NOT_CAMPAIGN_AUTHORITY",
    "campaign_id": "24247604341", "asset_group_id": "6746545742",
    "objective": "Prepare three landscape asset candidates for the actual mommy-and-me collection without changing product truth.",
    "generation_mode": "BUILT_IN_IMAGE_GEN_EDIT", "generation_calls": 4,
    "generated_count": 4, "pixel_dimension_pass_count": 4, "upload_ready_count": 0,
    "rejected_count": 1, "held_for_independent_review_count": 3,
    "assets": rows,
    "rights_scope": "Parent authorized these existing client product assets for creative review. No independent authorship, paid-ad license or model-release evidence was established in the bounded local source records; no new rights are asserted.",
    "originality_scope": "Original here means the exact unchanged input file used for the edit, not certified camera-original or verified non-AI imagery. Absence of common AI metadata markers does not prove a photographic origin.",
    "other_local_evidence": [
        {"path": "dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-01-google-ads-brand-search-asset-enrichment/",
         "finding": "Contains older product-derived 1200x628 blurred-background composites. Historical packet is explicitly superseded and lacks current exact-product/foreground verification; no upload recommendation is inherited."},
        {"path": "uploads/sunset-ombre-family-matching-set/01-product-image.png",
         "finding": "785x524 landscape source inspected. Adult faces/heads are clipped; reaching1.91 by cropping would further sacrifice garment framing. Not selected."},
        {"path": "uploads/white-crochet-mommy-and-me-set/01-white-crochet-mommy-and-me-set.png",
         "finding": "791x828 source inspected. Mother's head clipped; not selected for this three-source attempt."}],
    "measurement_limit": "Aspect ratio and ad strength are diagnostic asset-readiness signals, not purchases, conversion value, CPA, ROAS or profit. This packet demonstrates no sales lift or 650% ROAS attainment.",
    "replacement_search": {"images_inspected": 3,
                           "selected": "Navy Sprig: full two subjects/hats/shoes,310x476 source",
                           "not_selected": ["Green Botanical: mother's upper face and feet clipped", "Pink Lace: feet and upper accessory/hat edges clipped"]},
    "acceptance_criterion": "Consumer-visible truth of garment design, cut, color, print, fit and subjects. Byte-identical source pixels are not a proxy requirement. Specific foreground reconstruction rejected Sky Blue.",
    "next_action": "Complete independent consumer-truth review of Red Gingham, Together Heart and replacement Navy Sprig; exclude rejected Sky Blue. No additional generation or publication is authorized by this packet.",
    "source_sha256": {str(COLLECTION.relative_to(HERE)): sha(COLLECTION),
                      "generation_prompts.json": sha(HERE / "generation_prompts.json"),
                      "generation_receipts.json": sha(HERE / "generation_receipts.json"),
                      "replacement_generation_prompt.json": sha(HERE / "replacement_generation_prompt.json"),
                      "replacement_generation_receipt.json": sha(HERE / "replacement_generation_receipt.json")},
    "public_http_requests": 0, "shopify_metadata_queries": 0, "browser_or_native_actions": 0,
    "account_writes_or_uploads": 0, "cli_or_api_fallback_calls": 0,
}
write("manifest.json", manifest)
with (HERE / "manifest.csv").open("w", newline="") as handle:
    fields = ["asset_id", "product_id", "handle", "source_file", "source_dimensions", "generated_file",
              "generated_dimensions", "ratio", "decision", "background_only_invariant", "upload_ready"]
    writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow({"asset_id": row["asset_id"], "product_id": row["product_id"], "handle": row["handle"],
                         "source_file": row["source_file"],
                         "source_dimensions": f"{row['source_metadata']['width']}x{row['source_metadata']['height']}",
                         "generated_file": row["generated_file"],
                         "generated_dimensions": f"{row['generated_metadata']['width']}x{row['generated_metadata']['height']}",
                         "ratio": row["generated_metadata"]["ratio"], "decision": row["visual_review"]["decision"],
                         "background_only_invariant": row["visual_review"]["background_only_invariant"], "upload_ready": False})
write("VALIDATION.json", {"status": "PASS_WITH_FIDELITY_LIMITS", "local_source_images_scanned": len(inventory),
                          "collection_card_ids_and_handles_reconciled": len(cards), "generated_pngs": len(rows),
                          "all_output_copies_byte_identical": True, "dimension_and_aspect_checks": "PASS",
                          "source_and_output_visual_review": "RUN", "exact_foreground_preservation": "NOT_VERIFIED",
                          "sky_blue_background_only_check": "FAILED", "campaign_upload": "NOT_RUN"})
print(json.dumps({"status": "PASS_WITH_FIDELITY_LIMITS", "local_sources": len(inventory),
                  "generated": len(rows), "dimension_pass": 4, "held": 3, "rejected": 1, "upload_ready": 0}))
