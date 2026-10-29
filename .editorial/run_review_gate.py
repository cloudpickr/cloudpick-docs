#!/usr/bin/env python3
"""
리뷰 게이트 오케스트레이터 — 패킷검증→분류→(B/C)독립리뷰를 하나로 묶어 verdict 산출.

계약: froguin/multi-agent-stack@53618d6 §Review

입력(모두 신뢰된 base 코드가 데이터로 취급; PR head 코드 실행 없음):
  --numstat FILE        git diff --numstat (워크플로우가 GitHub API로 생성)
  --name-status FILE    git diff --name-status
  --diff FILE           통합 diff 텍스트(리뷰 데이터)
  --packet FILE|none    PR head의 단일 패킷 JSON을 API로 데이터 취득한 파일(없으면 'none')
  --repo, --pr, --base-sha, --head-sha   envelope 신원(GitHub 신뢰 값)

출력: stdout에 JSON {tier, verdict, state, reasons, envelope_key}.
exit code: 0=state success, 1=state failure(changes_requested 등), 2=state pending/error(비승인).

원칙:
  - 패킷 없음/스키마 불일치/unknown provenance를 A로 낮추지 않는다. 문서 실변경이면 B/C 보류.
  - 검증된 '일치' 패킷만 scope 예외로 인정(파일명=jira_key, target∈changed 등 validate 통과).
  - 실패/미설정/outage는 success로 변환하지 않는다.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import classify_change as cc  # noqa: E402
import review_runner as rr    # noqa: E402
import validate_packet as vp  # noqa: E402
import envelope as ev         # noqa: E402


def _state_from_verdict(verdict: str) -> str:
    if verdict == "approve":
        return "success"
    if verdict == "changes_requested":
        return "failure"
    return "pending"  # error / skipped-unconfigured / boundary holds


DOC_ROOT = "src/content/docs/"


def run(args) -> dict:
    numstat = Path(args.numstat).read_text(encoding="utf-8")
    name_status = Path(args.name_status).read_text(encoding="utf-8")
    all_changes = cc.parse_numstat_and_status(numstat, name_status)

    # 파일 경로 기준 스코프(scope by file path only) ---------------------------
    # editorial-review는 CloudPick '문서'(src/content/docs/**)만 평가한다. 관리/인프라
    # 코드, 워크플로우, .editorial/ 도구, 루트 문서 등 비문서 파일은 편집 리뷰 범위 밖이며
    # C로 escalate하지 않는다. 혼합 PR이라도 비문서 파일은 무시하고 문서 변경만 분류·리뷰한다.
    #   - 문서 변경이 하나도 없으면(비문서 전용 PR 포함) 편집 scope 밖 → 명시적 통과.
    #   - 문서 변경이 있으면 그 하위집합만 A/B/C 판정. 비문서 파일은 분류 입력에서 제외.
    # rename(R)은 '새 경로(path)'뿐 아니라 '이전 경로(old_path)'도 본다. 문서를 docs 밖으로
    # 이동(docs → non-docs)하면 새 경로만 보면 scope를 벗어나 조용히 통과하지만, 이는 실질적
    # '문서 이동/삭제'이므로 scope에 포함해 구조 변경(C)으로 판정해야 한다(무결성). 반대로
    # docs 안으로 들어오는 이동(non-docs → docs)도 새 경로가 docs라 당연히 포함된다.
    def _in_docs_scope(c) -> bool:
        if c.path.startswith(DOC_ROOT):
            return True
        if c.old_path and c.old_path.startswith(DOC_ROOT):
            return True
        return False

    changes = [c for c in all_changes if _in_docs_scope(c)]
    if not changes:
        return _out("feature-only", "approve",
                    ["no src/content/docs/** changes — out of editorial LLM/C scope "
                     "(non-document files are not editorially reviewed)"],
                    args, "")

    # 패킷 취득·검증 -----------------------------------------------------------
    packet = None
    packet_valid = False
    packet_reasons: list[str] = []
    packet_sha = ""
    packet_repo_path = (args.packet_repo_path or "").strip()  # GitHub API의 실제 저장소 경로
    if args.packet and args.packet != "none" and Path(args.packet).is_file():
        raw = Path(args.packet).read_bytes()
        packet_sha = ev.packet_sha256(raw)
        # 검증기에는 '실제 저장소 경로'를 넘긴다(내용의 jira_key로 재구성하지 않음).
        # 파일명==jira_key 불일치를 실제로 잡기 위함(#3 자기비교 제거).
        if not packet_repo_path:
            packet_reasons.append("packet repo path not provided — cannot verify filename")
        else:
            try:
                packet = vp.validate_packet(raw, Path(packet_repo_path))
                packet_valid = True
            except Exception as exc:  # noqa: BLE001 — 어떤 검증 실패든 승인 아님
                packet_reasons.append(f"packet invalid: {exc}")
                packet = None

    # 분류: 검증된 패킷만 신뢰. 무효/부재 패킷은 classify에 넘기지 않는다(A 하향 방지).
    #  또한 '검증된 단일 패킷 파일 경로'만 구조판정 scope 예외로 넘긴다(#1). 이렇게 해야
    #  패킷 신규파일(.editorial/packets/*.json 추가)이 모든 B를 C로 만들지 않는다.
    #  invalid/unrelated metadata는 예외에서 제외(예외 경로를 넘기지 않음).
    #  또한 '문서를 패킷 경로로 rename'한 경우는 면제하지 않는다: old_path가 docs였던
    #  rename(R)의 목적지가 패킷 경로와 같으면, 이는 standalone 패킷 추가가 아니라 구조적
    #  '문서 이동'이다. 목적지 경로만 보고 면제하면 그 이동이 scope에서 다시 빠져 tier A로
    #  통과(리뷰 우회)하므로, 이 경우 면제 대상에서 제외한다(codex 리뷰 지적).
    trusted_packet = packet if packet_valid else None
    exempt_paths: list[str] = []
    if packet_valid and packet_repo_path:
        packet_is_doc_rename_target = any(
            c.status in ("R", "C") and c.path == packet_repo_path
            and c.old_path and c.old_path.startswith(DOC_ROOT)
            for c in changes
        )
        if not packet_is_doc_rename_target:
            exempt_paths = [packet_repo_path]
    result = cc.classify(changes, trusted_packet, packet_scope_exempt=exempt_paths)
    tier = result.tier
    reasons = list(result.reasons) + packet_reasons

    # A: 결정론적 게이트로 충분. 단, 패킷이 첨부됐는데 무효면 A로 인정하지 않는다.
    if tier == "A":
        if args.packet and args.packet != "none" and not packet_valid:
            return _out("C", "changes_requested",
                        ["attached packet failed validation — not eligible for A"] + reasons,
                        args, packet_sha)
        return _out("A", "approve", ["tier A: deterministic checks only"] + reasons,
                    args, packet_sha)

    # B/C: 패킷이 유효해야 진행. 없음/무효면 보류(비승인) — A로 낮추지 않음.
    if not packet_valid:
        return _out(tier, "error",
                    ["B/C requires a valid evidence packet; none valid → hold"] + reasons,
                    args, packet_sha)

    # 독립 LLM 리뷰. claim_ledger의 공식 출처를 source_fetch로 독립 재취득해 리뷰에 연결(#2).
    config = rr.ReviewConfig.from_env()
    diff_text = Path(args.diff).read_text(encoding="utf-8") if Path(args.diff).is_file() else ""
    source_evidence, source_reasons = _fetch_sources(packet)
    if source_evidence is None:
        # SSRF 차단·fetch 실패는 non-pass(승인 아님).
        return _out(tier, "error",
                    ["independent source fetch failed/blocked — hold"] + source_reasons + reasons,
                    args, packet_sha)
    review = rr.run_review(config, packet, diff_text, source_evidence=source_evidence)
    reasons += [f"review:{review.verdict}"] + review.reasons + source_reasons

    # 레벨링(legal-B) 전용: 의미 보존 검사 추가. 결정론 가드(leveling-guard)는 사실 불변을
    # 강제하지만 '뉘앙스 왜곡'(부정 뒤집힘·서법어 소실·조건 삭제·벤더 편향)은 못 잡는다.
    # writer-distinct 리뷰어가 닫힌 enum만 '차단' 신호로 낸다(contradicted 선언 금지).
    # block=True면 changes_requested로 하향(승인 취소). error/미설정은 비차단(보류 유지).
    if _is_leveling_packet(packet) and review.verdict == "approve":
        mp = _meaning_preserved_from_diff(diff_text, packet)
        if mp.get("block"):
            reasons += ["leveling meaning-preserved review: BLOCK"] + \
                       [f"{s['type']}: '{s['before'][:40]}' → '{s['after'][:40]}'" for s in mp.get("signals", [])]
            reviewer_cfg = review.selected_model or (config.reviewer_model or "unset")
            return _out(tier, "changes_requested", reasons, args, packet_sha, reviewer_cfg)
        if mp.get("error"):
            # fail-closed: 의미보존 검사를 못 돌리면 approve로 떨어지지 않는다(hold).
            # 레벨링 예외는 '모든 가드 충족'이 전제이므로, 검사 불가 = 비승인(Codex P1, AGENTS.md).
            reviewer_cfg = review.selected_model or (config.reviewer_model or "unset")
            return _out(tier, "error",
                        [f"leveling meaning-preserved review unavailable → hold ({mp['error']})"] + reasons,
                        args, packet_sha, reviewer_cfg)
        reasons.append("leveling meaning-preserved review: ok")

    # link-refresh(URL-only 현행화) 전용: 사실 불변은 결정론 가드(scripts/link-refresh-guard.py)가
    # CI required 잡으로 전수 증명한다(base/head 전체 파일 필요 — diff만으론 불가). 또한
    # governance 투표 반영: url_map의 각 old URL을 독립 re-fetch해 리다이렉트 체인이 new로
    # 끝남을 '실제로' 확인한다(빈 claim_ledger로 fetch가 스킵되던 fail-open 차단). path-collapse나
    # 최종 URL 불일치는 hold(비승인). 이 게이트는 분류·독립 리뷰·redirect 재확인까지 책임지고,
    # URL 외 불변 증명은 CI 가드가 담당한다(가드 required는 라벨이 아니라 분류 자격에서 파생).
    if _is_link_refresh_packet(packet):
        lr = packet.get("link_refresh") or {}
        url_map = lr.get("url_map") or {}
        if not url_map:
            return _out(tier, "error",
                        ["link-refresh packet without link_refresh.url_map → hold"] + reasons,
                        args, packet_sha)
        # url_map key/value는 절대 http(s) URL이어야 한다(게이트에서도 강제 — council 권고).
        bad = [f"{k}→{v}" for k, v in url_map.items()
               if not (isinstance(k, str) and isinstance(v, str)
                       and k.startswith(("http://", "https://"))
                       and v.startswith(("http://", "https://")))]
        if bad:
            return _out(tier, "error",
                        ["link-refresh url_map has non-URL entries → hold"] + bad[:5] + reasons,
                        args, packet_sha)
        rchk = _verify_redirect_chains(url_map)
        if rchk.get("error"):
            # fetch 불가/차단/부분실패는 비승인(보류) — 리다이렉트=실제 이전 보증을 확인 못 함.
            return _out(tier, "error",
                        [f"link-refresh redirect re-fetch unavailable → hold ({rchk['error']})"] + reasons,
                        args, packet_sha)
        if rchk.get("mismatches"):
            reasons += ["link-refresh redirect re-fetch: MISMATCH"] + \
                       [f"{m['old']} → 최종 {m['final']} (기대 {m['expected']})" for m in rchk["mismatches"][:10]]
            return _out(tier, "changes_requested", reasons, args, packet_sha)
        reasons.append(f"link-refresh redirect re-fetch: ok ({rchk.get('checked', 0)} URLs → new)")

        # governance 투표(A): 가드를 editorial-review(이미 required) 안에서 직접 강제한다.
        # diff 재구성 매칭으로 'URL 교체만' 했음을 확인하고, 위반 시 non-pass로 머지를 막는다.
        # (별도 link-refresh-guard 잡이 required 미등록이어도 이 경로가 차단을 보증한다.)
        rc = _link_refresh_reconstruct_from_diff(diff_text, url_map)
        if rc.get("error"):
            return _out(tier, "error",
                        [f"link-refresh reconstruct check unavailable → hold ({rc['error']})"] + reasons,
                        args, packet_sha)
        if rc.get("block"):
            reasons += ["link-refresh reconstruct(diff): BLOCK — URL 외 변경 의심"] + rc.get("signals", [])[:10]
            return _out(tier, "changes_requested", reasons, args, packet_sha)
        reasons.append("link-refresh reconstruct(diff): ok (URL 교체만)")
        reasons.append("link-refresh: URL-only change — CI link-refresh-guard(재구성 매칭, 전체 파일)도 교차 강제")

    # 감사 정확성: 실제 선택된 리뷰어 model을 envelope에 기록(단일 고정값 아님).
    reviewer_cfg = review.selected_model or (config.reviewer_model or "unset")
    return _out(tier, review.verdict, reasons, args, packet_sha, reviewer_cfg)


def _is_leveling_packet(packet: dict) -> bool:
    """패킷이 레벨링(표현 전용) 성격인지 — claim_ledger 비었고 tier_reasons에 leveling 표기."""
    if not isinstance(packet, dict) or packet.get("claim_ledger"):
        return False
    reasons = " ".join(packet.get("tier_reasons", []) or [])
    return ("leveling" in reasons.lower()) or ("레벨링" in reasons)


def _is_link_refresh_packet(packet: dict) -> bool:
    """패킷이 link-refresh(URL-only 현행화) 성격인지 — claim_ledger 비었고
    policy_action=='link-refresh'(단일 필드, governance 투표 반영: tier_reasons 매칭 제거)."""
    if not isinstance(packet, dict) or packet.get("claim_ledger"):
        return False
    return (packet.get("policy_action") or "") == "link-refresh"


def _normalize_url(u: str) -> str:
    """리다이렉트 최종 URL 비교용 정규화 — trailing slash·fragment 차이만 흡수."""
    from urllib.parse import urlsplit, urlunsplit
    s = urlsplit(u.strip())
    path = s.path or "/"
    # 끝 슬래시 1개만 정규화(의미 있는 경로 차이는 보존).
    if len(path) > 1 and path.endswith("/"):
        path = path.rstrip("/") or "/"
    return urlunsplit((s.scheme.lower(), s.netloc.lower(), path, s.query, ""))


def _verify_redirect_chains(url_map: dict) -> dict:
    """link-refresh url_map의 각 old URL을 독립 re-fetch해 최종 URL이 new와 일치하는지 확인.

    governance 투표 반영: 빈 claim_ledger로 source fetch가 스킵되어 '리다이렉트=실제 이전'
    보증이 비던 fail-open을 차단한다. source_fetch(SSRF 방어·상한)를 재사용한다.

    반환: {checked:int, mismatches:[{old,final,expected}], error?:str}
      - error: 모듈 부재/전체 fetch 실패 등 '확인 불가'(→ 호출부에서 hold).
      - mismatches: old의 리다이렉트 체인이 new로 끝나지 않음(→ 호출부에서 changes_requested).
    """
    try:
        import source_fetch as sf
    except Exception as e:  # noqa: BLE001
        return {"error": f"source_fetch import 실패: {e}", "checked": 0, "mismatches": []}

    mismatches = []
    checked = 0
    errors = []
    for old, new in url_map.items():
        try:
            res = sf.fetch_source(old)
        except Exception as e:  # noqa: BLE001  (SSRF 차단·네트워크 실패 포함)
            errors.append(f"{old}: {e}")
            continue
        checked += 1
        final = getattr(res, "final_url", None) or getattr(res, "url", None) or ""
        if _normalize_url(final) != _normalize_url(new):
            mismatches.append({"old": old, "final": final, "expected": new})
    # 하나도 확인 못 했거나(전부 실패) 일부라도 실패하면(부분 실패) 확인 불가 → error.
    # governance 투표(B): 부분 실패를 통과시키면 '확인 안 된 old→new'가 승인되는 fail-open.
    if errors:
        return {"error": "일부/전체 old URL fetch 실패(확인 불가): " + "; ".join(errors[:5]),
                "checked": checked, "mismatches": mismatches, "fetch_errors": errors}
    return {"checked": checked, "mismatches": mismatches, "fetch_errors": []}


def _link_refresh_reconstruct_from_diff(diff_text: str, url_map: dict) -> dict:
    """통합 diff에서 'URL 교체만' 했음을 재구성 매칭으로 검증(가드를 editorial-review 안에서 강제).

    governance 투표(A): link-refresh-guard 잡이 required로 등록돼 있지 않아 가드가 머지를
    못 막던 fail-open을 닫는다. 이미 required인 editorial-review(run_review_gate)가 직접
    diff 기반 재구성을 수행하고, 위반 시 non-pass verdict을 낸다. (base/head 전체 파일이
    필요한 CI 잡 가드와 짝을 이루지만, 이 diff 검사만으로도 머지 차단을 보증한다.)

    각 '변경된 라인쌍'(연속한 - 다음 +)에서 삭제줄에 url_map을 리터럴 적용한 결과가 추가줄과
    바이트 일치해야 한다. 불일치·짝 안 맞음·순수 추가/삭제(짝 없는 +/-)는 block.
    반환: {block: bool, signals: [str], error?: str}
    """
    if not diff_text:
        return {"block": False, "signals": [], "error": "empty diff"}
    # governance 투표: GitHub이 대용량/다파일 PR에서 patch를 생략하면('(no textual patch)')
    # diff에 -/+ 라인이 없어 재구성이 'block:false'로 통과하는 fail-open이 된다. link-refresh는
    # 수백 파일이라 발생 확률이 높다 → patch 누락/절단은 error(hold)로 폴백(전체파일 가드가 1차 방어).
    if "(no textual patch)" in diff_text:
        return {"block": False, "signals": [],
                "error": "patch 생략 감지('(no textual patch)') — diff로 검증 불가, link-refresh-guard(전체파일)로만 검증"}
    try:
        import importlib.util
        import pathlib
        guard_path = pathlib.Path(__file__).resolve().parent.parent / "scripts" / "link-refresh-guard.py"
        spec = importlib.util.spec_from_file_location("link_refresh_guard", guard_path)
        lrg = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(lrg)
    except Exception as exc:  # noqa: BLE001
        return {"block": False, "signals": [], "error": f"link-refresh-guard import 실패: {exc}"}

    signals = []
    # 통합 diff를 hunk별로 돌며 - 블록과 + 블록을 순서대로 모아 1:1 대응시킨다.
    minus, plus = [], []

    def flush():
        # 삭제/추가 블록을 라인 단위 1:1로 재구성 비교.
        if len(minus) != len(plus):
            signals.append(f"라인 증감(삭제 {len(minus)} vs 추가 {len(plus)}) — URL 교체는 라인수 불변")
            return
        for m, p in zip(minus, plus):
            rebuilt = lrg.reconstruct(m, url_map)
            if rebuilt != p:
                signals.append(f"재구성≠추가: '{m.strip()[:50]}' → '{p.strip()[:50]}'")
        minus.clear()
        plus.clear()

    for line in diff_text.splitlines():
        if line.startswith("+++") or line.startswith("---"):
            continue
        if line.startswith("@@"):
            flush()
            continue
        if line.startswith("-"):
            minus.append(line[1:])
        elif line.startswith("+"):
            plus.append(line[1:])
        else:
            # 문맥 라인 → 지금까지의 -/+ 블록을 정산.
            flush()
    flush()

    return {"block": bool(signals), "signals": signals}


def _meaning_preserved_from_diff(diff_text: str, packet: dict) -> dict:
    """diff의 삭제(-)/추가(+) 라인을 before/after로 모아 의미 보존 검사에 넘긴다.

    leveling_core.meaning_preserved_review를 호출(writer-distinct 리뷰어, 닫힌 enum).
    반환은 그 결과({block, signals, error?}). 모듈/게이트웨이 부재 시 error를 반환하며,
    호출부(run)는 이 error를 fail-closed로 처리한다(검사 불가 → 승인 아님, hold).
    """
    try:
        import leveling_core as lc
    except Exception as exc:  # noqa: BLE001
        return {"block": False, "signals": [], "error": f"leveling_core import failed: {exc}"}
    before, after = [], []
    for ln in diff_text.splitlines():
        if ln.startswith("-") and not ln.startswith("---"):
            before.append(ln[1:])
        elif ln.startswith("+") and not ln.startswith("+++"):
            after.append(ln[1:])
    if not before and not after:
        return {"block": False, "signals": []}
    writer = (packet or {}).get("writer") or {}
    return lc.meaning_preserved_review("\n".join(before), "\n".join(after), writer=writer)


def _fetch_sources(packet: dict):
    """claim_ledger의 각 공식 출처를 독립 fetch. 하나라도 차단/실패면 (None, reasons).

    성공 시 (url -> FetchResult 요약) dict를 리뷰에 넘긴다. 출처가 없으면 빈 dict(리뷰가
    근거 부재로 판단하도록). 계약 §Evidence: fetcher는 SSRF·상한을 강제한다.
    """
    import source_fetch as sfetch
    evidence = {}
    reasons = []
    urls = []
    for claim in (packet or {}).get("claim_ledger", []):
        if claim.get("source_url"):
            urls.append(claim["source_url"])
        for s in claim.get("sources", []) or []:
            if s.get("source_url"):
                urls.append(s["source_url"])
    for url in urls:
        try:
            r = sfetch.fetch_source(url)
            evidence[url] = {"status": r.status, "sha256": r.body_sha256, "bytes": r.body_bytes}
        except sfetch.FetchError as exc:
            reasons.append(f"source fetch blocked/failed: {url}: {exc}")
            return None, reasons  # non-pass
    return evidence, reasons


def _out(tier, verdict, reasons, args, packet_sha, reviewer_cfg=None) -> dict:
    envelope = ev.ReviewEnvelope(
        repo=args.repo, pr_number=int(args.pr),
        base_sha=args.base_sha, head_sha=args.head_sha,
        packet_sha256=packet_sha or ("0" * 64),
        policy_version=ev.POLICY_VERSION,
        reviewer_config_version=(reviewer_cfg
                                 or rr.ReviewConfig.from_env().reviewer_model or "unset"),
        checked_at=args.now or "1970-01-01T00:00:00Z",
        expires_at=args.expires or "1970-01-08T00:00:00Z",
    )
    state = _state_from_verdict(verdict)
    return {
        "tier": tier, "verdict": verdict, "state": state,
        "reasons": reasons, "envelope_key": envelope.key(),
        "report": envelope.to_report(verdict, reasons),
    }


def main(argv) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--numstat", required=True)
    p.add_argument("--name-status", required=True, dest="name_status")
    p.add_argument("--diff", required=True)
    p.add_argument("--packet", default="none")
    p.add_argument("--packet-repo-path", default="", dest="packet_repo_path",
                   help="GitHub API가 보고한 패킷의 실제 저장소 경로(파일명 검증용)")
    p.add_argument("--repo", required=True)
    p.add_argument("--pr", required=True)
    p.add_argument("--base-sha", required=True, dest="base_sha")
    p.add_argument("--head-sha", required=True, dest="head_sha")
    p.add_argument("--now", default=None)
    p.add_argument("--expires", default=None)
    args = p.parse_args(argv)

    out = run(args)
    print(json.dumps(out, ensure_ascii=False, indent=2))
    # 상태를 exit code로 정확히 반영(fail을 녹색으로 마감하지 않음).
    if out["state"] == "success":
        return 0
    if out["state"] == "failure":
        return 1
    return 2  # pending/error/hold


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
