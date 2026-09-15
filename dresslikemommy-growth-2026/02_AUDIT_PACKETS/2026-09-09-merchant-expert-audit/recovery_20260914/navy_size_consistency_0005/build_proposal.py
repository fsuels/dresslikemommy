"""Build the exact local Navy 3XL copy proposal. No API, network, or source writes."""

from collections import Counter
from hashlib import sha256
from html import unescape
from pathlib import Path
import json
import re


BASE = Path(__file__).resolve().parent
BEFORE_SHA = "2bf21a5d758f64fc357a35dd487c6b1c5462e195e0418eabc9cc84dd01bb184e"
PRIVATE_SHA = "cfee12b0feeedaf04b81da3366d96a84d6b0e9ae1129c66caff4d9f6be5e71b4"
PRODUCT_ID = "gid://shopify/Product/7670609346657"
KEYS = ("body_html", "meta_description")
MOTHER_LABELS = {
    "en": "Mother", "ar": "الأم", "cs": "Maminka", "da": "Mor",
    "de": "Mama", "el": "Μητέρα", "es": "Mamá", "fi": "Äiti",
    "fr": "Maman", "he": "אמא", "hi": "माँ", "it": "Mamma",
    "ja": "ママ", "ko": "엄마", "nl": "Mama", "no": "Mamma",
    "pl": "Mama", "pt-BR": "Mãe", "ro": "Mamă", "ru": "Мама",
    "sv": "Mamma",
}
TABLE_RE = re.compile(r"<table\b[^>]*>.*?</table>", re.S | re.I)
ROW_RE = re.compile(r"<tr\b[^>]*>.*?</tr>", re.S | re.I)
CELL_RE = re.compile(r"<t[dh]\b[^>]*>.*?</t[dh]>", re.S | re.I)
RANGE_RE = re.compile(r"S[ \t\u00a0]*[-–—~～][ \t\u00a0]*(3XL)")


def digest(value):
    return sha256(value.encode("utf-8")).hexdigest()


def canonical_hash(value):
    return digest(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")))


def text_only(value):
    return " ".join(unescape(re.sub(r"<[^>]+>", " ", value)).split())


def table_id(table):
    opening = table[:table.index(">") + 1]
    matches = re.findall(r"\bid=[\"']([^\"']+)[\"']", opening)
    assert len(matches) == 1, "Table identity is ambiguous"
    return matches[0]


def exact_edit(before, operations):
    operations = sorted(operations, key=lambda op: op["beforeStart"])
    chunks, unchanged_before = [], []
    previous_end, after_position = 0, 0
    for op in operations:
        start, end = op["beforeStart"], op["beforeEnd"]
        assert previous_end <= start < end <= len(before)
        assert before[start:end] == op["beforeText"]
        segment = before[previous_end:start]
        chunks.extend((segment, op["afterText"]))
        unchanged_before.append(segment)
        after_position += len(segment)
        op["afterStart"] = after_position
        after_position += len(op["afterText"])
        op["afterEnd"] = after_position
        op["beforeByteStart"] = len(before[:start].encode("utf-8"))
        op["beforeByteEnd"] = len(before[:end].encode("utf-8"))
        op["beforeTextSha256"] = digest(op["beforeText"])
        op["afterTextSha256"] = digest(op["afterText"])
        previous_end = end
    chunks.append(before[previous_end:])
    unchanged_before.append(before[previous_end:])
    after = "".join(chunks)

    restored, unchanged_after, previous_end = [], [], 0
    for op in operations:
        start, end = op["afterStart"], op["afterEnd"]
        assert after[start:end] == op["afterText"]
        segment = after[previous_end:start]
        restored.extend((segment, op["beforeText"]))
        unchanged_after.append(segment)
        op["afterByteStart"] = len(after[:start].encode("utf-8"))
        op["afterByteEnd"] = len(after[:end].encode("utf-8"))
        previous_end = end
    restored.append(after[previous_end:])
    unchanged_after.append(after[previous_end:])
    assert "".join(restored) == before, "Exact reverse reconstruction failed"
    assert unchanged_before == unchanged_after, "Unedited bytes changed"
    return after, operations, digest("".join(unchanged_before))


def body_candidate(locale, before):
    assert before.count("3XL") == 3
    tables = list(TABLE_RE.finditer(before))
    assert len(tables) == 2
    assert [table_id(t.group()) for t in tables] == ["size-chart", "size-chart-cardigan"]
    operations, table_checks = [], []
    for table in tables:
        identity = table_id(table.group())
        rows = list(ROW_RE.finditer(table.group()))
        targets = [r for r in rows if "3XL" in r.group()]
        assert len(rows) == 14 and len(targets) == 1
        row = targets[0]
        cells = CELL_RE.findall(row.group())
        assert len(cells) == 10
        assert text_only(cells[0]) == MOTHER_LABELS[locale] + " 3XL"
        assert row.group().count("3XL") == 1
        assert not re.search(r"<img\b|\bhref=|\bsrc=", row.group(), re.I)
        operations.append({
            "kind": "remove_unavailable_mother_3xl_row", "tableId": identity,
            "beforeStart": table.start() + row.start(),
            "beforeEnd": table.start() + row.end(),
            "beforeText": row.group(), "afterText": "",
            "removedCellCount": len(cells),
            "rowLabel": text_only(cells[0]),
        })
        table_checks.append({
            "tableId": identity, "beforeRowsIncludingHeader": len(rows),
            "beforeCellCount": len(CELL_RE.findall(table.group())),
            "removedRows": 1, "removedCells": len(cells),
            "removedRowSha256": digest(row.group()),
            "retainedRowsSha256": digest("".join(r.group() for r in rows if r != row)),
        })
    ranges = list(RANGE_RE.finditer(before))
    assert len(ranges) == 1
    endpoint = ranges[0]
    assert all(not (t.start() <= endpoint.start() < t.end()) for t in tables)
    operations.append({
        "kind": "range_endpoint_3xl_to_2xl",
        "beforeStart": endpoint.start(1), "beforeEnd": endpoint.end(1),
        "beforeText": "3XL", "afterText": "2XL",
    })
    if locale == "fr":
        assert before.count("Echaque") == 1
        start = before.index("Echaque")
        assert before[start:start + len("Echaque pièce est sélectionnée indépendamment")] == "Echaque pièce est sélectionnée indépendamment"
        operations.append({
            "kind": "french_exact_typo",
            "beforeStart": start, "beforeEnd": start + len("Echaque"),
            "beforeText": "Echaque", "afterText": "Chaque",
            "independentLanguageQualification": "REQUIRED_BEFORE_EXECUTION",
        })
    else:
        assert "Echaque" not in before
    after, operations, preserved_sha = exact_edit(before, operations)
    assert "3XL" not in after and "Echaque" not in after
    after_tables = TABLE_RE.findall(after)
    assert len(after_tables) == 2
    for old_table, new_table, check in zip(tables, after_tables, table_checks):
        deleted = next(op["beforeText"] for op in operations if op.get("tableId") == check["tableId"])
        assert old_table.group().replace(deleted, "", 1) == new_table
        old_rows = ROW_RE.findall(old_table.group())
        retained = [r for r in old_rows if r != deleted]
        new_rows = ROW_RE.findall(new_table)
        assert retained == new_rows and len(new_rows) == 13
        assert len(CELL_RE.findall(new_table)) == 130
        check.update({
            "afterRowsIncludingHeader": len(new_rows), "afterCellCount": 130,
            "remainingRowsBytesExact": True, "remainingTableBytesExact": True,
            "remainingMeasurementCellsUnitsAndOrderExact": True,
        })
    return after, operations, {
        "tableChecks": table_checks, "removedRows": 2, "removedCells": 20,
        "beforeTableCellsIncludingHeaders": 280, "afterTableCellsIncludingHeaders": 260,
        "rangeEndpointEdits": 1, "frenchTypoEdits": int(locale == "fr"),
        "remaining3XL": 0, "remainingEchaque": 0,
        "allOtherBytesExact": True, "preservedContentSha256": preserved_sha,
        "exactReverseReconstruction": True,
    }


def seo_candidate(before):
    assert before.count("3XL") == 1
    ranges = list(RANGE_RE.finditer(before))
    assert len(ranges) == 1
    endpoint = ranges[0]
    after, operations, preserved_sha = exact_edit(before, [{
        "kind": "range_endpoint_3xl_to_2xl",
        "beforeStart": endpoint.start(1), "beforeEnd": endpoint.end(1),
        "beforeText": "3XL", "afterText": "2XL",
    }])
    assert "3XL" not in after
    return after, operations, {
        "rangeEndpointEdits": 1, "remaining3XL": 0, "allOtherBytesExact": True,
        "preservedContentSha256": preserved_sha, "exactReverseReconstruction": True,
    }


def main():
    source_path = BASE / "before.json"
    assert sha256(source_path.read_bytes()).hexdigest() == BEFORE_SHA, "Frozen input changed"
    snapshot = json.loads(source_path.read_text())
    assert snapshot["privateSourceBinding"]["sha256"] == PRIVATE_SHA
    product = snapshot["data"]["product"]
    assert product["id"] == PRODUCT_ID and product["status"] == "ACTIVE"
    assert len(product["variants"]["nodes"]) == 24
    assert product["variants"]["pageInfo"]["hasNextPage"] is False
    assert "3XL" not in json.dumps(product["variants"]["nodes"], ensure_ascii=False)
    resources = snapshot["data"]["translatableResourcesByIds"]["nodes"]
    assert len(resources) == 1 and resources[0]["resourceId"] == PRODUCT_ID
    resource = resources[0]
    english = {v["key"]: v for v in resource["translatableContent"]}
    assert english["body_html"]["value"] == product["descriptionHtml"]
    assert english["meta_description"]["value"] == product["seo"]["description"]
    translations = [t for k, values in resource.items() if k.startswith("l_") for t in values]
    assert len(translations) == 100
    assert set(t["locale"] for t in translations) == set(MOTHER_LABELS) - {"en"}
    assert all(t.get("marketId") in (None, "") for t in translations)
    localized = {(t["locale"], t["key"]): t for t in translations}
    assert len(localized) == 100

    changes = []
    for locale in MOTHER_LABELS:
        for key in KEYS:
            previous = english[key] if locale == "en" else localized[(locale, key)]
            before = previous["value"]
            if key == "body_html":
                after, operations, checks = body_candidate(locale, before)
            else:
                after, operations, checks = seo_candidate(before)
            changes.append({
                "resourceId": PRODUCT_ID, "locale": locale, "marketId": None,
                "key": key, "operation": "ProductUpdate" if locale == "en" else "TranslationsRegister",
                "sourceDigestBefore": english[key]["digest"],
                "sourceDigestAfter": None,
                "digestPolicy": "Read fresh Shopify source digest after the English ProductUpdate; content SHA256 is not a newly observed Shopify digest.",
                "beforeValue": before, "beforeValueSha256": digest(before),
                "value": after, "valueSha256": digest(after),
                "beforeOutdated": previous.get("outdated"),
                "sourceEnglishBeforeSha256": digest(english[key]["value"]),
                "edits": operations, "validation": checks,
            })
    en_changes = {c["key"]: c for c in changes if c["locale"] == "en"}
    for c in changes:
        c["sourceEnglishAfterSha256"] = en_changes[c["key"]]["valueSha256"]

    assert len(changes) == 42 and len({(c["locale"], c["key"]) for c in changes}) == 42
    assert sum(len(c["edits"]) for c in changes) == 85
    bodies = [c for c in changes if c["key"] == "body_html"]
    assert len(bodies) == 21
    assert sum(c["validation"]["removedCells"] for c in bodies) == 420
    assert sum(c["validation"]["afterTableCellsIncludingHeaders"] for c in bodies) == 5460
    untargeted_translations = [t for t in translations if t["key"] not in KEYS]
    assert len(untargeted_translations) == 60

    mirrors = []
    metafields = product["metafields"].get("nodes", [])
    for m in metafields:
        if m.get("namespace") == "global" and m.get("key") == "description_tag":
            bindings = [v for v in snapshot["privateSourceBinding"]["protectedMetafieldValueBindings"] if v["metafieldId"] == m["id"]]
            assert len(bindings) == 1
            mirror_before_sha = bindings[0]["valueSha256"]
            assert mirror_before_sha == digest(product["seo"]["description"])
            mirrors.append({
                "metafieldId": m["id"], "namespace": "global", "key": "description_tag",
                "beforeValueSha256": mirror_before_sha,
                "beforeValueBinding": "Exact private protected-metafield SHA256 equals the current English SEO value SHA256.",
                "expectedAfterValueSha256": en_changes["meta_description"]["valueSha256"],
                "explicitMetafieldMutation": False,
                "reason": "Shopify SEO description mirror; verify after ProductUpdate without a separate metafield write.",
            })

    proposal = {
        "action": snapshot["action"], "status": "PROPOSED_REQUIRES_INDEPENDENT_REVIEW",
        "resourceId": PRODUCT_ID, "marketId": None,
        "sourceObservedAt": snapshot["observedAt"], "sourceCompletedAt": snapshot["completedAt"],
        "beforeSnapshotSha256": BEFORE_SHA,
        "privateSourceBinding": {"path": snapshot["privateSourceBinding"]["path"], "sha256": PRIVATE_SHA},
        "scope": "English body_html/SEO description and the same two keys in all20 existing global translations; no other wording or record changes.",
        "operationOrder": [
            "Independent review of exact42 values and French Echaque to Chaque qualification.",
            "Root fresh exact source/product/translation/market-override guard.",
            "ProductUpdate descriptionHtml and seo.description only, then read actual source values and fresh source digests.",
            "Use those newly observed source digests for the40 existing global TranslationsRegister fields, then independent after-state and rendered verification.",
        ],
        "offsetUnits": "Unicode codepoints for Start/End; UTF8 bytes for ByteStart/ByteEnd. Half-open intervals refer to each exact before/after value.",
        "changes": changes, "blocked": [],
        "expectedSeoMirror": mirrors,
        "protectedBaseline": {
            "variantCount": 24, "variantsSha256": canonical_hash(product["variants"]),
            "optionsSha256": canonical_hash(product["options"]),
            "tagsSha256": canonical_hash(product["tags"]),
            "publicationSha256": canonical_hash(product["resourcePublicationsV2"]),
            "untargetedSourceFieldsSha256": canonical_hash([v for v in resource["translatableContent"] if v["key"] not in KEYS]),
            "untargetedGlobalTranslationsCount": 60,
            "untargetedGlobalTranslationsSha256": canonical_hash(untargeted_translations),
            "metadataProtectedByRootPrivateBeforeSnapshot": True,
        },
        "summary": {
            "status": "LOCAL_VALIDATION_PASS", "fieldCount": 42, "englishSourceFields": 2,
            "existingTranslationFields": 40, "localesIncludingEnglish": 21,
            "localeFieldCounts": dict(Counter(c["locale"] for c in changes)),
            "bodyFields": 21, "seoFields": 21, "atomicEdits": 85,
            "unavailableTableRowsRemoved": 42, "tableCellsRemoved": 420,
            "tableCellsBeforeIncludingHeaders": 5880,
            "tableCellsAfterIncludingHeaders": 5460,
            "rangeEndpointEdits": 42, "frenchTypoEdits": 1,
            "remaining3XLInProposedFields": 0,
            "remainingBytesMeasurementsUnitsAndOrderExact": True,
            "all42ExactReverseReconstructionsPass": True,
            "sourceDigestsAfterNotInvented": True, "externalActions": 0,
            "independentFrenchTypoQualification": "REQUIRED_BEFORE_EXECUTION",
            "marketOverrides": "Root query/readback remains separate; no claim of all-market completion from global proposals.",
        },
    }
    output = BASE / "proposal.json"
    output.write_text(json.dumps(proposal, ensure_ascii=False, indent=2) + "\n")
    proposal_sha = sha256(output.read_bytes()).hexdigest()
    script_sha = sha256(Path(__file__).read_bytes()).hexdigest()
    notes = f"""# Navy size-consistency copy proposal

Local proposal only. Root owns independent review, current guards, market-override coverage, supported API operations and exact after-state/rendered verification.

The September15 00:07:33UTC snapshot contains24 complete current variants and no3XL variant. This proposal does not recreate or remove any variant and does not infer who removed historical variants, why, or whether they will return.

## Exact scope

42fields: English body_html and meta_description, plus the same two keys in all20 existing global translations. Each body loses only the Mother3XL row in `size-chart` and in `size-chart-cardigan`. The single remaining body3XL size-range endpoint and single SEO3XL endpoint become2XL. Existing punctuation, ranges, wording, units and all other bytes remain unchanged. The French body additionally changes only `Echaque` to `Chaque` in the existing piece-selection sentence; independent language qualification is required before execution.

Locales: {', '.join(MOTHER_LABELS)}.

Broad retranslation is deliberately excluded. Awkward existing copy, metadata/category references, source images and archived charts are preserved. No chart generator or chart-metafield write is introduced. The global.description_tag SEO mirror is recorded for readback, not separately mutated.

## Verification actually run

- Exact42 field/locale partition, all100 existing translations inventoried,60 untargeted translation fields retained as a protected baseline.
- Every body has the exact two named tables, one verified localized Mother3XL row per table and one outside-table range endpoint.
- Each removed row contains10 cells. Total42 rows and420cells are removed;5460 table cells including headers remain, byte-for-byte with their original row order, measurements and units.
- All85 atomic edits are explicitly recorded:42 row deletions,42 range endpoint edits and one French typo edit. All42 fields reverse exactly to their before values; every byte outside those edits is identical.
- All proposed42 fields contain zero3XL. Each before/value hash and English source old/new content SHA256 is bound. New Shopify digests are intentionally null and must be freshly queried after English ProductUpdate.
- Input source and private evidence hashes are pinned. The builder writes only proposal.json and this notes file and makes no external call.

Proposal SHA256: `{proposal_sha}`

Deterministic builder SHA256: `{script_sha}`

Before snapshot SHA256: `{BEFORE_SHA}`

Private before snapshot SHA256: `{PRIVATE_SHA}`

## Remaining gates

Independent reviewer must qualify the exact French typo and all42 deltas. Root must reconcile relevant market overrides, refresh source/product/translation guards, apply English source first, query actual new Shopify digests, and then register the40 translations. Preserve all24 variants/options/prices/inventory and all unrelated fields. No live mutation or Merchant/feed/market-completion claim is made by this local packet.
"""
    (BASE / "proposal_notes.md").write_text(notes)
    print(json.dumps({
        "status": "PASS", "fields": 42, "localesIncludingEnglish": 21,
        "atomicEdits": 85, "rowsRemoved": 42, "cellsRemoved": 420,
        "cellsPreserved": 5460, "remaining3XL": 0, "seoMirrors": len(mirrors),
        "proposalSha256": proposal_sha,
        "notesSha256": sha256((BASE / "proposal_notes.md").read_bytes()).hexdigest(),
        "builderSha256": script_sha,
    }, indent=2))


if __name__ == "__main__":
    main()
