---
title: "AIエージェント連携 (MCP)"
description: "CloudPickドキュメントをAIコーディングエージェントから検索・参照する方法 — MCPサーバー接続設定と使用例"
---

> 文書基準: 2026年8月

CloudPickドキュメントサイトは[Model Context Protocol (MCP)](https://modelcontextprotocol.io/)サーバーを提供しています。AIコーディングエージェント（Kiro、Claude Desktop、Cursorなど）に接続すると、会話中にドキュメントを検索し、全文を参照できます。

## エンドポイント

```
https://docs.cloudpick.kr/mcp
```

プロトコル: **MCP Streamable HTTP** (POST)

ドキュメントサイトと同じオリジンです。`/mcp` が MCP サーバーです。

:::note[旧 GitBook エンドポイント]
GitBook 時代のアドレス `https://docs.cloudpick.kr/~gitbook/mcp` も上記エンドポイントにそのまま接続されます。既存のクライアント設定を変更しなくても動作しますが、提供されるツールは以下の CloudPick MCP ツール一覧に従います。**新規設定では `/mcp` を使用してください。**
:::

## クライアント別設定

### Kiro

`.kiro/settings/mcp.json`（ワークスペース）または `~/.kiro/settings/mcp.json`（グローバル）:

```json
{
  "mcpServers": {
    "cloudpick-docs": {
      "type": "streamable-http",
      "url": "https://docs.cloudpick.kr/mcp"
    }
  }
}
```

### Claude Desktop

`claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "cloudpick-docs": {
      "type": "streamable-http",
      "url": "https://docs.cloudpick.kr/mcp"
    }
  }
}
```

### Cursor

Settings → MCP Servers → Add:

```json
{
  "cloudpick-docs": {
    "url": "https://docs.cloudpick.kr/mcp"
  }
}
```

### VS Code (GitHub Copilot)

`.vscode/mcp.json`:

```json
{
  "servers": {
    "cloudpick-docs": {
      "type": "http",
      "url": "https://docs.cloudpick.kr/mcp"
    }
  }
}
```

## 利用可能なツール

| ツール | 説明 | パラメータ |
| --- | --- | --- |
| `list_docs` | 全ドキュメントのタイトル一覧を返却 | `lang`（任意） |
| `search_docs` | キーワードでドキュメント検索（ko・en・ja） | `query`、`limit`（デフォルト5）、`lang`（任意） |
| `get_doc` | ドキュメント1件の全マークダウンを返却 | `title`（部分一致対応）、`lang`（任意） |

## 多言語対応

CloudPickのドキュメントは韓国語（ko）・英語（en）・日本語（ja）の3言語で提供され、MCPサーバーが**リクエスト言語を自動判別**して該当言語のドキュメントを返します。

- **エンドポイントURLは言語に関係なく1つです**（`https://docs.cloudpick.kr/mcp`）。言語ごとに別のURLを設定する必要はありません。
- **デフォルト言語は韓国語（ko）です。** 韓国語が原本（SOT、source of truth）であり、言語シグナルがない場合は常にkoで応答します。
- **自動判別**: 検索語・タイトルの文字から言語を推定します（ハングル → ko、仮名 → ja）。ラテン文字のみの検索語（例: `EKS`、`S3`）は言語シグナルがないため、**koにフォールバック**します。
- **明示指定**: 確実にしたい場合は、任意の`lang`パラメータ（`ko`・`en`・`ja`）を各ツールに渡してください。**会話の言語に合わせて指定することを推奨します。**
- **言語表示ヘッダー**: すべての応答は `[lang=ko | also available: en, ja | source_lang=ko | to get another language, call again with lang="en"]` 形式のヘッダーで始まります。どの言語で応答したか、他にどの言語版が存在するか、別の言語で受け取るにはどう再リクエストするかを示すため、エージェントは必要に応じて `lang` を指定して再リクエストできます。

:::note[言語決定ルール — 3ツール共通]
言語は **① 明示的な`lang`パラメータ → ② 検索語・タイトルの文字判別（ハングル→ko、仮名→ja） → ③ デフォルトko** の順で決定されます。3つのツール（`list_docs`・`search_docs`・`get_doc`）すべてがこの同一ルールを使い、ツールごとに異なる例外はありません。

つまり **ラテン文字のみの検索語・タイトル（例: `EKS`、`CDN`、`API Gateway`）は言語を判別できないためkoで応答**します。英語・日本語で回答を得るには、下記のように`lang`を明示してください。
:::

### 英語・日本語で回答を受け取るには

ラテン文字のみの検索語・タイトルは韓国語（デフォルト）で応答するため、**英語・日本語の応答を受け取るには`lang`パラメータを明示的に指定**してください。多くのMCPクライアントではツール引数でこれを渡せます。エージェントに**ユーザーの会話言語を`lang`として渡すよう指示**してください。

```text
search_docs({ query: "EKS", lang: "ja" })          // 日本語で検索
get_doc({ title: "VPCとサブネット", lang: "ja" })    // 日本語ドキュメントを照会
get_doc({ title: "VPC and Subnets", lang: "en" })   // 英語ドキュメントを照会
```

ハングル・仮名の検索語は文字から自動判別されるため、`lang`なしでもそれぞれko・jaで応答します。判別された言語にドキュメントが存在しない場合は、別の言語版を探して返します（クロス言語照会）。その際は応答ヘッダーの`lang=`値で実際の返却言語を確認できます。

## 使用例

AIエージェントに以下のように依頼できます:

- 「CloudPickでサーバーレス関連のドキュメントを探して」
- 「CSAPの認証等級体系をCloudPickのドキュメントで確認して」
- 「CloudPickのVPCとサブネットのドキュメント全文を見せて」

エージェントが`search_docs`で関連ドキュメントを見つけ、`get_doc`で全文を読み、回答に活用します。

## 関連ドキュメント

- [紹介](../introduction/)
- [用語集](../glossary/)
