#!/usr/bin/env python3
"""
MCP 인덱스 품질 린트(warn-only) — 빌드 산출물 dist/llms/* 의 품질을 검증한다.

배경: MCP(및 llms.txt 소비자)는 scripts/build-llms-locales.mjs가 만든
  - dist/llms/llms-full-{ko,en,ja}.txt  (로케일별 전체 문서, 페이지마다 '# 제목')
  - dist/llms/routing-index.json         (제목(소문자) → [언어] 맵)
를 소비한다. 이 산출물이 소스 문서를 정확히 반영하는지(누락/중복/깨짐 없이)를 검증한다.

핵심 원칙 — FENCE-AWARE(agy/claude 교차검증 결론):
  llms-full의 '페이지'는 줄 맨앞 '# '로 시작하지만, **코드펜스(``` / ~~~) 내부의 '#'**
  (예: 셸 주석 '# comment')는 페이지 헤더가 아니다. 순진하게 '^#'를 세면 코드 주석이
  가짜 페이지로 잡혀 오탐이 난다(실측: raw 124 vs fence-aware 119 = 파일 수). 따라서
  모든 페이지 카운트/제목 추출은 CommonMark 코드펜스를 추적해 수행한다.

검사(포함 — 친구 합의):
  1) 페이지 수 정합: fence-aware 페이지 수 == 해당 로케일 소스 문서 수, 그리고 ko==en==ja.
  2) 제목 집합 일치(로케일 내): llms-full의 fence-aware 제목 집합 ⊇ 소스 frontmatter title 집합.
     (누락 제목 = MCP에서 검색 안 되는 문서 → 품질 이슈)
  3) routing-index.json: 유효한 JSON, 값은 ['ko'|'en'|'ja'] 부분집합, 키는 비어있지 않음.
  4) 빈 본문 페이지: 제목만 있고 본문이 없는 페이지(랜딩/소개는 ALLOW_EMPTY 제외).

의도적으로 제외(오탐 방지 — 친구 합의):
  - raw '^#' 카운트(fence 미인식) 사용 금지.
  - 로케일 간 routing-key 대칭(키가 번역 제목이라 원천적으로 비대칭 — 정상).
  - 로케일 내 중복 제목 자체를 실패로 보지 않음(index/introduction 등 정당).
  - 로케일 간 길이 동일성(번역은 길이가 다름).
  - 마커/파일경로 대칭(lint-docs-consistency.py가 이미 담당).

정책: warn-only(exit 0). dist/llms 없으면 빌드 안내 후 skip(non-fail).

사용법:
  npm run build && python3 scripts/lint-mcp-index.py
"""
from __future__ import annotations

import json
import os
import re
import sys

DOCS_DIR = "src/content/docs"
LLMS_DIR = "dist/llms"
LOCALES = ["ko", "en", "ja"]

# 빈 본문이 정당한 페이지(랜딩/소개/허브). 제목(소문자)으로 매칭.
ALLOW_EMPTY_TITLES = {
    "cloudpick docs",
}

FENCE_RE = re.compile(r"^(\s{0,3})(`{3,}|~{3,})")


def fence_aware_titles(text: str) -> list[str]:
    """코드펜스를 추적하며 페이지 제목('# ...')만 추출.

    CommonMark 근사: 여는 펜스는 ``` 또는 ~~~ (3자 이상), 최대 3칸 들여쓰기 허용.
    닫는 펜스는 같은 문자·같은 길이 이상. 펜스 내부의 '# '는 헤더로 세지 않는다.
    """
    titles: list[str] = []
    in_fence = False
    fence_char = ""
    fence_len = 0
    for line in text.split("\n"):
        m = FENCE_RE.match(line)
        if m:
            marker = m.group(2)
            ch, ln = marker[0], len(marker)
            if not in_fence:
                in_fence, fence_char, fence_len = True, ch, ln
                continue
            # 닫는 펜스: 같은 문자 + 같은 길이 이상
            if ch == fence_char and ln >= fence_len:
                in_fence = False
                continue
        if not in_fence and line.startswith("# "):
            titles.append(line[2:].strip())
    return titles


def fence_aware_pages(text: str) -> list[tuple[str, str]]:
    """(제목, 본문) 목록 — fence-aware. 본문은 다음 페이지 헤더 전까지."""
    lines = text.split("\n")
    pages: list[tuple[str, list[str]]] = []
    in_fence = False
    fence_char = ""
    fence_len = 0
    cur_title = None
    cur_body: list[str] = []
    for line in lines:
        m = FENCE_RE.match(line)
        toggled = False
        if m:
            marker = m.group(2)
            ch, ln = marker[0], len(marker)
            if not in_fence:
                in_fence, fence_char, fence_len = True, ch, ln
                toggled = True
            elif ch == fence_char and ln >= fence_len:
                in_fence = False
                toggled = True
        if not in_fence and not toggled and line.startswith("# "):
            if cur_title is not None:
                pages.append((cur_title, cur_body))
            cur_title = line[2:].strip()
            cur_body = []
        else:
            if cur_title is not None:
                cur_body.append(line)
    if cur_title is not None:
        pages.append((cur_title, cur_body))

    out = []
    for title, body in pages:
        body_text = "\n".join(body)
        # 설명(> ...)·SYSTEM 라인 제외한 실제 본문 유무 판단
        meaningful = [ln for ln in body
                      if ln.strip() and not ln.startswith(">")
                      and not ln.startswith("<SYSTEM>")]
        out.append((title, body_text if meaningful else ""))
    return out


def source_titles(locale: str) -> set[str]:
    """소스 frontmatter title 집합(소문자)."""
    base = os.path.join(DOCS_DIR, locale)
    titles = set()
    for root, _, files in os.walk(base):
        for f in files:
            if not f.endswith((".md", ".mdx")):
                continue
            with open(os.path.join(root, f), encoding="utf-8") as fh:
                raw = fh.read()
            if not raw.startswith("---"):
                continue
            end = raw.find("\n---", 3)
            if end == -1:
                continue
            for line in raw[3:end].split("\n"):
                mt = re.match(r'^title:\s*(.*)$', line)
                if mt:
                    v = mt.group(1).strip().strip('"').strip("'")
                    if v:
                        titles.add(v.lower())
                    break
    return titles


def source_doc_count(locale: str) -> int:
    base = os.path.join(DOCS_DIR, locale)
    n = 0
    for _, _, files in os.walk(base):
        n += sum(1 for f in files if f.endswith((".md", ".mdx")))
    return n


def main() -> int:
    if not os.path.isdir(LLMS_DIR):
        print(f"ℹ️  {LLMS_DIR} 없음 — 먼저 `npm run build` 실행 필요(품질 검사 skip, non-fail)")
        return 0

    warnings: list[str] = []
    page_counts: dict[str, int] = {}

    for loc in LOCALES:
        path = os.path.join(LLMS_DIR, f"llms-full-{loc}.txt")
        if not os.path.isfile(path):
            warnings.append(f"[mcp-index] {path} 없음 — 빌드 산출 확인")
            continue
        text = open(path, encoding="utf-8").read()
        pages = fence_aware_pages(text)
        titles = [t for t, _ in pages]
        page_counts[loc] = len(titles)

        # 1) 페이지 수 == 소스 문서 수
        doc_n = source_doc_count(loc)
        if len(titles) != doc_n:
            warnings.append(f"[mcp-index] {loc}: llms-full 페이지 {len(titles)}개 "
                            f"≠ 소스 문서 {doc_n}개 (fence-aware) — 누락/과잉 확인")

        # 2) 제목 집합: 소스 frontmatter title이 모두 llms-full에 있는지
        src = source_titles(loc)
        idx = {t.lower() for t in titles}
        missing = src - idx
        if missing:
            sample = ", ".join(sorted(missing)[:5])
            warnings.append(f"[mcp-index] {loc}: 소스 제목 {len(missing)}개가 llms-full에 없음 "
                            f"(MCP 검색 누락 위험): {sample}")

        # 4) 빈 본문 페이지
        for title, body in pages:
            if not body and title.lower() not in ALLOW_EMPTY_TITLES:
                warnings.append(f"[mcp-index] {loc}: 빈 본문 페이지 '{title}' "
                                f"— 내용 누락 또는 ALLOW_EMPTY_TITLES 등록 검토")

    # 1b) 로케일 간 페이지 수 동일
    if len(set(page_counts.values())) > 1:
        warnings.append(f"[mcp-index] 로케일 간 페이지 수 불일치: {page_counts} "
                        f"— 번역 누락 가능")

    # 3) routing-index.json 유효성
    ri_path = os.path.join(LLMS_DIR, "routing-index.json")
    if os.path.isfile(ri_path):
        try:
            ri = json.load(open(ri_path, encoding="utf-8"))
            if not isinstance(ri, dict):
                warnings.append("[mcp-index] routing-index.json: dict 아님")
            else:
                bad = [k for k, v in ri.items()
                       if not k or not isinstance(v, list)
                       or any(x not in LOCALES for x in v)]
                if bad:
                    warnings.append(f"[mcp-index] routing-index.json: 잘못된 항목 {len(bad)}개 "
                                    f"(빈 키 또는 비-로케일 값): {bad[:5]}")
        except json.JSONDecodeError as exc:
            warnings.append(f"[mcp-index] routing-index.json 파싱 실패: {exc}")
    else:
        warnings.append(f"[mcp-index] {ri_path} 없음")

    if not warnings:
        counts = ", ".join(f"{k}={v}" for k, v in page_counts.items())
        print(f"✅ MCP 인덱스 품질 OK (fence-aware) — 페이지 {counts}, routing-index 유효")
        return 0

    print(f"⚠️  MCP 인덱스 경고 {len(warnings)}건(warn-only, 비차단)\n")
    for w in warnings:
        print(f"  {w}")
    print("\n참고: 경고는 차단하지 않습니다(exit 0). 페이지/제목은 코드펜스 인식(fence-aware)으로 셉니다.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
