// Live readback of the UX ten-fix release on the published theme (no cart writes, pixels blocked).
const { chromium } = require('/opt/homebrew/lib/node_modules/playwright');
const OUT = __dirname;
const BLOCK = /google|facebook|pinterest|tiktok|bing|clarity|hotjar|doubleclick|analytics|pixel|monorail|trekkie|klaviyo|snapchat/i;
(async () => {
  const browser = await chromium.launch();
  const results = {};
  const pages = [
    ['pdp-en-desktop', '/products/beanie-ghost-family-matching-pajamas', { width: 1440, height: 1000 }],
    ['pdp-en-mobile', '/products/beanie-ghost-family-matching-pajamas', { width: 375, height: 812, isMobile: true }],
    ['pdp-es-mobile', '/es/products/beanie-ghost-family-matching-pajamas', { width: 375, height: 812, isMobile: true }],
    ['pdp-mommy-me-desktop', '/products/bamboo-garden-panda-mommy-and-me-pajamas', { width: 1440, height: 1000 }],
    ['cart-empty-mobile', '/cart', { width: 375, height: 812, isMobile: true }],
    ['halloween-collection', '/collections/halloween-family-pajamas', { width: 1440, height: 1000 }],
  ];
  for (const [name, path, vp] of pages) {
    const ctx = await browser.newContext({ viewport: { width: vp.width, height: vp.height }, isMobile: !!vp.isMobile });
    await ctx.route('**/*', (r) => (BLOCK.test(r.request().url()) ? r.abort() : r.continue()));
    const page = await ctx.newPage();
    const errors = [];
    page.on('pageerror', (e) => errors.push(String(e)));
    await page.goto('https://www.dresslikemommy.com' + path + '?lv=' + Date.now(), { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(4000);
    const r = await page.evaluate(() => ({
      theme: window.Shopify && Shopify.theme && Shopify.theme.id,
      liquidError: document.documentElement.innerHTML.includes('Liquid error'),
      orderBy: (document.querySelector('[data-dlm-holiday-order-by]') || {}).textContent || null,
      familyBuilderNodes: document.querySelectorAll('[class*="dlm-family"]').length,
      stale19: document.body.innerText.includes('latest 19'),
      cartHeading: (document.querySelector('.cart-page__empty-section-title') || {}).textContent || null,
      cartPicks: [...document.querySelectorAll('.cart-page__cross-sell-item')].slice(0, 4).map((a) => a.getAttribute('href')),
      collectionH1: (document.querySelector('h1') || {}).textContent || null,
      hScroll: document.documentElement.scrollWidth > document.documentElement.clientWidth,
    }));
    r.pageErrors = errors;
    results[name] = r;
    await page.screenshot({ path: `${OUT}/${name}.png`, fullPage: false });
    if (name.startsWith('pdp-en-mobile')) {
      const el = await page.$('[data-pdp-purchase-confidence]');
      if (el) { await el.scrollIntoViewIfNeeded(); await page.screenshot({ path: `${OUT}/${name}-confidence.png` }); }
      const fb = await page.$('[class*="dlm-family"]');
      if (fb) { await fb.scrollIntoViewIfNeeded(); await page.screenshot({ path: `${OUT}/${name}-builder.png` }); }
    }
    await ctx.close();
  }
  require('fs').writeFileSync(`${OUT}/results.json`, JSON.stringify(results, null, 2));
  console.log(JSON.stringify(results, null, 1));
  await browser.close();
})();
