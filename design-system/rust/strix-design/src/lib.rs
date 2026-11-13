//! The Strix design system for Rust: every token, the eight god themes, the theme cycle and the
//! default hotkeys.
//!
//! The same values as `tokens.json`, the QML module and the web bundle, generated from one source.
//! It has no dependencies, so every back end can take it.
//!
//! ```
//! let theme = strix_design::default_theme();
//! assert_eq!(theme.id, "saturnus");
//! assert_eq!(theme.colors.accent.hex(), "#c8102e");
//! assert!(theme.colors.text.contrast(theme.colors.background) >= 4.5);
//! ```

pub mod color;
pub mod cycle;
pub mod hotkeys;
pub mod themes;
pub mod tokens;

pub use color::Color;
pub use cycle::{Cycle, LockRotation};
pub use hotkeys::{HOTKEYS, Hotkey};
pub use themes::{Appearance, Colors, DEFAULT, THEMES, Terminal, Theme, default_theme, theme};

/// Version of `tokens.json` this crate was generated from.
pub const TOKENS_VERSION: u32 = tokens::VERSION;
