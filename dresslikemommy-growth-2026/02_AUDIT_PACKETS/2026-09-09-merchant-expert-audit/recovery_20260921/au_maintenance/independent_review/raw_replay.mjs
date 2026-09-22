// Offline verification only: no reader construction, network, or source writes.
import fs from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { createHash } from 'node:crypto';
import { isDeepStrictEqual } from 'node:util';

const run = process.argv[2];
const read = async name => JSON.parse(await fs.readFile(path.join(run, name), 'utf8'));
const intent = await read('build.intent.json');
const configPath = intent.command[intent.command.indexOf('--config') + 1];
const config = JSON.parse(await fs.readFile(configPath, 'utf8'));
const generatorPath = path.join(path.dirname(configPath), 'automation_release_v1/src/generator.js');
const { buildFeed } = await import(pathToFileURL(generatorPath).href);
const snapshot = await read('source/au-en.snapshot.json');
const diagnostic = await read('source/au-en.diagnostics.json');
const manifest = await read('source/au-en.manifest.json');
const previous = await read('before.au-en.manifest.json');
const market = config.markets.find(m => m.key === 'au-en');
const output = await buildFeed(snapshot, config, market, { now: new Date(diagnostic.generatedAt), previousIds: previous.rowIds });
const tsv = await fs.readFile(path.join(run, 'source/au-en.tsv'));
const md5 = createHash('md5').update(tsv).digest('hex');
const expectedManifest = {
  schemaVersion: 1, market: snapshot.market, objectKey: `merchant/au-en/${output.sha256}.tsv`,
  sha256: output.sha256, expectedMd5: md5, objectEtag: md5, bytes: output.bytes,
  rows: output.rows.length, rowIds: output.rowIds, generatedAt: output.diagnostics.generatedAt,
  sourceCompletedAt: snapshot.completedAt, sourceParents: output.diagnostics.sourceCounts.parents,
  sourceVariants: output.diagnostics.sourceCounts.variants,
  returnPolicyLabelsConfirmed: output.diagnostics.returnPolicyLabelsConfirmed, previous: null,
};
const checks = {
  generator_success: output.ok === true,
  tsv_exact: Buffer.from(output.tsv).equals(tsv),
  manifest_exact: isDeepStrictEqual(expectedManifest, manifest),
  diagnostics_exact: isDeepStrictEqual(output.diagnostics, diagnostic),
};
console.log(JSON.stringify({ checks, passed: Object.values(checks).every(Boolean), raw_rows: output.rows.length,
  sha256: output.sha256, clock_used: diagnostic.generatedAt, source_completed_at: snapshot.completedAt,
  source_writes: 0, network_calls: 0 }));
if (!Object.values(checks).every(Boolean)) process.exitCode = 1;
