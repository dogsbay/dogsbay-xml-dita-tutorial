#!/usr/bin/env python3
"""Compare titled lesson listings and diff hunks with their Git stage refs."""
import argparse
import re
import subprocess
from pathlib import Path


def git(repo, *args):
    result = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)
    if result.returncode:
        raise ValueError(result.stderr.strip())
    return result.stdout


def blocks(text):
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        match = re.match(r'^( *)(`{3,}|~{3,})(\w*)\s*(.*)$', lines[i])
        if not match:
            i += 1
            continue
        indent, fence, lang, meta = match.groups()
        title = re.search(r'\btitle="([^"]+)"', meta)
        start = i + 1
        body = []
        i += 1
        while i < len(lines) and not re.match(r'^\s*' + re.escape(fence[0]) + '{' + str(len(fence)) + r',}\s*$', lines[i]):
            body.append(lines[i][len(indent):] if lines[i].startswith(indent) else lines[i])
            i += 1
        if i == len(lines):
            raise ValueError(f"unclosed fence at line {start}")
        if title:
            yield start, lang, title.group(1), body
        i += 1


def check_diff(body, before, after):
    """Check both sides of every hunk, including offsets and line counts."""
    old, new = before.splitlines(), after.splitlines()
    i = 0
    count = 0
    while i < len(body):
        match = re.match(r'^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@', body[i])
        if not match:
            if body[i].startswith(("--- ", "+++ ", "diff ", "index ")) or not body[i]:
                i += 1
                continue
            raise ValueError("unrecognized diff content: " + body[i])
        a, an, b, bn = (int(v) if v is not None else 1 for v in match.groups())
        left, right = [], []
        i += 1
        while i < len(body) and not body[i].startswith('@@ '):
            line = body[i]
            if line.startswith('\\ No newline'):
                i += 1
                continue
            if not line or line[0] not in ' +-':
                raise ValueError("invalid hunk line: " + line)
            if line[0] in ' -':
                left.append(line[1:])
            if line[0] in ' +':
                right.append(line[1:])
            i += 1
        if len(left) != an or len(right) != bn:
            raise ValueError(f"incorrect hunk counts at -{a} +{b}")
        if left != old[max(a - 1, 0):max(a - 1, 0) + an]:
            raise ValueError(f"old hunk differs from preceding stage at line {a}")
        if right != new[max(b - 1, 0):max(b - 1, 0) + bn]:
            raise ValueError(f"new hunk differs from stage at line {b}")
        count += 1
    if not count:
        raise ValueError("diff has no hunks")


def main():
    repo = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('docs', nargs='?', type=Path, default=repo.parent / 'dogsbay-xml-dita-tutorial-docs')
    parser.add_argument('--repo', type=Path, default=repo)
    parser.add_argument('--ref-prefix', default='tutorial/', help='Use origin/tutorial/ in a fresh clone')
    args = parser.parse_args()
    pages = sorted((args.docs / 'content').glob('part-*/stage-*.md'))
    if not pages:
        parser.error('no stage pages found')
    refs = {}
    for page in pages:
        number, slug = re.match(r'stage-(\d+)-(.+)\.md$', page.name).groups()
        refs[int(number)] = args.ref_prefix + number + '-' + slug
    if sorted(refs) != list(range(len(pages))):
        parser.error('stage numbers must be unique and contiguous, starting at 00')
    cache = {}
    def source(ref, name):
        key = (ref, name)
        if key not in cache:
            cache[key] = git(args.repo, 'show', f'{ref}:{name}')
        return cache[key]
    failures, checked = [], 0
    targets = [(p, int(p.name[6:8])) for p in pages]
    reference = args.docs / 'content/reference/the-gate.md'
    if not reference.exists():
        parser.error('missing content/reference/the-gate.md')
    targets.append((reference, max(refs)))
    for page, stage in targets:
        try:
            git(args.repo, 'rev-parse', '--verify', refs[stage] + '^{commit}')
            for line, lang, name, body in blocks(page.read_text()):
                checked += 1
                try:
                    current = source(refs[stage], name)
                    if lang == 'diff':
                        if stage == 0:
                            raise ValueError('stage 00 cannot have a preceding-stage diff')
                        check_diff(body, source(refs[stage - 1], name), current)
                    elif '\n'.join(body).strip('\n') != current.strip('\n'):
                        raise ValueError('file listing differs from stage')
                except ValueError as error:
                    failures.append(f'{page}:{line}: {name}: {error}')
        except ValueError as error:
            failures.append(f'{page}: {error}')
    for failure in failures:
        print(failure)
    print(f'{checked} excerpts checked; {len(failures)} failures')
    return 1 if failures or not checked else 0


if __name__ == '__main__':
    raise SystemExit(main())
