"""Offline regression suite for SUBDOMINATRIX. Zero real DNS or HTTP calls."""
import csv
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "subdominatrix.py"


def load_tool():
    spec = importlib.util.spec_from_file_location("subdominatrix", SCRIPT)
    tool = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tool)
    return tool


class SubdominatrixTests(unittest.TestCase):
    def test_domain_boundaries_and_validation(self):
        m = load_tool()
        for target in ("example.com", "sub.example.org", "x-y.example.net"):
            self.assertTrue(m.valid_domain(target))
        for bad in ("http://example.com", "example.com/path", "127.0.0.1",
                    "localhost", "a..com", "_secret.com", "bad.com:443"):
            self.assertFalse(m.valid_domain(bad), bad)
        self.assertEqual("api.example.com", m.normalize("*.API.Example.Com", "example.com"))
        for bad in ("example.com", "notexample.com", "api.badexample.com",
                    "example.com.bad.org", "a..example.com", "http://a.example.com"):
            self.assertIsNone(m.normalize(bad, "example.com"), bad)
        self.assertTrue(m.public_ip("8.8.8.8"))
        self.assertFalse(m.public_ip("127.0.0.1"))
        self.assertFalse(m.public_ip("10.10.10.10"))
        self.assertFalse(m.public_ip("203.0.113.45"))

    def test_offline_demo_real_outputs(self):
        m = load_tool()
        report = m.collect("example.com", demo=True)
        self.assertEqual("SYNTHETIC OFFLINE DEMO", report["mode"])
        self.assertGreaterEqual(report["stats"]["names"], 10)
        self.assertGreater(report["stats"]["multi_source"], 0)
        self.assertEqual(0, report["stats"]["http_observed"])
        self.assertEqual(0, report["stats"]["dns_public"])
        self.assertTrue(all(record["dns"] == "not checked" for record in report["hosts"]))
        self.assertEqual(4, len(report["sources"]))
        with tempfile.TemporaryDirectory() as tmp:
            paths1 = m.export(report, tmp)
            paths2 = m.export(report, tmp)
            self.assertNotEqual(paths1["html"], paths2["html"])
            self.assertEqual({"csv", "txt", "html", "json"}, set(paths1))
            doc = json.loads(paths1["json"].read_text(encoding="utf-8"))
            self.assertEqual(report["stats"], doc["stats"])
            with paths1["csv"].open(newline="", encoding="utf-8") as fp:
                rows = list(csv.DictReader(fp))
            self.assertEqual(report["stats"]["names"], len(rows))
            self.assertEqual(report["stats"]["names"],
                             len(paths1["txt"].read_text().splitlines()))
            page = paths1["html"].read_text()
            self.assertIn("SUBDOMINATRIX", page)
            self.assertIn("SYNTHETIC OFFLINE DEMO", page)
            self.assertIn("Filter hostnames", page)

    def test_cli_offline_and_invalid_arguments(self):
        with tempfile.TemporaryDirectory() as temp:
            good = subprocess.run([sys.executable, str(SCRIPT), "--offline-demo",
                                   "--no-open", "--out", temp],
                                  text=True, capture_output=True, timeout=15)
            self.assertEqual(0, good.returncode, good.stderr)
            self.assertIn("[SAVED] HTML", good.stdout)
            self.assertEqual(1, len(list(Path(temp).glob("*.html"))))
            for args in (["bad..com", "--offline-demo"], ["--offline-demo", "--http-check"],
                         ["--offline-demo", "--max-results", "0"],
                         ["--offline-demo", "--max-verify", "999"]):
                bad = subprocess.run([sys.executable, str(SCRIPT), *args, "--no-open"],
                                     text=True, capture_output=True, timeout=15)
                self.assertNotEqual(0, bad.returncode, args)

    def test_real_source_parsers_mocked(self):
        m = load_tool()
        fake = [
            {"name_value": "*.api.example.com\nwww.example.com\nexample.com\nunsafe.bad.com"},
            {"name_value": "shop.example.com"}
        ]
        with patch.object(m, "fetch_json", return_value=fake):
            self.assertEqual(["api.example.com", "shop.example.com", "www.example.com"],
                             m.fetch_source("crt.sh", "example.com"))
        with patch.object(m, "fetch_json", return_value={
                "passive_dns": [{"hostname": "a.example.com"},
                                {"hostname": "x.example.com.attacker.com"}]}):
            self.assertEqual(["a.example.com"],
                             m.fetch_source("AlienVault OTX", "example.com"))
        with patch.object(m, "fetch_json", return_value={"results": [
            {"page": {"domain": "blog.example.com"},
             "task": {"domain": "admin.OTHER.com"}}]}):
            self.assertEqual(["blog.example.com"],
                             m.fetch_source("urlscan.io", "example.com"))

    def test_live_collection_with_mocked_providers_and_resolution(self):
        m = load_tool()
        names = {
            "crt.sh": ["www.example.com", "api.example.com"],
            "AlienVault OTX": ["www.example.com"],
            "HackerTarget": ["mail.example.com"],
            "urlscan.io": ["www.example.com", "shop.example.com"],
        }
        with patch.object(m, "fetch_source", side_effect=lambda name, domain, timeout: names[name]):
            with patch.object(m, "dns_check", side_effect=lambda name, timeout: {
                "dns": "public", "ips": ["8.8.8.8"], "detail": ""}):
                with patch.object(m, "head_https", return_value={
                    "http": "observed", "status": 200, "tech": ["nginx"], "detail": "mock"}):
                    report = m.collect("example.com", dns=True, http=True,
                                       max_verify=2, max_results=12)
        self.assertEqual(4, report["stats"]["names"])
        self.assertEqual(1, report["stats"]["multi_source"])
        self.assertEqual(2, report["stats"]["http_observed"])
        self.assertEqual(1, report["stats"]["unique_ips"])
        self.assertEqual(["nginx"], report["stats"]["technologies"])

    def test_output_escapes_html(self):
        m = load_tool()
        report = m.collect("example.com", demo=True)
        report["hosts"][0]["name"] = "<img src=x onerror=alert(1)>"
        rendered = m.render(report)
        self.assertNotIn("<img src=x onerror=alert(1)>", rendered)
        self.assertIn("&lt;img", rendered)

    def test_nonpublic_dns_is_skipped_by_http_probe(self):
        m = load_tool()
        self.assertEqual("skipped", m.head_https("internal.example.com",
                                                  ["127.0.0.1"])["http"])
        self.assertEqual("skipped", m.head_https("mixed.example.com",
                                                  ["8.8.8.8", "10.0.0.1"])["http"])


    def test_terminal_only_offline_mode_makes_no_files(self):
        with tempfile.TemporaryDirectory() as temp:
            run = subprocess.run(
                [sys.executable, str(SCRIPT), "example.com", "--offline-demo",
                 "--terminal-only", "--color", "always", "--out", temp],
                capture_output=True, text=True, timeout=15)
            self.assertEqual(0, run.returncode, run.stderr)
            self.assertIn("[DONE] SAVE OFF", run.stdout)
            self.assertIn("SYNTHETIC OFFLINE DEMO", run.stdout)
            self.assertEqual([], list(Path(temp).iterdir()))
            self.assertNotIn("[SAVED]", run.stdout)
            self.assertNotIn("[OPEN]", run.stdout)

    def test_public_source_progress_and_rate_limit_are_truthful(self):
        import urllib.error
        m = load_tool()
        events = []
        def fake_source(source, domain, timeout):
            if source == "AlienVault OTX":
                raise urllib.error.HTTPError(
                    "https://otx.alienvault.com/", 429,
                    "Too Many Requests", {"Retry-After": "6"}, None)
            return ["api.example.com", "www.example.com"]
        with patch.object(m, "fetch_source", side_effect=fake_source):
            report = m.collect("example.com", max_results=10,
                               timeout=3, progress=events.append)
        self.assertEqual(2, report["stats"]["names"])
        self.assertTrue(any("[FOUND] api.example.com" in x for x in events))
        self.assertTrue(any("[SOURCE] AlienVault OTX: rate-limited" in x for x in events))
        rate = next(x for x in report["sources"] if x["source"] == "AlienVault OTX")
        self.assertEqual("rate-limited", rate["status"])
        self.assertIn("provider cooldown 6", rate["detail"])

    def test_terminal_only_respects_source_validation(self):
        m = load_tool()
        events = []
        with patch.object(m, "fetch_source", return_value=["api.example.com"]):
            report = m.collect("example.com", max_results=1,
                               timeout=3, progress=events.append)
        self.assertEqual(1, report["stats"]["names"])
        self.assertEqual(1, len([e for e in events if e.startswith("[FOUND]")]))


    def test_findomain_cli_streams_candidates_and_reports_nonzero_exit(self):
        m = load_tool()
        with tempfile.TemporaryDirectory() as td:
            fake = Path(td) / "fake-findomain"
            fake.write_text(
                "#!" + sys.executable + "\n"
                "print('api.example.com', flush=True)\n"
                "print('www.example.com', flush=True)\n"
                "print('Provider failed later', flush=True)\n"
                "raise SystemExit(3)\n", encoding="utf-8")
            fake.chmod(0o755)
            events = []
            with patch.object(m.shutil, "which", return_value=str(fake)):
                names, info = m.optional_cli(
                    "findomain", "example.com", timeout=5, progress=events.append)
        self.assertEqual(["api.example.com", "www.example.com"], names)
        self.assertEqual("partial", info["status"])
        self.assertIn("Exit 3", info["detail"])
        self.assertIn("Provider failed later", info["detail"])
        self.assertTrue(any("[FOUND] api.example.com" in x for x in events))
        self.assertTrue(any("[FOUND] www.example.com" in x for x in events))

    def test_findomain_cli_timeout_keeps_partial_results(self):
        m = load_tool()
        with tempfile.TemporaryDirectory() as td:
            fake = Path(td) / "fake-findomain"
            fake.write_text(
                "#!" + sys.executable + "\n"
                "import time\n"
                "print('api.example.com', flush=True)\n"
                "time.sleep(5)\n", encoding="utf-8")
            fake.chmod(0o755)
            events = []
            with patch.object(m.shutil, "which", return_value=str(fake)):
                names, info = m.optional_cli(
                    "findomain", "example.com", timeout=0.5, progress=events.append)
        self.assertEqual(["api.example.com"], names)
        self.assertEqual("partial", info["status"])
        self.assertIn("0.5s CLI limit", info["detail"])
        self.assertTrue(any("[FOUND] api.example.com" in x for x in events))

    def test_reject_unbounded_optional_cli_timeout(self):
        m = load_tool()
        with self.assertRaisesRegex(ValueError, "cli-timeout"):
            m.collect("example.com", demo=True, cli_timeout=121)


    def test_easy_o_txt_saves_exact_requested_name_and_only_txt(self):
        with tempfile.TemporaryDirectory() as temp:
            requested = Path(temp) / "names.txt"
            result = subprocess.run([
                sys.executable, str(SCRIPT), "example.com", "--offline-demo",
                "-o", str(requested), "--color", "never"
            ], text=True, capture_output=True, timeout=15)
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertTrue(requested.is_file())
            names = requested.read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(names), len(set(names)))
            self.assertGreater(len(names), 0)
            self.assertTrue(all(name.endswith(".example.com") for name in names))
            self.assertEqual([requested], list(Path(temp).iterdir()))
            self.assertIn("[SAVED] TXT", result.stdout)
            self.assertNotIn("[OPEN]", result.stdout)
            self.assertNotIn("[SAVED] HTML", result.stdout)

    def test_easy_o_can_combine_with_terminal_only(self):
        with tempfile.TemporaryDirectory() as temp:
            requested = Path(temp) / "intel.txt"
            result = subprocess.run([
                sys.executable, str(SCRIPT), "example.com", "--offline-demo",
                "--terminal-only", "-o", str(requested)
            ], text=True, capture_output=True, timeout=15)
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertTrue(requested.is_file())
            self.assertEqual(1, len(list(Path(temp).iterdir())))

    def test_easy_o_never_replaces_preexisting_output(self):
        with tempfile.TemporaryDirectory() as temp:
            requested = Path(temp) / "keep.txt"
            requested.write_text("IMPORTANT ORIGINAL\n", encoding="utf-8")
            result = subprocess.run([
                sys.executable, str(SCRIPT), "example.com", "--offline-demo",
                "-o", str(requested)
            ], text=True, capture_output=True, timeout=15)
            self.assertNotEqual(0, result.returncode)
            self.assertIn("already exists", result.stderr)
            self.assertEqual("IMPORTANT ORIGINAL\n", requested.read_text())
            self.assertEqual(1, len(list(Path(temp).iterdir())))

    def test_easy_o_rejects_nontxt_filename(self):
        with tempfile.TemporaryDirectory() as temp:
            result = subprocess.run([
                sys.executable, str(SCRIPT), "example.com", "--offline-demo",
                "-o", str(Path(temp) / "report.json")
            ], text=True, capture_output=True, timeout=15)
            self.assertNotEqual(0, result.returncode)
            self.assertIn(".txt", result.stderr)
            self.assertFalse((Path(temp) / "report.json").exists())

    def test_easy_o_is_genuine_hostnames_without_metadata(self):
        m = load_tool()
        report = m.collect("example.com", demo=True)
        with tempfile.TemporaryDirectory() as temp:
            path = m.save_hostnames_txt(report, Path(temp) / "names.txt")
            lines = path.read_text(encoding="utf-8").splitlines()
            self.assertEqual(sorted(record["name"] for record in report["hosts"]), lines)
            self.assertNotIn("SYNTHETIC OFFLINE DEMO", path.read_text())


if __name__ == "__main__":
    unittest.main()
