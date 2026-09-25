import json,pathlib,re,collections,hashlib
O=pathlib.Path(__file__).resolve().parent
J=lambda p:json.loads(p.read_text())
d=J(O/'mapping_matrix.json');D={l:dict(zip(d['keys'],v)) for l,v in d.items() if l!='keys'}
rows=J(O/'unique_locale_phrases.json')['rows']
unit=re.compile(r'(\s*\((?:cm|kg|jin|ס"מ)[^()]*\))$')
base={'Size':'size','Age':'age','Height':'height','Weight':'weight','Bust':'bust','Waist':'waist','Hip':'hip','Hips':'hip','Shoulder':'shoulder','Sleeve':'sleeve','Length':'length','Chest Width':'chest_width','Shoulder Width':'shoulder_width','Sleeve Length':'sleeve_length','Pants Length':'pants_length','Pant Length':'pants_length','Shirt Length':'shirt_length','Skirt Length':'skirt_length','Garment Length':'garment_length','Clothing Length':'garment_length','Recommended Weight':'recommended_weight','Weight Recommendation':'recommended_weight','Suggested Weight':'recommended_weight','Recommended Height':'recommended_height','Suggested Height':'recommended_height',"Children's Sizes":'child_sizes','Father Sizes':'father_sizes','Body Length':'body_length','Chest/Bust':'chest_bust','Στήθος/Bust':'chest_bust','Pant':'pants'}
fixed={
('da','Underbust'):'Underbarm',('ru','Underbust'):'Под грудью',('sv','Underbust'):'Under bysten',
('ru','Upper Bust'):'Верхняя часть груди',('sv','Upper Bust'):'Övre byst',
('ru','Top Length'):'Длина топа',('sv','Top Length'):'Toppens längd',
('ru','US Height'):'Рост (США)',('sv','US Height'):'Längd (USA)',
('ru','Coat Length'):'Длина пальто',('sv','Coat Length'):'Kappans längd',
('el','Waist Stretch'):'Τέντωμα μέσης',('el','Leg Opening'):'Άνοιγμα ποδιού',('el','Height Range'):'Εύρος ύψους',
}
# Complete source labels with awkward partially localized Pant/Short fragments. Preserve original comparison/dash separator.
length_stems={'Pant/krátká délka','Pant/אורך קצר','Pant/Short Length','Pant/Kort längd','Pant/kort længde','Pant/Kort længde','Pant/kort lengde','Pant/kort längd'}
pants_length_stems={'Pant Délka','Pantlængde','Pant Lengde','Pantlängd'}
sleeve_skirt_stems={'Sleeve or Skirt','Sleeve / skjørt','Sleeve / kjol','Sleeve eller nederdel','Sleeve eller skjørt','Sleeve eller kjol'}
mixed_pants_length={'Pants طول القطعة','Pants Délka oděvu','Pants Tøjlængde','Pants Μήκος ρούχου','Pants Vaatteen pituus','Pants אורך הבגד','Pants परिधान लंबाई','Pants 着丈','Pants 의류 길이','Pants Kledinglengte','Pants Plagglengde','Pants Długość ubrania','Pants Длина изделия','Pants Plagglängd'}
mixed_pants_waist={'Pants الخصر','Pants Pas','Pants Talje','Pants Μέση','Pants Vyötärö','Pants מותן','Pants कमर','Pants ウエスト','Pants 허리','Pants Taille','Pants Midje','Pants Talia','Pants Талия','Pants Midja'}
def translate(loc,h):
 if loc=='fr' and h=='Age':return 'Âge','Correct native French orthography.'
 if '|' in h and loc=='ko':return h.split('|',1)[1],'Retain the complete existing Korean label; remove duplicate English label in the same header.'
 m=unit.search(h);suffix=m.group() if m else '';stem=h[:m.start()] if m else h
 q=D[loc]
 if stem in base:v=q[base[stem]]
 elif (loc,stem) in fixed:v=fixed[(loc,stem)]
 elif stem=='Bust * 2':v=q['bust']+' * 2'
 elif stem in length_stems:v=q['pants_short_length']
 elif stem in pants_length_stems or stem in mixed_pants_length:v=q['pants_length']
 elif stem in mixed_pants_waist:v=q['pants_waist']
 elif stem=='Sleeve Lengde':v=q['sleeve_length']
 elif stem in sleeve_skirt_stems:v=q['sleeve_or_skirt']
 elif re.fullmatch(r'Shoulder (?:or|ή) [—-]',stem):v=q['shoulder']+' '+q['or']+' '+stem[-1]
 elif re.fullmatch(r'Sleeve (?:or|eller) [—-]',stem):v=q['sleeve']+' '+q['or']+' '+stem[-1]
 elif re.fullmatch(r'(?:Pant|Housut)\s*/\s*(?:Short|Kort|kort|krátký|Krátký|קצר)(?: (?:or|eller|nebo|או|oder|tai) [—-])?',stem):
  v=q['pants']+'/'+q['shorts'].lower()
  if stem[-1] in '—-':v+=' '+q['or']+' '+stem[-1]
 else:raise ValueError((loc,h,stem))
 assert all(x in v+suffix for x in re.findall(r'\d+',h)),(loc,h,v)
 assert suffix=='' or (v+suffix).endswith(suffix)
 return v+suffix,'Translate the header label only; preserve exact trailing unit notation, multipliers, and dash meaning.'
output=[]
for r in rows:
 if r['classification'].startswith('KEEP'):continue
 v,why=translate(r['locale'],r['visibleHeader'])
 output.append(dict(locale=r['locale'],beforeLabel=r['visibleHeader'],proposedLabel=v,classification=r['classification'],occurrences=r['occurrences'],effectiveCurrentFalseOccurrences=r['effectiveOutdatedFalse'],effectiveOutdatedTrueOccurrences=r['effectiveOutdatedTrue'],distinctBodies=r['distinctBodies'],tagOverlapOccurrences=r['tagOverlapOccurrences'],reason=why,uses=r['uses']))
assert len(output)==946
out=O/'proposed_language_mappings.json';out.write_text(json.dumps({'status':'AUTHOR_PROPOSED_MAPPING_ONLY_PENDING_ROOT_INDEPENDENT_MEANING_REVIEW','rows':output},ensure_ascii=False,indent=2)+'\n')
print('mapping rows',len(output),'occurrences',sum(r['occurrences'] for r in output),'hash',hashlib.sha256(out.read_bytes()).hexdigest())
for l in D:
 rs=[r for r in output if r['locale']==l];print(l,len(rs),sum(r['effectiveCurrentFalseOccurrences'] for r in rs),sum(r['effectiveOutdatedTrueOccurrences'] for r in rs))
