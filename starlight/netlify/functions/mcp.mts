/**
 * CloudPick Docs 원격 MCP 서버 — Netlify Function (Streamable HTTP, stateless)
 *
 * 데이터 소스는 빌드 시 dist/에서 추출해 함수 번들에 포함한 mcp-data/llms-full.txt.
 * (scripts/extract-mcp-data.mjs가 이동, netlify.toml의 included_files가 번들에 포함)
 * llms*.txt는 공개 URL로 서빙되지 않는다 — 문서 페이지(HTML)만 퍼블릭.
 *
 * 도구 3종(list_docs / search_docs / get_doc)은 모두 읽기 전용·무상태이므로
 * 세션 관리 없는 stateless JSON 응답 모드로 동작한다. 필요한 프로토콜 표면이
 * initialize / tools/list / tools/call 정도로 작아 SDK 없이 직접 구현했다
 * (의존성 0 — 콜드스타트 최소화, package.json 변경 없음).
 */
import { readFile } from "node:fs/promises";
import { join } from "node:path";

type DocSection = { title: string; content: string };
type JsonRpcId = number | string | null;
type JsonRpcMessage = { jsonrpc?: string; id?: JsonRpcId; method?: string; params?: Record<string, unknown> };

const SERVER_INFO = { name: "cloudpick-docs", version: "1.0.0" };
// 최신 우선. initialize에서 클라이언트 요청 버전을 알면 echo, 모르면 최신 반환.
const SUPPORTED_PROTOCOL_VERSIONS = ["2025-06-18", "2025-03-26", "2024-11-05"];

/**
 * llms-full.txt를 페이지 단위 섹션으로 분할한다.
 * 페이지 경계는 fenced code block 밖의 H1(`# `) 라인.
 * 첫 번째 H1("CloudPick Docs")은 문서 전체 헤더이므로 프리앰블로 버린다.
 */
export function parseSections(text: string): DocSection[] {
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
	// 프리앰블(사이트 제목 섹션)은 본문이 짧으므로 첫 섹션이 실제 문서가 아니면 제거
	if (sections.length > 1 && sections[0].content.trim().split("\n").length <= 3) {
		sections.shift();
	}
	return sections;
}

async function readDataFile(): Promise<string> {
	// included_files는 사이트 base(starlight/) 기준 상대 경로를 유지한 채 번들에 들어간다.
	// 런타임 cwd 기준이 1순위, 로컬 테스트/번들 배치 차이 대비로 함수 파일 기준 경로도 시도.
	const candidates = [
		process.env.LLMS_FULL_PATH,
		join(process.cwd(), "mcp-data/llms-full.txt"),
		new URL("../../mcp-data/llms-full.txt", import.meta.url).pathname,
	].filter((p): p is string => Boolean(p));
	for (const p of candidates) {
		try {
			return await readFile(p, "utf-8");
		} catch {
			// 다음 후보 시도
		}
	}
	throw new Error(`문서 데이터(mcp-data/llms-full.txt)를 찾지 못했습니다: ${candidates.join(", ")}`);
}

// 웜 인스턴스 재사용 대비 모듈 스코프 캐시 — 배포마다 번들이 갈리므로 무효화 불필요
let sectionsPromise: Promise<DocSection[]> | null = null;
function loadSections(): Promise<DocSection[]> {
	sectionsPromise ??= readDataFile().then(parseSections);
	return sectionsPromise;
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

// ---- 도구 정의 ----------------------------------------------------------

const TOOLS = [
	{
		name: "list_docs",
		description:
			"CloudPick 멀티클라우드 문서의 전체 페이지 제목 목록을 반환합니다. 어떤 문서가 있는지 파악할 때 먼저 사용하세요.",
		inputSchema: { type: "object", properties: {} },
	},
	{
		name: "search_docs",
		description:
			"CloudPick 문서를 키워드로 검색합니다. 공백으로 구분된 여러 키워드를 지원하며(한국어/영어), 관련도 순으로 상위 결과의 제목과 발췌를 반환합니다.",
		inputSchema: {
			type: "object",
			properties: {
				query: { type: "string", description: "검색 키워드 (예: 'CSAP 등급', 'serverless cold start')" },
				limit: { type: "integer", minimum: 1, maximum: 20, default: 5, description: "최대 결과 수" },
			},
			required: ["query"],
		},
	},
	{
		name: "get_doc",
		description:
			"문서 페이지 한 편의 전체 마크다운을 반환합니다. title에는 list_docs/search_docs가 반환한 제목(부분 일치 가능)을 전달하세요.",
		inputSchema: {
			type: "object",
			properties: {
				title: { type: "string", description: "문서 제목 (부분 일치 지원)" },
			},
			required: ["title"],
		},
	},
];

type ToolResult = { content: { type: "text"; text: string }[] };

class InvalidParamsError extends Error {}

function requireString(args: Record<string, unknown>, key: string): string {
	const v = args[key];
	if (typeof v !== "string" || v.length === 0) {
		throw new InvalidParamsError(`'${key}'는 비어 있지 않은 문자열이어야 합니다.`);
	}
	return v;
}

async function callTool(name: string, args: Record<string, unknown>): Promise<ToolResult> {
	if (name === "list_docs") {
		const sections = await loadSections();
		const titles = sections.map((s, i) => `${i + 1}. ${s.title}`).join("\n");
		return { content: [{ type: "text", text: titles }] };
	}

	if (name === "search_docs") {
		const query = requireString(args, "query");
		const rawLimit = args.limit ?? 5;
		if (typeof rawLimit !== "number" || !Number.isInteger(rawLimit) || rawLimit < 1 || rawLimit > 20) {
			throw new InvalidParamsError("'limit'은 1~20 사이의 정수여야 합니다.");
		}
		const sections = await loadSections();
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
			.slice(0, rawLimit);
		if (scored.length === 0) {
			return {
				content: [{ type: "text", text: `'${query}'에 대한 검색 결과가 없습니다. list_docs로 제목 목록을 확인해 보세요.` }],
			};
		}
		const text = scored
			.map(({ s }) => `## ${s.title}\n${snippet(s.content, terms)}`)
			.join("\n\n");
		return { content: [{ type: "text", text }] };
	}

	if (name === "get_doc") {
		const title = requireString(args, "title");
		const sections = await loadSections();
		const tl = title.toLowerCase();
		const exact = sections.find((s) => s.title.toLowerCase() === tl);
		const partial = sections.filter((s) => s.title.toLowerCase().includes(tl));
		const hit = exact ?? (partial.length === 1 ? partial[0] : undefined);
		if (!hit) {
			const msg =
				partial.length > 1
					? `'${title}'와 일치하는 문서가 ${partial.length}개입니다:\n${partial.map((s) => `- ${s.title}`).join("\n")}`
					: `'${title}' 문서를 찾지 못했습니다. list_docs로 제목을 확인하세요.`;
			return { content: [{ type: "text", text: msg }] };
		}
		return { content: [{ type: "text", text: `# ${hit.title}\n${hit.content.trim()}` }] };
	}

	throw new InvalidParamsError(`알 수 없는 도구: ${name}`);
}

// ---- JSON-RPC 처리 ------------------------------------------------------

function rpcResult(id: JsonRpcId, result: unknown) {
	return { jsonrpc: "2.0", id, result };
}

function rpcError(id: JsonRpcId, code: number, message: string) {
	return { jsonrpc: "2.0", id, error: { code, message } };
}

/** 요청 1건 처리. 알림(id 없음)은 null 반환(응답 없음). */
async function handleMessage(msg: JsonRpcMessage): Promise<object | null> {
	const id = msg.id ?? null;
	const isNotification = msg.id === undefined;
	if (msg.jsonrpc !== "2.0" || typeof msg.method !== "string") {
		return isNotification ? null : rpcError(id, -32600, "유효한 JSON-RPC 2.0 요청이 아닙니다.");
	}
	if (isNotification) return null; // notifications/initialized 등 — 처리할 상태 없음

	const params = (msg.params ?? {}) as Record<string, unknown>;
	try {
		switch (msg.method) {
			case "initialize": {
				const requested = typeof params.protocolVersion === "string" ? params.protocolVersion : "";
				const protocolVersion = SUPPORTED_PROTOCOL_VERSIONS.includes(requested)
					? requested
					: SUPPORTED_PROTOCOL_VERSIONS[0];
				return rpcResult(id, {
					protocolVersion,
					capabilities: { tools: {} },
					serverInfo: SERVER_INFO,
				});
			}
			case "ping":
				return rpcResult(id, {});
			case "tools/list":
				return rpcResult(id, { tools: TOOLS });
			case "tools/call": {
				const name = typeof params.name === "string" ? params.name : "";
				const args = (params.arguments ?? {}) as Record<string, unknown>;
				try {
					return rpcResult(id, await callTool(name, args));
				} catch (e) {
					if (e instanceof InvalidParamsError) return rpcError(id, -32602, e.message);
					// 도구 실행 오류는 프로토콜 오류가 아닌 도구 결과로 전달 (MCP 규약)
					return rpcResult(id, {
						content: [{ type: "text", text: `도구 실행 오류: ${e instanceof Error ? e.message : String(e)}` }],
						isError: true,
					});
				}
			}
			default:
				return rpcError(id, -32601, `지원하지 않는 메서드: ${msg.method}`);
		}
	} catch (e) {
		return rpcError(id, -32603, e instanceof Error ? e.message : String(e));
	}
}

const JSON_HEADERS = { "content-type": "application/json; charset=utf-8" };

export default async (request: Request): Promise<Response> => {
	if (request.method === "GET") {
		return new Response(
			[
				"CloudPick Docs MCP Server",
				"",
				"Endpoint: POST /mcp (MCP Streamable HTTP, stateless)",
				"Tools: list_docs, search_docs(query), get_doc(title)",
			].join("\n"),
			{ headers: { "content-type": "text/plain; charset=utf-8" } },
		);
	}
	if (request.method !== "POST") {
		return new Response(JSON.stringify(rpcError(null, -32600, "POST만 지원합니다.")), {
			status: 405,
			headers: { ...JSON_HEADERS, allow: "GET, POST" },
		});
	}

	let body: unknown;
	try {
		body = await request.json();
	} catch {
		return new Response(JSON.stringify(rpcError(null, -32700, "JSON 파싱 실패")), {
			status: 400,
			headers: JSON_HEADERS,
		});
	}

	// 2025-03-26 스펙의 배치 요청도 수용 (이후 스펙에서는 단건만 옴)
	const messages = Array.isArray(body) ? (body as JsonRpcMessage[]) : [body as JsonRpcMessage];
	const responses = (await Promise.all(messages.map(handleMessage))).filter(
		(r): r is object => r !== null,
	);
	if (responses.length === 0) {
		return new Response(null, { status: 202 }); // 알림만 있는 요청
	}
	const payload = Array.isArray(body) ? responses : responses[0];
	return new Response(JSON.stringify(payload), { headers: JSON_HEADERS });
};

export const config = {
	path: "/mcp",
};
