---
title: "AI Agent Integration (MCP)"
description: "How to search and reference CloudPick docs from AI coding agents — MCP server connection setup and usage examples"
---

> Last reviewed: August 2026

The CloudPick documentation site provides a [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server. Connect it to your AI coding agent (Kiro, Claude Desktop, Cursor, etc.) to search and reference documentation during conversations.

## Endpoint

Before domain cutover (currently live):

```
https://cloudpick-docs-mcp.froguin.workers.dev/mcp
```

After the custom domain is connected:

```
https://docs.cloudpick.kr/mcp
```

Protocol: **MCP Streamable HTTP** (POST)

## Client Configuration

### Kiro

`.kiro/settings/mcp.json` (workspace) or `~/.kiro/settings/mcp.json` (global):

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

## Available Tools

| Tool | Description | Parameters |
| --- | --- | --- |
| `list_docs` | Returns the full list of document titles | None |
| `search_docs` | Search docs by keyword (Korean/English) | `query`, `limit` (default 5) |
| `get_doc` | Returns full markdown of a single document | `title` (partial match supported) |

## Usage Examples

You can ask your AI agent things like:

- "Search CloudPick docs for serverless best practices"
- "Look up the CSAP certification tier system in CloudPick"
- "Show me the full VPC and Subnets document from CloudPick"

The agent uses `search_docs` to find relevant documents, then `get_doc` to read the full content and incorporate it into its response.

## Data Source

The MCP server uses this site's [`llms-full.txt`](/llms-full.txt) as its source. When the site is updated, MCP search results reflect the changes within 5 minutes.

## Related Documents

> 📄 [Introduction](../introduction/)

> 📄 [Glossary](../glossary/)
