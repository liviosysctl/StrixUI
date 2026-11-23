//! The design system as files: tokens, fonts, plates, the component bundle with its previews and
//! READMEs, the docs, and a local preview under build/preview/.

use crate::{Src, gods::Gods, py, read, read_json, tokens, write};
use regex::Regex;
use serde_json::{Map, Value, json};
use std::fs;
use std::path::Path;

/// One component or screen: its card and the files of src/components/<name>/
pub struct Card {
    pub name: String,
    pub screen: bool,
    pub group: String,
    pub height: i64,
    pub width: Option<i64>,
    pub html: String,
    pub doc: String,
    pub css: String,
    pub js: String,
}

pub fn cards(src: &Src, fills: &[(&str, String)]) -> Vec<Card> {
    let index = read_json(&src.root.join("components/index.json"));
    index
        .as_array()
        .expect("index")
        .iter()
        .map(|e| {
            let name = e["name"].as_str().expect("name").to_string();
            let dir = src.root.join("components").join(&name);
            let opt = |f: &str| fs::read_to_string(dir.join(f)).unwrap_or_default();
            let mut js = opt("script.js");
            for (key, value) in fills {
                js = js.replace(key, value);
            }
            Card {
                screen: e["kind"] == "screen",
                group: e["group"].as_str().expect("group").into(),
                height: e["height"].as_i64().expect("height"),
                width: e.get("width").and_then(Value::as_i64),
                html: read(&dir.join("preview.html")),
                doc: read(&dir.join("README.md")),
                css: opt("style.css"),
                js,
                name,
            }
        })
        .collect()
}

/// The star-chart drawing: a few fine cream arcs, one graduated circle, a meridian, one flat disc
pub fn star_chart(inline: bool, palette: &tokens::Palette, stars: &Value) -> String {
    let (w, h) = (2560, 1440);
    let line = if inline {
        "var(--line)".into()
    } else {
        palette.c("line")
    };
    let acc = if inline {
        "var(--accent)".into()
    } else {
        palette.c("accent")
    };
    let bg = if inline {
        "var(--background)".into()
    } else {
        palette.c("background")
    };
    let st = |col: &str, extra: &str| format!("style=\"stroke:{col};fill:none;{extra}\"");
    let (cx, cy) = (1560.0_f64, 1010.0_f64);
    let mut p = vec![
        format!(
            "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 {w} {h}\" preserveAspectRatio=\"xMidYMid slice\">"
        ),
        format!("<rect width=\"{w}\" height=\"{h}\" style=\"fill:{bg}\"/>"),
    ];
    let (dx, dy, dr) = (1560_i64, 660_i64, 250_i64);
    p.push(format!(
        "<circle cx=\"{dx}\" cy=\"{dy}\" r=\"{dr}\" style=\"fill:{acc}\"/>"
    ));
    for (r, o, wd) in [
        (430, "0.55", "1.5"),
        (640, "0.5", "1.5"),
        (900, "0.42", "1.5"),
        (1210, "0.34", "1.5"),
        (1560, "0.26", "1.5"),
    ] {
        p.push(format!(
            "<circle cx=\"{cx}\" cy=\"{cy}\" r=\"{r}\" {}/>",
            st(&line, &format!("stroke-width:{wd};opacity:{o}"))
        ));
    }
    let (r1, r2) = (640.0_f64, 664.0_f64);
    p.push(format!(
        "<circle cx=\"{cx}\" cy=\"{cy}\" r=\"{r2}\" {}/>",
        st(&line, "stroke-width:1.5;opacity:0.5")
    ));
    let mut ticks = String::new();
    for i in 0..180 {
        let a = f64::from(i * 2).to_radians();
        let ra = r1 - if i % 5 == 0 { 16.0 } else { 0.0 };
        ticks.push_str(&format!(
            "M{:.1} {:.1}L{:.1} {:.1}",
            cx + ra * a.cos(),
            cy + ra * a.sin(),
            cx + r2 * a.cos(),
            cy + r2 * a.sin()
        ));
    }
    p.push(format!(
        "<path d=\"{ticks}\" {}/>",
        st(&line, "stroke-width:1.5;opacity:0.4")
    ));
    p.push(format!(
        "<ellipse cx=\"{cx}\" cy=\"{cy}\" rx=\"1210\" ry=\"360\" transform=\"rotate(-23.4 {cx} {cy})\" {}/>",
        st(&line, "stroke-width:1.5;opacity:0.5")
    ));
    p.push(format!(
        "<path d=\"M{cx} -40L{cx} {}\" {}/>",
        h + 40,
        st(&line, "stroke-width:1.5;opacity:0.4")
    ));
    p.push(format!(
        "<path d=\"M-40 {cy}L{} {cy}\" {}/>",
        w + 40,
        st(&line, "stroke-width:1.5;opacity:0.3")
    ));
    let mut path = String::new();
    for s in stars.as_array().expect("stars") {
        let n = |i: usize| s[i].as_i64().expect("int");
        let (x, y, size) = (n(0), n(1), n(2));
        if (x - dx).pow(2) + (y - dy).pow(2) < (dr + 60).pow(2) {
            continue;
        }
        path.push_str(&format!(
            "M{} {y}h{}M{x} {}v{}",
            x - size,
            2 * size,
            y - size,
            2 * size
        ));
    }
    p.push(format!(
        "<path d=\"{path}\" {}/>",
        st(&line, "stroke-width:1.5;opacity:0.75")
    ));
    p.push("</svg>".into());
    p.concat()
}

/// The Lucide symbols in use: name to the inner markup of its SVG
pub fn icons(src: &Src, names: &Value) -> Vec<(String, String)> {
    let comment = Regex::new(r"(?s)<!--.*?-->").expect("regex");
    let inner = Regex::new(r"(?s)<svg[^>]*>(.*)</svg>").expect("regex");
    let space = Regex::new(r"\s+").expect("regex");
    names
        .as_array()
        .expect("icons")
        .iter()
        .map(|n| {
            let n = n.as_str().expect("name");
            let text = read(&src.root.join("icons").join(format!("{n}.svg")));
            let text = comment.replace_all(&text, "");
            let body = inner.captures(&text).expect("an svg")[1].to_string();
            (
                n.to_string(),
                space.replace_all(&body, " ").trim().to_string(),
            )
        })
        .collect()
}

pub struct Build<'a> {
    pub src: &'a Src,
    pub out: &'a Path,
    pub artifact: bool,
}

pub fn build(b: &Build, gods: &Gods, palette: &tokens::Palette) {
    let src = b.src;
    let out = b.out;
    if out.exists() {
        fs::remove_dir_all(out).expect("remove the old output");
    }
    let design = read_json(&src.root.join("design/tokens.json"));
    let meta = read_json(&src.root.join("design/build.json"));
    let plates = read_json(&src.root.join("design/plates.json"));
    let hotkeys = read_json(&src.root.join("design/hotkeys.json"));
    let title = meta["title"].as_str().expect("title");
    let blobs = meta["blobs"].as_object().expect("blobs");

    let t = tokens::tokens(&design, palette, gods);
    write(&out.join("tokens.json"), &(py::json(&t, Some(1)) + "\n"));
    let fonts = out.join("fonts");
    for f in meta["fonts"].as_array().expect("fonts") {
        copy(
            &src.root.join("fonts").join(f.as_str().expect("font")),
            &fonts.join(f.as_str().expect("font")),
        );
    }
    // wallpapers: in the artifact they are uploads named by the index, in the repository plain files
    let walls: Vec<(String, String)> = blobs
        .iter()
        .map(|(bid, f)| {
            (
                f.as_str().expect("file").to_string(),
                format!("/_blob/{bid}"),
            )
        })
        .collect();
    if !b.artifact {
        for f in sorted(&src.root.join("fonts")) {
            if f.starts_with("LICENSE") {
                copy(&src.root.join("fonts").join(&f), &fonts.join(&f));
            }
        }
        let wd = out.join("assets/Wallpapers");
        for (f, _) in &walls {
            copy(&src.root.join("wallpapers").join(f), &wd.join(f));
        }
        for g in &gods.gods {
            let f = format!("{}-light.jpg", g.id);
            copy(&src.root.join("wallpapers").join(&f), &wd.join(&f));
        }
        write(
            &wd.join("star-chart.svg"),
            &star_chart(false, palette, &meta["stars"]),
        );
        // the owl, for documents, posters and pages outside the system
        for f in sorted(&src.root.join("logo")) {
            copy(
                &src.root.join("logo").join(&f),
                &out.join("assets/Logo").join(&f),
            );
        }
        // one owl per god, the drawing and the reduced one for small sizes: the eyes in the accent of the theme
        let red = crate::gods::get(&gods.colours(&gods.default), "accent").to_string();
        for stem in ["strix-owl", "strix-owl-small"] {
            let owl = read(&src.root.join("logo").join(format!("{stem}.svg")));
            for g in &gods.gods {
                let accent = crate::gods::get(&gods.colours(&g.id), "accent").to_string();
                write(
                    &out.join("assets/Logo").join(format!("{stem}-{}.svg", g.id)),
                    &owl.replace(&red, &accent),
                );
            }
        }
    }
    let fix = |html: &str| {
        let mut html = html.to_string();
        for (f, url) in &walls {
            let to = if b.artifact {
                url.clone()
            } else {
                format!("../../assets/Wallpapers/{f}")
            };
            html = html.replace(url.as_str(), &to);
        }
        html
    };

    // the values the previews take from the themes: the picker's plates, the lock screen's gods, the hotkeys
    let url = |gid: &str| {
        walls
            .iter()
            .find(|(f, _)| *f == format!("{gid}.jpg"))
            .map(|(_, u)| u.clone())
            .expect("a plate")
    };
    let plate = |gid: &str| {
        plates[gid]["caption"]
            .as_str()
            .expect("caption")
            .to_string()
    };
    let picker: Vec<Value> = gods
        .gods
        .iter()
        .map(|g| {
            json!([
                g.id,
                url(&g.id),
                g.name,
                "dark",
                plate(&g.id),
                crate::gods::get(&gods.colours(&g.id), "accent")
            ])
        })
        .collect();
    let lock: Vec<Value> = gods
        .gods
        .iter()
        .map(|g| json!([g.id, url(&g.id), plate(&g.id)]))
        .collect();
    let hk: Vec<Value> = hotkeys
        .as_array()
        .expect("hotkeys")
        .iter()
        .enumerate()
        .map(|(i, h)| json!({"g": h["group"], "t": h["action"], "k": h["keys"], "w": h["target"], "id": i}))
        .collect();
    let fills = [
        ("{{THEMES}}", py::json_ascii(&Value::Array(picker))),
        ("{{LOCK_GODS}}", py::json_ascii(&Value::Array(lock))),
        ("{{HOTKEYS}}", py::json_ascii(&Value::Array(hk))),
    ];
    let all = cards(src, &fills);

    // bundle
    let names: Vec<Value> = all
        .iter()
        .filter(|c| !c.screen)
        .map(|c| json!({"name": c.name}))
        .collect();
    let header = format!(
        "/* @ds-bundle: {} */\n",
        py::json_ascii(&json!({"format": 4, "namespace": meta["namespace"], "components": names}))
    );
    let icon_list = icons(src, &meta["icons"]);
    let mut icon_map = Map::new();
    for (n, s) in &icon_list {
        icon_map.insert(n.clone(), Value::String(s.clone()));
    }
    let bundle_gods: Vec<Value> = gods
        .gods
        .iter()
        .map(|g| {
            let file = format!("{}.jpg", g.id);
            let wall = if b.artifact { url(&g.id) } else { format!("../assets/Wallpapers/{file}") };
            json!({"id": g.id, "name": g.name, "wall": wall, "plate": plate(&g.id), "disc": plates[&g.id]["disc"]})
        })
        .collect();
    let js = read(&src.root.join("bundle.js"))
        .replace("__ICONS__", &py::json(&Value::Object(icon_map), None))
        .replace(
            "__WALL__",
            &py::json_ascii(&Value::String(star_chart(true, palette, &meta["stars"]))),
        )
        .replace("__GODS__", &py::json(&Value::Array(bundle_gods), None));
    assert!(!js.contains("</script") && !js.contains("<!--"));
    write(&out.join("components/bundle.js"), &(header + &js));
    write(
        &out.join("components/bundle.css"),
        &read(&src.root.join("bundle.css")),
    );
    write(
        &out.join("components/index.d.ts"),
        &read(&src.root.join("components/index.d.ts")),
    );

    let usage = read_json(&src.root.join("docs/usage.json"));
    for c in &all {
        let mut attrs = format!("group=\"{}\" height={}", c.group, c.height);
        if let Some(w) = c.width {
            attrs.push_str(&format!(" width={w}"));
        }
        let style = if c.css.is_empty() {
            String::new()
        } else {
            format!("<style>\n{}\n</style>", c.css.trim())
        };
        let html = format!(
            "<!-- @dsCard {attrs} -->\n<!doctype html>\n<html lang=\"en\">\n<head><meta charset=\"utf-8\"><title>{} — preview</title>{style}</head>\n<body>\n{}\n<script>\nKit.hydrate(document);\n{}\n</script>\n</body>\n</html>\n",
            c.name,
            c.html.trim(),
            c.js.trim()
        );
        assert!(html.len() < 256_000);
        write(
            &out.join(format!("components/{}/preview.html", c.name)),
            &fix(&html),
        );
        write(
            &out.join(format!("components/{}/README.md", c.name)),
            &format!(
                "# {}\n\n{}\n{}",
                c.name,
                c.doc.trim(),
                usage_section(&usage, &c.name, c.screen)
            ),
        );
    }
    write(
        &out.join("components/Cover/preview.html"),
        &read(&src.root.join("docs/cover.html")),
    );

    // the README with the gods' colours, the docs and the plates' list
    let mut rows = vec![
        "| God | `accent` | `background` | Colour |".to_string(),
        "| --- | --- | --- | --- |".to_string(),
    ];
    let (mut light, mut dark) = (Vec::new(), Vec::new());
    for g in &gods.gods {
        let tt = gods.colours(&g.id);
        rows.push(format!(
            "| {} | `{}` | `{}` | {} |",
            g.name,
            crate::gods::get(&tt, "accent"),
            crate::gods::get(&tt, "background"),
            g.description
        ));
        if crate::gods::get(&tt, "on-accent") != "#ffffff" {
            light.push(g.name.clone())
        } else {
            dark.push(g.name.clone())
        }
    }
    let both = |x: &[String]| {
        if x.len() > 1 {
            format!("{} and {}", x[..x.len() - 1].join(", "), x[x.len() - 1])
        } else {
            x[0].clone()
        }
    };
    let readme = read(&src.root.join("docs/README.md"))
        .replace("{{GODS_TABLE}}", &rows.join("\n"))
        .replace("{{LIGHT}}", &both(&light))
        .replace("{{DARK}}", &both(&dark));
    write(&out.join("README.md"), &readme);
    for f in ["motion.md", "surfaces.md"] {
        write(&out.join(f), &read(&src.root.join("docs").join(f)));
    }
    let mut list = Vec::new();
    for g in &gods.gods {
        let tt = gods.colours(&g.id);
        let role = if g.id == "saturnus" {
            " The default desktop."
        } else {
            ""
        };
        let credit = plates[&g.id]["credit"].as_str().expect("credit");
        list.push(format!(
            "- `{}.jpg` — {}: accent `{}` on `{}`.{} {}.",
            g.id,
            g.name,
            crate::gods::get(&tt, "accent"),
            crate::gods::get(&tt, "background"),
            role,
            credit.trim_end_matches('.')
        ));
    }
    let walls_md = read(&src.root.join("docs/wallpapers.md"))
        .replace("{{PLATES}}\n", &(list.join("\n") + "\n"));
    write(&out.join("assets/Wallpapers/README.md"), &walls_md);

    let components = all.iter().filter(|c| !c.screen).count();
    if b.artifact {
        write_index(src, out, title);
    } else {
        write(&out.join("tokens.css"), &tokens::css(&t, title));
        write_preview(src, out, &all);
        let plates_by_god: Vec<(String, String)> = gods
            .gods
            .iter()
            .map(|g| (g.id.clone(), plate(&g.id)))
            .collect();
        crate::targets::write_all(src, out, &t, gods, &plates_by_god, &hotkeys, &icon_list);
    }
    println!(
        "{}: {components} components, {} screens",
        out.strip_prefix(std::env::current_dir().unwrap_or_default())
            .unwrap_or(out)
            .display(),
        all.len() - components
    );
}

fn usage_section(usage: &Value, name: &str, screen: bool) -> String {
    if screen {
        return usage["screens"]
            .get(name)
            .and_then(Value::as_str)
            .map(|t| format!("\n## In Quickshell\n\n{t}\n"))
            .unwrap_or_default();
    }
    let Some(entry) = usage["qml"].get(name) else {
        return String::new();
    };
    let types: Vec<String> = entry[0]
        .as_str()
        .expect("types")
        .split(',')
        .map(|t| format!("`{}`", t.trim()))
        .collect();
    format!(
        "\n## In Quickshell (Linux shell and apps)\n\n`import Strix`, then {}.\n\n```qml\n{}\n```\n\n## In HTML (the previews)\n\n{}\n",
        types.join(", "),
        entry[1].as_str().expect("example"),
        usage["tauri"].as_str().expect("tauri")
    )
}

fn write_index(src: &Src, out: &Path, title: &str) {
    let a = read_json(&src.tools.join("artifact.json"));
    let mut files = Map::new();
    let mut order = Vec::new();
    for (f, rec) in a["wallpapers"].as_object().expect("wallpapers") {
        files.insert(
            f.clone(),
            json!({"name": f, "blob": rec["blob"], "size": rec["size"], "type": rec["type"]}),
        );
        order.push(Value::String(f.clone()));
    }
    let now = std::process::Command::new("date")
        .args(["-u", "+%Y-%m-%dT%H:%M:%SZ"])
        .output()
        .map(|o| String::from_utf8_lossy(&o.stdout).trim().to_string())
        .unwrap_or_default();
    let idx = json!({
        "v": 3, "layout": "files", "createdOnFiles": {"v": 1, "at": a["created"]}, "title": title,
        "namespace": "Kit", "libraries": [], "sections": {}, "groups": ["Wallpapers"],
        "assetGroups": {"Wallpapers": {"name": "Wallpapers", "tile": "l", "order": order, "files": files}},
        "blobs": {}, "docs": {"sections": []},
        "lastChange": {"by": "Livio", "at": now, "via": "StrixUI repository", "note": "Built from the StrixUI repository."}
    });
    write(
        &out.join("design-system.json"),
        &(py::json(&idx, Some(1)) + "\n"),
    );
}

/// A local copy of what the artifact shows: one page per preview with the tokens, stylesheet and script loaded
fn write_preview(src: &Src, out: &Path, all: &[Card]) {
    let preview = src.repo.join("build/preview");
    if preview.exists() {
        fs::remove_dir_all(&preview).expect("remove the old preview");
    }
    fs::create_dir_all(&preview).expect("build/preview");
    let rel = "../../design-system";
    let head = format!(
        "<link rel=\"stylesheet\" href=\"{rel}/tokens.css\"><link rel=\"stylesheet\" href=\"{rel}/components/bundle.css\"><script src=\"{rel}/components/bundle.js\"></script>"
    );
    let mut links = String::new();
    let mut pages: Vec<(&str, &str)> = vec![("Cover", "Overview")];
    pages.extend(all.iter().map(|c| (c.name.as_str(), c.group.as_str())));
    for (name, group) in pages {
        let page = read(&out.join(format!("components/{name}/preview.html")))
            .replace("../../assets/", &format!("{rel}/assets/"))
            .replacen("<head>", &format!("<head>{head}"), 1)
            .replace(
                "<html lang=\"en\">",
                "<html lang=\"en\" data-theme=\"saturnus\">",
            );
        write(&preview.join(format!("{name}.html")), &page);
        links.push_str(&format!(
            "<li><a href=\"{name}.html\">{name}</a> <small>{group}</small></li>"
        ));
    }
    write(
        &preview.join("index.html"),
        &format!(
            "<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\"><title>Strix previews</title><style>body{{background:#0b0a09;color:#ece6da;font:13px/1.8 monospace;padding:24px}}a{{color:#f2556a}}small{{color:#77726a}}</style></head><body><h1>Strix previews</h1><ul>{links}</ul></body></html>\n"
        ),
    );
}

fn copy(from: &Path, to: &Path) {
    if let Some(dir) = to.parent() {
        fs::create_dir_all(dir).expect("a folder");
    }
    fs::copy(from, to).unwrap_or_else(|e| panic!("cannot copy {}: {e}", from.display()));
}

pub fn sorted(dir: &Path) -> Vec<String> {
    let mut names: Vec<String> = fs::read_dir(dir)
        .unwrap_or_else(|e| panic!("cannot read {}: {e}", dir.display()))
        .flatten()
        .map(|e| e.file_name().to_string_lossy().into_owned())
        .collect();
    names.sort();
    names
}
