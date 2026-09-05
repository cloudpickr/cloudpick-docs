#!/usr/bin/env node

import { readdir, readFile } from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const MAX_URLS_PER_REQUEST = 10;
const MAX_REQUESTS_PER_RUN = 20;
const OIDC_AUDIENCE = 'ncp://cloudpick-link-checker';
const ALLOWED_HOST_SUFFIXES = Object.freeze([
  'go.kr',
  'or.kr',
  'korea.kr',
  'namu.wiki',
  'naver.com',
  'ncloud.com',
  'ncloud-docs.com',
  'naverncp.com',
  'ntruss.com',
]);

export function hostnameAllowed(hostname) {
  const host = hostname.toLowerCase().replace(/\.$/, '');
  return ALLOWED_HOST_SUFFIXES.some(
    (suffix) => host === suffix || host.endsWith(`.${suffix}`),
  );
}

export function extractKoreanUrls(text) {
  const matches = text.match(/https:\/\/[^\s<>"'\])]+/g) || [];
  const urls = [];
  for (const raw of matches) {
    const value = raw.replace(/[.,;:]+$/, '');
    try {
      const url = new URL(value);
      if (hostnameAllowed(url.hostname)) urls.push(url.href);
    } catch {
      // Malformed URLs remain the responsibility of the normal link checker.
    }
  }
  return urls;
}

async function markdownFiles(directory) {
  const files = [];
  for (const entry of await readdir(directory, { withFileTypes: true })) {
    const target = path.join(directory, entry.name);
    if (entry.isDirectory()) files.push(...await markdownFiles(target));
    if (entry.isFile() && ['.md', '.mdx'].includes(path.extname(entry.name))) files.push(target);
  }
  return files;
}

export async function collectKoreanUrls(directory) {
  const urls = new Set();
  for (const file of await markdownFiles(directory)) {
    for (const url of extractKoreanUrls(await readFile(file, 'utf8'))) urls.add(url);
  }
  return [...urls].sort();
}

export function validateEndpoint(rawUrl) {
  const endpoint = new URL(rawUrl);
  if (endpoint.protocol !== 'https:') throw new Error('NCP endpoint must use HTTPS');
  if (
    endpoint.hostname !== 'apigw.ntruss.com'
    && !endpoint.hostname.endsWith('.apigw.ntruss.com')
  ) {
    throw new Error('NCP endpoint must be hosted under apigw.ntruss.com');
  }
  return endpoint;
}

export async function getGithubOidcToken(env, fetchImpl = globalThis.fetch) {
  const requestUrl = (env.ACTIONS_ID_TOKEN_REQUEST_URL || '').trim();
  const requestToken = (env.ACTIONS_ID_TOKEN_REQUEST_TOKEN || '').trim();
  if (!requestUrl || !requestToken) throw new Error('GitHub OIDC environment is unavailable');
  const endpoint = new URL(requestUrl);
  endpoint.searchParams.set('audience', OIDC_AUDIENCE);
  const response = await fetchImpl(endpoint, {
    method: 'GET',
    signal: AbortSignal.timeout(10_000),
    headers: { Authorization: `Bearer ${requestToken}` },
  });
  if (!response.ok) throw new Error(`GitHub OIDC returned HTTP ${response.status}`);
  const payload = await response.json();
  if (!payload || typeof payload.value !== 'string' || payload.value.split('.').length !== 3) {
    throw new Error('GitHub OIDC returned an invalid token');
  }
  return payload.value;
}

export async function checkChunks(
  urls,
  endpoint,
  apiKey,
  oidcToken,
  fetchImpl = globalThis.fetch,
) {
  const chunks = [];
  for (let offset = 0; offset < urls.length; offset += MAX_URLS_PER_REQUEST) {
    chunks.push(urls.slice(offset, offset + MAX_URLS_PER_REQUEST));
  }
  if (chunks.length > MAX_REQUESTS_PER_RUN) throw new Error('NCP request budget exceeded');

  const results = [];
  for (const chunk of chunks) {
    const response = await fetchImpl(endpoint, {
      method: 'POST',
      signal: AbortSignal.timeout(35_000),
      headers: {
        'Content-Type': 'application/json',
        'x-ncp-apigw-api-key': apiKey,
        Authorization: `Bearer ${oidcToken}`,
      },
      body: JSON.stringify({ urls: chunk }),
    });
    if (!response.ok) throw new Error(`NCP checker returned HTTP ${response.status}`);
    let payload = await response.json();
    if (typeof payload === 'string') payload = JSON.parse(payload);
    if (!payload || !Array.isArray(payload.results)) throw new Error('Invalid NCP response');
    results.push(...payload.results);
  }
  return results;
}

export async function run(env = process.env, fetchImpl = globalThis.fetch) {
  const endpointValue = (env.NCP_LINK_CHECKER_URL || '').trim();
  const apiKey = (env.NCP_LINK_CHECKER_API_KEY || '').trim();
  if (!endpointValue || !apiKey) {
    console.log('::notice::NCP Korean link checker is not configured; normal link checks remain active.');
    return 0;
  }

  let endpoint;
  try {
    endpoint = validateEndpoint(endpointValue);
  } catch (error) {
    console.log(`::warning::NCP checker configuration ignored: ${error.message}`);
    return 0;
  }

  const docsDirectory = env.DOCS_DIRECTORY || 'src/content/docs';
  const urls = await collectKoreanUrls(docsDirectory);
  if (urls.length === 0) {
    console.log('No allowlisted Korean links found.');
    return 0;
  }

  let results;
  try {
    const oidcToken = await getGithubOidcToken(env, fetchImpl);
    results = await checkChunks(urls, endpoint, apiKey, oidcToken, fetchImpl);
  } catch (error) {
    console.log(`::warning::NCP Korean link check was inconclusive: ${error.message}`);
    return 0;
  }

  const dead = results.filter((item) => item.classification === 'dead');
  const inconclusive = results.filter(
    (item) => !['alive', 'dead'].includes(item.classification),
  );
  console.log(`NCP Korean links: checked=${results.length} dead=${dead.length} inconclusive=${inconclusive.length}`);
  for (const item of inconclusive) {
    console.log(`::warning::Inconclusive Korean link (${item.status || 0}): ${item.url}`);
  }
  for (const item of dead) {
    console.log(`::error::Confirmed dead Korean link (${item.status}): ${item.url}`);
  }
  return dead.length > 0 ? 1 : 0;
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) {
  process.exitCode = await run();
}
