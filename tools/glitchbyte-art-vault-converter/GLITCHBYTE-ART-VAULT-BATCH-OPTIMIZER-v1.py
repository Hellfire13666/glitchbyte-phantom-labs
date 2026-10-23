#!/usr/bin/env python3
"""GlitchByte Art Vault: offline batch converter for a 1 MiB/upload gallery.

Place artwork in ~/Pictures/GlitchByte-To-Upload and run this file with Python 3.
Outputs separate WebP copies in ~/Pictures/GlitchByte-Upload-Ready.
Original files are never modified or removed.
"""
import argparse
import io
import sys
from pathlib import Path

MAX_BYTES = 900 * 1024  # 900 KiB, below the site's 1 MiB image limit
SOURCE_NAME = "GlitchByte-To-Upload"
DEST_NAME = "GlitchByte-Upload-Ready"
EXTS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff"}


def prepare_image(src):
    from PIL import Image, ImageOps, UnidentifiedImageError

    # Pillow guards against decompression-bomb image sizes by default.
    with Image.open(src) as opened:
        if getattr(opened, "is_animated", False) and getattr(opened, "n_frames", 1) > 1:
            raise ValueError("animated images are skipped to avoid losing animation")
        img = ImageOps.exif_transpose(opened)
        img.load()
        if img.mode == "P" and "transparency" in img.info:
            img = img.convert("RGBA")
        elif img.mode not in ("RGB", "RGBA"):
            img = img.convert("RGBA" if "A" in img.getbands() else "RGB")
        return img


def encode_to_limit(img, max_bytes=MAX_BYTES):
    from PIL import Image

    original_max = max(img.size)
    # Lower dimensions only when needed; retain aspect ratio, never upscale.
    for cap in (2400, 2048, 1920, 1600, 1440, 1280, 1024, 900, 768, 640, 512, 400, 320):
        if cap >= original_max and cap != 2400:
            continue
        if cap >= original_max:
            candidate = img
        else:
            candidate = img.copy()
            candidate.thumbnail((cap, cap), Image.Resampling.LANCZOS)
        for quality in (91, 86, 81, 76, 70, 64, 58, 50, 42, 34, 26):
            out = io.BytesIO()
            # EXIF, GPS and ICC metadata deliberately excluded for privacy/space.
            candidate.save(out, format="WEBP", quality=quality, method=5)
            data = out.getvalue()
            if len(data) <= max_bytes:
                return data, candidate.size, quality
    raise ValueError("could not fit artwork within 900 KiB; try a smaller crop")


def process_folder(source, destination, force=False):
    if not source.exists() or not source.is_dir():
        source.mkdir(parents=True, exist_ok=True)
        print(f"[SETUP] Created input folder: {source}")
        print("[NEXT] Copy your PNG/JPG/WebP pictures into it, then run this command again.")
        return 0, 0, 0
    all_files = sorted(p for p in source.rglob("*") if p.is_file() and p.suffix.lower() in EXTS)
    if not all_files:
        print(f"[EMPTY] No supported pictures found inside: {source}")
        print("Copy your artwork into this folder and run this command again.")
        return 0, 0, 0
    ok = skipped = failed = 0
    print(f"[SOURCE] {source}")
    print(f"[COPIES] {destination}")
    print(f"[TARGET] Each file <= {MAX_BYTES // 1024} KiB (WebP)")
    print(f"[FOUND] {len(all_files)} images\n")
    for index, src in enumerate(all_files, 1):
        relative = src.relative_to(source)
        # Always include original extension in output name to avoid foo.png/foo.jpg collisions.
        rel_out = relative.with_name(relative.stem + "_" + relative.suffix[1:].lower() + ".webp")
        output = destination / rel_out
        if output.exists() and not force:
            skipped += 1
            print(f"[{index}/{len(all_files)}] SKIP already exists: {rel_out}")
            continue
        try:
            image = prepare_image(src)
            compressed, (width, height), quality = encode_to_limit(image)
            output.parent.mkdir(parents=True, exist_ok=True)
            # Atomic overwrite of generated copies only. Originals remain unchanged.
            temp = output.with_name(output.name + ".partial")
            try:
                temp.write_bytes(compressed)
                temp.replace(output)
            finally:
                if temp.exists():
                    temp.unlink()
            ok += 1
            before = src.stat().st_size
            print(f"[{index}/{len(all_files)}] PASS {relative} -> {rel_out} "
                  f"| {before/1024:.0f} KiB -> {len(compressed)/1024:.0f} KiB "
                  f"| {width}x{height} Q{quality}")
        except Exception as exc:
            failed += 1
            print(f"[{index}/{len(all_files)}] FAILED {relative}: {exc}")
    print(f"\n[COMPLETE] {ok} ready | {skipped} already done | {failed} failed")
    print(f"[UPLOAD] Select files from: {destination}")
    print(f"[ORIGINALS] Unchanged in: {source}")
    return ok, skipped, failed


def main(argv=None):
    parser = argparse.ArgumentParser(description="Batch prepare images for the GlitchByte Art Vault (offline).")
    parser.add_argument("--source", type=Path, default=Path.home()/"Pictures"/SOURCE_NAME,
                        help="folder of original photos (default: ~/Pictures/GlitchByte-To-Upload)")
    parser.add_argument("--dest", type=Path, default=Path.home()/"Pictures"/DEST_NAME,
                        help="folder for upload-ready WebP copies")
    parser.add_argument("--force", action="store_true", help="recreate copies that already exist")
    args = parser.parse_args(argv)
    source, dest = args.source.expanduser().resolve(), args.dest.expanduser().resolve()
    if source == dest or source in dest.parents or dest in source.parents:
        parser.error("source and destination must be separate, non-nested folders")
    try:
        from PIL import Image
    except ImportError:
        print("[MISSING] Pillow image support is not installed.")
        print("[ONE-TIME FIX] In MX Linux terminal: sudo apt install python3-pil")
        return 2
    _, _, failures = process_folder(source, dest, args.force)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
