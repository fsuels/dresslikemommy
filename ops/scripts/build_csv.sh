#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CHART="$SCRIPT_DIR/size_chart.json"
BODY_FILE="$SCRIPT_DIR/../listings/body.html"
OUT="$SCRIPT_DIR/../listings/autumn-peter-rabbit-mommy-and-me-pajamas-shopify-import.csv"

HANDLE="autumn-peter-rabbit-mommy-and-me-pajamas"
TITLE="Autumn Peter Rabbit Mommy and Me Pajamas — Short-Sleeve Set"
VENDOR="dresslikemommy.com"
PTYPE="Matching Family Pajamas"
TAGS='Autumn, Beige, Bunny, Child 2-3yr, Child 4-5yr, Child 6-8yr, Child 9-10yr, Cotton Gauze, Cream, Fall, Floral, Matching Family Pajamas, Mom Size L, Mom Size M, Mom Size S, Mom Size XL, Mommy and Me, Muslin, Pajamas, Peter Rabbit, Rabbit, Short Sleeve Pajamas, Woodland, https://detail.1688.com/offer/828526529351.html'
SEO_T="Peter Rabbit Mommy & Me Pajamas | Dress Like Mommy"
SEO_D="Shop our Autumn Peter Rabbit matching mommy-and-me pajamas — soft cotton Short-Sleeve Set for mom + daughter. Kids 2Y–10Y, Mom S–XL."
COLOR_NAME="Autumn Peter Rabbit"

BODY=$(python3 -c "import csv,sys; print(open('$BODY_FILE').read().replace('\r',' ').replace('\n',' '))")

HEADER='Handle,Title,Body (HTML),Vendor,Product Category,Type,Tags,Published,Option1 Name,Option1 Value,Option1 Linked To,Option2 Name,Option2 Value,Option2 Linked To,Option3 Name,Option3 Value,Option3 Linked To,Variant SKU,Variant Grams,Variant Inventory Tracker,Variant Inventory Qty,Variant Inventory Policy,Variant Fulfillment Service,Variant Price,Variant Compare At Price,Variant Requires Shipping,Variant Taxable,Variant Barcode,Image Src,Image Position,Image Alt Text,Gift Card,SEO Title,SEO Description,Google Shopping / Google Product Category,Google Shopping / Gender,Google Shopping / Age Group,Google Shopping / MPN,Google Shopping / Condition,Google Shopping / Custom Product,Google Shopping / Custom Label 0,Google Shopping / Custom Label 1,Google Shopping / Custom Label 2,Google Shopping / Custom Label 3,Google Shopping / Custom Label 4,Variant Image,Variant Weight Unit,Variant Tax Code,Cost per item,Included / United States,Price / United States,Compare At Price / United States,Included / International,Price / International,Compare At Price / International,Status'

python3 <<PY
import json, csv

with open("$CHART") as f:
    chart = json.load(f)
with open("$BODY_FILE") as f:
    body = f.read().replace("\r", " ").replace("\n", " ")

rows = []
header = "$HEADER".split(",")

first = True
for row in chart:
    price = "35.99" if row["audience"] == "child" else "39.99"
    cmp_  = "40.24" if row["audience"] == "child" else "45.99"
    sku   = f"DLM-VCF-{row['sku_suffix']}-CREAM"
    r = {h: "" for h in header}
    r["Handle"] = "$HANDLE"
    r["Option1 Name"] = "Size"
    r["Option1 Value"] = row["picker_label"]
    r["Option2 Name"] = "Color"
    r["Option2 Value"] = "$COLOR_NAME"
    r["Variant SKU"] = sku
    r["Variant Grams"] = "260" if row["audience"] == "child" else "480"
    r["Variant Inventory Tracker"] = "shopify"
    r["Variant Inventory Qty"] = "0"
    r["Variant Inventory Policy"] = "deny"
    r["Variant Fulfillment Service"] = "manual"
    r["Variant Price"] = price
    r["Variant Compare At Price"] = cmp_
    r["Variant Requires Shipping"] = "TRUE"
    r["Variant Taxable"] = "TRUE"
    r["Gift Card"] = "false"
    r["Variant Weight Unit"] = "oz"
    r["Status"] = "active"
    if first:
        r["Title"] = "$TITLE"
        r["Body (HTML)"] = body
        r["Vendor"] = "$VENDOR"
        r["Product Category"] = "Apparel & Accessories > Clothing > Sleepwear & Loungewear > Pajamas"
        r["Type"] = "$PTYPE"
        r["Tags"] = '$TAGS'
        r["Published"] = "TRUE"
        r["SEO Title"] = "$SEO_T"
        r["SEO Description"] = "$SEO_D"
        r["Google Shopping / Gender"] = "female"
        r["Google Shopping / Age Group"] = "adult"
        r["Google Shopping / Condition"] = "new"
        r["Google Shopping / Custom Product"] = "FALSE"
        r["Google Shopping / Custom Label 0"] = "Mommy and Me"
        r["Google Shopping / Custom Label 1"] = "Peter Rabbit"
        r["Google Shopping / Custom Label 2"] = "Fall"
        r["Google Shopping / Custom Label 3"] = "Short-Sleeve Set"
        r["Google Shopping / Custom Label 4"] = "Family Matching"
        first = False
    rows.append(r)

with open("$OUT", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=header, quoting=csv.QUOTE_MINIMAL)
    w.writeheader()
    w.writerows(rows)
print(f"Wrote {len(rows)} variant rows to $OUT")
PY
