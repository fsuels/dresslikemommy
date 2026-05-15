# Pinterest Exact Product-Group Unblock Packet

Generated: 2026-05-15 05:45 EDT

Mode: repo-local approval/build packet only. No Pinterest, Shopify, Merchant, Google Ads, GA4/GTM, tag, CAPI, catalog, feed, source, product, budget, bid, status, launch, publish, billing, or spend write occurred.

## Why This Exists

The approved Pinterest catalog sales launch reached a compliant CPC setup path, then stopped before publish because the live UI exposed only broad product groups. Broad groups would include products outside the refreshed active-clean whitelist.

This packet converts that blocker into the smallest exact approval/action surface: create or expose only exact product groups from existing feed attributes, then launch only after final review reconfirms the `333` clean scope, `$5/day` cap, and `$0.15` max CPC.

## Required Exact Groups

| Group | Feed filters | Variants | Products | Use |
|---|---|---:|---:|---|
| Mommy & Me | `custom_label_0=paid_eligible`; `custom_label_4=us_test_ready`; `custom_label_2=mommy_me` | 201 | 26 | Exact active-clean catalog sales group only |
| Family Matching | `custom_label_0=paid_eligible`; `custom_label_4=us_test_ready`; `custom_label_2=family_matching` | 103 | 7 | Exact active-clean catalog sales group only |
| Pajamas | `custom_label_0=paid_eligible`; `custom_label_4=us_test_ready`; `custom_label_2=pajamas` | 29 | 1 | Exact active-clean catalog sales group only |

## Father-Inclusive Probe

The current clean scope contains `43` father/dad/parent-themed variant rows across `4` products. These rows are proof candidates, not launch authority for a separate Daddy & Me group.

| Product ID | Current group | Variants | Product |
|---|---|---:|---|
| `7227624554593` | `family_matching` | 8 | Denim Button-Up Shirts Casual Unisex Jean Jackets f... |
| `7229124673633` | `family_matching` | 16 | Green and White Outfits Stylish Floral Print Family... |
| `7227620982881` | `family_matching` | 10 | Striped Fleece Hoodies Cozy Winter Pullover for Par... |
| `7227418738785` | `mommy_me` | 9 | Striped Cardigans Navy and Red Heart Embroidery Kni... |

## Row Quality Readback From Scope CSV

| Check | Passing rows |
|---|---:|
| Image status | 333 |
| Price status | 333 |
| Availability status | 333 |
| Shipping policy status | 333 |
| Return policy status | 333 |
| Public PDP source-clean status | 333 |

Held exclusions remain excluded: `9` variant rows across the public-source exclusion file.

## Approval Required

Exact phrase to unblock product-group creation/exposure:

`I approve creating/exposing exact Pinterest product groups for advertiser 549756244483 from existing feed attributes only: paid_eligible + us_test_ready split by Mommy & Me, Family Matching, Pajamas, and any active clean Daddy & Me/father-inclusive rows that pass the same gates, excluding the 9 held variants, with no catalog source/feed source/tag/CAPI/billing/Shopify product changes, then launch only if final review shows max $5/day and max $0.15 CPC.`

## Execution Checklist After Approval

1. Read back advertiser `549756244483`, account/domain, and current campaign count/spend before any write.
2. Create or expose exact groups only from existing feed attributes: `paid_eligible`, `us_test_ready`, and the named `custom_label_2` values.
3. Confirm each exact group count matches this packet or stop and record the mismatch.
4. Keep the `9` held variants excluded unless a separate approved cleanup/readback clears them.
5. Use `Catalog sales` + `Pin clicks` + `Custom` bidding because this is the known path that allows max CPC `$0.15`.
6. Final review before publish must confirm max `$5/day`, max `$0.15` CPC, exact product-group scope, and no catalog/source/feed/tag/CAPI/billing/Shopify mutation.
7. After publish, read back created object IDs, status, spend, serving, group counts, bid, budget, and no out-of-scope mutations.

## Stop Conditions

Stop before any save/publish if Pinterest requires broad groups, catalog/source/feed/tag/CAPI/billing changes, audience creation/edit, Performance+ bidding, CPC above `$0.15`, product rows outside the exact clean scope, account switch, permission, CAPTCHA, policy, or destructive confirmation.

## Decision

This is the closest Pinterest path to sales-moving execution. It avoids broad catalog waste, preserves the active-product/source-clean rule, and gives the owner one precise approval gate instead of another generic blocker.
