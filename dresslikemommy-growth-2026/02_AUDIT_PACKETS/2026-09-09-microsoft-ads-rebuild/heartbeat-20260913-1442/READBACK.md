# Microsoft Ads September13 reporting and account readback

Account477439 / customer770182. Checked September13 at14:46–14:56UTC through the task-owned Microsoft Advertising tab.

VERIFIED: September12's native report has13 campaigns, all currently Paused, with zero Spend, Revenue, Conv., Clicks, Impr. and Total spend. All five exported aggregate rows, including Deleted items total and Overall total, also contain numeric zeros.

September13 is a partial day. Its13 campaign rows contain the same numeric zeros and current Paused statuses. The UI displays zero overall metrics, but the three CSV aggregate rows contain dashes; these remain unavailable rather than being converted to zero. The UI lists the paused legacy USA Shopping campaign with Product offers not found; the export lists Campaign paused. Neither observation establishes feed repair.

The linked Account level options page displayed the Consent Mode notice again. After closing it without Continue, MSCLKID and replacement UTM auto-tagging were on; automatic simplified goals, dynamic-group multimedia and domain-image retrieval were off. No account settings were changed. This notice and these options do not verify consent or real-purchase acceptance.

Both native CSV files are preserved unchanged. Validation passed for their hashes, date headers,35-column row shapes, exact13 unique campaign IDs, current statuses and raw metric values. Today’s unavailable totals were explicitly retained. The UI reports Eastern Time (U.S. & Canada) with its literal GMT-05:00 label; no UTC order join is asserted. Last-hour delivery and recent conversions can lag.

CPA, CPC and ROAS with zero denominators are undefined, regardless of displayed zeros. These reports do not establish Shopify-attributed purchases or retained profit. They do not fill missing spend or costs in the older, differently dated profit baseline.

Disposition: hold with evidence. Paid scope remains NONE. Existing consent support contact is still unsent and its question pending. The next action is the supported consent repair, followed by genuine purchase acceptance; no duplicate owner question was raised. No account/campaign/goal saves, imports, paid activation, support message, order query, planner study or shared canonical write occurred. The existing parent sales clock and four-hour continuation remain unchanged. The account settings tab was marked for handoff.

Evidence and method: [readback.json](readback.json), [September12 CSV](campaign-2026-09-12.csv), [September13 partial-day CSV](campaign-2026-09-13.csv).

Continuation: ops/prompts/paid-growth-ai-army-continuation-prompt.md.
