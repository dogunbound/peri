#!/bin/bash

# 1. Get the ID of the currently focused window
WIN_ID=$(xprop -root _NET_ACTIVE_WINDOW | awk '{print $5}')

# 2. Get the PID of the Alacritty GUI process
ALACRITTY_PID=$(xprop -id "$WIN_ID" _NET_WM_PID | awk '{print $3}')

if [ -n "$ALACRITTY_PID" ] && ps -p "$ALACRITTY_PID" -o comm= | grep -q "alacritty"; then
    
    # 3. FIND THE SHELL: Find the child process of Alacritty
    # pgrep -P looks for processes whose parent is the Alacritty PID
    # We take the first child (the shell)
    SHELL_PID=$(pgrep -P "$ALACRITTY_PID" | head -n 1)

    if [ -n "$SHELL_PID" ]; then
        # Get the CWD of the SHELL, not the GUI
        CWD=$(readlink -f "/proc/$SHELL_PID/cwd")
    else
        # Fallback to GUI CWD if no child process is found
        CWD=$(readlink -f "/proc/$ALACRITTY_PID/cwd")
    fi

    /usr/bin/alacritty --working-directory "$CWD" &
else
    # Fallback: If Alacritty isn't focused, just launch a normal instance
    /usr/bin/alacritty &
fi
