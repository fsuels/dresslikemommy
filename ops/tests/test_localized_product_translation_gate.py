#!/usr/bin/env python3
"""Regression checks for the full-product localization gate."""

from __future__ import annotations

import sys
from pathlib import Path
from types import SimpleNamespace

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
OPS_SCRIPTS = REPO_ROOT / "ops" / "scripts"
if str(OPS_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(OPS_SCRIPTS))

from ops.scripts.audit_shopify_product_translation_completeness import (  # noqa: E402
    audit_product_snapshots,
)
from ops.scripts.audit_localized_pdp_language_leakage import locale_route  # noqa: E402
from ops.scripts.install_shopify_product_translation_launchagent import (  # noqa: E402
    build_program_arguments,
)
from ops.scripts.audit_localized_size_chart_variant_mapping import (  # noqa: E402
    audit_product as audit_variant_mapping,
)
from ops.scripts.poll_shopify_product_translations import (  # noqa: E402
    ExistingTranslation,
    RecentProduct,
    ResourceSnapshot,
    build_translation_payload,
)
from ops.scripts.repair_localized_product_size_charts import audit_product  # noqa: E402


SOURCE_BODY = """
<ul>
  <li><strong>Fabric:</strong> Lightweight chiffon with an easy warm-weather drape.</li>
  <li><strong>Family story:</strong> A soft mom-and-daughter match for sunny family plans.</li>
</ul>
<h3>Size Chart - Dress</h3>
<table id="size-chart"><thead><tr><th>Size</th></tr></thead><tbody><tr><td>Mother S</td></tr></tbody></table>
<p>Choose the sizes you need and create a breezy matching dress moment.</p>
"""


def product() -> RecentProduct:
    return RecentProduct(
        product_gid="gid://shopify/Product/1",
        product_id="1",
        handle="ivory-meadow-mommy-and-me-dresses",
        title="Ivory Meadow Mommy and Me Dresses",
        status="ACTIVE",
        created_at="2026-06-29T00:00:00Z",
        updated_at="2026-07-23T00:00:00Z",
    )


def snapshot(existing_value: str = "") -> ResourceSnapshot:
    existing = {}
    if existing_value:
        existing[("es", "body_html")] = ExistingTranslation(
            locale="es",
            key="body_html",
            value=existing_value,
            outdated=False,
        )
    return ResourceSnapshot(
        resource_id="gid://shopify/Product/1",
        resource_type="Product",
        translatable_content=[
            {
                "key": "body_html",
                "value": SOURCE_BODY,
                "digest": "digest-body",
                "locale": "en",
            }
        ],
        existing_translations=existing,
    )


class FakeClient:
    def __init__(self, resource_snapshot: ResourceSnapshot) -> None:
        self.resource_snapshot = resource_snapshot
        self.register_called = False

    def fetch_resource(self, resource_id: str, locales: list[str], nested_first: int) -> ResourceSnapshot:
        return self.resource_snapshot

    def register_translations(self, resource_id: str, translations: list[dict[str, str]]) -> dict:
        self.register_called = True
        return {"translations": translations}


class FakeTranslator:
    def __init__(self, translated_body: str) -> None:
        self.translated_body = translated_body
        self.calls: list[tuple[str, list[str]]] = []

    def translate_many(
        self,
        locale: str,
        texts: list[str],
        *,
        progress_label: str,
    ) -> dict[str, str]:
        self.calls.append((locale, texts))
        return {text: self.translated_body for text in texts}


def main() -> None:
    assert locale_route("pt-BR") == "pt"

    fallback_body = SOURCE_BODY.replace("Fabric:", "Tela:").replace("Family story:", "Historia familiar:")
    issues, counters = audit_product_snapshots(
        product(),
        [snapshot(fallback_body)],
        ["es"],
        max_snippets_per_body=20,
    )
    assert counters["body_language_issue_count"] == 1
    assert any(issue["issue_type"] == "body_source_language_leakage" for issue in issues)

    translated_body = """
    <ul>
      <li><strong>Tela:</strong> Gasa ligera con una caída cómoda para el clima cálido.</li>
      <li><strong>Historia familiar:</strong> Un conjunto suave para mamá e hija en planes familiares soleados.</li>
    </ul>
    <h3>Tabla de tallas - Vestido</h3>
    <table id="size-chart"><thead><tr><th>Talla</th></tr></thead><tbody><tr><td>Mamá S</td></tr></tbody></table>
    <p>Elige las tallas que necesitas y crea un conjunto de vestidos fresco y coordinado.</p>
    """
    translator = FakeTranslator(translated_body)
    payload, summary = build_translation_payload(
        [snapshot(fallback_body)],
        ["es"],
        translator=translator,
        progress_prefix="test",
        product=product(),
        force_refresh=True,
    )
    assert translator.calls == [("es", [SOURCE_BODY])]
    assert summary["translated_count"] == 1
    refreshed_body = payload[product().product_gid][0]["value"]
    assert "Lightweight chiffon" not in refreshed_body
    assert "Choose the sizes" not in refreshed_body
    assert "Gasa ligera" in refreshed_body
    assert "Mamá S" in refreshed_body

    fake_client = FakeClient(snapshot())
    row = audit_product(
        fake_client,
        {
            "id": "gid://shopify/Product/1",
            "legacyResourceId": "1",
            "handle": product().handle,
            "title": product().title,
            "status": product().status,
            "createdAt": product().created_at,
            "updatedAt": product().updated_at,
            "descriptionHtml": SOURCE_BODY,
        },
        ["es"],
        execute=True,
        pause_ms=0,
        force_rebuild_size_chart_tables=False,
    )
    assert row["planned_translation_count"] == 0
    assert row["registered_translation_count"] == 0
    assert row["missing_locales"] == ["es"]
    assert row["errors"] == ["es:missing_full_body_translation_run_translation_poll_first"]
    assert not fake_client.register_called

    mapping_client = FakeClient(snapshot(translated_body))
    mapping_row = audit_variant_mapping(
        mapping_client,
        {
            "id": "gid://shopify/Product/1",
            "legacyResourceId": "1",
            "handle": product().handle,
            "title": product().title,
            "status": product().status,
            "updatedAt": product().updated_at,
            "descriptionHtml": SOURCE_BODY,
            "options": [
                {"name": "Size", "position": 1, "values": ["Mother S"]},
                {"name": "Color", "position": 2, "values": ["Ivory Meadow"]},
            ],
            "variants": {
                "edges": [
                    {
                        "node": {
                            "id": "gid://shopify/ProductVariant/1",
                            "legacyResourceId": "1",
                            "title": "Mother S / Ivory Meadow",
                            "sku": "DLM-IVMD-MOM-S-IVORY",
                            "availableForSale": True,
                            "selectedOptions": [
                                {"name": "Size", "value": "Mother S"},
                                {"name": "Color", "value": "Ivory Meadow"},
                            ],
                        }
                    }
                ]
            },
        },
        ["es"],
    )
    assert mapping_row["available_variants"] == 1
    assert mapping_row["variants_checked"] == 1
    assert mapping_row["variant_locale_checks"] == 1
    assert mapping_row["unmatched_count"] == 0

    draft_product = {
        "id": "gid://shopify/Product/1",
        "legacyResourceId": "1",
        "handle": product().handle,
        "title": product().title,
        "status": "DRAFT",
        "updatedAt": product().updated_at,
        "descriptionHtml": SOURCE_BODY,
        "options": [
            {"name": "Size", "position": 1, "values": ["Mother S"]},
        ],
        "variants": {
            "edges": [
                {
                    "node": {
                        "id": "gid://shopify/ProductVariant/1",
                        "legacyResourceId": "1",
                        "title": "Mother S",
                        "sku": "DLM-IVMD-MOM-S-IVORY",
                        "availableForSale": False,
                        "selectedOptions": [
                            {"name": "Size", "value": "Mother S"},
                        ],
                    }
                }
            ]
        },
    }
    draft_mapping_row = audit_variant_mapping(mapping_client, draft_product, ["es"])
    assert draft_mapping_row["available_variants"] == 0
    assert draft_mapping_row["variants_checked"] == 1
    assert draft_mapping_row["variant_locale_checks"] == 1
    assert draft_mapping_row["unmatched_count"] == 0

    launch_args = build_program_arguments(
        SimpleNamespace(
            state_path="/tmp/state.json",
            cache_path="/tmp/cache.json",
            min_age_seconds=300,
            page_size=25,
            max_pages=4,
            max_products_per_run=3,
            max_nested_resources=100,
            pause_ms=250,
            execute=True,
            locales="",
        )
    )
    assert "--force-refresh" in launch_args
    assert "--execute" in launch_args

    print("ok")


if __name__ == "__main__":
    main()
