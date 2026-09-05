---
title: "LLMライセンスとコスト管理"
description: "FM提供社別のライセンスティア(Seat/API)、3P予約キャパシティ、コスト管理ツールとパターンを整理します。"
---

> 文書基準: 2026年8月

## SeatプランとAPIティア

:::note[前提知識と関連ドキュメント]
ファウンデーションモデルとプラットフォームの基本は[AIを始める](../../ai/getting-started/)、ファーストパーティ/サードパーティモデルの選択は[1P vs 3P](../../ai/1p-vs-3p/)を先に参照してください。本ドキュメントは、FMのライセンス等級とコスト管理に焦点を当てます。
:::

Seat(座席単位)とAPI(トークン単位)は別個の課金体系です。ほとんどのエンタープライズは両方を併用します。

### OpenAI — Seatベース

| プラン | 価格 | 対象 | Businessとの違い |
| --- | --- | --- | --- |
| **Business** (旧Team) | ~$25/席/月 | 小規模チーム (2席+) | — |
| **Enterprise** | ~$45-75/席/月 (交渉制、150席+) | 大規模組織 | SSO/SCIM, RBAC, 監査ログ, EKM, データレジデンシー, カスタムSLA, HIPAA構成 |

**Business → Enterpriseへのアップグレード時期:**
- 150席以上、またはセキュリティ/コンプライアンス要件(SSO必須、監査ログ、データレジデンシー)
- HIPAA対象データの処理が必要
- 組織全体のガバナンス(役割別権限、グループ別クレジット上限)

### OpenAI — APIティア

APIは累積支出額に応じて自動的に昇格します。([公式Rate Limits文書](https://platform.openai.com/docs/guides/rate-limits))

| ティア | 条件 | 月間利用上限 | RPM/TPM水準 |
| --- | --- | --- | --- |
| Free | 許可地域 | $100/月 | 低い |
| Tier 1 | $5支出 | $100/月 | 中程度 |
| Tier 2 | $50支出 | $500/月 | 中程度+ |
| Tier 3 | $100支出 | $1,000/月 | 高い |
| Tier 4 | $250支出 | $5,000/月 | 高い+ |
| Tier 5 | $1,000支出 | $200,000/月 | 最大 |

:::note
モデル別の正確なRPM/TPM上限は[Organization Limitsページ](https://platform.openai.com/settings/organization/limits)で確認してください。
:::

### Anthropic — Seatベース

| プラン | 価格 | 対象 | Teamとの違い |
| --- | --- | --- | --- |
| **Team Standard** | ~$25/席/月 ([公式価格](https://claude.com/pricing)) | 小規模チーム (最小座席数・上限は公式ページで確認) | — |
| **Team Premium** | ~$125/席/月 ([公式価格](https://claude.com/pricing)) | 高使用量チーム | より高い使用量を許可 |
| **Enterprise** | 座席 + API使用量等の契約型 ([公式案内](https://claude.com/pricing)) | 大規模組織 | SCIM, 監査ログ, Compliance API, CMEK, HIPAA/BAA, 組織別支出上限 |

**Team → Enterpriseへのアップグレード時期:**
- HIPAA/BAAが必要
- SCIMベースのユーザープロビジョニング
- 監査ログ + Compliance API
- 暗号鍵の直接管理(CMEK)

### Anthropic — APIティア

| ティア | レベル | 備考 |
| --- | --- | --- |
| **Start** | 入門 | 低いRPM/TPM |
| **Build** | 開発/テスト | 中程度 |
| **Scale** | プロダクション | 高いRPM/TPM、Enterprise契約でカスタム可能 |

公式Rate Limits: [platform.claude.com/docs/en/api/rate-limits](https://platform.claude.com/docs/en/api/rate-limits)

---

## 3Pチャネル予約キャパシティ

| ベンダー | 方式 | 適した時期 |
| --- | --- | --- |
| **Azure PTU** (Provisioned Throughput Unit) | 固定の時間単位課金、スループット保証 | 月1.5–2億+トークン以上の安定トラフィック |
| **Bedrock Provisioned Throughput** | モデルユニット予約 (1/6か月コミット) | 大量の安定ワークロード + レイテンシ保証 |
| **Bedrock On-demand** | トークン単位課金、予約なし | バースト/実験/不規則ワークロード |

:::note
予約キャパシティ(PTU、Provisioned)は使用しなくてもコストが発生します。正確な価格と損益分岐点はベンダーの公式ページを確認してください。
:::

---

## コストと利用量の管理

### チャネル別管理ツール

| チャネル | コストトラッキング | 予算/アラート | チーム別割り当て |
| --- | --- | --- | --- |
| **OpenAI** | Platform Usage Dashboard | プロジェクト別の月間予算上限 | Projects + API Keys |
| **Anthropic** | Console使用量ダッシュボード | ワークスペース別支出キャップ | Workspaces |
| **Azure Foundry** | Microsoft Cost Management | Azure Budgets + アラート | リソースタグ (`project`, `team`) |
| **Bedrock** | AWS Cost Explorer + CUR 2.0 | AWS Budgets + Cost Anomaly Detection | 推論プロファイル + コスト配分タグ |

### エンタープライズコスト管理パターン

| パターン | 説明 |
| --- | --- |
| **Showback** | チーム別使用量を可視化するが、実際の請求は行わない。意識向上が目的 |
| **Chargeback** | チーム予算から実際に控除。エージェントコストの暴走防止に効果的 |
| **モデルルーティング** | 単純な作業は軽量モデル、複雑な作業のみフロンティアモデルに分岐 |
| **トークン予算** | プロジェクト/チーム/ユーザー別の日次/月次トークン上限 |
| **AIゲートウェイ** | LiteLLM、Portkey等で仮想キーを発行し、ハード予算、ルーティング制御 |

---

## 関連ドキュメント

- [LLMチャネル選択ガイド](../../ai/1p-vs-3p/) — チャネルパターン、Seat vs API選択
- [AIプラットフォームとモデル比較](../../ai/ai-ml/) — モデルカタログ、推論コスト最適化
- [FinOps](../../governance/finops/) — クラウドコストガバナンス全般
- [エージェント導入ガイド](../../ai/agent-adoption/) — エージェントコスト管理

## 参考資料

Seat/API価格・最小座席数・ティア上限は随時変わります。以下の公式ページを基準に確認してください。

### モデル提供社

- [OpenAI Business/Enterprise価格](https://openai.com/business/pricing/)
- [OpenAI API価格](https://openai.com/api/pricing/)
- [Anthropic (Claude) プラン](https://claude.com/pricing)
- [Anthropic API価格](https://platform.claude.com/docs/en/about-claude/pricing)
- [Upstage Console](https://console.upstage.ai/)

### クラウドチャネル

- [Amazon Bedrock価格](https://aws.amazon.com/bedrock/pricing/)
- [Azure OpenAI価格](https://azure.microsoft.com/en-us/pricing/details/azure-openai/)
- [Google Cloud Vertex AI価格](https://cloud.google.com/vertex-ai/pricing)
- [OCI Generative AI価格](https://www.oracle.com/artificial-intelligence/generative-ai/generative-ai-service/pricing/)
