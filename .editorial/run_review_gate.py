#!/usr/bin/env python3
"""
리뷰 게이트 오케스트레이터 — 패킷검증→분류→(B/C)독립리뷰를 하나로 묶어 verdict 산출.

계약: froguin/multi-agent-stack@3113cfc §Review

입력(모두 신뢰된 base 코드가 데이터로 취급; PR head 코드 실행 없음):
  --numstat FILE        git diff --numstat (워크플로우가 GitHub API로 생성)
  --name-status FILE    git diff --name-status
  --diff FILE           통합 diff 텍스트(리뷰 데이터)
  --packet FILE|none    PR head의 단일 패킷 JSON을 API로 데이터 취득한 파일(없으면 'none')
  --repo, --pr, --base-sha, --head-sha   envelope 신원(GitHub 신뢰 값)

출력: stdout에 JSON {tier, verdict, state, reasons, envelope_key}.
exit code: 0=state success, 1=state failure(changes_requested 등), 2=state pending/error(비승인).

원칙:
  - 패킷 없음/스키마 불일치/unknown provenance를 A로 낮추지 않는다. 문서 실변경이면 B/C 보류.
  - 검증된 '일치' 패킷만 scope 예외로 인정(파일명=jira_key, target∈changed 등 validate 통과).
  - 실패/미설정/outage는 success로 변환하지 않는다.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import classify_change as cc  # noqa: E402
import review_runner as rr    # noqa: E402
import validate_packet as vp  # noqa: E402
import envelope as ev         # noqa: E402


def _state_from_verdict(verdict: str) -> str:
    if verdict == "approve":
        return "success"
    if verdict == "changes_requested":
        return "failure"
    return "pending"  # error / skipped-unconfigured / boundary holds


def run(args) -> dict:
    numstat = Path(args.numstat).read_text(encoding="utf-8")
    name_status = Path(args.name_status).read_text(encoding="utf-8")
    changes = cc.parse_numstat_and_status(numstat, name_status)

    # 패킷 취득·검증 -----------------------------------------------------------
    packet = None
    packet_valid = False
    packet_reasons: list[str] = []
    packet_sha = ""
    packet_repo_path = (args.packet_repo_path or "").strip()  # GitHub API의 실제 저장소 경로
    if args.packet and args.packet != "none" and Path(args.packet).is_file():
        raw = Path(args.packet).read_bytes()
        packet_sha = ev.packet_sha256(raw)
        # 검증기에는 '실제 저장소 경로'를 넘긴다(내용의 jira_key로 재구성하지 않음).
        # 파일명==jira_key 불일치를 실제로 잡기 위함(#3 자기비교 제거).
        if not packet_repo_path:
            packet_reasons.append("packet repo path not provided — cannot verify filename")
        else:
            try:
                packet = vp.validate_packet(raw, Path(packet_repo_path))
                packet_valid = True
            except Exception as exc:  # noqa: BLE001 — 어떤 검증 실패든 승인 아님
                packet_reasons.append(f"packet invalid: {exc}")
                packet = None

    # 분류: 검증된 패킷만 신뢰. 무효/부재 패킷은 classify에 넘기지 않는다(A 하향 방지).
    #  또한 '검증된 단일 패킷 파일 경로'만 구조판정 scope 예외로 넘긴다(#1). 이렇게 해야
    #  패킷 신규파일(.editorial/packets/*.json 추가)이 모든 B를 C로 만들지 않는다.
    #  invalid/unrelated metadata는 예외에서 제외(예외 경로를 넘기지 않음).
    trusted_packet = packet if packet_valid else None
    exempt_paths = [packet_repo_path] if (packet_valid and packet_repo_path) else []
    result = cc.classify(changes, trusted_packet, packet_scope_exempt=exempt_paths)
    tier = result.tier
    reasons = list(result.reasons) + packet_reasons

    # A: 결정론적 게이트로 충분. 단, 패킷이 첨부됐는데 무효면 A로 인정하지 않는다.
    if tier == "A":
        if args.packet and args.packet != "none" and not packet_valid:
            return _out("C", "changes_requested",
                        ["attached packet failed validation — not eligible for A"] + reasons,
                        args, packet_sha)
        return _out("A", "approve", ["tier A: deterministic checks only"] + reasons,
                    args, packet_sha)

    # B/C: 패킷이 유효해야 진행. 없음/무효면 보류(비승인) — A로 낮추지 않음.
    if not packet_valid:
        return _out(tier, "error",
                    ["B/C requires a valid evidence packet; none valid → hold"] + reasons,
                    args, packet_sha)

    # 독립 LLM 리뷰. claim_ledger의 공식 출처를 source_fetch로 독립 재취득해 리뷰에 연결(#2).
    config = rr.ReviewConfig.from_env()
    diff_text = Path(args.diff).read_text(encoding="utf-8") if Path(args.diff).is_file() else ""
    source_evidence, source_reasons = _fetch_sources(packet)
    if source_evidence is None:
        # SSRF 차단·fetch 실패는 non-pass(승인 아님).
        return _out(tier, "error",
                    ["independent source fetch failed/blocked — hold"] + source_reasons + reasons,
                    args, packet_sha)
    review = rr.run_review(config, packet, diff_text, source_evidence=source_evidence)
    reasons += [f"review:{review.verdict}"] + review.reasons + source_reasons
    return _out(tier, review.verdict, reasons, args, packet_sha)


def _fetch_sources(packet: dict):
    """claim_ledger의 각 공식 출처를 독립 fetch. 하나라도 차단/실패면 (None, reasons).

    성공 시 (url -> FetchResult 요약) dict를 리뷰에 넘긴다. 출처가 없으면 빈 dict(리뷰가
    근거 부재로 판단하도록). 계약 §Evidence: fetcher는 SSRF·상한을 강제한다.
    """
    import source_fetch as sfetch
    evidence = {}
    reasons = []
    urls = []
    for claim in (packet or {}).get("claim_ledger", []):
        if claim.get("source_url"):
            urls.append(claim["source_url"])
        for s in claim.get("sources", []) or []:
            if s.get("source_url"):
                urls.append(s["source_url"])
    for url in urls:
        try:
            r = sfetch.fetch_source(url)
            evidence[url] = {"status": r.status, "sha256": r.body_sha256, "bytes": r.body_bytes}
        except sfetch.FetchError as exc:
            reasons.append(f"source fetch blocked/failed: {url}: {exc}")
            return None, reasons  # non-pass
    return evidence, reasons


def _out(tier, verdict, reasons, args, packet_sha) -> dict:
    envelope = ev.ReviewEnvelope(
        repo=args.repo, pr_number=int(args.pr),
        base_sha=args.base_sha, head_sha=args.head_sha,
        packet_sha256=packet_sha or ("0" * 64),
        policy_version=ev.POLICY_VERSION,
        reviewer_config_version=(rr.ReviewConfig.from_env().reviewer_model or "unset"),
        checked_at=args.now or "1970-01-01T00:00:00Z",
        expires_at=args.expires or "1970-01-08T00:00:00Z",
    )
    state = _state_from_verdict(verdict)
    return {
        "tier": tier, "verdict": verdict, "state": state,
        "reasons": reasons, "envelope_key": envelope.key(),
        "report": envelope.to_report(verdict, reasons),
    }


def main(argv) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--numstat", required=True)
    p.add_argument("--name-status", required=True, dest="name_status")
    p.add_argument("--diff", required=True)
    p.add_argument("--packet", default="none")
    p.add_argument("--packet-repo-path", default="", dest="packet_repo_path",
                   help="GitHub API가 보고한 패킷의 실제 저장소 경로(파일명 검증용)")
    p.add_argument("--repo", required=True)
    p.add_argument("--pr", required=True)
    p.add_argument("--base-sha", required=True, dest="base_sha")
    p.add_argument("--head-sha", required=True, dest="head_sha")
    p.add_argument("--now", default=None)
    p.add_argument("--expires", default=None)
    args = p.parse_args(argv)

    out = run(args)
    print(json.dumps(out, ensure_ascii=False, indent=2))
    # 상태를 exit code로 정확히 반영(fail을 녹색으로 마감하지 않음).
    if out["state"] == "success":
        return 0
    if out["state"] == "failure":
        return 1
    return 2  # pending/error/hold


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
