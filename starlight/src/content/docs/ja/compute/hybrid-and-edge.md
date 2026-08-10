---
title: "ハイブリッド/エッジコンピューティング"
description: "ハイブリッドクラウド、エッジコンピューティング、マルチクラウドアーキテクチャパターンをベンダー別に比較します。"
---

> 文書基準: 2026年5月

## 概要

すべてのワークロードがパブリッククラウドに適しているわけではありません。データ主権、超低遅延、既存投資の保護などの理由から、**オンプレミス/エッジにクラウドインフラを拡張**する需要があります。

## ベンダー別ハイブリッド/エッジソリューション

| ベンダー | オンプレミス拡張 | エッジ | マルチクラウド管理 |
| --- | --- | --- | --- |
| AWS | [Outposts](https://aws.amazon.com/outposts/) (ラック/サーバー) | [Local Zones](https://aws.amazon.com/about-aws/global-infrastructure/localzones/)、[Wavelength](https://aws.amazon.com/wavelength/) | EKS Anywhere、ECS Anywhere |
| Azure | [Azure Stack HCI](https://learn.microsoft.com/azure/azure-local/)、[Azure Local](https://learn.microsoft.com/azure/azure-local/) | Azure Edge Zones | [Azure Arc](https://azure.microsoft.com/products/azure-arc/) |
| Google Cloud | [Google Distributed Cloud](https://cloud.google.com/distributed-cloud) (Connected/Edge/Air-gapped) | GDC Edge | [GKE Enterprise](https://cloud.google.com/kubernetes-engine/enterprise/docs) |
| OCI | [Dedicated Region](https://www.oracle.com/cloud/cloud-at-customer/dedicated-region/)、[Compute Cloud@Customer](https://www.oracle.com/cloud/cloud-at-customer/) | — | [OCI Multicloud](https://docs.oracle.com/en/solutions/oci-best-practices/deploy-multicloud-oci-oracle-database-services1.html) |

## ユースケース

| 事例 | 要件 | 適したソリューション |
| --- | --- | --- |
| **データ主権** | データが特定の国/施設の外に出てはならない | Dedicated Region、Azure Stack、GDC Air-gapped |
| **超低遅延** | 工場自動化、リアルタイムゲーム、AR/VR | Local Zones、Wavelength、Edge Zones |
| **既存投資の保護** | オンプレミス機器の寿命が残っている+クラウドサービスを利用 | Arc、GKE Enterprise、EKS Anywhere |
| **規制 (閉域網)** | インターネット接続不可の環境 | GDC Air-gapped、Dedicated Region |

## マルチクラウドアーキテクチャパターン

| パターン | 説明 | 例 |
| --- | --- | --- |
| **Split-stack** | 階層ごとに異なるベンダーを使用 | フロントエンド(AWS CloudFront)+バックエンド/DB(OCI) |
| **Data Gravity** | 大容量データは一箇所に、分析/AIは複数ベンダーからアクセス | データレイク(GCS)+ML(Vertex AI)+サービング(AWS) |
| **Best-of-Breed** | サービス領域ごとに最適なベンダーを選択 | AI(Google Cloud)+エンタープライズアプリ(Azure)+DB(OCI) |
| **Cloud-bursting** | 平常時はオンプレミス、ピーク時にパブリック拡張 | オンプレミスK8s+EKS/AKS/GKEバースト |
| **DR/Failover** | 主ベンダー障害時に補助ベンダーへ切り替え | AWS(主)+Azure(DR) |

:::note
マルチクラウドパターンは複雑さを追加します。[マルチクラウドを理解する](../../about-cloud/why-multicloud/)で導入動機とトレードオフを先に検討してください。
:::

## よくある間違い

- **ハイブリッドアーキテクチャでネットワーク遅延を過小評価** — オンプレミスとクラウド間の往復遅延(数十ms)を考慮せず同期呼び出しを設計すると、パフォーマンスが急激に低下します。
- **エッジ機器の運用負担を軽視** — エッジに展開すると、物理的アクセスが難しい環境でパッチ、障害復旧、モニタリングをリモートで行う必要があります。運用自動化なしで導入すると管理コストが急増します。
- **マルチクラウドをデフォルトとして選択** — 明確なビジネス要件(規制、DR、ベンダーロックイン回避)なしにマルチクラウドを導入すると、複雑さとコストだけが増加します。

## チェックリスト

- [ ] オンプレミス↔クラウド間のネットワーク帯域幅と遅延を測定したか
- [ ] エッジ/オンプレミス機器のリモート管理・モニタリング・パッチ自動化の方法があるか
- [ ] ハイブリッド/マルチクラウド導入のビジネス根拠(規制、DR、コスト)を文書化したか

## 参考資料

### AWS

- [AWS Outposts 文書](https://docs.aws.amazon.com/outposts/)

### Azure

- [Azure Arc 文書](https://learn.microsoft.com/azure/azure-arc/)

### Google Cloud

- [Google Distributed Cloud 文書](https://cloud.google.com/distributed-cloud)

### OCI

- [OCI Dedicated Region](https://www.oracle.com/cloud/cloud-at-customer/dedicated-region/)
- [OCI Alloy](https://www.oracle.com/cloud/alloy/)

### 標準およびコミュニティ

- [CNCF Multi-Cloud Patterns](https://www.cncf.io/reports/cncf-annual-survey-2023/)
