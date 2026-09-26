// Read-only harness for assets/dlm-family-builder.{js,css} on a LIVE PDP.
// - Every cart write (/cart/add, /cart/change, /cart/update, /cart/clear) is
//   intercepted at the network layer and answered with a stub; nothing
//   reaches the store. Ad/analytics hosts are aborted.
// - Injects the local CSS/JS, drives the flow, saves screenshots and the
//   exact request payloads to ../screenshots and ../harness-results.json.
// Usage (repo root): node <this file> [handle]
const path = require('path');
const fs = require('fs');
const { chromium } = require('/opt/homebrew/lib/node_modules/playwright');

const REPO = path.resolve(__dirname, '../../../../../..');
const LANE = path.resolve(__dirname, '..');
const OUT = path.join(LANE, 'screenshots');
const JS = fs.readFileSync(path.join(REPO, 'assets/dlm-family-builder.js'), 'utf8');
const CSS = fs.readFileSync(path.join(REPO, 'assets/dlm-family-builder.css'), 'utf8');
const BASE = 'https://www.dresslikemommy.com/products/';
const BLOCK = /(doubleclick|googleadservices|google-analytics|googletagmanager|facebook|fbcdn|pinterest|pinimg|tiktok|clarity\.ms|hotjar|bing\.com|monorail|trekkie|\/api\/collect|shopify-perf-kit|web-pixels|shop\.app)/i;
const CART_WRITE = /\/cart\/(add|change|update|clear)(\.js)?(\?|$)/;

async function openPdp(browser, handle, opts) {
  const ctx = await browser.newContext({
    viewport: { width: opts.w, height: opts.h },
    deviceScaleFactor: opts.dpr || 1,
    isMobile: !!opts.mobile,
    hasTouch: !!opts.mobile,
    reducedMotion: 'reduce',
    locale: 'en-US',
  });
  const page = await ctx.newPage();
  const cartCalls = [];
  page.__mode = 'ok';
  await page.route('**/*', async (route) => {
    const req = route.request();
    const url = req.url();
    if (BLOCK.test(url)) return route.abort();
    if (CART_WRITE.test(new URL(url).pathname)) {
      cartCalls.push({ url: new URL(url).pathname, method: req.method(), headers: req.headers(), body: req.postData() });
      if (page.__mode === 'error') {
        return route.fulfill({ status: 422, contentType: 'application/json', body: JSON.stringify({ status: 422, message: 'Cart Error', description: 'Stub: one of the selected sizes is sold out.' }) });
      }
      if (page.__mode === 'slow') await new Promise((r) => setTimeout(r, 800));
      return route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ items: [], sections: page.__sections || null }) });
    }
    return route.continue();
  });
  await page.goto(BASE + handle, { waitUntil: 'domcontentloaded', timeout: 90000 });
  await page.waitForSelector('[data-matching-set-builder]:not([hidden]) [data-select-role-group]', { timeout: 30000 }).catch(() => {});
  await page.evaluate(
    ([css, js]) => {
      const style = document.createElement('style');
      style.textContent = css;
      document.head.appendChild(style);
      const script = document.createElement('script');
      script.textContent = js;
      document.head.appendChild(script);
    },
    [CSS, JS]
  );
  await page.waitForTimeout(400);
  // Real (read-only) section HTML for the current cart, so the stubbed success
  // exercises the theme's own cart-drawer renderContents() path.
  page.__sections = await page.evaluate(() =>
    fetch('/?sections=cart-drawer,cart-icon-bubble').then((r) => r.json()).catch(() => null)
  );
  return { ctx, page, cartCalls };
}

async function state(page) {
  return page.evaluate(() => {
    const b = document.querySelector('[data-matching-set-builder]');
    const btn = b && b.querySelector('[data-matching-set-add-button]');
    const pressedRole = b && b.querySelector('[data-select-role-group][aria-pressed="true"]');
    return {
      mounted: !!document.querySelector('[data-dlm-family-builder]'),
      roles: b ? [...b.querySelectorAll('[data-select-role-group]')].map((r) => r.dataset.selectRoleGroup) : [],
      role: pressedRole ? pressedRole.dataset.selectRoleGroup : null,
      button: btn ? btn.textContent.trim() : null,
      buttonDisabled: btn ? btn.disabled : null,
      addAnotherVisible: !!document.querySelector('.dlm-family-builder__add-another:not([hidden])'),
      lines: [...document.querySelectorAll('.dlm-family-builder__line')].map((l) => l.innerText.replace(/\s*\n\s*/g, ' | ')),
      live: (document.querySelector('.dlm-family-builder__live') || {}).textContent || '',
      error: (document.querySelector('.dlm-family-builder__error:not([hidden])') || {}).textContent || '',
      overflowX: document.documentElement.scrollWidth > window.innerWidth,
      mobileSticky: (() => {
        const st = document.querySelector('[id^="StickyMobileATC-"]');
        if (!st) return null;
        const q = (sel) => { const n = st.querySelector(sel); return n ? n.textContent.trim() : null; };
        return { button: q('[data-sticky-mobile-atc-button]'), price: q('[data-sticky-mobile-atc-price]'), size: q('[data-sticky-mobile-atc-size]') };
      })(),
      desktopSticky: (() => {
        const st = document.querySelector('[data-desktop-sticky-atc]');
        if (!st) return null;
        const q = (sel) => { const n = st.querySelector(sel); return n ? n.textContent.trim() : null; };
        return { button: q('[data-desktop-sticky-button]'), price: q('[data-desktop-sticky-price]'), size: q('[data-desktop-sticky-size]') };
      })(),
    };
  });
}

async function pick(page, size) {
  await page.click(`[data-matching-set-builder] [data-instance-pill][data-size-label="${size}"]`);
  await page.waitForTimeout(120);
}

async function shootPanel(page, name) {
  const el = await page.$('[data-matching-set-builder]');
  await el.scrollIntoViewIfNeeded();
  await page.waitForTimeout(200);
  await el.screenshot({ path: path.join(OUT, name + '.png') });
}

(async () => {
  const handle = process.argv[2] || 'beanie-ghost-family-matching-pajamas';
  const browser = await chromium.launch();
  const results = { handle, runs: [] };

  for (const vp of [
    { name: 'desktop', w: 1440, h: 900 },
    { name: 'mobile375', w: 375, h: 812, dpr: 2, mobile: true },
  ]) {
    const { ctx, page, cartCalls } = await openPdp(browser, handle, vp);
    const run = { viewport: vp.name, steps: [] };
    const step = async (label) => run.steps.push({ label, ...(await state(page)) });

    await step('loaded');
    await shootPanel(page, `${vp.name}-0-loaded`);
    await pick(page, 'M');
    await step('mother M picked');
    await page.click('.dlm-family-builder__add-another');
    await page.waitForTimeout(150);
    await step('kept mother; picker moved on');
    await pick(page, 'L');
    await page.click('.dlm-family-builder__add-another');
    await page.waitForTimeout(150);
    await step('kept father');
    await pick(page, '4-5 Years');
    await page.click('[data-matching-set-builder] [data-qty-action="inc"]');
    await page.waitForTimeout(150);
    await step('child 4-5 x2 pending (counted in button)');
    await page.click('.dlm-family-builder__add-another');
    await page.waitForTimeout(150);
    await step('kept child x2');
    await shootPanel(page, `${vp.name}-1-three-people`);
    // Remove father (2nd line).
    await page.click('.dlm-family-builder__line:nth-child(2) .dlm-family-builder__remove');
    await page.waitForTimeout(150);
    await step('removed father');
    run.focusAfterRemove = await page.evaluate(() => document.activeElement && document.activeElement.getAttribute('aria-label'));
    await shootPanel(page, `${vp.name}-2-after-remove`);

    // Error path first: list must survive a 422.
    page.__mode = 'error';
    await page.click('[data-matching-set-add-button]');
    await page.waitForTimeout(500);
    await step('422 from cart (stub)');
    await shootPanel(page, `${vp.name}-3-error-kept-list`);

    // Double-submit guard: slow success, click three times fast.
    page.__mode = 'slow';
    const before = cartCalls.length;
    await page.evaluate(() => {
      const btn = document.querySelector('[data-matching-set-add-button]');
      btn.click();
      btn.click();
      btn.click();
    });
    await page.waitForTimeout(100);
    await step('busy during request');
    await page.waitForTimeout(1300);
    run.requestsFromTripleClick = cartCalls.length - before;
    await step('after stubbed success');
    run.drawerOpen = await page.evaluate(() => {
      const d = document.querySelector('cart-drawer');
      return !!(d && d.classList.contains('active'));
    });
    await page.screenshot({ path: path.join(OUT, `${vp.name}-4-drawer-after-success.png`) });
    run.cartCalls = cartCalls.map((c) => ({ url: c.url, method: c.method, contentType: c.headers['content-type'], body: c.body ? JSON.parse(c.body) : null }));
    results.runs.push(run);
    await ctx.close();
  }

  // Single-add flow must be untouched when the list is empty.
  {
    const { ctx, page, cartCalls } = await openPdp(browser, handle, { w: 1440, h: 900 });
    await pick(page, 'M');
    const s = await state(page);
    await page.click('[data-matching-set-add-button]');
    await page.waitForTimeout(600);
    results.singleAddUnchanged = {
      buttonBefore: s.button,
      calls: cartCalls.map((c) => ({ url: c.url, contentType: c.headers['content-type'], body: c.body })),
    };
    await ctx.close();
  }

  // Other product shapes: Mother/Child-only, and no "who" option at all.
  // Mobile: keep role 1, pick role 2, then tap the STICKY bar, which must
  // submit the whole list through the builder button.
  results.otherProducts = [];
  for (const other of ['bamboo-garden-panda-mommy-and-me-pajamas', 'lavender-mommy-and-me-floral-applique-sleeveless-ruffle-dress']) {
    const { ctx, page, cartCalls } = await openPdp(browser, other, { w: 375, h: 812, dpr: 2, mobile: true });
    const entry = { handle: other, loaded: await state(page) };
    if (entry.loaded.mounted) {
      const firstPill = async () => {
        const size = await page.evaluate(() => {
          const pill = document.querySelector('[data-matching-set-builder] [data-instance-pill]:not([disabled])');
          return pill ? pill.getAttribute('data-size-label') : null;
        });
        if (size) await pick(page, size);
        return size;
      };
      entry.firstSize = await firstPill();
      await page.click('.dlm-family-builder__add-another');
      await page.waitForTimeout(150);
      entry.secondSize = await firstPill();
      entry.beforeStickyTap = await state(page);
      await shootPanel(page, `other-${other.slice(0, 40)}-list`);
      await page.evaluate(() => window.scrollTo(0, 0));
      await page.waitForTimeout(300);
      const sticky = await page.$('[id^="StickyMobileATC-"] [data-sticky-mobile-atc-button]');
      entry.stickyVisible = sticky ? await sticky.isVisible() : false;
      if (sticky) {
        // DOM click (the bar may be translated off-screen when the CTA is in view).
        await sticky.evaluate((el) => el.click());
        await page.waitForTimeout(900);
      }
      entry.afterStickyTap = await state(page);
      entry.cartCalls = cartCalls.map((c) => ({ url: c.url, contentType: c.headers['content-type'], body: c.body && c.body.charAt(0) === '{' ? JSON.parse(c.body) : c.body }));
    } else {
      await page.screenshot({ path: path.join(OUT, `other-${other.slice(0, 40)}-not-mounted.png`) });
    }
    results.otherProducts.push(entry);
    await ctx.close();
  }

  fs.writeFileSync(path.join(LANE, `harness-results-${handle}.json`), JSON.stringify(results, null, 2));
  await browser.close();
  console.log(JSON.stringify(results, null, 2));
})().catch((e) => {
  console.error(e);
  process.exit(1);
});
