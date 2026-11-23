// A short state next to a name: "new", "3", "failed". kind: default, accent, error, count.
import QtQuick

Rectangle {
    id: root

    property string text
    property string kind: "default"
    property string iconName

    readonly property color ink: kind === "accent" || kind === "count" ? Theme.onAccent : kind === "error" ? Theme.error : Theme.textMuted

    implicitWidth: Math.max(Theme.mark, row.implicitWidth + 2 * Theme.space1)
    implicitHeight: Theme.mark
    radius: kind === "count" ? height / 2 : Theme.radiusSm
    color: kind === "accent" || kind === "count" ? Theme.accent : "transparent"
    border.width: Theme.lineHair
    border.color: kind === "accent" || kind === "count" ? Theme.accent : kind === "error" ? Theme.error : Theme.borderStrong

    // A count that changes pops, so a new notification is noticed without a sound.
    property bool _ready: false
    Component.onCompleted: _ready = true
    onTextChanged: if (_ready && kind === "count" && !Theme.reducedMotion) bump.restart()
    SequentialAnimation {
        id: bump
        NumberAnimation { target: root; property: "scale"; to: 1.25; duration: Theme.durInstant; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeOut }
        NumberAnimation { target: root; property: "scale"; to: 1; duration: Theme.durSlow; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeSpring }
    }

    Row {
        id: row
        anchors.centerIn: parent
        spacing: Theme.space1
        Icon { visible: root.iconName !== ""; name: root.iconName; size: Theme.space3; color: root.ink; anchors.verticalCenter: parent.verticalCenter }
        Label { text: root.text; textStyle: "micro"; color: root.ink; anchors.verticalCenter: parent.verticalCenter }
    }
}
