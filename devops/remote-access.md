---
description: SSH/RDP 없이 안전하게 인스턴스에 접근하는 관리형 서비스를 벤더별로 비교합니다.
---

# 원격 접근 관리

> 문서 기준: 2026년 5월

## 개요

서버에 접근할 때 전통적으로 SSH(Linux)나 RDP(Windows)를 사용합니다. 하지만 퍼블릭 IP 노출, SSH 키 관리, 보안 그룹 개방 등의 문제가 있습니다.

클라우드 벤더는 **에이전트 기반 또는 프록시 기반**의 관리형 접근 서비스를 제공하여, 퍼블릭 IP 없이도 프라이빗 서브넷의 인스턴스에 안전하게 접근할 수 있게 합니다.

## 전통적 접근 vs 관리형 접근

| 항목 | 전통적 (SSH/RDP 직접) | 관리형 서비스 |
| --- | --- | --- |
| **퍼블릭 IP** | 필요 (또는 Bastion Host 별도 운영) | 불필요 |
| **포트 개방** | 22/3389 인바운드 허용 필요 | 인바운드 규칙 불필요 |
| **키 관리** | SSH 키 배포/교체 직접 관리 | IAM 기반 인증 (키 불필요) |
| **감사 로그** | 별도 구성 필요 | 세션 로그 자동 기록 |
| **네트워크 경로** | 인터넷 → 인스턴스 | 벤더 내부 채널 (아웃바운드만) |

## 벤더별 서비스 비교

| 항목 | AWS | Azure | GCP | OCI |
| --- | --- | --- | --- | --- |
| **서비스명** | [Systems Manager Session Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager.html) | [Azure Bastion](https://learn.microsoft.com/azure/bastion/bastion-overview) | [Identity-Aware Proxy (IAP)](https://cloud.google.com/iap/docs/using-tcp-forwarding) | [OCI Bastion](https://docs.oracle.com/en-us/iaas/Content/Bastion/home.htm) |
| **방식** | 에이전트 기반 (SSM Agent) | 프록시 기반 (PaaS) | 프록시 기반 (TCP 포워딩) | 프록시 기반 (관리형 Bastion) |
| **퍼블릭 IP 필요** | 불필요 | 불필요 | 불필요 | 불필요 |
| **인바운드 포트** | 불필요 (아웃바운드 443만) | 불필요 | 불필요 | 불필요 |
| **인증** | IAM 정책 | Entra ID + RBAC | IAM + IAP 정책 | IAM 정책 |
| **세션 로그** | S3/CloudWatch Logs | Azure Monitor | Cloud Audit Logs | OCI Logging |
| **파일 전송** | 지원 (S3 경유 또는 포트 포워딩) | 네이티브 파일 업로드 | SCP over IAP 터널 | SSH 터널 경유 |
| **비용** | 무료 (SSM Agent 기본 포함) | SKU별 시간 과금 | 무료 (IAP 자체) | 무료 (세션 단위) |

## 핵심 차이점

**AWS Systems Manager Session Manager** — EC2에 기본 설치된 SSM Agent를 통해 동작합니다. 별도 인프라 배포 없이 IAM 권한만으로 즉시 사용 가능하며, 추가 비용이 없습니다. 포트 포워딩으로 RDS 등 다른 리소스에도 터널링할 수 있습니다.

**Azure Bastion** — VNet에 배포하는 PaaS 서비스로, 브라우저(Azure Portal)에서 직접 SSH/RDP 세션을 열 수 있습니다. 별도 클라이언트 설치가 불필요하지만, Bastion 호스트 자체에 시간 과금이 발생합니다.

**GCP Identity-Aware Proxy (IAP)** — Google의 제로 트러스트 접근 모델의 일부입니다. TCP 포워딩을 통해 SSH/RDP뿐 아니라 임의 포트에 대한 터널을 생성할 수 있습니다. 웹 애플리케이션 접근 제어에도 동일한 IAP를 사용합니다.

**OCI Bastion** — 관리형 Bastion 서비스로, 세션 생성 시 TTL(최대 3시간)을 지정합니다. 세션 만료 후 자동 정리되어 장기 접근 경로가 남지 않습니다.

## 실무 권장 사항

### 접근 방식 선택 기준

| 상황 | 권장 |
| --- | --- |
| 일상적 운영 (로그 확인, 설정 변경) | 관리형 서비스 사용 |
| 긴급 장애 대응 | 관리형 서비스 + 사전 권한 설정 (break-glass) |
| 대량 서버 명령 실행 | AWS Run Command / Azure Run Command / GCP OS Config |
| 개발/테스트 환경 임시 접근 | IAP 터널 또는 Session Manager 포트 포워딩 |
| 규정상 SSH 키 사용 필수 | OCI Bastion (SSH 키 기반 세션) |

### 보안 강화 팁

- **MFA 강제** — 세션 시작 시 MFA를 요구하도록 IAM 정책 설정
- **세션 시간 제한** — 유휴 타임아웃과 최대 세션 시간 설정
- **로그 중앙화** — 모든 세션 로그를 SIEM으로 전송하여 이상 접근 탐지
- **최소 권한** — 특정 인스턴스/태그에만 접근 가능하도록 정책 범위 제한
- **네트워크 분리** — 관리형 서비스를 사용하더라도 프라이빗 서브넷 유지

## 참고하기

- [AWS Systems Manager Session Manager 문서](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager.html)
- [Azure Bastion 문서](https://learn.microsoft.com/azure/bastion/bastion-overview)
- [GCP IAP TCP 포워딩 문서](https://cloud.google.com/iap/docs/using-tcp-forwarding)
- [OCI Bastion 문서](https://docs.oracle.com/en-us/iaas/Content/Bastion/home.htm)
- [AWS Run Command](https://docs.aws.amazon.com/systems-manager/latest/userguide/execute-remote-commands.html)
- [Azure Run Command](https://learn.microsoft.com/azure/virtual-machines/run-command-overview)
