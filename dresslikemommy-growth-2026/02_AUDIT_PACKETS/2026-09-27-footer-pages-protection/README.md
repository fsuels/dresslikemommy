# Footer pages redesign + business-protection copy (2026-09-27)

Owner request (chat): "improve every page of the footer make it look super beautiful, smart protection for the business. help me protect my interest in a smart way."

## What changed

### Theme (GitHub `main`, synced live and MD5-verified)
- `59ac5a9`, `20f958b`, `f47802f`
- `sections/main-page.liquid` gives every content page a hero, the help-hub pill navigation and a styled body card.
- New `snippets/dlm-help-hub-nav.liquid`. Labels come from the footer menus and `shop.policies`, so the existing translations apply.
- New `snippets/dlm-policy-hub.liquid`, rendered from `layout/theme.liquid` when `request.page_type == 'policy'`. It gives `/policies/*` the same navigation and styles.
- `assets/section-main-page.css` adds the `dlm-*` content components: lead, facts, steps, callouts, cards, FAQ accordions, tables, tracking form, buttons and CTA. It also restyles the contact form and the Shopify policy container.
- No new locale keys.

### Pages (Admin `pageUpdate`, token)
- New body and title for: about-us, shipping-info, return-policy, faqs, track-your-order, size-guide, contact-us, company-information.
- size-guide was empty before.
- track-your-order used to load a third-party 17track script. It is now a plain GET form to 17track.
- The legacy 2016 `terms-and-conditions` and `privacy-policy` pages had conflicting terms and an old support@ address. They are now short pointers to the canonical `/policies/*`.
- SEO `global.title_tag` and `global.description_tag` are set on the 8 help pages.

### Legal policies
- The Admin token and the MCP connector both lack `write_legal_policies`. The policies were saved in Shopify admin → Settings → Policies through the HTML editor, in the browser pane.
- Readback: the translatable-content value equals `after/policy-*.html` for all 5 (`verify_pol.py`: MATCH).
- Terms of Service rewrite. It adds:
  - Price-error cancellation, fraud verification, and quantity/reseller limits.
  - Promo-code rules and gift-card terms.
  - Address responsibility and refused-parcel handling, with the return cost disclosed.
  - Risk passing on delivery, and a 14-day delivered-not-received report window.
  - A chargeback process, IP and anti-scraping terms, and a UGC license.
  - Disclosure that some images are AI or edited.
  - A kids' small-parts warning.
  - Talk-first dispute resolution, Florida law with Collier County venue and small-claims carve-out, and individual claims.
  - A consumer-rights savings clause (EU/UK/AU) and an English-controls translation clause.
- Refund Policy: return authorization required first. Keep-it partial refund or credit option. Final Sale / hygiene / gift-card exclusions, carved out for defects. EU/UK withdrawal right with a model form. ACL clause.
- Shipping Policy: honest overseas-partner disclosure. Estimates are not guarantees. FTC mail-order delay notice with a cancel option. Lost-parcel trigger: 15 business days without movement or 30 days after shipping.
- Privacy Policy:
  - Removes "we will never sell" and states the US-state "sale/sharing" treatment of ad partners (Google, Microsoft, Pinterest, Meta), with an opt-out link and GPC.
  - Adds the newsletter financial-incentive notice, GDPR legal bases, and fulfillment-partner sharing and transfers.
- Contact information: the owner's personal name was replaced by the LLC. The mailing address is labelled "not a returns center".

### Security/privacy finding fixed
The Spanish translation of the privacy policy was publicly showing the owner's personal email address. That `es` translation was removed (live readback clean), and it is replaced by the new translation set.

### Translations
20 locales × 15 resources are generated from `after/source_en.json` and registered with `register_tr.py`. Status is in the worklog anchor.

## Review
An independent adversarial reviewer (subagent) found 5 must-fix and 8 should-fix items. All were applied before publishing. The main ones:
- A Florida §95.03-void 1-year claim limit was removed.
- "No middlemen" was removed.
- Delivery rules no longer depend on an unverified checkout estimate.
- The refused-parcel deduction was limited to the disclosed return cost.
- The defect carve-outs were added.
- GPC and consent wording was softened to what is verified.

## Rollback
- Pages: re-run `pageUpdate` with `before/pages.json` (title and body).
- SEO: restore `before/page_seo_metafields.json`. For pages without prior tags, delete `global.title_tag` and `global.description_tag`.
- Policies: paste `before/policies_rendered.json` bodies into Settings → Policies.
- Translations: re-register from `before/page_translations.json` and `before/policy_translations.json`. The redacted es privacy value must NOT be restored.
- Theme: revert `59ac5a9`, `20f958b` and `f47802f`.

## Not legal advice / owner follow-ups
- These texts were drafted for protection, not reviewed by a lawyer. Have a Florida e-commerce attorney review the Terms once.
- Product-level compliance outside this packet:
  - US "Imported" country-of-origin labelling on textile listings.
  - Children's sleepwear flammability rules (16 CFR 1615/1616: snug-fit or flame-resistant labelling) and CPSIA Children's Product Certificates for kids' items.
  - No drawstrings on kids' upper outerwear.
- UK VAT on orders of £135 or less is collected at checkout if the store is registered. Confirm the tax setup.
