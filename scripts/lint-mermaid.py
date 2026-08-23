#!/usr/bin/env python3
"""
Mermaid 다이어그램 린트 — Mermaid 11.x 호환성 검사

검사 항목:
1. 노드 라벨에 따옴표 없이 슬래시(/) 사용 → syntax error 유발
2. 노드 ID에 공백 → 파서 혼동 (subgraph 제외)

사용법:
  python3 scripts/lint-mermaid.py              # 전체 검사
  python3 scripts/lint-mermaid.py --fix        # 자동 수정 (/ → ·)
"""
import re
import os
import sys

DOCS_DIR = "src/content/docs"
LOCALES = ["ko", "en", "ja"]


def find_issues(content, path):
    issues = []
    blocks = re.findall(r"```mermaid\n(.*?)\n```", content, re.DOTALL)
    for block_idx, block in enumerate(blocks):
        for ln_idx, line in enumerate(block.strip().split("\n"), 1):
            # 따옴표 없이 슬래시가 포함된 노드 라벨
            unquoted = re.findall(r'(?<!\[")\[([^"\]]+/[^\]]+)\]', line)
            for u in unquoted:
                if "<br/>" not in u and "subgraph" not in line:
                    issues.append({
                        "file": path,
                        "block": block_idx + 1,
                        "line": ln_idx,
                        "type": "slash_in_label",
                        "detail": f"[{u}]",
                    })

            # 노드 ID에 공백 (subgraph 제외)
            if "subgraph" not in line.lower():
                id_space = re.findall(r"(\w+\s+\w+)\[", line)
                skip = {"graph TD", "graph LR", "graph RL", "graph BT",
                        "flowchart TD", "flowchart LR", "flowchart RL", "flowchart BT"}
                for m in id_space:
                    if m not in skip:
                        issues.append({
                            "file": path,
                            "block": block_idx + 1,
                            "line": ln_idx,
                            "type": "space_in_id",
                            "detail": f'"{m}"',
                        })
    return issues


def auto_fix(content):
    """슬래시를 중간점(·)으로 자동 교체"""
    def fix_block(match):
        block = match.group(0)
        lines = block.split("\n")
        fixed = []
        for line in lines:
            # 따옴표 없이 [xxx/yyy] → [xxx·yyy] (단, <br/>는 유지)
            def replace_slash(m):
                label = m.group(1)
                if "<br/>" in label:
                    return m.group(0)
                return "[" + label.replace("/", "·") + "]"

            if "subgraph" not in line:
                line = re.sub(r'(?<!\[")\[([^"\]]+/[^\]]+)\]', replace_slash, line)
            fixed.append(line)
        return "\n".join(fixed)

    return re.sub(r"```mermaid\n.*?\n```", fix_block, content, flags=re.DOTALL)


def main():
    fix_mode = "--fix" in sys.argv
    all_issues = []

    for lang in LOCALES:
        lang_dir = os.path.join(DOCS_DIR, lang)
        if not os.path.isdir(lang_dir):
            continue
        for root, _, files in os.walk(lang_dir):
            for f in files:
                if not f.endswith((".md", ".mdx")):
                    continue
                path = os.path.join(root, f)
                content = open(path, encoding="utf-8").read()
                issues = find_issues(content, path)
                all_issues.extend(issues)

                if fix_mode and issues:
                    fixed = auto_fix(content)
                    open(path, "w", encoding="utf-8").write(fixed)

    if all_issues:
        print(f"{'🔧 Fixed' if fix_mode else '❌ FAIL'}: {len(all_issues)} mermaid issue(s)\n")
        for iss in all_issues:
            print(f"  {iss['file']}  block#{iss['block']} line#{iss['line']}  "
                  f"[{iss['type']}] {iss['detail']}")
        if not fix_mode:
            print(f"\nRun with --fix to auto-replace '/' → '·'")
            sys.exit(1)
    else:
        print(f"✅ All mermaid blocks OK ({DOCS_DIR})")


if __name__ == "__main__":
    main()
