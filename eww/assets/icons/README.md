# Themed icons

## nm-applet

These are the symbolic icons from
[network-manager-applet](https://gitlab.gnome.org/GNOME/network-manager-applet),
recolored to the theme's text color (`#ffdadf`). The wired icons also have their
35% opacity removed so they don't look disabled.

They're saved under the names nm-applet uses, in the same layout as the system
`hicolor` icon theme. `up` adds this folder to eww's `XDG_DATA_DIRS`, so eww
finds these ahead of the system icons, while every other program keeps using the
originals. The size folders are symlinks to `scalable/apps`, since GTK prefers
fixed size icons when it has them.

Copyright 2004 - 2015 Red Hat, Inc. Licensed under the GNU General Public
License, version 2 or later (https://www.gnu.org/licenses/old-licenses/gpl-2.0.html),
unlike the rest of this repository.
