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
  initMatchingSizeGuide(wrapper);
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

function normalizeText(value) {
  return String(value || '')
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

var SIZE_LABEL_PATTERN = /\b(size|sizes|talla|tallas|taille|tailles|tamano|tamaño|pointure|pointures)\b/;
var TYPE_LABEL_PATTERN = /\b(type|style)\b/;
var ROLE_PATTERNS = [
  { key: 'mother', label: 'Mother', regex: /^(mother|mom)\b/i },
  { key: 'father', label: 'Father', regex: /^(father|dad)\b/i },
  { key: 'girl', label: 'Girl', regex: /^(girl|daughter)\b/i },
  { key: 'boy', label: 'Boy', regex: /^(boy|son)\b/i },
  { key: 'child', label: 'Child', regex: /^child\b/i },
  { key: 'baby', label: 'Baby', regex: /^baby\b/i },
  { key: 'adult', label: 'Adult', regex: /^adult\b/i },
];

function findSizeOptionIndex(options) {
  if (!Array.isArray(options)) return -1;

  for (var index = 0; index < options.length; index += 1) {
    if (SIZE_LABEL_PATTERN.test(normalizeText(options[index].name))) {
      return index;
    }
  }

  return -1;
}

function parseRoleFromSizeLabel(label) {
  var text = String(label || '').trim();
  if (!text) return null;

  for (var index = 0; index < ROLE_PATTERNS.length; index += 1) {
    var pattern = ROLE_PATTERNS[index];
    var match = text.match(pattern.regex);
    if (!match) continue;

    var sizeLabel = text.replace(pattern.regex, '').trim();
    return {
      key: pattern.key,
      label: pattern.label,
      sizeLabel: sizeLabel || text,
      fullLabel: text,
    };
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
      if (TYPE_LABEL_PATTERN.test(optionName)) continue;

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
    if (!TYPE_LABEL_PATTERN.test(optionName)) continue;

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

function initMatchingSizeGuide(wrapper) {
  var details = wrapper.querySelector('[data-matching-size-guide]');
  var content = wrapper.querySelector('[data-matching-size-guide-content]');
  var sizeTable = document.querySelector('table#size-chart, table[id*="size-chart"]');
  if (!details || !content || !sizeTable) return;

  var parsed = parseSizeGuideTable(sizeTable);
  if (!parsed) return;

  var groups = buildSizeGuideGroups(parsed);
  if (groups.length < 2) return;

  content.innerHTML =
    '<div class="matching-size-guide__grid">' +
    groups
      .map(function (group) {
        return (
          '<article class="matching-size-guide__card">' +
          '<h3>' +
          escapeHtml(group.label) +
          '</h3>' +
          '<div class="matching-size-guide__table-wrap">' +
          '<table class="matching-size-guide__table">' +
          '<thead><tr>' +
          group.headers
            .map(function (header) {
              return '<th>' + escapeHtml(header) + '</th>';
            })
            .join('') +
          '</tr></thead>' +
          '<tbody>' +
          group.rows
            .map(function (row) {
              return (
                '<tr>' +
                row
                  .map(function (cell) {
                    return '<td>' + escapeHtml(cell) + '</td>';
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
      })
      .join('') +
    '</div>';
  details.removeAttribute('hidden');
}

function parseSizeGuideTable(table) {
  var rows = Array.from(table.querySelectorAll('tr'));
  if (rows.length < 2) return null;

  var headers = Array.from(rows[0].querySelectorAll('th, td')).map(function (cell) {
    return cellText(cell);
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

  return {
    headers: headers,
    rows: bodyRows,
  };
}

function cellText(cell) {
  return String(cell && cell.textContent ? cell.textContent : '')
    .replace(/\s+/g, ' ')
    .trim();
}

function parseRoleFromHeader(header) {
  var cleaned = String(header || '')
    .replace(/\s*\(.+?\)\s*$/, '')
    .trim();

  if (!cleaned) return null;

  if (/^dad shirt\b/i.test(cleaned)) {
    return {
      key: 'father',
      label: 'Father',
      measurement: cleaned.replace(/^dad shirt\b/i, '').trim(),
    };
  }

  if (/^mom dress\b/i.test(cleaned)) {
    return {
      key: 'mother',
      label: 'Mother',
      measurement: cleaned.replace(/^mom dress\b/i, '').trim(),
    };
  }

  if (/^son shirt\b/i.test(cleaned)) {
    return {
      key: 'boy',
      label: 'Boy',
      measurement: cleaned.replace(/^son shirt\b/i, '').trim(),
    };
  }

  if (/^daughter dress\b/i.test(cleaned)) {
    return {
      key: 'girl',
      label: 'Girl',
      measurement: cleaned.replace(/^daughter dress\b/i, '').trim(),
    };
  }

  for (var index = 0; index < ROLE_PATTERNS.length; index += 1) {
    var rolePattern = ROLE_PATTERNS[index];
    if (!rolePattern.regex.test(cleaned)) continue;

    var measurement = cleaned.replace(rolePattern.regex, '').trim();
    if (!measurement) return null;

    return {
      key: rolePattern.key,
      label: rolePattern.label,
      measurement: measurement,
    };
  }

  return null;
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
    });

  if (groupedRows.length > 1) return groupedRows;

  var heightIndex = parsed.headers.findIndex(function (header) {
    return normalizeText(header).indexOf('height') === 0;
  });
  var groupedHeaders = {};

  parsed.headers.forEach(function (header, index) {
    if (index === 0 || index === heightIndex) return;
    var roleHeader = parseRoleFromHeader(header);
    if (!roleHeader) return;

    if (!groupedHeaders[roleHeader.key]) {
      groupedHeaders[roleHeader.key] = {
        label: roleHeader.label,
        headers: [parsed.headers[0]],
        columnIndexes: [],
      };
      if (heightIndex > -1) groupedHeaders[roleHeader.key].headers.push(parsed.headers[heightIndex]);
    }

    groupedHeaders[roleHeader.key].headers.push(roleHeader.measurement);
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
            return value && value !== '—';
          });
        });

      return {
        key: key,
        label: group.label,
        headers: group.headers,
        rows: rows,
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
  return SIZE_LABEL_PATTERN.test(normalizeText(optionName));
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
