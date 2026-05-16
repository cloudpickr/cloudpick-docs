---
description: 클라우드 계정과 조직 구조, 멀티 계정 전략, 주요 벤더의 계층 구조를 비교합니다.
---

# 계정과 조직 구조

> 문서 기준: 2026년 5월

## 왜 계정 구조가 중요한가

온프레미스 환경에서 부서별로 서버를 분리하는 이유를 생각해 보겠습니다. 개발팀과 운영팀이 같은 서버를 공유하면, 개발팀의 실수로 운영 서비스가 중단될 수 있습니다. 비용도 어느 부서가 얼마나 사용했는지 구분하기 어렵습니다. 그래서 부서별로 서버를 분리하고, 네트워크를 격리하고, 접근 권한을 나누는 것입니다.

클라우드에서도 동일한 문제가 발생합니다. 하나의 계정에 모든 리소스를 넣으면 다음과 같은 문제가 생깁니다.

- **보안 경계 부재** — 개발 환경의 보안 사고가 프로덕션 환경에 영향을 줄 수 있습니다.
- **비용 추적 어려움** — 어떤 팀이, 어떤 프로젝트가 비용을 발생시키는지 파악하기 어렵습니다.
- **권한 관리 복잡** — 세밀한 접근 제어가 어려워지고, 과다 권한이 부여되기 쉽습니다.
- **서비스 할당량 공유** — 한 팀이 API 호출 한도를 소진하면 다른 팀도 영향을 받습니다.

이러한 문제를 해결하기 위해 각 벤더 모두 **멀티 계정** (Multi-Account) 구조를 권장하며, 여러 계정을 체계적으로 관리할 수 있는 조직(Organization) 기능을 제공합니다.

## 핵심 개념

### 계정 (Account / Subscription / Project)

클라우드에서 "계정"은 리소스의 격리 단위이자 빌링 단위입니다. 각 벤더 모두 비슷한 개념을 가지고 있지만, 용어와 세부 동작이 다릅니다.

### 조직 (Organization)

여러 계정을 하나의 조직으로 묶어 중앙에서 관리하는 기능입니다. 조직 수준에서 보안 정책을 적용하고, 빌링을 통합하고, 계정 간 리소스 공유를 제어할 수 있습니다.

### 정책 상속

상위 조직에서 설정한 정책이 하위 계정에 자동으로 적용되는 구조입니다. 예를 들어, "모든 계정에서 특정 리전만 사용 가능"이라는 정책을 조직 수준에서 설정하면, 모든 하위 계정에 적용됩니다.

## 벤더별 비교

| 개념 | AWS | Azure | GCP | OCI |
| --- | --- | --- | --- | --- |
| **리소스 격리 단위** | Account | Subscription | Project | Compartment |
| **조직** | Organization | Management Group (최상위) | Organization | Tenancy |
| **중간 그룹** | Organizational Unit (OU) | Management Group (중첩 가능) | Folder | Compartment (중첩 가능) |
| **리소스 그룹** | — (태그로 대체) | Resource Group | — (라벨로 대체) | Compartment |
| **정책 제어** | SCP (Service Control Policy) | Azure Policy | Organization Policy | IAM Policy (Compartment 상속) |
| **빌링 단위** | Account (통합 빌링 가능) | Subscription | Billing Account → Project | Tenancy |
| **계정 생성** | Organizations API로 자동 생성 | 수동 또는 자동화 | Projects API로 자동 생성 | Compartment API |

{% tabs %}
{% tab title="AWS" %}
```mermaid
graph TD
    A1[Organization] --> A2[OU]
    A2 --> A3[Account]
```

AWS의 계층 구조는 **Organization → OU → Account** 입니다.

- **Organization** — 최상위 관리 단위입니다. 하나의 관리 계정(Management Account)이 조직을 소유합니다.
- **OU (Organizational Unit)** — 계정을 논리적으로 그룹화하는 단위입니다. OU는 중첩할 수 있습니다.
- **Account** — 리소스 격리와 빌링의 기본 단위입니다. 각 Account는 독립된 IAM, VPC, 서비스 할당량을 가집니다.
- **SCP (Service Control Policy)** — OU 또는 Account에 적용하여, 사용 가능한 서비스와 작업을 제한합니다. SCP는 권한을 부여하는 것이 아니라, 최대 권한 범위를 제한하는 가드레일 역할을 합니다.

AWS는 **AWS Control Tower**를 통해 모범 사례 기반의 멀티 계정 환경을 자동으로 구성할 수 있습니다.
{% endtab %}

{% tab title="Azure" %}
```mermaid
graph TD
    B1[Tenant] --> B2[Management Group]
    B2 --> B3[Subscription]
    B3 --> B4[Resource Group]
```

Azure의 계층 구조는 **Tenant → Management Group → Subscription → Resource Group** 입니다.

- **Tenant** — Azure AD(현 Microsoft Entra ID)의 인스턴스로, 조직의 ID 경계입니다.
- **Management Group** — Subscription을 그룹화하는 단위입니다. 최대 6단계까지 중첩할 수 있습니다.
- **Subscription** — 빌링과 리소스 격리의 기본 단위입니다. AWS의 Account에 해당합니다.
- **Resource Group** — Subscription 내에서 리소스를 논리적으로 그룹화하는 단위입니다. AWS/GCP에는 없는 Azure만의 개념입니다.
- **Azure Policy** — Management Group, Subscription, Resource Group 수준에서 정책을 적용할 수 있습니다.

Azure의 특징은 **Resource Group** 입니다. 하나의 Subscription 안에서도 리소스를 논리적으로 분리할 수 있어, 소규모 조직에서는 Subscription을 많이 만들지 않아도 됩니다.
{% endtab %}

{% tab title="GCP" %}
```mermaid
graph TD
    C1[Organization] --> C2[Folder]
    C2 --> C3[Project]
```

GCP의 계층 구조는 **Organization → Folder → Project** 입니다.

- **Organization** — Google Workspace 또는 Cloud Identity 도메인에 연결된 최상위 노드입니다.
- **Folder** — Project를 그룹화하는 단위입니다. 최대 10단계까지 중첩할 수 있습니다.
- **Project** — 리소스 격리의 기본 단위입니다. AWS의 Account, Azure의 Subscription에 해당합니다.
- **Organization Policy** — Organization, Folder, Project 수준에서 제약 조건을 적용합니다.

GCP의 특징은 **빌링이 Project와 분리** 되어 있다는 점입니다. 하나의 Billing Account에 여러 Project를 연결할 수 있어, 빌링 구조를 유연하게 설계할 수 있습니다.
{% endtab %}

{% tab title="OCI" %}
```mermaid
graph TD
    D1[Tenancy] --> D2[Compartment]
    D2 --> D3[Sub-Compartment]
```

OCI의 계층 구조는 **Tenancy → Compartment** 입니다.

- **Tenancy** — 최상위 관리 단위이자 루트 Compartment입니다. OCI 계약 시 하나의 Tenancy가 생성됩니다.
- **Compartment** — 리소스 격리와 정책 적용의 기본 단위입니다. 최대 6단계까지 중첩할 수 있습니다. AWS의 Account + OU 역할을 하나의 개념으로 통합한 것입니다.
- **IAM Policy** — Compartment 단위로 적용되며, 상위 Compartment의 정책이 하위에 상속됩니다.

OCI의 특징은 **Compartment가 리소스 격리와 조직 구조를 동시에 담당** 한다는 점입니다. AWS처럼 별도의 Account를 만들 필요 없이, Compartment 중첩으로 환경을 분리합니다.
{% endtab %}
{% endtabs %}

## 빌링 구조

### 권한 경계와 비용 경계 — 같은가, 다른가?

AWS는 Account 하나가 권한 경계이자 비용 경계입니다. 다른 벤더는 이 둘이 분리되어 있어 더 유연하지만, 이해하기 복잡합니다.

| 벤더 | 권한 경계 (리소스 격리) | 비용 경계 (청구 단위) | 관계 |
| --- | --- | --- | --- |
| **AWS** | Account | Account | **동일** — 계정을 나누면 비용도 자동 분리 |
| **Azure** | Subscription | Billing Account / Billing Profile | **분리** — 여러 Subscription을 하나의 청구로 묶거나, 하나의 Subscription 비용을 부서별로 나눌 수 있음 |
| **GCP** | Project | Billing Account | **분리** — Project를 다른 Billing Account로 자유롭게 이동 가능. 가장 유연 |
| **OCI** | Compartment | Tenancy | **분리** — Compartment로 권한을 나누되, 비용은 Tenancy 단위로 통합 청구 |

**실무적 의미:**

- **AWS** — 비용을 분리하려면 계정을 나눠야 합니다. 계정이 많아지면 Organizations 통합 결제로 묶습니다.
- **Azure/GCP** — 권한 분리와 비용 분리를 독립적으로 설계할 수 있습니다. 조직 개편 시 비용 구조만 바꾸고 리소스는 그대로 둘 수 있습니다.
- **OCI** — Compartment로 세밀하게 격리하되, 비용은 Tenancy 단위로 관리합니다.

### 비용 할당과 예산 관리

| 항목 | AWS | Azure | GCP | OCI |
| --- | --- | --- | --- | --- |
| **비용 할당** | 태그 기반 Cost Allocation | Resource Group + 태그 | 라벨 + Project 단위 | Compartment + 태그 |
| **예산 알림** | AWS Budgets | Azure Budgets | GCP Budget Alerts | OCI Budgets |
| **빌링 이관** | Billing Transfer (2025) | Subscription Transfer | Project의 Billing Account 변경 | Cross-Tenancy 전환 |

{% hint style="info" %}
파트너를 통해 통합빌링을 사용하는 경우, 빌링 이관 시 파트너와 사전 협의가 필요합니다.
{% endhint %}

### 실무 팁

- **부서별로 법적/세무적 분리가 필요** → 별도 Billing Account/Organization/Tenancy
- **그룹 단위로 통합 결제 + 부서별 비용 가시성** → 단일 Billing Account + 태그 기반 비용 할당
- **자주 변경되는 조직 구조** → Project↔Billing Account 분리 가능한 GCP가 유리
- **대량 약정 할인 극대화** → 하나의 Billing Account로 묶어 약정 단가 협상

공식 문서:

- [AWS — AWS Organizations와 통합 결제](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/consolidated-billing.html)
- [Azure — 빌링 계정 이해하기](https://learn.microsoft.com/azure/cost-management-billing/manage/view-all-accounts)
- [GCP — Cloud Billing 계정 개요](https://cloud.google.com/billing/docs/concepts)
- [OCI — 조직 관리와 빌링](https://docs.oracle.com/en-us/iaas/Content/GSG/Concepts/settinguptenancy.htm)

## 멀티 계정 전략

각 벤더 모두 다음과 같은 멀티 계정 전략을 권장합니다.

{% hint style="info" %}
멀티 계정 구조의 실제 구현 — VPC 분리 패턴, 가드레일 설정, 도입 순서 — 은 [랜딩존](../governance/landing-zone.md)을 참고하세요.
{% endhint %}

### 보안 경계와 IAM의 관계

계정 분리는 **격리**(blast radius 제한)를 제공하고, 조직 정책(SCP/Azure Policy/Organization Policy)은 **최대 허용 범위**를 제한합니다. IAM은 그 범위 안에서 **실제 권한을 부여**합니다. 세 계층이 함께 동작합니다.

| 계층 | 역할 | 벤더 예시 |
| --- | --- | --- |
| **계정 격리** | 장애/보안 사고의 영향 범위 제한 | Account, Subscription, Project, Compartment |
| **조직 정책 (가드레일)** | 계정이 할 수 있는 최대 범위 제한 | SCP, Azure Policy, Organization Policy, Compartment Policy |
| **IAM (권한 부여)** | 사용자/서비스에 실제 권한 부여 | IAM Policy, RBAC, IAM Binding, IAM Policy |

예: SCP로 "서울 리전만 허용"을 설정하면, IAM에서 아무리 넓은 권한을 줘도 다른 리전에는 접근 불가합니다.

IAM 설계 상세는 [IAM 개요](iam-overview.md) → [IAM 실무 설계](../security/iam.md)를 참고하세요.

### 환경별 분리

가장 기본적인 전략으로, 개발(dev), 스테이징(staging), 프로덕션(prod) 환경을 별도의 계정으로 분리합니다. 개발 환경에서의 실수가 프로덕션에 영향을 주지 않도록 격리합니다.

```mermaid
flowchart TD
    subgraph org["Organization"]
        subgraph dev["Dev OU"]
            DA[dev-account-a]
            DB[dev-account-b]
        end
        subgraph stg["Staging OU"]
            SA[staging-account]
        end
        subgraph prd["Prod OU"]
            PA[prod-account]
        end
    end
```

### 워크로드별 분리

서로 다른 워크로드(웹 서비스, 데이터 파이프라인, ML 플랫폼 등)를 별도의 계정으로 분리합니다. 각 워크로드의 보안 요건과 비용을 독립적으로 관리할 수 있습니다.

### 보안/로깅 전용 계정

보안 로그, 감사 로그, CloudTrail/Activity Log 등을 중앙 집중식으로 수집하는 전용 계정을 두는 것이 모범 사례입니다. 이 계정은 읽기 전용으로 운영하여, 로그의 무결성을 보장합니다.

### 크로스 계정 리소스 공유

계정을 분리하면 격리는 되지만, 공유 서브넷, 중앙 이미지, 공통 DNS 등 계정 간 리소스 공유가 필요한 경우가 생깁니다.

| 벤더 | 서비스 | 공유 대상 예시 |
| --- | --- | --- |
| AWS | [Resource Access Manager (RAM)](https://docs.aws.amazon.com/ram/) | 서브넷, Transit Gateway, Route 53 Resolver, AMI |
| Azure | 구독 간 VNet Peering + RBAC | VNet, DNS Zone, Image Gallery |
| GCP | [Shared VPC](https://cloud.google.com/vpc/docs/shared-vpc) | 호스트 프로젝트의 서브넷을 서비스 프로젝트에 공유 |
| OCI | Cross-Tenancy Policy + DRG | VCN, Object Storage 버킷 |

{% hint style="info" %}
네트워크 공유가 가장 흔한 사용 사례입니다. 중앙 네트워크 계정에서 서브넷을 만들고 워크로드 계정에 공유하면, IP 관리를 중앙화하면서 워크로드는 독립적으로 운영할 수 있습니다.
{% endhint %}

## 서비스 쿼타 (할당량) 관리

클라우드 서비스에는 계정당 사용할 수 있는 리소스 상한(**쿼타** 또는 **서비스 한도**)이 있습니다. 예: 리전당 VPC 수, EC2 인스턴스 수, API 호출 횟수/초 등.

### 쿼타가 존재하는 이유

- **인프라 보호** — 한 고객의 과도한 사용이 다른 고객에게 영향을 주지 않도록 격리
- **실수 방지** — 자동화 오류로 수천 개 리소스가 생성되는 사고 방지
- **용량 계획** — 벤더가 리전별 물리 용량을 계획하기 위한 기준

### 쿼타 관리 방법

| 벤더 | 쿼타 확인 | 증가 요청 | 비고 |
| --- | --- | --- | --- |
| AWS | [Service Quotas 콘솔](https://docs.aws.amazon.com/servicequotas/) | 콘솔에서 직접 요청 또는 Support 티켓 | Trusted Advisor에서 한도 근접 알림 |
| Azure | 구독 → 사용량 + 할당량 | Azure Portal에서 요청 | 일부 쿼타는 자동 승인 |
| GCP | IAM → 할당량 | 콘솔에서 요청 | 프로젝트 단위 적용 |
| OCI | 거버넌스 → 서비스 한도 | Support 요청 | Compartment 단위 제한 가능 |

### 실무 주의사항

- **프로덕션 전에 쿼타를 확인하세요.** 개발 환경에서는 문제없다가 프로덕션 스케일에서 한도에 걸리는 경우가 흔합니다.
- **멀티 계정 분리 시 각 계정의 쿼타는 독립입니다.** 한 계정의 쿼타 증가가 다른 계정에 적용되지 않습니다.
- **쿼타 증가 요청은 시간이 걸릴 수 있습니다.** 특히 GPU, 대형 인스턴스는 리전별 물리 용량에 따라 승인이 지연될 수 있으므로 여유를 두고 요청하세요.
- **비용 관리와 연계하세요.** 쿼타를 무한정 올리면 실수로 인한 비용 폭증을 막을 수 없습니다. [FinOps](../governance/finops.md)의 예산 알림과 함께 운영하세요.

## 관련 문서

{% content-ref url="iam-overview.md" %}
[iam-overview.md](iam-overview.md)
{% endcontent-ref %}

{% content-ref url="../governance/landing-zone.md" %}
[landing-zone.md](../governance/landing-zone.md)
{% endcontent-ref %}

{% content-ref url="../governance/finops.md" %}
[finops.md](../governance/finops.md)
{% endcontent-ref %}

## 참고하기

### AWS

- [AWS Organizations](https://aws.amazon.com/ko/organizations/)
- [AWS Control Tower](https://aws.amazon.com/ko/controltower/)
- [멀티 계정 전략 모범 사례](https://docs.aws.amazon.com/ko_kr/organizations/latest/userguide/orgs_best-practices.html)

### Azure

- [Azure 관리 그룹](https://learn.microsoft.com/ko-kr/azure/governance/management-groups/overview)
- [Azure 구독 관리](https://learn.microsoft.com/ko-kr/azure/cloud-adoption-framework/ready/azure-best-practices/organize-subscriptions)
- [Azure Policy](https://learn.microsoft.com/ko-kr/azure/governance/policy/overview)

### GCP

- [Resource Manager](https://cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy)
- [Organization Policy](https://cloud.google.com/resource-manager/docs/organization-policy/overview)
- [Google Cloud 설정 체크리스트](https://cloud.google.com/docs/enterprise/setup-checklist)

### OCI

- [OCI IAM with Identity Domains](https://docs.oracle.com/en-us/iaas/Content/Identity/home.htm)
- [OCI Compartments](https://docs.oracle.com/en-us/iaas/Content/Identity/Tasks/managingcompartments.htm)
- [OCI Tenancy Setup](https://docs.oracle.com/en-us/iaas/Content/GSG/Concepts/settinguptenancy.htm)
