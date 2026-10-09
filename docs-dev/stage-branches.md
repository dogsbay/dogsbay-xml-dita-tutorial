# The tutorial stage branches

The step-by-step tutorial lives on a chain of branches, `tutorial/00-setup`
through `tutorial/26-final`. Each branch is the previous one plus the commits
for one lesson, so `git diff tutorial/05-inline-and-block tutorial/06-rich-tasks`
is exactly what stage 06 teaches.

## Shape

- `tutorial/00-setup` is an **orphan** branch: no history shared with `main`,
  which used to be the deliberately broken agent demo. The demo has moved to
  a repository of its own. `main` is now the finished project: the tree of
  `tutorial/26-final` plus the maintainer files (`scripts/` and `docs-dev/`),
  committed on top of the old history.
- Every stage carries its own `scripts/check-stage.sh` (see `stage-gate.md`),
  a `README.md` whose "You are on" line names the stage, and the licence files.
- Commit messages start with `Stage NN:`.
- Text is written once, correctly; stages add structure. Mistakes are shown in
  the docs by what the gate reports, never committed.
- Before every stage commit: `dogsbay-xml format -i topics/*.dita` (the
  `.dogsbay/config.xml` format style), then the gate.

## Checking the whole ladder

The reader documentation now offers a core course and optional modules.
The redesigned sequence introduces maps at stage 02 and builds at stage 03.
A reader who skips a
module starts the next lesson from its prerequisite reference branch.

```bash
scripts/check-all-stages.sh            # every stage, each in a temporary worktree
scripts/check-all-stages.sh 04 06      # just those stages
SKIP_BUILD=1 scripts/check-all-stages.sh
```

After a successful stage build, the runner checks the generated HTML with
`scripts/check-output-links.py`. `SKIP_BUILD=1` skips that check too. The
checker needs Python 3.9 or later. It reports broken local pages, fragments,
and assets across the output directories. Historical gate success alone
does not guarantee that this additional check passes.

Check quoted documentation after a stage change:

```bash
bash scripts/check-excerpts.sh ../dogsbay-xml-dita-tutorial-docs
python3 -B scripts/test_checks.py
```

Use `--ref-prefix origin/tutorial/` with the excerpt checker when the stage
branches exist only as remote-tracking refs. It compares titled listings and
both sides of diff hunks against the corresponding stages.

## Adding a stage

1. `git checkout tutorial/<previous>` then `git checkout -b tutorial/NN-slug`.
2. Add the feature, update the README "You are on" line and the stage table.
3. Format, gate, commit.

## Changing a middle stage

Later stages must be rebased onto the change, in order:

```bash
git rebase --onto tutorial/05-inline-and-block <old-05-sha> tutorial/06-rich-tasks
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
  MathML plugin is installed. Stage 08 keeps a `<ph>` text alternative beside
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
- **`<dita>` composite documents have no prolog on the root.** The recorded
  metadata checker treats that container as a topic requiring keywords.
  This is a checker limitation; choose nesting only for a parent-child
  relationship. Unrelated topics can use separate files or a composite
  with appropriate validation.
- **`project-health` lists unused keys and recommended-metadata warnings only
  alongside some other finding.** On their own the project reports healthy and
  exits 0, so a stage can pass with idle keys and then "fail" for them the
  moment an unrelated error appears. Use every key you define.
- **`<shortcut>`, `svg:` and MathML** are in the Part 1 list; **`<p>` after a
  `<section>`** is invalid in `conbody` (blocks come first, sections last).
- `check-all-stages.sh` needs `pipefail`: the gate's exit code was hidden
  behind `tail` and a failing stage counted as passed until the fix.

## Lessons from Part 4 worth keeping

- **Bookmap content model.** `<bookmap>` allows only booktitle, bookmeta,
  frontmatter, chapters, parts, appendices, backmatter and reltables at the
  top level. Key definitions, scheme maprefs and resource-only refs go inside
  `<frontmatter>`.
- **A conref'd `<hazardstatement>` needs a placeholder panel**, like the
  `<cmd/>` of a conref'd step: `<messagepanel><typeofhazard/><howtoavoid/></messagepanel>`.
- **`<repsep>` comes first** inside the `<groupseq>` it applies to, before
  the keywords and variables.
- **`<lcTime>` requires `@value`** (an ISO duration such as `PT5M`); a plain
  `<p>` is not allowed in `<lcDuration>`.
- **The editor's built-in catalog has no Learning and Training DTDs.**
  `validate-project` and `project-health` report `learning/*.dita` as
  invalid ("learningAssessment.dtd: No such file"), while DITA-OT and
  `dogsbay-xml validate --catalog <DITA-OT>/catalog-dita.xml` validate them.
  From stage 23 the gate validates `learning/` against the DITA-OT catalog
  and runs `project-health` with an explicit `--include` list that leaves
  out its grammar pass. Worth fixing in the editor: add the L&T DTDs to the
  built-in catalog.
- **`project-health --include` with `schematron`** in the list fails unless
  house rules are configured; from stage 25 the gate runs the rules as a
  separate step.
- **The gate script needs `pipefail`** for the same reason the driver did;
  `cmd | tee` hid validate-project's exit code.

## Lessons from Part 5 worth keeping

- **The formatter re-escapes `&amp;` on every pass.** `dogsbay-xml format -i`
  turns `&amp;` into `&amp;amp;` and `&#x20;` into `&amp;#x20;`, and each
  later stage's format run doubled it again (found at stage 23, corrupted from
  stage 19). Do not put character entities in text: write "and", and let
  whitespace-only elements such as `<repsep>` be empty. Worth fixing in the
  editor. `format --check` on every file before committing catches a file the
  formatter cannot make canonical.
- **Rebasing the chain**: `scripts/rebase-stages.sh <NN> <old-sha>` carries
  every later stage along after an amend and re-gates them. Use
  `git rebase -X ours` by hand when the same line was reformatted on every
  later stage (that is how the entity corruption was undone).
- **House rules and `--include`**: once `.dogsbay/config.xml` names a
  `<default-schematron>`, `project-health` runs the rules by default; the
  gate's explicit include list (needed because of `learning/`) leaves
  `schematron` out and runs it as its own step.
- Resolving review markup is content work, not deletion: the
  `<required-cleanup remap="table">` became the table it asked for, and the
  answered `<draft-comment>` became a `<change-summary>` line.
