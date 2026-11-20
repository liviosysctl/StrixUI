// Load figures that act as one button: the CPU and memory of the top bar open the system
// monitor. One hover, one press and one focus ring for all of them; under the pointer the bars
// fill again from empty and take the accent.
//   MeterGroup { onClicked: monitor(); Meter { label: "CPU"; value: cpu } Meter { label: "MEM"; value: mem } }
import QtQuick
import QtQuick.Templates as T

T.AbstractButton {
    id: control

    default property alias meters: row.data

    implicitWidth: row.implicitWidth + leftPadding + rightPadding
    implicitHeight: Theme.controlSm
    padding: 0
    leftPadding: Theme.space2
    rightPadding: Theme.space2
    hoverEnabled: true
    focusPolicy: Qt.StrongFocus
    opacity: enabled ? 1 : Theme.dimDisabled

    // Pressing is quick, letting go a little slower
    scale: down ? 0.97 : 1
    Behavior on scale { NumberAnimation { duration: control.down ? Theme.durInstant : Theme.durFast; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeOut } }

    readonly property bool hot: hovered || visualFocus
    onHotChanged: {
        for (let i = 0; i < row.children.length; i++) {
            const meter = row.children[i]
            if (meter.hot === undefined) continue
            meter.hot = control.hot
            if (control.hot) meter.sweep(i * Theme.stagger)
        }
    }

    /// The gap between the parts: wide between meters, narrower between a symbol and its word
    property alias gap: row.spacing

    // The template already keeps the padding around this item: the row starts at its left edge,
    // so what is in it stands in the middle of the hover
    contentItem: Item {
        Row {
            id: row
            anchors.verticalCenter: parent.verticalCenter
            spacing: Theme.space4
        }
    }

    background: Rectangle {
        radius: Theme.radiusSm
        color: control.hovered ? Theme.surfaceRaised : "transparent"
        Behavior on color { ColorAnimation { duration: Theme.durFast } }
        FocusRing { target: control }
    }
}
