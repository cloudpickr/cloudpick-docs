---
title: "GPU Kubernetesとスケジューリング"
description: "GPUノードプール・device plugin、MIG/time-slicing共有、ResourceQuota・anti-hoarding、gang scheduling（Kueue/Volcano）、DCGM可観測性をベンダー中立の視点で整理します。"
---

> 文書基準: 2026年9月 | この文書は変化の速い領域であり、四半期ごとのレビュー対象です。

:::note
この文書はKubernetes上でGPUをスケジューリング・共有・統制する方法を扱います。クラスターのアップグレードやノード管理など一般的なKubernetes運用は[Kubernetes運用](../../../devops/kubernetes-operations/)で、GPUクラスターの通信・配置は[GPUワークロードの特性とリファレンスアーキテクチャ](../workload-and-architecture/)で扱います。
:::

## 概要

GPUは高価で希少です。そのため通常は1チームが独占せず、複数のチーム・複数のジョブが**一つのGPUクラスターを分け合って使います**。このとき「誰にGPUをいくつ、いつ渡すか」を決めるのがスケジューラで、この配分を誤ると高価なGPUが遊んだり、特定のチームが独占したりします。

Kubernetes（コンテナを自動配置・管理する標準ツール）はGPUを特別な資源として扱います。難しいのは、性格が正反対の2つのジョブを一つのクラスターで一緒に受け入れなければならない点です — **学習ジョブ**は「必要なGPUを一度に全部渡さないと」始まらず、**推論ジョブ**は「少ないGPUを長く握って」動きます。

:::note
Kubernetes自体が初めてなら、[コンテナサービス](../../../compute/containers/)と[Kubernetes運用](../../../devops/kubernetes-operations/)を先に読むことを勧めます。この文書はその上で**GPUに特化した**部分だけを扱います。
:::

## GPUノードプールとdevice plugin

Kubernetesは既定でGPUを認識しないため、ベンダーのdevice pluginとドライバ・オペレータをインストールして、GPUをスケジューリング可能なリソースとして公開します。

- **GPUノードプール** — 汎用ノードと分離したGPU専用ノードプールを構成します。（[ノードプール構成](../../../compute/containers/#ノードプール構成)を参照）
- **device plugin / オペレータ** — ドライバ・device plugin・DCGMを一括デプロイする[NVIDIA GPU Operator](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/index.html)が事実上の標準です。
- **taint/toleration** — GPUノードにtaintをかけ、非GPUワークロードが高価なGPUノードを占有しないようにします。

## GPU共有 — MIGとtime-slicing

単一のGPUを複数のジョブが分けて使うと、小規模な推論・開発ワークロードの利用率を高められます。

| 方式 | 分離レベル | 適したワークロード | 限界 |
| --- | --- | --- | --- |
| **MIG (Multi-Instance GPU)** | ハードウェアパーティション（メモリ・演算の分離） | 予測可能なマルチテナント推論 | 対応GPU・プロファイルの制約、動的変更の負担 |
| **MPS (Multi-Process Service)** | プロセス空間の共有（部分的分離） | 協調的なマルチプロセス、小規模推論 | メモリ分離を保証しない、障害伝播の可能性 |
| **Time-slicing** | 時間分割（分離なし） | 開発・実験、バースト的ワークロード | 性能干渉・OOMのリスク、公平性を保証しない |

MIGはハードウェア分離で最も強く、time-slicingは分離がなく、MPSはその中間で複数のプロセスが一つのGPUコンテキストを共有します。3方式ともNVIDIA GPUの共通機能であり、特定ベンダー専用ではありません。

:::caution
Time-slicingはメモリ・演算を分離しないため、あるジョブのOOMや暴走が同じGPUの他のジョブに影響します。本番のマルチテナントにはMIG（ハードウェア分離）を優先的に検討してください。MIGは対応GPU世代・プロファイルが限定的なため、対象GPUの対応可否を先に確認する必要があります。
:::

## クォータ・公平性・anti-hoarding

共有クラスターの悩みの種は、**あるチームがGPUを掴んで離さないこと**（独占、hoarding）です。すると他のジョブがGPUを受け取れず、飢え続けます。これを防ぐ仕組み:

- **ResourceQuota（総量の上限）** — チーム（名前空間）ごとに使えるGPU数の上限を決めます。
- **優先度・プリエンプション（preemption）** — ジョブごとに優先度を付け（PriorityClass）、急ぎのジョブが来たら急ぎでないジョブを一時的に押しのけて（プリエンプト）GPUを譲らせます。
- **遊んでいるGPUの回収（anti-hoarding）** — 掴んだだけで実際には使っていないGPUを、キューベースのスケジューラが公平配分・回収のルールで取り戻し、他のジョブに回します。
- **キューベースの配分** — 下記のgang scheduling層でチーム別の取り分と待ち行列を管理します。

## Gang scheduling

分散学習は必要なGPUを**一度に全部**確保しないと始められません。たとえばGPU 16枚が必要なのに10枚だけ掴んで残り6枚を待つと、掴んだ10枚は何もできず資源だけを縛ります（ひどいと互いに待ち合って止まるデッドロック）。Gang schedulingはこれを防ぐため、**「必要なだけ全部揃えば開始、そうでなければまったく開始しない（全か無か）」という方式**でスケジューリングします。「gang（一つの群れ）」を丸ごと掴むという意味です。

| ツール | 特徴 |
| --- | --- |
| [Kueue](https://kueue.sigs.k8s.io/) | Kubernetesネイティブのジョブキューイング、クォータ・公平共有、階層的キュー |
| [Volcano](https://volcano.sh/) | バッチスケジューラ、gang scheduling・キュー・プリエンプション統合、HPC/AI志向 |

:::note
KueueとVolcanoはいずれもベンダー中立のオープンソースであり、どのクラウドのKubernetesでも動作します。マネージド学習プラットフォーム（SageMaker HyperPod、Vertex AIなど）は同様のキューイング・gang schedulingを内蔵で提供するため、自己構成の代わりに活用できます。
:::

:::note
この文書はKubernetes上でのスケジューリングを扱います。Kubernetesの代わりにSlurm（HPCバッチスケジューラ）をオーケストレータとして使う方式と、ベンダー別のマッピング（HyperPod+Slurm、CycleCloud、Cluster Toolkitなど）は[GPUワークロードの特性とリファレンスアーキテクチャ — オーケストレータの選択](../workload-and-architecture/#オーケストレータの選択--slurmとkubernetes)で扱います。
:::

## ベンダー別マネージドKubernetes GPU対応

| 項目 | AWS (EKS) | Azure (AKS) | Google Cloud (GKE) | OCI (OKE) |
| --- | --- | --- | --- | --- |
| **GPUノードプール** | マネージドノードグループ | GPUノードプール | GPUノードプール | GPUノードプール |
| **ドライバインストール** | GPU Operator / EKS最適化AMI | GPU Operator / AKS GPUイメージ | GPU Operator / GKEドライバ自動インストール | GPU Operator / OKEイメージ |
| **GPU共有** | MIG、MPS、time-slicing | MIG、MPS、time-slicing | MIG、MPS、time-slicing | MIG、MPS、time-slicing |

:::note
GPU共有・gang scheduling・オペレータは大半がオープンソース層で動作するため、ベンダー間で概念が類似しています。ただしノードプールのプロビジョニングAPI、ドライバ自動インストールの方式、対応GPU世代はベンダーごとに異なるため、各ベンダーの公式ドキュメントで確認してください。
:::

## 可観測性 — DCGMとGPUメトリクス

GPUクラスターはCPU中心の可観測性だけではボトルネックを診断できません。[NVIDIA DCGM](https://docs.nvidia.com/datacenter/dcgm/latest/index.html)（Data Center GPU Manager、GPUの状態・性能を収集する標準ツール）でGPU利用率・メモリ・温度・通信網のトラフィックを集めます。

- **主要指標** — GPU利用率（単なる占有率ではなく実際の演算利用）、メモリ使用量、ファブリック帯域、電力・温度
- **利用率の落とし穴** — 「GPUが割り当てられている」と「GPUが実際に計算中である」は異なります。低い実効利用率は、データロード・通信ボトルネックのサインです。
- **SLO連携** — 収集したGPUメトリクスを[SLO](../../../devops/slo/)・[可観測性](../../../devops/observability/)の体系に統合し、学習スループット・推論遅延を継続的に管理します。

## 関連文書

- **次: 推論サービング・障害・容量・コスト** — [推論サービング・信頼性・コスト最適化](../serving-reliability-cost/)
- **一般的なKubernetes運用（アップグレード・ノード管理）** — [Kubernetes運用](../../../devops/kubernetes-operations/)
- **クラスターの通信・配置・マネージドクラスター** — [GPUワークロードの特性とリファレンスアーキテクチャ](../workload-and-architecture/)
- **並列化戦略（TP/PP/DP）** — [分散学習の標準アーキテクチャ](../distributed-training/)

## よくある間違い

- **gang schedulingなしで分散学習を投入** — GPUを一部だけ確保して待機し、リソースが拘束されデッドロックが発生
- **time-slicingを本番のマルチテナントに使用** — 分離がなく、あるジョブのOOMが他のジョブに伝播
- **ResourceQuota・プリエンプションポリシーの不在** — あるチームがGPUを独占（hoarding）し、他のジョブが枯渇
- **GPU割り当て率だけを見て利用率を見ない** — 低い実効利用率（データ・通信ボトルネック）を見逃し、高価なGPUが浪費される

## チェックリスト

- [ ] GPU専用ノードプールにtaintをかけ、非GPUワークロードの占有を防いだか
- [ ] マルチテナント推論にtime-slicingではなくMIG（ハードウェア分離）を検討したか
- [ ] 名前空間別のResourceQuotaとPriorityClass・プリエンプションポリシーを設定したか
- [ ] 分散学習にgang scheduling（Kueue/Volcanoまたはマネージド内蔵）を適用したか
- [ ] DCGMで実効GPU利用率を収集し、SLOに連携したか

## 参考リンク

### 共通（ベンダー中立）

- [NVIDIA GPU Operator](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/index.html)
- [NVIDIA DCGM](https://docs.nvidia.com/datacenter/dcgm/latest/index.html)
- [Kueue](https://kueue.sigs.k8s.io/)
- [Volcano](https://volcano.sh/)

### ベンダー別

- [AWS — EKS GPUワークロード](https://docs.aws.amazon.com/eks/latest/userguide/eks-optimized-ami.html)
- [Azure — AKS GPUノードプール](https://learn.microsoft.com/azure/aks/gpu-cluster)
- [Google Cloud — GKE GPU](https://cloud.google.com/kubernetes-engine/docs/how-to/gpus)
- [OCI — OKE GPUノード](https://docs.oracle.com/en-us/iaas/Content/ContEng/Tasks/contengrunninggpunodes.htm)
