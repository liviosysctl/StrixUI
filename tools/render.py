#!/usr/bin/env python3
"""Renders every preview to PNG with a real headless Chromium.

    python3 tools/build.py && python3 tools/render.py              # all previews at scale 1 into build/renders/
    python3 tools/render.py LockScreen Desktop --scale 2           # some, at scale 2

Needs: playwright (pip install playwright, then playwright install chromium), or set CHROME to a Chrome binary.
"""
import argparse, asyncio, os, sys
from playwright.async_api import async_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import components

async def run(jobs, scale):
    os.makedirs(os.path.join(ROOT, 'build', 'renders'), exist_ok=True)
    async with async_playwright() as p:
        opts = {'args': ['--no-sandbox']}
        if os.environ.get('CHROME'):
            opts['executable_path'] = os.environ['CHROME']
        b = await p.chromium.launch(**opts)
        for name, w, h in jobs:
            pg = await b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=scale)
            errs = []
            pg.on('pageerror', lambda e: errs.append(str(e)))
            await pg.goto('file://' + os.path.join(ROOT, 'build', 'preview', name + '.html'))
            await pg.evaluate('document.fonts.ready')
            await pg.wait_for_timeout(900)
            out = os.path.join(ROOT, 'build', 'renders', '%s%s.png' % (name, '' if scale == 1 else '@%gx' % scale))
            await pg.screenshot(path=out)
            print(('ERROR ' + '; '.join(errs) + '  ') if errs else '', os.path.relpath(out, ROOT))
            await pg.close()
        await b.close()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('names', nargs='*')
    ap.add_argument('--scale', type=float, default=1)
    a = ap.parse_args()
    allc = {c['name']: c for c in components.COMPONENTS + components.SCREENS}
    allc['Cover'] = {'name': 'Cover', 'height': 288}
    names = a.names or list(allc)
    jobs = [(n, allc[n].get('width') or 960, allc[n]['height']) for n in names]
    asyncio.run(run(jobs, a.scale))

if __name__ == '__main__':
    main()
