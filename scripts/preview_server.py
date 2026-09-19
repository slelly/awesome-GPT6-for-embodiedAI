#!/usr/bin/env python3
"""Serve one static directory on loopback with single-byte-range support.

This is only for the temporary local preview.  It deliberately has no
directory listing or parent-directory access, so the Cloudflare tunnel can
publish `site/` without exposing the repository.
"""
from __future__ import annotations

import argparse
import mimetypes
from email.utils import formatdate
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit


class StaticHandler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'
    root: Path

    def _file_for_request(self) -> Path | None:
        relative = unquote(urlsplit(self.path).path).lstrip('/')
        candidate = (self.root / relative).resolve()
        if candidate == self.root:
            candidate = candidate / 'index.html'
        if self.root not in candidate.parents or not candidate.is_file():
            return None
        return candidate

    def _range(self, total: int) -> tuple[int, int] | None:
        value = self.headers.get('Range')
        if not value:
            return (0, total - 1)
        if not value.startswith('bytes=') or ',' in value:
            return None
        start_text, _, end_text = value[6:].partition('-')
        try:
            if start_text:
                start = int(start_text)
                end = int(end_text) if end_text else total - 1
            else:
                length = int(end_text)
                start, end = max(0, total - length), total - 1
        except ValueError:
            return None
        if start < 0 or start >= total or end < start:
            return None
        return (start, min(end, total - 1))

    def _send_headers(self, path: Path) -> tuple[object, int] | None:
        try:
            file = path.open('rb')
        except OSError:
            self.send_error(HTTPStatus.NOT_FOUND)
            return None
        total = path.stat().st_size
        selected = self._range(total)
        if selected is None:
            file.close()
            self.send_response(HTTPStatus.REQUESTED_RANGE_NOT_SATISFIABLE)
            self.send_header('Content-Range', f'bytes */{total}')
            self.send_header('Content-Length', '0')
            self.end_headers()
            return None
        start, end = selected
        partial = self.headers.get('Range') is not None
        self.send_response(HTTPStatus.PARTIAL_CONTENT if partial else HTTPStatus.OK)
        self.send_header('Content-Type', mimetypes.guess_type(path.name)[0] or 'application/octet-stream')
        self.send_header('Content-Length', str(end - start + 1))
        self.send_header('Accept-Ranges', 'bytes')
        self.send_header('Last-Modified', formatdate(path.stat().st_mtime, usegmt=True))
        if partial:
            self.send_header('Content-Range', f'bytes {start}-{end}/{total}')
        self.end_headers()
        file.seek(start)
        return file, end - start + 1

    def do_GET(self) -> None:
        path = self._file_for_request()
        if path is None:
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        response = self._send_headers(path)
        if response is None:
            return
        file, remaining = response
        with file:
            while remaining:
                block = file.read(min(64 * 1024, remaining))
                if not block:
                    break
                self.wfile.write(block)
                remaining -= len(block)

    def do_HEAD(self) -> None:
        path = self._file_for_request()
        if path is None:
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        response = self._send_headers(path)
        if response is not None:
            response[0].close()

    def log_message(self, fmt: str, *args: object) -> None:
        print(f'{self.log_date_time_string()} {self.address_string()} {fmt % args}', flush=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory', type=Path, required=True)
    parser.add_argument('--bind', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=8765)
    args = parser.parse_args()
    root = args.directory.resolve()
    if not root.is_dir():
        parser.error(f'not a directory: {root}')
    StaticHandler.root = root
    server = ThreadingHTTPServer((args.bind, args.port), StaticHandler)
    print(f'Serving {root} on http://{args.bind}:{args.port}', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
