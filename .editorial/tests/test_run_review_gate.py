#!/usr/bin/env python3
"""
run_review_gate.py — mock E2E. 패킷 취득/검증/분류/리뷰 통합 동작을 실제로 보인다.

핵심 회귀:
  - 패킷 없음/무효를 A로 낮추지 않는다.
  - 검증된 패킷만 B/C 리뷰 진행. 무효 패킷 첨부 시 A 불가.
  - fail/hold는 success로 마감하지 않는다(exit code·state 정확).
"""
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))
import run_review_gate as g  # noqa: E402
import review_runner as rr   # noqa: E402


VALID_PACKET = {
    "schema_version": 1, "jira_key": "CLPKDOC-123", "policy_action": "update",
    "tier_hint": "B",
    "target_path": "src/content/docs/ko/compute/serverless.md",
    "changed_paths": ["src/content/docs/ko/compute/serverless.md"],
    "generated_by_llm": True,
    "writer": {"model": "docs-writer", "provider": "provider-a"},
    "claim_ledger": [{"claim": "x", "source_url": "https://docs.aws.amazon.com/x",
                      "checked_at": "2026-09-10T00:00:00Z", "status": "verified"}],
}


class Args:
    def __init__(self, **kw):
        self.repo = "cloudpickr/cloudpick-docs"; self.pr = "200"
        self.base_sha = "b" * 40; self.head_sha = "h" * 40
        self.now = "2026-09-10T00:00:00Z"; self.expires = "2026-09-17T00:00:00Z"
        self.numstat = self.name_status = self.diff = self.packet = "none"
        for k, v in kw.items():
            setattr(self, k, v)


def write(tmp, name, content):
    p = Path(tmp) / name
    p.write_text(content, encoding="utf-8")
    return str(p)


class TestGate(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        # 기본: 문서 1개 수정, 작은 변경
        self.numstat = write(self.tmp, "numstat.txt",
                              "3\t2\tsrc/content/docs/ko/compute/serverless.md\n")
        self.name_status = write(self.tmp, "name_status.txt",
                                 "M\tsrc/content/docs/ko/compute/serverless.md\n")
        self.diff = write(self.tmp, "diff.txt", "@@ -1 +1 @@\n-a\n+b\n")

    def _packet_file(self, obj):
        return write(self.tmp, "packet.json", json.dumps(obj) + "\n")

    def test_no_packet_small_human_edit_is_A(self):
        # 패킷 없음 + 작은 사람 편집 → A (하향 아님, 정상 A)
        a = Args(numstat=self.numstat, name_status=self.name_status, diff=self.diff, packet="none")
        out = g.run(a)
        self.assertEqual(out["tier"], "A")
        self.assertEqual(out["state"], "success")

    def test_invalid_packet_not_eligible_for_A(self):
        # 무효 패킷 첨부 → A 불가(changes_requested)
        bad = self._packet_file({"schema_version": 1})  # 필수 필드 누락
        a = Args(numstat=self.numstat, name_status=self.name_status, diff=self.diff, packet=bad)
        out = g.run(a)
        self.assertNotEqual(out["tier"], "A")
        self.assertNotEqual(out["state"], "success")

    def test_BC_without_valid_packet_holds(self):
        # 큰 변경(B/C인데) 패킷 없음 → 보류(비승인)
        numstat = write(self.tmp, "n2.txt", "40\t5\tsrc/content/docs/ko/compute/serverless.md\n")
        a = Args(numstat=numstat, name_status=self.name_status, diff=self.diff, packet="none")
        out = g.run(a)
        self.assertEqual(out["state"], "pending")  # hold, 비승인
        self.assertNotEqual(out["state"], "success")

    def test_BC_valid_packet_approve(self):
        # 유효 패킷 + LLM approve (writer-distinct 설정 주입) → success
        os.environ["LITELLM_BASE_URL"] = "https://litellm.internal"
        os.environ["LITELLM_API_KEY"] = "k"
        os.environ["LITELLM_REVIEWER_MODEL"] = "reviewer-model"
        os.environ["LITELLM_REVIEWER_PROVIDER"] = "provider-b"
        try:
            # review_runner의 실제 호출을 mock으로 대체
            orig = rr.run_review
            rr.run_review = lambda cfg, pkt, diff, **k: rr.ReviewResult("approve", ["ok"], 1, True)
            numstat = write(self.tmp, "n3.txt", "40\t5\tsrc/content/docs/ko/compute/serverless.md\n")
            pkt = self._packet_file(VALID_PACKET)
            a = Args(numstat=numstat, name_status=self.name_status, diff=self.diff, packet=pkt)
            out = g.run(a)
            self.assertEqual(out["state"], "success")
            self.assertEqual(out["verdict"], "approve")
            self.assertRegex(out["envelope_key"], r"^[0-9a-f]{64}$")
        finally:
            rr.run_review = orig
            for k in ("LITELLM_BASE_URL", "LITELLM_API_KEY", "LITELLM_REVIEWER_MODEL", "LITELLM_REVIEWER_PROVIDER"):
                os.environ.pop(k, None)

    def test_BC_valid_packet_unconfigured_llm_holds(self):
        # 유효 패킷이나 LLM 미설정 → skipped-unconfigured → pending(비승인, A아님)
        pkt = self._packet_file(VALID_PACKET)
        numstat = write(self.tmp, "n4.txt", "40\t5\tsrc/content/docs/ko/compute/serverless.md\n")
        a = Args(numstat=numstat, name_status=self.name_status, diff=self.diff, packet=pkt)
        out = g.run(a)
        self.assertEqual(out["state"], "pending")
        self.assertNotEqual(out["state"], "success")

    def test_structural_new_file_is_C(self):
        numstat = write(self.tmp, "n5.txt", "10\t0\tsrc/content/docs/ko/compute/new.md\n")
        name_status = write(self.tmp, "ns5.txt", "A\tsrc/content/docs/ko/compute/new.md\n")
        a = Args(numstat=numstat, name_status=name_status, diff=self.diff, packet="none")
        out = g.run(a)
        self.assertEqual(out["tier"], "C")
        self.assertNotEqual(out["state"], "success")


if __name__ == "__main__":
    unittest.main(verbosity=2)
