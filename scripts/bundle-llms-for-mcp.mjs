/**
 * 빌드 후처리: dist/llms-full.txt를 Netlify Blob에 업로드하고
 * dist에서 llms*.txt를 삭제하여 public URL 접근을 차단합니다.
 *
 * Netlify 빌드 환경에서 실행 시 자동으로 인증됩니다.
 * 로컬에서는 NETLIFY_AUTH_TOKEN + NETLIFY_SITE_ID 환경변수가 필요합니다.
 */
import { readFileSync, unlinkSync, existsSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { getStore } from '@netlify/blobs';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const dist = join(root, 'dist');

const BLOB_STORE_NAME = 'mcp-docs';
const BLOB_KEY = 'llms-full';

async function main() {
  // 1. llms-full.txt 읽기
  const llmsFullPath = join(dist, 'llms-full.txt');
  if (!existsSync(llmsFullPath)) {
    console.error('[bundle-llms] dist/llms-full.txt not found — skipping');
    process.exit(0);
  }

  const content = readFileSync(llmsFullPath, 'utf-8');
  console.log(`[bundle-llms] Read llms-full.txt (${(content.length / 1024).toFixed(1)} KB)`);

  // 2. Netlify Blob에 업로드
  try {
    const store = getStore(BLOB_STORE_NAME);
    await store.set(BLOB_KEY, content, { metadata: { updatedAt: new Date().toISOString() } });
    console.log(`[bundle-llms] Uploaded to Netlify Blob store "${BLOB_STORE_NAME}" key "${BLOB_KEY}"`);
  } catch (err) {
    // 로컬 빌드 시 Blob 접근 불가 — 경고만 출력
    console.warn(`[bundle-llms] Blob upload skipped (not in Netlify environment): ${err.message}`);
  }

  // 3. dist에서 llms*.txt 삭제 (public 접근 차단)
  for (const file of ['llms.txt', 'llms-full.txt', 'llms-small.txt']) {
    const p = join(dist, file);
    if (existsSync(p)) {
      unlinkSync(p);
      console.log(`[bundle-llms] Removed dist/${file}`);
    }
  }
}

main().catch((err) => {
  console.error('[bundle-llms] Fatal:', err);
  process.exit(1);
});
