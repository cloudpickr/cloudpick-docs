/**
 * Google Indexing API로 사이트맵 내 URL들을 인덱싱 요청합니다.
 * 
 * 사용법:
 *   node scripts/submit-indexing.mjs                    # 전체 사이트맵 URL 제출
 *   node scripts/submit-indexing.mjs --changed-only     # git diff로 변경된 페이지만
 *
 * 환경변수:
 *   GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json
 * 
 * 사전 조건:
 *   1. GCP 프로젝트에서 Indexing API 활성화
 *   2. 서비스 계정을 Search Console 소유자로 등록
 */
import { readFileSync, existsSync } from 'node:fs';
import { execSync } from 'node:child_process';

const SITE_URL = 'https://docs.cloudpick.kr';
const SITEMAP_URL = `${SITE_URL}/sitemap-index.xml`;
const MAX_REQUESTS_PER_DAY = 200;
const KEY_PATH = process.env.GOOGLE_APPLICATION_CREDENTIALS || '/tmp/cloudpick-indexing-key.json';

// ─── Auth ───

async function getAccessToken() {
  if (!existsSync(KEY_PATH)) {
    throw new Error(`Service account key not found: ${KEY_PATH}`);
  }
  const key = JSON.parse(readFileSync(KEY_PATH, 'utf-8'));
  
  // JWT 생성 (Google OAuth2)
  const header = Buffer.from(JSON.stringify({ alg: 'RS256', typ: 'JWT' })).toString('base64url');
  const now = Math.floor(Date.now() / 1000);
  const payload = Buffer.from(JSON.stringify({
    iss: key.client_email,
    scope: 'https://www.googleapis.com/auth/indexing',
    aud: 'https://oauth2.googleapis.com/token',
    iat: now,
    exp: now + 3600,
  })).toString('base64url');

  const crypto = await import('node:crypto');
  const sign = crypto.createSign('RSA-SHA256');
  sign.update(`${header}.${payload}`);
  const signature = sign.sign(key.private_key, 'base64url');

  const jwt = `${header}.${payload}.${signature}`;

  const res = await fetch('https://oauth2.googleapis.com/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: `grant_type=urn:ietf:params:oauth:grant-type:jwt-bearer&assertion=${jwt}`,
  });
  const data = await res.json();
  if (!data.access_token) throw new Error(`Auth failed: ${JSON.stringify(data)}`);
  return data.access_token;
}

// ─── URL 수집 ───

async function fetchSitemapUrls() {
  // sitemap-index.xml → 개별 sitemap → URL 추출
  const indexRes = await fetch(SITEMAP_URL);
  const indexXml = await indexRes.text();
  const sitemapUrls = [...indexXml.matchAll(/<loc>(.+?)<\/loc>/g)].map(m => m[1]);

  const allUrls = [];
  for (const sitemapUrl of sitemapUrls) {
    const res = await fetch(sitemapUrl);
    const xml = await res.text();
    const urls = [...xml.matchAll(/<loc>(.+?)<\/loc>/g)].map(m => m[1]);
    allUrls.push(...urls);
  }
  return allUrls;
}

function getChangedUrls() {
  try {
    const diff = execSync('git diff --name-only HEAD~1 HEAD -- src/content/docs/', { encoding: 'utf-8' });
    const files = diff.trim().split('\n').filter(Boolean);
    return files.map(f => {
      // src/content/docs/ko/ai/agents.md → https://docs.cloudpick.kr/ko/ai/agents/
      const slug = f
        .replace('src/content/docs/', '')
        .replace(/\.mdx?$/, '')
        .replace(/\/index$/, '');
      return `${SITE_URL}/${slug}/`;
    });
  } catch {
    console.log('git diff 실패 — 전체 URL로 fallback');
    return null;
  }
}

// ─── Indexing API 호출 ───

async function submitUrl(url, token, type = 'URL_UPDATED') {
  const res = await fetch('https://indexing.googleapis.com/v3/urlNotifications:publish', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
    body: JSON.stringify({ url, type }),
  });
  return { url, status: res.status, ok: res.ok };
}

// ─── Main ───

async function main() {
  const changedOnly = process.argv.includes('--changed-only');
  
  let urls;
  if (changedOnly) {
    urls = getChangedUrls();
    if (!urls) urls = await fetchSitemapUrls();
  } else {
    urls = await fetchSitemapUrls();
  }

  console.log(`[indexing] ${urls.length}개 URL 발견 (limit: ${MAX_REQUESTS_PER_DAY}/일)`);
  const batch = urls.slice(0, MAX_REQUESTS_PER_DAY);
  
  if (batch.length === 0) {
    console.log('[indexing] 제출할 URL 없음');
    return;
  }

  const token = await getAccessToken();
  console.log(`[indexing] 인증 성공. ${batch.length}개 URL 제출 시작...`);

  let success = 0, fail = 0;
  for (const url of batch) {
    const result = await submitUrl(url, token);
    if (result.ok) {
      success++;
    } else {
      fail++;
      console.log(`  ❌ ${result.url} → ${result.status}`);
    }
  }

  console.log(`[indexing] 완료: ✅ ${success}개 성공, ❌ ${fail}개 실패`);
}

main().catch(err => {
  console.error('[indexing] Error:', err.message);
  process.exit(1);
});
