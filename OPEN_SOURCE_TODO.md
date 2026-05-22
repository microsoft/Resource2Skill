# Open-Source Release TODO

This checklist tracks the remaining work before publishing the public
Resource2Skill repository.

## Blockers

- [x] Add a `LICENSE` file and confirm the license covers code, skill entries,
      generated demo assets, and third-party source-derived skill content.
- [ ] Add citation metadata once the arXiv record is final:
      `CITATION.cff`, README citation block, and paper badge/link.
- [ ] Decide the release boundary for the project page:
      either add `project_page/` plus required `assets/pipeline_overview.png`
      to the public allowlist, or ignore/remove them from the runtime repo and
      publish the page separately.
- [ ] Do a clean-clone smoke test from only tracked files. The current working
      tree contains ignored local domains and artifacts, so `python cli.py
      domains` locally is not identical to a fresh public checkout.
- [ ] Hide, remove, or clearly mark internal/research-only CLI commands such as
      collection, scoring, evolution, harness, and wiki maintenance commands if
      they are not supported in the public release.
- [ ] Add one reproducible dependency entry point (`requirements.txt` or
      `pyproject.toml`) instead of requiring users to copy multiple install
      commands from the README.
- [ ] Track CAD and UE5 as future domains. Keep them out of the initial
      runtime release until data packaging, skill libraries, examples, and
      smoke tests are ready.

## Validation

- [ ] Run `python cli.py domains` in a clean checkout and verify it lists only
      the released public domains.
- [ ] Run:
      `python cli.py validate-domain --domain web`
      `python cli.py validate-domain --domain ppt`
      `python cli.py validate-domain --domain excel`
      `python cli.py validate-domain --domain blender`
      `python cli.py validate-domain --domain reaper`
- [ ] Run `python -m compileall -q cli.py core domains`.
- [ ] Run a no-network or minimal-credential smoke case for at least the web
      domain and capture the expected output path in the README.
- [ ] Verify the README install instructions on a fresh Python 3.10+ virtual
      environment.

## Documentation

- [ ] Add a short "What is not included" section that matches
      `OPEN_SOURCE_ALLOWLIST.md` exactly.
- [ ] Document required external system packages per domain:
      Playwright/Chromium, LibreOffice, Blender, fluidsynth, and soundfonts.
- [ ] Add troubleshooting notes for missing credentials, missing system tools,
      and unavailable visual/audio review hooks.
- [ ] Update `OPEN_SOURCE_ALLOWLIST.md` after deciding whether the project page
      ships with the repo.

## Hygiene

- [ ] Run a final secret scan over the staged release contents.
- [ ] Confirm ignored local artifacts are not staged:
      `experiments/`, `bench/`, `reports/`, `demo/`, `docs/`, `scripts/`,
      `tests/`, paper drafts, snapshots, and local caches.
- [ ] Check public asset size. The runtime tracked files are small, but
      `project_page/` adds many media files if included.
- [ ] Remove stale local `__pycache__/` directories before packaging or rely on
      `.gitignore` in a clean checkout.
