import assert from 'node:assert/strict';
import { readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { createHash } from 'node:crypto';

const repo = '/Users/fsuels/Projects/dresslikemommy';
const audit = path.join(repo, 'dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-09-merchant-expert-audit/');
const pipe = path.join(repo, 'dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-09-merchant-expert-audit/recovery_20260911/direct-feed-deployment/automation_release_v1/');
const output = path.dirname(fileURLToPath(import.meta.url));
const readJSON = async f => JSON.parse(await readFile(f, 'utf8'));
const hash = async f => createHash('sha256').update(await readFile(f)).digest('hex');
const { buildFeed } = await import(pathToFileURL(path.join(pipe, 'src/generator.js')));
const { refreshMarket, currentManifest } = await import(pathToFileURL(path.join(pipe, 'src/worker.js')));
const { enqueueRefresh, consumeRefresh } = await import(pathToFileURL(path.join(pipe, 'src/checkpoint.js')));
const { config: fixtureConfig, market, now, product, variant, source, Bucket } = await import(pathToFileURL(path.join(pipe, 'test/fixtures.js')));
const { streamOptions } = await import(pathToFileURL(path.join(pipe, 'test/node-streams.js')));
const configured = await readJSON(path.join(pipe, 'config.json'));
const receipt = await readJSON(path.join(audit, 'recovery_20260914/cloud_hold_repair_20260914/implementation_receipt.json'));
const before = await readJSON(path.join(audit, 'recovery_20260914/cloud_hold_repair_20260914/before/config.json'));
const protectedHashes = {};
for (const [file, expected] of Object.entries({...receipt.changedFiles, ...receipt.preservedFiles})) {
  const actual = await hash(path.join(repo, file));
  assert.equal(actual, expected, file);
  protectedHashes[file] = actual;
}
const withoutHolds = structuredClone(configured); delete withoutHolds.eligibilityHolds;
assert.deepEqual(withoutHolds, before);
const canonicalFile = path.join(repo, receipt.canonicalHoldSource.path);
const canonical = await readJSON(canonicalFile);
assert.equal(await hash(canonicalFile), receipt.canonicalHoldSource.sha256);
assert.deepEqual(configured.eligibilityHolds.holds, canonical.holds);
const ids = new Set(canonical.holds.map(h => h.product_id));
assert.equal(ids.size, 6);

const savedReceipt = await readJSON(path.join(audit, 'recovery_20260914/cloud_hold_repair_20260914/saved-source-validation.json'));
const savedResults = [];
for (const item of savedReceipt.results) {
  assert.equal(await hash(item.snapshot), item.snapshotSha256);
  const snapshot = await readJSON(item.snapshot);
  const config = await readJSON(item.configInput);
  assert.equal(await hash(item.configInput), item.configInputSha256);
  config.eligibilityHolds = configured.eligibilityHolds;
  const target = config.markets.find(m => m.key === item.key);
  const testTime = new Date(Date.parse(snapshot.completedAt) + 60000);
  if (item.key === 'us-es') target.translationFailureMode = 'exclude_product';
  if (item.realLandingGateRejected) {
    assert.equal(target.landingContextVerified, false);
    await assert.rejects(buildFeed(snapshot, config, target, {now: testTime}), /landing_context_unverified/);
  }
  const branchTarget = {...target, landingContextVerified:true};
  const expectedIds = [], priceById = new Map();
  let unavailable = 0, held = 0, translation = 0, publication = 0;
  for (const p of snapshot.products) {
    if (!p.onlinePublished || !p.countryPublished || (target.expectedCatalogs && !p.catalogPublished)) { publication += p.variants.length; continue; }
    const translations = (p.translations || []).filter(t => t.locale === target.locale);
    const title = translations.find(t => t.key === 'title');
    const body = translations.find(t => t.key === 'body_html');
    const handle = translations.find(t => t.key === 'handle');
    const translationBad = target.locale !== config.sourceLocale &&
      (!title?.value || title.outdated || !body?.value || body.outdated || handle?.outdated);
    for (const v of p.variants) {
      if (!v.availableForSale) { unavailable++; continue; }
      if (ids.has(p.id)) { held++; continue; }
      if (translationBad) { translation++; continue; }
      const id = ['shopify',target.country,p.id.split('/').at(-1),v.id.split('/').at(-1)].join('_');
      expectedIds.push(id);
      priceById.set(id, Number(v.contextualPricing.price.amount).toFixed(target.minorUnits ?? 2)+' '+v.contextualPricing.price.currencyCode);
    }
  }
  const result = await buildFeed(snapshot, config, branchTarget, {now:testTime});
  assert.equal(result.ok, true, item.key);
  assert.deepEqual(result.rowIds.sort(), expectedIds.sort(), item.key + ' independently derived eligibility');
  assert.equal(held, 162); assert.equal(unavailable, 22);
  assert.equal(result.diagnostics.eligibilityHolds.removedAvailableRows, held);
  assert.equal(expectedIds.length + unavailable + held + translation + publication, 4925);
  assert.ok(result.rows.every(row => row.availability === 'in_stock' && row.price === priceById.get(row.id)));
  assert.equal(result.sha256, item.generatedSha256);
  savedResults.push({market:item.key, sourceSha256:item.snapshotSha256, sourceCompletedAt:snapshot.completedAt,
    evaluatedAt:testTime.toISOString(), rows:expectedIds.length, held, unavailable, translation, publication,
    independentlyDerivedMembershipAndPrices:true, generatedSha256:result.sha256,
    landingOverrideOnlyInMemory:Boolean(item.realLandingGateRejected), noNewSourceOrFeedWrite:true});
}

const graph = [], visited = new Set();
async function visit(file) {
  if (visited.has(file)) return;
  visited.add(file);
  const content = await readFile(file, 'utf8');
  const edges = [...content.matchAll(/(?:import|export)\s+(?:[^;]*?\s+from\s*)?['"]([^'"]+)['"]/g)].map(m=>m[1]);
  assert.ok(edges.every(p=>p.startsWith('.')), 'No unexpected external package import in runtime graph');
  graph.push({file:path.relative(pipe,file), sha256:await hash(file), imports:edges});
  for (const specifier of edges) await visit(path.resolve(path.dirname(file),specifier));
}
await visit(path.join(pipe,'src/automation.js'));
assert.ok(graph.some(m=>m.file === 'src/eligibility.js'));
await import(pathToFileURL(path.join(pipe,'src/automation.js')));

const adversarial = [];
const heldParent = product(Number(canonical.holds[0].product_id.split('/').at(-1)), [variant(90001)]);
heldParent.featuredMedia = null; heldParent.variants[0].media = null;
const queue = {messages:[], async send(message) {this.messages.push(structuredClone(message));}};
const cfg = {...structuredClone(fixtureConfig), eligibilityHolds:configured.eligibilityHolds, refresh:{maxSourceCallsPerInvocation:2}};
const env = {MERCHANT_CONFIG_JSON:JSON.stringify(cfg),MERCHANT_FEED_BUCKET:new Bucket(),MERCHANT_REFRESH_QUEUE:queue};
await refreshMarket(env,market.key,{graphql:source([product()]).graphql,now:()=>now});
const prior = (await currentManifest(env.MERCHANT_FEED_BUCKET,market.key)).manifest;
const bad = product(2); bad.variants[0].contextualPricing.price.amount = '0';
const badSource = source([heldParent,product(),bad]);
await enqueueRefresh(env,market.key,{now:()=>now});
let stepCount=0,last;
while(queue.messages.length) {
  last = await consumeRefresh(env,queue.messages.shift(),{graphql:badSource.graphql,now:()=>now,streamOptions});
  assert.ok(++stepCount<30);
}
assert.equal(last.failed,true); assert.equal(last.code,'feed_validation_failed');
assert.deepEqual((await currentManifest(env.MERCHANT_FEED_BUCKET,market.key)).manifest,prior);
adversarial.push({case:'Held image failure plus unrelated new zero-price variant across queue checkpoints',result:'PASS',steps:stepCount,code:last.code,priorPointerPreserved:true});

const oldEnv = {...env,MERCHANT_CONFIG_JSON:JSON.stringify(fixtureConfig),MERCHANT_REFRESH_QUEUE:{messages:[],async send(m){this.messages.push(m);}}};
await enqueueRefresh(oldEnv,market.key,{now:()=>new Date(now.getTime()+3600000)});
oldEnv.MERCHANT_CONFIG_JSON=JSON.stringify(cfg);
let requested=0;
const changed = await consumeRefresh(oldEnv,oldEnv.MERCHANT_REFRESH_QUEUE.messages.shift(),{now:()=>new Date(now.getTime()+3600000),graphql:async()=>{requested++;throw Error('must_not_read');}});
assert.equal(changed.code,'refresh_config_changed'); assert.equal(requested,0);
assert.deepEqual((await currentManifest(env.MERCHANT_FEED_BUCKET,market.key)).manifest,prior);
adversarial.push({case:'Old no-hold job delivered after reviewed hold configuration is bound',result:'PASS',code:changed.code,newSourceReads:requested,priorPointerPreserved:true});

const result = {status:'PASS_LOCAL_CODE_AND_SAVED_SOURCE_REVIEW',checkedAt:new Date().toISOString(),
  implementationHashesMatch:true, configOnlyAddsCanonicalSixHolds:true, protectedHashes,
  savedResults, importGraph:graph, adversarial, externalWrites:0, credentialsRead:0, newSourceCollections:0, tsvFilesWritten:0,
  limits:['Saved fixtures do not prove current buyer readiness or Google receipt.','Runtime graph import success is not a cloud deployment.','Deployment inline config is separately checked after the primary agent repair.']};
await writeFile(path.join(output,'independent-verification.json'),JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({status:result.status,savedCases:savedResults.length,adversarialCases:adversarial.length,runtimeModules:graph.length}));
