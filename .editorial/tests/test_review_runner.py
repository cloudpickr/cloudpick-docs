#!/usr/bin/env python3
"""
review_runner.py 테스트 — 실제 네트워크 없이 call_fn mock 주입.

계약(53618d6) §Review 원칙 검증:
  - writer-distinct 강제, outage/unknown은 pass로 변환 금지, 미설정=shadow(non-pass),
    성공만 캐시 가능, 예산 상한.
"""
import sys
import os
import json
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import review_runner as rr  # noqa: E402

PACKET = {
    "jira_key": "CLPKDOC-1",
    "writer": {"model": "claude-opus", "provider": "anthropic"},
    "claim_ledger": [{"claim": "x", "source_url": "https://docs.aws.amazon.com/x",
                      "checked_at": "2026-09-10T00:00:00Z", "status": "verified"}],
}
DIFF = "--- a/x.md\n+++ b/x.md\n@@ -1 +1 @@\n-old\n+new\n"


def cfg(model="llama-3.3-70b", provider="workers-ai", base="https://gateway.example",
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
        c = cfg(model="claude-opus", provider="workers-ai")  # writer와 동일 model
        r = rr.run_review(c, PACKET, DIFF, call_fn=lambda *a, **k: '{"verdict":"approve"}')
        self.assertEqual(r.verdict, "error")
        self.assertFalse(r.cacheable)

    def test_same_provider_rejected(self):
        # 다른 model이지만 같은 provider → 독립 아님
        c = cfg(model="claude-sonnet", provider="anthropic")  # writer provider와 동일
        r = rr.run_review(c, PACKET, DIFF, call_fn=lambda *a, **k: '{"verdict":"approve"}')
        self.assertEqual(r.verdict, "error")
        self.assertFalse(r.cacheable)

    def test_same_vendor_alias_rejected(self):
        # provider 문자열은 다르지만(hf-inference) 실제 벤더가 anthropic → 별칭 우회 차단.
        c = cfg(model="claude-3.5", provider="hf-inference")
        r = rr.run_review(c, PACKET, DIFF, call_fn=lambda *a, **k: '{"verdict":"approve"}')
        self.assertEqual(r.verdict, "error")
        joined = " ".join(r.reasons).lower()
        self.assertIn("vendor", joined)

    def test_missing_reviewer_provider_rejected(self):
        c = rr.ReviewConfig(base_url="https://x", api_key="k",
                            reviewer_model="llama-3.3-70b", reviewer_provider=None)
        r = rr.run_review(c, PACKET, DIFF, call_fn=lambda *a, **k: '{"verdict":"approve"}')
        self.assertEqual(r.verdict, "error")

    def test_missing_writer_in_packet_rejected(self):
        # writer 신고가 없으면 독립성 확인 불가 → 보류(error, 비승인)
        packet_no_writer = {k: v for k, v in PACKET.items() if k != "writer"}
        r = rr.run_review(cfg(), packet_no_writer, DIFF,
                          call_fn=lambda *a, **k: '{"verdict":"approve","reasons":[]}')
        self.assertEqual(r.verdict, "error")
        self.assertFalse(r.cacheable)

    def test_distinct_model_and_provider_ok(self):
        c = cfg(model="llama-3.3-70b", provider="workers-ai")  # meta/cloudflare vs anthropic
        r = rr.run_review(c, PACKET, DIFF, call_fn=lambda *a, **k: '{"verdict":"approve","reasons":[]}')
        self.assertEqual(r.verdict, "approve")

    def test_writer_vendor_field_takes_precedence(self):
        # writer가 명시적 vendor를 신고하면 그것으로 정규화(문자열 추론 실패 회피).
        packet = {**PACKET, "writer": {"model": "custom-x", "provider": "self-hosted",
                                       "vendor": "anthropic"}}
        c = cfg(model="claude-opus", provider="workers-ai")  # reviewer vendor=anthropic
        r = rr.run_review(c, packet, DIFF, call_fn=lambda *a, **k: '{"verdict":"approve"}')
        self.assertEqual(r.verdict, "error")  # vendor 충돌(anthropic==anthropic)


class TestNormalizeVendor(unittest.TestCase):
    def test_basic_vendors(self):
        self.assertEqual(rr.normalize_vendor("claude-opus", "anthropic"), "anthropic")
        self.assertEqual(rr.normalize_vendor("gpt-6", "openai"), "openai")
        self.assertEqual(rr.normalize_vendor("gemini-3", "google"), "google")

    def test_hosting_provider_defers_to_real_model(self):
        # workers-ai/huggingface(호스팅) + 실제 모델 벤더 → 실제 벤더 우선.
        self.assertEqual(rr.normalize_vendor("llama-3.3-70b", "workers-ai"), "meta")
        self.assertEqual(rr.normalize_vendor("claude-3.5", "hf-inference"), "anthropic")

    def test_hosting_only_returns_hosting(self):
        # 실제 모델 벤더를 특정 못하고 호스팅만 있으면 그 호스팅 벤더.
        self.assertEqual(rr.normalize_vendor("some-model", "workers-ai"), "cloudflare")

    def test_unknown_returns_none(self):
        self.assertIsNone(rr.normalize_vendor("mystery", "provider-x"))
        self.assertIsNone(rr.normalize_vendor("", ""))


class TestReviewerPool(unittest.TestCase):
    def _pool_cfg(self, pool, base="https://gw", key="k"):
        return rr.ReviewConfig(base_url=base, api_key=key, reviewer_model=None,
                               reviewer_provider=None, reviewer_pool=pool)

    def test_pool_selects_first_distinct(self):
        # 첫 후보가 writer와 vendor 충돌(anthropic), 둘째가 독립(workers-ai/meta) → 둘째 선택.
        pool = [{"model": "claude-opus", "provider": "anthropic"},
                {"model": "llama-3.3-70b", "provider": "workers-ai"}]
        r = rr.run_review(self._pool_cfg(pool), PACKET, DIFF,
                          call_fn=lambda *a, **k: '{"verdict":"approve","reasons":[]}')
        self.assertEqual(r.verdict, "approve")
        self.assertEqual(r.selected_model, "llama-3.3-70b")

    def test_pool_all_conflict_is_error(self):
        # pool 전량이 writer(anthropic)와 충돌 → error, 전용 사유코드.
        pool = [{"model": "claude-opus", "provider": "anthropic"},
                {"model": "claude-3.5", "provider": "hf-inference"}]  # 둘 다 anthropic vendor
        r = rr.run_review(self._pool_cfg(pool), PACKET, DIFF,
                          call_fn=lambda *a, **k: '{"verdict":"approve"}')
        self.assertEqual(r.verdict, "error")
        self.assertIn("pool-all-conflict", " ".join(r.reasons))

    def test_pool_selection_deterministic(self):
        # 같은 pool·writer면 항상 같은 후보(배열 순서=우선순위).
        pool = [{"model": "llama-3.3-70b", "provider": "workers-ai"},
                {"model": "gemini-3", "provider": "google"}]
        for _ in range(3):
            sel, _why = rr.select_reviewer(self._pool_cfg(pool), PACKET)
            self.assertEqual(sel["model"], "llama-3.3-70b")

    def test_pool_config_error_is_shadow(self):
        # REVIEWER_POOL JSON 파싱 실패 → 단일로 조용히 되돌아가지 않고 fail-closed.
        c = rr.ReviewConfig.from_env({"AI_GATEWAY_BASE_URL": "https://gw",
                                      "AI_GATEWAY_TOKEN": "k",
                                      "REVIEWER_POOL": "{not a list}"})
        self.assertIsNotNone(c.pool_error)
        self.assertFalse(c.is_configured())
        r = rr.run_review(c, PACKET, DIFF, call_fn=lambda *a, **k: '{"verdict":"approve"}')
        self.assertEqual(r.verdict, "skipped-unconfigured")

    def test_backward_compat_single_reviewer(self):
        # pool 미설정 + 단일 REVIEWER_MODEL/PROVIDER → 기존 동작 유지.
        c = rr.ReviewConfig.from_env({"AI_GATEWAY_BASE_URL": "https://gw",
                                      "AI_GATEWAY_TOKEN": "k",
                                      "REVIEWER_MODEL": "llama-3.3-70b",
                                      "REVIEWER_PROVIDER": "workers-ai"})
        self.assertIsNone(c.reviewer_pool)
        self.assertTrue(c.is_configured())
        r = rr.run_review(c, PACKET, DIFF,
                          call_fn=lambda *a, **k: '{"verdict":"approve","reasons":[]}')
        self.assertEqual(r.verdict, "approve")
        self.assertEqual(r.selected_model, "llama-3.3-70b")


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
            raise TimeoutError("gateway down")
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
    def test_oversized_diff_truncated_blocks_approve(self):
        # 변경분 압축(condense_diff)으로 큰 diff도 예산 내로 줄이되, 절단이 발생하면
        # LLM이 approve해도 fail-closed로 changes_requested로 강제된다(자동 머지 우회 차단).
        big_diff = "--- big.md\n" + ("+x\n" * 30_000)  # 파일당 상한 초과 → 절단 발생
        r = rr.run_review(cfg(), PACKET, big_diff, call_fn=lambda *a, **k: '{"verdict":"approve"}')
        self.assertEqual(r.verdict, "changes_requested")
        self.assertFalse(r.cacheable)
        self.assertTrue(any("truncat" in x.lower() or "budget" in x.lower() for x in r.reasons))

    def test_within_budget_diff_can_approve(self):
        # 절단이 없으면 정상적으로 approve가 유지된다(정상 크기 회귀 방지).
        small_diff = "--- a.md\n@@ -1 +1 @@\n-old\n+new\n"
        r = rr.run_review(cfg(), PACKET, small_diff, call_fn=lambda *a, **k: '{"verdict":"approve"}')
        self.assertEqual(r.verdict, "approve")


class TestCondenseDiff(unittest.TestCase):
    def test_small_diff_unchanged(self):
        d = "--- a.md\n@@ -1 +1 @@\n-old\n+new\n"
        out, truncated = rr.condense_diff(d)
        self.assertEqual(out, d)
        self.assertFalse(truncated)

    def test_total_cap_truncates_and_marks(self):
        # 여러 파일로 전체 상한을 넘기면 뒷부분 파일은 생략하고 마커 + truncated=True.
        seg = "--- f{n}.md\n" + ("+line\n" * 200)
        many = "\n".join(seg.replace("{n}", str(i)) for i in range(50))
        out, truncated = rr.condense_diff(many, max_total=5_000, max_per_file=1_000)
        self.assertTrue(truncated)
        self.assertLessEqual(len(out), 5_400)  # 상한 + 라인경계/마커 여유
        self.assertIn("truncated", out)

    def test_per_file_cap_truncates_each(self):
        one_big = "--- big.md\n" + ("+x\n" * 5_000)
        out, truncated = rr.condense_diff(one_big, max_total=1_000_000, max_per_file=2_000)
        self.assertTrue(truncated)
        self.assertLessEqual(len(out), 2_200)
        self.assertIn("per-file limit", out)

    def test_cut_on_line_boundary(self):
        # 라인 경계에서 절단(라인 중간 절단 금지).
        one_big = "--- big.md\n" + ("+abcdefghij\n" * 500)  # 각 줄 12자
        out, truncated = rr.condense_diff(one_big, max_total=1_000_000, max_per_file=300)
        self.assertTrue(truncated)
        body = out.split("… [truncated")[0]
        # 마커 앞 본문은 완전한 줄로 끝나야 함(줄 중간 절단 아님)
        self.assertTrue(body.endswith("\n") or body.endswith("+abcdefghij"))


class TestPromptDataFraming(unittest.TestCase):
    def test_prompt_marks_content_as_data(self):
        msgs = rr.build_prompt(PACKET, DIFF)
        self.assertEqual(msgs[0]["role"], "system")
        self.assertIn("DATA", msgs[0]["content"])
        self.assertIn("ignore", msgs[0]["content"].lower())
        # PR 콘텐츠는 user 메시지에 데이터로만
        self.assertIn("DIFF (data)", msgs[1]["content"])

    def test_prompt_includes_reader_difficulty_axis(self):        # 루브릭 4번째 축: 독자 난이도(초장문/고밀도 문단)를 검사하도록 지시가 있어야 한다.
        # 이 축이 빠지면 워크플로가 '너무 어렵게 쓰인 문서'를 놓친다(실측 갭 회귀 방지).
        sys_prompt = rr.build_prompt(PACKET, DIFF)[0]["content"].lower()
        self.assertIn("difficulty", sys_prompt)
        self.assertTrue(
            "excessively long" in sys_prompt or "dense" in sys_prompt,
            "reader-difficulty axis must describe long/dense paragraphs",
        )


class TestGatewayErrorClassification(unittest.TestCase):
    """게이트웨이 에러 분류 — verdict는 error 유지하되 원인/조치를 reasons에 노출."""

    def test_auth_error_classified(self):
        import urllib.error
        def boom(*a, **k):
            raise urllib.error.HTTPError("u", 401, "unauthorized", {}, None)
        r = rr.run_review(cfg(), PACKET, DIFF, call_fn=boom)
        self.assertEqual(r.verdict, "error")           # fail-closed 유지
        self.assertFalse(r.cacheable)
        joined = " ".join(r.reasons).lower()
        self.assertIn("auth", joined)
        self.assertIn("token", joined)                  # 토큰 교체 힌트

    def test_unreachable_error_classified(self):
        import urllib.error
        def boom(*a, **k):
            raise urllib.error.URLError("dns fail")
        r = rr.run_review(cfg(), PACKET, DIFF, call_fn=boom)
        self.assertEqual(r.verdict, "error")
        joined = " ".join(r.reasons).lower()
        self.assertIn("unreachable", joined)
        self.assertIn("--admin", " ".join(r.reasons))   # 장애 시 우회 가능 힌트

    def test_quota_error_classified(self):
        import urllib.error
        def boom(*a, **k):
            raise urllib.error.HTTPError("u", 429, "too many", {}, None)
        r = rr.run_review(cfg(), PACKET, DIFF, call_fn=boom)
        self.assertEqual(r.verdict, "error")
        self.assertIn("quota", " ".join(r.reasons).lower())

    def test_classify_helper_direct(self):
        import urllib.error
        self.assertEqual(rr.classify_gateway_error(
            urllib.error.HTTPError("u", 403, "x", {}, None))[0], "auth")
        self.assertEqual(rr.classify_gateway_error(
            urllib.error.HTTPError("u", 503, "x", {}, None))[0], "unreachable")
        self.assertEqual(rr.classify_gateway_error(TimeoutError())[0], "unreachable")


class TestGatewayRetry(unittest.TestCase):
    """_default_gateway_call의 transient 재시도 — 일시적 에러만 재시도, 영구 에러는 즉시 전파.

    friends 리뷰 결론(같은 provider bounded 재시도)을 검증. 재시도는 네트워크 호출만 반복하며
    verdict 판정에는 관여하지 않는다(fail-closed 보존).
    """

    def _patch(self, sequence):
        """urlopen을 sequence의 항목으로 순차 대체. 예외 객체면 raise, 아니면 응답 반환."""
        import urllib.request
        calls = {"n": 0}

        class FakeResp:
            def __init__(self, text):
                self._t = json.dumps(
                    {"choices": [{"message": {"content": text}}]}).encode()
            def read(self):
                return self._t
            def __enter__(self):
                return self
            def __exit__(self, *a):
                return False

        def fake_urlopen(req, timeout=60):
            i = calls["n"]
            calls["n"] += 1
            item = sequence[min(i, len(sequence) - 1)]
            if isinstance(item, Exception):
                raise item
            return FakeResp(item)

        self._orig = urllib.request.urlopen
        urllib.request.urlopen = fake_urlopen
        self._calls = calls
        os.environ.setdefault("AI_GATEWAY_BASE_URL", "https://gw.example")
        os.environ.setdefault("AI_GATEWAY_TOKEN", "k")
        return calls

    def tearDown(self):
        import urllib.request
        if hasattr(self, "_orig"):
            urllib.request.urlopen = self._orig

    def test_retries_on_5xx_then_succeeds(self):
        import urllib.error
        err = urllib.error.HTTPError("u", 503, "busy", {}, None)
        calls = self._patch([err, '{"verdict":"approve"}'])
        out = rr._default_gateway_call([{"role": "user", "content": "x"}], "m", 100)
        self.assertIn("approve", out)
        self.assertEqual(calls["n"], 2)  # 1 실패 + 1 성공

    def test_permanent_4xx_not_retried(self):
        import urllib.error
        err = urllib.error.HTTPError("u", 400, "bad", {}, None)
        calls = self._patch([err, '{"verdict":"approve"}'])
        with self.assertRaises(urllib.error.HTTPError):
            rr._default_gateway_call([{"role": "user", "content": "x"}], "m", 100)
        self.assertEqual(calls["n"], 1)  # 재시도 없음


if __name__ == "__main__":
    unittest.main(verbosity=2)
