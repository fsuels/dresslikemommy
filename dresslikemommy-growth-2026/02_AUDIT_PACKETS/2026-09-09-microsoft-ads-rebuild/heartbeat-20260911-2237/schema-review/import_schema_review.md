# Microsoft paused-import schema review

**PASS for the exact two-shell column-mapping probe; final Import remains held.** Seven checks passed. The strongest usable path here is Microsoft's native file-import review workflow, which separates column matching/options from Import and warns that unmatched columns are dropped. Header matching does not validate server acceptance. [Official file-import guide](https://help.ads.microsoft.com/apex/index/3/en/51039).

The [template actually linked by this account](https://adsuxprodfd-awb5gsddabddbqgv.z01.azurefd.net/cmuiresources-2/files/templates/Import/ImportTemplateWithAdExtensionsAndBSCAndAdGroupType.csv) was fetched and parsed:25,841bytes,179headers,69datarecords; SHA256 `05f8f0a590e2054a77c64ca1b7939612e5df938beed34374f05f74a92d7ade04`. It has Status/Bid Strategy Type but no maximum-CPC column, noMaxClicks/Paused sample and noRSA example. Its Active/legacy samples must not be imported unchanged.

| Field | Exact probe value | Evidence limit |
|---|---|---|
| Type | Campaign | Native template |
| Status | Paused | API enum; UI acceptance unproved |
| Campaign | Existing reviewed USEN/DEDE names | Absent from fresh account receipt |
| Campaign Type | Search | API enum; UI acceptance unproved |
| Budget Type | Daily | Native template example, not API spelling |
| Budget | 5.00 / 3.00 | Proposed configuration, no spend approval |
| Language | English / German | No location targeting supplied |
| Bid Strategy Type | MaxClicks | API enum; UI acceptance unproved |
| Bid Strategy MaxCpc | 0.15 | Extra API header absent from UI template |

The [Bulk API campaign contract](https://learn.microsoft.com/en-us/advertising/bulk-service/campaign?view=bingads-13) explicitly supports Paused and the MaxClicks cap; omitted Status defaults Active. API uses DailyBudgetStandard, blank/negative new IDs and account ParentId. Its [FormatVersion record](https://learn.microsoft.com/en-us/advertising/bulk-service/format-version?view=bingads-13) is Name6.0. These API conventions are not automatically native UI requirements. [Bulk upload](https://learn.microsoft.com/en-us/advertising/guides/bulk-download-upload?view=bingads-13) executes and can partially succeed; it is not a harmless validation substitute.

Microsoft documents the [optional MaxClicks ceiling](https://learn.microsoft.com/en-us/advertising/campaign-management-service/maxclicksbiddingscheme?view=bingads-13), but its [August31 announcement](https://www.about.ads.microsoft.com/en/blog/post/august-2026/ai-max-for-search-and-other-product-news-for-august-2026) removes it for new nonportfolio MaxClicks campaigns from October1. Existing capped pre-October campaigns/portfolios retain support. Today's schema or an old campaign input cannot prove future new-campaign acceptance.

I checked root's exactCSV `27262e…8964e` against its contract:2rows/9fields, bothPaused, nochildren/adcontent/IDs/website. Names are absent from the11Paused snapshot; configured budgets sum120USD. US/DE are name labels here, not configured geography. The six completed live repairs are untouched.

Proceed only through the declared mapper probe. Stop on dropped/coerced status/cap, direct-apply behavior or an existing-campaign update. If mapping succeeds, inspect options under a separately defined boundary; finalImport still needs exact review and persistedPaused/cap readback. No ads reduces exposure but does not make Active acceptable. Purchase/consent/cost/cash and campaign qualification remain open.

The JSON records source retrieval limitations and hashes. [Exact reviewed probe](../paused_shell_mapper_probe.csv), [contract](../mapper_probe_contract.json), [full review](import_schema_review.json). No browser/account writes or credentials were used by this reviewer.
