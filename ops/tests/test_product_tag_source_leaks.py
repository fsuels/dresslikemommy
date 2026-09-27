#!/usr/bin/env python3.13
"""Regression checks for the read-only product tag source-leak guard."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "ops/scripts/check_product_tag_source_leaks.py"
sys.path.insert(0, str(SCRIPT.parent))

import check_product_tag_source_leaks as guard  # noqa: E402

# Synthetic IDs only; never real supplier references.
LEAKY_TAGS = [
    "offer/123456789012.html",
    "/offer/123456789012.htm",
    "/offer/123456789012.html?",
    "/123456789012.html",
    "/item/12345678901.html",
    "https://item.example-market.com/item.htm?id=1",
    "detail.1688.com",
    "taobao listing",
]
CLEAN_TAGS = ["Daddy and Me", "Father 2XL", "Child 11-12yr", "T-Shirts", "Mommy & Me Collection", "html-free", "Spring"]


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args], cwd=ROOT, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )


def main() -> None:
    for tag in LEAKY_TAGS:
        assert guard.is_source_tag(tag), tag
    for tag in CLEAN_TAGS:
        assert not guard.is_source_tag(tag), tag

    redacted = guard.redact("offer/123456789012.html")
    assert redacted["shape"] == "offer/999999999999.html", redacted
    assert guard.redact("https://item.example-market.com/item.htm?id=1")["shape"] == "<example-market URL>"
    assert len(redacted["sha256_12"]) == 12

    products = [
        {"id": "gid://shopify/Product/1", "handle": "archived-one", "status": "ARCHIVED", "tags": ["Spring", LEAKY_TAGS[0]]},
        {"id": "gid://shopify/Product/2", "handle": "active-one", "status": "ACTIVE", "tags": ["Summer", LEAKY_TAGS[5]]},
        {"id": "gid://shopify/Product/3", "handle": "clean", "status": "ACTIVE", "tags": CLEAN_TAGS},
    ]
    findings = guard.find_leaks(products)
    assert [f["handle"] for f in findings] == ["active-one", "archived-one"], findings

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        fixture = tmp_path / "products.json"
        fixture.write_text(json.dumps(products), encoding="utf-8")
        state, log = tmp_path / "state.json", tmp_path / "log.jsonl"

        leak_run = run_cli("--fixture", str(fixture), "--state-path", str(state), "--jsonl-log", str(log), "--json")
        assert leak_run.returncode == 1, leak_run.stdout + leak_run.stderr
        report = json.loads(leak_run.stdout)
        assert report["result"] == "LEAKS_FOUND" and report["active_with_leaks"] == 1 and report["new_findings"] == 2
        # Raw tag strings must never reach stdout or the log.
        for text in (leak_run.stdout, log.read_text(encoding="utf-8")):
            for tag in (LEAKY_TAGS[0], LEAKY_TAGS[5]):
                assert tag not in text, tag

        repeat = json.loads(run_cli("--fixture", str(fixture), "--state-path", str(state), "--json").stdout)
        assert repeat["new_findings"] == 0, repeat

        fixture.write_text(json.dumps([products[2]]), encoding="utf-8")
        clean_run = run_cli("--fixture", str(fixture))
        assert clean_run.returncode == 0, clean_run.stdout + clean_run.stderr

        broken = run_cli("--fixture", str(tmp_path / "missing.json"), "--jsonl-log", str(log))
        assert broken.returncode == 2, broken.stdout + broken.stderr
        assert json.loads(log.read_text(encoding="utf-8").splitlines()[-1])["result"] == "ERROR"

    print("PASS product tag source-leak guard")


if __name__ == "__main__":
    main()
