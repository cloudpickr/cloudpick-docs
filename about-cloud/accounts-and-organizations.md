---
description: 클라우드 계정과 조직 구조, 멀티 계정 전략, 주요 벤더의 계층 구조를 비교합니다.
---

# 계정과 조직 구조

> 문서 기준: 2026년 5월

## 왜 계정 구조가 중요한가

온프레미스에서 부서별로 서버를 분리하는 이유를 생각해 보겠습니다. 같은 서버를 공유하면 한 팀의 실수가 다른 팀에 영향을 주고, 비용도 구분이 안 되고, 권한도 뒤섞입니다. 클라우드에서도 하나의 계정에 모든 리소스를 넣으면 동일한 문제가 발생합니다.

| 문제 | 멀티 계정으로 해결되는 이유 |
| --- | --- |
| **보안 경계 부재** | 계정이 격리 단위 — 한 계정의 사고가 다른 계정에 전파되지 않음 |
| **비용 추적 어려움** | 계정/프로젝트 단위로 비용이 자동 분리됨 |
| **권한 관리 복잡** | 계정별 독립 IAM + 조직 정책으로 최대 범위 제한 |
| **서비스 할당량 공유** | 계정별 쿼타가 독립 — 한 팀이 소진해도 다른 팀 무관 |

이 문제들을 해결하기 위해 각 벤더 모두 **멀티 계정 구조**를 권장합니다.

{% hint style="info" %}
멀티 계정 구조를 **실제로 구축하는 방법** — VPC 분리, 가드레일, 도입 순서, 체크리스트 — 은 [랜딩존](../governance/landing-zone.md)을 참고하세요. 이 문서는 "왜, 어떤 구조로" 나눠야 하는지 개념을 다룹니다.
{% endhint %}

## 벤더별 계층 구조

| 개념 | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- |
| **조직** | Organization | Tenant | Organization | Tenancy |
| **중간 그룹** | OU (Organizational Unit) | Management Group | Folder | Compartment (중첩) |
| **격리 단위** | Account | Subscription | Project | Compartment |
| **리소스 그룹** | — (태그로 대체) | Resource Group | — (라벨로 대체) | — |
| **조직 정책** | SCP | Azure Policy | Organization Policy | Compartment Policy |

{% tabs %}
{% tab title="AWS" %}
**Organization → OU → Account**

- Account = 권한 경계 = 비용 경계 (동일)
- SCP로 OU/Account의 최대 허용 범위 제한 (가드레일)
- Control Tower로 모범 사례 기반 자동 구성
{% endtab %}

{% tab title="Azure" %}
**Tenant → Management Group → Subscription → Resource Group**

- Subscription = 권한 경계, Billing Account = 비용 경계 (분리)
- Resource Group으로 Subscription 내 리소스를 추가 분류
- Azure Policy로 Management Group 수준에서 정책 상속
{% endtab %}

{% tab title="Google Cloud" %}
**Organization → Folder → Project**

- Project = 권한 경계, Billing Account = 비용 경계 (분리, 가장 유연)
- Project를 다른 Billing Account로 자유롭게 이동 가능
- Organization Policy로 Folder/Project 수준 제약
{% endtab %}

{% tab title="OCI" %}
**Tenancy → Compartment (중첩)**

- Compartment = 권한 경계, Tenancy = 비용 경계 (분리)
- Compartment가 OU + Account 역할을 동시에 수행
- IAM Policy가 Compartment 단위로 상속
{% endtab %}
{% endtabs %}

## 보안 경계와 IAM

계정 분리만으로는 부족합니다. 세 계층이 함께 동작해야 합니다.

| 계층 | 역할 | 예시 |
| --- | --- | --- |
| **계정 격리** | 장애/사고의 blast radius 제한 | Account, Subscription, Project, Compartment |
| **조직 정책 (가드레일)** | 계정이 할 수 있는 최대 범위 제한 | SCP, Azure Policy, Organization Policy |
| **IAM (권한 부여)** | 사용자/서비스에 실제 권한 부여 | IAM Policy, RBAC, IAM Binding |

예: SCP로 "서울 리전만 허용"을 설정하면, IAM에서 아무리 넓은 권한을 줘도 다른 리전에는 접근 불가합니다.

{% hint style="info" %}
IAM 설계 상세는 [IAM 개요](iam-overview.md) → [IAM 실무 설계](../security/iam.md)를 참고하세요.
{% endhint %}

## 비용 구조

### 권한 경계와 비용 경계

| 벤더 | 권한 경계 | 비용 경계 | 관계 |
| --- | --- | --- | --- |
| **AWS** | Account | Account | **동일** — 계정을 나누면 비용도 자동 분리 |
| **Azure** | Subscription | Billing Account / Profile | **분리** — 여러 Subscription을 하나의 청구로 묶을 수 있음 |
| **Google Cloud** | Project | Billing Account | **분리** — Project를 다른 Billing Account로 이동 가능 |
| **OCI** | Compartment | Tenancy | **분리** — Compartment로 격리, 비용은 Tenancy 통합 |

### 조직 규모별 설계 예시

| 규모 | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- |
| **스타트업** | 3 Account (dev/stg/prod) | 1 Subscription + 3 Resource Group | 3 Project + 1 Billing Account | 3 Compartment |
| **중견기업** | 팀별 Account + 공유서비스 Account | 팀별 Subscription + Management Group | 팀별 Folder + 서비스별 Project | 팀별 Compartment 중첩 |
| **대기업/공공** | 법인별 Org 또는 Billing Transfer | 법인별 Billing Profile + 중앙 MG | 법인별 Billing Account + 중앙 Org | 법인별 Tenancy |

| 항목 | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- |
| **비용 할당** | 태그 기반 | Resource Group + 태그 | 라벨 + Project | Compartment + 태그 |
| **예산 알림** | AWS Budgets | Azure Budgets | Budget Alerts | OCI Budgets |
| **빌링 이관** | Billing Transfer (2025) | Subscription Transfer | Billing Account 변경 | Cross-Tenancy |

{% hint style="info" %}
파트너(MSP/리셀러)를 통해 통합빌링을 사용하는 경우, 빌링 이관 시 파트너와 사전 협의가 필요합니다.
{% endhint %}

## 서비스 쿼타 (할당량)

계정당 리소스 상한이 있습니다 (리전당 VPC 수, 인스턴스 수, API 호출/초 등). 계정을 분리하면 쿼타도 독립됩니다.

| 벤더 | 쿼타 확인 | 증가 요청 |
| --- | --- | --- |
| AWS | [Service Quotas](https://docs.aws.amazon.com/servicequotas/) | 콘솔 또는 Support 티켓 |
| Azure | 구독 → 사용량 + 할당량 | Portal에서 요청 |
| Google Cloud | IAM → 할당량 | 콘솔에서 요청 |
| OCI | 거버넌스 → 서비스 한도 | Support 요청 |

{% hint style="warning" %}
프로덕션 전에 쿼타를 확인하세요. 개발 환경에서는 문제없다가 프로덕션 스케일에서 한도에 걸리는 경우가 흔합니다. GPU, 대형 인스턴스는 승인에 시간이 걸리므로 여유를 두고 요청하세요.
{% endhint %}

## 크로스 계정 리소스 공유

계정을 분리하면 격리는 되지만, 공유 서브넷·중앙 이미지·공통 DNS 등 계정 간 공유가 필요한 경우가 생깁니다.

| 벤더 | 서비스 | 공유 대상 예시 |
| --- | --- | --- |
| AWS | [RAM (Resource Access Manager)](https://docs.aws.amazon.com/ram/) | 서브넷, Transit Gateway, AMI |
| Azure | VNet Peering + RBAC | VNet, DNS Zone, Image Gallery |
| Google Cloud | [Shared VPC](https://cloud.google.com/vpc/docs/shared-vpc) | 호스트 프로젝트 서브넷 → 서비스 프로젝트 |
| OCI | Cross-Tenancy Policy + DRG | VCN, Object Storage 버킷 |

## 자주 하는 실수

- **"계정 하나로 충분하다"** — 소규모라도 dev/prod를 분리하지 않으면 개발 중 실수가 프로덕션에 영향을 줍니다. 계정 분리는 규모와 무관하게 기본입니다.
- **"태그만 달면 비용 추적이 된다"** — 태그는 누락되기 쉽고 강제가 어렵습니다. 계정/프로젝트 단위 분리가 가장 확실한 비용 경계입니다.
- **"나중에 구조를 바꾸면 된다"** — 리소스가 쌓인 뒤 계정 구조를 변경하는 것은 마이그레이션 수준의 작업입니다. 초기에 설계하는 것이 훨씬 쉽습니다.

## 체크리스트

- [ ] 최소 dev/staging/prod 환경을 별도 계정(또는 프로젝트/구독)으로 분리했는가?
- [ ] 조직 정책(SCP, Azure Policy 등)으로 허용 리전과 서비스 범위를 제한했는가?
- [ ] 프로덕션 쿼타(서비스 할당량)를 사전에 확인하고 증가 요청을 완료했는가?

## 참고하기

### AWS

- [AWS Organizations](https://aws.amazon.com/ko/organizations/)
- [AWS Control Tower](https://aws.amazon.com/ko/controltower/)
- [AWS Organizations와 통합 결제](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/consolidated-billing.html)

### Azure

- [Azure 관리 그룹](https://learn.microsoft.com/ko-kr/azure/governance/management-groups/overview)
- [Azure Policy](https://learn.microsoft.com/ko-kr/azure/governance/policy/overview)
- [빌링 계정 이해하기](https://learn.microsoft.com/azure/cost-management-billing/manage/view-all-accounts)

### Google Cloud

- [Resource Manager](https://cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy)
- [Organization Policy](https://cloud.google.com/resource-manager/docs/organization-policy/overview)
- [Cloud Billing 계정 개요](https://cloud.google.com/billing/docs/concepts)

### OCI

- [OCI Compartments](https://docs.oracle.com/en-us/iaas/Content/Identity/Tasks/managingcompartments.htm)
- [OCI IAM](https://docs.oracle.com/en-us/iaas/Content/Identity/home.htm)
- [조직 관리와 빌링](https://docs.oracle.com/en-us/iaas/Content/GSG/Concepts/settinguptenancy.htm)
