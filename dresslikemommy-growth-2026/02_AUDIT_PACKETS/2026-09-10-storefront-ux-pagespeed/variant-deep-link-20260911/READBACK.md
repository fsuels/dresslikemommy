# Existing variant-link repair verified — September 11

Status: VERIFIED in the existing unpublished V6 release; live acceptance pending. No theme, product, variant, price, feed, account or payment configuration changed in this follow-up. Final cleanup used normal Exit preview, verified MAIN and cart 0, and closed the audit tab before releasing the shared browser session to Merchant.

## Buyer result

The exact Together Heart link with variant 46512190292065 immediately selected Adult / 4XL / Green and displayed USD 26.99 in DLM UX Performance QA 2026-09-10, theme 137888792673. No size or color click was needed. One click on the main Add button placed that exact variant in the cart, quantity 1, total USD 26.99. Only the audit line was removed; cart 0 and no cart rows were verified. A fresh reload at 1280 by 720 retained the linked selection and enabled Add.

Parent independently observed the same preview success, then used normal Exit preview and reproduced MAIN's missing custom size/color selection and disabled Pick a size. MAIN's underlying variant inputs and the exact InStock / USD 26.99 JSON-LD remained correct. Parent receipt: ../../2026-09-05-ceo-turnaround/public_landing_diagnosis_20260911/public_readback.json.

## Exact source and provenance

Fresh full-file readback at 2026-09-11 16:06:45 UTC confirms all 527 candidate files match the local reviewed candidate. Candidate, MAIN's 525 files and the predecessor's 527 files have zero checksum changes since the V6 receipt. The candidate is still UNPUBLISHED; MAIN and predecessor roles remain unchanged.

MAIN snippets/product-desktop-ux.liquid omits selected_variant_id after currency. The predecessor and current candidate emit product.selected_variant.id at line 182. Candidate assets/product-desktop-ux-20260513-ruler-sync.js resolves that ID at 2495, seeds the variant's options at 3538 and initializes role, size, color axes and purchasable ID at 3617. This existing mechanism predates V6 and is present in the predecessor rollback. The unrelated section-level first-available variant field is not the matching-set input being repaired.

The two fresh Liquid bodies match API MD5/size receipts. The predecessor JavaScript rollback matches its fresh API checksum. Independent source review PASS; reviewer did not build or execute the repair. Full MAIN JavaScript text was not returned by the requested Text union branch, so a complete MAIN JavaScript reconstruction is not claimed.

No further patch is justified by this evidence. V6 remains the one combined release: 16 changes / 511 preserved from its predecessor, 59 differences from MAIN. No clone, reapplication, manifest revision or rollback change.

## Limits and separate findings

- This follow-up verifies the sampled available variant and a normal reload. Mobile was not rerun because this follow-up changed no source; prior V6 mobile checks retain their original date.
- No fresh full Theme Check or 42-test suite was needed for zero source changes. Existing V6 results remain dated evidence; current full-file hash binding verifies unchanged code.
- Google account-level website restriction and its requested review are separate. This sample does not establish that the picker caused the restriction or that publication will clear it.
- Parent separately owns five extreme Minimalist Heart source prices. That source problem is not repaired by this theme and must not be hidden with a theme patch.
- Amazon Pay acceptance, broader localization, published buyer behavior, valid released-theme PageSpeed scores and conversion lift remain open.

## Next owner action

Publish the existing reviewed combined theme through Shopify Admin after an action-time source/conflict check. This brings the verified repairs to shoppers; preserve the current MAIN for rollback. The Shopify connector blocks publication and MAIN writes.

Continuation prompt: Continue from the existing UX packet and the September 11 variant-link verification. Confirm current published theme identity and source before any release or buyer claims. After owner publication, replay the exact variant link and affected buyer flows, then run desktop/mobile PageSpeed bound to the released theme. Preserve Merchant/Pinterest ownership and the separate source-price correction.

## Shared-record update status

Automatic approval review rejected the proposed cross-file coordination, problem, marketing, queue and worklog updates as exceeding website-audit authorization and risking shared-state corruption. The temporary script was not created and no shared edit ran; the proposed anchor is absent from all six shared records. The canonical interval was released to parent. This packet remains the evidence receipt; no alternate writer was asked to execute the rejected plan.
