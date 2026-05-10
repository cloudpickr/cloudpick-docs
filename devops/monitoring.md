---
description: 메트릭/로그/트레이스, APM, SLO 모니터링, 알림 운영 원칙을 벤더별로 비교합니다.
---

# 모니터링

> 문서 기준: 2026년 5월

## 개요

온프레미스에서는 Nagios, Zabbix 같은 도구를 설치하여 서버 상태를 모니터링합니다. 클라우드에서는 벤더가 관리형 모니터링 서비스를 제공하여, 에이전트 설치와 서버 운영 없이 메트릭, 로그, 트레이스를 수집하고 알림을 설정할 수 있습니다.

### 왜 모니터링이 중요한가

- **장애 탐지** — 서버 다운, 응답 지연, 에러율 급증을 빠르게 감지합니다.
- **원인 분석** — "느리다"는 증상에서 "어떤 서비스의 어떤 쿼리가 느린지"까지 추적합니다.
- **용량 계획** — 트래픽 추이를 보고 스케일링 시점을 판단합니다.
- **비즈니스 의사결정** — 배포 후 전환율, 에러율 변화를 확인하여 롤백 여부를 결정합니다.

### 관측 가능성(Observability)의 세 기둥

- **메트릭** (Metrics) — CPU, 메모리, 요청 수 등 수치 데이터. 대시보드와 알림에 사용.
- **로그** (Logs) — 애플리케이션/시스템이 출력하는 텍스트 기록. 문제 원인 분석에 사용.
- **트레이스** (Traces) — 분산 시스템에서 요청이 거치는 경로 추적. 병목 구간 식별에 사용.

이 세 가지를 **상관관계** (Correlation)로 연결하는 것이 핵심입니다. "에러율이 올랐다"(메트릭) → "어떤 요청에서?"(트레이스) → "구체적으로 무슨 에러?"(로그)를 하나의 흐름으로 추적할 수 있어야 합니다.

### APM (Application Performance Monitoring)

인프라 메트릭(CPU, 메모리)만으로는 "왜 느린지"를 알 수 없습니다. **APM**은 애플리케이션 코드 수준에서 응답 시간, DB 쿼리 시간, 외부 API 호출 시간을 측정하여 병목을 찾아줍니다.

| 벤더 | 제품 | 비고 |
| --- | --- | --- |
| AWS | X-Ray + CloudWatch Application Signals | 서비스 맵 + SLO 모니터링 |
| Azure | Application Insights | 자동 계측. 성능 이상 자동 탐지 |
| GCP | Cloud Trace + Cloud Profiler | 트레이싱 + 코드 레벨 프로파일링 |
| OCI | OCI Application Performance Monitoring | 분산 트레이싱 + 합성 모니터링 |
| 3rd party | Datadog, New Relic, Dynatrace | 멀티클라우드 APM. 풍부한 자동 계측 |

### 왜 여럿이 함께 봐야 하는가

모니터링은 운영팀만의 도구가 아닙니다.

- **개발자** — 배포 후 에러율/지연 변화를 직접 확인. 코드 문제를 빠르게 파악.
- **운영/SRE** — 인프라 상태, 용량, SLO 준수 여부 모니터링.
- **제품/비즈니스** — 전환율, 사용자 경험 지표 확인.

같은 대시보드를 공유하면 "느리다"는 보고에 대해 개발자, 운영, 비즈니스가 동일한 데이터를 보고 빠르게 의사결정할 수 있습니다. 이것이 DevOps에서 **가시성** (Visibility)이 중요한 이유입니다.

### 알림은 액션으로 이어져야 한다

알림(Alert)은 받는 것이 목적이 아니라, **즉시 행동이 필요한 상황**에만 울려야 합니다. 모든 경고를 알림으로 보내면 피로(Alert Fatigue)가 쌓여 정작 중요한 알림을 무시하게 됩니다.

| 수준 | 기준 | 액션 |
| --- | --- | --- |
| **긴급 (Page)** | 사용자에게 영향. 즉시 대응 필요 | 당직자 호출. 자동 복구 트리거 |
| **경고 (Warning)** | 곧 문제가 될 수 있음 | 업무 시간 내 확인. 티켓 생성 |
| **정보 (Info)** | 참고용. 대응 불필요 | 대시보드에만 표시. 알림 안 보냄 |

{% hint style="warning" %}
**Alert Fatigue(알림 피로)** — 너무 많은 알림은 오히려 중요한 알림을 놓치게 합니다. 액션 없이 받기만 하는 알림은 주기적으로 삭제하거나 Info 레벨로 낮추세요.
{% endhint %}

지속 가능한 알림 운영을 위한 원칙:

- **액션 없는 알림은 제거하세요.** 받고도 아무것도 안 하는 알림은 노이즈입니다.
- **자동 복구를 먼저 시도하세요.** 알림 → Lambda/Runbook으로 자동 대응 → 실패 시에만 사람 호출.
- **정기적으로 알림을 리뷰하세요.** 한 달간 한 번도 액션하지 않은 알림은 삭제 후보입니다.

## SLO 모니터링

SLI/SLO/SLA 개념과 에러 버짓에 대해서는 [DevOps란?](what-is-devops.md)에서 다룹니다. 아래는 SLO를 측정하기 위한 주요 CSP 도구입니다.

| 벤더 | 도구 | 기능 |
| --- | --- | --- |
| AWS | CloudWatch Application Signals | SLO 정의, 에러 버짓 추적, 서비스 맵 연동 |
| Azure | Azure Monitor SLO (Preview) | SLI 기반 SLO 설정, 번다운 차트 |
| GCP | Cloud Monitoring SLO | SLO 정의, 에러 버짓 알림, 서비스 대시보드 |
| OCI | OCI Monitoring + Alarms | 커스텀 메트릭 기반 SLO 구성 |

## 제품 비교

### 메트릭 + 대시보드 + 알림

| 벤더 | 제품 | 비고 |
| --- | --- | --- |
| AWS | CloudWatch Metrics + Alarms | AWS 서비스 메트릭 자동 수집. 커스텀 메트릭 지원 |
| Azure | Azure Monitor Metrics + Alerts | Azure 서비스 통합. Action Groups로 알림 라우팅 |
| GCP | Cloud Monitoring | 자동 수집 + 커스텀 메트릭. PromQL 호환 |
| OCI | OCI Monitoring | OCI 서비스 메트릭 자동 수집. 알람 + 알림 |

### 로그

| 벤더 | 제품 | 비고 |
| --- | --- | --- |
| AWS | CloudWatch Logs | 로그 그룹/스트림 구조. Logs Insights로 쿼리 |
| Azure | Azure Monitor Logs (Log Analytics) | KQL(Kusto Query Language)로 분석 |
| GCP | Cloud Logging | 자동 수집. Log Analytics로 SQL 쿼리 |
| OCI | OCI Logging | 서비스 로그 자동 수집. Logging Analytics로 분석 |

### 분산 트레이싱

| 벤더 | 제품 | 비고 |
| --- | --- | --- |
| AWS | X-Ray | AWS 서비스 간 요청 추적. OpenTelemetry 호환 |
| Azure | Application Insights | 자동 계측. 성능 이상 탐지 |
| GCP | Cloud Trace | 자동 수집. OpenTelemetry 호환 |
| OCI | OCI APM Tracing | 분산 트레이싱. OpenTelemetry 호환 |

### 통합 대시보드

| 벤더 | 제품 | 비고 |
| --- | --- | --- |
| AWS | CloudWatch Dashboards | |
| Azure | Azure Dashboards / Workbooks | Workbooks로 인터랙티브 리포트 |
| GCP | Cloud Monitoring Dashboards | |
| OCI | OCI Monitoring Console | 커스텀 대시보드 |
| 3rd party | Grafana, Datadog, New Relic | 멀티클라우드 통합 모니터링에 많이 사용 |

## 핵심 차이점

**AWS CloudWatch** — AWS 서비스 메트릭이 자동으로 수집되며, 알림 → SNS → Lambda 연동으로 자동 복구 파이프라인을 구성할 수 있습니다. 다만 로그 쿼리(Logs Insights)는 타사 대비 기능이 제한적입니다.

**Azure Monitor** — Application Insights가 애플리케이션 성능 모니터링(APM)을 기본 제공합니다. KQL로 강력한 로그 분석이 가능하며, Workbooks로 인터랙티브 리포트를 만들 수 있습니다.

**GCP Cloud Operations** — OpenTelemetry와의 통합이 가장 자연스럽습니다. Cloud Logging이 모든 GCP 서비스 로그를 자동 수집하며, BigQuery로 내보내 장기 분석이 가능합니다.

**OCI Monitoring** — OCI 서비스 메트릭을 자동 수집하며, Logging Analytics로 로그 분석과 시각화를 제공합니다. APM Tracing으로 분산 트레이싱도 지원합니다.

### 멀티클라우드 모니터링

여러 벤더를 사용하는 환경에서는 Grafana, Datadog, New Relic 같은 3rd party 도구로 통합 모니터링하는 것이 일반적입니다. OpenTelemetry를 표준 계측 라이브러리로 사용하면 벤더 종속 없이 메트릭/로그/트레이스를 수집할 수 있습니다.

## 관련 문서

{% content-ref url="what-is-devops.md" %}
[DevOps란? (SLI/SLO/에러 버짓)](what-is-devops.md)
{% endcontent-ref %}

{% content-ref url="../governance/dr.md" %}
[재해복구 (DR)](../governance/dr.md)
{% endcontent-ref %}

## 참고하기

### AWS

- [Amazon CloudWatch 문서](https://docs.aws.amazon.com/ko_kr/cloudwatch/)
- [AWS X-Ray 문서](https://docs.aws.amazon.com/ko_kr/xray/)

### Azure

- [Azure Monitor 문서](https://learn.microsoft.com/ko-kr/azure/azure-monitor/)
- [Application Insights 문서](https://learn.microsoft.com/ko-kr/azure/azure-monitor/app/app-insights-overview)

### GCP

- [Cloud Monitoring 문서](https://cloud.google.com/monitoring/docs)
- [Cloud Logging 문서](https://cloud.google.com/logging/docs)
- [Cloud Trace 문서](https://cloud.google.com/trace/docs)

### OCI

- [OCI Monitoring 문서](https://docs.oracle.com/en-us/iaas/Content/Monitoring/home.htm)
- [OCI Logging 문서](https://docs.oracle.com/en-us/iaas/Content/Logging/home.htm)
- [OCI Application Performance Monitoring](https://docs.oracle.com/en-us/iaas/application-performance-monitoring/index.html)

### 오픈소스 / 3rd party

- [OpenTelemetry](https://opentelemetry.io/docs/)
- [Grafana](https://grafana.com/docs/)
