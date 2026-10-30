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
| `link-refresh.yml` | Link Refresh Drafts | 제한된 Google docs 호스트 이전 후보 보고 및 opt-in draft PR 생성. 문서 C 승인·머지는 별도 | schedule(주) · dispatch |
| `editorial-gateway-healthcheck.yml` | Editorial Gateway Healthcheck | AI 게이트웨이 토큰·쿼터 상태 일일 점검 | schedule(매일) · dispatch |
| `needs-fix-label.yml` | Label Bridge for Docs Agent | `changes_requested` 리뷰·`/fix` 코멘트를 라벨로 브리지 | pull_request_review · issue_comment |
| `docs-quality.yml` (일부) | Docs Quality | `emphasis-lint`·`editorial-advisory`·`leveling-guard`(라벨 기반)·`link-refresh-guard`(패킷 자격 파생) | push · PR |
| `codeql.yml` | CodeQL | 코드 보안 정적 분석(python·js·actions) | push · PR · schedule |

## 월간 문서 검토 원장

`monthly-review.yml`의 월초 실행은 ko 문서 목록과 분류·중복·가독성·레벨링 신호를 월간 이슈와 실행 아티팩트에 기록합니다. 이슈 본문의 `monthly-ledger` JSON은 문서별 `unreviewed`·`scanned`·`verified`·`unverified` 상태와 네 축의 후보(`open`·`hold`·`done`·`current`·`wontfix`)를 보존합니다. 자동 스캔은 후보만 생성하고 문서를 `verified`로 바꾸지 않습니다.

담당자는 월간 이슈의 JSON에서 상태·공식 근거 URL(`evidence`)·관련 PR URL(`pr`)을 직접 기록합니다. `verified` 문서와 `current` 후보에는 HTTPS 근거가 필요하며, `done` 후보에는 PR URL이 필요합니다. 근거 URL 형식 검사는 출처의 공식성이나 사실 일치 판정이 아닙니다. 새 달에는 문서를 다시 `unreviewed`로 시작하고 이전 달 `open`·`hold` 후보를 이월합니다. 종료 후보의 ID도 이어 받아 같은 후보를 다시 만들지 않습니다. 상세 기록은 원래 월간 이슈에 남습니다.

원장이 없던 이전 달은 이월을 자동으로 복구할 수 없어 수동 확인이 필요합니다. 기존 이슈에 사람이 자유 형식으로 남긴 코멘트를 자동으로 처리 완료로 해석하지 않습니다. 원장 JSON이 잘못되었거나 이슈 본문 크기 상한을 넘으면 갱신을 중단하고 Actions 실패로 표시합니다. 이슈 본문을 동시에 편집할 때는 실행이 끝난 뒤 변경 내용을 확인하세요.

일일 소식은 결정론적 매핑 후보를 축2 원장에 추가하고, 미매핑 소식은 문서 경로가 없는 축3 후보로 남깁니다. 근거는 `unverified`로 시작합니다. 공식 출처 확인·관련성 판단, 누락된 소식 재수집, 의미·구조 검토는 자동 스캔을 대체할 수 없습니다. 수집 실패·부분 실패는 월간 이슈에 표시하며 수동 재실행할 수 있습니다. 원장과 신호는 구조 변경을 승인하지 않으며, 분류·구조 변경은 기존 과반 의결을 따릅니다.

## 축4 레벨링 라벨 게이트

`docs-quality.yml`의 `leveling-guard` 잡은 `axis-4-leveling` 라벨이 붙은 PR에서만 required로 작동합니다. 트리거에 `labeled`·`unlabeled`가 포함되어 라벨 부착 시점에 재평가됩니다. 레벨링 PR의 사실 불변 강제는 `scripts/leveling-guard.py`(결정론), 의미 보존은 `editorial-review` 게이트가 담당합니다.

## 축1 링크 현행화 게이트 (패킷 자격에서 파생)

`docs-quality.yml`의 `link-refresh-guard` 잡은 **PR이 변경/추가한 패킷(`.editorial/packets/*.json`) 중 `policy_action: "link-refresh"`가 있으면** 작동합니다(변경 가능한 라벨이 아니라 '패킷 자격'에서 트리거를 파생 — 라벨 생략으로 스킵 불가, fail-open 차단). 해당 패킷들의 `link_refresh.url_map`을 모아, 변경된 모든 로케일 문서에 '재구성 매칭'(`scripts/link-refresh-guard.py`)을 적용해 URL 외 변경이 없음을 증명하고, `scripts/link-refresh-manifest.py`로 `manifest_sha256`·`changed_paths_count`를 실제 변경과 대조합니다. 추가로 editorial 게이트는 신뢰된 base 가드로 두 커밋의 문서 전체 및 매니페스트를 검사하고 각 old URL을 re-fetch해 리다이렉트 체인이 new로 끝남을 확인합니다. PR head 코드는 실행하지 않으며 파일·커밋을 취득하지 못하면 보류합니다. 자격·규제 경로 분리는 AGENTS.md "축1 링크 현행화 예외" 참조.

## 링크 현행화 예약·수동 실행

`link-refresh.yml`은 매주 화요일 10:35 KST에 후보 보고서를 만들고 14일 보관합니다. 기본값은 **보고만** 하며, 수동 `publish=true` 또는 저장소 변수 `LINK_REFRESH_CREATE_PRS=true`로 draft 생성을 선택합니다. `target`은 한국어 기준 상대 논리 경로(예: `compute/containers.md`)이며 생략하면 제한된 배치를 회전 검사합니다. 실행 코드는 dispatch 대상 ref와 관계없이 신뢰된 `master`에서만 가져옵니다.

문서 변경이 없는 자동화 코드 PR은 기존 `feature-only` 경로로 사람 문서 승인 없이 검증합니다. 봇이 생성한 문서 PR은 URL 변경만 있어도 C이며, 독립 리뷰·필수 CI·허용된 사람의 패킷 해시 확인과 머지가 필요합니다. 코드 구현 PR과 생성 문서 PR을 섞지 않습니다.

기본 `GITHUB_TOKEN`으로 PR을 만들면 GitHub가 후속 PR 워크플로 실행 승인을 요구할 수 있습니다. [GitHub 공식 설명](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow)에 따라 무인 CI가 필요하면 `LINK_REFRESH_PR_TOKEN`(contents·pull requests·issues 권한의 GitHub App/PAT)을 별도로 설정합니다. 토큰이 없더라도 성공을 가장하지 않으며, 문서 승인자 신원을 자동 승인에 사용하지 않습니다. 저장소의 Actions PR 생성 허용 설정도 필요합니다.

열린 링크 현행화 PR이 있으면 다음 draft 생성을 멈추고, 생성한 PR은 #271에 연결합니다. 후보 부재·fetch 실패·hold는 artifact와 실행 요약에서 확인하며, 실행 자체 실패는 실패한 Actions 실행으로 남깁니다. 범위·테스트·명령은 `scripts/README.md`를 참고하세요. 예약 실행·배포 후의 실제 동작 확인은 코드 CI 통과와 구분합니다.

## required 등록·롤백 명령

required 체크 등록/해제는 `.editorial/enforce_required_checks.sh`(versioned, `apply-enforce`/`apply-rollback`)로 수행합니다. 게이트웨이 장기 장애 시 editorial 2개를 임시로 내리고(결정론적 5개 유지) 복구 후 재승격하는 런북은 `CONTRIBUTING.md` "편집 리뷰 게이트와 장애 대응"을 참조하세요.
