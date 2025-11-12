Agent App Proxy – Product Finder (L1→L2)

Endpoint
- Path: /apps/agent/chat (App Proxy)
- Method: POST
- AuthN: Shopify App Proxy signature (HMAC) – verify on server
- Content-Type: application/json

Request
{
  "session": "optional-session-id",
  "message": "free text from user",
  "context": { "currency": "USD" }
}

Response
{
  "session": "server-assigned-session-id",
  "reply": "assistant text to display",
  "currency": "USD",
  "actions": [
    {
      "type": "recommendations",
      "items": [
        { "productId": "gid://shopify/Product/...", "title": "...", "image": "https://...", "variantId": "gid://shopify/ProductVariant/...", "price": 7900 }
      ]
    }
  ],
  "clarify": null
}

Server responsibilities
- Verify HMAC of App Proxy request.
- Maintain short-term session memory keyed by session id.
- Orchestrate LM (system prompt: brand-safe, factual, use tools only) with function-calling tools:
  - search_products(query, filters) -> Storefront GraphQL
  - get_product_variants(productId) -> Storefront GraphQL
  - get_policy(kind) -> RAG over policy documents
- Ground responses; never invent inventory/prices.
- Return compact JSON per the schema above.

Notes
- Cart actions remain client-side (theme calls /cart/add.js).
- Add rate limiting and logging; redact PII.

