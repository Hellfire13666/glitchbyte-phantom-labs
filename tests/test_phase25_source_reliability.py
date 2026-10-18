"""Phase 25 regression tests: artwork location and non-overwriting reports.

All checks are offline, use temporary folders, and do not alter user data.
"""
import importlib.util
import ipaddress
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def load_tool(name):
    source = ROOT / "tools" / name
    spec = importlib.util.spec_from_file_location("phase25_" + name.replace(".", "_"), source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SourceReliabilityTests(unittest.TestCase):
    def test_ip_shadow_art_matches_preserved_artwork(self):
        shadow = load_tool("rosie_ip_shadow_scraper.py")
        art = ROOT / "artwork" / "rosie_ip_shadow_art.png"
        self.assertEqual(shadow.ART.resolve(), art.resolve())
        self.assertTrue(art.is_file())

    def test_rose_crawler_reports_preserve_dotted_username_and_prior_runs(self):
        crawler = load_tool("rose_crawler.py")
        records = [{
            "platform": "Example", "url": "https://example.org", "status": "manual review",
            "http_status": "", "title": "", "description": "",
            "note": "offline example", "checked_at": "2026-10-17T00:00:00Z",
        }]
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            first = crawler.write_report(records, root, "demo.name")
            second = crawler.write_report(records, root, "demo.name")
            self.assertNotEqual(first, second)
            for base in (first, second):
                for ext in (".json", ".csv", ".html"):
                    report = Path(str(base) + ext)
                    self.assertTrue(report.is_file(), report)
                    self.assertIn("rose_demo.name_", report.name)
                self.assertEqual(json.loads(Path(str(base) + ".json").read_text()), records)
            self.assertEqual(6, len(list(root.iterdir())))

    def test_ip_shadow_same_target_reports_do_not_overwrite(self):
        shadow = load_tool("rosie_ip_shadow_scraper.py")
        with tempfile.TemporaryDirectory() as temp:
            with patch.object(shadow, "OUT", Path(temp)):
                target = ipaddress.ip_address("192.0.2.1")
                shadow.save(target, {"test": 1})
                shadow.save(target, {"test": 2})
                reports = list(Path(temp).glob("rosie_ip_192.0.2.1_*.json"))
                self.assertEqual(2, len(reports))
                payloads = [json.loads(p.read_text(encoding="utf-8")) for p in reports]
                self.assertEqual({1, 2}, {p["results"]["test"] for p in payloads})


if __name__ == "__main__":
    unittest.main()
