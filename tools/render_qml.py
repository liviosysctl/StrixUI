#!/usr/bin/env python3
"""Renders the QML gallery (design-system/qml/gallery.qml) to PNG, once per theme, and fails on any QML error.

    python3 tools/render_qml.py                    every theme into build/renders/qml-<theme>.png
    python3 tools/render_qml.py janus mars         only these
    python3 tools/render_qml.py --tokens FILE      apply a tokens.json of the theme engine first (strix-theme show <theme>)

Needs PySide6 (pip install PySide6-Essentials). Effects need OpenGL: with no display it starts Xvfb when there is one.
"""
import argparse, json, os, shutil, subprocess, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QML = os.path.join(ROOT, 'design-system', 'qml')
OUT = os.path.join(ROOT, 'build', 'renders')
GODS = ['saturnus', 'janus', 'apollo', 'mars', 'vulcanus', 'neptunus', 'pluto', 'bacchus']


def ensure_display():
    if os.environ.get('DISPLAY') or os.environ.get('WAYLAND_DISPLAY'):
        return None
    xvfb = shutil.which('Xvfb')
    if not xvfb:
        os.environ['QT_QPA_PLATFORM'] = 'offscreen'
        print('no display and no Xvfb: software rendering, effects (shadows, blur) are missing', file=sys.stderr)
        return None
    proc = subprocess.Popen([xvfb, ':97', '-screen', '0', '1600x1200x24'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1)
    os.environ['DISPLAY'] = ':97'
    os.environ['QT_QPA_PLATFORM'] = 'xcb'
    return proc


def render(theme, tokens, out):
    from PySide6.QtCore import QUrl, QTimer, QMetaObject, Q_ARG, Qt
    from PySide6.QtGui import QGuiApplication
    from PySide6.QtQuick import QQuickView
    app = QGuiApplication.instance() or QGuiApplication([sys.argv[0]])
    view = QQuickView()
    view.setResizeMode(QQuickView.SizeViewToRootObject)
    view.engine().addImportPath(QML)
    errors = []
    view.engine().warnings.connect(lambda ws: errors.extend(w.toString() for w in ws))
    theme_obj = view.engine().singletonInstance('Strix', 'Theme')
    if tokens:
        QMetaObject.invokeMethod(theme_obj, 'apply', Q_ARG('QVariant', tokens))
    else:
        QMetaObject.invokeMethod(theme_obj, 'preview', Q_ARG('QVariant', theme))
    view.setSource(QUrl.fromLocalFile(os.path.join(QML, 'gallery.qml')))
    errors += [e.toString() for e in view.errors()]
    view.show()
    done = []
    def grab():
        view.grabWindow().save(out)
        done.append(True)
        app.quit()
    QTimer.singleShot(2500, grab)
    app.exec()
    view.close()
    return errors


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('themes', nargs='*')
    ap.add_argument('--tokens')
    args = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    xvfb = ensure_display()
    try:
        bad = 0
        if args.tokens:
            tokens = json.load(open(args.tokens))
            wt = os.path.join(tokens.get('dir', ''), 'wallpaper.toml')
            if os.path.isfile(wt):                       # what ThemeFile reads for a theme from a theme repository
                import tomllib
                tokens['plate'] = tomllib.load(open(wt, 'rb')).get('caption', '')
            jobs = [(tokens.get('theme', 'tokens'), tokens)]
        else:
            jobs = [(t, None) for t in (args.themes or GODS)]
        for theme, tokens in jobs:
            out = os.path.join(OUT, 'qml-%s%s.png' % (theme, '-tokens' if tokens else ''))
            errors = render(theme, tokens, out)
            for e in errors:
                print('  ' + e)
            bad += len(errors)
            print('%s %s' % ('FAIL' if errors else 'ok  ', os.path.relpath(out, ROOT)))
        sys.exit(1 if bad else 0)
    finally:
        if xvfb:
            xvfb.terminate()


if __name__ == '__main__':
    main()
