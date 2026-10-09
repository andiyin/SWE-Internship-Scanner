#!/usr/bin/env python3
"""Builds dashboard.html from career_pages_full.csv and template.html.

Usage: python3 build.py [path/to/file.csv]
"""
import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
DEFAULT_CSV = HERE / "career_pages_full.csv"


def to_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def build(csv_path=DEFAULT_CSV):
    with open(csv_path, encoding="utf-8-sig", newline="") as f:
        rows = [
            {
                "company": (r.get("Company") or "").strip(),
                "status": (r.get("Status") or "").strip(),
                "title": (r.get("Position Title") or "").strip(),
                "loc": (r.get("Location") or "").strip(),
                "tier": (r.get("Location Tier") or "").strip(),
                "url": (r.get("Direct Job URL") or "").strip(),
                "board": (r.get("Career/Board URL") or "").strip(),
                "n": to_int(r.get("All Current Matches (count)")),
                "checked": (r.get("Last Checked") or "").strip(),
                "web": "web search" in (r.get("Notes") or ""),
            }
            for r in csv.DictReader(f)
            if (r.get("Company") or "").strip()
        ]

    data = json.dumps(rows, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    template = (HERE / "template.html").read_text(encoding="utf-8")
    head, body = template.replace("/*__DATA__*/[]", data).split("<!--BODY-->")

    # Standalone file for opening locally.
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
    total, with_jobs = build(Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_CSV)
    print(f"{total} Companies, {with_jobs} mit offenen Stellen -> dashboard.html")
