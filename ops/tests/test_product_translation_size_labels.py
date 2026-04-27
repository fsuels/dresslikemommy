#!/usr/bin/env python3
"""Regression checks for deterministic PDP size-label translation repair."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
OPS_SCRIPTS = REPO_ROOT / "ops" / "scripts"
if str(OPS_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(OPS_SCRIPTS))

from ops.scripts.poll_shopify_product_translations import (  # noqa: E402
    ExistingTranslation,
    RecentProduct,
    ResourceSnapshot,
    build_translation_payload,
    deterministic_option_translation,
    repair_product_html_size_labels,
)


def main() -> None:
    girl_context = {
        "ambiguous_child_role": "girl",
        "has_girl_context": True,
        "has_boy_context": False,
    }

    assert (
        deterministic_option_translation(
            "ProductOptionValue",
            "name",
            "Child 5 Years",
            "es",
            product_context=girl_context,
        )
        == "Niña 5 años"
    )
    assert (
        deterministic_option_translation(
            "ProductOptionValue",
            "name",
            "Mother S",
            "es",
            product_context=girl_context,
        )
        == "Mamá S"
    )
    assert (
        deterministic_option_translation(
            "ProductOptionValue",
            "name",
            'Adult S - Mother "VE"',
            "es",
            product_context=girl_context,
        )
        == 'Adulto S - Mamá "VE"'
    )

    source_html = """
    <h3>Size Chart - Dress</h3>
    <table id="size-chart">
      <thead><tr><th>Size</th><th>Age</th></tr></thead>
      <tbody>
        <tr><td>Child 5 Years</td><td>5</td></tr>
        <tr><td>Mother S</td><td></td></tr>
      </tbody>
    </table>
    """
    translated_html = """
    <h3>Tabla de tallas - Vestido</h3>
    <table id="size-chart">
      <thead><tr><th>Tamaño</th><th>Edad</th></tr></thead>
      <tbody>
        <tr><td>Niño 5 años</td><td>5</td></tr>
        <tr><td>Mother S</td><td></td></tr>
      </tbody>
    </table>
    """
    repaired = repair_product_html_size_labels(source_html, translated_html, "es", girl_context)

    assert "Niña 5 años" in repaired
    assert "Mamá S" in repaired
    assert "Niño 5 años" not in repaired
    assert "Mother S" not in repaired

    product = RecentProduct(
        product_gid="gid://shopify/Product/1",
        product_id="1",
        handle="ivory-tiered-ruffle-mommy-and-me-dresses",
        title="Ivory Tiered Ruffle Mommy and Me Dresses",
        status="ACTIVE",
        created_at="2026-04-27T00:00:00Z",
        updated_at="2026-04-27T00:00:00Z",
    )
    snapshot = ResourceSnapshot(
        resource_id=product.product_gid,
        resource_type="Product",
        translatable_content=[
            {
                "key": "body_html",
                "value": source_html,
                "digest": "digest-body",
                "locale": "en",
            }
        ],
        existing_translations={
            ("es", "body_html"): ExistingTranslation(
                locale="es",
                key="body_html",
                value=translated_html,
                outdated=False,
            )
        },
    )
    payload, summary = build_translation_payload(
        [snapshot],
        ["es"],
        translator=None,
        progress_prefix="test",
        product=product,
        force_refresh=False,
    )

    assert summary["translated_count"] == 1
    body_translation = payload[product.product_gid][0]
    assert body_translation["value"] == repaired

    print("ok")


if __name__ == "__main__":
    main()
