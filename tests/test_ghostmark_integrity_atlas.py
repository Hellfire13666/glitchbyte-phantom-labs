"""GHOSTMARK offline integrity and export regression tests."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "ghostmark_integrity_atlas.py"


def tool():
    spec = importlib.util.spec_from_file_location("ghostmark", SCRIPT)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


class GhostmarkTests(unittest.TestCase):
    def test_real_hashes_duplicates_and_changes(self):
        m = tool()
        with tempfile.TemporaryDirectory() as t:
            root = Path(t) / "inputs"
            root.mkdir()
            (root / "a.txt").write_text("rosie 🌹", encoding="utf-8")
            (root / "b.txt").write_text("rosie 🌹", encoding="utf-8")
            (root / "c.txt").write_text("different", encoding="utf-8")
            first = m.inventory(root)
            self.assertEqual(3, len(first["files"]))
            groups = m.duplicates(first["files"])
            self.assertEqual(1, len(groups))
            self.assertEqual(["a.txt", "b.txt"], groups[0]["paths"])
            (root / "c.txt").write_text("changed", encoding="utf-8")
            (root / "b.txt").unlink()
            (root / "d.txt").write_text("added", encoding="utf-8")
            now = m.inventory(root)
            change = m.compare(now, first)
            self.assertEqual(["c.txt"], change["changed"])
            self.assertEqual(["b.txt"], change["removed"])
            self.assertEqual(["d.txt"], change["added"])
            self.assertEqual(1, change["unchanged"])
            with self.assertRaises(ValueError):
                m.compare(now, {"app": "not ghostmark"})

    def test_ignore_symlinks_cap_and_nested_reports(self):
        m = tool()
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            (root / "a.txt").write_bytes(b"abc")
            (root / "big.bin").write_bytes(b"a" * 12)
            (root / "linked.txt").symlink_to(root / "a.txt")
            (root / "reports").mkdir()
            (root / "reports" / "old.txt").write_text("exclude")
            report = m.inventory(root, max_files=2, max_bytes=5, exclude=root / "reports")
            self.assertEqual(["a.txt"], [x["path"] for x in report["files"]])
            reasons = {x["reason"] for x in report["skipped"]}
            self.assertIn("exceeds file size cap", reasons)
            self.assertIn("symlink", reasons)
            self.assertEqual(b"abc", (root / "a.txt").read_bytes())
            self.assertEqual("exclude", (root / "reports" / "old.txt").read_text())

    def test_escaping_and_unique_export(self):
        m = tool()
        with tempfile.TemporaryDirectory() as t:
            root = Path(t) / "source"
            root.mkdir()
            (root / "<script>alert(1).txt").write_text("safe")
            record = m.inventory(root)
            record["duplicates"] = m.duplicates(record["files"])
            one, htmlone = m.write_report(record, Path(t) / "out")
            two, htmltwo = m.write_report(record, Path(t) / "out")
            self.assertNotEqual(one, two)
            self.assertTrue(htmltwo.exists())
            self.assertEqual(1, len(json.loads(one.read_text())["files"]))
            page = htmlone.read_text()
            self.assertIn("&lt;script&gt;", page)
            self.assertNotIn("<script>alert(1)", page)

    def test_actual_demo_cli_produces_html_json(self):
        with tempfile.TemporaryDirectory() as t:
            run = subprocess.run(
                [sys.executable, str(SCRIPT), "--demo", "--no-browser", "--out", t],
                capture_output=True, text=True, timeout=20)
            self.assertEqual(0, run.returncode, run.stderr)
            self.assertIn("duplicate groups", run.stdout)
            reports = list(Path(t).glob("*.json"))
            pages = list(Path(t).glob("*.html"))
            self.assertEqual(1, len(reports))
            self.assertEqual(1, len(pages))
            data = json.loads(reports[0].read_text(encoding="utf-8"))
            self.assertEqual(3, len(data["files"]))
            self.assertEqual(1, len(data["duplicates"]))
            self.assertIn("GHOSTMARK", pages[0].read_text(encoding="utf-8"))

    def test_reject_invalid_options(self):
        with tempfile.TemporaryDirectory() as t:
            for args in (["--folder", t, "--max-mb", "0"],
                         ["--demo", "--baseline", "missing.json"],
                         ["--folder", t, "--max-files", "0"]):
                run = subprocess.run(
                    [sys.executable, str(SCRIPT), *args, "--no-browser"],
                    capture_output=True, text=True, timeout=20)
                self.assertNotEqual(0, run.returncode)


if __name__ == "__main__":
    unittest.main()
