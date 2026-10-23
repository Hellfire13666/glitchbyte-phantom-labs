#!/usr/bin/env python3
"""GlitchByte Phantom Labs Art Vault New-Only Converter v2.

Converted-file history is stored outside both picture folders, so clearing
GlitchByte-Upload-Ready does not recreate previously processed pictures.
Original source artwork is never changed/deleted. Works entirely offline.
"""
import argparse
import hashlib
import io
import json
import os
import sys
from pathlib import Path

SOURCE_NAME = "GlitchByte-To-Upload"
DEST_NAME = "GlitchByte-Upload-Ready"
MAX_BYTES = 900 * 1024
EXTS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff"}


def state_path():
    default = Path.home() / ".local" / "state"
    base = Path(os.environ.get("XDG_STATE_HOME") or default).expanduser()
    return base / "glitchbyte-phantom-labs" / "art-vault-new-only-v2-history.json"


def read_history(path):
    if not path.exists():
        return {"version": 2, "seen": {}}
    try:
        obj = json.loads(path.read_text(encoding="utf-8"))
        if obj.get("version") != 2 or not isinstance(obj.get("seen"), dict):
            raise ValueError("unknown history version")
        return obj
    except (OSError, ValueError, TypeError) as exc:
        raise RuntimeError(f"History cannot be read ({exc}). Stopping so old photos won't reappear.") from exc


def store_history(path, history):
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    temp = path.with_name(path.name + ".tmp")
    try:
        fd = os.open(temp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        temp.replace(path)
    finally:
        if temp.exists():
            temp.unlink()


def candidates(source):
    if not source.is_dir():
        return []
    return sorted((p for p in source.rglob("*")
                   if p.is_file() and not p.is_symlink()
                   and p.suffix.lower() in EXTS), key=lambda p: str(p).lower())


def checksum(path):
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def prepare_image(src):
    from PIL import Image, ImageOps
    with Image.open(src) as opened:
        if getattr(opened, "is_animated", False) and getattr(opened, "n_frames", 1) > 1:
            raise ValueError("animated images are skipped to avoid removing animation")
        img = ImageOps.exif_transpose(opened)
        img.load()
        if img.mode == "P" and "transparency" in img.info:
            img = img.convert("RGBA")
        elif img.mode not in ("RGB", "RGBA"):
            img = img.convert("RGBA" if "A" in img.getbands() else "RGB")
        return img


def encode_to_limit(img):
    from PIL import Image
    largest = max(img.size)
    for cap in (2400, 2048, 1920, 1600, 1440, 1280, 1024, 900, 768, 640, 512, 400, 320):
        if cap >= largest and cap != 2400:
            continue
        if cap >= largest:
            candidate = img
        else:
            candidate = img.copy()
            candidate.thumbnail((cap, cap), Image.Resampling.LANCZOS)
        for quality in (91, 86, 81, 76, 70, 64, 58, 50, 42, 34, 26):
            out = io.BytesIO()
            candidate.save(out, format="WEBP", quality=quality, method=5)
            data = out.getvalue()
            if len(data) <= MAX_BYTES:
                return data, candidate.size
    raise ValueError("Image cannot be compressed below 900 KiB")


def run(source, dest, history_file, remember_existing=False):
    if not source.exists():
        source.mkdir(parents=True, exist_ok=True)
        print(f"[INPUT CREATED] {source}")
    items = candidates(source)
    history = read_history(history_file)
    already = history["seen"]
    print("\n GLITCHBYTE PHANTOM LABS // ART VAULT NEW-ONLY v2")
    print("=" * 57)
    print(f"[ORIGINALS] {source}")
    print(f"[READY]     {dest}")
    print(f"[FILES]     {len(items)} originals found")
    if remember_existing:
        new = 0
        for src in items:
            digest = checksum(src)
            if digest not in already:
                already[digest] = {"source": str(src.relative_to(source)), "status": "remembered_before_upgrade"}
                new += 1
        store_history(history_file, history)
        print(f"[NEW-ONLY SETUP] Remembered {new} existing pictures as ALREADY HANDLED.")
        print("[NEXT] Add a NEW picture to GlitchByte-To-Upload, then run the desktop shortcut.")
        print("[SAFE] No artwork was converted, moved or deleted during setup.")
        return 0
    if not items:
        print("[EMPTY] Copy new pictures into the input folder and run again.")
        return 0
    try:
        from PIL import Image  # noqa: F401
    except ImportError:
        print("[MISSING] Pillow. Install once: sudo apt install python3-pil")
        return 2
    created = skipped = errors = 0
    for index, src in enumerate(items, 1):
        relative = src.relative_to(source)
        try:
            digest = checksum(src)
            if digest in already:
                skipped += 1
                print(f"[{index}/{len(items)}] SKIP remembered: {relative}")
                continue
            image = prepare_image(src)
            data, dimensions = encode_to_limit(image)
            # Content-hash suffix prevents overwriting differently edited originals.
            output_rel = relative.with_name(
                f"{relative.stem}_{relative.suffix[1:].lower()}_{digest[:10]}.webp")
            output = dest / output_rel
            output.parent.mkdir(parents=True, exist_ok=True)
            if output.exists():
                if output.stat().st_size > MAX_BYTES:
                    raise ValueError("existing output unexpectedly exceeds 900 KiB")
            else:
                temp = output.with_name(output.name + ".partial")
                try:
                    temp.write_bytes(data)
                    temp.replace(output)
                finally:
                    if temp.exists():
                        temp.unlink()
            already[digest] = {"source": str(relative), "output": str(output_rel),
                               "status": "converted"}
            store_history(history_file, history)
            created += 1
            print(f"[{index}/{len(items)}] NEW {relative} -> {output_rel}"
                  f" | {src.stat().st_size//1024} KB -> {len(data)//1024} KB")
        except Exception as exc:
            errors += 1
            print(f"[{index}/{len(items)}] ERROR {relative}: {type(exc).__name__}: {exc}")
    print(f"\n[FINISHED] {created} NEW | {skipped} remembered/skipped | {errors} errors")
    print("[NO CLUTTER] Deleted output copies will NOT reappear on future runs.")
    print("[ORIGINALS] Source pictures are not moved, edited or deleted.")
    return 1 if errors else 0


def main(argv=None):
    p = argparse.ArgumentParser(description="Convert ONLY new GlitchByte Art Vault images; remember processed artwork.")
    p.add_argument("--source", type=Path, default=Path.home() / "Desktop" / SOURCE_NAME)
    p.add_argument("--dest", type=Path, default=Path.home() / "Desktop" / DEST_NAME)
    p.add_argument("--history", type=Path, default=state_path())
    p.add_argument("--remember-existing", action="store_true",
                   help="Mark currently present source pictures as already handled, without converting")
    a = p.parse_args(argv)
    source, dest = a.source.expanduser().resolve(), a.dest.expanduser().resolve()
    history_file = a.history.expanduser().resolve()
    if source == dest or source in dest.parents or dest in source.parents:
        p.error("Input and output must be separate, non-nested folders")
    try:
        return run(source, dest, history_file, a.remember_existing)
    except (OSError, RuntimeError) as exc:
        print(f"[STOP] {exc}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
