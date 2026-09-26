(() => {
  const DESKTOP_QUERY = window.matchMedia('(min-width: 990px)');
  const OPEN_DELAY_MS = 90;
  const CLOSE_DELAY_MS = 180;

  const loadDeferredImages = (root) => {
    if (!root) return;
    root.querySelectorAll('img[data-dlm-src]').forEach((image) => {
      if (image.dataset.dlmSrcset) image.srcset = image.dataset.dlmSrcset;
      image.src = image.dataset.dlmSrc;
      image.removeAttribute('data-dlm-src');
      image.removeAttribute('data-dlm-srcset');
    });
  };

  const initMegaMenu = (header) => {
    const items = Array.from(header.querySelectorAll('[data-dlm-mega]'));
    if (!items.length || header.dataset.dlmMegaReady) return;
    header.dataset.dlmMegaReady = 'true';

    const headerWrapper = header.querySelector('.header-wrapper');
    let openItem = null;
    let openTimer;
    let closeTimer;

    const setScrimTop = () => {
      if (!headerWrapper) return;
      const bottom = Math.max(0, Math.round(headerWrapper.getBoundingClientRect().bottom));
      header.style.setProperty('--dlm-mega-top', `${bottom}px`);
    };

    const close = (item) => {
      if (!item) return;
      item.removeAttribute('data-open');
      item.querySelector('.dlm-nav__toggle')?.setAttribute('aria-expanded', 'false');
      if (openItem === item) {
        openItem = null;
        header.classList.remove('dlm-mega-active');
      }
    };

    const open = (item) => {
      if (!DESKTOP_QUERY.matches) return;
      if (openItem && openItem !== item) close(openItem);
      setScrimTop();
      item.setAttribute('data-open', '');
      item.querySelector('.dlm-nav__toggle')?.setAttribute('aria-expanded', 'true');
      openItem = item;
      header.classList.add('dlm-mega-active');
    };

    const clearTimers = () => {
      window.clearTimeout(openTimer);
      window.clearTimeout(closeTimer);
    };

    items.forEach((item) => {
      const toggle = item.querySelector('.dlm-nav__toggle');
      const link = item.querySelector('.header__menu-item');

      item.addEventListener('pointerenter', (event) => {
        if (event.pointerType !== 'mouse') return;
        clearTimers();
        openTimer = window.setTimeout(() => open(item), openItem ? 0 : OPEN_DELAY_MS);
      });

      item.addEventListener('pointerleave', (event) => {
        if (event.pointerType !== 'mouse') return;
        clearTimers();
        closeTimer = window.setTimeout(() => close(item), CLOSE_DELAY_MS);
      });

      toggle?.addEventListener('click', () => {
        clearTimers();
        if (item.hasAttribute('data-open')) {
          close(item);
        } else {
          open(item);
        }
      });

      item.addEventListener('keydown', (event) => {
        if (event.key !== 'Escape' || !item.hasAttribute('data-open')) return;
        event.stopPropagation();
        close(item);
        (toggle || link)?.focus();
      });

      item.addEventListener('focusout', (event) => {
        if (!item.hasAttribute('data-open')) return;
        if (event.relatedTarget && item.contains(event.relatedTarget)) return;
        close(item);
      });
    });

    document.addEventListener('click', (event) => {
      if (openItem && !openItem.contains(event.target)) close(openItem);
    });

    DESKTOP_QUERY.addEventListener('change', () => {
      clearTimers();
      if (openItem) close(openItem);
    });
  };

  const initDrawerImages = () => {
    document.addEventListener(
      'toggle',
      (event) => {
        const details = event.target;
        if (!(details instanceof HTMLDetailsElement) || !details.open) return;
        if (details.id === 'Details-menu-drawer-container') {
          loadDeferredImages(details.querySelector('.dlm-drawer-rail'));
        } else if (details.closest('#menu-drawer')) {
          loadDeferredImages(details.querySelector(':scope > .menu-drawer__submenu'));
        }
      },
      true
    );
  };

  const init = () => {
    document.querySelectorAll('.section-header').forEach(initMegaMenu);
  };

  initDrawerImages();

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  document.addEventListener('shopify:section:load', init);
})();
