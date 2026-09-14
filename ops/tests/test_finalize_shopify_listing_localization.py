#!/usr/bin/env python3
"""Regression checks for the synchronous listing localization closeout."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops.scripts.finalize_shopify_listing_localization import (  # noqa: E402
    build_gate_steps,
    normalize_handles,
)


def main() -> None:
    assert normalize_handles("ivory-meadow-mommy-and-me-dresses") == [
        "ivory-meadow-mommy-and-me-dresses"
    ]
    assert normalize_handles("z-product,a-product,z-product") == ["a-product", "z-product"]

    with tempfile.TemporaryDirectory() as temp_dir:
        steps = build_gate_steps(
            repo_root=REPO_ROOT,
            python_executable=Path("/usr/bin/python3"),
            handles=["future-listing"],
            work_dir=Path(temp_dir),
        )

    assert [step.name for step in steps] == [
        "translate_full_product",
        "audit_full_product_before_size_repair",
        "repair_localized_size_charts",
        "audit_full_product_after_size_repair",
        "audit_localized_size_charts",
        "audit_variant_size_chart_mapping",
    ]

    translation_command = steps[0].command
    assert "--execute" in translation_command
    assert "--force-refresh" in translation_command
    min_age_index = translation_command.index("--min-age-seconds")
    assert translation_command[min_age_index + 1] == "0"

    assert sum("audit_shopify_product_translation_completeness.py" in " ".join(step.command) for step in steps) == 2
    assert all(
        "--fail-on-issues" in step.command
        for step in steps
        if "audit_shopify_product_translation_completeness.py" in " ".join(step.command)
    )
    assert "--execute" in steps[2].command
    assert "--fail-on-missing" in steps[4].command
    assert "--fail-on-unmatched" in steps[5].command

    required_reference = "finalize_shopify_listing_localization.py"
    for relative_path in [
        "ops/prompts/START-HERE.md",
        "ops/prompts/shopify-listing-master-prompt.md",
        "ops/prompts/shopify-listing-from-1688.md",
        "docs/agent-loops/product-listing-localization-loop.md",
    ]:
        assert required_reference in (REPO_ROOT / relative_path).read_text(encoding="utf-8"), relative_path

    print("ok")


if __name__ == "__main__":
    main()
