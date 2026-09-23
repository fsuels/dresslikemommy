#!/usr/bin/env python3
"""Reject provider token damage without contacting translation providers."""

import json
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))
from ops.scripts.translation_utils import TranslationBackend


class BrokenTranslator:
    def __init__(self, **kwargs):
        pass

    def translate(self, text):
        return text.replace("QZXTOKEN00000QXZ", "QZXTOKEN0000")


def main():
    with tempfile.TemporaryDirectory() as tmp:
        backend = TranslationBackend(Path(tmp) / "cache.json", retries=1, pause_seconds=0)
        source = '<p><strong>Dress</strong> <a href="https://example.com/a">shop</a></p>'
        protected, replacements = backend._protect(source, "fr")
        assert backend._restore_checked(protected, protected, replacements) == source
        first, second = replacements[0][0], replacements[1][0]
        damaged = [
            protected.replace(first, ""),
            protected.replace(first, first + first),
            protected.replace(first, "QZXTOKEN0000"),
            protected.replace(first, "SWAP").replace(second, first).replace("SWAP", second),
            protected + "QZ012QZ0",
            protected + '<span title="QZXTOKEN99999QXZ">X</span>',
            "<i>" + protected + "</i>",
            None,
        ]
        for value in damaged:
            try:
                backend._restore_checked(protected, value, replacements)
            except ValueError:
                pass
            else:
                raise AssertionError(f"Accepted damaged protected response: {value!r}")

        backend.glossary = [("Mom", {"fr": "Maman"}), ("Child", {"fr": "Enfant"})]
        text, terms = backend._protect("Mom Child Mom", "fr")
        moved = " ".join([terms[1][0], terms[0][0], terms[0][0]])
        assert backend._restore_checked(text, moved, terms) == "Enfant Maman Maman"
        for bad in ["QZXTOKEN0001", "QZXTOKEN00012QX", "QZXTOKENQZQ028ZTOKX8", "QZ012QZ0", "0024QXZ002", "Q0024QX0"]:
            assert backend._contains_placeholder_tokens(bad), bad
        assert not backend._contains_placeholder_tokens('<img src="https://cdn.example/QZ012QZ0.jpg">')
        assert not backend._contains_placeholder_tokens("https://cdn.example/QZ012QZ0.jpg")
        assert backend._contains_placeholder_tokens('<img alt="QZXTOKEN00005QXZ" src="x.jpg">')
        assert backend._contains_placeholder_tokens('shop<span></span>QZ012QZ0')

        # Exhausting all mocked providers fails closed, with no bad string cached.
        backend._http_translate_batch = lambda locale, texts: [BrokenTranslator().translate(t) for t in texts]
        with patch("ops.scripts.translation_utils.GoogleTranslator", BrokenTranslator), patch(
            "ops.scripts.translation_utils.MyMemoryTranslator", BrokenTranslator
        ):
            assert backend.translate_text("fr", source) is None
        assert backend.cache["fr"][source] is None
        assert json.loads(backend.cache_path.read_text())["fr"][source] is None

        # One corrupt batch member sends the whole batch through checked fallback.
        a, b = "<p>First</p>", "<p>Second</p>"
        backend._http_translate_batch = lambda locale, texts: [texts[0], texts[1].replace(first, "")]
        calls = []
        def fallback(locale, text, **kwargs):
            calls.append(text)
            return None
        with patch.object(backend, "_translate_single_uncached", side_effect=fallback):
            assert backend.translate_many("de", [a, b]) == {a: None, b: None}
        assert sorted(calls) == sorted([a, b])

        # Mangled legacy cache entries are retried; a clean response is restored.
        backend.cache["fr"][source] = "QZXTOKEN00012QX"
        backend._http_translate_batch = lambda locale, texts: texts
        assert backend.translate_text("fr", source) == source
        backend.cache["de"][a] = "0024QXZ002"
        assert backend.translate_many("de", [a]) == {a: a}
        # Old entries with silently lost markup must not bypass fresh validation.
        backend.cache["fr"][source] = "Dress shop"
        assert backend.translate_text("fr", source) == source
        backend.cache["de"][a] = "First"
        assert backend.translate_many("de", [a]) == {a: a}
        assert backend._cache_value_is_valid("<p>First</p>", "<p>Premier</p>")
    print("ok")


if __name__ == "__main__":
    main()
