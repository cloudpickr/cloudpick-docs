#!/usr/bin/env python3
"""
classify_change.py 테스트 — 실제 실행.

계약(53618d6) §Risk tiers의 A/B/C 판정과 '조용한 하향 금지·불명확은 상향' 원칙 검증.
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import classify_change as cc  # noqa: E402

FC = cc.FileChange
DOC = "src/content/docs"


def mod(path, added=1, deleted=1):
    return FC(path, "M", added, deleted)


class TestTierC(unittest.TestCase):
    def test_new_file_is_C(self):
        r = cc.classify([FC(f"{DOC}/ko/compute/new.md", "A", 10, 0)], None)
        self.assertEqual(r.tier, "C")

    def test_deleted_file_is_C(self):
        r = cc.classify([FC(f"{DOC}/ko/compute/old.md", "D", 0, 30)], None)
        self.assertEqual(r.tier, "C")

    def test_renamed_file_is_C(self):
        r = cc.classify([FC(f"{DOC}/ko/compute/b.md", "R", 0, 0, old_path=f"{DOC}/ko/compute/a.md")], None)
        self.assertEqual(r.tier, "C")

    def test_non_document_change_is_C(self):
        r = cc.classify([FC("astro.config.mjs", "M", 3, 1)], None)
        self.assertEqual(r.tier, "C")

    def test_regulatory_claim_is_C(self):
        r = cc.classify([mod(f"{DOC}/ko/compute/x.md")], {"claim_ledger": [{}]},
                        has_regulatory_claim=True)
        self.assertEqual(r.tier, "C")

    def test_human_hold_is_C(self):
        r = cc.classify([mod(f"{DOC}/ko/compute/x.md")], None, human_hold=True)
        self.assertEqual(r.tier, "C")

    def test_unknown_scope_is_C(self):
        r = cc.classify([mod(f"{DOC}/ko/compute/x.md")], None, scope_unknown=True)
        self.assertEqual(r.tier, "C")


class TestTierB(unittest.TestCase):
    def test_llm_generated_factual_is_B(self):
        changes = [mod(f"{DOC}/ko/compute/x.md", 3, 2),
                   mod(f"{DOC}/en/compute/x.md", 3, 2),
                   mod(f"{DOC}/ja/compute/x.md", 3, 2)]
        r = cc.classify(changes, {"generated_by_llm": True, "claim_ledger": [{"claim": "x"}]})
        self.assertEqual(r.tier, "B")

    def test_large_edit_with_evidence_is_B(self):
        changes = [mod(f"{DOC}/ko/compute/x.md", 40, 10)]
        r = cc.classify(changes, {"claim_ledger": [{"claim": "x"}]})
        self.assertEqual(r.tier, "B")


class TestTierA(unittest.TestCase):
    def test_small_mechanical_human_is_A(self):
        # 사람 작성(generated_by_llm 없음), 근거 없음, 합산 <=20, 기계적
        changes = [mod(f"{DOC}/ko/compute/x.md", 2, 2),
                   mod(f"{DOC}/en/compute/x.md", 2, 2),
                   mod(f"{DOC}/ja/compute/x.md", 2, 2)]  # 합산 12
        r = cc.classify(changes, {"generated_by_llm": False})
        self.assertEqual(r.tier, "A")


class TestEscalation(unittest.TestCase):
    def test_non_mechanical_without_evidence_escalates_to_C(self):
        # 21줄 초과이지만 근거 패킷 claim 없음 → 조용한 B 하향 대신 C로 상향
        changes = [mod(f"{DOC}/ko/compute/x.md", 30, 5)]
        r = cc.classify(changes, {"generated_by_llm": False})
        self.assertEqual(r.tier, "C")
        self.assertEqual(r.escalated_from, "B")

    def test_country_path_not_auto_C_but_not_A(self):
        # 국가 경로의 작은 기계적 변경: 자동 C는 아니지만 A 자격 제외 → 근거 없으면 C escalate
        changes = [mod(f"{DOC}/ko/korea/security/csap.md", 2, 1)]
        r = cc.classify(changes, {"generated_by_llm": False})
        self.assertIn(r.tier, ("B", "C"))  # A는 아님
        self.assertNotEqual(r.tier, "A")

    def test_country_path_with_evidence_is_B(self):
        changes = [mod(f"{DOC}/ko/korea/security/csap.md", 5, 2)]
        r = cc.classify(changes, {"claim_ledger": [{"claim": "x"}]})
        self.assertEqual(r.tier, "B")


class TestHintNotTrusted(unittest.TestCase):
    def test_tier_hint_A_does_not_downgrade_structural(self):
        # 패킷이 A를 주장해도 실제 신규 파일이면 C
        r = cc.classify([FC(f"{DOC}/ko/x.md", "A", 1, 0)],
                        {"tier_hint": "A"})
        self.assertEqual(r.tier, "C")

    def test_tier_hint_A_does_not_downgrade_llm(self):
        # 패킷이 A 주장 + generated_by_llm=true → 최소 B
        changes = [mod(f"{DOC}/ko/x.md", 2, 1)]
        r = cc.classify(changes, {"tier_hint": "A", "generated_by_llm": True,
                                  "claim_ledger": [{"claim": "x"}]})
        self.assertEqual(r.tier, "B")


class TestDiffParsing(unittest.TestCase):
    def test_parse_numstat_and_status(self):
        numstat = "3\t2\tsrc/content/docs/ko/x.md\n5\t0\tsrc/content/docs/en/x.md\n"
        name_status = "M\tsrc/content/docs/ko/x.md\nM\tsrc/content/docs/en/x.md\n"
        changes = cc.parse_numstat_and_status(numstat, name_status)
        self.assertEqual(len(changes), 2)
        self.assertEqual(cc._total_lines(changes), 10)

    def test_parse_rename(self):
        numstat = "0\t0\tsrc/content/docs/ko/b.md\n"
        name_status = "R100\tsrc/content/docs/ko/a.md\tsrc/content/docs/ko/b.md\n"
        changes = cc.parse_numstat_and_status(numstat, name_status)
        self.assertEqual(changes[0].status, "R")
        self.assertEqual(changes[0].old_path, "src/content/docs/ko/a.md")


if __name__ == "__main__":
    unittest.main(verbosity=2)
