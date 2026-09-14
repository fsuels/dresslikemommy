"""Render a bounded, local semantic review. Never writes the source campaign package."""
from pathlib import Path
from collections import Counter
import csv
import datetime
import hashlib
import json
import re
import unicodedata

HERE = Path(__file__).resolve().parent
PACKET = HERE.parent
EXPECTED = {
    'campaign_plan.md': '1617edecc07323215c080245930d051a8e5e7017fdc216d20f73d4cf843a58f0',
    'negative_keywords.csv': '6594c5ae6404228f8da10b605151592ee56f8c97e8901f0e07439cbee54de839',
    'keywords.csv': '658a8fef354ae4a299b2692d0dfda50f8c08a9d5f0c2d4fceb0c78351e53e94e',
    'ad_groups.csv': '448a80f4b78fd0fdc5f94a557e2c512f0959f7d2390743923e4f365eb6b868d8',
    'responsive_search_ads.csv': '0f8e442dbc8e7d5fc8e5424892ee4a357bf412edd0afdf843eac04c97f000eaa',
    'campaigns.csv': 'a2176510931436bb5a941fe6a986eac1bdd00d15b890aa80d499e8738ffb651e',
    'microsoft_deployed_app_pixel.js': 'bdf85b114cb9d9ef5c790dee198f38dd8032c46bc13bdf7ca9f4ee034abc7f29',
    'microsoft_deployed_storefront_script.js': '171802eab48befd7660099e6ad8c6d0423c14bfeb2b866b14b30694d7f7bce3a',
    'launch-plan-20260911/shopify_candidate_readback.json': '53716ee712fbbb7f3ca187ffdf8176ecf7503cbf9e3de82e8f9f39874a1e393d',
    'launch-plan-20260911/launch_contract.json': '06c9a560060b9d46048b50d5ee829a538d2512ed7f8cad39be718c523a8181b1',
}

def verify_sources():
    for name, expected in EXPECTED.items():
        assert hashlib.sha256((PACKET / name).read_bytes()).hexdigest() == expected, name

def read_csv(name):
    with (PACKET / name).open(newline='') as f:
        return list(csv.DictReader(f))

verify_sources()
negatives = read_csv('negative_keywords.csv')
positives = read_csv('keywords.csv')
groups = {r['ad_group_key']: r for r in read_csv('ad_groups.csv')}
ads = {r['ad_group_key']: r for r in read_csv('responsive_search_ads.csv')}
campaigns = {r['campaign_key']: r for r in read_csv('campaigns.csv')}
product_receipt = json.loads((PACKET / 'launch-plan-20260911/shopify_candidate_readback.json').read_text())
published = {r['locale'] for r in product_receipt['data']['shopLocales'] if r['published']}

# Explicit adjudications refer to CSV line numbers in the frozen negative file.
# They are local review keys, never Microsoft object IDs.
QUALIFIED_LINES = {
    6, 7, 8, 9, 10, 11,
    25, 26, 27, 28, 42, 43, 44, 45,
    57, 58, 59, 61, 62,
    74, 76, 77, 78, 79,
    91, 92, 93, 94, 95, 96,
    108, 109, 110, 111, 112, 113,
    129, 130, 143, 144, 145, 146,
    158, 159, 160, 161, 162, 163,
}
REJECTED_LINES = {23, 24, 40, 41, 55, 60, 75, 125, 126, 127, 128}
SHIRT_TERMS = {'t shirt', 't shirts', 'camiseta', 'camisetas', 'maglietta', 'magliette', 'tričko', 'trička', 'tricou', 'tricouri'}
SWIM_TERMS = {'swimsuit', 'bañador', 'maillot', 'badeanzug', 'badedragt', 'badpak', 'costume da bagno', 'plavky', 'costum de baie'}
SLEEP_TERMS = {'pajamas', 'pijama', 'pyjama', 'schlafanzug', 'pyjamas', 'pigiama', 'pyžamo'}
CUSTOM_TERMS = {
    'personalized', 'custom printed', 'personalizada', 'personalizadas',
    'personnalisé', 'personnalisés', 'personalisiert', 'bedrucken',
    'personlig tekst', 'tryk selv', 'gepersonaliseerd', 'bedrukken',
    'personalizzate', 'vlastní potisk', 'se jménem', 'personalizat', 'personalizate',
}
GLOSSES = {
    'personalized': 'personalized / made for a person', 'custom printed': 'custom printing',
    'personalizada': 'personalized, feminine singular', 'personalizadas': 'personalized, feminine plural',
    'personnalisé': 'personalized, masculine singular', 'personnalisés': 'personalized, masculine plural',
    'personalisiert': 'personalized', 'bedrucken': 'to print on',
    'personlig tekst': 'personal text', 'tryk selv': 'print yourself',
    'gepersonaliseerd': 'personalized', 'bedrukken': 'to print on',
    'personalizzate': 'personalized, feminine plural', 'vlastní potisk': 'own/custom print',
    'se jménem': 'with a name', 'personalizat': 'personalized, masculine/neuter singular',
    'personalizate': 'personalized, feminine/neuter plural',
}
LEXICAL = {
    'maillot': ('Jersey/top as well as swimwear; the bare noun is not a precise swimsuit exclusion.', 'https://www.larousse.fr/dictionnaires/francais/maillot/48685', 'Review maillot de bain separately if swimwear exclusion is warranted; not added here.'),
    'kleider': ('Plural can mean clothes generally, so it can suppress coordinated family-clothing intent relevant to tees.', 'https://www.duden.de/rechtschreibung/Kleid', 'Use a complete observed dress-specific query if later evidence warrants an exclusion.'),
    'vestido': ('Can denote clothing/an outfit generally, not only a dress; too broad for generic family-look searches.', 'https://dle.rae.es/vestido', 'Review complete dress-specific queries; do not exclude this bare word.'),
    'vestidos': ('Can denote clothing/outfits generally; a bare-word exclusion can remove relevant family-outfit intent.', 'https://dle.rae.es/vestido', 'Review complete dress-specific queries; do not exclude this bare word.'),
    'abito': ('Generic clothing/outfit meaning is broader than a dress-only purchase.', 'https://www.treccani.it/vocabolario/abito/', 'Review a complete dress-specific query; retain generic coordinated-clothing intent.'),
    'abiti': ('Plural clothing/outfits meaning is broader than dresses and can include family clothing.', 'https://www.treccani.it/vocabolario/abito/', 'Review a complete dress-specific query; retain generic coordinated-clothing intent.'),
    'vestito': ('Can denote an outfit or garment generally; it is not reliably a dress-only exclusion.', 'https://www.treccani.it/vocabolario/vestito/', 'Review a complete dress-specific query; retain generic coordinated-clothing intent.'),
    'vestiti': ('Plural commonly denotes clothes generally; excluding it would also restrict relevant apparel intent.', 'https://www.treccani.it/vocabolario/vestito/', 'Review a complete dress-specific query; retain generic coordinated-clothing intent.'),
}

def tokens(s):
    # A conservative local collision screen, NOT Microsoft's normalization engine.
    return re.findall(r'[^\W_]+', unicodedata.normalize('NFKC', s).casefold(), flags=re.UNICODE)

def contiguous(needle, haystack):
    a, b = tokens(needle), tokens(haystack)
    return any(b[i:i + len(a)] == a for i in range(len(b) - len(a) + 1))

def ordered(needle, haystack):
    it = iter(tokens(haystack))
    return all(any(x == term for x in it) for term in tokens(needle))

rows = []
for line, source in enumerate(negatives, 2):
    if source['local_state'] != 'HOLD_SEMANTIC_REVIEW':
        continue
    group = groups[source['ad_group_key']]
    campaign = campaigns[source['campaign_key']]
    ad = ads[source['ad_group_key']]
    term = source['negative_keyword']
    assert source['scope'] == 'AdGroup' and source['match_type'] == 'Phrase'
    assert campaign['shopify_locale'] in published
    assert ad['final_url'] == group['final_url']
    decision = 'QUALIFIED_LOCAL_SEED' if line in QUALIFIED_LINES else 'REJECT' if line in REJECTED_LINES else 'KEEP_HELD'
    dictionary_url = ''
    safer_direction = ''
    if decision == 'REJECT':
        reason, dictionary_url, safer_direction = LEXICAL[term]
        category = 'AMBIGUOUS_GARMENT_WORD'
        evidence = 'Dictionary meaning supports rejecting the current bare phrase; any replacement needs its own query/scope review.'
    elif group['intent'] == 'dresses':
        assert decision == 'KEEP_HELD'
        if term in SHIRT_TERMS:
            category = 'SHIRT_OR_MIXED_DRESS_INTENT'
            reason = f'"{term}" can occur in shirt-dress or mixed matching-garment intent. The landing is the broad Mommy-and-Me collection, not a fully reviewed dress-only offer allowlist.'
            evidence = 'Current qualified collection assortment plus complete search-query context; explicitly exclude shirt-dress/mixed looks before reconsidering this phrase.'
        elif term in SWIM_TERMS:
            category = 'SWIM_OR_COVERUP_SCOPE_UNRESOLVED'
            reason = f'"{term}" points to swimwear, but the collection has no reviewed exclusion of matching swim-dress/cover-up intent. Two product samples cannot establish the full assortment.'
            evidence = 'Complete qualified collection/offer scope and actual query context separating swimwear from cover-ups or dress comparisons.'
        elif term in SLEEP_TERMS:
            category = 'SLEEP_OR_NIGHTDRESS_SCOPE_UNRESOLVED'
            reason = f'"{term}" signals sleepwear, but exclusion of matching nightdress/sleepwear intent from the broad collection has not been qualified.'
            evidence = 'Confirm a dress-only qualified offer set excluding nightdress/sleepwear; prefer a complete observed irrelevant query if exclusion is needed.'
        else:
            raise AssertionError((line, term))
    elif term == 'šaty':
        assert decision == 'KEEP_HELD'
        category = 'CZECH_CLOTHING_CONTEXT_UNRESOLVED'
        reason = 'Dress versus broader clothing usage needs contextual review; do not infer a safe bare-word exclusion merely from the English group label.'
        evidence = 'Czech query-context or qualified linguistic review distinguishing dress intent from coordinated clothing; no native-language certification performed.'
    else:
        assert decision == 'QUALIFIED_LOCAL_SEED'
        assert 'sunshine-stripe-family-matching-tops' in group['final_url']
        if term in CUSTOM_TERMS:
            category = 'CUSTOMIZATION_SERVICE_OUTSIDE_FIXED_TEE_OFFER'
            reason = f'"{term}" ({GLOSSES[term]}) requests customization/printing intent. The reviewed ad and fixed Sunshine Stripe size/variant offer promise a finished tee, not that service.'
            evidence = 'Root local semantic review of this exact tee-only scope. Recheck if a customization offer or buyer flow is introduced; current conversion performance is unknown.'
        elif term in SWIM_TERMS:
            category = 'SWIMWEAR_OUTSIDE_FIXED_TEE_OFFER'
            reason = f'"{term}" requests swimwear; the exact Sunshine Stripe landing/ad sells a separate striped tee, not a swimming garment.'
            evidence = 'Keep this exclusion confined to the fixed Sunshine tee group. Re-review if the landing or promoted garment changes; no poor-query-performance claim.'
        elif term in SLEEP_TERMS:
            category = 'SLEEPWEAR_OUTSIDE_FIXED_TEE_OFFER'
            reason = f'"{term}" requests a sleepwear offer; this fixed tee ad/PDP does not promise pajamas or a sleepwear set.'
            evidence = 'Keep this exclusion confined to the finished Sunshine tee offer, not site-wide sleepwear. Root should inspect actual query mixtures after any serving.'
        else:
            category = 'DRESS_INTENT_OUTSIDE_FIXED_TEE_OFFER'
            reason = f'"{term}" denotes dress intent rather than the fixed separate Sunshine tee. An ad-group-only negative can separate those offers without excluding the dress group.'
            evidence = 'Preserve exact ad-group scope. Inspect complete mixed-outfit queries if observed; do not copy this negative to the campaign or shared list.'
    own = [r for r in positives if r['ad_group_key'] == source['ad_group_key']]
    cross = [r for r in positives if r['campaign_key'] == source['campaign_key'] and r['ad_group_key'] != source['ad_group_key']]
    literal_hits = [r['keyword_key'] for r in own if contiguous(term, r['keyword'])]
    ordered_hits = [r['keyword_key'] for r in own if ordered(term, r['keyword'])]
    cross_hits = [r['keyword_key'] for r in cross if contiguous(term, r['keyword'])]
    language_note = 'Model semantic review in the stated campaign language; no native-speaker certificate or automatic singular/plural, accent, hyphen or compound coverage inferred.'
    if campaign['country_code'] == 'US' and campaign['shopify_locale'] == 'es' and term == 'bañador':
        language_note += ' For U.S. Spanish, evaluate traje de baño as separate query wording if observed; no synonym was added.'
    elif campaign['country_code'] == 'AU' and term == 'pajamas':
        language_note += ' Australian pyjamas spelling needs its own query review; this original pajamas row is not assumed to cover it.'
    elif term in {'personalizzate', 'personalizada', 'personalizadas', 'personnalisé', 'personnalisés', 'personalizat', 'personalizate'}:
        language_note += ' Preserve the supplied gender/number form as its own proposal; unlisted inflections were not silently added.'
    elif term in {'t shirt', 't shirts'}:
        language_note += ' Local screening folds the hyphen to a token boundary; native treatment of T-shirt forms and compounds remains untested.'
    identity = {k: source[k] for k in ['campaign_key', 'ad_group_key', 'scope', 'negative_keyword', 'match_type']}
    key = 'local_neg_' + hashlib.sha256(json.dumps(identity, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:16]
    rows.append({
        'local_negative_key': key,
        'source_csv_line': line,
        **identity,
        'country_code': campaign['country_code'],
        'shopify_locale': campaign['shopify_locale'],
        'language_context_note': language_note,
        'group_intent': group['intent'],
        'decision': decision,
        'semantic_category': category,
        'rationale': reason,
        'evidence_needed_or_recheck_trigger': evidence,
        'dictionary_url': dictionary_url,
        'safer_direction_not_added': safer_direction,
        'same_group_literal_keyword_keys': ';'.join(literal_hits),
        'same_group_ordered_token_warning_keys': ';'.join(ordered_hits),
        'other_group_literal_keyword_keys_if_wrongly_upscoped': ';'.join(cross_hits),
        'ad_key': ad['ad_key'],
        'final_url': group['final_url'],
        'original_local_state': source['local_state'],
        'original_local_staging_state': source['local_staging_state'],
        'review_execution_state': 'LOCAL_REVIEW_ONLY_NOT_AN_IMPORT',
        'native_language_certification': 'NOT_PERFORMED',
        'query_performance_evidence': 'NONE_REVIEWED_NO_CPC_CPA_INFERENCE',
        'product_receipt_as_of_utc': product_receipt['as_of_utc'],
        'initial_dress_stage_eligible': 'false',
    })

assert len(negatives) == 180 and len(rows) == 103
assert len({r['local_negative_key'] for r in rows}) == 103
assert {r['source_csv_line'] for r in rows if r['decision'] == 'QUALIFIED_LOCAL_SEED'} == QUALIFIED_LINES
assert {r['source_csv_line'] for r in rows if r['decision'] == 'REJECT'} == REJECTED_LINES
assert not any(r['same_group_literal_keyword_keys'] or r['same_group_ordered_token_warning_keys'] for r in rows)
assert all(r['group_intent'] == 'tees' for r in rows if r['decision'] == 'QUALIFIED_LOCAL_SEED')
priority_campaigns = ['ms_us_en_202609', 'ms_de_de_202609']
priority = sorted([r for r in rows if r['campaign_key'] in priority_campaigns], key=lambda r: (priority_campaigns.index(r['campaign_key']), r['source_csv_line']))
qualified = [r for r in rows if r['decision'] == 'QUALIFIED_LOCAL_SEED']
assert len(priority) == 20 and len(qualified) == 48

def write_csv(name, content):
    with (HERE / name).open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(content)

write_csv('us_germany_priority.csv', priority)
write_csv('negative_review.csv', rows)
write_csv('qualified_local_seeds.csv', qualified)
verify_sources()
counts = dict(Counter(r['decision'] for r in rows))
priority_counts = dict(Counter(r['decision'] for r in priority))
by_campaign = {key: dict(Counter(r['decision'] for r in rows if r['campaign_key'] == key)) for key in campaigns}
receipt = {
    'reviewed_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'status': 'PASS_LOCAL_SEMANTIC_REVIEW__ROOT_REVIEW_BEFORE_CANDIDATE_EDITS',
    'input_hashes_verified_before_and_after': EXPECTED,
    'counts': {'source_negatives': 180, 'held_reviewed': 103, 'untouched_existing_proposals': 77, 'decisions': counts, 'us_en_germany_de_priority': priority_counts, 'by_campaign': by_campaign},
    'scope': {'browser_account_or_shopify_writes': 0, 'canonical_or_original_csv_edits': 0, 'campaign_scope_promotions': 0, 'qualified_new_negatives_for_minimal_dress_stage': 0, 'qualified_tee_reserve_rows': 48},
    'validation': {'unique_source_keys': 103, 'exact_source_row_coverage': True, 'same_group_literal_collisions': 0, 'same_group_ordered_token_warning_collisions': 0, 'qualified_rows_stay_ad_group_only': True, 'all_qualified_rows_target_exact_sunshine_pdp': True, 'all_reviewed_locales_published_in_frozen_receipt': True, 'native_language_certification': False},
    'upscope_warning': {'rows_with_literal_sibling_positive_conflicts': sum(bool(r['other_group_literal_keyword_keys_if_wrongly_upscoped']) for r in rows), 'qualified_rows_with_literal_sibling_positive_conflicts': sum(bool(r['other_group_literal_keyword_keys_if_wrongly_upscoped']) for r in qualified), 'meaning': 'Counterfactual local text screen only: these conflicts matter if an AdGroup exclusion is wrongly promoted to Campaign/shared scope.'},
    'decisions_defined': {'QUALIFIED_LOCAL_SEED': 'Semantically defensible local proposal for the exact fixed tee ad-group offer; not a performance finding, native-language certificate, import acceptance or new campaign scope.', 'KEEP_HELD': 'A specific assortment or linguistic-context gap remains; do not promote the original row.', 'REJECT': 'Reject this wording and scope as proposed because a documented broader meaning can exclude relevant garment intent; replacement suggestions are not added.'},
    'screen_limits': 'NFKC/casefold/punctuation-token comparison, retaining accents, plus a conservative ordered-token warning. This is not Microsoft serving/normalization emulation, has no query logs, and does not certify close-variant behavior. Zero static collisions is not proof of no future buyer loss.',
    'primary_sources': [
        'https://learn.microsoft.com/en-us/advertising/guides/negative-keywords?view=bingads-13',
        'https://learn.microsoft.com/en-us/advertising/campaign-management-service/negativekeyword?view=bingads-13',
        'https://www.larousse.fr/dictionnaires/francais/maillot/48685',
        'https://www.duden.de/rechtschreibung/Kleid',
        'https://dle.rae.es/vestido',
        'https://www.treccani.it/vocabolario/abito/',
        'https://www.treccani.it/vocabolario/vestito/',
    ],
    'files': {name: hashlib.sha256((HERE / name).read_bytes()).hexdigest() for name in ['us_germany_priority.csv', 'negative_review.csv', 'qualified_local_seeds.csv']},
}
(HERE / 'review_receipt.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'status': 'PASS', 'decisions': counts, 'priority': priority_counts, 'upscope_warning': receipt['upscope_warning'], 'original_files_unchanged': len(EXPECTED)}, ensure_ascii=False))
