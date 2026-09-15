"""Exact, local-only French chart-label follow-up to the frozen Navy candidate."""

from hashlib import sha256
from html.parser import HTMLParser
from pathlib import Path
import json
import re

BASE = Path(__file__).resolve().parent
FROZEN_SHA = "d200d5dc31fdfb443641e40e1729cfbf347a294938a8a3c7461c4f9eb5a28661"
BEFORE_BODY_SHA = "d53c181559e9ac10fcf8d2a1b1f9afee9be3b6f062ef60a69aa44f5b5c807b89"
OLD = "<th>Hip (cm/po)</th>"
NEW = "<th>Hanches (cm/po)</th>"


def digest(value):
    return sha256(value.encode("utf-8")).hexdigest()


class Structure(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.text = []

    def handle_starttag(self, tag, attrs):
        self.tags.append(("start", tag, attrs))

    def handle_endtag(self, tag):
        self.tags.append(("end", tag))

    def handle_data(self, value):
        self.text.append(value)


def main():
    frozen_path = BASE.parent / "proposal.json"
    frozen_bytes = frozen_path.read_bytes()
    assert sha256(frozen_bytes).hexdigest() == FROZEN_SHA
    frozen = json.loads(frozen_bytes)
    matches = [c for c in frozen["changes"] if c["locale"] == "fr" and c["key"] == "body_html"]
    assert len(matches) == 1
    field = matches[0]
    assert field["resourceId"] == "gid://shopify/Product/7670609346657"
    before = field["value"]
    assert digest(before) == BEFORE_BODY_SHA == field["valueSha256"]
    assert before.count(OLD) == 2
    tables = list(re.finditer(r"<table\b[^>]*>.*?</table>", before, re.S))
    assert len(tables) == 2
    edits = []
    for table, expected_id in zip(tables, ("size-chart", "size-chart-cardigan")):
        identity = re.search(r'\bid=["\x27]([^"\x27]+)', table.group()).group(1)
        assert identity == expected_id and table.group().count(OLD) == 1
        start = before.index(OLD, table.start(), table.end())
        edits.append({
            "tableId": identity, "columnIndexOneBased": 8,
            "beforeHtml": OLD, "afterHtml": NEW,
            "beforeCharStart": start, "beforeCharEnd": start + len(OLD),
            "beforeByteStart": len(before[:start].encode("utf-8")),
            "beforeByteEnd": len(before[:start + len(OLD)].encode("utf-8")),
        })
    after = before.replace(OLD, NEW)
    assert after.count(NEW) == 2 and OLD not in after
    assert after.replace(NEW, OLD) == before
    assert before.split(OLD) == after.split(NEW), "A byte outside the two labels changed"
    a, b = Structure(), Structure()
    a.feed(before)
    b.feed(after)
    assert a.tags == b.tags
    assert re.findall(r"\d+(?:[.,]\d+)?", " ".join(a.text)) == re.findall(r"\d+(?:[.,]\d+)?", " ".join(b.text))
    before_cells = re.findall(r"<td\b[^>]*>.*?</td>", before, re.S)
    after_cells = re.findall(r"<td\b[^>]*>.*?</td>", after, re.S)
    assert before_cells == after_cells and len(after_cells) == 240
    assert sum(1 for token in b.tags if token[0] == "start" and token[1] == "th") == 20
    assert frozen_path.read_bytes() == frozen_bytes

    proposal = {
        "action": "TA07-NAVY-FR-HIP-LABEL-FOLLOWUP",
        "status": "CANDIDATE_AFTER_PENDING_42_FIELD_REPAIR",
        "resourceId": field["resourceId"], "locale": "fr", "marketId": None,
        "key": "body_html",
        "basis": {
            "frozenProposalPath": str(frozen_path), "frozenProposalSha256": FROZEN_SHA,
            "candidateFrenchBodySha256": BEFORE_BODY_SHA,
            "basisIsLiveReadback": False,
        },
        "beforeValueExpectedSha256": BEFORE_BODY_SHA,
        "value": after, "valueSha256": digest(after),
        "sourceDigest": None,
        "requiredPreconditions": [
            "The prior42-field Navy repair must be actually completed and independently verified.",
            "Read the actual current global French body and current English body source digest afresh; require the French body to equal the bound after42 candidate before applying this follow-up.",
            "On any body/source drift, stop and rebase for review; do not register this candidate against a guessed or stale Shopify digest.",
        ],
        "edits": edits,
        "terminologyJustification": {
            "sourceTerm": "Hip", "frenchTerm": "Hanches",
            "reason": "Hanches is the standard French noun used for the hip region in clothing size charts. The plural is natural in this label. It translates the body area without adding a circumference claim such as tour de hanches.",
            "units": "The exact existing (cm/po) text is preserved; no unit or measurement conversion.",
            "qualification": "Linguistic rationale from the proposer; independent approval remains with root/reviewer.",
        },
        "validation": {
            "status": "PASS", "fieldCount": 1, "exactReplacementCount": 2,
            "tableCount": 2, "unchangedDataCellCount": 240,
            "unchangedHeaderCount": 18, "changedHeaderTextCount": 2,
            "allOtherBytesExact": True, "structureAttributesAndGeometryExact": True,
            "numericSequenceAndUnitsExact": True, "exactReverseReconstruction": True,
            "frozenParentCandidateUnchanged": True, "externalActions": 0,
        },
        "excluded": "No other wording, measurement, chart, locale, English source, product, variant, inventory, theme, FAQ, feed, canonical state or live mutation.",
    }
    output = BASE / "proposal.json"
    output.write_text(json.dumps(proposal, ensure_ascii=False, indent=2) + "\n")
    output_sha = sha256(output.read_bytes()).hexdigest()
    builder_sha = sha256(Path(__file__).read_bytes()).hexdigest()
    notes = f"""# Navy French hip-label follow-up

This is a separate local candidate based on the French body **after the pending 42-field repair**, not a current live-body observation. The frozen parent proposal remains unchanged.

Exactly two replacements, one in column 8 of `size-chart` and one in column 8 of `size-chart-cardigan`:

`{OLD}` → `{NEW}`

`Hanches` is the natural French label for the hip region in a clothing size chart. It does not infer that a value is a circumference; `tour de hanches` would add that interpretation and is intentionally not used. The existing `cm/po` units remain exact. No numerical conversion occurs.

Local validation passed: 240 data cells unchanged byte-for-byte, 18 other headers unchanged, identical HTML tag/attribute order and chart geometry, identical numeric sequence, exact inverse recovery of the prior body, and every byte outside the two labels unchanged. Parent proposal immutability was checked.

Before candidate body SHA-256: `{BEFORE_BODY_SHA}`

After candidate body SHA-256: `{digest(after)}`

Proposal SHA-256: `{output_sha}`

Builder SHA-256: `{builder_sha}`

Root must first verify completion of the 42-field repair, then freshly read the actual global French body and current English source digest. The actual French body must match the bound after-42 candidate. Any drift requires review before registration. No digest is invented here, and no live mutation was attempted.
"""
    (BASE / "notes.md").write_text(notes)
    assert frozen_path.read_bytes() == frozen_bytes
    print(json.dumps({
        "status": "PASS", "exactReplacementCount": 2,
        "beforeCandidateBodySha256": BEFORE_BODY_SHA,
        "afterCandidateBodySha256": digest(after),
        "proposalSha256": output_sha,
        "notesSha256": sha256((BASE / "notes.md").read_bytes()).hexdigest(),
        "builderSha256": builder_sha,
        "frozenParentProposalSha256": FROZEN_SHA,
    }, indent=2))


if __name__ == "__main__":
    main()
