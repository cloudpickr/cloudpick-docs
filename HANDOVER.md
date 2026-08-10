# HANDOVER — Starlight 마이그레이션 + 국가별 가이드 (2026-08-09)

다음 세션/에이전트를 위한 인수인계 문서. 완료 후 이 파일은 삭제해도 됨.

## 현재 상태 (프로덕션 라이브)

- **사이트**: https://cloudpick-docs.pages.dev (Cloudflare Pages, 프로젝트 `cloudpick-docs`, **프로덕션 브랜치는 `main`** — `wrangler pages deploy dist --project-name=cloudpick-docs --branch=main`으로 배포)
- **MCP 서버**: https://cloudpick-docs-mcp.froguin.workers.dev/mcp (`mcp/` 디렉터리, list_docs/search_docs/get_doc)
- **브랜치**: `feat/starlight-migration` (origin에 푸시됨). master 머지/PR은 미실행 — 사용자 결정 대기
- 304페이지: **ko/en/ja 3개 로케일 완역**(로케일당 101개 파일, 폴백 0)

## 아키텍처 핵심 (회귀 주의)

- 루트 GitBook 마크다운 = **전체 콘텐츠 SOT** (일반 9섹션 + `korea/`/`us/`/`eu/`/`japan/`/`singapore/` 국가 가이드 포함). `scripts/gitbook_to_starlight.py`로 `starlight/src/content/docs/ko/` 재생성 — **starlight/src/content/docs/ko/ 직접 수정 금지**. 국가 가이드도 루트에서 수정 후 변환 스크립트 실행.
- 기본 변환: `python3 scripts/gitbook_to_starlight.py` (코어+국가 전부). 국가만: `python3 scripts/gitbook_to_starlight.py korea us eu japan singapore`
- 사이드바 국가 index 라벨은 `astro.config.mjs`에서 "한국 개요" 등으로 그룹명과 구분 (P0-2)
- Round2 크로스리뷰 반영 요약: about-cloud/DevOps/AI 사이드바 서브그룹, ja 소버린 앵커 언어 종속 슬러그 제거, CONTRIBUTING에 i18n 티어·fallback 정책 문서화, 국가 관련 문서 포맷 통일(불릿), 글로벌 망분리에 US/EU 역참조
- en/ja 미번역 파일은 만들지 말 것 — 파일이 없어야 한국어 폴백 작동
- 정적 출력이라 @astrojs/cloudflare 어댑터 금지(satteri wasm 빌드 오류 유발)
- 폰트: `public/fonts/` (Pretendard 동적 서브셋 + Jetendard Regular/Bold), `src/styles/custom.css`, config `head:`에 pretendard css 링크

## 다음 세션 작업 목록 (사용자 결정 반영됨 — 2026-08-09)

사용자가 결정한 사항. 다음 세션은 이 순서대로 실행하면 됨.

1. ~~랜딩 → 시작하기 리디렉션~~ ✅ 완료 (2026-08-09, `/`·로케일 홈 → 각 시작하기 302, CardGrid 랜딩 파일은 보존)
2. ~~ja 전체 번역~~ ✅ 완료 (2026-08-09, 80개 문서 — 3개 로케일 101파일 대칭, 헤딩 구조 전수 일치 검증, ソブリンランディングゾーン 앵커 연동 수정 포함)
3. **운영 원칙**: 루트 GitBook 문서 업데이트 시 반드시 `python3 scripts/gitbook_to_starlight.py` 재실행으로 Starlight 동기화 후 빌드·배포 (이중 관리 아님 — 루트가 원본, starlight/ko는 파생)
4. **main 머지 시 repo 재구성** (컷오버와 함께, 시점은 사용자가 결정)
   - Starlight + Workers MCP 중심으로 저장소 재편: GitBook 유산(SUMMARY.md, index.html, _book/, .github의 GitBook 워크플로 등) 정리
   - 검토 필요: 루트 마크다운을 원본으로 유지할지, starlight/src/content/docs/ko를 원본으로 승격하고 변환 스크립트를 폐기할지 — 후자면 CONTRIBUTING.md 개정 필요
   - MCP `DOCS_BASE_URL`을 docs.cloudpick.kr로 변경 + 재배포는 도메인 연결 시점에
5. **컷오버(도메인 연결)는 보류** — 사용자가 시점 결정

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

## Netlify 이전 준비 (2026-08-10, 브랜치 `claude/starlight-netlify-i18n-spxhio`)

- 목적: 페이지는 퍼블릭 유지하되 **`llms*.txt` 합본은 공개 URL로 노출하지 않음** (사용자 결정)
- `starlight/netlify.toml`(사이트 base=`starlight`) + `netlify/functions/mcp.mts`(Streamable HTTP stateless, `/mcp`) 추가
- `npm run build:netlify` = astro build + `scripts/extract-mcp-data.mjs`(llms*.txt를 dist에서 제거, llms-full.txt만 `mcp-data/`로 추출 → 함수 번들 `included_files`)
- **기존 `npm run build`는 무변경** — 현행 Cloudflare Workers MCP(`mcp/`)는 공개 llms-full.txt fetch에 의존하므로, 컷오버 전 Cloudflare 배포는 계속 `npm run build` 사용
- 컷오버 시: Netlify 사이트 생성(base=starlight) → 도메인 연결 → MCP 클라이언트 엔드포인트를 `https://<사이트>/mcp`로 변경 → `mcp/`(Workers)와 위 4번의 `DOCS_BASE_URL` 항목은 폐기 가능

## 국가 중립화 리팩터링 (2026-08-10, 같은 브랜치)

- 원칙(사용자 결정): **일반 9섹션은 국가 중립** — 국가 특화 절·표는 국가 가이드로 이동, 문장 단위는 다국 병렬 예시("예: 한국 CSAP, 미국 FedRAMP")로 중립화. **언어(한국어 검색·형태소·예시 프롬프트) 관련은 유지**.
- 신규 문서: `korea/market.md`(한국 리전·국내 DR·KINX PoP·MSP·커뮤니티) — SUMMARY.md·사이드바(korea/market) 등록됨
- 주요 이동: network-isolation의 CSAP/N²SF 표(korea와 중복이라 삭제), regions-and-zones·dr·1p-vs-3p·compare-clouds·multicloud-networking·support-plans·compliance의 한국 절
- en/ja 동기화 필수 — 헤딩 구조 3로케일 대칭 유지. 이후 일반 문서에 국가 내용 추가 시 같은 원칙 적용할 것

## 남은 미결 사항

- **Pagefind 한국어 검색 품질**: 알려진 CJK 약점 — 실사용 평가 후 필요 시 대안 검색 검토
- 컷오버·main 머지 시점: 사용자 결정 (위 4·5번 항목 참조)

## 사용자 작업 스타일 (이 프로젝트)

- 벤더 중립, 한글 주표기+영문 병기, 사실 수정 시 참고하기에 출처 링크
- 기계적 작업은 sonnet/haiku 위임, 상위 모델은 설계·판단만 (전역 CLAUDE.md)
- 사실 검증은 외부 에이전트(grok/kiro/agy/codex) 교차 검증 선호, 병렬 실행 선호
- 국가 컴플라이언스 분리 시 원문서의 "왜/어떻게 생각해야 하는지" 본질 논의는 보존할 것
