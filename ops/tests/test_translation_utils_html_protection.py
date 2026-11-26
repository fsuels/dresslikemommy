#!/usr/bin/env python3
"""Lightweight regression checks for translation utility protections."""

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
        cache_path = Path(tmpdir) / "cache.json"
        glossary_path = Path(tmpdir) / "glossary.json"
        glossary_path.write_text(
            json.dumps(
                {
                    "Mommy and Me": {
                        "fr": "Maman et moi",
                    }
                }
            ),
            encoding="utf-8",
        )

        backend = TranslationBackend(cache_path, glossary_path)
        protected, replacements = backend._protect(  # noqa: SLF001
            '<table id="size-chart"><tr><td>Mommy and Me</td></tr></table>',
            "fr",
        )
        restored = backend._restore(protected, replacements)  # noqa: SLF001

        assert '<table id="size-chart">' not in protected
        assert "</table>" not in protected
        assert "Mommy and Me" not in protected
        assert restored == '<table id="size-chart"><tr><td>Maman et moi</td></tr></table>'
        assert backend._contains_placeholder_tokens("__DLMTOK0___") is True  # noqa: SLF001

        # Regression: a token glued to a word made the translator keep that word's
        # first letter ("Halto", "Eda talla"). Tokens must be space-separated.
        source = "<th>Height (cm)</th><p>Each size</p> text<strong>Print:</strong>x"
        protected, replacements = backend._protect(source, "es")  # noqa: SLF001
        import re as _re

        assert not _re.search(r"QZXTOKEN\d{5}QXZ(?!QZXTOKEN)[A-Za-z0-9]", protected)
        assert not _re.search(r"[A-Za-z0-9]QZXTOKEN", protected.replace("QXZQZXTOKEN", "QXZ QZXTOKEN"))
        assert backend._restore(protected, replacements) == source  # noqa: SLF001

    print("ok")


if __name__ == "__main__":
    main()
