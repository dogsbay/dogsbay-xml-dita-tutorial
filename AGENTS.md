# Project context — Audacity User Guide (DITA)

This is the documentation set for **Audacity**, authored in DITA 1.3 and built
with DogsBay XML. You (the agent) are helping maintain and fix it.

## Layout

- `audacity-guide.ditamap` — the main guide (start here). Other maps
  (`beginner-guide`, `podcaster-guide`, `audacity-book`, `audacity-collection`)
  reuse the same topics.
- `topics/` — concepts, tasks, references. `topics/glossary/` — glossary entries.
- `shared/` — content referenced by `conref` (`common-steps`, `common-notes`).
- `keydefs-product.ditamap`, `keydefs-glossary.ditamap` — key definitions.
- `filters/` — `.ditaval` conditional-publishing filters.
- `project.json` — the **DITA-OT project file**: the deliverables this guide ships
  (`full`, `beginner-mac`, `beginner-windows`, `podcaster-linux` = map · ditaval ·
  transtype · params). The source of truth for what builds.
- `.dogsbay/config.xml` — shared editor project settings (committed): the default
  root map (`audacity-guide.ditamap`), the required framework (`DITA-OT`, resolved
  per machine), and the default deliverable (`full`). `.dogsbay/local.xml` is a
  personal, gitignored override (e.g. a different active deliverable) — don't rely
  on it. Edit deliverables in `project.json`, not `.dogsbay`.

## House style (please follow when editing)

- **Never hardcode the product name or version.** Use the keys: `product-name`,
  `product-version`, `download-url`, `project-extension` (defined in
  `keydefs-product.ditamap`). Insert with `<keyword keyref="product-name"/>`.
- **UI labels** (buttons, menus, fields) use `<uicontrol>`, not `<b>`.
- **Menu paths** use `<menucascade><uicontrol>…</uicontrol></menucascade>`.
- **Reuse, don't repeat.** Shared steps/notes live in `shared/` and are pulled in
  with `conref`. If you find duplicated content, conref it.
- **Conditional content** uses `@platform` (`windows`, `mac`, `linux`) and
  `@audience` (`beginner`, `podcaster`) — match the values the **deliverable**
  `.ditaval` files (`mac-beginner` / `windows-beginner` / `linux-podcaster`) expect;
  those filters are the *contract* for what each value should be. These values aren't
  yet governed by a subjectScheme: to govern them (and catch drift like
  `platform="macos"` automatically), use the **dita-subject-schemes** skill — derive
  the controlled vocabulary from `filters/*.ditaval`, then validate with
  `validate_conditions` / **Project ▸ Check Controlled Values**.
  - Note: the canonical platform vocabulary is `windows`/`mac`/`linux`. The
    *branch-filter* ditavals `filters/platform-windows.ditaval` and
    `filters/platform-linux.ditaval` (used by `installation-variants.ditamap`)
    carry the same `macos` drift as the content, so don't blindly union *every*
    `.ditaval` when deriving the scheme — that would bake in the typo. Take the
    intended set from the deliverable ditavals; `rename_profile_value macos → mac`
    then cleans the content *and* those branch-filter ditavals in one pass.
- **Titles** are sentence case; keep topics single-sourced and focused.
- **Every topic needs a `<shortdesc>`** — one or two sentences, placed right after
  the title. Make it descriptive and SEO-friendly: lead with what the topic is
  about, keep it under ~155 characters, avoid filler like "this page describes…".
- Validate after every change; a topic should validate cleanly against its DOCTYPE.

## Which tools to use

- **Validate DITA with `validate_document`** (the editor tool) — it resolves the
  DITA DOCTYPEs via the editor's catalog. The generic `xml_validate` cannot find
  the DITA DTDs and will fail.
- **Edit open documents with the editor's document tools** (`set_document_content`,
  `replace_selection`) so changes land in the live editor buffer and are undoable.
  Use the generic `edit`/`write` only for files that aren't open in the editor.
- Use `where_used` before renaming/moving a topic, and `list_keys` before keyifying.

### Project-scale checks (one call, no files opened)

For anything that spans the whole guide, prefer the project tools over opening
files one by one:

- **`project_health`** — comprehensive read-only survey: validation errors,
  broken links, broken conref/keyref **element ids**, undefined/unused keys, and
  orphan topics. Run it first to triage, and again at the end as the done-gate —
  "publish-ready" means `project_health` reports clean.
- **`validate_project`** — validates every topic in the map's publication set;
  results also show in the editor's **Project Validation** tab.
- **`conref_audit`** — resolves every conref/keyref to a real file *and element
  id*; catches the `#file/idX` cases a plain link check misses.
- **`schematron_project house-style.sch`** — runs the project's house-style rules
  (shortdesc required, `<uicontrol>` not `<b>`, no hardcoded product name,
  allowed note types) across all topics in one call.
- **`validate_deliverables`** — validates each deliverable in `project.json`
  (map × `.ditaval` × transtype) and reports per output, so you can see which
  shipped products a problem affects.
- **`validate_deep`** — engine-tier validation: runs DITA-OT preprocessing on a
  deliverable (applying its DITAVAL), catching keyref/conref resolution and
  filtered-content errors the static checks miss. Needs DITA-OT installed; slower.
- **`build_deliverables`** — builds the deliverables with DITA-OT (transtype ·
  ditaval · params · output). Use to verify a deliverable actually publishes.

## Bulk changes — use code mode, don't open every file

For a change that applies the **same rule across many files** (normalize prolog
metadata, rename a profile value everywhere, add/align an element across all
topics, bulk find/replace), **write a script and run it** — do **not** open and
read every file into the conversation (that doesn't scale past a handful of files).

- Prefer an **XSLT** stylesheet (the idiomatic DITA transform) or a small
  **Python/lxml** or `sed`/`grep` script, run via `bash` over the topic files.
- Process the raw XML on disk; disable DTD loading in the script so you don't need
  the catalog.
- After running, **validate a sample** of the changed files with
  `validate_document` (not all of them) and spot-check the diff (`git diff`).
- Reserve the editor's `get/set_document_content` for **targeted, judgment-heavy
  edits** on the one or few files actually open — there the live buffer + undo
  matter.
- **Disk vs. live buffer.** Project-scale tools (`project_health`, `validate_project`,
  `metadata_set`, the refactors) read and write the files **on disk**; the editor
  document tools act on the **live buffer**. If a file is open with unsaved edits,
  save it (or close it) before a code-mode/bulk pass so the script sees your latest
  text and you don't clobber buffer changes.
