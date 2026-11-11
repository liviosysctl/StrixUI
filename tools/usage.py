"""How each component and screen is written in the two front ends. build.py appends this to every README."""

# component name: (QML types, QML example)
QML = {
    'Button': ('Button', 'Button { text: "Install"; variant: "primary"; onClicked: backend.call("install") }\nButton { text: "Checking"; loading: true }'),
    'IconButton': ('IconButton, ToolTip', 'IconButton {\n    id: off\n    iconName: "power"\n    danger: true\n    ToolTip { text: "Shut down"; visible: off.hovered }\n}'),
    'TextField': ('TextField', 'TextField { label: "Name"; help: "Lowercase letters and digits"; placeholderText: "strix" }\nTextField { id: pw; shape: "line"; echoMode: TextInput.Password; error: wrong ? "Wrong password" : "" }  // pw.shake()'),
    'SearchField': ('SearchField', 'SearchField { width: 300; onAccepted: search.call("query", { text: text }) }'),
    'Switch': ('Switch', 'Switch { text: "Keep this theme"; checked: theme.kept; onToggled: theme.call("keep", { kept: checked }) }'),
    'Checkbox': ('CheckBox', 'CheckBox { text: "Wi-Fi"; checked: true }'),
    'Radio': ('RadioButton, ButtonGroup', 'ButtonGroup { id: look }\nRadioButton { text: "Dark"; checked: true; ButtonGroup.group: look }\nRadioButton { text: "Light"; ButtonGroup.group: look }'),
    'Segmented': ('Segmented', 'Segmented { model: ["Dark", { text: "Light", enabled: false }]; currentIndex: 0; onActivated: i => ... }'),
    'Slider': ('Slider', 'Slider { iconName: "volume-2"; value: 0.62; onMoved: audio.volume = value }'),
    'Progress': ('ProgressBar', 'ProgressBar { value: 0.62; label: "Downloading"; valueText: "62%" }\nProgressBar { indeterminate: true }'),
    'Ring': ('Ring', 'Ring { value: 0.24; label: "RAM" }'),
    'Badge': ('Badge, Dot', 'Badge { text: "3"; kind: "count" }\nDot { live: true }'),
    'Tooltip': ('ToolTip', 'ToolTip { text: "Shut down"; visible: parent.hovered }'),
    'Notification': ('Notification', 'Notification { title: n.summary; body: n.body; time: "now"; urgency: n.urgency === NotificationUrgency.Critical ? "critical" : "normal"; actions: ["Restart", "Later"] }'),
    'Osd': ('Osd', 'Osd { iconName: "volume-2"; value: Pipewire.defaultAudioSink.audio.volume }'),
    'Dialog': ('Dialog', 'Dialog { id: ask; title: "Erase the stick?"; text: "Everything on it is lost."; acceptText: "Erase"; danger: true; onAccepted: backend.call("erase") }\n// ask.open()'),
    'List': ('ListRow', 'ListView {\n    model: apps\n    delegate: ListRow { width: ListView.view.width; text: name; iconName: icon; detail: keys; selected: ListView.isCurrentItem }\n}'),
    'SettingRow': ('SettingRow', 'SettingRow { title: "Change theme"; text: "Another god every 10 minutes"; Switch { checked: true } }'),
    'InfoBlock': ('InfoBlock', 'InfoBlock { title: "strix"; model: [["OS", "Strix 0.1"], ["Theme", Theme.gods[Theme.current].name + ", dark"]] }'),
    'Card': ('Card', 'Card { title: "Firefox"; text: "Web browser"; interactive: true; onClicked: ... }'),
    'Calendar': ('Calendar', 'Calendar { onPicked: day => ... }'),
    'ContextMenu': ('Menu, MenuItem, MenuSeparator', 'Menu {\n    id: menu\n    MenuItem { text: "Copy"; iconName: "copy"; shortcut: "Ctrl C" }\n    MenuSeparator {}\n    MenuItem { text: "Delete"; iconName: "trash-2"; danger: true }\n}\n// menu.popup()'),
    'Search': ('SearchField, SearchHit, KeyCaps, Surface', 'Surface {\n    // in a full-screen overlay layer over the dimmed desktop\n    SearchField { id: q; onTextChanged: search.call("query", { text: q.text }, r => hits.model = r) }\n    ListView { id: hits; delegate: SearchHit { text: modelData.title; hits: modelData.hits; path: modelData.path; kind: modelData.kind; iconName: modelData.icon; keys: modelData.keys } }\n}'),
    'TopBar': ('Workspaces, Meter, Label, Icon, Dot', 'PanelWindow {  // Quickshell, anchored top, no background\n    Workspaces { count: 5; current: Hyprland.focusedWorkspace.id - 1; onActivated: i => Hyprland.dispatch("workspace " + (i + 1)) }\n    Meter { label: "CPU"; value: cpu }\n}'),
    'EdgeDock': ('EdgeDock', 'PanelWindow {  // Quickshell, anchored to the bottom edge\n    EdgeDock {\n        out: edge.hovered\n        Button { small: true; variant: "quiet"; iconName: "settings" }\n    }\n    HoverHandler { id: edge }\n}'),
    'MediaPlayer': ('MediaPlayer', 'MediaPlayer { property var p: Mpris.players.values[0]; title: p.trackTitle; artist: p.trackArtist; cover: p.trackArtUrl; playing: p.isPlaying; position: p.position; length: p.length; onToggle: p.togglePlaying() }'),
    'Visualizer': ('Visualizer', 'Visualizer { values: cava.bars }  // numbers from 0 to 1, from a cava Process'),
    'SlantCard': ('SlantCard', 'Row {\n    spacing: -37\n    Repeater {\n        model: Theme.order\n        SlantCard { source: Theme.wallpaper(modelData); name: Theme.gods[modelData].name; caption: "dark"; selected: index === picker.index }\n    }\n}'),
    'WindowFrame': ('WindowFrame', 'WindowFrame { title: "Bootstick"; subtitle: "Strix 0.1"; active: true; Label { text: "The stick is ready." } }'),
}

SCREENS = {
    'LockScreen': 'A `WlSessionLock` from Quickshell with a `WlSessionLockSurface` per screen. Inside: `Wallpaper { dim: true }`, the clock in `Label { textStyle: "clock" }`, `TextField { shape: "line"; echoMode: TextInput.Password }` with `shake()` after a wrong password, the session `IconButton`s, `Wordmark`, and `Plate` with the caption. Which god comes at each lock is decided by the Rust theme service (`strix_design::LockRotation`); the lock screen only shows it with `Theme.preview(id)`.',
    'Desktop': 'Several Quickshell windows: a `PanelWindow` at the top for the bar (Workspaces, Meter), one at the bottom for the EdgeDock, one top right for Notification (Quickshell.Services.Notifications), one bottom centre for the Osd. Hyprland frames the app windows.',
    'ThemePicker': 'A full-screen overlay `PanelWindow` (layer overlay, keyboard focus exclusive) with `Wallpaper { dim: true }`, a row of SlantCard, a Segmented for the variant and `Switch { text: "Keep this theme" }` with KeyCaps K. The cycle (every 10 minutes, Keep) runs in the Rust theme service (`strix_design::Cycle`); the picker sends the choice and the keep flag over its Backend socket.',
    'Cheatsheet': 'A full-screen overlay `PanelWindow` with a Surface, a SearchField as filter, and the groups of `strix_design::HOTKEYS` in three columns of rows with KeyCaps. Hyprland opens it: `bind = SUPER, K, exec, qs ipc call cheatsheet toggle` to an `IpcHandler` in the shell.',
    'SettingsHotkeys': 'The Settings app, a Quickshell `FloatingWindow`: a WindowFrame body with a navigation of ListRow and a column of HotkeyRow. The Rust settings back end owns the bindings, starts from `strix_design::HOTKEYS`, checks for clashes and writes the Hyprland binds.',
    'Terminal': 'Not a component: Ghostty reads the `term-` colours from the theme engine; see surfaces.md.',
    'BootSplash': 'Not Quickshell: Plymouth, rendered by the theme engine from the theme; see surfaces.md.',
}

TAURI = 'The markup above with `tokens.css`, `components/bundle.css` and `components/bundle.js`; call `Kit.hydrate(root)` after adding it.'


def section(name, screen=False):
    if screen:
        text = SCREENS.get(name)
        return '\n## In Quickshell\n\n%s\n' % text if text else ''
    if name not in QML:
        return ''
    types, example = QML[name]
    return ('\n## In Quickshell (Linux shell and apps)\n\n`import Strix`, then %s.\n\n```qml\n%s\n```\n\n## In Tauri (Windows app)\n\n%s\n'
            % (', '.join('`%s`' % t.strip() for t in types.split(',')), example, TAURI))
