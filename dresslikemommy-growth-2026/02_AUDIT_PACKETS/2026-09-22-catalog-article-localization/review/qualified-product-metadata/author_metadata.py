# -*- coding: utf-8 -*-
import copy
import hashlib
import importlib.util
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
load = lambda path: json.loads(path.read_text())
dump = lambda name, value: (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
sha = lambda value: hashlib.sha256(value.encode()).hexdigest()
rows = load(HERE / 'eligible251_worklist.json')['rows']
spec = importlib.util.spec_from_file_location('offline_translation', ROOT / 'tooling/offline_translation.py')
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)

# Full recurring source segments are translated once and reused only for exact matches.
categories = [
    'daddy and me matching sets for dads and kids',
    'family matching button-down shirts for parents and kids',
    'family matching cardigans for parents and kids',
    'family matching hoodies for parents and kids',
    'family matching sets for parents and kids',
    'family matching shirts for parents and kids',
    'family matching sweaters for parents and kids',
    'family matching t-shirts for parents and kids',
    'mommy and me cardigans for moms and daughters',
    'mommy and me matching sets for moms and daughters',
    'mommy and me maxi dresses for moms and daughters',
    'mommy and me midi dresses for moms and daughters',
    'mommy and me pajama sets for moms and daughters',
    'mommy and me sundresses for moms and daughters',
]
attributes = ['beige', 'black white striped', 'blue', 'blue floral print', 'cartoon print', 'color block', 'cream', 'cream black heart print', 'fleece', 'floral print', 'gingham print', 'graphic print', 'green floral print', 'heart patch', 'heart print', 'matching style', 'navy floral print', 'navy gingham print', 'navy red striped', 'pink', 'pink blue ombre', 'rainbow stripe', 'striped', 'tropical print', 'watercolor', 'yellow', 'yellow tropical print']
occasions = ['bedtime, sleepovers, and cozy family nights', 'casual days, coordinated outings, and matching photos', 'cozy days, holiday moments, and family photos', 'easy coordinated looks, vacations, and family photos', 'family photos, parties, and everyday matching moments']

category_translations = {
    'ru': ['комплекты в едином стиле для пап и детей', 'рубашки на пуговицах в едином стиле для всей семьи — родителей и детей', 'кардиганы в едином стиле для всей семьи — родителей и детей', 'худи в едином стиле для всей семьи — родителей и детей', 'комплекты в едином стиле для всей семьи — родителей и детей', 'рубашки в едином стиле для всей семьи — родителей и детей', 'свитеры в едином стиле для всей семьи — родителей и детей', 'футболки в едином стиле для всей семьи — родителей и детей', 'кардиганы в едином стиле для мам и дочерей', 'комплекты в едином стиле для мам и дочерей', 'платья макси в едином стиле для мам и дочерей', 'платья миди в едином стиле для мам и дочерей', 'пижамные комплекты в едином стиле для мам и дочерей', 'сарафаны в едином стиле для мам и дочерей'],
    'sv': ['matchande set för pappor och barn', 'matchande skjortor med knappar för hela familjen, föräldrar och barn', 'matchande koftor för hela familjen, föräldrar och barn', 'matchande huvtröjor för hela familjen, föräldrar och barn', 'matchande set för hela familjen, föräldrar och barn', 'matchande skjortor för hela familjen, föräldrar och barn', 'matchande tröjor för hela familjen, föräldrar och barn', 'matchande t-shirts för hela familjen, föräldrar och barn', 'matchande koftor för mammor och döttrar', 'matchande set för mammor och döttrar', 'matchande maxiklänningar för mammor och döttrar', 'matchande midiklänningar för mammor och döttrar', 'matchande pyjamasset för mammor och döttrar', 'matchande sommarklänningar för mammor och döttrar'],
}
attribute_translations = {
    'ru': ['бежевого цвета', 'в чёрно-белую полоску', 'синего цвета', 'с синим цветочным принтом', 'с мультяшным принтом', 'с цветовыми блоками', 'кремового цвета', 'с принтом в виде сердечек в кремовых и чёрных тонах', 'из флиса', 'с цветочным принтом', 'с принтом в клетку виши', 'с графическим принтом', 'с зелёным цветочным принтом', 'с нашивкой в виде сердца', 'с принтом в виде сердечек', 'с согласованным дизайном', 'с тёмно-синим цветочным принтом', 'с тёмно-синим принтом в клетку виши', 'в тёмно-синюю и красную полоску', 'розового цвета', 'с розово-голубым градиентом омбре', 'в радужную полоску', 'в полоску', 'с тропическим принтом', 'с акварельным дизайном', 'жёлтого цвета', 'с жёлтым тропическим принтом'],
    'sv': ['i beige', 'med svarta och vita ränder', 'i blått', 'med blått blommönster', 'med tecknade motiv', 'med färgblock', 'i gräddvitt', 'med hjärtmönster i gräddvitt och svart', 'i fleece', 'med blommönster', 'med ginghamrutor', 'med grafiskt tryck', 'med grönt blommönster', 'med en hjärtformad applikation', 'med hjärtmönster', 'med samordnad stil', 'med marinblått blommönster', 'med marinblå ginghamrutor', 'med marinblå och röda ränder', 'i rosa', 'med rosa och blå färgtoning', 'med regnbågsränder', 'med ränder', 'med tropiskt mönster', 'med akvarellmönster', 'i gult', 'med gult tropiskt mönster'],
}
occasion_translations = {
    'ru': ['Идеально для сна, ночёвок в гостях и уютных семейных вечеров.', 'Идеально для повседневных дней, совместных выходов в согласованных образах и фотографий в едином стиле.', 'Идеально для уютных дней, праздничных моментов и семейных фотографий.', 'Идеально для лёгкого создания согласованных образов, отпуска и семейных фотографий.', 'Идеально для семейных фотографий, вечеринок и повседневных моментов в едином стиле.'],
    'sv': ['Perfekt för läggdags, övernattningar och mysiga familjekvällar.', 'Perfekt för lediga dagar, utflykter i samordnad stil och matchande foton.', 'Perfekt för mysiga dagar, högtidsstunder och familjefoton.', 'Perfekt för enkla samordnade stilar, semestrar och familjefoton.', 'Perfekt för familjefoton, fester och matchande stunder i vardagen.'],
}
C = {lang: dict(zip(categories, values)) for lang, values in category_translations.items()}
A = {lang: dict(zip(attributes, values)) for lang, values in attribute_translations.items()}
O = {lang: dict(zip(occasions, values)) for lang, values in occasion_translations.items()}
for values in category_translations.values():
    assert len(values) == len(categories)
for values in attribute_translations.values():
    assert len(values) == len(attributes)
for values in occasion_translations.values():
    assert len(values) == len(occasions)

# Other locales contain only the exact category/feature subsets below.
subset_categories = [categories[1], categories[4], categories[7]]
subset_attributes = ['beige', 'blue floral print', 'floral print', 'graphic print', 'green floral print', 'heart print', 'matching style', 'navy floral print', 'striped']
subset_occasions = [occasions[1], occasions[3]]
extra = {
    'ar': {
        'c': ['قمصان عائلية متناسقة بأزرار للوالدين والأطفال', 'أطقم عائلية متناسقة للوالدين والأطفال', 'تيشيرتات عائلية متناسقة للوالدين والأطفال'],
        'a': ['باللون البيج', 'بنقشة زهور زرقاء', 'بنقشة زهور', 'بطبعة رسومية', 'بنقشة زهور خضراء', 'بنقشة قلوب', 'بتصميم متناسق', 'بنقشة زهور باللون الكحلي', 'بنقشة مخططة'],
        'o': ['مثالية للأيام العادية والنزهات بإطلالات متناسقة والصور بملابس متطابقة.', 'مثالية لإطلالات متناسقة بسهولة والعطلات والصور العائلية.'],
    },
    'fr': {
        'c': ['des chemises à boutons assorties pour toute la famille, parents et enfants', 'des ensembles assortis pour toute la famille, parents et enfants', 'des t-shirts assortis pour toute la famille, parents et enfants'],
        'a': ['en beige', 'avec un imprimé floral bleu', 'avec un imprimé floral', 'avec un imprimé graphique', 'avec un imprimé floral vert', 'avec un imprimé cœur', 'au style coordonné', 'avec un imprimé floral bleu marine', 'à rayures'],
        'o': ['Parfaits pour les journées décontractées, les sorties en tenues coordonnées et les photos assorties.', 'Parfaits pour créer facilement des looks coordonnés, les vacances et les photos de famille.'],
    },
    'it': {
        'c': ['camicie abbinate con bottoni per tutta la famiglia, genitori e bambini', 'completi abbinati per tutta la famiglia, genitori e bambini', 't-shirt abbinate per tutta la famiglia, genitori e bambini'],
        'a': ['in beige', 'con stampa floreale blu', 'con stampa floreale', 'con stampa grafica', 'con stampa floreale verde', 'con stampa a cuori', 'dallo stile coordinato', 'con stampa floreale blu navy', 'a righe'],
        'o': ['Ideali per le giornate informali, le uscite in coordinato e le foto con abiti abbinati.', 'Ideali per creare facilmente look coordinati, per le vacanze e le foto di famiglia.'],
    },
    'ja': {
        'c': ['親子向けの家族おそろいのボタンダウンシャツ', '親子向けの家族おそろいのセットアップ', '親子向けの家族おそろいのTシャツ'],
        'a': ['ベージュ', 'ブルーの花柄', '花柄', 'グラフィックプリント', 'グリーンの花柄', 'ハート柄', 'おそろいのスタイル', 'ネイビーの花柄', 'ストライプ柄'],
        'o': ['普段の日やおそろいコーデでのお出かけ、おそろい写真にぴったりです。', '手軽なおそろいコーデや休暇、家族写真にぴったりです。'],
    },
    'nl': {
        'c': ['bijpassende overhemden met knopen voor het hele gezin, ouders en kinderen', 'bijpassende sets voor het hele gezin, ouders en kinderen', 'bijpassende T-shirts voor het hele gezin, ouders en kinderen'],
        'a': ['in beige', 'met blauwe bloemenprint', 'met bloemenprint', 'met grafische print', 'met groene bloemenprint', 'met hartjesprint', 'in een bijpassende stijl', 'met marineblauwe bloemenprint', 'met strepen'],
        'o': ['Perfect voor ontspannen dagen, uitstapjes in op elkaar afgestemde outfits en foto’s in bijpassende kleding.', 'Perfect voor moeiteloos op elkaar afgestemde outfits, vakanties en gezinsfoto’s.'],
    },
    'pl': {
        'c': ['pasujące do siebie koszule zapinane na guziki dla całej rodziny, rodziców i dzieci', 'pasujące do siebie zestawy dla całej rodziny, rodziców i dzieci', 'pasujące do siebie koszulki dla całej rodziny, rodziców i dzieci'],
        'a': ['w kolorze beżowym', 'z niebieskim nadrukiem kwiatowym', 'z nadrukiem kwiatowym', 'z nadrukiem graficznym', 'z zielonym nadrukiem kwiatowym', 'z nadrukiem w serca', 'w dopasowanym stylu', 'z granatowym nadrukiem kwiatowym', 'w paski'],
        'o': ['Idealne na swobodne dni, wyjścia w dopasowanych stylizacjach i zdjęcia w pasujących do siebie strojach.', 'Idealne do łatwego tworzenia dopasowanych stylizacji, na wakacje i rodzinne zdjęcia.'],
    },
}
for lang, values in extra.items():
    C[lang] = dict(zip(subset_categories, values['c']))
    A[lang] = dict(zip(subset_attributes, values['a']))
    O[lang] = dict(zip(subset_occasions, values['o']))
    assert len(values['c']) == len(subset_categories) and len(values['a']) == len(subset_attributes) and len(values['o']) == len(subset_occasions)

start = {'ru': 'Выбирайте', 'sv': 'Handla', 'ar': 'تسوّق', 'fr': 'Achetez', 'it': 'Acquista', 'nl': 'Koop', 'pl': 'Kup'}
end = {
    'ru': 'Покупайте сейчас в Dress Like Mommy. Бесплатная доставка + возврат в течение 30 дней.',
    'sv': 'Handla nu hos Dress Like Mommy. Fri frakt + 30 dagars returrätt.',
    'ar': 'تسوّق الآن لدى Dress Like Mommy. شحن مجاني + إرجاع خلال 30 يومًا.',
    'fr': 'Achetez dès maintenant chez Dress Like Mommy. Livraison gratuite + retours sous 30 jours.',
    'it': 'Acquista ora da Dress Like Mommy. Spedizione gratuita + resi entro 30 giorni.',
    'ja': 'Dress Like Mommyで今すぐお買い物。送料無料＋30日間返品対応。',
    'nl': 'Koop nu bij Dress Like Mommy. Gratis verzending + retourneren binnen 30 dagen.',
    'pl': 'Kup teraz w Dress Like Mommy. Darmowa dostawa + zwroty w ciągu 30 dni.',
}
regex = re.compile(r'^Shop (.+?) featuring (.+?)\. Perfect for (.+?)\. Shop now at Dress Like Mommy\. Free shipping \+ 30-day returns\.$')
out, checks, pairs = [], [], {}
for original in rows:
    row = copy.deepcopy(original)
    locale = row['locale']
    category, feature, occasion = regex.fullmatch(row['sourceValue']).groups()
    if locale == 'ja':
        first = C[locale][category] + 'をチェック。' + A[locale][feature] + 'が特徴です。'
        value = first + O[locale][occasion] + end[locale]
    else:
        # Attach the feature to the garment before the wearer phrase.
        markers = {'ru': ' для ', 'sv': ' för ', 'fr': ' pour ', 'it': ' per ', 'nl': ' voor ', 'pl': ' dla ', 'ar': ' للوالدين'}
        marker = markers[locale]
        garment, wearer = C[locale][category].split(marker, 1)
        first = start[locale] + ' ' + garment + ' ' + A[locale][feature] + marker + wearer + '.'
        value = first + ' ' + O[locale][occasion] + ' ' + end[locale]
    row['value'] = value
    row['sourceSHA256'] = sha(row['sourceValue'])
    row['valueSHA256'] = sha(value)
    row['marketId'] = None
    row['reason'] = 'Translate the complete current English SEO description after root disposition: the supported shipping/eligible-return shorthand is not itself a source hold; actual swimwear/category/design conflicts remain excluded.'
    row['previousSourceDisposition'] = row.get('remainderDisposition')
    row['remainderDisposition'] = 'READY_FOR_INDEPENDENT_TRANSLATION_REVIEW'
    row['dispositionReason'] = row['reason']
    row['reviewStatus'] = 'MANUALLY_AUTHORED_FULL_SOURCE_PENDING_INDEPENDENT_REVIEW'
    row['requiresFreshLiveSourceAndBeforeGuard'] = True
    row['rootSourceDisposition'] = 'AUTHORIZED_TRANSLATION_ONLY_SHORTHAND_NOT_A_GATE'
    raw_path = ROOT / 'products' / row['rawFile']
    row['rawFileResolved'] = str(raw_path.relative_to(ROOT))
    row['rawFileSHA256'] = hashlib.sha256(raw_path.read_bytes()).hexdigest()
    result = checker.verify_text(row['sourceValue'], value, locale)
    checks.append({'resourceId': row['resourceId'], 'locale': locale, 'key': row['key'], 'preservation': result})
    out.append(row)
    pairs[(locale, row['sourceValue'])] = {'locale': locale, 'sourceValue': row['sourceValue'], 'value': value}
assert len(out) == len({(r['resourceId'], r['locale'], r['key']) for r in out}) == 251
dump('candidate251.json', {'status': 'OFFLINE_SOURCE_BOUND_PENDING_INDEPENDENT_REVIEW', 'rows': out})
dump('checks251.json', {'rows': checks})
dump('assembled_review_pairs.json', {'rows': list(pairs.values())})
dump('translation_segments.json', {'categories': C, 'attributes': A, 'occasions': O, 'sourceSuffix': 'Shop now at Dress Like Mommy. Free shipping + 30-day returns.', 'targetSuffix': end})
print(json.dumps({'fields': len(out), 'uniqueCompleteTranslations': len(pairs), 'verificationExample': checks[0]['preservation']}))
