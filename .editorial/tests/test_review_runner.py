#!/usr/bin/env python3
"""
review_runner.py 테스트 — 실제 네트워크 없이 call_fn mock 주입.

계약(3113cfc) §Review 원칙 검증:
  - writer-distinct 강제, outage/unknown은 pass로 변환 금지, 미설정=shadow(non-pass),
    성공만 캐시 가능, 예산 상한.
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import review_runner as rr  # noqa: E402

PACKET = {
    "jira_key": "CLPKDOC-1",
    "writer": {"model": "docs-writer", "provider": "provider-a"},
    "claim_ledger": [{"claim": "x", "source_url": "https://docs.aws.amazon.com/x",
                      "checked_at": "2026-09-10T00:00:00Z", "status": "verified"}],
}
DIFF = "--- a/x.md\n+++ b/x.md\n@@ -1 +1 @@\n-old\n+new\n"


def cfg(model="reviewer-model", provider="provider-b", base="https://litellm.internal",
        key="k"):
    return rr.ReviewConfig(base_url=base, api_key=key, reviewer_model=model,
                           reviewer_provider=provider)


class TestConfig(unittest.TestCase):
    def test_unconfigured_is_shadow_non_pass(self):
        c = rr.ReviewConfig(None, None, None, None)
        r = rr.run_review(c, PACKET, DIFF)
        self.assertEqual(r.verdict, "skipped-unconfigured")
        self.assertFalse(r.cacheable)

    def test_partial_config_is_shadow(self):
        c = rr.ReviewConfig(base_url="https://x", api_key=None, reviewer_model="m",
                            reviewer_provider=None)
        self.assertFalse(c.is_configured())


class TestWriterDistinct(unittest.TestCase):
    def test_same_model_rejected(self):
        c = cfg(model="docs-writer")  # writer와 동일
        r = rr.run_review(c, PACKET, DIFF, call_fn=lambda *a, **k: '{"verdict":"approve"}')
        self.assertEqual(r.verdict, "error")
        self.assertFalse(r.cacheable)

    def test_distinct_model_ok(self):
        c = cfg(model="reviewer-model")
        r = rr.run_review(c, PACKET, DIFF, call_fn=lambda *a, **k: '{"verdict":"approve","reasons":[]}')
        self.assertEqual(r.verdict, "approve")


class TestVerdicts(unittest.TestCase):
    def test_approve(self):
        r = rr.run_review(cfg(), PACKET, DIFF,
                          call_fn=lambda *a, **k: '{"verdict":"approve","reasons":["ok"]}')
        self.assertEqual(r.verdict, "approve")
        self.assertTrue(r.cacheable)

    def test_changes_requested(self):
        r = rr.run_review(cfg(), PACKET, DIFF,
                          call_fn=lambda *a, **k: '{"verdict":"changes_requested","reasons":["fix"]}')
        self.assertEqual(r.verdict, "changes_requested")
        self.assertTrue(r.cacheable)

    def test_unknown_verdict_is_error(self):
        r = rr.run_review(cfg(), PACKET, DIFF,
                          call_fn=lambda *a, **k: '{"verdict":"maybe"}')
        self.assertEqual(r.verdict, "error")
        self.assertFalse(r.cacheable)


class TestOutageNotApproval(unittest.TestCase):
    def test_exception_is_error_not_pass(self):
        def boom(*a, **k):
            raise TimeoutError("litellm down")
        r = rr.run_review(cfg(), PACKET, DIFF, call_fn=boom)
        self.assertEqual(r.verdict, "error")
        self.assertFalse(r.cacheable)

    def test_unparseable_then_repair_fails_is_error(self):
        calls = {"n": 0}
        def junk(*a, **k):
            calls["n"] += 1
            return "not json at all"
        r = rr.run_review(cfg(), PACKET, DIFF, call_fn=junk)
        self.assertEqual(r.verdict, "error")
        self.assertFalse(r.cacheable)
        # repair round 포함 최대 MAX_REPAIR_ROUNDS+1회
        self.assertLessEqual(calls["n"], rr.MAX_REPAIR_ROUNDS + 1)


class TestBudget(unittest.TestCase):
    def test_input_over_budget_is_error(self):
        big_diff = "x" * (rr.MAX_INPUT_TOKENS * 4 + 100)
        r = rr.run_review(cfg(), PACKET, big_diff, call_fn=lambda *a, **k: '{"verdict":"approve"}')
        self.assertEqual(r.verdict, "error")
        self.assertFalse(r.cacheable)


class TestPromptDataFraming(unittest.TestCase):
    def test_prompt_marks_content_as_data(self):
        msgs = rr.build_prompt(PACKET, DIFF)
        self.assertEqual(msgs[0]["role"], "system")
        self.assertIn("DATA", msgs[0]["content"])
        self.assertIn("ignore", msgs[0]["content"].lower())
        # PR 콘텐츠는 user 메시지에 데이터로만
        self.assertIn("DIFF (data)", msgs[1]["content"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
