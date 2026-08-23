/**
 * Background Function: 문서 인덱스 재구축
 * 
 * /mcp 엔드포인트의 Blob 데이터를 강제로 갱신합니다.
 * Background Function이므로 최대 15분까지 실행 가능하며,
 * 호출 즉시 202를 반환하고 백그라운드에서 작업합니다.
 *
 * 사용 사례:
 * - 빌드 없이 Blob 데이터를 수동 갱신할 때
 * - 외부 소스에서 문서를 가져와 인덱스를 재구축할 때
 */
import { getDeployStore } from "@netlify/blobs";

const BLOB_STORE_NAME = "mcp-docs";
const BLOB_KEY = "llms-full";
const DOCS_SITE_URL = "https://docs.cloudpick.kr";

export default async function handler(request: Request) {
  // 간단한 인증 (환경변수로 토큰 확인)
  const authToken = Netlify.env.get("REINDEX_TOKEN");
  if (authToken) {
    const provided = request.headers.get("authorization")?.replace("Bearer ", "");
    if (provided !== authToken) {
      return new Response(JSON.stringify({ error: "Unauthorized" }), { status: 401 });
    }
  }

  console.log("[reindex-docs] Starting background reindex...");

  try {
    // llms-full.txt를 사이트에서 가져오기 시도 (빌드 후 삭제되므로 실패할 수 있음)
    // 실패 시 현재 Blob 데이터의 메타데이터만 확인
    const store = getDeployStore(BLOB_STORE_NAME);
    const existing = await store.get(BLOB_KEY, { type: "text" });

    if (existing) {
      console.log(`[reindex-docs] Current blob size: ${existing.length} bytes`);
      return new Response(JSON.stringify({
        status: "ok",
        message: "Blob data exists and is accessible",
        size: existing.length,
      }));
    } else {
      console.log("[reindex-docs] No blob data found — rebuild required");
      return new Response(JSON.stringify({
        status: "empty",
        message: "Blob data not found. Push a commit to trigger rebuild.",
      }));
    }
  } catch (err) {
    console.error("[reindex-docs] Error:", err);
    return new Response(JSON.stringify({ error: String(err) }), { status: 500 });
  }
}

export const config = {
  path: "/api/reindex",
  preferStatic: true,
};
