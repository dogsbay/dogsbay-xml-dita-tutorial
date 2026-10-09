# Audacity User Guide — a DITA tutorial

A complete user guide for Audacity, written in DITA 1.3 and built step by step
in a 27-stage tutorial. This branch, `main`, is the finished project: the
result of the last stage, and the sample project that DogsBay XML opens from
**File > Open Sample Project**.

The guide is an exercise. Audacity is a real open-source product, but this is
not its documentation.

## Follow the tutorial

- **Written lessons:** <https://dogsbay.ai/dogsbay-xml-dita-tutorial-docs/>
- **Videos:** one for each stage, linked from its lesson.
- **Editor:** the lessons use [DogsBay XML](https://github.com/dogsbay/dogsbay-xml),
  which is free and open source. Any XML or text editor works, with DITA-OT to
  build.

Each stage's finished project is a branch, from `tutorial/00-setup` to
`tutorial/26-final`. Use them to check your work, copy a listing, or start a
stage from the one before it. You don't need Git: on GitHub, browse a branch,
download it as a zip file, or compare two stages. With Git, the difference
between two neighbouring branches is exactly one lesson:

```bash
git diff origin/tutorial/01-concept origin/tutorial/02-first-map
```

Report problems with a lesson as an issue on this repository.

## Stages

| Branch | Lesson |
|---|---|
| `tutorial/00-setup` | setup |
| `tutorial/01-concept` | concept |
| `tutorial/02-first-map` | first map |
| `tutorial/03-first-build` | first build |
| `tutorial/04-task-and-reference` | task and reference |
| `tutorial/05-inline-and-block` | inline and block |
| `tutorial/06-rich-tasks` | rich tasks |
| `tutorial/07-links` | links |
| `tutorial/08-figures` | figures |
| `tutorial/09-map-structure` | map structure |
| `tutorial/10-keys` | keys |
| `tutorial/11-reuse` | reuse |
| `tutorial/12-glossary` | glossary |
| `tutorial/13-metadata-and-index` | metadata and index |
| `tutorial/14-conditional-text` | conditional text |
| `tutorial/15-subject-scheme` | subject scheme |
| `tutorial/16-branch-filtering` | branch filtering |
| `tutorial/17-key-scopes` | key scopes |
| `tutorial/18-chunking-and-output` | chunking and output |
| `tutorial/19-bookmap` | bookmap |
| `tutorial/20-troubleshooting` | troubleshooting |
| `tutorial/21-hazards-and-safety` | hazards and safety |
| `tutorial/22-software-domains` | software domains |
| `tutorial/23-learning` | learning |
| `tutorial/24-drafts-and-localization` | drafts and localization |
| `tutorial/25-house-rules` | house rules |
| `tutorial/26-final` | final |

## Verification

Check the project with **Project > Check Project** in the editor, or with
`dogsbay-xml check .`. Maintainers can also run `scripts/check-stage.sh` from
the project root. From stage 03, the gate builds the deliverables in `project.json`.
Run `python3 scripts/check-output-links.py <output-directory>` after publishing HTML. Source health and generated output checks report separate results.

The chunking experiment under `examples/chunking/` is available from stage 18. Build its maps separately; they are not release deliverables.

Maintainers: `scripts/check-all-stages.sh` checks every stage branch, and
`docs-dev/` explains how the branches are kept.

Topic text is adapted from the Audacity Manual. See LICENSE and NOTICE for licensing and attribution.
