---
description: 시크릿 관리, KMS, 인증서 관리 서비스를 벤더별로 비교하고 자동 교체와 외부 도구 연동을 설명합니다.
---

# 시크릿 관리

> 문서 기준: 2026년 5월

## 개요

애플리케이션은 DB 비밀번호, API 키, 인증서 등 민감한 정보(시크릿)를 사용합니다. 이를 소스 코드나 환경 변수에 하드코딩하면 유출 위험이 큽니다. **시크릿 관리 서비스**는 민감 정보를 암호화하여 중앙에서 관리하고, 애플리케이션이 런타임에 안전하게 조회할 수 있게 합니다.

### 왜 필요한가

- **유출 방지** — Git에 커밋된 비밀번호, 로그에 노출된 API 키 등의 사고를 방지합니다.
- **자동 교체** (Rotation) — 비밀번호를 주기적으로 자동 변경하여 유출 시 피해를 최소화합니다.
- **감사** (Audit) — 누가 언제 어떤 시크릿에 접근했는지 기록합니다.
- **중앙 관리** — 여러 서비스가 사용하는 시크릿을 한 곳에서 관리합니다.

## 제품 비교

### 시크릿 관리

| 벤더 | 제품 | 비고 |
| --- | --- | --- |
| AWS | Secrets Manager | 자동 교체(RDS, Redshift 등 네이티브 연동). 크로스 계정 공유 |
| AWS | SSM Parameter Store | 간단한 키-값 저장. 무료 티어 있음. 자동 교체는 제한적 |
| Azure | Key Vault (Secrets) | 시크릿 + 키 + 인증서 통합 관리 |
| GCP | Secret Manager | 버전 관리 내장. IAM으로 접근 제어 |
| OCI | OCI Vault (Secrets) | 시크릿 저장 + 버전 관리. IAM 정책으로 접근 제어 |

### 암호화 키 관리 (KMS)

시크릿을 암호화하는 키 자체를 관리하는 서비스입니다.

| 벤더 | 제품 | 비고 |
| --- | --- | --- |
| AWS | KMS (Key Management Service) | 벤더 관리 키 / 고객 관리 키(CMK) / BYOK |
| Azure | Key Vault (Keys) | HSM 지원. Managed HSM으로 전용 HSM |
| GCP | Cloud KMS | HSM, 외부 키 관리(EKM) 지원 |
| OCI | OCI Vault (Keys) | 소프트웨어 키 / HSM 키. BYOK 지원 |

### 인증서 관리

| 벤더 | 제품 | 비고 |
| --- | --- | --- |
| AWS | ACM (Certificate Manager) | 무료 공인 인증서 발급. ALB/CloudFront 자동 연동 |
| Azure | App Service Certificates / Key Vault | Key Vault에서 인증서 수명 주기 관리 |
| GCP | Certificate Manager | 무료 관리형 인증서. Load Balancer 자동 연동 |
| OCI | OCI Certificates | 인증서 발급 및 수명 주기 관리. Load Balancer 연동 |

## 핵심 차이점

**AWS** — Secrets Manager와 Parameter Store 두 가지 선택지가 있습니다. 자동 교체가 필요하면 Secrets Manager, 단순 설정값 저장이면 Parameter Store(무료)가 적합합니다.

**Azure** — Key Vault 하나로 시크릿, 암호화 키, 인증서를 모두 관리합니다. 서비스가 분리되지 않아 관리가 단순합니다.

**GCP** — Secret Manager가 버전 관리를 기본 제공하여, 시크릿 변경 이력을 추적하고 이전 버전으로 롤백할 수 있습니다.

**OCI** — Vault 하나로 시크릿과 암호화 키를 통합 관리하며, HSM 키와 소프트웨어 키를 선택할 수 있습니다. IAM 정책으로 세밀한 접근 제어가 가능합니다.

## 암호화 키 관리 모델

암호화 키를 누가 생성하고 관리하는지에 따라 3가지 모델이 있습니다.

| 모델 | 설명 | 특징 |
| --- | --- | --- |
| **벤더 관리 키 (Vendor-Managed)** | 벤더가 키 생성·관리·교체 | 기본값. 사용자 개입 최소 |
| **고객 관리 키 (CMK/CMEK)** | 사용자가 KMS에서 키 생성·관리 | 키 정책, 교체 주기, 접근 제어를 사용자가 직접 관리 |
| **BYOK (Bring Your Own Key)** | 사용자가 외부에서 키를 가져와 KMS에 업로드 | 키 원본을 외부에 보관. 규제 요건 대응 |
| **EKM/HYOK (External Key Management)** | 외부 HSM에 키를 두고 KMS는 참조만 | 키가 클라우드에 저장되지 않음. 가장 엄격한 통제 |

{% hint style="info" %}
규제 산업(금융, 의료, 공공)은 CMK 또는 BYOK가 일반적이며, 일반 웹 서비스는 벤더 관리 키로 충분한 경우가 많습니다.
{% endhint %}

## 시크릿 자동 교체 (Rotation)

시크릿을 주기적으로 자동 변경하면 유출 시 피해를 최소화할 수 있습니다.

| 벤더 | 자동 교체 지원 |
| --- | --- |
| AWS Secrets Manager | RDS, DocumentDB, Redshift 네이티브 교체. Lambda로 커스텀 교체 함수 작성 가능 |
| Azure Key Vault | 인증서 자동 갱신. 시크릿은 Event Grid + Function App으로 교체 구현 |
| GCP Secret Manager | 시크릿 버전 관리만 제공. 교체 로직은 Cloud Scheduler + Cloud Function으로 구현 |
| OCI Vault | Secret Rotation 지원 (Autonomous DB, MySQL 네이티브). Function으로 커스텀 교체 |

### 외부 시크릿 저장소 연동

HashiCorp Vault, CyberArk 등 외부 시크릿 관리 솔루션을 사용하는 경우, 클라우드 네이티브 서비스와 통합할 수 있습니다.

| 통합 방식 | 설명 |
| --- | --- |
| **External Secrets Operator** | Kubernetes에서 AWS/Azure/GCP 시크릿을 외부 저장소에서 동기화 |
| **HashiCorp Vault Dynamic Secrets** | Vault가 AWS IAM, DB 자격 증명을 동적으로 생성 |
| **CSI Secret Store Driver** | Kubernetes Pod에 시크릿을 파일로 마운트 |

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

### OCI

- [OCI Vault 문서](https://docs.oracle.com/en-us/iaas/Content/KeyManagement/home.htm)
- [OCI Certificates 문서](https://docs.oracle.com/en-us/iaas/Content/certificates/home.htm)
