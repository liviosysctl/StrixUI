# TopBar

The status line at the top of the screen. It has no surface of its own: small text and symbols sit straight on the wallpaper, in grey, with the accent for the one active thing.

- Left: search with the clock, then CPU, memory and temperature, each as symbol, a 3px vertical meter and a value.
- Middle: workspaces as dots, the active one a pill in the accent; next to them the playing track.
- Right: recording (with a dot in the accent while it runs), the bell with its count, power in `accent-text`.
- The bar is for reading. Search opens Search, the track opens the media player in the dock, the bell opens notifications, power opens the session menu. Everything adjustable lives in the dock.
- Height `bar-height`. Values roll when they change; the workspace pill slides.

## In Quickshell (Linux shell and apps)

`import Strix`, then `Workspaces`, `Meter`, `Label`, `Icon`, `Dot`.

```qml
PanelWindow {  // Quickshell, anchored top, no background
    Workspaces { count: 5; current: Hyprland.focusedWorkspace.id - 1; onActivated: i => Hyprland.dispatch("workspace " + (i + 1)) }
    Meter { label: "CPU"; value: cpu }
}
```

## In Tauri (Windows app)

The markup above with `tokens.css`, `components/bundle.css` and `components/bundle.js`; call `Kit.hydrate(root)` after adding it.
