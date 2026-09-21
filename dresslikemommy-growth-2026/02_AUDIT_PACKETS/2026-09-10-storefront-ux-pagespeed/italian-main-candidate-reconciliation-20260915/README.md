# Italian footer reconciliation and proposed correction

The two English picker instructions reported on the live Italian product page are already fixed in the accepted unpublished theme and local main commit `cb7ff3a`. A fresh Shopify read confirms all 527 accepted candidate file checksums and sizes. The actual MAIN page still renders both English instructions; the actual candidate renders both Italian instructions.

The accepted footer removes the three visible translation errors but falls back to generic menu titles. The candidate currently shows “Menù piè di pagina 1”, “Menù a piè di pagina 2” and “Menù a piè di pagina 3”. All nine menu links match the live page.

The local proposal changes two files only. It normalizes the three exact Italian heading-key aliases returned by Shopify into the existing canonical keys, and translates those three Italian locale values to “Informazioni sull'azienda”, “Aiuto e supporto” and “Servizio clienti”. This adds 555 bytes across `sections/footer.liquid` and `locales/it.json`. The other 525 candidate files, all menu links, forms, consent controls, picker and prior mobile-heading corrections are preserved. No new source files or dependencies are introduced into the theme.

Shopify's installed CLI checked complete 527-file baseline and proposed themes: both returned zero diagnostics and exit code 0. The skill wrapper could not start because its bundled theme-check dependency is absent; those original failures are retained. The exact diff has no whitespace diagnostics. An independent proposal review is stored in `review/` when complete. The proposed labels have not yet been uploaded or checked in the Shopify preview.

Before any accepted save, recheck the two before hashes and the complete candidate inventory. Save only the reviewed two-file successor to existing unpublished theme 137888792673, then independently read back both files and confirm all 525 others are unchanged. Verify all three labels, both Italian picker steps and nine menu links at desktop and narrow widths. The two original files in `proposal/before/` are the exact rollback material.

The paired browser check used one task-owned background tab, Italian language with United States/USD and an empty cart. It does not qualify Italy/EUR, cookie-independent locale entry, variants, cart or checkout. Preview was exited through the native control, actual MAIN 133290917985 was confirmed, and the temporary tab was closed. No root theme file, Shopify file, product, menu, account, local main or remote Git branch was changed by this reconciliation.

Parent integration owns the canonical problem, claim and worklog. Publication and GitHub main synchronization retain the existing connector restriction and owner publication step; this proposal grants no release authority.
