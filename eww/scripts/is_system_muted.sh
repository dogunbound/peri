#!/bin/bash

print_mute_state() {
  if pactl get-sink-mute @DEFAULT_SINK@ 2>/dev/null | grep -q "Mute: yes"; then
    echo "true"
  else
    echo "false"
  fi
}

last=""

emit_if_changed() {
  local v
  v=$(print_mute_state)
  if [[ $v != "$last" ]]; then
    last=$v
    printf '%s\n' "$last"
  fi
}

while :; do
  emit_if_changed
  while read -r line; do
    # Sink changes, or the default sink switching ("on server")
    if [[ $line == *" on sink #"* || $line == *" on server" ]]; then
      emit_if_changed
    fi
  done < <(pactl subscribe 2>/dev/null)
  sleep 1
done
