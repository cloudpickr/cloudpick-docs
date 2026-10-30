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
  - `python3 scripts/lint-docs-consistency.py` 린터(파일 경로 대칭성 검사)를 통과해야 합니다.

## 문서 기준 및 사실 검증 원칙

- **기준 시점: 2026년 9월**:
  - 모든 문서는 `> 문서 기준: 2026년 9월` 기준 최신 정보를 반영합니다. (en: `> Last reviewed: September 2026`, ja: `> 文書基準: 2026年9月`)
  - 기준 시점은 월 단위로 표기하며, 정기 리뷰(월 1–3회)를 거쳐 최신 월로 승격합니다.
  - 과거 시점(2024~2025년 및 2026년 상반기)의 출시/발효 일정이 "예정"으로 남아있지 않도록 현행화합니다.
  - 랜딩·웰컴 페이지(`index.mdx`, `introduction.mdx`)를 제외한 모든 문서는 이 기준 마커를 포함해야 하며, `python3 scripts/lint-docs-consistency.py` 린터(마커 존재 검사)를 통과해야 합니다.
- **공식 출처 기반 & 교차검증(Cross-check)**:
  - 기술 사실, 서비스 명칭, 가격 체계, 법적 요건은 반드시 각 벤더(AWS, Azure, Google Cloud, OCI)의 최신 공식 문서, 표준 기구(NIST, CNCF, FinOps Foundation), 공식 법률/가이드라인을 교차검증하여 작성합니다.
  - 변경 의도나 기준이 모호한 경우 반드시 `git log`와 커밋 히스토리를 확인하여 이전 의사결정 맥락을 파악한 후 진행합니다.
- **링크 유효성 검증(내부·외부)**:
  - **내부 링크**(상대 `../`·root-relative `/ko/..`)는 `npm run build`의 `starlight-links-validator`가 대상 존재 여부를 검증합니다. 깨진 내부 링크·누락 파일이 있으면 빌드가 실패해 머지가 차단됩니다.
  - **외부 링크**(`참고하기`의 공식 문서)는 CI(`External Link Check`, lychee)가 매 커밋 검사하며, 깨진 링크(404/410)는 차단됩니다. 리다이렉트(301/302/307/308)는 유효로 허용하되(lychee가 따라가 최종 200이면 통과), **실제 페이지 이전은 최종 URL로 갱신**합니다. 이때 로케일 세그먼트(`/en-us/` 등, 원본에 없었다면)와 추적 파라미터(`icid`·`utm_*`)는 원본에 없었다면 벗기고 버전 선택자(`view`·`tabs`·`pivots`)는 유지합니다 — 상세 원칙은 `CONTRIBUTING.md` "외부 링크 관리". 한국 도메인은 NCP 함수(`scripts/check-korean-links.mjs`)가 전담합니다.
  - 깨진 링크는 발견 즉시 유효한 공식 URL로 대체하거나 제거한 뒤 커밋합니다.
  - **상대 링크 깊이 함정(문서 이동·분할 시)**: `starlight-links-validator`가 통과해도 `trailingSlash: 'always'` 때문에 브라우저에서는 404가 나는 상대 링크가 있을 수 있습니다. 문서를 하위 디렉터리로 옮기거나 한 문서를 여러 문서로 **분할**하면 상대경로 깊이가 한 단계씩 어긋나므로, 이동·분할한 문서의 모든 `../`·`./` 링크를 새 위치 기준으로 재계산해야 합니다. 검증 방법(빌드 후 `dist` 상대경로를 브라우저 기준으로 풀어 실제 페이지 존재를 대조)은 `CONTRIBUTING.md`의 "상대 링크 깊이 함정"을 참고하세요.

## 문서 지속 관리 운영 모델 (4대 축)

이 리포지토리는 **반자율(semi-autonomous) 지속 유지보수 운영체계**로 운영됩니다. "반자율"은 정확한 명칭입니다 — **발굴·검증·초안 작성은 자동화**하되, **사실 판정과 머지는 사람이 관문**으로 두는 human-in-the-loop 설계이기 때문입니다. "완전 자율"이 아닙니다. 자동화가 담당하는 범위와 사람이 반드시 개입하는 경계는 아래 "자율성 경계"에서 불변 규칙으로 고정합니다.

원문인 **한국어(ko) 전체 문서**를 지속적으로 발굴·관리하여 최신성과 정확성을 유지합니다. 모든 변경은 **공식 웹 자료를 기준**으로 하며, **ko(SOT)를 먼저 수정한 뒤 en·ja에 동일하게 반영**합니다. 관리 범위는 네 가지 축입니다.

1. **유지보수(현행화)** — 기존 문서의 outdated 내용을 수정하거나 삭제합니다(예: 지난 "예정" 일정, Preview→GA 전환, 변경된 가격·리전 수).
2. **새 소식 반영** — 신규 벤더 발표를 **기존 범위 안에서** 관련 문서에 반영합니다.
3. **범위 확장** — 기존 범위를 벗어난 새 주제·구조(신규 카테고리·문서)를 추가합니다. 이는 분류/구조 변경이므로 위 **Multi-Agent Governance Protocol**의 과반 의결 대상입니다.
4. **재구성/교정** — 기존 구조의 결함이나 잘못된 서술을 바로잡거나 재구성합니다(예: 서술 오류·누락·중복, 낡은 아키텍처 전제, 섹션 불균형, 끊어진 교차참조).

### 통합 운영 루프

발굴(제보) → 트래킹 이슈 기록 → 결정론적 공식 출처 대조 → 사람/에이전트의 근거 패킷 PR(ko 먼저) → `editorial-review` 게이트의 출처 독립 재검증 → ko/en/ja 대칭 린트 → (필요 시) 문서 기준 마커 승격. 모든 발굴은 월간 트래킹 이슈(`monthly-review.yml`)로 모읍니다.

#### 자동화 현황 (어디까지 자동이고 어디부터 사람인가)

| 단계 | 담당 | 구현 |
| --- | --- | --- |
| 월간 트래킹 이슈 생성 | 자동 | `monthly-review.yml`(매월 1일) |
| 매일 벤더 새 소식 수집·이슈 코멘트 | 자동 | `monthly-review.yml`(daily) + `scripts/post-news-map-comment.py` |
| 축1 노후 후보 스캔·검증 | 자동(제보) | `scripts/scan-stale-candidates.py`·`verify-stale-candidates.py` |
| 축2 새 소식→문서 매핑 | 자동(제보) | `scripts/map-news-to-docs.py` |
| 축3 범위 확장 신호(미매핑 반복) | 자동(제보) | 축2 코멘트의 미매핑 누적 |
| 축1·2·3 사실 판정·문서 수정 | **사람/에이전트** | 공식 출처 확인 후 근거 패킷 PR |
| 축4 레벨링 PR 작성·보완 | 자동(에이전트) | `leveling-guard.py`·`leveling_core.py`(가드·의미보존 리뷰 전제) |
| 모든 PR 머지 승인 | **사람** | `editorial-review` 통과 + 사람 승인 |
| 축3 신규 카테고리·구조 신설 | **사람(과반 의결)** | 5에이전트 과반 찬성 |

이 경계가 "반자율"의 실체입니다. 봇·에이전트가 **발굴·검증·초안**까지 자동으로 끌고 오지만, **"이 사실이 맞다"는 판정과 머지**는 항상 사람(또는 사람이 승인하는 PR)을 거칩니다.

### 자율성 경계 (불변 규칙)

- **봇은 제보만 합니다.** 자동 스캔·검증 도구(`scripts/scan-stale-candidates.py`, `scripts/verify-stale-candidates.py`)는 `auto_edit:false`·`exit 0`·`status:advisory`이며, 문서를 스스로 수정하지 않고 required check로 승격하지 않습니다.
- **"제보 ≠ 판정", "매칭 없음 ≠ 최신", "인용 부분문자열 ≠ 모순 증명"**. 출처를 확인하지 못하면 `stale`이 아니라 `unverified`로 둡니다.
- **LLM은 보조 판정만** 하며, 단독으로 `contradicted`(모순) 결론을 내리지 않습니다(항상 `ambiguous` 이하로 보류). 키워드로 못 잡는 결함 대비 소규모 회전 샘플에만 사용합니다.
- **수정 착수는 사람/에이전트**가 공식 출처를 확인한 뒤 근거 패킷 PR로 합니다. 축3(범위 확장) 신설은 5에이전트 과반 의결을 거칩니다.

#### 축4 레벨링 한정 예외 (에이전트 자율 교정)

축1·축2의 "봇은 제보만" 원칙은 불변입니다. 단 **축4(재구성/교정) 중 '레벨링'(난이도·문장구조·분량 등 표현 교정)에 한해** 에이전트가 수정 PR을 직접 작성·보완할 수 있습니다(사람은 머지 승인만). 이때 다음 가드가 모두 전제됩니다.

- **표현만, 사실 불변** — `scripts/leveling-guard.py`(결정론)가 LLM보다 먼저 실행되어 코드·표·링크·수치·날짜·버전·고유명사·수식어 개수를 불변으로 강제합니다. 가드 실패는 LLM이 뒤집을 수 없습니다. **사실 변경은 레벨링이 아니라 축1 근거 패킷 경로**로 보냅니다.
- **의미 보존 리뷰** — 교정 writer와 **vendor-distinct**한 독립 리뷰어가 닫힌 enum(`negation_flip`/`modality_drop`/`omission_of_condition`/`vendor_tilt`)만 차단 신호로 냅니다. 유일한 수정은 해당 hunk revert이며, 리뷰어 이견은 `human-hold`입니다.
- **빈 `claim_ledger`는 정당** — 레벨링은 새 사실 주장이 없으므로 패킷의 claim_ledger가 비어도 됩니다(출처 날조 금지). 패킷 `tier_reasons`에 레벨링 성격을 명시합니다.
- **루프 상한** — 자동 수정 1라운드 + 24시간. 가드 재실패·동일 findings 반복·리뷰어 이견·범위 확대 시 `human-hold`로 정지합니다.
- **범위 제한** — 레벨링 PR은 1개 논리 문서 + ko/en/ja 미러만. 제목 변경·분할·이동·사이드바 등 구조 변경은 레벨링에 포함할 수 없고 별도 제안 + 과반 의결입니다.
- 상세 기준은 `.editorial/leveling-rules.yaml`(권위 원본)을 따릅니다.

#### 축1 링크 현행화 예외 (link-refresh — URL-only 자율 교정)

리다이렉트가 **실제 페이지 이전**을 가리킬 때, 외부 링크를 최종 URL로 일괄 갱신하는 것(link-refresh)은 레벨링과 같은 "사실 불변" 성격이라 에이전트가 PR을 직접 작성할 수 있습니다(모든 경로에 사람 승인 필수). 전제 가드:

- **URL 문자열만 교체, 그 외 바이트 불변** — `scripts/link-refresh-guard.py`(결정론)가 '재구성 매칭'으로 증명합니다: 승인된 old→new 매핑을 base에 적용한 결과가 head와 바이트 일치해야 하며, 라인 증감·코드/frontmatter/인라인코드/mermaid 내부 변경·URL 외 텍스트 변경은 fail-closed. **사실·문장 변경은 link-refresh가 아니라 축1 근거 패킷 경로**로 보냅니다.
- **로케일·버전 파라미터 규칙** — 최종 URL에서 원본에 없던 로케일 세그먼트(`/en-us/` 등)와 추적 파라미터(`icid`·`utm_*`)는 벗깁니다. `?view=`·`?tabs=`·`?pivots=`는 버전 선택자이므로 유지합니다. path-collapse(하위→상위 축약)나 edition/version 토큰 변경은 사람이 확인합니다. 현재 이를 자동 탐지하지 않으므로 모든 link-refresh는 C입니다.
- **빈 `claim_ledger` + manifest** — 새 사실 주장이 없으므로 claim_ledger는 비웁니다. 패킷 `policy_action: "link-refresh"`(이 단일 필드가 자격을 부여) + `link_refresh.url_map`(old→new) + `manifest_sha256`(전체 경로·매핑·base SHA 해시)로 대량 분산 변경의 완전성을 보증합니다(changed_paths 64 상한 우회). CI가 manifest를 재계산해 대조하며, 리뷰 envelope은 별도로 실제 head SHA에 바인딩합니다.
- **독립 리뷰 재fetch** — 게이트가 url_map의 각 old URL을 독립 re-fetch해 리다이렉트 체인이 new URL로 끝남을 확인합니다(최종 HTTP 성공 상태 확인; soft-404·path-collapse·edition 변경은 별도 검토 필요). 불일치·fetch 불가는 비승인(hold).
- **모든 경로는 C** — 리다이렉트만으로 soft-404·path-collapse·판본 변경을 완전히 판별할 수 없으므로 비규제·규제 경로 모두 사람 승인(C)이 필요합니다. core와 규제 PR은 검토를 위해 분리합니다.
- `policy_action=="link-refresh"`은 C를 부여하며 `editorial-review`에서 신뢰된 base 가드로 전체 파일 및 매니페스트 검증을 강제합니다. 별도 `link-refresh-guard` 잡도 라벨이 아니라 패킷에서 실행 여부를 파생합니다. 해당 잡을 required로 등록하려면 관리자 설정이 별도로 필요합니다.

### 체크리스트 (변경 PR 공통)

- [ ] 변경 근거가 **벤더 공식 문서/표준 기구/공식 법령**인가(2차 보도는 보조). `.editorial/` 근거 패킷의 `source_url`로 제시했는가
- [ ] ko(SOT)를 먼저 수정하고 en·ja에 동일 반영했는가(`lint-docs-consistency.py` 대칭 통과)
- [ ] outdated 내용을 "예정" 미래형으로 남기지 않았는가(지난 시점은 현행화·중립화)
- [ ] 구조 변경(이동·분할·신규 카테고리)이면 상대 링크 재계산 + 과반 의결 여부를 확인했는가

### 강제 게이트 (머지 차단)

- `editorial-review` — 근거 패킷의 각 `source_url`을 독립 fetch해 재검증(공식 교차검증 강제).
- `lint-docs-consistency.py` — ko/en/ja 경로 대칭 + 문서 기준 마커.
- `npm run build`(내부 링크) · `External Link Check`(외부 링크) · `lint-strikethrough` · `lint-mermaid`.

## 표기 및 문체 규약

- **범위 표기 시 물결표(`~`) 금지**:
  - 마크다운(GFM) 취소선(`<del>`) 오렌더링 방지를 위해 반각 `~` 대신 엔대시 `–`(U+2013)를 사용합니다. (일본어 문서는 전각 `～` 사용)
  - `python3 scripts/lint-strikethrough.py` 린터를 통과해야 합니다.
- **볼드(`**`) 경계 밀착 금지**:
  - 볼드 마커 `**`가 구두점이나 CJK 문자와 밀착해 렌더링이 깨지지 않도록 작성합니다.
  - `python3 scripts/lint-emphasis.py` 린터를 통과해야 합니다.
- **중립적·객관적 문체**:
  - "최고의", "가장 뛰어난", "완벽한", "무결한" 등의 주관적·과장된 수식어는 엄격히 금지됩니다.
  - 기술적 트레이드오프와 벤더 중립성을 항상 유지합니다.

## 문서 형식 및 구조 일관성

문서 간 형식이 제각각이면 독자 경험과 접근성이 저해됩니다. 아래 규칙으로 전체 문서의 형식을 통일합니다.

- **접이식(`<details>`/`<summary>`) 금지**:
  - 접이식 블록은 딥링크(`#앵커`)로 진입 시 내용이 감춰지고, 페이지 내 검색(Pagefind)·스크린리더에서 콘텐츠가 누락되므로 사용하지 않습니다.
  - 상세 정보는 접지 말고 소제목(`###`/`####`)이나 표로 펼쳐서 항상 노출합니다.
  - `python3 scripts/lint-docs-consistency.py` 린터(접이식 블록 검사)를 통과해야 합니다.
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

