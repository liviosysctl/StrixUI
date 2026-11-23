// A field with its label above and one line of help or error below.
// shape: "box" (default) or "line" (lock screen password). While it is typed into, its line takes
// the focus colour: a field needs no ring around it.
import QtQuick
import QtQuick.Templates as T

Column {
    id: root

    property string label
    property string help
    /// Set to show the field in error; the text replaces the help line.
    property string error
    property string shape: "box"
    property string iconName
    property alias text: field.text
    property alias placeholderText: field.placeholderText
    property alias echoMode: field.echoMode
    property alias field: field
    /// Extra items at the right inside the field, such as KeyCaps or an IconButton.
    default property alias trailing: tail.data

    signal accepted()

    /// Shake once, after a wrong password.
    function shake() { shakeAnim.restart() }

    width: 240
    spacing: Theme.space1
    opacity: enabled ? 1 : Theme.dimDisabled

    Label {
        visible: root.label !== ""
        text: root.label
        textStyle: "label"
    }

    Rectangle {
        id: box
        width: parent.width
        height: Theme.control
        radius: root.shape === "line" ? 0 : Theme.radiusMd
        color: root.shape === "line" ? "transparent" : Theme.surfaceSunken
        border.width: root.shape === "line" ? 0 : Theme.lineHair
        border.color: root.error !== "" ? Theme.error : field.activeFocus ? Theme.focus : hover.hovered ? Theme.textMuted : Theme.borderStrong
        Behavior on border.color { ColorAnimation { duration: Theme.durFast } }

        HoverHandler { id: hover }

        // the line style: only the bottom edge; focus draws a second line out from the middle
        Rectangle {
            visible: root.shape === "line"
            anchors { left: parent.left; right: parent.right; bottom: parent.bottom }
            height: Theme.lineHair
            color: hover.hovered ? Theme.textMuted : Theme.borderStrong
            Behavior on color { ColorAnimation { duration: Theme.durFast } }
            Rectangle {
                readonly property bool lit: field.activeFocus || root.error !== ""
                anchors.horizontalCenter: parent.horizontalCenter
                width: lit ? parent.width : 0
                height: lit ? Theme.lineBold : Theme.lineHair
                anchors.bottom: parent.bottom
                color: root.error !== "" ? Theme.error : Theme.focus
                Behavior on width { NumberAnimation { duration: Theme.durBase; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeOut } }
                Behavior on color { ColorAnimation { duration: Theme.durFast } }
            }
        }

        Row {
            id: inside
            anchors.fill: parent
            anchors.leftMargin: root.shape === "line" ? 0 : Theme.space2
            anchors.rightMargin: anchors.leftMargin
            spacing: Theme.space2

            Icon {
                visible: root.iconName !== ""
                name: root.iconName
                anchors.verticalCenter: parent.verticalCenter
            }

            T.TextField {
                id: field
                width: inside.width - (root.iconName !== "" ? Theme.icon + inside.spacing : 0) - (tail.width > 0 ? tail.width + inside.spacing : 0)
                height: parent.height
                verticalAlignment: TextInput.AlignVCenter
                color: Theme.text
                placeholderTextColor: Theme.textFaint
                selectionColor: Theme.accentSoft
                selectedTextColor: Theme.text
                font.family: Theme.sans
                font.pixelSize: Theme.styles.body.pixelSize
                font.letterSpacing: echoMode === TextInput.Password && length > 0 ? 3.6 : 0
                passwordCharacter: "•"
                padding: 0
                cursorDelegate: Rectangle { width: 1; color: Theme.accent; visible: field.cursorVisible }
                onAccepted: root.accepted()
                background: Label {
                    visible: !field.length && !field.preeditText
                    height: field.height
                    text: field.placeholderText
                    color: Theme.textFaint
                    elide: Text.ElideRight
                }
            }

            Row {
                id: tail
                spacing: Theme.space1
                anchors.verticalCenter: parent.verticalCenter
            }
        }

        transform: Translate { id: shift }
        SequentialAnimation {
            id: shakeAnim
            NumberAnimation { target: shift; property: "x"; to: -6; duration: Theme.durSlow * 0.2 }
            NumberAnimation { target: shift; property: "x"; to: 5; duration: Theme.durSlow * 0.2 }
            NumberAnimation { target: shift; property: "x"; to: -3; duration: Theme.durSlow * 0.2 }
            NumberAnimation { target: shift; property: "x"; to: 2; duration: Theme.durSlow * 0.2 }
            NumberAnimation { target: shift; property: "x"; to: 0; duration: Theme.durSlow * 0.2 }
        }
    }

    Label {
        visible: root.help !== "" || root.error !== ""
        width: parent.width
        text: root.error !== "" ? root.error : root.help
        textStyle: "caption"
        color: root.error !== "" ? Theme.error : Theme.textMuted
        wrapMode: Text.WordWrap
    }
}
