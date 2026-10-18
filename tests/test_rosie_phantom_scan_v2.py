"""Offline ROSIE PHANTOM SCAN V2 regression and report checks."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "rosie_phantom_scan_v2.py"


def load():
    spec = importlib.util.spec_from_file_location("rosie_v2", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class RosieScanV2Tests(unittest.TestCase):
    def test_validation(self):
        mod = load()
        for domain in ("example.com", "sub.example.org", "x-y.example.net"):
            self.assertTrue(mod.valid_domain(domain))
        for invalid in ("127.0.0.1", "localhost", "a..com", "x.com/path",
                        "http://example.com", "example.com:8080", "evil_.com"):
            self.assertFalse(mod.valid_domain(invalid), invalid)
        self.assertFalse(mod.public_ip("127.0.0.1"))
        self.assertFalse(mod.public_ip("192.168.1.1"))
        self.assertTrue(mod.public_ip("8.8.8.8"))
        self.assertEqual("one.example.com", mod.normalize_subdomain("*.one.example.com", "example.com"))
        self.assertIsNone(mod.normalize_subdomain("one.other.com", "example.com"))

    def test_offline_preview_and_real_exports(self):
        mod = load()
        report = mod.collect("example.com", offline=True, passive=True, findomain=True, whois_cli=True)
        self.assertEqual([], report["ip_addresses"])
        self.assertEqual({}, report["dns"])
        self.assertIn("Offline", report["notes"][0])
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            image = folder / "rosie_header.png"
            image.write_bytes(b"\x89PNG\r\n\x1a\n" + b"demo-artwork")
            p1, j1 = mod.export(report, folder, image)
            p2, j2 = mod.export(report, folder, image)
            for item in (p1, j1, p2, j2):
                self.assertTrue(item.is_file())
            self.assertNotEqual(p1, p2)
            self.assertEqual("example.com", json.loads(j1.read_text())["domain"])
            markup = p1.read_text()
            self.assertIn("ROSIE PHANTOM", markup)
            self.assertIn("WHOIS", markup)
            self.assertIn("FINDOMAIN", markup)
            self.assertIn("data:image/png;base64,", markup)
            self.assertIn("CERTIFICATE TRANSPARENCY", markup)

    def test_html_escapes_source_values(self):
        mod = load()
        report = mod.collect("example.com", offline=True)
        report["website"] = {"title": "<script>alert('x')</script>"}
        rendered = mod.render(report)
        self.assertNotIn("<script>", rendered)
        self.assertIn("&lt;script&gt;", rendered)

    def test_cli_offline_no_browser_and_bad_target(self):
        with tempfile.TemporaryDirectory() as temp:
            good = subprocess.run([sys.executable, str(SCRIPT), "example.com",
                                   "--offline", "--no-browser", "--out", temp],
                                  text=True, capture_output=True, timeout=20)
            self.assertEqual(0, good.returncode, good.stderr)
            self.assertIn("[SAVED] HTML:", good.stdout)
            self.assertEqual(1, len(list(Path(temp).glob("*.html"))))
            self.assertEqual(1, len(list(Path(temp).glob("*.json"))))
            bad = subprocess.run([sys.executable, str(SCRIPT), "127.0.0.1",
                                  "--offline", "--no-browser", "--out", temp],
                                 text=True, capture_output=True, timeout=20)
            self.assertNotEqual(0, bad.returncode)

    def test_website_parser_bounded_local_paths(self):
        mod = load()
        parser = mod.PageMetadata()
        parser.feed('<title>Hello &amp; hi</title><meta name="description" content="sample">'
                    '<a href="/about">A</a><a href="//another.com/path">No</a>')
        self.assertEqual("Hello & hi", "".join(parser.title))
        self.assertEqual(["/about"], parser.links)
        self.assertEqual("sample", parser.description)


if __name__ == "__main__":
    unittest.main()
