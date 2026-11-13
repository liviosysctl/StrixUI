# Osd

The answer to a hardware key: volume, brightness, mute. A pill at the bottom centre, above the dock.

- Parts: symbol, line, number. It never takes focus and leaves by itself after 1.5 seconds.
- The line follows the keys with `dur-fast` so repeated presses feel direct.

## In Quickshell (Linux shell and apps)

`import Strix`, then `Osd`.

```qml
Osd { iconName: "volume-2"; value: Pipewire.defaultAudioSink.audio.volume }
```

## In HTML (the previews)

The markup of the preview with `tokens.css`, `components/bundle.css` and `components/bundle.js`; call `Kit.hydrate(root)` after adding it.
