#!/bin/sh
# Builds from the current CSV and, if the data changed, commits and pushes it.
# The push triggers a new deployment of the hosted site.
cd "$(dirname "$0")" || exit 1
log() { echo "$(date '+%Y-%m-%d %H:%M:%S') $*"; }

python3 build.py --settle > /dev/null || { log "build failed, nothing published"; exit 1; }
git add career_pages_full.csv
if git diff --cached --quiet -- career_pages_full.csv; then
  log "CSV unchanged, nothing to publish"
  exit 0
fi
git commit -q -m "Update data ($(date +%Y-%m-%d))" -- career_pages_full.csv || { log "commit failed"; exit 1; }
if git push -q; then
  log "published new CSV"
else
  # undo the commit but keep the change staged, so the next run tries again
  git reset -q --soft HEAD~1
  log "push failed, will retry on the next run"
  exit 1
fi
