#!/usr/bin/env python3
"""Read-only exact-account Google Ads probe. No mutation endpoint or credential output."""
import importlib.util
import json
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("cfgcheck", ROOT / "ops/scripts/check_google_ads_api_config.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
cfg = mod.parse_simple_yaml(mod.SECURE_CONFIG_PATH)

def call(url, data, headers):
    try:
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        raw = error.read().decode("utf-8", "replace")
        for value in cfg.values():
            if value:
                raw = raw.replace(value, "[REDACTED]")
        report = {"as_of": datetime.now(timezone.utc).isoformat(), "phase": "oauth" if "oauth2" in url else "ads_read", "http_status": error.code, "error": raw[:2500]}
        (OUT / "google_api_access_readback.json").write_text(json.dumps(report, indent=2) + "\n")
        print(json.dumps(report))
        raise SystemExit(2)
    except Exception as error:
        print(json.dumps({"phase": "transport", "error_type": type(error).__name__, "reason": str(getattr(error, "reason", ""))[:250]}))
        raise SystemExit(3)

token = call("https://oauth2.googleapis.com/token", urllib.parse.urlencode({"grant_type": "refresh_token", "client_id": cfg["client_id"], "client_secret": cfg["client_secret"], "refresh_token": cfg["refresh_token"]}).encode(), {"Content-Type": "application/x-www-form-urlencoded"})
headers = {"Authorization": "Bearer " + token["access_token"], "developer-token": cfg["developer_token"], "login-customer-id": cfg["login_customer_id"], "Content-Type": "application/json"}
query = "SELECT customer.id, customer.descriptive_name, customer.currency_code, customer.time_zone FROM customer LIMIT 1"
result = call("https://googleads.googleapis.com/v25/customers/3990976848/googleAds:search", json.dumps({"query": query}).encode(), headers)
report = {"as_of": datetime.now(timezone.utc).isoformat(), "customer_id": "3990976848", "method": "googleAds:search", "query": query, "result": result}
(OUT / "google_api_access_readback.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
