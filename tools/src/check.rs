//! strixui check: the contrast of every colour pair of the palette and of every god theme.

use crate::colour::contrast;
use crate::gods::Gods;
use crate::tokens::Palette;

/// A minimum as the old tools printed it: 3, 4.5
fn min(x: f64) -> String {
    if x.fract() == 0.0 {
        format!("{x:.0}")
    } else {
        format!("{x}")
    }
}

/// Prints every row, returns the number of failures
pub fn palette(p: &Palette) -> usize {
    let s = ["background", "surface", "surface-raised"];
    let mut rows: Vec<(String, String, f64, f64)> = Vec::new();
    let mut chk = |fg: &str, bgs: &[&str], m: f64| {
        for b in bgs {
            rows.push((fg.into(), (*b).into(), contrast(&p.c(fg), &p.c(b)), m));
        }
    };
    chk("text", &s, 4.5);
    chk("text-muted", &s, 4.5);
    chk(
        "on-accent",
        &["accent", "accent-hover", "accent-pressed"],
        4.5,
    );
    chk("error", &s, 4.5);
    chk("focus", &s, 3.0);
    chk("accent-text", &s, 4.5);
    chk("warning", &s, 4.5);
    chk("success", &s, 4.5);
    chk("info", &s, 4.5);
    chk("border-strong", &s, 3.0);
    chk("text-faint", &s, 3.0);
    chk("accent", &["background", "surface"], 3.0);
    let syntax: Vec<String> = p
        .colors
        .keys()
        .filter(|k| k.starts_with("syntax-"))
        .cloned()
        .collect();
    for k in &syntax {
        chk(k, &["background", "surface"], 4.5);
    }
    for k in ["chart-1", "chart-2", "chart-3", "chart-4", "chart-5"] {
        chk(k, &["surface"], 3.0);
    }
    chk("accent-text", &["accent-soft"], 4.5);
    for k in p.terminal.keys() {
        if !matches!(k.as_str(), "background" | "cursor" | "selection" | "black") {
            rows.push((
                format!("term {k}"),
                "term bg".into(),
                contrast(&p.t(k), &p.t("background")),
                4.5,
            ));
        }
    }
    rows.push((
        "term fg".into(),
        "selection".into(),
        contrast(&p.t("foreground"), &p.t("selection")),
        4.5,
    ));
    rows.push((
        "term cursor".into(),
        "term bg".into(),
        contrast(&p.t("cursor"), &p.t("background")),
        3.0,
    ));
    let mut fails = 0;
    for (fg, bg, r, m) in &rows {
        let ok = *r >= *m;
        fails += usize::from(!ok);
        println!(
            "{fg:22} on {bg:16} {r:5.2} (min {}) {}",
            min(*m),
            if ok { "ok" } else { "FAIL" }
        );
    }
    println!("FAILS {fails}");
    fails
}

pub fn themes(g: &Gods) -> usize {
    let mut fails = 0;
    for god in &g.gods {
        let t = g.colours(&god.id);
        let parts: Vec<String> = t
            .iter()
            .map(|(k, v)| format!("{}={v}", k.replace("accent-", "a-").replace("surface", "s")))
            .collect();
        println!("{:<10} {}", god.id, parts.join(" "));
        let rows = g.checks(&t);
        for (fg, bg, r, m) in &rows {
            if r < m {
                fails += 1;
                println!("   FAIL {fg:<14} on {bg:<14} {r:.2} (min {})", min(*m));
            }
        }
        let lo = rows
            .iter()
            .min_by(|a, b| (a.2 / a.3).total_cmp(&(b.2 / b.3)))
            .expect("rows");
        println!(
            "   lowest margin: {} on {} {:.2} (min {})",
            lo.0,
            lo.1,
            lo.2,
            min(lo.3)
        );
    }
    println!("FAILS {fails}");
    fails
}
