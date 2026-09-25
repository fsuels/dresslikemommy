# -*- coding: utf-8 -*-
import copy
import hashlib
import html
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
load = lambda path: json.loads(path.read_text())
file_sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
sha = lambda value: hashlib.sha256(value.encode()).hexdigest()
plain = lambda value: re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', value))).strip()
dump = lambda name, value: (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
input_file = ROOT / 'review/product-title-completeness/candidate_000_079.json'
rows = load(input_file)
work = {}
for locale in {r['locale'] for r in rows}:
    f = ROOT / ('review/product-title-completeness/worklist_' + locale + '.json')
    for row in load(f)['rows']:
        work[row['i']] = (row, file_sha(f))

# Known source ambiguity is separated from a translation error; no replacement facts invented.
holds = {
    6: 'Ch... after the dash is ambiguous: chic, child, or another qualifier; the candidate discards that fragment.',
    9: 'Ruffle A... confirms ruffles but the missing A-word is not uniquely established by the body; candidate drops it.',
    16: 'wi... introduces an unknown following attribute; preserving ellipsis alone does not recover that source clause.',
    22: 'Current English title and introduction say Two-Piece, but same current body says Stylish one-piece design with elegant cut-out details.',
    24: 'wit... introduces an unknown following attribute; the proposed title silently drops it.',
    51: 'C... after Cardigans may refer to cream/cozy/cardigan or another qualification; not uniquely recoverable.',
    57: 'f... after Jean Jackets introduces an unknown recipient/qualification; candidate silently drops it.',
    59: 'for... lacks a uniquely recoverable recipient or qualification; body audience alone does not prove the missing title wording.',
    62: 'Perfect for S... is unresolved: body lists both spring and summer; candidate drops the entire qualification.',
    63: 'P... after Bow Detail is unresolved; candidate silently drops the fragment.',
    72: 'The quoted Wh... slogan is not given in the English body; do not invent or silently remove printed text.',
    77: 'D... after T-Shirt Set is unresolved; candidate silently drops the fragment.',
}
changes = {
    145: ('Elegante bañador tropical de una pieza con volantes y exuberante estampado botánico … | DLM', 'Restore source Chic and attach tropical to the swimsuit rather than the ruffles.'),
    148: ('בגד ים שלם טרופי ואלגנטי עם מלמלות ודוגמה בוטנית עשירה … | DLM', 'Restore omitted Chic meaning.'),
    206: ('Moderni monokromaattinen yhden olkapään uimapuku eläinkuviolla … | DLM', 'Monochrome is not necessarily solid-color; yksivärinen incorrectly implies no multi-tone pattern.'),
    248: ('בגד ים שלם מפוספס ואלגנטי עם מלמלות עליזות … | DLM', 'Restore omitted Chic meaning.'),
    425: ('Elegante bañador de una pieza con bloques de color para madre e hija … | DLM', 'Restore omitted Chic meaning.'),
    722: ('Matchende badeshorts til far og søn – elegant blåt … | DLM', 'Restore visible source Elegant Blue; living ocean is a different description.'),
    742: ('Matchende badeshorts til far og søn med tropisk præg … | DLM', 'Restore source Tropical Flair instead of substituting a fresh leaf pattern.'),
    762: ('Matchende badeshorts til far og søn "Dynamic Duo" … | DLM', 'Preserve the visible source design name Dynamic Duo; pink flamingo is a different description.'),
    1060: ('فساتين محبوكة مريحة متناسقة بنقشة النجوم باللون الكريمي للعائلة … | DLM', 'Cozy describes the garment rather than the cream color.'),
    1280: ('ملابس بألوان قوس قزح الزاهية مع تيشيرتات مخططة وأفرولات وشورتات صفراء … | DLM', 'Body resolves yellow bottoms to overalls AND shorts across the family, not only overalls.'),
    1281: ('Výrazné duhové soupravy s pruhovanými tričky a žlutými lacláči a šortkami … | DLM', 'Body resolves yellow bottoms to overalls and shorts.'),
    1282: ('Farverige regnbueoutfits med stribede T-shirts og gule overalls og shorts … | DLM', 'Body resolves yellow bottoms to overalls and shorts.'),
    1284: ('Ζωηρά σύνολα στα χρώματα του ουράνιου τόξου με ριγέ μπλουζάκια και κίτρινες σαλοπέτες και σορτς … | DLM', 'Body resolves yellow bottoms to overalls and shorts.'),
    1285: ('Conjuntos arcoíris vibrantes con camisetas de rayas, petos y pantalones cortos amarillos … | DLM', 'Body resolves yellow bottoms to overalls and shorts.'),
    1286: ('Eloisat sateenkaariasut raidallisilla T-paidoilla sekä keltaisilla lappuhaalareilla ja shortseilla … | DLM', 'Body resolves yellow bottoms to overalls and shorts.'),
    1287: ('Tenues arc-en-ciel éclatantes avec T-shirts rayés, salopettes et shorts jaunes … | DLM', 'Body resolves yellow bottoms to overalls and shorts.'),
    1288: ('תלבושות ססגוניות בצבעי הקשת עם חולצות טי מפוספסות ואוברולים ומכנסיים קצרים צהובים … | DLM', 'Restore vibrant and T-shirt specificity; body resolves yellow bottoms to overalls and shorts.'),
    1289: ('रंग-बिरंगे रेनबो आउटफिट्स, धारीदार टी-शर्ट और पीले ओवरऑल व शॉर्ट्स के साथ … | DLM', 'Body resolves yellow bottoms to overalls and shorts.'),
    1308: ('תלבושות במראה אומברה – חולצות טי ורודות וכחולות עם מכנסיים קצרים לבנים … | DLM', 'Preserve the source T-shirt garment category, not generic shirts.'),
    1428: ('סט חולצות טי תואמות לאבא ולתינוק עם הכיתובים "Player 1" ו-"Player 2" … | DLM', 'Preserve the body-resolved source T-shirt garment category.'),
    1488: ('סט תואם של חולצת טי ובגד גוף לתינוק עם "Top Dad" ו-"Top Son" … | DLM', 'Preserve source T-shirt rather than generic shirt.'),
    1588: ('סט תואם של חולצת טי ובגד גוף לאבא ולתינוק בעיצוב "Bestie Heart" … | DLM', 'Preserve source T-shirt rather than generic shirt.'),
}
qualified, held, proposals, checks = [], [], [], []
for row in rows:
    inv, work_sha = work[row['i']]
    for key in ['resourceId', 'locale', 'key', 'marketId', 'sourceValue', 'sourceDigest', 'sourceSHA256', 'rawBefore', 'effectiveBeforeValue', 'expectedEffectiveBeforeValueSHA256', 'overlayApplied', 'overlaySourceFile', 'overlaySourceFileSHA256', 'rawFile', 'rawFileSHA256', 'before']:
        assert row[key] == inv[key], (row['i'], key)
    assert row['sourceSHA256'] == sha(row['sourceValue'])
    assert row['valueSHA256'] == sha(row['value'])
    assert row['expectedBeforeValueSHA256'] == sha(row['effectiveBeforeValue'])
    assert row['rawFileSHA256'] == file_sha(ROOT / row['rawFile'])
    raw = load(ROOT / row['rawFile'])
    node = next(n for n in raw['data']['translatableResourcesByIds']['nodes'] if n['resourceId'] == row['resourceId'])
    title = next(t for t in node['translatableContent'] if t['key'] == 'title')
    body = next(t for t in node['translatableContent'] if t['key'] == 'body_html')
    assert title['value'] == row['sourceValue'] and title['digest'] == row['sourceDigest']
    assert row['supportingSourceDigests']['body_html'] == body['digest']
    assert row['supportingSourceBodySHA256'] == sha(body['value'])
    assert row['supportingSourceQuoteNormalizedWhitespace'] in plain(body['value']), row['i']
    target = copy.deepcopy(row)
    target['independentInputFile'] = str(input_file.relative_to(ROOT))
    target['independentInputFileSHA256'] = file_sha(input_file)
    target['independentWorklistSHA256'] = work_sha
    if row['productIndex'] in holds:
        target['independentReviewStatus'] = 'HELD_SOURCE_CONTRADICTION_OR_UNRESOLVED_CLIPPED_MEANING'
        target['independentHoldReason'] = holds[row['productIndex']]
        held.append(target)
        checks.append({'i': row['i'], 'binding': 'PASS', 'meaning': 'SOURCE_DISPOSITION_REQUIRED', 'reason': target['independentHoldReason']})
        continue
    if row['i'] in changes:
        value, reason = changes[row['i']]
        target['beforeCandidateValue'] = row['value']
        target['value'] = value
        target['valueSHA256'] = sha(value)
        target['independentCorrectionReason'] = reason
        proposals.append(copy.deepcopy(target))
    target['independentReviewStatus'] = 'PASS_COMPLETE_VISIBLE_TITLE_MEANING_AND_BOUND_CONTEXT'
    target['reviewStatus'] = 'INDEPENDENTLY_REVIEWED_PENDING_ROOT_FRESH_GUARDS'
    target['requiresFreshLiveSourceAndBeforeGuard'] = True
    qualified.append(target)
    checks.append({'i': row['i'], 'binding': 'PASS', 'meaning': 'PASS_AFTER_CORRECTION' if row['i'] in changes else 'PASS'})
assert len(rows) == 252 and len(held) == 37 and len(qualified) == 215 and len(proposals) == 22
dump('product_a000_079_reviewed215.json', {'rows': qualified})
dump('product_a000_079_holds37.json', {'rows': held})
dump('product_a000_079_corrections22.json', {'rows': proposals})
dump('product_a000_079_checks.json', {'status': '215_QUALIFIED_37_SOURCE_HOLDS', 'reviewed': 252, 'qualified': 215, 'wordingCorrections': 22, 'sourceHolds': 37, 'checks': checks, 'limitation': 'Exact saved source, raw/effective before, body digests and normalized quotes verified locally. Root must freshly check all source/digest/before/supporting-body values before release. No external writes.'})
print(json.dumps({'reviewed':252,'qualified':215,'corrections':22,'held':37}))
