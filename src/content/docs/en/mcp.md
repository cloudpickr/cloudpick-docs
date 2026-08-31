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

:::note[Legacy GitBook endpoint]
The old GitBook address `https://docs.cloudpick.kr/~gitbook/mcp` still reaches the endpoint above. Existing client configurations keep working without changes, but the tools served are the CloudPick MCP tools listed below. Connecting through this address also adds a migration note to the `initialize` response's `instructions`, telling the connecting agent to update the URL — so it may pass that along to you. **Use `/mcp` for any new configuration.**
:::

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
- **The default language is Korean (ko).** Korean is the source of truth (SOT); when there is no language signal, the server always responds in ko.
- **Auto-detection**: the language is inferred from the query/title script (Hangul → ko, Kana → ja). Latin-only queries (e.g., `EKS`, `S3`) carry no language signal and **fall back to ko**.
- **Explicit selection**: to be certain, pass the optional `lang` parameter (`ko`·`en`·`ja`) to any tool. **Setting it to the user's conversation language is recommended.**
- **Language header**: every response starts with a `[lang=ko | also available: en, ja | source_lang=ko | to get another language, call again with lang="en"]` header. It tells you which language was returned, which other versions exist, and how to re-request another language, so the agent can call again with `lang` when needed.

:::note[Language resolution — the same for all three tools]
Language is resolved in this order: **① explicit `lang` parameter → ② script detection of the query/title (Hangul→ko, Kana→ja) → ③ default ko**. All three tools (`list_docs`·`search_docs`·`get_doc`) use this identical rule — there are no per-tool exceptions.

This means **Latin-only queries/titles (e.g., `EKS`, `CDN`, `API Gateway`) cannot be identified and respond in ko**. To get English or Japanese, specify `lang` explicitly as shown below.
:::

### Getting answers in English or Japanese

Because Latin-only queries and titles respond in Korean (the default), **specify the `lang` parameter explicitly to receive English or Japanese responses**. Most MCP clients let you pass this via the tool arguments — **instruct your agent to pass the user's conversation language as `lang`**.

```text
search_docs({ query: "EKS", lang: "en" })          // search in English
get_doc({ title: "VPC and Subnets", lang: "en" })   // fetch the English doc
get_doc({ title: "VPCとサブネット", lang: "ja" })    // fetch the Japanese doc
```

Queries in Hangul or Kana are auto-detected and respond in ko or ja respectively without `lang`. If a document does not exist in the detected language, another language version is located and returned (cross-language lookup); in that case the `lang=` value in the response header tells you the actual returned language.

## Usage Examples

You can ask your AI agent things like:

- "Search CloudPick docs for serverless best practices"
- "Look up the CSAP certification tier system in CloudPick"
- "Show me the full VPC and Subnets document from CloudPick"

The agent uses `search_docs` to find relevant documents, then `get_doc` to read the full content and incorporate it into its response.

## Related Documents

- [Introduction](../introduction/)
- [Glossary](../glossary/)
