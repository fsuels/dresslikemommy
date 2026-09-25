"""Schema-validated, read-only Shopify article export. No translation provider calls."""
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p/'ops/scripts/shopify_admin_config.py').exists())
sys.path.insert(0, str(ROOT/'ops/scripts'))
from publish_blog_articles import graphql_request
from shopify_admin_config import load_access_token, resolve_store_domain

QUERIES = json.loads((HERE/'queries.json').read_text())
assert all(q.lstrip().startswith('query ') and 'mutation ' not in q for q in QUERIES.values())
DOMAIN = resolve_store_domain()
TOKEN = load_access_token()

def now():
    return datetime.now(timezone.utc).isoformat()

def save(path, data):
    path = HERE/path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n')

def fetch(kind, variables, filename):
    path = HERE/filename
    if path.exists():
        previous = json.loads(path.read_text())
        assert previous['queryName'] == kind and previous['variables'] == variables
        return previous['data']
    started = now()
    try:
        data = graphql_request(DOMAIN, TOKEN, '2026-01', QUERIES[kind], variables)
    except Exception as exc:
        # No auth headers, tokens, or credential contents are persisted.
        message = str(exc)
        if TOKEN:
            message = message.replace(TOKEN, '[REDACTED]')
        save('fetch_failure.json', {'at':now(),'queryName':kind,'variables':variables,'errorType':type(exc).__name__,'message':message[:1500]})
        raise RuntimeError('Read-only Shopify audit stopped; see fetch_failure.json for sanitized error.') from None
    save(filename, {'startedAt':started,'completedAt':now(),'queryName':kind,'variables':variables,'data':data})
    return data

snapshot_path = HERE/'selection_clock.json'
if snapshot_path.exists():
    cutoff = json.loads(snapshot_path.read_text())['at']
else:
    cutoff = now()
    save('selection_clock.json', {'at':cutoff,'selection':'isPublished true AND nonnull publishedAt <= this timestamp; source inventory covers all blogs, including metadata for excluded drafts/future articles'})
cutoff_time = datetime.fromisoformat(cutoff)
blogs_first = json.loads((HERE/'blogs_locales_raw.json').read_text())['data']
blogs = list(blogs_first['blogs']['nodes'])
cursor = blogs_first['blogs']['pageInfo']['endCursor'] if blogs_first['blogs']['pageInfo']['hasNextPage'] else None
page = 1
while cursor:
    data = fetch('blogs', {'after':cursor}, f'raw/blogs_{page:03d}.json')
    blogs.extend(data['blogs']['nodes'])
    cursor = data['blogs']['pageInfo']['endCursor'] if data['blogs']['pageInfo']['hasNextPage'] else None
    page += 1
locales = [x['locale'] for x in blogs_first['shopLocales'] if x['published'] and not x['primary']]
assert 'en' not in locales and len(locales)==len(set(locales))
all_articles=[]
cursor=None
page=0
while True:
    data=fetch('articles', {'after':cursor}, f'raw/inventory_{page:03d}.json')
    all_articles.extend(data['articles']['nodes'])
    info=data['articles']['pageInfo']
    print(json.dumps({'phase':'inventory','page':page,'articlesRead':len(all_articles),'hasNextPage':info['hasNextPage']}),flush=True)
    if not info['hasNextPage']:
        break
    assert info['endCursor'] and info['endCursor'] != cursor
    cursor=info['endCursor']
    page+=1
assert len(all_articles)==len({a['id'] for a in all_articles})
assert {a['blog']['id'] for a in all_articles} <= {b['id'] for b in blogs}
published=[]
excluded=[]
for article in all_articles:
    date=datetime.fromisoformat(article['publishedAt'].replace('Z','+00:00')) if article['publishedAt'] else None
    if article['isPublished'] and date and date<=cutoff_time:
        published.append(article)
    else:
        excluded.append(dict(article,exclusionReason='NOT_PUBLISHED' if not article['isPublished'] else 'FUTURE_OR_MISSING_PUBLISH_TIME'))
save('inventory.json', {'observedAt':cutoff,'blogs':blogs,'publishedLocales':blogs_first['shopLocales'],'nonEnglishLocales':locales,'allArticleCount':len(all_articles),'publishedArticleCount':len(published),'excludedArticleCount':len(excluded),'publishedArticles':published,'excludedArticles':excluded,'paginationExhausted':True})
print(json.dumps({'phase':'inventory_complete','blogs':len(blogs),'articles':len(all_articles),'published':len(published),'excluded':len(excluded),'locales':len(locales)}),flush=True)

ids=[a['id'] for a in published]
batches=[ids[i:i+20] for i in range(0,len(ids),20)]
for i, batch in enumerate(batches):
    data=fetch('source', {'ids':batch}, f'raw/source_{i:03d}.json')
    assert len(data['nodes'])==len(batch) and {n['id'] for n in data['nodes']}==set(batch)
    for n in data['nodes']:
        assert n['isPublished'] and n['publishedAt'] and datetime.fromisoformat(n['publishedAt'].replace('Z','+00:00'))<=cutoff_time
    print(json.dumps({'phase':'sources','batch':i+1,'totalBatches':len(batches)}),flush=True)

for locale in locales:
    for i,batch in enumerate(batches):
        data=fetch('translations', {'ids':batch,'locale':locale,'after':None}, f'raw/translations_{locale}_{i:03d}.json')
        result=data['translatableResourcesByIds']
        assert not result['pageInfo']['hasNextPage'], 'Unexpected translation pagination on exactly20 IDs'
        assert {n['resourceId'] for n in result['nodes']}==set(batch)
        print(json.dumps({'phase':'translations','locale':locale,'batch':i+1,'totalBatches':len(batches)}),flush=True)
save('fetch_complete.json', {'completedAt':now(),'blogs':len(blogs),'allArticles':len(all_articles),'publishedArticles':len(published),'excludedArticles':len(excluded),'nonEnglishLocales':locales,'sourceBatches':len(batches),'translationBatches':len(batches)*len(locales),'allPaginationExhausted':True,'externalWrites':False,'translationProviderCalls':0,'queriesSchemaValidated':True})
print(json.dumps({'phase':'complete','published':len(published),'localeArticlePairs':len(published)*len(locales)}),flush=True)
