'use strict';
/**
 * Editorial C-Approval Gate 로직.
 * 계약: froguin/multi-agent-stack@3113cfc §Review(5).
 *
 * 순수 판정 함수(evaluateApproval)는 테스트 가능하게 분리하고, main(github,...)은
 * GitHub API 연동(head SHA 재확인·리뷰 조회·commit status 기록)만 담당한다.
 *
 * 원칙:
 *  - C 승인: allowlist에 속한 '사람'이 '현재 head SHA'에 대해 approved 상태여야 한다.
 *    작성자·봇·에이전트 제외. dismissed/stale/이전 SHA 승인은 무효.
 *  - A/B: 이 게이트는 success로 명시 통과(자동 병합은 결정론적 5개 필수 체크가 담당).
 *  - 분류 실패/미설정/판정 불가 = 승인 아님(pending 또는 failure).
 *
 * 적용 맥락(중요):
 *  - 이 게이트는 '봇/에이전트가 작성한 핸드오프 PR'에 대해 사람(froguin)의 발행 승인을
 *    요구하는 것이 주 용도다. 사람(froguin)이 직접 작성한 PR은 GitHub이 자기승인을
 *    막고 이 게이트도 author 제외로 자가승인을 불허한다(allowlist에 있어도 무효).
 *    즉 froguin 작성 C PR은 다른 allowlisted 사람이 없으면 통과 불가 — 이는 의도된
 *    보수적 동작이다. 실제 스택 PR actor(봇/에이전트)의 신원 독립성 확인은 Grok 담당.
 *  - allowlist 임의 추가/자가승인 완화 금지.
 */

const CONTEXT_NAME = 'editorial-c-approval';

/**
 * 순수 판정. GitHub API 없이 입력만으로 결정한다.
 * @returns {{state:'success'|'failure'|'pending', description:string}}
 */
function evaluateApproval(input) {
  const {
    tier,                // 'A' | 'B' | 'C' | null(분류실패)
    headSha,             // 현재 PR head SHA
    prAuthor,            // PR 작성자 login
    allowlist,           // 허용된 사람 login 배열(소문자)
    reviews,             // [{user, state, commitId, authorAssociation, isBot}]
  } = input;

  if (!tier) {
    return { state: 'failure', description: 'classification failed or unavailable (not an approval)' };
  }
  if (tier === 'A' || tier === 'B') {
    // 독립 재분류가 A/B로 성공 → 이 게이트는 통과. 병합 자체는 필수 체크가 최종 결정.
    return { state: 'success', description: `tier ${tier}: no separate human C-approval required` };
  }
  // tier === 'C'
  if (!allowlist || allowlist.length === 0) {
    return { state: 'failure', description: 'C requires human approval but allowlist is unset (no arbitrary approver)' };
  }
  if (!headSha) {
    return { state: 'failure', description: 'C: current head SHA unavailable' };
  }
  const author = (prAuthor || '').toLowerCase();
  const valid = (reviews || []).filter((r) => {
    if (r.state !== 'APPROVED') return false;          // 최신 상태가 approved만
    if (r.commitId !== headSha) return false;          // 정확히 현재 head SHA
    if (r.isBot) return false;                          // 봇 제외
    const login = (r.user || '').toLowerCase();
    if (login === author) return false;                 // 작성자 제외
    if (!allowlist.includes(login)) return false;       // allowlist 인원만
    return true;
  });
  if (valid.length > 0) {
    return { state: 'success', description: `C approved by allowlisted human on head ${headSha.slice(0, 7)}` };
  }
  return { state: 'pending', description: `C awaiting allowlisted human approval of head ${headSha.slice(0, 7)}` };
}

/** 최신 리뷰만 남긴다(사용자별 마지막 제출). dismissed는 제외. */
function latestReviewsPerUser(rawReviews) {
  const byUser = new Map();
  for (const r of rawReviews) {
    const login = (r.user && r.user.login) || '';
    const prev = byUser.get(login);
    if (!prev || r.submitted_at > prev.submitted_at) byUser.set(login, r);
  }
  const out = [];
  for (const r of byUser.values()) {
    if (r.state === 'DISMISSED') continue;
    out.push({
      user: (r.user && r.user.login) || '',
      state: r.state,
      commitId: r.commit_id,
      authorAssociation: r.author_association,
      isBot: !!(r.user && r.user.type === 'Bot'),
    });
  }
  return out;
}

async function main({ github, context, core, exec }) {
  const pr = context.payload.pull_request
    || (context.payload.issue && context.payload.issue.pull_request ? context.payload.issue : null);
  if (!pr) {
    core.info('No pull request in context; skipping.');
    return;
  }
  const prNumber = context.payload.pull_request?.number || context.payload.issue?.number;

  // 이벤트마다 현재 PR 신원/head를 API로 재확인(오래된 이벤트 payload 신뢰 금지).
  const { data: fresh } = await github.rest.pulls.get({
    owner: context.repo.owner, repo: context.repo.repo, pull_number: prNumber,
  });
  const headSha = fresh.head.sha;
  const prAuthor = fresh.user.login;

  // 분류: 신뢰된 base 코드의 classify_change.py를 diff에 대해 실행.
  // (여기서는 tier를 계산해 넘긴다. 실제 diff 수집은 base 스크립트가 담당.)
  let tier = null;
  try {
    tier = await computeTier({ github, context, exec, prNumber, headSha, core });
  } catch (e) {
    core.warning(`classification error: ${e.message}`);
    tier = null; // 실패는 승인 아님
  }

  // 리뷰 조회(100개 초과도 pagination으로 모두) → 최신·유효만
  const rawReviews = await github.paginate(github.rest.pulls.listReviews, {
    owner: context.repo.owner, repo: context.repo.repo, pull_number: prNumber, per_page: 100,
  });
  const reviews = latestReviewsPerUser(rawReviews);

  const allowlist = (process.env.C_APPROVAL_ALLOWLIST || '')
    .split(',').map((s) => s.trim().toLowerCase()).filter(Boolean);

  const result = evaluateApproval({ tier, headSha, prAuthor, allowlist, reviews });

  // 현재 head SHA에 commit status 기록(위조 방지: GITHUB_TOKEN으로만 기록).
  await github.rest.repos.createCommitStatus({
    owner: context.repo.owner, repo: context.repo.repo,
    sha: headSha, state: result.state, context: CONTEXT_NAME,
    description: result.description.slice(0, 140),
  });
  core.info(`[${CONTEXT_NAME}] tier=${tier} state=${result.state} — ${result.description}`);
}

/** diff를 받아 tier 계산. 검증된 단일 패킷만 scope 예외로 인정하기 위해
 *  run_review_gate.py(패킷 검증·filename 확인·scope 예외 통일)에 위임하고 tier만 읽는다.
 *  LLM 미설정이어도 출력 JSON의 tier는 유효(승인 여부는 별도). */
async function computeTier({ github, context, exec, prNumber, headSha, core }) {
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
  return JSON.parse(out).tier;
}

module.exports = main;
module.exports.main = main;
module.exports.evaluateApproval = evaluateApproval;
module.exports.latestReviewsPerUser = latestReviewsPerUser;
module.exports.CONTEXT_NAME = CONTEXT_NAME;
