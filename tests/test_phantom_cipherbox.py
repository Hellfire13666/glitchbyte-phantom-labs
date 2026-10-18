"""End-to-end offline regression tests for PHANTOM CIPHERBOX."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools/phantom_cipherbox.py"


def tool():
    spec = importlib.util.spec_from_file_location("cipherbox_under_test", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CipherboxTests(unittest.TestCase):
    def test_round_trip_for_utf8_at_all_depths(self):
        mod = tool()
        for count in (2, 3, 4):
            for msg in ("Rose <3", "I love you 🌹", "café • moon\nsecond line"):
                with self.subTest(stages=count, message=msg):
                    puzzle, trail = mod.create(msg, 109, count)
                    self.assertEqual(msg, mod.recover(puzzle))
                    self.assertEqual(count, len(trail))
                    self.assertEqual(puzzle, mod.create(msg, 109, count)[0])
                    self.assertNotIn(msg, json.dumps(puzzle, ensure_ascii=False))

    def test_real_file_outputs_and_cli_verification(self):
        with tempfile.TemporaryDirectory() as home:
            message = "The rose survives the static 🌹"
            for _ in range(2):
                proc = subprocess.run(
                    [sys.executable, str(SCRIPT), "--message", message, "--seed", "19",
                     "--stages", "4", "--out", home],
                    text=True, capture_output=True, timeout=12, check=True,
                )
                self.assertIn("4 reversible layers", proc.stdout)
            path = Path(home)
            self.assertEqual(2, len(list(path.glob("*.json"))))
            self.assertEqual(2, len(list(path.glob("*.md"))))
            self.assertEqual(2, len(list(path.glob("*.html"))))
            self.assertEqual(2, len(list(path.glob("*.answer.txt"))))
            puzzle_path = list(path.glob("*.json"))[0]
            record = json.loads(puzzle_path.read_text(encoding="utf-8"))
            self.assertNotIn(message, json.dumps(record, ensure_ascii=False))
            self.assertNotIn(message, list(path.glob("*.html"))[0].read_text(encoding="utf-8"))
            self.assertIn(message, list(path.glob("*.answer.txt"))[0].read_text(encoding="utf-8"))
            yes = subprocess.run(
                [sys.executable, str(SCRIPT), "--verify", str(puzzle_path), "--guess", message],
                text=True, capture_output=True, timeout=12,
            )
            self.assertEqual(0, yes.returncode, yes.stderr)
            self.assertIn("PASS:", yes.stdout)
            no = subprocess.run(
                [sys.executable, str(SCRIPT), "--verify", str(puzzle_path), "--guess", "incorrect"],
                text=True, capture_output=True, timeout=12,
            )
            self.assertEqual(1, no.returncode)

    def test_file_input_and_bad_parameters(self):
        with tempfile.TemporaryDirectory() as home:
            path = Path(home)
            msgfile = path / "message.txt"
            msgfile.write_text("offline 💙", encoding="utf-8")
            proc = subprocess.run(
                [sys.executable, str(SCRIPT), "--message-file", str(msgfile),
                 "--out", str(path / "exports")],
                capture_output=True, text=True, timeout=12,
            )
            self.assertEqual(0, proc.returncode, proc.stderr)
            for flags in (
                ["--message", "  "],
                ["--message", "yes", "--stages", "5"],
                ["--message", "yes", "--guess", "yes"],
            ):
                with self.subTest(flags=flags):
                    bad = subprocess.run(
                        [sys.executable, str(SCRIPT), *flags, "--out", str(path / "bad")],
                        text=True, capture_output=True, timeout=12,
                    )
                    self.assertNotEqual(0, bad.returncode)


if __name__ == "__main__":
    unittest.main()
