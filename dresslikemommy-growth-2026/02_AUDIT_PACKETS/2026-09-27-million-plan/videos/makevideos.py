from PIL import Image, ImageDraw, ImageFont
import subprocess, json, imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
W, H, FPS = 1080, 1920, 30
SERIF = '/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf'
SANSB = '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'
SANS = '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'
RED, CREAM, INK = (168, 30, 36), (250, 246, 238), (34, 30, 28)
F = lambda p, s: ImageFont.truetype(p, s)

def base(path):
    im = Image.open(path).convert('RGB')
    r = max(W / im.width, H / im.height) * 1.12
    return im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)

def frame_of(big, t):  # t in [0,1] slow zoom-out
    s = 1.0 - 0.10 * t
    w, h = int(big.width * s), int(big.height * s)
    x, y = (big.width - w) // 2, int((big.height - h) * 0.0)
    return big.crop((x, y, x + w, y + h)).resize((W, H), Image.BILINEAR)

def wrap(d, text, font, maxw):
    words, lines, cur = text.split(), [], ''
    for w_ in words:
        t = (cur + ' ' + w_).strip()
        if d.textlength(t, font=font) <= maxw: cur = t
        else: lines.append(cur); cur = w_
    return lines + [cur]

def banner(img, text, y, size=64, fill=(255, 255, 255), bg=(0, 0, 0, 150)):
    ov = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov); f = F(SANSB, size)
    lines = wrap(d, text, f, W - 140); lh = size + 16; hgt = lh * len(lines) + 40
    d.rounded_rectangle((50, y, W - 50, y + hgt), 28, fill=bg)
    for i, l in enumerate(lines): d.text((W // 2, y + 20 + i * lh + lh // 2), l, font=f, fill=fill, anchor='mm')
    return Image.alpha_composite(img.convert('RGBA'), ov).convert('RGB')

def label(img, text):
    d = ImageDraw.Draw(img); f = F(SANSB, 110)
    d.ellipse((W - 230, 150, W - 60, 320), fill=RED); d.text((W - 145, 235), text, font=f, fill='white', anchor='mm')
    return img

def endcard(line1, line2):
    img = Image.new('RGB', (W, H), CREAM); d = ImageDraw.Draw(img)
    d.rectangle((0, 0, W, 24), fill=RED); d.rectangle((0, H - 24, W, H), fill=RED)
    y = 620
    for l in wrap(d, line1, F(SERIF, 96), W - 160): d.text((W // 2, y), l, font=F(SERIF, 96), fill=INK, anchor='mm'); y += 115
    y += 40
    for l in wrap(d, line2, F(SANS, 52), W - 180): d.text((W // 2, y), l, font=F(SANS, 52), fill=INK, anchor='mm'); y += 70
    d.text((W // 2, y + 110), 'dresslikemommy.com', font=F(SANSB, 70), fill=RED, anchor='mm')
    return img

def render(name, shots, hook, numbered, end1, end2, per=2.0, xf=0.4):
    proc = subprocess.Popen([FF, '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                             '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-preset', 'medium', '-crf', '22', '-movflags', '+faststart', f'videos/{name}.mp4'], stdin=subprocess.PIPE)
    bigs = [base(p) for p in shots]; n = int(per * FPS); nx = int(xf * FPS)
    def deco(img, i):
        if numbered: img = label(img, str(i + 1))
        return banner(img, hook, 1440)
    prev = None
    for i, bg in enumerate(bigs):
        for k in range(n):
            fr = deco(frame_of(bg, k / n), i)
            if prev is not None and k < nx: fr = Image.blend(prev, fr, k / nx)
            proc.stdin.write(fr.tobytes())
        prev = fr
    ec = endcard(end1, end2)
    for k in range(int(3.0 * FPS)):
        fr = Image.blend(prev, ec, k / nx) if k < nx else ec
        proc.stdin.write(fr.tobytes())
    proc.stdin.close(); proc.wait(); print(name, proc.returncode)

src = lambda h, i=0: f'pins/src/{h}_{i}.jpg'
END2 = 'Kids from $32.99 · Adults $35.99 · Each person sized separately · Order by Dec 8 for estimated US Christmas arrival'
render('dlm-xmas26-pov-pajamas', [src('classic-red-plaid-family-matching-pajamas'), src('we-are-family-red-family-matching-pajamas'), src('snowy-village-stripes-family-matching-pajamas'), src('blue-plaid-reindeer-family-matching-pajamas'), src('lights-out-reindeer-family-matching-pajamas'), src('evergreen-fair-isle-family-matching-pajamas')],
       'POV: this is the year the whole family matches 🎄'.replace(' 🎄', ''), False, 'Matching Family Christmas Pajamas 2026', END2)
render('dlm-xmas26-which-one-pajamas', [src('jolly-crew-family-matching-pajamas'), src('buffalo-plaid-tree-family-matching-pajamas'), src('let-it-snow-family-matching-pajamas'), src('green-plaid-merry-tree-family-matching-pajamas'), src('plaid-tree-trio-family-matching-pajamas'), src('joyful-merry-blessed-family-matching-pajamas')],
       'Which one is your family? Comment a number', True, '28 new matching Christmas designs', END2)
render('dlm-xmas26-sweaters', [src('jingle-bells-santa-family-matching-sweaters'), src('nordic-reindeer-family-matching-sweaters'), src('candy-cane-reindeer-family-matching-sweaters'), src('reindeer-row-family-matching-sweaters'), src('santa-hat-reindeer-family-matching-sweaters'), src('ho-ho-santa-family-matching-sweaters')],
       'Christmas card photo, sorted: matching family sweaters', False, 'Matching Family Christmas Sweaters 2026', END2)
render('dlm-xmas26-morning', [src('classic-red-plaid-family-matching-pajamas', 1), src('we-are-family-red-family-matching-pajamas', 1), src('snowy-village-stripes-family-matching-pajamas', 1), src('plaid-reindeer-family-matching-pajamas', 1), src('snowflake-reindeer-family-matching-onesie-pajamas', 0), src('lights-out-reindeer-family-matching-pajamas', 1)],
       'Christmas morning, but make it matching', False, 'Mom, Dad & the kids. All matching.', END2)
