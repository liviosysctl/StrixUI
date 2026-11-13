# List

Rows to pick from: app finder results, clipboard history, networks, devices.

- A row: symbol, name (`k-grow`, truncates), a faint note at the end.
- The chosen row gets a raised ground and a `>` in `accent-text` in front, like a cursor in a terminal. No coloured stripe.
- Rows enter one after another: class `k-enter` with `--i` as the position (`stagger` apart).
- Up and down move the choice, Enter takes it. Matching letters of a search are bold.
- Empty: one calm sentence in `k-empty`.

## In Quickshell (Linux shell and apps)

`import Strix`, then `ListRow`.

```qml
ListView {
    model: apps
    delegate: ListRow { width: ListView.view.width; text: name; iconName: icon; detail: keys; selected: ListView.isCurrentItem }
}
```

## In HTML (the previews)

The markup of the preview with `tokens.css`, `components/bundle.css` and `components/bundle.js`; call `Kit.hydrate(root)` after adding it.
