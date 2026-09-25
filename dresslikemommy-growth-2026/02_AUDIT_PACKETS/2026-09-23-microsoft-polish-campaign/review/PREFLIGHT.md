# Independent Polish campaign preflight

**Verdict: VERIFIED local payload; BLOCKED live build identity. This is not launch authorization.**

Reviewed 2026-09-23 by the independent read-only verifier. No browser, external writes, payload changes, or canonical-file edits were performed. The only owned output is this review. Confidence: high for exact attachment fidelity and local field checks; live completion is not established.

## Evidence and reproducible result

The verifier independently scanned the attachment by numbered group/section and compared ordered values, rather than rerunning the payload builder. The executed comparison passed **186/186 checks**, including all group JSON and keyword text sidecars. Every supplied positive, headline, description, group negative, campaign negative, URL/path, sitelink, sitelink association, callout, and snippet matches the attachment. No extraction discrepancy was found. All **222** constrained text fields fit the supplied limits. There are **311 unique negative tuples** identified by campaign, scope, keyword, and match type, with zero duplicate scoped tuples and zero token-normalized literal conflicts against a group's positives at campaign or its own group scope. This is not Microsoft's semantic matching or conflict report.

| Field | Independently verified count |
|---|---:|
| Groups | 8 |
| Positive keywords | 144 |
| Headlines / descriptions | 120 / 32 |
| Campaign Polish Phrase / supplemental English Phrase | 145 / 84 |
| Campaign provisional Exact | 18 |
| Total campaign negatives | 247 |
| Total group negatives | 64 |
| Conditional Exact group negatives | 31 |
| Sitelinks / group associations | 8 / 32 |
| Callouts / snippets | 6 / 8 |
| Actual supplied image caption/alt pairs | 0 |

| Group | Positive | Own negatives | Match/condition |
|---|---:|---:|---|
| 1 Sukienki dla mamy i córki | 17 | 10 | Phrase |
| 2 Ubrania dla całej rodziny | 20 | 10 | Exact; shirts/sweaters groups active and eligible |
| 3 Koszule i koszulki rodzinne | 18 | 6 | Exact |
| 4 Piżamy dla mamy i córki | 17 | 0 | Intentionally none |
| 5 Koszule dla taty i syna | 15 | 9 | Phrase |
| 6 Stylizacje dla mamy i córki | 16 | 21 | Exact; each corresponding specific group active and appropriate |
| 7 Stroje kąpielowe mama i córka | 18 | 0 | Intentionally none |
| 8 Swetry i bluzy dla rodziny | 23 | 8 | Phrase |

The complete 64-row expected group list must remain in reconciliation. The 31 conditional rows must not disappear merely because they are described after a conditional paragraph. Preserve those conditions in the build/enablement decision; a paused build does not establish downstream eligibility. Group-specific exclusions must never become campaign or shared-list exclusions. The 18 campaign Exact exclusions remain provisional catalog restrictions; do not broaden them to Phrase.

## Resolved attachment differences

- Current user destination is **DLM | MS | PL | PL | Search | 202609**, Poland/Polish. It supersedes the attachment's US/Polish market. Payload explicitly records the override and does not fabricate a target ID, actual status, budget, or bidding settings.
- The malformed attachment campaign-setting row is not used as identity authority; exact current user name is used.
- All eight proposed tracking suffixes change only `dlm_ms_us_pl_search_202609` to `dlm_ms_pl_pl_search_202609`; all original suffixes remain preserved. Application is correctly gated on native manual/inherited/ad/sitelink tracking reconciliation. Empty source campaign template/suffix alone does not establish account, ad, keyword, group or sitelink tagging. Do not clear working templates/custom parameters or add another UET/purchase goal.
- The attachment claims 160 image text pairs but supplies none, no usable download URL and no image-content mapping. Payload has `supplied_image_text_pairs: 0`, null pairs and null per-group image pairs. **No unsupported captions were invented.** Existing source images must be mapped and retained; captions can be translated only from actually observed copy with image truth verified. Missing attachment image files cannot be treated as verified assets.

## Parent observations and remaining live requirements

`native_source_readback.json` and `landing_smoke_readback.json` were inspected as **parent observations**, not independently repeated live checks. They report account 477439/customer 770182, 11 campaigns and no exact Polish target; source 506254907 enabled, USD10/day, Maximize Clicks, checked USD0.20 cap, English/United States/presence targeting. The pending question is new paused PL/PL copy versus identification of an existing copy. **Do not substitute a peer campaign or assume creation identity has been resolved.**

The source readback has **7 groups**; the attachment has **8**. Group 6 corresponds to “Mommy & Me Outfits,” absent from the seven source names. Exact source-copy parity, copied keyword match sequence and image/extension associations are therefore not established for all eight groups. Preserve the seven native source groups/assets and resolve the eighth target-only group's appropriate source assets from actual observations; no arbitrary duplication or fabricated source mapping.

Parent landing evidence reports all eight `/pl/collections/` URLs loaded with products and Polska/PLN visible. It expressly notes some English product names and no checkout, stock, matching-size or full translation audit. This clears only collection-page smoke checks. It does not establish purchasable matching sizes, per-item pricing clarity, Polish checkout/payment, delivery/returns, conversion tracking, CPC, profitability or launch readiness. Display PLN does not authorize changing the Microsoft account billing currency or prove purchase-event currency.

Before claiming campaign completion, the parent still needs:

1. Exact target identity/create decision, source/target settings preservation, and a fresh target before-state; maintain paused setup and do not infer activation/spend authority.
2. Native source ad/keyword/asset readbacks and an eight-group source-to-target mapping; preserve source/peer/shared records and images.
3. Saved/read-back Polish names, language overrides, Poland presence targeting, 144 positive tuples, eight RSAs, URLs/paths, and scoped assets. Verify native snippet menu headers; payload's “Style”/“Typy” are supplied translations, not observed native labels.
4. Full settled native export reconciliation of all 247 campaign negatives and 64 group negatives by campaign/group/text/match, including inherited/shared/source exclusions and the conditional routing rows. A visible total alone is insufficient.
5. Native tracking hierarchy checks before suffix application; source campaign blank fields are only one level. Native conflict report and remaining purchase/landing checks are separate from this local preflight.

No live Microsoft action or campaign outcome is certified by this review.

## Frozen review hashes

- Attachment SHA256: `46aa62a912cc20f9e88d037e045da5c8ba6c1b88e5a5db5df437fb3565e3aa05`
- `campaign_payload.json` SHA256: `f410411a0415c968d688bd1ffe78e258afeaa9ae169f5bbcc0d7062517393500`
- `validation.json` SHA256: `b1460c52d4c4407c7ababcf7a3426b1ce2ed44850023df64debc19e83bcd879f`

## Read-only reproduction

From the repository root, execute the following Python. It does not import or run the builder and does not modify files. It repeats the core ordered extraction, asset associations, keyword scope/conflict and character-limit checks. The extended 186-check run additionally verified every per-group JSON/keyword sidecar, source name/note/path and tracking field individually.

```python
from pathlib import Path
from collections import Counter
import hashlib, json, re, unicodedata
root = Path("dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-23-microsoft-polish-campaign")
src = Path("/Users/fsuels/.codex/attachments/85bc3fa4-696d-4532-a172-4a26031897df/Pasted text.txt")
rows = src.read_text().splitlines()
p = json.loads((root / "payload/campaign_payload.json").read_text())
v = json.loads((root / "payload/validation.json").read_text())
assert hashlib.sha256(src.read_bytes()).hexdigest() == p["source_sha256"] == v["source_sha256"]
def keyword(s):
    if re.fullmatch(r"\[.+\]", s): return {"text": s[1:-1], "match_type": "Exact"}
    if re.fullmatch(r'"[^"]+"', s): return {"text": s[1:-1], "match_type": "Phrase"}
def present(items): return [x for x in items if x.strip()]
def keys(items): return [keyword(x) for x in items if keyword(x)]
starts = [i for i, x in enumerate(rows) if re.match(r"\d+\. Grupa \d+ — ", x)]
assert len(starts) == len(p["ad_groups"]) == 8
ends = starts[1:] + [rows.index("11. Wykluczenia kampanii — pełne listy")]
for g, a, b in zip(p["ad_groups"], starts, ends):
    block = rows[a:b]
    kw, hd, ds, ng = [next(i for i, x in enumerate(block) if x.startswith(prefix))
        for prefix in ["Pozytywne słowa kluczowe", "Nagłówki", "Opisy", "Wykluczenia"]]
    assert g["positive_keywords"] == keys(block[kw+1:hd])
    assert g["headlines"] == present(block[hd+1:ds])
    assert g["descriptions"] == present(block[ds+1:ng])
    assert g["negative_keywords"] == keys(block[ng+1:])
    assert g["name"] == rows[a].split(" — ", 1)[1]
    assert g["image_text_pairs"] is None
    assert g["source_final_url_suffix"] in rows
    assert g["proposed_final_url_suffix"] == g["source_final_url_suffix"].replace("dlm_ms_us_pl_search_202609", "dlm_ms_pl_pl_search_202609")
    assert g["tracking_action"] == "CONDITIONAL_ON_NATIVE_TRACKING_READBACK"
    assert g["name"] + "\t" + "; ".join(g["sitelinks"]) in rows
    sn = g["structured_snippet"]
    assert g["name"] + "\t" + sn["header"] + "\t" + " · ".join(sn["values"]) in rows
headings = ["A. Polskie wykluczenia kampanii — Phrase", "B. Uzupełniające wykluczenia angielskie — Phrase", "C. Tymczasowe ograniczenia asortymentu — Exact", "D. Czego nie wykluczać automatycznie"]
bounds = [rows.index(x) for x in headings]
negatives = [keys(rows[a:b]) for a, b in zip(bounds, bounds[1:])]
assert [len(x) for x in negatives] == [145, 84, 18]
campaign = sum(negatives, [])
assert p["campaign"]["negative_keywords"] == campaign
assert [len(g["positive_keywords"]) for g in p["ad_groups"]] == [17,20,18,17,15,16,18,23]
assert [len(g["negative_keywords"]) for g in p["ad_groups"]] == [10,10,6,0,9,21,0,8]
assert sum(len(g["negative_keywords"]) for g in p["ad_groups"] if g["negative_application_condition"]) == 31
scope = [("campaign", k["text"], k["match_type"]) for k in campaign]
scope += [(g["name"], k["text"], k["match_type"]) for g in p["ad_groups"] for k in g["negative_keywords"]]
normalized = [(s, unicodedata.normalize("NFC", t).casefold(), m) for s, t, m in scope]
assert len(scope) == len(set(normalized)) == 311
def tokens(x): return re.findall(r"\w+", unicodedata.normalize("NFC", x).casefold())
for g in p["ad_groups"]:
    for positive in g["positive_keywords"]:
        pt = tokens(positive["text"])
        for negative in campaign + g["negative_keywords"]:
            nt = tokens(negative["text"])
            blocked = pt == nt if negative["match_type"] == "Exact" else any(pt[i:i+len(nt)] == nt for i in range(len(pt)-len(nt)+1))
            assert not blocked, (g["name"], positive, negative)
a = rows.index("Użyj polskiego Final URL odpowiadającej grupy.")
b = rows.index("Tytuły i opisy linków zostały sprawdzone względem limitów 25/35/35 znaków.")
texts = present(rows[a+1:b])
assert len(texts) == 32
for i, s in enumerate(p["campaign"]["sitelinks"]):
    assert [s["text"], s["text"], s["description_1"], s["description_2"]] == texts[i*4:i*4+4]
    assert s["final_url"] == p["ad_groups"][i]["final_url"]
a = rows.index("Jeden wiersz do każdego pola:")
b = rows.index("Wszystkie sześć tekstów mieści się w limicie 25 znaków.")
assert p["campaign"]["callouts"] == present(rows[a+1:b])
lengths = []
for g in p["ad_groups"]:
    lengths += [(len(x),30) for x in g["headlines"]] + [(len(x),90) for x in g["descriptions"]]
    lengths += [(len(g[x]),15) for x in ["path_1","path_2"]] + [(len(x),25) for x in g["structured_snippet"]["values"]]
for s in p["campaign"]["sitelinks"]:
    lengths += [(len(s["text"]),25),(len(s["description_1"]),35),(len(s["description_2"]),35)]
lengths += [(len(x),25) for x in p["campaign"]["callouts"]]
assert len(lengths) == 222 and all(n <= limit for n, limit in lengths)
assert [(x["length"],x["limit"]) for x in v["length_checks"]] == lengths
assert p["image_assets"]["supplied_image_text_pairs"] == 0 and p["image_assets"]["pairs"] is None
assert p["campaign"]["name"] == "DLM | MS | PL | PL | Search | 202609"
assert p["campaign"]["location"] == "Poland" and p["campaign"]["language"] == "Polish"
print("PASS: exact supplied values; 311 unique negative tuples; no literal conflicts; 222 valid text fields")
```
