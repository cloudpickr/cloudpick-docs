'use strict';

// Immutable snapshots: create all parts first, then publish the pointer in the
// issue body. A failed/partial write leaves the previous snapshot authoritative.
const crypto = require('node:crypto');
const ledger = require('./monthly_ledger.cjs');
const REF = /<!-- monthly-ledger-v2:([0-9a-f]{32}):(\d+):(\d{4}-\d{2}) -->/g;
const HEADER = '<!-- monthly-ledger-summary:start -->';
const FOOTER = '<!-- monthly-ledger-summary:end -->';
const MAX_PART = 44000;
const MAX_PARTS = 1000;
const encoded = value => JSON.stringify(value, null, 2).replace(/</g, '\\u003c').replace(/`/g, '\\u0060');

function pointer(body) {
  const matches = [...body.matchAll(REF)];
  if (matches.length > 1) throw new Error('duplicate ledger pointers');
  if (!matches.length) return null;
  const [, id, n, month] = matches[0];
  const count = Number(n);
  if (!count || count > MAX_PARTS) throw new Error('invalid ledger part count');
  const published = /<!-- monthly-ledger-published:([^ ]+) -->/.exec(body)?.[1] || null;
  if (published && !Number.isFinite(Date.parse(published))) throw new Error('invalid ledger publication time');
  return {id, count, month, published};
}

function makeParts(data, id = crypto.randomBytes(16).toString('hex')) {
  ledger.validate(data);
  if (!/^[0-9a-f]{32}$/.test(id)) throw new Error('invalid snapshot ID');
  const parts = [];
  const {version, month, documents, items, resolved_ids, ...metadata} = data;
  let newsDays = [];
  if (metadata.news_progress) {
    const {days, attempted, ...newsMeta} = metadata.news_progress;
    newsDays = Object.entries(days || {}).map(([date, vendors]) => ({date, vendors, ...(attempted?.[date] ? {attempted: attempted[date]} : {})}));
    metadata.news_progress = {...newsMeta, ...(attempted !== undefined ? {had_attempt_history:true} : {})};
  }
  let sourceRefs = [];
  if (metadata.source_progress) {
    const {refs, ...sourceMeta} = metadata.source_progress;
    sourceRefs = Object.entries(refs || {}).map(([url, value]) => ({url, value}));
    metadata.source_progress = sourceMeta;
  }
  for (const field of ['documents', 'items', 'resolved_ids', 'news_days', 'source_refs', 'metadata']) {
    const rows = field === 'metadata' ? [metadata] : field === 'news_days' ? newsDays : field === 'source_refs' ? sourceRefs : (data[field] || []);
    let batch = [];
    for (const row of rows) {
      const next = [...batch, row];
      if (Buffer.byteLength(encoded({rows: next}), 'utf8') > MAX_PART) {
        if (!batch.length) throw new Error('individual ledger entry exceeds part limit');
        parts.push({field, rows: batch});
        batch = [row];
        if (Buffer.byteLength(encoded({rows: batch}), 'utf8') > MAX_PART) throw new Error('individual ledger entry exceeds part limit');
      } else batch = next;
    }
    if (batch.length) parts.push({field, rows: batch});
  }
  if (!parts.length || parts.length > MAX_PARTS) throw new Error('ledger snapshot part count exceeds limit');
  return parts.map((part, i) => ({...part, version: 2, month: data.month, id, index: i + 1, count: parts.length}));
}

function partBody(part) {
  const marker = `<!-- monthly-ledger-part:${part.id}:${part.index}:${part.count} -->`;
  // Escape < so content cannot create marker syntax or close the fenced block.
  const content = encoded(part);
  return `${marker}\n\`\`\`json\n${content}\n\`\`\`\n`;
}

function extractPart(body, ref) {
  const marker = new RegExp(`<!-- monthly-ledger-part:${ref.id}:(\\d+):(\\d+) -->`);
  const match = marker.exec(body || '');
  if (!match) return null;
  const text = (body || '').slice(match.index + match[0].length).trim();
  const fenced = /^```json\s*\n([\s\S]*?)\n```\s*$/.exec(text);
  if (!fenced) throw new Error('invalid ledger part formatting');
  const p = JSON.parse(fenced[1]);
  if (p.version !== 2 || p.id !== ref.id || p.month !== ref.month || p.count !== ref.count || p.index !== Number(match[1]) || p.count !== Number(match[2]) || !['documents','items','resolved_ids','news_days','source_refs','metadata'].includes(p.field) || !Array.isArray(p.rows)) throw new Error('ledger part metadata mismatch');
  return p;
}

function assemble(ref, comments) {
  const parts = [];
  for (const c of comments) {
    if (c.user?.login !== 'github-actions[bot]') continue;
    if (ref.published && c.created_at && c.updated_at && /<!-- monthly-ledger-part:[0-9a-f]{32}:\d+:\d+ -->/.test(c.body || '') && !(c.body || '').includes(`<!-- monthly-ledger-part:${ref.id}:`) && Date.parse(c.updated_at) > Date.parse(ref.published) && Date.parse(c.updated_at) > Date.parse(c.created_at)) throw new Error('a non-current snapshot was edited after publication; reconcile its changes before continuing');
    const part = extractPart(c.body, ref);
    if (part) parts.push(part);
  }
  if (parts.length !== ref.count || new Set(parts.map(p => p.index)).size !== ref.count || parts.some(p => p.index < 1 || p.index > ref.count)) throw new Error('ledger snapshot incomplete or duplicated');
  const data = {version: 1, month: ref.month, documents: [], items: [], resolved_ids: []};
  const metadataParts = parts.filter(p => p.field === 'metadata');
  if (metadataParts.length !== 1 || metadataParts[0].rows.length !== 1) throw new Error('invalid ledger metadata');
  const metadata = metadataParts[0].rows[0];
  if (!metadata || typeof metadata !== 'object' || Array.isArray(metadata) || Object.keys(metadata).some(k => !['coverage', 'news_progress', 'source_progress', 'backlog'].includes(k))) throw new Error('invalid metadata fields');
  Object.assign(data, metadata);
  const newsDays = [];
  const sourceRefs = [];
  for (const p of parts.sort((a,b) => a.index - b.index)) {
    if (p.field === 'news_days') newsDays.push(...p.rows);
    else if (p.field === 'source_refs') sourceRefs.push(...p.rows);
    else if (p.field !== 'metadata') data[p.field].push(...p.rows);
  }
  if (data.news_progress) {
    if (new Set(newsDays.map(d => d.date)).size !== newsDays.length) throw new Error('duplicate news progress date');
    data.news_progress.days = Object.fromEntries(newsDays.map(d => [d.date, d.vendors]));
    const attempted = Object.fromEntries(newsDays.filter(d => d.attempted).map(d => [d.date, d.attempted]));
    if (Object.keys(attempted).length || metadata.news_progress.had_attempt_history) data.news_progress.attempted = attempted;
    delete data.news_progress.had_attempt_history;
    require('./monthly_news.cjs').validate(data.news_progress);
  } else if (newsDays.length) throw new Error('news progress metadata missing');
  if (data.source_progress) {
    if (data.source_progress.version !== 1 || new Set(sourceRefs.map(r => r.url)).size !== sourceRefs.length || sourceRefs.some(r => typeof r.url !== 'string' || !r.url.startsWith('https://') || !r.value || typeof r.value !== 'object')) throw new Error('invalid source progress');
    data.source_progress.refs = Object.fromEntries(sourceRefs.map(r => [r.url, r.value]));
  } else if (sourceRefs.length) throw new Error('source progress metadata missing');
  ledger.validate(data);
  return data;
}

function renderPointer(body, data, parts, published = new Date().toISOString()) {
  ledger.validate(data);
  const counts = Object.fromEntries(['unreviewed','scanned','verified','unverified'].map(s => [s, data.documents.filter(d => d.status === s).length]));
  const active = data.items.filter(i => ['open','hold'].includes(i.status));
  const marker = `<!-- monthly-ledger-v2:${parts[0].id}:${parts.length}:${data.month} -->\n<!-- monthly-ledger-published:${published} -->`;
  const overdue = data.backlog ? `전월(${data.backlog.previous_month}) 근거 검토 미완 ${data.backlog.previous_unfinished.length}개, 목록에서 사라진 문서 ${data.backlog.previous_missing.length}개.` : '전월 원장 없음 또는 미연결: 미완 이월 범위 확인 필요.';
  const news = data.news_progress ? `벤더 소식 복구 진행: ${require('./monthly_news.cjs').pending(data.news_progress, new Date().toISOString().slice(0,10))}개 벤더·날짜 미확인. ${data.news_progress.started_on} 이전은 미확인.` : '벤더 소식 수집 범위 미확인.';
  const coverage = data.coverage ? `검사 상태: ${Object.entries(data.coverage).map(([k,v]) => `${k}=${v}`).join(', ')}.` : '검사별 실행 상태 미확인.';
  const refs = Object.values(data.source_progress?.refs || {});
  const source = data.source_progress ? `문서 참조 출처 ${refs.length}개 중 이번 달(UTC) 조회 ${refs.filter(r => typeof r.checked_at === 'string' && r.checked_at.startsWith(data.month)).length}개. 최근 상태: 관측 ${refs.filter(r => r.status === 'observed').length}개, 실패·미확인 ${refs.filter(r => r.status === 'unverified').length}개, 미조회 ${refs.filter(r => !r.status).length}개. 관측과 변경 신호는 사실 검증이 아닙니다.` : '문서별 참조 출처 감시 미실행.';
  const summary = `${HEADER}\n## 월간 검토 원장\n\n${marker}\n\n문서 ${data.documents.length}개: 미검토 ${counts.unreviewed}, 스캔 ${counts.scanned}, 근거 검토 ${counts.verified}, 미확인 ${counts.unverified}. 처리 대기 후보 ${active.length}개. 자동 스캔은 근거 검토 완료를 뜻하지 않습니다.\n\n${overdue}\n\n${news}\n\n${source}\n\n${coverage}\n\n상세 원장은 아래 봇 댓글의 JSON 조각에 있습니다. 문서별 상태·근거 및 후보 상태·PR은 해당 댓글에서 수정합니다. 이전 스냅샷은 감사 이력으로 남습니다. 구조 변경은 별도 과반 의결을 따릅니다.\n${FOOTER}`;
  const start = body.indexOf(HEADER), end = body.indexOf(FOOTER);
  if ((start < 0) !== (end < 0) || (start >= 0 && (end < start || body.indexOf(HEADER, start + HEADER.length) !== -1 || body.indexOf(FOOTER, end + FOOTER.length) !== -1))) throw new Error('invalid summary markers');
  if (start >= 0) return body.slice(0, start) + summary + body.slice(end + FOOTER.length);
  // Migrate the v1 inline block while preserving unrelated text.
  const oldStart = body.indexOf('<!-- monthly-ledger:start -->'), oldEnd = body.indexOf('<!-- monthly-ledger:end -->');
  if (oldStart >= 0 || oldEnd >= 0) {
    ledger.parse(body);
    return body.slice(0, oldStart) + summary + body.slice(oldEnd + '<!-- monthly-ledger:end -->'.length);
  }
  return `${body.trimEnd()}\n\n${summary}\n`;
}

async function load(github, context, issue) {
  const ref = pointer(issue.body || '');
  const legacy = ledger.parse(issue.body || '');
  if (ref && legacy) throw new Error('both legacy ledger and new pointer present');
  if (!ref) return legacy;
  const comments = await github.paginate(github.rest.issues.listComments, {owner: context.repo.owner, repo: context.repo.repo, issue_number: issue.number, per_page: 100});
  return assemble(ref, comments);
}

async function save(github, context, issue, data, {baseBody = issue.body || '', expected = null} = {}) {
  const parts = makeParts(data);
  const body = renderPointer(baseBody, data, parts);
  if (Buffer.byteLength(body, 'utf8') > 60000) throw new Error('non-ledger issue text too large');
  for (const part of parts) await github.rest.issues.createComment({owner: context.repo.owner, repo: context.repo.repo, issue_number: issue.number, body: partBody(part)});
  const latest = await github.rest.issues.get({owner: context.repo.owner, repo: context.repo.repo, issue_number: issue.number});
  if (latest.data.body !== issue.body) throw new Error('issue changed while saving ledger; old snapshot remains active');
  if (expected && JSON.stringify(await load(github, context, latest.data)) !== JSON.stringify(expected)) throw new Error('ledger comments changed during snapshot; old snapshot remains active');
  await github.rest.issues.update({owner: context.repo.owner, repo: context.repo.repo, issue_number: issue.number, body});
  return parts.length;
}

module.exports = {pointer, makeParts, partBody, extractPart, assemble, renderPointer, load, save};
