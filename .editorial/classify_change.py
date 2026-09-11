#!/usr/bin/env python3
"""
변경 분류기(classify) — 저장소 측 신뢰된 재판정.

계약: froguin/multi-agent-stack@53618d6 §Risk tiers
  A: 순수 기계적 오타/형식/링크/렌더 변경. 로케일 피어 포함 '한 논리 문서',
     추가+삭제 20줄 이하(전 로케일 합산), 사실/변동/구조 변경 없음.
  B: 기존 문서의 제한된 갱신(공식 근거 기반 사실 갱신·번역 포함). 명시적 범위+근거+독립 리뷰.
  C: 신규/삭제/이동/병합/분할/카테고리/네비 변경, 법규·규제·컴플라이언스 주장,
     범위 불명/과대, 기존 human hold.

핵심 원칙:
  - tier_hint·generated_by_llm·writer는 '입력 신호'일 뿐. 이 분류기는 실제 diff와
    패킷으로 독립 재판정한다. 작성 측 신고만으로 하향하지 않는다.
  - LLM 생성 편집(generated_by_llm=true 또는 writer 신뢰 불가)은 최소 B.
  - 불명확/이견/알 수 없는 범위는 상향(escalate)한다. 절대 조용히 하향하지 않는다.
  - 이 분류기는 결정론적이며 LLM을 호출하지 않는다(사실 검증은 별도 리뷰 단계).

exit code: 0=분류 성공(결과 stdout에 tier), 1=분류 실패/입력 오류(승인 아님).
"""
from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

A_MAX_TOTAL_LINES = 20  # 전 로케일 합산 added+deleted
COUNTRY_DIRS = ("korea", "us", "eu", "japan", "singapore")
# 사실/규제 위험을 시사하는 경로 힌트(가중치 판단용, 단독으로 C를 확정하진 않음).
GOVERNANCE_HINT = ("governance/compliance", "security/network-isolation")


@dataclass
class FileChange:
    """한 파일의 변경 요약(신뢰된 git diff에서 파싱)."""
    path: str
    status: str  # A(added) M(modified) D(deleted) R(renamed)
    added: int = 0
    deleted: int = 0
    old_path: str | None = None  # rename 시


@dataclass
class Classification:
    tier: str            # "A" | "B" | "C"
    reasons: list[str] = field(default_factory=list)
    escalated_from: str | None = None  # 상향된 경우 원 tier


def _is_structural(changes: list[FileChange]) -> list[str]:
    """신규/삭제/이동/병합/분할/카테고리/네비 = 구조 변경 → C."""
    reasons = []
    for c in changes:
        if c.status == "A":
            reasons.append(f"new file (create): {c.path}")
        elif c.status == "D":
            reasons.append(f"deleted file: {c.path}")
        elif c.status == "R":
            reasons.append(f"moved/renamed: {c.old_path} -> {c.path}")
    return reasons


def _country_or_regulatory(changes: list[FileChange]) -> list[str]:
    """국가 규제 레이어·거버넌스 경로는 '위험 신호'(단독으로 C 확정 아님)."""
    reasons = []
    for c in changes:
        parts = c.path.split("/")
        # src/content/docs/<locale>/<maybe-country>/...
        if len(parts) >= 5 and parts[4] in COUNTRY_DIRS:
            reasons.append(f"country/regulatory path: {c.path}")
        if any(h in c.path for h in GOVERNANCE_HINT):
            reasons.append(f"governance path: {c.path}")
    return reasons


def _total_lines(changes: list[FileChange]) -> int:
    return sum(c.added + c.deleted for c in changes)


def _touches_astro_config_or_sidebar(changes: list[FileChange]) -> list[str]:
    reasons = []
    for c in changes:
        if not c.path.startswith("src/content/docs/"):
            # 문서 밖 변경(설정·워크플로우 등)은 이 분류기 범위 밖 → C로 escalate.
            reasons.append(f"non-document change: {c.path}")
    return reasons


def classify(
    changes: list[FileChange],
    packet: dict | None,
    *,
    has_regulatory_claim: bool = False,
    human_hold: bool = False,
    scope_unknown: bool = False,
    packet_scope_exempt: list[str] | None = None,
) -> Classification:
    """실제 diff + 패킷으로 A/B/C 재판정. 불명확/이견은 상향.

    packet_scope_exempt: 검증된 '단일 패킷 파일'의 실제 저장소 경로 목록. 이 경로의
      변경은 문서 스코프 판정(구조/라인수)에서 제외한다. 이렇게 해야 패킷 신규파일
      (.editorial/packets/*.json 추가)이 모든 B를 C로 만들지 않는다. 호출부는 '검증
      통과한' 경로만 넘겨야 하며, invalid/unrelated metadata는 넘기지 않는다(제외 금지).
    """
    reasons: list[str] = []
    exempt = set(packet_scope_exempt or [])

    # 스코프 예외: 검증된 패킷 파일만 판정 대상에서 제외. 나머지는 그대로 판정.
    scoped = [c for c in changes if c.path not in exempt]
    if exempt:
        reasons.append(f"scope-exempt validated packet file(s): {sorted(exempt)}")

    # C 확정 사유(고위험) ---------------------------------------------------
    if human_hold:
        return Classification("C", ["existing human hold"])
    if scope_unknown:
        return Classification("C", ["unknown scope"])

    structural = _is_structural(scoped)
    non_doc = _touches_astro_config_or_sidebar(scoped)
    if structural:
        return Classification("C", structural + reasons)
    if non_doc:
        # 문서 외 변경(카테고리/네비/설정)은 구조 영향 가능 → C escalate.
        return Classification("C", non_doc + reasons)
    if has_regulatory_claim:
        return Classification("C", ["legal/regulatory/compliance claim"] + reasons)

    # 국가/거버넌스 경로는 위험 신호 — 사실 변경과 결합 시 최소 B, 순수 오타는 아래 로직.
    risk_paths = _country_or_regulatory(scoped)

    # tier_hint는 참고만. LLM 생성/신뢰불가 writer는 최소 B.
    generated_by_llm = bool(packet and packet.get("generated_by_llm"))
    has_claims = bool(packet and packet.get("claim_ledger"))
    total = _total_lines(scoped)

    # A 자격: 순수 기계적, 합산 20줄 이하, 사실/구조 변경 없음, LLM 생성 아님.
    a_blockers = []
    if generated_by_llm:
        a_blockers.append("generated_by_llm=true → minimum B")
    if has_claims:
        a_blockers.append("claim_ledger present → factual change, minimum B")
    if total > A_MAX_TOTAL_LINES:
        a_blockers.append(f"total {total} lines > {A_MAX_TOTAL_LINES} (locale-summed)")
    if risk_paths:
        # 국가/거버넌스 경로의 순수 오타는 자동 C는 아니지만 A 자격에서는 제외(보수적).
        a_blockers.append("country/governance path → at least B")

    if not a_blockers:
        return Classification("A", ["mechanical change within A limits"] + risk_paths)

    # A 실패 → B. 단 근거(claim_ledger)나 명시 범위가 없으면 상향(escalate to C).
    if has_claims:
        return Classification("B", ["bounded factual update with evidence"] + a_blockers + risk_paths)

    # 근거 없는 비기계적 변경 = 범위/의도 불명확 → C로 상향(조용한 하향 금지).
    return Classification(
        "C",
        ["non-mechanical change without evidence packet claims → escalate"] + a_blockers + risk_paths,
        escalated_from="B",
    )


# ── git diff 파싱(신뢰된 base-branch 실행) ──────────────────────────────────
def parse_numstat_and_status(numstat: str, name_status: str) -> list[FileChange]:
    """`git diff --numstat`와 `--name-status` 출력을 FileChange로 병합."""
    added_deleted: dict[str, tuple[int, int]] = {}
    for line in numstat.strip().splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        if len(parts) < 3:
            continue
        a, d, path = parts[0], parts[1], parts[2]
        # binary는 '-' 로 표기됨
        ai = 0 if a == "-" else int(a)
        di = 0 if d == "-" else int(d)
        added_deleted[path] = (ai, di)

    changes: list[FileChange] = []
    for line in name_status.strip().splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        code = parts[0]
        if code.startswith("R") and len(parts) >= 3:
            old, new = parts[1], parts[2]
            a, d = added_deleted.get(new, (0, 0))
            changes.append(FileChange(new, "R", a, d, old_path=old))
        elif len(parts) >= 2:
            path = parts[1]
            a, d = added_deleted.get(path, (0, 0))
            changes.append(FileChange(path, code[0], a, d))
    return changes


def main(argv: list[str]) -> int:
    # 사용법: classify_change.py <numstat_file> <name_status_file> [packet.json]
    if len(argv) < 3:
        print("usage: classify_change.py <numstat> <name_status> [packet.json]",
              file=sys.stderr)
        return 1
    numstat = Path(argv[1]).read_text(encoding="utf-8")
    name_status = Path(argv[2]).read_text(encoding="utf-8")
    packet = None
    if len(argv) >= 4 and Path(argv[3]).is_file():
        packet = json.loads(Path(argv[3]).read_text(encoding="utf-8"))

    changes = parse_numstat_and_status(numstat, name_status)
    result = classify(changes, packet)
    out = {
        "tier": result.tier,
        "reasons": result.reasons,
        "escalated_from": result.escalated_from,
        "files": len(changes),
        "total_lines": _total_lines(changes),
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
