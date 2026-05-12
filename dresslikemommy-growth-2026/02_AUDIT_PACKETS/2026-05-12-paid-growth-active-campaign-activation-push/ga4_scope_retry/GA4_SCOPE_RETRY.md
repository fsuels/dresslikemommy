# GA4 Scope Retry

Generated: 2026-05-12

Target:
- GA4 property `330266838`
- Goal: determine whether the current shell can produce a read-only GA4 Data/Admin API token with sufficient Analytics scope.

Guardrails:
- No GA4 settings changes.
- No export/report creation.
- No checkout, payment, order, refund, cancelation, Ads/Merchant/Pinterest/Shopify write, budget/bid/status change, or conversion-goal change.

Commands/results:

```text
gcloud auth list --format='value(account,status)'
=> testhqfinds@gmail.com *

gcloud config get-value account
=> testhqfinds@gmail.com

gcloud auth print-access-token --help | rg -n "scopes|access-token|--scopes"
=> no --scopes option available on this installed command surface

gcloud auth application-default print-access-token
=> ERROR: default credentials were not found; metadata server unavailable

curl https://analyticsdata.googleapis.com/v1beta/properties/330266838/metadata with bearer token from gcloud auth print-access-token
=> HTTP 403 ACCESS_TOKEN_SCOPE_INSUFFICIENT
```

Conclusion:
- The current authenticated account exists, but the available user token still lacks GA4 Data API scopes.
- Application Default Credentials are not configured.
- The measurement gate cannot close through the current CLI token path.

Next unblock:
- Refresh/authenticate read-only GA4 Data/Admin API scopes for property `330266838`, or approve the controlled non-US measurement test purchase procedure in `APPROVAL_LADDER.md`.
