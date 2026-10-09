#!/usr/bin/env python3
"""Builds dashboard.html from the internship CSV and template.html.

Where the CSV comes from, in this order:
  1. a path given on the command line
  2. the CSV_PATH environment variable
  3. the path written in a file called .csv-source (not committed)
  4. career_pages_full.csv in this folder

If the CSV lives somewhere else, it is also copied into this folder so the
copy in the repo (which the hosted site is built from) stays up to date.
"""
import csv
import io
import json
import os
import sys
import time
from pathlib import Path

HERE = Path(__file__).parent
DEFAULT_CSV = HERE / "career_pages_full.csv"


def source_csv():
    path = os.environ.get("CSV_PATH", "").strip()
    pointer = HERE / ".csv-source"
    if not path and pointer.exists():
        path = pointer.read_text(encoding="utf-8").strip()
    if not path:
        return DEFAULT_CSV
    path = Path(path).expanduser()
    return path if path.is_absolute() else HERE / path


def to_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def wait_until_settled(path, quiet=2.0, timeout=60.0):
    """Waits until the file exists and has not changed for `quiet` seconds, so a
    CSV that is still being written is not picked up half finished."""
    deadline = time.monotonic() + timeout
    last = None
    while time.monotonic() < deadline:
        try:
            stat = path.stat()
            now = (stat.st_mtime, stat.st_size)
        except FileNotFoundError:
            now = None
        if now is not None and now == last:
            return
        last = now
        time.sleep(quiet)
    raise SystemExit(f"{path.name} did not settle within {timeout:.0f}s")


def build(csv_path=None):
    csv_path = Path(csv_path) if csv_path else source_csv()
    raw = csv_path.read_bytes()
    rows = []
    for r in csv.DictReader(io.StringIO(raw.decode("utf-8-sig"), newline="")):
        company = (r.get("Company") or "").strip()
        if not company:
            continue
        rows.append(
            {
                "company": company,
                "grade": (r.get("Tier") or "").strip(),
                "status": (r.get("Status") or "").strip(),
                "title": (r.get("Position Title") or "").strip(),
                "loc": (r.get("Location") or "").strip(),
                "tier": (r.get("Location Tier") or "").strip(),
                "url": (r.get("Direct Job URL") or "").strip(),
                "board": (r.get("Career/Board URL") or "").strip(),
                "n": to_int(r.get("All Current Matches (count)")),
                "checked": (r.get("Last Checked") or "").strip(),
            }
        )

    if not rows:
        raise SystemExit(f"{csv_path.name} has no rows with a Company column, not building")
    if csv_path.resolve() != DEFAULT_CSV.resolve() and (not DEFAULT_CSV.exists() or DEFAULT_CSV.read_bytes() != raw):
        DEFAULT_CSV.write_bytes(raw)

    data = json.dumps(rows, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    template = (HERE / "template.html").read_text(encoding="utf-8")
    head, body = template.replace("/*__DATA__*/[]", data).split("<!--BODY-->")

    # Standalone file for opening locally and for hosting.
    (HERE / "dashboard.html").write_text(
        '<!doctype html>\n<html lang="de">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f"{head}</head>\n<body>\n{body}</body>\n</html>\n",
        encoding="utf-8",
    )
    # Fragment without the document skeleton, for publishing as an artifact.
    (HERE / "dashboard.artifact.html").write_text(head + body, encoding="utf-8")
    return len(rows), sum(1 for r in rows if r["n"] > 0)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--settle"]
    path = Path(args[0]) if args else source_csv()
    if "--settle" in sys.argv:
        wait_until_settled(path)
    total, with_jobs = build(path)
    print(f"{total} companies, {with_jobs} with open internships -> dashboard.html")
