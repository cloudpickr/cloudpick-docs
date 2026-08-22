# CloudPick Docs — Starlight 사이트

GitBook에서 마이그레이션된 멀티클라우드 기술 문서 사이트입니다.
Astro [Starlight](https://starlight.astro.build) 기반 정적 사이트입니다.

배포:

- **Netlify** (`netlify.toml`) — 정적 `dist/` + `/mcp` Function
- **Cloudflare Pages** (대안) — `dist/`만 업로드. MCP는 `../mcp/` Workers가 담당

`@astrojs/cloudflare` 어댑터는 사용하지 않습니다 (wasm 빌드 오류).

## 구조

- 콘텐츠 원본(한국어)은 **저장소 루트**의 GitBook 마크다운(`ai/`, `security/`, …)이며,
  `scripts/gitbook_to_starlight.py`가 `src/content/docs/ko/`로 변환·복사합니다.
  - 변환 내용: frontmatter title 승격, `{% hint %}`→`:::note` 계열, `{% tabs %}`→MDX Tabs,
    content-ref→링크, 상대 `.md` 링크→URL 경로, `GLOSSARY.md`→`glossary`
  - **`src/content/docs/ko/`의 일반 섹션 파일을 직접 수정하지 말 것** (재변환 시 덮어씀).
    루트 원본을 수정하고 스크립트를 재실행하세요.
- `src/content/docs/{ko,en,ja}/` — 3개 로케일 대칭 번역 (로케일당 동일 페이지).
  파일이 없으면 한국어로 폴백됩니다. 미번역 파일을 만들지 마세요.

## i18n

`defaultLocale: 'ko'`, 전체 접두사(`/ko/`, `/en/`, `/ja/`).
`/`, `/ko/`, `/en/`, `/ja/` 는 각 로케일 소개 페이지로 리디렉션됩니다.

## 명령어

```sh
npm run dev      # 개발 서버
npm run build    # dist/ 정적 빌드 (llms.txt, pagefind, 로케일 홈 리디렉션 stub)
```

Netlify는 `starlight/`를 베이스 디렉터리로 빌드합니다.

## AI 접근

- 빌드 시 `starlight-llms-txt` 플러그인이 `/llms.txt`, `/llms-full.txt`, `/llms-small.txt` 생성
- MCP 엔드포인트: `https://cloudpick-docs.netlify.app/mcp` (Netlify Function, 문서 사이트와 동일 오리진)
