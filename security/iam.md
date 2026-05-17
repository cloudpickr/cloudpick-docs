---
description: IAM 실무 설계, 인증 방식, 권한 모델, 최소 권한 도구, 장기 자격 증명 위험을 벤더별로 비교합니다.
---

# IAM 실무 설계와 보안 운영

> 문서 기준: 2026년 5월

## 개요

이 문서는 IAM의 **실무 운영**에 집중합니다 — 자격 증명 선택, ID 유형별 적용, 최소 권한 실천, 보안 점검.

{% hint style="info" %}
벤더별 제품 비교, 인증 방식, 권한 모델 개요는 [IAM 개요](../about-cloud/iam-overview.md)를 참고하세요.
{% endhint %}

## 자격 증명의 종류

클라우드에서 인증하는 방법은 크게 3가지입니다. **어떤 ID에 어떤 자격 증명을 쓰느냐**가 보안의 핵심입니다.

| 방식 | 특징 | 적합한 대상 |
| --- | --- | --- |
| **장기 자격 증명** (Access Key, API Key) | 만료 없음. 유출 시 즉시 악용 가능 | ❌ 가능하면 사용하지 말 것 |
| **역할 기반 임시 자격 증명** (IAM Role, Managed Identity) | 자동 발급/만료. 코드에 시크릿 불필요 | ✅ 기기/서비스 (워크로드) |
| **페더레이션** (OIDC, SAML, Workload Identity) | 외부 IdP 토큰을 클라우드 권한으로 교환 | ✅ 사람(SSO), 서드파티, CI/CD |

{% hint style="warning" %}
**원칙:** 사람은 SSO + MFA + 페더레이션, 서비스는 역할 기반 임시 자격 증명, 서드파티는 페더레이션 + 시간 제한. 장기 키는 최후의 수단입니다.
{% endhint %}

{% hint style="danger" %}
**장기 키가 위험한 이유:** Git 저장소·로그·환경변수에 노출되면 즉시 악용 가능. 퇴사자 키가 회수되지 않으면 외부에서 계속 접근 가능. 교체를 자동화하지 않으면 수년간 같은 키가 사용됩니다.
{% endhint %}

{% hint style="success" %}
**역할 기반 인증의 장점:** 토큰이 자동 발급/만료되어 유출 시 피해가 제한됩니다. 코드에 시크릿을 넣을 필요가 없고, 교체도 자동으로 이루어져 관리 부담이 없습니다.
{% endhint %}

## ID 유형별 적용

IAM에서 관리하는 ID는 크게 3가지입니다. 각각 생성/권한 부여/회수 방법이 다릅니다.

### 사람 (직원/계약직)

| 라이프사이클 | 해야 할 일 | 벤더별 방법 |
| --- | --- | --- |
| **입사** | 계정 생성 + 그룹 배정 + MFA 강제 | AWS: Identity Center에서 사용자 생성 또는 외부 IdP(Okta, Microsoft Entra ID) 연동. Azure: Entra ID 사용자 생성. Google Cloud: Cloud Identity 또는 Workspace. OCI: Identity Domain 사용자 생성 |
| **부서 이동** | 기존 그룹 제거 + 새 그룹 배정 | 그룹 기반 권한이면 그룹만 변경. 개별 정책 부여했다면 수동 정리 필요 |
| **퇴사** | 계정 비활성화 → 세션 무효화 → 일정 기간 후 삭제 | 즉시 삭제하면 감사 추적 불가. 비활성화 후 90일 보존 권장 |
| **정기 검토** | 미사용 계정/과다 권한 탐지 | AWS: Access Analyzer, Azure: Access Reviews, Google Cloud: IAM Recommender |

**실무 원칙:**
- 개별 사용자에게 직접 정책을 붙이지 말 것 → **그룹 기반** 권한 관리
- 콘솔 접근은 **SSO + MFA** 필수
- 퇴사 프로세스에 "클라우드 계정 비활성화"를 HR 체크리스트에 포함

### 기기/서비스 (워크로드)

EC2, Lambda, 컨테이너, CI/CD 파이프라인 등 **사람이 아닌 워크로드**에 권한을 부여하는 방법입니다.

| 벤더 | 권장 방식 | 설명 |
| --- | --- | --- |
| AWS | **IAM Role** (Instance Profile, Task Role, Execution Role) | EC2/ECS/Lambda에 역할을 연결하면 임시 자격 증명이 자동 주입됨 |
| Azure | **Managed Identity** (System-assigned / User-assigned) | VM/App Service/Function에 연결. 토큰 자동 발급/갱신 |
| Google Cloud | **Attached Service Account** + Workload Identity | GKE Pod에 Service Account 연결. 키 파일 불필요 |
| OCI | **Instance Principal / Resource Principal** | Compute/Function에 동적 그룹 매칭으로 권한 부여 |

**절대 하지 말 것:**
- Access Key/Service Account Key를 환경변수나 코드에 하드코딩
- 하나의 서비스 계정을 여러 워크로드가 공유 (권한 분리 불가)

**해야 할 것:**
- 워크로드별 별도 역할/ID 생성 (최소 권한 적용 가능)
- CI/CD 파이프라인은 OIDC Federation으로 임시 자격 증명 발급 (GitHub Actions → AWS Role 등)

### 서드파티 (외부 파트너/SaaS/벤더)

외부 조직이나 SaaS 서비스에 우리 클라우드 리소스 접근을 허용해야 할 때입니다.

| 시나리오 | 권장 방법 | 주의사항 |
| --- | --- | --- |
| **외부 SaaS가 우리 S3/Blob 접근** | Cross-account Role (AWS), Service Principal + RBAC (Azure), Workload Identity Federation (Google Cloud) | 외부 계정 ID를 신뢰 정책에 명시. 와일드카드(`*`) 금지 |
| **파트너사 엔지니어가 콘솔 접근** | 별도 역할 생성 + 시간 제한 + MFA 강제 | 상시 접근 금지. JIT 방식으로 필요 시에만 활성화 |
| **감사/컨설팅 업체** | 읽기 전용 역할 + 특정 리소스만 | 전체 계정 읽기 권한 부여 금지. 필요한 서비스만 |
| **CI/CD 외부 서비스 (GitHub Actions 등)** | OIDC Federation (키 없이 토큰 교환) | 장기 키 대신 OIDC 사용. 리포지토리/브랜치 조건 제한 |

**벤더별 외부 접근 메커니즘:**

| 벤더 | 크로스 계정/테넌트 | 외부 IdP 연동 |
| --- | --- | --- |
| AWS | Cross-account IAM Role (신뢰 정책에 외부 계정 ID 지정) | OIDC/SAML Federation, IAM Identity Center |
| Azure | B2B Collaboration (Entra ID 게스트), Lighthouse (MSP용) | Entra External ID, Workload Identity Federation |
| Google Cloud | Cross-project IAM binding, Workload Identity Pool | Workforce Identity Federation, Workload Identity Federation |
| OCI | Cross-tenancy Policy (`define tenancy`), Identity Domain Federation | SAML/OIDC Federation |

{% hint style="warning" %}
**서드파티 접근의 핵심 원칙:** 장기 키를 공유하지 말 것. 역할 기반 임시 접근 + 최소 권한 + 시간 제한 + 감사 로그. 계약 종료 시 즉시 신뢰 관계 제거.
{% endhint %}

## 최소 권한 실천 도구

최소 권한 원칙을 지키려면, 실제 사용되는 권한을 모니터링하고 불필요한 권한을 지속적으로 제거해야 합니다. IAM 이상 행위 탐지(비정상 API 호출 등)는 [보안 태세 관리](security-posture.md)의 위협 탐지 서비스와 연동됩니다.

| 벤더 | 제품 | 기능 |
| --- | --- | --- |
| AWS | IAM Access Analyzer | 미사용 역할/권한 탐지. CloudTrail 기반 최소 권한 정책 자동 생성 |
| AWS | CloudTrail | 모든 API 호출 기록. 누가 무엇을 했는지 감사 |
| Azure | Entra ID Governance (Access Reviews) | 정기적 권한 검토 자동화. 과다 권한 탐지 |
| Google Cloud | IAM Recommender | 미사용 권한 탐지 + 축소 권장 |
| Google Cloud | Policy Analyzer | 누가 어떤 리소스에 접근 가능한지 분석 |

### 실천 가이드

- 처음에는 넓은 권한으로 시작하되, 일정 기간 후 실제 사용된 권한만 남기고 축소합니다.
- 정기적으로(분기별) 미사용 역할과 권한을 검토합니다.
- 서비스 간 접근은 장기 자격 증명(Access Key) 대신 역할(Role)/관리 ID를 사용합니다.

## 멀티클라우드 통합 자격 증명 (Identity Federation)

여러 클라우드를 사용할 때 각 벤더에 별도 계정을 만들면 관리가 파편화됩니다. **하나의 IdP(Identity Provider)로 모든 클라우드에 SSO(Single Sign-On)를 구성**하는 것이 멀티클라우드 IAM의 출발점입니다.

| 접근 방식 | 설명 | 도구 |
| --- | --- | --- |
| **중앙 IdP + Federation** | 하나의 IdP에서 인증 후 각 클라우드에 SAML/OIDC로 연동 | Microsoft Entra ID, Okta, Google Workspace |
| **AWS Identity Center** | AWS 전용 SSO. 외부 IdP 연동 가능 | AWS IAM Identity Center |
| **크로스 클라우드 워크로드 ID** | 서비스 간 인증을 장기 키 없이 처리 | OIDC Federation, Workload Identity |

{% hint style="info" %}
멀티클라우드 환경에서 IdP를 통합하지 않으면: 계정 관리 파편화, 퇴사자 처리 누락, 권한 감사 불가능 등의 문제가 발생합니다. 가장 먼저 해야 할 일은 **하나의 IdP를 정하고 모든 클라우드를 연동**하는 것입니다.
{% endhint %}

## IAM 보안 점검 체크리스트

- [ ] 루트/전역 관리자 계정에 MFA를 설정했는가
- [ ] 일상 작업에 루트 계정을 사용하지 않는가
- [ ] 장기 자격 증명(Access Key)을 사용하는 서비스가 없는가 (역할 기반으로 전환)
- [ ] 90일 이상 미사용 계정/역할을 비활성화했는가
- [ ] 과도한 권한(AdministratorAccess 등)을 가진 사용자가 없는가
- [ ] 서비스 간 접근은 역할/Managed Identity/Instance Principal을 사용하는가
- [ ] 외부 접근(서드파티)에 시간 제한과 조건을 설정했는가
- [ ] CloudTrail/Activity Log/Audit Log가 활성화되어 있는가
- [ ] 정기적(분기별) 권한 리뷰를 수행하는가
- [ ] 퇴사자 계정 비활성화가 HR 프로세스에 포함되어 있는가
- [ ] 멀티클라우드 사용 시 중앙 IdP로 SSO를 구성했는가

## 자주 하는 실수

- **개별 사용자에게 직접 정책을 부여** — 그룹 기반 관리를 하지 않아 퇴사/이동 시 권한 정리가 누락되고 과다 권한이 누적됨
- **CI/CD에 장기 Access Key 사용** — OIDC Federation 대신 장기 키를 시크릿에 저장하여 유출 시 즉시 악용 가능
- **퇴사자 계정을 즉시 삭제** — 비활성화 없이 바로 삭제하여 감사 추적이 불가능해짐. 비활성화 후 90일 보존 권장

## 체크리스트

- [ ] 모든 사람 계정에 SSO + MFA를 적용하고, 개별 정책 대신 그룹 기반 권한을 사용하는가
- [ ] 워크로드(EC2, Lambda, CI/CD)에 장기 키 대신 역할 기반 임시 자격 증명을 사용하는가
- [ ] 분기별 미사용 계정/과다 권한 리뷰를 수행하고 있는가

## 참고하기

### AWS

- [AWS IAM 문서](https://docs.aws.amazon.com/ko_kr/iam/)
- [IAM Identity Center 문서](https://docs.aws.amazon.com/ko_kr/singlesignon/)
- [IAM Access Analyzer](https://docs.aws.amazon.com/ko_kr/IAM/latest/UserGuide/what-is-access-analyzer.html)
- [IAM 모범 사례](https://docs.aws.amazon.com/ko_kr/IAM/latest/UserGuide/best-practices.html)
- [Well-Architected — 권한 지속 축소](https://docs.aws.amazon.com/wellarchitected/latest/framework/sec_permissions_continuous_reduction.html)

### Azure

- [Microsoft Entra ID 문서](https://learn.microsoft.com/ko-kr/entra/identity/)
- [Azure RBAC 문서](https://learn.microsoft.com/ko-kr/azure/role-based-access-control/)
- [Entra ID Governance](https://learn.microsoft.com/ko-kr/entra/id-governance/)
- [Conditional Access](https://learn.microsoft.com/ko-kr/entra/identity/conditional-access/)

### Google Cloud

- [Cloud IAM 문서](https://cloud.google.com/iam/docs)
- [IAM Recommender](https://cloud.google.com/iam/docs/recommender-overview)
- [Policy Analyzer](https://cloud.google.com/policy-intelligence/docs/analyze-iam-policies)
- [Workload Identity Federation](https://cloud.google.com/iam/docs/workload-identity-federation)

### OCI

- [OCI IAM 문서](https://docs.oracle.com/en-us/iaas/Content/Identity/home.htm)
- [OCI Identity Domains](https://docs.oracle.com/en-us/iaas/Content/Identity/domains/overview.htm)
- [OCI 정책 구문](https://docs.oracle.com/iaas/Content/Identity/policyreference/policyreference.htm)
