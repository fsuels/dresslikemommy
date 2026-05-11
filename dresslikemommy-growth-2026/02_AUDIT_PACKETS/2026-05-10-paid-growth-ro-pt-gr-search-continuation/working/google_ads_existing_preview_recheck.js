#!/usr/bin/env node
// Recheck an existing Google Ads bulk-upload preview without uploading the file again.
// Scoped to the approved paused non-US Search TEST BUILD continuation.

const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');
const { chromium } = require('playwright');

const REPO = '/Users/fsuels/Projects/dresslikemommy';
const PACKET = path.join(REPO, 'dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-ro-pt-gr-search-continuation');
const OLD_PACKET = path.join(REPO, 'dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-google-ads-non-us-search-paused-test-build-approved');
const PY_HELPER = path.join(OLD_PACKET, 'working/google_ads_split_bulk_apply.py');
const ADS_BULK_URL = 'https://ads.google.com/aw/bulk/uploads?ocid=220823493&euid=228618707&__u=2136917243&uscid=220823493&__c=9710510557&authuser=0';

function mkdirp(dir) {
  fs.mkdirSync(dir, { recursive: true });
}

async function bodyText(page) {
  return await page.locator('body').innerText({ timeout: 10000 });
}

function classify(body, filename) {
  const lower = body.toLowerCase();
  const hasFile = body.includes(filename);
  const errorZero = /Error count\s*0/i.test(body) || /错误数\s*0/.test(body);
  const success88 = /success\s*88/i.test(body) || /成功\s*88/.test(body);
  const complete = hasFile && errorZero && success88 && (lower.includes('preview is complete') || body.includes('预览已完成'));
  const inProgress = hasFile && errorZero && (lower.includes('preview is in progress') || body.includes('预览正在进行'));
  const failed = hasFile && (/Error count\s*[1-9]/i.test(body) || /错误数\s*[1-9]/.test(body));
  if (complete) return 'PREVIEW_COMPLETE_88_OK';
  if (inProgress) return 'PREVIEW_IN_PROGRESS_ERROR_0';
  if (failed) return 'PREVIEW_HAS_ERRORS';
  if (hasFile) return 'PREVIEW_FILE_VISIBLE_UNCLASSIFIED';
  return 'PREVIEW_FILE_NOT_VISIBLE';
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

async function clickLastText(page, pattern, label) {
  const locator = page.locator('material-button, button, [role=button], a').filter({ hasText: pattern, visible: true });
  const count = await locator.count();
  if (!count) throw new Error(`Could not find ${label}`);
  await locator.nth(count - 1).click({ timeout: 15000 });
}

async function downloadResults(page, country, phase, expectedName) {
  const dir = path.join(PACKET, 'raw', country.toLowerCase(), phase === 'preview' ? 'preview-downloads' : 'apply-downloads');
  fs.rmSync(dir, { recursive: true, force: true });
  mkdirp(dir);
  const sourceName = expectedName.replace('_RESULTS.csv', '.csv');
  await page.waitForFunction(
    ([name]) => {
      const body = document.body.innerText || '';
      return body.includes(name) && (body.includes('下载结果') || body.includes('Download results'));
    },
    [sourceName],
    { timeout: 30000 },
  );
  const downloadPromise = page.waitForEvent('download', { timeout: 30000 });
  const rowLocator = page
    .locator('.particle-table-row, [role=row], tr')
    .filter({ hasText: sourceName, visible: true })
    .locator('material-button, button, [role=button], a')
    .filter({ hasText: /下载结果|Download results/, visible: true });
  const rowCount = await rowLocator.count();
  if (rowCount) {
    await rowLocator.last().click({ timeout: 15000 });
  } else {
    const locator = page.locator('material-button, button, [role=button], a').filter({ hasText: /下载结果|Download results/, visible: true });
    const count = await locator.count();
    if (!count) throw new Error(`Could not find ${phase} download results`);
    await locator.last().click({ timeout: 15000 });
  }
  const download = await downloadPromise;
  const suggested = download.suggestedFilename();
  if (!suggested.includes(expectedName)) throw new Error(`Unexpected ${phase} download ${suggested}; expected ${expectedName}`);
  const out = path.join(dir, suggested);
  await download.saveAs(out);
  return out;
}

async function waitApply(page, country, filename) {
  await page.waitForFunction(
    ([name, expected]) => {
      const b = document.body.innerText || '';
      const escaped = name.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      const rowSuccess = new RegExp(`${escaped}[\\s\\S]{0,500}(${expected}\\s*处更改成功|${expected}\\s*successful)`, 'i').test(b);
      return b.includes(name) && rowSuccess;
    },
    [filename, 88],
    { timeout: 180000 },
  );
  const body = await bodyText(page);
  const outDir = path.join(PACKET, 'raw', country.toLowerCase());
  fs.writeFileSync(path.join(outDir, 'apply_body.txt'), body, 'utf8');
  await page.screenshot({ path: path.join(outDir, 'apply_result.png'), fullPage: false });
}

async function main() {
  const country = process.argv[2];
  const shouldApply = process.argv.includes('--apply');
  const shouldReload = process.argv.includes('--reload');
  const waitArg = process.argv.find((arg) => arg.startsWith('--wait-ms='));
  const waitMs = waitArg ? Number(waitArg.split('=')[1]) : 0;
  if (!country) throw new Error('Usage: google_ads_existing_preview_recheck.js <COUNTRY> [--apply]');
  const filename = `${country}_intl_search_paused_draft_web_bulk.csv`;
  const expectedResultName = `${country}_intl_search_paused_draft_web_bulk_RESULTS.csv`;
  const outDir = path.join(PACKET, 'raw', country.toLowerCase());
  mkdirp(outDir);

  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  try {
    const context = browser.contexts()[0];
    let page = context.pages().find((p) => p.url().includes('/aw/bulk/uploads'));
    if (!page) page = await context.newPage();
    if (!page.url().includes('/aw/bulk/uploads')) {
      await page.goto(ADS_BULK_URL, { waitUntil: 'domcontentloaded', timeout: 60000 });
    }
    await page.waitForFunction(() => document.title.includes('Google Ads') || document.body.innerText.includes('Upload operation') || document.body.innerText.includes('上传操作'), null, { timeout: 30000 });
    await page.bringToFront();
    if (shouldReload) {
      await page.reload({ waitUntil: 'domcontentloaded', timeout: 60000 });
      await page.waitForFunction(() => document.title.includes('Google Ads') || document.body.innerText.includes('Upload operation') || document.body.innerText.includes('上传操作'), null, { timeout: 30000 });
      await page.waitForTimeout(3000);
    }
    const deadline = Date.now() + waitMs;
    let body = await bodyText(page);
    let status = classify(body, filename);
    while (waitMs > 0 && Date.now() < deadline && status === 'PREVIEW_IN_PROGRESS_ERROR_0') {
      await page.waitForTimeout(10000);
      body = await bodyText(page);
      status = classify(body, filename);
    }
    fs.writeFileSync(path.join(outDir, 'existing_preview_recheck_body.txt'), body, 'utf8');
    await page.screenshot({ path: path.join(outDir, 'existing_preview_recheck.png'), fullPage: false });

    const statusPath = path.join(outDir, 'existing_preview_recheck_status.json');
    fs.writeFileSync(statusPath, JSON.stringify({ country, filename, status, checkedAt: new Date().toISOString(), applyRequested: shouldApply, reload: shouldReload, waitMs }, null, 2), 'utf8');
    console.log(JSON.stringify({ country, status, statusPath: path.relative(REPO, statusPath) }, null, 2));

    if (status !== 'PREVIEW_COMPLETE_88_OK') {
      process.exit(status === 'PREVIEW_IN_PROGRESS_ERROR_0' ? 3 : 4);
    }

    const previewFile = await downloadResults(page, country, 'preview', expectedResultName);
    validateResults(previewFile, country, 'preview');
    console.log(`[${country}] existing preview downloaded and validated 88/88 # OK`);

    if (!shouldApply) return;

    await clickLastText(page, /应用|Apply/, `${country} apply`);
    console.log(`[${country}] apply started from existing preview`);
    await waitApply(page, country, filename);
    const applyFile = await downloadResults(page, country, 'apply', expectedResultName);
    validateResults(applyFile, country, 'apply');
    console.log(`[${country}] apply downloaded and validated 88/88 # OK`);
  } finally {
    await browser.close();
  }
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
