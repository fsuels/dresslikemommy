document.addEventListener("DOMContentLoaded", function () {
  const descriptions = document.querySelectorAll("[data-product-description]");

  if (!descriptions.length) return;

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

  const wrapTable = function (tableElement) {
    if (!tableElement || tableElement.closest(".product-copy__table-card")) return;

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
      ? "Size Chart"
      : "Product Details";
    tableMeta.className = "product-copy__section-meta";
    tableMeta.textContent = tableCard.classList.contains("product-copy__table-card--size-chart")
      ? "Measurements from the supplier source table"
      : "Structured product information";

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
    eyebrow.textContent = "Details";

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

        ensureSectionHeading(list, "Why You'll Love It", "product-copy__section-heading--features");
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
          ensureSectionHeading(child, "Why You'll Love It", "product-copy__section-heading--features");
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
