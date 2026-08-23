# CloudPick Docs

CloudPick은 **멀티클라우드 환경에서 올바른 의사결정을 내리기 위한 벤더 중립 가이드**입니다.

멀티클라우드를 기본값으로 권장하지 않습니다. 단일 벤더, 하이브리드, 멀티클라우드는 각각의 비용과 책임이 있으며, 워크로드와 조직 상황에 따라 선택해야 합니다.

🌐 **사이트**: <https://docs.cloudpick.kr>

## 기술 스택

- [Astro](https://astro.build/) + [Starlight](https://starlight.astro.build/) — 정적 문서 사이트
- 3개 로케일: 한국어(ko, 기본), English(en), 日本語(ja)
- Netlify 배포 (정적 빌드 + `/mcp` Serverless Function)
- `starlight-llms-txt` 플러그인으로 `/llms.txt`, `/llms-full.txt` 자동 생성

## 개발

```bash
npm install
npm run dev       # 개발 서버 (localhost:4321)
npm run build     # dist/ 정적 빌드
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
netlify/           ← Netlify Functions (MCP 엔드포인트)
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

- 기본 로케일: `ko` (한국어)
- 전체 접두사 방식: `/ko/`, `/en/`, `/ja/`
- 미번역 파일은 만들지 않음 — 파일이 없으면 한국어로 폴백
- 콘텐츠 원본(SOT)은 `src/content/docs/ko/`

## AI 접근

- 빌드 시 자동 생성: `/llms.txt`, `/llms-full.txt`, `/llms-small.txt`
- MCP 엔드포인트: `https://docs.cloudpick.kr/mcp` (Netlify Function)

## 기여

[CONTRIBUTING.md](CONTRIBUTING.md)를 참고하세요.
