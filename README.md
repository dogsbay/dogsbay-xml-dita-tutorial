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

## Licence and attribution

This project is licensed under the **Creative Commons Attribution 4.0
International** licence (CC BY 4.0). The full text is in [LICENSE](LICENSE);
the summary is at <https://creativecommons.org/licenses/by/4.0/>.

You may share and adapt this material, including commercially, provided you
give appropriate credit, link to the licence, and say whether you changed
anything.

### Credit

The topics under `topics/` and `shared/` are **adapted from the Audacity user
documentation**, published by the Audacity team, and have been rewritten in
DITA 1.3 and deliberately seeded with errors for teaching purposes. They do
not describe Audacity accurately and should not be used as its documentation.

Audacity® is a registered trademark of Dominic Mazzoni. This project is not
affiliated with, nor endorsed by, the Audacity team.

Everything else here — the walkthrough in `DEMO.md`, the answer key in
`ISSUES.md`, `AGENTS.md`, the DITAVAL filters, the Schematron house style and
the project configuration — is original work by DogsBay Ltd., under the same
licence.

### One thing to confirm before wider distribution

CC BY 4.0 is chosen here as the plain attribution licence. If the upstream
Audacity documentation turns out to be under a **ShareAlike** variant, this
repository must carry that same variant instead, since ShareAlike obliges
derivatives to keep it. Attribution and a link to the source are required
either way, and are given above.
