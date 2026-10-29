#!/usr/bin/env python3
"""
레벨링 후보 선별 스캐너 (축4, council v1 5단계 — 제보 전용).

117문서 전체를 LLM으로 순회하는 건 비용·과신이므로 금지. 이 결정론 스캐너가 먼저
'레벨링이 필요해 보이는' ko 문서를 점수화해 월 N개(leveling-rules.yaml traversal)만
LLM 교정 대상으로 shortlist 한다. 봇은 제보만(advisory, exit 0).

점수 신호(결정론):
  - 미확정 서술(확인필요/미정/TBD/조사 필요): 실측상 가장 깨끗한 축4 신호(가중 ↑).
  - 가독성: soft/hard 문장 길이 초과 문장 수(leveling-rules.yaml readability).
  - 과대 문단: 매우 긴 문단 수(한 문단이 한 호흡에 안 읽힘).
우선순위 = 미확정 서술 + 가독성 + 과대 문단. 길이 자체는 보조 신호.

주의: 이 스캐너는 '교정하지 않는다'. shortlist만 제보하고, 실제 교정은 레벨링 엔진이
결정론 가드 + 의미보존 리뷰 + 사람 승인 경로로 수행한다(AGENTS.md 축4 예외).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

DOCS_KO = "src/content/docs/ko"
RULES = ".editorial/leveling-rules.yaml"

UNCERTAIN = re.compile(r"(확인이?\s*필요|확인\s*필요|미정|TBD|조사\s*필요|추가\s*확인|미확정)")
PARA_LONG_CHARS = 600   # 과대 문단(산문) 기준


def load_thresholds(path=RULES):
    soft, hard = 80, 120
    try:
        with open(path, encoding="utf-8") as fh:
            t = fh.read()
        ms = re.search(r"sentence_chars_soft:\s*(\d+)", t)
        mh = re.search(r"sentence_chars_hard:\s*(\d+)", t)
        if ms:
            soft = int(ms.group(1))
        if mh:
            hard = int(mh.group(1))
    except OSError:
        pass
    return soft, hard


def strip_blocks(text):
    """코드펜스·표를 제거한 산문만."""
    body = re.sub(r"```.*?```", "", text, flags=re.S)
    body = "\n".join(ln for ln in body.splitlines() if not ln.lstrip().startswith(("|", "#", ">")))
    return body


def sentences(prose):
    # 한국어 문장 분리(마침표·물음표·느낌표 + 줄바꿈). 러프하지만 길이 신호용으로 충분.
    parts = re.split(r"(?<=[.!?。])\s+|\n{2,}", prose)
    return [s.strip() for s in parts if s.strip()]


def paragraphs(prose):
    return [p.strip() for p in re.split(r"\n\s*\n", prose) if p.strip()]


def scan_file(path, soft, hard):
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    prose = strip_blocks(text)
    sents = sentences(prose)
    paras = paragraphs(prose)

    uncertain = len(UNCERTAIN.findall(text))
    soft_over = sum(1 for s in sents if len(s) > soft)
    hard_over = sum(1 for s in sents if len(s) > hard)
    long_paras = sum(1 for p in paras if len(p) > PARA_LONG_CHARS)

    # 점수: 미확정 서술(×3) + hard 초과 문장(×2) + 과대 문단(×2) + soft 초과(×1)
    score = uncertain * 3 + hard_over * 2 + long_paras * 2 + soft_over
    return {
        "path": os.path.relpath(path),
        "score": score,
        "uncertain": uncertain,
        "sent_soft_over": soft_over,
        "sent_hard_over": hard_over,
        "long_paragraphs": long_paras,
    }


def load_top_n(path=RULES, default=8):
    try:
        with open(path, encoding="utf-8") as fh:
            m = re.search(r"llm_docs_per_month:\s*(\d+)", fh.read())
        return int(m.group(1)) if m else default
    except OSError:
        return default


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=DOCS_KO)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--top", type=int, default=None, help="shortlist 크기(기본 rules의 llm_docs_per_month)")
    args = ap.parse_args(argv)

    soft, hard = load_thresholds()
    top_n = args.top if args.top is not None else load_top_n()

    rows = []
    for dirpath, _, files in os.walk(args.root):
        for f in sorted(files):
            if f.endswith((".md", ".mdx")):
                rows.append(scan_file(os.path.join(dirpath, f), soft, hard))
    rows.sort(key=lambda r: -r["score"])
    shortlist = [r for r in rows if r["score"] > 0][:top_n]

    if args.json:
        print(json.dumps({
            "thresholds": {"soft": soft, "hard": hard, "top_n": top_n},
            "shortlist": shortlist,
            "total_scored": sum(1 for r in rows if r["score"] > 0),
        }, ensure_ascii=False, indent=2))
        return 0

    print("# 레벨링 후보 선별 (축4, 결정론 · 제보 전용)\n")
    print(f"문장 길이 soft/hard={soft}/{hard}, shortlist 상위 {top_n}개 "
          f"(점수>0 문서 {sum(1 for r in rows if r['score']>0)}개 중)\n")
    print("※ 교정하지 않음 — shortlist만 제보. 실제 교정은 결정론 가드+의미보존 리뷰+사람 승인 경로.\n")
    print("| # | 문서 | 점수 | 미확정 | 긴문장(hard) | 과대문단 |")
    print("| --- | --- | --- | --- | --- | --- |")
    for i, r in enumerate(shortlist, 1):
        p = r["path"].replace("src/content/docs/ko/", "")
        print(f"| {i} | `{p}` | {r['score']} | {r['uncertain']} | {r['sent_hard_over']} | {r['long_paragraphs']} |")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
