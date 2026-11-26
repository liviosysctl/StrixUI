// Chips that belong together on one plate of smoked glass, parted by hair lines: the top bar holds
// a few of these instead of a plate for every chip. The chips inside take `plate: false`; a chip
// that is hidden takes its line with it, and a group with nothing shown draws no plate.
//   ChipGroup {
//       Chip { plate: false; iconName: "wifi"; text: "eduroam" }
//       Chip { plate: false; iconName: "volume-2"; text: "40%" }
//   }
import QtQuick

Item {
    id: root

    default property alias chips: row.data
    /// Where the hair lines stand: the left edge of every shown chip but the first
    property var cuts: []

    implicitWidth: row.implicitWidth
    implicitHeight: Theme.control

    // Hidden by the plate, not by the group: an invisible group would hide its chips as well and
    // never learn that one of them came back
    Surface {
        anchors.fill: parent
        visible: row.implicitWidth > 0
        elevation: "pop"
    }

    Row {
        id: row
        height: parent.height
        onPositioningComplete: root.cuts = row.children.filter(c => c.visible && c.width > 0).slice(1).map(c => c.x)
    }

    Repeater {
        model: root.cuts
        Rectangle {
            required property real modelData
            x: modelData
            anchors.verticalCenter: parent.verticalCenter
            width: Theme.lineHair
            height: Theme.icon
            color: Theme.glassEdge
        }
    }
}
