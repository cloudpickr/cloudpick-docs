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
import { LOCALES as SHARED_LOCALES, DEFAULT_LOCALE as SHARED_DEFAULT } from "../../config/locales.mjs";

// ─── 문서 파싱 ───

interface DocSection {
  title: string;
  content: string;
}

// 응답 상단에 붙이는 언어 메타 헤더. 에이전트가 실제로 읽는 텍스트 한 줄로,
// 어떤 언어로 응답했는지(lang)와 다른 어떤 언어가 존재하는지(also)를 알린다.
// 기본(SOT)은 ko이며, 다른 언어가 필요하면 lang 파라미터로 명시 재요청하도록 가이드한다.
// 에이전트가 읽는 한 줄이므로 행동 지침을 명시적으로 포함한다.
function langHeader(lang: Lang, available?: Lang[]): string {
  const others = (available ?? SUPPORTED_LANGS).filter((l) => l !== lang);
  if (others.length === 0) {
    return `[lang=${lang} | source_lang=${DEFAULT_LANG}]`;
  }
  return (
    `[lang=${lang} | also available: ${others.join(", ")} | source_lang=${DEFAULT_LANG}` +
    ` | to get another language, call again with lang="${others[0]}"]`
  );
}

const BLOB_STORE_NAME = "mcp-docs";
const CACHE_TTL_MS = 5 * 60 * 1000;

// 지원 언어. 기본(fallback)은 ko — SOT 로케일.
// ⚠️ 이 목록은 MCP 함수 전용 상수다(서버리스 런타임 격리). 언어별 스크립트 감지 규칙
//    (detectScriptLang)·enum·메시지가 이 목록과 강하게 결합돼 있어 함께 갱신해야 한다.
//    단일 정의(config/locales.mjs)와의 드리프트는 아래 모듈 로드 시 단언으로 방지한다.
const SUPPORTED_LANGS = ["ko", "en", "ja"] as const;
type Lang = (typeof SUPPORTED_LANGS)[number];
const DEFAULT_LANG: Lang = "ko";

// ── 드리프트 방지 단언(모듈 로드 시 1회) ──
// config/locales.mjs(빌드/업로드/헬스체크의 단일 정의)에 언어가 추가/변경됐는데
// MCP의 SUPPORTED_LANGS·DEFAULT_LANG·detectScriptLang을 갱신하지 않으면 여기서 즉시 실패한다.
// (esbuild가 이 정적 import를 번들에 인라인하므로 런타임 파일/블롭 접근이 필요 없다.)
{
  const mcp = [...SUPPORTED_LANGS].sort().join(",");
  const shared = [...SHARED_LOCALES].sort().join(",");
  if (mcp !== shared) {
    throw new Error(
      `[mcp] locale drift: SUPPORTED_LANGS=[${mcp}] but config/locales.mjs=[${shared}]. ` +
        `Update SUPPORTED_LANGS + detectScriptLang() + LANG_PARAM.enum + empty-result messages together.`,
    );
  }
  if (DEFAULT_LANG !== SHARED_DEFAULT) {
    throw new Error(`[mcp] default-locale drift: DEFAULT_LANG="${DEFAULT_LANG}" but config/locales.mjs="${SHARED_DEFAULT}".`);
  }
}

// 언어별 blob 키. 신규 키가 없으면(구 배포) legacy "llms-full"(=ko)로 폴백.
function blobKeyFor(lang: Lang): string {
  return `llms-full-${lang}`;
}
const LEGACY_BLOB_KEY = "llms-full";
const ROUTING_INDEX_KEY = "routing-index";

// 언어별 파싱 결과 캐시 (stateless 함수 인스턴스 내 lazy 로딩)
const sectionCache = new Map<Lang, { sections: DocSection[]; ts: number }>();
// 제목(소문자) → 존재하는 언어 목록. 동음이의(영자 서비스명 등)를 모두 보존.
let routingIndex: Record<string, Lang[]> | null = null;
let routingIndexTs = 0;

/**
 * 텍스트의 스크립트로만 언어를 감지한다. 신호가 없으면(Latin 전용 등) null.
 * 가나(히라가나/가타카나)→ja, 한글(음절/자모)→ko.
 */
function detectScriptLang(text: string): Lang | null {
  if (!text) return null;
  if (/[\u3040-\u30ff]/.test(text)) return "ja";
  if (/[\uac00-\ud7a3\u1100-\u11ff\u3130-\u318f]/.test(text)) return "ko";
  return null;
}

/**
 * 쿼리 텍스트로 언어를 자동 판별한다.
 * 우선순위: 명시적 lang 파라미터 → 스크립트 감지(한글/가나) → ko 기본값.
 * Latin 전용·신호 없음은 ko로 폴백(하위호환: 기존 한국어 사용자 무손상).
 */
function detectLang(text: string, explicit?: unknown): Lang {
  if (typeof explicit === "string") {
    const e = explicit.toLowerCase().trim();
    if ((SUPPORTED_LANGS as readonly string[]).includes(e)) return e as Lang;
  }
  return detectScriptLang(text) ?? DEFAULT_LANG;
}

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

async function loadSections(lang: Lang): Promise<DocSection[]> {
  const now = Date.now();
  const cached = sectionCache.get(lang);
  if (cached && now - cached.ts < CACHE_TTL_MS) {
    return cached.sections;
  }

  try {
    const store = getDeployStore(BLOB_STORE_NAME);
    // 신규 언어별 키 → 없으면 legacy(ko) 키로 폴백(구 배포 호환)
    let content = await store.get(blobKeyFor(lang), { type: "text" });
    if (!content && lang === DEFAULT_LANG) {
      content = await store.get(LEGACY_BLOB_KEY, { type: "text" });
    }
    if (!content) {
      throw new Error(`Blob for lang "${lang}" not found in store "${BLOB_STORE_NAME}"`);
    }
    const sections = parseSections(content);
    sectionCache.set(lang, { sections, ts: now });
    return sections;
  } catch (err) {
    if (cached) return cached.sections;
    throw err;
  }
}

/** routing-index blob 로드(제목 소문자 → 언어 목록). 없으면 빈 맵. */
async function loadRoutingIndex(): Promise<Record<string, Lang[]>> {
  const now = Date.now();
  if (routingIndex && now - routingIndexTs < CACHE_TTL_MS) return routingIndex;
  try {
    const store = getDeployStore(BLOB_STORE_NAME);
    const raw = await store.get(ROUTING_INDEX_KEY, { type: "text" });
    routingIndex = raw ? (JSON.parse(raw) as Record<string, Lang[]>) : {};
  } catch {
    routingIndex = routingIndex || {};
  }
  routingIndexTs = now;
  return routingIndex;
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

const LANG_PARAM = {
  type: "string",
  enum: ["ko", "en", "ja"],
  description:
    "Response language (ko/en/ja). Optional — set it to the user's conversation language. If omitted, the language is auto-detected from the query script (Hangul→ko, Kana→ja); Latin-only queries (e.g. 'EKS', 'S3') carry no signal and default to ko, the source-of-truth language. Every response is prefixed with a '[lang=… | also: … | source_lang=ko]' header stating which language was returned and which others exist — pass lang explicitly (e.g. lang:'en') to get another language.",
} as const;

const TOOLS = [
  {
    name: "list_docs",
    description:
      "CloudPick 멀티클라우드 문서의 전체 페이지 제목 목록을 반환합니다. (Returns all page titles of the CloudPick multi-cloud docs.)",
    inputSchema: {
      type: "object" as const,
      properties: { lang: LANG_PARAM },
    },
  },
  {
    name: "search_docs",
    description:
      "CloudPick 문서를 키워드로 검색합니다. 관련도 순 상위 결과를 반환합니다. (Searches CloudPick docs by keyword; ko/en/ja supported, auto-detected from the query.)",
    inputSchema: {
      type: "object" as const,
      properties: {
        query: { type: "string", description: "검색 키워드 (search keyword)" },
        limit: { type: "number", description: "최대 결과 수 (기본 5) (max results, default 5)" },
        lang: LANG_PARAM,
      },
      required: ["query"],
    },
  },
  {
    name: "get_doc",
    description:
      "문서 한 편의 전체 마크다운을 반환합니다. 부분 일치 지원. 제목이 어느 언어든 해당 언어 문서로 라우팅합니다. (Returns a full document; title match routes to the right language.)",
    inputSchema: {
      type: "object" as const,
      properties: {
        title: { type: "string", description: "문서 제목 (부분 일치) (document title, partial match)" },
        lang: LANG_PARAM,
      },
      required: ["title"],
    },
  },
];

async function callTool(
  name: string,
  args: Record<string, unknown>,
): Promise<{ content: { type: string; text: string }[]; isError?: boolean }> {
  if (name === "list_docs") {
    const lang = detectLang("", args.lang);
    const sections = await loadSections(lang);
    const titles = sections.map((s, i) => `${i + 1}. ${s.title}`).join("\n");
    return { content: [{ type: "text", text: `${langHeader(lang)}\n${titles}` }] };
  }

  if (name === "search_docs") {
    const query = (args.query as string) || "";
    const lang = detectLang(query, args.lang);
    const sections = await loadSections(lang);
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
      const msg = lang === "ja"
        ? `'${query}' の検索結果がありません。`
        : lang === "en"
          ? `No results for '${query}'.`
          : `'${query}'에 대한 검색 결과가 없습니다.`;
      return { content: [{ type: "text", text: msg }] };
    }
    const text = scored.map(({ s }) => `## ${s.title}\n${snippet(s.content, terms)}`).join("\n\n");
    return { content: [{ type: "text", text: `${langHeader(lang)}\n${text}` }] };
  }

  if (name === "get_doc") {
    const title = (args.title as string) || "";
    const tl = title.toLowerCase();

    // 언어 결정은 다른 도구와 동일한 단일 규칙: 명시 lang → 제목 스크립트(한글/가나) → ko.
    // (영문 제목을 en으로 자동 라우팅하던 특례는 제거 — 문서화된 기본값과 충돌하는
    //  '숨은 두 번째 기본값'이라 예측 불가능했다. 영어가 필요하면 lang:"en"으로 명시.)
    const lang = detectLang(title, args.lang);

    let resolvedLang = lang;
    let sections = await loadSections(lang);
    let exact = sections.find((s) => s.title.toLowerCase() === tl);
    let partial = sections.filter((s) => s.title.toLowerCase().includes(tl));

    // 판별 언어에서 못 찾으면 다른 언어 blob도 탐색(교차언어 '조회' 폴백 — 언어 기본값 변경이
    // 아니라, 해당 제목이 그 언어에만 존재할 때 문서를 찾아주기 위한 것).
    if (!exact && partial.length === 0) {
      for (const alt of SUPPORTED_LANGS) {
        if (alt === lang) continue;
        const altSections = await loadSections(alt);
        const e = altSections.find((s) => s.title.toLowerCase() === tl);
        const p = altSections.filter((s) => s.title.toLowerCase().includes(tl));
        if (e || p.length > 0) {
          sections = altSections;
          resolvedLang = alt;
          exact = e;
          partial = p;
          break;
        }
      }
    }

    const hit = exact ?? (partial.length === 1 ? partial[0] : undefined);
    if (!hit) {
      const msg = partial.length > 1
        ? `'${title}'와 일치하는 문서가 ${partial.length}개입니다:\n${partial.map((s) => `- ${s.title}`).join("\n")}`
        : `'${title}' 문서를 찾지 못했습니다. list_docs로 제목을 확인하세요. (Not found — use list_docs.)`;
      return { content: [{ type: "text", text: msg }] };
    }
    // 이 제목이 실제로 존재하는 언어 목록을 routing-index에서 얻어 헤더 also:에 반영.
    // (index가 없으면 undefined → 전체 지원 언어로 표기)
    const idx = await loadRoutingIndex();
    const available = idx[hit.title.toLowerCase()] as Lang[] | undefined;
    // resolvedLang이 요청 lang과 다르면 교차언어 폴백이 일어난 것 — 헤더로 명시한다.
    return {
      content: [{ type: "text", text: `${langHeader(resolvedLang, available)}\n# ${hit.title}\n${hit.content.trim()}` }],
    };
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
        instructions:
          "CloudPick documentation MCP. Docs exist in ko (source of truth), en, and ja. " +
          "Default response language is ko; queries in Hangul→ko and Kana→ja are auto-detected. " +
          "Latin-only queries have no language signal and return ko by default. " +
          "To get English or Japanese, pass the optional `lang` parameter (e.g. lang:'en') — " +
          "set it to the user's conversation language. Every tool response starts with a " +
          "'[lang=… | also: … | source_lang=ko]' header indicating the returned language.",
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

// ─── Rate Limit (클라이언트별 분 30회) ───
// MCP session-id > IP 순으로 클라이언트를 식별.
// NAT 뒤 다수 사용자도 세션별로 구분됩니다.

const RATE_LIMIT_WINDOW_MS = 60_000;
const RATE_LIMIT_MAX = 30;
const rateLimitMap = new Map<string, { count: number; resetAt: number }>();

function getRateLimitKey(req: Request): string {
  // 1순위: MCP 세션 ID (클라이언트별 고유)
  const sessionId = req.headers.get("mcp-session-id");
  if (sessionId) return `session:${sessionId}`;
  // 2순위: IP (fallback)
  const ip = req.headers.get("x-nf-client-connection-ip")
    || req.headers.get("x-forwarded-for")?.split(",")[0]?.trim()
    || "unknown";
  return `ip:${ip}`;
}

function checkRateLimit(key: string): boolean {
  const now = Date.now();
  let entry = rateLimitMap.get(key);
  if (!entry || now >= entry.resetAt) {
    entry = { count: 0, resetAt: now + RATE_LIMIT_WINDOW_MS };
    rateLimitMap.set(key, entry);
  }
  entry.count++;
  // 오래된 항목 정리 (메모리 누수 방지)
  if (rateLimitMap.size > 10_000) {
    for (const [k, v] of rateLimitMap) {
      if (now >= v.resetAt) rateLimitMap.delete(k);
    }
  }
  return entry.count <= RATE_LIMIT_MAX;
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

  // Rate limit 체크 (세션 ID 우선, IP fallback)
  const rateLimitKey = getRateLimitKey(req);
  if (!checkRateLimit(rateLimitKey)) {
    return new Response(
      JSON.stringify(jsonRpcError(null, -32000, "Rate limit exceeded. Max 30 requests/min.")),
      { status: 429, headers: { ...headers, "retry-after": "60" } },
    );
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
