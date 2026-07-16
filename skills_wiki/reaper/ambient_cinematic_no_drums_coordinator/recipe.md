# Recipe: Ambient Cinematic No-Drums Coordinator

- skill_id: `ambient_cinematic_no_drums_coordinator`
- confidence: `verified`
- reproducibility: `snippet`

## Mechanism

Use one full-form coordinator for ambient no-drums briefs. It creates long
sustains across the full bar count and places the sparse piano motif at bars
8, 24, and 40. Do not add drum, snare-roll, trap, boom-bap, or transient-heavy
skills after this coordinator.

## Composable Snippet

```python
apply_skill(
    skill_id="ambient_cinematic_no_drums_coordinator",
    target_id="project",
    kwargs_json='{"bpm": 90, "key": "C", "scale": "minor", "bars": 60}'
)
```
