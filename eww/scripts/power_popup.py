#!/usr/bin/env python3
# Power menu popup for the power icon on the bar: shutdown, lock, sleep,
# logout and restart in a row
import os
import subprocess

import popup
from popup import Gtk

CSS = """
window {
  border: none;
}

.power-menu {
  border: solid 4px $text;
}

.power-button {
  padding: 8px;
}

.power-button:hover {
  background-color: $hover;
}
"""


ACTIONS = [
    ("shutdown_icon.svg", ["systemctl", "poweroff"]),
    ("lock_icon.svg", ["dm-tool", "lock"]),
    ("sleep_icon.svg", ["systemctl", "suspend"]),
    ("logout_icon.svg", ["loginctl", "kill-session", os.environ.get("XDG_SESSION_ID", "")]),
    ("restart_icon.svg", ["systemctl", "reboot"]),
]


def on_clicked(_button, command):
    subprocess.Popen(command, start_new_session=True)
    Gtk.main_quit()


menu = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
menu.get_style_context().add_class("power-menu")
for icon, command in ACTIONS:
    button = Gtk.Button(image=popup.icon(icon))
    button.get_style_context().add_class("power-button")
    button.connect("clicked", on_clicked, command)
    menu.pack_start(button, False, False, 0)
popup.run(menu, CSS)
