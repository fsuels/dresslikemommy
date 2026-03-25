#!/usr/bin/env python3
import json
import re
import signal
import time
from pathlib import Path

from deep_translator import GoogleTranslator, MyMemoryTranslator
import requests


COMMENT_RE = re.compile(r"\A(/\*.*?\*/\s*)", re.S)
LIQUID_TOKEN_RE = re.compile(r"(\{\{.*?\}\}|\{%.*?%\}|https?://\S+|dresslikemommy\.com|Dresslikemommy|DLM)", re.I | re.S)
HTML_ENTITY_RE = re.compile(r"&[a-zA-Z#0-9]+;")
GOOGLE_ENDPOINT = "https://translate.googleapis.com/translate_a/single"
BATCH_SEPARATOR = "\n___DLMSEP___\n"
SPLIT_RE = re.compile(r"(\n{2,}|</p>|</li>|</tr>|<br\s*/?>)", re.I)

GOOGLE_TARGET_MAP = {
    "ar": "ar",
    "cs": "cs",
    "da": "da",
    "de": "de",
    "el": "el",
    "es": "es",
    "fi": "fi",
    "fr": "fr",
    "hi": "hi",
    "hr-HR": "hr",
    "hu": "hu",
    "id": "id",
    "it": "it",
    "ja": "ja",
    "ko": "ko",
    "lt-LT": "lt",
    "nb": "no",
    "nl": "nl",
    "pl": "pl",
    "pt-BR": "pt",
    "pt-PT": "pt",
    "ro-RO": "ro",
    "ru": "ru",
    "sk-SK": "sk",
    "sl-SI": "sl",
    "sv": "sv",
    "th": "th",
    "tr": "tr",
    "vi": "vi",
    "zh-CN": "zh-CN",
    "zh-TW": "zh-TW",
}


def read_shopify_json(path):
    raw = Path(path).read_text(encoding="utf-8")
    match = COMMENT_RE.match(raw)
    header = match.group(1) if match else ""
    body = raw[len(header):]
    return header, json.loads(body)


def write_shopify_json(path, header, data):
    payload = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    Path(path).write_text(f"{header}{payload}" if header else payload, encoding="utf-8")


def get_path(data, dotted):
    cur = data
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            raise KeyError(dotted)
        cur = cur[part]
    return cur


def set_path(data, dotted, value):
    cur = data
    parts = dotted.split(".")
    for part in parts[:-1]:
        if part not in cur or not isinstance(cur[part], dict):
            cur[part] = {}
        cur = cur[part]
    cur[parts[-1]] = value


def load_glossary(path):
    if not path:
        return []
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    # Sort longest first to avoid partial overlaps.
    return sorted(raw.items(), key=lambda item: len(item[0]), reverse=True)


def htmlish_text(text):
    stripped = re.sub(r"<[^>]+>", " ", text)
    stripped = HTML_ENTITY_RE.sub(" ", stripped)
    return re.sub(r"\s+", " ", stripped).strip()


def markup_heavy_text(text):
    if not text:
        return False
    return (
        text.count("<a ") >= 3
        or text.count("href=") >= 3
        or text.count("style=") >= 3
        or ("<!--" in text and ("<a " in text or "style=" in text))
    )


class TranslationBackend:
    def __init__(self, cache_path, glossary_path=None, batch_size=40, pause_seconds=0.25, retries=3, request_timeout=20, batch_char_limit=3500):
        self.cache_path = Path(cache_path)
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        if self.cache_path.exists():
            self.cache = json.loads(self.cache_path.read_text(encoding="utf-8"))
        else:
            self.cache = {}
        self.glossary = load_glossary(glossary_path)
        self.batch_size = batch_size
        self.pause_seconds = pause_seconds
        self.retries = retries
        self.request_timeout = request_timeout
        self.batch_char_limit = batch_char_limit

    def _save_cache(self):
        self.cache_path.write_text(json.dumps(self.cache, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    def _target_code(self, locale):
        return GOOGLE_TARGET_MAP.get(locale, locale)

    def _protect(self, text, locale):
        replacements = []
        protected = text

        def token_for(value):
            token = f"___DLMTOK{len(replacements)}___"
            replacements.append((token, value))
            return token

        protected = LIQUID_TOKEN_RE.sub(lambda m: token_for(m.group(0)), protected)

        for source, locale_map in self.glossary:
            target = locale_map.get(locale)
            if not target or source not in protected:
                continue
            protected = protected.replace(source, token_for(target))

        return protected, replacements

    @staticmethod
    def _restore(text, replacements):
        restored = text
        for token, value in replacements:
            restored = restored.replace(token, value)
        return restored

    def _call_with_timeout(self, fn):
        if not hasattr(signal, "SIGALRM"):
            return fn()

        def _raise_timeout(signum, frame):
            raise TimeoutError("translation request timed out")

        previous = signal.getsignal(signal.SIGALRM)
        signal.signal(signal.SIGALRM, _raise_timeout)
        signal.alarm(self.request_timeout)
        try:
            return fn()
        finally:
            signal.alarm(0)
            signal.signal(signal.SIGALRM, previous)

    def _split_long_text(self, text, limit=4000):
        if len(text) <= limit:
            return [text]

        parts = SPLIT_RE.split(text)
        chunks = []
        current = ""
        for part in parts:
            if not part:
                continue
            if len(current) + len(part) <= limit:
                current += part
                continue
            if current:
                chunks.append(current)
                current = ""
            while len(part) > limit:
                cut = part.rfind(" ", 0, limit)
                if cut <= 0:
                    cut = limit
                chunks.append(part[:cut])
                part = part[cut:]
            current = part
        if current:
            chunks.append(current)
        return chunks

    def _http_translate_batch(self, locale, prepared_texts):
        response = requests.post(
            GOOGLE_ENDPOINT,
            data={
                "client": "gtx",
                "sl": "en",
                "tl": self._target_code(locale),
                "dt": "t",
                "q": BATCH_SEPARATOR.join(prepared_texts),
            },
            timeout=self.request_timeout,
        )
        response.raise_for_status()
        payload = response.json()
        translated = "".join(part[0] for part in payload[0])
        parts = translated.split(BATCH_SEPARATOR)
        if len(parts) != len(prepared_texts):
            raise ValueError(f"Unexpected translation batch size for locale {locale}: {len(parts)} != {len(prepared_texts)}")
        return parts

    def _iter_batches(self, texts):
        batch = []
        batch_chars = 0
        for text in texts:
            text_len = len(text)
            projected = batch_chars + text_len + (len(BATCH_SEPARATOR) if batch else 0)
            if batch and (len(batch) >= self.batch_size or projected > self.batch_char_limit):
                yield batch
                batch = []
                batch_chars = 0
            batch.append(text)
            batch_chars += text_len + (len(BATCH_SEPARATOR) if len(batch) > 1 else 0)
        if batch:
            yield batch

    def _translate_core(self, translator, text, locale):
        if not text:
            return text
        lead = re.match(r"^\s*", text).group(0)
        trail = re.search(r"\s*$", text).group(0)
        core = text[len(lead): len(text) - len(trail) if trail else len(text)]
        if not core:
            return text
        protected, replacements = self._protect(core, locale)
        segments = self._split_long_text(protected)
        translated = "".join(translator.translate(segment) for segment in segments)
        return f"{lead}{self._restore(translated, replacements)}{trail}"

    def _translate_single_uncached(self, locale, text):
        locale_cache = self.cache.setdefault(locale, {})
        if text in locale_cache:
            return locale_cache[text]

        lead = re.match(r"^\s*", text).group(0)
        trail = re.search(r"\s*$", text).group(0)
        core = text[len(lead): len(text) - len(trail) if trail else len(text)]
        if not core:
            return text
        protected, replacements = self._protect(core, locale)

        for attempt in range(1, self.retries + 1):
            try:
                if len(protected) <= self.batch_char_limit:
                    translated_core = self._http_translate_batch(locale, [protected])[0]
                else:
                    translator = GoogleTranslator(source="en", target=self._target_code(locale))
                    translated_core = "".join(translator.translate(segment) for segment in self._split_long_text(protected))
                translated = f"{lead}{self._restore(translated_core, replacements)}{trail}"
                locale_cache[text] = translated
                self._save_cache()
                if self.pause_seconds:
                    time.sleep(self.pause_seconds)
                return translated
            except Exception:
                if attempt >= self.retries:
                    break
                time.sleep(min(3.0, 0.6 * attempt))

        translator = GoogleTranslator(source="en", target=self._target_code(locale))
        try:
            translated = self._call_with_timeout(lambda: self._translate_core(translator, text, locale))
        except Exception:
            fallback = MyMemoryTranslator(source="en-US", target=self._target_code(locale))
            try:
                translated = self._call_with_timeout(lambda: self._translate_core(fallback, text, locale))
            except Exception:
                if markup_heavy_text(text):
                    locale_cache[text] = None
                    self._save_cache()
                    return None
                raise
        locale_cache[text] = translated
        self._save_cache()
        return translated

    def translate_text(self, locale, text):
        return self._translate_single_uncached(locale, text)

    def translate_many(self, locale, texts):
        locale_cache = self.cache.setdefault(locale, {})
        missing = []
        order = []
        for text in texts:
            order.append(text)
            if text not in locale_cache:
                missing.append(text)

        oversized = [text for text in missing if len(text) > 4500]
        for text in oversized:
            locale_cache[text] = self._translate_single_uncached(locale, text)
        missing = [text for text in missing if text not in locale_cache]

        if missing:
            for batch in self._iter_batches(missing):
                prepared = []
                batch_replacements = []
                for text in batch:
                    lead = re.match(r"^\s*", text).group(0)
                    trail = re.search(r"\s*$", text).group(0)
                    core = text[len(lead): len(text) - len(trail) if trail else len(text)]
                    protected, replacements = self._protect(core, locale)
                    prepared.append((lead, protected, trail))
                    batch_replacements.append(replacements)

                translated_batch = None
                for attempt in range(1, self.retries + 1):
                    try:
                        translated_batch = self._http_translate_batch(locale, [item[1] for item in prepared])
                        break
                    except Exception:
                        if attempt >= self.retries:
                            translated_batch = None
                            break
                        time.sleep(min(3.0, 0.6 * attempt))

                if not isinstance(translated_batch, list) or len(translated_batch) != len(batch):
                    translator = GoogleTranslator(source="en", target=self._target_code(locale))
                    translated_batch = []
                    for text in batch:
                        try:
                            translated_batch.append(self._translate_core(translator, text, locale))
                        except Exception:
                            if markup_heavy_text(text):
                                translated_batch.append(None)
                            else:
                                raise
                    for text, translated in zip(batch, translated_batch):
                        locale_cache[text] = translated
                else:
                    for text, translated, prepared_item, replacements in zip(batch, translated_batch, prepared, batch_replacements):
                        lead, _, trail = prepared_item
                        locale_cache[text] = f"{lead}{self._restore(translated, replacements)}{trail}"

                self._save_cache()
                if self.pause_seconds:
                    time.sleep(self.pause_seconds)

        return {text: locale_cache[text] for text in order}
