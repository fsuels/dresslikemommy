from pathlib import Path
import hashlib, json, re
ROOT = Path(__file__).resolve().parent
BASE, THEME = ROOT / 'baseline', ROOT / 'theme'
sha = lambda value: hashlib.sha256(value).hexdigest()
filename = 'snippets/jsonld-seo.liquid'
before = (BASE / filename).read_bytes()
assert hashlib.md5(before).hexdigest() == 'b7935da217fb539fc8fc4b32793b7132'
expected = before.decode().replace("  {%- assign price_valid_until_year = 'now' | date: '%Y' | plus: 1 -%}\n", '')
expected = expected.replace("  {%- assign price_valid_until = price_valid_until_year | append: '-12-31' -%}\n", '')
expected = expected.replace('      "priceValidUntil": {{ price_valid_until | json }},\n', '')
expected = re.sub(r'      "hasMerchantReturnPolicy": \{[\s\S]*?      \},\n', '', expected, count=1)
assert (THEME / filename).read_bytes() in [before, expected.encode()]
(THEME / filename).write_text(expected)
main_file = 'sections/main-product.liquid'
prior = (ROOT.parent / 'theme_candidate/theme' / main_file).read_text()
call = "{% render 'product-faq-schema', product: product %}\n"
assert prior.count(call) == 1
after = prior.replace(call, '')
assert (THEME / main_file).read_text() in [prior, after]
(THEME / main_file).write_text(after)
proof = {'independent_contract': '../structured_data_scope_review.md', 'source_theme': 'gid://shopify/OnlineStoreTheme/133290917985', 'source_file': filename, 'source_md5': hashlib.md5(before).hexdigest(), 'source_sha256': sha(before), 'candidate_sha256': sha(expected.encode()), 'exact_removed_items': ['two invented next-year Dec31 expiry assignments', 'Offer.priceValidUntil', 'unconditional Offer.hasMerchantReturnPolicy', 'single main-product product-faq-schema render call'], 'new_schema_added': False, 'selected_offer_fields_and_other_schema_preserved': True, 'faq_snippet_file_unchanged': True, 'no_product_eligibility_inferred': True, 'rendered_json_validation': 'ROOT_OWNED_NOT_RUN_LOCALLY'}
(ROOT / 'structured_data_merge_proof.json').write_text(json.dumps(proof, indent=2) + '\n')
print('Exact deletion-only structured-data contract recorded; FAQ source file preserved.')
