'use strict';
/**
 * c_approval_gate.js 순수 로직 테스트 — node --test로 실행(외부 의존성 없음).
 * 계약 §5: C는 allowlisted human의 exact-SHA 승인, author/bot/stale/철회 방지.
 */
const { test } = require('node:test');
const assert = require('node:assert');
const { evaluateApproval, latestReviewsPerUser } = require('./c_approval_gate.cjs');

const HEAD = 'abc1234def5678abc1234def5678abc1234def56';
const OLD = '0000000000000000000000000000000000000000';

test('classification failure is not an approval', () => {
  const r = evaluateApproval({ tier: null, headSha: HEAD, prAuthor: 'writer', allowlist: ['alice'], reviews: [] });
  assert.strictEqual(r.state, 'failure');
});

test('tier A passes without human C-approval', () => {
  const r = evaluateApproval({ tier: 'A', headSha: HEAD, prAuthor: 'writer', allowlist: [], reviews: [] });
  assert.strictEqual(r.state, 'success');
});

test('tier B passes without human C-approval', () => {
  const r = evaluateApproval({ tier: 'B', headSha: HEAD, prAuthor: 'writer', allowlist: [], reviews: [] });
  assert.strictEqual(r.state, 'success');
});

test('C with empty allowlist fails (no arbitrary approver)', () => {
  const r = evaluateApproval({ tier: 'C', headSha: HEAD, prAuthor: 'writer', allowlist: [], reviews: [] });
  assert.strictEqual(r.state, 'failure');
});

test('C pending when no approval yet', () => {
  const r = evaluateApproval({ tier: 'C', headSha: HEAD, prAuthor: 'writer', allowlist: ['alice'], reviews: [] });
  assert.strictEqual(r.state, 'pending');
});

test('C approved by allowlisted human on current head', () => {
  const reviews = [{ user: 'alice', state: 'APPROVED', commitId: HEAD, isBot: false }];
  const r = evaluateApproval({ tier: 'C', headSha: HEAD, prAuthor: 'writer', allowlist: ['alice'], reviews });
  assert.strictEqual(r.state, 'success');
});

test('C approval on stale SHA is rejected', () => {
  const reviews = [{ user: 'alice', state: 'APPROVED', commitId: OLD, isBot: false }];
  const r = evaluateApproval({ tier: 'C', headSha: HEAD, prAuthor: 'writer', allowlist: ['alice'], reviews });
  assert.strictEqual(r.state, 'pending');
});

test('C self-approval by author is rejected', () => {
  const reviews = [{ user: 'writer', state: 'APPROVED', commitId: HEAD, isBot: false }];
  const r = evaluateApproval({ tier: 'C', headSha: HEAD, prAuthor: 'writer', allowlist: ['writer'], reviews });
  assert.strictEqual(r.state, 'pending');
});

test('C approval by bot is rejected', () => {
  const reviews = [{ user: 'some-bot', state: 'APPROVED', commitId: HEAD, isBot: true }];
  const r = evaluateApproval({ tier: 'C', headSha: HEAD, prAuthor: 'writer', allowlist: ['some-bot'], reviews });
  assert.strictEqual(r.state, 'pending');
});

test('C approval by non-allowlisted human is rejected', () => {
  const reviews = [{ user: 'mallory', state: 'APPROVED', commitId: HEAD, isBot: false }];
  const r = evaluateApproval({ tier: 'C', headSha: HEAD, prAuthor: 'writer', allowlist: ['alice'], reviews });
  assert.strictEqual(r.state, 'pending');
});

test('C changes_requested state is not approval', () => {
  const reviews = [{ user: 'alice', state: 'CHANGES_REQUESTED', commitId: HEAD, isBot: false }];
  const r = evaluateApproval({ tier: 'C', headSha: HEAD, prAuthor: 'writer', allowlist: ['alice'], reviews });
  assert.strictEqual(r.state, 'pending');
});

test('latestReviewsPerUser keeps last and drops dismissed', () => {
  const raw = [
    { user: { login: 'alice', type: 'User' }, state: 'CHANGES_REQUESTED', commit_id: OLD, submitted_at: '2026-09-10T00:00:00Z' },
    { user: { login: 'alice', type: 'User' }, state: 'APPROVED', commit_id: HEAD, submitted_at: '2026-09-10T01:00:00Z' },
    { user: { login: 'bob', type: 'User' }, state: 'DISMISSED', commit_id: HEAD, submitted_at: '2026-09-10T02:00:00Z' },
  ];
  const out = latestReviewsPerUser(raw);
  assert.strictEqual(out.length, 1);
  assert.strictEqual(out[0].user, 'alice');
  assert.strictEqual(out[0].state, 'APPROVED');
  assert.strictEqual(out[0].commitId, HEAD);
});

test('latestReviewsPerUser flags bot type', () => {
  const raw = [{ user: { login: 'b', type: 'Bot' }, state: 'APPROVED', commit_id: HEAD, submitted_at: '2026-09-10T00:00:00Z' }];
  assert.strictEqual(latestReviewsPerUser(raw)[0].isBot, true);
});
