//! The themes of Strix: one per Roman god, each a plate and a set of colours (src/design/gods.json).
//!
//! The colours of a theme are a small set of tokens that follow the god: a tinted background and its
//! surfaces, the accent and everything derived from it, and the terminal cursor and selection. Text,
//! line, the status colours and syntax stay as they are in every theme. The accent of each god is
//! picked by hand; the rest is derived in OKLCH so every theme has the lightness steps of Saturnus.

use crate::colour::{contrast, luminance, oklch, to_oklch};
use serde_json::{Map, Value};

/// A theme's colour tokens in the order they are derived
pub type Tokens = Vec<(String, String)>;

pub fn get<'a>(t: &'a Tokens, name: &str) -> &'a str {
    t.iter()
        .find(|(k, _)| k == name)
        .map(|(_, v)| v.as_str())
        .unwrap_or_else(|| panic!("no token {name}"))
}

pub fn set(t: &mut Tokens, name: &str, v: String) {
    match t.iter_mut().find(|(k, _)| k == name) {
        Some(slot) => slot.1 = v,
        None => t.push((name.to_string(), v)),
    }
}

pub struct God {
    pub id: String,
    pub name: String,
    pub accent: String,
    pub description: String,
}

pub struct Gods {
    pub default: String,
    pub gods: Vec<God>,
    base: Tokens,
    pub fixed: Map<String, Value>,
}

impl Gods {
    pub fn load(data: &Value) -> Gods {
        let gods = data["gods"]
            .as_array()
            .expect("gods")
            .iter()
            .map(|g| God {
                id: g["id"].as_str().expect("id").into(),
                name: g["name"].as_str().expect("name").into(),
                accent: match &g["accent"] {
                    Value::String(s) => s.clone(),
                    Value::Array(a) => {
                        let n = |i: usize| a[i].as_f64().expect("a number");
                        oklch(n(0), n(1), n(2))
                    }
                    _ => panic!("accent"),
                },
                description: g["description"].as_str().expect("description").into(),
            })
            .collect();
        let base = data["base"]
            .as_object()
            .expect("base")
            .iter()
            .map(|(k, v)| (k.clone(), v.as_str().expect("hex").to_string()))
            .collect();
        Gods {
            default: data["default"].as_str().expect("default").into(),
            gods,
            base,
            fixed: data["fixed"].as_object().expect("fixed").clone(),
        }
    }

    pub fn fixed(&self, name: &str) -> &str {
        self.fixed[name].as_str().expect("hex")
    }

    /// Every token of a god's theme, border-active included
    pub fn colours(&self, id: &str) -> Tokens {
        let mut t = if id == self.default {
            self.base.clone()
        } else {
            let god = self.gods.iter().find(|g| g.id == id).expect("a god");
            self.derive(&god.accent)
        };
        let ba = border_active(&t);
        set(&mut t, "border-active", ba);
        t
    }

    /// Every theme token for an accent that is not a god's, border-active included (pack)
    pub fn derive_all(&self, accent: &str) -> Tokens {
        let mut t = self.derive(accent);
        let ba = border_active(&t);
        set(&mut t, "border-active", ba);
        t
    }

    /// The tokens that follow an accent: grounds tinted to its hue, the accent family, focus,
    /// cursor, selection
    pub fn derive(&self, acc: &str) -> Tokens {
        let (mut la, ca, ha) = to_oklch(acc);
        let mut t = Tokens::new();
        for (k, c) in [
            ("background", 0.010),
            ("surface", 0.011),
            ("surface-raised", 0.012),
            ("surface-sunken", 0.008),
            ("border", 0.016),
        ] {
            let lb = to_oklch(get(&self.base, k)).0;
            set(&mut t, k, oklch(lb, c, ha));
        }
        let white = "#ffffff".to_string();
        let dark = get(&t, "surface-sunken").to_string();
        let fills = |l: f64| {
            [
                oklch(l, ca, ha),
                oklch(l + 0.04, ca, ha),
                oklch(l - 0.05, ca, ha),
            ]
        };
        let worst = |label: &str, l: f64| {
            fills(l)
                .iter()
                .map(|f| contrast(label, f))
                .fold(f64::INFINITY, f64::min)
        };
        let label = if worst(&white, la) >= worst(&dark, la) {
            white
        } else {
            dark
        };
        let step = if label == "#ffffff" { -0.005 } else { 0.005 };
        while worst(&label, la) < 4.5 {
            la += step;
        }
        let [a, hover, pressed] = fills(la);
        set(&mut t, "accent", a);
        set(&mut t, "accent-hover", hover);
        set(&mut t, "accent-pressed", pressed);
        set(&mut t, "on-accent", label);
        set(
            &mut t,
            "accent-soft",
            oklch(0.22, (ca * 0.35).min(0.06), ha),
        );
        set(&mut t, "selection", oklch(0.27, (ca * 0.4).min(0.07), ha));
        let lightest = max_luminance(&[
            get(&t, "surface-raised"),
            get(&t, "accent-soft"),
            get(&t, "background"),
        ]);
        let at = lighten_to(&lightest, 5.0, ha, ca.min(0.16), la.max(0.70));
        set(&mut t, "accent-text", at);
        let focus = lighten_to(get(&t, "surface-raised"), 4.0, ha, ca, la + 0.06);
        set(&mut t, "focus", focus);
        let cursor = get(&t, "accent").to_string();
        set(&mut t, "cursor", cursor);
        t
    }

    /// The contrast rows of one theme: (fg, bg, ratio, minimum)
    pub fn checks(&self, t: &Tokens) -> Vec<(String, String, f64, f64)> {
        let mut rows = Vec::new();
        let s = ["background", "surface", "surface-raised"];
        let mut chk = |fg: &str, fgc: &str, bgs: &[&str], min: f64| {
            for b in bgs {
                rows.push((fg.to_string(), b.to_string(), contrast(fgc, get(t, b)), min));
            }
        };
        chk("text", self.fixed("text"), &s, 4.5);
        chk("text-muted", self.fixed("text-muted"), &s, 4.5);
        chk("text-faint", self.fixed("text-faint"), &s, 3.0);
        chk("border-strong", self.fixed("border-strong"), &s, 3.0);
        chk(
            "accent-text",
            get(t, "accent-text"),
            &["background", "surface", "surface-raised", "accent-soft"],
            4.5,
        );
        chk("focus", get(t, "focus"), &s, 3.0);
        chk("accent", get(t, "accent"), &["background", "surface"], 3.0);
        for k in ["accent", "accent-hover", "accent-pressed"] {
            rows.push((
                "on-accent".into(),
                k.into(),
                contrast(get(t, "on-accent"), get(t, k)),
                4.5,
            ));
        }
        rows.push((
            "term text".into(),
            "selection".into(),
            contrast("#e6e0d4", get(t, "selection")),
            4.5,
        ));
        rows.push((
            "cursor".into(),
            "background".into(),
            contrast(get(t, "cursor"), get(t, "background")),
            3.0,
        ));
        rows.push((
            "border-active".into(),
            "background".into(),
            contrast(get(t, "border-active"), get(t, "background")),
            1.8,
        ));
        rows
    }
}

/// The first of the colours with the highest luminance, as Python's max(key=luminance)
pub fn max_luminance(colours: &[&str]) -> String {
    let mut best = colours[0];
    for c in &colours[1..] {
        if luminance(c) > luminance(best) {
            best = c;
        }
    }
    best.to_string()
}

/// Raises L until the colour reaches the contrast minimum on bg
pub fn lighten_to(bg: &str, minimum: f64, h: f64, c: f64, mut l: f64) -> String {
    let mut col = oklch(l, c, h);
    while contrast(&col, bg) < minimum && l < 0.97 {
        l += 0.01;
        col = oklch(l, c, h);
    }
    col
}

/// The border of the focused window: the accent, quietened toward the border
fn border_active(t: &Tokens) -> String {
    let (la, ca, ha) = to_oklch(get(t, "accent"));
    let lb = to_oklch(get(t, "border")).0;
    oklch(lb + 0.38 * (la - lb), ca * 0.5, ha)
}
