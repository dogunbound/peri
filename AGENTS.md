# Peri LeftWM theme

## Runtime
- `up` activates the theme: it runs the previous theme's teardown, symlinks `down` into `/tmp` and `eww/` to `~/.config/eww`, starts EWW and `nm-applet`, then loads `theme.ron`. Never run it as a test; it changes the active desktop and can kill EWW.
- `down` unloads the theme and kills EWW. `bash config/setup_config.sh all` installs both LeftWM and Alacritty configs; use `leftwm` or `alacritty` for one. It replaces matching files under `~/.config` with symlinks, so test it only with a temporary `HOME`.
- LeftWM theme settings are in `theme.ron`; keybindings and behavior are in `config/leftwm/config.ron`.

## EWW wiring
- `peri_bar` is a fixed-width left bar. Workspace buttons are rendered by `eww/scripts/getleftwmstate.sh` from `eww/templates/workspaces-template.liquid` via `leftwm state -w 0`.
- Calendar, mixer, and power menus are standalone GTK 3 Python processes, not EWW windows. Keep shared pointer-grab, positioning, and palette logic in `eww/scripts/popup.py`.
- `popup.py` parses unindented `$name: #hex;` lines directly from `eww.scss`; preserve that form for popup palette entries because it does not evaluate SCSS.
- EWW resolves `./scripts` and `./assets` from its config directory. Pass `-c "$PWD/eww"` for direct-checkout commands; when launching a daemon outside `up`, prepend `$PWD/eww/assets` to `XDG_DATA_DIRS` so themed icons resolve.
- Popups require PyGObject/GTK 3, GdkPixbuf, and SVG support; audio uses `pactl`. `up` appends missing-dependency warnings to `~/LEFTWM-THEME-PERI-WARN`.

## Verification
- No automated tests or linters are configured. After shell/Python edits, run:
  ```sh
  bash -n up down config/setup_config.sh config/leftwm/alacritty_launcher_script.sh eww/scripts/*.sh
  python3 -m py_compile eww/scripts/*.py
  ```
- Verify UI changes visually in X11/LeftWM. On the running theme, `eww -c "$PWD/eww" reload` avoids a full `up`; `eww -c "$PWD/eww" logs` follows daemon logs. Do not run `down` or kill EWW unless the user wants the bar stopped.

## Commits
- Commit your changes to this repository once they are complete.
- Commit-message rules:
  - Separate the subject from the body with a blank line.
  - Limit the subject line to 50 characters.
  - Capitalize the subject line.
  - Do not end the subject line with a period.
  - Use the imperative mood in the subject line.
  - Wrap the body at 72 characters.
  - Use the body to explain what and why, not how.
