# IaC (Infrastructure as Code)

## 개요

콘솔에서 클릭으로 인프라를 만들면 빠르지만, 재현이 불가능하고 변경 이력을 추적할 수 없습니다. **IaC(Infrastructure as Code)**는 인프라를 코드로 정의하여, 버전 관리, 코드 리뷰, 자동 배포를 가능하게 합니다.

온프레미스에서 서버 설정을 문서로 관리하던 것을, 실행 가능한 코드로 대체하는 것입니다. 코드를 실행하면 동일한 인프라가 반복적으로 생성됩니다.

### 명령형 vs 선언형

- **명령형(Imperative)** — "이것을 만들어라, 저것을 삭제해라" 순서대로 실행. CLI 스크립트.
- **선언형(Declarative)** — "최종 상태는 이것이다"를 정의. 도구가 현재 상태와 비교하여 차이만 적용. IaC의 주류.

## 제품 비교

### 벤더 네이티브 IaC

| 벤더 | 제품 | 언어/형식 | 비고 |
| --- | --- | --- | --- |
| AWS | CloudFormation | YAML, JSON | AWS 전용. 스택 단위 관리 |
| AWS | CDK (Cloud Development Kit) | TypeScript, Python, Java, Go, C# | 프로그래밍 언어로 CloudFormation 생성 |
| Azure | Bicep | Bicep DSL | ARM Template의 간결한 대안 |
| Azure | ARM Templates | JSON | Azure 네이티브. 복잡하지만 완전한 기능 |
| GCP | Config Connector | Kubernetes YAML | K8s 리소스처럼 GCP 리소스 관리 |
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
| GCP | — (서비스별 개별 API) | Config Connector가 K8s API로 추상화하지만, 통합 CRUD API는 없음 |
| OCI | OCI Resource Manager API | Terraform State 관리 + 리소스 프로비저닝 API |

AWS Cloud Control API는 Terraform이 새 AWS 리소스를 지원할 때 개별 서비스 API 대신 Cloud Control API를 백엔드로 사용할 수 있어, 새 서비스 출시 시 IaC 지원이 빨라집니다.

## 핵심 차이점

**AWS CloudFormation / CDK** — AWS 서비스와 가장 빠르게 연동됩니다. 새 서비스 출시 시 CloudFormation 지원이 가장 먼저 나옵니다. CDK는 프로그래밍 언어의 조건문, 반복문, 추상화를 활용할 수 있어 대규모 인프라 관리에 유리합니다.

**Azure Bicep** — ARM Template의 복잡한 JSON을 간결한 DSL로 대체합니다. VS Code 확장으로 자동 완성과 검증을 제공합니다.

**Terraform** — 멀티클라우드 환경에서 사실상 표준입니다. 하나의 언어(HCL)로 AWS, Azure, GCP를 모두 관리할 수 있습니다. 상태 파일(State) 관리가 필요합니다.

## 참고하기

### AWS

- [AWS CloudFormation 문서](https://docs.aws.amazon.com/ko_kr/cloudformation/)
- [AWS CDK 문서](https://docs.aws.amazon.com/ko_kr/cdk/)

### Azure

- [Bicep 문서](https://learn.microsoft.com/ko-kr/azure/azure-resource-manager/bicep/)
- [ARM Templates 문서](https://learn.microsoft.com/ko-kr/azure/azure-resource-manager/templates/)

### GCP

- [Config Connector 문서](https://cloud.google.com/config-connector/docs)

### OCI

- [OCI Resource Manager 문서](https://docs.oracle.com/en-us/iaas/Content/ResourceManager/home.htm)
- [OCI Terraform Provider](https://registry.terraform.io/providers/oracle/oci/latest/docs)

### 멀티클라우드

- [Terraform 문서](https://developer.hashicorp.com/terraform/docs)
- [OpenTofu 문서](https://opentofu.org/docs/)
- [Pulumi 문서](https://www.pulumi.com/docs/)
