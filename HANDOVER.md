# HANDOVER — Starlight 마이그레이션 + 국가별 가이드 (2026-08-09)

다음 세션/에이전트를 위한 인수인계 문서. 완료 후 이 파일은 삭제해도 됨.

## 현재 상태 (프로덕션 라이브)

- **사이트**: https://cloudpick-docs.pages.dev (Cloudflare Pages, 프로젝트 `cloudpick-docs`, **프로덕션 브랜치는 `main`** — `wrangler pages deploy dist --project-name=cloudpick-docs --branch=main`으로 배포)
- **MCP 서버**: https://cloudpick-docs-mcp.froguin.workers.dev/mcp (`mcp/` 디렉터리, list_docs/search_docs/get_doc)
- **브랜치**: `feat/starlight-migration` (origin에 푸시됨). master 머지/PR은 미실행 — 사용자 결정 대기
- 304페이지: ko 전체(9섹션 + 국가 5개국 + 용어집), en 전체 번역, ja는 국가 가이드+랜딩만(나머지 한국어 폴백)

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

1. **랜딩 → 시작하기 리디렉션** (결정: 리디렉션 채택)
   - `starlight/public/_redirects`에 로케일별 3줄 추가: `/ko/ /ko/about-cloud/getting-started/ 302` (en/ja 동일 패턴)
   - 루트 `/ → /ko/` 301은 유지. index.mdx(CardGrid 랜딩)는 삭제하지 말 것 — 리디렉션만으로 전환하고, 되돌리기 쉽게 유지
2. **ja 전체 번역** (결정: 모든 문서 ko/en/ja 완역)
   - 대상: ja에 없는 일반 섹션 전체(약 69개 = 9개 섹션 68 + glossary). 기존 en 번역 때 쓴 방식 재사용: 섹션별 4~5분할 sonnet-worker, 규칙은 ja korea 번역 프롬프트(이 저장소 히스토리의 커밋 메시지와 기존 ja/korea 파일 문체) 참조
   - 완료 후 en/ja 스텁 금지 원칙 유지(미번역 파일은 만들지 않기)
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

## 남은 미결 사항

- **Pagefind 한국어 검색 품질**: 알려진 CJK 약점 — 실사용 평가 후 필요 시 대안 검색 검토
- 컷오버·main 머지 시점: 사용자 결정 (위 4·5번 항목 참조)

## 사용자 작업 스타일 (이 프로젝트)

- 벤더 중립, 한글 주표기+영문 병기, 사실 수정 시 참고하기에 출처 링크
- 기계적 작업은 sonnet/haiku 위임, 상위 모델은 설계·판단만 (전역 CLAUDE.md)
- 사실 검증은 외부 에이전트(grok/kiro/agy/codex) 교차 검증 선호, 병렬 실행 선호
- 국가 컴플라이언스 분리 시 원문서의 "왜/어떻게 생각해야 하는지" 본질 논의는 보존할 것
