import { readFileSync, writeFileSync, mkdirSync, unlinkSync, existsSync, readdirSync, rmdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { getDeployStore } from '@netlify/blobs';

const BLOB_STORE_NAME = 'mcp-docs';
const LOCALES = ['ko', 'en', 'ja'];

// 업로드할 항목: blobKey → dist 내 소스 파일 경로(publishDir 기준 상대)
//  - 언어별: llms-full-{lang}  ← dist/llms/llms-full-{lang}.txt
//  - 라우팅 인덱스: routing-index ← dist/llms/routing-index.json
//  - legacy: llms-full (=ko) ← 하위호환용 1릴리스 병행 유지
function buildUploadPlan(publishDir) {
  const plan = [];
  for (const lang of LOCALES) {
    plan.push({ key: `llms-full-${lang}`, path: join(publishDir, 'llms', `llms-full-${lang}.txt`) });
  }
  plan.push({ key: 'routing-index', path: join(publishDir, 'llms', 'routing-index.json') });
  // legacy: 기존 MCP/외부 리더 호환 — ko와 동일 내용
  plan.push({ key: 'llms-full', path: join(publishDir, 'llms', 'llms-full-ko.txt') });
  return plan;
}

export const onPostBuild = async function ({ constants }) {
  const publishDir = constants.PUBLISH_DIR;
  const plan = buildUploadPlan(publishDir);

  // 필수 파일 존재 확인
  const missing = plan.filter((p) => !existsSync(p.path));
  if (missing.length) {
    // en/ja 누락은 로케일 비대칭 부분 배포 위험 → 명확히 경고
    console.warn(`[upload-llms-blob] ⚠️ WARNING: ${missing.length} expected file(s) missing: ${missing.map((m) => m.key).join(', ')}. Locales may be out of sync.`);
    // ko 언어 파일조차 없으면 업로드할 게 없으므로 종료
    if (!existsSync(join(publishDir, 'llms', 'llms-full-ko.txt'))) {
      console.log('[upload-llms-blob] ko source missing — nothing to upload, skipping.');
      return;
    }
  }

  let store = null;
  let useFallback = false;
  let fallbackBase = null;
  try {
    store = getDeployStore(BLOB_STORE_NAME);
  } catch (err) {
    useFallback = true;
  }

  for (const { key, path } of plan) {
    if (!existsSync(path)) continue;
    const content = readFileSync(path, 'utf-8');
    const sizeKb = (content.length / 1024).toFixed(1);

    if (!useFallback && store) {
      try {
        await store.set(key, content, { metadata: { updatedAt: new Date().toISOString() } });
        console.log(`[upload-llms-blob] ✓ Uploaded key "${key}" (${sizeKb} KB)`);
        continue;
      } catch (err) {
        // 로컬 빌드: Blob env 미구성 → file-based fallback으로 전환
        if (err.message?.includes('not been configured') || err.name === 'MissingBlobsEnvironmentError') {
          useFallback = true;
        } else {
          throw err;
        }
      }
    }

    // file-based fallback (.netlify/blobs/deploy/<store>/<key>)
    if (useFallback) {
      if (!fallbackBase) {
        fallbackBase = join(dirname(dirname(publishDir)), '.netlify', 'blobs', 'deploy', BLOB_STORE_NAME);
        mkdirSync(fallbackBase, { recursive: true });
      }
      writeFileSync(join(fallbackBase, key), content);
      console.log(`[upload-llms-blob] (fallback) wrote key "${key}" (${sizeKb} KB) to .netlify/blobs/deploy/${BLOB_STORE_NAME}/`);
    }
  }

  // dist에서 공개하면 안 되는 llms 텍스트 정리
  //  - dist/llms/*.txt (언어별 원천) 및 인덱스는 MCP 전용 → 공개 금지
  //  - dist/llms-full.txt / llms-small.txt (플러그인 산출물)도 삭제
  //  - dist/llms.txt 는 AI 비저빌리티용으로 공개 유지
  for (const lang of LOCALES) {
    const p = join(publishDir, 'llms', `llms-full-${lang}.txt`);
    if (existsSync(p)) { unlinkSync(p); }
  }
  for (const f of ['routing-index.json']) {
    const p = join(publishDir, 'llms', f);
    if (existsSync(p)) unlinkSync(p);
  }
  for (const file of ['llms-full.txt', 'llms-small.txt']) {
    const p = join(publishDir, file);
    if (existsSync(p)) {
      unlinkSync(p);
      console.log(`[upload-llms-blob] Removed ${file} from publish dir`);
    }
  }
  // 빈 llms 디렉토리 정리(내부 텍스트/인덱스는 위에서 삭제됨)
  try {
    const llmsDir = join(publishDir, 'llms');
    if (existsSync(llmsDir) && readdirSync(llmsDir).length === 0) {
      rmdirSync(llmsDir);
    }
  } catch { /* 무시 */ }
  console.log('[upload-llms-blob] Cleaned MCP-only llms artifacts from publish dir');
};
