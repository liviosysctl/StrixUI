//! The themes of Strix: one per Roman god, each a plate and a set of colours (src/design/gods.json).
//!
//! The colours of a theme are a small set of tokens that follow the god: a tinted background and its
//! surfaces, the accent and everything derived from it (the keywords of code and the first series of
//! a chart too), and the terminal cursor and selection. Text, line, the other status colours and the
//! rest of the syntax stay as they are in every theme; the error turns to vermilion where the accent
//! itself is red. The accent of each god is picked by hand; the rest is derived in OKLCH so every
//! theme has the lightness steps of Saturnus.

use crate::colour::{contrast, luminance, oklch, to_oklch};
use serde_json::{Map, Value};

/// A theme's colour tokens in the order they are derived
pub type Tokens = Vec<(String, String)>;

/// The grounds of the light variant: smoked glass on dark grey instead of black, and the faint text
/// one step lighter so it keeps 4.5:1 on them
const LIGHT_GROUNDS: [(&str, &str); 7] = [
    ("background", "#101011"),
    ("surface", "#1b1b1c"),
    ("surface-raised", "#242425"),
    ("surface-sunken", "#0c0c0d"),
    ("border", "#3a3a3c"),
    ("border-strong", "#7c7872"),
    ("text-faint", "#8a857e"),
];

/// The colour of an error, and the one it takes where the accent is red as well
const ERROR: &str = "#ff6b78";
const ERROR_BESIDE_RED: &str = "#f8875a";
/// Closer than this in OKLCH hue, an error would read as the accent
const ERROR_APART: f64 = 30.0;

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
        follow(&mut t);
        t
    }

    /// The light variant of a god's theme: the same colours on neutral dark grey grounds, one step
    /// lighter than the dark ones. The accent text and the focus ring are made again for these
    /// grounds.
    pub fn light(&self, id: &str) -> Tokens {
        let mut t = self.colours(id);
        for (k, v) in LIGHT_GROUNDS {
            set(&mut t, k, v.to_string());
        }
        // On the grey grounds a dark accent loses its edge: raised just enough to keep 3:1 there
        let surface = get(&t, "surface").to_string();
        if contrast(get(&t, "accent"), &surface) < 3.0 {
            let (mut la, ca, ha) = to_oklch(get(&t, "accent"));
            while contrast(&oklch(la, ca, ha), &surface) < 3.0 {
                la += 0.005;
            }
            set(&mut t, "accent", oklch(la, ca, ha));
            set(&mut t, "accent-hover", oklch(la + 0.04, ca, ha));
            set(&mut t, "accent-pressed", oklch(la - 0.05, ca, ha));
        }
        let (la, ca, ha) = to_oklch(get(&t, "accent"));
        let raised = get(&t, "surface-raised").to_string();
        set(
            &mut t,
            "accent-text",
            lighten_to(&raised, 5.0, ha, ca.min(0.16), la.max(0.70)),
        );
        set(&mut t, "focus", lighten_to(&raised, 4.0, ha, ca, la + 0.06));
        let ba = border_active(&t);
        set(&mut t, "border-active", ba);
        follow(&mut t);
        t
    }

    /// Every theme token for an accent that is not a god's, border-active included (pack)
    pub fn derive_all(&self, accent: &str) -> Tokens {
        let mut t = self.derive(accent);
        let ba = border_active(&t);
        set(&mut t, "border-active", ba);
        follow(&mut t);
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
        // The light variant brings its own faint text and strong border
        let own = |name: &str| {
            t.iter()
                .find(|(k, _)| k == name)
                .map_or_else(|| self.fixed(name), |(_, v)| v.as_str())
        };
        chk("text-faint", own("text-faint"), &s[..2], 4.5);
        chk("error", get(t, "error"), &s, 4.5);
        chk("border-strong", own("border-strong"), &s, 3.0);
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

/// The border of the focused window: the accent itself. Every other line stays quiet.
fn border_active(t: &Tokens) -> String {
    get(t, "accent").to_string()
}

/// The tokens that follow the accent outside its family: the keywords of code take the accent
/// text, the first series of a chart the accent, and the error moves off a red accent
fn follow(t: &mut Tokens) {
    let text = get(t, "accent-text").to_string();
    let accent = get(t, "accent").to_string();
    set(t, "syntax-keyword", text);
    set(t, "chart-1", accent.clone());
    set(t, "error", error_for(&accent).to_string());
}

/// Red, unless the accent is red too: then vermilion, as long as that lies further from it
fn error_for(accent: &str) -> &'static str {
    let h = to_oklch(accent).2;
    let apart = |c: &str| {
        let d = (h - to_oklch(c).2).abs() % 360.0;
        d.min(360.0 - d)
    };
    if apart(ERROR) < ERROR_APART && apart(ERROR_BESIDE_RED) > apart(ERROR) {
        ERROR_BESIDE_RED
    } else {
        ERROR
    }
}
