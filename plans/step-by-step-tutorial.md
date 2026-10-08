# Plan: the step-by-step DITA tutorial

This is the original design record. The implemented 27-stage sequence and
verification results are documented in [the redesign](../docs-dev/redesign.md).
Its first map and build are stages 02 and 03.

Turn this sample into a guided, stage-by-stage tour of DITA 1.3, built up from
one concept topic to a complete, coherent Audacity documentation set, with each
stage on its own git branch and the walkthrough published as a DogsBay MD site.
Written 2026-09-21.

## Goals

1. **Start from scratch.** Stage 1 is a single concept topic. Nothing else.
2. **One feature per stage.** Each stage adds one DITA feature (or one tight
   group) on top of the previous stage, so the diff between two stage branches
   *is* the lesson.
3. **End coherent.** The last stage is a complete, publish-ready Audacity guide:
   the same product, topics and maps as today's `main`, minus the planted
   issues, plus the DITA features `main` does not use yet.
4. **Testable.** Every stage branch passes the same gate (`scripts/check-stage.sh`):
   every file validates, project health is clean, every deliverable builds.
5. **Documented.** A separate DogsBay MD site walks a reader through the stages
   with the exact files to write and the commands to run.

Out of scope for now: rewriting `main`'s "deliberately broken" demo. It stays as
is. A follow-on could regenerate it from the final stage with a plant-the-issues
script so both tutorials share one content base (see "Later").

## Readers

- **A writer new to DITA** who knows what a topic is and wants to learn the
  language by building something real, in order, with a check at every step.
- **A DogsBay XML user** who wants to see every project feature (keys, reuse,
  filters, deliverables, health, house rules) exercised on a small project.
- **An AI agent** pointed at a stage branch and told "do the next stage".

## The branch model

- Stage branches are named `tutorial/NN-slug` and form one chain: each stage
  branch is the previous branch plus the commits for that stage.
- The chain starts from an **orphan** root (`tutorial/00-setup`) that carries
  only `README.md`, `LICENSE`, `NOTICE`, `.gitignore`, `.gitattributes`,
  `.dogsbay/config.xml`, `scripts/check-stage.sh` and an empty `topics/`. It
  shares no history with `main`, because `main` is a finished snapshot and the
  tutorial must start empty.
- `main` keeps the broken demo. The plan, the gate script and the developer
  docs are merged to `main` from `plan/step-by-step-tutorial`.
- The final stage branch is also tagged `tutorial/final` so the docs can link
  to a stable "finished" tree.
- Diffs between stages are linked from the docs as GitHub compare URLs:
  `https://github.com/dogsbay/dogsbay-xml-dita-tutorial/compare/tutorial/01-concept...tutorial/02-task-and-reference`.
- **Editing a middle stage** means rebasing every later stage. That is the price
  of "content builds on top of each other"; `scripts/rebase-stages.sh` (later
  stage of this plan) walks the chain with `git rebase --onto` and reruns the
  gate on each branch.

## The gate (`scripts/check-stage.sh`)

Already written and verified on this branch:

```bash
scripts/check-stage.sh            # validate-project + project-health + dita --project
SKIP_BUILD=1 scripts/check-stage.sh
STRICT=0 scripts/check-stage.sh   # project-health at --severity=error only
```

- Fails on today's `main` (2 invalid files, broken link, dangling conref, and
  the rest of `ISSUES.md`), which is the expected result for the broken snapshot.
- Passes on a one-topic project with and without a map and `project.json`,
  including the DITA-OT html5 build.
- Tools: `dogsbay-xml` (`~/github/dogsbay-xml/bin/dogsbay-xml`) and DITA-OT
  4.3.5 (`~/Downloads/dita-ot-4.3.5`), both overridable by env var. `xmllint`
  cannot be used: libxml2 rejects the DITA DTDs (entity amplification limit).
- Timing on the full guide: validate 2 s, health 2.5 s, build of four
  deliverables 11 s.

A driver `scripts/check-all-stages.sh` will check out each `tutorial/*` branch
into a temporary worktree and run the gate, so the whole ladder is one command.

## Stage ladder

Each stage: what the reader builds, the DITA features it introduces, the files
that change, and what the gate proves. "Extends `main`" marks features the
current sample does not use.

### Part 1 — Topics

| # | Branch | Builds | DITA features | Files |
|---|--------|--------|---------------|-------|
| 00 | `tutorial/00-setup` | An empty project that the tools recognise | DOCTYPEs and the DITA-OT catalog; `.dogsbay/config.xml` (project type, framework, format style); the gate script | config, scripts, README |
| 01 | `tutorial/01-concept` | *What is Audacity?* as a `<concept>` | `<concept>`, `@id`, `<title>`, `<shortdesc>`, `<conbody>`, `<p>`, `<ul>`/`<li>`, `<section>`; validate one file | `topics/what-is-audacity.dita` |
| 02 | `tutorial/02-task-and-reference` | *Recording your first track* (task) and *Supported audio formats* (reference) | `<task>`/`<taskbody>`, `<context>`, `<steps>`/`<step>`/`<cmd>`/`<info>`, `<result>`; `<reference>`/`<refbody>`, CALS `<table>` (`tgroup`, `colspec`, `thead`, `row`, `entry`); why three information types | 2 topics |
| 03 | `tutorial/03-inline-and-block` | *What is digital audio?*, *Trimming audio* | Inline: `<uicontrol>`, `<menucascade>`, `<shortcut>`, `<wintitle>`, `<filepath>`, `<ph>`, `<term>`, `<b>`/`<i>` and when not to; block: `<note>` and its types, `<dl>`, `<ol>`, `<sl>`, `<lq>`, `<fn>`, `<simpletable>`, `<codeblock>`, `<pre>` | 2 topics |
| 04 | `tutorial/04-rich-tasks` | *Installing Audacity*, *Exporting audio*, *Removing background noise* | `<prereq>`, `<postreq>`, `<substeps>`, `<choices>`, `<choicetable>` *(extends main)*, `<stepxmp>`, `<stepresult>`, `<steps-unordered>`, `<example>`, `<tutorialinfo>`, `@importance="optional"` | 3 topics |
| 05 | `tutorial/05-links` | Topics point at each other | `<xref>` (local, `@scope="external"`, `@format`), `<related-links>`/`<link>`/`<linklist>`/`<linkpool>`, `<desc>`, why links belong in the map later | all topics |
| 06 | `tutorial/06-figures` | Screenshots, a waveform SVG and the decibel formula | `<fig>`/`<image>` (`@href`, `@scale`, `@placement`, `<alt>`), `<svg-container>`, `<equation-block>`/`<mathml>`, `<imagemap>` *(all extend main)*; an `images/` folder | `images/`, 2 topics |

### Part 2 — Maps and publishing

| # | Branch | Builds | DITA features | Files |
|---|--------|--------|---------------|-------|
| 07 | `tutorial/07-first-map` | `audacity-guide.ditamap` and the first build | `<map>`, `<title>`, `<topicref>`, `<topichead>`/`@navtitle`, `<topicmeta>`; DITA-OT `html5`; `project.json` with the `full` deliverable; `default-root-map` in `.dogsbay` | map, project.json, config |
| 08 | `tutorial/08-map-structure` | Hierarchy, sequences and generated links | nested `<topicref>`, `@collection-type`, `@linking`, `@toc`, `@processing-role="resource-only"`, `@locktitle`, `<topicgroup>`, `<reltable>`/`<relheader>`/`<relcolspec>`/`<relrow>`/`<relcell>`; how map links replace hand-written `<related-links>` | map, topics |
| 09 | `tutorial/09-keys` | Product variables and indirect links | `<keydef>` with `<keywords>` (product-name, version, download-url, project-extension), `<keyword keyref>`, `@keyref` on `<xref>`/`<link>`, `<keydef href>` for topics (`start-here`), `<mapref>` to `keydefs-product.ditamap`, `<linktext>`; `dogsbay-xml keys` | keydefs map, all topics |
| 10 | `tutorial/10-reuse` | The `shared/` warehouse | `@conref` (element and range with `@conrefend`), `@conkeyref` *(extends main)*, `@id` on reusable elements, warehouse topics kept out of the TOC, `<step conref>`, `<note conref>`; conref push `@conaction` (`mark` + `pushbefore`/`pushafter`/`pushreplace`) done correctly | `shared/`, topics |
| 11 | `tutorial/11-glossary` | Glossary entries and abbreviations | `<glossentry>`/`<glossterm>`/`<glossdef>`, `<glossBody>`, `<glossAlt>`/`<glossAbbreviation>`/`<glossSurfaceForm>` *(extends main)*, `<abbreviated-form>`, `<term keyref>`, `<glossgroup>`, `keydefs-glossary.ditamap` | `topics/glossary/`, keydefs map |
| 12 | `tutorial/12-metadata-and-index` | Prolog metadata and a real index | `<prolog>`/`<metadata>`, `<author>`, `<critdates>`/`<created>`/`<revised>`, `<audience>`, `<category>`, `<keywords>`/`<keyword>`, `<indexterm>` nested, `<index-see>`, `<index-see-also>`, `<index-sort-as>`, `<copyright>`, `<resourceid>`, `<data>`, map-level `<topicmeta>`; the `.dogsbay` metadata policy | all topics, config |

### Part 3 — Conditions and variants

| # | Branch | Builds | DITA features | Files |
|---|--------|--------|---------------|-------|
| 13 | `tutorial/13-conditional-text` | Platform and audience conditions | `@platform`, `@audience`, `@product`, `@otherprops`, `@props`, `@rev`; DITAVAL `<prop action="include/exclude/flag">`, `<revprop>` with `<startflag>`/`<endflag>`, `<style-conflict>`; deliverables per ditaval in `project.json` (`beginner-mac`, `beginner-windows`, `podcaster-linux`); `beginner-guide` and `podcaster-guide` maps | `filters/`, maps, topics |
| 14 | `tutorial/14-subject-scheme` | A controlled vocabulary for the conditions | `<subjectScheme>`, `<subjectdef>`, `<enumerationdef>`/`<attributedef>`/`<defaultSubject>`, `<hasNarrower>`, `<schemeref>` in the root maps; `dogsbay-xml validate-conditions` | `subject-scheme.ditamap`, maps |
| 15 | `tutorial/15-branch-filtering` | Three install variants from one topic | `<ditavalref>`, `<ditavalmeta>`, `<dvrResourcePrefix>`/`<dvrResourceSuffix>`/`<dvrKeyscopePrefix>` *(suffix and keyscope prefix extend main)*; `installation-variants.ditamap`; `list_branches` | map, filters |
| 16 | `tutorial/16-key-scopes` | One collection of three guides | `@keyscope` on `<mapref>`, scoped keys (`beginner.start-here`), `<keydef scope="peer">` *(extends main)*, `audacity-collection.ditamap`; `dogsbay-xml keys --scope` | collection map, maps |
| 17 | `tutorial/17-chunking-and-output` | Control over pages and file names | `@chunk` (`to-content`, `by-topic`), `@copy-to`, nested topics in one file, `<dita>` composite, `@outputclass`, `@print`, `@search`, `<navref>`, `<topicset>`/`<topicsetref>` *(all extend main)* | maps, one composite topic |

### Part 4 — Books and specialised topics

| # | Branch | Builds | DITA features | Files |
|---|--------|--------|---------------|-------|
| 18 | `tutorial/18-bookmap` | The PDF book | `<bookmap>`, `<booktitle>`, `<bookmeta>` (`<bookrights>`, `<bookid>`, `<publisherinformation>`), `<frontmatter>` (`<preface>`, `<notices>`, `<booklists>`: `<toc>`, `<figurelist>`, `<indexlist>`, `<glossarylist>`), `<part>`/`<chapter>`/`<appendix>`, `<backmatter>`; the `pdf` transtype and `pdf` deliverable | `audacity-book.ditamap`, project.json |
| 19 | `tutorial/19-troubleshooting` | *Why is my recording silent?* | `<troubleshooting>`/`<troublebody>`/`<condition>`/`<troubleSolution>`/`<cause>`/`<remedy>`, `<tasktroubleshooting>`, `<steptroubleshooting>`, `<note type="trouble">` *(all extend main)* | 1 new topic, tasks |
| 20 | `tutorial/20-hazards-and-safety` | Hearing-safety statements | `<hazardstatement>`/`<messagepanel>`/`<typeofhazard>`/`<consequence>`/`<howtoavoid>`, `<hazardsymbol>` *(extends main)*; when a hazard is not a note | 2 topics |
| 21 | `tutorial/21-software-domains` | Scripting Audacity from the command line | `<codeblock>` with `@outputclass="language-…"`, `<coderef>`, `<screen>`, `<userinput>`/`<systemoutput>`, `<cmdname>`, `<option>`, `<parmname>`, `<varname>`, `<apiname>`, `<parml>`, `<msgph>`/`<msgblock>`/`<msgnum>`, `<syntaxdiagram>` *(all extend main)* | 1 new reference (`mod-script-pipe`), 1 task |
| 22 | `tutorial/22-learning` | A "test your knowledge" page | `<learningAssessment>`, `<lcInteraction>`, `<lcSingleSelect>`/`<lcMultipleSelect>`, `<lcAnswerOption>`, `<learningSummary>`, `<learningMap>` *(extends main; optional stage, DITA-OT ships the L&T plugin)* | `learning/` |

### Part 5 — Governance and the finish

| # | Branch | Builds | DITA features | Files |
|---|--------|--------|---------------|-------|
| 23 | `tutorial/23-drafts-and-localization` | Ready for review and translation | `<draft-comment>`, `<required-cleanup>`, `@status`, `@rev` with a revised-content ditaval flag, `@xml:lang`, `@translate="no"`, `@dir`, `<sort-as>`, `<change-historylist>` *(extend main)* | topics |
| 24 | `tutorial/24-house-rules` | Rules as code | `house-style.sch` (Schematron), `AGENTS.md`, the `.xagent/skills/audacity-house-style` skill, format style in `.dogsbay`, `dogsbay-xml project-health --schematron` as the done-gate | sch, AGENTS.md, skill |
| 25 | `tutorial/25-final` | The complete guide, tagged `tutorial/final` | Nothing new: every deliverable builds, `project-health` is clean at default severity, `project.json` ships `full`, `beginner-mac`, `beginner-windows`, `podcaster-linux`, `book-pdf` and `install-variants` | — |

Feature checklist versus `main` (what "work toward the current content" means):
topic/concept/task/reference/glossentry ✔ (01, 02, 11), map/bookmap/collection
✔ (07, 16, 18), keydefs and `start-here` ✔ (09), conref and conref push ✔ (10),
ditaval filters and deliverables ✔ (13), ditavalref branch filtering ✔ (15),
key scopes ✔ (16), reltable ✔ (08), indexterm and index-see ✔ (12),
abbreviated-form ✔ (11), subject scheme (named in `AGENTS.md` as "not yet") ✔
(14), metadata policy ✔ (12), Schematron, `AGENTS.md`, skill ✔ (24). Everything
marked *extends main* is new.

### Content decisions

- **Same product, same topics.** Reuse the Audacity Manual text already in
  `main` (CC BY 3.0, credited in `README.md`/`NOTICE`), fixed, and add the new
  topics the extra features need: a troubleshooting topic, a scripting
  reference, a hazard statement inside the recording task, a learning
  assessment.
- **`what-is-audacity` becomes a `<concept>`** rather than the generic `<topic>`
  it is on `main`. Stage 01 needs a concept; the generic topic is introduced in
  stage 10 for the warehouses, where it fits.
- **Text is written once, correctly.** Stages add structure, they do not plant
  bugs. Mistakes are demonstrated in the docs by showing what the gate reports
  when you make them, not by committing them.
- **Formatting.** Every stage is run through `dogsbay-xml format` before the gate,
  so `project-health` shows no "not in house style" warnings and diffs stay
  about the feature.

## The docs site

A new repo `~/github/dogsbay-xml-dita-tutorial-docs`, published at
`https://dogsbay.ai/dogsbay-xml-dita-tutorial-docs` (worker name, repo name and
`wrangler.jsonc` `name` identical, as the blog outage taught).

- Scaffolded with `dogsbay site init --from dogsbay-md --deploy cloudflare-workers`;
  `dogsbay.config.yml` copied from `dogsbay-migrate-docs` (pins `from: dogsbay-md`,
  carries the `agent:` block); `.gitignore` copied verbatim.
- `plans/site-plan.md` first, in the migrate-docs style.
- Structure (`content/nav.yml`):
  1. Start here: what you will build, how the branches work, install DITA-OT and
     DogsBay XML, run the gate.
  2. One page per stage, `type: tutorial`, same skeleton as
     `dogsbay-xml-docs/content/getting-started/tutorial-agentic.md`: intro, **Time**
     and **You need**, `## Step n:` headings with `:::steps`, the file to write in a
     fenced `xml` block titled with its path, the command to run, what the gate
     says, `## What you learned`, `:::cards` to the next stage and the compare link.
  3. Reference: element-to-stage index (every element in the ladder above with the
     stage that introduces it), the gate script, branch cheatsheet.
- DITA markup and `{…}` examples stay inside fences (migrate-docs README: the
  build evaluates Jinja-style syntax outside them).
- Check: `dogsbay site check` before every commit, plus `scripts/check-excerpts.sh`
  that verifies every fenced block titled with a path matches that file on the
  page's stage branch, so the docs cannot drift from the branches.

## Status (2026-09-21)

All 26 stage branches exist, pass the gate and are tagged at `tutorial/final`.
Docs pages exist for all five parts (dogsbay-xml-dita-tutorial-docs); the remaining work is
`scripts/check-excerpts.sh` in the docs repo (its prototype, fidelity.py, lives in a scratchpad). Deviations from the ladder:
stage 17 uses a nested `<reference>` rather than a `<dita>` composite (the
metadata policy cannot see a composite root), stage 16 drops the `<keydef
scope="peer">` in favour of a peer `<mapref>`, and stage 22 needs the gate to
validate `learning/` against the DITA-OT catalog.

## Work breakdown (feature branches, in order)

1. `plan/step-by-step-tutorial` (this branch): plan, gate script,
   `docs-dev/stage-gate.md`. Merge to `main`.
2. `tutorial/00-setup` → `tutorial/06-figures` (Part 1), each branch gated.
3. Docs repo scaffold, site plan, start-here pages, Part 1 pages.
4. Parts 2 and 3 branches, then their pages.
5. Parts 4 and 5 branches, then their pages; tag `tutorial/final`.
6. `scripts/check-all-stages.sh`, `scripts/rebase-stages.sh`,
   `scripts/check-excerpts.sh`; `docs-dev/stage-branches.md`.
7. `README.md` on `main` gains a "Learn DITA step by step" section pointing at
   the docs site and the branch list.

Every branch: gate passes before commit; commits need approval.

## Later

- Regenerate `main`'s broken demo from `tutorial/final` with a plant-the-issues
  script driven by `ISSUES.md`, so the agent demo and the tutorial share one
  source of truth.
- A "learning path" in `dogsbay-xml-docs` that links each stage to the editor
  feature it exercises.

## Decisions to confirm

1. Orphan root for the stage chain (no shared history with `main`).
2. Docs in a separate repo, `dogsbay-xml-dita-tutorial-docs`.
3. `what-is-audacity` as a `<concept>` in the ladder.
4. Stage 22 (learning and training) kept as an optional stage.
