---
name: audacity-house-style
description: Apply the Audacity guide's house style to DITA topics — use product keys instead of hardcoded names, semantic UI elements instead of bold, conref shared content, and sentence-case titles. Use when asked to apply house style, clean up a topic, or make content consistent.
---

# Audacity guide house style

When asked to apply house style (or to "clean up" / "make consistent") to one or
more DITA topics, apply these rules and re-validate afterwards:

1. **Product references → keys.** Replace any literal "Audacity", the version
   number, the download URL, or the project extension (`.aup3`) with the matching
   key:
   - `Audacity` → `<keyword keyref="product-name"/>`
   - version (e.g. `3.4`) → `<keyword keyref="product-version"/>`
   - download URL → `<keyword keyref="download-url"/>`
   - `.aup3` → `<keyword keyref="project-extension"/>`
   Keys are defined in `keydefs-product.ditamap`. Use `list_keys` to confirm.
   Do **not** replace literals inside `<codeblock>` or `<filepath>` examples
   (e.g. a shell command or `C:\Program Files\Audacity`).

2. **UI labels → `<uicontrol>`.** Replace `<b>Record</b>`-style highlighting of
   buttons, menu items, and field names with `<uicontrol>Record</uicontrol>`.
   Multi-level menu paths use
   `<menucascade><uicontrol>…</uicontrol>…</menucascade>`.

3. **Deduplicate via conref.** If a step or note is copied verbatim from
   `shared/common-steps.dita` or `shared/common-notes.dita`, replace the copy with
   a `conref` to the shared element instead of repeating it.

4. **Titles** are sentence case.

5. After editing, **validate** each changed topic and fix any errors before
   reporting done.

Make the minimal edits needed; preserve meaning and surrounding markup.
