/**
 * astro build 후처리: starlight-llms-txt가 dist/에 생성한 llms*.txt를
 * publish 디렉터리 밖으로 빼낸다.
 *
 * - dist/llms-full.txt → mcp-data/llms-full.txt (MCP 함수 번들용, netlify.toml included_files)
 * - 나머지 llms*.txt(llms.txt, llms-small.txt)는 삭제
 *
 * 결과: 합본 텍스트 파일은 공개 URL로 노출되지 않고, 문서 페이지(HTML)만 퍼블릭.
 */
import { copyFile, mkdir, readdir, rm } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import { join } from "node:path";

const distDir = fileURLToPath(new URL("../dist/", import.meta.url));
const dataDir = fileURLToPath(new URL("../mcp-data/", import.meta.url));

const llmsFiles = (await readdir(distDir)).filter(
	(f) => f === "llms.txt" || /^llms-.*\.txt$/.test(f),
);
if (!llmsFiles.includes("llms-full.txt")) {
	throw new Error(
		"dist/llms-full.txt가 없습니다 — starlight-llms-txt 플러그인이 빌드에서 빠졌는지 확인하세요.",
	);
}

await mkdir(dataDir, { recursive: true });
await copyFile(join(distDir, "llms-full.txt"), join(dataDir, "llms-full.txt"));
for (const f of llmsFiles) {
	await rm(join(distDir, f));
}
console.log(
	`[extract-mcp-data] mcp-data/llms-full.txt 추출, dist에서 제거: ${llmsFiles.join(", ")}`,
);
