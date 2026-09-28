#!/usr/bin/env python3
# Calendar popup for the clock on the bar
import popup
from popup import Gtk

CSS = """
calendar {
  color: #ffdadf;
  padding: 4px;
}

calendar:selected {
  color: #ff828d;
}

calendar:indeterminate {
  color: rgba(255, 218, 223, 0.5);
}

calendar.button:hover {
  color: #7c7cbf;
}
"""

calendar = Gtk.Calendar()
calendar.set_display_options(
    Gtk.CalendarDisplayOptions.SHOW_HEADING
    | Gtk.CalendarDisplayOptions.SHOW_DAY_NAMES
)
popup.run(calendar, CSS)
