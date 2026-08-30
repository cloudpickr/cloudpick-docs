#!/usr/bin/env python3
"""
취소선(strikethrough) 오렌더링 린트 — GFM 물결표(~) 문법 검사

배경:
  GFM에서 반각 물결표 `~`(U+007E) 또는 `~~`가 짝을 이루면 그 사이가
  취소선(<del>)으로 렌더링된다. 범위 표기(예: "수 주~수 개월")나 일본어
  문장에서 `~`를 무심코 쓰면, 의도치 않게 문구 전체가 취소선이 될 수 있다.

정책 (CONTRIBUTING.md "물결표·취소선" 참고):
  - 범위 표기는 엔대시 `–`(U+2013)를, 일본어는 전각 `～`(U+FF5E)를 사용한다.
  - 취소선이 정말 필요할 때만 `~~text~~`를 쓰고, 아래 ALLOWLIST에 등록한다.

검사 항목:
  코드펜스(```)와 인라인코드(`...`) 밖에서, GFM 규칙상 실제로 취소선으로
  렌더링되는 `~text~` / `~~text~~` 패턴을 탐지한다. 표 셀 경계(|)를 넘는
  짝은 렌더링되지 않으므로 셀 단위로 분리해 판정한다.

사용법:
  python3 scripts/lint-strikethrough.py        # 전체 검사 (CI)
"""
import re
import os
import sys

DOCS_DIR = "src/content/docs"
LOCALES = ["ko", "en", "ja"]

# 의도된 취소선(허용 목록). 매치된 내부 텍스트 기준으로 부분 일치 허용.
ALLOWLIST = [
    "2026.8.2 (원안)",
    "2026.8.2 (original)",
    "2026.8.2（原案）",
]

# GFM 취소선 근사 규칙:
#   여는 ~/~~ 다음에 공백·~가 오면 안 되고(left-flanking),
#   닫는 ~/~~ 앞에 공백·~가 오면 안 된다(right-flanking).
STRIKE = re.compile(r"(?<!~)(~~?)(?![\s~])(.+?)(?<![\s~])\1(?!~)")


def strip_code(text: str) -> str:
    """인라인 코드 스팬 제거 (내용은 공백으로 대체해 위치 왜곡 최소화)."""
    return re.sub(r"`[^`]*`", lambda m: " " * len(m.group(0)), text)


def is_allowed(inner: str) -> bool:
    return any(a in inner for a in ALLOWLIST)


def find_issues(content: str, path: str):
    issues = []
    in_fence = False
    for ln, raw in enumerate(content.split("\n"), 1):
        s = raw.rstrip()
        if s.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        line = strip_code(s)
        # 표 행이면 셀 단위로 분리 — 셀 경계(|)를 넘는 취소선은 렌더링되지 않음
        segments = line.split("|") if line.lstrip().startswith("|") else [line]
        for seg in segments:
            for m in STRIKE.finditer(seg):
                inner = m.group(2)
                if is_allowed(inner):
                    continue
                issues.append({
                    "file": path,
                    "line": ln,
                    "match": m.group(0)[:60],
                })
    return issues


def main():
    all_issues = []
    for lang in LOCALES:
        lang_dir = os.path.join(DOCS_DIR, lang)
        if not os.path.isdir(lang_dir):
            continue
        for root, _, files in os.walk(lang_dir):
            for f in files:
                if not f.endswith((".md", ".mdx")):
                    continue
                path = os.path.join(root, f)
                content = open(path, encoding="utf-8").read()
                all_issues.extend(find_issues(content, path))

    if all_issues:
        print(f"❌ FAIL: {len(all_issues)} unintended strikethrough(s)\n")
        for iss in all_issues:
            print(f"  {iss['file']}  line#{iss['line']}  {iss['match']!r}")
        print(
            "\n범위 표기는 엔대시 '–'(U+2013), 일본어는 전각 '～'(U+FF5E)를 사용하세요.\n"
            "의도된 취소선이면 scripts/lint-strikethrough.py의 ALLOWLIST에 추가하세요."
        )
        sys.exit(1)
    else:
        print(f"✅ No unintended strikethrough ({DOCS_DIR})")


if __name__ == "__main__":
    main()
