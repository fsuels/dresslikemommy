"""Read exactly the12 current GSC5xx example URLs, cookie-free; preserve old evidence."""
from datetime import datetime, timezone
from hashlib import sha256
from html.parser import HTMLParser
from pathlib import Path
import json
import urllib.error
import urllib.parse
import urllib.request

INPUT = Path(__file__).with_name("gsc_server_error_examples_current.json")
EXAMPLES = json.loads(INPUT.read_text())
URLS = [row["url"] for row in EXAMPLES["rows"]]
assert len(URLS) == len(set(URLS)) == 12
OUT = Path(__file__).with_name("gsc_server_error_public_readback.json")
HOSTS = {"www.dresslikemommy.com", "dresslikemommy.com"}
for url in URLS:
    parsed = urllib.parse.urlsplit(url)
    assert parsed.scheme == "https" and parsed.hostname in HOSTS and not parsed.username and not parsed.password and not parsed.query



def safe_location(url):
    parsed = urllib.parse.urlsplit(url)
    keys = set(urllib.parse.parse_qs(parsed.query))
    if keys.intersection({"token", "access_token", "id_token", "hmac", "session", "key", "password", "signature"}):
        raise RuntimeError("Stopped unexpected authentication material in public URL")
    return {"url": url, "query_keys": sorted(keys)}


class Redirects(urllib.request.HTTPRedirectHandler):
    def __init__(self):
        super().__init__()
        self.hops = []

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        parsed = urllib.parse.urlsplit(newurl)
        self.hops.append({"status": code, "from": safe_location(req.full_url), "to": safe_location(newurl)})
        if parsed.scheme != "https" or parsed.hostname not in HOSTS or len(self.hops) > 6:
            raise RuntimeError("Stopped unexpected destination or excessive redirect chain")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


class Head(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_head = False
        self.in_title = False
        self.title = []
        self.canonical = []
        self.robots = []
        self.html_lang = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.html_lang = a.get("lang")
        if tag == "head":
            self.in_head = True
        if tag == "title" and self.in_head:
            self.in_title = True
        if self.in_head and tag == "link" and a.get("rel") == "canonical":
            self.canonical.append(safe_location(a.get("href", "")))
        if self.in_head and tag == "meta" and a.get("name", "").lower() == "robots":
            self.robots.append(a.get("content"))

    def handle_endtag(self, tag):
        if tag == "head":
            self.in_head = False
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title.append(data)


report = {
    "checked_at_utc": datetime.now(timezone.utc).isoformat(),
    "scope": "Exactly12 original GSC server-error example URLs; query strings empty as observed",
    "examples_sha256": sha256(INPUT.read_bytes()).hexdigest(),
    "expected_rows": len(URLS),
    "method": "Cookie-free public GET, at most six same-site HTTPS redirects, no raw HTML retained",
    "rows": [],
    "stopped_reason": None,
}
for url in URLS:
    row = {"requested_url": url}
    redirects = Redirects()
    opener = urllib.request.build_opener(redirects)
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "text/html"})
    try:
        try:
            response = opener.open(request, timeout=25)
        except urllib.error.HTTPError as exc:
            response = exc
        with response:
            raw = response.read(5_000_001)
            row.update({
                "status": response.code,
                "final_location": safe_location(response.url),
                "redirects": redirects.hops,
                "content_type": response.headers.get("Content-Type"),
                "x_robots_tag": response.headers.get("X-Robots-Tag"),
                "body_bytes": len(raw),
                "body_truncated": len(raw) > 5_000_000,
                "body_sha256": sha256(raw).hexdigest(),
            })
            head = Head()
            decoded = raw.decode("utf-8", errors="replace")
            head.feed(decoded)
            if "cf-chl-" in decoded or "captcha challenge" in decoded.lower():
                report["stopped_reason"] = "Public challenge detected; no retry or further requests"
            row.update({"title": "".join(head.title), "html_lang": head.html_lang, "canonical": head.canonical, "robots": head.robots})
        if row["status"] in (401, 403, 429):
            report["stopped_reason"] = "HTTP access/rate gate; no retry or further requests"
    except (urllib.error.URLError, RuntimeError, TimeoutError) as exc:
        row.update({"error_type": type(exc).__name__, "message": str(exc)[:220], "redirects": redirects.hops})
        report["stopped_reason"] = "Network or redirect gate; remaining requests not run"
    report["rows"].append(row)
    print(json.dumps({"url": url, "status": row.get("status"), "error": row.get("error_type"), "title": row.get("title")}), flush=True)
    if report["stopped_reason"]:
        break
OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"rows": len(report["rows"]), "stopped_reason": report["stopped_reason"]}), flush=True)
