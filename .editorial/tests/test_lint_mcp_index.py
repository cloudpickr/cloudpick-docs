#!/usr/bin/env python3
"""
lint-mcp-index.py 단위 테스트 — fence-aware 파싱 회귀 방지.

핵심 회귀: 코드펜스(``` / ~~~) 내부의 '# ...'(예: 셸 주석)를 페이지 헤더로 오인하면
llms-full 페이지 수가 부풀려져(실측 124 vs 실제 119) 가짜 품질 경고가 난다. fence 추적이
빠지거나 깨지면 이 테스트가 즉시 실패한다.
"""
import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
spec = importlib.util.spec_from_file_location("lint_mcp_index", ROOT / "scripts" / "lint-mcp-index.py")
mcp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mcp)


class TestFenceAware(unittest.TestCase):
    def test_excludes_hash_inside_code_fence(self):
        text = (
            "<SYSTEM>x</SYSTEM>\n\n"
            "# Page One\n\n본문\n\n"
            "```bash\n# shell comment not a page\naws s3 ls\n```\n\n"
            "# Page Two\n\n본문2\n"
        )
        titles = mcp.fence_aware_titles(text)
        self.assertEqual(titles, ["Page One", "Page Two"])

    def test_tilde_fence_and_length_rule(self):
        # ~~~~ (4개)로 연 펜스는 ~~~ (3개)로 닫히지 않아야 한다(닫는 펜스 길이 >= 여는 길이).
        text = (
            "# P1\n\n"
            "~~~~\n# inside\n~~~\nstill inside # x\n~~~~\n\n"
            "# P2\n"
        )
        titles = mcp.fence_aware_titles(text)
        self.assertEqual(titles, ["P1", "P2"])

    def test_pages_body_and_empty_detection(self):
        text = (
            "# Has Body\n\n실제 본문 있음\n\n"
            "# Empty One\n\n"  # 본문 없음
            "# Next\n\n본문\n"
        )
        pages = dict(mcp.fence_aware_pages(text))
        self.assertNotEqual(pages["Has Body"], "")
        self.assertEqual(pages["Empty One"], "")

    def test_raw_count_would_overcount(self):
        # 대조: fence 미인식(raw)이면 셸 주석까지 세어 오탐. fence-aware는 정확.
        text = "# Real\n\n```\n# c1\n# c2\n```\n"
        self.assertEqual(len(mcp.fence_aware_titles(text)), 1)
        raw = sum(1 for ln in text.split("\n") if ln.startswith("# "))
        self.assertEqual(raw, 3)  # raw는 3개(오탐) — 이 격차가 fence-aware의 존재 이유


if __name__ == "__main__":
    unittest.main(verbosity=2)
