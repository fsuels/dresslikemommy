#!/usr/bin/env python3
"""Regression checks for locale-specific cleanup rules in translation utilities."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops.scripts.translation_utils import TranslationBackend


def main() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        cache_path = tmp_path / "cache.json"
        glossary_path = tmp_path / "glossary.json"
        cleanup_path = tmp_path / "cleanup.json"
        glossary_path.write_text("{}", encoding="utf-8")
        cleanup_path.write_text(
            json.dumps(
                {
                    "de": {
                        "Mama und ich Pyjamas": "Mama-und-ich-Pyjamas",
                    },
                    "ja": {
                        "2016 年以来信頼されています": "2016年から愛され続けています",
                    },
                }
            ),
            encoding="utf-8",
        )

        backend = TranslationBackend(
            cache_path,
            glossary_path,
            cleanup_rules_path=cleanup_path,
        )

        backend.cache["de"] = {
            "title": "Mama und ich Pyjamas",
        }
        backend.cache["ja"] = {
            "trust": "2016 年以来信頼されています",
        }

        translated = backend.translate_many("de", ["title"])
        trust_text = backend.translate_text("ja", "trust")

        assert translated["title"] == "Mama-und-ich-Pyjamas"
        assert trust_text == "2016年から愛され続けています"

    print("ok")


if __name__ == "__main__":
    main()
