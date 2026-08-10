---
title: "韓国市場・インフラ現況"
description: "韓国リージョン現況、国内DR構成、データ主権、専用接続PoP、MSP・コミュニティなど韓国市場のクラウドインフラ・エコシステムを整理します。"
---

> 文書基準: 2026年8月

## 概要

グローバル4大CSPはいずれもソウルにリージョンを運営しており、一部ベンダーは国内2リージョンでデータが国外に出ないDR構成をサポートしています。本文書では、ベンダー中立ドキュメントでは扱わない韓国特化のインフラ・エコシステム情報 — リージョン現況、国内DRの組み合わせ、専用接続PoP、MSP・コミュニティ — を整理します。

## 韓国リージョン現況

| ベンダー | リージョンコード | AZ/Zone数 | リリース時期 |
| --- | --- | --- | --- |
| AWS | `ap-northeast-2`（ソウル） | 4つのAZ | 2016年 |
| Azure | `koreacentral`（ソウル）、`koreasouth`（釜山） | 3つのAZ（Central） | 2017年 |
| Google Cloud | `asia-northeast3`（ソウル） | 3つのZone | 2020年 |
| OCI | `ap-seoul-1`（ソウル）、`ap-chuncheon-1`（春川） | 3 FD | 2020年 |

:::note
Azure（ソウル-釜山）とOCI（ソウル-春川）は国内に2つのリージョンを保有しているため、データが国外に出ないDR構成が可能です。AWS/Google Cloudは東京・大阪が最も近いDR候補です。リージョン・AZの概念は[リージョンと可用性ゾーン](../../about-cloud/regions-and-zones/)を参照してください。
:::

## 韓国リージョン基準のDR構成

| ベンダー | プライマリ（韓国） | セカンダリ候補 | レイテンシ | 備考 |
| --- | --- | --- | --- | --- |
| AWS | `ap-northeast-2`（ソウル） | `ap-northeast-1`（東京）、`ap-northeast-3`（大阪） | 約30〜50ms | 国外移転 |
| Azure | `koreacentral`（ソウル） | `koreasouth`（釜山） | 約5ms | **国内DR可能** |
| Azure | `koreacentral`（ソウル） | `japaneast`（東京） | 約30ms | 国外移転 |
| Google Cloud | `asia-northeast3`（ソウル） | `asia-northeast1`（東京）、`asia-northeast2`（大阪） | 約30〜50ms | 国外移転 |
| OCI | `ap-seoul-1`（ソウル） | `ap-chuncheon-1`（春川） | 約5ms | **国内DR可能** |
| OCI | `ap-seoul-1`（ソウル） | `ap-tokyo-1`（東京） | 約30ms | 国外移転 |

:::caution
国外リージョンをDR対象として使用する場合、個人情報保護法・信用情報法に基づくデータの国外移転要件を満たす必要があります。データ主権が厳格なワークロードは、上表で国内DRが可能なベンダーを優先的に検討してください。DR戦略のタイプとRPO/RTO設計は[災害復旧 (DR)](../../governance/dr/)を参照してください。
:::

## データ主権

韓国の**個人情報保護法**は、個人情報の国外移転時に情報主体の同意または法的根拠を要求します。**信用情報法**は金融分野の個人信用情報に対してより厳格な規制を適用します。クラウドベンダーを選択する際は、韓国リージョンの有無とデータ保存場所を必ず確認する必要があります。

リージョン制限をポリシーとして強制する方法（SCP、Azure Policyなど）は[リージョンと可用性ゾーン — データ主権とリージョン制限](../../about-cloud/regions-and-zones/)を参照してください。

## 専用接続PoPとCloud Exchange

国内で専用接続（Direct Connect、ExpressRoute、Cloud Interconnect、FastConnect）を構成する際に利用できるPoP現況です。

| 項目 | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- |
| **韓国PoP** | KINX、LG U+ | KINX、LG U+ | KINX | KINX |

**国内Cloud Exchangeの選択肢:**

- **KINX**: 国内最大のIX（Internet Exchange）。AWS、Azure、Google Cloud、OCIすべてにPoPを保有
- **Megaport**: グローバルCloud Exchange。ソウルにPoPあり
- **Equinix Fabric**: グローバル最大手。ソウルにデータセンターを運営

接続方式別のトレードオフは[マルチクラウドネットワーキング](../../networking/multicloud-networking/)を参照してください。

## MSPとコミュニティ

国内MSPを利用すると、一般的な運用代行に加えて次のような支援を受けられます。

- 税金計算書（税務証憑）発行、ウォン建て決済
- 規制対応（CSAP、ISMS-Pなど）支援 — 詳細は[コンプライアンス（韓国）](../../korea/governance/compliance/)

| ベンダー | コミュニティ | 備考 |
| --- | --- | --- |
| AWS | [AWSKRUG](https://www.awskr.org/) | 韓国のAWSユーザーコミュニティ |
| Google Cloud | [GDG Cloud Korea](https://gdg.community.dev/gdg-cloud-korea/) | 韓国のGoogle Cloudユーザーコミュニティ |

MSPの費用構造とサポートプラン全般については[技術サポートとサポートプラン](../../about-cloud/support-plans/)を参照してください。

## 関連ドキュメント

> 📄 [リージョンと可用性ゾーン](../../about-cloud/regions-and-zones/)

> 📄 [災害復旧 (DR)](../../governance/dr/)

> 📄 [マルチクラウドネットワーキング](../../networking/multicloud-networking/)

> 📄 [技術サポートとサポートプラン](../../about-cloud/support-plans/)

## 参考資料

- [KINX](https://www.kinx.net/) — 韓国国内最大のIX
- [KINX Cloud Hub](https://www.kinx.net/service/cloud/) — マルチクラウド専用接続サービス
- [AWSソウルリージョン](https://aws.amazon.com/ko/about-aws/global-infrastructure/regions_az/)
- [Azure韓国リージョン (Korea Central/South)](https://azure.microsoft.com/explore/global-infrastructure/geographies)
- [Google Cloudソウルリージョン](https://cloud.google.com/about/locations)
- [OCIリージョン](https://www.oracle.com/cloud/public-cloud-regions/)
