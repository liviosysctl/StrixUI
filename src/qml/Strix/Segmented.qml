// Two to four short options, one always chosen. The labels never move; the accent thumb glides.
// model: ["Dark", "Light"] or [{ text: "Light", enabled: false, icon: "sun" }]
import QtQuick
import QtQuick.Templates as T

Rectangle {
    id: root

    property var model: []
    property int currentIndex: 0
    signal activated(int index)

    /// The thumb stands one step inside the track
    readonly property int inset: Theme.space1

    function entry(i) { const m = model[i]; return typeof m === "string" ? { text: m } : m }

    implicitWidth: row.implicitWidth + 2 * inset
    implicitHeight: Theme.control
    radius: Theme.radiusMd
    color: Theme.surfaceSunken
    border.width: Theme.lineHair
    border.color: Theme.borderStrong

    Rectangle {
        id: thumb
        readonly property Item at: rep.count > root.currentIndex ? rep.itemAt(root.currentIndex) : null
        x: at ? at.x + root.inset : root.inset
        y: root.inset
        width: at ? at.width : 0
        height: root.height - 2 * root.inset
        radius: Theme.radiusSm
        color: Theme.accent
        Behavior on x { NumberAnimation { duration: Theme.durBase; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeInOut } }
        Behavior on width { NumberAnimation { duration: Theme.durBase; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeInOut } }
    }

    Row {
        id: row
        x: root.inset
        y: root.inset
        Repeater {
            id: rep
            model: root.model.length
            T.AbstractButton {
                id: seg
                HoverHandler { cursorShape: Qt.PointingHandCursor }
                readonly property var e: root.entry(index)
                readonly property bool selected: index === root.currentIndex
                height: root.height - 2 * root.inset
                leftPadding: Theme.space3
                rightPadding: Theme.space3
                implicitWidth: leftPadding + rightPadding + label.implicitWidth + (e.icon ? Theme.icon + Theme.space2 : 0)
                enabled: e.enabled !== false
                opacity: enabled ? 1 : Theme.dimDisabled
                hoverEnabled: true
                focusPolicy: Qt.StrongFocus
                onClicked: { root.currentIndex = index; root.activated(index) }
                Keys.onLeftPressed: if (index > 0) { root.currentIndex = index - 1; root.activated(index - 1) }
                Keys.onRightPressed: if (index < rep.count - 1) { root.currentIndex = index + 1; root.activated(index + 1) }
                contentItem: Row {
                    spacing: Theme.space2
                    Icon { visible: !!seg.e.icon; name: seg.e.icon || ""; hovered: seg.hovered; tinted: !seg.selected; color: label.color; anchors.verticalCenter: parent.verticalCenter }
                    Label {
                        id: label
                        text: seg.e.text
                        textStyle: "caption"
                        font.weight: Font.Medium
                        color: seg.selected ? Theme.onAccent : seg.hovered ? Theme.text : Theme.textMuted
                        anchors.verticalCenter: parent.verticalCenter
                        Behavior on color { ColorAnimation { duration: Theme.durBase } }
                    }
                }
                background: Item { FocusRing { target: seg; targetRadius: Theme.radiusSm } }
            }
        }
    }
}
