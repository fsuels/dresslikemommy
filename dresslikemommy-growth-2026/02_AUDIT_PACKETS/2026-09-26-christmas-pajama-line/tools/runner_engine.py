# Generic engine for 2026 Christmas family pajama draft runners.
# The generator prepends `SPEC = {...}` (one design) and wraps this file in a
# bash heredoc at ops/scripts/create-<shortcode>-<handle>.sh. Everything that
# varies by design lives in SPEC; SIZE_CHART is declared once from SPEC and all
# variants, tables, tags, SKUs and size refs are derived from it.
import csv
import html
import json
import math
import mimetypes
import os
import re
import subprocess
import tempfile
import time
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

import requests


ROOT = Path("/Users/fsuels/Projects/dresslikemommy")
API = f"https://{os.environ['SHOPIFY_STORE_DOMAIN']}/admin/api/2025-01/graphql.json"
TOKEN = os.environ["SHOPIFY_ADMIN_ACCESS_TOKEN"]

HANDLE = SPEC["handle"]
PRINT_NAME = SPEC["print_name"]
SHORTCODE = SPEC["shortcode"]
COLORS = SPEC["colors"]
COLOR_NAMES = [item["name"] for item in COLORS]
COLOR_TOKEN_BY_NAME = {item["name"]: item["token"] for item in COLORS}
COLOR_PATTERN_GIDS = SPEC["color_pattern_gids"]
COLOR_PATTERN_LABELS = SPEC["color_pattern_labels"]
FABRIC_GIDS = {
    "polyester": ["gid://shopify/Metaobject/69622366305"],
    "polyblend": ["gid://shopify/Metaobject/69622366305"],
    "poly95": ["gid://shopify/Metaobject/69622366305"],
    "cotton": ["gid://shopify/Metaobject/69622399073"],
    "cvc": ["gid://shopify/Metaobject/69622399073", "gid://shopify/Metaobject/69622366305"],
    "cotton35": ["gid://shopify/Metaobject/69622399073"],
    "cotton65": ["gid://shopify/Metaobject/69622399073"],
    "poly_velvet": ["gid://shopify/Metaobject/69622366305"],
    "cotton_sweat": ["gid://shopify/Metaobject/69622399073"],
    "coral_fleece": ["gid://shopify/Metaobject/69622366305"],
}[SPEC["fabric_key"]]
FABRIC_LABEL = {"polyester": "Polyester", "polyblend": "Polyester", "poly95": "Polyester", "cotton": "Cotton", "cvc": "Cotton, Polyester", "cotton35": "Cotton", "cotton65": "Cotton", "poly_velvet": "Polyester", "cotton_sweat": "Cotton", "coral_fleece": "Polyester"}[SPEC["fabric_key"]]
VENDOR = "dresslikemommy.com"
# Mode: "family_christmas" (mom, dad and kids; the 2026 Christmas line) or
# "mommy_me" (mother and child only; season-neutral winter copy).
MODE = SPEC.get("mode", "family_christmas")
MM = MODE == "mommy_me"
SW = MODE == "family_sweatshirt"  # unisex family crewneck sweatshirt (child + adult sizes)
PET = MODE == "family_pet"  # matching pet piece sold beside a family print (dog sizes only)
LISTING_MODE = "Mommy and Me" if MM else "Family Matching"
PRIMARY_CATEGORY = "Tops" if SW else ("Pet Apparel" if PET else "Pajamas")
PRODUCT_TYPE = "Family Matching Sweatshirts" if SW else "Matching Family Pajamas"  # SW type must contain "Family Matching" for the new-arrivals rule
TAXONOMY_GID = ("gid://shopify/TaxonomyCategory/aa-1-13-14" if SW else
                "gid://shopify/TaxonomyCategory/ap-2-6-13" if PET else "gid://shopify/TaxonomyCategory/aa-1-17-4")
EXPECTED_TAXONOMY_FULL_NAME = (
    "Apparel & Accessories > Clothing > Clothing Tops > Sweatshirts" if SW else
    "Animals & Pet Supplies > Pet Supplies > Pet Apparel > Pet Shirts" if PET else
    "Apparel & Accessories > Clothing > Sleepwear & Loungewear > Pajamas"
)
if PET:
    PRODUCT_TYPE = "Matching Family Pet Pajamas"  # contains "Pajamas" for the new-arrivals rule
FORCE_SPEC_PRICES = True
CHILD_PRICE = SPEC.get("child_price", "32.99")
ADULT_PRICE = SPEC.get("adult_price", "35.99")
SLEEVE_STYLE = SPEC.get("sleeve_style", "Long-Sleeve")

UPLOAD_DIR = ROOT / "uploads" / HANDLE
PRODUCT_IMAGE = UPLOAD_DIR / SPEC["image_filename"]
SOURCE_SIZE_CHART = ROOT / "ops/listings" / f"source-size-chart-{HANDLE}.jpg"
LISTING_MD = ROOT / "ops/listings" / f"{HANDLE}-listing.md"
CSV_OUT = ROOT / "ops/listings" / f"{HANDLE}-shopify-import.csv"
VERIFY_JSON_OUT = ROOT / "ops/listings" / f"verify-{HANDLE}.json"
SIZE_CHART_OUT = ROOT / "ops/listings" / f"size-chart-{HANDLE}.json"
BODY_HTML_OUT = ROOT / "ops/listings" / f"body-{HANDLE}.html"
SCRIPT_PATH = ROOT / "ops/scripts" / f"create-{SHORTCODE.lower()}-{HANDLE}.sh"
LOCALIZATION_CLOSEOUT = ROOT / "ops/listings" / f"{HANDLE}-localization-closeout.json"
CSV_HEADER_SOURCE = ROOT / "bird-chirping-mommy-and-me-pajamas-shopify-import.csv"

MEDIA_ALT = SPEC["media_alt"]

AGE_GROUP_GIDS = {
    "child": "gid://shopify/Metaobject/128116523105",
    "adult": "gid://shopify/Metaobject/128116490337",
}
TARGET_GENDER_GIDS = ["gid://shopify/Metaobject/129971617889" if MM else "gid://shopify/Metaobject/129972502625"]  # Female (Mommy & Me) / Unisex

# Store shopify--size catalog (read 2026-09-26). The store has no "14"
# metaobject, so Child 14 Years is skipped rather than faked. Mother and
# Father S-3XL share the adult metaobjects, so each GID is listed once.
SIZE_MAP_ALL = {
    "Child 2 Years": ("gid://shopify/Metaobject/129972863073", "2-3 years"),
    "Child 3 Years": ("gid://shopify/Metaobject/129972895841", "3-4 years"),
    "Child 4 Years": ("gid://shopify/Metaobject/129972928609", "4-5 years"),
    "Child 5 Years": ("gid://shopify/Metaobject/129972961377", "5-6 years"),
    "Child 6 Years": ("gid://shopify/Metaobject/129972994145", "6"),
    "Child 8 Years": ("gid://shopify/Metaobject/129973026913", "8"),
    "Child 10 Years": ("gid://shopify/Metaobject/129971552353", "10"),
    "Child 12 Years": ("gid://shopify/Metaobject/129971650657", "12"),
    "Mother S": ("gid://shopify/Metaobject/129975255137", "S"),
    "Mother M": ("gid://shopify/Metaobject/129975222369", "M"),
    "Mother L": ("gid://shopify/Metaobject/129975189601", "L"),
    "Mother XL": ("gid://shopify/Metaobject/129975287905", "XL"),
    "Mother 2XL": ("gid://shopify/Metaobject/129975156833", "2XL"),
    "Mother 3XL": ("gid://shopify/Metaobject/139840421985", "3XL"),
    "Father S": ("gid://shopify/Metaobject/129975255137", "S"),
    "Father M": ("gid://shopify/Metaobject/129975222369", "M"),
    "Father L": ("gid://shopify/Metaobject/129975189601", "L"),
    "Father XL": ("gid://shopify/Metaobject/129975287905", "XL"),
    "Father 2XL": ("gid://shopify/Metaobject/129975156833", "2XL"),
    "Father 3XL": ("gid://shopify/Metaobject/139840421985", "3XL"),
    "Mother 4XL": ("gid://shopify/Metaobject/139840716897", "4XL"),
    "Father 4XL": ("gid://shopify/Metaobject/139840716897", "4XL"),
}
NO_HONEST_SIZE_MATCH_ALL = {"Child 14 Years", "Child 7 Years", "Child 8-9 Years", "Child 10-11 Years"}
SIZE_MAP_ALL["Child 5-6 Years"] = ("gid://shopify/Metaobject/129972961377", "5-6 years")

ROLE_BY_AUDIENCE = {
    "child": "Child Sweatshirt" if SW else "Child Pajama Set",
    "mother": "Mother Pajama Set",
    "father": "Father Pajama Set",
    "adult": "Adult Sweatshirt",
    "pet": "Dog Vest",
}
# Sweatshirt picker labels: child ages are the usual bands for the chart's heights;
# only exact store size metaobjects are referenced.
SIZE_MAP_ALL.update({
    "Child 2-3 Years": ("gid://shopify/Metaobject/129972863073", "2-3 years"),
    "Adult S": ("gid://shopify/Metaobject/129975255137", "S"), "Adult M": ("gid://shopify/Metaobject/129975222369", "M"),
    "Adult L": ("gid://shopify/Metaobject/129975189601", "L"), "Adult XL": ("gid://shopify/Metaobject/129975287905", "XL"),
    "Adult 2XL": ("gid://shopify/Metaobject/129975156833", "2XL"), "Adult 3XL": ("gid://shopify/Metaobject/139840421985", "3XL"),
    "Adult 4XL": ("gid://shopify/Metaobject/139840716897", "4XL"),
})
NO_HONEST_SIZE_MATCH_ALL |= {"Dog S", "Dog M", "Dog L", "Dog XL", "Dog 2XL", "Child 6-12 Months", "Child 1-2 Years", "Child 4 Years", "Child 7-8 Years",
                             "Child 9-10 Years", "Child 11-12 Years"}

# Factory size chart (cm), transcribed from the supplier's own published
# chart image (offer 1073505941343; saved per listing as SOURCE_SIZE_CHART).
# Columns: 衣长 top length, 胸围 full chest (as-is), 袖长 sleeve, 裤长 pant
# length, 腰围 waist (elastic: relaxed-stretched range, as-is), 臀围 hip (as-is).
# The chart's 婴儿 baby rows (a separate romper with top measurements only) are
# never listed: baby is not an allowed Family Matching role.
FACTORY_CHART = {
    # vendor SKU label: (chart label, picker label, sku suffix, age, length, chest, sleeve, pant, waist, hip)
    "Children 2": ("80(2T)", "Child 2 Years", "KID2Y", "2", 39, 63, 29.5, 51, "42-60", 65),
    "Children 3": ("90(3T)", "Child 3 Years", "KID3Y", "3", 41, 65.5, 31.5, 55, "44-64", 68),
    "Children 4": ("100(4T)", "Child 4 Years", "KID4Y", "4", 43, 68, 33.5, 59, "46-68", 71),
    "Children 5": ("110(5T)", "Child 5 Years", "KID5Y", "5", 45, 70.5, 35.5, 63, "48-72", 75),
    "Children 6": ("120(6T)", "Child 6 Years", "KID6Y", "6", 47, 73, 37.5, 67, "50-76", 78),
    "Children 8": ("130(8T)", "Child 8 Years", "KID8Y", "8", 51, 78, 41.5, 75, "53-81", 83),
    "Children 10": ("140(10T)", "Child 10 Years", "KID10Y", "10", 55, 83, 45.5, 83, "56-86", 88),
    "Children 12": ("150(12T)", "Child 12 Years", "KID12Y", "12", 59, 88, 49.5, 91, "59-91", 93),
    "Children 14": ("160(14T)", "Child 14 Years", "KID14Y", "14", 63, 92, 53.5, 99, "62-96", 98),
    "Mom S": ("Womens S", "Mother S", "S", "—", 64, 97, 56.5, 100, "64-101", 102),
    "Mom M": ("Womens M", "Mother M", "M", "—", 66, 102, 57.5, 102, "68-106", 107),
    "Mom L": ("Womens L", "Mother L", "L", "—", 68, 107, 58.5, 104, "72-111", 112),
    "Mom XL": ("Womens XL", "Mother XL", "XL", "—", 70, 112, 59.5, 106, "76-116", 117),
    "Mom 2XL": ("Womens 2XL", "Mother 2XL", "2XL", "—", 72, 117, 60.5, 108, "80-121", 122),
    "Mom 3XL": ("Womens 3XL", "Mother 3XL", "3XL", "—", 74, 122, 61.5, 110, "84-126", 127),
    "Dad S": ("Mens S", "Father S", "S", "—", 70, 106, 61, 103, "68-104", 108),
    "Dad M": ("Mens M", "Father M", "M", "—", 72, 112, 62, 105, "72-110", 114),
    "Dad L": ("Mens L", "Father L", "L", "—", 74, 118, 63, 107, "76-116", 120),
    "Dad XL": ("Mens XL", "Father XL", "XL", "—", 76, 124, 64, 109, "80-122", 126),
    "Dad 2XL": ("Mens 2XL", "Father 2XL", "2XL", "—", 78, 130, 65, 110, "84-128", 132),
    "Dad 3XL": ("Mens 3XL", "Father 3XL", "3XL", "—", 80, 136, 66, 113, "88-134", 138),
    # 4XL rows appear only on the 4XL line's own chart (offer 1080353625335).
    "Dad 4XL": ("Mens 4XL", "Father 4XL", "4XL", "—", 82, 142, 67, 115, "92-140", 144),
    "Mom 4XL": ("Womens 4XL", "Mother 4XL", "4XL", "—", 76, 127, 62.5, 112, "88-131", 132),
}
# The 4XL line labels child SKUs with the chart's own T codes.
for _n in (2, 3, 4, 5, 6, 8, 10, 12, 14):
    FACTORY_CHART[f"{_n}T"] = FACTORY_CHART[f"Children {_n}"]


# 佐雅 (Guangzhou Zoya garment, 6-yr 1688 factory) chart, transcribed from the
# supplier's own published SIZE TABLE (offer 810867411211, description image 06;
# saved per listing as SOURCE_SIZE_CHART). Garment cm; waist is a single published
# figure (the pants are elastic), kept as-is rather than invented as a range.
# Kid rows are keyed by the SKU labels (Child 2 = 1~2T ... Child 14 = 13~14T).
ZOYA_CHART = {
    "Child 2": ("1~2T", "Child 2 Years", "KID2Y", "2", 39, 63, 36, 51, "42", 65),
    "Child 3": ("2~3T", "Child 3 Years", "KID3Y", "3", 41, 65.5, 39, 55, "44", 68),
    "Child 4": ("3~4T", "Child 4 Years", "KID4Y", "4", 43, 68, 41, 59, "46", 71),
    "Child 5": ("4~5T", "Child 5 Years", "KID5Y", "5", 45, 70.5, 44, 63, "48", 75),
    "Child 6": ("5~6T", "Child 6 Years", "KID6Y", "6", 47, 73, 47, 67, "50", 78),
    "Child 8": ("7~8T", "Child 8 Years", "KID8Y", "8", 51, 78, 51, 75, "53", 83),
    "Child 10": ("9~10T", "Child 10 Years", "KID10Y", "10", 55, 83, 55, 83, "56", 88),
    "Child 12": ("11~12T", "Child 12 Years", "KID12Y", "12", 59, 88, 59, 91, "59", 93),
    "Child 14": ("13~14T", "Child 14 Years", "KID14Y", "14", 63, 92, 63, 99, "62", 98),
    "Mom S": ("Womens S", "Mother S", "S", "—", 64, 97, 66, 100, "64", 102),
    "Mom M": ("Womens M", "Mother M", "M", "—", 66, 102, 68, 102, "68", 107),
    "Mom L": ("Womens L", "Mother L", "L", "—", 68, 107, 70, 104, "72", 112),
    "Mom XL": ("Womens XL", "Mother XL", "XL", "—", 70, 112, 72, 106, "76", 117),
    "Mom 2XL": ("Womens 2XL", "Mother 2XL", "2XL", "—", 72, 117, 74, 108, "80", 122),
    "Mom 3XL": ("Womens 3XL", "Mother 3XL", "3XL", "—", 74, 122, 76, 110, "84", 127),
    "Mom 4XL": ("Womens 4XL", "Mother 4XL", "4XL", "—", 76, 127, 78, 112, "88", 132),
    "Dad S": ("Mens S", "Father S", "S", "—", 70, 106, 73, 103, "68", 108),
    "Dad M": ("Mens M", "Father M", "M", "—", 72, 112, 75, 105, "72", 114),
    "Dad L": ("Mens L", "Father L", "L", "—", 74, 118, 77, 107, "76", 120),
    "Dad XL": ("Mens XL", "Father XL", "XL", "—", 76, 124, 79, 109, "80", 126),
    "Dad 2XL": ("Mens 2XL", "Father 2XL", "2XL", "—", 78, 130, 81, 111, "84", 132),
    "Dad 3XL": ("Mens 3XL", "Father 3XL", "3XL", "—", 80, 136, 83, 113, "88", 138),
    "Dad 4XL": ("Mens 4XL", "Father 4XL", "4XL", "—", 82, 142, 85, 115, "92", 144),
}
# Round (set-in) sleeve variant: the factory's "圆袖" SIZE TABLE (offer 816112676067,
# description image 06) differs only in sleeve length.
_ROUND_SLEEVE = {"Child 2": 29.5, "Child 3": 31.5, "Child 4": 33.5, "Child 5": 35.5, "Child 6": 37.5, "Child 8": 41.5,
                 "Child 10": 45.5, "Child 12": 49.5, "Child 14": 53.5, "Mom S": 56.5, "Mom M": 57.5, "Mom L": 58.5,
                 "Mom XL": 59.5, "Mom 2XL": 60.5, "Mom 3XL": 61.5, "Mom 4XL": 62.5, "Dad S": 61, "Dad M": 62,
                 "Dad L": 63, "Dad XL": 64, "Dad 2XL": 65, "Dad 3XL": 66, "Dad 4XL": 67}
ZOYA_ROUND_CHART = {k: v[:6] + (_ROUND_SLEEVE[k],) + v[7:] for k, v in ZOYA_CHART.items()}

# 衣林 (Guangzhou Yilin garment; our top pajama supplier by order history) charts,
# transcribed from the supplier's own published tables (garment cm; waist is the
# single relaxed figure the tables publish).
# yilin_cn: the Chinese 男装/女装/儿童 正肩袖 tables (2024/5) published on offers
# 1029357235756 and 1033855142669, whose kid SKUs use the same 2..13-14 labels.
# yilin_en: the English Women's/Men's/Kids' Size Chart published on offers
# 1048815429526 and 1072941798877, whose kid SKUs use the same 2T..14T labels.
YILIN_CN_CHART = {
    "Child 2": ("2T", "Child 2 Years", "KID2Y", "2", 36, 61.5, 30, 52, "42", 64),
    "Child 3": ("3T", "Child 3 Years", "KID3Y", "3", 39, 64.5, 33, 57, "44", 67),
    "Child 4": ("4T", "Child 4 Years", "KID4Y", "4", 41, 67, 35.5, 62, "46", 70),
    "Child 5": ("5T", "Child 5 Years", "KID5Y", "5", 43, 69.5, 38, 66, "48", 73),
    "Child 6": ("6-7T", "Child 6 Years", "KID6Y", "6-7", 46, 72.5, 40.5, 72, "50", 76),
    "Child 8": ("8-9T", "Child 8 Years", "KID8Y", "8-9", 52, 79.5, 45.5, 78, "53", 82),
    "Child 10": ("10-11T", "Child 10 Years", "KID10Y", "10-11", 58, 86.5, 50.5, 87, "56", 88),
    "Child 12": ("11-12T", "Child 12 Years", "KID12Y", "11-12", 63, 93.5, 55, 93, "60", 94),
    "Child 14": ("13-14T", "Child 14 Years", "KID14Y", "13-14", 68, 100.5, 59, 99, "64", 100),
    "Mom S": ("Womens S", "Mother S", "S", "—", 63, 98, 59, 103, "68", 104),
    "Mom M": ("Womens M", "Mother M", "M", "—", 64, 102, 60, 104.5, "72", 108),
    "Mom L": ("Womens L", "Mother L", "L", "—", 65, 108, 61, 106, "77", 114),
    "Mom XL": ("Womens XL", "Mother XL", "XL", "—", 66, 114, 62, 107, "82", 120),
    "Mom 2XL": ("Womens 2XL", "Mother 2XL", "2XL", "—", 67, 120, 63, 108, "87", 126),
    "Mom 3XL": ("Womens 3XL", "Mother 3XL", "3XL", "—", 68, 126, 64, 109, "93", 132),
    "Dad S": ("Mens S", "Father S", "S", "—", 70, 106, 63, 104, "73", 106),
    "Dad M": ("Mens M", "Father M", "M", "—", 72, 111, 65, 105.5, "78", 111),
    "Dad L": ("Mens L", "Father L", "L", "—", 74, 117, 67, 107, "83", 117),
    "Dad XL": ("Mens XL", "Father XL", "XL", "—", 76, 123, 68, 108.5, "90", 125),
    "Dad 2XL": ("Mens 2XL", "Father 2XL", "2XL", "—", 77, 129, 69, 110, "97", 133),
    "Dad 3XL": ("Mens 3XL", "Father 3XL", "3XL", "—", 78, 135, 70, 111, "104", 141),
}
YILIN_EN_CHART = {
    "Child 2": ("2T", "Child 2 Years", "KID2Y", "2", 37, 61.5, 34.9, 48, "40", 64),
    "Child 3": ("3T", "Child 3 Years", "KID3Y", "3", 39, 64.5, 38.2, 53, "42", 67),
    "Child 4": ("4T", "Child 4 Years", "KID4Y", "4", 41, 67, 41, 58, "44", 70),
    "Child 5": ("5T", "Child 5 Years", "KID5Y", "5", 43, 69.5, 43.8, 63, "46", 73),
    "Child 6": ("6T", "Child 6 Years", "KID6Y", "6", 46, 72.5, 46.6, 68, "48", 76),
    "Child 8": ("8T", "Child 8 Years", "KID8Y", "8", 52, 79.5, 52.2, 78, "51", 82),
    "Child 10": ("10T", "Child 10 Years", "KID10Y", "10", 58, 86.5, 57.8, 88, "54", 88),
    "Child 12": ("12T", "Child 12 Years", "KID12Y", "12", 63, 93.5, 62.9, 97, "58", 94),
    "Child 14": ("14T", "Child 14 Years", "KID14Y", "14", 69, 101, 67.5, 103, "62", 100),
    "Mom S": ("Womens S", "Mother S", "S", "—", 63, 98, 68, 103, "64", 104),
    "Mom M": ("Womens M", "Mother M", "M", "—", 64, 102, 69.5, 104.5, "68", 108),
    "Mom L": ("Womens L", "Mother L", "L", "—", 65, 108, 71, 106, "73", 114),
    "Mom XL": ("Womens XL", "Mother XL", "XL", "—", 66, 114, 72.5, 107, "78", 120),
    "Mom 2XL": ("Womens 2XL", "Mother 2XL", "2XL", "—", 67, 120, 73.5, 108, "83", 126),
    "Mom 3XL": ("Womens 3XL", "Mother 3XL", "3XL", "—", 68, 126, 74.5, 109, "89", 132),
    "Dad S": ("Mens S", "Father S", "S", "—", 70, 106, 73.2, 105, "68", 106),
    "Dad M": ("Mens M", "Father M", "M", "—", 72, 111, 75, 106, "73", 111),
    "Dad L": ("Mens L", "Father L", "L", "—", 74, 117, 76.8, 108, "78", 117),
    "Dad XL": ("Mens XL", "Father XL", "XL", "—", 76, 123, 78.6, 109, "83", 123),
    "Dad 2XL": ("Mens 2XL", "Father 2XL", "2XL", "—", 77, 129, 80.4, 111, "88", 129),
    "Dad 3XL": ("Mens 3XL", "Father 3XL", "3XL", "—", 78, 135, 81.2, 112, "93", 135),
}
# 诗茹梦 (Shenzhen Shirumeng) mommy-and-me velvet cardigan pajamas: the supplier's
# own 尺码展示 table (offer 1080921462408, description image 05). The table
# publishes length, chest, shoulder, sleeve, hip and pant length but no waist, so
# waist is "-". Heights and weights are the supplier's per-size fit guide (the
# SKU labels give them in cm/kg). Child ages are the usual age bands for those
# heights and are labelled as such in the body copy.
SHIRUMENG_CHART = {
    "Child 10": ("10 (110-120 cm)", "Child 5-6 Years", "KID56Y", "5-6", 47, 76, 32, 66, "-", 80),
    "Child 12": ("12 (120-130 cm)", "Child 7 Years", "KID7Y", "7", 50, 80, 36, 72, "-", 84),
    "Child 14": ("14 (125-135 cm)", "Child 8-9 Years", "KID89Y", "8-9", 53, 84, 40, 78, "-", 88),
    "Child 16": ("16 (135-145 cm)", "Child 10-11 Years", "KID1011Y", "10-11", 57, 88, 44, 84, "-", 92),
    "Mom S": ("Womens S", "Mother S", "S", "—", 60, 92, 47, 90, "-", 96),
    "Mom M": ("Womens M", "Mother M", "M", "—", 62, 98, 50, 93, "-", 100),
    "Mom L": ("Womens L", "Mother L", "L", "—", 65, 102, 52, 96, "-", 104),
    "Mom XL": ("Womens XL", "Mother XL", "XL", "—", 68, 106, 54, 99, "-", 108),
}
SHIRUMENG_FIT = {  # supplier fit guide: (height cm, weight kg)
    "Child 10": ("110-120", "19-22.5"), "Child 12": ("120-130", "22.5-27.5"),
    "Child 14": ("125-135", "25-30"), "Child 16": ("135-145", "27.5-34"),
    "Mom S": ("145-155", "34-42.5"), "Mom M": ("150-160", "42.5-50"),
    "Mom L": ("160-165", "50-57.5"), "Mom XL": ("165-170", "57.5-67.5"),
}
CHART_TABLE = {"zoya": ZOYA_CHART, "zoya_round": ZOYA_ROUND_CHART, "yilin_cn": YILIN_CN_CHART,
               "yilin_en": YILIN_EN_CHART, "shirumeng": SHIRUMENG_CHART}.get(SPEC.get("chart_table"), FACTORY_CHART)
# 斯蒂琪 (Shenzhen Sidiqi) family crewneck sweatshirt, offer 1081522411618: the
# supplier's 尺码表 (description image 00). 胸围x2 is doubled to a full chest;
# 建议体重 is in jin and halved to kg. The chart has no pant, hip or waist (tops only).
STQ_SWEAT_CHART = {
    "Child 80": ("80 (70-80 cm)", "Child 6-12 Months", "KID612M", "6-12 mo", 35, 69, 27, "-", "-", "-"),
    "Child 90": ("90 (80-90 cm)", "Child 1-2 Years", "KID12Y", "1-2", 38, 73, 29, "-", "-", "-"),
    "Child 100": ("100 (90-100 cm)", "Child 2-3 Years", "KID23Y", "2-3", 41, 77, 31, "-", "-", "-"),
    "Child 110": ("110 (100-110 cm)", "Child 4 Years", "KID4Y", "4", 44, 81, 33, "-", "-", "-"),
    "Child 120": ("120 (110-120 cm)", "Child 5-6 Years", "KID56Y", "5-6", 47, 85, 35, "-", "-", "-"),
    "Child 130": ("130 (120-130 cm)", "Child 7-8 Years", "KID78Y", "7-8", 50, 89, 37, "-", "-", "-"),
    "Child 140": ("140 (130-140 cm)", "Child 9-10 Years", "KID910Y", "9-10", 53, 93, 39, "-", "-", "-"),
    "Child 150": ("150 (140-150 cm)", "Child 11-12 Years", "KID1112Y", "11-12", 56, 97, 41, "-", "-", "-"),
    "Adult S": ("Adult S", "Adult S", "S", "—", 65, 108, 50.5, "-", "-", "-"),
    "Adult M": ("Adult M", "Adult M", "M", "—", 68, 112, 52, "-", "-", "-"),
    "Adult L": ("Adult L", "Adult L", "L", "—", 69, 116, 53.5, "-", "-", "-"),
    "Adult XL": ("Adult XL", "Adult XL", "XL", "—", 71, 120, 55, "-", "-", "-"),
    "Adult 2XL": ("Adult 2XL", "Adult 2XL", "2XL", "—", 73, 124, 56.5, "-", "-", "-"),
    "Adult 3XL": ("Adult 3XL", "Adult 3XL", "3XL", "—", 75, 128, 58, "-", "-", "-"),
    "Adult 4XL": ("Adult 4XL", "Adult 4XL", "4XL", "—", 77, 132, 59.5, "-", "-", "-"),
}
STQ_SWEAT_FIT = {  # (height cm, weight kg)
    "Child 80": ("70-80", "7-11"), "Child 90": ("80-90", "11-13.5"), "Child 100": ("90-100", "13.5-16.5"),
    "Child 110": ("100-110", "16.5-19"), "Child 120": ("110-120", "19-22.5"), "Child 130": ("120-130", "22.5-27.5"),
    "Child 140": ("130-140", "27.5-32.5"), "Child 150": ("140-150", "32.5-37.5"),
    "Adult S": ("150-165", "42.5-55"), "Adult M": ("155-170", "55-62.5"), "Adult L": ("160-175", "62.5-72.5"),
    "Adult XL": ("165-180", "72.5-82.5"), "Adult 2XL": ("170-185", "82.5-92.5"), "Adult 3XL": ("175-190", "92.5-105"),
    "Adult 4XL": ("180-195", "105-115"),
}
# 诗茹梦 coral-fleece mommy-and-me sets (offers 1083898601268 / 1084574812798): two
# published 尺码展示 tables, one per cut. Button-front table (image 03, full chest);
# zip stand-collar table (image 13 of 1083898601268, half chest doubled). Neither
# publishes hip or waist.
SRM_CF_BUTTON_CHART = {
    "Child 10": ("10 (110-120 cm)", "Child 5-6 Years", "KID56Y", "5-6", 50, 82, 37, 68, "-", "-"),
    "Child 12": ("12 (120-130 cm)", "Child 7 Years", "KID7Y", "7", 53, 86, 40, 74, "-", "-"),
    "Child 14": ("14 (125-135 cm)", "Child 8-9 Years", "KID89Y", "8-9", 56, 90, 43, 79, "-", "-"),
    "Child 16": ("16 (135-145 cm)", "Child 10-11 Years", "KID1011Y", "10-11", 60, 94, 46, 84, "-", "-"),
    "Mom S": ("Womens S", "Mother S", "S", "—", 63, 98, 49, 91, "-", "-"),
    "Mom M": ("Womens M", "Mother M", "M", "—", 65, 102, 52, 94, "-", "-"),
    "Mom L": ("Womens L", "Mother L", "L", "—", 68, 106, 54, 97, "-", "-"),
    "Mom XL": ("Womens XL", "Mother XL", "XL", "—", 71, 110, 56, 100, "-", "-"),
}
SRM_CF_ZIP_CHART = {
    "Child 10": ("10 (110-120 cm)", "Child 5-6 Years", "KID56Y", "5-6", 48, 80, 36, 66, "-", "-"),
    "Child 12": ("12 (120-130 cm)", "Child 7 Years", "KID7Y", "7", 51, 84, 39, 72, "-", "-"),
    "Child 14": ("14 (125-135 cm)", "Child 8-9 Years", "KID89Y", "8-9", 54, 88, 42, 78, "-", "-"),
    "Child 16": ("16 (135-145 cm)", "Child 10-11 Years", "KID1011Y", "10-11", 58, 92, 45, 84, "-", "-"),
    "Mom S": ("Womens S", "Mother S", "S", "—", 61, 96, 48, 91, "-", "-"),
    "Mom M": ("Womens M", "Mother M", "M", "—", 63, 102, 51, 94, "-", "-"),
    "Mom L": ("Womens L", "Mother L", "L", "—", 66, 106, 53, 97, "-", "-"),
    "Mom XL": ("Womens XL", "Mother XL", "XL", "—", 69, 110, 55, 100, "-", "-"),
}
# 衣林 dog vest sold with the Blue Plaid Reindeer print (offer 1029357235756): the
# supplier's 狗狗尺寸表 (description image 03). Back length -> garment length, bust ->
# chest; neck (collar) is listed per size in the size-range sentence.
YILIN_DOG_CHART = {
    "Dog S": ("Dog S", "Dog S", "DOGS", "—", 44, 55, "-", "-", "-", "-"),
    "Dog M": ("Dog M", "Dog M", "DOGM", "—", 52, 71, "-", "-", "-", "-"),
    "Dog L": ("Dog L", "Dog L", "DOGL", "—", 65, 84, "-", "-", "-", "-"),
    "Dog XL": ("Dog XL", "Dog XL", "DOGXL", "—", 77, 97, "-", "-", "-", "-"),
    "Dog 2XL": ("Dog 2XL", "Dog 2XL", "DOG2XL", "—", 90, 111, "-", "-", "-", "-"),
}
YILIN_DOG_NECK = {"Dog S": 36, "Dog M": 51, "Dog L": 61, "Dog XL": 71, "Dog 2XL": 81}
if SPEC.get("chart_table") == "yilin_dog":
    CHART_TABLE = YILIN_DOG_CHART
if SPEC.get("chart_table") == "stq_sweat":
    CHART_TABLE = STQ_SWEAT_CHART
elif SPEC.get("chart_table") == "srm_cf_button":
    CHART_TABLE = SRM_CF_BUTTON_CHART
elif SPEC.get("chart_table") == "srm_cf_zip":
    CHART_TABLE = SRM_CF_ZIP_CHART
NO_HIP = SPEC.get("chart_table") in ("stq_sweat", "srm_cf_button", "srm_cf_zip")
FIT_TABLE = {"shirumeng": SHIRUMENG_FIT, "stq_sweat": STQ_SWEAT_FIT, "srm_cf_button": SHIRUMENG_FIT,
             "srm_cf_zip": SHIRUMENG_FIT}.get(SPEC.get("chart_table"), {})
# Charts that publish one relaxed waist figure instead of a relaxed-stretched range.
WAIST_SINGLE = CHART_TABLE is not FACTORY_CHART


def chart_row(vendor_label: str) -> dict:
    chart_label, picker, suffix, age, length, chest, sleeve, pant, waist, hip = CHART_TABLE[vendor_label]
    audience = ("pet" if vendor_label.startswith("Dog") else
                "child" if (vendor_label.startswith(("Children", "Child")) or vendor_label.endswith("T")) else
                "mother" if vendor_label.startswith(("Mom", "Mother")) else
                "adult" if vendor_label.startswith("Adult") else "father")
    return {
        "audience": audience,
        "role": ROLE_BY_AUDIENCE[audience],
        "garment": "Sweatshirt" if SW else ("Dog Vest" if PET else "Pajama Set"),
        "vendor_label": vendor_label,
        "chart_label": chart_label,
        "picker_label": picker,
        "sku_suffix": suffix,
        "age": age,
        # The chart publishes no wearer weight. Its child size codes (80-160)
        # sit beside T labels that disagree with typical heights for those
        # ages, so no wearer height is claimed.
        "weight": FIT_TABLE.get(vendor_label, ("-", "-"))[1],
        "height": FIT_TABLE.get(vendor_label, ("-", "-"))[0],
        "chest_cm": chest,
        "hip_cm": hip,
        "waist_cm": waist,
        "length_cm": length,
        "sleeve_cm": sleeve,
        "pant_cm": pant,
    }


# One row per purchasable vendor SKU that also has a factory-chart row, in
# child -> mother -> father order.
SIZE_CHART = [chart_row(label) for label in SPEC["vendor_size_labels"]]
EXPECTED_VENDOR_LABELS = list(SPEC["vendor_size_labels"])
SIZE_MAP = {k: v for k, v in SIZE_MAP_ALL.items() if k in {r["picker_label"] for r in SIZE_CHART}}
NO_HONEST_SIZE_MATCH = {k for k in NO_HONEST_SIZE_MATCH_ALL if k in {r["picker_label"] for r in SIZE_CHART}}


# ---------------------------------------------------------------------------
# Shopper copy. Every sentence except the design slots (print sentence and one
# key feature) is shared across the 2026 Christmas pajama line, so validated
# translations can be reused. Variant keys select the honest shared sentence.
# Avoid words containing "son"/"person" (translation role-detection bug).
# ---------------------------------------------------------------------------
FABRIC_TEXT = {
    "polyester": "Soft, cotton-feel knit made of 100% polyester.",
    "polyblend": "Soft knit with an 80% polyester main fabric.",
    "poly95": "Soft knit with a 95% polyester main fabric.",
    "cotton": "Soft knit with a 95% cotton main fabric.",
    "cvc": "Soft knit blend of 35% cotton and 65% polyester.",
    "cotton35": "Soft cotton-blend knit with 35% cotton in the main fabric.",
    "cotton65": "Soft cotton-blend knit with 65% cotton in the main fabric.",
    "poly_velvet": "Soft brushed velvet knit made of 100% polyester.",
    "cotton_sweat": "Soft cotton sweatshirt knit.",
    "coral_fleece": "Thick, plush coral fleece made of polyester.",
}
FABRIC_FEATURE = {
    "polyester": ("Soft knit:", "A cotton-feel polyester knit for cozy winter bedtimes."),
    "polyblend": ("Soft knit:", "A soft polyester-blend knit for cozy winter bedtimes."),
    "poly95": ("Soft knit:", "A cotton-feel polyester knit for cozy winter bedtimes."),
    "cotton": ("Soft knit:", "A cotton-rich knit for cozy winter bedtimes."),
    "cvc": ("Soft knit:", "A soft cotton-blend knit for cozy winter bedtimes."),
    "cotton35": ("Soft knit:", "A soft cotton-blend knit for cozy winter bedtimes."),
    "cotton65": ("Soft knit:", "A soft cotton-blend knit for cozy winter bedtimes."),
    "poly_velvet": ("Soft knit:", "A soft brushed velvet knit that keeps the chill off on winter nights."),
    "cotton_sweat": ("Soft knit:", "A soft cotton knit for cozy holiday days."),
    "coral_fleece": ("Soft knit:", "Thick, plush fleece that keeps moms and kids warm on cold winter nights."),
}
if PET:  # the family fabric sentence stays; the feature line speaks about the dog
    FABRIC_FEATURE = dict(FABRIC_FEATURE, cotton65=("Soft knit:", "The same soft cotton-blend knit as the family set."))
FABRIC_SEO = {
    "polyester": "soft polyester knit",
    "polyblend": "soft polyester-blend knit",
    "poly95": "soft polyester knit",
    "cotton": "soft cotton knit",
    "cvc": "soft cotton-blend knit",
    "cotton35": "soft cotton-blend knit",
    "cotton65": "soft cotton-blend knit",
    "poly_velvet": "soft brushed velvet knit",
    "cotton_sweat": "soft cotton knit",
    "coral_fleece": "plush coral fleece",
}
DESIGN_TEXT = {
    "crew_trim": "Long-sleeve crew-neck top with a contrast neckline trim, plus full-length pants with an elastic waist.",
    "crew_plain": "Long-sleeve crew-neck top, plus full-length pants with an elastic waist.",
    "raglan": "Long-sleeve crew-neck top with contrast raglan sleeves, plus full-length pants with an elastic waist.",
    "cuffed": "Long-sleeve crew-neck top with ribbed cuffs, plus full-length pants with an elastic waist and cuffed ankles.",
    "short_crew": "Short-sleeve crew-neck top, plus full-length pants with an elastic waist.",
    "button": "Long-sleeve button-front top with a notched collar, plus full-length pants with an elastic waist.",
    "trim_cuffed": "Long-sleeve top with contrast trim at the neckline and cuffs, plus full-length pants with an elastic waist and cuffed ankles.",
    "button_peter": "Long-sleeve button-front top with a rounded Peter Pan collar, plus full-length pants with an elastic waist.",
    "button_lace": "Long-sleeve button-front top with a lace Peter Pan collar, plus full-length pants with an elastic waist.",
    "crew_sweatshirt": "Long-sleeve crewneck sweatshirt with a ribbed neckline, cuffs, and hem.",
    "zip_stand": "Long-sleeve zip-up top with a stand collar and two front pockets, plus full-length pants with an elastic waist and gathered ankles.",
    "button_round": "Long-sleeve button-front top with a round neckline, plus full-length pants with an elastic waist and gathered ankles.",
    "button_lace_fleece": "Long-sleeve button-front top with a lace-trimmed collar and pocket, plus full-length pants with an elastic waist.",
    "dog_vest": "Sleeveless dog vest with black binding at the neck, leg openings, and curved hem, and small snap closures down the center.",
}
SHARED_EN = {
    "fab_label": "Fabric:",
    "fam_label": "Family story:",
    "fam_text": "One cozy Christmas pajama look for mom, dad, and the kids, made for tree trimming, Christmas morning, and family photos.",
    "prt_label": "Print:",
    "des_label": "Design details:",
    "care_label": "Care:",
    "care_text": "Follow the care label sewn into each garment.",
    "size_label": "Size range:",
    "h3_chart": "Size Chart - Pajama Set",
    "th": ["Size", "Age", "Weight (kg)", "Height (cm)", "Chest/Bust (cm)", "Sleeve (cm)",
           "Pant/Short (cm)", "Hip (cm)", "Waist (cm)", "Garment Length (cm)"],
    "p1": "The whole family can wear the same Christmas pajama set, with child, women's, and men's sizes. Pick a size for each family member separately to build your matching look.",
    "p2": (
        "Each size is one two-piece set with a top and pants. Garment length is the "
        "top length; pant length is the full pants length. The waist is elastic, so "
        "it is shown as a relaxed-to-stretched range. Measurements are approximate, "
        "so compare chest, waist, and lengths with pajamas that fit well today."
    ),
    "p2_single": (
        "Each size is one two-piece set with a top and pants. Garment length is the "
        "top length; pant length is the full pants length. The waist is elastic; the "
        "chart shows the relaxed waist measurement. Measurements are approximate, "
        "so compare chest, waist, and lengths with pajamas that fit well today."
    ),
    "fam_text_mm": "One cozy pajama look for mom and her little girl, made for slow weekend mornings, bedtime stories, and matching photos.",
    "p1_mm": "Mom and daughter can wear the same pajama set, with child and women's sizes. Pick a size for each of you separately to build your matching look.",
    "p2_mm": (
        "Each size is one two-piece set with a top and pants. Garment length is the "
        "top length; pant length is the full pants length. The waist is elastic. Height "
        "and weight are a general fit guide, and child ages are typical for those "
        "heights. Measurements are approximate, so compare chest and lengths with "
        "pajamas that fit well today."
    ),
    "kf1_text_mm": "The same pajama set in child sizes plus a women's cut.",
    "kf4_text_mm": "Coordinated colors made for mommy-and-me photos.",
    "cta_mm": "Choose the sizes you need for cozy matching nights at home.",
    "kf1_label_mm": "Mom-and-daughter match:",
    "fam_text_sw": "One cozy Christmas look for mom, dad, and the kids, made for tree trimming, holiday outings, and family photos.",
    "p1_sw": "The whole family can wear the same Christmas sweatshirt, with child and adult sizes. Pick a size for each family member separately to build your matching look.",
    "p2_sw": (
        "Each size is one crewneck sweatshirt; the pants in the photos are not included. "
        "Chest is the full chest measurement and garment length is the top length. Height "
        "and weight are a general fit guide, and child ages are typical for those heights. "
        "Measurements are approximate, so compare with a sweatshirt that fits well today."
    ),
    "kf1_text_sw": "The same Christmas sweatshirt in child and adult sizes.",
    "h3_chart_sw": "Size Chart - Sweatshirt",
    "fam_text_pet": "The family dog's piece of the matching Christmas look, cut from the same plaid as the family pajama pants.",
    "p1_pet": "Pair it with the matching family pajama set, sold separately, so everyone in the Christmas photo matches. Pick the size from your dog's measurements.",
    "p2_pet": (
        "Back length runs from the base of the neck to the base of the tail; bust is the "
        "chest around the widest part. Measure your dog and compare with the chart; "
        "measurements are approximate."
    ),
    "kf1_label_pet": "Matches the family:",
    "kf1_text_pet": "The same plaid as the family pajama pants for an all-together Christmas photo.",
    "kf5_label_pet": "Dog sizes:",
    "cta_pet": "Pick your dog's size to complete the family Christmas photo.",
    "h3_chart_pet": "Size Chart - Dog Vest",
    "kf5_label_mm": "Full size range:",
    "h3_kf": "Key Features:",
    "kf1_label": "Whole-family match:",
    "kf1_text": "The same Christmas pajama set in child sizes plus women's and men's cuts.",
    "kf4_label": "Photo-ready:",
    "kf4_text": "Coordinated colors made for Christmas cards and holiday photos.",
    "kf5_label": "Full family size range:",
    "cta": "Choose the sizes you need for a cozy family Christmas.",
}
NUMBER_WORDS = {4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine"}


AUDIENCES = ("pet",) if PET else (("child", "mother") if MM else (("child", "adult") if SW else ("child", "mother", "father")))


def size_key() -> str:
    first_last = {}
    for aud in AUDIENCES:
        rows = [r for r in SIZE_CHART if r["audience"] == aud]
        first_last[aud] = (rows[0]["picker_label"], rows[-1]["picker_label"], len(rows))
    return "|".join(f"{a}:{f}>{l}:{n}" for a, (f, l, n) in first_last.items())


def size_range_phrase() -> str:
    c = [r for r in SIZE_CHART if r["audience"] == "child"]
    m = [r for r in SIZE_CHART if r["audience"] == "mother"]
    f = [r for r in SIZE_CHART if r["audience"] == "father"]
    a = [r for r in SIZE_CHART if r["audience"] == "adult"]
    if PET:
        return (f"{SIZE_CHART[0]['picker_label']} through {SIZE_CHART[-1]['picker_label']}. Neck: "
                + ", ".join(f"{r['sku_suffix'].replace('DOG', '')} {YILIN_DOG_NECK[r['vendor_label']]} cm" for r in SIZE_CHART) + ".")
    if SW:
        return (f"{c[0]['picker_label']} through {c[-1]['picker_label']}, and "
                f"{a[0]['picker_label']} through {a[-1]['picker_label']}.")
    if MM:
        return (f"{c[0]['picker_label']} through {c[-1]['picker_label']}, and "
                f"{m[0]['picker_label']} through {m[-1]['picker_label']}.")
    return (
        f"{c[0]['picker_label']} through {c[-1]['picker_label']}, "
        f"{m[0]['picker_label']} through {m[-1]['picker_label']}, and "
        f"{f[0]['picker_label']} through {f[-1]['picker_label']}."
    )


def counts_phrase() -> str:
    n = {a: sum(1 for r in SIZE_CHART if r["audience"] == a) for a in ("child", "mother", "father", "adult", "pet")}
    if PET:
        return f"{NUMBER_WORDS[n['pet']].capitalize()} dog sizes; see the size chart for back length and bust."
    if SW:
        return (f"{NUMBER_WORDS[n['child']].capitalize()} child sizes and {NUMBER_WORDS[n['adult']]} adult sizes; "
                "see the size chart for measurements.")
    if MM:
        return (f"{NUMBER_WORDS[n['child']].capitalize()} child sizes and {NUMBER_WORDS[n['mother']]} women's sizes; "
                "see the size chart for measurements.")
    return (
        f"{NUMBER_WORDS[n['child']].capitalize()} child sizes, {NUMBER_WORDS[n['mother']]} women's sizes, "
        f"and {NUMBER_WORDS[n['father']]} men's sizes; see the size chart for measurements."
    )


def size_short() -> str:
    if PET:
        return f"Dog {SIZE_CHART[0]['sku_suffix'][3:]}–{SIZE_CHART[-1]['sku_suffix'][3:]}."
    c = [r for r in SIZE_CHART if r["audience"] == "child"]
    m = [r for r in SIZE_CHART if r["audience"] == "mother"]
    f = [r for r in SIZE_CHART if r["audience"] == "father"]
    c0 = c[0]["picker_label"].replace("Child ", "").replace(" Years", "")
    c1 = c[-1]["picker_label"].replace("Child ", "").replace(" Years", "")
    if SW:
        a = [r for r in SIZE_CHART if r["audience"] == "adult"]
        return f"{c[0]['picker_label']} to {c1} Years, Adult {a[0]['sku_suffix']}–{a[-1]['sku_suffix']}."
    if MM:
        return f"Child {c0} to {c1} Years, Mother {m[0]['sku_suffix']}–{m[-1]['sku_suffix']}."
    return (
        f"Child {c0}–{c1} Years, Mother {m[0]['sku_suffix']}–{m[-1]['sku_suffix']}, "
        f"Father {f[0]['sku_suffix']}–{f[-1]['sku_suffix']}."
    )


def en_segments() -> dict:
    fabric = SPEC["fabric_key"]
    seg = dict(SHARED_EN)
    seg.update({
        "fab_text": FABRIC_TEXT[fabric],
        "prt_text": SPEC["print_sentence"],
        "des_text": DESIGN_TEXT[SPEC["design_key"]],
        "size_text": size_range_phrase(),
        "kf2_label": SPEC["feature_label"],
        "kf2_text": SPEC["feature_text"],
        "kf3_label": FABRIC_FEATURE[fabric][0],
        "kf3_text": FABRIC_FEATURE[fabric][1],
        "kf5_text": counts_phrase(),
    })
    if WAIST_SINGLE:
        seg["p2"] = SHARED_EN["p2_single"]
    if MM:
        for key in ("fam_text", "p1", "p2", "kf1_text", "kf4_text", "cta", "kf1_label", "kf5_label"):
            seg[key] = SHARED_EN[key + "_mm"]
    if SW:
        for key in ("fam_text", "p1", "p2", "kf1_text", "h3_chart"):
            seg[key] = SHARED_EN[key + "_sw"]
    if PET:
        for key in ("fam_text", "p1", "p2", "kf1_label", "kf1_text", "kf5_label", "cta", "h3_chart"):
            seg[key] = SHARED_EN[key + "_pet"]
    return seg


if PET:
    TITLE_TEMPLATE = "{P} Matching Dog Vest — Christmas Plaid"
    SEO_TITLE_TEMPLATE = "{P} Matching Dog Vest | Dress Like Mommy"
    SEO_DESCRIPTION_TEMPLATE = "{P}: a matching Christmas plaid vest for the family dog in {FABRIC}. {SIZES}"
elif SW:
    TITLE_TEMPLATE = "{P} Family Matching Sweatshirts — Christmas Crewneck"
    SEO_TITLE_TEMPLATE = "{P} Christmas Sweatshirts | Dress Like Mommy"
    SEO_DESCRIPTION_TEMPLATE = "{P}: matching Christmas sweatshirts for mom, dad, girls & boys in {FABRIC}. {SIZES}"
elif MM and SPEC.get("title_variant") == "fleece":
    TITLE_TEMPLATE = "{P} Mommy and Me Pajamas — Fleece Set"
    SEO_TITLE_TEMPLATE = "{P} Mommy & Me Fleece Pajamas | Dress Like Mommy"
    SEO_DESCRIPTION_TEMPLATE = "{P}: matching mommy-and-me fleece pajamas for mom and daughter in {FABRIC}. {SIZES}"
elif MM:
    TITLE_TEMPLATE = "{P} Mommy and Me Pajamas — Button-Up Set"
    SEO_TITLE_TEMPLATE = "{P} Mommy & Me Pajamas | Dress Like Mommy"
    SEO_DESCRIPTION_TEMPLATE = "{P}: matching mommy-and-me pajamas for mom and daughter in {FABRIC}. {SIZES}"
else:
    TITLE_TEMPLATE = "{P} Family Matching Pajamas — Christmas Set"
    SEO_TITLE_TEMPLATE = "{P} Family Pajamas | Dress Like Mommy"
    SEO_DESCRIPTION_TEMPLATE = "{P}: matching Christmas pajamas for mom, dad, girls & boys in {FABRIC}. {SIZES}"
TITLE = TITLE_TEMPLATE.format(P=PRINT_NAME)
SEO_TITLE = SEO_TITLE_TEMPLATE.format(P=PRINT_NAME)
SEO_DESCRIPTION = SEO_DESCRIPTION_TEMPLATE.format(P=PRINT_NAME, FABRIC=FABRIC_SEO[SPEC["fabric_key"]], SIZES=size_short())


def gql(query: str, variables: dict | None = None) -> dict:
    response = requests.post(
        API,
        headers={"X-Shopify-Access-Token": TOKEN, "Content-Type": "application/json"},
        json={"query": query, "variables": variables or {}},
        timeout=90,
    )
    response.raise_for_status()
    data = response.json()
    if data.get("errors"):
        raise RuntimeError("GraphQL errors: " + json.dumps(data["errors"], ensure_ascii=False))
    return data


def require_no_user_errors(data: dict, path: list[str]) -> None:
    current = data
    for key in path:
        current = current[key]
    if current:
        raise RuntimeError(json.dumps(current, indent=2, ensure_ascii=False))


def money(value: Decimal | str) -> str:
    return f"{Decimal(str(value)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP):.2f}"


def cost_for(price: str) -> str:
    return money(Decimal(price) * Decimal("0.50"))


def compare_at(price: str) -> str:
    # Owner rule (BuckyDrop pricing): compare-at = sale price + $10.
    return money(Decimal(price) + Decimal("10"))


def metric_cell(value, unit: str) -> str:
    text = str(value if value is not None else "").strip()
    if not text or text in {"-", "—", "--"}:
        return "-"
    return f"{text.replace('-', '–')} {unit}" if re.fullmatch(r"\d+(\.\d+)?-\d+(\.\d+)?", text) else f"{text} {unit}"


def role_token(row: dict) -> str:
    return {"Child Pajama Set": "KID", "Mother Pajama Set": "MOM", "Father Pajama Set": "DAD",
            "Child Sweatshirt": "KID", "Adult Sweatshirt": "ADT", "Dog Vest": "PET"}[row["role"]]


def price_for(row: dict) -> str:
    return CHILD_PRICE if row["audience"] == "child" else ADULT_PRICE


def sku_for(row: dict, color_name: str) -> str:
    return f"DLM-{SHORTCODE}-{role_token(row)}-{row['sku_suffix']}-{COLOR_TOKEN_BY_NAME[color_name]}"


def mapped_size_rows() -> list[tuple[str, str, str]]:
    return [(r["picker_label"], *SIZE_MAP[r["picker_label"]]) for r in SIZE_CHART if r["picker_label"] in SIZE_MAP]


def unique_size_refs() -> list[str]:
    return list(dict.fromkeys(gid for _, gid, _ in mapped_size_rows()))


def build_tags() -> list[str]:
    if PET:  # no "Christmas Pajamas": that tag feeds /collections/couples
        values = ["Christmas", "Christmas Pet", "Pet", "Dog", "Dog Clothes", "Pet Apparel",
                  "Matching Family Pet", "Holiday", "Winter", "Family Photos", PRINT_NAME, *SPEC["extra_tags"]]
        values.extend(r["picker_label"] for r in SIZE_CHART)
        return sorted(dict.fromkeys(values))
    if SW:
        values = [
            "Family Matching", "Mommy and Me", "Daddy and Me", "Christmas", "Christmas Sweaters",
            "Christmas Tops", "Christmas Sweatshirts", "Sweatshirts", "Family Sweatshirts",
            "Matching Family Sweatshirts", "Matching Family Tops", "Matching Family Outfits", "Tops",
            "Crewneck Sweatshirt", "Child Sweatshirt", "Adult Sweatshirt", "Long Sleeve Top",
            "Holiday", "Winter", "Family Photos", PRINT_NAME, *SPEC["extra_tags"],
        ]
        values.extend(r["picker_label"] for r in SIZE_CHART)
        return sorted(dict.fromkeys(values))
    if MM:
        values = [
            "Mommy and Me", "Mommy and Me Pajamas", "Mother Daughter", "Pajamas",
            "Matching Family Pajamas", "Two-Piece Pajama Set", "Pajama Set",
            "Child Pajama Set", "Mother Pajama Set", f"{SLEEVE_STYLE} Pajamas",
            "Winter", "Winter Pajamas", PRINT_NAME,
            *SPEC["extra_tags"],
        ]
        values.extend(r["picker_label"] for r in SIZE_CHART)
        return sorted(dict.fromkeys(values))
    values = [
        "Family Matching", "Mommy and Me", "Daddy and Me", "Pajamas",
        "Matching Family Pajamas", "Family Pajamas", "Matching Family Outfits",
        "Two-Piece Pajama Set", "Pajama Set", "Child Pajama Set",
        "Mother Pajama Set", "Father Pajama Set", f"{SLEEVE_STYLE} Pajamas",
        "Christmas", "Christmas Pajamas", "Family Christmas Pajamas",
        "Holiday Pajamas", "Winter", "Family Photos", PRINT_NAME,
        *SPEC["extra_tags"],
    ]
    values.extend(r["picker_label"] for r in SIZE_CHART)
    return sorted(dict.fromkeys(values))


def table_cells(row: dict) -> list[str]:
    return [
        row["picker_label"],
        row["age"] if row["audience"] == "child" else "-",
        metric_cell(row["weight"], "kg"),
        metric_cell(row["height"], "cm"),
        metric_cell(row["chest_cm"], "cm"),
        metric_cell(row["sleeve_cm"], "cm"),
        metric_cell(row["pant_cm"], "cm"),
        metric_cell(row["hip_cm"], "cm"),
        metric_cell(row["waist_cm"], "cm"),
        metric_cell(row["length_cm"], "cm"),
    ]


def build_body_from(seg: dict) -> str:
    """Render the body in the exact form Shopify stores (one <td> per line,
    a newline after <li>), so translation cache keys match the stored body."""
    esc = lambda text: html.escape(text, quote=False)

    def li(label_key: str, text_key: str) -> str:
        return f"<li>\n<strong>{esc(seg[label_key])}</strong> {esc(seg[text_key])}</li>"

    rows = []
    for row in SIZE_CHART:
        rows.append("<tr>\n" + "\n".join(f"<td>{esc(str(c))}</td>" for c in table_cells(row)) + "\n</tr>")
    return "\n".join([
        "<ul>",
        li("fab_label", "fab_text"), li("fam_label", "fam_text"), li("prt_label", "prt_text"),
        li("des_label", "des_text"), li("care_label", "care_text"), li("size_label", "size_text"),
        "</ul>", "",
        f"<h3>{esc(seg['h3_chart'])}</h3>",
        '<table id="size-chart" class="size-chart">',
        "<thead><tr>", *[f"<th>{esc(h)}</th>" for h in seg["th"]], "</tr></thead>",
        "<tbody>", *rows, "</tbody>", "</table>", "",
        f"<p>{esc(seg['p1'])}</p>", "",
        f"<p>{esc(seg['p2'])}</p>", "",
        f"<h3>{esc(seg['h3_kf'])}</h3>", "<ul>",
        li("kf1_label", "kf1_text"), li("kf2_label", "kf2_text"), li("kf3_label", "kf3_text"),
        li("kf4_label", "kf4_text"), li("kf5_label", "kf5_text"),
        "</ul>", "",
        f"<p>{esc(seg['cta'])}</p>",
    ])


def build_body() -> str:
    return build_body_from(en_segments())


KEY_FEATURES = ["kf1", "kf2", "kf3", "kf4", "kf5"]


def build_variants() -> list[dict]:
    variants = []
    for row in SIZE_CHART:
        price = price_for(row)
        for color_name in COLOR_NAMES:
            variants.append({
                "price": price,
                "compareAtPrice": compare_at(price),
                "taxable": True,
                "inventoryPolicy": "DENY",
                "optionValues": [
                    {"optionName": "Size", "name": row["picker_label"]},
                    {"optionName": "Color", "name": color_name},
                ],
                "inventoryItem": {
                    "sku": sku_for(row, color_name),
                    "cost": cost_for(price),
                    "tracked": True,
                    "requiresShipping": True,
                },
            })
    return variants


SUBCATEGORY2 = "Christmas Pet" if PET else ("Christmas Sweatshirts" if SW else ("Winter Pajamas" if MM else "Christmas Pajamas"))
STYLE_VALUE = "Dog Vest" if PET else ("Crewneck Sweatshirt" if SW else f"{SLEEVE_STYLE} Knit Pajama Set")
TYPE_VALUE = "Dog Vest" if PET else ("Crewneck Sweatshirt" if SW else "Two-Piece Pajama Set")
LABEL3 = "Dog Vest" if PET else ("Crewneck Sweatshirt" if SW else f"{SLEEVE_STYLE} Pajama Set")
GOOGLE_GENDER = "female" if MM else "unisex"
LABEL2 = "Winter Pajamas" if MM else "Christmas"
LABEL4 = "Christmas Pet" if PET else ("Family Christmas Sweatshirts" if SW else ("Mommy and Me Pajamas" if MM else "Family Christmas Pajamas"))


def mf(product_id: str, namespace: str, key: str, type_: str, value: str) -> dict:
    return {"ownerId": product_id, "namespace": namespace, "key": key, "type": type_, "value": value}


def build_metafields(product_id: str) -> list[dict]:
    text = "single_line_text_field"
    refs = "list.metaobject_reference"
    return [
        mf(product_id, "custom", "category1", text, LISTING_MODE),
        mf(product_id, "custom", "subcategory", text, "Family Sweatshirts" if SW else ("Pet Apparel" if PET else "Pajamas")),
        mf(product_id, "custom", "subcategory2", text, SUBCATEGORY2),
        mf(product_id, "custom", "pattern", text, PRINT_NAME),
        mf(product_id, "custom", "style", text, STYLE_VALUE),
        mf(product_id, "custom", "type", text, TYPE_VALUE),
        mf(product_id, "mm-google-shopping", "custom_product", "boolean", "false"),
        mf(product_id, "mm-google-shopping", "gender", text, GOOGLE_GENDER),
        mf(product_id, "mm-google-shopping", "age_group", text, "adult"),
        mf(product_id, "mm-google-shopping", "condition", text, "new"),
        mf(product_id, "mm-google-shopping", "custom_label_0", text, LISTING_MODE),
        mf(product_id, "mm-google-shopping", "custom_label_1", text, PRINT_NAME),
        mf(product_id, "mm-google-shopping", "custom_label_2", text, LABEL2),
        mf(product_id, "mm-google-shopping", "custom_label_3", text, LABEL3),
        mf(product_id, "mm-google-shopping", "custom_label_4", text, LABEL4),
        *([] if PET else [mf(product_id, "shopify", "age-group", refs, json.dumps([AGE_GROUP_GIDS["child"], AGE_GROUP_GIDS["adult"]]))]),
        mf(product_id, "shopify", "color-pattern", refs, json.dumps(COLOR_PATTERN_GIDS)),
        mf(product_id, "shopify", "fabric", refs, json.dumps(FABRIC_GIDS)),
        *([] if PET else [mf(product_id, "shopify", "size", refs, json.dumps(unique_size_refs()))]),
        *([] if PET else [mf(product_id, "shopify", "target-gender", refs, json.dumps(TARGET_GENDER_GIDS))]),  # not defined for Pet Shirts
        mf(product_id, "global", "title_tag", text, SEO_TITLE),
        mf(product_id, "global", "description_tag", text, SEO_DESCRIPTION),
    ]


SKIPPED_METAFIELDS = [
    ("shopify.sleeve-length-type", "The store has only Sleeveless/Short sleeve-length metaobjects; sleeve style is described in the body."),
    ("shopify.neckline", "Repo pajama precedent reserves neckline for Dresses/Tops, not Pajamas (crew neck is described in the body)."),
    ("shopify.top-length-type", "Not applicable to a two-piece pajama set."),
    ("shopify.dress-occasion", "Not applicable to a pajama set."),
    ("shopify.dress-style", "Not applicable to a pajama set."),
    ("shopify.skirt-dress-length-type", "Not applicable to a pajama set."),
]


def table_parts(body: str) -> tuple[list[str], list[list[str]]]:
    table_match = re.search(r"<table id=\"size-chart\"[^>]*>.*?</table>", body, re.S)
    table = table_match.group(0) if table_match else ""
    headers = [re.sub(r"<[^>]+>", "", v).strip() for v in re.findall(r"<th>(.*?)</th>", table, re.S)]
    tbody_match = re.search(r"<tbody>(.*?)</tbody>", table, re.S)
    tbody = tbody_match.group(1) if tbody_match else ""
    rows = [
        [html.unescape(re.sub(r"<[^>]+>", "", c)).strip() for c in re.findall(r"<td>(.*?)</td>", r, re.S)]
        for r in re.findall(r"<tr>(.*?)</tr>", tbody, re.S)
    ]
    return headers, rows


def shopper_payload(body: str, tags: list[str], metafields: list[dict] | None = None) -> str:
    parts = [TITLE, SEO_TITLE, SEO_DESCRIPTION, body, PRODUCT_TYPE, VENDOR, ", ".join(tags), MEDIA_ALT]
    if metafields:
        parts.extend(item["value"] for item in metafields)
    return "\n".join(parts).lower()


BLOCKED_TERMS = (
    "1688", "alibaba", "taobao", "supplier", "vendor", "smr", "赛美人",
    "grinch", "stitch", "disney", "rudolph", "chart-backed", "transcribed",
    "supplied", "attached", "this draft", "source row", "person's", "season",
    *[str(code).lower() for code in SPEC["vendor_codes"]],
)


def source_leak_errors(payload: str) -> list[str]:
    errors = []
    if re.search(r"(?:https?://|www\.)", payload, re.I):
        errors.append("URL-like text found in shopper/feed payload")
    scrubbed = payload.replace(VENDOR, "")
    for term in BLOCKED_TERMS:
        if term and term in scrubbed:
            errors.append(f"blocked source/trademark/wording term in shopper payload: {term}")
    return errors


def validate_preflight(body: str, variants: list[dict]) -> None:
    errors = []
    required = {"audience", "role", "garment", "vendor_label", "picker_label", "sku_suffix", "age",
                "weight", "height", "chest_cm", "hip_cm", "waist_cm", "length_cm", "sleeve_cm", "pant_cm"}
    expected_variant_count = len(SIZE_CHART) * len(COLORS)
    if len(variants) != expected_variant_count:
        errors.append(f"variants {len(variants)} != SIZE_CHART x colors {expected_variant_count}")
    if [r["vendor_label"] for r in SIZE_CHART] != EXPECTED_VENDOR_LABELS:
        errors.append("SIZE_CHART rows do not match the vendor SKU labels in order")
    unknown = [label for label in SPEC["vendor_size_labels"] if label not in CHART_TABLE]
    if unknown:
        errors.append("vendor labels without a factory-chart row: " + ", ".join(unknown))
    if any(label.lower().startswith(("baby",) if PET else ("baby", "dog")) for label in SPEC["vendor_size_labels"]):
        errors.append("baby/dog row present in SIZE_CHART")
    if PET and not all(label.startswith("Dog") for label in SPEC["vendor_size_labels"]):
        errors.append("pet listing must contain dog rows only")
    audiences = [r["audience"] for r in SIZE_CHART]
    if audiences != sorted(audiences, key=list(AUDIENCES).index) or set(audiences) != set(AUDIENCES):
        errors.append(f"SIZE_CHART must list {', '.join(AUDIENCES)} rows in order")
    for row in SIZE_CHART:
        missing = [f for f in required if f not in row or row[f] in (None, "")]
        if missing:
            errors.append(f"{row.get('vendor_label')} missing {missing}")
        for field in (("chest_cm", "length_cm") if PET else ("chest_cm", "length_cm", "sleeve_cm") if SW else
                      ("chest_cm", "length_cm", "sleeve_cm", "pant_cm") if NO_HIP else
                      ("chest_cm", "length_cm", "sleeve_cm", "pant_cm", "hip_cm")):
            if not isinstance(row[field], (int, float)) or row[field] <= 0:
                errors.append(f"{row['vendor_label']} lacks positive source {field}")
        if PET:
            continue
        if FIT_TABLE:
            if row["waist_cm"] != "-":
                errors.append(f"{row['vendor_label']} waist is not published by this chart")
            if (row["height"], row["weight"]) != FIT_TABLE[row["vendor_label"]]:
                errors.append(f"{row['vendor_label']} height/weight differ from the supplier fit guide")
            continue
        if not re.fullmatch(r"\d+-\d+" if CHART_TABLE is FACTORY_CHART else r"\d+(-\d+)?", str(row["waist_cm"])):
            errors.append(f"{row['vendor_label']} waist is not the published elastic range")
        for field in ("weight", "height"):
            if row[field] != "-":
                errors.append(f"{row['vendor_label']} invents source-omitted {field}")
    if len({(r["role"], r["picker_label"]) for r in SIZE_CHART}) != len(SIZE_CHART):
        errors.append("duplicate role/picker pair")
    if len({r["picker_label"] for r in SIZE_CHART}) != len(SIZE_CHART):
        errors.append("duplicate Size option value")
    if len(TITLE) > 70:
        errors.append(f"title too long: {len(TITLE)}")
    if len(SEO_TITLE) > 60:
        errors.append(f"SEO title too long: {len(SEO_TITLE)}")
    if SEO_TITLE == TITLE:
        errors.append("SEO title must differ from title")
    if len(SEO_DESCRIPTION) > 155:
        errors.append(f"SEO description too long: {len(SEO_DESCRIPTION)}")
    if len(HANDLE) > 60:
        errors.append(f"handle too long: {len(HANDLE)}")
    if not re.fullmatch(r"[A-Z]{3,4}", SHORTCODE):
        errors.append("shortcode must be 3-4 capital letters")
    expected_skus = [sku_for(r, c) for r in SIZE_CHART for c in COLOR_NAMES]
    actual_skus = [v["inventoryItem"]["sku"] for v in variants]
    if len(set(actual_skus)) != expected_variant_count or sorted(actual_skus) != sorted(expected_skus):
        errors.append("SKUs are not the unique values derived from SIZE_CHART")
    row_by_label = {r["picker_label"]: r for r in SIZE_CHART}
    expected_pairs = {(r["picker_label"], c) for r in SIZE_CHART for c in COLOR_NAMES}
    actual_pairs = {tuple(i["name"] for i in v["optionValues"]) for v in variants}
    if actual_pairs != expected_pairs:
        errors.append("Size x Color variant combinations do not match")
    for v in variants:
        pair = tuple(i["name"] for i in v["optionValues"])
        expected_price = price_for(row_by_label[pair[0]])
        if v["price"] != expected_price or v["compareAtPrice"] != compare_at(expected_price) or v["inventoryItem"]["cost"] != cost_for(expected_price):
            errors.append(f"price/compare-at/cost mismatch for {pair}")
    headers, table_rows = table_parts(body)
    if len(headers) != 10:
        errors.append(f"size table has {len(headers)} headers, expected 10")
    if len(table_rows) != len(SIZE_CHART):
        errors.append(f"size table has {len(table_rows)} rows, expected {len(SIZE_CHART)}")
    if [r[0] for r in table_rows if r] != [r["picker_label"] for r in SIZE_CHART]:
        errors.append("size-table first column does not match picker labels")
    if any(len(r) != 10 for r in table_rows):
        errors.append("one or more size-table rows lacks 10 cells")
    if body.count("<li>") != 6 + len(KEY_FEATURES):
        errors.append("body must contain 6 detail bullets plus the key features")
    if not 4 <= len(KEY_FEATURES) <= 5:
        errors.append("key features must be 4-5 bullets")
    if body.count("<p>") != 3:
        errors.append("body must contain two narrative paragraphs and one CTA")
    missing_refs = {r["picker_label"] for r in SIZE_CHART} - set(SIZE_MAP) - NO_HONEST_SIZE_MATCH
    if missing_refs:
        errors.append("missing honest size mappings: " + ", ".join(sorted(missing_refs)))
    pre_mf = build_metafields("gid://shopify/Product/0")
    skipped = {k for k, _ in SKIPPED_METAFIELDS}
    for item in pre_mf:
        if f"{item['namespace']}.{item['key']}" in skipped:
            errors.append(f"skipped metafield is being written: {item['namespace']}.{item['key']}")
        if item["value"] in ("", "[]"):
            errors.append(f"empty metafield value: {item['namespace']}.{item['key']}")
    for path in (SOURCE_SIZE_CHART, PRODUCT_IMAGE, CSV_HEADER_SOURCE):
        if not path.is_file():
            errors.append(f"missing required file: {path}")
    if UPLOAD_DIR.is_dir():
        uploads = sorted(p.name for p in UPLOAD_DIR.iterdir() if p.is_file() and not p.name.startswith("."))
        if uploads != [PRODUCT_IMAGE.name]:
            errors.append("upload directory must contain only the one vendor image: " + json.dumps(uploads))
    errors.extend(source_leak_errors(shopper_payload(body, build_tags(), pre_mf)))
    if errors:
        raise RuntimeError("PREFLIGHT FAILED:\n- " + "\n- ".join(errors))


def run_variant_model_guard(variants: list[dict]) -> None:
    with tempfile.TemporaryDirectory() as temp:
        temp_dir = Path(temp)
        (temp_dir / "size-chart.json").write_text(json.dumps(SIZE_CHART, ensure_ascii=False), encoding="utf-8")
        (temp_dir / "derived.json").write_text(json.dumps({"option_names": ["Size", "Color"], "variants": variants}), encoding="utf-8")
        (temp_dir / "vendor-evidence.json").write_text(json.dumps({
            "title": SPEC["vendor_title"],
            "notes": (
                "one complete two-piece Christmas pajama set sold only as a "
                "single purchasable item; the vendor color selector has exactly "
                f"{len(SPEC['vendor_color_values'])} value(s): {', '.join(SPEC['vendor_color_values'])} "
                "(design codes, not separate garments); the size selector lists Dad, Mom, "
                "Children, and Baby rows; baby romper rows are excluded because baby is not "
                "an allowed Family Matching role"
            ),
        }, ensure_ascii=False), encoding="utf-8")
        subprocess.run([
            "python3", str(ROOT / "ops/scripts/validate_listing_variant_model.py"),
            "--size-chart", str(temp_dir / "size-chart.json"),
            "--derived", str(temp_dir / "derived.json"),
            "--vendor-evidence", str(temp_dir / "vendor-evidence.json"),
            "--primary-category", PRIMARY_CATEGORY,
            "--tags", ", ".join(build_tags()),
        ], check=True)


def assert_taxonomy() -> None:
    node = gql(
        """
        query TaxonomyCategory($id: ID!) {
          node(id: $id) { __typename ... on TaxonomyCategory { id fullName isLeaf } }
        }
        """,
        {"id": TAXONOMY_GID},
    )["data"]["node"]
    if (node.get("__typename") != "TaxonomyCategory" or node.get("id") != TAXONOMY_GID
            or node.get("fullName") != EXPECTED_TAXONOMY_FULL_NAME or node.get("isLeaf") is not True):
        raise RuntimeError("Taxonomy guard failed: " + json.dumps(node, ensure_ascii=False))


def fetch_existing() -> dict | None:
    return gql(
        """
        query ExistingProduct($handle: String!) {
          productByHandle(handle: $handle) {
            id status publishedAt
            options { name values }
            variants(first: 100) { nodes { id sku selectedOptions { name value } } }
            media(first: 50) { nodes { ... on MediaImage { id alt } } }
            resourcePublicationsV2(first: 20) { nodes { isPublished publication { id name } } }
          }
        }
        """,
        {"handle": HANDLE},
    )["data"]["productByHandle"]


def pair_of(node: dict) -> tuple[str, ...]:
    return tuple(o["value"] for o in sorted(node["selectedOptions"], key=lambda i: 0 if i["name"] == "Size" else 1))


def assert_existing_is_safe(existing: dict, variants: list[dict]) -> str:
    if existing["status"] != "DRAFT":
        raise RuntimeError(f"Existing product is {existing['status']}; refusing to change it")
    if existing.get("publishedAt"):
        raise RuntimeError("Existing product has publishedAt; refusing draft workflow update")
    if any(n.get("isPublished") for n in existing["resourcePublicationsV2"]["nodes"]):
        raise RuntimeError("Existing product is channel-published; refusing update")
    alts = [n.get("alt") or "" for n in existing["media"]["nodes"]]
    if any(a != MEDIA_ALT for a in alts) or alts.count(MEDIA_ALT) > 1:
        raise RuntimeError("Existing draft has unexpected media; refusing destructive cleanup")
    if [o["name"] for o in existing["options"]] != ["Size", "Color"]:
        raise RuntimeError("Existing draft option axes are not Size / Color")
    live_variants = existing["variants"]["nodes"]
    if len(live_variants) == 1 and not live_variants[0].get("sku"):
        return "standalone"
    expected = {tuple(v["name"] for v in s["optionValues"]): s["inventoryItem"]["sku"] for s in variants}
    if {pair_of(n): n["sku"] for n in live_variants} != expected:
        raise RuntimeError("Existing draft variant shape/SKUs differ from spec; refusing create/delete")
    return "update"


def create_or_update_product(body: str, variants: list[dict]) -> str:
    product_input = {
        "handle": HANDLE, "title": TITLE, "descriptionHtml": body, "vendor": VENDOR,
        "productType": PRODUCT_TYPE, "tags": build_tags(), "status": "DRAFT",
        "category": TAXONOMY_GID, "seo": {"title": SEO_TITLE, "description": SEO_DESCRIPTION},
    }
    product_options = [
        {"name": "Size", "values": [{"name": r["picker_label"]} for r in SIZE_CHART]},
        {"name": "Color", "values": [{"name": n} for n in COLOR_NAMES]},
    ]
    existing = fetch_existing()
    mode = "new"
    if existing:
        mode = assert_existing_is_safe(existing, variants)
        product_id = existing["id"]
        result = gql(
            """
            mutation ProductUpdate($product: ProductUpdateInput!) {
              productUpdate(product: $product) { product { id handle status } userErrors { field message } }
            }
            """,
            {"product": {"id": product_id, **product_input}},
        )
        require_no_user_errors(result, ["data", "productUpdate", "userErrors"])
    else:
        result = gql(
            """
            mutation ProductCreate($input: ProductInput!) {
              productCreate(input: $input) { product { id handle status } userErrors { field message } }
            }
            """,
            {"input": {**product_input, "productOptions": product_options}},
        )
        require_no_user_errors(result, ["data", "productCreate", "userErrors"])
        product_id = result["data"]["productCreate"]["product"]["id"]
    if mode in {"new", "standalone"}:
        result = gql(
            """
            mutation ProductVariantsBulkCreate($productId: ID!, $variants: [ProductVariantsBulkInput!]!, $strategy: ProductVariantsBulkCreateStrategy) {
              productVariantsBulkCreate(productId: $productId, variants: $variants, strategy: $strategy) {
                productVariants { id sku } userErrors { field message }
              }
            }
            """,
            {"productId": product_id, "variants": variants, "strategy": "REMOVE_STANDALONE_VARIANT"},
        )
        require_no_user_errors(result, ["data", "productVariantsBulkCreate", "userErrors"])
    else:
        live_by_pair = {pair_of(n): n for n in existing["variants"]["nodes"]}
        update_inputs = [{"id": live_by_pair[tuple(i["name"] for i in s["optionValues"])]["id"], **s} for s in variants]
        result = gql(
            """
            mutation ProductVariantsBulkUpdate($productId: ID!, $variants: [ProductVariantsBulkInput!]!) {
              productVariantsBulkUpdate(productId: $productId, variants: $variants) {
                productVariants { id sku } userErrors { field message }
              }
            }
            """,
            {"productId": product_id, "variants": update_inputs},
        )
        require_no_user_errors(result, ["data", "productVariantsBulkUpdate", "userErrors"])
    return product_id


def write_metafields(product_id: str) -> None:
    values = build_metafields(product_id)
    for i in range(0, len(values), 25):
        result = gql(
            """
            mutation MetafieldsSet($metafields: [MetafieldsSetInput!]!) {
              metafieldsSet(metafields: $metafields) { metafields { namespace key } userErrors { field message } }
            }
            """,
            {"metafields": values[i:i + 25]},
        )
        require_no_user_errors(result, ["data", "metafieldsSet", "userErrors"])


def upload_owned_media(product_id: str) -> None:
    lookup = gql(
        """
        query ProductMedia($id: ID!) { product(id: $id) { media(first: 50) { nodes { ... on MediaImage { id alt } } } } }
        """,
        {"id": product_id},
    )
    alts = [n.get("alt") or "" for n in lookup["data"]["product"]["media"]["nodes"]]
    if any(a != MEDIA_ALT for a in alts):
        raise RuntimeError("Unexpected existing media; refusing destructive cleanup")
    if alts.count(MEDIA_ALT) > 1:
        raise RuntimeError("Duplicate owned media already exists")
    if MEDIA_ALT in alts:
        return
    mime = mimetypes.guess_type(PRODUCT_IMAGE.name)[0] or "application/octet-stream"
    staged = gql(
        """
        mutation StagedUploadsCreate($input: [StagedUploadInput!]!) {
          stagedUploadsCreate(input: $input) { stagedTargets { url resourceUrl parameters { name value } } userErrors { field message } }
        }
        """,
        {"input": [{"filename": PRODUCT_IMAGE.name, "mimeType": mime, "resource": "IMAGE", "httpMethod": "POST"}]},
    )
    require_no_user_errors(staged, ["data", "stagedUploadsCreate", "userErrors"])
    target = staged["data"]["stagedUploadsCreate"]["stagedTargets"][0]
    form = {p["name"]: p["value"] for p in target["parameters"]}
    with PRODUCT_IMAGE.open("rb") as fh:
        resp = requests.post(target["url"], data=form, files={"file": (PRODUCT_IMAGE.name, fh, mime)}, timeout=120)
        resp.raise_for_status()
    created = gql(
        """
        mutation ProductCreateMedia($productId: ID!, $media: [CreateMediaInput!]!) {
          productCreateMedia(productId: $productId, media: $media) { media { ... on MediaImage { id alt } } userErrors { field message } }
        }
        """,
        {"productId": product_id, "media": [{"originalSource": target["resourceUrl"], "mediaContentType": "IMAGE", "alt": MEDIA_ALT}]},
    )
    require_no_user_errors(created, ["data", "productCreateMedia", "userErrors"])


def fetch_verify(product_id: str) -> dict:
    return gql(
        """
        query VerifyProduct($id: ID!) {
          product(id: $id) {
            id title handle vendor productType status publishedAt onlineStoreUrl descriptionHtml tags
            seo { title description }
            category { id fullName }
            options { name position values }
            variants(first: 100) {
              nodes {
                id sku price compareAtPrice taxable inventoryPolicy
                selectedOptions { name value }
                inventoryItem { tracked requiresShipping unitCost { amount currencyCode } }
              }
            }
            media(first: 50) { nodes { ... on MediaImage { alt status image { url } } } }
            collections(first: 50) { nodes { title handle } }
            metafields(first: 120) { nodes { namespace key type value } }
            resourcePublicationsV2(first: 20) { nodes { isPublished publishDate publication { id name } } }
          }
        }
        """,
        {"id": product_id},
    )["data"]["product"]


def verify_product(product: dict, variants: list[dict]):
    checks = []

    def add(label: str, passed: bool, detail: str) -> None:
        checks.append((label, passed, detail))

    add("Handle matches", product["handle"] == HANDLE, product["handle"])
    add("Title matches", product["title"] == TITLE, product["title"])
    add("Vendor matches", product["vendor"] == VENDOR, product["vendor"])
    add("Product type matches", product["productType"] == PRODUCT_TYPE, product["productType"])
    add("SEO matches", product["seo"] == {"title": SEO_TITLE, "description": SEO_DESCRIPTION}, json.dumps(product["seo"], ensure_ascii=False))
    add("Status is DRAFT", product["status"] == "DRAFT", product["status"])
    add("publishedAt is null", product.get("publishedAt") is None, str(product.get("publishedAt")))
    live_pubs = [n for n in product["resourcePublicationsV2"]["nodes"] if n.get("isPublished")]
    add("No sales-channel publication is live", not live_pubs, str([n["publication"]["name"] for n in live_pubs]))
    category = product["category"] or {}
    add("Taxonomy GID matches", category.get("id") == TAXONOMY_GID, category.get("id") or "missing")
    add("Taxonomy fullName matches", category.get("fullName") == EXPECTED_TAXONOMY_FULL_NAME, category.get("fullName") or "missing")
    add("Options are Size / Color", [o["name"] for o in product["options"]] == ["Size", "Color"], str([o["name"] for o in product["options"]]))
    live_variants = product["variants"]["nodes"]
    spec_by_sku = {v["inventoryItem"]["sku"]: v for v in variants}
    live_skus = [n["sku"] for n in live_variants]
    add(f"Variant count is {len(variants)}", len(live_variants) == len(variants), str(len(live_variants)))
    add("Live SKUs match derived SKUs", sorted(live_skus) == sorted(spec_by_sku), "exact match" if sorted(live_skus) == sorted(spec_by_sku) else "mismatch")
    expected_pairs = {(r["picker_label"], c) for r in SIZE_CHART for c in COLOR_NAMES}
    add("Size x Color combinations match", {pair_of(n) for n in live_variants} == expected_pairs, f"{len(expected_pairs)} combinations")
    price_rows = []
    parity_all = True
    for live in live_variants:
        spec = spec_by_sku.get(live["sku"])
        unit_cost = ((live.get("inventoryItem") or {}).get("unitCost") or {}).get("amount")
        parity = (
            spec is not None and live["price"] == spec["price"] and live["compareAtPrice"] == spec["compareAtPrice"]
            and unit_cost is not None and Decimal(unit_cost) == Decimal(spec["inventoryItem"]["cost"])
            and live["inventoryPolicy"] == "DENY" and live["taxable"] is True
            and live["inventoryItem"]["tracked"] is True and live["inventoryItem"]["requiresShipping"] is True
        )
        parity_all = parity_all and parity
        price_rows.append({
            "sku": live["sku"], "live_price": live["price"], "live_compare_at": live["compareAtPrice"], "live_cost": unit_cost,
            "spec_price": spec["price"] if spec else "", "spec_compare_at": spec["compareAtPrice"] if spec else "",
            "spec_cost": spec["inventoryItem"]["cost"] if spec else "", "match": parity,
        })
    add("Price, compare-at, cost, and inventory parity", parity_all, f"{len(price_rows)} variants checked")
    headers, rows = table_parts(product["descriptionHtml"])
    add("Size table has 10 headers", len(headers) == 10, str(len(headers)))
    add(f"Size table has {len(SIZE_CHART)} rows", len(rows) == len(SIZE_CHART), str(len(rows)))
    add("Size table picker labels match", [r[0] for r in rows if r] == [i["picker_label"] for i in SIZE_CHART], "exact order match")
    if PET:
        add("Dog chart rows show back length and bust", all(r[4] != "-" and r[9] != "-" for r in rows), "all rows")
    elif FIT_TABLE:  # this chart publishes no waist; height and weight come from its fit guide
        add("Waist left blank (not published) and fit guide shown", all(r[8] == "-" and r[2] != "-" and r[3] != "-" for r in rows), "all rows")
    else:
        add("Waist populated for every row", all(r[8] not in ("", "-") for r in rows), "all rows")
    expected_tags = build_tags()
    add("Tags match exactly", product["tags"] == expected_tags, f"{len(product['tags'])} actual / {len(expected_tags)} expected")
    media_nodes = product["media"]["nodes"]
    add("Exactly one vendor image is attached", len(media_nodes) == 1 and (media_nodes[0].get("alt") or "") == MEDIA_ALT, str([n.get("alt") for n in media_nodes]))
    actual_mf = {(n["namespace"], n["key"]): n for n in product["metafields"]["nodes"]}
    expected_mf = build_metafields(product["id"])
    mismatched = [
        f"{m['namespace']}.{m['key']}" for m in expected_mf
        if (m["namespace"], m["key"]) not in actual_mf or (
            json.loads(actual_mf[(m["namespace"], m["key"])]["value"]) != json.loads(m["value"])
            if m["type"].startswith("list.") else actual_mf[(m["namespace"], m["key"])]["value"] != m["value"]
        )
    ]
    add("Applicable metafields are written exactly", not mismatched, ", ".join(mismatched) or f"{len(expected_mf)} exact")
    skipped_present = [k for k, _ in SKIPPED_METAFIELDS if tuple(k.split(".", 1)) in actual_mf]
    add("Skipped metafields are absent", not skipped_present, ", ".join(skipped_present) or "none present")
    leaks = source_leak_errors(shopper_payload(
        product["descriptionHtml"], product["tags"],
        [actual_mf[(m["namespace"], m["key"])] for m in expected_mf if (m["namespace"], m["key"]) in actual_mf],
    ))
    add("Source/trademark/wording leak guard", not leaks, "clean" if not leaks else "; ".join(leaks))
    failures = [f"{label}: {detail}" for label, passed, detail in checks if not passed]
    return checks, price_rows, failures


def write_csv(body: str, variants: list[dict], product: dict) -> None:
    with CSV_HEADER_SOURCE.open("r", encoding="utf-8", newline="") as source:
        header = next(csv.reader(source))
    media_url = ""
    if product["media"]["nodes"]:
        media_url = (product["media"]["nodes"][0].get("image") or {}).get("url") or ""
    size_labels = ", ".join(label for label, _, _ in mapped_size_rows())
    chart_by_label = {r["picker_label"]: r for r in SIZE_CHART}
    rows = []
    for index, variant in enumerate(variants, start=1):
        options = {v["optionName"]: v["name"] for v in variant["optionValues"]}
        chart = chart_by_label[options["Size"]]
        record = {column: "" for column in header}

        def put(column: str, value: str) -> None:
            if column in record:
                record[column] = value

        first = index == 1
        put("Handle", HANDLE)
        put("Title", TITLE if first else "")
        put("Body (HTML)", body if first else "")
        put("Vendor", VENDOR if first else "")
        put("Product Category", EXPECTED_TAXONOMY_FULL_NAME if first else "")
        put("Type", PRODUCT_TYPE if first else "")
        put("Tags", ", ".join(build_tags()) if first else "")
        put("Published", "FALSE")
        put("Option1 Name", "Size")
        put("Option1 Value", chart["picker_label"])
        put("Option2 Name", "Color")
        put("Option2 Value", options["Color"])
        put("Variant SKU", variant["inventoryItem"]["sku"])
        put("Variant Inventory Tracker", "shopify")
        put("Variant Inventory Policy", "deny")
        put("Variant Fulfillment Service", "manual")
        put("Variant Price", variant["price"])
        put("Variant Compare At Price", variant["compareAtPrice"])
        put("Variant Requires Shipping", "TRUE")
        put("Variant Taxable", "TRUE")
        put("Gift Card", "FALSE")
        put("SEO Title", SEO_TITLE if first else "")
        put("SEO Description", SEO_DESCRIPTION if first else "")
        put("Google Shopping / Google Product Category", EXPECTED_TAXONOMY_FULL_NAME if first else "")
        put("Google Shopping / Gender", GOOGLE_GENDER)
        put("Google Shopping / Age Group", "kids" if chart["audience"] == "child" else "adult")
        put("Google Shopping / MPN", variant["inventoryItem"]["sku"])
        put("Google Shopping / Condition", "new")
        put("Google Shopping / Custom Product", "FALSE")
        put("Google Shopping / Custom Label 0", LISTING_MODE if first else "")
        put("Google Shopping / Custom Label 1", PRINT_NAME if first else "")
        put("Google Shopping / Custom Label 2", LABEL2 if first else "")
        put("Google Shopping / Custom Label 3", LABEL3 if first else "")
        put("Google Shopping / Custom Label 4", LABEL4 if first else "")
        put("Category1 (product.metafields.custom.category1)", LISTING_MODE if first else "")
        put("Pattern (product.metafields.custom.pattern)", PRINT_NAME if first else "")
        put("Style (product.metafields.custom.style)", STYLE_VALUE if first else "")
        put("SubCategory (product.metafields.custom.subcategory)", "Pajamas" if first else "")
        put("SubCategory2 (product.metafields.custom.subcategory2)", SUBCATEGORY2 if first else "")
        put("Type (product.metafields.custom.type)", TYPE_VALUE if first else "")
        put("Google: Custom Product (product.metafields.mm-google-shopping.custom_product)", "false")
        put("Age group (product.metafields.shopify.age-group)", "kids, adults" if first else "")
        put("Color (product.metafields.shopify.color-pattern)", ", ".join(COLOR_PATTERN_LABELS) if first else "")
        put("Fabric (product.metafields.shopify.fabric)", FABRIC_LABEL if first else "")
        put("Size (product.metafields.shopify.size)", size_labels if first else "")
        put("Cost per item", variant["inventoryItem"]["cost"])
        put("Status", "draft")
        if first and media_url:
            put("Image Src", media_url)
            put("Image Position", "1")
            put("Image Alt Text", MEDIA_ALT)
        put("Variant Image", media_url)
        rows.append(record)
    with CSV_OUT.open("w", encoding="utf-8", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=header)
        writer.writeheader()
        writer.writerows(rows)


def write_listing(product: dict, checks, variants: list[dict], price_rows) -> None:
    admin_url = "https://admin.shopify.com/store/dresslikemommy/products/" + product["id"].split("/")[-1]
    by_pair = {tuple(v["name"] for v in var["optionValues"]): var for var in variants}
    recap = []
    for row in SIZE_CHART:
        gid, label = SIZE_MAP.get(row["picker_label"], ("skipped", "no honest catalog match"))
        for color_name in COLOR_NAMES:
            v = by_pair[(row["picker_label"], color_name)]
            recap.append("| " + " | ".join([
                row["role"], f"{row['vendor_label']} / chart {row['chart_label']}", row["picker_label"], color_name,
                v["inventoryItem"]["sku"], v["price"], v["compareAtPrice"], v["inventoryItem"]["cost"], f"{gid} ({label})",
            ]) + " |")
    written = sorted(f"{n['namespace']}.{n['key']}" for n in product["metafields"]["nodes"] if n["namespace"] != "judgeme")
    collections = [f"- {c['title']} (/{c['handle']})" for c in product["collections"]["nodes"]] or [
        "- None returned; smart-collection membership may not index until publication."]
    lines = [
        f"# {TITLE}", "",
        "## Status and links",
        "- Status: DRAFT", f"- Admin: {admin_url}", "- Live: not published",
        f"- Product GID: {product['id']}", f"- Handle: {HANDLE}", f"- Vendor: {VENDOR}", "",
        "## Request resolution",
        "| Field | Resolved value |", "|---|---|",
        f"| Vendor URL (local evidence only) | https://detail.1688.com/offer/{SPEC['offer_id']}.html |",
        f"| Offer created on 1688 | {SPEC['offer_created']} (owner filter: designs from 2026) |",
        "| Listing mode | Family Matching (vendor sells one two-piece set in children's, women's, and men's sizes) |",
        "| Primary category | Pajamas |",
        f"| Product type | {PRODUCT_TYPE} |",
        f"| Taxonomy | {EXPECTED_TAXONOMY_FULL_NAME} |",
        f"| Variant model | Size x Color; one two-piece set sold as one item; {len(COLORS)} colorway(s); role encoded in Size |",
        f"| Designs listed | {SPEC['designs_note']} |",
        f"| Exclusions | {SPEC['exclusions_note']} |",
        "| Force spec prices | true (owner-approved Sept 26 shortlist pricing: mother and father 35.99, child 32.99; matches live Boo Stripe / Trick or Treat precedent) |",
        f"| Shortcode | {SHORTCODE} |",
        f"| Color token(s) | {', '.join(COLOR_TOKEN_BY_NAME.values())} |",
        "",
        "## Evidence and assumptions",
        *[f"- {line}" for line in SPEC["evidence_lines"]],
        f"- Size chart: {SPEC['chart_note']}",
        "- Chart parsing (cm): 衣长 top length, 胸围 full chest (as-is), 袖长 sleeve, 裤长 pant length, 腰围 elastic waist range (as-is), 臀围 hip (as-is). Every kept row has all six values.",
        "- Child picker labels follow the chart's T labels (80(2T) -> Child 2 Years ... 160(14T) -> Child 14 Years), the Snowflake Reindeer onesie precedent. The chart's 80-160 codes are not shown as wearer height because they run below typical heights for those ages; Height stays `-`. No wearer weight is published.",
        "- The 婴儿 baby rows (a separate romper with top measurements only) and the vendor's baby SKUs are excluded: baby is not an allowed Family Matching role, and the romper would be a different garment.",
        "- shopify.size: Child 14 Years has no store metaobject (the catalog stops at 12), so it is skipped rather than faked. Mother and Father sizes share adult metaobjects, so each GID is listed once.",
        "- Image: exactly one original vendor image is attached, per the owner request (the owner is producing the final listing images).",
        "",
        "## Title and SEO",
        f"- Product title ({len(TITLE)}/70): {TITLE}",
        f"- SEO title ({len(SEO_TITLE)}/60): {SEO_TITLE}",
        f"- SEO description ({len(SEO_DESCRIPTION)}/155): {SEO_DESCRIPTION}",
        "",
        "## Pricing",
        "| Audience | Price | Compare-at | Cost |", "|---|---:|---:|---:|",
        f"| Child | {CHILD_PRICE} | {compare_at(CHILD_PRICE)} | {cost_for(CHILD_PRICE)} |",
        f"| Mother / Father | {ADULT_PRICE} | {compare_at(ADULT_PRICE)} | {cost_for(ADULT_PRICE)} |",
        f"- Vendor unit prices (CNY, local evidence): {SPEC['vendor_prices_note']}",
        "- Cost per item is exactly 50% of the final variant price, rounded to cents.",
        "",
        "## SIZE_CHART and variant recap",
        "| Role | Vendor SKU / chart row | Picker label | Color | SKU | Price | Compare-at | Cost | shopify.size |",
        "|---|---|---|---|---|---:|---:|---:|---|",
        *recap, "",
        "## Verification", "| Check | Result | Detail |", "|---|---|---|",
        *[f"| {label} | {'PASS' if passed else 'FAIL'} | {detail} |" for label, passed, detail in checks], "",
        "## Price and cost parity",
        "| SKU | Live price | Live compare-at | Live cost | Spec price | Spec compare-at | Spec cost | Match |",
        "|---|---:|---:|---:|---:|---:|---:|---|",
        *["| " + " | ".join([r["sku"], str(r["live_price"]), str(r["live_compare_at"]), str(r["live_cost"]),
                              str(r["spec_price"]), str(r["spec_compare_at"]), str(r["spec_cost"]),
                              "yes" if r["match"] else "no"]) + " |" for r in price_rows], "",
        "## Metafields written", *[f"- {k}" for k in written], "",
        "## Metafields skipped", *[f"- {k}: {why}" for k, why in SKIPPED_METAFIELDS],
        "- shopify.size entry for Child 14 Years: no honest catalog metaobject." if NO_HONEST_SIZE_MATCH else "", "",
        "## Tags written", ", ".join(product["tags"]), "",
        "## Smart collections", *collections, "",
        "## Manual follow-ups",
        f"- Fulfillment note: order design {', '.join(SPEC['vendor_color_values'])} by vendor size label (Child 2 Years = Children 2; Mother S = Mom S; Father S = Dad S).",
        "- Owner is producing the listing images; replace or add to the single vendor image before any publish step.",
        "- Inventory quantities remain unset and need an operator decision before any publish step.",
        "- Care method is not published by the vendor; the body points shoppers to the sewn-in care label.",
        f"- Localization closeout must pass at {LOCALIZATION_CLOSEOUT} before the listing is complete.",
        "",
        "## Files",
        *[f"- {p}" for p in (SCRIPT_PATH, PRODUCT_IMAGE, SOURCE_SIZE_CHART, LISTING_MD, CSV_OUT, SIZE_CHART_OUT,
                             BODY_HTML_OUT, VERIFY_JSON_OUT, LOCALIZATION_CLOSEOUT)],
    ]
    LISTING_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    (ROOT / "ops/listings").mkdir(parents=True, exist_ok=True)
    body = build_body()
    variants = build_variants()
    validate_preflight(body, variants)
    run_variant_model_guard(variants)
    SIZE_CHART_OUT.write_text(json.dumps(SIZE_CHART, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    BODY_HTML_OUT.write_text(body + "\n", encoding="utf-8")
    if os.environ.get("LISTING_PREFLIGHT_ONLY") == "1":
        print(json.dumps({
            "status": "preflight_passed", "handle": HANDLE, "title_len": len(TITLE),
            "seo_title_len": len(SEO_TITLE), "seo_description_len": len(SEO_DESCRIPTION),
            "size_chart_rows": len(SIZE_CHART), "variant_count": len(variants),
        }, indent=2, ensure_ascii=False))
        return
    assert_taxonomy()
    product_id = create_or_update_product(body, variants)
    write_metafields(product_id)
    upload_owned_media(product_id)
    time.sleep(3)
    product = fetch_verify(product_id)
    VERIFY_JSON_OUT.write_text(json.dumps({"data": {"product": product}}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    checks, price_rows, failures = verify_product(product, variants)
    write_csv(body, variants, product)
    write_listing(product, checks, variants, price_rows)
    if failures:
        raise RuntimeError("FINAL VERIFY FAILED:\n- " + "\n- ".join(failures))
    print(json.dumps({
        "admin_url": "https://admin.shopify.com/store/dresslikemommy/products/" + product_id.split("/")[-1],
        "live_url": "not published", "handle": HANDLE, "status": product["status"],
        "variant_count": len(product["variants"]["nodes"]), "published_at": product["publishedAt"],
        "price_cost_parity": all(r["match"] for r in price_rows),
        "collections": [c["handle"] for c in product["collections"]["nodes"]],
        "listing_md": str(LISTING_MD),
    }, indent=2))


if __name__ == "__main__":
    main()
