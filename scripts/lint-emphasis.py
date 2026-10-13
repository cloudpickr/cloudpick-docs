#!/usr/bin/env python3
"""
강조(볼드) 오렌더링 린트 — CJK 문맥의 `**` 닫는 경계 검사

배경:
  CommonMark에서 `**`가 닫는 구분자로 인정되려면 "right-flanking"이어야
  한다. 닫는 `**` 바로 **앞이 구두점이고 바로 뒤가 영숫자/CJK**이면
  (right-flanking이지만 intraword 조건 불충족) 닫는 구분자로 쓰이지 못해
  강조가 통째로 깨진다. 한글·일본어에서 조사·전각 구두점이 공백 없이 붙어
  자주 발생한다.

      깨짐:   **배포 형태(호스티드 ↔ 오픈웨이트)**와   ← '**' 앞 ')' + 뒤 '와'
      올바름: **배포 형태**(호스티드 ↔ 오픈웨이트)와

정책:
  강조는 용어만 감싸고 괄호·조사는 밖에 둔다.

구현 노트(오탐 방지):
  정규식 하나로 강조 쌍과 flanking을 동시에 보면 인접한 다른 강조의 '**'와
  잘못 짝지어 오탐이 폭증한다. 그래서 줄에서 코드/표셀을 제거한 뒤 '**'를
  **왼쪽부터 순서대로 쌍(여는→닫는)으로 토큰화**하고, 각 '닫는 **'에 대해서만
  flanking 위반을 판정한다. (단일 '*' 이탤릭은 오탐 위험이 커 검사 대상에서
  제외하고 '**'만 본다.)

사용법:
  python3 scripts/lint-emphasis.py        # 전체 검사 (CI)
"""
import re
import os
import sys

DOCS_DIR = "src/content/docs"
LOCALES = ["ko", "en", "ja"]

ALLOWLIST = []  # 매치 조각 부분 일치 허용 목록

CJK = "\uac00-\ud7a3\u1100-\u11ff\u3130-\u318f\u3040-\u30ff\u4e00-\u9fff"
# 닫는 ** 바로 앞 문자가 이 '구두점'이면서 뒤가 영숫자/CJK면 깨진다.
# (반각/전각 닫는 괄호·따옴표·마침표 등)
PUNCT_BEFORE = set(")]}>.,!?;:'\"”’）】》」』。")
# 닫는 ** 바로 뒤가 이 부류(영숫자/CJK)면 intraword로 간주돼 닫힘 실패.
AFTER_RE = re.compile(f"[0-9A-Za-z{CJK}]")


def strip_code(text: str) -> str:
    return re.sub(r"`[^`]*`", lambda m: " " * len(m.group(0)), text)


def check_segment(seg: str):
    """세그먼트(표 셀 또는 비표 줄)에서 깨진 '닫는 **'의 (col, frag) 목록."""
    # '**' 위치를 모두 찾는다.
    stars = [m.start() for m in re.finditer(r"\*\*", seg)]
    issues = []
    # 왼쪽부터 쌍으로 소비: [여는, 닫는], [여는, 닫는] ...
    i = 0
    while i + 1 < len(stars):
        open_pos = stars[i]
        close_pos = stars[i + 1]
        # 닫는 ** 바로 앞 문자와 바로 뒤 문자
        before = seg[close_pos - 1] if close_pos - 1 >= 0 else ""
        after_idx = close_pos + 2
        after = seg[after_idx] if after_idx < len(seg) else ""
        # right-flanking 위반(= 깨짐): 앞이 구두점 + 뒤가 영숫자/CJK
        if before in PUNCT_BEFORE and after and AFTER_RE.match(after):
            frag = seg[open_pos:min(len(seg), after_idx + 1)]
            issues.append((open_pos, frag[:70]))
        # 이 쌍을 소비하고 다음 쌍으로
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
            "\n닫는 '**' 바로 앞이 구두점이고 뒤에 글자가 붙으면 볼드가 렌더링되지 않습니다.\n"
            "강조는 용어만 감싸고 괄호·조사는 밖에 두세요. 예: **배포 형태**(호스티드)와"
        )
        sys.exit(1)
    print(f"✅ No broken bold boundaries ({DOCS_DIR})")


if __name__ == "__main__":
    main()
