/**
 * CloudPick Docs MCP Server — Netlify Function (Stateless, JSON-RPC over HTTP)
 *
 * MCP Streamable HTTP 프로토콜의 단순 구현:
 * - POST /mcp: JSON-RPC 요청 처리
 * - GET /mcp: 서버 정보
 * - DELETE /mcp: 세션 종료 (stateless이므로 204)
 *
 * 문서 데이터는 Netlify Blobs에서 로드합니다 (빌드 시 업로드됨).
 */

import { getDeployStore } from "@netlify/blobs";

// ─── 문서 파싱 ───

interface DocSection {
  title: string;
  content: string;
}

const BLOB_STORE_NAME = "mcp-docs";
const BLOB_KEY = "llms-full";
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

  try {
    const store = getDeployStore(BLOB_STORE_NAME);
    const content = await store.get(BLOB_KEY, { type: "text" });
    if (!content) {
      throw new Error(`Blob "${BLOB_KEY}" not found in store "${BLOB_STORE_NAME}"`);
    }
    cachedSections = parseSections(content);
    cacheTimestamp = now;
    return cachedSections;
  } catch (err) {
    if (cachedSections) return cachedSections;
    throw err;
  }
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

async function callTool(
  name: string,
  args: Record<string, unknown>,
): Promise<{ content: { type: string; text: string }[]; isError?: boolean }> {
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

  return { content: [{ type: "text", text: `알 수 없는 도구: ${name}` }], isError: true };
}

// ─── JSON-RPC 처리 ───

interface JsonRpcRequest {
  jsonrpc: "2.0";
  id?: string | number;
  method: string;
  params?: Record<string, unknown>;
}

const SUPPORTED_PROTOCOL_VERSIONS = ["2025-03-26", "2025-06-18", "2025-11-25"];
const FALLBACK_PROTOCOL_VERSION = "2025-06-18";

function jsonRpcResponse(id: string | number | null, result: unknown) {
  return { jsonrpc: "2.0" as const, id, result };
}

function jsonRpcError(id: string | number | null, code: number, message: string) {
  return { jsonrpc: "2.0" as const, id, error: { code, message } };
}

async function handleJsonRpc(request: JsonRpcRequest) {
  const { id, method, params } = request;
  const rpcId = id === undefined ? null : id;

  switch (method) {
    case "initialize": {
      const requested = typeof params?.protocolVersion === "string" ? params.protocolVersion : "";
      const protocolVersion = SUPPORTED_PROTOCOL_VERSIONS.includes(requested)
        ? requested
        : FALLBACK_PROTOCOL_VERSION;
      return jsonRpcResponse(rpcId, {
        protocolVersion,
        capabilities: { tools: { listChanged: false } },
        serverInfo: { name: "cloudpick-docs", version: "1.0.0" },
      });
    }

    case "notifications/initialized":
      return null;

    case "tools/list":
      return jsonRpcResponse(rpcId, { tools: TOOLS });

    case "tools/call": {
      const name = (params as { name?: string })?.name;
      const args = (params as { arguments?: Record<string, unknown> })?.arguments || {};
      if (!name || !TOOLS.some((t) => t.name === name)) {
        return jsonRpcError(rpcId, -32602, `Unknown tool: ${name ?? "(missing)"}`);
      }
      try {
        const result = await callTool(name, args);
        return jsonRpcResponse(rpcId, result);
      } catch (e: unknown) {
        const msg = e instanceof Error ? e.message : String(e);
        return jsonRpcResponse(rpcId, {
          content: [{ type: "text", text: msg }],
          isError: true,
        });
      }
    }

    case "ping":
      return jsonRpcResponse(rpcId, {});

    default:
      return jsonRpcError(rpcId, -32601, `Method not found: ${method}`);
  }
}

// ─── Netlify Function 핸들러 ───

export default async function handler(req: Request): Promise<Response> {
  // CORS * : 공개 MCP. 에이전트 클라이언트가 임의의 origin에서 붙는다.
  const headers = {
    "content-type": "application/json; charset=utf-8",
    "access-control-allow-origin": "*",
    "access-control-allow-methods": "GET, POST, DELETE, OPTIONS",
    "access-control-allow-headers":
      "content-type, accept, mcp-session-id, mcp-protocol-version, last-event-id",
  };

  // CORS preflight
  if (req.method === "OPTIONS") {
    return new Response(null, { status: 204, headers });
  }

  // GET 은 Streamable HTTP SSE. 이 서버는 stateless 라 미지원 → 405.
  if (req.method === "GET") {
    return new Response(null, {
      status: 405,
      headers: { ...headers, allow: "POST, DELETE, OPTIONS" },
    });
  }

  // DELETE → 세션 종료 (stateless)
  if (req.method === "DELETE") {
    return new Response(null, { status: 202, headers });
  }

  // POST → JSON-RPC
  if (req.method === "POST") {
    let body: unknown;
    try {
      body = await req.json();
    } catch {
      return new Response(
        JSON.stringify(jsonRpcError(null, -32700, "Parse error")),
        { status: 400, headers },
      );
    }

    if (Array.isArray(body)) {
      return new Response(
        JSON.stringify(jsonRpcError(null, -32600, "Batch requests are not supported")),
        { status: 400, headers },
      );
    }

    const result = await handleJsonRpc(body as JsonRpcRequest);
    if (result === null) {
      return new Response(null, { status: 202, headers });
    }
    return new Response(JSON.stringify(result), { headers });
  }

  return new Response(JSON.stringify({ error: "Method not allowed" }), { status: 405, headers });
}

export const config = {
  path: "/mcp",
};
