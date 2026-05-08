#!/usr/bin/env node
import fs from "node:fs/promises";
import path from "node:path";

const laneDir = path.dirname(new URL(import.meta.url).pathname);
const rawDir = path.join(laneDir, "raw");
const port = process.env.CDP_PORT || "9333";
const base = `http://127.0.0.1:${port}`;
const catalogId = "3041764155561548387";
const enFeedProfileId = "3041760867124595727";
const candidateCsv =
  process.env.PINTEREST_CANDIDATE_CSV ||
  path.resolve(
    laneDir,
    "../../../2026-04-29-pinterest-shopping-ads-gate/pinterest_paid_ready_candidate_offer_rows.csv",
  );

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

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

function toCsv(rows) {
  if (!rows.length) return "";
  const headers = Object.keys(rows[0]);
  const esc = (v) => {
    const s = `${v ?? ""}`;
    return /[",\n]/.test(s) ? `"${s.replaceAll('"', '""')}"` : s;
  };
  return [headers.join(","), ...rows.map((r) => headers.map((h) => esc(r[h])).join(","))].join("\n") + "\n";
}

class CDP {
  constructor(wsUrl) {
    this.wsUrl = wsUrl;
    this.nextId = 1;
    this.pending = new Map();
  }

  async connect() {
    this.ws = new WebSocket(this.wsUrl);
    await new Promise((resolve, reject) => {
      const timeout = setTimeout(() => reject(new Error("CDP websocket timed out")), 5000);
      this.ws.onopen = () => {
        clearTimeout(timeout);
        resolve();
      };
      this.ws.onerror = (event) => {
        clearTimeout(timeout);
        reject(new Error(`CDP websocket error: ${event.message || "unknown"}`));
      };
    });
    this.ws.onmessage = (event) => {
      const msg = JSON.parse(event.data);
      if (!msg.id || !this.pending.has(msg.id)) return;
      const { resolve, reject } = this.pending.get(msg.id);
      this.pending.delete(msg.id);
      if (msg.error) reject(new Error(JSON.stringify(msg.error)));
      else resolve(msg.result || {});
    };
  }

  send(method, params = {}, timeoutMs = 30000) {
    const id = this.nextId++;
    this.ws.send(JSON.stringify({ id, method, params }));
    return new Promise((resolve, reject) => {
      this.pending.set(id, { resolve, reject });
      setTimeout(() => {
        if (!this.pending.has(id)) return;
        this.pending.delete(id);
        reject(new Error(`CDP command timed out: ${method}`));
      }, timeoutMs);
    });
  }

  close() {
    this.ws?.close();
  }
}

async function createTarget() {
  const url = `${base}/json/new?${encodeURIComponent(`https://www.pinterest.com/business/catalogs/${catalogId}/products/`)}`;
  let resp = await fetch(url, { method: "PUT" });
  if (!resp.ok) resp = await fetch(url);
  if (!resp.ok) throw new Error(`Unable to create CDP target: ${resp.status}`);
  return resp.json();
}

async function main() {
  await fs.mkdir(rawDir, { recursive: true });
  const candidates = parseCsv(await fs.readFile(candidateCsv, "utf8"));
  const pinIds = [...new Set(candidates.map((row) => row.pinterest_en_us_pin_id).filter(Boolean))];
  const target = await createTarget();
  const cdp = new CDP(target.webSocketDebuggerUrl);
  await cdp.connect();
  await cdp.send("Page.enable");
  await cdp.send("Runtime.enable");
  await sleep(8000);

  const expression = `(async () => {
    const catalogId = ${JSON.stringify(catalogId)};
    const pinIds = ${JSON.stringify(pinIds)};
    const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
    const csrf = (document.cookie.match(/(?:^|; )csrftoken=([^;]+)/) || [])[1] || "";
    async function apiResource(url, data) {
      const body = new URLSearchParams();
      body.set("source_url", "/business/catalogs/" + catalogId + "/products/");
      body.set("data", JSON.stringify({ options: { url, data }, context: {} }));
      const response = await fetch("/resource/ApiResource/create/", {
        method: "POST",
        credentials: "include",
        headers: {
          "content-type": "application/x-www-form-urlencoded",
          "x-csrftoken": csrf,
          "x-pinterest-appstate": "active"
        },
        body
      });
      const json = await response.json().catch(() => ({}));
      return {
        ok: response.ok,
        status: response.status,
        endpoint: json.resource_response?.endpoint_name || "",
        data: json.resource_response?.data || null,
        message: json.resource_response?.message || "",
        code: json.resource_response?.code ?? null
      };
    }
    const metadata = [];
    const requests = [];
    for (let i = 0; i < pinIds.length; i += 10) {
      const pins = pinIds.slice(i, i + 10);
      const result = await apiResource("/v3/catalogs/" + catalogId + "/item_metadata/retail/", {
        include_details: true,
        include_media: false,
        pin_ids: pins
      });
      const data = Array.isArray(result.data) ? result.data : [];
      for (const row of data) {
        metadata.push({
          requested_pin_ids: pins,
          pin_id: row.main_pin_id || row.pin_id || (Array.isArray(row.pin_ids) ? row.pin_ids[0] : ""),
          pin_ids: row.pin_ids || [],
          item_id: row.item_id || "",
          feed_profile_id: row.feed_profile_id || "",
          locale: row.locale || "",
          country: row.country || "",
          availability: row.availability || "",
          condition: row.condition || "",
          title: row.title || "",
          link: row.link || "",
          price: row.price || "",
          currency_type: row.currency_type || "",
          custom_label_0: row.custom_label_0 || "",
          custom_label_2: row.custom_label_2 || "",
          custom_label_4: row.custom_label_4 || ""
        });
      }
      requests.push({ pins: pins.length, ok: result.ok, status: result.status, rows: data.length, message: result.message, code: result.code });
      await sleep(150);
    }
    return { metadata, requests };
  })()`;

  const probe = await cdp.send("Runtime.evaluate", { expression, awaitPromise: true, returnByValue: true }, 300000);
  const value = probe.result?.value || {};
  cdp.close();
  await fetch(`${base}/json/close/${target.id}`).catch(() => null);

  const metadata = value.metadata || [];
  const enRows = metadata.filter((row) => row.feed_profile_id === enFeedProfileId && row.locale === "en-US" && row.country === "US");
  const byPin = new Map();
  for (const row of enRows) {
    for (const pin of row.pin_ids?.length ? row.pin_ids : [row.pin_id]) byPin.set(String(pin), row);
    if (row.pin_id) byPin.set(String(row.pin_id), row);
  }
  const outputRows = candidates.map((candidate) => {
    const match = byPin.get(String(candidate.pinterest_en_us_pin_id));
    return {
      status: match?.availability === "IN_STOCK" ? "FOUND_EN_US_IN_STOCK" : match ? `FOUND_${match.availability || "UNKNOWN"}` : "NOT_FOUND_BY_PIN_METADATA",
      pinterest_product_group: candidate.pinterest_product_group,
      shopify_product_id: candidate.shopify_product_id,
      shopify_variant_id: candidate.shopify_variant_id,
      title: candidate.title,
      product_url: candidate.product_url,
      price: candidate.price,
      cost: candidate.cost,
      gross_margin_percent: candidate.gross_margin_percent,
      custom_label_0: candidate.custom_label_0,
      custom_label_2: candidate.custom_label_2,
      custom_label_4: candidate.custom_label_4,
      previous_pinterest_pin_id: candidate.pinterest_en_us_pin_id,
      pinterest_pin_id: match?.pin_id || "",
      pinterest_item_id: match?.item_id || "",
      pinterest_feed_profile_id: match?.feed_profile_id || "",
      pinterest_locale: match?.locale || "",
      pinterest_country: match?.country || "",
      pinterest_availability: match?.availability || "",
      pinterest_title: match?.title || "",
      pinterest_link: match?.link || "",
      pinterest_price: match?.price || "",
      pinterest_currency_type: match?.currency_type || "",
    };
  });
  const byGroup = {};
  for (const row of outputRows) {
    const key = row.custom_label_2 || "unknown";
    byGroup[key] ||= { requested: 0, found_en_us_in_stock: 0, not_found: 0, other: 0 };
    byGroup[key].requested += 1;
    if (row.status === "FOUND_EN_US_IN_STOCK") byGroup[key].found_en_us_in_stock += 1;
    else if (row.status === "NOT_FOUND_BY_PIN_METADATA") byGroup[key].not_found += 1;
    else byGroup[key].other += 1;
  }
  const summary = {
    status: "READ_ONLY_FULL_PIN_METADATA_PROBE_COMPLETE",
    generated_at: new Date().toISOString(),
    candidate_csv: candidateCsv,
    total_candidate_rows: candidates.length,
    unique_pin_ids_requested: pinIds.length,
    metadata_request_count: value.requests?.length || 0,
    metadata_rows_returned: metadata.length,
    en_us_rows_returned: enRows.length,
    matched_en_us_in_stock_rows: outputRows.filter((row) => row.status === "FOUND_EN_US_IN_STOCK").length,
    unmatched_rows: outputRows.filter((row) => row.status === "NOT_FOUND_BY_PIN_METADATA").length,
    non_in_stock_or_other_rows: outputRows.filter((row) => !["FOUND_EN_US_IN_STOCK", "NOT_FOUND_BY_PIN_METADATA"].includes(row.status)).length,
    by_group: byGroup,
    english_feed_profile_id: enFeedProfileId,
    writes_made: "No Pinterest writes; read-only metadata requests from logged-in browser session and local evidence files only.",
  };
  await fs.writeFile(path.join(rawDir, "full_item_metadata_summary.json"), JSON.stringify(summary, null, 2));
  await fs.writeFile(path.join(rawDir, "full_item_metadata_rows.csv"), toCsv(outputRows));
  await fs.writeFile(path.join(rawDir, "full_item_metadata_api_sanitized.json"), JSON.stringify({ requests: value.requests || [], enRows }, null, 2));
  console.log(JSON.stringify(summary, null, 2));
  process.exit(0);
}

main().catch(async (error) => {
  await fs.mkdir(rawDir, { recursive: true });
  const summary = {
    status: "BLOCKED_FULL_PIN_METADATA_PROBE_ERROR",
    generated_at: new Date().toISOString(),
    error: error.message,
  };
  await fs.writeFile(path.join(rawDir, "full_item_metadata_summary.json"), JSON.stringify(summary, null, 2));
  console.error(JSON.stringify(summary, null, 2));
  process.exit(1);
});
