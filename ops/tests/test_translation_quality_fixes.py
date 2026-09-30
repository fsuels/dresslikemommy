#!/usr/bin/env python3
"""Regression checks for the 2026-09-30 product-translation QA fixes (CEO QA sample, el/da/no/nl/he).

1. "Child 6-12 Months" sizes were left in English (only "Years" was handled).
2. "season"/"person" counted as "son", so mother-daughter products got "Boy" size labels.
3. Colour option values came from machine translation (nl "Green" -> "Groente", vegetables).
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
for path in (REPO_ROOT, REPO_ROOT / "ops" / "scripts"):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from ops.scripts.poll_shopify_product_translations import (  # noqa: E402
    RecentProduct,
    child_role_for_table,
    deterministic_option_translation,
    infer_product_context,
    translated_role_size_label,
)


def product(handle: str, title: str) -> RecentProduct:
    return RecentProduct(product_gid="gid://shopify/Product/1", product_id="1", handle=handle, title=title,
                         status="ACTIVE", created_at="2026-09-30T00:00:00Z", updated_at="2026-09-30T00:00:00Z")


def main() -> None:
    assert translated_role_size_label("Child 6-12 Months", "nl") == "Kind 6-12 maanden"
    assert translated_role_size_label("Child 6-12 Months", "de") == "Kind 6-12 Monate"
    assert translated_role_size_label("Child 6-12 Months", "ja") == "子供 6-12ヶ月"
    assert translated_role_size_label("Child 2-3 Years", "de") == "Kind 2-3 Jahre"  # unchanged

    swimsuit = infer_product_context(product("matching-mom-child-one-shoulder-swimsuit",
                                             "Matching Mom & Child One Shoulder Swimsuit, perfect for the holiday season"), [])
    assert swimsuit["ambiguous_child_role"] == "child"
    assert child_role_for_table("great for the season and every person", "<table></table>", swimsuit) == "child"
    dresses = infer_product_context(product("ivory-tiered-ruffle-mommy-and-me-dresses", "Ivory Tiered Ruffle Mommy and Me Dresses"), [])
    assert dresses["ambiguous_child_role"] == "girl"
    sons = infer_product_context(product("dad-and-sons-shirts", "Dad and Sons Matching Shirts"), [])
    assert sons["ambiguous_child_role"] == "boy"

    assert deterministic_option_translation("ProductOptionValue", "name", "Green", "nl", product_context={}) == "Groen"
    assert deterministic_option_translation("ProductOptionValue", "name", "Light Blue", "de", product_context={}) == "Hellblau"
    assert deterministic_option_translation("ProductOptionValue", "name", "Unlisted Colour", "nl", product_context={}) is None
    print("ok")


if __name__ == "__main__":
    main()
