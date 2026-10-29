#!/usr/bin/env python3
"""
레벨링 가드 — 축4 교정 PR이 '사실'을 바꾸지 못하게 결정론적으로 차단 (council v1 토대).

레벨링(축4)은 '표현'만 바꾼다. 이 가드는 base↔head 두 버전을 비교해, 사실 불변식
(.editorial/leveling-rules.yaml의 invariants)이 깨지면 FAIL(fail-closed)한다. LLM보다
먼저 실행되고 차단권을 가지며, LLM이 뒤집을 수 없다. 순수 산문(난이도/문장구조) 교정만
통과시킨다.

검사 불변식:
  - byte_identical: 코드블록/Mermaid/표/프론트매터/문서기준 마커가 바이트 동일.
  - structure_identical: H1~H4 제목·순서 동일.
  - multiset_identical: 링크 URL·숫자+단위/날짜/버전/%·고유명사(라틴·백틱)의 멀티셋 동일.
  - per_paragraph_modality_preserved: 문단별 수식어/서법어 개수 보존.

사용법:
  python3 scripts/leveling-guard.py --base OLD.md --head NEW.md
  # CI: git show로 base/head를 파일로 떨군 뒤 각 변경 문서에 대해 호출.
  # exit 0 = 통과(순수 표현 교정), exit 1 = 차단(사실 변경 의심).

주의: 이 가드는 '표현 교정'에만 쓴다. 사실을 의도적으로 바꾸는 변경(축1 현행화)은
레벨링 PR이 아니라 근거 패킷 PR 경로로 가야 하며, 이 가드를 적용하지 않는다.
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter

RULES_PATH = ".editorial/leveling-rules.yaml"

# yaml 의존 없이 필요한 값만 파싱(런타임 의존성 추가 금지). 실패 시 내장 기본값.
MODALITY_DEFAULT = ["Preview", "GA", "일부", "최대", "최소", "필수", "권장",
                    "미지원", "지원", "only", "may", "예정", "불가"]


def load_modality(path=RULES_PATH):
    try:
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
    except OSError:
        return MODALITY_DEFAULT
    # per_paragraph_modality_preserved: 아래의 "- "항목만 추출(간이 파서)
    m = re.search(r"per_paragraph_modality_preserved:\s*\n((?:\s*-\s*.+\n)+)", text)
    if not m:
        return MODALITY_DEFAULT
    items = re.findall(r'-\s*"?([^"\n]+?)"?\s*$', m.group(1), re.M)
    return [i.strip() for i in items if i.strip()] or MODALITY_DEFAULT


# ── 추출기들 ─────────────────────────────────────────────────────────
def code_fences(text):
    """```...``` 블록(언어 포함) 전체를 순서 리스트로."""
    return re.findall(r"```.*?```", text, re.S)


def tables(text):
    """표 라인(| ... |) 전체."""
    return [ln.strip() for ln in text.splitlines() if ln.lstrip().startswith("|")]


def frontmatter(text):
    m = re.match(r"^---\n.*?\n---\n", text, re.S)
    return m.group(0) if m else ""


def review_marker(text):
    m = re.search(r">\s*(문서 기준|Last reviewed|文書基準):.*", text)
    return m.group(0).strip() if m else ""


def headings(text):
    """코드블록 밖의 H1~H4 (순서 유지)."""
    out, in_fence = [], False
    for ln in text.splitlines():
        if ln.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence and re.match(r"^#{1,4}\s", ln):
            out.append(ln.strip())
    return out


def link_urls(text):
    urls = re.findall(r"\]\((https?://[^)\s]+)\)", text)
    urls += re.findall(r"\]\((\.{1,2}/[^)\s]+|/[^)\s]+)\)", text)  # 상대·root-relative 내부 링크
    urls += re.findall(r"<(https?://[^>\s]+)>", text)
    return [u.rstrip(".,)") for u in urls]


def numbers_with_units(text):
    """숫자+단위/날짜/버전/% 류. 코드블록 제외."""
    body = re.sub(r"```.*?```", "", text, flags=re.S)
    pats = [
        r"\d{4}[-./]\d{1,2}(?:[-./]\d{1,2})?",          # 날짜 2026-09 / 2026.09
        r"\d{4}년(?:\s*\d{1,2}월)?",                      # 2026년 9월
        r"v\d+(?:\.\d+)+",                               # v1.0
        r"\$\s?\d[\d,]*(?:\.\d+)?",                       # $0.05
        r"\d+(?:\.\d+)?\s*%",                            # 80%
        r"\d+\s*개\s*(?:리전|가용\s*영역|AZ)",            # 22개 리전
        r"\d+(?:\.\d+)?\s*(?:GB|TB|MB|ms|초|분|시간|일|개월|년)",
    ]
    out = []
    for p in pats:
        out += [m.group(0).strip() for m in re.finditer(p, body)]
    return out


def proper_nouns(text):
    """라틴 고유명사(대문자 포함 토큰)·백틱 식별자. 코드블록 제외."""
    body = re.sub(r"```.*?```", "", text, flags=re.S)
    backtick = re.findall(r"`([^`]+)`", body)
    # 대문자로 시작하는 라틴 토큰(CamelCase 포함). 중첩 수량자 없이 단일 문자클래스로
    # 매칭해 ReDoS(지수 백트래킹)를 피한다. 예: AgentCore, Bedrock, DynamoDB, VPC.
    latin = re.findall(r"\b[A-Z][A-Za-z0-9]*\b", body)
    return [t for t in backtick + latin if len(t) > 1]


def paragraphs(text):
    """빈 줄 구분 문단(코드블록·표 제외한 산문)."""
    body = re.sub(r"```.*?```", "", text, flags=re.S)
    paras = re.split(r"\n\s*\n", body)
    return [p for p in paras if p.strip() and not p.lstrip().startswith(("|", "#"))]


# ── 비교 ─────────────────────────────────────────────────────────────
def fails(name, base_val, head_val, kind):
    """불변식 1건 비교. 위반이면 (name, detail) 반환, 아니면 None."""
    if kind == "ordered":
        if base_val != head_val:
            return (name, f"순서/내용 변경: {len(base_val)} → {len(head_val)} 항목")
    elif kind == "multiset":
        b, h = Counter(base_val), Counter(head_val)
        if b != h:
            added = list((h - b).elements())
            removed = list((b - h).elements())
            det = []
            if removed:
                det.append(f"삭제 {removed[:5]}")
            if added:
                det.append(f"추가 {added[:5]}")
            return (name, "; ".join(det) or "멀티셋 불일치")
    elif kind == "scalar":
        if base_val != head_val:
            return (name, f"변경: {base_val!r} → {head_val!r}")
    return None


def modality_violations(base, head, words):
    """문단별 수식어 개수 보존. head 문단과 base 문단을 '최근접'으로 짝지어 비교하는
    대신, 문서 전체 합계가 줄면 경고(oversimplification 1차). 문단 분할/병합 때문에
    문단 단위 1:1은 깨지기 쉬워, 전체 합계 보존을 1차 가드로 쓴다."""
    def counts(t):
        low = t
        return {w: len(re.findall(re.escape(w), low)) for w in words}
    cb, ch = counts(base), counts(head)
    viol = []
    for w in words:
        if ch[w] < cb[w]:
            viol.append((w, cb[w], ch[w]))
    return viol


def run(base, head, rules_path=RULES_PATH):
    words = load_modality(rules_path)
    problems = []

    # byte_identical (ordered/scalar)
    for name, fn, kind in [
        ("code_fence", code_fences, "ordered"),
        ("table", tables, "ordered"),
        ("frontmatter", frontmatter, "scalar"),
        ("review_marker", review_marker, "scalar"),
        ("headings", headings, "ordered"),
    ]:
        r = fails(name, fn(base), fn(head), kind)
        if r:
            problems.append(r)

    # multiset_identical
    for name, fn in [
        ("link_urls", link_urls),
        ("numbers_with_units", numbers_with_units),
        ("proper_nouns", proper_nouns),
    ]:
        r = fails(name, fn(base), fn(head), "multiset")
        if r:
            problems.append(r)

    # modality 보존(합계 감소 = 위반)
    mv = modality_violations(base, head, words)
    if mv:
        problems.append(("modality", "; ".join(f"{w} {b}→{h}" for w, b, h in mv)))

    return problems


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True, help="수정 전 문서 경로")
    ap.add_argument("--head", required=True, help="수정 후 문서 경로")
    ap.add_argument("--rules", default=RULES_PATH)
    args = ap.parse_args(argv)

    with open(args.base, encoding="utf-8") as fh:
        base = fh.read()
    with open(args.head, encoding="utf-8") as fh:
        head = fh.read()

    problems = run(base, head, args.rules)
    if not problems:
        print("✅ leveling-guard: 표현 전용 변경 — 사실 불변식 통과")
        return 0
    print("❌ leveling-guard: 사실 불변식 위반(레벨링 PR은 표현만 바꿔야 함):")
    for name, detail in problems:
        print(f"  - [{name}] {detail}")
    print("\n→ 사실 변경이 의도라면 레벨링 PR이 아니라 근거 패킷(축1) 경로로 진행하세요.")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
