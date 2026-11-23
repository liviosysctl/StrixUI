// Facts as label and value, framed by double-line brackets with open corners.
//   InfoBlock { title: "strix"; model: [["OS", "Strix 0.1"], ["Theme", "Saturnus, dark"]] }
import QtQuick

Item {
    id: root

    property string title
    property var model: []

    implicitWidth: Math.max(grid.implicitWidth, head.implicitWidth) + 2 * Theme.space4
    implicitHeight: col.implicitHeight + 2 * Theme.space2

    // a bracket drawn as a double line: two nested open frames, 1px apart
    component Bracket: Item {
        property bool flip: false
        width: Theme.space2
        height: parent.height
        opacity: 0.5
        Repeater {
            model: 2
            Item {
                x: flip ? 0 : index * 2
                y: index * 2
                width: parent.width - index * 2
                height: parent.height - index * 4
                Rectangle { x: flip ? parent.width - 1 : 0; width: Theme.lineHair; height: parent.height; color: Theme.line }
                Rectangle { width: parent.width; height: Theme.lineHair; color: Theme.line }
                Rectangle { anchors.bottom: parent.bottom; width: parent.width; height: Theme.lineHair; color: Theme.line }
            }
        }
    }

    Bracket { anchors.left: parent.left }
    Bracket { anchors.right: parent.right; flip: true }

    Column {
        id: col
        x: Theme.space4
        y: Theme.space2
        Label { id: head; visible: root.title !== ""; text: root.title; textStyle: "subtitle"; font.italic: true; bottomPadding: 2 }
        Grid {
            id: grid
            columns: 3
            columnSpacing: Theme.space2
            Repeater {
                model: {
                    const cells = []
                    for (let i = 0; i < root.model.length; i++)
                        cells.push([root.model[i][0], "key"], ["::", "sep"], [root.model[i][1], "value"])
                    return cells
                }
                Label {
                    text: modelData[0]
                    font.weight: modelData[1] === "key" ? Font.DemiBold : Font.Normal
                    color: modelData[1] === "sep" ? Theme.textFaint : modelData[1] === "value" ? Theme.textMuted : Theme.text
                }
            }
        }
    }
}
