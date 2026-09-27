#!/usr/bin/env python3
"""Read-only guard: fail when any Shopify product tag carries a supplier/source reference.

Product tags are public (`/products/<handle>.js`), so a tag such as
`offer/<id>.html` or a marketplace item URL leaks the source page. This scans
every product in every status and never writes to Shopify.

Output and logs never contain the raw tag: each finding is reported as a
redacted shape (digits -> 9, URLs -> <host URL>) plus a sha256 prefix.

Exit codes: 0 clean, 1 leaks found, 2 scan error.

Usage:
    python3 ops/scripts/check_product_tag_source_leaks.py
    python3 ops/scripts/check_product_tag_source_leaks.py --json
    python3 ops/scripts/check_product_tag_source_leaks.py --jsonl-log LOG --state-path STATE --notify
    python3 ops/scripts/check_product_tag_source_leaks.py --fixture products.json   # offline

Fix path (owner-approved per incident): `tagsRemove` with the exact live strings,
see anchor 2026-09-26-source-reference-product-tag-cleanup.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import subprocess
import sys
import urllib.request
from pathlib import Path
from typing import Dict, Iterable, List

sys.path.insert(0, str(Path(__file__).resolve().parent))

API_VERSION = "2026-01"
SOURCE_TAG_PATTERN = re.compile(
    r"offer/|\.html?\b|1688|https?:|www\.|taobao|tmall|aliexpress|alibaba", re.IGNORECASE
)
PRODUCTS_QUERY = """query($cursor: String) {
  products(first: 250, after: $cursor) {
    pageInfo { hasNextPage endCursor }
    nodes { id handle status tags }
  }
}"""


def is_source_tag(tag: str) -> bool:
    return bool(SOURCE_TAG_PATTERN.search(tag or ""))


def redact(tag: str) -> Dict[str, str]:
    url = re.match(r"\s*https?://([^/?#\s]+)", tag, re.IGNORECASE)
    if url:
        labels = url.group(1).split(".")
        shape = f"<{labels[-2] if len(labels) > 1 else labels[0]} URL>"
    else:
        shape = re.sub(r"\d", "9", tag)
        shape = re.sub(r"\?.+$", "?<query>", shape)
    return {"shape": shape, "sha256_12": hashlib.sha256(tag.encode("utf-8")).hexdigest()[:12]}


def find_leaks(products: Iterable[Dict]) -> List[Dict]:
    findings = []
    for product in products:
        bad = [tag for tag in product.get("tags") or [] if is_source_tag(tag)]
        if bad:
            findings.append({
                "id": product.get("id"),
                "handle": product.get("handle"),
                "status": product.get("status"),
                "tags": [redact(tag) for tag in bad],
            })
    order = {"ACTIVE": 0, "DRAFT": 1, "ARCHIVED": 2}
    return sorted(findings, key=lambda f: (order.get(f["status"], 3), f["handle"] or ""))


def fetch_products(store_domain: str, token: str) -> List[Dict]:
    products: List[Dict] = []
    cursor = None
    while True:
        request = urllib.request.Request(
            f"https://{store_domain}/admin/api/{API_VERSION}/graphql.json",
            data=json.dumps({"query": PRODUCTS_QUERY, "variables": {"cursor": cursor}}).encode("utf-8"),
            headers={"Content-Type": "application/json", "X-Shopify-Access-Token": token},
        )
        with urllib.request.urlopen(request, timeout=60) as response:
            payload = json.loads(response.read())
        if payload.get("errors"):
            raise RuntimeError(f"GraphQL errors: {payload['errors']}")
        page = payload["data"]["products"]
        products.extend(page["nodes"])
        if not page["pageInfo"]["hasNextPage"]:
            return products
        cursor = page["pageInfo"]["endCursor"]


def finding_keys(findings: List[Dict]) -> List[str]:
    return sorted(f"{f['id']}:{t['sha256_12']}" for f in findings for t in f["tags"])


def notify(title: str, message: str) -> None:
    script = f"display notification {json.dumps(message)} with title {json.dumps(title)}"
    subprocess.run(["osascript", "-e", script], check=False, capture_output=True)


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--fixture", type=Path, help="Read products from a JSON list instead of Shopify.")
    parser.add_argument("--store-domain", default="")
    parser.add_argument("--access-token", default="")
    parser.add_argument("--json", action="store_true", help="Print the full report as JSON.")
    parser.add_argument("--jsonl-log", type=Path, help="Append one JSON line per run.")
    parser.add_argument("--state-path", type=Path, help="Remember findings so --notify fires only on new ones.")
    parser.add_argument("--notify", action="store_true", help="macOS notification when new leaks appear.")
    args = parser.parse_args(argv)

    report: Dict = {"checked_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")}
    try:
        if args.fixture:
            products = json.loads(args.fixture.read_text(encoding="utf-8"))
        else:
            from shopify_admin_config import load_access_token, resolve_store_domain

            products = fetch_products(resolve_store_domain(args.store_domain), load_access_token(args.access_token))
    except Exception as error:  # noqa: BLE001 - any scan failure must be visible, never a false clean
        report.update({"result": "ERROR", "error": f"{type(error).__name__}: {error}"})
        exit_code = 2
        findings: List[Dict] = []
    else:
        findings = find_leaks(products)
        report.update({
            "result": "LEAKS_FOUND" if findings else "CLEAN",
            "products_scanned": len(products),
            "products_with_leaks": len(findings),
            "active_with_leaks": sum(f["status"] == "ACTIVE" for f in findings),
            "tags_matched": sum(len(f["tags"]) for f in findings),
            "findings": findings,
        })
        exit_code = 1 if findings else 0

    new_keys: List[str] = []
    if args.state_path and exit_code != 2:
        previous = set()
        if args.state_path.exists():
            try:
                previous = set(json.loads(args.state_path.read_text(encoding="utf-8")).get("keys", []))
            except (ValueError, OSError):
                previous = set()
        keys = finding_keys(findings)
        new_keys = [key for key in keys if key not in previous]
        args.state_path.parent.mkdir(parents=True, exist_ok=True)
        args.state_path.write_text(json.dumps({"checked_at": report["checked_at"], "keys": keys}), encoding="utf-8")
        report["new_findings"] = len(new_keys)
    elif exit_code == 1:
        new_keys = finding_keys(findings)

    if args.notify:
        if exit_code == 1 and new_keys:
            handles = ", ".join(f["handle"] for f in findings[:3])
            notify("DLM source tag leak",
                   f"{report['tags_matched']} source tag(s) on {report['products_with_leaks']} product(s) "
                   f"({report['active_with_leaks']} active): {handles}")
        elif exit_code == 2:
            notify("DLM source tag guard failed", report["error"][:180])

    if args.jsonl_log:
        args.jsonl_log.parent.mkdir(parents=True, exist_ok=True)
        with args.jsonl_log.open("a", encoding="utf-8") as log:
            log.write(json.dumps(report) + "\n")

    if args.json:
        print(json.dumps(report, indent=1))
    else:
        summary = {k: v for k, v in report.items() if k != "findings"}
        print(json.dumps(summary))
        for finding in findings:
            shapes = ", ".join(f"{t['shape']} [{t['sha256_12']}]" for t in finding["tags"])
            print(f"{finding['status']} {finding['handle']}: {shapes}")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
