#!/usr/bin/env node
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const rawDir = path.join(__dirname, "raw");
const port = process.env.CDP_PORT || "9333";
const base = `http://127.0.0.1:${port}`;
const catalogId = "3041764155561548387";
const merchantId = "3041760832963738705";
const advertiserId = "549756244483";
const enFeedProfileId = "3041760867124595727";
const sitemapFeedId = "3041760916127467912";
const candidateCsv =
  process.env.PINTEREST_CANDIDATE_CSV ||
  path.join(
    __dirname,
    "..",
    "..",
    "..",
    "2026-04-29-pinterest-shopping-ads-gate",
    "pinterest_paid_ready_candidate_offer_rows.csv",
  );
const itemLimit = Number.parseInt(process.env.PINTEREST_ITEM_LIMIT || "45", 10);

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

function sanitizeUrl(value) {
  try {
    const u = new URL(value);
    const keys = [...u.searchParams.keys()];
    return `${u.origin}${u.pathname}${keys.length ? `?${keys.join("&")}` : ""}`;
  } catch {
    return value;
  }
}

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
    .map((r) =>
      Object.fromEntries(headers.map((h, i) => [h, r[i] || ""])),
    );
}

function stratifiedSample(rows, limit) {
  const byGroup = new Map();
  for (const row of rows) {
    const key = row.custom_label_2 || "unknown";
    if (!byGroup.has(key)) byGroup.set(key, []);
    byGroup.get(key).push(row);
  }
  const groups = [...byGroup.keys()].sort();
  const out = [];
  while (out.length < limit && groups.length) {
    let added = false;
    for (const group of groups) {
      const groupRows = byGroup.get(group);
      if (groupRows?.length && out.length < limit) {
        out.push(groupRows.shift());
        added = true;
      }
    }
    if (!added) break;
  }
  return out;
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
    this.handlers = new Map();
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
      if (msg.id && this.pending.has(msg.id)) {
        const { resolve, reject } = this.pending.get(msg.id);
        this.pending.delete(msg.id);
        if (msg.error) reject(new Error(JSON.stringify(msg.error)));
        else resolve(msg.result || {});
        return;
      }
      const callbacks = this.handlers.get(msg.method);
      if (callbacks) {
        for (const cb of callbacks) cb(msg.params || {});
      }
    };
  }

  send(method, params = {}, timeoutMs = 30000) {
    const id = this.nextId++;
    this.ws.send(JSON.stringify({ id, method, params }));
    return new Promise((resolve, reject) => {
      this.pending.set(id, { resolve, reject });
      setTimeout(() => {
        if (this.pending.has(id)) {
          this.pending.delete(id);
          reject(new Error(`CDP command timed out: ${method}`));
        }
      }, timeoutMs);
    });
  }

  on(method, cb) {
    if (!this.handlers.has(method)) this.handlers.set(method, new Set());
    this.handlers.get(method).add(cb);
    return () => this.handlers.get(method)?.delete(cb);
  }

  once(method, timeoutMs = 15000) {
    return new Promise((resolve) => {
      const off = this.on(method, (params) => {
        clearTimeout(timer);
        off();
        resolve(params);
      });
      const timer = setTimeout(() => {
        off();
        resolve(null);
      }, timeoutMs);
    });
  }

  close() {
    this.ws?.close();
  }
}

async function createTarget() {
  const url = `${base}/json/new?${encodeURIComponent("about:blank")}`;
  let resp = await fetch(url, { method: "PUT" });
  if (!resp.ok) resp = await fetch(url);
  if (!resp.ok) throw new Error(`Unable to create CDP target: ${resp.status}`);
  return resp.json();
}

async function capturePage(cdp, label, url, waitMs = 8000) {
  const network = [];
  const removeReq = cdp.on("Network.requestWillBeSent", (params) => {
    if (!["Document", "Fetch", "XHR"].includes(params.type)) return;
    network.push({
      event: "request",
      requestId: params.requestId,
      method: params.request?.method,
      resourceType: params.type,
      url: sanitizeUrl(params.request?.url || ""),
    });
  });
  const removeRes = cdp.on("Network.responseReceived", (params) => {
    if (!["Document", "Fetch", "XHR"].includes(params.type)) return;
    network.push({
      event: "response",
      requestId: params.requestId,
      status: params.response?.status,
      mimeType: params.response?.mimeType,
      resourceType: params.type,
      url: sanitizeUrl(params.response?.url || ""),
    });
  });

  const loadPromise = cdp.once("Page.loadEventFired", 20000);
  await cdp.send("Page.navigate", { url });
  await loadPromise;
  await sleep(waitMs);

  const evalResult = await cdp.send("Runtime.evaluate", {
    returnByValue: true,
    awaitPromise: true,
    expression: `(() => {
      const text = document.body?.innerText || "";
      const links = [...document.querySelectorAll("a[href]")].slice(0, 80).map((a) => ({
        text: (a.innerText || a.getAttribute("aria-label") || "").trim().slice(0, 160),
        href: a.href
      }));
      const buttons = [...document.querySelectorAll("button,[role='button']")].slice(0, 80).map((b) => ({
        text: (b.innerText || b.getAttribute("aria-label") || "").trim().slice(0, 160),
        aria: b.getAttribute("aria-label")
      }));
      return {
        url: location.href,
        title: document.title,
        readyState: document.readyState,
        timestamp: new Date().toISOString(),
        bodyText: text,
        bodyTextLength: text.length,
        h1: [...document.querySelectorAll("h1")].map((h) => h.innerText.trim()),
        loginOrBlockerHints: {
          hasLoginText: /log in|sign up|continue with/i.test(text),
          hasCaptchaText: /captcha|recaptcha|verify you/i.test(text),
          hasUnsavedText: /unsaved changes/i.test(text),
          hasBillingPrompt: /billing|payment method/i.test(text)
        },
        links,
        buttons
      };
    })()`,
  });
  const data = evalResult.result?.value || {};
  const shot = await cdp.send("Page.captureScreenshot", { format: "png" });
  await fs.writeFile(path.join(rawDir, `${label}.json`), JSON.stringify(data, null, 2));
  await fs.writeFile(path.join(rawDir, `${label}.txt`), data.bodyText || "");
  await fs.writeFile(path.join(rawDir, `${label}_network.json`), JSON.stringify(network, null, 2));
  await fs.writeFile(path.join(rawDir, `${label}.png`), Buffer.from(shot.data, "base64"));
  removeReq();
  removeRes();
  return data;
}

async function captureCurrentPage(target, label) {
  const cdp = new CDP(target.webSocketDebuggerUrl);
  await cdp.connect();
  await cdp.send("Page.enable");
  await cdp.send("Runtime.enable");
  const evalResult = await cdp.send("Runtime.evaluate", {
    returnByValue: true,
    awaitPromise: true,
    expression: `(() => {
      const text = document.body?.innerText || "";
      return {
        url: location.href,
        title: document.title,
        readyState: document.readyState,
        timestamp: new Date().toISOString(),
        bodyText: text,
        bodyTextLength: text.length,
        h1: [...document.querySelectorAll("h1")].map((h) => h.innerText.trim()),
        loginOrBlockerHints: {
          hasLoginText: /log in|sign up|continue with/i.test(text),
          hasCaptchaText: /captcha|recaptcha|verify you/i.test(text),
          hasUnsavedText: /unsaved changes/i.test(text),
          hasBillingPrompt: /billing|payment method/i.test(text)
        }
      };
    })()`,
  });
  const data = evalResult.result?.value || {};
  const shot = await cdp.send("Page.captureScreenshot", { format: "png" }).catch(() => null);
  await fs.writeFile(path.join(rawDir, `${label}.json`), JSON.stringify(data, null, 2));
  await fs.writeFile(path.join(rawDir, `${label}.txt`), data.bodyText || "");
  if (shot?.data) {
    await fs.writeFile(path.join(rawDir, `${label}.png`), Buffer.from(shot.data, "base64"));
  }
  cdp.close();
  return data;
}

async function mainExistingOnly() {
  await fs.mkdir(rawDir, { recursive: true });
  const pages = await (await fetch(`${base}/json/list`)).json();
  const pageTargets = pages.filter((page) => page.type === "page");
  const findPage = (predicate) => pageTargets.find((page) => predicate(page.url));
  const targets = {
    events_overview: findPage((url) => url.includes(`/advertiser/${advertiserId}/conversions/events-overview/`)),
    catalog_data_sources: findPage((url) => url === `https://www.pinterest.com/business/catalogs/${catalogId}/data-sources/`),
    catalog_en_source_detail: findPage((url) => url.includes(`/business/catalogs/${catalogId}/data-sources/${enFeedProfileId}/detail`)),
    catalog_en_ingestion_issues: findPage((url) => url.includes(`/business/catalogs/${catalogId}/diagnosticsv2/`) && url.includes(`dataSourceId=${enFeedProfileId}`)),
    catalog_product_groups_en: findPage((url) => url.includes(`/business/catalogs/${catalogId}/product-groups/`) && url.includes(`feedProfileId=${enFeedProfileId}`)),
  };
  const captured = {};
  for (const [label, target] of Object.entries(targets)) {
    if (!target) {
      captured[label] = { status: "NO_EXISTING_TARGET_FOUND" };
      continue;
    }
    captured[label] = await captureCurrentPage(target, label);
  }
  const summary = {
    status: "EXISTING_PAGES_CAPTURE_COMPLETE",
    generated_at: new Date().toISOString(),
    captured: Object.fromEntries(
      Object.entries(captured).map(([label, data]) => [
        label,
        { url: data.url || "", title: data.title || "", bodyTextLength: data.bodyTextLength || 0, status: data.status || "CAPTURED" },
      ]),
    ),
    writes_made: "No external writes; refreshed local evidence files from already-open Pinterest tabs.",
  };
  await fs.writeFile(path.join(rawDir, "existing_pages_capture_summary.json"), JSON.stringify(summary, null, 2));
  console.log(JSON.stringify(summary, null, 2));
  process.exit(0);
}

async function runItemProbe(cdp) {
  let rows = [];
  try {
    rows = parseCsv(await fs.readFile(candidateCsv, "utf8"));
  } catch (error) {
    const result = { status: "BLOCKED_CANDIDATE_CSV_UNAVAILABLE", error: error.message, candidateCsv };
    await fs.writeFile(path.join(rawDir, "item_level_probe_summary.json"), JSON.stringify(result, null, 2));
    return result;
  }
  const sample = stratifiedSample(rows, Math.min(itemLimit, rows.length));
  const candidateByVariant = new Map(sample.map((row) => [row.shopify_variant_id, row]));
  const variantIds = [...candidateByVariant.keys()].filter(Boolean);

  await capturePage(
    cdp,
    "catalog_products_context",
    `https://www.pinterest.com/business/catalogs/${catalogId}/products/`,
    10000,
  );

  const expression = `(async () => {
    const merchantId = ${JSON.stringify(merchantId)};
    const catalogId = ${JSON.stringify(catalogId)};
    const enFeedProfileId = ${JSON.stringify(enFeedProfileId)};
    const variantIds = ${JSON.stringify(variantIds)};
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
    const pinIds = new Set();
    const filterResults = [];
    for (let i = 0; i < variantIds.length; i += 12) {
      const values = variantIds.slice(i, i + 12);
      const filters = JSON.stringify({
        logical_operator: 0,
        criteria: [{ key: 1, values, negated: false, filter_operator_type: 1 }]
      });
      const result = await apiResource("/v3/catalogs/" + catalogId + "/product_groups/products/", {
        filters,
        active_only: false
      });
      const data = Array.isArray(result.data) ? result.data : [];
      data.forEach((id) => pinIds.add(String(id)));
      filterResults.push({ values, ok: result.ok, status: result.status, count: data.length, message: result.message, code: result.code });
      await sleep(200);
    }
    const pinList = [...pinIds];
    const metadata = [];
    const metadataRequests = [];
    for (let i = 0; i < pinList.length; i += 10) {
      const pins = pinList.slice(i, i + 10);
      const result = await apiResource("/v3/catalogs/" + catalogId + "/item_metadata/retail/", {
        include_details: true,
        include_media: false,
        pin_ids: pins
      });
      const data = Array.isArray(result.data) ? result.data : [];
      for (const row of data) {
        metadata.push({
          pin_id: row.main_pin_id || row.pin_id || (Array.isArray(row.pin_ids) ? row.pin_ids[0] : ""),
          pin_ids: row.pin_ids || [],
          item_id: row.item_id || "",
          merchant_item_group_id: row.merchant_item_group_id || "",
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
          custom_label_1: row.custom_label_1 || "",
          custom_label_2: row.custom_label_2 || "",
          custom_label_3: row.custom_label_3 || "",
          custom_label_4: row.custom_label_4 || ""
        });
      }
      metadataRequests.push({ pins: pins.length, ok: result.ok, status: result.status, rows: data.length, message: result.message, code: result.code });
      await sleep(200);
    }
    const enRows = metadata.filter((row) =>
      row.feed_profile_id === enFeedProfileId &&
      row.locale === "en-US" &&
      row.country === "US"
    );
    return { pinIds: pinList, filterResults, metadataRequests, metadata, enRows };
  })()`;

  const probe = await cdp.send("Runtime.evaluate", {
    expression,
    awaitPromise: true,
    returnByValue: true,
  }, 180000);
  const value = probe.result?.value || {};
  const enRowsByVariant = new Map((value.enRows || []).map((row) => [String(row.item_id), row]));
  const outputRows = sample.map((candidate) => {
    const match = enRowsByVariant.get(candidate.shopify_variant_id);
    return {
      status: match?.availability === "IN_STOCK" ? "FOUND_EN_US_IN_STOCK" : match ? `FOUND_${match.availability || "UNKNOWN"}` : "NOT_FOUND_IN_SAMPLE_PROBE",
      shopify_product_id: candidate.shopify_product_id,
      shopify_variant_id: candidate.shopify_variant_id,
      custom_label_0: candidate.custom_label_0,
      custom_label_2: candidate.custom_label_2,
      custom_label_4: candidate.custom_label_4,
      candidate_title: candidate.candidate_title,
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
    byGroup[key] ||= { requested: 0, found_en_us_in_stock: 0, not_found: 0 };
    byGroup[key].requested += 1;
    if (row.status === "FOUND_EN_US_IN_STOCK") byGroup[key].found_en_us_in_stock += 1;
    if (row.status === "NOT_FOUND_IN_SAMPLE_PROBE") byGroup[key].not_found += 1;
  }
  const summary = {
    status: "READ_ONLY_SAMPLE_PROBE_COMPLETE",
    generated_at: new Date().toISOString(),
    candidate_csv: candidateCsv,
    total_candidate_rows_available: rows.length,
    sampled_candidate_rows: sample.length,
    item_limit: itemLimit,
    catalog_id: catalogId,
    merchant_id: merchantId,
    english_feed_profile_id: enFeedProfileId,
    filter_request_count: value.filterResults?.length || 0,
    pin_ids_found: value.pinIds?.length || 0,
    metadata_request_count: value.metadataRequests?.length || 0,
    metadata_rows: value.metadata?.length || 0,
    en_us_rows: value.enRows?.length || 0,
    matched_en_us_in_stock_rows: outputRows.filter((row) => row.status === "FOUND_EN_US_IN_STOCK").length,
    by_group: byGroup,
    note: "Bounded read-only sample for freshness. Full 346-row item-level proof remains required before any Pinterest draft/build.",
  };
  await fs.writeFile(path.join(rawDir, "item_level_probe_summary.json"), JSON.stringify(summary, null, 2));
  await fs.writeFile(path.join(rawDir, "item_level_probe_rows.csv"), toCsv(outputRows));
  await fs.writeFile(path.join(rawDir, "item_level_probe_api_sanitized.json"), JSON.stringify({
    filterResults: value.filterResults || [],
    metadataRequests: value.metadataRequests || [],
    enRows: value.enRows || [],
  }, null, 2));
  return summary;
}

async function main() {
  await fs.mkdir(rawDir, { recursive: true });
  const startedAt = new Date().toISOString();
  const pagesBefore = await (await fetch(`${base}/json/list`)).json();
  const target = await createTarget();
  const cdp = new CDP(target.webSocketDebuggerUrl);
  await cdp.connect();
  await cdp.send("Page.enable");
  await cdp.send("Runtime.enable");
  await cdp.send("Network.enable", { maxPostDataSize: 0 });
  await cdp.send("Emulation.setDeviceMetricsOverride", {
    width: 1440,
    height: 1000,
    deviceScaleFactor: 1,
    mobile: false,
  });

  const campaignUrl = `https://ads.pinterest.com/advertiser/${advertiserId}/reporting/campaigns/?redirectSource=NONE&campaignFilter=RUNNING%2CPAUSED%2CNOT_STARTED%2CCOMPLETED%2CADVERTISER_DISABLED&campaignFilterUpdated=false&adGroupFilter=RUNNING%2CPAUSED%2CNOT_STARTED%2CCOMPLETED%2CADVERTISER_DISABLED&adGroupFilterUpdated=false&adFilter=APPROVED%2CPENDING%2CPAUSED%2CREJECTED%2CADVERTISER_DISABLED&adFilterUpdated=false&adFormatFilter=all&adFormatFilterUpdated=false&productGroupFilter=RUNNING%2CPAUSED%2CEXCLUDED&productGroupFilterUpdated=false&objectiveTypes=[AWARENESS,CONSIDERATION,CATALOG_SALES,WEB_CONVERSION,VIDEO_COMPLETION,VIDEO_VIEW]&objectiveTypesUpdated=false&customFilters=none&deliveryFilter=true&granularity=daily&attributionWindow=7%2F7%2F7&reportingViewId=-1&limit=10&bookmark=1`;
  const targets = [
    ["campaign_spend_baseline", campaignUrl, 10000],
    ["event_quality", `https://ads.pinterest.com/advertiser/${advertiserId}/conversions/health/`, 10000],
    ["events_overview", `https://ads.pinterest.com/advertiser/${advertiserId}/conversions/events-overview/`, 10000],
    ["catalog_data_sources", `https://www.pinterest.com/business/catalogs/${catalogId}/data-sources/`, 10000],
    ["catalog_en_source_detail", `https://www.pinterest.com/business/catalogs/${catalogId}/data-sources/${enFeedProfileId}/detail/`, 10000],
    ["catalog_en_ingestion_issues", `https://www.pinterest.com/business/catalogs/${catalogId}/diagnosticsv2/?dataSourceId=${enFeedProfileId}&tab=INGESTION_ISSUES`, 10000],
    ["catalog_failed_sitemap_detail", `https://www.pinterest.com/business/catalogs/${catalogId}/data-sources/${sitemapFeedId}/detail/`, 10000],
    ["catalog_product_groups_en", `https://www.pinterest.com/business/catalogs/${catalogId}/product-groups/?feedProfileId=${enFeedProfileId}`, 10000],
  ];
  const pages = {};
  for (const [label, url, waitMs] of targets) {
    pages[label] = await capturePage(cdp, label, url, waitMs);
  }
  let itemProbe;
  try {
    itemProbe = await runItemProbe(cdp);
  } catch (error) {
    itemProbe = { status: "BLOCKED_ITEM_PROBE_ERROR", error: error.message };
    await fs.writeFile(path.join(rawDir, "item_level_probe_summary.json"), JSON.stringify(itemProbe, null, 2));
  }
  await capturePage(cdp, "handoff_event_quality_tab", `https://ads.pinterest.com/advertiser/${advertiserId}/conversions/health/`, 5000);
  const pagesAfter = await (await fetch(`${base}/json/list`)).json();
  cdp.close();

  const summary = {
    status: "READ_ONLY_CDP_CAPTURE_COMPLETE",
    started_at: startedAt,
    finished_at: new Date().toISOString(),
    cdp_port: port,
    target_id: target.id,
    advertiser_id: advertiserId,
    catalog_id: catalogId,
    merchant_id: merchantId,
    english_feed_profile_id: enFeedProfileId,
    sitemap_feed_id: sitemapFeedId,
    pages_before: pagesBefore
      .filter((page) => page.type === "page")
      .map((page) => ({ id: page.id, title: page.title, url: page.url })),
    pages_captured: Object.fromEntries(
      Object.entries(pages).map(([label, data]) => [
        label,
        {
          url: data.url,
          title: data.title,
          bodyTextLength: data.bodyTextLength,
          loginOrBlockerHints: data.loginOrBlockerHints,
        },
      ]),
    ),
    item_probe: itemProbe,
    pages_after_count: pagesAfter.filter((page) => page.type === "page").length,
    writes_made: "No Pinterest/Shopify/Merchant/Google Ads writes; only browser reads and local lane artifacts.",
  };
  await fs.writeFile(path.join(rawDir, "cdp_capture_summary.json"), JSON.stringify(summary, null, 2));
  console.log(JSON.stringify(summary, null, 2));
  await fetch(`${base}/json/close/${target.id}`).catch(() => null);
  process.exit(0);
}

if (process.env.PINTEREST_EXISTING_ONLY === "1") {
  mainExistingOnly().catch(async (error) => {
    await fs.mkdir(rawDir, { recursive: true });
    const summary = {
      status: "BLOCKED_EXISTING_PAGES_CAPTURE_ERROR",
      generated_at: new Date().toISOString(),
      cdp_port: port,
      error: error.message,
    };
    await fs.writeFile(path.join(rawDir, "existing_pages_capture_summary.json"), JSON.stringify(summary, null, 2));
    console.error(JSON.stringify(summary, null, 2));
    process.exit(1);
  });
} else {
  main().catch(async (error) => {
    await fs.mkdir(rawDir, { recursive: true });
    const summary = {
      status: "BLOCKED_CDP_CAPTURE_ERROR",
      generated_at: new Date().toISOString(),
      cdp_port: port,
      error: error.message,
    };
    await fs.writeFile(path.join(rawDir, "cdp_capture_summary.json"), JSON.stringify(summary, null, 2));
    console.error(JSON.stringify(summary, null, 2));
    process.exit(1);
  });
}
