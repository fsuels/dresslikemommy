# Shopify order refresh — September 22, 2026

Status: VERIFIED_WITH_LIMITS. Read-only Shopify connector; no browser, external mutation, credential access, pixel query, or shared canonical edit.

## Source and cutoff

- Live identity verified: Dress Like Mommy, `dresslikemommy-com.myshopify.com`, shop currency USD, timezone America/New_York.
- Window: September 17 00:00:00 EDT through September 22 10:22:01 EDT, inclusive (`2026-09-17T04:00:00Z` through `2026-09-22T14:22:01Z`).
- Source response received by `2026-09-22T14:22:35Z`.
- Cohort uses createdAt; no financial-status exclusion in the source query. All returned records independently qualify as PAID, non-test, noncancelled, web-source.
- Three distinct transient order IDs; all three creation timestamps inside the window. Order pagination exhausted. Each journey ready=true, first=last, one available moment, no next moments page.
- Compared with SHOPIFY_READBACK.md's 14:01:52 UTC cutoff: no new orders, no order updatedAt after that cutoff, and no changes in observed amounts, qualification, refunds, source, URLs or UTMs. No fresh GA4 transaction-identity comparison was made in this refresh.

## Reconciled amounts

| Audit reference | Created (EDT) | Shop original/current subtotal and total | Presentment original/current subtotal and total | Shop refunds | First and last source |
|---|---|---|---|---|---|
| E1 | Sep 18 12:39:25 | USD64.98 | USD64.98 | USD0.00 | Direct |
| E2 (earlier O1) | Sep 19 11:28:07 | USD66.98 | USD66.98 | USD0.00 | Direct |
| E3 (earlier O2) | Sep 22 04:22:31 | USD68.20 | AUD96.00 | USD0.00 | Google / SEO |

Total shop-currency order value: **USD200.16**, independently aggregated as 20,016 integer cents. Direct orders total USD131.96. Do not sum mixed presentment currencies.

## Attribution evidence and limit

All first/last visits and all available moments have null UTM parameters and no query keys, msclkid, or gclid in recorded landing/referrer URLs. The Direct visits have null referrers; E3 records www.google.com as referrer and Google/SEO source.

No captured Shopify journey supports Microsoft paid attribution. Direct remains unresolved: this does not rule out earlier ad influence, identifier loss, consent effects, cross-device journeys, or unrecorded sessions. Complete API pagination is not complete real-world journey capture.

The newest checkout requires the correct value/currency pairing: AUD96.00 presentment versus USD68.20 shop reporting. No Microsoft payload, revenue receipt, goal match, click-ID join, CPA, ROAS, retained profit or tracking repair is established by these order reads.

## Validation

Schema discovery completed for QueryRoot, Order, Shop, CustomerJourneySummary, CustomerVisit, UTMParameters, MoneyBag, MoneyV2, OrderConnection, CustomerMomentConnection, PageInfo and OrderSortKeys. Connector validator passed for both identity and order queries before execution. Query used first=50 and pageInfo for both connection levels; every hasNextPage=false. No PII fields requested; raw order/click IDs were not printed or persisted. Shopify Admin authoring skill was inspected but not applied to this store-result connector workflow; the connector's mandatory discovery/validation workflow was followed.

## Sanitized source record

```json
{
  "summary": {
    "windowStart": "2026-09-17T04:00:00Z",
    "cutoff": "2026-09-22T14:22:01Z",
    "fetchedBy": "2026-09-22T14:22:35Z",
    "orderCount": 3,
    "distinctIds": 3,
    "hasMoreOrders": false,
    "moreMoments": false,
    "newCreationsSincePriorCutoff": 0,
    "updatedSincePriorCutoff": 0,
    "allWithinWindow": true,
    "qualified": 3,
    "currentTotalUSDCents": 20016,
    "refundUSDCents": 0
  },
  "rows": [
    {
      "auditRef": "E1",
      "createdAt": "2026-09-18T16:39:25Z",
      "processedAt": "2026-09-18T16:39:20Z",
      "updatedAt": "2026-09-18T16:39:27Z",
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
      "currentTotal": {
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
      "currentSubtotal": {
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
        },
        "presentmentMoney": {
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
        "hasMoreMoments": false
      }
    },
    {
      "auditRef": "E2",
      "createdAt": "2026-09-19T15:28:07Z",
      "processedAt": "2026-09-19T15:28:03Z",
      "updatedAt": "2026-09-21T11:23:42Z",
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
      "currentTotal": {
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
      "currentSubtotal": {
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
        },
        "presentmentMoney": {
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
        "hasMoreMoments": false
      }
    },
    {
      "auditRef": "E3",
      "createdAt": "2026-09-22T08:22:31Z",
      "processedAt": "2026-09-22T08:22:26Z",
      "updatedAt": "2026-09-22T08:22:36Z",
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
      "currentTotal": {
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
      "currentSubtotal": {
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
        },
        "presentmentMoney": {
          "amount": "0.0",
          "currencyCode": "AUD"
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
        "hasMoreMoments": false
      }
    }
  ]
}
```

