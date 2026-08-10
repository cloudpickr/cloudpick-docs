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
npm run dev              # 개발 서버
npm run build            # dist/ 정적 빌드 (llms*.txt 포함 — Cloudflare Pages 배포용)
npm run build:netlify    # 위 빌드 + llms*.txt를 dist에서 추출해 비공개화 (Netlify 배포용)
npx wrangler pages deploy dist --project-name=cloudpick-docs  # Cloudflare Pages 배포 (현행 프로덕션)
```

## 배포 — Netlify (컷오버 대상)

- `netlify.toml` 사용: Netlify 사이트의 **base directory를 `starlight`로 지정**하면
  빌드(`build:netlify`)·publish(`dist`)·MCP 함수가 한 배포로 묶인다.
- 원격 MCP 서버: `netlify/functions/mcp.mts` → `https://<사이트>/mcp`
  (Streamable HTTP, stateless — 도구는 기존과 동일한 list_docs / search_docs / get_doc).
- **`llms*.txt`는 공개 URL로 서빙되지 않는다**: `build:netlify`가 dist에서 제거하고
  `llms-full.txt`만 `mcp-data/`로 추출 → `included_files`로 MCP 함수 번들에 포함.
  문서와 데이터셋이 같은 배포에 원자적으로 묶여 버전 불일치도 없다.
- 주의: 기존 Cloudflare 경로(`../mcp/` Workers)는 **공개 llms-full.txt를 fetch하는 구조**이므로,
  컷오버 전까지 Cloudflare Pages 배포는 반드시 추출 없는 `npm run build`로 할 것.

## AI 접근

- 빌드 시 `starlight-llms-txt` 플러그인이 `llms.txt`, `llms-full.txt`, `llms-small.txt` 생성
- Cloudflare(현행): 위 파일이 공개 서빙되고, 원격 MCP는 `../mcp/`(Workers)가 이를 fetch
- Netlify(신규): 위 파일 비공개 — MCP 함수가 번들 내 `mcp-data/llms-full.txt`를 직접 읽음
