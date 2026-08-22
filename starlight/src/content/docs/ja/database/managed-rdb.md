---
title: "管理型RDB"
description: "管理型RDBとクラウドネイティブDBの違い、HA構成、PITRをベンダー別に比較します。"
---

> 文書基準: 2026年6月

## 概要

オンプレミスでデータベースを運用するには、サーバー設置、OSパッチ、DBエンジンのインストール、バックアップ設定、レプリケーション構成、フェイルオーバーをすべて自分で行う必要があります。**管理型RDB**は、この運用負担をベンダーが代行し、ユーザーはデータとクエリのみに集中できるようにします。

:::note
AWS RDSをご存知の方向けに: AzureはAzure SQL/Flexible Server、Google CloudはCloud SQL、OCIはAutonomous Databaseです。
:::

### DBAの役割の変化

| 領域 | オンプレミスDBA | 管理型RDB環境 |
| --- | --- | --- |
| OS/パッチ管理 | 自ら実施 | ベンダーが処理 |
| バックアップ/復旧 | スクリプト作成、テスト | 自動バックアップ + PITR内蔵 |
| HA/レプリケーション構成 | 自ら設計・運用 | マルチAZチェックボックス |
| 性能チューニング | クエリ + インフラ両方 | **クエリ/スキーマ最適化に集中** |
| 容量計画 | ディスク購入・拡張 | オンライン拡張または自動拡張 |

:::caution
特別な理由がなければ管理型を優先的に選択してください。VMに直接インストールするケースは、「管理型がサポートしていないエンジン/バージョン」「OSレベルのアクセスが必要」「BYOLライセンスコスト削減」など明確な要件がある場合です。
:::

:::note
DB選択後の運用 — スケーリングパターン、クエリ性能、キャッシュ、HA、バックアップ — は[データベース運用](../../database/operations/)を参照してください。
:::

## 製品比較

### 汎用管理型RDB

| ベンダー | 製品 | タイプ | サポートエンジン |
| --- | --- | --- | --- |
| AWS | RDS | 管理型 | MySQL、PostgreSQL、MariaDB、Oracle、SQL Server |
| AWS | Aurora | **ネイティブ** | MySQL/PostgreSQL互換。独自設計の分散ストレージ |
| Azure | Azure SQL Database | 管理型 | SQL Serverベース |
| Azure | Azure Database for MySQL/PostgreSQL | 管理型 | オープンソースエンジン管理型 |
| Google Cloud | Cloud SQL | 管理型 | MySQL、PostgreSQL、SQL Server |
| Google Cloud | AlloyDB | **ネイティブ** | PostgreSQL互換。独自設計。ベクトル検索内蔵 |
| OCI | Autonomous Database | **ネイティブ** | Oracle DBベース。自動チューニング/パッチ/スケーリング |
| OCI | MySQL HeatWave | 管理型 | MySQL互換。OLTP + OLAP統合処理 |

### クラウドネイティブDBとは

一般的な管理型(RDS、Cloud SQL)は既存のDBエンジンをそのまま使用しつつ運用のみを自動化したものです。Aurora、AlloyDBのような**クラウドネイティブDB**は、ストレージ層を独自設計しており根本的に異なるアーキテクチャを持ちます。

| 項目 | 一般管理型 | クラウドネイティブ |
| --- | --- | --- |
| **ストレージ** | インスタンスに接続されたブロックディスク | コンピューティングと分離された分散ストレージ |
| **レプリケーション** | 別インスタンスにデータ全体をコピー | ストレージ自体がマルチAZレプリケーション |
| **リードレプリカ追加** | データコピーが必要(遅い) | 同一ストレージ共有(速い) |
| **フェイルオーバー** | 待機インスタンスに切り替え(数十秒) | 新しいコンピューティング接続(数秒) |
| **容量** | ディスクサイズを事前指定 | 自動拡張 |

### グローバル分散DB

リージョンを越えて世界中にデータを分散し、各リージョンで読み書きが可能なDBです。一般的な管理型の「クロスリージョンリードレプリカ」とは異なり、**マルチリージョン書き込み**をサポートするサービスがあります。

| タイプ | ベンダー | 製品 | マルチリージョン書き込み | 一貫性 |
| --- | --- | --- | --- | --- |
| **RDB** | AWS | Aurora Global Database | — (読み取りのみ分散、書き込みは単一リージョン) | 強い一貫性(プライマリ) |
| **RDB** | Google Cloud | Spanner | サポート | 強い一貫性(グローバルトランザクション) |
| **NoSQL** | Azure | Cosmos DB | サポート | 5段階のレベル選択可能 |
| **NoSQL** | AWS | DynamoDB Global Tables | サポート | 結果整合性(リージョン間) |
| **RDB** | OCI | Autonomous Data Guard | — (クロスリージョンレプリケーション) | 強い一貫性(プライマリ) |

### グローバルDBが難しい理由

リージョン間のデータ同期は物理法則(光の速度)に制約されます。大陸間RTTは数百msに達するため、すべての書き込みを同期的にレプリケーションすると性能が大きく低下します。

| トレードオフ | 説明 |
| --- | --- |
| **強い一貫性 + マルチリージョン書き込み** | Spannerのみサポート。コスト非常に高い。TrueTime(原子時計)ベース |
| **結果整合性 + マルチリージョン書き込み** | DynamoDB Global Tables、Cosmos DB。競合解決戦略が必要 |
| **強い一貫性 + 単一リージョン書き込み** | Aurora Global DB。読み取りのみ分散。最もシンプルだが書き込み遅延が存在 |

:::caution
グローバルDBはコストが高く設計が複雑です。ほとんどのワークロードは以下の順序で検討してください:
1. 単一リージョンで十分か?(CDN + APIキャッシングで読み取り遅延を解決)
2. 読み取りのみ分散すればよいか?(クロスリージョンリードレプリカ)
3. 書き込みも分散する必要があるか?(グローバルDB — 競合解決/一貫性のトレードオフを受け入れる必要あり)
:::

## 主な違い

**AWS Aurora** — MySQL/PostgreSQL互換。ストレージが3つのAZに6つのコピーとして自動レプリケーションされます。Aurora Serverlessでアイドル時にコスト0が可能。

**Azure SQL Database** — SQL Serverベース。既存のSQL Serverワークロードを最も容易にマイグレーションできます。Hyperscaleティアで100TBまで拡張。

**Google Cloud AlloyDB** — PostgreSQL互換。ベクトル検索が内蔵されており、AIワークロードとの統合が強みです。

**OCI Autonomous Database** — Oracle DBベース。自動チューニング、自動パッチ、自動スケーリング。MySQL HeatWaveによるOLTP+OLAP統合処理もサポートします。

## Database@Cloud

Oracleは自社データベースを競合他社のデータセンター内に直接配置する戦略を推進しています。

| サービス | 配置場所 | 特徴 |
| --- | --- | --- |
| [Oracle Database@Azure](https://www.oracle.com/cloud/azure/) | Azure DC | Azure Portalからネイティブプロビジョニング |
| [Oracle Database@AWS](https://www.oracle.com/cloud/aws/) | AWS DC | AWSコンソールから直接プロビジョニング。Oracle Autonomous AI Database Serverless GA(2026.06)。DB@AWS全20リージョン |
| [Oracle Database@Google Cloud](https://www.oracle.com/cloud/google/) | Google Cloud DC | Google Cloudコンソールから直接使用 |

アプリとDBが同一データセンターにあるため、レイテンシ最小化、イグレスコストなし、データ主権の充足が可能です。

## いつ何を選ぶか

| 状況 | 推奨 |
| --- | --- |
| MySQL/PostgreSQL + 高可用性 + 自動ストレージ拡張 | AWS Aurora |
| 既存SQL Serverワークロードのマイグレーション | Azure SQL Database |
| PostgreSQL + AI/ベクトル検索統合 | Google Cloud AlloyDB |
| Oracle DB + 自動チューニング/パッチ | OCI Autonomous Database |
| アイドル時にコスト0(開発/テスト) | Aurora Serverless、Azure SQL Serverless |
| OLTP + OLAP統合MySQL | OCI MySQL HeatWave |

## よくある間違い

- **シングルAZ配置** — プロダクションDBを単一AZに配置すると、そのAZ障害時にサービスが完全に停止します。Multi-AZを必ず有効化してください。
- **バックアップの未テスト** — 自動バックアップを設定しても実際の復旧テストを行わないと、障害時に復旧が失敗したり想定より長くかかることがあります。
- **インデックスなしでの運用** — 適切なインデックスなしで運用すると、データ増加に伴いクエリ性能が急激に低下し、全テーブルスキャンによりDB負荷が増加します。

## チェックリスト

- [ ] Multi-AZ(または高可用性構成)を有効化したか
- [ ] 自動バックアップを設定し、復旧テストを実施したか
- [ ] スロークエリログを有効化しモニタリングしているか
- [ ] コネクションプーリング(RDS Proxy、PgBouncerなど)を設定したか

## 参考資料

### AWS

- [Amazon RDS ドキュメント](https://docs.aws.amazon.com/ko_kr/rds/)
- [Amazon Aurora ドキュメント](https://docs.aws.amazon.com/ko_kr/AmazonRDS/latest/AuroraUserGuide/)

### Azure

- [Azure SQL Database ドキュメント](https://learn.microsoft.com/ko-kr/azure/azure-sql/)
- [Azure Database for PostgreSQL ドキュメント](https://learn.microsoft.com/ko-kr/azure/postgresql/)

### Google Cloud

- [Cloud SQL ドキュメント](https://cloud.google.com/sql/docs)
- [AlloyDB ドキュメント](https://cloud.google.com/alloydb/docs)

### OCI

- [OCI Autonomous Database ドキュメント](https://docs.oracle.com/en-us/iaas/autonomous-database-serverless/index.html)
- [OCI MySQL HeatWave ドキュメント](https://docs.oracle.com/en-us/iaas/mysql-database/index.html)
