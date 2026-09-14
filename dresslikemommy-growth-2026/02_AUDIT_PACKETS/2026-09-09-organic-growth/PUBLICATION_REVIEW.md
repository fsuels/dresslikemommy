# Review the exact family-photo guide update
**Status: prepared locally; not applied.** No store field, public page, PDF upload or social post was changed.

Target: [What to Wear for Family Photos: Matching Outfit Ideas](https://www.dresslikemommy.com/blogs/news/what-to-wear-for-family-photos-matching-outfit-ideas), Shopify article **559471919201**, currently published. One source-body-only update. [Read the new section](article-insertion.html) or [full proposed body](article-body-proposed.html).

## What changes
1. Add one practical buying section after the two opening paragraphs: each person's piece, size, quantity, owned clothes, current delivery estimate and final comfort check.
2. Include direct links to the currently verified Rainbow and Pastel Bloom mother-daughter dresses. State that each dress is sold separately. Do not add fabric, measurements, sale, stock, customer-review or fast-shipping promises.
3. Replace the existing fixed “Plan outfits 2 weeks ahead” advice with checking the estimate for the shopper's destination and allowing time to try outfits on.

Everything else in the existing source body is byte-preserved. Title, handle, summary, tags, template and publication settings are omitted from the mutation and must be read back unchanged. updatedAt necessarily changes. Metadata is outside this release.

## Localization scope
A fresh read found **17 existing body translations**, 19 title translations, all currently outdated=false. Polish/Russian have title-only translations; Swedish has none in the requested set. This is an English-source pilot: it does not update the 17 translated bodies. Their outdated flags may change, and routes using source fallback may display the new English section. Do not report localization complete. Refresh the relevant body translations through the owning localization workflow before expanding this content campaign to those languages.

The source readback preserved in [article-before.json](article-before.json) is bound to the new body and rollback in verification.json. Fresh re-read immediately before a future write is mandatory: if any selected source/preservation field or coordination claim changed, stop and rebase the exact diff.

## Ready materials
- Schema-validated [operation](article-update.graphql), [exact variables](article-update-variables.json) and [rollback variables](article-rollback-variables.json).
- Current source, product facts, translation-impact readback and desktop/mobile buyer observations in this packet.
- The printable planner at output/pdf/family-photo-outfit-planner.pdf is separate. Its two shopping links work as document links, but the PDF has not been uploaded. This article proposal does not contain a missing PDF URL or depend on upload.
- Six Pin copy drafts require the current Pinterest owner's separate artwork, account and publishing checks. No customer or photographer send is included.

## Proposed authorization
“Publish the reviewed source-body update to the existing family-photo article 559471919201, including the buying section and delivery-planning correction. Preserve its URL and other fields. This covers the English source and its existing fallback behavior; no translated-body rewrite, PDF upload, other post, email, outreach or spend.”

Root must confirm the current article claim before execution. This request is separate from already-authorized DA/NL and Sunshine work and does not ask for their approval again. [Project AGENTS.md](../../../AGENTS.md) requires exact authority before external Save/Publish actions. [Marketing AGENTS.md](../../../ops/marketing/AGENTS.md) explicitly requires fresh approval for Shopify customer-visible data; this is a new source-body change outside the existing reviewed releases. [VISION.md](../../../VISION.md) supports preparing bounded artifacts before live-risk writes.

## Readback and rollback
After one approved mutation, check userErrors=[], exact source-body equality, title/handle/summary/tags/template/publication preservation and translation status. Verify the article at desktop/mobile; click its two new product links, check the intended language, current wearer options and separate-piece disclosure. No purchase is required. Log publication separately from measured traffic/sales.

Rollback, if needed and approved: use the same operation with article-rollback-variables.json only while the current body equals this packet's proposed body. If another writer changed the article, do not overwrite it. Read back restored source and affected translation flags. Restoring source may change outdated flags; do not promise restoration of timestamps/flags without readback.

Independent review: review.md. Artifact checks: verification.json. Approval is the remaining authority step; the fresh pre-write/readback checks are execution safeguards, not a new design task.

