Confidence: H for the source diagnosis, now bound to the parent’s current French product and English article readbacks.

Fresh Shopify reads confirm MAIN **133290917985** and unpublished candidate **137888792673** are unchanged. Fourteen relevant candidate files match the reviewed 527-file source map; the local cart footer retains its separately preserved fix. No theme, product, article, Git, browser or canonical state was changed.

The article CTA inherits `.rte a` text color from `assets/base.css`, overriding `.button` while retaining its dark background. The same conflict exists in MAIN and the candidate. `sections/main-article.liquid:134,175–189` creates the button inside `.article-template__content.rte`; `assets/section-blog-post.css:612` currently sets only its display.

The smallest separate correction replaces that rule with a selector specific enough to beat both normal and hover prose-link rules:

```css
.article-template__content .article-cta-inline__button.button {
  display: inline-block;
  color: rgb(var(--color-button-text));
}
```

It preserves the theme’s button color token, destination, label, focus behavior and other links. Parent verification should check en/ar/nl normal, hover and keyboard focus on desktop and a narrow viewport, including actual computed colors and navigation.

All twelve French findings are reconciled in `SOURCE_DIAGNOSIS.json`:

| Findings | Exact source and proposed scope |
| --- | --- |
| CAFR-01–04: four prepared controls | MAIN’s French dictionary lacks the keys; the candidate/local `assets/product-desktop-ux-20260513-ruler-sync.js:526–530` has the approved values. Exact source-function checks pass for `fr` and `fr-CA`; preserve these values and dynamic role/size/price. |
| CAFR-05–06: “Maman size”, “Fille size” | One expression at the candidate module’s line 3293 appends English ` size`. Add one French `Taille pour {role}` label with the existing expression as other-language fallback. Preserve the dynamic role. |
| CAFR-07: “Hip (Cm)” | Product **7670609346657**, global French `body_html`, contains two `<th>Hip (cm/po)</th>` headers. Product owner should replace only `Hip` with `Hanches`, retaining units and all 260 data cells. The theme’s measurement `dt` rule also capitalizes `cm`; exact lowercase units require a separate French-scoped `text-transform: none` override. |
| CAFR-08–09: tax/shipping labels | `sections/main-cart-footer.liquid:141,146` and `snippets/cart-drawer.liquid:624,634,640`. Translate only the French text outputs; preserve the tax condition, policy body and controls. Keep the local footer’s additional fix. |
| CAFR-10: selector heading | Change both `locales/fr.json:197` and `snippets/product-page-copy-map.liquid:549` to “Créez votre ensemble assorti”. The second supplies runtime/sticky copy. |
| CAFR-11–12: size range and typo | Fresh global French product body confirms both exact strings; Canada has no overriding body. Existing Merchant/source owner retains these corrections and all 24 variants. |

Both theme templates reference the ruler-sync asset at `sections/main-product.liquid:933`; old mirrors are not the module referenced there. MAIN module SHA256 is `a2d55e4177b65213ebce2d842f0e8cbedaff486e9aee46bfc20b95c986e33024`; candidate/local is `3f830b1bd48153ee4ac429240928a2eb8316e95a436e3c53e8743d3d8c5bba20`. Fresh Shopify checksums bind both sources; no short-lived source URL was requested or saved.

Parent readback at 00:25 UTC confirms Canada/CAD, cart 0, `lang=fr`, the actual ruler-sync asset, two English instructions, “Maman size” and the stale heading twice. English article readbacks at 00:20–00:24 UTC confirm the same dark-on-dark CTA. `PARENT_RENDERED_BINDING.json` preserves these exact evidence bindings; ar/nl follow-up remains with the parent.

Next: parent reviews the separately scoped theme repair using these source/rendered bindings. Do not replay completed cart/checkout tests or touch Ads editor 2. Continue from `SOURCE_DIAGNOSIS.json`; its per-file hashes and exact source records provide the repair boundaries.
