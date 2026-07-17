---
description: 동일한 FM을 1P(모델 제공사 직접)와 3P(클라우드 플랫폼 경유)로 소비할 때의 차이를 비교합니다.
---

# LLM 채널 선택: 1P vs 3P

> 문서 기준: 2026년 7월

## 개요

FM을 도입할 때 **두 가지 독립적인 선택**이 있습니다. 이 둘은 별개의 결정입니다.

| 선택 축 | 질문 | 옵션 |
| --- | --- | --- |
| **① 이용 형태** | 누가, 어떻게 쓰나? | Seat(채팅 UI) / API(코드 통합) / 셀프호스팅 |
| **② 채널** | 어디서 구매·운영하나? | 직접 이용(1P) / 클라우드 제공(3P) / 모델사+클라우드 결제 |

```
예) "Claude를 API로 Bedrock에서 사용" 
     → 이용 형태: API  
     → 채널: 클라우드 제공 (3P Inference)

예) "ChatGPT를 전 직원에게 Enterprise로 제공"
     → 이용 형태: Seat (Enterprise)
     → 채널: 직접 이용 (1P)
```

이 문서는 먼저 **① 이용 형태**(Seat vs API)를 정리한 뒤, **② 채널**(1P vs 3P)을 비교합니다.

---

## ① 이용 형태: Seat vs API

| 구분 | Seat 기반 플랜 | API 플랫폼 |
| --- | --- | --- |
| **누가 사용** | 비개발자 포함 전 직원 (채팅 UI) | 개발팀 (코드에서 호출) |
| **과금 단위** | 월 석당 고정 요금 | 사용한 토큰당 과금 |
| **용도** | 업무 보조, 문서 작성, 분석, 검색 | 제품 내 AI 기능, 자동화, 에이전트 |
| **거버넌스** | 어드민 콘솔, 사용량 대시보드 | API 키/프로젝트별 예산, 프로그래밍 제어 |
| **비용 예측** | 석 수 × 단가 = 고정 | 사용량에 따라 변동 (예측 어려움) |

**선택 기준:**
- 직원들이 ChatGPT/Claude를 **채팅 UI로** 사용 → **Seat 기반** (Business/Team)
- 자사 제품/서비스에 LLM을 **코드로 통합** → **API**
- 둘 다 필요 → **Seat 플랜 + API를 별도로 운영** (대부분의 엔터프라이즈)

### API를 쓸 때: 왜 3P(클라우드 경유)를 선택하나

엔터프라이즈가 API를 코드에서 호출할 때, 모델사 직접(1P)보다 **3P(Bedrock/Vertex/Azure Foundry)를 선택하는 경우가 많습니다.**

| 3P를 선택하는 이유 | 설명 |
| --- | --- |
| **기존 클라우드 커밋 소진** | AWS EDP, Azure EA/MACC가 있으면 LLM 비용을 기존 약정에서 차감 가능 |
| **네트워크 격리** | VPC/Private Link로 트래픽이 퍼블릭 인터넷을 경유하지 않음 |
| **컴플라이언스 활용** | 클라우드 벤더의 기존 인증(HIPAA, SOC 2 등) 활용 가능 |
| **통합 빌링/거버넌스** | 기존 청구서에 합산, 비용 태그로 팀별 추적, IAM으로 접근 제어 |
| **단일 계약** | 조달 부서가 새 벤더를 추가할 필요 없이 기존 계약 내 사용 |
| **멀티모델 접근** | 하나의 플랫폼에서 여러 모델을 동일 API로 전환 가능 |

| 그래도 1P를 선택하는 이유 | 설명 |
| --- | --- |
| **최신 모델/기능** | 신규 모델과 베타 기능이 1P에 먼저 출시 |
| **풀 기능** | Fine-tuning, Realtime API 등 3P에 없거나 지연되는 기능 |
| **간단한 시작** | 카드 등록 즉시 사용, 클라우드 설정 불필요 |
| **클라우드 비종속** | 특정 클라우드에 의존하지 않음 |

{% hint style="info" %}
대규모 엔터프라이즈의 일반적 패턴: **프로덕션은 3P** (거버넌스, 커밋 소진, 격리) + **실험은 1P** (최신 기능, 빠른 시작).
{% endhint %}

---

## ② 채널: 어디서 구매·운영하나

{% hint style="info" %}
"같은 모델인데 왜 채널에 따라 경험이 다른가?"를 이해하는 것이 이 섹션의 목적입니다. 모델 자체의 성능 비교는 [AI 플랫폼과 모델 비교](ai-ml.md)를 참고하세요.
{% endhint %}

### 채널 아키텍처 패턴

FM 제공사가 고객에게 모델을 전달하는 경로는 크게 **4가지 패턴**으로 나뉩니다. 이 구분을 먼저 이해하면 각 제공사의 복잡한 오퍼링이 정리됩니다.

| 패턴 | 비유 | 운영 주체 | 빌링 | 기능 범위 |
| --- | --- | --- | --- | --- |
| **A. 직접 이용** (1P) | 직영몰 | 모델사 | 모델사 직접 청구 | 풀 기능 (최신 우선) |
| **B. 모델사 서비스 + 클라우드 결제** | 백화점 입점 매장 | 모델사 | 클라우드 마켓플레이스 (커밋 소진 가능) | 풀 기능 (1P와 동일) |
| **C. 클라우드 제공** (3P Inference) | PB/편집숍 | 클라우드 벤더 | 클라우드 청구서 통합 | 클라우드 API 범위 (일부 기능 지연/미지원) |
| **D. 셀프호스팅** (오픈웨이트) | 직접 요리 | 고객 자체 | 인프라 비용 (GPU/서버) | 라이선스 조건 내 커스터마이징 자유 |

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                   FM 제공사 (OpenAI, Anthropic, Meta, etc.)                   │
├───────────┬───────────────────────────┬─────────────────────┬───────────────┤
│  A. 직접  │  B. 모델사 서비스 +        │  C. 클라우드 제공    │  D. 셀프      │
│  이용     │     클라우드 결제          │  (3P Inference)     │  호스팅       │
│ (직영몰)  │  (입점 매장)              │  (PB/편집숍)        │ (직접 요리)   │
│           │                           │                     │               │
│ • 풀 기능  │ • 풀 기능                  │ • 클라우드 API 범위  │ • 완전한 제어  │
│ • 직접 계약│ • 마켓플레이스/커밋 소진     │ • VPC/IAM 네이티브  │ • 인프라만 과금│
│ • 최신 우선│ • 모델사가 운영            │ • 클라우드가 운영    │ • 고객이 운영  │
└───────────┴───────────────────────────┴─────────────────────┴───────────────┘
```

### 제공사별 매핑

| 제공사 | A. 직접 이용 | B. 모델사 서비스 + 클라우드 결제 | C. 클라우드 제공 (3P Inference) | D. 셀프호스팅 |
| --- | --- | --- | --- | --- |
| **OpenAI** | api.openai.com (Enterprise) | — | Azure Foundry, Bedrock | ✗ (비공개 웨이트) |
| **Anthropic** | api.anthropic.com (Enterprise) | Claude Platform on AWS (CCU 빌링) | Bedrock Claude, Vertex AI Claude | ✗ (비공개 웨이트) |
| **Upstage** | console.upstage.ai | — | AWS/Azure Marketplace, SageMaker | ✅ Solar Open (오픈웨이트) |
| **LG EXAONE** | 직접 계약 | — | Marketplace | ✅ 오픈웨이트 (Hugging Face) |
| **Meta Llama** | — | — | Bedrock, Vertex, Azure (호스팅) | ✅ 오픈웨이트 (주 사용 경로) |
| **Mistral** | api.mistral.ai | — | Bedrock, Azure, Vertex | ✅ 오픈웨이트 일부 |

### 패턴별 특성 비교

| 비교 항목 | A. 직접 이용 | B. 모델사 서비스 + 클라우드 결제 | C. 클라우드 제공 | D. 셀프호스팅 |
| --- | --- | --- | --- | --- |
| 신규 모델 제공 | 최초 | 1P와 거의 동시 | 수일~수주 지연 | 오픈웨이트 공개 시점 |
| 플랫폼 기능 | 전체 | 전체 | 클라우드 API 범위 내 | 없음 (직접 구축) |
| Fine-tuning | 풀 옵션 | 풀 옵션 | 제한적이거나 지연 | 완전 자유 (자체 GPU) |
| 에이전트/도구 | 최신 (Claude Code, Codex 등) | 최신 | 자체 프레임워크 (AgentCore 등) | 직접 구축 (LangGraph 등) |
| VPC/네트워크 격리 | Enterprise 전용 | 마켓플레이스 내 격리 | 지원 (리전/서비스별 확인) | 완전 격리 (자체 인프라) |
| 컴플라이언스 | 제공사 인증 | 제공사 + 클라우드 인증 | 클라우드 인증 활용 가능 (구성 필요) | 자체 책임 |
| 커밋 소진 | 불가 | 가능 | 가능 | 불가 (인프라 비용만) |
| 운영 부담 | 없음 | 없음 | 낮음 | 높음 (GPU, 모델 서빙, 업데이트) |

### 오픈웨이트 모델이란 (패턴 D)

**오픈웨이트**(Open-weight)는 모델의 가중치(weight)를 공개하여 누구나 다운로드해서 자체 인프라에서 실행할 수 있는 모델입니다. "오픈소스"와 비슷하지만, 학습 데이터나 코드까지 공개하는 것은 아닌 경우가 많아 별도로 구분합니다.

**셀프호스팅을 선택하는 경우:**

- **데이터가 외부에 나갈 수 없음** — 망분리, 군사/정보 환경, 극도의 프라이버시 요건
- **완전한 커스터마이징** — 모델 파인튜닝, 양자화, 프루닝을 자유롭게 적용
- **비용 구조** — 대량 추론 시 토큰당 과금보다 GPU 임대/구매가 저렴해지는 규모
- **벤더 비종속** — 특정 API에 의존하지 않고, 모델을 직접 소유·교체

**셀프호스팅의 대가:**

- GPU 인프라 확보·관리 (클라우드 GPU 또는 온프레미스)
- 모델 서빙 프레임워크 운영 (vLLM, TGI, TensorRT-LLM 등)
- 보안, 업데이트, 스케일링을 모두 자체 책임
- 모델 제공사의 에이전트/도구 생태계를 직접 구축해야 함

{% hint style="info" %}
대표적 오픈웨이트 모델: **Meta Llama 4**, **Mistral** (일부 모델), **LG EXAONE**, **Upstage Solar Open**, **DeepSeek**, **Qwen**. 오픈웨이트라도 모델별로 라이선스 조건(상업적 사용 제한, 이용자 수 제한 등)이 다르므로 배포 전 확인이 필요합니다. 이들은 패턴 C(클라우드 제공)로도 사용 가능하므로, "셀프호스팅 vs 클라우드 호스팅" 선택이 됩니다.
{% endhint %}

### 실제 예시: "Claude Code를 쓰고 싶은데"

| 요구사항 | 적합한 패턴 |
| --- | --- |
| 최신 Claude Code + 빠른 업데이트 | **A. 직접 이용** |
| Claude Code + AWS EDP 소진 + AWS 청구서 | **B. 모델사 서비스 + 클라우드 결제** (Claude Platform on AWS) |
| Claude API만 필요 + VPC 격리 + 기존 AWS 거버넌스 | **C. 클라우드 제공** (Bedrock Claude) |

{% hint style="warning" %}
**패턴 B는 모든 제공사가 제공하는 것이 아닙니다.** Anthropic의 "Claude Platform on AWS"가 대표적이며, OpenAI는 현재 이에 해당하는 별도 오퍼링이 없습니다. 제공사별 가용한 패턴을 위 매핑 표에서 확인하세요.
{% endhint %}

---

## 주요 FM별 채널 현황

### OpenAI

| 채널 | 플랫폼 | 특징 |
| --- | --- | --- |
| 1P 직접 | api.openai.com | 최신 모델 최초 제공, 풀 기능(Assistants, Realtime, Batch), 사용량 기반 티어 자동 승급 |
| Azure Foundry | azure.microsoft.com | 엔터프라이즈 SLA(99.9%), PTU(예약 처리량), VNet 격리, EA/MACC 소진 가능 |
| Bedrock | aws.amazon.com | AWS IAM/VPC 통합, EDP 소진 가능, 독점 종료(2026.04) 이후 제공 시작 |
| OCI Marketplace | oracle.com/cloud | Universal Credits로 소비, Oracle DB 연동 |

### Anthropic (Claude)

| 채널 | 플랫폼 | 특징 |
| --- | --- | --- |
| 1P 직접 | api.anthropic.com | 최신 기능(Agent Skills, Claude Code, Computer Use) 최초 제공 |
| Claude Platform on AWS | AWS Marketplace | Anthropic 운영, AWS 빌링(Claude Consumption Units), 풀 Anthropic 기능 |
| Bedrock | aws.amazon.com | AWS 네이티브(CloudTrail, VPC, HIPAA BAA 상속), EDP 소진 |
| Vertex AI | cloud.google.com | GCP IAM/VPC 통합, GCP 커밋 소진 |

### 한국 FM

한국 FM 중 **1P와 3P 채널이 모두 존재**하여 채널 선택이 가능한 모델입니다.

| 제공사 | 모델 | 1P 채널 | 3P 채널 | 특징 |
| --- | --- | --- | --- | --- |
| **Upstage** | Solar Pro 3/2/Mini | Console API | AWS Marketplace, Azure Marketplace, SageMaker, 온프레미스 | 한국어+Document AI, MoE 효율 모델 |
| **LG AI Research** | EXAONE 4.x | LG 직접 계약 | Hugging Face, AWS/Azure Marketplace, 오픈웨이트 셀프호스팅 | 산업/B2B 특화, 오픈웨이트로 VPC/온프레미스 배포 용이 |

{% hint style="info" %}
이 외에도 Naver HyperCLOVA X, SKT, KT 등 다양한 한국 FM이 자사 플랫폼에서 제공되고 있습니다. 공공/금융 조달 시에는 과기정통부의 **독자파운데이션모델** 정책에 따라 특정 모델이 요구될 수 있으므로 정책 동향을 함께 확인하세요.
{% endhint %}

---

## 채널별 차이 비교

### 모델 가용성 (신규 모델 제공 시점)

| 채널 | 제공 시점 | 비고 |
| --- | --- | --- |
| **1P** | 출시 당일 | 항상 최초 |
| **Azure Foundry** | 수일~수주 후 | 프리뷰 기능(음성, 이미지)은 더 느림 |
| **Bedrock** | 수일~수주 후 | OpenAI는 독점 종료 후 제공 시작 (2026.04~) |
| **Vertex AI** | 수일~수주 후 | Anthropic 헤드라인 모델은 거의 동시 |

### 기능 패리티

| 기능 | 1P | 3P |
| --- | --- | --- |
| 채팅/완성 | ✅ | ✅ (거의 동일) |
| Fine-tuning | ✅ (풀 옵션) | △ (제한적이거나 지연) |
| 배치 추론 | ✅ | ✅ |
| 실시간/음성 | ✅ (최초) | △ (옵션/음성 제한) |
| 에이전트/어시스턴트 | ✅ (최신) | △ (수주~수개월 지연) |
| 베타 기능 (Computer Use 등) | ✅ | ✗ 또는 대폭 지연 |
| VPC 격리 / Private Link | ✗ 또는 Enterprise 전용 | ✅ (기본 제공) |
| HIPAA BAA / FedRAMP | 제공사별 별도 계약 | 클라우드 인증 상속 |

### 쿼터 (Rate Limit)

| 채널 | 구조 | 확장 방법 |
| --- | --- | --- |
| **OpenAI 1P** | 5개 사용 티어 (누적 지출 + 기간 기준 자동 승급). 티어별 TPM/RPM 상한 | Enterprise 계약으로 커스텀 한도 |
| **Azure Foundry** | 구독/리전/모델별 TPM 풀. 7개 티어 | PTU(예약 처리량) 구매, 포털에서 쿼터 증가 요청, EA로 초기 티어 상향 |
| **Anthropic 1P** | 4개 빌드 티어 | Enterprise 계약 |
| **Bedrock** | 계정/리전 서비스 쿼터 | Provisioned Throughput 구매, 쿼터 증가 티켓 |
| **Vertex AI** | 프로젝트별 쿼터 | Google 영업/지원을 통한 증가 |

{% hint style="info" %}
3P는 **보장된 용량**(PTU, Provisioned Throughput)에 강합니다. 1P는 글로벌 공유 용량에서 **유연한 버스트**에 강합니다. 안정적 대량 처리에는 3P 예약, 빠른 실험/최신 기능에는 1P가 유리합니다.
{% endhint %}

### 빌링과 비용

| 항목 | 1P | 3P |
| --- | --- | --- |
| **토큰 단가** | 기준가 | 공시 토큰가는 유사. 실효 비용은 커밋·예약·청구 단위(CCU 등)에 따라 상이 |
| **청구 방식** | 카드/인보이스, 별도 벤더 관계 | 기존 클라우드 청구서에 통합 |
| **커밋 소진** | 불가 | AWS EDP, Azure EA/MACC, GCP CUD로 소진 가능 |
| **할인 구조** | 제공사 Enterprise 계약 (볼륨 할인) | 클라우드 커밋 + 마켓플레이스 프라이빗 오퍼 |
| **TCO 고려** | 토큰 비용만 | 네트워킹, 지원 플랜, PTU 미활용 등 운영 오버헤드 가능 |

---

## 규모별 선택 가이드

| 규모 | 권장 | 이유 |
| --- | --- | --- |
| **월 $1K 미만** (실험/PoC) | 1P 직접 | 가장 빠른 시작, 최신 기능 즉시 접근, 복잡한 계약 불필요 |
| **월 $1K~$10K** (소규모 프로덕션) | 1P 또는 3P 단일 | 기존 클라우드 계약이 있으면 3P, 없으면 1P. 쿼터 이슈 적음 |
| **월 $10K~$100K** (중규모) | 3P 주력 + 1P 보조 | 클라우드 커밋 소진 효과 + VPC/컴플라이언스. 1P는 베타/최신 모델 접근용 |
| **월 $100K 이상** (대규모 엔터프라이즈) | 하이브리드 (3P 프로덕션 + 1P 혁신) | 프로덕션은 3P(커밋 소진, 예약 용량, 거버넌스). 혁신 팀은 1P(최신 기능, 빠른 실험). 양쪽 모두 협상 |

{% hint style="warning" %}
$100K+/월 규모에서는 **토큰 단가보다 조달 구조**(커밋 소진, 예약 용량, 프라이빗 오퍼)가 더 큰 비용 변수입니다. 클라우드 커밋이 큰 조직은 3P가 실질 비용에서 유리할 수 있습니다.
{% endhint %}

---

## 한국 엔터프라이즈 고려사항

| 요구사항 | 권장 채널 |
| --- | --- |
| 한국어 특화 + 멀티클라우드 | Upstage Solar, LG EXAONE (1P 또는 AWS/Azure Marketplace) |
| 데이터 주권 / 망분리 | 온프레미스(Upstage, EXAONE, Llama) 또는 국내 리전 3P |
| 기존 AWS/Azure 커밋 소진 | 3P (Bedrock / Azure Foundry / Marketplace) |
| 최신 글로벌 FM 즉시 접근 | 1P (OpenAI, Anthropic 직접) |
| 금융/공공 컴플라이언스 | 3P (클라우드 인증 상속) + 온프레미스 하이브리드 |
| 독자파운데이션모델 정책 대응 | 정책 참여 모델 확인 후 채널 선택 (공공/금융 조달 시) |

---

## 이용 형태별 요금제 (Seat 플랜 vs API 티어)

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

{% hint style="info" %}
모델별 정확한 RPM/TPM 한도는 [Organization Limits 페이지](https://platform.openai.com/settings/organization/limits)에서 확인하세요. 모델·티어에 따라 수백~수만 RPM, 수십만~수천만 TPM까지 다양합니다.
{% endhint %}

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

### 3P 채널 예약 용량

| 벤더 | 방식 | 적합 시점 |
| --- | --- | --- |
| **Azure PTU** (Provisioned Throughput Unit) | 고정 시간당 과금, 처리량 보장 | 월 1.5~2억+ 토큰 이상 안정 트래픽 |
| **Bedrock Provisioned Throughput** | 모델 유닛 예약 (1/6개월 커밋) | 대량 안정 워크로드 + 지연시간 보장 |
| **Bedrock On-demand** | 토큰당 과금, 예약 없음 | 버스트/실험/불규칙 워크로드 |

{% hint style="info" %}
예약 용량(PTU, Provisioned)은 사용하지 않아도 비용이 발생합니다. 정확한 가격과 손익분기점은 벤더 공식 페이지를 확인하세요.
{% endhint %}

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
| **모델 라우팅** | 단순 작업은 경량 모델, 복잡한 작업만 프론티어 모델로 분기하여 비용 절감 |
| **토큰 예산** | 프로젝트/팀/사용자별 일/월 토큰 상한 설정 |
| **AI 게이트웨이** | LiteLLM, Portkey 등으로 가상 키 발급, 하드 예산, 라우팅을 프로바이더 호출 전에 제어 |

### 공식 가격/기능 비교 페이지

| 제공사 | URL |
| --- | --- |
| OpenAI Business/Enterprise | [openai.com/business/pricing](https://openai.com/business/pricing/) |
| OpenAI API 가격 | [openai.com/api/pricing](https://openai.com/api/pricing/) |
| Anthropic 플랜 | [claude.com/pricing](https://claude.com/pricing) |
| Anthropic API 가격 | [platform.claude.com/docs/en/about-claude/pricing](https://platform.claude.com/docs/en/about-claude/pricing) |
| Azure OpenAI 가격 | [azure.microsoft.com/pricing/details/azure-openai](https://azure.microsoft.com/en-us/pricing/details/azure-openai/) |
| Bedrock 가격 | [aws.amazon.com/bedrock/pricing](https://aws.amazon.com/bedrock/pricing/) |
| Upstage 가격 | [console.upstage.ai](https://console.upstage.ai/) |

---

## 자주 하는 실수

- **"3P가 비싸다"는 가정** — 공시 토큰 단가는 대체로 유사합니다. 기존 클라우드 커밋이 있으면 3P가 실효 비용에서 유리할 수 있습니다. 다만 청구 단위(CCU 등)와 운영 비용은 별도 확인이 필요합니다.
- **단일 채널 올인** — 1P만 쓰면 클라우드 거버넌스 연동이 약할 수 있고, 3P만 쓰면 최신 기능에 지연이 있을 수 있습니다. 조직 상황에 맞게 병행을 검토하세요.
- **쿼터를 사후에 고려** — 프로덕션 트래픽을 예측하지 않고 시작하면, 쿼터 한도에 도달해 서비스 장애로 이어집니다. 규모가 크면 사전에 예약 용량을 확보하세요.

## 체크리스트

- [ ] 월간 예상 토큰 소비량을 추정했는가
- [ ] 기존 클라우드 커밋(EDP/EA/CUD)이 있는지 확인했는가
- [ ] 데이터 레지던시 요건(국내 리전, 망분리)을 정리했는가
- [ ] 필요한 기능(Fine-tuning, 에이전트, 실시간)이 어느 채널에서 제공되는지 확인했는가
- [ ] 쿼터/Rate Limit이 프로덕션 트래픽을 감당하는지 확인했는가
- [ ] 하이브리드(1P+3P) 운영 시 모델 버전 동기화 전략이 있는가

## 관련 문서

- [AI 플랫폼과 모델 비교](ai-ml.md) — 벤더별 FM 카탈로그, GPU/가속기
- [멀티클라우드 AI](multicloud-ai.md) — 벤더 조합 전략
- [LLMOps](llmops.md) — 비용 추적, 평가, 운영
- [FinOps](../governance/finops.md) — 클라우드 비용 거버넌스

## 참고하기

- [Azure OpenAI vs OpenAI: Enterprise Decision Guide](https://amitkoth.com/azure-openai-vs-openai/)
- [Anthropic API vs AWS Bedrock Claude](https://www.respan.ai/articles/claude-vs-bedrock-claude)
- [Claude Platform on AWS vs Bedrock](https://isimplifyme.com/blog/claude-platform-on-aws-vs-bedrock)
- [Azure Foundry Quotas and Limits](https://learn.microsoft.com/en-us/azure/foundry/openai/quotas-limits)
- [OpenAI API Rate Limits](https://platform.openai.com/docs/guides/rate-limits)
- [Upstage Console](https://console.upstage.ai/)
