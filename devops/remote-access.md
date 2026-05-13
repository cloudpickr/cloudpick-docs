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

### 접근 빈도와 운영 성숙도

인스턴스에 직접 접근(쉘 로그인)하는 빈도는 운영 성숙도의 지표입니다. 접근이 잦을수록 자동화가 부족하다는 신호입니다.

| 성숙도 단계 | 쉘 접근 빈도 | 특징 |
| --- | --- | --- |
| **Level 1 — 수동 운영** | 매일, 수시 | 로그 확인·설정 변경·배포를 수동으로 수행. 서버에 상주하는 패턴 |
| **Level 2 — 부분 자동화** | 주 수회 | CI/CD로 배포 자동화, 모니터링 대시보드 구축. 장애 시에만 접근 |
| **Level 3 — 관찰가능성 기반** | 월 수회 | 로그/메트릭/트레이스가 중앙화되어 대부분 콘솔에서 해결. 예외적 디버깅만 접근 |
| **Level 4 — Immutable/Serverless** | 거의 없음 | 인스턴스 교체로 문제 해결. 쉘 접근 자체가 보안 이벤트로 간주 |

쉘 접근을 줄이려면 다음을 자동화해야 합니다 (목표: Level 3 이상):

| 쉘에서 하던 일 | 대체 방법 |
| --- | --- |
| 로그 확인 (`tail -f`) | [모니터링](monitoring.md) 중앙화 (CloudWatch Logs / Azure Monitor / Cloud Logging) |
| 설정 파일 수정 | [구성 관리 서비스](../security/secrets.md#구성프로퍼티-관리-configuration-management) (Parameter Store, App Configuration) + 동적 리로드 |
| 패키지 설치/업데이트 | [Patch Manager](patch-and-vulnerability.md) + 골든 이미지 파이프라인 |
| 서비스 재시작 | Run Command 또는 Auto Scaling 인스턴스 교체 |
| 디스크 정리 | CloudWatch Agent 알림 + 자동 스크립트 (EventBridge → Lambda) |
| 디버깅 (strace, tcpdump) | [관찰가능성](observability.md) 도구로 대부분 해결. 불가피한 경우만 세션 접근 |

{% hint style="info" %}
**"서버에 들어가야 할 일이 생기면, 그것을 자동화할 기회"** 로 보세요. 접근 로그를 주기적으로 리뷰하여 반복되는 접근 사유를 파악하고, 해당 작업을 자동화하면 접근 빈도가 자연스럽게 줄어듭니다.
{% endhint %}

### 접근 제어 정책 설계

쉘 접근을 완전히 없앨 수는 없으므로, **누가, 언제, 어떤 조건에서** 접근할 수 있는지 정책을 설계합니다.

| 정책 항목 | 권장 |
| --- | --- |
| **상시 접근 권한** | 부여하지 않음. Just-In-Time (JIT) 방식으로 필요 시 요청 → 승인 → 시간 제한 부여 |
| **프로덕션 접근** | 최소 2인 승인 (Dual Control). 세션 녹화 필수 |
| **개발/테스트 접근** | 팀 단위 자율, 단 로그 기록 |
| **비상 접근 (Break-glass)** | 사전 정의된 긴급 역할. 사후 감사 필수. 24시간 내 사유 기록 |
| **접근 리뷰** | 월 1회 접근 로그 리뷰. 불필요한 접근 패턴 식별 → 자동화 |

**JIT 접근 구현 예시:**

- **AWS** — IAM Identity Center + Permission Set (시간 제한) 또는 SSM Session Manager + Approval Workflow
- **Azure** — Privileged Identity Management (PIM) — 역할 활성화 시 승인 + TTL
- **GCP** — PAM (Privileged Access Manager) — Just-In-Time 접근 요청/승인
- **OCI** — OCI Bastion 세션 TTL (최대 3시간) + IAM 동적 그룹

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

### 세션 로깅과 감사 추적

쉘 접근은 **누가, 언제, 어떤 인스턴스에서, 무엇을 실행했는지** 기록해야 합니다. 감사 대응과 사고 분석의 핵심 증거입니다.

**두 가지 레이어의 로그가 필요합니다:**

1. **API/관리 레이어** — "세션을 시작/종료한 행위" 자체의 기록 (누가, 언제, 어디에)
2. **세션 레이어** — "세션 안에서 실행한 명령과 출력" 기록 (무엇을 했는지)

| 벤더 | API/관리 로그 | 세션 내용 로그 | 저장 위치 |
| --- | --- | --- | --- |
| AWS | **CloudTrail** (`StartSession`, `TerminateSession`, `SendCommand`) | Session Manager 세션 로깅 (명령 입출력 스트림) | CloudTrail → S3, 세션 로그 → S3/CloudWatch Logs |
| Azure | **Activity Log** (Bastion 연결 이벤트) | Bastion 진단 로그 (연결 메타데이터) | Log Analytics Workspace |
| GCP | **Cloud Audit Logs** (IAP 터널 생성/종료) | OS Login 감사 로그 (메타데이터만, 명령 내용 미기록) | Cloud Logging |
| OCI | **Audit Log** (Bastion 세션 생성/만료) | OCI Logging (세션 메타데이터) | OCI Logging / Object Storage |

**CloudTrail 연계 (AWS 예시):**

CloudTrail은 세션 접근의 "관리 행위"를 자동으로 기록합니다:

- `StartSession` — 누가 어떤 인스턴스에 세션을 열었는지 (사용자 ARN, 인스턴스 ID, 시간)
- `TerminateSession` — 세션 종료 시점
- `SendCommand` (Run Command) — 원격 명령 실행 기록 (명령 내용 포함)
- 이 이벤트들은 [보안 태세 관리](../security/security-posture.md)의 GuardDuty/Security Hub와 연동하여 비정상 패턴을 자동 탐지할 수 있습니다

**로깅 설정 체크리스트:**

- [ ] API 감사 로그 활성화 확인 (CloudTrail/Activity Log/Audit Logs — 대부분 기본 활성)
- [ ] 세션 내용 로깅 활성화 (AWS: Session Manager Preferences에서 S3/CloudWatch 설정)
- [ ] 명령 입출력 기록 활성화 (AWS는 기본 비활성, 명시적으로 켜야 함)
- [ ] 로그 보존 기간 설정 (규정 준수 요건에 따라 1년\~7년)
- [ ] 로그 암호화 (KMS/Key Vault로 저장 시 암호화)
- [ ] 로그 변조 방지 (S3 Object Lock, Immutable Storage 등)
- [ ] SIEM 연동 (이상 패턴 탐지: 비정상 시간대 접근, 대량 명령 실행, 미승인 인스턴스 접근)

{% hint style="warning" %}
**AWS Session Manager는 기본적으로 명령 입출력을 기록하지 않습니다.** Session Manager Preferences에서 S3 또는 CloudWatch Logs로의 로깅을 명시적으로 활성화해야 합니다. 활성화하지 않으면 CloudTrail에 "누가 접속했는지"만 남고 "무엇을 했는지"는 남지 않습니다.
{% endhint %}

## 참고하기

- [AWS Systems Manager Session Manager 문서](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager.html)
- [Azure Bastion 문서](https://learn.microsoft.com/azure/bastion/bastion-overview)
- [GCP IAP TCP 포워딩 문서](https://cloud.google.com/iap/docs/using-tcp-forwarding)
- [OCI Bastion 문서](https://docs.oracle.com/en-us/iaas/Content/Bastion/home.htm)
- [AWS Run Command](https://docs.aws.amazon.com/systems-manager/latest/userguide/execute-remote-commands.html)
- [Azure Run Command](https://learn.microsoft.com/azure/virtual-machines/run-command-overview)
