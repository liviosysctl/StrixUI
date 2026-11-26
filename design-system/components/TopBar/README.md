# TopBar

The buttons at the top of the screen. The bar has no band of its own: its buttons stand on the wallpaper, and those that belong together share one plate of smoked glass, parted by hair lines (`ChipGroup` in QML, `.k-group` in HTML).

- Left: search, the clock (a click shows the month under it; while the clock of the desktop is in view only the symbol of the calendar), CPU and memory as one button that opens the system monitor.
- Middle: the workspaces as dots, the active one a pill in the accent.
- Right: the state of the machine (network, Bluetooth, sound, battery, a recording, the microphone, the keyboard layout when there is more than one), each opening its quick panel under it; then the tray, staying awake, the bell with its count and power.
- What is playing is in the dock. Nothing in the bar needs a hint: every button says what it is.
- Height `bar-height`. Values roll when they change; the workspace pill slides.

## In Quickshell (Linux shell and apps)

`import Strix`, then `Workspaces`, `Meter`, `Label`, `Icon`, `Dot`.

```qml
PanelWindow {  // Quickshell, anchored top, no background
    Workspaces { count: 5; current: Hyprland.focusedWorkspace.id - 1; onActivated: i => Hyprland.dispatch("workspace " + (i + 1)) }
    Meter { label: "CPU"; value: cpu }
}
```

## In HTML (the previews)

The markup of the preview with `tokens.css`, `components/bundle.css` and `components/bundle.js`; call `Kit.hydrate(root)` after adding it.
