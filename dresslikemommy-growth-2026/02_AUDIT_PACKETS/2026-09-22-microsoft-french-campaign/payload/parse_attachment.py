from pathlib import Path
import re, json, hashlib, unicodedata

SOURCE = Path('/Users/fsuels/.codex/attachments/55d965e7-ab46-4851-aac8-46d48cab29ae/Pasted text.txt')
OUT = Path(__file__).parent
text = SOURCE.read_text()

def lines(s):
    return [x.strip() for x in s.splitlines() if x.strip()]

def terms(s):
    result=[]
    for line in lines(s):
        if re.fullmatch(r'\[.+\]|".+"',line):
            result.append({'text':line[1:-1], 'match_type':'Exact' if line.startswith('[') else 'Phrase', 'entry':line})
    return result

matches=list(re.finditer(r'^\d+\. Groupe (\d+) — (.+)$', text, re.M))
groups=[]
for i,m in enumerate(matches):
    block=text[m.end():matches[i+1].start() if i+1<len(matches) else text.index('11. Exclusions de campagne')]
    english=re.search(r'Équivalent de (.+)\.',block).group(1)
    url=re.search(r'https://\S+',block).group(0)
    path1=re.search(r'Chemin 1 : (.+)',block).group(1)
    path2=re.search(r'Chemin 2 : (.+)',block).group(1)
    posblock=block.split('Mots-clés positifs\n',1)[1].split('Titres',1)[0]
    headlineblock=re.split(r'Titres[^\n]*\n',block,1)[1].split('Descriptions',1)[0]
    descblock=re.split(r'Descriptions[^\n]*\n',block,1)[1].split('Exclusions',1)[0]
    negblock=block.split('Exclusions',1)[1]
    groups.append({
        'number':int(m.group(1)), 'name':m.group(2), 'english_source_name':english,
        'final_url':url, 'path1':path1, 'path2':path2,
        'headlines':lines(headlineblock), 'descriptions':lines(descblock),
        'positive_keywords':terms(posblock), 'negative_keywords':terms(negblock),
        'positive_keywords_lines':'\n'.join(t['entry'] for t in terms(posblock)),
        'negative_keywords_lines':'\n'.join(t['entry'] for t in terms(negblock)),
        'source_notes': '\n'.join(l for l in lines(negblock) if not re.fullmatch(r'\[.+\]|".+"',l)),
        'landing_verification':'NOT_RUN_CURRENT_SESSION',
    })

campaignblock=text.split('11. Exclusions de campagne',1)[1].split('12. Options de suivi',1)[0]
neg_fr=terms(campaignblock.split('A. Exclusions françaises — Expression',1)[1].split('B. Complément anglais',1)[0])
neg_en=terms(campaignblock.split('B. Complément anglais',1)[1].split('C. Restrictions temporaires',1)[0])
neg_temp=terms(campaignblock.split('C. Restrictions temporaires',1)[1].split('D. Ce qui reste à examiner',1)[0])
trackingblock=text.split('12. Options de suivi',1)[1].split('13. Extensions françaises',1)[0]
for g in groups:
    source_suffix=re.search(re.escape(g['name'])+r'\n(utm_source=[^\n]+)',trackingblock).group(1)
    g['source_final_url_suffix']=source_suffix
    g['candidate_final_url_suffix_for_fr_ca']=source_suffix.replace('dlm_ms_us_fr_search_202609','dlm_ms_fr_ca_fr_search_202609')
    g['tracking_note']='Candidate only. Root must verify geography and live tagging inheritance; do not duplicate or change tracking blindly.'

extblock=text.split('13. Extensions françaises',1)[1].split('14. Extensions d’image',1)[0]
callouts=lines(extblock.split('Accroches — une par champ',1)[1].split('Les six accroches',1)[0])
sitelinkblock=extblock.split('indiquée plus haut.',1)[1].split('Les titres et descriptions',1)[0]
slines=lines(sitelinkblock)
assert len(slines)==32
sitelinks=[]
for i in range(8):
    heading,label,d1,d2=slines[4*i:4*i+4]
    assert heading==label
    sitelinks.append({'text':label,'description1':d1,'description2':d2,'final_url':groups[i]['final_url'],'group_number':i+1})
assocblock=extblock.split('Groupe\tLiens annexes proposés\n',1)[1].split('N’associez pas',1)[0]
associations={l.split('\t')[0]:l.split('\t')[1].split(' ; ') for l in lines(assocblock)}
snippetblock=extblock.split('Groupe\tEn-tête\tValeurs\n',1)[1]
snippets=[]
for l in lines(snippetblock):
    name,header,values=l.split('\t')
    snippets.append({'group_name':name,'header':header,'values':values.split(' · ')})
for g in groups:
    g['sitelink_associations']=associations[g['name']]
    g['structured_snippet']=next(s for s in snippets if s['group_name']==g['name'])
    g['conditional_routing_negatives']=g['number'] in [2,3,6]
    g['routing_condition']=('Only apply each routing negative when the matching specific group can serve; explicit in attachment for groups 2 and 6 and logically required for group 3.' if g['conditional_routing_negatives'] else None)

payload={
    'artifact_status':'LOCAL_CANDIDATE_NOT_APPLIED',
    'source_attachment':str(SOURCE), 'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    'target_campaign_id':'506255077',
    'target_campaign_name':'DLM | MS | FR & CA | FR | Search | 202609',
    'attachment_campaign_name':'DLM | MS | US | FR | Search | 202609',
    'copy_source_campaign_id':'506254907',
    'copy_source_campaign_name':'DLM | MS | US | EN | Search | 202609',
    'source_language':'French', 'target_geography_status':'ROOT_CLARIFICATION_PENDING_AT_PARSE_TIME',
    'settings_from_attachment':{'objective':'Drive conversions', 'campaign_type':'Search', 'ad_group_type':'Standard', 'ad_type':'Responsive Search Ad', 'language':'French','source_country':'United States','location_intent':'People in your targeted locations','setup_status':'Paused','pinning':'None initially','budget':'No amount authorized by attachment; retain exact root/user authority','bids':'Verify actual strategy and caps before activation','ai_max_broad_url_expansion':'Do not automatically enable'},
    'groups':groups,
    'campaign_negatives':{'french_phrase':neg_fr,'english_phrase':neg_en,'temporary_catalog_exact':neg_temp,'all':neg_fr+neg_en+neg_temp,'all_lines':'\n'.join(t['entry'] for t in neg_fr+neg_en+neg_temp)},
    'extensions':{'callouts':callouts,'sitelinks':sitelinks,'structured_snippets':snippets,'image_text_pairs':None,'image_text_status':'NOT_SUPPLIED_ATTACHMENT_REFERENCES_DOWNLOADS_WITHOUT_ACTUAL_LINKS_OR_PAIR_STRINGS'},
    'limitations':['User target overrides US attachment campaign name/geography; root owns final geography decision.', 'Current landing pages, catalog assortment, shipping and purchase path not verified by this local parser.', 'Image pairs are claimed but absent from the pasted attachment; do not invent the 160 pairs.', 'Source groups 3 and 8 URLs explicitly require verification. Source says father-son page and cart/shipping include English.', 'All conditional routing negatives need destination-specific group eligibility before application.', '14 temporary catalog exclusions were not reverified for current availability.', 'English phrase negatives are intentional complementary exclusions for mixed-language queries.'],
}

limit_errors=[]
checks=[]
for g in groups:
    for field,limit,count in [('headlines',30,15),('descriptions',90,4)]:
        assert len(g[field])==count,(g['name'],field,len(g[field]))
        for j,v in enumerate(g[field],1):
            if len(v)>limit: limit_errors.append({'group':g['number'],'field':field,'index':j,'length':len(v),'limit':limit,'text':v})
    for field in ['path1','path2']:
        if len(g[field])>15:limit_errors.append({'group':g['number'],'field':field,'length':len(g[field]),'limit':15,'text':g[field]})
    checks.append({'group_number':g['number'],'name':g['name'],'positives':len(g['positive_keywords']),'group_negatives':len(g['negative_keywords']),'headline_max':max(map(len,g['headlines'])),'description_max':max(map(len,g['descriptions']))})
for c in callouts:
    if len(c)>25:limit_errors.append({'field':'callout','text':c,'length':len(c),'limit':25})
for s in sitelinks:
    for field,limit in [('text',25),('description1',35),('description2',35)]:
        if len(s[field])>limit:limit_errors.append({'field':'sitelink_'+field,'text':s[field],'length':len(s[field]),'limit':limit})
for s in snippets:
    for v in s['values']:
        if len(v)>25:limit_errors.append({'field':'snippet_value','text':v,'length':len(v),'limit':25})

def normalize(s):
    return ' '.join(re.sub(r"[^\w\s]",' ',unicodedata.normalize('NFC',s).casefold()).split())
conflicts=[]
for g in groups:
    for p in g['positive_keywords']:
        for n in payload['campaign_negatives']['all']+g['negative_keywords']:
            ps,ns=normalize(p['text']),normalize(n['text'])
            blocked=(ps==ns) if n['match_type']=='Exact' else (' '+ns+' ') in (' '+ps+' ')
            if blocked:conflicts.append({'group':g['number'],'positive':p['entry'],'negative':n['entry']})
validation={
    'status':'LOCAL_LITERAL_VALIDATION_ONLY',
    'counts':{'groups':len(groups),'positive_keywords':sum(len(g['positive_keywords']) for g in groups),'headlines':sum(len(g['headlines']) for g in groups),'descriptions':sum(len(g['descriptions']) for g in groups),'group_negatives':sum(len(g['negative_keywords']) for g in groups),'campaign_french_phrase':len(neg_fr),'campaign_english_phrase':len(neg_en),'campaign_phrase_total':len(neg_fr)+len(neg_en),'campaign_temporary_exact':len(neg_temp),'campaign_negatives_total':len(neg_fr+neg_en+neg_temp),'callouts':len(callouts),'sitelinks':len(sitelinks),'structured_snippets':len(snippets),'image_pairs_supplied':0},
    'per_group':checks,'limit_errors':limit_errors,'literal_negative_conflicts':conflicts,
    'duplicate_terms':{},
    'method':'Parse exact source strings; codepoint character lengths; NFC lowercased punctuation-to-space whole-phrase/exact lexical conflicts. Does not simulate Microsoft semantic matching or account inherited negatives.',
    'factual_claims_requiring_landing_evidence':['Every item sold separately/per selected piece', 'Adult and child sizes and relevant combinations purchasable', 'Dresses: floral prints, ruffles, long cuts, smocking', 'Family shirts: T-shirts, button-up, floral and striped styles', 'Pajamas: short/long sleeves, shorts/trousers', 'Father-son shirts: buttoned, Hawaiian/tropical and short-sleeved styles', 'Mother-daughter outfits: dresses, tops, skirts and coordinated pieces', 'Swimwear: bikinis, one piece, skirted suits, tankinis, ruffles', 'Sweaters: cardigans, hoodies, heart and cable-knit designs', 'Size guides, delivery estimates/options and return conditions accessible'],
    'unsupported_promises_detected':[],
}
for scope,ts in [('campaign',payload['campaign_negatives']['all'])]+[(f"group_{g['number']}_positive",g['positive_keywords']) for g in groups]+[(f"group_{g['number']}_negative",g['negative_keywords']) for g in groups]:
    seen=set();dupes=[]
    for t in ts:
        key=(t['text'],t['match_type'])
        if key in seen:dupes.append(t['entry'])
        seen.add(key)
    if dupes:validation['duplicate_terms'][scope]=dupes
assert validation['counts']['positive_keywords']==144
assert validation['counts']['group_negatives']==58
assert validation['counts']['campaign_negatives_total']==251
assert not limit_errors
assert not conflicts
(OUT/'campaign_fr_payload.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
(OUT/'validation.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2)+'\n')
(OUT/'campaign_negatives.txt').write_text(payload['campaign_negatives']['all_lines']+'\n')
for g in groups:
    (OUT/f"group_{g['number']:02d}.json").write_text(json.dumps(g,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(validation,ensure_ascii=False,indent=2))
