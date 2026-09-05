---
title: "データ分析プラットフォーム"
description: "データウェアハウス、データレイクハウス、分析プラットフォームをベンダー別に比較します。"
---

> 文書基準: 2026年8月

## 概要

:::note[前提知識と関連ドキュメント]
トランザクションデータベースの選択は、[マネージドRDB](../../database/managed-rdb/)、[NoSQL](../../database/nosql/)を先に参照してください。データ収集・変換は[データパイプライン](../../database/data-pipeline/)と連携します。本ドキュメントは、大規模集計・BI・データウェアハウスなどの分析(OLAP)ワークロードに焦点を当てます。
:::

### OLTP vs OLAP — なぜ分離するのか

運用データベース([管理型RDB](../../database/managed-rdb/)、[NoSQL](../../database/nosql/))はトランザクション処理(OLTP)に最適化されています。大量データを集計・分析するには別途の分析プラットフォーム(OLAP)が必要です。

**例え:** 運用DBは店舗のレジ(高速な個別取引処理)であり、ウェアハウスは本社の経営分析チーム(全店舗のデータを集めてトレンド分析)です。レジで経営分析を行うと行列が長くなります。

運用DBで大量の集計クエリを実行すると:
- トランザクション処理性能の低下(注文が遅くなる)
- 正規化されたスキーマでは分析クエリのJOINが数十個 → 遅く複雑
- そのため運用DB → ETL → 分析専用DB(ウェアハウス)に分離

| 区分 | OLTP(運用DB) | OLAP(分析プラットフォーム) |
| --- | --- | --- |
| **目的** | 個別トランザクション処理(注文、決済) | 大量データ集計・分析(売上トレンド、ユーザー行動) |
| **クエリパターン** | 少量行の読み書き(ミリ秒単位) | 大量行のスキャン・集計(秒〜分単位) |
| **データサイズ** | GB〜TB | TB〜PB |
| **スキーマ** | 正規化(3NF) | 非正規化(Star/Snowflake)またはスキーマレス |

## ベンダー別分析プラットフォーム比較

| ベンダー | データウェアハウス | 特徴 | 課金モデル |
| --- | --- | --- | --- |
| AWS | [Amazon Redshift](https://docs.aws.amazon.com/redshift/latest/mgmt/welcome.html) | クラスタベース + Serverlessオプション。S3データを直接クエリ(Spectrum) | ノード時間またはRPU(Serverless) |
| Azure | [Azure Synapse Analytics](https://learn.microsoft.com/azure/synapse-analytics/) | 統合分析プラットフォーム(SQL + Spark + Data Explorer)。サーバーレスSQLプール | DWU(専用)またはクエリデータ処理量(サーバーレス) |
| Google Cloud | [BigQuery](https://cloud.google.com/bigquery/docs) | 完全サーバーレス。インフラ管理不要。ML内蔵(BQML) | クエリスキャン量またはスロット(容量予約) |
| OCI | [OCI Analytics Cloud](https://docs.oracle.com/en-us/iaas/analytics-cloud/index.html) + [Autonomous Data Warehouse](https://docs.oracle.com/en-us/iaas/autonomous-database-serverless/index.html) | Oracle DBベースの自動チューニング。BI可視化統合 | OCPU時間 |

### 主な違い

**BigQuery(Google Cloud)** — 完全サーバーレスでクラスタ管理が不要です。クエリスキャンデータ量に基づく課金であり、BigQuery MLによりSQLベースのML学習をサポートします。Gemini 3.1 Flash Lite / 3.5 Flashモデルが生成AI関数でGA利用可能となり、Conversational Analytics（プレビュー）で自然言語データ分析が可能です。MCP（Model Context Protocol）統合でエージェントベースの分析ワークフローを構築できます。

**Redshift(AWS)** — クラスタベースとServerlessオプションの両方を提供します。S3のデータをRedshift Spectrumで直接クエリでき、データレイクとの統合が容易です。ServerlessではAI駆動の自動スケーリングが新規ワークグループのデフォルトとなりました（2026.04）。3年予約（Serverless Reservations）でコスト削減が可能です。スナップショット復元時にzero-ETL/S3イベント統合が自動保持されます（2026.07）。

**Synapse(Azure)** — SQL分析、Apache Spark、Data Explorerを1つのプラットフォームで提供します。サーバーレスSQLプールでデータレイクを直接クエリでき、Power BIとネイティブ統合されます。Microsoft Fabricへの統合が進行中で、VS Code統合の強化、ノートブックの復元力向上、ML・ガバナンス機能拡張、リアルタイムデータ処理など継続的に機能追加されています。

**Autonomous DW(OCI)** — Oracle Databaseベースで自動チューニング、自動スケーリングを提供します。既存のOracleワークロードとの互換性が高いです。

## データレイク vs データウェアハウス vs レイクハウス

| アーキテクチャ | 特徴 | 適した場合 |
| --- | --- | --- |
| **データレイク** | 生データをそのまま保存(S3/ADLS/GCS)。スキーマオンリード | 多様な形式の大量データ保存、ML学習データ |
| **データウェアハウス** | 整形されたデータを構造化して保存。スキーマオンライト | 定型データ分析、BIレポート、ダッシュボード |
| **レイクハウス** | レイクの上にウェアハウス機能を追加(Delta Lake、Iceberg) | 両者を統合したい場合 |

ベンダー別レイクハウスアプローチ:

| ベンダー | レイクハウスアプローチ |
| --- | --- |
| AWS | S3 + Glue Catalog + Redshift Spectrum + Athena(Apache Icebergサポート) |
| Azure | ADLS Gen2 + Synapse + Delta Lake(Microsoft Fabricに統合) |
| Google Cloud | GCS + BigQuery(BigLakeで外部テーブル統合) |
| OCI | Object Storage + Autonomous DW + OCI Data Flow(Spark) |

## BI可視化ツール

分析結果を人が見るにはBI(Business Intelligence)ツールが必要です。

| ベンダー | BIツール | 特徴 |
| --- | --- | --- |
| AWS | [Amazon Quick Sight](https://aws.amazon.com/quick/) | Amazon Quick傘下のBI機能(旧QuickSight)。AIエージェントベースの自然言語クエリ、ダッシュボード、分析。Quick Desktopアプリからもアクセス可能 |
| Azure | [Power BI](https://powerbi.microsoft.com/) | 最も広いユーザー基盤、Excelフレンドリー、Copilot統合 |
| Google Cloud | [Looker / Looker Studio](https://cloud.google.com/looker) | LookMLベースのセマンティックレイヤー、Looker Studioは無料 |
| OCI | [OCI Analytics Cloud](https://docs.oracle.com/en-us/iaas/analytics-cloud/index.html) | Oracleネイティブ、セルフサービス可視化 |
| 3rd party | Tableau、Metabase、Apache Superset | ベンダー中立、マルチクラウド環境で有用 |

BIツールが重要な理由:
- SQLを知らないビジネスユーザーもデータ活用が可能
- ダッシュボードでリアルタイムモニタリング
- セルフサービス分析 → データチームのボトルネック解消

## 選択基準

| 基準 | 推奨 |
| --- | --- |
| インフラ管理の最小化 + クエリベース課金 | BigQuery |
| 既存AWSデータレイク(S3)との統合 | Redshift + Spectrum |
| SQL + Spark + BI統合プラットフォーム | Synapse / Microsoft Fabric |
| Oracle DBワークロード + 自動チューニング | OCI Autonomous DW |
| コスト予測可能性(固定容量) | Redshiftクラスタ / BigQueryスロット予約 |
| 断続的な分析(コスト最小化) | BigQueryオンデマンド / Redshift Serverless / Synapseサーバーレス |

## よくある間違い

- **運用DBで直接分析クエリを実行** — OLTPとOLAPを分離しないと分析クエリがトランザクション処理性能を低下させます。必ず分析専用プラットフォームに分離してください。
- **クエリスキャン量ベースの課金でSELECT *を乱用** — BigQueryなどスキャン量課金モデルで必要なカラムのみを指定しないと、コストが数十倍増加します。
- **データレイクにガバナンスなしでデータを蓄積** — スキーマ管理、アクセス制御、データカタログなしで蓄積すると「データスワンプ(Data Swamp)」になります。

## チェックリスト

- [ ] OLTP(運用)とOLAP(分析)のワークロードが物理的に分離されているか
- [ ] 分析プラットフォームの課金モデル(スキャン量/スロット/ノード)を理解し、コスト上限を設定したか
- [ ] データカタログとアクセス制御ポリシーが構成されているか

## 参考資料

### AWS

- [Amazon Redshift ドキュメント](https://docs.aws.amazon.com/redshift/latest/mgmt/welcome.html)
- [Amazon Quick ドキュメント](https://docs.aws.amazon.com/quick/latest/userguide/what-is.html)
- [Amazon Quick Desktop ダウンロード](https://aws.amazon.com/quick/download/)

### Azure

- [Azure Synapse Analytics ドキュメント](https://learn.microsoft.com/azure/synapse-analytics/)

### Google Cloud

- [Google BigQuery ドキュメント](https://cloud.google.com/bigquery/docs)

### OCI

- [OCI Autonomous Data Warehouse ドキュメント](https://docs.oracle.com/en-us/iaas/autonomous-database-serverless/index.html)

### 標準とコミュニティ

- [Apache Iceberg](https://iceberg.apache.org/)
- [Delta Lake](https://delta.io/)
