/**
 * Scheduled Function: MCP Blob 데이터 헬스체크
 * 주 1회 실행하여 Blob에 llms-full 데이터가 존재하고 최소 크기 이상인지 확인합니다.
 */
import { getStore } from "@netlify/blobs";

const BLOB_STORE_NAME = "mcp-docs";
const BLOB_KEY = "llms-full";
const MIN_SIZE_BYTES = 100_000; // 최소 100KB 이상이어야 정상

export default async function handler() {
  const store = getStore(BLOB_STORE_NAME);

  try {
    const metadata = await store.getMetadata(BLOB_KEY);

    if (!metadata) {
      console.error(`[healthcheck] CRITICAL: Blob "${BLOB_KEY}" not found in store "${BLOB_STORE_NAME}"`);
      return new Response(JSON.stringify({ status: "error", message: "Blob not found" }), { status: 500 });
    }

    // Blob이 존재하면 실제 데이터 크기 확인
    const content = await store.get(BLOB_KEY, { type: "text" });
    if (!content || content.length < MIN_SIZE_BYTES) {
      console.error(`[healthcheck] WARNING: Blob size ${content?.length ?? 0} bytes — below minimum ${MIN_SIZE_BYTES}`);
      return new Response(JSON.stringify({ status: "warning", size: content?.length ?? 0 }), { status: 200 });
    }

    console.log(`[healthcheck] OK: Blob "${BLOB_KEY}" exists, size ${content.length} bytes, updated ${metadata.metadata?.updatedAt ?? "unknown"}`);
    return new Response(JSON.stringify({
      status: "ok",
      size: content.length,
      updatedAt: metadata.metadata?.updatedAt,
    }), { status: 200 });
  } catch (err) {
    console.error(`[healthcheck] ERROR:`, err);
    return new Response(JSON.stringify({ status: "error", message: String(err) }), { status: 500 });
  }
}

export const config = {
  schedule: "@weekly",
};
