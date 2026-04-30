# Google Ads Paid Value Measurement Gate - PASS

Status: `PASS_PAID_VALUE_MEASUREMENT_GATE`

## Shopify Paid Order

| Field | Value | Result |
|---|---:|---:|
| Order | `#9476` | PASS |
| Confirmation | `5QU2KJ7DN` | PASS |
| Shopify order id | `6575644803169` | PASS |
| Financial status | `PAID` | PASS |
| Total | `19.99 USD` | PASS |
| Successful capture | `True` | PASS |

## Google Ads Purchase Proof

| Field | Value | Result |
|---|---:|---:|
| Primary conversion endpoint | `www.googleadservices.com/pagead/conversion/853411529/` | PASS |
| Conversion label | `UbkpCN-fhogBEMmN-JYD` | PASS |
| Event | `purchase` | PASS |
| Value | `19.99` | PASS |
| Currency | `USD` | PASS |
| Dedupe/order id | `6575644803169` | PASS |
| Enhanced conversion hash present | `True` | PASS |

## GA4 / Google Measurement Proof

A paired Google measurement purchase request for measurement id `G-N4EQNK0MMB` carried `event=purchase`, `value=19.99`, `currency=USD`, and transaction id `6575644803169`.

## Dedupe

All captured purchase requests for this paid checkout used the same order id where an order id was present: `6575644803169`. The controlled reload did not produce a new distinct purchase order id.

## Decision

The strict paid-value measurement blocker is cleared. Non-budget campaign edits that depend on proving paid purchase value can now proceed.

This report does not by itself enable campaigns or approve budget increases. Campaign-specific feed, website, product-scope, policy, and owner-approval gates still apply before launch.

## Privacy

Stored evidence is sanitized. Headers, cookies, card data, full URLs, payment payloads, email, phone, and address were not stored.
