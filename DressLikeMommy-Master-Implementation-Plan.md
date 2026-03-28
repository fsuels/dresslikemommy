# DRESS LIKE MOMMY — Master Implementation Plan (v2 — CORRECTED)
## Unified Strategy Across Google Ads, GA4, Merchant Center & GTM
**Date:** March 27, 2026 | **Site:** dresslikemommy.com | **Platform:** Shopify
**Version:** 2.0 — Corrected architecture based on current Google/Shopify guidance

---

## HOW TO USE THIS DOCUMENT

Each task below contains an **exact prompt** you copy-paste into an AI browser agent (like Claude in Chrome). The prompts tell the agent exactly where to go, what to do, and how to verify.

**Rules:**
- Tasks marked **🔴 SEQUENTIAL** must be done in the listed order — the next task depends on the previous one completing.
- Tasks marked **🟢 PARALLEL** can be done at the same time as other parallel tasks in the same phase.
- Phases 1 and 2 are independent workstreams and CAN run in parallel with each other.
- Phase 3 depends on Phase 0 being complete.
- Phase 5 (ad launch) depends on Phases 1, 2, 3, and 4 ALL being complete.
- After each task, verify the success metric before moving on.

---

## ARCHITECTURE DECISIONS

These are the governing decisions for the entire plan. Every prompt below follows these rules.

**1. Google & YouTube app = sole Google-tag deployment on Shopify.**
Current Google guidance (2025-2026) says to use the Google & YouTube app for all Google measurement on Shopify. Running Google tags in GTM or Shopify custom pixels is explicitly unsupported. We remove all duplicate Google tags from GTM, theme code, and custom pixels — and keep the Google & YouTube app as the source of truth for GA4, Google Ads conversion tracking, and Merchant Center feed sync.
*Sources: [Google Ads Help answer/16000892](https://support.google.com/google-ads/answer/16000892), [Tag Manager Help answer/15642481](https://support.google.com/tagmanager/answer/15642481)*

**2. GTM = dormant for Google tags. Active for non-Google tags only.**
GTM container GTM-5QVH4W3 will have its Google Tag and Conversion Linker removed. GTM remains useful ONLY for managing Facebook/Meta pixel, Bing UET, Pinterest, and any other non-Google third-party tags. This keeps those tags governed under one system.

**3. One purchase conversion for Google Ads bidding. Nothing else.**
Exactly one purchase action is Primary in Google Ads (the one fed by the Google & YouTube app's supported conversion path). All micro-conversions (add_to_cart, begin_checkout, view_item, page_view) are Secondary or observation-only. We do NOT run a second "redundant" purchase conversion tag.

**4. Feed fixes and measurement must both be green before any ad spend.**
Complete Phases 0-4 before enabling any campaigns in Phase 5. No exceptions.

**5. Merchant Center policies must match reality.**
Return policy, promotions, and shipping promises in Merchant Center must exactly match what the website and operations can actually honor. We do not inflate claims for better badges.

**6. add_shipping_info is treated as advanced/optional work.**
The GA4 Checkout Journey report needs this event, but implementing it on Shopify requires a custom pixel for Google tags — which is unsupported. This is Phase 7 (optional) work, done cautiously only after the supported stack is stable.

---

## PHASE 0: INVENTORY & DISCOVERY (Day 1)
*Everything in this phase is 🔴 SEQUENTIAL — do in exact order listed*
*CHANGE NOTHING in this phase. Document only.*

### Task 0.1: Complete Tag Inventory — Document Every Google Tag Source
**Audits:** GTM #4, GA4 #2, GTM Risk #5 | **Priority:** P0 | **Time:** 1 hour

**Why first:** Before removing anything, we need a complete picture of what's running. The other plan correctly identified this as the safest first step.

> **PROMPT FOR AI BROWSER AGENT:**
>
> Act as a change-controlled measurement auditor for dresslikemommy.com.
>
> **Do not change anything yet.** Your job is to produce a complete inventory of every Google-related tag source currently affecting the store.
>
> Check ALL of these places:
>
> 1. Shopify Admin → Sales channels → Google & YouTube → Settings
>    - Note: Is GA4 measurement ID configured? Which ID?
>    - Is Google Ads linked? Which account ID?
>    - Is Merchant Center linked? Which account ID?
>
> 2. Shopify Admin → Settings → Customer events
>    - List every custom pixel. For each: name, status (active/disabled), and whether it contains any Google tag IDs.
>
> 3. Shopify Admin → Settings → Checkout → Additional scripts (or Order status page scripts)
>    - Search for any Google tag snippets (gtag, GTM, AW-, G-, UA-)
>
> 4. Shopify Admin → Online Store → Themes → Current theme → Edit code
>    - Search ALL theme files for: gtag, GTM-, G-N4EQNK0MMB, GT-PJ5D7RB, AW-853411529, G-3VR0TDX4ZK, google-analytics.com, googletagmanager.com, googleadservices.com, MC-MQ104D130Y
>    - Note which files contain which IDs
>
> 5. Google Tag Manager container GTM-5QVH4W3 (https://tagmanager.google.com)
>    - List every tag, trigger, and variable in the container
>    - Note the current live version number
>
> 6. Check for installed Shopify apps that might inject Google tags:
>    - 123LegalDoc (known to inject G-3VR0TDX4ZK)
>    - Any other analytics/tracking apps
>
> Specifically look for these IDs:
> - GA4: G-N4EQNK0MMB
> - Google tag: GT-PJ5D7RB
> - GTM: GTM-5QVH4W3
> - Google Ads: AW-853411529
> - 123LegalDoc: G-3VR0TDX4ZK
> - Merchant Center: MC-MQ104D130Y
> - Shopify Channel App tags: GT-WRDD7FL, GT-WRH8Q3MD
>
> **Also inventory non-Google tags:**
> - Facebook/Meta pixel: 547553035448852
> - Bing UET tag ID
> - Pinterest tag ID
> - Any other tracking pixels
>
> Output a table with columns:
> | Source Location | Tag ID | Platform/Purpose | Active? | Deployed Via | Keep/Remove Recommendation | Why |
>
> **Do NOT disable or delete anything in this step.**

**Verify:** You have a complete table of every tag, from every source, with clear keep/remove recommendations.

---

### Task 0.2: Back Up Everything Before Changes
**Priority:** P0 | **Time:** 15 min

> **PROMPT FOR AI BROWSER AGENT:**
>
> Before we make any tracking changes to dresslikemommy.com, I need backups of everything:
>
> 1. Go to Shopify Admin → Online Store → Themes → Current theme → click "..." menu → "Duplicate"
>    - This creates a backup copy of the theme with all its code
>    - Name it: "BACKUP-PRE-TRACKING-CLEANUP-[today's date]"
>
> 2. Go to Google Tag Manager (https://tagmanager.google.com) → container GTM-5QVH4W3
>    - Go to Admin → Export Container
>    - Download the current container as a JSON file
>    - Note the current live version number
>
> 3. Go to Shopify Admin → Settings → Customer events
>    - For each custom pixel that exists, copy its FULL code and save it in a text document (screenshot or copy-paste)
>
> 4. If there's code in Shopify → Settings → Checkout → Additional scripts, copy that too
>
> Confirm all backups are saved. List what was backed up.

---

## PHASE 1: FIX DUPLICATE MEASUREMENT & CONSENT (Days 2-4)
*🔴 SEQUENTIAL — do in this exact order*
*This phase depends on Phase 0 being complete.*

### Task 1.1: Remove Duplicate Google Tags — Keep Only Google & YouTube App
**Audits:** GA4 #2, GTM Risk #1 | **Priority:** P0 | **Time:** 1-2 hours

> **PROMPT FOR AI BROWSER AGENT:**
>
> Using the tag inventory from the previous step, I need to remove all DUPLICATE Google tags from dresslikemommy.com. The architecture decision is:
>
> **KEEP:** Google & YouTube app as the ONLY Google-tag deployment path for Shopify.
>
> **REMOVE or DISABLE (based on inventory):**
>
> 1. **GTM Google tags:** Go to https://tagmanager.google.com → container GTM-5QVH4W3
>    - Find the Google Tag (GA4 config tag for G-N4EQNK0MMB) → DELETE it
>    - Find the Conversion Linker tag → DELETE it (the Google & YouTube app handles this)
>    - Do NOT delete the container itself — we'll use it for non-Google tags (Facebook, Bing, Pinterest)
>    - Do NOT publish yet — we'll publish after adding non-Google tags
>
> 2. **Custom Pixels:** Go to Shopify Admin → Settings → Customer events
>    - Any custom pixel containing Google tag IDs (G-N4EQNK0MMB, GT-PJ5D7RB, AW-853411529, GTM-5QVH4W3) → DISABLE it
>    - Do NOT disable pixels that only contain non-Google tags (Facebook, Bing, etc.)
>
> 3. **Theme code:** Go to Shopify Admin → Online Store → Themes → Edit code (on the LIVE theme, not the backup)
>    - Remove any hardcoded gtag.js snippets for G-N4EQNK0MMB or AW-853411529
>    - Remove any GTM container snippets (the head script and body noscript for GTM-5QVH4W3) **ONLY IF** we decide GTM is not needed for non-Google tags. If we're keeping GTM for Facebook/Bing/Pinterest, keep the GTM snippets.
>    - Remove any standalone Google Ads conversion tracking code
>
> 4. **123LegalDoc:** Go to Shopify Admin → Apps → find 123LegalDoc
>    - Disable its analytics tracking (G-3VR0TDX4ZK) or remove the app if it's not providing essential legal pages
>
> 5. **Checkout/additional scripts:** Go to Shopify Admin → Settings → Checkout → Additional scripts
>    - Remove any Google tag snippets there (the Google & YouTube app handles checkout tracking through its supported path)
>
> **DO NOT TOUCH:**
> - The Google & YouTube sales channel connection — this MUST remain active (it manages the feed sync AND measurement)
> - Non-Google tracking pixels (Facebook, Bing, Pinterest)
>
> **After removing duplicates:**
> - Go to Google & YouTube sales channel → Settings → verify GA4 measurement ID G-N4EQNK0MMB is still configured
> - Verify Google Ads account 399-097-6848 is still linked
> - Verify Merchant Center account 124884876 is still linked
> - Open the dresslikemommy.com site → open GA4 Real-time report → confirm events are still flowing (from the Google & YouTube app)
>
> **Output:** List every tag you removed/disabled, where it was, and confirm the Google & YouTube app is still the active measurement source. Include before/after screenshots if possible.

**Verify:** GA4 Real-time report shows events flowing. Only one source of Google tags remains (Google & YouTube app). No duplicate page_views in GA4 DebugView.

---

### Task 1.2: Clean Google Ads Conversion Actions
**Audits:** Google Ads Leak #1 | **Priority:** P0 | **Time:** 30 min

> **PROMPT FOR AI BROWSER AGENT:**
>
> I need to clean up conversion actions in Google Ads account 399-097-6848 so only ONE purchase action drives bidding.
>
> 1. Go to https://ads.google.com → account 399-097-6848
> 2. Navigate to Goals → Conversions → Summary
> 3. Inventory every conversion action in the account. List them all with their:
>    - Name
>    - Source (GA4, Google Ads tag, AdWords, etc.)
>    - Category (Purchase, Add to cart, Page view, etc.)
>    - Status (Recording, No recent, Needs attention)
>    - Primary vs Secondary designation
>    - Count (all time and last 30 days)
>
> 4. Make these changes:
>    - **Keep as PRIMARY:** The ONE purchase conversion that comes through the supported Google & YouTube app / Shopify path. This is likely either:
>      - The Google Ads purchase conversion auto-created by the Google & YouTube app, OR
>      - The GA4 purchase import — but ONLY if the Google & YouTube app's native Ads conversion is unavailable
>    - **Change to SECONDARY:** ALL of these:
>      - Any add_to_cart action
>      - Any begin_checkout action
>      - Any page_view or view_item action
>      - Any legacy AdWords pixel conversion actions
>      - Any old Universal Analytics imports
>      - Any duplicate purchase actions (keep only ONE as primary)
>    - **Archive:** Anything with "Needs attention" or "No recent conversions" status that is clearly obsolete
>
> 5. Verify auto-tagging is ON: Account Settings → Auto-tagging → confirm checked
> 6. Check enhanced conversions: Goals → Conversions → Settings → Enhanced conversions → should be ON. If it needs the Google & YouTube app path, note that and we'll configure it properly.
> 7. Check attribution model on the primary purchase action: should be "Data-driven"
>
> **Do NOT change campaign budgets, unpause campaigns, or modify campaign settings.**
>
> Output: Table of ALL conversion actions — what they were, what you changed them to, and the final state. Screenshot of the final conversion summary.

---

### Task 1.3: Deploy Consent Management
**Audits:** GTM Risk #3 | **Priority:** P0 (Legal) | **Time:** 2-4 hours

> **PROMPT FOR AI BROWSER AGENT:**
>
> I need to set up consent management on dresslikemommy.com that integrates with Google Consent Mode v2. The store currently has NO consent banner.
>
> **Part A — Shopify Customer Privacy Settings**
>
> 1. Go to Shopify Admin → Settings → Customer privacy
> 2. Check whether a cookie banner is already active
> 3. Check whether Google Consent Mode v2 is enabled in the customer privacy settings
> 4. If Shopify's built-in privacy settings support Google Consent Mode v2 (Shopify has been adding this natively), enable it with:
>    - Default consent for EU/EEA/UK visitors: ALL denied (ad_storage: denied, ad_user_data: denied, ad_personalization: denied, analytics_storage: denied)
>    - Default consent for US visitors: Follow Shopify's recommended US defaults
>    - Consent banner: Enable with Accept/Reject/Manage options
>
> 5. If Shopify's built-in settings are NOT sufficient for full Consent Mode v2:
>    - Go to Shopify App Store
>    - Install a consent app that integrates with Shopify's Customer Privacy API AND Google Consent Mode v2
>    - Recommended: Pandectes GDPR Compliance, CookieYes, or Consentmo
>    - Configure with the same defaults listed above
>
> **Part B — Verify consent signals reach Google tags**
>
> 6. Visit the site in an incognito window → consent banner should appear
> 7. Before accepting cookies, check: are Google tags being suppressed? (They should not fire until consent is granted for EU visitors)
> 8. Accept cookies → verify Google tags start firing
>
> **Part C — Verify with the Google & YouTube app**
>
> 9. Go back to Shopify Admin → Sales channels → Google & YouTube → check if there are any consent-related settings or warnings there
>
> Output: What was configured, which app (if any) was installed, and confirmation that consent mode is working. Screenshots of the banner and consent signal flow.

---

## PHASE 2: MERCHANT CENTER & PRODUCT FEED (Days 2-14)
*🟢 This entire phase runs in PARALLEL with Phase 1. They are independent workstreams.*
*Within Phase 2: Tasks 2.1-2.5 are 🟢 PARALLEL with each other. Tasks 2.6-2.7 depend on 2.1-2.5.*

### 🟢 PARALLEL BLOCK (Tasks 2.1–2.5)

### Task 2.1: Fix Corrupted Brand Attribute (1688.com URLs)
**Audits:** Merchant Center Problem #1 | **Priority:** P0 | **Time:** 1-2 hours

> **PROMPT FOR AI BROWSER AGENT:**
>
> The product feed for dresslikemommy.com has a critical issue: many products have their "brand" attribute set to Chinese wholesale marketplace URLs (like "https://detail.1688.com/offer/722909741976.html") instead of the brand name.
>
> **Step 1: Assess the scope (do NOT bulk-change yet)**
> 1. Go to Shopify admin → Products
> 2. The "Vendor" field maps to the "brand" attribute in the Google feed
> 3. Sample at least 20 products across different categories
> 4. For each, check the Vendor field — note which ones have:
>    - 1688.com URLs
>    - "dresslikemommy.com"
>    - "dress like mommy" (lowercase)
>    - "Dress Like Mommy" (correct)
>    - Any OTHER brand name that might be a legitimate third-party brand
>
> **Step 2: Determine if ALL products are house-brand**
> 5. Are there ANY products from legitimate third-party brands in the catalog? If yes, those should keep their real brand name — DO NOT override them with "Dress Like Mommy"
> 6. Tell me what you found before proceeding to bulk changes
>
> **Step 3: Fix house-brand products only (after I confirm)**
> 7. For products that ARE house-brand (confirmed), use Shopify's bulk editor:
>    - Select the affected products
>    - Change Vendor to "Dress Like Mommy" (exact capitalization)
>
> **Step 4: Backup via Merchant Center feed rule**
> 8. Go to https://merchants.google.com → account 124884876
> 9. Navigate to Products → Feeds → primary feed → Feed rules
> 10. Create a rule: IF brand contains "1688.com" THEN set brand to "Dress Like Mommy"
> 11. This catches anything the Shopify cleanup missed
>
> Output: Count of products sampled, vendor values found, whether any legitimate third-party brands exist, and what was changed.

---

### Task 2.2: Fix 69 Unavailable Product Pages
**Audits:** Merchant Center Problem #3 | **Priority:** P0 | **Time:** 1 hour

> **PROMPT FOR AI BROWSER AGENT:**
>
> In Google Merchant Center (account 124884876), 69 products are disapproved because their landing pages are unavailable.
>
> 1. Go to https://merchants.google.com → account 124884876
> 2. Navigate to Products → Diagnostics → find "Landing page not accessible" or "Product page unavailable"
> 3. Click into it to see the list of affected products
> 4. For each product:
>    a. Copy the URL and visit it — does it 404? Redirect? Load?
>    b. If it 404s: go to Shopify admin → Products → search for this product → check if it's unpublished or deleted
>    c. If it redirects: note the redirect destination
> 5. For products that are truly discontinued in Shopify:
>    - Set them to "Draft" status so they stop syncing to the feed
>    - OR set their Google & YouTube channel availability to "not available"
> 6. For products with fixable URL issues: repair the URL or republish
>
> Output: Count breakdown — how many were 404s, redirects, or other issues. What was fixed.

---

### Task 2.3: Fix Missing Prices + Create Return Policy + Fix Logos
**Audits:** Merchant Center Quick Wins | **Priority:** P0-P1 | **Time:** 45 min

> **PROMPT FOR AI BROWSER AGENT:**
>
> Three quick fixes in Google Merchant Center (account 124884876):
>
> **Fix 1: 23 products missing price**
> 1. Go to Merchant Center → Products → Diagnostics → "Missing price"
> 2. Note the product IDs/titles
> 3. Go to Shopify admin → Products → find each one → ensure every variant has a price set
>
> **Fix 2: Return policy in Merchant Center**
> 1. In Merchant Center → Shipping and returns → Return policies
> 2. Create a return policy that EXACTLY matches what your website currently says:
>    - If the site says 30-day free returns → set 30-day, free return shipping
>    - If the site says 14-day returns → set 14-day
>    - Do NOT set a longer window than what you actually honor
>    - Applies to: All products
>    - Return method: By mail (or whatever the site offers)
> 3. **IMPORTANT:** Before saving, verify the website's actual return policy page. Read it. The Merchant Center policy must match exactly. If there's any discrepancy, flag it for me rather than guessing.
>
> **Fix 3: Invalid logos**
> 1. In Merchant Center → Business information or Store settings → Logos
> 2. Upload a square logo (1:1 ratio, minimum 512×512 pixels) — the "Dress Like Mommy" brand logo
> 3. If a rectangular logo (2:1 ratio) is also needed, upload that too
> 4. Both should be PNG format with clean backgrounds
> 5. If you don't have the image files, tell me and we'll come back to this
>
> Output: Status of each fix. Confirmation that return policy matches the website.

---

### Task 2.4: Fix 33 Policy-Flagged Products
**Audits:** Merchant Center Scorecard #3 | **Priority:** P2 | **Time:** 1 hour

> **PROMPT FOR AI BROWSER AGENT:**
>
> In Google Merchant Center (account 124884876), 33 products are flagged for "personalized advertising: personal hardships."
>
> 1. Go to Merchant Center → Products → Diagnostics
> 2. Find the "Limited: Personalized advertising - personal hardships" issue
> 3. Click into it and review the affected products — note titles and descriptions
> 4. Identify which words are triggering the policy (for maternity/family brands, triggers often include: "maternity," "pregnant," "baby bump," health-related terms)
> 5. For each product, check the Shopify title and description
> 6. **Do NOT change anything yet** — give me the list of triggered products and the likely trigger words so I can decide how to rephrase
>
> This policy means the products can still show in regular Shopping results but cannot be used for personalized remarketing ads. In some cases, the flag may be acceptable and we leave it. I need the data to decide.
>
> Output: Table of all 33 products with: Product title | Likely trigger word(s) | Recommended action (rephrase/accept/escalate)

---

### Task 2.5: Clean Duplicate Shipping Policies
**Audits:** Merchant Center Scorecard #6 | **Priority:** P2 | **Time:** 15 min

> **PROMPT FOR AI BROWSER AGENT:**
>
> In Google Merchant Center (account 124884876), there are duplicate shipping policies for some countries (France and Israel reportedly have 4 entries each).
>
> 1. Go to Merchant Center → Shipping and returns → Shipping services
> 2. Review all shipping policies/services
> 3. For countries that have duplicate entries, remove the redundant ones — keep only the correct one
> 4. Also check: are there "Incomplete" countries (Chile, Colombia, Côte d'Ivoire, Jordan) with 0 products? If so, remove those incomplete entries to clean up the configuration
> 5. Do NOT change shipping rates or delivery times — only remove duplicates
>
> Output: What was removed, what remains.

---

### 🔴 SEQUENTIAL (After 2.1-2.5)

### Task 2.6: Build Supplemental Feed for Apparel Attributes
**Audits:** Merchant Center Problem #2, Google Ads Leak #2 | **Priority:** P1 | **Time:** 4-8 hours

**This is the highest-effort task in Phase 2 and one of the most impactful. 90% of products are missing required apparel attributes.**

> **PROMPT FOR AI BROWSER AGENT:**
>
> I need to build a Google Sheets supplemental feed for Google Merchant Center (account 124884876) to add missing apparel attributes to 4,540+ products. Currently 90.3% are missing age_group, 81.7% missing gender, 29.5% missing color.
>
> **Step 1: Confirm the product ID format**
> 1. Go to Merchant Center → Products → All products → click on any product
> 2. Note the exact product ID format (usually "shopify_US_[product_id]_[variant_id]")
> 3. Tell me the format before building the sheet
>
> **Step 2: Export Shopify product data**
> 1. Go to Shopify admin → Products → Export → Export all products as CSV
> 2. Download the file
>
> **Step 3: Build a PILOT supplemental feed (50 products first)**
> 1. Go to Google Sheets → create new spreadsheet → name it "DLM Supplemental Feed"
> 2. Columns: id | age_group | gender | color | size
> 3. The "id" column must exactly match the Merchant Center product IDs
> 4. Start with 50 products across different categories (dresses, swimsuits, t-shirts, family sets)
>
> Rules for populating:
> - **age_group:** Determine from product title AND size options:
>   - Women's sizes (S, M, L, XL, 0-16): "adult"
>   - Kids sizes (2T-14, or titled "girls/boys"): "kids"
>   - Toddler sizes (2T-5T): "toddler"
>   - Infant sizes (0-24M, NB): "infant"
>   - If a product has variants spanning multiple age groups, each variant gets its own row
>
> - **gender:** Determine from title and category:
>   - Women's/girls' dresses: "female"
>   - Men's/boys' outfits: "male"
>   - Family sets with both: "unisex"
>   - If uncertain, use "unisex" but FLAG it for review
>
> - **color:** Extract from title, variant name, or images:
>   - Use Google's accepted values (Red, Blue, Pink, Floral, Multicolor, etc.)
>   - If color is truly ambiguous, leave BLANK and flag for review
>
> - **size:** From Shopify variant options (S, M, L, XL, 2T, etc.)
>
> **Step 4: Connect the PILOT sheet to Merchant Center**
> 1. Go to Merchant Center → Products → Feeds → Add supplemental feed
> 2. Name: "Apparel Attributes Supplement"
> 3. Source: Google Sheets → select the sheet
> 4. Map columns → save
>
> **Step 5: Validate pilot**
> 5. Wait 24 hours → check Merchant Center diagnostics
> 6. Did the 50 products get their attribute warnings resolved?
> 7. Report results before scaling to the full catalog
>
> Output: Pilot sheet link, sample of how IDs/attributes map, validation results after 24 hours.

---

### Task 2.7: Optimize Product Titles in Feed
**Audits:** Merchant Center Scorecard #7 | **Priority:** P2 | **Time:** 2-4 hours

> **PROMPT FOR AI BROWSER AGENT:**
>
> I need to optimize product titles in my Google Merchant Center feed (account 124884876). Current issues: pipe characters (|), variant suffixes, and suboptimal keyword structure.
>
> Ideal apparel title format: Product Type + Key Attribute (Color/Pattern) + Target Audience
> Example: "Matching Mother Daughter Floral Maxi Dress - Pink"
>
> 1. Go to Merchant Center → Products → All products
> 2. Review 15-20 product titles across categories
> 3. Common fixes needed:
>    - Remove "| DLM" or "| Dress Like Mommy" suffix (brand is in the brand field)
>    - Remove or replace pipe characters "|" with hyphens
>    - Front-load product type and key attributes
>    - Remove variant suffixes like "/ S" or "/ Blue"
>
> 4. **Show me 5 before/after examples** across different product types BEFORE applying broadly
> 5. For scale: create feed rules in Merchant Center → Products → Feeds → primary feed → Feed rules
>    - Rule to strip pipe characters from titles
>    - Rule to remove brand suffix from titles
>
> Wait for my approval on the format before applying rules broadly.

---

## PHASE 3: GA4 & ANALYTICS CONFIGURATION (Days 4-14)
*🟢 This phase can start as soon as Phase 1, Task 1.1 is complete (duplicate tags removed)*
*All tasks in this phase are 🟢 PARALLEL with each other*

### Task 3.1: Add Unwanted Referral Exclusions
**Audits:** GA4 Category 6 | **Priority:** P1 | **Time:** 15 min

> **PROMPT FOR AI BROWSER AGENT:**
>
> I need to add unwanted referral exclusions in GA4 property 330266838 to prevent payment gateways from stealing attribution.
>
> 1. Go to https://analytics.google.com → property 330266838
> 2. Admin → Data streams → web stream (G-N4EQNK0MMB) → Configure tag settings → Show all → "List unwanted referrals"
>
> **Before adding anything:** First check current Referral traffic to see which payment domains are actually appearing:
> 3. Go to Reports → Acquisition → Traffic acquisition → look at Referral channel
> 4. Note any payment/checkout domains appearing as referrals
>
> **Then add these as unwanted referrals** (match type "Contains") — but ONLY if they make sense:
> - paypal.com (if you accept PayPal)
> - stripe.com (if you use Stripe)
> - shop.app (if Shop Pay is active)
> - klarna.com (if used)
> - afterpay.com (if used)
> - Any other payment domains you saw in the Referral report
>
> **DO NOT add:** dresslikemommy.com, checkout.shopify.com, or dresslikemommy-com.myshopify.com (these are handled by cross-domain tracking which is already configured correctly)
>
> Output: Which domains were added and why. Which were skipped and why.

---

### Task 3.2: Set Up Anomaly Detection Alerts
**Audits:** GA4 Category 10 | **Priority:** P1 | **Time:** 20 min

> **PROMPT FOR AI BROWSER AGENT:**
>
> Set up automated alerts in GA4 property 330266838 (dresslikemommy.com).
>
> 1. Go to https://analytics.google.com → property 330266838
> 2. Navigate to Home or Reports → find "Insights" or "Custom insights"
> 3. Create these alerts:
>
>    **Alert 1: "Purchase Drop"**
>    - Metric: Key event count (purchase)
>    - Condition: Decreases > 50% vs. same period previous week
>    - Email: ON → suelsferro@hotmail.com
>
>    **Alert 2: "Session Drop"**
>    - Metric: Sessions
>    - Condition: Decreases > 40% vs. previous week
>    - Email: ON → suelsferro@hotmail.com
>
>    **Alert 3: "Direct Traffic Spike"**
>    - Metric: Direct sessions increase > 30% vs. previous week
>    - Email: ON → suelsferro@hotmail.com
>
>    **Alert 4: "Engagement Time Drop"**
>    - Metric: Average engagement time drops below 20 seconds
>    - Email: ON → suelsferro@hotmail.com
>
> 4. Also configure Reports Snapshot: Reports → Reports snapshot → Customize → select "Generate leads and drive sales" or "Sales and revenue" template
>
> Output: Confirm all 4 alerts created and snapshot configured.

---

### Task 3.3: Update Key Events & Custom Dimensions
**Audits:** GA4 Category 4 | **Priority:** P1 | **Time:** 15 min

> **PROMPT FOR AI BROWSER AGENT:**
>
> Update key events and custom dimensions in GA4 property 330266838.
>
> 1. Go to https://analytics.google.com → Admin → property 330266838
> 2. Go to Events:
>    - Mark "view_item" as a key event (for reporting and audiences — NOT for Google Ads bidding)
>    - Mark "add_payment_info" as a key event
>    - **NOTE:** When these become key events, they'll be importable to Google Ads. Do NOT import them as Primary bidding conversions. They should remain Secondary/observation only if imported at all.
>
> 3. Go to Admin → Custom definitions → Custom dimensions
>    - Note the existing legacy dimensions (event_category, event_label) — leave them for now, we'll clean up later
>    - Create NEW custom dimension:
>      - Name: "Content Group"
>      - Scope: Event
>      - Event parameter: content_group
>      - Description: "Page type: homepage, collection, product, cart, blog, info"
>
> Output: Confirm key events marked and custom dimension created.

---

### Task 3.4: Build Remarketing Audiences
**Audits:** GA4 Category 9, Google Ads Action #11 | **Priority:** P2 | **Time:** 45 min

> **PROMPT FOR AI BROWSER AGENT:**
>
> Create remarketing audiences in GA4 (property 330266838) that sync to Google Ads (399-097-6848).
>
> Go to https://analytics.google.com → Admin → Audiences → Create:
>
> 1. **"High-Intent Browsers"**
>    - Include: view_item event 3+ times in last 7 days
>    - Exclude: add_to_cart in last 7 days
>    - Duration: 7 days
>
> 2. **"Cart Abandoners (14d)"**
>    - Include: add_to_cart in last 14 days
>    - Exclude: purchase in last 14 days
>    - Duration: 14 days
>
> 3. **"Checkout Abandoners (14d)"**
>    - Include: begin_checkout in last 14 days
>    - Exclude: purchase in last 14 days
>    - Duration: 14 days
>
> 4. **"Recent Purchasers (30d)"**
>    - Include: purchase in last 30 days
>    - Duration: 30 days
>
> 5. **"Lapsed Customers (31-180d)"**
>    - Include: purchase 31-180 days ago
>    - Exclude: purchase in last 30 days
>    - Duration: 180 days
>
> 6. **"All Visitors (30d)"**
>    - Include: session_start in last 30 days
>    - Duration: 30 days
>
> 7. **"All Visitors (90d)"**
>    - Include: session_start in last 90 days
>    - Duration: 90 days
>
> Verify each audience has "Enable personalized advertising" ON and will export to Google Ads.
>
> Also: Delete or archive legacy audiences: "New 540days - GA4", "Converted Audience - GA4" (from 2023).
>
> Output: List of audiences created with estimated sizes.

---

### Task 3.5: Investigate Bot/Direct Traffic
**Audits:** GA4 Category 5 | **Priority:** P1 | **Time:** 1 hour

> **PROMPT FOR AI BROWSER AGENT:**
>
> 59.4% of traffic to dresslikemommy.com is "Direct" with only 22.9% engagement rate and 8-second session duration. This suggests bot/spam traffic. Investigate.
>
> 1. Go to GA4 (property 330266838) → Explore → Create Free-form exploration
> 2. Dimensions: Landing page, Country, City, Device category, Browser, Session default channel group
> 3. Metrics: Sessions, Engagement rate, Average engagement time
> 4. Filter: Session default channel group = "Direct"
> 5. Sort by Sessions descending
>
> Look for patterns:
> - Specific landing pages getting all Direct traffic?
> - One country/city disproportionately?
> - One device type or browser?
> - Engagement times near 0 for certain segments?
>
> 6. Also check Reports → Acquisition → Traffic acquisition → Referral channel for suspicious referral domains
>
> **IMPORTANT:** Run this analysis AFTER the duplicate tags were removed (Task 1.1) — use only data from AFTER that date. The duplicate tag was inflating session counts and may have been the primary cause of the high Direct traffic. If Direct % has already dropped significantly post-cleanup, that's the answer.
>
> Output: Patterns found, % that appears to be bot vs. legitimate, whether the post-cleanup data already shows improvement, and recommended mitigation.

---

### Task 3.6: Cross-Validate GA4 Revenue Against Shopify
**Audits:** GA4 Action #12 | **Priority:** P1 | **Time:** 30 min

**Do this 7+ days after Task 1.1 (duplicate tag removal) so you have clean data to compare.**

> **PROMPT FOR AI BROWSER AGENT:**
>
> I need to verify GA4 revenue tracking matches Shopify after the tracking cleanup. Use data from the 7 days AFTER the duplicate Google tag was removed.
>
> 1. Go to Shopify admin → Analytics or Orders
>    - Pull: total revenue, number of orders, average order value for the last 7 clean days
>
> 2. Go to GA4 (property 330266838)
>    - Reports → Monetization → Overview
>    - Same 7-day period
>    - Pull: total revenue, number of purchases, average revenue per purchase
>
> 3. Go to Google Ads (399-097-6848)
>    - Campaigns → check conversion data for same period
>    - Is the purchase conversion showing any data?
>
> 4. Compare:
>    - Revenue match within ±10%? (±5% is ideal)
>    - Order/purchase count match?
>    - If GA4 > Shopify → still duplicating somewhere
>    - If GA4 < Shopify → missing conversions (ad blocker, consent denial, or tracking gap)
>
> Output: Exact numbers from all three sources, % discrepancy, and your assessment.

---

## PHASE 4: NON-GOOGLE TAG MANAGEMENT (Days 5-14)
*🟢 This phase runs in PARALLEL with Phase 3.*
*GTM is used here ONLY for non-Google tags (Facebook, Bing, Pinterest).*
*Tasks 4.1-4.3 are 🟢 PARALLEL.*

### Task 4.1: Consolidate Facebook/Meta Pixel into GTM
**Audits:** GTM Risk #5 | **Priority:** P1 | **Time:** 2 hours

> **PROMPT FOR AI BROWSER AGENT:**
>
> I need to move the Facebook/Meta pixel (ID: 547553035448852) into GTM container GTM-5QVH4W3 and remove the separate Shopify deployment. GTM is now used ONLY for non-Google tags.
>
> **Prerequisites:** Make sure the GTM container snippet (head + body) is still present in the Shopify theme (it should be, from the Phase 1 cleanup — we kept it for non-Google tags). If the GTM snippet was removed, we need to add it back first.
>
> **Step 1: Install Facebook Pixel template in GTM**
> 1. Go to https://tagmanager.google.com → container GTM-5QVH4W3
> 2. Tags → New → Tag Configuration → Community Template Gallery
> 3. Search for "Facebook Pixel" → install the official or most-used template
>
> **Step 2: Create Facebook tags (all in a "Meta" folder)**
>
> First, create a "Meta" folder if it doesn't exist.
>
> Tag 1: "Meta - PageView - All Pages"
> - Pixel ID: 547553035448852
> - Event: PageView
> - Trigger: All Pages
> - Consent: Require ad_storage = Granted (if consent is wired through GTM; if consent is handled by Shopify Customer Privacy API, the tag may fire unconditionally and Shopify handles consent)
>
> Tag 2: "Meta - ViewContent - Product View"
> - Event: ViewContent
> - You'll need to set up dataLayer variables if Shopify pushes product data to the dataLayer. Check what data is available.
> - Trigger: Custom Event for view_item (or Page Path contains /products/)
>
> Tag 3: "Meta - AddToCart"
> - Event: AddToCart
> - Trigger: Custom Event for add_to_cart
>
> **Note on checkout events:** Facebook purchase tracking on Shopify checkout is best handled through a Shopify custom pixel for Facebook (not GTM, since GTM can't reach checkout pages). Check if there's already a Facebook custom pixel in Shopify → Settings → Customer events. If yes, keep that for checkout events.
>
> **Step 3: Remove the old Facebook deployment**
> 1. Check Shopify → Apps for Facebook/Meta Commerce Manager app
> 2. Check theme code for "547553035448852" or "fbq"
> 3. Remove hardcoded pixel code from theme (GTM handles pre-checkout pages now)
> 4. Keep any Shopify custom pixel for Facebook that handles checkout/purchase (Facebook in custom pixels IS allowed — only Google tags are unsupported there)
>
> **Step 4: Test**
> - Use GTM Preview mode + Facebook Pixel Helper Chrome extension
> - Verify PageView fires on all pages
> - Verify ViewContent fires on product pages
> - Verify AddToCart fires when adding to cart
>
> Do NOT publish until validated.
>
> Output: Tags created, test results, what was removed.

---

### Task 4.2: Consolidate Bing UET into GTM
**Audits:** GTM Risk #5 | **Priority:** P2 | **Time:** 1 hour

> **PROMPT FOR AI BROWSER AGENT:**
>
> Migrate Bing UET tag into GTM container GTM-5QVH4W3 and remove the separate deployment.
>
> 1. Go to https://tagmanager.google.com → container GTM-5QVH4W3
> 2. First, find the Bing UET tag ID: visit dresslikemommy.com → developer tools → search page source/Network for "bat.bing.com" or "uetq" → note the tag ID
> 3. Create a "Microsoft" folder in GTM
> 4. Create tag:
>    - Name: "Microsoft - UET - All Pages"
>    - Type: Search Community Template Gallery for "Microsoft UET" or "Bing UET"
>    - UET Tag ID: [the ID you found]
>    - Trigger: All Pages
>
> 5. Remove the old Bing deployment:
>    - Check Shopify apps for Microsoft/Bing advertising app
>    - Check theme code for "bat.bing.com" or the tag ID
>    - Remove hardcoded code
>
> 6. Test in GTM Preview
>
> Output: Tag created, old deployment removed, test results.

---

### Task 4.3: Publish GTM Container (Non-Google Tags Only)
**Priority:** P1 | **Time:** 30 min

> **PROMPT FOR AI BROWSER AGENT:**
>
> Time to publish the GTM container with the non-Google tags. Go to https://tagmanager.google.com → container GTM-5QVH4W3.
>
> **Pre-publish checklist:**
> 1. Verify the container has NO Google tags (no GA4 config, no Google Ads tags, no Conversion Linker)
> 2. Verify it HAS: Facebook/Meta pixel tags, Bing UET tag, and any Pinterest tags
> 3. All tags should be organized in folders (Meta, Microsoft, Pinterest, Utility)
>
> **Test in Preview mode:**
> - Homepage → PageView fires for Facebook and Bing
> - Product page → ViewContent fires for Facebook
> - Add to cart → AddToCart fires for Facebook
> - Spanish locale page (/es/) → all tags fire (this verifies the /es/ locale tag coverage fix)
>
> **If all tests pass:**
> 4. Submit → Publish
> 5. Version name: "v[X] - Non-Google tag consolidation (Facebook, Bing)"
> 6. Description: "Consolidated Facebook pixel and Bing UET into GTM. Removed Google tags from GTM (Google measurement handled by Shopify Google & YouTube app). All tags in folders with naming convention."
>
> **After publishing:** Monitor for 30 minutes. Check Facebook Events Manager and Bing UET validation.
>
> Output: Published version number, test results, confirmation.

---

## PHASE 5: GOOGLE ADS REBUILD (Days 14-30)
*🔴 Do NOT start this phase until ALL of these launch gates are met:*
- *✅ Duplicate Google tag resolved (only Google & YouTube app remains)*
- *✅ Exactly one purchase conversion is Primary in Google Ads*
- *✅ Auto-tagging is ON, enhanced conversions enabled*
- *✅ Merchant Center brand corruption is fixed*
- *✅ Missing prices fixed, unavailable URLs fixed*
- *✅ Apparel attributes largely populated (supplemental feed live)*
- *✅ Shopify vs GA4 vs Google Ads purchases reconcile within ±10% over 7 clean days*
- *✅ Old campaigns remain paused/archived*

### Task 5.1: Build Negative Keyword List
**Audits:** Google Ads Leak #4 | **Priority:** P1 | **Time:** 2 hours
*🟢 This task can be done anytime — start it during Phase 2-3 if you want.*

> **PROMPT FOR AI BROWSER AGENT:**
>
> Build a comprehensive negative keyword list for a "mommy and me" / matching family outfits ecommerce store. I need 200+ terms organized by category.
>
> **Category 1: DIY/Sewing/Crafts** (people wanting to MAKE outfits, not buy)
> Include: sewing pattern, DIY, how to make, tutorial, crochet, knit, fabric, pattern download, free pattern, handmade, template, craft, stitch, embroidery, quilt
>
> **Category 2: Competitor/Other Brands**
> Research and include: top mommy-and-me dress brands, PatPat, Primary, Hanna Andersson, Carter's, Old Navy, Amazon, Shein, Temu + any other brand names you can identify
>
> **Category 3: Irrelevant Products**
> Include: dog matching, pet matching, pet outfit, costume, halloween, cosplay, doll clothes, barbie, american girl, outfit ideas, inspiration board
>
> **Category 4: Informational/Non-Purchase Intent**
> Include: what is, meaning, definition, ideas, inspiration, pinterest, instagram, tiktok, blog, article, review, reddit, forum, youtube, how to, tips
>
> **Category 5: Wholesale/Resale**
> Include: wholesale, supplier, manufacturer, dropship, alibaba, 1688, resell, bulk order, white label, private label
>
> **Category 6: Free/Budget-Extreme**
> Include: free, second hand, used, thrift, goodwill, consignment
>
> **Category 7: Wrong Geography**
> Include: near me, pickup, in store, local, same day delivery
>
> **Category 8: Wrong Product Types**
> Include: shoes only, jewelry only, accessories only, formal wear, wedding, bridesmaid, prom (unless you sell these — check the site first)
>
> Format the list for Google Ads import: one keyword per line. Use phrase match (quotes around multi-word terms) for most. Use exact match [brackets] for single ambiguous words.
>
> Output: Complete list organized by category, 200+ terms total.

---

### Task 5.2: Create Brand Search Campaign
**Audits:** Google Ads Action #6 | **Priority:** P1 | **Time:** 1.5 hours

> **PROMPT FOR AI BROWSER AGENT:**
>
> Create a new Brand Search campaign in Google Ads (account 399-097-6848). Do NOT unpause any existing campaigns.
>
> **Campaign: "Search - Brand"**
> - Goal: Sales
> - Network: Google Search ONLY (uncheck Display Network AND Search Partners)
> - Locations: United States
> - Language: English
> - Budget: $10/day (conservative start)
> - Bidding: Maximize conversion value (no target ROAS yet — not enough data)
>
> **Ad Group 1: "Brand - Exact"**
> Keywords (exact match):
> - [dress like mommy]
> - [dresslikemommy]
> - [dresslikemommy.com]
> - [dress like mommy store]
> - [dress like mommy shop]
> - [dlm dresses]
>
> **Ad Group 2: "Brand - Phrase"**
> Keywords (phrase match):
> - "dress like mommy"
> - "dresslikemommy"
>
> **RSA Ad (create 1 per ad group):**
> Headlines (15):
> 1. Dress Like Mommy® Official Site
> 2. Matching Mother & Daughter Dresses
> 3. Mommy and Me Outfits
> 4. Free Shipping on Every Order
> 5. Family Matching Outfits
> 6. Shop New Arrivals Today
> 7. Matching Family Dresses & Sets
> 8. Cute Mommy & Me Dresses
> 9. Shop the Full Collection
> 10. Quality Family Matching Wear
> 11. Free Returns on All Orders
> 12. Matching Swimsuits for Family
> 13. New Styles Added Weekly
> 14. Mother Daughter Dress Sets
> 15. Matching Outfits for Every Occasion
>
> Descriptions (4):
> 1. Shop our collection of matching mommy and me dresses, family outfits & swimsuits. Free shipping on every order!
> 2. Quality matching outfits for mothers and daughters. New arrivals weekly. Free shipping & easy returns.
> 3. Dress Like Mommy — where families match in style. Dresses, swimsuits & matching sets. Shop now!
> 4. Find the perfect matching outfit for you and your little one. Adorable designs, quality fabrics. Order today.
>
> Pin "Dress Like Mommy® Official Site" to Headline 1 position.
>
> **Extensions:**
> - Sitelinks: New Arrivals, Best Sellers, Matching Swimsuits, Matching Dresses, Family Sets
> - Callouts: Free Shipping, Free Returns, New Styles Weekly, Family Matching
> - Structured snippets: Types → Dresses, Swimsuits, T-Shirts, Pajamas, Sweaters
>
> Final URL: https://www.dresslikemommy.com
>
> **Apply the negative keyword list from Task 5.1.**
>
> Set to PAUSED — do not enable yet.
>
> Output: Campaign created, all settings confirmed, ad strength score.

---

### Task 5.3: Create Non-Brand Search Campaign
**Audits:** Google Ads Action #7 | **Priority:** P1 | **Time:** 2 hours

> **PROMPT FOR AI BROWSER AGENT:**
>
> Create a Non-Brand Search campaign in Google Ads (account 399-097-6848).
>
> **Campaign: "Search - Non-Brand"**
> - Goal: Sales
> - Network: Google Search ONLY (uncheck Display, uncheck Search Partners)
> - Locations: United States
> - Language: English
> - Budget: $25/day
> - Bidding: Maximize conversions (no target CPA yet)
>
> **Ad Group 1: "Mommy and Me Dresses"**
> Keywords:
> - [mommy and me dresses] | "mommy and me dresses"
> - [mother daughter matching dresses] | "mother daughter matching dresses"
> - [matching mom and daughter outfits] | "matching mom and daughter outfits"
> - [mommy and me matching dresses] | "mommy and me matching dresses"
> - [mom and daughter dresses] | "mom and daughter dresses"
> Final URL: best matching collection page (e.g., /collections/matching-dresses or /collections/all)
>
> **Ad Group 2: "Family Matching Outfits"**
> Keywords:
> - [family matching outfits] | "family matching outfits"
> - [matching family clothes] | "matching family clothes"
> - [matching family dresses] | "matching family dresses"
> - [family matching sets] | "family matching sets"
> Final URL: appropriate collection page
>
> **Ad Group 3: "Matching Swimsuits"**
> Keywords:
> - [mommy and me swimsuits] | "mommy and me swimsuits"
> - [matching mother daughter swimsuits] | "matching mother daughter swimsuits"
> - [matching family swimwear] | "matching family swimwear"
> - [mommy and me bathing suits] | "mommy and me bathing suits"
> Final URL: /collections/swimsuits or similar
>
> **For each ad group:** Create 1 RSA with:
> - 10+ headlines specific to that product category
> - 4 descriptions
> - Include "Free Shipping" in at least one headline
> - Pin the most product-specific headline to position 1
> - Ad strength must be "Good" or "Excellent"
>
> **Extensions:** Same as Brand campaign (sitelinks, callouts, structured snippets)
>
> **Apply the negative keyword list from Task 5.1.**
>
> Set to PAUSED.
>
> Output: Campaign structure, keyword list, ad strength scores.

---

### Task 5.4: Create Standard Shopping Campaign
**Audits:** Google Ads Action #8 | **Priority:** P1 | **Time:** 1 hour

> **PROMPT FOR AI BROWSER AGENT:**
>
> Create a Standard Shopping campaign in Google Ads (account 399-097-6848).
>
> **GATE CHECK FIRST:** Before creating this campaign:
> 1. Go to Google Merchant Center (124884876) → Products → Diagnostics
> 2. What % of products are now eligible?
> 3. If LESS than 80% are eligible, STOP — tell me the current eligibility rate and we'll fix the feed more before creating this campaign
>
> **If 80%+ eligible, create:**
>
> **Campaign: "Shopping - All Products"**
> - Campaign type: Shopping
> - Merchant Center: 124884876
> - Network: Google Search ONLY (uncheck Search Partners initially)
> - Locations: United States
> - Budget: $25/day
> - Bidding: Maximize clicks with a max CPC bid limit of $0.50 (conservative start — we'll switch to Target ROAS after 30+ conversions)
> - Products: All products
> - Campaign priority: Medium
>
> Set to PAUSED.
>
> Verify: Check the "Products" tab — how many products are eligible and showing?
>
> Output: Campaign created, product eligibility count, settings confirmed.

---

### Task 5.5: Apply Negatives, Final Review & LAUNCH
**Audits:** Google Ads Leak #4, Final Recommendation | **Priority:** P1 | **Time:** 45 min

> **PROMPT FOR AI BROWSER AGENT:**
>
> Final pre-launch review and then LAUNCH.
>
> **Step 1: Apply negative keywords**
> 1. Go to Google Ads (399-097-6848) → Tools → Shared library → Negative keyword lists
> 2. Create shared list: "Master Negatives - DLM"
> 3. Add ALL negative keywords from Task 5.1
> 4. Apply to ALL three new campaigns
>
> **Step 2: Pre-launch checklist (verify EVERY item):**
> - [ ] Network: Google Search only on all campaigns (no Display Network)
> - [ ] Location: United States only
> - [ ] Language: English
> - [ ] Negative keyword list applied to all 3 campaigns
> - [ ] Ad strength: "Good" or "Excellent" on all RSAs
> - [ ] Extensions: sitelinks + callouts approved
> - [ ] Conversion tracking: Primary purchase action status = "Recording conversions" or "Tag active"
> - [ ] Auto-tagging: ON
> - [ ] Enhanced conversions: Enabled
> - [ ] Budgets: $10 (Brand) + $25 (Non-Brand) + $25 (Shopping) = $60/day total
> - [ ] Old campaigns: ALL still paused/archived (do not touch them)
>
> **Step 3: If ALL checklist items pass → LAUNCH**
> 5. Enable all three campaigns (Paused → Enabled)
> 6. Wait 30 minutes, then check:
>    - Are impressions flowing?
>    - Any ad disapprovals?
>    - Any campaign warnings?
>
> Total daily budget at launch: $60/day (~$1,800/month)
>
> Output: Checklist results (pass/fail for each item), launch confirmation, initial impression data.

---

## PHASE 6: OPTIMIZATION & REPORTING (Days 30-90)
*All tasks are 🟢 PARALLEL and ongoing*

### Task 6.1: Weekly Search Terms Review
**Run every Wednesday | 30 min**

> **PROMPT FOR AI BROWSER AGENT:**
>
> Review search terms report for Google Ads account 399-097-6848 — last 7 days.
>
> 1. Go to Google Ads → Insights & Reports → Search terms → Last 7 days → sort by Impressions
> 2. For each term: KEEP (relevant), ADD AS NEGATIVE (irrelevant), or ADD AS NEW KEYWORD (converting opportunity)
> 3. Add irrelevant terms to "Master Negatives - DLM" shared list
> 4. Note new keyword opportunities
> 5. Check Quality Scores — flag any keyword below 5/10
>
> Output: New negatives added (count + terms), new keyword opportunities, Quality Score concerns.

---

### Task 6.2: Build Looker Studio Dashboard
**One-time setup | 2-3 hours**

> **PROMPT FOR AI BROWSER AGENT:**
>
> Create a weekly performance dashboard in Looker Studio connecting GA4 (property 330266838) and Google Ads (399-097-6848).
>
> Go to https://lookerstudio.google.com → Create report → Connect both data sources.
>
> **Section 1: Revenue KPIs** (scorecards with comparison to prior period)
> - Revenue, Purchases, Conversion Rate, Average Order Value
>
> **Section 2: Traffic & Channels** (table + pie chart)
> - Sessions by channel, engagement rate, key events
> - Direct traffic % scorecard (flag if >35%)
>
> **Section 3: Google Ads Performance** (table)
> - Spend, clicks, conversions, ROAS by campaign
> - Cost per conversion trend line
>
> **Section 4: Funnel** (bar chart with conversion rates)
> - view_item → add_to_cart → begin_checkout → purchase
>
> **Section 5: Top Products** (table)
> - Top 10 products by revenue, products with high clicks but 0 conversions
>
> Default date range: Last 28 days vs. previous period.
> Schedule weekly email: Mondays → suelsferro@hotmail.com
>
> Output: Dashboard URL.

---

### Task 6.3: Merchant Center Ongoing Governance
**Run every Monday | 15 min**

> **PROMPT FOR AI BROWSER AGENT:**
>
> Weekly Merchant Center health check for account 124884876.
>
> 1. Go to Merchant Center → Needs attention / Diagnostics
> 2. Check: any NEW disapprovals since last week?
> 3. Check: overall product approval rate — should be 95%+
> 4. Check: any new policy issues?
> 5. Check: feed sync status (last sync date, any "Needs update" warnings)
> 6. If any new issues: document them and flag for immediate fix
>
> Output: Current approval rate, new issues (if any), feed sync status.

---

### Task 6.4: Set Up Promotion (With Coupon Code)
**Audits:** Merchant Center Problem #5 | **Priority:** P2 | **Time:** 30 min

**NOTE: Google Merchant Center requires a valid redemption code for all shipping promotions. A "free shipping" promotion without a coupon code will be rejected.**

> **PROMPT FOR AI BROWSER AGENT:**
>
> I want to create a promotion in Google Merchant Center (124884876) to get promotional annotations on Shopping listings.
>
> **Before creating anything:**
> 1. Go to dresslikemommy.com and check: is there currently a promo code or coupon active on the site? (Check homepage banners, checkout page, any popup)
> 2. If there IS an active coupon code (like "SHIP10" or "WELCOME15"), we'll use that
> 3. If there is NO active coupon, I need to create one in Shopify first — tell me and we'll set that up
>
> **If a valid coupon exists:**
> 4. Go to Merchant Center → Marketing → Promotions → Create
> 5. Promotion type: Whatever matches the real offer (% off, $ off, or free shipping WITH coupon code)
> 6. Generic redemption code: [the actual coupon code from the site]
> 7. Title: [matches the actual offer — e.g., "15% Off with code WELCOME15"]
> 8. Applies to: All products (or specific products if the promo is limited)
> 9. Start/end dates: Match the actual promotion period
> 10. Destinations: Free listings AND Shopping ads
>
> **IMPORTANT RULES:**
> - Free shipping promotions REQUIRE a coupon code — Google rejects "automatic" free shipping promotions
> - The promotion must match EXACTLY what the website honors
> - Do NOT create fake or temporary offers just to get a badge
>
> **Also check Shopify sale prices:**
> 11. In Shopify admin → Products → are any products using "Compare at price" (strikethrough pricing)?
> 12. If yes, verify the Google & YouTube channel is syncing compare_at_price as sale_price to Merchant Center
> 13. This enables "Sale" badges on Shopping listings for those products
>
> Output: Promotion created (or coupon code needed), sale price sync status.

---

### Task 6.5: Transition to PMax (After 50+ Conversions)
**DO NOT do until Standard Shopping has 50+ conversions**

> **PROMPT FOR AI BROWSER AGENT:**
>
> Standard Shopping has generated [X] conversions at [X] ROAS. Time to test Performance Max.
>
> 1. Go to Google Ads (399-097-6848) → Create new PMax campaign:
>    - Name: "PMax - All Products"
>    - Merchant Center: 124884876
>    - Budget: Same as current Shopping budget
>    - Bidding: Target ROAS (set to 80% of current Shopping ROAS as conservative start)
>
> 2. Asset Groups (organize by product type):
>    - "Mommy & Me Dresses" — filter to dresses, add relevant images/headlines/descriptions
>    - "Family Matching Sets" — filter to sets
>    - "Matching Swimsuits" — filter to swimwear
>
> 3. Audience Signals (from GA4 audiences):
>    - Cart Abandoners, Checkout Abandoners, High-Intent Browsers
>    - In-market: Women's Clothing, Children's Clothing
>
> 4. Creative assets: 5+ images, 5+ headlines, 5+ descriptions, logo
>
> 5. Enable PMax → Reduce Shopping budget by 50% → After 2 weeks, if PMax meets targets, pause Shopping
>
> Output: Campaign setup, asset groups, initial status.

---

## PHASE 7: OPTIONAL — ADVANCED (After 90 Days)
*Only after the supported stack is stable and producing clean data*

### Task 7.1: Prototype add_shipping_info Event
**Audits:** GA4 Category 3, Category 8 | **Priority:** P3 | **Time:** Varies

**WARNING:** This requires a Google tag inside a Shopify custom pixel, which Google explicitly says is unsupported. Proceed with caution and only if the checkout funnel gap is preventing meaningful optimization.

> **PROMPT FOR AI BROWSER AGENT:**
>
> This is an OPTIONAL, ADVANCED task. Handle cautiously.
>
> The GA4 Checkout Journey report is missing add_shipping_info. The Google & YouTube app tracks begin_checkout, add_payment_info, and purchase — but NOT add_shipping_info.
>
> **Goal:** Prototype the lightest possible implementation.
>
> 1. Confirm current state: In GA4 (330266838), check Events → is add_shipping_info present? What about begin_checkout, add_payment_info, purchase?
>
> 2. Check Shopify → Settings → Customer events for the checkout_shipping_info_submitted standard event availability
>
> 3. The implementation would require a Shopify custom pixel that listens for checkout_shipping_info_submitted and sends add_shipping_info to GA4. This IS technically possible but IS an unsupported Google tag implementation on Shopify.
>
> 4. **Design but DO NOT deploy yet.** Give me:
>    - The proposed implementation code
>    - Whether it's supported or unsupported
>    - The risk of it reintroducing duplicate pageviews or purchases
>    - A go/no-go recommendation
>
> I will decide whether to proceed.
>
> Output: Implementation proposal, support status, risk assessment, recommendation.

---

## COMPLETE DEPENDENCY MAP

```
PHASE 0 (Day 1) ─── INVENTORY & BACKUP
  ├── 0.1 Tag inventory (change nothing) 🔴
  └── 0.2 Back up everything 🔴

  ↓ must complete

PHASE 1 (Days 2-4)                     ║  PHASE 2 (Days 2-14)
  FIX MEASUREMENT & CONSENT             ║  MERCHANT CENTER & FEED
  ├── 1.1 Remove duplicate tags 🔴      ║  ├── 2.1 Fix brand attribute 🟢
  ├── 1.2 Clean Ads conversions 🔴      ║  ├── 2.2 Fix 69 broken pages 🟢
  └── 1.3 Deploy consent 🔴             ║  ├── 2.3 Prices + return policy 🟢
      (These run in parallel ↔)          ║  ├── 2.4 Policy-flagged products 🟢
                                         ║  ├── 2.5 Clean shipping policies 🟢
                                         ║  ├── 2.6 Supplemental feed 🔴 (after 2.1)
                                         ║  └── 2.7 Title optimization 🔴

  ↓ Phase 1.1 done                       ↓ independent

PHASE 3 (Days 4-14) ─ GA4 SETUP         PHASE 4 (Days 5-14) ─ NON-GOOGLE TAGS
  ├── 3.1 Referral exclusions 🟢        ├── 4.1 Facebook → GTM 🟢
  ├── 3.2 Anomaly alerts 🟢             ├── 4.2 Bing → GTM 🟢
  ├── 3.3 Key events + dimensions 🟢    └── 4.3 Publish GTM 🔴
  ├── 3.4 Build audiences 🟢
  ├── 3.5 Bot traffic investigation 🟢
  └── 3.6 Revenue cross-validation 🟢
      (7 days after 1.1)

  ↓ ALL launch gates must be green

PHASE 5 (Days 14-30) ─── GOOGLE ADS REBUILD
  ├── 5.1 Negative keyword list 🟢 (start anytime)
  ├── 5.2 Brand Search campaign 🔴
  ├── 5.3 Non-Brand Search campaign 🔴
  ├── 5.4 Shopping campaign 🔴
  └── 5.5 Apply negatives + LAUNCH 🔴

  ↓ 30+ days of data

PHASE 6 (Days 30-90) ─── OPTIMIZE
  ├── 6.1 Weekly search terms 🟢
  ├── 6.2 Looker Studio dashboard 🟢
  ├── 6.3 MC weekly governance 🟢
  ├── 6.4 Promotion setup 🟢
  └── 6.5 PMax transition (50+ conv) 🔴

PHASE 7 (90+ days) ─── OPTIONAL ADVANCED
  └── 7.1 add_shipping_info prototype
```

---

## LAUNCH GATES CHECKLIST

Do NOT launch ads until ALL are true:

- [ ] Google tag duplication resolved — only Google & YouTube app remains
- [ ] Exactly one purchase conversion is Primary in Google Ads
- [ ] Auto-tagging is ON, GCLID is not being stripped
- [ ] Enhanced conversions enabled via supported path
- [ ] Merchant Center brand corruption fixed
- [ ] Missing prices fixed, unavailable URLs fixed or excluded
- [ ] Required apparel attributes populated on 80%+ of products
- [ ] Shopify vs GA4 vs Google Ads purchases reconcile within ±10% over 7 clean days
- [ ] Consent management deployed and working
- [ ] Old campaigns remain paused/archived
- [ ] Negative keyword list built and ready to apply
- [ ] Only new simplified campaign structure will be launched

---

## TARGET STATE AT 90 DAYS

| Metric | Current | Target |
|--------|---------|--------|
| Google tag sources | 4+ (duplicate) | 1 (Google & YouTube app) |
| Product feed eligibility | 0% | 95%+ |
| GA4 ecommerce events | 5/12 | 8/12 (add_shipping_info deferred) |
| Active campaigns | 0 | 3-5 |
| Daily ad budget | $0 | $60-150 |
| Ecommerce conversion rate | 0.22% | 0.5%+ |
| Blended ROAS | Unknown | 3x+ |
| Direct traffic share | 59.4% | <30% |
| Negative keywords | 0 | 200+ |
| Remarketing audiences | 1 (expired) | 7+ active |
| Consent management | None | Full Consent Mode v2 |
| Weekly review cadence | None | Mon/Wed/Fri |

---

## ASSUMPTIONS

- "Dress Like Mommy" is the correct canonical brand name
- The site truly offers the return/shipping terms found in the audit
- There are no meaningful third-party brands in the catalog
- Launch budgets ($60/day) are affordable — adjust based on your actual margins and cash flow
- Target ROAS and Target CPA should be set from gross margin data when available

If any assumption is wrong, adjust the relevant prompts before executing.

---

*Document v2.0 — March 27, 2026*
*Corrected architecture: Google & YouTube app for Google measurement, GTM for non-Google tags only*
*Merged best practices from two independent audit analyses*
