# Editorial handoff — 저장소 측 참조

이 디렉터리는 multi-agent-stack → 문서 저장소 편집 핸드오프 계약의 **저장소 측 준비물**을 담습니다.
운영 전환(cutover)은 아직 이루어지지 않았으며, 기존 발행 게이트는 그대로 유효합니다.

## 계약 원본 (Source of Truth)

계약 본문은 이 저장소에 **사본을 두지 않습니다.** 아래 핀 커밋 링크를 단일 기준으로 참조합니다.

- **정규 계약(pinned):** `froguin/multi-agent-stack` 커밋 `53618d6`
  `docs/architecture/editorial-actions-contract.md`
- 계약의 명확화 반영 및 핀 갱신은 **스택 측 책임**입니다. 여기의 핀만 따라 갱신합니다.
- 핀 이력: `e0dbbdc` → `3113cfc` → `4d60805`(문서 신원 = packet SHA-256) →
  `53618d6`(편집 리뷰 scope by file path only 문안 동기화).

## 이 디렉터리의 내용

## 이 디렉터리의 내용 (소스 맵)

`.editorial/`의 모든 소스는 AGENTS.md의 **4대 축 운영 모델**을 떠받칩니다. 각 파일이 어느 축·어느 역할인지 아래 표로 정리합니다(파일 이동 없이 역할을 명시). 상세 설명은 각 파일 상단 docstring을 참조하세요.

### 편집 리뷰 게이트 (축1·2·4 공통 — 근거 패킷 PR 판정)

| 파일 | 역할 |
| --- | --- |
| `packet.schema.json` | 근거 패킷 **형식 검증** 스키마(JSON Schema 2020-12). 계약 §Evidence packet 최소 필드. |
| `validate_packet.py` | 패킷 **trusted validator**(경로 정규화·128KiB·중복 JSON 키·trailing newline·BOM·checked_at RFC3339·target∈changed·파일명 일치). |
| `classify_change.py` | diff+패킷으로 **A/B/C 재판정**. `src/content/docs/**` 문서 변경만 판정, 비문서는 scope 밖. legal-B(단일 논리 문서) 티어 로직 포함. |
| `review_runner.py` | B/C **독립 LLM 리뷰**(LiteLLM 재사용, writer-distinct 강제, 예산·호출·토큰 상한, outage/미설정은 non-pass). |
| `source_fetch.py` | 패킷 `source_url`을 **독립 fetch해 대조**(SSRF 방어: 사설/메타데이터·불안전 리다이렉트 거부, 바이트·시간 상한). |
| `envelope.py` | 리뷰 결과를 repo/PR/base_sha/head_sha/packet-SHA256/policy/reviewer-config 튜플에 **바인딩**(하나라도 바뀌면 캐시 미스). |
| `run_review_gate.py` | **게이트 오케스트레이터** — 패킷검증→분류→(B/C)독립리뷰→verdict. 레벨링 패킷은 의미보존 리뷰로 분기(fail-closed), link-refresh 패킷은 CI 가드 통과를 머지 전제로 명시. |

### 축1 — 링크 현행화(link-refresh, URL-only)

| 파일 | 역할 |
| --- | --- |
| `scripts/link-refresh-guard.py` (루트) | '재구성 매칭'으로 URL 교체만 했음을 결정론 증명(승인 매핑을 base에 적용→head와 바이트 일치). 라인증감·코드/frontmatter/인라인코드/mermaid 내부·URL 외 변경은 fail-closed. |
| `scripts/link-refresh-manifest.py` (루트) | 패킷 `link_refresh.url_map` 병합(가드 입력) + `manifest_sha256` 재계산 대조(전체 경로·매핑·base SHA 대조, changed_paths 64 상한 우회; 실제 head는 리뷰 envelope에 바인딩). |

:::note
link-refresh 패킷은 `policy_action: "link-refresh"`(이 단일 필드가 자격 부여) + 빈 `claim_ledger` + `link_refresh{url_map, manifest_sha256, changed_paths_count}`. 비규제·규제 경로 모두 C(사람 승인 및 독립 리뷰 필요). URL 목적의 의미와 판본을 자동으로 충분히 판별할 수 있을 때까지 B 경로는 보류. **강제 경로(이중)**: ① 이미 required인 `editorial-review`(run_review_gate)가 diff 재구성 매칭 + redirect 체인 re-fetch를 직접 수행해 위반 시 non-pass, ② `link-refresh-guard` 잡이 전체 파일 재구성으로 교차 강제(required 등록 필요: 스크립트 변경만으로 브랜치 보호 설정은 바뀌지 않음). 상세는 AGENTS.md "축1 링크 현행화 예외".
:::

### 축1 — 노후(stale) 스캔 전용 헬퍼

| 파일 | 역할 |
| --- | --- |
| `verifier_core.py` | stale 스캔 2단계 전용 인용/대조 헬퍼(date_probes·cooccurs·quote_is_substring·llm_adjudicate, `MAX_LLM_CALLS` 상한). 게이트 러너와 공유하지 않음(advisory exit-0 시맨틱 충돌 방지). |

### 축4 — 레벨링(표현 교정) 엔진

| 파일 | 역할 |
| --- | --- |
| `leveling-rules.yaml` | 레벨링 **권위 원본 규칙**(불변 사실군 정의, 규제 경로 tier-C 고정, 루프 상한). |
| `leveling_core.py` | 레벨링 교정 엔진 — LLM writer 제안 + **의미보존 리뷰**(닫힌 enum만 차단, 유일 수정은 hunk revert, 24h 만료). 사실은 바이트/멀티셋 불변(가드가 강제). |

### 운영·테스트

| 파일 | 역할 |
| --- | --- |
| `enforce_required_checks.sh` | required 체크 등록/롤백 **versioned 스크립트**(`apply-enforce`/`apply-rollback`). |
| `tests/` | 위 모듈들의 단위 테스트(unittest). |
| `packets/` | 근거 패킷 실제 파일(`<jira_key>.json`, draft PR에 포함). |

:::note
결정론적 가드 `scripts/leveling-guard.py`는 LLM보다 **먼저** 실행되어 코드·표·링크·수치·날짜·버전·고유명사·수식어 개수를 불변으로 강제합니다. 가드 실패는 LLM이 뒤집을 수 없습니다(위치: 저장소 루트 `scripts/`).
:::

### 관련 워크플로/스크립트 (저장소 루트)

- `.github/workflows/editorial-c-approval.yml` — C 승인 게이트(status `editorial-review`·`editorial-c-approval`를 생성).
- `.github/scripts/c_approval_gate.cjs` (+`.test.cjs`) — A/B는 명시 pass, 비문서 전용 PR은 scope 밖 pass, C는 allowlisted human이 **현재 packet SHA-256을 코멘트로 confirm**(`/approve <64-hex>`)해야 pass. GitHub PR Approve는 C 신호가 아니며, 무관한 커밋은 C를 리셋하지 않는다. `EDITORIAL_C_APPROVAL_ALLOWLIST` 미설정 시 C 승인 불가.
- 저장소 루트 `scripts/`의 스캐너/린터 인벤토리는 `scripts/README.md` 참조.

## 공통 크기 상한 (스택·저장소 양측 동일 적용)

Grok(스택 측 `runner/editorial_packet.py`)과 저장소 측 스키마가 **동일 한도**를 쓰도록 고정합니다.

| 항목 | 한도 | 강제 위치 |
| --- | --- | --- |
| 패킷 직렬화 크기(UTF-8) | 128 KiB | trusted validator (파일 크기 — JSON Schema로 표현 불가) |
| `changed_paths` | 64개 | 스키마 `maxItems` |
| `claim_ledger` | 32개 | 스키마 `maxItems` |
| claim당 `sources` | 8개 | 스키마 `maxItems` |

## 검증 분담 (형식 vs 신뢰)

스키마(형식)로 잡는 것과 trusted validator(Actions)가 최종 담당하는 것을 구분합니다.

- **스키마가 잡음:** 필수 필드, enum, 경로 패턴(제어문자·`..`·중복 슬래시·역슬래시 차단),
  `source_url` 또는 `sources` 최소 1개 존재, 배열 상한, SHA-256 형식.
- **trusted validator가 최종 담당(스키마로 불가):**
  - 경로 **정규화** 검증 — 정규식은 최선의 방어일 뿐, `../`·`./`·심볼릭·정규화 후 탈출을
    validator가 정규 상대경로로 재확인.
  - 패킷 **직렬화 128KiB** 상한(파일 크기).
  - **파서/파일 레벨 케이스**(파싱된 객체로는 판별 불가): 중복 JSON 키 거부(표준 파서는
    마지막 값 채택하므로 strict 파서로 거부), 후행 개행(trailing newline) 정책, BOM.
  - claim 출처의 **실재·내용 일치**, `status: verified`의 진위 — 자기신고 verified로
    대체 금지, 공식 출처 독립 fetch로 확인(fetcher는 사설/메타데이터 목적지·불안전
    리다이렉트 거부, 바이트·시간 상한).
  - `checked_at`/`source_updated_at`의 의미(미상 발행일에 오늘 날짜 대체 금지).

## 스택 측 하드닝 케이스 호환 (agy 패킷 빌더)

스택 측 `runner/editorial_packet.py`가 강화 중인 거부 케이스에 대한 저장소 스키마 대응:

| 케이스 | 스키마 처리 | 비고 |
| --- | --- | --- |
| timezone 없는 `checked_at` | **거부** (pattern으로 RFC3339 tz 강제) | `format:date-time`은 비강제라 pattern 병행 |
| `./` 경로(선두·중간) | **거부** (`(^\|/)\.\.?(/\|$)` not) | `..`·`./` 모두 차단 |
| malformed `changed_paths`(비문자열·빈 배열) | **거부** (items type·minItems) | |
| 후행 개행(trailing newline) | validator/파일 레벨 | 스키마는 파싱된 객체만 봄 |
| 중복 JSON 키 | validator/파서 레벨 | strict 파서로 거부 |

## 경계와 주의 (계약과 일치)

- **형식 검증 ≠ 내용 신뢰.** 스키마 통과는 패킷의 *모양*만 보증하며, 근거 내용의 사실성은
  신뢰된 base-branch 정책(Actions)이 실제 diff·공식 출처로 독립 검증합니다.
- **`tier_hint`·`generated_by_llm`·`writer`는 입력 신호일 뿐** 최종 판정이 아닙니다.
  Actions가 실제 diff·근거로 재분류하며, 불명확/이견은 상향(escalate)하되 조용히 하향하지 않습니다.
  LLM 생성 편집은 최소 B이고, 출처 불명은 A로 낮추지 않습니다.
- **검증된 패킷 JSON만** 문서 스코프 카운팅에서 제외됩니다. 그 외 `.editorial/` 임의 변경은
  C/blocked로 취급합니다(무검증 경로 통째 제외 금지).
- 이 디렉터리는 `src/content/docs/` 밖이라 문서 린터(`lint-mermaid`/`lint-strikethrough`/
  `lint-docs-consistency`)와 Astro 빌드·콘텐츠 컬렉션의 대상이 아닙니다(회귀 테스트로 확인).

## 아직 하지 않은 것 (전환 전 금지)

- 운영 cutover, 기존 게이트 해제, 유료 추론 서비스 추가.

## 현행 상태: editorial 게이트 required 운영 중 (2026년 10월 기준)

**현재 상태 — 두 체크는 재도입되어 required로 운영 중이다:**

- `editorial-review`·`editorial-c-approval` 두 commit status는 `.github/workflows/editorial-c-approval.yml`
  단일 워크플로가 생성한다(별도 `editorial-review.yml` 파일은 없다). 매 PR(`pull_request`·
  `issue_comment`·`workflow_dispatch`)에서 실행된다.
- 두 체크는 master 브랜치 보호의 **required 체크**다. 현재 required는 7개다:
  `build`·`docs-consistency-lint`·`link-check`·`mermaid-lint`·`strikethrough-lint`·
  `editorial-review`·`editorial-c-approval`. `editorial-review`는 fail-closed이며
  게이트웨이 장애/토큰 만료/쿼터 소진을 pass로 바꾸지 않는다(장애 대응 런북은
  `CONTRIBUTING.md` "편집 리뷰 게이트와 장애 대응" 참고).
- `enforce_admins=false`를 유지한다(genuine outage 한정 관리자 비상 우회 허용).
- 관련 유지보수 커밋: 재도입 #179, concurrency 분리 #183, REVIEWER_POOL 도입 #190,
  required 트리거 paths 수정 #193·#195, fail-open 차단 #196.

### 과거 결정: shadow 워크플로 제거 (2026년 9월, 번복됨 — 히스토리 보존)

아래는 2026년 9월에 한 차례 내렸다가 이후 번복된 결정이다. #160에서 shadow 워크플로를
제거했으나, #179에서 PR 트리거 편집 리뷰 워크플로로 재도입하고 이후 required로 승격했다.
현행 상태는 위 절을 따른다.

- (당시 결정) `editorial-review.yml`·`editorial-c-approval.yml` 워크플로를 제거한다. 두 체크는
  required가 아닌 shadow 상태였고 병합을 강제하지 않았으나, 모든 PR에 fail/pending status를
  띄우는 노이즈만 발생시켰다.
- (당시 근거) C 승인 방식(allowlisted human이 64-hex packet SHA-256을 `/approve` 코멘트로 확인)이
  사람이 실제로 수행하기 어려운 마찰이라고 보았다. 상위 계약의 C 승인 정의 개정을
  `froguin/multi-agent-stack#139`로 요청했다.
- (당시에도 유지) `.editorial/` 도구(validator·classifier·review_runner·envelope·스키마·테스트)와
  `enforce_required_checks.sh`는 보존한다. 결정론적 5개 게이트(`build`·`link-check`·
  `mermaid-lint`·`strikethrough-lint`·`docs-consistency-lint`)는 불변이다.

### 더 이전 방침 (2026년 8월, 히스토리 보존)

- `editorial-review` · `editorial-c-approval`은 **shadow(비필수) 상태로 유지**한다. cutover 전까지 required로 등록하지 않는다. 두 체크는 PR에 판정 신호만 제공하고 병합을 강제하지 않는다.
- `enforce_admins=false`를 유지한다(관리자 비상 우회 허용). 계약 §Review(5)가 지적하듯 우회가 열려 있는 동안에는 이 게이트가 '엄격히 강제되는 발행 게이트'가 아니며, 이는 의도된 상태다.
- 근거: 아직 스택 draft-only cutover가 이루어지지 않았고(문서는 사람+AI가 직접 작성), 매 PR은 크로스 에이전트 리뷰로 품질을 담보한다. required 강제가 부과하는 매-PR 근거 패킷 작성 비용이 현시점의 실익을 초과한다. shadow 상태로도 "근거 패킷 없는 문서 변경"은 fail-closed 신호로 그대로 노출된다.
- 재검토 시점: 스택이 실제 자동 핸드오프(draft-only)를 시작하는 cutover 시점에 admin 우회 방침과 함께 다시 판단한다.

기술 선행조건은 이미 실증되어 있어(아래 절차 참고), 재검토 시 `enforce_required_checks.sh apply-enforce` 한 번으로 전환할 수 있다.

## 필요한 Secret / Variable (부모가 값 설정 — 코드는 값 안 읽음/안 만듦)

리뷰/게이트 워크플로우가 참조하는 이름. 실제 값은 스택 측이 발급·등록한다.

| 이름 | 종류 | 용도 | 최소 권한/요구 |
| --- | --- | --- | --- |
| `AI_GATEWAY_BASE_URL` | variable | Cloudflare AI Gateway OpenAI 호환 엔드포인트 | `https://gateway.ai.cloudflare.com/v1/<account_id>/ai-gateway/compat`. 비민감이라 variable |
| `AI_GATEWAY_TOKEN` | **secret** | 리뷰 호출용 Cloudflare API 토큰 | **AI Gateway Run 권한만**. 계정 마스터/글로벌 키 아님. merge/write 권한 없음 |
| `REVIEWER_MODEL` | variable | 리뷰어 모델 (`{provider}/{model}`) — 단일 리뷰어. `REVIEWER_POOL` 미설정 시 사용 | 패킷 `writer.model`과 **달라야** 함(writer-distinct) |
| `REVIEWER_PROVIDER` | variable | 리뷰어 공급자 — 단일 리뷰어 | writer provider와 **달라야** 함(같은 provider면 독립 아님) |
| `REVIEWER_POOL` | variable | 리뷰어 후보 배열(JSON). 설정 시 `REVIEWER_MODEL/PROVIDER`보다 우선 | `[{"model":"...","provider":"..."}, ...]`. writer와 겹치지 않는 **첫** 후보를 결정론적 선택. 전량 겹치면 `error`(pass 아님). JSON 파싱 실패 시 단일로 되돌아가지 않고 fail-closed |
| `EDITORIAL_C_APPROVAL_ALLOWLIST` | variable | C 승인 허용 GitHub 로그인(콤마구분) | 사용자 승인값 `froguin` (미설정 시 워크플로우 기본값 `froguin`) |

- **writer-distinct는 문자열이 아니라 정규화된 '실제 벤더'로도 판정한다.** provider/model 문자열이
  달라도 정규화 벤더가 같으면(예: writer=`anthropic`/`claude`, reviewer=`hf-inference`/`claude-3.5`)
  별칭 우회로 보고 `error` 처리한다. 어느 한쪽 벤더를 정규화할 수 없으면(모호) 역시 `error`(fail-closed).
  정규화가 곤란한 writer는 패킷 `writer.vendor`를 명시하면 그 값을 우선 사용한다.
- **Hugging Face를 리뷰어로 쓸 때 주의(하위계층 failover):** HF Inference Providers는 공급자
  장애 시 하위 계층에서 실제 추론 공급자를 자동 전환(failover)할 수 있다. runner가 폴백을 금지해도
  이 하위 전환은 writer-distinct 감사를 깰 수 있으므로, **실제 추론 공급자를 고정**하고 model·endpoint·
  인증 조합이 OpenAI 호환 `/chat/completions`를 지원하는지 SDK·HF·게이트웨이 전 계층에서 확인한 뒤
  `REVIEWER_POOL`에 넣는다. 프로바이더 연결 성공만으로는 충분하지 않다.
- `REVIEWER_POOL`을 쓰면 헬스체크 워크플로가 **pool의 모든 후보 model**을 프로브한다(하나라도
  만료/도달불가면 실패로 알림).

- 키 미설정 시 LLM 리뷰는 `skipped-unconfigured`(non-pass)로 동작하며 결정론적 5개
  게이트는 그대로 필수다. outage/quota/timeout도 절대 pass로 변환하지 않는다.
- 엔드포인트 fetcher는 사설/메타데이터 주소·불안전 리다이렉트를 거부하고 바이트·시간
  상한을 적용한다(계약 §Evidence). 리뷰 잡은 base 코드만 실행하고 PR은 데이터로만 쓴다.

## required 등록 상태와 롤백 절차

기존 결정론적 5개(`build`·`link-check`·`mermaid-lint`·`strikethrough-lint`·
`docs-consistency-lint`)에 더해 `editorial-review`·`editorial-c-approval`를 required로
등록하는 것은 **versioned script + rollback 기록**으로 적용한다(`enforce_required_checks.sh`).
현재는 두 체크가 **required로 등록되어 있다**(master 보호 7개). 게이트웨이 장애가 장기화돼
다수 PR이 막히면 `apply-rollback`으로 editorial 2개를 임시로 내리고(결정론적 5개 유지),
복구 후 `apply-enforce`로 다시 승격한다(런북은 `CONTRIBUTING.md` 참고).

기술 선행조건은 실증 완료 상태다:

- A/B/C/feature-only 판정, C 차단→packet SHA-256 확인 후 통과, 무관 커밋이 C를 리셋하지
  않음, provider outage 시 non-pass 보류(pass로 변환 안 함) — E2E로 실제 GitHub
  Actions·AI Gateway에서 확인.
- 스택↔저장소 **패킷 상호운용성** — 스택 `runner/editorial_packet.py`가 만든 패킷이 이
  저장소 `validate_packet.py`를 통과하고 packet SHA-256이 양측 동일함을 확인.

임시 롤백/재승격 순서: (1) `apply-rollback`으로 editorial 2개 제거 → (2) 장애 해소 후
`apply-enforce`로 재승격 → (3) 열려 있던 PR의 체크 상태 reconcile. `enforce_admins` 등 다른
브랜치 보호 설정은 이 스크립트가 건드리지 않는다.
