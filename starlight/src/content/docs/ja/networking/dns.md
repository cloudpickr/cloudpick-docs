---
title: "DNS"
description: "マネージドDNS、ルーティングポリシー、DNSSEC、Private DNSをベンダー別に比較します。"
---

> 文書基準: 2026年5月

## 概要

**DNS**（Domain Name System）は、ドメイン名（例: example.com）をIPアドレスに変換するサービスです。すべてのインターネット通信の最初のステップであるため、DNSが停止するとサービス全体にアクセスできなくなります。

オンプレミスではBINDやWindows DNSを直接運用しますが、クラウドマネージドDNSはグローバルAnycastネットワーク上で運用されるため、単一障害点がありません。AWS Route 53、Google Cloud Cloud DNS、Azure DNSはいずれも**100%可用性SLA**を提供しています。

:::note
DNSが停止すると、サービスURL自体が応答しなくなり、サービス全体にアクセスできなくなります。本番環境では**TTLを低く**維持し（300秒以下）、DNSフェイルオーバー時に迅速に伝播するようにしてください。
:::

単純な名前解決に加えて、地理的ルーティング、ヘルスチェックベースのフェイルオーバー、重み付け分散などのトラフィック管理機能を含みます。

## DNSレコードタイプ

よく使用されるDNSレコードタイプです。

| レコード | 用途 | 例 |
| --- | --- | --- |
| **A** | ドメインをIPv4アドレスにマッピング | `example.com → 93.184.216.34` |
| **AAAA** | ドメインをIPv6アドレスにマッピング | `example.com → 2606:2800:220:1:248:1893:25c8:1946` |
| **CNAME** | 別のドメイン名へのエイリアス接続 | `www.example.com → example.com` |
| **MX** | メールサーバーの指定（優先度を含む） | `example.com → 10 mail.example.com` |
| **TXT** | テキスト情報（SPF、DKIM、ドメイン所有権証明） | `v=spf1 include:_spf.google.com ~all` |
| **NS** | 該当ドメインの権威ネームサーバーの指定 | `example.com → ns1.example.com` |
| **SRV** | サービスの場所を指定（ポートを含む） | `_sip._tcp.example.com → 10 60 5060 sip.example.com` |
| **PTR** | IPをドメインに逆引きマッピング | `34.216.184.93.in-addr.arpa → example.com` |
| **ALIAS/ANAME** | CNAMEと類似だがルートドメインで使用可能 | AWS Alias、Azure Alias、Google Cloud独自のALIASレコードタイプ（Public Zone限定） |

### AWSのAliasレコードの特徴

AWS Route 53の**Alias Record**はCNAMEのように見えますが、DNSクエリではなくAWS内部で直接解決されるため、ルートドメイン（zone apex）にも使用可能で、コストもかかりません。ELB、CloudFront、S3ウェブサイトホスティングなどのAWSリソースを指す際に使用します。

## ホストゾーン（Public vs Private）

DNSホストゾーンは、ドメインのレコードを管理するコンテナです。**Public Zone**はインターネットからアクセス可能なレコードを、**Private Zone**はVPC/VNet内部でのみ解決されるレコードを管理します。

### Split-horizon DNS

同一ドメインに対して、リクエスト元によって異なるレコードを返すパターンです。

- 内部ユーザー（VPC内） → プライベートIPで応答
- 外部ユーザー（インターネット） → パブリックIPで応答

これにより、内部APIエンドポイントを外部に公開せずに同一ドメインを使用できます。

### ベンダー別実装

| ベンダー | Public Zone | Private Zone | Split-horizon |
| --- | --- | --- | --- |
| AWS | Route 53 Public Hosted Zone | Route 53 Private Hosted Zone（VPC接続） | Public/Private Zoneの分離で実装 |
| Azure | Azure Public DNS Zone | Azure Private DNS Zone（VNetリンク、自動登録） | Public/Private Zoneの分離 |
| Google Cloud | Cloud DNS Public Zone | Cloud DNS Private Zone（VPCバインディング） | ネイティブSplit-horizonサポート |
| OCI | OCI DNS Public Zone | OCI DNS Private Views（VCN接続） | DNS Viewsによる条件付き応答 |

### 活用シナリオ

- **ハイブリッド環境**: オンプレミス↔クラウド間の名前解決（条件付きフォワーディング）
- **マルチVPC**: 中央DNS管理 — 共有サービスVPCでPrivate Zoneを他のVPCに接続
- **セキュリティ分離**: 内部DB/APIエンドポイントを外部に公開せずに利便性の高い名前を使用

マルチクラウド環境でのDNS統合（条件付きフォワーディング、クロスベンダーリゾルビング）については、[マルチクラウドコネクティビティ — DNS統合戦略](../../networking/multicloud-connectivity/)を参照してください。

## 製品比較

| ベンダー | 製品 | ポジショニング |
| --- | --- | --- |
| AWS | Route 53 | ドメイン登録 + DNS + ヘルスチェック + ルーティングポリシーのオールインワン。100% SLA |
| Azure | Azure DNS + Traffic Manager | DNSホスティングとトラフィックルーティングが別サービスに分離。**100% SLA** |
| Google Cloud | Cloud DNS | 100% SLA。DNSSECを標準サポート。独自のヘルスチェックなし |
| OCI | OCI DNS | グローバルAnycast。Traffic Managementでルーティングポリシーを提供 |

### ルーティングポリシー

DNSレベルでトラフィックを制御できるルーティングポリシーです。

| ポリシー | 説明 | AWS Route 53 | Azure Traffic Manager | Google Cloud Cloud DNS | OCI DNS Traffic Management |
| --- | --- | --- | --- | --- | --- |
| **地理的** | ユーザーの位置に基づくルーティング | Geolocation / Geoproximity | Geographic | Geolocation | Geolocation Steering |
| **重み付け** | 比率ベースの分散（A/Bテスト、段階的デプロイ） | Weighted | Weighted | Weighted Round Robin | Load Balancer |
| **フェイルオーバー** | ヘルスチェック失敗時に代替エンドポイントへ切り替え | Failover | Priority | —（別途ヘルスチェック） | Failover |
| **レイテンシ** | 最も高速なリージョンへルーティング | Latency | Performance | — | — |
| **マルチバリュー** | 複数IPの返却 + ヘルスチェック | Multivalue Answer | — | — | — |

### ヘルスチェック

| ベンダー | 機能 | 備考 |
| --- | --- | --- |
| AWS | Route 53 Health Checks | HTTP/HTTPS/TCP。CloudWatchアラーム連携。障害時に自動DNS切り替え |
| Azure | Traffic Manager Probes | HTTP/HTTPS/TCP。エンドポイント監視 |
| Google Cloud | — | Cloud DNS独自のヘルスチェックなし。Cloud Load Balancingのヘルスチェックと組み合わせ |
| OCI | Health Checks | HTTP/HTTPS/TCP。DNS Traffic Managementと連携 |

## 主要な違い

- **AWS Route 53** — ドメイン登録からルーティングまでオールインワン。ルーティングポリシーが最も豊富です（Geoproximity、Multivalueなど）。
- **Azure** — DNSホスティング（Azure DNS）とグローバルトラフィックルーティング（Traffic Manager）が別サービスです。Traffic ManagerはDNSベースのグローバルロードバランサーの役割を果たします。
- **Google Cloud Cloud DNS** — DNSSECの標準サポート、Split-horizonのネイティブサポートが強みです。独自のヘルスチェックがないため、フェイルオーバーはCloud Load Balancingと組み合わせる必要があります。
- **OCI DNS** — Traffic Managementで地理的ルーティング、フェイルオーバーなどのポリシーを提供し、Health Checksと連携して自動DNS切り替えが可能です。

## DNSSEC

**DNSSEC**（DNS Security Extensions）は、DNS応答の改ざんを防止するセキュリティ拡張です。攻撃者がDNS応答を傍受して悪意のあるサイトへ誘導するDNSスプーフィング/キャッシュポイズニングを防ぎます。

| ベンダー | サポートレベル |
| --- | --- |
| AWS Route 53 | DNSSEC署名および登録に対応 |
| Azure DNS | DNSSEC署名に対応 |
| Google Cloud Cloud DNS | DNSSEC署名に対応（デフォルト有効化オプションあり） |
| OCI DNS | DNSSEC署名に対応 |

## よくある間違い

- **TTLを長く設定（例: 86400秒）したままフェイルオーバーを構成** — DNS切り替えが伝播するまで最大24時間かかります。フェイルオーバーが必要なレコードはTTL 300秒以下に設定してください。
- **ルートドメイン（zone apex）にCNAMEを使用** — DNS標準違反であり動作しません。AWS Alias、Azure Alias、Google Cloud ALIASレコードを使用してください。
- **ヘルスチェックなしでFailoverルーティングを設定** — 障害が発生しても切り替わりません。ルーティングポリシーとヘルスチェックは必ず併せて構成してください。

## チェックリスト

- [ ] 本番ドメインのTTLがフェイルオーバー要件に合わせて設定されているか（推奨: 300秒以下）?
- [ ] ヘルスチェックが構成されており、障害時に自動DNS切り替えが動作するか?
- [ ] DNSSECが有効化されており、DNSスプーフィング/キャッシュポイズニングを防止しているか?

## 関連ドキュメント

> 📄 [ロードバランサー](../../networking/load-balancer/)

> 📄 [CDN](../../networking/cdn/)

> 📄 [マルチクラウドコネクティビティ](../../networking/multicloud-connectivity/)

## 参考資料

### AWS

- [Amazon Route 53ドキュメント](https://docs.aws.amazon.com/ko_kr/route53/)
- [Route 53ルーティングポリシー](https://docs.aws.amazon.com/ko_kr/Route53/latest/DeveloperGuide/routing-policy.html)
- [Route 53ヘルスチェック](https://docs.aws.amazon.com/ko_kr/Route53/latest/DeveloperGuide/health-checks-creating.html)

### Azure

- [Azure DNSドキュメント](https://learn.microsoft.com/ko-kr/azure/dns/)
- [Azure Traffic Managerドキュメント](https://learn.microsoft.com/ko-kr/azure/traffic-manager/)
- [Azure DNS SLA（100%）](https://azure.microsoft.com/en-us/support/legal/sla/dns/v1_1/)

### Google Cloud

- [Cloud DNSドキュメント](https://cloud.google.com/dns/docs)
- [Cloud DNS ALIASレコードの概要](https://cloud.google.com/dns/docs/records-overview)

### OCI

- [OCI DNSドキュメント](https://docs.oracle.com/en-us/iaas/Content/DNS/home.htm)
