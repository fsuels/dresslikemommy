# Discount Disposition Review

Generated: 2026-04-29T02:39:50.655217+00:00
Store: `dresslikemommy-com.myshopify.com`
Mode: read-only. No Shopify discount changes were made.

## Summary

- `discount_nodes_total`: `125`
- `active_discount_count`: `94`
- `bucket_counts_all`: `{'CAP_OR_DISABLE': 7, 'DISABLE': 77, 'REVIEW': 8, 'KEEP': 2, 'NO_ACTION_INACTIVE': 31}`
- `bucket_counts_active`: `{'CAP_OR_DISABLE': 7, 'DISABLE': 77, 'REVIEW': 8, 'KEEP': 2}`
- `active_loox_like_count`: `67`
- `active_over_15_percent_count`: `8`

Active bucket counts:

- `CAP_OR_DISABLE`: `7`
- `DISABLE`: `77`
- `REVIEW`: `8`
- `KEEP`: `2`

## Required Owner Decisions

1. Approve or reject deactivation of `DISABLE` bucket codes. Suggested: approve Loox/test/unused open-ended codes after checking live automations.
2. Decide each `CAP_OR_DISABLE` code: deactivate, cap to 15%, or explicitly approve as an above-cap exception.
3. Decide `QP672`: keep as-is, add a minimum purchase threshold such as `$75`, or sunset after replacing with a cleaner campaign code.
4. Confirm whether any `KEEP` or `REVIEW` codes are tied to current emails, ads, influencers, wholesale/customer-service promises, or abandoned-cart flows.

## Active Action Table

| Code | ID | Status | Value | Uses | Min | Bucket | Reason | Action |
| --- | --- | --- | --- | ---: | --- | --- | --- | --- |
| `W15MTMX300` | `362923655265` | ACTIVE | 16% | 1 | subtotal>=300.0 USD | `CAP_OR_DISABLE` | 16% exceeds the 15% marketing cap. | Disable or cap at 15% only if owner confirms active campaign need. |
| `5YH8V` | `289036632161` | ACTIVE | 20% | 0 |  | `CAP_OR_DISABLE` | 20% exceeds the 15% marketing cap. | Disable or cap at 15% only if owner confirms active campaign need. |
| `CATASUELS45OFF` | `311618535521` | ACTIVE | 45% | 0 |  | `CAP_OR_DISABLE` | 45% exceeds the 15% marketing cap. | Disable or cap at 15% only if owner confirms active campaign need. |
| `V700J25%OFF` | `288950222945` | ACTIVE | 25% | 0 |  | `CAP_OR_DISABLE` | 25% exceeds the 15% marketing cap. | Disable or cap at 15% only if owner confirms active campaign need. |
| `W20MDRX600` | `302320615521` | ACTIVE | 19% | 0 | subtotal>=400.0 USD | `CAP_OR_DISABLE` | 19% exceeds the 15% marketing cap. | Disable or cap at 15% only if owner confirms active campaign need. |
| `W25MTMX500` | `302320713825` | ACTIVE | 22% | 0 | subtotal>=500.0 USD | `CAP_OR_DISABLE` | 22% exceeds the 15% marketing cap. | Disable or cap at 15% only if owner confirms active campaign need. |
| `W25MTMX600` | `362924540001` | ACTIVE | 25% | 0 | subtotal>=600.0 USD | `CAP_OR_DISABLE` | 25% exceeds the 15% marketing cap. | Disable or cap at 15% only if owner confirms active campaign need. |
| `TESTMEONLY` | `416416596065` | ACTIVE | 100% | 1 |  | `DISABLE` | Looks like internal/test code and is 100%, above the 15% cap. | Deactivate after owner approval or replace with controlled draft/test flow. |
| `12%OFF1200` | `727300931681` | ACTIVE | 12% | 0 | subtotal>=1200.0 USD | `DISABLE` | Unused active discount with no current-use evidence. | Deactivate after owner approval if not tied to a live flow. |
| `15%OFF2000` | `727301226593` | ACTIVE | 15% | 0 | subtotal>=2000.0 USD | `DISABLE` | Unused active discount with no current-use evidence. | Deactivate after owner approval if not tied to a live flow. |
| `8%OFF500` | `727301488737` | ACTIVE | 8% | 0 | subtotal>=500.0 USD | `DISABLE` | Unused active discount with no current-use evidence. | Deactivate after owner approval if not tied to a live flow. |
| `BDAY` | `288321994849` | ACTIVE | 10% | 0 |  | `DISABLE` | Unused open-ended discount with no minimum and no current-use evidence. | Deactivate after owner approval if not tied to a live flow. |
| `DONTGO` | `2386963141` | ACTIVE | 10% | 0 |  | `DISABLE` | Unused open-ended discount with no minimum and no current-use evidence. | Deactivate after owner approval if not tied to a live flow. |
| `LUCKY11OFF-PSBNWSP` | `372335902817` | ACTIVE | 11% | 0 |  | `DISABLE` | Unused open-ended discount with no minimum and no current-use evidence. | Deactivate after owner approval if not tied to a live flow. |
| `LUCKY15OFF-K58C9TM` | `372336033889` | ACTIVE | 15% | 0 |  | `DISABLE` | Unused open-ended discount with no minimum and no current-use evidence. | Deactivate after owner approval if not tied to a live flow. |
| `LUCKY5OFF-24XNM20` | `372335738977` | ACTIVE | 5% | 0 |  | `DISABLE` | Unused open-ended discount with no minimum and no current-use evidence. | Deactivate after owner approval if not tied to a live flow. |
| `LUCKY7OFF-0XY6N62` | `372335837281` | ACTIVE | 7% | 0 |  | `DISABLE` | Unused open-ended discount with no minimum and no current-use evidence. | Deactivate after owner approval if not tied to a live flow. |
| `LUCKY9OFF-KDTTCT` | `372335968353` | ACTIVE | 9% | 0 |  | `DISABLE` | Unused open-ended discount with no minimum and no current-use evidence. | Deactivate after owner approval if not tied to a live flow. |
| `LX-07Z66P` | `732385640545` | ACTIVE | 10% | 0 |  | `DISABLE` | Active orphan Loox-style LX code with 0 uses. | Deactivate after owner approval; do not delete. |
| `LX-0S5L3B` | `728643895393` | ACTIVE | 10% | 0 |  | `DISABLE` | Active orphan Loox-style LX code with 0 uses. | Deactivate after owner approval; do not delete. |
| `LX-17X5YH` | `1095788986465` | ACTIVE | 10% | 0 |  | `DISABLE` | Active orphan Loox-style LX code with 0 uses. | Deactivate after owner approval; do not delete. |
| `LX-1IFK24` | `1024092733537` | ACTIVE | 10% | 0 |  | `DISABLE` | Active orphan Loox-style LX code with 0 uses. | Deactivate after owner approval; do not delete. |
| `LX-1OO6FH` | `931450486881` | ACTIVE | 10% | 0 |  | `DISABLE` | Active orphan Loox-style LX code with 0 uses. | Deactivate after owner approval; do not delete. |
| `LX-3LK5YE` | `315677900897` | ACTIVE | 10% | 0 |  | `DISABLE` | Active orphan Loox-style LX code with 0 uses. | Deactivate after owner approval; do not delete. |
| `LX-3S2UG9` | `931068379233` | ACTIVE | 10% | 0 |  | `DISABLE` | Active orphan Loox-style LX code with 0 uses. | Deactivate after owner approval; do not delete. |
| `LX-42XZVQ` | `1072583770209` | ACTIVE | 10% | 0 |  | `DISABLE` | Active orphan Loox-style LX code with 0 uses. | Deactivate after owner approval; do not delete. |
| `LX-4H0HRV` | `1008547364961` | ACTIVE | 10% | 0 |  | `DISABLE` | Active orphan Loox-style LX code with 0 uses. | Deactivate after owner approval; do not delete. |
| `LX-4N1TA9` | `732385378401` | ACTIVE | 10% | 0 |  | `DISABLE` | Active orphan Loox-style LX code with 0 uses. | Deactivate after owner approval; do not delete. |
| `LX-4NZ3K7` | `1021410869345` | ACTIVE | 10% | 0 |  | `DISABLE` | Active orphan Loox-style LX code with 0 uses. | Deactivate after owner approval; do not delete. |
| `LX-5WWILV` | `949919219809` | ACTIVE | 10% | 0 |  | `DISABLE` | Active orphan Loox-style LX code with 0 uses. | Deactivate after owner approval; do not delete. |
| `LX-72ZIUJ` | `728643960929` | ACTIVE | 10% | 0 |  | `DISABLE` | Active orphan Loox-style LX code with 0 uses. | Deactivate after owner approval; do not delete. |
| `LX-84KR1W` | `928896286817` | ACTIVE | 10% | 0 |  | `DISABLE` | Active orphan Loox-style LX code with 0 uses. | Deactivate after owner approval; do not delete. |
| `LX-8ESBIB` | `987682668641` | ACTIVE | 10% | 0 |  | `DISABLE` | Active orphan Loox-style LX code with 0 uses. | Deactivate after owner approval; do not delete. |
| `LX-8VWPTD` | `611369320545` | ACTIVE | 10% | 0 |  | `DISABLE` | Active orphan Loox-style LX code with 0 uses. | Deactivate after owner approval; do not delete. |
| `LX-9XWHGH` | `686690369633` | ACTIVE | 10% | 0 |  | `DISABLE` | Active orphan Loox-style LX code with 0 uses. | Deactivate after owner approval; do not delete. |
| `LX-ABYUCR` | `722053431393` | ACTIVE | 10% | 0 |  | `DISABLE` | Active orphan Loox-style LX code with 0 uses. | Deactivate after owner approval; do not delete. |
| `LX-AT5IFV` | `405713354849` | ACTIVE | 10% | 0 |  | `DISABLE` | Active orphan Loox-style LX code with 0 uses. | Deactivate after owner approval; do not delete. |
| `LX-BN3D77` | `1032735260769` | ACTIVE | 10% | 0 |  | `DISABLE` | Active orphan Loox-style LX code with 0 uses. | Deactivate after owner approval; do not delete. |
| `LX-CHVNX4` | `1042086494305` | ACTIVE | 10% | 0 |  | `DISABLE` | Active orphan Loox-style LX code with 0 uses. | Deactivate after owner approval; do not delete. |
| `LX-CUGZZ3` | `1012164034657` | ACTIVE | 10% | 0 |  | `DISABLE` | Active orphan Loox-style LX code with 0 uses. | Deactivate after owner approval; do not delete. |
| `LX-CZ2G7Z` | `405713420385` | ACTIVE | 10% | 0 |  | `DISABLE` | Active orphan Loox-style LX code with 0 uses. | Deactivate after owner approval; do not delete. |
| `LX-DI3N75` | `928268877921` | ACTIVE | 10% | 0 |  | `DISABLE` | Active orphan Loox-style LX code with 0 uses. | Deactivate after owner approval; do not delete. |
| `LX-DZLJER` | `914542755937` | ACTIVE | 10% | 0 |  | `DISABLE` | Active orphan Loox-style LX code with 0 uses. | Deactivate after owner approval; do not delete. |
| `LX-F4RZO5` | `684152094817` | ACTIVE | 10% | 0 |  | `DISABLE` | Active orphan Loox-style LX code with 0 uses. | Deactivate after owner approval; do not delete. |
| `LX-FW5H8W` | `728643436641` | ACTIVE | 10% | 0 |  | `DISABLE` | Active orphan Loox-style LX code with 0 uses. | Deactivate after owner approval; do not delete. |
| `LX-FXX3CJ` | `600549064801` | ACTIVE | 10% | 0 |  | `DISABLE` | Active orphan Loox-style LX code with 0 uses. | Deactivate after owner approval; do not delete. |
| `LX-G9H0ZM` | `734159634529` | ACTIVE | 10% | 0 |  | `DISABLE` | Active orphan Loox-style LX code with 0 uses. | Deactivate after owner approval; do not delete. |
| `LX-GDDUAD` | `933381079137` | ACTIVE | 10% | 0 |  | `DISABLE` | Active orphan Loox-style LX code with 0 uses. | Deactivate after owner approval; do not delete. |
| `LX-H4Y7SZ` | `604047868001` | ACTIVE | 10% | 0 |  | `DISABLE` | Active orphan Loox-style LX code with 0 uses. | Deactivate after owner approval; do not delete. |
| `LX-HLGHCN` | `694886432865` | ACTIVE | 10% | 0 |  | `DISABLE` | Active orphan Loox-style LX code with 0 uses. | Deactivate after owner approval; do not delete. |
| `LX-IRIK6T` | `618992631905` | ACTIVE | 10% | 0 |  | `DISABLE` | Active orphan Loox-style LX code with 0 uses. | Deactivate after owner approval; do not delete. |
| `LX-IW5U5C` | `944214704225` | ACTIVE | 10% | 0 |  | `DISABLE` | Active orphan Loox-style LX code with 0 uses. | Deactivate after owner approval; do not delete. |
| `LX-JQ9OET` | `933904187489` | ACTIVE | 10% | 0 |  | `DISABLE` | Active orphan Loox-style LX code with 0 uses. | Deactivate after owner approval; do not delete. |
| `LX-K4NHZ4` | `728644681825` | ACTIVE | 10% | 0 |  | `DISABLE` | Active orphan Loox-style LX code with 0 uses. | Deactivate after owner approval; do not delete. |
| `LX-KW7BDM` | `1090413789281` | ACTIVE | 10% | 0 |  | `DISABLE` | Active orphan Loox-style LX code with 0 uses. | Deactivate after owner approval; do not delete. |
| `LX-LFWSGG` | `754418712673` | ACTIVE | 10% | 0 |  | `DISABLE` | Active orphan Loox-style LX code with 0 uses. | Deactivate after owner approval; do not delete. |
| `LX-MEHN03` | `1032735522913` | ACTIVE | 10% | 0 |  | `DISABLE` | Active orphan Loox-style LX code with 0 uses. | Deactivate after owner approval; do not delete. |
| `LX-MK4AGO` | `759170269281` | ACTIVE | 10% | 0 |  | `DISABLE` | Active orphan Loox-style LX code with 0 uses. | Deactivate after owner approval; do not delete. |
| `LX-MXI43O` | `623074639969` | ACTIVE | 10% | 0 |  | `DISABLE` | Active orphan Loox-style LX code with 0 uses. | Deactivate after owner approval; do not delete. |
| `LX-N9GTYS` | `684159303777` | ACTIVE | 10% | 0 |  | `DISABLE` | Active orphan Loox-style LX code with 0 uses. | Deactivate after owner approval; do not delete. |
| `LX-OZJK3M` | `991449219169` | ACTIVE | 10% | 0 |  | `DISABLE` | Active orphan Loox-style LX code with 0 uses. | Deactivate after owner approval; do not delete. |
| `LX-PTPXL1` | `308978614369` | ACTIVE | 10% | 0 |  | `DISABLE` | Active orphan Loox-style LX code with 0 uses. | Deactivate after owner approval; do not delete. |
| `LX-PW6N4J` | `311602544737` | ACTIVE | 10% | 0 |  | `DISABLE` | Active orphan Loox-style LX code with 0 uses. | Deactivate after owner approval; do not delete. |
| `LX-PWZ4AI` | `669064233057` | ACTIVE | 10% | 0 |  | `DISABLE` | Active orphan Loox-style LX code with 0 uses. | Deactivate after owner approval; do not delete. |
| `LX-QC3VDR` | `611368992865` | ACTIVE | 10% | 0 |  | `DISABLE` | Active orphan Loox-style LX code with 0 uses. | Deactivate after owner approval; do not delete. |
| `LX-QECONH` | `308679868513` | ACTIVE | 10% | 0 |  | `DISABLE` | Active orphan Loox-style LX code with 0 uses. | Deactivate after owner approval; do not delete. |
| `LX-QNZTC3` | `710420398177` | ACTIVE | 10% | 0 |  | `DISABLE` | Active orphan Loox-style LX code with 0 uses. | Deactivate after owner approval; do not delete. |
| `LX-RJIOQ9` | `308680327265` | ACTIVE | 10% | 0 |  | `DISABLE` | Active orphan Loox-style LX code with 0 uses. | Deactivate after owner approval; do not delete. |
| `LX-SB55ZX` | `308680065121` | ACTIVE | 10% | 0 |  | `DISABLE` | Active orphan Loox-style LX code with 0 uses. | Deactivate after owner approval; do not delete. |
| `LX-SKQG6I` | `728633147489` | ACTIVE | 10% | 0 |  | `DISABLE` | Active orphan Loox-style LX code with 0 uses. | Deactivate after owner approval; do not delete. |
| `LX-SLBYNO` | `1032735326305` | ACTIVE | 10% | 0 |  | `DISABLE` | Active orphan Loox-style LX code with 0 uses. | Deactivate after owner approval; do not delete. |
| `LX-SS95VC` | `414592729185` | ACTIVE | 10% | 0 |  | `DISABLE` | Active orphan Loox-style LX code with 0 uses. | Deactivate after owner approval; do not delete. |
| `LX-SXVOMX` | `620997050465` | ACTIVE | 10% | 0 |  | `DISABLE` | Active orphan Loox-style LX code with 0 uses. | Deactivate after owner approval; do not delete. |
| `LX-U616HM` | `937999466593` | ACTIVE | 10% | 0 |  | `DISABLE` | Active orphan Loox-style LX code with 0 uses. | Deactivate after owner approval; do not delete. |
| `LX-UPOOYG` | `1032735457377` | ACTIVE | 10% | 0 |  | `DISABLE` | Active orphan Loox-style LX code with 0 uses. | Deactivate after owner approval; do not delete. |
| `LX-V5PMYM` | `728632623201` | ACTIVE | 10% | 0 |  | `DISABLE` | Active orphan Loox-style LX code with 0 uses. | Deactivate after owner approval; do not delete. |
| `LX-VQ41PW` | `1036208963681` | ACTIVE | 10% | 0 |  | `DISABLE` | Active orphan Loox-style LX code with 0 uses. | Deactivate after owner approval; do not delete. |
| `LX-W8TX8D` | `928896057441` | ACTIVE | 10% | 0 |  | `DISABLE` | Active orphan Loox-style LX code with 0 uses. | Deactivate after owner approval; do not delete. |
| `LX-XDGA1D` | `1032735490145` | ACTIVE | 10% | 0 |  | `DISABLE` | Active orphan Loox-style LX code with 0 uses. | Deactivate after owner approval; do not delete. |
| `LX-XROA8E` | `755633848417` | ACTIVE | 10% | 0 |  | `DISABLE` | Active orphan Loox-style LX code with 0 uses. | Deactivate after owner approval; do not delete. |
| `LX-YDDFKK` | `1032735129697` | ACTIVE | 10% | 0 |  | `DISABLE` | Active orphan Loox-style LX code with 0 uses. | Deactivate after owner approval; do not delete. |
| `LX-ZJ8HTK` | `759942512737` | ACTIVE | 10% | 0 |  | `DISABLE` | Active orphan Loox-style LX code with 0 uses. | Deactivate after owner approval; do not delete. |
| `NEW15OFF` | `374584475745` | ACTIVE | 15% | 0 |  | `DISABLE` | Unused open-ended discount with no minimum and no current-use evidence. | Deactivate after owner approval if not tied to a live flow. |
| `THANKYOU10` | `374585852001` | ACTIVE | 10% | 0 |  | `DISABLE` | Unused open-ended discount with no minimum and no current-use evidence. | Deactivate after owner approval if not tied to a live flow. |
| `QP672` | `2626435205` | ACTIVE | 10% | 90 |  | `REVIEW` | Only materially used code found: 90 uses, 10%, no minimum. | Keep active only if intended; recommended owner decision on minimum purchase, e.g. $75. |
| `BGV310` | `299828412513` | ACTIVE | 10% | 2 |  | `REVIEW` | Has 2 use(s), so business context is needed before disabling. | Review owner/campaign intent before changing. |
| `LUCKY13OFF-WBW8MT` | `372336001121` | ACTIVE | 13% | 1 |  | `REVIEW` | Has 1 use(s), so business context is needed before disabling. | Review owner/campaign intent before changing. |
| `LX-8DZ9HV` | `688107651169` | ACTIVE | 10% | 1 |  | `REVIEW` | Has 1 use(s), so business context is needed before disabling. | Review owner/campaign intent before changing. |
| `LX-FJNXBU` | `987681554529` | ACTIVE | 10% | 1 |  | `REVIEW` | Has 1 use(s), so business context is needed before disabling. | Review owner/campaign intent before changing. |
| `LX-L12KDK` | `967755104353` | ACTIVE | 10% | 1 |  | `REVIEW` | Has 1 use(s), so business context is needed before disabling. | Review owner/campaign intent before changing. |
| `W10MZPZ100` | `291135848545` | ACTIVE | 10% | 1 | subtotal>=100.0 USD | `REVIEW` | Has 1 use(s), so business context is needed before disabling. | Review owner/campaign intent before changing. |
| `W15MTMX200` | `302320517217` | ACTIVE | 13% | 1 | subtotal>=200.0 USD | `REVIEW` | Has 1 use(s), so business context is needed before disabling. | Review owner/campaign intent before changing. |
| `WWNL9` | `2641678533` | ACTIVE | 15% | 9 |  | `KEEP` | Has 9 uses and is at or below 15%. | Keep unless campaign is obsolete. |
| `FB10%OFF` | `377951322209` | ACTIVE | 10% | 5 |  | `KEEP` | Has 5 uses and is at or below 15%. | Keep unless campaign is obsolete. |

## Files

- `raw_json`: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-29-discount-disposition/discount_nodes_raw.json`
- `disposition_csv`: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-29-discount-disposition/discount_disposition.csv`
- `markdown`: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-29-discount-disposition/discount_disposition.md`

## STOP

Do not deactivate, cap, delete, or edit any discount until Francisco approves the exact code list.
