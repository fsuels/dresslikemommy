#!/usr/bin/env node
// Nightly Merchant Center feed validator.
//
// Input:  Shopify product export shape:  { "products": [ { id, handle, title,
//         tags, product_type, options:[{name,values}], images:[{src,...}],
//         variants:[{option1,option2,option3,available,featured_image,...}] } ] }
//
// Output (per bucket, in <out>/<BUCKET>/):
//   valid.jsonl   — one GMC-flat item per line, ready for downstream feed build
//   errors.csv    — id,title,bucket,issue,field,value  (one row per failure)
//   summary.json  — counts, timing, error histogram
//
// Failure mode: alert + exclude. Items with errors are written to errors.csv
// and EXCLUDED from valid.jsonl. The process exits 0 as long as it finished;
// CI inspects summary.json (or the artifact) to decide whether to alert.
// To switch to hard-fail mode, pass --strict.

import fs from 'node:fs/promises';
import path from 'node:path';
import process from 'node:process';
import { fileURLToPath } from 'node:url';
import { request } from 'undici';

import { bucketsFor } from './categories.js';
import { deriveAgeGroup } from './ageGroup.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// ---------- CLI ----------
function parseArgs(argv) {
  const args = {
    input: null,            // path to Shopify products JSON, or '-' for stdin
    out: path.join(__dirname, 'reports'),
    storeDomain: process.env.SHOPIFY_STORE_DOMAIN || 'dresslikemommy.com',
    concurrency: 12,
    timeoutMs: 10_000,
    skipUrlCheck: false,
    strict: false,
    deriveAgeGroup: true,
    ageGroupMinConfidence: 'high', // confidence floor for inclusion in supplemental CSV
    idFormat: 'shopify_pv',          // id format in supplemental CSV: shopify_pv | sku | variant_id
  };
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    const next = () => argv[++i];
    if (a === '--input') args.input = next();
    else if (a === '--out') args.out = next();
    else if (a === '--store-domain') args.storeDomain = next();
    else if (a === '--concurrency') args.concurrency = Number(next());
    else if (a === '--timeout-ms') args.timeoutMs = Number(next());
    else if (a === '--skip-url-check') args.skipUrlCheck = true;
    else if (a === '--strict') args.strict = true;
    else if (a === '--no-age-group') args.deriveAgeGroup = false;
    else if (a === '--age-group-min-confidence') args.ageGroupMinConfidence = next();
    else if (a === '--id-format') args.idFormat = next();
    else if (a === '-h' || a === '--help') {
      printHelp();
      process.exit(0);
    } else {
      console.error(`unknown arg: ${a}`);
      process.exit(2);
    }
  }
  if (!args.input) {
    console.error('error: --input <path|-> is required');
    printHelp();
    process.exit(2);
  }
  return args;
}

function printHelp() {
  console.log(`Usage: validateFeed.js --input <path|-> [options]

  --input <path|->         Shopify product export JSON, or "-" for stdin
  --out <dir>              Output directory (default: ./reports)
  --store-domain <host>    Public storefront host for landing-page URLs (default: dresslikemommy.com)
  --concurrency <n>        Parallel URL probes (default: 12)
  --timeout-ms <n>         URL probe timeout (default: 10000)
  --skip-url-check         Validate required fields only, do not probe URLs
  --strict                 Exit non-zero if any item has errors
  --no-age-group           Disable age_group derivation entirely
  --age-group-min-confidence <high|medium|low>
                           Minimum confidence for inclusion in age_group_supplemental.csv
                           (default: high)
  --id-format <shopify_pv|sku|variant_id>
                           id column format in supplemental CSV/TSV. Match whatever
                           your primary GMC feed uses. (default: shopify_pv)
`);
}

// ---------- Input loading ----------
async function loadFeed(inputArg) {
  let raw;
  if (inputArg === '-') {
    const chunks = [];
    for await (const c of process.stdin) chunks.push(c);
    raw = Buffer.concat(chunks);
  } else {
    raw = await fs.readFile(inputArg);
  }
  // Shopify exports sometimes ship UTF-16 LE with BOM — handle both.
  let text;
  if (raw[0] === 0xff && raw[1] === 0xfe) text = raw.toString('utf16le').replace(/^﻿/, '');
  else if (raw[0] === 0xfe && raw[1] === 0xff) text = Buffer.from(raw).swap16().toString('utf16le').replace(/^﻿/, '');
  else text = raw.toString('utf8').replace(/^﻿/, '');

  const parsed = JSON.parse(text);
  if (Array.isArray(parsed)) return parsed;
  if (parsed && Array.isArray(parsed.products)) return parsed.products;
  throw new Error('input must be an array of products or { products: [...] }');
}

// ---------- Flatten Shopify -> GMC items ----------
const REQUIRED_FIELDS = ['id', 'title', 'link', 'image_link', 'availability', 'price'];

function classifyOptions(options) {
  // options[] looks like [{name:"Size", position:1, values:[...]}, {name:"Color", ...}]
  // Returns { color: 'option2', size: 'option1', ... } i.e. which option key holds what.
  const map = {};
  for (const o of options || []) {
    const slot = `option${o.position}`;
    const name = String(o.name || '').toLowerCase();
    if (/colou?r|colorway|shade/.test(name)) map.color = slot;
    else if (/size|fit/.test(name)) map.size = slot;
    else if (/pattern|print/.test(name)) map.pattern = slot;
    else if (/material|fabric/.test(name)) map.material = slot;
  }
  return map;
}

function variantImage(product, variant) {
  if (variant.featured_image && variant.featured_image.src) return variant.featured_image.src;
  if (Array.isArray(product.images) && product.images.length) {
    // prefer an image whose variant_ids contains this variant
    const matched = product.images.find(
      (img) => Array.isArray(img.variant_ids) && img.variant_ids.includes(variant.id),
    );
    return (matched || product.images[0]).src || null;
  }
  return null;
}

function landingPage(storeDomain, product) {
  if (!product.handle) return null;
  return `https://${storeDomain}/products/${product.handle}`;
}

function flattenProducts(products, storeDomain) {
  const out = [];
  for (const p of products) {
    const optMap = classifyOptions(p.options);
    const buckets = bucketsFor(p);
    for (const v of p.variants || []) {
      const item = {
        id: `shopify_${p.id}_${v.id}`,
        product_id: String(p.id),
        variant_id: String(v.id),
        title: p.title,
        link: landingPage(storeDomain, p),
        image_link: variantImage(p, v),
        color: optMap.color ? v[optMap.color] : null,
        size: optMap.size ? v[optMap.size] : null,
        pattern: optMap.pattern ? v[optMap.pattern] : null,
        material: optMap.material ? v[optMap.material] : null,
        availability: v.available ? 'in stock' : 'out of stock',
        price: v.price != null ? String(v.price) : null,
        sku: v.sku || null,
        product_type: p.product_type || null,
        tags: Array.isArray(p.tags) ? p.tags : [],
        // Kept around for downstream age_group derivation; trimmed before write.
        option1: v.option1 || null,
        option2: v.option2 || null,
        option3: v.option3 || null,
        age_group: null,
        age_group_confidence: null,
        age_group_reason: null,
        buckets,
      };
      out.push(item);
    }
  }
  return out;
}

// ---------- Validation ----------
function validateRequired(item) {
  const issues = [];
  for (const f of REQUIRED_FIELDS) {
    const v = item[f];
    if (v == null || (typeof v === 'string' && v.trim() === '')) {
      issues.push({ field: f, code: 'missing_required', value: '' });
    }
  }
  if (item.image_link && !/^https?:\/\//i.test(item.image_link)) {
    issues.push({ field: 'image_link', code: 'invalid_url', value: item.image_link });
  }
  if (item.link && !/^https?:\/\//i.test(item.link)) {
    issues.push({ field: 'link', code: 'invalid_url', value: item.link });
  }
  return issues;
}

// ---------- URL probing ----------
class UrlProbe {
  constructor({ concurrency, timeoutMs }) {
    this.concurrency = concurrency;
    this.timeoutMs = timeoutMs;
    this.cache = new Map(); // url -> Promise<{ok, status}>
    this.active = 0;
    this.queue = [];
  }
  check(url) {
    if (!url) return Promise.resolve({ ok: false, status: 0, reason: 'empty' });
    if (this.cache.has(url)) return this.cache.get(url);
    const p = new Promise((resolve) => {
      const run = async () => {
        this.active++;
        try {
          resolve(await this._probe(url));
        } finally {
          this.active--;
          const next = this.queue.shift();
          if (next) next();
        }
      };
      if (this.active < this.concurrency) run();
      else this.queue.push(run);
    });
    this.cache.set(url, p);
    return p;
  }
  async _probe(url) {
    const ac = new AbortController();
    const t = setTimeout(() => ac.abort(), this.timeoutMs);
    // Always attach an error sink to the body before any await so an aborted
    // response can't emit an unhandled 'error' on its readable stream.
    const drain = async (body) => {
      if (!body) return;
      body.on('error', () => {});
      try { for await (const _ of body) { /* discard */ } } catch { /* ignore */ }
    };
    // Shopify and many CDNs block HEAD with a default fetch UA.
    const headers = {
      'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
      'accept': '*/*',
      'accept-language': 'en-US,en;q=0.9',
    };
    const opts = { signal: ac.signal, maxRedirections: 5, headers };
    try {
      let r = await request(url, { method: 'HEAD', ...opts });
      // Some origins refuse HEAD — fall back to GET.
      if ([403, 405, 429, 501, 503].includes(r.statusCode)) {
        await drain(r.body);
        r = await request(url, { method: 'GET', ...opts });
      }
      await drain(r.body);
      const ok = r.statusCode >= 200 && r.statusCode < 400;
      return { ok, status: r.statusCode };
    } catch (e) {
      return { ok: false, status: -1, reason: e.name === 'AbortError' ? 'timeout' : (e.code || e.message) };
    } finally {
      clearTimeout(t);
    }
  }
}

// ---------- Output ----------
function csvEscape(v) {
  if (v == null) return '';
  const s = String(v);
  if (/[",\n]/.test(s)) return `"${s.replace(/"/g, '""')}"`;
  return s;
}

// Fields we keep as internal scratch space and DON'T want in valid.jsonl.
const INTERNAL_FIELDS = ['option1', 'option2', 'option3', 'age_group_reason', 'buckets'];

function publicItem(item) {
  const out = { ...item };
  for (const k of INTERNAL_FIELDS) delete out[k];
  return out;
}

async function writeReports(outDir, byBucket, summary, supplemental) {
  await fs.mkdir(outDir, { recursive: true });
  for (const [bucket, group] of Object.entries(byBucket)) {
    const dir = path.join(outDir, bucket);
    await fs.mkdir(dir, { recursive: true });
    const validLines = group.valid.map((it) => JSON.stringify(publicItem(it))).join('\n');
    await fs.writeFile(path.join(dir, 'valid.jsonl'), validLines + (validLines ? '\n' : ''));

    const errHeader = 'id,product_id,variant_id,title,bucket,issue_code,field,value,link,image_link\n';
    const errRows = group.errors.map((e) =>
      [
        e.id, e.product_id, e.variant_id, e.title, bucket,
        e.code, e.field, e.value, e.link, e.image_link,
      ].map(csvEscape).join(','),
    ).join('\n');
    await fs.writeFile(path.join(dir, 'errors.csv'), errHeader + errRows + (errRows ? '\n' : ''));

    const warnHeader = 'id,product_id,variant_id,title,bucket,issue_code,field,value,reason\n';
    const warnRows = (group.warnings || []).map((w) =>
      [
        w.id, w.product_id, w.variant_id, w.title, bucket,
        w.code, w.field, w.value, w.reason,
      ].map(csvEscape).join(','),
    ).join('\n');
    await fs.writeFile(path.join(dir, 'warnings.csv'), warnHeader + warnRows + (warnRows ? '\n' : ''));
  }

  // GMC-compatible supplemental feed: tab-separated, header row "id\tage_group" only.
  // We also emit a richer CSV with confidence + source for human review.
  const tsvHeader = 'id\tage_group\n';
  const tsvRows = supplemental.map((r) => `${r.id}\t${r.age_group}`).join('\n');
  await fs.writeFile(path.join(outDir, 'age_group_supplemental.tsv'), tsvHeader + tsvRows + (tsvRows ? '\n' : ''));

  const csvHeader = 'id,age_group,confidence,source_size\n';
  const csvRows = supplemental.map((r) =>
    [r.id, r.age_group, r.confidence, r.source_size].map(csvEscape).join(','),
  ).join('\n');
  await fs.writeFile(path.join(outDir, 'age_group_supplemental.csv'), csvHeader + csvRows + (csvRows ? '\n' : ''));

  await fs.writeFile(path.join(outDir, 'summary.json'), JSON.stringify(summary, null, 2));
}

// ---------- Main ----------
async function main() {
  const args = parseArgs(process.argv);
  const startedAt = Date.now();

  const products = await loadFeed(args.input);
  const items = flattenProducts(products, args.storeDomain);

  // Derive age_group up-front so downstream reports + supplemental CSV agree.
  const confRank = { high: 3, medium: 2, low: 1, none: 0 };
  const minConf = confRank[args.ageGroupMinConfidence] ?? confRank.high;
  const ageHistogram = {};
  if (args.deriveAgeGroup) {
    for (const item of items) {
      const a = deriveAgeGroup(item);
      item.age_group = a.value;
      item.age_group_confidence = a.confidence;
      item.age_group_reason = a.reason;
      const k = `${a.value || 'unknown'}/${a.confidence}`;
      ageHistogram[k] = (ageHistogram[k] || 0) + 1;
    }
  }

  const probe = args.skipUrlCheck ? null : new UrlProbe({ concurrency: args.concurrency, timeoutMs: args.timeoutMs });

  // Per-bucket accumulators. An item with N matched buckets is added to all N.
  const byBucket = {};
  const ensure = (b) => (byBucket[b] ||= { valid: [], errors: [], warnings: [] });

  // Single global supplemental feed — MC matches by id, so per-bucket dup is
  // unnecessary and would cause "duplicate id" warnings on upload.
  const supplemental = [];
  const seenSupplemental = new Set();

  let totalErrors = 0;
  await Promise.all(
    items.map(async (item) => {
      const issues = validateRequired(item);
      if (probe && item.image_link && /^https?:/i.test(item.image_link)) {
        const r = await probe.check(item.image_link);
        if (!r.ok) issues.push({ field: 'image_link', code: `unreachable_${r.reason || r.status}`, value: item.image_link });
      }
      if (probe && item.link && /^https?:/i.test(item.link)) {
        const r = await probe.check(item.link);
        if (!r.ok) issues.push({ field: 'link', code: `unreachable_${r.reason || r.status}`, value: item.link });
      }

      // Soft warning — does NOT exclude the item, but is reported so we know
      // how much of the catalog still relies on MC's auto-detection.
      const warnings = [];
      if (args.deriveAgeGroup && (!item.age_group || confRank[item.age_group_confidence] < minConf)) {
        warnings.push({
          field: 'age_group',
          code: item.age_group ? `low_confidence_${item.age_group_confidence}` : 'missing_age_group',
          value: item.age_group || '',
          reason: item.age_group_reason || '',
        });
      }

      for (const b of item.buckets) {
        const slot = ensure(b);
        if (issues.length === 0) {
          slot.valid.push(item);
        } else {
          for (const issue of issues) {
            slot.errors.push({
              id: item.id,
              product_id: item.product_id,
              variant_id: item.variant_id,
              title: item.title,
              code: issue.code,
              field: issue.field,
              value: issue.value,
              link: item.link,
              image_link: item.image_link,
            });
            totalErrors++;
          }
        }
        for (const w of warnings) {
          slot.warnings.push({
            id: item.id,
            product_id: item.product_id,
            variant_id: item.variant_id,
            title: item.title,
            code: w.code,
            field: w.field,
            value: w.value,
            reason: w.reason,
          });
        }
      }

      // Add to supplemental feed once per unique id, only if confidence threshold met.
      if (
        args.deriveAgeGroup &&
        item.age_group &&
        confRank[item.age_group_confidence] >= minConf
      ) {
        let outId;
        if (args.idFormat === 'sku') outId = item.sku;
        else if (args.idFormat === 'variant_id') outId = item.variant_id;
        else outId = item.id;
        if (outId && !seenSupplemental.has(outId)) {
          seenSupplemental.add(outId);
          supplemental.push({
            id: outId,
            age_group: item.age_group,
            confidence: item.age_group_confidence,
            source_size: item.size || '',
          });
        }
      }
    }),
  );

  const summary = {
    started_at: new Date(startedAt).toISOString(),
    finished_at: new Date().toISOString(),
    duration_ms: Date.now() - startedAt,
    input: args.input,
    store_domain: args.storeDomain,
    skip_url_check: args.skipUrlCheck,
    derive_age_group: args.deriveAgeGroup,
    age_group_min_confidence: args.ageGroupMinConfidence,
    products: products.length,
    items: items.length,
    buckets: Object.fromEntries(
      Object.entries(byBucket).map(([k, v]) => [
        k,
        { valid: v.valid.length, errors: v.errors.length, warnings: (v.warnings || []).length },
      ]),
    ),
    age_group_histogram: ageHistogram,
    age_group_supplemental_count: supplemental.length,
    total_errors: totalErrors,
  };

  await writeReports(args.out, byBucket, summary, supplemental);

  // Always print summary to stdout so CI can parse it.
  process.stdout.write(JSON.stringify(summary, null, 2) + '\n');

  if (args.strict && totalErrors > 0) process.exitCode = 1;
}

main().catch((e) => {
  console.error(e);
  process.exitCode = 1;
});
