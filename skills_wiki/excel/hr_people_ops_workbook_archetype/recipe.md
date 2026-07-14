# Recipe: HR People-Ops Workbook Archetype

- skill_id: `hr_people_ops_workbook_archetype`
- confidence: `verified`
- reproducibility: `snippet`
- related: dashboard KPI shells, conditional-formatting components, chart components

## Mechanism

Create source data first (`Headcount`), derived hierarchy second (`Org Tree`),
analysis tables third (`Comp Analysis`), and presentation last (`Insights
Dashboard`). Keep all executive numbers formula-backed.

## Composable Snippet

```python
apply_skill(
    skill_id="hr_people_ops_workbook_archetype",
    target_id=workbook_id,
    kwargs_json='{"title": "Engineering People Ops Review"}'
)
```
