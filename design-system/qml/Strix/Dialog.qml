// A question that must be answered first. Rare: actions that cannot be undone or that end the session.
//   Dialog { title: "Erase the stick?"; text: "..."; acceptText: "Erase"; danger: true; onAccepted: ... }
import QtQuick
import QtQuick.Templates as T

T.Dialog {
    id: control

    property string text
    property string acceptText: "OK"
    property string rejectText: "Cancel"
    /// The accept button destroys data: it is drawn as a danger button.
    property bool danger: false

    anchors.centerIn: T.Overlay.overlay
    width: 340
    modal: true
    focus: true
    padding: Theme.space5
    topPadding: Theme.space4
    bottomPadding: Theme.space4

    enter: Transition {
        ParallelAnimation {
            NumberAnimation { property: "opacity"; from: 0; to: 1; duration: Theme.durBase; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeOut }
            NumberAnimation { property: "scale"; from: 0.98; to: 1; duration: Theme.durBase; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeOut }
        }
    }
    exit: Transition { NumberAnimation { property: "opacity"; to: 0; duration: Theme.durFast; easing.type: Easing.BezierSpline; easing.bezierCurve: Theme.easeIn } }

    T.Overlay.modal: Rectangle {
        color: Theme.scrim
        Behavior on opacity { NumberAnimation { duration: Theme.durBase } }
    }

    background: Surface { elevation: "panel" }

    contentItem: Column {
        spacing: Theme.space1
        Label { width: parent.width; text: control.title; textStyle: "title"; wrapMode: Text.WordWrap }
        Label { width: parent.width; text: control.text; color: Theme.textMuted; wrapMode: Text.WordWrap; lineHeightMode: Text.ProportionalHeight; lineHeight: 1.5; bottomPadding: Theme.space4 }
        Row {
            anchors.right: parent.right
            spacing: Theme.space2
            Button { text: control.rejectText; variant: "quiet"; onClicked: control.reject() }
            Button { text: control.acceptText; variant: control.danger ? "danger" : "primary"; onClicked: control.accept() }
        }
    }
}
