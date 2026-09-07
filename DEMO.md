# AI Agent demo — from a single edit to a whole project

**The story.** You've inherited the *Audacity User Guide* from a writer who left
in a hurry. It builds… mostly. But topics are missing descriptions, there are
validation errors, broken links and conrefs, hardcoded product names,
inconsistent conditions, an overgrown topic, and an unfinished one.

You'll fix it with the **AI Agent** — and the demo is deliberately staged so you
feel *why* the project-scale tools exist:

- **Part A — one file at a time.** Small, focused edits on the document in front
  of you: simplify a paragraph, write a description, tune it for SEO. The agent
  as a careful co-author.
- **Part B — the wall.** Try one of those edits *everywhere* and you'd have to
  open every topic — which doesn't scale and blows out the agent's context
  window. This is where the demo turns.
- **Part C — project scale.** The agent surveys, validates, and audits the
  **whole guide in single calls — without opening every file** — and edits in
  bulk with *code mode*.
- **Part D — the gate.** "Make it publish-ready," proven by a check the agent
  *must show you* (and that you can run yourself in the editor).

> This repo **is** the broken starting point. The agent's fixes are working-tree
> changes — reset any time with `git restore . && git clean -fd`. The config
> files (`AGENTS.md`, `project.json`, `.dogsbay/config.xml`, `house-style.sch`,
> `.xagent/skills/`) are committed, so a reset keeps them and only reverts topic
> content (and `.dogsbay/local.xml`, being gitignored, survives too). Full issue
> inventory in **`ISSUES.md`** (the "answer key").

## Before you start

1. Open this folder as a project in DogsBay XML.
2. Open the **AI Agent** panel (sparkle icon, right sidebar). On open it reads
   `AGENTS.md` (house rules) and loads skills automatically.
3. Connect a provider — Scenario 0.

> **Driving this headlessly.** Every project-scale and refactor tool is also a
> typed CLI/MCP command (`bin/dogsbay …`), so most of the demo runs without the
> GUI. A few scenarios are **editor-UI** — they show a panel, the live buffer, or
> the status bar and have no headless equivalent: **0** (provider bar), **1** (live
> selection), **3b** (Author view), and **14b** (status-bar deliverable selector).
> Those are marked **[editor UI]** below.

---

# Part A — One file at a time

## Scenario 0 — Connect a provider  [editor UI]

**Shows:** lazy startup, provider bar, multi-provider, ChatGPT login.

The panel opens with no API key — the hint line says what to do. Pick one:

- **Local & free:** choose `ollama` in the provider dropdown → **Use** (needs Ollama running).
- **API key:** choose `anthropic`/`openai`/`gemini`, paste a key → **Use**.
- **ChatGPT:** click **Sign in to ChatGPT** (browser OAuth; shared with the CLI).

Then try `/help` and `/skills` — you'll see the bundled DITA skills plus the
project's own `audacity-house-style` skill (from `.xagent/skills/`).

> `/provider` or `/model` switch any time; the header shows
> `provider / model · session`.

## Scenario 1 — Simplify a selected paragraph (selection context)  [editor UI]

**Shows:** the agent acts on highlighted text; live-buffer edit + undo.

Open `topics/what-is-digital-audio.dita` and **select** the wordy opening
paragraph.

> **Prompt:** *"Rewrite the selected paragraph to be simpler and shorter."*

You didn't paste anything — the selection rides with your message. The approval
prompt now shows the **actual before/after change** (not a blind yes/no), so you
approve what you can see. Apply it; **Ctrl+Z** undoes it like any edit. This is the
agent at its smallest and most precise: one selection, one change.

> **No typing? Right-click instead.**  [editor UI]  Select text and right-click →
> **AI** for the same transforms as a menu — *Rewrite / Simplify / Fix issues /
> Summarize / Expand*, plus a **DITA** section (*Generate shortdesc*, *Wrap as
> note*). Each shows the same before/after review, and the dialog footer names the
> **provider · model · tokens · cost** that produced it.

## Scenario 2 — Write a description for a topic (authoring)

**Shows:** the agent authors DITA structure, not just fixes it — via the
`dita-shortdesc` skill.

Almost every topic here has **no `<shortdesc>`**. With
`what-is-digital-audio.dita` still open:

> **Prompt:** *"This topic has no shortdesc. Write a concise one-sentence
> description and add it in the right place."*

Steered by the **`dita-shortdesc`** skill, the agent inserts a standalone,
front-loaded `<shortdesc>` right after the title (the correct DITA position) and
re-validates. One file, one focused edit.

> **Menu shortcut.**  [editor UI]  Select the topic body, right-click → **AI ▸
> Generate shortdesc** for the same result in one click, reviewed as a diff before
> it lands. (The DITA actions only appear — and only emit DITA elements — when the
> document actually is DITA.)

## Scenario 3 — Make a description SEO-friendly

**Shows:** content-quality judgment on a single field — the SEO half of
`dita-shortdesc`.

Open `topics/what-is-audacity.dita` — it has a bland placeholder description:
*"This page is about the software and some of the things it does."*

> **Prompt:** *"Rewrite this topic's shortdesc to be SEO-friendly — lead with what
> the product is, keep it under ~155 characters, make it compelling."*

The `dita-shortdesc` skill carries the discipline: rewrite just the `<shortdesc>`,
lead with the subject, ≤155 chars, active voice, no filler, reads standalone (it's
the link preview + HTML meta description). This is the per-page polish you do by
hand — fast, on the open file.

## Scenario 3b — Edit a topic in Author view (WYSIWYG)  [editor UI]

**Shows:** Author view — `author_outline`, `author_insert_block`, `author_set_text`,
`author_issues` (structural editing without angle brackets).

Open `topics/trimming-audio.dita` and switch to the **Author** tab: the topic
renders as editable blocks, not XML.

> **Prompt:** *"In Author view, add a step that tells the user to listen back to the
> result before saving."*

`author_outline` returns the block tree as JSON with stable block ids;
`author_insert_block --parent <id> --kind step` inserts a step in the right place;
`author_set_text` fills its text; `author_issues` flags structural problems. The
model stays valid DITA throughout — switch back to the **Editor** tab to see the
XML it produced. This is single-file authoring, visually.

---

# Part B — The wall: why batch mode exists

## Scenario 4 — "Now do it everywhere" (don't kill the context)

**Shows:** why per-file doesn't scale, and the agent's bulk strategy — the same
`dita-shortdesc` skill, now applied across the whole guide.

You just wrote one description. The guide has ~20 topics, and nearly all are
missing one.

> **Prompt:** *"Every topic in the guide should have a shortdesc. Add a sensible
> one to each — but don't open and read all of them into our conversation."*

Watch what the agent does **not** do: open 20 files (that floods its context
window and runs up cost — read 20 topics and there's no room left to reason).
Instead — steered by `AGENTS.md` and its built-in rules — it:

1. **Finds the gaps in one call** — `schematron_project` with `house-style.sch`
   (which has a "every topic needs a shortdesc" rule), or an `xpath` query —
   getting back just the *list* of topics missing a description, not their bodies.
2. **Edits in bulk with code mode** — writes a small script/XSLT and runs it over
   those files on disk, instead of read-edit-write per file.
3. **Validates a sample** to confirm, and shows the diff.

This is the hinge of the whole platform: **targeted edits → editor tools;
project-wide work → batch tools + code mode.** Everything in Part C is built on
that idea — single project-scale calls that never open the files.

---

# Part C — Project scale (single calls, no files opened)

## Scenario 5 — Survey the whole guide

**Shows:** `project_health` — one comprehensive, read-only call.

> **Prompt:** *"Run a health check on this guide and give me a prioritized list of
> everything that's wrong."*

In a single call (no topics opened), `project_health` reports validation errors,
broken references, **broken conref element ids**, undefined/unused keys, and
orphan topics. That's your to-do list — and the done-gate you'll return to in
Part D.

## Scenario 5b — Search and query across the project

**Shows:** `search_project` + `xpath_query` (and the raw-XML toolbox:
`format_document`, `transform_xslt`).

> **Prompt:** *"Find every file that still hardcodes the version '3.4', and list all
> the `<note>` types used across the guide."*

`search_project "3.4"` returns literal matches with file + line across the whole
project; `xpath_query "//note/@type"` returns every note type in use — exactly the
reconnaissance you want before writing a house rule or a keyify pass. The same XML
engine backs `format_document` (pretty-print a file) and `transform_xslt` (run a
stylesheet), for raw-XML chores that aren't DITA-specific.

## Scenario 6 — Validate every topic, and see it in the editor

**Shows:** `validate_project` + the **Project Validation** tab.

> **Prompt:** *"Validate every topic in the guide and fix the validation errors."*

The agent validates the map's publication set in one call, finds the invalid
`<x>` element and `note type="tipp"` in `installing-audacity.dita` and
`trimming-audio.dita`, fixes them, and re-validates until clean. The agent also
gets **validation feedback after each of its own edits** automatically, so it
catches a fix that re-broke something in the same turn instead of at the end.

Then verify it yourself: **XML → Validate Project**. Results land in the
**Project Validation** tab — **single-click any error to open that file at the
line**. Agent and human read the *same* validation surface.

> **Fix one straight from the marker.**  [editor UI]  Right-click any error in the
> **Project Validation** tab → **Fix with AI**: it hands *that specific* error
> (file, line, message) to the agent as a focused fix and re-validates — turning a
> diagnostic the editor already computed into a one-click repair, without retyping
> it into the chat.

## Scenario 7 — Repair broken links and conref ids

**Shows:** `check_links` + `conref_audit` (element-id resolution).

> **Prompt:** *"Find every broken link and broken content reference and fix them."*

`check_links` flags the related-link in `recording-your-first-track.dita` to the
non-existent `digital-audio-basics.dita` (→ `what-is-digital-audio.dita`).
`conref_audit` catches the subtle one: `removing-background-noise.dita` conrefs
`#common-notes/backup-warningX` — the *file* exists but that *element id* doesn't
(the id is `backup-warning`). Approve the fixes.

## Scenario 7b — Warehouse a note for reuse (conref)

**Shows:** `extract_conref` + `inline_conref` — content reuse, both directions.

The tip in `recording-your-first-track.dita` (`#quiet-room-tip`) is advice other
recording topics could share, but it's stuck inline in one file. (The guide already
reuses shared notes/steps via conref — see `shared/common-notes.dita`.)

> **Prompt:** *"Move the quiet-room-tip note into the shared warehouse and conref it
> back, so other topics can reuse it."*

`extract_conref recording-your-first-track.dita quiet-room-tip --to
shared/common-notes.dita` moves the element into the warehouse topic and leaves a
`conref` in its place — any topic can now pull `#common-notes/quiet-room-tip`. The
inverse, `inline_conref`, expands a conref back to literal content when you no longer
want the indirection. Both are reference-safe and `--dry-run`-able.

## Scenario 8 — Enforce house style as policy

**Shows:** `schematron_project` with the project's own `house-style.sch`.

> **Prompt:** *"Run our house-style rules and fix every violation."*

`schematron_project house-style.sch` flags, across the whole guide: UI labels
wrapped in `<b>` (should be `<uicontrol>`), hardcoded "Audacity" in prose (should
be the `product-name` key), and the disallowed note type — all in one call. The
agent fixes them, using the `audacity-house-style` skill for judgment about
what's a real UI control vs. decorative emphasis, and re-runs until the rules
pass.

> **8 vs 9 — same symptom, two beats.** Both touch hardcoded "Audacity". Scenario
> 8 is the **markup/style sweep** (`<b>` → `<uicontrol>`, note types) and *flags*
> the product-name violations; Scenario 9 is the **keyify mechanic** that actually
> *replaces* them with `keyref="product-name"` in bulk (code mode). So expect
> schematron to still report product-name findings after Scenario 8 — they clear in
> 9. The schematron rule matches direct `text()` only, so literals inside
> `<filepath>`/`<codeblock>` are deliberately left alone (the house rule keeps path
> and command literals verbatim).

## Scenario 9 — Keyify hardcoded product references

**Shows:** `list_keys`, the `keyify` refactor, key-space awareness, code mode.

> **Prompt:** *"Replace every hardcoded 'Audacity' in prose with the product-name
> key — leave shell commands and file paths alone. There's also a dangling keyref
> in installing-audacity; fix it too."*

The agent confirms the key with `list_keys`, keyifies the prose (skipping
`<codeblock>`/`<filepath>` per the house rules), uses **code mode** for the
repetitive replacement across files, and corrects the `produkt-version` typo to
`product-version`.

## Scenario 9b — Tidy the key space

**Shows:** `merge_keydefs`, `rename_key`, `inline_key`, `create_keydef`,
`resolve_key` — the rest of the key lifecycle (Scenario 9 only created keys).

`keydefs-glossary.ditamap` defines `product-version` a **second** time (a stale
`3.3`) — a shadowed duplicate that quietly drifts out of date.

> **Prompt:** *"Clean up the key space: remove the duplicate product-version
> definition, and tell me what product-name resolves to."*

`merge_keydefs` removes the shadowed `<keydef>` from the root map's closure (keeping
the winning `3.4` in `keydefs-product.ditamap`); `resolve_key product-name` reports a
key's effective value; `rename_key` renames a key and every `keyref`/`conkeyref` in
one reference-safe pass; `create_keydef` adds a new text key to a map; `inline_key`
is the inverse of keyify (replace a keyref with its resolved value). All preview with
`--dry-run`.

## Scenario 9c — Fix a key collision with key scopes (`@keyscope`)

**Shows:** the agent *introducing* DITA 1.3 **key scopes** to fix a silent
collision — `edit_map set-attr` + scope-aware `resolve_key --scope`.

`audacity-collection.ditamap` reuses three guides (`audacity-guide`,
`beginner-guide`, `podcaster-guide`), and each guide defines its own entry point
under the **same bare key**, `start-here`. Combined into one flat collection those
three definitions collide — first-definition-wins, so `start-here` silently
resolves to *only* the user guide's page; the beginner and podcaster landing pages
are shadowed and unreachable by key. (This is the *legitimate* counterpart to the
flat duplicate you removed in 9b: here you want all three, kept apart.)

> **Prompt:** *"In audacity-collection.ditamap the 'start-here' key only points to
> the user guide — each guide's own start page is getting shadowed. Give each guide
> its own key scope so start-here resolves correctly per guide, then show me where
> it lands for each."*

The agent confirms the collision (`list_keys` shows a single `start-here`), then
adds a key scope to each `<mapref>` with `edit_map set-attr`
(`--name keyscope --value userguide|beginner|podcaster`). Now the keys coexist as
`userguide.start-here`, `beginner.start-here`, `podcaster.start-here`, and
`resolve_key start-here --scope podcaster` lands on `podcast-production-workflow.dita`
while `--scope beginner` lands on `recording-your-first-track.dita` — one key name,
a different binding per scope, the DITA 1.3 way to reuse a sub-publication without
its keys clashing. (In-process resolution is exact when you name the scope; scope a
topic *inherits* from where a map places it is the engine's job at build time.)

Scoping doesn't just fix `resolve_key` — every key consumer is now scope-aware:
`list_keys` shows the fully-qualified names, `where_used` finds a scoped key's
references, `conref_audit` and the publication-set crawl resolve scoped targets, and
the DITA preview renders a scoped key's binding. So the fix propagates everywhere the
key is used, not just where it's defined.

## Scenario 10 — Govern conditional values with a subject scheme

**Shows:** the `dita-subject-schemes` skill + `list_subjects` +
`validate_conditions` + `rename_profile_value` — controlled-value governance, end
to end (discover → fix → prevent).

The guide profiles content with `@platform` and `@audience`, but **nothing defines
the allowed values**, so drift hides in plain sight: `installing-audacity.dita`
marks a step `platform="macos"`, while every `.ditaval` filters on `mac`. The Mac
build silently drops that step — no error anywhere. (Try a `mac-beginner.ditaval`
preview first: the macOS step is missing. That's the symptom.)

> **Prompt:** *"Our conditional values aren't governed. Introduce a subject scheme
> for @platform and @audience based on what our ditavals actually filter on, wire
> it into the maps, then find and fix any content that doesn't conform."*

The agent (guided by the **dita-subject-schemes** skill) does the real
governance workflow:

1. **Survey the contract** — the `*.ditaval` files filter on platform
   `windows`/`mac`/`linux` and audience `beginner`/`podcaster`. That's the intended
   vocabulary (deriving it from the *content* would just bake in the typo).
2. **Author** `controlled-values.ditamap` — a subjectScheme binding those values —
   and reference it from each deliverable's root map via `<mapref>`.
3. **Discover** — `validate_conditions` (or **Project ▸ Check Controlled Values**)
   flags the lone violation:
   `installing-audacity.dita:26 — @platform="macos" — did you mean "mac"?`
4. **Fix** — `rename_profile_value` changes `macos` → `mac` project-wide (ditavals
   included); re-validate → clean. The Mac build now includes the step. (The rename
   is scheme-aware: it would warn if you renamed *to* a value the scheme doesn't
   allow.)
5. **Prevent** — the scheme stays as a guardrail; it joins the publish-ready gate
   (Scenario 15), and `list_subjects controlled-values.ditamap` shows the governed
   vocabulary at any time. From now on, typing a `@platform` value in the editor
   offers the controlled values (windows/mac/linux) in the completion popup.

This is the payoff of governance: a silent, content-dropping bug becomes a visible,
one-line finding — and can never drift back unnoticed.

## Scenario 10b — Audit and normalize metadata

**Shows:** `metadata_audit` + `metadata_set` (field-preserving) + a required-metadata
policy + the done-gate.

The shared `.dogsbay/config.xml` carries a **metadata policy**: every **task** must
have an ISO `<created>` date, and an `<audience>` is recommended everywhere. But the
inherited topics have almost no prolog metadata — so the guide isn't publish-ready by
that standard.

> **Prompt:** *"Audit our metadata against the project policy, then backfill what's
> required."*

1. **Audit** — `metadata_audit` (or **Project ▸ Audit Metadata**) reports the task
   topics missing a required `<created>` date (errors) plus audience-recommended
   warnings across the guide, in the Project Validation pane.
2. **Normalize** — `metadata_set --fill created=2024-06-01` stamps a created date on
   every topic that lacks one, **field-preserving**: it adds the `<prolog><critdates>`
   skeleton where needed and leaves all other content + formatting untouched (preview
   with `--dry-run` first). Or **Project ▸ Normalize Metadata…**.
3. **Re-audit** → the required-metadata errors are gone (audience stays a soft
   recommendation). `project_health` now passes its metadata leg — part of the
   publish-ready gate.

> Export the policy for CI with **`metadata-export-schematron`** (or **Project ▸
> Export Metadata Policy as Schematron…**) to run the same checks in DITA-OT/oXygen.

## Scenario 10c — Generate keywords for search and relatedness

**Shows:** the `dita-keywords` skill — AI-generated metadata, grounded in the
project's own vocabulary.

The policy also **requires a `<keyword>`** on every topic (see `.dogsbay/config.xml`).
But unlike a `<created>` date, you can't fill keywords with a constant — they have to
come from each topic's content. This is the line between a *bulk fill* and *content
generation*.

> **Prompt:** *"Every topic needs subject keywords. Generate them from each topic's
> content — reuse the keywords we already use, don't invent synonyms."*

The **`dita-keywords`** skill first runs **`keyword_audit`** to learn the project's
existing vocabulary — distinct keywords with frequencies, topics with none, and
**near-duplicate spellings** (so it reuses "installation", not "setup"/"set up") —
then reads each topic and proposes 3–7 grounded subject terms, preferring any value
the subject scheme governs (Scenario 10), and writes them with
`metadata_set field=keyword mode=append` (field-preserving; `--dry-run` to preview).
Re-audit (Scenario 10b) and the required-`keyword` findings clear.

`keyword_audit` also emits the **relatedness signal** — its keyword **co-occurrence**
lists the topic pairs that share keywords, which is exactly the clustering input for
the relationship table in Scenario 11d (and pairs with `dita-shortdesc` from
Scenarios 2–4 as the searchability duo: the facets plus the snippet a search index
wants).

## Scenario 10d — Govern the DITA 1.3 constructs (index · glossary · conref push)

**Shows:** the DITA 1.3 standard-breadth audits — `index_audit`, `glossary_audit`,
`conref_push_audit`, `specialization_info` — via the `dita-index` / `dita-glossary` /
`dita-conref-push` skills. Three planted construct bugs the lexical checks miss.

> **Prompt:** *"Audit the DITA 1.3 constructs across the guide — the index, the
> glossary, and any conref-push — and fix what's broken."*

In single project-scale calls the agent surfaces (and fixes):

1. **Index** — `index_audit` finds the **dangling redirect** in
   `supported-audio-formats.dita`: `<index-see>codecs</index-see>` promises an index
   entry "codecs" that doesn't exist, so a reader following it lands nowhere (fix:
   point the see at a real entry, or add it). It also reports index **coverage** — most
   topics carry no index terms yet.
2. **Glossary** — `glossary_audit … --root-map audacity-guide.ditamap` flags the
   **undefined** `<abbreviated-form keyref="gl-bitdepth"/>` (a typo of `gl-bit-depth`,
   so it resolves to no glossentry) and the **unused** glossentries nothing references
   (`gl-normalization` / `gl-compression`) — dead weight or a missing link.
3. **Conref push** — `conref_push_audit` catches the **orphan** `conaction="pushbefore"`
   caution in `effects-reference.dita`: it has no sibling `conaction="mark"` to identify
   *where* to push, so the content goes nowhere (fix: add the mark with its `@conref`
   target). Because conref push only materializes at build, `validate_deep` confirms it.

`specialization_info <file>` rounds it out — it names a file's DOCTYPE, root element,
and `@class` generalization chain (e.g. `topic/topic → concept/concept`), confirming
the editor understands the project's specializations (including the bookmap's
`glossentry` glossary topics). Every one of these is a typed tool (CLI + MCP), so the
agent runs them headlessly without opening the files.

## Scenario 11 — Rename and move a topic

**Shows:** `where_used` + `rename_file` (reference-safe refactor).

> **Prompt:** *"Show me everywhere installing-audacity.dita is referenced, then
> rename it to installation.dita and update all references."*

`where_used` lists the map topicref and links; `rename_file` renames and rewrites
every reference. Run `check_links` after to confirm nothing dangles.

## Scenario 11b — Reorganize the map (edit topicrefs)

**Shows:** `edit_map` — structural map editing (move/insert/remove/set-attr),
reference-safe and formatting-preserving.

`topics/keyboard-shortcuts.dita` is a reference topic, but its topicref sits at the
bottom of **Recording and Editing** instead of under **Reference**.

> **Prompt:** *"keyboard-shortcuts is in the wrong section of audacity-guide.ditamap
> — move it under Reference."*

The agent runs `edit_map move --ref keyboard-shortcuts --parent reference`. The
topicref is cut and pasted verbatim (its formatting and attributes survive); the
rest of the map — comments, the reltable, indentation — is untouched. The same tool
also **inserts** a topicref (`insert --parent reference --href … --navtitle …`),
**removes** one (`remove --ref …`, warning if the topic is still referenced
elsewhere), and re-attributes (`set-attr --ref … --name toc --value yes`). Add
`--dry-run` to preview first.

## Scenario 11c — Surgical reference refactors

**Shows:** `rename_element_id`, `retarget`, `delete_file` — single-target edits that
rewrite references project-wide (the same reverse-index that powers Scenario 11).

> **Prompt:** *"Rename the `backup-warning` id to `save-warning` everywhere it's
> conref'd, and show me what would break if I deleted keyboard-shortcuts.dita."*

`rename_element_id` renames an element id and every `#fragment` that points at it
(here the conrefs in `trimming-audio.dita` and `removing-background-noise.dita`);
`retarget` redirects every reference from one file to another in one pass
(consolidating duplicates); `delete_file --dry-run` reports the inbound references a
delete would strip or orphan — the blast radius — before you commit. Each previews
with `--dry-run` / `where_used`.

## Scenario 11d — Relate topics with a relationship table

**Shows:** the `dita-reltables` skill — `reltable_audit` + `edit_reltable` to author
governed related-links in one place, plus the **Edit Relationship Tables** grid.

`audacity-guide.ditamap` already has a `<reltable>` (concept ↔ task ↔ reference), but
the **editing-techniques** concept isn't related to anything.

> **Prompt:** *"Audit the relationship table and show the links it generates, then
> relate editing-techniques to its task and reference topics."*

The **`dita-reltables`** skill grounds the *relatedness judgment* in data, not
guesswork: it reads the **`keyword_audit`** co-occurrence (Scenario 10c) to see which
topics share subjects, proposes a concept/task/reference row (here
editing-techniques ↔ trimming-audio ↔ supported-audio-formats), and confirms with
you. `reltable_audit` validates every cell (resolves, targets a topic not a map,
column type matches) and **previews the per-topic related-links** the table generates
— the DITA-OT matrix. `edit_reltable add-row` + `add-target` wires the row in,
formatting-preservingly (dry-run to preview). In the editor, **Project ▸ Edit
Relationship Tables…** opens the same table as a grid.

A reltable keeps relationships in **one place** (the map) instead of scattered
`<related-links>` in every topic — and the keyword work in 10c is what makes the
agent's row proposals grounded rather than guessed.

## Scenario 11e — Undo a whole turn with `/revert`  [editor UI]

**Shows:** per-turn checkpoint + one-command revert — the trust that lets you say
"yes" to a multi-file refactor.

A reference-safe refactor (Scenarios 11–11c) touches many files at once: the map,
the links, the conrefs. That's exactly the kind of change you want to be able to
take back cleanly. Run one — e.g. *"rename installation.dita back to
installing-audacity.dita and update all references"* — approve it, then:

> **Type:** `/revert`

The agent reports *"Reverted the last turn — restored N files"*, every file-system
change from that turn is rolled back on disk, and open editors refresh to match.
Behind the scenes each turn snapshots the files a tool is about to change
(copy-on-write) and `/revert` restores them — but **only the files whose content
actually changed**, so a turn that merely *read* files, or edits you *denied* at the
approval gate, revert to nothing (no spurious "restored", no touched timestamps).

> **In-buffer vs. on-disk.** `/revert` undoes **file-system** changes (new files,
> renames, multi-file refactors) that aren't on the editor's undo stack. A
> single-buffer edit like `replace_selection` (Scenario 1) is undone the normal way
> with **Ctrl+Z** — and crucially, `/revert` will **never** clobber your *unsaved*
> manual edits in an open file, because a buffer-only change never altered disk.

This is the safety net under Part C: the project-scale tools are powerful precisely
because a whole turn is one undoable unit.

## Scenario 12 — Split an overgrown topic

**Shows:** `split_topic` (structural refactor).

`topics/editing-techniques.dita` crams four techniques (Trimming, Fading,
Normalizing, Removing Noise) into one concept.

> **Prompt:** *"editing-techniques.dita is too broad — split each section into its
> own topic and wire them into the map under Recording and Editing."*

## Scenario 13 — Finish an unwritten task (authoring)

**Shows:** content generation with correct DITA structure.

`topics/burning-an-audio-cd.dita` is a stub — title and context, no steps.

> **Prompt:** *"This task is a stub. Write the steps for exporting a WAV and
> burning it to an audio CD on Windows and macOS. Follow our house style."*

The agent writes a proper `<steps>` structure (using `<uicontrol>`, the product
key, and `@platform` conditions). Approve, then **render preview** to see it.

## Scenario 14 — Validate every deliverable

**Shows:** `validate_deliverables` + `get_project` — multi-output validation.

This project ships several outputs, defined in `project.json`: the **full** guide
(`audacity-guide.ditamap`), a **beginner** guide for **mac** and **windows**
(`beginner-guide.ditamap` + a `.ditaval` each), and a **podcaster** guide for
**linux** (PDF).

> **Prompt:** *"Validate every deliverable and tell me which outputs are affected
> by each problem."*

`validate_deliverables` validates each deliverable's filtered publication set and
reports **per output** — so a broken *shared* topic shows up against **every**
output that ships it (e.g. `installing-audacity.dita` is flagged under `full`
*and* both beginner builds). `get_project` tells the agent the deliverables and
conditions up front, so it doesn't go hunting.

## Scenario 14b — Deliverables in the editor: switch · deep-validate · publish  [editor UI]

**Shows:** the editor's deliverable awareness — the status-bar selector, DITA-OT
engine validation, and filtered publish. These read `project.json`'s deliverables
directly (the same ones the agent sees), no prompts needed.

The deliverables in `project.json` (`full` · `beginner-mac` · `beginner-windows`
· `podcaster-linux`) drive three editor features:

1. **Status-bar selector.** Bottom-left shows the active deliverable. The shared
   default is `full` (from `.dogsbay/config.xml`), but this checkout's personal
   `.dogsbay/local.xml` selects **`beginner-mac`** — so you start there, while a
   teammate without that local file would start on `full`. Click the selector to
   switch; picking a deliverable makes its map, `.ditaval`, transtype, and params
   the active "current map · profile" everywhere below. (Use **Project → Save
   Project Settings…** to write the shared `.dogsbay/config.xml`.)

2. **Deep validate with DITA-OT** (requires the DITA-OT framework imported —
   *File → Import Framework*). Beyond the static `validate_project`, this runs the
   real preprocessing pipeline, catching keyref/conref resolution and filtered-out
   content errors:
   - **Project → Validate with DITA-OT — Current Map** validates the active
     deliverable (with its DITAVAL); results land in the **Project Validation**
     tab, click-to-open.
   - **Project → Validate with DITA-OT — All Deliverables** validates every output.

3. **Filtered publish + build.** Publishing from the DITA Map Explorer now honors
   the active deliverable: it applies the deliverable's DITAVAL (so a `beginner-mac`
   build is actually filtered) and its publication params (e.g. `nav-toc`), and
   defaults the transtype + output. **Project → Build Deliverables…** builds every
   deliverable to a chosen folder. Pick `beginner-mac`, publish, and the
   Windows-only and advanced steps are filtered out of the result.

4. **Manage the deliverable set.** **Project → Manage DITA Deliverables…** (or the
   status-bar switcher → *Manage Deliverables…*) lists every deliverable across the
   project files, marks the active one, and lets you **add / edit / delete / set
   active**. The editor form picks the **input map** and **DITAVAL** from dropdowns
   of the project's `.ditamap`/`.ditaval` files (or Browse…), sets the transtype and
   output, and edits **publication params** in a `value`/`href`/`path` table — all
   written field-preservingly to `project.json`. The active deliverable persists
   across restarts (in the gitignored `.dogsbay/local.xml`).

> Agent equivalents: the **`validate_deep`** and **`build_deliverables`** MCP tools
> run the same DITA-OT validation/build headlessly (`bin/dogsbay validate-ot` /
> `bin/dogsbay build <root> [deliverable]` on the CLI).

## Scenario 14c — Variants from one map (branch filtering)

**Shows:** DITA 1.3 **branch filtering** (`<ditavalref>`) + `list_branches` — one map
producing several filtered deliverable variants instead of near-duplicate
project.json entries.

`installing-audacity.dita` carries `platform="windows|macos|linux"` conditions, and
today the project ships them as **separate deliverables** (`beginner-mac`,
`beginner-windows` …) that differ only by their DITAVAL. `installation-variants.ditamap`
expresses the same split *inside one map*: the install topic has three sibling
`<ditavalref>`s (windows / macOS / linux), each with a `dvrResourcePrefix`, so DITA-OT
duplicates and filters the topic into `win-` / `mac-` / `linux-` variants from a single
source.

> **Prompt:** *"How many deliverable variants does installation-variants.ditamap
> produce, and what does each filter on? I want one map that fans out to all three
> platforms instead of separate per-platform deliverables."*

`list_branches installation-variants.ditamap` reports the three variants and each
one's DITAVAL. In the editor the variants appear **indented under the deliverable in
the status-bar popup** (select one to deep-validate / build / preview just that
platform), as a **Branch dropdown in the DITA preview** (see the filtered topic), and
as italic **branch:** leaves under the topicref in the **Map Explorer**. The actual
duplicated, platform-filtered output is produced by DITA-OT at build; in-process the
editor enumerates, previews, and validation-scopes the branches.

Then prove which variant a problem belongs to:

> **Prompt:** *"Deep-validate installation-variants.ditamap with DITA-OT and tell me
> which platform variant each error belongs to."*

`validate_deep` (editor: **Project ▸ Validate with DITA-OT**) builds the branch-filtered
map; the install topic's planted errors (the invalid `<x>` and `note type="tipp"`)
recur once per generated variant, and each diagnostic in the **Project Validation
pane** is tagged **`[branch: win-]` / `[branch: mac-]` / `[branch: linux-]`** — DITA-OT
names the generated resources with the `dvrResourcePrefix`, and the editor attributes
each message back to its branch (best-effort, by that affix). So a failure in one
platform's variant is immediately attributable, not lost in a flat error list.

> **Try it in the editor:** open `topics/installing-audacity.dita` in a **DITA preview**
> tab, set the context map to `installation-variants.ditamap`, and switch the **Branch**
> dropdown between *win-* / *mac-* / *linux-* — the platform-conditioned steps appear and
> disappear as each branch's DITAVAL is applied.

---

# Part D — The gate

## Scenario 15 — The capstone: "make it publish-ready"

**Shows:** multi-tool autonomy, code mode, sessions, and a **grounded done-gate**.

> **Use a capable model** (Claude Sonnet/Opus or a GPT-4-class model) and start
> fresh with `/new`. A long autonomous task is more than a small/fast model will
> reliably finish.

> **Prompt:** *"Make this entire guide publish-ready: fix all validation errors,
> broken links and conrefs, missing descriptions, hardcoded product names,
> markup style, and conditional values that don't conform to our subject scheme.
> For bulk, uniform edits write a script (code mode) rather than opening every
> file; use `validate_project` and `validate_conditions` for validation. When you
> believe you're done, run `project_health` and show me the result — I'll consider
> it done only when it reports clean."*

The agent chains survey → validate → links → conref audit → house style → keyify
→ conditions, then **runs `project_health` and shows a clean report as proof**.
It can't credibly claim "publish-ready" without it: `project_health` is
comprehensive — it machine-checks validation, references, keys, **and conref
element ids** in one pass — so a clean result actually *means* clean. Use **Allow
for session** on the first edit so the batch flows; `/compact` if it runs long.

> **What the gate does and doesn't cover.** `project_health` is the structural gate
> (validation · references · keys · conref/keyref element ids · required metadata).
> *House style* (`schematron_project house-style.sch`, Scenario 8) and *controlled
> values* (`validate_conditions`, Scenario 10) are **separate** checks the agent runs
> alongside it — they're not folded into `project_health`. "Publish-ready" here means
> all three are clean, which is why the verify list below runs each one.

**Verify it yourself — agent and human share one source of truth:**

- **XML → Validate Project** in the editor → the Project Validation tab should be
  empty (every topic valid);
- `bin/dogsbay project-health . --map audacity-guide.ditamap` from a terminal
  should report clean;
- `bin/dogsbay validate-conditions . -S controlled-values.ditamap` should report
  no controlled-value violations (the subject scheme governs `@platform`/`@audience`);
- spot-check: no `<b>`, no literal "Audacity" in prose, no `platform="macos"`, no
  `backup-warningX`, no `produkt-version`, every topic has a `<shortdesc>`.

When done, the session is saved — close the app, reopen, **Sessions → Resume**,
and the conversation (and history) is back.

---

## Capability checklist (what the demo proves)

| Capability | Scenario |
|---|---|
| Lazy startup / providers / Ollama / ChatGPT login | 0 |
| Slash commands (`/help`, `/skills`, `/provider`, `/model`, `/compact`, `/new`) | 0, 15 |
| Selection context (act on highlighted text) | 1 |
| Right-click **AI** actions on a selection (incl. DITA: shortdesc/wrap), diff-reviewed | 1, 2 |
| Tool approval shows the actual **before/after diff** (with provider · model · cost) | 1 |
| Authoring new structure (shortdesc, steps) | 2, 13 |
| Author view — WYSIWYG block editing (`author_outline`/`author_insert_block`/`author_set_text`) | 3b |
| Content-quality judgment — SEO descriptions/abstracts (`dita-shortdesc` skill) | 2, 3, 4 |
| Keyword generation + vocabulary audit (`dita-keywords` skill, `keyword_audit` co-occurrence) | 10c |
| DITA 1.3 construct audits — index / glossary / conref-push / specialization (`index_audit`, `glossary_audit`, `conref_push_audit`, `specialization_info`) | 10d |
| **Why batch: per-file doesn't scale / don't kill the context** | 4 |
| Code mode (script/XSLT for bulk edits) | 4, 9, 15 |
| Project-wide survey in one call (`project_health`) | 5, 15 |
| Project-wide search + XPath (`search_project`, `xpath_query`) | 5b |
| Bulk validation (`validate_project`) + editor Project Validation tab | 6 |
| Auto edit→validate loop (agent self-corrects per edit) + **Fix with AI** on a marker | 6 |
| Broken-link repair + conref **element-id** audit | 7 |
| Content reuse warehouse (`extract_conref`, `inline_conref`) | 7b |
| House style as policy (`schematron_project` + `house-style.sch`) | 8 |
| Keyify + key-space awareness + dangling key | 9 |
| Key lifecycle (`merge_keydefs`, `rename_key`, `inline_key`, `create_keydef`, `resolve_key`) | 9b |
| Key scopes (`@keyscope`) — fix a key collision via `edit_map`; scope-aware `resolve_key --scope` / `list_keys` / `where_used` / preview | 9c |
| Controlled-value governance (subject scheme + `validate_conditions` + `list_subjects` + `rename_profile_value`) | 10 |
| Reference-safe rename/move (`where_used`, `rename_file`) | 11 |
| Structural map editing (`edit_map` move/insert/remove/set-attr) | 11b |
| Relationship tables (`dita-reltables` skill: `reltable_audit`, `edit_reltable`, grid editor) | 11d |
| Surgical reference refactors (`rename_element_id`, `retarget`, `delete_file`) | 11c |
| Per-turn checkpoint + `/revert` (undo a whole turn's file changes) | 11e |
| Split topic (`split_topic`) | 12 |
| Per-deliverable validation (`validate_deliverables`, `get_project`) | 14 |
| Status-bar deliverable selector (active map · profile) | 14b |
| Manage deliverables (add/edit/delete, params, persisted active) | 14b |
| Deep validation with DITA-OT (engine tier) + `validate_deep` | 14b |
| Filtered publish + build deliverables (`build_deliverables`) | 14b |
| Branch filtering (DITA 1.3 `ditavalref`) — `list_branches`, branch preview, per-branch deep-validate + `[branch:]` attribution | 14c |
| Shared project settings (`.dogsbay/config.xml`) + personal `local.xml` | 14b |
| Grounded done-gate (machine-checked "publish-ready") | 15 |
| Bundled DITA skills + project custom skill (incl. `dita-subject-schemes`) | 0, 8, 10 |
| Context file (`AGENTS.md`), tool approval, sessions resume | all, 15 |

## Reset for another run

```bash
git restore . && git clean -fd      # back to the broken starting point
```

`AGENTS.md`, `project.json`, `.dogsbay/config.xml`, `house-style.sch`, and
`.xagent/skills/` are committed, so the reset keeps them — only topic content
reverts. `.dogsbay/local.xml` is gitignored, so it also survives `git clean -fd`.

## Tip: reset between scenarios for an isolated showcase

Some fixes overlap (validating in Scenario 6 also clears errors that Scenario 9
or 15 would otherwise touch). For a clean per-feature showcase, reset between
scenarios. For the cumulative story, run straight through to the capstone.
