# SlantCard

The tall slanted card of the theme picker, and the carousel that holds a row of them. The preview shows the eight god themes.

- Each card is a parallelogram that overlaps its neighbour. The chosen card in the middle is 420px wide and taller, with a cream hair edge and the theme's name in blackletter; all others are 96px wide and dimmed.
- Markup: `.k-carousel` > `.k-carousel-track` > `button.k-slant` with `.k-slant-art` (the preview), `.k-slant-edge`, `.k-slant-name`.
- Paging: left and right arrows, the wheel, or a click on a neighbour. The row glides over `dur-slow` while the old middle narrows and the new one widens.
- A click on the middle card fires `apply` with the pointer position, which is where the circular reveal starts (`Kit.reveal`).
- The art is the theme's or the god's own engraving, never a screenshot of somebody else's work.

## In Quickshell (Linux shell and apps)

`import Strix`, then `SlantCard`.

```qml
Row {
    spacing: -37
    Repeater {
        model: Theme.order
        SlantCard { source: Theme.wallpaper(modelData); name: Theme.gods[modelData].name; caption: "dark"; selected: index === picker.index }
    }
}
```

## In HTML (the previews)

The markup of the preview with `tokens.css`, `components/bundle.css` and `components/bundle.js`; call `Kit.hydrate(root)` after adding it.
