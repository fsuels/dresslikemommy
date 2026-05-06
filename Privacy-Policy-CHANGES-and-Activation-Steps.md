# Privacy Policy Update — Change Summary & Google Ads Activation Steps

**Goal:** Make it safe for FKG Trading LLC (Dress Like Mommy) to confirm Google Ads' "Turn on conversion-based Customer lists" policy compliance dialog.

---

## 1. What changed in your privacy policy

I rewrote the policy at `Privacy-Policy-REVISED.md`. The legally important edits:

### Section 3 — How We Use Your Information
- **Added:** "Measure advertising performance, attribute conversions, and deliver personalized advertising on platforms such as Google (Google Ads, YouTube, Search, Display, Gmail) and other advertising partners."
- **Added:** "Build audiences of existing or similar customers."
- **Replaced** the line "We will never sell your personal information to third parties" with a more accurate, CCPA-aware version that explains we don't sell data for money but that ad-cookie use may count as a "sale/share" under California law — with an opt-out.

### Section 4 — Third-Party Services
- **Added an explicit Google Ads / Customer Match disclosure** naming hashed email/phone/address sharing and the four reasons we share it (measurement, audiences, lookalikes, exclusion).
- **Removed** the contradictory line "We do not share your information with third parties for their own marketing purposes" and replaced it with: Google and other partners are contractually restricted to using the data on our behalf, and we don't allow them to use it for their own independent marketing.

### Section 5 — Cookies, Tracking, and Consent
- Split cookies into 3 categories: strictly necessary, analytics, advertising.
- Explicitly states we use a consent banner and **Google Consent Mode** before any ad/analytics tags fire in regulated regions.

### Section 8 — Your Rights and Choices
- Added CCPA/CPRA opt-out language for "sale or sharing of personal information for cross-context behavioral advertising."
- Added that we honor **Global Privacy Control (GPC)** signals.
- Added the **"Do Not Sell or Share My Personal Information"** footer-link instruction.

### Last Updated date
- Bumped to **May 4, 2026**.

---

## 2. How to publish the new policy in Shopify (5 minutes)

1. Open Shopify Admin → **Settings** → **Policies**.
2. Click **Privacy policy**.
3. Select all the existing text and **delete it**.
4. Open `Privacy-Policy-REVISED.md` (link below), copy everything, paste into the Shopify policy editor.
   - Shopify's policy editor accepts plain text with headings — the markdown `##` headings will paste cleanly. If you want exact HTML formatting, I can produce an HTML version next.
5. Click **Save**.
6. Open https://www.dresslikemommy.com/policies/privacy-policy in a private tab and confirm the new text shows.

---

## 3. Make sure the consent infrastructure is on (Shopify side)

The policy is only credible if the site actually behaves the way it describes. Verify these in Shopify Admin:

1. **Settings → Customer privacy → Cookie banner**
   - Region visibility: set to **All regions** (recommended) or at least EEA/UK/Switzerland + California.
   - Position: bottom (default is fine).
   - Click **Publish**.

2. **Settings → Customer privacy → Privacy settings**
   - Toggle **on**: "Show Do Not Sell or Share My Personal Information page" (this auto-creates the footer link CCPA requires).
   - Toggle **on**: "Honor Global Privacy Control (GPC)."
   - Data sales region: set to **United States** (or all regions if you'd rather be conservative).

3. **Settings → Customer events** (or Online Store → Themes → app embeds)
   - Confirm your Google tag (`AW-853411529`) is loaded via the Google & YouTube Shopify app or Google Tag Manager — *not* hardcoded in the theme. The Google & YouTube app respects Shopify's Customer Privacy / Consent Mode automatically.

---

## 4. Now you can confirm the Google Ads dialog

After steps 2 and 3 are saved/published, the two attestations Google is asking for are true:

- ✅ Your privacy policy **discloses** that you share customer data with Google and other third parties for advertising purposes (Section 4 of the new policy).
- ✅ You **obtain consent where required** (Shopify cookie banner + Google Consent Mode + GPC honoring + "Do Not Sell or Share" link).

**Go ahead and:**
1. Check **"Turn on conversion-based Customer lists."**
2. Confirm/continue past the policy compliance screen.

---

## 5. One last sanity check (recommended, 2 min)

Open your site in a private window from a US IP and an EU IP (use a VPN) and confirm:

- **EU view:** cookie banner appears; if you click "Reject," no `googleadservices.com` or `google.com/ccm` requests fire (check browser DevTools → Network).
- **US view:** site loads normally; footer shows a "Do Not Sell or Share My Personal Information" link.

If either of those fails, fix the consent banner config before flipping the Google Ads switch.

---

## Files

- Revised policy: `Privacy-Policy-REVISED.md`
- This activation guide: `Privacy-Policy-CHANGES-and-Activation-Steps.md`

I am not a lawyer, and this isn't legal advice — for a U.S. apparel DTC store on Shopify Basic this is a reasonable, widely-used disclosure pattern, but if you have a privacy counsel on retainer (or want one), this is the moment to have them eyeball Section 4 specifically before publishing.
