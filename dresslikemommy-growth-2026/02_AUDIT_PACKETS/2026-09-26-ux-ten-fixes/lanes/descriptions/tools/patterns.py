import re
NUM = r"(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|\d+)"
AUD = r"(?:baby|child|kid|kids'|adult|women's|men's|mother|father|girl|boy|unisex)"
# Documented detection list: operator / audit / sourcing language that shoppers should never see.
PATTERNS = [
  ("chart_backed",        r"chart[- ]backed"),
  ("transcribed",         r"\btranscrib\w*"),
  ("supplied_published",  r"\b(?:supplied|attached|published) (?:size )?(?:charts?|rows?|evidence)\b|\blargest published row\b|\bfactory publishes\b|\bsupplied (?:\w+ )?(?:image|photo)s?\b"),
  ("not_supplied",        r"\b(?:is|are|was|were) not (?:supplied|specified|stated|visible|confirmed)\b"),
  ("makers_labels",       r"\bmaker'?s\b"),
  ("factory",             r"\bfactory\b"),
  ("vendor_supplier",     r"\b(?:vendor|supplier|seller|manufacturer)s?\b|\bon the source\b|\bsource (?:page|chart|listing|rows?|image)\b"),
  ("marketplace",         r"1688|alibaba|aliexpress|taobao"),
  ("not_part_of_listing", r"\bnot part of this (?:listing|product)\b"),
  ("row_count",           rf"\b{NUM} {AUD} rows\b"),
  ("evidence_wording",    r"\b(?:evidence|verified|verification|inferred|inference|conservative|this draft|drafting)\b"),
  ("hardcoded_count",     r"\b(?:latest|newest) \d+ (?:new )?(?:arrivals|styles|prints|designs|products)\b|\b\d+ new arrivals\b"),
  ("cjk_fragment",        r"[぀-ヿ一-鿿]"),
  ("published_wording",   r"\b(?:is|are) published\b|\bpublishes\b"),
  ("sku_variant_jargon",  r"\bSKUs?\b|\bsize variant\b|\bsize/variant\b|\bselected variant\b|\bsingle-garment scope\b"),
  ("admin_artifact",      r"admin\.shopify\.com|http-equiv"),
]
COMPILED = [(k, re.compile(v, re.I)) for k, v in PATTERNS]
