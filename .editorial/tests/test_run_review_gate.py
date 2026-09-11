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
        self.packet_repo_path = ""
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
        os.environ["AI_GATEWAY_BASE_URL"] = "https://gateway.example"
        os.environ["AI_GATEWAY_TOKEN"] = "k"
        os.environ["REVIEWER_MODEL"] = "reviewer-model"
        os.environ["REVIEWER_PROVIDER"] = "provider-b"
        orig = rr.run_review
        orig_fetch = g._fetch_sources
        try:
            # review_runner·source fetch를 mock (SSRF 실호출 없이 통합 경로 검증)
            rr.run_review = lambda cfg, pkt, diff, **k: rr.ReviewResult("approve", ["ok"], 1, True)
            g._fetch_sources = lambda pkt: ({"https://docs.aws.amazon.com/x": {"status": 200}}, [])
            numstat = write(self.tmp, "n3.txt", "40\t5\tsrc/content/docs/ko/compute/serverless.md\n")
            pkt = self._packet_file(VALID_PACKET)
            a = Args(numstat=numstat, name_status=self.name_status, diff=self.diff, packet=pkt,
                     packet_repo_path=".editorial/packets/CLPKDOC-123.json")
            out = g.run(a)
            self.assertEqual(out["state"], "success")
            self.assertEqual(out["verdict"], "approve")
            self.assertRegex(out["envelope_key"], r"^[0-9a-f]{64}$")
        finally:
            rr.run_review = orig
            g._fetch_sources = orig_fetch
            for k in ("AI_GATEWAY_BASE_URL", "AI_GATEWAY_TOKEN", "REVIEWER_MODEL", "REVIEWER_PROVIDER"):
                os.environ.pop(k, None)

    def test_BC_valid_packet_unconfigured_llm_holds(self):
        # 유효 패킷이나 LLM 미설정 → skipped-unconfigured → pending(비승인, A아님)
        orig_fetch = g._fetch_sources
        try:
            g._fetch_sources = lambda pkt: ({}, [])  # 출처 fetch는 통과
            pkt = self._packet_file(VALID_PACKET)
            numstat = write(self.tmp, "n4.txt", "40\t5\tsrc/content/docs/ko/compute/serverless.md\n")
            a = Args(numstat=numstat, name_status=self.name_status, diff=self.diff, packet=pkt,
                     packet_repo_path=".editorial/packets/CLPKDOC-123.json")
            out = g.run(a)
            self.assertEqual(out["state"], "pending")
            self.assertNotEqual(out["state"], "success")
        finally:
            g._fetch_sources = orig_fetch

    def test_structural_new_file_is_C(self):
        numstat = write(self.tmp, "n5.txt", "10\t0\tsrc/content/docs/ko/compute/new.md\n")
        name_status = write(self.tmp, "ns5.txt", "A\tsrc/content/docs/ko/compute/new.md\n")
        a = Args(numstat=numstat, name_status=name_status, diff=self.diff, packet="none")
        out = g.run(a)
        self.assertEqual(out["tier"], "C")
        self.assertNotEqual(out["state"], "success")

    # ── AGY BLOCKER 회귀 테스트 ──────────────────────────────────────────
    def test_blocker1_packet_new_file_does_not_force_C(self):
        # #1: 패킷 신규파일(.editorial/packets/*.json 추가 A)이 있어도, 검증된 패킷은
        #     scope 예외라 B 문서변경이 C로 강등되지 않는다.
        os.environ["AI_GATEWAY_BASE_URL"] = "https://gateway.example"
        os.environ["AI_GATEWAY_TOKEN"] = "k"
        os.environ["REVIEWER_MODEL"] = "reviewer-model"
        os.environ["REVIEWER_PROVIDER"] = "provider-b"
        orig, orig_fetch = rr.run_review, g._fetch_sources
        try:
            rr.run_review = lambda cfg, pkt, diff, **k: rr.ReviewResult("approve", ["ok"], 1, True)
            g._fetch_sources = lambda pkt: ({}, [])
            # 문서 수정(M, B급 40줄) + 패킷 신규파일(A) 함께 변경
            numstat = write(self.tmp, "n6.txt",
                            "40\t5\tsrc/content/docs/ko/compute/serverless.md\n"
                            "12\t0\t.editorial/packets/CLPKDOC-123.json\n")
            name_status = write(self.tmp, "ns6.txt",
                                "M\tsrc/content/docs/ko/compute/serverless.md\n"
                                "A\t.editorial/packets/CLPKDOC-123.json\n")
            pkt = self._packet_file(VALID_PACKET)
            a = Args(numstat=numstat, name_status=name_status, diff=self.diff, packet=pkt,
                     packet_repo_path=".editorial/packets/CLPKDOC-123.json")
            out = g.run(a)
            # 패킷 신규파일 때문에 C가 되면 안 됨 → B로 판정되어 리뷰 approve → success
            self.assertEqual(out["tier"], "B")
            self.assertEqual(out["state"], "success")
        finally:
            rr.run_review = orig; g._fetch_sources = orig_fetch
            for k in ("AI_GATEWAY_BASE_URL", "AI_GATEWAY_TOKEN", "REVIEWER_MODEL", "REVIEWER_PROVIDER"):
                os.environ.pop(k, None)

    def test_blocker2_source_fetch_block_is_non_pass(self):
        # #2: 독립 출처 fetch가 SSRF 차단/실패면 리뷰 진행 전 non-pass(hold).
        os.environ["AI_GATEWAY_BASE_URL"] = "https://gateway.example"
        os.environ["AI_GATEWAY_TOKEN"] = "k"
        os.environ["REVIEWER_MODEL"] = "reviewer-model"
        os.environ["REVIEWER_PROVIDER"] = "provider-b"
        orig, orig_fetch = rr.run_review, g._fetch_sources
        try:
            # 리뷰가 approve해도, fetch가 None(차단)이면 리뷰까지 안 가고 hold여야 함
            rr.run_review = lambda cfg, pkt, diff, **k: rr.ReviewResult("approve", ["ok"], 1, True)
            g._fetch_sources = lambda pkt: (None, ["source fetch blocked: SSRF"])
            numstat = write(self.tmp, "n7.txt", "40\t5\tsrc/content/docs/ko/compute/serverless.md\n")
            pkt = self._packet_file(VALID_PACKET)
            a = Args(numstat=numstat, name_status=self.name_status, diff=self.diff, packet=pkt,
                     packet_repo_path=".editorial/packets/CLPKDOC-123.json")
            out = g.run(a)
            self.assertNotEqual(out["state"], "success")
            self.assertTrue(any("source fetch" in r for r in out["reasons"]))
        finally:
            rr.run_review = orig; g._fetch_sources = orig_fetch
            for k in ("AI_GATEWAY_BASE_URL", "AI_GATEWAY_TOKEN", "REVIEWER_MODEL", "REVIEWER_PROVIDER"):
                os.environ.pop(k, None)

    def test_blocker3_filename_mismatch_rejected(self):
        # #3: 실제 저장소 경로(파일명)와 packet의 jira_key가 불일치하면 검증 실패 → 승인 아님.
        pkt = self._packet_file(VALID_PACKET)  # jira_key=CLPKDOC-123
        numstat = write(self.tmp, "n8.txt", "3\t2\tsrc/content/docs/ko/compute/serverless.md\n")
        # 실제 경로를 다른 이름으로 넘김(위조 시나리오)
        a = Args(numstat=numstat, name_status=self.name_status, diff=self.diff, packet=pkt,
                 packet_repo_path=".editorial/packets/WRONG-999.json")
        out = g.run(a)
        self.assertNotEqual(out["state"], "success")
        self.assertTrue(any("packet invalid" in r or "filename" in r for r in out["reasons"]))

    def test_blocker3_missing_repo_path_rejected(self):
        # #3: 실제 경로 미제공이면 파일명 검증 불가 → 유효 처리 안 함.
        pkt = self._packet_file(VALID_PACKET)
        numstat = write(self.tmp, "n9.txt", "3\t2\tsrc/content/docs/ko/compute/serverless.md\n")
        a = Args(numstat=numstat, name_status=self.name_status, diff=self.diff, packet=pkt,
                 packet_repo_path="")
        out = g.run(a)
        self.assertNotEqual(out["state"], "success")

    # ── 계약 §5 feature-only 회귀 ────────────────────────────────────────
    def test_feature_only_pr_is_out_of_scope_pass(self):
        # 문서 미변경(.github/**만) + 패킷 없음 → feature-only, 편집 C scope 밖 → 명시 통과.
        numstat = write(self.tmp, "nf.txt", "5\t2\t.github/workflows/x.yml\n"
                                            "3\t0\t.editorial/README.md\n")
        name_status = write(self.tmp, "nsf.txt", "M\t.github/workflows/x.yml\n"
                                                 "M\t.editorial/README.md\n")
        a = Args(numstat=numstat, name_status=name_status, diff=self.diff, packet="none")
        out = g.run(a)
        self.assertEqual(out["tier"], "feature-only")
        self.assertEqual(out["state"], "success")

    def test_feature_only_not_applied_when_packet_attached(self):
        # 문서 미변경이라도 패킷이 첨부되면 정규 검증 경로(유효 패킷 없으면 비승인).
        pkt = self._packet_file({"schema_version": 1})  # 무효 패킷
        numstat = write(self.tmp, "nf2.txt", "5\t2\t.github/workflows/x.yml\n")
        name_status = write(self.tmp, "nsf2.txt", "M\t.github/workflows/x.yml\n")
        a = Args(numstat=numstat, name_status=name_status, diff=self.diff, packet=pkt,
                 packet_repo_path=".editorial/packets/CLPKDOC-123.json")
        out = g.run(a)
        self.assertNotEqual(out["tier"], "feature-only")
        self.assertNotEqual(out["state"], "success")


if __name__ == "__main__":
    unittest.main(verbosity=2)
