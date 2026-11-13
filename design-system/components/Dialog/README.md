# Dialog

A question that must be answered before anything else. Rare: only for actions that cannot be undone, or that end the session.

- Parts: a serif title that is the question, one or two sentences that name the consequence, actions bottom right with the safe one first.
- The button repeats the verb of the title ("Erase disk"), never "OK" or "Yes".
- Opens with a fade of the `scrim` and a small rise; Escape and the quiet button close it. Focus starts on the safe action.

## In Quickshell (Linux shell and apps)

`import Strix`, then `Dialog`.

```qml
Dialog { id: ask; title: "Erase the stick?"; text: "Everything on it is lost."; acceptText: "Erase"; danger: true; onAccepted: backend.call("erase") }
// ask.open()
```

## In HTML (the previews)

The markup of the preview with `tokens.css`, `components/bundle.css` and `components/bundle.js`; call `Kit.hydrate(root)` after adding it.
