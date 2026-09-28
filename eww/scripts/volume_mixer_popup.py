#!/usr/bin/env python3
# Volume mixer popup for the sound icon on the bar: one column for the default
# sink ("Master") and one per application playing audio
import json
import os
import subprocess

import gi

gi.require_version("GdkPixbuf", "2.0")
from gi.repository import GdkPixbuf

import popup
from popup import Gtk

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")

CSS = """
.volume-mixer {
  padding: 16px 8px 4px 0px;
}

.mixer-row {
  padding: 8px;
}

.mixer-name {
  color: #ffdadf;
}

.mixer-scale {
  min-height: 150px;
  min-width: 16px;
  padding-bottom: 16px;
}

.mixer-scale trough {
  background-color: #0d0c1e;
}

.mixer-scale highlight {
  background-color: #7c7cbf;
}

.mixer-scale slider {
  background-color: #ffdadf;
  min-width: 12px;
  min-height: 12px;
}

.mixer-mute:hover {
  background-color: #7c7cbf;
}
"""


def pactl(*args):
    return subprocess.run(["pactl", *args], capture_output=True, text=True).stdout


def first_channel_percent(volume):
    channel = next(iter(volume.values()), {"value_percent": "0%"})
    return int(channel["value_percent"].rstrip("%"))


def get_master():
    default = pactl("get-default-sink").strip()
    for sink in json.loads(pactl("-f", "json", "list", "sinks") or "[]"):
        if sink["name"] == default:
            return first_channel_percent(sink["volume"]), sink["mute"]
    return 0, False


def get_sink_inputs():
    inputs = []
    for sink_input in json.loads(pactl("-f", "json", "list", "sink-inputs") or "[]"):
        props = sink_input["properties"]
        name = props.get("application.name") or props.get("media.name") or "unknown"
        inputs.append(
            (
                sink_input["index"],
                name,
                first_channel_percent(sink_input["volume"]),
                sink_input["mute"],
            )
        )
    return inputs


def mute_icon(muted):
    name = "sound_muted_icon.png" if muted else "sound_icon.png"
    pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(os.path.join(ASSETS, name), 20, 20)
    return Gtk.Image.new_from_pixbuf(pixbuf)


# Name written top to bottom, one character per line, cut to 12 characters
def mixer_row(name, volume, muted, set_volume, toggle_mute):
    label = Gtk.Label(label="\n".join(name[:12]), valign=Gtk.Align.START)
    label.get_style_context().add_class("mixer-name")

    scale = Gtk.Scale.new_with_range(Gtk.Orientation.VERTICAL, 0, 100, 1)
    scale.get_style_context().add_class("mixer-scale")
    scale.set_inverted(True)
    scale.set_draw_value(False)
    scale.set_value(volume)
    scale.connect("value-changed", lambda s: set_volume(int(s.get_value())))

    button = Gtk.Button()
    button.get_style_context().add_class("mixer-mute")
    button.add(mute_icon(muted))

    def on_click(_):
        nonlocal muted
        muted = not muted
        toggle_mute()
        button.get_child().destroy()
        button.add(mute_icon(muted))
        button.show_all()

    button.connect("clicked", on_click)

    controls = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    controls.pack_start(scale, False, False, 0)
    controls.pack_start(button, False, False, 0)

    row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, homogeneous=True)
    row.get_style_context().add_class("mixer-row")
    row.add(label)
    row.add(controls)
    return row


mixer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, homogeneous=True)
mixer.get_style_context().add_class("volume-mixer")

volume, muted = get_master()
mixer.add(
    mixer_row(
        "Master",
        volume,
        muted,
        lambda v: pactl("set-sink-volume", "@DEFAULT_SINK@", f"{v}%"),
        lambda: pactl("set-sink-mute", "@DEFAULT_SINK@", "toggle"),
    )
)

for index, name, volume, muted in get_sink_inputs():
    mixer.add(
        mixer_row(
            name,
            volume,
            muted,
            lambda v, i=index: pactl("set-sink-input-volume", str(i), f"{v}%"),
            lambda i=index: pactl("set-sink-input-mute", str(i), "toggle"),
        )
    )

popup.run(mixer, CSS)
