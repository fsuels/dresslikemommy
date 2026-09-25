// Local preview harness: renders the real sections/hero-banner.liquid with the real
// templates/index.json settings and splices it into a script-free copy of the live page.
// Usage: node render.js <lang> <live-html> <out-html> [themeDir]
const fs = require('fs');
const path = require('path');
const { Liquid, Tag, Hash } = require('../liquidjs.cjs');

const [lang, liveHtmlPath, outPath, themeDirArg] = process.argv.slice(2);
const themeDir = themeDirArg || '/Users/fsuels/Projects/dresslikemommy';
const ASSET_ORIGIN = 'http://127.0.0.1:8791/assets/';

const stripComment = (t) => t.replace(/^\s*\/\*[\s\S]*?\*\//, '');
const indexJson = JSON.parse(stripComment(fs.readFileSync(path.join(themeDir, 'templates/index.json'), 'utf8')));
const hero = indexJson.sections.hero_banner_main;
const enLocale = JSON.parse(stripComment(fs.readFileSync(path.join(themeDir, 'locales/en.default.json'), 'utf8')));
const locFile = fs.readdirSync(path.join(themeDir, 'locales')).find((f) => f.startsWith(lang) && !f.includes('schema'));
const locLocale = locFile ? JSON.parse(stripComment(fs.readFileSync(path.join(themeDir, 'locales', locFile), 'utf8'))) : enLocale;

let src = fs.readFileSync(path.join(themeDir, 'sections/hero-banner.liquid'), 'utf8');
const schemaText = src.slice(src.indexOf('{% schema %}') + 12, src.indexOf('{% endschema %}'));
const schema = JSON.parse(schemaText);
src = src.slice(0, src.indexOf('{% schema %}'));

// Apply schema defaults like Shopify does.
const settings = {};
for (const s of schema.settings) if ('default' in s) settings[s.id] = s.default;
Object.assign(settings, hero.settings);
const blockDefaults = {};
for (const s of schema.blocks[0].settings) if ('default' in s) blockDefaults[s.id] = s.default;
const blocks = hero.block_order.map((id) => ({
  id,
  type: hero.blocks[id].type,
  settings: Object.assign({}, blockDefaults, hero.blocks[id].settings),
  shopify_attributes: '',
}));

const engine = new Liquid({ root: [path.join(themeDir, 'snippets')], extname: '.liquid', strictFilters: true });

class StyleTag extends Tag {
  constructor(token, remainTokens, liquid) {
    super(token, remainTokens, liquid);
    this.tpls = [];
    let closed = false;
    while (remainTokens.length) {
      const t = remainTokens.shift();
      if (t.name === 'endstyle') { closed = true; break; }
      this.tpls.push(liquid.parser.parseToken(t, remainTokens));
    }
    if (!closed) throw new Error('style not closed');
  }
  * render(ctx, emitter) {
    emitter.write('<style data-shopify>');
    yield this.liquid.renderer.renderTemplates(this.tpls, ctx, emitter);
    emitter.write('</style>');
  }
}
engine.registerTag('style', StyleTag);

const lookup = (obj, key) => key.split('.').reduce((o, k) => (o == null ? undefined : o[k]), obj);
engine.registerFilter('t', (key) => lookup(locLocale, key) ?? lookup(enLocale, key) ?? key);
engine.registerFilter('asset_url', (name) => ASSET_ORIGIN + name);
engine.registerFilter('image_url', () => '');
engine.registerFilter('image_tag', () => '');
engine.registerFilter('placeholder_svg_tag', () => '<svg class="placeholder-svg"></svg>');
engine.registerFilter('handleize', (s) => String(s || '').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, ''));
engine.registerFilter('color_modify', (hex, prop, val) => {
  const m = String(hex).replace('#', '');
  const [r, g, b] = [0, 2, 4].map((i) => parseInt(m.slice(i, i + 2), 16));
  return `rgba(${r}, ${g}, ${b}, ${val})`;
});

const prefix = lang === 'en' ? '' : '/' + (lang === 'pt' ? 'pt' : lang);
const isoCode = { pt: 'pt-BR' }[lang] || lang;
const ctx = {
  section: { id: 'template--17118394024033__hero_banner_main', index: 1, settings, blocks },
  request: { page_type: 'index', locale: { iso_code: isoCode } },
  localization: { language: { iso_code: isoCode } },
  shop: { name: 'Dress Like Mommy', locale: 'en', shipping_policy: { url: '/policies/shipping-policy' }, refund_policy: { url: '/policies/refund-policy' } },
  routes: { collections_url: prefix + '/collections' },
};

engine.parseAndRender(src, ctx).then((heroHtml) => {
  let page = fs.readFileSync(liveHtmlPath, 'utf8');
  const open = page.match(/<section id="shopify-section-[^"]*hero_banner_main"[^>]*>/);
  const start = open.index + open[0].length;
  const end = page.indexOf('</section>', start);
  page = page.slice(0, start) + heroHtml + page.slice(end);
  // Keep the hero's own scripts; drop every other script (analytics, pixels, apps).
  const heroStart = start, heroEnd = start + heroHtml.length;
  let out = '', last = 0;
  const re = /<script\b[\s\S]*?<\/script>/gi;
  let m;
  while ((m = re.exec(page))) {
    const inHero = m.index >= heroStart && m.index < heroEnd;
    out += page.slice(last, m.index) + (inHero ? m[0] : '');
    last = m.index + m[0].length;
  }
  out += page.slice(last);
  out = out.replace(/<link[^>]+rel="(?:preconnect|dns-prefetch|modulepreload)"[^>]*>/gi, '');
  out = out.replace('<head>', '<head><base href="https://www.dresslikemommy.com/">');
  fs.writeFileSync(outPath, out);
  fs.writeFileSync(outPath.replace('.html', '.hero.html'), heroHtml);
  console.log('rendered', lang, 'hero bytes', heroHtml.length);
}).catch((e) => { console.error('RENDER ERROR', e.message); process.exit(1); });
