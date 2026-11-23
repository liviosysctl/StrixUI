// One of several independent choices: a small square, filled with an accent square when on.
import QtQuick
import QtQuick.Templates as T

T.CheckBox {
    id: control

    // The hand over what can be pressed, as on every clickable part of the shell
    HoverHandler { cursorShape: Qt.PointingHandCursor }

    // The text already leaves room for the indicator at its left (leftPadding of contentItem)
    implicitWidth: text !== "" ? implicitContentWidth : implicitIndicatorWidth
    implicitHeight: Theme.mark
    spacing: Theme.space2
    padding: 0
    hoverEnabled: true
    opacity: enabled ? 1 : Theme.dimDisabled

    indicator: Rectangle {
        implicitWidth: Theme.icon
        implicitHeight: Theme.icon
        y: (control.height - height) / 2
        radius: Theme.radiusSm
        color: Theme.surfaceSunken
        border.width: Theme.lineHair
        border.color: control.checked ? Theme.accentText : Theme.borderStrong

        Rectangle {
            anchors.centerIn: parent
            width: Theme.space2
            height: Theme.space2
            radius: Theme.radiusSm / 2
            color: Theme.accent
            scale: control.checked ? 1 : 0
            Behavior on scale { NumberAnimation { duration: Theme.durFast; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeSpring } }
        }

        FocusRing { target: control; targetRadius: parent.radius }
    }

    contentItem: Label {
        leftPadding: control.indicator.width + control.spacing
        text: control.text
    }
}
