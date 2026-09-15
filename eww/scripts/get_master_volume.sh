#!/bin/bash
shopt -s nocasematch

print_volume() {
  local v
  v=$(pactl get-sink-volume @DEFAULT_SINK@ 2>/dev/null | grep -o '[0-9]\+%' | head -1 | tr -d '%')
  echo "${v:-0}"
}

last=""

emit_if_changed() {
  local v
  v=$(print_volume)
  if [[ $v != "$last" ]]; then
    last=$v
    printf '%s\n' "$last"
  fi
}

while :; do
  emit_if_changed
  while read -r line; do
    if [[ $line == *sink* && $line != *sink*input* ]]; then
      emit_if_changed
    fi
  done < <(pactl subscribe 2>/dev/null)
  sleep 1
done
