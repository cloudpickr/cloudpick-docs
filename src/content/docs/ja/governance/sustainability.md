---
title: "サステナビリティとGreenOps"
description: "クラウドのサステナビリティ（GreenOps）— 炭素排出の追跡、低炭素設計の原則、ベンダー別ツールを比較します。"
---

> 文書基準: 2026年8月

## 概要

クラウドのサステナビリティは、ベンダーと顧客の**共同責任**です。ベンダーはデータセンターの効率（PUE）、再生可能エネルギーへの転換を担当し、顧客はワークロードの効率化により不要なリソース使用を減らします。

## ベンダー別炭素排出追跡ツール

| ベンダー | ツール | 特徴 |
| --- | --- | --- |
| AWS | [Customer Carbon Footprint Tool](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/what-is-ccft.html) | アカウント別の炭素排出量ダッシュボード。Scope 1/2/3を区分 |
| Azure | [Emissions Impact Dashboard](https://learn.microsoft.com/azure/carbon-optimization/view-emissions) | Microsoft Sustainability Managerと連携。リージョン別の炭素強度 |
| Google Cloud | [Carbon Footprint](https://cloud.google.com/carbon-footprint) | プロジェクト別排出量。リージョン別の炭素指数（CFE%）を公開 |
| OCI | [Sustainability ダッシュボード](https://www.oracle.com/corporate/citizenship/sustainability/) | リージョン別エネルギー効率レポート |

## サステナブルな設計原則

### 低炭素リージョンの選択

各リージョンの電力構成（再生可能エネルギー比率）は異なります。レイテンシ要件に柔軟性があるワークロードは、炭素強度の低いリージョンを選択できます。

- **AWS** — 運用電力100%再生可能エネルギーマッチングの目標を2023年に達成と報告(その後の年度も維持を報告)。[Customer Carbon Footprint Tool](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/what-is-ccft.html)でアカウント別排出量を確認
- **Azure** — 再生可能エネルギー・炭素目標の進捗はMicrosoftのサステナビリティ公開資料を確認。排出量追跡は[Emissions Impact Dashboard](https://learn.microsoft.com/azure/carbon-optimization/view-emissions)を使用
- **Google Cloud** — リージョン別のCFE（Carbon-Free Energy）比率を公開、2030年に24/7カーボンフリーの目標
- **OCI** — EU等リージョン別の再生可能エネルギー目標・現状はOracleの公開資料を確認。Cloud Advisorがサステナビリティに関する推奨事項を提供

### リソース効率化

| 原則 | 方法 | 効果 |
| --- | --- | --- |
| **適正サイジング** | オーバープロビジョニングの排除。CPU/メモリ使用率に基づく縮小 | リソース削減＝エネルギー削減 |
| **スケジューリング** | 非業務時間の開発環境停止 | アイドルリソースの排除 |
| **サーバーレス/マネージド** | 共有インフラで密度を向上 | 専用サーバーに比べエネルギー効率が高い |
| **効率的なインスタンス** | Armベース（Graviton、Ampere、Tau）の選択 | 同一性能に対して電力消費が低い |
| **データ保持ポリシー** | 不要データの削除、コールドストレージへの移行 | ストレージのエネルギー削減 |

### グリーンアーキテクチャパターン

- **非同期処理** — ピーク時間の分散によりインフラの最大容量を縮小
- **キャッシング** — 反復する演算/照会の排除によりコンピューティングを削減
- **データローカリティ** — データとコンピューティングを同一リージョンに配置しネットワーク転送を最小化

:::note
**GreenOpsとFinOpsは方向性が同じです。** コストを削減する行為（アイドルリソースの排除、適正サイジング、サーバーレスへの移行）は、たいてい炭素排出も削減します。[FinOps](../../governance/finops/)の実践がそのままGreenOpsになります。
:::

## GreenOps運用指標

### 追跡すべき指標

| 指標 | 説明 | 出典 |
| --- | --- | --- |
| ワークロード別炭素排出量の推移 | 月別のtCO₂e変化 | ベンダーの炭素ダッシュボード |
| コスト対炭素効率 | $/tCO₂e | コスト＋炭素レポートの組み合わせ |
| アイドルリソース比率 | CPU使用率5%未満のインスタンス比率 | モニタリングツール |
| スケジューリングで削減したコンピューティング時間 | 業務外時間の自動停止による削減量 | 自動化ログ |
| データ保持ポリシーによる削減 | ライフサイクルポリシーで削減したストレージ | ストレージレポート |

### Scopeと責任範囲

炭素排出レポートでよく登場するScopeの概念です。

| Scope | 説明 | クラウドにおける意味 |
| --- | --- | --- |
| Scope 1 | 直接排出（自社施設） | クラウド利用者には該当しない |
| Scope 2 | 間接排出（購入電力） | ベンダーがデータセンター電力として責任を負う |
| Scope 3 | バリューチェーン排出 | **利用者のクラウド利用**がここに該当する |

利用者が直接削減できる領域: アイドルリソースの排除、適正サイジング、低炭素リージョンの選択、効率的なアーキテクチャ。

### FinOpsとGreenOpsの違い

共通点は多いですが、常に一致するわけではありません。

| 状況 | FinOpsの観点 | GreenOpsの観点 |
| --- | --- | --- |
| 低炭素リージョンの方が高価 | コスト最低のリージョンを選択 | 炭素最低のリージョンを選択 |
| スポットインスタンス | コスト削減 ✅ | 再起動の繰り返しでかえって非効率な場合あり |
| アイドルリソースの排除 | コスト削減 ✅ | 炭素削減 ✅（同一） |
| 適正サイジング | コスト削減 ✅ | 炭素削減 ✅（同一） |

### 意思決定チェックリスト

- [ ] レイテンシ/SLAのためにリージョンを変更できないワークロードか？
- [ ] バッチジョブのように実行時間を調整できるワークロードか？
- [ ] データ保持期間が規制要求より過度に長くないか？
- [ ] 炭素最適化がセキュリティ/可用性/コンプライアンスを損なわないか？

## よくある間違い

- **低炭素リージョンを選んだがレイテンシ要件を無視** — 利用者から遠いリージョンを選択し、応答時間がSLAを超過する
- **GreenOps指標は追跡するが実際の対策を行わない** — ダッシュボードだけ作成し、アイドルリソースの排除やスケジューリングといった実行を行わない
- **FinOpsとGreenOpsを別々のイニシアティブとして運用する** — ほとんどのコスト削減活動がそのまま炭素削減になるのに、重複した組織/プロセスを作ってしまう

## チェックリスト

- [ ] ベンダーの炭素排出ダッシュボード(Customer Carbon Footprint Tool等)を有効化し、月次推移を追跡しているか
- [ ] 非業務時間に開発/テスト環境を自動停止するスケジューリングを適用しているか
- [ ] Armベースのインスタンス(Graviton、Ampere)を互換性のあるワークロードに優先適用しているか

## 参考資料

### AWS

- [AWS Sustainability Pillar (Well-Architected)](https://docs.aws.amazon.com/wellarchitected/latest/sustainability-pillar/sustainability-pillar.html)

### Azure

- [Azure Well-Architected — Sustainability](https://learn.microsoft.com/azure/well-architected/sustainability/)

### Google Cloud

- [Google Cloud Carbon Footprint](https://cloud.google.com/carbon-footprint)
- [Google Cloud Region Carbon-Free Energy](https://cloud.google.com/sustainability/region-carbon)

### OCI

- [Oracle Cloud Sustainability](https://www.oracle.com/corporate/citizenship/sustainability/)

### 標準およびコミュニティ

- [Green Software Foundation](https://greensoftware.foundation/)
