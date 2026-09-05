---
title: "IAM 개요"
description: "IAM의 기본 개념, 인증 방식, 권한 모델을 벤더별로 비교합니다."
---

> 문서 기준: 2026년 8월

:::note
ID 유형별 관리(사람/기기/서드파티), 최소 권한 실천, 보안 점검 체크리스트 등 실무 운영은 [IAM 실무 설계와 보안 운영](../../security/iam/)을 참고하세요.
:::

## 왜 IAM이 중요한가

클라우드에서는 수백 개의 서비스와 수천 개의 리소스가 API로 접근 가능합니다. IAM을 잘못 설정하면 데이터 유출이나 리소스 삭제 같은 보안 사고로 이어집니다. **최소 권한 원칙** — 필요한 최소한의 권한만 부여하는 것이 기본 원칙입니다.

## 핵심 개념

- **사용자** (User) — 사람 또는 애플리케이션을 나타내는 ID
- **그룹** (Group) — 사용자를 묶어 권한을 일괄 부여
- **역할** (Role) — 임시로 부여할 수 있는 권한 세트. 서비스 간 접근에 주로 사용
- **정책** (Policy) — "누가, 무엇을, 어떤 리소스에" 할 수 있는지 정의하는 문서
- **MFA** — 비밀번호 외 추가 인증 수단

## 벤더별 제품 비교

| 벤더 | 제품 | 비고 |
| --- | --- | --- |
| AWS | IAM + IAM Identity Center | 사용자, 그룹, 역할, 정책. Identity Center로 멀티 계정 SSO |
| Azure | Microsoft Entra ID (구 Azure AD) | 디렉토리 서비스 + RBAC. Microsoft 365와 통합 |
| Google Cloud | Cloud IAM | 프로젝트/폴더/조직 수준 RBAC. 서비스 계정으로 서비스 간 인증 |
| OCI | OCI IAM with Identity Domains | 사용자, 그룹, 정책, 컴파트먼트 기반 접근 제어 |

## 인증 방식

| 방식 | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- |
| **콘솔 로그인** | 사용자명 + 비밀번호 + MFA | Entra ID 계정 + MFA | Google 계정 + MFA | 사용자명 + 비밀번호 + MFA |
| **CLI/SDK** | Access Key 또는 `aws login` | `az login` (브라우저) | `gcloud auth login` (브라우저) | API Key 또는 `oci session authenticate` |
| **서비스 간** | IAM Role (임시 자격 증명) | Managed Identity | Service Account | Instance Principal |
| **외부 IdP 연동** | SAML/OIDC Federation | Entra ID 외부 ID | Workforce Identity Federation | SAML/OIDC Federation |

## 권한 관리 모델

| 벤더 | 모델 | 특징 |
| --- | --- | --- |
| **AWS** | 정책 기반 (JSON) | ID 기반 + 리소스 기반 정책 조합. 가장 세밀하지만 복잡 |
| **Azure** | RBAC (역할 기반) | 기본/커스텀 역할. 범위(구독/리소스그룹/리소스) 지정. Conditional Access로 동적 제어 |
| **Google Cloud** | RBAC (역할 기반, 계층 상속) | 조직→폴더→프로젝트 상속. Workload Identity Federation으로 외부 토큰 직접 사용 |
| **OCI** | 정책 기반 (HCL 유사) | `Allow group X to manage Y in compartment Z` 직관적 구문. 컴파트먼트 계층 상속 |

## 자격 증명 방식 비교

| 벤더 | 장기 자격 증명 | 역할 기반 (권장) | 페더레이션 |
| --- | --- | --- | --- |
| AWS | Access Key | IAM Role (Instance Profile, Task Role) | OIDC/SAML Federation |
| Azure | Service Principal Secret | Managed Identity | Entra External ID, Workload Identity Federation |
| Google Cloud | Service Account Key (JSON) | Attached Service Account | Workload Identity Federation |
| OCI | API Signing Key | Instance Principal | SAML/OIDC Federation |

## 자주 하는 실수

- **"관리자 권한을 주면 편하다"** — 편의를 위해 광범위한 권한을 부여하면 사고 시 피해 범위가 커집니다. 최소 권한 원칙을 처음부터 적용하세요.
- **"Access Key를 코드에 넣어도 괜찮다"** — 장기 자격 증명이 소스 코드나 설정 파일에 노출되면 유출 위험이 큽니다. 역할(Role) 기반 임시 자격 증명을 사용하세요.
- **"IAM은 한 번 설정하면 끝이다"** — 인원 변동, 서비스 변경에 따라 권한을 주기적으로 검토하지 않으면 미사용 권한이 누적됩니다.

## 체크리스트

- [ ] 루트/전역 관리자 계정에 MFA를 활성화하고 일상 작업에 사용하지 않도록 했는가?
- [ ] 서비스 간 인증에 장기 자격 증명 대신 역할(Role/Managed Identity/Service Account)을 사용하는가?
- [ ] 사용자와 그룹에 최소 권한 원칙을 적용하고, 정기 권한 리뷰 일정을 수립했는가?

## 참고하기

### AWS

- [AWS IAM 문서](https://docs.aws.amazon.com/ko_kr/iam/)
- [IAM Identity Center](https://docs.aws.amazon.com/ko_kr/singlesignon/)

### Azure

- [Microsoft Entra ID 문서](https://learn.microsoft.com/ko-kr/entra/identity/)
- [Azure RBAC](https://learn.microsoft.com/ko-kr/azure/role-based-access-control/)

### Google Cloud

- [Cloud IAM 문서](https://cloud.google.com/iam/docs)

### OCI

- [OCI IAM 문서](https://docs.oracle.com/en-us/iaas/Content/Identity/home.htm)
