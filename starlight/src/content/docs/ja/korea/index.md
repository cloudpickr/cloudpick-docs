---
title: "韓国付録"
description: "韓国環境に特化したガイド — CSAP、網分離、ソブリンAI政策、国産FMプロバイダー"
---

> 文書基準: 2026年8月

## 概要

本セクションでは、韓国市場でクラウドを導入・運用する際に直面する規制とエコシステムを扱います。これまでのベンダー中立ドキュメントがグローバル共通のアーキテクチャを扱ってきたのに対し、この付録では韓国固有の法制度・供給者環境に焦点を当てます。

エンタープライズアーキテクトが公共・金融分野でクラウドを導入する際、あるいは生成AIを国内の規制環境に合わせて導入する際に参考にできるよう構成しています。

## 韓国リージョン現況

| ベンダー | リージョンコード | AZ/Zone数 | リリース時期 |
| --- | --- | --- | --- |
| AWS | `ap-northeast-2`（ソウル） | 4つのAZ | 2016年 |
| Azure | `koreacentral`（ソウル）、`koreasouth`（釜山） | 3つのAZ（Central） | 2017年 |
| Google Cloud | `asia-northeast3`（ソウル） | 3つのZone | 2020年 |
| OCI | `ap-seoul-1`、`ap-chuncheon-1` | 3 FD | 2020年 |

:::note
Azure（ソウル-釜山）とOCI（ソウル-春川）は国内に2つのリージョンを保有しているため、データが国外に出ないDR構成が可能です。AWS/Google Cloudは東京・大阪が最も近いDR候補です。リージョンの概念は[リージョンと可用性ゾーン](../../about-cloud/regions-and-zones/)を参照してください。
:::

### 韓国リージョン基準のDR構成

| ベンダー | プライマリ | セカンダリ候補 | レイテンシ | 備考 |
| --- | --- | --- | --- | --- |
| AWS | `ap-northeast-2`（ソウル） | `ap-northeast-1`（東京）、`ap-northeast-3`（大阪） | 約30〜50ms | 国外移転 |
| Azure | `koreacentral`（ソウル） | `koreasouth`（釜山） | 約5ms | **国内DR可能** |
| Azure | `koreacentral`（ソウル） | `japaneast`（東京） | 約30ms | 国外移転 |
| Google Cloud | `asia-northeast3`（ソウル） | `asia-northeast1`（東京）、`asia-northeast2`（大阪） | 約30〜50ms | 国外移転 |
| OCI | `ap-seoul-1`（ソウル） | `ap-chuncheon-1`（春川） | 約5ms | **国内DR可能** |
| OCI | `ap-seoul-1`（ソウル） | `ap-tokyo-1`（東京） | 約30ms | 国外移転 |

:::caution
国外リージョンをDR対象として使用する場合、韓国の個人情報保護法・信用情報法に基づくデータの国外移転要件を満たす必要があります。DR戦略のタイプは[災害復旧（DR）](../../governance/dr/)を参照してください。
:::

### 韓国の専用接続・コミュニティ

専用接続（Direct Connect / ExpressRoute / Interconnect / FastConnect）の韓国PoPはKINX、LG U+が代表的です。マルチクラウドのCloud Exchangeは[KINX Cloud Hub](https://www.kinx.net/service/cloud/)、Megaport（ソウルPoP）、Equinix Fabric（ソウルDC）を検討します。概念は[マルチクラウドネットワーキング](../../networking/multicloud-networking/)を参照してください。

ローカルユーザーコミュニティ: [AWSKRUG](https://www.awskr.org/)、[GDG Cloud Korea](https://gdg.community.dev/gdg-cloud-korea/)。

公共・金融の大型プロジェクトでは、サムスンSDS、LG CNS、SK C&Cなどの現地SIが全体システムを構築し、製品会社のFDEは自社AI/SaaS統合を担当する協業構造が一般的です。

## 取り扱うトピック

### セキュリティ・規制

- **[コンプライアンス（韓国）](../korea/governance/compliance/)** — ISMS-P、CSAP、金融業界規制など、韓国固有の認証・規制体系を一覧で整理し、各詳細ドキュメントへ案内します。
- **[CSAP（クラウドセキュリティ認証）](../korea/security/csap/)** — 公共機関のクラウド導入における必須要件であるCSAP制度の等級体系、ハイパースケーラー・国内CSPの認証状況、2027年に予定されている国家情報院の単一検証体系への改編を整理します。
- **[網分離とネットワーク隔離](../korea/security/network-isolation/)** — 金融・公共分野の網分離規制、2024年以降進められている金融分野の網分離改善ロードマップ、そして国家網セキュリティ体系（N²SF）への移行がクラウド・SaaS・生成AI導入に与える影響を扱います。

### AI・ソブリン政策

- **[ソブリンFM政策](../korea/ai/sovereign-fm-policy/)** — 科学技術情報通信部の独自AI基盤モデルプロジェクト、精鋭チーム選定の経緯、および企業アーキテクトの観点からの示唆を整理します。
- **[FMプロバイダー比較](../korea/ai/fm-providers/)** — NAVER、LG AI研究院、カカオ、KT、Upstage、NC AIなど、国内の基盤モデルプロバイダーの最新モデル・ライセンス・提供チャネルを比較します。

:::note
本セクションの内容は、急速に変化する政策・規制の状況を扱っています。各ドキュメント下部の「参考資料」セクションに記載の出典を通じて、最新の公式発表を直接ご確認いただくことを推奨します。
:::

## 関連ドキュメント

> 📄 [データ保護とワークロードセキュリティ](../security/data-protection/)

> 📄 [ソブリンランディングゾーン](../governance/landing-zone/)
