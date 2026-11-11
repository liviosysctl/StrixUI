// Bars that follow the sound, hair thin like the hatching of an engraving. Grey at rest, the accent at the peaks.
// values: numbers from 0 to 1, one per bar (cava gives them); peak: bars above it turn to the accent.
import QtQuick

Item {
    id: root

    property var values: []
    property real peak: 0.8

    implicitWidth: 320
    implicitHeight: 96

    Repeater {
        model: root.values.length
        Rectangle {
            readonly property real v: Math.max(0.04, Math.min(1, root.values[index]))
            x: root.values.length > 1 ? index * (root.width - 1) / (root.values.length - 1) : 0
            width: 1
            height: root.height * v
            y: root.height - height
            color: v >= root.peak ? Theme.accentText : Theme.textMuted
            Behavior on height { NumberAnimation { duration: Theme.durFast } }
        }
    }
}
