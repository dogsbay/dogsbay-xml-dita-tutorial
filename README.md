# DITA tutorial

Build a guide through 27 stages. Maps begin at stage 02; HTML publication begins at stage 03.

You are on stage 12: glossary.

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

Run `scripts/check-stage.sh` from the project root. From stage 03, the gate builds the deliverables in `project.json`.
Run `python3 scripts/check-output-links.py <output-directory>` after publishing HTML. Source health and generated output checks report separate results.

The chunking experiment under `examples/chunking/` is available from stage 18. Build its maps separately; they are not release deliverables.

Topic text is adapted from the Audacity Manual. See LICENSE and NOTICE for licensing and attribution.
