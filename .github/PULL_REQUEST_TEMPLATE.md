<!--
CloudPick 문서 PR 템플릿.
편집 핸드오프 계약(froguin/multi-agent-stack@3113cfc docs/architecture/editorial-actions-contract.md)
및 저장소 측 참조(.editorial/README.md)를 따릅니다. 운영 cutover 전이며, 기존 발행 게이트가 유효합니다.
-->

## 변경 요약

<!-- 무엇을, 왜 바꿨는지 1~3문장. -->

## 근거 패킷 (evidence packet)

- [ ] `.editorial/packets/<jira_key>.json` 을 이 PR에 포함했습니다(스택 생성 초안인 경우).
- 스키마: `.editorial/packet.schema.json` (형식만 검증 — 내용 신뢰는 별개).

> `tier_hint`·`generated_by_llm`·`writer`는 **입력 신호일 뿐**입니다. 최종 tier 판정과 사실
> 검증은 신뢰된 base-branch 정책(Actions)이 실제 diff·공식 출처로 독립 수행합니다.
> 힌트만으로 자동 병합·승인·작성자‑리뷰어 독립성이 인정되지 않습니다.

## 위험 등급 (제안 — 확정 아님)

<!-- 제안일 뿐이며 Actions가 재분류합니다. 불명확/이견은 상향(C)되며 조용히 하향되지 않습니다. -->

- [ ] A — 순수 기계적 오타/형식/링크/렌더 수정, 로케일 합산 20줄 이하, 사실·구조 변경 없음
      (LLM 생성 편집은 A 불가 — 최소 B)
- [ ] B — 공식 근거 기반의 제한된 사실 갱신/번역, 명시적 범위 + 근거 + 독립 리뷰
- [ ] C — 신규/삭제/이동/병합/분할/카테고리/네비 변경, 법규·규제·컴플라이언스 주장,
      범위 불명/과대, 기존 human hold (→ 허가된 **사람**의 정확한 head SHA 승인 필요)

## 결정론적 체크 (LLM 무관, 항상 필수 — 병합 차단)

- [ ] `npm run build` 성공 (내부 링크 검증 포함 — 깨진 내부 링크·누락 파일 없음)
- [ ] `python3 scripts/lint-docs-consistency.py` 통과 (로케일 대칭성 · 문서 기준 마커 · `<details>` 금지)
- [ ] `python3 scripts/lint-mermaid.py` 통과
- [ ] `python3 scripts/lint-strikethrough.py` 통과
- [ ] 외부 링크 `External Link Check`(lychee + 한국 NCP) 통과 — PR 체크 기준(스케줄 이슈 아님)

## SOT·로케일

- [ ] Korean(ko)이 SOT이며, 공유 사실이 바뀌면 en·ja 대응 파일을 **같은 PR**에 포함했습니다.
- [ ] ko/en/ja 파일 구조가 대칭이고 사실·날짜·구조가 일치합니다.

## 관련 티켓

<!-- Jira: CLPKDOC-XXX (요약·링크만; 승인 권한은 PR/체크에 있음) -->
