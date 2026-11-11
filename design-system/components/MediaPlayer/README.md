# MediaPlayer

What is playing, with the three transport buttons. Opens from the music symbol in the dock or from the track in the top bar.

- Parts: cover (a disc symbol when there is none), serif title, muted artist, elapsed and total time around a Progress line, previous, play or pause, next.
- Title and artist truncate; they never wrap.
- Nothing playing: the pill hides its music symbol and the top bar shows no track.

## In Quickshell (Linux shell and apps)

`import Strix`, then `MediaPlayer`.

```qml
MediaPlayer { property var p: Mpris.players.values[0]; title: p.trackTitle; artist: p.trackArtist; cover: p.trackArtUrl; playing: p.isPlaying; position: p.position; length: p.length; onToggle: p.togglePlaying() }
```

## In Tauri (Windows app)

The markup above with `tokens.css`, `components/bundle.css` and `components/bundle.js`; call `Kit.hydrate(root)` after adding it.
