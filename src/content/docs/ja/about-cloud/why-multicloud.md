---
title: "マルチクラウドを理解する"
description: "マルチクラウドの定義、導入動機、採用状況、主な課題を説明します。"
---

> 文書基準: 2026年8月

## マルチクラウドとは

マルチクラウドとは、**2つ以上のパブリッククラウドベンダーを意図的に組み合わせて運用する戦略**です。単に複数ベンダーのアカウントを保有することではなく、ワークロードを目的に応じて分散配置し、統合的に運用することを意味します。

:::note
ISO/IEC 22123-1では、マルチクラウドを *「2つ以上のクラウドサービス事業者が提供するパブリッククラウドサービスを使用するクラウド展開モデル」* と定義しています。
:::

似ているようで異なる概念と区別して見ていきましょう。

| 戦略 | 定義 | 例 |
| --- | --- | --- |
| **マルチクラウド** | 2つ以上のパブリッククラウドを組み合わせる | AWS(コンピューティング) + Google Cloud(AI/ML) |
| **ハイブリッドクラウド** | オンプレミス + パブリッククラウドを接続 | 社内DC + AWS Direct Connect |
| **マルチアカウント** | 単一ベンダー内で複数アカウントを運用 | AWS Organizationsでdev/staging/prodを分離 |

:::note
実務ではこの3つが重なるケースが多く見られます。「オンプレミス + AWS + Google Cloud」を運用している場合、ハイブリッドであると同時にマルチクラウドでもあります。
:::

## 採用状況

マルチクラウドはすでに主流の戦略です。

- CNCF Annual Survey 2024によると、企業の約60%が2つ以上のクラウドを使用しています。
- Flexera 2024 State of the Cloud Reportでは、企業の89%がマルチクラウド戦略を採用していると報告されています。

## 導入動機

### ベンダーロックイン(Lock-in)回避

単一ベンダーにすべてのワークロードを集中させると、価格交渉力が弱まり、ベンダーの方針変更に対して脆弱になります。マルチクラウドは交渉カードを確保し、長期的な移行可能性を確保します。

### 規制とデータ主権

国ごとの規制により、特定のデータを特定の地域に保存しなければならなかったり、認証済みのベンダーのみを使用しなければならない場合があります。これにより、ワークロードを複数ベンダーに分散配置する構成が発生します。

### サービス特化(Best-of-Breed)

各ベンダーの強みを組み合わせる戦略です。

- **AI/ML**: Google Cloud Vertex AI + BigQueryで学習、Amazon SageMaker AIでサービング
- **データ分析**: Google Cloud BigQuery(分析) + AWS S3(保存)
- **エンタープライズ**: Azure Entra ID(ID統合) + AWS(インフラ)
- **DB中心**: OCI Autonomous DB + AWS(アプリサーバー)

### M&Aと組織統合

M&A時に被買収企業が異なるベンダーを使用している場合、即座に統合するよりもマルチクラウドとして共存する方が現実的です。

### 可用性と災害復旧

単一ベンダーのグローバル障害に備え、主要サービスを別ベンダーにスタンバイ配置するパターンです。ただしコストと複雑度が高いため、実際にこの目的のみでマルチクラウドを導入するケースは稀です。

## 課題

マルチクラウドは無料ではありません。以下のコストを許容する準備ができているか、まず確認してください。

### 運用複雑度の増加

- ベンダーごとに異なるネットワークモデル、IAM体系、モニタリングツール
- IaC(Terraformなど)で抽象化しても、ベンダー間の差異を完全に隠すことはできない
- 障害発生時の原因特定が単一ベンダーに比べて困難

### チーム能力の分散

- エンジニアが2~3のベンダーすべてを深く扱うのは困難
- 「AWSチーム / Azureチーム」というサイロが生まれると、統合運用のメリットが失われる
- 採用時、マルチクラウド経験者のプールが狭い

### イグレス費用

クラウド間のデータ移動にはイグレス(アウトバウンド)料金が発生します。大容量データをクラウド間で頻繁に転送するアーキテクチャは、コストが急激に増加する可能性があります。ベンダーごとの無料枠と単価については[コスト構造を理解する](../../about-cloud/pricing-model/)を参照してください。

:::note
専用接続(Direct Connect、ExpressRouteなど)を使用するとイグレス単価は下がりますが、回線費用が追加で発生します。
:::

### 可観測性(Observability)の分散

- 各ベンダーのモニタリングツール(CloudWatch、Azure Monitor、Cloud Monitoring)が分離される
- 統合観測のためにDatadog、Grafana Cloudなどのサードパーティツールの導入が事実上必須
- 分散トレーシング(Distributed Tracing)がクラウド境界をまたぐ際に複雑化する

### セキュリティ境界の拡張

- 攻撃対象領域(Attack Surface)がベンダーの数だけ増加
- 統合ID管理(Okta、Entra IDなど)を導入しないとアカウント管理が断片化する
- コンプライアンス監査の範囲が広がる

### Day-2運用負担

初期構築(Day-1)後の継続的な運用(Day-2)において、マルチクラウドの複雑度が顕在化します。

- **二重IAM監査** — ベンダーごとに別々の権限レビュー、未使用アカウントの整理、ポリシー監査を実施する必要がある
- **障害の帰属** — クラウド間の通信障害時、どちらのベンダーの問題か判別が困難。両ベンダーに同時にチケットを起票しなければならないケースが発生
- **パッチ/更新の調整** — ベンダーごとにメンテナンススケジュールが異なるため、同時障害の可能性を考慮した変更管理が必要
- **コストガバナンス** — ベンダーごとに請求体系が異なり、統合コスト分析が困難。FinOps FOCUS仕様など標準化ツールが必要

## マルチクラウドを避けるべき場合

以下の状況では、単一ベンダーに集中する方がより良い選択です。

| 状況 | 理由 |
| --- | --- |
| チーム規模が小さい(10名以下) | マルチクラウド運用のオーバーヘッドを賄う余力がない |
| 明確な規制要件がない | ベンダー分離の動機が弱い |
| データ移動が頻繁なアーキテクチャ | イグレス費用がメリットを相殺する |
| ベンダー固有サービスへの深い依存 | 抽象化コストが高すぎる(例: DynamoDB、Cosmos DB) |
| 「他社がやっているから」 | 戦略のないマルチクラウドは複雑度を増すだけ |

:::caution
**核心原則:** マルチクラウドは目的ではなく手段です。「なぜ複数ベンダーを使う必要があるのか?」に明確な答えがないなら、単一ベンダーでうまく運用する方がより良い戦略です。
:::

## マルチクラウドを始める前のチェックリスト

マルチクラウド導入を検討している場合は、以下の質問に答えてみてください。

- [ ] マルチクラウドを導入すべき具体的なビジネス/規制上の理由があるか?
- [ ] 各ベンダーに配置するワークロードの基準は明確か?
- [ ] クラウド間のネットワーク接続方式とコストを検討したか?
- [ ] 統合ID管理(IdPフェデレーション)戦略はあるか?
- [ ] 統合モニタリング/可観測性ツールを選定したか?
- [ ] IaCでマルチベンダーを管理する能力はあるか?
- [ ] チームは2つ以上のベンダーを運用できる規模か?

---

## よくある間違い

- **「マルチクラウドにすれば可用性が自動的に高まる」** — マルチクラウドDRは二重運用コストと複雑度が非常に高くなります。単一ベンダーのマルチリージョンの方が現実的な場合が多いです。
- **「他社がやっているから自分たちもやるべきだ」** — 明確なビジネス/規制上の理由なく導入すると、複雑度が増すだけです。「なぜ必要なのか」にまず答えてください。
- **「Terraformで抽象化すればベンダーの違いはなくなる」** — IaCでプロビジョニングは統一できますが、IAM・ネットワーク・モニタリングなど運用モデルの違いは依然として残ります。

## 参考資料

### AWS

- [AWS — Prescriptive Guidance: Strategy for multicloud](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-multicloud/welcome.html)

### Azure

- [Azure — Cloud Adoption Framework](https://learn.microsoft.com/azure/cloud-adoption-framework/)

### Google Cloud

- [Google Cloud — Hybrid and Multi-cloud Reference Architectures](https://cloud.google.com/architecture/network-hybrid-multicloud)

### OCI

- [OCI — Multicloud Solutions](https://docs.oracle.com/en/solutions/oci-best-practices/deploy-multicloud-oci-oracle-database-services1.html)

### 標準とコミュニティ

- [ISO/IEC 22123-1 — Cloud computing: Concepts and terminology](https://www.iso.org/standard/82758.html) — マルチクラウドの公式定義
- [ISO/IEC 22123-3 — Multi-cloud reference architecture](https://www.iso.org/standard/90339.html) — マルチクラウドリファレンスアーキテクチャ標準
- [NIST SP 500-292 — Cloud Computing Reference Architecture](https://www.nist.gov/publications/nist-cloud-computing-reference-architecture) — クラウドリファレンスアーキテクチャ
- [NIST Multi-Cloud Security Public Working Group](https://www.nist.gov/publications/nist-cloud-computing-reference-architecture) — マルチクラウドセキュリティリファレンス
- [CNCF Annual Survey 2024](https://www.cncf.io/reports/cncf-annual-survey-2024/) — クラウドネイティブ採用状況、マルチクラウド統計
- [FinOps Foundation — FOCUS Specification](https://finops.org/framework) — マルチクラウドコストデータの標準化
- [Cloud Security Alliance — Security Guidance](https://cloudsecurityalliance.org/research/guidance) — マルチクラウドセキュリティガイド
