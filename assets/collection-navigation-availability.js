(() => {
  const SECTION_ID = "main-collection-product-grid";
  const LINK_SELECTOR = [
    ".collection-category-nav__tab[href]",
    ".collection-hub-subcategory-card[href]",
  ].join(",");

  function isCollectionUrl(url) {
    return (
      url.origin === window.location.origin &&
      url.pathname.includes("/collections/")
    );
  }

  function buildSectionUrl(href) {
    const url = new URL(href, window.location.href);
    url.searchParams.set("section_id", SECTION_ID);
    return url.toString();
  }

  function hasRenderedProducts(html) {
    const documentFragment = new DOMParser().parseFromString(html, "text/html");
    return Boolean(documentFragment.querySelector("#product-grid li.grid__item"));
  }

  function rowHasVisibleItems(row) {
    return Array.from(row.querySelectorAll(".collection-category-nav__item")).some(
      (item) => !item.hidden
    );
  }

  function cardsHaveVisibleItems(container) {
    return Array.from(
      container.querySelectorAll(".collection-hub-subcategory-cards__item")
    ).some((item) => !item.hidden);
  }

  function refreshContainerVisibility(container) {
    if (!container) return;

    if (container.classList.contains("collection-category-nav__row")) {
      container.hidden = !rowHasVisibleItems(container);

      const nav = container.closest(".collection-category-nav");
      if (!nav) return;

      nav.hidden = !Array.from(
        nav.querySelectorAll(".collection-category-nav__row")
      ).some((row) => !row.hidden);
      return;
    }

    if (container.classList.contains("collection-hub-subcategory-cards")) {
      container.hidden = !cardsHaveVisibleItems(container);
    }
  }

  function targetContainer(link) {
    if (link.classList.contains("collection-hub-subcategory-card")) {
      return link.closest(".collection-hub-subcategory-cards");
    }

    return link.closest(".collection-category-nav__row");
  }

  function targetItem(link) {
    if (link.classList.contains("collection-hub-subcategory-card")) {
      return link.closest(".collection-hub-subcategory-cards__item");
    }

    return link.closest(".collection-category-nav__item");
  }

  const groupedLinks = new Map();

  document.querySelectorAll(LINK_SELECTOR).forEach((link) => {
    if (link.dataset.daddyFilter) return;

    const url = new URL(link.getAttribute("href"), window.location.href);
    if (!isCollectionUrl(url)) return;

    const item = targetItem(link);
    const container = targetContainer(link);
    if (!item || !container) return;

    const key = url.toString();
    if (!groupedLinks.has(key)) {
      groupedLinks.set(key, []);
    }

    groupedLinks.get(key).push({ link, item, container });
  });

  groupedLinks.forEach((entries, href) => {
    fetch(buildSectionUrl(href), { credentials: "same-origin" })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`Failed to check ${href}`);
        }

        return response.text();
      })
      .then((html) => {
        if (hasRenderedProducts(html)) return;

        entries.forEach(({ link, item, container }) => {
          if (link.getAttribute("aria-current") === "page") return;

          item.hidden = true;
          refreshContainerVisibility(container);
        });
      })
      .catch(() => {});
  });
})();
