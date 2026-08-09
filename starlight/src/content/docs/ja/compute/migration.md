---
title: "アプリケーションマイグレーション"
description: "ワークロードマイグレーション戦略(7R)、評価/実行段階、リフト&シフト vs リファクタリングのトレードオフをベンダー別に比較します。"
---

> 文書基準: 2026年5月

## 概要

オンプレミスまたは別のクラウドにあるアプリケーションとインフラをクラウドへ移行する作業です。単純にVMをコピーするのではなく、アプリケーションのアーキテクチャ、依存関係、運用方式全体を再評価するプロセスです。

:::note
データベースマイグレーションは[データベースマイグレーション](../../database/migration/)、大容量ファイルの移行は[ストレージマイグレーション](../../storage/migration/)を参照してください。
:::

:::caution
マイグレーション前に**ガバナンス基盤を先に準備してください。** アカウント/組織構造、ネットワーク(VPC/サブネット)、IAMポリシー、タグ体系、ロギングがない状態でワークロードを移すと、後ですべて再構成する必要があります。[クラウドガバナンスを始める](../../governance/getting-started/) → [ランディングゾーン](../../governance/landing-zone/)を先に確認してください。
:::

## 7Rマイグレーション戦略

Gartnerが提示しAWSが拡張した**7Rフレームワーク**は、ワークロードごとのマイグレーション戦略を分類する標準です。

| 戦略 | 説明 | 難易度 | 効果 |
| --- | --- | --- | --- |
| **Retire** (廃止) | もはや不要なワークロードを停止 | 低 | 即座にコスト削減 |
| **Retain** (維持) | オンプレミスを維持 (ハイブリッド) | 低 | マイグレーションコストなし |
| **Relocate** (再配置) | ハイパーバイザーレベルでそのまま移動 (例: VMware Cloud on AWS) | 低 | 最小限の変更で迅速な移行 |
| **Rehost** (リホスト) | VM単位のLift & Shift | 低 | 迅速な移行、クラウドの利点は限定的 |
| **Replatform** (リプラットフォーム) | マネージドサービスへ一部転換 (例: DBをRDSへ) | 中 | 運用負担の軽減 |
| **Repurchase** (再購入) | SaaSへの切り替え (例: 自社CRM → Salesforce) | 中 | 運用責任の委譲 |
| **Refactor** (リファクタリング) | クラウドネイティブに再設計 (サーバーレス、マイクロサービス) | 高 | 拡張性/効率性の最大化 |

### 戦略選択の基準

| 状況 | 推奨戦略 |
| --- | --- |
| データセンター撤退の期限が迫っている | RelocateまたはRehost |
| ビジネス価値が低く寿命が短いワークロード | Retire |
| 既に商用ソリューションがある機能 | Repurchase (SaaS) |
| クラウドの利点(拡張性、コスト)を最大化したいコアワークロード | Refactor |
| 変更なしで安定運用を望むレガシー | Retain |
| 運用負担を減らしたいがコードは維持 | Replatform |

:::caution
**注意:** すべてのワークロードをRefactorしようとすると、時間とコストが急増します。ほとんどの企業は**Rehost/Replatformを基本とし、コアワークロードのみRefactor**するハイブリッドアプローチを使用します。
:::

## リフト&シフト vs リファクタリングのトレードオフ

最も一般的な選択肢であるRehost(Lift & Shift)とRefactorの比較です。

| 項目 | Rehost (Lift & Shift) | Refactor (クラウドネイティブ) |
| --- | --- | --- |
| **移行期間** | 数週間~数ヶ月 | 数ヶ月~数年 |
| **開発コスト** | 低 (変更最小限) | 高 (再設計/再実装) |
| **運用コスト** | オンプレミスと同程度 | クラウド最適化で削減可能 |
| **拡張性** | 限定的 (VM単位) | 高い (サーバーレス、水平拡張) |
| **障害復旧** | 既存方式を維持 | クラウドネイティブHA/DR |
| **リスク** | 低 | 高 (再設計失敗の可能性) |
| **クラウドの利点の活用** | 限定的 | 最大 |
| **データセンター撤退の期限** | 短くても対応可能 | 長い期間が必要 |

:::note
**一般的なパターン:** データセンター撤退の期限がある場合は、**まずRehostで移行した後、安定化後に段階的にReplatform/Refactor**する戦略が現実的です。最初からすべてのワークロードをRefactorすると、スケジュール遅延や品質問題が発生しやすくなります。
:::

## マイグレーションプロセス

大規模マイグレーションは複数の段階を経るプロジェクトです。

| 段階 | 主な活動 |
| --- | --- |
| **1. Discovery** | インベントリ収集 — サーバー、アプリケーション、依存関係、利用状況の把握 |
| **2. Assessment** | ワークロードごとの7R戦略決定、コスト見積もり、リスク分析 |
| **3. Planning** | マイグレーション順序(Wave)の決定、ロールバック計画、ダウンタイム予算 |
| **4. Landing Zone** | クラウドアカウント/ネットワーク/セキュリティ基盤の構成 ([ランディングゾーン](../../governance/landing-zone/)参照) |
| **5. Migration** | 実際のデータ/アプリケーション移行 |
| **6. Validation** | パフォーマンス/機能テスト、ユーザー受け入れテスト |
| **7. Cutover** | トラフィック切り替え、モニタリング強化 |
| **8. Optimize** | クラウド環境の最適化 (コスト、パフォーマンス、セキュリティ) |

### マイグレーションウェーブ (Wave)

数百~数千のワークロードを一度に移行するのはリスクがあります。通常は**ウェーブ(Wave)** 単位に分けて進めます。

- **Pilot Wave** — シンプルでリスクの低いワークロードで経験を蓄積 (例: 内部ツール、開発環境)
- **Core Waves** — アプリケーショングループ単位でまとめて順次移行
- **Critical Wave** — ビジネスクリティカルなワークロードは最後に移行 (十分な検証後)

## ダウンタイムの最小化

本番ワークロードはダウンタイムを最小化する必要があります。

| 技法 | 説明 | 使用時期 |
| --- | --- | --- |
| **ブロックレベル連続レプリケーション** | ソースVMの変更ブロックを継続的に対象へレプリケート | ほとんどのVMマイグレーションツールのデフォルト方式 |
| **Blue/Green切り替え** | 旧インフラと新インフラを並行運用した後DNS/LBで切り替え | Webサービス、API |
| **データベースCDC** | DBの変更を継続的にレプリケートし、Cutover時に数分以内に切り替え | DBマイグレーション |
| **段階的Cutover** | ユーザー/地域/機能ごとに段階的に切り替え | 大規模ユーザー向けサービス |

## Cutoverチェックリスト

実際の切り替え時点で確認すべき項目です。

- [ ] データ整合性検証完了 (チェックサム、レコード数)
- [ ] アプリケーション機能テスト完了
- [ ] パフォーマンスベンチマークが既存環境以上
- [ ] セキュリティ設定(IAM、ファイアウォール、暗号化)の検証
- [ ] バックアップ/DR構成完了
- [ ] モニタリングおよび通知の動作確認
- [ ] ロールバック計画およびロールバック時点の決定
- [ ] 関係者への通知およびGo/No-Go承認
- [ ] Cutover時間帯(週末/夜間)の確定
- [ ] 障害発生時の対応要員待機

## マイグレーションツール

:::note
**AI支援マイグレーション:** 各CSPはAIを活用してマイグレーション評価・コード変換・テストを自動化するサービスを提供しています。[AWS Transform](https://aws.amazon.com/transform/)(AIベースのコード変換)、[Azure Migrate with Copilot](https://learn.microsoft.com/azure/migrate/)(評価自動化)、[Google Cloud Dual Run](https://cloud.google.com/blog/products/databases/dual-run-for-mainframe-modernization)(メインフレーム並行検証)などが代表的です。大規模レガシー転換時に手作業での分析時間を大幅に短縮できますが、AI成果物に対する検証は依然として必要です。
:::

### 評価および発見

| ベンダー | 製品 | 機能 |
| --- | --- | --- |
| AWS | [Application Discovery Service](https://aws.amazon.com/application-discovery/) | エージェント/エージェントレス方式でオンプレミスインベントリを収集 |
| AWS | [Migration Hub](https://aws.amazon.com/migration-hub/) | マイグレーション中央ダッシュボード |
| Azure | [Azure Migrate](https://azure.microsoft.com/products/azure-migrate/) | 評価、サーバー/DBマイグレーション統合 |
| Google Cloud | [Migration Center](https://cloud.google.com/migration-center/docs) | ポートフォリオ評価、依存関係マッピング |
| OCI | [Cloud Migrations](https://docs.oracle.com/en-us/iaas/Content/cloud-migration/home.htm) | 評価および実行統合 |

### VM/サーバーマイグレーション

| ベンダー | 製品 | 機能 |
| --- | --- | --- |
| AWS | [Application Migration Service (MGN)](https://aws.amazon.com/application-migration-service/) | ブロックレベルレプリケーション。最小ダウンタイムRehost |
| Azure | [Azure Migrate: Server Migration](https://learn.microsoft.com/azure/migrate/migrate-services-overview) | VMware/Hyper-V/物理サーバー → Azure VM |
| Google Cloud | [Migrate to Virtual Machines](https://cloud.google.com/migrate/virtual-machines/docs) | VMware/AWS/Azure → Compute Engine |
| OCI | [OCI Cloud Migrations](https://docs.oracle.com/en-us/iaas/Content/cloud-migration/home.htm) | VMware/AWS → OCI |

### コンテナ化

| ベンダー | 製品 | 機能 |
| --- | --- | --- |
| AWS | [App2Container](https://aws.amazon.com/app2container/) | Java/.NETアプリをコンテナ化 |
| Azure | [Migrate to containers](https://learn.microsoft.com/azure/migrate/tutorial-app-containerization-aspnet-kubernetes) | ASP.NET/Java → AKS |
| Google Cloud | [Migrate to Containers](https://cloud.google.com/migrate/containers/docs) | VM → GKEコンテナ |

## よくある間違い

- **Discovery/Assessmentなしで直接マイグレーション開始** — 依存関係とトラフィックパターンを把握しないと、切り替え後に障害が発生しロールバックが必要になります。
- **ランディングゾーンなしでワークロードを先に移行** — アカウント構造、ネットワーク、IAM、タグ体系がない状態で移すと、後ですべて再構成する必要があります。
- **すべてのワークロードを同時にRefactorしようとする** — スケジュールが崩れ、品質問題が発生します。ほとんどの場合Rehost後に段階的に改善するのが現実的です。

## 参考資料

### AWS

- [AWS Cloud Migration](https://aws.amazon.com/cloud-migration/)
- [AWS Migration Hub](https://aws.amazon.com/migration-hub/)
- [AWS Application Migration Service](https://aws.amazon.com/application-migration-service/)
- [AWS Prescriptive Guidance: Migration Strategies (7R)](https://docs.aws.amazon.com/prescriptive-guidance/latest/large-migration-guide/migration-strategies.html)

### Azure

- [Azure Migrate](https://azure.microsoft.com/products/azure-migrate/)
- [Cloud Adoption Framework — Migrate](https://learn.microsoft.com/azure/cloud-adoption-framework/migrate/)
- [Azure Migrate 文書](https://learn.microsoft.com/azure/migrate/)

### Google Cloud

- [Migration Center](https://cloud.google.com/migration-center/docs)
- [Migrate to Virtual Machines](https://cloud.google.com/migrate/virtual-machines/docs)
- [Migrate to Containers](https://cloud.google.com/migrate/containers/docs)

### OCI

- [OCI Cloud Migrations](https://docs.oracle.com/en-us/iaas/Content/cloud-migration/home.htm)
- [OCI Migration Solutions](https://www.oracle.com/cloud/migration/)
