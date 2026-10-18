"""No network, secrets or external fixtures required."""
from __future__ import annotations
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from PIL import Image

FILE = Path(__file__).resolve().parents[1] / 'screamframe_pixel_autopsy.py'
spec = importlib.util.spec_from_file_location('screamframe', FILE)
sf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sf)


class PixelAutopsyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.source = self.base / 'input'
        self.source.mkdir()
        self.reports = self.base / 'reports'

    def test_demo_has_exact_and_visual_and_mismatch(self):
        sf.generate_demo(self.source)
        result = sf.scan(self.source, self.reports, demo=True)
        self.assertEqual(result['counts']['inspected'], 4)
        self.assertEqual(result['counts']['exact_groups'], 1)
        self.assertEqual(result['counts']['visual_pairs'], 2)
        self.assertEqual(result['counts']['format_mismatches'], 1)
        self.assertEqual(result['source'], 'synthetic demo')
        self.assertTrue(all(len(x['sha256']) == 64 for x in result['files']))

    def test_no_symlinks_or_nested_reports(self):
        sf.generate_demo(self.source)
        nested = self.source / 'reports'
        nested.mkdir()
        Image.new('RGB', (10, 10)).save(nested / 'not_scanned.png')
        (self.source / 'shortcut.png').symlink_to(self.source / 'screen_original.png')
        result = sf.scan(self.source, nested)
        self.assertEqual(result['counts']['inspected'], 4)
        self.assertFalse(any(x['file'].startswith('reports/') for x in result['files']))
        self.assertFalse(any(x['file'] == 'shortcut.png' for x in result['files']))

    def test_bad_images_and_oversized_skipped(self):
        (self.source / 'bad.png').write_bytes(b'not a real png')
        big = self.source / 'large.png'
        big.write_bytes(b'x' * (1024 * 1024 + 1))
        result = sf.scan(self.source, self.reports, max_mb=1)
        self.assertEqual(result['counts']['skipped'], 2)
        self.assertEqual(result['counts']['inspected'], 0)

    def test_html_escapes_untrusted_names_and_reports_do_not_store_previews(self):
        Image.new('RGB', (20, 20)).save(self.source / 'a<b&c>.png')
        result = sf.scan(self.source, self.reports, previews=True)
        j, h = sf.save_reports(result, self.reports)
        html = h.read_text()
        self.assertIn('a&lt;b&amp;c&gt;.png', html)
        self.assertNotIn('a<b&c>.png', html)
        self.assertIn('data:image/png;base64,', html)
        data = json.loads(j.read_text())
        self.assertNotIn('thumbnail_data_uri', data['files'][0])

    def test_limits_and_exact_hashes(self):
        sf.generate_demo(self.source)
        result = sf.scan(self.source, self.reports, max_images=2, threshold=0)
        self.assertEqual(result['counts']['inspected'], 2)
        self.assertEqual(result['counts']['skipped'], 2)
        self.assertEqual(result['counts']['visual_pairs'], 0)
        self.assertEqual(result['counts']['exact_groups'], 0)

    def test_exports_never_overwrite(self):
        sf.generate_demo(self.source)
        report = sf.scan(self.source, self.reports)
        a, _ = sf.save_reports(report, self.reports)
        b, _ = sf.save_reports(report, self.reports)
        self.assertNotEqual(a, b)
        self.assertTrue(a.exists() and b.exists())

    def test_read_only_original_images(self):
        sf.generate_demo(self.source)
        path = self.source / 'screen_original.png'
        before = (sf.sha256_file(path), path.stat().st_mtime_ns)
        sf.scan(self.source, self.reports)
        after = (sf.sha256_file(path), path.stat().st_mtime_ns)
        self.assertEqual(before, after)

    def test_real_cli_demo(self):
        p = subprocess.run([sys.executable, str(FILE), '--demo', '--out', str(self.reports)],
                           capture_output=True, text=True, timeout=30)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn('[REPORT]', p.stdout)
        self.assertEqual(len(list(self.reports.glob('screamframe_echo_*.json'))), 1)
        self.assertEqual(len(list(self.reports.glob('screamframe_echo_*.html'))), 1)


if __name__ == '__main__':
    unittest.main()