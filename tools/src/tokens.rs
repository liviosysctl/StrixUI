//! tokens.json, the one source of every value, and tokens.css made from it.

use crate::gods::{self, Gods};
use serde_json::{Map, Value, json};

pub struct Palette {
    pub colors: Map<String, Value>,
    pub terminal: Map<String, Value>,
}

impl Palette {
    pub fn load(data: &Value) -> Palette {
        Palette {
            colors: data["colors"].as_object().expect("colors").clone(),
            terminal: data["terminal"].as_object().expect("terminal").clone(),
        }
    }
    pub fn c(&self, name: &str) -> String {
        self.colors[name]
            .as_str()
            .unwrap_or_else(|| panic!("colour {name}"))
            .to_string()
    }
    pub fn t(&self, name: &str) -> String {
        self.terminal[name]
            .as_str()
            .unwrap_or_else(|| panic!("terminal {name}"))
            .to_string()
    }
}

pub const ANSI: [&str; 8] = [
    "black", "red", "green", "yellow", "blue", "magenta", "cyan", "white",
];

/// The finished tokens.json: static data from src/design/tokens.json, colours per god
pub fn tokens(design: &Value, palette: &Palette, gods: &Gods) -> Value {
    let colours: Vec<(String, gods::Tokens)> = gods
        .gods
        .iter()
        .map(|g| (g.id.clone(), gods.colours(&g.id)))
        .collect();
    let first = &gods.gods[0].id;
    let border_active = gods::get(&colours[0].1, "border-active").to_string();
    let c = |name: &str| {
        if name == "border-active" {
            border_active.clone()
        } else {
            palette.c(name)
        }
    };
    let per_god = |token: &str, base: String| -> Value {
        let mut v = Map::new();
        v.insert(first.clone(), Value::String(base.clone()));
        for (gid, t) in &colours[1..] {
            if let Some((_, value)) = t.iter().find(|(k, _)| k == token)
                && *value != base
            {
                v.insert(gid.clone(), Value::String(value.clone()));
            }
        }
        Value::Object(v)
    };
    let meta = &design["color"];
    let mut colour_tokens = Vec::new();
    for n in meta["order"].as_array().expect("order") {
        let n = n.as_str().expect("name");
        colour_tokens
            .push(json!({"name": n, "value": per_god(n, c(n)), "usage": meta["usage"][n]}));
    }
    let mut term = vec!["background", "foreground", "cursor", "selection"];
    let bright: Vec<String> = ANSI.iter().map(|a| format!("bright-{a}")).collect();
    term.extend(ANSI);
    term.extend(bright.iter().map(String::as_str));
    for k in term {
        let value = if matches!(k, "background" | "cursor" | "selection") {
            per_god(k, palette.t(k))
        } else {
            json!({ first.clone(): palette.t(k) })
        };
        let usage = meta["term_usage"]
            .get(k)
            .and_then(Value::as_str)
            .map(str::to_string)
            .unwrap_or_else(|| format!("ANSI {}.", k.replace('-', " ")));
        colour_tokens.push(json!({"name": format!("term-{k}"), "value": value, "usage": usage}));
    }
    let themes: Vec<Value> = gods
        .gods
        .iter()
        .map(|g| json!({"id": g.id, "name": g.name}))
        .collect();

    let mut out = Map::new();
    out.insert("name".into(), design["name"].clone());
    out.insert("version".into(), design["version"].clone());
    out.insert(
        "color".into(),
        json!({"themes": themes, "tokens": colour_tokens}),
    );
    for key in [
        "type", "spacing", "radius", "shadow", "line", "size", "duration", "easing", "opacity",
    ] {
        let mut v = design[key].clone();
        if key == "shadow" {
            for s in v["tokens"].as_array_mut().expect("tokens") {
                if let Some(text) = s["value"].as_str() {
                    let filled = text
                        .replace("{background}", &palette.c("background"))
                        .replace("{focus}", &palette.c("focus"));
                    s["value"] = Value::String(filled);
                }
            }
        }
        out.insert(key.into(), v);
    }
    Value::Object(out)
}

pub fn css(t: &Value, title: &str) -> String {
    let themes = t["color"]["themes"].as_array().expect("themes");
    let first = themes[0]["id"].as_str().expect("id");
    let colours = t["color"]["tokens"].as_array().expect("tokens");
    let s = |v: &Value| {
        v.as_str()
            .map(str::to_string)
            .unwrap_or_else(|| v.to_string())
    };
    let mut out = vec![
        format!("/* {title} — generated from tokens.json */"),
        format!(":root, [data-theme=\"{first}\"] {{"),
    ];
    for c in colours {
        out.push(format!("  --{}: {};", s(&c["name"]), s(&c["value"][first])));
    }
    for sh in t["shadow"]["tokens"].as_array().expect("shadow") {
        out.push(format!("  --{}: {};", s(&sh["name"]), s(&sh["value"])));
    }
    out.push("}".into());
    for th in &themes[1..] {
        let id = th["id"].as_str().expect("id");
        out.push(format!("[data-theme=\"{id}\"] {{"));
        for c in colours {
            if let Some(v) = c["value"].get(id) {
                out.push(format!("  --{}: {};", s(&c["name"]), s(v)));
            }
        }
        out.push("}".into());
    }
    out.push(":root {".into());
    for fam in [
        "spacing", "radius", "line", "size", "duration", "easing", "opacity",
    ] {
        for x in t[fam]["tokens"].as_array().expect("tokens") {
            out.push(format!("  --{}: {};", s(&x["name"]), s(&x["value"])));
        }
    }
    for (k, v) in t["type"]["families"].as_object().expect("families") {
        out.push(format!("  --font-{k}: {};", s(v)));
    }
    out.push("}".into());
    for g in t["type"]["groups"].as_array().expect("groups") {
        for st in g["styles"].as_array().expect("styles") {
            out.push(format!(
                ".{} {{ font-family: var(--font-{}); font-size: {}; line-height: {}; font-weight: {};{}{} }}",
                s(&st["name"]),
                s(&g["family"]),
                s(&st["fontSize"]),
                num(&st["lineHeight"]),
                num(&st["fontWeight"]),
                st.get("fontStyle").map(|v| format!(" font-style: {};", s(v))).unwrap_or_default(),
                st.get("letterSpacing").map(|v| format!(" letter-spacing: {};", s(v))).unwrap_or_default(),
            ));
        }
    }
    for f in t["type"]["fonts"].as_array().expect("fonts") {
        out.push(format!(
            "@font-face {{ font-family: \"{}\"; src: url(\"{}\") format(\"woff2\"); font-weight: {}; font-style: {}; font-display: block; }}",
            s(&f["family"]),
            s(&f["file"]),
            s(&f["weight"]),
            s(&f["style"])
        ));
    }
    out.join("\n") + "\n"
}

/// A value as Python's '%s' writes it: strings bare, numbers as repr
pub fn num(v: &Value) -> String {
    match v {
        Value::String(s) => s.clone(),
        Value::Number(n) if n.is_f64() => crate::py::repr(n.as_f64().expect("f64")),
        other => other.to_string(),
    }
}
