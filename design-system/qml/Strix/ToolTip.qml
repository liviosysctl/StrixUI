// The name of a control that shows only a symbol. Appears after dur-slow above the control.
//   IconButton { id: off; iconName: "power"; ToolTip { text: "Shut down"; visible: off.hovered } }
import QtQuick
import QtQuick.Templates as T

T.ToolTip {
    id: control

    x: parent ? (parent.width - implicitWidth) / 2 : 0
    y: -implicitHeight - 6
    delay: Theme.durSlow
    margins: Theme.space1
    padding: 0
    leftPadding: 6
    rightPadding: 6
    closePolicy: T.Popup.CloseOnEscape | T.Popup.CloseOnPressOutsideParent | T.Popup.CloseOnReleaseOutsideParent

    enter: Transition {
        ParallelAnimation {
            NumberAnimation { property: "opacity"; from: 0; to: 1; duration: Theme.durFast; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeOut }
            NumberAnimation { property: "y"; from: -control.implicitHeight - 3; to: -control.implicitHeight - 6; duration: Theme.durFast }
        }
    }
    exit: Transition { NumberAnimation { property: "opacity"; to: 0; duration: Theme.durFast } }

    contentItem: Label {
        text: control.text
        textStyle: "caption"
        color: Theme.text
    }

    background: Rectangle {
        radius: Theme.radiusXs
        color: Theme.surfaceRaised
        border.width: Theme.lineHair
        border.color: Theme.borderStrong
    }
}
