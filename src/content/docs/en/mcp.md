---
title: "AI Agent Integration (MCP)"
description: "How to search and reference CloudPick docs from AI coding agents — MCP server connection setup and usage examples"
---

> Last reviewed: August 2026

The CloudPick documentation site provides a [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server. Connect it to your AI coding agent (Kiro, Claude Desktop, Cursor, etc.) to search and reference documentation during conversations.

## Endpoint

```
https://docs.cloudpick.kr/mcp
```

Protocol: **MCP Streamable HTTP** (POST)

This is the same origin as the docs site. `/mcp` is the MCP server.

## Client Configuration

### Kiro

`.kiro/settings/mcp.json` (workspace) or `~/.kiro/settings/mcp.json` (global):

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

## Available Tools

| Tool | Description | Parameters |
| --- | --- | --- |
| `list_docs` | Returns the full list of document titles | `lang` (optional) |
| `search_docs` | Search docs by keyword (ko·en·ja) | `query`, `limit` (default 5), `lang` (optional) |
| `get_doc` | Returns full markdown of a single document | `title` (partial match supported), `lang` (optional) |

## Multilingual Support

CloudPick docs are available in Korean (ko), English (en), and Japanese (ja), and the MCP server **auto-detects the request language** to return docs in that language.

- **One endpoint URL, language-independent** (`https://docs.cloudpick.kr/mcp`). You do not need a different URL per language.
- **Auto-detection**: `search_docs` infers the language from the query's script (Hangul → ko, Kana → ja). Otherwise it defaults to **ko**.
- **Explicit selection**: to be certain, pass the optional `lang` parameter (`ko`·`en`·`ja`) to any tool — ideally set to the user's conversation language. Latin-only queries (e.g., `EKS`, `S3`) can't be identified by script alone, so specifying `lang` is more reliable.
- **Cross-language lookup**: `get_doc` routes to the right language document whatever language the title is in.

:::note
`lang` is optional. Write in Korean and you get Korean docs; write in English or Japanese and you get those, just as before.
:::

## Usage Examples

You can ask your AI agent things like:

- "Search CloudPick docs for serverless best practices"
- "Look up the CSAP certification tier system in CloudPick"
- "Show me the full VPC and Subnets document from CloudPick"

The agent uses `search_docs` to find relevant documents, then `get_doc` to read the full content and incorporate it into its response.

## Related Documents

- [Introduction](../introduction/)
- [Glossary](../glossary/)
