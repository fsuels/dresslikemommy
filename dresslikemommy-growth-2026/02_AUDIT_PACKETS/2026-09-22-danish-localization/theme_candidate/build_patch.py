import hashlib
import json
import pathlib
import re
import difflib

ROOT = pathlib.Path(__file__).resolve().parent
BEFORE, AFTER = ROOT / 'before', ROOT / 'theme'

def patch(name, old, new):
    path = AFTER / name
    source = path.read_text()
    assert source.count(old) == 1, (name, old[:90], source.count(old))
    path.write_text(source.replace(old, new))

for source in BEFORE.rglob('*'):
    if source.is_file():
        target = AFTER / source.relative_to(BEFORE)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(source.read_bytes())

patch('sections/footer.liquid',
      "              assign footer_journal_cta_prefix = 'Leer el '\n            endif",
      "              assign footer_journal_cta_prefix = 'Leer el '\n            elsif request.locale.iso_code == 'da'\n              assign footer_journal_summary = 'Tips til familiemode, idéer til matchende tøj og sæsonens stilguider.'\n              assign footer_journal_cta_prefix = 'Læs '\n            endif")

patch('snippets/facets.liquid',
      "    assign collection_filter_hint = 'Start with size, color, and price. Product type is already organized through the collection tabs.'",
      "    assign collection_filter_hint = 'Start with size, color, and price. Product type is already organized through the collection tabs.'\n    if request.locale.iso_code == 'da'\n      assign collection_filter_hint = 'Start med størrelse, farve og pris. Produkttyperne er allerede inddelt under kollektionens faner.'\n    endif")

blog_text = {
    'Trending now': 'Populært lige nu',
    'Family swimwear that looks polished in photos': 'Familiebadetøj, der ser flot ud på billeder',
    'Use the swim guides to compare mother-daughter swimsuits, matching family bathing suits, and beach outfits before you shop.': 'Brug badetøjsguiderne til at sammenligne badedragter til mor og datter, matchende badedragter til familien og strandtøj, før du handler.',
    'Shop swimsuits': 'Se badedragter',
    'Shop family swim': 'Se familiebadetøj',
    'Featured article': 'Udvalgt artikel',
    'min read': 'minutters læsetid',
    'Read article': 'Læs artiklen',
    'How to use the Style Journal': 'Sådan bruger du stiljournalen',
    'Find the guide, then shop the matching look': 'Find guiden, og køb det matchende look',
    "Every article is organized around a real shopping moment: family photos, beach vacations, Father's Day, Mother's Day, holidays, and everyday matching. Start with the guide that matches your occasion, then use the collection links to compare the pieces that fit.": 'Hver artikel tager udgangspunkt i en konkret anledning: familiebilleder, strandferier, fars dag, mors dag, højtider og matchende hverdagstøj. Start med den guide, der passer til din anledning, og brug derefter links til kollektionerne til at sammenligne det relevante tøj.',
    'Stay in the loop': 'Hold dig opdateret',
    'Get styling tips + 10% off': 'Få stylingtips + 10% rabat',
    'Join our Style Journal newsletter for matching outfit inspiration, new arrivals, and an exclusive welcome discount.': 'Tilmeld dig stiljournalens nyhedsbrev, og få inspiration til matchende tøj, nyheder og en eksklusiv velkomstrabat.',
    'Your email address': 'Din e-mailadresse',
    'Email address': 'E-mailadresse',
    'Subscribe': 'Tilmeld dig',
}
for english, danish in blog_text.items():
    patch('sections/main-blog.liquid', english, "{% if request.locale.iso_code == 'da' %}" + danish + '{% else %}' + english + '{% endif %}')

home = AFTER / 'snippets/home-category-localized-copy.liquid'
s = home.read_text()
start = s.index("    when 'da'")
end = s.index('    else\n', start)
danish = s[start:end]
for old, new in {
    'Gratis fragt pa alle ordrer': 'Gratis fragt på alle ordrer',
    'Hjaelp til storrelser': 'Hjælp til størrelser',
    'Matchende familietoj': 'Matchende familietøj',
    'Badetoj': 'Badetøj', 'Fodselsdage': 'Fødselsdage',
    'Blode saet til hyggelige aftener': 'Bløde sæt til hyggelige aftener',
    'Matchende far-barn-ojeblikke': 'Matchende far-barn-øjeblikke',
    'Lavet til familieportraetter': 'Lavet til familieportrætter',
    'Sode outfits til fejring': 'Søde outfits til fejring',
    'Valg til forarsbegivenheder': 'Valg til forårsbegivenheder',
    'Se matchende kjoler til foraret': 'Se matchende kjoler til foråret',
}.items():
    assert danish.count(old) == 1, old
    danish = danish.replace(old, new)
home.write_text(s[:start] + danish + s[end:])

patch('layout/theme.liquid',
      "      assign resolved_page_description = 'Shop mommy and me dresses, mother daughter matching outfits, and family matching clothes for photos, vacations, and everyday moments.'",
      "      assign resolved_page_description = 'Shop mommy and me dresses, mother daughter matching outfits, and family matching clothes for photos, vacations, and everyday moments.'\n      if request.locale.iso_code == 'da'\n        assign resolved_page_title = 'Kjoler til mor og datter | Matchende familietøj'\n        assign resolved_page_description = 'Find kjoler til mor og datter, matchende tøj til mor og barn og matchende familietøj til billeder, ferier og hverdagens øjeblikke.'\n      endif")

for filename, indent in [('snippets/header-mega-menu.liquid', '          '), ('snippets/header-drawer.liquid', '                    ')]:
    assignment = indent + "assign nav_link_title = 'Family Matching'"
    patch(filename, assignment, assignment + '\n' + indent + "if request.locale.iso_code == 'da'\n" + indent + "  assign nav_link_title = 'Matchende familietøj'\n" + indent + 'endif')
patch('snippets/header-mega-menu-feature-card.liquid',
      "    assign card_description = 'Start with family matching outfits, then branch into matching family vacation outfits, matching beach swimsuits, or daddy and me shirts.'",
      "    assign card_description = 'Start with family matching outfits, then branch into matching family vacation outfits, matching beach swimsuits, or daddy and me shirts.'\n    if request.locale.iso_code == 'da'\n      assign menu_link_display_title = 'Matchende familietøj'\n      assign card_description = 'Start med matchende familietøj, og udforsk derefter matchende ferietøj til familien, badetøj til stranden eller skjorter til far og barn.'\n    endif")

patch('snippets/header-mega-menu-feature-card.liquid', '  if custom_product_handle != blank\n', '''  if request.locale.iso_code == 'da'
    if card_cta == 'Shop the edit'
      assign card_cta = 'Se udvalget'
    else
      assign card_cta = 'Se mere'
    endif
    case card_label
      when 'Trending now'
        assign card_label = 'Populært lige nu'
      when 'Best-selling family looks'
        assign card_label = 'Mest solgte familielooks'
      when 'Resort favorite'
        assign card_label = 'Feriefavorit'
      when 'Getaway edit'
        assign card_label = 'Udvalgt til ferien'
      when 'Dress best sellers'
        assign card_label = 'Mest solgte kjoler'
      when 'Easy sets'
        assign card_label = 'Nemme sæt'
      when 'Cold-weather pick'
        assign card_label = 'Udvalgt til koldt vejr'
      when 'Pool-day favorite'
        assign card_label = 'Favorit til pooldage'
      when 'New pajama styles'
        assign card_label = 'Nye pyjamasmodeller'
    endcase
  endif

  if custom_product_handle != blank
''')

patch('snippets/collection-seo-fallback.liquid',
      "      echo meta_description_key | t\n    elsif collection_handle == 'all'",
      "      echo meta_description_key | t\n    elsif request.locale.iso_code == 'da'\n      echo 'Se '\n      echo effective_display_title\n      echo ' hos Dress Like Mommy. Sammenlign modellerne, og se størrelser og produktdetaljer på hver produktside.'\n    elsif collection_handle == 'all'")
patch('snippets/collection-seo-fallback.liquid',
      "      echo translated_body_description\n    elsif collection_handle == 'mommy-and-me'",
      "      echo translated_body_description\n    elsif request.locale.iso_code == 'da'\n      echo '<p>Se udvalget af '\n      echo effective_display_title | escape\n      echo ', og sammenlign modellerne i kollektionen.</p>'\n      echo '<p>Åbn den enkelte produktside for at se de tilgængelige varianter, størrelsesguiden og produktdetaljerne, før du vælger.</p>'\n    elsif collection_handle == 'mommy-and-me'")

callout_danish = '''  if request.locale.iso_code == 'da'
    assign primary_label = 'Se kollektionen'
    case collection_handle
      when 'matching-couples-t-shirts'
        assign callout_eyebrow = 'Find hurtigere det rette'
        assign callout_title = 'Sammenlign matchende t-shirts til par, og udforsk derefter flere matchende looks'
        assign callout_body = 'Sammenlign motiverne på t-shirts til par her på siden. Udforsk derefter matchende familietøj, hvis du ønsker mere end t-shirts.'
        assign primary_label = 'Se t-shirts nedenfor'
        assign secondary_label = 'Se matchende familietøj'
      when 'mommy-and-me'
        assign callout_eyebrow = 'Find hurtigere det rette'
        assign callout_title = 'Se hele kollektionen til mor og barn, og gå videre til de nyeste pyjamasser'
        assign callout_body = 'Start med det brede udvalg af matchende tøj her. Hvis du leder efter nattøj, kan du gå videre til kollektionen med nye pyjamasser.'
        assign primary_label = 'Se denne kollektion'
        assign secondary_label = 'Se nye pyjamasser'
        assign tertiary_label = 'Se alle pyjamasser'
      when 'matching-outfits', 'family-matching-outfits', 'new-women-outfits'
        assign callout_eyebrow = 'Find hurtigere det rette'
        assign callout_title = 'Start med familietøjet, og gå videre til de nyeste pyjamasser'
        assign callout_body = 'Sammenlign det brede udvalg af matchende familietøj her. Hvis du leder efter det nyeste nattøj, kan du gå videre til kollektionen med nye pyjamasser.'
        assign primary_label = 'Se denne kollektion'
        assign secondary_label = 'Se nye pyjamasser'
        assign tertiary_label = 'Se alle pyjamasser'
      when 'pajamas'
        assign callout_eyebrow = 'Find hurtigere det rette'
        assign callout_title = 'Se alle pyjamasser først, og gå derefter videre til nyhederne'
        assign callout_body = 'Sammenlign alle pyjamasmodellerne her. Gå videre til nyhederne, hvis du vil se de nyeste mønstre først.'
        assign primary_label = 'Se pyjamasser nedenfor'
        assign secondary_label = 'Se de seneste nyheder'
        assign tertiary_label = 'Se tøj til mor og barn'
      when 'new-pajama-drop'
        assign callout_eyebrow = 'Netop tilføjet'
        assign callout_title = 'Nye matchende pyjamasser samlet ét sted'
        assign callout_body = 'Se de nyeste mønstre samlet her. Gå videre til hele pyjamaskollektionen, hvis du vil sammenligne alle modellerne.'
        assign primary_label = 'Se nyhederne'
        assign secondary_label = 'Se alle pyjamasser'
      when 'new-matching-outfits'
        assign callout_eyebrow = 'Nye varer'
        assign callout_title = 'Se de nyeste matchende looks samlet her'
        assign callout_body = 'Start med nyhederne her, og udforsk derefter den bredere kollektion til mor og barn, hvis du vil se flere muligheder.'
        assign primary_label = 'Se nyhederne'
        assign secondary_label = 'Se tøj til mor og barn'
    endcase
    if secondary_url != blank
      assign secondary_url = routes.root_url | append: secondary_url
    endif
    if tertiary_url != blank
      assign tertiary_url = routes.root_url | append: tertiary_url
    endif
  endif

'''
patch('snippets/collection-merchandising-callout.liquid',
      '  if collection.image != blank\n', callout_danish + '  if collection.image != blank\n')
patch('snippets/collection-merchandising-callout.liquid',
      '          <li>{{ collection_live_count }} live styles</li>\n          <li>Standard shipping included</li>\n          <li>30-day return window</li>',
      "          {%- if request.locale.iso_code == 'da' -%}\n            <li>Modeller i kollektionen: {{ collection_live_count }}</li>\n            <li>Standardfragt inkluderet</li>\n            <li>30 dages returfrist</li>\n          {%- else -%}\n            <li>{{ collection_live_count }} live styles</li>\n            <li>Standard shipping included</li>\n            <li>30-day return window</li>\n          {%- endif -%}")

locale = AFTER / 'locales/da.json'
raw = locale.read_text()
data = json.loads(raw[raw.index('{'):])
header = raw[:raw.index('{')]
assert json.dumps(data, ensure_ascii=False, indent=2) + '\n' == raw[raw.index('{'):]
changes = {}

def translate(key, value):
    obj = data
    segments = key.split('.')
    for segment in segments[:-1]: obj = obj[segment]
    old = obj[segments[-1]]
    if old == value: return
    assert sorted(re.findall(r'{{.*?}}', old)) == sorted(re.findall(r'{{.*?}}', value)), key
    obj[segments[-1]] = value
    changes[key] = {'before': old, 'after': value}

replacements = {
 'sections.related_products.you_may_also_like': 'Du kan også lide',
 'sections.collection_seo.display_titles.mommy_and_me': 'Matchende tøj til mor og barn',
 'sections.collection_seo.display_titles.daddy_me': 'Matchende tøj til far og barn',
 'sections.collection_seo.display_titles.spring_matching': 'Påskekjoler til mor og barn og matchende forårstøj',
 'sections.collection_navigation.within_family_matching': 'I matchende familietøj',
 'sections.collection_navigation.within_daddy_me': 'I tøj til far og barn',
 'sections.breadcrumbs.label_trunks': 'Badebukser',
 'sections.breadcrumbs.label_button_downs': 'Skjorter med knapper',
 'products.product.occasions.title': 'Perfekt til',
 'sections.collection_seo.meta_descriptions.mommy_and_me': 'Find matchende tøj, kjoler, badedragter og sæt til mor og barn til fødselsdage, familiebilleder, ferier og matchende hverdagslooks.',
 'sections.collection_seo.meta_descriptions.spring_matching': 'Find påskekjoler til mor og barn og matchende forårstøj til kirke, brunch, æggejagt, familiebilleder og sæsonens øvrige fester.',
 'sections.collection_seo.meta_descriptions.maxi_dresses': 'Find maxikjoler til mor og barn og matchende maxikjoler til billeder, rejser, fester og velklædte hverdagslooks.',
 'sections.collection_seo.meta_descriptions.swimsuits': 'Find matchende badedragter til familien og til mor og datter til strandture, pooldage, krydstogter og matchende sommerbilleder.',
 'sections.collection_seo.meta_descriptions.family_swimsuits': 'Find matchende badedragter og badetøj til familien til strandferier, pooldage, krydstogter og matchende sommerbilleder.',
 'sections.collection_seo.meta_descriptions.family_sets': 'Find matchende ferietøj og strandsæt til familien til krydstogter, ophold på feriesteder, familiebilleder og sommerrejser.',
 'sections.collection_seo.meta_descriptions.family_matching': 'Find matchende familietøj og tøj til mor og barn til billeder, ferier, højtider og koordinerede looks til alle sæsoner.',
 'sections.collection_seo.meta_descriptions.daddy_me': 'Find skjorter, t-shirts og matchende tøj til far og barn til familiebilleder, fars dag, ferier og matchende hverdagslooks.',
 'sections.collection_seo.meta_descriptions.daddy_me_tshirts': 'Find skjorter og matchende t-shirts til far og barn til fars dag, ferier, fødselsdage, billeder og hverdagstøj til fædre og børn.',
 'sections.collection_seo.meta_descriptions.couples': 'Find matchende tøj til par med koordinerede sæt, toppe, pyjamasser og ferielooks til dates, gaver, rejser og hverdag.',
 'sections.collection_seo.meta_descriptions.couples_tshirts': 'Find matchende skjorter og t-shirts til par til dates, rejser, koncerter, højtider, gaver og koordinerede hverdagslooks.',
 'sections.collection_seo.swimsuits.title': 'Matchende badetøj til mødre, døtre og hele familien',
 'sections.collection_seo.swimsuits.copy_1': 'Start her, hvis du først vil se det brede udvalg af badetøj. Denne side samler modeller til mor og datter, matchende badedragter til familien og badetøj til ferien, så du kan sammenligne dem uden at skifte mellem flere kollektioner.',
 'sections.collection_seo.swimsuits.copy_2': 'Når du ved, hvem der skal matche, kan du gå videre til kollektionerne med familiebadetøj eller badebukser for et mere afgrænset udvalg. Find størrelsesoplysningerne på produktsiden og i størrelsesguiden til den model, du bedst kan lide.',
 'sections.collection_seo.swimsuits.family_swimwear_caption': 'Gå direkte til kollektionen med badetøj til hele familien, når alle skal matche.',
 'sections.collection_seo.swimsuits.trunks_title': 'Matchende badebukser',
 'sections.collection_seo.swimsuits.trunks_caption': 'Tilføj badetøj til far og dreng, når du vil sammensætte et komplet strandsæt.',
 'sections.collection_seo.swimsuits.mommy_me_caption': 'Fortsæt det koordinerede look ud over badetøj med matchende tøj til andre anledninger.',
 'sections.collection_seo.swimsuits.faq_answer_1': 'Størrelserne varierer efter model, så se de tilgængelige varianter, og brug størrelsesguiden på hver produktside, før du går til kassen. Denne kollektion rummer matchende badetøj til mor og datter, og nogle modeller indgår også i et bredere matchende familielook.',
 'sections.collection_seo.swimsuits.faq_question_3': 'Hvad er forskellen på badedragter til mor og barn og matchende familiebadetøj?',
 'sections.collection_seo.swimsuits.faq_answer_3': 'Badedragter til mor og barn fokuserer som regel på matchende modeller til mor og datter. Matchende familiebadetøj udvider idéen, så du kan sammensætte et koordineret look til flere familiemedlemmer, herunder far og drenge, når modellerne findes til dem.',
 'sections.collection_seo.body.family_matching_html': '<p>Se {{ title }} til familiebilleder, rejser, fødselsdage, højtider og matchende hverdagslooks. Start her, når du vil sammenligne koordineret tøj til familien, før du vælger en mere afgrænset kollektion med kjoler, badetøj eller feriesæt.</p>',
}
for key, value in replacements.items(): translate(key, value)
for key in ['sections.collection_seo.body.swimsuits_html', 'sections.collection_seo.body.family_swimsuits_html', 'sections.collection_seo.rich_parts.family_swimsuits.part_4_html', 'sections.collection_seo.rich_parts.family_swimsuits.part_5_html', 'sections.collection_seo.rich_parts.daddy_me.part_9_html']:
    obj=data
    for segment in key.split('.'):obj=obj[segment]
    translate(key,obj.replace('kufferter','badebukser'))
for key in ['sections.collection_seo.rich_parts.dresses.part_1_html','sections.collection_seo.rich_parts.mommy_and_me.part_1_html']:
    obj=data
    for segment in key.split('.'):obj=obj[segment]
    translate(key,obj.replace('venskabsbyer','matchende looks'))
raw = header + json.dumps(data, ensure_ascii=False, indent=2) + '\n'
locale.write_text(raw)
assert json.loads(raw[raw.index('{'):]) == data
(ROOT / 'locale_changes.json').write_text(json.dumps(changes, ensure_ascii=False, indent=2)+'\n')

manifest=[]
diff=[]
for source in sorted(BEFORE.rglob('*')):
    if not source.is_file():continue
    name=source.relative_to(BEFORE).as_posix();old=source.read_bytes();new=(AFTER/name).read_bytes()
    manifest.append({'filename':name,'sourceMd5':hashlib.md5(old).hexdigest(),'sourceSha256':hashlib.sha256(old).hexdigest(),'candidateMd5':hashlib.md5(new).hexdigest(),'candidateSha256':hashlib.sha256(new).hexdigest()})
    diff.extend(difflib.unified_diff(old.decode().splitlines(True),new.decode().splitlines(True),fromfile='before/'+name,tofile='theme/'+name))
(ROOT/'MANIFEST.json').write_text(json.dumps({'themeId':'137888792673','files':manifest,'localeValuesChanged':len(changes)},indent=2)+'\n')
(ROOT/'changes.diff').write_text(''.join(diff))
print(json.dumps({'files':len(manifest),'localeValuesChanged':len(changes)},indent=2))
