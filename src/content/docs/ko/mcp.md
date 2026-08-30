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
| `list_docs` | 전체 문서 제목 목록 반환 | `lang` (선택) |
| `search_docs` | 키워드로 문서 검색 (ko·en·ja) | `query`, `limit` (기본 5), `lang` (선택) |
| `get_doc` | 문서 한 편의 전체 마크다운 반환 | `title` (부분 일치 지원), `lang` (선택) |

## 다국어 지원

CloudPick 문서는 한국어(ko)·영어(en)·일본어(ja) 세 언어로 제공되며, MCP 서버가 **요청 언어를 자동으로 판별**해 해당 언어 문서를 반환합니다.

- **엔드포인트 URL은 언어와 무관하게 하나입니다** (`https://docs.cloudpick.kr/mcp`). 언어별로 다른 URL을 설정할 필요가 없습니다.
- **자동 판별**: `search_docs`는 검색어의 문자를 보고 언어를 추정합니다(한글 → ko, 가나 → ja). 그 외에는 기본값 **ko**로 응답합니다.
- **명시 지정**: 원하는 언어를 확실히 하려면 모든 도구에 선택적 `lang` 파라미터(`ko`·`en`·`ja`)를 전달하세요. 대화 언어에 맞춰 지정하는 것을 권장합니다. 특히 영어 약어 위주 검색어(예: `EKS`, `S3`)는 문자만으로 언어를 알 수 없으므로 `lang`을 지정하면 정확합니다.
- **교차 언어 조회**: `get_doc`은 제목이 어느 언어든 해당 언어 문서로 라우팅합니다.

:::note
`lang`을 지정하지 않아도 동작합니다. 기존처럼 한국어로 쓰면 한국어 문서가, 영어/일본어로 쓰면 각 언어 문서가 반환됩니다.
:::

## 사용 예시

AI 에이전트에게 다음과 같이 요청할 수 있습니다:

- "CloudPick에서 서버리스 관련 문서를 찾아줘"
- "CSAP 인증 등급 체계를 CloudPick 문서에서 확인해줘"
- "CloudPick의 VPC 서브넷 문서 전체를 보여줘"

에이전트가 `search_docs`로 관련 문서를 찾고, `get_doc`으로 전문을 읽어 답변에 활용합니다.

## 관련 문서

- [소개](../introduction/)
- [용어집](../glossary/)
