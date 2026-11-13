# strix-design

The Strix design system for Rust back ends: the services behind the Quickshell front ends. No dependencies. Generated with the rest of `design-system/`: `tokens.rs`, `themes.rs` and `hotkeys.rs` come from `tokens.json`; `color.rs` and `cycle.rs` from `src/rust/` in the repository.

```toml
[dependencies]
strix-design = { git = "https://github.com/liviosysctl/strixui" }
```

```rust
use std::time::Duration;
use strix_design::{Cycle, THEMES, theme, tokens};

let janus = theme("janus").unwrap();
println!("{} on {}", janus.colors.accent, janus.colors.background);   // #688f7f on #070c09
let wait = tokens::DUR_BASE;                                            // 220 ms

// the desktop theme cycle: every 10 minutes another god, unless kept
let mut cycle = Cycle::new(0, THEMES.len());
cycle.set_kept(true);                                                   // the count goes on
if let Some(next) = cycle.tick(Duration::from_secs(60), &mut |n| fastrand::usize(..n)) {  // any random source
    println!("now {}", THEMES[next].name);
}
```

| Module | What |
|---|---|
| `tokens` | Spacing, radius, line, size (`Px`), durations (`Duration`), curves (`CubicBezier`), opacity, shadows, families and text styles |
| `themes` | `THEMES` (the default first), `theme(id)`, `default_theme()`; every colour token in `Colors`, the terminal in `Terminal`, name lookup with `get("text-muted")` |
| `color` | `Color` with `parse`, `hex`, `contrast` (WCAG 2.x) and `to_tuple` |
| `cycle` | `Cycle` (10 minutes, Keep, a theme chosen by hand starts a new period) and `LockRotation` (never the same god twice in a row). The caller passes the time that went by and a random number function |
| `hotkeys` | `HOTKEYS`, the defaults of the cheat sheet and Settings › Hotkeys |

```sh
cargo test        # the contrast rules for every theme, the cycle, no two hotkeys on the same keys
```
