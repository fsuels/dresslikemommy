(() => {
  const MOBILE_MEDIA_QUERY = '(max-width: 989px)';
  const mobileMedia = window.matchMedia(MOBILE_MEDIA_QUERY);
  let headerMetricsRaf;

  const isMobile = () => mobileMedia.matches;
  const normalizeText = (value = '') => value.toLowerCase().trim();

  const safelyFocus = (element) => {
    if (!element) return;
    try {
      element.focus({ preventScroll: true });
    } catch (error) {
      element.focus();
    }
  };

  const updateMobileHeaderMetrics = () => {
    if (!isMobile()) return;

    const sectionHeader = document.querySelector('.section-header');
    if (!sectionHeader) return;

    const headerRect = sectionHeader.getBoundingClientRect();
    const headerBottom = Math.max(0, Math.round(headerRect.bottom));
    const headerHeight = Math.max(0, Math.round(headerRect.height));

    document.documentElement.style.setProperty('--mobile-header-bottom', `${headerBottom}px`);
    document.documentElement.style.setProperty('--mobile-header-height', `${headerHeight}px`);
    document.documentElement.style.setProperty('--header-height', `${headerHeight}px`);
  };

  const requestMobileHeaderMetrics = () => {
    if (headerMetricsRaf) cancelAnimationFrame(headerMetricsRaf);
    headerMetricsRaf = requestAnimationFrame(() => {
      updateMobileHeaderMetrics();
      headerMetricsRaf = undefined;
    });
  };

  const updatePredictiveHeading = (detailsModal) => {
    if (!isMobile()) return;
    const heading = detailsModal.querySelector('#predictive-search-queries');
    if (heading && heading.textContent.trim() !== 'Collections') heading.textContent = 'Collections';
  };

  const buildCollectionFallbackUrl = (formElement, query) => {
    const fallbackCollectionUrl = formElement?.dataset?.collectionFallbackUrl || '/collections/all';
    const url = new URL(fallbackCollectionUrl, window.location.origin);
    if (query) {
      url.searchParams.set('q', query);
    }
    return url.toString();
  };

  const getTopLevelSummary = (detailsElement) => {
    if (!detailsElement) return null;
    const firstChild = detailsElement.firstElementChild;
    if (firstChild && firstChild.tagName === 'SUMMARY') return firstChild;
    return detailsElement.querySelector('summary');
  };

  const closeSearchDetails = (searchDetails) => {
    if (!searchDetails?.hasAttribute('open')) return;

    const summary = getTopLevelSummary(searchDetails);
    if (summary) {
      summary.click();
      return;
    }

    searchDetails.removeAttribute('open');
  };

  const closeOpenMobileSearchPanels = (excludeDetails = null) => {
    if (!isMobile()) return;

    document.querySelectorAll('.mobile-header-search-icon details[open]').forEach((searchDetails) => {
      if (excludeDetails && searchDetails === excludeDetails) return;
      closeSearchDetails(searchDetails);
    });

    if (!document.querySelector('.mobile-header-search-icon details[open]')) {
      document.body.classList.remove('mobile-search-open');
    }
  };

  const forceCloseMobileMenuDrawer = (menuDetails, headerDrawer) => {
    if (!menuDetails) return;

    const menuSummary = getTopLevelSummary(menuDetails);

    menuDetails.classList.remove('menu-opening');
    menuDetails.removeAttribute('open');
    menuSummary?.setAttribute('aria-expanded', 'false');

    menuDetails.querySelectorAll('details').forEach((submenuDetails) => {
      submenuDetails.classList.remove('menu-opening');
      submenuDetails.removeAttribute('open');
      submenuDetails.querySelector('summary')?.setAttribute('aria-expanded', 'false');
    });
    menuDetails.querySelectorAll('.submenu-open').forEach((submenu) => submenu.classList.remove('submenu-open'));

    const breakpoint = headerDrawer?.dataset?.breakpoint;
    if (breakpoint) {
      document.body.classList.remove(`overflow-hidden-${breakpoint}`);
    }
    document.body.classList.remove('overflow-hidden-mobile', 'overflow-hidden-tablet', 'overflow-hidden-desktop');
    document.body.classList.remove('overflow-hidden');
    document.querySelector('.section-header')?.classList.remove('menu-open');

    if (typeof window.removeTrapFocus === 'function') {
      window.removeTrapFocus();
    }

    if (typeof headerDrawer?.onResize === 'function') {
      window.removeEventListener('resize', headerDrawer.onResize);
    }
  };

  const closeOpenMobileMenuDrawer = () => {
    if (!isMobile()) return;

    const headerDrawer = document.querySelector('header-drawer');
    const menuDetails = headerDrawer?.querySelector('.menu-drawer-container');
    if (!menuDetails?.hasAttribute('open')) return;

    const menuSummary = getTopLevelSummary(menuDetails);
    if (
      typeof headerDrawer?.closeMenuDrawer === 'function' &&
      menuSummary &&
      typeof MouseEvent !== 'undefined'
    ) {
      headerDrawer.closeMenuDrawer(new MouseEvent('click', { bubbles: true }), menuSummary);
    }

    if (!menuDetails.hasAttribute('open')) return;

    forceCloseMobileMenuDrawer(menuDetails, headerDrawer);
  };

  const bindMobileMenuDrawer = (headerDrawer) => {
    if (!headerDrawer || headerDrawer.dataset.mobileHeaderUxMenuBound === 'true') return;

    const menuDetails = headerDrawer.querySelector('.menu-drawer-container');
    const menuSummary = getTopLevelSummary(menuDetails);
    if (!menuDetails || !menuSummary) return;

    headerDrawer.dataset.mobileHeaderUxMenuBound = 'true';

    menuSummary.addEventListener(
      'click',
      () => {
        if (!isMobile()) return;
        const isOpeningMenu = !menuDetails.hasAttribute('open');
        if (isOpeningMenu) closeOpenMobileSearchPanels();
      },
      { capture: true }
    );

    menuDetails.addEventListener('toggle', () => {
      if (!isMobile()) return;
      if (menuDetails.hasAttribute('open')) {
        closeOpenMobileSearchPanels();
      } else {
        document.body.classList.remove('mobile-search-open');
      }
    });
  };

  const bindMobileSearch = (detailsModal) => {
    if (detailsModal.dataset.mobileHeaderUxBound === 'true') return;

    const details = detailsModal.querySelector('details');
    const summary = getTopLevelSummary(details);
    const form = detailsModal.querySelector('form[role="search"]');
    const input = detailsModal.querySelector('input[type="search"]');
    const emptyState = detailsModal.querySelector('[data-mobile-search-empty-state]');
    const predictive = detailsModal.querySelector('predictive-search');
    const predictiveResults = detailsModal.querySelector('[data-predictive-search]');

    if (!details || !form || !input || !emptyState) return;

    detailsModal.dataset.mobileHeaderUxBound = 'true';

    const getCollectionLinkFromShortcuts = (query) => {
      const normalizedQuery = normalizeText(query);
      if (!normalizedQuery.length) return null;

      const shortcutLinks = Array.from(detailsModal.querySelectorAll('.mobile-search-empty-state__link'));

      for (const link of shortcutLinks) {
        const shortcutTitle = normalizeText(link.textContent);
        const shortcutKeywords = normalizeText(link.dataset.collectionKeywords || '')
          .split(',')
          .map((keyword) => normalizeText(keyword))
          .filter(Boolean);

        if (
          (shortcutTitle && (normalizedQuery.includes(shortcutTitle) || shortcutTitle.includes(normalizedQuery))) ||
          shortcutKeywords.some((keyword) => normalizedQuery.includes(keyword))
        ) {
          return link;
        }
      }

      return null;
    };

    const getPredictiveCollectionLink = () => detailsModal.querySelector('[id^="predictive-search-option-collection-"] a');

    const syncEmptyState = () => {
      if (!isMobile() || !details.hasAttribute('open')) {
        emptyState.hidden = true;
        return;
      }

      const hasQuery = input.value.trim().length > 0;
      const predictiveActive = Boolean(
        predictive &&
          (predictive.hasAttribute('open') ||
            predictive.hasAttribute('loading') ||
            predictive.getAttribute('results') === 'true')
      );

      emptyState.hidden = hasQuery || predictiveActive;
    };

    if (summary) {
      summary.addEventListener(
        'click',
        () => {
          if (!isMobile()) return;
          const isOpeningSearch = !details.hasAttribute('open');
          if (isOpeningSearch) closeOpenMobileMenuDrawer();
        },
        { capture: true }
      );
    }

    form.addEventListener('submit', (event) => {
      if (!isMobile()) return;

      const query = input.value.trim();
      if (!query.length) return;

      const keyboardSelectedOption = detailsModal.querySelector('[aria-selected="true"] a');
      if (keyboardSelectedOption) return;

      const shortcutCollectionLink = getCollectionLinkFromShortcuts(query);
      const predictiveCollectionLink = getPredictiveCollectionLink();
      const targetCollectionLink = shortcutCollectionLink || predictiveCollectionLink;

      if (targetCollectionLink?.href) {
        event.preventDefault();
        window.location.assign(targetCollectionLink.href);
        return;
      }

      event.preventDefault();
      window.location.assign(buildCollectionFallbackUrl(form, query));
    });

    details.addEventListener('toggle', () => {
      if (details.hasAttribute('open') && isMobile()) {
        closeOpenMobileSearchPanels(details);
        closeOpenMobileMenuDrawer();
        requestMobileHeaderMetrics();
        document.body.classList.add('mobile-search-open');
        requestAnimationFrame(() => safelyFocus(input));
      } else {
        document.body.classList.remove('mobile-search-open');
      }
      syncEmptyState();
      updatePredictiveHeading(detailsModal);
    });

    input.addEventListener('input', syncEmptyState);
    input.addEventListener('focus', syncEmptyState);

    if (predictive) {
      const predictiveObserver = new MutationObserver(() => {
        syncEmptyState();
        updatePredictiveHeading(detailsModal);
      });
      predictiveObserver.observe(predictive, {
        attributes: true,
        attributeFilter: ['open', 'loading', 'results'],
      });
    }

    if (predictiveResults) {
      const resultsObserver = new MutationObserver(() => {
        syncEmptyState();
        updatePredictiveHeading(detailsModal);
      });
      resultsObserver.observe(predictiveResults, {
        childList: true,
        subtree: true,
      });
    }

    syncEmptyState();
  };

  const init = (root = document) => {
    const scope = root instanceof Element ? root : document;
    scope.querySelectorAll('header-drawer').forEach(bindMobileMenuDrawer);
    scope.querySelectorAll('.mobile-header-search-icon details-modal').forEach(bindMobileSearch);
    requestMobileHeaderMetrics();
  };

  document.addEventListener('DOMContentLoaded', () => {
    init(document);
  });

  document.addEventListener('shopify:section:load', (event) => {
    init(event.target || document);
  });

  mobileMedia.addEventListener('change', () => {
    if (!isMobile()) {
      document.body.classList.remove('mobile-search-open');
      return;
    }
    requestMobileHeaderMetrics();
    init(document);
  });

  window.addEventListener('resize', requestMobileHeaderMetrics, { passive: true });
  window.addEventListener('scroll', () => {
    if (!document.body.classList.contains('mobile-search-open')) return;
    requestMobileHeaderMetrics();
  }, { passive: true });
})();
