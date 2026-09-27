#!/usr/bin/env python3
"""Side-by-side review sheet: vendor reference + IMAGE 1/3/5/6 for one handle."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw
ROOT = Path("/Users/fsuels/Projects/dresslikemommy")
handle, out = sys.argv[1], sys.argv[2]
d = ROOT / "uploads" / handle / "ai"
files = [("vendor ref", d / "ref1.jpg")] + [(f"image{n}", d / f"image{n}.png") for n in (1, 3, 5, 6)]
H = 900
tiles = []
for label, p in files:
    im = Image.open(p).convert("RGB"); im.thumbnail((H, H)); tiles.append((label, im))
W = sum(t.width for _, t in tiles) + 10 * len(tiles)
sheet = Image.new("RGB", (W, H + 30), "white"); dr = ImageDraw.Draw(sheet); x = 0
for label, im in tiles:
    sheet.paste(im, (x, 30)); dr.text((x + 5, 8), f"{label} {Image.open(dict(files)[label]).size}", fill="black"); x += im.width + 10
sheet.save(out, quality=88)
