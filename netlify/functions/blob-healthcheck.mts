/**
 * Scheduled Function: MCP Blob 데이터 헬스체크
 * 주 1회 실행하여 언어별 llms-full Blob이 존재하고 최소 크기 이상인지 확인합니다.
 */
import { getStore } from "@netlify/blobs";
import { LANG_BLOB_KEYS } from "../../config/locales.mjs";

const BLOB_STORE_NAME = "mcp-docs";
// 언어별 blob 키(config/locales.mjs 파생). 모든 언어가 존재·정상 크기여야 정상.
const LANG_KEYS = LANG_BLOB_KEYS;
const MIN_SIZE_BYTES = 100_000; // 최소 100KB 이상이어야 정상

export default async function handler() {
  const store = getStore(BLOB_STORE_NAME);
  const results: Record<string, { ok: boolean; size: number; updatedAt?: string; error?: string }> = {};
  let critical = false;
  let warning = false;

  for (const key of LANG_KEYS) {
    try {
      const metadata = await store.getMetadata(key);
      if (!metadata) {
        console.error(`[healthcheck] CRITICAL: Blob "${key}" not found in store "${BLOB_STORE_NAME}"`);
        results[key] = { ok: false, size: 0, error: "not found" };
        critical = true;
        continue;
      }
      const content = await store.get(key, { type: "text" });
      const size = content?.length ?? 0;
      if (!content || size < MIN_SIZE_BYTES) {
        console.error(`[healthcheck] WARNING: Blob "${key}" size ${size} bytes — below minimum ${MIN_SIZE_BYTES}`);
        results[key] = { ok: false, size };
        warning = true;
        continue;
      }
      console.log(`[healthcheck] OK: Blob "${key}" exists, size ${size} bytes, updated ${metadata.metadata?.updatedAt ?? "unknown"}`);
      results[key] = { ok: true, size, updatedAt: metadata.metadata?.updatedAt as string | undefined };
    } catch (err) {
      console.error(`[healthcheck] ERROR for "${key}":`, err);
      results[key] = { ok: false, size: 0, error: String(err) };
      critical = true;
    }
  }

  const status = critical ? "error" : warning ? "warning" : "ok";
  const httpStatus = critical ? 500 : 200;
  return new Response(JSON.stringify({ status, results }), { status: httpStatus });
}

export const config = {
  schedule: "@weekly",
};
