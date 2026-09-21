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
