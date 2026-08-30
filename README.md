# CloudPick Docs

CloudPick은 **멀티클라우드 환경에서 올바른 의사결정을 내리기 위한 벤더 중립 가이드**입니다.

멀티클라우드를 기본값으로 권장하지 않습니다. 단일 벤더, 하이브리드, 멀티클라우드는 각각의 비용과 책임이 있으며, 워크로드와 조직 상황에 따라 선택해야 합니다.

## 기술 스택

- [Astro](https://astro.build/) + [Starlight](https://starlight.astro.build/) — 정적 문서 사이트
- 3개 로케일: 한국어(ko, 기본), English(en), 日本語(ja)
- Netlify 배포 (정적 빌드 + MCP Serverless Function)
- 문서 데이터는 언어별로 Netlify Blobs에 저장 — 다국어 MCP(ko/en/ja)를 통해서만 접근 가능

## 개발

```bash
npm install
npm run dev       # 개발 서버 (localhost:4321)
npm run build     # dist/ 정적 빌드 + Blob 업로드
npm run preview   # 빌드 결과 로컬 프리뷰
```

## 프로젝트 구조

```
src/
  content/
    docs/
      ko/          ← 한국어 콘텐츠 (기본 로케일, SOT)
      en/          ← 영어 번역
      ja/          ← 일본어 번역
  styles/          ← 커스텀 CSS
public/            ← 정적 에셋 (폰트, 이미지)
netlify/           ← Netlify Functions (MCP 엔드포인트, Blob 헬스체크)
plugins/           ← 빌드 플러그인 (언어별 llms Blob 업로드)
scripts/           ← 빌드 후처리 (리디렉트 stub, 언어별 llms 생성), 문서 린터
config/            ← 로케일 단일 정의 (locales.mjs — 언어 목록 SOT)
astro.config.mjs   ← 사이트 설정, 사이드바, 로케일
netlify.toml       ← Netlify 빌드 + 리디렉트 설정
```

## 콘텐츠 구조

| 섹션 | 설명 |
|------|------|
| about-cloud/ | 클라우드 기초·의사결정·핵심 개념 |
| compute/ | VM, 컨테이너, 서버리스, 오토스케일링 |
| networking/ | VPC, LB, DNS, CDN, API Gateway |
| storage/ | 오브젝트, 블록/파일, 백업 |
| database/ | RDB, NoSQL, 캐시, 메시징, 분석 |
| devops/ | CI/CD, IaC, 모니터링, SLO |
| security/ | IAM, 시크릿, 데이터 보호, 제로 트러스트 |
| governance/ | 랜딩존, FinOps, DR, 컴플라이언스 |
| ai/ | AI/ML, RAG, 에이전트, LLMOps |
| korea/ us/ eu/ japan/ singapore/ | 국가별 규제 가이드 |

## i18n

- 기본 로케일: `ko` (한국어), SOT
- 전체 접두사 방식: `/ko/`, `/en/`, `/ja/`
- ko에 있는 문서는 en·ja도 동일 내용으로 완전 번역해 유지 — 3개 로케일 파일 구조·내용 대칭
- 콘텐츠 원본(SOT)은 `src/content/docs/ko/`

## MCP (AI 에이전트 연동)

AI 에이전트가 문서를 검색·조회할 수 있는 MCP 엔드포인트를 제공합니다.
문서 전문 데이터는 언어별로 Netlify Blobs에 저장되며(`llms-full-{ko,en,ja}`), MCP Function을 통해서만 접근 가능합니다.

- 엔드포인트: `https://docs.cloudpick.kr/mcp` (언어와 무관하게 단일 URL)
- 사용 가능한 도구:
  - `list_docs` — 전체 페이지 제목 목록
  - `search_docs` — 키워드 검색
  - `get_doc` — 특정 문서 전문 조회
- **다국어**: 세 도구 모두 선택적 `lang`(`ko`·`en`·`ja`) 파라미터를 받습니다. 미지정 시 검색어/제목의 문자로 언어를 판별하고(한글→ko, 가나→ja), 신호가 없으면 **기본값 ko(SOT)로 폴백**합니다. 응답은 사용 언어와 재요청 방법을 담은 헤더로 시작합니다.
- 자세한 설정·동작은 [문서의 MCP 페이지](https://docs.cloudpick.kr/ko/mcp/)를 참고하세요.

## 기여

[CONTRIBUTING.md](CONTRIBUTING.md)를 참고하세요.
