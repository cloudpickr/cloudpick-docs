#!/usr/bin/env python3
"""
축2 매핑 결과를 월간 트래킹 이슈에 코멘트로 제보 (monthly-review.yml daily에서 호출).

map-news-to-docs.py --json 출력(/tmp/news-map.json)을 받아, 반영 후보/미매핑을 코멘트로
작성해 gh CLI로 이슈에 게시한다. 멱등: 같은 날짜 범위 마커가 이미 있으면 skip.
제보 전용 — 반영은 사람/에이전트의 근거 패킷 PR(AGENTS.md 축2).

사용법(워크플로):
  python3 scripts/post-news-map-comment.py <map_json> <issue_number> <date_range>
  (환경변수 GH_TOKEN, GITHUB_REPOSITORY 필요)
"""
from __future__ import annotations

import json
import os
import subprocess
import sys


def main(argv):
    if len(argv) < 3:
        print("usage: post-news-map-comment.py <map_json> <issue> <range>", file=sys.stderr)
        return 0  # advisory — 인자 부족도 이슈를 깨지 않는다
    map_json, issue, rng = argv[0], argv[1], argv[2]
    try:
        with open(map_json, encoding="utf-8") as fh:
            data = json.load(fh)
    except OSError:
        print("매핑 결과 파일 없음 — 생략."); return 0

    s = data.get("summary", {})
    mapped = data.get("mapped", [])
    unmapped = data.get("unmapped", [])
    if not mapped and not unmapped:
        print("매핑 결과 비어 있음 — 코멘트 생략."); return 0

    marker = f"<!-- news-map:{rng} -->"
    lines = [
        marker,
        "## 🔗 새 소식 → 문서 매핑 (축2, 결정론 · 제보 전용)",
        "",
        "위 새 소식을 반영할 **후보 ko 문서**입니다(토큰·별칭 겹침 기반). "
        "'매핑=반영 지시'가 아니며, 공식 출처 확인 후 근거 패킷 PR로 반영합니다.",
        "",
        f"**요약**: 매핑 {s.get('mapped', 0)} · 미매핑 {s.get('unmapped', 0)}",
        "",
    ]
    if mapped:
        lines.append("### 반영 후보")
        for r in mapped[:20]:
            lines.append(f"- {r['news']}" + (f"  ({r['url']})" if r.get("url") else ""))
            for c in r.get("candidates", []):
                p = c["path"].replace("src/content/docs/ko/", "")
                lines.append(f"    → `{p}` (score {c['score']})")
    if unmapped:
        lines.append("")
        lines.append(f"### 미매핑 — 기존 범위 밖일 수 있음(반복되면 축3 신설 검토): {len(unmapped)}건")
        for r in unmapped[:10]:
            lines.append(f"- {r['news']}" + (f"  ({r['url']})" if r.get("url") else ""))
    lines += ["", "_auto-mapped by `monthly-review.yml` (daily, 결정론) — 판단·반영은 담당자 몫._"]
    body = "\n".join(lines)

    repo = os.environ.get("GITHUB_REPOSITORY", "")
    # 멱등: 같은 날짜 범위 코멘트가 이미 있으면 skip.
    existing = subprocess.run(
        ["gh", "api", f"repos/{repo}/issues/{issue}/comments", "--paginate", "--jq", ".[].body"],
        capture_output=True, text=True,
    ).stdout
    if marker in existing:
        print("해당 날짜 매핑 코멘트 이미 존재 — skip."); return 0
    subprocess.run(
        ["gh", "api", f"repos/{repo}/issues/{issue}/comments", "-f", f"body={body}"],
        check=True,
    )
    print(f"매핑 코멘트 게시 완료 (#{issue}).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
