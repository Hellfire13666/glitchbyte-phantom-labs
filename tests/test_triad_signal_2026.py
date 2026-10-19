"""Offline regression tests for GlitchByte Phantom Labs' Triad Signal companion."""
import importlib.util
import os
import stat
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "triad_signal_2026.py"


def module():
    spec = importlib.util.spec_from_file_location("triad_signal", SCRIPT)
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


def create_fakes(folder):
    for name in ("amass", "gau", "waybackurls"):
        exe = Path(folder) / name
        output = {
            "amass": "api.example.com\ninvalid-domain.evil.net\n",
            "gau": "https://example.com/a?x=1\nNOTICE broken source\n",
            "waybackurls": "http://example.com/a\nhttps://example.com/a?x=1\n",
        }[name]
        exe.write_text("#!" + sys.executable + "\n"
                       "import sys\n"
                       "sys.stdout.write(" + repr(output) + ")\n"
                       "sys.stdout.flush()\n", encoding="utf-8")
        exe.chmod(0o755)


class TriadSignalTests(unittest.TestCase):
    def test_normalize_enforces_target_and_valid_public_formats(self):
        m = module()
        self.assertEqual("api.example.com", m.normalize("API.EXAMPLE.COM", "example.com"))
        self.assertEqual("https://example.com/x?y=1",
                         m.normalize("https://example.com/x?y=1", "example.com"))
        self.assertIsNone(m.normalize("example.com.evil.net", "example.com"))
        self.assertIsNone(m.normalize("https://evil.net/foo", "example.com"))
        self.assertIsNone(m.normalize("https://user:pass@example.com/private", "example.com"))
        self.assertIsNone(m.normalize("no more connections allowed", "example.com"))
        self.assertIsNone(m.normalize("\x00example.com", "example.com"))

    def test_cli_no_save_and_completes_fake_modules(self):
        with tempfile.TemporaryDirectory() as tmp:
            create_fakes(tmp)
            env = dict(os.environ, PATH=tmp + os.pathsep + os.environ.get("PATH", ""))
            run = subprocess.run([sys.executable, "-B", "-u", str(SCRIPT), "example.com",
                                  "--color", "never", "--amass-seconds", "5",
                                  "--gau-seconds", "5", "--wayback-seconds", "5"],
                                 capture_output=True, text=True, timeout=15, env=env)
            self.assertEqual(0, run.returncode, run.stderr)
            self.assertIn("[AMASS][COMPLETE]", run.stdout)
            self.assertIn("[GAU][COMPLETE]", run.stdout)
            self.assertIn("[WAYBACKURLS][COMPLETE]", run.stdout)
            self.assertIn("[DONE] No companion report saved", run.stdout)
            self.assertEqual(sorted(["amass", "gau", "waybackurls"]),
                             sorted(p.name for p in Path(tmp).iterdir()))

    def test_short_o_saves_deduplicated_real_candidate_lines(self):
        with tempfile.TemporaryDirectory() as tmp:
            create_fakes(tmp)
            file = Path(tmp) / "unique.txt"
            env = dict(os.environ, PATH=tmp + os.pathsep + os.environ.get("PATH", ""))
            result = subprocess.run([sys.executable, "-B", str(SCRIPT), "example.com",
                                     "-o", str(file), "--color", "never",
                                     "--amass-seconds", "5", "--gau-seconds", "5",
                                     "--wayback-seconds", "5"], capture_output=True,
                                    text=True, timeout=15, env=env)
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn("[SAVED] TXT", result.stdout)
            self.assertEqual([
                "api.example.com",
                "http://example.com/a",
                "https://example.com/a?x=1",
            ], file.read_text().splitlines())
            self.assertNotIn("NOTICE", file.read_text())

    def test_saved_txt_private_under_permissive_umask(self):
        # Reproduce the real Ubuntu 664 discovery even when umask permits 666.
        # Subprocess adjusts its own umask; it never changes the test runner.
        with tempfile.TemporaryDirectory() as tmp:
            create_fakes(tmp)
            file = Path(tmp) / "private.txt"
            env = dict(os.environ, PATH=tmp + os.pathsep + os.environ.get("PATH", ""))
            driver = "import os,sys;os.umask(0);os.execv(sys.executable,[sys.executable,*sys.argv[1:]])"
            cmd = [sys.executable, "-B", "-c", driver,
                   "-B", str(SCRIPT), "example.com", "--only", "waybackurls",
                   "--o", str(file), "--wayback-seconds", "5"]
            result = subprocess.run(cmd, capture_output=True, text=True,
                                    timeout=15, env=env)
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn("[SAVED] TXT", result.stdout)
            self.assertEqual(0o600, stat.S_IMODE(file.stat().st_mode))
            self.assertTrue(file.read_text().startswith("http://example.com"))

    def test_long_o_no_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            create_fakes(tmp)
            file = Path(tmp) / "evidence.txt"
            file.write_text("ORIGINAL\n")
            env = dict(os.environ, PATH=tmp + os.pathsep + os.environ.get("PATH", ""))
            result = subprocess.run([sys.executable, "-B", str(SCRIPT),
                                     "example.com", "--o", str(file)],
                                    capture_output=True, text=True, timeout=10, env=env)
            self.assertNotEqual(0, result.returncode)
            self.assertEqual("ORIGINAL\n", file.read_text())
            self.assertIn("will not be overwritten", result.stderr)

    def test_partial_timeout_retains_printed_candidate(self):
        m = module()
        with tempfile.TemporaryDirectory() as tmp:
            exe = Path(tmp) / "amass"
            exe.write_text("#!" + sys.executable + "\n"
                           "import time\n"
                           "print('api.example.com', flush=True)\n"
                           "time.sleep(4)\n", encoding="utf-8")
            exe.chmod(0o755)
            event = []
            with patch.object(m.shutil, "which", return_value=str(exe)):
                result = m.probe("amass", "example.com", 0.3, 3, event.append)
            self.assertEqual("partial-timeout", result["status"])
            self.assertEqual(["api.example.com"], result["results"])
            self.assertTrue(any("[FOUND]" in x for x in event))

    def test_reject_out_of_scope_and_excessive_timeout(self):
        m = module()
        with patch.object(sys, "argv", ["triad", "example.com", "--gau-seconds", "500"]):
            with self.assertRaises(SystemExit):
                m.run()
        with patch.object(sys, "argv", ["triad", "https://example.com"]):
            with self.assertRaises(SystemExit):
                m.run()


if __name__ == "__main__":
    unittest.main()
