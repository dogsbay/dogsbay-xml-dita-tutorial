#!/usr/bin/env python3
"""Rebuild the internal tutorial sequence and synchronize its lesson excerpts.

Run with --docs PATH. Saves the old refs and docs under --backup before edits.
Use --publish-refs after reviewing the generated commit manifest.
"""
import argparse
import difflib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def git(*args, data=None, env=None):
    return subprocess.check_output(['git', '-C', str(ROOT), *args], input=data, env=env)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--docs', type=Path, required=True)
    ap.add_argument('--backup', type=Path, required=True)
    ap.add_argument('--publish-refs', action='store_true')
    args = ap.parse_args()
    args.backup.mkdir(parents=True, exist_ok=True)
    saved = args.backup / 'refs.json'
    if not saved.exists():
        refs = dict(line.split() for line in git('for-each-ref', '--format=%(refname:short) %(objectname)', 'refs/heads/tutorial/').decode().splitlines())
        saved.write_text(json.dumps(refs, indent=2))
        git('bundle', 'create', str(args.backup / 'history.bundle'), '--all')
        shutil.copytree(args.docs / 'content', args.backup / 'content')
    refs = json.loads(saved.read_text())
    old = sorted(refs)
    assert len(old) == 26
    # Keep map structure as its own lesson. Split the old map/build lesson.
    sequence = [(0, 'setup'), (1, 'concept'), (None, 'first-map'), (None, 'first-build')]
    sequence += [(i, old[i].split('-', 1)[1]) for i in range(2, 7)]
    sequence += [(i, old[i].split('-', 1)[1]) for i in range(8, 26)]
    names = [f'tutorial/{i:02d}-{slug}' for i, (_, slug) in enumerate(sequence)]
    renumber = {o: n for n, (o, _) in enumerate(sequence) if o is not None}
    renumber[7] = 2
    replacements = {old[o]: names[n] for o, n in renumber.items()}

    def rename(text):
        text = re.sub(r'tutorial/\d{2}-[a-z-]+', lambda m: replacements.get(m[0], m[0]), text)
        text = re.sub(r'(?i)\bstage ([0-9]{2})\b', lambda m: m[0][:-2] + f'{renumber.get(int(m[1]), int(m[1])):02d}', text)
        return text.replace('26 stages', '27 stages').replace('all 26', 'all 27')

    def snapshot(i):
        ref = refs[old[i]]
        result = {}
        for line in git('ls-tree', '-r', ref).decode().splitlines():
            meta, path = line.split('\t')
            mode, _, oid = meta.split()
            result[path] = (mode, git('cat-file', 'blob', oid))
        return result

    trees = []
    commits = []
    for n, (o, slug) in enumerate(sequence):
        files = snapshot(1 if o is None else o)
        def put(path, value):
            files[path] = (files.get(path, ('100644', b''))[0], value.encode() if isinstance(value, str) else value)
        if 2 <= n <= 8:
            paths = sorted(p for p in files if p.startswith('topics/') and p.endswith('.dita'))
            body = '\n'.join(f'  <topicref href="{p}"/>' for p in paths)
            put('audacity-guide.ditamap', '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE map PUBLIC "-//OASIS//DTD DITA Map//EN" "map.dtd">\n\n<map>\n  <title>Audio user guide</title>\n' + body + '\n</map>\n')
            config = snapshot(7)['.dogsbay/config.xml'][1].decode()
            if n == 2:
                config = re.sub(r'  <default-deliverable[^\n]+\n', '', config)
            put('.dogsbay/config.xml', config)
            if n >= 3:
                put('project.json', snapshot(7)['project.json'][1])
        if o is not None and o >= 17:
            path = 'topics/effects-reference.dita'
            source = files[path][1].decode()
            nested = re.search(r'  <reference id="effect-presets">[\s\S]*?  </reference>\n', source)
            assert nested
            child = '\n'.join(line[2:] for line in nested[0].rstrip().splitlines()) + '\n'
            put('topics/effect-presets.dita', '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE reference PUBLIC "-//OASIS//DTD DITA Reference//EN" "reference.dtd">\n\n' + child)
            source = source.replace(nested[0], '')
            source = re.sub(r'<!-- Nested topics:[\s\S]*?-->\n', '', source)
            put(path, source)
            for path in ('audacity-guide.ditamap', 'podcaster-guide.ditamap', 'audacity-book.ditamap'):
                if path not in files:
                    continue
                source = files[path][1].decode().replace(' chunk="by-topic"', '')
                source = re.sub(r'^.*<!-- One file, two topics:.*\n', '', source, flags=re.M)
                source = re.sub(r'^(\s*)(<(topicref|appendix) href="topics/effects-reference.dita"[^\n]+)', lambda m: m[0] + '\n' + m[1] + '<' + m[3] + ' href="topics/effect-presets.dita"/>', source, flags=re.M)
                put(path, source)
            demo = '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE reference PUBLIC "-//OASIS//DTD DITA Reference//EN" "reference.dtd">\n<reference id="chunk-parent">\n  <title>Chunking demonstration</title>\n  <shortdesc>Compare a combined page with separate pages for nested topics.</shortdesc>\n  <prolog><author>The tutorial team</author><metadata><keywords><keyword>chunking</keyword></keywords></metadata></prolog>\n  <refbody><section><p>The parent and child share one source file.</p></section></refbody>\n  <reference id="chunk-child">\n    <title>Nested topic</title>\n    <shortdesc>The child can be published on its own page.</shortdesc>\n    <prolog><author>The tutorial team</author><metadata><keywords><keyword>chunking</keyword></keywords></metadata></prolog>\n    <refbody><section><p>Check the generated parent and child links.</p></section></refbody>\n  </reference>\n</reference>\n'
            put('examples/chunking/topics/nested.dita', demo)
            for variant, attr in [('split', ' chunk="by-topic"'), ('combined', '')]:
                put(f'examples/chunking/{variant}.ditamap', '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE map PUBLIC "-//OASIS//DTD DITA Map//EN" "map.dtd">\n<map>\n  <title>Chunking demonstration</title>\n  <topicref href="topics/nested.dita"' + attr + '/>\n</map>\n')
        for path, (mode, content) in list(files.items()):
            if path.endswith(('.md', '.sh')):
                put(path, rename(content.decode()))
        table = '\n'.join(f'| `{name}` | {name.split("-", 1)[1].replace("-", " ")} |' for name in names)
        put('README.md', '# DITA tutorial\n\nBuild a guide through 27 stages. Maps begin at stage 02; HTML publication begins at stage 03.\n\n'
            + f'You are on stage {n:02d}: {slug.replace("-", " ")}.\n\n## Stages\n\n| Branch | Lesson |\n|---|---|\n' + table
            + '\n\n## Verification\n\nRun `scripts/check-stage.sh` from the project root. From stage 03, the gate builds the deliverables in `project.json`.\n'
            + 'Run `python3 scripts/check-output-links.py <output-directory>` after publishing HTML. Source health and generated output checks report separate results.\n'
            + '\nThe chunking experiment under `examples/chunking/` is available from stage 18. Build its maps separately; they are not release deliverables.\n'
            + '\nTopic text is adapted from the Audacity Manual. See LICENSE and NOTICE for licensing and attribution.\n')
        put('scripts/check-output-links.py', (ROOT / 'scripts/check-output-links.py').read_bytes())
        trees.append(files)
        with tempfile.TemporaryDirectory(prefix='dita-index-') as tmp:
            env = {**os.environ, 'GIT_INDEX_FILE': tmp + '/index'}
            git('read-tree', '--empty', env=env)
            entries = []
            for path, (mode, content) in sorted(files.items()):
                oid = git('hash-object', '-w', '--stdin', data=content).decode().strip()
                entries.append(f'{mode} {oid}\t{path}\n')
            git('update-index', '--index-info', data=''.join(entries).encode(), env=env)
            tree = git('write-tree', env=env).decode().strip()
            parent = ['-p', commits[-1]] if commits else []
            commits.append(git('commit-tree', tree, *parent, '-m', f'Stage {n:02d}: {slug.replace("-", " ")}').decode().strip())
    manifest = dict(zip(names, commits))
    (args.backup / 'new-refs.json').write_text(json.dumps(manifest, indent=2))
    for name, commit in manifest.items():
        git('update-ref', name.replace('tutorial/', 'refs/heads/redesign/'), commit)
    print(f'Prepared {len(commits)} commits; manifest: {args.backup / "new-refs.json"}', flush=True)

    pages = sorted((args.backup / 'content').glob('part-*/stage-*.md'))
    old_pages = {int(p.name[6:8]): p for p in pages}
    paths = {}
    for n, (o, slug) in enumerate(sequence):
        folder = 'part-1-topics' if n <= 8 else old_pages[o].parent.name
        paths[n] = f'{folder}/stage-{n:02d}-{slug}.md'
    routes = {str(p.relative_to(args.backup / 'content')).removesuffix('.md'): paths[renumber[o]].removesuffix('.md') for o, p in old_pages.items()}

    def docrename(text):
        text = rename(text)
        text = re.sub(r'part-[\w-]+/stage-\d{2}-[\w-]+', lambda m: routes.get(m[0], m[0]), text)
        # Range endpoints and numeric link labels carry no branch slug.
        text = re.sub(r'(?i)\bstages (\d{2}) to (\d{2})', lambda m: 'stages ' + f'{renumber[int(m[1])]:02d} to {renumber[int(m[2])]:02d}', text)
        text = re.sub(r'\[(\d{2})\](?=\(/part-)', lambda m: '[' + f'{renumber[int(m[1])]:02d}' + ']', text)
        return text

    for p in (args.backup / 'content').rglob('*'):
        if p.is_file() and p.suffix in ('.md', '.yml') and not re.match(r'stage-\d', p.name):
            dest = args.docs / 'content' / p.relative_to(args.backup / 'content')
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(docrename(p.read_text()))
    # These files are all backed up above; destinations can reuse old numbers.
    for p in (args.docs / 'content').glob('part-*/stage-*.md'):
        p.unlink()

    from importlib.machinery import SourceFileLoader
    checker = SourceFileLoader('excerpts', str(ROOT / 'scripts/check-excerpts.py')).load_module()
    for n, (o, slug) in enumerate(sequence):
        if o is None:
            text = new_lesson(n, paths)
        else:
            text = docrename(old_pages[o].read_text())
            # Replace exact excerpts from the new source, retaining fence metadata.
            lines = text.splitlines()
            for line, lang, path, body in reversed(list(checker.blocks(text))):
                if path not in trees[n]:
                    continue
                current = trees[n][path][1].decode()
                if lang == 'diff':
                    previous = trees[n-1].get(path, ('', b''))[1].decode() if n else ''
                    current = ''.join(difflib.unified_diff(previous.splitlines(True), current.splitlines(True), fromfile='a/'+path, tofile='b/'+path))
                    if not current:
                        # A retained file is shown as a full listing, never an empty diff.
                        current = trees[n][path][1].decode()
                        lines[line-1] = lines[line-1].replace('```diff', '```text')
                indent = re.match(r' *', lines[line-1])[0]
                lines[line:line+len(body)] = [indent + x for x in current.rstrip('\n').splitlines()]
            text = '\n'.join(lines) + '\n'
        # Historical diagnostics include counts and filenames from the old sequence.
        if '== project-health' in text or '== validate-project' in text:
            at = text.find('\n## ')
            text = text[:at] + '\n\nRecorded diagnostic examples below come from earlier runs. File counts, paths, and stage numbers can differ. Run the gate for your current checkout.\n' + text[at:]
        if 4 <= n <= 8:
            extra = '\n## Publish your changes\n\nAdd the lesson\'s topics to `audacity-guide.ditamap`, then rebuild the guide. The complete map at this checkpoint is:\n\n```xml title="audacity-guide.ditamap"\n' + trees[n]['audacity-guide.ditamap'][1].decode() + '```\n\n```bash\ndita --project=project.json --output=out\npython3 scripts/check-output-links.py out\n```\n'
            text = text.replace('\n## What you learned', extra + '\n## What you learned')
        dest = args.docs / 'content' / paths[n]
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(text)
    (args.backup / 'mapping.json').write_text(json.dumps({'renumber': renumber, 'paths': paths}, indent=2))
    editor = SourceFileLoader('redesign_docs', str(ROOT / 'scripts/redesign-docs.py')).load_module()
    editor.finish(args.docs, paths, names, trees)
    if args.publish_refs:
        commands = ['start']
        for name in old:
            if name not in manifest:
                commands.append(f'delete refs/heads/{name} {refs[name]}')
        for name, commit in manifest.items():
            commands.append(f'update refs/heads/{name} {commit}')
        commands.append(f'update refs/tags/tutorial/final {commits[-1]}')
        commands += ['prepare', 'commit']
        git('update-ref', '--stdin', data=('\n'.join(commands)+'\n').encode())
        print('Published the redesigned local tutorial refs.', flush=True)


def new_lesson(n, paths):
    if n == 2:
        return '''---
title: "Stage 02: Create the first map"
description: Add your first topic to a DITA map and select the map as the project root.
type: tutorial
---

# Stage 02: Create the first map

A map selects the topics in a publication and their navigation order. Create
one now so that later lessons can add topics to a working guide.

**You need:** stage 01 complete. **Time:** about 10 minutes.

## Create the guide map

Save this file as `audacity-guide.ditamap` in the project root:

```xml title="audacity-guide.ditamap"
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE map PUBLIC "-//OASIS//DTD DITA Map//EN" "map.dtd">

<map>
  <title>Audio user guide</title>
  <topicref href="topics/what-is-audacity.dita"/>
</map>
```

The `href` is relative to the map. The map title names the publication;
the topic title supplies its navigation label. Add a topicref when you add
a topic to the guide. Later lessons introduce hierarchy and generated links.

## Select and validate the map

Set the default root map to `audacity-guide.ditamap` in the project settings.
Validate the document in the editor, or run from the project root:

```bash
dogsbay-xml validate audacity-guide.ditamap
scripts/check-stage.sh
```

The gate checks the source. Stage 03 adds a deliverable so the gate can also
publish HTML. Try an incorrect topic filename, check the diagnostic, then
restore the filename and validate again.

## Next lesson

Continue with [Stage 03: First build](/part-1-topics/stage-03-first-build).
'''
    return '''---
title: "Stage 03: Publish the first guide"
description: Define an HTML deliverable, build the guide with DITA-OT, and inspect its generated pages.
type: tutorial
---

# Stage 03: Publish the first guide

Publish the map from stage 02. Keep this build throughout the course so you
can inspect every topic, link, and navigation change as you make it.

**You need:** stage 02 complete and DITA-OT installed. **Time:** about 10 minutes.

## Define the deliverable

Create `project.json` in the project root:

```json
{
  "deliverables": [{
    "name": "full",
    "context": {"id": "full", "input": "audacity-guide.ditamap"},
    "output": "out/full",
    "publication": {"transtype": "html5", "params": [{"name": "nav-toc", "value": "full"}]}
  }]
}
```

The context identifies the root map. The publication selects the HTML5
transformation and requests navigation on each page. The output is relative
to the build's output base directory. Select `full` as the default deliverable
in the editor's project settings.

## Build and inspect

From the project root, run:

```bash
scripts/check-stage.sh
dita --project=project.json --output=out
python3 scripts/check-output-links.py out
```

The gate builds into a temporary directory. The second command keeps a local
copy under `out/out/full/`. Open its `index.html`, follow the topic link, and
check the heading, short description, list, and section.

Change the topic title, rebuild, and refresh the browser. Check both the page
heading and navigation label. Restore the title when you finish the exercise.

If a command fails, check the working directory, the map-relative paths, and
the configured DITA-OT installation. A successful source check does not ensure
that generated links work; inspect the output-link check separately.

## Next lesson

Continue with [Stage 04: Tasks and references](/part-1-topics/stage-04-task-and-reference).
'''


if __name__ == '__main__':
    main()
