#!/usr/bin/env python3
"""Phantom Labs: optional plain-text terminal transcript for any local CLI tool.

Example:
    python3 scripts/phantom_easy_save.py -o findings.txt -- python3 -u tools/my_tool.py --help

The wrapper executes an argv list (never a shell string), streams combined
stdout/stderr as-is to the terminal, and optionally saves an ANSI-free
transcript. This DOES NOT convert printed logs to a tool's native data export.
"""
import argparse
import os
from pathlib import Path
import subprocess
import sys


class StripAnsi:
    """Incremental ANSI control-sequence remover that handles split chunks."""

    def __init__(self):
        self.state = 0  # 0=normal, 1=ESC, 2=CSI, 3=OSC, 4=OSC_ESC
        self.pending_cr = False

    def clean(self, data):
        out = bytearray()
        for byte in data:
            if self.state == 0:
                # CR and CRLF are terminal line controls, not useful in a TXT.
                # Keep this state across chunks to avoid duplicate newlines.
                if self.pending_cr:
                    out.append(10)
                    self.pending_cr = False
                    if byte == 10:
                        continue
                if byte == 27:
                    self.state = 1
                elif byte == 13:
                    self.pending_cr = True
                elif byte in (9, 10) or byte >= 32 and byte != 127:
                    # Strip NUL, BEL, BS, other C0 and DEL, which can cause
                    # 'less' to label a transcript as binary.
                    # Bytes >= 128 are retained to preserve UTF-8/emoji.
                    out.append(byte)
            elif self.state == 1:
                if byte == ord("["):
                    self.state = 2
                elif byte == ord("]"):
                    self.state = 3
                else:
                    self.state = 0
            elif self.state == 2:
                if 0x40 <= byte <= 0x7E:
                    self.state = 0
            elif self.state == 3:
                if byte == 7:
                    self.state = 0
                elif byte == 27:
                    self.state = 4
            elif self.state == 4:
                if byte == ord("\\"):
                    self.state = 0
                else:
                    self.state = 3
        return bytes(out)

    def finish(self):
        """Flush an unfinished carriage return at end of the stream."""
        if self.pending_cr:
            self.pending_cr = False
            return b"\n"
        return b""


def parse_args(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    parser = argparse.ArgumentParser(
        description="Run any terminal tool, optionally saving its printed output as plain text.",
        epilog=("Use -- before the tool command. Example: "
                "phantom_easy_save.py -o findings.txt -- python3 -u tools/your_tool.py --help"))
    parser.add_argument("-o", "--o", "--output", dest="output", metavar="NAME.txt",
                        help="Optional NEW TXT file for the terminal transcript (no overwrites)")
    if argv == ["-h"] or argv == ["--help"]:
        parser.parse_args(argv)  # argparse prints genuine help and exits 0
    if "--" not in argv:
        parser.error("Missing '--' separator before the command to run")
    marker = argv.index("--")
    opts = parser.parse_args(argv[:marker])
    command = argv[marker + 1:]
    if not command:
        parser.error("Enter the command after '--'")
    if opts.output:
        destination = Path(opts.output).expanduser()
        if destination.suffix.lower() != ".txt":
            parser.error("-o / --o needs a .txt filename")
        if not destination.parent.is_dir():
            parser.error(f"Parent directory does not exist: {destination.parent}")
        if destination.exists():
            parser.error(f"Output file exists (won't overwrite): {destination}")
    return opts, command


def execute(argv=None):
    opts, command = parse_args(argv)
    output = Path(opts.output).expanduser() if opts.output else None
    saved = None
    if output:
        try:
            descriptor = os.open(output, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            saved = os.fdopen(descriptor, "wb")
        except FileExistsError:
            print(f"[ERROR] Existing file not overwritten: {output}", file=sys.stderr)
            return 2
        except OSError as exc:
            print(f"[ERROR] Cannot save file: {exc}", file=sys.stderr)
            return 2

    try:
        # Never invoke a shell or reinterpret a tool's arguments.
        proc = subprocess.Popen(command, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, stdin=None,
                                bufsize=0)
    except OSError as exc:
        if saved is not None:
            saved.close()
            try:
                output.unlink()
            except OSError:
                pass
        print(f"[ERROR] Unable to launch tool: {exc}", file=sys.stderr)
        return 127

    filter_ansi = StripAnsi()
    try:
        while True:
            chunk = os.read(proc.stdout.fileno(), 4096)
            if not chunk:
                break
            # Preserve original color and content on the screen.
            sys.stdout.buffer.write(chunk)
            sys.stdout.buffer.flush()
            if saved is not None:
                saved.write(filter_ansi.clean(chunk))
        code = proc.wait()
        if saved is not None:
            saved.write(filter_ansi.finish())
    except KeyboardInterrupt:
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait()
        code = 130
    finally:
        proc.stdout.close()
        if saved is not None:
            saved.close()

    if output:
        print(f"\n[SAVED] Plain-text terminal output: {output}", flush=True)
    else:
        print("\n[SAVE OFF] Nothing saved by the wrapper.", flush=True)
    return code


if __name__ == "__main__":
    raise SystemExit(execute())
