"""Build the local, customer-facing one-page family outfit planner. No network."""
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_LEFT
from urllib.parse import urlencode

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "output/pdf/family-photo-outfit-planner.pdf"
OUT.parent.mkdir(parents=True, exist_ok=True)
W, H = 612, 792
INK = colors.HexColor("#292529")
MUTED = colors.HexColor("#665D60")
ROSE = colors.HexColor("#895363")
LINE = colors.HexColor("#D8CBCB")
PALE = colors.HexColor("#F8F2EF")
c = canvas.Canvas(str(OUT), pagesize=(W,H), pageCompression=1)
c.setTitle("Family Photo Outfit Planner | Dress Like Mommy")
c.setAuthor("Dress Like Mommy")
c.setSubject("A practical checklist for planning coordinated family outfits.")
styles = {
    "body": ParagraphStyle("body", fontName="Helvetica", fontSize=10, leading=14, textColor=INK),
    "small": ParagraphStyle("small", fontName="Helvetica", fontSize=8.5, leading=11.5, textColor=MUTED),
    "head": ParagraphStyle("head", fontName="Helvetica-Bold", fontSize=12, leading=16, textColor=ROSE)
}
def p(text,x,y,w,style="body"):
    para=Paragraph(text,styles[style]); _,h=para.wrap(w,1000)
    para.drawOn(c,x,y-h)
    return y-h
def rule(y):
    c.setStrokeColor(LINE); c.setLineWidth(.6); c.line(42,y,570,y)
def label(text,x,y):
    c.setFillColor(MUTED); c.setFont("Helvetica",9); c.drawString(x,y,text)
def link(text,url,x,y,w):
    p('<link href="'+url.replace("&","&amp;")+'" color="#895363"><u>'+text+'</u></link>',x,y,w)
def tracked(path,content):
    return "https://www.dresslikemommy.com"+path+"?"+urlencode({"utm_source":"family_photo_planner","utm_medium":"referral","utm_campaign":"organic_202609","utm_content":content})

c.setFillColor(PALE); c.rect(0,650,W,142,fill=1,stroke=0)
c.setFillColor(ROSE); c.setFont("Helvetica-Bold",11)
c.drawString(42,750,"DRESS LIKE MOMMY")
c.setFillColor(INK); c.setFont("Helvetica-Bold",25)
c.drawString(42,713,"Family photo outfit planner")
p("Pick a palette. Plan each person's pieces. Check the details before you order.",42,693,516)

label("PHOTO DATE",42,626); c.setStrokeColor(LINE); c.line(118,624,295,624)
label("LOCATION / WEATHER",322,626); c.line(445,624,570,624)
label("OUR COLORS",42,601); c.line(126,599,570,599)

p("01  Make a plan for everyone",42,576,528,"head")
p("Start with one print or color you love. Coordinate the rest with clothes, shoes and layers you already own.",42,555,528)

xs=[42,112,267,339,459,570]
top=507
c.setFillColor(PALE); c.rect(42,top-27,528,27,fill=1,stroke=0)
headers=["Person","Piece / look","Size*","Already own","To add / qty"]
for i,text in enumerate(headers):
    c.setFont("Helvetica-Bold",9); c.setFillColor(INK); c.drawString(xs[i]+8,top-17,text)
for row in range(5):
    y=top-27-row*37
    rule(y)
    if row<4:
        for x in xs:
            c.setStrokeColor(LINE); c.line(x,y,x,y-37)
rule(top-27-4*37)
p("*Use the size chart on each exact product page. Check the units and measurements shown; age labels alone do not confirm fit.",42,320,528,"small")

p("02  Check before you order",42,278,528,"head")
checks=[
("What one selection includes", "Where pieces are sold separately, add a size for each wearer."),
("Sizes, quantities and total", "Review every bag line and the combined price."),
("Delivery for your destination", "Check current estimates and allow time to try outfits on."),
("Comfort and a backup", "Try the whole look with shoes and layers; keep a backup ready.")
]
for i,(title,body) in enumerate(checks):
    x=42+(i%2)*270; y=254-(i//2)*51
    c.setStrokeColor(ROSE); c.rect(x,y-10,8,8,fill=0,stroke=1)
    p("<b>"+title+"</b><br/>"+body,x+16,y,239,"small")

rule(151)
p("03  Choose a look to build around",42,137,528,"head")
link("Colorful rainbow dresses",tracked("/products/vibrant-rainbow-maxi-dress-set-for-mom-and-daughter-colorful-summer-matching-outfits","planner_rainbow"),42,112,250)
link("Pastel floral dresses",tracked("/products/pastel-bloom-mommy-and-me-dresses","planner_pastel"),312,112,240)
p("Mother and daughter dresses are separate selections. Check current sizes, prices and delivery information on the product page.",42,92,528,"small")
c.setFillColor(MUTED); c.setFont("Helvetica",8.5)
c.drawString(42,42,"Dress Like Mommy  |  www.dresslikemommy.com")
c.drawRightString(570,42,"Keep this planner for your next family photo.")
c.save()
print(OUT)

