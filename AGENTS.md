## Development

When starting the dev server, use background mode:

```
astro dev --background
```

Manage the background server with `astro dev stop`, `astro dev status`, and `astro dev logs`.

## Multi-Agent Governance Protocol

본 리포지토리의 문서 관리와 확장은 5개 에이전트의 협업 체계로 운영됩니다.
- **참여 에이전트**: `codex`, `claude`, `kiro`, `grok`, `gemini`
- **분류/구조 변경 의결 규칙**:
  - 문서 분류 추가(새 카테고리, 도메인 신설, 사이드바 구조 개편, 신규 토픽 생성 등)는 반드시 다른 에이전트들과의 검토를 거쳐 **과반수 찬성(5개 에이전트 중 3표 이상)**을 획득해야 머지할 수 있습니다.
  - 테스트/임시 문서(예: `automation-trigger-test.md`)를 정식 문서로 승격하거나 사이드바에 편입할 때도 동일한 과반 찬성 절차가 적용됩니다.

## Source of Truth (SOT) 및 다국어 번역 원칙

- **한국어(ko)가 SOT(Source of Truth)**:
  - 모든 콘텐츠는 `src/content/docs/ko/`를 기준으로 먼저 작성·업데이트합니다.
  - `en/`과 `ja/`는 한국어 문서를 그대로 충실히 번역하여 100% 동일한 구조와 정보를 유지합니다.
- **글로벌 기준 작성 (한국 편향 최소화)**:
  - 한국어 본문을 작성할 때 한국 특화 표현(예: "한국 기업의 관점", "국내 엔터프라이즈", "한국의 CSAP처럼")을 최소화하고, 글로벌 엔터프라이즈 기준으로 서술해야 합니다. 그렇지 않으면 번역본(`en`, `ja`)에서 심각한 문맥 왜곡이 발생합니다.
  - 한국 고유의 규제, 인증, 법령(CSAP, 망분리, 전자금융감독규정, ISMS-P, 소버린 FM 등)은 반드시 국가별 가이드인 `src/content/docs/[locale]/korea/` 문서군으로 격리하여 다룹니다.
  - 글로벌 코어 문서 및 타국 가이드(`japan/`, `us/`, `eu/`, `singapore/`)에서는 특정 국가 시점이 아닌 중립적인 다국가·크로스보더 관점으로 서술합니다.
- **3개 로케일 대칭성 보장**:
  - 파일 추가, 수정, 삭제 시 `ko`, `en`, `ja` 세 언어의 파일 경로와 내용이 완벽하게 일치해야 합니다. 미번역 파일이나 고립된 테스트 문서를 남기지 않습니다.

## 문서 기준 및 사실 검증 원칙

- **기준 시점: 2026년 8월**:
  - 모든 문서는 `> 문서 기준: 2026년 8월` 기준 최신 정보를 반영합니다.
  - 과거 시점(2024~2025년 및 2026년 상반기)의 출시/발효 일정이 "예정"으로 남아있지 않도록 현행화합니다.
- **공식 출처 기반 & 교차검증(Cross-check)**:
  - 기술 사실, 서비스 명칭, 가격 체계, 법적 요건은 반드시 각 벤더(AWS, Azure, Google Cloud, OCI)의 최신 공식 문서, 표준 기구(NIST, CNCF, FinOps Foundation), 공식 법률/가이드라인을 교차검증하여 작성합니다.
  - 변경 의도나 기준이 모호한 경우 반드시 `git log`와 커밋 히스토리를 확인하여 이전 의사결정 맥락을 파악한 후 진행합니다.

## 표기 및 문체 규약

- **범위 표기 시 물결표(`~`) 금지**:
  - 마크다운(GFM) 취소선(`<del>`) 오렌더링 방지를 위해 반각 `~` 대신 엔대시 `–`(U+2013)를 사용합니다. (일본어 문서는 전각 `～` 사용)
  - `python3 scripts/lint-strikethrough.py` 린터를 통과해야 합니다.
- **중립적·객관적 문체**:
  - "최고의", "가장 뛰어난", "완벽한", "무결한" 등의 주관적·과장된 수식어는 엄격히 금지됩니다.
  - 기술적 트레이드오프와 벤더 중립성을 항상 유지합니다.

## 문서 형식 및 구조 일관성

문서 간 형식이 제각각이면 독자 경험과 접근성이 저해됩니다. 아래 규칙으로 전체 문서의 형식을 통일합니다.

- **접이식(`<details>`/`<summary>`) 금지**:
  - 접이식 블록은 딥링크(`#앵커`)로 진입 시 내용이 감춰지고, 페이지 내 검색(Pagefind)·스크린리더에서 콘텐츠가 누락되므로 사용하지 않습니다.
  - 상세 정보는 접지 말고 소제목(`###`/`####`)이나 표로 펼쳐서 항상 노출합니다.
- **보조 정보는 Starlight aside로 통일**:
  - 주의·참고·팁은 원시 HTML이나 위첨자 각주(`¹`, `> ¹ ...`)가 아니라 Starlight 네이티브 aside 문법(`:::note`, `:::caution`, `:::tip`)으로 작성합니다.
  - 표 셀에 각주 기호를 달아 표 밖에서 설명하는 방식 대신, 해당 제약·주의사항을 aside 블록으로 표 근처에 명시합니다.
- **Mermaid 다이어그램 작성 규칙**:
  - 노드 라벨에 슬래시(`/`), 괄호(`()`, `{}`) 등 특수문자가 포함되면 반드시 따옴표로 감쌉니다. 예: `C["3. 모델 전략<br/>(Buy/Build/Train)"]`.
  - 코드펜스는 순수 백틱(```` ```mermaid ````)만 사용하며 이스케이프된 백틱(`` \` ``)을 쓰지 않습니다.
  - `python3 scripts/lint-mermaid.py` 린터를 통과해야 합니다.
- **파일 확장자 기준 (`.md` vs `.mdx`)**:
  - JSX 컴포넌트(`<Tabs>`, `<Card>`, `<LinkCard>` 등)나 `import`가 실제로 필요한 문서만 `.mdx`로 작성합니다.
  - 순수 마크다운 문서(Starlight aside 커스텀 문법 `:::` 포함)는 `.md`를 사용합니다. 컴포넌트를 쓰지 않는 문서를 `.mdx`로 두지 않습니다.
- **사이드바 정보 아키텍처**:
  - 한 그룹의 문서가 많아지면 의미 단위 소그룹으로 분할하여 탐색성을 확보합니다.
  - 단, 사이드바 소그룹 신설·재편은 "분류/구조 변경"에 해당하므로 위 **Multi-Agent Governance Protocol**의 과반 의결 절차를 따릅니다.

## Documentation Reference

Full documentation: https://docs.astro.build

Consult these guides before working on related tasks:

- [Adding pages, dynamic routes, or middleware](https://docs.astro.build/en/guides/routing/)
- [Working with Astro components](https://docs.astro.build/en/basics/astro-components/)
- [Using React, Vue, Svelte, or other framework components](https://docs.astro.build/en/guides/framework-components/)
- [Adding or managing content](https://docs.astro.build/en/guides/content-collections/)
- [Adding styles or using Tailwind](https://docs.astro.build/en/guides/styling/)
- [Supporting multiple languages](https://docs.astro.build/en/guides/internationalization/)

