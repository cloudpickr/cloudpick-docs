---
description: 클라우드 보안의 접근 방식과 보호 영역을 구조화하여 보안 섹션의 읽기 가이드를 제공합니다.
---

# 클라우드 보안 시작하기

> 문서 기준: 2026년 5월

## 보안은 "무엇을 보호할지"부터

클라우드 보안의 첫 단계는 방화벽을 설정하는 것이 아닙니다. **자산 식별 → 위협 모델링 → 보호 우선순위** 순서로 접근해야 합니다.

1. **자산 식별** — 무엇을 보호할지 모르면 무엇을 막아야 할지도 모릅니다.
2. **데이터 분류** — 공개 / 내부 / 기밀 / 극비로 등급을 나누고, 각 등급에 맞는 보호 수준을 결정합니다.
3. **위협 모델링** — 누가, 어떤 경로로, 무엇을 노릴 수 있는지 식별합니다.
4. **보호 우선순위** — 가장 큰 영향을 줄 수 있는 위협부터 대응합니다.

## 클라우드 보안 관점의 전환

온프레미스와 클라우드는 보안 접근 방식이 다릅니다.

| 온프레미스 (전통) | 클라우드 (현대) |
| --- | --- |
| 경계 방어 (방화벽으로 막기) | 제로 트러스트 (모든 요청 검증) |
| 사전 차단 위주 | 사후 탐지 + 자동 대응 (감사 로그, 이상 탐지) |
| 수동 감사 (분기별) | 지속적 감사 (실시간 규정 준수) |
| 정적 정책 | 정책 as Code (OPA, SCP, Azure Policy) |
| 변경 통제 위원회 | 가드레일 + 자동 차단 (예방적 통제) |

{% hint style="info" %}
핵심 메시지: 먼저 무조건 차단하는 것이 아니라, **감사(Audit)로 확인하고, 정책(Policy)으로 막고, 탐지(Detection)로 잡는다**.
{% endhint %}

## 보호 영역 구조 — 보안 섹션 읽기 가이드

클라우드 보안은 여러 계층으로 구성됩니다. 각 계층에 해당하는 CloudPick 문서를 매핑합니다.

| 계층 | 역할 | CloudPick 문서 |
| --- | --- | --- |
| 거버넌스 & 정책 | 책임 범위, 규정 준수 | [공동 책임 모델](../about-cloud/shared-responsibility.md), [컴플라이언스](../governance/compliance.md) |
| 신원 & 접근 제어 | 누가 무엇을 할 수 있는지 | [IAM 심화](iam.md), [제로 트러스트](zero-trust.md) |
| 네트워크 보안 | 트래픽 격리와 필터링 | [VPC/서브넷](../networking/vpc-subnet.md) |
| 데이터 보호 | 암호화, 키 관리, DLP | [데이터 보호](data-protection.md), [시크릿 관리](secrets.md) |
| 탐지 & 대응 | 위협 탐지, 사고 대응 | [보안 태세 관리](security-posture.md), [사고 대응](incident-response.md) |
| DevSecOps | 파이프라인 보안 | [DevSecOps](../devops/devsecops.md) |
| AI 보안 | 모델/데이터 보호 | [AI 보안](ai-security.md) |

## 보안 성숙도 단계

한 번에 모든 것을 적용하려 하지 마세요. 단계적으로 성숙도를 높여갑니다.

| 단계 | 초점 | 예시 |
| --- | --- | --- |
| 1. 기본 | IAM 최소 권한, MFA, 암호화 기본 | 루트 계정 잠금, 기본 암호화 활성화 |
| 2. 가시성 | 로깅, 감사, 자산 인벤토리 | CloudTrail, Config, 보안 허브 활성화 |
| 3. 자동화 | 정책 as Code, 자동 탐지/차단 | SCP, GuardDuty, 자동 격리 |
| 4. 지속적 | 레드팀, 카오스 보안, 위협 인텔리전스 | 침투 테스트, 위협 모델링 정기화 |

## 참고하기

- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [AWS Security Best Practices](https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html)
- [Azure Security Documentation](https://learn.microsoft.com/azure/security/)
- [Google Cloud Security Best Practices](https://cloud.google.com/security/best-practices)
- [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks)
