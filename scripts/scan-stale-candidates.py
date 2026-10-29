#!/usr/bin/env python3
"""
Stale 후보 스캐너 (결정론적 1차 필터) — council 합의안 v1 (추출 단계 PoC).

목적:
  월간 리뷰가 whats-new(= '무엇이 새로 나왔나')는 자동 수집하지만, 기존 문서에 이미
  박힌 '낡았을 수 있는 서술'(예: 1년 전 'X는 Preview'가 이미 GA)은 사람이 체크리스트로
  수동으로 훑는 데 의존한다. 이 스크립트는 ko(SOT) 전체를 결정론적으로 스캔해
  "현행성이 의심되는 후보 문장"만 뽑아 '제보'한다. 자동 편집·판정은 하지 않는다.

council 합의 원칙 반영:
  - ko/ 만 스캔(en/ja는 ko 교정이 승인된 뒤 팩트 PR에서 따라감).
  - 결정론적(정규식/날짜) 1차 필터만. LLM·네트워크 호출 없음(이 PoC 범위).
  - "매칭 없음 = 최신"이 아니다. 이 스크립트는 후보만 제시하고, stale 단정은 하지 않는다.
    등급은 의심의 '강도'일 뿐이며, 실제 검증(공식 출처 대조)은 다음 단계/사람의 몫.
  - 노이즈 억제: HIGH/MEDIUM만 상세 행으로, LOW는 건수 요약.
  - 코드펜스·역사적 서술·미래(마커 이후) 일정은 제외.

등급(council 조정판):
  - HIGH   : 문서 기준 마커보다 '과거'인데 아직 "예정/planned"으로 남은 일정.
             (가장 확실한 stale 신호 — 과거가 미래형으로 서술됨)
  - MEDIUM : Preview/Beta/프리뷰/리서치 프리뷰 등 상태어(연혁 서술 제외).
  - LOW    : 맨 가격($x)·리전 수·가용영역 수 등 변동성 높은 수치. 건수만 요약.

사용법:
  python3 scripts/scan-stale-candidates.py            # 사람용 텍스트 리포트
  python3 scripts/scan-stale-candidates.py --json     # 머신리더블(JSON)
  python3 scripts/scan-stale-candidates.py --max-month 2026-10   # 마커 못 읽을 때 기준월 강제

주의:
  - exit code는 항상 0(advisory). CI를 실패시키지 않는다.
  - 억제: 문장에 `<!-- stale-ignore: 사유 -->` 가 같은 줄/직전 줄에 있으면 제외.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

DOCS_KO = "src/content/docs/ko"

# 문서 기준 마커: "> 문서 기준: 2026년 10월"
MARKER_RE = re.compile(r">\s*문서\s*기준:\s*(\d{4})년\s*(\d{1,2})월")

# 억제 주석
IGNORE_RE = re.compile(r"<!--\s*stale-ignore:")

# ── 후보 룰 ────────────────────────────────────────────────────────────────
# 상태어(MEDIUM). "GA/정식 출시" 맥락, "Preview → GA" 연혁 화살표는 호출부에서 제외.
STATUS_RE = re.compile(
    r"(리서치\s*프리뷰|퍼블릭\s*프리뷰|프리뷰|Public\s+Preview|Technical\s+Preview|Research\s+Preview|Preview|베타|Beta)",
    re.IGNORECASE,
)

# "예정" 일정(HIGH 후보). 문장에서 YYYY년 (M월|상·하반기|Q분기)를 함께 뽑는다.
PLANNED_RE = re.compile(r"(출시\s*예정|발효\s*예정|시행\s*예정|도입\s*예정|적용\s*예정|예정|planned|upcoming)")
DATE_IN_SENTENCE_RE = re.compile(r"(\d{4})년(?:\s*(\d{1,2})월)?")

# 완료형(이미 일어난 일) 신호 — 있으면 "예정"이 아니라 과거 서술이므로 HIGH 제외.
COMPLETED_RE = re.compile(
    r"(되었습니다|됐습니다|되었다|했습니다|발효되|출시되|시행되|완료|공개했|발표했|GA(되|\s*전환)|정식\s*출시)"
)

# LOW: 맨 가격·리전/가용영역 수
PRICE_RE = re.compile(r"\$\s?\d[\d,]*(?:\.\d+)?")
COUNT_RE = re.compile(r"\d+\s*개\s*(리전|가용\s*영역|AZ|리전을|가용영역)")

# 역사적/연혁 서술 제외 신호(상태어가 '과거 사건'을 설명하는 경우).
# 예: "2026.02 Technical Preview → 2026.06 Public Preview", "2026년 8월 … 프리뷰를 공개했습니다"
HISTORY_HINT_RE = re.compile(r"(→|->|공개했|출시했|발표했|되었|전환|거쳐|이후\s*GA|GA\s*전환)")

# 상태어가 '후보가 아닌' 메타/범례/면책 서술인 경우 제외.
#   - 범례:  "✅ GA = 정식 출시, 🔶 프리뷰 = 미리보기"
#   - 면책:  "Preview/GA는 공식 문서 확인", "상태는 … 확인"
#   - 메타:  "GA/Preview 상태 등 빠르게 바뀌는 정보"(방법론 설명)
STATUS_META_RE = re.compile(
    r"(=\s*(정식\s*출시|미리보기)|공식\s*문서(에서)?\s*확인|상태\s*등|상태는|상태를\s*확인|"
    r"현행\s*출시\s*단계를\s*확인|빠르게\s*바뀌는|Preview/GA|GA/Preview|세대·변형)"
)


def read_marker_month(text: str):
    m = MARKER_RE.search(text)
    if not m:
        return None
    return int(m.group(1)), int(m.group(2))


def strip_code_fences(lines):
    """코드펜스(```) 내부 라인을 (line_no, text)에서 제외."""
    out, in_fence = [], False
    for i, raw in enumerate(lines, 1):
        if raw.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            out.append((i, raw))
    return out


def ym_tuple(y, mo):
    return (y, mo if mo else 1)


def scan_file(path, default_month):
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    marker = read_marker_month(text) or default_month
    lines = text.splitlines()
    kept = strip_code_fences(lines)

    findings = []
    for ln, raw in kept:
        line = raw.strip()
        if not line or line.startswith(("|---", "---")):
            continue
        if IGNORE_RE.search(raw):
            continue

        # HIGH: 마커보다 과거인데 "예정"으로 남은 일정.
        #   false positive 방지:
        #   - 완료형("발효되었습니다" 등)이 있으면 과거 서술이므로 제외.
        #   - 문장에 여러 날짜가 섞일 수 있으므로, "예정" 토큰과 '가장 가까운' 날짜만 평가.
        if marker and PLANNED_RE.search(line) and not COMPLETED_RE.search(line):
            planned_pos = PLANNED_RE.search(line).start()
            nearest = None
            for dm in DATE_IN_SENTENCE_RE.finditer(line):
                dist = abs(dm.start() - planned_pos)
                if nearest is None or dist < nearest[0]:
                    y = int(dm.group(1))
                    mo = int(dm.group(2)) if dm.group(2) else None
                    nearest = (dist, y, mo)
            if nearest and ym_tuple(nearest[1], nearest[2]) < ym_tuple(*marker):
                findings.append(("HIGH", "planned-past", ln, line))

        # MEDIUM: 상태어(연혁/과거 서술·메타/범례/면책 제외)
        if (STATUS_RE.search(line)
                and not HISTORY_HINT_RE.search(line)
                and not STATUS_META_RE.search(line)):
            findings.append(("MEDIUM", "status-word", ln, line))

        # LOW: 가격/리전 수 (건수만 집계용)
        if PRICE_RE.search(line) or COUNT_RE.search(line):
            findings.append(("LOW", "volatile-number", ln, line))

    return marker, findings


def excerpt(s, n=140):
    s = re.sub(r"\s+", " ", s).strip()
    return s if len(s) <= n else s[: n - 1] + "…"


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--max-month", default=None, help="마커 폴백 기준월 YYYY-MM")
    ap.add_argument("--root", default=DOCS_KO)
    args = ap.parse_args(argv)

    default_month = None
    if args.max_month:
        y, mo = args.max_month.split("-")
        default_month = (int(y), int(mo))

    results = []
    for root, _, files in os.walk(args.root):
        for f in sorted(files):
            if not f.endswith((".md", ".mdx")):
                continue
            p = os.path.join(root, f)
            marker, findings = scan_file(p, default_month)
            for level, rule, ln, line in findings:
                results.append({
                    "path": os.path.relpath(p),
                    "line": ln,
                    "level": level,
                    "rule": rule,
                    "marker": f"{marker[0]}-{marker[1]:02d}" if marker else None,
                    "excerpt": excerpt(line),
                })

    high = [r for r in results if r["level"] == "HIGH"]
    med = [r for r in results if r["level"] == "MEDIUM"]
    low = [r for r in results if r["level"] == "LOW"]

    if args.json:
        print(json.dumps({
            "summary": {"high": len(high), "medium": len(med), "low": len(low),
                        "files_with_low": len({r["path"] for r in low})},
            "high": high, "medium": med,
            "low_count_by_path": _count_by_path(low),
        }, ensure_ascii=False, indent=2))
        return 0

    # 사람용 텍스트 리포트
    print("# Stale 후보 스캔 (ko, 결정론적 1차 필터 — advisory)\n")
    print(f"HIGH={len(high)}  MEDIUM={len(med)}  LOW={len(low)}"
          f"  (LOW는 {len({r['path'] for r in low})}개 문서)\n")
    print("※ '매칭 없음 = 최신'이 아님. 후보는 의심 신호일 뿐, 공식 출처 대조는 다음 단계/사람 몫.\n")

    if high:
        print("## HIGH — 마커보다 과거인데 '예정'으로 남은 일정\n")
        for r in high:
            print(f"- [{r['marker']}] {r['path']}:{r['line']}\n    {r['excerpt']}")
        print()
    if med:
        print("## MEDIUM — Preview/Beta 등 상태어 (연혁 서술 제외)\n")
        for r in med:
            print(f"- {r['path']}:{r['line']}\n    {r['excerpt']}")
        print()
    if low:
        print("## LOW — 변동 수치(가격·리전 수): 건수 요약만\n")
        for path, c in sorted(_count_by_path(low).items(), key=lambda x: -x[1]):
            print(f"- {path}: {c}건")
    return 0


def _count_by_path(rows):
    out = {}
    for r in rows:
        out[r["path"]] = out.get(r["path"], 0) + 1
    return out


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
