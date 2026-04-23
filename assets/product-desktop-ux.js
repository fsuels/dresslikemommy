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
  initMatchingSizeGuide(wrapper, sectionId);
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

function addBusinessDays(startDate, businessDays) {
  var date = new Date(startDate);
  var added = 0;

  while (added < businessDays) {
    date.setDate(date.getDate() + 1);
    var day = date.getDay();
    if (day !== 0 && day !== 6) added += 1;
  }

  return date;
}

function formatShortDate(date) {
  var locale = document.documentElement.getAttribute('lang') || undefined;
  try {
    return new Intl.DateTimeFormat(locale, { month: 'short', day: 'numeric' }).format(date);
  } catch (_error) {
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  }
}

function initDeliveryHighlights(wrapper) {
  var standardEstimate = formatShortDate(addBusinessDays(new Date(), 10));
  var premiumEstimate = formatShortDate(addBusinessDays(new Date(), 7));

  wrapper.querySelectorAll('[data-desktop-estimate]').forEach(function (node) {
    if (node.getAttribute('data-desktop-estimate') === 'premium') {
      node.textContent = premiumEstimate;
      return;
    }

    node.textContent = standardEstimate;
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
  'maat',
  'maten',
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
var TYPE_LABEL_TOKENS = ['type', 'style', 'tipo', 'estilo', 'genre', 'coupe', 'نوع', 'ستايل', 'نمط'];
var HEIGHT_LABEL_TOKENS = ['height', 'hauteur', 'altura', 'estatura', 'الارتفاع', 'الطول'];
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
    aliases: ['mother', 'mom', 'mom dress', 'madre', 'mama', 'mamá', 'mere', 'mère', 'maman', 'الأم', 'الام'],
  },
  {
    key: 'father',
    label: 'Father',
    labels: { ar: 'الأب', es: 'Papá', fr: 'Papa' },
    aliases: ['father', 'dad', 'dad shirt', 'padre', 'papa', 'papá', 'pere', 'père', 'الأب', 'الاب'],
  },
  {
    key: 'girl',
    label: 'Girl',
    labels: { ar: 'البنت', es: 'Niña', fr: 'Fille' },
    aliases: ['girl', 'daughter', 'daughter dress', 'nina', 'niña', 'fille', 'البنت', 'فتاة', 'الفتاة'],
  },
  {
    key: 'boy',
    label: 'Boy',
    labels: { ar: 'الولد', es: 'Niño', fr: 'Garçon' },
    aliases: ['boy', 'son', 'son shirt', 'nino', 'niño', 'garcon', 'garçon', 'الولد', 'ولد', 'فتى', 'الفتى'],
  },
  {
    key: 'child',
    label: 'Child',
    labels: { ar: 'الطفل', es: 'Niño', fr: 'Enfant' },
    aliases: ['child', 'children', 'kid', 'kids', 'enfant', 'enfants', 'infant', 'طفل', 'الطفل', 'أطفال', 'اطفال'],
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
    child: 'Consejo: compáralo con la talla habitual del niño.',
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
  return normalizeText(locale).split(/[-_]/)[0] || 'en';
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
  var locale = getLocaleRoot();
  return (roleDefinition.labels && roleDefinition.labels[locale]) || roleDefinition.label || '';
}

function sanitizeRoleSizeLabel(value) {
  return normalizeLocalizedSizeValue(value)
    .replace(/^(?:de|del|da|do|du|des|d'|من)\s+/i, '')
    .replace(/\s+/g, ' ')
    .trim();
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

    for (var aliasIndex = 0; aliasIndex < roleDefinition.aliases.length; aliasIndex += 1) {
      var alias = roleDefinition.aliases[aliasIndex];
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
  var copy = ROLE_FIT_COPY_BY_LOCALE[locale] || ROLE_FIT_COPY_BY_LOCALE.en;

  return Object.prototype.hasOwnProperty.call(copy, roleKey) ? copy[roleKey] : '';
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

function buildRoleGroups(productData, currentOptionContext) {
  var sizeOptionIndex = findSizeOptionIndex(productData.options);
  if (sizeOptionIndex === -1) return [];

  var roleGroups = {};

  productData.variants.forEach(function (variant) {
    if (!variant || !variant.available) return;

    for (var optionIndex = 0; optionIndex < productData.options.length; optionIndex += 1) {
      if (optionIndex === sizeOptionIndex) continue;

      var optionName = normalizeText(productData.options[optionIndex].name);
      if (!currentOptionContext[optionName]) continue;
      if (isTypeLikeLabel(optionName)) continue;

      if (normalizeText(getOptionValue(variant, optionIndex)) !== normalizeText(currentOptionContext[optionName])) {
        return;
      }
    }

    var roleInfo = parseRoleFromSizeLabel(getOptionValue(variant, sizeOptionIndex));
    if (!roleInfo) return;

    if (!roleGroups[roleInfo.key]) {
      roleGroups[roleInfo.key] = {
        key: roleInfo.key,
        label: roleInfo.label,
        helper: getRoleHelperLabel(variant, productData.options, sizeOptionIndex),
        options: [],
      };
    }

    roleGroups[roleInfo.key].options.push({
      id: String(variant.id),
      sizeLabel: roleInfo.sizeLabel,
      fullLabel: roleInfo.fullLabel,
      price: Number(variant.price) || 0,
    });
  });

  return Object.keys(roleGroups)
    .map(function (key) {
      return roleGroups[key];
    })
    .sort(function (first, second) {
      return getRoleOrder(first.key) - getRoleOrder(second.key);
    });
}

function getRoleHelperLabel(variant, options, sizeOptionIndex) {
  for (var optionIndex = 0; optionIndex < options.length; optionIndex += 1) {
    if (optionIndex === sizeOptionIndex) continue;

    var optionName = normalizeText(options[optionIndex].name);
    if (!isTypeLikeLabel(optionName)) continue;

    return String(getOptionValue(variant, optionIndex) || '').trim();
  }

  return '';
}

function getMatchingSetSelections(builder) {
  var selections = {};
  builder.querySelectorAll('[data-role-select]').forEach(function (select) {
    if (!select.value) return;
    selections[select.getAttribute('data-role-select')] = String(select.value);
  });
  return selections;
}

function initMatchingSetBuilder(wrapper, sectionId, productData) {
  var builder = wrapper.querySelector('[data-matching-set-builder]');
  if (!builder) return;

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

  function getCurrentVariant() {
    if (!selectedVariantInput || !selectedVariantInput.value) return null;
    var selectedId = String(selectedVariantInput.value);
    return (
      productData.variants.find(function (variant) {
        return String(variant.id) === selectedId;
      }) || null
    );
  }

  function updateSummary() {
    var selectedItems = [];

    builder.querySelectorAll('[data-role-select]').forEach(function (select) {
      var selectedOption = select.options[select.selectedIndex];
      var priceNode = select.closest('.product-matching-set__card').querySelector('[data-role-price]');
      if (selectedOption && selectedOption.getAttribute('data-price')) {
        priceNode.textContent = formatMoney(selectedOption.getAttribute('data-price'), currency);
      } else {
        priceNode.textContent = priceNode.getAttribute('data-default-price') || '';
      }

      if (!select.value || !selectedOption) return;

      selectedItems.push({
        id: select.value,
        label: selectedOption.textContent,
        price: Number(selectedOption.getAttribute('data-price')) || 0,
      });
    });

    if (!selectedItems.length) {
      emptyCopy.removeAttribute('hidden');
      chips.innerHTML = '';
      chips.setAttribute('hidden', 'hidden');
      total.textContent = '';
      total.setAttribute('hidden', 'hidden');
      addButton.setAttribute('disabled', 'disabled');
      return;
    }

    emptyCopy.setAttribute('hidden', 'hidden');
    chips.removeAttribute('hidden');
    chips.innerHTML = selectedItems
      .map(function (item) {
        return '<span class="product-matching-set__chip">' + escapeHtml(item.label) + '</span>';
      })
      .join('');

    total.textContent = formatMoney(
      selectedItems.reduce(function (sum, item) {
        return sum + item.price;
      }, 0),
      currency
    );
    total.removeAttribute('hidden');
    addButton.removeAttribute('disabled');
  }

  function renderBuilder(preservedSelections) {
    var groups = buildRoleGroups(productData, getCurrentOptionContext(variantSelects));

    if (groups.length < 2) {
      builder.setAttribute('hidden', 'hidden');
      return;
    }

    builder.removeAttribute('hidden');

    roleGrid.innerHTML = groups
      .map(function (group) {
        var minimumPrice = group.options.reduce(function (lowest, option) {
          return lowest === null || option.price < lowest ? option.price : lowest;
        }, null);

        var optionMarkup = group.options
          .map(function (option) {
            return (
              '<option value="' +
              escapeHtml(option.id) +
              '" data-price="' +
              escapeHtml(option.price) +
              '">' +
              escapeHtml(group.label + ' ' + option.sizeLabel) +
              '</option>'
            );
          })
          .join('');

        return (
          '<div class="product-matching-set__card">' +
          '<div class="product-matching-set__card-header">' +
          '<span class="product-matching-set__card-title">' +
          escapeHtml(group.label) +
          '</span>' +
          '<span class="product-matching-set__card-price" data-role-price data-default-price="' +
          escapeHtml(formatMoney(minimumPrice, currency)) +
          '">' +
          escapeHtml(formatMoney(minimumPrice, currency)) +
          '</span>' +
          '</div>' +
          (group.helper
            ? '<span class="product-matching-set__card-helper">' + escapeHtml(group.helper) + '</span>'
            : '') +
          '<select class="product-matching-set__select" data-role-select="' +
          escapeHtml(group.key) +
          '">' +
          '<option value="">' +
          escapeHtml(wrapper.getAttribute('data-select-size-label') || 'Select size') +
          '</option>' +
          optionMarkup +
          '</select>' +
          '</div>'
        );
      })
      .join('');

    var nextSelections = preservedSelections || {};
    if (!Object.keys(nextSelections).length) {
      var currentVariant = getCurrentVariant();
      if (currentVariant && !getFirstMissingOption(variantSelects)) {
        var currentRole = parseRoleFromSizeLabel(getOptionValue(currentVariant, findSizeOptionIndex(productData.options)));
        if (currentRole) nextSelections[currentRole.key] = String(currentVariant.id);
      }
    }

    builder.querySelectorAll('[data-role-select]').forEach(function (select) {
      var roleKey = select.getAttribute('data-role-select');
      var selectionValue = nextSelections[roleKey];
      if (!selectionValue) return;
      var matchingOption = Array.from(select.options).find(function (option) {
        return option.value === selectionValue;
      });
      if (matchingOption) select.value = selectionValue;
    });

    builder.querySelectorAll('[data-role-select]').forEach(function (select) {
      select.addEventListener('change', function () {
        status.setAttribute('hidden', 'hidden');
        updateSummary();
      });
    });

    updateSummary();
  }

  async function addSelectedItems() {
    var selectedItems = Array.from(builder.querySelectorAll('[data-role-select]'))
      .filter(function (select) {
        return !!select.value;
      })
      .map(function (select) {
        return { id: select.value, quantity: 1 };
      });

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

function initMatchingSizeGuide(wrapper, sectionId) {
  var UNIT_SYSTEM_STORAGE_KEY = 'dlm_size_chart_unit_system';
  var productSection = sectionId ? document.getElementById('MainProduct-' + sectionId) : null;
  var sizeGuideRoot = productSection || wrapper.closest('[id^="MainProduct-"]') || wrapper;
  var descriptionRoot = (sizeGuideRoot && sizeGuideRoot.querySelector('[data-product-description]')) || document.querySelector('[data-product-description]');
  var variantSelects = sectionId ? document.getElementById('variant-selects-' + sectionId) : null;
  var imagePresetGuide = descriptionRoot ? getImageBasedSizeGuidePreset(descriptionRoot) : null;
  var snapshot = sizeGuideRoot ? sizeGuideRoot.querySelector('[data-matching-size-guide-snapshot]') : null;
  var details = sizeGuideRoot ? sizeGuideRoot.querySelector('[data-matching-size-guide]') : null;
  var content = sizeGuideRoot ? sizeGuideRoot.querySelector('[data-matching-size-guide-content]') : null;
  var summary = details ? details.querySelector('summary') : null;
  var sizeSelect = findSizeGuideSelect(sizeGuideRoot);
  var sizeTable = getSizeGuideTable(sizeGuideRoot, sizeSelect, getSelectedGuideTypeValue());
  if (!snapshot || !details || !content || !sizeTable) return;

  var parsed = parseSizeGuideTable(sizeTable);
  if (!parsed) return;
  if (descriptionRoot) hideRedundantSizeGuideSources(descriptionRoot, imagePresetGuide);

  var compareLabel = wrapper.getAttribute('data-size-guide-compare-label') || 'Compare all sizes';
  var groupedLabel = wrapper.getAttribute('data-size-guide-grouped-label') || 'Compare family sizes';
  var snapshotLabel = wrapper.getAttribute('data-size-guide-selected-label') || 'Your size details';
  var compareHintLabel =
    wrapper.getAttribute('data-size-guide-compare-hint') || 'Open the full chart below to compare nearby sizes.';
  var unitToggleLabel = wrapper.getAttribute('data-size-guide-unit-toggle-label') || 'Size chart units';
  var groups = buildSizeGuideGroups(parsed);
  var selectedUnitSystem = getStoredSizeGuideUnitSystem() || 'metric';

  function getSelectedGuideTypeValue() {
    var optionContext = getCurrentOptionContext(variantSelects);
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

    var headerRow = table.querySelector('thead tr');
    if (headerRow) context.push(cellText(headerRow));

    return normalizeText(context.join(' '));
  }

  function tableMatchesSelectedType(table, selectedTypeValue) {
    var normalizedType = normalizeText(selectedTypeValue);
    if (!normalizedType) return false;

    var context = getSizeGuideTableContextText(table);
    if (!context) return false;
    if (context.indexOf(normalizedType) !== -1) return true;

    return normalizedType
      .split(/\s+/)
      .filter(function (token) {
        return token && token.length > 2;
      })
      .some(function (token) {
        return context.indexOf(token) !== -1;
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
      return (
        existingTables.find(function (table) {
          return tableMatchesSelectedType(table, selectedTypeValue);
        }) || existingTables[0]
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
    if (!existingParsed || (preferredGuide && preferredGuide.rows.length > existingParsed.rows.length)) {
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
    if (!sizeSelect) return null;

    var rawValue = String(sizeSelect.value || '').trim();
    var rawText = sizeSelect.selectedOptions && sizeSelect.selectedOptions[0]
      ? String(sizeSelect.selectedOptions[0].textContent || '').trim()
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
    var selectedRole = parsedRawValue || parsedRawText || parsedDisplayValue || null;

    return {
      rawValue: rawValue,
      rawText: rawText,
      displayValue: displayValue,
      roleKey: selectedRole && selectedRole.key ? selectedRole.key : '',
      roleLabel: selectedRole && selectedRole.label ? selectedRole.label : '',
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

    var ageRangeMatch = comparableRaw.match(/(\d{1,2})\s*-\s*(\d{1,2})\s*(?:t|y|yr|yrs|year|years)\b/i);
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

  function getGuideRowMatchScore(rowLabel, selectedState, rowRoleKey) {
    if (!selectedState || !selectedState.tokens) return -Infinity;
    if (selectedState.roleKey && rowRoleKey && selectedState.roleKey !== rowRoleKey) return -Infinity;

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
          score -= 140;
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
    var snapshotHtml = '<section class="matching-size-guide__snapshot-card" aria-live="polite" aria-atomic="true">';
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
      snapshotHtml += '<div class="matching-size-guide__metrics">' + measurementHtml + '</div>';
    } else {
      snapshotHtml += '<p class="matching-size-guide__helper matching-size-guide__helper--snapshot">' + escapeHtml(compareHintLabel) + '</p>';
    }

    snapshotHtml += '</section>';
    snapshot.innerHTML = snapshotHtml;
    snapshot.removeAttribute('hidden');
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
    sizeTable = getSizeGuideTable(sizeGuideRoot, sizeSelect, getSelectedGuideTypeValue());
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

  renderGuide();

  if (sizeSelect) {
    sizeSelect.addEventListener('change', function () {
      renderGuide();
    });
  }

  if (variantSelects) {
    variantSelects.addEventListener('change', function () {
      renderGuide();
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
  if (!parsed || !parsed.sizeLabel) return null;

  return {
    key: parsed.key,
    label: parsed.label,
    measurement: parsed.sizeLabel,
  };
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
          var rowValues = [row[0]];
          if (heightIndex > -1) rowValues.push(row[heightIndex]);
          group.columnIndexes.forEach(function (columnIndex) {
            rowValues.push(row[columnIndex]);
          });
          return rowValues;
        })
        .filter(function (rowValues) {
          return rowValues.slice(1).some(function (value) {
            return !isGuideEmptyValue(value);
          });
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
  var reviewRoot = document.getElementById('judgeme_product_reviews');
  if (!panel || !media || !reviewRoot) return;

  function populatePhotoPanel() {
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
  var priceContainer = document.getElementById('price-' + sectionId);
  var desktopMedia = window.matchMedia('(min-width: 990px)');
  var buttonInView = true;
  var highlightedGroup = null;

  if (!stickyBar || !stickyButton) return;
  if (!mainButton && productForm) mainButton = productForm.querySelector('[name="add"]');
  if (!mainButton) return;

  function updatePrice() {
    if (!stickyPrice) return;

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

  stickyButton.addEventListener('click', function (event) {
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
