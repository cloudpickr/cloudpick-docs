#!/usr/bin/env python3
"""source_fetch.py 테스트 — mock resolver/opener로 SSRF 방어·상한·리다이렉트 검증."""
import io
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import source_fetch as sf  # noqa: E402


class FakeBody(io.BytesIO):
    pass


def opener_ok(body=b"hello world"):
    def _op(url):
        return 200, {}, FakeBody(body)
    return _op


def opener_redirect(location):
    calls = {"n": 0}
    def _op(url):
        calls["n"] += 1
        if calls["n"] == 1:
            return 302, {"Location": location}, FakeBody(b"")
        return 200, {}, FakeBody(b"final")
    return _op


class TestScheme(unittest.TestCase):
    def test_http_rejected(self):
        with self.assertRaises(sf.FetchError):
            sf.fetch_source("http://example.com/x", opener=opener_ok(), resolver=lambda h: ["1.2.3.4"])

    def test_file_scheme_rejected(self):
        with self.assertRaises(sf.FetchError):
            sf.fetch_source("file:///etc/passwd", opener=opener_ok(), resolver=lambda h: ["1.2.3.4"])


class TestSSRFResolver(unittest.TestCase):
    def test_ip_safety_checks(self):
        self.assertFalse(sf._ip_is_safe("127.0.0.1"))       # loopback
        self.assertFalse(sf._ip_is_safe("10.0.0.5"))        # private
        self.assertFalse(sf._ip_is_safe("192.168.1.1"))     # private
        self.assertFalse(sf._ip_is_safe("169.254.169.254")) # metadata/link-local
        self.assertFalse(sf._ip_is_safe("100.64.1.1"))      # CGNAT
        self.assertFalse(sf._ip_is_safe("::1"))             # ipv6 loopback
        self.assertTrue(sf._ip_is_safe("93.184.216.34"))    # public

    def test_real_resolver_blocks_private(self):
        # resolver를 직접 호출해 사설 IP면 FetchError
        with self.assertRaises(sf.FetchError):
            sf.fetch_source("https://x.test/", opener=opener_ok(),
                            resolver=lambda h: (_ for _ in ()).throw(sf.FetchError("blocked 10.0.0.1")))


class TestRedirect(unittest.TestCase):
    def test_redirect_revalidated(self):
        # 리다이렉트 목적지도 resolver로 재검증됨(안전하면 통과)
        seen = []
        def resolver(h):
            seen.append(h)
            return ["93.184.216.34"]
        r = sf.fetch_source("https://a.test/x", opener=opener_redirect("https://b.test/y"),
                            resolver=resolver)
        self.assertEqual(r.status, 200)
        self.assertEqual(seen, ["a.test", "b.test"])  # 두 홉 모두 검증

    def test_redirect_to_private_blocked(self):
        def resolver(h):
            if h == "evil.test":
                raise sf.FetchError("redirect to private blocked")
            return ["93.184.216.34"]
        with self.assertRaises(sf.FetchError):
            sf.fetch_source("https://a.test/x", opener=opener_redirect("https://evil.test/y"),
                            resolver=resolver)


class TestLimits(unittest.TestCase):
    def test_bytes_cap(self):
        big = b"x" * (sf.MAX_BYTES + 10)
        with self.assertRaises(sf.FetchError):
            sf.fetch_source("https://a.test/x", opener=opener_ok(big),
                            resolver=lambda h: ["93.184.216.34"])

    def test_ok_within_limits(self):
        r = sf.fetch_source("https://a.test/x", opener=opener_ok(b"small body"),
                            resolver=lambda h: ["93.184.216.34"])
        self.assertEqual(r.status, 200)
        self.assertEqual(len(r.body_sha256), 64)


if __name__ == "__main__":
    unittest.main(verbosity=2)
