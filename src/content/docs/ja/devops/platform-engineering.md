---
title: "プラットフォームエンジニアリング"
description: "プラットフォームエンジニアリングとIDP(Internal Developer Platform)の概念、ツール、マルチクラウド標準化について説明します。"
---

> 文書基準: 2026年8月

## 概要

:::note[前提知識と関連ドキュメント]
このドキュメントは、[DevOpsを始める](../../devops/getting-started/)のCI/CD・自動化の概念と[Kubernetes運用](../../devops/kubernetes-operations/)を前提とする発展的なトピックです。基本的なパイプラインの概念は、それらのドキュメントを先に参照してください。本ドキュメントは、開発者セルフサービスのための内部開発者プラットフォーム(IDP)の構築に焦点を当てます。
:::

[DevOps](../../devops/getting-started/)が「開発と運用の協働」だとすれば、**プラットフォームエンジニアリング**は「開発者がインフラを意識せずセルフサービスでデプロイできるプラットフォームを作ること」です。

開発者がJiraチケットを開いてインフラチームに依頼する代わりに、プラットフォームが提供するGolden Pathに沿って自ら環境をプロビジョニングします。

## IDP (Internal Developer Platform)

| コンポーネント | 役割 | 主要ツール |
| --- | --- | --- |
| **開発者ポータル** | サービスカタログ、所有者の追跡、オンボーディング | Backstage (CNCF Incubating), Port, Cortex |
| **インフラセルフサービス** | PRで環境をリクエスト → 自動プロビジョニング | Crossplane, Terraform + Atlantis, Pulumi Operator |
| **Golden Path** | 推奨アーキテクチャテンプレートによる迅速な開始 | Backstage Software Templates, Cookiecutter |
| **CI/CDパイプライン(共通)** | 標準化されたビルド/デプロイパイプラインのテンプレート | Argo CD, Flux, Tekton, GitHub Actions reusable workflows |
| **シークレット管理** | ベンダーシークレットをK8s/アプリに注入 | External Secrets Operator, HashiCorp Vault |
| **可観測性スタック** | メトリクス、ログ、トレースの統合収集 | OpenTelemetry, Prometheus, Grafana, Loki |
| **ポリシーエンジン(ガードレール)** | セキュリティ/コスト/コンプライアンスの自動強制 | OPA/Gatekeeper, Kyverno, Checkov, tfsec |
| **コスト可視化** | チーム/サービス別コスト配賦、アラート | OpenCost, Kubecost, Infracost |
| **環境管理** | 一時環境(プレビュー環境)の作成/削除 | Argo CD ApplicationSet, vCluster |
| **内部モジュールレジストリ** | 検証済みのTerraformモジュール、Helmチャート | Terraform Registry (private), Harbor |

### オープンソースエコシステムマップ

**ポータル&カタログ:**
- Backstage (Spotify、CNCF Incubating) — 最も広いエコシステム、豊富なプラグイン
- Port — SaaS、コード不要
- Cortex — SaaS、スコアカードに強み

**GitOps&デプロイ:**
- Argo CD — K8sデプロイの標準、マルチクラスター
- Flux — 軽量、CNCF Graduated
- Tekton — K8sネイティブCI/CDパイプライン

**インフラ抽象化:**
- Crossplane — K8s CRDでクラウドリソースを管理、マルチクラウド
- Terraform + Atlantis — PRベースのplan/apply自動化

**ポリシー&ガバナンス:**
- OPA/Gatekeeper — K8s Admission Control
- Kyverno — YAMLベースのポリシー(OPAより導入障壁が低い)

**可観測性:**
- OpenTelemetry — ベンダー中立の計測標準(CNCF Graduated)
- Prometheus + Grafana — メトリクス収集/可視化の事実上の標準

**シークレット:**
- HashiCorp Vault — 最も成熟、マルチクラウド
- External Secrets Operator — K8sでベンダーシークレットマネージャーと連携

## マルチクラウド標準化

プラットフォームエンジニアリングの中核的な価値の1つは、**ベンダー間の差異を抽象化する**ことです。

| 抽象化レイヤー | 方法 | ツール |
| --- | --- | --- |
| **インフラプロビジョニング** | ベンダー中立IaC | [Crossplane](https://www.crossplane.io/) (K8sネイティブ), Terraformモジュール |
| **デプロイ** | 統合GitOps | Argo CD (マルチクラスター) |
| **シークレット** | 統合シークレット管理 | External Secrets Operator |
| **可観測性** | 統合メトリクス/ログ | OpenTelemetry + Grafana |

## Platform as a Product

プラットフォームチームは、内部の開発者を「顧客」とみなし、プラットフォームを「製品」として運用します。

- **ユーザーフィードバック** — 定期的に開発者満足度調査を実施
- **SLO** — プラットフォーム自体の可用性/応答時間目標を設定
- **ロードマップ** — 機能の優先順位をユーザーニーズに基づいて決定
- **ドキュメント化** — セルフサービスガイド、APIドキュメント、トラブルシューティングガイド

## よくある間違い

- **開発者のフィードバックなしにプラットフォームを構築** — 誰も使わない内部ツールになります。初期から開発者をユーザーとして参加させ、フィードバックループを作りましょう。
- **Golden Pathを強制してすべての例外を遮断** — 柔軟性がないと開発者が回避します。ガードレール(禁止事項)とGolden Path(推奨経路)を区別しましょう。
- **プラットフォームチームがすべてのインフラリクエストを直接処理** — チケットキューがボトルネックになります。セルフサービス自動化がプラットフォームエンジニアリングの中核です。

## チェックリスト

- [ ] 開発者がインフラチームへのチケット依頼なしに環境をセルフサービスで作成できるか?
- [ ] プラットフォーム自体のSLO(可用性、デプロイパイプライン成功率)が定義されているか?
- [ ] 定期的な開発者満足度調査とフィードバック反映プロセスがあるか?

## 参考資料

### 標準とコミュニティ

- [CNCF Platforms White Paper](https://tag-app-delivery.cncf.io/whitepapers/platforms/)
- [Backstageドキュメント](https://backstage.io/docs/)
- [Crossplaneドキュメント](https://docs.crossplane.io/)
- [Humanitec Platform Orchestrator](https://humanitec.com/)
- [Team Topologies — Platform Teams](https://teamtopologies.com/)
