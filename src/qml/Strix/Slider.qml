// A value on a range: a hair track, the filled part in accent-text, a thin upright thumb.
// valueText shows the value at the right ("62"); leave it empty for none.
import QtQuick
import QtQuick.Templates as T

T.Slider {
    id: control

    property string iconName
    property string valueText: Math.round(value * (to > 1 ? 1 : 100)).toString()

    implicitWidth: 240
    implicitHeight: 16
    leftPadding: iconName !== "" ? 14 + Theme.space2 : 0
    rightPadding: valueText !== "" ? 4 * 7 + Theme.space2 : 0
    hoverEnabled: true
    opacity: enabled ? 1 : Theme.dimDisabled

    background: Item {
        Icon {
            visible: control.iconName !== ""
            name: control.iconName
            anchors.verticalCenter: parent.verticalCenter
        }
        Rectangle {
            x: control.leftPadding
            y: control.height / 2
            width: control.availableWidth
            height: Theme.lineHair
            color: Theme.borderStrong
            Rectangle { width: control.visualPosition * parent.width; height: parent.height; color: Theme.accentText }
        }
        Label {
            visible: control.valueText !== ""
            anchors.right: parent.right
            anchors.verticalCenter: parent.verticalCenter
            textStyle: "caption"
            text: control.valueText
            horizontalAlignment: Text.AlignRight
        }
        FocusRing { target: control; targetRadius: Theme.radiusXs }
    }

    handle: Rectangle {
        x: control.leftPadding + control.visualPosition * (control.availableWidth - width)
        y: (control.height - height) / 2
        width: 3
        height: 11
        color: Theme.text
        scale: control.pressed ? 1.3 : 1
        Behavior on scale { NumberAnimation { duration: Theme.durFast; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeSpring } }
    }
}
