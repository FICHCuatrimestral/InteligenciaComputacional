"""Renderiza los SVG a PNG con Chromium para poder revisarlos visualmente."""
import glob, os, sys, json
from playwright.sync_api import sync_playwright

files = sorted(glob.glob("/home/claude/work/figs/out/*.svg"))
if len(sys.argv) > 1:
    files = [f for f in files if any(k in f for k in sys.argv[1:])]

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1000, "height": 800}, device_scale_factor=2)
    for f in files:
        svg = open(f).read()
        html = (f'<html><body style="margin:0;background:#fcfcfb">'
                f'<div id="w" style="display:inline-block">{svg}</div></body></html>')
        pg.set_content(html)
        el = pg.query_selector("#w")
        el.screenshot(path=f.replace(".svg", ".png"))
        print("->", os.path.basename(f))
    b.close()
