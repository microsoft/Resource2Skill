# Recipe: Sales Pipeline Tracker Workbook Archetype

- skill_id: `sales_pipeline_tracker_workbook_archetype`
- confidence: `verified`
- reproducibility: `snippet`

## Mechanism

Separate opportunity facts from rep/account dimensions, then use formulas for
weighted pipeline, closed-won rollups, attainment, and heatmap coloring.

## Composable Snippet

```python
apply_skill(
    skill_id="sales_pipeline_tracker_workbook_archetype",
    target_id=workbook_id,
    kwargs_json='{"title": "Enterprise SaaS Pipeline Review"}'
)
```
