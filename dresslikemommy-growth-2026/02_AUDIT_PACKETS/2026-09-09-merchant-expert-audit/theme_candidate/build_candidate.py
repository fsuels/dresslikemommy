from pathlib import Path
import hashlib, json, re, shutil

ROOT = Path(__file__).resolve().parent
BASE = ROOT / 'baseline'
THEME = ROOT / 'theme'
assert hashlib.md5((BASE / 'assets/product-desktop-ux-20260513-ruler-sync.js').read_bytes()).hexdigest() == '61ded53111ee5002eb5c37b42a2c4b3f'
shutil.copytree(BASE, THEME, dirs_exist_ok=True)

def replace(path, old, new):
    target = THEME / path
    text = target.read_text()
    assert text.count(old) == 1, (path, text.count(old), old[:60])
    target.write_text(text.replace(old, new))

JS = 'assets/product-desktop-ux-20260513-ruler-sync.js'
replace(JS, "  var currentGroupKey = '';\n", "  var currentGroupKey = '';\n  var bootstrapComplete = false;\n")
replace(JS, '''  function getCurrentVariant() {
    if (!selectedVariantInput || !selectedVariantInput.value) return null;
    var selectedId = String(selectedVariantInput.value);''', '''  function getExplicitLandingVariant() {
    if (!productData.selected_variant_id) return null;
    var selectedId = String(productData.selected_variant_id);''')
replace(JS, '''      if (!group || !option) return;
      items.push({''', '''      if (!group || !option || option.available === false) return;
      items.push({''')
replace(JS, '''    return uiLabel('chooseOptionsStep', 'Choose size and options');
  }

  function getSelectedItems()''', '''    var selectedOption = resolveVariantInGroup(activeGroup, activeInstance.sizeLabel, selections);
    if (selectedOption && selectedOption.available === false) {
      return uiLabel('outOfStockCurrent', 'Out of stock for current selection');
    }
    return uiLabel('chooseOptionsStep', 'Choose size and options');
  }

  function getSelectedItems()''')
replace(JS, '''  function updateSummary() {
    var items = getSelectedItems();''', '''  function getDisplayedMatchingVariant() {
    var inst = instances[0];
    if (!inst || !inst.sizeLabel) return null;
    var group = getGroupByKey(inst.groupKey);
    if (!group) return null;
    var selections = inst.axisSelections || {};
    var requiredAxes = getRequiredAxesForGroup(group);
    if (requiredAxes.some(function (axis) { return !selections[axis]; })) return null;
    var option = resolveVariantInGroup(group, inst.sizeLabel, selections);
    if (!option) return null;
    return productData.variants.find(function (variant) {
      return String(variant.id) === String(option.id);
    }) || null;
  }

  function decodeMatchingPriceText(value) {
    var decoder = document.createElement('textarea');
    decoder.innerHTML = String(value).replace(/</g, '&lt;').replace(/>/g, '&gt;');
    return decoder.textContent;
  }

  function updateMatchingPrice() {
    if (!infoContainer || !productData.default_price_html) return;
    var priceContainer = document.getElementById('price-' + sectionId);
    if (!priceContainer) return;
    var template = document.createElement('template');
    template.innerHTML = productData.default_price_html;
    var price = template.content.querySelector('.price');
    if (!price) return;
    var variant = getDisplayedMatchingVariant();
    if (variant) {
      var regularPrice = price.querySelector('.price__regular .price-item--regular');
      if (!regularPrice || typeof variant.price_text !== 'string') return;
      var priceText = decodeMatchingPriceText(variant.price_text);
      regularPrice.textContent = priceText;
      price.classList.remove('price--range', 'price--on-sale', 'price--sold-out');
      price.setAttribute('data-price-variant-id', String(variant.id));
      price.setAttribute('data-price-current-text', priceText);
      price.setAttribute('data-price-compare-text', '');
      price.setAttribute('data-price-available', String(variant.available !== false));
      price.setAttribute('data-price-on-sale', 'false');
    }
    var unitPrice = price.querySelector('.unit-price');
    if (unitPrice) {
      var hasUnitPrice = !!(variant && variant.unit_price_text && variant.unit_price_reference_unit);
      unitPrice.hidden = !hasUnitPrice;
      unitPrice.classList.toggle('hidden', !hasUnitPrice);
      if (hasUnitPrice) {
        var unitValue = unitPrice.querySelector('.price-item > span:first-child');
        var unitReference = unitPrice.querySelector('.price-item > span:last-child');
        if (unitValue) unitValue.textContent = decodeMatchingPriceText(variant.unit_price_text);
        if (unitReference) unitReference.textContent =
          (Number(variant.unit_price_reference_value) === 1 ? '' : String(variant.unit_price_reference_value)) +
          variant.unit_price_reference_unit;
      }
    }
    var nextHtml = template.innerHTML;
    if (priceContainer.innerHTML !== nextHtml) priceContainer.replaceChildren(template.content.cloneNode(true));
  }

  function updateSummary() {
    updateMatchingPrice();
    var items = getSelectedItems();''')
replace(JS, '''    var currentCtx = getCurrentOptionContext(variantSelects);
    var groups = buildRoleGroups(productData, currentCtx, true, {''', '''    var currentCtx = getCurrentOptionContext(variantSelects);
    var landingVariant = !bootstrapComplete ? getExplicitLandingVariant() : null;
    if (landingVariant) {
      productData.options.forEach(function (option, index) {
        currentCtx[normalizeText(option.name)] = getOptionValue(landingVariant, index);
      });
    }
    var groups = buildRoleGroups(productData, currentCtx, true, {''')
replace(JS, '''    if (!currentGroupKey) {
      var defaultGroup = getDefaultGroupForBootstrap(groups);''', '''    if (!bootstrapComplete) {
      bootstrapComplete = true;
      var landingGroup = landingVariant && groups.find(function (group) {
        return !!getOptionByVariantId(group, landingVariant.id);
      });
      if (landingGroup) {
        var landingOption = getOptionByVariantId(landingGroup, landingVariant.id);
        var landingInstance = addInstanceForGroup(landingGroup);
        currentGroupKey = landingGroup.key;
        landingInstance.sizeLabel = landingOption.sizeLabel || '';
        landingInstance.axisSelections = Object.assign({}, landingOption.axes || {});
        landingInstance.variantId = landingOption.available !== false ? String(landingOption.id) : '';
      }
    }

    if (!currentGroupKey) {
      var defaultGroup = getDefaultGroupForBootstrap(groups);''')
replace(JS, '''  renderBuilder();

  if (variantSelects) {''', '''  renderBuilder();

  var matchingPriceContainer = document.getElementById('price-' + sectionId);
  if (infoContainer && matchingPriceContainer && typeof MutationObserver === 'function') {
    var matchingPriceObserver = new MutationObserver(updateMatchingPrice);
    matchingPriceObserver.observe(matchingPriceContainer, { childList: true, subtree: true });
  }

  if (variantSelects) {''')

LIQUID = 'snippets/product-desktop-ux.liquid'
replace(LIQUID, '''<script type="application/json" id="ProductMatchingSetData-{{ section.id }}">
  {
    "currency": {{ cart.currency.iso_code | json }},''', '''{%- capture matching_default_price_html -%}
  {%- render 'price', product: product, use_variant: false, show_price_range: true, show_badges: false, show_sold_out_badge: false, price_class: 'price--large' -%}
{%- endcapture -%}
<script type="application/json" id="ProductMatchingSetData-{{ section.id }}">
  {
    "currency": {{ cart.currency.iso_code | json }},
    "selected_variant_id": {{ product.selected_variant.id | json }},
    "default_price_html": {{ matching_default_price_html | json }},''')
replace(LIQUID, '''          "price": {{ variant.price | json }},
          "sku":''', '''          "price": {{ variant.price | json }},
          "price_text": {% if settings.currency_code_enabled %}{{ variant.price | money_with_currency | strip_html | json }}{% else %}{{ variant.price | money | strip_html | json }}{% endif %},
          "unit_price_text": {{ variant.unit_price | money | strip_html | json }},
          "unit_price_reference_value": {{ variant.unit_price_measurement.reference_value | json }},
          "unit_price_reference_unit": {{ variant.unit_price_measurement.reference_unit | json }},
          "sku":''')
MAIN = 'sections/main-product.liquid'
replace(MAIN, '''                  assign pdp_use_variant_price = true
                  if has_matching_set_context
                    assign pdp_show_price_badges = false
                    assign pdp_use_variant_price = false''', '''                  assign pdp_use_variant_price = true
                  assign pdp_show_price_range = false
                  assign pdp_show_compare_at_price = true
                  if has_matching_set_context
                    assign pdp_show_price_badges = false
                    assign pdp_show_compare_at_price = false
                    if product.selected_variant == nil
                      assign pdp_use_variant_price = false
                      assign pdp_show_price_range = true
                    endif''')
replace(MAIN, '''                    show_price_range: has_matching_set_context,
                    show_badges:''', '''                    show_price_range: pdp_show_price_range,
                    show_compare_at_price: pdp_show_compare_at_price,
                    show_badges:''')

manifest = []
for path in sorted(BASE.rglob('*')):
    if not path.is_file(): continue
    rel = path.relative_to(BASE)
    before, after = path.read_bytes(), (THEME / rel).read_bytes()
    manifest.append({'filename': str(rel), 'baseline_md5': hashlib.md5(before).hexdigest(), 'baseline_sha256': hashlib.sha256(before).hexdigest(), 'candidate_sha256': hashlib.sha256(after).hexdigest(), 'changed': before != after})
(ROOT / 'file_manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
print('Candidate code generated from verified baseline; locale copy follows.')
