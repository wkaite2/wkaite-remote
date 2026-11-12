#!/usr/bin/env python2
"""Small threaded static file server for the WKAite download mirror.

Runs on the CentOS 7 host's Python 2.7. Supports concurrent downloads,
HTTP Range requests, and explicit MIME types for installer files.
"""
from __future__ import print_function

import BaseHTTPServer
import email.utils
import mimetypes
import os
import posixpath
import re
import SocketServer
import sys
import urllib

ROOT = "/opt/rustdesk-selfhost/downloads"
PORT = 21120

MIME_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".webp": "image/webp",
    ".png": "image/png",
    ".svg": "image/svg+xml",
    ".txt": "text/plain; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".apk": "application/vnd.android.package-archive",
    ".exe": "application/vnd.microsoft.portable-executable",
    ".msi": "application/x-msi",
    ".deb": "application/vnd.debian.binary-package",
    ".rpm": "application/x-rpm",
    ".dmg": "application/x-apple-diskimage",
    ".appimage": "application/octet-stream",
    ".zst": "application/zstd",
}


class ThreadedHTTPServer(SocketServer.ThreadingMixIn, BaseHTTPServer.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True
    request_queue_size = 128


class DownloadHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    server_version = "WKAiteDownload/1.0"

    def log_message(self, fmt, *args):
        sys.stdout.write("%s - - [%s] %s\n" % (
            self.address_string(), self.log_date_time_string(), fmt % args))
        sys.stdout.flush()

    def translate_path(self, raw_path):
        path = urllib.unquote(raw_path.split("?", 1)[0].split("#", 1)[0])
        clean = posixpath.normpath(path)
        parts = [p for p in clean.split("/") if p not in ("", ".", "..")]
        target = os.path.realpath(os.path.join(ROOT, *parts))
        if target != ROOT and not target.startswith(ROOT + os.sep):
            raise ValueError("path outside download root")
        return target

    def do_HEAD(self):
        self.serve(False)

    def do_GET(self):
        self.serve(True)

    def serve(self, include_body):
        try:
            path = self.translate_path(self.path)
        except ValueError:
            self.send_error(403, "Forbidden")
            return

        if os.path.isdir(path):
            index = os.path.join(path, "index.html")
            if os.path.isfile(index):
                path = index
            else:
                self.send_error(404, "Not Found")
                return

        if not os.path.isfile(path):
            self.send_error(404, "Not Found")
            return

        try:
            f = open(path, "rb")
            st = os.fstat(f.fileno())
        except (IOError, OSError):
            self.send_error(403, "Forbidden")
            return

        size = st.st_size
        start = 0
        end = size - 1
        status = 200
        range_header = self.headers.get("Range")

        if range_header:
            match = re.match(r"^bytes=(\d*)-(\d*)$", range_header.strip())
            if not match:
                f.close()
                self.send_error(416, "Requested Range Not Satisfiable")
                return
            first, last = match.groups()
            if first == "":
                if last == "":
                    f.close()
                    self.send_error(416, "Requested Range Not Satisfiable")
                    return
                suffix = int(last)
                if suffix <= 0:
                    f.close()
                    self.send_error(416, "Requested Range Not Satisfiable")
                    return
                start = max(0, size - suffix)
            else:
                start = int(first)
            if last != "":
                end = int(last)
            if start >= size or end < start:
                f.close()
                self.send_response(416)
                self.send_header("Content-Range", "bytes */%d" % size)
                self.send_header("Content-Length", "0")
                self.send_header("Connection", "close")
                self.end_headers()
                return
            end = min(end, size - 1)
            status = 206

        ext = os.path.splitext(path)[1].lower()
        content_type = MIME_TYPES.get(ext)
        if content_type is None:
            content_type = mimetypes.guess_type(path)[0] or "application/octet-stream"

        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(end - start + 1 if size else 0))
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Last-Modified", email.utils.formatdate(st.st_mtime, usegmt=True))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("X-Content-Type-Options", "nosniff")
        if ext not in (".html", ".webp", ".png", ".svg"):
            self.send_header("Content-Disposition", 'attachment; filename="%s"' % os.path.basename(path))
        if status == 206:
            self.send_header("Content-Range", "bytes %d-%d/%d" % (start, end, size))
        self.send_header("Connection", "close")
        self.end_headers()

        if include_body and size:
            try:
                f.seek(start)
                remaining = end - start + 1
                while remaining > 0:
                    chunk = f.read(min(1024 * 1024, remaining))
                    if not chunk:
                        break
                    self.wfile.write(chunk)
                    remaining -= len(chunk)
            except (IOError, OSError):
                # Browsers commonly cancel an in-flight download when the user navigates away.
                pass
        f.close()


def main():
    if len(sys.argv) > 1:
        globals()["PORT"] = int(sys.argv[1])
    server = ThreadedHTTPServer(("0.0.0.0", PORT), DownloadHandler)
    print("Serving %s on 0.0.0.0:%d with threading and Range support" % (ROOT, PORT))
    sys.stdout.flush()
    server.serve_forever(poll_interval=0.5)


if __name__ == "__main__":
    main()
