---
title: "Message Queues and Event Streaming"
description: "Compares the concept of message queues and event streaming, vendor services, and selection criteria."
---

> Last reviewed: August 2026

## Overview

### An easy way to understand it

A **message queue** is like a restaurant's order slip. When the front of house (producer) puts up a slip, it piles up while the kitchen (consumer) is busy, and gets processed in order once there's capacity. The front of house doesn't need to know the kitchen's state.

**Event streaming** is like a radio broadcast. The station (producer) transmits once, and multiple listeners (consumers) may each tune in at different times. If it's recorded (retained), it can also be listened to again later.

### Why it's needed — the problem with synchronous calls

If the order service calls payment → inventory → notification synchronously:
- If even one is slow, **everything is delayed**
- If even one fails, **the order fails**
- During a traffic surge, **cascading failures** occur

Adding a message queue: the order completes immediately, and the rest is processed at its own pace. Failures are isolated.

### What was used on-premises

| Cloud service | On-premises equivalent |
| --- | --- |
| SQS, Service Bus Queue | IBM MQ (MQ Series), RabbitMQ, ActiveMQ |
| MSK, Event Hubs | Apache Kafka (self-managed) |
| SNS, Event Grid | RabbitMQ Exchange (fanout), TIBCO |
| EventBridge, Eventarc | ESB (Enterprise Service Bus) — though lighter-weight than an ESB |

### Message queue vs. event streaming

Direct (synchronous) calls between microservices increase coupling and propagate failures. **Message queues** and **event streaming** decouple inter-service communication asynchronously, providing loose coupling, load buffering, and failure isolation.

| Aspect | Message queue | Event streaming |
| --- | --- | --- |
| **Model** | Producer → queue → consumer (1:1 or fan-out) | Producer → topic → multiple consumers (Pub/Sub) |
| **Message retention** | Deleted after consumption | Can be re-read during the retention period |
| **Order guarantee** | FIFO option | Order guaranteed within a partition |
| **Suitable for** | Work queues, async processing, load distribution | Event sourcing, real-time analytics, log collection |

## Comparison of vendor services

| Area | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- |
| **Message queue** | [SQS](https://docs.aws.amazon.com/sqs/) | [Service Bus Queue](https://learn.microsoft.com/azure/service-bus-messaging/) | [Cloud Tasks](https://cloud.google.com/tasks/docs) | [OCI Queue](https://docs.oracle.com/en-us/iaas/Content/queue/home.htm) |
| **Pub/Sub** | [SNS](https://docs.aws.amazon.com/sns/) | [Service Bus Topic](https://learn.microsoft.com/azure/service-bus-messaging/) | [Pub/Sub](https://cloud.google.com/pubsub/docs) | [OCI Streaming](https://docs.oracle.com/en-us/iaas/Content/Streaming/home.htm) |
| **Event routing** | [EventBridge](https://docs.aws.amazon.com/eventbridge/) | [Event Grid](https://learn.microsoft.com/azure/event-grid/) | [Eventarc](https://cloud.google.com/eventarc/docs) | [OCI Events](https://docs.oracle.com/en-us/iaas/Content/Events/home.htm) |
| **Streaming (Kafka-compatible)** | [MSK](https://docs.aws.amazon.com/msk/) | [Event Hubs](https://learn.microsoft.com/azure/event-hubs/) (Kafka protocol compatible) | [Pub/Sub](https://cloud.google.com/pubsub/docs) + [Dataflow](https://cloud.google.com/dataflow/docs) | [OCI Streaming](https://docs.oracle.com/en-us/iaas/Content/Streaming/home.htm) (Kafka compatible) |

## What to choose when

| Requirement | Recommendation |
| --- | --- |
| Simple work queue (async processing, retries) | SQS, Service Bus Queue, Cloud Tasks, OCI Queue |
| Event fan-out (1:N notification) | SNS, Service Bus Topic, Pub/Sub |
| Event-driven architecture (routing, filtering) | EventBridge, Event Grid, Eventarc |
| High-volume real-time streaming (logs, clickstream) | MSK/Kafka, Event Hubs, Pub/Sub, OCI Streaming |
| Event sourcing (history replay needed) | Kafka (MSK), Event Hubs (Capture) |
| Vendor-neutral (multi-cloud) | Apache Kafka (self-managed or Confluent Cloud) |

## Common mistakes

- **Confusing message queues with event streaming** — Adopting Kafka when a 1:1 work queue is needed, or choosing SQS when event replay is required, results in a mismatched architecture.
- **Not configuring a Dead Letter Queue (DLQ)** — If failed messages retry endlessly, the queue gets clogged and normal messages also stop being processed.
- **Using a standard queue when message ordering is required** — Standard queues don't guarantee order. If order matters, choose a FIFO queue or partition-key-based streaming.

## Checklist

- [ ] Have you chosen the message pattern (1:1 queue vs. 1:N fan-out vs. streaming) to fit your requirements?
- [ ] Have you configured a Dead Letter Queue and retry policy (max attempts, backoff)?
- [ ] Have you confirmed there's no message loss on consumer failure (at-least-once guarantee)?

## References

### AWS

- [Amazon SQS documentation](https://docs.aws.amazon.com/sqs/)
- [Amazon EventBridge documentation](https://docs.aws.amazon.com/eventbridge/)
- [Amazon MSK documentation](https://docs.aws.amazon.com/msk/)

### Azure

- [Azure Service Bus documentation](https://learn.microsoft.com/azure/service-bus-messaging/)
- [Azure Event Hubs documentation](https://learn.microsoft.com/azure/event-hubs/)

### Google Cloud

- [Cloud Pub/Sub documentation](https://cloud.google.com/pubsub/docs)
- [Eventarc documentation](https://cloud.google.com/eventarc/docs)

### OCI

- [OCI Queue documentation](https://docs.oracle.com/en-us/iaas/Content/queue/home.htm)
- [OCI Streaming documentation](https://docs.oracle.com/en-us/iaas/Content/Streaming/home.htm)
