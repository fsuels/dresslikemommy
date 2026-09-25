"""Extract and validate the supplied Portuguese copy. Local only; no account writes."""
import hashlib
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path

SOURCE = Path('/Users/fsuels/.codex/attachments/dc7e3a91-c385-4fe1-b4b5-8a24a8a72f62/Pasted text.txt')
OUT = Path(__file__).resolve().parent
source = SOURCE.read_text()


def between(text, first, last):
    return text.split(first, 1)[1].split(last, 1)[0]


def nonempty(text):
    return [line.strip() for line in text.strip().splitlines() if line.strip()]


def keywords(text):
    result = []
    for line in nonempty(text):
        if line.startswith('[') and line.endswith(']'):
            result.append({'text': line[1:-1], 'match_type': 'Exact'})
        elif line.startswith('"') and line.endswith('"'):
            result.append({'text': line[1:-1], 'match_type': 'Phrase'})
    return result


def render_keywords(values):
    return '\n'.join('[' + v['text'] + ']' if v['match_type'] == 'Exact' else '"' + v['text'] + '"' for v in values)


groups = []
sections = list(re.finditer(r'^\d+\. Grupo (\d+) — (.+)$', source, re.M))
for i, m in enumerate(sections):
    end = sections[i + 1].start() if i + 1 < len(sections) else source.index('11. Negativas de campanha')
    block = source[m.end():end]
    number = int(m[1])
    negative_part = block.split('Negativas ', 1)[1]
    group = {
        'number': number,
        'name': m[2],
        'source_role_english': re.search(r'Equivalente a (.+)\.', block)[1],
        'source_lines': [source[:m.start()].count('\n') + 1, source[:end].count('\n')],
        'ad_group_type': 'Standard',
        'ad_type': 'Responsive Search Ad',
        'final_url': re.search(r'^https://\S+$', block, re.M)[0],
        'path_1': re.search(r'^Caminho 1: (.+)$', block, re.M)[1],
        'path_2': re.search(r'^Caminho 2: (.+)$', block, re.M)[1],
        'positive_keywords': keywords(between(block, 'Palavras-chave positivas', 'Títulos')),
        'headlines': nonempty(between(block, 'Títulos', 'Descrições').removeprefix(' — um por campo')),
        'descriptions': nonempty(between(block, 'Descrições', 'Negativas ').removeprefix(' — uma por campo')),
        'negative_keywords': keywords(negative_part),
        'source_negative_guidance': nonempty('\n'.join(l for l in negative_part.splitlines()[1:] if not l.startswith(('"', '[')))),
        'pins': None,
        'landing_status': 'LIVE_READBACK_REQUIRED',
        'locale_path_status': 'UNVERIFIED_SUPPLIED_PT_PATH_MAY_REQUIRE_PT_BR',
    }
    if number in (3, 7, 8):
        group['source_landing_warning'] = 'Attachment author could not recover this destination. That is not current evidence of a broken or empty page.'
    if number in (2, 3, 6):
        group['routing_status'] = 'CONDITIONAL_ROOT_READBACK_REQUIRED'
        group['routing_requirement'] = 'Apply each Exact routing negative only after the corresponding receiving group and destination are active and fit to receive its intended traffic. Preserve campaign Paused while completing setup; no activation authority in this payload.'
        group['routing_condition_provenance'] = 'Explicit attachment instruction' if number in (2, 6) else 'Conservative consistent treatment of equivalent routing exclusions; root resolves from live evidence'
    else:
        group['routing_status'] = 'CATEGORY_SPECIFIC_EXCLUSION_OR_NO_GROUP_NEGATIVES'
    groups.append(group)

portuguese_negatives = keywords(between(source, 'A. Negativas em português — Frase', 'B. Complemento em inglês — Frase'))
english_negatives = keywords(between(source, 'B. Complemento em inglês — Frase', 'C. Restrições temporárias de catálogo — Exata'))
temporary_negatives = keywords(between(source, 'C. Restrições temporárias de catálogo — Exata', 'D. Termos que continuam condicionais'))
suffixes = re.findall(r'^utm_source=.+$', between(source, '12. Opções de URL e rastreamento', '13. Extensões em português'), re.M)
assert len(groups) == len(suffixes) == 8
for group, suffix in zip(groups, suffixes):
    group['tracking'] = {
        'status': 'CONDITIONAL_ROOT_READBACK_REQUIRED',
        'candidate_final_url_suffix': suffix.replace('dlm_ms_us_pt_search_202609', 'dlm_ms_br_pt_pt_search_202609'),
        'source_final_url_suffix': suffix,
        'tracking_template': None,
        'custom_parameters': None,
        'requirement': 'Use candidate only after root confirms manual UTM method, no duplicated automatic/inherited parameters, and copied lower-level suffix reconciliation. Null is a no-change placeholder, not an instruction to clear an existing field.',
    }

callouts = nonempty(between(source, 'Frases de destaque — uma por campo', 'Todas respeitam o limite'))
sitelink_lines = nonempty(between(source, 'Use a URL portuguesa do grupo correspondente. Não associe uma página que ainda precise ser validada.', 'Os textos respeitam os limites'))
assert len(sitelink_lines) == 32
sitelinks = []
for i in range(8):
    label, text, desc1, desc2 = sitelink_lines[4 * i:4 * i + 4]
    assert label == text
    sitelinks.append({'id': i + 1, 'text': text, 'description_1': desc1, 'description_2': desc2, 'final_url': groups[i]['final_url'], 'destination_status': 'LIVE_READBACK_REQUIRED'})
associations = between(source, 'Sitelinks para associar a cada grupo', 'Snippets estruturados')
snippet_lines = between(source, 'Grupo\tCabeçalho\tValores', '14. Extensões de imagem')
for group in groups:
    row = next(l for l in associations.splitlines() if l.startswith(group['name'] + '\t'))
    group['sitelink_texts'] = row.split('\t')[1].split('; ')
    row = next(l for l in snippet_lines.splitlines() if l.startswith(group['name'] + '\t'))
    _, header, values = row.split('\t')
    group['structured_snippet'] = {'header_display_portuguese': header, 'header_reference_english': 'Styles' if header == 'Estilos' else 'Types', 'values': values.split(' · ')}

# Keep all source rows but distinguish conditional routing from category exclusions.
routing = {2: [3] * 4 + [8] * 4 + [3] * 4 + [8] * 4,
           3: [5] * 3 + [8] * 3 + [5] + [8] * 3,
           6: ([1] * 3 + [4] * 3 + [7] * 3 + [8] * 2) * 2}
for group in groups:
    if group['number'] in routing:
        assert len(group['negative_keywords']) == len(routing[group['number']])
        for negative, recipient in zip(group['negative_keywords'], routing[group['number']]):
            negative['recipient_group'] = recipient
            negative['application_status'] = 'CONDITIONAL_ROOT_READBACK_REQUIRED'
    else:
        for negative in group['negative_keywords']:
            negative['application_status'] = 'SUPPLIED_CATEGORY_EXCLUSION_TARGET_GROUP_ONLY'
    group['nonconditional_negative_keywords'] = [k for k in group['negative_keywords'] if 'recipient_group' not in k]
    group['conditional_routing_negative_keywords'] = [k for k in group['negative_keywords'] if 'recipient_group' in k]

payload = {
    'artifact_type': 'LOCAL_REVIEW_PAYLOAD_NOT_LIVE_RECEIPT',
    'source': {'file': str(SOURCE), 'sha256': hashlib.sha256(source.encode()).hexdigest(), 'scope': 'User-pasted text only; referenced ZIP, Excel and image-caption assets were not supplied.'},
    'authority': {'account_id': '477439', 'customer_id': '770182', 'existing_campaign_id': None, 'target_identity_status': 'ROOT_NATIVE_READBACK_REQUIRED', 'live_writer': 'Root only', 'status_during_setup': 'Paused', 'budget': 'Preserve current root-verified target setting; do not infer or duplicate source budget', 'images': 'Preserve source images; do not invent captions or image mappings', 'activation': 'NOT_AUTHORIZED_BY_THIS_LOCAL_PAYLOAD'},
    'campaign': {
        'name': 'DLM | MS | BR & PT | PT | Search | 202609',
        'source_campaign_name': 'DLM | MS | US | EN | Search | 202609',
        'attachment_campaign_name_superseded': 'DLM | MS | US | PT | Search | 202609',
        'countries': ['Brazil', 'Portugal'],
        'language': 'Portuguese', 'copy_variant': 'Brazilian Portuguese as supplied', 'language_code': 'PT',
        'location_intent': 'People in your targeted locations', 'campaign_type': 'Search',
        'bidding': 'Preserve live-readback setting; no strategy or cap proposal',
        'campaign_negatives_portuguese_phrase': portuguese_negatives,
        'campaign_negatives_supplementary_english_phrase': english_negatives,
        'campaign_negatives_temporary_exact': temporary_negatives,
        'negative_list_scope': 'Exact target campaign only; never mutate lists shared with other campaigns',
        'conditional_terms_guidance': nonempty(between(source, 'Termo ou intenção\tTratamento', '12. Opções de URL e rastreamento')),
    },
    'groups': groups,
    'extensions': {'callouts': callouts, 'sitelinks': sitelinks, 'image_text_pairs': [], 'image_text_status': 'MISSING_SOURCE_160_REFERENCED_PAIRS', 'image_text_requirement': 'Obtain actual pairs/mapping or root inspect each copied image and existing caption before faithful localization. No image text fields validated by this extraction.'},
    'unresolved_inputs': [
        'Root exact target campaign native ID, state, copied entity IDs and full English asset inventory.',
        'All eight supplied /pt destinations require native language-menu verification; actual published Portuguese locale may be /pt-br.',
        'Root recipient-group/destination readiness for conditional routing negatives and all sitelinks.',
        'Root tagging inheritance and copied ad-level URL suffix readback.',
        '160 referenced image caption/alt pairs absent from attachment; no image mapping supplied.',
    ],
    'source_limitations': ['Brazilian Portuguese copy is supplied for both target markets; no separate Portugal lexicon or search-volume validation.', 'No new stock/size/shipping/mobile/checkout audit.', '17 temporary assortment Exact negatives preserve source restrictions without a fresh catalog audit.', 'No native account write, eligibility, performance, purchase or profitability proof.'],
}

counts = {
    'groups': len(groups), 'positive_keywords': sum(len(g['positive_keywords']) for g in groups),
    'headlines': sum(len(g['headlines']) for g in groups), 'descriptions': sum(len(g['descriptions']) for g in groups),
    'campaign_portuguese_phrase_negatives': len(portuguese_negatives), 'campaign_english_phrase_negatives': len(english_negatives),
    'campaign_temporary_exact_negatives': len(temporary_negatives), 'group_negatives': sum(len(g['negative_keywords']) for g in groups),
    'conditional_group_routing_negatives': sum(len(g['conditional_routing_negative_keywords']) for g in groups),
    'nonconditional_group_negatives': sum(len(g['nonconditional_negative_keywords']) for g in groups),
    'callouts': len(callouts), 'sitelinks': len(sitelinks), 'sitelink_group_associations': sum(len(g['sitelink_texts']) for g in groups),
    'structured_snippets': len(groups), 'image_pairs_available': 0,
}
expected = {'groups': 8, 'positive_keywords': 144, 'headlines': 120, 'descriptions': 32,
            'campaign_portuguese_phrase_negatives': 141, 'campaign_english_phrase_negatives': 86,
            'campaign_temporary_exact_negatives': 17, 'group_negatives': 76,
            'conditional_group_routing_negatives': 48, 'nonconditional_group_negatives': 28,
            'callouts': 6, 'sitelinks': 8, 'sitelink_group_associations': 32, 'structured_snippets': 8, 'image_pairs_available': 0}
assert counts == expected, (counts, expected)
length_errors, length_maxima, conflicts, duplicates, cross_group_duplicates = [], {}, [], [], []


def check_lengths(kind, values, limit):
    length_maxima[kind] = max(length_maxima.get(kind, 0), max(map(len, values), default=0))
    length_errors.extend({'field': kind, 'text': v, 'length': len(v), 'limit': limit} for v in values if len(v) > limit)


def normalize(value, fold_accents=False):
    value = ' '.join(value.casefold().split())
    return ''.join(c for c in unicodedata.normalize('NFD', value) if not unicodedata.combining(c)) if fold_accents else value


def detect_conflicts(fold_accents=False):
    hits = []
    for g in groups:
        for keyword in g['positive_keywords']:
            pos = normalize(keyword['text'], fold_accents)
            for scope, negative in [('campaign', n) for n in all_campaign_negatives] + [('own_group', n) for n in g['negative_keywords']]:
                neg = normalize(negative['text'], fold_accents)
                hit = pos == neg if negative['match_type'] == 'Exact' else (' ' + neg + ' ') in (' ' + pos + ' ')
                if hit:
                    hits.append({'group': g['number'], 'positive': keyword, 'negative': negative, 'negative_scope': scope})
    return hits


def check_duplicates(scope, values):
    for key, count in Counter((normalize(v['text']), v['match_type']) for v in values).items():
        if count > 1:
            duplicates.append({'scope': scope, 'text': key[0], 'match_type': key[1], 'count': count})


all_campaign_negatives = portuguese_negatives + english_negatives + temporary_negatives
for g in groups:
    assert len(g['headlines']) == 15 and len(g['descriptions']) == 4
    assert g['final_url'].startswith('https://www.dresslikemommy.com/pt/collections/')
    check_lengths('headlines', g['headlines'], 30)
    check_lengths('descriptions', g['descriptions'], 90)
    check_lengths('paths', [g['path_1'], g['path_2']], 15)
    check_lengths('snippet_values', g['structured_snippet']['values'], 25)
    check_lengths('keywords', [k['text'] for k in g['positive_keywords']], 100)
    check_duplicates(f"group_{g['number']}_positives", g['positive_keywords'])
    check_duplicates(f"group_{g['number']}_negatives", g['negative_keywords'])
    assert len(set(g['headlines'])) == 15 and len(set(g['descriptions'])) == 4
    assert len(g['sitelink_texts']) == len(set(g['sitelink_texts'])) == 4
    assert all(t in {s['text'] for s in sitelinks} for t in g['sitelink_texts'])
    assert 'dlm_ms_us_' not in g['tracking']['candidate_final_url_suffix']
    assert not g['tracking']['candidate_final_url_suffix'].startswith('?')
check_duplicates('campaign_negatives', all_campaign_negatives)
check_lengths('callouts', callouts, 25)
check_lengths('sitelink_titles', [s['text'] for s in sitelinks], 25)
check_lengths('sitelink_descriptions', [s[k] for s in sitelinks for k in ('description_1', 'description_2')], 35)
conflicts = detect_conflicts()
accent_fold_conflicts = detect_conflicts(True)
all_positive_rows = {}
for g in groups:
    for k in g['positive_keywords']:
        key = (normalize(k['text']), k['match_type'])
        all_positive_rows.setdefault(key, []).append(g['number'])
cross_group_duplicates = [{'text': key[0], 'match_type': key[1], 'groups': numbers} for key, numbers in all_positive_rows.items() if len(numbers) > 1]
preserved_values = callouts + [s[k] for s in sitelinks for k in ('text', 'description_1', 'description_2')]
preserved_values += [n['text'] for n in all_campaign_negatives]
for g in groups:
    preserved_values += [g['name'], g['final_url'], g['path_1'], g['path_2']]
    preserved_values += g['headlines'] + g['descriptions'] + g['structured_snippet']['values']
    preserved_values += [k['text'] for k in g['positive_keywords'] + g['negative_keywords']]
assert all(v in source for v in preserved_values)
assert not length_errors and not conflicts and not duplicates and not cross_group_duplicates and not accent_fold_conflicts
payload['validation'] = {
    'status': 'PASS_LOCAL_TEXT_ONLY', 'counts': counts, 'character_maxima': length_maxima,
    'character_limit_errors': length_errors, 'literal_positive_negative_conflicts': conflicts,
    'accent_folded_literal_positive_negative_conflicts': accent_fold_conflicts,
    'duplicate_text_match_rows': duplicates, 'cross_group_duplicate_positive_text_match_rows': cross_group_duplicates,
    'source_preserved_text_values': len(preserved_values),
    'method': 'Casefolded whitespace-normalized Exact equality or contiguous word-bounded Phrase containment against campaign and own-group negatives; repeated with accents removed as a sensitivity check. Exact/Phrase positive pairs are intentional.',
    'limits_basis': 'Attachment limits; no external policy/specification verification by this local worker.',
    'limitations': 'Does not reproduce Microsoft semantic or punctuation matching, account/shared negatives, eligibility, live routing or demand. No image captions available.',
}
(OUT / 'payload.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n')
(OUT / 'validation.json').write_text(json.dumps(payload['validation'], ensure_ascii=False, indent=2) + '\n')
rows = '\n'.join(f"| {g['number']} | {g['name']} | {len(g['positive_keywords'])} | {len(g['negative_keywords'])} | {len(g['conditional_routing_negative_keywords'])} |" for g in groups)
review = f'''# Portuguese campaign payload validation

Confidence: H for faithful text extraction and local checks; live state is unverified.

Target: `DLM | MS | BR & PT | PT | Search | 202609`, Brazil and Portugal, Portuguese. Current user geography supersedes the attachment's US market. Copy remains the supplied Brazilian Portuguese. Root owns exact native identity, permissions, browser work, current settings and all external writes. This payload grants no activation authority.

| Group | Portuguese name | Positives | Group negatives | Conditional routing subset |
|---|---|---:|---:|---:|
{rows}

Verified: 8 groups, 144 positive Exact/Phrase entries, 120 headlines (15 per group), 32 descriptions (4 per group), 244 campaign negatives (141 Portuguese Phrase + 86 supplemental English Phrase + 17 temporary Exact), 76 group negatives, 8 sitelinks with 32 group associations, 6 callouts and 8 snippets. All {len(preserved_values)} extracted text values are present unchanged in the supplied source. There are no same-text/same-match duplicate positive rows within or across groups, no duplicate negatives within their applied scope, and no literal positive-versus-campaign/own-group-negative conflicts. An accent-folded sensitivity check also finds zero conflicts.

Character maxima: headlines {length_maxima['headlines']}/30; descriptions {length_maxima['descriptions']}/90; paths {length_maxima['paths']}/15; callouts {length_maxima['callouts']}/25; sitelink titles {length_maxima['sitelink_titles']}/25; sitelink descriptions {length_maxima['sitelink_descriptions']}/35; snippet values {length_maxima['snippet_values']}/25. Limits follow the attachment. Brand, public URL slugs, tracking tokens and intentionally supplemental English negative keywords remain as supplied.

## Conditional items and exact gaps

- **All eight URLs need current verification.** Source `/pt/collections/…` paths are proposed only; the published locale may be `/pt-br`. Root must verify through the language menu and update ads, sitelinks and related destination associations consistently. The attachment specifically could not recover family-tops, swimsuits or family-sweaters. That historical limitation does not prove those pages broken or empty.
- **48 routing negatives are separated from 28 category exclusions.** Group 2 routes to 3/8; group 3 to 5/8; group 6 to 1/4/7/8. Source explicitly conditions groups 2/6 on recipient active/readiness. Group 3 is conservatively marked with the equivalent gate for root resolution. Keep Exact match, preserve the setup pause and do not transform these into broad category negatives. Category Phrase exclusions in 1/5/8 stay at their own group level.
- **Candidate tracking uses `dlm_ms_br_pt_pt_search_202609`.** Apply only after checking the real inherited/manual/automatic tagging method and copied ad-level suffixes. Null template/custom-parameter fields mean no proposed change, not clearing. Preserve `bing`, `cpc`, `{{AdId}}`, `{{Keyword}}`, and no initial `?` or `{{lpurl}}` in suffixes.
- **160 referenced image-caption/alt pairs are absent.** Zero image fields were available or validated. Preserve original images; obtain actual source pairs or inspect each existing image/caption before a faithful translation. Do not invent pictured people, clothing, colors or angles.
- The 17 temporary catalog Exact exclusions are source-preserved, not freshly stock-qualified. Brazilian and European Portuguese demand, native eligibility, shipping, stock, paired sizes, purchase measurement and profitability remain unverified. Never mutate lists/assets shared with another campaign while localizing the target.

Source SHA256: `{payload['source']['sha256']}`.

Files: `payload.json` contains the structured candidate and provenance; `validation.json` contains check results; `paste_blocks.txt` provides source-faithful UI text with conditional routing separately labeled; `extract_validate.py` reproduces all artifacts. No shared canonical files or external accounts changed by this worker. Root integrates verified findings into its own claim/worklog.

Reproduce: `python3 {OUT / 'extract_validate.py'}`.

Next action: root reconcile native copied objects and published Portuguese destinations before applying the candidate.
'''
(OUT / 'review.md').write_text(review)
paste = [payload['campaign']['name'], 'CAMPAIGN NEGATIVES — PHRASE PORTUGUESE + ENGLISH', render_keywords(portuguese_negatives + english_negatives), 'CAMPAIGN TEMPORARY CATALOG NEGATIVES — EXACT', render_keywords(temporary_negatives), 'CALLOUTS', '\n'.join(callouts)]
for g in groups:
    paste += [f"GROUP {g['number']}: {g['name']}", 'FINAL URL — UNVERIFIED SOURCE PATH', g['final_url'], 'PATH 1', g['path_1'], 'PATH 2', g['path_2'], 'POSITIVE KEYWORDS', render_keywords(g['positive_keywords']), 'HEADLINES', '\n'.join(g['headlines']), 'DESCRIPTIONS', '\n'.join(g['descriptions']), 'NONCONDITIONAL GROUP NEGATIVES', render_keywords(g['nonconditional_negative_keywords']) or '(none)', 'CONDITIONAL ROUTING NEGATIVES — DO NOT APPLY BEFORE RECIPIENT GATE', render_keywords(g['conditional_routing_negative_keywords']) or '(none)', 'CANDIDATE URL SUFFIX — TAGGING READBACK REQUIRED', g['tracking']['candidate_final_url_suffix'], 'SNIPPET HEADER', g['structured_snippet']['header_display_portuguese'], 'SNIPPET VALUES', '\n'.join(g['structured_snippet']['values'])]
paste += ['SITELINKS — ALL DESTINATIONS UNVERIFIED']
for s in sitelinks:
    paste += [s['text'], s['description_1'], s['description_2'], s['final_url']]
(OUT / 'paste_blocks.txt').write_text('\n\n'.join(paste) + '\n')
print(json.dumps({'counts': counts, 'character_maxima': length_maxima, 'conflicts': len(conflicts), 'accent_folded_conflicts': len(accent_fold_conflicts), 'duplicates': len(duplicates), 'source_preserved_text_values': len(preserved_values), 'output_directory': str(OUT)}, ensure_ascii=False, indent=2))
