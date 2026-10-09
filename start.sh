#!/bin/sh
# Startet den lokalen Server und öffnet das Dashboard im Browser.
# Das Dashboard wird bei jedem Neuladen aus der CSV neu gebaut, wenn sie sich geändert hat.
# Optional: ./start.sh /pfad/zur/anderen.csv
cd "$(dirname "$0")" || exit 1
# Einen noch laufenden alten Dashboard-Server auf dem Port beenden.
OLD=$(lsof -tiTCP:8765 -sTCP:LISTEN)
[ -n "$OLD" ] && kill $OLD && sleep 1
(sleep 1 && open "http://localhost:8765/") &
exec python3 serve.py "$@"
