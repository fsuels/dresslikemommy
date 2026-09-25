"""Unauthenticated public GETs only; no shared browser cookies or storefront actions."""
import concurrent.futures
import hashlib
import json
import re
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen

root = Path(__file__).resolve().parent
payload = json.loads((root.parent / "payload/campaign_fr_payload.json").read_text())
sources = root / "landing_sources"
sources.mkdir(exist_ok=True)


class PublicText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.skip = False
        self.main = False
        self.language = None
        self.current_heading = None
        self.headings = []
        self.main_text = []
        self.all_text = []
        self.title = []
        self.in_title = False
        self.in_head = False
        self.product_links = []
        self.current_link = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "html":
            self.language = attrs.get("lang")
        if tag == "head":
            self.in_head = True
        if tag in ("script", "style"):
            self.skip = True
        if tag == "main":
            self.main = True
        if tag == "title" and self.in_head:
            self.in_title = True
        if tag in ("h1", "h2", "h3") and self.main:
            self.current_heading = {"tag": tag, "text_parts": []}
        if tag == "a" and self.main and "/products/" in attrs.get("href", ""):
            self.current_link = {"url": attrs["href"], "text_parts": []}

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.skip = False
        if tag == "title":
            self.in_title = False
        if tag == "head":
            self.in_head = False
        if self.current_heading and tag == self.current_heading["tag"]:
            self.headings.append({"tag": tag, "text": " ".join(self.current_heading["text_parts"])})
            self.current_heading = None
        if tag == "a" and self.current_link:
            self.product_links.append({"url": self.current_link["url"], "text": " ".join(self.current_link["text_parts"])})
            self.current_link = None
        if tag == "main":
            self.main = False

    def handle_data(self, data):
        text = " ".join(data.split())
        if not text or self.skip:
            return
        self.all_text.append(text)
        if self.in_title:
            self.title.append(text)
        if self.main:
            self.main_text.append(text)
        if self.current_heading:
            self.current_heading["text_parts"].append(text)
        if self.current_link:
            self.current_link["text_parts"].append(text)


def read_group(group):
    url = group["final_url"]
    record = {"group": group["name"], "requested_url": url, "method": "PUBLIC_HTTP_GET_NO_BROWSER_COOKIES"}
    try:
        with urlopen(Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=35) as response:
            body = response.read()
            record.update({"http_status": response.status, "final_url": response.geturl(), "bytes": len(body), "source_html_sha256": hashlib.sha256(body).hexdigest()})
        parser = PublicText()
        parser.feed(body.decode("utf-8", errors="replace"))
        slug = url.rsplit("/", 1)[-1]
        (sources / (slug + ".txt")).write_text("\n".join(parser.all_text) + "\n")
        (sources / (slug + "-main.txt")).write_text("\n".join(parser.main_text) + "\n")
        seen = set()
        products = []
        for link in parser.product_links:
            if link["text"] and link["url"] not in seen:
                seen.add(link["url"])
                products.append(link)
        record.update({"html_lang": parser.language, "title": " ".join(parser.title), "main_headings": parser.headings, "main_text_lines": len(parser.main_text), "all_text_lines": len(parser.all_text), "product_links_on_first_page": len(products), "products": products, "public_source_text": str(sources / (slug + ".txt")), "main_source_text": str(sources / (slug + "-main.txt"))})
    except Exception as error:
        record["error"] = type(error).__name__ + ": " + str(error)
    return record


with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    records = list(pool.map(read_group, payload["groups"]))
report = {"observed_at_utc": datetime.now(timezone.utc).isoformat(), "scope": "Eight exact French campaign URLs, first collection page only; source HTML content, not browser rendering; no location/country/cookie changes", "records": records}
(root / "landing_readback.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
for row in records:
    print(json.dumps({key: value for key, value in row.items() if key in {"group", "http_status", "final_url", "html_lang", "error", "product_links_on_first_page"}}, ensure_ascii=False))
