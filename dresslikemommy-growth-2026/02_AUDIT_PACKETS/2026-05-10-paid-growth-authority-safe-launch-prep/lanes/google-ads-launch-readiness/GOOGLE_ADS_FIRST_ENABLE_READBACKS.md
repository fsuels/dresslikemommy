# Google Ads First Enable Readbacks

Date: 2026-05-10

These are the just-in-time readbacks required after the measurement gate is closed and before any first live click.

## Corrected Ad Group Name

The actual built/readback ad group is:

`Mommy & Me Dresses - Exact`

Older local runbook text used `Mommy & Me Dresses - Exact only`. That wording is now treated as a local documentation bug and must not be used for a live UI click.

## Required Pre-Enable Captures

Save all evidence under a new action packet before any enable:

- Campaign RPC/UI readback for `23838895360` showing `PAUSED`, Search, `$2/day`, Manual CPC, max CPC `$0.15`, GB presence-only, Search-only, content/YouTube off.
- Ad group readback showing `Mommy & Me Dresses - Exact` is `PAUSED`; all other ad groups are `PAUSED`.
- Keyword readback for that ad group showing exact-match only and final URLs with `?country=GB`.
- Ads/RSA readback showing claim-safe copy and no unsupported delivery, stock, sale, review, bestseller, or physical inventory claims.
- Conversion settings readback showing account-default purchases and no campaign-level override.
- Google Ads change-history check showing no unexpected recent budget/bid/status/conversion/product/feed changes.
- Storefront browser readback for the active final URL: product visible, GBP/GB presentment, add-to-cart and checkout entry without payment, no verification wall.

## Required Post-Enable Captures If The Enable Is Later Approved

Expected delta must be exactly:

- Campaign `23838895360`: `PAUSED` to `ENABLED`.
- Ad group `Mommy & Me Dresses - Exact`: `PAUSED` to `ENABLED`.
- All other ad groups: unchanged `PAUSED`.
- Budget, bid, geo, network, conversion goal: byte-identical to pre-readback.

Any other delta triggers immediate rollback and a problem-tracker entry.
