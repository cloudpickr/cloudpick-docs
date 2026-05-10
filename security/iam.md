# IAM과 접근 제어

## 개요

온프레미스에서는 Active Directory나 LDAP으로 사용자를 관리하고, 서버별로 접근 권한을 설정합니다. 클라우드에서는 수백 개의 서비스와 수천 개의 리소스가 있으므로, 누가 무엇을 할 수 있는지를 체계적으로 관리하는 **IAM** (Identity and Access Management)이 핵심입니다.

> AWS IAM을 아시는 분을 위해: Azure는 Entra ID, GCP는 Cloud IAM, OCI는 IAM with Identity Domains입니다.

IAM을 잘못 설정하면 데이터 유출이나 리소스 삭제 같은 보안 사고로 이어집니다. **최소 권한 원칙** (Principle of Least Privilege) — 필요한 최소한의 권한만 부여하는 것이 기본 원칙입니다.

### 핵심 개념

- **사용자** (User) — 사람 또는 애플리케이션을 나타내는 ID
- **그룹** (Group) — 사용자를 묶어 권한을 일괄 부여
- **역할** (Role) — 임시로 부여할 수 있는 권한 세트. 서비스 간 접근에 주로 사용
- **정책** (Policy) — "누가, 무엇을, 어떤 리소스에" 할 수 있는지 정의하는 JSON/YAML 문서
- **MFA(Multi-Factor Authentication)** — 비밀번호 외 추가 인증 수단

## 제품 비교

| 벤더 | 제품 | 비고 |
| --- | --- | --- |
| AWS | IAM | 사용자, 그룹, 역할, 정책. IAM Identity Center(구 SSO)로 멀티 계정 통합 |
| Azure | Microsoft Entra ID (구 Azure AD) | 디렉토리 서비스 + RBAC. Microsoft 365와 통합 |
| GCP | Cloud IAM | 프로젝트/폴더/조직 수준 RBAC. 서비스 계정으로 서비스 간 인증 |
| OCI | OCI IAM with Identity Domains | 사용자, 그룹, 정책, 컴파트먼트 기반 접근 제어 |

### 인증 방식

| 방식 | AWS | Azure | GCP | OCI |
| --- | --- | --- | --- | --- |
| **콘솔 로그인** | 사용자명 + 비밀번호 + MFA | Entra ID 계정 + MFA | Google 계정 + MFA | 사용자명 + 비밀번호 + MFA |
| **CLI/SDK** | Access Key 또는 `aws login` | `az login` (브라우저) | `gcloud auth login` (브라우저) | API Key + Config 또는 `oci session authenticate` |
| **서비스 간** | IAM Role (임시 자격 증명) | Managed Identity | Service Account | Instance Principal / Resource Principal |
| **외부 IdP 연동** | SAML/OIDC Federation | Entra ID 외부 ID | Workforce Identity Federation | SAML/OIDC Federation |

### 권한 관리 모델

| 벤더 | 모델 | 비고 |
| --- | --- | --- |
| AWS | 정책 기반 (JSON Policy Document) | Identity-based + Resource-based 정책 조합 |
| Azure | RBAC (역할 기반 접근 제어) | 기본 제공 역할 + 커스텀 역할. 범위(구독/리소스그룹/리소스) 지정 |
| GCP | RBAC (역할 기반) | 기본 역할, 사전 정의 역할, 커스텀 역할. 조직/폴더/프로젝트 상속 |
| OCI | 정책 기반 (HCL 유사 구문) | 컴파트먼트 계층 구조에서 정책 상속. 동사+리소스 타입 조합 |

## 핵심 차이점

**AWS IAM** — 정책 문서(JSON)로 매우 세밀한 권한 제어가 가능합니다. 리소스 기반 정책(S3 버킷 정책 등)과 ID 기반 정책을 조합하는 구조가 강력하지만 복잡합니다. IAM Identity Center로 멀티 계정 SSO를 관리합니다.

**Azure Entra ID** — Active Directory 기반이라 기존 온프레미스 AD와 하이브리드 연동이 자연스럽습니다. Conditional Access로 디바이스 상태, 위치, 위험 수준에 따라 접근을 동적으로 제어할 수 있습니다.

**GCP Cloud IAM** — 조직 → 폴더 → 프로젝트 계층에서 권한이 상속됩니다. 서비스 계정(Service Account)으로 서비스 간 인증을 처리하며, Workload Identity Federation으로 외부 IdP의 토큰을 직접 사용할 수 있습니다.

**OCI IAM with Identity Domains** — HCL 유사 구문의 정책 언어로 `Allow group <그룹> to <동사> <리소스타입> in compartment <컴파트먼트>` 형태로 권한을 정의합니다. 컴파트먼트 계층에서 정책이 상속되며, Identity Domains로 멀티 테넌시 ID 관리와 외부 IdP 페더레이션을 지원합니다.

## 최소 권한 실천 도구

최소 권한 원칙을 지키려면, 실제 사용되는 권한을 모니터링하고 불필요한 권한을 지속적으로 제거해야 합니다.

| 벤더 | 제품 | 기능 |
| --- | --- | --- |
| AWS | IAM Access Analyzer | 미사용 역할/권한 탐지. CloudTrail 기반 최소 권한 정책 자동 생성 |
| AWS | CloudTrail | 모든 API 호출 기록. 누가 무엇을 했는지 감사 |
| Azure | Entra ID Governance (Access Reviews) | 정기적 권한 검토 자동화. 과다 권한 탐지 |
| Azure | Access Reviews | 정기적 권한 검토 자동화 |
| GCP | IAM Recommender | 미사용 권한 탐지 + 축소 권장 |
| GCP | Policy Analyzer | 누가 어떤 리소스에 접근 가능한지 분석 |

### 실천 가이드

- 처음에는 넓은 권한으로 시작하되, 일정 기간 후 실제 사용된 권한만 남기고 축소합니다.
- 정기적으로(분기별) 미사용 역할과 권한을 검토합니다.
- 서비스 간 접근은 장기 자격 증명(Access Key) 대신 역할(Role)/관리 ID를 사용합니다.

### 장기 자격 증명 vs 역할 기반 인증

| 방식 | 예시 | 위험성 |
| --- | --- | --- |
| **장기 자격 증명** | AWS Access Key, Azure Service Principal Secret | 유출 시 만료 전까지 무제한 접근. 코드/환경변수에 하드코딩되기 쉬움. 교체 주기 관리 필요 |
| **역할 기반 (임시 자격 증명)** | AWS IAM Role, Azure Managed Identity, GCP Service Account (Workload Identity), OCI Instance Principal | 임시 토큰 자동 발급/만료. 유출되어도 수 분~수 시간 내 만료. 코드에 시크릿 불필요 |

**장기 자격 증명이 위험한 이유:**

- Access Key가 Git 저장소, 로그, 환경변수에 노출되면 즉시 악용 가능
- 퇴사자의 키가 회수되지 않으면 외부에서 계속 접근 가능
- 키 교체(rotation)를 자동화하지 않으면 수년간 같은 키가 사용됨

**역할 기반 인증의 장점:**

- 자격 증명이 인스턴스/서비스에 자동으로 주입되므로 코드에 시크릿을 넣을 필요 없음
- 토큰이 자동 만료되므로 유출 시 피해 범위가 제한됨
- 교체가 자동으로 이루어져 관리 부담 없음

| 벤더 | 장기 자격 증명 | 역할 기반 대안 |
| --- | --- | --- |
| AWS | Access Key ID + Secret | IAM Role (EC2 Instance Profile, ECS Task Role, Lambda Execution Role) |
| Azure | Service Principal Client Secret | Managed Identity (System-assigned / User-assigned) |
| GCP | Service Account Key (JSON) | Workload Identity, Attached Service Account |
| OCI | API Signing Key | Instance Principal, Resource Principal |

> **원칙:** 사람이 사용하는 계정은 MFA + SSO, 서비스가 사용하는 계정은 역할 기반 임시 자격 증명을 사용하세요.

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

### GCP

- [Cloud IAM 문서](https://cloud.google.com/iam/docs)
- [IAM Recommender](https://cloud.google.com/iam/docs/recommender-overview)
- [Policy Analyzer](https://cloud.google.com/policy-intelligence/docs/analyze-iam-policies)
- [Workload Identity Federation](https://cloud.google.com/iam/docs/workload-identity-federation)

### OCI

- [OCI IAM 문서](https://docs.oracle.com/en-us/iaas/Content/Identity/home.htm)
- [OCI Identity Domains](https://docs.oracle.com/en-us/iaas/Content/Identity/domains/overview.htm)
- [OCI 정책 구문](https://docs.oracle.com/en-us/iaas/Content/Identity/policysyntax/policysyntax.htm)
