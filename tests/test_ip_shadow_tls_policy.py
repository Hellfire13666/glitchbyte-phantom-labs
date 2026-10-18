"""Offline TLS regression checks for the preserved IP Shadow Scraper.

Mocks the network and TLS handshake. Confirms verified TLS is requested,
without claiming a live endpoint certificate was validated.
"""
import importlib.util
from pathlib import Path
import ssl
import unittest
from unittest.mock import MagicMock, patch

SOURCE = Path(__file__).resolve().parents[1] / "tools" / "rosie_ip_shadow_scraper.py"


def load_original():
    spec = importlib.util.spec_from_file_location("rosie_ip_shadow_scraper_under_test", SOURCE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class IpShadowTlsPolicyTests(unittest.TestCase):
    def test_tls_fingerprint_uses_verified_hostname_context(self):
        tool = load_original()
        context = MagicMock()
        connection = MagicMock()
        wrapped = MagicMock()
        connection.__enter__.return_value = connection
        wrapped.__enter__.return_value = wrapped
        context.wrap_socket.return_value = wrapped
        wrapped.getpeercert.return_value = b"example-der-for-offline-test"
        wrapped.version.return_value = "TLSv1.3"
        wrapped.cipher.return_value = ("TLS_AES_256_GCM_SHA384", "TLSv1.3", 256)

        with patch.object(tool.ssl, "create_default_context", return_value=context) as make_context, \
             patch.object(tool.socket, "create_connection", return_value=connection) as connect:
            report = tool.tls(tool.parse_ip("192.0.2.1"))

        make_context.assert_called_once_with()
        self.assertTrue(context.check_hostname)
        self.assertEqual(context.verify_mode, ssl.CERT_REQUIRED)
        connect.assert_called_once_with(("192.0.2.1", 443), timeout=tool.TIMEOUT)
        context.wrap_socket.assert_called_once_with(connection, server_hostname="192.0.2.1")
        self.assertIn("certificate_sha256", report)
        self.assertNotIn("error", report)

    def test_untrusted_certificate_does_not_produce_fingerprint(self):
        tool = load_original()
        context = MagicMock()
        connection = MagicMock()
        connection.__enter__.return_value = connection
        context.wrap_socket.side_effect = ssl.SSLCertVerificationError("certificate verify failed")

        with patch.object(tool.ssl, "create_default_context", return_value=context), \
             patch.object(tool.socket, "create_connection", return_value=connection):
            report = tool.tls(tool.parse_ip("192.0.2.1"))
        self.assertIn("error", report)
        self.assertNotIn("certificate_sha256", report)


if __name__ == "__main__":
    unittest.main()
