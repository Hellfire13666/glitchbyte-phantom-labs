#!/usr/bin/env python3
"""PHANTOM CIPHERBOX: offline reversible puzzle studio, not encryption."""
import argparse
import base64
import codecs
import datetime as dt
import html
import json
from pathlib import Path
import random
import secrets

METHODS = ("hex", "base64", "reverse", "rot13")
CLUES = {
    "hex": "Decode hexadecimal bytes into UTF-8 text.",
    "base64": "Decode Base64 bytes into UTF-8 text.",
    "reverse": "Reverse all the characters in the transmission.",
    "rot13": "Apply ROT13 to Latin letters; leave other characters alone.",
}


def encode(value, method):
    if method == "hex":
        return value.encode("utf-8").hex()
    if method == "base64":
        return base64.b64encode(value.encode("utf-8")).decode("ascii")
    if method == "reverse":
        return value[::-1]
    if method == "rot13":
        return codecs.encode(value, "rot_13")
    raise ValueError("Unsupported encoding method")


def decode(value, method):
    if method == "hex":
        return bytes.fromhex(value).decode("utf-8")
    if method == "base64":
        return base64.b64decode(value, validate=True).decode("utf-8")
    if method == "reverse":
        return value[::-1]
    if method == "rot13":
        return codecs.decode(value, "rot_13")
    raise ValueError("Unsupported decoding method")


def create(message, seed=404, stages=3):
    if not message.strip():
        raise ValueError("Message cannot be blank")
    if not 2 <= stages <= 4:
        raise ValueError("Number of stages must be 2 to 4")
    methods = random.Random(seed).sample(METHODS, stages)
    value = message
    trail = []
    for method in methods:
        value = encode(value, method)
        trail.append((method, value))
    record = {
        "project": "PHANTOM CIPHERBOX",
        "format": 1,
        "seed": seed,
        "stages": stages,
        "operations": methods,
        "clues": [CLUES[x] for x in reversed(methods)],
        "ciphertext": value,
        "disclaimer": "Reversible educational encoding, NOT encryption.",
    }
    return record, trail


def recover(record):
    value = record["ciphertext"]
    for method in reversed(record["operations"]):
        value = decode(value, method)
    return value


def markdown(record):
    lines = [
        "# PHANTOM CIPHERBOX // CODED TRANSMISSION",
        "",
        "Educational puzzle, not cryptographic protection.",
        "",
        "Seed: " + str(record["seed"]),
        "Stages: " + str(record["stages"]),
        "",
        "## Encoded payload",
        "",
        "~~~text",
        record["ciphertext"],
        "~~~",
        "",
        "## Follow these decode clues in order",
        "",
    ]
    lines.extend(f"{i}. {clue}" for i, clue in enumerate(record["clues"], 1))
    return "\n".join(lines) + "\n"


def webpage(record):
    clues = "".join("<li>" + html.escape(c) + "</li>" for c in record["clues"])
    value = html.escape(record["ciphertext"])
    return ("""<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>PHANTOM CIPHERBOX // SIGNAL</title>
<style>:root{color-scheme:dark}*{box-sizing:border-box}
body{margin:0;background:radial-gradient(ellipse at 12% 0%,#243f34,#0b1213 50%,#08090d);
color:#eef8eb;font:17px system-ui,sans-serif;min-height:100vh}
main{max-width:880px;margin:auto;padding:60px 25px}
h1{font-size:clamp(40px,8vw,82px);letter-spacing:-.08em;line-height:.98;color:#bdff67}
.eyebrow{font-size:12px;color:#8fe7d9;letter-spacing:.27em}
.panel{background:#101c1bcc;border:1px solid #6f9e64;border-radius:14px;padding:28px}
pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#06100f;color:#b4ffcb;
border:1px solid #4b7564;padding:20px;border-radius:8px;line-height:1.6}
li{margin:12px 0}footer{margin-top:25px;color:#94a79d;font-size:13px}
</style><main><div class="eyebrow">GLITCHBYTE PHANTOM LABS / OFFLINE PUZZLE STATION</div>
<h1>PHANTOM<br>CIPHERBOX_</h1><section class="panel"><p>TRANSMISSION / """ +
            str(record["stages"]) + " STAGES · SEED " + str(record["seed"]) +
            "</p><pre>" + value + "</pre><h2>DECODE SEQUENCE</h2><ol>" +
            clues + """</ol><p>The answer key stays with the creator.</p>
</section><footer>REAL REVERSIBLE CODE · NO INTERNET · NO ENCRYPTION CLAIM</footer>
</main></html>""")


def export(folder, record, message, trail):
    folder = Path(folder).expanduser()
    folder.mkdir(parents=True, exist_ok=True)
    while True:
        stem = f"cipherbox_{record['seed']}_{secrets.token_hex(6)}"
        paths = [folder / (stem + ext) for ext in
                 (".json", ".md", ".html", ".answer.txt")]
        if not any(path.exists() for path in paths):
            break
    answer = [
        "PHANTOM CIPHERBOX // CREATOR'S ANSWER KEY",
        "PRIVATE: this file contains the original message.",
        "Created UTC: " + dt.datetime.now(dt.timezone.utc).isoformat(),
        "",
        "ORIGINAL MESSAGE:",
        message,
        "",
        "ENCODING SEQUENCE:",
    ]
    answer.extend(f"Stage {i}: {name} -> {result}"
                  for i, (name, result) in enumerate(trail, 1))
    payloads = (
        json.dumps(record, indent=2, ensure_ascii=False) + "\n",
        markdown(record),
        webpage(record),
        "\n".join(answer) + "\n",
    )
    for path, payload in zip(paths, payloads):
        with path.open("x", encoding="utf-8") as handle:
            handle.write(payload)
    return paths


def load_puzzle(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    operations = data.get("operations")
    stages = data.get("stages")
    if (data.get("project") != "PHANTOM CIPHERBOX"
            or data.get("format") != 1
            or type(stages) is not int or not 2 <= stages <= 4
            or type(operations) is not list or len(operations) != stages
            or len(set(operations)) != stages
            or any(m not in METHODS for m in operations)
            or not isinstance(data.get("ciphertext"), str)):
        raise ValueError("Invalid CIPHERBOX puzzle JSON")
    return data


def main(argv=None):
    p = argparse.ArgumentParser(description="Create and verify offline reversible puzzles")
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument("--message", help="Message to encode (visible in shell history)")
    group.add_argument("--message-file", help="Read local UTF-8 message from a file")
    group.add_argument("--verify", metavar="PUZZLE_JSON", help="Verify a decoded guess")
    p.add_argument("--guess", help="Guess text; omit for a concealed prompt")
    p.add_argument("--seed", type=int, default=404)
    p.add_argument("--stages", type=int, default=3, choices=(2, 3, 4))
    p.add_argument("--out", default=str(Path.home() / "PhantomCipherboxReports"))
    args = p.parse_args(argv)
    if args.verify:
        try:
            data = load_puzzle(args.verify)
            if args.guess is None:
                import getpass
                guess = getpass.getpass("Decoded message: ")
            else:
                guess = args.guess
            match = secrets.compare_digest(recover(data).encode("utf-8"), guess.encode("utf-8"))
        except (ValueError, OSError, UnicodeError, TypeError, KeyError) as exc:
            p.error(str(exc))
        print("PASS: Correct decoded message." if match else "NO MATCH: Decode each clue in sequence.")
        return 0 if match else 1
    if args.guess is not None:
        p.error("--guess requires --verify")
    try:
        message = (Path(args.message_file).expanduser().read_text(encoding="utf-8")
                   if args.message_file else args.message)
        record, trail = create(message, args.seed, args.stages)
        files = export(args.out, record, message, trail)
    except (ValueError, OSError, UnicodeError) as exc:
        p.error(str(exc))
    print(f"PHANTOM CIPHERBOX // {args.stages} reversible layers | seed {args.seed}")
    for file in files:
        print("[SAVED]", file)
    print("[CAUTION] Protect the .answer.txt file containing your original message.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
