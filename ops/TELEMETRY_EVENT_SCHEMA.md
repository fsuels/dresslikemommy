# CRO-01: Telemetry Event Schema Documentation

## Overview
This document outlines the event measurement layer for DressLikeMommy, covering ecommerce funnel tracking, errors, and key micro-conversions. All events are pushed to Google Analytics 4 (GA4) via the dataLayer.

## Event Categories

### 1. Ecommerce Core Events (GA4 Standard)
These events follow GA4 ecommerce conventions and are pre-existing.

**view_item**
- Fired when: Product page loads
- Payload: `ecommerce` object with item details
- Dedupe: `viewItemPushed` flag (fires once per page load)

**view_item_list**
- Fired when: Product card enters viewport (40%+ visible)
- Payload: `ecommerce` object with item_list_id, item_list_name, and item
- Dedupe: `viewedListKeys` map prevents duplicate views per product+list combo

**select_item**
- Fired when: User clicks product card link
- Payload: `ecommerce` object with item_list_id, item_list_name, and item

**add_to_cart**
- Fired when: User adds product to cart (from product form)
- Source: PUB_SUB_EVENTS.cartUpdate event with source='product-form'
- Payload: `ecommerce` object with item details and quantity

**view_cart**
- Fired when: User views /cart page or opens cart drawer
- Payload: `ecommerce` object with all cart items
- Context: `cart_context` field = 'cart_page' or 'cart_drawer'
- Dedupe: `lastViewCartSignature` prevents repeat fires for same cart state

**remove_from_cart**
- Fired when: User decreases quantity or removes item from cart
- Payload: `ecommerce` object with removed item and quantity delta

**begin_checkout**
- Fired when: User clicks checkout button
- Payload: `ecommerce` object with cart items
- Source: `checkout_source` field captures button ID/form/class
- Dedupe: 400ms timestamp debounce prevents duplicate fires

### 2. Error Tracking Events

**cart_update_error**
- Fired when: Cart operation fails (from CRO-02 cart resilience improvements)
- Trigger: PUB_SUB_EVENTS.cartUpdate event with `errors` field
- Payload:
  - `event`: 'cart_update_error'
  - `error_message`: User-facing error message (non-PII)
  - `error_type`: Error category (e.g., 'inventory', 'unknown')
  - `source`: Source of update (e.g., 'cart-items', 'product-form')
- Notes: Helps identify cart friction points

**contact_form_error**
- Fired when: Contact form submission fails
- Trigger: Form error message visible on page load
- Payload:
  - `event`: 'contact_form_error'
  - `has_error`: true

### 3. Search Events (CRO-04 Search Page)

**search_submit**
- Fired when: User submits search form
- Trigger: Form submit event on search input
- Payload:
  - `event`: 'search_submit'
  - `search_term`: Query string (no PII)
- Dedupe: Fires on each form submit (natural dedupe via user action)

**search_no_results**
- Fired when: Search performed but returned zero product results
- Trigger: Automatic on /search page load if no results
- Payload:
  - `event`: 'search_no_results'
- Notes: Identifies search quality issues

**search_result_click**
- Fired when: User clicks product card from search results
- Trigger: Click on product link within search results
- Payload:
  - `event`: 'search_result_click'
  - `item_id`: Product/variant ID
  - `item_name`: Product title
  - `search_source`: 'search_page'

### 4. 404 Error Recovery Events (CRO-07)

**page_404_view**
- Fired when: User lands on 404 page
- Trigger: Automatic on page load at /404 path
- Payload:
  - `event`: 'page_404_view'
  - `page_path`: Full pathname that resulted in 404
- Notes: Monitors broken links and user navigation issues

**404_recovery_click**
- Fired when: User clicks recovery link on 404 page
- Trigger: Click on any link within 404 page
- Payload:
  - `event`: '404_recovery_click'
  - `recovery_link`: Target URL (href attribute)
- Options tracked: 'Continue Shopping', 'Browse Collections'

### 5. Contact Form Engagement

**contact_form_submit**
- Fired when: User submits contact form
- Trigger: Form submit event on #ContactForm
- Payload:
  - `event`: 'contact_form_submit'
- Notes: Baseline engagement metric

**contact_form_success**
- Fired when: Form submission completes successfully
- Trigger: Page displays success message
- Payload:
  - `event`: 'contact_form_success'
- Notes: Conversion-level metric for contact intent

### 6. Hero and Homepage CTAs

**hero_video_view**
- Fired when: Hero video enters 60%+ viewport visibility
- Payload:
  - `event`: 'hero_video_view'
  - `heroId`: 'family_fit'
  - `sectionId`: Section ID
- Dedupe: `viewed` flag fires once per page load

**homepage_cta_click**
- Fired when: User clicks any button with data-cta-id
- Payload:
  - `event`: 'homepage_cta_click'
  - `ctaId`: Button identifier
  - `ctaScope`: Scope of CTA (e.g., 'hero', '')
  - `ctaText`: Button text content
  - `destination`: Link target
  - `productHandle`: Associated product (if applicable)

**hero_cta_click**
- Fired when: User clicks CTA within hero scope
- Payload: Includes heroId, sectionId, ctaId, ctaText (subset of homepage_cta_click)

## Payload Principles

### Non-PII Data Only
- Never include: emails, phone numbers, customer IDs, addresses, IP addresses
- Error messages: Use generic/translated strings, not raw API responses
- Search terms: Include (no PII, useful for search quality)

### Consistency with GA4 Conventions
- Item IDs use product/variant IDs (non-PII)
- Prices in decimal format (e.g., 29.99, not 2999)
- Currency always included in ecommerce payloads
- Categories use custom taxonomy fields (item_category through item_category5)

### Experiment Context (Automatic)
All events include experiment flags if `window.experimentConfig` is defined:
- `experiments_enabled`: boolean
- `experiment_flags`: array of active flag names

## Dedupe Protections

| Event | Dedupe Mechanism | Duration |
|-------|-----------------|----------|
| view_item | `viewItemPushed` flag | Per page load |
| view_item_list | `viewedListKeys` map (product+list) | Per page load |
| view_cart | `lastViewCartSignature` (cart content hash) | Per page load |
| begin_checkout | 400ms `lastCheckoutTimestamp` debounce | 400ms |
| hero_video_view | `viewed` flag per IntersectionObserver | Per page load |
| search_result_click (on search page) | Natural (one click per result) | Per interaction |

## Event Flow by Page Type

### Product Page
1. **page_load**: view_item (if product data available)
2. **scroll**: view_item_list (for related products)
3. **click**: select_item (product card clicks)
4. **form_submit**: add_to_cart (from product form)

### Search Page
1. **page_load**: search_no_results (if performed, no results)
2. **form_submit**: search_submit
3. **click**: search_result_click (product cards)

### Cart Page / Cart Drawer
1. **open_drawer**: view_cart (cart_drawer context)
2. **page_load**: view_cart (cart_page context)
3. **quantity_change**: remove_from_cart (if qty decreases)
4. **error**: cart_update_error (if update fails)
5. **checkout_click**: begin_checkout

### Contact Page
1. **page_load**: contact_form_error (if form has errors)
2. **form_submit**: contact_form_submit
3. **success_page**: contact_form_success

### 404 Page
1. **page_load**: page_404_view
2. **link_click**: 404_recovery_click

## Implementation Notes

- All events are pushed via `pushToDataLayer()` helper
- Event payloads include experiment context automatically via `getExperimentContext()`
- Error messages are normalized to prevent PII leakage
- High-frequency events (cart updates, search input) use debouncing/dedupe
- All code follows strict ECMA5 syntax (no arrow functions, template literals)
- Event names follow snake_case convention
- Timestamp debouncing prevents event spam on rapid interactions

## GA4 Configuration
Events are consumed by Google Analytics 4 which provides:
- Automatic user property assignment
- Session management
- Conversion tracking (via GA4 conversions)
- Custom event processing via GA4 Event configuration

## Testing & Validation
- Use browser DevTools to inspect window.dataLayer
- Confirm events fire in correct sequence during user flows
- Validate no PII is present in event payloads
- Check dedupe flags prevent duplicate events on rapid interactions
- Verify experiment context includes appropriate flags
