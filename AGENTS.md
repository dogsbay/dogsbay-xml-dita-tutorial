# Project context — Audacity User Guide (DITA)

This is the documentation set for **Audacity**, authored in DITA 1.3 and built
with DogsBay XML. It is also the finished state of a step-by-step DITA tutorial:
every `tutorial/NN-*` branch adds one feature, and this file describes the
conventions the finished project keeps.

## Layout

- `audacity-guide.ditamap` — the main guide (start here). `beginner-guide`,
  `podcaster-guide`, `audacity-book` (PDF), `audacity-collection` (all three
  guides, key-scoped) and `installation-variants` (branch filtering) reuse the
  same topics.
- `topics/` — concepts, tasks, references, a troubleshooting topic;
  `topics/glossary/` — glossary entries; `learning/` — a learning assessment;
  `shared/` — warehouses pulled in by conref; `samples/` — code pulled in by
  coderef; `images/` — illustrations.
- `keydefs-product.ditamap`, `keydefs-glossary.ditamap` — key definitions.
- `subject-scheme.ditamap` — the controlled values for `@platform`
  (`windows`, `mac`, `linux`) and `@audience` (`beginner`, `podcaster`).
- `filters/` — DITAVAL files, one per deliverable plus `review.ditaval` (flags).
- `project.json` — the DITA-OT project file: every deliverable this guide ships.
- `.dogsbay/config.xml` — default root map and deliverable, the metadata
  policy, the house rules (`house-style.sch`) and the format style.
- `scripts/check-stage.sh` — the gate: validation, project health,
  controlled values, house rules and a build of every deliverable.

## House style

- **Never hardcode the product name, version, download URL or project
  extension.** Use the keys `product-name`, `product-version`, `download-url`,
  `project-extension`: `<keyword keyref="product-name"/>`. Literals inside
  `<filepath>`, `<codeph>`, `<codeblock>` and `<cite>` are fine.
- **UI labels** use `<uicontrol>`, never `<b>`; menu paths use
  `<menucascade>`; a mnemonic is `<shortcut>` inside `<uicontrol>`.
- **Reuse, don't repeat.** Shared steps, notes and hazards live in `shared/`
  and are pulled in with `conref` or `conkeyref`.
- **Conditions** use only the values in `subject-scheme.ditamap`;
  `validate-conditions` fails on anything else.
- **Every topic needs a `<shortdesc>`** right after the title, under about 155
  characters, leading with what the topic is about.
- **Every topic needs keywords** in its prolog; tasks need a `<created>` date;
  an `<author>` is recommended. The metadata policy in `.dogsbay/config.xml`
  enforces this.
- **Review markup does not ship.** Resolve `<draft-comment>` and
  `<required-cleanup>` before a release; the house rules report them.
- **Titles** are sentence case. **Language** is `xml:lang="en-GB"` on every
  root element; product names and code carry `translate="no"`.
- **Format** every file with `dogsbay-xml format -i` before committing. Do not
  put character entities such as `&amp;` in text; write "and".

## Checks

Run `scripts/check-stage.sh` before every commit; it must print `STAGE OK`.
For one dimension: `dogsbay-xml validate-project .`, `project-health .`,
`validate-conditions -S subject-scheme.ditamap .`,
`project-health --include=schematron .`, or `dita --project=project.json`.
