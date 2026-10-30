'use strict';

const crypto = require('node:crypto');
const START = '<!-- monthly-ledger:start -->';
const END = '<!-- monthly-ledger:end -->';
const STATES = new Set(['unreviewed', 'scanned', 'verified', 'unverified']);
const ITEM_STATES = new Set(['open', 'hold', 'done', 'current', 'wontfix']);

function parse(body) {
  const start = body.indexOf(START), end = body.indexOf(END);
  if (start < 0 && end < 0) return null;
  if (start < 0 || end < start || body.indexOf(START, start + START.length) !== -1 || body.indexOf(END, end + END.length) !== -1) throw new Error('invalid ledger markers');
  const value = JSON.parse(body.slice(start + START.length, end).trim());
  validate(value);
  return value;
}

function validate(ledger) {
  if (!ledger || ledger.version !== 1 || !/^\d{4}-(0[1-9]|1[0-2])$/.test(ledger.month) || !Array.isArray(ledger.documents) || !Array.isArray(ledger.items)) throw new Error('invalid ledger');
  const seen = new Set();
  for (const doc of ledger.documents) {
    if (!doc || typeof doc.path !== 'string' || !doc.path.startsWith('src/content/docs/ko/') || !STATES.has(doc.status) || seen.has(doc.path)) throw new Error('invalid document');
    seen.add(doc.path);
    if (doc.status === 'verified' && (!Array.isArray(doc.evidence) || !doc.evidence.length || doc.evidence.some(x => typeof x !== 'string' || !x.startsWith('https://')))) throw new Error('verified document requires HTTPS evidence');
  }
  const ids = new Set();
  for (const item of ledger.items) {
    if (!item || typeof item.id !== 'string' || ids.has(item.id) || !ITEM_STATES.has(item.status) || ![1,2,3,4].includes(item.axis) || typeof item.reason !== 'string' || !item.reason || !(typeof item.path === 'string' && item.path.startsWith('src/content/docs/ko/') || item.axis === 3 && item.path === null)) throw new Error('invalid item');
    ids.add(item.id);
    if (item.status === 'current' && (!Array.isArray(item.evidence) || !item.evidence.length || item.evidence.some(x => typeof x !== 'string' || !x.startsWith('https://')))) throw new Error('current item requires HTTPS evidence');
    if (item.status === 'done' && (typeof item.pr !== 'string' || !item.pr.startsWith('https://'))) throw new Error('done item requires PR URL');
  }
  if (ledger.resolved_ids !== undefined && (!Array.isArray(ledger.resolved_ids) || ledger.resolved_ids.some(id => typeof id !== 'string' || !/^[0-9a-f]{24}$/.test(id)))) throw new Error('invalid resolved IDs');
}

function fingerprint(path, axis, reason) {
  return crypto.createHash('sha256').update(JSON.stringify([path, axis, reason])).digest('hex').slice(0, 24);
}

function build(month, paths, previous, current, candidates = []) {
  if (current && current.month !== month) throw new Error('current ledger month mismatch');
  if (previous) validate(previous);
  if (current) validate(current);
  const docs = new Map((current?.documents || []).map(d => [d.path, d]));
  const items = new Map((current?.items || []).map(i => [i.id, i]));
  const resolved = new Set(current?.resolved_ids || previous?.resolved_ids || []);
  if (!current && previous) for (const item of previous.items) {
    if (item.status === 'open' || item.status === 'hold') items.set(item.id, {...item, carried_from: previous.month});
    else resolved.add(item.id); // Details stay in the previous issue; IDs suppress duplicate rediscovery.
  }
  // A new month starts unreviewed even if last month was verified; last month's
  // evidence remains reachable in the previous issue, never reasserted as current.
  const documents = [...new Set(paths)].sort().map(path => docs.get(path) || {path, status: 'unreviewed', evidence: [], pr: null});
  for (const doc of docs.values()) if (!paths.includes(doc.path)) documents.push({...doc, missing_from_inventory: true});
  for (const candidate of candidates) {
    const id = fingerprint(candidate.path, candidate.axis, candidate.reason);
    if (!items.has(id) && !resolved.has(id)) items.set(id, {id, ...candidate, status: 'open', evidence: [], pr: null});
  }
  const result = {version: 1, month, documents, items: [...items.values()], resolved_ids: [...resolved].sort()};
  validate(result);
  return result;
}

function render(body, ledger) {
  validate(ledger);
  const block = `${START}\n${JSON.stringify(ledger, null, 2).replace(/</g, '\\u003c')}\n${END}`;
  const start = body.indexOf(START), end = body.indexOf(END);
  if (start < 0 && end < 0) return `${body.trimEnd()}\n\n## 월간 검토 원장\n\n아래 JSON을 편집해 문서별 상태·공식 근거와 후보 상태·PR을 기록합니다. verified에는 HTTPS 근거가 필요합니다. 자동 스캔은 verified를 부여하지 않습니다.\n\n${block}\n`;
  parse(body); // fail closed for malformed or duplicated markers
  return body.slice(0, start) + block + body.slice(end + END.length);
}

module.exports = {parse, validate, fingerprint, build, render};
