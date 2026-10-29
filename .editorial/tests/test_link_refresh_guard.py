#!/usr/bin/env python3
"""
link-refresh-guard.py 테스트 — 실제 실행(subprocess).

council 합의: '재구성 매칭'으로 URL 교체만 통과시키고, URL 외 변경·라인증감·보호영역
(코드/frontmatter/mermaid)·인라인코드 변경은 fail-closed로 차단함을 검증.
"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

GUARD = Path(__file__).resolve().parent.parent.parent / "scripts" / "link-refresh-guard.py"

BASE = """---
title: Test
---
본문입니다. [문서](https://docs.anthropic.com/) 참고.
`https://docs.anthropic.com/` 는 코드(현행화 대상 아님).

```sh
curl https://docs.anthropic.com/
```
끝.
"""

MAP = {"https://docs.anthropic.com/": "https://platform.claude.com/docs/en/home"}


def run_guard(base: str, head: str, mapping: dict) -> int:
    with tempfile.TemporaryDirectory() as d:
        dp = Path(d)
        (dp / "base.md").write_text(base, encoding="utf-8")
        (dp / "head.md").write_text(head, encoding="utf-8")
        (dp / "map.json").write_text(json.dumps(mapping), encoding="utf-8")
        r = subprocess.run(
            [sys.executable, str(GUARD), "--base", str(dp / "base.md"),
             "--head", str(dp / "head.md"), "--mapping", str(dp / "map.json")],
            capture_output=True, text=True,
        )
        return r.returncode


class TestPass(unittest.TestCase):
    def test_prose_url_only_replacement_passes(self):
        head = BASE.replace(
            "[문서](https://docs.anthropic.com/)",
            "[문서](https://platform.claude.com/docs/en/home)",
        )
        self.assertEqual(run_guard(BASE, head, MAP), 0)

    def test_no_change_passes(self):
        self.assertEqual(run_guard(BASE, BASE, MAP), 0)


class TestFailClosed(unittest.TestCase):
    def test_prose_text_changed_fails(self):
        head = BASE.replace(
            "[문서](https://docs.anthropic.com/) 참고.",
            "[문서](https://platform.claude.com/docs/en/home) 꼭 참고하세요.",
        )
        self.assertEqual(run_guard(BASE, head, MAP), 1)

    def test_line_added_fails(self):
        head = BASE.replace(
            "[문서](https://docs.anthropic.com/)",
            "[문서](https://platform.claude.com/docs/en/home)",
        ) + "추가된 줄.\n"
        self.assertEqual(run_guard(BASE, head, MAP), 1)

    def test_code_fence_url_change_fails(self):
        head = BASE.replace(
            "curl https://docs.anthropic.com/",
            "curl https://platform.claude.com/docs/en/home",
        )
        self.assertEqual(run_guard(BASE, head, MAP), 1)

    def test_inline_code_url_change_fails(self):
        head = BASE.replace(
            "`https://docs.anthropic.com/`",
            "`https://platform.claude.com/docs/en/home`",
        )
        self.assertEqual(run_guard(BASE, head, MAP), 1)

    def test_identity_mapping_rejected(self):
        bad = {"https://x.com/": "https://x.com/"}
        self.assertEqual(run_guard(BASE, BASE, bad), 1)

    def test_substring_old_rejected(self):
        bad = {
            "https://a.com/": "https://b.com/",
            "https://a.com/x": "https://c.com/",  # 'https://a.com/' ⊂ this key
        }
        self.assertEqual(run_guard(BASE, BASE, bad), 1)

    def test_non_url_mapping_rejected(self):
        bad = {"not-a-url": "https://b.com/"}
        self.assertEqual(run_guard(BASE, BASE, bad), 1)


if __name__ == "__main__":
    unittest.main()
