"""Editorial follow-up for the tutorial history migration."""
import re


def finish(docs, paths, names, trees):
    content = docs / 'content'
    def write(path, text):
        (content / path).write_text(text)
    def source(n, path, lang='xml'):
        return f'```{lang} title="{path}"\n' + trees[n][path][1].decode().rstrip() + '\n```\n'
    def link(n):
        return '/' + paths[n].removesuffix('.md')
    for p in content.rglob('*.md'):
        text = p.read_text().replace('/start-here/first-build', link(3))
        text = re.sub(r'Compare (\d{2}) to (\d{2}) on GitHub', 'Compare this stage with its predecessor on GitHub', text)
        text = re.sub(r'compare \d{2} to \d{2}', 'compare these stages', text)
        p.write_text(text)
    (content / 'start-here/first-build.md').unlink(missing_ok=True)
    nav = (content / 'nav.yml').read_text()
    nav = nav.replace('    - Publish your first topic: start-here/first-build.md\n',
        f'    - "Stage 02: First map": {paths[2]}\n    - "Stage 03: First build": {paths[3]}\n')
    nav = nav.replace(f'    - "Stage 02: The guide map": {paths[2]}\n', '')
    write('nav.yml', nav)
    for path in ['index.md', 'reference/branches.md']:
        text = (content / path).read_text()
        rows = re.findall(r'^\| .*`tutorial/\d{2}-[^\n]+$', text, re.M)
        if rows:
            new_rows = [r for r in rows if '`tutorial/02-first-map`' not in r]
            if path == 'index.md':
                new_rows += [f'| [02]({link(2)}) | `tutorial/02-first-map` | A one-topic guide map | `<map>`, `<topicref>`, relative paths, project root |', f'| [03]({link(3)}) | `tutorial/03-first-build` | The first HTML guide | `project.json`, DITA-OT, output inspection |']
            else:
                new_rows += [f'| `tutorial/02-first-map` | The first map | [Stage 02]({link(2)}) |', f'| `tutorial/03-first-build` | The first HTML deliverable | [Stage 03]({link(3)}) |']
            new_rows.sort(key=lambda r: int(re.search(r'tutorial/(\d+)', r)[1]))
            text = text.replace('\n'.join(rows), '\n'.join(new_rows))
        text = text.replace('one-topic HTML guide immediately after stage 01', 'one-topic HTML guide in stages 02 and 03')
        write(path, text)
    write('start-here/learning-path.md', '''---
title: Choose a learning path
description: Build your first guide in stages 00 to 03, then choose the core course or optional DITA modules.
type: explanation
---

# Choose a learning path

Start with a topic, a map, and a working HTML build. Keep publishing as you
learn: every authoring lesson after stage 03 adds to a buildable guide.

## Core course

| Module | Lessons | Result |
|---|---|---|
| Plan and publish | Plan your topics, stages 00 to 03 | A content plan, concept topic, map, and HTML output |
| Write topics | Stages 04 to 07 | Tasks, references, semantic markup, and working links |
| Organize and reuse | Stages 09 to 11 | Map hierarchy, keys, and shared content |
| Publish variants | Stages 14 and 15 | Audience and platform variants with controlled values |
| Check and complete | Stage 25, accessibility review, capstone, stage 26 | Reviewed output and a completed project |

Stage 11 introduces pull reuse with `conref` and `conkeyref`. Its range and
push examples are optional. Use the stage 13 checkpoint before continuing
with stage 14 if you skip those examples.

## Continue across a skipped stage

Reference branches form one cumulative sequence. Skipping a lesson means
using its completed source before starting the next lesson. Your authored
work stays in its existing directory.

| Next core lesson | Starting checkpoint |
|---|---|
| Stage 09 after skipping figures | `origin/tutorial/08-figures` |
| Stage 14 after skipping glossary and metadata | `origin/tutorial/13-metadata-and-index` |
| Stage 25 after skipping specialized modules | `origin/tutorial/24-drafts-and-localization` |

From the tutorial clone, create a practice branch and worktree, for example:

```bash
git worktree add -b practice-conditions ../audacity-conditions origin/tutorial/13-metadata-and-index
cd ../audacity-conditions
scripts/check-stage.sh
```

Use a new branch and directory name if either already exists. The checkpoint
includes the skipped examples so later diffs apply cleanly.

## Optional modules

| Module | Lessons | Starting checkpoint |
|---|---|---|
| Figures and equations | Stage 08 | `origin/tutorial/07-links` |
| Glossary, metadata, and index | Stages 12 and 13 | `origin/tutorial/11-reuse` |
| Branch filtering, key scopes, and chunking | Stages 16 to 18 | `origin/tutorial/15-subject-scheme` |
| PDF books | Stage 19 | `origin/tutorial/18-chunking-and-output` |
| Troubleshooting and hazards | Stages 20 and 21 | `origin/tutorial/19-bookmap` |
| Software documentation | Stage 22 | `origin/tutorial/21-hazards-and-safety` |
| Learning and Training | Stage 23 | `origin/tutorial/22-software-domains` |
| Review and translation | Stage 24 | `origin/tutorial/23-learning` |

To author every example, follow stages 00 to 26 in order. Complete the
[practice exercises](/practice/exercises) after each core module and the
[capstone](/practice/capstone) before tagging your finished guide.
''')
    text = '''---
title: "Stage 18: Chunking and output"
description: Combine output pages, test splitting in a separate example, and control publication names and visibility.
type: tutorial
---

# Stage 18: Chunking and output

Control how topics become pages. Combine topics with `chunk="to-content"`,
test `chunk="by-topic"` with an isolated example, and assign an output name
with `copy-to`.

**Optional module.** See [Choose a learning path](/start-here/learning-path).
**You need:** stage 17 complete. **Time:** about 35 minutes.

## Add the production topics

Create the following files. The effects reference and presets use separate
source files. Each gets an explicit topicref in the production maps.
The effect-order concept supports the reusable cleanup branch. The guide
information topic is published in print output.

'''
    for p in ['topics/effects-reference.dita', 'topics/effect-presets.dita', 'topics/effect-order.dita', 'topics/about-this-guide.dita']:
        text += source(18, p) + '\n'
    text += '''## Update the production maps

Apply the map changes below. `to-content` combines the introductory topics.
`print="printonly"` restricts the guide information topic to print output;
`toc="no"` and `search="no"` control navigation and search where supported.

The `cleanup` topicset names a reusable branch. The podcaster map includes
that branch with `topicsetref`. The beginner map uses `copy-to` to give the
audio-formats topic a different output filename.

'''
    import difflib
    for p in ['audacity-guide.ditamap', 'beginner-guide.ditamap', 'podcaster-guide.ditamap', 'topics/podcast-production-workflow.dita']:
        diff = ''.join(difflib.unified_diff(trees[17][p][1].decode().splitlines(True), trees[18][p][1].decode().splitlines(True), fromfile='a/'+p, tofile='b/'+p))
        text += f'```diff title="{p}"\n{diff}```\n\n'
    text += '''## Compare combined and split pages

Create these files under `examples/chunking/`. This example has its own maps
and is excluded from the deliverables in `project.json`.

'''
    for p in ['examples/chunking/topics/nested.dita', 'examples/chunking/combined.ditamap', 'examples/chunking/split.ditamap']:
        text += source(18, p) + '\n'
    text += '''Run both builds from the project root:

```bash
dita --input=examples/chunking/combined.ditamap --format=html5 --output=out/chunk-combined --nav-toc=full
dita --input=examples/chunking/split.ditamap --format=html5 --output=out/chunk-split --nav-toc=full
python3 scripts/check-output-links.py out/chunk-combined
python3 scripts/check-output-links.py out/chunk-split
```

Open each output's `index.html`. The combined version keeps the parent and
child on one page. The split version should create a page for each topic.
Follow the parent, child, and navigation links. Generated filenames can vary.

**Warning:** The previous effects example produced broken generated links
with DITA-OT 4.3.5. Nested topics with `chunk="by-topic"` are valid DITA.
The separate example preserves that lesson but does not guarantee that a
processor will handle every chunking case correctly. Record the results for
your version and transformation, and check generated links before publishing.

## Check the guide

Run `scripts/check-stage.sh`, build the production deliverables, and run the
output-link checker. Record remaining [known output issues](/reference/known-output-issues)
separately from the chunking experiment.

Check that the effects and presets pages have stable filenames, the merged
introduction links resolve, and the beginner formats page uses its alternate
name. `outputclass="compact"` on the effects table supplies a CSS class; a
stylesheet must define its visual effect.

## What you learned

- `to-content` combines topics into an output document.
- `by-topic` splits nested topics; inspect generated links as well as pages.
- `copy-to` assigns an alternate output filename in a map.
- Print, navigation, and search attributes control different output features.
- `topicset` and `topicsetref` reuse map branches.
'''
    write(paths[18], text)
    write(paths[26], '''---
title: "Stage 26: Final"
description: Verify every deliverable and generated link, complete the capstone, and tag your finished guide.
type: tutorial
---

# Stage 26: Final

Complete the [capstone](/practice/capstone), check the source, and inspect
every deliverable before tagging your work.

**You need:** stage 25 complete. **Time:** about 15 minutes, plus corrections.

## Review the project

`project.json` defines eight deliverables: full, beginner-mac,
beginner-windows, podcaster-linux, review, install-variants, collection,
and book-pdf. The chunking examples have separate maps and are built manually.

The README records the complete branch sequence:

''' + source(26, 'README.md', 'md') + '''
## Validate and publish

Run these commands from the project root:

```bash
scripts/check-stage.sh
dita --project=project.json --output=out
python3 scripts/check-output-links.py out
```

The gate checks source validation, project health, controlled values, house
rules, and publication. The output checker tests local HTML links and assets.
Inspect PDF navigation, accessibility, and layout separately.

Review [known output issues](/reference/known-output-issues). A successful
source gate does not override a failed output check. Resolve release defects
before describing your own guide as ready for publication.

## Tag your result

Commit your lesson changes and confirm that `git status` is clean. After
completing the checks, create a tag for your own result:

```bash
git tag my-tutorial-final
git show --stat my-tutorial-final
```

The supplied reference is `tutorial/26-final`, also tagged `tutorial/final`.
It includes every optional lesson. The tag identifies a checkpoint, not a
claim that every known publishing issue has been resolved.
''')
    # Next links and prerequisites must describe the actual linear sequence.
    for n, path in paths.items():
        p = content / path
        text = p.read_text()
        text = re.sub(r'\n## (?:Where to go next|Next lesson)[\s\S]*$', '', text)
        text = text.replace('before Part 2', 'before the next lesson')
        if n == 4:
            text = text.replace('**You need:** stage 01 complete.', '**You need:** stage 03 complete.')
        if n == 9:
            text = text.replace('**You need:** stage 02 complete.', '**You need:** stage 08 complete.')
        if n < 26:
            text += f'\n## Next lesson\n\nContinue with [Stage {n+1:02d}: {names[n+1].split("-", 1)[1].replace("-", " ")}]({link(n+1)}).\n'
            text += '\nFor the core course, use the [learning path](/start-here/learning-path) to skip optional modules.\n'
        if n:
            text += f'\n[Compare this stage with its predecessor](https://github.com/dogsbay/dogsbay-xml-dita-tutorial/compare/{names[n-1]}...{names[n]}).\n'
        p.write_text(text)
    # Update maintainer wording outside lesson content.
    readme = docs / 'README.md'
    text = readme.read_text().replace('Stage filenames and\nbranch names retain their original numbering.', 'The 27 stage branches introduce the first map at stage 02 and the first build at stage 03.')
    readme.write_text(text)
