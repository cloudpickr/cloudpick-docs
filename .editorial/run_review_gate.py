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
    if args.packet and args.packet != "none" and Path(args.packet).is_file():
        raw = Path(args.packet).read_bytes()
        packet_sha = ev.packet_sha256(raw)
        try:
            # 파일명 == jira_key 검증까지 위해 논리 파일명을 넘긴다.
            logical = Path(f"{json.loads(raw.decode('utf-8')).get('jira_key','')}.json")
            packet = vp.validate_packet(raw, logical)
            packet_valid = True
        except Exception as exc:  # noqa: BLE001 — 어떤 검증 실패든 승인 아님
            packet_reasons.append(f"packet invalid: {exc}")
            packet = None

    # 분류: 검증된 패킷만 신뢰. 무효/부재 패킷은 classify에 넘기지 않는다(A 하향 방지).
    trusted_packet = packet if packet_valid else None
    result = cc.classify(changes, trusted_packet)
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

    # 독립 LLM 리뷰(writer-distinct·예산·outage 처리 포함).
    config = rr.ReviewConfig.from_env()
    diff_text = Path(args.diff).read_text(encoding="utf-8") if Path(args.diff).is_file() else ""
    review = rr.run_review(config, packet, diff_text)
    reasons += [f"review:{review.verdict}"] + review.reasons
    return _out(tier, review.verdict, reasons, args, packet_sha)


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
