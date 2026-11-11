# Cheatsheet

The cheat sheet (Super K) is the one place that explains the keys. Components carry no instructions of their own; at most a single key chip stands next to a control where one key matters (Esc in Search, K in the theme picker). Everything else is learned here.

- Over the dimmed desktop, a wide panel lists every hotkey of the system in groups: Learn, Apps, Windows, Workspaces, Style, Capture, Clipboard, System. Group names in the serif italic, actions in mono, keys as chips at the right.
- Typing filters by action or by keys, fuzzy as in Search: "shot" finds the screenshots, "super shift" every binding with both. Up and Down move, Enter runs the action, Esc clears the field and a second Esc closes.
- Edit opens Settings › Hotkeys. The pencil next to a row opens Settings at that very row, marked for a moment, ready to take new keys.
- The list is read from the live bindings, so a hotkey changed or added in Settings shows here at once.

## In Quickshell

A full-screen overlay `PanelWindow` with a Surface, a SearchField as filter, and the groups of `strix_design::HOTKEYS` in three columns of rows with KeyCaps. Hyprland opens it: `bind = SUPER, K, exec, qs ipc call cheatsheet toggle` to an `IpcHandler` in the shell.
