#!/usr/bin/env python3
"""
문서 일관성 린트 — AGENTS.md 규약 중 기계적으로 검증 가능한 3가지 검사

검사 항목:
  1) 로케일 대칭성(locale parity)
     - ko/en/ja 세 로케일의 문서 상대경로 집합이 완벽히 일치해야 한다.
       (AGENTS.md "3개 로케일 대칭성 보장": 미번역/고립 파일 금지)
  2) 문서 기준 마커(review marker)
     - 각 문서는 로케일별 표준 접두사로 시작하는 `>` 인용 마커를 가져야 한다.
       ko: "> 문서 기준: 2026년 8월"
       en: "> Last reviewed: August 2026"
       ja: "> 文書基準: 2026年8月"
       (AGENTS.md "기준 시점: 2026년 8월", 모든 문서에 기준 시점 명시)
     - 랜딩 페이지 index.mdx는 예외.
  3) 접이식 블록 금지(no <details>/<summary>)
     - 딥링크·Pagefind·스크린리더 접근성 저해로 AGENTS.md에서 금지.

사용법:
  python3 scripts/lint-docs-consistency.py      # 전체 검사 (CI)
"""
import os
import re
import sys

DOCS_DIR = "src/content/docs"
LOCALES = ["ko", "en", "ja"]

# 로케일별 문서 기준 마커의 표준 접두사(뒤에 부가 문구가 붙는 변형 허용).
MARKER_PREFIX = {
    "ko": "> 문서 기준: 2026년 8월",
    "en": "> Last reviewed: August 2026",
    "ja": "> 文書基準: 2026年8月",
}

# 마커 예외 파일(로케일 루트 기준 상대경로). 랜딩·웰컴 페이지는 마커를 두지 않는다.
MARKER_EXEMPT = {"index.mdx", "introduction.mdx"}

# 접이식 블록 탐지(여는 태그만 잡으면 충분).
DETAILS_RE = re.compile(r"<\s*(details|summary)\b", re.IGNORECASE)


def doc_files(locale_dir):
    """로케일 디렉터리 내 .md/.mdx의 (상대경로, 절대경로) 목록."""
    out = []
    for root, _, files in os.walk(locale_dir):
        for f in files:
            if f.endswith((".md", ".mdx")):
                abs_path = os.path.join(root, f)
                rel_path = os.path.relpath(abs_path, locale_dir)
                out.append((rel_path, abs_path))
    return out


def strip_code_fences(lines):
    """코드펜스(```) 내부 라인은 <details> 검사에서 제외."""
    kept = []
    in_fence = False
    for ln, raw in enumerate(lines, 1):
        if raw.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            kept.append((ln, raw))
    return kept


def check_parity(sets_by_locale):
    """세 로케일의 상대경로 집합 대칭성 검사."""
    issues = []
    union = set().union(*sets_by_locale.values())
    for rel in sorted(union):
        present = [loc for loc in LOCALES if rel in sets_by_locale[loc]]
        if len(present) != len(LOCALES):
            missing = [loc for loc in LOCALES if loc not in present]
            issues.append(
                f"[parity] {rel} — 존재: {','.join(present)} / 누락: {','.join(missing)}"
            )
    return issues


def check_marker(rel_path, abs_path, locale):
    """문서 기준 마커 존재 검사."""
    if rel_path in MARKER_EXEMPT:
        return []
    prefix = MARKER_PREFIX[locale]
    with open(abs_path, encoding="utf-8") as fh:
        content = fh.read()
    for line in content.split("\n"):
        if line.strip().startswith(prefix):
            return []
    return [f"[marker] {abs_path} — 표준 마커 누락 (기대: '{prefix} ...')"]


def check_details(abs_path):
    """접이식 블록(<details>/<summary>) 사용 검사."""
    issues = []
    with open(abs_path, encoding="utf-8") as fh:
        lines = fh.read().split("\n")
    for ln, raw in strip_code_fences(lines):
        if DETAILS_RE.search(raw):
            issues.append(f"[details] {abs_path} line#{ln} — 접이식 블록 금지: {raw.strip()[:60]!r}")
    return issues


def main():
    sets_by_locale = {}
    all_issues = []

    for locale in LOCALES:
        locale_dir = os.path.join(DOCS_DIR, locale)
        if not os.path.isdir(locale_dir):
            all_issues.append(f"[parity] 로케일 디렉터리 없음: {locale_dir}")
            sets_by_locale[locale] = set()
            continue

        files = doc_files(locale_dir)
        sets_by_locale[locale] = {rel for rel, _ in files}

        for rel_path, abs_path in files:
            all_issues.extend(check_marker(rel_path, abs_path, locale))
            all_issues.extend(check_details(abs_path))

    all_issues = check_parity(sets_by_locale) + all_issues

    if all_issues:
        print(f"❌ FAIL: {len(all_issues)} docs consistency issue(s)\n")
        for iss in all_issues:
            print(f"  {iss}")
        print(
            "\n규약: AGENTS.md의 3로케일 대칭성 / 문서 기준 마커 / 접이식 금지 참고.\n"
            "마커 표준 문구: ko '문서 기준: 2026년 8월', en 'Last reviewed: August 2026', "
            "ja '文書基準: 2026年8月'."
        )
        sys.exit(1)
    else:
        print(f"✅ Docs consistency OK — parity + markers + no <details> ({DOCS_DIR})")


if __name__ == "__main__":
    main()
