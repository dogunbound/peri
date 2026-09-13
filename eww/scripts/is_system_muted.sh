#!/bin/bash

print_mute_state() {
  if pactl get-sink-mute @DEFAULT_SINK@ | grep -q "Mute: yes"; then
    echo "true"
  else
    echo "false"
  fi
}

print_mute_state

pactl subscribe | while read -r line; do
  if [[ "$line" == *"sink"* ]]; then
    print_mute_state
  fi
done
