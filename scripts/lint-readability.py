#!/usr/bin/env python3
"""
가독성 린트(warn-only) — 독자 난이도 이상치(초장문 문단·초장문 문장)를 경고한다.

배경: 편집 리뷰 워크플로의 LLM 축(reader difficulty)은 PR diff 범위만 본다. 이 린터는
전체 문서를 결정적으로 훑어, 사람이 육안으로 하던 "너무 어렵게/길게 쓰였나" 점검을
기계적으로 재현한다. AGENTS.md의 중립·명료 문체 원칙을 보조한다.

기준(코퍼스 실측 + claude/agy 리뷰 반영):
  - 문단 길이 >= PARA_WARN(기본 400자) → 경고. (코퍼스 p95≈290, 400자+는 소수 이상치)
  - 문장 길이 >= SENT_WARN(기본 150자)가 한 문서에서 SENT_MIN_HITS(기본 3)건 이상일 때만
    경고. (문장 p95≈140 — 단발 장문은 정상 범위라 문서당 다발일 때만 신호)

측정 정규화(오탐 최소화):
  - frontmatter(--- ... ---), 코드펜스(``` ... ```) 제외.
  - 표 행(| ...), 헤딩(#), 인용/aside(>, :::), 리스트 마커, import 라인 제외.
  - 링크 [텍스트](url) → 텍스트만, 인라인코드 `...` → 내용, 괄호 보조구 (…) 제거 후 길이 측정.

정책:
  - warn-only: 문제를 찾아도 exit 0(차단하지 않음). CI에서 정보성 경고로만 노출.
  - ko(SOT) 전용: 한국어 원문 기준. en/ja는 번역이라 별도 기준.
  - baseline(옵션): --baseline PATH 로 기존 이슈 지문을 무시하고 신규만 표면화.

사용법:
  python3 scripts/lint-readability.py
  python3 scripts/lint-readability.py --baseline .github/readability-baseline.txt
  python3 scripts/lint-readability.py --write-baseline .github/readability-baseline.txt
"""
from __future__ import annotations

import argparse
import hashlib
import os
import re
import sys

DOCS_DIR = "src/content/docs/ko"

PARA_WARN = 400      # 문단 길이 경고 임계(자)
SENT_WARN = 150      # 문장 길이 경고 임계(자)
SENT_MIN_HITS = 3    # 한 문서에서 장문 문장이 이 개수 이상일 때만 보고

LINK_RE = re.compile(r"\[([^\]]*)\]\([^)]*\)")   # [text](url) → text
INLINE_CODE_RE = re.compile(r"`([^`]*)`")         # `code` → code
PAREN_RE = re.compile(r"[（(][^（()）]*[)）]")      # (보조구) 제거(전각/반각)
SENT_SPLIT_RE = re.compile(r"(?<=[.。!?！?])\s+")


def normalize(text: str) -> str:
    """길이 측정 전 정규화 — 링크 URL·인라인코드 백틱·괄호 보조구를 제거."""
    text = LINK_RE.sub(r"\1", text)
    text = INLINE_CODE_RE.sub(r"\1", text)
    text = PAREN_RE.sub("", text)
    return " ".join(text.split())


def is_skippable(line: str) -> bool:
    """문단 후보에서 제외할 라인(표·헤딩·인용·aside·리스트·import·JSX·frontmatter 구분)."""
    s = line.lstrip()
    return (
        s.startswith("|")            # 표
        or s.startswith("#")         # 헤딩
        or s.startswith(">")         # 인용
        or s.startswith(":::")       # Starlight aside
        or s.startswith(("- ", "* ", "+ "))  # 리스트
        or re.match(r"^\d+\.\s", s) is not None  # 번호 리스트
        or s.startswith("import ")   # mdx import
        or s.startswith("<")         # JSX/HTML 컴포넌트(<CardGrid>, <LinkCard> 등) — 산문 아님
        or s == "---"                # frontmatter/구분선
    )


def paragraphs(md: str) -> list[str]:
    """코드펜스·frontmatter를 제외하고 빈 줄로 구분된 산문 문단만 추출."""
    lines = md.split("\n")
    out: list[str] = []
    buf: list[str] = []
    in_fence = False
    in_frontmatter = False
    # 선행 frontmatter 처리
    if lines and lines[0].strip() == "---":
        in_frontmatter = True
        lines = lines[1:]

    def flush():
        if buf:
            para = " ".join(x.strip() for x in buf)
            out.append(para)
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


def fingerprint(rel: str, kind: str, snippet: str) -> str:
    h = hashlib.sha256(f"{rel}|{kind}|{snippet[:80]}".encode("utf-8")).hexdigest()[:16]
    return h


def analyze(rel: str, md: str) -> list[tuple[str, str, str]]:
    """(fingerprint, message, kind) 목록 반환."""
    issues: list[tuple[str, str, str]] = []
    paras = paragraphs(md)
    long_sents = []
    for para in paras:
        norm = normalize(para)
        if len(norm) >= PARA_WARN:
            fp = fingerprint(rel, "para", norm)
            issues.append((fp,
                           f"[readability] {rel} — 문단 {len(norm)}자(>= {PARA_WARN}) "
                           f"— 소제목/표/짧은 문장으로 분할 검토: {norm[:60]}…", "para"))
        for s in SENT_SPLIT_RE.split(norm):
            s = s.strip()
            if len(s) >= SENT_WARN:
                long_sents.append(s)
    if len(long_sents) >= SENT_MIN_HITS:
        fp = fingerprint(rel, "sent", str(len(long_sents)))
        sample = long_sents[0][:60]
        issues.append((fp,
                       f"[readability] {rel} — 장문 문장 {len(long_sents)}개"
                       f"(각 >= {SENT_WARN}자, 문서당 {SENT_MIN_HITS}개 이상) "
                       f"— 문장 분할 검토: {sample}…", "sent"))
    return issues


def load_baseline(path: str | None) -> set[str]:
    if not path or not os.path.isfile(path):
        return set()
    with open(path, encoding="utf-8") as fh:
        return {ln.strip() for ln in fh if ln.strip() and not ln.startswith("#")}


def collect() -> list[tuple[str, str, str]]:
    all_issues: list[tuple[str, str, str]] = []
    for root, _, files in os.walk(DOCS_DIR):
        for f in sorted(files):
            if not f.endswith((".md", ".mdx")):
                continue
            abs_path = os.path.join(root, f)
            rel = os.path.relpath(abs_path, DOCS_DIR)
            with open(abs_path, encoding="utf-8") as fh:
                md = fh.read()
            all_issues.extend(analyze(rel, md))
    return all_issues


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--baseline", default=None, help="무시할 기존 이슈 지문 파일")
    ap.add_argument("--write-baseline", default=None, help="현재 이슈 지문을 파일로 저장")
    args = ap.parse_args()

    issues = collect()

    if args.write_baseline:
        with open(args.write_baseline, "w", encoding="utf-8") as fh:
            fh.write("# readability-baseline — 기존 이슈 지문(신규만 표면화용). 자동생성.\n")
            for fp, _, _ in sorted(issues):
                fh.write(fp + "\n")
        print(f"✅ baseline 작성: {args.write_baseline} ({len(issues)} 지문)")
        return 0

    baseline = load_baseline(args.baseline)
    new_issues = [(fp, msg, kind) for fp, msg, kind in issues if fp not in baseline]

    if not new_issues:
        suffix = " (baseline 제외 후)" if baseline else ""
        print(f"✅ 가독성 경고 없음{suffix} — {DOCS_DIR}")
        return 0

    print(f"⚠️  가독성 경고 {len(new_issues)}건(warn-only, 비차단)"
          + (f" — baseline {len(baseline)}건 제외" if baseline else "") + "\n")
    for _, msg, _ in sorted(new_issues, key=lambda x: x[1]):
        print(f"  {msg}")
    print("\n참고: 경고는 차단하지 않습니다(exit 0). 기준·정규화는 scripts/lint-readability.py 상단 주석 참고.")
    return 0  # warn-only: 항상 성공


if __name__ == "__main__":
    sys.exit(main())
