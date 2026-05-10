# 랜딩존

## 랜딩존이란

랜딩존(Landing Zone)은 멀티 계정 클라우드 환경을 안전하고 일관되게 운영하기 위한 기반 설정입니다. 일반적으로 다음 요소를 포함합니다:

- **네트워크**: 표준화된 VPC/VNet 구조, 허브-스포크 토폴로지, 연결 정책
- **보안**: 계정 간 보안 경계, 암호화 정책, 위협 탐지
- **로깅**: 중앙 집중식 로그 수집, 감사 추적, 규정 준수 증적
- **가드레일**: 예방적/탐지적 정책으로 조직 전체에 일관된 거버넌스 적용

랜딩존을 통해 새로운 워크로드 계정을 빠르고 안전하게 프로비저닝할 수 있으며, 조직의 보안·규정 준수 요구사항을 자동으로 적용할 수 있습니다.

## 4사 비교

| 항목 | AWS | Azure | GCP | OCI |
| --- | --- | --- | --- | --- |
| 서비스명 | [AWS Control Tower](https://aws.amazon.com/controltower/) | [Azure Landing Zone](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/) | [GCP Foundation Toolkit](https://cloud.google.com/foundation-toolkit) | [OCI Landing Zone](https://www.oracle.com/cloud/landing-zones/) |
| 계정 구조 | AWS Organizations + OU | Management Group + Subscription | Organization + Folder + Project | Tenancy + Compartment |
| 가드레일 | Controls (예방적/탐지적/사전 예방적) | Azure Policy + Blueprints | Organization Policy | CIS Benchmark 기반 정책 |
| 네트워크 기본 구조 | VPC + Transit Gateway | Hub-Spoke VNet + Azure Firewall | Shared VPC + Cloud Interconnect | Hub-Spoke VCN + DRG |
| IaC 제공 | AWS CloudFormation (기본 내장) | Bicep / Terraform 모듈 | Terraform 모듈 | Terraform 모듈 |
| 로깅 | AWS CloudTrail + Config | Activity Log + Defender for Cloud | Cloud Audit Logs + Security Command Center | Audit + Cloud Guard |

## 참고하기

| 벤더 | 공식 문서 |
| --- | --- |
| AWS | [AWS Control Tower 문서](https://docs.aws.amazon.com/controltower/), [AWS Organizations 문서](https://docs.aws.amazon.com/organizations/) |
| Azure | [Azure Landing Zone 아키텍처](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/), [Cloud Adoption Framework](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/) |
| GCP | [Foundation Toolkit 문서](https://cloud.google.com/foundation-toolkit/docs/overview), [Security Foundation Blueprint](https://cloud.google.com/architecture/security-foundations) |
| OCI | [OCI Landing Zone 문서](https://docs.oracle.com/en-us/iaas/Content/cloud-adoption-framework/landing-zone.htm), [CIS OCI Benchmark](https://www.oracle.com/security/cloud-security/cis-benchmarks/) |
