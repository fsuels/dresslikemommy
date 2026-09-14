#!/usr/bin/env python3
"""Regression checks that transient translation failures remain retryable."""

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
        cache_path.write_text(
            json.dumps({"el": {"body": None, "description": None}}),
            encoding="utf-8",
        )
        backend = TranslationBackend(cache_path, pause_seconds=0)
        calls = []

        def fake_http_translate_batch(locale, texts):
            calls.append((locale, list(texts)))
            return [f"translated:{text}" for text in texts]

        backend._http_translate_batch = fake_http_translate_batch  # noqa: SLF001

        translated_many = backend.translate_many("el", ["body"])
        translated_one = backend.translate_text("el", "description")

        assert translated_many["body"] == "translated:body"
        assert translated_one == "translated:description"
        assert calls == [("el", ["body"]), ("el", ["description"])]

    with tempfile.TemporaryDirectory() as tmpdir:
        cache_path = Path(tmpdir) / "cache.json"
        backend = TranslationBackend(
            cache_path,
            pause_seconds=0,
            batch_char_limit=20,
        )
        calls = []

        def fake_http_translate_batch(locale, texts):
            calls.append((locale, list(texts)))
            return [f"translated:{text}" for text in texts]

        backend._http_translate_batch = fake_http_translate_batch  # noqa: SLF001
        source = "first paragraph with words\n\nsecond paragraph with words"
        backend._split_long_text = lambda text: [  # noqa: SLF001
            "first paragraph with words\n\n",
            "second paragraph with words",
        ]
        translated = backend.translate_text("de", source)

        assert translated == "translated:first paragraph with words\n\ntranslated:second paragraph with words"
        assert calls == [
            ("de", ["first paragraph with words\n\n"]),
            ("de", ["second paragraph with words"]),
        ]

    print("ok")


if __name__ == "__main__":
    main()
