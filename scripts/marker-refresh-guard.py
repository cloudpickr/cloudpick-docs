#!/usr/bin/env python3
"""
marker-refresh 가드 — 리뷰 기준 마커의 '월 토큰만' 바뀌었음을 결정론적으로 증명.

marker-refresh는 문서의 리뷰 기준 마커 라인(`> 문서 기준: …`, `> Last reviewed: …`,
`> 文書基準: …`)의 월 표기만 한 달 승격하는 변경이다. 새로운 사실 주장이 없으므로
패킷 claim_ledger는 비어도 정당하지만(link-refresh와 같은 성격), 그 '사실 불변'을
사람이 아니라 결정론 가드가 전수 증명해야 머지 자동화가 신뢰할 수 있다.

이 가드는 link-refresh-guard.py와 같은 fail-closed 구조를 따른다:

  1) base==head면 통과(no-op; 이 파일은 승격 대상이 아니었을 수 있음).
  2) 라인 수가 바뀌면 fail(마커 월 교체는 라인 수를 바꾸지 않는다).
  3) 변경된 라인은 '정확히' 리뷰 기준 마커 라인이어야 하고, 그 라인에서 바뀐 부분은
     승인된 월 토큰(from_month → to_month)뿐이어야 한다. 마커 접두사·뒤 부가문구·
     그 외 모든 라인은 base와 바이트 동일해야 한다(재구성 매칭).
  4) 마커가 아닌 라인이 하나라도 바뀌면 fail(본문·코드·frontmatter 변경 = 사실 변경
     의심 → 축1 근거 패킷 경로로 보내야 함).

로케일은 마커 접두사로 자동 판별한다(ko/en/ja). from/to 월은 로케일별 표기로 받는다.

사용법:
  python3 scripts/marker-refresh-guard.py --base BASE --head HEAD \
      --from-month-ko '2026년 9월'  --to-month-ko '2026년 10월' \
      --from-month-en 'September 2026' --to-month-en 'October 2026' \
      --from-month-ja '2026年9月' --to-month-ja '2026年10月'

Exit: 0 = 마커 월 교체만 확인 / 1 = 위반(fail-closed).
"""
from __future__ import annotations

import argparse
import re
import sys

# 로케일별 리뷰 기준 마커의 '접두사'(월 토큰 바로 앞까지). 월 토큰은 이 접두사 뒤에 온다.
# 마커 라인은 `>` 인용으로 시작하며, 접두사 뒤에 '월 토큰 + (선택적) 부가문구'가 붙는다.
MARKER_PREFIX = {
    "ko": "문서 기준: ",
    "en": "Last reviewed: ",
    "ja": "文書基準: ",
}

# 로케일별 월 토큰의 '정확한' 구문. 월 토큰은 '연·월만' 담아야 하며 임의 접미사를 허용하지
# 않는다(예: 'October 2026; HIPAA certified' 같은 주장 삽입 차단 — 리뷰 봇 P1). 전각 숫자는
# 쓰지 않는다는 레포 관례를 반영해 ASCII 숫자만 허용한다.
_MONTH_EN = {
    "january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6,
    "july": 7, "august": 8, "september": 9, "october": 10, "november": 11, "december": 12,
}
_MONTH_RE = {
    "ko": re.compile(r"^(?P<y>\d{4})년 (?P<m>\d{1,2})월$"),
    "en": re.compile(r"^(?P<name>[A-Z][a-z]+) (?P<y>\d{4})$"),
    "ja": re.compile(r"^(?P<y>\d{4})年(?P<m>\d{1,2})月$"),
}


def parse_month(loc: str, token: str) -> tuple[int, int] | None:
    """로케일 월 토큰을 (연, 월)로 파싱. 구문이 정확히 '연·월'이 아니면 None.

    임의 접미사·접두사를 허용하지 않아, 월 토큰에 사실 주장을 몰래 끼워 넣는 우회를 막는다.
    """
    m = _MONTH_RE[loc].match(token.strip())
    if not m:
        return None
    if loc == "en":
        mon = _MONTH_EN.get(m.group("name").lower())
        if mon is None:
            return None
        return int(m.group("y")), mon
    mon = int(m.group("m"))
    if not 1 <= mon <= 12:
        return None
    return int(m.group("y")), mon


def _fail(msg: str) -> None:
    print(f"❌ marker-refresh-guard: {msg}", file=sys.stderr)
    sys.exit(1)


def _ok(msg: str) -> None:
    print(f"✅ marker-refresh-guard: {msg}")
    sys.exit(0)


def marker_locale(line: str) -> str | None:
    """라인이 리뷰 기준 마커 라인이면 로케일을 반환, 아니면 None.

    마커 라인은 '>'로 시작하는 인용이며 로케일별 접두사를 포함한다. 선행 공백과
    '>' 뒤 공백을 허용한다. (예: '> 문서 기준: 2026년 9월 (부가)')
    """
    stripped = line.lstrip()
    if not stripped.startswith(">"):
        return None
    body = stripped[1:].lstrip()
    for loc, prefix in MARKER_PREFIX.items():
        if body.startswith(prefix):
            return loc
    return None


def promote_line(line: str, months: dict[str, tuple[str, str]]) -> tuple[str, str | None]:
    """마커 라인의 월 토큰을 from→to로 '한 번만' 치환한 결과와 사용된 로케일을 반환.

    마커 라인이 아니면 (line, None). 마커 라인이지만 from_month가 접두사 바로 뒤에
    오지 않으면(=승격 대상 월이 아님) 치환 없이 (line, loc)로 돌려보내 호출부가
    base==head 여부로 판정하게 한다(no-op 라인 보존).
    """
    loc = marker_locale(line)
    if loc is None:
        return line, None
    from_m, to_m = months[loc]
    prefix = MARKER_PREFIX[loc]
    idx = line.find(prefix)
    if idx < 0:
        return line, loc
    after = idx + len(prefix)
    # 접두사 '바로 뒤'가 from_month여야 한다(월 토큰은 접두사 직후에 온다).
    if line[after:after + len(from_m)] == from_m:
        new = line[:after] + to_m + line[after + len(from_m):]
        return new, loc
    return line, loc


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True, help="변경 전 파일(git show BASE:path)")
    ap.add_argument("--head", required=True, help="변경 후 파일(작업 트리/head)")
    ap.add_argument("--from-month-ko", required=True)
    ap.add_argument("--to-month-ko", required=True)
    ap.add_argument("--from-month-en", required=True)
    ap.add_argument("--to-month-en", required=True)
    ap.add_argument("--from-month-ja", required=True)
    ap.add_argument("--to-month-ja", required=True)
    args = ap.parse_args(argv[1:])

    months = {
        "ko": (args.from_month_ko, args.to_month_ko),
        "en": (args.from_month_en, args.to_month_en),
        "ja": (args.from_month_ja, args.to_month_ja),
    }
    # 월 토큰은 '정확히 연·월' 구문이어야 한다(임의 접미사로 주장 삽입 차단 — 리뷰 봇 P1).
    parsed_from, parsed_to = {}, {}
    for loc, (f, t) in months.items():
        if not f or not t or f == t:
            _fail(f"{loc} from/to 월 토큰이 비었거나 동일함: {f!r}→{t!r}")
        pf = parse_month(loc, f)
        pt = parse_month(loc, t)
        if pf is None:
            _fail(f"{loc} from_month이 '연·월' 구문이 아님(접미사 등 불허): {f!r}")
        if pt is None:
            _fail(f"{loc} to_month이 '연·월' 구문이 아님(접미사 등 불허): {t!r}")
        parsed_from[loc] = pf
        parsed_to[loc] = pt
    # 세 로케일이 같은 (연,월)을 가리켜야 한다(로케일별로 다른 달로 승격하는 비대칭 차단).
    if len(set(parsed_from.values())) != 1:
        _fail(f"from_month이 로케일 간 불일치: {parsed_from}")
    if len(set(parsed_to.values())) != 1:
        _fail(f"to_month이 로케일 간 불일치: {parsed_to}")

    try:
        with open(args.base, encoding="utf-8", newline="") as fh:
            base = fh.read()
        with open(args.head, encoding="utf-8", newline="") as fh:
            head = fh.read()
    except OSError as e:
        _fail(f"파일 읽기 실패: {e}")

    # base==head — 승격 대상이 아니었던 파일(no-op) → 통과.
    if base == head:
        _ok(f"{args.head}: 변경 없음")

    base_lines = base.splitlines(keepends=True)
    head_lines = head.splitlines(keepends=True)

    # 2) 라인 수 변경 = 추가/삭제/병합/분할 → fail-closed.
    if len(base_lines) != len(head_lines):
        _fail(
            f"{args.head}: 라인 수 변경 base={len(base_lines)} head={len(head_lines)} "
            "(마커 월 교체는 라인 수를 바꾸지 않는다)"
        )

    # 3·4) 재구성 매칭: base의 각 라인에 '마커 월 승격'을 적용한 결과가 head와 바이트 일치.
    #      마커가 아닌 라인은 그대로 둔다 → 그런 라인이 바뀌었다면 재구성≠head로 fail.
    rebuilt = []
    changed_marker_lines = 0
    for b in base_lines:
        nb, _ = promote_line(b, months)
        rebuilt.append(nb)
    if "".join(rebuilt) != head:
        for idx, (r, h, b) in enumerate(zip(rebuilt, head_lines, base_lines), start=1):
            if r != h:
                loc = marker_locale(b)
                if loc is None:
                    _fail(
                        f"{args.head}:{idx}: 마커가 아닌 라인이 변경됨 (사실/본문 변경 의심 — "
                        f"근거 패킷 경로로 보내세요)\n  base: {b.rstrip()}\n  head: {h.rstrip()}"
                    )
                _fail(
                    f"{args.head}:{idx}: 마커 라인이 승인된 월 교체 외로 변경됨\n"
                    f"  재구성: {r.rstrip()}\n  실제  : {h.rstrip()}"
                )
        _fail(f"{args.head}: 재구성≠head (말미 불일치)")

    # 실제로 월이 승격된 마커 라인이 최소 1개는 있어야 의미 있는 변경(no-op는 위에서 통과).
    for b, h in zip(base_lines, head_lines):
        if b != h and marker_locale(b) is not None:
            changed_marker_lines += 1
    if changed_marker_lines == 0:
        _fail(f"{args.head}: 변경은 있으나 승격된 마커 라인이 없음(마커 외 변경)")

    _ok(f"{args.head}: 마커 월 교체만 확인(재구성 일치, {changed_marker_lines}개 마커)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
