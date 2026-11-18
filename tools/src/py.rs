//! Text the way the old Python tools wrote it, so the design system stays byte for byte the same:
//! JSON as `json.dumps` writes it, and the number formats `repr`, `%g` and `round` produce.

use serde_json::Value;

/// `json.dumps(v, ensure_ascii=False)` (`indent` None) or with `indent=n`
pub fn json(v: &Value, indent: Option<usize>) -> String {
    let mut out = String::new();
    write(&mut out, v, indent, 0, false);
    out
}

/// `json.dumps(v)`: compact, everything beyond ASCII as \uXXXX
pub fn json_ascii(v: &Value) -> String {
    let mut out = String::new();
    write(&mut out, v, None, 0, true);
    out
}

fn write(out: &mut String, v: &Value, indent: Option<usize>, depth: usize, ascii: bool) {
    match v {
        Value::Null => out.push_str("null"),
        Value::Bool(b) => out.push_str(if *b { "true" } else { "false" }),
        Value::Number(n) => {
            if let Some(i) = n.as_i64() {
                out.push_str(&i.to_string());
            } else if let Some(u) = n.as_u64() {
                out.push_str(&u.to_string());
            } else {
                out.push_str(&repr(n.as_f64().unwrap_or(0.0)));
            }
        }
        Value::String(s) => string_with(out, s, ascii),
        Value::Array(items) => {
            if items.is_empty() {
                out.push_str("[]");
                return;
            }
            out.push('[');
            for (i, item) in items.iter().enumerate() {
                sep(out, i, indent, depth + 1);
                write(out, item, indent, depth + 1, ascii);
            }
            close(out, indent, depth);
            out.push(']');
        }
        Value::Object(map) => {
            if map.is_empty() {
                out.push_str("{}");
                return;
            }
            out.push('{');
            for (i, (k, item)) in map.iter().enumerate() {
                sep(out, i, indent, depth + 1);
                string_with(out, k, ascii);
                out.push_str(": ");
                write(out, item, indent, depth + 1, ascii);
            }
            close(out, indent, depth);
            out.push('}');
        }
    }
}

fn sep(out: &mut String, i: usize, indent: Option<usize>, depth: usize) {
    match indent {
        Some(n) => {
            if i > 0 {
                out.push(',');
            }
            out.push('\n');
            out.push_str(&" ".repeat(n * depth));
        }
        None => {
            if i > 0 {
                out.push_str(", ");
            }
        }
    }
}

fn close(out: &mut String, indent: Option<usize>, depth: usize) {
    if let Some(n) = indent {
        out.push('\n');
        out.push_str(&" ".repeat(n * depth));
    }
}

/// A JSON string as Python writes it with ensure_ascii=False
pub fn string(out: &mut String, s: &str) {
    string_with(out, s, false);
}

fn string_with(out: &mut String, s: &str, ascii: bool) {
    out.push('"');
    for c in s.chars() {
        match c {
            '"' => out.push_str("\\\""),
            '\\' => out.push_str("\\\\"),
            '\n' => out.push_str("\\n"),
            '\r' => out.push_str("\\r"),
            '\t' => out.push_str("\\t"),
            '\u{8}' => out.push_str("\\b"),
            '\u{c}' => out.push_str("\\f"),
            c if (c as u32) < 0x20 => out.push_str(&format!("\\u{:04x}", c as u32)),
            c if ascii && !c.is_ascii() => {
                let mut units = [0u16; 2];
                for unit in c.encode_utf16(&mut units) {
                    out.push_str(&format!("\\u{unit:04x}"));
                }
            }
            c => out.push(c),
        }
    }
    out.push('"');
}

/// `json.dumps` of one string
pub fn quote(s: &str) -> String {
    let mut out = String::new();
    string(&mut out, s);
    out
}

/// `repr(float)`: the shortest text that reads back as the same number, with ".0" when whole
pub fn repr(x: f64) -> String {
    if x.is_finite() && x.fract() == 0.0 && x.abs() < 1e16 {
        format!("{x:.1}")
    } else if x != 0.0 && (x.abs() < 1e-4 || x.abs() >= 1e16) {
        let s = format!("{x:e}");
        // Rust writes 1e-5, Python 1e-05
        match s.split_once('e') {
            Some((m, e)) => {
                let (sign, digits) = e.strip_prefix('-').map_or(("+", e), |d| ("-", d));
                format!("{m}e{sign}{digits:0>2}")
            }
            None => s,
        }
    } else {
        format!("{x}")
    }
}

/// `'%g' % x`: six significant digits, trailing zeros dropped
pub fn g(x: f64) -> String {
    if x == 0.0 {
        return "0".into();
    }
    let sci = format!("{:.5e}", x);
    let (mantissa, exp) = sci.split_once('e').expect("scientific");
    let exp: i32 = exp.parse().expect("exponent");
    if !(-4..6).contains(&exp) {
        let m = mantissa.trim_end_matches('0').trim_end_matches('.');
        let sign = if exp < 0 { '-' } else { '+' };
        return format!("{m}e{sign}{:02}", exp.abs());
    }
    let decimals = (5 - exp).max(0) as usize;
    let s = format!("{x:.decimals$}");
    if s.contains('.') {
        s.trim_end_matches('0').trim_end_matches('.').to_string()
    } else {
        s
    }
}

/// `round(x, n)` as a float
pub fn round(x: f64, n: usize) -> f64 {
    format!("{x:.n$}").parse().expect("a number")
}

/// `int(round(x))`: halves go to the even neighbour
pub fn round_int(x: f64) -> i64 {
    x.round_ties_even() as i64
}

#[cfg(test)]
mod tests {
    use super::*;
    use serde_json::json;

    #[test]
    fn json_like_python() {
        let v = json!({"a": [1, 2.5, "ü\"x"], "b": {}, "c": []});
        assert_eq!(
            json(&v, None),
            r#"{"a": [1, 2.5, "ü\"x"], "b": {}, "c": []}"#
        );
        assert_eq!(
            json(&v, Some(1)),
            "{\n \"a\": [\n  1,\n  2.5,\n  \"ü\\\"x\"\n ],\n \"b\": {},\n \"c\": []\n}"
        );
    }

    #[test]
    fn ascii_like_python() {
        assert_eq!(
            json_ascii(&json!(["1–9", "ü"])),
            r#"["1\u20139", "\u00fc"]"#
        );
    }

    #[test]
    fn numbers_like_python() {
        assert_eq!(repr(1.0), "1.0");
        assert_eq!(repr(0.92), "0.92");
        assert_eq!(repr(1e-5), "1e-05");
        assert_eq!(g(1.0), "1");
        assert_eq!(g(0.2), "0.2");
        assert_eq!(g(112.0), "112");
        assert_eq!(g(103.04), "103.04");
        assert_eq!(g(1234567.0), "1.23457e+06");
        assert_eq!(g(0.00001), "1e-05");
        assert_eq!(round(110.4000001, 2), 110.4);
        assert_eq!(round_int(2.5), 2);
        assert_eq!(round_int(3.5), 4);
    }
}
