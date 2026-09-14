# Merchant API access check — 11 September 2026

**BLOCKED_EXISTING_CREDENTIAL_UNAVAILABLE.** The existing local gcloud access-token command exited with code 1 without providing a token, during **15:09:10–15:09:12 UTC**. No Merchant API request ran. Consequently, neither account access nor data-source access is verified, and no Merchant HTTP 401/403 was observed. The underlying credential failure was not diagnosed; raw diagnostic output was suppressed to avoid exposing unrelated identity or credential information.

The intended read-only targets were `GET https://merchantapi.googleapis.com/accounts/v1/accounts/513542500`, followed only after verified account identity by `GET https://merchantapi.googleapis.com/datasources/v1/accounts/513542500/dataSources?pageSize=1000`. These are the current documented [account GET](https://developers.google.com/merchant/api/reference/rest/accounts_v1/accounts/get) and [data-source list](https://developers.google.com/merchant/api/reference/rest/datasources_v1/accounts.dataSources/list) endpoints; both require the `https://www.googleapis.com/auth/content` OAuth scope. Documentation retrieved 11 September 2026.

No token was printed or stored. The legacy exporter was not executed. No other accounts or projects were enumerated; no login, scope change, credential regeneration, API mutation, or native browser operation occurred. The probe does not establish write permission.

**Next action:** continue the already authorized native Merchant submission and readback, because this bounded credential route is unavailable. No authentication recovery was attempted.

Machine evidence: [merchant-api-access-readback.json](./merchant-api-access-readback.json).
