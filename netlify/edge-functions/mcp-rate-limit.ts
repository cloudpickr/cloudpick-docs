/**
 * Edge Function: MCP 엔드포인트 IP별 rate limit
 * IP당 분 60회 제한. 초과 시 429 반환.
 * Netlify Edge Functions에서 동작하며, Function invocation 전에 차단합니다.
 */

const WINDOW_MS = 60_000; // 1분
const MAX_REQUESTS = 60; // IP당 분 60회

// 인메모리 카운터 (Edge Function 인스턴스 수명 동안 유지)
const counters = new Map<string, { count: number; resetAt: number }>();

export default async function handler(request: Request) {
  const ip = request.headers.get("x-nf-client-connection-ip")
    || request.headers.get("x-forwarded-for")?.split(",")[0]?.trim()
    || "unknown";

  const now = Date.now();
  let entry = counters.get(ip);

  if (!entry || now >= entry.resetAt) {
    entry = { count: 0, resetAt: now + WINDOW_MS };
    counters.set(ip, entry);
  }

  entry.count++;

  if (entry.count > MAX_REQUESTS) {
    return new Response(
      JSON.stringify({
        jsonrpc: "2.0",
        id: null,
        error: { code: -32000, message: "Rate limit exceeded. Max 60 requests per minute." },
      }),
      {
        status: 429,
        headers: {
          "content-type": "application/json",
          "retry-after": String(Math.ceil((entry.resetAt - now) / 1000)),
          "access-control-allow-origin": "*",
        },
      }
    );
  }

  // 통과 — 원래 Function으로 계속 진행
  return;
}

export const config = {
  path: "/mcp",
};
