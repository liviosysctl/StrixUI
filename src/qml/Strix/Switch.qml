// On or off, effective at once. The text says what is on.
import QtQuick
import QtQuick.Templates as T

T.Switch {
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
        implicitWidth: 2 * Theme.icon
        implicitHeight: Theme.mark
        y: (control.height - height) / 2
        radius: height / 2
        color: control.checked ? Theme.accent : Theme.surfaceSunken
        border.width: Theme.lineHair
        border.color: control.checked ? Theme.accent : Theme.borderStrong
        Behavior on color { ColorAnimation { duration: Theme.durBase } }

        Rectangle {
            readonly property int knob: Theme.mark - 2 * Theme.space1
            y: Theme.space1
            x: control.checked ? parent.width - width - Theme.space1 : Theme.space1
            width: control.down ? knob + Theme.space1 : knob
            height: knob
            radius: knob / 2
            color: control.checked ? Theme.onAccent : Theme.textMuted
            Behavior on x { NumberAnimation { duration: Theme.durBase; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeSpring } }
            Behavior on width { NumberAnimation { duration: Theme.durFast } }
        }

        FocusRing { target: control; targetRadius: Theme.mark / 2 }
    }

    contentItem: Label {
        leftPadding: control.indicator.width + control.spacing
        text: control.text
    }
}
