# Recipe: Battery Lab Characterisation Workbook Archetype

- skill_id: `battery_lab_characterization_workbook_archetype`
- confidence: `verified`
- reproducibility: `snippet`

## Mechanism

Generate physically plausible cycle rows first, derive rolling capacity and
normalised capacity with formulas, then plot capacity and resistance trends.
Keep unit-bearing headers and correct number formats.

## Composable Snippet

```python
apply_skill(
    skill_id="battery_lab_characterization_workbook_archetype",
    target_id=workbook_id,
    kwargs_json='{"title": "Battery Characterisation Study"}'
)
```
