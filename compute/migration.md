---
description: 워크로드 마이그레이션 전략(7R), 평가/실행 단계, 리프트앤시프트 vs 리팩터링 트레이드오프를 벤더별로 비교합니다.
---

# 애플리케이션 마이그레이션

> 문서 기준: 2026년 5월

## 개요

온프레미스 또는 다른 클라우드에 있는 애플리케이션과 인프라를 클라우드로 이전하는 작업입니다. 단순히 VM을 복사하는 것이 아니라, 애플리케이션의 아키텍처, 의존성, 운영 방식 전체를 재평가하는 과정입니다.

{% hint style="info" %}
데이터베이스 마이그레이션은 [데이터베이스 마이그레이션](../database/migration.md), 대용량 파일 이전은 [스토리지 마이그레이션](../storage/migration.md)을 참고하세요.
{% endhint %}

{% hint style="warning" %}
마이그레이션 전에 **거버넌스 기반을 먼저 준비하세요.** 계정/조직 구조, 네트워크(VPC/서브넷), IAM 정책, 태그 체계, 로깅이 없는 상태에서 워크로드를 옮기면 나중에 전부 재구성해야 합니다. [클라우드 거버넌스 시작하기](../governance/getting-started.md) → [랜딩존](../governance/landing-zone.md)을 먼저 확인하세요.
{% endhint %}

## 7R 마이그레이션 전략

Gartner가 제시하고 AWS가 확장한 **7R 프레임워크** 는 워크로드별 마이그레이션 전략을 분류하는 표준입니다.

| 전략 | 설명 | 난이도 | 효과 |
| --- | --- | --- | --- |
| **Retire** (폐기) | 더 이상 필요 없는 워크로드를 중단 | 낮음 | 즉시 비용 절감 |
| **Retain** (유지) | 온프레미스 유지 (하이브리드) | 낮음 | 마이그레이션 비용 없음 |
| **Relocate** (재배치) | 하이퍼바이저 수준에서 그대로 이동 (예: VMware Cloud on AWS) | 낮음 | 최소 변경으로 빠른 이전 |
| **Rehost** (리호스트) | VM 단위 Lift & Shift | 낮음 | 빠른 이전, 클라우드 이점 제한적 |
| **Replatform** (리플랫폼) | 관리형 서비스로 일부 전환 (예: DB를 RDS로) | 중간 | 운영 부담 감소 |
| **Repurchase** (재구매) | SaaS로 전환 (예: 자체 CRM → Salesforce) | 중간 | 운영 책임 위임 |
| **Refactor** (리팩터) | 클라우드 네이티브로 재설계 (서버리스, 마이크로서비스) | 높음 | 확장성/효율성 최대화 |

### 전략 선택 기준

| 상황 | 권장 전략 |
| --- | --- |
| 데이터센터 철수 기한이 촉박 | Relocate 또는 Rehost |
| 비즈니스 가치가 낮고 수명이 짧은 워크로드 | Retire |
| 상용 솔루션이 이미 있는 기능 | Repurchase (SaaS) |
| 클라우드 이점(확장성, 비용)을 최대화하고 싶은 핵심 워크로드 | Refactor |
| 변경 없이 안정적 운영을 원하는 레거시 | Retain |
| 운영 부담을 줄이고 싶지만 코드는 유지 | Replatform |

{% hint style="warning" %}
**주의:** 모든 워크로드를 Refactor하려 하면 시간과 비용이 급증합니다. 대부분의 기업은 **Rehost/Replatform을 기본으로 하고, 핵심 워크로드만 Refactor** 하는 하이브리드 접근을 사용합니다.
{% endhint %}

## 리프트앤시프트 vs 리팩터링 트레이드오프

가장 흔한 선택지인 Rehost(Lift & Shift)와 Refactor의 비교입니다.

| 항목 | Rehost (Lift & Shift) | Refactor (클라우드 네이티브) |
| --- | --- | --- |
| **이전 기간** | 수 주\~수 개월 | 수 개월\~수 년 |
| **개발 비용** | 낮음 (변경 최소) | 높음 (재설계/재구현) |
| **운영 비용** | 온프레미스와 유사 | 클라우드 최적화로 절감 가능 |
| **확장성** | 제한적 (VM 단위) | 높음 (서버리스, 수평 확장) |
| **장애 복구** | 기존 방식 유지 | 클라우드 네이티브 HA/DR |
| **위험도** | 낮음 | 높음 (재설계 실패 가능) |
| **클라우드 이점 활용** | 제한적 | 최대 |
| **데이터센터 철수 기한** | 짧아도 대응 가능 | 긴 기간 필요 |

{% hint style="info" %}
**일반적 패턴:** 데이터센터 철수 기한이 있다면 **먼저 Rehost로 이전한 후, 안정화 후 점진적으로 Replatform/Refactor** 하는 전략이 현실적입니다. 처음부터 모든 워크로드를 Refactor하면 일정 지연과 품질 문제가 발생하기 쉽습니다.
{% endhint %}

## 마이그레이션 프로세스

대규모 마이그레이션은 여러 단계를 거치는 프로젝트입니다.

| 단계 | 주요 활동 |
| --- | --- |
| **1. Discovery** | 인벤토리 수집 — 서버, 애플리케이션, 의존성, 사용량 파악 |
| **2. Assessment** | 워크로드별 7R 전략 결정, 비용 추정, 위험 분석 |
| **3. Planning** | 마이그레이션 순서(Wave) 결정, 롤백 계획, 다운타임 예산 |
| **4. Landing Zone** | 클라우드 계정/네트워크/보안 기반 구성 ([랜딩존](../governance/landing-zone.md) 참고) |
| **5. Migration** | 실제 데이터/애플리케이션 이전 |
| **6. Validation** | 성능/기능 테스트, 사용자 수용 테스트 |
| **7. Cutover** | 트래픽 전환, 모니터링 강화 |
| **8. Optimize** | 클라우드 환경 최적화 (비용, 성능, 보안) |

### 마이그레이션 웨이브 (Wave)

수백\~수천 개의 워크로드를 한 번에 이전하는 것은 위험합니다. 보통 **웨이브(Wave)** 단위로 나눠 진행합니다.

- **Pilot Wave** — 간단하고 위험이 낮은 워크로드로 경험 축적 (예: 내부 도구, 개발 환경)
- **Core Waves** — 애플리케이션 그룹 단위로 묶어 순차적으로 이전
- **Critical Wave** — 비즈니스 크리티컬 워크로드는 마지막에 이전 (충분한 검증 후)

## 다운타임 최소화

프로덕션 워크로드는 다운타임을 최소화해야 합니다.

| 기법 | 설명 | 사용 시점 |
| --- | --- | --- |
| **블록 수준 연속 복제** | 소스 VM의 변경 블록을 지속적으로 대상으로 복제 | 대부분의 VM 마이그레이션 도구 기본 방식 |
| **Blue/Green 전환** | 이전 인프라와 신규 인프라를 병행 운영 후 DNS/LB로 전환 | 웹 서비스, API |
| **데이터베이스 CDC** | DB 변경을 지속 복제하여 Cutover 시 몇 분 내 전환 | DB 마이그레이션 |
| **단계적 Cutover** | 사용자/지역/기능별로 점진적 전환 | 대규모 사용자 대상 서비스 |

## Cutover 체크리스트

실제 전환 시점에 확인해야 할 항목들입니다.

- [ ] 데이터 무결성 검증 완료 (체크섬, 레코드 수)
- [ ] 애플리케이션 기능 테스트 완료
- [ ] 성능 벤치마크가 기존 환경 이상
- [ ] 보안 설정(IAM, 방화벽, 암호화) 검증
- [ ] 백업/DR 구성 완료
- [ ] 모니터링 및 알림 동작 확인
- [ ] 롤백 계획 및 롤백 시점 결정
- [ ] 이해관계자 통보 및 Go/No-Go 승인
- [ ] Cutover 시간대(주말/야간) 확정
- [ ] 장애 발생 시 대응 인력 대기

## 마이그레이션 도구

{% hint style="info" %}
**AI 지원 마이그레이션:** 각 CSP는 AI를 활용하여 마이그레이션 평가·코드 변환·테스트를 자동화하는 서비스를 제공하고 있습니다. [AWS Transform](https://aws.amazon.com/transform/)(Q Developer 기반 코드 변환), [Azure Migrate with Copilot](https://learn.microsoft.com/azure/migrate/)(평가 자동화), [Google Cloud Dual Run](https://cloud.google.com/blog/products/databases/dual-run-for-mainframe-modernization)(메인프레임 병렬 검증) 등이 대표적입니다. 대규모 레거시 전환 시 수작업 분석 시간을 크게 줄일 수 있으나, AI 결과물에 대한 검증은 여전히 필요합니다.
{% endhint %}

### 평가 및 발견

| 벤더 | 제품 | 기능 |
| --- | --- | --- |
| AWS | [Application Discovery Service](https://aws.amazon.com/application-discovery/) | 에이전트/에이전트리스 방식으로 온프레미스 인벤토리 수집 |
| AWS | [Migration Hub](https://aws.amazon.com/migration-hub/) | 마이그레이션 중앙 대시보드 |
| Azure | [Azure Migrate](https://azure.microsoft.com/products/azure-migrate/) | 평가, 서버/DB 마이그레이션 통합 |
| Google Cloud | [Migration Center](https://cloud.google.com/migration-center/docs) | 포트폴리오 평가, 의존성 매핑 |
| OCI | [Cloud Migrations](https://docs.oracle.com/en-us/iaas/Content/cloud-migration/home.htm) | 평가 및 실행 통합 |

### VM/서버 마이그레이션

| 벤더 | 제품 | 기능 |
| --- | --- | --- |
| AWS | [Application Migration Service (MGN)](https://aws.amazon.com/application-migration-service/) | 블록 수준 복제. 최소 다운타임 Rehost |
| Azure | [Azure Migrate: Server Migration](https://learn.microsoft.com/azure/migrate/migrate-services-overview) | VMware/Hyper-V/물리 서버 → Azure VM |
| Google Cloud | [Migrate to Virtual Machines](https://cloud.google.com/migrate/virtual-machines/docs) | VMware/AWS/Azure → Compute Engine |
| OCI | [OCI Cloud Migrations](https://docs.oracle.com/en-us/iaas/Content/cloud-migration/home.htm) | VMware/AWS → OCI |

### 컨테이너화

| 벤더 | 제품 | 기능 |
| --- | --- | --- |
| AWS | [App2Container](https://aws.amazon.com/app2container/) | Java/.NET 앱을 컨테이너화 |
| Azure | [Migrate to containers](https://learn.microsoft.com/azure/migrate/tutorial-app-containerization-aspnet-kubernetes) | ASP.NET/Java → AKS |
| Google Cloud | [Migrate to Containers](https://cloud.google.com/migrate/containers/docs) | VM → GKE 컨테이너 |

## 참고하기

### AWS

- [AWS Cloud Migration](https://aws.amazon.com/cloud-migration/)
- [AWS Migration Hub](https://aws.amazon.com/migration-hub/)
- [AWS Application Migration Service](https://aws.amazon.com/application-migration-service/)
- [AWS Prescriptive Guidance: Migration Strategies (7R)](https://docs.aws.amazon.com/prescriptive-guidance/latest/large-migration-guide/migration-strategies.html)

### Azure

- [Azure Migrate](https://azure.microsoft.com/products/azure-migrate/)
- [Cloud Adoption Framework — Migrate](https://learn.microsoft.com/azure/cloud-adoption-framework/migrate/)
- [Azure Migrate 문서](https://learn.microsoft.com/azure/migrate/)

### Google Cloud

- [Migration Center](https://cloud.google.com/migration-center/docs)
- [Migrate to Virtual Machines](https://cloud.google.com/migrate/virtual-machines/docs)
- [Migrate to Containers](https://cloud.google.com/migrate/containers/docs)

### OCI

- [OCI Cloud Migrations](https://docs.oracle.com/en-us/iaas/Content/cloud-migration/home.htm)
- [OCI Migration Solutions](https://www.oracle.com/cloud/migration/)
