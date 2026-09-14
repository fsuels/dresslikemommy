# Italian GA4 native-field interpretation

Confidence: H for semantics; attribution unresolved. Reviewed 2026-09-06. Independent documentation review of [diagnostic](ITALIAN_ATTRIBUTION_DIAGNOSTIC.md) and [semantics](italian_attribution_semantics.md); no account read.

Operator-supplied scope: property 330266838, June 7–September 4, 2026 inclusive; one matched Italian purchase, USD151.46, generic session campaign 23866684201. The Transactions picker restricts dimensions to cross-platform fields. This is an observed report limitation, not a missing Ads value.

Google’s [Data API schema](https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema) defines:

| Field | Meaning |
| --- | --- |
| `sessionGoogleAdsCampaignId` | Google Ads campaign attributed to the session. |
| `sessionGoogleAdsCustomerId` | Google Ads account attributed to the session. |
| `sessionManualCampaignId` | Manual campaign identifier populated from `utm_id`. |

Generic `sessionCampaignId` includes Ads, manual and other campaigns; numeric appearance establishes no origin.

- **Both Ads fields populated:** preserve GA4’s account/campaign assignment; privately verify expected identity. This is not an independent click join or Google Ads conversion-credit receipt.
- **Manual ID populated:** supports a manual campaign parameter. It does not prove organic acquisition or exclude Ads: [manual and auto-tagging can coexist](https://support.google.com/analytics/answer/11242870?hl=en). Preserve both when returned; investigate disagreement without forcing equivalence.
- **Ads values absent or `(not set)`:** attribution remains unresolved. Google documents [unlinked auto-tagged traffic remaining google/cpc](https://support.google.com/analytics/answer/9379420?hl=en) while new Ads dimensions are missing, and [WBRAID/GBRAID-related missing dimensions](https://support.google.com/analytics/answer/14452452?hl=en). These are possibilities, not diagnoses here.

The [exploration API schema](https://developers.google.com/analytics/devguides/reporting/data/v1/exploration-api-schema) covers funnel reports; its Yes/No column means “Available in segments,” not universal picker availability. Unavailable fields and empty filtered results are not negative click evidence. Preserve exact scope, filters, coverage and quality notices before comparison.

[Session dimensions use paid-and-organic last-click attribution](https://support.google.com/analytics/answer/11080067?hl=en), unaffected by the property’s event-attribution model.

Next action: root’s bounded native-field readback, or an explicit capability limitation. Neither result alone supports CPA, 650% ROAS, incrementality or profit; campaign spend, conversion accounting and actual costs remain necessary. No measurement or paid-media change follows from this interpretation.
