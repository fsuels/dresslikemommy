# Merchant automatic refresh activation

The cloud refresh implementation is complete locally and passed 77 tests. The reviewed deployment bundle is built. Production activation requires the exact dedicated-app access approval below and successful live checks; no app, credential binding, queue, or deployment was created in this packet.

The proposed **DLM Merchant Feed Reader** app belongs to `dresslikemommy-com.myshopify.com` (Shopify shop 15571635). It requests only `read_products`, `read_publications`, `read_markets`, `read_locales`, `read_translations`, and `read_metaobjects`. Its client ID and secret would be stored as encrypted secrets on the existing Cloudflare Worker **dlm-merchant-feed-worker**, in account `6b1df53f8a1ce4b5b5312f833a2cd966`. It would generate the existing US English feed hourly. The current broad Shopify Admin credential would remain on the Mac.

After activation, complete catalog reads would add eligible newly active variants and remove archived, deleted, unavailable, or unpublished variants from the next successful feed replacement. The six existing product holds remain. Incomplete reads, unsupported prices, invalid product data, ambiguous configuration, or failed authentication preserve the last valid file. Source age remains limited to 48 hours. Google's ingestion schedule remains separate from hourly hosted generation.

| Check | Result |
| --- | --- |
| Runtime regression suite | 77 passed, 0 failed |
| Token renewal | Renew before a 15-minute consumer could outlive its token |
| Cloud configuration | Two small variables reconstruct the exact reviewed configuration and six holds |
| Package | Wrangler 4.86.0 dry-run succeeded; no deployment |
| Existing Worker | Version `d117e959-0e32-44c6-a8e9-41d4821b73a7`, 100% traffic; no cron schedules |
| Existing bindings | Public feed configuration and R2 bucket only; no Shopify credential |
| Existing US pointer | 4,741 rows; source completed September 14 at 13:16:10.466 UTC |
| Public feed acceptance | One local GET returned HTTP 403; cause unknown, no bypass or retry |
| Real limited-token collection | Not run; new app has not been created |
| First cloud refresh and later scheduled refresh | Not run |

The owner decision authorizes creating and installing the exact read-only app, storing its client credentials at the named Worker, and activating the existing US feed's hourly refresh after the live checks pass. It does not authorize a paid plan, customer/order access, write scopes, or silently substituting another credential. Shopify's same-organization requirement must pass. Any owner login or installation step remains an interactive dependency.

Automatic approval review rejected the September 11 attempt to place the existing Shopify Admin token on Cloudflare because the credential destination and access change were not explicitly authorized. This package replaces that approach with a separate, narrowly scoped app. See the [exact activation plan](activation_plan.json).

Evidence: [local validation](integration_validation_final.json), [independent verification](../cloud_final_independent_review_2102/final-package-verification.json), [current deployment and settings](cloud_runtime_before_readback.json), and [current source pointer](cloud_before_readback.json). At activation, capture the then-current deployment and settings again. Rollback restores that captured read-only host and preserves a valid source pointer; it must not restore expired data or change unrelated Workers.

Use the exact reviewed `config.json`, split bindings, source hashes, and package from this packet. Do not run old activation scripts, default `config.example.json` instructions, or the old local lifecycle promoter: its frozen configuration guards predate this candidate. Do not relax those guards to force it to run.

Canada, UK, Spanish, and other markets remain separate release qualifications. This initial activation enables only `us-en` and does not certify all-market publication, free-listing exposure, traffic, or profit.

Primary technical references: [Shopify client credentials](https://shopify.dev/docs/apps/build/authentication-authorization/client-credentials-grant?lang=node), [Shopify access scopes](https://shopify.dev/docs/api/usage/access-scopes), and [Cloudflare Worker configuration APIs](https://developers.cloudflare.com/api/resources/workers/subresources/scripts/).
