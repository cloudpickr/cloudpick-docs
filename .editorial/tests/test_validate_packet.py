#!/usr/bin/env python3
"""
validate_packet.py 테스트 — 실제 실행(python3 -m pytest 또는 python3 이 파일).

계약(53618d6)의 형식·구조·경로 안전 규칙과 스택 하드닝 케이스를 검증한다.
내용 신뢰(status=verified 진위·출처 실재)는 이 검증기의 책임이 아니므로 테스트하지 않는다.
"""
import copy
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import validate_packet as vp  # noqa: E402

VALID = {
    "schema_version": 1,
    "jira_key": "CLPKDOC-123",
    "policy_action": "update",
    "tier_hint": "B",
    "tier_reasons": ["bounded existing-document update"],
    "target_path": "src/content/docs/ko/compute/serverless.md",
    "changed_paths": [
        "src/content/docs/ko/compute/serverless.md",
        "src/content/docs/en/compute/serverless.md",
        "src/content/docs/ja/compute/serverless.md",
    ],
    "generated_by_llm": True,
    "writer": {"model": "docs-writer", "provider": "resolved-provider"},
    "claim_ledger": [{
        "claim": "assertion",
        "source_url": "https://docs.aws.amazon.com/lambda/latest/dg/welcome.html",
        "quote": "supporting passage",
        "checked_at": "2026-09-10T00:00:00Z",
        "source_updated_at": "2026-09-09",
        "status": "verified",
    }],
}


def to_bytes(obj) -> bytes:
    return (json.dumps(obj) + "\n").encode("utf-8")


class TestValidPacket(unittest.TestCase):
    def test_valid_packet_passes(self):
        vp.validate_packet(to_bytes(VALID))

    def test_valid_with_filename_match(self):
        vp.validate_packet(to_bytes(VALID), Path("CLPKDOC-123.json"))

    def test_legal_multi_sources(self):
        d = copy.deepcopy(VALID)
        d["claim_ledger"][0].pop("source_url")
        d["claim_ledger"][0]["sources"] = [{"source_url": "https://eur-lex.europa.eu/x"}]
        vp.validate_packet(to_bytes(d))


class TestFileParserLevel(unittest.TestCase):
    def test_oversize_rejected(self):
        d = copy.deepcopy(VALID)
        d["tier_reasons"] = ["x" * 200] * 32
        raw = to_bytes(d)
        raw = raw + b" " * (vp.MAX_PACKET_BYTES + 1 - len(raw))
        with self.assertRaises(vp.PacketError):
            vp.validate_packet(raw)

    def test_bom_rejected(self):
        with self.assertRaises(vp.PacketError):
            vp.validate_packet(b"\xef\xbb\xbf" + to_bytes(VALID))

    def test_no_trailing_newline_rejected(self):
        with self.assertRaises(vp.PacketError):
            vp.validate_packet(json.dumps(VALID).encode("utf-8"))

    def test_double_trailing_newline_rejected(self):
        with self.assertRaises(vp.PacketError):
            vp.validate_packet(json.dumps(VALID).encode("utf-8") + b"\n\n")

    def test_duplicate_json_keys_rejected(self):
        raw = b'{"schema_version": 1, "schema_version": 2, "jira_key": "CLPKDOC-1"}\n'
        with self.assertRaises(vp.PacketError):
            vp.validate_packet(raw)

    def test_non_object_root_rejected(self):
        with self.assertRaises(vp.PacketError):
            vp.validate_packet(b"[1,2,3]\n")

    def test_invalid_utf8_rejected(self):
        with self.assertRaises(vp.PacketError):
            vp.validate_packet(b"\xff\xfe not utf8 \n")


class TestPathTraversal(unittest.TestCase):
    def _reject_path(self, path):
        d = copy.deepcopy(VALID)
        d["target_path"] = path
        d["changed_paths"] = [path]
        with self.assertRaises(vp.PacketError):
            vp.validate_packet(to_bytes(d))

    def test_parent_traversal(self):
        self._reject_path("src/content/docs/ko/../../../etc/passwd.md")

    def test_dot_prefix(self):
        self._reject_path("./src/content/docs/ko/x.md")

    def test_mid_dot_segment(self):
        self._reject_path("src/content/docs/ko/./x.md")

    def test_double_slash(self):
        self._reject_path("src/content/docs/ko//x.md")

    def test_backslash(self):
        self._reject_path("src/content/docs/ko/a\\b.md")

    def test_control_char(self):
        self._reject_path("src/content/docs/ko/a\x00b.md")

    def test_outside_docs(self):
        self._reject_path("README.md")

    def test_dotted_dir_ok(self):
        # 오탐 방지: a.b 같은 디렉터리명은 유효해야 한다.
        d = copy.deepcopy(VALID)
        p = "src/content/docs/ko/a.b/x.md"
        d["target_path"] = p
        d["changed_paths"] = [p]
        vp.validate_packet(to_bytes(d))


class TestSemantics(unittest.TestCase):
    def test_target_not_in_changed_rejected(self):
        d = copy.deepcopy(VALID)
        d["target_path"] = "src/content/docs/ko/compute/containers.md"
        with self.assertRaises(vp.PacketError):
            vp.validate_packet(to_bytes(d))

    def test_filename_mismatch_rejected(self):
        with self.assertRaises(vp.PacketError):
            vp.validate_packet(to_bytes(VALID), Path("WRONG-1.json"))

    def test_checked_at_without_tz_rejected(self):
        d = copy.deepcopy(VALID)
        d["claim_ledger"][0]["checked_at"] = "2026-09-10T00:00:00"
        with self.assertRaises(vp.PacketError):
            vp.validate_packet(to_bytes(d))

    def test_checked_at_offset_tz_ok(self):
        d = copy.deepcopy(VALID)
        d["claim_ledger"][0]["checked_at"] = "2026-09-10T00:00:00+09:00"
        vp.validate_packet(to_bytes(d))

    def test_claim_without_source_rejected(self):
        d = copy.deepcopy(VALID)
        d["claim_ledger"][0].pop("source_url")
        with self.assertRaises(vp.PacketError):
            vp.validate_packet(to_bytes(d))

    def test_missing_required_field_rejected(self):
        d = copy.deepcopy(VALID)
        d.pop("jira_key")
        with self.assertRaises(vp.PacketError):
            vp.validate_packet(to_bytes(d))

    def test_bad_enum_rejected(self):
        d = copy.deepcopy(VALID)
        d["tier_hint"] = "D"
        with self.assertRaises(vp.PacketError):
            vp.validate_packet(to_bytes(d))


class TestLimits(unittest.TestCase):
    def test_changed_paths_over_64_rejected(self):
        d = copy.deepcopy(VALID)
        d["changed_paths"] = [f"src/content/docs/ko/f{i}.md" for i in range(65)]
        d["target_path"] = d["changed_paths"][0]
        with self.assertRaises(vp.PacketError):
            vp.validate_packet(to_bytes(d))

    def test_claims_over_32_rejected(self):
        d = copy.deepcopy(VALID)
        d["claim_ledger"] = [VALID["claim_ledger"][0]] * 33
        with self.assertRaises(vp.PacketError):
            vp.validate_packet(to_bytes(d))


if __name__ == "__main__":
    unittest.main(verbosity=2)
