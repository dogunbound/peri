#!/bin/bash
# Cycles through the images in wallpapers/ with feh.
# Interval in seconds: WALLPAPER_INTERVAL env var, or the first line of wallpapers/interval.
SCRIPTPATH="$(
  cd "$(dirname "$0")"
  pwd -P
)"
DIR="$SCRIPTPATH/wallpapers"
PIDFILE="/tmp/leftwm-theme-peri-wallpaper.pid"
FEH="$(command -v feh || echo /usr/bin/feh)"

if [ "$1" = "stop" ]; then
  [ -f "$PIDFILE" ] && kill "$(cat "$PIDFILE")" 2>/dev/null
  rm -f "$PIDFILE"
  exit 0
fi

"$0" stop
echo $$ >"$PIDFILE"

INTERVAL="${WALLPAPER_INTERVAL:-$(head -n1 "$DIR/interval" 2>/dev/null)}"
[[ "$INTERVAL" =~ ^[0-9]+$ && "$INTERVAL" -gt 0 ]] || INTERVAL=300

while true; do
  mapfile -t IMAGES < <(find "$DIR" -maxdepth 1 -type f \( -iname '*.png' -o -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.webp' \))
  if [ "${#IMAGES[@]}" -eq 0 ]; then
    exit 0
  fi
  "$FEH" --no-fehbg --randomize --bg-fill "${IMAGES[@]}"
  # Only a single image: nothing to cycle
  [ "${#IMAGES[@]}" -eq 1 ] && exit 0
  sleep "$INTERVAL"
done
