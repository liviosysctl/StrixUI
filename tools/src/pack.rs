//! strixui pack REPO [--check]: builds a theme repository, themes outside the eight gods with the same
//! colour rules and the same wallpaper treatment.
//!
//! A theme repository (layout 1, see the README of strix-theme-template) holds strix-themes.toml and
//! themes/<id>/ with theme.toml (theme engine format 1), wallpaper.jpg and wallpaper.toml. Its
//! source.toml is the recipe:
//!
//!     [[theme]]
//!     id = "lucifer"
//!     name = "Lucifer"
//!     description = "One line about the colour."
//!     accent = [0.55, 0.10, 32]            # OKLCH lightness, chroma, hue; or "#rrggbb"
//!     accent2 = [0.74, 0.10, 85]           # optional second colour: lines and letters (accent-text, focus) and discs2
//!     [theme.plate]
//!     source = "rijks:Tgakd:3200"          # rijks:<Micrio id>:<width>, aic:<IIIF id>, or file:<path in the repository>
//!     crop = [0.05, 0.42, 0.95]            # x0, y0, x1 of the scan; the height follows from 16:9
//!     # or, for a scene taller than 16:9, set it whole on a ground of ink instead of crop:
//!     # fit = [0.04, 0.03, 0.95, 0.86]     # x0, y0, x1, y1 of the scan
//!     # place = [1500, 0.96]               # centre x on the 2560 by 1440 picture, height as a share of 1440
//!     disc = [1330, 520, 260]              # centre and radius of the accent disc on the 2560 by 1440 picture
//!     discs2 = [[900, 300, 120]]           # optional, with accent2: discs in the second colour
//!     caption = "What it shows and who made it."
//!     credit = "Maker, title, date. Collection, number, licence"
//!     licence = "public domain"            # public domain or CC0 only

use crate::colour::{contrast, oklch, to_oklch};
use crate::gods::{Gods, get, lighten_to, max_luminance};
use crate::targets::{self, REQUIRED, TERMINAL, Table};
use crate::wallpapers::{self, Disc, Print};
use crate::{Src, py, read, read_json, write};
use regex::Regex;
use serde_json::Value;
use std::path::Path;
use toml::Value as Toml;

const LICENCES: [&str; 2] = ["public domain", "CC0"];

fn num(v: &Toml) -> f64 {
    v.as_float()
        .or_else(|| v.as_integer().map(|i| i as f64))
        .expect("a number")
}

fn nums(v: &Toml) -> Vec<f64> {
    v.as_array()
        .expect("a list of numbers")
        .iter()
        .map(num)
        .collect()
}

fn text<'a>(v: &'a Toml, key: &str) -> &'a str {
    v.get(key)
        .and_then(Toml::as_str)
        .unwrap_or_else(|| panic!("{key} is missing"))
}

fn accent(v: &Toml) -> String {
    match v.as_str() {
        Some(hex) => hex.to_string(),
        None => {
            let n = nums(v);
            oklch(n[0], n[1], n[2])
        }
    }
}

/// Every colour token of the design system for this theme: the derived ones, the rest as in the default
/// theme. With accent2 a dual-colour theme: accent fills everything that is filled (buttons, progress, the
/// first disc), the second colour takes everything that is a line or a letter (accent-text, focus) and the
/// second disc.
fn table(spec: &Toml, t: &Value, gods: &Gods) -> Table {
    let mut derived = gods.derive_all(&accent(&spec["accent"]));
    if let Some(a2) = spec.get("accent2") {
        let second = gods.derive_all(&accent(a2));
        let (l, c, h) = to_oklch(get(&second, "accent"));
        let lightest = max_luminance(&[
            get(&derived, "surface-raised"),
            get(&derived, "accent-soft"),
        ]);
        let at = lighten_to(&lightest, 5.0, h, c.min(0.16), l.max(0.70));
        let focus = lighten_to(get(&derived, "surface-raised"), 4.0, h, c, l + 0.06);
        crate::gods::set(&mut derived, "accent-text", at);
        crate::gods::set(&mut derived, "focus", focus);
        crate::gods::set(&mut derived, "accent-2", get(&second, "accent").to_string());
    }
    let first = &gods.gods[0].id;
    let mut tab = targets::table(t, first, first);
    for (k, v) in derived {
        if k == "cursor" || k == "selection" {
            set(&mut tab.terminal, &k, v);
        } else if k == "accent-2" || tab.colors.iter().any(|(n, _)| *n == k) {
            set(&mut tab.colors, &k, v);
        }
    }
    let bg = tab.c("background").to_string();
    set(&mut tab.terminal, "background", bg);
    tab
}

fn set(list: &mut Vec<(String, String)>, k: &str, v: String) {
    match list.iter_mut().find(|(n, _)| n == k) {
        Some(e) => e.1 = v,
        None => list.push((k.to_string(), v)),
    }
}

fn checks(id: &str, tab: &Table) -> Vec<String> {
    let mut fails = Vec::new();
    let mut need = |what: String, a: &str, b: &str, minimum: f64| {
        let r = contrast(a, b);
        if r < minimum {
            fails.push(format!(
                "{id}: {what} {r:.2} < {}",
                if minimum.fract() == 0.0 {
                    format!("{minimum:.0}")
                } else {
                    minimum.to_string()
                }
            ));
        }
    };
    for g in ["background", "surface", "surface-raised"] {
        for (fg, min) in [
            ("text", 4.5),
            ("text-muted", 4.5),
            ("accent-text", 4.5),
            ("error", 4.5),
            ("focus", 3.0),
            ("border-strong", 3.0),
        ] {
            need(format!("{fg} on {g}"), tab.c(fg), tab.c(g), min);
        }
    }
    for k in ["accent", "accent-hover", "accent-pressed"] {
        need(
            format!("on-accent on {k}"),
            tab.c("on-accent"),
            tab.c(k),
            4.5,
        );
    }
    need(
        "terminal foreground".into(),
        tab.t("foreground"),
        tab.t("background"),
        4.5,
    );
    fails
}

fn theme_toml(spec: &Toml, tab: &Table) -> String {
    let (name, description) = (text(spec, "name"), text(spec, "description"));
    let mut o = vec![
        format!("# {name}. {description}"),
        "# Made with strixui pack from source.toml. Change source.toml and build again.".into(),
        "format = 1".into(),
        format!("name = \"{name}\""),
        format!(
            "description = {}",
            py::json_ascii(&Value::String(description.into()))
        ),
        "default-variant = \"dark\"".into(),
        String::new(),
        "[variants.dark]".into(),
        "name = \"Dark\"".into(),
        "appearance = \"dark\"".into(),
        String::new(),
        "[variants.dark.colors]".into(),
    ];
    for n in REQUIRED {
        o.push(format!("{n} = \"{}\"", tab.c(n)));
    }
    o.push("# every other token of the design system, under its own name".into());
    for (n, v) in &tab.colors {
        if !REQUIRED.contains(&n.as_str()) {
            o.push(format!("{n} = \"{v}\""));
        }
    }
    o.push(String::new());
    o.push("[variants.dark.terminal]".into());
    for n in TERMINAL {
        o.push(format!("{n} = \"{}\"", tab.t(n)));
    }
    o.join("\n") + "\n"
}

pub fn wallpaper_toml(caption: &str, credit: &str, licence: &str) -> String {
    let q = |s: &str| py::json_ascii(&Value::String(s.into()));
    format!(
        "caption = {}\ncredit = {}\nlicence = {}\n",
        q(caption),
        q(credit),
        q(licence)
    )
}

pub fn build(src: &Src, gods: &Gods, repo: &Path, only_check: bool) -> bool {
    let source: Toml =
        toml::from_str(&read(&repo.join("source.toml"))).expect("source.toml is not TOML");
    let t = read_json(&src.repo.join("design-system/tokens.json"));
    let id_re = Regex::new(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$").expect("regex");
    let cache = src.repo.join("build/engravings");
    let mut fails = Vec::new();
    let empty = Vec::new();
    for spec in source
        .get("theme")
        .and_then(Toml::as_array)
        .unwrap_or(&empty)
    {
        let id = text(spec, "id");
        if !id_re.is_match(id) || id.len() > 32 {
            fails.push(format!(
                "{id}: the id must be lowercase letters, digits and single hyphens"
            ));
        }
        let plate = &spec["plate"];
        let licence = plate.get("licence").and_then(Toml::as_str).unwrap_or("");
        if !LICENCES.contains(&licence) {
            fails.push(format!("{id}: the picture must be public domain or CC0"));
        }
        let tab = table(spec, &t, gods);
        fails.extend(checks(id, &tab));
        if only_check {
            continue;
        }
        let d = repo.join("themes").join(id);
        write(&d.join("theme.toml"), &theme_toml(spec, &tab));
        write(
            &d.join("wallpaper.toml"),
            &wallpaper_toml(text(plate, "caption"), text(plate, "credit"), licence),
        );
        let mut scan = wallpapers::fetch(&cache, repo, text(plate, "source"));
        if let Some(fit) = plate.get("fit") {
            let f = nums(fit);
            let place = plate
                .get("place")
                .map(nums)
                .unwrap_or_else(|| vec![1280.0, 0.96]);
            scan = wallpapers::fitted(
                &scan,
                [f[0], f[1], f[2], f[3]],
                [place[0], place[1]],
                &cache,
            );
        }
        let more = match tab.colors.iter().find(|(n, _)| n == "accent-2") {
            Some((_, a2)) => plate
                .get("discs2")
                .and_then(Toml::as_array)
                .unwrap_or(&empty)
                .iter()
                .map(|x| {
                    let n = nums(x);
                    (
                        Disc {
                            x: n[0],
                            y: n[1],
                            r: n[2],
                        },
                        a2.clone(),
                    )
                })
                .collect(),
            None => Vec::new(),
        };
        let crop = plate
            .get("crop")
            .map(nums)
            .unwrap_or_else(|| vec![0.0, 0.0, 1.0]);
        let disc = nums(&plate["disc"]);
        let print = Print {
            background: tab.c("background"),
            accent: tab.c("accent"),
            paper: plate.get("paper").map(num).unwrap_or(0.46),
            vignette: plate.get("vig").map(num).unwrap_or(0.92),
            more,
        };
        wallpapers::make(
            &scan,
            [crop[0], crop[1], crop[2]],
            Disc {
                x: disc[0],
                y: disc[1],
                r: disc[2],
            },
            &print,
            &d.join("wallpaper.jpg"),
        );
        println!(
            "{id}  accent {} on {}",
            tab.c("accent"),
            tab.c("background")
        );
    }
    for f in &fails {
        println!("FAIL {f}");
    }
    println!("FAILS {}", fails.len());
    fails.is_empty()
}
