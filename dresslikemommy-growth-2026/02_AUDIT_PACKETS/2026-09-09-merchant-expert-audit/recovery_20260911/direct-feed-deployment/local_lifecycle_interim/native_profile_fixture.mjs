// Synthetic local integration fixture. No network or private credentials.
import fs from 'node:fs/promises';
import path from 'node:path';
import { createHash } from 'node:crypto';
import { product, variant, snapshot } from '../automation_release_v1/test/fixtures.js';
import { buildFeed } from '../automation_release_v1/src/generator.js';

const [out, scenario = 'base'] = process.argv.slice(2);
const config = JSON.parse(await fs.readFile(new URL('../automation_release_v1/config.json', import.meta.url), 'utf8'));
const market = config.markets.find(item => item.key === 'us-en');
const protectedVariants = [41883237220449, 41883237285985, 41883237318753, 41883238465633, 41883238498401];
const baseline = () => [product(6718945034337, [variant(39756755861601)]),
  product(7230336729185, protectedVariants.map(id => variant(id))),
  product(7516369715297, [variant(9001)]), product(2, [Object.assign(variant(201), { availableForSale: false })]),
  product(3, [variant(301)])].map(item => ({ ...item, catalogPublished: true }));
function input(products, time) {
  const value = snapshot(products, market);
  value.startedAt = value.completedAt = time;
  value.marketContext = { currency: market.currency, activeMarketIds: [market.marketId],
    catalogs: structuredClone(market.expectedCatalogs) };
  value.finalMarketContext = structuredClone(value.marketContext);
  return value;
}
const beforeTime = '2026-09-14T19:00:00.000Z', afterTime = '2026-09-14T20:00:00.000Z';
const before = await buildFeed(input(baseline(), beforeTime), config, market, { now: new Date(beforeTime) });
let products = baseline();
if (scenario === 'held-absent') products = products.filter(item => item.id !== 'gid://shopify/Product/7516369715297');
if (scenario === 'protected-parent-absent') products = products.filter(item => item.id !== 'gid://shopify/Product/6718945034337');
if (scenario === 'protected-unavailable') products[0].variants[0].availableForSale = false;
if (scenario === 'protected-unpublished') products[0].onlinePublished = false;
const source = input(products, afterTime);
const after = await buildFeed(source, config, market, { now: new Date(afterTime), previousIds: before.rowIds });
if (!before.ok || !after.ok) throw new Error('synthetic_fixture_build_failed');
function manifest(result, source) {
  const md5 = createHash('md5').update(result.tsv).digest('hex');
  return { schemaVersion: 1, market: source.market, objectKey: `merchant/us-en/${result.sha256}.tsv`,
    sha256: result.sha256, expectedMd5: md5, objectEtag: md5, bytes: result.bytes,
    rows: result.rows.length, rowIds: result.rowIds, generatedAt: result.diagnostics.generatedAt,
    sourceCompletedAt: source.completedAt, sourceParents: result.diagnostics.sourceCounts.parents,
    sourceVariants: result.diagnostics.sourceCounts.variants,
    returnPolicyLabelsConfirmed: result.diagnostics.returnPolicyLabelsConfirmed, previous: null };
}
await fs.mkdir(path.join(out, 'candidate'), { recursive: true });
await fs.writeFile(path.join(out, 'before.tsv'), before.tsv);
await fs.writeFile(path.join(out, 'before.pointer.json'), JSON.stringify(manifest(before, input(baseline(), beforeTime)), null, 2) + '\n');
await fs.writeFile(path.join(out, 'candidate/us-en.tsv'), after.tsv);
for (const [suffix, value] of [['snapshot', source], ['manifest', manifest(after, source)], ['diagnostics', after.diagnostics]]) {
  await fs.writeFile(path.join(out, `candidate/us-en.${suffix}.json`), JSON.stringify(value, null, 2) + '\n');
}
process.stdout.write(JSON.stringify({ synthetic: true, scenario, rows: after.rows.length, networkCalls: 0 }) + '\n');
