#!/usr/bin/env python3
"""HEXWAKE Palette Foundry: original offline Glitch HEX palette workstation.

Generate reproducible contrast-aware palettes as JSON, CSS, and a single HTML
preview. No dependencies beyond Python 3, no network access, no tracking.
"""
import argparse
import colorsys
import datetime as dt
import html
import json
from pathlib import Path
import random
import re
import secrets

ANCHORS = (
    ("Signal Pink", "#FF1493"), ("Acid Lime", "#B6FF00"),
    ("Electric Cyan", "#00F5FF"), ("Ultraviolet", "#8A2BE2"),
    ("Signal Orange", "#FF7A18"), ("Abyss Teal", "#02B8A2"),
    ("Ember Red", "#F43F5E"), ("Solar Gold", "#FFD166"),
)
BACKGROUNDS = ("#080808", "#111320", "#1E1023", "#091C1D", "#231913", "#13151A")
NAMES = ("BLACKSTAR", "ROSEGHOST", "ACID ORBIT", "EMBERWIRE",
         "DEEPSIGNAL", "STATIC BLOOM", "ECLIPSE CRT", "GHOST CIRCUIT")
HEX = re.compile(r"^#[0-9A-Fa-f]{6}$")


def validate_hex(value):
    candidate = value.strip().upper()
    if not HEX.fullmatch(candidate):
        raise argparse.ArgumentTypeError("Use a six-digit hex color like #FF1493")
    return candidate


def rgb(color):
    return tuple(int(color[i:i + 2], 16) / 255 for i in (1, 3, 5))


def hexcolor(channels):
    return "#" + "".join(f"{round(max(0.0, min(1.0, x)) * 255):02X}" for x in channels)


def contrasting(color):
    def linear(x):
        return x / 12.92 if x <= .04045 else ((x + .055) / 1.055) ** 2.4
    light = sum(weight * linear(channel) for weight, channel in
                zip((.2126, .7152, .0722), rgb(color)))
    return "#080808" if light > .18 else "#FFFFFF"


def rotate(color, degrees, sat=1, val=1):
    h, s, v = colorsys.rgb_to_hsv(*rgb(color))
    return hexcolor(colorsys.hsv_to_rgb((h + degrees / 360) % 1,
                                       min(1, s * sat), min(1, v * val)))


def make_palettes(seed, count=4, base=None):
    """Deterministic palette definitions. Seed is reflected in JSON metadata."""
    rng = random.Random(seed)
    results = []
    for number in range(count):
        background = BACKGROUNDS[(number + rng.randrange(len(BACKGROUNDS))) % len(BACKGROUNDS)]
        anchor_name, anchor = rng.choice(ANCHORS)
        if base and number == 0:
            anchor_name, anchor = "Custom Signal", base
        secondary = rotate(anchor, rng.choice((75, 110, 140, 170, 210, 245, 290)))
        third = rotate(anchor, rng.choice((25, 40, 315, 330)), sat=.78)
        accent = rng.choice(ANCHORS)[1]
        colors = [
            {"role": "void", "hex": background},
            {"role": "primary", "hex": anchor},
            {"role": "secondary", "hex": secondary},
            {"role": "pulse", "hex": third},
            {"role": "signal", "hex": accent},
        ]
        for swatch in colors:
            swatch["text"] = contrasting(swatch["hex"])
        results.append({
            "name": NAMES[(number + rng.randrange(len(NAMES))) % len(NAMES)],
            "anchor_name": anchor_name,
            "index": number + 1,
            "colors": colors,
            "glitch": {
                "rgb_shift_px": rng.randrange(2, 8),
                "scanline_opacity": round(rng.uniform(.08, .25), 2),
                "pixel_size_px": rng.choice((3, 4, 6, 8)),
            },
        })
    return results


def make_css(palettes):
    lines = ["/* HEXWAKE // locally generated, independent palettes */"]
    for p in palettes:
        lines.append(f'.hexwake-{p["index"]} {{')
        for color in p["colors"]:
            lines.append(f'  --hx-{color["role"]}: {color["hex"]};')
        glitch = p["glitch"]
        lines.extend((
            f'  --hx-rgb-shift: {glitch["rgb_shift_px"]}px;',
            f'  --hx-scanlines: {glitch["scanline_opacity"]};',
            f'  --hx-pixel: {glitch["pixel_size_px"]}px;',
            '}',
        ))
    return "\n".join(lines) + "\n"


def make_html(palettes, seed):
    sections = []
    for p in palettes:
        css_class = f'hexwake-{p["index"]}'
        swatches = "".join(
            '<div class="swatch" style="background:' + c["hex"] + ';color:' +
            c["text"] + '"><span>' + html.escape(c["role"]) +
            '</span><strong>' + c["hex"] + '</strong></div>'
            for c in p["colors"]
        )
        sections.append(
            '<section class="palette ' + css_class + '"><div class="meta">'
            '<span class="series">CHANNEL ' + str(p["index"]).zfill(2) + '</span>'
            '<h2>' + html.escape(p["name"]) + '</h2>'
            '<p>ANCHOR // ' + html.escape(p["anchor_name"]) + '</p></div>'
            '<div class="swatches">' + swatches + '</div>'
            '<div class="spec">RGB SPLIT ' + str(p["glitch"]["rgb_shift_px"]) +
            'px · SCANLINE ' + str(p["glitch"]["scanline_opacity"]) +
            ' · PIXEL ' + str(p["glitch"]["pixel_size_px"]) + 'px</div></section>'
        )
    style = """
    :root{color-scheme:dark}*{box-sizing:border-box}
    body{margin:0;background:#080808;color:#ebedf5;font:15px system-ui,sans-serif}
    main{max-width:1120px;margin:auto;padding:35px 18px 90px}
    .eyebrow{letter-spacing:.34em;color:#b6ff00;font-size:12px}
    h1{font-size:clamp(36px,8vw,84px);letter-spacing:-.06em;line-height:1;
       margin:17px 0;text-shadow:3px 0 #00f5ff,-3px 0 #ff1493}
    header p{color:#9eabc0;max-width:630px;line-height:1.65}
    .palette{border:1px solid #333746;background:var(--hx-void);padding:25px;
      border-radius:15px;margin:25px 0;box-shadow:7px 7px 0 #16151d}
    .meta h2{font-size:28px;letter-spacing:.09em;margin:7px 0}
    .meta p,.series,.spec{font-size:12px;letter-spacing:.16em;color:#b7b5c6}
    .swatches{display:grid;grid-template-columns:repeat(5,1fr);gap:9px;margin:25px 0}
    .swatch{min-height:112px;padding:13px;border-radius:7px;display:flex;
       justify-content:space-between;flex-direction:column;overflow-wrap:anywhere}
    .swatch span{text-transform:uppercase;letter-spacing:.08em;font-size:10px}
    .swatch strong{font-size:clamp(12px,2vw,18px);font-variant-numeric:tabular-nums}
    footer{margin-top:30px;color:#8692a7}
    @media(max-width:650px){.swatches{grid-template-columns:repeat(2,1fr)}
       .swatch:last-child{grid-column:span 2}}
    """
    return ("<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
            "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
            "<title>HEXWAKE // Palette Foundry</title><style>" + style +
            "</style><style>" + make_css(palettes) + "</style></head><body>"
            "<main><header><div class=\"eyebrow\">GLITCHBYTE PHANTOM LABS / DESIGN STATION</div>"
            "<h1>HEXWAKE<span style=\"color:#ff1493\">.</span></h1>"
            "<p>Offline glitch-color laboratory. Each set rotates a different "
            "high-voltage color story with reusable CSS variables. "
            "Every color is real hex, every run can be reproduced by seed.</p>"
            "<p>SEED // " + str(seed) + "</p></header>" +
            "".join(sections) +
            "<footer>NO API KEYS · NO TRACKING · LOCALLY GENERATED · "
            "GLITCH IS AN EFFECT, NOT ONE COLOR</footer></main></body></html>")


def generate(output, seed, count, base):
    output = Path(output).expanduser()
    output.mkdir(parents=True, exist_ok=True)
    palettes = make_palettes(seed, count, base)
    report = {
        "project": "HEXWAKE Palette Foundry",
        "seed": seed,
        "generated_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "base": base,
        "palettes": palettes,
        "disclaimer": "Generated swatches are design suggestions; validate contrast for your actual UI.",
    }
    # Avoid overwriting a prior export, including runs in the same second.
    while True:
        tag = secrets.token_hex(5)
        stem = output / f"hexwake_{seed}_{tag}"
        paths = [Path(str(stem) + ext) for ext in (".json", ".css", ".html")]
        if not any(path.exists() for path in paths):
            break
    for path, payload in zip(paths, (
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        make_css(palettes),
        make_html(palettes, seed),
    )):
        with path.open("x", encoding="utf-8") as stream:
            stream.write(payload)
    return paths


def main(argv=None):
    p = argparse.ArgumentParser(description="HEXWAKE: offline Glitch HEX palette foundry")
    p.add_argument("--seed", type=int, default=404,
                   help="Reproducible palette seed (default: 404)")
    p.add_argument("--count", type=int, default=4,
                   help="Number of palettes, 1–12 (default: 4)")
    p.add_argument("--base", type=validate_hex,
                   help="Optional first-palette anchor in six-digit hex, e.g. '#FF1493'")
    p.add_argument("--out", default=str(Path.home() / "HexwakePaletteReports"),
                   help="Directory for saved JSON/CSS/HTML exports")
    args = p.parse_args(argv)
    if not 1 <= args.count <= 12:
        p.error("--count must be between 1 and 12")
    paths = generate(args.out, args.seed, args.count, args.base)
    print(f"HEXWAKE // {args.count} palettes generated offline | seed {args.seed}")
    for path in paths:
        print("[SAVED]", path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
