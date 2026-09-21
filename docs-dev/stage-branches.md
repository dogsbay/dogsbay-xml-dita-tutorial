# The tutorial stage branches

The step-by-step tutorial lives on a chain of branches, `tutorial/00-setup`
through `tutorial/25-final`. Each branch is the previous one plus the commits
for one lesson, so `git diff tutorial/03-inline-and-block tutorial/04-rich-tasks`
is exactly what stage 04 teaches. The plan with the full ladder is
`plans/step-by-step-tutorial.md`.

## Shape

- `tutorial/00-setup` is an **orphan** branch: no history shared with `main`,
  which is the finished, deliberately broken demo project.
- Every stage carries its own `scripts/check-stage.sh` (see `stage-gate.md`),
  a `README.md` whose "You are on" line names the stage, and the licence files.
- Commit messages start with `Stage NN:`.
- Text is written once, correctly; stages add structure. Mistakes are shown in
  the docs by what the gate reports, never committed.
- Before every stage commit: `dogsbay-xml format -i topics/*.dita` (the
  `.dogsbay/config.xml` format style), then the gate.

## Checking the whole ladder

```bash
scripts/check-all-stages.sh            # every stage, each in a temporary worktree
scripts/check-all-stages.sh 04 06      # just those stages
SKIP_BUILD=1 scripts/check-all-stages.sh
```

## Adding a stage

1. `git checkout tutorial/<previous>` then `git checkout -b tutorial/NN-slug`.
2. Add the feature, update the README "You are on" line and the stage table.
3. Format, gate, commit.

## Changing a middle stage

Later stages must be rebased onto the change, in order:

```bash
git rebase --onto tutorial/03-inline-and-block <old-03-sha> tutorial/04-rich-tasks
# ... and so on up the chain, then
scripts/check-all-stages.sh
```

A `scripts/rebase-stages.sh` helper is planned once the ladder is complete.

## Lessons from Part 1 worth keeping

- `<shortcut>` is only valid inside `<uicontrol>` in DITA 1.3; key
  combinations such as Ctrl+A are plain `<uicontrol>` text.
- Inline SVG must use the `svg:` prefix (`<svg:svg xmlns:svg=…>`): the DTD
  declares the SVG elements under that prefix.
- DITA-OT 4.3.5 html5 drops `<mathml>` (a `foreign` specialisation) unless a
  MathML plugin is installed. Stage 06 keeps a `<ph>` text alternative beside
  the MathML inside `<equation-block>`, as the spec allows.
- `xmllint` cannot validate DITA against these DTDs; use `dogsbay-xml`.

## Lessons from Part 2 worth keeping

- `<prolog>` order is fixed: author, source, publisher, copyright, critdates,
  permissions, metadata, resourceid, data. `<resourceid>` and `<data>` sit
  after `<metadata>`, not inside it.
- A `<glossgroup>` is a topic of its own: the metadata policy applies to it as
  well as to the entries it contains, so it needs its own prolog.
- The `keys` command takes the root map, not a directory:
  `dogsbay-xml keys audacity-guide.ditamap`.
- DITA-OT resolves `@conkeyref` only when the key is defined in the root map's
  key space; an undefined key is a build error (DOTJ046E), not a warning.
- Scripted edits: run `dogsbay-xml format -i` *before* matching text in a
  file, not after. The formatter reflows `<menucascade>` and MathML, so a
  string matched against the unformatted file misses on the next stage.

## Lessons from Part 3 worth keeping

- **Root-scope keys in a collection.** A conref push in a warehouse reaches
  its target topic directly, outside any guide's key scope, and that copy of
  the topic resolves its keys in the root scope. The collection map therefore
  defines the keys such content needs (product keys, `common-notes`) at its
  root as well.
- **A bare key is not visible in the parent scope.** In the collection,
  `start-here` is undefined; only `userguide.start-here`,
  `beginner.start-here` and `podcaster.start-here` exist.
- **Every root map needs every key its topics use.** A `<link keyref="install"/>`
  in a shared topic fails the build of any map that does not define `install`
  (DOTX028E). Give the topicref the same `keys` in each map, or keep such links
  in topics that appear in one map only.
- **`chunk="to-content"` on a branch that other content links to by key**
  breaks those links in DITA-OT 4.3.5 (DOTX031E for `term keyref` into a
  chunked glossary). Merge small topics that nothing links into; leave the
  glossary as separate files.
- **`<dita>` composite documents have no prolog on the root**, so the DogsBay
  metadata policy reports them as missing keywords. Nest topics under a real
  topic root instead (a `<reference>` may nest `<reference>`).
- **`project-health` lists unused keys and recommended-metadata warnings only
  alongside some other finding.** On their own the project reports healthy and
  exits 0, so a stage can pass with idle keys and then "fail" for them the
  moment an unrelated error appears. Use every key you define.
- **`<shortcut>`, `svg:` and MathML** are in the Part 1 list; **`<p>` after a
  `<section>`** is invalid in `conbody` (blocks come first, sections last).
- `check-all-stages.sh` needs `pipefail`: the gate's exit code was hidden
  behind `tail` and a failing stage counted as passed until the fix.
