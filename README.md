# DogsBay DITA tutorial — a deliberately broken DITA project

A small but complete **Audacity User Guide** in DITA 1.3, seeded with realistic
problems, used to demo the **AI Agent** in DogsBay XML. The walkthrough starts
with single-file edits, hits the wall where per-file work stops scaling, and then
moves to project-scale tools — fixing the whole guide in single calls.

> This repo is the *starting* state — it is meant to be broken. Fixing it is
> the exercise.

## Start here

1. Open this folder as a project in **DogsBay XML**.
2. Open the **AI Agent** panel (right sidebar) and connect a provider.
3. Follow the walkthrough at
   <https://dogsbay.ai/dogsbay-xml-docs/getting-started/tutorial-agentic> —
   staged in four parts (one file at a time → why batch → project scale → the
   publish-ready gate), each scenario with the exact prompt to type.

- **`AGENTS.md`** — project context + house rules the agent reads automatically.
- **`.xagent/skills/audacity-house-style/`** — a project-specific agent skill.
- **`project.json`** — the DITA-OT project file: the deliverables this guide ships.
- **`.dogsbay/config.xml`** — shared editor project settings (default map, required
  framework, default deliverable); committed. `.dogsbay/local.xml` is a personal,
  gitignored override.

### Not in the bundled copy

`DEMO.md` (the scripted walkthrough) and `ISSUES.md` (the answer key: every
planted issue and its fix) live here for maintainers, and `.gitattributes`
marks both `export-ignore` so they stay out of the `git archive` snapshot the
editor ships as its sample project.

They name every planted issue and its fix. The sample exists to show the
project tools *finding* those issues, and an agent pointed at the project will
open a root-level `ISSUES.md` — so shipping the answer key beside the puzzle
meant the demo could not demonstrate the thing it is for. The editor's e2e
workflow checks out this repository rather than the bundled zip, so it still
sees both.

## Layout

```
audacity-guide.ditamap        main guide (start here)
beginner-guide / podcaster-guide / audacity-book / audacity-collection .ditamap
keydefs-product / keydefs-glossary .ditamap   key definitions
topics/            concepts, tasks, references
topics/glossary/   glossary entries
shared/            conref'd content (common-steps, common-notes)
filters/           .ditaval conditional-publishing filters
project.json       DITA-OT project file (deliverables)
.dogsbay/          shared editor project settings (config.xml; local.xml gitignored)
images/
```

## Reset between runs

The agent's fixes are working-tree edits. To get back to the broken starting
state and run the demo again:

```bash
git restore . && git clean -fd
```

## Licence and attribution

This project is licensed under the **Creative Commons Attribution 4.0
International** licence (CC BY 4.0). The full text is in [LICENSE](LICENSE);
the summary is at <https://creativecommons.org/licenses/by/4.0/>.

You may share and adapt this material, including commercially, provided you
give appropriate credit, link to the licence, and say whether you changed
anything.

### Credit

The topics under `topics/` and `shared/` are **adapted from the
[Audacity Manual](https://manual.audacityteam.org/)**, copyright the Audacity
Team and the Manual's authors, which is available under the
[Creative Commons Attribution 3.0](https://creativecommons.org/licenses/by/3.0/)
licence. That copyright notice and those licence terms are kept in
[NOTICE](NOTICE), as CC BY 3.0 requires of anyone reusing the material.

**What changed:** the material was rewritten as DITA 1.3 topics, restructured
into maps, and deliberately seeded with errors so that fixing them can be
taught. It no longer describes Audacity accurately and must not be used as its
documentation. The Audacity Team does not endorse this work and is not
affiliated with it. Audacity® is a registered trademark of Dominic Mazzoni.

Everything else here — the walkthrough, the answer key, `AGENTS.md`, the
DITAVAL filters, the Schematron house style and the project configuration — is
original work by DogsBay Ltd., under the same CC BY 4.0 licence.
