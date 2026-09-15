#!/bin/bash
shopt -s nocasematch

EVENT_QUIESCE_MS=75
VOLUME_DEBOUNCE_MS=750

get_state() {
  pactl list sink-inputs 2>/dev/null | awk '
    BEGIN { first = 1; json = "["; sig = "[" }
    function flush() {
      if (idx == "") return
      gsub(/\\/, "\\\\", name)
      gsub(/"/, "\\\"", name)
      if (name == "") name = "unknown"
      if (!first) { json = json ","; sig = sig "," }
      first = 0
      json = json "{\"index\":" idx ",\"name\":\"" name "\",\"volume\":" vol ",\"muted\":" (mute ? "true" : "false") "}"
      sig = sig "{\"index\":" idx ",\"name\":\"" name "\",\"muted\":" (mute ? "true" : "false") "}"
    }
    /^Sink Input #/ {
      flush()
      idx = $3
      sub(/^#/, "", idx)
      name = ""
      vol = 0
      volset = 0
      mute = 0
      next
    }
    idx != "" && $1 == "Mute:" { if ($2 == "yes") mute = 1; next }
    idx != "" && $1 == "Volume:" && !volset {
      if (match($0, /[0-9]+%/)) { vol = substr($0, RSTART, RLENGTH - 1) + 0; volset = 1 }
      next
    }
    idx != "" && name == "" && $0 ~ /application\.name = "/ {
      s = $0
      sub(/^[^"]*"/, "", s)
      sub(/".*$/, "", s)
      name = s
      next
    }
    idx != "" && name == "" && $1 == "Source:" {
      s = $0
      sub(/^[ \t]*Source: */, "", s)
      name = s
      next
    }
    idx != "" && name == "" && $1 == "Name:" {
      s = $0
      sub(/^[ \t]*Name: */, "", s)
      name = s
      next
    }
    END {
      flush()
      json = json "]"
      sig = sig "]"
      print json
      print sig
    }
  '
}

now_ms() {
  local t=$EPOCHREALTIME
  t=${t/./}
  printf "%d" $((10#$t / 1000))
}

last_json=""
last_sig=""
pending_json=""
pending_sig=""
event_pending=0
last_event=0
last_volume_change=0
state=""
state_json=""
state_sig=""

split_state() {
  state_json=${state%$'\n'*}
  state_sig=${state##*$'\n'}
}

emit_state() {
  last_json=$1
  last_sig=$2
  pending_json=""
  pending_sig=""
  printf "%s\n" "$last_json"
}

refresh_state() {
  state=$(get_state)
  split_state

  if [[ $state_json == "$last_json" ]]; then
    pending_json=""
    pending_sig=""
    return
  fi

  if [[ $state_sig == "$last_sig" ]]; then
    pending_json=$state_json
    pending_sig=$state_sig
    last_volume_change=$(now_ms)
  else
    emit_state "$state_json" "$state_sig"
  fi
}

flush_pending() {
  [[ -z $pending_json ]] && return
  local now
  now=$(now_ms)
  if (( now - last_volume_change >= VOLUME_DEBOUNCE_MS )); then
    emit_state "$pending_json" "$pending_sig"
  fi
}

state=$(get_state)
split_state
emit_state "$state_json" "$state_sig"

while :; do
  while :; do
    read -r -t 0.05 line
    rc=$?

    if (( rc == 0 )); then
      if [[ $line == *sink*input* ]]; then
        event_pending=1
        last_event=$(now_ms)
      fi
    elif (( rc == 1 )); then
      break
    elif (( rc != 142 )); then
      break
    fi

    if (( event_pending )); then
      now=$(now_ms)
      if (( now - last_event >= EVENT_QUIESCE_MS )); then
        event_pending=0
        refresh_state
      fi
    else
      flush_pending
    fi
  done < <(pactl subscribe 2>/dev/null)

  sleep 1
done
