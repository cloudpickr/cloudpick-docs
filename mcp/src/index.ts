import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { McpAgent } from "agents/mcp";
import { z } from "zod";

interface Env {
	DOCS_BASE_URL: string;
	CloudPickDocsMCP: DurableObjectNamespace;
}

type DocSection = { title: string; content: string };

const CACHE_TTL_SECONDS = 300;

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

async function loadSections(env: Env): Promise<DocSection[]> {
	const url = `${env.DOCS_BASE_URL}/llms-full.txt`;
	const cacheKey = new Request(url);
	const cache = caches.default;
	let res = await cache.match(cacheKey);
	if (!res) {
		const fetched = await fetch(url, { signal: AbortSignal.timeout(10_000) });
		if (!fetched.ok) {
			throw new Error(`문서 소스 로드 실패: ${fetched.status} ${url}`);
		}
		res = new Response(fetched.body, fetched);
		res.headers.set("Cache-Control", `public, max-age=${CACHE_TTL_SECONDS}`);
		await cache.put(cacheKey, res.clone());
	}
	return parseSections(await res.text());
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

export class CloudPickDocsMCP extends McpAgent<Env> {
	server = new McpServer({
		name: "cloudpick-docs",
		version: "1.0.0",
	});

	async init() {
		this.server.registerTool(
			"list_docs",
			{
				description:
					"CloudPick 멀티클라우드 문서의 전체 페이지 제목 목록을 반환합니다. 어떤 문서가 있는지 파악할 때 먼저 사용하세요.",
				inputSchema: {},
			},
			async () => {
				const sections = await loadSections(this.env);
				const titles = sections.map((s, i) => `${i + 1}. ${s.title}`).join("\n");
				return { content: [{ type: "text", text: titles }] };
			},
		);

		this.server.registerTool(
			"search_docs",
			{
				description:
					"CloudPick 문서를 키워드로 검색합니다. 공백으로 구분된 여러 키워드를 지원하며(한국어/영어), 관련도 순으로 상위 결과의 제목과 발췌를 반환합니다.",
				inputSchema: {
					query: z.string().describe("검색 키워드 (예: 'CSAP 등급', 'serverless cold start')"),
					limit: z.number().int().min(1).max(20).default(5).describe("최대 결과 수"),
				},
			},
			async ({ query, limit }) => {
				const sections = await loadSections(this.env);
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
					return {
						content: [{ type: "text", text: `'${query}'에 대한 검색 결과가 없습니다. list_docs로 제목 목록을 확인해 보세요.` }],
					};
				}
				const text = scored
					.map(({ s }) => `## ${s.title}\n${snippet(s.content, terms)}`)
					.join("\n\n");
				return { content: [{ type: "text", text }] };
			},
		);

		this.server.registerTool(
			"get_doc",
			{
				description:
					"문서 페이지 한 편의 전체 마크다운을 반환합니다. title에는 list_docs/search_docs가 반환한 제목(부분 일치 가능)을 전달하세요.",
				inputSchema: {
					title: z.string().describe("문서 제목 (부분 일치 지원)"),
				},
			},
			async ({ title }) => {
				const sections = await loadSections(this.env);
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
			},
		);
	}
}

export default {
	fetch(request: Request, env: Env, ctx: ExecutionContext) {
		const url = new URL(request.url);
		if (url.pathname === "/" || url.pathname === "") {
			return new Response(
				[
					"CloudPick Docs MCP Server",
					"",
					"Endpoint: POST /mcp (MCP Streamable HTTP)",
					"Tools: list_docs, search_docs(query), get_doc(title)",
					`Source: ${env.DOCS_BASE_URL}/llms-full.txt`,
				].join("\n"),
				{ headers: { "content-type": "text/plain; charset=utf-8" } },
			);
		}
		if (url.pathname.startsWith("/mcp")) {
			return CloudPickDocsMCP.serve("/mcp", { binding: "CloudPickDocsMCP" }).fetch(request, env, ctx);
		}
		return new Response("Not found", { status: 404 });
	},
};
