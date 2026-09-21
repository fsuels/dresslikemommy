#!/usr/bin/env python3
"""Create a sanitized repository receipt from a private raw receipt; never print values."""
import hashlib, html, json, os, re, sys
from pathlib import Path
from urllib.parse import urlsplit
HERE=Path(__file__).resolve().parent
PRIVATE=Path('/Users/fsuels/.config/dresslikemommy/merchant-execution-receipts/20260915-it-cohort-1305')
name=sys.argv[1]
if not re.fullmatch(r'[a-z0-9_]+\.json',name): raise SystemExit('invalid receipt name')
raw=PRIVATE/name
os.chmod(raw,0o600)
data=json.loads(raw.read_text())
redactions=[]
def sha(s): return hashlib.sha256(s.encode()).hexdigest()
def scrub(value,path=''):
    if isinstance(value,dict): return {k:scrub(v,path+'/'+k) for k,v in value.items()}
    if isinstance(value,list): return [scrub(v,path+'/'+str(i)) for i,v in enumerate(value)]
    if not isinstance(value,str): return value
    count=0
    def replace(m):
        nonlocal count
        host=(urlsplit(html.unescape(m.group(0))).hostname or '').lower()
        if host=='admin.shopify.com' or any(host==d or host.endswith('.'+d) for d in ('alicdn.com','alibaba.com','aliexpress.com','1688.com','taobao.com','tmall.com')):
            count+=1
            return '[REDACTED_SOURCE_URL]'
        return m.group(0)
    clean=re.sub(r'https?://[^\s"\'<>]+',replace,value)
    if count: redactions.append({'path':path,'originalValueSHA256':sha(value),'urlOccurrences':count})
    return clean
clean=scrub(data)
clean['privateOriginal']={'path':str(raw),'sha256':hashlib.sha256(raw.read_bytes()).hexdigest()}
clean['sourceUrlRedactions']=redactions
out=HERE/name
out.write_text(json.dumps(clean,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'name':name,'privateSHA256':clean['privateOriginal']['sha256'],'sanitizedSHA256':hashlib.sha256(out.read_bytes()).hexdigest(),'redactedValues':len(redactions),'privateMode':oct(raw.stat().st_mode&0o777)}))
