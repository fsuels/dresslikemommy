// Read-only visual check: loads live PDPs, injects assets/dlm-holiday-order-by.js,
// screenshots the purchase-confidence card. Blocks ad/analytics pixels. No cart actions.
// Usage: node shoot_holiday_order_by.js <repoRoot> <outDir>
const { chromium } = require('/opt/homebrew/lib/node_modules/playwright');
const path = require('path');
const [repo, OUT] = process.argv.slice(2);
const SCRIPT = path.join(repo, 'assets/dlm-holiday-order-by.js');
const BASE = 'https://www.dresslikemommy.com';
const BLOCK = /google-analytics|googletagmanager|doubleclick|facebook|connect\.facebook|pinimg\.com\/ct|ct\.pinterest|tiktok|clarity\.ms|hotjar|bing\.com|monorail|\/api\/collect|trekkie|shopify-perf-kit/;
// fakeNow lets the Christmas line be previewed inside its lead window.
const shots = [
  { name: 'desktop-en-beanie-ghost', url: '/products/beanie-ghost-family-matching-pajamas', w: 1440, h: 900 },
  { name: 'mobile-en-beanie-ghost', url: '/products/beanie-ghost-family-matching-pajamas', w: 375, h: 812, mobile: true },
  { name: 'mobile-es-beanie-ghost', url: '/es/products/beanie-ghost-family-matching-pajamas', w: 375, h: 812, mobile: true },
  { name: 'desktop-de-beanie-ghost', url: '/de/products/beanie-ghost-family-matching-pajamas', w: 1440, h: 900 },
  { name: 'desktop-en-christmas-today', url: '/products/nordic-reindeer-family-matching-sweaters', w: 1440, h: 900 },
  { name: 'desktop-en-christmas-2026-10-20', url: '/products/nordic-reindeer-family-matching-sweaters', w: 1440, h: 900, fakeNow: '2026-10-20T12:00:00' },
  { name: 'desktop-en-halloween-2026-10-16', url: '/products/beanie-ghost-family-matching-pajamas', w: 1440, h: 900, fakeNow: '2026-10-16T09:00:00' },
];
(async () => {
  const browser = await chromium.launch();
  const results = [];
  for (const s of shots) {
    const ctx = await browser.newContext({ viewport: { width: s.w, height: s.h }, deviceScaleFactor: s.mobile ? 2 : 1, isMobile: !!s.mobile, hasTouch: !!s.mobile });
    if (s.fakeNow) {
      await ctx.addInitScript((iso) => {
        const fixed = new Date(iso).getTime();
        const RealDate = Date;
        function FakeDate(...a) { return a.length ? new RealDate(...a) : new RealDate(fixed); }
        FakeDate.prototype = RealDate.prototype;
        FakeDate.now = () => fixed;
        FakeDate.UTC = RealDate.UTC;
        FakeDate.parse = RealDate.parse;
        window.Date = FakeDate;
      }, s.fakeNow);
    }
    await ctx.route('**/*', (route) => (BLOCK.test(route.request().url()) ? route.abort() : route.continue()));
    const page = await ctx.newPage();
    await page.goto(BASE + s.url, { waitUntil: 'domcontentloaded', timeout: 90000 });
    await page.waitForSelector('[data-pdp-purchase-confidence] [data-dlm-delivery-window]', { timeout: 60000 });
    await page.waitForTimeout(1500);
    await page.addScriptTag({ path: SCRIPT });
    await page.waitForTimeout(2500);
    const info = await page.evaluate(() => {
      const card = document.querySelector('[data-pdp-purchase-confidence]');
      const line = document.querySelector('[data-dlm-holiday-order-by]');
      const est = card && card.querySelector('.dlm-pc-row__estimate');
      return {
        locale: (window.Shopify && window.Shopify.locale) || document.documentElement.lang,
        estimate: est ? est.textContent.replace(/\s+/g, ' ').trim() : null,
        line: line ? line.textContent : null,
        lines: document.querySelectorAll('[data-dlm-holiday-order-by]').length,
        scrollWidth: document.documentElement.scrollWidth,
        clientWidth: document.documentElement.clientWidth,
      };
    });
    const row = page.locator('[data-pdp-purchase-confidence] .dlm-pc-row').first();
    await row.scrollIntoViewIfNeeded();
    await page.waitForTimeout(400);
    await page.locator('[data-pdp-purchase-confidence]').screenshot({ path: `${OUT}/${s.name}.png` });
    results.push({ ...s, ...info });
    console.log(JSON.stringify({ name: s.name, ...info }));
    await ctx.close();
  }
  await browser.close();
  require('fs').writeFileSync(`${OUT}/results.json`, JSON.stringify(results, null, 2));
})().catch((e) => { console.error(e); process.exit(1); });
