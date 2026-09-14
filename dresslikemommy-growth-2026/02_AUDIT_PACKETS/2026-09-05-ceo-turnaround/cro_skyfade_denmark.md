# Skyfade Denmark / Danish candidate readback

Confidence: H for observed UI; **TA-10 LAUNCH BLOCKER — LOCALIZATION REPAIR REQUIRED**, not paid-traffic clearance. Readback completed 2026-09-05 by 22:57 UTC.

Product `7536992976993`, **Skyfade Family Matching Set - Dress & Shirt**, handle `skyfade-family-matching-set`; parent’s current Shopify aggregate reports `ACTIVE`. Chrome test tab `475224132`; theme `133290917985`, `dresslikemommy/main`, role `main` as reconciled in the preceding audit.

Route observed through shopper controls: US product → mobile Menu → country selector → `Denmark DKK kr.` → footer language → `Dansk`. Final URL: **https://www.dresslikemommy.com/da/products/skyfade-family-matching-set**; DOM language `da`; SEO title `Skyfade familie matchende sæt | Klæd dig som mor – Dress Like Mommy`. Requested viewport `390×844`; actual DOM viewport **433×937**. Screenshot: `cro_skyfade_denmark.png`.

**What works:**

- US price range `$19.99–$29.99 USD` changes to **131,00–196,00 DKK** for Denmark. Danish product title, role buttons `Mor/Far/Pige/Dreng`, color buttons `Blå/Lilla`, and separate-piece explanation render.
- Selected **Mor / S / Blå**, labeled `Kjole`, produces **196,00 kr.** and an enabled add-to-bag button. No item was added.
- Sizing panel opens with cm/in controls and Danish measurement labels. Observed Mother S values: weight `43–48 kg`, height `155–160 cm`, chest `84 cm`, skirt length `100 cm`. This validates display, not supplier measurement truth.
- Delivery wording says **“Forventet levering til Danmark: 17. september - 21. september”**, standard shipping included, and 30-day returns/exchanges. Actual delivery performance and complete address-specific rates were not tested.
- Cart button opens a Danish empty-cart drawer and confirms Denmark selected. No checkout was started.

**Verified blockers/friction:**

1. Under current visible title `Skyfade familie matchende sæt - kjole og skjorte`, the Danish body’s **Stof** bullet reads exactly: `Letvægtsvævet stof med en flydende, strandklar afdækning; det nøjagtige fiberindhold var ikke synligt fra den blokerede leverandørside.` The latter clause says the exact fiber content was not visible from the blocked supplier page. Current English description differs. **TA-10 blocks Danish launch.** Proposed minimal omission: delete only the internal clause beginning `; det nøjagtige fiberindhold` through `leverandørside`, terminating the retained sentence with a period. Add no fiber, material, care, or delivery assertion. Root must bind the body translation mutation to this exact product, locale, and current source digest before any write.
2. Purchase flow still shows `Choose who this piece is for`, `Choose size and options`, `Ready to add`, and **`Add this piece to bag`** in English. Both lower size-chart headings remain English.
3. Footer displays `sektioner.fodtekst_overskrifter.firma_info` and `Translation missing: da.sections.footer_headings.kundeservice`.
4. Danish cart’s recently viewed Skyfade card displays **`$131.0`** and links to the unlocalized `/products/skyfade-family-matching-set`; the current Denmark product range uses DKK. Previously viewed US products also retain cached dollar prices. This panel is not market-safe.
5. Product colors say `Lilla`/Purple while description describes lavender; obtain color/photo truth before changing either term.

**Next action:** root prepares exact TA-10 Skyfade Danish body omission, shared Danish purchase/footer repair, and market-aware recently viewed rendering; independently repeat this route before ads. No live translations touched. The historical May Denmark checkout pass is not current clearance.

Only this report and screenshot were written. No Admin/theme write, HTTP bulk scan, cart mutation, customer data, payment, or order. Restored English homepage, US/USD, empty cart, viewport override reset; final DOM viewport `2133×1200`. Continue through the canonical paid-growth continuation prompt with this candidate held.
