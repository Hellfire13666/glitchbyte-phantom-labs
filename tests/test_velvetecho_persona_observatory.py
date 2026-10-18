"""Offline deterministic regression coverage for VELVETECHO."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'tools' / 'velvetecho-persona-observatory' / 'velvetecho_persona_observatory.py'
module_spec = importlib.util.spec_from_file_location('velvetecho_persona_observatory', SOURCE)
velvet = importlib.util.module_from_spec(module_spec)
module_spec.loader.exec_module(velvet)


class VelvetEchoTests(unittest.TestCase):
    def test_unique_persona_handles(self):
        self.assertEqual(velvet.parse_handles('@Rosie,rosie,Pixie_1'), ['Rosie', 'rosie', 'Pixie_1'])
        with self.assertRaises(ValueError):
            velvet.parse_handles('alice,bob,charlie,david,ella,frank')
        for bad in ['a/b', 'https://example.com', '🥀', 'x' * 41, '']:
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                velvet.parse_handle(bad)

    def test_offline_site_catalog_and_urls(self):
        sites = velvet.catalog()
        self.assertGreaterEqual(len(sites), 8)
        self.assertTrue(all(x['url'].startswith('https://') for x in sites))
        data = velvet.candidates(['rosie_glitch'], sites)
        self.assertEqual(len(data), len(sites))
        self.assertTrue(all(x['status'] == 'CANDIDATE' for x in data))
        self.assertIn('rosie_glitch', data[0]['url'])

    def test_custom_site_catalog(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'catalog.json'
            path.write_text(json.dumps({'sites': [{'name': 'My public hub', 'category':'custom', 'url':'https://example.org/u/{username}'}]}), encoding='utf-8')
            sites = velvet.catalog(path)
            self.assertEqual(sites[0]['name'], 'My public hub')
            self.assertIn('/u/rose', velvet.candidates(['rose'], sites)[0]['url'])

    def test_invalid_custom_catalogs_rejected(self):
        bad = [
            'http://example.org/{username}',
            'https://127.0.0.1/{username}',
            'https://localhost.local/{username}',
            'https://example.org:8080/u/{username}',
            'https://example.org/u/rosie',
            'https://example.org/{username}/{username}',
            'https://evil.test/{username}?q={other}',
            'https://user:pass@example.org/{username}',
        ]
        for template in bad:
            with self.subTest(template=template), self.assertRaises(ValueError):
                velvet.validate_template(template)

    def test_private_ip_dns_blocked(self):
        fake = [(2, 1, 6, '', ('127.0.0.1', 443))]
        with patch.object(velvet.socket, 'getaddrinfo', return_value=fake):
            with self.assertRaises(ValueError):
                velvet.resolve_public_domain('example.org')

    def test_robots_denial_skips_target(self):
        row = velvet.candidates(['rosie'], velvet.catalog()[:1])[0]
        with patch.object(velvet, 'robots_allowed', return_value=(False, 'Disallowed by robots.txt')):
            with patch.object(velvet, 'http_read', side_effect=AssertionError('Target must not be fetched')):
                result = velvet.inspect(row)
        self.assertEqual(result['status'], 'UNKNOWN')
        self.assertIn('robots.txt', result['note'])

    def test_robots_404_allows_and_disallow_blocks(self):
        with patch.object(velvet, 'http_read', return_value=(404, 'text/plain', b'')):
            allowed, _ = velvet.robots_allowed('https://example.org/rosie', 6)
            self.assertTrue(allowed)
        with patch.object(velvet, 'http_read', return_value=(200, 'text/plain', b'User-agent: *\nDisallow: /\n')):
            allowed, _ = velvet.robots_allowed('https://example.org/rosie', 6)
            self.assertFalse(allowed)

    def test_conservative_statuses(self):
        row = velvet.candidates(['rosie'], velvet.catalog()[:1])[0]
        with patch.object(velvet, 'robots_allowed', return_value=(True, 'Allowed')):
            for code, kind, data, status in [
                (200, 'text/html', b'Rosie public profile', 'POSSIBLE'),
                (200, 'text/plain', b'Rosie', 'UNKNOWN'),
                (404, 'text/html', b'', 'NOT_FOUND'),
                (302, 'text/html', b'', 'UNKNOWN'),
                (429, 'text/html', b'', 'UNKNOWN'),
            ]:
                with self.subTest(code=code), patch.object(velvet, 'http_read', return_value=(code, kind, data)):
                    self.assertEqual(velvet.inspect(row)['status'], status)

    def test_html_escapes_names_and_urls(self):
        row = velvet.demo_rows()[0]
        row['site'] = '<img src=x onerror=alert(1)>'
        row['note'] = '<script>alert(1)</script>'
        report = {'mode': 'DEMO', 'created_at':'2026', 'results':[row]}
        html = velvet.render_html(report)
        self.assertNotIn('<script>alert(1)</script>', html)
        self.assertIn('&lt;script&gt;alert(1)&lt;/script&gt;', html)
        self.assertNotIn('<img src=x onerror=alert(1)>', html)

    def test_reports_unique_and_complete(self):
        with tempfile.TemporaryDirectory() as temp:
            first = velvet.write_reports(velvet.demo_rows(), temp, 'DEMO')
            second = velvet.write_reports(velvet.demo_rows(), temp, 'DEMO')
            self.assertNotEqual(first[0], second[0])
            self.assertTrue(all(x.exists() for x in first + second))
            report = json.loads(first[0].read_text(encoding='utf-8'))
            self.assertEqual(len(report['results']), 4)
            self.assertIn('VELVETECHO', first[2].read_text(encoding='utf-8'))
            self.assertIn('status,code,note', first[1].read_text(encoding='utf-8'))

    def test_offline_cli_never_calls_live(self):
        with tempfile.TemporaryDirectory() as temp:
            with patch.object(velvet, 'inspect', side_effect=AssertionError('network not allowed')):
                self.assertEqual(velvet.main(['-u', 'rosie', '--out', temp]), 0)
            report = next(Path(temp).glob('velvetecho_signals_*.json'))
            self.assertTrue(all(r['status'] == 'CANDIDATE' for r in json.loads(report.read_text())['results']))

    def test_live_requires_permission(self):
        with self.assertRaises(SystemExit) as cm:
            velvet.main(['--live', '--usernames', 'rosie'])
        self.assertEqual(cm.exception.code, 2)

    def test_phone_structure_and_masking(self):
        record = velvet.phone_report_entry('+1 202 555 0117')
        self.assertEqual(record['status'], 'FORMAT_OK')
        self.assertEqual(record['region'], 'NANP (US/Canada/etc.)')
        self.assertNotIn('2025550117', str(record))
        self.assertIn('0117', record['number'])
        self.assertEqual(velvet.phone_report_entry('+44 20 7946 0958')['status'], 'FORMAT_OK')
        self.assertEqual(velvet.phone_report_entry('123')['status'], 'INVALID')
        self.assertEqual(velvet.phone_report_entry('020 7946 0958')['status'], 'UNKNOWN')

    def test_phone_dedup_country_hint_and_invalid_digits(self):
        records = velvet.parse_phones('202-555-0117,+1 (202) 555-0117,+49 30 123456')
        self.assertEqual(len(records), 2)
        self.assertIn('Germany', records[1]['region'])
        self.assertEqual(velvet.phone_report_entry('+1 022 555 0123')['status'], 'INVALID')
        self.assertEqual(velvet.phone_report_entry('+1 202 055 0123')['status'], 'INVALID')
        self.assertEqual(velvet.phone_report_entry('555.1234')['status'], 'INVALID')

    def test_phone_research_links_are_opt_in_and_never_fetched(self):
        with tempfile.TemporaryDirectory() as temp:
            with patch.object(velvet, 'http_read', side_effect=AssertionError('No network for phones')):
                self.assertEqual(velvet.main(['--phones', '+1 202 555 0117', '--out', temp]), 0)
            doc = json.loads(next(Path(temp).glob('*.json')).read_text())
            self.assertFalse(doc['phone_results'][0]['research_url'])
            self.assertNotIn('12025550117', str(doc))
            with self.assertRaises(SystemExit):
                velvet.main(['--phones', '+1 202 555 0117', '--phone-research-links'])
        record = velvet.phone_report_entry('+1 202 555 0117', research=True)
        self.assertTrue(record['research_url'].startswith('https://www.google.com/search?q='))

    def test_html_includes_escaped_phone_cards(self):
        phone = velvet.phone_report_entry('+1 202 555 0117')
        phone['note'] = '<svg onload=alert(1)>'
        doc = {'mode':'DEMO', 'created_at':'2026', 'results':[], 'phone_results':[phone]}
        rendered = velvet.render_html(doc)
        self.assertIn('PHONE SIGNAL READOUT', rendered)
        self.assertIn('&lt;svg onload=alert(1)&gt;', rendered)
        self.assertNotIn('<svg onload=alert(1)>', rendered)

    def test_phone_csv_and_report_uniqueness(self):
        with tempfile.TemporaryDirectory() as temp:
            paths = velvet.write_reports([], temp, 'OFFLINE', velvet.parse_phones('+44 20 7946 0958'))
            csvs = list(Path(temp).glob('*_phones.csv'))
            self.assertEqual(len(csvs), 1)
            self.assertIn('FORMAT_OK', csvs[0].read_text())
            self.assertIn('phone_results', json.loads(paths[0].read_text()))

    def test_color_codes_only_when_requested(self):
        self.assertNotIn('\x1b', velvet.paint('POSSIBLE', 'POSSIBLE', False))
        self.assertIn('\x1b[92m', velvet.paint('POSSIBLE', 'POSSIBLE', True))

    def test_short_invalid_phone_also_masked(self):
        record = velvet.phone_report_entry('123')
        self.assertNotIn('123', record['number'])
        self.assertEqual(record['status'], 'INVALID')

    def test_private_phone_file_input(self):
        with tempfile.TemporaryDirectory() as temp:
            phone_list = Path(temp) / 'my-phones.txt'
            phone_list.write_text('+1 202 555 0117\n+44 20 7946 0958\n', encoding='utf-8')
            with patch.object(velvet, 'http_read', side_effect=AssertionError('Offline only')):
                self.assertEqual(velvet.main(['--phones-file', str(phone_list), '--out', temp]), 0)
            report_path = next(Path(temp).glob('velvetecho_signals_*.json'))
            report = json.loads(report_path.read_text(encoding='utf-8'))
            self.assertEqual(len(report['phone_results']), 2)
            self.assertNotIn('12025550117', report_path.read_text())

    def test_demo_synthetic_only(self):
        with tempfile.TemporaryDirectory() as temp:
            with patch.object(velvet, 'inspect', side_effect=AssertionError('not live')):
                self.assertEqual(velvet.main(['--demo', '--out', temp]), 0)
            record = next(Path(temp).glob('*.json'))
            self.assertIn('SYNTHETIC DEMO', json.loads(record.read_text())['mode'])


if __name__ == '__main__':
    unittest.main()
