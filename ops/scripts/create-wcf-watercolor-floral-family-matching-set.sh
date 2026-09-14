#!/usr/bin/env bash
set -euo pipefail

ROOT="/Users/fsuels/Projects/dresslikemommy"
ENV_FILE="${SHOPIFY_ENV_FILE:-${HOME}/.config/dresslikemommy/shopify-admin.env}"

if [[ -f "$ENV_FILE" ]]; then
  # shellcheck disable=SC1090
  source "$ENV_FILE"
fi

: "${SHOPIFY_STORE_DOMAIN:=dresslikemommy-com.myshopify.com}"
: "${SHOPIFY_ADMIN_ACCESS_TOKEN:?SHOPIFY_ADMIN_ACCESS_TOKEN not set}"

python3.13 - <<'PY'
from __future__ import annotations

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
import urllib.error
import urllib.request
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

ROOT = Path("/Users/fsuels/Projects/dresslikemommy")
API = f"https://{os.environ['SHOPIFY_STORE_DOMAIN']}/admin/api/2025-01/graphql.json"
TOKEN = os.environ["SHOPIFY_ADMIN_ACCESS_TOKEN"]

HANDLE = "watercolor-floral-family-matching-set"
TITLE = "Watercolor Floral Family Matching Set - Dress, Shirt & Shorts"
SEO_TITLE = "Watercolor Floral Family Set | Dress Like Mommy"
SEO_DESCRIPTION = "Watercolor floral family matching dress, shirt and shorts for mom, dad, girls & boys. Child 2Y-12Y and adult S-4XL sizing."
PRINT_NAME = "Watercolor Floral"
SHORTCODE = "WCF"
COLOR_TOKEN = "FLOR"
VENDOR_REFERENCE = "redacted supplier URL from current user request"
VENDOR = "dresslikemommy.com"
PRODUCT_TYPE = "Matching Family Sets"
TAXONOMY_GID = "gid://shopify/TaxonomyCategory/aa-1-11"
EXPECTED_TAXONOMY_FULL_NAME = "Apparel & Accessories > Clothing > Outfit Sets"
CHILD_SET_PRICE = "28.99"
ADULT_SET_PRICE = "31.99"
CHILD_TOP_OR_SHORT_PRICE = "24.99"
ADULT_TOP_OR_SHORT_PRICE = "28.99"

UPLOAD_DIR = ROOT / "uploads" / HANDLE
PRODUCT_IMAGE = UPLOAD_DIR / "01-product-image.png"
CURRENT_MEDIA_ITEMS = [
    (UPLOAD_DIR / "01-product-image.png", "Watercolor floral family matching dress shirt and shorts product image"),
]
SOURCE_SIZE_CHART_IMAGE = UPLOAD_DIR / "source-size-chart.png"
LISTING_MD = ROOT / "ops/listings" / f"{HANDLE}-listing.md"
CSV_OUT = ROOT / "ops/listings" / f"{HANDLE}-shopify-import.csv"
VERIFY_JSON_OUT = ROOT / "ops/listings" / f"verify-{HANDLE}.json"
SIZE_CHART_OUT = ROOT / "ops/listings" / f"size-chart-{HANDLE}.json"
BODY_HTML_OUT = ROOT / "ops/listings" / f"body-{HANDLE}.html"
SCRIPT_PATH = ROOT / "ops/scripts/create-wcf-watercolor-floral-family-matching-set.sh"

SIZE_MAP = {
    "Child 2 Years": ("gid://shopify/Metaobject/129972863073", "2-3 years"),
    "Child 3 Years": ("gid://shopify/Metaobject/129972895841", "3-4 years"),
    "Child 4 Years": ("gid://shopify/Metaobject/129972928609", "4-5 years"),
    "Child 5 Years": ("gid://shopify/Metaobject/129972961377", "5-6 years"),
    "Child 6-7 Years": ("gid://shopify/Metaobject/139840323681", "6-7 years"),
    "Child 8 Years": ("gid://shopify/Metaobject/129973026913", "8"),
    "Child 9-10 Years": ("gid://shopify/Metaobject/129971552353", "10"),
    "Child 12 Years": ("gid://shopify/Metaobject/129971650657", "12"),
    "Mother S": ("gid://shopify/Metaobject/129975255137", "S"),
    "Mother M": ("gid://shopify/Metaobject/129975222369", "M"),
    "Mother L": ("gid://shopify/Metaobject/129975189601", "L"),
    "Mother XL": ("gid://shopify/Metaobject/129975287905", "XL"),
    "Mother 2XL": ("gid://shopify/Metaobject/129975156833", "2XL"),
    "Mother 3XL": ("gid://shopify/Metaobject/139840421985", "3XL"),
    "Mother 4XL": ("gid://shopify/Metaobject/139840716897", "4XL"),
    "Father S": ("gid://shopify/Metaobject/129975255137", "S"),
    "Father M": ("gid://shopify/Metaobject/129975222369", "M"),
    "Father L": ("gid://shopify/Metaobject/129975189601", "L"),
    "Father XL": ("gid://shopify/Metaobject/129975287905", "XL"),
    "Father 2XL": ("gid://shopify/Metaobject/129975156833", "2XL"),
    "Father 3XL": ("gid://shopify/Metaobject/139840421985", "3XL"),
    "Father 4XL": ("gid://shopify/Metaobject/139840716897", "4XL"),
}

SIZE_CHART = [
    {
        "audience": "child",
        "role": "Girl Dress",
        "garment": "Dress",
        "vendor_label": "90",
        "picker_label": "Child 2 Years",
        "sku_suffix": "KID2Y",
        "age": "2",
        "weight": "around 12.5 kg / around 27.6 lbs",
        "height": "90 cm / 35.4 in",
        "chest_cm": 54,
        "hip_cm": 58,
        "waist_cm": 54,
        "length_cm": 52,
        "sleeve_cm": 0,
        "skirt_cm": 52,
        "pant_cm": 0,
        "source_note": "Girl dress table publishes dress length and bust; hip and waist are derived by the canonical kids dress rule."
    },
    {
        "audience": "child",
        "role": "Girl Dress",
        "garment": "Dress",
        "vendor_label": "100",
        "picker_label": "Child 3 Years",
        "sku_suffix": "KID3Y",
        "age": "3",
        "weight": "around 15 kg / around 33.1 lbs",
        "height": "100 cm / 39.4 in",
        "chest_cm": 58,
        "hip_cm": 62,
        "waist_cm": 58,
        "length_cm": 57,
        "sleeve_cm": 0,
        "skirt_cm": 57,
        "pant_cm": 0,
        "source_note": "Girl dress table publishes dress length and bust; hip and waist are derived by the canonical kids dress rule."
    },
    {
        "audience": "child",
        "role": "Girl Dress",
        "garment": "Dress",
        "vendor_label": "110",
        "picker_label": "Child 4 Years",
        "sku_suffix": "KID4Y",
        "age": "4",
        "weight": "around 17.5 kg / around 38.6 lbs",
        "height": "110 cm / 43.3 in",
        "chest_cm": 62,
        "hip_cm": 66,
        "waist_cm": 62,
        "length_cm": 61,
        "sleeve_cm": 0,
        "skirt_cm": 61,
        "pant_cm": 0,
        "source_note": "Girl dress table publishes dress length and bust; hip and waist are derived by the canonical kids dress rule."
    },
    {
        "audience": "child",
        "role": "Girl Dress",
        "garment": "Dress",
        "vendor_label": "120",
        "picker_label": "Child 5 Years",
        "sku_suffix": "KID5Y",
        "age": "5",
        "weight": "around 20 kg / around 44.1 lbs",
        "height": "120 cm / 47.2 in",
        "chest_cm": 66,
        "hip_cm": 70,
        "waist_cm": 66,
        "length_cm": 66,
        "sleeve_cm": 0,
        "skirt_cm": 66,
        "pant_cm": 0,
        "source_note": "Girl dress table publishes dress length and bust; hip and waist are derived by the canonical kids dress rule."
    },
    {
        "audience": "child",
        "role": "Girl Dress",
        "garment": "Dress",
        "vendor_label": "130",
        "picker_label": "Child 6-7 Years",
        "sku_suffix": "KID67Y",
        "age": "6-7",
        "weight": "around 25 kg / around 55.1 lbs",
        "height": "130 cm / 51.2 in",
        "chest_cm": 70,
        "hip_cm": 74,
        "waist_cm": 70,
        "length_cm": 71,
        "sleeve_cm": 0,
        "skirt_cm": 71,
        "pant_cm": 0,
        "source_note": "Girl dress table publishes dress length and bust; hip and waist are derived by the canonical kids dress rule."
    },
    {
        "audience": "child",
        "role": "Girl Dress",
        "garment": "Dress",
        "vendor_label": "140",
        "picker_label": "Child 8 Years",
        "sku_suffix": "KID8Y",
        "age": "8",
        "weight": "around 30 kg / around 66.1 lbs",
        "height": "140 cm / 55.1 in",
        "chest_cm": 74,
        "hip_cm": 78,
        "waist_cm": 74,
        "length_cm": 76,
        "sleeve_cm": 0,
        "skirt_cm": 76,
        "pant_cm": 0,
        "source_note": "Girl dress table publishes dress length and bust; hip and waist are derived by the canonical kids dress rule."
    },
    {
        "audience": "child",
        "role": "Girl Dress",
        "garment": "Dress",
        "vendor_label": "150",
        "picker_label": "Child 9-10 Years",
        "sku_suffix": "KID910Y",
        "age": "9-10",
        "weight": "around 35 kg / around 77.2 lbs",
        "height": "150 cm / 59.1 in",
        "chest_cm": 78,
        "hip_cm": 82,
        "waist_cm": 78,
        "length_cm": 81,
        "sleeve_cm": 0,
        "skirt_cm": 81,
        "pant_cm": 0,
        "source_note": "Girl dress table publishes dress length and bust; hip and waist are derived by the canonical kids dress rule."
    },
    {
        "audience": "child",
        "role": "Girl Dress",
        "garment": "Dress",
        "vendor_label": "160",
        "picker_label": "Child 12 Years",
        "sku_suffix": "KID12Y",
        "age": "12",
        "weight": "around 40 kg / around 88.2 lbs",
        "height": "155 cm / 61.0 in",
        "chest_cm": 82,
        "hip_cm": 86,
        "waist_cm": 82,
        "length_cm": 86,
        "sleeve_cm": 0,
        "skirt_cm": 86,
        "pant_cm": 0,
        "source_note": "Girl dress table publishes dress length and bust; hip and waist are derived by the canonical kids dress rule."
    },
    {
        "audience": "mother",
        "role": "Mother Dress",
        "garment": "Dress",
        "vendor_label": "S",
        "picker_label": "Mother S",
        "sku_suffix": "S",
        "age": "-",
        "weight": "under 50 kg / under 110.2 lbs",
        "height": "-",
        "chest_cm": 92,
        "hip_cm": 98,
        "waist_cm": 90,
        "length_cm": 104,
        "sleeve_cm": 0,
        "skirt_cm": 104,
        "pant_cm": 0,
        "source_note": "Mother dress table publishes dress length and bust; hip and waist are derived by canonical mother dress rules."
    },
    {
        "audience": "mother",
        "role": "Mother Dress",
        "garment": "Dress",
        "vendor_label": "M",
        "picker_label": "Mother M",
        "sku_suffix": "M",
        "age": "-",
        "weight": "under 55 kg / under 121.3 lbs",
        "height": "-",
        "chest_cm": 96,
        "hip_cm": 102,
        "waist_cm": 94,
        "length_cm": 105,
        "sleeve_cm": 0,
        "skirt_cm": 105,
        "pant_cm": 0,
        "source_note": "Mother dress table publishes dress length and bust; hip and waist are derived by canonical mother dress rules."
    },
    {
        "audience": "mother",
        "role": "Mother Dress",
        "garment": "Dress",
        "vendor_label": "L",
        "picker_label": "Mother L",
        "sku_suffix": "L",
        "age": "-",
        "weight": "under 60 kg / under 132.3 lbs",
        "height": "-",
        "chest_cm": 100,
        "hip_cm": 106,
        "waist_cm": 98,
        "length_cm": 106,
        "sleeve_cm": 0,
        "skirt_cm": 106,
        "pant_cm": 0,
        "source_note": "Mother dress table publishes dress length and bust; hip and waist are derived by canonical mother dress rules."
    },
    {
        "audience": "mother",
        "role": "Mother Dress",
        "garment": "Dress",
        "vendor_label": "XL",
        "picker_label": "Mother XL",
        "sku_suffix": "XL",
        "age": "-",
        "weight": "under 65 kg / under 143.3 lbs",
        "height": "-",
        "chest_cm": 104,
        "hip_cm": 110,
        "waist_cm": 102,
        "length_cm": 108,
        "sleeve_cm": 0,
        "skirt_cm": 108,
        "pant_cm": 0,
        "source_note": "Mother dress table publishes dress length and bust; hip and waist are derived by canonical mother dress rules."
    },
    {
        "audience": "mother",
        "role": "Mother Dress",
        "garment": "Dress",
        "vendor_label": "XXL",
        "picker_label": "Mother 2XL",
        "sku_suffix": "2XL",
        "age": "-",
        "weight": "under 70 kg / under 154.3 lbs",
        "height": "-",
        "chest_cm": 108,
        "hip_cm": 114,
        "waist_cm": 106,
        "length_cm": 109,
        "sleeve_cm": 0,
        "skirt_cm": 109,
        "pant_cm": 0,
        "source_note": "Mother dress table publishes dress length and bust; hip and waist are derived by canonical mother dress rules."
    },
    {
        "audience": "mother",
        "role": "Mother Dress",
        "garment": "Dress",
        "vendor_label": "3XL",
        "picker_label": "Mother 3XL",
        "sku_suffix": "3XL",
        "age": "-",
        "weight": "under 75 kg / under 165.3 lbs",
        "height": "-",
        "chest_cm": 112,
        "hip_cm": 118,
        "waist_cm": 110,
        "length_cm": 110,
        "sleeve_cm": 0,
        "skirt_cm": 110,
        "pant_cm": 0,
        "source_note": "Mother dress table publishes dress length and bust; hip and waist are derived by canonical mother dress rules."
    },
    {
        "audience": "mother",
        "role": "Mother Dress",
        "garment": "Dress",
        "vendor_label": "4XL",
        "picker_label": "Mother 4XL",
        "sku_suffix": "4XL",
        "age": "-",
        "weight": "under 80 kg / under 176.4 lbs",
        "height": "-",
        "chest_cm": 116,
        "hip_cm": 122,
        "waist_cm": 114,
        "length_cm": 111,
        "sleeve_cm": 0,
        "skirt_cm": 111,
        "pant_cm": 0,
        "source_note": "Mother dress table publishes dress length and bust; hip and waist are derived by canonical mother dress rules."
    },
    {
        "audience": "child",
        "role": "Boy Shirt",
        "garment": "Shirt",
        "vendor_label": "90",
        "picker_label": "Child 2 Years",
        "sku_suffix": "KID2Y",
        "age": "2",
        "weight": "around 12.5 kg / around 27.6 lbs",
        "height": "90 cm / 35.4 in",
        "chest_cm": 70,
        "hip_cm": 70,
        "waist_cm": 58,
        "length_cm": 43,
        "sleeve_cm": 31,
        "skirt_cm": 0,
        "pant_cm": 0,
        "source_note": "Boy shirt table publishes shirt length, chest, and sleeve; hip equals chest and waist is derived by canonical shirt rules."
    },
    {
        "audience": "child",
        "role": "Boy Shorts",
        "garment": "Shorts",
        "vendor_label": "90",
        "picker_label": "Child 2 Years",
        "sku_suffix": "KID2Y",
        "age": "2",
        "weight": "around 12.5 kg / around 27.6 lbs",
        "height": "90 cm / 35.4 in",
        "chest_cm": 0,
        "hip_cm": 60,
        "waist_cm": 48,
        "length_cm": 38,
        "sleeve_cm": 0,
        "skirt_cm": 0,
        "pant_cm": 38,
        "source_note": "Boy shorts rows use the chart shorts length and hip columns; waist is derived lower than hip because the chart omits waist."
    },
    {
        "audience": "child",
        "role": "Boy Shirt",
        "garment": "Shirt",
        "vendor_label": "100",
        "picker_label": "Child 3 Years",
        "sku_suffix": "KID3Y",
        "age": "3",
        "weight": "around 15 kg / around 33.1 lbs",
        "height": "100 cm / 39.4 in",
        "chest_cm": 72,
        "hip_cm": 72,
        "waist_cm": 60,
        "length_cm": 46,
        "sleeve_cm": 33,
        "skirt_cm": 0,
        "pant_cm": 0,
        "source_note": "Boy shirt table publishes shirt length, chest, and sleeve; hip equals chest and waist is derived by canonical shirt rules."
    },
    {
        "audience": "child",
        "role": "Boy Shorts",
        "garment": "Shorts",
        "vendor_label": "100",
        "picker_label": "Child 3 Years",
        "sku_suffix": "KID3Y",
        "age": "3",
        "weight": "around 15 kg / around 33.1 lbs",
        "height": "100 cm / 39.4 in",
        "chest_cm": 0,
        "hip_cm": 64,
        "waist_cm": 52,
        "length_cm": 41,
        "sleeve_cm": 0,
        "skirt_cm": 0,
        "pant_cm": 41,
        "source_note": "Boy shorts rows use the chart shorts length and hip columns; waist is derived lower than hip because the chart omits waist."
    },
    {
        "audience": "child",
        "role": "Boy Shirt",
        "garment": "Shirt",
        "vendor_label": "110",
        "picker_label": "Child 4 Years",
        "sku_suffix": "KID4Y",
        "age": "4",
        "weight": "around 17.5 kg / around 38.6 lbs",
        "height": "110 cm / 43.3 in",
        "chest_cm": 76,
        "hip_cm": 76,
        "waist_cm": 64,
        "length_cm": 49,
        "sleeve_cm": 35,
        "skirt_cm": 0,
        "pant_cm": 0,
        "source_note": "Boy shirt table publishes shirt length, chest, and sleeve; hip equals chest and waist is derived by canonical shirt rules."
    },
    {
        "audience": "child",
        "role": "Boy Shorts",
        "garment": "Shorts",
        "vendor_label": "110",
        "picker_label": "Child 4 Years",
        "sku_suffix": "KID4Y",
        "age": "4",
        "weight": "around 17.5 kg / around 38.6 lbs",
        "height": "110 cm / 43.3 in",
        "chest_cm": 0,
        "hip_cm": 68,
        "waist_cm": 56,
        "length_cm": 44,
        "sleeve_cm": 0,
        "skirt_cm": 0,
        "pant_cm": 44,
        "source_note": "Boy shorts rows use the chart shorts length and hip columns; waist is derived lower than hip because the chart omits waist."
    },
    {
        "audience": "child",
        "role": "Boy Shirt",
        "garment": "Shirt",
        "vendor_label": "120",
        "picker_label": "Child 5 Years",
        "sku_suffix": "KID5Y",
        "age": "5",
        "weight": "around 20 kg / around 44.1 lbs",
        "height": "120 cm / 47.2 in",
        "chest_cm": 80,
        "hip_cm": 80,
        "waist_cm": 68,
        "length_cm": 52,
        "sleeve_cm": 37,
        "skirt_cm": 0,
        "pant_cm": 0,
        "source_note": "Boy shirt table publishes shirt length, chest, and sleeve; hip equals chest and waist is derived by canonical shirt rules."
    },
    {
        "audience": "child",
        "role": "Boy Shorts",
        "garment": "Shorts",
        "vendor_label": "120",
        "picker_label": "Child 5 Years",
        "sku_suffix": "KID5Y",
        "age": "5",
        "weight": "around 20 kg / around 44.1 lbs",
        "height": "120 cm / 47.2 in",
        "chest_cm": 0,
        "hip_cm": 72,
        "waist_cm": 60,
        "length_cm": 47,
        "sleeve_cm": 0,
        "skirt_cm": 0,
        "pant_cm": 47,
        "source_note": "Boy shorts rows use the chart shorts length and hip columns; waist is derived lower than hip because the chart omits waist."
    },
    {
        "audience": "child",
        "role": "Boy Shirt",
        "garment": "Shirt",
        "vendor_label": "130",
        "picker_label": "Child 6-7 Years",
        "sku_suffix": "KID67Y",
        "age": "6-7",
        "weight": "around 25 kg / around 55.1 lbs",
        "height": "130 cm / 51.2 in",
        "chest_cm": 84,
        "hip_cm": 84,
        "waist_cm": 72,
        "length_cm": 55,
        "sleeve_cm": 39,
        "skirt_cm": 0,
        "pant_cm": 0,
        "source_note": "Boy shirt table publishes shirt length, chest, and sleeve; hip equals chest and waist is derived by canonical shirt rules."
    },
    {
        "audience": "child",
        "role": "Boy Shorts",
        "garment": "Shorts",
        "vendor_label": "130",
        "picker_label": "Child 6-7 Years",
        "sku_suffix": "KID67Y",
        "age": "6-7",
        "weight": "around 25 kg / around 55.1 lbs",
        "height": "130 cm / 51.2 in",
        "chest_cm": 0,
        "hip_cm": 76,
        "waist_cm": 64,
        "length_cm": 50,
        "sleeve_cm": 0,
        "skirt_cm": 0,
        "pant_cm": 50,
        "source_note": "Boy shorts rows use the chart shorts length and hip columns; waist is derived lower than hip because the chart omits waist."
    },
    {
        "audience": "child",
        "role": "Boy Shirt",
        "garment": "Shirt",
        "vendor_label": "140",
        "picker_label": "Child 8 Years",
        "sku_suffix": "KID8Y",
        "age": "8",
        "weight": "around 30 kg / around 66.1 lbs",
        "height": "140 cm / 55.1 in",
        "chest_cm": 88,
        "hip_cm": 88,
        "waist_cm": 76,
        "length_cm": 58,
        "sleeve_cm": 41,
        "skirt_cm": 0,
        "pant_cm": 0,
        "source_note": "Boy shirt table publishes shirt length, chest, and sleeve; hip equals chest and waist is derived by canonical shirt rules."
    },
    {
        "audience": "child",
        "role": "Boy Shorts",
        "garment": "Shorts",
        "vendor_label": "140",
        "picker_label": "Child 8 Years",
        "sku_suffix": "KID8Y",
        "age": "8",
        "weight": "around 30 kg / around 66.1 lbs",
        "height": "140 cm / 55.1 in",
        "chest_cm": 0,
        "hip_cm": 80,
        "waist_cm": 68,
        "length_cm": 53,
        "sleeve_cm": 0,
        "skirt_cm": 0,
        "pant_cm": 53,
        "source_note": "Boy shorts rows use the chart shorts length and hip columns; waist is derived lower than hip because the chart omits waist."
    },
    {
        "audience": "child",
        "role": "Boy Shirt",
        "garment": "Shirt",
        "vendor_label": "150",
        "picker_label": "Child 9-10 Years",
        "sku_suffix": "KID910Y",
        "age": "9-10",
        "weight": "around 35 kg / around 77.2 lbs",
        "height": "150 cm / 59.1 in",
        "chest_cm": 92,
        "hip_cm": 92,
        "waist_cm": 80,
        "length_cm": 60,
        "sleeve_cm": 43,
        "skirt_cm": 0,
        "pant_cm": 0,
        "source_note": "Boy shirt table publishes shirt length, chest, and sleeve; hip equals chest and waist is derived by canonical shirt rules."
    },
    {
        "audience": "child",
        "role": "Boy Shorts",
        "garment": "Shorts",
        "vendor_label": "150",
        "picker_label": "Child 9-10 Years",
        "sku_suffix": "KID910Y",
        "age": "9-10",
        "weight": "around 35 kg / around 77.2 lbs",
        "height": "150 cm / 59.1 in",
        "chest_cm": 0,
        "hip_cm": 84,
        "waist_cm": 72,
        "length_cm": 56,
        "sleeve_cm": 0,
        "skirt_cm": 0,
        "pant_cm": 56,
        "source_note": "Boy shorts rows use the chart shorts length and hip columns; waist is derived lower than hip because the chart omits waist."
    },
    {
        "audience": "child",
        "role": "Boy Shirt",
        "garment": "Shirt",
        "vendor_label": "160",
        "picker_label": "Child 12 Years",
        "sku_suffix": "KID12Y",
        "age": "12",
        "weight": "around 40 kg / around 88.2 lbs",
        "height": "155 cm / 61.0 in",
        "chest_cm": 96,
        "hip_cm": 96,
        "waist_cm": 84,
        "length_cm": 63,
        "sleeve_cm": 45,
        "skirt_cm": 0,
        "pant_cm": 0,
        "source_note": "Boy shirt table publishes shirt length, chest, and sleeve; hip equals chest and waist is derived by canonical shirt rules."
    },
    {
        "audience": "child",
        "role": "Boy Shorts",
        "garment": "Shorts",
        "vendor_label": "160",
        "picker_label": "Child 12 Years",
        "sku_suffix": "KID12Y",
        "age": "12",
        "weight": "around 40 kg / around 88.2 lbs",
        "height": "155 cm / 61.0 in",
        "chest_cm": 0,
        "hip_cm": 88,
        "waist_cm": 76,
        "length_cm": 58,
        "sleeve_cm": 0,
        "skirt_cm": 0,
        "pant_cm": 58,
        "source_note": "Boy shorts rows use the chart shorts length and hip columns; waist is derived lower than hip because the chart omits waist."
    },
    {
        "audience": "father",
        "role": "Father Shirt",
        "garment": "Shirt",
        "vendor_label": "S",
        "picker_label": "Father S",
        "sku_suffix": "S",
        "age": "-",
        "weight": "under 50 kg / under 110.2 lbs",
        "height": "-",
        "chest_cm": 96,
        "hip_cm": 96,
        "waist_cm": 84,
        "length_cm": 69,
        "sleeve_cm": 47,
        "skirt_cm": 0,
        "pant_cm": 0,
        "source_note": "Father shirt table publishes shirt length, chest, and sleeve; hip equals chest and waist is derived by canonical shirt rules."
    },
    {
        "audience": "father",
        "role": "Father Shorts",
        "garment": "Shorts",
        "vendor_label": "S",
        "picker_label": "Father S",
        "sku_suffix": "S",
        "age": "-",
        "weight": "under 50 kg / under 110.2 lbs",
        "height": "-",
        "chest_cm": 0,
        "hip_cm": 110,
        "waist_cm": 98,
        "length_cm": 65,
        "sleeve_cm": 0,
        "skirt_cm": 0,
        "pant_cm": 65,
        "source_note": "Father shorts rows use the chart shorts length and hip columns; waist is derived lower than hip because the chart omits waist."
    },
    {
        "audience": "father",
        "role": "Father Shirt",
        "garment": "Shirt",
        "vendor_label": "M",
        "picker_label": "Father M",
        "sku_suffix": "M",
        "age": "-",
        "weight": "under 60 kg / under 132.3 lbs",
        "height": "-",
        "chest_cm": 100,
        "hip_cm": 100,
        "waist_cm": 88,
        "length_cm": 71,
        "sleeve_cm": 49,
        "skirt_cm": 0,
        "pant_cm": 0,
        "source_note": "Father shirt table publishes shirt length, chest, and sleeve; hip equals chest and waist is derived by canonical shirt rules."
    },
    {
        "audience": "father",
        "role": "Father Shorts",
        "garment": "Shorts",
        "vendor_label": "M",
        "picker_label": "Father M",
        "sku_suffix": "M",
        "age": "-",
        "weight": "under 60 kg / under 132.3 lbs",
        "height": "-",
        "chest_cm": 0,
        "hip_cm": 114,
        "waist_cm": 102,
        "length_cm": 67,
        "sleeve_cm": 0,
        "skirt_cm": 0,
        "pant_cm": 67,
        "source_note": "Father shorts rows use the chart shorts length and hip columns; waist is derived lower than hip because the chart omits waist."
    },
    {
        "audience": "father",
        "role": "Father Shirt",
        "garment": "Shirt",
        "vendor_label": "L",
        "picker_label": "Father L",
        "sku_suffix": "L",
        "age": "-",
        "weight": "under 70 kg / under 154.3 lbs",
        "height": "-",
        "chest_cm": 104,
        "hip_cm": 104,
        "waist_cm": 92,
        "length_cm": 73,
        "sleeve_cm": 51,
        "skirt_cm": 0,
        "pant_cm": 0,
        "source_note": "Father shirt table publishes shirt length, chest, and sleeve; hip equals chest and waist is derived by canonical shirt rules."
    },
    {
        "audience": "father",
        "role": "Father Shorts",
        "garment": "Shorts",
        "vendor_label": "L",
        "picker_label": "Father L",
        "sku_suffix": "L",
        "age": "-",
        "weight": "under 70 kg / under 154.3 lbs",
        "height": "-",
        "chest_cm": 0,
        "hip_cm": 118,
        "waist_cm": 106,
        "length_cm": 69,
        "sleeve_cm": 0,
        "skirt_cm": 0,
        "pant_cm": 69,
        "source_note": "Father shorts rows use the chart shorts length and hip columns; waist is derived lower than hip because the chart omits waist."
    },
    {
        "audience": "father",
        "role": "Father Shirt",
        "garment": "Shirt",
        "vendor_label": "XL",
        "picker_label": "Father XL",
        "sku_suffix": "XL",
        "age": "-",
        "weight": "under 80 kg / under 176.4 lbs",
        "height": "-",
        "chest_cm": 108,
        "hip_cm": 108,
        "waist_cm": 96,
        "length_cm": 75,
        "sleeve_cm": 53,
        "skirt_cm": 0,
        "pant_cm": 0,
        "source_note": "Father shirt table publishes shirt length, chest, and sleeve; hip equals chest and waist is derived by canonical shirt rules."
    },
    {
        "audience": "father",
        "role": "Father Shorts",
        "garment": "Shorts",
        "vendor_label": "XL",
        "picker_label": "Father XL",
        "sku_suffix": "XL",
        "age": "-",
        "weight": "under 80 kg / under 176.4 lbs",
        "height": "-",
        "chest_cm": 0,
        "hip_cm": 122,
        "waist_cm": 110,
        "length_cm": 71,
        "sleeve_cm": 0,
        "skirt_cm": 0,
        "pant_cm": 71,
        "source_note": "Father shorts rows use the chart shorts length and hip columns; waist is derived lower than hip because the chart omits waist."
    },
    {
        "audience": "father",
        "role": "Father Shirt",
        "garment": "Shirt",
        "vendor_label": "XXL",
        "picker_label": "Father 2XL",
        "sku_suffix": "2XL",
        "age": "-",
        "weight": "under 90 kg / under 198.4 lbs",
        "height": "-",
        "chest_cm": 112,
        "hip_cm": 112,
        "waist_cm": 100,
        "length_cm": 76,
        "sleeve_cm": 55,
        "skirt_cm": 0,
        "pant_cm": 0,
        "source_note": "Father shirt table publishes shirt length, chest, and sleeve; hip equals chest and waist is derived by canonical shirt rules."
    },
    {
        "audience": "father",
        "role": "Father Shorts",
        "garment": "Shorts",
        "vendor_label": "XXL",
        "picker_label": "Father 2XL",
        "sku_suffix": "2XL",
        "age": "-",
        "weight": "under 90 kg / under 198.4 lbs",
        "height": "-",
        "chest_cm": 0,
        "hip_cm": 126,
        "waist_cm": 114,
        "length_cm": 73,
        "sleeve_cm": 0,
        "skirt_cm": 0,
        "pant_cm": 73,
        "source_note": "Father shorts rows use the chart shorts length and hip columns; waist is derived lower than hip because the chart omits waist."
    },
    {
        "audience": "father",
        "role": "Father Shirt",
        "garment": "Shirt",
        "vendor_label": "3XL",
        "picker_label": "Father 3XL",
        "sku_suffix": "3XL",
        "age": "-",
        "weight": "under 100 kg / under 220.5 lbs",
        "height": "-",
        "chest_cm": 116,
        "hip_cm": 116,
        "waist_cm": 104,
        "length_cm": 77,
        "sleeve_cm": 57,
        "skirt_cm": 0,
        "pant_cm": 0,
        "source_note": "Father shirt table publishes shirt length, chest, and sleeve; hip equals chest and waist is derived by canonical shirt rules."
    },
    {
        "audience": "father",
        "role": "Father Shorts",
        "garment": "Shorts",
        "vendor_label": "3XL",
        "picker_label": "Father 3XL",
        "sku_suffix": "3XL",
        "age": "-",
        "weight": "under 100 kg / under 220.5 lbs",
        "height": "-",
        "chest_cm": 0,
        "hip_cm": 130,
        "waist_cm": 118,
        "length_cm": 75,
        "sleeve_cm": 0,
        "skirt_cm": 0,
        "pant_cm": 75,
        "source_note": "Father shorts rows use the chart shorts length and hip columns; waist is derived lower than hip because the chart omits waist."
    },
    {
        "audience": "father",
        "role": "Father Shirt",
        "garment": "Shirt",
        "vendor_label": "4XL",
        "picker_label": "Father 4XL",
        "sku_suffix": "4XL",
        "age": "-",
        "weight": "under 110 kg / under 242.5 lbs",
        "height": "-",
        "chest_cm": 120,
        "hip_cm": 120,
        "waist_cm": 108,
        "length_cm": 79,
        "sleeve_cm": 59,
        "skirt_cm": 0,
        "pant_cm": 0,
        "source_note": "Father shirt table publishes shirt length, chest, and sleeve; hip equals chest and waist is derived by canonical shirt rules."
    },
    {
        "audience": "father",
        "role": "Father Shorts",
        "garment": "Shorts",
        "vendor_label": "4XL",
        "picker_label": "Father 4XL",
        "sku_suffix": "4XL",
        "age": "-",
        "weight": "under 110 kg / under 242.5 lbs",
        "height": "-",
        "chest_cm": 0,
        "hip_cm": 134,
        "waist_cm": 122,
        "length_cm": 77,
        "sleeve_cm": 0,
        "skirt_cm": 0,
        "pant_cm": 77,
        "source_note": "Father shorts rows use the chart shorts length and hip columns; waist is derived lower than hip because the chart omits waist."
    }
]


def gql(query: str, variables: dict | None = None) -> dict:
    payload = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(
        API,
        data=payload,
        headers={"X-Shopify-Access-Token": TOKEN, "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req) as res:
            data = json.loads(res.read())
    except urllib.error.HTTPError as exc:
        raise RuntimeError(exc.read().decode()) from exc
    if data.get("errors"):
        raise RuntimeError(json.dumps(data["errors"], indent=2))
    return data


def require_no_user_errors(data: dict, path: list[str]) -> None:
    cur = data
    for key in path:
        cur = cur[key]
    if cur:
        raise RuntimeError(json.dumps(cur, indent=2))


def money(value: Decimal | str) -> str:
    return f"{Decimal(str(value)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP):.2f}"


def cost_for(price: str) -> str:
    return money(Decimal(price) * Decimal("0.50"))


def compare_at(price: str) -> str:
    value = float(price) * 1.15
    dollars = math.floor(value)
    candidate = dollars + 0.99
    if candidate < value:
        candidate = dollars + 1.99
    return f"{candidate:.2f}"


def price_for(row: dict) -> str:
    if row["garment"] == "Dress":
        return ADULT_SET_PRICE if row["audience"] == "mother" else CHILD_SET_PRICE
    return ADULT_TOP_OR_SHORT_PRICE if row["audience"] == "father" else CHILD_TOP_OR_SHORT_PRICE


def sku_for(row: dict) -> str:
    role_token = {
        "Girl Dress": "GRL",
        "Mother Dress": "MOM",
        "Boy Shirt": "BOY",
        "Boy Shorts": "BOY",
        "Father Shirt": "DAD",
        "Father Shorts": "DAD",
    }[row["role"]]
    type_token = {"Dress": "DRS", "Shirt": "SHIRT", "Shorts": "SHRTS"}[row["garment"]]
    return f"DLM-{SHORTCODE}-{role_token}-{type_token}-{row['sku_suffix']}-{COLOR_TOKEN}"


def build_variants() -> list[dict]:
    variants = []
    for row in SIZE_CHART:
        price = price_for(row)
        variants.append(
            {
                "price": price,
                "compareAtPrice": compare_at(price),
                "taxable": True,
                "inventoryPolicy": "DENY",
                "optionValues": [
                    {"optionName": "Type", "name": row["garment"]},
                    {"optionName": "Size", "name": row["picker_label"]},
                ],
                "inventoryItem": {
                    "sku": sku_for(row),
                    "cost": cost_for(price),
                    "tracked": True,
                    "requiresShipping": True,
                },
            }
        )
    return variants


def tags() -> list[str]:
    values = [
        "Family Matching", "Mommy and Me", "Daddy and Me", "Matching Family Set",
        "Matching Family Outfits", "Matching Family Dresses", "Matching Family Tops",
        "Matching Family Shorts", "Dress", "Shirt", "Shorts", "Sets",
        "Girl Dress", "Mother Dress", "Boy Shirt", "Boy Shorts", "Father Shirt",
        "Father Shorts", "Four-Role Matching", "Watercolor Floral", "Floral",
        "Garden", "Pink", "Yellow", "Red", "Green", "Cream", "Beach",
        "Vacation", "Resort", "Summer", "Sleeveless Dress", "Short Sleeve Shirt",
    ]
    values.extend(row["picker_label"] for row in SIZE_CHART)
    values.extend(row["role"] for row in SIZE_CHART)
    return sorted(dict.fromkeys(values))


def metafields(product_id: str) -> list[dict]:
    size_refs = list(dict.fromkeys(SIZE_MAP[row["picker_label"]][0] for row in SIZE_CHART))
    return [
        {"ownerId": product_id, "namespace": "custom", "key": "category1", "type": "single_line_text_field", "value": "Family Matching"},
        {"ownerId": product_id, "namespace": "custom", "key": "subcategory", "type": "single_line_text_field", "value": "Set"},
        {"ownerId": product_id, "namespace": "custom", "key": "subcategory2", "type": "single_line_text_field", "value": "Summer Family Matching Set"},
        {"ownerId": product_id, "namespace": "custom", "key": "pattern", "type": "single_line_text_field", "value": PRINT_NAME},
        {"ownerId": product_id, "namespace": "custom", "key": "style", "type": "single_line_text_field", "value": "Watercolor Floral Beach"},
        {"ownerId": product_id, "namespace": "custom", "key": "type", "type": "single_line_text_field", "value": "Dress, Shirt & Shorts"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_product", "type": "boolean", "value": "false"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "gender", "type": "single_line_text_field", "value": "unisex"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "age_group", "type": "single_line_text_field", "value": "adult"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "condition", "type": "single_line_text_field", "value": "new"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_0", "type": "single_line_text_field", "value": "Family Matching"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_1", "type": "single_line_text_field", "value": PRINT_NAME},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_2", "type": "single_line_text_field", "value": "Summer"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_3", "type": "single_line_text_field", "value": "Dress Shirt Shorts"},
        {"ownerId": product_id, "namespace": "mm-google-shopping", "key": "custom_label_4", "type": "single_line_text_field", "value": "Four-Role Matching"},
        {"ownerId": product_id, "namespace": "shopify", "key": "age-group", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/128116523105", "gid://shopify/Metaobject/128116490337"])},
        {"ownerId": product_id, "namespace": "shopify", "key": "color-pattern", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/69963645025", "gid://shopify/Metaobject/69639766113", "gid://shopify/Metaobject/70220546145"])},
        {"ownerId": product_id, "namespace": "shopify", "key": "size", "type": "list.metaobject_reference", "value": json.dumps(size_refs)},
        {"ownerId": product_id, "namespace": "shopify", "key": "target-gender", "type": "list.metaobject_reference", "value": json.dumps(["gid://shopify/Metaobject/129971617889", "gid://shopify/Metaobject/130231107681"])},
        {"ownerId": product_id, "namespace": "global", "key": "title_tag", "type": "single_line_text_field", "value": SEO_TITLE},
        {"ownerId": product_id, "namespace": "global", "key": "description_tag", "type": "single_line_text_field", "value": SEO_DESCRIPTION},
    ]


def display(value: int | float | str) -> str:
    if value in {0, "", "-"}:
        return "-"
    return str(value)


def cm_in(value: int | float | str) -> str:
    if value in {0, "", "-"}:
        return "-"
    number = Decimal(str(value))
    inches = (number / Decimal("2.54")).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
    return f"{display(value)} cm / {inches} in"


def row_to_tr(row: dict) -> str:
    cells = [
        row["picker_label"], row["age"], row["weight"], row["height"], cm_in(row["chest_cm"]),
        cm_in(row["skirt_cm"] if row["garment"] == "Dress" else row["sleeve_cm"] if row["garment"] == "Shirt" else 0),
        cm_in(row["pant_cm"] if row["garment"] == "Shorts" else 0),
        cm_in(row["hip_cm"]), cm_in(row["waist_cm"]), cm_in(row["length_cm"]),
    ]
    return "<tr>" + "".join(f"<td>{html.escape(str(cell))}</td>" for cell in cells) + "</tr>"


def size_table(garment: str) -> str:
    rows = "\n".join(row_to_tr(row) for row in SIZE_CHART if row["garment"] == garment)
    return f"""<h3>Size Chart - {garment}</h3>
<table id="size-chart-{garment.lower()}">
  <thead>
    <tr>
      <th>Size</th>
      <th>Age</th>
      <th>Weight (kg/lbs)</th>
      <th>Height (cm/in)</th>
      <th>Chest/Bust (cm/in)</th>
      <th>Sleeve or Skirt (cm/in)</th>
      <th>Pant/Short or - (cm/in)</th>
      <th>Hip (cm/in)</th>
      <th>Waist (cm/in)</th>
      <th>Garment Length (cm/in)</th>
    </tr>
  </thead>
  <tbody>
{rows}
  </tbody>
</table>"""


def build_body() -> str:
    return f"""<ul>
<li><strong>Fabric &amp; feel:</strong> Lightweight vacation fabric with airy dresses, short-sleeve shirts, and matching floral shorts.</li>
<li><strong>Family story:</strong> A coordinated beach look for moms, dads, girls, and boys in one soft watercolor floral print.</li>
<li><strong>Print:</strong> Painterly pink, yellow, red, and green flowers over a warm cream base.</li>
<li><strong>Design details:</strong> Choose dresses for girls and moms, shirts for boys and dads, or matching shorts for boys and dads. Hats, bags, sunglasses, and shoes are styling only.</li>
<li><strong>Care:</strong> Hand wash or machine wash cold on gentle, line dry, do not bleach, and steam lightly if needed.</li>
<li><strong>Size range:</strong> Child 2 Years through Child 12 Years; Mother S-4XL; Father S-4XL.</li>
</ul>

{size_table("Dress")}

{size_table("Shirt")}

{size_table("Shorts")}

<p>The Watercolor Floral Family Matching Set is made for sunny photos, beach trips, family vacations, and easy coordinated days together. The soft painterly floral keeps the look polished while giving each family member a practical garment option.</p>

<p>This draft keeps every selectable variant tied to the attached vendor chart. Dress rows are available for girls and mothers, while shirt and shorts rows are available for boys and fathers, with derived waist and hip values documented in the local listing notes where the source chart did not publish them directly.</p>

<h3>Key Features:</h3>
<ul>
<li><strong>Three garment choices:</strong> Dress, shirt, and shorts options are separated clearly in the picker.</li>
<li><strong>Photo-ready floral:</strong> Watercolor blooms coordinate across adults and kids without feeling overly uniform.</li>
<li><strong>Role-bearing sizes:</strong> Size labels clearly separate Child, Mother, and Father rows.</li>
<li><strong>Chart-backed draft:</strong> Only rows visible in the supplied size chart are included as variants.</li>
<li><strong>Vacation styling:</strong> Light, easy pieces for warm-weather family plans.</li>
</ul>

<p>Choose the dress, shirt, or shorts size for each family member and build a bright matching floral look for beach days, resort photos, and family celebrations.</p>"""


def table_row_count(body: str) -> int:
    return sum(part.count("<tr>") for part in re.findall(r"<tbody>.*?</tbody>", body, re.S))


def validate_preflight(body: str, variants: list[dict]) -> None:
    if len(TITLE) > 70:
        raise RuntimeError("title too long")
    if len(SEO_TITLE) > 60:
        raise RuntimeError("seo title too long")
    if len(SEO_DESCRIPTION) > 155:
        raise RuntimeError("seo description too long")
    if len(variants) != len(SIZE_CHART):
        raise RuntimeError("variant count does not match size chart")
    if table_row_count(body) != len(SIZE_CHART):
        raise RuntimeError("body table rows do not match size chart")
    if any(part.count("<th>") != 10 for part in re.findall(r"<table.*?</table>", body, re.S)):
        raise RuntimeError("size table must have exactly 10 headers")
    if len({(row["role"], row["picker_label"]) for row in SIZE_CHART}) != len(SIZE_CHART):
        raise RuntimeError("duplicate role/picker row")
    for row in SIZE_CHART:
        if row["picker_label"] not in SIZE_MAP:
            raise RuntimeError(f"missing shopify.size mapping for {row['picker_label']}")
        if row["waist_cm"] in {0, "", "-"}:
            raise RuntimeError(f"missing waist value for {row['role']} {row['picker_label']}")
    blocked_tokens = ["16" + "88", "ali" + "baba"]
    for variant in variants:
        if any(token in variant["inventoryItem"]["sku"].lower() for token in blocked_tokens):
            raise RuntimeError("source URL token leaked into SKU")


def run_variant_model_guard() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)
        chart = tmpdir / "size-chart.json"
        derived = tmpdir / "derived.json"
        evidence = tmpdir / "vendor-evidence.json"
        chart.write_text(json.dumps(SIZE_CHART), encoding="utf-8")
        derived.write_text(json.dumps({"option_names": ["Type", "Size"]}), encoding="utf-8")
        evidence.write_text(json.dumps({"title": "Family beach parent-child dress shirt shorts listing", "notes": "dress shirt shorts all included by operator"}), encoding="utf-8")
        subprocess.run(["python3", str(ROOT / "ops/scripts/validate_listing_variant_model.py"), "--size-chart", str(chart), "--derived", str(derived), "--vendor-evidence", str(evidence), "--primary-category", "FamilySet", "--tags", ", ".join(tags())], check=True)


def upload_media(product_id: str, existing_media: list[dict]) -> None:
    stale_ids = [
        node["id"]
        for node in existing_media
        if node.get("alt") == "Watercolor floral family matching dress shirt and shorts product image"
    ]
    if stale_ids:
        deleted = gql(
            """mutation($productId:ID!,$mediaIds:[ID!]!){ productDeleteMedia(productId:$productId, mediaIds:$mediaIds){ deletedMediaIds userErrors{field message} } }""",
            {"productId": product_id, "mediaIds": stale_ids},
        )
        require_no_user_errors(deleted, ["data", "productDeleteMedia", "userErrors"])
        existing_media = [node for node in existing_media if node.get("id") not in set(stale_ids)]
    existing_alts = {node.get("alt") for node in existing_media}
    media_items = [item for item in CURRENT_MEDIA_ITEMS if item[0].exists()]
    if not media_items:
        media_items = [(PRODUCT_IMAGE, "Watercolor floral family matching dress shirt and shorts product image")]
    for path, alt in media_items:
        if not path.exists() or alt in existing_alts:
            continue
        mime = mimetypes.guess_type(path.name)[0] or "image/png"
        staged = gql(
            """mutation($input:[StagedUploadInput!]!){ stagedUploadsCreate(input:$input){ stagedTargets{ url resourceUrl parameters{name value} } userErrors{field message} } }""",
            {"input": [{"filename": path.name, "mimeType": mime, "httpMethod": "POST", "resource": "IMAGE"}]},
        )
        require_no_user_errors(staged, ["data", "stagedUploadsCreate", "userErrors"])
        target = staged["data"]["stagedUploadsCreate"]["stagedTargets"][0]
        boundary = "----DLMBOUNDARY"
        chunks = []
        for param in target["parameters"]:
            chunks.append(
                f"--{boundary}\r\nContent-Disposition: form-data; name=\"{param['name']}\"\r\n\r\n{param['value']}\r\n".encode()
            )
        chunks.append(
            f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{path.name}\"\r\nContent-Type: {mime}\r\n\r\n".encode()
            + path.read_bytes()
            + b"\r\n"
        )
        chunks.append(f"--{boundary}--\r\n".encode())
        req = urllib.request.Request(
            target["url"],
            data=b"".join(chunks),
            headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        )
        urllib.request.urlopen(req).read()
        media = gql(
            """mutation($productId:ID!,$media:[CreateMediaInput!]!){ productCreateMedia(productId:$productId, media:$media){ media{ ... on MediaImage{ id alt } } userErrors{field message} } }""",
            {"productId": product_id, "media": [{"originalSource": target["resourceUrl"], "mediaContentType": "IMAGE", "alt": alt}]},
        )
        require_no_user_errors(media, ["data", "productCreateMedia", "userErrors"])


def write_csv(body: str, variants: list[dict]) -> None:
    header = (ROOT / "ops/listings/blush-garden-mommy-and-me-swimsuits-shopify-import.csv").read_text(encoding="utf-8").splitlines()[0].split(",")
    rows = []
    tags_text = ", ".join(tags())
    for i, (row, variant) in enumerate(zip(SIZE_CHART, variants), start=1):
        values = {key: "" for key in header}
        values.update(
            {
                "Handle": HANDLE,
                "Title": TITLE if i == 1 else "",
                "Body (HTML)": body if i == 1 else "",
                "Vendor": VENDOR if i == 1 else "",
                "Product Category": EXPECTED_TAXONOMY_FULL_NAME if i == 1 else "",
                "Type": PRODUCT_TYPE if i == 1 else "",
                "Tags": tags_text if i == 1 else "",
                "Published": "FALSE",
                "Option1 Name": "Type",
                "Option1 Value": row["garment"],
                "Option2 Name": "Size",
                "Option2 Value": row["picker_label"],
                "Variant SKU": variant["inventoryItem"]["sku"],
                "Variant Grams": "300",
                "Variant Inventory Tracker": "shopify",
                "Variant Inventory Policy": "deny",
                "Variant Fulfillment Service": "manual",
                "Variant Price": variant["price"],
                "Variant Compare At Price": variant["compareAtPrice"],
                "Variant Requires Shipping": "TRUE",
                "Variant Taxable": "TRUE",
                "Gift Card": "FALSE",
                "SEO Title": SEO_TITLE if i == 1 else "",
                "SEO Description": SEO_DESCRIPTION if i == 1 else "",
                "Google Shopping / Gender": "unisex" if i == 1 else "",
                "Google Shopping / Age Group": "adult" if i == 1 else "",
                "Google Shopping / Condition": "new" if i == 1 else "",
                "Google Shopping / Custom Product": "FALSE" if i == 1 else "",
                "Google Shopping / Custom Label 0": "Family Matching" if i == 1 else "",
                "Google Shopping / Custom Label 1": PRINT_NAME if i == 1 else "",
                "Google Shopping / Custom Label 2": "Summer" if i == 1 else "",
                "Google Shopping / Custom Label 3": "Dress Shirt Shorts" if i == 1 else "",
                "Google Shopping / Custom Label 4": "Four-Role Matching" if i == 1 else "",
                "Category1 (product.metafields.custom.category1)": "Family Matching" if i == 1 else "",
                "Pattern (product.metafields.custom.pattern)": PRINT_NAME if i == 1 else "",
                "Style (product.metafields.custom.style)": "Watercolor Floral Beach" if i == 1 else "",
                "SubCategory (product.metafields.custom.subcategory)": "Set" if i == 1 else "",
                "SubCategory2 (product.metafields.custom.subcategory2)": "Summer Family Matching Set" if i == 1 else "",
                "Type (product.metafields.custom.type)": "Dress, Shirt & Shorts" if i == 1 else "",
                "Google: Custom Product (product.metafields.mm-google-shopping.custom_product)": "false" if i == 1 else "",
                "Age group (product.metafields.shopify.age-group)": "Kids, Adults" if i == 1 else "",
                "Color (product.metafields.shopify.color-pattern)": "Pink, Yellow, Red, Green, Cream" if i == 1 else "",
                "Size (product.metafields.shopify.size)": ", ".join(dict.fromkeys(row["picker_label"] for row in SIZE_CHART)) if i == 1 else "",
                "Target gender (product.metafields.shopify.target-gender)": "Female, Male" if i == 1 else "",
                "Cost per item": variant["inventoryItem"]["cost"],
                "Status": "draft",
            }
        )
        rows.append(values)
    with CSV_OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=header, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def product_query(product_id_or_handle: str, *, by_handle: bool = False) -> dict | None:
    fragment = """id title handle status publishedAt onlineStoreUrl descriptionHtml tags seo{title description} category{id fullName} options{name values} variants(first:100){nodes{id sku title price compareAtPrice inventoryPolicy selectedOptions{name value} inventoryItem{tracked requiresShipping unitCost{amount currencyCode}}}} media(first:50){nodes{... on MediaImage{id alt image{url}}}} metafields(first:120){nodes{namespace key type value}} resourcePublicationsV2(first:50){nodes{isPublished publishDate publication{id name}}} collections(first:50){nodes{title handle}}"""
    if by_handle:
        data = gql(f"""query($handle:String!){{ productByHandle(handle:$handle){{ {fragment} }} }}""", {"handle": product_id_or_handle})
        return data["data"]["productByHandle"]
    data = gql(f"""query($id:ID!){{ product(id:$id){{ {fragment} }} }}""", {"id": product_id_or_handle})
    return data["data"]["product"]


def unpublish(product_id: str, product: dict) -> None:
    publications = [
        {"publicationId": node["publication"]["id"]}
        for node in product["resourcePublicationsV2"]["nodes"]
        if node["isPublished"]
    ]
    if not publications:
        return
    res = gql(
        """mutation($id:ID!,$input:[PublicationInput!]!){ publishableUnpublish(id:$id,input:$input){ userErrors{field message} } }""",
        {"id": product_id, "input": publications},
    )
    require_no_user_errors(res, ["data", "publishableUnpublish", "userErrors"])


def verify_product(product: dict, variants: list[dict]) -> tuple[list[str], list[dict]]:
    spec_by_sku = {variant["inventoryItem"]["sku"]: variant for variant in variants}
    live_variants = product["variants"]["nodes"]
    errors: list[str] = []
    price_rows: list[dict] = []
    if product["status"] != "DRAFT":
        errors.append(f"status is {product['status']}, expected DRAFT")
    if product.get("publishedAt"):
        errors.append(f"publishedAt is {product['publishedAt']}, expected null")
    if any(node["isPublished"] for node in product["resourcePublicationsV2"]["nodes"]):
        errors.append("one or more sales-channel publications is live")
    if product["category"]["fullName"] != EXPECTED_TAXONOMY_FULL_NAME:
        errors.append(f"taxonomy is {product['category']['fullName']}")
    if len(live_variants) != len(variants):
        errors.append(f"variant count is {len(live_variants)}, expected {len(variants)}")
    live_skus = sorted(node["sku"] for node in live_variants)
    spec_skus = sorted(spec_by_sku)
    if live_skus != spec_skus:
        errors.append("live SKUs do not match derived SKUs")
    if table_row_count(product["descriptionHtml"]) != len(SIZE_CHART):
        errors.append("size table row count does not match SIZE_CHART")
    if any(part.count("<th>") != 10 for part in re.findall(r"<table.*?</table>", product["descriptionHtml"], re.S)):
        errors.append("one or more live size table does not have 10 headers")
    if [option["name"] for option in product["options"]] != ["Type", "Size"]:
        errors.append("option axes are not Type / Size")
    expected_pairs = {(row["garment"], row["picker_label"]) for row in SIZE_CHART}
    live_pairs = {tuple(option["value"] for option in node["selectedOptions"]) for node in live_variants}
    if live_pairs != expected_pairs:
        errors.append("live Type x Size option combinations do not match")
    joined_product_data = json.dumps(
        {
            "title": product["title"],
            "descriptionHtml": product["descriptionHtml"],
            "tags": product["tags"],
            "seo": product["seo"],
            "metafields": product["metafields"]["nodes"],
        },
        ensure_ascii=False,
    ).lower()
    blocked_tokens = ["16" + "88", "ali" + "baba", "detail."]
    if any(token in joined_product_data for token in blocked_tokens):
        errors.append("source URL leaked into Shopify product data")
    for node in live_variants:
        spec = spec_by_sku.get(node["sku"])
        unit_cost = ((node.get("inventoryItem") or {}).get("unitCost") or {}).get("amount")
        cost_ok = unit_cost is not None and Decimal(unit_cost) == Decimal(spec["inventoryItem"]["cost"])
        match = (
            spec is not None
            and node["price"] == spec["price"]
            and node["compareAtPrice"] == spec["compareAtPrice"]
            and node["inventoryPolicy"] == "DENY"
            and node["inventoryItem"]["tracked"]
            and node["inventoryItem"]["requiresShipping"]
            and cost_ok
        )
        if not match:
            errors.append(f"variant mismatch for {node['sku']}")
        price_rows.append(
            {
                "sku": node["sku"],
                "live_price": node["price"],
                "live_compare_at": node["compareAtPrice"],
                "live_cost": unit_cost,
                "spec_price": spec["price"],
                "spec_compare_at": spec["compareAtPrice"],
                "spec_cost": spec["inventoryItem"]["cost"],
                "match": match,
            }
        )
    return errors, price_rows


def write_listing(product_id: str, verify: dict, variants: list[dict], price_rows: list[dict], created_skus: list[str], deleted_skus: list[str]) -> None:
    admin_url = f"https://admin.shopify.com/store/dresslikemommy/products/{product_id.split('/')[-1]}"
    recap = []
    for row, variant in zip(SIZE_CHART, variants):
        gid, label = SIZE_MAP[row["picker_label"]]
        recap.append(
            f"| {row['role']} | {row['vendor_label']} | {row['picker_label']} | {row['garment']} | `{variant['inventoryItem']['sku']}` | {variant['price']} | {variant['inventoryItem']['cost']} | `{gid}` ({label}) |"
        )
    written = sorted(f"{node['namespace']}.{node['key']}" for node in verify["metafields"]["nodes"] if node["namespace"] not in {"judgeme"})
    live_publications = [node["publication"]["name"] for node in verify["resourcePublicationsV2"]["nodes"] if node["isPublished"]]
    skipped = {
        "shopify.fabric": "Exact fiber composition was not visible in the supplied evidence.",
        "shopify.sleeve-length-type": "The product mixes sleeveless dresses, short-sleeve shirts, and shorts; one product-level sleeve value would mislead.",
        "shopify.neckline": "The product mixes dresses, shirts, and shorts; one product-level neckline does not apply.",
        "shopify.top-length-type": "The chart provides shirt garment length, but the mixed Outfit Sets product makes one top-length metafield too broad.",
        "shopify.dress-occasion": "The product is not a dress-only listing.",
        "shopify.dress-style": "The product mixes dresses, shirts, and shorts, so one dress style would not describe every variant.",
        "shopify.skirt-dress-length-type": "The product mixes dresses, shirts, and shorts, so one skirt/dress length value would not describe every variant.",
    }
    collections = sorted(node["handle"] for node in verify["collections"]["nodes"]) or ["collection indexing may wait until publication"]
    lines = [
        f"# {TITLE}",
        "",
        "## Links",
        f"- **Admin:** {admin_url}",
        "- **Live:** not published",
        f"- **Vendor:** {VENDOR_REFERENCE}",
        f"- **Product GID:** `{product_id}`",
        f"- **Handle:** `{HANDLE}`",
        "",
        "## Inputs (resolved)",
        "| Field | Value |",
        "|---|---|",
        f"| VENDOR_URL | {VENDOR_REFERENCE} |",
        "| SIZE_CHART_SOURCE | attached size-chart image plus attached product image |",
        "| LISTING_MODE | Family Matching |",
        "| PRIMARY_CATEGORY | FamilySet / Outfit Sets |",
        "| DESIGNS_TO_LIST | Dress, Shirt, and Shorts |",
        "| FORCE_SPEC_PRICES | true |",
        f"| SHORTCODE | {SHORTCODE} |",
        f"| COLOR_TOKEN | {COLOR_TOKEN} |",
        "",
        "## Vendor Fetch Status",
        "Direct supplier fetch was not used for customer-facing product data. The attached product image and attached size chart were used as authoritative evidence per the canonical workflow, and the supplier URL is redacted from repo artifacts and Shopify product data.",
        "",
        "## Title & SEO",
        "| Field | Value | Chars |",
        "|---|---|---|",
        f"| Product title | `{TITLE}` | {len(TITLE)} |",
        f"| SEO title | `{SEO_TITLE}` | {len(SEO_TITLE)} |",
        f"| SEO description | `{SEO_DESCRIPTION}` | {len(SEO_DESCRIPTION)} |",
        "",
        "## SIZE_CHART / Variant Recap",
        "| Role | Vendor | Picker | Type | SKU | Price | Cost | shopify.size GID |",
        "|---|---|---|---|---|---:|---:|---|",
        *recap,
        "",
        "## Derivations",
        "- Girl dress and mother dress waist/hip values are derived where the vendor chart omits them; the source publishes length, bust/chest, and weight or height guidance.",
        "- Boy and father shirt measurements use the chart's shirt length, chest, and sleeve columns.",
        "- Boy and father shorts use the chart's shorts length and hip columns; waist is derived lower than hip because the source omits waist.",
        "- The 160 child row is mapped to Child 12 Years using the store's existing 160cm size convention.",
        "- Mother 4XL and Father 4XL are retained because the size chart publishes them; both use the store's 4XL size metaobject.",
        "- Pricing follows garment fallback patterns: dress child 28.99, dress adult 31.99, shirt/shorts child 24.99, shirt/shorts adult 28.99; Cost per item is exactly 50%.",
        "- No source/vendor URL or source marketplace token is written to Shopify product title, body, tags, SEO, or metafields.",
        "",
        "## Verification",
        "| Check | Result | Detail |",
        "|---|---|---|",
        f"| Product status is DRAFT | {'PASS' if verify['status'] == 'DRAFT' else 'FAIL'} | {verify['status']} |",
        f"| publishedAt is null | {'PASS' if not verify.get('publishedAt') else 'FAIL'} | {verify.get('publishedAt')} |",
        f"| No sales-channel publications live | {'PASS' if not live_publications else 'FAIL'} | {live_publications} |",
        f"| Variant count matches SIZE_CHART | {'PASS' if len(verify['variants']['nodes']) == len(SIZE_CHART) else 'FAIL'} | {len(verify['variants']['nodes'])} vs {len(SIZE_CHART)} |",
        f"| Price and cost parity | {'PASS' if all(row['match'] for row in price_rows) else 'FAIL'} | {len(price_rows)} variants checked |",
        f"| Taxonomy fullName matches | {'PASS' if verify['category']['fullName'] == EXPECTED_TAXONOMY_FULL_NAME else 'FAIL'} | {verify['category']['fullName']} |",
        f"| Created SKUs | INFO | {', '.join(created_skus) if created_skus else 'none'} |",
        f"| Deleted stale SKUs | INFO | {', '.join(deleted_skus) if deleted_skus else 'none'} |",
        "",
        "## Price and Cost Parity",
        "| SKU | Live Price | Live Compare-at | Live Cost | Spec Price | Spec Compare-at | Spec Cost | Match |",
        "|---|---:|---:|---:|---:|---:|---:|---|",
        *[
            f"| `{row['sku']}` | {row['live_price']} | {row['live_compare_at']} | {row['live_cost']} | {row['spec_price']} | {row['spec_compare_at']} | {row['spec_cost']} | {'yes' if row['match'] else 'no'} |"
            for row in price_rows
        ],
        "",
        "## Metafields Written",
        *[f"- `{key}`" for key in written],
        "",
        "## Metafields Skipped",
        *[f"- `{key}`: {reason}" for key, reason in skipped.items()],
        "",
        "## Smart Collections",
        ", ".join(collections),
        "",
        "## Manual Follow-ups",
        "- Confirm exact fabric composition if the vendor page becomes fully readable later.",
        "- Inventory quantities and variant grams remain operator stock inputs.",
        "- Review the product image crop before any separate publish-live request.",
        "",
        "## Files Saved",
        f"- `{SCRIPT_PATH}`",
        f"- `{LISTING_MD}`",
        f"- `{CSV_OUT}`",
        f"- `{SIZE_CHART_OUT}`",
        f"- `{BODY_HTML_OUT}`",
        f"- `{VERIFY_JSON_OUT}`",
        f"- `{UPLOAD_DIR}`",
    ]
    LISTING_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    (ROOT / "ops/listings").mkdir(parents=True, exist_ok=True)
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    body = build_body()
    variants = build_variants()
    validate_preflight(body, variants)
    run_variant_model_guard()
    SIZE_CHART_OUT.write_text(json.dumps(SIZE_CHART, indent=2), encoding="utf-8")
    BODY_HTML_OUT.write_text(body, encoding="utf-8")
    write_csv(body, variants)

    tax = gql("""query($id:ID!){ node(id:$id){ __typename ... on TaxonomyCategory{id fullName isLeaf} } }""", {"id": TAXONOMY_GID})["data"]["node"]
    if tax["fullName"] != EXPECTED_TAXONOMY_FULL_NAME or not tax["isLeaf"]:
        raise RuntimeError(f"Taxonomy guard failed: {tax}")

    product_options = [
        {"name": "Type", "values": [{"name": value} for value in ["Dress", "Shirt", "Shorts"]]},
        {"name": "Size", "values": [{"name": value} for value in list(dict.fromkeys(row["picker_label"] for row in SIZE_CHART))]},
    ]
    product_input = {
        "handle": HANDLE,
        "title": TITLE,
        "descriptionHtml": body,
        "vendor": VENDOR,
        "productType": PRODUCT_TYPE,
        "tags": tags(),
        "status": "DRAFT",
        "category": TAXONOMY_GID,
        "seo": {"title": SEO_TITLE, "description": SEO_DESCRIPTION},
    }

    product = product_query(HANDLE, by_handle=True)
    if product and product["status"] == "DRAFT":
        raise RuntimeError(f"Existing product {HANDLE} is ACTIVE; refusing draft-only update")
    if product:
        product_id = product["id"]
        res = gql("""mutation($product:ProductUpdateInput!){ productUpdate(product:$product){ product{id handle title status} userErrors{field message} } }""", {"product": {"id": product_id, **product_input}})
        require_no_user_errors(res, ["data", "productUpdate", "userErrors"])
        unpublish(product_id, product)
    else:
        res = gql("""mutation($input:ProductInput!){ productCreate(input:$input){ product{id handle title status} userErrors{field message} } }""", {"input": {**product_input, "productOptions": product_options}})
        require_no_user_errors(res, ["data", "productCreate", "userErrors"])
        product_id = res["data"]["productCreate"]["product"]["id"]

    product = product_query(product_id)
    assert product is not None
    spec_by_sku = {variant["inventoryItem"]["sku"]: variant for variant in variants}
    live_by_sku = {variant.get("sku"): variant for variant in product["variants"]["nodes"] if variant.get("sku")}
    delete_ids = [variant["id"] for sku, variant in live_by_sku.items() if sku not in spec_by_sku]
    deleted_skus = sorted(sku for sku in live_by_sku if sku not in spec_by_sku)
    if delete_ids:
        res = gql("""mutation($productId:ID!,$ids:[ID!]!){ productVariantsBulkDelete(productId:$productId, variantsIds:$ids){ product{id} userErrors{field message} } }""", {"productId": product_id, "ids": delete_ids})
        require_no_user_errors(res, ["data", "productVariantsBulkDelete", "userErrors"])

    product = product_query(product_id)
    assert product is not None
    live_by_sku = {variant.get("sku"): variant for variant in product["variants"]["nodes"] if variant.get("sku")}
    create_variants = [variant for sku, variant in spec_by_sku.items() if sku not in live_by_sku]
    created_skus = sorted(variant["inventoryItem"]["sku"] for variant in create_variants)
    if create_variants:
        res = gql("""mutation($productId:ID!,$variants:[ProductVariantsBulkInput!]!,$strategy:ProductVariantsBulkCreateStrategy){ productVariantsBulkCreate(productId:$productId, variants:$variants, strategy:$strategy){ productVariants{id sku title price compareAtPrice inventoryPolicy inventoryItem{tracked requiresShipping unitCost{amount currencyCode}}} userErrors{field message} } }""", {"productId": product_id, "variants": create_variants, "strategy": "REMOVE_STANDALONE_VARIANT"})
        require_no_user_errors(res, ["data", "productVariantsBulkCreate", "userErrors"])

    product = product_query(product_id)
    assert product is not None
    live_by_sku = {variant.get("sku"): variant for variant in product["variants"]["nodes"] if variant.get("sku")}
    update_variants = []
    for sku, spec in spec_by_sku.items():
        live = live_by_sku.get(sku)
        if not live:
            continue
        update_variants.append(
            {
                "id": live["id"],
                "price": spec["price"],
                "compareAtPrice": spec["compareAtPrice"],
                "taxable": True,
                "inventoryPolicy": "DENY",
                "inventoryItem": spec["inventoryItem"],
                "optionValues": spec["optionValues"],
            }
        )
    if update_variants:
        res = gql("""mutation($productId:ID!,$variants:[ProductVariantsBulkInput!]!){ productVariantsBulkUpdate(productId:$productId, variants:$variants){ productVariants{id sku title price compareAtPrice inventoryPolicy inventoryItem{tracked requiresShipping unitCost{amount currencyCode}}} userErrors{field message} } }""", {"productId": product_id, "variants": update_variants})
        require_no_user_errors(res, ["data", "productVariantsBulkUpdate", "userErrors"])

    mfs = metafields(product_id)
    for i in range(0, len(mfs), 25):
        res = gql("""mutation($metafields:[MetafieldsSetInput!]!){ metafieldsSet(metafields:$metafields){ metafields{namespace key type value} userErrors{field message} } }""", {"metafields": mfs[i:i + 25]})
        require_no_user_errors(res, ["data", "metafieldsSet", "userErrors"])

    product = product_query(product_id)
    assert product is not None
    upload_media(product_id, product["media"]["nodes"])
    time.sleep(2)
    verify = product_query(product_id)
    assert verify is not None
    VERIFY_JSON_OUT.write_text(json.dumps({"data": {"product": verify}}, indent=2), encoding="utf-8")
    errors, price_rows = verify_product(verify, variants)
    write_listing(product_id, verify, variants, price_rows, created_skus, deleted_skus)
    if errors:
        raise RuntimeError("FINAL VERIFY FAILED:\n- " + "\n- ".join(errors))
    print(
        json.dumps(
            {
                "admin_url": f"https://admin.shopify.com/store/dresslikemommy/products/{product_id.split('/')[-1]}",
                "status": verify["status"],
                "publishedAt": verify["publishedAt"],
                "onlineStoreUrl": verify["onlineStoreUrl"],
                "variant_count": len(verify["variants"]["nodes"]),
                "price_cost_parity": all(row["match"] for row in price_rows),
                "source_url_leak_check": "pass",
                "files": [str(LISTING_MD), str(CSV_OUT), str(VERIFY_JSON_OUT), str(SIZE_CHART_OUT), str(BODY_HTML_OUT)],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
PY
