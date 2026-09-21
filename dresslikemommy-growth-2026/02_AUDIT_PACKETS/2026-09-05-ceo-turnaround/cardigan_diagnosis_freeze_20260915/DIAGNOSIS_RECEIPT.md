# Cardigan fit-guide diagnosis — September 14, 2026

Status: VERIFIED defect; repair PROPOSED ONLY. This packet records a read-only investigation, not a theme release.

At 2026-09-15T00:48:48.832Z, the public Navy Sprig product showed Cardigan selected while the reopened Mother fit panel displayed the Dress measurements. Mother S showed bust 84 cm and garment length 114 cm; the original Cardigan table in the same page contained bust 80 cm, sleeve 56 cm and garment length 40 cm. No product measurements were changed.

## Reproduction and evidence

1. Opened the existing English product in a task-owned background tab, inheriting Canada/CAD and an empty cart.
2. Opened Mother fit, selected Cardigan, and reopened Mother fit.
3. Read back Cardigan aria-pressed=true; the fit trigger's garment key was empty. The separate native Type selector remained Dress.
4. Captured the visible Dress headers and rows, the intact original Cardigan rows, and a screenshot. The builder also continued to display the Dress helper label.

See browser-cardigan-open.json, browser-cardigan-open.png and the browser accessibility records. Browser warning/error entries were zero. No country, cart, checkout, product or theme writes occurred. The temporary tab was closed.

## Source diagnosis

The independently inspected MAIN and candidate modules share the relevant routing functions. The garment classifier does not recognize Cardigan. An empty garment key skips the direct original-table lookup and falls back to cached groups selected through the native Type control, which still says Dress.

The compact measurement tooltip is not proof of correct garment routing: the unrecognized Cardigan table becomes an untyped lookup entry. Its apparent success must be tested separately from the inline fit panel.

The proposed narrow repair is to recognize the actual Cardigan type and chart context, retain instance-specific selection, and derive the displayed garment helper from that selection. Preserve all original chart values, product data and variant identities. The detailed source report and regression matrix are in source/.

## Verification limits

The live mismatch was reproduced on desktop. The source specialist's 24 synthetic cases verify the diagnosis and a bounded in-memory classifier proposal across the current MAIN and candidate; they are not browser acceptance of an implemented repair. No production source or project test file was edited. Before any candidate release, verify Mother/Girl, Dress/Cardigan, both unit modes, switching selections, unselected Type, tooltip consistency, original measurement preservation and affected desktop/mobile/localized flows.

## Main synchronization remains partial

A fresh remote read still reports GitHub main e077c69e06bbc729da121533a480c55456b079ba; local main is 4203184e6937167281ed41d8014d30f4652b0c63. All 72 pending theme-file differences are committed locally, with no uncommitted theme changes. Later work by other active tasks is preserved.

Shopify still reports 133290917985 as MAIN and 137888792673 as UNPUBLISHED, with neither processing nor failed processing. The established publishing/MAIN-write connector restriction still applies. No Git or browser workaround was attempted.

Next action: prepare and independently verify the smallest Cardigan theme repair before renewing candidate buyer acceptance. The parent task owns shared canonical integration and any exact successor release decision. Keep the owner Admin publication dependency and the pending main synchronization explicit.

Continuation: Prepare the minimal instance-specific Cardigan fit-guide and garment-label repair from this frozen diagnosis, preserving measurements and variants; review and test it before any separately scoped candidate upload. Do not bypass the existing MAIN or publication restriction.


Project strict continuity verification also passed during closeout. A repair must additionally fail safely for missing, ambiguous or unmatched garment charts; the existing fallback behavior is not certified by the positive synthetic cases.
