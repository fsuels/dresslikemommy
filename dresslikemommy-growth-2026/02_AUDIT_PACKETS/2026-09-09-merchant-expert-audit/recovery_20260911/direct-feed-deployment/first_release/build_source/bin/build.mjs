import fs from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import { createHash } from 'node:crypto';
import { collectCatalog, createAdminReader, SourceError } from '../src/collector.js';
import { buildFeed } from '../src/generator.js';

const args = process.argv.slice(2);
function argument(name, fallback = null) { const index = args.indexOf(name); return index < 0 ? fallback : args[index + 1]; }
async function main() {
  const configPath = argument('--config', new URL('../config.example.json', import.meta.url).pathname);
  const config = JSON.parse(await fs.readFile(configPath, 'utf8'));
  const key = argument('--market', 'us-en'), market = config.markets.find(m => m.key === key);
  if (!market) throw new SourceError('market_configuration_missing');
  const output = argument('--out');
  if (!output) throw new SourceError('output_directory_required');
  const snapshotPath = argument('--snapshot');
  let snapshot;
  if (snapshotPath) snapshot = JSON.parse(await fs.readFile(snapshotPath, 'utf8'));
  else {
    if (!args.includes('--live')) throw new SourceError('explicit_live_or_snapshot_input_required');
    let domain = process.env.SHOPIFY_ADMIN_SHOP_DOMAIN || process.env.SHOPIFY_STORE_DOMAIN;
    let token = process.env.SHOPIFY_ADMIN_API_TOKEN || process.env.SHOPIFY_ADMIN_ACCESS_TOKEN || process.env.SHOPIFY_ADMIN_TOKEN;
    if (!domain || !token) {
      // Existing private credential convention; never copied into output/config/logs.
      const credentialFile = argument('--credential-file', path.join(os.homedir(), '.config/dresslikemommy/admin-api-token.json'));
      let credentials;
      try { credentials = JSON.parse(await fs.readFile(credentialFile, 'utf8')); } catch { throw new SourceError('private_admin_credentials_unavailable'); }
      domain ||= credentials.store_domain; token ||= credentials.access_token;
    }
    if (domain !== config.storeDomain) throw new SourceError('configured_admin_domain_mismatch');
    const reader = createAdminReader({ domain, token, apiVersion: config.apiVersion });
    snapshot = await collectCatalog(reader, config, market, { progress: state => {
      if (state.productsRead % 20 === 0 || state.productsRead === state.totalProducts) console.log(JSON.stringify({ event: 'read_progress', ...state }));
    } });
  }
  const previousPath = argument('--previous-manifest');
  const previous = previousPath ? JSON.parse(await fs.readFile(previousPath, 'utf8')).rowIds : [];
  const result = await buildFeed(snapshot, config, market, { previousIds: previous });
  await fs.mkdir(output, { recursive: true });
  await fs.writeFile(path.join(output, `${key}.diagnostics.json`), JSON.stringify(result.diagnostics, null, 2) + '\n');
  if (!result.ok) { console.log(JSON.stringify({ ok: false, errors: result.diagnostics.errors.length, feedWritten: false })); process.exitCode = 2; return; }
  await fs.writeFile(path.join(output, `${key}.snapshot.json`), JSON.stringify(snapshot, null, 2) + '\n');
  await fs.writeFile(path.join(output, `${key}.tsv`), result.tsv);
  const manifest = {
    schemaVersion: 1, market: snapshot.market, objectKey: `merchant/${key}/${result.sha256}.tsv`,
    sha256: result.sha256, expectedMd5: createHash('md5').update(result.tsv).digest('hex'),
    objectEtag: createHash('md5').update(result.tsv).digest('hex'),
    bytes: result.bytes, rows: result.rows.length, rowIds: result.rowIds,
    generatedAt: result.diagnostics.generatedAt, sourceCompletedAt: snapshot.completedAt,
    sourceParents: result.diagnostics.sourceCounts.parents, sourceVariants: result.diagnostics.sourceCounts.variants,
    returnPolicyLabelsConfirmed: result.diagnostics.returnPolicyLabelsConfirmed,
    previous: null,
  };
  await fs.writeFile(path.join(output, `${key}.manifest.json`), JSON.stringify(manifest, null, 2) + '\n');
  console.log(JSON.stringify({ ok: true, market: key, parents: manifest.sourceParents, sourceVariants: manifest.sourceVariants, feedRows: manifest.rows, bytes: manifest.bytes, sha256: manifest.sha256, warningCount: result.diagnostics.warnings.length, exceptionRows: result.diagnostics.exceptionRows, returnPolicyLabelsConfirmed: manifest.returnPolicyLabelsConfirmed, requests: snapshot.trace.length + 2, sourceCompletedAt: snapshot.completedAt }));
}
main().catch(error => { console.error(JSON.stringify({ ok: false, code: error instanceof SourceError ? error.code : 'local_build_failed' })); process.exitCode = 1; });
