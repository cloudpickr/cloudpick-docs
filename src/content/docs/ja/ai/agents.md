---
title: "AIエージェント"
description: "AIエージェントの概念、アーキテクチャ、プロトコル、ベンダープラットフォーム、コーディング/Desktop/自律運用エージェントを比較します。"
---

> 文書基準: 2026年7月

## プロンプティングからエージェントへ

従来のLLMは**1回のプロンプト → 1回の応答**という構造です。AIエージェントは**目標を受け取ると自ら計画を立て、ツールを呼び出し、結果を検証し、必要であれば再試行する**自律的な実行ループを持ちます。

| 区分 | LLMプロンプティング | AIエージェント |
| --- | --- | --- |
| 実行方式 | 単一リクエスト-レスポンス | 多段階ループ(観察→思考→行動→繰り返し) |
| 外部連携 | 限定的 | ツール呼び出し(API、DB、ファイルシステム) |
| 自律性 | ユーザーが各ステップを指示 | 目標だけ与えれば自ら分解・実行 |

**エージェントが不要な場合:** 単純な質疑応答、定型化されたパイプライン(Step Functionsなど)、リアルタイム応答が必要な場合。

---

## エージェントの種類

| 種類 | 対象 | 例 | 特徴 |
| --- | --- | --- | --- |
| **Desktop Agent** (業務) | 全社員 | Claude Cowork、Amazon Quick、ChatGPT Work、M365 Copilot、Gemini | ローカルファイル・アプリへのアクセス、Computer Use、MCPコネクタ |
| **Coding Agent** (開発) | エンジニアリング | Kiro、Claude Code、Codex、Grok Build、Copilot、Antigravity、OpenCode | ターミナル/IDE/Git、コード生成・修正・テスト・PR |
| **自律運用エージェント** | DevOps/セキュリティ/FinOps | AWS DevOps/Security/FinOps Agent、Security Copilot、Google SecOps Agents | 数時間~数日の自律実行、常時の人的監督なし |

### Desktop Agent — なぜ登場したのか

LLMチャットはブラウザの中に閉じ込められていました。Desktop Agentは、ローカルファイルへのアクセス、OS操作(Computer Use)、外部ツール連携(MCP)、長時間の自律実行によってこの限界を超えます。

| 区分 | セルフホスティング (OpenClaw、Hermesなど) | マネージド (Claude Cowork、Quick、Copilot) |
| --- | --- | --- |
| デプロイ | ユーザーが直接インストール | ITがMDM/SSOで一括デプロイ |
| モデル | ローカル/個人APIキー | ベンダーホスティング(フロンティアモデル) |
| データ統制 | ローカル制御(組織ポリシーの適用が困難) | DLP、コネクタ許可リスト、監査ログ |
| メリット | プライバシー、カスタマイズ性 | ガバナンス、フロンティアモデル、企業ツール統合 |

:::note
エンタープライズDesktop Agentの満足度は、**モデル性能よりもITによるデータソース接続範囲**に左右されます。この設定を組織単位で体系的に行うのがAXです — [エージェント導入ガイド](../../ai/agent-adoption/)参照。
:::

### 自律運用エージェント

各クラウドベンダーがドメイン特化型の自律エージェントをリリースしています。AWSは「Frontier Agent」、Microsoftは「Copilot Agents」、Googleは「AI Agents」としてブランディングしています。

| ドメイン | AWS | Microsoft | Google Cloud |
| --- | --- | --- | --- |
| セキュリティ | Security Agent (GA) | Security Copilot Agents (GA) | Security Operations Agents (プレビュー) |
| DevOps/SRE | DevOps Agent (GA) | Azure Copilot | — |
| FinOps | FinOps Agent (プレビュー) | Azure Copilot コスト最適化 | — |
| コーディング | Kiro (IDE/CLI/Web) | GitHub Copilot | Antigravity |

---

## アーキテクチャパターン

| パターン | 説明 | 適した場合 |
| --- | --- | --- |
| **ReAct** | 推論と行動を交互に実行 | 単一エージェント、単純なツール呼び出し |
| **Plan-and-Execute** | 全体計画を立ててから順次実行 | 複雑な多段階作業 |
| **マルチエージェント** | 役割別の専門エージェントが協業 | 大規模ワークフロー、ドメイン分離 |
| **Human-in-the-Loop** | 危険な行動の前に人が承認 | プロダクション、高リスク作業 |

---

## エージェントプロトコル — MCP、A2A、ACP

| プロトコル | 役割 | 要点 |
| --- | --- | --- |
| [MCP](https://modelcontextprotocol.io/) | エージェント → ツール/データ | JSON-RPC 2.0、Tools/Resources/Prompts。事実上の標準 |
| [A2A](https://github.com/google/A2A) | エージェント → エージェント(クロスベンダー) | Agent Card、Task Lifecycle、SSE/gRPC |
| [ACP](https://agentcommunicationprotocol.dev/) | エージェント → エージェント(社内ピア) | RESTネイティブ、SDK不要 |

3つのプロトコルはいずれも[AAIF (Linux Foundation)](https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation)のガバナンス下にあります。

---

## ベンダー別エージェントプラットフォーム

| ベンダー | プラットフォーム | 特徴 |
| --- | --- | --- |
| AWS | [Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/) | フレームワーク非依存、Harness、Memory、Gateway、MCP |
| Azure | [Microsoft Foundry Agents](https://learn.microsoft.com/azure/ai-foundry/agents/) | Responses API、MCP、Agent 365ガバナンス |
| Google | [Gemini Enterprise Agent Platform](https://cloud.google.com/products/agent-builder) | ADK(オープンソース)、A2Aネイティブ、Agent Runtime |
| OCI | [OCI Enterprise AI Agents](https://docs.oracle.com/iaas/Content/generative-ai/agents.htm) | RAGエージェント、Oracle DB連携、AI Guardrails |

### オープンソースフレームワーク

| フレームワーク | 特徴 |
| --- | --- |
| [LangGraph](https://github.com/langchain-ai/langgraph) | ステートマシンベースのマルチエージェント |
| [CrewAI](https://github.com/crewAIInc/crewAI) | 役割ベースの協業 |
| [Strands Agents](https://strandsagents.com/) | AWSオープンソース、モデル非依存 |
| [AutoGen](https://github.com/microsoft/autogen) | Microsoft、対話型マルチエージェント |

---

## コーディングエージェント

| 製品 | 提供社 | 特徴 |
| --- | --- | --- |
| [Kiro](https://kiro.dev/) | AWS | Spec-driven、Hooks、IDE/CLI/Web |
| [Claude Code](https://github.com/anthropics/claude-code) | Anthropic | Agent Teams、29 hooks、プラグイン |
| [Codex](https://openai.com/codex/) | OpenAI | 並列エージェント、Computer Use |
| [Grok Build](https://x.ai/news/grok-build-cli) | xAI | 8並列サブエージェント、Git worktree分離 |
| [GitHub Copilot](https://github.com/features/copilot) | Microsoft | Agent Mode、Agent Merge、Cloud Sessions |
| [Antigravity](https://antigravity.google/) | Google | Agent-first IDE、Managed Agents |
| [OpenCode](https://opencode.ai/) | Anomaly | オープンソース、モデル非依存 |

---

## デプロイと運用

| 項目 | 内容 |
| --- | --- |
| **コスト** | ループ実行によりトークンを数倍~数十倍消費。タスクごとの予算、ループ制限、モデル階層化が必要 |
| **評価** | タスク成功率、ツール選択精度、ハルシネーション率。ベンダー別評価サービスを活用 |
| **可観測性** | OpenTelemetryベースのトレーシング。エージェント特化の指標は[LLMOps](../../ai/llmops/)参照 |
| **セキュリティ** | プロンプトインジェクション、権限昇格、データ流出、無限ループ。詳細は[AIセキュリティ](../../security/ai-security/)参照 |

### Desktop Agent固有のリスク

| リスク | 対応 |
| --- | --- |
| 長時間実行によるコスト急増 | セッション予算、自動停止 |
| クロスアプリインジェクション | コネクタ許可リスト、入力サニタイズ |
| 自律エージェントのドリフト | チェックポイント、kill switch、diffレビュー |
| シャドーAI | 公式Desktop Agentで同等の体験を提供 |

---

## チェックリスト

- [ ] エージェントが必要な作業か判断(単純なプロンプトで十分か)
- [ ] ツールごとの最小権限 + ホワイトリスト
- [ ] ガードレール(入力/出力/実行の制限)
- [ ] Human-in-the-Loopポリシー
- [ ] トレーシング・モニタリング(OpenTelemetry)
- [ ] コスト予算とサーキットブレーカー
- [ ] 導入戦略は[エージェント導入ガイド](../../ai/agent-adoption/)参照

## 関連ドキュメント

- [エージェント導入ガイド](../../ai/agent-adoption/) — AX戦略、ロールアウト、ガバナンス
- [AIプラットフォームとモデル比較](../../ai/ai-ml/) — モデルカタログ
- [LLMOps](../../ai/llmops/) — エージェントの可観測性、評価、コスト
- [AIセキュリティ](../../security/ai-security/) — ガードレール、プロンプトインジェクション
- [LLMチャネル選定ガイド](../../ai/1p-vs-3p/) — Seat vs API、チャネルパターン

## 参考資料

- [Bedrock AgentCore](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/)
- [Microsoft Foundry Agents](https://learn.microsoft.com/azure/ai-foundry/agents/)
- [Gemini Agent Platform](https://cloud.google.com/products/agent-builder)
- [MCP](https://modelcontextprotocol.io/) · [A2A](https://github.com/google/A2A) · [ACP](https://agentcommunicationprotocol.dev/)
- [Kiro](https://kiro.dev/) · [Claude Code](https://github.com/anthropics/claude-code) · [Codex](https://openai.com/codex/)
