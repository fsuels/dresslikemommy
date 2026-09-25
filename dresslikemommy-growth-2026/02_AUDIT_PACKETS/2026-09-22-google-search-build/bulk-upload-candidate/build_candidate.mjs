import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { createHash } from "node:crypto";
import assert from "node:assert/strict";
import { Workbook } from "@oai/artifact-tool";

const dir = path.dirname(fileURLToPath(import.meta.url));
const payloadBytes = await fs.readFile(path.join(dir, "..", "payload.json"));
const payload = JSON.parse(payloadBytes);
const sourceManifest = JSON.parse(await fs.readFile(path.join(dir, "sources", "template_manifest.json"), "utf8"));
const campaign = payload.campaign.name;
const manifest = { status: "LOCAL_ONLY_NOT_UPLOADED_NOT_APPLIED", payloadSha256: createHash("sha256").update(payloadBytes).digest("hex"), campaign, files: [] };

function template(name) {
  const source = sourceManifest.find(s => s.file === name);
  assert(source, name);
  const rows = source.tables.CSV;
  const header = rows.find(row => ["Row Type", "Row type", "Action"].includes(row[0]));
  assert(header, name);
  return { source, header };
}
function cell(value) {
  const string = value === null || value === undefined ? "" : String(value);
  return /[",\r\n]/.test(string) ? `"${string.replaceAll('"', '""')}"` : string;
}
function columnName(index) {
  let result = "";
  for (let n = index; n > 0; n = Math.floor((n - 1) / 26)) result = String.fromCharCode(65 + (n - 1) % 26) + result;
  return result;
}
async function writeCandidate(filename, sourceFile, headers, objects, options = {}) {
  const { source, header } = template(sourceFile);
  assert(headers.every(h => header.includes(h)), `${filename}: unsupported header`);
  assert.equal(new Set(headers).size, headers.length);
  const rows = [headers, ...objects.map(object => headers.map(h => object[h] ?? ""))];
  assert(objects.every(object => object.Campaign === campaign));
  assert(objects.every(object => ["Add", "add"].includes(object.Action)));
  const statusColumn = headers.find(h => /^(Ad group|Ad|Keyword) status$/.test(h));
  if (statusColumn) assert(objects.every(o => o[statusColumn] === "Paused"));

  const workbook = Workbook.create();
  const sheet = workbook.worksheets.add("Upload");
  const area = `A1:${columnName(headers.length)}${rows.length}`;
  sheet.getRange(area).values = rows;
  workbook.recalculate();
  const values = sheet.getRange(area).values;
  assert.deepEqual(values, rows);
  const inspection = await workbook.inspect({ kind: "region", sheetId: sheet.name, range: `A1:${columnName(Math.min(headers.length, 7))}${Math.min(rows.length, 3)}`, maxChars: 1500 });
  assert(inspection.ndjson.length > 0);
  // The available Artifact Tool API has no documented CSV exporter. Serialize
  // its authored, read-back cell matrix as RFC4180 CSV, retaining exact headers.
  const csv = values.map(row => row.map(cell).join(",")).join("\r\n") + "\r\n";
  const target = path.join(dir, filename);
  await fs.writeFile(target, csv);
  manifest.files.push({ file: filename, rowCount: objects.length, headers, statusColumn: statusColumn ?? null, sourceFile, sourceUrl: source.url, schemaStatus: options.schemaStatus ?? "MATCHES_NATIVE_ADVERTISED_TEMPLATE_HEADERS", sha256: createHash("sha256").update(csv).digest("hex"), ...options });
}

await writeCandidate("01_ad_groups.PREVIEW_ONLY.csv", "native_ad_group_template.csv",
  ["Row Type", "Action", "Ad group status", "Campaign", "Ad group", "Ad group type", "Default max. CPC"],
  payload.ad_groups.map(group => ({ "Row Type": "Ad group", Action: "Add", "Ad group status": "Paused", Campaign: campaign, "Ad group": group.name, "Ad group type": "Standard", "Default max. CPC": Number(group.proposed_default_cpc_usd) })),
  { gates: ["Parent campaign must resolve to the intended saved paused campaign.", "USD account currency must be verified before applying bids.", "Native Preview must accept Manual CPC and each row."] });

await writeCandidate("02_keywords.PREVIEW_ONLY.csv", "native_keyword_template.csv",
  ["Row Type", "Action", "Keyword status", "Campaign", "Ad group", "Keyword", "Type", "Default max. CPC"],
  payload.ad_groups.flatMap(group => group.keywords.map(keyword => ({ "Row Type": "Keyword", Action: "Add", "Keyword status": "Paused", Campaign: campaign, "Ad group": group.name, Keyword: keyword.text, Type: keyword.match_type === "EXACT" ? "Exact match" : "Phrase match", "Default max. CPC": keyword.match_type === "EXACT" ? Number(keyword.proposed_max_cpc_usd) : "" }))),
  { gates: ["USD currency and intended paused parent must be verified.", "Phrase bids intentionally inherit the ad-group default; exact bids explicitly override it.", "Do not duplicate already saved draft keywords."] });

const rsaHeaders = ["Row Type", "Action", "Ad status", "Campaign", "Ad group", "Ad type", ...Array.from({length: 12}, (_, i) => `Headline ${i + 1}`), ...Array.from({length: 4}, (_, i) => `Description ${i + 1}`), "Description 1 position", "Path 1", "Path 2", "Final URL"];
const rsas = payload.ad_groups.map(group => {
  const ad = group.rsa;
  const row = { "Row Type": "Ad", Action: "Add", "Ad status": "Paused", Campaign: campaign, "Ad group": group.name, "Ad type": "Responsive search ad", "Description 1 position": 1, "Path 1": ad.display_paths[0].text, "Path 2": ad.display_paths[1].text, "Final URL": ad.final_url };
  ad.headlines.forEach((value, index) => { row[`Headline ${index + 1}`] = value.text; });
  ad.descriptions.forEach((value, index) => { row[`Description ${index + 1}`] = value.text; });
  return row;
});
await writeCandidate("03_responsive_search_ads.PREVIEW_ONLY.csv", "native_responsive_search_ad_template.csv", rsaHeaders, rsas,
  { gates: ["All headline and remaining-description positions are omitted and stay unpinned on creation.", "Reconcile already saved dress RSA before any Add action."] });

const negativeHeaders = ["Row Type", "Action", "Keyword status", "Level", "Campaign", "Ad group", "Negative keyword", "Type"];
function negativeRows(negatives) {
  return negatives.map(n => ({ "Row Type": "Negative keyword", Action: "Add", "Keyword status": "Paused", Level: n.scope === "CAMPAIGN" ? "Campaign" : "Ad group", Campaign: campaign, "Ad group": n.ad_group ?? "", "Negative keyword": n.text, Type: n.match_type === "EXACT" ? "Exact match" : "Phrase match" }));
}
await writeCandidate("04_campaign_negatives.PREVIEW_ONLY.csv", "native_ad_group_negative_keyword_template.csv", negativeHeaders, negativeRows(payload.negative_keywords.campaign),
  { gates: ["The native template explicitly supports Level=Campaign but generically labels Ad group required; campaign-level rows deliberately leave Ad group blank and require Preview validation.", "Paused negative rows are candidates only: do not claim exclusions are effective without native readback."] });
await writeCandidate("05_ad_group_negatives.PREVIEW_ONLY.csv", "native_ad_group_negative_keyword_template.csv", negativeHeaders, negativeRows(payload.negative_keywords.ad_groups),
  { gates: ["All negative rows explicitly say Paused as requested; native support/semantics must be read back.", "Receiving-group and deliberate-traffic-exclusion gates from payload.json remain prerequisites to any later effective routing."] });

const links = new Map(payload.assets.sitelinks.map(s => [s.id, s]));
const sitelinkRows = payload.assets.sitelink_associations.map(association => {
  const asset = links.get(association.sitelink_id);
  return { "Row Type": "Sitelink", Action: "Add", "Asset action": "Create new", Level: "Ad group", Campaign: campaign, "Ad group": association.ad_group, "Sitelink text": asset.text, Description: asset.description_1, "Description 2": asset.description_2, "Final URL": asset.final_url };
});
await writeCandidate("06_sitelink_associations.HELP_TEMPLATE_PREVIEW_ONLY.csv", "help_create_sitelink.csv",
  ["Row Type", "Action", "Asset action", "Level", "Campaign", "Ad group", "Sitelink text", "Description", "Description 2", "Final URL"], sitelinkRows,
  { schemaStatus: "MATCHES_OFFICIAL_HELP_TEMPLATE_HEADERS", uniqueContentDefinitions: 6, gates: ["Six distinct content definitions are repeated across 14 requested associations, following Google's multiple-row guidance.", "Actual unique asset object count/deduplication is unverified. Inspect inherited/existing assets before applying to avoid duplicates.", "No asset status column is advertised here: these associations must stay confined to the exact verified paused campaign.", "Destination and advertised-selection clearance remain required."] });

await writeCandidate("07_callouts.HELP_TEMPLATE_PREVIEW_ONLY.csv", "help_create_callout.csv",
  ["Row type", "Action", "Campaign", "Ad group", "Callout text"],
  payload.assets.callouts.map(asset => ({ "Row type": "Callout extension", Action: "add", Campaign: campaign, "Ad group": "", "Callout text": asset.text })),
  { schemaStatus: "MATCHES_OFFICIAL_HELP_LEGACY_TEMPLATE_HEADERS_REQUIRES_NATIVE_PREVIEW", gates: ["Blank Ad group follows the official campaign-level example; campaign scope is the explicit proposed operator inference in payload.json.", "Parent reports four callouts already saved in the draft. Reconcile those instead of blindly adding these rows.", "No supported status field exists in this template; only associate with the exact verified paused parent."] });

const snippet = payload.assets.structured_snippet;
await writeCandidate("08_structured_snippet.HELP_TEMPLATE_PREVIEW_ONLY.csv", "help_create_snippet.csv",
  ["Action", "Campaign", "Ad group", "Structured snippet header", "Structured snippet values"],
  [{ Action: "add", Campaign: campaign, "Ad group": snippet.ad_group, "Structured snippet header": snippet.header, "Structured snippet values": snippet.values.map(v => v.text).join(";") }],
  { schemaStatus: "MATCHES_OFFICIAL_HELP_TEMPLATE_HEADERS_REQUIRES_NATIVE_PREVIEW", gates: ["Only Mommy & Me Outfits receives this association.", "No status field is advertised; parent campaign must be verified paused.", "Destination/category clearance remains required."] });

const campaignSource = template("native_campaign_template.csv");
const stub = {
  artifactType: "NON_EXECUTABLE_CAMPAIGN_STUB_DO_NOT_UPLOAD",
  blockedBy: ["Budget type/amount/dates unanswered", "Account currency USD unverified", "Campaign identity and safe paused-create preview unverified"],
  sourceUrl: campaignSource.source.url,
  proposedRow: { "Row Type": "Campaign", Action: "Add", "Campaign status": "Paused", Campaign: campaign, "Campaign type": "Search", Networks: "Google search", Budget: null, "Budget type": null, "Bid strategy type": "Manual CPC", "Campaign start date": null, "Campaign end date": null, Language: "en", Location: "United States", "EU political ads": "No" },
  notes: ["Current native campaign template marks Budget and EU political ads required on create. Budget is intentionally null, and no campaign CSV is emitted.", "No is an apparel-content classification for EU political ads, not a spending authorization.", "The native template supports Manual CPC even though the creation wizard did not offer it; account acceptance requires Preview.", "Presence-only targeting, campaign purchase-goal selection and AI automation controls are not expressible through verified columns in this template; verify in the native account before any later activation.", "Do not import against an ambiguous duplicate campaign name or assume a wizard draft is an importable saved campaign."]
};
assert(Object.keys(stub.proposedRow).every(key => campaignSource.header.includes(key)));
assert.equal(stub.proposedRow.Budget, null);
assert.equal(stub.proposedRow["Campaign status"], "Paused");
await fs.writeFile(path.join(dir, "campaign_stub.NOT_UPLOADABLE.json"), JSON.stringify(stub, null, 2) + "\n");
manifest.counts = { campaignCsvRows: 0, campaignStubRows: 1, adGroups: 6, positiveKeywords: 48, rsas: 6, headlines: 72, descriptions: 24, campaignNegatives: 26, adGroupNegatives: 41, uniqueSitelinkContents: 6, sitelinkAssociations: 14, callouts: 4, snippets: 1 };
manifest.unsupportedOrUnverified = [
  "No executable campaign CSV: budget type/amount/dates and USD currency remain unknown.",
  "Advanced location Presence-only setting lacks a verified column in the downloaded native campaign schema.",
  "Purchases-only campaign goal, conversion action identity/deduplication, consent and completed-order validity lack verified upload fields.",
  "AI Max, text customization and final URL expansion toggles lack verified upload fields; do not infer paused bulk-created campaign defaults.",
  "Native asset status columns are unverified/absent in the supplied asset templates. Asset rows require a verified paused parent.",
  "Campaign-negative blank Ad group and all negative Paused status semantics need native Preview/readback; no claim of effective exclusions.",
  "Callout/structured-snippet templates on the official Help page contain legacy examples and require current native Preview.",
  "Sitelink asset object deduplication is unverified; 14 association rows carry six distinct definitions.",
  "Existing draft contents and four already saved callouts require deduplication/reconciliation before Add; no claim that these files can amend the wizard draft.",
  "No native upload or Preview has run for these files; schema-supported candidates are not platform acceptance or publication receipts."
];
await fs.writeFile(path.join(dir, "candidate_manifest.json"), JSON.stringify(manifest, null, 2) + "\n");
console.log(JSON.stringify({ status: manifest.status, counts: manifest.counts, files: manifest.files.map(f => ({ file: f.file, rows: f.rowCount, statusColumn: f.statusColumn, schemaStatus: f.schemaStatus })) }, null, 2));
