'use strict';
/**
 * c_approval_gate.cjs 순수 로직 테스트 — node --test로 실행(외부 의존성 없음).
 * 계약 §5(53618d6): C는 allowlisted human이 '현재 packet SHA-256'을 코멘트로 confirm.
 *   - GitHub PR Approve는 C 신호가 아니다.
 *   - 무관한 커밋으로 head가 바뀌어도 packet hash가 같으면 confirm 유효.
 *   - 봇/에이전트 코멘트, 잘못된/오래된 hash, allowlist 밖 사람은 무효.
 *   - feature-only PR(문서 변경 없음 + 유효 패킷 없음)은 편집 scope 밖 → 명시적 통과.
 */
const { test } = require('node:test');
const assert = require('node:assert');
const { evaluateApproval, normalizeComments, approvalFingerprint } = require('./c_approval_gate.cjs');
const gate = require('./c_approval_gate.cjs');

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

test('simple approval requires an unedited allowed comment and matching recorded change', () => {
  const comment = {id: 42, user:'alice', body:'/approve', isBot:false, createdAt:'t', updatedAt:'t'};
  const input = {tier:'C',packetSha256:PACKET,allowlist:['alice'],confirmations:[comment],fingerprint:OTHER,bindings:{42:OTHER}};
  assert.strictEqual(evaluateApproval(input).state, 'success');
  assert.strictEqual(evaluateApproval({...input, fingerprint:PACKET}).state, 'pending');
  assert.strictEqual(evaluateApproval({...input, bindings:{}}).state, 'pending');
  assert.strictEqual(evaluateApproval({...input, confirmations:[{...comment,updatedAt:'later'}]}).state, 'pending');
  assert.strictEqual(evaluateApproval({...input, confirmations:[{...comment,isBot:true}]}).state, 'pending');
  assert.strictEqual(evaluateApproval({...input, confirmations:[{...comment,user:'mallory'}]}).state, 'pending');
});

test('approval fingerprint ignores only link manifest regeneration and binds document contents', () => {
  const packet = {policy_action:'link-refresh', link_refresh:{manifest_sha256:'old',url_map:{'https://old.test':'https://new.test'}}};
  const docs = [{path:'src/content/docs/ko/a.md',status:'modified',base:'old',head:'new'}];
  const first = approvalFingerprint(packet,docs);
  assert.strictEqual(first, approvalFingerprint({...packet,link_refresh:{...packet.link_refresh,manifest_sha256:'new'}},docs));
  assert.notStrictEqual(first, approvalFingerprint(packet,[{...docs[0],head:'changed'}]));
  assert.notStrictEqual(first, approvalFingerprint(packet,[{...docs[0],base:'changed'}]));
  assert.notStrictEqual(first, approvalFingerprint({...packet, link_refresh:{...packet.link_refresh,url_map:{'https://old.test':'https://other.test'}}},docs));
});

test('approval fingerprint ignores only marker manifest regeneration and binds document contents', () => {
  const packet = {policy_action:'marker-refresh', marker_refresh:{manifest_sha256:'old',from_month:{ko:'2026년 9월',en:'September 2026',ja:'2026年9月'},to_month:{ko:'2026년 10월',en:'October 2026',ja:'2026年10月'},changed_paths_count:1}};
  const docs = [{path:'src/content/docs/ko/a.md',status:'modified',base:'old',head:'new'}];
  const first = approvalFingerprint(packet,docs);
  // manifest 재계산(해시 변경)은 지문을 바꾸지 않는다(CI가 재계산하므로).
  assert.strictEqual(first, approvalFingerprint({...packet,marker_refresh:{...packet.marker_refresh,manifest_sha256:'new'}},docs));
  // 문서 blob이나 승인된 월 토큰이 바뀌면 지문이 달라져 재승인을 강제한다.
  assert.notStrictEqual(first, approvalFingerprint(packet,[{...docs[0],head:'changed'}]));
  assert.notStrictEqual(first, approvalFingerprint({...packet, marker_refresh:{...packet.marker_refresh,to_month:{ko:'2026년 11월',en:'November 2026',ja:'2026年11月'}}},docs));
});

test('command binds once, survives manifest refresh, and rejects changed documents', async () => {
  const priorEnv = process.env.C_APPROVAL_ALLOWLIST;
  process.env.C_APPROVAL_ALLOWLIST = 'alice';
  const comment = {id:123, body:'/approve', user:{login:'alice',type:'User'}, created_at:'2026-10-01T12:00:00Z', updated_at:'2026-10-01T12:00:00Z'};
  const packet = {policy_action:'link-refresh', link_refresh:{manifest_sha256:'one',url_map:{a:'b'}}};
  const state = {head:'head1', base:'base1', doc:'blob1', statuses:[]};
  const files = [{filename:'.editorial/packets/P.json',status:'added',additions:1,deletions:0}, {filename:'src/content/docs/ko/x.md',status:'modified',additions:1,deletions:1}];
  const github = {rest:{pulls:{get:async()=>({data:{head:{sha:state.head},base:{sha:state.base},updated_at:'2026-10-01T11:00:00Z'}}),listFiles:'files',listCommits:'commits'}, issues:{listComments:'comments'},repos:{getContent:async({path,ref})=>({data:path.endsWith('.json') ? {content:Buffer.from(JSON.stringify(packet)).toString('base64'),encoding:'base64'} : {sha:ref === state.base ? 'baseblob' : state.doc,type:'file'}}),listCommitStatusesForRef:'statuses',createCommitStatus:async s => state.statuses.unshift({...s,creator:{login:'github-actions[bot]'}})}},paginate:async (method)=>({files,comments:[comment],commits:[{sha:'head1'},{sha:state.head}],statuses:state.statuses}[method])};
  const context = {repo:{owner:'org',repo:'repo'},eventName:'issue_comment',payload:{action:'created',issue:{number:1,pull_request:{}},comment}};
  const exec = {exec:async (_cmd,_args,options)=>options.listeners.stdout(Buffer.from(JSON.stringify({tier:'C',report:{envelope:{packet_sha256:PACKET}}})))};
  const core = {info(){},warning(){}};
  try {
    await gate({github,context,core,exec});
    assert.equal(state.statuses[0].state,'success');
    packet.link_refresh.manifest_sha256 = 'two'; state.head = 'head2'; state.base = 'base2';
    await gate({github,context:{...context,eventName:'pull_request',payload:{pull_request:{number:1}}},core,exec});
    assert.equal(state.statuses[0].state,'success');
    state.doc = 'changed'; state.head = 'head3';
    await gate({github,context:{...context,eventName:'pull_request',payload:{pull_request:{number:1}}},core,exec});
    assert.equal(state.statuses[0].state,'pending');
    await gate({github,context,core,exec}); // rerunning an old comment cannot bind the new change
    assert.equal(state.statuses[0].state,'pending');
  } finally {
    if (priorEnv === undefined) delete process.env.C_APPROVAL_ALLOWLIST; else process.env.C_APPROVAL_ALLOWLIST = priorEnv;
  }
});
