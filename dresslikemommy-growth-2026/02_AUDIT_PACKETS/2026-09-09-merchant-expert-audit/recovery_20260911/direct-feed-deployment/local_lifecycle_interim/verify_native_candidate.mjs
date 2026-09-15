// Offline verification only. This entry point never constructs an Admin reader.
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createHash } from 'node:crypto';
import { isDeepStrictEqual } from 'node:util';
import { buildFeed } from '../automation_release_v1/src/generator.js';

class VerificationError extends Error {}
function check(value, code) { if (!value) throw new VerificationError(code); }
const digest = (value, algorithm = 'sha256') => createHash(algorithm).update(value).digest('hex');
const read = async filename => JSON.parse(await fs.readFile(filename, 'utf8'));

export async function verifyNativeCandidate({ candidate, configPath, previousPath, holdsPath, protectedIds = [] }) {
  const [config, snapshot, diagnostics, manifest, previous, holds, holdBytes, body] = await Promise.all([
    read(configPath), read(path.join(candidate, 'us-en.snapshot.json')),
    read(path.join(candidate, 'us-en.diagnostics.json')), read(path.join(candidate, 'us-en.manifest.json')),
    read(previousPath), read(holdsPath), fs.readFile(holdsPath), fs.readFile(path.join(candidate, 'us-en.tsv')),
  ]);
  const market = config.markets.find(item => item.key === 'us-en');
  check(market?.country === 'US' && market.locale === 'en' && market.currency === 'USD' &&
    market.enabled === true && market.landingContextVerified === true, 'local_us_market_required');
  check(config.returnPolicy?.emitLabels === false, 'return_contract_changed');
  check(config.eligibilityHolds?.source?.sha256 === digest(holdBytes) &&
    isDeepStrictEqual(config.eligibilityHolds.holds, holds.holds), 'canonical_holds_binding_mismatch');
  check(Array.isArray(previous.rowIds) && new Set(previous.rowIds).size === previous.rowIds.length,
    'invalid_previous_ids');
  const replayClock = new Date(diagnostics.generatedAt);
  check(Number.isFinite(replayClock.getTime()), 'invalid_generation_clock');
  // This clock makes comparison deterministic; the publisher separately enforces
  // a genuinely new live scan and the current 120-minute promotion window.
  const result = await buildFeed(snapshot, config, market, { now: replayClock, previousIds: previous.rowIds });
  check(result.ok && result.rows.length > 0, 'candidate_replay_failed');
  check(Buffer.from(result.tsv).equals(body), 'candidate_tsv_replay_mismatch');
  check(isDeepStrictEqual(result.diagnostics, diagnostics), 'candidate_diagnostics_replay_mismatch');
  const md5 = digest(body, 'md5');
  const expectedManifest = {
    schemaVersion: 1, market: snapshot.market, objectKey: `merchant/us-en/${result.sha256}.tsv`,
    sha256: result.sha256, expectedMd5: md5, objectEtag: md5,
    bytes: result.bytes, rows: result.rows.length, rowIds: result.rowIds,
    generatedAt: result.diagnostics.generatedAt, sourceCompletedAt: snapshot.completedAt,
    sourceParents: result.diagnostics.sourceCounts.parents,
    sourceVariants: result.diagnostics.sourceCounts.variants,
    returnPolicyLabelsConfirmed: result.diagnostics.returnPolicyLabelsConfirmed, previous: null,
  };
  check(isDeepStrictEqual(expectedManifest, manifest), 'candidate_manifest_replay_mismatch');
  check(Array.isArray(protectedIds) && new Set(protectedIds).size === protectedIds.length,
    'invalid_protected_ids');
  const included = new Set(result.rowIds), protectedOmissions = [];
  for (const id of protectedIds) {
    const match = /^shopify_US_(\d+)_(\d+)$/.exec(id);
    check(match, 'invalid_protected_id');
    if (included.has(id)) continue;
    const product = snapshot.products.find(item => item.id === `gid://shopify/Product/${match[1]}`);
    const variant = product?.variants.find(item => item.id === `gid://shopify/ProductVariant/${match[2]}`);
    let reason;
    if (!product) reason = 'parent_absent_from_complete_active_catalog';
    else if (!variant) reason = 'variant_absent_from_complete_parent';
    else if (!product.onlinePublished) reason = 'not_on_online_store';
    else if (!product.countryPublished) reason = 'not_published_in_country';
    else if (market.expectedCatalogs && !product.catalogPublished) reason = 'not_in_market_catalog';
    else if (variant.availableForSale === false) reason = 'variant_not_available_for_sale';
    else if (config.eligibilityHolds.holds.some(item => item.product_id === product.id)) reason = 'reviewed_parent_eligibility_hold';
    check(reason, 'eligible_protected_offer_missing');
    protectedOmissions.push({ id, reason });
  }
  const native = diagnostics.eligibilityHolds;
  return {
    mode: 'generator_native_holds_v1', rows: result.rows.length,
    feedSha256: result.sha256, sourceCompletedAt: snapshot.completedAt,
    removedAvailableRows: native.removedAvailableRows,
    keptParents: new Set(result.rows.map(item => item.item_group_id)).size,
    configuredHeldParentIds: native.configuredParentIds,
    sourceAbsentHeldParentIds: native.sourceAbsentParentIds,
    protectedOmissions: protectedOmissions.sort((a, b) => a.id.localeCompare(b.id)),
    exactTsvManifestDiagnostics: true, sourceClockChanged: false, networkCalls: 0,
  };
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const args = process.argv.slice(2);
  const arg = name => args[args.indexOf(name) + 1];
  try {
    for (const name of ['--candidate', '--config', '--previous', '--holds', '--protected']) {
      check(args.includes(name) && arg(name), 'verification_arguments_missing');
    }
    const result = await verifyNativeCandidate({ candidate: arg('--candidate'), configPath: arg('--config'),
      previousPath: arg('--previous'), holdsPath: arg('--holds'), protectedIds: JSON.parse(arg('--protected')) });
    process.stdout.write(JSON.stringify(result) + '\n');
  } catch (error) {
    process.stderr.write(JSON.stringify({ ok: false,
      code: error instanceof VerificationError ? error.message : 'native_candidate_verification_failed' }) + '\n');
    process.exitCode = 1;
  }
}
