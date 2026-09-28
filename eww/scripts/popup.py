# Shared code for the bar popups. They close on any click outside of them (or
# Escape), like a tray menu. eww windows can't grab the pointer, so each popup
# runs as its own GTK window and grabs the pointer while it is open.
import gi

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
from gi.repository import Gdk, GLib, Gtk

# Same position the eww popups used: 42px from the left, 2px from the bottom
X_OFFSET = 42
Y_OFFSET = 2

# Colors match eww.scss
BASE_CSS = """
* {
  all: unset;
  font-family: 'Source Code Pro', 'DejaVu Sans Mono', 'Noto Sans Mono', 'JetBrains Mono', 'Liberation Mono', monospace;
  font-size: 16px;
  font-weight: 500;
}

window {
  background-color: #29293e;
  border: solid 4px #ffdadf;
}
"""


def grab_pointer(window):
    seat = Gdk.Display.get_default().get_default_seat()
    status = seat.grab(
        window.get_window(), Gdk.SeatCapabilities.ALL, True, None, None, None
    )
    # The grab can fail while the click that launched us is still held; retry
    return status != Gdk.GrabStatus.SUCCESS


# Close on release rather than press, so the release of a click on the bar
# button doesn't reach eww and reopen the popup
def on_button_release(window, event):
    width, height = window.get_size()
    if not (0 <= event.x < width and 0 <= event.y < height):
        Gtk.main_quit()
    return False


def on_key_press(window, event):
    if event.keyval == Gdk.KEY_Escape:
        Gtk.main_quit()
    return False


def run(child, css):
    provider = Gtk.CssProvider()
    provider.load_from_data((BASE_CSS + css).encode())
    Gtk.StyleContext.add_provider_for_screen(
        Gdk.Screen.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_USER
    )

    window = Gtk.Window(type=Gtk.WindowType.POPUP)
    window.add(child)
    window.connect("button-release-event", on_button_release)
    window.connect("key-press-event", on_key_press)
    window.connect("destroy", Gtk.main_quit)

    window.show_all()
    monitor = Gdk.Display.get_default().get_monitor(0).get_geometry()
    _, height = window.get_size()
    window.move(
        monitor.x + X_OFFSET, monitor.y + monitor.height - height - Y_OFFSET
    )

    if grab_pointer(window):
        GLib.timeout_add(50, grab_pointer, window)

    Gtk.main()
