#!/usr/bin/env python3
"""Attach real, user-selected artwork to the matching Phantom Labs showcase.

Never invent a PNG link, choose between alternate artwork, alter source files,
or replace a page's color-coded upload door.
"""
from __future__ import annotations
import json
from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "docs" / "TOOL_COVER_MAP.json"
START = "<!-- GLITCHBYTE-ART-COVER:START -->"
END = "<!-- GLITCHBYTE-ART-COVER:END -->"


def build():
    if not MAP.is_file():
        raise RuntimeError("Missing artwork manifest")
    catalog = json.loads(MAP.read_text(encoding="utf-8"))
    touched, skipped = [], []
    for item in catalog["covers"]:
        page_path = ROOT / item["showcase"]
        image_path = ROOT / item["image"]
        if not page_path.is_file():
            raise RuntimeError("Missing actual tool page: " + item["showcase"])
        if not image_path.is_file() and item.get("status") == "user-approved-awaiting-image-upload":
            # If a browser upload preserved a folder, promote only the selected cover.
            base = ROOT / "artwork" / "tool-covers"
            matches = sorted(p for p in base.rglob(image_path.name)
                             if p.is_file() and p != image_path)
            if len(matches) == 1:
                with matches[0].open("rb") as stream:
                    if stream.read(8) != b"\x89PNG\r\n\x1a\n":
                        raise RuntimeError("Invalid approved PNG upload: " + str(matches[0]))
                image_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(matches[0], image_path)
                print("Promoted selected cover:", item["title"], "from", matches[0].relative_to(ROOT))
            elif len(matches) > 1:
                print("Multiple uploaded cover copies; please select one:", item["title"])
        if not image_path.is_file():
            skipped.append(item["title"])
            continue
        # The image has to be a real PNG, not a GitHub LFS pointer or empty placeholder.
        with image_path.open("rb") as stream:
            if stream.read(8) != b"\x89PNG\r\n\x1a\n":
                raise RuntimeError("Invalid PNG art: " + item["image"])
        doc = page_path.read_text(encoding="utf-8")
        image_url = "../../" + item["image"]
        alt = item["title"].replace("[", "").replace("]", "")
        cover = START + "\n\n" + f"![{alt} | GlitchByte Phantom Labs official artwork]({image_url})" + "\n\n" + END
        if START in doc or END in doc:
            if doc.count(START) != 1 or doc.count(END) != 1:
                raise RuntimeError("Malformed existing cover markers: " + item["showcase"])
            revised = re.sub(re.escape(START) + r".*?" + re.escape(END),
                             lambda unused: cover, doc, count=1, flags=re.DOTALL)
        else:
            heading = re.search(r"(?m)^# [^\n]+\n", doc)
            if not heading:
                raise RuntimeError("Missing page title: " + item["showcase"])
            revised = doc[:heading.end()] + "\n" + cover + "\n" + doc[heading.end():]
        if revised != doc:
            page_path.write_text(revised, encoding="utf-8")
            touched.append(item["title"])
    print("New or refreshed art links:", ", ".join(touched) if touched else "none")
    print("Covers not yet uploaded:", ", ".join(skipped) if skipped else "none")
    return touched


if __name__ == "__main__":
    build()
