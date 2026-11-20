// The workspaces in the top bar: small dots, used ones lighter, the current one a short accent bar.
// The bar moves elastically: its leading edge runs ahead and the trailing edge catches up.
// With Quickshell bind count, current and used to Hyprland.workspaces (Quickshell.Hyprland).
import QtQuick

Item {
    id: root

    property int count: 5
    /// Index of the current workspace, from 0.
    property int current: 0
    /// Indices that hold windows.
    property var used: []
    signal activated(int index)

    readonly property int dot: 5
    readonly property int wide: 18
    readonly property int gap: 5
    property int previous: current

    function slotX(i) { return i * (dot + gap) }

    implicitWidth: count * dot + (count - 1) * gap + wide - dot
    implicitHeight: 9

    onCurrentChanged: {
        const forward = current > previous
        previous = current
        const l = slotX(current)
        leftEdge.to = l
        rightEdge.to = l + wide
        // the edge in the direction of travel goes first
        leftEdge.duration = forward ? Theme.durBase : Theme.durFast
        rightEdge.duration = forward ? Theme.durFast : Theme.durBase
        leftEdge.restart()
        rightEdge.restart()
    }

    Repeater {
        id: dots
        model: root.count
        Rectangle {
            readonly property bool here: index === root.current
            x: root.slotX(index) + (index > root.current ? root.wide - root.dot : 0)
            y: (root.height - height) / 2
            width: root.dot
            height: root.dot
            radius: root.dot / 2
            scale: hh.hovered && !here ? 1.6 : 1
            color: hh.hovered ? Theme.text : root.used.indexOf(index) >= 0 ? Theme.textMuted : Theme.borderStrong
            Behavior on x { NumberAnimation { duration: Theme.durBase; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeInOut } }
            Behavior on color { ColorAnimation { duration: Theme.durBase } }
            Behavior on scale { NumberAnimation { duration: Theme.durFast; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeSpring } }
            HoverHandler { id: hh; cursorShape: Qt.PointingHandCursor }
            TapHandler { onTapped: root.activated(index) }
        }
    }

    Rectangle {
        id: pill
        // the two edges, moved by leftEdge and rightEdge
        property real l: 0
        property real r: root.wide
        Component.onCompleted: { l = root.slotX(root.current); r = l + root.wide }
        x: l
        y: (root.height - height) / 2
        width: Math.max(root.dot, r - l)
        height: root.dot
        radius: root.dot / 2
        color: Theme.accent
    }

    NumberAnimation { id: leftEdge; target: pill; property: "l"; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeOut }
    NumberAnimation { id: rightEdge; target: pill; property: "r"; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeOut }
}
