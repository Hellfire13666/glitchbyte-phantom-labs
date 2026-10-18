"""Run actual Quick Open workflows locally, without any downloads or browser."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "phantom_quickopen.py"


def load():
    spec = importlib.util.spec_from_file_location("quickopen", SCRIPT)
    tool = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tool)
    return tool


class QuickOpenTests(unittest.TestCase):
    def test_all_five_real_tools_save_html_in_isolated_home(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            for tool in ("hexwake", "cipherbox", "rosie-scan", "ghostmark", "subdominatrix"):
                with self.subTest(tool=tool):
                    args = [sys.executable, str(SCRIPT), tool,
                            "--source-dir", str(ROOT),
                            "--workspace", str(folder), "--no-browser"]
                    result = subprocess.run(args, capture_output=True, text=True, timeout=30)
                    self.assertEqual(0, result.returncode, result.stderr + result.stdout)
                    self.assertIn("[REPORT]", result.stdout)
                    reports = list((folder / "reports" / tool).glob("*.html"))
                    self.assertEqual(1, len(reports))
                    self.assertTrue(list((folder / "reports" / tool).glob("*.json")))
            cipherfiles = list((folder / "reports" / "cipherbox").glob("*.answer.txt"))
            self.assertEqual(1, len(cipherfiles))
            self.assertIn("The rose survived the static", cipherfiles[0].read_text())
            domains = list((folder / "reports" / "rosie-scan").glob("*.json"))
            self.assertEqual("offline", json.loads(domains[0].read_text())["mode"])
            ghost = list((folder / "reports" / "ghostmark").glob("*.json"))
            self.assertEqual(1, len(json.loads(ghost[0].read_text())["duplicates"]))
            subfiles = list((folder / "reports" / "subdominatrix").glob("*.json"))
            data = json.loads(subfiles[0].read_text())
            self.assertEqual("SYNTHETIC OFFLINE DEMO", data["mode"])
            self.assertGreaterEqual(data["stats"]["names"], 10)

    def test_separate_runs_preserve_old_html(self):
        with tempfile.TemporaryDirectory() as tmp:
            for _ in range(2):
                result = subprocess.run(
                    [sys.executable, str(SCRIPT), "hexwake",
                     "--source-dir", str(ROOT), "--workspace", tmp, "--no-browser"],
                    capture_output=True, text=True, timeout=20)
                self.assertEqual(0, result.returncode, result.stderr)
            self.assertEqual(2, len(list((Path(tmp) / "reports" / "hexwake").glob("*.html"))))

    def test_existing_cache_not_overwritten_if_source_unavailable(self):
        mod = load()
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "cached.py"
            target.write_text("# existing safe version\n")
            saved = mod.install_source("tools/missing.py", target, source_dir="/missing")
            self.assertEqual(saved, target)
            self.assertEqual("# existing safe version\n", target.read_text())
            with self.assertRaises(OSError):
                mod.install_source("tools/missing.py", target, source_dir="/missing", refresh=True)
            self.assertEqual("# existing safe version\n", target.read_text())

    def test_tool_failures_and_parameter_misuse(self):
        with tempfile.TemporaryDirectory() as tmp:
            for flags in (["hexwake", "--count", "0"],
                          ["ghostmark", "--baseline", "/missing/old.json"],
                          ["hexwake", "--live"]):
                result = subprocess.run(
                    [sys.executable, str(SCRIPT), *flags,
                     "--source-dir", str(ROOT), "--workspace", tmp, "--no-browser"],
                    capture_output=True, text=True, timeout=20)
                self.assertNotEqual(0, result.returncode)

    def test_local_folder_scan(self):
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp)
            files = work / "sample"
            files.mkdir()
            (files / "a.txt").write_text("rosie")
            (files / "b.txt").write_text("rosie")
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "ghostmark",
                 "--folder", str(files), "--source-dir", str(ROOT),
                 "--workspace", str(work / "station"), "--no-browser"],
                capture_output=True, text=True, timeout=20)
            self.assertEqual(0, result.returncode, result.stderr)
            data = json.loads(next((work / "station" / "reports" / "ghostmark").glob("*.json")).read_text())
            self.assertEqual(2, len(data["files"]))
            self.assertEqual(1, len(data["duplicates"]))


if __name__ == "__main__":
    unittest.main()
