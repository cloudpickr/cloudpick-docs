---
title: "AI 에이전트 연동 (MCP)"
description: "CloudPick 문서를 AI 코딩 에이전트에서 검색·참조하는 방법 — MCP 서버 연결 설정과 사용 예시"
---

> 문서 기준: 2026년 8월

CloudPick 문서 사이트는 [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) 서버를 제공합니다. AI 코딩 에이전트(Kiro, Claude Desktop, Cursor 등)에 연결하면 대화 중에 문서를 검색하고 전체 내용을 참조할 수 있습니다.

## 엔드포인트

```
https://docs.cloudpick.kr/mcp
```

프로토콜: **MCP Streamable HTTP** (POST)

문서 사이트와 같은 오리진입니다. `/mcp`가 MCP 서버로 연결됩니다.

## 클라이언트별 설정

### Kiro

`.kiro/settings/mcp.json` (워크스페이스) 또는 `~/.kiro/settings/mcp.json` (글로벌):

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

## 사용 가능한 도구

| 도구 | 설명 | 파라미터 |
| --- | --- | --- |
| `list_docs` | 전체 문서 제목 목록 반환 | 없음 |
| `search_docs` | 키워드로 문서 검색 (한국어/영어) | `query`, `limit` (기본 5) |
| `get_doc` | 문서 한 편의 전체 마크다운 반환 | `title` (부분 일치 지원) |

## 사용 예시

AI 에이전트에게 다음과 같이 요청할 수 있습니다:

- "CloudPick에서 서버리스 관련 문서를 찾아줘"
- "CSAP 인증 등급 체계를 CloudPick 문서에서 확인해줘"
- "CloudPick의 VPC 서브넷 문서 전체를 보여줘"

에이전트가 `search_docs`로 관련 문서를 찾고, `get_doc`으로 전문을 읽어 답변에 활용합니다.

## 데이터 소스

MCP 서버는 이 사이트의 [`llms-full.txt`](/llms-full.txt)를 소스로 사용합니다. 사이트가 업데이트되면 5분 이내에 MCP 검색 결과에도 반영됩니다.

## 관련 문서

> 📄 [소개](../introduction/)

> 📄 [용어집](../glossary/)
