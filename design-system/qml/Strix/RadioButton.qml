// One choice out of a few that are all visible. Put them in a ButtonGroup.
import QtQuick
import QtQuick.Templates as T

T.RadioButton {
    id: control

    implicitWidth: implicitIndicatorWidth + (text !== "" ? spacing + implicitContentWidth : 0)
    implicitHeight: 18
    spacing: Theme.space2
    padding: 0
    hoverEnabled: true
    opacity: enabled ? 1 : Theme.dimDisabled

    indicator: Rectangle {
        implicitWidth: 12
        implicitHeight: 12
        y: (control.height - height) / 2
        radius: 6
        color: Theme.surfaceSunken
        border.width: Theme.lineHair
        border.color: control.checked ? Theme.accentText : Theme.borderStrong

        Rectangle {
            anchors.centerIn: parent
            width: 6
            height: 6
            radius: 3
            color: Theme.accent
            scale: control.checked ? 1 : 0
            Behavior on scale { NumberAnimation { duration: Theme.durFast; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeSpring } }
        }

        FocusRing { target: control; targetRadius: 6 }
    }

    contentItem: Label {
        leftPadding: control.indicator.width + control.spacing
        text: control.text
    }
}
