from PIL import Image, ImageDraw, ImageFont, ImageStat
import json, re
rows = json.load(open('xmas_products.json'))
W, H, PH = 1000, 1500, 1170
CREAM, INK, RED, GREEN = (250, 246, 238), (34, 30, 28), (168, 30, 36), (31, 77, 52)
SERIF = '/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf'
SANS = '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'
SANSB = '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'
f = lambda p, s: ImageFont.truetype(p, s)

def kind(h):
    if 'onesie' in h: return 'Matching Family Christmas Onesies'
    if 'sweater' in h: return 'Matching Family Christmas Sweaters'
    return 'Matching Family Christmas Pajamas'

def name(t):
    return re.split(r'\s+Family Matching', t)[0].strip()

def is_flat(path):
    im = Image.open(path).convert('L').resize((90, 160))
    px = list(im.getdata())
    return sum(1 for p in px if p > 235) / len(px) > 0.45

def cover(im, w, h):
    r = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    left = (im.width - w) // 2
    top = int((im.height - h) * 0.03)  # keep heads in frame
    return im.crop((left, top, left + w, top + h))

def fit(draw, text, path, size, maxw):
    while size > 20:
        ft = f(path, size)
        if draw.textlength(text, font=ft) <= maxw: return ft
        size -= 2
    return f(path, size)

def pin(r, src, out, eyebrow):
    c = Image.new('RGB', (W, H), CREAM)
    c.paste(cover(Image.open(src).convert('RGB'), W, PH), (0, 0))
    d = ImageDraw.Draw(c)
    # eyebrow pill on photo
    ef = f(SANSB, 30); tw = d.textlength(eyebrow, font=ef)
    d.rounded_rectangle((40, 40, 40 + tw + 48, 100), 30, fill=RED)
    d.text((64, 70), eyebrow, font=ef, fill='white', anchor='lm')
    d.rectangle((0, PH, W, PH + 10), fill=GREEN)
    t = name(r['t']); tf = fit(d, t, SERIF, 70, W - 100)
    d.text((W // 2, PH + 75), t, font=tf, fill=INK, anchor='mm')
    sf = fit(d, kind(r['h']), SANS, 40, W - 100)
    d.text((W // 2, PH + 145), kind(r['h']), font=sf, fill=INK, anchor='mm')
    sizes = 'Baby, kids & adult sizes' if 'onesie' in r['h'] else 'Kids & adult sizes'
    line = f"From ${r['pmin']:.2f} per person  ·  {sizes}"
    lf = fit(d, line, SANSB, 32, W - 100)
    d.text((W // 2, PH + 210), line, font=lf, fill=RED, anchor='mm')
    d.text((W // 2, PH + 275), 'dresslikemommy.com', font=f(SANS, 30), fill=(90, 84, 78), anchor='mm')
    c.save(out, 'JPEG', quality=86, optimize=True)

made = []
for r in rows:
    srcs = [f"pins/src/{r['h']}_{i}.jpg" for i in range(3)]
    life = [s for s in srcs if not is_flat(s)] + [s for s in srcs if is_flat(s)]
    for n, (src, eb) in enumerate(zip(life[:2], ['NEW FOR CHRISTMAS 2026', 'MATCH THE WHOLE FAMILY'])):
        out = f"pins/out/dlm-{r['h']}-pin{n+1}.jpg"; pin(r, src, out, eb); made.append(out)
print(len(made))
