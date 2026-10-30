# scripts/ — 린터·스캐너·빌드 인벤토리

저장소 루트의 자동화 스크립트 목록입니다. 크게 **린터**(머지 차단/경고), **축별 스캐너·봇**(제보 전용 또는 가드), **빌드·인덱싱**으로 나뉩니다. 편집 리뷰 게이트의 엔진은 `.editorial/`에 있으며 그 소스 맵은 `.editorial/README.md`를 참조하세요.

## 린터 (문체·형식 규약)

AGENTS.md "표기 및 문체 규약 / 문서 형식 및 구조 일관성"을 기계적으로 검증합니다.

### 강제(required 또는 머지 차단)

| 스크립트 | 검사 | 게이트 |
| --- | --- | --- |
| `lint-docs-consistency.py` | ko/en/ja 경로 대칭 + 문서 기준 마커 + `<details>` 금지 | `docs-consistency-lint` (required) |
| `lint-strikethrough.py` | GFM 물결표(`~`) 취소선 오렌더링 | `strikethrough-lint` (required) |
| `lint-mermaid.py` | Mermaid 11.x 호환성(특수문자 따옴표·코드펜스) | `mermaid-lint` (required) |
| `lint-emphasis.py` | CJK 문맥의 볼드(`**`) 닫는 경계 | `emphasis-lint` |
| `leveling-guard.py` | 축4 교정 PR의 사실 불변 강제(결정론, LLM보다 먼저) | `leveling-guard` (라벨 기반) |
| `link-refresh-guard.py` | 축1 링크 현행화 PR의 'URL 교체만' 재구성 매칭 증명(결정론) | `link-refresh-guard`(패킷 자격 파생) + `editorial-review` diff 재구성 |

### 경고 전용(warn-only, 머지 비차단)

| 스크립트 | 검사 |
| --- | --- |
| `lint-duplication.py` | 문서 간 near-duplicate 문단 |
| `lint-readability.py` | 초장문 문단·문장 등 난이도 이상치 |
| `lint-taxonomy.py` | 사이드바 ↔ 실제 문서 정합성 |
| `lint-mcp-index.py` | 빌드 산출물 `dist/llms/*` 품질 |

## 축별 스캐너·봇 (4대 축 운영 모델)

봇은 **제보만** 합니다(`exit 0`, advisory). 사실 판정·문서 수정은 근거 패킷 PR로, 사람/에이전트가 합니다. 예외는 축4 레벨링(에이전트가 PR 작성, 사람은 머지 승인만). 자세한 경계는 AGENTS.md "자율성 경계" 참조.

| 스크립트 | 축 | 역할 |
| --- | --- | --- |
| `scan-stale-candidates.py` | 축1 | 노후 후보 결정론적 1차 추출 |
| `verify-stale-candidates.py` | 축1 | 추출 후보를 공식 출처로 대조·검증(제보) |
| `map-news-to-docs.py` | 축2 | 새 벤더 소식 → 후보 ko 문서 매핑(제보) |
| `post-news-map-comment.py` | 축2 | 매핑 결과를 월간 트래킹 이슈에 코멘트(제보) |
| `scan-leveling-candidates.py` | 축4 | 레벨링 후보 ko 문서 선별(제보) |
| `leveling-guard.py` | 축4 | 레벨링 PR 사실 불변 가드(차단) |
| `link-refresh-guard.py` | 축1 | 링크 현행화 PR의 URL-only 재구성 매칭 가드(차단) |
| `link-refresh-manifest.py` | 축1 | link-refresh 패킷 url_map 병합 + manifest_sha256 대조 |

## 빌드·인덱싱 (`.mjs`)

| 스크립트 | 역할 |
| --- | --- |
| `build-llms-locales.mjs` | 로케일별 `llms-full`/routing-index 생성(MCP용) |
| `write-locale-home-redirects.mjs` | 로케일 홈 리다이렉트 생성 |
| `check-korean-links.mjs` | 한국 도메인 외부 링크 검사(NCP 함수 연동) |
| `submit-indexing.mjs` | 검색 인덱싱 제출 |

`*.test.mjs`는 각 빌드 스크립트의 단위 테스트입니다.

## 실행 예

```sh
# 린터(강제)
python3 scripts/lint-docs-consistency.py
python3 scripts/lint-strikethrough.py
python3 scripts/lint-mermaid.py

# 축1 노후 스캔 → 검증
python3 scripts/scan-stale-candidates.py
python3 scripts/verify-stale-candidates.py

# 빌드(내부 링크 검증 포함)
npm run build
```
