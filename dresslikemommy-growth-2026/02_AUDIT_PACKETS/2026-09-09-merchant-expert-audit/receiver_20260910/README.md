# Merchant receiving audit and timezone correction

Confidence: H for the bounded account readbacks and saved timezone; overall product ingestion, approval, automatic withdrawal and international coverage remain incomplete.

Current anchor: `2026-09-10-merchant-source-receiver-audit-and-timezone-alignment`. This checkpoint supersedes the earlier missing-permission and unstable-Chrome directions in the frozen `native_authorized_20260910` packet. The user authorized selecting and operating Merchant Center 513542500. The current native blocker is a newly observed Mac lock, with the existing unlock question pending.

## Verified account state

The September 10, 18:29:50–18:43:46 UTC readback verified the same Merchant account from Merchant Center and Shopify's Google & YouTube app. The existing Content API source **10014302986** has **0 products**, last update **“-”**, country **US**, language **English**, feed label **US**, and Free listings plus Shopping ads destinations. The Google app independently displays total, approved, limited, not approved and under-review counts of zero. The cause remains UNKNOWN. Google's additional-products banner and setup illustrations are not a receipt of Shopify offers.

Shopify's Product sync, Shipping Information and Countries and languages controls display **On**. The countries screen separately displays **Automatic sync On** and says product visibility updates when Shopify settings change. No control was disabled, reset or resubmitted. The earlier AppCatalog `autoPublish:false` field is distinct from these native controls; its speculative mutation remains NOT RUN.

The earlier complete 15:46 UTC Shopify source read accounts for **240 ACTIVE parents / 4,945 variants**, with all parents available to Google and Online Store. It is a dated source baseline, not a receiving count. Draft or archived membership in an app publication does not establish current Google visibility. Add, edit, archive/delete and stock-change propagation have not yet been demonstrated end to end.

## Markets and languages

The app's displayed group sizes total **34 current countries**. Two collapsed country groups and one collapsed language group were not expanded; not every member was individually read. Its 51 unsupported entries consist of 31 countries and 20 language-reason entries. The language warnings omit their countries and overlap languages present in supported groups, so they do not establish that all 20 languages are globally disabled.

Merchant Center separately lists **31 configured countries**, each Incomplete with product readiness zero. Neither count proves approved country coverage. Serbia and Slovenia appear supported in Google's current Shopify documentation but unsupported in the actual app; that contradiction remains unresolved and cannot explain the zero US/English source. The existing Shopify inventory has 65 served countries and 21 published languages; these are separate layers. See [live baseline](live_baseline.json) and [official-source reconciliation](standards_reconciliation.md).

## Implemented correction

One Merchant setting was saved: timezone changed from **Blanc-Sablon** to the exact **Eastern Standard Time (New York)** option, matching Shopify's verified `America/New_York`. The root observed the separate Save, then reloaded the account and verified the persisted New York value. Account language and product protection remained unchanged. The independent saved-receipt review passed **8/8 checks**; it did not replay the native operation. The execution occurred after 18:50:00.604412 UTC and before 18:51:58 UTC.

This changes future reporting-time calculations; it does not resubmit products, recalculate historical metrics or prove traffic/profit. The captured old setting is the configuration rollback. See [receipt](timezone_receipt.json) and [review](timezone_review.md).

## Remaining setup

Merchant detected a **15-day** return-policy suggestion for ten displayed/aggregated countries. Both current published Shopify policy sources instead state **30 days from delivery with eligibility and exclusions**. Independent source reconciliation passed **20/20 checks** and found their visible content identical. Both source pages require **NO_CHANGE**. Do not accept the incorrect 15-day suggestion or invent restocking fees, universal eligibility or delivery promises. Separate broader wording in Terms remains a recorded conflict, without a legal-policy rewrite.

The Merchant overview shows **4 of 5 setup tasks complete**. Its Complete setup link opened the return-policy task for Austria. Clicking Continue was blocked because the Mac locked and automatic unlock failed. The return form did not open; no return policy was submitted. This identifies the next visible task, not a proven cause of zero product submissions. See [policy reconciliation](return_policy_reconciliation.md) and [access checkpoint](access_checkpoint.json).

Shipping shows **76 services**, with sampled imported rows Complete / Show on Google. Not all services were audited, and displayed delivery ranges have not been substantiated against fulfillment evidence. The website is Verified and Claimed and the Shopify link matches. No logo control appeared in the inspected Business details or expanded Marketing menu; the current logo and approval are UNKNOWN. Google Search brand-profile inspection remains NOT RUN. No logo was uploaded.

## Access and exact next step

**Owner action: unlock the Mac.** The existing unlock question remains pending; no new general Merchant permission is needed. Resume the selected account's return setup, map the verified policy and exceptions, read back any saved result, then trace a genuine product update to source 10014302986 before expanding countries or creating another source. Keep native automatic sync as the first path; no dummy edit, off/on cycle, reinstall or duplicate feed is justified by the current evidence. Google approval and actual search exposure cannot be guaranteed by submission alone.

Automatic approval review separately rejected opening the **Product sync On** card twice because it might disable sync. The exact-click approval question is pending; neither click executed and no alternate route was used. Continue independent work without bypassing that rejection.

All previous barcode, image and market-membership repairs remain preserved. UX owns the current unpublished successor **137888792673**; do not publish its older Merchant predecessor. Paid authority remains NONE. This packet is evidence, not another command layer or a new scheduler.

Continuation: “Continue Merchant 513542500 from the source-receiver/timezone anchor. After the existing Mac unlock gate clears, resume the Austria return setup using the verified 30-day policy and exceptions, then prove receipt and lifecycle behavior on the existing Shopify source. Preserve the separate Product sync exact-click gate, previous repairs, UX successor and paid authority.”
