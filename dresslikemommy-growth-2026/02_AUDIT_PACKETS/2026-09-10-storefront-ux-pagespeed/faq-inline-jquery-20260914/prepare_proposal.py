"""Prepare local-only FAQ proposal; never calls Shopify or Git."""
from pathlib import Path
import hashlib
import json
import re
import difflib

PACKET = Path(__file__).resolve().parent

def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()

source = json.loads((PACKET / 'shopify-readback.json').read_text())
page = source['data']['pages']['nodes'][0]
assert page['id'] == 'gid://shopify/Page/161933381' and page['handle'] == 'faqs'
before = page['body']
assert (PACKET / 'page-before.html').read_bytes() == before.encode()
scripts = re.findall(r'<script>.*?</script>', before, re.S)
assert len(scripts) == 2
assert 'function remove_classes_active()' in scripts[0]
assert 'getWidthBrowser()' in scripts[1] and "$('#goGrid')" in scripts[1]
proposed = re.sub(r'<script>.*?</script>', '', before, flags=re.S)
pattern = re.compile(r'<div class="question-answer-block">\s*<h3><a class="ask" onclick="[^"]*">([^<]+)</a></h3>\s*<div class="answer" style="display: none; font-size: 16px;">(.*?)</div>\s*</div>', re.S)
blocks = list(pattern.finditer(proposed))
assert len(blocks) == 8

def disclosure(match):
    label, answer = match.groups()
    return (f'<details class="question-answer-block" name="dlm-faq">\n'
            f'<summary class="ask"><h3>{label}</h3></summary>\n'
            f'<div class="answer" style="font-size: 16px;">{answer}</div>\n'
            '</details>')

proposed = pattern.sub(disclosure, proposed)
style = '''<style>
#page-content .help-page summary.ask { display: list-item; list-style: disclosure-closed inside; min-height: 44px; padding: 10px 0; cursor: pointer; }
#page-content .help-page details[open] > summary.ask { list-style-type: disclosure-open; }
#page-content .help-page summary.ask::-webkit-details-marker { display: inline; }
#page-content .help-page summary.ask h3 { display: inline; margin: 0; }
#page-content .help-page summary.ask:focus-visible { outline: 2px solid currentColor; outline-offset: 4px; }
</style>'''
proposed = proposed.replace('<div id="page-content">', '<div id="page-content">\n' + style, 1)
assert not re.search(r'<script|onclick=|jQuery|display: none;', proposed)
answers_before = [m.group(2) for m in blocks]
answers_after = re.findall(r'<div class="answer" style="font-size: 16px;">(.*?)</div>', proposed, re.S)
assert answers_before == answers_after
links_before = re.findall(r'<a href=.*?</a>', before)
links_after = re.findall(r'<a href=.*?</a>', proposed)
assert links_before == links_after
(PACKET / 'page-proposed.html').write_text(proposed)
(PACKET / 'page-body.patch').write_text(''.join(difflib.unified_diff(before.splitlines(True), proposed.splitlines(True), fromfile='Page161933381.before.body', tofile='Page161933381.proposed.body')))
manifest = {
    'status': 'LOCAL_PROPOSAL_ONLY',
    'page_id': page['id'], 'handle': page['handle'], 'source_updated_at': page['updatedAt'],
    'before_sha256': sha(before), 'proposed_sha256': sha(proposed),
    'before_bytes': len(before.encode()), 'proposed_bytes': len(proposed.encode()),
    'removed_legacy_scripts': 2, 'converted_controls': len(blocks),
    'answer_html_byte_preservation': answers_before == answers_after,
    'all_answer_hashes': [sha(a) for a in answers_before],
    'all_href_anchors_byte_preserved': links_before == links_after,
    'href_anchor_count': len(links_before),
    'labels': [m.group(1) for m in blocks],
    'live_writes': 0, 'theme_changes': 0,
    'rollback': 'Restore exact page-before.html only after fresh same-page source readback and separately authorized release.',
    'release_gate': 'Parent owns approval and canonical updates; current scope excludes page/theme writes, publish, commit and push.'
}
(PACKET / 'proposal-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
print(json.dumps(manifest, indent=2))
