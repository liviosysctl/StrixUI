// A button that holds a symbol, a word or a figure, or all of them. On the picture it stands on a
// plate of smoked glass of its own (the top bar); on a plate that is already there it is plain
// (the dock).
//   Chip { iconName: "wifi"; text: "eduroam"; open: panel.visible; onClicked: panel.toggle() }
//   Chip { plate: false; onClicked: monitor(); Icon { name: "cpu" } Label { text: "8%" } }
import QtQuick
import QtQuick.Templates as T

T.AbstractButton {
    id: control

    // The hand over what can be pressed, as on every clickable part of the shell
    HoverHandler { cursorShape: Qt.PointingHandCursor }

    property string iconName
    /// What it switches is on: the symbol and the word take the accent
    property bool on: false
    /// What it opened is open: it stays lit
    property bool open: false
    /// Nothing to report (offline, switched off): the symbol and the word step back
    property bool faint: false
    /// Smoked glass of its own. Off for a chip that stands on a plate
    property bool plate: true
    /// More than a symbol and a word: what is put inside follows them in the row
    default property alias extra: row.data

    readonly property bool lit: hovered || visualFocus || open
    readonly property color ink: on ? Theme.accentText : faint && !lit ? Theme.textFaint : Theme.text
    readonly property color symbolInk: on ? Theme.accentText : faint && !lit ? Theme.textFaint : lit ? Theme.text : Theme.textMuted

    implicitHeight: Theme.control
    implicitWidth: Math.max(Theme.control, row.implicitWidth + 2 * Theme.space2)
    padding: 0
    hoverEnabled: true
    focusPolicy: Qt.StrongFocus
    opacity: enabled ? 1 : Theme.dimDisabled

    // Pressing is quick, letting go a little slower
    scale: down ? 0.97 : 1
    Behavior on scale { NumberAnimation { duration: control.down ? Theme.durInstant : Theme.durFast; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeOut } }

    contentItem: Item {
        Row {
            id: row
            anchors.centerIn: parent
            spacing: Theme.space2
            Icon {
                visible: control.iconName !== ""
                name: control.iconName
                color: control.symbolInk
                hovered: control.hovered || control.visualFocus
                active: control.on
                anchors.verticalCenter: parent.verticalCenter
            }
            Label {
                visible: control.text !== ""
                text: control.text
                textStyle: "value"
                color: control.ink
                anchors.verticalCenter: parent.verticalCenter
                Behavior on color { ColorAnimation { duration: Theme.durFast } }
            }
        }
    }

    background: Item {
        Surface {
            visible: control.plate
            anchors.fill: parent
            elevation: "pop"
            tint: control.down ? Theme.surfaceSunken : control.lit ? Theme.surfaceRaised : Theme.surface
            Behavior on tint { ColorAnimation { duration: Theme.durFast } }
        }
        Rectangle {
            visible: !control.plate
            anchors.fill: parent
            radius: Theme.radiusMd
            color: control.lit ? Theme.surfaceRaised : "transparent"
            Behavior on color { ColorAnimation { duration: Theme.durFast } }
        }
        FocusRing { target: control }
    }
}
