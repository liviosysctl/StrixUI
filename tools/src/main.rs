//! The tools of the Strix design system.
//!
//!     strixui build                  writes design-system/ and a local preview under build/preview/
//!     strixui build --artifact DIR   the same system as the Claude Design System artifact expects it
//!     strixui check                  contrast of every colour pair and of every god theme
//!     strixui wallpapers [god ...]   remakes the plates of the gods in src/wallpapers/
//!     strixui pack REPO [--check]    a theme repository from its source.toml
//!     strixui render [name ...] [--scale N]
//!                                    PNG of every preview into build/renders/ (headless Chromium)
//!     strixui render-qml [theme ...] [--tokens FILE]
//!                                    the QML gallery of every theme into build/renders/, fails on any QML error
//!
//! Every value comes from src/design/; nothing in design-system/ is edited by hand.

mod check;
mod colour;
mod gods;
mod pack;
mod py;
mod render;
mod site;
mod targets;
mod tokens;
mod wallpapers;

use serde_json::Value;
use std::fs;
use std::path::{Path, PathBuf};
use std::process::ExitCode;

/// Where the sources are: the repository, its src/ and tools/
pub struct Src {
    pub repo: PathBuf,
    pub root: PathBuf,
    pub tools: PathBuf,
}

pub fn read(path: &Path) -> String {
    fs::read_to_string(path).unwrap_or_else(|e| panic!("cannot read {}: {e}", path.display()))
}

pub fn read_json(path: &Path) -> Value {
    serde_json::from_str(&read(path))
        .unwrap_or_else(|e| panic!("{} is not JSON: {e}", path.display()))
}

pub fn write(path: &Path, text: &str) {
    if let Some(dir) = path.parent() {
        fs::create_dir_all(dir).unwrap_or_else(|e| panic!("cannot create {}: {e}", dir.display()));
    }
    fs::write(path, text).unwrap_or_else(|e| panic!("cannot write {}: {e}", path.display()));
}

/// The repository: STRIXUI, else the current folder when it is one, else the parent of tools/
fn repo() -> PathBuf {
    if let Some(dir) = std::env::var_os("STRIXUI") {
        return PathBuf::from(dir);
    }
    if let Ok(dir) = std::env::current_dir()
        && dir.join("src/design/gods.json").is_file()
    {
        return dir;
    }
    let manifest = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    manifest.parent().map(Path::to_path_buf).unwrap_or(manifest)
}

const USAGE: &str =
    "usage: strixui build [--artifact DIR] | check | wallpapers [god ...] | pack REPO [--check]
               | render [name ...] [--scale N] | render-qml [theme ...] [--tokens FILE]";

fn status(ok: bool) -> ExitCode {
    if ok {
        ExitCode::SUCCESS
    } else {
        ExitCode::FAILURE
    }
}

fn absolute(p: &str) -> PathBuf {
    std::path::absolute(p).unwrap_or_else(|e| panic!("{p}: {e}"))
}

/// The plain arguments and the value of one option
fn split_option(args: &[&str], option: &str) -> (Vec<String>, Option<String>) {
    let mut plain = Vec::new();
    let mut value = None;
    let mut it = args.iter();
    while let Some(a) = it.next() {
        if *a == option {
            value = Some(
                it.next()
                    .unwrap_or_else(|| panic!("{option} takes a value"))
                    .to_string(),
            );
        } else {
            plain.push(a.to_string());
        }
    }
    (plain, value)
}

fn main() -> ExitCode {
    let args: Vec<String> = std::env::args().skip(1).collect();
    let repo = repo();
    let src = Src {
        root: repo.join("src"),
        tools: repo.join("tools"),
        repo: repo.clone(),
    };
    let gods = gods::Gods::load(&read_json(&src.root.join("design/gods.json")));
    let palette = tokens::Palette::load(&read_json(&src.root.join("design/palette.json")));
    match args
        .iter()
        .map(String::as_str)
        .collect::<Vec<_>>()
        .as_slice()
    {
        ["build"] => {
            let out = repo.join("design-system");
            site::build(
                &site::Build {
                    src: &src,
                    out: &out,
                    artifact: false,
                },
                &gods,
                &palette,
            );
            ExitCode::SUCCESS
        }
        ["build", "--artifact", dir] => {
            let out = Path::new(dir).join("project");
            site::build(
                &site::Build {
                    src: &src,
                    out: &out,
                    artifact: true,
                },
                &gods,
                &palette,
            );
            ExitCode::SUCCESS
        }
        ["check"] => {
            let fails = check::palette(&palette) + check::themes(&gods);
            status(fails == 0)
        }
        ["wallpapers", names @ ..] => {
            let names: Vec<String> = names.iter().map(|s| s.to_string()).collect();
            wallpapers::gods(&src, &gods, &names);
            ExitCode::SUCCESS
        }
        ["pack", repo] => status(pack::build(&src, &gods, &absolute(repo), false)),
        ["pack", repo, "--check"] | ["pack", "--check", repo] => {
            status(pack::build(&src, &gods, &absolute(repo), true))
        }
        ["render", rest @ ..] => {
            let (names, scale) = split_option(rest, "--scale");
            let scale = scale
                .map(|s| s.parse().expect("--scale takes a number"))
                .unwrap_or(1.0);
            status(render::previews(&src, &names, scale))
        }
        ["render-qml", rest @ ..] => {
            let (themes, tokens) = split_option(rest, "--tokens");
            status(render::qml(
                &src,
                &gods,
                &themes,
                tokens.map(|t| absolute(&t)).as_deref(),
            ))
        }
        _ => {
            eprintln!("{}", USAGE);
            ExitCode::from(64)
        }
    }
}
