#!/usr/bin/env python3
"""
검증 공통 헬퍼 (stale 스캔 2단계 전용, council 합의 F항).

원칙:
  - editorial-review 게이트 러너(run_review_gate.py)는 재사용하지 않는다. 그 게이트의
    approve/changes_requested verdict과 'fetch 실패 → PR 보류' 시맨틱은 exit-0 advisory
    스캔과 충돌한다. 공유는 이 작은 인용/대조 헬퍼까지만.
  - source_fetch.fetch_source 는 import해 재사용(SSRF 방어·상한). 텍스트 추출은 opt-in.
  - 절대 status:verified 를 쓰지 않는다. 이 모듈은 '제보용 신호'만 만든다.
"""
from __future__ import annotations

import re
import unicodedata

# 상태 전이 어휘: 문서가 "Preview"인데 출처에 이런 말이 있으면 모순(contradicted) 후보.
GA_WORDS = re.compile(r"(generally\s+available|\bGA\b|정식\s*출시|一般提供|正式提供|제공\s*개시)", re.IGNORECASE)
RETIRED_WORDS = re.compile(r"(retired|deprecated|end\s+of\s+(life|support)|종료|지원\s*중단|폐지|廃止|提供終了)", re.IGNORECASE)
PREVIEW_WORDS = re.compile(r"(preview|beta|프리뷰|베타|プレビュー|ベータ)", re.IGNORECASE)

# 부정어(가까이 있으면 supports 판정을 무효화).
NEGATION = re.compile(r"(not|아직\s*아님|아닙니다|없|되지\s*않|예정에\s*없|ない|ではない)", re.IGNORECASE)

WINDOW = 200  # 공존 판정 창(문자)


def normalize(s: str) -> str:
    """NFKC 정규화 + 공백 축약(대조 안정화)."""
    s = unicodedata.normalize("NFKC", s)
    return re.sub(r"\s+", " ", s).strip()


def date_probes(sentence: str) -> list[str]:
    """문장에서 뽑은 날짜를 출처에서 찾기 위한 다국어 프로브 문자열 목록.
    예: '2026년 9월' -> ['2026-09','2026/9','2026年9月','September 2026', ...]
    """
    probes: list[str] = []
    months_en = ["January","February","March","April","May","June",
                 "July","August","September","October","November","December"]
    for m in re.finditer(r"(\d{4})\s*년?\s*(\d{1,2})?\s*월?", sentence):
        y = m.group(1)
        mo = m.group(2)
        if not y:
            continue
        probes.append(y)
        if mo:
            mo_i = int(mo)
            probes += [f"{y}-{mo_i:02d}", f"{y}/{mo_i}", f"{y}年{mo_i}月", f"{months_en[mo_i-1]} {y}"]
    # 중복 제거(순서 보존)
    seen, out = set(), []
    for p in probes:
        if p not in seen:
            seen.add(p); out.append(p)
    return out


def cooccurs(body: str, probe: str, status_re, window: int = WINDOW) -> bool:
    """출처 본문에서 probe(날짜 등)와 status 단어가 window 내에 공존하고
    부정어가 끼지 않으면 True."""
    nb = normalize(body)
    for m in re.finditer(re.escape(normalize(probe)), nb):
        lo = max(0, m.start() - window)
        hi = min(len(nb), m.end() + window)
        seg = nb[lo:hi]
        if status_re.search(seg) and not NEGATION.search(seg):
            return True
    return False


def quote_is_substring(quote: str, excerpts: list[str]) -> bool:
    """LLM이 반환한 인용문이 실제 fetch 발췌의 '정확한 부분문자열'인지 자동 검증.
    council D항: 인용 필수만으론 불충분 — 이 결정론적 단언이 동반돼야 한다."""
    nq = normalize(quote)
    if len(nq) < 8:
        return False
    return any(nq in normalize(e) for e in excerpts)


def extract_links(md_text: str) -> list[str]:
    """마크다운에서 https URL 추출(참고하기/인라인 공통)."""
    urls = re.findall(r"\((https://[^)\s]+)\)", md_text)
    urls += re.findall(r"<(https://[^>\s]+)>", md_text)
    seen, out = set(), []
    for u in urls:
        u = u.rstrip(".,)")
        if u not in seen:
            seen.add(u); out.append(u)
    return out
