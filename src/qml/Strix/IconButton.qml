// A control that shows only a symbol. Give it a ToolTip with its name.
// checkable + checked shows the pressed state in accent-text, and the cup ("coffee") steams; danger for the power symbol.
import QtQuick
import QtQuick.Templates as T

T.Button {
    id: control

    // The hand over what can be pressed, as on every clickable part of the shell
    HoverHandler { cursorShape: Qt.PointingHandCursor }

    property string iconName
    property bool danger: false

    implicitWidth: Theme.control
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
            active: control.checked
            hovered: control.hovered || control.visualFocus
            color: control.danger || control.checked ? Theme.accentText : control.hovered ? Theme.text : Theme.textMuted
        }
    }

    background: Rectangle {
        radius: Theme.radiusMd
        color: control.hovered ? Theme.surfaceRaised : "transparent"
        Behavior on color { ColorAnimation { duration: Theme.durFast } }
        FocusRing { target: control }
    }
}
