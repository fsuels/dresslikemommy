/*
1688 browser-assisted candidate collector.

How to use:
1. Log into 1688 in your browser.
2. Search a category or open a supplier/product results page.
3. Open DevTools Console.
4. Paste this whole file and press Enter.
5. Save the downloaded JSON or paste the copied JSON into:
   ops/sourcing/<date>-<search>/candidates.json

This reads only the visible DOM in your logged-in browser tab. It does not call
private APIs, bypass login, or write anything back to 1688.
*/

(() => {
  const absolutize = (url) => {
    try {
      return new URL(url, location.href).href;
    } catch {
      return "";
    }
  };

  const text = (node) => (node?.innerText || node?.textContent || "").replace(/\s+/g, " ").trim();
  const attr = (node, name) => node?.getAttribute?.(name) || "";
  const uniq = (items) => [...new Set(items.filter(Boolean))];

  const usefulParent = (anchor) => {
    let node = anchor;
    for (let i = 0; i < 7 && node?.parentElement; i += 1) {
      const body = text(node);
      const hasImage = Boolean(node.querySelector("img"));
      const hasPrice = /[¥￥]\s*\d|起批|成交|回头率|发货|实力商家|官方物流/.test(body);
      if (hasImage && body.length > 20 && (hasPrice || body.length > 80)) return node;
      node = node.parentElement;
    }
    return anchor.closest("div,li,article") || anchor;
  };

  const parsePrice = (body) => {
    const match = body.match(/[¥￥]\s*([0-9]+(?:\.[0-9]+)?)/);
    return match ? match[1] : "";
  };

  const parseMoq = (body) => {
    const match = body.match(/(?:起批|起订|MOQ|moq)[^\d]{0,8}(\d+)/i);
    return match ? match[1] : "";
  };

  const parsePercent = (body, label) => {
    const escaped = label.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    const match = body.match(new RegExp(`${escaped}[^0-9]{0,10}([0-9]+(?:\\.[0-9]+)?)\\s*%`, "i"));
    return match ? `${match[1]}%` : "";
  };

  const parseYears = (body) => {
    const match = body.match(/(\d+(?:\.\d+)?)\s*年(?:店|诚信通|经营|会员)?/);
    return match ? match[1] : "";
  };

  const parseSales = (body) => {
    const match = body.match(/(?:成交|付款|销量|已售|售出|sold|orders)[^\d]{0,8}(\d+(?:\.\d+)?)(万)?/i);
    if (!match) return "";
    const value = Number(match[1]) * (match[2] ? 10000 : 1);
    return String(Math.round(value));
  };

  const detectTerms = (body, terms) => terms.filter((term) => body.toLowerCase().includes(term.toLowerCase()));

  const badgeTerms = [
    "实力商家",
    "超级工厂",
    "深度验厂",
    "深度认证",
    "真实工厂",
    "买家保障",
    "品质保障",
    "官方物流",
    "48小时发货",
    "24小时发货",
    "现货",
    "一件代发",
    "15天包换",
    "包换",
  ];

  const riskTerms = [
    "Disney",
    "Mickey",
    "Minnie",
    "Nike",
    "Adidas",
    "Barbie",
    "Hello Kitty",
    "Snoopy",
    "Pokemon",
    "Marvel",
    "迪士尼",
    "米奇",
    "米妮",
    "耐克",
    "阿迪",
    "芭比",
    "凯蒂猫",
    "史努比",
    "宝可梦",
    "漫威",
    "卡通",
    "联名",
    "品牌",
    "logo",
  ];

  const anchors = Array.from(document.querySelectorAll('a[href*="/offer/"], a[href*="detail.1688.com/offer/"]'));
  const seen = new Set();
  const candidates = [];

  for (const anchor of anchors) {
    const productUrl = absolutize(anchor.href);
    const offerId = productUrl.match(/offer\/(\d+)\.html/)?.[1] || productUrl;
    if (!productUrl || seen.has(offerId)) continue;
    seen.add(offerId);

    const card = usefulParent(anchor);
    const body = text(card);
    const image = card.querySelector("img") || anchor.querySelector("img");
    const imageUrl = absolutize(
      attr(image, "src") ||
        attr(image, "data-src") ||
        attr(image, "data-original") ||
        attr(image, "data-lazy-src") ||
        ""
    );
    const title =
      attr(anchor, "title") ||
      attr(image, "alt") ||
      text(anchor) ||
      body.split(/[¥￥]/)[0].slice(0, 120);

    candidates.push({
      product_url: productUrl,
      image_url: imageUrl,
      title,
      vendor_name: "",
      vendor_url: "",
      vendor_location: "",
      price_cny: parsePrice(body),
      moq: parseMoq(body),
      monthly_sales: parseSales(body),
      repurchase_rate_pct: parsePercent(body, "回头率"),
      rating: "",
      years_on_1688: parseYears(body),
      badges: uniq(detectTerms(body, badgeTerms)).join(" | "),
      service_flags: uniq(detectTerms(body, ["官方物流", "48小时发货", "24小时发货", "现货", "一件代发", "15天包换", "包换"])).join(" | "),
      dropship_supported: body.includes("一件代发") ? "yes" : "",
      size_chart: "",
      category_match: "",
      style_fit: "",
      image_quality: imageUrl ? "3" : "",
      ip_risk_flags: uniq(detectTerms(`${title} ${body}`, riskTerms)).join(" | "),
      raw_card_text: body.slice(0, 1200),
      notes: `Collected from ${location.href}`,
    });
  }

  const payload = {
    collected_at: new Date().toISOString(),
    page_url: location.href,
    page_title: document.title,
    candidates,
  };

  const json = JSON.stringify(payload, null, 2);
  const blob = new Blob([json], { type: "application/json" });
  const downloadUrl = URL.createObjectURL(blob);
  const panel = document.createElement("div");
  panel.style.cssText = [
    "position:fixed",
    "z-index:2147483647",
    "right:16px",
    "bottom:16px",
    "width:min(520px,calc(100vw - 32px))",
    "max-height:70vh",
    "background:#fffdf8",
    "color:#1f2523",
    "border:1px solid #ded7ca",
    "border-radius:8px",
    "box-shadow:0 18px 45px rgba(42,36,28,.22)",
    "font:14px/1.45 system-ui,-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif",
    "overflow:auto",
    "padding:16px",
  ].join(";");
  panel.innerHTML = `
    <div style="display:flex;gap:12px;align-items:start;justify-content:space-between">
      <div>
        <strong style="font-size:18px">1688 candidates collected</strong>
        <div style="color:#68716b">${candidates.length} product links found from the visible page.</div>
      </div>
      <button type="button" data-close style="border:1px solid #ded7ca;background:white;border-radius:8px;min-height:34px;padding:0 10px;cursor:pointer">Close</button>
    </div>
    <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:14px">
      <a download="1688-candidates.json" href="${downloadUrl}" style="display:inline-flex;align-items:center;min-height:38px;padding:0 12px;border-radius:8px;background:#1f2523;color:white;text-decoration:none;font-weight:700">Download JSON</a>
      <button type="button" data-copy style="border:1px solid #ded7ca;background:white;border-radius:8px;min-height:38px;padding:0 12px;cursor:pointer;font-weight:700">Copy JSON</button>
    </div>
    <textarea readonly style="margin-top:12px;width:100%;height:220px;border:1px solid #ded7ca;border-radius:8px;padding:10px;font:12px/1.35 ui-monospace,SFMono-Regular,Menlo,monospace">${json.replaceAll("&", "&amp;").replaceAll("<", "&lt;")}</textarea>
  `;
  document.body.appendChild(panel);
  panel.querySelector("[data-close]").addEventListener("click", () => panel.remove());
  panel.querySelector("[data-copy]").addEventListener("click", async (event) => {
    await navigator.clipboard.writeText(json);
    event.currentTarget.textContent = "Copied";
    setTimeout(() => {
      event.currentTarget.textContent = "Copy JSON";
    }, 1200);
  });

  console.log("1688 sourcing candidates", payload);
})();
