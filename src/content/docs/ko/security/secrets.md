---
title: "시크릿 관리"
description: "시크릿 관리, KMS, 인증서 관리 서비스를 벤더별로 비교하고 자동 교체와 외부 도구 연동을 설명합니다."
---

> 문서 기준: 2026년 8월

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
| Google Cloud | Secret Manager | 버전 관리 내장. IAM으로 접근 제어 |
| OCI | OCI Vault (Secrets) | 시크릿 저장 + 버전 관리. IAM 정책으로 접근 제어 |

### 암호화 키 관리 (KMS)

시크릿을 암호화하는 키 자체를 관리하는 서비스입니다.

| 벤더 | 제품 | 비고 |
| --- | --- | --- |
| AWS | KMS (Key Management Service) | 벤더 관리 키 / 고객 관리 키(CMK) / BYOK |
| Azure | Key Vault (Keys) | HSM 지원. Managed HSM으로 전용 HSM |
| Google Cloud | Cloud KMS | HSM, 외부 키 관리(EKM) 지원 |
| OCI | OCI Vault (Keys) | 소프트웨어 키 / HSM 키. BYOK 지원 |

### 인증서 관리

| 벤더 | 제품 | 비고 |
| --- | --- | --- |
| AWS | ACM (Certificate Manager) | 무료 공인 인증서 발급. ALB/CloudFront 자동 연동 |
| Azure | App Service Certificates / Key Vault | Key Vault에서 인증서 수명 주기 관리 |
| Google Cloud | Certificate Manager | 무료 관리형 인증서. Load Balancer 자동 연동 |
| OCI | OCI Certificates | 인증서 발급 및 수명 주기 관리. Load Balancer 연동 |

## 핵심 차이점

**AWS** — Secrets Manager와 Parameter Store 두 가지 선택지가 있습니다. 자동 교체가 필요하면 Secrets Manager, 단순 설정값 저장이면 Parameter Store(무료)가 적합합니다. 2025–2026년에 Managed External Secrets 기능이 추가되어 Salesforce, MongoDB Atlas, Confluent Cloud, Jenkins 등 서드파티 자격 증명의 표준화된 관리와 자동 교체도 지원합니다.

**Azure** — Key Vault 하나로 시크릿, 암호화 키, 인증서를 모두 관리합니다. 서비스가 분리되지 않아 관리가 단순합니다.

**Google Cloud** — Secret Manager가 버전 관리를 기본 제공하여, 시크릿 변경 이력을 추적하고 이전 버전으로 롤백할 수 있습니다. 교체 스케줄(Rotation Schedule)을 네이티브로 설정할 수 있어, 지정 주기마다 Pub/Sub로 알림을 보내 Cloud Function에서 교체를 실행하는 패턴을 쉽게 구현할 수 있습니다.

**OCI** — Vault 하나로 시크릿과 암호화 키를 통합 관리하며, HSM 키와 소프트웨어 키를 선택할 수 있습니다. IAM 정책으로 세밀한 접근 제어가 가능합니다.

## 암호화 키 관리 모델

암호화 키를 누가 생성하고 관리하는지에 따라 3가지 모델이 있습니다.

| 모델 | 설명 | 특징 |
| --- | --- | --- |
| **벤더 관리 키 (Vendor-Managed)** | 벤더가 키 생성·관리·교체 | 기본값. 사용자 개입 최소 |
| **고객 관리 키 (CMK/CMEK)** | 사용자가 KMS에서 키 생성·관리 | 키 정책, 교체 주기, 접근 제어를 사용자가 직접 관리 |
| **BYOK (Bring Your Own Key)** | 사용자가 외부에서 키를 가져와 KMS에 업로드 | 키 원본을 외부에 보관. 규제 요건 대응 |
| **EKM/HYOK (External Key Management)** | 외부 HSM에 키를 두고 KMS는 참조만 | 키가 클라우드에 저장되지 않음. 가장 엄격한 통제 |

:::note
규제 산업(금융, 의료, 공공)은 CMK 또는 BYOK가 일반적이며, 일반 웹 서비스는 벤더 관리 키로 충분한 경우가 많습니다.
:::

## 시크릿 자동 교체 (Rotation)

시크릿을 주기적으로 자동 변경하면 유출 시 피해를 최소화할 수 있습니다.

| 벤더 | 자동 교체 지원 |
| --- | --- |
| AWS Secrets Manager | RDS, DocumentDB, Redshift 네이티브 교체. Lambda로 커스텀 교체 함수 작성 가능. Managed External Secrets로 서드파티(Salesforce, MongoDB Atlas, Confluent Cloud, Jenkins 등) 자격 증명도 자동 교체 |
| Azure Key Vault | 인증서 자동 갱신. 시크릿은 Event Grid + Function App으로 교체 구현 |
| Google Cloud Secret Manager | 교체 스케줄(Rotation Schedule) 네이티브 지원 — 교체 주기와 시간을 설정하면 Pub/Sub 토픽으로 알림 발송. Cloud Function이 구독하여 실제 교체 로직을 실행하는 패턴 |
| OCI Vault | Secret Rotation 지원 (Autonomous DB, MySQL 네이티브). Function으로 커스텀 교체 |

### 외부 시크릿 저장소 연동

HashiCorp Vault, CyberArk 등 외부 시크릿 관리 솔루션을 사용하는 경우, 클라우드 네이티브 서비스와 통합할 수 있습니다.

| 통합 방식 | 설명 |
| --- | --- |
| **External Secrets Operator** | 클라우드 벤더 시크릿 저장소(AWS Secrets Manager, Azure Key Vault 등)의 시크릿을 Kubernetes Secret으로 자동 동기화. v1.x GA 달성으로 프로덕션 안정성 확보 |
| **HashiCorp Vault Dynamic Secrets** | Vault가 AWS IAM, DB 자격 증명을 동적으로 생성 |
| **CSI Secret Store Driver** | Kubernetes Pod에 시크릿을 파일로 마운트 |

## 구성/프로퍼티 관리 (Configuration Management)

시크릿(비밀번호, API 키)과 달리, **구성값**(feature flag, 엔드포인트 URL, 타임아웃 값 등)은 민감하지 않지만 중앙에서 관리하고 런타임에 동적으로 변경할 필요가 있습니다. 각 벤더는 시크릿 관리와 별도로(또는 통합하여) 구성 관리 서비스를 제공합니다.

### 시크릿 vs 구성값

| 구분 | 시크릿 | 구성값 |
| --- | --- | --- |
| **예시** | DB 비밀번호, API 키, 인증서 | Feature flag, 엔드포인트 URL, 타임아웃, 환경별 설정 |
| **암호화** | 필수 (저장 시 + 전송 시) | 선택 (민감한 설정은 암호화) |
| **접근 제어** | 최소 권한, 감사 필수 | 팀/서비스 단위 |
| **교체 주기** | 주기적 자동 교체 권장 | 배포/릴리스 시 변경 |
| **저장 위치** | Secrets Manager / Key Vault | Parameter Store / App Configuration |

### 벤더별 구성 관리 서비스

| 벤더 | 서비스 | 특징 |
| --- | --- | --- |
| AWS | [SSM Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html) | 계층형 키-값 저장. String/StringList/SecureString 타입. 무료 표준 티어 (10,000개). 고급 티어는 정책 기반 만료/알림 |
| AWS | [AWS AppConfig](https://docs.aws.amazon.com/appconfig/latest/userguide/what-is-appconfig.html) | Feature flag + 구성 배포. 점진적 롤아웃, 검증 후 배포, 자동 롤백 |
| Azure | [Azure App Configuration](https://learn.microsoft.com/azure/azure-app-configuration/overview) | 중앙 구성 저장소. Feature flag 내장. Key Vault 참조로 시크릿 연동. 라벨로 환경별 분리 |
| Google Cloud | [Runtime Configurator](https://cloud.google.com/deployment-manager/runtime-configurator) (레거시) / [Firebase Remote Config](https://firebase.google.com/docs/remote-config) | Runtime Configurator는 제한적. 서버 앱은 Secret Manager에 비밀이 아닌 값도 저장하는 패턴이 일반적 |
| OCI | [OCI Resource Manager Variables](https://docs.oracle.com/en-us/iaas/Content/ResourceManager/Concepts/resourcemanager.htm) / Vault | 전용 구성 서비스 없음. Vault에 비밀이 아닌 값도 저장하거나, Object Storage + 앱 로직으로 구현 |

### 실무 패턴

- **환경별 분리** — `dev/db-endpoint`, `prod/db-endpoint`처럼 경로 또는 라벨로 환경 구분
- **Feature flag** — 코드 배포 없이 기능 ON/OFF. AWS AppConfig, Azure App Configuration이 네이티브 지원
- **동적 리로드** — 구성 변경 시 애플리케이션 재시작 없이 반영. 폴링 또는 이벤트 기반
- **시크릿 참조** — 구성 서비스에서 시크릿 값을 직접 저장하지 않고, Secrets Manager/Key Vault의 ARN/URI를 참조

:::note
**Google Cloud/OCI 사용자:** 전용 구성 관리 서비스가 약하므로, Kubernetes ConfigMap + External Secrets Operator 조합이나 HashiCorp Consul을 고려하세요. 멀티클라우드 환경에서는 벤더 중립적인 외부 도구가 유리할 수 있습니다.
:::

## 자주 하는 실수

- **시크릿 하드코딩** — 소스 코드나 설정 파일에 비밀번호, API 키를 직접 작성하면 Git 이력에 영구히 남아 유출 위험이 큽니다.
- **로테이션 없이 영구 사용** — 시크릿을 한 번 생성한 후 교체하지 않으면, 유출 시 피해 범위가 무한히 확대됩니다.
- **환경변수에 직접 저장** — 시크릿을 환경변수에 평문으로 저장하면 프로세스 목록, 로그, 크래시 덤프에 노출될 수 있습니다. 시크릿 저장소에서 런타임에 조회하세요.

## 체크리스트

- [ ] 모든 시크릿을 전용 저장소(Secrets Manager, Key Vault 등)에서 관리하고 있는가
- [ ] 자동 교체(Rotation)를 설정했는가
- [ ] pre-commit hook으로 시크릿 커밋을 방지하고 있는가 (git-secrets, detect-secrets 등)
- [ ] 시크릿 접근 감사 로그를 활성화했는가

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

### Google Cloud

- [Secret Manager 문서](https://cloud.google.com/secret-manager/docs)
- [Cloud KMS 문서](https://cloud.google.com/kms/docs)
- [Certificate Manager 문서](https://cloud.google.com/certificate-manager/docs)

### OCI

- [OCI Vault 문서](https://docs.oracle.com/en-us/iaas/Content/KeyManagement/home.htm)
- [OCI Certificates 문서](https://docs.oracle.com/en-us/iaas/Content/certificates/home.htm)
