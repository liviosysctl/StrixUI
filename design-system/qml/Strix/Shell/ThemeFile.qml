// Keeps Strix.Theme on the theme the engine applied. Put one in shell.qml:
//   import Strix.Shell
//   ThemeFile {}
// The engine (strix-theme, Rust) writes /run/strix/theme/tokens.json on every switch; this
// watches the file and hands it to Theme.apply(). Needs Quickshell.
import QtQuick
import Quickshell.Io
import Strix

FileView {
    id: file

    path: "/run/strix/theme/tokens.json"
    watchChanges: true
    printErrors: false
    onFileChanged: reload()
    onLoaded: {
        try {
            Theme.apply(JSON.parse(text()))
        } catch (e) {
            console.warn("Strix: cannot read " + path + ": " + e)
        }
    }
    // no engine (a nested session, a test): the built-in default theme stays
    onLoadFailed: error => Theme.preview(Theme.current)
}
