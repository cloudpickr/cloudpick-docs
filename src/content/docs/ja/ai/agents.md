---
title: "AIエージェント"
description: "AIエージェントの概念、アーキテクチャ、プロトコル、ベンダープラットフォーム、コーディング/Desktop/自律運用エージェントを比較します。"
---

> 文書基準: 2026年10月

## プロンプティングからエージェントへ

:::note[前提知識と関連ドキュメント]
AIが初めての場合は、[AIを始める](../../ai/getting-started/)と[プロンプトエンジニアリング](../../ai/prompt-engineering/)を先にお読みください。本ドキュメントは、その上で動作する自律エージェントの概念・アーキテクチャ・ベンダープラットフォームに焦点を当てます。組織導入戦略は[エージェント導入ガイド](../../ai/agent-adoption/)を参照してください。
:::

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
| **自律運用エージェント** | DevOps/セキュリティ/FinOps | AWS DevOps/Security/FinOps Agent、Security Copilot、Google SecOps Agents | 数時間～数日の自律実行、常時の人的監督なし |

### Desktop Agent — なぜ登場したのか

LLMチャットはブラウザの中に閉じ込められていました。Desktop Agentは、ローカルファイルへのアクセス、OS操作(Computer Use)、外部ツール連携(MCP)、長時間の自律実行によってこの限界を超えます。

| 区分 | セルフホスティング (OpenClaw、Hermesなど) | マネージド (Claude Cowork、Quick、Copilot) |
| --- | --- | --- |
| デプロイ | ユーザーが直接インストール | ITがMDM/SSOで一括デプロイ |
| モデル | ローカル/個人APIキー | ベンダーホスティング(フロンティアモデル) |
| データ統制 | ローカル制御(組織ポリシーの適用が困難) | DLP、コネクタ許可リスト、監査ログ |
| メリット | プライバシー、カスタマイズ性 | ガバナンス、フロンティアモデル、企業ツール統合 |

**Claude Cowork現況(2026.09):** macOS/Windows GA(4月) → Web・iOS・Android + クラウドリモートセッション(7月) → デスクトップアプリのサイドパネル内蔵ブラウザ(8月末発表、Pro/Max/Teamへ順次ロールアウト)。デバイス間セッション連続性とArtifacts共有をサポート。

:::note
エンタープライズDesktop Agentの満足度は、**モデル性能よりもITによるデータソース接続範囲**に左右されます。この設定を組織単位で体系的に行うのがAXです — [エージェント導入ガイド](../../ai/agent-adoption/)参照。
:::

### 自律運用エージェント

各クラウドベンダーがドメイン特化型の自律エージェントをリリースしています。AWSは「Frontier Agent」、Microsoftは「Copilot Agents」、Googleは「AI Agents」としてブランディングしています。

| ドメイン | AWS | Microsoft | Google Cloud |
| --- | --- | --- | --- |
| セキュリティ | Security Agent (GA) | Security Copilot Agents (GA) | Security Operations Agents (一部GA・新規は一部プレビュー) |
| DevOps/SRE | DevOps Agent (GA) | Azure Copilot | — |
| FinOps | FinOps Agent (プレビュー) | Azure Copilot コスト最適化 | — |
| コーディング | Kiro (IDE/CLI/Web) | GitHub Copilot | Antigravity |

### 常時稼働プロアクティブエージェントへの移行

2026年に入り、主要ベンダーが一斉に同じ方向へ製品を移しました — **リクエストに応答するチャットボット**から、ユーザーの指示を待たず**自ら先回りして動く(プロアクティブ)常時稼働(always-on)エージェント**への移行です。ここで「常時稼働」とはアプリを閉じても背景で動き続けること、「プロアクティブ」とは命令を待たずに先にやるべきことを提案・実行することを指します。

これらの製品には4つの共通点があります。

- **背景実行** — ユーザーが離席しても作業を続ける。
- **専用の実行環境** — 各エージェントが専用のクラウドコンピューターやVMで動作する。
- **先回りの点検** — 接続されたアプリ(メール・カレンダーなど)を定期的に確認し、先に提案する。
- **機微な操作の制御** — 送信・決済・削除などの操作について、人の承認と監査証跡をサポートする(承認を必須とするかは製品・組織の設定による)。

以下は各ベンダーの代表的な製品です。「区分」はコンシューマー向けか企業向けかを示します。

| 製品 | ベンダー | 公開 | 区分 | ガバナンス・セキュリティの特徴 |
| --- | --- | --- | --- | --- |
| [Muse](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/) | Meta | 2026.09 | コンシューマー | 専用Secure VMで動作。別個のSentinelエージェントが外部送信を承認し、認証情報を露出せずに利用 |
| [Scout / Autopilot](https://www.microsoft.com/en-us/copilot/blog/2026/06/02/introducing-microsoft-scout-your-always-on-personal-agent/) | Microsoft | 2026.06～09 | 企業 | 「Autopilots」という新区分。エージェント別Entra ID、認証情報のログからの削除、Purview DLPの即時適用。機微な操作の承認は組織の設定に従う |
| [Quick 常時稼働エージェント](https://aws.amazon.com/about-aws/whats-new/2026/09/amazon-quick-always-on-agents-sharper-feed-enterprise-controls/) | AWS | 2026.09 | 企業 | スケジュール・モニタリングエージェントがクラウドで常時実行。管理者制御(MDM・権限)、Purview DLP連携 |
| [Gemini Spark / Daily Brief](https://blog.google/innovation-and-ai/products/gemini-app/next-evolution-gemini-app/) | Google | 2026.05 (I/O) | コンシューマー | 24/7プロアクティブ、デイリーブリーフ。macOSアプリがローカルマシンで動作 |
| [dots](https://openai.com/devday/2026/) | OpenAI | 2026.09 (DevDay) | コンシューマー | DevDay 2026で公開された常時稼働エージェント |
| [Claude Duet](https://claude.com/resources/articles/claude-duet) | Anthropic | 2026.10 | コンシューマー/プロ | Opus 5.5ベース、デイリーブリーフ。機微な操作の前にユーザー確認。米国Pro/Maxのリサーチプレビュー(ウェイトリスト) |

:::note
この移行の核心はモデル性能ではなく、**行動境界とガバナンス**です。企業向け製品(Scout/Autopilot、Quick)はいずれもガバナンスドID、DLPの即時適用、機微な操作の承認構成を強調します。組織導入時に適用する行動境界・承認ポリシー・監査は[エージェント導入ガイド](../../ai/agent-adoption/)を、非人間IDの管理は同ドキュメントの「エージェントID」項目を参照してください。
:::

:::caution
常時稼働エージェントには2つの大きなリスクがあります。第一に、長時間の自律実行で**コストが急増**する可能性があります。第二に、外部入力を通じた**クロスアプリのプロンプトインジェクション**にさらされる可能性があります。セッション予算・自動停止、コネクタ許可リスト、送信・決済前の承認ゲートを併せて適用してください。詳細なリスクは下記の[Desktop Agent固有のリスク](#desktop-agent固有のリスク)を参照してください。
:::

---

## アーキテクチャパターン

| パターン | 説明 | 適した場合 |
| --- | --- | --- |
| **ReAct** | 推論と行動を交互に実行 | 単一エージェント、単純なツール呼び出し |
| **Plan-and-Execute** | 全体計画を立ててから順次実行 | 複雑な多段階作業 |
| **マルチエージェント** | 役割別の専門エージェントが協業 | 大規模ワークフロー、ドメイン分離 |
| **Human-in-the-Loop** | 危険な行動の前に人が承認 | プロダクション、高リスク作業 |

---

## エージェントプロトコル — MCP、A2A

| プロトコル | 役割 | 要点 |
| --- | --- | --- |
| [MCP](https://modelcontextprotocol.io/) | エージェント → ツール/データ | **2026-07-28スペック**: ステートレスコア、Extensionsフレームワーク、Tasks、MCP Apps。月4億+SDKダウンロード |
| [A2A](https://github.com/google-a2a/A2A) | エージェント → エージェント(クロスベンダー) | v1.0(2026年3月GA)。マルチプロトコルバインディング、署名付きAgent Card、150+参加組織。IBMのACPは2025年8月にA2Aへ統合(Linux Foundation) |

2つのプロトコルはいずれも[AAIF (Linux Foundation)](https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation)のガバナンス下にあります。

### MCP 2026-07-28の主な変更

MCPリリース以来最大規模の改訂です。主な変更点:

- **ステートレスコア** — プロトコルレベルのセッション(`Mcp-Session-Id`)と`initialize`ハンドシェイクを廃止。サーバーレス/エッジへのデプロイが可能に
- **Extensionsフレームワーク** — 逆引きDNS識別子による独立バージョン管理。TasksとMCP Appsが公式Extensionとして正式化
- **Tasks** — 非同期の長時間実行タスク向け標準ライフサイクル
- **MCP Apps** — サーバーレンダリングのインタラクティブUIをホストでサンドボックス実行
- **認可の強化** — OAuth 2.1ベースの認可改善
- **公式非推奨ポリシー** — Roots、Sampling、Loggingがdeprecated表示

AgentCore GatewayおよびClaude製品群ですでにサポート中。

---

## ベンダー別エージェントプラットフォーム

| ベンダー | プラットフォーム | 特徴 |
| --- | --- | --- |
| AWS | [Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/) | フレームワーク非依存、Harness(マネージド、オープンソースのStrands harnessとは別)、Memory、Gateway(ツール接続・呼び出し)、MCP |
| Azure | [Microsoft Foundry Agents](https://learn.microsoft.com/azure/ai-foundry/agents/) | Responses API、MCP、Agent 365ガバナンス |
| Google | [Gemini Enterprise Agent Platform](https://cloud.google.com/products/agent-builder) | ADK(オープンソース)、A2Aネイティブ、Agent Runtime |
| OCI | [OCI Enterprise AI Agents](https://docs.oracle.com/iaas/Content/generative-ai/agents.htm) | RAGエージェント、Oracle DB連携、AI Guardrails |

### エージェントレジストリとゲートウェイ

組織でエージェントとツールが増えると、チームごとに同じ機能を重複して作り、「誰が何を作ったか」の追跡が難しくなります。これに対処する2つの層があります — **レジストリ(Registry)** は何が存在するかを探すカタログであり、**ゲートウェイ(Gateway)** はツール呼び出しが実際に通過するランタイムの入口です。両者は代替ではなく補完の関係です。

| 区分 | エージェントレジストリ | エージェントゲートウェイ |
| --- | --- | --- |
| 役割 | 発見・メタデータカタログ・ガバナンス | ツール呼び出し中継・プロトコル変換・ランタイム認証 |
| 扱うもの | エージェント・ツール・スキル・MCPサーバーのレコード(所有者、プロトコル、公開機能、呼び出し方法) | REST・Lambda・Smithy・MCPを呼び出し可能なMCPツールに変換 |
| 主な作業 | 検索、公開承認(キュレーション)、所有権追跡 | ingress・egress認証、ルーティング、監査ログ |

:::note
レジストリへの登録は「何が存在するか」を識別するものであり、実行権限を付与するものではありません。呼び出し時点の権限・隔離はゲートウェイとランタイムガードレールが別途担当します。全社的なエージェントガバナンスの構築手順は[エージェント導入ガイド](../../ai/agent-adoption/)を参照してください。
:::

主要ベンダーがレジストリ/ディレクトリサービスを提供しており、多くは自社だけでなく他プロバイダー・オンプレミスのエージェントまで登録範囲を広げています。ただし強調点はベンダーごとに異なります。

| ベンダー | サービス | 状態・焦点 |
| --- | --- | --- |
| AWS | [Agent Registry](https://aws.amazon.com/bedrock/agentcore/) (Bedrock AgentCore) | 2026.08 GA。エージェント・ツール・スキル・MCPサーバーのカタログ、キュレーター承認、IAM・OAuth(JWT) |
| Google Cloud | [Agent Registry](https://docs.cloud.google.com/agent-registry/overview) (Gemini Enterprise Agent Platform) | GA。MCPサーバー・ツール・エージェントのカタログ、ランタイム自動登録(一部Preview) |
| Microsoft | [Entra Agent Registry](https://learn.microsoft.com/entra/agent-id/identity-platform/what-is-agent-registry) (Entra Agent ID) | Preview。ID・ディレクトリの観点 — 他社ビルダー・マルチプラットフォームのエージェントのインベントリ可視性 |

:::note[誰に適しているか]
- **エージェントを作る人(開発者・非開発者)** — 必要な機能が既にあるかを検索して再利用し、インストール前にそのエージェント・ツールが何をするかをレコードで確認します。自分が作ったものを登録すれば、組織内で発見・再利用される資産になります。キュレーションが有効なレジストリでは、公開はレビューを経てから検索に表示されます。
- **IT・プラットフォーム管理** — 組織全体のエージェント・ツール・MCPサーバーのインベントリと公開承認プロセスを運用し、IAM・OAuth認証と暗号化・監査でアクセスを統制します。可視性の範囲は登録・収集の対象によって変わるため、実行統制はゲートウェイ・ランタイムポリシーで別途適用します。
:::

### オープンソースフレームワーク

| フレームワーク | 特徴 |
| --- | --- |
| [LangGraph](https://github.com/langchain-ai/langgraph) | ステートマシンベースのマルチエージェント |
| [CrewAI](https://github.com/crewAIInc/crewAI) | 役割ベースの協業 |
| [Strands Agents](https://strandsagents.com/) | AWSオープンソース、モデル非依存。SDK(部品を自ら組み立て)+ harness(組み合わせ層。`create_harness()`で完成形エージェントを返す、公開2026-09-21) |
| [AG2](https://ag2.ai/)(旧AutoGen) | コミュニティフォーク、オープンソースAgentOS |
| [Microsoft Agent Framework](https://learn.microsoft.com/agent-framework/) | AutoGen後継、2026.04 GA |

:::note[Strandsの3層構造]
- **SDK** — エージェントの構成要素(部品)を自ら組み立てるライブラリ。
- **harness** — SDK上の薄い組み合わせ層。ツール・コンテキスト・セッション・メモリ・フックとシステムプロンプトを構成した標準のStrands Agentを返し、すべてのデフォルト設定は変更できます。
- **Bedrock AgentCore** — エージェントをマネージド環境でホストする別のランタイム層。

harnessはローカルでも任意のクラウドでも実行できます。
:::

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

:::note
Claude Codeは100万（1M）トークンのコンテキストをサポートします（2026年3月GA）。Max・Team・Enterpriseプランでは大規模コードベース全体を1セッションで扱うのに活用でき、対応モデル・条件は[公式文書](https://claude.com/blog/1m-context-ga)で確認してください。
:::

---

## デプロイと運用

| 項目 | 内容 |
| --- | --- |
| **コスト** | ループ実行によりトークンを数倍～数十倍消費。タスクごとの予算、ループ制限、モデル階層化が必要 |
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
- [ ] 多数のエージェント運用時: エージェント・ツール・MCPサーバーのインベントリ(レジストリ)と公開承認プロセス — 実行統制はゲートウェイ・ランタイムポリシーで別途適用
- [ ] 導入戦略は[エージェント導入ガイド](../../ai/agent-adoption/)参照

## 関連ドキュメント

- [エージェント導入ガイド](../../ai/agent-adoption/) — AX戦略、ロールアウト、ガバナンス
- [AIプラットフォームとモデル比較](../../ai/ai-ml/) — モデルカタログ
- [LLMOps](../../ai/llmops/) — エージェントの可観測性、評価、コスト
- [AIセキュリティ](../../security/ai-security/) — ガードレール、プロンプトインジェクション
- [LLMチャネル選定ガイド](../../ai/1p-vs-3p/) — Seat vs API、チャネルパターン
- [現場デプロイ (Field Deployment)](../../about-cloud/field-deployment/) — 顧客環境でエージェントを本番に定着させ、ゴーライブ・Human-in-the-Loopを判断する役割

## 参考資料

- [Bedrock AgentCore](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/)
- [AWS Agent Registry](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry-get-started.html) · [Google Agent Registry](https://docs.cloud.google.com/agent-registry/overview) · [Microsoft Entra Agent Registry](https://learn.microsoft.com/entra/agent-id/identity-platform/what-is-agent-registry)
- [Microsoft Foundry Agents](https://learn.microsoft.com/azure/ai-foundry/agents/)
- [Gemini Agent Platform](https://cloud.google.com/products/agent-builder)
- [MCP](https://modelcontextprotocol.io/) · [MCP 2026-07-28 Changelog](https://modelcontextprotocol.io/specification/2026-07-28/changelog) · [A2A](https://github.com/google-a2a/A2A)
- [Kiro](https://kiro.dev/) · [Claude Code](https://github.com/anthropics/claude-code) · [Codex](https://openai.com/codex/)
- プロアクティブエージェント: [Meta Muse](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/) · [Microsoft Scout](https://www.microsoft.com/en-us/copilot/blog/2026/06/02/introducing-microsoft-scout-your-always-on-personal-agent/) · [Microsoft Copilot (Home・Code・Autopilot)](https://blogs.microsoft.com/blog/2026/09/25/introducing-the-new-copilot-with-home-code-and-autopilot/) · [Amazon Quick](https://aws.amazon.com/about-aws/whats-new/2026/09/amazon-quick-always-on-agents-sharper-feed-enterprise-controls/) · [Gemini Spark](https://blog.google/innovation-and-ai/products/gemini-app/next-evolution-gemini-app/) · [OpenAI DevDay 2026](https://openai.com/devday/2026/) · [Claude Duet](https://claude.com/resources/articles/claude-duet)
