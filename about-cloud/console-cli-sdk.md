# 콘솔, CLI, SDK

## 클라우드를 다루는 세 가지 방법

온프레미스 환경에서 서버를 관리하는 방법을 떠올려 보겠습니다. 서버실에 직접 가서 모니터와 키보드로 작업하거나, SSH로 원격 접속하거나, 자동화 스크립트를 통해 API를 호출할 수 있습니다. 클라우드에서도 동일한 세 가지 접근 방식이 있습니다.

- **콘솔(웹 UI)** — 서버실에 직접 가서 작업하는 것과 비슷합니다. 시각적으로 리소스를 확인하고 관리할 수 있어, 처음 배울 때나 현황을 파악할 때 유용합니다.
- **CLI(Command Line Interface)** — SSH로 원격 접속하여 명령어로 작업하는 것과 비슷합니다. 반복 작업을 스크립트로 자동화할 수 있어, 운영 업무에 적합합니다.
- **SDK(Software Development Kit)** — 애플리케이션 코드에서 API를 호출하는 것과 비슷합니다. 프로그래밍 언어로 클라우드 리소스를 제어할 수 있어, 애플리케이션 통합에 적합합니다.

실무에서는 이 세 가지를 상황에 따라 혼합하여 사용합니다. 콘솔로 현황을 확인하고, CLI로 반복 작업을 자동화하고, SDK로 애플리케이션에 클라우드 서비스를 통합하는 것이 일반적입니다.

## 콘솔 (웹 UI)

각 벤더는 웹 브라우저에서 클라우드 리소스를 관리할 수 있는 콘솔을 제공합니다.

| 항목 | AWS | Azure | GCP | OCI |
| --- | --- | --- | --- | --- |
| **이름** | AWS Management Console | Azure Portal | Google Cloud Console | OCI Console |
| **URL** | [console.aws.amazon.com](https://console.aws.amazon.com) | [portal.azure.com](https://portal.azure.com) | [console.cloud.google.com](https://console.cloud.google.com) | [cloud.oracle.com](https://cloud.oracle.com) |
| **한국어 지원** | 지원 | 지원 | 부분 지원 | 부분 지원 |
| **모바일 앱** | AWS Console Mobile App | Azure Mobile App | Google Cloud App | OCI Mobile App |
| **특징** | 서비스별 독립 콘솔, 리전 선택 필수 | 통합 대시보드, 리소스 그룹 중심 | 프로젝트 중심, 검색 강점 | Compartment 중심, 깔끔한 UI |

### 콘솔 사용 시 주의사항

- **리전 확인** — AWS와 GCP는 콘솔에서 리전을 명시적으로 선택해야 합니다. 잘못된 리전에서 리소스를 생성하는 실수가 흔합니다.
- **프로덕션 변경 자제** — 콘솔에서의 수동 변경은 추적이 어렵고 재현이 불가능합니다. 프로덕션 환경은 CLI나 IaC로 관리하는 것을 권장합니다.

## CLI (Command Line Interface)

각 벤더는 터미널에서 클라우드 리소스를 관리할 수 있는 CLI 도구를 제공합니다.

| 항목 | AWS | Azure | GCP | OCI |
| --- | --- | --- | --- | --- |
| **CLI 이름** | AWS CLI | Azure CLI (`az`) | Google Cloud CLI (`gcloud`) | OCI CLI (`oci`) |
| **추가 CLI** | — | Azure PowerShell | — | — |
| **설치** | [설치 가이드](https://docs.aws.amazon.com/ko_kr/cli/latest/userguide/getting-started-install.html) | [설치 가이드](https://learn.microsoft.com/ko-kr/cli/azure/install-azure-cli) | [설치 가이드](https://cloud.google.com/sdk/docs/install) | [설치 가이드](https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/cliinstall.htm) |
| **인증** | `aws login` (브라우저 인증, CLI v2.32+) | `az login` (브라우저 인증) | `gcloud auth login` (브라우저 인증) | `oci session authenticate` (브라우저 인증) |
| **출력 형식** | JSON, YAML, Table, Text | JSON, YAML, Table, TSV | JSON, YAML, Table, CSV | JSON, Table |

### 기본 사용 예시

```bash
# AWS — EC2 인스턴스 목록 조회
aws ec2 describe-instances --region ap-northeast-2

# Azure — VM 목록 조회
az vm list --resource-group my-rg --output table

# GCP — Compute Engine 인스턴스 목록 조회
gcloud compute instances list --project my-project

# OCI — Compute 인스턴스 목록 조회
oci compute instance list --compartment-id <compartment-ocid>
```

Azure는 CLI 외에 **Azure PowerShell**도 제공합니다. Windows 환경에서 PowerShell을 주로 사용하는 조직이라면 Azure PowerShell이 더 익숙할 수 있습니다.

## SDK (Software Development Kit)

각 벤더는 주요 프로그래밍 언어용 SDK를 제공하여, 애플리케이션 코드에서 직접 클라우드 서비스를 호출할 수 있습니다.

| 언어 | AWS | Azure | GCP | OCI |
| --- | --- | --- | --- | --- |
| **Python** | Boto3 | azure-sdk-for-python | google-cloud-python | oci-python-sdk |
| **JavaScript/TypeScript** | AWS SDK for JavaScript | azure-sdk-for-js | google-cloud-node | oci-typescript-sdk |
| **Java** | AWS SDK for Java | azure-sdk-for-java | google-cloud-java | oci-java-sdk |
| **Go** | AWS SDK for Go | azure-sdk-for-go | google-cloud-go | oci-go-sdk |
| **.NET (C#)** | AWS SDK for .NET | Azure SDK for .NET | Google Cloud .NET | oci-dotnet-sdk |
| **설치 문서** | [AWS SDK 가이드](https://docs.aws.amazon.com/ko_kr/sdkref/latest/guide/overview.html) | [Azure SDK 가이드](https://learn.microsoft.com/ko-kr/azure/developer/) | [Cloud Client Libraries](https://cloud.google.com/apis/docs/cloud-client-libraries) | [OCI SDK 가이드](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/sdks.htm) |

SDK는 CLI와 달리 애플리케이션 코드에 직접 통합되므로, 에러 처리, 재시도 로직, 비동기 호출 등을 프로그래밍 언어의 기능을 활용하여 구현할 수 있습니다.

## Cloud Shell

각 벤더 모두 브라우저에서 바로 CLI를 사용할 수 있는 **Cloud Shell**을 제공합니다. 별도의 설치 없이 웹 브라우저만으로 CLI 작업이 가능하여, 빠른 테스트나 긴급 대응 시 유용합니다.

| 항목 | AWS | Azure | GCP | OCI |
| --- | --- | --- | --- | --- |
| **이름** | AWS CloudShell | Azure Cloud Shell | Google Cloud Shell | OCI Cloud Shell |
| **사전 설치 도구** | AWS CLI, Python, Node.js, Git 등 | Azure CLI, PowerShell, Terraform 등 | gcloud, kubectl, Terraform, Python 등 | OCI CLI, Python, Terraform 등 |
| **스토리지** | 리전당 1GB | 5GB (Azure Files) | 5GB (홈 디렉토리) | 5GB (홈 디렉토리) |
| **비용** | 무료 | 무료 (스토리지 비용 별도) | 무료 | 무료 |
| **에디터** | 내장 에디터 | Monaco 에디터 (VS Code 기반) | Theia 에디터 (VS Code 기반) | 내장 에디터 |

## IaC (Infrastructure as Code)와의 관계

콘솔, CLI, SDK는 리소스를 직접 생성하고 관리하는 **명령형(Imperative)** 방식입니다. 이와 대비되는 **선언형(Declarative)** 방식이 **IaC(Infrastructure as Code)**입니다. IaC는 인프라의 원하는 상태를 코드로 정의하고, 도구가 현재 상태와 비교하여 자동으로 변경을 적용합니다.

### 벤더 네이티브 IaC 도구

| 벤더 | 도구 | 언어/형식 |
| --- | --- | --- |
| **AWS** | CloudFormation | YAML, JSON |
| **AWS** | CDK (Cloud Development Kit) | TypeScript, Python, Java, C#, Go |
| **Azure** | Bicep | Bicep (DSL) |
| **Azure** | ARM Templates | JSON |
| **GCP** | Config Connector | Kubernetes YAML |
| **GCP** | Deployment Manager | YAML, Jinja2, Python |

### 멀티클라우드 IaC 도구

여러 벤더를 동시에 관리해야 하는 멀티클라우드 환경에서는 벤더 중립적인 IaC 도구가 유용합니다.

- **[Terraform](https://www.terraform.io/)** — HashiCorp이 개발한 가장 널리 사용되는 멀티클라우드 IaC 도구입니다. HCL(HashiCorp Configuration Language)로 인프라를 정의합니다.
- **[Pulumi](https://www.pulumi.com/)** — TypeScript, Python, Go 등 일반 프로그래밍 언어로 인프라를 정의할 수 있습니다.
- **[OpenTofu](https://opentofu.org/)** — Terraform의 오픈소스 포크로, Linux Foundation에서 관리합니다.

## 참고하기

### AWS

- [AWS CLI 설치 가이드](https://docs.aws.amazon.com/ko_kr/cli/latest/userguide/getting-started-install.html)
- [AWS SDK 설치 (언어별)](https://docs.aws.amazon.com/ko_kr/sdkref/latest/guide/overview.html)
- [AWS CloudShell 문서](https://docs.aws.amazon.com/ko_kr/cloudshell/latest/userguide/)
- [AWS CloudFormation 문서](https://docs.aws.amazon.com/ko_kr/cloudformation/)

### Azure

- [Azure CLI 설치 가이드](https://learn.microsoft.com/ko-kr/cli/azure/install-azure-cli)
- [Azure SDK 설치 (언어별)](https://learn.microsoft.com/ko-kr/azure/developer/)
- [Azure Cloud Shell 문서](https://learn.microsoft.com/ko-kr/azure/cloud-shell/overview)
- [Bicep 설치 가이드](https://learn.microsoft.com/ko-kr/azure/azure-resource-manager/bicep/install)

### GCP

- [Google Cloud CLI 설치 가이드](https://cloud.google.com/sdk/docs/install)
- [Google Cloud Client Libraries (언어별)](https://cloud.google.com/apis/docs/cloud-client-libraries)
- [Google Cloud Shell 문서](https://cloud.google.com/shell/docs)
- [Terraform on Google Cloud](https://cloud.google.com/docs/terraform)

### OCI

- [OCI CLI 설치 가이드](https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/cliinstall.htm)
- [OCI SDK](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/sdks.htm)
- [OCI Cloud Shell](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/cloudshellintro.htm)
- [Terraform on OCI](https://docs.oracle.com/en-us/iaas/Content/dev/terraform.htm)
