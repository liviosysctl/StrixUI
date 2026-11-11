// The one focus ring: 2px in `focus` after a 2px gap in `background`. Shown only for keyboard focus.
// It surrounds its parent (a control's background or indicator); `target` is the control whose focus counts.
import QtQuick

Rectangle {
    id: ring

    property var target: parent
    property real targetRadius: Theme.radiusSm

    anchors.fill: parent
    anchors.margins: -4
    radius: targetRadius + 4
    color: "transparent"
    border.width: 2
    border.color: Theme.focus
    visible: !!target && !!target.visualFocus
    z: 10

    Rectangle {
        anchors.fill: parent
        anchors.margins: 2
        radius: Math.max(0, ring.radius - 2)
        color: "transparent"
        border.width: 2
        border.color: Theme.background
    }
}
