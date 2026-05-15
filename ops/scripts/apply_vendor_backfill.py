#!/usr/bin/env python3.13
"""Backfill Shopify product vendor to 'Dress Like Mommy' for every active product
where vendor != 'Dress Like Mommy'.

Idempotent: products already at the target value are skipped (Shopify returns
no-op with no userErrors).

Credentials are read from the local operator-only credential files used by
other ops/scripts/* automation:
    SHOPIFY_STORE_DOMAIN=www.dresslikemommy.com  (or "<shop>.myshopify.com")
    SHOPIFY_ADMIN_ACCESS_TOKEN=***
    SHOPIFY_ADMIN_API_VERSION=2024-10  (optional, default 2024-10)

Usage:
    python3.13 ops/scripts/apply_vendor_backfill.py             # full live run
    python3.13 ops/scripts/apply_vendor_backfill.py --dry-run   # list only
    python3.13 ops/scripts/apply_vendor_backfill.py --limit 5   # smoke test

Outputs:
    dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-vendor-brand-auto-fix-execution/
        vendor_backfill_execution_log.csv
        vendor_backfill_summary.json
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

CREDS_DIR = pathlib.Path.home() / ".config" / "dresslikemommy"
CREDS_PATH = CREDS_DIR / "shopify-admin.env"
TOKEN_JSON_PATH = CREDS_DIR / "admin-api-token.json"
TOKEN_ENV_KEYS = ("SHOPIFY_ADMIN_ACCESS_TOKEN", "SHOPIFY_ADMIN_API_TOKEN")
TARGET_VENDOR = "Dress Like Mommy"
DEFAULT_API_VERSION = "2024-10"

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
EVIDENCE_DIR = (
    REPO_ROOT
    / "dresslikemommy-growth-2026"
    / "02_AUDIT_PACKETS"
    / "2026-05-15-vendor-brand-auto-fix-execution"
)

SEARCH_QUERY = 'status:active AND NOT vendor:"Dress Like Mommy"'

PAGE_QUERY = """
query VendorAudit($after: String) {
  products(first: 50, after: $after, query: "status:active AND NOT vendor:\\"Dress Like Mommy\\"") {
    pageInfo { hasNextPage endCursor }
    edges { node { id vendor } }
  }
}
""".strip()

MUTATION = """
mutation SetVendor($id: ID!) {
  productUpdate(product: { id: $id, vendor: "Dress Like Mommy" }) {
    product { id vendor }
    userErrors { field message }
  }
}
""".strip()


def load_credentials() -> tuple[str, str, str]:
    env: dict[str, str] = {}
    if CREDS_PATH.exists():
        for raw in CREDS_PATH.read_text().splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            env[key.strip()] = value.strip().strip('"').strip("'")

    token_json: dict[str, str] = {}
    if TOKEN_JSON_PATH.exists():
        try:
            token_json = json.loads(TOKEN_JSON_PATH.read_text())
        except json.JSONDecodeError as exc:
            sys.exit(f"Could not parse {TOKEN_JSON_PATH}: {exc}")

    if not env and not token_json:
        sys.exit(
            "Credentials not loaded in this shell: expected "
            f"{CREDS_PATH} or {TOKEN_JSON_PATH}."
        )

    domain = env.get("SHOPIFY_STORE_DOMAIN") or token_json.get("shop_domain") or token_json.get(
        "store_domain"
    )
    token = next((env.get(key) for key in TOKEN_ENV_KEYS if env.get(key)), None) or token_json.get(
        "access_token"
    )
    version = env.get("SHOPIFY_ADMIN_API_VERSION", DEFAULT_API_VERSION)
    if not domain or not token:
        sys.exit(
            "Credentials file present but SHOPIFY_STORE_DOMAIN and "
            "SHOPIFY_ADMIN_ACCESS_TOKEN are required."
        )
    if not domain.endswith("myshopify.com"):
        # The Shopify Admin API requires the myshopify.com host, not the custom domain.
        # We allow operators to set either; if a custom domain is set we try to derive
        # the canonical shop, but most repos store the myshopify host directly.
        sys.exit(
            f"SHOPIFY_STORE_DOMAIN must be the *.myshopify.com host (got {domain}). "
            "The www.dresslikemommy.com domain is not valid for Admin API calls."
        )
    return domain, token, version


def graphql(domain: str, token: str, version: str, query: str, variables: dict) -> dict:
    url = f"https://{domain}/admin/api/{version}/graphql.json"
    body = json.dumps({"query": query, "variables": variables}).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": token,
            "Accept": "application/json",
        },
        method="POST",
    )
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
            if "errors" in payload:
                # transient throttle?
                if any("throttled" in str(e).lower() for e in payload["errors"]) and attempt < 4:
                    time.sleep(2 * (attempt + 1))
                    continue
                raise RuntimeError(f"GraphQL errors: {payload['errors']}")
            return payload
        except urllib.error.HTTPError as exc:
            if exc.code in (429, 502, 503, 504) and attempt < 4:
                time.sleep(2 * (attempt + 1))
                continue
            raise
    raise RuntimeError("GraphQL request failed after retries")


def collect_targets(domain: str, token: str, version: str) -> list[str]:
    targets: list[str] = []
    after: str | None = None
    while True:
        data = graphql(domain, token, version, PAGE_QUERY, {"after": after})["data"]["products"]
        for edge in data["edges"]:
            targets.append(edge["node"]["id"])
        if not data["pageInfo"]["hasNextPage"]:
            break
        after = data["pageInfo"]["endCursor"]
    return targets


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Only list, do not mutate.")
    parser.add_argument("--limit", type=int, default=0, help="Cap the number of mutations.")
    args = parser.parse_args()

    domain, token, version = load_credentials()
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    log_path = EVIDENCE_DIR / "vendor_backfill_execution_log.csv"
    summary_path = EVIDENCE_DIR / "vendor_backfill_summary.json"

    print(f"[+] Collecting active products with vendor != {TARGET_VENDOR!r} ...")
    targets = collect_targets(domain, token, version)
    print(f"[+] Found {len(targets)} target products.")

    if args.limit:
        targets = targets[: args.limit]
        print(f"[!] --limit applied: will only process first {len(targets)}.")

    if args.dry_run:
        for gid in targets:
            print(f"DRY {gid}")
        return

    started = datetime.now(timezone.utc).isoformat()
    ok = 0
    failed: list[dict] = []
    with log_path.open("w", encoding="utf-8") as fh:
        fh.write("timestamp,product_gid,result,detail\n")
        for gid in targets:
            try:
                resp = graphql(domain, token, version, MUTATION, {"id": gid})
                result = resp["data"]["productUpdate"]
                errs = result.get("userErrors") or []
                if errs:
                    failed.append({"id": gid, "errors": errs})
                    fh.write(
                        f"{datetime.now(timezone.utc).isoformat()},{gid},ERROR,"
                        f"\"{json.dumps(errs).replace(chr(34), chr(39))}\"\n"
                    )
                    print(f"[ERR] {gid}: {errs}")
                else:
                    ok += 1
                    fh.write(
                        f"{datetime.now(timezone.utc).isoformat()},{gid},OK,vendor=Dress Like Mommy\n"
                    )
                    if ok % 25 == 0:
                        print(f"  ... {ok}/{len(targets)} done")
            except Exception as exc:  # noqa: BLE001
                failed.append({"id": gid, "errors": str(exc)})
                fh.write(
                    f"{datetime.now(timezone.utc).isoformat()},{gid},EXCEPTION,"
                    f"\"{str(exc).replace(chr(34), chr(39))}\"\n"
                )
                print(f"[EXC] {gid}: {exc}")

    finished = datetime.now(timezone.utc).isoformat()
    summary = {
        "started_utc": started,
        "finished_utc": finished,
        "target_vendor": TARGET_VENDOR,
        "search_query": SEARCH_QUERY,
        "candidates_found": len(targets),
        "succeeded": ok,
        "failed": len(failed),
        "failures": failed,
    }
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"\n[+] Done. ok={ok} failed={len(failed)}")
    print(f"    Log:     {log_path}")
    print(f"    Summary: {summary_path}")
    if failed:
        sys.exit(2)


if __name__ == "__main__":
    main()
