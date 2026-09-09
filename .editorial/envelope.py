#!/usr/bin/env python3
"""
리뷰 envelope — 리뷰/승인 결과를 정확한 맥락 튜플에 바인딩.

계약: froguin/multi-agent-stack@3113cfc §Evidence packet
  "Actions builds an envelope from GitHub's trusted repository/PR identity,
   base_sha, head_sha, packet SHA-256, policy version and reviewer/model
   configuration version. A changed head, relevant base, packet or policy
   invalidates the prior result. Freshness expiry also requires revalidation."

원칙:
  - 패킷 자신의 커밋 SHA를 패킷에 넣지 않는다(self-reference 금지). envelope는 GitHub의
    신뢰된 신원(repo/PR/base/head)과 패킷 해시·정책 버전으로 Actions가 구성한다.
  - head/base/packet/policy/reviewer-config 중 하나라도 바뀌면 envelope 키가 달라져
    이전 리뷰 결과가 자동 무효화된다(캐시 미스).
  - freshness(신선도) 만료 시 재검증 필요 — expires_at 포함.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, asdict


POLICY_VERSION = "editorial-contract-3113cfc"


@dataclass(frozen=True)
class ReviewEnvelope:
    repo: str            # owner/name (신뢰된 GitHub 신원)
    pr_number: int
    base_sha: str
    head_sha: str
    packet_sha256: str   # 패킷 바이트의 SHA-256
    policy_version: str
    reviewer_config_version: str  # 리뷰 model/provider 구성 버전
    checked_at: str      # 리뷰 수행 시각(RFC3339)
    expires_at: str      # 신선도 만료(RFC3339) — 이후 재검증 필요

    def key(self) -> str:
        """캐시/바인딩 키. 구성요소가 바뀌면 키가 달라진다(무효화)."""
        material = "|".join([
            self.repo, str(self.pr_number), self.base_sha, self.head_sha,
            self.packet_sha256, self.policy_version, self.reviewer_config_version,
        ])
        return hashlib.sha256(material.encode("utf-8")).hexdigest()

    def to_report(self, verdict: str, reasons: list[str]) -> dict:
        """리뷰 리포트(체크/아티팩트로 저장). 승인은 이 튜플에 바인딩된다."""
        return {
            "envelope_key": self.key(),
            "envelope": asdict(self),
            "verdict": verdict,
            "reasons": reasons,
        }


def packet_sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def is_still_valid(prev: ReviewEnvelope, current: ReviewEnvelope) -> bool:
    """이전 리뷰 결과가 현재 맥락에 여전히 유효한가.

    head/base/packet/policy/reviewer-config 중 하나라도 다르면 무효.
    (freshness 만료는 호출부에서 current.checked_at vs prev.expires_at로 판단.)
    """
    return prev.key() == current.key()


if __name__ == "__main__":
    # 데모: 두 envelope 키 비교(수동 확인용).
    import sys
    print(json.dumps({"policy_version": POLICY_VERSION}, indent=2))
    sys.exit(0)
