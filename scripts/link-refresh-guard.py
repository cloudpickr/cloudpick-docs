#!/usr/bin/env python3
"""
링크 현행화 가드 — 'URL 문자열 교체만' 했음을 결정론적으로 증명 (council v1 합의).

리다이렉트가 실제 페이지 이전을 가리킬 때, 외부 링크를 최종 URL로 일괄 갱신하는
PR(link-refresh)이 **URL 교체 외의 어떤 변경도 하지 않았음**을 바이트 단위로 강제한다.
LLM보다 먼저 required로 실행되며 차단권을 가진다(fail-closed). 레벨링 가드와 같은 설계.

검증 방식 — '재구성 매칭'(council 합의: 정규식 추출이 아님):
  승인된 old→new 매핑(패킷 manifest)을 base 파일의 각 줄에 '리터럴'로 적용한 재구성본이
  head 파일과 **바이트 완전 일치**해야 한다. 하나라도 어긋나면 FAIL.

  이 방식은 Q4의 URL 파싱 함정(쿼리스트링/앵커/trailing slash/퍼센트 인코딩/마크다운
  링크 vs 본문 URL)을 구조적으로 제거한다 — URL을 '파싱'하지 않고, 승인된 문자열을
  '그대로 치환'해 재구성하기 때문이다.

fail-closed 조건(어느 하나라도 해당하면 차단):
  - base/head 라인 수 불일치(라인 추가·삭제·병합·분할).
  - 재구성본 != head (URL 외 텍스트가 바뀜 — 사실·문장·수치·날짜 변경).
  - 매핑의 old가 head에 그대로 남아 있음(미적용/부분적용).
  - 변경이 코드펜스(``` ... ```)·인라인코드(`...`)·frontmatter(--- ... ---)·
    Mermaid 블록 내부에서 발생(해당 영역은 base==head 바이트 동일을 별도 강제).
  - 매핑 old==new(무의미) 또는 old가 다른 old의 부분문자열(치환 순서 모호성).

사용법:
  python3 scripts/link-refresh-guard.py --base OLD.md --head NEW.md --mapping MAP.json
    MAP.json: {"old_url": "new_url", ...}  (패킷 manifest의 url_map)
  exit 0 = 통과(URL 교체만), exit 1 = 차단(URL 외 변경 의심/적용 오류).

주의: 이 가드는 '링크 현행화'에만 쓴다. 사실을 바꾸는 변경(축1 현행화)은 근거 패킷
PR 경로로 가야 하며 이 가드를 적용하지 않는다.
"""
from __future__ import annotations

import argparse
import json
import re
import sys


def _fail(msg: str) -> None:
    print(f"link-refresh-guard: FAIL — {msg}", file=sys.stderr)
    sys.exit(1)


def _ok(msg: str) -> None:
    print(f"link-refresh-guard: OK — {msg}")
    sys.exit(0)


def load_mapping(path: str) -> dict[str, str]:
    try:
        with open(path, encoding="utf-8") as fh:
            raw = json.load(fh)
    except (OSError, json.JSONDecodeError) as e:
        _fail(f"매핑 파일 로드 실패: {e}")
    if not isinstance(raw, dict) or not raw:
        _fail("매핑이 비었거나 객체가 아님")
    for k, v in raw.items():
        if not isinstance(k, str) or not isinstance(v, str):
            _fail("매핑 키/값은 문자열이어야 함")
        if not k or not v:
            _fail("매핑 키/값은 비어 있을 수 없음")
        if k == v:
            _fail(f"무의미한 매핑(old==new): {k}")
        if not (k.startswith("http://") or k.startswith("https://")):
            _fail(f"old는 절대 URL이어야 함: {k}")
        if not (v.startswith("http://") or v.startswith("https://")):
            _fail(f"new는 절대 URL이어야 함: {v}")
    # old가 다른 old의 부분문자열이면 치환 순서에 따라 결과가 달라짐(모호) → 차단.
    keys = list(raw)
    for a in keys:
        for b in keys:
            if a != b and a in b:
                _fail(f"old가 다른 old의 부분문자열(모호한 치환): {a!r} ⊂ {b!r}")
    return raw


def reconstruct(line: str, mapping: dict[str, str]) -> str:
    """base 라인에 승인 매핑을 '긴 old부터' 리터럴 치환해 head를 재구성.

    인라인코드(`...`) 구간은 치환에서 제외한다(그 안의 URL은 현행화 대상이 아니며,
    main의 3) 검사가 인라인코드 구간 불변을 별도로 강제한다).
    """
    # 인라인코드 구간을 분리해 바깥 세그먼트에만 치환 적용.
    parts = re.split(r"(`[^`]*`)", line)
    out = []
    for seg in parts:
        if seg.startswith("`") and seg.endswith("`") and len(seg) >= 2:
            out.append(seg)  # 인라인코드 — 불변
            continue
        for old in sorted(mapping, key=len, reverse=True):
            if old in seg:
                seg = seg.replace(old, mapping[old])
        out.append(seg)
    return "".join(out)


# 보호 영역(코드/frontmatter/mermaid) 마킹: 해당 영역은 base==head 바이트 동일 강제.
_FENCE = re.compile(r"^\s*(```|~~~)")


def protected_mask(lines: list[str]) -> list[bool]:
    """각 줄이 보호 영역(코드펜스/frontmatter/mermaid) 내부인지 표시."""
    mask = [False] * len(lines)
    in_fence = False
    # frontmatter: 파일 맨 처음의 --- ... ---
    i = 0
    if lines and lines[0].strip() == "---":
        mask[0] = True
        i = 1
        while i < len(lines):
            mask[i] = True
            if lines[i].strip() == "---":
                i += 1
                break
            i += 1
    for j in range(i, len(lines)):
        if _FENCE.match(lines[j]):
            # 펜스 여는/닫는 줄 자체도 보호.
            mask[j] = True
            in_fence = not in_fence
            continue
        if in_fence:
            mask[j] = True
    return mask


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True, help="변경 전 파일(git show BASE:path)")
    ap.add_argument("--head", required=True, help="변경 후 파일(작업 트리/head)")
    ap.add_argument("--mapping", required=True, help="승인된 url_map JSON")
    args = ap.parse_args(argv[1:])

    mapping = load_mapping(args.mapping)

    try:
        with open(args.base, encoding="utf-8", newline="") as fh:
            base = fh.read()
        with open(args.head, encoding="utf-8", newline="") as fh:
            head = fh.read()
    except OSError as e:
        _fail(f"파일 읽기 실패: {e}")

    # 변경 없음 — URL 미적용(이 파일은 매핑 대상이 아니었을 수 있음)이면 통과(no-op).
    if base == head:
        _ok(f"{args.head}: 변경 없음")

    base_lines = base.splitlines(keepends=True)
    head_lines = head.splitlines(keepends=True)

    # 1) 라인 수 불일치 = 추가/삭제/병합/분할 → fail-closed.
    if len(base_lines) != len(head_lines):
        _fail(
            f"{args.head}: 라인 수 변경 base={len(base_lines)} head={len(head_lines)} "
            "(URL 교체는 라인 수를 바꾸지 않는다)"
        )

    # 2) 보호 영역(코드/frontmatter/mermaid)은 base==head 바이트 동일 강제.
    bmask = protected_mask(base_lines)
    for idx, (b, h, prot) in enumerate(zip(base_lines, head_lines, bmask), start=1):
        if prot and b != h:
            _fail(f"{args.head}:{idx}: 보호 영역(코드/frontmatter/mermaid) 내부 변경")

    # 3) 인라인코드(`...`) 내부 변경 금지: 변경된 줄에서 인라인코드 구간이 동일해야 함.
    inline = re.compile(r"`[^`]*`")
    for idx, (b, h) in enumerate(zip(base_lines, head_lines), start=1):
        if b == h:
            continue
        if inline.findall(b) != inline.findall(h):
            _fail(f"{args.head}:{idx}: 인라인코드(`...`) 구간이 변경됨")

    # 4) 재구성 매칭: base에 매핑 적용 → head와 바이트 일치.
    #    보호 영역(코드/frontmatter/mermaid) 줄은 매핑을 적용하지 않는다(그 안의 URL은
    #    현행화 대상이 아니며, 2)에서 base==head 바이트 동일을 이미 강제했다).
    rebuilt = [
        b if prot else reconstruct(b, mapping)
        for b, prot in zip(base_lines, bmask)
    ]
    if "".join(rebuilt) != head:
        # 어느 줄이 어긋났는지 첫 지점을 보고.
        for idx, (r, h) in enumerate(zip(rebuilt, head_lines), start=1):
            if r != h:
                _fail(
                    f"{args.head}:{idx}: 재구성≠head (URL 외 변경 의심)\n"
                    f"  재구성: {r.rstrip()}\n  실제  : {h.rstrip()}"
                )
        _fail(f"{args.head}: 재구성≠head (말미 불일치)")

    # 5) 매핑 old가 '보호 영역·인라인코드 밖'에 남아 있으면 미적용(부분 적용) → 차단.
    #    보호 영역(코드/frontmatter/mermaid)·인라인코드 안의 old URL은 현행화 대상이 아니므로 허용.
    nonprot_lines = [h for h, prot in zip(head_lines, bmask) if not prot]
    nonprot_head = "".join(re.sub(r"`[^`]*`", "", ln) for ln in nonprot_lines)
    for old in mapping:
        if old in nonprot_head:
            _fail(f"{args.head}: old URL이 본문(보호영역·인라인코드 밖)에 잔존(미적용): {old}")

    _ok(f"{args.head}: URL 교체만 확인(재구성 일치)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
