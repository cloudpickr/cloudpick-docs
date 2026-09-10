#!/usr/bin/env python3
"""envelope.py 테스트 — head/base/packet/policy 변경 시 이전 결과 무효화 검증."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import envelope as ev  # noqa: E402


def make(**over):
    base = dict(
        repo="cloudpickr/cloudpick-docs", pr_number=200,
        base_sha="b" * 40, head_sha="h" * 40,
        packet_sha256="p" * 64, policy_version=ev.POLICY_VERSION,
        reviewer_config_version="rc-1",
        checked_at="2026-09-10T00:00:00Z", expires_at="2026-09-17T00:00:00Z",
    )
    base.update(over)
    return ev.ReviewEnvelope(**base)


class TestEnvelope(unittest.TestCase):
    def test_same_context_valid(self):
        self.assertTrue(ev.is_still_valid(make(), make()))

    def test_changed_head_invalidates(self):
        self.assertFalse(ev.is_still_valid(make(), make(head_sha="x" * 40)))

    def test_changed_base_invalidates(self):
        self.assertFalse(ev.is_still_valid(make(), make(base_sha="x" * 40)))

    def test_changed_packet_invalidates(self):
        self.assertFalse(ev.is_still_valid(make(), make(packet_sha256="q" * 64)))

    def test_changed_policy_invalidates(self):
        self.assertFalse(ev.is_still_valid(make(), make(policy_version="other")))

    def test_changed_reviewer_config_invalidates(self):
        self.assertFalse(ev.is_still_valid(make(), make(reviewer_config_version="rc-2")))

    def test_key_is_stable(self):
        self.assertEqual(make().key(), make().key())

    def test_packet_sha256(self):
        h = ev.packet_sha256(b'{"a":1}\n')
        self.assertEqual(len(h), 64)
        self.assertRegex(h, r"^[0-9a-f]{64}$")

    def test_report_binds_key(self):
        rep = make().to_report("approve", ["ok"])
        self.assertEqual(rep["envelope_key"], make().key())
        self.assertEqual(rep["verdict"], "approve")


if __name__ == "__main__":
    unittest.main(verbosity=2)
