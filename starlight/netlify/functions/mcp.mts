/**
 * CloudPick Docs MCP Server — Netlify Function (Stateless, JSON-RPC over HTTP)
 *
 * MCP Streamable HTTP 프로토콜의 단순 구현:
 * - POST /mcp: JSON-RPC 요청 처리
 * - GET /mcp: 서버 정보
 * - DELETE /mcp: 세션 종료 (stateless이므로 204)
 */

// ─── 문서 파싱 ───

interface DocSection {
  title: string;
  content: string;
}

const DOCS_BASE_URL = process.env.DOCS_BASE_URL || "https://docs.cloudpick.kr";
const CACHE_TTL_MS = 5 * 60 * 1000;

let cachedSections: DocSection[] | null = null;
let cacheTimestamp = 0;

function parseSections(text: string): DocSection[] {
  const sections: DocSection[] = [];
  let current: DocSection | null = null;
  let inFence = false;

  for (const line of text.split("\n")) {
    if (/^(```|~~~)/.test(line.trim())) inFence = !inFence;
    if (!inFence && line.startsWith("# ")) {
      if (current) sections.push(current);
      current = { title: line.slice(2).trim(), content: "" };
      continue;
    }
    if (current) current.content += line + "\n";
  }
  if (current) sections.push(current);

  if (sections.length > 1 && sections[0].content.trim().split("\n").length <= 3) {
    sections.shift();
  }
  return sections;
}

async function loadSections(): Promise<DocSection[]> {
  const now = Date.now();
  if (cachedSections && now - cacheTimestamp < CACHE_TTL_MS) {
    return cachedSections;
  }

  const url = `${DOCS_BASE_URL}/llms-full.txt`;
  const res = await fetch(url);
  if (!res.ok) {
    throw new Error(`문서 소스 로드 실패: ${res.status} ${url}`);
  }

  cachedSections = parseSections(await res.text());
  cacheTimestamp = now;
  return cachedSections;
}

function snippet(content: string, terms: string[], length = 240): string {
  const lower = content.toLowerCase();
  let idx = -1;
  for (const t of terms) {
    idx = lower.indexOf(t.toLowerCase());
    if (idx >= 0) break;
  }
  if (idx < 0) idx = 0;
  const start = Math.max(0, idx - 60);
  return (start > 0 ? "…" : "") + content.slice(start, start + length).trim() + "…";
}

// ─── MCP Tool 실행 ───

const TOOLS = [
  {
    name: "list_docs",
    description: "CloudPick 멀티클라우드 문서의 전체 페이지 제목 목록을 반환합니다.",
    inputSchema: { type: "object" as const, properties: {} },
  },
  {
    name: "search_docs",
    description: "CloudPick 문서를 키워드로 검색합니다. 관련도 순으로 상위 결과를 반환합니다.",
    inputSchema: {
      type: "object" as const,
      properties: {
        query: { type: "string", description: "검색 키워드" },
        limit: { type: "number", description: "최대 결과 수 (기본 5)" },
      },
      required: ["query"],
    },
  },
  {
    name: "get_doc",
    description: "문서 한 편의 전체 마크다운을 반환합니다. 부분 일치 지원.",
    inputSchema: {
      type: "object" as const,
      properties: {
        title: { type: "string", description: "문서 제목 (부분 일치 지원)" },
      },
      required: ["title"],
    },
  },
];

async function callTool(name: string, args: Record<string, unknown>): Promise<{ content: { type: string; text: string }[] }> {
  const sections = await loadSections();

  if (name === "list_docs") {
    const titles = sections.map((s, i) => `${i + 1}. ${s.title}`).join("\n");
    return { content: [{ type: "text", text: titles }] };
  }

  if (name === "search_docs") {
    const query = (args.query as string) || "";
    const limit = Math.min(Math.max((args.limit as number) || 5, 1), 20);
    const terms = query.split(/\s+/).filter(Boolean);

    const scored = sections
      .map((s) => {
        const titleLower = s.title.toLowerCase();
        const bodyLower = s.content.toLowerCase();
        let score = 0;
        for (const t of terms) {
          const tl = t.toLowerCase();
          if (titleLower.includes(tl)) score += 10;
          score += Math.min(bodyLower.split(tl).length - 1, 10);
        }
        return { s, score };
      })
      .filter((x) => x.score > 0)
      .sort((a, b) => b.score - a.score)
      .slice(0, limit);

    if (scored.length === 0) {
      return { content: [{ type: "text", text: `'${query}'에 대한 검색 결과가 없습니다.` }] };
    }
    const text = scored.map(({ s }) => `## ${s.title}\n${snippet(s.content, terms)}`).join("\n\n");
    return { content: [{ type: "text", text }] };
  }

  if (name === "get_doc") {
    const title = (args.title as string) || "";
    const tl = title.toLowerCase();
    const exact = sections.find((s) => s.title.toLowerCase() === tl);
    const partial = sections.filter((s) => s.title.toLowerCase().includes(tl));
    const hit = exact ?? (partial.length === 1 ? partial[0] : undefined);

    if (!hit) {
      const msg = partial.length > 1
        ? `'${title}'와 일치하는 문서가 ${partial.length}개입니다:\n${partial.map((s) => `- ${s.title}`).join("\n")}`
        : `'${title}' 문서를 찾지 못했습니다. list_docs로 제목을 확인하세요.`;
      return { content: [{ type: "text", text: msg }] };
    }
    return { content: [{ type: "text", text: `# ${hit.title}\n${hit.content.trim()}` }] };
  }

  return { content: [{ type: "text", text: `알 수 없는 도구: ${name}` }] };
}

// ─── JSON-RPC 처리 ───

interface JsonRpcRequest {
  jsonrpc: "2.0";
  id?: string | number;
  method: string;
  params?: Record<string, unknown>;
}

function jsonRpcResponse(id: string | number | undefined, result: unknown) {
  return { jsonrpc: "2.0", id, result };
}

function jsonRpcError(id: string | number | undefined, code: number, message: string) {
  return { jsonrpc: "2.0", id, error: { code, message } };
}

async function handleJsonRpc(request: JsonRpcRequest) {
  const { id, method, params } = request;

  switch (method) {
    case "initialize":
      return jsonRpcResponse(id, {
        protocolVersion: "2025-03-26",
        capabilities: { tools: { listChanged: false } },
        serverInfo: { name: "cloudpick-docs", version: "1.0.0" },
      });

    case "notifications/initialized":
      return null; // 알림이므로 응답 없음

    case "tools/list":
      return jsonRpcResponse(id, { tools: TOOLS });

    case "tools/call": {
      const name = (params as { name: string })?.name;
      const args = (params as { arguments?: Record<string, unknown> })?.arguments || {};
      try {
        const result = await callTool(name, args);
        return jsonRpcResponse(id, result);
      } catch (e: unknown) {
        const msg = e instanceof Error ? e.message : String(e);
        return jsonRpcError(id, -32603, msg);
      }
    }

    case "ping":
      return jsonRpcResponse(id, {});

    default:
      return jsonRpcError(id, -32601, `Method not found: ${method}`);
  }
}

// ─── Netlify Function 핸들러 ───

export default async function handler(req: Request): Promise<Response> {
  const headers = {
    "content-type": "application/json",
    "access-control-allow-origin": "*",
    "access-control-allow-methods": "GET, POST, DELETE, OPTIONS",
    "access-control-allow-headers": "content-type, mcp-session-id",
  };

  // CORS preflight
  if (req.method === "OPTIONS") {
    return new Response(null, { status: 204, headers });
  }

  // GET → 서버 정보
  if (req.method === "GET") {
    return new Response(
      JSON.stringify({
        name: "cloudpick-docs",
        version: "1.0.0",
        description: "CloudPick 문서용 MCP 서버",
        tools: TOOLS.map((t) => t.name),
        endpoint: "POST /mcp",
        source: `${DOCS_BASE_URL}/llms-full.txt`,
      }),
      { headers },
    );
  }

  // DELETE → 세션 종료 (stateless)
  if (req.method === "DELETE") {
    return new Response(null, { status: 204, headers });
  }

  // POST → JSON-RPC
  if (req.method === "POST") {
    let body: unknown;
    try {
      body = await req.json();
    } catch {
      return new Response(
        JSON.stringify(jsonRpcError(undefined, -32700, "Parse error")),
        { status: 400, headers },
      );
    }

    // 배치 요청 지원
    if (Array.isArray(body)) {
      const results = await Promise.all(
        body.map((r: JsonRpcRequest) => handleJsonRpc(r)),
      );
      const responses = results.filter((r) => r !== null);
      if (responses.length === 0) {
        return new Response(null, { status: 204, headers });
      }
      return new Response(JSON.stringify(responses), { headers });
    }

    const result = await handleJsonRpc(body as JsonRpcRequest);
    if (result === null) {
      return new Response(null, { status: 204, headers });
    }
    return new Response(JSON.stringify(result), { headers });
  }

  return new Response(JSON.stringify({ error: "Method not allowed" }), { status: 405, headers });
}

export const config = {
  path: "/mcp",
};
