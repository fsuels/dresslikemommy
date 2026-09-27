/*
  Dress Like Mommy: collection "Show more" loading.

  Progressive enhancement over Shopify pagination. The "Show more" and
  "Previous page" controls are real ?page=N links (crawlable, work without JS;
  numbered pagination is a <noscript> fallback). With JS the next page is
  fetched through the Section Rendering API and its grid items are appended to
  #product-grid. The URL is never rewritten; the loaded page range lives in
  sessionStorage keyed by the URL without `page`.

  Works after facets.js swaps #ProductGridContainer (state lives on the
  [data-dlm-load-more] element, which is re-rendered with every swap), and
  restores loaded pages + scroll position when a shopper comes back from a
  product page without bfcache (or reloads).
*/
(() => {
  if (window.DLMCollectionLoadMore) return;

  const ROOT_SELECTOR = '[data-dlm-load-more]';
  const BUTTON_SELECTOR = '[data-dlm-load-more-button]';
  const STORAGE_KEY = 'dlm:collection-load-more';
  const MAX_PAGES = 10;
  const MAX_AGE_MS = 30 * 60 * 1000;
  // Pages can render 0 cards (cards are hidden after pagination); skip at most this many in a row.
  const MAX_EMPTY_SKIPS = 3;
  const ANIMATION_CLASSES = ['scroll-trigger', 'animate--slide-in', 'animate--fade-in', 'scroll-trigger--offscreen'];

  let busy = false;
  // Bumped whenever facets.js replaces the grid; results from older fetches are discarded.
  let generation = 0;
  let lastClickedKey = '';

  const getRoot = () => document.querySelector(ROOT_SELECTOR);
  const getGrid = () => document.getElementById('product-grid');

  function toInt(value, fallback) {
    const parsed = parseInt(value, 10);
    return Number.isFinite(parsed) ? parsed : fallback;
  }

  function readRange(root) {
    return {
      first: toInt(root.dataset.firstPage, 1),
      last: toInt(root.dataset.lastPage, 1),
      total: toInt(root.dataset.totalPages, 1),
    };
  }

  function stateKey() {
    const url = new URL(window.location.href);
    url.searchParams.delete('page');
    url.searchParams.delete('section_id');
    url.searchParams.sort();
    return url.pathname + url.search;
  }

  function pageUrl(page, forSection) {
    const url = new URL(window.location.href);
    url.hash = '';
    url.searchParams.delete('section_id');
    if (page > 1) {
      url.searchParams.set('page', String(page));
    } else {
      url.searchParams.delete('page');
    }
    if (forSection) {
      const grid = getGrid();
      if (grid && grid.dataset.id) url.searchParams.set('section_id', grid.dataset.id);
    }
    return url;
  }

  function cleanHref(href) {
    const url = new URL(href, window.location.href);
    url.searchParams.delete('section_id');
    return url.pathname + url.search;
  }

  function fetchPage(page) {
    return fetch(pageUrl(page, true).toString(), { credentials: 'same-origin' })
      .then((response) => {
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        return response.text();
      })
      .then((html) => {
        const doc = new DOMParser().parseFromString(html, 'text/html');
        if (!doc.getElementById('product-grid')) throw new Error('Missing product grid');
        return doc;
      });
  }

  // Stable product key for a grid item: analytics handle, else product URL path.
  function itemKey(element) {
    if (!element) return '';
    const card = element.matches('[data-analytics-product-card]')
      ? element
      : element.querySelector('[data-analytics-product-card]');
    const handle = card && card.getAttribute('data-analytics-handle');
    if (handle) return `h:${handle}`;
    const link = element.querySelector('a[href*="/products/"]');
    if (!link) return '';
    try {
      return `p:${new URL(link.getAttribute('href'), window.location.href).pathname}`;
    } catch (_error) {
      return '';
    }
  }

  function gridKeys(grid) {
    const keys = new Set();
    grid.querySelectorAll(':scope > li').forEach((item) => {
      const key = itemKey(item);
      if (key) keys.add(key);
    });
    return keys;
  }

  // Imports a fetched page's items, skipping products already in the grid
  // (newest-first collections shift when a product is published between loads).
  function importItems(doc, seenKeys) {
    const fragment = document.createDocumentFragment();
    doc.querySelectorAll('#product-grid > li').forEach((item) => {
      const key = itemKey(item);
      if (key && seenKeys.has(key)) return;
      if (key) seenKeys.add(key);

      const node = document.importNode(item, true);
      // Appended items are already in view context; skip reveal-on-scroll so they never stay hidden.
      ANIMATION_CLASSES.forEach((className) => node.classList.remove(className));
      node.removeAttribute('data-cascade');
      node.style.removeProperty('--animation-order');
      if (!node.getAttribute('style')) node.removeAttribute('style');
      fragment.appendChild(node);
    });
    return fragment;
  }

  function countItems(doc) {
    return doc.querySelectorAll('#product-grid > li').length;
  }

  // Running totals of rendered vs expected cards across every loaded page.
  function readTally(root) {
    return {
      rendered: toInt(root.dataset.renderedTotal, toInt(root.dataset.renderedCount, 0)),
      expected: toInt(root.dataset.expectedTotal, toInt(root.dataset.expectedCount, 0)),
    };
  }

  function addToTally(root, doc) {
    const source = doc.querySelector(ROOT_SELECTOR);
    const tally = readTally(root);
    tally.rendered += countItems(doc);
    tally.expected += source ? toInt(source.dataset.expectedCount, 0) : 0;
    root.dataset.renderedTotal = String(tally.rendered);
    root.dataset.expectedTotal = String(tally.expected);
  }

  // Copies text, percentages, label and next link from the newest loaded page.
  function syncFromSource(root, doc) {
    const source = doc.querySelector(ROOT_SELECTOR);
    const button = root.querySelector(BUTTON_SELECTOR);
    if (!source) {
      if (button) button.remove();
      return;
    }

    ['countPercent', 'pagePercent', 'pageLabel'].forEach((key) => {
      if (source.dataset[key] !== undefined) root.dataset[key] = source.dataset[key];
    });

    const text = root.querySelector('[data-dlm-progress-text]');
    const sourceText = source.querySelector('[data-dlm-progress-text]');
    if (text && sourceText) text.textContent = sourceText.textContent.trim();

    const sourceButton = source.querySelector(BUTTON_SELECTOR);
    if (button) {
      if (sourceButton) {
        button.setAttribute('href', cleanHref(sourceButton.getAttribute('href')));
      } else {
        button.remove();
      }
    }
  }

  // "X of Y" only when every loaded page rendered its full expected count;
  // otherwise just the bar (pages loaded / total pages) and the button.
  function renderProgress(root) {
    const tally = readTally(root);
    const exact = tally.expected > 0 && tally.rendered === tally.expected;
    const text = root.querySelector('[data-dlm-progress-text]');
    if (text) text.hidden = !exact;

    const percent = exact ? root.dataset.countPercent : root.dataset.pagePercent;
    const fill = root.querySelector('[data-dlm-progress-fill]');
    if (fill) fill.style.setProperty('--dlm-progress', `${Math.min(100, toInt(percent, 0))}%`);

    if (!root.querySelector(BUTTON_SELECTOR)) root.classList.add('is-complete');
    return exact && text ? text.textContent : root.dataset.pageLabel || '';
  }

  // Fetches from startPage on, skipping forward over pages that rendered no cards.
  async function fetchFrom(startPage, totalPages) {
    const results = [];
    let page = startPage;
    let skips = 0;
    while (page <= totalPages) {
      const doc = await fetchPage(page);
      results.push({ page, doc });
      if (countItems(doc) > 0 || !doc.querySelector(ROOT_SELECTOR)) break;
      if (page >= totalPages || skips >= MAX_EMPTY_SKIPS) break;
      skips += 1;
      page += 1;
    }
    return results;
  }

  function syncPrevious(first) {
    const previous = document.querySelector('[data-dlm-load-previous]');
    if (!previous) return;
    if (first <= 1) {
      previous.remove();
      return;
    }
    const link = previous.querySelector('a');
    if (link) {
      const url = pageUrl(first - 1, false);
      link.setAttribute('href', url.pathname + url.search);
    }
  }

  function announce(root, message) {
    const status = root.querySelector('[data-dlm-load-more-status]');
    if (!status || !message) return;
    status.textContent = '';
    window.setTimeout(() => {
      status.textContent = message;
    }, 50);
  }

  function focusFirst(items) {
    // Wait a frame so observers (e.g. the daddy-me card filter) can hide items first.
    window.requestAnimationFrame(() => {
      const first = items.find((item) => item.isConnected && !item.hidden);
      if (!first) return;
      const target = first.querySelector('a[href]:not([tabindex="-1"])');
      if (target) target.focus({ preventScroll: true });
    });
  }

  function focusLastCard(grid) {
    const items = Array.from(grid.querySelectorAll(':scope > li')).filter((item) => !item.hidden);
    const last = items[items.length - 1];
    const target = last && last.querySelector('a[href]:not([tabindex="-1"])');
    if (target) target.focus({ preventScroll: true });
  }

  function withInstantScroll(callback) {
    // html has scroll-behavior: smooth; restoring position must be instant.
    const rootStyle = document.documentElement.style;
    const previous = rootStyle.scrollBehavior;
    rootStyle.scrollBehavior = 'auto';
    callback();
    rootStyle.scrollBehavior = previous;
  }

  function setLoading(root, loading) {
    const button = root.querySelector(BUTTON_SELECTOR);
    root.classList.toggle('is-loading', loading);
    if (!button) return;
    if (loading) {
      button.setAttribute('aria-disabled', 'true');
      button.setAttribute('aria-busy', 'true');
    } else {
      button.removeAttribute('aria-disabled');
      button.removeAttribute('aria-busy');
    }
  }

  function loadNext(button, options = {}) {
    const root = button.closest(ROOT_SELECTOR);
    const grid = getGrid();
    if (!root || !grid || busy) return;

    const range = readRange(root);
    const nextPage = range.last + 1;
    if (nextPage > range.total) return;

    const startGeneration = generation;
    busy = true;
    setLoading(root, true);

    fetchFrom(nextPage, range.total)
      .then((results) => {
        // A facets.js swap replaced the grid while we were fetching: discard.
        if (startGeneration !== generation || !root.isConnected || getGrid() !== grid) return;

        const seenKeys = gridKeys(grid);
        const items = [];
        results.forEach(({ doc }) => {
          const fragment = importItems(doc, seenKeys);
          items.push(...Array.from(fragment.children));
          grid.appendChild(fragment);
          addToTally(root, doc);
        });

        const lastLoaded = results[results.length - 1];
        root.dataset.lastPage = String(lastLoaded.page);
        syncFromSource(root, lastLoaded.doc);
        const message = renderProgress(root);
        setLoading(root, false);

        const hasMore = Boolean(root.querySelector(BUTTON_SELECTOR));
        if (!items.length && !hasMore) {
          // Trailing pages were all empty: nothing more to show.
          root.hidden = true;
          if (!options.auto) window.requestAnimationFrame(() => focusLastCard(grid));
          return;
        }

        if (items.length) announce(root, message);
        if (!options.auto) {
          if (items.length) {
            focusFirst(items);
          } else {
            button.focus({ preventScroll: true });
          }
        }
      })
      .catch(() => {
        // Fall back to a normal page navigation (only for a live, user-initiated click).
        if (!options.auto && startGeneration === generation && button.isConnected) {
          window.location.assign(cleanHref(button.getAttribute('href')));
        }
      })
      .finally(() => {
        busy = false;
        if (root.isConnected) setLoading(root, false);
        // A swap during the fetch may have produced an empty first page that still needs checking.
        skipEmptyRenderedPage();
      });
  }

  function onClick(event) {
    const button = event.target.closest && event.target.closest(BUTTON_SELECTOR);
    if (!button) return;
    if (event.defaultPrevented || event.button !== 0) return;
    if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;

    event.preventDefault();
    loadNext(button);
  }

  function saveState() {
    const root = getRoot();
    let storage;
    try {
      storage = window.sessionStorage;
    } catch (_error) {
      return;
    }
    if (!storage) return;

    try {
      if (!root) {
        storage.removeItem(STORAGE_KEY);
        return;
      }
      const range = readRange(root);
      if (range.last <= range.first) {
        storage.removeItem(STORAGE_KEY);
        return;
      }
      storage.setItem(
        STORAGE_KEY,
        JSON.stringify({
          key: stateKey(),
          first: range.first,
          last: range.last,
          scrollY: Math.round(window.scrollY || window.pageYOffset || 0),
          anchor: lastClickedKey,
          ts: Date.now(),
        })
      );
    } catch (_error) {
      // Storage full or blocked; restoring is best effort only.
    }
  }

  function onGridLinkClick(event) {
    const link = event.target.closest && event.target.closest('a[href]');
    if (!link || !link.closest('#product-grid')) return;
    lastClickedKey = itemKey(link.closest('#product-grid > li')) || '';
    saveState();
  }

  function readSavedState() {
    try {
      const raw = window.sessionStorage.getItem(STORAGE_KEY);
      return raw ? JSON.parse(raw) : null;
    } catch (_error) {
      return null;
    }
  }

  function navigationType() {
    try {
      const entry = performance.getEntriesByType('navigation')[0];
      if (entry && entry.type) return entry.type;
    } catch (_error) {
      // Fall through to the legacy API.
    }
    if (performance.navigation) {
      if (performance.navigation.type === 2) return 'back_forward';
      if (performance.navigation.type === 1) return 'reload';
    }
    return 'navigate';
  }

  function restoreScroll(grid, saved, pagesDropped) {
    if (!pagesDropped) {
      const targetY = toInt(saved.scrollY, 0);
      withInstantScroll(() => window.scrollTo(0, targetY));
      return;
    }
    // Some saved pages were not restored: only jump if the clicked card is present.
    if (!saved.anchor) return;
    const item = Array.from(grid.querySelectorAll(':scope > li')).find((li) => itemKey(li) === saved.anchor);
    if (item) withInstantScroll(() => item.scrollIntoView({ block: 'center' }));
  }

  function restore() {
    const root = getRoot();
    const grid = getGrid();
    if (!root || !grid) return;

    const navType = navigationType();
    if (navType !== 'back_forward' && navType !== 'reload') return;

    const saved = readSavedState();
    if (!saved || saved.key !== stateKey()) return;
    if (typeof saved.ts !== 'number' || Date.now() - saved.ts > MAX_AGE_MS) return;

    const range = readRange(root);
    const rendered = range.first;
    const last = Math.min(toInt(saved.last, rendered), range.total);
    const savedFirst = Math.max(1, toInt(saved.first, rendered));
    let first = savedFirst;
    if (last - first + 1 > MAX_PAGES) first = last - MAX_PAGES + 1;
    const pagesDropped = first !== savedFirst || last !== toInt(saved.last, last);
    if (rendered < first || rendered > last) return;
    if (first === rendered && last === rendered) return;

    const pages = [];
    for (let page = first; page <= last; page += 1) {
      if (page !== rendered) pages.push(page);
    }

    const startGeneration = generation;
    busy = true;
    setLoading(root, true);

    Promise.all(pages.map((page) => fetchPage(page).then((doc) => ({ page, doc }))))
      .then((results) => {
        if (startGeneration !== generation || !root.isConnected || getGrid() !== grid) return;

        const seenKeys = gridKeys(grid);
        const before = document.createDocumentFragment();
        const after = document.createDocumentFragment();
        let lastDoc = null;
        results
          .sort((a, b) => a.page - b.page)
          .forEach(({ page, doc }) => {
            const fragment = importItems(doc, seenKeys);
            addToTally(root, doc);
            if (page < rendered) {
              before.appendChild(fragment);
            } else {
              after.appendChild(fragment);
              lastDoc = doc;
            }
          });

        grid.insertBefore(before, grid.firstChild);
        grid.appendChild(after);

        root.dataset.firstPage = String(first);
        root.dataset.lastPage = String(last);
        root.dataset.emptyChecked = 'true';
        if (lastDoc) syncFromSource(root, lastDoc);
        renderProgress(root);
        syncPrevious(first);

        window.requestAnimationFrame(() => restoreScroll(grid, saved, pagesDropped));
      })
      .catch(() => {
        // Keep the server-rendered page as-is if any page fails to load.
      })
      .finally(() => {
        busy = false;
        if (root.isConnected) setLoading(root, false);
        skipEmptyRenderedPage();
      });
  }

  // If the server-rendered page itself shows no cards, pull in the next non-empty page (once per grid).
  function skipEmptyRenderedPage() {
    const root = getRoot();
    if (!root || busy || root.dataset.emptyChecked) return;
    if (toInt(root.dataset.renderedCount, 1) > 0) return;
    root.dataset.emptyChecked = 'true';
    const button = root.querySelector(BUTTON_SELECTOR);
    if (button) loadNext(button, { auto: true });
  }

  function init() {
    restore();
    skipEmptyRenderedPage();

    // facets.js replaces #ProductGridContainer's children on filter/sort changes.
    const container = document.getElementById('ProductGridContainer');
    if (container && 'MutationObserver' in window) {
      new MutationObserver(() => {
        generation += 1;
        skipEmptyRenderedPage();
      }).observe(container, { childList: true });
    }
  }

  document.addEventListener('click', onClick);
  document.addEventListener('click', onGridLinkClick, true);
  window.addEventListener('pagehide', saveState);

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init, { once: true });
  } else {
    init();
  }

  window.DLMCollectionLoadMore = { restore, saveState };
})();
