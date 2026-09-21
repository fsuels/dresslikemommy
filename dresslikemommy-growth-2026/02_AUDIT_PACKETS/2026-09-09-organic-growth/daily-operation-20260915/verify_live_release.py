"""Additive acceptance of one observed Shopify HTML serialization; original gates stay immutable."""
import sys, json
import verify_release as v

def serialization():
    authored=(v.BASE/'gift-guide-candidate.html').read_text()
    actual=(v.BASE/'english-shopify-normalized.html').read_text()
    assert authored.count('<li><strong>')==8
    expected=authored.replace('<li><strong>','<li>\n<strong>')
    assert actual==expected, 'Unexpected serialization bytes'
    assert v.sha(actual)=='3dcef8da979c7a8772f47db7b3ad3090457a0f85b0142746f0aad240ff8fba06'
    ap=v.Blocks();ap.feed(authored);bp=v.Blocks();bp.feed(actual)
    assert not bp.errors and not bp.stack and ap.blocks==bp.blocks and ap.links==bp.links and ap.tags==bp.tags
    return actual

def run(stage):
    actual=serialization()
    if stage=='payload-bound':
        checks=v.payload_check(True)
        checks.pop('source_digest_exact_current_candidate')
        current=v.data('after-english-inventory.json')
        source=next(r for r in current['translatableResource']['translatableContent'] if r['key']=='body_html')
        checks['source_digest_exact_api_serialization']=source['value']==actual and source['digest']==v.sha(actual) and current['article']['body']==actual and current['translatableResource']['resourceId']==v.TARGET
        superseded=['source_digest_exact_current_candidate']
    else:
        checks=v.verify(stage)
        current=v.data(stage+'-inventory.json')
        source=next(r for r in current['translatableResource']['translatableContent'] if r['key']=='body_html')
        checks['english_body']=current['article']['body']==actual
        checks['english_source_body']=source['value']==actual and source['digest']==v.sha(actual) and source['locale']=='en' and source['type']=='HTML'
        superseded=['english_body','english_source_body']
    checks['exact_observed_serialization_only']=True
    result={'status':'PASS' if all(checks.values()) else 'FAILED','stage':stage,'passed':sum(checks.values()),'total':len(checks),'checks':checks,'serialization_superseded_expectations':superseded,'qualification':'Only the specified eight inserted LF bytes are accepted; independent review is a separate release prerequisite; the original exact-byte failure remains preserved. No relaxed whitespace or body-content comparison. All other original checks still apply.'}
    (v.BASE/('verification-'+stage+'-serialization.json')).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:w for k,w in result.items() if k!='checks'}));print('Failed:',[k for k,w in checks.items() if not w])
    return all(checks.values())

if __name__=='__main__':
    assert sys.argv[1] in ['after-english','after','payload-bound']
    sys.exit(0 if run(sys.argv[1]) else 1)

