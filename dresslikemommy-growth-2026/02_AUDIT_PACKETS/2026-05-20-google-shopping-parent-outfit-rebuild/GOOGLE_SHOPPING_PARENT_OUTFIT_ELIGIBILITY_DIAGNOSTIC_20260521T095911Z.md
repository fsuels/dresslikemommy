# Google Shopping Parent-Outfit Eligibility Diagnostic

UTC timestamp: `20260521T095911Z`

## Verdict

- Diagnostic mode: read-only.
- Activation allowed: `false`.
- Feed/product/campaign writes performed: `false`.

## Gate Result

- Expected rows: `4531`
- Google Ads present expected rows: `4460`
- Google Ads missing expected rows: `71`
- Ready-label rows: `4390`
- Present non-ready-label rows: `70`
- Raw Ads rows returned for expected IDs: `8852`
- Status counts: `{'NOT_ELIGIBLE': 4460}`
- Availability counts: `{'IN_STOCK': 4440, 'OUT_OF_STOCK': 20}`

## Issue Diagnosis

- Hard error counts: `{'not_eligible_in_any_campaign': 4460, 'not_eligible_out_of_stock': 20}`
- Issue severity counts: `{'WARNING': 3430, 'ERROR': 4480}`
- Attribute issue counts: `{'age group|missing_item_attribute_for_product_type': 2031, 'color|missing_item_attribute_for_product_type': 1049, 'gender|missing_item_attribute_for_product_type': 343, 'size|missing_item_attribute_for_product_type': 7}`

Interpretation:

- The ready-label rows are not failing because of label or image mismatch.
- Their main Ads hard error is `not_eligible_in_any_campaign`, which is expected while every parent-outfit Shopping campaign is intentionally paused.
- The still-real blocker is source matching/readiness for the expected scope: some expected offer IDs are absent from Google Ads Shopping-product and some are present without the approved ready label, while Merchant source `10663204023` reports `139` unmatched offers after the approved TSV refresh.

## Parent Scope

- Expected parent counts by lane: `{'daddy_and_me': 34, 'family_matching': 77, 'mommy_and_me': 99}`
- Ready parent counts by lane: `{'daddy_and_me': 34, 'family_matching': 77, 'mommy_and_me': 92}`
- Missing parent counts by lane: `{'mommy_and_me': 4}`
- Present non-ready parent counts by lane: `{'mommy_and_me': 5}`
- Missing parent rows: `[{'parent_product_id': '7562834215009', 'handle': 'white-crochet-mommy-and-me-set', 'lane': 'mommy_and_me', 'missing_variants': 35}, {'parent_product_id': '6718945034337', 'handle': 'mom-child-matching-two-piece-swimsuit', 'lane': 'mommy_and_me', 'missing_variants': 20}, {'parent_product_id': '6719774720097', 'handle': 'matching-mommy-me-orange-print-swimsuit', 'lane': 'mommy_and_me', 'missing_variants': 10}, {'parent_product_id': '7227254276193', 'handle': 'mommy-and-me-matching-yellow-sleeveless-maxi-dress-vibrant-summer-beach-dress-for-mother-daughter', 'lane': 'mommy_and_me', 'missing_variants': 6}]`
- Present non-ready parent rows: `[{'parent_product_id': '6718948147297', 'handle': 'matching-mom-child-one-shoulder-swimsuit', 'lane': 'mommy_and_me', 'present_non_ready_variants': 40}, {'parent_product_id': '6719764463713', 'handle': 'matching-mommy-and-me-hollow-out-bikini', 'lane': 'mommy_and_me', 'present_non_ready_variants': 10}, {'parent_product_id': '6719792873569', 'handle': 'matching-mommy-me-sunflower-print-swimsuit', 'lane': 'mommy_and_me', 'present_non_ready_variants': 10}, {'parent_product_id': '7535944368225', 'handle': 'powder-blue-mommy-and-me-set', 'lane': 'mommy_and_me', 'present_non_ready_variants': 8}, {'parent_product_id': '7227254276193', 'handle': 'mommy-and-me-matching-yellow-sleeveless-maxi-dress-vibrant-summer-beach-dress-for-mother-daughter', 'lane': 'mommy_and_me', 'present_non_ready_variants': 2}]`

## Shopify / Google & YouTube Readback

- Diagnostic parent product IDs checked: `['6718945034337', '6718948147297', '6719764463713', '6719774720097', '6719792873569', '7227254276193', '7535944368225', '7562834215009']`
- Missing parent Shopify summary: `{'6718945034337': {'found': True, 'handle': 'mom-child-matching-two-piece-swimsuit', 'status': 'ACTIVE', 'google_published': True, 'feedback_summary': None, 'feedback_messages': []}, '6718948147297': {'found': True, 'handle': 'matching-mom-child-one-shoulder-swimsuit', 'status': 'ACTIVE', 'google_published': True, 'feedback_summary': None, 'feedback_messages': []}, '6719764463713': {'found': True, 'handle': 'matching-mommy-and-me-hollow-out-bikini', 'status': 'ACTIVE', 'google_published': True, 'feedback_summary': None, 'feedback_messages': []}, '6719774720097': {'found': True, 'handle': 'matching-mommy-me-orange-print-swimsuit', 'status': 'ACTIVE', 'google_published': True, 'feedback_summary': None, 'feedback_messages': []}, '6719792873569': {'found': True, 'handle': 'matching-mommy-me-sunflower-print-swimsuit', 'status': 'ACTIVE', 'google_published': True, 'feedback_summary': None, 'feedback_messages': []}, '7227254276193': {'found': True, 'handle': 'mommy-and-me-matching-yellow-sleeveless-maxi-dress-vibrant-summer-beach-dress-for-mother-daughter', 'status': 'ACTIVE', 'google_published': True, 'feedback_summary': None, 'feedback_messages': []}, '7535944368225': {'found': True, 'handle': 'powder-blue-mommy-and-me-set', 'status': 'ACTIVE', 'google_published': True, 'feedback_summary': None, 'feedback_messages': []}, '7562834215009': {'found': True, 'handle': 'white-crochet-mommy-and-me-set', 'status': 'ACTIVE', 'google_published': True, 'feedback_summary': None, 'feedback_messages': []}}`
- Shopify feedback message counts: `{}`

## Merchant Scope Readback

- Merchant Content API scope available: `False`
- Merchant Content API scope probe: `{'available': False, 'error_type': 'RefreshError', 'message': "('invalid_scope: Bad Request', {'error': 'invalid_scope', 'error_description': 'Bad Request'})"}`
- Authenticated Merchant source readback for `10663204023` remains the current source-level proof: `4,531` total updated products, `4,392` matched products, all attributes recognized, `139` `Offer does not exist` rows.

## Decision

The safest next move is not another upload, Shopify resync, or broad Google & YouTube sync. The smallest exact action packet should either exclude the unresolved Mommy & Me parent products from the activation scope, or get fresh owner approval for a deeper Google & YouTube/Merchant product-status repair if a human control surface exposes an exact per-product repair. I recommend the exclusion packet first because the present ready-label rows already have clean labels/images and the unresolved rows have resisted the narrow publication, attribute, and supplemental-refresh repairs.

## Output Files

- JSON: `google_shopping_parent_outfit_eligibility_diagnostic_20260521T095911Z.json`
- Present rows CSV: `google_shopping_parent_outfit_eligibility_present_rows_20260521T095911Z.csv`
- Missing rows CSV: `google_shopping_parent_outfit_eligibility_missing_rows_20260521T095911Z.csv`
