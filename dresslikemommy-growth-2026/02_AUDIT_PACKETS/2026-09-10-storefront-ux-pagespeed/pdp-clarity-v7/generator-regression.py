"""Check actual map generation with only its local JSON helper dependencies loaded.

The bundled Python lacks deep_translator, which translation_utils imports eagerly.
These checks execute its unchanged JSON helpers from source without loading network
translation clients. They do not certify a normal generator CLI invocation.
"""
import ast
import importlib.util
import json
from pathlib import Path
import re
import sys
import tempfile
import types

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
CANDIDATE = HERE.parent / 'candidate'
source = ROOT / 'ops/scripts/translation_utils.py'
tree = ast.parse(source.read_text())
helpers = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name in {'read_shopify_json', 'get_path'}]
utility = types.ModuleType('translation_utils')
utility.__dict__.update({'Path': Path, 're': re, 'json': json, 'COMMENT_RE': re.compile(r'\A(/\*.*?\*/\s*)', re.S)})
exec(compile(ast.Module(body=helpers, type_ignores=[]), str(source), 'exec'), utility.__dict__)
sys.modules['translation_utils'] = utility
spec = importlib.util.spec_from_file_location('copy_map_generator', ROOT / 'ops/scripts/build_product_page_copy_map.py')
generator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generator)
generator.LOCALES_DIR = CANDIDATE / 'locales'
actual = generator.build_map()
candidate = json.loads((CANDIDATE / 'snippets/product-page-copy-map.liquid').read_text().split('\n', 1)[1])
keys = {'back_to_context', 'view_similar_styles_in', 'browse_more_from'}
assert len(candidate) == 35
assert all(candidate[locale][key] == actual[locale][key] for locale in candidate for key in keys)

with tempfile.TemporaryDirectory(prefix='dlm-map-regression-') as temp:
    directory = Path(temp)
    en = {'nav': {'back': 'Back {{ context }}', 'similar': 'Styles {{collection}}', 'browse': 'Browse {{ collection }}', 'other': 'Keep {{ collection }}'}}
    (directory / 'en.default.json').write_text(json.dumps(en))
    (directory / 'ja.json').write_text(json.dumps({'nav': {'back': '', 'similar': 'translation missing: ja.nav.similar'}}))
    generator.LOCALES_DIR = directory
    generator.COPY_KEYS = [('back_to_context', 'nav.back'), ('view_similar_styles_in', 'nav.similar'), ('browse_more_from', 'nav.browse'), ('other', 'nav.other')]
    output = generator.build_map()
    for locale in ['en', 'ja']:
        assert output[locale] == {'back_to_context': 'Back __CONTEXT__', 'view_similar_styles_in': 'Styles __CONTEXT__', 'browse_more_from': 'Browse __CONTEXT__', 'other': 'Keep {{ collection }}'}
print(json.dumps({'status': 'PASS', 'realLocaleTemplates': 105, 'fallbackLocales': 2, 'unrelatedPlaceholderPreserved': True, 'execution': 'Actual generator with source-extracted local JSON helpers; network clients excluded'}))
