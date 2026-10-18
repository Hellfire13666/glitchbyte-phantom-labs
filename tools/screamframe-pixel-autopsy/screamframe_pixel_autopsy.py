#!/usr/bin/env python3
"""SCREAMFRAME | Offline screenshot echo and metadata triage.

GlitchByte Phantom Labs. Read-only analysis; no image authentication claims.
"""
from __future__ import annotations

import argparse
import base64
from collections import defaultdict
from datetime import datetime, timezone
import hashlib
from html import escape
from io import BytesIO
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import warnings
import webbrowser

try:
    from PIL import Image, ImageDraw, ImageOps, UnidentifiedImageError
except ImportError:
    print("[ERROR] Pillow missing. Install: python3 -m pip install -r requirements.txt", file=sys.stderr)
    raise SystemExit(2)

Image.MAX_IMAGE_PIXELS = 55_000_000
SUPPORTED = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif", ".tif", ".tiff"}
EXTENSIONS = {
    "PNG": {".png"}, "JPEG": {".jpg", ".jpeg"}, "WEBP": {".webp"},
    "BMP": {".bmp"}, "GIF": {".gif"}, "TIFF": {".tif", ".tiff"},
}
VERSION = "1.0.0"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def difference_hash(image: Image.Image) -> str:
    """64-bit horizontal difference hash; perceptual hint, not proof."""
    gray = ImageOps.grayscale(ImageOps.exif_transpose(image)).resize((9, 8), Image.Resampling.LANCZOS)
    pixels = list(gray.get_flattened_data()) if hasattr(gray, "get_flattened_data") else list(gray.getdata())
    result = 0
    for row in range(8):
        for col in range(8):
            result = (result << 1) | int(pixels[row * 9 + col] > pixels[row * 9 + col + 1])
    return f"{result:016x}"


def hash_distance(left: str, right: str) -> int:
    return (int(left, 16) ^ int(right, 16)).bit_count()


def thumbnail_data_uri(image: Image.Image) -> str:
    image = ImageOps.exif_transpose(image)
    image.thumbnail((256, 154), Image.Resampling.LANCZOS)
    if image.mode not in ("RGB", "RGBA"):
        image = image.convert("RGB")
    stream = BytesIO()
    image.save(stream, format="PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(stream.getvalue()).decode("ascii")


def safe_time(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    # Image EXIF has numerous vendor fields; keep only a plausible timestamp.
    match = re.fullmatch(r"\d{4}:\d\d:\d\d \d\d:\d\d:\d\d", value.strip())
    return value.strip() if match else None


def analyze_file(path: Path, root: Path, *, previews: bool) -> dict:
    before = path.stat()
    entry = {
        "file": path.relative_to(root).as_posix(), "bytes": before.st_size,
        "modified_utc": datetime.fromtimestamp(before.st_mtime, tz=timezone.utc).isoformat(),
        "sha256": None, "dhash64": None, "format": None, "width": None,
        "height": None, "frames": 1, "exif_datetime_original": None,
        "extension_mismatch": False, "warnings": [],
    }
    with warnings.catch_warnings():
        warnings.simplefilter("error", Image.DecompressionBombWarning)
        with Image.open(path) as im:
            entry["format"] = im.format
            entry["width"], entry["height"] = im.size
            entry["frames"] = getattr(im, "n_frames", 1)
            if im.format in EXTENSIONS and path.suffix.lower() not in EXTENSIONS[im.format]:
                entry["extension_mismatch"] = True
                entry["warnings"].append("Extension does not match decoded image format")
            exif = im.getexif()
            if exif:
                entry["exif_datetime_original"] = safe_time(exif.get(36867))
            im.seek(0)
            im.load()
            entry["dhash64"] = difference_hash(im)
            if previews:
                entry["thumbnail_data_uri"] = thumbnail_data_uri(im.copy())
    entry["sha256"] = sha256_file(path)
    after = path.stat()
    if (before.st_size, before.st_mtime_ns, before.st_ino) != (after.st_size, after.st_mtime_ns, after.st_ino):
        raise OSError("File changed during inspection; ignored inconsistent result")
    return entry


def iter_image_paths(root: Path, *, excluded: Path):
    for current, dirs, files in os.walk(root, followlinks=False):
        parent = Path(current)
        dirs[:] = sorted(name for name in dirs if not (parent / name).is_symlink()
                         and not (parent / name).resolve().is_relative_to(excluded))
        for name in sorted(files):
            item = parent / name
            if item.suffix.lower() in SUPPORTED and not item.is_symlink() and not item.resolve().is_relative_to(excluded):
                yield item


def groups_and_pairs(entries: list[dict], threshold: int) -> tuple[list[list[str]], list[dict]]:
    by_sha: dict[str, list[str]] = defaultdict(list)
    for entry in entries:
        by_sha[entry["sha256"]].append(entry["file"])
    exact = [sorted(paths) for paths in by_sha.values() if len(paths) > 1]
    exact.sort()
    similar = []
    for index, a in enumerate(entries):
        for b in entries[index + 1:]:
            if a["sha256"] == b["sha256"]:
                continue
            d = hash_distance(a["dhash64"], b["dhash64"])
            if d <= threshold:
                similar.append({"a": a["file"], "b": b["file"], "distance": d})
    similar.sort(key=lambda item: (item["distance"], item["a"], item["b"]))
    return exact, similar


def scan(root: Path, out: Path, *, max_images: int = 300, max_mb: int = 20,
         threshold: int = 5, previews: bool = False, demo: bool = False) -> dict:
    root = root.resolve(strict=True)
    if not root.is_dir():
        raise ValueError("Folder must be a readable directory")
    out = out.resolve()
    inspected = []
    skipped = []
    limit_bytes = max_mb * 1024 * 1024
    for path in iter_image_paths(root, excluded=out):
        rel = path.relative_to(root).as_posix()
        if len(inspected) >= max_images:
            skipped.append({"file": rel, "reason": f"scan limit ({max_images} images)"})
            continue
        try:
            if path.stat().st_size > limit_bytes:
                skipped.append({"file": rel, "reason": f"size limit ({max_mb} MiB)"})
                continue
            item = analyze_file(path, root, previews=previews)
            inspected.append(item)
            print(f"[{len(inspected):03}] {item['format'] or '?':<5} {item['width']}x{item['height']} {rel}", flush=True)
        except (OSError, ValueError, UnidentifiedImageError, Image.DecompressionBombError,
                Image.DecompressionBombWarning, SyntaxError) as exc:
            skipped.append({"file": rel, "reason": f"{type(exc).__name__}: {str(exc)[:160]}"})
    exact, similar = groups_and_pairs(inspected, threshold)
    report = {
        "tool": "SCREAMFRAME Pixel Autopsy", "version": VERSION,
        "generated_utc": datetime.now(tz=timezone.utc).isoformat(),
        "source": "synthetic demo" if demo else str(root),
        "method": "SHA-256 exact matches; 64-bit difference hash image likeness",
        "threshold": threshold,
        "files": inspected, "exact_duplicate_groups": exact, "visual_echo_pairs": similar,
        "skipped": skipped,
        "counts": {"inspected": len(inspected), "exact_groups": len(exact),
                   "visual_pairs": len(similar), "format_mismatches": sum(e["extension_mismatch"] for e in inspected),
                   "skipped": len(skipped)},
        "notice": "Metadata and perceptual likeness cannot authenticate, attribute, or prove tampering with an image.",
    }
    return report


def render_html(report: dict) -> str:
    c = report["counts"]
    rows = []
    for obj in report["files"]:
        path = escape(obj["file"])
        label = escape(obj["format"] or "?")
        dims = f"{obj['width']} x {obj['height']}"
        badge = '<span class="flag">EXTENSION ALERT</span>' if obj["extension_mismatch"] else ""
        thumb = ('<img alt="Local thumbnail" src="' + escape(obj["thumbnail_data_uri"], quote=True) + '">') if obj.get("thumbnail_data_uri") else '<span class="glyph">▧</span>'
        rows.append(f'<article class="tile" data-filter="{escape(obj["file"].lower(), quote=True)}">'
                    f'<div class="preview">{thumb}</div><div class="info"><h3>{path}</h3>{badge}'
                    f'<p>{label} · {dims} · {obj["bytes"]:,} bytes</p>'
                    f'<p class="digest">SHA-256: {obj["sha256"]}</p>'
                    f'<p class="digest">dHash: {obj["dhash64"]} | EXIF date: {escape(obj["exif_datetime_original"] or "not present")}</p>'
                    '</div></article>')
    echo = "".join(f'<li>{escape(x["a"])} ↔ {escape(x["b"])} <b>(distance {x["distance"]})</b></li>' for x in report["visual_echo_pairs"])
    groups = "".join("<li>" + " = ".join(escape(path) for path in group) + "</li>" for group in report["exact_duplicate_groups"])
    skipped = "".join(f'<li>{escape(x["file"])}: {escape(x["reason"])}</li>' for x in report["skipped"])
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>SCREAMFRAME | Pixel Autopsy</title>
<style>
:root{{--black:#090c0e;--ink:#d9e9e7;--acid:#d2ff37;--orange:#ff713e;--muted:#a1b2b0}}
*{{box-sizing:border-box}}body{{margin:0;background:radial-gradient(circle at 87% 2%,#252f19,transparent 32%),var(--black);color:var(--ink);font:15px/1.6 system-ui,Arial,sans-serif}}
main{{max-width:1160px;margin:auto;padding:32px 20px 80px}}header{{border-bottom:1px solid #4b5940;padding:22px 0 32px}}small,.mono{{font-family:monospace;letter-spacing:.14em;color:var(--acid)}}h1{{font-size:clamp(2.7rem,7vw,6rem);letter-spacing:-.08em;line-height:1;margin:10px 0;color:#f6fbf4}}h1 span{{color:var(--orange)}}
.sub{{max-width:650px;color:var(--muted)}}.stats{{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px;margin:24px 0}}.stat{{padding:20px;border:1px solid #4e6537;border-radius:8px;background:#151a16}}.stat b{{font-size:2rem;color:var(--acid);display:block}}.stat span{{font:12px monospace;letter-spacing:.09em;color:#c1ccc2}}
section{{margin-top:40px}}h2{{color:var(--acid);font-size:1.3rem}}input{{display:block;width:100%;max-width:480px;background:#161d1a;color:var(--ink);border:1px solid #698c4e;padding:12px 15px;border-radius:8px}}
.gallery{{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:14px;margin-top:20px}}.tile{{border:1px solid #334735;background:#151a17;border-radius:10px;overflow:hidden}}.preview{{height:164px;display:grid;place-items:center;background:repeating-linear-gradient(0deg,#1b231e,#1b231e 2px,#1c2920 3px)}}.preview img{{max-height:100%;max-width:100%;object-fit:contain}}.glyph{{font-size:5rem;color:#5d754a}}
.info{{padding:14px 18px;overflow-wrap:anywhere}}.info h3{{margin:0;font-size:1rem}}.info p{{margin:7px 0;color:#b0c1bb}}.digest{{font:11px/1.5 monospace}}.flag{{background:#5e2412;color:#ffb58f;font:12px monospace;padding:2px 5px}}
li{{margin:8px 0;overflow-wrap:anywhere}}.warning{{border-left:3px solid var(--orange);padding-left:14px;color:#e2b49c}}footer{{margin-top:65px;color:#a9bcae;font-size:12px}}
</style></head><body><main><header><small>GLITCHBYTE PHANTOM LABS // ROSIEGLITCHBYTE // LOCAL ONLY</small>
<h1>SCREAM<span>FRAME</span><span style="color:var(--acid)">_</span></h1>
<div class="mono">PIXEL AUTOPSY / VISUAL ECHO STUDIO / {escape(report['generated_utc'][:19])}Z</div>
<p class="sub">Find repeated screenshots, lookalike edits, suspicious extensions, and limited image metadata. Images stay on your machine.</p></header>
<div class="stats">{''.join(f'<div class="stat"><b>{value}</b><span>{escape(label.upper())}</span></div>' for label,value in [('images scanned',c['inspected']),('exact duplicate sets',c['exact_groups']),('visual echo pairs',c['visual_pairs']),('extension flags',c['format_mismatches']),('skipped',c['skipped'])])}</div>
<section><h2>01 / FILE GALLERY</h2><label for="filter">Search local file names</label><input id="filter" type="search" placeholder="Type a filename…" oninput="document.querySelectorAll('.tile').forEach(e=>e.hidden=!e.dataset.filter.includes(this.value.toLowerCase()))"><div class="gallery">{''.join(rows) or '<p>No readable images found.</p>'}</div></section>
<section><h2>02 / BYTE-FOR-BYTE COPIES</h2><ul>{groups or '<li>No exact duplicates found.</li>'}</ul></section>
<section><h2>03 / VISUAL ECHOES (dHash distance ≤ {report['threshold']})</h2><ul>{echo or '<li>No approximate matches found.</li>'}</ul></section>
<section><h2>04 / SKIPPED FILES</h2><ul>{skipped or '<li>None.</li>'}</ul></section>
<section class="warning"><h2>WHAT THIS CANNOT PROVE</h2><p>{escape(report['notice'])} Visual hashes can collide on simple or unrelated images, and EXIF can be edited or absent.</p></section>
<footer>SCREAMFRAME v{VERSION} · Offline only · no uploads · reports may contain private filenames or embedded previews</footer>
</main></body></html>'''


def save_reports(report: dict, out: Path) -> tuple[Path, Path]:
    out.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    prefix = out / f"screamframe_echo_{stamp}"
    json_path, html_path = prefix.with_suffix(".json"), prefix.with_suffix(".html")
    # Thumbnails are available in HTML only; keep JSON reports compact and tidy.
    clean = {**report, "files": [{k: v for k, v in entry.items() if k != "thumbnail_data_uri"} for entry in report["files"]]}
    with json_path.open("x", encoding="utf-8") as f:
        json.dump(clean, f, indent=2, ensure_ascii=False)
    with html_path.open("x", encoding="utf-8") as f:
        f.write(render_html(report))
    return json_path, html_path


def generate_demo(folder: Path) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    im = Image.new("RGB", (620, 320), "#101820")
    draw = ImageDraw.Draw(im)
    draw.rectangle((22, 22, 598, 74), fill="#d2ff37")
    draw.text((44, 40), "SCREAMFRAME :: DEMO SCREENSHOT", fill="#080b0d")
    for i in range(7):
        draw.rectangle((44, 115 + i*25, 310 + i*28, 119 + i*25), fill="#ff713e")
    im.save(folder / "screen_original.png")
    im.save(folder / "screen_exact_copy.png")
    edit = im.copy()
    ImageDraw.Draw(edit).rectangle((475, 195, 498, 215), fill="#6e9c5c")
    edit.save(folder / "screen_small_edit.png")
    different = Image.new("RGB", (550, 400), "#1a2531")
    d = ImageDraw.Draw(different)
    d.ellipse((80, 65, 450, 355), fill="#fa7050")
    d.line((50, 350, 490, 70), fill="white", width=11)
    different.save(folder / "pretend_jpeg.jpg", format="PNG")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="SCREAMFRAME: inspect local screenshots for exact and visual echoes, offline.")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--folder", type=Path, help="Local screenshot directory to inspect read-only")
    source.add_argument("--demo", action="store_true", help="Generate and inspect harmless sample images")
    parser.add_argument("--out", type=Path, default=Path.home() / "ScreamframeEchoReports")
    parser.add_argument("--max-images", type=int, default=300, help="Maximum decoded images (1..5000)")
    parser.add_argument("--max-mb", type=int, default=20, help="Maximum size per image in MiB (1..500)")
    parser.add_argument("--distance", type=int, default=5, help="Visual similarity Hamming distance (0..16)")
    parser.add_argument("--previews", action="store_true", help="Embed thumbnails in local HTML (may contain private imagery)")
    parser.add_argument("--open-browser", action="store_true", help="Open local HTML dashboard in default browser")
    args = parser.parse_args(argv)
    if not (1 <= args.max_images <= 5000 and 1 <= args.max_mb <= 500 and 0 <= args.distance <= 16):
        parser.error("limits: max-images 1..5000, max-mb 1..500, distance 0..16")
    print("\033[38;5;214m✦ SCREAMFRAME\033[0m  :: PIXEL AUTOPSY :: GLITCHBYTE PHANTOM LABS")
    print("[MODE] LOCAL ONLY | READ-ONLY | NO NETWORK")
    try:
        if args.demo:
            with tempfile.TemporaryDirectory(prefix="screamframe-sample-") as temp:
                root = Path(temp)
                generate_demo(root)
                report = scan(root, args.out, max_images=args.max_images, max_mb=args.max_mb,
                              threshold=args.distance, previews=True, demo=True)
        else:
            report = scan(args.folder, args.out, max_images=args.max_images, max_mb=args.max_mb,
                          threshold=args.distance, previews=args.previews)
        j, h = save_reports(report, args.out)
    except (OSError, ValueError) as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 1
    print("[RESULT]", report["counts"])
    print("[JSON]", j)
    print("[REPORT]", h)
    if args.open_browser:
        webbrowser.open(h.resolve().as_uri())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())