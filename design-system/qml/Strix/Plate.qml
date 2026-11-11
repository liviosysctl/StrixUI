// The caption of an engraving: what it shows and who made it, in small serif italic.
import QtQuick

Label {
    font.family: Theme.serif
    font.italic: true
    font.pixelSize: 12
    font.weight: Font.Normal
    font.letterSpacing: 0.24
    lineHeight: 16
    color: Theme.textMuted
}
