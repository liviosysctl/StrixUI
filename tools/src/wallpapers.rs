//! The engraving wallpapers: one plate per theme, printed in two inks of its colours.
//!
//! The scan comes from an open-access collection (Art Institute of Chicago, CC0, or Rijksmuseum,
//! public domain), is cropped to the upper body at 16:9 and printed in two inks: paper becomes the
//! cream `line` colour, ink becomes the theme's `background`, and ink inside one disc becomes its
//! `accent`. The picture is darkened toward the edges, hardest along the top (bar) and the bottom
//! (dock), gets a little grain and fine lines around the disc.

use image::imageops::{self, FilterType};
use image::{GrayImage, Luma, Rgb, RgbImage};
use std::f64::consts::PI;
use std::fs;
use std::io::BufWriter;
use std::path::{Path, PathBuf};
use std::process::Command;

pub const W: u32 = 2560;
pub const H: u32 = 1440;
const CREAM: [f64; 3] = [216.0, 208.0, 192.0];

/// A plate source: aic:<IIIF id>, rijks:<Micrio id>:<width> or file:<path>
pub fn fetch(cache: &Path, base: &Path, source: &str) -> PathBuf {
    let (kind, rest) = source
        .split_once(':')
        .unwrap_or_else(|| panic!("not a plate source: {source}"));
    let (path, url) = match kind {
        "file" => return base.join(rest),
        "aic" => (
            cache.join(format!("{rest}.jpg")),
            format!("https://www.artic.edu/iiif/2/{rest}/full/3000,/0/default.jpg"),
        ),
        "rijks" => {
            let (id, width) = rest.split_once(':').unwrap_or((rest, "3000"));
            (
                cache.join(format!("rijks-{id}.jpg")),
                format!("https://iiif.micr.io/{id}/full/{width},/0/default.jpg"),
            )
        }
        _ => panic!("unknown plate source: {source}"),
    };
    if !path.exists() {
        fs::create_dir_all(cache).expect("the engraving cache");
        let part = path.with_extension("part");
        let ok = Command::new("curl")
            .args([
                "-fsSL",
                "--max-time",
                "300",
                "-A",
                "strixui-wallpapers",
                "-o",
            ])
            .arg(&part)
            .arg(&url)
            .status()
            .map(|s| s.success())
            .unwrap_or(false);
        assert!(ok, "cannot download {url} (curl is needed)");
        fs::rename(&part, &path).expect("the scan");
    }
    path
}

/// A disc of the accent, or of the second colour
pub struct Disc {
    pub x: f64,
    pub y: f64,
    pub r: f64,
}

pub struct Print<'a> {
    pub background: &'a str,
    pub accent: &'a str,
    /// Brightness of the paper, lower for a print with much bare paper
    pub paper: f64,
    pub vignette: f64,
    /// Discs in the second colour of a dual-colour theme
    pub more: Vec<(Disc, String)>,
}

fn rgb(hex: &str) -> [f64; 3] {
    crate::colour::hex2rgb(hex).map(f64::from)
}

/// The crop (x0, y0, x1 of the scan, the height follows from 16:9) at 2560 by 1440, sharpened a little
fn crop(scan: &GrayImage, box_: [f64; 3]) -> GrayImage {
    let (w, h) = (f64::from(scan.width()), f64::from(scan.height()));
    let [x0, y0, x1] = box_;
    let cw = (x1 - x0) * w;
    let ch = cw * f64::from(H) / f64::from(W);
    let (left, top) = ((x0 * w) as i64, (y0 * h) as i64);
    let (right, bottom) = ((x1 * w) as i64, (y0 * h + ch) as i64);
    // Outside the scan is black, as Pillow's crop does it
    let mut part = GrayImage::new((right - left) as u32, (bottom - top) as u32);
    for (x, y, p) in part.enumerate_pixels_mut() {
        let (sx, sy) = (left + i64::from(x), top + i64::from(y));
        if sx >= 0 && sy >= 0 && sx < i64::from(scan.width()) && sy < i64::from(scan.height()) {
            *p = *scan.get_pixel(sx as u32, sy as u32);
        }
    }
    let sized = imageops::resize(&part, W, H, FilterType::Lanczos3);
    // Unsharp mask: radius 2, 60 percent
    let blurred = imageops::blur(&sized, 2.0);
    let mut out = sized.clone();
    for (o, (a, b)) in out.pixels_mut().zip(sized.pixels().zip(blurred.pixels())) {
        let (a, b) = (f64::from(a[0]), f64::from(b[0]));
        *o = Luma([(a + 0.6 * (a - b)).round().clamp(0.0, 255.0) as u8]);
    }
    out
}

/// numpy's percentile with linear interpolation
fn percentile(sorted: &[u8], p: f64) -> f64 {
    let i = p / 100.0 * (sorted.len() - 1) as f64;
    let (lo, hi) = (i.floor() as usize, i.ceil() as usize);
    f64::from(sorted[lo]) + (f64::from(sorted[hi]) - f64::from(sorted[lo])) * (i - lo as f64)
}

/// Grain: a small deterministic generator with Box-Muller, the same picture every build
struct Grain(u64);

impl Grain {
    fn next(&mut self) -> f64 {
        // splitmix64
        self.0 = self.0.wrapping_add(0x9e37_79b9_7f4a_7c15);
        let mut z = self.0;
        z = (z ^ (z >> 30)).wrapping_mul(0xbf58_476d_1ce4_e5b9);
        z = (z ^ (z >> 27)).wrapping_mul(0x94d0_49bb_1331_11eb);
        ((z ^ (z >> 31)) >> 11) as f64 / (1u64 << 53) as f64
    }
    fn normal(&mut self, sigma: f64) -> f64 {
        let u = self.next().max(f64::MIN_POSITIVE);
        (-2.0 * u.ln()).sqrt() * (2.0 * PI * self.next()).cos() * sigma
    }
}

fn disc_mask(x: f64, y: f64, d: &Disc) -> f64 {
    let dist = ((x - d.x).powi(2) + (y - d.y).powi(2)).sqrt();
    ((d.r - dist) / 1.5 + 0.5).clamp(0.0, 1.0)
}

/// Coverage of a one-pixel line at distance `dist` from its centre
fn hair(dist: f64) -> f64 {
    (1.0 - dist.abs()).clamp(0.0, 1.0)
}

/// The fine lines around one disc: two circles, a graduated ring and, around the first disc, a wide circle
fn rings(x: f64, y: f64, d: &Disc, first: bool) -> f64 {
    let dist = ((x - d.x).powi(2) + (y - d.y).powi(2)).sqrt();
    let mut a: f64 = 0.0;
    let mut circles = vec![(d.r + 56.0, 120.0), (d.r + 64.0, 70.0)];
    if first {
        circles.push((d.r + 260.0, 60.0));
    }
    for (rr, alpha) in circles {
        a = a.max(hair(dist - rr + 0.5) * alpha / 255.0);
    }
    let r1 = d.r + 64.0;
    if dist >= r1 - 1.0 && dist <= r1 + 19.0 {
        // the nearest tick, one every 3 degrees, a long one every 15
        let angle = (y - d.y).atan2(x - d.x).to_degrees().rem_euclid(360.0);
        let i = ((angle / 3.0).round() as i64 * 3).rem_euclid(360);
        let len = if i % 15 == 0 { 18.0 } else { 9.0 };
        let t = (i as f64).to_radians();
        let (ux, uy) = (t.cos(), t.sin());
        let (px, py) = (x - d.x, y - d.y);
        let along = px * ux + py * uy;
        let across = -px * uy + py * ux;
        if along >= r1 - 0.5 && along <= r1 + len + 0.5 {
            a = a.max(hair(across) * 70.0 / 255.0);
        }
    }
    a
}

/// Prints `scan` as a wallpaper of 2560 by 1440 in the colours of one theme
pub fn make(scan: &Path, box_: [f64; 3], disc: Disc, print: &Print, out: &Path) {
    let gray = image::open(scan)
        .unwrap_or_else(|e| panic!("cannot read {}: {e}", scan.display()))
        .to_luma8();
    let g = crop(&gray, box_);
    let mut sorted: Vec<u8> = g.as_raw().clone();
    sorted.sort_unstable();
    let (lo, hi) = (percentile(&sorted, 3.0), percentile(&sorted, 97.0));
    let (bg, acc) = (rgb(print.background), rgb(print.accent));
    let more: Vec<(&Disc, [f64; 3])> = print.more.iter().map(|(d, c)| (d, rgb(c))).collect();
    let mut grain = Grain(3);
    let (w, h) = (f64::from(W), f64::from(H));
    let mut img = RgbImage::new(W, H);
    for (px, py, p) in img.enumerate_pixels_mut() {
        let (x, y) = (f64::from(px), f64::from(py));
        let l = ((f64::from(g.get_pixel(px, py)[0]) - lo) / (hi - lo))
            .clamp(0.0, 1.0)
            .powf(1.7); // 0 ink, 1 paper
        let m = disc_mask(x, y, &disc);
        // Outside the disc: dark ink on dim cream paper. Inside, the paper takes the accent, a little dulled
        // by the cream under it, and the ink stays dark, so light accents keep the engraving readable
        let mut pap = [0.0; 3];
        for k in 0..3 {
            pap[k] = CREAM[k] * print.paper * (1.0 - m)
                + (acc[k] * 0.90 + CREAM[k] * print.paper * 0.12) * m;
        }
        let mut f_disc = m * 0.9;
        for (d, col) in &more {
            let mk = disc_mask(x, y, d);
            for k in 0..3 {
                pap[k] = pap[k] * (1.0 - mk) + (col[k] * 0.90 + CREAM[k] * print.paper * 0.12) * mk;
            }
            f_disc = f_disc.max(mk * 0.9);
        }
        let dv = (((x - disc.x) / (w * 0.62)).powi(2) + ((y - disc.y) / (h * 0.78)).powi(2)).sqrt();
        let v = 1.0 - print.vignette * ((dv - 0.25) / 0.75).clamp(0.0, 1.0).powf(1.4);
        let top = (y / 110.0).clamp(0.35, 1.0);
        let bottom = ((h - y) / 90.0).clamp(0.45, 1.0);
        let f = (v * top * bottom).max(f_disc);
        let noise = grain.normal(3.2);
        // hair lines in cream: the rings around every disc and the meridian through the first
        let mut a = rings(x, y, &disc, true);
        for (d, _) in &more {
            a = a.max(rings(x, y, d, false));
        }
        a = a.max(hair(x - disc.x + 0.5) * 40.0 / 255.0);
        let mut c = [0u8; 3];
        for k in 0..3 {
            let ink = bg[k] * (1.0 - l) + pap[k] * l;
            let printed = (bg[k] + (ink - bg[k]) * f + noise)
                .clamp(0.0, 255.0)
                .floor();
            c[k] = (printed * (1.0 - a) + CREAM[k] * a)
                .round()
                .clamp(0.0, 255.0) as u8;
        }
        *p = Rgb(c);
    }
    if let Some(dir) = out.parent() {
        fs::create_dir_all(dir).expect("the wallpaper folder");
    }
    let file = BufWriter::new(
        fs::File::create(out).unwrap_or_else(|e| panic!("cannot write {}: {e}", out.display())),
    );
    image::codecs::jpeg::JpegEncoder::new_with_quality(file, 84)
        .encode_image(&img)
        .expect("a JPEG");
}

/// A whole scene that is taller than 16:9: the part `fit` (x0, y0, x1, y1 of the scan) set whole on a
/// 2560 by 1440 ground of ink, `place` = (centre x, height as a share of 1440), its edges fading into the ink
pub fn fitted(scan: &Path, fit: [f64; 4], place: [f64; 2], cache: &Path) -> PathBuf {
    let im = image::open(scan)
        .unwrap_or_else(|e| panic!("cannot read {}: {e}", scan.display()))
        .to_luma8();
    let (w, h) = (f64::from(im.width()), f64::from(im.height()));
    let (x0, y0) = ((fit[0] * w) as u32, (fit[1] * h) as u32);
    let part = imageops::crop_imm(
        &im,
        x0,
        y0,
        (fit[2] * w) as u32 - x0,
        (fit[3] * h) as u32 - y0,
    )
    .to_image();
    let ph = (f64::from(H) * place[1]) as u32;
    let pw = (f64::from(part.width()) * f64::from(ph) / f64::from(part.height())) as u32;
    let part = imageops::resize(&part, pw, ph, FilterType::Lanczos3);
    let mut ground = GrayImage::new(W, H);
    let (x, y) = (
        (place[0] - f64::from(pw) / 2.0) as i64,
        i64::from((H - ph) / 2),
    );
    for (px, py, p) in part.enumerate_pixels() {
        let edge = px.min(pw - 1 - px).min(py.min(ph - 1 - py));
        let mask = (f64::from(edge) / 120.0).clamp(0.0, 1.0).powf(1.5);
        let (gx, gy) = (x + i64::from(px), y + i64::from(py));
        if gx >= 0 && gx < i64::from(W) && gy >= 0 && gy < i64::from(H) {
            ground.put_pixel(gx as u32, gy as u32, Luma([(f64::from(p[0]) * mask) as u8]));
        }
    }
    let stem = scan.file_stem().and_then(|s| s.to_str()).unwrap_or("scan");
    let out = cache.join(format!("fitted-{stem}.png"));
    fs::create_dir_all(cache).expect("the engraving cache");
    ground.save(&out).expect("the fitted scan");
    out
}

fn f(v: &serde_json::Value) -> f64 {
    v.as_f64().expect("a number")
}

pub fn three(v: &serde_json::Value) -> [f64; 3] {
    let a = v.as_array().expect("three numbers");
    [f(&a[0]), f(&a[1]), f(&a[2])]
}

/// strixui wallpapers [god ...]: remakes the plates of the eight gods in src/wallpapers/
pub fn gods(src: &crate::Src, gods: &crate::gods::Gods, names: &[String]) {
    let plates = crate::read_json(&src.root.join("design/plates.json"));
    let cache = src.repo.join("build/engravings");
    let names: Vec<String> = if names.is_empty() {
        gods.gods.iter().map(|g| g.id.clone()).collect()
    } else {
        names.to_vec()
    };
    for n in &names {
        let p = plates.get(n).unwrap_or_else(|| panic!("no plate for {n}"));
        let t = gods.colours(n);
        let [x, y, r] = three(&p["disc"]);
        let print = Print {
            background: crate::gods::get(&t, "background"),
            accent: crate::gods::get(&t, "accent"),
            paper: p.get("paper").map(f).unwrap_or(0.46),
            vignette: p.get("vig").map(f).unwrap_or(0.92),
            more: Vec::new(),
        };
        let out = src.root.join("wallpapers").join(format!("{n}.jpg"));
        make(
            &fetch(&cache, &src.repo, p["source"].as_str().expect("source")),
            three(&p["crop"]),
            Disc { x, y, r },
            &print,
            &out,
        );
        println!(
            "{n}.jpg  {} bytes  ({})",
            fs::metadata(&out).map(|m| m.len()).unwrap_or(0),
            p["credit"].as_str().unwrap_or("")
        );
    }
}
