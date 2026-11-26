# DE / FR / ES / UK / AU funnel, 2026-11-26 — BLOCKED (read-only)

Status: BLOCKED. The live shopper walk could not run. At 19:26-19:28 UTC every request to www.dresslikemommy.com (home, /de, /robots.txt, product .js, and the myshopify domain which redirects there) returned HTTP 429 with `cf-mitigated: challenge` (Cloudflare managed challenge) for both a mobile and a desktop UA, with and without cookie jars. The earlier Italy and CZ/CA audits ran from the same method earlier today; this IP was challenged afterwards (probably request volume). Clearing the challenge is bot-detection bypass and the brief forbids a browser, so nothing was bypassed. No finding below is invented.

Also not possible: Admin GraphQL `@inContext` is not defined for this token/endpoint, so per-market prices (DE/FR/ES/GB/AU) cannot be read through Admin either (same limit as the earlier audits: no read_markets).

## Findings
None verified for these five markets. Zero live evidence collected.

## Already known (from Italy and CZ/CA audits, expected to repeat in DE/FR/ES; UK/AU unchecked)
- No compare-at / sale badge in EUR markets; ~15% price uplift over FX.
- Unclear VAT/duties ("taxes calculated at checkout", no tax line).
- Phone number required at checkout.
- Christmas order-by date is global (US-only is the fix).
- Mixed symbol+code price format ("€53,95 EUR"), dot decimals in size chart, all-dash columns for sweaters.

## OWNER / next step
- Re-run this walk after the Cloudflare challenge on www.dresslikemommy.com clears for the agent IP (or from an IP that is not challenged); script method = `italy-funnel-2026-11-26.md`. Check Cloudflare Security > Events for the rule that fired (may also be hurting real shoppers or Googlebot: worth one look).
- UK/AU specific checks still to do: GBP/AUD formatting, "fall"/"ZIP" wording, AU summer seasonality on home, hreflang/canonical, JSON-LD currency.
