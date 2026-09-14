# Tracking Pixel Loop

Use this loop for Shopify Customer Events pixels, GA4, Google Ads conversion tracking, consent behavior, checkout-completed measurement, or tracking setup docs.

## Read First

1. `AGENTS.md`
2. `VISION.md`
3. `pixels/README.md`
4. `docs/tracking-setup.md`
5. `ops/marketing/AGENTS.md` if paid-growth reporting or conversion goals are involved
6. Relevant measurement entries in `ops/PROBLEM_TRACKER.md`

## Safety Defaults

- Pixel code may contain placeholders, but real API secrets, conversion labels, click IDs, checkout tokens, emails, phones, addresses, and raw conversion URLs must not be committed or pasted into evidence.
- Replacing placeholders with live values happens only in the Shopify Customer Events editor or another owner-approved secure surface.
- Do not place a real test order, refund an order, change conversion goals, or change attribution settings without exact owner approval.
- Do not disable the Google & YouTube sales channel as a shortcut; it can affect Merchant feed continuity.

## Validate Static Changes

For pixel JavaScript changes, run syntax checks on touched files:

```bash
node --check pixels/ga4-custom-pixel.js
node --check pixels/google-ads-custom-pixel.js
git diff --check
```

If a tracking doc or script names a live account/conversion state, label it as repo-known, live-verified, or live-readback-required.

## Browser And Live Readbacks

Use the browser only inside the approved scope:

- Product page event dispatch, add-to-cart event, checkout-start event, and checkout-completed event are distinct gates.
- Stop before payment unless the owner explicitly approves a real test order.
- Debug logs must be redacted before they enter repo evidence.
- GA4/Ads readbacks need timestamps, property/account IDs when visible, and whether the result is current live proof or expected lag.

## Done

The loop is done when static checks pass, secret placeholders are not committed with live values, consent and dedup assumptions are documented, and any external tracking claim has a fresh readback or is marked as unverified.
