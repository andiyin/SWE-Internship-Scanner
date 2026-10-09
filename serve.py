#!/usr/bin/env python3
"""Serves the dashboard on http://localhost:8765 and rebuilds it from the CSV
whenever the CSV or the template changed since the last page load.

Usage: python3 serve.py [path/to/file.csv]
"""
import os
import sys
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from build import DEFAULT_CSV, HERE, build

PORT = int(os.environ.get("PORT", 8765))
CSV = Path(sys.argv[1]).expanduser().resolve() if len(sys.argv) > 1 else DEFAULT_CSV
last_built = None


def rebuild_if_changed():
    global last_built
    stamp = (CSV.stat().st_mtime, (HERE / "template.html").stat().st_mtime)
    if stamp != last_built:
        total, with_jobs = build(CSV)
        last_built = stamp
        print(f"Neu gebaut: {total} Companies, {with_jobs} mit offenen Stellen")


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.split("?")[0] in ("/", "/dashboard.html"):
            self.path = "/dashboard.html"
            try:
                rebuild_if_changed()
            except Exception as e:  # keep serving the last good build
                print(f"Build fehlgeschlagen, zeige letzten Stand: {e}")
        super().do_GET()

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


if __name__ == "__main__":
    rebuild_if_changed()
    print(f"Quelle: {CSV}\nDashboard: http://localhost:{PORT}/  (Ctrl+C beendet)")
    ThreadingHTTPServer(("127.0.0.1", PORT), partial(Handler, directory=str(HERE))).serve_forever()
