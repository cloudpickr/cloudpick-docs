'use strict';
/**
 * c_approval_gate.cjs 순수 로직 테스트 — node --test로 실행(외부 의존성 없음).
 * 계약 §5(4d60805): C는 allowlisted human이 '현재 packet SHA-256'을 코멘트로 confirm.
 *   - GitHub PR Approve는 C 신호가 아니다.
 *   - 무관한 커밋으로 head가 바뀌어도 packet hash가 같으면 confirm 유효.
 *   - 봇/에이전트 코멘트, 잘못된/오래된 hash, allowlist 밖 사람은 무효.
 *   - feature-only PR(문서 변경 없음 + 유효 패킷 없음)은 편집 scope 밖 → 명시적 통과.
 */
const { test } = require('node:test');
const assert = require('node:assert');
const { evaluateApproval, normalizeComments } = require('./c_approval_gate.cjs');

const PACKET = 'a'.repeat(64);        // 현재 packet SHA-256
const OTHER = 'b'.repeat(64);         // 다른(오래된) packet SHA-256
const approve = (hash) => `looks good\n/approve ${hash}`;

test('classification failure is not an approval', () => {
  const r = evaluateApproval({ tier: null, packetSha256: PACKET, allowlist: ['alice'], confirmations: [] });
  assert.strictEqual(r.state, 'failure');
});

test('tier A passes without human C-approval', () => {
  const r = evaluateApproval({ tier: 'A', packetSha256: '', allowlist: [], confirmations: [] });
  assert.strictEqual(r.state, 'success');
});

test('tier B passes without human C-approval', () => {
  const r = evaluateApproval({ tier: 'B', packetSha256: PACKET, allowlist: [], confirmations: [] });
  assert.strictEqual(r.state, 'success');
});

test('feature-only PR is out of editorial C scope (explicit pass)', () => {
  const r = evaluateApproval({ tier: 'feature-only', packetSha256: '', allowlist: [], confirmations: [] });
  assert.strictEqual(r.state, 'success');
});

test('C with empty allowlist fails (no arbitrary approver)', () => {
  const r = evaluateApproval({ tier: 'C', packetSha256: PACKET, allowlist: [], confirmations: [] });
  assert.strictEqual(r.state, 'failure');
});

test('C without a validated packet hash fails', () => {
  const r = evaluateApproval({ tier: 'C', packetSha256: '', allowlist: ['alice'], confirmations: [] });
  assert.strictEqual(r.state, 'failure');
});

test('C pending when no confirmation yet', () => {
  const r = evaluateApproval({ tier: 'C', packetSha256: PACKET, allowlist: ['alice'], confirmations: [] });
  assert.strictEqual(r.state, 'pending');
});

test('C confirmed by allowlisted human for current packet hash', () => {
  const confirmations = [{ user: 'alice', body: approve(PACKET), isBot: false }];
  const r = evaluateApproval({ tier: 'C', packetSha256: PACKET, allowlist: ['alice'], confirmations });
  assert.strictEqual(r.state, 'success');
});

test('C self-confirmation by allowlisted human is valid (actor identity shared)', () => {
  // 계약: actor로 사람/에이전트 구분 불가 → 검증은 packet hash confirm 자체.
  const confirmations = [{ user: 'froguin', body: approve(PACKET), isBot: false }];
  const r = evaluateApproval({ tier: 'C', packetSha256: PACKET, allowlist: ['froguin'], confirmations });
  assert.strictEqual(r.state, 'success');
});

test('C confirmation of a stale/other packet hash is rejected', () => {
  const confirmations = [{ user: 'alice', body: approve(OTHER), isBot: false }];
  const r = evaluateApproval({ tier: 'C', packetSha256: PACKET, allowlist: ['alice'], confirmations });
  assert.strictEqual(r.state, 'pending');
});

test('C confirmation by bot/agent is rejected', () => {
  const confirmations = [{ user: 'some-bot', body: approve(PACKET), isBot: true }];
  const r = evaluateApproval({ tier: 'C', packetSha256: PACKET, allowlist: ['some-bot'], confirmations });
  assert.strictEqual(r.state, 'pending');
});

test('C confirmation by non-allowlisted human is rejected', () => {
  const confirmations = [{ user: 'mallory', body: approve(PACKET), isBot: false }];
  const r = evaluateApproval({ tier: 'C', packetSha256: PACKET, allowlist: ['alice'], confirmations });
  assert.strictEqual(r.state, 'pending');
});

test('a plain comment without /approve <hash> is not a confirmation', () => {
  const confirmations = [{ user: 'alice', body: 'lgtm 👍', isBot: false }];
  const r = evaluateApproval({ tier: 'C', packetSha256: PACKET, allowlist: ['alice'], confirmations });
  assert.strictEqual(r.state, 'pending');
});

test('bare hash mention without /approve keyword is not a confirmation', () => {
  const confirmations = [{ user: 'alice', body: `packet is ${PACKET}`, isBot: false }];
  const r = evaluateApproval({ tier: 'C', packetSha256: PACKET, allowlist: ['alice'], confirmations });
  assert.strictEqual(r.state, 'pending');
});

test('confirmation remains valid across an unrelated head change (same packet hash)', () => {
  // 무관한 커밋으로 head가 바뀌어도 packet hash가 동일하면 이전 confirm이 그대로 유효.
  const confirmations = [{ user: 'alice', body: approve(PACKET), isBot: false }];
  const r = evaluateApproval({ tier: 'C', packetSha256: PACKET, allowlist: ['alice'], confirmations });
  assert.strictEqual(r.state, 'success');
});

test('normalizeComments flags bot type and preserves body', () => {
  const raw = [
    { user: { login: 'alice', type: 'User' }, body: approve(PACKET) },
    { user: { login: 'b', type: 'Bot' }, body: approve(PACKET) },
  ];
  const out = normalizeComments(raw);
  assert.strictEqual(out.length, 2);
  assert.strictEqual(out[0].user, 'alice');
  assert.strictEqual(out[0].isBot, false);
  assert.strictEqual(out[1].isBot, true);
  assert.ok(out[0].body.includes('/approve'));
});
