#[cfg(test)]
mod tests {
    use super::*;

    /// The rules of the theme engine (format 1) and of the design system, for every theme.
    #[test]
    fn every_theme_passes_the_contrast_rules() {
        let mut fails = Vec::new();
        for t in &THEMES {
            let c = &t.colors;
            let mut need = |what: &str, a: Color, b: Color, min: f64| {
                let r = a.contrast(b);
                if r < min {
                    fails.push(format!("{}: {what} {r:.2} < {min}", t.id));
                }
            };
            for (name, ground) in [("background", c.background), ("surface", c.surface), ("surface-raised", c.surface_raised)] {
                need(&format!("text on {name}"), c.text, ground, 4.5);
                need(&format!("text-muted on {name}"), c.text_muted, ground, 4.5);
                need(&format!("accent-text on {name}"), c.accent_text, ground, 4.5);
                need(&format!("error on {name}"), c.error, ground, 4.5);
                need(&format!("focus on {name}"), c.focus, ground, 3.0);
            }
            need("on-accent on accent", c.on_accent, c.accent, 4.5);
            need("on-accent on accent-hover", c.on_accent, c.accent_hover, 4.5);
            need("on-accent on accent-pressed", c.on_accent, c.accent_pressed, 4.5);
            need("border-strong on surface", c.border_strong, c.surface, 3.0);
            need("terminal foreground", t.terminal.foreground, t.terminal.background, 4.5);
            assert!(c.text.luminance() > c.background.luminance(), "{} is dark", t.id);
        }
        assert!(fails.is_empty(), "{}", fails.join("\n"));
    }

    #[test]
    fn ids_are_unique_and_the_default_comes_first() {
        assert_eq!(THEMES[0].id, DEFAULT);
        for (i, a) in THEMES.iter().enumerate() {
            assert!(THEMES[i + 1..].iter().all(|b| b.id != a.id), "{} twice", a.id);
            assert_eq!(theme(a.id), Some(a));
        }
        assert_eq!(theme("chamber"), None);
    }

    #[test]
    fn names_reach_every_field() {
        let c = &THEMES[1].colors;
        assert_eq!(c.iter().count(), Colors::NAMES.len());
        assert_eq!(c.get("accent"), Some(c.accent));
        assert_eq!(c.get("nothing"), None);
        assert!(Terminal::NAMES.iter().all(|n| THEMES[1].terminal.get(n).is_some()));
    }
}
