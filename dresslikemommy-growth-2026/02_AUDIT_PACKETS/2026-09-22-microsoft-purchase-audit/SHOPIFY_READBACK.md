# Shopify readback — Microsoft purchase audit

## Extended window requested by parent: September17 through same cutoff

Native Microsoft first-click evidence caused parent to request a separate wider cohort. Query executed by September22 14:03:52UTC, preserving fixed cutoff14:01:52UTC; start `2026-09-17T04:00:00Z`. All-status orders returned3distinctIDs and no next page. All3 are PAID/non-test/noncancelled/web with USD0refunds. Ready journeys have one moment each and no next moments page.

Additional order E1: created Sep18 12:39:25EDT (processed12:39:20EDT); USD64.98shop subtotal/currenttotal and USD64.98presentment. Its first=last Direct visit at12:30:54EDT landed on `/products/vintage-cottage-floral-mommy-and-me-pajama-set`, with null referrer, nullUTM, no query keys/msclkid/gclid. E2=O1 and E3=O2; never add these overlapping windows.

Extended shop total: USD64.98+66.98+68.20=**USD200.16**. Two Shopify Direct orders sumUSD131.96. The independent GA4 specialist reports fresh GA4 Sep17–22 total3purchases/USD200.32, Direct2/USD131.96 and data-not-available1/USD68.36. Subsequent private identifier reconciliation matched all three Shopify numeric order IDs to GA4 transaction IDs using equal 13-character lengths and identical FNV1a64 fingerprints, computed independently from each source. All three comparisons returned true. This is strong practical identifier evidence, beyond matching counts; raw IDs and fingerprints are not persisted. Noncryptographic fingerprint collision is a theoretical limitation. The newest matched order has a USD0.16 reporting-value difference (GA4USD68.36 versus ShopifyUSD68.20). FX timing is possible but unverified; true presentment remainsAUD96.00. GA4 receiving these orders does not establish Microsoft receiving or attributing them.

Sanitized additional source row:

```json
{
  "auditRef": "E1",
  "createdAt": "2026-09-18T16:39:25Z",
  "processedAt": "2026-09-18T16:39:20Z",
  "test": false,
  "cancelledAt": null,
  "status": "PAID",
  "sourceName": "web",
  "total": {
    "shopMoney": {
      "amount": "64.98",
      "currencyCode": "USD"
    },
    "presentmentMoney": {
      "amount": "64.98",
      "currencyCode": "USD"
    }
  },
  "subtotal": {
    "shopMoney": {
      "amount": "64.98",
      "currencyCode": "USD"
    },
    "presentmentMoney": {
      "amount": "64.98",
      "currencyCode": "USD"
    }
  },
  "refund": {
    "shopMoney": {
      "amount": "0.0",
      "currencyCode": "USD"
    }
  },
  "journey": {
    "ready": true,
    "first": {
      "occurredAt": "2026-09-18T16:30:54Z",
      "source": "direct",
      "sourceType": null,
      "landing": {
        "host": "www.dresslikemommy.com",
        "path": "/products/vintage-cottage-floral-mommy-and-me-pajama-set",
        "queryKeys": [],
        "msclkidPresent": false,
        "gclidPresent": false
      },
      "referrer": null,
      "utm": null
    },
    "last": {
      "occurredAt": "2026-09-18T16:30:54Z",
      "source": "direct",
      "sourceType": null,
      "landing": {
        "host": "www.dresslikemommy.com",
        "path": "/products/vintage-cottage-floral-mommy-and-me-pajama-set",
        "queryKeys": [],
        "msclkidPresent": false,
        "gclidPresent": false
      },
      "referrer": null,
      "utm": null
    },
    "moments": [
      {
        "occurredAt": "2026-09-18T16:30:54Z",
        "source": "direct",
        "sourceType": null,
        "landing": {
          "host": "www.dresslikemommy.com",
          "path": "/products/vintage-cottage-floral-mommy-and-me-pajama-set",
          "queryKeys": [],
          "msclkidPresent": false,
          "gclidPresent": false
        },
        "referrer": null,
        "utm": null
      }
    ],
    "moreMoments": false
  }
}
```


Status: VERIFIED_WITH_LIMITS. Fresh live read-only evidence; no external writes.

Additional exact pixel identity read was BLOCKED: Shopify Admin returned `Access denied for webPixel field. Required access: read_pixels access scope.` for the known pixel931561569. Schema and query validated, but no pixel state was returned. No retry, scope grant or settings change; native Connected status remains outside this API evidence.

## Identity, source and window

- Observed through authenticated Shopify connector using schema-discovered and validated Admin GraphQL.
- Store: Dress Like Mommy, `dresslikemommy-com.myshopify.com`; timezone `America/New_York`; shop currency USD.
- Fixed query window: September 19, 2026 00:00 EDT (`2026-09-19T04:00:00Z`) through `2026-09-22T14:01:52Z` (September 22 10:01:52 EDT).
- All-status creation query returned 2 distinct order IDs; all 2 pass PAID, non-test, noncancelled, web-source qualification. No excluded records in this window. Orders pagination exhausted.
- Both journeys report ready=true, first=last, exactly one returned moment and no further moments page.
- Actual order IDs retained only transiently for distinctness; never written here. O1/O2 are local audit labels, not transaction IDs.
- Shopify createdAt defines cohort membership. processedAt is separately retained. This is not an exact campaign-launch cohort: launch timestamp remains with parent Microsoft audit.

## Reconciled orders

| Audit ref | Created (EDT) | Shop subtotal/current total | Checkout presentment subtotal/current total | Recorded refunds | First and last recorded source |
|---|---|---|---|---|---|
| O1 | Sep19 11:28:07 | USD66.98 | USD66.98 | USD0.00 | direct |
| O2 | Sep22 04:22:31 | USD68.20 | AUD96.00 | USD0.00 | Google / SEO |

Total shop-currency current order value: USD66.98 + USD68.20 = **USD135.18**. These are two store orders, not two attributed Microsoft sales. No mixed-currency addition was performed.

O1: one recorded visit Sep19 11:18:39 EDT; home-page landing, null referrer, null UTM, no query keys and no msclkid/gclid in recorded URL.

O2: one recorded visit Sep22 04:18:20 EDT; `/products/little-pear-mommy-and-me-pajamas` landing, `www.google.com/` referrer, null UTM, no query keys and no msclkid/gclid in recorded URLs. This supports Shopify-reported Google organic attribution only.

## Decision and uncertainty

- **No Shopify journey in this two-order cohort supports Microsoft paid credit.** Direct is unresolved, not evidence of organic/direct causality or proof that no Microsoft ad influenced it.
- The newest checkout uses **AUD96.00**, whereas shop reporting uses USD68.20. A matching purchase payload should be compared using the correct value-currency pair and transaction identity. Do not label AUD96 as USD96 or infer payload acceptance from Shopify amounts.
- Complete captured moments do not guarantee complete real-world visits: missing identifiers, consent, cross-device or unrecorded journeys remain possible.
- All three extended-cohort orders were privately reconciled to GA4 transaction IDs as described above. No order-to-Microsoft receiver join has been proved. A same-day single UET purchase is insufficient.
- Completed Sep21 New York day: 0 qualifying creations in this query. Sep22 through cutoff: 1 order/USD68.20 shop value, recorded Google SEO. Verified Microsoft paid sales/revenue, CPA, ROAS, retained profit and improvement are **unknown**, not zero.
- Spend and platform conversion values belong to parent's independently dated Microsoft audit. Do not calculate ROAS from USD135.18 all-store revenue.
- Target remains profitable paid sales around650% ROAS and modeled CPA aboutUSD10.77; this evidence does not support scaling, high-intent economics or cannibalization conclusions.
- Next required diagnostic: compare the receiver's actual purchase value/currency and transaction evidence, goal match and click-ID preservation against these orders. If native UI exposes parameter names only, preserve the match as unverified and use the supported publisher/support path.

## Validation and operational limits

- Query schema inspected for QueryRoot, Order, CustomerJourneySummary, CustomerVisit, UTMParameters, Shop, MoneyBag and MoneyV2.
- Connector query validator: PASS.
- Shopify Admin skill documentation search: PASS using bundled Node runtime.
- Skill script validator: PASS.
- Response checks: 2 distinct transient order IDs, every createdAt within fixed window, no orders next page, no moments next page, integer-cent aggregate13518.
- Default Homebrew node initially failed with missing `libsimdjson.29.dylib`; bundled Codex Node succeeded. No access/auth blocker.
- No customer name, email, address, order ID, click token or credential requested into this artifact. No browser tabs used, checkout/test orders, tracking changes or other external mutations.

## Sanitized source rows

```json
[
  {
    "auditRef": "O1",
    "createdAt": "2026-09-19T15:28:07Z",
    "processedAt": "2026-09-19T15:28:03Z",
    "test": false,
    "cancelledAt": null,
    "status": "PAID",
    "sourceName": "web",
    "total": {
      "shopMoney": {
        "amount": "66.98",
        "currencyCode": "USD"
      },
      "presentmentMoney": {
        "amount": "66.98",
        "currencyCode": "USD"
      }
    },
    "subtotal": {
      "shopMoney": {
        "amount": "66.98",
        "currencyCode": "USD"
      },
      "presentmentMoney": {
        "amount": "66.98",
        "currencyCode": "USD"
      }
    },
    "refund": {
      "shopMoney": {
        "amount": "0.0",
        "currencyCode": "USD"
      }
    },
    "journey": {
      "ready": true,
      "first": {
        "occurredAt": "2026-09-19T15:18:39Z",
        "source": "direct",
        "sourceType": null,
        "landing": {
          "host": "www.dresslikemommy.com",
          "path": "/",
          "queryKeys": [],
          "msclkidPresent": false,
          "gclidPresent": false
        },
        "referrer": null,
        "utm": null
      },
      "last": {
        "occurredAt": "2026-09-19T15:18:39Z",
        "source": "direct",
        "sourceType": null,
        "landing": {
          "host": "www.dresslikemommy.com",
          "path": "/",
          "queryKeys": [],
          "msclkidPresent": false,
          "gclidPresent": false
        },
        "referrer": null,
        "utm": null
      },
      "moments": [
        {
          "occurredAt": "2026-09-19T15:18:39Z",
          "source": "direct",
          "sourceType": null,
          "landing": {
            "host": "www.dresslikemommy.com",
            "path": "/",
            "queryKeys": [],
            "msclkidPresent": false,
            "gclidPresent": false
          },
          "referrer": null,
          "utm": null
        }
      ],
      "moreMoments": false
    }
  },
  {
    "auditRef": "O2",
    "createdAt": "2026-09-22T08:22:31Z",
    "processedAt": "2026-09-22T08:22:26Z",
    "test": false,
    "cancelledAt": null,
    "status": "PAID",
    "sourceName": "web",
    "total": {
      "shopMoney": {
        "amount": "68.2",
        "currencyCode": "USD"
      },
      "presentmentMoney": {
        "amount": "96.0",
        "currencyCode": "AUD"
      }
    },
    "subtotal": {
      "shopMoney": {
        "amount": "68.2",
        "currencyCode": "USD"
      },
      "presentmentMoney": {
        "amount": "96.0",
        "currencyCode": "AUD"
      }
    },
    "refund": {
      "shopMoney": {
        "amount": "0.0",
        "currencyCode": "USD"
      }
    },
    "journey": {
      "ready": true,
      "first": {
        "occurredAt": "2026-09-22T08:18:20Z",
        "source": "Google",
        "sourceType": "SEO",
        "landing": {
          "host": "www.dresslikemommy.com",
          "path": "/products/little-pear-mommy-and-me-pajamas",
          "queryKeys": [],
          "msclkidPresent": false,
          "gclidPresent": false
        },
        "referrer": {
          "host": "www.google.com",
          "path": "/",
          "queryKeys": [],
          "msclkidPresent": false,
          "gclidPresent": false
        },
        "utm": null
      },
      "last": {
        "occurredAt": "2026-09-22T08:18:20Z",
        "source": "Google",
        "sourceType": "SEO",
        "landing": {
          "host": "www.dresslikemommy.com",
          "path": "/products/little-pear-mommy-and-me-pajamas",
          "queryKeys": [],
          "msclkidPresent": false,
          "gclidPresent": false
        },
        "referrer": {
          "host": "www.google.com",
          "path": "/",
          "queryKeys": [],
          "msclkidPresent": false,
          "gclidPresent": false
        },
        "utm": null
      },
      "moments": [
        {
          "occurredAt": "2026-09-22T08:18:20Z",
          "source": "Google",
          "sourceType": "SEO",
          "landing": {
            "host": "www.dresslikemommy.com",
            "path": "/products/little-pear-mommy-and-me-pajamas",
            "queryKeys": [],
            "msclkidPresent": false,
            "gclidPresent": false
          },
          "referrer": {
            "host": "www.google.com",
            "path": "/",
            "queryKeys": [],
            "msclkidPresent": false,
            "gclidPresent": false
          },
          "utm": null
        }
      ],
      "moreMoments": false
    }
  }
]
```
