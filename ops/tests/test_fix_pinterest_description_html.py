#!/usr/bin/env python3
"""Regression checks for Pinterest description HTML trimming."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops.scripts.fix_pinterest_description_html import ProductSnapshot, build_plan, trim_for_pinterest  # noqa: E402


def product(description_html: str, translations: dict[str, str] | None = None, *, active: bool = True) -> ProductSnapshot:
    return ProductSnapshot(
        id="gid://shopify/Product/1",
        legacy_resource_id="1",
        handle="test-product",
        title="Test Product",
        status="ACTIVE" if active else "DRAFT",
        description_html=description_html,
        online_store_published=active,
        pinterest_published=active,
        translations=translations or {},
    )


def test_trim_for_pinterest_falls_back_below_target() -> None:
    html = "<p>" + ("A" * 9000) + "</p><p>" + ("B" * 9000) + "</p>"
    trimmed, reason = trim_for_pinterest(html, 8000)

    assert len(trimmed) <= 8000
    assert reason


def test_build_plan_targets_source_and_translation_rows() -> None:
    rows = build_plan(
        [
            product(
                "<p>" + ("A" * 10050) + "</p>",
                {"pt-BR": "<p>" + ("B" * 10050) + "</p>", "es": "<p>short</p>"},
            )
        ],
        min_length=10000,
        target_length=8000,
        include_not_published=False,
    )

    assert [(row.target, row.locale) for row in rows] == [("source", ""), ("translation", "pt-BR")]
    assert all(row.new_length <= 8000 for row in rows)


def test_build_plan_ignores_not_published_scope_by_default() -> None:
    rows = build_plan(
        [
            ProductSnapshot(
                id="gid://shopify/Product/1",
                legacy_resource_id="1",
                handle="draft-product",
                title="Draft Product",
                status="DRAFT",
                description_html="<p>" + ("A" * 10050) + "</p>",
                online_store_published=False,
                pinterest_published=False,
                translations={},
            )
        ],
        min_length=10000,
        target_length=8000,
        include_not_published=False,
    )

    assert rows == []


if __name__ == "__main__":
    test_trim_for_pinterest_falls_back_below_target()
    test_build_plan_targets_source_and_translation_rows()
    test_build_plan_ignores_not_published_scope_by_default()
    print("ok")
