"""Offline integration and consistency tests for independent HEXWAKE tool."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "hexwake_palette_foundry.py"


def load():
    spec = importlib.util.spec_from_file_location("hexwake_tool_under_test", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class HexwakeTests(unittest.TestCase):
    def test_reproducible_palette_content_and_hex_values(self):
        mod = load()
        a = mod.make_palettes(404, 5, "#FF1493")
        b = mod.make_palettes(404, 5, "#FF1493")
        self.assertEqual(a, b)
        self.assertEqual("#FF1493", a[0]["colors"][1]["hex"])
        for palette in a:
            self.assertEqual(5, len(palette["colors"]))
            for swatch in palette["colors"]:
                self.assertRegex(swatch["hex"], r"^#[0-9A-F]{6}$")
                self.assertIn(swatch["text"], ("#080808", "#FFFFFF"))

    def test_repeated_cli_runs_preserve_all_three_exports(self):
        with tempfile.TemporaryDirectory() as temp:
            for _ in range(2):
                p = subprocess.run(
                    [sys.executable, str(SCRIPT), "--seed", "404", "--count", "3",
                     "--base", "#FF1493", "--out", temp],
                    text=True, capture_output=True, check=True, timeout=20
                )
                self.assertIn("3 palettes generated offline", p.stdout)
            out = Path(temp)
            self.assertEqual(2, len(list(out.glob("hexwake_*.json"))))
            self.assertEqual(2, len(list(out.glob("hexwake_*.css"))))
            self.assertEqual(2, len(list(out.glob("hexwake_*.html"))))
            for file in out.glob("*.json"):
                record = json.loads(file.read_text(encoding="utf-8"))
                self.assertEqual(3, len(record["palettes"]))
                self.assertEqual(404, record["seed"])
            for file in out.glob("*.html"):
                html = file.read_text(encoding="utf-8")
                self.assertIn("HEXWAKE", html)
                self.assertIn('class="swatch"', html)
            for file in out.glob("*.css"):
                self.assertIn("--hx-primary:", file.read_text(encoding="utf-8"))

    def test_rejects_invalid_color_and_count(self):
        with tempfile.TemporaryDirectory() as temp:
            for args in (["--base", "not-hex"], ["--count", "0"], ["--count", "13"]):
                with self.subTest(args=args):
                    result = subprocess.run(
                        [sys.executable, str(SCRIPT), "--out", temp, *args],
                        capture_output=True, text=True, timeout=10
                    )
                    self.assertNotEqual(0, result.returncode)
            self.assertEqual([], list(Path(temp).iterdir()))


if __name__ == "__main__":
    unittest.main()
