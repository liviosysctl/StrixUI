// Every QML component on one board, for a look and for the render test.
//   qml -I design-system/qml design-system/qml/gallery.qml        (Qt's qml tool)
//   python3 tools/render_qml.py                                    (PNG of every theme into build/renders/)
// Another theme: qml -I design-system/qml design-system/qml/gallery.qml -- --theme=janus
import QtQuick
import Strix

Rectangle {
    id: board

    width: 1280
    height: 1220
    color: Theme.background

    Component.onCompleted: {
        const id = Qt.application.arguments.find(a => a.startsWith("--theme="))
        if (id) Theme.preview(id.slice(8))
    }

    component Caption: Label { textStyle: "micro"; color: Theme.textFaint; font.capitalization: Font.AllUppercase; font.letterSpacing: 1.2 }

    Wallpaper { x: 880; y: 0; width: 400; height: 300; dim: true }
    Column {
        x: 900; y: 20
        spacing: 6
        Wordmark { }
        Plate { width: 360; wrapMode: Text.WordWrap; text: Theme.about.plate }
    }

    Row {
        x: 32
        y: 28
        spacing: 48

        // ------------------------------------------------------------ column 1
        Column {
            spacing: 18
            width: 320

            Caption { text: "Buttons" }
            Row {
                spacing: 8
                Button { text: "Install"; variant: "primary" }
                Button { text: "Check"; loading: true }
                Button { text: "Cancel"; variant: "quiet" }
            }
            Row {
                spacing: 8
                Button { text: "Erase disk"; variant: "danger"; iconName: "trash-2" }
                Button { text: "Later"; enabled: false }
                IconButton { iconName: "power"; danger: true }
                IconButton { iconName: "settings" }
                IconButton { iconName: "bell"; checkable: true; checked: true }
            }

            Caption { text: "Fields" }
            TextField { label: "Name"; placeholderText: "strix"; help: "Lowercase letters and digits" }
            TextField { label: "Password"; text: "nocte"; echoMode: TextInput.Password; error: "Wrong password" }
            SearchField { width: 300; KeyCaps { keys: "Super Space"; ink: Theme.textFaint } }
            TextField { shape: "line"; width: 200; placeholderText: "Password" }

            Caption { text: "Choices" }
            Row {
                spacing: 16
                Switch { text: "Keep this theme"; checked: true }
                Switch { text: "Off" }
            }
            Row {
                spacing: 16
                CheckBox { text: "Wi-Fi"; checked: true }
                CheckBox { text: "Bluetooth" }
                RadioButton { text: "Dark"; checked: true }
                RadioButton { text: "Light" }
            }
            Segmented { model: ["Dark", { text: "Light", enabled: false }, "Auto"]; currentIndex: 0 }
            Slider { width: 280; iconName: "volume-2"; value: 0.62 }
        }

        // ------------------------------------------------------------ column 2
        Column {
            spacing: 18
            width: 320

            Caption { text: "Progress" }
            ProgressBar { width: 300; value: 0.62; label: "Downloading"; valueText: "62%" }
            ProgressBar { width: 300; indeterminate: true }
            Row {
                spacing: 24
                Ring { value: 0.08; label: "CPU" }
                Ring { value: 0.24; label: "RAM" }
                Ring { value: 0.71; label: "Disk" }
            }

            Caption { text: "Badges and keys" }
            Row {
                spacing: 8
                Badge { text: "new" }
                Badge { text: "3"; kind: "count" }
                Badge { text: "live"; kind: "accent"; iconName: "video" }
                Badge { text: "failed"; kind: "error" }
                Dot { anchors.verticalCenter: parent.verticalCenter; live: true }
                KeyCaps { keys: "Super Shift Return" }
            }

            Caption { text: "List" }
            Column {
                width: 320
                ListRow { width: 320; text: "Ghostty"; iconName: "terminal"; detail: "Super Return"; selected: true }
                ListRow { width: 320; text: "Files"; iconName: "folder"; detail: "Super Shift F" }
                ListRow { width: 320; text: "Settings"; iconName: "settings" }
            }

            Caption { text: "Search" }
            Surface {
                width: 320
                height: 92
                elevation: "panel"
                Column {
                    x: 4; y: 6
                    SearchHit { width: 312; text: "Theme picker"; iconName: "palette"; hits: [0, 1, 2, 3, 4]; path: ["Style", "Theme"]; keys: "Super Ctrl Space"; selected: true }
                    SearchHit { width: 312; text: "strix-theme set janus"; kind: "command"; iconName: "square-terminal"; path: ["Command"] }
                }
            }
        }

        // ------------------------------------------------------------ column 3
        Column {
            spacing: 18
            width: 400
            topPadding: 300

            Caption { text: "Notification and OSD" }
            Notification { width: 320; title: "Update ready"; body: "Strix 0.2 is downloaded. Restart to finish."; time: "now"; actions: ["Restart", "Later"] }
            Notification { width: 320; title: "Battery low"; body: "8% left. Plug in the charger."; time: "1 min"; urgency: "critical"; iconName: "triangle-alert" }
            Osd { value: 0.62 }

            Caption { text: "Info and settings" }
            InfoBlock { title: "strix"; model: [["OS", "Strix 0.1"], ["Theme", Theme.about.name + ", dark"], ["Shell", "Quickshell"]] }
            SettingRow { width: 400; title: "Change theme"; text: "Another god every 10 minutes"; Switch { checked: true } }
            SettingRow { width: 400; title: "Wallpaper"; text: "Lock screen"; last: true; Button { small: true; text: "Choose" } }
        }
    }

    Row {
        x: 32
        y: 880
        spacing: 32

        Column {
            spacing: 10
            Caption { text: "Top bar parts" }
            Row {
                spacing: 16
                Workspaces { count: 5; current: 1; used: [0, 3]; anchors.verticalCenter: parent.verticalCenter }
                Meter { label: "CPU"; value: 0.08 }
                Meter { label: "RAM"; value: 0.24 }
            }
            Caption { text: "Dock" }
            Item {
                width: 300; height: 34
                Rectangle { anchors.bottom: parent.bottom; width: parent.width; height: 1; color: Theme.border }
                EdgeDock {
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.bottom: parent.bottom
                    out: true
                    Button { small: true; variant: "quiet"; iconName: "layout-grid"; text: "Apps" }
                    Button { small: true; variant: "quiet"; iconName: "music"; text: "Music" }
                    Button { small: true; variant: "quiet"; iconName: "cpu"; text: "8%" }
                }
            }
            Caption { text: "Calendar" }
            Calendar { month: new Date(2026, 10, 1); today: new Date(2026, 10, 11) }
        }

        Column {
            spacing: 10
            Caption { text: "Window" }
            WindowFrame {
                width: 360; height: 150; title: "Bootstick"; subtitle: "Strix 0.1"
                Label { text: "The stick is ready."; color: Theme.textMuted }
            }
            MediaPlayer { title: "Nocturne in E-flat"; artist: "Chopin, op. 9 no. 2"; position: 74; length: 271; playing: true }
        }

        Column {
            spacing: 10
            Caption { text: "Theme picker card" }
            Row {
                spacing: -37
                SlantCard { source: Theme.wallpaper("janus"); name: "Janus" }
                SlantCard { source: Theme.wallpaper(); name: Theme.about.name; caption: "dark"; selected: true }
                SlantCard { source: Theme.wallpaper("mars"); name: "Mars" }
            }
            HotkeyRow { width: 480; action: "Theme picker"; target: "Themes and wallpapers"; keys: "Super Ctrl Space"; tail: "reset" }
        }
    }
}
