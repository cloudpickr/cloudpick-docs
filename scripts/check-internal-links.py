#!/usr/bin/env python3
"""Check internal Markdown/GitBook links and document quality for GitBook docs."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", "_book", "node_modules", "memory"}
META_FILES = {"README.md", "SUMMARY.md", "GLOSSARY.md", "CONTRIBUTING.md"}

MD_LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
CONTENT_REF_RE = re.compile(r'{%\s*content-ref\s+url="([^"]+)"\s*%}')
DATE_RE = re.compile(r"문서 기준:\s*\d{4}년\s*\d{1,2}월")
REFERENCE_RE = re.compile(r"^##\s*참고하기", re.MULTILINE)
VOLATILE_RE = re.compile(
    r"(?:\$[\d,.]+|무료\s*(?:제공|티어)|할인|리전\s*수|AZ\s*수|\d+\s*Gbps|\d+\s*TB|~\d+%)",
)


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
            resolved = str((summary.parent / unquote(url)).resolve().relative_to(ROOT))
            if Path(resolved).name not in META_FILES:
                linked.add(resolved)

    actual = {
        str(path.relative_to(ROOT))
        for path in files
        if path.name not in META_FILES
    }

    errors: list[str] = []
    for path in sorted(actual - linked):
        errors.append(f"SUMMARY.md: missing entry for {path}")
    for path in sorted(linked - actual):
        errors.append(f"SUMMARY.md: entry points to non-existing file {path}")
    return errors


def is_content_file(path: Path) -> bool:
    """Return True if the file is a content document (not a meta file)."""
    return path.name not in META_FILES


def check_doc_date(files: list[Path]) -> list[str]:
    """Check that content files have a '문서 기준: YYYY년 M월' line."""
    warnings: list[str] = []
    for path in files:
        if not is_content_file(path):
            continue
        text = path.read_text(encoding="utf-8")
        if not DATE_RE.search(text):
            warnings.append(f"{path.relative_to(ROOT)}: '문서 기준:' 누락")
    return warnings


def check_reference_section(files: list[Path]) -> list[str]:
    """Check that content files have a '## 참고하기' section."""
    warnings: list[str] = []
    for path in files:
        if not is_content_file(path):
            continue
        text = path.read_text(encoding="utf-8")
        if not REFERENCE_RE.search(text):
            warnings.append(f"{path.relative_to(ROOT)}: '## 참고하기' 섹션 누락")
    return warnings


def check_volatile_keywords(files: list[Path]) -> list[str]:
    """Warn about lines containing volatile data (prices, counts, etc.)."""
    warnings: list[str] = []
    for path in files:
        if not is_content_file(path):
            continue
        for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if VOLATILE_RE.search(line):
                snippet = line.strip()[:80]
                warnings.append(f"{path.relative_to(ROOT)}:{i}: 변동성 키워드 — {snippet}")
    return warnings


def main() -> int:
    files = iter_markdown_files()
    errors = check_links(files) + check_summary_coverage(files)

    # Quality warnings (non-blocking)
    warnings: list[str] = []
    warnings += check_doc_date(files)
    warnings += check_reference_section(files)
    warnings += check_volatile_keywords(files)

    if warnings:
        print(f"⚠️  Document quality warnings ({len(warnings)}):")
        for w in warnings:
            print(f"  - {w}")
        print()

    if errors:
        print("❌ Internal link check failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"✅ Internal link check passed ({len(files)} markdown files).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
