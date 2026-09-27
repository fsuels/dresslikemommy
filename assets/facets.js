class FacetFiltersForm extends HTMLElement {
  constructor() {
    super();
    this.onActiveFilterClick = this.onActiveFilterClick.bind(this);

    this.debouncedOnSubmit = debounce((event) => {
      this.onSubmitHandler(event);
    }, 800);

    const facetForm = this.querySelector('form');
    facetForm.addEventListener('input', this.debouncedOnSubmit.bind(this));

    const facetWrapper = this.querySelector('#FacetsWrapperDesktop');
    if (facetWrapper) facetWrapper.addEventListener('keyup', onKeyUpEscape);
  }

  static setListeners() {
    const onHistoryChange = (event) => {
      const searchParams = event.state ? event.state.searchParams : FacetFiltersForm.searchParamsInitial;
      if (searchParams === FacetFiltersForm.searchParamsPrev) return;
      FacetFiltersForm.renderPage(searchParams, null, false);
    };
    window.addEventListener('popstate', onHistoryChange);
  }

  static toggleActiveFacets(disable = true) {
    document.querySelectorAll('.js-facet-remove').forEach((element) => {
      element.classList.toggle('disabled', disable);
    });
  }

  static renderPage(searchParams, event, updateURLHash = true) {
    FacetFiltersForm.searchParamsPrev = searchParams;
    const sections = FacetFiltersForm.getSections();
    const countContainer = document.getElementById('ProductCount');
    const countContainerDesktop = document.getElementById('ProductCountDesktop');
    const loadingSpinners = document.querySelectorAll(
      '.facets-container .loading__spinner, facet-filters-form .loading__spinner'
    );
    loadingSpinners.forEach((spinner) => spinner.classList.remove('hidden'));
    document.getElementById('ProductGridContainer').querySelector('.collection').classList.add('loading');
    if (countContainer) {
      countContainer.classList.add('loading');
    }
    if (countContainerDesktop) {
      countContainerDesktop.classList.add('loading');
    }
    FacetFiltersForm.toggleLiveCountLoading(true);

    sections.forEach((section) => {
      const url = `${window.location.pathname}?section_id=${section.section}&${searchParams}`;
      const filterDataUrl = (element) => element.url === url;

      FacetFiltersForm.filterData.some(filterDataUrl)
        ? FacetFiltersForm.renderSectionFromCache(filterDataUrl, event)
        : FacetFiltersForm.renderSectionFromFetch(url, event);
    });

    if (updateURLHash) FacetFiltersForm.updateURLHash(searchParams);
  }

  static renderSectionFromFetch(url, event) {
    fetch(url)
      .then((response) => response.text())
      .then((responseText) => {
        const html = responseText;
        FacetFiltersForm.filterData = [...FacetFiltersForm.filterData, { html, url }];
        FacetFiltersForm.renderFilters(html, event);
        FacetFiltersForm.renderProductGridContainer(html);
        FacetFiltersForm.renderProductCount(html);
        if (typeof initializeScrollAnimationTrigger === 'function') initializeScrollAnimationTrigger(html.innerHTML);
      });
  }

  static renderSectionFromCache(filterDataUrl, event) {
    const html = FacetFiltersForm.filterData.find(filterDataUrl).html;
    FacetFiltersForm.renderFilters(html, event);
    FacetFiltersForm.renderProductGridContainer(html);
    FacetFiltersForm.renderProductCount(html);
    if (typeof initializeScrollAnimationTrigger === 'function') initializeScrollAnimationTrigger(html.innerHTML);
  }

  static renderProductGridContainer(html) {
    document.getElementById('ProductGridContainer').innerHTML = new DOMParser()
      .parseFromString(html, 'text/html')
      .getElementById('ProductGridContainer').innerHTML;

    document
      .getElementById('ProductGridContainer')
      .querySelectorAll('.scroll-trigger')
      .forEach((element) => {
        element.classList.add('scroll-trigger--cancel');
      });
  }

  static renderProductCount(html) {
    const count = new DOMParser().parseFromString(html, 'text/html').getElementById('ProductCount').innerHTML;
    const container = document.getElementById('ProductCount');
    const containerDesktop = document.getElementById('ProductCountDesktop');
    container.innerHTML = count;
    container.classList.remove('loading');
    if (containerDesktop) {
      containerDesktop.innerHTML = count;
      containerDesktop.classList.remove('loading');
    }
    const loadingSpinners = document.querySelectorAll(
      '.facets-container .loading__spinner, facet-filters-form .loading__spinner'
    );
    loadingSpinners.forEach((spinner) => spinner.classList.add('hidden'));
    FacetFiltersForm.toggleLiveCountLoading(false);
  }

  static toggleLiveCountLoading(isLoading) {
    document.querySelectorAll('.dlm-facets-live-count').forEach((element) => {
      element.classList.toggle('is-loading', isLoading);
    });
  }

  static renderFilters(html, event) {
    const parsedHTML = new DOMParser().parseFromString(html, 'text/html');
    const facetDetailsElementsFromFetch = parsedHTML.querySelectorAll(
      '#FacetFiltersForm .js-filter, #FacetFiltersFormMobile .js-filter, #FacetFiltersPillsForm .js-filter'
    );
    const facetDetailsElementsFromDom = document.querySelectorAll(
      '#FacetFiltersForm .js-filter, #FacetFiltersFormMobile .js-filter, #FacetFiltersPillsForm .js-filter'
    );

    // Remove facets that are no longer returned from the server
    Array.from(facetDetailsElementsFromDom).forEach((currentElement) => {
      if (!Array.from(facetDetailsElementsFromFetch).some(({ id }) => currentElement.id === id)) {
        currentElement.remove();
      }
    });

    const matchesId = (element) => {
      const jsFilter = event ? event.target.closest('.js-filter') : undefined;
      return jsFilter ? element.id === jsFilter.id : false;
    };

    const facetsToRender = Array.from(facetDetailsElementsFromFetch).filter((element) => !matchesId(element));
    const countsToRender = Array.from(facetDetailsElementsFromFetch).find(matchesId);

    facetsToRender.forEach((elementToRender, index) => {
      const currentElement = document.getElementById(elementToRender.id);
      // Element already rendered in the DOM so just update the innerHTML
      if (currentElement) {
        document.getElementById(elementToRender.id).innerHTML = elementToRender.innerHTML;
      } else {
        if (index > 0) {
          const { className: previousElementClassName, id: previousElementId } = facetsToRender[index - 1];
          // Same facet type (eg horizontal/vertical or drawer/mobile)
          if (elementToRender.className === previousElementClassName) {
            document.getElementById(previousElementId).after(elementToRender);
            return;
          }
        }

        if (elementToRender.parentElement) {
          document.querySelector(`#${elementToRender.parentElement.id} .js-filter`).before(elementToRender);
        }
      }
    });

    FacetFiltersForm.renderActiveFacets(parsedHTML);
    FacetFiltersForm.renderAdditionalElements(parsedHTML);

    if (countsToRender) {
      const closestJSFilterID = event.target.closest('.js-filter').id;

      if (closestJSFilterID) {
        FacetFiltersForm.renderCounts(countsToRender, event.target.closest('.js-filter'));
        FacetFiltersForm.renderMobileCounts(countsToRender, document.getElementById(closestJSFilterID));

        const newFacetDetailsElement = document.getElementById(closestJSFilterID);
        const newElementSelector = newFacetDetailsElement.classList.contains('mobile-facets__details')
          ? `.mobile-facets__close-button`
          : `.facets__summary`;
        const newElementToActivate = newFacetDetailsElement.querySelector(newElementSelector);

        const isTextInput = event.target.getAttribute('type') === 'text';

        if (newElementToActivate && !isTextInput) newElementToActivate.focus();
      }
    }

    FacetFiltersForm.syncSortControls();
  }

  // Keeps the mobile quick-sort proxy and the visible sort names in step with the real sort selects.
  static syncSortControls() {
    const sourceSelect = document.getElementById('SortBy-mobile') || document.getElementById('SortBy');
    document.querySelectorAll('[data-dlm-sort-proxy]').forEach((proxy) => {
      if (sourceSelect && proxy.value !== sourceSelect.value) proxy.value = sourceSelect.value;
    });
    document.querySelectorAll('[data-dlm-sort]').forEach(FacetFiltersForm.updateSortName);
  }

  static updateSortName(wrapper) {
    const select = wrapper.querySelector('select');
    const nameElement = wrapper.querySelector('.dlm-facets__sort-current');
    if (!select || !nameElement || select.selectedIndex < 0) return;
    nameElement.textContent = select.options[select.selectedIndex].textContent.trim();
  }

  static renderActiveFacets(html) {
    const activeFacetElementSelectors = ['.active-facets-mobile', '.active-facets-desktop'];

    activeFacetElementSelectors.forEach((selector) => {
      const activeFacetsElement = html.querySelector(selector);
      if (!activeFacetsElement) return;
      document.querySelector(selector).innerHTML = activeFacetsElement.innerHTML;
    });

    FacetFiltersForm.toggleActiveFacets(false);
  }

  static renderAdditionalElements(html) {
    const mobileElementSelectors = ['.mobile-facets__open', '.mobile-facets__count', '.sorting'];

    mobileElementSelectors.forEach((selector) => {
      if (!html.querySelector(selector)) return;
      document.querySelector(selector).innerHTML = html.querySelector(selector).innerHTML;
    });

    // The Filter button's active state lives on the element itself, not its innerHTML.
    const openButtonSource = html.querySelector('.mobile-facets__open');
    const openButtonTarget = document.querySelector('.mobile-facets__open');
    if (openButtonSource && openButtonTarget) openButtonTarget.className = openButtonSource.className;

    const liveCount = html.querySelector('.dlm-facets-live-count');
    if (liveCount) {
      document.querySelectorAll('.dlm-facets-live-count').forEach((element) => {
        element.innerHTML = liveCount.innerHTML;
      });
    }

    document.getElementById('FacetFiltersFormMobile').closest('menu-drawer').bindEvents();
  }

  static renderCounts(source, target) {
    const targetSummary = target.querySelector('.facets__summary');
    const sourceSummary = source.querySelector('.facets__summary');

    if (sourceSummary && targetSummary) {
      targetSummary.outerHTML = sourceSummary.outerHTML;
    }

    const targetHeaderElement = target.querySelector('.facets__header');
    const sourceHeaderElement = source.querySelector('.facets__header');

    if (sourceHeaderElement && targetHeaderElement) {
      targetHeaderElement.outerHTML = sourceHeaderElement.outerHTML;
    }

    const targetWrapElement = target.querySelector('.facets-wrap');
    const sourceWrapElement = source.querySelector('.facets-wrap');

    if (sourceWrapElement && targetWrapElement) {
      const isShowingMore = Boolean(target.querySelector('show-more-button .label-show-more.hidden'));
      if (isShowingMore) {
        sourceWrapElement
          .querySelectorAll('.facets__item.hidden')
          .forEach((hiddenItem) => hiddenItem.classList.replace('hidden', 'show-more-item'));
      }

      targetWrapElement.outerHTML = sourceWrapElement.outerHTML;
    }
  }

  static renderMobileCounts(source, target) {
    const targetFacetsList = target.querySelector('.mobile-facets__list');
    const sourceFacetsList = source.querySelector('.mobile-facets__list');

    if (sourceFacetsList && targetFacetsList) {
      targetFacetsList.outerHTML = sourceFacetsList.outerHTML;
    }

    const targetSummaryMeta = target.querySelector('.dlm-facets__summary-meta');
    const sourceSummaryMeta = source.querySelector('.dlm-facets__summary-meta');

    if (sourceSummaryMeta && targetSummaryMeta) {
      targetSummaryMeta.innerHTML = sourceSummaryMeta.innerHTML;
    }
  }

  static updateURLHash(searchParams) {
    history.pushState({ searchParams }, '', `${window.location.pathname}${searchParams && '?'.concat(searchParams)}`);
  }

  static getSections() {
    return [
      {
        section: document.getElementById('product-grid').dataset.id,
      },
    ];
  }

  createSearchParams(form) {
    const formData = new FormData(form);
    return new URLSearchParams(formData).toString();
  }

  onSubmitForm(searchParams, event) {
    FacetFiltersForm.renderPage(searchParams, event);
  }

  onSubmitHandler(event) {
    event.preventDefault();
    const sortFilterForms = document.querySelectorAll('facet-filters-form form');
    if (event.srcElement.className == 'mobile-facets__checkbox') {
      const searchParams = this.createSearchParams(event.target.closest('form'));
      this.onSubmitForm(searchParams, event);
    } else {
      const forms = [];
      const isMobile = event.target.closest('form').id === 'FacetFiltersFormMobile';

      sortFilterForms.forEach((form) => {
        if (!isMobile) {
          if (form.id === 'FacetSortForm' || form.id === 'FacetFiltersForm' || form.id === 'FacetSortDrawerForm') {
            forms.push(this.createSearchParams(form));
          }
        } else if (form.id === 'FacetFiltersFormMobile') {
          forms.push(this.createSearchParams(form));
        }
      });
      this.onSubmitForm(forms.join('&'), event);
    }
  }

  onActiveFilterClick(event) {
    event.preventDefault();
    FacetFiltersForm.toggleActiveFacets();
    const url =
      event.currentTarget.href.indexOf('?') == -1
        ? ''
        : event.currentTarget.href.slice(event.currentTarget.href.indexOf('?') + 1);
    FacetFiltersForm.renderPage(url);
  }
}

FacetFiltersForm.filterData = [];
FacetFiltersForm.searchParamsInitial = window.location.search.slice(1);
FacetFiltersForm.searchParamsPrev = window.location.search.slice(1);
customElements.define('facet-filters-form', FacetFiltersForm);
FacetFiltersForm.setListeners();

class PriceRange extends HTMLElement {
  constructor() {
    super();
    this.querySelectorAll('input').forEach((element) => {
      element.addEventListener('change', this.onRangeChange.bind(this));
      element.addEventListener('keydown', this.onKeyDown.bind(this));
    });
    this.setMinAndMaxValues();
  }

  onRangeChange(event) {
    this.adjustToValidValues(event.currentTarget);
    this.setMinAndMaxValues();
  }

  onKeyDown(event) {
    if (event.metaKey) return;

    const pattern = /[0-9]|\.|,|'| |Tab|Backspace|Enter|ArrowUp|ArrowDown|ArrowLeft|ArrowRight|Delete|Escape/;
    if (!event.key.match(pattern)) event.preventDefault();
  }

  setMinAndMaxValues() {
    const inputs = this.querySelectorAll('input');
    const minInput = inputs[0];
    const maxInput = inputs[1];
    if (maxInput.value) minInput.setAttribute('data-max', maxInput.value);
    if (minInput.value) maxInput.setAttribute('data-min', minInput.value);
    if (minInput.value === '') maxInput.setAttribute('data-min', 0);
    if (maxInput.value === '') minInput.setAttribute('data-max', maxInput.getAttribute('data-max'));
  }

  adjustToValidValues(input) {
    const value = Number(input.value);
    const min = Number(input.getAttribute('data-min'));
    const max = Number(input.getAttribute('data-max'));

    if (value < min) input.value = min;
    if (value > max) input.value = max;
  }
}

customElements.define('price-range', PriceRange);

class FacetRemove extends HTMLElement {
  constructor() {
    super();
    const facetLink = this.querySelector('a');
    facetLink.setAttribute('role', 'button');
    facetLink.addEventListener('click', this.closeFilter.bind(this));
    facetLink.addEventListener('keyup', (event) => {
      event.preventDefault();
      if (event.code.toUpperCase() === 'SPACE') this.closeFilter(event);
    });
  }

  closeFilter(event) {
    event.preventDefault();
    const form = this.closest('facet-filters-form') || document.querySelector('facet-filters-form');
    form.onActiveFilterClick(event);
  }
}

customElements.define('facet-remove', FacetRemove);

(() => {
  // DLM facets: mobile quick sort, visible sort names and the sticky mobile toolbar.
  const MOBILE_QUERY = window.matchMedia('(max-width: 749px)');

  function onSortChange(event) {
    const select = event.target;
    if (!(select instanceof HTMLSelectElement)) return;

    const wrapper = select.closest('[data-dlm-sort]');
    if (wrapper) FacetFiltersForm.updateSortName(wrapper);

    if (!select.matches('[data-dlm-sort-proxy]')) return;

    const mobileSort = document.getElementById('SortBy-mobile');
    const mobileForm = document.getElementById('FacetFiltersFormMobile');
    if (!mobileSort || !mobileForm) return;

    mobileSort.value = select.value;
    FacetFiltersForm.renderPage(new URLSearchParams(new FormData(mobileForm)).toString());
  }

  function initStickyToolbar() {
    const container = document.querySelector('.facets-container.dlm-facets');
    const host = container && container.closest('.facets-wrapper');
    if (!host || host.dataset.dlmFacetsHost) return;

    host.dataset.dlmFacetsHost = 'true';
    host.classList.add('dlm-facets-host');

    let frame;
    const updateStuck = () => {
      frame = undefined;
      const isStuck = MOBILE_QUERY.matches && window.scrollY > 0 && host.getBoundingClientRect().top <= 1;
      host.classList.toggle('is-stuck', isStuck);
    };
    const requestUpdate = () => {
      if (!frame) frame = requestAnimationFrame(updateStuck);
    };

    window.addEventListener('scroll', requestUpdate, { passive: true });
    window.addEventListener('resize', requestUpdate, { passive: true });
    requestUpdate();

    // The drawer lives inside the sticky toolbar's stacking context, so lift the toolbar while it is open.
    document.addEventListener(
      'toggle',
      (event) => {
        const details = event.target;
        if (!(details instanceof HTMLDetailsElement)) return;
        if (!details.classList.contains('mobile-facets__disclosure') || !host.contains(details)) return;
        host.classList.toggle('is-drawer-open', details.open);
      },
      true
    );
  }

  // Desktop pill panels: close on Escape from anywhere and on outside click (Dawn's overlay stays as is).
  function closePanel(details, restoreFocus) {
    const summary = details.querySelector('summary');
    details.removeAttribute('open');
    if (!summary) return;
    summary.setAttribute('aria-expanded', 'false');
    if (restoreFocus) summary.focus();
  }

  function openPanels() {
    return document.querySelectorAll('.dlm-facets details.facets__disclosure[open]');
  }

  document.addEventListener('keyup', (event) => {
    if (event.key !== 'Escape') return;
    openPanels().forEach((details) => {
      const active = document.activeElement;
      closePanel(details, !active || active === document.body || details.contains(active));
    });
  });

  document.addEventListener('click', (event) => {
    const target = event.target;
    // Ignore clicks whose target was re-rendered away (e.g. a Reset link inside the panel).
    if (!(target instanceof Node) || !target.isConnected) return;
    openPanels().forEach((details) => {
      if (!details.contains(target)) closePanel(details, false);
    });
  });

  document.querySelectorAll('.dlm-facets').forEach((container) => container.classList.add('dlm-facets--js'));
  document.addEventListener('change', onSortChange);

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initStickyToolbar, { once: true });
  } else {
    initStickyToolbar();
  }
})();

(() => {
  const SECTION_ID = 'main-collection-product-grid';
  const LINK_SELECTOR = ['.collection-category-nav__tab[href]', '.collection-hub-subcategory-card[href]'].join(',');

  function isCollectionUrl(url) {
    return url.origin === window.location.origin && url.pathname.includes('/collections/');
  }

  function buildSectionUrl(href) {
    const url = new URL(href, window.location.href);
    url.searchParams.set('section_id', SECTION_ID);
    return url.toString();
  }

  function hasRenderedProducts(html) {
    const documentFragment = new DOMParser().parseFromString(html, 'text/html');
    return Boolean(documentFragment.querySelector('#product-grid li.grid__item'));
  }

  function rowHasVisibleItems(row) {
    return Array.from(row.querySelectorAll('.collection-category-nav__item')).some((item) => !item.hidden);
  }

  function cardsHaveVisibleItems(container) {
    return Array.from(container.querySelectorAll('.collection-hub-subcategory-cards__item')).some((item) => !item.hidden);
  }

  function refreshContainerVisibility(container) {
    if (!container) return;

    if (container.classList.contains('collection-category-nav__row')) {
      container.hidden = !rowHasVisibleItems(container);

      const nav = container.closest('.collection-category-nav');
      if (!nav) return;

      nav.hidden = !Array.from(nav.querySelectorAll('.collection-category-nav__row')).some((row) => !row.hidden);
      return;
    }

    if (container.classList.contains('collection-hub-subcategory-cards')) {
      container.hidden = !cardsHaveVisibleItems(container);
    }
  }

  function targetContainer(link) {
    if (link.classList.contains('collection-hub-subcategory-card')) {
      return link.closest('.collection-hub-subcategory-cards');
    }

    return link.closest('.collection-category-nav__row');
  }

  function targetItem(link) {
    if (link.classList.contains('collection-hub-subcategory-card')) {
      return link.closest('.collection-hub-subcategory-cards__item');
    }

    return link.closest('.collection-category-nav__item');
  }

  function hideEmptyCollectionLinks() {
    const groupedLinks = new Map();

    document.querySelectorAll(LINK_SELECTOR).forEach((link) => {
      if (link.dataset.daddyFilter) return;

      const url = new URL(link.getAttribute('href'), window.location.href);
      if (!isCollectionUrl(url)) return;

      const item = targetItem(link);
      const container = targetContainer(link);
      if (!item || !container) return;

      const key = url.toString();
      if (!groupedLinks.has(key)) {
        groupedLinks.set(key, []);
      }

      groupedLinks.get(key).push({ item, container, isCurrent: link.getAttribute('aria-current') === 'page' });
    });

    groupedLinks.forEach((entries, href) => {
      fetch(buildSectionUrl(href), { credentials: 'same-origin' })
        .then((response) => {
          if (!response.ok) {
            throw new Error(`Failed to check ${href}`);
          }

          return response.text();
        })
        .then((html) => {
          if (hasRenderedProducts(html)) return;

          entries.forEach(({ item, container, isCurrent }) => {
            if (isCurrent) return;

            item.hidden = true;
            refreshContainerVisibility(container);
          });
        })
        .catch(() => {});
    });
  }

  const availability = window.DLMCollectionNavigationAvailability || {
    initialized: false,
    init() {
      if (this.initialized) return;
      this.initialized = true;
      hideEmptyCollectionLinks();
    },
  };

  window.DLMCollectionNavigationAvailability = availability;
  availability.init();
})();
