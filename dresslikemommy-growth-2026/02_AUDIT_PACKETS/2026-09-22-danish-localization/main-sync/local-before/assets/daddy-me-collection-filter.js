(() => {
  const FILTER_PARAM = "dlm-daddy-filter";
  const PARENT_HANDLE = "daddy-me";
  const TEES_HANDLE = "daddy-me-t-shirts";
  const SHIRTS_HANDLE = "daddy-me-shirts";
  const BUTTON_DOWNS_FILTER = "button-downs";
  const TEES_FILTER = "tees";

  function normalizeTitle(value) {
    return ` ${(value || "").toLowerCase().replace(/[^a-z0-9]+/g, " ").trim()} `;
  }

  function isButtonDownTitle(title) {
    const normalized = normalizeTitle(title);
    const hasShirtText =
      normalized.includes(" shirt ") || normalized.includes(" shirts ");
    const isTeeTitle =
      normalized.includes(" t shirt ") ||
      normalized.includes(" t shirts ") ||
      normalized.includes(" tee ") ||
      normalized.includes(" tees ");

    return hasShirtText && !isTeeTitle;
  }

  function currentFilter() {
    const params = new URLSearchParams(window.location.search);
    return params.get(FILTER_PARAM) || "all";
  }

  function collectionNav() {
    return document.querySelector("[data-daddy-collection-nav='true']");
  }

  function filterForHandle(handle) {
    if (handle === PARENT_HANDLE) {
      return currentFilter();
    }

    if (handle === TEES_HANDLE) {
      return TEES_FILTER;
    }

    if (handle === SHIRTS_HANDLE) {
      return BUTTON_DOWNS_FILTER;
    }

    return null;
  }

  function matchesFilter(title, filter) {
    if (filter === BUTTON_DOWNS_FILTER) {
      return isButtonDownTitle(title);
    }

    if (filter === TEES_FILTER) {
      return !isButtonDownTitle(title);
    }

    return true;
  }

  function updateCount(visibleCount) {
    ["ProductCount", "ProductCountDesktop"].forEach((id) => {
      const element = document.getElementById(id);
      if (!element) return;
      element.textContent = `${visibleCount} product${visibleCount === 1 ? "" : "s"}`;
    });
  }

  function updateNav(nav, filter) {
    nav.querySelectorAll("[data-daddy-filter]").forEach((link) => {
      const isActive = link.dataset.daddyFilter === filter;
      link.classList.toggle("is-active", isActive);
      if (isActive) {
        link.setAttribute("aria-current", "page");
      } else {
        link.removeAttribute("aria-current");
      }
    });
  }

  function updateNavAvailability(nav, cards) {
    const buttonDownCount = cards.reduce((count, card) => {
      const title = card.dataset.analyticsTitle || "";
      return matchesFilter(title, BUTTON_DOWNS_FILTER) ? count + 1 : count;
    }, 0);

    nav.querySelectorAll("[data-daddy-filter]").forEach((link) => {
      const navItem = link.closest(".collection-category-nav__item");
      if (!navItem) return;

      const isCurrent = link.getAttribute("aria-current") === "page";
      if (link.dataset.daddyFilter === "button-downs") {
        navItem.hidden = buttonDownCount === 0 && !isCurrent;
        return;
      }

      navItem.hidden = false;
    });

    const secondaryRow = nav.querySelector(".collection-category-nav__row--secondary");
    if (!secondaryRow) return;

    secondaryRow.hidden = !Array.from(
      secondaryRow.querySelectorAll(".collection-category-nav__item")
    ).some((item) => !item.hidden);
  }

  function applyFilter() {
    const nav = collectionNav();
    if (!nav) return;

    const currentHandle = nav.dataset.currentCollectionHandle || "";
    const filter = filterForHandle(currentHandle);
    if (!filter) return;

    const cards = Array.from(
      document.querySelectorAll("#product-grid .product-card-wrapper")
    );
    if (!cards.length) return;

    updateNavAvailability(nav, cards);

    let visibleCount = 0;
    cards.forEach((card) => {
      const gridItem = card.closest("li.grid__item");
      if (!gridItem) return;

      const title = card.dataset.analyticsTitle || "";
      const matches = matchesFilter(title, filter);

      gridItem.hidden = !matches;
      if (matches) visibleCount += 1;
    });

    if (currentHandle === PARENT_HANDLE) {
      updateNav(nav, filter === BUTTON_DOWNS_FILTER ? BUTTON_DOWNS_FILTER : "all");
    }
    updateCount(visibleCount);
  }

  function setFilter(filter) {
    const url = new URL(window.location.href);
    if (filter === "all") {
      url.searchParams.delete(FILTER_PARAM);
    } else {
      url.searchParams.set(FILTER_PARAM, filter);
    }
    window.history.replaceState({}, "", url);
    applyFilter();
  }

  document.addEventListener("click", (event) => {
    const link = event.target.closest("[data-daddy-filter]");
    if (!link) return;

    const nav = link.closest("[data-daddy-collection-nav='true']");
    if (!nav || nav.dataset.currentCollectionHandle !== PARENT_HANDLE) return;

    const filter = link.dataset.daddyFilter;
    if (filter !== "all" && filter !== BUTTON_DOWNS_FILTER) return;

    event.preventDefault();
    setFilter(filter);
  });

  window.addEventListener("popstate", applyFilter);

  const productGridContainer = document.getElementById("ProductGridContainer");
  if (productGridContainer) {
    const observer = new MutationObserver(() => {
      applyFilter();
    });
    observer.observe(productGridContainer, { childList: true, subtree: true });
  }

  applyFilter();
})();
