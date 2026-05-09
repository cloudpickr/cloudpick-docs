# 시크릿 관리

## 개요

애플리케이션은 DB 비밀번호, API 키, 인증서 등 민감한 정보(시크릿)를 사용합니다. 이를 소스 코드나 환경 변수에 하드코딩하면 유출 위험이 큽니다. **시크릿 관리 서비스**는 민감 정보를 암호화하여 중앙에서 관리하고, 애플리케이션이 런타임에 안전하게 조회할 수 있게 합니다.

### 왜 필요한가

- **유출 방지** — Git에 커밋된 비밀번호, 로그에 노출된 API 키 등의 사고를 방지합니다.
- **자동 교체(Rotation)** — 비밀번호를 주기적으로 자동 변경하여 유출 시 피해를 최소화합니다.
- **감사(Audit)** — 누가 언제 어떤 시크릿에 접근했는지 기록합니다.
- **중앙 관리** — 여러 서비스가 사용하는 시크릿을 한 곳에서 관리합니다.

## 제품 비교

### 시크릿 관리

| 벤더 | 제품 | 비고 |
| --- | --- | --- |
| AWS | Secrets Manager | 자동 교체(RDS, Redshift 등 네이티브 연동). 크로스 계정 공유 |
| AWS | SSM Parameter Store | 간단한 키-값 저장. 무료 티어 있음. 자동 교체는 제한적 |
| Azure | Key Vault (Secrets) | 시크릿 + 키 + 인증서 통합 관리 |
| GCP | Secret Manager | 버전 관리 내장. IAM으로 접근 제어 |

### 암호화 키 관리 (KMS)

시크릿을 암호화하는 키 자체를 관리하는 서비스입니다.

| 벤더 | 제품 | 비고 |
| --- | --- | --- |
| AWS | KMS (Key Management Service) | 벤더 관리 키 / 고객 관리 키(CMK) / BYOK |
| Azure | Key Vault (Keys) | HSM 지원. Managed HSM으로 전용 HSM |
| GCP | Cloud KMS | HSM, 외부 키 관리(EKM) 지원 |

### 인증서 관리

| 벤더 | 제품 | 비고 |
| --- | --- | --- |
| AWS | ACM (Certificate Manager) | 무료 공인 인증서 발급. ALB/CloudFront 자동 연동 |
| Azure | App Service Certificates / Key Vault | Key Vault에서 인증서 수명 주기 관리 |
| GCP | Certificate Manager | 무료 관리형 인증서. Load Balancer 자동 연동 |

## 핵심 차이점

**AWS** — Secrets Manager와 Parameter Store 두 가지 선택지가 있습니다. 자동 교체가 필요하면 Secrets Manager, 단순 설정값 저장이면 Parameter Store(무료)가 적합합니다.

**Azure** — Key Vault 하나로 시크릿, 암호화 키, 인증서를 모두 관리합니다. 서비스가 분리되지 않아 관리가 단순합니다.

**GCP** — Secret Manager가 버전 관리를 기본 제공하여, 시크릿 변경 이력을 추적하고 이전 버전으로 롤백할 수 있습니다.

## 참고하기

### AWS

- [AWS Secrets Manager 문서](https://docs.aws.amazon.com/ko_kr/secretsmanager/)
- [AWS KMS 문서](https://docs.aws.amazon.com/ko_kr/kms/)
- [AWS Certificate Manager 문서](https://docs.aws.amazon.com/ko_kr/acm/)
- [SSM Parameter Store](https://docs.aws.amazon.com/ko_kr/systems-manager/latest/userguide/systems-manager-parameter-store.html)

### Azure

- [Azure Key Vault 문서](https://learn.microsoft.com/ko-kr/azure/key-vault/)
- [Key Vault 시크릿](https://learn.microsoft.com/ko-kr/azure/key-vault/secrets/)
- [Key Vault 인증서](https://learn.microsoft.com/ko-kr/azure/key-vault/certificates/)

### GCP

- [Secret Manager 문서](https://cloud.google.com/secret-manager/docs)
- [Cloud KMS 문서](https://cloud.google.com/kms/docs)
- [Certificate Manager 문서](https://cloud.google.com/certificate-manager/docs)
