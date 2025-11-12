import express from 'express';
import fetch from 'node-fetch';
import dotenv from 'dotenv';
import crypto from 'crypto';

dotenv.config();

const app = express();
app.use(express.json());

const PORT = process.env.PORT || 3000;
const STORE_DOMAIN = process.env.SHOPIFY_STORE_DOMAIN; // e.g. dresslikemommy.myshopify.com
const SF_TOKEN = process.env.SHOPIFY_STOREFRONT_TOKEN; // Storefront API public token
const APP_PROXY_SECRET = process.env.SHOPIFY_APP_PROXY_SECRET; // TODO: verify signature

function isDev() { return process.env.NODE_ENV !== 'production'; }

function respondError(res, code, msg) { return res.status(code).json({ error: msg }); }

// TODO: Implement App Proxy signature verification
function verifyAppProxy(req) {
  if (isDev()) return true;
  try {
    const url = new URL(req.originalUrl, `https://${STORE_DOMAIN}`);
    const sig = url.searchParams.get('signature');
    if (!sig) return false;
    url.searchParams.delete('signature');
    // Build canonical query string sorted by key
    const pairs = [];
    url.searchParams.forEach((v,k)=>{ pairs.push([k,v]); });
    pairs.sort((a,b)=> a[0].localeCompare(b[0]));
    const qs = pairs.map(([k,v])=> `${k}=${v}`).join('&');
    const expected = crypto.createHmac('sha256', APP_PROXY_SECRET).update(qs).digest('hex');
    return crypto.timingSafeEqual(Buffer.from(sig,'utf8'), Buffer.from(expected,'utf8'));
  } catch(e) {
    return false;
  }
}

async function storefront(query, variables={}) {
  const url = `https://${STORE_DOMAIN}/api/2024-07/graphql.json`;
  const r = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-Shopify-Storefront-Access-Token': SF_TOKEN,
    },
    body: JSON.stringify({ query, variables })
  });
  if (!r.ok) throw new Error(`Storefront error: ${r.status}`);
  const j = await r.json();
  if (j.errors) throw new Error(`Storefront errors: ${JSON.stringify(j.errors)}`);
  return j.data;
}

async function searchProducts(q, limit=4) {
  const query = /* GraphQL */ `
    query ProductSearch($q: String!, $n: Int!) {
      products(first: $n, query: $q) {
        edges { node { id title handle featuredImage { url altText } variants(first:1) { edges { node { id price { amount currencyCode } } } } } }
      }
    }
  `;
  const data = await storefront(query, { q, n: limit });
  const items = (data.products.edges || []).map(({ node }) => {
    const v = (node.variants.edges[0]?.node) || null;
    return {
      productId: node.id,
      title: node.title,
      image: node.featuredImage?.url || null,
      variantId: v?.id || null,
      price: v ? Math.round(parseFloat(v.price.amount) * 100) : null,
      currency: v?.price?.currencyCode || 'USD',
      handle: node.handle
    };
  });
  return items;
}

function extractBudgetCents(message){
  const m = message.match(/(?:under|below|<=|less than|budget)\s*\$?(\d+)(?:\.(\d{1,2}))?/i);
  if(!m) return null;
  const dollars = parseInt(m[1]||'0',10);
  const cents = m[2]? parseInt((m[2]+'00').slice(0,2),10):0;
  return dollars*100 + cents;
}

function planQuery(message){
  // Very lightweight L2-style planning: extract key terms, avoid stopwords
  const stop = new Set(['the','a','an','and','for','with','of','to','me','my','our','matching','set','sets','please']);
  const tokens = (message.toLowerCase().match(/[a-z0-9]+/g) || []).filter(t=>!stop.has(t));
  const budget = extractBudgetCents(message);
  let terms = tokens.join(' ');
  return { terms, budget };
}

app.post(['/apps/agent/chat','/agent/chat'], async (req, res) => {
  try {
    if (!verifyAppProxy(req)) return respondError(res, 401, 'unauthorized');
    const { message, session, context } = req.body || {};
    if (!message || typeof message !== 'string') return respondError(res, 400, 'message required');

    // L2-lite: plan terms + budget, then search and filter
    const plan = planQuery(message);
    let items = await searchProducts(plan.terms || message, 6);
    if (plan.budget != null) {
      items = items.filter(it=> typeof it.price === 'number' && it.price <= plan.budget);
    }
    items = items.slice(0,4);
    const currency = items[0]?.currency || context?.currency || 'USD';
    let reply;
    let clarify = null;
    if (items.length) {
      reply = `Here are some options for "${message}":`;
      if (plan.budget != null) {
        reply += ` (within ${(plan.budget/100).toFixed(2)} ${currency})`;
      }
    } else {
      reply = `I couldn't find matches for "${message}".`;
      clarify = 'Do you have a budget, color, size, or specific category (e.g., dresses, swimsuits)?';
    }

    const payload = {
      session: session || `sess_${Date.now()}`,
      reply,
      currency,
      actions: [ { type: 'recommendations', items } ],
      clarify
    };
    res.json(payload);
  } catch (e) {
    console.error(e);
    respondError(res, 500, 'server_error');
  }
});

app.get('/health', (req,res)=>res.json({ok:true}));

app.listen(PORT, ()=>{
  console.log(`Agent backend listening on :${PORT}`);
});
