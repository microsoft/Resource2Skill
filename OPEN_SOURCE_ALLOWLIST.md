# Open-Source Allowlist

Stage these paths for the public runtime repository:

```bash
git add \
  .gitignore \
  README.md \
  .env.example \
  OPEN_SOURCE_ALLOWLIST.md \
  cli.py \
  core \
  domains \
  skills_library \
  skills_wiki \
  briefs \
  briefs_showcase \
  fixtures \
  examples
```

Do not stage:

```text
experiments/
bench/
reports/
demo/
scripts/
docs/
tests/
main.tex
reference.bib
reference_decks/
mc_demo/
snapshots/
CLAUDE.md
DESIGN.md
```

The public repository is meant to expose the runtime and skill libraries, not
the internal experiment orchestration, scoring, top-80 selection, or paper
drafting workflow.
