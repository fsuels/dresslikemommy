#!/usr/bin/env node
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const rawDir = path.join(__dirname, "raw");
const candidateCsv = path.join(
  __dirname,
  "..",
  "..",
  "..",
  "2026-04-29-pinterest-shopping-ads-gate",
  "pinterest_paid_ready_candidate_offer_rows.csv",
);
const previousProofCsv = path.join(
  __dirname,
  "..",
  "..",
  "..",
  "2026-05-08-paid-growth-pt-presentment-url-readback",
  "lanes",
  "pinterest",
  "raw",
  "full_item_metadata_rows.csv",
);
const reresolveCsv = path.join(rawDir, "unresolved_variant_reresolve_rows.csv");

function parseCsv(text) {
  const rows = [];
  let row = [];
  let cell = "";
  let quoted = false;
  for (let i = 0; i < text.length; i += 1) {
    const ch = text[i];
    const next = text[i + 1];
    if (quoted) {
      if (ch === '"' && next === '"') {
        cell += '"';
        i += 1;
      } else if (ch === '"') {
        quoted = false;
      } else {
        cell += ch;
      }
    } else if (ch === '"') {
      quoted = true;
    } else if (ch === ",") {
      row.push(cell);
      cell = "";
    } else if (ch === "\n") {
      row.push(cell);
      rows.push(row);
      row = [];
      cell = "";
    } else if (ch !== "\r") {
      cell += ch;
    }
  }
  if (cell || row.length) {
    row.push(cell);
    rows.push(row);
  }
  const headers = rows.shift() || [];
  return rows
    .filter((r) => r.some((v) => v !== ""))
    .map((r) => Object.fromEntries(headers.map((h, i) => [h, r[i] || ""])));
}

function toCsv(rows, preferredHeaders = []) {
  const headers = [
    ...preferredHeaders,
    ...[...new Set(rows.flatMap((row) => Object.keys(row)))].filter((h) => !preferredHeaders.includes(h)),
  ];
  const esc = (value) => {
    const s = `${value ?? ""}`;
    return /[",\n]/.test(s) ? `"${s.replaceAll('"', '""')}"` : s;
  };
  return [headers.join(","), ...rows.map((row) => headers.map((h) => esc(row[h])).join(","))].join("\n") + "\n";
}

function byVariant(rows) {
  return new Map(rows.map((row) => [String(row.shopify_variant_id), row]));
}

const candidates = parseCsv(await fs.readFile(candidateCsv, "utf8"));
const previousProof = byVariant(parseCsv(await fs.readFile(previousProofCsv, "utf8")));
const reresolveProof = byVariant(parseCsv(await fs.readFile(reresolveCsv, "utf8")));

const cleanRows = [];
const excludedRows = [];

for (const candidate of candidates) {
  const variantId = String(candidate.shopify_variant_id);
  const recovered = reresolveProof.get(variantId);
  const previous = previousProof.get(variantId);
  if (recovered?.status === "RERESOLVED_EN_US_IN_STOCK") {
    cleanRows.push({
      ...candidate,
      pinterest_item_level_status: "FOUND_EN_US_IN_STOCK",
      pinterest_en_us_pin_id: recovered.pinterest_pin_id,
      pinterest_en_us_feed_profile_id: recovered.pinterest_feed_profile_id,
      pinterest_en_us_locale: recovered.pinterest_locale,
      pinterest_en_us_availability: recovered.pinterest_availability,
      pinterest_en_us_link: recovered.pinterest_link,
      pinterest_en_us_price: recovered.pinterest_price,
      review_only_launch_status: "CANDIDATE_ONLY_NOT_LAUNCH_APPROVED",
      proof_source: "2026-05-08-reresolved-by-shopify-variant-id",
      previous_pinterest_en_us_pin_id: candidate.pinterest_en_us_pin_id,
    });
  } else if (previous?.status === "FOUND_EN_US_IN_STOCK") {
    cleanRows.push({
      ...candidate,
      pinterest_item_level_status: "FOUND_EN_US_IN_STOCK",
      proof_source: "2026-05-08-full-pin-metadata-proof",
      previous_pinterest_en_us_pin_id: candidate.pinterest_en_us_pin_id,
    });
  } else {
    excludedRows.push({
      ...candidate,
      exclusion_status: recovered?.status || previous?.status || "NO_CURRENT_PROOF",
      exclusion_reason: "No current EN-US Pinterest in-stock item metadata by stale pin ID or fresh Shopify variant ID re-resolution.",
      proof_source: recovered ? "2026-05-08-reresolved-by-shopify-variant-id" : "2026-05-08-full-pin-metadata-proof",
      previous_pinterest_en_us_pin_id: candidate.pinterest_en_us_pin_id,
      pinterest_item_level_status: "NOT_CURRENTLY_RESOLVED_EN_US",
      pinterest_en_us_pin_id: "",
      pinterest_en_us_feed_profile_id: "",
      pinterest_en_us_locale: "",
      pinterest_en_us_availability: "",
      pinterest_en_us_link: "",
      pinterest_en_us_price: "",
      review_only_launch_status: "EXCLUDED_FROM_CURRENT_PINTEREST_SCOPE",
    });
  }
}

const countBy = (rows, key) =>
  rows.reduce((acc, row) => {
    const value = row[key] || "unknown";
    acc[value] = (acc[value] || 0) + 1;
    return acc;
  }, {});

const summary = {
  status: "PINTEREST_US_CLEAN_SCOPE_BUILT_NO_ACCOUNT_WRITES",
  generated_at: new Date().toISOString(),
  source_candidate_rows: candidates.length,
  previous_found_rows: [...previousProof.values()].filter((row) => row.status === "FOUND_EN_US_IN_STOCK").length,
  recovered_rows: [...reresolveProof.values()].filter((row) => row.status === "RERESOLVED_EN_US_IN_STOCK").length,
  clean_scope_rows: cleanRows.length,
  excluded_rows: excludedRows.length,
  clean_scope_by_custom_label_2: countBy(cleanRows, "custom_label_2"),
  excluded_by_custom_label_2: countBy(excludedRows, "custom_label_2"),
  excluded_variant_ids: excludedRows.map((row) => row.shopify_variant_id),
  output_files: {
    clean_scope_csv: path.join(rawDir, "pinterest_us_clean_launch_scope_resolved_342.csv"),
    exclusions_csv: path.join(rawDir, "pinterest_us_unresolved_exclusions_4.csv"),
    summary_json: path.join(rawDir, "pinterest_us_clean_scope_summary.json"),
  },
  writes_made: "Local files only. No Pinterest, Shopify, Merchant, Google Ads, tag, CAPI, catalog source, product group, campaign, budget, bid, or spend writes.",
};

await fs.writeFile(summary.output_files.clean_scope_csv, toCsv(cleanRows, [
  "proof_source",
  "pinterest_product_group",
  "pinterest_group_label",
  "shopify_product_id",
  "shopify_variant_id",
  "merchant_center_item_id",
  "title",
  "product_url",
  "image_url",
  "price",
  "cost",
  "gross_margin_percent",
  "max_cac",
  "custom_label_0",
  "custom_label_2",
  "custom_label_4",
  "pinterest_item_level_status",
  "pinterest_en_us_pin_id",
  "pinterest_en_us_feed_profile_id",
  "pinterest_en_us_locale",
  "pinterest_en_us_availability",
  "pinterest_en_us_link",
  "pinterest_en_us_price",
  "review_only_launch_status",
  "previous_pinterest_en_us_pin_id",
]));
await fs.writeFile(summary.output_files.exclusions_csv, toCsv(excludedRows, [
  "exclusion_status",
  "exclusion_reason",
  "proof_source",
  "pinterest_product_group",
  "pinterest_group_label",
  "shopify_product_id",
  "shopify_variant_id",
  "merchant_center_item_id",
  "title",
  "product_url",
  "price",
  "cost",
  "gross_margin_percent",
  "custom_label_0",
  "custom_label_2",
  "custom_label_4",
  "previous_pinterest_en_us_pin_id",
]));
await fs.writeFile(summary.output_files.summary_json, JSON.stringify(summary, null, 2));

console.log(JSON.stringify(summary, null, 2));
