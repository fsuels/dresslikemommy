const { chromium } = require('/opt/homebrew/lib/node_modules/playwright');
(async () => {
  const b = await chromium.launch();
  const p = await (await b.newContext({ viewport: { width: 1440, height: 900 } })).newPage();
  const errors = [];
  p.on('pageerror', (e) => errors.push(e.message));
  p.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
  await p.goto('http://127.0.0.1:8791/en.html', { waitUntil: 'load' });
  await p.waitForTimeout(500);
  // Tab from the top of the hero: first stop should be the active slide link.
  await p.focus('.hero-banner__slide.is-active .hero-banner__slide-link');
  const s0 = await p.evaluate(() => document.activeElement.getAttribute('href'));
  await p.keyboard.press('ArrowRight');
  await p.waitForTimeout(1500);
  const s1 = await p.evaluate(() => ({ href: document.activeElement.getAttribute('href'), cls: document.activeElement.className, active: document.querySelector('.hero-banner__slide.is-active').id.slice(-1), hidden: [...document.querySelectorAll('.hero-banner__slide')].map((s) => s.getAttribute('aria-hidden')) }));
  await p.keyboard.press('ArrowLeft');
  await p.waitForTimeout(1500);
  const s2 = await p.evaluate(() => ({ href: document.activeElement.getAttribute('href'), active: document.querySelector('.hero-banner__slide.is-active').id.slice(-1) }));
  // Tab order after the slide link.
  const order = [];
  for (let i = 0; i < 7; i++) { await p.keyboard.press('Tab'); order.push(await p.evaluate(() => (document.activeElement.getAttribute('aria-label') || document.activeElement.textContent).trim().slice(0, 34))); }
  // Broken-art resilience: point slide 2 art at a missing file, then advance.
  await p.goto('http://127.0.0.1:8791/en.html', { waitUntil: 'load' });
  await p.evaluate(() => { const t = document.querySelector('template[data-hero-slide-picture]'); const img = t.content.querySelector('.hero-banner__art'); img.setAttribute('srcset', '/assets/missing-art-760.webp 760w'); img.setAttribute('src', '/assets/missing-art-760.webp'); });
  await p.click('[data-hero-next]');
  await p.waitForTimeout(1500);
  const s3 = await p.evaluate(() => { const act = document.querySelector('.hero-banner__slide.is-active'); const art = act.querySelector('.hero-banner__art'); return { active: act.id.slice(-1), artHidden: art ? art.hidden : null }; });
  console.log(JSON.stringify({ start: s0, afterRight: s1, afterLeft: s2, tabOrder: order, brokenArt: s3, errors }, null, 1));
  await b.close();
})();
