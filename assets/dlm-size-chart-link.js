/*
 * Visible size-guide text link for the PDP matching-set builder.
 *
 * Each builder card (rendered by product-desktop-ux-20260513-ruler-sync.js)
 * has only an icon-only ruler button (.product-matching-set__fit-icon). This
 * adds a small text link ("Size guide & fit", the localized
 * data-size-guide-single-label) to the card header, next to the role name and
 * right above the size pills. Clicking it clicks that card's ruler button, so
 * the existing inline fit panel and size chart open exactly as before.
 * Cards are re-rendered with innerHTML, so a MutationObserver re-adds links.
 */
(function () {
  'use strict';

  var CARD = '[data-instance-card]';
  var HEADER = '.product-matching-set__card-header';
  var ICON = '[data-pdp-fit-inline-trigger]';
  var LINK_ATTR = 'data-dlm-size-chart-link';
  var FALLBACK_LABEL = 'Size guide & fit';

  function labelFor(card) {
    var wrapper = card.closest('[data-size-guide-single-label]') || document.querySelector('[data-size-guide-single-label]');
    var label = wrapper ? String(wrapper.getAttribute('data-size-guide-single-label') || '').trim() : '';
    if (!label || /translation missing/i.test(label)) label = FALLBACK_LABEL;
    return label;
  }

  function addLink(card) {
    var header = card.querySelector(HEADER);
    var icon = card.querySelector(ICON);
    if (!header || !icon || header.querySelector('[' + LINK_ATTR + ']')) return;
    var link = document.createElement('button');
    link.type = 'button';
    link.className = 'dlm-size-chart-link';
    link.setAttribute(LINK_ATTR, '');
    var controls = icon.getAttribute('aria-controls');
    if (controls) link.setAttribute('aria-controls', controls);
    link.textContent = labelFor(card);
    header.appendChild(link);
  }

  function scan(root) {
    Array.prototype.forEach.call((root || document).querySelectorAll(CARD), addLink);
  }

  document.addEventListener('click', function (event) {
    var link = event.target && event.target.closest ? event.target.closest('[' + LINK_ATTR + ']') : null;
    if (!link) return;
    var card = link.closest(CARD);
    var icon = card ? card.querySelector(ICON) : null;
    if (!icon) return;
    event.preventDefault();
    icon.click();
  });

  function start() {
    var builders = document.querySelectorAll('.product-matching-set');
    if (!builders.length) return;
    scan(document);
    if (typeof MutationObserver !== 'function') return;
    var observer = new MutationObserver(function () {
      scan(document);
    });
    Array.prototype.forEach.call(builders, function (builder) {
      observer.observe(builder, { childList: true, subtree: true });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start);
  } else {
    start();
  }
})();
