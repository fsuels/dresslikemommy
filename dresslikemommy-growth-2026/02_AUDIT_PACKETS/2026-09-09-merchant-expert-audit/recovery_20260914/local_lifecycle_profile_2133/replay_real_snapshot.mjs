// Historical catalog rehearsal only. No network, credentials, or source refresh.
import fs from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { createHash } from 'node:crypto';

const [local, historical, out] = process.argv.slice(2);
const { buildFeed } = await import(pathToFileURL(path.join(local, '../automation_release_v1/src/generator.js')));
const read = async name => JSON.parse(await fs.readFile(name, 'utf8'));
const config = await read(path.join(local, '../automation_release_v1/config.json'));
const snapshotPath = path.join(historical, 'unfiltered/us-en.snapshot.json');
const snapshotBytes = await fs.readFile(snapshotPath);
const snapshot = JSON.parse(snapshotBytes);
const originalDiagnostics = await read(path.join(historical, 'unfiltered/us-en.diagnostics.json'));
const before = await read(path.join(historical, 'before.pointer.json'));
const result = await buildFeed(snapshot, config, config.markets.find(item => item.key === 'us-en'),
  { now: new Date(originalDiagnostics.generatedAt), previousIds: before.rowIds });
if (!result.ok) throw new Error('historical_replay_build_failed');
const digest = (body, algorithm = 'sha256') => createHash(algorithm).update(body).digest('hex');
const md5 = digest(result.tsv, 'md5');
const manifest = {
  schemaVersion: 1, market: snapshot.market, objectKey: `merchant/us-en/${result.sha256}.tsv`,
  sha256: result.sha256, expectedMd5: md5, objectEtag: md5,
  bytes: result.bytes, rows: result.rows.length, rowIds: result.rowIds,
  generatedAt: result.diagnostics.generatedAt, sourceCompletedAt: snapshot.completedAt,
  sourceParents: result.diagnostics.sourceCounts.parents,
  sourceVariants: result.diagnostics.sourceCounts.variants,
  returnPolicyLabelsConfirmed: result.diagnostics.returnPolicyLabelsConfirmed, previous: null,
};
await fs.mkdir(path.join(out, 'candidate'), { recursive: true });
await fs.writeFile(path.join(out, 'candidate/us-en.tsv'), result.tsv);
await fs.writeFile(path.join(out, 'candidate/us-en.snapshot.json'), snapshotBytes);
for (const [name, value] of [['manifest', manifest], ['diagnostics', result.diagnostics]]) {
  await fs.writeFile(path.join(out, `candidate/us-en.${name}.json`), JSON.stringify(value, null, 2) + '\n');
}
for (const name of ['before.pointer.json', 'before.tsv']) {
  await fs.copyFile(path.join(historical, name), path.join(out, name));
}
const publishedBody = await fs.readFile(path.join(historical, 'candidate/us-en.tsv'));
if (!Buffer.from(result.tsv).equals(publishedBody)) throw new Error('historical_published_body_changed');
process.stdout.write(JSON.stringify({
  historicalRehearsal: true, sourcePath: snapshotPath,
  sourceSnapshotSha256: digest(snapshotBytes), sourceCompletedAt: snapshot.completedAt,
  originalGeneratedAt: originalDiagnostics.generatedAt, generatedAt: result.diagnostics.generatedAt,
  sourceParents: manifest.sourceParents, sourceVariants: manifest.sourceVariants,
  rows: manifest.rows, bytes: manifest.bytes, feedSha256: result.sha256,
  matchesPreviouslyPublishedFeedBytes: true,
  previousPublishedFeedPath: path.join(historical, 'candidate/us-en.tsv'),
  liveSourceRefresh: false, sourceClockChanged: false, networkCalls: 0,
}) + '\n');
