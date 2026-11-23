//! The engraving wallpapers: two plates per theme, a dark and a light one.
//!
//! The scan comes from an open-access collection (Rijksmuseum, public domain, or Art Institute of
//! Chicago, CC0) at its full resolution and is cropped at 16:9 so it fills the screen. Ink and
//! paper are neutral; the only colour is the theme's. The dark plate is almost black with a glow
//! around a fine ring in the accent on the head of the god. The light plate is lit from the
//! middle, and the paper inside the ring takes the accent.

use image::imageops::{self, FilterType};
use image::{GrayImage, Luma, Rgb, RgbImage};
use std::fs;
use std::io::BufWriter;
use std::path::{Path, PathBuf};
use std::process::Command;

pub const W: u32 = 2560;
pub const H: u32 = 1440;
/// Ink, paper and hair line of every plate
const INK: [f64; 3] = [8.0, 7.0, 7.0];
const PAPER: [f64; 3] = [186.0, 184.0, 178.0];
const LINE: [f64; 3] = [214.0, 208.0, 196.0];

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

/// The dark plate or the light one
#[derive(Clone, Copy, PartialEq, Eq)]
pub enum Mode {
    Dark,
    Light,
}

pub struct Print<'a> {
    pub accent: &'a str,
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
fn disc_mask(x: f64, y: f64, d: &Disc) -> f64 {
    let dist = ((x - d.x).powi(2) + (y - d.y).powi(2)).sqrt();
    ((d.r - dist) / 1.5 + 0.5).clamp(0.0, 1.0)
}

/// Coverage of a circle line of `width` pixels with radius `r`, at `dist` from the centre
fn ring(dist: f64, r: f64, width: f64) -> f64 {
    (width / 2.0 + 0.5 - (dist - r).abs()).clamp(0.0, 1.0)
}

/// Prints `scan` as a wallpaper of 2560 by 1440 in the colour of one theme
pub fn make(scan: &Path, box_: [f64; 3], disc: Disc, print: &Print, mode: Mode, out: &Path) {
    let gray = image::open(scan)
        .unwrap_or_else(|e| panic!("cannot read {}: {e}", scan.display()))
        .to_luma8();
    let g = crop(&gray, box_);
    let mut sorted: Vec<u8> = g.as_raw().clone();
    sorted.sort_unstable();
    let (lo, hi) = (percentile(&sorted, 1.5), percentile(&sorted, 93.0));
    let mut discs: Vec<(&Disc, [f64; 3])> = vec![(&disc, rgb(print.accent))];
    discs.extend(print.more.iter().map(|(d, c)| (d, rgb(c))));
    // The light plate is lit from between the discs
    let n = discs.len() as f64;
    let cx = discs.iter().map(|(d, _)| d.x).sum::<f64>() / n;
    let cy = discs.iter().map(|(d, _)| d.y).sum::<f64>() / n;
    let mut img = RgbImage::new(W, H);
    for (px, py, p) in img.enumerate_pixels_mut() {
        let (x, y) = (f64::from(px), f64::from(py));
        let l = ((f64::from(g.get_pixel(px, py)[0]) - lo) / (hi - lo))
            .clamp(0.0, 1.0)
            .powf(1.25); // 0 ink, 1 paper
        let light = match mode {
            Mode::Light => 0.07 + 0.74 * (-((x - cx).hypot(y - cy) / 760.0).powf(2.2)).exp(),
            Mode::Dark => {
                let glow = |d: &Disc| {
                    0.62 * (-((x - d.x).hypot(y - d.y) / (d.r * 1.3).max(300.0)).powi(2)).exp()
                };
                (0.035 + discs.iter().map(|(d, _)| glow(d)).sum::<f64>()).min(0.7)
            }
        };
        let mut paper = PAPER.map(|c| c * light);
        if mode == Mode::Light {
            for (d, col) in &discs {
                let m = disc_mask(x, y, d);
                for k in 0..3 {
                    paper[k] = paper[k] * (1.0 - m) + col[k] * (0.34 + 0.62 * light) * m;
                }
            }
        }
        let mut c = [0, 1, 2].map(|k| INK[k] + (paper[k] - INK[k]) * l);
        // Two hair lines around every disc: its edge, in the accent on the dark plate, and one outside it
        for (d, col) in &discs {
            let dist = (x - d.x).hypot(y - d.y);
            let (edge, outer) = match mode {
                Mode::Dark => ((ring(dist, d.r, 1.6) * 0.92, *col), 0.27),
                Mode::Light => ((ring(dist, d.r, 2.2) * 0.92, LINE), 0.47),
            };
            let outer = ring(dist, d.r + 14.0, 1.0) * outer;
            for k in 0..3 {
                c[k] = c[k] * (1.0 - edge.0) + edge.1[k] * edge.0;
                c[k] = c[k] * (1.0 - outer) + LINE[k] * outer;
            }
        }
        *p = Rgb(c.map(|v| v.round().clamp(0.0, 255.0) as u8));
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

/// strixui wallpapers [god ...]: remakes the dark and the light plate of the gods in src/wallpapers/
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
            accent: crate::gods::get(&t, "accent"),
            more: Vec::new(),
        };
        let scan = fetch(&cache, &src.repo, p["source"].as_str().expect("source"));
        for (mode, file) in [
            (Mode::Dark, format!("{n}.jpg")),
            (Mode::Light, format!("{n}-light.jpg")),
        ] {
            let out = src.root.join("wallpapers").join(&file);
            make(
                &scan,
                three(&p["crop"]),
                Disc { x, y, r },
                &print,
                mode,
                &out,
            );
            println!(
                "{file}  {} bytes  ({})",
                fs::metadata(&out).map(|m| m.len()).unwrap_or(0),
                p["credit"].as_str().unwrap_or("")
            );
        }
    }
}
