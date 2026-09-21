# The stage gate

`scripts/check-stage.sh` is the check every tutorial stage branch must pass
before it is committed. It is also a useful one-shot health check for any DITA
project folder.

## What it runs

| Step | Command | Proves |
|------|---------|--------|
| 1 | `dogsbay-xml validate-project <root>` | every `.dita` and `.ditamap` validates against its DOCTYPE |
| 2 | `dogsbay-xml project-health <root>` | no broken links, undefined or unused keys, broken element ids, orphan conref pushes, dangling index redirects, metadata-policy or house-rule violations; house-style formatting and authoring leftovers as warnings |
| 3 | `dita --project=project.json --output=<tmp>` | every deliverable in `project.json` builds; the log is scanned for `Error:` lines and DITA-OT `E`/`F` codes because the build does not always exit non-zero |

Step 2 uses the root map and Schematron configured in `.dogsbay/config.xml`;
step 3 is skipped when the stage has no `project.json` yet.

## Usage

```bash
scripts/check-stage.sh                 # this repo
scripts/check-stage.sh /path/to/stage  # another project root
SKIP_BUILD=1 scripts/check-stage.sh    # skip DITA-OT (fast loop while authoring)
STRICT=0 scripts/check-stage.sh        # project-health at --severity=error only
```

Environment: `DOGSBAY_XML` (path to the `dogsbay-xml` CLI, default
`~/github/dogsbay-xml/bin/dogsbay-xml` or the one on `PATH`), `DITA_HOME` or
`DITA` (default `~/Downloads/dita-ot-4.3.5`), `OUT` (build output directory).

Exit codes: `0` stage OK, `1` a gate failed, `2` a tool was not found.

## Why not xmllint

libxml2 refuses the DITA 1.3 DTDs with "Maximum entity amplification factor
exceeded", even with `--huge`, so DTD validation goes through the DogsBay XML
CLI (Xerces with the DITA-OT catalog).

## Verified behaviour

- On `main` (the deliberately broken demo) the gate fails: 2 invalid files and
  the reference, key, conref-push and index findings listed in `ISSUES.md`.
- On a one-topic project it passes, with and without a map and `project.json`.
- Timing on the full guide: validate about 2 s, health about 2.5 s, the four
  deliverables about 11 s.
