#!/usr/bin/env python3
"""GitBook markdown → Starlight content 변환기.

루트 GitBook 문서(about-cloud/, ai/, ...)를
starlight/src/content/docs/ko/ 아래로 변환·복사한다.

변환 규칙:
  1. frontmatter: 본문 첫 H1을 title로 승격(본문에서 제거), description은 따옴표 처리
  2. {% hint style="X" %} → :::note|caution|danger|tip / {% endhint %} → :::
  3. {% content-ref url="..." %}[text](url){% endcontent-ref %} → > 📄 [text](url)
  4. {% tabs %}/{% tab title="T" %} 사용 파일 → .mdx로 변환 + <Tabs><TabItem> 컴포넌트
  5. 그 외 본문은 그대로 유지

사용법:
  python3 scripts/gitbook_to_starlight.py            # 전체 변환
  python3 scripts/gitbook_to_starlight.py ai         # 특정 섹션만
  python3 scripts/gitbook_to_starlight.py --validate REF  # REF 시점 원본으로 생성해
                                                     # 기존 starlight 파일과 diff 비교
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_BASE = ROOT / "starlight" / "src" / "content" / "docs" / "ko"
SECTIONS = [
    "about-cloud", "ai", "compute", "database", "devops",
    "governance", "networking", "security", "storage",
]
# 국가별 가이드 — 루트 원본(SOT)에서 재귀 수집. Starlight 전용 수정을 두지 말 것.
COUNTRY_SECTIONS = ["korea", "us", "eu", "japan", "singapore"]
HINT_MAP = {"info": "note", "warning": "caution", "danger": "danger", "success": "tip"}

HINT_RE = re.compile(r'\{%\s*hint\s+style="(\w+)"\s*%\}')
ENDHINT_RE = re.compile(r"\{%\s*endhint\s*%\}")
CONTENT_REF_RE = re.compile(
    r'\{%\s*content-ref\s+url="[^"]*"\s*%\}\s*\n(.*?)\n\{%\s*endcontent-ref\s*%\}',
    re.DOTALL,
)
TABS_OPEN_RE = re.compile(r"\{%\s*tabs\s*%\}")
TABS_CLOSE_RE = re.compile(r"\{%\s*endtabs\s*%\}")
TAB_OPEN_RE = re.compile(r'\{%\s*tab\s+title="([^"]*)"\s*%\}')
TAB_CLOSE_RE = re.compile(r"\{%\s*endtab\s*%\}")
MD_LINK_RE = re.compile(r"\]\(([^)\s]+?\.md)(#[^)]*)?\)")


def rewrite_links(body: str, rel_path: str) -> str:
    """상대 .md 링크를 로케일 무관 상대 URL로 재작성.

    Starlight는 본문 내 .md 상대링크를 변환하지 않으므로 여기서 처리한다.
    페이지 URL은 /<locale>/<section>/<page>/ 형태(디렉터리 깊이 2)이므로
    루트 기준 경로를 '../../<section>/<page>/'로 만든다. (glossary는 깊이 1)
    """
    src_dir = Path(rel_path).parent

    def repl(m):
        target, anchor = m.group(1), m.group(2) or ""
        if target.startswith(("http://", "https://")):
            return m.group(0)
        resolved = (src_dir / target).resolve().relative_to(ROOT.resolve())
        parts = list(resolved.with_suffix("").parts)
        if parts == ["GLOSSARY"]:
            parts = ["glossary"]
        depth = len(Path(rel_path).parts)  # section/file.md → 2, GLOSSARY.md → 1
        url = "../" * depth + "/".join(parts) + "/"
        return f"]({url}{anchor})"

    return MD_LINK_RE.sub(repl, body)


def split_frontmatter(text: str):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        return {}, text
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip().strip("'\"")
    return fm, text[m.end():]


def yaml_quote(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def convert(text: str, rel_path: str):
    """반환: (변환된 본문, mdx 여부)"""
    fm, body = split_frontmatter(text)

    # 첫 H1 → title 승격
    h1 = re.search(r"^# (.+)$", body, re.MULTILINE)
    if not h1:
        raise ValueError(f"{rel_path}: H1 제목 없음")
    title = h1.group(1).strip()
    body = body[: h1.start()] + body[h1.end():]
    body = body.lstrip("\n")

    # hint → aside
    body = HINT_RE.sub(lambda m: ":::" + HINT_MAP[m.group(1)], body)
    body = ENDHINT_RE.sub(":::", body)

    # content-ref → 블록쿼트 링크
    body = CONTENT_REF_RE.sub(lambda m: "> 📄 " + m.group(1).strip(), body)

    # 상대 .md 링크 → URL 경로
    body = rewrite_links(body, rel_path)

    # tabs → MDX Tabs 컴포넌트
    is_mdx = bool(TABS_OPEN_RE.search(body))
    if is_mdx:
        body = TABS_OPEN_RE.sub("<Tabs>", body)
        body = TABS_CLOSE_RE.sub("</Tabs>", body)
        body = TAB_OPEN_RE.sub(lambda m: f'<TabItem label="{m.group(1)}">', body)
        body = TAB_CLOSE_RE.sub("</TabItem>", body)
        body = (
            "import { Tabs, TabItem } from '@astrojs/starlight/components';\n\n"
            + body
        )

    out = ["---", f"title: {yaml_quote(title)}"]
    if fm.get("description"):
        out.append(f"description: {yaml_quote(fm['description'])}")
    out.append("---")
    return "\n".join(out) + "\n\n" + body, is_mdx


def source_files(sections):
    for sec in sections:
        base = ROOT / sec
        if not base.exists():
            continue
        # 국가 가이드는 중첩 경로(korea/security/csap.md 등)
        paths = (
            sorted(base.rglob("*.md"))
            if sec in COUNTRY_SECTIONS
            else sorted(base.glob("*.md"))
        )
        for p in paths:
            yield p.relative_to(ROOT)


def run_convert(sections):
    count = mdx_count = 0
    files = list(source_files(sections))
    # 전체 코어 변환 시 용어집·소개(GitBook 홈 README) 포함
    if set(sections) >= set(SECTIONS):
        for extra in (Path("GLOSSARY.md"), Path("README.md")):
            if extra not in files:
                files.append(extra)
    SPECIAL = {"GLOSSARY.md": Path("glossary.md"), "README.md": Path("introduction.md")}
    for rel in files:
        text = (ROOT / rel).read_text(encoding="utf-8")
        converted, is_mdx = convert(text, str(rel))
        out_rel = SPECIAL.get(rel.name, rel)
        out_path = OUT_BASE / out_rel
        if is_mdx:
            out_path = out_path.with_suffix(".mdx")
            # 동일 slug의 기존 .md 플레이스홀더 제거
            leftover = OUT_BASE / out_rel
            if leftover.exists():
                leftover.unlink()
            mdx_count += 1
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(converted, encoding="utf-8")
        count += 1
    print(f"변환 완료: {count}개 (mdx {mdx_count}개)")


def run_validate(ref: str):
    """REF 시점의 루트 원본을 변환해 기존 starlight 파일과 비교(스크립트 충실도 검증)."""
    import difflib

    mismatches = 0
    for rel in source_files(["ai"]):
        try:
            old = subprocess.run(
                ["git", "show", f"{ref}:{rel}"],
                capture_output=True, text=True, check=True, cwd=ROOT,
            ).stdout
        except subprocess.CalledProcessError:
            print(f"  (skip: {ref}에 {rel} 없음)")
            continue
        generated, _ = convert(old, str(rel))
        existing_path = OUT_BASE / rel
        if not existing_path.exists():
            print(f"  (기존 파일 없음: {rel})")
            continue
        existing = existing_path.read_text(encoding="utf-8")
        if generated.strip() != existing.strip():
            mismatches += 1
            print(f"--- 불일치: {rel}")
            diff = difflib.unified_diff(
                existing.splitlines(), generated.splitlines(),
                "existing", "generated", lineterm="", n=1,
            )
            print("\n".join(list(diff)[:30]))
    print(f"검증 완료: 불일치 {mismatches}개")


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "--validate":
        run_validate(args[1] if len(args) > 1 else "HEAD")
    else:
        # 인자 없으면 코어 + 국가 가이드 전부 변환
        default = SECTIONS + COUNTRY_SECTIONS
        run_convert(args or default)
