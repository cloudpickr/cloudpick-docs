# IAM과 접근 제어

## 개요

클라우드에서는 수백 개의 서비스와 수천 개의 리소스가 있으므로, "누가 무엇을 할 수 있는가"를 체계적으로 관리하는 IAM (Identity and Access Management)이 핵심입니다.

## 글로벌 4사 비교

| 항목 | AWS | Azure | GCP | OCI |
| --- | --- | --- | --- | --- |
| **IAM 서비스** | IAM, IAM Identity Center | Microsoft Entra ID | Cloud IAM | IAM with Identity Domains |
| **권한 모델** | 정책 기반 (JSON) | RBAC (역할 기반) | RBAC (역할 기반) | 정책 기반 (HCL 유사) |
| **SSO** | IAM Identity Center | Entra ID SSO | Cloud Identity | Identity Domains |
| **외부 IdP 연동** | SAML, OIDC | SAML, OIDC, WS-Fed | Workload Identity Federation | SAML, OIDC |
| **최소 권한 도구** | IAM Access Analyzer | Entra Permissions Management | IAM Recommender | Cloud Guard |

### 핵심 차이점

| 벤더 | 권한 모델 | 차별점 |
| --- | --- | --- |
| **AWS** | JSON 정책 문서 (ID 기반 + 리소스 기반) | 가장 세밀하고 유연하지만 복잡 |
| **Azure** | RBAC (역할 기반) | AD 하이브리드 연동, Conditional Access로 동적 제어 |
| **GCP** | RBAC (역할 기반, 계층 상속) | Workload Identity Federation으로 외부 토큰 직접 사용 |
| **OCI** | 정책 기반 (HCL 유사 구문, 계층 상속) | `Allow group X to manage Y in compartment Z` 직관적 구문 |

## 자세한 내용

최소 권한 원칙, 장기 자격 증명 vs 역할 기반 인증, 감사 도구 등 실무 가이드는 아래 문서에서 다룹니다.

→ [IAM과 접근 제어 (심화)](../security/iam.md)
