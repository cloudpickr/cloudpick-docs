# Editorial handoff — 저장소 측 참조

이 디렉터리는 multi-agent-stack → 문서 저장소 편집 핸드오프 계약의 **저장소 측 준비물**을 담습니다.
운영 전환(cutover)은 아직 이루어지지 않았으며, 기존 발행 게이트는 그대로 유효합니다.

## 계약 원본 (Source of Truth)

계약 본문은 이 저장소에 **사본을 두지 않습니다.** 아래 핀 커밋 링크를 단일 기준으로 참조합니다.

- **정규 계약(pinned):** `froguin/multi-agent-stack` 커밋 `3113cfc`
  `docs/architecture/editorial-actions-contract.md`
- 계약의 명확화 반영 및 핀 갱신은 **스택 측 책임**입니다. 여기의 핀만 따라 갱신합니다.
- 이전 핀: `e0dbbdc` (동일 본문 + 합의 명확화가 `3113cfc`에 반영됨).

## 이 디렉터리의 내용

- `packet.schema.json` — 근거 패킷(evidence packet) **형식 검증** 스키마(JSON Schema 2020-12).
  계약 §Evidence packet의 최소 필드를 반영합니다.
- `validate_packet.py` — 패킷 **trusted validator**(형식+파서/파일 레벨: 경로 정규화·128KiB·
  중복 JSON 키·trailing newline·BOM·checked_at RFC3339·target∈changed·파일명 일치).
- `classify_change.py` — 실제 diff+패킷으로 **A/B/C 재판정**(tier_hint는 입력일 뿐,
  LLM 생성 최소 B, 신규/삭제/이동/문서외/규제=C, 근거 없는 비기계적 변경은 C로 상향).
- `review_runner.py` — B/C **독립 LLM 리뷰**(LiteLLM 재사용, writer-distinct 강제, 예산·
  호출·토큰 상한, outage/미설정은 non-pass, PR 내용은 데이터). 미설정 시 shadow(non-pass).
- `envelope.py` — 리뷰 결과를 repo/PR/base_sha/head_sha/packet-SHA256/policy/reviewer-config
  튜플에 **바인딩**. 하나라도 바뀌면 이전 결과 무효(캐시 미스). freshness 만료 포함.
- `tests/` — 위 4개의 실제 단위 테스트(unittest).
- 패킷 실제 파일 위치(계약 제안): `.editorial/packets/<jira_key>.json` (draft PR에 포함).

관련 워크플로/스크립트(저장소 루트):
- `.github/workflows/editorial-c-approval.yml` — C 승인 게이트(status `editorial-c-approval`).
- `.github/scripts/c_approval_gate.cjs` (+`.test.cjs`) — A/B는 명시 pass, feature-only PR
  (문서 변경 없음 + 유효 패킷 없음)은 편집 scope 밖으로 명시 pass, C는 allowlisted human
  (봇/에이전트 제외)이 **현재 packet SHA-256을 코멘트로 confirm**해야 pass. 형식:
  `/approve <64-hex packet_sha256>`. GitHub PR Approve는 C 신호가 아니다. 무관한 커밋
  (CI/feature/merge)이 packet·문서 바이트를 바꾸지 않으면 C를 리셋하지 않는다.
  `EDITORIAL_C_APPROVAL_ALLOWLIST` 변수 미설정 시 C는 승인 불가(임의 승인자 없음).

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

- 운영 cutover, 기존 게이트 해제, 브랜치 보호 설정 변경, 유료 추론 서비스 추가.
- admin/bot 우회 차단 정책 확정 — cutover 전 별도로 정합니다.

## 필요한 Secret / Variable (부모가 값 설정 — 코드는 값 안 읽음/안 만듦)

리뷰/게이트 워크플로우가 참조하는 이름. 실제 값은 스택 측이 발급·등록한다.

| 이름 | 종류 | 용도 | 최소 권한/요구 |
| --- | --- | --- | --- |
| `AI_GATEWAY_BASE_URL` | variable | Cloudflare AI Gateway OpenAI 호환 엔드포인트 | `https://gateway.ai.cloudflare.com/v1/<account_id>/ai-gateway/compat`. 비민감이라 variable |
| `AI_GATEWAY_TOKEN` | **secret** | 리뷰 호출용 Cloudflare API 토큰 | **AI Gateway Run 권한만**. 계정 마스터/글로벌 키 아님. merge/write 권한 없음 |
| `REVIEWER_MODEL` | variable | 리뷰어 모델 (`{provider}/{model}`) | 패킷 `writer.model`과 **달라야** 함(writer-distinct) |
| `REVIEWER_PROVIDER` | variable | 리뷰어 공급자 | writer provider와 **달라야** 함(같은 provider면 독립 아님) |
| `EDITORIAL_C_APPROVAL_ALLOWLIST` | variable | C 승인 허용 GitHub 로그인(콤마구분) | 사용자 승인값 `froguin` (미설정 시 워크플로우 기본값 `froguin`) |

- 키 미설정 시 LLM 리뷰는 `skipped-unconfigured`(non-pass)로 동작하며 결정론적 5개
  게이트는 그대로 필수다. outage/quota/timeout도 절대 pass로 변환하지 않는다.
- 엔드포인트 fetcher는 사설/메타데이터 주소·불안전 리다이렉트를 거부하고 바이트·시간
  상한을 적용한다(계약 §Evidence). 리뷰 잡은 base 코드만 실행하고 PR은 데이터로만 쓴다.

## 실제 enforce(required 등록) 전환 절차 (검증 후)

기존 필수 5개(`build`·`link-check`·`mermaid-lint`·`strikethrough-lint`·
`docs-consistency-lint`)에 더해 `editorial-review`·`editorial-c-approval`를 required로
등록하는 것은 **versioned script + rollback 기록**으로 검증 후 적용한다. 이 저장소는
아직 등록하지 않았다(shadow-ready). admin/bot 우회 방침 확정도 전환 선행 조건이다.
