# CloudPick Docs — Starlight 사이트

GitBook에서 마이그레이션된 멀티클라우드 기술 문서 사이트입니다.
Astro [Starlight](https://starlight.astro.build) 기반, Cloudflare Pages에 정적 배포합니다.

## 구조

- 콘텐츠 원본(한국어)은 **저장소 루트**의 GitBook 마크다운(`ai/`, `security/`, …)이며,
  `scripts/gitbook_to_starlight.py`가 `src/content/docs/ko/`로 변환·복사합니다.
  - 변환 내용: frontmatter title 승격, `{% hint %}`→`:::note` 계열, `{% tabs %}`→MDX Tabs,
    content-ref→링크, 상대 `.md` 링크→URL 경로, `GLOSSARY.md`→`glossary`
  - **`src/content/docs/ko/`의 일반 섹션 파일을 직접 수정하지 말 것** (재변환 시 덮어씀).
    루트 원본을 수정하고 스크립트를 재실행하세요.
- `src/content/docs/ko/korea/` — 한국 특화 문서(CSAP, 망분리, 소버린 AI 등).
  루트에 원본이 없는 Starlight 전용 콘텐츠로, 여기서 직접 편집합니다.
  `src/routeData.ts` 미들웨어가 en/ja 사이드바에서 이 그룹을 숨깁니다.
- `src/content/docs/en/` — 영어 번역본. 파일이 없으면 한국어로 폴백됩니다.
- `src/content/docs/ja/` — 일본어(현재 랜딩 페이지만, 나머지는 폴백).

## i18n

`defaultLocale: 'ko'`, 전체 접두사(`/ko/`, `/en/`, `/ja/`). 미번역 페이지는
한국어 콘텐츠 + "번역 없음" 안내로 자동 폴백됩니다.

## 명령어

```sh
npm run dev      # 개발 서버
npm run build    # dist/ 정적 빌드 (llms.txt, pagefind 인덱스 포함)
npx wrangler pages deploy dist --project-name=cloudpick-docs  # 배포
```

## AI 접근

- 빌드 시 `starlight-llms-txt` 플러그인이 `/llms.txt`, `/llms-full.txt`, `/llms-small.txt` 생성
- 원격 MCP 서버: `../mcp/` (Cloudflare Workers, llms-full.txt 기반 검색/조회)
