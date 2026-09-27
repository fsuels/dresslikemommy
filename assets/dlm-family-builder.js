/*
 * Family list for the PDP "Build your matching set" picker.
 *
 * Progressive enhancement on top of the existing matching-set builder
 * rendered by snippets/product-desktop-ux.liquid and driven by
 * assets/product-desktop-ux-*.js. That builder adds ONE person's size per
 * add-to-cart. This module lets a shopper keep several people in a list
 * ("+ Add another family member"), then add everything with one
 * /cart/add.js request (items: [...] plus Dawn's cart-drawer sections).
 *
 * Rules:
 * - With an empty list nothing changes: the builder's own single-add button
 *   and flow work exactly as before.
 * - Only real variants with their real prices (from the page's own
 *   ProductMatchingSetData JSON). No bundle pricing or discounts.
 * - Does nothing when the page has no builder or fewer than two "who"
 *   choices (e.g. products without a Mother/Father/Child option).
 * - Never edits the builder's markup; it only clicks the builder's own
 *   controls to reset the picker, and (while the list has lines) holds back
 *   the builder's label/disabled writes to its add button so that button
 *   reads "Add all to bag (n) · total". Those writes are replayed when the
 *   list empties again.
 *
 * Pure helpers are exported for node tests (ops/tests/test_family_builder.mjs).
 * ES5 only; no build step.
 */
(function (root, factory) {
  var api = factory();
  if (typeof module === 'object' && module && module.exports) module.exports = api;
  if (root && root.document) {
    root.DLMFamilyBuilder = api;
    api.autoStart(root);
  }
})(typeof window !== 'undefined' ? window : this, function () {
  'use strict';

  var MAX_LINE_QTY = 99;

  // Customer-visible copy. Keys are language roots; unknown languages use en.
  var STRINGS = {
    en: {
      addAnother: '+ Add another family member',
      listTitle: 'Your family list',
      addAll: 'Add all to bag ({count}) · {total}',
      remove: 'Remove',
      added: 'Added to your family list',
      error: 'Could not add to bag. Please try again.',
      soldOut: '{item} is no longer available. Please remove it.'
    },
    es: {
      addAnother: '+ Añadir otro familiar',
      listTitle: 'Tu lista familiar',
      addAll: 'Añadir todo al carrito ({count}) · {total}',
      remove: 'Quitar',
      added: 'Añadido a tu lista familiar',
      error: 'No se pudo añadir al carrito. Inténtalo de nuevo.',
      soldOut: '{item} ya no está disponible. Quítalo, por favor.'
    },
    fr: {
      addAnother: '+ Ajouter un autre membre de la famille',
      listTitle: 'Votre liste famille',
      addAll: 'Tout ajouter au panier ({count}) · {total}',
      remove: 'Retirer',
      added: 'Ajouté à votre liste famille',
      error: "Impossible d'ajouter au panier. Veuillez réessayer.",
      soldOut: "{item} n'est plus disponible. Veuillez le retirer."
    },
    de: {
      addAnother: '+ Weiteres Familienmitglied hinzufügen',
      listTitle: 'Deine Familienliste',
      addAll: 'Alle in den Warenkorb ({count}) · {total}',
      remove: 'Entfernen',
      added: 'Zu deiner Familienliste hinzugefügt',
      error: 'Konnte nicht in den Warenkorb gelegt werden. Bitte versuche es erneut.',
      soldOut: '{item} ist nicht mehr verfügbar. Bitte entferne es.'
    },
    it: {
      addAnother: '+ Aggiungi un altro familiare',
      listTitle: 'La tua lista famiglia',
      addAll: 'Aggiungi tutto al carrello ({count}) · {total}',
      remove: 'Rimuovi',
      added: 'Aggiunto alla tua lista famiglia',
      error: 'Impossibile aggiungere al carrello. Riprova.',
      soldOut: '{item} non è più disponibile. Rimuovilo.'
    },
    nl: {
      addAnother: '+ Nog een gezinslid toevoegen',
      listTitle: 'Je gezinslijst',
      addAll: 'Alles in winkelwagen ({count}) · {total}',
      remove: 'Verwijderen',
      added: 'Toegevoegd aan je gezinslijst',
      error: 'Toevoegen aan winkelwagen is mislukt. Probeer het opnieuw.',
      soldOut: '{item} is niet meer beschikbaar. Verwijder het.'
    },
    pt: {
      addAnother: '+ Adicionar outro familiar',
      listTitle: 'Sua lista da família',
      addAll: 'Adicionar tudo ao carrinho ({count}) · {total}',
      remove: 'Remover',
      added: 'Adicionado à sua lista da família',
      error: 'Não foi possível adicionar ao carrinho. Tente novamente.',
      soldOut: '{item} não está mais disponível. Remova-o.'
    },
    da: {
      addAnother: '+ Tilføj endnu et familiemedlem',
      listTitle: 'Din familieliste',
      addAll: 'Læg alle i kurven ({count}) · {total}',
      remove: 'Fjern',
      added: 'Tilføjet til din familieliste',
      error: 'Kunne ikke lægge i kurven. Prøv igen.',
      soldOut: '{item} er ikke længere tilgængelig. Fjern den venligst.'
    },
    sv: {
      addAnother: '+ Lägg till ännu en familjemedlem',
      listTitle: 'Din familjelista',
      addAll: 'Lägg allt i varukorgen ({count}) · {total}',
      remove: 'Ta bort',
      added: 'Tillagd i din familjelista',
      error: 'Det gick inte att lägga i varukorgen. Försök igen.',
      soldOut: '{item} är inte längre tillgänglig. Ta bort den.'
    },
    no: {
      addAnother: '+ Legg til enda et familiemedlem',
      listTitle: 'Din familieliste',
      addAll: 'Legg alt i handlekurven ({count}) · {total}',
      remove: 'Fjern',
      added: 'Lagt til i familielisten din',
      error: 'Kunne ikke legge i handlekurven. Prøv igjen.',
      soldOut: '{item} er ikke lenger tilgjengelig. Fjern den.'
    },
    pl: {
      addAnother: '+ Dodaj kolejnego członka rodziny',
      listTitle: 'Twoja lista rodzinna',
      addAll: 'Dodaj wszystko do koszyka ({count}) · {total}',
      remove: 'Usuń',
      added: 'Dodano do listy rodzinnej',
      error: 'Nie udało się dodać do koszyka. Spróbuj ponownie.',
      soldOut: 'Produkt {item} jest już niedostępny. Usuń go z listy.'
    },
    cs: {
      addAnother: '+ Přidat dalšího člena rodiny',
      listTitle: 'Váš rodinný seznam',
      addAll: 'Přidat vše do košíku ({count}) · {total}',
      remove: 'Odebrat',
      added: 'Přidáno do rodinného seznamu',
      error: 'Nepodařilo se přidat do košíku. Zkuste to prosím znovu.',
      soldOut: 'Položka {item} již není dostupná. Odeberte ji prosím.'
    },
    fi: {
      addAnother: '+ Lisää toinen perheenjäsen',
      listTitle: 'Perheesi lista',
      addAll: 'Lisää kaikki ostoskoriin ({count}) · {total}',
      remove: 'Poista',
      added: 'Lisätty perheesi listaan',
      error: 'Lisääminen ostoskoriin epäonnistui. Yritä uudelleen.',
      soldOut: '{item} ei ole enää saatavilla. Poista se.'
    },
    ro: {
      addAnother: '+ Adaugă încă un membru al familiei',
      listTitle: 'Lista familiei tale',
      addAll: 'Adaugă tot în coș ({count}) · {total}',
      remove: 'Elimină',
      added: 'Adăugat în lista familiei',
      error: 'Nu s-a putut adăuga în coș. Încearcă din nou.',
      soldOut: '{item} nu mai este disponibil. Te rugăm să îl elimini.'
    },
    el: {
      addAnother: '+ Προσθήκη άλλου μέλους της οικογένειας',
      listTitle: 'Η οικογενειακή σας λίστα',
      addAll: 'Προσθήκη όλων στο καλάθι ({count}) · {total}',
      remove: 'Αφαίρεση',
      added: 'Προστέθηκε στην οικογενειακή σας λίστα',
      error: 'Δεν ήταν δυνατή η προσθήκη στο καλάθι. Δοκιμάστε ξανά.',
      soldOut: 'Το {item} δεν είναι πλέον διαθέσιμο. Αφαιρέστε το.'
    },
    hu: {
      addAnother: '+ Újabb családtag hozzáadása',
      listTitle: 'Családi listád',
      addAll: 'Összes a kosárba ({count}) · {total}',
      remove: 'Eltávolítás',
      added: 'Hozzáadva a családi listához',
      error: 'Nem sikerült a kosárba tenni. Kérjük, próbáld újra.',
      soldOut: 'A(z) {item} már nem elérhető. Kérjük, távolítsd el.'
    },
    tr: {
      addAnother: '+ Başka bir aile üyesi ekle',
      listTitle: 'Aile listen',
      addAll: 'Tümünü sepete ekle ({count}) · {total}',
      remove: 'Kaldır',
      added: 'Aile listene eklendi',
      error: 'Sepete eklenemedi. Lütfen tekrar dene.',
      soldOut: '{item} artık mevcut değil. Lütfen kaldır.'
    },
    ru: {
      addAnother: '+ Добавить ещё члена семьи',
      listTitle: 'Ваш семейный список',
      addAll: 'Добавить всё в корзину ({count}) · {total}',
      remove: 'Удалить',
      added: 'Добавлено в семейный список',
      error: 'Не удалось добавить в корзину. Попробуйте ещё раз.',
      soldOut: 'Товар {item} больше недоступен. Удалите его.'
    },
    ja: {
      addAnother: '+ 別のご家族を追加',
      listTitle: 'ご家族リスト',
      addAll: 'すべてカートに追加 ({count}) · {total}',
      remove: '削除',
      added: 'ご家族リストに追加しました',
      error: 'カートに追加できませんでした。もう一度お試しください。',
      soldOut: '{item} は現在ご購入いただけません。削除してください。'
    },
    ko: {
      addAnother: '+ 다른 가족 추가',
      listTitle: '가족 목록',
      addAll: '모두 장바구니에 담기 ({count}) · {total}',
      remove: '삭제',
      added: '가족 목록에 추가되었습니다',
      error: '장바구니에 담지 못했습니다. 다시 시도해 주세요.',
      soldOut: '{item} 상품은 더 이상 구매할 수 없습니다. 삭제해 주세요.'
    },
    zh: {
      addAnother: '+ 添加其他家庭成员',
      listTitle: '您的家庭清单',
      addAll: '全部加入购物车 ({count}) · {total}',
      remove: '移除',
      added: '已加入家庭清单',
      error: '无法加入购物车，请重试。',
      soldOut: '{item} 已无法购买，请移除。'
    },
    ar: {
      addAnother: '+ أضف فردًا آخر من العائلة',
      listTitle: 'قائمة عائلتك',
      addAll: 'أضف الكل إلى السلة ({count}) · {total}',
      remove: 'إزالة',
      added: 'تمت الإضافة إلى قائمة عائلتك',
      error: 'تعذرت الإضافة إلى السلة. يرجى المحاولة مرة أخرى.',
      soldOut: '{item} لم يعد متوفرًا. يرجى إزالته.'
    },
    he: {
      addAnother: '+ הוספת בן או בת משפחה נוספים',
      listTitle: 'הרשימה המשפחתית שלך',
      addAll: 'הוספת הכול לסל ({count}) · {total}',
      remove: 'הסרה',
      added: 'נוסף לרשימה המשפחתית',
      error: 'לא ניתן היה להוסיף לסל. נסו שוב.',
      soldOut: '{item} אינו זמין עוד. יש להסיר אותו.'
    },
    hi: {
      addAnother: '+ परिवार का एक और सदस्य जोड़ें',
      listTitle: 'आपकी परिवार सूची',
      addAll: 'सभी को कार्ट में जोड़ें ({count}) · {total}',
      remove: 'हटाएँ',
      added: 'आपकी परिवार सूची में जोड़ा गया',
      error: 'कार्ट में नहीं जोड़ा जा सका। कृपया फिर से प्रयास करें।',
      soldOut: '{item} अब उपलब्ध नहीं है। कृपया इसे हटाएँ।'
    }
  };

  var LANGUAGE_ALIASES = { nb: 'no', nn: 'no', iw: 'he' };

  // ---------------------------------------------------------------------
  // Pure helpers (tested in node)
  // ---------------------------------------------------------------------

  function resolveLanguage(locale) {
    var rootLang = String(locale || '').toLowerCase().replace('_', '-').split('-')[0];
    if (LANGUAGE_ALIASES[rootLang]) rootLang = LANGUAGE_ALIASES[rootLang];
    return Object.prototype.hasOwnProperty.call(STRINGS, rootLang) ? rootLang : 'en';
  }

  function translate(key, locale, values) {
    var lang = resolveLanguage(locale);
    var template = (STRINGS[lang] && STRINGS[lang][key]) || STRINGS.en[key] || '';
    return String(template).replace(/\{([a-zA-Z0-9_]+)\}/g, function (match, name) {
      return values && Object.prototype.hasOwnProperty.call(values, name) ? String(values[name]) : '';
    });
  }

  function clampQty(value) {
    var qty = Math.floor(Number(value) || 0);
    if (qty < 1) return 0;
    return qty > MAX_LINE_QTY ? MAX_LINE_QTY : qty;
  }

  // Lines are keyed by variant id; adding the same variant again merges
  // quantities. Returns a new array and never mutates the input.
  function mergeLine(lines, line) {
    var result = [];
    var list = lines || [];
    var i;
    for (i = 0; i < list.length; i += 1) result.push(copyLine(list[i]));
    if (!line || !line.variantId) return result;
    var qty = clampQty(line.quantity);
    if (!qty) return result;
    var id = String(line.variantId);
    for (i = 0; i < result.length; i += 1) {
      if (result[i].variantId === id) {
        result[i].quantity = clampQty(result[i].quantity + qty);
        return result;
      }
    }
    var added = copyLine(line);
    added.quantity = qty;
    result.push(added);
    return result;
  }

  function copyLine(line) {
    return {
      variantId: String(line.variantId),
      quantity: clampQty(line.quantity),
      unitPrice: Math.round(Number(line.unitPrice) || 0),
      roleKey: line.roleKey ? String(line.roleKey) : '',
      label: line.label ? String(line.label) : ''
    };
  }

  function removeLine(lines, variantId) {
    var id = String(variantId);
    var result = [];
    (lines || []).forEach(function (line) {
      if (String(line.variantId) !== id) result.push(copyLine(line));
    });
    return result;
  }

  // The picker's current, fully chosen selection counts toward the button
  // total ("what you see selected is what gets added").
  function combineWithPending(lines, pending) {
    return pending ? mergeLine(lines, pending) : mergeLine(lines, null);
  }

  function computeTotals(lines) {
    var count = 0;
    var cents = 0;
    (lines || []).forEach(function (line) {
      var qty = clampQty(line.quantity);
      count += qty;
      cents += qty * Math.round(Number(line.unitPrice) || 0);
    });
    return { count: count, cents: cents };
  }

  function buildItems(lines) {
    var items = [];
    (lines || []).forEach(function (line) {
      var qty = clampQty(line.quantity);
      var id = Number(line.variantId);
      if (!qty || !id) return;
      items.push({ id: id, quantity: qty });
    });
    return items;
  }

  function buildRequestBody(lines, sectionIds, sectionsUrl) {
    var body = { items: buildItems(lines) };
    if (sectionIds && sectionIds.length) {
      body.sections = sectionIds.join(',');
      if (sectionsUrl) body.sections_url = sectionsUrl;
    }
    return body;
  }

  // Lines whose variant is missing from the page data or marked sold out.
  function findUnavailable(lines, variantsById) {
    var map = variantsById || {};
    var out = [];
    (lines || []).forEach(function (line) {
      var variant = map[String(line.variantId)];
      if (!variant || variant.available === false) out.push(copyLine(line));
    });
    return out;
  }

  function usedRoleMap(lines, extraRoleKeys) {
    var used = {};
    (lines || []).forEach(function (line) {
      if (line && line.roleKey) used[line.roleKey] = true;
    });
    (extraRoleKeys || []).forEach(function (key) {
      if (key) used[key] = true;
    });
    return used;
  }

  // Next "who" to pre-select after a piece is kept or added to the bag: the
  // first role in the builder's order that is not yet in the list (or, via
  // extraRoleKeys, already added to the bag from this page). null = stay on
  // the current role (e.g. a second child) and just clear its size.
  function nextRoleKey(roleKeys, lines, extraRoleKeys) {
    var used = usedRoleMap(lines, extraRoleKeys);
    for (var i = 0; i < (roleKeys || []).length; i += 1) {
      if (!used[roleKeys[i]]) return roleKeys[i];
    }
    return null;
  }

  // "+ Father" / "+ Child" chips, one per role the builder actually offers
  // (roles = [{ key, label }] in builder order, labels already localized by
  // the builder). A chip keeps the current piece and switches the picker to
  // that role; the current role stays offered for a second child. `missing`
  // marks roles nobody has picked yet. Returns [] when any label is unknown,
  // so the plain "+ Add another family member" button is used instead.
  function roleChips(roles, lines, pending, extraRoleKeys) {
    var list = roles || [];
    if (list.length < 2) return [];
    var used = usedRoleMap(pending ? (lines || []).concat([pending]) : lines, extraRoleKeys);
    var chips = [];
    for (var i = 0; i < list.length; i += 1) {
      var key = list[i] && list[i].key ? String(list[i].key) : '';
      var label = list[i] && list[i].label ? String(list[i].label).trim() : '';
      if (!key || !label) return [];
      chips.push({ key: key, label: '+ ' + label, missing: !used[key] });
    }
    return chips;
  }

  // Caption over the chips: the existing "+ Add another family member"
  // copy without its leading plus (the chips carry their own).
  function stripLeadingPlus(text) {
    return String(text || '').replace(/^\s*[+\uff0b]\s*/, '');
  }

  // True when the builder's status line shows its own success copy.
  function isAddSuccess(statusText, successText) {
    var expected = String(successText || '').trim();
    return !!expected && String(statusText || '').trim() === expected;
  }

  // Learn the shop's money format from one rendered variant price, e.g.
  // "$32.99 USD" for 3299 cents or "32,99 €" for 3299 cents.
  function parseMoneyFormat(text, cents) {
    var source = String(text || '');
    var value = Math.round(Number(cents));
    if (!source || !(value >= 0)) return null;
    var match = source.match(/\d(?:[\d.,'\u00a0\u202f ]*\d)?/);
    if (!match) return null;
    var chunk = match[0];
    var digits = chunk.replace(/\D/g, '');
    var decimalMatch = chunk.match(/([.,])(\d{2})$/);
    var decimals = 0;
    var decimalSep = '.';
    if (decimalMatch && digits === String(value)) {
      decimals = 2;
      decimalSep = decimalMatch[1];
    } else if (digits !== String(Math.round(value / 100))) {
      return null;
    }
    var integerPart = decimals ? chunk.slice(0, chunk.length - 3) : chunk;
    var thousandsMatch = integerPart.match(/[^\d]/);
    var thousandsSep = thousandsMatch ? thousandsMatch[0] : decimalSep === ',' ? '.' : ',';
    return {
      prefix: source.slice(0, match.index),
      suffix: source.slice(match.index + chunk.length),
      decimals: decimals,
      decimalSep: decimalSep,
      thousandsSep: thousandsSep
    };
  }

  function formatMoney(cents, format, currency, locale) {
    var value = Math.round(Number(cents) || 0);
    if (format) {
      var whole = format.decimals ? Math.floor(value / 100) : Math.round(value / 100);
      var integer = String(whole).replace(/\B(?=(\d{3})+(?!\d))/g, format.thousandsSep);
      var fraction = format.decimals ? format.decimalSep + ('0' + (value % 100)).slice(-2) : '';
      return format.prefix + integer + fraction + format.suffix;
    }
    try {
      return new Intl.NumberFormat(locale || undefined, { style: 'currency', currency: currency || 'USD' }).format(value / 100);
    } catch (error) {
      return (value / 100).toFixed(2);
    }
  }

  function cartAddJsUrl(routes) {
    var base = (routes && routes.cart_add_url) || '/cart/add';
    return /\.js$/.test(base) ? base : base + '.js';
  }

  // ---------------------------------------------------------------------
  // DOM layer
  // ---------------------------------------------------------------------

  function decodeEntities(doc, text) {
    var area = doc.createElement('textarea');
    area.innerHTML = String(text || '').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    return area.value;
  }

  function cssEscape(win, value) {
    if (win.CSS && typeof win.CSS.escape === 'function') return win.CSS.escape(value);
    return String(value).replace(/["\\]/g, '\\$&');
  }

  function mount(win, wrapper) {
    var doc = win.document;
    if (!wrapper || wrapper.hasAttribute('data-dlm-family-builder-mounted')) return false;
    var builder = wrapper.querySelector('[data-matching-set-builder]');
    if (!builder || builder.hidden) return false;
    var roleGrid = builder.querySelector('[data-matching-set-roles]');
    var addButton = builder.querySelector('[data-matching-set-add-button]');
    if (!roleGrid || !addButton || !addButton.parentNode) return false;
    if (roleGrid.querySelectorAll('[data-select-role-group]').length < 2) return false;

    var sectionId = wrapper.getAttribute('data-section-id') || '';
    var dataNode = doc.getElementById('ProductMatchingSetData-' + sectionId);
    var productData;
    try {
      productData = JSON.parse(dataNode ? dataNode.textContent : '');
    } catch (error) {
      return false;
    }
    if (!productData || !productData.variants || !productData.variants.length) return false;

    wrapper.setAttribute('data-dlm-family-builder-mounted', 'true');

    var locale = (win.Shopify && win.Shopify.locale) || doc.documentElement.getAttribute('lang') || 'en';
    var variantsById = {};
    productData.variants.forEach(function (variant) {
      variantsById[String(variant.id)] = variant;
    });
    var sample = productData.variants[0];
    var moneyFormat = parseMoneyFormat(decodeEntities(doc, sample.price_text), sample.price);
    var status = builder.querySelector('[data-matching-set-status]');

    var lines = [];
    // Roles added to the bag from this page view (single piece or list), so
    // the picker moves on to the next family member instead of repeating.
    var addedRoleKeys = [];
    // Role of a single piece the builder is adding right now (no list).
    var singleAddRole = '';
    var successText = wrapper.getAttribute('data-matching-set-success') || '';
    var busy = false;
    var applying = false;
    var appliedLabel = '';
    // What the builder itself last wrote to its button (restored when the
    // list empties again).
    var builderState = { text: addButton.textContent, disabled: addButton.hasAttribute('disabled') };

    function t(key, values) {
      return translate(key, locale, values);
    }

    function money(cents) {
      return formatMoney(cents, moneyFormat, productData.currency, locale);
    }

    // --- panel markup (built with DOM APIs, no HTML strings) ---
    var panel = doc.createElement('div');
    panel.className = 'dlm-family-builder';
    panel.setAttribute('data-dlm-family-builder', '');

    // "+ Father" / "+ Child" chips (shown once a piece is chosen).
    var chipBox = doc.createElement('div');
    chipBox.className = 'dlm-family-builder__next';
    chipBox.setAttribute('role', 'group');
    chipBox.hidden = true;
    var chipTitle = doc.createElement('p');
    chipTitle.className = 'dlm-family-builder__next-title';
    chipTitle.id = 'DlmFamilyNext-' + sectionId;
    chipTitle.textContent = stripLeadingPlus(t('addAnother'));
    chipBox.setAttribute('aria-labelledby', chipTitle.id);
    var chipRow = doc.createElement('div');
    chipRow.className = 'dlm-family-builder__chips';
    chipBox.appendChild(chipTitle);
    chipBox.appendChild(chipRow);
    var chipSignature = '';

    var addAnother = doc.createElement('button');
    addAnother.type = 'button';
    addAnother.className = 'dlm-family-builder__add-another';
    addAnother.textContent = t('addAnother');
    addAnother.hidden = true;

    var listBox = doc.createElement('div');
    listBox.className = 'dlm-family-builder__list';
    listBox.hidden = true;
    var heading = doc.createElement('p');
    heading.className = 'dlm-family-builder__heading';
    heading.id = 'DlmFamilyList-' + sectionId;
    heading.textContent = t('listTitle');
    var list = doc.createElement('ul');
    list.className = 'dlm-family-builder__lines';
    list.setAttribute('aria-labelledby', heading.id);
    listBox.appendChild(heading);
    listBox.appendChild(list);

    var errorBox = doc.createElement('p');
    errorBox.className = 'dlm-family-builder__error';
    errorBox.setAttribute('role', 'alert');
    errorBox.hidden = true;

    var announcer = doc.createElement('p');
    announcer.className = 'visually-hidden dlm-family-builder__live';
    announcer.setAttribute('aria-live', 'polite');
    announcer.setAttribute('role', 'status');

    panel.appendChild(chipBox);
    panel.appendChild(addAnother);
    panel.appendChild(listBox);
    panel.appendChild(errorBox);
    panel.appendChild(announcer);
    addButton.parentNode.parentNode.insertBefore(panel, addButton.parentNode);

    // --- reading the builder's current selection ---
    function roleKeysInOrder() {
      var keys = [];
      roleGrid.querySelectorAll('[data-select-role-group]').forEach(function (btn) {
        keys.push(btn.getAttribute('data-select-role-group'));
      });
      return keys;
    }

    function roleOptions() {
      var roles = [];
      roleGrid.querySelectorAll('[data-select-role-group]').forEach(function (btn) {
        var labelNode = btn.querySelector('.product-matching-set__role-label');
        roles.push({ key: btn.getAttribute('data-select-role-group'), label: labelNode ? labelNode.textContent : '' });
      });
      return roles;
    }

    function rememberAdded(roleKeys) {
      (roleKeys || []).forEach(function (key) {
        if (key && addedRoleKeys.indexOf(key) === -1) addedRoleKeys.push(key);
      });
    }

    function getPending() {
      var cards = roleGrid.querySelectorAll('[data-instance-card]');
      if (cards.length !== 1) return null;
      var card = cards[0];
      var pill = card.querySelector('[data-instance-pill][aria-pressed="true"]');
      if (!pill) return null;
      var priceNode = doc.querySelector('#price-' + cssEscape(win, sectionId) + ' .price[data-price-variant-id]');
      var variant = priceNode ? variantsById[priceNode.getAttribute('data-price-variant-id')] : null;
      if (!variant || variant.available === false) return null;
      var roleButton = roleGrid.querySelector('[data-select-role-group][aria-pressed="true"]');
      var roleLabelNode = roleButton && roleButton.querySelector('.product-matching-set__role-label');
      var parts = [roleLabelNode ? roleLabelNode.textContent.trim() : '', pill.getAttribute('data-size-label') || ''];
      card.querySelectorAll('[data-instance-axis][aria-pressed="true"]').forEach(function (axis) {
        parts.push(axis.getAttribute('data-axis-value') || '');
      });
      var qtyNode = card.querySelector('[data-qty-value]');
      return {
        variantId: String(variant.id),
        quantity: clampQty(qtyNode ? qtyNode.textContent : 1) || 1,
        unitPrice: Number(variant.price) || 0,
        roleKey: roleButton ? roleButton.getAttribute('data-select-role-group') : '',
        label: parts.filter(Boolean).join(' · ')
      };
    }

    // --- rendering ---
    function renderChips(pending) {
      var chips = pending && !busy ? roleChips(roleOptions(), lines, pending, addedRoleKeys) : [];
      chipBox.hidden = chips.length === 0;
      addAnother.hidden = !pending || busy || chips.length > 0;
      var signature = JSON.stringify(chips);
      if (signature === chipSignature) return;
      var hadFocus = chipRow.contains(doc.activeElement);
      chipSignature = signature;
      while (chipRow.firstChild) chipRow.removeChild(chipRow.firstChild);
      chips.forEach(function (chip) {
        var button = doc.createElement('button');
        button.type = 'button';
        button.className = 'dlm-family-builder__chip' + (chip.missing ? ' dlm-family-builder__chip--missing' : '');
        button.setAttribute('data-dlm-family-role', chip.key);
        button.textContent = chip.label;
        chipRow.appendChild(button);
      });
      if (hadFocus && chipRow.firstChild) chipRow.firstChild.focus();
    }

    function renderList() {
      while (list.firstChild) list.removeChild(list.firstChild);
      lines.forEach(function (line) {
        var item = doc.createElement('li');
        item.className = 'dlm-family-builder__line';
        var label = doc.createElement('span');
        label.className = 'dlm-family-builder__line-label';
        label.textContent = line.label;
        var qty = doc.createElement('span');
        qty.className = 'dlm-family-builder__line-qty';
        qty.textContent = '× ' + line.quantity;
        var price = doc.createElement('span');
        price.className = 'dlm-family-builder__line-price';
        price.textContent = money(line.unitPrice * line.quantity);
        var remove = doc.createElement('button');
        remove.type = 'button';
        remove.className = 'dlm-family-builder__remove';
        remove.setAttribute('data-dlm-family-remove', line.variantId);
        remove.setAttribute('aria-label', t('remove') + ': ' + line.label);
        remove.textContent = t('remove');
        item.appendChild(label);
        item.appendChild(qty);
        item.appendChild(price);
        item.appendChild(remove);
        list.appendChild(item);
      });
      listBox.hidden = lines.length === 0;
    }

    function combinedLabel() {
      var totals = computeTotals(combineWithPending(lines, getPending()));
      return t('addAll', { count: totals.count, total: money(totals.cents) });
    }

    // The builder rewrites its button (textContent + disabled attribute) on
    // every render. Capture those writes synchronously on this one element:
    // with an empty list they pass straight through (single-add unchanged);
    // with a list they are remembered and our label is re-applied.
    var textDescriptor = Object.getOwnPropertyDescriptor(win.Node.prototype, 'textContent');
    var nativeSetAttribute = addButton.setAttribute;
    var nativeRemoveAttribute = addButton.removeAttribute;

    function writeText(text) {
      if (textDescriptor.get.call(addButton) !== text) textDescriptor.set.call(addButton, text);
    }

    function writeDisabled(disabled) {
      if (disabled) nativeSetAttribute.call(addButton, 'disabled', 'disabled');
      else nativeRemoveAttribute.call(addButton, 'disabled');
    }

    Object.defineProperty(addButton, 'textContent', {
      configurable: true,
      get: function () {
        return textDescriptor.get.call(this);
      },
      set: function (value) {
        builderState.text = String(value);
        if (lines.length && !applying) sync();
        else textDescriptor.set.call(this, value);
      }
    });
    addButton.setAttribute = function (name, value) {
      if (String(name).toLowerCase() === 'disabled' && !applying) {
        builderState.disabled = true;
        if (lines.length) return undefined;
      }
      return nativeSetAttribute.call(this, name, value);
    };
    addButton.removeAttribute = function (name) {
      if (String(name).toLowerCase() === 'disabled' && !applying) {
        builderState.disabled = false;
        if (lines.length) return undefined;
      }
      return nativeRemoveAttribute.call(this, name);
    };

    function setButton(text, disabled) {
      applying = true;
      try {
        writeText(text);
        writeDisabled(disabled);
      } finally {
        applying = false;
      }
    }

    function sync() {
      var pending = getPending();
      renderChips(pending);
      if (!lines.length) {
        wrapper.removeAttribute('data-dlm-family-list');
        nativeRemoveAttribute.call(addButton, 'aria-busy');
        if (appliedLabel) {
          appliedLabel = '';
          setButton(builderState.text, builderState.disabled);
        }
        if (stickyIsOurs) scheduleSticky();
        return;
      }
      wrapper.setAttribute('data-dlm-family-list', String(lines.length));
      appliedLabel = combinedLabel();
      setButton(appliedLabel, busy);
      if (busy) addButton.setAttribute('aria-busy', 'true');
      else addButton.removeAttribute('aria-busy');
      scheduleSticky();
    }

    // Sticky add bars (desktop in product-desktop-ux, mobile in
    // main-product) read the builder's "dlm:matching-set-summary" state and
    // forward taps to the add button. While the list is used, publish a
    // list-aware state right after the builder's own; restore the builder's
    // last state when the list empties.
    var stickyStore = win.DLMMatchingSetStickyState || {};
    var lastBuilderSticky = stickyStore[sectionId] || null;
    var stickyTimer = null;
    var stickyIsOurs = false;

    function publishSticky() {
      stickyTimer = null;
      var detail;
      if (lines.length) {
        var all = combineWithPending(lines, getPending());
        var totals = computeTotals(all);
        detail = {
          sectionId: sectionId,
          source: 'dlm-family-builder',
          pieceCount: totals.count,
          pieceCountLabel: t('listTitle') + ' (' + totals.count + ')',
          totalText: money(totals.cents),
          summaryText: all
            .map(function (line) {
              return line.label + (line.quantity > 1 ? ' x' + line.quantity : '');
            })
            .join(', '),
          isReady: true
        };
        stickyIsOurs = true;
      } else if (stickyIsOurs && lastBuilderSticky) {
        detail = lastBuilderSticky;
        stickyIsOurs = false;
      } else {
        return;
      }
      try {
        win.DLMMatchingSetStickyState = win.DLMMatchingSetStickyState || {};
        win.DLMMatchingSetStickyState[sectionId] = detail;
        doc.dispatchEvent(new win.CustomEvent('dlm:matching-set-summary', { detail: detail }));
      } catch (error) {
        /* sticky bars are optional */
      }
    }

    function scheduleSticky() {
      if (!stickyTimer) stickyTimer = win.setTimeout(publishSticky, 0);
    }

    doc.addEventListener('dlm:matching-set-summary', function (event) {
      var detail = event && event.detail;
      if (!detail || detail.sectionId !== sectionId || detail.source === 'dlm-family-builder') return;
      lastBuilderSticky = detail;
      if (lines.length) scheduleSticky();
    });

    function announce(prefix) {
      var text = lines.length ? combinedLabel() : '';
      announcer.textContent = [prefix, text].filter(Boolean).join('. ');
    }

    function showError(message) {
      errorBox.textContent = message;
      errorBox.hidden = !message;
    }

    // Size/role changes re-render the grid; keep "+ Add another" in step
    // even if a render path does not rewrite the button.
    if (typeof win.MutationObserver === 'function') {
      new win.MutationObserver(function () {
        sync();
      }).observe(roleGrid, { childList: true });
    }

    // --- picker reset (only through the builder's own controls) ---
    function clearCurrentSize() {
      var pill = roleGrid.querySelector('[data-instance-pill][aria-pressed="true"]');
      if (pill) pill.click();
      for (var guard = 0; guard < MAX_LINE_QTY; guard += 1) {
        var dec = roleGrid.querySelector('[data-qty-action="dec"]');
        if (!dec || dec.disabled) break;
        dec.click();
      }
    }

    // targetKey: a role the shopper chose from a chip; otherwise the next
    // family member nobody has picked yet.
    function resetPicker(targetKey) {
      var next = targetKey || nextRoleKey(roleKeysInOrder(), lines, addedRoleKeys);
      var nextButton = next
        ? roleGrid.querySelector('[data-select-role-group="' + cssEscape(win, next) + '"]')
        : null;
      if (nextButton && nextButton.getAttribute('aria-pressed') !== 'true') nextButton.click();
      else clearCurrentSize();
      var focusTarget = roleGrid.querySelector('[data-select-role-group][aria-pressed="true"]');
      if (focusTarget && typeof focusTarget.focus === 'function') focusTarget.focus();
    }

    function keepPending(targetKey) {
      if (busy) return;
      var pending = getPending();
      if (!pending) return;
      showError('');
      if (status) status.hidden = true;
      lines = mergeLine(lines, pending);
      renderList();
      resetPicker(targetKey);
      sync();
      announce(t('added') + ': ' + pending.label);
    }

    addAnother.addEventListener('click', function () {
      keepPending('');
    });

    chipRow.addEventListener('click', function (event) {
      var chip = event.target && event.target.closest ? event.target.closest('[data-dlm-family-role]') : null;
      if (chip) keepPending(chip.getAttribute('data-dlm-family-role'));
    });

    // After the builder's own single-piece add succeeds, pre-select the next
    // family member so the second piece is one size tap away. The builder
    // hides its confirmation when the role changes; show it again.
    function onStatusChange() {
      if (!singleAddRole || !status || status.hidden) return;
      var role = singleAddRole;
      singleAddRole = '';
      // Same fallback copy the builder shows when the attribute is empty.
      if (!isAddSuccess(status.textContent, successText || 'Matching set added to cart.')) return;
      rememberAdded([role]);
      var next = nextRoleKey(roleKeysInOrder(), lines, addedRoleKeys);
      var nextButton = next
        ? roleGrid.querySelector('[data-select-role-group="' + cssEscape(win, next) + '"]')
        : null;
      if (!nextButton || nextButton.getAttribute('aria-pressed') === 'true') return;
      var confirmation = status.textContent;
      nextButton.click();
      status.textContent = confirmation;
      status.hidden = false;
    }

    if (status && typeof win.MutationObserver === 'function') {
      new win.MutationObserver(onStatusChange).observe(status, {
        attributes: true,
        attributeFilter: ['hidden'],
        childList: true,
        characterData: true,
        subtree: true
      });
    }

    list.addEventListener('click', function (event) {
      var button = event.target && event.target.closest ? event.target.closest('[data-dlm-family-remove]') : null;
      if (!button || busy) return;
      var items = Array.prototype.slice.call(list.querySelectorAll('[data-dlm-family-remove]'));
      var index = items.indexOf(button);
      lines = removeLine(lines, button.getAttribute('data-dlm-family-remove'));
      showError('');
      renderList();
      sync();
      announce('');
      var remaining = list.querySelectorAll('[data-dlm-family-remove]');
      var focusTarget = remaining[Math.min(index, remaining.length - 1)] || (!chipBox.hidden && chipRow.firstChild) || (addAnother.hidden ? addButton : addAnother);
      if (focusTarget && typeof focusTarget.focus === 'function') focusTarget.focus();
    });

    function publish(eventName, data) {
      try {
        if (typeof win.publish === 'function' && win.PUB_SUB_EVENTS && win.PUB_SUB_EVENTS[eventName]) {
          win.publish(win.PUB_SUB_EVENTS[eventName], data);
        }
      } catch (error) {
        /* subscribers are optional */
      }
    }

    function submitAll() {
      var all = combineWithPending(lines, getPending());
      var unavailable = findUnavailable(all, variantsById);
      if (unavailable.length) {
        showError(t('soldOut', { item: unavailable[0].label }));
        return;
      }
      if (!all.length) return;

      busy = true;
      showError('');
      if (status) status.hidden = true;
      sync();

      var drawer = doc.querySelector('cart-drawer');
      var sectionIds = [];
      if (drawer && typeof drawer.getSectionsToRender === 'function') {
        drawer.getSectionsToRender().forEach(function (section) {
          sectionIds.push(section.id);
        });
        if (typeof drawer.setActiveElement === 'function') drawer.setActiveElement(doc.activeElement);
      }
      var config =
        typeof win.fetchConfig === 'function'
          ? win.fetchConfig('json')
          : { method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' } };
      config.headers = config.headers || {};
      config.headers['X-Requested-With'] = 'XMLHttpRequest';
      config.body = JSON.stringify(buildRequestBody(all, sectionIds, win.location.pathname));

      var responseOk = false;
      win
        .fetch(cartAddJsUrl(win.routes), config)
        .then(function (response) {
          responseOk = response.ok;
          return response.json();
        })
        .then(function (parsed) {
          if (!responseOk || !parsed || parsed.status) {
            var message = (parsed && (parsed.description || parsed.message)) || '';
            publish('cartError', { source: 'dlm-family-builder', errors: message, message: message });
            showError(typeof message === 'string' && message ? message : t('error'));
            return;
          }
          rememberAdded(
            all.map(function (line) {
              return line.roleKey;
            })
          );
          lines = [];
          renderList();
          busy = false;
          sync();
          clearCurrentSize();
          if (status) {
            status.textContent = successText;
            status.hidden = !successText;
          }
          announcer.textContent = successText;
          publish('cartUpdate', { source: 'dlm-family-builder', cartData: parsed });
          if (drawer && parsed.sections && typeof drawer.renderContents === 'function') {
            drawer.renderContents(parsed);
          } else {
            win.location.href = (win.routes && win.routes.cart_url) || '/cart';
          }
        })
        .catch(function (error) {
          showError(t('error'));
          if (win.console) win.console.error(error);
        })
        .then(function () {
          busy = false;
          sync();
        });
    }

    // Capture phase on the builder runs before the builder's own click
    // listener on the button (and before the sticky bar's forwarded
    // .click()), so with a non-empty list the whole list is added instead
    // of one piece. With an empty list the event passes through untouched.
    builder.addEventListener(
      'click',
      function (event) {
        var target = event.target && event.target.closest ? event.target.closest('[data-matching-set-add-button]') : null;
        if (target !== addButton) return;
        if (!lines.length) {
          // Single piece: the builder adds it; remember who it was for.
          var single = busy ? null : getPending();
          singleAddRole = single ? single.roleKey : '';
          return;
        }
        event.preventDefault();
        event.stopPropagation();
        if (event.stopImmediatePropagation) event.stopImmediatePropagation();
        if (!busy) submitAll();
      },
      true
    );

    sync();
    return true;
  }

  function autoStart(win) {
    var doc = win.document;

    function tryAll() {
      var pending = false;
      doc.querySelectorAll('[data-product-desktop-ux]').forEach(function (wrapper) {
        if (wrapper.hasAttribute('data-dlm-family-builder-mounted')) return;
        if (!mount(win, wrapper)) pending = true;
      });
      return pending;
    }

    function start() {
      if (!tryAll()) return;
      // The builder renders from another deferred script; wait for it.
      if (typeof win.MutationObserver !== 'function') return;
      var observer = new win.MutationObserver(function () {
        if (!tryAll()) observer.disconnect();
      });
      doc.querySelectorAll('[data-matching-set-builder]').forEach(function (builder) {
        observer.observe(builder, { attributes: true, attributeFilter: ['hidden'], childList: true, subtree: true });
      });
      win.setTimeout(function () {
        observer.disconnect();
      }, 15000);
    }

    if (doc.readyState === 'loading') doc.addEventListener('DOMContentLoaded', start);
    else start();
  }

  return {
    STRINGS: STRINGS,
    MAX_LINE_QTY: MAX_LINE_QTY,
    resolveLanguage: resolveLanguage,
    translate: translate,
    mergeLine: mergeLine,
    removeLine: removeLine,
    combineWithPending: combineWithPending,
    computeTotals: computeTotals,
    buildItems: buildItems,
    buildRequestBody: buildRequestBody,
    findUnavailable: findUnavailable,
    nextRoleKey: nextRoleKey,
    roleChips: roleChips,
    stripLeadingPlus: stripLeadingPlus,
    isAddSuccess: isAddSuccess,
    parseMoneyFormat: parseMoneyFormat,
    formatMoney: formatMoney,
    cartAddJsUrl: cartAddJsUrl,
    mount: mount,
    autoStart: autoStart
  };
});
