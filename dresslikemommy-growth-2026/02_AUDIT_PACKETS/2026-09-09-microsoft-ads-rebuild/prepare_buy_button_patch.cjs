// Local preparation only. Never uploads, publishes, or changes a theme asset.
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const crypto = require('node:crypto');
const packet = __dirname;
const root = path.resolve(packet, '../../..');
const labels = JSON.parse(fs.readFileSync(path.join(packet, 'buy_button_locale_replacements.json'), 'utf8'));
const sha = value => crypto.createHash('sha256').update(value).digest('hex');
function extract(source) {
  const match = /\bUI_LABELS_BY_LOCALE\s*=\s*\{/.exec(source);
  if (!match) throw new Error('Locale map absent');
  const start = match.index + match[0].lastIndexOf('{');
  let depth = 0, quote = '', escaped = false;
  for (let i = start; i < source.length; i++) {
    const c = source[i];
    if (quote) {
      if (escaped) escaped = false;
      else if (c === '\\') escaped = true;
      else if (c === quote) quote = '';
    } else if (c === "'" || c === '"') quote = c;
    else if (c === '{') depth++;
    else if (c === '}' && --depth === 0) return {start, end:i+1, literal:source.slice(start,i+1)};
  }
  throw new Error('Unterminated map');
}
// Accept only nested string dictionaries, never executable source expressions.
function parseMap(literal) {
  const token = /\s+|[{},:]|[A-Za-z_$][A-Za-z0-9_$]*|'(?:\\[\s\S]|[^'\\])*'|"(?:\\[\s\S]|[^"\\])*"/y;
  const tokens = [];
  for (let at=0; at<literal.length;) {
    token.lastIndex=at;
    const m=token.exec(literal);
    if(!m) throw new Error('Unsupported dictionary token');
    at=token.lastIndex;
    if(m[0].trim()) tokens.push(m[0]);
  }
  let i=0;
  const string = t => vm.runInNewContext(t, Object.create(null), {timeout:100, contextCodeGeneration:{strings:false,wasm:false}});
  const consume = t => {if(tokens[i++]!==t) throw new Error('Malformed dictionary');};
  function object() {
    consume('{');
    const result = {};
    while(tokens[i]!=='}') {
      const raw=tokens[i++];
      const key=/^["']/.test(raw)?string(raw):raw;
      if(!/^[A-Za-z_$][A-Za-z0-9_$]*$/.test(key)||Object.hasOwn(result,key)) throw new Error('Invalid or duplicate key');
      consume(':');
      if(tokens[i]==='{') result[key]=object();
      else if(/^["']/.test(tokens[i])) result[key]=string(tokens[i++]);
      else throw new Error('Only string values allowed');
      if(tokens[i]!=='}') consume(',');
    }
    consume('}');
    return result;
  }
  const result=object();
  if(i!==tokens.length) throw new Error('Unexpected trailing dictionary source');
  return result;
}
const liveSource=fs.readFileSync(path.join(packet,'buy_button_deployed_asset_before.js'),'utf8');
const live=parseMap(extract(liveSource).literal);
const files=['product-desktop-ux.js','product-desktop-ux-20260513.js','product-desktop-ux-20260513-ruler-sync.js'];
const report={status:'LOCAL_CANDIDATES_ONLY',labels_sha256:sha(JSON.stringify(labels)),deployed_sha256:sha(liveSource),files:[]};
for(const name of files) {
  const source=fs.readFileSync(path.join(root,'assets',name),'utf8');
  const range=extract(source), before=parseMap(range.literal);
  if(JSON.stringify(before)!==JSON.stringify(live)) throw new Error('Live/local map mismatch: '+name);
  let literal=range.literal, inserted=0;
  for(const [locale,values] of Object.entries(labels)) {
    const existing=before[locale];
    if(existing) {
      for(const [key,value] of Object.entries(values)) if(Object.hasOwn(existing,key)&&existing[key]!==value) throw new Error('Existing translation conflict: '+locale+'.'+key);
      const additions=Object.entries(values).filter(([key])=>!Object.hasOwn(existing,key));
      if(additions.length) {
        const pattern=new RegExp('(^  '+locale+': \\{[\\s\\S]*?)(^  \\},?)','m');
        if(!pattern.test(literal)) throw new Error('Locale block absent: '+locale);
        literal=literal.replace(pattern,(_all,a,b)=>a+additions.map(([k,v])=>'    '+k+': '+JSON.stringify(v)+',\n').join('')+b);
        inserted+=additions.length;
      }
    } else {
      const block='  '+locale+': {\n'+Object.entries(values).map(([k,v])=>'    '+k+': '+JSON.stringify(v)+',\n').join('')+'  },\n';
      literal=literal.slice(0,-1)+block+'}';
      inserted+=Object.keys(values).length;
    }
  }
  const after=parseMap(literal);
  for(const [locale,values] of Object.entries(before)) for(const [key,value] of Object.entries(values)) if(after[locale][key]!==value) throw new Error('Changed existing label');
  for(const [locale,values] of Object.entries(labels)) for(const [key,value] of Object.entries(values)) if(after[locale][key]!==value) throw new Error('Missing replacement');
  const candidate=source.slice(0,range.start)+literal+source.slice(range.end);
  const output=path.join(packet,'buy_button_candidate_'+name);
  fs.writeFileSync(output,candidate);
  report.files.push({source:'assets/'+name,candidate:path.basename(output),before_sha256:sha(source),candidate_sha256:sha(candidate),inserted_labels:inserted,existing_labels_preserved:true,outside_dictionary_bytes_preserved:true,live_map_semantically_matches:true});
}
fs.writeFileSync(path.join(packet,'buy_button_patch_receipt.json'),JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify(report,null,2));
