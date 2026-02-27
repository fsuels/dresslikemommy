# Multi-Language Setup Prompt for DressLikeMommy Shopify Store

Copy everything below the line and give it to your browser AI agent.

---

## TASK: Set Up Multi-Language Support for DressLikeMommy Shopify Store

You have full browser access to my Shopify admin. My store is **DressLikeMommy** and it currently only has English. I want to add **all the languages that SHEIN supports** so I can reach international customers. Shopify will auto-generate hreflang tags once languages are enabled through Markets.

### STEP 1 — Install the "Translate & Adapt" App

1. Go to **Shopify Admin → Settings → Apps and sales channels → Shopify App Store**
   (or navigate directly to: `https://apps.shopify.com/translate-and-adapt`)
2. Search for **"Translate & Adapt"** by Shopify (it's free and official)
3. Click **Install** / **Add app** and approve any permissions
4. Confirm the app appears under Apps in the admin sidebar

### STEP 2 — Enable Languages in Shopify Admin

1. Go to **Settings → Languages** (in the Shopify admin sidebar)
2. Click **"Add language"** and add the following languages one by one. These match SHEIN's supported languages:

**Priority Tier (free auto-translation available via Translate & Adapt):**
- Spanish (es)
- French (fr)

**Full Language List (add all of these):**
- Arabic (ar)
- Czech (cs)
- Danish (da)
- German (de)
- Greek (el)
- Spanish (es)
- Finnish (fi)
- French (fr)
- Hebrew (he)
- Hindi (hi)
- Hungarian (hu)
- Indonesian (id)
- Italian (it)
- Japanese (ja)
- Korean (ko)
- Malay (ms)
- Dutch (nl)
- Norwegian (no / nb)
- Polish (pl)
- Portuguese - Brazil (pt-BR)
- Portuguese - Portugal (pt-PT)
- Romanian (ro)
- Russian (ru)
- Slovak (sk)
- Swedish (sv)
- Thai (th)
- Turkish (tr)
- Vietnamese (vi)
- Chinese Simplified (zh-CN)
- Chinese Traditional (zh-TW)

3. After adding each language, click **"Publish"** to make it live
4. If Shopify asks you to assign languages to Markets, assign them to the appropriate market (or create new markets — see Step 3)

### STEP 3 — Set Up Shopify Markets

1. Go to **Settings → Markets**
2. You should see your **Primary market** (likely United States / North America)
3. Create additional markets to group languages by region. Suggested setup:

| Market Name | Countries/Regions | Languages |
|---|---|---|
| North America | US, Canada | English, Spanish, French |
| Europe | EU countries, UK | English, French, German, Spanish, Italian, Dutch, Polish, Portuguese (PT), Swedish, Danish, Finnish, Norwegian, Czech, Greek, Hungarian, Romanian, Slovak |
| Latin America | Mexico, Brazil, Argentina, etc. | Spanish, Portuguese (BR) |
| Middle East | Saudi Arabia, UAE, Israel, etc. | Arabic, Hebrew, English |
| Asia Pacific | Japan, Korea, China, India, etc. | Japanese, Korean, Chinese (Simplified), Chinese (Traditional), Hindi, Thai, Vietnamese, Malay, Indonesian |
| Russia & Turkey | Russia, Turkey | Russian, Turkish |

4. For each market, click into it and under **Languages and domains**, assign the relevant languages
5. Enable **"Active"** for each market you want to go live

### STEP 4 — Enable Auto-Translation

1. Go to **Apps → Translate & Adapt**
2. You'll see all your published languages listed
3. For **Spanish** and **French**: Click on the language, then look for **"Auto-translate"** button. Click it to auto-translate all store content (product titles, descriptions, collection names, navigation, etc.)
4. For all other languages: Shopify's free auto-translate only covers 2 languages. You have two options:
   - **Option A (Recommended):** Install a paid translation app like **Weglot**, **Langify**, or **LangShop** that supports auto-translation for all languages via Google Translate / DeepL
   - **Option B:** Use the Translate & Adapt app to manually translate key content (product titles, navigation, checkout) for each language — this is free but very time-consuming

### STEP 5 — Configure Language Selector

1. Go to **Online Store → Themes → Customize**
2. Look in the **Header** section settings for a language/country selector option
3. Enable the **language selector** so visitors can switch languages
4. Also check the **Footer** section for a language selector and enable it there too
5. Save changes

### STEP 6 — Verify Hreflang Tags

1. Go to your live store homepage in a browser
2. Right-click → **View Page Source**
3. Search for `hreflang` in the source code
4. You should see `<link rel="alternate" hreflang="es" href="...">` tags for each published language
5. Confirm there is also an `hreflang="x-default"` tag pointing to the English version
6. If hreflang tags are NOT present, go back to Settings → Markets and make sure each market has languages assigned and is set to Active

### STEP 7 — Quick QA Check

1. Visit the store homepage
2. Use the language selector to switch to Spanish — confirm product titles, navigation, and collection names are translated
3. Switch to French — confirm the same
4. Check that the URL changes (e.g., `/es/` prefix for Spanish, `/fr/` for French)
5. Verify the checkout page also shows in the selected language

### IMPORTANT NOTES

- **Do NOT touch any theme code files.** Shopify handles hreflang automatically through Markets. No Liquid template changes needed.
- **Start with Spanish and French** for auto-translate, then expand to other languages.
- If the store uses a custom domain, make sure the language subfolders work (e.g., `dresslikemommy.com/es/`)
- After setup, I can check Google Search Console in a few days to confirm Google is picking up the hreflang tags.
- The Translate & Adapt app is free. Paid alternatives like Weglot ($15+/mo) can auto-translate ALL languages at once if budget allows.

### LOGIN INFO

*(Fill in your Shopify admin URL before handing this prompt over)*

- Shopify Admin URL: `https://admin.shopify.com/store/YOUR-STORE-NAME`
- Or: `https://YOUR-STORE-NAME.myshopify.com/admin`
