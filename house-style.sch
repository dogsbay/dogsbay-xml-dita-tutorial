<?xml version="1.0" encoding="UTF-8"?>
<!--
  Audacity guide house style as machine-checkable rules.
  Run across the project with:  dogsbay schematron-project . house-style.sch
  (or ask the agent: "run our house-style rules and fix the violations").

  Design notes:
   - The product-name / extension tests match direct text() only, so a literal
     inside a descendant <filepath>/<codeblock> (e.g.
     <filepath>C:\Program Files\Audacity</filepath>) does NOT trip the enclosing
     <p> — the house rule deliberately leaves such literals alone.
   - Coverage spans the places hardcoded names actually hide: prose <p>, list
     items <li>, table cells <entry>, definitions <dd>, shortdescs, and step
     commands <cmd>. One pattern per element keeps each rule readable and its
     report message specific.
-->
<schema xmlns="http://purl.oclc.org/dsdl/schematron">
  <title>Audacity User Guide house style</title>

  <!-- every topic needs a shortdesc (one pattern per topic type) -->
  <pattern id="shortdesc-topic"><rule context="topic"><assert test="shortdesc">Every topic needs a shortdesc (a one- or two-sentence description).</assert></rule></pattern>
  <pattern id="shortdesc-concept"><rule context="concept"><assert test="shortdesc">Every topic needs a shortdesc (a one- or two-sentence description).</assert></rule></pattern>
  <pattern id="shortdesc-task"><rule context="task"><assert test="shortdesc">Every topic needs a shortdesc (a one- or two-sentence description).</assert></rule></pattern>
  <pattern id="shortdesc-reference"><rule context="reference"><assert test="shortdesc">Every topic needs a shortdesc (a one- or two-sentence description).</assert></rule></pattern>

  <pattern id="ui-labels-use-uicontrol">
    <rule context="b">
      <report test="true()">Use uicontrol for UI labels (and drop decorative bold); do not use b.</report>
    </rule>
  </pattern>

  <!-- no hardcoded product name; direct text() only (filepath/codeblock literals exempt) -->
  <pattern id="pn-p"><rule context="p"><report test="text()[contains(., 'Audacity')]">Do not hardcode the product name "Audacity" in prose; use a keyword with keyref="product-name".</report></rule></pattern>
  <pattern id="pn-li"><rule context="li"><report test="text()[contains(., 'Audacity')]">Do not hardcode the product name "Audacity" in a list item; use keyref="product-name".</report></rule></pattern>
  <pattern id="pn-entry"><rule context="entry"><report test="text()[contains(., 'Audacity')]">Do not hardcode the product name "Audacity" in a table cell; use keyref="product-name".</report></rule></pattern>
  <pattern id="pn-dd"><rule context="dd"><report test="text()[contains(., 'Audacity')]">Do not hardcode the product name "Audacity" in a definition; use keyref="product-name".</report></rule></pattern>
  <pattern id="pn-shortdesc"><rule context="shortdesc"><report test="text()[contains(., 'Audacity')]">Do not hardcode the product name "Audacity" in a shortdesc; use keyref="product-name".</report></rule></pattern>
  <pattern id="pn-cmd"><rule context="cmd"><report test="text()[contains(., 'Audacity')]">Do not hardcode the product name "Audacity" in a step command; use keyref="product-name".</report></rule></pattern>

  <!-- no hardcoded project extension; use keyref="project-extension" -->
  <pattern id="ext-p"><rule context="p"><report test="text()[contains(., '.aup3')]">Do not hardcode ".aup3"; use keyref="project-extension".</report></rule></pattern>
  <pattern id="ext-li"><rule context="li"><report test="text()[contains(., '.aup3')]">Do not hardcode ".aup3"; use keyref="project-extension".</report></rule></pattern>
  <pattern id="ext-entry"><rule context="entry"><report test="text()[contains(., '.aup3')]">Do not hardcode ".aup3"; use keyref="project-extension".</report></rule></pattern>
  <pattern id="ext-dd"><rule context="dd"><report test="text()[contains(., '.aup3')]">Do not hardcode ".aup3"; use keyref="project-extension".</report></rule></pattern>

  <!-- leftover authoring markers must not ship -->
  <pattern id="todo-p"><rule context="p"><report test="contains(., 'TODO') or contains(., 'FIXME') or contains(., 'TBD')">Remove authoring markers (TODO/FIXME/TBD) before publishing.</report></rule></pattern>
  <pattern id="todo-li"><rule context="li"><report test="contains(., 'TODO') or contains(., 'FIXME') or contains(., 'TBD')">Remove authoring markers (TODO/FIXME/TBD) before publishing.</report></rule></pattern>
  <pattern id="todo-cmd"><rule context="cmd"><report test="contains(., 'TODO') or contains(., 'FIXME') or contains(., 'TBD')">Remove authoring markers (TODO/FIXME/TBD) before publishing.</report></rule></pattern>
  <pattern id="todo-draftcomment"><rule context="draft-comment"><report test="true()">Remove draft-comment before publishing.</report></rule></pattern>
  <pattern id="todo-reqcleanup"><rule context="required-cleanup"><report test="true()">Remove required-cleanup before publishing.</report></rule></pattern>

  <!-- a step command must say something (conref'd steps exempt) -->
  <pattern id="cmd-not-empty"><rule context="cmd"><assert test="normalize-space(.) != '' or @conref or @conkeyref or parent::step/@conref or parent::step/@conkeyref">A cmd must have text, or pull content via conref.</assert></rule></pattern>

  <pattern id="note-type-allowed">
    <rule context="note[@type]">
      <assert test="@type = 'note' or @type = 'tip' or @type = 'important' or @type = 'caution' or @type = 'warning' or @type = 'attention' or @type = 'danger' or @type = 'fastpath' or @type = 'remember' or @type = 'restriction' or @type = 'trouble' or @type = 'other'">note type is not an allowed DITA value.</assert>
    </rule>
  </pattern>

  <pattern id="step-has-cmd">
    <rule context="step">
      <assert test="cmd">Every step must contain a cmd.</assert>
    </rule>
  </pattern>
</schema>
