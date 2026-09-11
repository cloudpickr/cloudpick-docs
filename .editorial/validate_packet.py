#!/usr/bin/env python3
"""
근거 패킷(evidence packet) trusted validator — 저장소 측(문서 Actions) 검증기.

계약: froguin/multi-agent-stack@53618d6 docs/architecture/editorial-actions-contract.md
스키마: .editorial/packet.schema.json

이 검증기는 신뢰된 base-branch 코드로 실행된다(PR 코드/텍스트는 데이터로만 취급).
형식 스키마로 잡을 수 없는 항목을 추가로 강제한다:
  - 파서 레벨: 중복 JSON 키 거부(strict), BOM 거부
  - 파일 레벨: 128 KiB(UTF-8) 상한, 후행 개행(trailing newline) 정책
  - 경로 정규화: ../ ./ 심볼릭·정규화 후 탈출을 정규 상대경로로 재확인
  - 파일명 == jira_key 일치
  - target_path ∈ changed_paths
  - checked_at RFC3339 timezone 필수(스키마 pattern과 이중 확인)

중요 (계약 원칙):
  - 형식 통과 ≠ 내용 신뢰. status=verified 자기신고, 출처 실재/내용 일치는
    별도 리뷰 단계(공식 출처 독립 fetch)에서 확인한다. 이 검증기는 '형식·구조·경로
    안전'만 책임진다.
  - 검증 실패/unknown은 절대 pass로 변환하지 않는다(호출부에서 non-zero exit).

exit code: 0=유효, 1=검증 실패, 2=사용법/입력 오류.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MAX_PACKET_BYTES = 128 * 1024  # 128 KiB (UTF-8 직렬화)
SCHEMA_PATH = Path(__file__).parent / "packet.schema.json"
DOC_PATH_RE = re.compile(r"^src/content/docs/(ko|en|ja)/.+\.mdx?$")
CHECKED_AT_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})$"
)


class PacketError(Exception):
    """검증 실패. 메시지는 사람이 읽을 수 있는 사유."""


def _reject_duplicate_keys(pairs):
    """strict JSON: 같은 객체에 중복 키가 있으면 거부."""
    seen = {}
    for key, value in pairs:
        if key in seen:
            raise PacketError(f"duplicate JSON key: {key!r}")
        seen[key] = value
    return seen


def load_packet_bytes(raw: bytes) -> dict:
    """바이트 → 검증된 dict. 파일/파서 레벨 검사를 여기서 수행."""
    if len(raw) > MAX_PACKET_BYTES:
        raise PacketError(
            f"packet exceeds {MAX_PACKET_BYTES} bytes (got {len(raw)})"
        )
    if raw.startswith(b"\xef\xbb\xbf"):
        raise PacketError("packet must not start with a UTF-8 BOM")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise PacketError(f"packet is not valid UTF-8: {exc}") from exc
    # 후행 개행 정책: 정확히 하나의 trailing newline 허용, 그 외(0개·2개+·공백)는 거부.
    if not text.endswith("\n"):
        raise PacketError("packet must end with exactly one trailing newline")
    if text.endswith("\n\n"):
        raise PacketError("packet must not end with multiple trailing newlines")
    try:
        data = json.loads(text, object_pairs_hook=_reject_duplicate_keys)
    except json.JSONDecodeError as exc:
        raise PacketError(f"packet is not valid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise PacketError("packet root must be a JSON object")
    return data


def _norm_reject_traversal(path: str, field: str) -> None:
    """경로 정규화 재확인: 스키마 정규식 위에 정규 상대경로로 탈출 방지."""
    if not isinstance(path, str):
        raise PacketError(f"{field}: path must be a string")
    if not DOC_PATH_RE.match(path):
        raise PacketError(f"{field}: not under src/content/docs/(ko|en|ja): {path!r}")
    if "\\" in path:
        raise PacketError(f"{field}: backslash not allowed: {path!r}")
    if any(ord(c) < 0x20 or ord(c) == 0x7F for c in path):
        raise PacketError(f"{field}: control character in path: {path!r}")
    segments = path.split("/")
    if any(seg in ("", ".", "..") for seg in segments):
        raise PacketError(f"{field}: empty/./.. segment not allowed: {path!r}")
    # 정규화 후에도 동일 경로여야 하고 접두어를 유지해야 한다.
    normalized = "/".join(segments)
    if normalized != path or not normalized.startswith("src/content/docs/"):
        raise PacketError(f"{field}: path escapes docs root after normalization: {path!r}")


def validate_schema(data: dict) -> None:
    """JSON Schema 형식 검증(있으면). jsonschema 미설치 시 필수 필드만 확인."""
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    try:
        import jsonschema
    except ImportError:
        for req in schema.get("required", []):
            if req not in data:
                raise PacketError(f"missing required field: {req}")
        return
    validator = jsonschema.Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(data), key=lambda e: list(e.path))
    if errors:
        first = errors[0]
        loc = "/".join(str(p) for p in first.path) or "(root)"
        raise PacketError(f"schema: {loc}: {first.message}")


def validate_semantics(data: dict, packet_path: Path | None) -> None:
    """스키마 밖의 계약 규칙(경로 정규화·파일명 일치·target∈changed·checked_at)."""
    _norm_reject_traversal(data["target_path"], "target_path")
    for idx, p in enumerate(data["changed_paths"]):
        _norm_reject_traversal(p, f"changed_paths[{idx}]")

    if data["target_path"] not in data["changed_paths"]:
        raise PacketError("target_path must be included in changed_paths")

    if packet_path is not None:
        expected = f"{data['jira_key']}.json"
        if packet_path.name != expected:
            raise PacketError(
                f"filename {packet_path.name!r} must match jira_key ({expected!r})"
            )

    for i, claim in enumerate(data.get("claim_ledger", [])):
        ca = claim.get("checked_at")
        if ca is not None and not CHECKED_AT_RE.match(ca):
            raise PacketError(f"claim_ledger[{i}].checked_at needs RFC3339 timezone: {ca!r}")
        # 출처 최소 1개(스키마 anyOf와 이중 확인)
        if "source_url" not in claim and not claim.get("sources"):
            raise PacketError(f"claim_ledger[{i}]: source_url or sources required")


def validate_packet(raw: bytes, packet_path: Path | None = None) -> dict:
    data = load_packet_bytes(raw)
    validate_schema(data)
    validate_semantics(data, packet_path)
    return data


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: validate_packet.py <packet.json>", file=sys.stderr)
        return 2
    path = Path(argv[1])
    if not path.is_file():
        print(f"::error::packet not found: {path}", file=sys.stderr)
        return 2
    try:
        validate_packet(path.read_bytes(), path)
    except PacketError as exc:
        # 실패는 절대 pass로 변환하지 않는다.
        print(f"::error::invalid evidence packet ({path}): {exc}", file=sys.stderr)
        return 1
    print(f"✅ evidence packet valid: {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
