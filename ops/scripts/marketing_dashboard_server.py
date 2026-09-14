#!/usr/bin/env python3
"""Serve the existing growth cockpit locally; never contact business accounts.

Only GET/HEAD, the rendered cockpit, its explicitly linked safe records, and a
small status receipt are exposed. Repository records remain the sole task store.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import signal
import sys
import tempfile
import threading
import time
import types
from html.parser import HTMLParser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urljoin, urlsplit


ROOT = Path(__file__).resolve().parents[2]
SERVICE = "dlm-growth-dashboard"
DEFAULT_PORT = 8767
DASHBOARD = "ops/marketing/operator_cockpit.html"
RENDERER = "ops/scripts/render_marketing_cockpit.py"
WORKLOG = "ops/AGENT_WORKLOG.md"
SOURCE_FILES = (
    "ops/marketing/operator_cockpit.md",
    "ops/marketing/action_queue.md",
    "ops/marketing/daily_scorecard.md",
    "ops/marketing/blocker_board.md",
    "ops/marketing/spend_authorization.md",
    "ops/marketing/current_marketing_state.md",
    "ops/marketing/campaign_explorer.json",
    "ops/marketing/team_registry.md",
    "ops/marketing/review_log.md",
    "ops/prompts/paid-growth-ai-army-continuation-prompt.md",
    "ops/AGENT_COORDINATION.md",
    WORKLOG,
    RENDERER,
)
SAFE_CANONICAL_FILES = frozenset(SOURCE_FILES) - {RENDERER, WORKLOG}
SAFE_CANONICAL_FILES |= frozenset({
    "ops/marketing/decision_log.md", "ops/marketing/memory_digest.md",
    "ops/PROBLEM_TRACKER.md",
})
EVIDENCE_ROOT = "dresslikemommy-growth-2026/02_AUDIT_PACKETS/"
SAFE_EXTENSIONS = frozenset({".md", ".json", ".csv", ".txt", ".pdf", ".png", ".jpg", ".jpeg", ".webp"})
CONTENT_ERROR = "The latest records could not be rendered. Any displayed dashboard is the last successful render."
MAX_FILE_BYTES = 16 * 1024 * 1024


def iso_time(timestamp: float | None = None) -> str:
    value = dt.datetime.now(dt.timezone.utc) if timestamp is None else dt.datetime.fromtimestamp(timestamp, dt.timezone.utc)
    return value.isoformat(timespec="seconds").replace("+00:00", "Z")


def workspace_id(root: Path) -> str:
    """Identify this checkout without exposing its absolute path over HTTP."""
    return hashlib.sha256(str(root.resolve()).encode()).hexdigest()[:16]


def safe_file(root: Path, relative: str) -> Path:
    parts = PurePosixPath(relative).parts
    if not parts or relative.startswith("/") or any(p in {".", ".."} for p in parts) or "\\" in relative:
        raise ValueError("Invalid record path")
    candidate = root.joinpath(*parts)
    for index in range(1, len(parts) + 1):
        if root.joinpath(*parts[:index]).is_symlink():
            raise ValueError("Symlink records are not served")
    resolved = candidate.resolve(strict=True)
    if not resolved.is_relative_to(root) or not resolved.is_file():
        raise ValueError("Record is unavailable")
    return resolved


def read_tail(path: Path, lines: int = 500) -> bytes:
    """Read only a bounded tail of the append-only chronology."""
    with path.open("rb") as handle:
        position = handle.seek(0, os.SEEK_END)
        chunks: list[bytes] = []
        size = newlines = 0
        while position and newlines <= lines and size < 2 * 1024 * 1024:
            amount = min(position, 8192)
            position -= amount
            handle.seek(position)
            chunk = handle.read(amount)
            chunks.append(chunk)
            size += len(chunk)
            newlines += chunk.count(b"\n")
    return b"\n".join(b"".join(reversed(chunks)).splitlines()[-lines:])


def recent_handoffs(raw: bytes) -> list[dict]:
    """Expose header metadata only, never worklog paragraphs or arbitrary paths."""
    entries: list[dict] = []
    current: dict | None = None
    for line in raw.decode("utf-8").splitlines():
        heading = re.match(r"^## (\d{4}-\d{2}-\d{2})\s+[—–-]\s+(.+)$", line)
        if heading:
            title = re.sub(r"[`*]", "", heading.group(2))
            title = re.sub(r"(?:https?://|/Users/|/home/|~/|[A-Za-z]:\\)\S+", "[detail omitted]", title)
            title = re.sub(r"\b[^\s@]+@[^\s@]+\.[^\s@]+\b", "[detail omitted]", title)
            if re.search(r"\b(?:secret|password|token|api[_ -]?key)\s*[:=]", title, re.I):
                title = "Recorded handoff"
            current = {"date": heading.group(1), "title": title[:180], "anchor": None, "task_ids": []}
            entries.append(current)
        elif current is not None:
            anchor = re.match(r"^AGENT_CONTINUITY_ANCHOR:\s*`?(\d{4}-\d{2}-\d{2}-[a-z0-9-]{1,180})`?\s*$", line)
            if anchor:
                current["anchor"] = anchor.group(1)
            if re.match(r"^-\s+`?task_entities`?:", line):
                current["task_ids"] = sorted(set(re.findall(r"\bTA-\d{2,3}\b", line)))
    return list(reversed([entry for entry in entries if entry["anchor"]][-8:]))


def request_path(raw: str) -> str:
    if not raw.startswith("/") or raw.startswith("//"):
        raise ValueError("Invalid request path")
    parsed = urlsplit(raw)
    if parsed.scheme or parsed.netloc:
        raise ValueError("Invalid request path")
    path = parsed.path
    for _ in range(4):
        if re.search(r"%(?![0-9a-fA-F]{2})", path):
            raise ValueError("Invalid URL encoding")
        decoded = unquote(path, errors="strict")
        if decoded == path:
            break
        path = decoded
    if "%" in path or "\\" in path or any(ord(c) < 32 or ord(c) == 127 for c in path):
        raise ValueError("Invalid request path")
    if path.startswith("//") or any(part in {".", ".."} for part in path.split("/")):
        raise ValueError("Invalid request path")
    return path


class RecordLinks(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return
        for name, value in attrs:
            if name != "href" or not value or value.startswith("#"):
                continue
            parsed = urlsplit(value)
            if parsed.scheme or parsed.netloc:
                continue
            try:
                path = request_path(urljoin("/" + DASHBOARD, value)).lstrip("/")
            except (ValueError, UnicodeError):
                continue
            if path in SAFE_CANONICAL_FILES or (path.startswith(EVIDENCE_ROOT) and PurePosixPath(path).suffix.lower() in SAFE_EXTENSIONS):
                self.links.add(path)


class DashboardState:
    def __init__(self, root: Path = ROOT, poll_interval: float = 2.0, *, write_cache: bool = True) -> None:
        self.root = root.resolve(strict=True)
        self.poll_interval = max(0.0, poll_interval)
        self.write_cache = write_cache
        self.lock = threading.RLock()
        self.started_at = iso_time()
        self.checked_at: str | None = None
        self.rendered_at: str | None = None
        self.last_source_change_at: str | None = None
        self.revision: str | None = None
        self.content_error: str | None = None
        self.source_files: list[dict] = []
        self.handoffs: list[dict] = []
        self.html: str | None = None
        self.allowed_files: set[str] = set()
        self._module: types.ModuleType | None = None
        self._module_digest: str | None = None
        self._last_check = float("-inf")
        # An existing generated copy is a fallback only; it is never called current.
        try:
            cache = safe_file(self.root, DASHBOARD)
            if cache.stat().st_size <= MAX_FILE_BYTES:
                self.html = cache.read_text(encoding="utf-8")
                self.rendered_at = iso_time(cache.stat().st_mtime)
        except (OSError, ValueError, UnicodeError):
            pass
        self.refresh(force=True)

    def _snapshot(self, extra: set[str]) -> tuple[str, dict[str, bytes], list[dict]]:
        digest = hashlib.sha256()
        data: dict[str, bytes] = {}
        records: list[dict] = []
        for relative in sorted(set(SOURCE_FILES) | extra):
            file = safe_file(self.root, relative)
            stat = file.stat()
            if relative != WORKLOG and stat.st_size > MAX_FILE_BYTES:
                raise ValueError("Record exceeds local limit")
            raw = read_tail(file) if relative == WORKLOG else file.read_bytes()
            raw.decode("utf-8") if file.suffix in {".md", ".json", ".py", ".txt", ".csv"} else None
            data[relative] = raw
            digest.update(relative.encode() + b"\0" + hashlib.sha256(raw).digest())
            records.append({"name": file.name, "modified_at": iso_time(stat.st_mtime)})
        return digest.hexdigest(), data, records

    def _renderer(self, raw: bytes) -> types.ModuleType:
        digest = hashlib.sha256(raw).hexdigest()
        if self._module is None or digest != self._module_digest:
            # Compile the exact source instead of reusing stale timestamp-based pyc.
            name = "_dlm_growth_renderer_" + workspace_id(self.root)
            module = types.ModuleType(name)
            module.__file__ = str(self.root / RENDERER)
            previous = sys.modules.get(name)
            sys.modules[name] = module
            try:
                exec(compile(raw, module.__file__, "exec"), module.__dict__)
            except Exception:
                if previous is None:
                    sys.modules.pop(name, None)
                else:
                    sys.modules[name] = previous
                raise
            self._module, self._module_digest = module, digest
        return self._module

    def _write_html(self, output: str) -> None:
        target = self.root / DASHBOARD
        if target.is_symlink() or target.parent.resolve() != self.root / "ops/marketing":
            raise ValueError("Unsafe generated destination")
        if target.exists():
            try:
                if target.read_text(encoding="utf-8") == output:
                    return
            except UnicodeError:
                pass  # A corrupt generated cache can be replaced by valid inputs.
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=target.parent, prefix=".cockpit-", delete=False) as handle:
            temporary = Path(handle.name)
            try:
                handle.write(output)
                handle.flush()
                os.fsync(handle.fileno())
            except Exception:
                temporary.unlink(missing_ok=True)
                raise
        try:
            os.replace(temporary, target)
        finally:
            temporary.unlink(missing_ok=True)

    def refresh(self, *, force: bool = False) -> None:
        with self.lock:
            now = time.monotonic()
            if not force and now - self._last_check < self.poll_interval:
                return
            self._last_check = now
            self.checked_at = iso_time()
            try:
                # Missing former evidence links are dropped on the next successful
                # rebuild; missing canonical sources remain an explicit error.
                existing: set[str] = set()
                for name in self.allowed_files:
                    try:
                        safe_file(self.root, name)
                        existing.add(name)
                    except (OSError, ValueError):
                        pass
                revision, data, records = self._snapshot(existing)
                self.source_files = records
                self.last_source_change_at = max(record["modified_at"] for record in records)
                if revision == self.revision and self.content_error is None:
                    return
                module = self._renderer(data[RENDERER])
                for name in SOURCE_FILES:
                    if name != WORKLOG and not data[name].strip():
                        raise ValueError("Empty canonical source")
                json.loads(data["ops/marketing/campaign_explorer.json"])
                # The existing renderer owns source semantics and task parsing.
                if hasattr(module, "current_task_rows"):
                    queue = data["ops/marketing/action_queue.md"].decode()
                    section = re.search(r"^## Current turnaround tasks[^\n]*\n", queue, re.M)
                    if section is None or not re.search(r"^## ", queue[section.end():], re.M):
                        raise ValueError("The current task section is incomplete")
                if hasattr(module, "parse_authoritative_control"):
                    control = module.parse_authoritative_control(data["ops/marketing/current_marketing_state.md"].decode())
                    if not all(control.get(key) for key in ("live_state_mode", "effective_approval_policy", "next_best_action")):
                        raise ValueError("Missing current control")
                output = module.build_html()
                if not isinstance(output, str) or "<html" not in output.lower() or "</html>" not in output.lower():
                    raise ValueError("Renderer did not produce a full page")
                parser = RecordLinks()
                parser.feed(output)
                allowed: set[str] = set()
                for name in parser.links:
                    try:
                        safe_file(self.root, name)
                        allowed.add(name)
                    except (OSError, ValueError):
                        continue
                check_revision, _, _ = self._snapshot(existing)
                if revision != check_revision:
                    raise ValueError("Sources changed during rendering")
                final_revision, final_data, final_records = self._snapshot(allowed)
                if any(final_data[name] != raw for name, raw in data.items() if name in final_data):
                    raise ValueError("Sources changed before committing the render")
                handoffs = recent_handoffs(final_data[WORKLOG])
                if self.write_cache:
                    self._write_html(output)
                self.html = output
                self.allowed_files = allowed
                self.revision = final_revision
                self.source_files = final_records
                self.last_source_change_at = max(record["modified_at"] for record in final_records)
                self.handoffs = handoffs
                self.rendered_at = iso_time()
                self.content_error = None
            except Exception:
                # Error text/tracebacks may contain source bodies, credentials, or
                # absolute paths. Only this fixed receipt reaches HTTP or logs.
                self.content_error = CONTENT_ERROR

    def status(self) -> dict:
        self.refresh()
        with self.lock:
            return {
                "service": SERVICE, "online": True, "workspace_id": workspace_id(self.root),
                "started_at": self.started_at, "checked_at": self.checked_at,
                "revision": self.revision, "rendered_at": self.rendered_at,
                "last_source_change_at": self.last_source_change_at,
                "source_files": list(self.source_files), "recent_handoffs": list(self.handoffs),
                "live_agent_status": "not_connected", "content_error": self.content_error,
            }

    def page(self) -> bytes | None:
        self.refresh()
        with self.lock:
            if self.html is None:
                return None
            marker = '<meta name="dlm-dashboard-revision" content="' + (self.revision or "") + '">'
            output = re.sub(r"</head\s*>", marker + "</head>", self.html, count=1, flags=re.I)
            if marker not in output:
                output = marker + output
            return output.encode("utf-8")


class DashboardServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, state: DashboardState, port: int = DEFAULT_PORT) -> None:
        self.state = state
        super().__init__(("127.0.0.1", port), DashboardHandler)


class DashboardHandler(BaseHTTPRequestHandler):
    server_version = "DLM-Dashboard"
    sys_version = ""

    def log_message(self, format: str, *args) -> None:
        pass  # Do not persist request URLs, worklog data, or browser details.

    def _local_request(self) -> bool:
        hosts = self.headers.get_all("Host", [])
        port = self.server.server_port
        valid = {f"127.0.0.1:{port}", f"localhost:{port}"}
        if port == 80:
            valid |= {"127.0.0.1", "localhost"}
        if len(hosts) != 1 or hosts[0].lower() not in valid:
            return False
        origin = "http://" + hosts[0].lower()
        if self.headers.get("Sec-Fetch-Site", "none") not in {"none", "same-origin"}:
            return False
        if self.headers.get("Origin") not in {None, origin}:
            return False
        referer = self.headers.get("Referer")
        if referer:
            try:
                parts = urlsplit(referer)
                if f"{parts.scheme}://{parts.netloc}".lower() != origin:
                    return False
            except ValueError:
                return False
        return True

    def _respond(self, code: int, body: bytes = b"", content_type: str = "text/plain; charset=utf-8", **headers: str) -> None:
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Cross-Origin-Resource-Policy", "same-origin")
        self.send_header("Referrer-Policy", "same-origin")
        self.send_header("Content-Security-Policy", "default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; base-uri 'none'; frame-ancestors 'none'; form-action 'none'")
        for key, value in headers.items():
            self.send_header(key, value)
        self.end_headers()
        if self.command != "HEAD" and body:
            self.wfile.write(body)

    def do_GET(self) -> None:
        if not self._local_request():
            self._respond(403, b"Local same-origin access only.\n")
            return
        try:
            path = request_path(self.path)
        except (ValueError, UnicodeError):
            self._respond(400, b"Invalid request path.\n")
            return
        state = self.server.state
        if path == "/":
            self._respond(302, Location="/" + DASHBOARD)
        elif path == "/api/status":
            self._respond(200, json.dumps(state.status(), separators=(",", ":")).encode(), "application/json; charset=utf-8")
        elif path == "/" + DASHBOARD:
            page = state.page()
            self._respond(200 if page is not None else 503, page or b"Dashboard records are unavailable.\n", "text/html; charset=utf-8")
        else:
            state.refresh()
            relative = path.lstrip("/")
            with state.lock:
                permitted = relative in state.allowed_files
            if not permitted:
                self._respond(404, b"Record not found.\n")
                return
            try:
                file = safe_file(state.root, relative)
                if file.stat().st_size > MAX_FILE_BYTES:
                    raise ValueError("Record exceeds local limit")
                types_by_suffix = {".json": "application/json; charset=utf-8", ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp", ".pdf": "application/pdf"}
                self._respond(200, file.read_bytes(), types_by_suffix.get(file.suffix.lower(), "text/plain; charset=utf-8"))
            except (OSError, ValueError):
                self._respond(404, b"Record not found.\n")

    do_HEAD = do_GET

    def _read_only(self) -> None:
        self._respond(405 if self._local_request() else 403, b"This service is read-only.\n", Allow="GET, HEAD")

    do_POST = do_PUT = do_PATCH = do_DELETE = do_OPTIONS = do_TRACE = do_CONNECT = _read_only


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--poll-seconds", type=float, default=2.0)
    args = parser.parse_args()
    if not 0 <= args.port <= 65535 or not 0.25 <= args.poll_seconds <= 60:
        parser.error("Use a valid port and a polling interval from 0.25 to 60 seconds.")
    state = DashboardState(args.root, args.poll_seconds)
    try:
        server = DashboardServer(state, args.port)
    except OSError:
        raise SystemExit("Dashboard could not bind its loopback port; no other process was stopped.")
    stopped = threading.Event()

    def poll_sources() -> None:
        while not stopped.wait(args.poll_seconds):
            state.refresh()

    def stop(signum: int, frame) -> None:
        stopped.set()
        threading.Thread(target=server.shutdown, daemon=True).start()

    for signum in (signal.SIGTERM, signal.SIGINT):
        signal.signal(signum, stop)
    threading.Thread(target=poll_sources, daemon=True).start()
    print(f"{SERVICE} listening on http://127.0.0.1:{server.server_port}/", flush=True)
    try:
        server.serve_forever(poll_interval=0.25)
    finally:
        stopped.set()
        server.server_close()


if __name__ == "__main__":
    main()
