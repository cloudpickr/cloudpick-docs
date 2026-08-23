---
title: "メッセージキューとイベントストリーミング"
description: "メッセージキューとイベントストリーミングの概念、ベンダー別サービス、選択基準を比較します。"
---

> 文書基準: 2026年5月

## 概要

### わかりやすく理解する

**メッセージキュー**はレストランの注文伝票のようなものです。ホール(生産者)が伝票を挿すと、厨房(消費者)が忙しいときは伝票が積み上がり、余裕ができれば順番に処理します。ホールは厨房の状態を知らなくても構いません。

**イベントストリーミング**はラジオ放送のようなものです。放送局(生産者)は一度送出し、複数のリスナー(消費者)がそれぞれ異なるタイミングで聴くことがあります。録音(保存)しておけば後で再度聴くこともできます。

### なぜ必要か — 同期呼び出しの問題

注文サービスが決済 → 在庫 → 通知を同期で呼び出すと:
- 1つでも遅ければ**全体が遅延**
- 1つでも落ちれば**注文失敗**
- トラフィック急増時に**連鎖障害**

メッセージキューを入れると: 注文は即座に完了し、残りはそれぞれの速度で処理します。障害が隔離されます。

### オンプレミスで使われていたもの

| クラウドサービス | オンプレミス対応 |
| --- | --- |
| SQS、Service Bus Queue | IBM MQ(MQ Series)、RabbitMQ、ActiveMQ |
| MSK、Event Hubs | Apache Kafka(自前運用) |
| SNS、Event Grid | RabbitMQ Exchange(fanout)、TIBCO |
| EventBridge、Eventarc | ESB(Enterprise Service Bus) — ただしESBより軽量 |

### メッセージキュー vs イベントストリーミング

マイクロサービス間の直接呼び出し(同期)は結合度を高め、障害が伝播します。**メッセージキュー**と**イベントストリーミング**はサービス間通信を非同期に分離し、疎結合、負荷緩衝、障害隔離を提供します。

| 区分 | メッセージキュー | イベントストリーミング |
| --- | --- | --- |
| **モデル** | 生産者 → キュー → 消費者(1:1またはファンアウト) | 生産者 → トピック → 複数の消費者(Pub/Sub) |
| **メッセージ保存** | 消費後に削除 | 保存期間中は再読み取り可能 |
| **順序保証** | FIFOオプション | パーティション内で順序保証 |
| **適した場合** | 作業キュー、非同期処理、負荷分散 | イベントソーシング、リアルタイム分析、ログ収集 |

## ベンダー別サービス比較

| 領域 | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- |
| **メッセージキュー** | [SQS](https://docs.aws.amazon.com/sqs/) | [Service Bus Queue](https://learn.microsoft.com/azure/service-bus-messaging/) | [Cloud Tasks](https://cloud.google.com/tasks/docs) | [OCI Queue](https://docs.oracle.com/en-us/iaas/Content/queue/home.htm) |
| **Pub/Sub** | [SNS](https://docs.aws.amazon.com/sns/) | [Service Bus Topic](https://learn.microsoft.com/azure/service-bus-messaging/) | [Pub/Sub](https://cloud.google.com/pubsub/docs) | [OCI Streaming](https://docs.oracle.com/en-us/iaas/Content/Streaming/home.htm) |
| **イベントルーティング** | [EventBridge](https://docs.aws.amazon.com/eventbridge/) | [Event Grid](https://learn.microsoft.com/azure/event-grid/) | [Eventarc](https://cloud.google.com/eventarc/docs) | [OCI Events](https://docs.oracle.com/en-us/iaas/Content/Events/home.htm) |
| **ストリーミング(Kafka互換)** | [MSK](https://docs.aws.amazon.com/msk/) | [Event Hubs](https://learn.microsoft.com/azure/event-hubs/)(Kafkaプロトコル互換) | [Pub/Sub](https://cloud.google.com/pubsub/docs) + [Dataflow](https://cloud.google.com/dataflow/docs) | [OCI Streaming](https://docs.oracle.com/en-us/iaas/Content/Streaming/home.htm)(Kafka互換) |

## いつ何を選ぶか

| 要件 | 推奨 |
| --- | --- |
| シンプルな作業キュー(非同期処理、リトライ) | SQS、Service Bus Queue、Cloud Tasks、OCI Queue |
| イベントファンアウト(1:N通知) | SNS、Service Bus Topic、Pub/Sub |
| イベント駆動アーキテクチャ(ルーティング、フィルタリング) | EventBridge、Event Grid、Eventarc |
| 大容量リアルタイムストリーミング(ログ、クリックストリーム) | MSK/Kafka、Event Hubs、Pub/Sub、OCI Streaming |
| イベントソーシング(履歴再生が必要) | Kafka(MSK)、Event Hubs(Capture) |
| ベンダー中立(マルチクラウド) | Apache Kafka(自前運用またはConfluent Cloud) |

## よくある間違い

- **メッセージキューとイベントストリーミングを混同して選択** — 1:1の作業キューが必要なのにKafkaを導入したり、イベント再生が必要なのにSQSを選択すると、アーキテクチャが合いません。
- **Dead Letter Queue(DLQ)を設定しない** — 処理失敗メッセージが無限リトライされるとキューが詰まり、正常なメッセージも処理されなくなります。
- **メッセージ順序保証が必要なのに一般的なキューを使用** — 標準キューは順序を保証しません。順序が重要な場合はFIFOキューまたはパーティションキーベースのストリーミングを選択してください。

## チェックリスト

- [ ] メッセージパターン(1:1キュー vs 1:Nファンアウト vs ストリーミング)を要件に合わせて選択したか
- [ ] Dead Letter Queueとリトライポリシー(最大回数、バックオフ)を設定したか
- [ ] 消費者障害時にメッセージ損失がないか(at-least-once保証)を確認したか

## 関連ドキュメント

- [サーバーレス](../../compute/serverless/) — イベントトリガー・非同期呼び出しとキュー連携
- [API Gateway](../../networking/api-gateway/) — 同期API前段と非同期バックエンドの分離
- [データパイプラインとETL](../../database/data-pipeline/) — ストリーミング・バッチパイプライン
- [統合可観測性アーキテクチャ](../../devops/observability/) — キュー/ストリームの遅延・失敗の観測

## 参考資料

### AWS

- [Amazon SQS ドキュメント](https://docs.aws.amazon.com/sqs/)
- [Amazon EventBridge ドキュメント](https://docs.aws.amazon.com/eventbridge/)
- [Amazon MSK ドキュメント](https://docs.aws.amazon.com/msk/)

### Azure

- [Azure Service Bus ドキュメント](https://learn.microsoft.com/azure/service-bus-messaging/)
- [Azure Event Hubs ドキュメント](https://learn.microsoft.com/azure/event-hubs/)

### Google Cloud

- [Cloud Pub/Sub ドキュメント](https://cloud.google.com/pubsub/docs)
- [Eventarc ドキュメント](https://cloud.google.com/eventarc/docs)

### OCI

- [OCI Queue ドキュメント](https://docs.oracle.com/en-us/iaas/Content/queue/home.htm)
- [OCI Streaming ドキュメント](https://docs.oracle.com/en-us/iaas/Content/Streaming/home.htm)
