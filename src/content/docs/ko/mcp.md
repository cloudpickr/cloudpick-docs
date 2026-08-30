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

:::note[구 GitBook 엔드포인트]
GitBook 시절 주소인 `https://docs.cloudpick.kr/~gitbook/mcp`도 위 엔드포인트로 그대로 연결됩니다. 기존 클라이언트 설정을 바꾸지 않아도 동작하지만, 제공되는 도구는 아래 CloudPick MCP 도구 목록을 따르며 **새로 설정할 때는 `/mcp`를 사용**하세요.
:::

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
- **기본 언어는 한국어(ko)입니다.** 한국어가 원본(SOT, source of truth)이며, 언어 신호가 없으면 항상 ko로 응답합니다.
- **자동 판별**: 검색어/제목의 문자를 보고 언어를 추정합니다(한글 → ko, 가나 → ja). 라틴 문자만 있는 검색어(예: `EKS`, `S3`)는 언어 신호가 없어 **ko로 폴백**합니다.
- **명시 지정**: 원하는 언어를 확실히 하려면 모든 도구에 선택적 `lang` 파라미터(`ko`·`en`·`ja`)를 전달하세요. **대화 언어에 맞춰 지정하는 것을 권장**합니다.
- **언어 표기 헤더**: 모든 응답은 `[lang=ko | also available: en, ja | source_lang=ko | to get another language, call again with lang="en"]` 형태의 헤더로 시작합니다. 어느 언어로 응답했는지, 다른 어떤 언어 버전이 존재하는지, 그리고 다른 언어로 받으려면 어떻게 재요청하는지를 알려주므로 에이전트가 필요 시 `lang`을 지정해 재요청할 수 있습니다.

:::note[언어 결정 규칙 — 세 도구 공통]
언어는 **① 명시 `lang` 파라미터 → ② 검색어/제목 스크립트 감지(한글→ko, 가나→ja) → ③ 기본값 ko** 순서로 결정됩니다. 세 도구(`list_docs`·`search_docs`·`get_doc`)가 모두 이 동일한 규칙을 씁니다 — 도구마다 다르게 동작하는 예외는 없습니다.

즉 **라틴 문자만으로 된 검색어·제목(예: `EKS`, `CDN`, `API Gateway`)은 언어를 알 수 없으므로 ko로 응답**합니다. 영어·일본어로 답을 받으려면 아래처럼 `lang`을 명시하세요.
:::

### 영어·일본어로 답을 받으려면

라틴 문자만 있는 검색어·제목은 한국어(기본값)로 응답되므로, **영어·일본어 응답을 받으려면 `lang` 파라미터를 명시적으로 지정**하세요. 대부분의 MCP 클라이언트는 도구 인자로 이를 전달할 수 있습니다. 에이전트에게 **사용자의 대화 언어를 `lang`으로 전달하도록 지시**하세요.

```text
search_docs({ query: "EKS", lang: "en" })     // 영어로 검색
get_doc({ title: "VPC and Subnets", lang: "en" })  // 영어 문서 조회
get_doc({ title: "VPCとサブネット", lang: "ja" })   // 일본어 문서 조회
```

한글·가나로 된 검색어는 문자로 자동 판별되므로 `lang` 없이도 각각 ko·ja로 응답합니다. 문서가 판별된 언어에 없으면 다른 언어 버전을 찾아 반환하며(교차 언어 조회), 이때 응답 헤더의 `lang=` 값으로 실제 반환 언어를 확인할 수 있습니다.

## 사용 예시

AI 에이전트에게 다음과 같이 요청할 수 있습니다:

- "CloudPick에서 서버리스 관련 문서를 찾아줘"
- "CSAP 인증 등급 체계를 CloudPick 문서에서 확인해줘"
- "CloudPick의 VPC 서브넷 문서 전체를 보여줘"

에이전트가 `search_docs`로 관련 문서를 찾고, `get_doc`으로 전문을 읽어 답변에 활용합니다.

## 관련 문서

- [소개](../introduction/)
- [용어집](../glossary/)
