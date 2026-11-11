// The workspaces in the top bar: small dots, used ones lighter, the current one a short accent bar.
// With Quickshell bind count, current and used to Hyprland.workspaces (Quickshell.Hyprland).
import QtQuick

Row {
    id: root

    property int count: 5
    /// Index of the current workspace, from 0.
    property int current: 0
    /// Indices that hold windows.
    property var used: []
    signal activated(int index)

    spacing: 5

    Repeater {
        model: root.count
        Rectangle {
            width: index === root.current ? 18 : 5
            height: 5
            radius: 2.5
            anchors.verticalCenter: parent.verticalCenter
            color: index === root.current ? Theme.accent : hh.hovered ? Theme.text : root.used.indexOf(index) >= 0 ? Theme.textMuted : Theme.borderStrong
            Behavior on width { NumberAnimation { duration: Theme.durBase; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeInOut } }
            Behavior on color { ColorAnimation { duration: Theme.durBase } }
            HoverHandler { id: hh }
            TapHandler { onTapped: root.activated(index) }
        }
    }
}
