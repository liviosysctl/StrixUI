//! strixui render: every preview to PNG with a headless Chromium.
//! strixui render-qml: the QML gallery to PNG for every theme with Qt's qml tool; fails on any QML error.

use crate::{Src, read_json, write};
use serde_json::Value;
use std::path::{Path, PathBuf};
use std::process::{Command, Stdio};

fn which(names: &[&str]) -> Option<PathBuf> {
    let path = std::env::var_os("PATH")?;
    names.iter().find_map(|n| {
        std::env::split_paths(&path)
            .map(|d| d.join(n))
            .find(|p| p.is_file())
    })
}

fn tool(var: &str, names: &[&str]) -> PathBuf {
    std::env::var_os(var)
        .map(PathBuf::from)
        .or_else(|| which(names))
        .unwrap_or_else(|| panic!("no {} found: put it on the PATH or set {var}", names[0]))
}

fn rel(src: &Src, p: &Path) -> String {
    p.strip_prefix(&src.repo).unwrap_or(p).display().to_string()
}

/// The previews to render: name, width, height
fn jobs(src: &Src, names: &[String]) -> Vec<(String, u64, u64)> {
    let index = read_json(&src.root.join("components/index.json"));
    let mut all: Vec<(String, u64, u64)> = index
        .as_array()
        .expect("index.json is a list")
        .iter()
        .map(|c| {
            let name = c["name"].as_str().expect("name").to_string();
            (
                name,
                c.get("width").and_then(Value::as_u64).unwrap_or(960),
                c["height"].as_u64().expect("height"),
            )
        })
        .collect();
    all.push(("Cover".into(), 960, 288));
    if names.is_empty() {
        return all;
    }
    names
        .iter()
        .map(|n| {
            all.iter()
                .find(|(a, _, _)| a == n)
                .cloned()
                .unwrap_or_else(|| panic!("no preview {n}"))
        })
        .collect()
}

pub fn previews(src: &Src, names: &[String], scale: f64) -> bool {
    let chrome = tool(
        "CHROME",
        &[
            "chromium",
            "chromium-browser",
            "google-chrome",
            "google-chrome-stable",
        ],
    );
    let out_dir = src.repo.join("build/renders");
    std::fs::create_dir_all(&out_dir).expect("build/renders");
    let mut ok = true;
    for (name, w, h) in jobs(src, names) {
        let page = src.repo.join("build/preview").join(format!("{name}.html"));
        let suffix = if scale == 1.0 {
            String::new()
        } else {
            format!("@{}x", crate::py::g(scale))
        };
        let out = out_dir.join(format!("{name}{suffix}.png"));
        let run = Command::new(&chrome)
            .args([
                "--headless=new",
                "--no-sandbox",
                "--hide-scrollbars",
                "--disable-gpu",
                "--enable-logging=stderr",
                "--v=0",
            ])
            .arg(format!("--window-size={w},{h}"))
            .arg(format!("--force-device-scale-factor={scale}"))
            // time for the fonts and the first animations, as the old renderer waited 900 ms after fonts.ready
            .arg("--virtual-time-budget=2500")
            .arg(format!("--screenshot={}", out.display()))
            .arg(format!("file://{}", page.display()))
            .stdout(Stdio::null())
            .output()
            .expect("chromium runs");
        let log = String::from_utf8_lossy(&run.stderr);
        let errors: Vec<&str> = log.lines().filter(|l| l.contains("Uncaught")).collect();
        if !run.status.success() || !out.is_file() {
            ok = false;
            println!("ERROR chromium failed  {}", rel(src, &out));
        } else if errors.is_empty() {
            println!(" {}", rel(src, &out));
        } else {
            ok = false;
            println!("ERROR {}  {}", errors.join("; "), rel(src, &out));
        }
    }
    ok
}

const RUNNER: &str = r#"// Written by strixui render-qml: shows the gallery in one theme, saves it and quits.
import QtQuick
import QtQuick.Window
import Strix

Window {
    id: window
    visible: true
    width: gallery.item ? gallery.item.width : 1280
    height: gallery.item ? gallery.item.height : 1220
    Component.onCompleted: {
        @APPLY@
        gallery.source = @GALLERY@
    }
    Loader { id: gallery }
    Timer {
        interval: 2500
        running: true
        onTriggered: gallery.item.grabToImage(r => { r.saveToFile(@OUT@); Qt.quit() })
    }
}
"#;

fn json_str(s: &str) -> String {
    serde_json::to_string(s).expect("a string")
}

/// strixui render-qml [theme ...] [--tokens FILE]
pub fn qml(src: &Src, gods: &crate::gods::Gods, themes: &[String], tokens: Option<&Path>) -> bool {
    let qml = tool("QML", &["qml"]);
    let module = src.repo.join("design-system/qml");
    let out_dir = src.repo.join("build/renders");
    let jobs: Vec<(String, Option<Value>)> = match tokens {
        Some(file) => {
            let mut t = read_json(file);
            // what ThemeFile reads for a theme from a theme repository
            let caption = t
                .get("dir")
                .and_then(Value::as_str)
                .map(|d| Path::new(d).join("wallpaper.toml"))
                .filter(|p| p.is_file());
            if let Some(p) = caption {
                let w: toml::Value =
                    toml::from_str(&crate::read(&p)).expect("wallpaper.toml is not TOML");
                t["plate"] = Value::String(
                    w.get("caption")
                        .and_then(toml::Value::as_str)
                        .unwrap_or("")
                        .into(),
                );
            }
            vec![(
                t.get("theme")
                    .and_then(Value::as_str)
                    .unwrap_or("tokens")
                    .to_string(),
                Some(t),
            )]
        }
        None if themes.is_empty() => gods.gods.iter().map(|g| (g.id.clone(), None)).collect(),
        None => themes.iter().map(|t| (t.clone(), None)).collect(),
    };
    let mut bad = 0;
    for (theme, tok) in jobs {
        let out = out_dir.join(format!(
            "qml-{theme}{}.png",
            if tok.is_some() { "-tokens" } else { "" }
        ));
        let apply = match &tok {
            Some(t) => format!("Theme.apply({})", t),
            None => format!("Theme.preview({})", json_str(&theme)),
        };
        let runner = src.repo.join("build/render-qml.qml");
        let text = RUNNER
            .replace("@OUT@", &json_str(&out.display().to_string()))
            .replace(
                "@GALLERY@",
                &json_str(&format!("file://{}", module.join("gallery.qml").display())),
            )
            .replace("@APPLY@", &apply);
        write(&runner, &text);
        let _ = std::fs::remove_file(&out);
        let mut cmd = Command::new(&qml);
        cmd.arg("-I")
            .arg(&module)
            .arg(&runner)
            .stdout(Stdio::null());
        // Effects need OpenGL; with no display Qt draws in software and shadows and blur are missing
        if std::env::var_os("DISPLAY").is_none() && std::env::var_os("WAYLAND_DISPLAY").is_none() {
            cmd.env("QT_QPA_PLATFORM", "offscreen");
        }
        let run = cmd.output().expect("the qml tool runs");
        let errors: Vec<String> = String::from_utf8_lossy(&run.stderr)
            .lines()
            .filter(|l| {
                l.contains("file://")
                    || l.contains("qrc:")
                    || l.contains("Error")
                    || l.contains("is not a type")
            })
            .map(str::to_string)
            .collect();
        for e in &errors {
            println!("  {e}");
        }
        let failed = !errors.is_empty() || !out.is_file();
        bad += usize::from(failed);
        println!(
            "{} {}",
            if failed { "FAIL" } else { "ok  " },
            rel(src, &out)
        );
    }
    bad == 0
}
