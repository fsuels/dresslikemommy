"""Layered seasonal hero assets for sections/hero-banner.liquid.

Per season:
  hero-<season>-sky.jpg         2400x1000  full-bleed sky (object-fit: cover, crops freely)
  hero-<season>-sky-mobile.jpg  1000x1100  mobile sky
  hero-<season>-art.webp        1520x1100  transparent arch cluster (object-fit: contain, never cropped)
No text is baked in; the theme renders localized copy in HTML.
"""
import random
from PIL import Image, ImageDraw, ImageFilter, ImageChops

SRC = 'full/'
OUT = 'out/'
S = 3  # supersampling for crisp arch edges


def lerp(a, b, t):
    t = min(1.0, max(0.0, t))
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))


def gradient(w, h, c0, c1, c2, wx, wy):
    """Three-stop gradient along direction (wx, wy) — cheap: rendered small, upscaled smoothly."""
    sw, sh = 120, 60
    small = Image.new('RGB', (sw, sh))
    px = small.load()
    for y in range(sh):
        for x in range(sw):
            t = wx * x / (sw - 1) + wy * y / (sh - 1)
            px[x, y] = lerp(c0, c1, t / 0.55) if t < 0.55 else lerp(c1, c2, (t - 0.55) / 0.45)
    return small.resize((w, h), Image.BICUBIC)


def soft_ellipse(size, box, color, alpha, blur):
    layer = Image.new('RGBA', size, color + (0,))
    ImageDraw.Draw(layer).ellipse(box, fill=color + (int(255 * alpha),))
    return layer.filter(ImageFilter.GaussianBlur(blur))


def arch_mask(w, h):
    m = Image.new('L', (w * S, h * S), 0)
    d = ImageDraw.Draw(m)
    r = w * S // 2
    d.ellipse([0, 0, w * S - 1, 2 * r], fill=255)
    d.rectangle([0, r, w * S - 1, h * S - 1], fill=255)
    return m.resize((w, h), Image.LANCZOS)


def arch_ring(w, h, stroke):
    ring = arch_mask(w, h)
    ring.paste(0, (stroke, stroke), arch_mask(w - 2 * stroke, h - 2 * stroke))
    return ring


def cover(img, w, h, fx=0.5, fy=0.4, zoom=1.0):
    iw, ih = img.size
    if zoom > 1:
        cw, ch = iw / zoom, ih / zoom
        img = img.crop((int((iw - cw) * fx), int((ih - ch) * fy), int((iw - cw) * fx + cw), int((ih - ch) * fy + ch)))
        iw, ih = img.size
    scale = max(w / iw, h / ih)
    nw, nh = int(iw * scale + 0.5), int(ih * scale + 0.5)
    img = img.resize((nw, nh), Image.LANCZOS)
    x, y = int((nw - w) * fx), int((nh - h) * fy)
    return img.crop((x, y, x + w, y + h))


def stars(size, n, density, color, rmin, rmax, seed, blur=0, avoid=(), y_bias=1.0):
    """density(x, y) -> 0..1 acceptance probability."""
    rnd = random.Random(seed)
    W, H = size
    layer = Image.new('RGBA', size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    placed = tries = 0
    while placed < n and tries < n * 80:
        tries += 1
        x, y = rnd.uniform(0, W), H * rnd.random() ** y_bias
        if rnd.random() > density(x, y):
            continue
        if any(a < x < c and b < y < e for a, b, c, e in avoid):
            continue
        r = rnd.uniform(rmin, rmax)
        d.ellipse([x - r, y - r, x + r, y + r], fill=color + (int(255 * rnd.uniform(0.25, 0.9)),))
        placed += 1
    return layer.filter(ImageFilter.GaussianBlur(blur)) if blur else layer


def grain(img, seed=5, strength=12):
    W, H = img.size
    random.seed(seed)
    noise = Image.effect_noise((W // 2, H // 2), 28).resize((W, H), Image.BICUBIC)
    img.alpha_composite(Image.merge('RGBA', (noise, noise, noise, Image.new('L', (W, H), strength))))


THEMES = {
    'halloween': {
        'grad': ((12, 8, 22), (28, 15, 40), (48, 22, 46)),
        'horizon': (255, 110, 40), 'horizon_a': 0.40, 'twilight': (132, 72, 196),
        'halo': (255, 158, 80), 'halo_a': 0.26,
        'frame': (248, 238, 224), 'hairline': (231, 180, 108, 210), 'accent': (241, 194, 124),
        'dots': (255, 238, 210), 'snow': False, 'moon': True,
        'photos': [('pumpkin-ghost-family-mat.src', 0.5, 0.25, 1.0),
                   ('boo-stripe-family-matchi.src', 0.5, 0.30, 1.0),
                   ('spooky-skeleton-family-m.src', 0.5, 0.25, 1.0)],
    },
    'winter': {
        'grad': ((6, 24, 24), (12, 42, 39), (22, 60, 54)),
        'horizon': (198, 232, 222), 'horizon_a': 0.16, 'twilight': (120, 196, 184),
        'halo': (255, 222, 170), 'halo_a': 0.16,
        'frame': (250, 246, 238), 'hairline': (228, 198, 138, 210), 'accent': (242, 216, 162),
        'dots': (255, 255, 255), 'snow': True, 'moon': False,
        'photos': [('cable-horse-3.src', 0.55, 0.20, 1.0),
                   ('family-matching-red-cabl.src', 0.5, 0.30, 1.0),
                   ('family-matching-cable-kn.src', 0.5, 0.25, 1.0)],
    },
}


# ---------- sky ----------
def sky(theme, W, H, mobile, out):
    t = THEMES[theme]
    wx, wy = (0.35, 0.65) if mobile else (0.62, 0.38)
    c = gradient(W, H, *t['grad'], wx, wy).convert('RGBA')
    if mobile:
        cx, base = W * 0.5, H * 0.94
        c.alpha_composite(soft_ellipse(c.size, [-W * 0.2, base - H * 0.2, W * 1.2, base + H * 0.3], t['horizon'], t['horizon_a'], W * 0.13))
        c.alpha_composite(soft_ellipse(c.size, [-W * 0.4, -H * 0.3, W * 0.6, H * 0.4], t['twilight'], 0.12, W * 0.2))
        dens = lambda x, y: 1.0
        clear_x = 0
    else:
        cx, base = W * 0.76, H * 0.94
        c.alpha_composite(soft_ellipse(c.size, [W * 0.42, base - H * 0.28, W * 1.12, base + H * 0.34], t['horizon'], t['horizon_a'], W * 0.07))
        c.alpha_composite(soft_ellipse(c.size, [W * 0.30, -H * 0.4, W * 0.78, H * 0.5], t['twilight'], 0.14, W * 0.1))
        clear_x = W * 0.54
        dens = lambda x, y: min(1.0, max(0.0, (x - clear_x * 0.5) / (clear_x * 0.5))) ** 1.6
    k = W / 2400 if not mobile else W / 1100
    if t['snow']:
        c.alpha_composite(stars(c.size, int(W * H / 3800), dens, t['dots'], 1.2 * k, 3.4 * k, 7, blur=0.9 * k, y_bias=1.15))
        c.alpha_composite(stars(c.size, int(W * H / 32000), dens, t['dots'], 4.5 * k, 8 * k, 11, blur=3.2 * k))
    else:
        c.alpha_composite(stars(c.size, int(W * H / 6500), lambda x, y: dens(x, y) * (1 - 0.7 * y / H), t['dots'], 0.9 * k, 2.6 * k, 3, y_bias=1.5))
    grain(c)
    c.convert('RGB').save(out, 'JPEG', quality=82, optimize=True, progressive=True)


# ---------- art ----------
AW, AH = 1520, 1100
ARCHES = [(150, 330, 350, 660), (530, 90, 460, 900), (1020, 330, 350, 660)]  # left, center, right (x, y, w, h)
MOON = (1300, 175, 50)
SPARKS = [(95, 285, 16), (455, 140, 10), (1455, 300, 11), (1100, 1045, 8), (70, 900, 7)]


def edge_feather(size, margin):
    """Alpha multiplier that is 1 inside and fades to 0 at the canvas edges."""
    W, H = size
    m = Image.new('L', size, 0)
    ImageDraw.Draw(m).rectangle([margin, margin, W - margin, H - margin], fill=255)
    return m.filter(ImageFilter.GaussianBlur(margin / 2.2))


def sparkle(layer, cx, cy, r, color):
    layer.alpha_composite(soft_ellipse(layer.size, [cx - r * 1.4, cy - r * 1.4, cx + r * 1.4, cy + r * 1.4], color, 0.32, r))
    s = Image.new('RGBA', layer.size, (0, 0, 0, 0))
    q = r * 0.16
    ImageDraw.Draw(s).polygon([(cx, cy - r), (cx + q, cy - q), (cx + r, cy), (cx + q, cy + q), (cx, cy + r), (cx - q, cy + q), (cx - r, cy), (cx - q, cy - q)], fill=color + (240,))
    layer.alpha_composite(s.filter(ImageFilter.GaussianBlur(0.5)))


def crescent(layer, cx, cy, r, color):
    layer.alpha_composite(soft_ellipse(layer.size, [cx - r * 2.3, cy - r * 2.3, cx + r * 2.3, cy + r * 2.3], color, 0.18, r))
    n = int(4 * r)
    m = Image.new('L', (n * S, n * S), 0)
    d = ImageDraw.Draw(m)
    o, R = 2 * r * S, r * S
    d.ellipse([o - R, o - R, o + R, o + R], fill=255)
    d.ellipse([o - R * 0.5, o - R * 1.2, o + R * 1.5, o + R * 0.8], fill=0)
    m = m.resize((n, n), Image.LANCZOS)
    layer.paste(Image.new('RGBA', (n, n), color + (255,)), (int(cx - 2 * r), int(cy - 2 * r)), m)


def art(theme, out_webp, preview_bg=None):
    t = THEMES[theme]
    fx = Image.new('RGBA', (AW, AH), (0, 0, 0, 0))  # glows that must fade before the canvas edge
    (lx, ly, lw, lh), (cx, cy, cw, ch), (rx, ry, rw, rh) = ARCHES
    fx.alpha_composite(soft_ellipse(fx.size, [lx - 40, cy + ch * 0.2, rx + rw + 40, cy + ch + 40], t['halo'], t['halo_a'], 110))
    if t['moon']:
        crescent(fx, *MOON, (252, 236, 204))
    for s in SPARKS:
        sparkle(fx, *s, t['accent'])
    a = fx.split()[3]
    fx.putalpha(ImageChops.multiply(a, edge_feather(fx.size, 60)))
    layer = fx
    for i in (0, 2, 1):
        x, y, w, h = ARCHES[i]
        border = max(8, round(w / 46))
        # contact shadow
        sh = Image.new('RGBA', layer.size, (0, 0, 0, 0))
        sm = arch_mask(w + 2 * border, h + 2 * border)
        sh.paste(Image.new('RGBA', sm.size, (5, 3, 9, 175)), (x - border, y - border + round(h / 32)), sm)
        sh = sh.filter(ImageFilter.GaussianBlur(round(w / 11)))
        layer.alpha_composite(sh)
        if i == 1:
            gap = round(w / 23)
            ow, oh = w + 2 * (border + gap), h + 2 * (border + gap)
            hl = Image.new('RGBA', layer.size, (0, 0, 0, 0))
            hl.paste(Image.new('RGBA', (ow, oh), t['hairline']), (x - border - gap, y - border - gap), arch_ring(ow, oh, 3))
            # hairline stops at the floor line instead of closing under the arch
            hl.paste((0, 0, 0, 0), (0, y + h + 2, AW, AH))
            layer.alpha_composite(hl)
        fm = arch_mask(w + 2 * border, h + 2 * border)
        layer.paste(Image.new('RGBA', fm.size, t['frame'] + (255,)), (x - border, y - border), fm)
        src, pfx, pfy, zoom = t['photos'][i]
        ph = cover(Image.open(SRC + src).convert('RGB'), w, h, pfx, pfy, zoom).convert('RGBA')
        # a whisper of inner vignette so photos sit "inside" the arch
        vig = Image.new('L', (w, h), 0)
        ImageDraw.Draw(vig).rectangle([0, 0, w, h], outline=60, width=max(6, w // 40))
        ph = Image.composite(Image.new('RGBA', (w, h), (20, 12, 20, 255)), ph, vig.filter(ImageFilter.GaussianBlur(w // 30)).point(lambda v: v // 3))
        layer.paste(ph, (x, y), arch_mask(w, h))
    for width in (1520, 1140, 760):
        img = layer if width == AW else layer.resize((width, round(AH * width / AW)), Image.LANCZOS)
        img.save(out_webp.replace('.webp', f'-{width}.webp'), 'WEBP', quality=82, method=6, alpha_quality=88)
    if preview_bg:
        bg = Image.open(preview_bg).convert('RGBA').resize((AW, AH))
        bg.alpha_composite(layer)
        bg.convert('RGB').save(out_webp.replace('.webp', '-preview.jpg'), quality=85)


for theme in THEMES:
    sky(theme, 2400, 1000, False, f'{OUT}hero-{theme}-sky.jpg')
    sky(theme, 1000, 1100, True, f'{OUT}hero-{theme}-sky-mobile.jpg')
    art(theme, f'{OUT}hero-{theme}-art.webp')
print('ok')
