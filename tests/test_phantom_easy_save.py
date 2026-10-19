"""Offline checks for the universal GlitchByte Phantom Labs easy-save runner."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
WRAPPER = ROOT / "scripts" / "phantom_easy_save.py"


def invoke(*args):
    return subprocess.run([sys.executable, str(WRAPPER), *map(str, args)],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          text=True, timeout=15)


class PhantomEasySaveTests(unittest.TestCase):
    def test_no_output_file_without_flag(self):
        with tempfile.TemporaryDirectory() as root:
            testfile = Path(root) / "never.txt"
            proc = invoke("--", sys.executable, "-u", "-c", "print('SIGNAL FOUND')")
            self.assertEqual(0, proc.returncode, proc.stderr)
            self.assertIn("SIGNAL FOUND", proc.stdout)
            self.assertIn("[SAVE OFF]", proc.stdout)
            self.assertFalse(testfile.exists())

    def test_short_o_saves_clean_uncolored_output(self):
        with tempfile.TemporaryDirectory() as root:
            saved = Path(root) / "intel.txt"
            child = ("import sys;"
                     "print('\\x1b[95mFOUND\\x1b[0m');"
                     "print('WARN', file=sys.stderr)")
            proc = invoke("-o", saved, "--", sys.executable, "-u", "-c", child)
            self.assertEqual(0, proc.returncode, proc.stderr)
            self.assertIn("\x1b[95mFOUND", proc.stdout)
            lines = saved.read_text().splitlines()
            self.assertEqual(["FOUND", "WARN"], lines)
            self.assertNotIn("\x1b", saved.read_text())
            self.assertEqual([saved], list(Path(root).iterdir()))

    def test_long_double_o_alias(self):
        with tempfile.TemporaryDirectory() as root:
            saved = Path(root) / "results.txt"
            proc = invoke("--o", saved, "--", sys.executable, "-u", "-c",
                          "print('two-way result')")
            self.assertEqual(0, proc.returncode, proc.stderr)
            self.assertEqual("two-way result\n", saved.read_text())

    def test_preserve_legacy_user_file(self):
        with tempfile.TemporaryDirectory() as root:
            saved = Path(root) / "mydata.txt"
            saved.write_text("ORIGINAL\n")
            proc = invoke("-o", saved, "--", sys.executable, "-u", "-c",
                          "print('should not run')")
            self.assertNotEqual(0, proc.returncode)
            self.assertEqual("ORIGINAL\n", saved.read_text())
            self.assertNotIn("should not run", proc.stdout)

    def test_error_exit_status_propagates_and_transcript_is_kept(self):
        with tempfile.TemporaryDirectory() as root:
            saved = Path(root) / "partial.txt"
            proc = invoke("-o", saved, "--", sys.executable, "-u", "-c",
                          "print('partial finding');raise SystemExit(9)")
            self.assertEqual(9, proc.returncode)
            self.assertIn("partial finding", saved.read_text())

    def test_no_shell_interpolation_or_command_splitting(self):
        with tempfile.TemporaryDirectory() as root:
            safe = Path(root) / "literal.txt"
            value = f";touch {root}/evil.txt"
            proc = invoke("-o", safe, "--", sys.executable, "-u", "-c",
                          "import sys;print(sys.argv[1])", value)
            self.assertEqual(0, proc.returncode, proc.stderr)
            self.assertEqual(value + "\n", safe.read_text())
            self.assertFalse((Path(root) / "evil.txt").exists())

    def test_validation(self):
        for options in (["-o", "report.json"], ["--o", "folder/no.txt"]):
            with self.subTest(options=options):
                proc = invoke(*options, "--", sys.executable, "-u", "-c",
                              "print('must not execute')")
                self.assertNotEqual(0, proc.returncode)
                self.assertNotIn("must not execute", proc.stdout)
        self.assertNotEqual(0, invoke("-o", "only.txt").returncode)

    def test_failed_program_does_not_leave_placeholder(self):
        with tempfile.TemporaryDirectory() as root:
            path = Path(root) / "nothing.txt"
            proc = invoke("-o", path, "--", "phantom-nonexistent-executable-59288")
            self.assertEqual(127, proc.returncode)
            self.assertFalse(path.exists())


    def test_txt_drops_control_bytes_and_preserves_unicode(self):
        with tempfile.TemporaryDirectory() as root:
            saved = Path(root) / "clean.txt"
            child = (
                "import sys;"
                "sys.stdout.buffer.write("
                "b'first\\x00\\x07\\x08\\x0b\\x0c\\x7f\\rsecond\\r\\nthird\\n'"
                "+'💀 🔍\\n'.encode('utf-8'));"
                "sys.stdout.buffer.flush()"
            )
            proc = invoke("-o", saved, "--", sys.executable, "-u", "-c", child)
            self.assertEqual(0, proc.returncode, proc.stderr)
            content = saved.read_bytes()
            self.assertEqual("first\nsecond\nthird\n💀 🔍\n",
                             content.decode("utf-8"))
            self.assertFalse(any(byte < 32 and byte not in (9, 10)
                                 or byte == 127 for byte in content))

    def test_incremental_line_and_escape_cleaning(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location("phantom_easy_save", WRAPPER)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        clean = mod.StripAnsi()
        parts = [
            b"hello\r",
            b"\nESC:\x1b[3",
            b"1mgreen\x1b[0m\x00\r",
            b"next\r",
        ]
        result = b"".join(clean.clean(part) for part in parts) + clean.finish()
        self.assertEqual(b"hello\nESC:green\nnext\n", result)



if __name__ == "__main__":
    unittest.main()
