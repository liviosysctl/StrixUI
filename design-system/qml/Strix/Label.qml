// Text in one of the styles of the brand book: Label { textStyle: "caption"; text: "8%" }
import QtQuick

Text {
    /// body, label, value, heading, caption, micro, clock (mono); title-lg, title, subtitle, aside, motto (serif); display, emblem (blackletter)
    property string textStyle: "body"
    readonly property var s: Theme.styles[textStyle] || Theme.styles.body

    color: Theme.text
    font.family: s.family
    font.pixelSize: s.pixelSize
    font.weight: s.weight
    font.italic: s.italic
    font.letterSpacing: s.letterSpacing * s.pixelSize
    font.features: ({ "liga": 0, "calt": 0 })
    lineHeightMode: Text.FixedHeight
    lineHeight: s.lineHeight
    verticalAlignment: Text.AlignVCenter
    textFormat: Text.PlainText
}
