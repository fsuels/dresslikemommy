import json, csv, re, sys, datetime as dt
rows = {r['h']: r for r in json.load(open('xmas_products.json'))}
urls = json.load(open('file_urls.json'))  # filename -> public CDN url
def name(t): return re.split(r'\s+Family Matching', t)[0].strip()
def kind(h):
    return 'onesies' if 'onesie' in h else 'sweaters' if 'sweater' in h else 'pajamas'
BOARD = {'pajamas': 'Matching Family Christmas Pajamas', 'onesies': 'Matching Family Christmas Pajamas', 'sweaters': 'Matching Family Christmas Sweaters'}
KW = {'pajamas': 'matching family christmas pajamas, family christmas pajamas, christmas pajamas for family, matching christmas pjs, family christmas photo',
      'onesies': 'matching family christmas onesies, family christmas pajamas, christmas onesie family, matching christmas pjs',
      'sweaters': 'matching family christmas sweaters, family christmas sweaters, ugly christmas sweater family, matching christmas outfits, family christmas photo'}
def title(r, n):
    k = kind(r['h']); nm = name(r['t'])
    return (f"{nm} Matching Family Christmas {k.title()}" if n == 1 else f"Matching Christmas {k.title()} for Mom, Dad & Kids: {nm}")[:100]
def desc(r, n):
    k = kind(r['h']); nm = name(r['t']); p = f"${r['pmin']:.2f}"
    sizes = 'baby, kids and adult sizes' if k == 'onesies' else 'kids and adult sizes'
    a = (f"New for Christmas 2026: {nm} matching family Christmas {k}. Each person's piece is sold separately, so you pick a size for everyone on one page ({sizes}). "
         f"From {p} per person, standard shipping included. Order by Dec 8 for estimated US Christmas arrival.")
    b = (f"Planning the family Christmas photo? The {nm} {k} match the whole crew: mom, dad and the kids ({sizes}). "
         f"From {p} per person with standard shipping included. Estimated delivery is 12-16 days, so order by Dec 8 for US Christmas morning.")
    return (a if n == 1 else b)[:500]
def link(h, n):
    return f"https://www.dresslikemommy.com/products/{h}?utm_source=pinterest&utm_medium=organic&utm_campaign=xmas2026_pins&utm_content={h}-pin{n}"
hs = sorted(rows)
order = [(h, 1) for h in hs]
half = len(hs) // 2
order2 = [(h, 2) for h in hs[half:] + hs[:half]]   # second pin of a design lands ~2 weeks after its first
start = dt.date.fromisoformat(sys.argv[1])
slots = []
for i in range(len(hs)):
    day = start + dt.timedelta(days=i)
    slots.append((order[i], f"{day}T14:00:00"))   # 10:00 ET
    slots.append((order2[i], f"{day + dt.timedelta(days=1)}T01:00:00"))  # 21:00 ET same US day
hdr = ['Title', 'Media URL', 'Pinterest board', 'Thumbnail', 'Description', 'Link', 'Publish date', 'Keywords']
for b, part in enumerate([slots[:len(slots)//2], slots[len(slots)//2:]], 1):
    with open(f'pinterest_bulk_xmas2026_batch{b}.csv', 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh, lineterminator='\n'); w.writerow(hdr)
        for (h, n), when in part:
            r = rows[h]; fn = f"dlm-{h}-pin{n}.jpg"
            w.writerow([title(r, n), urls[fn], BOARD[kind(h)], '', desc(r, n), link(h, n), when, KW[kind(h)]])
    print('batch', b, len(part), part[0][1], '->', part[-1][1])
