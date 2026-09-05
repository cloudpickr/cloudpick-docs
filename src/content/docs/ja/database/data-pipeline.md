---
title: "データパイプラインとETL"
description: "データパイプライン(ETL/ELT)の概念、ベンダー別サービス、バッチ vs ストリーミングの選択を比較します。"
---

> 文書基準: 2026年8月

## 概要

元データを[分析プラットフォーム](../../database/analytics/)やMLパイプラインで使用するには、**抽出(Extract) → 変換(Transform) → 格納(Load)** の過程が必要です。

| 区分 | ETL | ELT |
| --- | --- | --- |
| **変換の位置** | パイプライン中間(別エンジン) | 格納後に対象システムで変換 |
| **適した場合** | データ整形が複雑、対象システムの負荷制限 | 対象がBigQuery/Redshiftのように計算能力十分 |
| **トレンド** | 従来型の方式 | クラウドDWの計算力活用で主流化 |

## ベンダー別サービス比較

| ベンダー | バッチETL/ELT | ストリーミング | オーケストレーション |
| --- | --- | --- | --- |
| AWS | [Glue](https://docs.aws.amazon.com/glue/)(サーバーレスSpark) | [Kinesis Data Streams](https://docs.aws.amazon.com/kinesis/) | [Step Functions](https://docs.aws.amazon.com/step-functions/)、[MWAA](https://docs.aws.amazon.com/mwaa/)(Airflow) |
| Azure | [Data Factory](https://learn.microsoft.com/azure/data-factory/) | [Stream Analytics](https://learn.microsoft.com/azure/stream-analytics/) | Data Factoryパイプライン、[Synapse Pipelines](https://learn.microsoft.com/azure/synapse-analytics/) |
| Google Cloud | [Dataflow](https://cloud.google.com/dataflow/docs)(Apache Beam) | Dataflow(統合) | [Cloud Composer](https://cloud.google.com/composer/docs)(Airflow)、[Workflows](https://cloud.google.com/workflows/docs) |
| OCI | [OCI Data Integration](https://docs.oracle.com/en-us/iaas/data-integration/home.htm) | [OCI Streaming](https://docs.oracle.com/en-us/iaas/Content/Streaming/home.htm) + [Data Flow](https://docs.oracle.com/en-us/iaas/data-flow/using/home.htm)(Spark) | OCI Data Integrationパイプライン |

## バッチ vs ストリーミング

| 項目 | バッチ | ストリーミング |
| --- | --- | --- |
| **遅延** | 分〜時間 | 秒〜分 |
| **コスト** | 実行時間のみ課金(サーバーレス) | 常時実行(またはイベントベース) |
| **複雑度** | 低い | 高い(順序、重複、遅延処理) |
| **適した場合** | 日/週単位のレポート、大量マイグレーション | リアルタイムダッシュボード、異常検知、レコメンド |

## Zero-ETL

運用DBから分析プラットフォームへデータを**パイプラインなしで自動的に**レプリケーション/同期するアプローチです。ETLパイプラインの構築・保守の負担を取り除くことが目標です。

### ETL → ELT → Zero-ETLの流れ

| 世代 | 方式 | 負担 |
| --- | --- | --- |
| ETL | 別エンジンで変換後に格納 | パイプラインの構築・運用・モニタリング |
| ELT | 格納後にDWで変換 | パイプラインは単純化、変換ロジックは依然として必要 |
| Zero-ETL | ソース → 対象を自動レプリケーション、パイプライン不要 | 設定するだけ(理論上) |

### ベンダー別Zero-ETLの現状

| ベンダー | サービス | ソース → 対象 |
| --- | --- | --- |
| AWS | Aurora Zero-ETL to Redshift | Aurora MySQL/PostgreSQL → Redshift |
| AWS | DynamoDB Zero-ETL to Redshift | DynamoDB → Redshift |
| Azure | Fabric Mirroring | Azure SQL/Cosmos DB → Microsoft Fabric |
| Google Cloud | BigQuery連続クエリ + Change Streams | Spanner/Bigtable → BigQuery |
| OCI | GoldenGate + Autonomous DB | 運用DB → Autonomous DW |

### 依然として残る限界

| 限界 | 説明 |
| --- | --- |
| **ベンダー依存** | 同一ベンダー内のソース→対象のみサポート。クロスベンダーZero-ETLは存在しない |
| **変換ロジックの不在** | データを「そのまま」レプリケーションするだけで、ビジネス変換(整形、集計、結合)は別途必要 |
| **スキーマ変更への対応** | ソーススキーマが変わると同期が壊れたり手動介入が必要 |
| **サポートソースの制限** | すべてのDBがサポートされるわけではない。特定のエンジン/バージョンのみ可能 |

:::note
Zero-ETLは**単純レプリケーション**に適しており、複雑な変換・複数ソース結合・クロスベンダー統合には依然としてETL/ELTパイプラインが必要です。現実的にはZero-ETL + 軽量ELTの組み合わせになるでしょう。
:::

## いつ何を選ぶか

| 要件 | 推奨 |
| --- | --- |
| 単純レプリケーション(同一ベンダー、変換不要) | Zero-ETL |
| サーバーレスバッチETL(Spark) | Glue、Dataflow、Data Flow |
| コードレスETL(GUIベース) | Data Factory、OCI Data Integration |
| バッチ+ストリーミング統合(Apache Beam) | Google Cloud Dataflow |
| ワークフローオーケストレーション(DAG) | Airflow(MWAA、Cloud Composer)、Step Functions |
| リアルタイムストリーミング分析 | Kinesis Analytics、Stream Analytics、Dataflow |

## よくある間違い

- **バッチで十分なワークロードにストリーミングを導入** — リアルタイム処理が不要なのにストリーミングを選択すると、複雑度とコストだけが増加します。日/週単位のレポートはバッチで十分です。
- **Zero-ETLを万能と期待** — Zero-ETLは単純レプリケーションのみをサポートします。ビジネス変換(整形、集計、結合)が必要な場合は依然としてETL/ELTパイプラインが必要です。
- **パイプラインモニタリングなしで運用** — データ遅延、スキーマ変更、失敗したジョブを検知できないと、分析結果が古いデータに基づくことになります。

## チェックリスト

- [ ] ワークロードの遅延許容範囲(分/時間/日)を定義し、バッチ vs ストリーミングを選択したか
- [ ] パイプライン失敗時のアラートとリトライポリシーが設定されているか
- [ ] ソーススキーマ変更時にパイプラインが壊れないようスキーマ進化(Schema Evolution)戦略があるか

## 参考資料

### AWS

- [AWS Glue ドキュメント](https://docs.aws.amazon.com/glue/)
- [Amazon Kinesis ドキュメント](https://docs.aws.amazon.com/kinesis/)

### Azure

- [Azure Data Factory ドキュメント](https://learn.microsoft.com/azure/data-factory/)
- [Azure Stream Analytics ドキュメント](https://learn.microsoft.com/azure/stream-analytics/)

### Google Cloud

- [Dataflow ドキュメント](https://cloud.google.com/dataflow/docs)
- [Cloud Composer ドキュメント](https://cloud.google.com/composer/docs)

### OCI

- [OCI Data Integration ドキュメント](https://docs.oracle.com/en-us/iaas/data-integration/home.htm)
- [OCI Data Flow ドキュメント](https://docs.oracle.com/en-us/iaas/data-flow/using/home.htm)
