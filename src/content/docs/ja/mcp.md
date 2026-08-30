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
- **自動判別**: `search_docs`は検索語の文字から言語を推定します（ハングル → ko、仮名 → ja）。それ以外はデフォルトの **ko** で応答します。
- **明示指定**: 確実にしたい場合は、任意の`lang`パラメータ（`ko`・`en`・`ja`）を各ツールに渡してください。会話の言語に合わせて指定することを推奨します。特に英字略語中心の検索語（例: `EKS`、`S3`）は文字だけでは言語を判別できないため、`lang`を指定すると正確です。
- **クロス言語照会**: `get_doc`はタイトルがどの言語でも該当言語のドキュメントにルーティングします。

:::note
`lang`は任意です。従来どおり韓国語で書けば韓国語ドキュメントが、英語・日本語で書けば各言語のドキュメントが返されます。
:::

## 使用例

AIエージェントに以下のように依頼できます:

- 「CloudPickでサーバーレス関連のドキュメントを探して」
- 「CSAPの認証等級体系をCloudPickのドキュメントで確認して」
- 「CloudPickのVPCとサブネットのドキュメント全文を見せて」

エージェントが`search_docs`で関連ドキュメントを見つけ、`get_doc`で全文を読み、回答に活用します。

## 関連ドキュメント

- [紹介](../introduction/)
- [用語集](../glossary/)
