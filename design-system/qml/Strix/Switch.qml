// On or off, effective at once. The text says what is on.
import QtQuick
import QtQuick.Templates as T

T.Switch {
    id: control

    implicitWidth: implicitIndicatorWidth + (text !== "" ? spacing + implicitContentWidth : 0)
    implicitHeight: 18
    spacing: Theme.space2
    padding: 0
    hoverEnabled: true
    opacity: enabled ? 1 : Theme.dimDisabled

    indicator: Rectangle {
        implicitWidth: 26
        implicitHeight: 14
        y: (control.height - height) / 2
        radius: height / 2
        color: control.checked ? Theme.accent : Theme.surfaceSunken
        border.width: Theme.lineHair
        border.color: control.checked ? Theme.accent : Theme.borderStrong
        Behavior on color { ColorAnimation { duration: Theme.durBase } }

        Rectangle {
            y: 2
            x: control.checked ? (control.down ? 9 : 14) : 2
            width: control.down ? 11 : 8
            height: 8
            radius: 4
            color: control.checked ? Theme.onAccent : Theme.textMuted
            Behavior on x { NumberAnimation { duration: Theme.durBase; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeSpring } }
            Behavior on width { NumberAnimation { duration: Theme.durFast } }
        }

        FocusRing { target: control; targetRadius: 7 }
    }

    contentItem: Label {
        leftPadding: control.indicator.width + control.spacing
        text: control.text
    }
}
