"""Render a local review video from accepted stills; no network or source mutation."""

import hashlib
import json
import math
import subprocess
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageStat


HERE = Path(__file__).resolve().parent
CAMPAIGN = HERE.parent
ACCEPTANCE = CAMPAIGN / "CREATIVE_ACCEPTANCE.json"
FFMPEG = "/opt/homebrew/bin/ffmpeg"
FFPROBE = "/opt/homebrew/bin/ffprobe"
VIDEO = HERE / "mommy_and_me_15s_silent_draft.mp4"
WIDTH, HEIGHT, FPS, SECONDS = 1920, 1080, 30, 15
BACKGROUND, INK = (249, 247, 243), (34, 39, 43)
FONT_REGULAR = "/System/Library/Fonts/Supplemental/Arial.ttf"
FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
BRAND = "Dress Like Mommy"
COPY = {
    "Dress Like Mommy",
    "Matching Mommy & Me Styles",
    "Choose Each Person's Size",
    "Explore Matching Family Styles",
    "Shop DressLikeMommy.com",
}
SCENES = [
    {"name": "RGHM_landscape_v1.png", "title": "Matching Mommy & Me Styles", "cta": "Shop DressLikeMommy.com"},
    {"name": "TGHW_landscape_v1.png", "title": "Explore Matching Family Styles", "cta": "Choose Each Person's Size"},
    {"name": "NSPR_landscape_v1.png", "title": "Choose Each Person's Size", "cta": "Shop DressLikeMommy.com"},
]
SAMPLE_TIMES = [1.0, 4.7, 4.966667, 5.3, 7.5, 9.966667, 10.3, 12.5, 14.9]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save_json(name, data):
    (HERE / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def command(args):
    result = subprocess.run(args, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(f"Local command failed ({result.returncode}): {args[0]}\n{result.stderr[-2500:]}")
    return result


def centered_text(canvas, text, top, font):
    assert text in COPY
    draw = ImageDraw.Draw(canvas)
    box = draw.textbbox((0, 0), text, font=font)
    text_width, text_height = box[2] - box[0], box[3] - box[1]
    left = (WIDTH - text_width) // 2
    draw.text((left - box[0], top - box[1]), text, font=font, fill=INK)
    return [left, top, left + text_width, top + text_height]


started_at = datetime.now(timezone.utc).isoformat()
assert Path(FFMPEG).is_file() and Path(FFPROBE).is_file()
assert Path(FONT_REGULAR).is_file() and Path(FONT_BOLD).is_file()
assert not VIDEO.exists(), "Refusing to overwrite an existing video draft"
acceptance = json.loads(ACCEPTANCE.read_text())
acceptance_hash = digest(ACCEPTANCE)
accepted = {Path(a["file"]).name: a for a in acceptance["accepted_with_limits"]}
assert set(accepted) == {s["name"] for s in SCENES}
assert not any("SBF" in s["name"] for s in SCENES)
version = command([FFMPEG, "-hide_banner", "-version"]).stdout
(HERE / "ffmpeg_version.txt").write_text(version)
brand_font = ImageFont.truetype(FONT_BOLD, 40)
title_font = ImageFont.truetype(FONT_REGULAR, 31)
cta_font = ImageFont.truetype(FONT_BOLD, 28)
base = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
brand_box = centered_text(base, BRAND, 32, brand_font)
frames, sources, expected_photos = [], [], []
for index, scene in enumerate(SCENES):
    record = accepted[scene["name"]]
    path = CAMPAIGN / record["file"]
    assert digest(path) == record["sha256"], path
    with Image.open(path) as opened:
        source = opened.convert("RGB")
        assert source.size == (record["width"], record["height"])
    # Full-image fit, one uniform scale factor; no crop, warp, retouch or resynthesis.
    scale = min(1664 / source.width, 800 / source.height)
    size = (round(source.width * scale), round(source.height * scale))
    photo = source.resize(size, Image.Resampling.LANCZOS)
    left, top = (WIDTH - photo.width) // 2, 162
    photo_box = [left, top, left + photo.width, top + photo.height]
    frame = base.copy()
    frame.paste(photo, (left, top))
    title_box = centered_text(frame, scene["title"], 101, title_font)
    cta_box = centered_text(frame, scene["cta"], 1009, cta_font)
    for box in [brand_box, title_box, cta_box]:
        assert box[0] >= 0 and box[2] <= WIDTH and box[1] >= 0 and box[3] <= HEIGHT
        assert box[3] < photo_box[1] or box[1] > photo_box[3], "Text overlaps photograph"
    frames.append(frame)
    expected_photos.append(photo)
    sources.append({"file": "../" + record["file"], "sha256": record["sha256"],
                    "width": source.width, "height": source.height,
                    "source_rectangle": [0, 0, source.width, source.height],
                    "video_photo_rectangle": photo_box, "fit": "CONTAIN_FULL_IMAGE_NO_CROP",
                    "start_seconds": index * 5, "end_seconds": (index + 1) * 5,
                    "on_screen_copy": [BRAND, scene["title"], scene["cta"]],
                    "text_rectangles": [brand_box, title_box, cta_box]})

args = [FFMPEG, "-hide_banner", "-loglevel", "warning", "-n", "-f", "rawvideo",
        "-pix_fmt", "rgb24", "-s:v", f"{WIDTH}x{HEIGHT}", "-r", str(FPS), "-i", "pipe:0",
        "-an", "-c:v", "libx264", "-preset", "medium", "-tune", "stillimage", "-crf", "18",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-frames:v", str(FPS * SECONDS),
        "-metadata", "title=Matching Mommy & Me Styles",
        "-metadata", "comment=Silent local review draft; no audio track; no upload or platform acceptance implied",
        str(VIDEO)]
with (HERE / "encode.log").open("w") as log:
    process = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=log)
    try:
        for scene_index, frame in enumerate(frames):
            still_bytes = frame.tobytes()
            for local_frame in range(5 * FPS):
                fade_in = min(1.0, local_frame / 6)
                fade_out = min(1.0, (149 - local_frame) / 6) if scene_index < 2 else 1.0
                alpha = min(fade_in, fade_out)
                payload = still_bytes if alpha == 1 else Image.blend(base, frame, alpha).tobytes()
                process.stdin.write(payload)
        process.stdin.close()
        returncode = process.wait()
    except Exception:
        process.kill()
        process.wait()
        raise
assert returncode == 0, "FFmpeg encoding failed; see encode.log"

probe_args = [FFPROBE, "-v", "error", "-count_frames", "-show_streams", "-show_format", "-of", "json", str(VIDEO)]
probe = json.loads(command(probe_args).stdout)
save_json("ffprobe.json", probe)
video_streams = [s for s in probe["streams"] if s["codec_type"] == "video"]
audio_streams = [s for s in probe["streams"] if s["codec_type"] == "audio"]
assert len(video_streams) == 1 and not audio_streams
stream = video_streams[0]
assert (stream["width"], stream["height"]) == (WIDTH, HEIGHT)
assert stream["codec_name"] == "h264" and stream["pix_fmt"] == "yuv420p"
assert stream["avg_frame_rate"] == "30/1" and int(stream["nb_read_frames"]) == 450
assert abs(float(probe["format"]["duration"]) - SECONDS) < 0.001
decode_args = [FFMPEG, "-hide_banner", "-v", "error", "-i", str(VIDEO), "-f", "null", "-"]
decode = command(decode_args)
(HERE / "decode_validation.log").write_text(decode.stderr)

keyframes = HERE / "keyframes"
keyframes.mkdir(exist_ok=True)


def extract_sample(time):
    path = keyframes / (f"frame_{time:06.3f}s.png")
    assert not path.exists(), path
    extract_args = [FFMPEG, "-hide_banner", "-v", "error", "-n", "-ss", str(time),
                    "-i", str(VIDEO), "-frames:v", "1", "-update", "1", str(path)]
    command(extract_args)
    return {"requested_time_seconds": time, "file": "keyframes/" + path.name, "sha256": digest(path)}


with ThreadPoolExecutor(max_workers=3) as executor:
    samples = list(executor.map(extract_sample, SAMPLE_TIMES))
sheet = Image.new("RGB", (1440, 930), (240, 240, 240))
sheet_draw = ImageDraw.Draw(sheet)
caption_font = ImageFont.truetype(FONT_REGULAR, 18)
for index, sample in enumerate(samples):
    with Image.open(HERE / sample["file"]) as sample_image:
        thumb = sample_image.resize((480, 270), Image.Resampling.LANCZOS)
    x, y = (index % 3) * 480, (index // 3) * 310
    sheet.paste(thumb, (x, y))
    sheet_draw.text((x + 12, y + 281), f"Review frame — {sample['requested_time_seconds']:.3f}s", font=caption_font, fill=INK)
sheet.save(HERE / "review_contact_sheet.jpg", quality=93)

# Compare stable decoded image regions with the exact full-image fit used by the renderer.
# This detects unintended framing/encoding problems, not underlying product-image authenticity.
photo_checks = []
for scene_index, sample_index in enumerate([0, 4, 7]):
    sample = samples[sample_index]
    with Image.open(HERE / sample["file"]) as sample_image:
        decoded_photo = sample_image.convert("RGB").crop(sources[scene_index]["video_photo_rectangle"])
    from PIL import ImageChops
    stat = ImageStat.Stat(ImageChops.difference(decoded_photo, expected_photos[scene_index]))
    mse = sum(value * value for value in stat.rms) / 3
    psnr = 10 * math.log10(255 * 255 / mse) if mse else None
    assert psnr is None or psnr > 30, (scene_index, psnr)
    photo_checks.append({"source": SCENES[scene_index]["name"], "sample": sample["file"],
                         "decoded_fitted_photo_psnr_db": None if psnr is None else round(psnr, 3),
                         "framing_and_encoding_check": "PASS"})
assert all(digest(HERE / s["file"]) == s["sha256"] for s in sources)
assert digest(ACCEPTANCE) == acceptance_hash
finished_at = datetime.now(timezone.utc).isoformat()
save_json("manifest.json", {
    "status": "LOCAL_SILENT_VIDEO_DRAFT_READY_FOR_SEPARATE_VISUAL_REVIEW",
    "campaign_id": "24247604341", "asset_group_id": "6746545742",
    "started_at": started_at, "finished_at": finished_at,
    "acceptance_source": "../CREATIVE_ACCEPTANCE.json", "acceptance_sha256": acceptance_hash,
    "video": {"file": VIDEO.name, "sha256": digest(VIDEO), "bytes": VIDEO.stat().st_size,
              "duration_seconds": SECONDS, "width": WIDTH, "height": HEIGHT, "aspect_ratio": "16:9",
              "frame_rate": FPS, "frames": 450, "video_codec": "h264", "pixel_format": "yuv420p",
              "audio": "SILENT_NO_AUDIO_STREAM", "music": "NONE"},
    "sources": sources, "sources_unchanged_after_render": True,
    "allowed_copy": sorted(COPY),
    "claim_basis": "Exact parent-supplied whitelist only; no price, bundle, inventory, material, shipping, promotion or performance claims.",
    "transitions": "Six-frame /0.2-second fade-in; first two scenes fade out over6frames to neutral background. Brand stays visible. No overlapping product-photo crossfade. Final CTA holds through end.",
    "rendering": "Already-installed Pillow and system fonts compose video frames in memory; FFmpeg encodes piped raw RGB. No standalone altered product image is created.",
    "font_files": [FONT_REGULAR, FONT_BOLD], "encode_command": args, "probe_command": probe_args,
    "decode_command": decode_args, "sampled_frames": samples,
    "contact_sheet": {"file": "review_contact_sheet.jpg", "sha256": digest(HERE / "review_contact_sheet.jpg"),
                      "purpose": "QA artifact only; thumbnails of decoded video frames"},
    "review_limit": "Underlying accepted images retain CREATIVE_ACCEPTANCE.json source-detail limitations. Technical validity does not prove Google upload eligibility, ad acceptance, Excellent Ad Strength, conversions or profit.",
    "external_requests": 0, "package_installs": 0, "new_image_generation": 0, "uploads": 0, "publication": "NOT_RUN",
})
save_json("VALIDATION.json", {"status": "TECHNICAL_PASS_VISUAL_REVIEW_PENDING", "duration_seconds": 15,
                             "frames": 450, "video_streams": 1, "audio_streams": 0,
                             "h264_1920x1080_30fps_yuv420p": "PASS", "full_decode": "PASS",
                             "exact_accepted_source_hashes": "PASS", "rejected_sbf_excluded": True,
                             "all_source_pixels_in_frame": "PASS_NO_CROP", "text_outside_photo": "PASS",
                             "decoded_photo_checks": photo_checks, "sampled_keyframes": len(samples),
                             "standalone_product_image_edits": 0, "separate_visual_review": "PENDING"})
print(json.dumps({"status": "TECHNICAL_PASS_VISUAL_REVIEW_PENDING", "video": str(VIDEO),
                  "duration": 15, "dimensions": "1920x1080", "fps": 30, "frames": 450,
                  "audio_streams": 0, "keyframes": len(samples), "bytes": VIDEO.stat().st_size,
                  "photo_checks": photo_checks}))
