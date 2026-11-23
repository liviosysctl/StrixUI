// The one way to trigger an action. variant: "primary" at most once per view, "default" for the
// secondary action, "quiet" for cancel and dismiss, "danger" for actions that destroy data.
import QtQuick
import QtQuick.Templates as T

T.Button {
    id: control

    // The hand over what can be pressed, as on every clickable part of the shell
    HoverHandler { cursorShape: Qt.PointingHandCursor }

    property string variant: "default"
    /// A short piece runs along the bottom edge. Keep the label, change its wording ("Checking").
    property bool loading: false
    property string iconName: ""

    readonly property bool primary: variant === "primary"
    readonly property bool quiet: variant === "quiet"
    readonly property bool danger: variant === "danger"
    readonly property color ink: primary ? Theme.onAccent : danger ? Theme.error : quiet && !hovered ? Theme.textMuted : Theme.text

    implicitHeight: Theme.control
    implicitWidth: Math.max(implicitHeight, implicitContentWidth + leftPadding + rightPadding)
    leftPadding: Theme.space3
    rightPadding: leftPadding
    hoverEnabled: true
    focusPolicy: Qt.StrongFocus
    opacity: enabled ? 1 : Theme.dimDisabled
    transform: Translate { y: control.down ? 1 : 0 }

    contentItem: Row {
        spacing: Theme.space2
        Icon {
            visible: control.iconName !== ""
            name: control.iconName
            color: control.ink
            hovered: control.hovered
            tinted: !control.primary
            anchors.verticalCenter: parent.verticalCenter
        }
        Label {
            text: control.text
            color: control.ink
            textStyle: "label"
            elide: Text.ElideRight
            anchors.verticalCenter: parent.verticalCenter
            Behavior on color { ColorAnimation { duration: Theme.durFast; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeOut } }
        }
    }

    background: Rectangle {
        radius: Theme.radiusMd
        clip: true
        color: control.primary ? (control.down ? Theme.accentPressed : control.hovered ? Theme.accentHover : Theme.accent)
             : control.danger ? (control.hovered ? Theme.accentSoft : "transparent")
             : control.quiet ? "transparent"
             : control.hovered ? Theme.surfaceRaised : "transparent"
        border.width: Theme.lineHair
        border.color: control.primary ? color
                    : control.quiet ? "transparent"
                    : control.danger ? Theme.error
                    : control.hovered ? Theme.textMuted : Theme.borderStrong
        Behavior on color { ColorAnimation { duration: Theme.durFast; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeOut } }
        Behavior on border.color { ColorAnimation { duration: Theme.durFast } }

        Rectangle {
            id: run
            visible: control.loading
            y: parent.height - 1
            width: parent.width * 0.28
            height: 1
            color: control.ink
            NumberAnimation on x {
                running: control.loading
                loops: Animation.Infinite
                from: -run.width * 1.1
                to: run.width * 4.6
                duration: Theme.durLoop
                easing.type: Easing.BezierSpline
                easing.bezierCurve: Theme.easeInOut
            }
        }

        FocusRing { target: control }
    }
}
