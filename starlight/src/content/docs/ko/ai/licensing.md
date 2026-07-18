---
title: "LLM 라이선스와 비용 관리"
description: "FM 제공사별 라이선스 티어(Seat/API), 3P 예약 용량, 비용 관리 도구와 패턴을 정리합니다."
---

# LLM 라이선스와 비용 관리

> 문서 기준: 2026년 7월

## Seat 플랜 vs API 티어

Seat(석 단위)과 API(토큰 단위)는 별개의 과금 체계입니다. 대부분의 엔터프라이즈는 둘을 병행합니다.

### OpenAI — Seat 기반

| 플랜 | 가격 | 대상 | Business와의 차이 |
| --- | --- | --- | --- |
| **Business** (구 Team) | ~$25/석/월 | 소규모 팀 (2석+) | — |
| **Enterprise** | ~$45-75/석/월 (협상, 150석+) | 대규모 조직 | SSO/SCIM, RBAC, 감사 로그, EKM, 데이터 레지던시, 커스텀 SLA, HIPAA 구성 |

**Business → Enterprise 업그레이드 시점:**
- 150석 이상 또는 보안/컴플라이언스 요건 (SSO 필수, 감사 로그, 데이터 레지던시)
- HIPAA 대상 데이터 처리 필요
- 조직 전체 거버넌스 (역할별 권한, 그룹별 크레딧 한도)

### OpenAI — API 티어

API는 누적 지출액에 따라 자동 승급됩니다. ([공식 Rate Limits 문서](https://platform.openai.com/docs/guides/rate-limits))

| 티어 | 조건 | 월 사용 상한 | RPM/TPM 수준 |
| --- | --- | --- | --- |
| Free | 허용 지역 | $100/월 | 낮음 |
| Tier 1 | $5 지출 | $100/월 | 중간 |
| Tier 2 | $50 지출 | $500/월 | 중간+ |
| Tier 3 | $100 지출 | $1,000/월 | 높음 |
| Tier 4 | $250 지출 | $5,000/월 | 높음+ |
| Tier 5 | $1,000 지출 | $200,000/월 | 최대 |

:::note
모델별 정확한 RPM/TPM 한도는 [Organization Limits 페이지](https://platform.openai.com/settings/organization/limits)에서 확인하세요.
:::

### Anthropic — Seat 기반

| 플랜 | 가격 | 대상 | Team과의 차이 |
| --- | --- | --- | --- |
| **Team Standard** | ~$25/석/월 | 소규모 팀 (5석+) | — |
| **Team Premium** | ~$125/석/월 | 고사용량 팀 | 더 높은 사용량 허용 |
| **Enterprise** | 협상 (석 + API 사용량 별도) | 대규모 조직 | SCIM, 감사 로그, Compliance API, CMEK, HIPAA/BAA, 조직별 지출 한도 |

**Team → Enterprise 업그레이드 시점:**
- HIPAA/BAA 필요
- SCIM 기반 사용자 프로비저닝
- 감사 로그 + Compliance API
- 암호화 키 직접 관리(CMEK)

### Anthropic — API 티어

| 티어 | 수준 | 비고 |
| --- | --- | --- |
| **Start** | 입문 | 낮은 RPM/TPM |
| **Build** | 개발/테스트 | 중간 |
| **Scale** | 프로덕션 | 높은 RPM/TPM, Enterprise 계약으로 커스텀 가능 |

공식 Rate Limits: [platform.claude.com/docs/en/api/rate-limits](https://platform.claude.com/docs/en/api/rate-limits)

---

## 3P 채널 예약 용량

| 벤더 | 방식 | 적합 시점 |
| --- | --- | --- |
| **Azure PTU** (Provisioned Throughput Unit) | 고정 시간당 과금, 처리량 보장 | 월 1.5–2억+ 토큰 이상 안정 트래픽 |
| **Bedrock Provisioned Throughput** | 모델 유닛 예약 (1/6개월 커밋) | 대량 안정 워크로드 + 지연시간 보장 |
| **Bedrock On-demand** | 토큰당 과금, 예약 없음 | 버스트/실험/불규칙 워크로드 |

:::note
예약 용량(PTU, Provisioned)은 사용하지 않아도 비용이 발생합니다. 정확한 가격과 손익분기점은 벤더 공식 페이지를 확인하세요.
:::

---

## 비용 및 사용량 관리

### 채널별 관리 도구

| 채널 | 비용 추적 | 예산/알림 | 팀별 할당 |
| --- | --- | --- | --- |
| **OpenAI** | Platform Usage Dashboard | 프로젝트별 월간 예산 상한 | Projects + API Keys |
| **Anthropic** | Console 사용량 대시보드 | 워크스페이스별 지출 캡 | Workspaces |
| **Azure Foundry** | Microsoft Cost Management | Azure Budgets + 알림 | 리소스 태그 (`project`, `team`) |
| **Bedrock** | AWS Cost Explorer + CUR 2.0 | AWS Budgets + Cost Anomaly Detection | 추론 프로파일 + 비용 할당 태그 |

### 엔터프라이즈 비용 관리 패턴

| 패턴 | 설명 |
| --- | --- |
| **Showback** | 팀별 사용량을 가시화하되 실제 청구는 하지 않음. 인식 개선 목적 |
| **Chargeback** | 팀 예산에서 실제 차감. 에이전트 비용 폭주 방지에 효과적 |
| **모델 라우팅** | 단순 작업은 경량 모델, 복잡한 작업만 프론티어 모델로 분기 |
| **토큰 예산** | 프로젝트/팀/사용자별 일/월 토큰 상한 |
| **AI 게이트웨이** | LiteLLM, Portkey 등으로 가상 키 발급, 하드 예산, 라우팅 제어 |

---

## 공식 가격 페이지

| 제공사 | URL |
| --- | --- |
| OpenAI Business/Enterprise | [openai.com/business/pricing](https://openai.com/business/pricing/) |
| OpenAI API 가격 | [openai.com/api/pricing](https://openai.com/api/pricing/) |
| Anthropic 플랜 | [claude.com/pricing](https://claude.com/pricing) |
| Anthropic API 가격 | [platform.claude.com/docs/en/about-claude/pricing](https://platform.claude.com/docs/en/about-claude/pricing) |
| Azure OpenAI 가격 | [azure.microsoft.com/pricing/details/azure-openai](https://azure.microsoft.com/en-us/pricing/details/azure-openai/) |
| Bedrock 가격 | [aws.amazon.com/bedrock/pricing](https://aws.amazon.com/bedrock/pricing/) |
| Upstage 가격 | [console.upstage.ai](https://console.upstage.ai/) |

## 관련 문서

- [LLM 채널 선택 가이드](1p-vs-3p.md) — 채널 패턴, Seat vs API 선택
- [AI 플랫폼과 모델 비교](ai-ml.md) — 모델 카탈로그, 추론 비용 최적화
- [FinOps](../governance/finops.md) — 클라우드 비용 거버넌스 전반
- [에이전트 도입 가이드](agent-adoption.md) — 에이전트 비용 관리
