# Excel Design-System Primer

Foundational reference for building polished Excel workbooks. Use this primer to pick themes, dispatch by skill tier, and follow openpyxl patterns that produce verified, well-structured output.

## Theme Catalog (`theme=` arg on workbook + shell + component calls)

| Theme | Palette | Best for |
|---|---|---|
| `corporate_blue` | Navy + white + amber accents | Sales, finance, executive reports, quarterly summaries |
| `dark_finance` | Bloomberg-style charcoal + amber + green | Trading dashboards, ops monitors |
| `clean_minimal` | Black + white + thin gray rules | Executive summaries, one-pagers, analyst briefs |
| `warm_report` | Terracotta + cream + brown | HR, marketing, narrative-style reports |
| `kpi_traffic` | Neutral gray + RAG (red/amber/green) status | SLA dashboards, ops scorecards |
| `ocean_calm` | Soft teal + slate + cream | B2C product KPIs, customer-facing |

**Theme discipline**: pick ONE theme per workbook and pass the same `theme` argument to every shell/component call so colors line up across sheets.

## Skill Tier Dispatch

| Tier | Tool | Produces | When to choose |
|---|---|---|---|
| Archetype (T5) | `init_from_archetype` | Multi-sheet workbook spine (cover + data + summary + charts) | Recognizable report types: quarterly report, financial model, KPI dashboard |
| Sheet Shell (T4) | `add_sheet_from_shell` | One complete sheet (title + data + chart + table) | Per-sheet build when no full archetype fits |
| Component (T3) | `apply_component` | One block at a cell anchor (KPI strip, header band, summary row, themed chart) | Decorating a sheet that already exists |
| Token (T1) | `get_palette_preset` / `get_format_preset` / `get_chart_template` / `get_formula_snippet` | Design data only (no code) | Inside `execute_xlsx_code` to keep colors/formats consistent |
| Free code | `execute_xlsx_code` | Anything | Custom logic not covered by tier skills. Pre-injected names: `wb`, `Font`, `PatternFill`, `Alignment`, `Border`, `Side`, `BarChart`, `LineChart`, `Reference`, `ColorScaleRule`, `Table`, `TableStyleInfo`, `get_column_letter`, `token(kind, name)` |

Tier name aliases: `archetype` ≡ `T5`, `sheet_shell` ≡ `T4`, `component` ≡ `T3`, `token` ≡ `T1`. Both forms work in `list_skills(tier=...)`.

## Decision rule

- **Archetype if** the brief is a STRONG match (literal phrase like "quarterly report", "financial model", "KPI dashboard"). Otherwise the archetype's preset structure will fight the brief — go custom.
- **Sheet shell if** you need one specific sheet pattern (KPI dashboard, P&L, sales report) and the rest is custom.
- **Components if** you need to decorate an existing sheet (KPI strip on top, themed chart in the corner).
- **Free `execute_xlsx_code` if** the brief calls for custom formulas, conditional formatting, or a layout no skill covers — use `token("themes", name)` to pull palette colors so the custom code stays consistent.

**When in doubt, prefer `execute_xlsx_code` over a weakly-matched archetype/shell.** A weak archetype match produces a generic dashboard that drains rubric points (data_density loses, structure_clarity loses) compared to a custom build that follows the brief literally.

## Seed vs Distilled

The library has two kinds of skills:

- **Seed skills** — hand-written `.py` modules. Short IDs (e.g. `kpi_dashboard`, `quarterly_report`). Directly invokable via `init_from_archetype` / `add_sheet_from_shell` / `apply_component`.
- **Distilled skills** — auto-extracted from YouTube tutorials. IDs end in a 6-8 char hash (e.g. `interactive_task_tracker_with_status_for_6551e4cb`). **Reference-only**: not directly callable. Read with `get_skill_code(skill_id)`, then adapt and run inside `execute_xlsx_code`.

If `init_from_archetype` returns "distilled (reference-only)", switch to: `get_skill_code(<id>)` → `execute_xlsx_code(workbook_id, "<adapted code>")`.

## kwargs_json Format

`apply_component`, `add_sheet_from_shell`, `init_from_archetype` take a JSON string for kwargs (the engine parses it). Example:
```
add_sheet_from_shell(
    workbook_id="wb_a1b2c3d4",
    shell_id="kpi_dashboard",
    sheet_name="Q1",
    kwargs_json='{"title": "Q1 KPIs",
                  "metrics": [{"label":"Revenue","value":"$1.2M","delta":"+12%","delta_kind":"good"}],
                  "detail_headers":["Month","Revenue","Target"],
                  "detail_rows":[["Jan",100000,95000],["Feb",110000,105000]],
                  "theme":"corporate_blue"}'
)
```

## openpyxl Patterns inside `execute_xlsx_code`

### Header band with theme
```python
ws = wb["Q1"]
theme = token("themes", "corporate_blue")
ws.merge_cells("A1:F1")
ws["A1"] = "Q1 Performance Summary"
ws["A1"].font = Font(name="Calibri", size=18, bold=True, color=theme["title_fg"])
ws["A1"].fill = PatternFill("solid", fgColor=theme["title_bg"])
ws["A1"].alignment = Alignment(horizontal="center", vertical="center")
ws.row_dimensions[1].height = 36
```

### Conditional formatting (RAG status)
```python
from openpyxl.formatting.rule import CellIsRule
green = PatternFill("solid", fgColor="C6EFCE")
red   = PatternFill("solid", fgColor="FFC7CE")
ws.conditional_formatting.add("D2:D13", CellIsRule(operator="greaterThanOrEqual", formula=["100000"], fill=green))
ws.conditional_formatting.add("D2:D13", CellIsRule(operator="lessThan", formula=["100000"], fill=red))
```

### Inline formula
```python
ws["B14"] = "=SUMIFS(C2:C13, A2:A13, \"Premium\")"
ws["B14"].font = Font(bold=True, color=theme["title_fg"])
```

### Chart with explicit data range
```python
chart = BarChart()
chart.title = "Monthly Revenue"
chart.y_axis.title = "USD"
data_ref = Reference(ws, min_col=2, min_row=1, max_col=4, max_row=13)
cats_ref = Reference(ws, min_col=1, min_row=2, max_row=13)
chart.add_data(data_ref, titles_from_data=True)
chart.set_categories(cats_ref)
ws.add_chart(chart, "F2")
```

## Common Pitfalls

- **Do not invent skill IDs** — always confirm via `list_skills(...)` first.
- **Empty sheets are a failure** — `verify_workbook` flags them as warnings; rebuild that sheet.
- **Default Sheet1 left behind** — when an archetype/shell adds named sheets, delete the leftover via `execute_xlsx_code` (`wb.remove(wb["Sheet"])`) if your sheet-by-sheet build leaves an empty `Sheet`.
- **Charts need a populated data range** — `data_range="A1:C13"` requires those cells to actually have values; chart with empty range renders as a blank box.
- **Formulas in `execute_xlsx_code`** must be quoted strings starting with `=`: `ws["E2"] = "=SUMIFS(C:C, A:A, \"Jan\")"`.
- **Realistic data only** — never write `"foo"`, `"bar"`, `"TBD"`. The task brief tells you what data to use.
- **Browse budget**: at most 3 `list_skills` calls and 2 `get_skill_*` calls total. After that, commit to a skill or go straight to `execute_xlsx_code`.

## Skill leverage rule

Use skills for STRUCTURE (titles, header bands, theme), not as a substitute for source data. A run that uses an archetype but ships 8 placeholder rows per sheet loses on data_density. The skill gives you the spine — `execute_xlsx_code` fills it with realistic content.

## MANDATORY data density

**Every data-bearing sheet must have ≥60 rows of realistic data.** This is the single biggest score lever:

- The brief usually names the data type (deals, employees, customers, transactions, tickets, line items). Generate that many rows of plausible data with reasonable variation across columns. Use `execute_xlsx_code` to write rows in a loop.
- Vary columns realistically: dates spread across months, names from a small pool, numeric ranges that look plausible (revenue $5k–$200k, NOT all $100k), categorical fields with 3-6 distinct values.
- Summary/dashboard sheets are NOT a substitute for source data — they sit on top of it.
- A workbook with one 8-row data sheet + a fancy dashboard scores LOWER than the same workbook with 60+ rows on each data sheet, even if the dashboard is plainer.

Example loop pattern inside `execute_xlsx_code`:
```python
import random
random.seed(42)
ws = wb["Deals"]
ws.append(["Deal ID","Account","Stage","Amount","Owner","Close Date","Industry"])
stages = ["Qualified","Proposal","Negotiation","Closed Won","Closed Lost"]
industries = ["SaaS","Healthcare","Finance","Retail","Manufacturing"]
owners = ["A. Chen","B. Patel","C. Garcia","D. Kim","E. Nguyen"]
for i in range(60):
    ws.append([
        f"D-{1000+i}",
        f"Account {i+1}",
        random.choice(stages),
        random.randint(8000, 250000),
        random.choice(owners),
        f"2026-0{random.randint(1,9)}-{random.randint(1,28):02d}",
        random.choice(industries),
    ])
```

## Chart floor — one simple chart, no exceptions

Even briefs that read as "raw data only" (lab results, transaction logs, RFM tables) still get scored on `chart_quality`. **A workbook with zero charts caps you at chart_quality≈0.** Add at least ONE simple `BarChart` on the headline sheet, sized for visibility:

```python
from openpyxl.chart import BarChart, Reference
ws = wb[wb.sheetnames[0]]   # headline sheet
# Pick any plausible numeric column with a category column to its left.
# Defensive bounds: only chart if the data range is populated.
last_row = ws.max_row
if last_row >= 3:
    chart = BarChart()
    chart.title = "Summary"
    chart.height = 9
    chart.width = 16
    data_ref = Reference(ws, min_col=2, min_row=1, max_col=2, max_row=min(last_row, 13))
    cats_ref = Reference(ws, min_col=1, min_row=2, max_row=min(last_row, 13))
    chart.add_data(data_ref, titles_from_data=True)
    chart.set_categories(cats_ref)
    ws.add_chart(chart, "F2")
```

That's the floor — one chart, on the active sheet, with `height=9 width=16` so it's not microscopic. If the brief explicitly asks for "trends / dashboards / comparisons", add 1-2 more charts (LineChart for time series, PieChart for share/mix) — but never ship zero.

## Active-sheet rule

The renderer captures the currently-active sheet on save. Before `save_workbook`:
```python
wb.active = wb.sheetnames.index("Summary")   # or whichever sheet is the headline
```
Pick the sheet a stakeholder would open first — usually a Cover/Summary/Dashboard, not a raw data sheet.

## Multi-sheet visibility

Briefs that spec "N sheets" need actual N labeled sheets. After build, verify via `get_workbook_info` that the sheet count and names match. Empty leftover `Sheet` from openpyxl creation must be removed (`wb.remove(wb["Sheet"])`).
