"""Build a body-only repair from frozen Shopify data; no network or writes to Shopify."""
from pathlib import Path
import hashlib
import html
import json
import re

ROOT = Path(__file__).resolve().parent
before = json.loads((ROOT / "coral_copy_before.json").read_text())
copy = json.loads((ROOT / "coral_copy_replacements.json").read_text())
product = before["product_readback"]["product"]
resource = before["translations_readback"]["translatableResource"]
original = {"en": product["descriptionHtml"]}
for key, value in resource.items():
    if re.fullmatch(r"l\d+", key):
        bodies = [row for row in value if row["key"] == "body_html"]
        assert len(bodies) == 1, key
        original[bodies[0]["locale"]] = bodies[0]["value"]
assert set(original) == set(copy) and len(original) == 21

def digest(value):
    return hashlib.sha256(value.encode()).hexdigest()

def transform(source, locale):
    lists = list(re.finditer(r"<ul\b[^>]*>.*?</ul>", source, re.S))
    assert len(lists) == 2, (locale, "list count")
    chunks = []
    for idx, match in enumerate(lists):
        items = re.findall(r"<li\b[^>]*>.*?</li>", match.group(), re.S)
        assert len(items) == (6 if idx == 0 else 5), (locale, idx, "item count")
        # Existing top rows: fabric, story, print, design, care, size range.
        # Existing lower rows: matching, ruffles, palette, internal chart claim, draft note.
        keep = [1, 2, 3, 5] if idx == 0 else [0, 1, 2]
        chunks.append((match.start(), match.end(), "<ul>\n" + "\n".join(items[i] for i in keep) + "\n</ul>"))
    repaired = source
    for start, end, replacement in reversed(chunks):
        repaired = repaired[:start] + replacement + repaired[end:]
    tables = list(re.finditer(r'<table id="size-chart">.*?</table>', repaired, re.S))
    assert len(tables) == 1, (locale, "size chart")
    table = tables[0]
    prefix, suffix = repaired[:table.start()], repaired[table.end():]
    paragraphs = list(re.finditer(r"<p\b[^>]*>.*?</p>", suffix, re.S))
    assert len(paragraphs) == 3, (locale, "trailing paragraph count")
    assert "<ul" not in suffix[:paragraphs[1].end()], locale
    # Replace the buying-choice paragraph; remove the internal source/derived-size paragraph.
    p0, p1 = paragraphs[:2]
    suffix = suffix[:p1.start()] + suffix[p1.end():]
    suffix = suffix[:p0.start()] + "<p>" + html.escape(copy[locale]["choice"]) + "</p>" + suffix[p0.end():]
    repaired = prefix + "<p>" + html.escape(copy[locale]["note"]) + "</p>\n" + table.group() + suffix
    if locale == "es":
        assert repaired.count("madre e hijo") == 2
        repaired = repaired.replace("madre e hijo", "madre e hija")
        old = "Niñas de 4 años a niños de 9 a 10 años; Madre S a Madre XL."
        assert repaired.count(old) == 1
        repaired = repaired.replace(old, "Tallas para niñas de 4 a 10 años y para mamá de S a XL.")
    if locale == "pt-BR":
        assert repaired.count("para mãe e filho") == 1
        repaired = repaired.replace("para mãe e filho", "para mãe e filha")
    if locale == "fi":
        assert repaired.count("joustava hame") == 1
        repaired = repaired.replace("joustava hame", "laskeutuva hame")
    old_table = re.search(r'<table id="size-chart">.*?</table>', source, re.S).group()
    new_table = re.search(r'<table id="size-chart">.*?</table>', repaired, re.S).group()
    assert old_table == new_table, (locale, "measurement/table change")
    assert repaired != source
    assert repaired.count("<li>") == 7, locale
    assert re.findall(r"https?://[^\s<]+", source) == re.findall(r"https?://[^\s<]+", repaired)
    return repaired, digest(old_table)

changes = []
for locale, source in original.items():
    value, table_hash = transform(source, locale)
    changes.append({"locale": locale, "key": "body_html", "before_sha256": digest(source),
                    "after_sha256": digest(value), "unchanged_size_table_sha256": table_hash,
                    "before": source, "after": value})
plan = {"status": "PREPARED_NOT_APPLIED", "resource_id": product["id"],
        "scope": "Product descriptionHtml and exactly20 existing body_html translations only",
        "authority": "Owner continued the audit with continue working fix everything on September9",
        "change_count": len(changes), "changes": changes,
        "preserve": ["all21 size tables byte-for-byte", "all9 variants and prices", "title", "handle", "status", "onlineStoreUrl", "SEO", "all80 non-body translation values and flags"],
        "source_evidence": ["uploads/coral-blossom-mommy-and-me-dresses/source-size-chart.png", "uploads/coral-blossom-mommy-and-me-dresses/source-selector-mother-xl.png"],
        "measurement_limit": "The source lacks hip values and MotherXL dimensions. Existing numbers stay unchanged and are explicitly disclosed as estimates, not recertified.",
        "rollback": "Restore before English descriptionHtml; read the restored body digest; restore the20 exact original translated bodies with that fresh digest. Do not alter non-body fields.",
        "checks": {"locales":21, "exact_unchanged_size_tables":21, "spanish_gender_corrections":3, "portuguese_gender_corrections":1, "finnish_unverified_stretch_claims_removed":1, "live_writes":0}}
(ROOT / "coral_copy_plan.json").write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n")
(ROOT / "coral_copy_preview_en.html").write_text(changes[0]["after"] + "\n")
print(json.dumps({"status":"PASS", "locales":21, "size_tables_byte_identical":21, "spanish_gender_corrections":3, "portuguese_gender_corrections":1, "finnish_unverified_stretch_claims_removed":1, "live_writes":0}))
