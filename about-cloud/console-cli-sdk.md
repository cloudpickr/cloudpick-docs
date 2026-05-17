---
description: 콘솔, CLI, SDK, Cloud Shell의 역할과 IaC와의 관계를 벤더별로 비교합니다.
---

# 클라우드 관리 도구 (콘솔, CLI, SDK)

> 문서 기준: 2026년 5월

## 클라우드를 다루는 세 가지 방법

온프레미스 환경에서 서버를 관리하는 방법을 떠올려 보겠습니다. 서버실에 직접 가서 모니터와 키보드로 작업하거나, SSH로 원격 접속하거나, 자동화 스크립트를 통해 API를 호출할 수 있습니다. 클라우드에서도 동일한 세 가지 접근 방식이 있습니다.

- **콘솔(웹 UI)** — 서버실에 직접 가서 작업하는 것과 비슷합니다. 시각적으로 리소스를 확인하고 관리할 수 있어, 처음 배울 때나 현황을 파악할 때 유용합니다.
- **CLI(Command Line Interface)** — SSH로 원격 접속하여 명령어로 작업하는 것과 비슷합니다. 반복 작업을 스크립트로 자동화할 수 있어, 운영 업무에 적합합니다.
- **SDK(Software Development Kit)** — 애플리케이션 코드에서 API를 호출하는 것과 비슷합니다. 프로그래밍 언어로 클라우드 리소스를 제어할 수 있어, 애플리케이션 통합에 적합합니다.

실무에서는 이 세 가지를 상황에 따라 혼합하여 사용합니다. 콘솔로 현황을 확인하고, CLI로 반복 작업을 자동화하고, SDK로 애플리케이션에 클라우드 서비스를 통합하는 것이 일반적입니다.

## 콘솔 (웹 UI)

각 벤더는 웹 브라우저에서 클라우드 리소스를 관리할 수 있는 콘솔을 제공합니다.

| 항목 | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- |
| **이름** | AWS Management Console | Azure Portal | Google Cloud Console | OCI Console |
| **URL** | [console.aws.amazon.com](https://console.aws.amazon.com) | [portal.azure.com](https://portal.azure.com) | [console.cloud.google.com](https://console.cloud.google.com) | [cloud.oracle.com](https://cloud.oracle.com) |
| **한국어 지원** | 지원 | 지원 | 부분 지원 | 부분 지원 |
| **모바일 앱** | AWS Console Mobile App | Azure Mobile App | Google Cloud App | OCI Mobile App |
| **특징** | 서비스별 독립 콘솔, 리전 선택 필수 | 통합 대시보드, 리소스 그룹 중심 | 프로젝트 중심, 검색 강점 | Compartment 중심, 깔끔한 UI |

### 콘솔 사용 시 주의사항

- **리전 확인** — AWS와 Google Cloud는 콘솔에서 리전을 명시적으로 선택해야 합니다. 잘못된 리전에서 리소스를 생성하는 실수가 흔합니다.
- **프로덕션 변경 자제** — 콘솔에서의 수동 변경은 추적이 어렵고 재현이 불가능합니다. 프로덕션 환경은 CLI나 IaC로 관리하는 것을 권장합니다.

{% hint style="warning" %}
콘솔로 프로덕션 환경을 직접 변경하면 변경 이력이 남지 않고 재현이 불가능합니다. **IaC 파이프라인을 통한 변경**을 원칙으로 하고, 콘솔은 현황 조회와 긴급 대응에만 사용하세요.
{% endhint %}

## CLI (Command Line Interface)

각 벤더는 터미널에서 클라우드 리소스를 관리할 수 있는 CLI 도구를 제공합니다.

| 항목 | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- |
| **CLI 이름** | AWS CLI (`aws`) | Azure CLI (`az`) | Google Cloud CLI (`gcloud`) | OCI CLI (`oci`) |
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

# Google Cloud — Compute Engine 인스턴스 목록 조회
gcloud compute instances list --project my-project

# OCI — Compute 인스턴스 목록 조회
oci compute instance list --compartment-id <compartment-ocid>
```

Azure는 CLI 외에 **Azure PowerShell**도 제공합니다. Windows 환경에서 PowerShell을 주로 사용하는 조직이라면 Azure PowerShell이 더 익숙할 수 있습니다.

## SDK (Software Development Kit)

각 벤더는 주요 프로그래밍 언어용 SDK를 제공하여, 애플리케이션 코드에서 직접 클라우드 서비스를 호출할 수 있습니다.

| 언어 | AWS | Azure | Google Cloud | OCI |
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

| 항목 | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- |
| **이름** | AWS CloudShell | Azure Cloud Shell | Google Cloud Shell | OCI Cloud Shell |
| **사전 설치 도구** | AWS CLI, Python, Node.js, Git 등 | Azure CLI, PowerShell, Terraform 등 | gcloud, kubectl, Terraform, Python 등 | OCI CLI, Python, Terraform 등 |
| **스토리지** | 리전당 1GB | 5GB (Azure Files) | 5GB (홈 디렉토리) | 5GB (홈 디렉토리) |
| **비용** | 무료 | 무료 (스토리지 비용 별도) | 무료 | 무료 |
| **에디터** | 내장 에디터 | Monaco 에디터 (VS Code 기반) | Theia 에디터 (VS Code 기반) | 내장 에디터 |

## 코드로 관리하는 인프라 (IaC)와의 관계

콘솔, CLI, SDK는 리소스를 직접 생성하고 관리하는 **명령형** (Imperative) 방식입니다. "서버를 만들어라", "네트워크를 연결해라"처럼 한 단계씩 지시합니다.

이와 대비되는 **선언형** (Declarative) 방식이 **IaC**입니다. "서버 3대, 네트워크 1개가 있어야 한다"처럼 원하는 최종 상태만 정의하면, 도구가 현재 상태와 비교하여 필요한 변경을 자동으로 적용합니다.

| 방식 | 특징 | 도구 예시 |
| --- | --- | --- |
| **명령형** | 순서대로 실행. 빠른 테스트, 긴급 대응에 적합 | CLI 스크립트, SDK 코드 |
| **선언형** | 최종 상태 정의. 재현성, 버전 관리, 팀 협업에 적합 | Terraform, CloudFormation, Bicep, CDK |

실무에서는 콘솔로 현황을 확인하고, CLI로 긴급 대응하며, **프로덕션 인프라는 IaC로 관리**하는 것이 표준입니다.

{% hint style="info" %}
IaC 도구 비교, Terraform 상태 관리, 모듈 설계, 드리프트 관리 등 상세는 [코드로 관리하는 인프라 (IaC)](../devops/iac.md)를 참고하세요.
{% endhint %}

## 자주 하는 실수

- **"콘솔에서 만들면 끝이다"** — 콘솔로 생성한 리소스는 이력이 남지 않아 재현과 감사가 불가능합니다. 프로덕션은 IaC로 관리해야 합니다.
- **"CLI와 SDK는 같은 것이다"** — CLI는 터미널에서 단발성 명령을 실행하는 도구이고, SDK는 애플리케이션 코드에 통합하는 라이브러리입니다. 용도가 다릅니다.
- **"Cloud Shell이면 로컬 설치가 필요 없다"** — Cloud Shell은 임시 환경이며 세션 종료 시 상태가 초기화될 수 있습니다. 지속적인 운영에는 로컬 CLI 설치가 필요합니다.

## 체크리스트

- [ ] CLI 인증을 장기 자격 증명(Access Key) 대신 브라우저 기반 임시 인증으로 설정했는가?
- [ ] 프로덕션 환경 변경은 콘솔이 아닌 IaC 파이프라인을 통해 수행하는 원칙을 수립했는가?
- [ ] 사용할 벤더의 CLI를 설치하고 기본 명령어(리소스 조회)를 실행해 보았는가?

## 참고하기

### AWS

- [AWS CLI 설치 가이드](https://docs.aws.amazon.com/ko_kr/cli/latest/userguide/getting-started-install.html)
- [AWS SDK 설치 (언어별)](https://docs.aws.amazon.com/ko_kr/sdkref/latest/guide/overview.html)
- [AWS CloudShell 문서](https://docs.aws.amazon.com/ko_kr/cloudshell/latest/userguide/)

### Azure

- [Azure CLI 설치 가이드](https://learn.microsoft.com/ko-kr/cli/azure/install-azure-cli)
- [Azure SDK 설치 (언어별)](https://learn.microsoft.com/ko-kr/azure/developer/)
- [Azure Cloud Shell 문서](https://learn.microsoft.com/ko-kr/azure/cloud-shell/overview)

### Google Cloud

- [Google Cloud CLI 설치 가이드](https://cloud.google.com/sdk/docs/install)
- [Google Cloud Client Libraries (언어별)](https://cloud.google.com/apis/docs/cloud-client-libraries)
- [Google Cloud Shell 문서](https://cloud.google.com/shell/docs)

### OCI

- [OCI CLI 설치 가이드](https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/cliinstall.htm)
- [OCI SDK](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/sdks.htm)
- [OCI Cloud Shell](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/cloudshellintro.htm)
