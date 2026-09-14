---
title: "推論サービング・信頼性・コスト最適化"
description: "GPU推論サービングの運用、ノード障害の自動再開、容量運用（Capacity Blocks・予約・マルチリージョンフォールバック）、GPUコスト最適化をベンダー中立の視点で整理します。"
---

> 文書基準: 2026年9月 | この文書は変化の速い領域であり、四半期ごとのレビュー対象です。

:::note
この文書はGPUインフラの運用段階（推論サービング・障害対応・容量・コスト）を扱います。学習の並列化は[分散学習の標準アーキテクチャ](../distributed-training/)を、クラスターアーキテクチャは[GPUワークロードの特性とリファレンスアーキテクチャ](../workload-and-architecture/)を参照してください。
:::

## 概要

GPUインフラは構築後の運用段階でコストと安定性が分かれます。この文書は推論サービング（遅延・オートスケール）、障害復旧（チェックポイント・ノード再投入）、そしてGPU容量の確保とコスト最適化（コミット・スポット・容量予約）を扱います。特に2026年現在は、性能よりも**欲しいときにGPUを実際に確保できるか**が最大の制約です。

推論と学習は性格が異なります。学習が長く・大きく・一度に回す仕事だとすれば、推論はユーザーのリクエストが来るたびに**素早く応答**し、リクエスト量に応じて**自動で増えたり減ったり**する必要があります。

## 推論サービング

推論は学習と相反する運用プロファイルを持ちます。学習が長時間・高通信・バッチ志向であるのに対し、推論は**遅延に敏感・リクエスト単位・オートスケール志向**です。

- **遅延 vs スループット** — リアルタイムサービングは低遅延（速い応答）が、バッチ推論は高スループット（一度に多く）が目標です。動的バッチング（dynamic batching = 短い時間に入ってきたリクエストをまとめて一度に処理）で両者のバランスを取ります。
- **オートスケール** — リクエスト量に応じてGPUレプリカを増減します。ただしGPUは起動時にモデルの重みをメモリに載せる時間（コールドスタート）が長く、CPUより反応が遅いです。そのため最低数台は常に点けておくか、あらかじめ予熱しておきます。
- **モデル並列サービング** — 単一のGPUに収まらない大型モデルは、推論でもテンソル並列を使います。（[並列化戦略](../distributed-training/)を参照）
- **トークン単位のコスト・ルーティング** — ファウンデーションモデルAPIのトークンコスト・プロンプトキャッシング・モデルルーティングは[LLMOps](../../../ai/llmops/)と[AIプラットフォームとモデル比較 — 推論コスト最適化](../../../ai/ai-ml/#推論コスト最適化)で扱います。

## 信頼性・障害対応

ノードが多いほど、学習の途中でハードウェアが故障する確率が高くなります。数百枚GPU規模では故障が例外ではなく日常です。そこで「故障は起きる」を前提に備えます。

- **故障検知** — ノードヘルスチェックとGPUエラー信号（Xidエラー = NVIDIAドライバが報告するGPUエラーコード、メモリエラー、通信リンク切れ）で異常ノードを素早く見つけて隔離します。
- **チェックポイントで再開** — 最後に保存しておいた地点（[チェックポイント](../distributed-training/#チェックポイント戦略)）から再び始めます。故障したノードは交換し、残りのノードはしばらく待ってから再び合わせます。
- **遅いノード（straggler）対応** — 1ノードだけ遅くなっても（ネットワーク問題や発熱による速度低下）、全体がそのノードを待って一緒に遅くなります。こうした遅いノード（straggler）を見つけて隔離・交換します。
- **マネージドクラスターの自動復旧** — [マネージドGPUクラスター](../workload-and-architecture/#マネージドgpuクラスター)（例: SageMaker HyperPod）は故障検知・自動交換・チェックポイント再開を丸ごと提供し、この負担を軽くします。

## 容量運用

2026年現在、最新世代のGPUは**必要なときに即座に確保できない**ことが多いです。容量の確保はインフラ設計の第一級の制約です。

| 項目 | AWS | Azure | Google Cloud | OCI |
| --- | --- | --- | --- | --- |
| **容量予約** | [Capacity Blocks for ML](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-capacity-blocks.html)、On-Demand Capacity Reservations | On-Demand Capacity Reservations | [Future Reservations](https://cloud.google.com/compute/docs/instances/reservations-overview)、Calendar mode | Capacity Reservation |
| **コミット割引** | Savings Plans、Reserved Instances | Reserved VM Instances | CUD (Committed Use Discount) | Universal Credits、コミット |
| **プリエンプティブル** | Spot Instances | Spot VMs | Spot VMs | Preemptible Instances |

- **容量ブロック・予約キュー** — 特定期間のGPU容量を事前に予約します。大規模学習は開始前の容量確保が前提です。
- **リージョンの希少性** — 最新のGPUは少数のリージョンにのみあり、数量が限られます。希望するリージョン・世代の実際の可用性を事前に確認する必要があります。
- **マルチリージョン・マルチクラウドフォールバック** — 単一リージョンの容量不足に備え、代替リージョン・世代をフォールバックとして準備します。データの所在・イグレスコストを一緒に考慮します。

:::caution
最新のGPU世代ほどリージョン可用性が限定的で、コミット確保の競争が激しくなります。「インスタンスタイプがドキュメントに存在する」ことと「希望するリージョンで希望する数量を今確保できる」ことはまったく別の問題です。容量は設計初期に確認し、予約してください。
:::

:::note
上表の軸は性格が異なります。**容量確保**（Capacity Blocks・Future Reservationsなど）は「数量を押さえる」メカニズムであり、**コミット割引**（Savings Plans・CUD・RIなど）は「価格を下げる」財務コミットです。両者は一般に重ねて適用されないため、容量確保とコスト削減を別々に設計する必要があります。また、OCI Universal CreditsはGPU容量割引ではなく、アカウント単位の消費コミットである点に留意してください。
:::

## コスト最適化

GPUはクラウドで最も高価なリソースであるため、利用率と購入方式がコストを左右します。

- **購入方式の組み合わせ** — 常時稼働ワークロードはコミット割引（Savings Plans/CUD/RI）で、学習・バッチはプリエンプティブル（Spot）で、予測可能な大規模学習は容量予約で配分します。
- **プリエンプティブル + チェックポイント** — プリエンプティブルは最大で数十%安いですが中断される可能性があるため、[チェックポイント](../distributed-training/#チェックポイント戦略)と組み合わせて中断時に再開します。
- **right-sizing** — ワークロードに過大なGPU世代を使いません。推論・ファインチューニングは上位世代が不要な場合が多いです。
- **アイドル回収** — [GPU共有（MIG/time-slicing）](../kubernetes-and-scheduling/#gpu共有--migとtime-slicing)とアイドルノードのスケールダウンで浪費を減らします。
- **GPU時間のFinOps** — GPUの時間単位コスト・利用率をチーム別に配分・追跡する体系は[FinOps](../../../governance/finops/)で、モデルライセンス・使用料は[AIライセンシング](../../../ai/licensing/)で扱います。

## 関連文書

この文書はGPUインフラシリーズの最終部（第4部）です。シリーズ全体は[GPUワークロードの特性とリファレンスアーキテクチャ](../workload-and-architecture/)から始まります。

- **クラスターアーキテクチャ・マネージドクラスター** — [GPUワークロードの特性とリファレンスアーキテクチャ](../workload-and-architecture/)
- **並列化・チェックポイント** — [分散学習の標準アーキテクチャ](../distributed-training/)
- **スケジューリング・GPU共有・可観測性** — [GPU Kubernetesとスケジューリング](../kubernetes-and-scheduling/)
- **コスト配分・予算** — [FinOps](../../../governance/finops/)
- **トークン・プロンプトコスト** — [LLMOps](../../../ai/llmops/)

## よくある間違い

- **容量確保を設計の最後に確認** — 希望するリージョン・世代のGPUがなく、プロジェクトのスケジュールが遅延
- **推論に学習と同じ構成を使用** — 遅延・オートスケールの要求を無視し、学習用の大規模構成をそのまま適用してコストを浪費
- **プリエンプティブルをチェックポイントなしで学習に使用** — 中断時に進捗をすべて失う
- **利用率モニタリングなしの常時オンデマンド** — アイドルのGPUをオンデマンドで点けっぱなしにし、コストが累積

## チェックリスト

- [ ] 推論サービングに動的バッチング・オートスケール・コールドスタート緩和を適用したか
- [ ] 大規模学習に障害検知とチェックポイントベースの自動再開を構成したか
- [ ] 希望するリージョン・世代のGPU容量を事前に確認し、予約したか
- [ ] マルチリージョン/フォールバック戦略をデータの所在・イグレスと一緒に検討したか
- [ ] コミット・プリエンプティブル・容量予約をワークロード特性に合わせて組み合わせたか
- [ ] GPU利用率をチーム別に追跡し、FinOpsに連携したか

## 参考リンク

### AWS

- [EC2 Capacity Blocks for ML](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-capacity-blocks.html)
- [Spot Instances](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-spot-instances.html)

### Azure

- [On-Demand Capacity Reservations](https://learn.microsoft.com/azure/virtual-machines/capacity-reservation-overview)
- [Azure Spot Virtual Machines](https://learn.microsoft.com/azure/virtual-machines/spot-vms)

### Google Cloud

- [Compute 予約](https://cloud.google.com/compute/docs/instances/reservations-overview)
- [Spot VMs](https://cloud.google.com/compute/docs/instances/spot)

### OCI

- [Capacity Reservation](https://docs.oracle.com/en-us/iaas/Content/Compute/Tasks/reserve-capacity.htm)
- [Preemptible Instances](https://docs.oracle.com/en-us/iaas/Content/Compute/Concepts/preemptible.htm)
