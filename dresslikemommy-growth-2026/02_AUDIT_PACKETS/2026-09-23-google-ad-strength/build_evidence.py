import copy,json
from pathlib import Path
base=Path(__file__).parent
source=json.loads((base.parent/'2026-09-22-google-search-build/payload.json').read_text())
deltas={
'Mommy & Me Pajamas':{'ids':['825605060532','202058006764'],'heads':{0:'Mommy and Me Pajamas',1:'Mother and Daughter Pajamas',2:'Mother Daughter Matching PJs',3:'Mommy and Me Long Sleeve PJs',4:'Mommy and Me Short Sleeve PJs',5:'Find Your Matching Sleepwear',12:'Matching Mommy and Me Pajamas',13:'Short & Long Sleeve Pajamas',14:'Coordinated Bedtime Looks'},'desc':{0:"Shop mommy and me pajamas. Each person's pajama set is selected and priced separately.",1:"Find mother daughter matching pajamas. Each person's set is priced separately.",2:"Shop mommy and me short sleeve pajamas. Choose and buy each person's set separately.",3:'Find mommy and me long sleeve pajamas, priced per person. Review delivery at checkout.'},'unpin':True},
'Father & Son Shirts':{'ids':['825646172296','202058006804'],'heads':{0:'Father Son Matching Shirts',2:'Daddy and Me Button Up Shirts',12:'Explore Prints Together',13:'Shirts for Dad and Child',14:'Find a Look for Family Photos'},'desc':{0:'Shop father son matching shirts. Each shirt is priced and purchased separately.',1:'Find father son matching Hawaiian shirts in tropical prints for photos and days together.',2:'Browse father son matching button up shirts. Choose dad and child sizes separately.'}},
'Mommy & Me Dresses':{'ids':['825646199950','202058006524'],'heads':{0:'Mommy and Me Dresses',2:'Mommy and Me Floral Dresses',3:'Mommy and Me Maxi Dresses',12:'Mother Daughter Matching Dress',13:'Create a Shared Photo-Day Look',14:'Browse Prints for Both of You'},'desc':{0:'Shop mommy and me dresses. Each dress is priced and sold separately.',1:'Explore mother daughter matching dresses for photos, outings and time together.'}},
'Mommy & Me Outfits':{'ids':['825646199956','202058006844'],'heads':{0:'Mommy and Me Outfits',2:'Mommy and Me Matching Sets',12:'Mother Daughter Matching Looks',13:'Mommy and Me Photo Outfits',14:'Build Your Coordinated Style'},'desc':{1:'Browse mother daughter matching outfits, from dresses to coordinated sets for shared days.',3:'Find mommy and me outfits for pictures. Review delivery estimates before your photo day.'}},
'Family Matching Outfits':{'ids':['825727913987','202058006564'],'heads':{12:'Matching Family Photo Outfits',13:'Matching Family Vacation Looks',14:'Family Dress and Shirt Styles'},'desc':{1:'Browse matching family vacation outfits. Pick coordinated dresses, shirts and sets.',2:"Explore matching family outfits for pictures. Choose each person's pieces and sizes.",3:'Find a matching family dress and shirt. Review delivery estimates before your event.'}},
'Family Matching Shirts':{'ids':['825727944842','202058006604'],'heads':{12:'Matching Family T Shirts',13:'Family Matching Tops',14:'Matching Family Button Ups'},'desc':{1:'Explore matching family button up shirts and tees in coordinated prints for photos.'}}
}
def fields(r):return [r['final_url']]+[p['text'] for p in r['display_paths']]+[x['text'] for x in r['headlines']]+[x['text'] for x in r['descriptions']]
def fnv(a):
 h=2166136261
 for c in json.dumps(a,ensure_ascii=False,separators=(',',':')):h=((h^ord(c))*16777619)&0xffffffff
 return hex(h)[2:]
ads=[]
for name,d in deltas.items():
 g=next(g for g in source['ad_groups'] if g['name']==name);before=copy.deepcopy(g['rsa']);after=copy.deepcopy(before)
 after['headlines'] += [{'text':'','characters':0,'pinned_field':None} for _ in range(3)]
 for n,t in d['heads'].items():after['headlines'][n].update(text=t,characters=len(t))
 for n,t in d['desc'].items():after['descriptions'][n].update(text=t,characters=len(t))
 if d.get('unpin'):
  for x in after['descriptions']:x['pinned_field']=None
 assert len(after['headlines'])==15 and all(0<len(x['text'])<=30 for x in after['headlines'])
 assert len(after['descriptions'])==4 and all(0<len(x['text'])<=90 for x in after['descriptions'])
 kws=sorted({k['text'].lower() for k in g['keywords']});texts=[x['text'].lower() for x in after['headlines']+after['descriptions']]
 cover={k:any(k in t for t in texts) for k in kws}
 assert all(cover.values()),cover
 entry={'group':name,'ad_id':d['ids'][0],'group_id':d['ids'][1],'before':before,'after':after,'after_fields_fnv1a':fnv(fields(after)),'literal_keyword_coverage':cover,'native_saved_table_strength':'Pending','native_reopened_editor_strength':'Poor','native_keyword_category':'low','native_reopened_fields_exact_match':True,'native_reopened_sitelinks':6}
 ads.append(entry)
out={'as_of':'2026-09-23','campaign_id':'24273103416','campaign_name':'DLM | GADS | US | EN | Search | 202609','overall':'PARTIAL_EXCELLENT_NOT_ACHIEVED','ads':ads,'campaign_sitelinks':source['assets']['sitelinks'],'native_campaign_status':'Paused','native_all_ads_and_groups_status':'Paused','native_budget':'USD210 campaign total','evidence_method':'Current-session CUA native table plus six reopen/readback comparisons; before copy reconstructed from historical payload only where current editor matched; historical campaign ID is not reused. FNV checksums are non-security transfer checks.'}
(base/'ad_copy_before_after.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps([{'ad_id':a['ad_id'],'fields_fnv1a':a['after_fields_fnv1a'],'keywords_covered':len(a['literal_keyword_coverage'])} for a in ads],indent=2))
