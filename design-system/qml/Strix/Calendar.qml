// One month, Monday first, today marked in the accent. Lives in the Today panel.
import QtQuick

Column {
    id: root

    /// Any day of the month shown.
    property date month: new Date()
    property date today: new Date()
    signal picked(date day)

    readonly property var names: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    readonly property var days: {
        const y = month.getFullYear(), m = month.getMonth()
        const first = new Date(y, m, 1)
        const lead = (first.getDay() + 6) % 7
        const out = []
        for (let i = 0; i < 42; i++) out.push(new Date(y, m, 1 - lead + i))
        return out
    }

    width: 196

    Item {
        width: parent.width
        height: 24
        Label { text: root.names[root.month.getMonth()] + " " + root.month.getFullYear(); textStyle: "aside"; anchors.verticalCenter: parent.verticalCenter }
        Row {
            anchors.right: parent.right
            anchors.verticalCenter: parent.verticalCenter
            IconButton { small: true; iconName: "chevron-left"; onClicked: root.month = new Date(root.month.getFullYear(), root.month.getMonth() - 1, 1) }
            IconButton { small: true; iconName: "chevron-right"; onClicked: root.month = new Date(root.month.getFullYear(), root.month.getMonth() + 1, 1) }
        }
    }

    Grid {
        columns: 7
        Repeater {
            model: ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
            Label { width: 28; height: 20; text: modelData; textStyle: "caption"; font.weight: Font.Medium; color: Theme.textFaint; horizontalAlignment: Text.AlignHCenter }
        }
        Repeater {
            model: root.days
            Rectangle {
                id: cell
                readonly property bool out: modelData.getMonth() !== root.month.getMonth()
                readonly property bool isToday: modelData.toDateString() === root.today.toDateString()
                width: 28
                height: 22
                radius: Theme.radiusXs
                color: isToday ? Theme.accent : tap.hovered ? Theme.surfaceRaised : "transparent"
                opacity: out ? 0.6 : 1
                HoverHandler { id: tap }
                TapHandler { onTapped: root.picked(modelData) }
                Label {
                    anchors.centerIn: parent
                    text: modelData.getDate()
                    textStyle: "caption"
                    font.weight: cell.isToday ? Font.DemiBold : Font.Normal
                    color: cell.isToday ? Theme.onAccent : cell.out ? Theme.textFaint : tap.hovered ? Theme.text : Theme.textMuted
                }
            }
        }
    }
}
