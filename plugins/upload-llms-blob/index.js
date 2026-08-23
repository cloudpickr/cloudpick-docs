import { readFileSync, unlinkSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import { getStore } from '@netlify/blobs';

const BLOB_STORE_NAME = 'mcp-docs';
const BLOB_KEY = 'llms-full';

export const onPostBuild = async function ({ constants }) {
  const publishDir = constants.PUBLISH_DIR;

  // 1. llms-full.txt 읽기
  const llmsFullPath = join(publishDir, 'llms-full.txt');
  if (!existsSync(llmsFullPath)) {
    console.log('[upload-llms-blob] dist/llms-full.txt not found — skipping');
    return;
  }

  const content = readFileSync(llmsFullPath, 'utf-8');
  console.log(`[upload-llms-blob] Read llms-full.txt (${(content.length / 1024).toFixed(1)} KB)`);

  // 2. Netlify Blob에 업로드
  const store = getStore(BLOB_STORE_NAME);
  await store.set(BLOB_KEY, content, {
    metadata: { updatedAt: new Date().toISOString() },
  });
  console.log(`[upload-llms-blob] Uploaded to Blob store "${BLOB_STORE_NAME}" key "${BLOB_KEY}"`);

  // 3. dist에서 llms*.txt 삭제 (public 접근 차단)
  for (const file of ['llms.txt', 'llms-full.txt', 'llms-small.txt']) {
    const p = join(publishDir, file);
    if (existsSync(p)) {
      unlinkSync(p);
      console.log(`[upload-llms-blob] Removed ${file} from publish dir`);
    }
  }
};
