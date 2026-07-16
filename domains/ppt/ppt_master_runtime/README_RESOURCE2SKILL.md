# PPT Master Runtime Adapter

This directory vendors the runnable PPT Master script/runtime subset used by
`domains/ppt/mcp_server/pptmaster_engine.py`.

Upstream:

- Repository: `https://github.com/hugohe3/ppt-master`
- Imported commit: `a8802cedc1477a0fecc7aa276b396508ba85bb79`
- License: MIT, preserved in `LICENSE.ppt-master`

What is included:

- `tools/`: SVG project management, SVG finalization, PPTX template import,
  and SVG to native editable PPTX export.
- `templates/brands`, `templates/layouts`, `templates/charts`, `templates/decks`:
  lightweight bundled template catalogs.

What is intentionally not included:

- `templates/icons/`: the upstream icon bundle is large. The MCP adapter still
  works without it; `pptmaster_export_project(..., finalize=False)` and plain
  SVG source slides do not require the icon bundle. Add the upstream icon
  directory later if decks should use `<use data-icon="...">` placeholders.

The Resource2Skill PPT domain keeps two execution paths:

- Existing `python-pptx` path: `create_presentation`, `add_slide`,
  `add_slide_from_skill`, `add_slide_from_shell`, `replace_slide`,
  `save_presentation`.
- PPT Master path: `pptmaster_create_project`, `pptmaster_add_svg_slide`,
  `pptmaster_replace_svg_slide`, `pptmaster_import_pptx_template`,
  `pptmaster_export_project`.

Keep both paths available. The legacy path is still the runtime for existing
wiki skills; the PPT Master path is an SVG-first backend for editable PPTX
generation and template replication.

Resource2Skill integration policy lives above this vendored runtime. Do not
put fixed skill IDs, fixed deck skeletons, or prompt-specific R2S selection
logic in the PPT Master adapter/runtime. See
`domains/ppt/pptmaster_r2s_integration_contract.md` and validate batch outputs
with `domains/ppt/validate_pptmaster_r2s_run.py` when testing prompt-specific
PPTMaster/R2S runs. The deterministic reference runner is
`domains/ppt/pptmaster_r2s_prompt_runner.py`; it lives outside this vendored
runtime for the same reason.
