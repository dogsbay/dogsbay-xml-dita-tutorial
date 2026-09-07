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
3. Follow **[`DEMO.md`](DEMO.md)** — staged in four parts (one file at a time →
   why batch → project scale → the publish-ready gate), each scenario with the
   exact prompt to type.

- **[`DEMO.md`](DEMO.md)** — the scripted walkthrough (the main event).
- **[`ISSUES.md`](ISSUES.md)** — the answer key: every planted issue and its fix.
- **`AGENTS.md`** — project context + house rules the agent reads automatically.
- **`.xagent/skills/audacity-house-style/`** — a project-specific agent skill.
- **`project.json`** — the DITA-OT project file: the deliverables this guide ships.
- **`.dogsbay/config.xml`** — shared editor project settings (default map, required
  framework, default deliverable); committed. `.dogsbay/local.xml` is a personal,
  gitignored override.

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

## Where this content comes from, and its licence

The topics are adapted from the Audacity user documentation. The Audacity
manual is published by the Audacity team under a Creative Commons licence, so
this derivative carries the same obligations: attribution, and the same licence
on redistribution.

**This repository does not yet carry a `LICENSE` file, and must not be
published without one.** Two things need settling first: which Creative
Commons version and variant the source material is under, and therefore what
this repository must be licensed as. The demo material written for this
project (`DEMO.md`, `ISSUES.md`, `AGENTS.md`, the DITAVAL filters and the
Schematron house style) is DogsBay's own and can carry whatever licence
DogsBay chooses, but the topics under `topics/` and `shared/` cannot.
