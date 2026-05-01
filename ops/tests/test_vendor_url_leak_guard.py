#!/usr/bin/env python3
"""Regression checks for vendor/source URL leak prevention."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops.scripts.audit_and_remove_vendor_url_leaks import (  # noqa: E402
    contains_vendor_url,
    find_text_leaks,
    leaking_tags,
)


def main() -> None:
    assert contains_vendor_url("https://detail.1688.com/offer/123.html")
    assert contains_vendor_url("Supplier page: alibaba.com/item/123")
    assert not contains_vendor_url("https://www.dresslikemommy.com/products/floral-dress")

    tags = [
        "Mommy and Me",
        "https://detail.1688.com/offer/123.html",
        "Dress Like Mommy",
    ]
    assert leaking_tags(tags) == ["https://detail.1688.com/offer/123.html"]

    product = {
        "title": "Clean Dress",
        "descriptionHtml": "<p>Shop Dress Like Mommy.</p>",
        "seo": {"title": "Clean", "description": "https://detail.1688.com/offer/123.html"},
        "metafields": {"nodes": [{"namespace": "custom", "key": "proof", "value": "clean"}]},
    }
    assert find_text_leaks(product) == ["seo.description"]

    prompt = (REPO_ROOT / "ops/prompts/shopify-listing-master-prompt.md").read_text(encoding="utf-8")
    forbidden = [
        "Put `VENDOR_URL` in tags only",
        "- `VENDOR_URL`\n\n## Backup CSV",
        "source URL",
    ]
    assert forbidden[0] not in prompt
    assert forbidden[1] not in prompt
    assert "Never include:" in prompt
    assert "supplier domains" in prompt

    print("ok")


if __name__ == "__main__":
    main()
