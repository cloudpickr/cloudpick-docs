#!/usr/bin/env python3
"""
강조(볼드) 오렌더링 린트 — CJK 문맥의 `**` 닫는 경계 검사

배경:
  CommonMark에서 `**`가 닫는 구분자로 인정되려면 "right-flanking"이어야
  하고, 닫는 `**` 바로 **앞이 구두점이면 바로 뒤는 공백이나 구두점**이어야
  한다. 앞이 구두점이고 뒤가 '문자(letter/숫자)'면 닫는 구분자로 쓰이지
  못해 강조가 통째로 깨진다. 한글·일본어에서 괄호·조사·기호가 공백 없이
  붙어 자주 발생한다.

      깨짐:   **배포 형태(호스티드 ↔ 오픈웨이트)**와   ← '**' 앞 ')' + 뒤 '와'
      깨짐:   **年間シンガポール売上高の10%**の        ← '**' 앞 '%' + 뒤 'の'
      올바름: **배포 형태**(호스티드 ↔ 오픈웨이트)와

정책:
  강조는 용어만 감싸고 괄호·조사·단위기호는 밖에 둔다.

구현 노트(오탐 방지):
  - '구두점' 판정은 하드코딩 목록이 아니라 Unicode 카테고리(P*, S*)로 한다
    (예: '%'(Po), ')'(Pe), '）'(Pe), '。'(Po), '」'(Pe) 등 모두 포함).
  - '뒤 문자' 판정은 공백도 구두점도 아닌 것(= letter/숫자류)로 한다.
  - 코드 스팬은 가변 길이 백틱(`, ``, ``` ...)을 모두 제거한다.
  - '**'를 왼쪽부터 쌍으로 토큰화해 '닫는 **'에 대해서만 flanking을 본다
    (정규식 단독은 인접 강조의 '**'와 오짝지어 오탐이 폭증한다).

사용법:
  python3 scripts/lint-emphasis.py        # 전체 검사 (CI)
"""
import re
import os
import sys
import unicodedata

DOCS_DIR = "src/content/docs"
LOCALES = ["ko", "en", "ja"]

ALLOWLIST = []  # 매치 조각 부분 일치 허용 목록

# 가변 길이 백틱 코드 스팬 제거: `..`, ``..``, ```..``` 등 균형 쌍.
CODESPAN = re.compile(r"(`+)(?:.+?)\1")


def strip_code(text: str) -> str:
    return CODESPAN.sub(lambda m: " " * len(m.group(0)), text)


def is_punct(ch: str) -> bool:
    """Unicode 구두점/기호 — 닫는 ** 앞에 오면 flanking 판정 대상."""
    if not ch:
        return False
    cat = unicodedata.category(ch)
    # P* = 구두점, S* = 기호(%,·는 각각 Po/Po지만 통화·수학기호 Sc/Sm 포함).
    return cat.startswith("P") or cat.startswith("S")


def is_letter_like(ch: str) -> bool:
    """닫는 ** 뒤에 오면 깨짐을 유발하는 '문자'류(공백도 구두점도 아님)."""
    if not ch:
        return False
    if ch.isspace():
        return False
    cat = unicodedata.category(ch)
    # 구두점/기호가 아니면(= 글자·숫자·CJK 등) letter-like로 본다.
    return not (cat.startswith("P") or cat.startswith("S"))


def check_segment(seg: str):
    """세그먼트에서 깨진 '닫는 **'의 (col, frag) 목록."""
    stars = [m.start() for m in re.finditer(r"\*\*", seg)]
    issues = []
    i = 0
    while i + 1 < len(stars):
        open_pos = stars[i]
        close_pos = stars[i + 1]
        before = seg[close_pos - 1] if close_pos - 1 >= 0 else ""
        after_idx = close_pos + 2
        after = seg[after_idx] if after_idx < len(seg) else ""
        # 깨짐: 닫는 ** 앞이 구두점/기호 + 뒤가 문자류(공백·구두점 아님)
        if is_punct(before) and is_letter_like(after):
            frag = seg[open_pos:min(len(seg), after_idx + 1)]
            issues.append((open_pos, frag[:70]))
        i += 2
    return issues


def find_issues(content: str, path: str):
    out = []
    in_fence = False
    for ln, raw in enumerate(content.split("\n"), 1):
        s = raw.rstrip()
        if s.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        line = strip_code(s)
        segments = line.split("|") if line.lstrip().startswith("|") else [line]
        for seg in segments:
            for _col, frag in check_segment(seg):
                if any(a in frag for a in ALLOWLIST):
                    continue
                out.append({"file": path, "line": ln, "match": frag})
    return out


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
                with open(path, encoding="utf-8") as fh:
                    all_issues.extend(find_issues(fh.read(), path))

    if all_issues:
        print(f"❌ FAIL: {len(all_issues)} broken bold boundary(ies)\n")
        for iss in all_issues:
            print(f"  {iss['file']}  line#{iss['line']}  {iss['match']!r}")
        print(
            "\n닫는 '**' 바로 앞이 구두점/기호이고 뒤에 글자가 붙으면 볼드가 렌더링되지 않습니다.\n"
            "강조는 용어만 감싸고 괄호·조사·단위기호는 밖에 두세요. 예: **배포 형태**(호스티드)와"
        )
        sys.exit(1)
    print(f"✅ No broken bold boundaries ({DOCS_DIR})")


if __name__ == "__main__":
    main()
