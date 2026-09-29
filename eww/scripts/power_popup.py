#!/usr/bin/env python3
# Power menu popup for the power icon on the bar: shutdown, lock, sleep,
# logout and restart in a row
import os
import subprocess

import gi

gi.require_version("GdkPixbuf", "2.0")
from gi.repository import GdkPixbuf

import popup
from popup import Gtk

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")

CSS = """
.power-menu {
  padding: 4px;
}

.power-button {
  padding: 8px;
  margin: 2px;
}

.power-button:hover {
  background-color: #7c7cbf;
}
"""


def logout():
    return ["loginctl", "terminate-session", os.environ.get("XDG_SESSION_ID", "")]


ACTIONS = [
    ("shutdown_icon.svg", lambda: ["systemctl", "poweroff"]),
    ("lock_icon.svg", lambda: ["dm-tool", "lock"]),
    ("sleep_icon.svg", lambda: ["systemctl", "suspend"]),
    ("logout_icon.svg", logout),
    ("restart_icon.svg", lambda: ["systemctl", "reboot"]),
]


def on_clicked(_button, command):
    subprocess.Popen(command(), start_new_session=True)
    Gtk.main_quit()


menu = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
menu.get_style_context().add_class("power-menu")
for icon, command in ACTIONS:
    pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
        os.path.join(ASSETS, icon), 20, 20
    )
    button = Gtk.Button(image=Gtk.Image.new_from_pixbuf(pixbuf))
    button.get_style_context().add_class("power-button")
    button.connect("clicked", on_clicked, command)
    menu.pack_start(button, False, False, 0)
popup.run(menu, CSS)
