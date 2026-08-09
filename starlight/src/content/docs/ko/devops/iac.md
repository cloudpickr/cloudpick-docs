---
title: "코드로 관리하는 인프라 (IaC)"
description: "IaC 개념, 벤더 네이티브/멀티클라우드 도구 비교, Terraform 상태 관리와 모듈 설계를 다룹니다."
---

> 문서 기준: 2026년 5월

## 개요

콘솔에서 클릭으로 인프라를 만들면 빠르지만, 재현이 불가능하고 변경 이력을 추적할 수 없습니다. CLI 스크립트로 자동화해도 "현재 상태가 어떤지"를 코드가 알지 못합니다. 담당자가 바뀌면 "이 서버가 왜 이렇게 설정되어 있는지" 아무도 모르는 상황이 됩니다.

**IaC** (Infrastructure as Code)는 인프라의 원하는 상태를 코드로 정의하여, 버전 관리, 코드 리뷰, 자동 배포, 변경 추적을 가능하게 합니다. 온프레미스에서 서버 설정을 문서로 관리하던 것을, 실행 가능한 코드로 대체하는 것입니다.

| 방식 | 문제 | IaC로 해결 |
| --- | --- | --- |
| 콘솔 클릭 | 재현 불가, 이력 없음, 실수 추적 어려움 | 코드 = 문서 = 실행 가능한 설계도 |
| CLI 스크립트 | 현재 상태 모름, 멱등성 없음 | 선언형: 현재 상태와 비교하여 차이만 적용 |
| 수동 문서화 | 문서와 실제가 불일치 | 코드가 곧 최신 상태 (Single Source of Truth) |

### 명령형 vs 선언형

- **명령형** (Imperative) — "이것을 만들어라, 저것을 삭제해라" 순서대로 실행. CLI 스크립트.
- **선언형** (Declarative) — "최종 상태는 이것이다"를 정의. 도구가 현재 상태와 비교하여 차이만 적용. IaC의 주류.

## 제품 비교

### 벤더 네이티브 IaC

| 벤더 | 제품 | 언어/형식 | 비고 |
| --- | --- | --- | --- |
| AWS | CloudFormation | YAML, JSON | AWS 전용. 스택 단위 관리 |
| AWS | CDK (Cloud Development Kit) | TypeScript, Python, Java, Go, C# | 프로그래밍 언어로 CloudFormation 생성 |
| Azure | Bicep | Bicep DSL | ARM Template의 간결한 대안 |
| Azure | ARM Templates | JSON | Azure 네이티브. 복잡하지만 완전한 기능 |
| Google Cloud | Config Connector | Kubernetes YAML | K8s 리소스처럼 Google Cloud 리소스 관리 |
| OCI | OCI Resource Manager | HCL (Terraform) | Terraform 기반. OCI 네이티브 관리형 |

### 멀티클라우드 IaC

| 제품 | 언어 | 비고 |
| --- | --- | --- |
| Terraform / OpenTofu | HCL (HashiCorp Configuration Language) | 가장 널리 사용. 모든 벤더 지원 |
| Pulumi | TypeScript, Python, Go, C#, Java | 일반 프로그래밍 언어 사용. 테스트 용이 |
| Crossplane | Kubernetes YAML | K8s 클러스터에서 클라우드 리소스 관리 |

### 통합 리소스 관리 API

IaC 도구가 리소스를 관리하려면 각 서비스별 API를 호출해야 합니다. AWS는 이를 단일 API로 표준화했습니다.

| 벤더 | 제품 | 비고 |
| --- | --- | --- |
| AWS | Cloud Control API | 모든 AWS + 3rd party 리소스를 CRUD-L 단일 API로 관리. Terraform 등 IaC 도구의 백엔드로 사용 |
| Azure | Azure Resource Manager (ARM) REST API | 모든 Azure 리소스를 단일 관리 계층으로 제어. AzAPI Terraform 프로바이더로 직접 호출 가능 |
| Google Cloud | — (서비스별 개별 API) | Config Connector가 K8s API로 추상화하지만, 통합 CRUD API는 없음 |
| OCI | OCI Resource Manager API | Terraform State 관리 + 리소스 프로비저닝 API |

AWS Cloud Control API는 Terraform이 새 AWS 리소스를 지원할 때 개별 서비스 API 대신 Cloud Control API를 백엔드로 사용할 수 있어, 새 서비스 출시 시 IaC 지원이 빨라집니다.

## 핵심 차이점

**AWS CloudFormation / CDK** — AWS 서비스와 가장 빠르게 연동됩니다. 새 서비스 출시 시 CloudFormation 지원이 가장 먼저 나옵니다. CDK는 프로그래밍 언어의 조건문, 반복문, 추상화를 활용할 수 있어 대규모 인프라 관리에 유리합니다.

**Azure Bicep** — ARM Template의 복잡한 JSON을 간결한 DSL로 대체합니다. VS Code 확장으로 자동 완성과 검증을 제공합니다.

**Terraform** — 멀티클라우드 환경에서 사실상 표준입니다. 하나의 언어(HCL)로 AWS, Azure, Google Cloud를 모두 관리할 수 있습니다. 상태 파일(State) 관리가 필요합니다.

**OCI Resource Manager** — Terraform 기반의 관리형 IaC 서비스로, 상태 파일 관리와 리소스 프로비저닝을 OCI 콘솔에서 통합 운영할 수 있습니다.

## Terraform 상태 관리

Terraform은 현재 인프라 상태를 `terraform.tfstate` 파일에 저장합니다. 이 파일은 다음 역할을 합니다.

- **리소스 매핑** — 코드의 리소스를 실제 클라우드 리소스 ID와 연결
- **의존성 추적** — 변경 시 어떤 리소스를 먼저/나중에 처리할지 결정
- **성능 최적화** — 매번 모든 리소스를 조회하지 않고 캐시된 상태 사용

### 로컬 vs 원격 백엔드

:::caution
`terraform.tfstate` 파일에는 리소스 ID, IP 등이 담겨 있으며, 시크릿이 **평문으로 저장**될 수 있습니다. 로컬에 저장하지 말고 반드시 **원격 백엔드를 사용**하고, 상태 파일 접근 권한을 최소화하세요.
:::

| 방식 | 장점 | 단점 |
| --- | --- | --- |
| **로컬 상태** | 설정 간단 | 팀 협업 불가, 파일 유실 위험, 시크릿이 plaintext로 저장 |
| **원격 백엔드** | 팀 협업, 잠금(locking), 암호화, 버전 관리 | 초기 설정 필요 |

### 원격 백엔드 옵션

| 백엔드 | 사용 사례 |
| --- | --- |
| **S3 + DynamoDB** | AWS 환경. S3는 상태 저장, DynamoDB는 동시 실행 잠금 |
| **Azure Storage** | Azure 환경. Blob Storage + Lease 기반 잠금 |
| **GCS** | Google Cloud 환경. 객체 버전 관리로 이력 추적 |
| **OCI Resource Manager** | OCI 관리형 백엔드. 상태와 실행을 OCI에서 통합 관리 |
| **Terraform Cloud / HCP Terraform** | 멀티클라우드. UI, 정책, 팀 관리 통합 |

## 모듈 설계 모범사례

Terraform 모듈은 재사용 가능한 인프라 단위입니다.

### 계층 구조

```text
environments/
├── dev/
│   └── main.tf       # 모듈 호출
├── staging/
│   └── main.tf
└── prod/
    └── main.tf

modules/
├── vpc/              # 범용 VPC 모듈
├── eks-cluster/      # EKS 클러스터 모듈
└── rds-instance/     # RDS 모듈
```

### 모범사례

- **작게 나누기** — 한 모듈이 너무 많은 리소스를 관리하면 재사용이 어려움
- **입력 변수로 유연성 확보** — 하드코딩 지양, `variables.tf`로 노출
- **출력(outputs)으로 의존성 명시** — 다른 모듈이 참조할 수 있도록
- **버전 고정** — Git 태그 또는 Terraform Registry 버전으로 고정
- **기본값 신중히** — 프로덕션에 부적합한 기본값(예: `deletion_protection = false`)은 피하기

## 드리프트(Drift) 관리

IaC 외부에서 리소스가 수동으로 변경되면 코드와 실제 상태가 불일치하게 됩니다(드리프트).

| 벤더 | 드리프트 탐지 도구 |
| --- | --- |
| AWS | CloudFormation Drift Detection, Config Rules |
| Azure | Policy, Blueprints Compliance |
| Google Cloud | Config Connector (K8s 모델로 드리프트 자동 수정) |
| OCI | Resource Manager Drift Detection |
| Terraform | `terraform plan` (현재 상태와 코드 비교) |

드리프트를 근본적으로 막으려면 **SCP/Azure Policy/Organization Policy**로 콘솔에서의 수동 변경을 제한하고, 모든 변경을 IaC 파이프라인을 통해서만 수행하도록 강제합니다. IaC 코드 자체의 보안 검증(Checkov, tfsec 등)은 [DevSecOps](../../devops/devsecops/)를 참고하세요.

## 자주 하는 실수

- **콘솔 직접 수정 후 drift 방치** — 콘솔에서 리소스를 수동 변경하면 코드와 실제 상태가 불일치(drift)합니다. 이를 방치하면 다음 `apply` 시 예상치 못한 변경이 발생합니다.
- **상태 파일 로컬 저장** — `terraform.tfstate`를 로컬에 저장하면 팀 협업이 불가능하고, 파일 유실 시 인프라 관리가 불가능해집니다.
- **모듈화 없이 복사-붙여넣기** — 동일한 코드를 여러 환경에 복사하면 변경 시 모든 곳을 수동으로 수정해야 하며, 불일치가 발생합니다.
- **Azure에서 사용자 계정으로 IaC 실행** — 2025.10부터 Azure CLI/PowerShell/ARM API에 MFA가 강제됩니다. CI/CD 파이프라인이 `az login --identity`(Managed Identity) 또는 서비스 프린시펄 + Federated Credential을 사용하지 않으면 중단됩니다. 상세는 [IAM — Azure MFA 의무화](../../security/iam/)를 참고하세요.

## 체크리스트

- [ ] 원격 상태 저장소(S3+DynamoDB, Azure Storage, GCS 등)를 사용하고 있는가
- [ ] drift 탐지를 정기적으로 수행하고 있는가 (`terraform plan`, Config Rules 등)
- [ ] 공통 인프라를 모듈로 분리하여 재사용하고 있는가
- [ ] `plan` 결과를 코드 리뷰에서 확인하는 프로세스가 있는가

## 관련 문서

> 📄 [CI/CD](../../devops/cicd/)

> 📄 [클라우드 관리 도구 (콘솔, CLI, SDK)](../../about-cloud/console-cli-sdk/)

## 참고하기

### AWS

- [AWS CloudFormation 문서](https://docs.aws.amazon.com/ko_kr/cloudformation/)
- [AWS CDK 문서](https://docs.aws.amazon.com/ko_kr/cdk/)

### Azure

- [Bicep 문서](https://learn.microsoft.com/ko-kr/azure/azure-resource-manager/bicep/)
- [ARM Templates 문서](https://learn.microsoft.com/ko-kr/azure/azure-resource-manager/templates/)

### Google Cloud

- [Config Connector 문서](https://cloud.google.com/config-connector/docs)

### OCI

- [OCI Resource Manager 문서](https://docs.oracle.com/en-us/iaas/Content/ResourceManager/home.htm)
- [OCI Terraform Provider](https://registry.terraform.io/providers/oracle/oci/latest/docs)

### 멀티클라우드

- [Terraform 문서](https://developer.hashicorp.com/terraform/docs)
- [OpenTofu 문서](https://opentofu.org/docs/)
- [Pulumi 문서](https://www.pulumi.com/docs/)
