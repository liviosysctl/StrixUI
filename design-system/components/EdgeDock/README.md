# EdgeDock

The dock is part of the bottom edge of the screen, not a floating bar. At rest it is a tab 5px high and 132px wide with a short line in the accent, flush with the edge, its corners flaring into it. When the pointer reaches the bottom edge it rises to 28px and widens to fit its content. When the pointer leaves, it sinks back after a short wait.

- Everything that can be adjusted starts here: settings, the date with the weather, media, Wi-Fi, Bluetooth, sound, about. A click on a symbol lets its panel grow upward out of that symbol; a second click, Escape or a click elsewhere folds it back.
- Main panel: a Segmented with Today (date, weather, calendar, the day as a line), System (three rings and the disk) and About (name, version, channel, and "Check", which runs the update and shows its progress in place).
- Small panels (`data-size="sm"`): Wi-Fi and Bluetooth as a switch with a List, sound as a Slider, media as a MediaPlayer.
- While a panel is open or a control inside has keyboard focus, the dock stays out.
- Motion: height over `dur-base`, width over `dur-slow`, content fades in `dur-fast` later. A panel scales up from its symbol over `dur-slow`.
- Markup: `.k-dockbar` (the hot strip along the bottom edge) > `.k-dock` > panels (`.k-panel.k-surface` with an id) + `.k-edge` > `u` (the line in the accent) + `.k-edge-in` > buttons with `data-panel="#id"` and optional `data-tab`. Thin `s` elements separate groups.
- `data-pinned` on `.k-dock` keeps it out, for touch screens.
