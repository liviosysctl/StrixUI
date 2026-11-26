The dock is part of the bottom edge of the screen, not a floating bar. At rest it is a tab 5px high and 128px wide with a short line in the accent, flush with the edge, its corners flaring into it. When the pointer reaches the bottom edge it rises to 38px (one row of controls) and widens to fit its content. When the pointer leaves, it sinks back after a short wait.

- It holds what the bar does not: the tools (a screenshot of a region, one to draw on, the text of a region, a recording of a region, the colour picker), the clipboard history and the theme picker, the night light, and what is playing, the only place for it.
- A click on the title lets the media player grow upward out of it; a second click, Escape or a click elsewhere folds it back. While it is open, the dock stays out.
- Motion: height over `dur-base`, width over `dur-slow`, content fades in `dur-fast` later. A panel scales up from its button over `dur-slow`.
- Markup: `.k-dockbar` (the hot strip along the bottom edge) > `.k-dock` > panels (`.k-panel.k-surface` with an id) + `.k-edge` > `u` (the line in the accent) + `.k-edge-in` > buttons, the title with `data-panel="#id"`. Thin `s` elements separate groups.
- `data-pinned` on `.k-dock` keeps it out, for touch screens.
