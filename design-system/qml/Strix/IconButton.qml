// A control that shows only a symbol. Give it a ToolTip with its name.
// checkable + checked shows the pressed state in accent-text; danger for the power symbol.
import QtQuick
import QtQuick.Templates as T

T.Button {
    id: control

    property string iconName
    property bool small: false
    property bool danger: false

    implicitWidth: small ? Theme.controlSm : Theme.controlMd
    implicitHeight: implicitWidth
    padding: 0
    hoverEnabled: true
    focusPolicy: Qt.StrongFocus
    opacity: enabled ? 1 : Theme.dimDisabled
    scale: down ? 0.92 : 1
    Behavior on scale { NumberAnimation { duration: Theme.durInstant; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeOut } }

    contentItem: Item {
        Icon {
            anchors.centerIn: parent
            name: control.iconName
            hovered: control.hovered || control.visualFocus
            size: control.small ? 12 : 14
            color: control.danger || control.checked ? Theme.accentText : control.hovered ? Theme.text : Theme.textMuted
        }
    }

    background: Rectangle {
        radius: Theme.radiusSm
        color: control.hovered ? Theme.surfaceRaised : "transparent"
        Behavior on color { ColorAnimation { duration: Theme.durFast } }
        FocusRing { target: control }
    }
}
