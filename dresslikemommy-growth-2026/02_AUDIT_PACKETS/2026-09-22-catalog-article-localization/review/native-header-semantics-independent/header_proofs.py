"""Independent local preservation primitives, imported only by this review lane."""
import re,html,hashlib
from html.parser import HTMLParser
SHA=lambda s:hashlib.sha256(s.encode()).hexdigest()
TH=re.compile(r'(<th\b[^>]*>)([\s\S]*?)(</th\s*>)',re.I)
NUM=re.compile(r'\d+(?:[.,]\d+)?')
def plain(s):return html.unescape(re.sub(r'<[^>]+>','',s))
def header_envelope(s):return TH.sub(lambda m:m[1]+'{REVIEWED_HEADER_TEXT}'+m[3],s)
class Events(HTMLParser):
 def __init__(self,s):
  super().__init__(convert_charrefs=True);self.events=[];self.feed(s);self.close()
 def handle_starttag(self,t,a):self.events.append(('start',t,a))
 def handle_endtag(self,t):self.events.append(('end',t))
 def handle_startendtag(self,t,a):self.events.append(('empty',t,a))
def prove_only_header_text(before,after):
 assert header_envelope(before)==header_envelope(after),'Non-header bytes changed'
 assert re.findall(r'<[^>]+>',before)==re.findall(r'<[^>]+>',after),'Markup/attributes changed'
 assert Events(before).events==Events(after).events,'Independent parsed tag/attribute events changed'
 b=list(TH.finditer(before));a=list(TH.finditer(after));assert len(b)==len(a)
 changes=[]
 for i,(x,y) in enumerate(zip(b,a)):
  if x[2]==y[2]:continue
  assert NUM.findall(plain(x[2]))==NUM.findall(plain(y[2])),'Header numeric identifiers changed'
  changes.append({'headerOrdinal':i,'beforeHTML':x[2],'afterHTML':y[2],'beforeLabel':plain(x[2]),'afterLabel':plain(y[2])})
 assert changes,'Candidate has no changes'
 assert re.findall(r'<td\b[^>]*>[\s\S]*?</td\s*>',before,re.I)==re.findall(r'<td\b[^>]*>[\s\S]*?</td\s*>',after,re.I),'Data cell changed'
 return {'beforeValueSHA256':SHA(before),'valueSHA256':SHA(after),'nonHeaderBytes':'PASS','allRawTagBytesAndAttributes':'PASS','independentParserEvents':'PASS','allDataCells':'PASS','headerNumericIdentifiers':'PASS','changes':changes}
