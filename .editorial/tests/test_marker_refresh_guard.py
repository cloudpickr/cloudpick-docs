#!/usr/bin/env python3
"""
marker-refresh-guard.py 테스트 — 실제 실행(subprocess).

리뷰 기준 마커의 '월 토큰만' 교체는 통과시키고, 마커 외 변경·라인증감·본문 날짜
조작(마커가 아닌 라인의 월 변경)은 fail-closed로 차단함을 검증.
"""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

GUARD = Path(__file__).resolve().parent.parent.parent / "scripts" / "marker-refresh-guard.py"

BASE_KO = """---
title: Test
---

> 문서 기준: 2026년 9월

## 개요

이 제도는 2026년 9월 현재 확정되지 않았습니다.
본문 끝.
"""

BASE_KO_SUFFIX = """---
title: Test
---

> 문서 기준: 2026년 9월 (2차 단계평가 결과 반영)

본문.
"""

BASE_EN = """---
title: Test
---

> Last reviewed: September 2026

As of September 2026, this is pending.
"""

BASE_JA = """---
title: Test
---

> 文書基準: 2026年9月

2026年9月現在、未確定です。
"""

ARGS = [
    "--from-month-ko", "2026년 9월", "--to-month-ko", "2026년 10월",
    "--from-month-en", "September 2026", "--to-month-en", "October 2026",
    "--from-month-ja", "2026年9月", "--to-month-ja", "2026年10月",
]


def run_guard(base: str, head: str) -> int:
    with tempfile.TemporaryDirectory() as d:
        dp = Path(d)
        (dp / "base.md").write_text(base, encoding="utf-8")
        (dp / "head.md").write_text(head, encoding="utf-8")
        r = subprocess.run(
            [sys.executable, str(GUARD), "--base", str(dp / "base.md"),
             "--head", str(dp / "head.md"), *ARGS],
            capture_output=True, text=True,
        )
        return r.returncode


class TestPass(unittest.TestCase):
    def test_ko_marker_only_promotion_passes(self):
        head = BASE_KO.replace("> 문서 기준: 2026년 9월", "> 문서 기준: 2026년 10월")
        self.assertEqual(run_guard(BASE_KO, head), 0)

    def test_ko_marker_with_suffix_preserved(self):
        head = BASE_KO_SUFFIX.replace(
            "> 문서 기준: 2026년 9월 (2차 단계평가 결과 반영)",
            "> 문서 기준: 2026년 10월 (2차 단계평가 결과 반영)",
        )
        self.assertEqual(run_guard(BASE_KO_SUFFIX, head), 0)

    def test_en_marker_only_promotion_passes(self):
        head = BASE_EN.replace("> Last reviewed: September 2026", "> Last reviewed: October 2026")
        self.assertEqual(run_guard(BASE_EN, head), 0)

    def test_ja_marker_only_promotion_passes(self):
        head = BASE_JA.replace("> 文書基準: 2026年9月", "> 文書基準: 2026年10月")
        self.assertEqual(run_guard(BASE_JA, head), 0)

    def test_no_change_passes(self):
        self.assertEqual(run_guard(BASE_KO, BASE_KO), 0)


class TestFailClosed(unittest.TestCase):
    def test_body_date_tamper_fails(self):
        # 마커는 올리되 본문의 '9월 현재'를 '10월 현재'로 몰래 바꾸는 날조 → 차단.
        head = BASE_KO.replace("> 문서 기준: 2026년 9월", "> 문서 기준: 2026년 10월")
        head = head.replace("2026년 9월 현재", "2026년 10월 현재")
        self.assertEqual(run_guard(BASE_KO, head), 1)

    def test_body_only_date_tamper_without_marker_fails(self):
        head = BASE_KO.replace("2026년 9월 현재", "2026년 10월 현재")
        self.assertEqual(run_guard(BASE_KO, head), 1)

    def test_line_added_fails(self):
        head = BASE_KO.replace("> 문서 기준: 2026년 9월", "> 문서 기준: 2026년 10월") + "추가 줄.\n"
        self.assertEqual(run_guard(BASE_KO, head), 1)

    def test_wrong_target_month_fails(self):
        # 마커를 11월로 올림(승인된 to=10월이 아님) → 재구성 불일치로 차단.
        head = BASE_KO.replace("> 문서 기준: 2026년 9월", "> 문서 기준: 2026년 11월")
        self.assertEqual(run_guard(BASE_KO, head), 1)

    def test_prose_change_fails(self):
        head = BASE_KO.replace("본문 끝.", "본문 바뀜.")
        self.assertEqual(run_guard(BASE_KO, head), 1)


if __name__ == "__main__":
    unittest.main()
