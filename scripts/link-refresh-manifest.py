#!/usr/bin/env python3
"""
link-refresh 매니페스트 도구 — 패킷의 url_map 병합 + manifest_sha256 대조 (council 합의).

link-refresh 패킷은 changed_paths(스키마 상한 64)로 담을 수 없는 대량 분산 변경을
manifest_sha256으로 완전성·불변성 보증한다. 이 도구는 CI에서 두 가지를 한다:

  merge   : PR이 변경한 패킷들의 link_refresh.url_map을 하나로 병합해 출력(가드 입력용).
  verify  : 패킷의 manifest_sha256이 (정렬된 changed_paths + 정렬된 url_map +
            base_sha)의 재계산 해시와 일치하는지, changed_paths_count가
            실제 변경 파일 수와 맞는지 대조. 불일치는 exit 1(fail-closed).

manifest 계산식(양측 동일해야 함):
  payload = json.dumps({
    "changed_paths": sorted(changed_paths),
    "url_map": dict(sorted(url_map.items())),
    "base_sha": base_sha,
  }, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
  manifest_sha256 = sha256(payload.encode("utf-8")).hexdigest()

사용법:
  python3 scripts/link-refresh-manifest.py merge  <packet.json> [<packet.json> ...]
  python3 scripts/link-refresh-manifest.py compute --changed-paths FILE --url-map FILE \
      --base-sha SHA
  python3 scripts/link-refresh-manifest.py verify --packet P.json \
      --changed-paths FILE --base-sha SHA
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


def _die(msg: str) -> None:
    print(f"link-refresh-manifest: {msg}", file=sys.stderr)
    sys.exit(1)


def load_packet(path: str) -> dict:
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError) as e:
        _die(f"패킷 로드 실패 {path}: {e}")


def compute_manifest(changed_paths, url_map, base_sha: str) -> str:
    payload = json.dumps(
        {
            "changed_paths": sorted(changed_paths),
            "url_map": dict(sorted(url_map.items())),
            "base_sha": base_sha,
        },
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def cmd_merge(packets: list[str]) -> int:
    merged: dict[str, str] = {}
    for p in packets:
        d = load_packet(p)
        lr = d.get("link_refresh")
        if not lr or not isinstance(lr.get("url_map"), dict):
            _die(f"패킷에 link_refresh.url_map 없음: {p}")
        for k, v in lr["url_map"].items():
            if k in merged and merged[k] != v:
                _die(f"url_map 충돌(같은 old, 다른 new): {k}")
            merged[k] = v
    if not merged:
        _die("병합된 url_map이 비었음")
    json.dump(merged, sys.stdout)
    print(f"url_map {len(merged)}개 병합", file=sys.stderr)
    return 0


def cmd_compute(args) -> int:
    changed = [l.strip() for l in Path(args.changed_paths).read_text(encoding="utf-8").splitlines() if l.strip()]
    url_map = json.loads(Path(args.url_map).read_text(encoding="utf-8"))
    print(compute_manifest(changed, url_map, args.base_sha))
    return 0


def cmd_verify(args) -> int:
    d = load_packet(args.packet)
    lr = d.get("link_refresh")
    if not lr:
        _die(f"link_refresh 블록 없음: {args.packet}")
    url_map = lr.get("url_map") or {}
    claimed = lr.get("manifest_sha256")
    count = lr.get("changed_paths_count")

    changed = [l.strip() for l in Path(args.changed_paths).read_text(encoding="utf-8").splitlines() if l.strip()]
    if count != len(changed):
        _die(f"changed_paths_count={count} != 실제 변경 {len(changed)}개")
    recomputed = compute_manifest(changed, url_map, args.base_sha)
    if recomputed != claimed:
        _die(f"manifest_sha256 불일치\n  패킷: {claimed}\n  재계산: {recomputed}")
    print(f"link-refresh-manifest: OK — manifest 일치({len(changed)} paths, {len(url_map)} mappings)")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    m = sub.add_parser("merge")
    m.add_argument("packets", nargs="+")
    c = sub.add_parser("compute")
    c.add_argument("--changed-paths", required=True)
    c.add_argument("--url-map", required=True)
    c.add_argument("--base-sha", required=True)
    v = sub.add_parser("verify")
    v.add_argument("--packet", required=True)
    v.add_argument("--changed-paths", required=True)
    v.add_argument("--base-sha", required=True)
    args = ap.parse_args(argv[1:])
    if args.cmd == "merge":
        return cmd_merge(args.packets)
    if args.cmd == "compute":
        return cmd_compute(args)
    if args.cmd == "verify":
        return cmd_verify(args)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
