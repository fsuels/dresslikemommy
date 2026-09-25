const { chromium } = require('/opt/homebrew/lib/node_modules/playwright');
const OUT = process.argv[2];
(async () => {
  const browser = await chromium.launch();
  const shots = [
    { name: 'after-desktop-halloween', url: 'en.html', w: 1440, h: 900, dpr: 1, slide: 1, clipH: 800 },
    { name: 'after-desktop-winter', url: 'en.html', w: 1440, h: 900, dpr: 1, slide: 2, clipH: 800 },
    { name: 'after-mobile-halloween', url: 'en.html', w: 390, h: 844, dpr: 2, slide: 1, clipH: 700, mobile: true },
    { name: 'after-mobile-winter', url: 'en.html', w: 390, h: 844, dpr: 2, slide: 2, clipH: 700, mobile: true },
    { name: 'before-desktop', url: 'before-en.html', w: 1440, h: 900, dpr: 1, slide: 1, clipH: 800 },
    { name: 'before-mobile', url: 'before-en.html', w: 390, h: 844, dpr: 2, slide: 1, clipH: 700, mobile: true },
    { name: 'after-mobile-de', url: 'de.html', w: 390, h: 844, dpr: 2, slide: 1, clipH: 700, mobile: true },
    { name: 'after-desktop-ja', url: 'ja.html', w: 1440, h: 900, dpr: 1, slide: 1, clipH: 800 },
  ];
  for (const s of shots) {
    const ctx = await browser.newContext({ viewport: { width: s.w, height: s.h }, deviceScaleFactor: s.dpr, isMobile: !!s.mobile, hasTouch: !!s.mobile, reducedMotion: 'reduce' });
    const page = await ctx.newPage();
    await page.goto('http://127.0.0.1:8791/' + s.url, { waitUntil: 'load', timeout: 60000 });
    await page.waitForTimeout(800);
    if (s.slide === 2) {
      await page.click('[data-hero-dot="1"]');
      await page.waitForTimeout(900);
    }
    await page.evaluate(() => window.scrollTo(0, 0));
    await page.waitForTimeout(300);
    await page.screenshot({ path: `${OUT}/${s.name}.png`, clip: { x: 0, y: 0, width: s.w, height: s.clipH } });
    await ctx.close();
    console.log('shot', s.name);
  }
  await browser.close();
})().catch((e) => { console.error(e); process.exit(1); });
