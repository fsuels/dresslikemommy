document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('[id^="MainProduct-"][data-section]').forEach(function (productSection) {
    try {
      initDesktopProductMediaFlow(productSection);
    } catch (error) {
      console.error('Product desktop media flow init failed', error);
    }
  });

  document.querySelectorAll('[data-product-desktop-ux]').forEach(function (wrapper) {
    try {
      initProductDesktopUx(wrapper);
    } catch (error) {
      console.error('Product desktop UX init failed', error);
    }
  });
});

function initDesktopProductMediaFlow(productSection) {
  var sectionId = productSection.getAttribute('data-section');
  if (!sectionId) return;

  var desktopMediaQuery = window.matchMedia('(min-width: 990px)');
  var mediaWrapper = productSection.querySelector('.product__media-wrapper');
  var productInfo = document.getElementById('ProductInfo-' + sectionId);
  if (!mediaWrapper || !productInfo) return;

  var state = {
    active: false,
    maxOffset: 0,
    ticking: false,
  };

  var clearDesktopMediaFlow = function () {
    state.active = false;
    state.maxOffset = 0;
    productSection.classList.remove('product-section--desktop-media-flow');
    productSection.style.setProperty('--desktop-media-flow-offset', '0px');
  };

  var getDesktopMediaFlowAnchorOffset = function (mediaTop, mediaHeight, maxOffset) {
    var candidates = productSection.querySelectorAll(
      '[data-product-description], .product__accordion, product-recommendations, .product__view-details'
    );
    var gap = 24;

    for (var index = 0; index < candidates.length; index += 1) {
      var candidate = candidates[index];
      if (!candidate || candidate.offsetParent === null) continue;

      var candidateTop = candidate.getBoundingClientRect().top + window.scrollY;
      var candidateOffset = candidateTop - mediaTop - mediaHeight - gap;
      if (candidateOffset > 0) {
        return Math.min(maxOffset, candidateOffset);
      }
    }

    return maxOffset;
  };

  var syncDesktopMediaFlow = function () {
    if (!state.active) {
      productSection.style.setProperty('--desktop-media-flow-offset', '0px');
      return;
    }

    var offset = Math.min(window.scrollY, state.maxOffset);
    productSection.style.setProperty('--desktop-media-flow-offset', Math.max(offset, 0) + 'px');
  };

  var updateDesktopMediaFlow = function () {
    if (!desktopMediaQuery.matches) {
      clearDesktopMediaFlow();
      return;
    }

    var mediaHeight = Math.ceil(mediaWrapper.getBoundingClientRect().height);
    var infoHeight = Math.ceil(productInfo.getBoundingClientRect().height);
    if (!mediaHeight || !infoHeight) {
      clearDesktopMediaFlow();
      return;
    }

    var maxOffset = Math.max(0, infoHeight - mediaHeight - 24);
    var mediaTop = mediaWrapper.getBoundingClientRect().top + window.scrollY;
    maxOffset = getDesktopMediaFlowAnchorOffset(mediaTop, mediaHeight, maxOffset);

    if (maxOffset <= 24) {
      clearDesktopMediaFlow();
      return;
    }

    state.active = true;
    state.maxOffset = maxOffset;
    productSection.classList.add('product-section--desktop-media-flow');
    syncDesktopMediaFlow();
  };

  updateDesktopMediaFlow();

  if (typeof ResizeObserver === 'function') {
    var resizeObserver = new ResizeObserver(updateDesktopMediaFlow);
    resizeObserver.observe(mediaWrapper);
    resizeObserver.observe(productInfo);
  }

  if (typeof desktopMediaQuery.addEventListener === 'function') {
    desktopMediaQuery.addEventListener('change', updateDesktopMediaFlow);
  } else if (typeof desktopMediaQuery.addListener === 'function') {
    desktopMediaQuery.addListener(updateDesktopMediaFlow);
  }

  window.addEventListener('load', updateDesktopMediaFlow, { once: true });
  window.addEventListener('resize', updateDesktopMediaFlow);
  window.addEventListener('scroll', function () {
    if (state.ticking) return;

    state.ticking = true;
    window.requestAnimationFrame(function () {
      syncDesktopMediaFlow();
      state.ticking = false;
    });
  }, { passive: true });
}

function initProductDesktopUx(wrapper) {
  var sectionId = wrapper.getAttribute('data-section-id');
  if (!sectionId) return;

  var dataScript = document.getElementById('ProductMatchingSetData-' + sectionId);
  var productData = safeParseJson(dataScript && dataScript.textContent);
  if (!productData) return;

  initDeliveryHighlights(wrapper);
  initMatchingSizeGuide(wrapper, sectionId, productData);
  initMatchingSetBuilder(wrapper, sectionId, productData);
  initPhotoReviewPanel(wrapper);
  initDesktopStickyAtc(wrapper, sectionId);
}

function safeParseJson(value) {
  if (!value) return null;
  try {
    return JSON.parse(value);
  } catch (_error) {
    return null;
  }
}

function stripDiacritics(value) {
  var text = String(value || '');
  if (typeof text.normalize !== 'function') return text;
  return text.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
}

function replaceLocaleDigits(value) {
  return String(value || '')
    .replace(/[٠-٩]/g, function (digit) {
      return String('٠١٢٣٤٥٦٧٨٩'.indexOf(digit));
    })
    .replace(/[۰-۹]/g, function (digit) {
      return String('۰۱۲۳۴۵۶۷۸۹'.indexOf(digit));
    });
}

function normalizeText(value) {
  return stripDiacritics(replaceLocaleDigits(value))
    .toLowerCase()
    .trim()
    .replace(/\s+/g, ' ');
}

function escapeHtml(value) {
  return String(value || '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function getOptionValue(variant, optionIndex) {
  return variant ? variant['option' + String(optionIndex + 1)] : '';
}

function formatMoney(cents, currency) {
  var locale = document.documentElement.getAttribute('lang') || undefined;
  try {
    return new Intl.NumberFormat(locale, {
      style: 'currency',
      currency: currency || 'USD',
      maximumFractionDigits: 2,
    }).format((Number(cents) || 0) / 100);
  } catch (_error) {
    return '$' + ((Number(cents) || 0) / 100).toFixed(2);
  }
}

function initDeliveryHighlights(wrapper) {
  wrapper.querySelectorAll('[data-desktop-estimate]').forEach(function (node) {
    var fallback = node.getAttribute('data-delivery-fallback') || node.textContent || '';
    node.textContent = fallback;
  });
}

var SIZE_LABEL_TOKENS = [
  'size',
  'sizes',
  'talla',
  'tallas',
  'tamano',
  'tamaño',
  'tamanos',
  'tamaños',
  'taille',
  'tailles',
  'pointure',
  'pointures',
  'mida',
  'mides',
  'taglia',
  'taglie',
  'tamanho',
  'tamanhos',
  'mărime',
  'marime',
  'mărimi',
  'marimi',
  'größe',
  'große',
  'maat',
  'maten',
  'velikost',
  'velikosti',
  'størrelse',
  'storrelse',
  'størrelser',
  'storrelser',
  'μέγεθος',
  'μεγεθος',
  'koko',
  'koot',
  'מידה',
  'מידות',
  'आकार',
  'साइज़',
  'サイズ',
  '사이즈',
  '크기',
  'rozmiar',
  'rozmiary',
  'размер',
  'размеры',
  'storlek',
  'storlekar',
  '尺寸',
  '尺码',
  'groesse',
  'grosse',
  'grösse',
  'größen',
  'مقاس',
  'مقاسات',
  'الحجم',
  'الأحجام',
  'الاحجام',
];
var TYPE_LABEL_TOKENS = [
  'type',
  'style',
  'tipo',
  'estilo',
  'genre',
  'coupe',
  'typ',
  'tip',
  'τύπος',
  'τυπος',
  'tyyppi',
  'sug',
  'סוג',
  'प्रकार',
  'タイプ',
  '유형',
  'тип',
  'نوع',
  'ستايل',
  'نمط',
];
var HEIGHT_LABEL_TOKENS = ['height', 'hauteur', 'altura', 'estatura', 'altezza', 'înălțime', 'inaltime', 'größe', 'große', 'körpergröße', 'korpergrosse', 'الارتفاع', 'الطول'];
var ROLE_LABELS_BY_LOCALE = {
  en: { mother: 'Mother', father: 'Father', girl: 'Girl', boy: 'Boy', child: 'Child', baby: 'Baby', adult: 'Adult' },
  ar: { mother: 'الأم', father: 'الأب', girl: 'البنت', boy: 'الولد', child: 'الأطفال', baby: 'الرضيع', adult: 'الكبار' },
  cs: { mother: 'Maminka', father: 'Tatínek', girl: 'Dívka', boy: 'Chlapec', child: 'Dítě', baby: 'Miminko', adult: 'Dospělý' },
  da: { mother: 'Mor', father: 'Far', girl: 'Pige', boy: 'Dreng', child: 'Barn', baby: 'Baby', adult: 'Voksen' },
  de: { mother: 'Mama', father: 'Papa', girl: 'Mädchen', boy: 'Junge', child: 'Kind', baby: 'Baby', adult: 'Erwachsene' },
  el: { mother: 'Μητέρα', father: 'Πατέρας', girl: 'Κορίτσι', boy: 'Αγόρι', child: 'Παιδί', baby: 'Μωρό', adult: 'Ενήλικας' },
  es: { mother: 'Mamá', father: 'Papá', girl: 'Niña', boy: 'Niño', child: 'Infantil', baby: 'Bebé', adult: 'Adulto' },
  fi: { mother: 'Äiti', father: 'Isä', girl: 'Tyttö', boy: 'Poika', child: 'Lapsi', baby: 'Vauva', adult: 'Aikuinen' },
  fr: { mother: 'Maman', father: 'Papa', girl: 'Fille', boy: 'Garçon', child: 'Enfant', baby: 'Bébé', adult: 'Adulte' },
  he: { mother: 'אמא', father: 'אבא', girl: 'ילדה', boy: 'ילד', child: 'ילדים', baby: 'תינוק', adult: 'מבוגר' },
  hi: { mother: 'माँ', father: 'पिता', girl: 'लड़की', boy: 'लड़का', child: 'बच्चा', baby: 'शिशु', adult: 'वयस्क' },
  it: { mother: 'Mamma', father: 'Papà', girl: 'Bambina', boy: 'Bambino', child: 'Bimbi', baby: 'Bebè', adult: 'Adulto' },
  ja: { mother: 'ママ', father: 'パパ', girl: '女の子', boy: '男の子', child: '子供', baby: 'ベビー', adult: '大人' },
  ko: { mother: '엄마', father: '아빠', girl: '여아', boy: '남아', child: '아동', baby: '베이비', adult: '성인' },
  nl: { mother: 'Mama', father: 'Papa', girl: 'Meisje', boy: 'Jongen', child: 'Kind', baby: 'Baby', adult: 'Volwassene' },
  no: { mother: 'Mamma', father: 'Pappa', girl: 'Jente', boy: 'Gutt', child: 'Barn', baby: 'Baby', adult: 'Voksen' },
  pl: { mother: 'Mama', father: 'Tata', girl: 'Dziewczynka', boy: 'Chłopiec', child: 'Dziecko', baby: 'Niemowlę', adult: 'Dorosły' },
  pt: { mother: 'Mãe', father: 'Pai', girl: 'Menina', boy: 'Menino', child: 'Infantil', baby: 'Bebê', adult: 'Adulto' },
  ro: { mother: 'Mamă', father: 'Tată', girl: 'Fată', boy: 'Băiat', child: 'Copil', baby: 'Bebeluș', adult: 'Adult' },
  ru: { mother: 'Мама', father: 'Папа', girl: 'Девочка', boy: 'Мальчик', child: 'Дети', baby: 'Малыш', adult: 'Взрослый' },
  sv: { mother: 'Mamma', father: 'Pappa', girl: 'Flicka', boy: 'Pojke', child: 'Barn', baby: 'Baby', adult: 'Vuxen' },
  zh: { mother: '妈妈', father: '爸爸', girl: '女孩', boy: '男孩', child: '儿童', baby: '婴儿', adult: '成人' },
};
var GARMENT_LABELS_BY_LOCALE = {
  en: { dress: 'Dress', shirt: 'Shirt', shorts: 'Shorts', top: 'Top', romper: 'Romper', pants: 'Pants', shirtShortsSet: 'Shirt & Shorts Set' },
  ar: { dress: 'فستان', shirt: 'قميص', shorts: 'شورت', top: 'توب', romper: 'رومبر', pants: 'بنطال', shirtShortsSet: 'طقم قميص وشورت' },
  cs: { dress: 'Šaty', shirt: 'Košile', shorts: 'Šortky', top: 'Top', romper: 'Overal', pants: 'Kalhoty', shirtShortsSet: 'Set košile a šortek' },
  da: { dress: 'Kjole', shirt: 'Skjorte', shorts: 'Shorts', top: 'Top', romper: 'Heldragt', pants: 'Bukser', shirtShortsSet: 'Skjorte- og shortssæt' },
  de: { dress: 'Kleid', shirt: 'Hemd', shorts: 'Shorts', top: 'Top', romper: 'Strampler', pants: 'Hose', shirtShortsSet: 'Hemd- und Shorts-Set' },
  el: { dress: 'Φόρεμα', shirt: 'Πουκάμισο', shorts: 'Σορτς', top: 'Τοπ', romper: 'Φορμάκι', pants: 'Παντελόνι', shirtShortsSet: 'Σετ πουκάμισο και σορτς' },
  es: { dress: 'Vestido', shirt: 'Camisa', shorts: 'Shorts', top: 'Top', romper: 'Pelele', pants: 'Pantalón', shirtShortsSet: 'Conjunto de camisa y shorts' },
  fi: { dress: 'Mekko', shirt: 'Paita', shorts: 'Shortsit', top: 'Yläosa', romper: 'Haalari', pants: 'Housut', shirtShortsSet: 'Paita- ja shortsisetti' },
  fr: { dress: 'Robe', shirt: 'Chemise', shorts: 'Short', top: 'Haut', romper: 'Barboteuse', pants: 'Pantalon', shirtShortsSet: 'Ensemble chemise et short' },
  he: { dress: 'שמלה', shirt: 'חולצה', shorts: 'מכנסיים קצרים', top: 'טופ', romper: 'אוברול', pants: 'מכנסיים', shirtShortsSet: 'סט חולצה ומכנסיים קצרים' },
  hi: { dress: 'ड्रेस', shirt: 'शर्ट', shorts: 'शॉर्ट्स', top: 'टॉप', romper: 'रोम्पर', pants: 'पैंट', shirtShortsSet: 'शर्ट और शॉर्ट्स सेट' },
  it: { dress: 'Vestito', shirt: 'Camicia', shorts: 'Shorts', top: 'Top', romper: 'Pagliaccetto', pants: 'Pantaloni', shirtShortsSet: 'Set camicia e shorts' },
  ja: { dress: 'ワンピース', shirt: 'シャツ', shorts: 'ショーツ', top: 'トップス', romper: 'ロンパース', pants: 'パンツ', shirtShortsSet: 'シャツ＆ショーツセット' },
  ko: { dress: '드레스', shirt: '셔츠', shorts: '반바지', top: '상의', romper: '롬퍼', pants: '바지', shirtShortsSet: '셔츠와 반바지 세트' },
  nl: { dress: 'Jurk', shirt: 'Shirt', shorts: 'Shorts', top: 'Top', romper: 'Boxpakje', pants: 'Broek', shirtShortsSet: 'Shirt- en shortset' },
  no: { dress: 'Kjole', shirt: 'Skjorte', shorts: 'Shorts', top: 'Topp', romper: 'Romper', pants: 'Bukse', shirtShortsSet: 'Skjorte- og shortsett' },
  pl: { dress: 'Sukienka', shirt: 'Koszula', shorts: 'Szorty', top: 'Top', romper: 'Rampers', pants: 'Spodnie', shirtShortsSet: 'Zestaw koszula i szorty' },
  pt: { dress: 'Vestido', shirt: 'Camisa', shorts: 'Shorts', top: 'Top', romper: 'Macacão', pants: 'Calça', shirtShortsSet: 'Conjunto de camisa e shorts' },
  ro: { dress: 'Rochie', shirt: 'Cămașă', shorts: 'Șorturi', top: 'Top', romper: 'Salopetă', pants: 'Pantaloni', shirtShortsSet: 'Set cămașă și șorturi' },
  ru: { dress: 'Платье', shirt: 'Рубашка', shorts: 'Шорты', top: 'Топ', romper: 'Ромпер', pants: 'Брюки', shirtShortsSet: 'Комплект рубашка и шорты' },
  sv: { dress: 'Klänning', shirt: 'Skjorta', shorts: 'Shorts', top: 'Topp', romper: 'Romper', pants: 'Byxor', shirtShortsSet: 'Skjorta och shorts-set' },
  zh: { dress: '连衣裙', shirt: '衬衫', shorts: '短裤', top: '上衣', romper: '连体衣', pants: '长裤', shirtShortsSet: '衬衫短裤套装' },
};
var SIZE_UNIT_LABELS_BY_LOCALE = {
  en: { year: 'Year', years: 'Years', month: 'Month', months: 'Months', joiner: ' ' },
  ar: { year: 'سنة', years: 'سنوات', month: 'شهر', months: 'أشهر', joiner: ' ' },
  cs: { year: 'rok', years: 'let', month: 'měsíc', months: 'měsíců', joiner: ' ' },
  da: { year: 'år', years: 'år', month: 'mdr.', months: 'mdr.', joiner: ' ' },
  de: { year: 'Jahr', years: 'Jahre', month: 'Monat', months: 'Monate', joiner: ' ' },
  el: { year: 'έτος', years: 'ετών', month: 'μήνας', months: 'μηνών', joiner: ' ' },
  es: { year: 'año', years: 'años', month: 'mes', months: 'meses', joiner: ' ' },
  fi: { year: 'vuosi', years: 'vuotta', month: 'kk', months: 'kk', joiner: ' ' },
  fr: { year: 'an', years: 'ans', month: 'mois', months: 'mois', joiner: ' ' },
  he: { year: 'שנה', years: 'שנים', month: 'חודש', months: 'חודשים', joiner: ' ' },
  hi: { year: 'वर्ष', years: 'वर्ष', month: 'महीना', months: 'महीने', joiner: ' ' },
  it: { year: 'anno', years: 'anni', month: 'mese', months: 'mesi', joiner: ' ' },
  ja: { year: '歳', years: '歳', month: 'か月', months: 'か月', joiner: '' },
  ko: { year: '세', years: '세', month: '개월', months: '개월', joiner: '' },
  nl: { year: 'jaar', years: 'jaar', month: 'maand', months: 'maanden', joiner: ' ' },
  no: { year: 'år', years: 'år', month: 'mnd.', months: 'mnd.', joiner: ' ' },
  pl: { year: 'rok', years: 'lat', month: 'mies.', months: 'mies.', joiner: ' ' },
  pt: { year: 'ano', years: 'anos', month: 'mês', months: 'meses', joiner: ' ' },
  ro: { year: 'an', years: 'ani', month: 'lună', months: 'luni', joiner: ' ' },
  ru: { year: 'год', years: 'лет', month: 'мес.', months: 'мес.', joiner: ' ' },
  sv: { year: 'år', years: 'år', month: 'mån', months: 'mån', joiner: ' ' },
  zh: { year: '岁', years: '岁', month: '个月', months: '个月', joiner: '' },
};
var UI_LABELS_BY_LOCALE = {
  en: {
    pieceOne: '1 Matching Piece',
    pieceMany: '{count} Matching Pieces',
    total: 'Total',
    each: 'each',
    units: 'Units',
    closeSizeDetails: 'Close size details',
    outOfStockCurrent: 'Out of stock for current selection',
    notAvailableSelectedSize: 'Not available in your selected size',
    pickSize: 'Pick a size',
    pickAxis: 'Pick a {axis}',
    removeRole: 'Remove {role}',
    decreaseQuantity: 'Decrease quantity',
    increaseQuantity: 'Increase quantity',
    findFit: "Find {role}'s fit",
    addRole: '+ Add {role}',
    addAnotherFamilyMember: 'Add another family member',
    customerPhotos: 'Customer photos',
  },
  cs: {
    pieceOne: '1 ladící kus',
    pieceMany: '{count} ladících kusů',
    total: 'Celkem',
    each: 'za kus',
    units: 'Jednotky',
    closeSizeDetails: 'Zavřít detaily velikosti',
    outOfStockCurrent: 'Není skladem pro aktuální výběr',
    notAvailableSelectedSize: 'Není dostupné ve vybrané velikosti',
    pickSize: 'Vyberte velikost',
    pickAxis: 'Vyberte {axis}',
    removeRole: 'Odebrat {role}',
    decreaseQuantity: 'Snížit množství',
    increaseQuantity: 'Zvýšit množství',
    findFit: 'Najít velikost pro {role}',
    addRole: '+ Přidat {role}',
    addAnotherFamilyMember: 'Přidat dalšího člena rodiny',
    customerPhotos: 'Fotky zákazníků',
  },
  da: {
    pieceOne: '1 matchende del',
    pieceMany: '{count} matchende dele',
    total: 'I alt',
    each: 'stk.',
    units: 'Enheder',
    closeSizeDetails: 'Luk størrelsesdetaljer',
    outOfStockCurrent: 'Udsolgt for det aktuelle valg',
    notAvailableSelectedSize: 'Ikke tilgængelig i den valgte størrelse',
    pickSize: 'Vælg en størrelse',
    pickAxis: 'Vælg {axis}',
    removeRole: 'Fjern {role}',
    decreaseQuantity: 'Sænk antal',
    increaseQuantity: 'Øg antal',
    findFit: 'Find pasform til {role}',
    addRole: '+ Tilføj {role}',
    addAnotherFamilyMember: 'Tilføj endnu et familiemedlem',
    customerPhotos: 'Kundebilleder',
  },
  de: {
    pieceOne: '1 passendes Teil',
    pieceMany: '{count} passende Teile',
    total: 'Gesamt',
    each: 'pro Stück',
    units: 'Einheiten',
    closeSizeDetails: 'Größendetails schließen',
    outOfStockCurrent: 'Für die aktuelle Auswahl ausverkauft',
    notAvailableSelectedSize: 'In der gewählten Größe nicht verfügbar',
    pickSize: 'Größe wählen',
    pickAxis: '{axis} wählen',
    removeRole: '{role} entfernen',
    decreaseQuantity: 'Menge verringern',
    increaseQuantity: 'Menge erhöhen',
    findFit: 'Passform für {role} finden',
    addRole: '+ {role} hinzufügen',
    addAnotherFamilyMember: 'Weiteres Familienmitglied hinzufügen',
    customerPhotos: 'Kundenfotos',
  },
  el: {
    pieceOne: '1 ασορτί κομμάτι',
    pieceMany: '{count} ασορτί κομμάτια',
    total: 'Σύνολο',
    each: 'το καθένα',
    units: 'Μονάδες',
    closeSizeDetails: 'Κλείσιμο λεπτομερειών μεγέθους',
    outOfStockCurrent: 'Εξαντλημένο για την τρέχουσα επιλογή',
    notAvailableSelectedSize: 'Δεν είναι διαθέσιμο στο επιλεγμένο μέγεθος',
    pickSize: 'Επιλέξτε μέγεθος',
    pickAxis: 'Επιλέξτε {axis}',
    removeRole: 'Αφαίρεση {role}',
    decreaseQuantity: 'Μείωση ποσότητας',
    increaseQuantity: 'Αύξηση ποσότητας',
    findFit: 'Βρείτε εφαρμογή για {role}',
    addRole: '+ Προσθήκη {role}',
    addAnotherFamilyMember: 'Προσθήκη άλλου μέλους οικογένειας',
    customerPhotos: 'Φωτογραφίες πελατών',
  },
  es: {
    pieceOne: '1 pieza a juego',
    pieceMany: '{count} piezas a juego',
    total: 'Total',
    each: 'cada una',
    units: 'Unidades',
    closeSizeDetails: 'Cerrar detalles de talla',
    outOfStockCurrent: 'Agotado para la selección actual',
    notAvailableSelectedSize: 'No disponible en la talla seleccionada',
    pickSize: 'Elige una talla',
    pickAxis: 'Elige {axis}',
    removeRole: 'Quitar {role}',
    decreaseQuantity: 'Disminuir cantidad',
    increaseQuantity: 'Aumentar cantidad',
    findFit: 'Ver talla de {role}',
    addRole: '+ Añadir {role}',
    addAnotherFamilyMember: 'Añadir otro familiar',
    customerPhotos: 'Fotos de clientes',
  },
  fr: {
    pieceOne: '1 pièce assortie',
    pieceMany: '{count} pièces assorties',
    total: 'Total',
    each: 'chacune',
    units: 'Unités',
    closeSizeDetails: 'Fermer les détails de taille',
    outOfStockCurrent: 'En rupture pour la sélection actuelle',
    notAvailableSelectedSize: 'Non disponible dans la taille sélectionnée',
    pickSize: 'Choisissez une taille',
    pickAxis: 'Choisissez {axis}',
    removeRole: 'Retirer {role}',
    decreaseQuantity: 'Diminuer la quantité',
    increaseQuantity: 'Augmenter la quantité',
    findFit: 'Trouver la taille pour {role}',
    addRole: '+ Ajouter {role}',
    addAnotherFamilyMember: 'Ajouter un autre membre de la famille',
    customerPhotos: 'Photos clients',
  },
  it: {
    pieceOne: '1 capo coordinato',
    pieceMany: '{count} capi coordinati',
    total: 'Totale',
    each: 'ciascuno',
    units: 'Unità',
    closeSizeDetails: 'Chiudi dettagli taglia',
    outOfStockCurrent: 'Esaurito per la selezione attuale',
    notAvailableSelectedSize: 'Non disponibile nella taglia selezionata',
    pickSize: 'Scegli una taglia',
    pickAxis: 'Scegli {axis}',
    removeRole: 'Rimuovi {role}',
    decreaseQuantity: 'Diminuisci quantità',
    increaseQuantity: 'Aumenta quantità',
    findFit: 'Trova la vestibilità per {role}',
    addRole: '+ Aggiungi {role}',
    addAnotherFamilyMember: 'Aggiungi un altro familiare',
    customerPhotos: 'Foto dei clienti',
  },
  nl: {
    pieceOne: '1 matchend item',
    pieceMany: '{count} matchende items',
    total: 'Totaal',
    each: 'per stuk',
    units: 'Eenheden',
    closeSizeDetails: 'Maatdetails sluiten',
    outOfStockCurrent: 'Uitverkocht voor de huidige selectie',
    notAvailableSelectedSize: 'Niet beschikbaar in de geselecteerde maat',
    pickSize: 'Kies een maat',
    pickAxis: 'Kies {axis}',
    removeRole: '{role} verwijderen',
    decreaseQuantity: 'Aantal verlagen',
    increaseQuantity: 'Aantal verhogen',
    findFit: 'Vind de pasvorm voor {role}',
    addRole: '+ {role} toevoegen',
    addAnotherFamilyMember: 'Nog een gezinslid toevoegen',
    customerPhotos: "Foto's van klanten",
  },
  pl: {
    pieceOne: '1 pasujący element',
    pieceMany: '{count} pasujących elementów',
    total: 'Razem',
    each: 'za sztukę',
    units: 'Jednostki',
    closeSizeDetails: 'Zamknij szczegóły rozmiaru',
    outOfStockCurrent: 'Wyprzedane dla bieżącego wyboru',
    notAvailableSelectedSize: 'Niedostępne w wybranym rozmiarze',
    pickSize: 'Wybierz rozmiar',
    pickAxis: 'Wybierz {axis}',
    removeRole: 'Usuń {role}',
    decreaseQuantity: 'Zmniejsz ilość',
    increaseQuantity: 'Zwiększ ilość',
    findFit: 'Znajdź rozmiar dla {role}',
    addRole: '+ Dodaj {role}',
    addAnotherFamilyMember: 'Dodaj kolejnego członka rodziny',
    customerPhotos: 'Zdjęcia klientów',
  },
  pt: {
    pieceOne: '1 peça combinando',
    pieceMany: '{count} peças combinando',
    total: 'Total',
    each: 'cada',
    units: 'Unidades',
    closeSizeDetails: 'Fechar detalhes de tamanho',
    outOfStockCurrent: 'Esgotado para a seleção atual',
    notAvailableSelectedSize: 'Não disponível no tamanho selecionado',
    pickSize: 'Escolha um tamanho',
    pickAxis: 'Escolha {axis}',
    removeRole: 'Remover {role}',
    decreaseQuantity: 'Diminuir quantidade',
    increaseQuantity: 'Aumentar quantidade',
    findFit: 'Encontrar caimento para {role}',
    addRole: '+ Adicionar {role}',
    addAnotherFamilyMember: 'Adicionar outro familiar',
    customerPhotos: 'Fotos de clientes',
  },
  ro: {
    pieceOne: '1 piesă asortată',
    pieceMany: '{count} piese asortate',
    total: 'Total',
    each: 'fiecare',
    units: 'Unități',
    closeSizeDetails: 'Închide detaliile mărimii',
    outOfStockCurrent: 'Stoc epuizat pentru selecția curentă',
    notAvailableSelectedSize: 'Indisponibil pentru mărimea selectată',
    pickSize: 'Alege o mărime',
    pickAxis: 'Alege {axis}',
    removeRole: 'Elimină {role}',
    decreaseQuantity: 'Scade cantitatea',
    increaseQuantity: 'Crește cantitatea',
    findFit: 'Găsește potrivirea pentru {role}',
    addRole: '+ Adaugă {role}',
    addAnotherFamilyMember: 'Adaugă un alt membru al familiei',
    customerPhotos: 'Fotografii de la clienți',
  },
  sv: {
    pieceOne: '1 matchande del',
    pieceMany: '{count} matchande delar',
    total: 'Totalt',
    each: 'styck',
    units: 'Enheter',
    closeSizeDetails: 'Stäng storleksdetaljer',
    outOfStockCurrent: 'Slut i lager för aktuellt val',
    notAvailableSelectedSize: 'Inte tillgänglig i vald storlek',
    pickSize: 'Välj storlek',
    pickAxis: 'Välj {axis}',
    removeRole: 'Ta bort {role}',
    decreaseQuantity: 'Minska antal',
    increaseQuantity: 'Öka antal',
    findFit: 'Hitta passform för {role}',
    addRole: '+ Lägg till {role}',
    addAnotherFamilyMember: 'Lägg till en familjemedlem',
    customerPhotos: 'Kundfoton',
  },
};
var GUIDE_MEASUREMENT_TOKENS = [
  'length',
  'bust',
  'chest',
  'waist',
  'hips',
  'height',
  'weight',
  'shoulder',
  'sleeve',
  'age',
  'longueur',
  'poitrine',
  'taille',
  'hanches',
  'hauteur',
  'poids',
  'epaule',
  'épaule',
  'manche',
  'âge',
  'largo',
  'pecho',
  'cintura',
  'cadera',
  'altura',
  'peso',
  'hombro',
  'manga',
  'edad',
  'الطول',
  'الصدر',
  'الخصر',
  'الورك',
  'الكتف',
  'الارتفاع',
  'الوزن',
  'العمر',
];
var GUIDE_UNIT_TOKENS = [
  'cm',
  'cms',
  'centimeter',
  'centimeters',
  'centimetre',
  'centimetres',
  'in',
  'inch',
  'inches',
  'kg',
  'kgs',
  'kilogram',
  'kilograms',
  'lb',
  'lbs',
  'سم',
  'بوصة',
  'بوصات',
  'انش',
  'إنش',
  'كجم',
  'كغ',
  'رطل',
  'ارطال',
  'أرطال',
];
var ROLE_DEFINITIONS = [
  {
    key: 'mother',
    label: 'Mother',
    labels: { ar: 'الأم', es: 'Mamá', fr: 'Maman' },
    aliases: ['mother', 'mom', 'mom dress', 'madre', 'mama', 'mamá', 'mamă', 'mere', 'mère', 'maman', 'mutter', 'mãe', 'mae', 'moeder', 'mor', 'äiti', 'mamma', 'maminka', 'אמא', 'mama', 'мама', 'мать', '妈妈', '媽媽', 'ママ', '엄마', '어머니', 'माँ', 'الأم', 'الام'],
  },
  {
    key: 'father',
    label: 'Father',
    labels: { ar: 'الأب', es: 'Papá', fr: 'Papa' },
    aliases: ['father', 'dad', 'dad shirt', 'padre', 'papa', 'papá', 'pere', 'père', 'vater', 'pai', 'vader', 'far', 'isä', 'papà', 'tatínek', 'אבא', 'папа', 'отец', '爸爸', 'パパ', '아빠', 'पिता', 'الأب', 'الاب'],
  },
  {
    key: 'girl',
    label: 'Girl',
    labels: { ar: 'البنت', es: 'Niña', fr: 'Fille' },
    aliases: ['girl', 'daughter', 'daughter dress', 'hija', 'filha', 'figlia', 'tochter', 'fille', 'daughter', 'nina', 'niña', 'menina', 'ragazza', 'bambina', 'tyttö', 'mädchen', 'maedchen', 'pige', 'jente', 'flicka', 'dziewczynka', 'dívka', 'κορίτσι', 'fată', 'אילדה', 'ילדה', 'девочка', 'дочь', '女孩', '女の子', '娘', '여아', '딸', 'लड़की', 'البنت', 'ابنة', 'الابنة', 'فتاة', 'الفتاة'],
  },
  {
    key: 'boy',
    label: 'Boy',
    labels: { ar: 'الولد', es: 'Niño', fr: 'Garçon' },
    aliases: ['boy', 'son', 'son shirt', 'hijo', 'filho', 'figlio', 'sohn', 'fils', 'nino', 'niño', 'garcon', 'garçon', 'menino', 'ragazzo', 'junge', 'dreng', 'gutt', 'pojke', 'chłopiec', 'chlapec', 'ילד', 'мальчик', 'сын', '男孩', '男の子', '息子', '남아', '아들', 'लड़का', 'الولد', 'ابن', 'الابن', 'ولد', 'فتى', 'الفتى'],
  },
  {
    key: 'child',
    label: 'Child',
    labels: { ar: 'الطفل', es: 'Infantil', fr: 'Enfant' },
    aliases: ['child', 'children', 'kid', 'kids', 'infantil', 'enfant', 'enfants', 'infant', 'kind', 'kinder', 'bambini', 'barn', 'dziecko', 'dzieci', 'dítě', 'детский', 'ребенок', 'ребёнок', '儿童', '兒童', '子供', '아동', 'ילדים', 'बच्चा', 'طفل', 'الطفل', 'أطفال', 'اطفال'],
  },
  {
    key: 'baby',
    label: 'Baby',
    labels: { ar: 'الرضيع', es: 'Bebé', fr: 'Bébé' },
    aliases: ['baby', 'bebe', 'bebé', 'bébé', 'رضيع', 'بيبي'],
  },
  {
    key: 'adult',
    label: 'Adult',
    labels: { ar: 'الكبار', es: 'Adulto', fr: 'Adulte' },
    aliases: ['adult', 'adults', 'adulto', 'adulta', 'adultes', 'adulte', 'بالغ', 'بالغة', 'بالغين', 'البالغين', 'الكبار', 'للكبار'],
  },
];
var ROLE_FIT_COPY_BY_LOCALE = {
  en: {
    mother: "Fit tip: compare with your usual women's size.",
    father: "Fit tip: compare with your usual men's size.",
    girl: "Fit tip: compare with her usual kids' size.",
    boy: "Fit tip: compare with his usual kids' size.",
    child: "Fit tip: compare with the child's usual size.",
    baby: "Fit tip: compare with the baby's usual size.",
    adult: 'Fit tip: compare with your usual adult size.',
  },
  es: {
    mother: 'Consejo: compáralo con tu talla habitual de mujer.',
    father: 'Consejo: compáralo con tu talla habitual de hombre.',
    girl: 'Consejo: compáralo con su talla infantil habitual.',
    boy: 'Consejo: compáralo con su talla infantil habitual.',
    child: 'Consejo: compáralo con su talla infantil habitual.',
    baby: 'Consejo: compáralo con la talla habitual del bebé.',
    adult: 'Consejo: compáralo con tu talla habitual de adulto.',
  },
  fr: {
    mother: 'Conseil coupe : comparez avec votre taille femme habituelle.',
    father: 'Conseil coupe : comparez avec votre taille homme habituelle.',
    girl: 'Conseil coupe : comparez avec sa taille enfant habituelle.',
    boy: 'Conseil coupe : comparez avec sa taille enfant habituelle.',
    child: "Conseil coupe : comparez avec la taille habituelle de l'enfant.",
    baby: 'Conseil coupe : comparez avec la taille habituelle du bébé.',
    adult: 'Conseil coupe : comparez avec votre taille adulte habituelle.',
  },
  ja: {
    mother: 'フィットの目安：普段のレディースサイズと比べてください。',
    father: 'フィットの目安：普段のメンズサイズと比べてください。',
    girl: 'フィットの目安：普段のお子さまサイズと比べてください。',
    boy: 'フィットの目安：普段のお子さまサイズと比べてください。',
    child: 'フィットの目安：お子さまの普段のサイズと比べてください。',
    baby: 'フィットの目安：赤ちゃんの普段のサイズと比べてください。',
    adult: 'フィットの目安：普段の大人サイズと比べてください。',
  },
  ar: {
    mother: 'نصيحة للمقاس: قارنيها بمقاسك المعتاد للسيدات.',
    father: 'نصيحة للمقاس: قارنها بمقاسك المعتاد للرجال.',
    girl: 'نصيحة للمقاس: قارنيها بمقاسها المعتاد للأطفال.',
    boy: 'نصيحة للمقاس: قارنه بمقاسه المعتاد للأطفال.',
    child: 'نصيحة للمقاس: قارنيه بمقاس الطفل المعتاد.',
    baby: 'نصيحة للمقاس: قارنيه بمقاس الرضيع المعتاد.',
    adult: 'نصيحة للمقاس: قارنيه بمقاس البالغ المعتاد.',
  },
};
var IMAGE_BASED_SIZE_GUIDE_PRESETS = [
  {
    imageTokens: ['htb1s.5.shppk1rjszffq6y5ppxav', 'htb1oo6bshvpk1rjszpiq6zmwxxaa'],
    headers: [
      'Size',
      'Estimated Height (cm)',
      'Son Shirt Bust (cm/in)',
      'Son Shirt Shoulder (cm/in)',
      'Son Shirt Length (cm/in)',
      'Daughter Dress Bust (cm/in)',
      'Daughter Dress Length (cm/in)',
      'Dad Shirt Bust (cm/in)',
      'Dad Shirt Shoulder (cm/in)',
      'Dad Shirt Length (cm/in)',
      'Mom Dress Bust (cm/in)',
      'Mom Dress Length (cm/in)',
    ],
    rows: [
      ['24M/90', '90', '57/22.44', '25/9.84', '38/14.96', '58/22.83', '58/22.83', '—', '—', '—', '—', '—'],
      ['3T/100', '90-100', '61/24.02', '26/10.24', '41/16.14', '62/24.41', '62/24.41', '—', '—', '—', '—', '—'],
      ['4T/110', '100-110', '65/25.59', '27/10.63', '44/17.32', '66/25.98', '66/25.98', '—', '—', '—', '—', '—'],
      ['5T/120', '110-120', '69/27.17', '29/11.42', '47/18.50', '71/27.95', '71/27.95', '—', '—', '—', '—', '—'],
      ['6T/130', '120-130', '73/28.74', '30/11.81', '50/19.69', '77/30.31', '77/30.31', '—', '—', '—', '—', '—'],
      ['8T/140', '130-140', '77/30.31', '32/12.60', '53/20.87', '84/33.07', '84/33.07', '—', '—', '—', '—', '—'],
      ['10T/150', '140-150', '81/31.89', '33/12.99', '56/22.05', '91/35.83', '91/35.83', '—', '—', '—', '—', '—'],
      ['S', '—', '—', '—', '—', '—', '—', '—', '—', '—', '94/37.01', '114/44.88'],
      ['M', '—', '—', '—', '—', '—', '—', '96/37.80', '41/16.14', '67/26.38', '98/38.58', '115.5/45.47'],
      ['L', '—', '—', '—', '—', '—', '—', '100/39.37', '43/16.93', '69/27.17', '102/40.16', '117/46.06'],
      ['XL', '—', '—', '—', '—', '—', '—', '104/40.94', '44/17.32', '71/27.95', '106/41.73', '118.5/46.65'],
      ['XXL', '—', '—', '—', '—', '—', '—', '108/42.52', '46/18.11', '73/28.74', '110/43.31', '120/47.24'],
      ['3XL', '—', '—', '—', '—', '—', '—', '112/44.09', '47/18.50', '76/29.92', '—', '—'],
    ],
  },
];

function getLocaleRoot() {
  var locale = document.documentElement.getAttribute('lang') || document.documentElement.lang || '';
  var root = normalizeText(locale).split(/[-_]/)[0] || 'en';
  if (root === 'zh') return 'zh';
  return root;
}

function getLocaleMap(source, fallbackLocale) {
  var locale = getLocaleRoot();
  return source[locale] || source[fallbackLocale || 'en'] || {};
}

function interpolateLabel(template, values) {
  return String(template || '').replace(/\{([a-zA-Z0-9_]+)\}/g, function (_match, key) {
    return Object.prototype.hasOwnProperty.call(values || {}, key) ? String(values[key]) : '';
  });
}

function uiLabel(key, fallback, values) {
  var labels = getLocaleMap(UI_LABELS_BY_LOCALE, 'en');
  var english = UI_LABELS_BY_LOCALE.en || {};
  return interpolateLabel(labels[key] || english[key] || fallback || '', values || {});
}

function containsDictionaryToken(value, tokens) {
  var normalizedValue = normalizeText(value);
  if (!normalizedValue) return false;

  return tokens.some(function (token) {
    return normalizedValue.indexOf(normalizeText(token)) !== -1;
  });
}

function isSizeLikeLabel(value) {
  return containsDictionaryToken(value, SIZE_LABEL_TOKENS);
}

function isTypeLikeLabel(value) {
  return containsDictionaryToken(value, TYPE_LABEL_TOKENS);
}

// Detect "Type perfectly partitions roles" — i.e. each Type value
// (Dress / Shirt / etc.) corresponds to a disjoint set of family roles
// with NO role appearing in two Types. When this holds, the Type
// picker is redundant — each role's natural Type is implied. The
// matching bundle uses this to:
//   (a) hide the global Type picker
//   (b) skip the Type filter in buildRoleGroups (so all four role
//       groups stay available even though only one Type is "selected")
//   (c) show the Type as a small subtitle below the role name
// Returns { implicit: true, roleToType: { mother:'Dress', boy:'Shirt'... } }
// when the pattern matches, otherwise { implicit: false }.
function detectImplicitTypeMapping(productData) {
  var result = { implicit: false, roleToType: {} };
  if (!productData || !productData.options || !productData.variants) return result;

  var sizeOptionIndex = findSizeOptionIndex(productData.options);
  if (sizeOptionIndex === -1) return result;

  var typeOptionIndex = -1;
  for (var oi = 0; oi < productData.options.length; oi += 1) {
    if (oi === sizeOptionIndex) continue;
    if (isTypeLikeLabel(normalizeText(productData.options[oi].name))) {
      typeOptionIndex = oi;
      break;
    }
  }
  if (typeOptionIndex === -1) return result; // no Type axis → nothing to do

  // For each variant, collect roleKey ↔ typeValue. If any role has more
  // than one Type, the pattern fails.
  var roleToTypes = Object.create(null);
  var typeToRoles = Object.create(null);

  for (var vi = 0; vi < productData.variants.length; vi += 1) {
    var variant = productData.variants[vi];
    if (!variant) continue;
    var roleInfo = getRoleInfoForVariant(variant, productData.options, sizeOptionIndex);
    if (!roleInfo) continue;
    var roleKey = roleInfo.key;
    var typeValue = getOptionValue(variant, typeOptionIndex);
    if (!typeValue) continue;

    if (!roleToTypes[roleKey]) roleToTypes[roleKey] = Object.create(null);
    roleToTypes[roleKey][typeValue] = true;

    if (!typeToRoles[typeValue]) typeToRoles[typeValue] = Object.create(null);
    typeToRoles[typeValue][roleKey] = true;
  }

  // Two implicit-Type patterns we can detect:
  //
  // (A) STRICT disjoint mapping — each role maps to exactly ONE Type
  //     (e.g. Picnic Plaid after role inference: mother→Dress,
  //     father→Shirt, girl→Dress, boy→Shirt). The global Type picker
  //     is redundant because the role already implies the garment.
  //
  // (B) PER-TYPE SPLIT — at least one role has variants of multiple
  //     Types AND those variants use NON-OVERLAPPING size sets per
  //     Type. Example: Blue Check has role=father appearing in both
  //     Shirt (sizes Adult S/M/L/XL/2XL/3XL) and Shorts (same sizes),
  //     and role=father in Skirt would never appear. The intent is
  //     "father shirt" and "father shorts" are two separate buying
  //     decisions that belong on two cards, not a within-card Type
  //     toggle. We split per (role, Type) and skip the Type filter,
  //     letting getRoleGroupKey() emit "father:shirt" and "father:
  //     shorts" as distinct group keys.
  //
  //     The safety check: if there exists a (role, sizeLabel) pair
  //     that maps to multiple Types, that means the SAME shopper at
  //     the SAME size could legitimately choose between Types — i.e.
  //     Type is a real within-card axis, not a card discriminator.
  //     In that case Pattern B does NOT apply and we keep the global
  //     Type picker (existing behavior).
  //
  // Both patterns produce the same downstream behavior when they fire:
  // hide the global Type picker and let buildRoleGroups emit every
  // (role, type) group as its own card.
  var roleKeys = Object.keys(roleToTypes);
  if (!roleKeys.length) return result;

  var typeKeys = Object.keys(typeToRoles);
  if (typeKeys.length < 2) return result; // only one Type → nothing to partition

  var allRolesStrict = true;
  for (var rk = 0; rk < roleKeys.length; rk += 1) {
    var types = Object.keys(roleToTypes[roleKeys[rk]]);
    if (types.length !== 1) {
      allRolesStrict = false;
      break;
    }
    result.roleToType[roleKeys[rk]] = types[0];
  }

  if (allRolesStrict) {
    // Pattern A — original behavior preserved.
    result.implicit = true;
    result.typeOptionIndex = typeOptionIndex;
    result.typeOptionName = productData.options[typeOptionIndex].name;
    return result;
  }

  // Pattern B fires whenever Pattern A failed but there are 2+ Types.
  // Empirically (May 12 2026 product-catalog review): every family-set
  // product with 2+ Types wants the per-(role, Type) split — "father
  // shirt" and "father shorts" should be addable to the bundle as
  // separate line items, not collapsed into a single father card with
  // an internal Type toggle. Earlier revisions tried to guard against a
  // hypothetical product where a single shopper at one size could pick
  // between Types, but that pattern doesn't exist in this catalog and
  // splitting it into one-card-per-Type would still be a sensible
  // default if it did. Clear roleToType — Pattern B doesn't have a
  // one-to-one role→Type mapping. Downstream code only reads `implicit`
  // and the option metadata, not roleToType, for the filter-skip
  // behavior.
  result.roleToType = {};
  result.implicit = true;
  result.typeOptionIndex = typeOptionIndex;
  result.typeOptionName = productData.options[typeOptionIndex].name;
  return result;
}

function isHeightLikeLabel(value) {
  return containsDictionaryToken(value, HEIGHT_LABEL_TOKENS);
}

function isMeasurementLikeLabel(value) {
  return containsDictionaryToken(value, GUIDE_MEASUREMENT_TOKENS);
}

function hasGuideUnitToken(value) {
  var text = String(value || '');
  return containsDictionaryToken(text, GUIDE_UNIT_TOKENS) || /\([^)]*\/[^)]*\)/.test(text);
}

function getCompactToken(value) {
  var normalizedValue = normalizeText(value);
  try {
    return normalizedValue.replace(/[^\p{L}\p{N}]+/gu, '');
  } catch (_error) {
    return normalizedValue.replace(/[^a-z0-9]+/g, '');
  }
}

function escapeRegExp(value) {
  return String(value || '').replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function normalizeLocalizedSizeValue(value) {
  return replaceLocaleDigits(value)
    .replace(/[\u200e\u200f\u202a-\u202e]/g, ' ')
    .replace(/(^|\s)من\s+/g, '$1')
    .replace(/(\d+(?:\.\d+)?)\s*(?:إلى|الى)\s*(\d+(?:\.\d+)?)/g, '$1-$2')
    .replace(/(^|\s)(?:سنتين|سنتان|عامين|عامان)(?=\s|$)/g, '$12 سنة')
    .replace(/(^|\s)(?:شهرين|شهران)(?=\s|$)/g, '$12 شهر')
    .replace(/(^|\s)لام(?=\s|$)/g, '$1ل')
    .replace(/(^|\s)ميم(?=\s|$)/g, '$1م')
    .replace(/(^|\s)(?:اس|إس)(?=\s|$)/g, '$1س')
    .replace(/\s+/g, ' ')
    .trim();
}

function getLocalizedRoleLabel(roleDefinition) {
  if (!roleDefinition) return '';
  return getLocalizedRoleLabelByKey(roleDefinition.key) || roleDefinition.label || '';
}

function getLocalizedRoleLabelByKey(roleKey) {
  var labels = getLocaleMap(ROLE_LABELS_BY_LOCALE, 'en');
  return labels[roleKey] || (ROLE_LABELS_BY_LOCALE.en && ROLE_LABELS_BY_LOCALE.en[roleKey]) || roleKey || '';
}

function sanitizeRoleSizeLabel(value) {
  return normalizeLocalizedSizeValue(value)
    .replace(/^(?:de|del|da|do|du|des|d'|من)\s+/i, '')
    .replace(/\s+/g, ' ')
    .trim();
}

function getTypeOptionValue(variant, options, sizeOptionIndex) {
  for (var optionIndex = 0; optionIndex < options.length; optionIndex += 1) {
    if (optionIndex === sizeOptionIndex) continue;

    var optionName = normalizeText(options[optionIndex].name);
    if (!isTypeLikeLabel(optionName)) continue;

    return String(getOptionValue(variant, optionIndex) || '').trim();
  }

  return '';
}

function getGarmentKey(value) {
  var text = normalizeText(value);
  if (!text) return '';

  if (
    text.indexOf('shirt & shorts') !== -1 ||
    text.indexOf('shirt and shorts') !== -1 ||
    text.indexOf('camisa y short') !== -1 ||
    text.indexOf('chemise et short') !== -1 ||
    text.indexOf('قميص وشورت') !== -1
  ) {
    return 'shirtShortsSet';
  }

  if (/(dress|skirt|robe|vestido|vestito|kleid|jurk|kjole|sukienka|rochie|плать|فستان|שמלה|ड्रेस|ワンピース|드레스|连衣裙|連衣裙|洋裝)/i.test(text)) {
    return 'dress';
  }
  if (/(shirt|tee|t-shirt|camisa|chemise|hemd|skjorte|koszula|cămașă|camicie|рубаш|قميص|חולצה|शर्ट|シャツ|셔츠|衬衫|襯衫)/i.test(text)) {
    return 'shirt';
  }
  if (/(short|shorts|trunk|bermuda|шорт|شورت|מכנסיים קצרים|ショーツ|반바지|短裤|短褲)/i.test(text)) {
    return 'shorts';
  }
  if (/(romper|pelele|barboteuse|strampler|pagliaccetto|rampers|אוברול|ロンパース|롬퍼|连体衣|連身衣)/i.test(text)) {
    return 'romper';
  }
  if (/(pant|pants|trouser|pantal|hose|broek|bukse|spodnie|брюк|بنطال|מכנסיים|पैंट|パンツ|바지|长裤|長褲)/i.test(text)) {
    return 'pants';
  }
  if (/(top|haut|topp|yläosa|上衣|トップス|상의|טופ|टॉप|توب)/i.test(text)) {
    return 'top';
  }

  return '';
}

function localizeTypeLabel(value) {
  var garmentKey = getGarmentKey(value);
  if (!garmentKey) return String(value || '').trim();

  var labels = getLocaleMap(GARMENT_LABELS_BY_LOCALE, 'en');
  return labels[garmentKey] || (GARMENT_LABELS_BY_LOCALE.en && GARMENT_LABELS_BY_LOCALE.en[garmentKey]) || String(value || '').trim();
}

function inferRoleKeyFromSku(sku) {
  var text = normalizeText(sku).replace(/[^a-z0-9]+/g, '-');
  if (!text) return '';

  if (/(^|-)(grl|girl|daughter)(-|$)/.test(text)) return 'girl';
  if (/(^|-)(boy|son)(-|$)/.test(text)) return 'boy';
  if (/(^|-)(mom|mum|mother)(-|$)/.test(text)) return 'mother';
  if (/(^|-)(dad|father)(-|$)/.test(text)) return 'father';
  if (/(^|-)(baby|bby)(-|$)/.test(text)) return 'baby';
  if (/(^|-)(adult)(-|$)/.test(text)) return 'adult';

  return '';
}

function inferRoleKeyFromType(typeValue, baseRoleKey) {
  var garmentKey = getGarmentKey(typeValue);
  if (!garmentKey) return '';

  if (garmentKey === 'dress') {
    return baseRoleKey === 'adult' ? 'mother' : 'girl';
  }

  if (['shirt', 'shorts', 'shirtShortsSet'].indexOf(garmentKey) !== -1) {
    return baseRoleKey === 'adult' ? 'father' : 'boy';
  }

  return '';
}

function cloneRoleInfoWithKey(roleInfo, roleKey) {
  if (!roleInfo || !roleKey || roleInfo.key === roleKey) return roleInfo;

  return {
    key: roleKey,
    label: getLocalizedRoleLabelByKey(roleKey),
    sizeLabel: roleInfo.sizeLabel,
    fullLabel: roleInfo.fullLabel,
  };
}

function getRoleInfoForVariant(variant, options, sizeOptionIndex) {
  var roleInfo = parseRoleFromSizeLabel(getOptionValue(variant, sizeOptionIndex));
  if (!roleInfo) return null;

  var skuRoleKey = inferRoleKeyFromSku(variant && variant.sku);
  if (skuRoleKey) {
    roleInfo = cloneRoleInfoWithKey(roleInfo, skuRoleKey);
  }

  var typeValue = getTypeOptionValue(variant, options, sizeOptionIndex);
  var typeRoleKey = inferRoleKeyFromType(typeValue, roleInfo.key);
  if (
    typeRoleKey &&
    (!skuRoleKey || roleInfo.key === 'child' || roleInfo.key === 'adult' || roleInfo.key === 'boy' || roleInfo.key === 'girl')
  ) {
    if (
      roleInfo.key === 'child' ||
      roleInfo.key === 'adult' ||
      (roleInfo.key === 'boy' && typeRoleKey === 'girl') ||
      (roleInfo.key === 'girl' && typeRoleKey === 'boy')
    ) {
      roleInfo = cloneRoleInfoWithKey(roleInfo, typeRoleKey);
    }
  }

  return roleInfo;
}

function getRoleGroupKey(roleInfo, typeValue, opts) {
  if (!roleInfo) return '';

  var groupKey = roleInfo.key;
  // When Type is being rendered as a per-card axis (skipTypeFilter /
  // Pattern A or B), DO NOT also split the group key by Type — Type
  // lives inside the card as a pill row alongside Color, not as a
  // separate card per Type. The legacy whitelist
  // ['girl','boy','child','adult'] was for the older single-card-per-
  // (role, Type) model. With the axis-row model we want one card per
  // role regardless of how many Types that role spans.
  var noSplitByType = !!(opts && opts.noSplitByType);
  if (noSplitByType) return groupKey;

  var garmentKey = getGarmentKey(typeValue);
  if (garmentKey && ['girl', 'boy', 'child', 'adult'].indexOf(roleInfo.key) !== -1) {
    groupKey += ':' + garmentKey;
  }

  return groupKey;
}

function normalizeAgeSpan(value) {
  return String(value || '').replace(/\s*[–-]\s*/g, '-').trim();
}

function getLeadingAgeNumber(value) {
  var match = String(value || '').match(/^\d+/);
  return match ? Number(match[0]) : 0;
}

function isPluralAgeSpan(value) {
  var normalized = normalizeAgeSpan(value);
  if (normalized.indexOf('-') !== -1) return true;
  return Number(normalized) !== 1;
}

function getLocalizedAgeUnitLabel(value, unit, units) {
  var root = getLocaleRoot();
  var normalizedValue = normalizeAgeSpan(value);
  var isRange = normalizedValue.indexOf('-') !== -1;
  var number = getLeadingAgeNumber(normalizedValue);

  if (unit === 'year') {
    if (root === 'ar' && normalizedValue === '2') return 'سنتين';
    if (root === 'cs' && !isRange) return number === 1 ? 'rok' : number >= 2 && number <= 4 ? 'roky' : 'let';
    if (root === 'pl' && !isRange) {
      var plLast = number % 10;
      var plLastTwo = number % 100;
      return number === 1 ? 'rok' : plLast >= 2 && plLast <= 4 && (plLastTwo < 12 || plLastTwo > 14) ? 'lata' : 'lat';
    }
    if (root === 'ru' && !isRange) {
      var ruLast = number % 10;
      var ruLastTwo = number % 100;
      return ruLast === 1 && ruLastTwo !== 11 ? 'год' : ruLast >= 2 && ruLast <= 4 && (ruLastTwo < 12 || ruLastTwo > 14) ? 'года' : 'лет';
    }
  }

  var plural = isPluralAgeSpan(normalizedValue);
  var unitKey = unit === 'month' ? (plural ? 'months' : 'month') : plural ? 'years' : 'year';
  return units[unitKey] || SIZE_UNIT_LABELS_BY_LOCALE.en[unitKey];
}

function formatLocalizedAge(value, unit) {
  var units = getLocaleMap(SIZE_UNIT_LABELS_BY_LOCALE, 'en');
  var normalizedValue = normalizeAgeSpan(value);
  var unitLabel = getLocalizedAgeUnitLabel(normalizedValue, unit, units);
  if (getLocaleRoot() === 'ar' && unit === 'year' && normalizedValue === '2') return unitLabel;
  return normalizedValue + (units.joiner || ' ') + unitLabel;
}

function localizeSizeLabel(sizeLabel, roleKey) {
  var text = sanitizeRoleSizeLabel(sizeLabel);
  if (!text) return '';

  var yearMatch = text.match(/^(\d+(?:\s*[–-]\s*\d+)?)\s*(?:years?|yrs?|yr|y|años?|anos?|ans?|jahre|jahr|anni|anno|jaar|år|lata|lat|ani|an|года|год|лет|سنة|سنوات|שנים|שנה|वर्ष|년|세|歳|才|岁|歲)?$/i);
  if (yearMatch && (roleKey === 'child' || roleKey === 'girl' || roleKey === 'boy' || roleKey === 'baby')) {
    return formatLocalizedAge(yearMatch[1], roleKey === 'baby' && /month|mes|mois|monat|mese|maand|mån|mies|חודש|شهر|ヶ月|개월/i.test(text) ? 'month' : 'year');
  }

  var monthMatch = text.match(/^(\d+(?:\s*[–-]\s*\d+)?)\s*(?:months?|mos?|mo|meses?|mois|monate|mesi|maanden|måneder|mnd|mies|شهر|أشهر|חודשים|חודש|महीने|か月|ヶ月|개월)$/i);
  if (monthMatch) {
    return formatLocalizedAge(monthMatch[1], 'month');
  }

  return text;
}

function findSizeOptionIndex(options) {
  if (!Array.isArray(options)) return -1;

  for (var index = 0; index < options.length; index += 1) {
    if (isSizeLikeLabel(options[index].name)) {
      return index;
    }
  }

  return -1;
}

function parseRoleFromSizeLabel(label) {
  var text = String(label || '').trim();
  if (!text) return null;

  for (var index = 0; index < ROLE_DEFINITIONS.length; index += 1) {
    var roleDefinition = ROLE_DEFINITIONS[index];
    var aliasCandidates = getRoleAliasCandidates(roleDefinition);

    for (var aliasIndex = 0; aliasIndex < aliasCandidates.length; aliasIndex += 1) {
      var alias = aliasCandidates[aliasIndex];
      var escapedAlias = escapeRegExp(alias).replace(/\s+/g, '\\s+');
      var startPattern = new RegExp('^' + escapedAlias + '(?:\\s+|\\s*[-–/]\\s*)(.+)$', 'i');
      var endPattern = new RegExp('^(.+?)(?:\\s+|\\s*[-–/]\\s*)' + escapedAlias + '$', 'i');
      var startMatch = text.match(startPattern);
      var endMatch = text.match(endPattern);
      var sizeLabel = startMatch && startMatch[1] ? startMatch[1].trim() : '';

      if (!sizeLabel && endMatch && endMatch[1]) {
        sizeLabel = endMatch[1].trim();
      }

      if (!sizeLabel) continue;
      sizeLabel = sanitizeRoleSizeLabel(sizeLabel);

      return {
        key: roleDefinition.key,
        label: getLocalizedRoleLabel(roleDefinition),
        sizeLabel: sizeLabel,
        fullLabel: text,
      };
    }
  }

  return null;
}

function getRoleAliasCandidates(roleDefinition) {
  var aliases = (roleDefinition && roleDefinition.aliases ? roleDefinition.aliases : []).slice();
  var seen = {};

  Object.keys(ROLE_LABELS_BY_LOCALE).forEach(function (locale) {
    var localizedLabel = ROLE_LABELS_BY_LOCALE[locale] && ROLE_LABELS_BY_LOCALE[locale][roleDefinition.key];
    if (localizedLabel) aliases.push(localizedLabel);
  });

  return aliases
    .map(function (alias) {
      return String(alias || '').trim();
    })
    .filter(function (alias) {
      var key = String(alias || '').toLowerCase().trim();
      if (!key || seen[key]) return false;
      seen[key] = true;
      return true;
    })
    .sort(function (first, second) {
      return second.length - first.length;
    });
}

function getRoleOrder(roleKey) {
  var order = {
    mother: 1,
    father: 2,
    girl: 3,
    boy: 4,
    child: 5,
    baby: 6,
    adult: 7,
  };

  return Object.prototype.hasOwnProperty.call(order, roleKey) ? order[roleKey] : 99;
}

function getRoleFitCopy(roleKey) {
  var locale = getLocaleRoot();
  var copy = ROLE_FIT_COPY_BY_LOCALE[locale];

  if (!copy && locale === 'en') {
    copy = ROLE_FIT_COPY_BY_LOCALE.en;
  }

  return copy && Object.prototype.hasOwnProperty.call(copy, roleKey) ? copy[roleKey] : '';
}

function getCurrentOptionContext(variantSelects) {
  var context = {};
  if (!variantSelects) return context;

  var controls = variantSelects.querySelectorAll('select[name], input[type="radio"][name]:checked');
  controls.forEach(function (control) {
    var optionName = getOptionNameFromControl(control);
    if (!optionName) return;
    context[normalizeText(optionName)] = String(control.value || '').trim();
  });

  return context;
}

function getOptionNameFromControl(control) {
  if (!control) return '';

  var name = String(control.getAttribute('name') || '').trim();
  var match = name.match(/^options\[(.+)\]$/);
  return match && match[1] ? match[1] : name;
}

function buildRoleGroups(productData, currentOptionContext, includeAllAxes, opts) {
  var sizeOptionIndex = findSizeOptionIndex(productData.options);
  if (sizeOptionIndex === -1) return [];

  // When the caller passes `opts.skipTypeFilter = true`, we treat Type
  // as implicit (a role-discriminator) instead of a global filter —
  // see detectImplicitTypeMapping(). Variants of every Type are emitted
  // into their natural role groups (mother→Dress, father→Shirt, etc.).
  var skipTypeFilter = !!(opts && opts.skipTypeFilter);

  var roleGroups = {};

  productData.variants.forEach(function (variant) {
    if (!variant) return;
    // When includeAllAxes is true the caller wants every variant (the
    // bundle does per-card axis filtering itself). Otherwise we skip
    // unavailable variants to preserve legacy behavior.
    if (!includeAllAxes && !variant.available) return;

    for (var optionIndex = 0; optionIndex < productData.options.length; optionIndex += 1) {
      if (optionIndex === sizeOptionIndex) continue;

      var optionName = normalizeText(productData.options[optionIndex].name);

      // Type filter: normally applied when picker has a value, BUT
      // skipped entirely when Type is implicit (per-role). In implicit
      // mode each role group naturally collects variants of its own
      // Type, so Mother sees only Dress variants etc.
      if (isTypeLikeLabel(optionName)) {
        if (skipTypeFilter) continue;
        if (!currentOptionContext[optionName]) continue;
        if (normalizeText(getOptionValue(variant, optionIndex)) !== normalizeText(currentOptionContext[optionName])) {
          return;
        }
        continue;
      }

      if (includeAllAxes) continue; // per-card filters handle Color/etc
      if (!currentOptionContext[optionName]) continue;
      if (normalizeText(getOptionValue(variant, optionIndex)) !== normalizeText(currentOptionContext[optionName])) {
        return;
      }
    }

	    var roleInfo = getRoleInfoForVariant(variant, productData.options, sizeOptionIndex);
	    if (!roleInfo) return;
	    var typeValue = getTypeOptionValue(variant, productData.options, sizeOptionIndex);
	    var groupKey = getRoleGroupKey(roleInfo, typeValue, { noSplitByType: skipTypeFilter });

	    if (!roleGroups[groupKey]) {
	      roleGroups[groupKey] = {
	        key: groupKey,
	        roleKey: roleInfo.key,
	        label: roleInfo.label,
	        helper: localizeTypeLabel(typeValue),
	        helperRaw: typeValue,
	        options: [],
	      };
	    }

	    // Capture every non-size axis value (Color, Pattern, Style, …)
	    // per variant so the bundle's per-card picker can build a
	    // swatch/pill row for each axis with OOS combos disabled.
	    //
	    // Type is normally excluded because the global Type picker
	    // handles it. But when Type is implicit (Pattern A/B in
	    // detectImplicitTypeMapping → skipTypeFilter is true) the
	    // global picker is hidden and Type needs to live INSIDE each
	    // card as a pill row — same pattern as Color on Picnic Plaid.
	    // For Pattern A products (e.g. Picnic Plaid: mother↔Dress,
	    // father↔Shirt) Type ends up as a 1-value axis per card and is
	    // auto-suppressed by the renderer's `values.length <= 1` gate.
	    // For Pattern B products (e.g. Blue Check: father has both
	    // Shirt + Shorts) the Type pill row genuinely renders and lets
	    // the shopper pick the garment for THAT family member without
	    // affecting other cards. That's the behavior Frank wants per
	    // May 12 2026 PDP review.
	    var nonSizeAxes = {};
	    for (var ai = 0; ai < productData.options.length; ai += 1) {
	      if (ai === sizeOptionIndex) continue;
	      var axisName = productData.options[ai].name;
	      if (!axisName) continue;
	      if (!skipTypeFilter && isTypeLikeLabel(normalizeText(axisName))) continue;
	      var axisVal = getOptionValue(variant, ai);
	      if (axisVal) nonSizeAxes[axisName] = axisVal;
	    }

	    roleGroups[groupKey].options.push({
	      id: String(variant.id),
	      sizeLabel: localizeSizeLabel(roleInfo.sizeLabel, roleInfo.key),
	      fullLabel: roleInfo.fullLabel,
	      price: Number(variant.price) || 0,
	      available: variant.available !== false,
	      axes: nonSizeAxes,
	    });
  });

  return Object.keys(roleGroups)
    .map(function (key) {
      return roleGroups[key];
    })
	    .sort(function (first, second) {
	      var roleSort = getRoleOrder(first.roleKey || first.key) - getRoleOrder(second.roleKey || second.key);
	      if (roleSort !== 0) return roleSort;
	      return String(first.helperRaw || '').localeCompare(String(second.helperRaw || ''));
	    });
}

function getRoleHelperLabel(variant, options, sizeOptionIndex) {
  return localizeTypeLabel(getTypeOptionValue(variant, options, sizeOptionIndex));
}

function getMatchingSetSelections(builder) {
  // Returns { groupKey: variantId } map for whichever instance cards
  // currently have a selected pill. Used to preserve user choices when
  // the main <variant-selects> fires "change". With the instance model
  // (May 11 2026 rev), per-card state is held in the closure's
  // `instances` array — this function exists for back-compat with the
  // outer change handler but most preservation is already automatic.
  var selections = {};
  builder.querySelectorAll('[data-instance-card]').forEach(function (card) {
    var groupKey = card.getAttribute('data-role-card');
    var selectedPill = card.querySelector('[data-instance-pill].is-selected');
    if (!groupKey || !selectedPill) return;
    // Last write wins — if two cards of the same group both have
    // selections, the second one overrides. That's fine for the outer
    // change handler because the instance model itself isn't reset.
    selections[groupKey] = String(selectedPill.getAttribute('data-variant-id') || '');
  });
  return selections;
}

function getMatchingSetOptionLabel(group, option) {
  var parts = [group && group.label, group && group.helper, option && option.sizeLabel].filter(Boolean);
  return parts.join(' ');
}

function initMatchingSetBuilder(wrapper, sectionId, productData) {
  var builder = wrapper.querySelector('[data-matching-set-builder]');
  if (!builder) return;

  // ─────────────────────────────────────────────────────────────────────
  // CRITICAL: normalize productData.options ordering by .position.
  // The Liquid template iterates product.options_with_values which is
  // not guaranteed to be position-sorted. Our buildRoleGroups +
  // getOptionValue use ARRAY INDEX (assumes index+1 = variant.option{N}),
  // so an unordered array causes wrong field lookups (size column
  // returning a color value, etc.). Sort once on init.
  // ─────────────────────────────────────────────────────────────────────
  if (productData && Array.isArray(productData.options)) {
    var sortedOptions = productData.options.slice().sort(function (a, b) {
      var pa = Number(a && a.position) || 0;
      var pb = Number(b && b.position) || 0;
      return pa - pb;
    });
    // Only swap if order actually differs to avoid breaking referential
    // equality where it isn't needed.
    var needsSort = sortedOptions.some(function (opt, idx) {
      return opt !== productData.options[idx];
    });
    if (needsSort) {
      productData = Object.assign({}, productData, { options: sortedOptions });
    }
  }

  // CRO redesign May 2026: on bundle products the legacy "Compare
  // family sizes" details element (rendered by product-variant-picker.liquid)
  // sits at the same DOM level as the variant picker we hide via CSS,
  // but without the `hidden` attribute it stays visible and adds an
  // empty disclosure above the bundle. Mark it hidden so it doesn't
  // paint by default; the existing [data-pdp-size-guide-trigger] handler
  // will remove the attribute when the shopper taps "Find {role}'s fit"
  // on a card.
  var infoContainer = wrapper.closest('.product__info-container--matching-set');
  if (infoContainer) {
    var legacyGuide = document.querySelector('[data-matching-size-guide]');
    if (legacyGuide && !legacyGuide.hasAttribute('hidden')) {
      legacyGuide.setAttribute('hidden', 'hidden');
    }
  }

  var roleGrid = builder.querySelector('[data-matching-set-roles]');
  var chips = builder.querySelector('[data-matching-set-chips]');
  var total = builder.querySelector('[data-matching-set-total]');
  var emptyCopy = builder.querySelector('[data-matching-set-empty-copy]');
  var status = builder.querySelector('[data-matching-set-status]');
  var addButton = builder.querySelector('[data-matching-set-add-button]');
  var variantSelects = document.getElementById('variant-selects-' + sectionId);
  var productForm = document.getElementById('product-form-' + sectionId);
  var selectedVariantInput = productForm ? productForm.querySelector('[name="id"]') : null;
  var currency = productData.currency || 'USD';

  // ─────────────────────────────────────────────────────────────────────
  // CRO redesign May 2026 — INSTANCE MODEL (rev 2, May 11).
  //
  // The first rev keyed selections by role (one Mother card, one Child
  // card, period). That broke real family use cases — moms with two
  // daughters in different sizes, or a mom who wants two matching
  // outfits for herself + a friend, couldn't add them.
  //
  // Current model: `instances` is an ORDERED ARRAY of cards. Each card
  // is one independent line item. The same role can appear N times
  // with different sizes/qty. Default state shows one empty Mother
  // card + one empty Child card; + Add buttons always create a NEW
  // instance (never reuses an existing one); × removes that specific
  // instance.
  //
  //   instances = [
  //     { instanceId, roleKey, groupKey, variantId, quantity },
  //     ...
  //   ]
  //
  // ─────────────────────────────────────────────────────────────────────
  var instances = [];
  var instanceCounter = 0;
  var hasSeededDefaults = false;
  var roleGroupsCache = [];
  // Tracks the last Type axis value seen (e.g. "shirt" / "dress").
  // When the global Type picker changes, the bundle resets its
  // default-visible cards. null sentinel = first render — don't reset.
  var lastTypeContext = null;

  // Implicit-Type detection: when each Type value maps to a disjoint
  // set of roles (e.g. Dress↔mother/girl, Shirt↔father/boy), the
  // global Type picker becomes redundant and we treat Type as an
  // implied per-role attribute. See detectImplicitTypeMapping().
  var typeMapping = detectImplicitTypeMapping(productData);
  var typeIsImplicit = !!(typeMapping && typeMapping.implicit);
  // When Type is implicit we also instruct the surrounding CSS to hide
  // the global Type picker. The body class is read by the bundle's
  // CSS selectors.
  if (typeIsImplicit) {
    try {
      var bundleRoot = wrapper.closest('.product__info-container--matching-set');
      if (bundleRoot) bundleRoot.setAttribute('data-type-implicit', 'true');
    } catch (_e) { /* defensive */ }
  }

  // Per-bundle persistent size panel state.
  //   unitSystem      'metric' | 'imperial' — shared with the legacy
  //                   size-guide unit toggle via localStorage so the
  //                   shopper's preference rides across reloads and
  //                   between the panel + the full size chart.
  //   closedPanels    instanceIds the shopper has X-dismissed; cleared
  //                   when they pick a different size on that card so
  //                   the panel re-opens with fresh info.
  var BUNDLE_UNIT_STORAGE_KEY = 'dlm_size_chart_unit_system';
  var unitSystem = (function () {
    try {
      var stored = window.localStorage && window.localStorage.getItem(BUNDLE_UNIT_STORAGE_KEY);
      if (stored === 'imperial' || stored === 'metric') return stored;
    } catch (e) { /* localStorage may be blocked; default to metric */ }
    return 'metric';
  })();
  var closedPanels = Object.create(null);

  function setUnitSystem(next) {
    if (next !== 'metric' && next !== 'imperial') return;
    if (next === unitSystem) return;
    unitSystem = next;
    try {
      if (window.localStorage) window.localStorage.setItem(BUNDLE_UNIT_STORAGE_KEY, next);
    } catch (e) { /* ignore */ }
    renderBuilder();
  }

  function closeOpenSizePanels() {
    var changed = false;
    for (var i = 0; i < instances.length; i += 1) {
      var inst = instances[i];
      if (!inst || !inst.sizeLabel || closedPanels[inst.instanceId]) continue;
      closedPanels[inst.instanceId] = true;
      changed = true;
    }
    return changed;
  }

  function isMobileSizePanelViewport() {
    if (typeof window === 'undefined') return false;
    return !window.matchMedia || window.matchMedia('(max-width: 749px)').matches;
  }

  // ─────────────────────────────────────────────────────────────────────
  // Size-measurements lookup, populated lazily on first card render.
  // Source: the same <table id="size-chart"> that powers the legacy
  // "Compare family sizes" details element. Parsing is shared with
  // parseSizeGuideTable() so the tooltip can't drift from the size
  // chart Frank already maintains per product.
  //
  // Shape: sizeMeasurementsByLabel = {
  //   "mother s": { headers: [...], row: [...] },
  //   "boy 4t":   { headers: [...], row: [...] },
  //   ...
  // }
  // Keyed by lowercased+trimmed size label. Empty cells / age/weight
  // columns that don't apply to a given role are filtered out by the
  // tooltip renderer.
  // ─────────────────────────────────────────────────────────────────────
  var sizeMeasurementsByLabel = null;

  function normalizeSizeKey(text) {
    return String(text || '').toLowerCase().replace(/\s+/g, ' ').trim();
  }

  function buildSizeMeasurementsLookup() {
    if (sizeMeasurementsByLabel) return sizeMeasurementsByLabel;
    sizeMeasurementsByLabel = Object.create(null);

    var table = document.querySelector('table#size-chart, table[id*="size-chart"]');
    if (!table || typeof parseSizeGuideTable !== 'function') return sizeMeasurementsByLabel;

    var parsed = parseSizeGuideTable(table);
    if (!parsed || !parsed.rows || !parsed.headers) return sizeMeasurementsByLabel;

    parsed.rows.forEach(function (row) {
      var rawLabel = String((row[0] || '')).trim();
      if (!rawLabel) return;
      var key = normalizeSizeKey(rawLabel);
      sizeMeasurementsByLabel[key] = { headers: parsed.headers, row: row };
    });
    return sizeMeasurementsByLabel;
  }

  function findMeasurementsForOption(group, option) {
    if (!option) return null;
    buildSizeMeasurementsLookup();
    if (!sizeMeasurementsByLabel) return null;

    // Try multiple lookup keys in order of specificity. Each PDP's
    // variant naming convention varies — try the raw size label
    // ("Mother S"), the role-prefixed full label ("Mother S"), and
    // size-only ("S") as fallbacks.
    var candidates = [];
    if (option.fullLabel) candidates.push(option.fullLabel);
    if (group && group.label && option.sizeLabel) {
      candidates.push(group.label + ' ' + option.sizeLabel);
    }
    if (option.sizeLabel) candidates.push(option.sizeLabel);

    for (var i = 0; i < candidates.length; i += 1) {
      var key = normalizeSizeKey(candidates[i]);
      if (sizeMeasurementsByLabel[key]) return sizeMeasurementsByLabel[key];
    }
    return null;
  }

  function isMeaningfulMeasurementValue(value) {
    if (value === null || value === undefined) return false;
    var text = String(value).trim();
    if (!text) return false;
    if (text === '-' || text === '—' || text === '--') return false;
    // The size-chart cells empty for a role show as "" — already filtered.
    return /[0-9]/.test(text);
  }

  // Pick the unit-system-appropriate value from a dual-unit cell like
  // "92.71-95.25 / 36.5-37.5" (cm / in) and return { value, unit }.
  // Falls back gracefully if the cell only has one unit (we return it
  // as-is with the header's first unit).
  function extractValueForUnit(rawValue, header, activeUnit) {
    var text = String(rawValue || '').trim();
    if (!text) return null;
    var parts = (typeof splitGuideMeasurementParts === 'function')
      ? splitGuideMeasurementParts(text)
      : text.split(/\s+\/\s+/).map(function (p) { return p.trim(); }).filter(Boolean);
    var units = (header && header.units) ? header.units : [];

    // Multi-unit cell: pick the index matching activeUnit.
    if (parts.length >= 2 && units.length >= 2) {
      for (var i = 0; i < units.length; i += 1) {
        if (String(units[i]).toLowerCase() === activeUnit) {
          return { value: parts[Math.min(i, parts.length - 1)], unit: units[i] };
        }
      }
      return { value: parts[0], unit: units[0] };
    }

    // Single-unit cell: convert on the fly if needed.
    var sourceUnit = (units[0] || '').toLowerCase();
    if (!sourceUnit) return { value: text, unit: '' };
    if (sourceUnit === activeUnit) return { value: text, unit: sourceUnit };
    var converted = convertRangeValue(text, sourceUnit, activeUnit);
    if (converted) return { value: converted, unit: activeUnit };
    return { value: text, unit: sourceUnit };
  }

  // Convert a single value or "min-max" range from one unit to another.
  // Supports cm <-> in and kg <-> lbs. Returns null if conversion isn't
  // possible (e.g. unitless age columns).
  function convertRangeValue(text, from, to) {
    if (!text || !from || !to || from === to) return null;
    var factor = null;
    if (from === 'cm' && to === 'in') factor = 1 / 2.54;
    else if (from === 'in' && to === 'cm') factor = 2.54;
    else if (from === 'kg' && to === 'lbs') factor = 2.2046226218;
    else if (from === 'lbs' && to === 'kg') factor = 1 / 2.2046226218;
    if (factor === null) return null;

    var pieces = String(text).split('-').map(function (p) { return p.trim(); });
    var converted = [];
    for (var i = 0; i < pieces.length; i += 1) {
      var n = parseFloat(pieces[i]);
      if (!isFinite(n)) return null;
      converted.push(roundMeasurement(n * factor));
    }
    return converted.join('-');
  }

  // Round any numeric measurement to a single decimal place — and drop
  // the trailing .0 so "92" stays "92", not "92.0". Used both on
  // converted values and on raw chart cells (some products were entered
  // with absurd precision like 44.8819 inches; this trims them down to
  // a single decimal at render time without touching the source data).
  function roundMeasurement(num) {
    if (!isFinite(num)) return String(num);
    return Number(num).toFixed(1).replace(/\.0$/, '');
  }

  // Take a raw chart cell value (which may be a number, a "min-max"
  // range, or already contain a unit suffix) and trim trailing decimals
  // beyond 1 on each numeric piece. Non-numeric text is passed through.
  function tidyMeasurementValue(text) {
    var raw = String(text || '').trim();
    if (!raw) return raw;
    // Replace any number with more than one decimal with a 1-decimal version.
    return raw.replace(/(\d+)\.(\d{2,})/g, function (_, intPart, decimals) {
      var n = parseFloat(intPart + '.' + decimals);
      if (!isFinite(n)) return _;
      return roundMeasurement(n);
    });
  }

  function buildMeasurementsHtml(measurements, options) {
    if (!measurements || !measurements.headers || !measurements.row) return '';
    var opts = options || {};
    var activeUnit = opts.activeUnit || (unitSystem === 'imperial' ? 'in' : 'cm');

    var pairs = [];
    measurements.headers.forEach(function (header, headerIndex) {
      if (headerIndex === 0) return; // index 0 is the size label itself
      var rawValue = measurements.row[headerIndex];
      if (!isMeaningfulMeasurementValue(rawValue)) return;

      var headerLabel = '';
      var headerUnits = [];
      if (header && typeof header === 'object') {
        headerLabel = header.label || header.raw || '';
        headerUnits = (header.units || []).map(function (u) { return String(u).toLowerCase(); });
      } else {
        headerLabel = String(header || '');
      }

      // For length-style headers (cm/in) honor the active unit system.
      // For weight (kg/lbs) honor it the same way. For unitless headers
      // (Age, Size) show as-is regardless of toggle.
      var preferredUnit = activeUnit;
      if (headerUnits.indexOf('kg') !== -1 || headerUnits.indexOf('lbs') !== -1) {
        preferredUnit = unitSystem === 'imperial' ? 'lbs' : 'kg';
      } else if (headerUnits.indexOf('cm') !== -1 || headerUnits.indexOf('in') !== -1) {
        preferredUnit = unitSystem === 'imperial' ? 'in' : 'cm';
      } else {
        preferredUnit = '';
      }

      var extracted = preferredUnit
        ? extractValueForUnit(rawValue, header, preferredUnit)
        : { value: String(rawValue).trim(), unit: '' };
      if (!extracted || !extracted.value) return;

      var displayLabel = headerLabel;
      if (extracted.unit) displayLabel += ' (' + extracted.unit + ')';

      // Trim absurd precision in raw chart cells before display.
      // E.g. some products were entered with "44.8819" — show "44.9".
      pairs.push({ label: displayLabel, value: tidyMeasurementValue(extracted.value) });
    });
    if (!pairs.length) return '';
    return (
      '<dl class="product-matching-set__measurement-list">' +
      pairs
        .map(function (pair) {
          return (
            '<div class="product-matching-set__measurement-row">' +
            '<dt>' +
            escapeHtml(pair.label) +
            '</dt>' +
            '<dd>' +
            escapeHtml(pair.value) +
            '</dd>' +
            '</div>'
          );
        })
        .join('') +
      '</dl>'
    );
  }

  var selectSizeLabel = wrapper.getAttribute('data-select-size-label') || 'Select size';

  function newInstanceId() {
    instanceCounter += 1;
    return 'inst-' + instanceCounter;
  }

  function getCurrentVariant() {
    if (!selectedVariantInput || !selectedVariantInput.value) return null;
    var selectedId = String(selectedVariantInput.value);
    return (
      productData.variants.find(function (variant) {
        return String(variant.id) === selectedId;
      }) || null
    );
  }

  function getGroupByKey(groupKey) {
    for (var i = 0; i < roleGroupsCache.length; i += 1) {
      if (roleGroupsCache[i].key === groupKey) return roleGroupsCache[i];
    }
    return null;
  }

  // Get one representative group per roleKey (so the + Add row lists
  // each family role once, even when the product has multiple groupKeys
  // per role like mother__dress vs mother__shirt).
  function getRoleRepresentatives() {
    var seen = Object.create(null);
    var reps = [];
    roleGroupsCache.forEach(function (group) {
      var roleKey = group.roleKey || group.key;
      if (seen[roleKey]) return;
      seen[roleKey] = true;
      reps.push(group);
    });
    return reps;
  }

  function getOptionByVariantId(group, variantId) {
    if (!group || !variantId) return null;
    for (var i = 0; i < group.options.length; i += 1) {
      if (String(group.options[i].id) === String(variantId)) return group.options[i];
    }
    return null;
  }

  // ─── Axis helpers (May 2026 rev 5: per-card color/pattern picker) ──
  // Distinct size labels for a group, in the order variants were
  // emitted. Used to render the size pill row.
  function getDistinctSizesForGroup(group) {
    if (!group) return [];
    var seen = Object.create(null);
    var result = [];
    group.options.forEach(function (opt) {
      var key = opt.sizeLabel || '';
      if (!key || seen[key]) return;
      seen[key] = true;
      result.push(key);
    });
    return result;
  }

  // Distinct axis NAMES present on this group (e.g. ['Color']).
  function getAxisNamesForGroup(group) {
    if (!group) return [];
    var seen = Object.create(null);
    var names = [];
    group.options.forEach(function (opt) {
      Object.keys(opt.axes || {}).forEach(function (axisName) {
        if (seen[axisName]) return;
        seen[axisName] = true;
        names.push(axisName);
      });
    });
    return names;
  }

  // Distinct values for a given axis on this group, in first-seen order.
  function getAxisValuesForGroup(group, axisName) {
    if (!group || !axisName) return [];
    var seen = Object.create(null);
    var values = [];
    group.options.forEach(function (opt) {
      var v = opt.axes && opt.axes[axisName];
      if (!v || seen[v]) return;
      seen[v] = true;
      values.push(v);
    });
    return values;
  }

  // Resolve { sizeLabel, axisSelections } to a variant in the group.
  // Returns the option object or null when no exact match exists.
  function resolveVariantInGroup(group, sizeLabel, axisSelections) {
    if (!group) return null;
    var sels = axisSelections || {};
    var selKeys = Object.keys(sels);
    for (var i = 0; i < group.options.length; i += 1) {
      var opt = group.options[i];
      if (sizeLabel && opt.sizeLabel !== sizeLabel) continue;
      var matches = true;
      for (var k = 0; k < selKeys.length; k += 1) {
        var axisName = selKeys[k];
        if (!sels[axisName]) continue;
        if ((opt.axes && opt.axes[axisName]) !== sels[axisName]) {
          matches = false;
          break;
        }
      }
      if (matches) return opt;
    }
    return null;
  }

  // Does this group have at least one available variant for the given
  // sizeLabel + axisSelections combo? Used to disable OOS pills.
  function isComboAvailable(group, sizeLabel, axisSelections) {
    var opt = resolveVariantInGroup(group, sizeLabel, axisSelections);
    return !!(opt && opt.available !== false);
  }

  function findInstance(instanceId) {
    for (var i = 0; i < instances.length; i += 1) {
      if (instances[i].instanceId === instanceId) return instances[i];
    }
    return null;
  }

  function removeInstance(instanceId) {
    instances = instances.filter(function (inst) {
      return inst.instanceId !== instanceId;
    });
  }

  function addInstanceForGroup(group) {
    instances.push({
      instanceId: newInstanceId(),
      roleKey: group.roleKey || group.key,
      groupKey: group.key,
      sizeLabel: '',          // size pill picked by shopper
      axisSelections: {},     // { Color: 'Pink', Pattern: 'Plaid', ... }
      variantId: '',          // derived from sizeLabel + axisSelections
      quantity: 1,
    });
  }

  // Recompute inst.variantId whenever the shopper changes a pill on
  // any axis. Sets variantId to '' when the current size + axis combo
  // doesn't resolve to a real variant (OOS or impossible combination).
  //
  // STRICT REQUIREMENT (May 2026): every axis present on this group
  // (e.g. Color) must have a value in inst.axisSelections before we
  // commit a variantId. Without this guard, resolveVariantInGroup
  // happily returns the first option that matches the picked size,
  // which causes two visible bugs on PDPs with un-picked color
  // swatches:
  //   1) The green "Mother · S · $31.99 each" confirmation appears
  //      before the shopper has chosen a color.
  //   2) The "ADD SELECTED PIECES TO CART" button enables, letting
  //      shoppers add a variant they never explicitly picked.
  // Note: resolveVariantInGroup itself stays permissive — it's also
  // used as a "is anything available for this combo?" probe by the
  // size-pill and axis-swatch renderers, which DO want wildcard
  // behavior. Only the commit step here needs to be strict.
  function refreshInstanceVariantId(inst) {
    var group = getGroupByKey(inst.groupKey);
    if (!group) { inst.variantId = ''; return; }
    if (!inst.sizeLabel) { inst.variantId = ''; return; }
    var requiredAxes = getAxisNamesForGroup(group).filter(function (axisName) {
      // Treat single-value axes as auto-satisfied — the renderer hides
      // them ("values.length <= 1 → return ''") so the shopper has no
      // way to pick them.
      return getAxisValuesForGroup(group, axisName).length > 1;
    });
    var sels = inst.axisSelections || {};
    for (var i = 0; i < requiredAxes.length; i += 1) {
      if (!sels[requiredAxes[i]]) { inst.variantId = ''; return; }
    }
    var opt = resolveVariantInGroup(group, inst.sizeLabel, sels);
    inst.variantId = opt && opt.available !== false ? String(opt.id) : '';
  }

  function getSelectedItems() {
    var items = [];
    instances.forEach(function (inst) {
      if (!inst.variantId || !inst.quantity) return;
      var group = getGroupByKey(inst.groupKey);
      var option = getOptionByVariantId(group, inst.variantId);
      if (!group || !option) return;
      items.push({
        instanceId: inst.instanceId,
        roleKey: inst.roleKey,
        roleLabel: group.label,
        sizeLabel: option.sizeLabel,
        id: inst.variantId,
        quantity: inst.quantity,
        unitPrice: Number(option.price) || 0,
      });
    });
    return items;
  }

  function formatPieceCount(count) {
    if (count === 1) return uiLabel('pieceOne', '1 Matching Piece');
    return uiLabel('pieceMany', '{count} Matching Pieces', { count: count });
  }

  function updateSummary() {
    var items = getSelectedItems();
    var pieceCount = items.reduce(function (sum, item) {
      return sum + item.quantity;
    }, 0);
    var subtotal = items.reduce(function (sum, item) {
      return sum + item.unitPrice * item.quantity;
    }, 0);
    if (!pieceCount) {
      if (emptyCopy) emptyCopy.removeAttribute('hidden');
      if (chips) {
        chips.innerHTML = '';
        chips.setAttribute('hidden', 'hidden');
      }
      if (total) {
        total.textContent = '';
        total.setAttribute('hidden', 'hidden');
      }
      addButton.setAttribute('disabled', 'disabled');
      publishMatchingSetStickyState(items, pieceCount, subtotal);
      return;
    }

    if (emptyCopy) emptyCopy.setAttribute('hidden', 'hidden');
    if (chips) {
      chips.innerHTML =
        '<span class="product-matching-set__chip product-matching-set__chip--count">' +
        escapeHtml(formatPieceCount(pieceCount)) +
        '</span>';
      chips.removeAttribute('hidden');
    }
    if (total) {
      total.innerHTML =
        escapeHtml(uiLabel('total', 'Total')) + ' <strong>' + escapeHtml(formatMoney(subtotal, currency)) + '</strong>';
      total.removeAttribute('hidden');
    }
    addButton.removeAttribute('disabled');
    publishMatchingSetStickyState(items, pieceCount, subtotal);
  }

  function publishMatchingSetStickyState(items, pieceCount, subtotal) {
    var summaryItems = (items || []).map(function (item) {
      var label = [item.roleLabel, item.sizeLabel].filter(Boolean).join(' ');
      if (item.quantity > 1) label += ' x' + item.quantity;
      return label;
    }).filter(Boolean);
    var detail = {
      sectionId: sectionId,
      pieceCount: pieceCount || 0,
      pieceCountLabel: pieceCount ? formatPieceCount(pieceCount) : '',
      totalText: pieceCount ? uiLabel('total', 'Total') + ' ' + formatMoney(subtotal || 0, currency) : '',
      summaryText: summaryItems.join(', '),
      isReady: !!pieceCount,
    };

    try {
      window.DLMMatchingSetStickyState = window.DLMMatchingSetStickyState || {};
      window.DLMMatchingSetStickyState[sectionId] = detail;
      document.dispatchEvent(
        new CustomEvent('dlm:matching-set-summary', {
          detail: detail,
        })
      );
    } catch (_e) { /* non-critical sticky enhancement */ }
  }

  function renderInstanceSizeBlurb(inst, group) {
    // Friendly green confirmation line beneath the pills once a size
    // is picked. The detailed measurements live in the pinned compact
    // tooltip floating above the selected pill (see renderCard) —
    // same look as the unselected-pill hover tooltip, just pinned
    // open with an × and a cm/in toggle.
    var option = getOptionByVariantId(group, inst.variantId);
    if (!option) return '';
    var sizeLabel = option.sizeLabel || '';
    var unitPrice = Number(option.price) || 0;

    return (
      '<p class="product-matching-set__size-blurb" role="status">' +
      '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="20 6 9 17 4 12"/></svg>' +
      '<span class="product-matching-set__size-blurb-text">' +
      escapeHtml(group.label) +
      ' &middot; <strong>' +
      escapeHtml(sizeLabel) +
      '</strong> &middot; ' +
      escapeHtml(formatMoney(unitPrice, currency)) +
      ' ' +
      escapeHtml(uiLabel('each', 'each')) +
      '</span>' +
      '</p>'
    );
  }

  function renderCard(inst) {
    var group = getGroupByKey(inst.groupKey);
    if (!group) return '';

    // Backfill the new instance fields for cards that pre-existed the
    // axes refactor: derive sizeLabel + axisSelections from variantId
    // if they're empty.
    if (!inst.sizeLabel && inst.variantId) {
      var existingOpt = getOptionByVariantId(group, inst.variantId);
      if (existingOpt) {
        inst.sizeLabel = existingOpt.sizeLabel || '';
        inst.axisSelections = Object.assign({}, existingOpt.axes || {});
      }
    }
    if (!inst.axisSelections) inst.axisSelections = {};

    var minimumPrice = group.options.reduce(function (lowest, option) {
      return lowest === null || option.price < lowest ? option.price : lowest;
    }, null);

    var distinctSizes = getDistinctSizesForGroup(group);
    var axisNames = getAxisNamesForGroup(group);

    var selectedPanelOption = null;
    var selectedPanelMeasurementsHtml = '';
    var selectedPanelHtml = '';

    if (inst.sizeLabel && !closedPanels[inst.instanceId]) {
      selectedPanelOption =
        resolveVariantInGroup(group, inst.sizeLabel, inst.axisSelections) ||
        group.options.find(function (o) { return o.sizeLabel === inst.sizeLabel; });
      var selectedPanelMeasurements = selectedPanelOption ? findMeasurementsForOption(group, selectedPanelOption) : null;
      selectedPanelMeasurementsHtml = selectedPanelMeasurements ? buildMeasurementsHtml(selectedPanelMeasurements) : '';
      if (selectedPanelMeasurementsHtml) {
        var mobileIsImperial = unitSystem === 'imperial';
        selectedPanelHtml =
          '<div class="product-matching-set__mobile-size-panel" role="status">' +
          '<div class="product-matching-set__mobile-size-panel-header">' +
          '<strong class="product-matching-set__mobile-size-panel-title">' +
          escapeHtml(group.label) +
          ' &middot; ' +
          escapeHtml(selectedPanelOption.sizeLabel || inst.sizeLabel || '') +
          '</strong>' +
          '<span class="product-matching-set__pill-tooltip-controls">' +
          '<span class="product-matching-set__pill-tooltip-toggle" role="group" aria-label="' +
          escapeHtml(uiLabel('units', 'Units')) +
          '">' +
          '<button type="button" class="product-matching-set__pill-tooltip-unit' +
          (mobileIsImperial ? '' : ' is-active') +
          '" data-unit-set="metric" aria-pressed="' +
          (mobileIsImperial ? 'false' : 'true') +
          '">cm</button>' +
          '<button type="button" class="product-matching-set__pill-tooltip-unit' +
          (mobileIsImperial ? ' is-active' : '') +
          '" data-unit-set="imperial" aria-pressed="' +
          (mobileIsImperial ? 'true' : 'false') +
          '">in</button>' +
          '</span>' +
          '<button type="button" class="product-matching-set__pill-tooltip-close" data-size-panel-close="' +
          escapeHtml(inst.instanceId) +
          '" aria-label="' +
          escapeHtml(uiLabel('closeSizeDetails', 'Close size details')) +
          '">×</button>' +
          '</span>' +
          '</div>' +
          selectedPanelMeasurementsHtml +
          '</div>';
      }
    }

    var pillsHtml = distinctSizes
      .map(function (sizeLabel) {
        // Each distinct size pill represents ONE size — its underlying
        // variant is resolved via current axisSelections (e.g. picked
        // color). When no variant exists for this size + selections we
        // disable & strike through the pill so shoppers see what's OOS.
        var representative = resolveVariantInGroup(group, sizeLabel, inst.axisSelections) ||
          group.options.find(function (o) { return o.sizeLabel === sizeLabel; });
        if (!representative) return '';
        var option = representative;
        var isSelected = inst.sizeLabel === sizeLabel;
        var combo = resolveVariantInGroup(group, sizeLabel, inst.axisSelections);
        var isDisabled = !combo || combo.available === false;

        // Compact floating tooltip on EVERY pill that has measurement
        // data. When the pill is unselected it shows on hover/focus
        // (mouse-over preview). When the pill is selected AND the
        // shopper hasn't dismissed it, the tooltip is pinned open
        // with an × close button and a cm/in toggle so the size
        // information stays visible while picking quantity and
        // other family members. Picking a different size on the
        // same card auto-reopens the new pinned tooltip.
        var measurements = findMeasurementsForOption(group, option);
        var measurementsHtml = measurements ? buildMeasurementsHtml(measurements) : '';
        var isPinned = isSelected && measurementsHtml && !closedPanels[inst.instanceId];
        var tooltipHtml = '';
        if (measurementsHtml) {
          var pinnedExtras = '';
          if (isPinned) {
            var isImperial = unitSystem === 'imperial';
            pinnedExtras =
              '<span class="product-matching-set__pill-tooltip-controls">' +
              '<span class="product-matching-set__pill-tooltip-toggle" role="group" aria-label="' +
              escapeHtml(uiLabel('units', 'Units')) +
              '">' +
              '<button type="button" class="product-matching-set__pill-tooltip-unit' +
              (isImperial ? '' : ' is-active') +
              '" data-unit-set="metric" aria-pressed="' +
              (isImperial ? 'false' : 'true') +
              '">cm</button>' +
              '<button type="button" class="product-matching-set__pill-tooltip-unit' +
              (isImperial ? ' is-active' : '') +
              '" data-unit-set="imperial" aria-pressed="' +
              (isImperial ? 'true' : 'false') +
              '">in</button>' +
              '</span>' +
              '<button type="button" class="product-matching-set__pill-tooltip-close" data-size-panel-close="' +
              escapeHtml(inst.instanceId) +
              '" aria-label="' +
              escapeHtml(uiLabel('closeSizeDetails', 'Close size details')) +
              '">×</button>' +
              '</span>';
          }
          tooltipHtml =
            '<span class="product-matching-set__pill-tooltip' +
            (isPinned ? ' is-pinned' : '') +
            '" role="tooltip">' +
            '<span class="product-matching-set__pill-tooltip-header">' +
            '<span class="product-matching-set__pill-tooltip-title">' +
            escapeHtml(group.label) +
            ' &middot; ' +
            escapeHtml(option.sizeLabel || '') +
            '</span>' +
            pinnedExtras +
            '</span>' +
            measurementsHtml +
            '</span>';
        }

        return (
          '<span class="product-matching-set__pill-wrap' +
          (tooltipHtml ? ' has-tooltip' : '') +
          '">' +
          '<button type="button"' +
          ' class="product-matching-set__pill' +
          (isSelected ? ' is-selected' : '') +
          (isDisabled ? ' is-disabled' : '') +
          '"' +
          ' data-instance-pill="' +
          escapeHtml(inst.instanceId) +
          '"' +
          ' data-size-label="' +
          escapeHtml(sizeLabel) +
          '"' +
          ' data-price="' +
          escapeHtml(option.price) +
          '"' +
          (isDisabled ? ' disabled aria-disabled="true"' : '') +
          (isDisabled ? ' title="' + escapeHtml(uiLabel('outOfStockCurrent', 'Out of stock for current selection')) + '"' : '') +
          ' aria-pressed="' +
          (isSelected ? 'true' : 'false') +
          '">' +
          escapeHtml(sizeLabel) +
          '</button>' +
          tooltipHtml +
          '</span>'
        );
      })
      .filter(Boolean)
      .join('');

    // Per-axis pickers (Color, Pattern, etc.) rendered after the size
    // pill row. Each axis becomes its own row with swatches. OOS combos
    // for the current size selection are disabled but visible.
    var axisRowsHtml = axisNames.map(function (axisName) {
      var values = getAxisValuesForGroup(group, axisName);
      if (values.length <= 1) return ''; // single-value axis = no choice
      var pickedValue = inst.axisSelections[axisName] || '';
      // Debug: log axis probe state when window.DLM_BUNDLE_DEBUG is
      // set (use ?dlm_bundle_debug=1 in the URL to enable). Helps
      // trace OOS false-positives.
      var debug = typeof window !== 'undefined' && window.DLM_BUNDLE_DEBUG;
      var swatchesHtml = values.map(function (value) {
        // Probe availability: variant must exist for current sizeLabel
        // (if picked) and this axis value. If no size is picked yet,
        // probe across any size.
        var probeSels = Object.assign({}, inst.axisSelections);
        probeSels[axisName] = value;
        var sizeForProbe = inst.sizeLabel || '';
        var matchOpt = resolveVariantInGroup(group, sizeForProbe, probeSels);
        var anyMatch = matchOpt || group.options.find(function (o) {
          return (o.axes && o.axes[axisName]) === value;
        });
        var avail = matchOpt && matchOpt.available !== false;
        var disabled = !anyMatch || (sizeForProbe && !avail);
        var isSelectedSwatch = pickedValue === value;
        if (debug) {
          /* eslint-disable no-console */
          console.log('[bundle axis probe]', {
            role: group.label,
            axisName: axisName,
            value: value,
            size: sizeForProbe,
            probeSels: JSON.stringify(probeSels),
            matchOpt: matchOpt && { id: matchOpt.id, axes: matchOpt.axes, sizeLabel: matchOpt.sizeLabel, available: matchOpt.available },
            anyMatch: !!anyMatch,
            avail: avail,
            disabled: disabled,
            groupOptions: group.options.map(function (o) { return { sl: o.sizeLabel, axes: o.axes, avail: o.available }; }),
          });
          /* eslint-enable no-console */
        }
        return (
          '<button type="button"' +
          ' class="product-matching-set__axis-pill' +
          (isSelectedSwatch ? ' is-selected' : '') +
          (disabled ? ' is-disabled' : '') +
          '"' +
          ' data-instance-axis="' +
          escapeHtml(inst.instanceId) +
          '"' +
          ' data-axis-name="' +
          escapeHtml(axisName) +
          '"' +
          ' data-axis-value="' +
          escapeHtml(value) +
          '"' +
          (disabled ? ' disabled aria-disabled="true" title="' + escapeHtml(uiLabel('notAvailableSelectedSize', 'Not available in your selected size')) + '"' : '') +
          ' aria-pressed="' +
          (isSelectedSwatch ? 'true' : 'false') +
          '">' +
          escapeHtml(value) +
          '</button>'
        );
      }).join('');
      // Inline contextual prompt for this axis — appears beneath the
      // axis pills when nothing has been picked yet. Small, subtle.
      var axisHint = pickedValue
        ? ''
        : '<p class="product-matching-set__inline-hint">' +
          escapeHtml(uiLabel('pickAxis', 'Pick a {axis}', { axis: axisName.toLowerCase() })) +
          '</p>';
      return (
        '<div class="product-matching-set__axis-row" role="group" aria-label="' +
        escapeHtml(axisName) +
        '">' +
        '<span class="product-matching-set__axis-label">' +
        escapeHtml(axisName) +
        (pickedValue ? ': <strong>' + escapeHtml(pickedValue) + '</strong>' : '') +
        '</span>' +
        '<div class="product-matching-set__axis-pills">' + swatchesHtml + '</div>' +
        axisHint +
        '</div>'
      );
    }).filter(Boolean).join('');

    var qty = inst.quantity || 1;

    return (
      '<div class="product-matching-set__card" data-instance-card="' +
      escapeHtml(inst.instanceId) +
      '" data-role-card="' +
      escapeHtml(inst.roleKey) +
      '">' +
      '<div class="product-matching-set__card-header">' +
      '<span class="product-matching-set__card-title">' +
      escapeHtml(group.label) +
      '</span>' +
      '<button type="button" class="product-matching-set__card-remove" data-instance-remove="' +
      escapeHtml(inst.instanceId) +
      '" aria-label="' +
      escapeHtml(uiLabel('removeRole', 'Remove {role}', { role: group.label })) +
      '">×</button>' +
      '</div>' +
      (group.helper
        ? '<span class="product-matching-set__card-helper">' + escapeHtml(group.helper) + '</span>'
        : '') +
      '<div class="product-matching-set__pills" role="group" aria-label="' +
      escapeHtml(group.label + ' size') +
      '">' +
      pillsHtml +
      '</div>' +
      selectedPanelHtml +
      // Inline contextual prompt directly under the size pills if no
      // size picked yet. Small + subtle (sits inside the row, not as
      // a full-width banner) so each prompt reads as guidance for the
      // adjacent control.
      (!inst.sizeLabel
        ? '<p class="product-matching-set__inline-hint">' + escapeHtml(uiLabel('pickSize', 'Pick a size')) + '</p>'
        : '') +
      // Per-card axis rows (Color, Pattern, etc.) — each axis row
      // emits its own inline "Pick a {axis}" hint below its pills.
      axisRowsHtml +
      // Green confirmation blurb only when the card is fully resolved
      // (size + every axis picked → variantId exists).
      (inst.variantId ? renderInstanceSizeBlurb(inst, group) : '') +
      '<div class="product-matching-set__qty" data-instance-qty="' +
      escapeHtml(inst.instanceId) +
      '">' +
      '<button type="button" class="product-matching-set__qty-button" data-qty-action="dec" aria-label="' +
      escapeHtml(uiLabel('decreaseQuantity', 'Decrease quantity')) +
      '">−</button>' +
      '<span class="product-matching-set__qty-value" data-qty-value>' +
      String(qty) +
      '</span>' +
      '<button type="button" class="product-matching-set__qty-button" data-qty-action="inc" aria-label="' +
      escapeHtml(uiLabel('increaseQuantity', 'Increase quantity')) +
      '">+</button>' +
      '<span class="product-matching-set__card-price" data-role-price>' +
      escapeHtml(formatMoney(minimumPrice, currency)) +
      '</span>' +
      '</div>' +
      // Per-card "Find my fit" link — uses the same delegated handler
      // as the Purchase Confidence size-guide trigger.
      '<a href="#size-chart" class="product-matching-set__fit-link" data-pdp-size-guide-trigger aria-haspopup="dialog">' +
      escapeHtml(uiLabel('findFit', "Find {role}'s fit", { role: group.label })) +
      ' →' +
      '</a>' +
      '</div>'
    );
  }

  function renderAddRoleButtons() {
    // Always show one + Add button per role available on this product.
    // Tapping creates a NEW card instance (so a mom with two daughters
    // can have two Girl cards, each with its own size + quantity).
    var reps = getRoleRepresentatives();
    if (!reps.length) return '';
    var buttonsHtml = reps
      .map(function (group) {
        return (
          '<button type="button" class="product-matching-set__add-role" data-add-role-group="' +
          escapeHtml(group.key) +
          '">' +
          escapeHtml(uiLabel('addRole', '+ Add {role}', { role: group.label })) +
          '</button>'
        );
      })
      .join('');
    return (
      '<div class="product-matching-set__add-roles" role="group" aria-label="' +
      escapeHtml(uiLabel('addAnotherFamilyMember', 'Add another family member')) +
      '">' +
      buttonsHtml +
      '</div>'
    );
  }

  function getDefaultGroupsForBootstrap(groups) {
    // First page load: surface ONE adult card (Mother → Father) + ONE
    // child card (Girl → Boy → Child → Baby), in role-priority order.
    // Falls back gracefully when the product is missing either pole.
    var result = [];

    var adultPriorities = ['mother', 'father', 'adult'];
    for (var i = 0; i < adultPriorities.length && !result.length; i += 1) {
      var rk = adultPriorities[i];
      var match = groups.find(function (g) {
        return (g.roleKey || g.key) === rk;
      });
      if (match) result.push(match);
    }

    var childPriorities = ['girl', 'boy', 'child', 'baby'];
    for (var j = 0; j < childPriorities.length; j += 1) {
      var ck = childPriorities[j];
      var cmatch = groups.find(function (g) {
        return (g.roleKey || g.key) === ck;
      });
      if (cmatch && result.indexOf(cmatch) === -1) {
        result.push(cmatch);
        break;
      }
    }

    // Ensure two cards default-visible. If the product only has one
    // role bucket, push the next available group. (Some products may
    // only have a single bucket — e.g. all "Child" variants — and we
    // still want the shopper to see a clear "+ Add another Child"
    // affordance below the single visible card.)
    if (!result.length && groups.length) result.push(groups[0]);
    if (result.length === 1 && groups.length > 1) {
      var second = groups.find(function (g) {
        return g !== result[0];
      });
      if (second) result.push(second);
    }
    return result;
  }

  function bindCardEvents() {
    // Size pill click — sets inst.sizeLabel and recomputes variantId
    // from the current axisSelections. Toggling the selected pill
    // clears it.
    builder.querySelectorAll('[data-instance-pill]').forEach(function (pill) {
      pill.addEventListener('click', function () {
        if (pill.hasAttribute('disabled')) return;
        var instanceId = pill.getAttribute('data-instance-pill');
        var sizeLabel = pill.getAttribute('data-size-label');
        var inst = findInstance(instanceId);
        if (!inst) return;
        if (inst.sizeLabel === sizeLabel) {
          inst.sizeLabel = '';
        } else {
          inst.sizeLabel = sizeLabel;
        }
        refreshInstanceVariantId(inst);
        delete closedPanels[instanceId];
        if (status) status.setAttribute('hidden', 'hidden');
        renderBuilder();
      });

      // Auto-close any pinned size panel as soon as the shopper hovers
      // (mouseenter) or keyboard-focuses a different size pill. That
      // includes the same card, so a clicked XL panel is dismissed
      // before a hovered S preview can show. Two panels never stack.
      // We only re-render when state actually changed, so hovering
      // around the currently selected pill doesn't trigger render thrash.
      var dismissPinnedPanelsForPillPreview = function () {
        // On touch/mobile, focus fires before the synthetic click. If we
        // re-render here, the first tap on a new size gets swallowed and
        // shoppers have to tap twice. Let the click handler switch the
        // selected size and reopen the panel in one pass.
        if (isMobileSizePanelViewport()) return;
        var hoveredInstanceId = pill.getAttribute('data-instance-pill');
        var hoveredSizeLabel = pill.getAttribute('data-size-label');
        var changed = false;
        for (var i = 0; i < instances.length; i += 1) {
          var other = instances[i];
          if (!other) continue;
          if (other.instanceId === hoveredInstanceId && other.sizeLabel === hoveredSizeLabel) continue;
          // A pinned panel exists when the other card has a sizeLabel
          // selected AND the shopper hasn't already X-dismissed it.
          if (other.sizeLabel && !closedPanels[other.instanceId]) {
            closedPanels[other.instanceId] = true;
            changed = true;
          }
        }
        if (changed) renderBuilder();
      };
      pill.addEventListener('mouseenter', dismissPinnedPanelsForPillPreview);
      pill.addEventListener('focusin', dismissPinnedPanelsForPillPreview);
    });

    // Axis swatch click (Color, Pattern, etc.). Picking a new value
    // updates inst.axisSelections; if the current size is no longer
    // available in the new combo, sizeLabel is preserved but variantId
    // becomes '' (and the size pill renders as OOS until shopper
    // adjusts).
    builder.querySelectorAll('[data-instance-axis]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        if (btn.hasAttribute('disabled')) return;
        var instanceId = btn.getAttribute('data-instance-axis');
        var axisName = btn.getAttribute('data-axis-name');
        var axisValue = btn.getAttribute('data-axis-value');
        var inst = findInstance(instanceId);
        if (!inst || !axisName) return;
        if (!inst.axisSelections) inst.axisSelections = {};
        if (inst.axisSelections[axisName] === axisValue) {
          delete inst.axisSelections[axisName];
        } else {
          inst.axisSelections[axisName] = axisValue;
        }
        refreshInstanceVariantId(inst);
        delete closedPanels[instanceId];
        renderBuilder();
      });
    });

    // Size-panel close (×).
    builder.querySelectorAll('[data-size-panel-close]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var instanceId = btn.getAttribute('data-size-panel-close');
        closedPanels[instanceId] = true;
        renderBuilder();
      });
    });

    // Per-panel cm/in toggle — flips the global unitSystem and
    // re-renders ALL panels. Persists to localStorage.
    builder.querySelectorAll('[data-unit-set]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var next = btn.getAttribute('data-unit-set');
        setUnitSystem(next);
      });
    });

    builder.querySelectorAll('[data-instance-qty]').forEach(function (qtyEl) {
      var instanceId = qtyEl.getAttribute('data-instance-qty');
      qtyEl.querySelectorAll('[data-qty-action]').forEach(function (button) {
        button.addEventListener('click', function () {
          var inst = findInstance(instanceId);
          if (!inst) return;
          if (!isMobileSizePanelViewport()) closeOpenSizePanels();
          var action = button.getAttribute('data-qty-action');
          if (action === 'inc') {
            inst.quantity = (inst.quantity || 1) + 1;
          } else if (action === 'dec') {
            var current = inst.quantity || 1;
            if (current <= 1) {
              // At qty=1, − behaves like × — remove the whole card so
              // shoppers don't get stuck with a row they can't dismiss
              // from the qty stepper.
              removeInstance(instanceId);
            } else {
              inst.quantity = current - 1;
            }
          }
          renderBuilder();
        });
      });
    });

    builder.querySelectorAll('[data-instance-remove]').forEach(function (removeBtn) {
      removeBtn.addEventListener('click', function () {
        var instanceId = removeBtn.getAttribute('data-instance-remove');
        if (!isMobileSizePanelViewport()) closeOpenSizePanels();
        removeInstance(instanceId);
        renderBuilder();
      });
    });

    builder.querySelectorAll('[data-add-role-group]').forEach(function (addBtn) {
      addBtn.addEventListener('click', function () {
        var groupKey = addBtn.getAttribute('data-add-role-group');
        var group = getGroupByKey(groupKey);
        if (!group) return;
        if (!isMobileSizePanelViewport()) closeOpenSizePanels();
        addInstanceForGroup(group);
        renderBuilder();
      });
    });
  }

  function renderBuilder(preservedSelections) {
    // Pass `true` so we get every variant (including OOS combos) plus
    // the axes map. When Type is implicit per role (mother↔Dress,
    // father↔Shirt etc.), also skip the Type filter so all four role
    // groups stay available regardless of which Type the legacy picker
    // happens to have selected.
    var currentCtx = getCurrentOptionContext(variantSelects);
    var groups = buildRoleGroups(productData, currentCtx, true, {
      skipTypeFilter: typeIsImplicit,
    });
    roleGroupsCache = groups;

    // Optional debug dump. Enable in browser console with
    //   window.DLM_BUNDLE_DEBUG = true;
    // and click any pill to trigger a re-render — useful when chasing
    // per-card axis bugs (e.g. "only one color showing" cases).
    try {
      if (window && window.DLM_BUNDLE_DEBUG) {
      // eslint-disable-next-line no-console
      console.debug('[DLM bundle render]', {
        typeIsImplicit: typeIsImplicit,
        currentCtx: currentCtx,
        productOptions: productData.options,
        groups: groups.map(function (g) {
          return {
            key: g.key, roleKey: g.roleKey, label: g.label, helper: g.helper,
            distinctSizes: getDistinctSizesForGroup(g),
            axisNames: getAxisNamesForGroup(g),
            axisValues: getAxisNamesForGroup(g).reduce(function (a, n) {
              a[n] = getAxisValuesForGroup(g, n);
              return a;
            }, {}),
            optionsSample: g.options.slice(0, 30).map(function (o) {
              return { id: o.id, sl: o.sizeLabel, axes: o.axes, avail: o.available };
            }),
          };
        }),
        instances: instances.map(function (inst) {
          return {
            id: inst.instanceId, roleKey: inst.roleKey, groupKey: inst.groupKey,
            sizeLabel: inst.sizeLabel, axisSelections: inst.axisSelections, variantId: inst.variantId,
          };
        }),
      });
      }
    } catch (_e) { /* ignore */ }

    if (groups.length < 2) {
      builder.setAttribute('hidden', 'hidden');
      return;
    }

    builder.removeAttribute('hidden');

    // Type axis reactivity. Only relevant when Type is NOT implicit —
    // for products where Type cleanly partitions roles, the per-card
    // model already shows all roles and Type changes are noise we
    // don't want to react to (they'd erase the shopper's cards).
    if (!typeIsImplicit) {
      var typeKey = '';
      var ctxKeys = Object.keys(currentCtx);
      for (var ti = 0; ti < ctxKeys.length; ti += 1) {
        if (isTypeLikeLabel(ctxKeys[ti])) {
          typeKey = String(currentCtx[ctxKeys[ti]] || '').toLowerCase();
          break;
        }
      }
      if (lastTypeContext !== null && lastTypeContext !== typeKey) {
        instances = [];
        hasSeededDefaults = false;
        closedPanels = Object.create(null);
      }
      lastTypeContext = typeKey;
    }

    // First render (or after a Type change): seed one EMPTY card per
    // default-visible role. The shopper must deliberately pick a size
    // — no URL-variant pre-selection (covered in earlier fix).
    if (!hasSeededDefaults && !instances.length) {
      hasSeededDefaults = true;
      getDefaultGroupsForBootstrap(groups).forEach(function (group) {
        addInstanceForGroup(group);
      });
    }

    // NOTE: we intentionally drop the old preservedSelections bootstrap
    // here. The `instances` array IS the source of truth and survives
    // re-renders (it lives in the closure). Auto-filling cards from a
    // <variant-selects> change event would re-trigger the same wrong
    // pre-selection behavior described above.

    // Render cards in instance-order (the order the shopper added them).
    var visibleCardsHtml = instances.map(renderCard).join('');
    roleGrid.innerHTML = visibleCardsHtml + renderAddRoleButtons();

    bindCardEvents();
    updateSummary();
    positionMobilePillTooltips();
  }

  // ─────────────────────────────────────────────────────────────────
  // Mobile pill-tooltip positioner.
  //
  // On phones the tooltip can't be centered over the pill (it would
  // clip past the left edge for the leftmost pill, hiding text like
  // "Garment Length", "Skirt Length", "Hip"). The matching CSS rule
  // (see component-product-desktop-ux.css "Mobile: full-width
  // measurement panel") repositions the tooltip with `position: fixed;
  // left: 1rem; right: 1rem;` so it spans the viewport — but it still
  // needs a vertical position. We compute it here and write it to the
  // tooltip element as a CSS variable.
  //
  // We anchor the tooltip just ABOVE the pill row so the panel doesn't
  // cover the pills the shopper is comparing. If there's no room above
  // (pill row is near the top of the viewport), we drop it BELOW.
  // ─────────────────────────────────────────────────────────────────
  function positionMobilePillTooltips() {
    if (typeof window === 'undefined') return;
    if (window.matchMedia && !window.matchMedia('(max-width: 749px)').matches) {
      // Desktop / tablet: the default CSS positioning is correct.
      // Clear any previously-set CSS vars in case the user resized.
      var stale = roleGrid && roleGrid.querySelectorAll
        ? roleGrid.querySelectorAll('.product-matching-set__pill-tooltip')
        : [];
      for (var s = 0; s < stale.length; s += 1) {
        stale[s].style.removeProperty('--dlm-pill-tooltip-top');
        stale[s].style.removeProperty('--dlm-pill-tooltip-bottom');
      }
      return;
    }
    if (!roleGrid || !roleGrid.querySelectorAll) return;

    var tooltips = roleGrid.querySelectorAll('.product-matching-set__pill-tooltip');
    for (var i = 0; i < tooltips.length; i += 1) {
      var tip = tooltips[i];
      var wrap = tip.closest('.product-matching-set__pill-wrap');
      var pillsRow = wrap ? wrap.closest('.product-matching-set__pills') : null;
      var anchor = pillsRow || wrap;
      if (!anchor) continue;
      var rect = anchor.getBoundingClientRect();
      var viewportH = window.innerHeight || document.documentElement.clientHeight;
      var GAP = 12; // gap between tooltip and pill row, in px
      // Prefer ABOVE the row (so pills stay tappable below it).
      // If above doesn't have enough room (< 220px), drop BELOW.
      var spaceAbove = rect.top;
      var spaceBelow = viewportH - rect.bottom;
      if (spaceAbove >= 220 || spaceAbove >= spaceBelow) {
        tip.style.setProperty('--dlm-pill-tooltip-bottom', (viewportH - rect.top + GAP) + 'px');
        tip.style.removeProperty('--dlm-pill-tooltip-top');
      } else {
        tip.style.setProperty('--dlm-pill-tooltip-top', (rect.bottom + GAP) + 'px');
        tip.style.removeProperty('--dlm-pill-tooltip-bottom');
      }
    }
  }

  // Recompute when the viewport changes (rotation, browser-chrome
  // hide/show on iOS Safari). Throttled with rAF so we don't thrash.
  var __dlmPillTooltipResizeRaf = null;
  function schedulePillTooltipReposition() {
    if (__dlmPillTooltipResizeRaf) return;
    __dlmPillTooltipResizeRaf = window.requestAnimationFrame(function () {
      __dlmPillTooltipResizeRaf = null;
      positionMobilePillTooltips();
    });
  }
  if (typeof window !== 'undefined') {
    window.addEventListener('resize', schedulePillTooltipReposition);
    window.addEventListener('scroll', schedulePillTooltipReposition, { passive: true });
    window.addEventListener('orientationchange', schedulePillTooltipReposition);
  }

  async function addSelectedItems() {
    var items = getSelectedItems()
      .filter(function (item) {
        return !!item.id && item.quantity > 0;
      })
      .map(function (item) {
        return { id: item.id, quantity: item.quantity };
      });

    var selectedItems = items;

    if (!selectedItems.length) return;

    addButton.setAttribute('disabled', 'disabled');
    status.setAttribute('hidden', 'hidden');

    var cartDrawer = document.querySelector('cart-drawer');
    var config = typeof fetchConfig === 'function' ? fetchConfig('javascript') : { method: 'POST', headers: {} };
    config.headers = config.headers || {};
    config.headers['X-Requested-With'] = 'XMLHttpRequest';
    delete config.headers['Content-Type'];

    var formData = new FormData();
    selectedItems.forEach(function (item, index) {
      formData.append('items[' + index + '][id]', item.id);
      formData.append('items[' + index + '][quantity]', String(item.quantity));
    });

    if (cartDrawer && typeof cartDrawer.getSectionsToRender === 'function') {
      formData.append(
        'sections',
        cartDrawer
          .getSectionsToRender()
          .map(function (section) {
            return section.id;
          })
          .join(',')
      );
      formData.append('sections_url', window.location.pathname);
    }

    config.body = formData;

    try {
      var response = await fetch((window.routes && window.routes.cart_add_url) || '/cart/add', config);
      var parsed = await response.json();

      if (!response.ok || parsed.status) {
        throw new Error(parsed.description || parsed.message || 'Add to cart failed');
      }

      status.textContent = wrapper.getAttribute('data-matching-set-success') || 'Matching set added to cart.';
      status.removeAttribute('hidden');

      if (cartDrawer && parsed.sections) {
        cartDrawer.renderContents(parsed);
      } else {
        window.location.href = (window.routes && window.routes.cart_url) || '/cart';
      }
    } catch (error) {
      status.textContent =
        wrapper.getAttribute('data-matching-set-error') || 'Unable to add the selected pieces. Please try again.';
      status.removeAttribute('hidden');
      console.error(error);
    } finally {
      updateSummary();
    }
  }

  addButton.addEventListener('click', function () {
    addSelectedItems();
  });

  renderBuilder();

  if (variantSelects) {
    variantSelects.addEventListener('change', function () {
      renderBuilder(getMatchingSetSelections(builder));
    });
  }
}

function initMatchingSizeGuide(wrapper, sectionId, productData) {
  var UNIT_SYSTEM_STORAGE_KEY = 'dlm_size_chart_unit_system';
  var productSection = sectionId ? document.getElementById('MainProduct-' + sectionId) : null;
  var sizeGuideRoot = productSection || wrapper.closest('[id^="MainProduct-"]') || wrapper;
  var productHandle = String(wrapper.getAttribute('data-product-handle') || '').trim();
  var descriptionRoot = getCurrentDescriptionRoot();
  var imagePresetGuide = descriptionRoot ? getImageBasedSizeGuidePreset(descriptionRoot) : null;
  var snapshot = sizeGuideRoot ? sizeGuideRoot.querySelector('[data-matching-size-guide-snapshot]') : null;
  var details = sizeGuideRoot ? sizeGuideRoot.querySelector('[data-matching-size-guide]') : null;
  var content = sizeGuideRoot ? sizeGuideRoot.querySelector('[data-matching-size-guide-content]') : null;
  var summary = details ? details.querySelector('summary') : null;
  var sizeTable = getSizeGuideTable(sizeGuideRoot, getCurrentSizeSelect(), getSelectedGuideTypeValue());
  var defaultLocaleSizeGuideLoad = null;
  if (!snapshot || !details || !content) return;

  var parsed = sizeTable ? parseSizeGuideTable(sizeTable) : null;
  if (sizeTable && !parsed) return;
  if (descriptionRoot && parsed) hideRedundantSizeGuideSources(descriptionRoot, imagePresetGuide);

  var compareLabel = wrapper.getAttribute('data-size-guide-compare-label') || 'Compare all sizes';
  var groupedLabel = wrapper.getAttribute('data-size-guide-grouped-label') || 'Compare family sizes';
  var snapshotLabel = wrapper.getAttribute('data-size-guide-selected-label') || 'Your size details';
  var compareHintLabel =
    wrapper.getAttribute('data-size-guide-compare-hint') || 'Open the full chart below to compare nearby sizes.';
  var unitToggleLabel = wrapper.getAttribute('data-size-guide-unit-toggle-label') || 'Size chart units';
  var groups = buildSizeGuideGroups(parsed);
  var selectedUnitSystem = getStoredSizeGuideUnitSystem() || 'metric';
  var scheduledGuideRender = null;

  function getCurrentDescriptionRoot() {
    return (sizeGuideRoot && sizeGuideRoot.querySelector('[data-product-description]')) || document.querySelector('[data-product-description]');
  }

  function defaultLocaleProductJsonUrl() {
    if (!productHandle || !window.location || !window.location.origin) return '';
    return window.location.origin + '/products/' + encodeURIComponent(productHandle) + '.js';
  }

  function htmlContainsSizeGuideTable(html) {
    return /<table\b/i.test(String(html || '')) && /size-chart/i.test(String(html || ''));
  }

  function appendDefaultLocaleSizeGuideSource(descriptionHtml) {
    var targetRoot = getCurrentDescriptionRoot();
    if (!targetRoot || !htmlContainsSizeGuideTable(descriptionHtml)) return false;
    if (targetRoot.querySelector('[data-default-locale-size-guide-source]')) return true;

    var parserRoot = document.createElement('div');
    parserRoot.innerHTML = descriptionHtml;
    var sourceTables = Array.from(parserRoot.querySelectorAll('table#size-chart, table[id*="size-chart"], table.size-chart'));
    if (!sourceTables.length) return false;

    var sourceContainer = document.createElement('div');
    sourceContainer.setAttribute('data-default-locale-size-guide-source', 'true');
    sourceContainer.setAttribute('aria-hidden', 'true');
    sourceContainer.hidden = true;
    sourceContainer.style.setProperty('display', 'none', 'important');

    sourceTables.forEach(function (table) {
      var previous = table.previousElementSibling;
      if (previous && /^H[1-6]$/i.test(previous.tagName) && /size|chart/i.test(previous.textContent || '')) {
        sourceContainer.appendChild(previous.cloneNode(true));
      }
      sourceContainer.appendChild(table.cloneNode(true));
    });

    targetRoot.appendChild(sourceContainer);
    return true;
  }

  function loadDefaultLocaleSizeGuideSource() {
    if (defaultLocaleSizeGuideLoad) return defaultLocaleSizeGuideLoad;

    var productJsonUrl = defaultLocaleProductJsonUrl();
    if (!productJsonUrl || typeof fetch !== 'function') {
      defaultLocaleSizeGuideLoad = Promise.resolve(false);
      return defaultLocaleSizeGuideLoad;
    }

    defaultLocaleSizeGuideLoad = fetch(productJsonUrl, { credentials: 'same-origin' })
      .then(function (response) {
        if (!response || !response.ok) return null;
        return response.json();
      })
      .then(function (productJson) {
        var fallbackDescription =
          productJson && (productJson.description || productJson.body_html || productJson.body || '');
        return appendDefaultLocaleSizeGuideSource(fallbackDescription);
      })
      .catch(function () {
        return false;
      });

    return defaultLocaleSizeGuideLoad;
  }

  function getCurrentVariantSelects() {
    return sectionId ? document.getElementById('variant-selects-' + sectionId) : null;
  }

  function getCurrentVariant() {
    if (!productData || !Array.isArray(productData.variants)) return null;

    var variantInput =
      (sizeGuideRoot && sizeGuideRoot.querySelector('form[action*="/cart/add"] input[name="id"]')) ||
      document.querySelector('form[action*="/cart/add"] input[name="id"], input[name="id"]');
    var selectedId = variantInput ? String(variantInput.value || '').trim() : '';
    if (!selectedId) return null;

    return (
      productData.variants.find(function (variant) {
        return String(variant && variant.id) === selectedId;
      }) || null
    );
  }

  function getCurrentSizeSelect() {
    return findSizeGuideSelect(sizeGuideRoot);
  }

  function scheduleGuideRender(delay) {
    if (scheduledGuideRender) window.clearTimeout(scheduledGuideRender);
    scheduledGuideRender = window.setTimeout(function () {
      scheduledGuideRender = null;
      renderGuide();
    }, typeof delay === 'number' ? delay : 0);
  }

  function getSelectedGuideTypeValue() {
    var optionContext = getCurrentOptionContext(getCurrentVariantSelects());
    var optionNames = Object.keys(optionContext);

    for (var index = 0; index < optionNames.length; index += 1) {
      if (isTypeLikeLabel(optionNames[index])) return optionContext[optionNames[index]];
    }

    return '';
  }

  function getStoredSizeGuideUnitSystem() {
    try {
      var stored = window.localStorage.getItem(UNIT_SYSTEM_STORAGE_KEY);
      return stored === 'imperial' || stored === 'metric' ? stored : null;
    } catch (_error) {
      return null;
    }
  }

  function storeSizeGuideUnitSystem(unitSystem) {
    try {
      window.localStorage.setItem(UNIT_SYSTEM_STORAGE_KEY, unitSystem);
    } catch (_error) {
      // localStorage may be blocked
    }
  }

  function getKnownSizeGuideLabels(select) {
    var labels = {};
    if (!select || !select.options) return labels;

    function addLabel(value) {
      var raw = String(value || '').replace(/[\u200e\u200f\u202a-\u202e]/g, '').trim();
      if (!raw) return;

      var normalized = normalizeText(raw);
      var compact = getCompactToken(raw);
      if (normalized) labels[normalized] = true;
      if (compact) labels[compact] = true;
    }

    Array.from(select.options).forEach(function (option) {
      if (!option || option.value === '') return;
      addLabel(option.value);
      addLabel(option.textContent);
      addLabel(option.getAttribute('data-display-label'));

      if (window.DLMSizeLabelFormatter && typeof window.DLMSizeLabelFormatter.formatSizeLabel === 'function') {
        addLabel(window.DLMSizeLabelFormatter.formatSizeLabel(option.value));
      }
    });

    return labels;
  }

  function lineMatchesKnownSizeLabel(line, knownLabels) {
    var raw = String(line || '').trim();
    if (!raw) return false;

    var normalized = normalizeText(raw);
    var compact = getCompactToken(raw);
    return !!(knownLabels[normalized] || knownLabels[compact]);
  }

  function isLikelyStandaloneSizeToken(value, knownLabels) {
    var raw = String(value || '').trim();
    if (!raw) return false;
    if (lineMatchesKnownSizeLabel(raw, knownLabels)) return true;
    if (/^(?:XXXXL|XXXL|XXL|[2-9]XL|XL|XS|S|M|L|س|م|ل)$/i.test(raw)) return true;
    if (/^\d{2,3}(?:\s*cm)?$/i.test(raw)) return true;
    if (/^\d{1,2}\s*[-–]\s*\d{1,2}(?:\s*(?:y|yr|yrs|year|years|ano|anos|año|años|an|ans|سن(?:ة|وات)|months?|mos?|mois|شهر(?:ا|ًا)?|أشهر))?$/i.test(raw)) return true;
    if (/^\d{1,2}(?:\s*(?:y|yr|yrs|year|years|ano|anos|año|años|an|ans|سن(?:ة|وات)|months?|mos?|mois|شهر(?:ا|ًا)?|أشهر))$/i.test(raw)) return true;
    if (/^\d{1,2}\s*m\/\d{2,3}$/i.test(raw)) return true;
    return false;
  }

  function isLikelySizeGuideRowLabel(line, knownLabels) {
    if (lineMatchesKnownSizeLabel(line, knownLabels)) return true;

    var parsedRole = parseRoleFromSizeLabel(line);
    if (parsedRole && isLikelyStandaloneSizeToken(parsedRole.sizeLabel, knownLabels)) return true;

    return isLikelyStandaloneSizeToken(line, knownLabels);
  }

  function isLikelyGuideSizeHeaderLine(line, knownLabels) {
    var raw = String(line || '').trim();
    if (!raw || !isSizeLikeLabel(raw)) return false;
    if (isLikelySizeGuideRowLabel(raw, knownLabels)) return false;
    if (hasGuideUnitToken(raw)) return false;
    return raw.length <= 24;
  }

  function isIgnorableGuideLine(line) {
    var raw = String(line || '').trim();
    if (!raw) return true;
    if (/^<\/?[^>]+>$/.test(raw)) return true;
    if (/^<!--.*-->$/.test(raw)) return true;
    return false;
  }

  function extractGuideLines(sourceRoot) {
    if (!sourceRoot) return [];

    return String(sourceRoot.textContent || '')
      .split(/\n+/)
      .map(function (line) {
        return String(line || '')
          .replace(/[\u200e\u200f\u202a-\u202e]/g, '')
          .replace(/\s+/g, ' ')
          .trim();
      })
      .filter(Boolean);
  }

  function collectGuideHeaders(lines, startIndex, knownLabels) {
    var headers = [];

    for (var index = startIndex; index < lines.length; index += 1) {
      var line = lines[index];
      if (isIgnorableGuideLine(line)) continue;
      if (headers.length && isLikelySizeGuideRowLabel(line, knownLabels)) break;
      if (
        headers.length > 1 &&
        isSizeLikeLabel(line) &&
        !hasGuideUnitToken(line) &&
        !isMeasurementLikeLabel(line) &&
        !isLikelySizeGuideRowLabel(line, knownLabels)
      ) {
        break;
      }
      headers.push(line);
    }

    return headers;
  }

  function collectGuideRows(lines, headerCount, knownLabels) {
    var rows = [];

    for (var index = 0; index < lines.length; index += 1) {
      var line = lines[index];
      if (isIgnorableGuideLine(line)) continue;
      if (!isLikelySizeGuideRowLabel(line, knownLabels)) continue;

      var row = [line];

      while (index + 1 < lines.length && row.length < headerCount) {
        var nextLine = lines[index + 1];
        index += 1;

        if (isIgnorableGuideLine(nextLine)) continue;
        if (isSizeLikeLabel(nextLine) && !isLikelySizeGuideRowLabel(nextLine, knownLabels)) continue;
        if (row.length > 1 && isLikelySizeGuideRowLabel(nextLine, knownLabels)) {
          index -= 1;
          break;
        }

        row.push(nextLine);
      }

      if (row.length === headerCount) rows.push(row);
    }

    return rows;
  }

  function buildFallbackSizeGuideTable(sourceRoot, headers, rows) {
    var existing = sourceRoot.querySelector('table[data-size-guide-reconstructed="true"]');
    if (existing) return existing;

    var originalTable = sourceRoot.querySelector('table#size-chart, table[id*="size-chart"]');
    if (originalTable) {
      originalTable.hidden = true;
      originalTable.setAttribute('aria-hidden', 'true');
      originalTable.setAttribute('data-size-guide-original-source', 'true');
      originalTable.style.display = 'none';
      originalTable.removeAttribute('id');
    }

    var table = document.createElement('table');
    table.id = 'size-chart';
    table.className = 'size-chart';
    table.setAttribute('data-size-guide-reconstructed', 'true');
    table.setAttribute('aria-hidden', 'true');
    table.style.display = 'none';

    var thead = document.createElement('thead');
    var headRow = document.createElement('tr');
    headers.forEach(function (header) {
      var cell = document.createElement('th');
      cell.textContent = header;
      headRow.appendChild(cell);
    });
    thead.appendChild(headRow);
    table.appendChild(thead);

    var tbody = document.createElement('tbody');
    rows.forEach(function (row) {
      var bodyRow = document.createElement('tr');
      row.forEach(function (value) {
        var cell = document.createElement('td');
        cell.textContent = value;
        bodyRow.appendChild(cell);
      });
      tbody.appendChild(bodyRow);
    });
    table.appendChild(tbody);
    sourceRoot.appendChild(table);

    return table;
  }

  function getImageBasedSizeGuidePreset(sourceRoot) {
    if (!sourceRoot) return null;

    var imageUrls = Array.from(sourceRoot.querySelectorAll('img[src]'))
      .map(function (image) {
        return String(image.getAttribute('src') || image.currentSrc || '').toLowerCase();
      })
      .filter(Boolean);

    if (!imageUrls.length) return null;

    for (var presetIndex = 0; presetIndex < IMAGE_BASED_SIZE_GUIDE_PRESETS.length; presetIndex += 1) {
      var preset = IMAGE_BASED_SIZE_GUIDE_PRESETS[presetIndex];
      var hasEveryImage = preset.imageTokens.every(function (token) {
        return imageUrls.some(function (imageUrl) {
          return imageUrl.indexOf(token) !== -1;
        });
      });

      if (hasEveryImage) return preset;
    }

    return null;
  }

  function getImageBasedSizeGuideMediaTarget(image, sourceRoot) {
    if (!image || !sourceRoot) return null;

    var mediaContainer = image.closest('.product-copy__media');
    if (mediaContainer && sourceRoot.contains(mediaContainer)) return mediaContainer;

    var figure = image.closest('figure');
    if (figure && sourceRoot.contains(figure)) return figure;

    var parent = image.parentElement;
    if (
      parent &&
      parent !== sourceRoot &&
      /^(P|DIV|A)$/.test(parent.tagName) &&
      parent.querySelectorAll('img').length === 1 &&
      !normalizeText(parent.textContent || '')
    ) {
      return parent;
    }

    return image;
  }

  function getTableBasedSizeGuideTarget(table, sourceRoot) {
    if (!table || !sourceRoot) return null;

    var tableCard = table.closest('.product-copy__table-card');
    if (tableCard && sourceRoot.contains(tableCard)) return tableCard;

    var section = table.closest('section');
    if (section && section !== sourceRoot && sourceRoot.contains(section)) return section;

    var parent = table.parentElement;
    if (
      parent &&
      parent !== sourceRoot &&
      /^(DIV|P)$/.test(parent.tagName) &&
      parent.querySelectorAll('table').length === 1
    ) {
      return parent;
    }

    return table;
  }

  function hideSizeGuideSourceTarget(target, attributeName) {
    if (!target) return;

    target.hidden = true;
    target.setAttribute('aria-hidden', 'true');
    target.setAttribute(attributeName, 'true');
    target.style.setProperty('display', 'none', 'important');
  }

  function hideImageBasedSizeGuideMedia(sourceRoot, preset) {
    if (!sourceRoot || !preset || !Array.isArray(preset.imageTokens) || !preset.imageTokens.length) return;

    Array.from(sourceRoot.querySelectorAll('img[src]')).forEach(function (image) {
      var imageUrl = String(image.getAttribute('src') || image.currentSrc || '').toLowerCase();
      if (!imageUrl) return;

      var isPresetImage = preset.imageTokens.some(function (token) {
        return imageUrl.indexOf(token) !== -1;
      });
      if (!isPresetImage) return;

      var target = getImageBasedSizeGuideMediaTarget(image, sourceRoot) || image;
      hideSizeGuideSourceTarget(target, 'data-size-guide-image-source-only');
    });
  }

  function hideTableBasedSizeGuideSources(sourceRoot) {
    if (!sourceRoot) return;

    var tables = Array.from(
      sourceRoot.querySelectorAll(
        'table#size-chart, table[id*="size-chart"], table.size-chart, table[data-size-chart-source-only="true"], table[data-size-guide-original-source="true"]'
      )
    );
    var hiddenTargets = [];

    tables.forEach(function (table) {
      if (table.getAttribute('data-size-guide-reconstructed') === 'true') return;

      var target = getTableBasedSizeGuideTarget(table, sourceRoot) || table;
      if (hiddenTargets.indexOf(target) !== -1) return;

      hiddenTargets.push(target);
      hideSizeGuideSourceTarget(target, 'data-size-guide-table-source-only');
    });
  }

  function hideRedundantSizeGuideSources(sourceRoot, preset) {
    if (!sourceRoot) return;

    hideTableBasedSizeGuideSources(sourceRoot);
    hideImageBasedSizeGuideMedia(sourceRoot, preset);
  }

  function getSizeGuideTableContextText(table) {
    if (!table) return '';

    var context = [];
    if (table.id) context.push(table.id);

    var previous = table.previousElementSibling;
    while (previous) {
      if (/^H[1-6]$/i.test(previous.tagName)) {
        context.push(cellText(previous));
        break;
      }
      if (/^TABLE$/i.test(previous.tagName)) break;
      previous = previous.previousElementSibling;
    }

    return normalizeText(context.join(' '));
  }

  function tableMatchesSelectedType(table, selectedTypeValue) {
    var normalizedType = normalizeText(selectedTypeValue);
    if (!normalizedType) return false;

    var context = getSizeGuideTableContextText(table);
    if (!context) return false;
    var selectedGarmentKey = getGarmentKey(selectedTypeValue);
    var contextGarmentKey = getGarmentKey(context);
    var idGarmentKey = getGarmentKey(table.id || '');

    if (selectedGarmentKey && idGarmentKey) {
      if (selectedGarmentKey === idGarmentKey) return true;
      if (
        ['shirt', 'shorts', 'shirtShortsSet'].indexOf(selectedGarmentKey) !== -1 &&
        ['shirt', 'shorts', 'shirtShortsSet'].indexOf(idGarmentKey) !== -1
      ) {
        return true;
      }
      return false;
    }

    if (selectedGarmentKey && contextContainsGarmentKey(context, selectedGarmentKey)) return true;

    if (selectedGarmentKey) {
      if (selectedGarmentKey === 'dress') {
        return contextGarmentKey === 'dress' || (!contextGarmentKey && normalizeText(table.id) === 'size chart');
      }

      if (['shirt', 'shorts', 'shirtShortsSet'].indexOf(selectedGarmentKey) !== -1) {
        return ['shirt', 'shorts', 'shirtShortsSet'].indexOf(contextGarmentKey) !== -1;
      }

      if (contextGarmentKey) return selectedGarmentKey === contextGarmentKey;
    }

    if (context.indexOf(normalizedType) !== -1) return true;

    return normalizedType
      .split(/\s+/)
      .filter(function (token) {
        return token && token.length > 3;
      })
      .some(function (token) {
        return context.indexOf(token) !== -1;
    });
  }

  function contextContainsGarmentKey(context, garmentKey) {
    var text = normalizeText(context);
    if (!text || !garmentKey) return false;
    if (garmentKey === 'dress') return /(dress|skirt|robe|vestido|vestito|kleid|jurk|kjole|sukienka|rochie|плать|فستان|שמלה|ワンピース|드레스|连衣裙|連衣裙|洋裝)/i.test(text);
    if (garmentKey === 'shirt') return /(shirt|tee|t-shirt|camisa|chemise|hemd|skjorte|koszula|cămașă|camicie|рубаш|قميص|חולצה|シャツ|셔츠|衬衫|襯衫)/i.test(text);
    if (garmentKey === 'shorts') return /(short|shorts|trunk|bermuda|шорт|شورت|מכנסיים קצרים|ショーツ|반바지|短裤|短褲)/i.test(text);
    if (garmentKey === 'shirtShortsSet') return contextContainsGarmentKey(text, 'shirt') && contextContainsGarmentKey(text, 'shorts');
    if (garmentKey === 'romper') return /(romper|pelele|barboteuse|strampler|pagliaccetto|rampers|אוברול|ロンパース|롬퍼|连体衣|連身衣|baby|bebé|bebe|bébé|الرضيع|بيبي)/i.test(text);
    if (garmentKey === 'pants') return /(pant|pants|trouser|pantal|hose|broek|bukse|spodnie|брюк|بنطال|מכנסיים|パンツ|바지|长裤|長褲)/i.test(text);
    if (garmentKey === 'top') return /(top|haut|topp|yläosa|上衣|トップス|상의|טופ|توب)/i.test(text);
    return false;
  }

  function getSelectedRoleKeyForTableSelection(select, selectedTypeValue) {
    var currentVariant = getCurrentVariant();
    var sizeOptionIndex = productData && Array.isArray(productData.options) ? findSizeOptionIndex(productData.options) : -1;
    if (currentVariant && sizeOptionIndex > -1) {
      var variantRole = getRoleInfoForVariant(currentVariant, productData.options, sizeOptionIndex);
      if (variantRole && variantRole.key) return variantRole.key;
    }

    var rawValue = select ? String(select.value || '').trim() : '';
    var rawText = select && select.selectedOptions && select.selectedOptions[0]
      ? String(select.selectedOptions[0].textContent || '').trim()
      : rawValue;
    var parsedRole = parseRoleFromSizeLabel(rawValue) || parseRoleFromSizeLabel(rawText);
    var baseRoleKey = parsedRole && parsedRole.key ? parsedRole.key : '';
    var typeRoleKey = inferRoleKeyFromType(selectedTypeValue, baseRoleKey);
    return typeRoleKey || baseRoleKey;
  }

  function tableHasCompatibleSelectedRole(table, selectedRoleKey) {
    if (!table || !selectedRoleKey) return false;

    var firstCells = Array.from(table.querySelectorAll('tr')).map(function (row) {
      var firstCell = row.querySelector('th, td');
      return firstCell ? cellText(firstCell) : '';
    });

    if (firstCells.some(function (value) {
      var parsedRole = parseRoleFromSizeLabel(value);
      return parsedRole && areSizeGuideRolesCompatible(selectedRoleKey, parsedRole.key);
    })) {
      return true;
    }

    return Array.from(table.querySelectorAll('tr:first-child th, tr:first-child td')).some(function (cell) {
      var roleHeader = parseRoleFromHeader(cellText(cell));
      return roleHeader && areSizeGuideRolesCompatible(selectedRoleKey, roleHeader.key);
    });
  }

  function getSizeGuideTable(root, select, selectedTypeValue) {
    var descriptionRoot = (root && root.querySelector('[data-product-description]')) || document.querySelector('[data-product-description]');
    var existingTables = descriptionRoot
      ? Array.from(descriptionRoot.querySelectorAll('table#size-chart, table[id*="size-chart"]'))
      : [];
    var fallbackGuide = null;
    var imagePresetGuide = descriptionRoot ? getImageBasedSizeGuidePreset(descriptionRoot) : null;

    if (existingTables.length > 1) {
      var selectedRoleKey = getSelectedRoleKeyForTableSelection(select, selectedTypeValue);
      return (
        existingTables.find(function (table) {
          return tableMatchesSelectedType(table, selectedTypeValue);
        }) ||
        existingTables.find(function (table) {
          return tableHasCompatibleSelectedRole(table, selectedRoleKey);
        }) ||
        existingTables[0]
      );
    }

    var existingTable = existingTables[0] || document.querySelector('table#size-chart, table[id*="size-chart"]');

    if (descriptionRoot) {
      var lines = extractGuideLines(descriptionRoot);
      var knownLabels = getKnownSizeGuideLabels(select);

      for (var index = 0; index < lines.length; index += 1) {
        var line = lines[index];
        if (!isLikelyGuideSizeHeaderLine(line, knownLabels)) continue;

        var headers = collectGuideHeaders(lines, index, knownLabels);
        if (headers.length < 2) continue;
        if (!headers.slice(1).some(function (headerLine) {
          return hasGuideUnitToken(headerLine) || isMeasurementLikeLabel(headerLine);
        })) {
          continue;
        }

        var rows = collectGuideRows(lines.slice(index + headers.length), headers.length, knownLabels);
        if (!rows.length) continue;

        fallbackGuide = {
          headers: headers,
          rows: rows,
        };
        break;
      }
    }

    var preferredGuide = fallbackGuide;
    if (imagePresetGuide && (!preferredGuide || imagePresetGuide.rows.length > preferredGuide.rows.length)) {
      preferredGuide = imagePresetGuide;
    }

    if (!existingTable) {
      return descriptionRoot && preferredGuide ? buildFallbackSizeGuideTable(descriptionRoot, preferredGuide.headers, preferredGuide.rows) : null;
    }

    if (!preferredGuide) return existingTable;

    var existingParsed = parseSizeGuideTable(existingTable);
    var shouldUseFallbackGuide =
      !existingParsed ||
      (preferredGuide &&
        existingParsed.headers &&
        existingParsed.headers.length <= 2 &&
        preferredGuide.headers &&
        preferredGuide.headers.length > existingParsed.headers.length &&
        preferredGuide.rows.length > existingParsed.rows.length);
    if (shouldUseFallbackGuide) {
      return descriptionRoot ? buildFallbackSizeGuideTable(descriptionRoot, preferredGuide.headers, preferredGuide.rows) : existingTable;
    }

    return existingTable;
  }

  function findSizeGuideSelect(root) {
    var selects = Array.from(root.querySelectorAll("select[name^='options[']"));
    for (var index = 0; index < selects.length; index += 1) {
      var name = String(selects[index].name || '');
      var optionMatch = name.match(/^options\[(.+)\]$/);
      var optionName = optionMatch && optionMatch[1] ? optionMatch[1] : name;
      if (isSizeLikeLabel(optionName)) return selects[index];
    }

    return root.querySelector("select[data-size-option='true'], select.size-select");
  }

  function parseGuideHeader(headerText) {
    var raw = String(headerText || '').trim();
    var match = raw.match(/\(([^)]+)\)\s*$/);
    var units = [];
    var label = raw;

    if (match) {
      label = raw.slice(0, match.index).trim();
      units = match[1]
        .split('/')
        .map(function (unit) {
          return String(unit || '').trim();
        })
        .filter(Boolean);
    }

    return {
      raw: raw,
      label: label || raw,
      units: units,
    };
  }

  function pickPreferredGuideUnitIndex(units, unitSystem) {
    var normalizedUnits = (units || []).map(normalizeGuideUnit);
    var preferredTokens = unitSystem === 'imperial' ? ['in', 'lbs'] : ['cm', 'kg'];

    for (var index = 0; index < preferredTokens.length; index += 1) {
      var preferredIndex = normalizedUnits.indexOf(preferredTokens[index]);
      if (preferredIndex !== -1) return preferredIndex;
    }

    return unitSystem === 'imperial' ? Math.min(1, normalizedUnits.length - 1) : 0;
  }

  function formatGuideNumericValue(num) {
    if (num === null || typeof num === 'undefined' || Number.isNaN(num)) return '';
    return Number(num).toFixed(2).replace(/\.00$/, '').replace(/(\.\d)0$/, '$1');
  }

  function convertGuideValueBetweenUnits(num, fromUnit, toUnit) {
    var from = normalizeGuideUnit(fromUnit);
    var to = normalizeGuideUnit(toUnit);
    if (!from || !to || from === to) return num;
    if (from === 'cm' && to === 'in') return num / 2.54;
    if (from === 'in' && to === 'cm') return num * 2.54;
    if (from === 'kg' && to === 'lbs') return num * 2.20462;
    if (from === 'lbs' && to === 'kg') return num / 2.20462;
    return null;
  }

  function stripGuideTrailingUnit(value, unit) {
    var text = String(value || '').trim();
    var normalizedUnit = normalizeGuideUnit(unit);
    if (!normalizedUnit) return text;

    if (normalizedUnit === 'cm') return text.replace(/\s*(?:cm|cms|centimeter|centimeters|centimetre|centimetres)$/i, '').trim();
    if (normalizedUnit === 'in') return text.replace(/\s*(?:in|inch|inches)$/i, '').trim();
    if (normalizedUnit === 'kg') return text.replace(/\s*(?:kg|kgs|kilogram|kilograms)$/i, '').trim();
    if (normalizedUnit === 'lbs') return text.replace(/\s*(?:lb|lbs)$/i, '').trim();

    return text;
  }

  function getGuideTargetUnit(sourceUnit, unitSystem) {
    var normalizedSource = normalizeGuideUnit(sourceUnit);
    if (!normalizedSource) return '';

    if (unitSystem === 'imperial') {
      if (normalizedSource === 'cm') return 'in';
      if (normalizedSource === 'kg') return 'lbs';
    }

    if (unitSystem === 'metric') {
      if (normalizedSource === 'in') return 'cm';
      if (normalizedSource === 'lbs') return 'kg';
    }

    return normalizedSource;
  }

  function convertGuideCellText(text, fromUnit, toUnit) {
    var cleaned = stripGuideTrailingUnit(text, fromUnit);
    var normalizedFrom = normalizeGuideUnit(fromUnit);
    var normalizedTo = normalizeGuideUnit(toUnit);

    if (!cleaned) return '';
    if (!normalizedFrom || !normalizedTo || normalizedFrom === normalizedTo) return cleaned;

    var singleMatch = cleaned.match(/^(-?\d+(?:\.\d+)?)$/);
    if (singleMatch) {
      var convertedSingle = convertGuideValueBetweenUnits(parseFloat(singleMatch[1]), normalizedFrom, normalizedTo);
      return convertedSingle === null ? null : formatGuideNumericValue(convertedSingle);
    }

    var rangeMatch = cleaned.match(/^(-?\d+(?:\.\d+)?)\s*([\-–])\s*(-?\d+(?:\.\d+)?)$/);
    if (rangeMatch) {
      var convertedMin = convertGuideValueBetweenUnits(parseFloat(rangeMatch[1]), normalizedFrom, normalizedTo);
      var convertedMax = convertGuideValueBetweenUnits(parseFloat(rangeMatch[3]), normalizedFrom, normalizedTo);
      if (convertedMin === null || convertedMax === null) return null;
      return formatGuideNumericValue(convertedMin) + rangeMatch[2] + formatGuideNumericValue(convertedMax);
    }

    return null;
  }

  function formatGuideHeaderLabel(header, unitSystem) {
    if (!header || !header.units || !header.units.length) return header ? header.label : '';

    var units = header.units.map(normalizeGuideUnit);
    var unitIndex = unitSystem === 'imperial' ? Math.min(1, units.length - 1) : 0;
    var activeUnit = units[unitIndex] || units[0];
    return header.label + ' (' + activeUnit + ')';
  }

  function formatGuideCellValue(value, header, unitSystem) {
    var text = String(value || '').replace(/\s+/g, ' ').trim();
    if (!text || text === '—') return '—';
    var parts = splitGuideMeasurementParts(text);
    var units = header && header.units ? header.units.map(normalizeGuideUnit).filter(Boolean) : [];

    if (!units.length) {
      var inferredUnits = parts.map(inferGuideUnitFromText);
      if (parts.length >= 2 && inferredUnits.filter(Boolean).length >= 2) {
        var inferredIndex = pickPreferredGuideUnitIndex(inferredUnits, unitSystem);
        var inferredUnit = inferredUnits[inferredIndex] || inferredUnits[0] || '';
        return stripGuideTrailingUnit(parts[inferredIndex] || parts[0] || text, inferredUnit);
      }

      var inferredSourceUnit = inferGuideUnitFromText(text);
      var inferredTargetUnit = getGuideTargetUnit(inferredSourceUnit, unitSystem);
      var inferredConvertedText = convertGuideCellText(text, inferredSourceUnit, inferredTargetUnit);
      if (inferredConvertedText !== null && inferredConvertedText !== '') return inferredConvertedText;
      return stripGuideTrailingUnit(text, inferredTargetUnit || inferredSourceUnit);
    }

    if (units.length >= 2 && parts.length >= 2) {
      var valueIndex = pickPreferredGuideUnitIndex(units, unitSystem);
      var activeUnit = units[valueIndex] || units[0] || '';
      return stripGuideTrailingUnit(parts[valueIndex] || parts[0] || text, activeUnit);
    }

    var sourceUnit = units[0] || '';
    var targetUnit = getGuideTargetUnit(sourceUnit, unitSystem);
    var convertedText = convertGuideCellText(text, sourceUnit, targetUnit);
    if (convertedText !== null && convertedText !== '') return convertedText;

    return stripGuideTrailingUnit(text, targetUnit || sourceUnit);
  }

  function getSelectedSizeState() {
    var currentSizeSelect = getCurrentSizeSelect();
    if (!currentSizeSelect) return null;

    var rawValue = String(currentSizeSelect.value || '').trim();
    var rawText = currentSizeSelect.selectedOptions && currentSizeSelect.selectedOptions[0]
      ? String(currentSizeSelect.selectedOptions[0].textContent || '').trim()
      : rawValue;

    if (!rawValue && !rawText) return null;

    var formatter = formatGuideSizeLabel;
    var displayValue = rawText || rawValue;
    var exactDisplayValue = formatter ? formatter(rawValue) : '';
    if (exactDisplayValue && exactDisplayValue !== rawValue) displayValue = exactDisplayValue;
    var parsedRawValue = parseRoleFromSizeLabel(rawValue);
    var parsedRawText = parseRoleFromSizeLabel(rawText);
    var parsedDisplayValue = parseRoleFromSizeLabel(displayValue);
    var comparableValues = [rawValue, rawText, displayValue];
    if (parsedRawValue && parsedRawValue.sizeLabel) comparableValues.push(parsedRawValue.sizeLabel);
    if (parsedRawText && parsedRawText.sizeLabel) comparableValues.push(parsedRawText.sizeLabel);
    if (parsedDisplayValue && parsedDisplayValue.sizeLabel) comparableValues.push(parsedDisplayValue.sizeLabel);
    var variantRole = null;
    var currentVariant = getCurrentVariant();
    var sizeOptionIndex = productData && Array.isArray(productData.options) ? findSizeOptionIndex(productData.options) : -1;
    if (currentVariant && sizeOptionIndex > -1) {
      variantRole = getRoleInfoForVariant(currentVariant, productData.options, sizeOptionIndex);
      var variantSizeValue = getOptionValue(currentVariant, sizeOptionIndex);
      if (variantSizeValue) comparableValues.push(variantSizeValue);
      if (variantRole && variantRole.fullLabel) comparableValues.push(variantRole.fullLabel);
      if (variantRole && variantRole.sizeLabel) comparableValues.push(variantRole.sizeLabel);
    }
    var selectedRole = variantRole || parsedRawValue || parsedRawText || parsedDisplayValue || null;
    var selectedRoleKey = selectedRole && selectedRole.key ? selectedRole.key : '';
    var selectedRoleLabel = selectedRole && selectedRole.label ? selectedRole.label : '';
    var baseRoleKeyForType = selectedRoleKey;
    if (!baseRoleKeyForType) {
      var comparableForRole = getPrimaryComparableSize(comparableValues);
      if (comparableForRole && comparableForRole.adultToken) {
        baseRoleKeyForType = 'adult';
      } else if (comparableForRole) {
        baseRoleKeyForType = 'child';
      }
    }
    var selectedTypeRoleKey = inferRoleKeyFromType(getSelectedGuideTypeValue(), baseRoleKeyForType);

    if (
      selectedTypeRoleKey &&
      (!selectedRoleKey ||
        selectedRoleKey === 'child' ||
        selectedRoleKey === 'adult' ||
        (selectedRoleKey === 'boy' && selectedTypeRoleKey === 'girl') ||
        (selectedRoleKey === 'girl' && selectedTypeRoleKey === 'boy'))
    ) {
      selectedRoleKey = selectedTypeRoleKey;
      selectedRoleLabel = getLocalizedRoleLabelByKey(selectedTypeRoleKey);
    }

    return {
      rawValue: rawValue,
      rawText: rawText,
      displayValue: displayValue,
      roleKey: selectedRoleKey,
      roleLabel: selectedRoleLabel,
      sizeLabel: selectedRole && selectedRole.sizeLabel ? selectedRole.sizeLabel : '',
      tokens: buildSizeMatchTokens(comparableValues),
      comparableValues: comparableValues,
      comparable: getPrimaryComparableSize(comparableValues),
    };
  }

  function buildSizeMatchTokens(values) {
    var tokens = {};

    function addToken(value) {
      var raw = normalizeLocalizedSizeValue(value);
      if (!raw) return;

      var normalized = normalizeText(raw);
      var compact = getCompactToken(raw);
      if (normalized) tokens[normalized] = true;
      if (compact) tokens[compact] = true;

      var numericCmMatch = compact.match(/^(\d{2,3})cm$/);
      if (numericCmMatch) {
        tokens[numericCmMatch[1]] = true;
        tokens[numericCmMatch[1] + 'cm'] = true;
      }

      var numericMatch = compact.match(/^(\d{2,3})$/);
      if (numericMatch) {
        tokens[numericMatch[1]] = true;
        tokens[numericMatch[1] + 'cm'] = true;
      }

      var numericSequence = normalized.match(/\d+(?:[.,]\d+)?/g);
      if (numericSequence && numericSequence.length) {
        var canonicalSequence = numericSequence
          .map(function (segment) {
            return String(segment || '').replace(',', '.').replace(/\.0+$/, '');
          })
          .join('-');
        if (canonicalSequence) tokens['n:' + canonicalSequence] = true;
      }

      var adultMatch = raw.toUpperCase().match(/\b(XXXXL|XXXL|XXL|2XL|3XL|4XL|XL|XS|S|M|L)\b/);
      if (adultMatch) {
        var adultToken = adultMatch[1];
        if (adultToken === 'XXL') adultToken = '2XL';
        if (adultToken === 'XXXL') adultToken = '3XL';
        if (adultToken === 'XXXXL') adultToken = '4XL';
        tokens[adultToken.toLowerCase()] = true;
      }

      if (normalized === 'س') tokens.s = true;
      if (normalized === 'م') tokens.m = true;
      if (normalized === 'ل') tokens.l = true;
      if (/^(?:小|小号|小號)$/.test(normalized)) tokens.s = true;
      if (/^(?:中|中号|中號)$/.test(normalized)) tokens.m = true;
      if (/^(?:大|長|长|大号|大號)$/.test(normalized)) tokens.l = true;

      var comparable = parseComparableSize(raw);
      if (comparable) {
        if (comparable.adultToken) tokens['adult:' + comparable.adultToken] = true;
        if (comparable.monthToken) tokens['month:' + comparable.monthToken] = true;
        if (comparable.toddlerToken) tokens['toddler:' + comparable.toddlerToken] = true;
        if (comparable.ageMax !== null) tokens['age-max:' + comparable.ageMax] = true;
        if (comparable.ageMin !== null && comparable.ageMax !== null) {
          tokens['age-range:' + comparable.ageMin + '-' + comparable.ageMax] = true;
        }
        if (comparable.heightMax !== null) tokens['height-max:' + comparable.heightMax] = true;
        if (comparable.heightMin !== null && comparable.heightMax !== null) {
          tokens['height-range:' + comparable.heightMin + '-' + comparable.heightMax] = true;
        }
      }

      var formatted = formatGuideSizeLabel(raw);
      if (formatted && formatted !== raw) {
        var formattedNormalized = normalizeText(formatted);
        var formattedCompact = getCompactToken(formatted);
        if (formattedNormalized) tokens[formattedNormalized] = true;
        if (formattedCompact) tokens[formattedCompact] = true;
      }
    }

    values.forEach(addToken);
    return tokens;
  }

  function extractComparableAdultToken(value) {
    var match = String(value || '').toUpperCase().match(/\b(XXXXL|XXXL|XXL|2XL|3XL|4XL|XL|XS|S|M|L)\b/);
    if (!match) return '';
    if (match[1] === 'XXL') return '2xl';
    if (match[1] === 'XXXL') return '3xl';
    if (match[1] === 'XXXXL') return '4xl';
    return match[1].toLowerCase();
  }

  function getAdultSizeRank(token) {
    var ranks = {
      xs: 1,
      s: 2,
      m: 3,
      l: 4,
      xl: 5,
      '2xl': 6,
      '3xl': 7,
      '4xl': 8,
    };
    return Object.prototype.hasOwnProperty.call(ranks, token) ? ranks[token] : null;
  }

  function hasComparableSizeData(comparable) {
    return !!(
      comparable &&
      (comparable.adultToken ||
        comparable.monthToken ||
        comparable.toddlerToken ||
        comparable.ageMin !== null ||
        comparable.ageMax !== null ||
        comparable.heightMin !== null ||
        comparable.heightMax !== null)
    );
  }

  function parseComparableSize(value) {
    var raw = normalizeLocalizedSizeValue(value);
    if (!raw) return null;

    var roleSize = parseRoleFromSizeLabel(raw);
    var comparableRaw = normalizeLocalizedSizeValue(roleSize && roleSize.sizeLabel ? roleSize.sizeLabel : raw)
      .replace(/[–—]/g, '-')
      .trim();
    if (!comparableRaw) return null;

    var comparable = {
      adultToken: extractComparableAdultToken(comparableRaw),
      monthToken: '',
      toddlerToken: '',
      ageMin: null,
      ageMax: null,
      heightMin: null,
      heightMax: null,
    };

    var ageRangeMatch = comparableRaw.match(/(\d{1,2})\s*-\s*(\d{1,2})\s*(?:t|y|yr|yrs|year|years|歳|才|岁|歲|세|년)\b/i);
    if (ageRangeMatch) {
      comparable.ageMin = parseInt(ageRangeMatch[1], 10);
      comparable.ageMax = parseInt(ageRangeMatch[2], 10);
      comparable.toddlerToken = String(comparable.ageMax) + 't';
    }

    var monthMatch = comparableRaw.match(/(?:^|[^0-9])(\d{1,2})\s*m(?:onths?)?(?:\/|\b|$)/i);
    if (monthMatch) {
      var monthValue = parseInt(monthMatch[1], 10);
      if (!isNaN(monthValue)) {
        comparable.monthToken = String(monthValue) + 'm';
        if (monthValue % 12 === 0) {
          var monthYears = monthValue / 12;
          if (comparable.ageMax === null) comparable.ageMax = monthYears;
          if (comparable.ageMin === null) comparable.ageMin = monthYears > 1 ? monthYears - 1 : monthYears;
          if (!comparable.toddlerToken) comparable.toddlerToken = String(monthYears) + 't';
        }
      }
    }

    var localizedSingleAgeMatch = comparableRaw.match(/(?:^|[^0-9])(\d{1,2})\s*(?:歳|才|岁|歲|세|년)(?:\b|$)/i);
    if (localizedSingleAgeMatch) {
      var localizedAgeValue = parseInt(localizedSingleAgeMatch[1], 10);
      if (!isNaN(localizedAgeValue)) {
        if (comparable.ageMax === null) comparable.ageMax = localizedAgeValue;
        if (comparable.ageMin === null) comparable.ageMin = localizedAgeValue;
        if (!comparable.toddlerToken) comparable.toddlerToken = String(localizedAgeValue) + 't';
      }
    }

    var toddlerMatch = comparableRaw.match(/(?:^|[^0-9])(\d{1,2})\s*t(?:\/|\b|$)/i);
    if (toddlerMatch) {
      var toddlerValue = parseInt(toddlerMatch[1], 10);
      if (!isNaN(toddlerValue)) {
        comparable.toddlerToken = String(toddlerValue) + 't';
        if (comparable.ageMax === null) comparable.ageMax = toddlerValue;
        if (comparable.ageMin === null) comparable.ageMin = toddlerValue > 1 ? toddlerValue - 1 : toddlerValue;
      }
    }

    var heightRangeMatch = comparableRaw.match(/(?:^|[^0-9])(\d{2,3})\s*-\s*(\d{2,3})(?:\s*cm)?(?:\b|$)/i);
    if (heightRangeMatch) {
      comparable.heightMin = parseInt(heightRangeMatch[1], 10);
      comparable.heightMax = parseInt(heightRangeMatch[2], 10);
    }

    var slashHeightMatch = comparableRaw.match(/\/\s*(\d{2,3})(?:\s*cm)?$/i);
    if (slashHeightMatch && comparable.heightMax === null) {
      comparable.heightMin = parseInt(slashHeightMatch[1], 10);
      comparable.heightMax = comparable.heightMin;
    }

    var standaloneHeightMatch = comparableRaw.match(/(?:^|[^0-9])(\d{2,3})(?:\s*cm)?(?:\b|$)/i);
    if (standaloneHeightMatch && comparable.heightMax === null) {
      var standaloneHeight = parseInt(standaloneHeightMatch[1], 10);
      if (!isNaN(standaloneHeight) && standaloneHeight >= 80) {
        comparable.heightMin = standaloneHeight;
        comparable.heightMax = standaloneHeight;
      }
    }

    return hasComparableSizeData(comparable) ? comparable : null;
  }

  function getPrimaryComparableSize(values) {
    if (!values || !values.length) return null;

    for (var index = 0; index < values.length; index += 1) {
      var comparable = parseComparableSize(values[index]);
      if (hasComparableSizeData(comparable)) return comparable;
    }

    return null;
  }

  function getGuideRowValues(rowLabel) {
    var rowValues = [rowLabel];
    var parsedRow = parseRoleFromSizeLabel(rowLabel);
    rowValues.push(formatGuideSizeLabel(rowLabel));
    if (parsedRow && parsedRow.sizeLabel) rowValues.push(parsedRow.sizeLabel);
    return rowValues;
  }

  function areSizeGuideRolesCompatible(selectedRoleKey, rowRoleKey) {
    if (!selectedRoleKey || !rowRoleKey || selectedRoleKey === rowRoleKey) return true;
    if (selectedRoleKey === 'child') return rowRoleKey === 'girl' || rowRoleKey === 'boy' || rowRoleKey === 'baby';
    if (selectedRoleKey === 'adult') return rowRoleKey === 'mother' || rowRoleKey === 'father';
    if (rowRoleKey === 'child') return selectedRoleKey === 'girl' || selectedRoleKey === 'boy' || selectedRoleKey === 'baby';
    if (rowRoleKey === 'adult') return selectedRoleKey === 'mother' || selectedRoleKey === 'father';
    return false;
  }

  function getGuideRowMatchScore(rowLabel, selectedState, rowRoleKey) {
    if (!selectedState || !selectedState.tokens) return -Infinity;
    if (!areSizeGuideRolesCompatible(selectedState.roleKey, rowRoleKey)) return -Infinity;

    var rowValues = getGuideRowValues(rowLabel);
    var rowTokens = buildSizeMatchTokens(rowValues);
    var sharedTokenCount = 0;

    Object.keys(rowTokens).forEach(function (token) {
      if (selectedState.tokens[token]) sharedTokenCount += 1;
    });

    var score = sharedTokenCount * 100;
    var selectedComparable = selectedState.comparable || getPrimaryComparableSize(selectedState.comparableValues || []);
    var rowComparable = getPrimaryComparableSize(rowValues);

    if (selectedComparable && rowComparable) {
      if (selectedComparable.adultToken && rowComparable.adultToken) {
        if (selectedComparable.adultToken === rowComparable.adultToken) {
          score += 140;
        } else {
          var selectedAdultRank = getAdultSizeRank(selectedComparable.adultToken);
          var rowAdultRank = getAdultSizeRank(rowComparable.adultToken);
          if (selectedAdultRank !== null && rowAdultRank !== null) {
            var adultRankDistance = Math.abs(selectedAdultRank - rowAdultRank);
            score += Math.max(10, 90 - adultRankDistance * 12);
          } else {
            score -= 140;
          }
        }
      }

      if (selectedComparable.monthToken && rowComparable.monthToken && selectedComparable.monthToken === rowComparable.monthToken) {
        score += 140;
      }

      if (selectedComparable.toddlerToken && rowComparable.toddlerToken) {
        var selectedToddlerValue = parseInt(selectedComparable.toddlerToken, 10);
        var rowToddlerValue = parseInt(rowComparable.toddlerToken, 10);

        if (selectedComparable.toddlerToken === rowComparable.toddlerToken) score += 140;
        if (!isNaN(selectedToddlerValue) && !isNaN(rowToddlerValue)) {
          score += Math.max(0, 60 - Math.abs(selectedToddlerValue - rowToddlerValue) * 20);
        }
      }

      if (
        selectedComparable.ageMin !== null &&
        selectedComparable.ageMax !== null &&
        rowComparable.ageMin !== null &&
        rowComparable.ageMax !== null
      ) {
        var overlapMin = Math.max(selectedComparable.ageMin, rowComparable.ageMin);
        var overlapMax = Math.min(selectedComparable.ageMax, rowComparable.ageMax);
        if (overlapMax >= overlapMin) {
          score += overlapMax > overlapMin ? 100 : 25;
        }
      }

      if (selectedComparable.ageMax !== null && rowComparable.ageMax !== null) {
        score += Math.max(0, 50 - Math.abs(selectedComparable.ageMax - rowComparable.ageMax) * 10);
      }

      if (selectedComparable.heightMax !== null && rowComparable.heightMax !== null) {
        score += Math.max(0, 40 - Math.abs(selectedComparable.heightMax - rowComparable.heightMax) * 0.5);
      }
    }

    return score > 0 ? score : -Infinity;
  }

  function getGuideRowEntries() {
    var entries = [];

    if (groups.length >= 1) {
      groups.forEach(function (group) {
        group.rows.forEach(function (row) {
          entries.push({
            roleKey: group.key,
            label: group.label || '',
            helper: group.helper || '',
            headers: group.headers,
            row: row,
          });
        });
      });
      return entries;
    }

    parsed.rows.forEach(function (row) {
      entries.push({
        roleKey: '',
        label: '',
        helper: '',
        headers: parsed.headers,
        row: row,
      });
    });

    return entries;
  }

  function getSelectedGuideRowEntry(selectedState) {
    if (!selectedState) return null;

    var entries = getGuideRowEntries();
    var bestEntry = null;
    var bestScore = -Infinity;

    entries.forEach(function (entry) {
      var score = getGuideRowMatchScore(entry.row[0], selectedState, entry.roleKey);
      if (score > bestScore) {
        bestScore = score;
        bestEntry = entry;
      }
    });

    return bestScore > -Infinity ? bestEntry : null;
  }

  function isSelectedGuideRow(entry, rowLabel, roleKey) {
    if (!entry || !entry.row) return false;
    if ((entry.roleKey || '') !== (roleKey || '')) return false;
    return normalizeText(String(entry.row[0] || '')) === normalizeText(String(rowLabel || ''));
  }

  function getSelectedGuideRowLabel(selectedState) {
    var matchingEntry = getSelectedGuideRowEntry(selectedState);
    return matchingEntry ? formatGuideSizeLabel(String(matchingEntry.row[0] || '').trim()) : '';
  }

  function formatGuideSizeLabel(value) {
    var raw = String(value || '').trim();
    if (!raw) return '';

    if (window.DLMSizeLabelFormatter && typeof window.DLMSizeLabelFormatter.formatSizeLabel === 'function') {
      return window.DLMSizeLabelFormatter.formatSizeLabel(raw);
    }

    var compact = raw.toLowerCase().replace(/\s+/g, '');
    var sizeMap = {
      '90': '1–2Y',
      '90cm': '1–2Y',
      '100': '2–3Y',
      '100cm': '2–3Y',
      '110': '3–4Y',
      '110cm': '3–4Y',
      '120': '5–6Y',
      '120cm': '5–6Y',
      '130': '6–7Y',
      '130cm': '6–7Y',
      '140': '8–9Y',
      '140cm': '8–9Y',
      '150': '10–11Y',
      '150cm': '10–11Y',
      '160': '12–13Y',
      '160cm': '12–13Y',
    };

    return sizeMap[compact] || raw;
  }

  function hasUnitToggle(headers) {
    return headers.some(function (header) {
      return header && header.units && header.units.length > 1;
    });
  }

  function renderGuideUnitToggle(headers) {
    if (!hasUnitToggle(headers)) return '';

    var toggleHtml = '<div class="matching-size-guide__unit-toggle" role="group" aria-label="' + escapeHtml(unitToggleLabel) + '">';
    toggleHtml += '<button type="button" class="matching-size-guide__unit-button' + (selectedUnitSystem === 'metric' ? ' is-active' : '') + '" data-size-guide-unit="metric" aria-pressed="' + (selectedUnitSystem === 'metric') + '">cm</button>';
    toggleHtml += '<button type="button" class="matching-size-guide__unit-button' + (selectedUnitSystem === 'imperial' ? ' is-active' : '') + '" data-size-guide-unit="imperial" aria-pressed="' + (selectedUnitSystem === 'imperial') + '">in</button>';
    toggleHtml += '</div>';
    return toggleHtml;
  }

  function getGuideHeadersForUnitToggle(groupList, fallbackHeaders) {
    var headerSets = [];

    if (Array.isArray(groupList) && groupList.length) {
      headerSets = groupList
        .map(function (group) {
          return group && group.headers ? group.headers : [];
        })
        .filter(function (headers) {
          return headers && headers.length;
        });
    }

    if (fallbackHeaders && fallbackHeaders.length) {
      headerSets.push(fallbackHeaders);
    }

    for (var index = 0; index < headerSets.length; index += 1) {
      if (hasUnitToggle(headerSets[index])) return headerSets[index];
    }

    return fallbackHeaders || [];
  }

  function renderGuideContentToolbar(headers, label) {
    if (!hasUnitToggle(headers)) return '';

    var toolbarHtml = '<div class="matching-size-guide__toolbar">';
    if (label) {
      toolbarHtml += '<div class="matching-size-guide__intro">';
      toolbarHtml += '<p class="matching-size-guide__eyebrow">' + escapeHtml(label) + '</p>';
      toolbarHtml += '</div>';
    }
    toolbarHtml += renderGuideUnitToggle(headers);
    toolbarHtml += '</div>';
    return toolbarHtml;
  }

  function getSelectedGuideMatch(selectedState) {
    var matchingEntry = getSelectedGuideRowEntry(selectedState);
    if (!matchingEntry) return null;

    return {
      label: matchingEntry.label || '',
      helper: matchingEntry.helper || '',
      headers: matchingEntry.headers,
      row: matchingEntry.row,
      roleKey: matchingEntry.roleKey || '',
    };
  }

  function formatSelectedGuideDisplay(match, selectedState) {
    var selectedGuideLabel = match && match.row ? formatGuideSizeLabel(String(match.row[0] || '').trim()) : '';
    var labelParts = [];

    if (match && match.label) labelParts.push(match.label);
    if (selectedGuideLabel) labelParts.push(selectedGuideLabel);

    if (labelParts.length) return labelParts.join(' ');
    return getSelectedGuideRowLabel(selectedState) || (selectedState && selectedState.displayValue ? selectedState.displayValue : '');
  }

  function renderSelectedGuideSnapshot(match, selectedState) {
    if (!match || !match.row || !match.headers || !match.headers.length) {
      snapshot.innerHTML = '';
      snapshot.setAttribute('hidden', 'hidden');
      return;
    }

    var measurementHtml = match.headers
      .map(function (header, headerIndex) {
        if (headerIndex === 0) return '';

        var value = formatGuideCellValue(match.row[headerIndex], header, selectedUnitSystem);
        if (isGuideEmptyValue(value)) return '';

        return (
          '<div class="matching-size-guide__metric">' +
          '<span class="matching-size-guide__metric-label">' + escapeHtml(formatGuideHeaderLabel(header, selectedUnitSystem)) + '</span>' +
          '<strong class="matching-size-guide__metric-value">' + escapeHtml(value) + '</strong>' +
          '</div>'
        );
      })
      .filter(Boolean)
      .join('');

    var selectedGuideDisplay = formatSelectedGuideDisplay(match, selectedState);
    // CRO Tier 1 (May 2026): the measurement grid is dense and dominates
    // the viewport before commitment. Collapse it by default and reveal
    // it on demand so the size-confirmation summary stays clean.
    var metricsId = 'matching-size-guide-metrics-' + Math.random().toString(36).slice(2, 9);
    var snapshotHtml = '<section class="matching-size-guide__snapshot-card matching-size-guide__snapshot-card--collapsible" data-matching-size-guide-snapshot-card aria-live="polite" aria-atomic="true">';
    snapshotHtml += '<div class="matching-size-guide__toolbar">';
    snapshotHtml += '<div class="matching-size-guide__intro">';
    snapshotHtml += '<p class="matching-size-guide__eyebrow">' + escapeHtml(snapshotLabel) + '</p>';
    snapshotHtml += '<p class="matching-size-guide__selected"><strong>' + escapeHtml(selectedGuideDisplay) + '</strong></p>';
    if (match.helper) {
      snapshotHtml += '<p class="matching-size-guide__helper matching-size-guide__helper--snapshot">' + escapeHtml(match.helper) + '</p>';
    }
    snapshotHtml += '</div>';
    snapshotHtml += renderGuideUnitToggle(match.headers);
    snapshotHtml += '</div>';

    if (measurementHtml) {
      snapshotHtml +=
        '<button type="button" class="matching-size-guide__metrics-toggle" data-matching-size-guide-metrics-toggle aria-expanded="false" aria-controls="' +
        metricsId +
        '">' +
        '<span class="matching-size-guide__metrics-toggle-label" data-matching-size-guide-metrics-toggle-label>Find your family\'s fit</span>' +
        '<span class="matching-size-guide__metrics-toggle-icon" aria-hidden="true"></span>' +
        '</button>';
      snapshotHtml +=
        '<div class="matching-size-guide__metrics matching-size-guide__metrics--collapsible" id="' +
        metricsId +
        '" data-matching-size-guide-metrics hidden>' +
        measurementHtml +
        '</div>';
    } else {
      snapshotHtml += '<p class="matching-size-guide__helper matching-size-guide__helper--snapshot">' + escapeHtml(compareHintLabel) + '</p>';
    }

    snapshotHtml += '</section>';
    snapshot.innerHTML = snapshotHtml;
    snapshot.removeAttribute('hidden');

    // Wire up the new measurements toggle. The button starts collapsed
    // (aria-expanded="false"), reveals the grid on first click, and
    // updates its label text/aria-expanded so it stays accessible.
    var toggle = snapshot.querySelector('[data-matching-size-guide-metrics-toggle]');
    var metricsPanel = snapshot.querySelector('[data-matching-size-guide-metrics]');
    var toggleLabel = snapshot.querySelector('[data-matching-size-guide-metrics-toggle-label]');
    if (toggle && metricsPanel) {
      toggle.addEventListener('click', function () {
        var nextExpanded = toggle.getAttribute('aria-expanded') !== 'true';
        toggle.setAttribute('aria-expanded', nextExpanded ? 'true' : 'false');
        if (nextExpanded) {
          metricsPanel.removeAttribute('hidden');
        } else {
          metricsPanel.setAttribute('hidden', 'hidden');
        }
        if (toggleLabel) {
          toggleLabel.textContent = nextExpanded ? 'Hide fit details' : 'Find your family\'s fit';
        }
      });
    }
  }

  var renderTableCard = function (headers, rows, title, helper, selectedEntry, roleKey) {
    return (
      '<article class="matching-size-guide__card">' +
      (title ? '<h3>' + escapeHtml(title) + '</h3>' : '') +
      (helper ? '<p class="matching-size-guide__helper">' + escapeHtml(helper) + '</p>' : '') +
      '<div class="matching-size-guide__table-wrap">' +
      '<table class="matching-size-guide__table">' +
      '<thead><tr>' +
      headers
        .map(function (header) {
          return '<th>' + escapeHtml(formatGuideHeaderLabel(header, selectedUnitSystem)) + '</th>';
        })
        .join('') +
      '</tr></thead>' +
      '<tbody>' +
      rows
        .map(function (row) {
          var isSelectedRow = isSelectedGuideRow(selectedEntry, row[0], roleKey);
          return (
            '<tr' + (isSelectedRow ? ' class="is-selected"' : '') + '>' +
            row
              .map(function (cell, cellIndex) {
                return '<td>' + escapeHtml(formatGuideCellValue(cell, headers[cellIndex], selectedUnitSystem)) + '</td>';
              })
              .join('') +
            '</tr>'
          );
        })
        .join('') +
      '</tbody>' +
      '</table>' +
      '</div>' +
      '</article>'
    );
  };

  function bindUnitToggleEvents() {
    sizeGuideRoot.querySelectorAll('[data-size-guide-unit]').forEach(function (button) {
      button.addEventListener('click', function () {
        var nextUnitSystem = button.getAttribute('data-size-guide-unit');
        if (nextUnitSystem !== 'metric' && nextUnitSystem !== 'imperial') return;
        if (nextUnitSystem === selectedUnitSystem) return;
        selectedUnitSystem = nextUnitSystem;
        storeSizeGuideUnitSystem(selectedUnitSystem);
        renderGuide();
      });
    });
  }

  function renderGuide() {
    descriptionRoot = getCurrentDescriptionRoot();
    imagePresetGuide = descriptionRoot ? getImageBasedSizeGuidePreset(descriptionRoot) : null;
    if (descriptionRoot) hideRedundantSizeGuideSources(descriptionRoot, imagePresetGuide);

    sizeTable = getSizeGuideTable(sizeGuideRoot, getCurrentSizeSelect(), getSelectedGuideTypeValue());
    if (!sizeTable) return;

    parsed = parseSizeGuideTable(sizeTable);
    if (!parsed) return;

    groups = buildSizeGuideGroups(parsed);

    var selectedState = getSelectedSizeState();
    var selectedMatch = getSelectedGuideMatch(selectedState);
    var guideSummaryLabel = groups.length > 1 ? groupedLabel : compareLabel;
    var guideHeadersForToggle = getGuideHeadersForUnitToggle(groups, parsed.headers);
    var guideToolbarHtml = selectedMatch ? '' : renderGuideContentToolbar(guideHeadersForToggle, guideSummaryLabel);

    renderSelectedGuideSnapshot(selectedMatch, selectedState);

    if (groups.length >= 1) {
      if (summary) summary.textContent = guideSummaryLabel;
      if (groups.length > 1) {
        content.innerHTML =
          guideToolbarHtml +
          '<div class="matching-size-guide__grid">' +
          groups
            .map(function (group) {
              return renderTableCard(group.headers, group.rows, group.label, group.helper, selectedMatch, group.key);
            })
            .join('') +
          '</div>';
      } else {
        content.innerHTML =
          guideToolbarHtml +
          renderTableCard(groups[0].headers, groups[0].rows, groups[0].label, groups[0].helper, selectedMatch, groups[0].key);
      }
    } else {
      if (summary) summary.textContent = compareLabel;
      content.innerHTML = guideToolbarHtml + renderTableCard(parsed.headers, parsed.rows, '', '', selectedMatch);
    }

    bindUnitToggleEvents();
    details.removeAttribute('hidden');
  }

  if (sizeTable && parsed) {
    renderGuide();
  } else {
    loadDefaultLocaleSizeGuideSource().then(function (loaded) {
      if (loaded) scheduleGuideRender(0);
    });
  }

  sizeGuideRoot.addEventListener('change', function (event) {
    var target = event && event.target;
    if (!target) return;

    var optionName = getOptionNameFromControl(target);
    if (!optionName || (!isSizeLikeLabel(optionName) && !isTypeLikeLabel(optionName))) return;

    scheduleGuideRender(ON_CHANGE_DEBOUNCE_TIMER + 25);
  });

  if (typeof subscribe === 'function' && typeof PUB_SUB_EVENTS !== 'undefined' && PUB_SUB_EVENTS.variantChange) {
    subscribe(PUB_SUB_EVENTS.variantChange, function (event) {
      if (!event || !event.data || String(event.data.sectionId || '') !== String(sectionId)) return;
      scheduleGuideRender(0);
    });
  }
}

function parseSizeGuideTable(table) {
  var rows = Array.from(table.querySelectorAll('tr'));
  if (rows.length < 2) return null;

  var headers = Array.from(rows[0].querySelectorAll('th, td')).map(function (cell) {
    return parseSizeGuideHeaderText(cellText(cell));
  });
  if (!headers.length) return null;

  var bodyRows = rows
    .slice(1)
    .map(function (row) {
      return Array.from(row.querySelectorAll('td')).map(function (cell) {
        return cellText(cell);
      });
    })
    .filter(function (cells) {
      return cells.length === headers.length;
    });

  if (!bodyRows.length) return null;
  headers = enrichSizeGuideHeaders(headers, bodyRows);

  return {
    headers: headers,
    rows: bodyRows,
  };
}

function parseSizeGuideHeaderText(headerText) {
  var raw = String(headerText || '').trim();
  var match = raw.match(/\(([^)]+)\)\s*$/);
  var units = [];
  var label = raw;

  if (match) {
    label = raw.slice(0, match.index).trim();
    units = match[1]
      .split('/')
      .map(function (unit) {
        return String(unit || '').trim();
      })
      .filter(Boolean);
  }

  return {
    raw: raw,
    label: label || raw,
    units: units,
  };
}

function normalizeGuideUnit(unit) {
  var token = normalizeText(unit);
  if (!token) return '';
  if (token === 'cms' || token === 'centimeter' || token === 'centimeters' || token === 'centimetre' || token === 'centimetres' || token === 'سم') return 'cm';
  if (token === 'inch' || token === 'inches' || token === 'بوصة' || token === 'بوصات' || token === 'انش' || token === 'إنش') return 'in';
  if (token === 'lb' || token === 'lbs') return 'lbs';
  if (token === 'kilogram' || token === 'kilograms' || token === 'كجم' || token === 'كغ') return 'kg';
  if (token === 'رطل' || token === 'ارطال' || token === 'أرطال') return 'lbs';
  return token;
}

function inferGuideUnitFromText(text) {
  var normalizedText = String(text || '').toLowerCase();
  var unitCandidates = [
    'cm',
    'cms',
    'centimeter',
    'centimeters',
    'centimetre',
    'centimetres',
    'سم',
    'in',
    'inch',
    'inches',
    'بوصة',
    'بوصات',
    'انش',
    'إنش',
    'kg',
    'kgs',
    'kilogram',
    'kilograms',
    'كجم',
    'كغ',
    'lb',
    'lbs',
    'رطل',
    'ارطال',
    'أرطال',
  ];

  for (var index = 0; index < unitCandidates.length; index += 1) {
    var token = unitCandidates[index];
    var escaped = token.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    var pattern = new RegExp('\\b' + escaped + '\\b', 'i');
    if (pattern.test(normalizedText)) return normalizeGuideUnit(token);
  }

  return '';
}

function splitGuideMeasurementParts(text) {
  return String(text || '')
    .split(/\s+\/\s+/)
    .map(function (part) {
      return String(part || '').trim();
    })
    .filter(Boolean);
}

function getGuideConvertibleUnits(unit) {
  var normalizedUnit = normalizeGuideUnit(unit);
  if (normalizedUnit === 'cm' || normalizedUnit === 'in') return ['cm', 'in'];
  if (normalizedUnit === 'kg' || normalizedUnit === 'lbs') return ['kg', 'lbs'];
  return [];
}

function mergeGuideUnitCandidates(targetUnits, candidateUnits) {
  (candidateUnits || []).forEach(function (unit) {
    if (unit && targetUnits.indexOf(unit) === -1) targetUnits.push(unit);
  });
}

function inferGuideUnitPairFromValues(columnValues) {
  var detectedUnits = [];

  (columnValues || []).forEach(function (value) {
    var parts = splitGuideMeasurementParts(value);

    if (parts.length) {
      parts.forEach(function (part) {
        mergeGuideUnitCandidates(detectedUnits, getGuideConvertibleUnits(inferGuideUnitFromText(part)));
      });
      return;
    }

    mergeGuideUnitCandidates(detectedUnits, getGuideConvertibleUnits(inferGuideUnitFromText(value)));
  });

  if (detectedUnits.indexOf('cm') !== -1 || detectedUnits.indexOf('in') !== -1) return ['cm', 'in'];
  if (detectedUnits.indexOf('kg') !== -1 || detectedUnits.indexOf('lbs') !== -1) return ['kg', 'lbs'];

  return [];
}

function inferGuideUnitPairFromLabel(labelText) {
  var normalizedLabel = normalizeText(labelText);
  if (!normalizedLabel) return [];
  if (normalizedLabel === 'size' || normalizedLabel === 'age' || normalizedLabel === '—') return [];

  if (normalizedLabel.indexOf('weight') !== -1) return ['kg', 'lbs'];

  var measurementTokens = [
    'height',
    'chest',
    'bust',
    'hip',
    'waist',
    'length',
    'sleeve',
    'shoulder',
    'pant',
    'short',
    'skirt',
    'garment',
  ];

  if (measurementTokens.some(function (token) {
    return normalizedLabel.indexOf(token) !== -1;
  })) {
    return ['cm', 'in'];
  }

  return [];
}

function inferGuideHeaderUnits(header, columnValues) {
  if (!header) return header;

  var normalizedUnits = (header.units || []).map(normalizeGuideUnit).filter(Boolean);
  if (normalizedUnits.length >= 2) return header;

  var inferredUnits = [];
  normalizedUnits.forEach(function (unit) {
    mergeGuideUnitCandidates(inferredUnits, getGuideConvertibleUnits(unit));
  });

  if (!inferredUnits.length) {
    mergeGuideUnitCandidates(inferredUnits, inferGuideUnitPairFromValues(columnValues));
  }

  if (!inferredUnits.length) {
    mergeGuideUnitCandidates(inferredUnits, inferGuideUnitPairFromLabel(header.label || header.raw || ''));
  }

  if (!inferredUnits.length) return header;

  return {
    raw: header.raw,
    label: header.label,
    units: inferredUnits,
  };
}

function enrichSizeGuideHeaders(headers, rows) {
  return (headers || []).map(function (header, index) {
    var columnValues = (rows || [])
      .map(function (row) {
        return row[index];
      })
      .filter(function (value) {
        return !isGuideEmptyValue(value);
      });

    return inferGuideHeaderUnits(header, columnValues);
  });
}

function cellText(cell) {
  return String(cell && cell.textContent ? cell.textContent : '')
    .replace(/\s+/g, ' ')
    .trim();
}

function isGuideEmptyValue(value) {
  var text = String(value || '')
    .replace(/\s+/g, ' ')
    .trim();

  return !text || text === '—' || text === '-' || text === '--' || /^n\/a$/i.test(text);
}

function pruneGuideGroupColumns(headers, rows) {
  if (!headers || !headers.length || !rows || !rows.length) {
    return {
      headers: headers || [],
      rows: rows || [],
    };
  }

  var keepIndexes = headers
    .map(function (_header, index) {
      return index;
    })
    .filter(function (index) {
      if (index === 0) return true;

      return rows.some(function (row) {
        return !isGuideEmptyValue(row[index]);
      });
    });

  return {
    headers: keepIndexes.map(function (index) {
      return headers[index];
    }),
    rows: rows.map(function (row) {
      return keepIndexes.map(function (index) {
        return row[index];
      });
    }),
  };
}

function parseRoleFromHeader(header) {
  var cleaned = String(header && header.raw ? header.raw : header || '')
    .replace(/\s*\(.+?\)\s*$/, '')
    .trim();

  if (!cleaned) return null;

  var parsed = parseRoleFromSizeLabel(cleaned);
  if (parsed && parsed.sizeLabel) {
    return {
      key: parsed.key,
      label: parsed.label,
      measurement: cleanRoleHeaderMeasurement(parsed.sizeLabel),
    };
  }

  var normalizedHeader = normalizeText(cleaned);
  for (var index = 0; index < ROLE_DEFINITIONS.length; index += 1) {
    var roleDefinition = ROLE_DEFINITIONS[index];
    var aliasCandidates = getRoleAliasCandidates(roleDefinition);

    for (var aliasIndex = 0; aliasIndex < aliasCandidates.length; aliasIndex += 1) {
      var alias = aliasCandidates[aliasIndex];
      var normalizedAlias = normalizeText(alias);
      if (!normalizedAlias || normalizedAlias.length < 3) continue;
      if (/^[a-z0-9]+$/.test(normalizedAlias)) {
        var aliasPattern = new RegExp('(^|[^a-z0-9])' + escapeRegExp(normalizedAlias) + '([^a-z0-9]|$)', 'i');
        if (!aliasPattern.test(normalizedHeader)) continue;
      } else if (normalizedHeader.indexOf(normalizedAlias) === -1) {
        continue;
      }

      return {
        key: roleDefinition.key,
        label: getLocalizedRoleLabel(roleDefinition),
        measurement: cleanRoleHeaderMeasurement(stripRoleAliasFromHeader(cleaned, aliasCandidates)) || cleaned,
      };
    }
  }

  return null;
}

function stripRoleAliasFromHeader(header, aliases) {
  var measurement = String(header || '').trim();
  if (!measurement) return '';

  for (var index = 0; index < aliases.length; index += 1) {
    var alias = String(aliases[index] || '').trim();
    if (!alias) continue;

    var escapedAlias = escapeRegExp(alias).replace(/\s+/g, '\\s+');
    var aliasPattern = new RegExp('(^|\\s+|\\s*[-–/]\\s*)' + escapedAlias + '(?=\\s+|$|\\s*[-–/]\\s*)', 'i');
    if (!aliasPattern.test(measurement)) continue;

    return measurement.replace(aliasPattern, ' ').replace(/\s+/g, ' ').trim();
  }

  return measurement;
}

function cleanRoleHeaderMeasurement(value) {
  return String(value || '')
    .replace(/\s+(?:de|del|de la|do|da|dos|das|di|della|del|du|des|of|for)\s*$/i, '')
    .replace(/\s+/g, ' ')
    .trim();
}

function buildSizeGuideGroups(parsed) {
  var rowGroups = {};

  parsed.rows.forEach(function (row) {
    var roleInfo = parseRoleFromSizeLabel(row[0]);
    if (!roleInfo) return;

    if (!rowGroups[roleInfo.key]) {
      rowGroups[roleInfo.key] = {
        key: roleInfo.key,
        label: roleInfo.label,
        helper: getRoleFitCopy(roleInfo.key),
        headers: [parsed.headers[0]].concat(parsed.headers.slice(1)),
        rows: [],
      };
    }

    rowGroups[roleInfo.key].rows.push([roleInfo.sizeLabel].concat(row.slice(1)));
  });

  var groupedRows = Object.keys(rowGroups)
    .map(function (key) {
      return rowGroups[key];
    })
    .filter(function (group) {
      return group.rows.length > 0;
    })
    .sort(function (first, second) {
      return getRoleOrder(first.key) - getRoleOrder(second.key);
    })
    .map(function (group) {
      var prunedGroup = pruneGuideGroupColumns(group.headers, group.rows);

      return {
        key: group.key,
        label: group.label,
        helper: group.helper,
        headers: prunedGroup.headers,
        rows: prunedGroup.rows,
      };
    });

  if (groupedRows.length > 1) return groupedRows;

  var heightIndex = parsed.headers.findIndex(function (header) {
    return isHeightLikeLabel(header && header.label ? header.label : '');
  });
  var groupedHeaders = {};

  parsed.headers.forEach(function (header, index) {
    if (index === 0 || index === heightIndex) return;
    var roleHeader = parseRoleFromHeader(header);
    if (!roleHeader) return;

    if (!groupedHeaders[roleHeader.key]) {
      groupedHeaders[roleHeader.key] = {
        label: roleHeader.label,
        helper: getRoleFitCopy(roleHeader.key),
        headers: [parsed.headers[0]],
        columnIndexes: [],
      };
      if (heightIndex > -1) groupedHeaders[roleHeader.key].headers.push(parsed.headers[heightIndex]);
    }

    groupedHeaders[roleHeader.key].headers.push({
      raw: parsed.headers[index].raw,
      label: roleHeader.measurement || parsed.headers[index].label,
      units: parsed.headers[index].units,
    });
    groupedHeaders[roleHeader.key].columnIndexes.push(index);
  });

  return Object.keys(groupedHeaders)
    .map(function (key) {
      var group = groupedHeaders[key];
      var rows = parsed.rows
        .map(function (row) {
          var hasRoleSpecificValue = group.columnIndexes.some(function (columnIndex) {
            return !isGuideEmptyValue(row[columnIndex]);
          });
          if (!hasRoleSpecificValue) return null;

          var rowValues = [row[0]];
          if (heightIndex > -1) rowValues.push(row[heightIndex]);
          group.columnIndexes.forEach(function (columnIndex) {
            rowValues.push(row[columnIndex]);
          });
          return rowValues;
        })
        .filter(function (rowValues) {
          return !!rowValues;
        });

      var prunedGroup = pruneGuideGroupColumns(group.headers, rows);

      return {
        key: key,
        label: group.label,
        headers: prunedGroup.headers,
        rows: prunedGroup.rows,
      };
    })
    .filter(function (group) {
      return group.rows.length > 0;
    })
    .sort(function (first, second) {
      return getRoleOrder(first.key) - getRoleOrder(second.key);
    });
}

function initPhotoReviewPanel(wrapper) {
  var panel = wrapper.querySelector('[data-photo-review-panel]');
  var media = wrapper.querySelector('[data-photo-review-media]');
  var title = wrapper.querySelector('.product-photo-strip__title');
  var reviewCount = parseInt(wrapper.getAttribute('data-product-review-count'), 10) || 0;
  var customerPhotosLabel = wrapper.getAttribute('data-customer-photos-label') || uiLabel('customerPhotos', 'Customer photos');
  var reviewRoot = document.getElementById('judgeme_product_reviews');
  if (!panel || !media || !reviewRoot) return;

  function populatePhotoPanel() {
    if (title && reviewCount <= 0) title.textContent = customerPhotosLabel;

    var links = Array.from(
      reviewRoot.querySelectorAll('.jdgm-rev__pics a, .jdgm-rev__pic-link, .jdgm-gallery__thumbnail-link, .jdgm-gallery__image-link')
    )
      .map(function (link) {
        var image = link.querySelector('img');
        if (!image || !image.getAttribute('src')) return null;
        return { href: link.getAttribute('href') || '#judgeme_product_reviews', src: image.getAttribute('src') };
      })
      .filter(Boolean)
      .slice(0, 4);

    if (!links.length) {
      panel.setAttribute('hidden', 'hidden');
      return;
    }

    media.innerHTML = links
      .map(function (item) {
        return (
          '<a href="' +
          escapeHtml(item.href) +
          '">' +
          '<img loading="lazy" src="' +
          escapeHtml(item.src) +
          '" alt="Customer review photo">' +
          '</a>'
        );
      })
      .join('');
    panel.removeAttribute('hidden');
  }

  populatePhotoPanel();

  var observer = new MutationObserver(populatePhotoPanel);
  observer.observe(reviewRoot, { childList: true, subtree: true });
}

function getRenderedPriceState(priceContainer) {
  if (!priceContainer) return null;

  var priceNode = priceContainer.querySelector('.price');
  var currentPrice = priceNode && priceNode.dataset ? priceNode.dataset.priceCurrentText : '';
  var compareAtPrice = priceNode && priceNode.dataset ? priceNode.dataset.priceCompareText : '';
  var isOnSale = priceNode && priceNode.dataset ? priceNode.dataset.priceOnSale === 'true' : false;

  if (!currentPrice) {
    var salePrice = priceContainer.querySelector('.price__sale .price-item--sale');
    var regularPrice = priceContainer.querySelector('.price__regular .price-item--regular');
    var fallbackPrice = priceContainer.querySelector('.price-item');
    var activePrice = salePrice || regularPrice || fallbackPrice;
    currentPrice = activePrice && activePrice.textContent ? activePrice.textContent.replace(/\s+/g, ' ').trim() : '';
  }

  return {
    currentPrice: currentPrice || '',
    compareAtPrice: compareAtPrice || '',
    isOnSale: isOnSale,
  };
}

function initDesktopStickyAtc(wrapper, sectionId) {
  var stickyBar = wrapper.parentElement.querySelector('[data-desktop-sticky-atc]');
  var stickyButton = stickyBar ? stickyBar.querySelector('[data-desktop-sticky-button]') : null;
  var stickyPrice = stickyBar ? stickyBar.querySelector('[data-desktop-sticky-price]') : null;
  var stickySize = stickyBar ? stickyBar.querySelector('[data-desktop-sticky-size]') : null;
  var variantSelects = document.getElementById('variant-selects-' + sectionId);
  var productForm = document.getElementById('product-form-' + sectionId);
  var mainButton = document.getElementById('ProductSubmitButton-' + sectionId);
  var matchingSetBuilder = wrapper.querySelector('[data-matching-set-builder]');
  var matchingSetButton = wrapper.querySelector('[data-matching-set-add-button]');
  var isMatchingSet = !!(matchingSetBuilder && matchingSetButton);
  var matchingSetStickyState =
    window.DLMMatchingSetStickyState && window.DLMMatchingSetStickyState[sectionId]
      ? window.DLMMatchingSetStickyState[sectionId]
      : null;
  var priceContainer = document.getElementById('price-' + sectionId);
  var desktopMedia = window.matchMedia('(min-width: 990px)');
  var buttonInView = true;
  var highlightedGroup = null;

  if (!stickyBar || !stickyButton) return;
  if (!mainButton && productForm) mainButton = productForm.querySelector('[name="add"]');
  if (isMatchingSet) mainButton = matchingSetButton;
  if (!mainButton) return;
  stickyBar.classList.toggle('sticky-desktop-atc--matching-set', isMatchingSet);

  function updatePrice() {
    if (!stickyPrice) return;
    if (isMatchingSet) {
      var hasSelectedPieces = !!(matchingSetStickyState && matchingSetStickyState.isReady);
      stickyPrice.textContent = hasSelectedPieces
        ? matchingSetStickyState.pieceCountLabel || wrapper.getAttribute('data-matching-set-add') || 'Matching pieces'
        : wrapper.getAttribute('data-matching-set-copy') || wrapper.getAttribute('data-matching-set-add') || 'Matching pieces';
      stickyPrice.removeAttribute('aria-label');
      stickyPrice.removeAttribute('title');
      return;
    }

    var priceState = getRenderedPriceState(priceContainer);
    if (!priceState || !priceState.currentPrice) return;

    stickyPrice.textContent = priceState.currentPrice;
    if (priceState.isOnSale && priceState.compareAtPrice && priceState.compareAtPrice !== priceState.currentPrice) {
      stickyPrice.setAttribute(
        'aria-label',
        priceState.currentPrice + ', compare at ' + priceState.compareAtPrice
      );
      stickyPrice.title = priceState.compareAtPrice;
      return;
    }

    stickyPrice.removeAttribute('aria-label');
    stickyPrice.removeAttribute('title');
  }

  function updateSize() {
    if (!stickySize || !variantSelects) return;
    if (isMatchingSet) {
      var hasSelectedPieces = !!(matchingSetStickyState && matchingSetStickyState.isReady);
      if (hasSelectedPieces && matchingSetStickyState.totalText) {
        stickySize.textContent = matchingSetStickyState.totalText;
        if (matchingSetStickyState.summaryText) {
          stickySize.title = matchingSetStickyState.summaryText;
          stickySize.setAttribute('aria-label', matchingSetStickyState.totalText + ': ' + matchingSetStickyState.summaryText);
        } else {
          stickySize.removeAttribute('title');
          stickySize.removeAttribute('aria-label');
        }
        stickySize.removeAttribute('hidden');
      } else {
        stickySize.textContent = '';
        stickySize.removeAttribute('title');
        stickySize.removeAttribute('aria-label');
        stickySize.setAttribute('hidden', 'hidden');
      }
      return;
    }

    var selectedSizes = [];

    Array.from(variantSelects.querySelectorAll('.product-form__input')).forEach(function (group) {
      if (!isVisibleGroup(group) || !isSizeGroup(group)) return;
      var value = getSelectedGroupValue(group);
      if (value) selectedSizes.push(value);
    });

    if (!selectedSizes.length) {
      stickySize.textContent = '';
      stickySize.setAttribute('hidden', 'hidden');
      return;
    }

    stickySize.textContent = selectedSizes.join(' / ');
    stickySize.removeAttribute('hidden');
  }

  function updateButtonState() {
    if (isMatchingSet) {
      var hasSelectedPieces = !!(matchingSetStickyState && matchingSetStickyState.isReady);
      stickyButton.textContent = hasSelectedPieces
        ? (matchingSetButton.textContent || wrapper.getAttribute('data-matching-set-add') || 'Add matching pieces').replace(/\s+/g, ' ').trim()
        : wrapper.getAttribute('data-choose-options-label') || 'Choose options';
      stickyButton.removeAttribute('disabled');
      stickyBar.classList.toggle('requires-options', !hasSelectedPieces);
      return;
    }

    var missingOption = getFirstMissingOption(variantSelects);
    var labelNode = mainButton.querySelector('span');
    var mainLabel = labelNode && labelNode.textContent ? labelNode.textContent.replace(/\s+/g, ' ').trim() : '';

    if (missingOption) {
      stickyButton.textContent = wrapper.getAttribute('data-select-size-label') || wrapper.getAttribute('data-choose-options-label');
      stickyButton.removeAttribute('disabled');
      return;
    }

    stickyButton.textContent = mainLabel || wrapper.getAttribute('data-add-to-cart-label') || 'Add to cart';
    if (mainButton.hasAttribute('disabled')) {
      stickyButton.setAttribute('disabled', 'disabled');
    } else {
      stickyButton.removeAttribute('disabled');
    }
  }

  function syncVisibility() {
    var shouldShow = desktopMedia.matches && !buttonInView;
    stickyBar.classList.toggle('is-visible', shouldShow);
    stickyBar.setAttribute('aria-hidden', shouldShow ? 'false' : 'true');
  }

  function alignMatchingSetForDrawer() {
    if (!matchingSetBuilder || typeof matchingSetBuilder.getBoundingClientRect !== 'function') return;

    var headerOffset = 120;
    var targetTop = matchingSetBuilder.getBoundingClientRect().top + window.scrollY - headerOffset;
    window.DLMCartDrawerOpenScrollY = Math.max(0, targetTop);
    window.scrollTo({
      top: window.DLMCartDrawerOpenScrollY,
      behavior: 'auto',
    });
  }

  stickyButton.addEventListener('click', function (event) {
    if (isMatchingSet) {
      if (!matchingSetStickyState || !matchingSetStickyState.isReady || matchingSetButton.hasAttribute('disabled')) {
        event.preventDefault();
        if (matchingSetBuilder && typeof matchingSetBuilder.scrollIntoView === 'function') {
          matchingSetBuilder.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
        return;
      }
      alignMatchingSetForDrawer();
      matchingSetButton.click();
      return;
    }

    var missingOption = getFirstMissingOption(variantSelects);
    if (missingOption) {
      event.preventDefault();
      scrollToMissingOption(missingOption, function (group) {
        if (highlightedGroup && highlightedGroup !== group) {
          highlightedGroup.classList.remove('sticky-option-target--highlight');
        }

        highlightedGroup = group;
      });
      return;
    }

    if (mainButton.hasAttribute('disabled')) return;
    mainButton.click();
  });

  if (isMatchingSet) {
    document.addEventListener('dlm:matching-set-summary', function (event) {
      if (!event || !event.detail || event.detail.sectionId !== sectionId) return;
      matchingSetStickyState = event.detail;
      updatePrice();
      updateSize();
      updateButtonState();
      syncVisibility();
    });
  }

  var buttonObserver = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        buttonInView = entry.isIntersecting;
        syncVisibility();
      });
    },
    { threshold: 0 }
  );
  buttonObserver.observe(mainButton);

  if (variantSelects) {
    variantSelects.addEventListener('change', function () {
      updateSize();
      updateButtonState();
    });
  }

  var buttonMutationObserver = new MutationObserver(updateButtonState);
  buttonMutationObserver.observe(mainButton, {
    attributes: true,
    attributeFilter: ['disabled'],
    childList: true,
    subtree: true,
    characterData: true,
  });

  if (priceContainer) {
    var priceObserver = new MutationObserver(updatePrice);
    priceObserver.observe(priceContainer, { childList: true, subtree: true, characterData: true });
  }

  function handleViewportChange() {
    if (!desktopMedia.matches) stickyBar.classList.remove('is-visible');
    syncVisibility();
  }

  if (typeof desktopMedia.addEventListener === 'function') {
    desktopMedia.addEventListener('change', handleViewportChange);
  } else if (typeof desktopMedia.addListener === 'function') {
    desktopMedia.addListener(handleViewportChange);
  }

  updatePrice();
  updateSize();
  updateButtonState();
  syncVisibility();
}

function isVisibleGroup(group) {
  if (!group) return false;
  var computedStyle = window.getComputedStyle(group);
  return computedStyle.display !== 'none' && computedStyle.visibility !== 'hidden';
}

function isSizeGroup(group) {
  if (!group) return false;
  var optionName = '';
  var control = group.querySelector('select[name], input[type="radio"][name]');
  if (control) optionName = getOptionNameFromControl(control);
  if (!optionName) {
    var label = group.querySelector('legend, label.form__label, .form__label');
    optionName = label ? label.textContent : '';
  }
  return isSizeLikeLabel(optionName);
}

function getSelectedGroupValue(group) {
  if (!group) return '';
  var select = group.querySelector('select');
  if (select) return String(select.value || '').trim();

  var checkedRadio = group.querySelector('input[type="radio"]:checked');
  if (checkedRadio) return String(checkedRadio.value || '').trim();

  return '';
}

function getFirstMissingOption(variantSelects) {
  if (!variantSelects) return null;

  var optionGroups = Array.from(variantSelects.querySelectorAll('.product-form__input')).filter(isVisibleGroup);

  for (var index = 0; index < optionGroups.length; index += 1) {
    var group = optionGroups[index];
    var select = group.querySelector('select');
    if (select && !select.value) {
      return {
        group: group,
        focusTarget: select,
        anchor: group.querySelector('label, legend, .form__label') || group,
      };
    }

    var radios = Array.from(group.querySelectorAll('input[type="radio"]'));
    if (radios.length && !group.querySelector('input[type="radio"]:checked')) {
      return {
        group: group,
        focusTarget: radios[0],
        anchor: group.querySelector('label, legend, .form__label') || group,
      };
    }
  }

  return null;
}

function scrollToMissingOption(missingOption, onHighlight) {
  if (!missingOption || !missingOption.group) return;

  missingOption.group.classList.add('sticky-option-target--highlight');
  if (typeof onHighlight === 'function') onHighlight(missingOption.group);

  window.setTimeout(function () {
    missingOption.group.classList.remove('sticky-option-target--highlight');
  }, 1400);

  var anchor = missingOption.anchor || missingOption.group;
  var offset = 120;
  var topPosition = window.scrollY + anchor.getBoundingClientRect().top - offset;
  window.scrollTo({ top: Math.max(topPosition, 0), behavior: 'smooth' });

  if (missingOption.focusTarget && typeof missingOption.focusTarget.focus === 'function') {
    try {
      missingOption.focusTarget.focus({ preventScroll: true });
    } catch (_error) {
      missingOption.focusTarget.focus();
    }
  }
}
