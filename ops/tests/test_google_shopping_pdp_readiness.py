#!/usr/bin/env python3
"""Regression checks for Shopping PDP readiness helpers."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops.scripts.audit_google_shopping_pdp_readiness import (  # noqa: E402
    first_available_candidate_variant,
    has_delivery_estimate,
    local_viable,
    parse_html_checks,
    product_handle,
    visible_text,
)


def main() -> None:
    assert product_handle("https://www.dresslikemommy.com/products/mommy-dress") == "mommy-dress"
    assert local_viable({"exclusion_reason": "needs_merchant_center_status;needs_pdp_verification"})
    assert not local_viable({"exclusion_reason": "exclude_missing_gtin;needs_pdp_verification"})

    html = """
    <html><body>
      <form action="/cart/add"><input name="id" value="1"><button name="add">Add to cart</button></form>
      <variant-selects></variant-selects>
      <p>Size guide & fit</p><p>United States | USD $</p>
      <script>subscription hidden</script>
      <p hidden>Delivery details at checkout subscription hidden</p>
      <p style="display:none">Secure Logistics</p>
      <p id="shopify-buyer-consent">This item is a deferred, subscription, or recurring purchase.</p>
    </body></html>
    """
    checks = parse_html_checks(html)
    assert checks["has_product_form"]
    assert checks["has_variant_input"]
    assert checks["has_add_button"]
    assert checks["has_size_guide"]
    assert checks["has_us_currency"]
    assert "subscription hidden" not in visible_text(html)
    assert "Secure Logistics" not in visible_text(html)
    assert "deferred, subscription, or recurring purchase" not in visible_text(html)
    assert has_delivery_estimate("Estimated U.S. delivery: 8-18 business days including processing")
    assert has_delivery_estimate("Estimated delivery May 12")
    assert not has_delivery_estimate("Delivery details at checkout")

    product_json = {
        "variants": [
            {"id": 1, "available": False},
            {"id": 2, "available": True},
        ]
    }
    variant = first_available_candidate_variant(
        product_json,
        [{"shopify_variant_id": "1"}, {"shopify_variant_id": "2"}],
    )
    assert variant["id"] == 2

    print("ok")


if __name__ == "__main__":
    main()
