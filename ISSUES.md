# Planted issues — the answer key

Every problem deliberately present in this project, what's wrong, and how the
agent fixes it. (Maps to the scenarios in `DEMO.md`.) Some issues are inherited
from the source content; most were planted for the demo.

## Missing / weak descriptions  → Scenarios 2, 3, 4

| File(s) | Problem | Fix |
|---|---|---|
| nearly all topics | no `<shortdesc>` at all | add a concise one-sentence description after the title |
| `topics/what-is-audacity.dita` | bland placeholder shortdesc ("This page is about the software…") | rewrite SEO-friendly (lead with the product, <155 chars) |

The house-style rule "every topic needs a shortdesc" is machine-checkable —
`schematron_project house-style.sch` lists every topic missing one (Scenario 8),
which is also how the batch fix in Scenario 4 finds its targets.

## Validation errors  → Scenario 6 (`validate_project`)

| File | Problem | Fix |
|---|---|---|
| `topics/installing-audacity.dita` | invalid element `<x>TODO…</x>` in `<context>` | remove it |
| `topics/installing-audacity.dita` | invalid `<note type="tipp">` (not a valid note type) | `type="tip"` |
| `topics/trimming-audio.dita` | invalid element `<x></x>` in `<context>` | remove it |

## Broken links & conrefs  → Scenario 7 (`check_links`, `conref_audit`)

| File | Problem | Fix |
|---|---|---|
| `topics/recording-your-first-track.dita` | related-link to `digital-audio-basics.dita` (no such file) | `what-is-digital-audio.dita` |
| `topics/removing-background-noise.dita` | conref to `#common-notes/backup-warningX` (id is `backup-warning`) | drop the trailing `X` |

## Content reuse  → Scenario 7b (`extract_conref`, `inline_conref`)

Not an error — a *reuse opportunity*. The agent demonstrates warehousing.

| Target | Opportunity | Tool |
|---|---|---|
| `topics/recording-your-first-track.dita` `#quiet-room-tip` | a useful inline tip that belongs in the shared warehouse so other topics can reuse it | `extract_conref … quiet-room-tip --to shared/common-notes.dita` (and `inline_conref` for the inverse) |

## House style  → Scenario 8 (`schematron_project house-style.sch` + `audacity-house-style` skill)

| File(s) | Problem | Fix |
|---|---|---|
| `what-is-audacity`, `trimming-audio`, `podcast-production-workflow` | `<b>` used for UI labels / emphasis | UI controls → `<uicontrol>`; decorative emphasis is a judgment call |
| `editing-techniques`, `effects-reference`, `exporting-audio`, `installing-audacity`, `keyboard-shortcuts`, `supported-audio-formats` | hardcoded "Audacity" in prose | keyref `product-name` (see Keys) |
| `topics/installing-audacity.dita` | `note type="tipp"` | allowed note type (`tip`) |

## Keys  → Scenario 9 (`keyify`, `list_keys`)

| File(s) | Problem | Fix |
|---|---|---|
| `exporting-audio`, `supported-audio-formats`, `keyboard-shortcuts`, `effects-reference`, `editing-techniques`, `installing-audacity`, `glossary/g-waveform`, `glossary/g-clipping` | hardcoded "Audacity" (and `.aup3`) in prose | keyref `product-name` / `project-extension`; **leave** shell commands & `<filepath>` literals |
| `topics/installing-audacity.dita` | dangling `keyref="produkt-version"` (typo) | `product-version` |

## Key space  → Scenario 9b (`merge_keydefs`, key lifecycle)

| Target | Problem | Fix |
|---|---|---|
| `keydefs-glossary.ditamap` | defines `product-version` a second time (stale `3.3`) — a shadowed duplicate of the `3.4` in `keydefs-product.ditamap` | `merge_keydefs audacity-guide.ditamap` removes the shadowed `<keydef>` |

## Key collision  → Scenario 9c (`@keyscope`, `edit_map`, `resolve_key --scope`)

| Target | Problem | Fix |
|---|---|---|
| `audacity-collection.ditamap` | each reused guide defines its own `start-here` keydef (`audacity-guide` → `what-is-audacity`, `beginner-guide` → `recording-your-first-track`, `podcaster-guide` → `podcast-production-workflow`); combined **flat**, they collide — first-wins, so `start-here` resolves only to the user guide and the other two landing pages are shadowed | give each `<mapref>` a key scope: `edit_map set-attr --ref /1/1 --name keyscope --value userguide` (and `/2/1` → `beginner`, `/3/1` → `podcaster`). Keys then coexist as `userguide.start-here` / `beginner.start-here` / `podcaster.start-here`; `resolve_key start-here --scope podcaster` → `podcast-production-workflow.dita` |

The legitimate counterpart to the *flat* duplicate removed in 9b: there you delete a
shadow you don't want; here you scope shadows you *do* want (same key, three bindings).

## Conditional values  → Scenario 10 (subject scheme + `validate_conditions` + `rename_profile_value`)

Conditional content is **ungoverned**: `@platform`/`@audience` values are free text,
with no subject scheme defining what's allowed — so drift hides. The scenario has the
agent *introduce* governance (it generates `controlled-values.ditamap` from the
DITAVAL contract — see the `dita-subject-schemes` skill), then `validate_conditions`
surfaces the drift and `rename_profile_value` fixes it.

| File | Problem | Fix |
|---|---|---|
| `topics/installing-audacity.dita` | step marked `platform="macos"`; the **deliverable** ditavals (`mac-beginner` / `windows-beginner` / `linux-podcaster`) filter on `mac`, so the Mac build silently drops the step | author a subject scheme (`@platform` ∈ windows/mac/linux), then `rename_profile_value` `macos` → `mac` |
| `filters/platform-windows.ditaval`, `filters/platform-linux.ditaval` | their `<prop att="platform" val="macos" action="exclude"/>` exclude rules **also** use the non-canonical `macos` — the project mixes `mac` and `macos` for the same platform across its own filters (the branch-filter ditavals used by `installation-variants.ditamap`) | the same `rename_profile_value macos → mac` rewrites these too — it edits matching `<prop val>` entries in `.ditaval` files, not just element attributes; once the subject scheme exists, `validate_conditions` flags these DITAVAL entries as well |

So the `macos` drift lives in **three** places, not one: the content step plus those
two branch-filter ditavals. (`installation-variants.ditamap` references
`filters/platform-macos.ditaval` by *filename* — that's not a profiling value and is
not drift.) `rename_profile_value` fixes all three in one reference-safe pass.

There is intentionally **no** `controlled-values.ditamap` in the starting project —
the agent creates it. Once it exists, the scheme guards every deliverable (it joins
the publish-ready gate in Scenario 15).

## Refactors  → Scenarios 11–12

| Target | Task | Tool |
|---|---|---|
| `topics/installing-audacity.dita` | rename → `installation.dita`, update all refs | `where_used`, `rename_file` |
| `topics/editing-techniques.dita` | overgrown — 4 sections to split into topics | `split_topic` |

## Map structure  → Scenario 11b (`edit_map`)

| Target | Problem | Fix |
|---|---|---|
| `audacity-guide.ditamap` | `keyboard-shortcuts.dita` topicref (id `keyboard-shortcuts`) is the last child of **Recording and Editing** — it belongs under **Reference** (id `reference`) | `edit_map move --ref keyboard-shortcuts --parent reference` |

## Relationships  → Scenario 11d (`reltable_audit`, `edit_reltable`)

| Target | Opportunity | Tool |
|---|---|---|
| `audacity-guide.ditamap` reltable | `editing-techniques.dita` (concept) isn't related to any task/reference — a missing concept/task/reference row | `edit_reltable add-row` + `add-target` (editing-techniques / trimming-audio / supported-audio-formats); `reltable_audit` previews the generated links |

## Unfinished content  → Scenario 13 (authoring)

| File | Problem | Fix |
|---|---|---|
| `topics/burning-an-audio-cd.dita` | stub — `<context>` only, no `<steps>` | write the steps |

## Deliverables  → Scenario 14 (`validate_deliverables`)

`project.json` defines four outputs (full / beginner-mac / beginner-windows /
podcaster-linux). The shared invalid topics above (`installing-audacity`,
`trimming-audio`) surface under **every** deliverable that ships them — that's the
point of validating per output rather than per file.

## Branch filtering  → Scenario 14c (`<ditavalref>`, `list_branches`)

Not a planted defect — a capability showcase. `installation-variants.ditamap` puts
three sibling `<ditavalref>`s (windows / macOS / linux, each with a
`dvrResourcePrefix`) on the `installing-audacity.dita` topicref, so one map fans out
to three platform-filtered variants — the DITA 1.3 alternative to the separate
per-platform deliverables in `project.json`. The answer the agent should give:
`list_branches installation-variants.ditamap` → three variants (`win-` /
`mac-` / `linux-`), each filtering on its platform DITAVAL. The duplicated output is
DITA-OT's at build; in-process the editor enumerates / previews / validation-scopes them.
Deep-validating the map (`validate_deep`) re-surfaces the install topic's planted
errors (the invalid `<x>` and `note type="tipp"` from Scenario 6) once per generated
variant, each tagged `[branch: win-/mac-/linux-]` in the Project Validation pane — so
the agent can say which platform variant a failure belongs to.

## DITA 1.3 constructs  → Scenario 10d (`index_audit`, `glossary_audit`, `conref_push_audit`)

| File | Problem | Fix |
|---|---|---|
| `topics/supported-audio-formats.dita` | `<indexterm>compression<index-see>codecs</index-see></indexterm>` — the see redirects to "codecs", which is no index entry anywhere (a reader following it finds nothing) | point the see at a real index entry, or add a "codecs" entry — `index_audit` flags it |
| `topics/supported-audio-formats.dita` | `<abbreviated-form keyref="gl-bitdepth"/>` — a typo of the key `gl-bit-depth`, so it resolves to no glossentry | correct to `gl-bit-depth`; `glossary_audit --root-map …` flags it as undefined |
| `keydefs-glossary.ditamap` / glossary | the `gl-clipping` glossentry is defined but never referenced by any `abbreviated-form`/`term` (the `gl-normalization`/`gl-compression` entries *are* used, from `podcast-production-workflow.dita`) | reference it from a topic that discusses the term (e.g. `what-is-digital-audio.dita`), or remove — `glossary_audit` and `project_health` (unused keys) report it |
| `topics/effects-reference.dita` | `<note conaction="pushbefore">` with **no** sibling `conaction="mark"` — the conref push has nothing to identify where to push, so the caution goes nowhere | add a `<note conaction="mark" conref="editing-techniques.dita#…"/>` sibling; `conref_push_audit` flags the orphan |

These are DITA 1.3 construct bugs the lexical checks (`check_links`, `validate_project`)
miss — the dedicated audits surface them. `specialization_info` is informational (no
defect): it reports a file's DOCTYPE / root / `@class` chain.

## Metadata  → Scenario 10b (`metadata_audit` + `metadata_set`)

| Scope | Problem | Fix |
|---|---|---|
| every `<task>` topic (6) | the policy requires a `<created>` date; the inherited topics have no prolog metadata | `metadata-set --fill created=<date>` (field-preserving) |
| all topics | the policy requires a `<keyword>`; keywords must be **derived from content**, not a constant | the `dita-keywords` skill generates them from each topic (Scenario 10c), reusing the existing vocabulary |
| all topics | `<audience>` is recommended (warning, non-blocking) | optional `metadata-set --fill audience=…` |

The required-metadata policy lives in `.dogsbay/config.xml`. The missing required
`<created>` dates and `<keyword>`s fail the `project_health` metadata leg until
addressed — `created` by a bulk fill (10b), `keyword` by content generation (10c).

---

**Note on validation:** structural/DTD errors (invalid elements/attributes,
dangling keyrefs, broken conrefs) are reported by the editor's DITA grammar (and
by `validate_project` / `project_health`) when you run the agent in DogsBay XML.
All files are XML **well-formed** — the project loads; the issues are
semantic/DITA-level, which is exactly what the agent and its skills are built to
fix. Prolog metadata is also sparse (only `what-is-audacity.dita` has it) — which the
metadata policy turns into a real audit + bulk-normalize beat (Scenario 10b).
