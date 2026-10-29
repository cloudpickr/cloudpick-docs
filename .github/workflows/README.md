# GitHub Actions 워크플로 개요

이 저장소의 CI/자동화 워크플로 전체 목록입니다. **머지 차단(required)** 체크와 **자동화/보조** 체크를 구분합니다. 운영 모델의 맥락은 저장소 루트 `AGENTS.md`의 "문서 지속 관리 운영 모델", 편집 게이트 내부는 `.editorial/README.md`를 참조하세요.

## 머지 차단 게이트 (branch protection required)

master 보호의 required 체크는 7개입니다: `build`·`docs-consistency-lint`·`link-check`·`mermaid-lint`·`strikethrough-lint`·`editorial-review`·`editorial-c-approval`.

| 워크플로 파일 | name | 생성 체크(required) | 트리거 |
| --- | --- | --- | --- |
| `starlight-build.yml` | Build | `build` (내부 링크 검증 포함) | push · 모든 PR |
| `docs-quality.yml` | Docs Quality | `docs-consistency-lint`·`mermaid-lint`·`strikethrough-lint` | push · 모든 PR |
| `external-link-check.yml` | External Link Check | `link-check` (lychee, 외부 링크) | push · 모든 PR · schedule |
| `editorial-c-approval.yml` | Editorial Review | `editorial-review`·`editorial-c-approval` | pull_request · issue_comment(`/approve`) · dispatch |

:::caution
`link-check`·`build`는 모든 PR에서 돕니다(paths 필터 없음). paths 필터를 두면 필터 밖 경로만 바꾸는 PR에서 required 체크가 생성되지 않아 머지가 영구 대기(BLOCKED)에 빠집니다. 필터를 추가하지 마세요.
:::

## 자동화·보조 워크플로 (머지 비차단)

| 워크플로 파일 | name | 역할 | 트리거 |
| --- | --- | --- | --- |
| `monthly-review.yml` | Monthly Docs Review | 월간 트래킹 이슈 생성(매월 1일) + 매일 새 소식 수집·매핑 코멘트(축2) | schedule(월·일) · dispatch |
| `editorial-gateway-healthcheck.yml` | Editorial Gateway Healthcheck | AI 게이트웨이 토큰·쿼터 상태 일일 점검 | schedule(매일) · dispatch |
| `needs-fix-label.yml` | Label Bridge for Docs Agent | `changes_requested` 리뷰·`/fix` 코멘트를 라벨로 브리지 | pull_request_review · issue_comment |
| `docs-quality.yml` (일부) | Docs Quality | `emphasis-lint`·`editorial-advisory`·`leveling-guard`(라벨 기반)·`link-refresh-guard`(패킷 자격 파생) | push · PR |
| `codeql.yml` | CodeQL | 코드 보안 정적 분석(python·js·actions) | push · PR · schedule |

## 축4 레벨링 라벨 게이트

`docs-quality.yml`의 `leveling-guard` 잡은 `axis-4-leveling` 라벨이 붙은 PR에서만 required로 작동합니다. 트리거에 `labeled`·`unlabeled`가 포함되어 라벨 부착 시점에 재평가됩니다. 레벨링 PR의 사실 불변 강제는 `scripts/leveling-guard.py`(결정론), 의미 보존은 `editorial-review` 게이트가 담당합니다.

## 축1 링크 현행화 게이트 (패킷 자격에서 파생)

`docs-quality.yml`의 `link-refresh-guard` 잡은 **PR이 변경/추가한 패킷(`.editorial/packets/*.json`) 중 `policy_action: "link-refresh"`가 있으면** 작동합니다(변경 가능한 라벨이 아니라 '패킷 자격'에서 트리거를 파생 — 라벨 생략으로 스킵 불가, fail-open 차단). 해당 패킷들의 `link_refresh.url_map`을 모아, 변경된 모든 로케일 문서에 '재구성 매칭'(`scripts/link-refresh-guard.py`)을 적용해 URL 외 변경이 없음을 증명하고, `scripts/link-refresh-manifest.py`로 `manifest_sha256`·`changed_paths_count`를 실제 변경과 대조합니다. 추가로 editorial 게이트가 각 old URL을 re-fetch해 리다이렉트 체인이 new로 끝남을 확인합니다. 자격·규제 경로 분리는 AGENTS.md "축1 링크 현행화 예외" 참조.

## required 등록·롤백

required 체크 등록/해제는 `.editorial/enforce_required_checks.sh`(versioned, `apply-enforce`/`apply-rollback`)로 수행합니다. 게이트웨이 장기 장애 시 editorial 2개를 임시로 내리고(결정론적 5개 유지) 복구 후 재승격하는 런북은 `CONTRIBUTING.md` "편집 리뷰 게이트와 장애 대응"을 참조하세요.
