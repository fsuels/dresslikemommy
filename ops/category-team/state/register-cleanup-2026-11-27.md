# Register cleanup 2026-11-27 (de Sie, ro polite plural)
Owner: UI strings (theme). Full list: `ops/organic/receipts/2026-11-27/register-cleanup/proposed.json` ({locale: {key: {old, new, round}}}; inline keys are `file::label`, old/new joined by " | " when several edits).

## Counts (rewritten and released)
| | locale-file keys | hard-coded (theme files) | total | rounds |
|---|---|---|---|---|
| de | 47 | 7 | 54 | 3 |
| ro | 93 | 27 | 120 (cap 120) | 5 |

German: all informal and slang strings found are in the list (du/dein, Entdecke, Nutze, Verwende, "shoppen", ihr-form in the Christmas guide, Deine/deiner in the family list).
Romanian: 51 more informal strings were found than the 120 cap allows; the least visible are NOT released (list below).

## Wording rules used
Neutral forms where natural for buttons ("Mehr aus X entdecken", "Neuheiten entdecken", "Vedeți tot"); Sie/Ihr and dvs. elsewhere; cart, checkout and shipping wording not touched (already reviewed in V55). "shoppen" replaced by "entdecken" or "stöbern"; Romanian "Vezi tot" is "Vedeți tot". No new claims.

## Left (not released)
Romanian, over the 120 cap (account pages, gift card, aria labels): accessibility.close, accessibility.skip_to_text, accessibility.skip_to_product_info, general.share.close, general.share.copy_to_clipboard, general.slider.next_slide, general.slider.previous_slide, sections.video.load_video, sections.slideshow.load_slide, sections.slideshow.play_slideshow, general.social.alt_text.share_on_facebook, general.social.alt_text.share_on_twitter, general.social.alt_text.share_on_pinterest, localization.update_language, localization.update_country, templates.search.no_results, templates.search.search_for, blogs.article.read_more_title, blogs.article.comment_form_title, blogs.article.post, blogs.article.share, general.password_page.login_form_password_placeholder, general.password_page.admin_link_html, customer.account.view_addresses, customer.activate_account.title, customer.activate_account.subtext, customer.activate_account.password_confirm, customer.activate_account.submit, customer.activate_account.cancel, customer.addresses.add_new, customer.addresses.edit_address, customer.addresses.set_default, customer.addresses.add, customer.addresses.update, customer.addresses.cancel, customer.addresses.edit, customer.addresses.delete, customer.order.track_shipment, customer.register.title, customer.register.submit, customer.reset_password.title, customer.reset_password.password_confirm, customer.reset_password.submit, gift_cards.issued.how_to_use_gift_card, gift_cards.issued.title, gift_cards.issued.subtext, gift_cards.issued.shop_link, gift_cards.issued.add_to_apple_wallet, gift_cards.issued.qr_image_alt, gift_cards.issued.copy_code, recipient.form.send_on_label.
Outside the theme (needs Admin translation write, not theme): footer newsletter heading "Get 10% off your first order" (sections/footer-group.json setting; the Romanian "Primește…" text lives in Shopify translations); menu link titles if they are Admin translated.
Not touched on purpose: `locales/it.json`, `locales/ro-RO.json` (not used: the copy map reads the language root `ro`), Romanian SEO body prose that is third person.
