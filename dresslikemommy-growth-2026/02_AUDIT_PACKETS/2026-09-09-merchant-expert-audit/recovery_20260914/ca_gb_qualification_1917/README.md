# Canada and UK source and buyer qualification

Action: TA07-CA-GB-QUALIFY-20260914-1917. Account: Google Merchant513542500. Shopify:15571635.

Both full Shopify scans completed on September14,2026. Canada completed at19:22:54UTC; UK at19:25:28UTC. Each scan contains238 active parents and4,925 variants, with all native prices and currencies checked. The source-only partition is4,741 candidates,22 unavailable variants excluded, and162 available variants under the same six existing product holds. Candidate counts do not establish eligibility or approval in Google.

| Country | Currency | Source candidates | Price changes vs stale September11 file |
| --- | --- | ---: | ---: |
| Canada | CAD | 4,741 | 350 |
| United Kingdom | GBP | 4,741 | 1,084 |

Both comparisons retain4,741 existing IDs and remove20; neither adds an ID. No feed file was produced or uploaded. Configurations remain disabled with landingContextVerified=false.

The Canada numeric variant URL failed to select the intended child variant on the published theme. After manual selection, the cart carried exactly the intended variant at26CAD. The same anonymous checkout repriced to14GBP after switching to the UK. Free Standard Shipping was offered for both public test destinations; neither displayed a delivery estimate. No contact, name, phone, or payment details were entered and no order was placed. The test destination fields were cleared, the country restored to the US, and the sole temporary item removed; final cart0 was verified.

Merchant currently configures Canada at5–6days and UK at9–15days, while the Canadian product page displayed September26–30. Those values are observed configuration, not verified supplier transit commitments. The owner was asked once for reliable transit ranges; an answer remains pending.

The separate UX owner supplied fresh evidence that both exact Spanish variant URLs pass in reviewed draft theme137888792673. The Shopify connector blocks theme publishing and MAIN writes, so the existing owner publication step remains required. That draft evidence does not certify the current published theme or Canada/UK routes. Recheck those routes after publication, refresh source if it has become stale, then create and verify exact country sources.

Authoritative evidence: source_and_buyer_qualification.json, both source_receipt.json files, source snapshots, source partitions, and deltas in this directory. The six original holds, US/AU sources, paid settings, and live theme were unchanged by this work.
