#!/usr/bin/env node
/**
 * 로케일별 llms-full 텍스트 생성 (ko/en/ja)
 *
 * 배경:
 *   starlight-llms-txt 플러그인은 기본 로케일(ko) 하나만 `dist/llms-full.txt`로
 *   생성한다. MCP를 다국어로 제공하려면 en/ja도 같은 형식의 텍스트가 필요하다.
 *
 * 이 스크립트가 하는 일:
 *   1. ko: 플러그인이 만든 `dist/llms-full.txt`를 그대로 사용(가장 정확).
 *   2. en/ja: 소스 마크다운(src/content/docs/{en,ja})에서 동일 형식으로 생성.
 *   3. 결과를 `dist/llms/llms-full-{ko,en,ja}.txt`로 출력.
 *   4. 빌드타임 라우팅 인덱스(제목/슬러그 → lang)를 `dist/llms/routing-index.json`으로 출력.
 *
 * 출력 형식(플러그인과 호환):
 *   <SYSTEM>...</SYSTEM>
 *   # <title>
 *   > <description>
 *   <body>
 *   (페이지 구분자: 빈 줄 2개)
 *
 * MCP function은 이 텍스트를 `# ` 헤더 단위로 파싱해 검색/조회한다.
 * 정밀한 HTML→MD 변환은 불필요하며, MDX 컴포넌트/import는 제거한다.
 *
 * 실행: astro build 이후 (dist 존재 전제). package.json build 스크립트에서 호출.
 */
import { readFileSync, writeFileSync, mkdirSync, existsSync, readdirSync, statSync } from 'node:fs';
import { join, relative } from 'node:path';

const DOCS_DIR = 'src/content/docs';
const DIST_DIR = 'dist';
const OUT_DIR = join(DIST_DIR, 'llms');
const LOCALES = ['ko', 'en', 'ja'];
const PAGE_SEPARATOR = '\n\n';
const SITE_TITLE = 'CloudPick';
const SYSTEM_LINE = `<SYSTEM>This is the full developer documentation for ${SITE_TITLE}</SYSTEM>`;

/** 디렉토리 재귀 순회하며 .md/.mdx 파일 경로 수집 */
function walk(dir) {
  const out = [];
  for (const name of readdirSync(dir)) {
    const p = join(dir, name);
    const st = statSync(p);
    if (st.isDirectory()) out.push(...walk(p));
    else if (name.endsWith('.md') || name.endsWith('.mdx')) out.push(p);
  }
  return out;
}

/** frontmatter(---...---) 파싱 → { data, body } */
function parseFrontmatter(raw) {
  if (!raw.startsWith('---')) return { data: {}, body: raw };
  const end = raw.indexOf('\n---', 3);
  if (end === -1) return { data: {}, body: raw };
  const fmBlock = raw.slice(3, end).trim();
  const body = raw.slice(end + 4).replace(/^\n+/, '');
  const data = {};
  // 최상위 key: value만 파싱(중첩은 무시 — title/description만 필요)
  for (const line of fmBlock.split('\n')) {
    const m = /^([A-Za-z0-9_]+):\s*(.*)$/.exec(line);
    if (m && !line.startsWith(' ')) {
      let v = m[2].trim();
      if ((v.startsWith('"') && v.endsWith('"')) || (v.startsWith("'") && v.endsWith("'"))) {
        v = v.slice(1, -1);
      }
      data[m[1]] = v;
    }
  }
  return { data, body };
}

/** MDX 본문 정리: import문·JSX 컴포넌트 태그 제거, LinkCard는 텍스트로 치환 */
function cleanBody(body) {
  let s = body;
  // import 라인 제거
  s = s.replace(/^import\s.+$/gm, '');
  // <LinkCard title="X" description="Y" ... /> → [X] Y
  s = s.replace(/<LinkCard\b([^>]*)\/?>/g, (_, attrs) => {
    const t = /title=["']([^"']*)["']/.exec(attrs);
    const d = /description=["']([^"']*)["']/.exec(attrs);
    return (t ? t[1] : '') + (d ? ` — ${d[1]}` : '');
  });
  // <Tabs>/<TabItem>/<CardGrid> 등 여는·닫는 태그 제거(내용은 유지)
  s = s.replace(/<\/?(?:Tabs|TabItem|CardGrid|Card|Aside|Steps|LinkButton|Badge)\b[^>]*>/g, '');
  // 남은 self-closing 컴포넌트(<Foo ... />) 제거
  s = s.replace(/<[A-Z][A-Za-z0-9]*\b[^>]*\/>/g, '');
  // 3개 이상 연속 빈 줄 → 2개
  s = s.replace(/\n{3,}/g, '\n\n');
  return s.trim();
}

/** 페이지 정렬: index를 최상단으로(promote=['index*']), 그 외 경로순 */
function sortEntries(entries) {
  return entries.sort((a, b) => {
    const ai = /(^|\/)index$/.test(a.slug) ? 0 : 1;
    const bi = /(^|\/)index$/.test(b.slug) ? 0 : 1;
    if (ai !== bi) return ai - bi;
    return a.slug.localeCompare(b.slug);
  });
}

/** 한 로케일의 소스에서 llms-full 텍스트와 라우팅 엔트리 생성 */
function generateFromSource(locale) {
  const base = join(DOCS_DIR, locale);
  const files = walk(base);
  const entries = [];
  for (const file of files) {
    const raw = readFileSync(file, 'utf-8');
    const { data, body } = parseFrontmatter(raw);
    const title = data.title || '';
    if (!title) continue;
    const slug = relative(base, file).replace(/\.(md|mdx)$/, '').replace(/\/index$/, '');
    entries.push({ slug, title, description: data.description || '', body: cleanBody(body) });
  }
  sortEntries(entries);

  const segments = [SYSTEM_LINE];
  for (const e of entries) {
    const seg = [`# ${e.title}`];
    if (e.description) seg.push(`> ${e.description}`);
    if (e.body) seg.push(e.body);
    segments.push(seg.join('\n\n'));
  }
  return { text: segments.join(PAGE_SEPARATOR), entries };
}

/** dist/llms-full.txt(플러그인 ko 산출물)에서 제목 추출 → 라우팅 엔트리 */
function titlesFromPluginText(text) {
  const entries = [];
  let inFence = false;
  for (const line of text.split('\n')) {
    if (/^(```|~~~)/.test(line.trim())) inFence = !inFence;
    if (!inFence && line.startsWith('# ')) {
      entries.push({ title: line.slice(2).trim() });
    }
  }
  return entries;
}

function main() {
  mkdirSync(OUT_DIR, { recursive: true });
  // 제목(소문자) → 존재하는 언어 목록. 동음이의(영자 서비스명 등)를 모두 보존.
  const routingIndex = {};
  const addTitle = (title, lang) => {
    const key = title.toLowerCase();
    if (!routingIndex[key]) routingIndex[key] = [];
    if (!routingIndex[key].includes(lang)) routingIndex[key].push(lang);
  };

  // ── ko: 플러그인 산출물 우선, 없으면 소스에서 생성 ──
  const pluginKoPath = join(DIST_DIR, 'llms-full.txt');
  let koText;
  if (existsSync(pluginKoPath)) {
    koText = readFileSync(pluginKoPath, 'utf-8');
    for (const e of titlesFromPluginText(koText)) addTitle(e.title, 'ko');
    console.log('[build-llms-locales] ko: reused plugin dist/llms-full.txt');
  } else {
    const gen = generateFromSource('ko');
    koText = gen.text;
    for (const e of gen.entries) addTitle(e.title, 'ko');
    console.log('[build-llms-locales] ko: generated from source (plugin output not found)');
  }
  writeFileSync(join(OUT_DIR, 'llms-full-ko.txt'), koText);

  // ── en/ja: 소스에서 생성 ──
  for (const locale of ['en', 'ja']) {
    const gen = generateFromSource(locale);
    writeFileSync(join(OUT_DIR, `llms-full-${locale}.txt`), gen.text);
    for (const e of gen.entries) addTitle(e.title, locale);
    console.log(`[build-llms-locales] ${locale}: generated ${gen.entries.length} pages (${(gen.text.length / 1024).toFixed(1)} KB)`);
  }

  writeFileSync(join(OUT_DIR, 'routing-index.json'), JSON.stringify(routingIndex));
  console.log(`[build-llms-locales] ✓ wrote llms-full-{ko,en,ja}.txt + routing-index.json (${Object.keys(routingIndex).length} titles) to ${OUT_DIR}`);
}

main();
