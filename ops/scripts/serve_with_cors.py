#!/usr/bin/env python3
"""Serve a local directory over HTTP with permissive CORS headers."""

from __future__ import annotations

import argparse
import functools
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


class CORSRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, HEAD, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        super().end_headers()

    def do_OPTIONS(self) -> None:  # noqa: N802
        self.send_response(204)
        self.end_headers()


def main() -> None:
    parser = argparse.ArgumentParser(description="Serve a local directory with CORS headers.")
    parser.add_argument("--directory", default=".", help="Directory to serve.")
    parser.add_argument("--port", type=int, default=8080, help="Port to bind.")
    parser.add_argument("--bind", default="127.0.0.1", help="Bind address.")
    args = parser.parse_args()

    directory = Path(args.directory).resolve()
    handler = functools.partial(CORSRequestHandler, directory=str(directory))
    server = ThreadingHTTPServer((args.bind, args.port), handler)
    print(f"Serving {directory} on http://{args.bind}:{args.port}/ with CORS")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
