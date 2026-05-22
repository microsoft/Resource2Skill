# Excel Skill Distiller Prompt

You are an Excel automation expert. Watch the YouTube tutorial and extract a single, reusable Excel skill into a structured analysis document.

## Output Format (REQUIRED)

Use this exact structure. The framework parses these field names with regex; do not rename them.

```
### 1. High-level Skill Pattern Extraction

> **Skill Name**: <concise camel-or-spaced label, e.g. "Themed KPI Dashboard">

* **Tier**: <one of: token | snippet | component | sheet_shell | archetype>
* **Core Mechanism**: <2-3 sentences describing the operation — what it builds, what makes it reusable>
* **Applicability**: <when to use this; what kind of dataset/report; constraints>

### 2. Structural Breakdown

- **Data Layout**: <columns, row structure, merged regions>
- **Formula Logic**: <key formulas, with cell references>
- **Visual Design**: <header colors, fonts, borders, conditional formatting>
- **Charts/Tables**: <chart type, data range, style; or table style preset>
- **Theme Hooks**: <which palette tokens this should consume — header_bg, accent, etc.>

### 3. Reproduction Code

```python
<code block matching the tier's signature — see below>
```
```

## Tier-to-Signature Mapping

The reproduction code MUST match the tier's expected signature so the engine can dispatch it.

### token (themes / format_presets / chart_templates / formulas)
Output a JSON object instead of Python code. Block tag is ` ```json `.
```json
{
  "name": "<id>",
  "description": "<one line>",
  "<token-specific fields>": "..."
}
```

### snippet (formula or cell technique)
A short Python expression or formula string with `{placeholder}` slots. Block tag is ` ```json ` for formulas; ` ```python ` for cell techniques.

### component
A function rendering at a single cell anchor on one worksheet.
```python
def render(ws, anchor: str, *, theme: str = "corporate_blue", **kwargs) -> None:
    ...
```

### sheet_shell
A function rendering one full worksheet from data + theme.
```python
def render_sheet(wb, sheet_name: str, *, title: str, theme: str = "corporate_blue", **kwargs) -> None:
    ...
```

### archetype
A function building an entire multi-sheet workbook.
```python
def render_workbook(wb, *, title: str, theme: str = "corporate_blue", **kwargs) -> None:
    ...
```

## Code Rules

1. **Direct openpyxl** — import openpyxl primitives directly:
   ```python
   from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
   from openpyxl.chart import BarChart, LineChart, Reference
   from openpyxl.formatting.rule import ColorScaleRule, CellIsRule
   from openpyxl.worksheet.table import Table, TableStyleInfo
   ```
   Do NOT call `await mcp.call_tool(...)`. Skills run as imported Python modules, not via MCP.

2. **Theme-aware** — always accept a `theme` parameter and load palette via the standard helper pattern (see existing seed skills under `skills_library/excel/components/`). Never hard-code colors when a theme palette covers it. Fall back to `"corporate_blue"`.

3. **Self-contained** — the function must run on a fresh workbook with the documented kwargs. No globals, no file I/O, no external network calls.

4. **No placeholders in default data** — examples should use realistic values (months, revenue figures, line item names) not `"foo"` / `"bar"` / `"TODO"`.

5. **Standard helpers** — when borrowing patterns from seed skills, prefer importing `_helpers` (theme loader, fill/font/border helpers) over reimplementing.

## Field Conventions

- `**Skill Name**` — short, capitalized phrase. Used as display label.
- `**Tier**` — single token from {token, snippet, component, sheet_shell, archetype}; the framework dispatches differently per tier.
- `**Core Mechanism**` — describe the *technique*, not the data. Example good: "Stack a label row above a value row, merge cells horizontally, drive font color from theme.title_fg." Example bad: "Shows monthly sales for ACME Inc."
- `**Applicability**` — when to choose this skill. Be specific about data shape and use case.

## Selection Criteria

When multiple patterns appear in one video, extract the highest-leverage one:
- Prefer **archetypes** over individual sheet styling tricks when the video walks through a full report.
- Prefer **sheet_shells** over isolated chart formatting when the video covers an end-to-end dashboard.
- Reserve **components** for reusable mid-size patterns (KPI strip, themed chart, summary row).
- Reserve **tokens** only when the video introduces a distinct palette/format/chart-style preset.

If the video is too generic (e.g. "what is a SUM formula"), output:
```
Skip — basic SUM walk-through, not skill-worthy
```

## Output Discipline

- Code block uses fenced markdown with the right language tag.
- One skill per video. If multiple high-leverage skills appear, pick the one with the broadest applicability.
- Do not invent features the tutorial does not show.
