---
title: "データベース運用"
description: "RDB拡張パターン、NoSQLキー設計、キャッシュ運用、スロークエリ管理、HA/バックアップを扱います。"
---

> 文書基準: 2026年8月

## 概要

クラウド管理型DBはインフラ運用(パッチ、バックアップ、HA)を自動化しますが、**データ設計とクエリ性能は自動的には良くなりません。** この文書は、DBを選択した後の運用段階で知っておくべき主要なトピックを扱います。

:::note
DB選択ガイドは[マネージドRDB](../../database/managed-rdb/)、[NoSQL](../../database/nosql/)、[キャッシュ](../../database/cache/)を参考にしてください。この文書は「選択した後どう運用するか」に焦点を当てます。
:::

## RDB拡張パターン

RDBはNoSQLと異なり、水平拡張(シャーディング)が困難です。ほとんどの拡張は**読み取り分散**によって行われます。

| 段階 | 方法 | 効果 | 例 |
| --- | --- | --- | --- |
| 1. **垂直拡張** | インスタンスタイプのアップグレード (CPU/メモリ増強) | 最も単純。限界あり | db.r5.large → db.r5.4xlarge |
| 2. **読み取りレプリカ** | 読み取りトラフィックをレプリカへ分散 | 読み取り80%以上のワークロードに効果的 | 商品一覧照会をレプリカで処理 |
| 3. **キャッシュ層** | よく読み取られるデータをキャッシュ(Redis/Valkey)に格納 | DB負荷を大幅に削減。ミリ秒応答 | セッション、人気商品、設定値をキャッシュ |
| 4. **CQRS** | 書き込み(Command)と読み取り(Query)のDBを分離 | それぞれ独立して最適化可能 | 注文の書き込みはRDB、検索/ダッシュボードは別の読み取りDB |
| 5. **シャーディング** | データを複数のDBに分散格納 | 最後の手段。アプリの複雑さが急増 | ユーザーID基準でDBを分割 |

:::note
ほとんどのWebサービスは読み取りが80～90%です。読み取りレプリカ + キャッシュの組み合わせでRDB負荷の大部分を解決できます。
:::

## クエリ性能管理

| 問題 | 症状 | 対応 |
| --- | --- | --- |
| **無分別なJOIN** | 多数のテーブルJOIN時に応答が数秒以上かかる | 読み取りレプリカの分離、非正規化、DWへの分析クエリ移管 |
| **インデックス未設計** | フルテーブルスキャン。データ増加に伴い次第に遅くなる | 実行計画(EXPLAIN)の確認、クエリパターンに合わせたインデックス追加 |
| **スロークエリの放置** | 特定のクエリがDB全体の性能を低下させる | スロークエリログの有効化、定期レビュー、クエリのリファクタリング |
| **DBをストレージのように使用** | ログ/イベントをRDBに無制限に蓄積 | 時系列データはオブジェクトストレージ/時系列DBへ分離 |

:::caution
OLTP(トランザクション)とOLAP(分析)を同じDBで処理すると、互いの性能を圧迫します。分析クエリが増えてきたら[データ分析プラットフォーム](../../database/analytics/)へ分離してください。
:::

### インデックス設計の基本

**カーディナリティ(Cardinality)**: カラムに含まれる固有値の数です。ユーザーID(数百万個)はカーディナリティが高く、性別(2個)は低いです。カーディナリティが高いカラムにインデックスを設定すると効果が大きくなります。

| 原則 | 説明 |
| --- | --- |
| **WHERE句基準** | 頻繁にフィルタリングするカラムにインデックス |
| **カーディナリティの確認** | 固有値が多いカラムほどインデックス効果が大きい。booleanのような低カーディナリティは効果なし |
| **複合インデックスの順序** | 最も選択性の高い(カーディナリティの高い)カラムを前方に配置 |
| **カバリングインデックス** | SELECTカラムまでインデックスに含めればテーブルアクセスなしで応答可能 |
| **過度なインデックスに注意** | インデックスが多いと書き込み性能が低下。読み取り/書き込み比率を考慮 |

:::note
インデックス追加前には必ず`EXPLAIN`(実行計画)で現在のクエリがどう動作するか確認してください。フルテーブルスキャンが発生するクエリから優先的に改善します。
:::

## 高可用性 (HA)

| 方式 | 動作 | RPO | RTO | コスト | 適した場合 |
| --- | --- | --- | --- | --- | --- |
| **マルチAZ同期レプリケーション** | 同一リージョン内の複数AZへ同期レプリケーション。自動フェイルオーバー | 0 | 数十秒〜数分 | 中間 (待機インスタンスコスト) | プロダクション基本 |
| **読み取りレプリカ** | 非同期レプリケーション。読み取り分散 + 手動昇格でDR可能 | 数秒 (レプリケーション遅延) | 数分 (手動昇格) | 低い | 読み取り負荷分散 + 簡易DR |
| **クロスリージョンレプリケーション** | 別リージョンへ非同期レプリケーション。リージョン障害対策 | 数秒〜数分 | 数分 (手動昇格) | 高い (リージョン間転送) | リージョン障害DR |

### ベンダー別HAサービス

| 機能 | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- |
| **マルチAZ同期** | RDS Multi-AZ, Auroraストレージレプリケーション | Zone-redundant HA | Cloud SQL HA | ADB自動HA |
| **読み取りレプリカ** | Aurora Read Replica | Read Replica | Cloud SQL Read Replica | ADB Read-only Replica |
| **クロスリージョン** | Aurora Global Database | Geo-replication | Cross-Region Replica | Autonomous Data Guard |

## バックアップとPITR

| ベンダー | バックアップ保持期間 | PITR |
| --- | --- | --- |
| AWS RDS / Aurora | 最大35日 | 秒単位の復旧 |
| Azure SQL Database | 最大35日 | 秒単位の復旧 |
| Google Cloud Cloud SQL / AlloyDB | 最大365日 | 秒単位の復旧 |
| OCI Autonomous Database | 最大60日 | 秒単位の復旧 |

:::note
バックアップ戦略とDR構成の詳細は[バックアップと復旧](../../storage/backup/)、[災害復旧](../../governance/dr/)を参考にしてください。
:::

## コネクションプール管理

DBコネクションは有限のリソースです。特にサーバーレス/オートスケーリング環境でインスタンスが急増すると、コネクションが爆発的に増加します。

| 問題 | 対応 |
| --- | --- |
| コネクション枯渇 | コネクションプーラー(RDS Proxy, Cloud SQL Auth Proxy, PgBouncer)を使用 |
| サーバーレス関数の同時実行数爆発 | Reserved Concurrencyで制限 + コネクションプーラーが必須 |
| アイドルコネクションの占有 | idle timeoutの設定、コネクションの再利用 |

## NoSQLキー設計のアンチパターン

NoSQLはRDBと異なり、**クエリパターンを先に決めてからキーを設計**する必要があります。運用中によく発生する症状(ホットパーティション、スロットリング)は、設計段階でのキー設計ミスに起因します。

:::note
キー設計パターンと原則は[NoSQLデータベース — キー設計パターン](../../database/nosql/)を参考にしてください。
:::

## キャッシュ運用

キャッシュはDB負荷を減らす主要なツールですが、運用時には固有の注意点があります。

:::note
キャッシュパターンの定義(Cache-Aside, Write-Through, Write-Behindなど)とベンダー別サービス比較は[キャッシュ](../../database/cache/)を参考にしてください。
:::

### キャッシュ運用時の注意事項

- **キャッシュスタンピード** — TTL満了時に数百のリクエストが同時にDBへ殺到。ランダムTTLジッターまたはロックベースの更新で防止
- **キャッシュウォームアップ** — デプロイ/再起動直後にキャッシュが空でDB負荷が急増。事前ウォーミングスクリプトが必要
- **メモリ管理** — キャッシュメモリ超過時のeviction方針(LRU, LFU)を確認。重要なデータが押し出されないように
- **キャッシュを永続ストレージのように使用しない** — キャッシュはいつでも消える可能性がある前提で設計。原本は必ずDBに
- **すべてのキーにTTLを設定** — TTLなしでキャッシュするとデータが永遠に残りDBと不整合が発生

## よくある間違い

- **EXPLAINなしでインデックスを追加** — 実行計画を確認せずにインデックスを追加すると、書き込み性能だけが低下し読み取り改善効果がない場合があります。
- **サーバーレス環境でコネクションプーラーなしで運用** — Lambda/Functionsの同時実行数が急増するとDBコネクションが枯渇します。RDS Proxyなどのコネクションプーラーを必ず使用してください。
- **バックアップは設定したが復旧テストをしない** — バックアップがあっても復旧手順を検証しないと、実際の障害時に復旧に失敗する可能性があります。

## チェックリスト

- [ ] スロークエリログを有効化し、定期的にレビューするプロセスがあるか
- [ ] マルチAZまたは読み取りレプリカで高可用性が構成されているか
- [ ] PITR(Point-in-Time Recovery)復旧を実際にテストしたことがあるか

## 関連ドキュメント

- [マネージドRDB](../../database/managed-rdb/) — DB選択ガイド
- [NoSQL](../../database/nosql/) — NoSQL選択ガイド
- [キャッシュとインメモリ](../../database/cache/) — キャッシュ選択ガイド

## 参考資料

### AWS

- [Amazon RDS ユーザーガイド](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Welcome.html)
- [Amazon Aurora ユーザーガイド](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/CHAP_AuroraOverview.html)
- [Amazon RDS Proxy](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-proxy.html)
- [RDS リードレプリカの操作](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ReadRepl.html)

### Azure

- [Azure Database for PostgreSQL ドキュメント](https://learn.microsoft.com/azure/postgresql/)
- [Azure SQL Database 高可用性](https://learn.microsoft.com/azure/azure-sql/database/high-availability-sla)
- [Azure SQL Database 読み取りスケールアウト(リードレプリカ)](https://learn.microsoft.com/azure/azure-sql/database/read-scale-out)

### Google Cloud

- [Cloud SQL 高可用性の概要](https://cloud.google.com/sql/docs/postgres/high-availability)
- [Cloud SQL リードレプリカ](https://cloud.google.com/sql/docs/postgres/replication)
- [Cloud SQL Auth Proxy](https://cloud.google.com/sql/docs/postgres/sql-proxy)

### OCI

- [OCI Autonomous Database ドキュメント](https://docs.oracle.com/en-us/iaas/autonomous-database/index.html)
- [Autonomous Data Guard](https://docs.oracle.com/en-us/iaas/autonomous-database-serverless/doc/autonomous-data-guard.html)

### 標準・ツール

- [PostgreSQL EXPLAIN ドキュメント](https://www.postgresql.org/docs/current/sql-explain.html)
- [PgBouncer — 軽量コネクションプーラー](https://www.pgbouncer.org/)
