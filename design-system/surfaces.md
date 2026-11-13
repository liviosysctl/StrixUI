# Surfaces

Every own program of Strix has its back end in Rust and its front end in Quickshell (QML), for the shell and for every app. The previews draw the same components in HTML; names, states and measurements are the same in both.

| Surface | Front end | Back end | Takes |
|---|---|---|---|
| Desktop shell: bar, dock, lock screen, greeter, theme picker, search, cheat sheet, notifications, OSD | Quickshell, QML module `Strix` | Rust services: theme, search, settings | Every token from `Theme`; the colours at runtime from the theme engine through `ThemeFile`; the components by the same name |
| Linux apps: settings, store, graphical installer | Quickshell, a `FloatingWindow` per app, QML module `Strix` | Rust, one service per app | The same module; Hyprland frames the window like any other |
| Theme engine | none | Rust (`strix-theme`) | `themes/<god>/theme.toml`, one per god |
| Compositor | Hyprland | | Window geometry, `border-active` and the animation block in the Motion section |
| Terminal | Ghostty | | `term-` colours, `mono` at 13px with 20px line height, a block cursor in `term-cursor`, the god's plate as `background-image` at `background-image-opacity = 0.06`, the prompt `›` in the accent |
| Boot splash | Plymouth | theme engine | `background`, `text`, `text-muted`, `line`, `accent`, `error`; the wordmark in `display`; the lozenge rule; the running line |
| Text installer | console | | `term-` colours with colour 0 as `background` and colour 7 as `term-foreground`; the accent for the current step and the logo, white only for what the person types |

## Quickshell: the shell and the Linux apps

- Import path: the `qml/` folder of the repository (the shell's config can link it, or the Nix package puts it on `QML_IMPORT_PATH`). Then `import Strix`; the Quickshell-only parts are in `import Strix.Shell`.
- `ThemeFile {}` once in `shell.qml` (and in each app) watches `/run/strix/theme/tokens.json`, which the theme engine rewrites on every switch, and recolours everything at once. Without the engine the built-in Saturnus stays.
- Tokens: `Theme.<token in camelCase>`, sizes in pixels at scale 1, durations in milliseconds, curves for `Easing.BezierSpline`: `NumberAnimation { duration: Theme.durBase; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeOut }`. `Theme.order`, `Theme.gods` and `Theme.wallpaper(id)` serve the theme picker.
- Type: `Label { textStyle: "caption" }`; the fonts ship inside the module.
- Components build on `QtQuick.Templates`, so keyboard focus, accessibility and Popup handling are Qt's own. Needs Qt 6.8 or newer (QtQuick.Shapes with `fillItem` and the curve renderer, QtQuick.Effects).
- Screens are assembled in the shell from the components with Quickshell's own types: `PanelWindow` for the bar, dock, notifications and OSD; an overlay layer for search, the theme picker and the cheat sheet; `WlSessionLock` for the lock screen. Each screen's README says how.
- `qml/gallery.qml` shows every QML component; `tools/render_qml.py` renders it for every theme and fails on any QML error.

## Front end and back end

Quickshell has no general D-Bus client in QML, so a front end talks to its Rust back end over a Unix socket:

- Path: `$XDG_RUNTIME_DIR/strix/<service>.sock`, owned by the back end (a systemd user service).
- One JSON object per line. A call: `{"id": 7, "method": "query", "params": {"text": "term"}}`. Its answer: `{"id": 7, "result": ...}` or `{"id": 7, "error": "No index yet"}`. A message the back end sends by itself: `{"event": "index-ready", "data": {...}}`.
- `Backend { service: "search" }` from `Strix.Shell` does this on the QML side: `call(method, params, done)`, the signals `event(name, data)` and `failed(method, message)`, reconnecting when the service restarts.
- Hyprland and scripts reach the shell with Quickshell's `IpcHandler`: `bind = SUPER, K, exec, qs ipc call cheatsheet toggle`.
- State that only needs to be read (the current theme) is a file the back end writes atomically and the front end watches, like `tokens.json`. D-Bus stays where the system needs it, between back ends and system services (polkit, logind, NetworkManager).

## Rust: every back end

- The crate `strix-design` (`rust/strix-design/` in the repository), without dependencies: `strix-design = { git = "https://github.com/liviosysctl/strixui" }`.
- Holds every token (`tokens::SPACE_3`, `tokens::DUR_BASE`, `tokens::EASE_OUT`, `tokens::text::BODY`), the eight themes (`THEMES`, `theme("janus")`, every colour as `Color` with `hex()` and `contrast()`), the theme cycle (`Cycle`: 10 minutes, Keep, the count goes on while kept) and the lock screen rotation (`LockRotation`), and the default hotkeys (`HOTKEYS`).
- Its tests check every theme against the contrast rules of the theme engine and that no two hotkeys share keys.

## HTML: the previews

- `tokens.css`, `components/bundle.css` and `components/bundle.js` with the fonts next to them; nothing loads from the network.
- `<html data-theme="saturnus">` sets the theme; `Kit.theme()`, `Kit.onTheme(fn)` and `Kit.god(id)` follow and describe it.
- `bundle.js` uses no `eval` and no inline event handlers, so a content security policy without `'unsafe-eval'` works.
- Motion follows `prefers-reduced-motion`.

## Sizes on a 2560 by 1440 screen at scale 1

The Screens previews are drawn on a 1280 by 720 board, which is that screen at half size. Measurements of components do not double: a button is 28px high on the real screen, the bar 26px, the dock 28px once it is out. What grows with the screen is the room between things: the lock screen column sits 128px from the left edge, and the stacked clock is set at twice the `clock` style.

## Console

The installer runs in the Linux console in Terminus (ter-v16n). Neither the serif nor the blackletter is available there: the wordmark is drawn as block characters with a one-cell shadow, and titles are bold mono.
