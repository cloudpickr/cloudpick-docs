#!/usr/bin/env python3
"""Check internal Markdown/GitBook links for GitBook docs."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", "_book", "node_modules"}

MD_LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
CONTENT_REF_RE = re.compile(r'{%\s*content-ref\s+url="([^"]+)"\s*%}')


def iter_markdown_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*.md"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        files.append(path)
    return sorted(files)


def is_external(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme in {"http", "https", "mailto", "tel"}


def strip_fragment(url: str) -> str:
    return url.split("#", 1)[0]


def check_links(files: list[Path]) -> list[str]:
    errors: list[str] = []
    for path in files:
        text = path.read_text(encoding="utf-8")
        links = [m.group(1).strip() for m in MD_LINK_RE.finditer(text)]
        links += [m.group(1).strip() for m in CONTENT_REF_RE.finditer(text)]

        for raw in links:
            url = raw.strip("<>")
            if not url or url.startswith("#") or is_external(url):
                continue

            target_part = unquote(strip_fragment(url))
            if not target_part:
                continue

            target = (path.parent / target_part).resolve()
            try:
                target.relative_to(ROOT)
            except ValueError:
                errors.append(f"{path.relative_to(ROOT)}: link escapes repo: {raw}")
                continue

            if not target.exists():
                errors.append(f"{path.relative_to(ROOT)}: missing link target: {raw}")

    return errors


def check_summary_coverage(files: list[Path]) -> list[str]:
    summary = ROOT / "SUMMARY.md"
    if not summary.exists():
        return ["SUMMARY.md is missing"]

    text = summary.read_text(encoding="utf-8")
    linked = set()
    for match in MD_LINK_RE.finditer(text):
        url = strip_fragment(match.group(1).strip())
        if url and not is_external(url):
            linked.add(str((summary.parent / unquote(url)).resolve().relative_to(ROOT)))

    actual = {
        str(path.relative_to(ROOT))
        for path in files
        if path.name != "SUMMARY.md"
    }

    errors: list[str] = []
    for path in sorted(actual - linked):
        errors.append(f"SUMMARY.md: missing entry for {path}")
    for path in sorted(linked - actual):
        errors.append(f"SUMMARY.md: entry points to non-existing file {path}")
    return errors


def main() -> int:
    files = iter_markdown_files()
    errors = check_links(files) + check_summary_coverage(files)
    if errors:
        print("Internal link check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Internal link check passed ({len(files)} markdown files).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
