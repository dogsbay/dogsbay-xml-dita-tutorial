# Tutorial sequence redesign

The internal tutorial now has 27 stages, `tutorial/00-setup` through
`tutorial/26-final`. Each branch points to one commit in a linear history.
`tutorial/final` points to the last commit. The original sequence is retained
in `/tmp/dita-redesign-20260922/history.bundle` for recovery.

## Teaching order

| Previous stage | New stage |
|---|---|
| 00: setup | 00: setup |
| 01: concept | 01: concept |
| 07: first map and build | 02: first map; 03: first build |
| 02 to 06: topic authoring | 04 to 08: topic authoring |
| 08 to 25: remaining lessons | 09 to 26: remaining lessons |

Every stage from 03 has an HTML deliverable. The early authoring stages add
their topics to a simple guide map. Stage 09 introduces hierarchy and
relationship tables. The optional modules use the existing cumulative
checkpoint model; skipping study of a feature still supplies its completed
source before the next dependent lesson.

Stage 18 separates effects and presets into production topics. The nested
topic demonstration lives under `examples/chunking/`, with combined and split
maps that are built independently of `project.json`.

## Verification

All 27 stage gates passed using DogsBay XML and DITA-OT 4.3.5. These checks
cover validation, source health, controlled values where applicable, and all
configured deliverable builds. The new demonstration files produce formatting
warnings but no validation or reference errors.

The final production build contains 177 HTML pages. The output checker reports
12 existing failures: seven glossary links and five sample-download links.
Separating effects and presets removed the eight effects links and one
stylesheet failure from the original output. The isolated split demonstration
reproduces two broken generated links; the lesson explicitly warns about them.

The documentation has 27 lesson pages. The excerpt checker discovers the
numbered sequence and checks 194 quoted files and diffs. All match the new
branches. The source site audit and production site build pass.

## Recovery and publication

The migration replaced local tutorial branch names and moved `tutorial/final`.
It did not push changes to a remote. The old final-stage worktree was clean
and is detached on its original commit, preserving its contents.

The migration scripts are one-time maintenance tools, not learner commands.
Their saved input refs and docs are under `/tmp/dita-redesign-20260922`.
Do not rerun the migration against edited branches or docs without reviewing
the saved inputs and changes made after the migration.
