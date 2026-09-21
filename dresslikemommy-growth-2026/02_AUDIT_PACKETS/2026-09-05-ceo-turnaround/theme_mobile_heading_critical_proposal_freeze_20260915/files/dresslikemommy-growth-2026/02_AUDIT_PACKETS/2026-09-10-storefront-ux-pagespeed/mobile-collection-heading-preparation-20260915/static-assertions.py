"""Bounded source/cascade checks; not a browser, renderer, or general CSS validator."""
from pathlib import Path
from dataclasses import dataclass, field
import hashlib
import json
import re

PACKET = Path(__file__).resolve().parent
TARGET = "assets/theme-inline-body-static-07.css"
BEFORE = "63d4589f6c6a7bd06dea98eea70e35a0ca2b37274fe4ade7a36ba3e141da67d8"
AFTER = "cde012519aca7deab9cb065962166e8010dfee9a720405d0958b25f89f620736"
assertions = []


def check(name, condition):
    assert condition, name
    assertions.append(name)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_rules(text, bounds=(0, float("inf"))):
    """Parse balanced blocks and retain only this component's relevant selectors."""
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    position = 0
    output = []
    while position < len(text):
        opening = text.find("{", position)
        if opening < 0:
            assert not text[position:].strip()
            break
        prelude = text[position:opening].strip()
        depth, quote, escaped = 1, None, False
        ending = opening + 1
        while ending < len(text) and depth:
            char = text[ending]
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif quote:
                if char == quote:
                    quote = None
            elif char in "\"'":
                quote = char
            elif char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
            ending += 1
        assert depth == 0 and quote is None
        body = text[opening + 1:ending - 1]
        if prelude.startswith("@media"):
            minimum, maximum = bounds
            for kind, value in re.findall(r"(min|max)-width\s*:\s*(\d+)px", prelude):
                if kind == "min":
                    minimum = max(minimum, int(value))
                else:
                    maximum = min(maximum, int(value))
            output.extend(parse_rules(body, (minimum, maximum)))
        elif not prelude.startswith("@"):
            for selector in prelude.split(","):
                selector = selector.strip()
                if "collection-hero" not in selector and selector != ".page-width--collection-breadcrumbs":
                    continue
                if "::" in selector or ":hover" in selector:
                    continue
                declarations = []
                for declaration in body.split(";"):
                    if not declaration.strip():
                        continue
                    prop, value = declaration.split(":", 1)
                    important = "!important" in value
                    value = value.replace("!important", "").strip()
                    prop = prop.strip()
                    if prop in ("padding", "margin"):
                        parts = value.split()
                        if len(parts) <= 4 and not value.startswith("calc("):
                            top = parts[0]
                            right = parts[1] if len(parts) > 1 else top
                            bottom = parts[2] if len(parts) > 2 else top
                            left = parts[3] if len(parts) > 3 else right
                            declarations.extend((prop + "-" + side, val, important) for side, val in zip(("top", "right", "bottom", "left"), (top, right, bottom, left)))
                            continue
                    declarations.append((prop, value, important))
                output.append((selector, bounds, declarations))
        position = ending
    return output


@dataclass(eq=False)
class Node:
    tag: str
    classes: set = field(default_factory=set)
    parent: object = None
    children: list = field(default_factory=list)

    def add(self, tag, classes=""):
        child = Node(tag, set(classes.split()), self)
        self.children.append(child)
        return child


def simple_match(node, selector):
    for excluded in re.findall(r":not\(([^)]+)\)", selector):
        if simple_match(node, excluded):
            return False
    selector = re.sub(r":not\([^)]+\)", "", selector)
    assert not any(char in selector for char in "#:[]()"), selector
    classes = re.findall(r"\.([\w-]+)", selector)
    tag = re.sub(r"\.[\w-]+", "", selector)
    return set(classes) <= node.classes and (not tag or tag == "*" or tag == node.tag)


def match(node, selector):
    parts = re.split(r"\s+", selector.strip())
    if not simple_match(node, parts[-1]):
        return False
    if len(parts) == 1:
        return True
    if parts[-2] == ">":
        return node.parent is not None and match(node.parent, " ".join(parts[:-2]))
    if parts[-2] == "+":
        siblings = node.parent.children if node.parent else []
        index = siblings.index(node)
        return index > 0 and match(siblings[index - 1], " ".join(parts[:-2]))
    ancestor = node.parent
    while ancestor:
        if match(ancestor, " ".join(parts[:-1])):
            return True
        ancestor = ancestor.parent
    return False


def style(node, rules, width):
    winners = {}
    for order, (selector, (minimum, maximum), declarations) in enumerate(rules):
        if not minimum <= width <= maximum or not match(node, selector):
            continue
        specificity = (len(re.findall(r"\.[\w-]+", selector)), 0)
        for prop, value, important in declarations:
            rank = (important, specificity, order)
            if prop not in winners or rank >= winners[prop][0]:
                winners[prop] = (rank, value)
    return {prop: item[1] for prop, item in winners.items()}


def visible(node, rules, width):
    return style(node, rules, width).get("display", "block") != "none" and (node.parent is None or visible(node.parent, rules, width))


def fixture(with_image):
    root = Node("main")
    hero = root.add("div", "collection-hero" + (" collection-hero--with-image" if with_image else ""))
    inner = hero.add("div", "collection-hero__inner page-width")
    wrapper = inner.add("div", "collection-hero__text-wrapper")
    title = wrapper.add("h1", "collection-hero__title")
    secondary = [wrapper.add("div", cls) for cls in ("collection-hero__description rte", "collection-hub-subcategory-cards", "collection-merchandising-callout", "collection-hero__journal")]
    secondary[0].add("p")
    image = inner.add("div", "collection-hero__image-container media") if with_image else None
    if image:
        image.add("img")
    breadcrumbs = root.add("div", "page-width--collection-breadcrumbs")
    pill = breadcrumbs.add("a", "collection-category-nav__tab is-active")
    return hero, inner, wrapper, title, secondary, image, breadcrumbs, pill


extraction = json.loads((PACKET / "SOURCE_EXTRACTION.json").read_text())
check("parent extraction reports accepted paired inventory", extraction["allInventoryAndMetadataMatchOneKeyAfter"] is True)
for source in extraction["checks"]:
    path = PACKET / "source" / source["side"] / source["filename"]
    check("frozen source hash: " + source["side"] + "/" + source["filename"], sha(path) == source["sha256"])

check("candidate before hash", sha(PACKET / "source/candidate" / TARGET) == BEFORE)
check("MAIN before hash", sha(PACKET / "source/current" / TARGET) == BEFORE)
check("rollback is byte exact", (PACKET / "rollback" / TARGET).read_bytes() == (PACKET / "source/candidate" / TARGET).read_bytes())
check("proposed hash", sha(PACKET / "proposal" / TARGET) == AFTER)
check("exactly one proposed theme file", [str(x.relative_to(PACKET / "proposal")) for x in (PACKET / "proposal").rglob("*") if x.is_file()] == [TARGET])

before = (PACKET / "source/candidate" / TARGET).read_text()
after = (PACKET / "proposal" / TARGET).read_text()
suffix = "    /* Small gap between search bar and pills */"
check("breadcrumb block and suffix byte-for-byte preserved", before[before.index(suffix):] == after[after.index(suffix):])
check("existing breakpoint preserved", re.findall(r"@media[^\{]+", after) == ["@media (max-width: 767px) "])
check("all proposed declarations restricted to existing mobile range", all(bounds == (0, 767) for _, bounds, _ in parse_rules(after)))
check("no HTML, Liquid, JavaScript, asset reference, hiding workaround or font changes", not re.search(r"<h1|<script|\{\{|url\(|@import|aria-|clip|opacity|position|font-|line-height", after))

cases = []
for side in ("current", "candidate"):
    source = PACKET / "source" / side
    layout = (source / "layout/theme.liquid").read_text()
    section = (source / "sections/main-collection-banner.liquid").read_text()
    check(side + " head/section/body CSS order", layout.index("theme-inline-head-static-03.css") < layout.index("{{ content_for_layout }}") < layout.index("theme-inline-body-static-07.css"))
    check(side + " component stylesheet precedes H1", section.index("component-collection-hero.css") < section.index('<h1 class="collection-hero__title">'))
    check(side + " single unchanged native section H1", section.count("<h1") == 1 and "{{- collection_display_title | escape -}}" in section)
    check(side + " body07 remains collection-only", re.search(r"\{%- if is_collection_template -%\}\s*<link[^>]+theme-inline-body-static-07\.css", layout) is not None)
    inline = re.search(r"\{%- style -%\}(.*?)\{%- endstyle -%\}", section, re.S).group(1)
    inline = re.sub(r"\{\{.*?\}\}", "24", inline)
    head = (source / "assets/theme-inline-head-static-03.css").read_text()
    head_collection = re.search(r"/\* Mobile: collection page adjustments \*/(.*?)(?=\n\s*header\s*\{)", head, re.S).group(1)
    check(side + " bounded head block includes the only hero selector", head.count(".collection-hero") == head_collection.count(".collection-hero") == 1)
    common = parse_rules(head_collection) + parse_rules((source / "assets/component-collection-hero.css").read_text()) + parse_rules(inline)
    old_rules, new_rules = common + parse_rules(before), common + parse_rules(after)
    for with_image in (False, True):
        for width in (320, 390, 749, 750, 767, 768, 990, 1280):
            hero, inner, wrapper, title, secondary, image, breadcrumbs, pill = fixture(with_image)
            mobile = width <= 767
            label = f"{side}, image={with_image}, width={width}"
            check(label + ": reproduces legacy H1 visibility", visible(title, old_rules, width) == (not mobile))
            check(label + ": existing H1 exposed", visible(title, new_rules, width))
            check(label + ": secondary blocks retain visibility", all(visible(x, new_rules, width) == (not mobile) for x in secondary))
            if image:
                check(label + ": image retains visibility", visible(image, new_rules, width) == (not mobile))
            check(label + ": category pill remains visible", visible(pill, new_rules, width))
            check(label + ": breadcrumb styles unchanged", style(breadcrumbs, old_rules, width) == style(breadcrumbs, new_rules, width))
            if mobile:
                check(label + ": no reserved inner image spacing", style(inner, new_rules, width).get("padding-bottom", "0") == "0")
                check(label + ": text takes full row", style(wrapper, new_rules, width)["flex-basis"] == "100%")
                if with_image:
                    check(label + ": image banner padding removed", all(style(hero, new_rules, width).get("padding-" + s, "0") == "0" for s in ("top", "right", "bottom", "left")))
                    check(label + ": image text padding removed", all(style(wrapper, new_rules, width)["padding-" + s] == "0" for s in ("top", "right", "bottom", "left")))
            else:
                check(label + ": desktop component styles identical", all(style(x, old_rules, width) == style(x, new_rules, width) for x in [hero, inner, wrapper, title] + secondary + ([image] if image else [])))
            cases.append({"side": side, "width": width, "withImage": with_image, "status": "PASS", "afterBrowserAcceptance": "NOT RUN"})

result = {
    "status": "PASS",
    "type": "BOUNDED_STATIC_SOURCE_AND_CASCADE_MODEL",
    "sourceReadAtUtc": extraction["observedAtUtc"],
    "beforeSha256": BEFORE,
    "proposedSha256": AFTER,
    "assertionCount": len(assertions),
    "assertions": assertions,
    "syntheticCases": cases,
    "syntheticCaseCount": len(cases),
    "limitations": [
        "No DOM rendering, pixel layout, network, JavaScript animation, computed browser style, or user interaction was run.",
        "The model covers relevant class selectors, descendant/child/adjacent combinators, :not(simple-class), media width bounds and !important/source order only.",
        "Only the head CSS collection media block, component CSS, body07 CSS and section style are modeled; unrelated global styles and dynamic application styles are not treated as tested.",
        "Inline Liquid shadow spacing uses a synthetic 24px value, not a claim about store settings.",
        "Historical browser evidence proves the before defect on candidate, not after acceptance or direct current MAIN rendered behavior."
    ]
}
(PACKET / "STATIC_ASSERTIONS.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({k: result[k] for k in ("status", "type", "assertionCount", "syntheticCaseCount", "proposedSha256")}, indent=2))
