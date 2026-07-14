# Recipe: Lo-Fi Study Beat Coordinator

- skill_id: `lofi_study_beat_coordinator`
- confidence: `verified`
- reproducibility: `snippet`

## Mechanism

Use a 75-90 BPM half-time grid, min7/maj9 chord color, swung hats, a warm bass
line following chord roots, and a lead that enters after bar 16. Render with
`style="lofi_hiphop"`.

## Composable Snippet

```python
apply_skill(
    skill_id="lofi_study_beat_coordinator",
    target_id="project",
    kwargs_json='{"bpm": 75, "key": "A", "scale": "minor", "bars": 32}'
)
```
