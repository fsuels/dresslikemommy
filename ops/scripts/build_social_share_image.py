#!/usr/bin/env python3
"""Build the homepage social share image from a supplied background image."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageColor, ImageDraw, ImageFilter, ImageFont


TARGET_WIDTH = 1200
TARGET_HEIGHT = 628
TARGET_ASPECT = TARGET_WIDTH / TARGET_HEIGHT

PALETTE = {
    "dusty_rose": "#D4A5A5",
    "warm_gold": "#D4A44C",
    "cream": "#FFF8F0",
    "dark_brown": "#5C3D2E",
    "soft_coral": "#E8967A",
}

TITLE_FONT_CANDIDATES = [
    "/System/Library/Fonts/Supplemental/Georgia Bold Italic.ttf",
    "/System/Library/Fonts/Supplemental/Baskerville.ttc",
    "/System/Library/Fonts/Supplemental/NewYorkItalic.ttf",
]

SANS_FONT_CANDIDATES = [
    "/System/Library/Fonts/Supplemental/HelveticaNeue.ttc",
    "/System/Library/Fonts/Supplemental/Avenir Next.ttc",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create the Dress Like Mommy homepage social share image."
    )
    parser.add_argument("--source", required=True, help="Path to the source background image.")
    parser.add_argument("--output", required=True, help="Path to the rendered JPG/PNG output.")
    parser.add_argument(
        "--crop-top",
        type=int,
        default=100,
        help="Top offset for the crop before resizing to 1200x628.",
    )
    parser.add_argument(
        "--quality",
        type=int,
        default=84,
        help="JPEG quality for JPG output.",
    )
    return parser.parse_args()


def load_font(candidates: list[str], size: int) -> ImageFont.FreeTypeFont:
    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            return ImageFont.truetype(str(path), size)
    raise FileNotFoundError(f"No usable font found from: {candidates}")


def build_background(source_path: Path, crop_top: int) -> Image.Image:
    image = Image.open(source_path).convert("RGB")
    crop_height = round(image.width / TARGET_ASPECT)
    crop_bottom = crop_top + crop_height

    if crop_top < 0 or crop_bottom > image.height:
        raise ValueError(
            f"Crop top {crop_top} is invalid for source size {image.size}; "
            f"needs crop height {crop_height}."
        )

    cropped = image.crop((0, crop_top, image.width, crop_bottom))
    return cropped.resize((TARGET_WIDTH, TARGET_HEIGHT), Image.Resampling.LANCZOS)


def build_overlay() -> Image.Image:
    overlay = Image.new("RGBA", (TARGET_WIDTH, TARGET_HEIGHT), (0, 0, 0, 0))
    cream_rgb = ImageColor.getrgb(PALETTE["cream"])
    pixels = overlay.load()
    max_opaque_x = 600
    fade_end_x = 785

    for x in range(TARGET_WIDTH):
        if x <= max_opaque_x:
            alpha = 255
        elif x >= fade_end_x:
            alpha = 0
        else:
            fade = (x - max_opaque_x) / (fade_end_x - max_opaque_x)
            alpha = int(255 * (1 - fade))

        tinted = (*cream_rgb, alpha)
        for y in range(TARGET_HEIGHT):
            pixels[x, y] = tinted

    glow = Image.new("RGBA", (TARGET_WIDTH, TARGET_HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(glow)
    draw.ellipse(
        (-180, -160, 830, 540),
        fill=(*ImageColor.getrgb(PALETTE["warm_gold"]), 70),
    )
    draw.ellipse(
        (190, 150, 760, 720),
        fill=(*ImageColor.getrgb(PALETTE["soft_coral"]), 34),
    )

    return Image.alpha_composite(overlay, glow.filter(ImageFilter.GaussianBlur(68)))


def draw_cta(
    image: Image.Image, x: int, y: int, font: ImageFont.FreeTypeFont
) -> tuple[Image.Image, tuple[int, int, int, int]]:
    draw = ImageDraw.Draw(image)
    pill_height = 60
    padding_x = 26
    arrow_gap = 22
    arrow_length = 18
    head_length = 8
    copy_gap = 16
    shop_copy = "Shop Now"
    domain_copy = "dresslikemommy.com"

    shop_box = draw.textbbox((0, 0), shop_copy, font=font)
    domain_box = draw.textbbox((0, 0), domain_copy, font=font)
    shop_width = shop_box[2] - shop_box[0]
    domain_width = domain_box[2] - domain_box[0]
    pill_width = padding_x * 2 + shop_width + arrow_gap + arrow_length + copy_gap + domain_width
    pill_bounds = (x, y, x + pill_width, y + pill_height)

    shadow = Image.new("RGBA", image.size, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rounded_rectangle(
        (pill_bounds[0] + 5, pill_bounds[1] + 8, pill_bounds[2] + 5, pill_bounds[3] + 8),
        radius=30,
        fill=(92, 61, 46, 46),
    )
    composed = Image.alpha_composite(image, shadow.filter(ImageFilter.GaussianBlur(10)))
    draw = ImageDraw.Draw(composed)

    draw.rounded_rectangle(
        pill_bounds,
        radius=30,
        fill=PALETTE["dusty_rose"],
        outline="#C58F8F",
        width=2,
    )

    text_y = y + 13
    text_color = PALETTE["dark_brown"]
    draw.text((x + padding_x, text_y), shop_copy, font=font, fill=text_color)

    arrow_x = x + padding_x + shop_width + arrow_gap
    arrow_y = y + pill_height // 2
    draw.line((arrow_x, arrow_y, arrow_x + arrow_length, arrow_y), fill=text_color, width=4)
    draw.polygon(
        [
            (arrow_x + arrow_length, arrow_y),
            (arrow_x + arrow_length - head_length, arrow_y - head_length + 1),
            (arrow_x + arrow_length - head_length, arrow_y + head_length - 1),
        ],
        fill=text_color,
    )
    draw.text(
        (arrow_x + arrow_length + copy_gap, text_y),
        domain_copy,
        font=font,
        fill=text_color,
    )
    return composed, pill_bounds


def render_social_image(source_path: Path, crop_top: int) -> Image.Image:
    background = build_background(source_path, crop_top).convert("RGBA")
    composed = Image.alpha_composite(background, build_overlay())
    draw = ImageDraw.Draw(composed)

    title_font = load_font(TITLE_FONT_CANDIDATES, 78)
    sans_font = load_font(SANS_FONT_CANDIDATES, 37)
    fine_font = load_font(SANS_FONT_CANDIDATES, 26)
    cta_font = load_font(SANS_FONT_CANDIDATES, 29)

    x = 60
    y = 92

    for line in ("Dress Like", "Mommy"):
        draw.text((x, y), line, font=title_font, fill=PALETTE["dark_brown"])
        y = draw.textbbox((x, y), line, font=title_font)[3] + 8

    draw.multiline_text(
        (x + 4, y + 18),
        "Matching Outfits\nfor the Whole Family",
        font=sans_font,
        fill=PALETTE["dark_brown"],
        spacing=10,
    )

    divider_y = y + 120
    draw.rounded_rectangle(
        (x + 4, divider_y, x + 292, divider_y + 4),
        radius=2,
        fill=PALETTE["warm_gold"],
    )
    draw.text(
        (x + 4, divider_y + 24),
        "Free Shipping · 30-Day Returns",
        font=fine_font,
        fill=PALETTE["dark_brown"],
    )

    composed, _ = draw_cta(composed, x, divider_y + 68, cta_font)
    return composed.convert("RGB")


def save_image(image: Image.Image, output_path: Path, quality: int) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    suffix = output_path.suffix.lower()

    if suffix in {".jpg", ".jpeg"}:
        image.save(output_path, quality=quality, optimize=True, progressive=True)
        return

    if suffix == ".png":
        image.save(output_path, optimize=True)
        return

    raise ValueError(f"Unsupported output type for {output_path}")


def main() -> None:
    args = parse_args()
    source_path = Path(args.source)
    output_path = Path(args.output)
    image = render_social_image(source_path, args.crop_top)
    save_image(image, output_path, args.quality)


if __name__ == "__main__":
    main()
