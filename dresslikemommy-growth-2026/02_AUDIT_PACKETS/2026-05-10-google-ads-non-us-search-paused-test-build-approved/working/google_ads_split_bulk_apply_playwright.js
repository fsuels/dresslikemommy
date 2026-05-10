#!/usr/bin/env node
// Apply one approved paused non-US Google Ads split CSV through the logged-in CDP browser.
// The script stops unless preview downloads validate as 88/88 # OK before clicking Apply.

const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');
const { chromium } = require('playwright');

const REPO = '/Users/fsuels/Projects/dresslikemommy';
const PACKET = path.join(REPO, 'dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-google-ads-non-us-search-paused-test-build-approved');
const SPLIT_DIR = path.join(REPO, 'dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/google-ads-split-manifest/split_csvs');
const STATE_PATH = path.join(PACKET, 'working/google_ads_split_bulk_apply_state.json');
const PY_HELPER = path.join(PACKET, 'working/google_ads_split_bulk_apply.py');
const ADS_BULK_URL = 'https://ads.google.com/aw/bulk/uploads?ocid=220823493&euid=228618707&__u=2136917243&uscid=220823493&__c=9710510557&authuser=0';
const COUNTRIES = new Set(['CA', 'AU', 'CH', 'DK', 'DE', 'NL', 'SE', 'FR', 'BE', 'ES', 'IT', 'PL', 'CZ', 'RO', 'PT', 'GR']);

function mkdirp(dir) {
  fs.mkdirSync(dir, { recursive: true });
}

function loadState() {
  if (!fs.existsSync(STATE_PATH)) {
    return { completed: { GB: { note: 'GB canary applied manually before automation' } }, failures: {} };
  }
  return JSON.parse(fs.readFileSync(STATE_PATH, 'utf8'));
}

function saveState(state) {
  fs.writeFileSync(STATE_PATH, JSON.stringify(state, null, 2), 'utf8');
}

function validateResults(filePath, country, phase) {
  const code = `
import importlib.util, json, pathlib, sys
helper = pathlib.Path(${JSON.stringify(PY_HELPER)})
spec = importlib.util.spec_from_file_location('bulk_helper', helper)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
summary = mod.validate_results(pathlib.Path(sys.argv[1]), sys.argv[2], sys.argv[3])
out = pathlib.Path(sys.argv[1]).with_suffix(pathlib.Path(sys.argv[1]).suffix + '.validation.json')
out.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding='utf-8')
print(json.dumps(summary, indent=2, sort_keys=True))
`;
  execFileSync('python3', ['-c', code, filePath, country, phase], { stdio: 'inherit' });
}

async function bodyText(page) {
  return await page.locator('body').innerText({ timeout: 10000 });
}

async function clickLastText(page, pattern, label) {
  const locator = page.locator('material-button, button, [role=button], a').filter({ hasText: pattern });
  const count = await locator.count();
  if (!count) throw new Error(`Could not find ${label}`);
  await locator.nth(count - 1).click({ timeout: 15000 });
}

async function ensureUploadDrawer(page) {
  let body = await bodyText(page);
  if (!body.includes('上传电子表格') && !body.includes('Upload spreadsheet')) {
    const newUpload = page.locator('[aria-label*="新建上传操作"], [aria-label*="New upload"], [aria-label*="Create upload"]').first();
    await newUpload.click({ timeout: 15000 });
    await page.waitForFunction(
      () => document.body.innerText.includes('上传电子表格') || document.body.innerText.includes('Upload spreadsheet'),
      null,
      { timeout: 30000 },
    );
  }
}

async function ensureUploadFileSource(page) {
  let body = await bodyText(page);
  if (body.includes('从计算机选择文件') || body.includes('Choose file from computer') || body.includes('Select file from computer')) return;
  const source = page.locator('div[role=button], material-dropdown-select, dropdown-button').filter({ hasText: /选择来源|Select source|Choose source/ }).first();
  await source.click({ timeout: 15000 });
  await page.locator('material-select-dropdown-item, [role=option]').filter({ hasText: /上传文件|Upload File/ }).first().click({ timeout: 15000, force: true });
  await page.waitForFunction(
    () => document.body.innerText.includes('从计算机选择文件') || document.body.innerText.includes('Choose file from computer') || document.body.innerText.includes('Select file from computer'),
    null,
    { timeout: 15000 },
  );
}

async function selectFile(page, country, filePath) {
  const filename = path.basename(filePath);
  const activeSelected = await page.evaluate((name) => {
    const source = document.querySelector('div.source-section');
    return !!source && source.innerText.includes(name);
  }, filename);
  if (activeSelected) return;
  await ensureUploadFileSource(page);
  await page.waitForTimeout(1000);
  const chooserPromise = page.waitForEvent('filechooser', { timeout: 15000 });
  await page.locator('div.choose-file').filter({ hasText: /从计算机选择文件|Choose file from computer|Select file from computer/ }).click({ timeout: 15000 });
  const chooser = await chooserPromise;
  await chooser.setFiles(filePath);
  await page.waitForFunction(
    (name) => document.body.innerText.includes(name),
    filename,
    { timeout: 30000 },
  );
  await page.screenshot({ path: path.join(PACKET, `raw/preview/${country}_file_selected_before_preview.png`), fullPage: false });
}

async function waitPreview(page, country, filename) {
  await page.waitForFunction(
    ([name, expected]) => {
      const b = document.body.innerText;
      return b.includes(name)
        && (b.toLowerCase().includes('preview is complete') || b.includes('预览已完成'))
        && (/错误数\s*0/.test(b) || /Error count\s*0/i.test(b))
        && (new RegExp(`success\\s*${expected}`, 'i').test(b) || new RegExp(`成功\\s*${expected}`).test(b));
    },
    [filename, 88],
    { timeout: 120000 },
  );
  const body = await bodyText(page);
  fs.writeFileSync(path.join(PACKET, `raw/preview/${country}_preview_body.txt`), body, 'utf8');
  await page.screenshot({ path: path.join(PACKET, `raw/preview/${country}_preview_result.png`), fullPage: false });
}

async function waitApply(page, country, filename) {
  await page.waitForFunction(
    ([name, expected]) => {
      const b = document.body.innerText;
      const escaped = name.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      const rowSuccess = new RegExp(`${escaped}[\\s\\S]{0,400}(${expected}\\s*处更改成功|${expected}\\s*successful)`, 'i').test(b);
      return b.includes(name) && rowSuccess;
    },
    [filename, 88],
    { timeout: 150000 },
  );
  const body = await bodyText(page);
  fs.writeFileSync(path.join(PACKET, `raw/after-readbacks/${country}_apply_body.txt`), body, 'utf8');
  await page.screenshot({ path: path.join(PACKET, `raw/after-readbacks/${country}_apply_result.png`), fullPage: false });
}

async function downloadResults(page, country, phase, expectedName) {
  const dir = path.join(PACKET, phase === 'preview' ? `raw/preview/downloads/${country}` : `raw/after-readbacks/downloads/${country}`);
  fs.rmSync(dir, { recursive: true, force: true });
  mkdirp(dir);
  await page.waitForFunction(
    ([name]) => {
      const body = document.body.innerText || '';
      return body.includes(name) && (body.includes('下载结果') || body.includes('Download results'));
    },
    [expectedName.replace('_RESULTS.csv', '.csv')],
    { timeout: 30000 },
  );
  const downloadPromise = page.waitForEvent('download', { timeout: 30000 });
  const locator = page.locator('material-button, button, [role=button], a').filter({ hasText: /下载结果|Download results/ });
  const count = await locator.count();
  if (!count) throw new Error(`Could not find ${phase} download results`);
  await locator.nth(phase === 'apply' ? 0 : count - 1).click({ timeout: 15000 });
  const download = await downloadPromise;
  const suggested = download.suggestedFilename();
  if (!suggested.includes(expectedName)) throw new Error(`Unexpected ${phase} download ${suggested}; expected ${expectedName}`);
  const out = path.join(dir, suggested);
  await download.saveAs(out);
  return out;
}

async function run(country) {
  if (!COUNTRIES.has(country)) throw new Error(`Unsupported country ${country}`);
  const filePath = path.join(SPLIT_DIR, `${country}_intl_search_paused_draft_web_bulk.csv`);
  if (!fs.existsSync(filePath)) throw new Error(`Missing ${filePath}`);
  const filename = path.basename(filePath);
  const expectedResultName = `${country}_intl_search_paused_draft_web_bulk_RESULTS.csv`;
  const state = loadState();
  state.completed = state.completed || {};
  state.failures = state.failures || {};
  if (state.completed[country]) {
    console.log(`[${country}] already completed, skipping`);
    return;
  }

  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  try {
    const context = browser.contexts()[0];
    let page = context.pages().find((p) => p.url().includes('/aw/bulk/uploads'));
    if (!page) page = await context.newPage();
    await page.goto(ADS_BULK_URL, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForFunction(() => document.title.includes('Google Ads') || document.body.innerText.includes('上传操作'), null, { timeout: 30000 });
    await page.bringToFront();
    await ensureUploadDrawer(page);
    await selectFile(page, country, filePath);

    await clickLastText(page, /预览|Preview/, `${country} preview`);
    console.log(`[${country}] preview started`);
    await waitPreview(page, country, filename);
    const previewFile = await downloadResults(page, country, 'preview', expectedResultName);
    validateResults(previewFile, country, 'preview');
    console.log(`[${country}] preview validated 88/88 # OK`);

    await clickLastText(page, /应用|Apply/, `${country} apply`);
    console.log(`[${country}] apply started`);
    await waitApply(page, country, filename);
    const applyFile = await downloadResults(page, country, 'apply', expectedResultName);
    validateResults(applyFile, country, 'apply');
    console.log(`[${country}] apply validated 88/88 # OK`);

    state.completed[country] = {
      preview: path.relative(REPO, previewFile),
      apply: path.relative(REPO, applyFile),
      time: new Date().toISOString(),
    };
    delete state.failures[country];
    saveState(state);
  } catch (error) {
    state.failures[country] = { error: String(error && error.stack ? error.stack : error), time: new Date().toISOString() };
    saveState(state);
    throw error;
  }
}

const country = process.argv[2];
if (!country) {
  console.error('Usage: google_ads_split_bulk_apply_playwright.js <COUNTRY>');
  process.exit(2);
}
run(country).then(() => {
  process.exit(0);
}).catch((error) => {
  console.error(`[STOP] ${country}:`, error);
  process.exit(1);
});
