#!/usr/bin/env bash
# 편집 리뷰 게이트의 required status check 등록/롤백 (versioned, idempotent).
#
# 계약: froguin/multi-agent-stack@53618d6 §Review(5), §Cutover.
# 목적: 검증 후에만 editorial-review·editorial-c-approval을 required로 추가한다.
#   실제 적용은 부모 검증 후. 이 스크립트는 최소 diff·rollback을 기록·재현 가능하게 한다.
#
# 안전:
#   - admin 우회를 켜거나 보호를 약화시키지 않는다(enforce_admins는 건드리지 않음).
#   - strict 유지. 기존 5개 결정론적 게이트를 그대로 보존하고 2개만 추가한다.
#   - --apply 없이는 변경하지 않는다(기본 dry-run: 계획만 출력).
#
# 사용법:
#   ./enforce_required_checks.sh plan            # 현재 vs 목표 diff 출력(변경 없음)
#   ./enforce_required_checks.sh apply-enforce   # editorial 2개 추가(검증 후에만)
#   ./enforce_required_checks.sh apply-rollback  # editorial 2개 제거(원복)
#
# 필요 권한: repo admin. GITHUB 인증은 gh CLI 사용.
set -euo pipefail

REPO="cloudpickr/cloudpick-docs"
BRANCH="master"
BASE_CONTEXTS=(build docs-consistency-lint link-check mermaid-lint strikethrough-lint)
EDITORIAL_CONTEXTS=(editorial-review editorial-c-approval)

join_json() {  # 배열 → JSON 문자열 배열
  local out="" c
  for c in "$@"; do out+="\"$c\","; done
  echo "[${out%,}]"
}

current_contexts() {
  gh api "repos/$REPO/branches/$BRANCH/protection/required_status_checks" \
    -q '.contexts | join(",")' 2>/dev/null || echo ""
}

set_contexts() {  # $1 = JSON 배열
  # strict=true 유지. required_status_checks만 갱신(다른 보호설정 불변).
  gh api -X PATCH "repos/$REPO/branches/$BRANCH/protection/required_status_checks" \
    -H "Accept: application/vnd.github+json" \
    -f strict=true \
    --input - <<JSON
{ "strict": true, "contexts": $1 }
JSON
}

TARGET_ENFORCE=$(join_json "${BASE_CONTEXTS[@]}" "${EDITORIAL_CONTEXTS[@]}")
TARGET_ROLLBACK=$(join_json "${BASE_CONTEXTS[@]}")

cmd="${1:-plan}"
echo "repo=$REPO branch=$BRANCH"
echo "current: $(current_contexts)"
case "$cmd" in
  plan)
    echo "enforce target : $TARGET_ENFORCE"
    echo "rollback target: $TARGET_ROLLBACK"
    echo "(dry-run: no changes made. run apply-enforce/apply-rollback to apply.)"
    ;;
  apply-enforce)
    echo "applying enforce target (adds editorial-review, editorial-c-approval)…"
    set_contexts "$TARGET_ENFORCE" >/dev/null
    echo "done. now required: $(current_contexts)"
    ;;
  apply-rollback)
    echo "applying rollback (removes editorial checks, keeps deterministic 5)…"
    set_contexts "$TARGET_ROLLBACK" >/dev/null
    echo "done. now required: $(current_contexts)"
    ;;
  *)
    echo "usage: $0 {plan|apply-enforce|apply-rollback}" >&2
    exit 2
    ;;
esac
