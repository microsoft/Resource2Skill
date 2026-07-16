# Excel Wiki Primer

Use skills as workbook construction mechanisms, not as demo data to copy.

## Canonical Archetypes

| User need | Canonical skill |
|---|---|
| CFO board scenario model, AI infra forecast, base/upside/downside | `cfo_scenario_board_workbook_archetype` |
| Engineering HR roster, people ops, org tree, comp analysis | `hr_people_ops_workbook_archetype` |
| Battery cycling, lab characterisation, capacity fade | `battery_lab_characterization_workbook_archetype` |
| B2B SaaS pipeline, ARR forecast, sales activity heatmap | `sales_pipeline_tracker_workbook_archetype` |

## Composition Rules

1. Start with one exact-match T5 archetype when available.
2. Add or adapt T3/T4 skills for dashboard layout, KPI cards, charts, formulas,
   conditional formatting, or table styling.
3. Keep source data sheets dense: at least 60 rows for operational data.
4. Dashboard values should reference model/analysis sheets with formulas.
5. If a skill contains placeholder demo numbers, replace them with formulas or
   generated task-specific source data.

## Common Roles

| Role | Search terms |
|---|---|
| Workbook spine | archetype, workbook, scenario, tracker, lab, roster |
| Dashboard | KPI dashboard, chart dashboard, sidebar dashboard, executive summary |
| Chart | line chart, combo chart, bar chart, pie chart, histogram |
| Formatting | currency, percent, date, conditional formatting, data bars |
| Formula model | SUMIFS, XLOOKUP, INDEX MATCH, CHOOSE, SWITCH, rolling average |
