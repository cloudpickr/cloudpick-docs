---
title: "AIエージェント連携 (MCP)"
description: "CloudPickドキュメントをAIコーディングエージェントから検索・参照する方法 — MCPサーバー接続設定と使用例"
---

> 文書基準: 2026年8月

CloudPickドキュメントサイトは[Model Context Protocol (MCP)](https://modelcontextprotocol.io/)サーバーを提供しています。AIコーディングエージェント（Kiro、Claude Desktop、Cursorなど）に接続すると、会話中にドキュメントを検索し、全文を参照できます。

## エンドポイント

ドメイン切り替え前（現在稼働）:

```
https://cloudpick-docs-mcp.froguin.workers.dev/mcp
```

カスタムドメイン接続後:

```
https://docs.cloudpick.kr/mcp
```

プロトコル: **MCP Streamable HTTP** (POST)

## クライアント別設定

### Kiro

`.kiro/settings/mcp.json`（ワークスペース）または `~/.kiro/settings/mcp.json`（グローバル）:

```json
{
  "mcpServers": {
    "cloudpick-docs": {
      "type": "streamable-http",
      "url": "https://cloudpick-docs-mcp.froguin.workers.dev/mcp"
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
      "url": "https://cloudpick-docs-mcp.froguin.workers.dev/mcp"
    }
  }
}
```

### Cursor

Settings → MCP Servers → Add:

```json
{
  "cloudpick-docs": {
    "url": "https://cloudpick-docs-mcp.froguin.workers.dev/mcp"
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
      "url": "https://cloudpick-docs-mcp.froguin.workers.dev/mcp"
    }
  }
}
```

## 利用可能なツール

| ツール | 説明 | パラメータ |
| --- | --- | --- |
| `list_docs` | 全ドキュメントのタイトル一覧を返却 | なし |
| `search_docs` | キーワードでドキュメント検索（韓国語/英語対応） | `query`、`limit`（デフォルト5） |
| `get_doc` | ドキュメント1件の全マークダウンを返却 | `title`（部分一致対応） |

## 使用例

AIエージェントに以下のように依頼できます:

- 「CloudPickでサーバーレス関連のドキュメントを探して」
- 「CSAPの認証等級体系をCloudPickのドキュメントで確認して」
- 「CloudPickのVPCとサブネットのドキュメント全文を見せて」

エージェントが`search_docs`で関連ドキュメントを見つけ、`get_doc`で全文を読み、回答に活用します。

## データソース

MCPサーバーは本サイトの[`llms-full.txt`](/llms-full.txt)をソースとして使用しています。サイトが更新されると、5分以内にMCP検索結果にも反映されます。

## 関連ドキュメント

> 📄 [紹介](../introduction/)

> 📄 [用語集](../glossary/)
