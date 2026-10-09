#!/bin/sh
# Takes the current CSV, and if it changed, commits and pushes it.
# The push triggers a new deployment of the hosted site.
cd "$(dirname "$0")" || exit 1
python3 build.py || exit 1
git add career_pages_full.csv
if git diff --cached --quiet; then
  echo "CSV unchanged, nothing to publish."
  exit 0
fi
git commit -q -m "Update data ($(date +%Y-%m-%d))" && git push
