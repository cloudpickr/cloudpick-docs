# HANDOVER — Starlight 마이그레이션 + 국가별 가이드 (2026-08-09)

다음 세션/에이전트를 위한 인수인계 문서. 완료 후 이 파일은 삭제해도 됨.

## 현재 상태 (프로덕션 라이브)

- **사이트**: https://cloudpick-docs.pages.dev (Cloudflare Pages, 프로젝트 `cloudpick-docs`, **프로덕션 브랜치는 `main`** — `wrangler pages deploy dist --project-name=cloudpick-docs --branch=main`으로 배포)
- **MCP 서버**: https://cloudpick-docs-mcp.froguin.workers.dev/mcp (`mcp/` 디렉터리, list_docs/search_docs/get_doc)
- **브랜치**: `feat/starlight-migration` (origin에 푸시됨). master 머지/PR은 미실행 — 사용자 결정 대기
- 304페이지: ko 전체(9섹션 + 국가 5개국 + 용어집), en 전체 번역, ja는 국가 가이드+랜딩만(나머지 한국어 폴백)

## 아키텍처 핵심 (회귀 주의)

- 루트 GitBook 마크다운 = ko 원본. `scripts/gitbook_to_starlight.py`로 `starlight/src/content/docs/ko/` 재생성 — **ko 일반 섹션 파일 직접 수정 금지**(korea/us/eu/japan/singapore/ 국가 디렉터리는 Starlight 전용이라 직접 편집)
- en/ja 미번역 파일은 만들지 말 것 — 파일이 없어야 한국어 폴백 작동
- 정적 출력이라 @astrojs/cloudflare 어댑터 금지(satteri wasm 빌드 오류 유발)
- 폰트: `public/fonts/` (Pretendard 동적 서브셋 + Jetendard Regular/Bold), `src/styles/custom.css`, config `head:`에 pretendard css 링크

## 방금 진행 중이던 작업 (이어서 할 것)

1. **en/ja 전파 에이전트** (sonnet-worker, codex 팩트체크 14건을 en/ja에 반영) — 세션 종료 시점에 실행 중이었음.
   - 완료 여부 확인: ko와 en/ja의 아래 마커 대조
     - `en/us/fedramp.md`·`ja/us/fedramp.md`에 "scope"/"범위" 기반 Class 설명이 반영됐는지 (ko는 "평가·인증의 범위" 표현)
     - `en/singapore/pdpa.md`에 CBPR 2020년 인정 언급이 있는지
   - 미반영이면: ko의 최신 문장(아래 14건 목록) 기준으로 en/ja 대응 문장 수정 후 빌드·배포
2. **codex 14건 목록** (ko는 반영 완료, en/ja 전파 대상):
   ismap 갱신주기 / appi 법정예외 추가 / appi 한-EU 적정성 표현 / fedramp Class=범위 분류(등급 대체 아님, fedramp.gov 원문 확인됨) / hipaa NPRM 2024.12 / hipaa 로그 6년 표현 / itar CONUS 일률의무 아님 / itar EAR 행정 $374,474 / EU Data Boundary 예외 존재 / DORA 20개 유형 / DORA CTPP 12개월 내 EU 자회사 의무 / MTCS Level3 일률 필수 아님 / PDPC 법적 구조 / PDPA CBPR 2020년부터 인정
3. 전파 완료 후: `cd starlight && npm run build` → `npx wrangler pages deploy dist --project-name=cloudpick-docs --branch=main --commit-dirty=true` → 커밋·푸시

## 크로스체크 검증 결과 (외부 에이전트 4종)

| 검증자 | 결과 | 반영 |
|---|---|---|
| grok | korea 치명2+경미3, 국가 경미6 | ✅ 3개 로케일 수정 완료 |
| codex | 국가 치명7+경미7 (법적 뉘앙스) | ✅ ko 완료, en/ja 전파 중 |
| kiro-cli | 치명0·경미0 (44건 확인) | — |
| agy | 치명0·경미0 (**codex 수정 후** 검증 = 사후 통과) | — |

- 상충 판별 사례: FedRAMP Class — grok "등급 대체 확인" vs codex "범위 분류" → fedramp.gov NTC-0004 원문으로 codex 손을 들어줌
- 외부 CLI 호출법: `grok --single "<프롬프트>" --always-approve` / `kiro-cli chat --no-interactive --trust-all-tools "<프롬프트>"` / `agy --dangerously-skip-permissions --print "<프롬프트>"` (**플래그 순서 중요** — --print 앞에) / `codex exec --sandbox read-only -c tools.web_search=true "<프롬프트>"` / gemini CLI는 지원 종료로 사용 불가
- 검증 상세 로그: 세션 scratchpad `crosscheck-*.md` (임시 — 세션 만료 시 소실 가능)

## 사용자 결정 대기 사항

1. **랜딩 페이지**: CardGrid 개편본 확인 후 유지 vs `/ko/ → 시작하기` 리디렉션(`_redirects` 한 줄)
2. **도메인 컷오버**: docs.cloudpick.kr을 Pages에 연결(현재 미연결, 리스크 없음). 연결 후 `mcp/wrangler.jsonc`의 DOCS_BASE_URL 변경 + `cd mcp && npx wrangler deploy`
3. **master 머지/PR**: feat/starlight-migration → master
4. **ja 일반 섹션 번역**: 현재 국가 가이드만 일본어, 나머지 한국어 폴백
5. **Pagefind 한국어 검색 품질**: 알려진 CJK 약점 — 실사용 평가 필요

## 사용자 작업 스타일 (이 프로젝트)

- 벤더 중립, 한글 주표기+영문 병기, 사실 수정 시 참고하기에 출처 링크
- 기계적 작업은 sonnet/haiku 위임, 상위 모델은 설계·판단만 (전역 CLAUDE.md)
- 사실 검증은 외부 에이전트(grok/kiro/agy/codex) 교차 검증 선호, 병렬 실행 선호
- 국가 컴플라이언스 분리 시 원문서의 "왜/어떻게 생각해야 하는지" 본질 논의는 보존할 것
