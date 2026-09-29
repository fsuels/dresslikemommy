#!/usr/bin/env python3
"""Translate new design copy into the 20 store locales with the ChatGPT app's Codex
(owner's Pro plan; never the paid API), then validate and merge into tr_<loc>.json.

Usage:
  codex_translate_designs.py run <designs_en.json>     # runs Codex in a scratch dir, writes out/<loc>.json
  codex_translate_designs.py merge <designs_en.json>   # validates out/*.json and merges into tr_<loc>.json + en_source.json

designs_en.json: {handle: {"print", "print_sentence", "feature_label", "feature_text"}}
"""
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CODEX = "/Applications/ChatGPT.app/Contents/Resources/codex"
WORK = Path("/tmp/dlm-codex/codex_i18n")
LOCALES = ["ar", "cs", "da", "de", "el", "es", "fi", "fr", "he", "hi", "it", "ja", "ko", "nl", "no", "pl", "pt-BR", "ro", "ru", "sv"]
KEYS = ("print", "print_sentence", "feature_label", "feature_text")


def build_prompt(designs: dict) -> str:
    rules = json.loads((HERE / "en_source.json").read_text(encoding="utf-8"))["_instructions"]
    examples = {loc: {k: v for k, v in list(json.loads((HERE / f"tr_{loc}.json").read_text(encoding="utf-8"))["designs"].items())[:2]} for loc in ("de", "es", "ja")}
    return f"""You are a professional e-commerce translator for Dress Like Mommy, a store of matching family Christmas pajamas.

TASK: translate the product copy in designs_en.json (in this directory) into these 20 locales: {', '.join(LOCALES)}.
Write one UTF-8 JSON file per locale into ./out/<locale>.json (create ./out). Each file must have exactly the same handles
and keys as designs_en.json: {{"<handle>": {{"print": ..., "print_sentence": ..., "feature_label": ..., "feature_text": ...}}}}.

RULES (from the store's translation style guide):
{rules}
- Garment lettering printed on the clothes (e.g. Merry Christmas, MERRY CHRISTMAS, HO HO HO) stays exactly as printed, in the original language and case.
- Natural, fluent shopping copy for native speakers; no machine-literal phrasing; same meaning, no added claims.
- feature_label ends with a colon like the English.
- Keep numbers exactly.

STYLE EXAMPLES from existing approved translations (match this tone and terminology):
{json.dumps(examples, ensure_ascii=False, indent=1)}

Do not ask questions. When all 20 files are written, reply with one line per file: locale, number of handles.
"""


def run(src: Path) -> None:
    designs = json.loads(src.read_text(encoding="utf-8"))
    WORK.mkdir(parents=True, exist_ok=True)
    (WORK / "designs_en.json").write_text(json.dumps(designs, ensure_ascii=False, indent=1), encoding="utf-8")
    (WORK / "prompt.txt").write_text(build_prompt(designs), encoding="utf-8")
    with open(WORK / "prompt.txt", "rb") as fh, open(WORK / "codex.log", "wb") as log:
        rc = subprocess.run(["perl", "-e", "alarm shift; exec @ARGV", "2400", CODEX, "exec", "--skip-git-repo-check",
                             "-C", str(WORK), "-s", "workspace-write", "-"], stdin=fh, stdout=log, stderr=subprocess.STDOUT, cwd=WORK).returncode
    print("codex rc", rc, "files", sorted(p.stem for p in (WORK / "out").glob("*.json")) if (WORK / "out").exists() else [])


def merge(src: Path) -> None:
    designs = json.loads(src.read_text(encoding="utf-8"))
    problems = []
    for loc in LOCALES:
        p = WORK / "out" / f"{loc}.json"
        if not p.exists():
            problems.append(f"{loc}: missing file")
            continue
        tr = json.loads(p.read_text(encoding="utf-8"))
        for handle, en in designs.items():
            t = tr.get(handle)
            if not t or any(not isinstance(t.get(k), str) or not t[k].strip() for k in KEYS):
                problems.append(f"{loc}/{handle}: missing keys")
                continue
            for k in KEYS:
                if re.findall(r"\d+", en[k]) != re.findall(r"\d+", t[k]):
                    problems.append(f"{loc}/{handle}/{k}: numbers differ")
            if not t["feature_label"].rstrip().endswith((":", "：")):
                problems.append(f"{loc}/{handle}: feature_label colon")
            for lettering in re.findall(r"\b(?:MERRY CHRISTMAS|Merry Christmas|HO HO(?: HO)?|MERRY)\b", en["print_sentence"]):
                if lettering not in t["print_sentence"]:
                    problems.append(f"{loc}/{handle}: lettering '{lettering}' not kept")
    if problems:
        print("\n".join(problems[:60]))
        raise SystemExit(f"{len(problems)} problems; nothing merged")
    for loc in LOCALES:
        f = HERE / f"tr_{loc}.json"
        d = json.loads(f.read_text(encoding="utf-8"))
        d["designs"].update(json.loads((WORK / "out" / f"{loc}.json").read_text(encoding="utf-8")))
        f.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    e = json.loads((HERE / "en_source.json").read_text(encoding="utf-8"))
    e["designs"].update(designs)
    (HERE / "en_source.json").write_text(json.dumps(e, ensure_ascii=False, indent=1), encoding="utf-8")
    print("merged", len(designs), "designs into", len(LOCALES), "locales + en_source")


if __name__ == "__main__":
    {"run": run, "merge": merge}[sys.argv[1]](Path(sys.argv[2]))
