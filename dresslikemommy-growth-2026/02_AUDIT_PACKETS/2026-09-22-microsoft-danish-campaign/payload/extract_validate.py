"""Extract the user-supplied Danish packet; local-only, no account operations."""
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

SOURCE = Path('/Users/fsuels/.codex/attachments/a344cc3d-d59d-4935-a7ce-9ed44882a3b9/Pasted text.txt')
OUT = Path(__file__).resolve().parent
source = SOURCE.read_text()


def between(text, first, last):
    return text.split(first, 1)[1].split(last, 1)[0]


def keywords(text):
    result = []
    for line in text.splitlines():
        line = line.strip()
        if line.startswith('[') and line.endswith(']'):
            result.append({'text': line[1:-1], 'match_type': 'Exact'})
        elif line.startswith('"') and line.endswith('"'):
            result.append({'text': line[1:-1], 'match_type': 'Phrase'})
    return result


def nonempty(text):
    return [line.strip() for line in text.strip().splitlines() if line.strip()]


groups = []
sections = list(re.finditer(r'^\d+\. Gruppe (\d+) — (.+)$', source, re.M))
for i, m in enumerate(sections):
    end = sections[i + 1].start() if i + 1 < len(sections) else source.index('11. Kampagnenegative')
    block = source[m.end():end]
    number = int(m[1])
    negatives_part = block.split('Negative søgeord', 1)[1]
    group = {
        'number': number,
        'name': m[2],
        'source_role_english': re.search(r'Samme rolle som (.+)\.', block)[1],
        'ad_group_type': 'Standard',
        'final_url': re.search(r'^https://\S+$', block, re.M)[0],
        'path_1': re.search(r'^Path 1: (.+)$', block, re.M)[1],
        'path_2': re.search(r'^Path 2: (.+)$', block, re.M)[1],
        'positive_keywords': keywords(between(block, 'Positive søgeord', 'Overskrifter')),
        'headlines': nonempty(between(block, 'Overskrifter', 'Beskrivelser').removeprefix(' — én linje pr. felt')),
        'descriptions': nonempty(between(block, 'Beskrivelser', 'Negative søgeord').removeprefix(' — én linje pr. felt')),
        'negative_keywords': keywords(negatives_part),
        'source_negative_guidance': nonempty('\n'.join(l for l in negatives_part.splitlines()[1:] if not l.startswith(('"', '[')))),
        'pins': None,
        'landing_status': 'LIVE_READBACK_REQUIRED',
    }
    if number in (3, 8):
        group['source_landing_warning'] = 'Source author could not verify this destination; no claim of defect or readiness.'
    if number in (4, 7):
        group['source_landing_warning'] = 'Source author reported English text and missing-translation notice; current readback required.'
    if number in (2, 3, 6):
        group['routing_status'] = 'CONDITIONAL_DO_NOT_APPLY_BLINDLY'
        group['routing_requirement'] = 'Apply each routing negative only after root verifies the corresponding receiving group and destination can receive the intended traffic. Campaign remains paused; no launch authority.'
        group['routing_condition_provenance'] = 'Explicit attachment condition' if number != 3 else 'Conservative consistency with attachment routing conditions; root must decide from live evidence'
    else:
        group['routing_status'] = 'Source category exclusion or no group negatives'
    groups.append(group)

campaign_negatives = keywords(between(source, 'Danske kampagnenegativer — Phrase', 'Supplerende engelske kampagnenegativer — Phrase'))
english_negatives = keywords(between(source, 'Supplerende engelske kampagnenegativer — Phrase', 'Midlertidige sortimentsbegrænsninger — Exact'))
temporary_negatives = keywords(between(source, 'Midlertidige sortimentsbegrænsninger — Exact', 'Ord, der ikke automatisk skal blokeres'))
suffixes = re.findall(r'^utm_source=.+$', between(source, '12. URL-sporing', '13. Danske annonceudvidelser'), re.M)
assert len(groups) == len(suffixes)
for group, suffix in zip(groups, suffixes):
    group['tracking'] = {
        'status': 'CONDITIONAL_ROOT_READBACK_REQUIRED',
        'candidate_final_url_suffix': suffix.replace('dlm_ms_us_da_search_202609', 'dlm_ms_dk_da_search_202609'),
        'source_final_url_suffix': suffix,
        'tracking_template': None,
        'custom_parameters': None,
        'requirement': 'Use only if root verifies manual UTM tagging is the existing method, no duplicate automatic/inherited tags, and copied ad-level suffixes are reconciled. Null means no change proposed, not an instruction to clear an existing field.',
    }

callouts = nonempty(between(source, 'Callouts — én linje pr. felt', 'Alle seks er kontrolleret'))
sitelink_lines = nonempty(between(source, 'For eksempel bruger sitelinket til nattøj samme URL som gruppe 4.', 'Sitelinktitler og beskrivelser'))
assert len(sitelink_lines) == 32
sitelinks = []
for i in range(8):
    label, text, desc1, desc2 = sitelink_lines[4*i:4*i+4]
    assert label == text
    sitelinks.append({'id': i+1, 'text': text, 'description_1': desc1, 'description_2': desc2, 'final_url': groups[i]['final_url'], 'destination_status': 'LIVE_READBACK_REQUIRED'})
associations = between(source, 'Tilknytning til grupperne', 'Tilknyt ikke de endnu uverificerede')
snippet_lines = between(source, 'Gruppe\tOverskrift\tVærdier', '14. Billedudvidelser')
for group in groups:
    row = next(l for l in associations.splitlines() if l.startswith(group['name']+'\t'))
    group['sitelink_texts'] = row.split('\t')[1].split('; ')
    row = next(l for l in snippet_lines.splitlines() if l.startswith(group['name']+'\t'))
    _, header, values = row.split('\t')
    group['structured_snippet'] = {'header_display_danish': header, 'header_reference_english': 'Styles' if header == 'Design' else 'Types', 'values': values.split(' · ')}

# Record routing recipients per row, preserving exact supplied text/match.
routing = {2: [3]*4 + [8]*4, 3: [5]*3 + [8]*3, 6: [1]*3 + [4]*3 + [7]*3 + [8]*2}
for group in groups:
    if group['number'] in routing:
        assert len(group['negative_keywords']) == len(routing[group['number']])
        for negative, recipient in zip(group['negative_keywords'], routing[group['number']]):
            negative['recipient_group'] = recipient
            negative['application_status'] = 'CONDITIONAL_ROOT_READBACK_REQUIRED'

payload = {
    'artifact_type': 'LOCAL_REVIEW_PAYLOAD_NOT_LIVE_RECEIPT',
    'source': {'file': str(SOURCE), 'sha256': hashlib.sha256(source.encode()).hexdigest(), 'scope': 'User-pasted text only; linked ZIP/Excel/image-caption assets were not supplied.'},
    'authority': {'account_id': '477439', 'customer_id': '770182', 'existing_campaign_id': '506254908', 'live_writer': 'Root only', 'status': 'Paused', 'budget': 'Preserve observed 3.00 and currency/budget period; root readback required', 'images': 'Preserve existing images; no image selection or caption invention'},
    'campaign': {'name': 'DLM | MS | DK | DA | Search | 202609', 'country': 'Denmark', 'language': 'Danish', 'language_code': 'DA', 'location_intent': 'People in your targeted locations', 'campaign_type': 'Search', 'bidding': 'Preserve current live-readback settings; no strategy or cap change', 'campaign_negatives_danish_phrase': campaign_negatives, 'campaign_negatives_supplementary_english_phrase': english_negatives, 'campaign_negatives_temporary_exact': temporary_negatives, 'negative_list_scope': 'Campaign 506254908 only; never mutate shared lists used by other campaigns'},
    'groups': groups,
    'extensions': {'callouts': callouts, 'sitelinks': sitelinks, 'image_text_pairs': [], 'image_text_status': 'MISSING_SOURCE_160_REFERENCED_PAIRS', 'image_text_requirement': 'Obtain supplied ZIP/text pairs or root inspect each actual copied image and existing caption before faithful image-specific Danish localization; do not claim all320fields validated.'},
    'unresolved_inputs': [
        '160 image Name/Display Text and Image Alt Text pairs referenced by attachment are absent; no supplied ZIP or working download links.',
        'Root live inventory of copied ad/group IDs, English text assets and associations, positive/negative keywords, campaign settings and inherited/shared assets.',
        'Root current destination and recipient-group readiness for conditional routing negatives and sitelinks, especially family-tops and family-sweaters.',
        'Root current tracking template/suffix/custom parameter/automatic-tagging readback before applying candidate DK UTMs.',
    ],
    'source_limitations': ['No verified Danish Keyword Planner volume/CPC evidence.', 'No full stock/size/mobile/checkout test in attachment.', 'No live Microsoft writes or approvals proved by attachment.', 'No current performance or profitability claims.'],
}

counts = {
    'groups': len(groups), 'positive_keywords': sum(len(g['positive_keywords']) for g in groups),
    'headlines': sum(len(g['headlines']) for g in groups), 'descriptions': sum(len(g['descriptions']) for g in groups),
    'campaign_danish_phrase_negatives': len(campaign_negatives), 'campaign_english_phrase_negatives': len(english_negatives),
    'campaign_temporary_exact_negatives': len(temporary_negatives), 'group_negatives': sum(len(g['negative_keywords']) for g in groups),
    'callouts': len(callouts), 'sitelinks': len(sitelinks), 'structured_snippets': len(groups), 'image_pairs_available': 0,
}
expected = {'groups': 8, 'positive_keywords': 144, 'headlines': 120, 'descriptions': 32, 'campaign_danish_phrase_negatives': 112, 'campaign_english_phrase_negatives': 80, 'campaign_temporary_exact_negatives': 9, 'group_negatives': 45, 'callouts': 6, 'sitelinks': 8, 'structured_snippets': 8, 'image_pairs_available': 0}
assert counts == expected, (counts, expected)
length_errors = []
length_maxima = {}


def check_lengths(kind, values, limit):
    length_maxima[kind] = max(length_maxima.get(kind, 0), max(map(len, values), default=0))
    length_errors.extend({'field': kind, 'text': v, 'length': len(v), 'limit': limit} for v in values if len(v) > limit)


all_campaign_negatives = campaign_negatives + english_negatives + temporary_negatives
conflicts = []
duplicates = []
for g in groups:
    assert len(g['headlines']) == 15 and len(g['descriptions']) == 4
    assert g['final_url'].startswith('https://www.dresslikemommy.com/da/collections/')
    check_lengths('headlines', g['headlines'], 30)
    check_lengths('descriptions', g['descriptions'], 90)
    check_lengths('paths', [g['path_1'], g['path_2']], 15)
    check_lengths('snippet_values', g['structured_snippet']['values'], 25)
    for keyword in g['positive_keywords']:
        positive = keyword['text'].casefold()
        for neg in all_campaign_negatives + g['negative_keywords']:
            negative = neg['text'].casefold()
            hit = positive == negative if neg['match_type'] == 'Exact' else (' '+negative+' ') in (' '+positive+' ')
            if hit:
                conflicts.append({'group': g['number'], 'positive': keyword, 'negative': neg})
    for kind in ('positive_keywords', 'negative_keywords'):
        duplicates.extend({'group': g['number'], 'kind': kind, 'text_match': key, 'count': n} for key, n in Counter((x['text'].casefold(), x['match_type']) for x in g[kind]).items() if n > 1)
    assert set(g['sitelink_texts']).issubset({s['text'] for s in sitelinks})
check_lengths('callouts', callouts, 25)
for s in sitelinks:
    check_lengths('sitelink_titles', [s['text']], 25)
    check_lengths('sitelink_descriptions', [s['description_1'], s['description_2']], 35)
assert not length_errors, length_errors
assert not conflicts, conflicts
assert not duplicates, duplicates
preserved_values = list(callouts)
for g in groups:
    preserved_values += g['headlines'] + g['descriptions'] + [g['name'], g['final_url'], g['path_1'], g['path_2']]
    preserved_values += [r['text'] for r in g['positive_keywords'] + g['negative_keywords']]
    preserved_values += g['structured_snippet']['values']
preserved_values += [n['text'] for n in all_campaign_negatives]
for s in sitelinks:
    preserved_values += [s['text'], s['description_1'], s['description_2']]
assert all(value in source for value in preserved_values)
payload['local_validation'] = {
    'counts': counts, 'length_maxima': length_maxima, 'length_errors': length_errors,
    'source_preserved_text_values': len(preserved_values),
    'literal_positive_vs_own_group_and_campaign_negative_conflicts': conflicts, 'duplicate_text_match_within_group': duplicates,
    'conflict_check_method': 'Casefolded exact equality for Exact negatives and contiguous whitespace-bounded literal phrase containment for Phrase negatives against supplied positive text. Does not simulate Microsoft semantic matching, spelling/punctuation expansion, account/shared negatives or live auction routing.',
    'limits_basis': 'Limits quoted in user attachment; no new external specification verification performed by bounded local worker.',
    'status': 'PASS_LOCAL_TEXT_ONLY',
}
(OUT/'payload.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2)+'\n')
rows = '\n'.join(f"| {g['number']} | {g['name']} | {len(g['positive_keywords'])} | {len(g['negative_keywords'])} | {g['routing_status']} |" for g in groups)
review = f'''# Danish campaign payload review

LOCAL REVIEW PAYLOAD — no external writes or live verification by this worker.

Target: account 477439/customer 770182, existing campaign 506254908 → `DLM | MS | DK | DA | Search | 202609`, Denmark/Danish. Preserve Paused, observed 3.00 budget, bidding and images. Root owns live readback, exact approval scope and all writes. The current user's DK decision supersedes the attachment's US geography; no new campaign or launch is proposed here.

Source: `{SOURCE}`. SHA256 `{payload['source']['sha256']}`.

| Group | Danish name | Positive entries | Group negatives | Routing condition |
|---|---|---:|---:|---|
{rows}

Verified locally: 8 groups, 144 positive entries, 120 headlines (15 each), 32 descriptions (4 each), 192 campaign Phrase negatives (112 Danish + 80 supplementary English), 9 temporary Exact negatives, 45 group negatives, 8 sitelinks, 6 callouts and 8 structured snippets. All supplied text fields pass attachment limits; maximum headline {length_maxima['headlines']}/30, description {length_maxima['descriptions']}/90, path {length_maxima['paths']}/15, callout {length_maxima['callouts']}/25, sitelink title {length_maxima['sitelink_titles']}/25, sitelink description {length_maxima['sitelink_descriptions']}/35. Zero literal positive-versus-own-group/campaign-negative conflicts and zero duplicate same-text/same-match rows within a group. Exact and Phrase pairs are intentional. All {len(preserved_values)} extracted customer-facing text values occur unchanged in the supplied source.

## Conditions root must resolve

- Group 2 negatives route to 3/8; group 3 to 5/8; group 6 to 1/4/7/8. Preserve Exact match. Apply each only after corresponding recipient readiness is verified. Attachment explicitly conditions 2/6; the same gate is conservatively marked for 3. Source category-specific Phrase exclusions in 1/5/8 must stay at group level. No broad category negatives are introduced.
- Candidate UTMs use `dlm_ms_dk_da_search_202609`. Do not apply before root confirms manual tagging/no duplicate inherited or automatic tags and checks copied ad-level suffixes. Null templates/custom parameters are no-change placeholders, not clearing instructions. Never translate `bing`, `cpc`, `{{AdId}}` or `{{Keyword}}`.
- Every URL is supplied `/da/collections/…` text, not current endpoint evidence. Source author could not verify family-tops/family-sweaters and reported mixed English on pajamas/swimsuits. Current public verification may supersede those historical warnings. Do not attach unverified sitelink destinations.
- 192 campaign Phrase negatives intentionally include 80 supplementary English entries; group-level shirt/swim/sweater English exclusions also remain. These are relevant exclusions, not untranslated positive targeting. Do not alter another campaign's shared assets or lists.
- Brand `Dress Like Mommy`, established Danish loanwords such as T-shirts/outfits, URL slugs and tracking tokens are preserved as supplied; source copy is faithfully extracted, not rewritten.

## Exact missing inputs

1. The 160 image Name/Display Text and Alt Text pairs are referenced but not present; no ZIP, download URL or image mapping was supplied. Zero of these 320 fields was validated. Root may obtain missing pairs or inspect actual copied images/captions for faithful Danish translation; never infer pictured people/garments.
2. Root native inventory/readback of copied IDs, current names/text, all inherited/shared assets and keyword/negative/settings state.
3. Root destination and recipient readiness evidence, and tagging readback as above.

No Keyword Planner demand/CPC, performance, eligibility, purchases or profit are established. Matching validation is literal and cannot reproduce Microsoft's full matching or account-level negatives. The 9 temporary assortment Exact negatives are preserved from source, not freshly stock-qualified.

Reproduce local extraction and checks: `python3 {OUT/'extract_validate.py'}`.
Machine-readable content: `payload.json`. No canonical files changed by worker; root integrates its own state/claim/worklog.
'''
(OUT/'review.md').write_text(review)
print(json.dumps({'counts': counts, 'length_maxima': length_maxima, 'conflicts': len(conflicts), 'duplicates': len(duplicates), 'files': [str(OUT/'payload.json'), str(OUT/'review.md')]}, ensure_ascii=False, indent=2))
