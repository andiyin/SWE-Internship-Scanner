#!/bin/sh
# macOS only. Installs a background job (LaunchAgent) that runs publish.sh as soon
# as the CSV is changed or replaced, so the hosted site updates on its own.
#
#   ./install-watcher.sh          install or update
#   ./install-watcher.sh remove   uninstall
cd "$(dirname "$0")" || exit 1
DIR=$(pwd -P)
LABEL=local.internship-scanner.publish
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
LOG="$HOME/Library/Logs/internship-scanner.log"
DOMAIN="gui/$(id -u)"

launchctl bootout "$DOMAIN/$LABEL" 2>/dev/null
if [ "$1" = "remove" ]; then
  rm -f "$PLIST"
  echo "Watcher removed."
  exit 0
fi

CSV=$(python3 -c "from build import source_csv; print(source_csv().resolve())") || exit 1
[ -f "$CSV" ] || { echo "CSV not found: $CSV"; exit 1; }
# Also watch the folder, because replacing a file swaps it out underneath the watcher.
WATCH="<string>$CSV</string>"
[ "$(dirname "$CSV")" != "$DIR" ] && WATCH="$WATCH<string>$(dirname "$CSV")</string>"

mkdir -p "$HOME/Library/LaunchAgents" "$HOME/Library/Logs"
cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>$LABEL</string>
  <key>ProgramArguments</key><array><string>/bin/sh</string><string>$DIR/publish.sh</string></array>
  <key>WatchPaths</key><array>$WATCH</array>
  <key>StartInterval</key><integer>3600</integer>
  <key>RunAtLoad</key><true/>
  <key>ProcessType</key><string>Background</string>
  <key>EnvironmentVariables</key><dict><key>PATH</key><string>/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string></dict>
  <key>StandardOutPath</key><string>$LOG</string>
  <key>StandardErrorPath</key><string>$LOG</string>
</dict>
</plist>
EOF
launchctl bootstrap "$DOMAIN" "$PLIST" || exit 1
echo "Watcher installed. It logs to $LOG"
