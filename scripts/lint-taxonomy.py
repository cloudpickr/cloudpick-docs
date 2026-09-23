#!/usr/bin/env python3
"""
분류(정보 아키텍처) 린트(warn-only) — 사이드바와 실제 문서의 정합성을 경고한다.

배경: 사람이 육안으로 하던 "문서가 엉뚱한 그룹에 있나 / 사이드바에서 빠졌나 / 한 그룹이
너무 비대한가" 점검을 결정적으로 재현한다. 편집 리뷰 LLM 축은 diff만 보므로 전역 구조
정합성은 잡지 못한다 → 이 린터가 담당.

검사(claude/agy 리뷰 반영):
  1) 고아 문서(orphan): src/content/docs/ko/**의 문서 중 astro.config.mjs 사이드바 어떤 slug로도
     참조되지 않는 것. 단 랜딩/부분/인라인 전용 페이지가 있을 수 있어 '오류'가 아니라 '경고'이며,
     ORPHAN_ALLOW로 의도적 비링크 페이지를 제외한다.
  2) 그룹 크기: 한 사이드바 그룹의 문서 수가 GROUP_MAX(기본 12) 초과 → 소그룹 분할 검토 경고,
     또는 0/1개 → 그룹 존재 의의 재검토 경고.

의도적으로 하지 않는 것:
  - 사이드바가 '없는 파일'을 가리키는 깨진 참조(missing ref)는 Starlight 빌드(링크 검증)가
    이미 실패시키므로 여기서 중복 검사하지 않는다.
  - 소그룹 신설/재편 제안은 AGENTS.md의 3-of-5 거버넌스 의결 대상이다. 이 린터는 '검토하라'는
    경고만 낼 뿐 자동 변경하지 않는다.

정책: warn-only(exit 0), ko 전용, 사이드바 파싱은 정규식(mjs).

사용법:
  python3 scripts/lint-taxonomy.py
"""
from __future__ import annotations

import argparse
import os
import re
import sys

DOCS_DIR = "src/content/docs/ko"
CONFIG = "astro.config.mjs"

GROUP_MAX = 12   # 그룹당 문서 수 상한(초과 시 분할 검토 경고)

# 의도적으로 사이드바에 링크하지 않는 문서(랜딩/웰컴/부분/개요 허브 페이지 등). 로케일 루트 기준 상대경로.
ORPHAN_ALLOW = {
    "index.mdx",         # 랜딩
    "introduction.mdx",  # 소개(사이드바 상단 link로 별도 취급)
    "glossary.md",       # 용어집(link로 별도)
    "mcp.md",            # MCP(link로 별도)
    # 국가별 섹션 개요(허브) 페이지 — 그룹 자체가 랜딩 역할을 하며 개별 slug로 링크하지 않음.
    "eu/index.md",
    "us/index.md",
    "japan/index.md",
    "korea/index.md",
    "singapore/index.md",
}

SLUG_RE = re.compile(r"slug:\s*'([^']+)'")
LINK_RE = re.compile(r"link:\s*'([^']+)'")


def sidebar_slugs(config_text: str) -> list[str]:
    """astro.config.mjs에서 참조된 모든 slug/link 경로(ko 로케일 기준, 접두사 없음)."""
    slugs = SLUG_RE.findall(config_text)
    links = LINK_RE.findall(config_text)
    return slugs + links


def doc_slugs() -> dict[str, str]:
    """실제 문서 → slug(확장자 제거, 로케일 접두사 없음) 매핑. {slug: rel_path}."""
    out: dict[str, str] = {}
    for root, _, files in os.walk(DOCS_DIR):
        for f in sorted(files):
            if not f.endswith((".md", ".mdx")):
                continue
            abs_path = os.path.join(root, f)
            rel = os.path.relpath(abs_path, DOCS_DIR)             # 예: ai/ai-ml.md
            slug = re.sub(r"\.(md|mdx)$", "", rel)                # 예: ai/ai-ml
            out[slug] = rel
    return out


def group_sizes(config_text: str) -> list[tuple[str, int]]:
    """각 사이드바 그룹(label 블록)의 직속 slug 개수. (label, count) 목록.

    중첩 items를 정확히 파싱하는 대신, label 라인과 그다음 label 라인 사이의 slug 수를 센다
    (근사). 과다/과소 그룹 신호 용도로는 충분하다.
    """
    lines = config_text.split("\n")
    label_idx = [(i, m.group(1)) for i, ln in enumerate(lines)
                 if (m := re.search(r"label:\s*'([^']+)'", ln))]
    sizes = []
    for k, (i, label) in enumerate(label_idx):
        end = label_idx[k + 1][0] if k + 1 < len(label_idx) else len(lines)
        count = sum(1 for j in range(i, end) if "slug:" in lines[j])
        if count > 0:  # slug를 직접 담는 leaf 그룹만(상위 컨테이너 label 제외)
            sizes.append((label, count))
    return sizes


def main() -> int:
    argparse.ArgumentParser().parse_args()

    if not os.path.isfile(CONFIG):
        print(f"⚠️  {CONFIG} 없음 — 분류 검사 건너뜀")
        return 0

    config_text = open(CONFIG, encoding="utf-8").read()
    referenced = set(sidebar_slugs(config_text))
    docs = doc_slugs()

    warnings: list[str] = []

    # 1) 고아 문서
    for slug, rel in sorted(docs.items()):
        if rel in ORPHAN_ALLOW:
            continue
        if slug not in referenced:
            warnings.append(f"[taxonomy] 고아 문서(사이드바 미참조): {rel} "
                            f"— 사이드바 편입 또는 ORPHAN_ALLOW 등록 검토")

    # 2) 그룹 크기
    for label, count in group_sizes(config_text):
        if count > GROUP_MAX:
            warnings.append(f"[taxonomy] 그룹 '{label}' 문서 {count}개(> {GROUP_MAX}) "
                            f"— 의미 단위 소그룹 분할 검토(거버넌스 의결 대상)")
        elif count == 1:
            warnings.append(f"[taxonomy] 그룹 '{label}' 문서 1개 "
                            f"— 그룹 존재 의의/병합 검토")

    if not warnings:
        print(f"✅ 분류 경고 없음 — 사이드바 {len(referenced)} slug, 문서 {len(docs)}개")
        return 0

    print(f"⚠️  분류 경고 {len(warnings)}건(warn-only, 비차단)\n")
    for w in warnings:
        print(f"  {w}")
    print("\n참고: 경고는 차단하지 않습니다(exit 0). 구조 변경은 AGENTS.md의 과반 의결 절차를 따르세요.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
