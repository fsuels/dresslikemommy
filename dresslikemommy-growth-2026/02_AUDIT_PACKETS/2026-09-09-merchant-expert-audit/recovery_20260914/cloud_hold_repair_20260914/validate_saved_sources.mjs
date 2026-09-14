import assert from 'node:assert/strict';
import { readFile, writeFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';

const audit = new URL('../../', import.meta.url);
const base = new URL('recovery_20260911/direct-feed-deployment/', audit);
const pipe = new URL('automation_release_v1/', base);
const rec = new URL('recovery_20260914/', audit);
const { buildFeed, sha256 } = await import(new URL('src/generator.js', pipe));
const json = async url => JSON.parse(await readFile(url, 'utf8'));
const digest = async url => sha256(await readFile(url, 'utf8'));
const configured = await json(new URL('config.json', pipe));
const before = await json(new URL('before/config.json', import.meta.url));
const withoutHolds = structuredClone(configured); delete withoutHolds.eligibilityHolds;
assert.deepEqual(withoutHolds, before, 'Market settings, enablement, schedules and all existing config values must remain unchanged');
const holdNumbers = new Set(configured.eligibilityHolds.holds.map(hold => hold.product_id.split('/').at(-1)));
const cases = [
  { key: 'us-en', snapshot: new URL('local_lifecycle_interim/runs/20260914T131200Z-us-freshness/unfiltered/us-en.snapshot.json', base),
    config: new URL('config.json', pipe), existingTsv: new URL('local_lifecycle_interim/runs/20260914T131200Z-us-freshness/candidate/us-en.tsv', base) },
  { key: 'au-en', snapshot: new URL('au_source_freshness_1453/source/au-en.snapshot.json', rec),
    config: new URL('international_candidate_config.json', base), existingTsv: new URL('au_source_freshness_1453/candidate/au-en.tsv', rec) },
  ...['ca-en', 'gb-en'].map(key => ({ key, snapshot: new URL(`ca_gb_qualification_1917/${key}.snapshot.json`, rec),
    config: new URL('ca_gb_qualification_1917/qualification.config.json', rec), landingGateMustReject: true })),
  { key: 'us-es', snapshot: new URL('us_spanish_qualification/derived_global_translation_input_NOT_RELEASED.json', rec),
    config: new URL('us_spanish_qualification/isolated_config.json', rec), landingGateMustReject: true, translationFailureMode: 'exclude_product',
    limitation: 'Dated derived global-translation fixture from September 14 18:04 source, before later Spanish translation corrections; not a new collection.' },
];
const now = new Date();
const results = [];
for (const item of cases) {
  const snapshot = await json(item.snapshot), config = await json(item.config);
  config.eligibilityHolds = configured.eligibilityHolds;
  const target = config.markets.find(market => market.key === item.key);
  assert.ok(target);
  if (item.translationFailureMode) target.translationFailureMode = item.translationFailureMode;
  if (item.landingGateMustReject) {
    assert.equal(target.enabled, false);
    assert.equal(target.landingContextVerified, false);
    await assert.rejects(buildFeed(snapshot, config, target, { now }), /landing_context_unverified/);
  }
  // Test-only, in-memory branch coverage. Neither configuration nor feed bytes
  // are written, and this does not establish buyer qualification for a market.
  const branchTarget = { ...target, landingContextVerified: true };
  const result = await buildFeed(snapshot, config, branchTarget, { now });
  assert.equal(result.ok, true, `${item.key}: ${JSON.stringify(result.diagnostics.errors)}`);
  assert.deepEqual(result.diagnostics.sourceCounts, { parents: 238, variants: 4925 });
  assert.equal(result.diagnostics.eligibilityHolds.removedAvailableRows, 162);
  assert.equal(result.diagnostics.exclusions.filter(row => row.code === 'variant_not_available_for_sale').length, 22);
  assert.equal(result.diagnostics.exclusions.reduce((sum, row) => sum + row.variants, 0) + result.rows.length, 4925);
  assert.ok(result.rowIds.every(id => !holdNumbers.has(id.split('_')[2])));
  const referenceConfig = structuredClone(config); delete referenceConfig.eligibilityHolds;
  const reference = await buildFeed(snapshot, referenceConfig, branchTarget, { now });
  assert.equal(reference.ok, true, `${item.key}: reference generator path`);
  const retainedBytes = reference.tsv.split('\n').filter((line, index) => index === 0 || !holdNumbers.has(line.split('\t')[0].split('_')[2])).join('\n');
  assert.equal(result.tsv, retainedBytes, `${item.key}: retained-row byte equality`);
  if (item.existingTsv) assert.equal(result.tsv, await readFile(item.existingTsv, 'utf8'), `${item.key}: currently contained file byte equality`);
  if (item.key === 'us-es') {
    const strict = await buildFeed(snapshot, config, { ...branchTarget, translationFailureMode: 'reject_feed' }, { now });
    assert.equal(strict.ok, false);
    assert.ok(strict.diagnostics.errors.length > 0);
    assert.ok(strict.diagnostics.errors.every(error => !configured.eligibilityHolds.holds.some(hold => hold.product_id === error.productId)));
  } else assert.equal(result.rows.length, 4741);
  results.push({
    key: item.key, snapshot: fileURLToPath(item.snapshot), snapshotSha256: await digest(item.snapshot), sourceCompletedAt: snapshot.completedAt,
    configInput: fileURLToPath(item.config), configInputSha256: await digest(item.config),
    sourceCounts: result.diagnostics.sourceCounts, rows: result.rows.length, heldAvailableRows: result.diagnostics.eligibilityHolds.removedAvailableRows,
    unavailableRows: 22, translationExcludedRows: result.diagnostics.exclusions.filter(row => row.reason === 'translation_unusable').length,
    retainedRowsByteIdentical: true, currentContainedTsvByteIdentical: item.existingTsv ? true : null,
    generatedSha256: result.sha256, tsvWritten: false,
    realLandingGateRejected: item.landingGateMustReject || false,
    landingBranchOverride: item.landingGateMustReject ? 'TEST_ONLY_IN_MEMORY_NOT_A_BUYER_VERIFICATION' : null,
    limitation: item.limitation || 'Saved complete source regression only; no new source collection or live release.',
  });
}
const receipt = { action: 'TA07-CLOUD-HOLD-REPAIR-20260914', status: 'PASS_LOCAL_SAVED_SOURCE_REGRESSION', checkedAt: now.toISOString(),
  completeSourceFiles: cases.length, currentPreparedConfigUnrelatedFieldsPreserved: true, externalWrites: 0,
  tsvFilesWritten: 0, newSourceCollections: 0, results };
await writeFile(new URL('saved-source-validation.json', import.meta.url), JSON.stringify(receipt, null, 2) + '\n');
console.log(JSON.stringify(receipt));
