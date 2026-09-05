---
title: "検索とログ分析"
description: "全文検索、ベクトル検索、ログ分析サービスをベンダー別に比較します。"
---

> 文書基準: 2026年8月

## 概要

### 実務で検索が必要な場面

| 使用事例 | 説明 | なぜDBのLIKE/WHEREでは不十分か |
| --- | --- | --- |
| 製品/コンテンツ検索 | ECサイトの商品検索、社内文書検索 | 形態素解析、類義語、ランキングが必要 |
| ログ/アクセスログ分析 | 数億件のログからエラーパターンを見つける | RDBは大量テキストスキャンに不向き |
| セキュリティイベント検知 (SIEM) | 異常パターンをリアルタイム検知 | 時系列 + 全文検索 + 集計の組み合わせ |
| AI質問応答 (RAG) | ユーザーの質問と意味的に類似する文書を探す | キーワードマッチングでは意味の把握が不可能 |
| オートコンプリート/レコメンド | 入力中のリアルタイム提案 | ms単位の応答 + prefixマッチング + 人気度反映 |

### 検索方式比較 — キーワード vs セマンティック vs ハイブリッド

| 方式 | 動作原理 | 長所 | 短所 |
| --- | --- | --- | --- |
| **キーワード (BM25)** | 逆インデックス + TF-IDF/BM25スコアリング | 正確な用語マッチング、高速、予測可能 | 「自動車」で検索しても「車両」を見つけられない |
| **セマンティック (ベクトル)** | テキストを埋め込みベクトルへ変換 → コサイン類似度 | 意味ベース、類義語/多言語対応 | 正確な固有名詞/コード検索に弱い |
| **ハイブリッド** | キーワード + ベクトルの結果を組み合わせ (RRFなど) | 両方の長所を組み合わせ | 複雑さが増し、チューニングが必要 |

ベクトル検索の詳細は[ベクトルストア](../../ai/vector-store/)を参考にしてください。

### 技術系譜

```
Apache Lucene (検索エンジンライブラリ)
  ├─ Apache Solr (2004~, 独立した検索サーバー)
  └─ Elasticsearch (2010~, 分散検索 + 分析)
       └─ OpenSearch (2021~, AWSフォーク, Apache 2.0ライセンス)
```

- **Solr**: 依然として使用されていますが、クラウド管理型サービスがほとんどありません。オンプレミスのレガシーに残っているケースが多い
- **Elasticsearch**: Elastic社がライセンスを変更 (SSPL)。Elastic Cloudで管理型を提供
- **OpenSearch**: AWSがフォーク。クラウド管理型の主流。Valkeyと似た文脈 (ライセンス問題 → オープンソースフォーク)

### ログ分析がなぜ「検索」なのか

ログ分析の核心は**大量の非構造化テキストからパターンを見つけること**です。全文検索エンジン(逆インデックス)がこの作業に適しているため、ELK/EFKスタック(Elasticsearch + Logstash/Fluentd + Kibana)がログ分析の事実上の標準となりました。

### 検索タイプまとめ

「検索」は用途によって全く異なるサービスを使用します。

| 種類 | 目的 | 代表的な技術 |
| --- | --- | --- |
| **全文検索** (Full-text) | テキストキーワードマッチング、形態素解析 | Elasticsearch/OpenSearch, Solr |
| **ベクトル検索** (Semantic) | 意味ベースの類似度検索 (AI/RAG) | ベクトルDB, pgvector |
| **ログ分析** | 大量ログの収集・検索・可視化 | OpenSearch, Loki, BigQuery |

この文書は全文検索とログ分析に焦点を当てます。

## ベンダー別サービス比較

| ベンダー | 全文検索 | AI検索 (ハイブリッド) | ログ分析 |
| --- | --- | --- | --- |
| AWS | [OpenSearch Service](https://docs.aws.amazon.com/opensearch-service/) | OpenSearch + k-NN | [CloudWatch Logs Insights](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/) |
| Azure | [Azure AI Search](https://learn.microsoft.com/azure/search/) | AI Search (ベクトル + キーワード + セマンティック) | [Log Analytics](https://learn.microsoft.com/azure/azure-monitor/logs/data-platform-logs) |
| Google Cloud | — (Firestore全文検索は限定的) | [Vertex AI Search](https://cloud.google.com/generative-ai-app-builder/docs) | [Cloud Logging](https://cloud.google.com/logging/docs) + [BigQuery](https://cloud.google.com/bigquery/docs) |
| OCI | [OCI Search with OpenSearch](https://docs.oracle.com/en-us/iaas/Content/search-opensearch/home.htm) | OpenSearch + k-NN | [OCI Logging Analytics](https://docs.oracle.com/en-us/iaas/logging-analytics/home.htm) |

## いつ何を選ぶべきか

| 要件 | 推奨 |
| --- | --- |
| 製品カタログ検索 (キーワード + フィルター) | OpenSearch, Azure AI Search |
| AIベースの質問応答 (RAG) | [ベクトルストア](../../ai/vector-store/) + ハイブリッド検索 |
| 大量ログ検索 + ダッシュボード | OpenSearch (Dashboards), Log Analytics, Cloud Logging |
| コスト最小化のログ長期保管 + クエリ | S3 + Athena, BigQuery, OCI Object Storage + Logging Analytics |
| 多言語・CJK形態素解析が必要 | OpenSearch (kuromoji, noriプラグイン), Azure AI Search (言語別アナライザー) |

## よくある間違い

- **RDBのLIKE検索で全文検索を代替しようとする** — データが増えるとフルテーブルスキャンで性能が急激に低下します。全文検索が必要な場合は検索エンジンを導入してください。
- **シャード数を過度に設定** — OpenSearch/Elasticsearchでシャードが多すぎるとクラスターのオーバーヘッドが増加します。シャードあたり10〜50GBを基準に設計してください。
- **ログ保存期間を無制限に設定** — 検索エンジンにすべてのログを永久保管すると、ストレージコストが急増します。ホット/ウォーム/コールドティアを活用し、古いログはオブジェクトストレージへ移管してください。

## チェックリスト

- [ ] 検索要件(キーワード/セマンティック/ハイブリッド)を定義し、適切なサービスを選択したか
- [ ] インデックスライフサイクルポリシー(ILM)とログ保存期間を設定したか
- [ ] 多言語（CJKなど）検索が必要な場合、適切な形態素解析器（kuromoji、noriなど）を構成したか

## 参考資料

### AWS

- [Amazon OpenSearch Service 文書](https://docs.aws.amazon.com/opensearch-service/)
- [CloudWatch Logs Insights](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/)

### Azure

- [Azure AI Search 文書](https://learn.microsoft.com/azure/search/)
- [Log Analytics 文書](https://learn.microsoft.com/azure/azure-monitor/logs/data-platform-logs)

### Google Cloud

- [Vertex AI Search 文書](https://cloud.google.com/generative-ai-app-builder/docs)
- [Cloud Logging 文書](https://cloud.google.com/logging/docs)

### OCI

- [OCI Search with OpenSearch](https://docs.oracle.com/en-us/iaas/Content/search-opensearch/home.htm)
- [OCI Logging Analytics](https://docs.oracle.com/en-us/iaas/logging-analytics/home.htm)
