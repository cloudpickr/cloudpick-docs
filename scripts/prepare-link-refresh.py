#!/usr/bin/env python3
"""Bounded URL-only draft preparation. No factual approval or merge authority."""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.editorial'))
from source_fetch import fetch_source  # noqa: E402
from validate_packet import validate_packet  # noqa: E402


def load_script(name):
    spec = importlib.util.spec_from_file_location(name.replace('-', '_'), ROOT / 'scripts' / f'{name}.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


GUARD = load_script('link-refresh-guard')
MANIFEST = load_script('link-refresh-manifest')
REGULATED = {'korea', 'japan', 'eu', 'us', 'singapore'}
LINK = re.compile(r'\]\((https://[^\s()<>]+)\)')
MAX_FILE = 2 * 1024 * 1024
MAX_URLS = 12
MAX_DOCS = 8
MAX_SECONDS = 120


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()


def eligible_mapping(old, new):
    """Initial scope: Google's docs host migration, exact path/query/fragment only.

    This selects drafts, never proves semantic equivalence. Everything else is held.
    """
    a, b = urlsplit(old), urlsplit(new)
    return (a.scheme == b.scheme == 'https'
            and a.netloc == 'cloud.google.com' and b.netloc == 'docs.cloud.google.com'
            and a.path == b.path and a.query == b.query and a.fragment == b.fragment
            and 'docs' in a.path.split('/') and a.path != '/')


def body_links(raw):
    lines = raw.decode('utf-8').splitlines(keepends=True)
    mask = GUARD.protected_mask(lines)
    text = ''.join(re.sub(r'`[^`]*`', '', line) for line, protected in zip(lines, mask) if not protected)
    return sorted(set(LINK.findall(text)))


def reconstruct(raw, mapping):
    lines = raw.decode('utf-8').splitlines(keepends=True)
    def replace_line(line):
        return ''.join(part if part.startswith('`') else LINK.sub(
            lambda match: '](' + mapping.get(match.group(1), match.group(1)) + ')', part)
            for part in re.split(r'(`[^`]*`)', line))
    return ''.join(line if protected else replace_line(line)
                   for line, protected in zip(lines, GUARD.protected_mask(lines))).encode('utf-8')


def guard_bytes(base, head, mapping):
    with tempfile.TemporaryDirectory() as folder:
        tmp = Path(folder)
        (tmp / 'base').write_bytes(base)
        (tmp / 'head').write_bytes(head)
        (tmp / 'map').write_text(json.dumps(mapping))
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            try:
                GUARD.main(['guard', '--base', str(tmp / 'base'), '--head', str(tmp / 'head'), '--mapping', str(tmp / 'map')])
            except SystemExit as exc:
                if exc.code != 0:
                    raise ValueError('full-file reconstruction guard rejected candidate') from exc


def prepare_mirrors(root, relative, mapping):
    """Validate all mirrors and guards before writing any file."""
    changes = {}
    for locale in ('ko', 'en', 'ja'):
        name = f'src/content/docs/{locale}/{relative}'
        path = root / name
        if (any(p.is_symlink() for p in (path, *path.parents) if p != root and p.is_relative_to(root))
                or not path.is_file() or path.stat().st_size > MAX_FILE):
            raise ValueError(f'missing/unsafe/oversized locale: {name}')
        # No symlinked ancestor may escape the repository.
        if not path.resolve().is_relative_to((root / f'src/content/docs/{locale}').resolve()):
            raise ValueError(f'path escapes locale: {name}')
        raw = path.read_bytes()
        links = body_links(raw)
        if any(old not in links for old in mapping):
            raise ValueError(f'mapping absent from locale Markdown links: {name}')
        head = reconstruct(raw, mapping)
        if head == raw:
            raise ValueError(f'no locale change: {name}')
        guard_bytes(raw, head, mapping)
        changes[name] = head
    return changes


def candidate_paths(root, target=None, day=None):
    base = root / 'src/content/docs/ko'
    paths = sorted(p for p in base.rglob('*') if p.suffix in {'.md', '.mdx'}
                   and p.relative_to(base).parts[0] not in REGULATED and not p.is_symlink())
    if target:
        paths = [p for p in paths if p.relative_to(base).as_posix() == target]
        if not paths:
            raise ValueError('target must be an existing non-regulatory ko document relative path')
    elif paths:
        # A rotating, bounded batch; repeated failures cannot pin scanning to the first page.
        start = ((day or datetime.now(timezone.utc).date()).toordinal() * MAX_DOCS) % len(paths)
        paths = (paths[start:] + paths[:start])[:MAX_DOCS]
    return paths


def scan(root, target=None, fetch=fetch_source, now=time.monotonic, previous_pr=None):
    report = {'status': 'advisory', 'auto_merge': False, 'checked_urls': 0, 'findings': [], 'candidate': None}
    deadline = now() + MAX_SECONDS
    cache = {}
    for path in candidate_paths(root, target):
        if path.stat().st_size > MAX_FILE:
            continue
        relative = path.relative_to(root / 'src/content/docs/ko').as_posix()
        mapping = {}
        for old in body_links(path.read_bytes()):
            parsed = urlsplit(old)
            if parsed.netloc != 'cloud.google.com' or 'docs' not in parsed.path.split('/'):
                continue
            if old not in cache:
                if report['checked_urls'] >= MAX_URLS or now() >= deadline:
                    report['budget_exhausted'] = True
                    break
                report['checked_urls'] += 1
                try:
                    result = fetch(old)
                    cache[old] = (result.status, result.url)
                except Exception as exc:
                    cache[old] = (None, type(exc).__name__)
            status, final = cache[old]
            if status and 200 <= status < 300 and eligible_mapping(old, final):
                mapping[old] = final
            elif status is None or not 200 <= status < 300 or final != old:
                report['findings'].append({'path': relative, 'url': old, 'status': 'unverified', 'http_status': status, 'final': final})
        if mapping:
            try:
                prepare_mirrors(root, relative, mapping)
                candidate = {'path': relative, 'url_map': mapping}
                previous = previous_pr(candidate) if previous_pr else None
                if previous:
                    report['findings'].append({'path': relative, 'status': 'hold',
                                               'reason': 'candidate already proposed; continuing bounded batch',
                                               'previous_pr': previous})
                    continue
                report['candidate'] = candidate
                break
            except (ValueError, UnicodeError) as exc:
                report['findings'].append({'path': relative, 'status': 'hold', 'reason': str(exc)})
        if report.get('budget_exhausted'):
            break
    return report


def write_candidate(root, report, base_sha, ticket):
    if not re.fullmatch(r'[A-Z][A-Z0-9]+-[0-9]+', ticket):
        raise ValueError('invalid packet key')
    if not re.fullmatch(r'[0-9a-f]{40}', base_sha):
        raise ValueError('invalid base SHA')
    candidate = report['candidate']
    mapping = candidate['url_map']
    if not mapping or not all(eligible_mapping(a, b) for a, b in mapping.items()):
        raise ValueError('mapping outside initial migration scope')
    changes = prepare_mirrors(root, candidate['path'], mapping)
    paths = list(changes)
    packet = {
        'schema_version': 1, 'jira_key': ticket, 'policy_action': 'link-refresh', 'tier_hint': 'C',
        'tier_reasons': ['URL-only draft generated deterministically; semantic equivalence is unverified until independent review and human C approval.',
                         'One non-regulatory logical document and ko/en/ja mirrors; exact Google docs host migration only.',
                         'writer identifies the OpenAI-authored generator/template, not a runtime LLM call. Conservative generated_by_llm=true; never eligible for A. Refs #271.'],
        'target_path': paths[0], 'changed_paths': paths, 'claim_ledger': [],
        'generated_by_llm': True,
        'writer': {'model': 'gpt-6-authored-link-refresh-tool-v1', 'provider': 'openai'},
        'link_refresh': {'url_map': mapping, 'changed_paths_count': len(paths),
                         'manifest_sha256': MANIFEST.compute_manifest(paths, mapping, base_sha)},
    }
    packet_path = root / f'.editorial/packets/{ticket}.json'
    if packet_path.exists():
        raise ValueError('packet already exists; refusing overwrite')
    raw = (json.dumps(packet, ensure_ascii=False, indent=2) + '\n').encode()
    validate_packet(raw, packet_path)
    # No mutation before all three mirrors and the packet have validated.
    for name, content in changes.items():
        (root / name).write_bytes(content)
    packet_path.write_bytes(raw)
    report['written_paths'] = paths + [packet_path.relative_to(root).as_posix()]
    report['packet_sha256'] = hashlib.sha256(raw).hexdigest()


def gh(*args):
    return subprocess.check_output(['gh', *args], cwd=ROOT, text=True).strip()


def has_active_pr(repo):
    pulls = json.loads(gh('pr', 'list', '--repo', repo, '--state', 'open', '--limit', '100', '--json', 'headRefName,url'))
    if len(pulls) >= 100:
        raise ValueError('open PR listing reached limit; cannot establish absence of duplicates')
    return next((p['url'] for p in pulls if p['headRefName'].startswith('docs/link-refresh-')), None)


def candidate_branch(candidate):
    fingerprint = hashlib.sha256(json.dumps(candidate, sort_keys=True).encode()).hexdigest()[:12]
    return f'docs/link-refresh-auto-{fingerprint}'


def previous_candidate_pr(repo, candidate):
    pulls = json.loads(gh('pr', 'list', '--repo', repo, '--state', 'all', '--head', candidate_branch(candidate), '--json', 'url,state'))
    return pulls[0]['url'] if pulls else None


def publish(report, repo):
    """Create at most one new draft; never update an existing human-reviewed head."""
    candidate = report['candidate']
    branch = candidate_branch(candidate)
    fingerprint = branch.rsplit('-', 1)[1]
    previous = previous_candidate_pr(repo, candidate)
    if previous:
        report['skipped'] = 'candidate already proposed (open/closed/merged); no automatic retry'
        report['previous_pr'] = previous
        return
    ticket = f'LINKREFRESH-{int(fingerprint, 16)}'
    write_candidate(ROOT, report, report['base_sha'], ticket)
    # Verify the checkout is still based on the PR base; no force pushes or rebases.
    git('switch', '-c', branch)
    git('add', '--', *report['written_paths'])
    git('-c', 'user.name=cloudpick-link-refresh[bot]', '-c', 'user.email=cloudpick-link-refresh[bot]@users.noreply.github.com',
        'commit', '-m', 'docs: prepare URL-only link refresh (refs #271)')
    git('push', '-u', 'origin', branch)
    body = ('Refs #271. One logical non-regulatory document and ko/en/ja mirrors.\n\n'
            'Generated deterministically from the trusted default-branch tool. Only the exact Google docs host migration is eligible; '
            'HTTP success and unchanged path/query are candidate signals, not semantic approval. '
            'Unknown mappings and fetch failures remain unverified in the workflow artifact.\n\n'
            'Full-file guards and packet validation passed locally. The PR must independently pass editorial-review, '
            'redirect re-fetch, build and link checks. All link-refresh remains C. '
            'A human must inspect meaning, edition and soft-404 before confirming; no automatic merge is configured.\n\n'
            f'Packet: `.editorial/packets/{ticket}.json`\n\n'
            f'Human confirmation command (after review):\n```text\n/approve {report["packet_sha256"]}\n```\n\n'
            'If CI awaits workflow approval because GITHUB_TOKEN created this PR, a user with write access must approve the workflow runs. '
            'An optional LINK_REFRESH_PR_TOKEN can enable unattended CI; never use the C approval identity to auto-approve.\n')
    with tempfile.TemporaryDirectory() as folder:
        body_file = Path(folder) / 'body.md'
        body_file.write_text(body)
        report['pr_url'] = gh('pr', 'create', '--repo', repo, '--base', 'master', '--head', branch, '--draft',
                              '--title', 'docs: prepare Google documentation link refresh', '--body-file', str(body_file))
    gh('api', f'repos/{repo}/issues/271/comments', '-f', f'body=Link-refresh draft: {report["pr_url"]}. C human confirmation and merge remain pending.')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', help='optional logical path, e.g. compute/containers.md')
    parser.add_argument('--write', action='store_true', help='prepare local changes; never commits, pushes, approves or merges')
    parser.add_argument('--publish', action='store_true', help='create one draft PR; requires GH_REPO/GH_TOKEN and clean default-branch checkout')
    parser.add_argument('--ticket', default='LINKREFRESH-271')
    parser.add_argument('--report', required=True)
    args = parser.parse_args(argv)
    if args.write and args.publish:
        parser.error('--write and --publish are mutually exclusive')
    if git('status', '--porcelain'):
        raise ValueError('working tree must be clean')
    base_sha = git('rev-parse', 'HEAD')
    repo = os.environ.get('GH_REPO', '')
    if args.publish:
        if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', repo):
            raise ValueError('GH_REPO must identify the repository')
        if not os.environ.get('GH_TOKEN'):
            raise ValueError('publishing requires GH_TOKEN')
        if git('branch', '--show-current') != 'master' or base_sha != git('rev-parse', 'origin/master'):
            raise ValueError('publishing requires a clean current master checkout')
        active = has_active_pr(repo)
        if active:
            Path(args.report).write_text(json.dumps({'status': 'advisory', 'skipped': 'existing link-refresh PR', 'pr_url': active}) + '\n')
            return
    report = scan(ROOT, args.target, previous_pr=(lambda candidate: previous_candidate_pr(repo, candidate)) if args.publish else None)
    report['base_sha'] = base_sha
    if args.write and report['candidate']:
        write_candidate(ROOT, report, base_sha, args.ticket)
    try:
        if args.publish and report['candidate']:
            publish(report, repo)
    finally:
        Path(args.report).write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'checked_urls': report['checked_urls'], 'candidate': bool(report['candidate']), 'written': bool(report.get('written_paths'))}))


if __name__ == '__main__':
    main()
