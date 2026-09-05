---
title: "キャッシュとインメモリデータベース"
description: "インメモリキャッシュの概念、キャッシュパターン、ベンダー別マネージドサービスを比較します。"
---

> 文書基準: 2026年8月

## 概要

データベース照会はディスクI/Oが発生するため数ミリ秒〜数十ミリ秒かかります。**インメモリキャッシュ**は頻繁に参照されるデータをメモリに保存し、応答時間をマイクロ秒単位に短縮します。

:::note
キャッシュ運用時に注意すべきアンチパターン(永続ストレージのように使用、TTL未設定、キャッシュ依存アーキテクチャなど)は、[データベース運用 — キャッシュアンチパターン](../../database/operations/#キャッシュ運用時の注意事項)を参照してください。
:::

## キャッシュパターン

| パターン | 動作 | 適した場合 |
| --- | --- | --- |
| **Cache-Aside** | アプリがキャッシュ確認 → ミス時にDB照会 → キャッシュ保存 | 読み取り中心、最も一般的 |
| **Write-Through** | アプリがキャッシュに書き込み → キャッシュがDBに同期書き込み | 整合性が重要、書き込み遅延許容 |
| **Write-Behind** | アプリがキャッシュに書き込み → キャッシュが非同期でDBに書き込み | 書き込み性能が重要、一時的な不整合許容 |
| **Read-Through** | キャッシュがDB照会を代行 | キャッシュライブラリがDB連携をサポートする場合 |

## ベンダー別サービス比較

| ベンダー | サービス | エンジン | 特徴 |
| --- | --- | --- | --- |
| AWS | [ElastiCache for Valkey](https://docs.aws.amazon.com/elasticache/) | Valkey(Redisフォーク) | **基本推奨**。Serverlessオプション。ベクトル検索サポート |
| AWS | [ElastiCache for Redis](https://docs.aws.amazon.com/elasticache/) | Redis | 既存ワークロード互換用 |
| AWS | [MemoryDB for Valkey](https://docs.aws.amazon.com/memorydb/) | Valkey | 耐久性保証(ディスク永続化)。プライマリDBとして使用可能 |
| Azure | [Azure Cache for Redis](https://learn.microsoft.com/azure/azure-cache-for-redis/) | Redis | Enterpriseティア(Redis Enterpriseベース) |
| Google Cloud | [Memorystore for Valkey](https://cloud.google.com/memorystore/docs) | Valkey | **基本推奨**。Clusterモード、自動フェイルオーバー |
| Google Cloud | [Memorystore for Redis](https://cloud.google.com/memorystore/docs) | Redis | 既存互換用 |
| OCI | [OCI Cache](https://docs.oracle.com/en-us/iaas/Content/ocicache/home.htm) | Redis互換 | マネージドRedisクラスタ |

:::note
**Valkeyとは?** Redisが2024年にライセンスを変更(BSD → SSPL/RSALv2)したことで、Linux Foundation傘下でオープンソースフォークとして誕生したプロジェクトです。既存のRedisクライアントと互換性があり、AWSとGoogle Cloudが基本エンジンとして採用しています。新規プロジェクトはValkeyベースを推奨します。
:::

## Valkey/Redis vs Memcached

| 項目 | Valkey/Redis | Memcached |
| --- | --- | --- |
| **データ構造** | String、Hash、List、Set、Sorted Set、Stream | Stringのみ(key-value) |
| **永続性** | RDB/AOFスナップショット可能 | なし(純粋なキャッシュ) |
| **レプリケーション/HA** | レプリカ + 自動フェイルオーバー | なし(クライアントシャーディング) |
| **Pub/Sub** | サポート | 非サポート |
| **適した場合** | セッションストア、リーダーボード、リアルタイム分析、Pub/Sub | シンプルなキャッシュ、大容量オブジェクトキャッシング |

## いつ何を選ぶか

| 要件 | 推奨 |
| --- | --- |
| DB読み取り負荷分散(一般的なキャッシュ) | ElastiCache/Memorystore Valkey (またはRedis) (Cache-Aside) |
| セッションストア(TTL + 構造化データ) | Valkey / Redis(Hashタイプ) |
| プライマリDBの代替(耐久性が必要) | MemoryDB for Valkey |
| シンプルなkey-value、最大スループット | Memcached |
| リアルタイムリーダーボード/カウンター | Valkey / Redis(Sorted Set) |

## よくある間違い

- **キャッシュを永続ストレージのように使用** — キャッシュはいつでも消える可能性があります。オリジナルデータなしでキャッシュのみに保存すると、障害時にデータが失われます。
- **すべてのキーにTTLを設定しない** — TTLなしでキャッシュすると、データが永遠に残りDBとの不整合が発生し、メモリが枯渇します。
- **キャッシュ障害時のfallbackを実装しない** — キャッシュ依存アーキテクチャでキャッシュがダウンすると、サービス全体が停止します。キャッシュミス時のDB直接照会経路を必ず確保してください。

## チェックリスト

- [ ] すべてのキャッシュキーにビジネス要件に合ったTTLが設定されているか
- [ ] キャッシュ障害時にDB直接照会へのfallback経路が実装されているか
- [ ] キャッシュメモリ使用量のモニタリングとeviction戦略(LRU/LFU)を確認したか

## 参考資料

### オープンソース

- [Valkey 公式サイト](https://valkey.io/) — Linux Foundation傘下のRedisフォーク
- [Valkey GitHub](https://github.com/valkey-io/valkey)

### AWS

- [Amazon ElastiCache ドキュメント](https://docs.aws.amazon.com/elasticache/)
- [Amazon MemoryDB ドキュメント](https://docs.aws.amazon.com/memorydb/)

### Azure

- [Azure Cache for Redis ドキュメント](https://learn.microsoft.com/azure/azure-cache-for-redis/)

### Google Cloud

- [Memorystore ドキュメント](https://cloud.google.com/memorystore/docs)

### OCI

- [OCI Cache ドキュメント](https://docs.oracle.com/en-us/iaas/Content/ocicache/home.htm)
