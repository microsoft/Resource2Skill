# Recipe: CFO Scenario Board Workbook Archetype

- skill_id: `cfo_scenario_board_workbook_archetype`
- confidence: `verified`
- reproducibility: `snippet`

## Mechanism

Centralize assumptions in `Inputs`, derive monthly revenue and costs from
those assumptions, summarize Base/Upside/Downside in a matrix, then reference
that matrix from the dashboard and board callouts.

## Composable Snippet

```python
apply_skill(
    skill_id="cfo_scenario_board_workbook_archetype",
    target_id=workbook_id,
    kwargs_json='{"title": "AI Infrastructure Board Scenario Model"}'
)
```
