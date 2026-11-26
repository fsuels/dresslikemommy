#!/usr/bin/env python3
"""The store name must reach the translator as a protected token and come back verbatim."""

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
        glossary_path = Path(tmpdir) / "glossary.json"
        glossary_path.write_text(json.dumps({}), encoding="utf-8")
        backend = TranslationBackend(Path(tmpdir) / "cache.json", glossary_path)
        source = "Red Heart Family Sweaters | Dress Like Mommy"
        protected, replacements = backend._protect(source, "es")  # noqa: SLF001
        assert "Dress Like Mommy" not in protected, protected
        # Simulate a translator that rewrites every plain word around the token.
        translated = protected.replace("Red Heart Family Sweaters", "Suéteres familiares Red Heart")
        restored = backend._restore(translated, replacements)  # noqa: SLF001
        assert restored == "Suéteres familiares Red Heart | Dress Like Mommy", restored
        untouched, reps = backend._protect("Soft knit for the whole family.", "es")  # noqa: SLF001
        assert backend._restore(untouched, reps) == "Soft knit for the whole family."  # noqa: SLF001
    print("ok")


if __name__ == "__main__":
    main()
