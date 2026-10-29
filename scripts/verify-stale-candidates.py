#!/usr/bin/env python3
"""
Stale 후보 검증 (2단계, council 합의 v1 — 제보 전용).

1단계(scan-stale-candidates.py)가 뽑은 HIGH/MEDIUM 후보를 받아, 문서 내 공식 출처와
'결정론적으로' 대조해 신뢰도를 매긴다. LLM·네트워크는 opt-in. 이 스크립트는 수정하지
않으며(auto_edit:false), status:verified 를 설정하지 않는다. exit 0(advisory).

council 합의(요약):
  - 문서 내 출처 우선: 후보 문단 링크 → 섹션 링크 → '## 참고하기'의 모든 https URL.
    fetch 상한 8건. URL 없으면 'not-checked' 행. (Gennai 교훈: 밖을 찾기 전에 안을 본다)
  - "unverified != stale": fetch 실패·근거 없음은 모순이 아니다. 토큰 미스 ≠ 모순,
    토큰 히트 ≠ 지지.
  - 판정:
      supports      = 날짜 + (문서와 같은) 상태가 ~200자 창에 공존, 부정어 없음 → 현행, 제외
      contradicted  = 같은 제품 맥락에 '반대 상태어'(Preview↔GA/종료) 공존 → 실제 현행화 필요
      unverified    = fetch 실패/근거 없음/URL 없음 → 보류(사람 판단)
  - LLM은 최후(opt-in): fetch 본문 존재 + 결정론 애매할 때만. 인용문은 발췌의 정확한
    부분문자열이어야 함(verifier_core.quote_is_substring)로 자동 단언.
  - 출력: contradicted 만 상세 행, supports 는 건수, unverified 는 '검사함/사람 필요'로 분리.
    1단계 HIGH 등급을 재사용하지 않는다.

사용법:
  python3 scripts/scan-stale-candidates.py --json > /tmp/cand.json
  python3 scripts/verify-stale-candidates.py --candidates /tmp/cand.json           # 오프라인(네트워크 없음): 출처 수집만
  python3 scripts/verify-stale-candidates.py --candidates /tmp/cand.json --fetch   # 공식 출처 fetch + 결정론 대조
  # --with-llm 은 애매 케이스에만(옵트인, 기본 off). REVIEWER_* 환경변수 필요.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EDITORIAL = os.path.join(os.path.dirname(HERE), ".editorial")
sys.path.insert(0, EDITORIAL)

import verifier_core as vc  # noqa: E402

FETCH_CAP = 8  # 런·후보당 fetch 상한


def read_doc(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def section_links_for(md_text, line_no):
    """후보 줄이 속한 섹션(가장 가까운 상위 ##/### 헤딩 블록)의 링크 + 문서 전체
    '## 참고하기' 링크를 캐스케이드 순서로 반환."""
    lines = md_text.splitlines()
    # 1) 후보 줄 자신의 링크
    cand_line = lines[line_no - 1] if 0 < line_no <= len(lines) else ""
    cascade = list(vc.extract_links(cand_line))

    # 2) 후보가 속한 섹션 블록의 링크
    start = 0
    for i in range(min(line_no, len(lines)) - 1, -1, -1):
        if re.match(r"^#{2,4}\s", lines[i]):
            start = i
            break
    end = len(lines)
    for i in range(line_no, len(lines)):
        if re.match(r"^#{2,4}\s", lines[i]):
            end = i
            break
    for u in vc.extract_links("\n".join(lines[start:end])):
        if u not in cascade:
            cascade.append(u)

    # 3) '## 참고하기' / 'References' 섹션 전체 링크
    refs = []
    in_ref = False
    for ln in lines:
        if re.match(r"^#{2,3}\s*(참고하기|참고|References|参考)", ln):
            in_ref = True
            continue
        if in_ref and re.match(r"^#{1,3}\s", ln):
            in_ref = False
        if in_ref:
            refs.append(ln)
    for u in vc.extract_links("\n".join(refs)):
        if u not in cascade:
            cascade.append(u)

    return cascade[:FETCH_CAP]


def classify(sentence, bodies):
    """결정론 판정. bodies: {url: text}. 반환: (verdict, evidence).

    보수적 규칙(council B·Gennai 교훈): 날짜 공존 없는 '본문에 GA 단어 있음'만으로는
    contradicted로 단정하지 않는다(같은 기사 내 다른 제품 맥락일 수 있음) — ambiguous로
    두어 LLM/사람에게 넘긴다. contradicted는 '같은 날짜 맥락'에서 반대 상태가 공존할 때만.
    """
    probes = vc.date_probes(sentence)
    doc_is_preview = bool(vc.PREVIEW_WORDS.search(sentence))

    # contradicted: 문서가 Preview인데 출처에서 같은 날짜 맥락에 GA/종료가 공존(강한 신호만)
    for url, body in bodies.items():
        if not body:
            continue
        if doc_is_preview and probes:
            for p in probes:
                if vc.cooccurs(body, p, vc.GA_WORDS) or vc.cooccurs(body, p, vc.RETIRED_WORDS):
                    return "contradicted", {"url": url, "probe": p}

    # supports: 날짜 + (문서 상태어와 같은 계열) 공존
    for url, body in bodies.items():
        if not body:
            continue
        status_re = vc.PREVIEW_WORDS if doc_is_preview else vc.GA_WORDS
        for p in probes:
            if vc.cooccurs(body, p, status_re):
                return "supports", {"url": url, "probe": p}

    # ambiguous: 날짜 공존은 없지만 본문에 반대 상태 신호가 존재 → LLM/사람 판단 필요(모순 아님)
    if doc_is_preview:
        for url, body in bodies.items():
            if body and (vc.GA_WORDS.search(vc.normalize(body)) or vc.RETIRED_WORDS.search(vc.normalize(body))):
                return "ambiguous", {"url": url, "probe": None}

    return "unverified", {}


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidates", required=True, help="scan-stale-candidates.py --json 출력")
    ap.add_argument("--fetch", action="store_true", help="문서 내 공식 출처를 실제로 fetch해 대조")
    ap.add_argument("--with-llm", action="store_true", help="애매 케이스만 LLM 판정(옵트인, 기본 off)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    if args.with_llm and not args.fetch:
        sys.stderr.write("[verify] --with-llm은 --fetch가 필요합니다(판정할 본문이 있어야 함). 무시합니다.\n")

    with open(args.candidates, encoding="utf-8") as fh:
        cand = json.load(fh)
    targets = (cand.get("high") or []) + (cand.get("medium") or [])

    fetch_source = None
    if args.fetch:
        import source_fetch as sf
        fetch_source = sf.fetch_source

    rows = []
    llm_calls = [0]  # 런당 LLM 호출 수(상한 vc.MAX_LLM_CALLS)
    for c in targets:
        path, line, sent = c["path"], c["line"], c["excerpt"]
        md = read_doc(path)
        links = section_links_for(md, line)
        bodies, fetched_urls, fetch_errors = {}, [], []
        if args.fetch and links:
            for u in links:
                try:
                    r = fetch_source(u)
                    bodies[u] = getattr(r, "text_sample", "") or ""
                    fetched_urls.append(u)
                except Exception as e:  # noqa: BLE001 — fetch 실패는 unverified로
                    fetch_errors.append(f"{u}: {type(e).__name__}")
        verdict, ev = classify(sent, bodies) if bodies else ("unverified", {})

        # ambiguous → LLM 3진 판정(opt-in, council D). fetch 본문이 있을 때만, 런당 상한.
        llm = None
        if verdict == "ambiguous" and args.with_llm and args.fetch:
            if llm_calls[0] < vc.MAX_LLM_CALLS:
                url = ev.get("url")
                body = bodies.get(url, "")
                if body:
                    llm_calls[0] += 1
                    llm = vc.llm_adjudicate(sent, body)
                    # LLM이 모순이라 하고 인용도 발췌의 부분문자열이면 contradicted로 승격.
                    # 지지/언급없음/에러/인용 불일치는 ambiguous 유지(과신 금지).
                    if llm.get("verdict") == "contradicts" and llm.get("quote_ok"):
                        verdict, ev = "contradicted", {"url": url, "probe": ev.get("probe"),
                                                       "llm_quote": llm.get("quote")}
                    elif llm.get("verdict") == "supports" and llm.get("quote_ok"):
                        verdict, ev = "supports", {"url": url, "llm_quote": llm.get("quote")}
            else:
                llm = {"verdict": "skipped", "error": "per-run LLM call cap reached"}

        # unverified 세분화(council E): 검사함(URL 있었고 fetch함) vs 사람이 출처 찾아야(URL 없음)
        sub = None
        if verdict == "unverified":
            if not links:
                sub = "needs-human-source-hunt"   # 문서에 출처 링크 없음
            elif not args.fetch:
                sub = "not-fetched (오프라인 모드)"
            else:
                sub = "checked-inconclusive"       # fetch했으나 결론 못 냄
        rows.append({
            "path": path, "line": line, "excerpt": sent,
            "verdict": verdict, "sub": sub, "evidence": ev,
            "examined_urls": links, "fetched": fetched_urls, "fetch_errors": fetch_errors,
            "llm": llm,
            "auto_edit": False, "status": "advisory",   # 절대 verified 아님
        })

    contradicted = [r for r in rows if r["verdict"] == "contradicted"]
    ambiguous = [r for r in rows if r["verdict"] == "ambiguous"]
    supports = [r for r in rows if r["verdict"] == "supports"]
    unverified = [r for r in rows if r["verdict"] == "unverified"]

    if args.json:
        print(json.dumps({
            "summary": {"contradicted": len(contradicted), "ambiguous": len(ambiguous),
                        "supports": len(supports), "unverified": len(unverified),
                        "fetched": args.fetch},
            "contradicted": contradicted, "ambiguous": ambiguous, "unverified": unverified,
            "supports_count": len(supports),
        }, ensure_ascii=False, indent=2))
        return 0

    print("# Stale 후보 검증 (2단계, 결정론 — advisory)\n")
    print(f"입력 후보: {len(rows)}  |  contradicted={len(contradicted)}  ambiguous={len(ambiguous)}  "
          f"supports={len(supports)}  unverified={len(unverified)}  (fetch={'on' if args.fetch else 'off'})\n")
    print("※ 'unverified ≠ stale'. 출처를 못 찾았거나 결론 못 낸 것은 모순이 아니다. 수정은 사람/에이전트의 패킷 PR로.\n")

    if contradicted:
        print("## contradicted — 공식 출처가 문서 서술과 같은 날짜 맥락에서 모순 (실제 현행화 유력)\n")
        for r in contradicted:
            print(f"- {r['path']}:{r['line']}  ← {r['evidence'].get('url')} (날짜 {r['evidence'].get('probe')})")
            print(f"    {r['excerpt']}")
        print()
    if ambiguous:
        print("## ambiguous — 출처에 반대 상태 신호가 있으나 같은 날짜 맥락 아님 (LLM/사람 판단 필요, 모순 단정 금지)\n")
        for r in ambiguous:
            print(f"- {r['path']}:{r['line']}  ← {r['evidence'].get('url')}")
            print(f"    {r['excerpt'][:90]}")
        print()
    print(f"## supports — 출처가 현행 서술을 뒷받침: {len(supports)}건 (제외)\n")
    if unverified:
        print("## unverified — 보류 (모순 아님)\n")
        human = [r for r in unverified if r["sub"] == "needs-human-source-hunt"]
        checked = [r for r in unverified if r["sub"] != "needs-human-source-hunt"]
        if human:
            print(f"### 사람이 출처를 찾아야 함 (문서에 공식 링크 없음): {len(human)}건")
            for r in human:
                print(f"- {r['path']}:{r['line']}  {r['excerpt'][:80]}")
        if checked:
            print(f"### 검사했으나 결론 못 냄: {len(checked)}건")
            for r in checked:
                print(f"- {r['path']}:{r['line']}  (검사 URL {len(r['examined_urls'])}개)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
