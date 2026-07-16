# Recipe: Future Bass Drop Coordinator

- skill_id: `future_bass_drop_coordinator`
- confidence: `verified`
- reproducibility: `snippet`

## Mechanism

Set the brief BPM/key, then build sections: intro, build, drop, breakdown,
final drop. Use half-time drums and a strong 808 only in drops, keep pads wide,
and double the lead an octave up in the final drop.

## Composable Snippet

```python
apply_skill(
    skill_id="future_bass_drop_coordinator",
    target_id="project",
    kwargs_json='{"bpm": 150, "key": "F#", "scale": "minor", "bars": 48}'
)
```
