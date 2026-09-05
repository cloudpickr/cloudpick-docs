---
title: "仮想マシン"
description: "汎用、Arm、GPU仮想マシン製品とイメージ(OSテンプレート)をベンダー別に比較します。"
---

> 文書基準: 2026年8月

## 概要

自社データセンターでサーバーを運用するには、ハードウェアの購入、設置、OS設定、ネットワーク構成を自ら行う必要があります。機器導入に数週間かかり、スペックを変更するには物理的に交換する必要があります。

**仮想マシン** (VM)はこのプロセスをソフトウェアで代替します。数分で希望スペックのサーバーを作成し、不要になれば即座に削除できます。物理サーバーの柔軟性の問題を解決した、クラウドの最も基本的なサービスです。

ただし、VMでもOSパッチ、セキュリティ設定、障害対応はユーザー自身が管理する必要があります。この管理負担を軽減するために、コンテナやサーバーレスといった、より高い抽象化レイヤーが登場しました。

## 製品比較

### 汎用VM

| ベンダー | 製品 | 備考 |
| --- | --- | --- |
| AWS | EC2 (M/C/Rインスタンス) | インスタンスタイプが最も多様。1秒単位の課金 |
| Azure | Virtual Machines (D/F/Eシリーズ) | Windowsワークロードに強み (Azure Hybrid Benefitによるライセンス節約) |
| Google Cloud | Compute Engine (N/C/E/Mマシンシリーズ) | Custom Machine Type (CPU/メモリ比率を自由に指定) |
| OCI | OCI Compute | Flexible ShapeでCPU/メモリを自由に組み合わせ。Ampere A1無料枠 |

### Armベース VM

| ベンダー | 製品 | 備考 |
| --- | --- | --- |
| AWS | EC2 Graviton (最新 m9g/c9g/r9g、m8g、t4gなど) | 自社設計のArmプロセッサ(最新Graviton5、旧世代Graviton4/3/2も併行提供)。x86に比べ高いコストパフォーマンス |
| Azure | Cobalt 100 (Dpsv6など) / Dpsv5シリーズ | 自社設計Cobalt 100およびAmpere Altraベース |
| Google Cloud | Axion (C4A) / Tau T2A | 自社設計AxionおよびArmベース汎用 |
| OCI | Ampere A1 Compute | Ampere Altraベース。無料枠を提供 |

### GPU / AIアクセラレータ

| ベンダー | 製品 | 備考 |
| --- | --- | --- |
| AWS | P5、**G7**、G5、Inf2、Trn1/Trn2 | NVIDIA (H100、**RTX PRO 4500 Blackwell**) + 自社チップ(Inferentia、Trainium)。G7は主要クラウド初のRTX PRO Blackwell提供 |
| Azure | NC、ND、NVシリーズ | NVIDIA A100、H100 |
| Google Cloud | A3、A2、G2シリーズ + TPU (v5p/v6e/Ironwood) | NVIDIA H100 + 自社TPU (第7世代Ironwood/TPU7x最新) |
| OCI | GPU Instances (A10、A100、H100) | NVIDIA GPU。Bare Metalオプション提供 |

### イメージ (OSテンプレート)

| ベンダー | 製品 | 備考 |
| --- | --- | --- |
| AWS | AMI (Amazon Machine Image) | Marketplaceでサードパーティイメージを提供 |
| Azure | VM Image / Shared Image Gallery | |
| Google Cloud | Image / Image Family | |
| OCI | Custom Image / Platform Image | Marketplaceでサードパーティイメージを提供 |

:::note
VMは**管理負担が最も大きいコンピューティングサービス**です。OSパッチ、セキュリティ設定、高可用性構成を自ら行う必要があります。運用負担を減らしたい場合は、マネージドコンテナサービスやサーバーレスを検討してください。
:::

## 主な違い

- **AWS** — インスタンスタイプが最も多様で、自社Armプロセッサ(Graviton)によりコスト削減が可能です。
- **Azure** — 既存のWindowsライセンスを活用したHybrid Benefitでコストを削減できます。
- **Google Cloud** — CPUとメモリを自由に組み合わせるCustom Machine Typeを提供します。
- **OCI** — Flexible ShapeでCPU/メモリを自由に組み合わせ、Ampere A1無料枠を提供します。

## いつ何を選ぶべきか

| こんなとき | これを選ぶ |
| --- | --- |
| Windowsワークロード + 既存ライセンスの活用 | Azure VM (Hybrid Benefit) |
| インスタンスタイプの選択肢が最も多く必要なとき | AWS EC2 |
| CPU/メモリを1 vCPU単位で自由に組み合わせたいとき | Google Cloud Compute Engine (Custom Machine Type) またはOCI (Flexible Shape) |
| Armベースのコスト削減が目標のとき | AWS EC2 Graviton |
| 無料枠でArm VMを使用したいとき | OCI Ampere A1 |
| GPU/AIアクセラレータ + 自社チップ(Inferentia、Trainium)が必要なとき | AWS EC2 (P5、Inf2、Trn1) |
| Bare Metalサーバーが必要なとき | OCI Bare MetalまたはAWS Bare Metal |

## 購入オプション (価格モデル)

同じVMでも、契約方式によって価格が大きく異なります。

| オプション | 説明 | 割引率 | リスク |
| --- | --- | --- | --- |
| **オンデマンド (On-Demand / Pay-As-You-Go)** | 使用した分だけ秒/時間単位で課金 | 0% (基準価格) | なし |
| **予約 (Reserved)** | 1年または3年契約 | 最大72% | 使用しなくても料金が発生 |
| **利用コミット割引 (Savings Plans / Savings Plan / CUD)** | 時間あたりの利用金額を契約 | 最大72% | 柔軟だが利用量のコミットが必要 |
| **Spot / Preemptible** | 余剰キャパシティを安価に利用 | 最大90% | いつでも回収される可能性あり |
| **Reserved Capacity** | 特定のAZ/ゾーンにキャパシティを予約 | — | キャパシティ確保を保証 |

### 購入オプション比較

| ベンダー | オンデマンド | 長期契約 | Spot |
| --- | --- | --- | --- |
| AWS | On-Demand | Reserved Instance + Savings Plans | Spot Instance |
| Azure | Pay-As-You-Go | Reserved VM Instance + Savings Plan | Spot VM |
| Google Cloud | On-Demand | Committed Use Discount (CUD) | Preemptible / Spot VM |
| OCI | Pay-As-You-Go | Monthly Flex / Annual Flex / Universal Credits | Preemptible Instance |

> 上記の数値は文書作成時点の基準であり、変動する可能性があります。最新の価格は各ベンダーの公式価格表をご確認ください。

:::note
コスト構造に関する詳細は[コスト構造を理解する](../../about-cloud/pricing-model/)を参考にしてください。
:::

## 配置グループと専用ホスト

高性能/コンプライアンス要件に応じてVMを物理的に制御できます。

| 機能 | 説明 | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- | --- |
| **同一ラック配置** | 低遅延通信 (HPC、分散DB) | Placement Group (Cluster) | Proximity Placement Group | Compact Placement | Cluster Network |
| **分散配置** | 単一障害点の排除 | Placement Group (Spread) | Availability Set | Spread Placement | Fault Domain |
| **専用物理サーバー** | ライセンス/コンプライアンス | Dedicated Host | Dedicated Host | Sole-tenant Node | Dedicated VM Host |

## よくある間違い

- **オンデマンドのみで運用しコストに不満** — 安定して使用するワークロードは、Reserved InstanceやSavings Plansで最大72%削減できます。使用パターンを分析してください。
- **インスタンスタイプを一度決めたまま見直さない** — ベンダーは継続的に新世代をリリースします。同じコストでより高い性能を得られる場合があるため、定期的に見直してください。
- **Golden Imageなしで毎回手動設定** — インスタンスを作成するたびにパッケージのインストールと設定を繰り返すと、一貫性が崩れ時間が無駄になります。AMI/Imageをビルドパイプラインで管理してください。

## チェックリスト

- [ ] ワークロードの特性(CPU/メモリ/GPU)に合ったインスタンスファミリーを選択したか
- [ ] 安定利用のワークロードに対して予約インスタンスまたはSavings Plansを適用したか
- [ ] OSパッチ、セキュリティアップデートの自動化(SSM、Update Managementなど)が構成されているか

## 参考資料

### AWS

- [Amazon EC2 ドキュメント](https://docs.aws.amazon.com/ko_kr/ec2/)
- [Amazon EC2 インスタンスタイプ](https://docs.aws.amazon.com/ko_kr/ec2/latest/instancetypes/)

### Azure

- [Azure Virtual Machines ドキュメント](https://learn.microsoft.com/ko-kr/azure/virtual-machines/)
- [Azure VM サイズ](https://learn.microsoft.com/ko-kr/azure/virtual-machines/sizes/)

### Google Cloud

- [Google Compute Engine ドキュメント](https://cloud.google.com/compute/docs)
- [Google Compute Engine マシンタイプ](https://cloud.google.com/compute/docs/machine-types)

### OCI

- [OCI Compute ドキュメント](https://docs.oracle.com/en-us/iaas/Content/Compute/home.htm)
- [OCI Compute Shapes](https://docs.oracle.com/en-us/iaas/Content/Compute/References/computeshapes.htm)
