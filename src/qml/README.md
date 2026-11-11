# Strix for Quickshell

The design system as a QML module, for the shell and every Linux app of Strix. Generated with the rest of `design-system/`: `Theme.qml` and `Icons.qml` come from `tokens.json`, the components from `src/qml/` in the repository.

```qml
import Strix          // Theme, Icons and the components
import Strix.Shell    // ThemeFile and Backend; these need Quickshell

ShellRoot {
    ThemeFile {}      // follows /run/strix/theme/tokens.json
    PanelWindow {
        color: "transparent"
        Button { text: "Install"; variant: "primary" }
    }
}
```

Add this folder to the import path: `QML_IMPORT_PATH=/path/to/design-system/qml`, or a link from the shell's config folder. Needs Qt 6.8 or newer.

| Module | What |
|---|---|
| `Strix` | `Theme` (every token, the eight themes, `apply()` for the engine's tokens.json, `preview(id)`), `Icons`, and the components: Label, Icon, Surface, FocusRing, Button, IconButton, TextField, SearchField, Switch, CheckBox, RadioButton, Segmented, Slider, ProgressBar, Ring, Badge, Dot, ToolTip, KeyCaps, ListRow, Card, Menu, MenuItem, MenuSeparator, Dialog, SettingRow, InfoBlock, Notification, Osd, MediaPlayer, Visualizer, Calendar, Rule, Plate, Wordmark, WindowFrame, Wallpaper, Workspaces, Meter, EdgeDock, SlantCard, SearchHit, HotkeyRow |
| `Strix.Shell` | `ThemeFile` (watches the engine's tokens.json), `Backend` (the socket to a Rust back end, one JSON object per line) |

Each component's README in `components/` has its QML example. `gallery.qml` shows them all:

```sh
qml -I design-system/qml design-system/qml/gallery.qml
python3 tools/render_qml.py          # PNG per theme into build/renders/, fails on any QML error
```
