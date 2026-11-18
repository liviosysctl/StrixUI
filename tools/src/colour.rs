//! Colour maths: sRGB, WCAG contrast and OKLCH, the way the themes are derived.

pub fn hex2rgb(h: &str) -> [u8; 3] {
    let h = h.trim_start_matches('#');
    let byte = |i: usize| u8::from_str_radix(&h[i..i + 2], 16).expect("a hex colour");
    [byte(0), byte(2), byte(4)]
}

pub fn rgb2hex(rgb: [f64; 3]) -> String {
    let c = |v: f64| crate::py::round_int(v.clamp(0.0, 255.0)) as u8;
    format!("#{:02x}{:02x}{:02x}", c(rgb[0]), c(rgb[1]), c(rgb[2]))
}

fn lin(c: u8) -> f64 {
    let c = f64::from(c) / 255.0;
    if c <= 0.04045 {
        c / 12.92
    } else {
        ((c + 0.055) / 1.055).powf(2.4)
    }
}

fn gam(c: f64) -> f64 {
    let c = c.clamp(0.0, 1.0);
    255.0
        * if c <= 0.0031308 {
            12.92 * c
        } else {
            1.055 * c.powf(1.0 / 2.4) - 0.055
        }
}

pub fn luminance(h: &str) -> f64 {
    let [r, g, b] = hex2rgb(h);
    0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)
}

pub fn contrast(a: &str, b: &str) -> f64 {
    let (la, lb) = (luminance(a), luminance(b));
    let (hi, lo) = if la >= lb { (la, lb) } else { (lb, la) };
    (hi + 0.05) / (lo + 0.05)
}

/// (L, C, H in degrees)
pub fn to_oklch(h: &str) -> (f64, f64, f64) {
    let [r, g, b] = hex2rgb(h).map(lin);
    let l = (0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b).powf(1.0 / 3.0);
    let m = (0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b).powf(1.0 / 3.0);
    let s = (0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b).powf(1.0 / 3.0);
    let ll = 0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s;
    let a = 1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s;
    let bb = 0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s;
    (ll, a.hypot(bb), bb.atan2(a).to_degrees().rem_euclid(360.0))
}

fn oklch_rgb(l: f64, c: f64, h: f64) -> [f64; 3] {
    let (a, b) = (c * h.to_radians().cos(), c * h.to_radians().sin());
    let l_ = (l + 0.3963377774 * a + 0.2158037573 * b).powi(3);
    let m_ = (l - 0.1055613458 * a - 0.0638541728 * b).powi(3);
    let s_ = (l - 0.0894841775 * a - 1.2914855480 * b).powi(3);
    [
        4.0767416621 * l_ - 3.3077115913 * m_ + 0.2309699292 * s_,
        -1.2684380046 * l_ + 2.6097574011 * m_ - 0.3413193965 * s_,
        -0.0041960863 * l_ - 0.7034186147 * m_ + 1.7076147010 * s_,
    ]
}

/// OKLCH to hex; chroma is reduced until the colour fits sRGB
pub fn oklch(l: f64, mut c: f64, h: f64) -> String {
    while c > 0.0 {
        let rgb = oklch_rgb(l, c, h);
        if rgb.iter().all(|v| (-1e-4..=1.0 + 1e-4).contains(v)) {
            break;
        }
        c -= 0.002;
    }
    rgb2hex(oklch_rgb(l, c.max(0.0), h).map(gam))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn round_trips() {
        assert_eq!(rgb2hex([200.0, 16.0, 46.0]), "#c8102e");
        let (l, c, h) = to_oklch("#c8102e");
        assert_eq!(oklch(l, c, h), "#c8102e");
        assert!((contrast("#ffffff", "#000000") - 21.0).abs() < 1e-9);
    }
}
