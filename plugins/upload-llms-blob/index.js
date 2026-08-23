import { readFileSync, writeFileSync, mkdirSync, unlinkSync, existsSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { getDeployStore } from '@netlify/blobs';

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

  // 2. Deploy-specific Blob store에 업로드
  try {
    const store = getDeployStore(BLOB_STORE_NAME);
    await store.set(BLOB_KEY, content, {
      metadata: { updatedAt: new Date().toISOString() },
    });
    console.log(`[upload-llms-blob] ✓ Uploaded to deploy store "${BLOB_STORE_NAME}" key "${BLOB_KEY}"`);
  } catch (err) {
    // 로컬 빌드 시 file-based fallback (.netlify/blobs/deploy/ 디렉토리)
    if (err.message?.includes('not been configured') || err.name === 'MissingBlobsEnvironmentError') {
      const fallbackDir = join(dirname(dirname(publishDir)), '.netlify', 'blobs', 'deploy', BLOB_STORE_NAME);
      mkdirSync(fallbackDir, { recursive: true });
      writeFileSync(join(fallbackDir, BLOB_KEY), content);
      console.log(`[upload-llms-blob] Blob env not available — wrote file-based fallback to .netlify/blobs/deploy/${BLOB_STORE_NAME}/${BLOB_KEY}`);
    } else {
      throw err;
    }
  }

  // 3. dist에서 llms*.txt 삭제 (public 접근 차단)
  for (const file of ['llms.txt', 'llms-full.txt', 'llms-small.txt']) {
    const p = join(publishDir, file);
    if (existsSync(p)) {
      unlinkSync(p);
      console.log(`[upload-llms-blob] Removed ${file} from publish dir`);
    }
  }
};
