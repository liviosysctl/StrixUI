//! Colours as the design system writes them: `#rrggbb` or `#rrggbbaa`.

use std::fmt;

/// An sRGB colour with alpha, 8 bits per channel.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash)]
pub struct Color {
    pub r: u8,
    pub g: u8,
    pub b: u8,
    pub a: u8,
}

impl Color {
    pub const fn rgb(r: u8, g: u8, b: u8) -> Self {
        Self { r, g, b, a: 255 }
    }

    pub const fn rgba(r: u8, g: u8, b: u8, a: u8) -> Self {
        Self { r, g, b, a }
    }

    /// Reads `#rrggbb` or `#rrggbbaa`. Short forms and names are refused, as in the theme engine.
    pub fn parse(text: &str) -> Option<Self> {
        let hex = text.strip_prefix('#')?;
        if !(hex.len() == 6 || hex.len() == 8) || !hex.bytes().all(|b| b.is_ascii_hexdigit()) {
            return None;
        }
        let channel = |i: usize| u8::from_str_radix(&hex[i..i + 2], 16).ok();
        let a = if hex.len() == 8 { channel(6)? } else { 255 };
        Some(Self::rgba(channel(0)?, channel(2)?, channel(4)?, a))
    }

    /// `#rrggbb` when opaque, `#rrggbbaa` otherwise.
    pub fn hex(self) -> String {
        if self.a == 255 {
            format!("#{:02x}{:02x}{:02x}", self.r, self.g, self.b)
        } else {
            format!("#{:02x}{:02x}{:02x}{:02x}", self.r, self.g, self.b, self.a)
        }
    }

    /// The four channels, for APIs that take a tuple, such as a window's background colour.
    pub const fn to_tuple(self) -> (u8, u8, u8, u8) {
        (self.r, self.g, self.b, self.a)
    }

    /// Relative luminance after WCAG 2.x. Alpha is ignored.
    pub fn luminance(self) -> f64 {
        fn linear(c: u8) -> f64 {
            let c = f64::from(c) / 255.0;
            if c <= 0.039_28 { c / 12.92 } else { ((c + 0.055) / 1.055).powf(2.4) }
        }
        0.2126 * linear(self.r) + 0.7152 * linear(self.g) + 0.0722 * linear(self.b)
    }

    /// Contrast ratio after WCAG 2.x, from 1 to 21.
    pub fn contrast(self, other: Self) -> f64 {
        let (a, b) = (self.luminance(), other.luminance());
        (a.max(b) + 0.05) / (a.min(b) + 0.05)
    }
}

impl fmt::Display for Color {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_str(&self.hex())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parses_and_writes_both_forms() {
        assert_eq!(Color::parse("#c8102e"), Some(Color::rgb(0xc8, 0x10, 0x2e)));
        assert_eq!(Color::parse("#000000b8").map(Color::hex).as_deref(), Some("#000000b8"));
        assert_eq!(Color::rgb(1, 2, 3).hex(), "#010203");
    }

    #[test]
    fn refuses_what_the_engine_refuses() {
        for bad in ["#fff", "c8102e", "#c8102", "#c8102g", "red", "#c8102e0"] {
            assert_eq!(Color::parse(bad), None, "{bad}");
        }
    }

    #[test]
    fn contrast_matches_wcag() {
        let black = Color::rgb(0, 0, 0);
        let white = Color::rgb(255, 255, 255);
        assert!((black.contrast(white) - 21.0).abs() < 1e-9);
        assert!((white.contrast(white) - 1.0).abs() < 1e-9);
    }
}
