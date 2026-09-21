import fs from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import { fileURLToPath } from 'node:url';
import { createHash } from 'node:crypto';
import { collectCatalog, createAdminReader, SourceError } from '../../recovery_20260911/direct-feed-deployment/automation_release_v1/src/collector.js';

const packet = path.dirname(fileURLToPath(import.meta.url));
const audit = path.resolve(packet, '../..');
const release = path.join(audit, 'recovery_20260911/direct-feed-deployment/automation_release_v1');
const configPath = path.resolve(packet, '../us_spanish_qualification/isolated_config.json');
const privateDirectory = path.join(os.homedir(), '.config/dresslikemommy/merchant-evidence/20260915-us-es-full');
const sha = bytes => createHash('sha256').update(bytes).digest('hex');
const write = (file, value, mode = 0o600) => fs.writeFile(file, JSON.stringify(value, null, 2) + '\n', { flag: 'wx', mode });
const pins = {
  [path.join(release, 'src/collector.js')]: '1d0c5ef07628ed41b5b0a66f612ef454f35abe54355dfd76803f1a73259716b8',
  [path.join(release, 'src/generator.js')]: 'a028e2f7f3bb1f0c1f03e222e6b2a608b742f46b6a8f13cc97572885fe009c4f',
  [path.join(release, 'config.json')]: '668e512e5c60c7a6a5696d35b6ef47903157bcc347167f7712315c59b17b2ec8',
  [configPath]: '2c85719db86f8fb4e041c6d4ef66001dfe5e8817d2f1a2e8cf37c641ed98582e',
};

async function main() {
  for (const [file, expected] of Object.entries(pins)) {
    if (sha(await fs.readFile(file)) !== expected) throw new SourceError('source_dependency_drift');
  }
  const config = JSON.parse(await fs.readFile(configPath, 'utf8'));
  const market = config.markets.find(m => m.key === 'us-es');
  if (!market || market.enabled || market.landingContextVerified || market.country !== 'US' || market.currency !== 'USD' || market.locale !== 'es') throw new SourceError('qualification_scope_mismatch');
  const credentialFile = path.join(os.homedir(), '.config/dresslikemommy/admin-api-token.json');
  let credentials;
  try { credentials = JSON.parse(await fs.readFile(credentialFile, 'utf8')); }
  catch { throw new SourceError('private_admin_credentials_unavailable'); }
  if (credentials.store_domain !== config.storeDomain) throw new SourceError('configured_admin_domain_mismatch');
  const admin = createAdminReader({ domain: credentials.store_domain, token: credentials.access_token, apiVersion: config.apiVersion });
  const identities = [];
  let requests = 0;
  const reader = async (query, variables) => {
    if (/\bmutation\b/.test(query)) throw new SourceError('read_only_scope');
    requests++;
    const data = await admin(query, variables);
    if (data.shop && data.shopLocales && data.activeCount) identities.push({ observedAt: new Date().toISOString(), shopId: data.shop.id, shopLocales: data.shopLocales, activeCount: data.activeCount });
    return data;
  };
  await fs.mkdir(privateDirectory, { recursive: true, mode: 0o700 });
  await write(path.join(packet, 'execution_intent.json'), { atUtc: new Date().toISOString(), actionId: 'TA07-US-ES-FULL-QUALIFY-20260915', mode: 'LIVE_READ_ONLY_SOURCE_QUALIFICATION', market, pins, privateSourcePath: path.join(privateDirectory, 'source.json'), feedBuild: false, liveWrites: 0 });
  const snapshot = await collectCatalog(reader, config, market, { progress: state => {
    if (state.productsRead % 20 === 0 || state.productsRead === state.totalProducts) console.log(JSON.stringify({ event: 'read_progress', ...state }));
  } });
  const raw = JSON.stringify(snapshot, null, 2) + '\n';
  await fs.writeFile(path.join(privateDirectory, 'source.json'), raw, { flag: 'wx', mode: 0o600 });
  for (const [file, expected] of Object.entries(pins)) {
    if (sha(await fs.readFile(file)) !== expected) throw new SourceError('source_dependency_changed_during_read');
  }
  const receipt = { status: 'COMPLETE_FRESH_US_ES_SOURCE_READ', atUtc: new Date().toISOString(), market: snapshot.market, sourceStartedAt: snapshot.startedAt, sourceCompletedAt: snapshot.completedAt, parents: snapshot.products.length, variants: snapshot.products.reduce((n,p) => n + p.variants.length, 0), paginationComplete: snapshot.paginationComplete, requests, identities, marketContext: snapshot.marketContext, finalMarketContext: snapshot.finalMarketContext, translationContext: snapshot.translationContext, privateSourcePath: path.join(privateDirectory, 'source.json'), sourceSha256: sha(raw), sourceBytes: Buffer.byteLength(raw), liveWrites: 0, feedBuild: false, googleSubmission: false, pins };
  await write(path.join(packet, 'collection_receipt.json'), receipt);
  console.log(JSON.stringify({ status: receipt.status, sourceCompletedAt: receipt.sourceCompletedAt, parents: receipt.parents, variants: receipt.variants, requests, sourceSha256: receipt.sourceSha256, liveWrites: 0 }));
}
main().catch(async error => {
  const failure = { atUtc: new Date().toISOString(), status: 'FAILED_READ_ONLY_COLLECTION', code: error instanceof SourceError ? error.code : 'local_collection_failed', liveWrites: 0, feedBuild: false, googleSubmission: false };
  try { await write(path.join(packet, 'collection_failure.json'), failure); } catch {}
  console.error(JSON.stringify(failure)); process.exitCode = 1;
});
