document.addEventListener("DOMContentLoaded", function () {
  const descriptions = document.querySelectorAll("[data-product-description]");

  if (!descriptions.length) return;

  const getLocaleCopy = function () {
    const copyMap = window.DLM_PRODUCT_PAGE_COPY;
    if (!copyMap || typeof copyMap !== "object") return {};

    const localeSource =
      (window.Shopify && typeof window.Shopify.locale === "string" && window.Shopify.locale) ||
      (document.documentElement && document.documentElement.lang) ||
      "";
    const locale = String(localeSource || "").replace("_", "-").toLowerCase();
    const root = locale.split("-")[0];
    const candidates = [locale];

    if (root && root !== locale) candidates.push(root);
    if (root === "pt") candidates.push("pt-BR", "pt-PT");
    if (root === "ro") candidates.push("ro", "ro-RO");
    if (root === "no") candidates.push("no", "nb");
    candidates.push("en");

    const keys = Object.keys(copyMap);
    for (let index = 0; index < candidates.length; index += 1) {
      const candidate = candidates[index];
      const key = keys.find(function (mapKey) {
        return mapKey.toLowerCase() === candidate.toLowerCase();
      });
      if (key && copyMap[key]) return copyMap[key];
    }

    return {};
  };

  const localeCopy = getLocaleCopy();
  const copy = {
    detailsEyebrow: localeCopy.description_details_eyebrow || "Details",
    highlightsHeading: localeCopy.description_highlights_heading || "Why You'll Love It",
    sizeChartHeading: localeCopy.description_size_chart_heading || "Size Chart",
    productDetailsHeading: localeCopy.description_product_details_heading || "Product Details",
    sizeChartMeta: localeCopy.description_size_chart_meta || "Measurements from the supplier source table",
    productDetailsMeta: localeCopy.description_product_details_meta || "Structured product information",
  };

  const getTextContent = function (element) {
    return String(element && element.textContent ? element.textContent : "")
      .replace(/\s+/g, " ")
      .trim();
  };

  const isEmptyList = function (element) {
    if (!element || !/^(UL|OL)$/.test(element.tagName)) return false;

    return !Array.from(element.children).some(function (child) {
      return child.tagName === "LI" && getTextContent(child) !== "";
    });
  };

  const isTextBlock = function (element) {
    if (!element || !/^(P|DIV)$/.test(element.tagName)) return false;
    if (element.querySelector("table, ul, ol, img, iframe, video, blockquote")) return false;

    return getTextContent(element) !== "";
  };

  const shouldPromoteToFeature = function (element) {
    const text = getTextContent(element);

    if (!text) return false;
    if (text.length > 220) return false;

    return (text.match(/[.!?]/g) || []).length <= 2;
  };

  const hasOnlySafeWrapperAttributes = function (element) {
    return Array.from(element.attributes || []).every(function (attribute) {
      if (/^(data-|aria-)/.test(attribute.name)) return true;
      if (attribute.name !== "style") return false;

      return /^text-align:\s*(start|left);?$/i.test(String(attribute.value || "").trim());
    });
  };

  const isTransparentDescriptionWrapper = function (element) {
    if (!element || element.tagName !== "DIV") return false;
    if (!element.children.length) return false;
    if (!hasOnlySafeWrapperAttributes(element)) return false;

    return Array.from(element.children).every(function (child) {
      return /^(P|DIV|UL|OL|TABLE|IMG|FIGURE|BR)$/.test(child.tagName);
    });
  };

  const isEmptySpacerBlock = function (element) {
    if (!element) return false;
    if (element.tagName === "BR") return true;
    if (!/^(P|DIV)$/.test(element.tagName)) return false;
    if (element.querySelector("table, ul, ol, img, iframe, video, figure, blockquote")) return false;

    return getTextContent(element) === "";
  };

  const isListItemBlockElement = function (element) {
    if (!element || element.nodeType !== 1) return false;

    return /^(P|DIV|UL|OL|TABLE|FIGURE|IMG|VIDEO|IFRAME|BLOCKQUOTE|H1|H2|H3|H4|H5|H6)$/.test(element.tagName);
  };

  const wrapInlineListItemContent = function (item) {
    if (!item || item.tagName !== "LI") return;

    let inlineNodes = [];

    const flushInlineNodes = function (anchorNode) {
      if (!inlineNodes.length) return;

      const paragraph = document.createElement("p");
      paragraph.className = "product-copy__item-copy";

      inlineNodes.forEach(function (node) {
        paragraph.appendChild(node);
      });

      item.insertBefore(paragraph, anchorNode || null);
      inlineNodes = [];
    };

    Array.from(item.childNodes).forEach(function (node) {
      if (node.nodeType === 3) {
        if (String(node.textContent || "").trim() === "") {
          node.remove();
          return;
        }

        inlineNodes.push(node);
        return;
      }

      if (node.nodeType !== 1) {
        node.remove();
        return;
      }

      if (isListItemBlockElement(node)) {
        flushInlineNodes(node);
        return;
      }

      inlineNodes.push(node);
    });

    flushInlineNodes(null);
  };

  const normalizeDescriptionStructure = function (container) {
    let changed = true;

    while (changed) {
      changed = false;

      Array.from(container.children).forEach(function (child) {
        if (!isTransparentDescriptionWrapper(child)) return;

        while (child.firstChild) {
          container.insertBefore(child.firstChild, child);
        }

        child.remove();
        changed = true;
      });

      Array.from(container.children).forEach(function (child) {
        if (!isEmptyList(child) && !isEmptySpacerBlock(child)) return;
        child.remove();
        changed = true;
      });
    }
  };

  const cleanListItem = function (item) {
    if (!item || item.tagName !== "LI") return;

    Array.from(item.children).forEach(function (child) {
      if (/^(P|DIV|SPAN)$/.test(child.tagName) && getTextContent(child) === "") {
        child.remove();
      }
    });

    const paragraphs = Array.from(item.children).filter(function (child) {
      return child.tagName === "P" && getTextContent(child) !== "";
    });
    const hasOnlyParagraphs = paragraphs.length > 1 && paragraphs.length === item.children.length;

    if (hasOnlyParagraphs) {
      const firstParagraph = paragraphs[0];

      paragraphs.slice(1).forEach(function (paragraph) {
        if (getTextContent(firstParagraph) !== "" && getTextContent(paragraph) !== "") {
          firstParagraph.appendChild(document.createTextNode(" "));
        }

        while (paragraph.firstChild) {
          firstParagraph.appendChild(paragraph.firstChild);
        }

        paragraph.remove();
      });
    }

    wrapInlineListItemContent(item);
  };

  const normalizeList = function (listElement, className) {
    Array.from(listElement.children).forEach(function (child) {
      if (child.tagName === "LI") return;

      const item = document.createElement("li");

      while (child.firstChild) {
        item.appendChild(child.firstChild);
      }

      child.replaceWith(item);
    });

    Array.from(listElement.children).forEach(function (item) {
      cleanListItem(item);
      if (item.tagName !== "LI" || getTextContent(item) !== "") return;
      item.remove();
    });

    String(className || "")
      .split(/\s+/)
      .filter(Boolean)
      .forEach(function (token) {
        listElement.classList.add(token);
      });
  };

  const shouldSuppressVisibleSizeChart = function (tableElement) {
    if (!tableElement) return false;

    const firstHeader = tableElement.querySelector("th");
    const headerText = firstHeader ? getTextContent(firstHeader).toLowerCase() : "";
    const tableId = String(tableElement.id || "").toLowerCase();
    const isSizeChart = tableId.indexOf("size-chart") !== -1 || headerText === "size";
    if (!isSizeChart) return false;

    const productRoot = tableElement.closest("[id^='MainProduct-']");
    return !!(productRoot && productRoot.querySelector("[data-matching-size-guide]"));
  };

  const wrapTable = function (tableElement) {
    if (!tableElement || tableElement.closest(".product-copy__table-card")) return;

    if (shouldSuppressVisibleSizeChart(tableElement)) {
      tableElement.hidden = true;
      tableElement.setAttribute("aria-hidden", "true");
      tableElement.setAttribute("data-size-chart-source-only", "true");
      tableElement.style.setProperty("display", "none", "important");
      return;
    }

    const tableCard = document.createElement("div");
    const tableHeader = document.createElement("div");
    const tableTitle = document.createElement("h3");
    const tableMeta = document.createElement("p");
    const tableScroll = document.createElement("div");
    const firstHeader = tableElement.querySelector("th");
    const headerText = firstHeader ? getTextContent(firstHeader).toLowerCase() : "";
    const tableId = String(tableElement.id || "").toLowerCase();

    tableCard.className = "product-copy__table-card";
    if (tableId.indexOf("size-chart") !== -1 || headerText === "size") {
      tableCard.classList.add("product-copy__table-card--size-chart");
    }

    tableHeader.className = "product-copy__table-header";
    tableTitle.className = "product-copy__section-title";
    tableTitle.textContent = tableCard.classList.contains("product-copy__table-card--size-chart")
      ? copy.sizeChartHeading
      : copy.productDetailsHeading;
    tableMeta.className = "product-copy__section-meta";
    tableMeta.textContent = tableCard.classList.contains("product-copy__table-card--size-chart")
      ? copy.sizeChartMeta
      : copy.productDetailsMeta;

    tableScroll.className = "product-copy__table-scroll";
    tableElement.classList.add("product-copy__table");

    tableElement.parentNode.insertBefore(tableCard, tableElement);
    tableCard.appendChild(tableHeader);
    tableHeader.appendChild(tableTitle);
    tableHeader.appendChild(tableMeta);
    tableCard.appendChild(tableScroll);
    tableScroll.appendChild(tableElement);
  };

  const ensureSectionHeading = function (element, title, variantClass) {
    if (!element) return;
    if (element.previousElementSibling && element.previousElementSibling.classList.contains("product-copy__section-heading")) {
      return;
    }

    const heading = document.createElement("div");
    const eyebrow = document.createElement("span");
    const headingTitle = document.createElement("h3");

    heading.className = "product-copy__section-heading";
    if (variantClass) heading.classList.add(variantClass);

    eyebrow.className = "product-copy__section-eyebrow";
    eyebrow.textContent = copy.detailsEyebrow;

    headingTitle.className = "product-copy__section-title";
    headingTitle.textContent = title;

    heading.appendChild(eyebrow);
    heading.appendChild(headingTitle);
    element.parentNode.insertBefore(heading, element);
  };

  descriptions.forEach(function (description) {
    if (description.dataset.productDescriptionReady === "true") return;

    normalizeDescriptionStructure(description);

    let leadAssigned = false;
    let highlightsAssigned = false;
    let pendingFeatureParagraphs = [];

    const flushPendingFeatureParagraphs = function () {
      if (!pendingFeatureParagraphs.length) return;

      if (!highlightsAssigned && pendingFeatureParagraphs.length >= 2) {
        const list = document.createElement("ul");
        const firstParagraph = pendingFeatureParagraphs[0];

        list.className = "product-copy__highlights product-copy__feature-list";
        firstParagraph.parentNode.insertBefore(list, firstParagraph);

        pendingFeatureParagraphs.forEach(function (paragraph) {
          const item = document.createElement("li");

          while (paragraph.firstChild) {
            item.appendChild(paragraph.firstChild);
          }

          list.appendChild(item);
          paragraph.remove();
        });

        ensureSectionHeading(list, copy.highlightsHeading, "product-copy__section-heading--features");
        highlightsAssigned = true;
      } else {
        pendingFeatureParagraphs.forEach(function (paragraph) {
          paragraph.classList.add("product-copy__body");
        });
      }

      pendingFeatureParagraphs = [];
    };

    const mergePendingFeatureParagraphsIntoList = function (listElement) {
      if (!pendingFeatureParagraphs.length) return;

      const fragment = document.createDocumentFragment();

      pendingFeatureParagraphs.forEach(function (paragraph) {
        const item = document.createElement("li");

        while (paragraph.firstChild) {
          item.appendChild(paragraph.firstChild);
        }

        fragment.appendChild(item);
        paragraph.remove();
      });

      listElement.insertBefore(fragment, listElement.firstChild);
      pendingFeatureParagraphs = [];
    };

    Array.from(description.children).forEach(function (child) {
      if (isEmptyList(child) || isEmptySpacerBlock(child)) {
        child.remove();
        return;
      }

      if (child.tagName === "TABLE") {
        flushPendingFeatureParagraphs();
        wrapTable(child);
        return;
      }

      if (/^(UL|OL)$/.test(child.tagName)) {
        mergePendingFeatureParagraphsIntoList(child);
        normalizeList(
          child,
          highlightsAssigned ? "product-copy__body-list" : "product-copy__highlights product-copy__feature-list"
        );
        if (!highlightsAssigned) {
          ensureSectionHeading(child, copy.highlightsHeading, "product-copy__section-heading--features");
        }
        highlightsAssigned = true;
        return;
      }

      if (isTextBlock(child)) {
        if (!leadAssigned) {
          child.classList.add("product-copy__lead");
          leadAssigned = true;
          return;
        }

        if (!highlightsAssigned && shouldPromoteToFeature(child)) {
          pendingFeatureParagraphs.push(child);
          return;
        }

        flushPendingFeatureParagraphs();
        child.classList.add("product-copy__body");
        return;
      }

      flushPendingFeatureParagraphs();

      if (/^(IMG|FIGURE)$/.test(child.tagName)) {
        child.classList.add("product-copy__media");
      }
    });

    flushPendingFeatureParagraphs();
    description.dataset.productDescriptionReady = "true";
  });
});
