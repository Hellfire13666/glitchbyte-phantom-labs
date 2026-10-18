"""Run actual safe, offline first-run exercises on Linux CI.

No third-party X APIs, public-site probes, or credentials are used here.
Each exercise runs the real program from tools/ under an isolated HOME.
"""
import csv
import json
import os
import re
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"


class OfflineTerminalVerification(unittest.TestCase):
    def invoke(self, script, arguments=(), stdin=None, timeout=25):
        env = os.environ.copy()
        env["HOME"] = str(self.home)
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        return subprocess.run(
            [sys.executable, str(TOOLS / script), *map(str, arguments)],
            input=stdin, text=True, capture_output=True, cwd=self.home,
            env=env, timeout=timeout, check=True,
        )

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="phantom-offline-")
        self.addCleanup(self.tmp.cleanup)
        self.home = Path(self.tmp.name)

    def test_all_16_python_scripts_parse(self):
        scripts = sorted(TOOLS.glob("*.py"))
        self.assertEqual(16, len(scripts))
        for script in scripts:
            with self.subTest(script=script.name):
                compile(script.read_bytes(), str(script), "exec")

    def test_cli_help_for_argparse_tools(self):
        scripts = (
            "glitchbyte_domain_intel.py", "glitchbyte_log_constellation.py",
            "glitchbyterosie_x_intel.py", "glitchbyterosie_x_no_api.py",
            "rose_crawler.py", "rosie_ip_shadow_scraper.py",
            "rosie_signal_garden.py", "rosie_username_intel.py",
            "rosieglitchbyte_domain_phantom.py", "rosieglitchbyte_hackgirl.py",
            "rosieglitchbyte_ip_specter.py",
            "rosieglitchbyte_neon_rose_phantom_3.py",
        )
        for script in scripts:
            with self.subTest(script=script):
                result = self.invoke(script, ["--help"])
                self.assertIn("usage:", result.stdout.lower())

    def test_offline_research_and_reports(self):
        log_out = self.home / "logs"
        self.invoke("glitchbyte_log_constellation.py", ["--demo", "--out", log_out])
        self.assertIn("total", json.loads((log_out / "constellation.json").read_text()))
        self.assertTrue((log_out / "constellation.html").is_file())

        garden = self.home / "garden"
        garden_out = self.home / "garden-reports"
        self.invoke("rosie_signal_garden.py", [
            "--demo", "--folder", garden, "--output", garden_out, "--keyword", "phantom"
        ])
        self.assertTrue((garden_out / "signal_garden.json").is_file())
        self.assertTrue((garden_out / "signal_garden.html").is_file())

        crawler = self.home / "crawler"
        self.invoke("rose_crawler.py", ["phantomlabdemo", "--output", crawler])
        self.assertTrue(list(crawler.glob("*.json")))
        self.assertTrue(list(crawler.glob("*.html")))
        self.assertTrue(list(crawler.glob("*.csv")))

        self.invoke("rosie_username_intel.py", ["phantomlabdemo", "--links-only"])
        user = json.loads((self.home / "rosie_intel_phantomlabdemo.json").read_text())
        self.assertEqual(8, len(user["results"]))

        self.invoke("rosieglitchbyte_domain_phantom.py", [
            "example.org", "--mode", "7", "--no-animation"
        ])
        self.assertTrue(list((self.home / "RosieGlitchByte_Domain_Intel").glob("*.json")))

        self.invoke("rosieglitchbyte_neon_rose_phantom_3.py", [
            "example.org", "--mode", "7", "--no-animation"
        ])
        rose_files = list((self.home / "RosieGlitchByte_Neon_Rose_Reports").glob("*.json"))
        self.assertEqual(1, len(rose_files))
        self.assertIn("RDAP research link", json.loads(rose_files[0].read_text())["modules"])

        self.invoke("rosieglitchbyte_ip_specter.py", ["192.0.2.1", "--mode", "1"])
        self.assertTrue(list((self.home / "RosieGlitchByte_IP_Reports").glob("*.json")))

        self.invoke("rosie_ip_shadow_scraper.py", ["192.0.2.1", "--mode", "1"])
        self.assertTrue(list((self.home / "RosieGlitchByte_IP_Shadow_Reports").glob("*.json")))

    def test_no_api_offline_imports(self):
        sample = self.home / "fictional_posts.csv"
        with sample.open("w", encoding="utf-8", newline="") as out:
            w = csv.DictWriter(out, fieldnames=[
                "date", "username", "text", "url", "likes", "reposts", "replies", "quotes"
            ])
            w.writeheader()
            w.writerow({"date": "2026-10-10", "username": "demo",
                        "text": "#PhantomLabs hello https://example.org",
                        "url": "", "likes": 2, "reposts": 0, "replies": 0, "quotes": 0})

        self.invoke("glitchbyterosie_x_no_api.py", [
            "--import-file", sample, "--filter", "PhantomLabs"
        ])
        self.assertTrue(list((self.home / "glitchbyte_x_reports").glob("posts_*.json")))
        self.assertTrue(list((self.home / "glitchbyte_x_reports").glob("posts_*.csv")))

        self.invoke("rosieglitchbyte_hackgirl.py", [
            "--import-file", sample, "--filter", "PhantomLabs", "--html"
        ])
        reports = self.home / "RosieGlitchbyte_Intel"
        self.assertTrue(list(reports.glob("post_analysis_*.json")))
        self.assertTrue(list(reports.glob("dashboard_*.html")))

        self.invoke("glitchbyterosie_x_no_api.py", ["--keyword", "Phantom Labs"])
        self.invoke("rosieglitchbyte_hackgirl.py", ["--keyword", "Phantom Labs"])

    def test_original_creative_games_and_letters(self):
        # Import the real source with animation disabled only for this subprocess.
        cases = [
            ("rosie_ghost_heart.py", "echo\nrose\nkeyboard\nheart\nlove\n", "ONE HEART WAS FOUND"),
            ("rosie_hide_seek.py", "signal\nrose\nyou\n", "You found me."),
            ("rosie_catch_me_chaos.py", "rose\nstatic\nkeyboard\n", "GAME COMPLETE"),
        ]
        runner = (
            "import importlib.util,sys,time;"
            "p=sys.argv[1];"
            "s=importlib.util.spec_from_file_location('game',p);"
            "g=importlib.util.module_from_spec(s);s.loader.exec_module(g);"
            "time.sleep=lambda _:None;"
            "g.ANIMATE=False if hasattr(g,'ANIMATE') else None;"
            "g.FAST=True if hasattr(g,'FAST') else None;"
            "g.main()"
        )
        for name, answers, ending in cases:
            with self.subTest(game=name):
                done = subprocess.run(
                    [sys.executable, "-c", runner, str(TOOLS / name)],
                    input=answers, text=True, capture_output=True,
                    cwd=self.home, timeout=30, check=True
                )
                plain = re.sub(r"\x1b\[[0-9;]*m", "", done.stdout)
                self.assertIn(ending, plain)
                self.assertIn("RosieGlitchbyte <3", plain)

        # The fourth creative tool is not a puzzle, just a hex-encoded letter.
        decoder = (
            "import importlib.util,sys;"
            "s=importlib.util.spec_from_file_location('dark',sys.argv[1]);"
            "m=importlib.util.module_from_spec(s);s.loader.exec_module(m);"
            "print(m.decode_letter())"
        )
        result = subprocess.run(
            [sys.executable, "-c", decoder, str(TOOLS / "rosie_dark_desire.py")],
            text=True, capture_output=True, check=True, timeout=15
        )
        self.assertIn("RosieGlitchbyte <3", result.stdout)


if __name__ == "__main__":
    unittest.main()
