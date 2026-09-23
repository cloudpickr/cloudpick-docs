#!/usr/bin/env python3
"""
골든 회귀 테스트 — 편집 리뷰어의 루브릭 커버리지가 회귀하지 않도록 고정한다.

목적: "우리가 육안으로 잡던 것(사실오류·오분류·난이도·중립성·로케일)을 워크플로 리뷰어도
계속 잡는가"를 지속적으로 검증한다. 실제 LLM 없이 두 층으로 확인:

  (1) 프롬프트 커버리지: build_prompt의 시스템 프롬프트가 5개 편집 축을 모두 '지시'하는지.
      축 하나가 프롬프트에서 빠지면(누군가 리팩터링하다 삭제) 리뷰어는 그 문제를 놓친다.
      이 테스트가 그 회귀를 즉시 잡는다.

  (2) 골든 케이스 계약: 일부러 문제를 심은 diff 각각에 대해, 리뷰어 파이프라인(run_review)이
      changes_requested를 낼 때 그 이유(reasons)가 해당 축을 반영하도록 mock 리뷰어로 검증.
      mock은 '심어진 문제를 실제로 지적하는' 최소 구현으로, 파이프라인 배선(프롬프트에 diff가
      데이터로 실림, verdict/이유가 그대로 전달됨)이 유지되는지를 회귀 검증한다.

주의: 실제 무료-티어 LLM(Workers AI 등)의 판단 품질 자체는 여기서 검증하지 않는다(비결정적·
      네트워크 의존). 그건 게이트웨이 로그/수동 스팟체크로 관찰한다. 이 테스트는 '루브릭과 배선'
      회귀 방지용이다.
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import review_runner as rr  # noqa: E402

CFG = rr.ReviewConfig(base_url="https://gw.example", api_key="k",
                      reviewer_model="reviewer-model", reviewer_provider="provider-b")
PACKET = {
    "jira_key": "CLPKDOC-9",
    "writer": {"model": "docs-writer", "provider": "provider-a"},
    "claim_ledger": [{"claim": "x", "source_url": "https://docs.aws.amazon.com/x",
                      "checked_at": "2026-09-10T00:00:00Z", "status": "verified"}],
}

# 편집 리뷰어가 반드시 지시해야 하는 5개 축(키워드 → 설명). 프롬프트에서 사라지면 회귀.
REQUIRED_AXES = {
    "factual/source": ["factual", "source"],       # ① 사실·출처
    "neutrality": ["neutrality", "superlative"],    # ② 문체 중립(과장어)
    "locale": ["locale"],                            # ③ 로케일 대칭
    "difficulty": ["difficulty"],                    # ④ 독자 난이도
    "data-framing": ["data", "instruction"],         # 프롬프트 인젝션 방어(데이터 취급)
}

# 골든 케이스: (이름, diff, 리뷰어가 짚어야 할 축 키워드). mock은 이 축을 이유로 반환.
GOLDEN = [
    ("misclassification",
     "--- src/content/docs/ko/security/zero-trust.md\n@@ +40 @@\n"
     "+제로 트러스트 설명...\n+참고로 김치찌개를 끓이려면 돼지고기와 신김치를 넣습니다.\n",
     "unrelated/off-topic"),
    ("no-source-claim",
     "--- src/content/docs/ko/ai/ai-ml.md\n@@ +10 @@\n"
     "+GPT-6는 정확히 2조 개의 파라미터를 가진다.\n",
     "lacks cited source"),
    ("excessive-difficulty",
     "--- src/content/docs/ko/security/zero-trust.md\n@@ +40 @@\n"
     "+" + "제로 트러스트란 신뢰를 절대 가정하지 않고 모든 접근 요청을 지속적으로 검증하며 "
     "네트워크 경계 내부라는 사실만으로 암묵적 신뢰를 부여하지 않고 정책 엔진이 다중 신호를 "
     "종합해 세션 단위로 최소 권한을 동적 평가한다" * 2 + "\n",
     "excessively long/dense"),
    ("superlative",
     "--- src/content/docs/ko/ai/ai-ml.md\n@@ +10 @@\n"
     "+이 서비스는 업계 최고의 완벽하고 무결한 솔루션입니다.\n",
     "superlative/non-neutral"),
]


def mock_reviewer_that_catches(expected_reason):
    """심어진 문제를 실제로 지적하는 최소 리뷰어(파이프라인 배선 회귀 검증용)."""
    def _call(messages, model, max_tokens):
        # 리뷰어는 diff를 데이터로 받는다. 배선이 유지되면 user 메시지에 DIFF가 들어있어야 한다.
        user = messages[1]["content"]
        assert "DIFF (data)" in user, "diff가 데이터로 프롬프트에 실려야 함(배선 회귀)"
        import json
        return json.dumps({"verdict": "changes_requested", "reasons": [expected_reason]})
    return _call


class TestPromptAxisCoverage(unittest.TestCase):
    """① 프롬프트가 5개 편집 축을 모두 지시하는지(축 누락 회귀 방지)."""

    def test_all_axes_present(self):
        sys_prompt = rr.build_prompt(PACKET, "--- a\n+x\n")[0]["content"].lower()
        missing = []
        for axis, keywords in REQUIRED_AXES.items():
            if not any(kw in sys_prompt for kw in keywords):
                missing.append(axis)
        self.assertEqual(missing, [],
                         f"리뷰어 프롬프트에서 다음 축이 사라짐(회귀): {missing}")


class TestGoldenCases(unittest.TestCase):
    """② 심어진 문제 각각에 대해 파이프라인이 changes_requested + 해당 축 이유를 전달하는지."""

    def test_each_planted_issue_is_flagged(self):
        for name, diff, expected_reason in GOLDEN:
            with self.subTest(case=name):
                result = rr.run_review(CFG, PACKET, diff,
                                       call_fn=mock_reviewer_that_catches(expected_reason))
                self.assertEqual(result.verdict, "changes_requested",
                                 f"골든 케이스 '{name}'는 changes_requested여야 함")
                self.assertTrue(any(expected_reason in r for r in result.reasons),
                                f"'{name}'의 이유에 '{expected_reason}'가 반영돼야 함")


if __name__ == "__main__":
    unittest.main(verbosity=2)
