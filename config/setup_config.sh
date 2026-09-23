#!/bin/bash

shopt -s dotglob
shopt -s nullglob

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)

cd "$SCRIPT_DIR"

CONFIG_FOLDERS=(*/)

help_message() {
  echo "Provide the name of the config you want to install, or use 'all' to install all of them"
  echo ""
  echo "Available configs:"
  for dir in "${CONFIG_FOLDERS[@]}"; do
    echo "${dir%/}"
  done
}

link_config() {
  local name="$1"
  local src_root="$SCRIPT_DIR/$name"
  local dest_root="$HOME/.config/$name"

  if [[ ! -d "$src_root" ]]; then
    echo "Config '$name' does not exist"
    return 1
  fi

  echo "Setting up '$name'..."

  local file rel dest
  while IFS= read -r -d '' file; do
    rel="${file#"$src_root"/}"
    dest="$dest_root/$rel"

    if [[ -d "$dest" && ! -L "$dest" ]]; then
      echo "  Skipping '$dest': destination is a directory, leaving it alone"
      continue
    fi

    mkdir -p "$(dirname "$dest")"
    if [[ -e "$dest" || -L "$dest" ]]; then
      rm -f "$dest"
    fi
    ln -s "$file" "$dest"
    echo "  $dest -> $file"
  done < <(find "$src_root" -type f -print0)
}

if [[ $# -eq 0 ]]; then
  help_message
  exit 1
fi

names=()
for arg in "$@"; do
  if [[ "$arg" == "all" ]]; then
    for dir in "${CONFIG_FOLDERS[@]}"; do
      names+=("${dir%/}")
    done
  else
    names+=("$arg")
  fi
done

for name in "${names[@]}"; do
  link_config "$name"
done
