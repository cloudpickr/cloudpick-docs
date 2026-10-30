#!/usr/bin/env python3
"""Bounded, advisory source-change scan across the complete Korean corpus.

Content hashes only flag a possible change; they do not prove a factual change,
source authority, or that an unflagged document is current.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import importlib.util
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.editorial'))
from source_fetch import fetch_source  # noqa: E402

spec = importlib.util.spec_from_file_location('link_refresh_guard', ROOT / 'scripts/link-refresh-guard.py')
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)
URL = re.compile(r'https://[^\s<>\[\]{}()\'"`]+')
MAX_URLS = 75
WORKERS = 5


def inventory(root):
    base = root / 'src/content/docs/ko'
    result = {}
    files = sorted(p for p in base.rglob('*') if p.is_file() and p.suffix in ('.md', '.mdx') and not p.is_symlink())
    if not files:
        raise ValueError('no Korean documents found')
    for path in files:
        name = path.relative_to(root).as_posix()
        lines = path.read_text(encoding='utf-8').splitlines(keepends=True)
        mask = guard.protected_mask(lines)
        text = ''.join(re.sub(r'`[^`]*`', '', line) for line, protected in zip(lines, mask) if not protected)
        for match in URL.findall(text):
            url = match.rstrip('.,;:!?。')
            try:
                p = urlsplit(url)
                if p.scheme != 'https' or not p.hostname or p.username or p.password or (p.port and p.port != 443):
                    continue
                canonical = urlunsplit((p.scheme, p.netloc, p.path, p.query, ''))
            except ValueError:
                continue
            result.setdefault(canonical, set()).add(name)
    return {url: sorted(paths) for url, paths in sorted(result.items())}


def scan(refs, previous, now, fetch=fetch_source, limit=MAX_URLS, workers=WORKERS):
    if not isinstance(previous, dict) or limit < 1 or limit > MAX_URLS or workers < 1 or workers > WORKERS:
        raise ValueError('invalid source scan state or limits')
    state = {url: {**previous.get(url, {}), 'paths': paths} for url, paths in refs.items()}
    # Never-checked first, then least-recently checked, including failed URLs.
    selected = sorted(refs, key=lambda url: (state[url].get('checked_at', ''), url))[:limit]
    def check(url):
        try:
            result = fetch(url)
            if not 200 <= result.status < 300:
                return url, {'status': 'unverified', 'error': f'HTTP {result.status}'}
            return url, {'status': 'observed', 'hash': result.body_sha256, 'final_url': result.url}
        except Exception as exc:
            return url, {'status': 'unverified', 'error': type(exc).__name__}
    with ThreadPoolExecutor(max_workers=workers) as pool:
        results = list(pool.map(check, selected))
    candidates = []
    for url, result in results:
        entry = state[url]
        old_hash, old_final = entry.get('hash'), entry.get('final_url')
        entry['checked_at'] = now
        entry['status'] = result['status']
        if result['status'] == 'observed':
            if old_hash and (old_hash != result['hash'] or old_final != result['final_url']):
                for path in entry['paths']:
                    candidates.append({'path': path, 'axis': 1, 'origin': 'source-watch',
                        'reason': f"출처 변경 신호: {url} ({old_hash[:12]} → {result['hash'][:12]})",
                        'source_url': url, 'source_status': 'unverified'})
            entry.update(hash=result['hash'], final_url=result['final_url'])
            entry.pop('error', None)
        else:
            entry['error'] = result['error']
    return {'refs': state, 'checked': len(selected), 'total': len(refs), 'candidates': candidates,
            'failed': sum(1 for _, result in results if result['status'] == 'unverified')}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--previous', required=True)
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    previous = json.loads(Path(args.previous).read_text(encoding='utf-8'))
    now = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    result = scan(inventory(ROOT), previous, now)
    Path(args.output).write_text(json.dumps(result, ensure_ascii=False) + '\n', encoding='utf-8')
    print(f"source scan: {result['checked']}/{result['total']} checked; {result['failed']} unverified; {len(result['candidates'])} change signals")


if __name__ == '__main__':
    main()
