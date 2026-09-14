# Merchant daily operation — September 14, 2026

The ongoing goal is active. One daily heartbeat now resumes this existing Merchant task at **9 a.m. and 5 p.m. New York time**. Its persisted status, target and prompt were verified; the parent and other channel automations remain intact. A scheduled run still depends on local Codex/runtime availability.

This cycle implemented the existing feed pipeline's global translation inheritance and explicit translation-only exclusion mode. Exact-market overrides retain their stale flags; invalid price, identity, image, publication, currency or landing data cannot be hidden by a translation exclusion. English defaults remain unchanged. The independent review found a replay timestamp defect; it was fixed by recording original source observations in the existing checkpoint journal, with a conservative job-start fallback for older entries. **47 tests pass**, and independent review is **PASS_WITH_LIMITS**. No deployment or foreign source submission occurred.

Current Merchant country readiness directly shows **US 4,741/4,741 approved** and **Australia 4,741/4,741 approved**. Free listings are Active/On and the domain is Verified/Claimed. Canada and ten other rendered countries have zero products. Only 13 country rows were captured; this is not an exhaustive live matrix.

Store Quality still shows **No score**. Apple Pay, Google Pay and Shop Pay already exist but are pending Google review, so they were not duplicated. Current logo status was not verified. Shipping/return truth and effective country assignment remain separate from product approval. [Google's Store Quality guidance](https://support.google.com/merchants/answer/14261098?hl=en) says missing ratings can reflect missing information or insufficient impressions, and policy updates can take up to 30 days to affect the score.

The [operating plan](operating_plan.json) tracks daily execution, US/AU maintenance, multilingual lifecycle, US Spanish, Canada/UK, remaining country/language coverage, customer trust, and actual customer/profit evidence. A fresh translation flag is not full language QA, and approval is not evidence of impressions or sales.

**Next action:** the existing UX owner must complete the two exact Spanish variant-entry repairs and buyer readbacks. The Spanish file remains withheld by its real landing-context gate. Its frozen partition is 4,552 potential offers, 189 available offers with stale content, 162 existing-held available offers, and 22 unavailable variants. Canada/UK fresh-source qualification remains a separate queued lane; their September11 files must not be uploaded as current data.

Changed runtime files: collector.js, generator.js and checkpoint.js, plus their existing feed and checkpoint tests. No new service, harness or dependency was created. Current live US/AU files, six holds, business settings, theme, product data, translations, paid settings and security were preserved. All shared canonical edits remain with the parent integrator.

Continue through the existing canonical paid-growth continuation prompt and this task's latest checkpoint; no additional owner prompt is needed for the scheduled work.
