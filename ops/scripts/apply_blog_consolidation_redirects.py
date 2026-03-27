#!/usr/bin/env python3
"""Apply Shopify blog consolidation redirects from a generated CSV.

Expected input columns:
- Redirect from
- Redirect to

The script will:
- look up any existing redirect for the source path
- leave it unchanged if the target already matches
- replace conflicting redirects
- create missing redirects

Dry-run is the default. Pass --execute to apply live changes.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path
from typing import Dict, Iterable, List

from shopify_admin_config import (
    DEFAULT_ENV_PATH,
    DEFAULT_STORE_DOMAIN,
    DEFAULT_TOKEN_PATH,
    load_access_token,
    resolve_store_domain,
)


DEFAULT_API_VERSION = os.environ.get("SHOPIFY_API_VERSION", "2026-01")
REQUIRED_COLUMNS = {"Redirect from", "Redirect to"}

URL_REDIRECTS_QUERY = """
query UrlRedirects($query: String!) {
  urlRedirects(first: 10, query: $query) {
    nodes {
      id
      path
      target
    }
  }
}
"""

URL_REDIRECT_CREATE_MUTATION = """
mutation UrlRedirectCreate($urlRedirect: UrlRedirectInput!) {
  urlRedirectCreate(urlRedirect: $urlRedirect) {
    urlRedirect {
      id
      path
      target
    }
    userErrors {
      field
      message
    }
  }
}
"""

URL_REDIRECT_DELETE_MUTATION = """
mutation UrlRedirectDelete($id: ID!) {
  urlRedirectDelete(id: $id) {
    deletedUrlRedirectId
    userErrors {
      field
      message
    }
  }
}
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="CSV containing Redirect from / Redirect to columns")
    parser.add_argument("--api-version", default=DEFAULT_API_VERSION)
    parser.add_argument("--store-domain", default=DEFAULT_STORE_DOMAIN)
    parser.add_argument("--access-token", default=os.environ.get("SHOPIFY_ADMIN_ACCESS_TOKEN", ""))
    parser.add_argument("--token-file", default=str(DEFAULT_TOKEN_PATH))
    parser.add_argument("--execute", action="store_true", help="Apply live redirect creates/deletes")
    return parser.parse_args()


def graphql_request(store_domain: str, access_token: str, api_version: str, query: str, variables: Dict) -> Dict:
    endpoint = f"https://{store_domain}/admin/api/{api_version}/graphql.json"
    payload = json.dumps({"query": query, "variables": variables}).encode("utf-8")
    request = urllib.request.Request(
        endpoint,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": access_token,
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            body = response.read().decode("utf-8")
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Shopify GraphQL HTTP {error.code}: {body}") from error

    decoded = json.loads(body)
    if decoded.get("errors"):
        raise RuntimeError(f"Shopify GraphQL errors: {decoded['errors']}")
    return decoded["data"]


def format_user_errors(payload: Dict) -> str:
    messages: List[str] = []
    for error in payload.get("userErrors", []):
        field = ".".join(error.get("field") or [])
        messages.append(f"{field}: {error['message']}" if field else error["message"])
    return "; ".join(messages)


def load_redirect_rows(path: Path) -> List[Dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise RuntimeError("Redirect CSV is empty.")
        missing = REQUIRED_COLUMNS - set(reader.fieldnames)
        if missing:
            raise RuntimeError(f"Missing required columns: {', '.join(sorted(missing))}")
        rows = []
        for row in reader:
            source = str(row.get("Redirect from", "") or "").strip()
            target = str(row.get("Redirect to", "") or "").strip()
            if not source or not target:
                continue
            rows.append({"Redirect from": source, "Redirect to": target})
        return rows


def query_redirect_nodes(store_domain: str, access_token: str, api_version: str, path: str) -> List[Dict[str, str]]:
    data = graphql_request(
        store_domain=store_domain,
        access_token=access_token,
        api_version=api_version,
        query=URL_REDIRECTS_QUERY,
        variables={"query": f"path:{path}"},
    )
    return list(data["urlRedirects"]["nodes"])


def delete_redirect(store_domain: str, access_token: str, api_version: str, redirect_id: str) -> None:
    data = graphql_request(
        store_domain=store_domain,
        access_token=access_token,
        api_version=api_version,
        query=URL_REDIRECT_DELETE_MUTATION,
        variables={"id": redirect_id},
    )
    payload = data["urlRedirectDelete"]
    if payload.get("userErrors"):
        raise RuntimeError(format_user_errors(payload))


def create_redirect(store_domain: str, access_token: str, api_version: str, path: str, target: str) -> Dict[str, str]:
    data = graphql_request(
        store_domain=store_domain,
        access_token=access_token,
        api_version=api_version,
        query=URL_REDIRECT_CREATE_MUTATION,
        variables={"urlRedirect": {"path": path, "target": target}},
    )
    payload = data["urlRedirectCreate"]
    if payload.get("userErrors"):
        raise RuntimeError(format_user_errors(payload))
    return payload["urlRedirect"]


def ensure_redirect(
    store_domain: str,
    access_token: str,
    api_version: str,
    path: str,
    target: str,
    execute: bool,
) -> str:
    existing_nodes = query_redirect_nodes(store_domain, access_token, api_version, path)
    exact_nodes = [node for node in existing_nodes if node["path"] == path]
    if exact_nodes and all(node["target"] == target for node in exact_nodes):
        return "unchanged"
    if not execute:
        return "replace" if exact_nodes else "create"

    for node in exact_nodes:
        delete_redirect(store_domain, access_token, api_version, node["id"])
    create_redirect(store_domain, access_token, api_version, path, target)
    return "replaced" if exact_nodes else "created"


def main() -> int:
    args = parse_args()
    rows = load_redirect_rows(args.input.expanduser())
    if not rows:
        print("No redirect rows found.", file=sys.stderr)
        return 1

    try:
        store_domain = resolve_store_domain(
            args.store_domain,
            env_path=DEFAULT_ENV_PATH,
            fallback_domain=DEFAULT_STORE_DOMAIN,
        )
        access_token = load_access_token(
            args.access_token,
            Path(args.token_file).expanduser(),
            env_path=DEFAULT_ENV_PATH,
        )
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1

    action_counts: Counter[str] = Counter()
    for row in rows:
        path = row["Redirect from"]
        target = row["Redirect to"]
        status = ensure_redirect(
            store_domain=store_domain,
            access_token=access_token,
            api_version=args.api_version,
            path=path,
            target=target,
            execute=args.execute,
        )
        action_counts[status] += 1
        print(f"{status}: {path} -> {target}")

    print(
        f"Completed. rows={len(rows)} "
        + " ".join(f"{key}={value}" for key, value in sorted(action_counts.items()))
    )
    if not args.execute:
        print("Dry run only. Re-run with --execute to apply live redirects.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
