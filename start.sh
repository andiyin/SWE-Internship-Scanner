#!/bin/sh
# Starts the local server and opens the dashboard in the browser.
# The dashboard is rebuilt on reload whenever the CSV changed.
# Optional: ./start.sh path/to/other.csv
cd "$(dirname "$0")" || exit 1
# Stop an old dashboard server that still holds the port.
OLD=$(lsof -tiTCP:8765 -sTCP:LISTEN)
[ -n "$OLD" ] && kill $OLD && sleep 1
(sleep 1 && open "http://localhost:8765/") &
exec python3 serve.py "$@"
