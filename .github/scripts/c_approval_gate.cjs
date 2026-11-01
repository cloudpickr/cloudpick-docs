'use strict';
/**
 * Editorial C-Approval Gate 로직.
 * 사용자 승인 정책: 허용된 사람이 문서와 근거를 확인한 뒤 /approve로 승인한다.
 *
 * 순수 판정 함수(evaluateApproval)는 테스트 가능하게 분리하고, main(github,...)은
 * GitHub API 연동(현재 packet SHA-256 계산·코멘트 조회·commit status 기록)만 담당한다.
 *
 * 허용된 사람의 신규 `/approve`를 문서 base/head blob과 근거 패킷의 지문에 묶는다.
 * link-refresh의 재계산 가능한 manifest_sha256만 지문에서 제외한다. 링크 매핑,
 * 문서 내용, 경로, 그 밖의 패킷 내용이 바뀌면 새 승인이 필요하다.
 *
 * 무관한 커밋은 승인 지문을 바꾸지 않는다. 기존 지문 기록이 PR의 커밋 이력에
 * 남아 있으면 승인을 유지하고, 이력이 재작성되어 기록을 찾지 못하면 다시 승인한다.
 *
 * 원칙:
 *  - GitHub PR Approve(리뷰)는 C 신호가 아니다. 사람의 코멘트를 사용한다.
 *  - PR 작성자 자기승인 여부는 actor로 구분 불가(에이전트/사람이 froguin 인증 공유).
 *    그래서 allowlisted 사람의 코멘트와 승인 지문으로
 *    검증한다. 봇 타입 코멘트 작성자는 제외.
 *  - Feature-only PR(문서 변경 없음 + 유효 패킷 없음)은 편집 LLM/C scope 밖 → 명시적 통과.
 *  - A/B: 이 게이트는 success로 명시 통과(자동 병합은 결정론적 5개 필수 체크가 담당).
 *  - 분류 실패/미설정/판정 불가 = 승인 아님(pending 또는 failure).
 *  - allowlist 임의 추가/자가승인 완화 금지.
 */

const CONTEXT_NAME = 'editorial-c-approval';
const APPROVE_RE = /\/approve\s+([0-9a-f]{64})\b/i;
const SIMPLE_APPROVE_RE = /^\s*\/approve\s*$/i;
const BINDING_PREFIX = 'editorial-approval-binding/';
const crypto = require('node:crypto');

function stable(value) {
  if (Array.isArray(value)) return value.map(stable);
  if (value && typeof value === 'object') return Object.fromEntries(Object.keys(value).sort().map(k => [k, stable(value[k])]));
  return value;
}

function approvalFingerprint(packet, docs) {
  const copy = structuredClone(packet);
  if (copy.policy_action === 'link-refresh' && copy.link_refresh) delete copy.link_refresh.manifest_sha256;
  if (copy.policy_action === 'marker-refresh' && copy.marker_refresh) delete copy.marker_refresh.manifest_sha256;
  const ordered = [...docs].sort((a, b) => a.path.localeCompare(b.path));
  return crypto.createHash('sha256').update(JSON.stringify(stable({packet: copy, docs: ordered}))).digest('hex');
}

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
    fingerprint,
    bindings,
  } = input;

  if (!tier) {
    return { state: 'failure', description: 'classification failed or unavailable (not an approval)' };
  }
  // Out-of-scope PR: src/content/docs/** 변경이 하나도 없음 → 편집 리뷰/C scope 밖.
  // 파일 경로 기준 스코프(scope by file path only): 관리/인프라 코드·워크플로우·
  // .editorial/ 도구·루트 문서 등 비문서 파일은 편집적으로 리뷰하지 않는다. 혼합 PR은
  // run_review_gate.py가 문서 하위집합만 분류하므로 여기서는 그 tier를 그대로 받는다.
  if (tier === 'feature-only') {
    return { state: 'success', description: 'no document changes: out of editorial LLM/C scope' };
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
    if (m && m[1].toLowerCase() !== want) return false;
    if (m && !fingerprint) return true; // compatibility for the standalone legacy evaluator
    return !!(fingerprint && c.id && c.createdAt && c.updatedAt && c.createdAt === c.updatedAt && (m || SIMPLE_APPROVE_RE.test(c.body || '')) && bindings?.[String(c.id)] === fingerprint);
  });
  if (valid.length > 0) {
    return { state: 'success', description: `C confirmed by allowlisted human for packet ${want.slice(0, 12)}` };
  }
  return { state: 'pending', description: `C awaiting allowlisted human confirmation of packet ${want.slice(0, 12)}` };
}

/**
 * 이슈 코멘트를 판정용 형태로 정규화(봇 타입 표시).
 * PR review가 아니라 issue comment를 쓴다.
 */
function normalizeComments(rawComments) {
  return (rawComments || []).map((c) => ({
    user: (c.user && c.user.login) || '',
    body: c.body || '',
    isBot: !!(c.user && c.user.type === 'Bot'),
    id: c.id, createdAt: c.created_at, updatedAt: c.updated_at,
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
  // head SHA는 신뢰된 데이터 조회와 승인 기록 대상이다.
  const { data: fresh } = await github.rest.pulls.get({
    owner: context.repo.owner, repo: context.repo.repo, pull_number: prNumber,
  });
  const headSha = fresh.head.sha;

  // 분류 + 현재 packet SHA-256 계산: 신뢰된 base 코드로 실행.
  let tier = null;
  let packetSha256 = '';
  let fingerprint = '';
  try {
    const computed = await computeTierAndPacketSha({ github, context, exec, prNumber, headSha, core });
    tier = computed.tier;
    packetSha256 = computed.packetSha256;
    if (tier === 'C' && packetSha256) fingerprint = await computeApprovalFingerprint({github, context, prNumber, headSha, baseSha: fresh.base.sha});
  } catch (e) {
    core.warning(`classification error: ${e.message}`);
    tier = null; // 실패는 승인 아님
  }

  // 이슈 코멘트 조회(pagination) → 사람 승인 신호 탐색.
  const rawComments = await github.paginate(github.rest.issues.listComments, {
    owner: context.repo.owner, repo: context.repo.repo, issue_number: prNumber, per_page: 100,
  });
  const confirmations = normalizeComments(rawComments);

  const allowlist = (process.env.C_APPROVAL_ALLOWLIST || '')
    .split(',').map((s) => s.trim().toLowerCase()).filter(Boolean);

  // Bind a new, unedited human command to the exact observed change. The
  // commit status is an append-only GitHub record, not a PR-controlled file.
  const eventComment = context.eventName === 'issue_comment' && context.payload.action === 'created' ? context.payload.comment : null;
  const eligible = confirmations.find(c => c.id === eventComment?.id && !c.isBot && allowlist.includes(c.user.toLowerCase()) && c.createdAt && c.createdAt === c.updatedAt && (SIMPLE_APPROVE_RE.test(c.body) || (APPROVE_RE.exec(c.body)?.[1]?.toLowerCase() === packetSha256)));
  const bindings = {};
  if (tier === 'C' && fingerprint && confirmations.some(c => SIMPLE_APPROVE_RE.test(c.body || '') || APPROVE_RE.test(c.body || ''))) {
    const commits = await github.paginate(github.rest.pulls.listCommits, {owner: context.repo.owner, repo: context.repo.repo, pull_number: prNumber, per_page: 100});
    for (const commit of commits) {
      const statuses = await github.paginate(github.rest.repos.listCommitStatusesForRef, {owner: context.repo.owner, repo: context.repo.repo, ref: commit.sha, per_page: 100});
      for (const status of statuses) {
        const id = status.context?.startsWith(BINDING_PREFIX) ? status.context.slice(BINDING_PREFIX.length) : '';
        if (/^\d+$/.test(id) && status.creator?.login === 'github-actions[bot]' && status.state === 'success' && /^v1:[0-9a-f]{64}$/.test(status.description || '') && !(id in bindings)) bindings[id] = status.description.slice(3);
      }
    }
  }
  if (eligible && fingerprint && tier === 'C' && !(String(eligible.id) in bindings)) {
    const {data: latest} = await github.rest.pulls.get({owner: context.repo.owner, repo: context.repo.repo, pull_number: prNumber});
    if (latest.head.sha !== headSha || latest.base.sha !== fresh.base.sha) throw new Error('PR changed while recording approval; retry on the current revision');
    if (!latest.updated_at || Date.parse(latest.updated_at) > Date.parse(eligible.createdAt)) throw new Error('PR changed after the approval comment; submit a new /approve after reviewing the current revision');
    await github.rest.repos.createCommitStatus({owner: context.repo.owner, repo: context.repo.repo, sha: headSha, state: 'success', context: `${BINDING_PREFIX}${eligible.id}`, description: `v1:${fingerprint}`});
    bindings[String(eligible.id)] = fingerprint;
  }

  const result = evaluateApproval({ tier, packetSha256, allowlist, confirmations, fingerprint, bindings });

  // 현재 head SHA에 commit status 기록(위조 방지: GITHUB_TOKEN으로만 기록).
  await github.rest.repos.createCommitStatus({
    owner: context.repo.owner, repo: context.repo.repo,
    sha: headSha, state: result.state, context: CONTEXT_NAME,
    description: result.description.slice(0, 140),
  });
  core.info(`[${CONTEXT_NAME}] tier=${tier} packet=${packetSha256.slice(0, 12)} state=${result.state} — ${result.description}`);
}

async function computeApprovalFingerprint({github, context, prNumber, headSha, baseSha}) {
  const {owner, repo} = context.repo;
  const files = await github.paginate(github.rest.pulls.listFiles, {owner, repo, pull_number: prNumber, per_page: 100});
  const packets = files.filter(f => /^\.editorial\/packets\/[^/]+\.json$/.test(f.filename));
  if (packets.length !== 1) throw new Error('approval fingerprint requires exactly one packet');
  const {data: packetBlob} = await github.rest.repos.getContent({owner, repo, path: packets[0].filename, ref: headSha});
  const packet = JSON.parse(Buffer.from(packetBlob.content, packetBlob.encoding).toString('utf8'));
  const docs = [];
  for (const f of files.filter(f => f.filename.startsWith('src/content/docs/') || f.previous_filename?.startsWith('src/content/docs/'))) {
    if (!['added','removed','modified','renamed'].includes(f.status)) throw new Error('unsupported document status');
    const previous = f.previous_filename || f.filename;
    let base = null;
    if (f.status !== 'added') {
      const {data} = await github.rest.repos.getContent({owner, repo, path: previous, ref: baseSha});
      if (!data.sha || data.type !== 'file') throw new Error('base document unavailable');
      base = data.sha;
    }
    let head = null;
    if (f.status !== 'removed') {
      const {data} = await github.rest.repos.getContent({owner, repo, path: f.filename, ref: headSha});
      if (!data.sha || data.type !== 'file') throw new Error('head document unavailable');
      head = data.sha;
    }
    docs.push({path: f.filename, previous, status: f.status, base, head});
  }
  if (!docs.length) throw new Error('approval fingerprint requires document changes');
  return approvalFingerprint(packet, docs);
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
  // GitHub API f.status → git name-status 코드. renamed·copied는 previous_filename을 보존하는
  // 3-필드로 만든다. copied(C)는 'C'로 보존(파이썬 분류기가 복사=구조 변경으로 판정). 알 수 없는
  // status를 'M'으로 폴백하면 구조 변경이 modified로 둔갑해 리뷰를 우회하므로(fail-open), 미지
  // status는 'X'(미상)로 보내 분류기가 C로 escalate하게 한다. 'changed'(파일 타입 변경)는
  // 수정이 아니라 'T'(typechange)로 보내 구조 변경으로 잡는다(M으로 두면 tier A 우회).
  const smap = { added: 'A', removed: 'D', modified: 'M', changed: 'T' };
  const threeField = (f) => `${f.status === 'copied' ? 'C100' : 'R100'}\t${f.previous_filename}\t${f.filename}`;
  const nameStatus = files.map((f) => (f.status === 'renamed' || f.status === 'copied')
    ? threeField(f)
    : `${smap[f.status] || 'X'}\t${f.filename}`).join('\n');

  const fs = require('fs');
  const os = require('os');
  const path = require('path');
  // 예측 가능한 /tmp 고정 경로는 심링크/레이스 공격에 노출된다(CodeQL js/insecure-temporary-file).
  // 프로세스마다 고유한 임시 디렉터리를 0700으로 생성하고 그 안에만 쓴다.
  const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'ca-gate-'));
  const numstatPath = path.join(tmpDir, 'numstat.txt');
  const nameStatusPath = path.join(tmpDir, 'name_status.txt');
  const packetPath = path.join(tmpDir, 'packet.json');
  fs.writeFileSync(numstatPath, numstat + '\n');
  fs.writeFileSync(nameStatusPath, nameStatus + '\n');

  // 단일 패킷 파일이면 head SHA 콘텐츠를 데이터로 취득하고 실제 경로를 검증기에 전달.
  const packets = files.filter((f) => /^\.editorial\/packets\/[^/]+\.json$/.test(f.filename));
  let packetArg = 'none';
  let packetRepoPath = '';
  if (packets.length === 1) {
    const { data: blob } = await github.rest.repos.getContent({
      owner: context.repo.owner, repo: context.repo.repo, path: packets[0].filename, ref: headSha,
    });
    fs.writeFileSync(packetPath, Buffer.from(blob.content, blob.encoding).toString('utf8'));
    packetArg = packetPath;
    packetRepoPath = packets[0].filename;
  }

  // Feature-only 판정은 run_review_gate.py가 tier='feature-only'로 내려준다.
  // (문서 미변경 + 유효 패킷 없음 → 편집 C scope 밖. 저장소 단일 진실원천으로 통일.)
  const base = context.payload.pull_request?.base?.sha || '';
  let out = '';
  await exec.exec('python3', [
    '.editorial/run_review_gate.py',
    '--numstat', numstatPath, '--name-status', nameStatusPath,
    '--diff', nameStatusPath, // diff는 tier 판정에 무관(리뷰 단계 전 tier만 사용)
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
module.exports.approvalFingerprint = approvalFingerprint;
