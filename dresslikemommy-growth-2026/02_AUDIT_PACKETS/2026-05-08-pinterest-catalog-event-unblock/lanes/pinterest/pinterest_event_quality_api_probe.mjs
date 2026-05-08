#!/usr/bin/env node
import fs from "node:fs/promises";
import path from "node:path";

const laneDir = path.dirname(new URL(import.meta.url).pathname);
const rawDir = path.join(laneDir, "raw");
const port = process.env.CDP_PORT || "9333";
const base = `http://127.0.0.1:${port}`;
const advertiserId = "549756244483";
const eventQualityUrl = `https://ads.pinterest.com/advertiser/${advertiserId}/conversions/health/`;

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

function sanitizeUrl(value) {
  try {
    const u = new URL(value);
    const keys = [...u.searchParams.keys()].sort();
    return `${u.origin}${u.pathname}${keys.length ? `?${keys.join("&")}` : ""}`;
  } catch {
    return value;
  }
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
      this.ws.onerror = () => {
        clearTimeout(timeout);
        reject(new Error("CDP websocket error"));
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
        if (!this.pending.has(id)) return;
        this.pending.delete(id);
        reject(new Error(`CDP command timed out: ${method}`));
      }, timeoutMs);
    });
  }

  on(method, cb) {
    if (!this.handlers.has(method)) this.handlers.set(method, new Set());
    this.handlers.get(method).add(cb);
    return () => this.handlers.get(method)?.delete(cb);
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

async function main() {
  await fs.mkdir(rawDir, { recursive: true });
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

  const responses = [];
  cdp.on("Network.responseReceived", (params) => {
    const url = params.response?.url || "";
    if (!url.includes("/conversions/")) return;
    if (!["XHR", "Fetch"].includes(params.type)) return;
    responses.push({
      requestId: params.requestId,
      status: params.response?.status,
      mimeType: params.response?.mimeType,
      url,
      sanitizedUrl: sanitizeUrl(url),
      timestamp: new Date().toISOString(),
    });
  });

  await cdp.send("Page.navigate", { url: eventQualityUrl });
  await sleep(25000);

  const dom = await cdp.send("Runtime.evaluate", {
    awaitPromise: true,
    returnByValue: true,
    expression: `(() => ({
      url: location.href,
      title: document.title,
      timestamp: new Date().toISOString(),
      bodyText: document.body?.innerText || "",
      bodyTextLength: (document.body?.innerText || "").length,
      blockerHints: {
        hasLoginText: /log in|sign up|continue with/i.test(document.body?.innerText || ""),
        hasCaptchaText: /captcha|recaptcha|verify you/i.test(document.body?.innerText || ""),
        hasUnsavedText: /unsaved changes/i.test(document.body?.innerText || ""),
        hasBillingPrompt: /billing|payment method/i.test(document.body?.innerText || "")
      }
    }))`,
  });
  const screenshot = await cdp.send("Page.captureScreenshot", { format: "png" }).catch(() => null);

  const bodies = [];
  for (const response of responses) {
    let body = "";
    let base64Encoded = false;
    let parseError = "";
    try {
      const result = await cdp.send("Network.getResponseBody", { requestId: response.requestId }, 5000);
      body = result.body || "";
      base64Encoded = Boolean(result.base64Encoded);
    } catch (error) {
      parseError = error.message;
    }
    let json = null;
    if (body && !base64Encoded) {
      try {
        json = JSON.parse(body);
      } catch {
        json = null;
      }
    }
    bodies.push({
      status: response.status,
      mimeType: response.mimeType,
      sanitizedUrl: response.sanitizedUrl,
      bodyLength: body.length,
      base64Encoded,
      parseError,
      json,
    });
  }

  const data = {
    status: "READ_ONLY_EVENT_QUALITY_API_PROBE_COMPLETE",
    generated_at: new Date().toISOString(),
    advertiser_id: advertiserId,
    target_id: target.id,
    page: dom.result?.value || {},
    responses: bodies,
    writes_made: "No Pinterest writes; captured only Event Quality page text/screenshot and conversions API response bodies; no headers or cookies stored.",
  };
  await fs.writeFile(path.join(rawDir, "event_quality_api_probe.json"), JSON.stringify(data, null, 2));
  await fs.writeFile(path.join(rawDir, "event_quality_api_probe.txt"), data.page.bodyText || "");
  if (screenshot?.data) {
    await fs.writeFile(path.join(rawDir, "event_quality_api_probe.png"), Buffer.from(screenshot.data, "base64"));
  }

  cdp.close();
  await fetch(`${base}/json/close/${target.id}`).catch(() => null);
  console.log(JSON.stringify({
    status: data.status,
    generated_at: data.generated_at,
    page_body_text_length: data.page.bodyTextLength || 0,
    response_count: data.responses.length,
    response_summaries: data.responses.map((r) => ({
      status: r.status,
      bodyLength: r.bodyLength,
      sanitizedUrl: r.sanitizedUrl,
      parsed: Boolean(r.json),
    })),
    writes_made: data.writes_made,
  }, null, 2));
}

main().catch(async (error) => {
  await fs.mkdir(rawDir, { recursive: true });
  const data = {
    status: "BLOCKED_EVENT_QUALITY_API_PROBE_ERROR",
    generated_at: new Date().toISOString(),
    error: error.message,
  };
  await fs.writeFile(path.join(rawDir, "event_quality_api_probe.json"), JSON.stringify(data, null, 2));
  console.error(JSON.stringify(data, null, 2));
  process.exit(1);
});
