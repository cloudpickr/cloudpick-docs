---
title: "메시지 큐와 이벤트 스트리밍"
description: "메시지 큐와 이벤트 스트리밍의 개념, 벤더별 서비스, 선택 기준을 비교합니다."
---

> 문서 기준: 2026년 5월

## 개요

### 쉽게 이해하기

**메시지 큐**는 식당의 주문 전표와 같습니다. 홀(생산자)이 전표를 꽂으면 주방(소비자)이 바쁠 때는 전표가 쌓이고, 여유가 생기면 순서대로 처리합니다. 홀은 주방 상태를 몰라도 됩니다.

**이벤트 스트리밍**은 라디오 방송과 같습니다. 방송국(생산자)은 한 번 송출하고, 여러 청취자(소비자)가 각자 듣는 시점이 다를 수 있습니다. 녹음(보존)해두면 나중에 다시 들을 수도 있습니다.

### 왜 필요한가 — 동기 호출의 문제

주문 서비스가 결제 → 재고 → 알림을 동기로 호출하면:
- 하나라도 느리면 **전체 지연**
- 하나라도 죽으면 **주문 실패**
- 트래픽 급증 시 **연쇄 장애**

메시지 큐를 넣으면: 주문은 즉시 완료되고, 나머지는 각자 속도로 처리합니다. 장애가 격리됩니다.

### 온프레미스에서 쓰던 것

| 클라우드 서비스 | 온프레미스 대응 |
| --- | --- |
| SQS, Service Bus Queue | IBM MQ(MQ Series), RabbitMQ, ActiveMQ |
| MSK, Event Hubs | Apache Kafka (직접 운영) |
| SNS, Event Grid | RabbitMQ Exchange(fanout), TIBCO |
| EventBridge, Eventarc | ESB(Enterprise Service Bus) — 다만 ESB보다 경량 |

### 메시지 큐 vs 이벤트 스트리밍

마이크로서비스 간 직접 호출(동기)은 결합도를 높이고 장애가 전파됩니다. **메시지 큐**와 **이벤트 스트리밍**은 서비스 간 통신을 비동기로 분리하여 느슨한 결합, 부하 완충, 장애 격리를 제공합니다.

| 구분 | 메시지 큐 | 이벤트 스트리밍 |
| --- | --- | --- |
| **모델** | 생산자 → 큐 → 소비자 (1:1 또는 팬아웃) | 생산자 → 토픽 → 여러 소비자 (Pub/Sub) |
| **메시지 보존** | 소비 후 삭제 | 보존 기간 동안 재읽기 가능 |
| **순서 보장** | FIFO 옵션 | 파티션 내 순서 보장 |
| **적합한 경우** | 작업 큐, 비동기 처리, 부하 분산 | 이벤트 소싱, 실시간 분석, 로그 수집 |

## 벤더별 서비스 비교

| 영역 | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- |
| **메시지 큐** | [SQS](https://docs.aws.amazon.com/sqs/) | [Service Bus Queue](https://learn.microsoft.com/azure/service-bus-messaging/) | [Cloud Tasks](https://cloud.google.com/tasks/docs) | [OCI Queue](https://docs.oracle.com/en-us/iaas/Content/queue/home.htm) |
| **Pub/Sub** | [SNS](https://docs.aws.amazon.com/sns/) | [Service Bus Topic](https://learn.microsoft.com/azure/service-bus-messaging/) | [Pub/Sub](https://cloud.google.com/pubsub/docs) | [OCI Streaming](https://docs.oracle.com/en-us/iaas/Content/Streaming/home.htm) |
| **이벤트 라우팅** | [EventBridge](https://docs.aws.amazon.com/eventbridge/) | [Event Grid](https://learn.microsoft.com/azure/event-grid/) | [Eventarc](https://cloud.google.com/eventarc/docs) | [OCI Events](https://docs.oracle.com/en-us/iaas/Content/Events/home.htm) |
| **스트리밍 (Kafka 호환)** | [MSK](https://docs.aws.amazon.com/msk/) | [Event Hubs](https://learn.microsoft.com/azure/event-hubs/) (Kafka 프로토콜 호환) | [Pub/Sub](https://cloud.google.com/pubsub/docs) + [Dataflow](https://cloud.google.com/dataflow/docs) | [OCI Streaming](https://docs.oracle.com/en-us/iaas/Content/Streaming/home.htm) (Kafka 호환) |

## 언제 무엇을 선택할 것인가

| 요구사항 | 권장 |
| --- | --- |
| 단순 작업 큐 (비동기 처리, 재시도) | SQS, Service Bus Queue, Cloud Tasks, OCI Queue |
| 이벤트 팬아웃 (1:N 알림) | SNS, Service Bus Topic, Pub/Sub |
| 이벤트 기반 아키텍처 (라우팅, 필터링) | EventBridge, Event Grid, Eventarc |
| 대용량 실시간 스트리밍 (로그, 클릭스트림) | MSK/Kafka, Event Hubs, Pub/Sub, OCI Streaming |
| 이벤트 소싱 (이력 재생 필요) | Kafka(MSK), Event Hubs (Capture) |
| 벤더 중립 (멀티클라우드) | Apache Kafka (자체 운영 또는 Confluent Cloud) |

## 자주 하는 실수

- **메시지 큐와 이벤트 스트리밍을 혼동하여 선택** — 1:1 작업 큐가 필요한데 Kafka를 도입하거나, 이벤트 재생이 필요한데 SQS를 선택하면 아키텍처가 맞지 않습니다.
- **Dead Letter Queue(DLQ)를 설정하지 않음** — 처리 실패 메시지가 무한 재시도되면 큐가 막히고 정상 메시지도 처리되지 않습니다.
- **메시지 순서 보장이 필요한데 일반 큐를 사용** — 표준 큐는 순서를 보장하지 않습니다. 순서가 중요하면 FIFO 큐 또는 파티션 키 기반 스트리밍을 선택하세요.

## 체크리스트

- [ ] 메시지 패턴(1:1 큐 vs 1:N 팬아웃 vs 스트리밍)을 요구사항에 맞게 선택했는가
- [ ] Dead Letter Queue와 재시도 정책(최대 횟수, 백오프)을 설정했는가
- [ ] 소비자 장애 시 메시지 유실이 없는지(at-least-once 보장) 확인했는가

## 참고하기

### AWS

- [Amazon SQS 문서](https://docs.aws.amazon.com/sqs/)
- [Amazon EventBridge 문서](https://docs.aws.amazon.com/eventbridge/)
- [Amazon MSK 문서](https://docs.aws.amazon.com/msk/)

### Azure

- [Azure Service Bus 문서](https://learn.microsoft.com/azure/service-bus-messaging/)
- [Azure Event Hubs 문서](https://learn.microsoft.com/azure/event-hubs/)

### Google Cloud

- [Cloud Pub/Sub 문서](https://cloud.google.com/pubsub/docs)
- [Eventarc 문서](https://cloud.google.com/eventarc/docs)

### OCI

- [OCI Queue 문서](https://docs.oracle.com/en-us/iaas/Content/queue/home.htm)
- [OCI Streaming 문서](https://docs.oracle.com/en-us/iaas/Content/Streaming/home.htm)
