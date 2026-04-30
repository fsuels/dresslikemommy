# PSI API Attempt

The scalable PageSpeed Insights API path was attempted for the 424 default/canonical routes with mobile and desktop strategies. The API returned HTTP 429 RESOURCE_EXHAUSTED for the environment's default Google consumer project, with quota metadata showing `quota_limit_value: 0` for `pagespeedonline.googleapis.com/default`.

Because every attempted API row returned the same quota failure, the run was treated as blocked and the measurement path switched to:

- official `pagespeed.web.dev` UI captures for the representative route set
- local Lighthouse JSON/HTML reports for the same representative route set
- browser screenshots plus console/network/image/overflow checks

A Google PSI API key/quota is required before running the full 424 canonical route x mobile/desktop PSI JSON batch.
