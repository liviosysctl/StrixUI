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
            const tokens = JSON.parse(text())
            Theme.apply(tokens)
            plate.path = Theme.external && Theme.external.id === tokens.theme ? tokens.dir + "/wallpaper.toml" : ""
        } catch (e) {
            console.warn("Strix: cannot read " + path + ": " + e)
        }
    }
    // no engine (a nested session, a test): the built-in default theme stays
    onLoadFailed: error => Theme.preview(Theme.current)

    // a theme from a theme repository brings its plate caption in wallpaper.toml
    property FileView plate: FileView {
        printErrors: false
        onLoaded: {
            const m = /^caption\s*=\s*"((?:[^"\\]|\\.)*)"/m.exec(text())
            if (m && Theme.external) Theme.external = Object.assign({}, Theme.external, { plate: JSON.parse('"' + m[1] + '"') })
        }
    }
}
