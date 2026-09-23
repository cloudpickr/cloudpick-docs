#!/usr/bin/env python3
"""
중복 린트(warn-only) — 서로 다른 문서 간 near-duplicate 문단을 경고한다.

배경: 편집 리뷰 워크플로의 LLM 축은 PR diff만 본다. 문서 간 중복은 "다른 문서 전체"와
대조해야 하므로 diff만으로는 원천적으로 불가능하다. 이 린터가 전역 대조를 결정적으로
수행해, 사람이 육안으로 하던 "이 내용이 다른 문서와 겹치나" 점검을 재현한다.

방법(claude/agy 리뷰 반영 — 한국어 특성):
  - 한국어는 교착어라 단어 n-gram이 조사 변화로 흔들린다 → **문자(char) 5-gram shingle** 사용.
  - 문단 쌍의 유사도 = Jaccard(shingle 집합). 임계 JACCARD_WARN(기본 0.7) 이상이면 경고.
  - 최소 길이 MIN_CHARS(기본 120자) 미만 문단은 제외(짧은 공통구·표제 오탐 방지).
  - `:::` aside(공통 주의/참고 블록)와 표·헤딩·리스트·코드펜스는 제외 — 의도적 반복이 많다.
  - BOILERPLATE_ALLOW: 의도적으로 반복되는 정형 문구(문서 기준 마커 등)는 명시 허용.

정책:
  - warn-only: exit 0(차단하지 않음). CI 정보성 경고로만 노출.
  - ko(SOT) 전용: 같은 로케일 내 문서 간 비교(번역본 en/ja는 원문 대응이라 제외).
  - baseline(옵션): 기존 중복 쌍 지문을 무시하고 신규만 표면화.

성능: 문단 후보를 MIN_CHARS로 선필터하고, 4-gram 프리픽스 버킷으로 후보쌍을 좁혀
      전수 비교(O(n^2))를 피한다. 코퍼스 규모(수천 문단)에서 수초 내.

사용법:
  python3 scripts/lint-duplication.py
  python3 scripts/lint-duplication.py --baseline .github/duplication-baseline.txt
  python3 scripts/lint-duplication.py --write-baseline .github/duplication-baseline.txt
"""
from __future__ import annotations

import argparse
import hashlib
import os
import re
import sys
from collections import defaultdict

DOCS_DIR = "src/content/docs/ko"

JACCARD_WARN = 0.7   # 유사도 경고 임계
MIN_CHARS = 120      # 이 미만 문단은 비교 제외
SHINGLE_K = 5        # 문자 n-gram 크기

# 의도적으로 여러 문서에 반복되는 정형 문구(중복으로 보고하지 않음).
BOILERPLATE_ALLOW = (
    "문서 기준: 2026년",
    "이 문서는 변동이 빠른 영역으로",
    "1P(직접)와 3P(클라우드 제공)의 차이",
)

LINK_RE = re.compile(r"\[([^\]]*)\]\([^)]*\)")
INLINE_CODE_RE = re.compile(r"`([^`]*)`")


def normalize(text: str) -> str:
    text = LINK_RE.sub(r"\1", text)
    text = INLINE_CODE_RE.sub(r"\1", text)
    # 공백·구두점 정규화(한국어 문자 위주 비교).
    text = re.sub(r"[\s]+", "", text)
    return text


def is_skippable(line: str) -> bool:
    s = line.lstrip()
    return (
        s.startswith("|") or s.startswith("#") or s.startswith(">")
        or s.startswith(":::") or s.startswith(("- ", "* ", "+ "))
        or re.match(r"^\d+\.\s", s) is not None
        or s.startswith("import ") or s.startswith("<") or s == "---"
    )


def paragraphs(md: str) -> list[str]:
    lines = md.split("\n")
    out: list[str] = []
    buf: list[str] = []
    in_fence = False
    in_frontmatter = False
    if lines and lines[0].strip() == "---":
        in_frontmatter = True
        lines = lines[1:]

    def flush():
        if buf:
            out.append(" ".join(x.strip() for x in buf))
            buf.clear()

    for raw in lines:
        s = raw.strip()
        if in_frontmatter:
            if s == "---":
                in_frontmatter = False
            continue
        if s.startswith("```"):
            in_fence = not in_fence
            flush()
            continue
        if in_fence:
            continue
        if not s:
            flush()
            continue
        if is_skippable(raw):
            flush()
            continue
        buf.append(raw)
    flush()
    return out


def shingles(norm: str, k: int = SHINGLE_K) -> frozenset[str]:
    if len(norm) < k:
        return frozenset({norm})
    return frozenset(norm[i:i + k] for i in range(len(norm) - k + 1))


def jaccard(a: frozenset[str], b: frozenset[str]) -> float:
    if not a or not b:
        return 0.0
    inter = len(a & b)
    if inter == 0:
        return 0.0
    return inter / len(a | b)


def is_boilerplate(para: str) -> bool:
    return any(bp in para for bp in BOILERPLATE_ALLOW)


def pair_fp(rel_a: str, rel_b: str, sa: str, sb: str) -> str:
    key = "|".join(sorted([f"{rel_a}:{sa[:40]}", f"{rel_b}:{sb[:40]}"]))
    return hashlib.sha256(key.encode("utf-8")).hexdigest()[:16]


def collect_units() -> list[tuple[str, str, frozenset[str]]]:
    """(rel, 원문문단, shingle집합) — MIN_CHARS 이상, 보일러플레이트 제외."""
    units = []
    for root, _, files in os.walk(DOCS_DIR):
        for f in sorted(files):
            if not f.endswith((".md", ".mdx")):
                continue
            abs_path = os.path.join(root, f)
            rel = os.path.relpath(abs_path, DOCS_DIR)
            with open(abs_path, encoding="utf-8") as fh:
                md = fh.read()
            for para in paragraphs(md):
                norm = normalize(para)
                if len(norm) < MIN_CHARS or is_boilerplate(para):
                    continue
                units.append((rel, para, shingles(norm)))
    return units


def find_duplicates(units) -> list[tuple[str, str]]:
    """(fingerprint, message) 목록. 프리픽스 버킷으로 후보쌍 축소 후 Jaccard 비교."""
    # 후보 축소: 각 유닛의 shingle 중 정렬 최소 4개를 버킷 키로 사용(공통 shingle 공유 시만 비교).
    buckets: dict[str, list[int]] = defaultdict(list)
    for i, (_, _, sh) in enumerate(units):
        for key in sorted(sh)[:4]:
            buckets[key].append(i)

    seen_pairs: set[tuple[int, int]] = set()
    results: list[tuple[str, str]] = []
    for idxs in buckets.values():
        if len(idxs) < 2:
            continue
        for a in range(len(idxs)):
            for b in range(a + 1, len(idxs)):
                i, j = idxs[a], idxs[b]
                if i == j or (i, j) in seen_pairs:
                    continue
                seen_pairs.add((i, j))
                rel_i, para_i, sh_i = units[i]
                rel_j, para_j, sh_j = units[j]
                if rel_i == rel_j:
                    continue  # 같은 문서 내 반복은 대상 아님(문서 간 중복만)
                sim = jaccard(sh_i, sh_j)
                if sim >= JACCARD_WARN:
                    fp = pair_fp(rel_i, rel_j, normalize(para_i), normalize(para_j))
                    results.append((fp,
                                    f"[duplication] {rel_i} ↔ {rel_j} — 유사도 {sim:.2f}"
                                    f"(>= {JACCARD_WARN}) — 공통화/링크 참조 검토\n"
                                    f"      A: {para_i[:70]}…\n"
                                    f"      B: {para_j[:70]}…"))
    return results


def load_baseline(path: str | None) -> set[str]:
    if not path or not os.path.isfile(path):
        return set()
    with open(path, encoding="utf-8") as fh:
        return {ln.strip() for ln in fh if ln.strip() and not ln.startswith("#")}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--baseline", default=None)
    ap.add_argument("--write-baseline", default=None)
    args = ap.parse_args()

    units = collect_units()
    dups = find_duplicates(units)

    if args.write_baseline:
        with open(args.write_baseline, "w", encoding="utf-8") as fh:
            fh.write("# duplication-baseline — 기존 중복 쌍 지문(신규만 표면화용). 자동생성.\n")
            for fp, _ in sorted(dups):
                fh.write(fp + "\n")
        print(f"✅ baseline 작성: {args.write_baseline} ({len(dups)} 쌍)")
        return 0

    baseline = load_baseline(args.baseline)
    new_dups = [(fp, msg) for fp, msg in dups if fp not in baseline]

    if not new_dups:
        suffix = " (baseline 제외 후)" if baseline else ""
        print(f"✅ 문서 간 중복 경고 없음{suffix} — {DOCS_DIR}")
        return 0

    print(f"⚠️  문서 간 중복 경고 {len(new_dups)}건(warn-only, 비차단)"
          + (f" — baseline {len(baseline)}건 제외" if baseline else "") + "\n")
    for _, msg in sorted(new_dups, key=lambda x: x[1]):
        print(f"  {msg}")
    print("\n참고: 경고는 차단하지 않습니다(exit 0). 의도적 반복은 상단 BOILERPLATE_ALLOW 또는 baseline으로 제외하세요.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
