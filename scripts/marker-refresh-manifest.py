#!/usr/bin/env python3
"""
marker-refresh 매니페스트 도구 — 패킷의 manifest_sha256 완전성·불변성 대조.

marker-refresh 패킷은 changed_paths(스키마 상한 64)로 담을 수 없는 대량 문서를
manifest_sha256으로 보증한다(link-refresh-manifest.py와 동형). CI가 verify로
재계산해 대조하며, 불일치는 fail-closed다.

manifest 계산식(양측 동일해야 함):
  payload = json.dumps({
    "changed_paths": sorted(changed_paths),
    "from_month": {ko,en,ja} (키 정렬),
    "to_month":   {ko,en,ja} (키 정렬),
    "base_sha": base_sha,
  }, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
  manifest_sha256 = sha256(payload.encode("utf-8")).hexdigest()

사용법:
  python3 scripts/marker-refresh-manifest.py compute --changed-paths FILE \
      --from-month-ko .. --to-month-ko .. --from-month-en .. --to-month-en .. \
      --from-month-ja .. --to-month-ja .. --base-sha SHA
  python3 scripts/marker-refresh-manifest.py verify --packet P.json \
      --changed-paths FILE --base-sha SHA
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


def _die(msg: str) -> None:
    print(f"marker-refresh-manifest: {msg}", file=sys.stderr)
    sys.exit(1)


def load_packet(path: str) -> dict:
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError) as e:
        _die(f"패킷 로드 실패 {path}: {e}")


def compute_manifest(changed_paths, from_month: dict, to_month: dict, base_sha: str) -> str:
    payload = json.dumps(
        {
            "changed_paths": sorted(changed_paths),
            "from_month": dict(sorted(from_month.items())),
            "to_month": dict(sorted(to_month.items())),
            "base_sha": base_sha,
        },
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _read_paths(path: str) -> list[str]:
    return [l.strip() for l in Path(path).read_text(encoding="utf-8").splitlines() if l.strip()]


def cmd_compute(args) -> int:
    changed = _read_paths(args.changed_paths)
    from_m = {"ko": args.from_month_ko, "en": args.from_month_en, "ja": args.from_month_ja}
    to_m = {"ko": args.to_month_ko, "en": args.to_month_en, "ja": args.to_month_ja}
    print(compute_manifest(changed, from_m, to_m, args.base_sha))
    return 0


def cmd_verify(args) -> int:
    d = load_packet(args.packet)
    mr = d.get("marker_refresh")
    if not mr:
        _die(f"marker_refresh 블록 없음: {args.packet}")
    from_m = mr.get("from_month") or {}
    to_m = mr.get("to_month") or {}
    claimed = mr.get("manifest_sha256")
    count = mr.get("changed_paths_count")

    for key, obj in (("from_month", from_m), ("to_month", to_m)):
        if set(obj) != {"ko", "en", "ja"}:
            _die(f"{key}에 ko/en/ja 키가 모두 있어야 함: {sorted(obj)}")

    changed = _read_paths(args.changed_paths)
    if count != len(changed):
        _die(f"changed_paths_count={count} != 실제 변경 {len(changed)}개")
    recomputed = compute_manifest(changed, from_m, to_m, args.base_sha)
    if recomputed != claimed:
        _die(f"manifest_sha256 불일치\n  패킷: {claimed}\n  재계산: {recomputed}")
    print(f"marker-refresh-manifest: OK — manifest 일치({len(changed)} paths)")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("compute")
    for loc in ("ko", "en", "ja"):
        c.add_argument(f"--from-month-{loc}", required=True)
        c.add_argument(f"--to-month-{loc}", required=True)
    c.add_argument("--changed-paths", required=True)
    c.add_argument("--base-sha", required=True)
    v = sub.add_parser("verify")
    v.add_argument("--packet", required=True)
    v.add_argument("--changed-paths", required=True)
    v.add_argument("--base-sha", required=True)
    args = ap.parse_args(argv[1:])
    if args.cmd == "compute":
        return cmd_compute(args)
    if args.cmd == "verify":
        return cmd_verify(args)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
