// The line from a Quickshell front end to its Rust back end: a Unix socket in
// $XDG_RUNTIME_DIR/strix/<service>.sock, one JSON object per line (see ipc.md of the design system).
//
//   Backend {
//       id: search
//       service: "search"
//       onEvent: (name, data) => if (name === "index-ready") ...
//   }
//   search.call("query", { text: "term" }, result => hits = result)
import QtQuick
import Quickshell
import Quickshell.Io

Socket {
    id: root

    /// Name of the service; the socket file is <service>.sock.
    property string service
    /// Reconnect after this many milliseconds when the back end is not there (yet).
    property int retry: 2000

    signal event(string name, var data)
    signal failed(string method, string message)

    property int next: 1
    property var waiting: ({})

    /// Calls `method` with `params`; `done(result)` gets the answer.
    function call(method, params, done) {
        if (!connected) {
            failed(method, "not connected")
            return
        }
        const id = next++
        waiting[id] = { method: method, done: done }
        write(JSON.stringify({ id: id, method: method, params: params || {} }) + "\n")
        flush()
    }

    path: Quickshell.env("XDG_RUNTIME_DIR") + "/strix/" + service + ".sock"
    connected: true

    onConnectedChanged: if (!connected) again.restart()
    onError: again.restart()

    parser: SplitParser {
        onRead: line => {
            let m
            try { m = JSON.parse(line) } catch (e) { console.warn("Strix: bad line from " + root.service + ": " + line); return }
            if (m.event !== undefined) {
                root.event(m.event, m.data)
                return
            }
            const w = root.waiting[m.id]
            if (!w) return
            delete root.waiting[m.id]
            if (m.error !== undefined) root.failed(w.method, m.error)
            else if (w.done) w.done(m.result)
        }
    }

    property Timer again: Timer {
        interval: root.retry
        onTriggered: root.connected = true
    }
}
