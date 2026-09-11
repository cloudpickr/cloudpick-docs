'use strict';
/**
 * Editorial C-Approval Gate 로직.
 * 계약: froguin/multi-agent-stack@4d60805 §Review, approval and budget enforcement (5).
 *
 * 순수 판정 함수(evaluateApproval)는 테스트 가능하게 분리하고, main(github,...)은
 * GitHub API 연동(현재 packet SHA-256 계산·코멘트 조회·commit status 기록)만 담당한다.
 *
 * 계약 §5의 정확한 C 정의(중요 — head SHA Approve 방식 폐기):
 *  "C additionally requires an allowlisted human (not a bot or agent) to confirm
 *   the current packet SHA-256, not a GitHub PR Approve bound to PAT+commit SHA.
 *   Unrelated commits (CI, feature code, merge-from-master) that leave the packet
 *   and listed docs unchanged do not reset C. GitHub self-approval on the PR
 *   author is not the C signal."
 *
 * 그래서 C 승인 신호는 다음이다:
 *  - allowlist에 속한 '사람'(봇/에이전트 아님)이
 *  - 현재 PR의 packet SHA-256(패킷 바이트의 sha256 hex)을 코멘트로 confirm.
 *    형식: 코멘트 본문에 `/approve <64-hex packet_sha256>` 포함.
 *  - 확인 hash가 현재 계산된 packet SHA-256과 정확히 일치해야 유효.
 *
 * head SHA는 병합시점 저장소 신원일 뿐이다. 무관한 커밋(CI/feature/merge-from-master)이
 * packet과 나열된 문서 바이트를 바꾸지 않으면 C를 리셋하지 않는다 → 이전 confirm이 그대로
 * 유효하다(같은 packet hash를 계속 가리키므로).
 *
 * 원칙:
 *  - GitHub PR Approve(리뷰)는 C 신호가 아니다. 오직 packet SHA-256 코멘트 confirm만.
 *  - PR 작성자 자기승인 여부는 actor로 구분 불가(에이전트/사람이 froguin 인증 공유).
 *    그래서 '누가 눌렀나'가 아니라 'allowlisted 사람이 현재 packet hash를 confirm했나'로
 *    검증한다. 봇 타입 코멘트 작성자는 제외.
 *  - Feature-only PR(문서 변경 없음 + 유효 패킷 없음)은 편집 LLM/C scope 밖 → 명시적 통과.
 *  - A/B: 이 게이트는 success로 명시 통과(자동 병합은 결정론적 5개 필수 체크가 담당).
 *  - 분류 실패/미설정/판정 불가 = 승인 아님(pending 또는 failure).
 *  - allowlist 임의 추가/자가승인 완화 금지.
 */

const CONTEXT_NAME = 'editorial-c-approval';
const SHA256_RE = /\b([0-9a-f]{64})\b/i;
const APPROVE_RE = /\/approve\s+([0-9a-f]{64})\b/i;

/**
 * 순수 판정. GitHub API 없이 입력만으로 결정한다.
 * @param {object} input
 * @param {'A'|'B'|'C'|'feature-only'|null} input.tier  분류 결과(null=분류 실패)
 * @param {string} input.packetSha256  현재 PR의 packet SHA-256(패킷 없음이면 '')
 * @param {string[]} input.allowlist   허용된 사람 login 배열(소문자)
 * @param {Array<{user:string,body:string,isBot:boolean}>} input.confirmations  이슈 코멘트
 * @returns {{state:'success'|'failure'|'pending', description:string}}
 */
function evaluateApproval(input) {
  const {
    tier,
    packetSha256,
    allowlist,
    confirmations,
  } = input;

  if (!tier) {
    return { state: 'failure', description: 'classification failed or unavailable (not an approval)' };
  }
  // Feature-only PR: src/content/docs/** 변경 없음 + 유효 패킷 없음 → 편집 C scope 밖.
  // 계약 §5: "A required conditional C-approval check may explicitly pass for
  //           independently classified A/B" + feature-only는 out of editorial scope.
  if (tier === 'feature-only') {
    return { state: 'success', description: 'feature-only PR: out of editorial LLM/C scope' };
  }
  if (tier === 'A' || tier === 'B') {
    // 독립 재분류가 A/B로 성공 → 이 게이트는 통과. 병합 자체는 필수 체크가 최종 결정.
    return { state: 'success', description: `tier ${tier}: no separate human C-approval required` };
  }
  // tier === 'C'
  if (!allowlist || allowlist.length === 0) {
    return { state: 'failure', description: 'C requires human approval but allowlist is unset (no arbitrary approver)' };
  }
  if (!packetSha256) {
    // C인데 검증된 패킷 해시가 없다 = confirm 대상 자체가 없음 → 비승인 보류.
    return { state: 'failure', description: 'C: no validated packet SHA-256 to confirm' };
  }
  const want = packetSha256.toLowerCase();
  const valid = (confirmations || []).filter((c) => {
    if (c.isBot) return false;                              // 봇/에이전트 코멘트 제외
    const login = (c.user || '').toLowerCase();
    if (!allowlist.includes(login)) return false;           // allowlist 인원만
    const m = APPROVE_RE.exec(c.body || '');
    if (!m) return false;                                   // `/approve <hash>` 형식만
    return m[1].toLowerCase() === want;                     // 현재 packet hash와 정확 일치
  });
  if (valid.length > 0) {
    return { state: 'success', description: `C confirmed by allowlisted human for packet ${want.slice(0, 12)}` };
  }
  return { state: 'pending', description: `C awaiting allowlisted human confirmation of packet ${want.slice(0, 12)}` };
}

/**
 * 이슈 코멘트를 판정용 형태로 정규화(봇 타입 표시).
 * PR review가 아니라 issue comment를 쓴다: C 신호는 packet hash confirm 코멘트다.
 */
function normalizeComments(rawComments) {
  return (rawComments || []).map((c) => ({
    user: (c.user && c.user.login) || '',
    body: c.body || '',
    isBot: !!(c.user && c.user.type === 'Bot'),
  }));
}

async function main({ github, context, core, exec }) {
  const pr = context.payload.pull_request
    || (context.payload.issue && context.payload.issue.pull_request ? context.payload.issue : null);
  if (!pr) {
    core.info('No pull request in context; skipping.');
    return;
  }
  const prNumber = context.payload.pull_request?.number || context.payload.issue?.number;

  // 이벤트마다 현재 PR head를 API로 재확인(오래된 이벤트 payload 신뢰 금지).
  // head SHA는 commit status 기록 대상일 뿐, C 승인 판정에는 packet hash를 쓴다.
  const { data: fresh } = await github.rest.pulls.get({
    owner: context.repo.owner, repo: context.repo.repo, pull_number: prNumber,
  });
  const headSha = fresh.head.sha;

  // 분류 + 현재 packet SHA-256 계산: 신뢰된 base 코드로 실행.
  let tier = null;
  let packetSha256 = '';
  try {
    const computed = await computeTierAndPacketSha({ github, context, exec, prNumber, headSha, core });
    tier = computed.tier;
    packetSha256 = computed.packetSha256;
  } catch (e) {
    core.warning(`classification error: ${e.message}`);
    tier = null; // 실패는 승인 아님
  }

  // 이슈 코멘트 조회(pagination) → packet hash confirm 신호 탐색.
  const rawComments = await github.paginate(github.rest.issues.listComments, {
    owner: context.repo.owner, repo: context.repo.repo, issue_number: prNumber, per_page: 100,
  });
  const confirmations = normalizeComments(rawComments);

  const allowlist = (process.env.C_APPROVAL_ALLOWLIST || '')
    .split(',').map((s) => s.trim().toLowerCase()).filter(Boolean);

  const result = evaluateApproval({ tier, packetSha256, allowlist, confirmations });

  // 현재 head SHA에 commit status 기록(위조 방지: GITHUB_TOKEN으로만 기록).
  await github.rest.repos.createCommitStatus({
    owner: context.repo.owner, repo: context.repo.repo,
    sha: headSha, state: result.state, context: CONTEXT_NAME,
    description: result.description.slice(0, 140),
  });
  core.info(`[${CONTEXT_NAME}] tier=${tier} packet=${packetSha256.slice(0, 12)} state=${result.state} — ${result.description}`);
}

/** diff를 받아 tier + 현재 packet SHA-256 계산.
 *  run_review_gate.py(패킷 검증·filename 확인·scope 예외 통일)에 위임한다.
 *  - 문서 변경 없음 + 유효 패킷 없음 → 'feature-only'(편집 scope 밖).
 *  - packet SHA-256은 run_review_gate.py의 envelope.packet_sha256 출력에서 읽는다.
 *    (env packet_sha256이 '0'*64이면 유효 패킷 없음으로 취급 → 빈 문자열.) */
async function computeTierAndPacketSha({ github, context, exec, prNumber, headSha, core }) {
  const files = await github.paginate(github.rest.pulls.listFiles, {
    owner: context.repo.owner, repo: context.repo.repo, pull_number: prNumber, per_page: 100,
  });
  const numstat = files.map((f) => `${f.additions}\t${f.deletions}\t${f.filename}`).join('\n');
  const smap = { added: 'A', removed: 'D', modified: 'M', renamed: 'R', changed: 'M' };
  const nameStatus = files.map((f) => f.status === 'renamed'
    ? `R100\t${f.previous_filename}\t${f.filename}`
    : `${smap[f.status] || 'M'}\t${f.filename}`).join('\n');

  const fs = require('fs');
  fs.writeFileSync('/tmp/ca_numstat.txt', numstat + '\n');
  fs.writeFileSync('/tmp/ca_name_status.txt', nameStatus + '\n');

  // 단일 패킷 파일이면 head SHA 콘텐츠를 데이터로 취득하고 실제 경로를 검증기에 전달.
  const packets = files.filter((f) => /^\.editorial\/packets\/[^/]+\.json$/.test(f.filename));
  let packetArg = 'none';
  let packetRepoPath = '';
  if (packets.length === 1) {
    const { data: blob } = await github.rest.repos.getContent({
      owner: context.repo.owner, repo: context.repo.repo, path: packets[0].filename, ref: headSha,
    });
    fs.writeFileSync('/tmp/ca_packet.json', Buffer.from(blob.content, blob.encoding).toString('utf8'));
    packetArg = '/tmp/ca_packet.json';
    packetRepoPath = packets[0].filename;
  }

  // Feature-only 판정은 run_review_gate.py가 tier='feature-only'로 내려준다.
  // (문서 미변경 + 유효 패킷 없음 → 편집 C scope 밖. 저장소 단일 진실원천으로 통일.)
  const base = context.payload.pull_request?.base?.sha || '';
  let out = '';
  await exec.exec('python3', [
    '.editorial/run_review_gate.py',
    '--numstat', '/tmp/ca_numstat.txt', '--name-status', '/tmp/ca_name_status.txt',
    '--diff', '/tmp/ca_name_status.txt', // diff는 tier 판정에 무관(리뷰 단계 전 tier만 사용)
    '--packet', packetArg, '--packet-repo-path', packetRepoPath,
    '--repo', `${context.repo.owner}/${context.repo.repo}`, '--pr', String(prNumber),
    '--base-sha', base, '--head-sha', headSha,
  ], { ignoreReturnCode: true, listeners: { stdout: (d) => { out += d.toString(); } } });

  const parsed = JSON.parse(out);
  // envelope.report.envelope.packet_sha256에서 현재 packet 해시를 읽는다.
  let packetSha256 = '';
  try {
    const ps = parsed.report && parsed.report.envelope && parsed.report.envelope.packet_sha256;
    if (ps && ps !== '0'.repeat(64)) packetSha256 = String(ps).toLowerCase();
  } catch (_) { /* 무시: 없으면 빈 문자열 */ }

  return { tier: parsed.tier, packetSha256 };
}

module.exports = main;
module.exports.main = main;
module.exports.evaluateApproval = evaluateApproval;
module.exports.normalizeComments = normalizeComments;
module.exports.CONTEXT_NAME = CONTEXT_NAME;
